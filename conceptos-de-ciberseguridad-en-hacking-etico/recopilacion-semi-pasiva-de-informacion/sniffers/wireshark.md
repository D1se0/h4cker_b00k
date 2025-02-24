---
icon: wifi
---

# Wireshark

Cuando hay una conexion entre varios equipos se le denomina `red` y cuando varios equipos estan en una `red` a estos se les llama `nodos` (Equipos de una red).

Cuando estos datos llegan a otro `nodo` de la `red` con el que estamos intercambiando informacion, este `nodo` recibe los datos (Una cadena de `bytes`) y de alguna manera tiene que interpretarlos, es decir, tiene que determinar que del `byte 0` al `byte 10` va un campo determinado, que por ejemplo puede ser un campo de texto, del `byte 11` al `byte 15` va otro campo determinado y asi sucesivamente. Esto es para poder entender que informacion nos esta enviando el otro `nodo`, pero a priori es simplemente una `ristra de bytes`, para interpretar esta informacion que se esta intercambiando entre diferentes `nodos` de la `red` lo que se utiliza son los `prtocolos de red` (Conjunto de reglas que se aplica sobre la informacion recibida de una `red` de manera que se pueda interpretar), dependiendo del protocolo que se este implementando se interpretara la informacion de una manera o de otra.

Los `Sniffers` son herramientas las cuales se van a situar en nuestro `sistema operativo` y su funcion sera `monitorizar` todo el `trafico de red` tanto entrante como saliente que estamos intercambiando con otros `nodos` de la `red`.

En `wireshark` cuando lo ejecutamos y se abre, veremos varias interfaces de `red`, si el equipo estuviera con mas adaptadores de red, en `wireshark` se veria, pero vamos hablar de las que vienen por defecto, que entre ellas serian las 3 primeras que aparecen:

```
eth0
Loopback: lo
any
```

`eth0` es la tipica interfaz de `red` primaria donde pasa practicamente todo nuestro trafico de `red` a nivel de `internet`

`Loopback: lo` es el `localhost` de nuestra `red` de forma simplificada.

`any` seria cualquier interfaz de `red`.

En nuestro caso vamos a capturar el trafico de la interfaz de `red` tipica `eth0` por lo que le daremos doble click y entraremos en un modo `monitor` de captura de `red` entre los `nodos` que esten en dicha `red` o cualquier cosa que se este transmitiendo por la `red`.

Deberemos de ver algo asi:

<figure><img src="../../../.gitbook/assets/image (13) (1).png" alt=""><figcaption></figcaption></figure>

Si nosotros abrimos un navegador o hacemos cualquier cosa que genere trafico de `red` podremos observar en `wireshark` que se nos captura dichos protocolos, paquetes, etc... Tambien podremos filtrar por protocolos, IP's, etc... En la barra superior poniendo lo que queremos filtrar en caso de que exista nos lo mostrara, si no, no mostrara nada.

De estos botones:

<figure><img src="../../../.gitbook/assets/image (14) (1).png" alt=""><figcaption></figcaption></figure>

El de la izquierda del todo es para empezar a capturar el trafico, y el del medio es para parar de capturar el trafico.

Si por ejemplo filtramos por `DNS` nos apareceran los paquetes de `DNS` y si pulsamos en uno de ellos, veremos lo siguiente:

<figure><img src="../../../.gitbook/assets/image (15) (1).png" alt=""><figcaption></figcaption></figure>

Es una secuencia de `bytes` codificados en `hexadecimal` y si ponemos el raton encima de una de la secciones del `hexadecimal` veremos que se corresponde a la seccion de la derecha en formato texto. (`wireshark` nos lo muestra con las reglas de los protocolos de `red` ya aplicadas)

En esta seccion esta lo que mencione de los protocolos de `red` que `wiresharkk` ha ido siguiendo siendo el primero el llamado `Ethernet`:

<figure><img src="../../../.gitbook/assets/image (16) (1).png" alt=""><figcaption></figcaption></figure>

Y con esto podremos ir siguiendo el rastro de paquetes en la `red` de como lo ha ido combinando con los protocolos hasta finalmente mostrarnos a nivel usuario los `bytes` codificados en `hexadecimal`.

Si nos vamos a la `lupa` que tenemos encima:

<figure><img src="../../../.gitbook/assets/image (17) (1).png" alt=""><figcaption></figcaption></figure>

Nos aparecera un recuadro de busqueda debajo de la seccion de la `lupa`:

<figure><img src="../../../.gitbook/assets/image (18) (1).png" alt=""><figcaption></figcaption></figure>

Donde pone `Display Filter` por ejemplo ponemos que nos filtre por `String` y buscamos lo que el usuario haya buscado en internet que hayamos descuvierto por ejemplo `kali.org`, quedamdo algo asi:

<figure><img src="../../../.gitbook/assets/image (19) (1).png" alt=""><figcaption></figcaption></figure>

Si pinchamos en uno, nos pondra que la busqueda es de tipo `(query)`:

<figure><img src="../../../.gitbook/assets/image (21) (1).png" alt=""><figcaption></figcaption></figure>

Si desplegamos `Domain Name System (query)` veremos que si bajamos un poco es de `tipo A` por lo que es lo que estamos buscando ya que significa que podremos acceder a la petición a ese servidor web de dicho dominio y que nos devuelva la pagina web que queremos renderizar en nuestro navegador.

<figure><img src="../../../.gitbook/assets/image (22) (1).png" alt=""><figcaption></figcaption></figure>

Si queremos ver la respuesta de esa busqueda, podremos identificarlo con las flechas que marca `wireshark`:

<figure><img src="../../../.gitbook/assets/image (23) (1).png" alt=""><figcaption></figcaption></figure>

La flecha `->` indica que es la "Pregunta" (Busqueda) y la flecha `<-` es la respuesta de esa "Pregunta" (Busqueda o resultados)

Por lo que se pinchamos en la `respuesta` y bajamos, veremos dentro de `Domain Name System (Responder)` un apartado de `Answer` y si lo desplegamos veremos el dominio que se ha buscado junto a la `IP` a la que pertenece ese dominio.

<figure><img src="../../../.gitbook/assets/image (24) (1).png" alt=""><figcaption></figcaption></figure>

Si por ejemplo la busqueda que hemos echo fuera por `HTTP` sin `SSL` la conexion no estaria cifrada, por lo que a la hora de capturar el trafico de `red` podria identificarse mucho mejor la informacion ya que el `HTTPS` cifra la informacion con unos metodos de algoritmos para que no sea entendible a nivel usuario.

Si filtramos por `HTTP` y nos vamos al primero que ponga en la seccion de `protocolos` `HTTP`, le daremos click derecho -> `Follow` -> `HTTP Stream` y esto nos abrira una ventana representando la pagina que hemos buscado en internet:

<figure><img src="../../../.gitbook/assets/image (25) (1).png" alt=""><figcaption></figcaption></figure>

Nos lo proporcionara el `ASCII`.
