---
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

# Alternativas a Nmap - Naabu y Netcat

Alguna alternativa a esta herramienta podria ser principalmente la llamada `naabu` que lo encontraremos en el siguiente link:

URL = [Naabu GitHub](https://github.com/projectdiscovery/naabu)

Si estamos en `kali` solamente tendremos que poner el siguiente comando:

```shell
sudo apt install naabu
```

Y una vez instala podremos hacer un reconocimiento como `nmap` con un `Host-Discovery` de la siguiente forma:

```shell
naabu 192.168.20.0/24
```

Y esto nos mostrara los `hosts` mas los puertos a los que van asociados cada uno de ellos, pero con esto seremos detectado en herramientas como `Snort`.

Si nosotros queremos realizar un escaneo de `servicios/puertos` de forma manual sin automatizar nada con `nmap` u otra herramienta, podremos hacerlo con `netcat`.

```shell
netcat -nv 192.168.20.130 80
```

Con `-nv` especificamos que no nos haga `DNS` reverso y que nos muestre el `verbose` de las operaciones que se este haciendo por detras.

Con el numero `80` lo que estamos especificando es el puerto al que nos estamos intentando conectar de dicha IP.

Con esto lo que estamos intentando hacer es que nos muestre con el `verbose` si ese `host` esta activo o no, comprobando la conexion, como sabemos que la IP del `130` no esta activa nos dara el siguiente error sin ser detectados por herramientas `IDS`:

```
(UNKNOWN) [192.168.20.130] 80 (http) : No route to host
```

Por lo que nos comenta no hay nada ahi, por lo que no esta acrtivo, pero si nos vamos a una que si este activa, nos aparecera lo siguiente:

```shell
netcat -nv 192.168.20.128 80
```

Info:

```
(UNKNOWN) [192.168.20.128] 80 (http) open
```

Vemos que nos pone `Open` por lo que ya sabremos que dicha `IP` esta activa, y todo esto sin ser detectados de forma manual todo.

Ahora si queremos realizar un escaneo de puertos en esa IP de forma manual, lo haremos de la siguiente forma añadiendole un `TimeOut` de espera para que no sea tan de seguido.

```shell
netcat -nvw2 192.168.20.128 1-100
```

Con el `-w2` especificamos que haga una espera de `2` segundos por cada conexion. Con los numeros `1-100` estamos especificando los puertos que queremos que nos testee en este caso en un rango del `1` al `100`.

Pero esto si puede ser detectado por herramientas `IDS`.

Tambien lo que podemos hacer es desubrir los servicios de los puertos que tenga ese `host` con `netcat` ya que cuando nos intentamos generalmente conectar a dicho puerto por defecto tiene que enviar un `banner` en el cual se especifica la version del servicio u otras catacteristicas mas.

```shell
netcat -nv 192.168.20.128 21
```

Info:

```
(UNKNOWN) [192.168.20.128] 21 (ftp) open
220 (vsFTPd 3.0.2)
```

Como estamos viendo si nos intentamos conectar a un `FTP` que la maquina tenga desplegado, nos muestra como `banner` la version del servicio ya de primeras.

Para tambien identificar si un `host` esta activo, aunque el puerto no este activo en dicho `host` podremos identificarlo con el siguiente mensaje:

```shell
netcat -nv 192.168.20.128 90
```

Info:

```
(UNKNOWN) [192.168.20.128] 90 (?) : Connection refused
```

Vemos que no hay ningun puerto `90` activo en la `128`, pero no esta dando un `Connection refused` por lo que nos indica que el `host` esta activo.
