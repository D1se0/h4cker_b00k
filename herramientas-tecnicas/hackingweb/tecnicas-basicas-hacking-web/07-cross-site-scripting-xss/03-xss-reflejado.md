# XSS Reflejado (Reflected)

## En qué se diferencia del almacenado

El XSS reflejado también pasa por el servidor backend, pero **no se guarda**: la entrada se procesa y se devuelve inmediatamente en la misma respuesta (un mensaje de error, un resultado de búsqueda, una confirmación), sin persistir en ninguna base de datos. Esto significa que, al salir de esa página concreta, el payload deja de existir — afecta únicamente a quien recibió esa respuesta específica, no a futuros visitantes.

## Ejemplo práctico

Sobre una aplicación similar a la del apartado anterior, al enviar un valor de prueba (`test`) en un campo que provoca un mensaje de error:

```
Task 'test' could not be added.
```

El mensaje de error **incluye literalmente** la entrada enviada. Si esa entrada no se sanitiza antes de incluirse en la respuesta, es candidata directa a XSS. Probando la misma carga útil que en el apartado anterior:

```html
<script>alert(window.origin)</script>
```

La alerta aparece, y el mensaje de error pasa a mostrar `Task '' could not be added.` — las comillas vacías son la pista de que el navegador interpretó (y ejecutó) la etiqueta `<script>` en lugar de mostrarla como texto literal. El código fuente confirma la inyección exacta:

```html
<div style="padding-left:25px">Task '<script>alert(window.origin)</script>' could not be added.</div>
```

## Confirmando que es no-persistente

Si se vuelve a visitar la página sin el payload, el mensaje de error desaparece y la alerta no se vuelve a disparar — confirmando que, efectivamente, es **no-persistente**: solo se activa para la petición concreta que contenía el payload.

## La pregunta clave: si no es persistente, ¿cómo se ataca a una víctima?

La respuesta depende del **método HTTP** usado para enviar la entrada vulnerable. Inspeccionando la petición en la pestaña *Network* de las DevTools del navegador (visto en detalle en el bloque de *Web Requests*):

- Si la petición es `GET`, los parámetros viajan **en la propia URL**.
- Esto significa que se puede construir una **URL maliciosa completa** que, al ser visitada por la víctima, dispare automáticamente el payload — sin que la víctima tenga que escribir nada en ningún formulario.

```
http://10.10.10.5/index.php?task=<script>alert(window.origin)</script>
```

Compartiendo esta URL con la víctima (por correo, mensaje, enlace acortado para ocultar el payload visible) y consiguiendo que la visite, el ataque se ejecuta exactamente igual que si la víctima hubiera introducido el payload manualmente.

## Por qué el XSS reflejado depende tanto de la ingeniería social

A diferencia del almacenado (que se ejecuta automáticamente para cualquier visitante normal de la página), el reflejado **requiere que la víctima interactúe específicamente con una URL o petición manipulada**. Esto reduce su alcance potencial, pero no elimina su peligrosidad: técnicas de phishing dirigido, enlaces acortados, o incluso incrustar la URL maliciosa como `src` de una imagen en otra página, son vías habituales para conseguir que la víctima dispare el payload sin saberlo.

## Conectando con el resto del bloque

Este es exactamente el patrón que se explota en el apartado de *Phishing*, más adelante en este mismo bloque: un XSS reflejado se convierte en el vehículo perfecto para entregar una URL maliciosa que, al visitarse, inyecta un formulario de login falso — sin necesidad de que el atacante consiga insertar nada de forma persistente en la aplicación.
