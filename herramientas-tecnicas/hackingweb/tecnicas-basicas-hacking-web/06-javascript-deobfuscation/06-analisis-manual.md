# Análisis manual del código desofuscado

## El código ya es legible — ahora hay que entenderlo

Una vez desofuscado, el código se parece a JavaScript normal y corriente, pero eso no significa que su propósito sea evidente de inmediato. El siguiente paso es un análisis funcional, línea por línea, para entender exactamente qué hace.

```js
function generateSerial() {
  var flag = "HTB{...}";
  var xhr = new XMLHttpRequest;
  var url = "/serial.php";
  xhr.open("POST", url, true);
  xhr.send(null);
};
```

## Método de trabajo: leer variable por variable, función por función

### Identificar las variables y su tipo

`xhr` se inicializa como un objeto `XMLHttpRequest`. Si no se conoce esta API de memoria, una búsqueda rápida confirma que es el mecanismo estándar de JavaScript para realizar peticiones HTTP desde el navegador sin recargar la página (la base de las peticiones AJAX mencionadas en bloques anteriores).

`url` contiene `/serial.php` — al no especificar dominio, se asume relativo al mismo origen donde se sirve el script.

### Identificar las funciones invocadas y su efecto

`xhr.open("POST", url, true)`: abre una petición HTTP con método `POST` hacia la URL indicada, de forma asíncrona (`true`).

`xhr.send(null)`: envía la petición, sin cuerpo (`null`).

### Conclusión funcional

Toda la función `generateSerial()` se reduce a: **enviar una petición `POST` vacía a `/serial.php`**, sin parámetros y sin procesar ninguna respuesta visible en el propio script.

## Por qué esta función "no usada" es interesante

Si, tras revisar el HTML completo de la página, no aparece ningún botón ni elemento que invoque `generateSerial()`, es razonable sospechar que se trata de **funcionalidad no publicada todavía** — quizás en desarrollo, quizás simplemente abandonada — pero potencialmente **accesible igualmente**, ya que el endpoint `/serial.php` en el backend no tiene por qué saber (ni le importa) si el frontend la invoca o no.

Esto conecta directamente con uno de los principios más repetidos en este temario: **el frontend no protege nada por sí mismo**. Si el endpoint existe en el servidor, es accesible directamente, independientemente de si la interfaz visible lo expone o no.

## El siguiente paso lógico: replicar la petición manualmente

Una vez entendida la lógica, el paso natural es **reproducir esa misma petición directamente**, sin depender del navegador ni de que el JavaScript se ejecute — exactamente la misma filosofía vista repetidamente en el bloque de *Web Requests*: interactuar directamente con el backend ahorra tiempo y revela el comportamiento real, sin el filtro de la interfaz visual.

Esto se desarrolla en el siguiente apartado, donde se usa `curl` para replicar exactamente lo que el script ofuscado estaba haciendo, y observar qué responde realmente el servidor.

## Generalizando el método

Este proceso —desofuscar, identificar variables y funciones, buscar documentación de cualquier API desconocida, y concluir el propósito funcional— es aplicable a cualquier script, sea cual sea su complejidad. La clave está en no intentar entender todo de golpe: aislar cada pieza, entenderla individualmente, y solo después recomponer el panorama completo.
