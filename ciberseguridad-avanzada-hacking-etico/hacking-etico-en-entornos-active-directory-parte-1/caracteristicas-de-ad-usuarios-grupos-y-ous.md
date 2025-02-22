---
icon: users-between-lines
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

# Características de AD - Usuarios, Grupos y OUs

Generalmente un `administrador` se va a encontrar la mayor parte del tiempo en la siguiente seccion dentro del `DC`:

Dentro del `Administrador del servidor` -> `Herramientas` -> `Usuarios y equipos de Active Directory`.

Dentro de ese aparatado sera el principal para un `administrador`, ya que es donde puede gestionar todos los usuarios, sus limitaciones, privilegios al igual que los equipos, etc...

En la parte de la izquierda apareceran todos los dominios que tenemos creados en nuestro `Bosque`, que en este caso solo tendremos el de `corp.local`, si nosotros desplegamos esa carpeta del dominio, veremos otras subcarpetas las cuales se les llama carpetas logicas en las que son como objetos que principalmente no llevan nada en su interior, pero cuando veamos una carpeta con un cuadradito dentro en el logo de la siguiente forma:

<figure><img src="../../.gitbook/assets/image (210).png" alt=""><figcaption></figcaption></figure>

Esto se corresponde con `OUs` (Unidades Organizativas) y en ellas vamos a poder establecer políticas.

Si nosotros entramos por ejemplo dentro de la carpeta `Computers` veremos que tenemos 2 equipos dentro del dominio que son el `WS01` y el `WS02`.

Dentro de la carpeta `Domain Controllers` tendremos nuestro `DC01` el cual esta el unico equipo que esta actuando como controlador de dominio que es el `Windows Server` que estamos utilizando actualmente.

Dentro de la carpeta `Users` tendremos todos los usuarios a nivel de dominio que tendremos dentro de nuestro dominio `corp.local` incluidos los usuarios que creamos previamente y mas de los cuales vienen por defecto en el sistema.

Generalmente los `administradores` van a crear los usuarios o grupos desde esa parte de `Users` y no como lo hicimos anteriormente, ya que te vienen mas opciones a nivel de seguridad frente al dominio, por lo que seria una buena practica la creacion de usuarios y grupos en esta parte de la carpeta y para crear uno seria de la siguiente forma:

Click en la parte de la carpeta de `corp.local` -> click derecho en la seccion donde estan todas las carpetas -> `Nuevo` -> `Crear usuario` -> nos aparecera lo siguiente:

<figure><img src="../../.gitbook/assets/image (211).png" alt=""><figcaption></figcaption></figure>

Por lo que vamos a probar a crear el usuario `empleado3` con su contraseña `Passw0rd4`, seguimos todos los pasos, poniendo que la contraseña nunca expire y cuando finalicemos, veremos que el usuario se creo en el mismo directorio donde estan todas las carpetas, por lo que vemos que la carpeta `Users` no es una carpeta organizativa y si lo dejamos como esta lo va a reconocer a nivel de dominio aunque no este dentro de la carpeta `Users`:

<figure><img src="../../.gitbook/assets/image (212).png" alt=""><figcaption></figcaption></figure>

Pero lo moveremos a la carpeta `Users` arrastrandolo a ella simplemente.

### Crear un OUs/Departamento a nivel de dominio

Si nosotros queremos crear un nuevo departamento como carpeta de una `OUs` seria de la siguiente forma, le daremos a este icono:

<figure><img src="../../.gitbook/assets/image (213).png" alt=""><figcaption></figcaption></figure>

Ya que esto se utiliza para dividir departamentos, otros grupos, subdepartamentos, etc... Dentro de una empresa.

Cuando pulsamos en el icono veremos una ventana en la que tendremos que poner el nombre que le queremos dar a la Unidad Organizativa en mi caso sera `TestDept`, si lo creamos veremos que tendra un cuadradito dentro la carpeta en el icono y con esto sabremos que es una carpeta de una Unidad Organizativa.

Si nosotros queremos mover los 3 usuarios que hemos creado a la carpeta de la Unidad Organizativa que hemos creado `TestDept` para que pertenezcan a esa `OUs` lo haremos arrastrando los 3 usuarios a dicha carpeta, por lo que se vera algo asi:

