---
icon: person-to-portal
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

# Netcat Port-Pivot Relay

***

> Explicación básica

El **Netcat Port-Pivot Relay** es una técnica utilizada en **pentesting** o ataques de ciberseguridad para **redireccionar tráfico de una máquina a otra a través de Netcat**.

#### ¿Cómo funciona?

1. Un atacante compromete una máquina dentro de una red (pivot).
2. Usa **Netcat** para crear un túnel entre el atacante y otra máquina dentro de la red.
3. Redirige el tráfico de un puerto local en la máquina pivot hacia otro destino interno.

#### ¿Para qué se usa?

* Para **acceder a redes internas** sin conexión directa desde el atacante.
* Para **escalar privilegios** o moverse lateralmente en una red.
* Para **crear túneles** que permiten enviar comandos o extraer datos.

#### Ejemplo básico:

```shell
nc -l -p 8888 | nc <IP_OBJETIVO> 80
```

Todo lo que llegue al puerto `8888` en la máquina pivot se reenvía al puerto `80` del objetivo.

En resumen, **Netcat Port-Pivot Relay** permite a un atacante usar una máquina intermedia para acceder a objetivos dentro de una red restringida.

***

Tendremos que tener las `2` maquinas `WS01` y `WS02` corriendo, como anteriormente ya nos descargamos `netcat` en `WS02` lo utilizaremos para abrir un puerto de escucha en el `23` de forma local, no estara expuesto a la red de fuera, solo a nivel local.

Abriremos un `PowerShell` y ejecutaremos lo siguiente:

```powershell
cd .\Desktop\
cd .\ncat-portable-5.59BETA1\ncat-portable-5.59BETA1\
.\ncat.exe -lvp 23
```

Info:

```
Ncat: Version 5.59BETA1 ( http://nmap.org/ncat )
Ncat: Listening on 0.0.0.0:23
```

Ahora nos abriremos otra `PowerShell` y vamos a redirigir todo lo que pase en el puerto `40` que vamos a levantar ahora hacia el puerto `23` que esta a nivel local:

```powershell
.\ncat.exe -lvp 40 | .\ncat.exe 192.168.5.209 23
```

Info:

```
Ncat: Version 5.59BETA1 ( http://nmap.org/ncat )
Ncat: Listening on 0.0.0.0:40
```

Si nosotros tenemos esto que permite la conexion al puerto `40`, pero no al `23` nuestro `firewall`, lo que podremos hacer es atacar al puerto `40` ya que esta redirigiendo el trafico al puerto `23`.

Por lo que tendremos que hacer un `Netcat Port-Pivot Relay` a la maquina `Windows`.

Ahora abriremos otro `PowerShell` para realizar esto, pongamos que esto lo podemos hacer tambien a nivel externo, ya que el puerto `40` seria el que esta expuesto, se podria hacer con un `exploit` o lo que queramos, en este caso, lo haremos para que se entienda mejor esto en un `PowerShell`.

```powershell
.\ncat.exe 192.168.5.209 40
```

Info:

```
enviando exploit
exploit
```

Una vez enviado esos mensajes haremos `Ctrl+C` para cerrar la conexion, si nos vamos a donde esta la escucha del puerto `40`veremos lo siguiente:

```
Ncat: Version 5.59BETA1 ( http://nmap.org/ncat )
Ncat: Listening on 0.0.0.0:40
Ncat: Connection from 192.168.5.209:63482.
```

Vemos que realizo la conexion correctamente, pero no veremos los mensajes, ya que se estan redirigiendo al puerto `23`, por lo que si nos vamos al puerto `23` veremos lo siguiente:

```
Ncat: Version 5.59BETA1 ( http://nmap.org/ncat )
Ncat: Listening on 0.0.0.0:23
enviando exploit
exploit
```

Vemos que llego correctamente al puerto `23`.

En el caso de que fuera en un `linux` seria de la misma forma que en `windows` pero utilizando el comando `nc`.

```shell
nc -lvnp 23
```

En este caso para no tener que cerrar la conexion para que se envien esos datos, podemos crear un fichero `fifo` llamado `pivot` con el siguiente comando:

```shell
mknod pivot p
```

Ahora vamos a escuchar en otro puerto como hicimos anteriormente en el puerto `40` y lo redirigimos al fichero `fifo`, despues lo redirigimos a su vez al puerto `23`.

```shell
nc -lvnp 40 0<pivot | nc 127.0.0.1 23 1>pivot
```

Y ahora ya por ultimo en otra terminal nos conectamos al puerto `40` para pasarle la informacion que a su vez este puerto se la pasara al `23`.

```shell
nc 127.0.0.1 40
```

Si le enviamos lo siguiente:

```
hola
```

Y vamos al puerto `23` directamente a ver si llego dicho mensaje, veremos lo siguiente:

```
listening on [any] 23 ...
connect to [127.0.0.1] from (UNKNOWN) [127.0.0.1] 47166
hola
```

Vemos que ha funcionado correctamente.
