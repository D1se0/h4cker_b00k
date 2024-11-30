# Pagina Shodan

Este buscador es muy util para cuando estamos haciendo una auditoria para la recoleccion pasiva de informacion, ya que especificando a que organizacion/empresa queremos que busque, nos proporcionara informacion de puertos activos, informacion de banners, etc... de dicha empresa, por lo que podremos reolectar informacion de dichos puertos para luego posteriormente ver si tienen algun tipo de vulnerabilidad.

URL [Pagina Shodan](https://www.shodan.io)

Para buscar este tipo de informacion en este buscador nos tendremos que registrar e iniciar sesion, al igual que `google` este buscador tambien utiliza comandos porpios para filtrar las busquedas.

Y en vez de buscar las empresas directamente, aqui buscariamos por puertos, etc... Por ejemplo si queremos ver cosas relacionadas con los puertos `ftp` pondriamos en el buscador `ftp` y nos mostrara resultados de paginas que tienen estos puertos.

Y nos lo devuelve con IP's de ciertas maquinas en las cuales esta corriendo dicho puerto.

Si entramos en una de las IP's nos mostrara ya no solo la informacion del puerto y el banner que aparece, si no tambien otras vulnerabilidades que tenga junto a mas puertos en los que tenga corriendo en esa maquina, tambien intenta hacer login de forma automatica anonima por si se pudiera o para encontrar mas vulnerabilidades.

Podremos buscar de forma mas exacta con la siguiente busqueda:

```
ftp anonymous
```

Y si lo queremos de un pais en concreto, podremos pinchar el que queramos a la izquierda o buscarlo de la siguiente forma:

```
ftp anonymous country:"US"
```

Y esto solo nos buscara maquinas con el puerto `ftp` en el que aparezca en el banner la palabra `anonymous` en `Estados Unidos`.

Pero si queremos filtrarlo todavia mas, para saber seguros que se puede hacer login de forma anonima, podremos hacerlo de la siguiente forma:

```
ftp anonymous login ok
```

Y con esto nos encontrara que se puede iniciar sesion de forma anonima al puerto `ftp`.

Y si queremos filtrar por puertos de forma mas especifica, lo podremos hacer pinchando a la izquierda en la seccion de `ports` o poniendo en la barra de busqueda:

```
ftp anonymous country:"ES" port:"21"
```

Que el puerto `21` se asocia al del `ftp`.

Y este buscador no te encuentra paginas web, te encuentra sistema como tal que al hacer una peticion a un puerto determinado en el que hay un servicio corriendo nos devuelve esa informacion y en esa informacion aparecen las palabras que nosotros buscamos.

Si queremos buscar de una organizacion en particular, se podra hacer de con `org:` y la organizacion.

Por ejemplo se podria hacer de la siguiente forma:

```
ftp org:"Google"
```

En la siguiente URL sera un `GitHub` el cual estaran subidas consultas ya echas las cuales nos pueden venir muy bien a la hora de querer saber informacion de forma mas especifica:

URL = [GitHub Querys Shodan](https://github.com/jakejarvis/awesome-shodan-queries)
