---
icon: arrows-up-down-left-right
---

# Funciones de FOCA

Abriremos `FOCA` seguiremos los pasos que nos pida hasta llegar a uno en concreto en el que se tenga que conectar a una `base de datos` SQL, le especificaremos la siguiente ruta.

```
Server name: localhost
```

Le daremos a `Connect` y si todo ha ido bien, deberia de abrirnos la aplicacion para poder empezar a utilizarla.

Tendremos que ver algo tal que asi:

<figure><img src="../../../.gitbook/assets/image (9) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Antes nos descargaremos un fichero cualquiera por ejemplo `PDF` para sacarle los metadatos e ir probando esta herramienta, nos iremos a `google` y buscaremos algo como:

```
site:microsoft.com ext:pdf
```

Nos descargamos el primero o el que queramos al escritorio.

En `FOCA` nos vamos a `Document Analysis`, en la parte izquierda tendremos un espacio de trabajo en el que pincharemos click derecho y seleccionamos la opcion `Add File` -> Seleccionamos el fichero que nos descargamos y le daremos a `Abrir`.

Ahora le daremos dentro de `FOCA` click derecho en el archivo que se puso en nuestro espacio de trabajo, le daremos a la opcion `Extract Metadata`, esto lo que hara sera un proceso de extraccion de metadatos del archivo por lo que puede tardar un poco.

Una vez que los haya extraido lo veremos en la parte de la izquierda en la seccion `Metadata Summary`:

![](<../../../.gitbook/assets/image (7) (1) (1) (1).png>)

Aqui ya podremos ver la informacion que ha extraido e ir clicando uno por uno en los numeritos que no sean un `0` para ver que informacion a extraido, en mi caso no extrajo mucha informacion.

Pero para no ir uno por uno descargando estos archivos a mano y poniendolos en `FOCA`, este mismo software nos proporciona una opcion para automatizar todo esto.

Nos iremos a `Project` -> `New Project` -> Donde pone la seccion de `Domain Website` poner el dominio que nosotros queremos analizar (Ejemplo: microsoft.com) -> `Create` -> Nos pondra que el proyecto se creo correctamente y encima en la cabecera veremos que podemos buscar por todas esas extensiones:

<figure><img src="../../../.gitbook/assets/image (8) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Podremos seleccionar por ejemplo `Bing` para que busque por ese navegador utilizando las `querys` de `google dorks` y ya seleccionar los tipos de extensiones por la que queremos que busque, por ejemplo yo seleccionare `doc, ppt, xls, docx, pptx, xlsx y pdf`, le daremos a `Search All` para que busque todo eso seleccionado.

Ahora con los resultados encontrados, pulsaremos `Ctrl` y clicaremos en los documentos que queremos analizar los metadatos, una vez seleccionados todos aquellos documentos que queremos analizar damos click derecho y le damos a la opcion `Download`, esto nos descargara los archivos a nuestra maquina de forma local, una vez descargado todo filtraremos por los archivos descargados en la opcion de `Download`:

<figure><img src="../../../.gitbook/assets/image (10) (1).png" alt=""><figcaption></figcaption></figure>

Para que solo aparezcan los primeros los archivos descargados, por lo que clicaremos el primero y con el `Shift` mantenido clicaremos el ultimo descargado que seran lo que aparezcan con un punto en verde a la derecha, y veremos que se selecciona todo, le daremos click derecho y a la opcion `Extract Metadata`.

Y depende de que documento extraigamos los metadatos nos mostrara mas informacion o menos, descubriendo cosas interesante o no:

<figure><img src="../../../.gitbook/assets/image (11) (1).png" alt=""><figcaption></figcaption></figure>

En mi caso ya que descubrio mas cosas.

En `domains` tambien nos analiza los dominios que ha descubierto y con los metadatos en general se pueden saber muchas cosas, como mencione anteriormente sabiendo el sistema operativo y sabiendo que si el archivo es bastante actual utilizando un S.O. Se podrian aprovechar vulnerabilidades ya conocidas de dicho sistema, usuarios, correos, etc... Con esta herramienta se pueden hacer muchas cosas.