<figure><img src="../../.gitbook/assets/image (214).png" alt=""><figcaption></figcaption></figure>

Con esto podemos decir que estos 3 usuarios pertenezcan a este departamento en concreto y asi con todos los usuarios y departamentos que creemos, para tenerlo organizado todo.

### Crear un grupo a nivel de dominio

Lo que tambien podemos crear ahi dentro es un grupo de la siguiente forma, pincharemos en el siguiente icono:

<figure><img src="../../.gitbook/assets/image (215).png" alt=""><figcaption></figcaption></figure>

Se nos abrira una ventana en la que pondremos como nombre de grupo `TestGroup`.

<figure><img src="../../.gitbook/assets/image (216).png" alt=""><figcaption></figcaption></figure>

En esta parte de aqui `Universal` se refiere a que va a pertenecer a todos los `Forests` que tuviesemos, el `Global` que se aplica a todos los dominios que tengamos dentro de nuestro `Forest` y el `Domain local` que se aplica a solamente dentro de este dominio en mi caso `corp.local`.

En este apartado:

<figure><img src="../../.gitbook/assets/image (217).png" alt=""><figcaption></figcaption></figure>

Se refiere con el de `Security` a los grupo donde se le va a poner politicas de seguridad para administrar o cualquier otro tipo que tenga que ver con la seguridad y el de `Distribution` que se refiere a que cuando por ejemplo si quiero crear una lista de correco electronico tener una serie de usuarios a los que le lleguen dichos correos (Por ejemplo. Grupo de incidencias) pues tu mandas ese correo a dicho grupo el cual tiene el tipo de `Distribution` y se le enviaria a todos los usuarios que pertenezcan a dicho grupo.

### Añadir usuarios a un grupo de dominio

Ahora para añadir a usuarios a dicho grupo le daremos click derecho en el grupo -> `Propiedades` -> vamos a la seccion de `Miembros` -> `Agregar` -> escribimos `empleado` sin mas y le damos a `Comprobar` -> esto nos saltara los resultados encontrados con esa palabra a nivel de usuario y veremos los 3 empleados, por lo que agregaremos a los 3 -> `Agregar` -> `Aceptar` -> `Aplicar` -> `Aceptar`.

Y con esto ya estarian añadidos a dicho grupo.

### Añadir un grupo dentro de otro grupo a nivel de dominio

Tambien lo que se puede hacer es meter a un grupo dentro de otro grupo, pero esto tiene unas consecuencias de seguridad bastante grabes si no se gestiona bien, las cuales veremos mas adelante.

Le daremos click derecho al grupo -> `Propiedades` -> `Miembro de` -> `Agregar` -> escribimos `Administrad` y le damos a `Comprobar Nombres` -> seleccionamos `Administradores` -> `Aceptar` -> `Aplicar` -> `Aceptar`.

Con esto habremos metido el grupo de `TestGroup` dentro del grupo `Administradores`.

Pero esto tiene un riesgo ya que hereda los permisos del grupo administrador el grupo `TestGroup` que a su vez lo heredan los usuarios que esten dentro en mi caso los 3 empleados, por lo que ahora mismo los 3 empleados podrian realizar acciones de administrador.

### Características avanzadas

Para ver mas información le daremos a `ver` -> marcaremos `Características avanzadas`.

Y ahora podremos ver cosas mas a nivel avanzado en las que podremos tocar de mejor forma:

<figure><img src="../../.gitbook/assets/image (218).png" alt=""><figcaption></figcaption></figure>

Si ahora por ejemplo le damos a `TestDept` -> click derecho a `empleado1` -> `Propiedades`

Veremos muchisimas mas opciones de las que veiamos antes:

<figure><img src="../../.gitbook/assets/image (219).png" alt=""><figcaption></figcaption></figure>

Si le damos a `Security` podremos ver las opciones de seguridad que tiene el usuario y lo que queremos que haga o lo que no.

Si dentro de esta seccion le damos a `Opciones avanzadas` veremos una cosa que se llama `DACL` que son listas de control de acceso que exploraremos mas adelante, aqui veremos los permisos y los objetos que tienen cada uno de forma muy detallada.

Ahora vamos a eliminar el grupo `TestGroup` simplemente dandole click derecho y eliminar.
