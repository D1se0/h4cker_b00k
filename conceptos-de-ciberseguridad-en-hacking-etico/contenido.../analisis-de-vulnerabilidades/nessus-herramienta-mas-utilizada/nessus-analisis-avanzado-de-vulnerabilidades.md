# Nessus (Análisis avanzado de vulnerabilidades)

Vamos a empezar por la opcion de `Advanced Scan`.

La diferencia de este tipo de escaneos es que tendremos que configurarlo todo nosotros de forma manual, en la pestaña de `Assessment` si es verdad que se añaden muchas mas cosas, pero donde realmente hay muchisima diferencia en este tipo de escaneos es en la pestaña de los `plugins`, proporcionandonos todos los `plugins` que son muchisimos, por lo que nosotros podremos seleccionar manualmente que `plugins` queremos utilizar activandolos o desactivandolos, dependiendo del escaneo que queramos realizar.

Pero en este caso no le daremos a `Save`, si no que nos iremos fuera a `Nessus` y en el panel izquierdo, en la seccion llamadas `Polices`(Politicas) pincharemos para meternos dentro.

Una vez dentro le daremos a `New Policy` y nos llevara a una interfaz igualita a cuando le damos a `New Scan`, pero con la diferencia de que estamos creando una politica respecto a un tipo de escaneo, para guardar dicha configuracion, por lo que le daremos a `Advanced Scan`.

Rellenaremos la informacion que queramos configurar en el escaneo.

<figure><img src="../../../../.gitbook/assets/image (38) (1).png" alt=""><figcaption></figcaption></figure>

En la seccion de `plugins` dejaremos todos los `plugins` activados para que haga un escaneo de vulnerabilidades completo, pero esto sera muy intrusivo a nivel de `red` generando mucho trafico.

<figure><img src="../../../../.gitbook/assets/image (39) (1).png" alt=""><figcaption></figcaption></figure>

Dejaremos todas las opciones por defecto para que saque la mayor informacion posible, en la seccion de `Settings` -> `Discovery` -> `Port Scanning` -> `Local Port Enumeration` -> Seleccionaremos la pestaña llamada `Verify open TCP ports found by local port enumerators` para que tenga mas detalles aun.

En la seccion de `Assessment` -> `Web Application` -> Seleccionamos la opcion llamada `Scan web applications`, para que asi tambien escanee aplicaciones web.

Y por ultimo en la parte de `Advanced` -> Deseleccionamos la casilla llamada `Enable safe checks` esta opcion lo que hace es que `Nessus` verifica que no se pase de intrusion por que puede llegar a romper la conexion con la maquina o que pueda tirar algun equipo por el escaneo tan intrusivo, pero como a nosotros nos da igual por que estamos en un entorno controlado, no pasa nada.

Por lo que le daremos a `Save` y lo que hara sera craer una politica con la configuracion que le hemos establecido.

<figure><img src="../../../../.gitbook/assets/image (40) (1).png" alt=""><figcaption></figcaption></figure>

Ahora si nos vamos a `New Scan` y seleccionamos la pestaña de arriba llamada `User Defined` podremos ver el archivo de politica que configuramos nosotros para que se nos cargue en el escaneo con el que lo configuramos.

<figure><img src="../../../../.gitbook/assets/image (41) (1).png" alt=""><figcaption></figcaption></figure>

Si le damos, veremos que se nos carga todo como lo configuramos, pero solo tendremos que seleccionar las `targets` a las cuales queremos realizar dicho escaneo:

<figure><img src="../../../../.gitbook/assets/image (42) (1).png" alt=""><figcaption></figcaption></figure>

Una vez establecido esto, solo le tendremos que dar a `Save` y ya estaria listo para ser iniciado cuando queramos.

Por lo que le daremos a `play` para que se inicie el escaneo.

Mientras el escaneo esta en funcionamiento, si nos vamos a `New Policy` y seleccionamos el `Advanced Dynamic Scan`, esto para lo que sirve es que en vez de ir uno por uno en la seccion de los `plugins` eligiendolos a mano en el `Escaneo avanzado` en este tipo de escaneo podremos filtrar por los puertos o por los `plugins` que realemente queramos utilizar siendo mas facil todo, tambien si se van añadiendo `plugins`, vulnerabilidades nuevas, etc... Con este escaneo se actualiza todo sin necesidad de tener que desactivar nada o de tener que revisarlo como en el `avanzado`.

Lo unico que diferencia al `Escaneo avanzado` es la seccion que se llama `Dynamic Plugins` donde podremos elegir el `CVE` que cargaran esos `plugins` en tiempo real sin necesidad de irlo cambiando.

Dejando esto de lado, si volvemos al escaneo que teniamos en ejecuccion, una vez que haya terminado, podremos exportar dichos resultados de una forma muy sencilla y que esteticamente se veria genial, ya que esto puede servir como informe de auditoria para una empresa realmente.

<figure><img src="../../../../.gitbook/assets/image (44) (1).png" alt=""><figcaption></figcaption></figure>

Para ello le podremos dar en la opcion de `Report` -> `HTML` -> `Generating Report` -> Y con esto ya se nos habria generado un reporte sobre las 2 maquinas con sus vulnerabilidades, con toda la informacion detallada de cada una de ellas, explicando absolutamente todo, esto puede servir para presentarlo en una organizacion a nivel real.

<figure><img src="../../../../.gitbook/assets/image (45) (1).png" alt=""><figcaption></figcaption></figure>
