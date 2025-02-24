---
icon: face-viewfinder
---

# Recon-ng Herramienta

Esta herramienta se utiliza para automatizar mucho mas esa bsuqueda de informacion publica para encontrar informacion sensible o que nos sea util.

URL = [GitHub Recon-ng](https://github.com/lanmaster53/recon-ng)

Para abrir la herramienta no hara falta descargarnos nada, ya que viene por defecto en `kali linux` por lo que solamente buscaremos en el busca `recon-ng` y cuando la ejecutemos se nos abrira la terminal, ya que es una herramienta pura de terminal, estando asi en su entorno de la herramienta.

Inicialmente en la herramienta no vamos a tener ningun modulo instalado, por lo que empezaremos a instalar algunos modulos de la siguiente forma:

```shell
marketplace search
```

Con esto nos mostrara todos los modulos disponibles que hay en la herramienta.

Si queremos filtrar por algun modulo que nos interese mas como por ejemplo paginas como `shodan`, herramientas, etc... Lo podremos hacer de la siguiente forma:

```shell
marketplace search whois
```

Y esto nos mostrara los modulos que estan relacionados con las BBDD `whois`.

Si queremos saber que hace un modulo, para obtener esta informacion podremos hacerlo de la siguiente forma:

```shell
marketplace info recon/domains-contacts/whois_pocs
```

Y esto nos mostrara informacion de ese modulo en concreto, utilizaremos ese modulo ya que busca informacion privada de la gente en la que este registrada bajo el dominio que pongamos.

```shell
marketplace install recon/domains-contacts/whois_pocs
```

Con esto instalaremos dicho modulo, si vemos cuales son los modulos que tenemos instalados de la siguiente forma.

```shell
modules search
```

Podremos ver que esta instalado correctamente para ser usado.

Para cargar el modulo lo haremos de la siguiente forma:

```shell
modules load recon/domains-contacts/whois_pocs
```

Para ver como utilizar la herramienta pondremos:

```shell
options list
```

O

```shell
info
```

Por lo que ahora vamos a configurar la herramienta poniendo...

```shell
options set SOURCE <DOMAIN>
```

> Ejemplo:

```shell
options set SOURCE microsoft.com
```

Ahora para ejecutar la herramienta con el valor ya establecido, solamente tendremos que poner:

```shell
run
```

Y esto ejecutara la herramienta dandonos informacion de lo que ha encontrado pero no la mostrara, para ver la informacion encontrada tendremos que poner:

```shell
show contacts
```

Y esto si nos mostrara toda la informacion sensible que haya enconctrado.

Para salirnos del modulo ejecutaremos `back` y con esto estaremos en la herramienta principal.

Ahora instalaremos `shodan`.

```shell
marketplace search shodan
```

```shell
marketplace install recon/companies-multi/shodan_org
```

En algunos modulos como en este nos avisara de que hara falta una `API Key` de `shodan`, nos avisara por que no tenemos establecido ninguna `API Key` de `shodan`, por lo que estableceremos la `API Key` de la siguiente forma.

```shell
keys add shodan_api <API KEY>
```

Lo unico seria cambiar `<API KEY>` por la `API` real llendonos a la pagina -> nuestra cuenta -> Show API Key, copiariamos la `API` y la pegariamos en la terminal despues de `shodan_api`.

Y con esto ya habriamos añadido la `API Key` a `shodan`.

Ahora cargaremos el modulo:

```shell
modules load recon/companies-multi/shodan_org
```

Miraremos las opciones:

```shell
options list
```

Ahora le estableceremos un valor:

```shell
options set SOURCE google.com
```

Una vez establecido el valor, le daremos a `run`, por lo que empezara a buscar los `hosts` del dominio, si se alarga mucho la busqueda o queremos pararla con los `hosts` que haya encontrado, simplemente haremos `Ctrl+C`, se parara y se quedara con los resultados ya encontrados.

Para ver los resultados pondremos:

```shell
show hosts
```

Y con esto veremos todos los `hosts` que nos ha detectado del dominio establecido.

Si nos salimos del modulo con `back` y listamos los modulos de `marketplace`:

```shell
marketplace search
```

En la parte final veremos unos modulos interesantes con las extensiones de `csv, xml, html, json, list, proxifier, pushpin y xlsx`, esto nos sirve para exportar los resultados encontrados con la herramienta `recon-ng` al tipo de formato deseado.

Si por ejemplo queremos exportarlo en `HTML` instalaremos dicho modulo:

```shell
marketplace install reporting/html
```

Cargamos el modulo:

```shell
modules load reporting/html
```

Y para ver lo que se necesita de dicho modulo:

```shell
options list
```

Ahora vamos a configurar el modulo:

```shell
options set CREATOR d1se0
options set CUSTOMER orgX
options set FILENAME /home/d1se0/Desktop/results.html
```

Le daremos a `run` y con esto se nos habra creado el `.html` con los resultados obtendios de los diferentes modulos.
