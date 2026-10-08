---
icon: memory
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

# Forense de RAM con Volatility 3

> **Volatility 3** es el framework de referencia para analizar volcados de memoria (RAM). Sustituye a Volatility 2 (archivado en 2025) y funciona tanto con dumps de **Linux** como de **Windows**.

## Instalación

```bash
# Recomendado: en un venv aislado
python3 -m venv .venv && source .venv/bin/activate
pip install volatility3

# Comprobación
python3 -m volatility3 --help
vol=$(python3 -m volatility3 --help >/dev/null 2>&1 && echo "python3 -m volatility3")
# A partir de aquí, en la doc usamos "vol" como alias:
#   alias vol="python3 -m volatility3"
```

## Volcado de RAM en Linux

> Volatility **no** captura memoria; solo la analiza. Para capturar en Linux:

| Herramienta               | Cómo funciona                                                                       | Cuándo usar                                                            |
| ------------------------- | ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **LiME**                  | LKM (Loadable Kernel Module) — requiere compilar para el kernel exacto del objetivo | Máxima fidelidad, formato RAW o LiME                                   |
| **AVML**                  | Binario estático de Microsoft, sin dependencias                                     | Lo más rápido y cómodo; recomendado por la doc oficial de Volatility 3 |
| **/dev/mem, /proc/kcore** | Solo con `CONFIG_STRICT_DEVMEM=n`; obsoleto en kernels modernos                     | Nunca en producción                                                    |
| **LibPBA**                | Binario user-space (`libhma_linux_ram_x64.so`) con módulo temporal                  | Sistemas sin cabeceras de kernel para compilar                         |

```bash
# Con AVML (recomendado por la doc oficial):
sudo ./avml output.lime

# Con LiME:
git clone https://github.com/504ensicsLabs/LiME && cd LiME/src
make
sudo insmod lime-$(uname -r).ko "path=/tmp/ram.lime format=lime"
sudo rmmod lime
```

**Importante:** en un CTF el dump ya te lo dan. Solo necesitas saber reconocer el formato: `.lime` empieza con el magic `4C 69 4D 45` (LiME), `.raw` suele ser una copia de `/dev/mem` o `dd` de la memoria.

## Símbolos (ISF) — el 90 % de los errores con Volatility 3

Volatility 3 necesita **Intermediate Symbol Files** (JSON con la estructura del kernel/binary) para entender el dump. Sin símbolos, la mayoría de plugins fallan con `Unable to validate layers` o `Unsatisfied requirement plugins`.

### Windows

Volatility 3 descarga automáticamente los símbolos (PDB → ISF) si tiene acceso a internet. Si estás offline, usa `vol.py isfinfo` para ver qué tienes.

### Linux

Los kernels no traen un PDB universal. Tienes dos opciones:

**Opción A — Repo de símbolos pre-generados** (probado primero):

```bash
# Repo comunitario organizado por versión de kernel
git clone https://github.com/Abyss-W4tcher/volatility3-symbols
# Copia el JSON.xz correspondiente a tu kernel a:
#   $(python3 -c 'import volatility3,os;print(os.path.dirname(volatility3.__file__))')/symbols/
```

También el repositorio oficial `volatility3-symbols` tiene packs por distro (Ubuntu, Debian, AlmaLinux…).

**Opción B — Generarlos tú mismo** (necesitas el kernel exacto):

```bash
# 1. Instala dwarf2json (Go)
go install github.com/volatilityfoundation/dwarf2json@latest

# 2. Consigue vmlinux con símbolos DWARF:
#    Debian/Ubuntu:
apt-get download linux-image-$(uname -r)-dbgsym
#    o compila el kernel con CONFIG_DEBUG_INFO=y

# 3. Convierte DWARF → ISF
dwarf2json linux --elf /usr/lib/debug/boot/vmlinux-$(uname -r) \
                 --system-map /boot/System.map-$(uname -r) \
                 | xz > ubuntu-$(uname -r).json.xz

# 4. Muévelo a symbols/
mv ubuntu-*.json.xz $(python3 -c 'import volatility3,os;print(os.path.dirname(volatility3.__file__))')/symbols/
```

## Primer comando SIEMPRE: banners

Identifica el kernel/distribución del dump y te dice qué ISF necesitas:

```bash
vol -f memory.vmem banners
```

```
Offset Banner
0x141c1390 Linux version 4.15.0-42-generic (buildd@lgw01-amd64-023) ...
0x63a00160 Linux version 4.15.0-72-generic ...
```

Si el kernel no está en tu repo de símbolos → genera el ISF con el paso anterior.

## Plugins Linux esenciales (en orden de análisis)

### 1. Información básica

```bash
vol -f mem.vmem linux.boottime      # Hora de arranque → línea temporal
vol -f mem.vmem banners             # Versión de kernel / distro
```

### 2. Procesos

```bash
vol -f mem.vmem linux.pslist        # Lista lineal de procesos con PID, PPID, UID
vol -f mem.vmem linux.pstree        # Árbol padre/hijo — detecta orfandad e inyección
vol -f mem.vmem linux.psaux         # Processes + command line completa (¡MUY útil!)
vol -f mem.vmem linux.psscan        # Procesos terminados en memoria (no solo activos)
```

**Qué buscar en `pstree` / `psaux`:**

