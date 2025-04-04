---
icon: share-all
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

# Características de AD - GPOs y recursos compartidos

En este caso nos iremos en la parte de `Administrador del servidor` -> `Herramientas` -> `Administracion de directivas de grupo`

Ha esto se le denomina `GPO` las politicas que aplicamos sobre diferentes objetos, aqui nos aparecera nuestro `Bosque: copr.local` con sus dominios, sitios, etc... en su interior.

Si abrimos la carpeta `dominios` -> `corp.local` -> `Objeto de directiva de grupo`

Dentro de el veremos varias politicas que hay creadas por defecto, en las demas carpetas encontraremos las politicas a las que estan asociadas de las politicas creadas en `Objeto de directiva de grupo`.

### Crear/Editar una política

Vamos a darle click derecho a `TestDept` -> `Crear un GPO en este dominio y vincularlo aqui...` -> dentro de aqui lo que vamos a crear con esta politica es que cuando se inicie sesion se ejecute un script que realice algunas acciones determinadas, le pondremos como nombre `Logon script Policy` -> `Aceptar`

Y esto ya crea automaticamente la politica dentro de la carpeta `TestDept`.

Ahora le vamos a dar click derecho en la politica -> `Editar politica` -> dentro de esta seccion se puede configurar para que solo aplique a nivel de equipo o a nivel de usuario determinando cuales queremos que aplique a que.

La seccion de las `Directivas` se aplican cada `90 minutos`, por lo que cuando añadamos una directiva nueva, pasados `90 Minutos` comprobara si hay alguna politica de directiva nueva y la aplicara, sin que el usuario pueda decidir si aplicarla o no.

En las preferencias, ira mas dedicado al estilo en como se crea un escritorio, como se distribuye y en esta seccion el usuario si podra elegir determinadas cosas que el `Administrador` quiera.

Si nos vamos a `Configuracion del usuario` -> `Directivas` -> `Configuracion de Windows` -> `Scripts (inicio de sesion o cierre de sesion)` -> configuraremos que cuando inicie sesion se ejecute algo le daremos doble click en el script llamado `Iniciar sesion` -> dentro de esta seccion tendremos que seleccionar el script que queremos que se ejecute, por lo que vamos a crearlo antes:

> script.bat

```bat
calc.exe
```

Esto lo que hara sera abrir una calculadora de `Windows` simplemente eso para ver que funciona bien la politica.

Una vez creado, seleccionaremos en el panel donde estabamos a `Mostrar archivos` -> se nos abrira en la siguiente ruta `\\corp.local\SysVol\corp.local\Policies\{1825ED2B-B7CE-4DC1-A903-A50B21A0004C}\User\Scripts\Logon` y tendremos que arrastrar el script a la carpeta que se abre teniendo algo asi:

<figure><img src="../../../.gitbook/assets/image (220).png" alt=""><figcaption></figcaption></figure>

Echo esto cerraremos la ventana -> `Agregar` -> `Examinar` -> seleccionamos el `script.bat` -> `Abrir` -> `Aceptar` -> `Aplicar` -> `Aceptar`

Y con esto ya estaria configurado dicho script.

Ahora si nos vamos al equipo del `empleado1` e iniciamos sesion veremos que se nos ejecuta la calculadora, por lo que esta funcionando bien, ya que este usuario junto a los demas estan dentro del `OUs` `TestDept` y este a la vez tiene asignado una politica de script que cada inicio de sesion ejecute dicho script y los usuarios que metamos dentro de este departamento se ejecutara en su inicio de sesion.

Una vez probado esto ya podremos eliminar esa politica.

### Crear un recurso compartido

Ahora si nos vamos al `Servidor del administrador` -> en la seccion de la izquierda llamada `Servicios de archivos y de almacenamiento` -> `Recursos compartidos` -> dentro de `Volumen` -> `TAREAS` -> `Nuevo recurso compartido` -> lo dejamos por defecto `Siguiente` -> `Siguiente` -> le pondremos como nombre `departamental` nos aparecera la informacion de donde se va a ubicar y como se podra acceder a ella (`\\DC01\departamental`) -> `Siguiente` -> `Siguiente` -> dentro de esta seccion podemos personalizar los permisos que queremos que tenga esta carpeta compartida pero lo dejaremos por defecto `Siguiente` -> `Crear` -> `Cerrar`

Ahora veremos que se nos creo correctamente:

<figure><img src="../../../.gitbook/assets/image (221).png" alt=""><figcaption></figcaption></figure>

Ahora para acceder a el abriremos en nuestro `DC` una carpeta normal y en la barra de busqueda pondremos lo siguiente `\\DC01\departamental`:

<figure><img src="../../../.gitbook/assets/image (222).png" alt=""><figcaption></figcaption></figure>

Y con esto estaremos dentro de dicha carpeta:

<figure><img src="../../../.gitbook/assets/image (223).png" alt=""><figcaption></figcaption></figure>

Se podra acceder a ella los usuarios que esten dentro de este dominio, por lo que podremos hacerlo de la misma forma para los otros 3 usuarios de `Windows 10`.

Y podemos acceder mediante el nombre de dominio `DC01` ya que nuestro `DC` actua como servidor `DNS` sin necesidad de tener que meter la IP.

Ahora vamos a crearnos una politica con un script en la que cada vez que inicien sesion los usuarios les aparezca el recurso compartido de la carpeta `departamental`, por lo que crearemos como hicimos anteriormente una politica en `TestDept` llamada `Unidad Compartida Policy` -> dentro del script que creemos en el escritorio pondremos lo siguiente:

> script.bat

```bat
net use t: \\192.168.5.5\departamental
```

Cargamos el script como hicimos anteriormente y si iniciamos sesion por ejemplo en el usuario `empleado1` y nos vamos a la carpeta veremos lo siguiente:

<figure><img src="../../../.gitbook/assets/image (224).png" alt=""><figcaption></figcaption></figure>

Vemos que se ha creado correctamente.

Nosotros tambien con este usuario de primeras y como esta configurado por defecto si nos vamos a la siguiente direccion `\\DC01\sysvol\corp.local\Policies\{507F35A7-D0D3-4917-9561-240C31EE0DD4}\User\Scripts\Logon` podremos ver el script que hemos creado desde el `Administrador` y lo podremos editar a la vez que visualizar lo que se esta ejecutando, esto es una mala configuracion ya que con esto podremos hacer varias cosas y como `Administrador` ya que se ejecuta como `Administrador`.

Ahora vamos a dejar todo como estaba antes, vamos a mover los usuarios de `TestDept` a la carpetas `Users`, pero si intentamos eliminar la carpeta `TestDept` no podremos ya que esta protegido contra eliminaciones accidentales, por lo que tendremos que hacer lo siguiente:

Le daremos click derecho -> `Propiedades` -> `Objeto` -> desmarcar `Proteger objeto contra eliminaciones accidentales` -> `Aplicar` -> `Aceptar`

Y con esto ya podremos eliminarlo, tambien eliminaremos el `empleado3`.
