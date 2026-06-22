# Interceptación de respuestas

## Por qué interceptar también la respuesta, no solo la petición

Hasta ahora hemos visto cómo modificar lo que **enviamos**. Pero a veces la restricción que queremos saltarnos no está en lo que enviamos, sino en cómo el **frontend renderiza** la página recibida: campos deshabilitados, valores ocultos, validaciones de formato (`type="number"`, `maxlength`) que limitan lo que el usuario puede escribir desde la interfaz.

Interceptar la respuesta del servidor **antes** de que llegue al navegador permite editar ese HTML sobre la marcha, eliminando esas restricciones del lado del cliente para poder interactuar con el formulario sin las limitaciones impuestas originalmente.

## Habilitando la interceptación de respuesta

### Burp

`Proxy > Proxy settings > Response interception rules` → activar **Intercept Response**. A partir de aquí, con la interceptación de petición también activa, tras reenviar la petición se mostrará la respuesta correspondiente, editable antes de continuar hacia el navegador.

### ZAP

Al interceptar una petición, el botón **Step** envía la petición y automáticamente intercepta también la respuesta asociada, presentándola para edición antes de que llegue al navegador.

## Ejemplo: habilitar un campo restringido

Supongamos un campo definido como:

```html
<input type="number" id="ip" name="ip" min="1" max="255" maxlength="3" required>
```

El atributo `type="number"` impide al usuario teclear directamente caracteres no numéricos, y `maxlength="3"` limita la longitud. Si se intercepta la respuesta que contiene este HTML y se modifica a:

```html
<input type="text" id="ip" name="ip" min="1" max="255" maxlength="100" required>
```

Al reenviar la respuesta modificada, el navegador renderiza el campo como texto libre y sin límite de 3 caracteres, permitiendo escribir directamente el payload deseado desde la propia interfaz, sin tener que interceptar y editar manualmente la petición cada vez.

## Limitación: los cambios no persisten

Una modificación realizada interceptando manualmente una única respuesta es temporal: si se recarga la página, el HTML original (con las restricciones intactas) vuelve a cargarse, y habría que repetir el proceso de interceptar y editar de nuevo. Esto se resuelve con **reglas de modificación automática**, que aplican el cambio a cada respuesta que coincida con un patrón, sin intervención manual — lo veremos en el siguiente apartado.

## Funciones adicionales en ZAP HUD

El HUD de ZAP ofrece atajos para tareas comunes sin necesidad de interceptar manualmente cada respuesta:

- **Show/Enable**: habilita automáticamente campos deshabilitados o muestra campos ocultos en la página actual, sin tener que editar el HTML a mano.
- **Comments**: marca visualmente en la página las posiciones donde existen comentarios HTML, mostrando su contenido al pasar el ratón — útil para localizar rápidamente comentarios de desarrollador olvidados (relevante para lo visto en el apartado de exposición de datos sensibles).

Burp ofrece una funcionalidad equivalente en `Proxy > Proxy settings > Response modification rules`, con opciones como **Unhide hidden form fields**, que automatizan exactamente este tipo de ajuste sin necesidad de interceptar manualmente cada respuesta.
