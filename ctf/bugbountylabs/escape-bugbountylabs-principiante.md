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

# Escape BugBountyLabs (Principiante)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip bugbountylabs_escape.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
python3 bugbountylabs_escape.py
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

Descargando la máquina escape, espere por favor...

[########################################] 100%
Descarga completa.
La IP de la máquina escape es -> 172.17.0.2

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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-16 14:22 CET
Nmap scan report for ssti.dl (172.17.0.2)
Host is up (0.000039s latency).

PORT     STATE SERVICE VERSION
5000/tcp open  upnp?
| fingerprint-strings:
|   GetRequest:
|     HTTP/1.1 200 OK
|     Server: Werkzeug/3.1.3 Python/3.10.16
|     Date: Sun, 16 Mar 2025 13:22:16 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 1158
|     Connection: close
|     <!DOCTYPE html>
|     <html lang="en">
|     <head>
|     <meta charset="UTF-8">
|     <meta name="viewport" content="width=device-width, initial-scale=1.0">
|     <title>Laboratorio Reflected XSS</title>
|     <link rel="stylesheet" href="/static/styles.css">
|     </head>
|     <body>
|     <header class="navbar">
|     <div class="container">
|     <h1>Laboratorio Reflected XSS</h1>
|     </div>
|     </header>
|     <main class="container">
|     <section id="lab" class="lab-section">
|     <h2>Prueba tu payload</h2>
|     <p>Introduce un payload y observa c
|     refleja en la p
|     gina. Para explotar, deber
|     escapar del atributo HTML.</p>
|     <form method="POST" class="pentest-form">
|     <label for="in
|   RTSPRequest:
|     <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
|     "http://www.w3.org/TR/html4/strict.dtd">
|     <html>
|     <head>
|     <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
|     <title>Error response</title>
|     </head>
|     <body>
|     <h1>Error response</h1>
|     <p>Error code: 400</p>
|     <p>Message: Bad request version ('RTSP/1.0').</p>
|     <p>Error code explanation: HTTPStatus.BAD_REQUEST - Bad request syntax or unsupported method.</p>
|     </body>
|_    </html>
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port5000-TCP:V=7.94SVN%I=7%D=3/16%Time=67D6D088%P=x86_64-pc-linux-gnu%r
SF:(GetRequest,536,"HTTP/1\.1\x20200\x20OK\r\nServer:\x20Werkzeug/3\.1\.3\
SF:x20Python/3\.10\.16\r\nDate:\x20Sun,\x2016\x20Mar\x202025\x2013:22:16\x
SF:20GMT\r\nContent-Type:\x20text/html;\x20charset=utf-8\r\nContent-Length
SF::\x201158\r\nConnection:\x20close\r\n\r\n<!DOCTYPE\x20html>\n<html\x20l
SF:ang=\"en\">\n<head>\n\x20\x20\x20\x20<meta\x20charset=\"UTF-8\">\n\x20\
SF:x20\x20\x20<meta\x20name=\"viewport\"\x20content=\"width=device-width,\
SF:x20initial-scale=1\.0\">\n\x20\x20\x20\x20<title>Laboratorio\x20Reflect
SF:ed\x20XSS</title>\n\x20\x20\x20\x20<link\x20rel=\"stylesheet\"\x20href=
SF:\"/static/styles\.css\">\n</head>\n<body>\n\x20\x20\x20\x20<header\x20c
SF:lass=\"navbar\">\n\x20\x20\x20\x20\x20\x20\x20\x20<div\x20class=\"conta
SF:iner\">\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20<h1>Laboratori
SF:o\x20Reflected\x20XSS</h1>\n\x20\x20\x20\x20\x20\x20\x20\x20</div>\n\x2
SF:0\x20\x20\x20</header>\n\x20\x20\x20\x20<main\x20class=\"container\">\n
SF:\x20\x20\x20\x20\x20\x20\x20\x20<section\x20id=\"lab\"\x20class=\"lab-s
SF:ection\">\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20<h2>Prueba\x
SF:20tu\x20payload</h2>\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20<
SF:p>Introduce\x20un\x20payload\x20y\x20observa\x20c\xc3\xb3mo\x20se\x20re
SF:fleja\x20en\x20la\x20p\xc3\xa1gina\.\x20Para\x20explotar,\x20deber\xc3\
SF:xa1s\x20escapar\x20del\x20atributo\x20HTML\.</p>\n\x20\x20\x20\x20\x20\
SF:x20\x20\x20\x20\x20\x20\x20<form\x20method=\"POST\"\x20class=\"pentest-
SF:form\">\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x
SF:20<label\x20for=\"in")%r(RTSPRequest,1F4,"<!DOCTYPE\x20HTML\x20PUBLIC\x
SF:20\"-//W3C//DTD\x20HTML\x204\.01//EN\"\n\x20\x20\x20\x20\x20\x20\x20\x2
SF:0\"http://www\.w3\.org/TR/html4/strict\.dtd\">\n<html>\n\x20\x20\x20\x2
SF:0<head>\n\x20\x20\x20\x20\x20\x20\x20\x20<meta\x20http-equiv=\"Content-
SF:Type\"\x20content=\"text/html;charset=utf-8\">\n\x20\x20\x20\x20\x20\x2
SF:0\x20\x20<title>Error\x20response</title>\n\x20\x20\x20\x20</head>\n\x2
SF:0\x20\x20\x20<body>\n\x20\x20\x20\x20\x20\x20\x20\x20<h1>Error\x20respo
SF:nse</h1>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Error\x20code:\x20400</p>\
SF:n\x20\x20\x20\x20\x20\x20\x20\x20<p>Message:\x20Bad\x20request\x20versi
SF:on\x20\('RTSP/1\.0'\)\.</p>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Error\x
SF:20code\x20explanation:\x20HTTPStatus\.BAD_REQUEST\x20-\x20Bad\x20reques
SF:t\x20syntax\x20or\x20unsupported\x20method\.</p>\n\x20\x20\x20\x20</bod
SF:y>\n</html>\n");
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 92.77 seconds
```

Vemos que hay un puerto `5000` si entramos a dicho puerto veremos una pagina web que se centra en la vulnerabilidad de un `XSS`, el objetivo es realizar una inyeccion de `XSS` pero escapando del atributo `HTML`, que se podra hacer realizando lo siguiente:

URL = [Info Payloads XSS](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XSS%20Injection)

```html
"><img src=x onerror=alert('XSS');>
```

<figure><img src="../../.gitbook/assets/image (296).png" alt=""><figcaption></figcaption></figure>

Con `">` ya estamos escapando el `HTML` y estamos añadiendo una nueva seccion a nivel de codigo, si inspeccionamos el codigo veremos esto:

<figure><img src="../../.gitbook/assets/image (297).png" alt=""><figcaption></figcaption></figure>

Vemos que efectivamente se nos añadio el bloque del `img` por lo que ha funcionado y habremos resuelto el laboratorio de forma correcta.
