# Nessus (Análisis básico de vulnerabilidades)

Vamos a empezar por un escaneo simple de `hosts` para descubrir que `hosts`/`nodos` estan en el segmento de red activos.

Le daremos a `New Scan` y pulsaremos en `Host Discovery`, esto nos llevara a una interfaz configurable, en el que le configuraremos lo siguiente:

```
Name: HostDiscoveryTest
Description: Escaneo de prueba
Folder: My Scans
Targets: 192.168.16.0/24
```

<figure><img src="../../../../.gitbook/assets/image (34) (1).png" alt=""><figcaption></figcaption></figure>

En la seccion de `Schedule` se puede configurar para que haga un escaneo a una determinada hora, en un determinado horario, etc...

En la seccion de `Notifications` podremos intriducir un correo electronico para recivir las notificaciones de los escaneos que se vayan realizando.

Todo esto anteriror es solo en la pestaña `Basic` (Basica).

Si nos vamos a la pestaña de `Discovery` podremos seleccionar el tipo de escaneo que queremos que realice, como por ejemplo `Host enumeration, OS identification, Port Scan (Puertos comunes), Port Scan (Todos los puertos) y Custom (Para algo mas personalizado)`, esto lo dejaremos por defecto en `Host enumeration`.

En la pestaña de `Report` podremos seleccionar las casillas a guste de como queramos que se vea el reporte a nivel de informacion, en mi caso lo dejaremos por defecto.

En la pestaña de `Advanced` podremos modificar toda esta informacion para hacer un escaneo menos intrusivo, menos cargado, menos detectable o vicebersa, pero en mi caso lo dejare por defecto.

Le daremos a guardar con el boton `Save` y ya tendriamos el escaneo configurado.

Ahora para ejecutar el escaneo, tendremos que darle a boton de `Play` en la parte del escaneo que se representa como con una flecha (`>`).

<figure><img src="../../../../.gitbook/assets/image (35) (1).png" alt=""><figcaption></figcaption></figure>

Si pulsamos en el escaneo podremos ver que esta en ejeccion, por lo que tendremos que esperar, pero igualmente a tiempo real nos ira poniendo lo que va encontrando:

<figure><img src="../../../../.gitbook/assets/image (36) (1).png" alt=""><figcaption></figcaption></figure>

Y mientras esto va terminando, podremos probar hacer otro escaneo ya preconfigurados sobre vulnerabilidades famosas como por ejemplo la de el grupo de `hackers` llamados `Shadow Brockers`, si pinchamos en ese tipo de escaneo, configuraremos de forma normal el escaneo, por ejemplo poniendole en este caso a 2 maquinas objetivos:

```
Targets: 192.168.16.129,192.168.16.132
```

En la pestaña `Discovery` ya cambiaran las cosas entorno a como se hace este tipo de analisis de vulnerabilidad.

Todas las demas pestañas estaran modificadas al formato en el que se le haya dado este tipo de escaneo.

Pero si nos vamos a la parte de `Plugins` en nuestro escaneo de `Host Discovery` no habia nada en dicha parte, pero en este caso es un escaneo de vulnerabilidades a 2 `hosts` por lo que utilizara unos cuantos `plugins` para poder realizar estas acciones y en concreto utilizara unos determinados `plugins` dedicados a las vulnerabilidades que filtraron los `Shadow Brockers`.

Solo le tendriamos que dar a `Save` y ejecutarlo, llendonos al otro escaneo que realizamos principalmente de `hosts`, veremos que ha terminado y si pinchamos en el, veremos algo tal que asi:

<figure><img src="../../../../.gitbook/assets/image (37) (1).png" alt=""><figcaption></figcaption></figure>

Ha descubierto 5 `hosts` pero los que nos interesan son los que terminan en `129` y `132`.

No nos da mas informacion por que solo le pedimos que nos descubriera los `hosts` del segmento de red que le proporcionamos.

Si nos vamos a realizar mas escaneos (`Malware Scan`), podremos ver que podemos escanear maquinas proporcionandole unas credenciales para que nos diga si hay algun tipo de malware en el equipo o no.