* Procesos huérfanos (PPID inexistente) o con `PPID=1` sospechoso.
* Comandos raros: `bash -c` anidados, `nc`, `socat`, `python -c` con base64, `curl | sh`.
* Binarios fuera de ruta estándar (`/tmp/`, `/dev/shm/`, `/home/user/`).
* Combinaciones de LOLBins: `rundll32`, `regsvr32` (Windows), `openssl s_client`, `bash -i >& /dev/tcp/...`.

### 3. Historiales y actividad de usuario

```bash
vol -f mem.vmem linux.bash          # Historial de bash RECUPERADO DE MEMORIA
vol -f mem.vmem linux.check_syscall # Tabla de syscalls hookeda (rootkits)
vol -f mem.vmem linux.tty_check     # TTYs y sesiones interactivas
```

### 4. Red

```bash
vol -f mem.vmem linux.sock          # Sockets abiertos con inodo
vol -f mem.vmem linux.lsof          # Ficheros abiertos por cada proceso
vol -f mem.vmem linux.ip.Addr       # IPs por interfaz
vol -f mem.vmem linux.ip.Link       # Enlaces y estado de red
```

### 5. Malware / inyección

```bash
vol -f mem.vmem linux.malfind       # Regiones RWX anónimas (código inyectado)
vol -f mem.vmem linux.elfs          # ELF cargados en memoria
vol -f mem.vmem linux.vmayarascan --yara-file reglas.yar   # YARA sobre memoria de proceso
vol -f mem.vmem linux.lsmod         # Módulos del kernel cargados
vol -f mem.vmem linux.check_creds   # Estructuras de credenciales sospechosas
```

**Qué devuelve `linux.malfind`:** regiones con protección **RWX** sin fichero de respaldo (`Anonymous Mapping`). Es la firma de shellcode, packers o payload desempaquetado en runtime. Si el PID es de un servicio del sistema (networkd, systemd, sshd), es casi seguro compromiso.

## Plugins Windows esenciales

```bash
vol -f mem.vmem windows.info          # Info general, versión, uptime
vol -f mem.vmem windows.pslist        # Procesos activos
vol -f mem.vmem windows.pstree        # Árbol de procesos
vol -f mem.vmem windows.cmdline       # CommandLine por proceso
vol -f mem.vmem windows.netscan       # Conexiones de red (históricas y activas)
vol -f mem.vmem windows.malfind       # Regiones RWX con shellcode
vol -f mem.vmem windows.dlllist --pid <PID>    # DLLs cargadas por un PID
vol -f mem.vmem windows.handles --pid <PID>    # Handles abiertos (ficheros, mutex, pipes)
vol -f mem.vmem windows.registry.printkey --key "Software\Microsoft\Windows\CurrentVersion\Run"
vol -f mem.vmem windows.filescan | grep -i "suspicious"   # Escaneo de ficheros en memoria
vol -f mem.vmem windows.dumpfiles --pid <PID>  # Extraer ficheros/dlls de un proceso
```

## Volcado de un proceso específico

```bash
# En Volatility 3 ya se puede hacer directamente con --dump
vol -f mem.vmem linux.pslist --pid 1733 --dump
vol -f mem.vmem windows.pslist --pid 4242 --dump

# Para regiones concretas de memoria de un proceso:
vol -f mem.vmem linux.malfind --pid 540 --dump
```

## Workflows de retos típicos

### Reto tipo "¿qué hizo el usuario?"

```bash
vol -f mem.vmem linux.bash
vol -f mem.vmem linux.psaux
```

### Reto tipo "encuentra el PID malicioso"

```bash
vol -f mem.vmem linux.pstree       # Buscar padres raros
vol -f mem.vmem linux.psaux        # Buscar command line sospechosa
vol -f mem.vmem linux.malfind      # Buscar regiones RWX anónimas
vol -f mem.vmem linux.vmayarascan --yara-file ~/yara/malware.yar
```

### Reto tipo "¿a qué dominio se conectó?"

```bash
vol -f mem.vmem linux.sock
vol -f mem.vmem linux.lsof | grep -E "(socket|TCP|UDP)"
vol -f mem.vmem windows.netscan    # En dumps Windows
```

## Errores comunes y cómo arreglarlos

| Error                                      | Causa                                    | Solución                                      |
| ------------------------------------------ | ---------------------------------------- | --------------------------------------------- |
| `Unsatisfied requirement plugins`          | No hay símbolos ISF                      | Genera/instala el JSON.xz correcto            |
| `Layer ... invalid`                        | El dump no es de memoria o está corrupto | Verifica con `file` y `banners`               |
| `linux.pslist` devuelve vacío              | Kernel moderno no soportado aún          | Actualiza Volatility 3; prueba `linux.psscan` |
| Proceso existe pero no sale en `pslist`    | Proceso terminado                        | Usa `psscan` / `psxview`                      |
| `malfind` devuelve muchos falsos positivos | JIT de navegadores es RWX normal         | Filtra por procesos del sistema               |

## Volatility 2 vs Volatility 3 (cheat rápido)

| Volatility 2 (obsoleto)                      | Volatility 3                        |
| -------------------------------------------- | ----------------------------------- |
| `vol.py -f dump --profile=Win7SP1x64 pslist` | `vol -f dump windows.pslist`        |
| Necesitas perfil exacto                      | Detecta símbolos automáticamente    |
| `linux_bash`                                 | `linux.bash`                        |
| `malfind`                                    | `windows.malfind` / `linux.malfind` |
| No soporta kernels nuevos de Linux           | Sí (generando ISF con dwarf2json)   |

**En resumen:** usa siempre Volatility 3, con Volatility 2 solo para CTFs antiguos que requieran perfiles raros.
