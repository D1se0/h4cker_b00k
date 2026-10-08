---
icon: album-collection-circle-user
layout:
  width: default
  title:
    visible: true
  description:
    visible: false
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
  metadata:
    visible: true
  tags:
    visible: true
  actions:
    visible: true
  anchors:
    visible: true
---

# Triage collections y artefactos (Velociraptor/KAPE)

> Cada vez más retos (y más IRs reales) te dan en lugar de una imagen de disco una **colección triage**: un ZIP/7z con artefactos seleccionados generada por **Velociraptor** (`Windows.KapeFiles.Targets` / `Windows.Triage.Targets`) o **KAPE**. Saber reconocer y parsear cada artefacto es la clave.

## Cómo reconocer un triage

Tras descomprimir:

```bash
7z x UnderZer0_incident_xxx.7z -oextracted
ls extracted/
```

Estructura típica:

```
Windows.KapeFiles.Targets/
├── All File Metadata.json        ← NDJSON con metadatos de cada fichero
├── Uploads.json                  ← NDJSON con lista de uploads
C/
├── Windows/
│   ├── System32/config/          ← Hives del registro (SYSTEM, SOFTWARE, SAM)
│   ├── System32/winevt/Logs/     ← .evtx (Sysmon, Security, System, ...)
│   └── Prefetch/                 ← *.pf  (¡CLAVE en muchos retos!)
└── Users/<user>/
    ├── AppData/Roaming/Microsoft/Windows/PowerShell/PSReadline/
    │   └── ConsoleHost_history.txt
    └── AppData/Roaming/Microsoft/Windows/Recent/   ← *.lnk
```

**Regla rápida:** si ves `All File Metadata.json` o `Windows.KapeFiles.Targets` → es un triage; no uses Volatility ni TSK.

## Primer paso SIEMPRE: el historial de PowerShell

```bash
cat "C/Users/<user>/AppData/Roaming/Microsoft/Windows/PowerShell/PSReadline/ConsoleHost_history.txt"
```

Es texto plano y suele dar el mejor indicio del caso (comandos ejecutados, binarios que el usuario inspeccionó, herramientas de limpieza…).

## EVTX — Logs de eventos Windows

### Opción A · python-evtx (Python puro)

```bash
pip install python-evtx
```

```bash
# Volcar a XML (patrón habitual):
{
  echo '<?xml version="1.0" encoding="utf-8"?>'
  echo '<Events>'
  python3 -c "
import Evtx.Evtx as evtx
with evtx.Evtx('System.evtx') as log:
    for r in log.records():
        print(r.xml())
"
  echo '</Events>'
} > all.xml
```

### Opción B · evtx\_dump (Rust, mucho más rápido en logs grandes)

```bash
# Instalación: https://github.com/omerbenamram/EVTX (binario precompilado)
evtx_dump file.evtx > out.jsonl           # JSON Lines
evtx_dump -o xml file.evtx > out.xml
```

### Eventos Sysmon que importan

| EID   | Significado              | Qué buscar                                       |
| ----- | ------------------------ | ------------------------------------------------ |
| 1     | Process Creation         | `CommandLine`, `CurrentDirectory`, `ParentImage` |
| 3     | Network Connection       | Proceso que se conecta a qué IP:puerto           |
| 5     | Process Terminate        | Duración del proceso                             |
| 7     | Image Load               | DLLs cargadas (orden = orden real de arranque)   |
| 11    | FileCreate               | Qué proceso creó qué fichero                     |
| 13    | Registry Set             | Persistencia en `Run`/`RunOnce`                  |
| 15    | FileCreateStreamHash     | ADS `Zone.Identifier` (fichero descargado)       |
| 17/18 | Pipe Created/Connected   | `PSHost` pipe = PowerShell interactivo           |
| 22    | DNS Query                | Dominios consultados por proceso                 |
| 23    | FileDelete               | Borrado de ficheros (anti-forense)               |
| 29    | File Executable Detected | Creación de un PE (exe/dll)                      |

### Filtrado con Python (probado)

