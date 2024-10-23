# KeyCroc (Hack5) Función

Este dispositivo basicamente lo que hace es registrar las pulsaciones de un teclado en el que conectaremos el teclado al puerto USB del dispositivo y con el otro puerto USB al equipo para que haga de intermediario, a parte de tener herramientas de pentesting, etc... Pero para ponerlo en `Modo armamento` y poder convertirlo en una `Unidad Flash` de forma temporal con la que podamos trabajar para programarle cualquier cosa tendremos con un alfiler o un pin introducirlo en un mini agujerito del dispositivo y con esto ya estaria de forma temporal en `Modo armamento`.

## Función del KeyCroc

Su funcion basica que viene por defecto sin programar nada, es la de un `KeyLogger`, por lo que si lo conectamos como dije anteriormente y el usuario teclea lo que sea, esto se quedara almacenado en el dispositivo y despues poniendolo en `Modo armamento` podremos extraer dicha informacion de el.

Y si entramos en ese modo, podremos ver varios archivos, pero entre ellos nos interesa la carpeta llamada `loot` en el que se habra creado un archivo algo parecido como `croc_char.log` (Esto en tal caso de que ya lo hayamos conectado para capturar las pulsaciones de teclas) y si entramos dentro veremos todas las pulsaciones de teclas que se han estado tecleando.

### Para capturar de forma mas profesional con KeyCroc

En la realidad si se capturara todo lo que una persona escribe en horas, podria ser caotico la de informacion que podria haber capturado, pero podremos hacer lo siguiente para capturar de una forma mas profesional.

Nos iremos a la carpeta `library`, dentro de ella nos vamos a `examples` y dentro abriremos el archivo llamado `example_crocctl-ipinfo.txt`, copiaremos las lineas en las que pone lo siguiente:

```txt
MATCH __crocctl-ipinfo
QUACK ENTER
```

Ahora con eso copiado nos vamos a la carpeta llamada `payloads` y creamos un archivo llamado `payload.txt`, dentro pegaremos esas 2 lineas y añadiremos una cosa mas, tiene que quedar algo tal que asi:

```txt
MATCH pwned
QUACK STRING texto de prueba
```

Esto lo que hace es que cuando detecte el dispositivo que hemos escrito la palabra `pwned` en el teclado Victima, se va automaticamente a escribir la palabra `texto de prueba` en el equipo Victima.

Por lo que en vez de escribir palabras se podria utilizar para que cuando detecte cierta palabra se cargue alguna carga util o algun comando en especifico. (Esto se repite las veces en la que el usuario ponga la palabra)

## Control remoto de teclado con KeyCroc

Lo que se podria hacer es que cuando se conecte el dispositivo hacer que este mismo se conecte a la vez a un `punto de acceso` (Red Wifi) la cual se podria estar gestionando con otro dispositivo externo como un movil (Parte del atacante) para esto se le tiene que indicar cual es el nombre de la `Wifi` y la contraseña de la misma, todo esto en los archivos de configuracion para que funcione.

La idea es que por `DHCP` se le va asignar una IP al `KeyCroc`, pero no podremos saber cual es, por lo que configuraremos una palabra clave al dispositivo para que cuando sea introducida vuelque en algun archivo de texto cual es la IP.

Una vez que ya sepamos cual es la IP habiendo echo todo lo anterior, nos conectaremos desde el movil al `KeyCroc` para especificar cuales son las teclas que queremos que se presionen de forma remota.

### Configuración de KeyCroc (Teclado remoto)

Estando el dispositivo en `Modo armamento` nos iremos a la carpeta llamada `library`, dentro de ella nos iremos a `examples` y de ahi nos copiaremos el archivo llamado `example_crocctl-ipinfo.txt`, una vez copiado, lo pegaremos en la carpeta de `payloads` y borraremos el anterior `payload.txt` que creamos.

Abriremos el archivo `example_crocctl-ipinfo.txt` para configurarlo, dentro del mismo cambiaremos la linea llamada `MATCH __crocctl-ipinfo` por `MATCH vermiip` para que cuando metamos esa palabra se ejecute lo demas que sera basicamente para ver la IP del dispositivo.

Ahora para que este dispositivo se pueda conectar a un `punto de acceso`, tendremos que editar un archivo llamado `config.txt` y dentro del mismo cambiaremos lo siguiente donde pone `WIFI_SSID` poner el nombre de tu wifi a la derecha de esta palabra `WIFI_SSID <NAME_WIFI>` y donde pone `WIFI_PASS` la contraseña del wifi a la derecha de esa palabra `WIFI_PASS <PASSWORD_WIFI>` y debajo de `WIFI_PASS` habria que añadir la siguiente linea llamada `SSH ENABLE`

Una vez hecho todos estos cambios, ya lo podremos desconectar y conectar en el equipo victima.

Para ver la IP que tiene el `KeyCroc` pondremos la palabra clave, que en mi caso es `vermiip` y esto nos mostrara la IP del dispositivo, por lo que teniendo esto nos iremos al movil.

En el movil donde tengamos el `punto de acceso` que se puede hacer con la aplicacion llamada `Termius - SSH and SFTP client` le daremos al `+` y seleccionaremos la opcion llamada `New Host`, en el apartado `Hostname` pondremos la direccion IP del `KeyCroc`, mas abajo pondremos las credenciales del SSH que son las siguientes que te vienen por defecto.

```
USERNAME = root
PASSWORD = HACK5CROC
```

Le daremos a `Save` y le daremos al host que hemos creado, si le damos se nos habrira una ventana de terminal con una consola interactiva del `KeyCroc` en este punto podremos mandar comandos al dispositivo para que este los reciva y los ejecute pudiendo tomar el control del teclado mediante comandos.

Por ejemplo, si esta en un bloq de notas y metemos en el movil el siguiente comando:

```shell
QUACK STRING Esto es una prueba
```

Automaticamente se escribira en el bloq de notas y con esto podremos hacer muchisimas cosas mas.
