---
icon: album
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

# Balanceadores y almacenamiento en la nube (AWS)

Para crear un `balanceador de carga` tendremos que irnos a `Load Balancing` -> `Load Balancers` -> `Create Load Balancer` -> seleccionaremos el llamado `Application Load Balancer` -> `Create` -> lo llamaremos `WEBAPP-LB`, en `VPC` seleccionaremos `WEBAPP-VPC`, en `Mappings` seleccionaremos las `2` zonas de disponibilidad, en `Security Groups` seleccionaremos el `LB-SG`, en `Listeners` seleccionaremos `Create Target Group` -> lo llamaremos `WEBAPP-TG` -> `Next` -> meteremos los `2` servidores en el `target group` -> `Include as pending below` -> `Create Target Group` -> ahora actualizamos y seleccionamos `WEBAPP-TG`:

<figure><img src="../../../.gitbook/assets/image (57).png" alt=""><figcaption></figcaption></figure>

Le daremos a `Create Load Balancer` y con esto ya lo tendremos creado:

<figure><img src="../../../.gitbook/assets/image (58).png" alt=""><figcaption></figcaption></figure>

Ahora en la informacion del `balanceador` se accederia desde esa `URL` que te proporciona `Amazon`:

<figure><img src="../../../.gitbook/assets/image (59).png" alt=""><figcaption></figcaption></figure>

Que eso realmente es donde `google` te redirigiria si intentaras acceder a la web en vez de al servidor real como medida de seguridad.

Ahora vamos a instalar un `RDS` buscando eso mismo para poder crear una base de datos:

<figure><img src="../../../.gitbook/assets/image (60).png" alt=""><figcaption></figcaption></figure>

Le daremos a `Create database` -> seleccionaremos `MySQL`, seleccionaremos la version `MySQL 5.7.34`, en los `templates` seleccionaremos `Free tier`, lo llamaremos `WEBAPP-DB`, renombraremos el nombre de usuario de `admin` a `dbadmin`, pondremos una contraseña sencillita para no complicarnos, en `VPC` seleccionamos el nuestro `WEBAPP-VPC`, en el `VPC Security Group` seleccionaremos el `BD-SG`, en `Additional Configuration` le pondremos como nombre `phonebook` -> `Create database`

Con esto ya se estaria creando la base de datos:

<figure><img src="../../../.gitbook/assets/image (61).png" alt=""><figcaption></figcaption></figure>

Si nosotros pulsamos en la base de datos, una de las cosas que nos proporciona es un `endpoint` que es como si fuese un nombre de dominio para ese servidor de base de datos, si nosotros como administradores y programadores quisiesemos que se comunicara con la base de datos a traves del codigo tendriamos que meter ese `endpoint` y el puerto para que se comunicara de forma correcta:

<figure><img src="../../../.gitbook/assets/image (62).png" alt=""><figcaption></figcaption></figure>

Ahora vamos a irnos al `Load Balancer` el dominio que nos porporciona para comunicarnos con la pagina web y pulsaremos el boton de `RDS` para que nos lleve a esta parte:

<figure><img src="../../../.gitbook/assets/image (63).png" alt=""><figcaption></figcaption></figure>

Pondremos el `endpoint` que nos proporciono la base de datos, el nombre que pusimos a la base de datos que fue el `phonebook`, despues el nombre de usuario que era `dbadmin` y la contraseña que le hayamos configurado:

<figure><img src="../../../.gitbook/assets/image (64).png" alt=""><figcaption></figcaption></figure>

Le daremos a `Submit` y si todo fue bien se estara generando una conexion en una de esas dos instancias que tenemos de los `2` servidores y estara creando una serie de tablas para los servidores y si le volvemos a dar al boton de `RDS` veremos lo siguiente:

<figure><img src="../../../.gitbook/assets/image (65).png" alt=""><figcaption></figcaption></figure>

Vemos que se creo todo correctamente, pero si lo volvemos a cargar a lo mejor nos lleva otra vez a la anterior parte en la que teniamos que rellenar la info para crear la base de datos, ya que el `blanceador de carga` nos estara realizando la conexion en el otro servidor en el que toddavia no hemos creado eso, por lo que tendremos que volver a meter dicha informacion para que se nos cree tambien en ese servidor y cuando recarguemos podremos ver en los dos servidores la base de datos de forma correcta.