```python
import xml.etree.ElementTree as ET

NS = "{http://schemas.microsoft.com/win/2004/08/events/event}"
STAGING = ("\\Temp\\", "\\Downloads\\")     # rutas sospechosas

for _, event in ET.iterparse("all.xml", events=("end",)):
    if event.tag != f"{NS}Event":
        continue
    sys_ = event.find(f"{NS}System")
    eid = sys_.find(f"{NS}EventID").text
    if eid != "1":
        event.clear(); continue
    data = {d.get("Name"): d.text for d in event.iter(f"{NS}Data")}
    cwd = data.get("CurrentDirectory", "") or ""
    cmd = data.get("CommandLine", "") or ""
    if any(s in cwd for s in STAGING) or any(s in cmd for s in STAGING):
        ts = sys_.find(f"{NS}TimeCreated").get("SystemTime")
        print(f"[{ts}] PID {data.get('ProcessId')}  {data.get('Image')}")
        print(f"    cmd = {cmd}")
        print(f"    parent = {data.get('ParentImage')} (PID {data.get('ParentProcessId')})")
    event.clear()
```

### Caso práctico: detectar PowerShell "sin pipe PSHost"

Un PowerShell **interactivo legítimo** genera un EID 17 con el pipe `PSHost`. Un PowerShell usado para ejecutar payload sin interacción **no lo crea**:

```python
import xml.etree.ElementTree as ET
NS = "{http://schemas.microsoft.com/win/2004/08/events/event}"

ps_pids = {"4236", "6076"}      # PIDs de powershell.exe vistos en EID 1
pshost_pids = set()

with open("all.xml", "rb") as f:
    for _, ev in ET.iterparse(f, events=("end",)):
        if ev.tag != f"{NS}Event":
            continue
        if ev.find(f"{NS}System").find(f"{NS}EventID").text != "17":
            ev.clear(); continue
        data = {d.get("Name"): d.text for d in ev.iter(f"{NS}Data")}
        if "PSHost" in (data.get("PipeName") or ""):
            pshost_pids.add(data.get("ProcessId"))
        ev.clear()

print("Legítimos:", pshost_pids)
print("Sospechosos:", ps_pids - pshost_pids)     # ← el malicioso
```

## Prefetch (Windows) — evidencia de ejecución

Los `.pf` de Windows 10/11 van en `C:\Windows\Prefetch\*.pf`, empiezan con la firma **`MAM\x04`** y están comprimidos con **LZXPRESS-Huffman**. Con `strings` verás basura: hay que descomprimir.

### Parser con dissect (probado)

```bash
pip install dissect
```

```python
from dissect.util.compression import lzxpress_huffman
import struct
from datetime import datetime, timedelta, timezone

def filetime_to_dt(ft):
    if ft == 0:
        return None
    return datetime(1601, 1, 1, tzinfo=timezone.utc) + timedelta(microseconds=ft // 10)

raw = open("RUNDLL32.EXE-F72EA656.pf", "rb").read()
assert raw.startswith(b"MAM"), "no es un .pf de Win10+"
decompressed = lzxpress_huffman.decompress(raw[8:])   # 8 = firma+versión

# Strings de ficheros/directorios tocados (UTF-16LE)
s = decompressed.decode("utf-16-le", errors="ignore").upper()
print(s[:2000])

# Última ejecución: FILETIME en offset 0x80 del buffer DESCOMPRIMIDO
last_run = struct.unpack_from("<Q", decompressed, 0x80)[0]
print("Última ejecución:", filetime_to_dt(last_run))

# Histórico de hasta 8 ejecuciones (Win8.1+) a partir de 0x80
for i in range(8):
    ft = struct.unpack_from("<Q", decompressed, 0x80 + i*8)[0]
    dt = filetime_to_dt(ft)
    if dt and 2000 < dt.year < 2030:
        print(f"  Run {i+1}: {dt}")
```

### Alternativas CLI

* **PECmd** (Eric Zimmerman): `PECmd.exe -d C:\Windows\Prefetch --csv .`
* **WinPrefetchView** (NirSoft, GUI, Windows).

### Cómo interpretar Prefetch

