---
icon: flag
---

# DogShow BugBountyLabs (Avanzado)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip bugbountylabs_dogshow.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
python3 bugbountylabs_dogshow.py
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

Descargando la máquina dogshow, espere por favor...

[########################################] 100%
Descarga completa.
La IP de la máquina dogshow es -> 172.17.0.2

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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-17 12:35 CET
Nmap scan report for openredirect.dl (172.17.0.2)
Host is up (0.000033s latency).

PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.62 ((Debian))
|_http-title: P\xC3\xA1gina Vulnerable a XSS
|_http-server-header: Apache/2.4.62 (Debian)
5000/tcp open  upnp?
| fingerprint-strings:
|   GetRequest:
|     HTTP/1.1 200 OK
|     Server: Werkzeug/3.1.3 Python/3.11.2
|     Date: Mon, 17 Mar 2025 11:35:59 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 935
|     Connection: close
|     <!DOCTYPE html>
|     <html lang="en">
|     <head>
|     <meta charset="UTF-8">
|     <meta name="viewport" content="width=device-width, initial-scale=1.0">
|     <title>Dog Competition</title>
|     <link rel="stylesheet" href="/static/styles.css">
|     </head>
|     <body>
|     <header>
|     <h1>Welcome to the Dog Competition</h1>
|     <nav>
|     href="/register" class="button register">Register</a>
|     href="/login" class="button login">Login</a>
|     </nav>
|     </header>
|     <main>
|     <div class="image-container">
|     <img src="/static/images/balulero.png" alt="Balulero the dog">
|     </div>
|     <p>Join our competition and showcase your dog!</p>
|     </main>
|     <footer>
|     <p>&copy; 2
|   RTSPRequest:
|     <!DOCTYPE HTML>
|     <html lang="en">
|     <head>
|     <meta charset="utf-8">
|     <title>Error response</title>
|     </head>
|     <body>
|     <h1>Error response</h1>
|     <p>Error code: 400</p>
|     <p>Message: Bad request version ('RTSP/1.0').</p>
|     <p>Error code explanation: 400 - Bad request syntax or unsupported method.</p>
|     </body>
|_    </html>
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port5000-TCP:V=7.94SVN%I=7%D=3/17%Time=67D8091F%P=x86_64-pc-linux-gnu%r
SF:(GetRequest,455,"HTTP/1\.1\x20200\x20OK\r\nServer:\x20Werkzeug/3\.1\.3\
SF:x20Python/3\.11\.2\r\nDate:\x20Mon,\x2017\x20Mar\x202025\x2011:35:59\x2
SF:0GMT\r\nContent-Type:\x20text/html;\x20charset=utf-8\r\nContent-Length:
SF:\x20935\r\nConnection:\x20close\r\n\r\n<!DOCTYPE\x20html>\n<html\x20lan
SF:g=\"en\">\n<head>\n\x20\x20\x20\x20<meta\x20charset=\"UTF-8\">\n\x20\x2
SF:0\x20\x20<meta\x20name=\"viewport\"\x20content=\"width=device-width,\x2
SF:0initial-scale=1\.0\">\n\x20\x20\x20\x20<title>Dog\x20Competition</titl
SF:e>\n\x20\x20\x20\x20<link\x20rel=\"stylesheet\"\x20href=\"/static/style
SF:s\.css\">\n</head>\n<body>\n\x20\x20\x20\x20<header>\n\x20\x20\x20\x20\
SF:x20\x20\x20\x20<h1>Welcome\x20to\x20the\x20Dog\x20Competition</h1>\n\x2
SF:0\x20\x20\x20\x20\x20\x20\x20<nav>\n\x20\x20\x20\x20\x20\x20\x20\x20\x2
SF:0\x20\x20\x20<a\x20href=\"/register\"\x20class=\"button\x20register\">R
SF:egister</a>\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20<a\x20href
SF:=\"/login\"\x20class=\"button\x20login\">Login</a>\n\x20\x20\x20\x20\x2
SF:0\x20\x20\x20</nav>\n\x20\x20\x20\x20</header>\n\x20\x20\x20\x20\n\x20\
SF:x20\x20\x20<main>\n\x20\x20\x20\x20\x20\x20\x20\x20<div\x20class=\"imag
SF:e-container\">\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20<img\x2
SF:0src=\"/static/images/balulero\.png\"\x20alt=\"Balulero\x20the\x20dog\"
SF:>\n\x20\x20\x20\x20\x20\x20\x20\x20</div>\n\x20\x20\x20\x20\x20\x20\x20
SF:\x20<p>Join\x20our\x20competition\x20and\x20showcase\x20your\x20dog!</p
SF:>\n\x20\x20\x20\x20</main>\n\x20\x20\x20\x20<footer>\n\x20\x20\x20\x20\
SF:x20\x20\x20\x20<p>&copy;\x202")%r(RTSPRequest,16C,"<!DOCTYPE\x20HTML>\n
SF:<html\x20lang=\"en\">\n\x20\x20\x20\x20<head>\n\x20\x20\x20\x20\x20\x20
SF:\x20\x20<meta\x20charset=\"utf-8\">\n\x20\x20\x20\x20\x20\x20\x20\x20<t
SF:itle>Error\x20response</title>\n\x20\x20\x20\x20</head>\n\x20\x20\x20\x
SF:20<body>\n\x20\x20\x20\x20\x20\x20\x20\x20<h1>Error\x20response</h1>\n\
SF:x20\x20\x20\x20\x20\x20\x20\x20<p>Error\x20code:\x20400</p>\n\x20\x20\x
SF:20\x20\x20\x20\x20\x20<p>Message:\x20Bad\x20request\x20version\x20\('RT
SF:SP/1\.0'\)\.</p>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Error\x20code\x20e
SF:xplanation:\x20400\x20-\x20Bad\x20request\x20syntax\x20or\x20unsupporte
SF:d\x20method\.</p>\n\x20\x20\x20\x20</body>\n</html>\n");
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 92.88 seconds
```

Vemos que tenemos `2` puertos, si vamos al del `80` veremos una pagina web, como sabemos que esta enfocado al `XSS` vamos a probar a meter un `payload` en el campo de `Comentario` y le daremos a `enviar`:

```html
"><script>alert('XSS')</script>
```

Echo esto veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (301).png" alt=""><figcaption></figcaption></figure>

Esta parte ya estaria echa, pero nos queda el del puerto `5000`, si entramos en el veremos una pagina web para poder registrarnos y poder logueranos, vamos a crear un usuario primero.

Le daremos a `register` y en mi caso pondre lo siguiente:

```
User: test
Email: test@test.com
Pass: test123
```

Una vez registrados, nos llevara al `login` de forma automatica, nos logueamos con dichas credenciales y veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (302).png" alt=""><figcaption></figcaption></figure>

Vemos que hay varios campos, por lo que vamos a probar a inyectar un `payload` de `XSS` en el campo de `Dog's Name`:

```html
"><script>alert('XSS')</script>
```

Una vez añadido todo esto y dandole a `Add Dog` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (303).png" alt=""><figcaption></figcaption></figure>

Vemos que ha funcionado, por lo que habremos realizado en los `2` puertos las vulnerabilidades correctar y habremos terminado la maquina.
