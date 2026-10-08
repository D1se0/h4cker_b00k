# 04 · Carving y recuperación de datos

> **Carving** = recuperar ficheros que ya no tienen inodo válido (borrados, fragmentados o huérfanos) buscando **firmas** en los bytes crudos de la imagen. Es la técnica que salva retos donde `fls` no muestra nada útil.

## Cuándo necesitas carving

- El fichero aparece en `fls` marcado con `*` (borrado) y `icat` devuelve basura o nada.
- El fichero ni siquiera aparece listado pero sabes que existió.
- El fichero está **fragmentado** y las estructuras del FS están dañadas.
- Buscas payloads embebidos dentro de otros ficheros (PDFs con EXEs, imágenes con ZIPs…).

## Firmas clave que conviene memorizar

| Firma (hex) | Tipo |
|---|---|
| `4C 00 00 00` + GUID `00021401-0000-0000-C000-000000000046` | Windows Shortcut (.LNK) |
| `4D 5A` (`MZ`) | Ejecutable Windows (PE) |
| `7F 45 4C 46` (`\x7fELF`) | Ejecutable Linux |
| `50 4B 03 04` (`PK`) | ZIP / DOCX / XLSX / JAR |
| `1F 8B 08` | GZIP |
| `42 4D` (`BM`) | BMP |
| `FF D8 FF` | JPEG |
| `89 50 4E 47` (`\x89PNG`) | PNG |
| `52 61 72 21` (`Rar!`) | RAR |
| `4D 41 4D 04` (`MAM\x04`) | Prefetch Windows 10/11 |
| `4C 69 4D 45` (`LiME`) | Volcado de memoria LiME |
| `25 50 44 46` (`%PDF`) | PDF |
| `37 7A BC AF 27 1C` | 7-Zip |
| `46 49 4C 45` + `N/4` alternando | Cabecera MFT (NTFS) |
| `D0 CF 11 E0 A1 B1 1A E1` | OLE (DOC/XLS antiguos, MSI) |

## Carving manual con Python (método quirúrgico)

Cuando sabes **exactamente** qué firma buscas, un script propio es más preciso que herramientas genéricas. Ejemplo real: recuperar un `.lnk` borrado de un USB NTFS:

```python
import re

with open("usb_mnt20202703.img", "rb") as f:
    data = f.read()

# Firma de un Shell Link (LNK): 4C 00 00 00 + GUID 00021401-...
sig = bytes.fromhex("4c0000000114020000000000c000000000000046")

offsets = [m.start() for m in re.finditer(re.escape(sig), data)]
print(f"Ocurrencias: {len(offsets)}")
for off in offsets:
    print(f"  0x{off:08X}")
```

Luego extraes un bloque razonable desde ese offset y lo parseas:

```python
from dissect.shellitem.lnk import Lnk
import io

IMAGE_PATH = "usb_mnt20202703.img"
LNK_OFFSET = 0x1B8EF000
BLOCK_SIZE = 4096

with open(IMAGE_PATH, "rb") as f:
    f.seek(LNK_OFFSET)
    lnk_data = f.read(BLOCK_SIZE)

with open("desktop_carved.lnk", "wb") as f:
    f.write(lnk_data)

lnk = Lnk(io.BytesIO(lnk_data))
for k, v in lnk.stringdata.string_data.items():
    print(k, "→", v.string)
```

> **Lección práctica:** si el espacio sin asignar no está sobrescrito, el LNK borrado suele quedar **íntegro y sin fragmentar**, por lo que un bloque de 4096 bytes basta. Si el `stringdata` sale truncado o con basura, el fichero está fragmentado → busca la siguiente firma o usa herramientas de carving con reensamblado.

## Carving automático

### foremost / foremost-ng

```bash
sudo apt install foremost
foremost -i imagen.img -o salida/ -t jpg,png,pdf,zip
```

### binwalk (embebidos, ideal para firmware y ficheros anidados)

```bash
binwalk imagen.img            # Solo escaneo: ver qué hay
binwalk -e imagen.img         # Extrae todo lo que reconozca
binwalk --dd="zip:zip" imagen.img   # Extrae solo ZIPs
```

### photorec (GUI por terminal, muy eficaz con imágenes)

```bash
photorec imagen.img   # seguir el asistente: elegir partición → tipo de fichero → destino
```

### scalpel (sucesor moderno de foremost)

```bash
scalpel imagen.img -o salida/    # config en /etc/scalpel/scalpel.conf
```

## Búsqueda con `grep` sobre imagen cruda

Más rápido que cualquier carving cuando solo buscas **textos**:

```bash
# -a trata el binario como texto; -o imprime el match; -b muestra el offset en bytes
grep -aob "flag{" imagen.img
grep -aobE "https?://[a-zA-Z0-9./-]+" imagen.img | head

# Prueba NEGATIVA: si devuelve 0, el IOC NO está en claro (prueba de ofuscación)
grep -aobc "bitsadmin" imagen.img         # → 0 (no existe en claro)
grep -aobc "dominio-malicioso" imagen.img # → 0 (solo se materializa al decodificar)
```

## Recuperación en ext4 (Linux)

### Desde el journal

```bash
# Los bloques recientes pueden seguir en el journal
debugfs -R "logdump -a" imagen.img > journal.txt
less journal.txt
```

### Buscando inodos huérfanos

TSK los agrupa automáticamente bajo `$OrphanFiles`:

```bash
fls -r -p imagen.img | grep -i orphan
icat -o 0 imagen.img <inodo> > recuperado.bin
```

### Búsqueda de bloques no asignados con blkls

```bash
# Vuelca solo el contenido de bloques NO asignados (ideal para carving)
blkls imagen.img > unallocated.bin
strings -n 8 unallocated.bin | grep -i flag
binwalk unallocated.bin
```

## Slack space

Los ficheros rara vez llenan su último cluster: el **slack** puede contener restos de ficheros anteriores.

```bash
# Con TSK: la diferencia entre el tamaño lógico (istat) y el ocupado en disco
istat imagen.img <inodo>
# Si "Size: 1234" pero el bloque asignado son 4096 → hay 2862 bytes de slack
# Extrae el bloque completo y recorta:
icat imagen.img <inodo> > slack_full.bin
```

## Metodología de carving ordenada

1. `fls -r -p -d` → lista ficheros borrados conocidos.
2. `icat` cada uno → si el contenido es válido, ya está.
3. Si está fragmentado/vacío → `blkls` + búsqueda de firmas con Python.
4. Para ficheros embebidos → `binwalk -e`.
5. Para fotos/documentos genéricos → `foremost`/`photorec`.
6. Siempre validar lo extraído con `file` y hashes.

## Caso práctico resumido (recuperar un LNK borrado)

```
fls detecta desktop.lnk BORRADO (ino=0)
  ↓
Búsqueda por firma de LNK en la imagen cruda (Python + re)
  ↓
Offset identificado → extraer bloque de 4096 bytes
  ↓
dissect.shellitem parsea StringData
  ↓
command_line_arguments contiene cmd ofuscado %a85a:~N,1%
  ↓
Decodificar sustitución de caracteres → bitsadmin … http://DOMINIO-MALICIOSO/i.bat
  ↓
Dominio C2 identificado  →  md5sum → flag{<md5-del-IOC>}
```
