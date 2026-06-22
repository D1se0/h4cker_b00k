# Localizando JavaScript en una página

## La trinidad del frontend, en código fuente

Cualquier página web combina tres lenguajes: HTML (estructura), CSS (presentación) y JavaScript (comportamiento). Como vimos en el bloque de *Introducción a Aplicaciones Web*, todo este código llega completo al navegador del cliente — y, por tanto, está siempre disponible para su inspección.

## Paso 1: ver el código fuente HTML

`Ctrl+U` (o clic derecho → *Ver código fuente*) muestra el HTML tal como lo envió el servidor, sin que el navegador lo haya procesado todavía. Es el primer lugar donde buscar:

- **Comentarios** que el equipo de desarrollo pudo olvidar eliminar — a veces contienen directamente información sensible, como ya se vio en el bloque de *Introducción a Aplicaciones Web*.
- **Referencias a archivos externos**, tanto CSS como JavaScript.

## Paso 2: localizar el CSS

El CSS puede estar definido **internamente** (entre etiquetas `<style>` dentro del propio HTML) o **externamente** (en un archivo `.css` referenciado mediante `<link>`):

```html
<style>
    h1 { font-size: 144px; }
</style>
```

```html
<head>
    <link rel="stylesheet" href="style.css">
</head>
```

Aunque el CSS rara vez es el foco principal de un análisis de seguridad, conviene revisarlo brevemente: a veces revela pistas sobre clases o identificadores usados por funcionalidad oculta, o sobre frameworks empleados (relevante para el fingerprinting visto en *Information Gathering*).

## Paso 3: localizar el JavaScript

Mismo patrón que el CSS: **interno** (entre `<script>...</script>`) o **externo** (`<script src="archivo.js"></script>`).

```html
<script src="secret.js"></script>
```

Al visitar directamente la URL del archivo `.js` referenciado, puede aparecer algo así:

```js
eval(function (p, a, c, k, e, d) { e = function (c) { ... } ... }('5.4(\'3 2 1 0\');', 6, 6, '...'.split('|'), 0, {}))
```

Código completamente ilegible para un humano, aunque perfectamente funcional para el navegador — exactamente lo que se conoce como **código ofuscado**, el tema central de este bloque.

## Por qué empezar siempre por aquí

Antes de lanzarse a desofuscar nada, conviene tener claro el panorama completo: cuántos archivos JS hay, cuáles son internos y cuáles externos, y si alguno de ellos llama la atención por su tamaño, su nombre (`secret.js`, `admin.js`, `debug.js`) o por estar evidentemente ofuscado frente al resto. Este reconocimiento inicial, igual que en cualquier otra fase de auditoría web, orienta dónde invertir el esfuerzo de análisis a continuación.

## Conectando con DevTools

Más allá de `Ctrl+U`, las herramientas de desarrollo del navegador (vistas en detalle en el bloque de *Web Requests*) ofrecen un **depurador de JavaScript** propio, con capacidad de formatear automáticamente código minificado (función *Pretty Print*), poner puntos de interrupción, e inspeccionar variables en tiempo de ejecución — funcionalidad que se retoma en el apartado de desofuscación de este mismo bloque.
