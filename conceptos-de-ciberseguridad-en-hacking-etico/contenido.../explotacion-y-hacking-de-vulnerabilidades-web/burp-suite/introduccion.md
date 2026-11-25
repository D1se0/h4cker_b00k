# Introducción

Basicamente esta herramienta es un `proxy` de interceptación, mediante una encuenta a expertos en ciberseguridad la que mas se utiliza sin ninguna duda es `Burp Suite` para las auditorias o para programas como `Bug Bounty`.

Esta herramienta se va a situar entre nuestro navegador y la aplicacion web/servidro web, al que estamos realizando la peticion para consumir esa pagina web.

Por lo que tendremos que configurar el navegador para que todas las peticiones pasen a traves de `Burp Suit` desde este `proxy` y con esto nos podra mostrar una serie de informacion, para realizar una serie de tareas las cuales nos permitiran analizar.

Esta herramienta ya viene por defecto instalada en `kali`, por lo que la podremos iniciar buscandola en el buscador o en terminal poniendo:

```shell
burpsuite
```

Le damos todo `Acpetar`, `Next`, hasta que lleguemos a `Start BurpSuite`, una vez que ya este iniciada, veremos algo tal que asi:

<figure><img src="../../../../.gitbook/assets/image (50) (1).png" alt=""><figcaption></figcaption></figure>

Esta herramienta por lo que mas se identifica y se utiliza es en la pestaña llamada `Proxy`.

Si nos vamos a la pagina de `mutillidae` que configuramos e intentamos hacer una peticion `proxy` como recargar la pagina o irnos algun sitio de la pagina, no capturara nada `Burp Suite` ya que necesita el navegador escucha en el la misma direccion que `Burp Suite`, por lo que vamos a configurar el navegador.

Primero vemos donde esta `Burp Suite` escuchando:

<figure><img src="../../../../.gitbook/assets/image (51) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que esta en la `127.0.0.1:8080`, por lo que haremos lo siguiente:

Nos vamos al navegador a las opciones de arriba a la izquierda -> `Preferences` -> `Network Settings` -> seleccionamos la casilla de `Manual Proxy Configuration` -> donde pone `HTTP Proxy` (Donde va a estar este `proxy` corriendo) pondremos `127.0.0.1` y en el `Port` pondremos `8080` -> `Ok`.

Ahora todas las peticiones que realicemos van a pasar por ese `Proxy` (`Burp Suite`).

Ahora para que `Burp Suite` este en modo activado para interceptar cualquier peticion de `proxy` nos iremos a la pestaña `Proxy` -> le daremos al boton `Intercept is off` de la pestaña `Intercept`.

Tendria que estar algo tal que asi:

<figure><img src="../../../../.gitbook/assets/image (52) (1).png" alt=""><figcaption></figcaption></figure>

Si ahora probamos a pinchar en alguna pestaña, automaticamente `Burp Suite` lo intercepta y nos lo muestra por pantalla:

<figure><img src="../../../../.gitbook/assets/image (53) (1).png" alt=""><figcaption></figcaption></figure>

Ahora el navegador se va a quedar pensando ya que esta esperando la peticion que capturo la herramienta, por lo que si le damos a `Forward` lo que vamos hacer es enviar la peticion para que le llegue al servidor web y nos pueda responder.

Si nos vamos a las `opciones` dentro de `proxy` y bajamos un poco, veremos que la interceptacion de la peticion al `servidor` esta desactivada por defecto, cosa que vamos activar por que es recomendable.

<figure><img src="../../../../.gitbook/assets/image (54) (1).png" alt=""><figcaption></figcaption></figure>

Si ahora ponemos el `Burp Suite` a interceptar con el `On` y clicamos en alguna pagina veremos que la primera peticion es como la de antes, pero si le damos a `Forward` veremos que nos llega la peticion del servidor tambien:

<figure><img src="../../../../.gitbook/assets/image (55) (1).png" alt=""><figcaption></figcaption></figure>

Lo bueno de esta herramienta es que podemos cambiar a tiempo real la peticion injectando algun tipo de codigo o aprovechando alguna vulnerabilidad en el `head` de la pagina, pudiendo asi sacar informacion debil o una posible intrusion al servidor.
