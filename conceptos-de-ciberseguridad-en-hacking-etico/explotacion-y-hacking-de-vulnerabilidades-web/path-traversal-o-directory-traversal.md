# Path Traversal o Directory Traversal

La clave de esta vulnerabilidad es tratar de influir en la ruta para en lugar de obtener el fichero que se esta buscando tratar de obtener otros ficheros u otros archivos del sistema de ficheros del web server.

Si nos vamos en la pagina de `mutillidae` a un sitio cualquiera, ya que en si, en cualquier sitio va a ser vulnerable de esta pagina, podremos fijarnos en la URL como le esta pasando la pagina a la que queremos acceder mediante el parametro `page=`, por lo que con esto podemos aprovecharlo para hacer esta tecnica:

```
URL = http://<IP>/mutillidae/src/index.php?page=user-info.php
```

Si nos vamos a otra parte de la pagina, el `page=` va a cambiar de `.php` por lo que podemos ver que nos esta pillando directamente el archivo que queremos que nos muestre en pantalla, siendo asi una vulnerabilidad enorme.

Por ejemplo si queremos ver el `passwd` podremos hacerlo de la siguiente forma:

```
URL = http://<IP>/mutillidae/src/index.php?page=/etc/passwd
```

o

```
URL = http://<IP>/mutillidae/src/index.php?page=../../../../../etc/passwd
```

Con la segunda opcion lo que hago es que se vaya todos los directorios para atras hasta llegar al raiz `/` y de ahi le indico la ruta absoluta al fichero, por si acaso hubiera algun problema con el primero.

<figure><img src="../../.gitbook/assets/image (77).png" alt=""><figcaption></figcaption></figure>

Por lo que esto nos va a mostrar el `passwd`.

Para un sistema `windows` seria de la misma forma, pero con la barra invertida y llendonos al archivo que queramos.

```
URL = http://<IP>/mutillidae/src/index.php?page=..\..\..\..\..\archivo
```
