# Interceptación de peticiones

## El flujo básico

Una vez el navegador está enrutado a través del proxy, activar la interceptación permite **pausar cada petición** antes de que llegue al servidor, examinarla, modificarla a voluntad, y decidir si reenviarla, descartarla o repetirla.

### Burp

La pestaña `Proxy > Intercept` tiene la interceptación activada por defecto. El botón **Intercept is on/off** controla el estado. Con la interceptación activa, cualquier navegación genera una petición pausada esperando acción manual — clic en **Forward** para reenviarla.

### ZAP

La interceptación está **desactivada** por defecto (indicado por un icono verde en la barra superior). Se activa con el mismo icono o el atajo `Ctrl+B`. Una vez activa, las peticiones quedan pausadas en el panel correspondiente, con un botón de **step** para avanzarlas una a una.

ZAP además ofrece el **HUD (Heads Up Display)**: un panel superpuesto directamente sobre el navegador preconfigurado que permite controlar las funciones principales de ZAP sin cambiar de ventana — interceptar, ver historial, codificar/decodificar, todo desde la propia pestaña del navegador.

## Por qué interceptar (y no solo observar)

Interceptar una petición y modificarla antes de enviarla es la base de prácticamente cualquier técnica de explotación manual: permite comprobar en tiempo real cómo reacciona el backend ante una entrada distinta a la que el frontend "permite" enviar de forma natural. Casos de uso típicos:

- Pruebas de **inyección SQL**: añadir comillas o lógica SQL en un parámetro.
- Pruebas de **inyección de comandos**: añadir operadores de shell (`;`, `|`, `&&`) a un campo que se sospecha se usa para construir un comando del sistema.
- **Bypass de carga de archivos**: modificar el `Content-Type` o el nombre de archivo declarado.
- **Bypass de autenticación**: alterar cookies, tokens, o parámetros que determinan el rol del usuario.
- Pruebas de **XSS**, **XXE**, manejo de errores, deserialización, y prácticamente cualquier otra clase de vulnerabilidad que dependa de cómo procesa el servidor una entrada concreta.

## Ejemplo ilustrativo: saltarse una validación del frontend

Imaginemos un formulario con un campo numérico (`<input type="number">`) que el navegador impide rellenar con texto, restringiendo así, aparentemente, qué se puede enviar. Sin embargo, esa restricción es puramente del lado del cliente (como vimos en el bloque de *Introducción a Aplicaciones Web*): basta con interceptar la petición ya generada y editar manualmente el valor del parámetro antes de reenviarla, sin que el navegador tenga oportunidad de "bloquear" nada — la restricción del `<input>` solo afecta a cómo se escribe en el formulario, no a lo que viaja en la petición HTTP final.

```
POST /ping HTTP/1.1
Host: 10.10.10.5
Content-Type: application/x-www-form-urlencoded
Content-Length: 4

ip=1
```

Si el backend tampoco valida que `ip` contenga únicamente un valor numérico, se puede sustituir por una cadena que rompa la lógica esperada — por ejemplo, encadenando un comando adicional si ese valor se usa para construir un comando de sistema (`ping`) sin sanitización:

```
ip=;ls;
```

Si la respuesta cambia de la salida habitual de `ping` a un listado de archivos, se ha confirmado una **inyección de comandos** explotable — exactamente el tipo de hallazgo que la interceptación de peticiones hace posible verificar en segundos.

## Buena práctica: desactivar la interceptación cuando no se necesita

Trabajar con la interceptación siempre activa ralentiza la navegación, ya que cada petición —incluidas las de recursos estáticos (CSS, JS, imágenes) que rara vez interesan— queda pausada esperando una acción manual. Lo habitual es navegar con la interceptación desactivada mientras se explora la aplicación, y activarla puntualmente justo antes de disparar la acción concreta que se quiere interceptar y modificar.
