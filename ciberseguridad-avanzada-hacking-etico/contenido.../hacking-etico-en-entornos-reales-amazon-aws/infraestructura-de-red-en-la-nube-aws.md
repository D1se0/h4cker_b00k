---
icon: amazon
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

# Infraestructura de red en la nube (AWS)

Una vez que entremos dentro veremos la consola de `amazon AWS`:

<figure><img src="../../../.gitbook/assets/image (39).png" alt=""><figcaption></figcaption></figure>

`Amazon` tiene distribuidos muchos `CPDs` por todo el mundo, en nuestro caso tendremos que elegir el de `Londres` ya que es el mas cercano para que asi la `Latencia` sea mucho menor y genere una mejor conexion:

<figure><img src="../../../.gitbook/assets/image (40).png" alt=""><figcaption></figcaption></figure>

Dentro de esta region tiene zonas de disponibilidad, que esto son diferentes sitios fisicos donde tienen estos servidores que estan soportando toda esta infraestructura la cual nosotros vamos a pedir que nos cree y dentro de una misma region los tiene separados, por si ocurriera algo como un desastre natural o lo que pueda pasarle a uno de los `CPDs` tiene otro que lo respalde en la misma region que se les llama las `zonas de disponibilidad`.

Podremos crear `subredes` en una zona de disponibilidad y otra `subred` en otra zona de disponibilidad, justamente para asegurar la disponibilidad de sus servicios.

Vamos a crear una `VPC` buscando la palabra y dandole a la que nos aparece la primera:

<figure><img src="../../../.gitbook/assets/image (41).png" alt=""><figcaption></figcaption></figure>

Vamos a irnos en el panel izquierdo a `Sus VPC` -> `Crear VPC` -> la llamaremos `WEBAPP-VPC`, vamos a especificar el siguiente rango `10.0.0.0/16` -> `Crear VPC`.

Una vez que ya la tengamos creada veremos algo asi:

<figure><img src="../../../.gitbook/assets/image (42).png" alt=""><figcaption></figcaption></figure>

Ahora nos vamos a `Subredes` -> `Crear Subred` -> seleccionamos la `VPC` que creamos anteriormente el llamado `WEBAPP-VPC`, llamaremos a la subred `Subred Publica 1`, en la zona de disponibilidad veremos `3` pues seleccionaremos el numero `1`, en el bloque de CIDR pondremos `10.0.0.0/24` -> `Crear Subred`

Cuando hayamos creado la `subred` veremos algo asi:

<figure><img src="../../../.gitbook/assets/image (43).png" alt=""><figcaption></figcaption></figure>

Ahora vamos a seleccionarla -> `Acciones` -> `Editar la configuracion de la subred` -> marcaremos la casilla llamada `Habilitar la asignacion automatica de la direccion IPv4 publica` -> `Guardar`

Ahora crearemos otra `subred` de la misma forma que antes, pero esta se llamara `Subred Publica 2`, seleccionaremos en las zonas de disponibilidad la numero `2` y en el CIDR pondremos `10.0.1.0/24`.

Despues crearemos una ultima `subred` mas que esta sera la que contenga la `BBDD` de forma privada, por lo que la nombraremos `Subred Privada`, la zona de disponibilidad la dejaremos `Sin Preferencia` y le asiganremos al CIDR la `10.0.2.0/23`.

Ahora vamos a configurarle un `balanceador` en el que cuando se conecte desde internet vaya a ese `balanceador` y que muestre el mismo la pagina web y que no vayan directamente al servidor como medida de seguridad.

Pero para que tenga salida a internet, tendremos que crear un componente que se llama `Internet Gateway`.

Vamos a poner el idioma en `ingles` para que sea mas facil utilizar las opciones, nos iremos a la seccion de `Virtual Private Cloud` -> `Internet Gateways` -> `Create Internet Gateway` -> le llamaremos `WEBAPP-IG` -> `Create Internet Gateway`.

Una vez creado veremos algo asi:

<figure><img src="../../../.gitbook/assets/image (44).png" alt=""><figcaption></figcaption></figure>

Rapidamente le daremos a la opcion de arriba a la derecha llamada `Attach to a VPC` para conectarlo con un `VPC` y seleccionaremos el `WEBAPP-VPC`, ahora nuestro servidor tiene salida a internet.

Ahora lo que vamos a configurar es restringir al maximo la `Subred Privada` para que solo se pueda acceder desde un determinado servidor o `VPC` pero que no tenga salida a internet y para ello tendremos que crear un `enrutamiento`, seleccionaremos `Route Tables` -> `Create Route Tables` -> lo llamaremos `Public-RT`, seleccionaremos el `WEBAPP-VPC` en `VPC` -> `Create Route Tables`.

Una vez creado veremos lo siguiente:

<figure><img src="../../../.gitbook/assets/image (45).png" alt=""><figcaption></figcaption></figure>

Ahora vamos a crear una serie de `reglas` para ver como se pueden comunicar esas `Route Tables` y como queremos que sea la comunicacion, etc...

Le daremos a `Edit routes` -> `Add route` -> seleccionaremos `0.0.0.0/0` para que se pueda conectar a internet, en `target` pondremos `WEBAPP-IG` -> `Add route`.

Ahora crearemos otra `Route Table` que en este caso sera la privada, la llamaremos `Private-RT` y seleccionaremos en `VPC` la llamada `WEBAPP-VPC` y esta no la modificaremos ya que queremos que se quede a nivel local sin que tenga acceso a internet.

Ahora seleccionaremos la `Subred Publica 1` en la seccion de `Subredes` -> `Route tables` -> `Edir route tables association` -> en la `Route table ID` seleccionaremos `Public-RT` -> `Save`.

Ahora dentro de esa `Subred publica 1` tendra acceso a internet y todas las instancias dentro de ellas.

Haremos exactamente lo mismo para la `Subred publica 2`, pero en la `Subred privada` vamos asignarle la `Private-RT` para que sea una red privada.
