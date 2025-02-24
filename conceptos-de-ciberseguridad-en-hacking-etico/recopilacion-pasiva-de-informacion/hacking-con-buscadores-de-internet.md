---
icon: landmark-magnifying-glass
---

# Hacking con buscadores de internet

Una de las primeras tecnicas que realizaria un analista sin tener ningun tipo de informacion de la empresa, seria el saber que puertos tiene expuestos, como funciona por dentro y todo este tipo de cosas, pero de forma `pasiva` por lo que dentro de nuestro `kali` podremos ejecutar la primera tecnica llamada `Hacking con buscadores` es informacion que nosotros llegamos a encontrar de internet respecto a la informacion que se ha indexado en paginas, foros, etc... Con buscadores realizando busquedas avanzadas de lo que se hace normalmente, mediante una serie de simbolos, caracteres, los cuales son como filtros para llegar a encontrar informacion especifica.

Si nosotros en el `kali` nos vamos a `web browser` en la barra de busqueda y buscamos el buscador mas utilizado llamado `google` podremos filtrar informacion de la siguiente forma:

Esto que vamos a ver en `google` se pueden ver los comandos que se pueden utilizar en lo conocido como `Google Dorks` que estara en el siguiente link:

URL = [Google Doks](https://www.boxpiper.com/posts/google-dork-list)

En el buscador si queremos buscar solo por un sitio en concreto utilizaremos el siguiente comando en el buscador:

```
site:<SITIO>.<EXTENSION> <BUSQUEDA>
```

> Ejemplo:

```
site:youtube.com hacking
```

Y solo encontrare resultados de la pagina de `youtube` sin que me aparezca otra pagina, reduciendo el rango de busqueda para que sea mas exacta.

Si queremos reducirlo todavia mas el espacio de busqueda, podemos forzar a `google` a que nos busque de forma concreta sitios como `youtube` y que solo sean formatos `pdf` por ejemplo:

```
site:youtube.com filetype:pdf
```

Tambien se puede filtrar por ficheros `.txt` que suelen ser menos comunes:

```
site:youtube.com filetype:txt
```

Muchas veces muchas organizaciones, exponen ficheros `.logs` en los cuales pueden ser muy utiles para sacar informacion, por lo que podremos hacer una busqueda de estos ficheros de la siguiente forma:

```
"index of" / "chat/logs"
```

Utilizamos `chat/logs` por que es la ruta mas tipica de donde se suelen alojar los `logs` de las empresas.

Y lo que estamos haciendo es que con las `""` estamos buscando esa palabra de forma exacta y con la `/` estamos haciendo es que muestre los 2 textos en la busqueda, por lo que con esto podremos ver algunos ficheros que `google` a indexado de forma publica de conversaciones de empresas las cuales no han cuidado su privacidad y se han dejado de forma publica.

Y esto lo podriamos combinar para buscar de una organizacion en concreto de la siguiente forma:

```
"index of" / "chat/logs" site:<DOMINIO>
```

Lo mas tipico que se suele buscar son `dumps` de bases de datos de las empresas (Volcados de datos) en las cuales puede tener informacion muy sensible, esto se puede hacer de la siguiente forma:

```
filetype:sql
```

O tambien se podria con:

```
ext:sql
```

Es exactamente lo mismo, se puede hacer de una forma u otra.

Para hacerlo de forma mas concreta lo haremos de la siguiente forma:

```
filetype:sql "MySQL dump"
```

Es una cadena de texto muy tipica de bases de datos de empresas por lo que se puede encontrar mucha informacion con eso, este comando lo que hara sera mostrar informacion de bases de datos de `mysql` hasta poder llegar a encontrar contraseñas, usuarios, correos de empleados, etc... Por lo que es muy importante saber buscar.

Si nosotros queremos buscar de forma mas exacta el que aparezca en las bases de datos ciertas palabras para filtrarlo, podremos hacerlo de la siguiente forma:

```
filetype:sql "MySQL dump" (pass|password|passwd|pwd)
```

Esto `|` es un operador logico `booleano` lo que estamos diciendo con esto es que encuentre indexado en las bases de datos que encuentre la palabra `pass` o `password` o `passwd` o `pwd`, etc... Y con esto podremos filtrar mucho mas la busqueda.

Y con esto se puede filtrar hacia una organizacion en concreto con `site`:

```
filetype:sql "MySQL dump" (pass|password|passwd|pwd) site:<DOMINIO>
```

Para filtrar y buscar con un parametro en concreto de URL teniendo lo que nosotros queremos se podria hacer de la siguiente forma, que es una de las cosas que mas se suele hacer para encontrar posteriormente vulnerabilidades como `SQL Injection`, etc...

```
inurl:index.php?id=
```

Y con esto lo que haces es encontrar paginas que tengan ese parametro en el que puede ser vulnerables a lo que mencione anteriormente como por ejemplo lo mas basico de `SQL Injection`.

```
?id=' OR 1=1-- -
```

Y si queremos centrarlo mas la busqueda seria poner el parametro `site`:

```
inurl:index.php?id= site:<DOMINIO>
```

Tambien se le puede poner busquedas mas genericas, como por ejemplo la siguiente busqueda:

```
site:gov filetype:pdf allintitle:restricted
```

Con esto lo que estamos haciendo es que nos muestre dominios con `site` que despues del `.` tengan `gov` o que contengan esto siendo de forma muy generica relacionado a gobiernos, el tipo de archivo en `pdf` y despues que contengan el titulo de `restricted`.

La pagina mas importante para saber todos estos comandos, seria la siguiente:

URL = [Google Hacking Database](https://www.exploit-db.com/google-hacking-database)
