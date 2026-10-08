---
icon: floppy-disks
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

# Forense de disco/USB con TSK y pytsk3

> Cuando la evidencia es una **imagen de disco** (HDD, SSD, USB, tarjeta SD), la herramienta estándar es **The Sleuth Kit (TSK)** y su binding Python **pytsk3**. Ambos leen el filesystem **sin montar** la imagen (no necesitas root, no modificas nada).

## Instalación

```bash
# CLI de TSK (fls, icat, mmls, fsstat, istat, ...)
sudo pacman -S sleuthkit          # Arch/BlackArch
sudo apt install sleuthkit        # Debian/Ubuntu/Kali

# Binding Python
python3 -m venv .venv && source .venv/bin/activate
pip install pytsk3
```

## Paso 1 · Reconocimiento del formato

```bash
file usb_mnt20202703.img
# DOS/MBR boot sector; partition 1 : ID=0x7, active, start-CHS (0x0,1,2),
#   end-CHS (0x3e,177,51), startsector 64, 1007168 sectors
```

Interpretación típica:

* **DOS/MBR** vs **GPT**: `mmls` lo confirma.
* **ID de partición**: `0x7` = NTFS/HPFS, `0x83` = Linux, `0xC` = FAT32 LBA, `0xEF` = EFI System.
* **startsector** = offset en **sectores de 512 bytes** donde empieza la partición. En el ejemplo: `64 × 512 = 32768 bytes`.

```bash
# Estructura de particiones
mmls usb_mnt20202703.img

# Leer la tabla de partición MBR a mano (entrada en offset 446, 16 bytes)
xxd -s 446 -l 16 usb_mnt20202703.img
#   byte 1:  0x80 (arrancable)
#   byte 4:  0x07 (tipo NTFS)
#   bytes 8-11 (LE): sector de inicio LBA
#   bytes 12-15 (LE): tamaño en sectores

# Tipo de filesystem dentro de una partición
fsstat -o 64 usb_mnt20202703.img   # Muestra ext4, NTFS, FAT, ...
```

## Paso 2 · Listar el árbol de ficheros

```bash
# -r recursivo, -p rutas completas
fls -r -p -o 64 usb_mnt20202703.img
```

Salida típica:

```
d/d 36:    /System Volume Information
+ d/d 39:  /System Volume Information/ClientRecoveryPasswordRotation
r/r 41:    /9788483432914_L33_24.pdf
r/r 43:    /backup.zip
-/r * 48:  /desktop.lnk     ← asterisco = BORRADO
```

**Convención de `fls`:**

* `r/r` = nombre regular / metadata regular; `d/d` = directorio.
* `*` = entrada **desasignada** (borrada) — la metadata puede seguir ahí.
* El número de la izquierda es el **inodo (inode / MFT entry)** → lo necesitas para extraer.

## Paso 3 · Ver metadatos de un inodo

```bash
# Timestamps, tamaño, atributos ADS (Alternate Data Streams en NTFS)
istat -o 64 usb_mnt20202703.img 42
```

Devuelve: fechas (acceso/modificación/cambio/creación — MACB), tamaño, lista de clusters ADS (`$DATA`), `Zone.Identifier` si fue descargado de internet, etc.

**Timestamps NTFS/MFT que verás:**

* `Standard Information` (SI) — lo que ve el usuario.
* `File Name` (FN) — cuando se renombró o movió por última vez.
* **Timestomping**: si SI ≪ FN, el atacante falseó las fechas.

## Paso 4 · Extraer ficheros por inodo

```bash
# Extraer el fichero del inodo 42
icat -o 64 usb_mnt20202703.img 42 > autorun.inf

# Extraer un ADS concreto de NTFS (Zone.Identifier)
icat -o 64 usb_mnt20202703.img 42-128 > zone_identifier.txt
```

## pytsk3 — lo mismo pero desde Python

Ventajas: puedes iterar, filtrar, calcular hashes, decodificar en el mismo script y **no necesitas root** para leer.

