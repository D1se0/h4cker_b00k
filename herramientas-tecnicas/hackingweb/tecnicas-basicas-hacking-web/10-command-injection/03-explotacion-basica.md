# Explotación básica: inyectando el primer comando

## Construyendo la carga útil

Retomando el ejemplo del comprobador de host del apartado anterior: si la entrada `127.0.0.1` produce el comando interno `ping -c 1 127.0.0.1`, añadir un punto y coma seguido de un segundo comando debería ejecutar ambos secuencialmente:

```
127.0.0.1; whoami
```

```bash
ping -c 1 127.0.0.1; whoami
```

Si la entrada no se valida ni se escapa antes de pasar a la función de ejecución, el resultado combina la salida del `ping` original con la del comando inyectado — confirmando la vulnerabilidad.

## Cuando la validación parece bloquear el intento

Es habitual encontrar que, al introducir el payload directamente en un campo de formulario, la aplicación lo rechaza con un mensaje de error genérico (por ejemplo, indicando que el formato no es válido). Esto **no significa necesariamente** que la vulnerabilidad no exista — puede tratarse de una validación implementada únicamente en el **frontend**.

### Confirmando que la validación es solo de frontend

Abriendo las DevTools del navegador (pestaña *Network*, vista en detalle en el bloque de *Web Requests*) y repitiendo el intento: si **no se genera ninguna petición HTTP** al hacer clic en el botón de envío, la validación está ocurriendo enteramente en JavaScript del lado del cliente, antes de que la petición llegue siquiera a salir hacia el servidor.

Esto conecta directamente con uno de los principios repetidos a lo largo de todo este temario: **el frontend no protege nada por sí mismo**. Una validación únicamente en JavaScript (por ejemplo, un atributo `pattern` en un campo `<input>` que solo acepta formato de IP) es una mejora de experiencia de usuario, no una barrera de seguridad real — porque nada impide construir y enviar la petición HTTP directamente, sin pasar por esa interfaz.

## Saltándose la validación de frontend

El método más directo: usar un proxy de intercepción (Burp Suite o ZAP, vistos en detalle en el bloque de *Web Proxies*) para capturar la petición legítima generada con una entrada válida, y modificarla manualmente antes de reenviarla.

1. Activar la interceptación de peticiones.
2. Enviar el formulario con una entrada válida (`127.0.0.1`) para capturar la estructura exacta de la petición.
3. Enviar la petición capturada a Repeater.
4. Sustituir el valor del parámetro por el payload de inyección (`127.0.0.1; whoami`).
5. Codificar correctamente en URL si es necesario (los operadores de shell contienen caracteres especiales que deben transmitirse sin alterar su significado).
6. Reenviar y observar la respuesta.

Si la respuesta ahora contiene tanto la salida del comando original como la del comando inyectado, la inyección se ha confirmado y explotado con éxito — el frontend rechazaba la entrada, pero el backend, al recibir la petición directamente, la procesó sin ninguna validación adicional.

## La lección de fondo

Este patrón —validación robusta en apariencia en el frontend, ausente por completo en el backend— es extremadamente común en aplicaciones reales, normalmente no por mala fe sino por la separación de responsabilidades entre equipos de frontend y backend, o por una confianza injustificada en que la validación del cliente sería suficiente. Por eso, ante cualquier mecanismo de validación, la pregunta de un auditor siempre debe ser: **¿se aplica también del lado del servidor, o solo decora la interfaz?** — algo que únicamente se puede confirmar interactuando directamente con el backend, sin pasar por la interfaz visual.
