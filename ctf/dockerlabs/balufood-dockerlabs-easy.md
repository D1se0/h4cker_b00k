---
icon: flag
---

# Balufood DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip balufood.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh balufood.tar
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
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-05 11:51 EDT
Nmap scan report for 172.17.0.2
Host is up (0.000079s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.2p1 Debian 2+deb12u5 (protocol 2.0)
| ssh-hostkey: 
|   256 69:15:7d:34:74:1c:21:8a:cb:2c:a2:8c:42:a4:21:7f (ECDSA)
|_  256 a7:3a:c9:b2:ac:cf:44:77:a7:9c:ab:89:98:c7:88:3f (ED25519)
5000/tcp open  http    Werkzeug httpd 2.2.2 (Python 3.11.2)
|_http-server-header: Werkzeug/2.2.2 Python/3.11.2
|_http-title: Restaurante Balulero - Inicio
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.83 seconds
```

Veremos que hay un puerto `5000` abierto, en el que se aloja una pagina web, si entramos dentro veremos una pagina web de un restaurante normal, pero si nos vamos a `Ver carta` -> `Admin` veremos un `login`, por lo que vamos a probar las credenciales por defecto tipicas:

```
User: admin
Pass: admin
```

Veremos que si nos autenticamos, pero no veremos gran cosa por fuera, si probamos a inspeccionar el codigo veremos lo siguiente:

```html
<!-- Backup de acceso: sysadmin:backup123 -->
```

Podemos ver que pueden ser unas credenciales para el puerto `SSH` por lo que vamos a probar ha realizar lo siguiente:

```shell
ssh sysadmin@<IP>
```

Metemos como contraseña `backup123` y veremos que estamos dentro.

## Escalate user balulero

Si listamos la carpeta en la que nos encontramos de la `home` de dicho usuario y leemos el archivo `app.py` para inspeccionar el codigo veremos lo siguiente al principio:

```python
from flask import Flask, render_template, redirect, url_for, request, session, flash
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = 'cuidaditocuidadin'
DATABASE = 'restaurant.db'
...........................<RESTO DE CODIGO>......................................
```

Veremos que hay una clave secreta la cual puede ser la contraseña de uno de los usuarios del sistema:

```shell
cat /etc/passwd | grep "/bin/bash"
```

Info:

```
root:x:0:0:root:/root:/bin/bash
sysadmin:x:1000:1000:sysadmin,sysadmin,,:/home/sysadmin:/bin/bash
balulero:x:1001:1001:balulero,,,:/home/balulero:/bin/bash
```

Vamos a probar con `balulero` de la siguiente forma:

```shell
su balulero
```

Metemos como contraseña `cuidaditocuidadin` y veremos que estaremos dentro.

## Escalate Privileges

Si leemos de la `home` de dicho usuario el archivo `.bashrc` y veremos lo siguiente:

```shell
cat ~/.bashrc
```

Info:

```
...........................<RESTO DE CODIGO>.....................................

alias ser-root='echo chocolate2 | su - root'
```

Veremos que esta pasando como contraseña `chocolate2` para loguearse con `root` por lo que vamos a probar dicha contraseña a ver si funciona.

```shell
su root
```

Metemos como contraseña `chocolate2`.

```
root@a064182c909b:~# whoami
root
```

Veremos que seremos el usuario `root`, por lo que habremos terminado la maquina.
