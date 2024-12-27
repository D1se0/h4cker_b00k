# Utilizar transformador shodan en maltego

Por ejemplo si hemos identificado una direccion IP de dicha empresa o usuario, podremos añadir una entidad llamada `IPv4 Address` al espacio de trabajo.

Podremos añadirle una relacion a `persona` con el nombre de `mantiene el host` y dandole click en la entidad de `IPv4 Address`, podremos ver que en la lista de transformadores nos aparece el transformador llamado `shodan`.

![](<../../../.gitbook/assets/image (4) (1) (1) (1).png>)

Por lo que abriremos la interfaz y para ver si tiene vulnerabilidades esa IP, podremos irnos a la seccion de `Vulnerabilities Details` y seleccionamos la unica opcion que hay, esto lo que hara sera reportarnos si hay vulnerabilidades asociadas a dicha IP.

Esta informacion la podemos exportar con las opciones de `maltego` llendonos en la parte superior izquierda en el icono de `maltego` -> `Export` -> `Generate Report` y lo nombramos como queramos, con esto lo que hara sera generar un reporte respecto a la informacion que hemos ido descubriendo teniendolo todo perfectamente ordenado y detallado.
