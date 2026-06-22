# XSS basado en DOM

## La diferencia fundamental: nunca llega al servidor

A diferencia del reflejado, el **XSS basado en DOM** se procesa **completamente en el navegador**, mediante JavaScript, sin que la entrada del usuario llegue nunca al servidor backend. Esto tiene una consecuencia inmediata y observable: si se inspecciona la pestaña *Network* de las DevTools mientras se interactúa con el campo vulnerable, **no se genera ninguna petición HTTP** — toda la "magia" ocurre localmente en el navegador.

## Reconociendo la señal: el fragmento (#)

Un indicio característico es el uso del carácter `#` (fragmento) en la URL para pasar el parámetro:

```
http://10.10.10.5/index.php#task=test
```

Como se vio en el bloque de *Web Requests*, el fragmento de una URL **nunca se envía al servidor** — lo procesa exclusivamente el navegador. Esto es una pista directa de que la entrada se está manejando del lado del cliente.

## Por qué no aparece en el código fuente estático

Si se revisa el código fuente con `Ctrl+U`, la entrada del usuario **no aparece por ningún lado**. Esto se debe a que el HTML que el servidor envía inicialmente no contiene esa entrada — es JavaScript, ejecutándose **después** de que el navegador ya cargó la página, quien la inserta dinámicamente. Para ver el DOM actualizado (que sí refleja los cambios dinámicos), hace falta usar el **Inspector** del navegador (`Ctrl+Shift+C`), que muestra el árbol DOM *en su estado actual*, no el HTML original servido por el servidor.

## El concepto clave: Source y Sink

Para entender (y encontrar) XSS basado en DOM, hay que identificar dos elementos en el código JavaScript:

| Concepto | Definición |
|---|---|
| **Source** | El objeto JavaScript que recibe la entrada del usuario — un parámetro de URL, un campo de formulario, cualquier dato controlable por el atacante. |
| **Sink** | La función que escribe esa entrada en el DOM de la página. Si el sink no sanitiza adecuadamente lo que recibe, es vulnerable. |

### Funciones sink habituales en JavaScript puro

- `document.write()`
- `DOM.innerHTML`
- `DOM.outerHTML`

### Funciones sink habituales en jQuery

- `add()`
- `after()`
- `append()`

Cualquiera de estas funciones, si escribe la entrada del usuario **tal cual**, sin sanitización, abre la puerta a XSS basado en DOM.

## Ejemplo de revisión de código

```js
// Source: lee el parámetro "task" directamente de la URL
var pos = document.URL.indexOf("task=");
var task = document.URL.substring(pos + 5, document.URL.length);

// Sink: escribe esa entrada sin sanitizar, directamente en el DOM
document.getElementById("todo").innerHTML = "<b>Next Task:</b> " + decodeURIComponent(task);
```

El **source** es el parámetro `task` de la URL; el **sink** es `innerHTML`, que inserta directamente esa cadena en el DOM sin escapar ningún carácter especial. Esta combinación confirma la vulnerabilidad sin necesidad de probar nada todavía — la simple lectura del código ya lo demuestra.

## Por qué `<script>` puede no funcionar (y qué usar en su lugar)

Muchas funciones sink, como `innerHTML`, **no ejecutan** etiquetas `<script>` insertadas dinámicamente — es una protección incorporada en la especificación del DOM, no un filtro explícito de la aplicación. Esto significa que el payload clásico `<script>alert(...)</script>` puede fallar silenciosamente incluso en una página genuinamente vulnerable.

La solución: usar vectores de inyección que **no dependan** de la etiqueta `<script>`:

```html
<img src="" onerror=alert(window.origin)>
```

Esta etiqueta crea un elemento de imagen con una fuente vacía (que provocará un error de carga), disparando el atributo `onerror`, que sí se ejecuta normalmente incluso cuando se inserta vía `innerHTML`.

```html
<img src=x onerror="alert(document.cookie)">
```

La misma técnica, aplicada para confirmar acceso a la cookie de sesión — el mismo patrón de prueba mínima visto en los apartados anteriores.

## Atacando con XSS basado en DOM

Al ser no-persistente y procesarse enteramente en el cliente, el ataque requiere —igual que el reflejado— que la víctima visite una **URL específica** que contenga el payload en el fragmento o parámetro correspondiente. Compartir esa URL es, de nuevo, el vector de entrega.

## Por qué el DOM XSS es especialmente interesante para Blind XSS

Como se verá en el apartado de *Session Hijacking* de este bloque, el XSS basado en DOM tiene una tasa de éxito particularmente alta en escenarios de **Blind XSS**, precisamente porque, al tratarse de código del lado del cliente, suele ser posible **revisar el código fuente JavaScript directamente** (a diferencia de la lógica de backend, oculta por definición) y construir un payload muy preciso basado en el análisis exacto del source y el sink involucrados.
