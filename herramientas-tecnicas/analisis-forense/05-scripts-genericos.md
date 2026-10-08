# 05 · Scripts genéricos Python3 listos para usar

> Todos los scripts de esta página han sido **ejecutados y verificados** en un entorno con `pytsk3`, `dissect`, `python-registry` y `python-evtx`. Instala las dependencias con:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install pytsk3 dissect python-registry python-evtx
```

---

## 1 · Listar y extraer ficheros de una imagen de disco (pytsk3)

Ajusta `IMAGE_PATH` y `OFFSET_BYTES` (offset de la partición en bytes, `startsector × 512`).

```python
#!/usr/bin/env python3
"""fs_walk.py — Lista recursivamente y extrae ficheros de una imagen de disco.
   Uso:
       python3 fs_walk.py imagen.img              # listar
       python3 fs_walk.py imagen.img --extract 42 # extraer inodo 42
"""
import pytsk3, sys, argparse

SISTEMA = (b'.', b'..', b'lost+found', b'$OrphanFiles',
           b'$AttrDef', b'$BadClus', b'$Bitmap', b'$Boot', b'$Extend',
           b'$LogFile', b'$MFT', b'$MFTMirr', b'$Secure', b'$UpCase', b'$Volume')

def walk(fs, path="/", indent=0):
    dir_ = fs.open_dir(path=path)
    out = []
    for entry in dir_:
        if entry.info.name.name in SISTEMA:
            continue
        name = entry.info.name.name.decode(errors='replace')
        meta = entry.info.meta
        if meta is None:
            print(f"{' '*indent}?  ino=0    /{name}  (BORRADO, sin meta)")
            continue
        tipo = 'F' if meta.type == pytsk3.TSK_FS_META_TYPE_REG else 'D'
        borrado = entry.info.name.flags == pytsk3.TSK_FS_NAME_FLAG_UNALLOC
        nota = " (BORRADO)" if borrado else ""
        line = f"{' '*indent}{tipo}  ino={meta.addr:<6} size={meta.size:<10} /{name}{nota}"
        print(line)
        out.append((meta.addr, f"{path}/{name}" if path != '/' else f"/{name}", meta.size))
        if meta.type == pytsk3.TSK_FS_META_TYPE_DIR and not borrado:
            out += walk(fs, f"{path}/{name}" if path != '/' else f"/{name}", indent+4)
    return out

def extract(fs, inode, out_path):
    f = fs.open_meta(inode=inode)          # ¡argumento nombrado!
    size = f.info.meta.size
    data = f.read_random(0, size)
    with open(out_path, "wb") as o:
        o.write(data)
    print(f"[+] Extraído inodo {inode} ({size} bytes) → {out_path}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--offset", type=int, default=0, help="offset partición en BYTES")
    ap.add_argument("--extract", type=int, default=None, help="inodo a extraer")
    ap.add_argument("-o", "--out", default="extraido.bin")
    args = ap.parse_args()

    img = pytsk3.Img_Info(args.image)
    fs = pytsk3.FS_Info(img, offset=args.offset)
    if args.extract is not None:
        extract(fs, args.extract, args.out)
    else:
        walk(fs, "/")
```

---

## 2 · Carving por firma + parseo de LNK

```python
#!/usr/bin/env python3
"""carve_lnk.py — Busca cabeceras de .lnk en una imagen cruda y las parsea.
   Uso: python3 carve_lnk.py imagen.img
"""
import re, io, sys
from dissect.shellitem.lnk import Lnk

LNK_SIG = bytes.fromhex("4c0000000114020000000000c000000000000046")

def find_offsets(data, sig):
    return [m.start() for m in re.finditer(re.escape(sig), data)]

def carve(image, offsets, block=4096):
    with open(image, "rb") as f:
        for off in offsets:
            f.seek(off)
            blob = f.read(block)
            try:
                lnk = Lnk(io.BytesIO(blob))
                print(f"\n=== LNK @ 0x{off:08X} ===")
                for k, v in lnk.stringdata.string_data.items():
                    print(f"  {k}: {v.string!r}")
            except Exception as e:
                print(f"  0x{off:08X}: no parsea ({e})")

if __name__ == "__main__":
    img = sys.argv[1]
    data = open(img, "rb").read()
    offs = find_offsets(data, LNK_SIG)
    print(f"[+] {len(offs)} firma(s) de LNK encontradas")
    carve(img, offs)
```

---

## 3 · Decodificador genérico del patrón `%var:~N,1%` (cmd.exe)

Aparece constantemente en LNK maliciosos. Ajusta el nombre de la variable y el alfabeto si difieren.

```python
#!/usr/bin/env python3
"""decode_cmd_substring.py — Decodifica comandos ofuscados con subcadenas de cmd.exe.
   Uso: pega el valor de command_line_arguments en CMDLINE y ejecuta.
"""
import re

a85a = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
VAR = "a85a"

CMDLINE = "/c Set a85a=0123456789abcdef & %a85a:~11,1%%a85a:~18,1%"

