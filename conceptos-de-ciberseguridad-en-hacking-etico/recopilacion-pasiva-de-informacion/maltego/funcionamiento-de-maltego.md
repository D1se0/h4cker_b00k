---
icon: file-circle-info
---

# Funcionamiento de Maltego

`Maltego` actua como transformador de la informacion a la hora de hacer consultas a las bases de datos (querys), consultas a distintos repositorios, etc... Mostrandonos la informacion obtenida de forma detallada y visual en un espacion de trabajo, con diferentes transformadores que te proporciona `maltego`.

Dentro de los transformadores, tendremos que ver algo asi:

<figure><img src="../../../.gitbook/assets/image (3) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Si no aparece lo de logearte no tendremos eso, para logearnos de forma manual, nos tendremos que ir al simbolo de arriba a la izquierda de `maltego` -> `Licence Manager` -> y seguir los pasos para obtener una licencia de la comunidad logeandote o registrandote

Estando en esa parte de los transformadores, instalaremos algunas adiccionales, entre ellas la llamada `Have I Been Pwned?`, `Virus Total` (En el caso de este nos pedira una APIKey la cual tendremos que irnos a la pagina donde nuestra cuenta y copiar esa APIKey), `Social Link`,etc...

Ahora vamos a crear un llamado `Grafo` que es como nuestro espacio de trabajo, donde esta el simbolo de una hoja blanca con un `+`.

En este `grafo` vamos a poder arrastrar diferentes entidades que es lo de la parte de la izquierda donde cada una de las entidades mostrara un tipo de informacion en concreto, lo que nos permitira buscar informacion mediante los transformadores.

Imaginemos que queremos investigar a alguien, en la barra de busqueda de arriba buscaremos `Persona` y arrastraremos la entidad `persona` al campo de trabajo creandose un circulo de un logo de una `persona` con un nombre random.

Podremos editar el nombre dandole doble click en el.

A esta persona la podemos ligar alguna organizacion, buscando `Company` y arrastrandolo al campo, la renombramos haciendo doble click.

Si la damos al siguiente icono:

![](<../../../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png>)

Podremos ligarlo a la compañia poniendo el nombre de `Trabaja en` y dandole aceptar se creara una flecha.

Si nos vamos a las siguientes opciones pulsando en la persona:

![](<../../../.gitbook/assets/image (2) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png>)

Y le damos a `All Transforms` podremos ver todo lo que podemos ejecutar para buiscar informacion de esa persona, tanto correos, numeros de telefono, informacion debil, etc... De todo.

Nosotros lo que vamos hacer es ejecutar todos los transformadores a la vez para ver que informacion nos reporta dandole al icono `>>` de donde pone `All Transforms`, si le damos a ejecutar todo, tendremos que ver algo asi:

![](<../../../.gitbook/assets/image (3) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png>)

Nos habra encontrado bastante informacion sobre dicho usuario.

Si nos vamos a una de esas busquedas y le damos doble click, nos aparecera una ventana en la que mostrara mas informacion y si nos vamos a la pestaña `Propietiers` podremos ver la informacion de cuando se creo el documento, etc...

Puede encontrar nominas, documentos sensibles, cuentas de redes sociales, etc...

A este usuario le podemos añadir un `alias` en tal caso de que lo hayamos descubierto haciendo `google hacking` o demas cosas, para añadirle esto lo haremos de la siguiente forma.

buscaremos la palabra `alias` y lo arrastramos al campo de trabajo, lo unimos con la `persona` y lo nombramos como `tiene un alias`.

Le damos doble click en el `alias` y ponemos el nombre del `alias`.

Le daremos un click a `alias` para seleccionarlo y buscaremos por redes sociales dandole `All run` al transformador llamado `Social Link`.

Y si le damos tambien a buscar todo, podremos identificar bastante informacion con dicho `alias`.

Imaginemos que hemos encontrado un correo electronico el cual queremos investigar, podremos hacerlo arrastrando el llamado `Email Address` y dandole doble click pegamos el correo electronico que encontramos.

Ahora creamos una relacion con la `persona` al correo llamada `Tiene un email`.

Podemos ejecutar para investigar ese `email` el transformador `Have I Been Pwned?` y la primera opcion en concreto, por lo que si tiene alguna brecha esta te la mostrara.
