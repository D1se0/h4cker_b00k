# Inyecciones de codigo y contexto

Para que pueda haber una injeccion de codigo tiene que haber algun campo dentro de la pagina web en el que nosotros podamos interactuar con esa aplicacion objetivo, estos campos normalmente suelen llamarse `puntos de injeccion` ya que es el punto en el que nosotros podemos meter codigo/informacion que la aplicacion objetivo cuando la reciba va a parsearla/analizarla y hara algo con ella.

Si nosotros capturamos una autenticacion de `login` con `Burp Suite` a parte de poder intentar ver algun tipo de vulnerabilidad que tenga la pagina, tambien en algunos casos podremos ver las `Coockies` del usuario, por lo que seria otro punto de injeccion, a parte de que en la pestaña `Params` nos filtrara de mejor forma toda la informacion del `request`.

Para diferenciar un `SQL Injecction` de un `Cross-site-Scripting (XSS)` es el contexto en el que estamos realizando esa injeccion de codigo, muchas veces para ver donde responde el servidor y para ver donde se ha realizado la injeccion de codigo nosotros utilizamos una cosa que denomina `canario`, un `canario` es simplemente una palabra clave que nosotros metemos para que cuando recivimos la respuesta del servidor podamos buscar en el codigo de respuesta donde se ha injectado nuestro codigo.

Por ejemplo, estando con `Burp Suite` a la escucha de cualquier peticion, realizamos una peticion de login con la siguiente informacion:

```
User: canario
Pass: canariopassword
```

Y veremos algo asi:

<figure><img src="../../../../.gitbook/assets/image (59) (1).png" alt=""><figcaption></figcaption></figure>

Le damos a `Forward`, nos responde el servidor de aplicacion y en el buscaremos la palabra `canario` en la barra de busqueda en la parte de abajo:

<figure><img src="../../../../.gitbook/assets/image (60) (1).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../../../.gitbook/assets/image (61) (1).png" alt=""><figcaption></figcaption></figure>

Por lo que podemos comprobar es que nuestra palabra `clave` viene reflejada en la respuesta del servidor y vemos que viene dentro de un contexto en `HTML` dentro de unos parametro de `HTML` por lo que podremos pensar ya en algunas vulnerabilidades como `XSS`, por lo que probaremos a cerrar la etiqueta `HTML` y abrir una nuestra para ver que puede pasar.

Por lo que volveremos a capturar la peticion del login con la palabra clave, para hacerle los cambios desde `Burp Suite`.

En la seccion de `Username` pondremos lo siguiente:

```
&username=</span><script>alert('alerta xss')</script>
```

Para cerrar el `span` de antes y ejecutar una sentencia nuestra de `HTMl`, pero veremos que no lo coge muy bien `Burp Suite` por lo que haremos lo siguiente:

Le daremos click derecho a todo lo que escribimos y seleccionaremos la que pone `URL-encode as with type` para codificarlo en `URL` y que asi funcione.

Cortaremos esa linea:

```
</span><script>alert('alerta xss')</script>
```

Y nos iremos a la pestaña del `Decoder`, pegaremos esa linea en el cuadro de la izquierda y en el boton de `Encode as ...` podremos ponerle la opcion `URL`, para que nos lo muestre en `URL Encode`, seria otra forma de codificarlo.

<figure><img src="../../../../.gitbook/assets/image (62) (1).png" alt=""><figcaption></figcaption></figure>

Copiamos el codificado y lo pegamos donde `username`.

<figure><img src="../../../../.gitbook/assets/image (63) (1).png" alt=""><figcaption></figcaption></figure>

Ahora le daremos a `Fordware` 2 veces para enviar las 2 peticiones del cliente y del servidor, una vez echo esto, si vamos a la pagina veremos lo siguiente:

<figure><img src="../../../../.gitbook/assets/image (64) (1).png" alt=""><figcaption></figcaption></figure>

Ahora si por ejemplo hacemos una consulta, para comprobar si es vulnerable a un `SQLInjecction` podremos hacerlo de la siguiente forma:

```
User: diseo'
Pass: null
```

Si ponemos esa comilla simple, veremos lo siguiente:

<figure><img src="../../../../.gitbook/assets/image (65) (1).png" alt=""><figcaption></figcaption></figure>

Nos esta mostrando un error, el cual ya de por si esto es un fallo de seguridad respecto a como se esta haciendo la consulta y por que ha fallado.

Por lo que podremos aprovechar esto, para injectar codigo `SQL`.

Si ponemos lo siguiente, podremos aprovechar dicha vulnerabilidad para que nos saque todas las bases de datos de los usuarios de `mysql`:

```
User: diseo' OR 1=1-- -
Pass: null
```

Y veremos que funciono:

<figure><img src="../../../../.gitbook/assets/image (66) (1).png" alt=""><figcaption></figcaption></figure>

Ya que lo que estamos haciendo es que se cumpla siempre la condicion, ya que `1` es igual a `1` siempre, por lo que cuando se cumple la condicion nos muestra la informacion de dicho usuario, pero en este caso como es generico nos dumpea toda la informacion de la base de datos.
