---
icon: bee
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

# Análisis de vulnerabilidades - OWASP ZAP Proxy

Una vez que tengamos toda la informacion con las anteriores herramientas, podremos utilizar un `framework` bastante util para encontrar vulnerabilidades web denominado `zaproxy`, no viene por defecto en `kali` por lo que tendremos que instalarla.

URL = [Zaproxy GitHub](https://github.com/zaproxy/zaproxy)

```shell
sudo apt install zaproxy
```

Con esto ya estaria instalado y a pesar de que se utiliza para realizar un analisis de vulnerabilidades web, tambien es utilizado como un `proxy` de interceptacion como `BurpSuite`.

Tendremos que buscarla en la barra de busqueda de `kali` la herramienta ya que es con entorno grafico, esto nos abrira una aplicacion en la que podremos tratar con ella de la siguiente forma:

<figure><img src="../../../.gitbook/assets/image (185).png" alt=""><figcaption></figcaption></figure>

Vamos a probar a realizar un `Automated Scanner`, por lo que pincharemos en el, veremos un apartado en el que tendremos que meter la `URL`, meteremos lo siguiente:

```
192.168.5.211:8080
```

Y le daremos al boton de `Attack`.

Lo que primero va a realizar es el proceso de `Spidering`, despues de terminal con el. realizara el proceso de `Active Scan` que este tardara un poco mas y cuando finalice nos creara un mapa de las vulnerabilidades que ha podido ser capaz de encontrar.

Mientras se termina si nos vamos en la parte de `Alets` veremos las diferentes alertas que se van encontrando del proceso de `Active Scan` y clasificadas por peligrosidad de las cuales tiene la pagina web:

<figure><img src="../../../.gitbook/assets/image (186).png" alt=""><figcaption></figcaption></figure>

Para poder ver hasta donde ha llegado el proceso de `Spidering` tendremos que desplegar la pestaña de `Sites`:

<figure><img src="../../../.gitbook/assets/image (187).png" alt=""><figcaption></figcaption></figure>

Nosotros por cada sitios que le demos o cada `Alert` que pulsemos, veremos el codigo fuente asociado a el en la parte superior derecha.

Ahora si nos volvemos atras dandole a `Quick Start` -> y al simbolo `<`, veremos de nuevo los tipos de escaneo, por lo que seleccionaremos el llamado `Manual Explore`.

Lo interesante de esto es que viene con un `HUD` que es un set de herramientas que nos permitira interactuar con la aplicacion web a la vez que se realiza este escaneo o analisis de seguridad.

Metemos la `URL` la cual queremos escanear y le daremos a `Launch Browser`.

Esto lo que hara sera abrir el navegador para que podamos interactuar con el mientras se va realizando el escaneo, veremos algo asi:

<figure><img src="../../../.gitbook/assets/image (188).png" alt=""><figcaption></figcaption></figure>

Las herramientas que tendremos seran las que estan en la parte de los laterales:

<figure><img src="../../../.gitbook/assets/image (189).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image (190).png" alt=""><figcaption></figcaption></figure>

Si le damos a las alertas que tenemos en las partes laterales alguna veremos algo asi:

<figure><img src="../../../.gitbook/assets/image (191).png" alt=""><figcaption></figcaption></figure>

Vemos que nos muestra informacion y podemos seleccionar la alerta para ver mas informacion sobre ello, pudiendo saber que tipo de vulnerabilidad esta teniendo.

Nos iremos a un apartado que sepamos que tiene un `SQL Injection` de la siguiente forma en el `panel`.

<figure><img src="../../../.gitbook/assets/image (192).png" alt=""><figcaption></figcaption></figure>

Le daremos a `hack` y veremos la pagina donde tiene la vulnerabilidad. automaticamente cuando entremos realizara un escaneo tambien de dicha pagina, pudiendo ver en las herramientas lo que va encontrando.

Pero si enviamos algo en el apartado que nos proporciona como por ejemplo la palabra `test`, veremos que no nos encuentra nada ya que este analisis lo esta haciendo de forma `pasiva` y no esta insertando ningun `payload` ni nada por el estilo, solamente esta analizando y probando las cabeceras de las peticiones que se van realizando por si encintrara alguna vulenrabilidad, pero si queremos que realice un escaneo de forma activa probando diferentes `payloads` tendremos que activar la siguiente opcion:

<figure><img src="../../../.gitbook/assets/image (193).png" alt=""><figcaption></figcaption></figure>

Nos aparecera una ventana y le daremos a `Start`, mientras eso funciona si nos venimos a este boton de aqui:

<figure><img src="../../../.gitbook/assets/image (194).png" alt=""><figcaption></figcaption></figure>

Esto lo que hace es poder sacar o meter del `Scop` de la pagina que estamos actualmente del analisis, es decir, que ahora mismo le vemos activo, por lo que esta dentro del analisis que esta realizando, pero si le queremos omitir la pagina actual o no queremos que haga ningun tipo de analisis en la pagina actual le tendremos que sacar del `Scop` osea apagar ese boton y no realizara nada en la pagina actual.

En el boton `Sites` si le pulsamos podremos ver todo el `arbol` que ha escaneado de `URLs` y podremos analizarlas una a una de forma manual por si alguna nos interesara.

En este boton:

<figure><img src="../../../.gitbook/assets/image (195).png" alt=""><figcaption></figcaption></figure>

Lo que hace es realizar `Spidering` sobre `HTML` en el cual empieza a investigar la `URL` desde donde estas buscando nuevos directorios o recursos que encuentre importantes, pero desde el punto donde estas, ahora que si queremos realizar `Spidering` sobre `JavaScript` tendremos que pulsar el siguiente boton:

<figure><img src="../../../.gitbook/assets/image (196).png" alt=""><figcaption></figcaption></figure>

Este boton de aqui:

<figure><img src="../../../.gitbook/assets/image (197).png" alt=""><figcaption></figcaption></figure>

Lo que realiza es un escaneo de todos los enlaces que vamos recorriendo de forma activa, por defecto esta en `off`, pero si le damos a `On` realizara lo que estoy comentando, aunque bajo mi opinion es mucho mejor el boton del `fueguito`.

Si nosotros le damos a este boton `Comments`:

<figure><img src="../../../.gitbook/assets/image (198).png" alt=""><figcaption></figcaption></figure>

Veremos que nos muestra los comentarios superpuestos a la pagina web de la siguiente forma:

<figure><img src="../../../.gitbook/assets/image (199).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image (200).png" alt=""><figcaption></figcaption></figure>

Pues si nosotros nos ponemos con el cursor encima de un comentario podremos ver lo que contiene, esto son comentarios a nivel de codigo fuente de `HTML`.

Ahora volviendo al proceso de `Scaneo Activo` una vez que haya terminado, si nos vamos a las alertas de la derecha, veremos lo siguiente:

<figure><img src="../../../.gitbook/assets/image (201).png" alt=""><figcaption></figcaption></figure>

Veremos que nos ha encontrado un `SQL Injection`, y nos explica como realizarlo si pulsamos en el y como lo ha echo.

Si pulsamos sobre el `payload` que ha utilizado y bajamos un poco podremos ver que podremos replicarlo para verlo nosotros mismo en el boton `Replay in Browser`.

<figure><img src="../../../.gitbook/assets/image (202).png" alt=""><figcaption></figcaption></figure>

Este boton de aqui:

<figure><img src="../../../.gitbook/assets/image (203).png" alt=""><figcaption></figcaption></figure>

Lo que hace es que si lo activamos se pone a la escucha de cualquier peticion que le enviemos al servidor mediante la pagina web pudiendo capturarla como hace `BurpSuite` y asi poder modificarla a tiempo real:

<figure><img src="../../../.gitbook/assets/image (204).png" alt=""><figcaption></figcaption></figure>

Vemos que si enviamos algo con eso activo, nos captura la peticion con toda su informacion.