decoded = re.sub(
    rf"%{VAR}:~(\d+),1%",
    lambda m: a85a[int(m.group(1))] if int(m.group(1)) < len(a85a) else "?",
    CMDLINE,
)
# Quitar el prefijo "Set VAR=... & " si existe
if f"Set {VAR}=" in decoded:
    decoded = decoded.split("&", 1)[1].strip()

print(decoded)
```

---

## 4 · Parser de Prefetch (.pf de Windows 10/11)

```python
#!/usr/bin/env python3
"""parse_prefetch.py — Descomprime y parsea ficheros .pf (MAM\x04) de un directorio.
   Uso: python3 parse_prefetch.py C/Windows/Prefetch/ [filtro]
"""
import glob, struct, sys
from datetime import datetime, timedelta, timezone
from dissect.util.compression import lzxpress_huffman

def filetime_to_dt(ft):
    if ft == 0:
        return None
    return datetime(1601, 1, 1, tzinfo=timezone.utc) + timedelta(microseconds=ft // 10)

def parse_pf(path):
    raw = open(path, "rb").read()
    if not raw.startswith(b"MAM"):
        return None, None
    buf = lzxpress_huffman.decompress(raw[8:])
    s = buf.decode("utf-16-le", errors="ignore").upper()
    runs = []
    for i in range(8):
        ft = struct.unpack_from("<Q", buf, 0x80 + i*8)[0]
        dt = filetime_to_dt(ft)
        if dt and 2000 < dt.year < 2030:
            runs.append(dt)
    return s, runs

if __name__ == "__main__":
    pattern = sys.argv[1] if len(sys.argv) > 1 else "C/Windows/Prefetch/*.pf"
    filtro = sys.argv[2].upper() if len(sys.argv) > 2 else None
    for p in sorted(glob.glob(pattern)):
        s, runs = parse_pf(p)
        if s is None:
            continue
        if filtro and filtro not in s:
            continue
        print(f"\n=== {p} ===")
        if runs:
            print(f"  Última ejecución: {runs[0]}")
        # Ficheros tocados: líneas tipo \DEVICE\...\FICHERO.EXT
        import re
        for m in sorted(set(re.findall(r"\\[^\\/\x00\r\n]{2,120}\.[A-Z0-9]{1,5}", s))):
            print("   ", m)
```

### Escaneo masivo de staging en %TEMP% / %DOWNLOADS%

```python
#!/usr/bin/env python3
"""scan_prefetch_staging.py — Detecta ficheros ejecutados directamente desde
   %TEMP% o %DOWNLOADS% (patrón típico de droppers).
   Uso: python3 scan_prefetch_staging.py "C/Windows/Prefetch/*.pf"
"""
import glob, re
from collections import Counter
from dissect.util.compression import lzxpress_huffman

EXCLUIR = ("\\WINDOWS\\", "\\PROGRAM FILES", "\\PROGRAMDATA\\",
           "\\$RECYCLE", "\\APPDATA\\LOCAL\\PACKAGES\\",
           "\\APPDATA\\ROAMING\\MICROSOFT\\", "\\APPDATA\\LOCAL\\MICROSOFT\\")
STAGING = ("\\TEMP\\", "\\DOWNLOADS\\", "\\TMP\\")
PATTERN = re.compile(r"\\[^\x00\r\n]{4,250}\.[A-Z0-9]{2,5}(?=[\\\x00\s,;]|$)", re.I)

freq, detalle = Counter(), {}
for p in sorted(glob.glob("C/Windows/Prefetch/*.pf")):
    raw = open(p, "rb").read()
    if not raw.startswith(b"MAM"):
        continue
    s = lzxpress_huffman.decompress(raw[8:]).decode("utf-16-le", errors="ignore").upper()
    for m in PATTERN.findall(s):
        if any(x in m for x in EXCLUIR):
            continue
        fname = m.rsplit("\\", 1)[-1]
        parent = m.rsplit("\\", 2)[-2] if "\\" in m else ""
        if not any(st in m for st in STAGING):
            continue
        if parent not in ("TEMP", "DOWNLOADS", "TMP"):
            continue
        freq[fname] += 1
        detalle.setdefault(fname, set()).add(p)

for fname, n in freq.most_common(40):
    print(f"[{n} pf] {fname}")
    for pf in sorted(detalle[fname]):
        print(f"    → {pf.split('/')[-1]}")
```

---

## 5 · EVTX a XML + filtros Sysmon

### Volcado completo a XML

```bash
{
  echo '<?xml version="1.0" encoding="utf-8"?>'
  echo '<Events>'
  python3 -c "
import Evtx.Evtx as evtx
with evtx.Evtx('johnnycab_1990.evtx') as log:
    for r in log.records():
        print(r.xml())
"
  echo '</Events>'
} > all.xml
```

### Filtro de procesos creados desde staging (EID 1)

```python
#!/usr/bin/env python3
"""sysmon_filter.py — Filtra eventos Sysmon del XML volcado.
   Uso: python3 sysmon_filter.py all.xml
"""
import xml.etree.ElementTree as ET

NS = "{http://schemas.microsoft.com/win/2004/08/events/event}"
STAGING = ("\\Temp\\", "\\Downloads\\", "\\AppData\\Local\\Temp\\")

for _, ev in ET.iterparse("all.xml", events=("end",)):
    if ev.tag != f"{NS}Event":
        continue
    sys_ = ev.find(f"{NS}System")
    eid = sys_.find(f"{NS}EventID").text
    data = {d.get("Name"): d.text for d in ev.iter(f"{NS}Data")}
    cwd = data.get("CurrentDirectory", "") or ""
    cmd = data.get("CommandLine", "") or ""
    if eid == "1" and (any(s in cwd for s in STAGING) or any(s in cmd for s in STAGING)):
        ts = sys_.find(f"{NS}TimeCreated").get("SystemTime")
        print(f"[{ts}] PID {data.get('ProcessId')}  {data.get('Image')}")
        print(f"    cwd    = {cwd}")
        print(f"    cmd    = {cmd}")
        print(f"    parent = {data.get('ParentImage')} (PID {data.get('ParentProcessId')})\n")
    ev.clear()
```

### Traza de ciclo de vida de un PID (EID 1 → EID 7 → EID 5)

```python
#!/usr/bin/env python3
"""pid_trace.py — Imprime todos los eventos Sysmon de un PID concreto.
   Uso: python3 pid_trace.py all.xml 6076
"""
import sys, xml.etree.ElementTree as ET
NS = "{http://schemas.microsoft.com/win/2004/08/events/event}"
TARGET = sys.argv[2]

with open(sys.argv[1], "rb") as f:
    for _, ev in ET.iterparse(f, events=("end",)):
        if ev.tag != f"{NS}Event":
            continue
        sys_ = ev.find(f"{NS}System")
        eid = sys_.find(f"{NS}EventID").text
        data = {d.get("Name"): d.text for d in ev.iter(f"{NS}Data")}
        pid = data.get("ProcessId") or data.get("ProcessID")
        if pid == TARGET:
            ts = sys_.find(f"{NS}TimeCreated").get("SystemTime")
            print(f"EID {eid:>3}  {ts}  Image={data.get('Image')}  Rule={data.get('RuleName')}")
        ev.clear()
```

---

## 6 · Parser del NDJSON de procesos de Velociraptor

```python
#!/usr/bin/env python3
"""pslist_ndjson.py — Parsea Windows.System.Pslist.json de un triage.
   Uso: python3 pslist_ndjson.py Windows.System.Pslist.json [filtro_nombre]
"""
import json, sys

FILTRO = sys.argv[2].lower() if len(sys.argv) > 2 else None

for line in open(sys.argv[1]):
    o = json.loads(line)
    if FILTRO and FILTRO not in o.get("Name", "").lower():
        continue
    print(f"PID {o.get('Pid'):>6}  PPID {o.get('Ppid'):>6}  {o.get('Name')}")
    if o.get("CommandLine"):
        print(f"        cmd: {o['CommandLine']}")
    if o.get("Exe"):
        print(f"        exe: {o['Exe']}")
```

---

## 7 · Búsqueda de dominios / URLs en cualquier evidencia

```python
#!/usr/bin/env python3
"""ioc_hunt.py — Extrae dominios y URLs de ASCII+UTF-16LE de un fichero binario.
   Uso: python3 ioc_hunt.py imagen.img
"""
import re, sys

data = open(sys.argv[1], "rb").read()

# ASCII
ascii_blob = data.decode("latin-1", errors="ignore")
# UTF-16LE: los caracteres ASCII quedan separados por \x00
utf16_blob = data.decode("utf-16-le", errors="ignore")

DOMAIN = re.compile(r"\b(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}\b", re.I)
URL    = re.compile(r"\bhttps?://[^\s\"'<>]{4,}", re.I)

for label, blob in (("ASCII", ascii_blob), ("UTF-16LE", utf16_blob)):
    print(f"--- {label} ---")
    for m in sorted(set(m.group(0).lower() for m in DOMAIN.finditer(blob))):
        print("  dom:", m)
    for m in sorted(set(m.group(0) for m in URL.finditer(blob))):
        print("  url:", m)
```

---

## 8 · Utilidades varias

### Hash en el formato flag

```bash
printf 'dominio-malicioso.ejemplo' | md5sum
printf 'fichero_malicioso.dat' | md5sum
python3 -c "import hashlib; print(hashlib.md5(b'6076').hexdigest())"   # ej.: hash de un PID
```

### Prueba negativa de IOC (demostrar ofuscación)

```bash
grep -aobc "bitsadmin" imagen.img         # → 0 (no existe en claro)
grep -aobc "dominio-malicioso" imagen.img # → 0 (solo se materializa al decodificar)
```

### Verificar si un .pf está comprimido o crudo

```bash
xxd -l 4 fichero.pf
# "MAM\004" → Win10/11, comprimido (usar script §4)
# Otra cosa  → Win7/8, formato crudo (se puede strings directamente)
```

### Extraer el contenido de un ADS de NTFS

```bash
icat -o 64 imagen.img 42-128 > zone_identifier.txt
```
