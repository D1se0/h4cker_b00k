# XSS Almacenado (Stored)

## Por qué es el tipo más crítico

El XSS almacenado (también llamado *persistente*) ocurre cuando el payload inyectado se guarda en la base de datos del servidor y se sirve a **cualquier usuario** que posteriormente visite la página afectada. Esto lo distingue radicalmente de los otros dos tipos: no hace falta atraer a una víctima a una URL especialmente manipulada — basta con que visite normalmente una página de la aplicación (un comentario, una publicación, un ticket de soporte) que ya contiene el payload guardado.

Esta característica explica por qué se considera el tipo de XSS más grave: el público potencialmente afectado es **todo el que use la aplicación**, no un único objetivo escogido. Además, puede ser complicado de remediar por completo, ya que requiere localizar y eliminar el payload directamente de la base de datos, no solo "arreglar" el formulario que lo originó.

## Ejemplo práctico: descubriendo XSS almacenado

Sobre una aplicación sencilla tipo lista de tareas (*To-Do List*) donde se puede añadir texto libre:

```html
<script>alert(window.origin)</script>
```

Esta es la carga útil de prueba por excelencia. Se elige `alert(window.origin)` en lugar de, por ejemplo, `alert(1)`, por una razón concreta: muchas aplicaciones modernas usan iframes de distinto origen para gestionar formularios. Si la alerta muestra la URL del origen donde realmente se ejecuta, se puede confirmar inequívocamente **qué formulario concreto** es el vulnerable, incluso en presencia de iframes anidados.

Si la aplicación es vulnerable, aparece una ventana de alerta inmediatamente al enviar el formulario (o al recargar la página). Revisando el código fuente se confirma la inyección:

```html
<div></div><ul class="list-unstyled" id="todo">
  <script>alert(window.origin)</script>
</ul>
```

## Confirmando la persistencia

El paso decisivo para confirmar que es **almacenado** (y no reflejado): **recargar la página**. Si la alerta vuelve a aparecer tras la recarga, el payload sigue ahí, guardado en el servidor — confirmando XSS almacenado. Y, crucialmente, **cualquier otro usuario** que visite esa misma página activará el mismo payload, sin que el atacante tenga que hacer nada adicional.

## Payloads alternativos cuando `alert()` está bloqueado

Algunos navegadores modernos pueden restringir `alert()` en ciertos contextos. Alternativas igualmente fáciles de detectar visualmente:

```html
<plaintext>
```

Detiene el renderizado de cualquier HTML posterior, mostrándolo como texto plano — un efecto visual muy evidente.

```html
<script>print()</script>
```

Abre el diálogo de impresión del navegador, una acción que rara vez está bloqueada por configuraciones de seguridad del navegador.

## El siguiente paso natural: robar la cookie

Una vez confirmado que el `alert(window.origin)` funciona, sustituirlo por `alert(document.cookie)` confirma —de forma igualmente visible e inofensiva— que el script tiene acceso de lectura a las cookies del documento. Esto es la prueba de concepto mínima para el ataque de **secuestro de sesión** que se trata en detalle más adelante en este bloque: si se puede leer la cookie con `alert()`, se puede igualmente **exfiltrarla** hacia un servidor controlado por el atacante en lugar de simplemente mostrarla.

```html
<script>alert(document.cookie)</script>
```

## Por qué el XSS almacenado es el "objetivo soñado" en una auditoría

Encontrar un punto de inyección XSS almacenada accesible para usuarios de bajo privilegio, pero **visible para un administrador** (por ejemplo, un campo de "nombre de usuario" que aparece en un panel de gestión de usuarios), es uno de los hallazgos más valiosos en pentesting: convierte una vulnerabilidad aparentemente "solo del lado del cliente" en una vía directa hacia el secuestro de la sesión de un administrador — y, por extensión, hacia un compromiso mucho más amplio de la aplicación.
