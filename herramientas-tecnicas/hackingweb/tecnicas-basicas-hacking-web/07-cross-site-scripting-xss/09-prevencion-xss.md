# Prevención de XSS

## El marco conceptual: Source y Sink, en ambos extremos

Como se ha visto repetidamente en este bloque, XSS gira en torno a dos puntos: el **Source** (donde entra la entrada del usuario) y el **Sink** (donde esa entrada se muestra o procesa). La prevención efectiva requiere actuar en **ambos extremos**, y en **ambas capas** de la aplicación (frontend y backend) — confiar en una sola capa es, sistemáticamente, insuficiente.

## Prevención en el frontend

### Validación de entrada

Comprobar que el dato introducido cumple el formato esperado, antes incluso de enviarlo:

```js
function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}
```

### Sanitización de entrada

Más allá de validar el formato, hay que **escapar o eliminar** caracteres peligrosos antes de procesar la entrada. La librería [DOMPurify](https://github.com/cure53/DOMPurify) es el estándar de facto para esto:

```html
<script src="dist/purify.min.js"></script>
<script>
  let clean = DOMPurify.sanitize(dirty);
</script>
```

### Evitar que la entrada del usuario llegue directamente a contextos peligrosos

Nunca insertar entrada de usuario sin sanitizar dentro de:

- Etiquetas `<script>...</script>`
- Bloques `<style>...</style>`
- Atributos de etiquetas HTML (`<div name='ENTRADA_USUARIO'>`)
- Comentarios HTML (`<!-- ENTRADA_USUARIO -->`)

Y evitar (o usar con extrema cautela, siempre acompañadas de sanitización) las funciones que escriben HTML/texto directamente en el DOM:

**JavaScript nativo:**
- `innerHTML` / `outerHTML`
- `document.write()` / `document.writeln()`
- `document.domain`

**jQuery:**
- `html()`, `parseHTML()`
- `add()`, `append()`, `prepend()`
- `after()`, `insertAfter()`, `before()`, `insertBefore()`
- `replaceAll()`, `replaceWith()`

Estas son exactamente las funciones "sink" identificadas en el apartado de XSS basado en DOM — su presencia en el código no es automáticamente un problema, pero exige verificar que todo lo que escriben ha pasado por una sanitización adecuada primero.

## Prevención en el backend

### Por qué el frontend nunca es suficiente

Como demostró el propio ejercicio de descubrimiento visto anteriormente: aunque un formulario tenga validación JavaScript en el frontend, esto **no impide** enviar una petición `POST`/`GET` manipulada directamente (vía `curl`, un proxy de intercepción, o cualquier herramienta que se salte la interfaz visual). La validación de frontend es, en el mejor de los casos, una mejora de experiencia de usuario — nunca un control de seguridad real, principio que se ha repetido constantemente a lo largo de este temario.

### Validación de entrada en servidor

```php
if (filter_var($_GET['email'], FILTER_VALIDATE_EMAIL)) {
    // procesar
} else {
    // rechazar — nunca mostrar la entrada rechazada
}
```

### Sanitización de entrada en servidor

PHP:

```php
addslashes($_GET['email']);
```

NodeJS (con la misma librería DOMPurify, también disponible en backend):

```js
import DOMPurify from 'dompurify';
var clean = DOMPurify.sanitize(dirty);
```

### Codificación de salida (Output Encoding)

Quizás la medida individual más importante: **codificar** los caracteres especiales antes de insertar cualquier entrada de usuario en HTML de respuesta, de forma que se muestren como texto literal en lugar de interpretarse como sintaxis HTML/JS.

PHP:

```php
htmlentities($_GET['email']);
// '<' se convierte en '&lt;', '>' en '&gt;', etc.
```

NodeJS:

```js
import encode from 'html-entities';
encode('<'); // -> '&lt;'
```

Esta técnica permite **mostrar** la entrada del usuario exactamente como la escribió (sin perder información ni rechazar la petición), pero garantizando que el navegador la interprete como texto inerte, no como código ejecutable.

## Configuración del servidor y cabeceras de seguridad

Retomando las cabeceras de seguridad vistas en el bloque de *Web Requests*:

| Medida | Efecto |
|---|---|
| HTTPS en todo el dominio | Evita interceptación/modificación del tráfico en tránsito |
| `Content-Security-Policy: script-src 'self'` | Solo permite ejecutar scripts alojados en el propio dominio, bloqueando scripts inyectados desde fuente externa |
| `X-Content-Type-Options: nosniff` | Evita que el navegador "adivine" un tipo de contenido distinto al declarado |
| Cookies con `HttpOnly` | JavaScript no puede leer la cookie vía `document.cookie` — mitiga directamente el robo de sesión visto en este bloque |
| Cookies con `Secure` | La cookie solo se transmite por HTTPS, nunca en claro |

Un **Web Application Firewall (WAF)** bien configurado añade una capa adicional, detectando y bloqueando automáticamente patrones de inyección en peticiones HTTP entrantes. Algunos frameworks (como ASP.NET) incluyen protección XSS integrada de fábrica.

## La filosofía final: defensa en profundidad

Ninguna medida aislada es infalible: la validación de entrada puede tener huecos, la sanitización puede tener bypasses conocidos, un WAF puede evadirse con técnicas de ofuscación. La estrategia robusta combina **todas** las capas simultáneamente — validación, sanitización, codificación de salida, cabeceras de seguridad, y revisión activa mediante pruebas ofensivas — de forma que el fallo de una sola capa no comprometa toda la aplicación.

Esto cierra el círculo de este bloque: entender XSS desde la perspectiva ofensiva (cómo se descubre y explota) es exactamente lo que permite implementar defensas efectivas desde la perspectiva defensiva — ambas disciplinas se alimentan mutuamente, y dominar una sin la otra deja, inevitablemente, puntos ciegos.
