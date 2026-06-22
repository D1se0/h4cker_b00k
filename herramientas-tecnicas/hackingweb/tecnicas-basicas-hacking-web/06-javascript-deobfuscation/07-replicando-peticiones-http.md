# Replicando peticiones HTTP descubiertas

## De la teoría a la comprobación práctica

Tras el análisis manual del apartado anterior, se sabe que el script intentaba enviar un `POST` vacío a `/serial.php`. El siguiente paso lógico es comprobar directamente, con `curl`, qué responde realmente ese endpoint — sin depender de que el JavaScript se ejecute en un navegador.

## Replicando con `curl`

```bash
curl -s http://10.10.10.5/ -X POST
```

`-X POST` fuerza el método. `-s` (silencioso) evita el ruido de las estadísticas de progreso de `curl`, dejando solo la respuesta limpia.

Si el endpoint espera además parámetros concretos, se añaden con `-d`:

```bash
curl -s http://10.10.10.5/serial.php -X POST -d "param1=valor"
```

## Por qué empezar sin datos y luego iterar

Es buena práctica probar primero la petición **más simple posible** (sin parámetros) y observar la respuesta, antes de empezar a añadir datos. Esto revela información valiosa por sí sola:

- Si el servidor responde con un error indicando qué parámetro falta, se ha aprendido algo sobre el contrato esperado del endpoint sin tener que adivinarlo del código.
- Si responde con éxito incluso sin datos, significa que la funcionalidad no requiere ningún parámetro adicional — como ocurría en el ejemplo de `generateSerial()`, que efectivamente enviaba `null` como cuerpo.

## Resultado típico: una respuesta inesperada

```bash
curl -X POST -i http://10.10.10.5/serial.php

HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8

N2gxNV8xNV9hX3MzY3IzN19tMzU1NGcz
```

El servidor responde con éxito (`200 OK`), pero el contenido no es texto legible directamente — tiene toda la apariencia de estar **codificado**, no simplemente devuelto en claro. Esto es exactamente el tipo de hallazgo que justificó toda la investigación: una funcionalidad backend, accesible directamente sin pasar por ninguna interfaz visible, que devuelve algo que requiere un paso adicional de decodificación para interpretarse.

## El patrón completo: del frontend ofuscado al backend real

Este recorrido —localizar JavaScript → desofuscarlo → entender su lógica → replicar la petición directamente con `curl`→ analizar la respuesta— es exactamente la metodología que conecta este bloque con el de *Web Requests*: el JavaScript ofuscado no era más que una capa de ocultación sobre una petición HTTP perfectamente normal y corriente, que termina pudiendo reproducirse y manipularse libremente una vez identificada.

El siguiente apartado completa el ejemplo: identificar y revertir el tipo de codificación de la respuesta obtenida, para llegar finalmente al contenido real que el servidor estaba devolviendo.
