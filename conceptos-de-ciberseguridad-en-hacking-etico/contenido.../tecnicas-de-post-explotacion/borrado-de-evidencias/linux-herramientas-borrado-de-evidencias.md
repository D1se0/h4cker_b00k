# Linux (Herramientas Borrado de evidencias)

En `linux` esta mas facil, por lo que enseñare 2 herramientas para `linux` que son muy utiles de cara hacer esta limpieza.

La primera se llama `shred` lo que hace es sobrescribir con otra informacion diferente esas direcciones de memoria en las cuales estan nuestra huella de atacante, pudiendo asi borrar lo anterior por si se recuperar el disco duro para hacer un reconocimiento de analisis forense.

Si por ejemplo nosotros hacemos el siguiente comando:

```shell
echo 'hola' > testfile.txt
```

Y despues borramos nuestro rastro con el siguiente comando utilizando la herramienta:

```shell
shred -vfz testfile.txt
```

Info:

```
shred: testfile.txt: pass 1/4 (random)...
shred: testfile.txt: pass 2/4 (random)...
shred: testfile.txt: pass 3/4 (random)...
shred: testfile.txt: pass 4/4 (000000)...
```

Aqui lo que vemos es que esta escribiendo datos random's en el fichero para no dejar `metadatos`, ni practicamente nada, por lo que si leemos el archivo veremos que esta vacio, ya que borro todo.

Y la otra herramienta es la llamada `srm` que lo que hace es borrar un fichero de manera segura y a parte realiza `38` escrituras sobre ese fichero y se utilizaria de la siguiente forma:

Primero crearemos otro archivo:

```shell
echo 'testfile' > testfile2.txt
```

Y ahora pondremos:

```shell
srm -v testfile2.txt
```

Info:

```
Using /dev/urandom for random input.
Wipe mode is secure (38 special passes)
Wiping testfile.txt 
pass:37[==================================================]100%
 Removed file testfile.txt ... Done
```

Una vez echo esto, ya no tendremos el archivo y habria realizado esas `38` escrituras sobre el archivo.
