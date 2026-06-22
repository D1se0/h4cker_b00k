# Validación del lado del cliente

## El primer obstáculo, y el más débil

Muchas aplicaciones implementan una primera capa de comprobación visible en el navegador: el formulario de carga rechaza visualmente un archivo cuya extensión no coincida con un patrón esperado (por ejemplo, solo `.jpg`, `.png`, `.pdf`), normalmente mediante JavaScript o atributos HTML como `accept`.

## Por qué esta capa nunca es una defensa real

Exactamente el mismo principio repetido en cada bloque de este temario: cualquier control que viva únicamente en el código que se ejecuta en el navegador del usuario puede ser **inspeccionado y evitado** por quien controla ese navegador. Las herramientas vistas en el bloque de *Web Proxies* —interceptar la petición con un proxy y modificarla antes de que salga hacia el servidor— permiten construir una petición de carga con cualquier nombre de archivo y contenido, independientemente de lo que el formulario visual permitiera seleccionar.

## La consecuencia práctica para una auditoría

Encontrar una validación de tipo de archivo que solo existe en el frontend no es, por sí mismo, el hallazgo final — es la señal de que hace falta comprobar **si el servidor repite esa misma validación de forma independiente**. Si no lo hace, el escenario se reduce exactamente al caso de "ausencia de validación" tratado en los apartados anteriores. Si el servidor sí implementa sus propios controles, entran en juego las distintas estrategias de validación de backend que se examinan en el resto de este bloque: listas negras, listas blancas, y verificación del tipo de contenido real.

## La lección de diseño que se repite

Cualquier control de seguridad debe asumirse "decorativo" hasta que se confirme que existe también, de forma independiente, en el servidor. Esto no es exclusivo de la carga de archivos: es el mismo principio aplicado en *Cross-Site Scripting* (validación de formato en frontend, fácilmente evitable enviando la petición directamente), y en *Command Injection* (un patrón de entrada aceptado visualmente que no impide construir la petición real a mano). La carga de archivos simplemente eleva la apuesta: aquí, lo que se "evita" no es una cadena de texto, sino el contenido binario completo de un archivo arbitrario.
