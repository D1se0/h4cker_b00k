# Cross-Site Scripting (XSS) — primera toma de contacto

> Este apartado es una introducción conceptual. El bloque dedicado *Cross-Site Scripting (XSS)* desarrolla la técnica en mucha mayor profundidad: tipos, vectores, explotación avanzada y mitigaciones.

## De la inyección HTML a la inyección de JavaScript

Cuando una aplicación refleja entrada de usuario sin sanitizarla, lo primero que suele probarse es una **inyección HTML**: insertar etiquetas propias (`<b>`, `<h1>`, formularios falsos) que se renderizan tal cual en la página. Es una prueba de concepto sencilla que confirma la ausencia de filtrado.

El siguiente paso natural es preguntarse: si puedo inyectar HTML arbitrario, ¿puedo inyectar también **JavaScript**? Si la respuesta es sí, estamos ante **Cross-Site Scripting (XSS)** — la vulnerabilidad que permite ejecutar código JavaScript arbitrario en el navegador de otro usuario, en el contexto de la aplicación legítima.

## Los tres tipos fundamentales de XSS

| Tipo | Cuándo ocurre |
|---|---|
| **Reflejado (Reflected)** | La entrada del usuario se devuelve inmediatamente en la respuesta (por ejemplo, un mensaje de error que repite el término buscado), sin pasar por almacenamiento persistente. |
| **Almacenado (Stored)** | La entrada se guarda en el servidor (base de datos) y se muestra posteriormente a cualquier usuario que visite esa página — por ejemplo, un comentario o publicación maliciosa. |
| **Basado en DOM (DOM-based)** | La entrada del usuario se procesa directamente en el navegador y se inserta en el DOM vía JavaScript, sin que el servidor llegue a intervenir en ese tramo concreto. |

## Ejemplo práctico: robo de cookie de sesión

Si una aplicación refleja un parámetro sin sanitizar el contenido dentro de un atributo HTML, un payload típico de prueba sería:

```html
"><img src=/ onerror=alert(document.cookie)>
```

Cómo funciona, paso a paso:

1. `">` cierra cualquier atributo y etiqueta HTML abierta previamente, "escapando" del contexto original donde se inyecta el texto.
2. `<img src=/ onerror=alert(...)>` crea una etiqueta de imagen con una fuente inválida deliberadamente (`/`), lo que dispara el evento `onerror`.
3. `onerror=alert(document.cookie)` ejecuta JavaScript que muestra en una ventana emergente el valor actual de `document.cookie` — es decir, las cookies accesibles desde JavaScript en esa página.

Si esto funciona, significa que cualquier código JavaScript arbitrario puede ejecutarse en el navegador de quien visite/interactúe con esa entrada maliciosa — no solo `alert()`, sino cualquier lógica: exfiltrar la cookie a un servidor controlado por el atacante, redirigir al usuario, modificar el contenido de la página, etc.

## Por qué importa especialmente el robo de cookies

Como vimos en el bloque de *Web Requests*, una cookie de sesión válida es, en muchas aplicaciones, **suficiente por sí sola** para autenticarse — no se necesita conocer usuario ni contraseña. Si un atacante consigue ejecutar JavaScript en el navegador de la víctima y exfiltrar `document.cookie`, puede copiar esa cookie en su propio navegador y suplantar completamente a la víctima (técnica conocida como **session hijacking**), sin que la víctima llegue a notar nada extraño más allá, quizás, de un comportamiento momentáneo en la página.

Esto es exactamente lo que motiva el atributo `HttpOnly` en las cookies (visto en el bloque de cabeceras HTTP): cuando una cookie se marca como `HttpOnly`, JavaScript no puede leerla mediante `document.cookie`, lo que mitiga (aunque no elimina por completo) el riesgo de robo de sesión vía XSS.

## Por qué XSS sigue siendo tan común

La causa raíz casi siempre es la misma: **ausencia o insuficiencia de saneamiento de entrada y/o salida**. Si una aplicación refleja exactamente lo que el usuario envió, sin codificar caracteres especiales (`<`, `>`, `"`, `'`) antes de insertarlos en el HTML de respuesta, cualquier entrada que contenga sintaxis HTML/JS válida se interpretará literalmente en el navegador de quien la reciba.

Profundizaremos en los tres tipos de XSS, técnicas de descubrimiento, payloads avanzados, casos de uso ofensivos (desfiguración, phishing, session hijacking) y todas las medidas de prevención en el bloque dedicado *Cross-Site Scripting (XSS)*.
