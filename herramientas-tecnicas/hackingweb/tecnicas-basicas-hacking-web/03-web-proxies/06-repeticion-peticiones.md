# Repetición de peticiones (Repeater)

## El problema que resuelve

Si se quisiera probar manualmente diez payloads distintos contra un mismo parámetro repitiendo el ciclo completo de interceptar → modificar → reenviar → comprobar respuesta, cada iteración requeriría varios pasos — y con docenas o cientos de variantes a probar, el proceso se vuelve completamente inviable a mano.

La función de **repetición de peticiones** resuelve esto: toma cualquier petición ya capturada por el proxy (desde el historial), permite editarla libremente las veces que se quiera, y reenviarla con un solo clic, viendo la respuesta al instante sin tener que volver a interceptar nada.

## Historial del proxy

Antes de repetir una petición, hay que localizarla en el historial:

- **Burp**: `Proxy > HTTP History`
- **ZAP**: panel **History** (inferior) o pestaña **History** de la interfaz principal

Ambas herramientas permiten filtrar y ordenar el historial — esencial cuando se ha generado un volumen alto de tráfico y se busca una petición concreta. También mantienen un historial separado de conexiones **WebSocket**, relevante en aplicaciones que usan actualizaciones en tiempo real, aunque queda fuera del alcance básico de este bloque.

> **Diferencia útil**: Burp conserva tanto la petición **original** como la **editada** si se modificó algo antes de reenviarla, permitiendo comparar ambas versiones. ZAP solo muestra la versión final enviada.

## Enviando una petición a Repeater / Request Editor

### Burp

Clic derecho sobre la petición en el historial → **Send to Repeater** (o `Ctrl+R`), después navegar a la pestaña **Repeater** (`Ctrl+Shift+R`) y pulsar **Send**.

### ZAP

Clic derecho → **Open/Resend with Request Editor**, que abre una ventana editable con botón **Send**. El menú desplegable de método permite cambiar rápidamente entre `GET`/`POST`/etc. sin reescribir toda la petición.

También se puede repetir directamente desde el HUD: localizar la petición en el panel de historial inferior y elegir **Replay in Console** (respuesta dentro del propio HUD) o **Replay in Browser** (respuesta renderizada visualmente en el navegador).

## Flujo de trabajo típico de explotación manual

1. Capturar una petición base (por ejemplo, la que dispara una funcionalidad de `ping` que recibe una IP).
2. Enviarla a Repeater.
3. Modificar el parámetro de interés con un payload de prueba.
4. Pulsar **Send** y observar la respuesta.
5. Repetir el paso 3-4 ajustando el payload según el resultado — sin tener que volver a navegar la aplicación ni reinterceptar nada.

```
POST /ping HTTP/1.1
Host: 10.10.10.5
Content-Type: application/x-www-form-urlencoded
Content-Length: 11

ip=1;ls -la
```

Cambiando únicamente el valor de `ip` en sucesivos envíos desde Repeater —por ejemplo, de `ls -la` a `find / -name "*.txt"` o a cualquier otro comando de interés—, se puede iterar sobre una enumeración completa del sistema en cuestión de segundos, todo desde la misma ventana, sin reconstruir la petición desde cero cada vez.

## Por qué Repeater es la herramienta más usada en la práctica

A diferencia de Intruder/Fuzzer (orientados a probar automáticamente listas extensas de valores), Repeater está pensado para **iteración manual guiada por criterio**: el pentester observa cada respuesta, decide el siguiente payload en función de lo que ha visto, y ajusta sobre la marcha. Es la herramienta natural para confirmar y explotar manualmente una vulnerabilidad ya detectada, mientras que Intruder/Fuzzer son más adecuados para la fase de *descubrimiento* masivo.
