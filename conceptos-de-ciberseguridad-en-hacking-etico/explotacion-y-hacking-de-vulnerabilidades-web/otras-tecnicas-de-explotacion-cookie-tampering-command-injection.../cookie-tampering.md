# Cookie Tampering

Llendonos a `OWASP 2017` -> `Injection SQL` -> `SQLi Extract Data` -> `User Info (SQL)`, que es donde realizaremos dicha tecnica.

Una `Cookie` es simplemente una porcion de informacion que solicita el servidor web para que tu navegador la mantenga almacenada y cuando hacemos peticiones a ese servidor introduzca dicha informacion.

Para interceptar las `Cookies` en este caso abriremos `Burp Suite` y estando a la escucha ejecutaremos la peticion, una vez que lo hayamos capturado con `Burp Suite` veremos lo siguiente:

<figure><img src="../../../.gitbook/assets/image (109).png" alt=""><figcaption></figcaption></figure>

Vemos algunas `Cookies` en la seccion de `Cookie:`.

En este caso hay 2 importantes la llamada `PHPSESSID=` y la `showhints=`, en este caso la segunda mencionada esta visible con valor `1` ya que en la pagina de `Mutillidae` tenemos activado el `Toggle Hints`:

<figure><img src="../../../.gitbook/assets/image (110).png" alt=""><figcaption></figcaption></figure>

Si lo desactivamos dandole al mismo boton, cuando lo captures se pondra en `0`.

Y la parte de `PHPSESSID=` es la sesion del usuario entera, pero en la parte de `showhints=` si esta en `0` y la modificamos a `1` mediante `Burp Suite` cuando le demos a `Forward` la pagina se va a creer que esta en `1` y le va a mostrar las `hints` por lo que es un punto de injeccion.

Si nos vamos a la pagina de `login` como para logearnos y ponemos a nuetro `Burp Suite` a interceptar, cuando enviemos dichas credenciales, las capturaremos con `Burp Suite` si nosotros le damos a `Forward` veremos lo siguiente:

<figure><img src="../../../.gitbook/assets/image (111).png" alt=""><figcaption></figcaption></figure>

Se nos esta estableciendo en `Set-Cookie:` el `username` y el `uid`, con esto lo que esta hacien es pedirle al servidor que almacene esas `Cookies`.

Le daremos otra vez a `Forward` y veremos esto:

<figure><img src="../../../.gitbook/assets/image (112).png" alt=""><figcaption></figcaption></figure>

Y ya a parte de almacenar la sesion con `PHPSESSID` y `showhints`, lo que va hacer es tambien almacenar el `username` y el `uid`.

Le volveremos a dar a `Forward`, quitaremos la interceptacion.

Si nosotros creamos un nuevo usuario en la pagina por ejemplo llamado `canario`, y cuando nos vayamos a logear lo interceptamos con `Burp Suite` para ver si hay alguna diferencia en las `Cookies` o en los `id's`:

<figure><img src="../../../.gitbook/assets/image (113).png" alt=""><figcaption></figcaption></figure>

Aqui vemos que hemos capturado el login del usuario `canario`, le daremos a `Forward`, veremos lo siguiente:

<figure><img src="../../../.gitbook/assets/image (114).png" alt=""><figcaption></figcaption></figure>

Estamos viendo que que nos setea las `Cookies` de nuevo, pero lo que esta cambiando aqui es el `uid` por lo que podemos llegar a creer que el `uid` es lo que esta identificando a los usuarios y puede ser un punto de injeccion.

Le daremos a `Intercept is on` para ponerlo en `off`.

Si nosotros por ejemplo pinchamos en cualquier apartado de la pagina con el `Burp Suite` interceptando para capturar la peticion:

<figure><img src="../../../.gitbook/assets/image (115).png" alt=""><figcaption></figcaption></figure>

Por lo que vemos el `uid` va en orden a las cuentas que se han ido creando y podremos deducir que el primer usuario de la pagina podria ser el administrador, por lo que si cambiamos el `uid` donde pone `42` que es nuestro identificador por el `1` a ver que usuario somos.

<figure><img src="../../../.gitbook/assets/image (117).png" alt=""><figcaption></figcaption></figure>

Le daremos a `Forward` y dejaremos de interceptar, por lo que si nos vamos a la pagina y vemos que usuario somos:

<figure><img src="../../../.gitbook/assets/image (118).png" alt=""><figcaption></figcaption></figure>

Vemos que somos el usuario `admin` por lo que ha funcionado.

Lo que tambien se podria hacer es `robar` ese `TOKEN` de sesion del `PHPSESSID`, capturarlo con `Burp Suite` y reemplazar el `PHPSESSID` nuestro por el del `administrador` el cual hayamos capturado, para tener su sesion.