1. El nombre del `.pf` (`RUNDLL32.EXE-F72EA656.pf`) indica el binario ejecutado + hash de la ruta.
2. La lista de ficheros tocados revela **argumentos de línea de comandos**: si `rundll32` tocó `\Users\<user>\AppData\Local\Temp\PAYLOAD.DAT`, es que ese fichero fue pasado como argumento (T1218.011).
3. La pila de DLLs (`wininet`, `urlmon`, `winhttp`, `ws2_32`) tras la carga del fichero → actividad de red → posible C2.
4. Si `WerFault.exe` (Windows Error Reporting) tocó el mismo fichero → el proceso **crasheó**, y WER registró los ficheros implicados.

## Registro de Windows (hives)

```bash
pip install regipy
```

```python
from regipy.registry import RegistryHive
reg = RegistryHive("C/Windows/System32/config/SYSTEM")
for entry in reg.recurse_subkeys(reg.get_key("\\ControlSet001\\Services")):
    print(entry.path, entry.values)
```

```bash
# Alternativa CLI
regipy-dump SYSTEM | grep -i "wsock32"
```

### Hives que importan

| Hive           | Qué contiene                                           |
| -------------- | ------------------------------------------------------ |
| `SYSTEM`       | Servicios, dispositivos, control sets, timezone        |
| `SOFTWARE`     | Apps instaladas, `Run` global, info del sistema        |
| `SAM`          | Usuarios locales (hashes NTLM si el reto lo permite)   |
| `NTUSER.DAT`   | Por usuario: RecentDocs, RunMRU, Shellbags, UserAssist |
| `UsrClass.dat` | Shellbags (por usuario)                                |
| `Amcache.hve`  | Evidencia de ejecución: SHA1 de cada binario ejecutado |

## LNK / Shell Items — accesos recientes

```bash
pip install dissect.shellitem
```

```python
import glob
from dissect.shellitem.lnk import Lnk

for path in glob.glob("C/Users/*/AppData/Roaming/Microsoft/Windows/Recent/*.lnk"):
    try:
        with open(path, "rb") as f:
            lnk = Lnk(f)
        if lnk.linkinfo:
            target = lnk.linkinfo.local_base_path or b""
            target += lnk.linkinfo.common_path_suffix or b""
        else:
            target = b"(sin linkinfo)"
        print(f"{path.split('/')[-1]:40s} → {target}")
    except Exception as e:
        print(f"{path}: ERROR {e}")
```

**Un LNK guarda mucho más que la ruta:** máquina donde se creó (TrackerDataBlock → MachineID), volumen (serial), fechas (acceso/creación/escritura del target), tamaño, y —lo más interesante en retos— los **argumentos de línea de comandos**, a veces ofuscados con el patrón `%var:~N,1%` de `cmd.exe` (ver decodificador en [05 · Scripts](05-scripts-genericos.md)).

## Navegadores

```bash
# Historial Chrome/Brave/Edge (SQLite)
cp "C/Users/<user>/AppData/Local/Google/Chrome/User Data/Default/History" hist.db
sqlite3 hist.db "SELECT url, title, visit_count, datetime(last_visit_time/1000000-11644473600, 'unixepoch') FROM urls ORDER BY last_visit_time DESC LIMIT 50;"

# Hindsight automatiza todo esto (Chrome + Firefox + Edge):
pip install hindsight
hindsight -i "C/Users/<user>/AppData/Local/Google/Chrome/User Data/Default/History" -o salida.xlsx
```

## Cookies, descargas y ZIPs

```bash
# Ficheros descargados (con URL de origen)
sqlite3 hist.db "SELECT target_path, tab_url FROM downloads;"

# ZIP con contraseña: probar con la del enunciado o crackear con john
7z l suspicious.zip
zip2john suspicious.zip > hash.txt
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
```

## Checklist final de triage

1. ☐ `ConsoleHost_history.txt` de todos los usuarios
2. ☐ Procesos: `Windows.System.Pslist.json` (NDJSON)
3. ☐ Prefetch: buscar rutas fuera de `\Windows\` y `\Program Files\`
4. ☐ Recent/\*.lnk con `dissect.shellitem`
5. ☐ EVTX de Sysmon: EID 1 con `CurrentDirectory` en `\Temp\` o `\Downloads\`
6. ☐ Hives: `Run`/`RunOnce` en SOFTWARE y NTUSER.DAT, Amcache para SHA1
7. ☐ Correlacionar timestamps y construir una timeline única