```python
import pytsk3

IMAGE_PATH = "usb_mnt20202703.img"
OFFSET_BYTES = 64 * 512   # 32768

img = pytsk3.Img_Info(IMAGE_PATH)
fs = pytsk3.FS_Info(img, offset=OFFSET_BYTES)

def walk(fs, path="/", indent=0):
    """Recorre recursivamente el FS y lista entradas."""
    dir_ = fs.open_dir(path=path)
    for entry in dir_:
        if entry.info.name.name in (b'.', b'..'):
            continue
        name = entry.info.name.name.decode(errors='replace')
        meta = entry.info.meta
        if meta is None:
            print(f"{' '*indent}?  ino=0   /{name}  (borrado, sin metadata)")
            continue
        tipo = 'F' if meta.type == pytsk3.TSK_FS_META_TYPE_REG else 'D'
        borrado = entry.info.name.flags == pytsk3.TSK_FS_NAME_FLAG_UNALLOC
        nota = " (BORRADO)" if borrado else ""
        print(f"{' '*indent}{tipo}  ino={meta.addr:<6} size={meta.size:<10} /{name}{nota}")
        if meta.type == pytsk3.TSK_FS_META_TYPE_DIR and not borrado:
            sub = f"{path}/{name}" if path != "/" else f"/{name}"
            walk(fs, sub, indent+4)

walk(fs, "/")
```

> ⚠️ **API de pytsk3 que conviene memorizar** (probado): `fs.open_meta(inode=N)` (¡con el argumento llamado `inode`!) y para leer: `f.info.meta.size` (el tamaño está en `f.info.meta`, **no** en `f.info`).

### Extraer un fichero por inodo en pytsk3

```python
f = fs.open_meta(inode=42)
data = f.read_random(0, f.info.meta.size)
with open("autorun.inf", "wb") as out:
    out.write(data)
```

### Recorrer sin recursión manual: `fs.open_dir(path="/")`

Cada `entry.info` tiene:

* `name.name` (bytes) → nombre
* `name.flags` → `TSK_FS_NAME_FLAG_ALLOC` (1) o `UNALLOC` (2, borrado)
* `meta.type` → `TSK_FS_META_TYPE_REG` (fichero), `_DIR` (dir), etc.
* `meta.addr` → inodo
* `meta.size`, `meta.mtime`, `meta.ctime`, `meta.atime`, `meta.crtime`

## Sistemas de archivos Linux

### ext2/ext3/ext4 con debugfs (sin instalar nada)

```bash
# Listar el contenido de la imagen ext4
debugfs -R "ls -l /" imagen.img

# Extraer un fichero
debugfs -R "dump /flag.txt /tmp/flag.txt" imagen.img

# Ver el inodo completo
debugfs -R "stat <15>" imagen.img
```

> `debugfs` es muy útil porque **no necesita root** y permite escribir en la imagen para crear "cáscara" (útil para construir fixtures de test).

### Ext4 journal (el "logfile" de ext4)

```bash
# El journal puede contener operaciones recientes aún no commiteadas
debugfs -R "logdump -a" imagen.img | less
```

### XFS, Btrfs

TSK tiene soporte parcial; para Btrfs suele ser mejor `btrfs restore` (requiere root o loop-mount):

```bash
sudo mount -o loop,ro imagen.img /mnt
# o sin montar:
sudo btrfs restore -i imagen.img /mnt/recuperado
```

## Montar vs no montar

| Montar (`mount -o loop`)                          | TSK / pytsk3 / debugfs          |
| ------------------------------------------------- | ------------------------------- |
| Requiere root                                     | No requiere root                |
| Puede modificar la imagen (journal replay, atime) | Lectura pura, no modifica nada  |
| Cómodo para explorar                              | Más trabajo manual              |
| No funciona en filesystems corruptos              | Permite leer incluso FS dañados |

**Regla forense: SIEMPRE no-montar.** Si necesitas montar, hazlo `ro` sobre una **copia**.

## Trucos rápidos

```bash
# Ver todos los ficheros borrados
fls -r -p -d imagen.img

# Solo ficheros regulares (no directorios)
fls -r -p -F imagen.img

# Búsqueda de cadena en la imagen cruda (sin parser)
grep -aob "flag{" imagen.img

# ¿Qué ADS tiene este fichero NTFS?
istat -o 64 imagen.img 42 | grep -A3 "Attributes"
```

## Resumen de la cadena de comandos

```
file → mmls → fsstat → fls -r → istat → icat
                (o pytsk3 para todo junto)
```
