# Fuzzing integrado: Burp Intruder y ZAP Fuzzer

## Qué es el fuzzing y por qué un proxy lo incorpora

*Fuzzing* consiste en enviar automáticamente un gran volumen de valores predefinidos (una lista de palabras, una secuencia numérica, permutaciones) contra un punto concreto de una petición, observando las respuestas para identificar comportamientos interesantes: un código `200` donde se esperaban `404`s, un tiempo de respuesta anómalo, una diferencia de tamaño en la respuesta. Es la técnica base para descubrir directorios ocultos, fuerza bruta de credenciales, o identificar qué valores de un parámetro provocan un comportamiento distinto al normal.

Tanto Burp como ZAP integran su propio motor de fuzzing, evitando salir a una herramienta externa (`ffuf`, `gobuster`, `wfuzz`) cuando ya se está trabajando dentro del proxy con una petición concreta capturada.

## Burp Intruder

Para enviar una petición a Intruder: localizarla en el historial → clic derecho → **Send to Intruder** (`Ctrl+I`), y luego ir a la pestaña Intruder (`Ctrl+Shift+I`).

### 1. Positions (posiciones de carga útil)

Se marca, dentro de la petición, el punto exacto donde se insertará cada valor de la lista, envolviéndolo con el marcador `§...§` (o seleccionando el texto y pulsando **Add §**).

```
GET /§DIRECTORY§ HTTP/1.1
Host: 10.10.10.5
```

### 2. Payloads (carga útil)

- **Payload set**: a qué posición marcada corresponde cada lista de valores (relevante cuando hay varias posiciones, según el tipo de ataque elegido — `Sniper`, `Cluster Bomb`, etc.).
- **Payload type**: el formato de la lista. `Simple list` es la opción básica (se proporciona una lista de palabras y se itera línea por línea); `Runtime file` hace lo mismo pero cargando el archivo línea a línea durante la ejecución, evitando cargar todo en memoria de golpe — preferible para listas muy grandes.
- **Payload configuration**: aquí se carga el archivo de wordlist (por ejemplo, una lista de directorios comunes) o se añaden valores manualmente.
- **Payload processing**: reglas adicionales aplicadas a cada elemento antes de enviarlo — por ejemplo, añadir un sufijo (`.html`) a cada palabra, o saltar líneas que coincidan con un patrón de expresión regular (`Skip if matches regex`).
- **Payload encoding**: si se codifica automáticamente en URL cada valor antes de insertarlo.

### 3. Settings: filtrando resultados relevantes

La opción **Grep - Match** permite marcar automáticamente qué respuestas contienen una cadena de interés (por ejemplo, `200 OK`), añadiendo una columna en los resultados que facilita identificar de un vistazo qué peticiones tuvieron éxito sin tener que revisar respuesta por respuesta. **Grep - Extract** permite, además, extraer y mostrar solo un fragmento concreto de cada respuesta, útil cuando las respuestas son extensas y solo interesa un dato puntual dentro de ellas.

### 4. Lanzando el ataque

**Start Attack** inicia el proceso. Los resultados se pueden ordenar por columnas como `Status`, `Length`, o la columna de coincidencia Grep configurada, para localizar rápidamente respuestas anómalas entre cientos o miles de intentos.

> **Limitación de la versión Community**: el Intruder gratuito limita la velocidad a 1 petición/segundo, lo que lo hace impráctico para listas de palabras grandes. Para esos casos, conviene recurrir a herramientas de fuzzing de línea de comandos (`ffuf`, `gobuster`) o a ZAP Fuzzer, que no tiene esa limitación.

## ZAP Fuzzer

Conceptualmente equivalente a Intruder, con su propio flujo:

1. Localizar la petición en el historial → clic derecho → **Attack > Fuzz**.
2. **Fuzz Location**: seleccionar el texto a sustituir y pulsar **Add** (equivalente a las posiciones de Burp).
3. **Payloads**: ZAP ofrece varios tipos, incluyendo listas de archivo propias (`File`) y, de forma destacada, **listas de palabras integradas** (`File Fuzzers`) que vienen incluidas con la herramienta sin necesidad de aportar wordlists externas — una ventaja práctica frente a Burp Community.
4. **Processors**: transformaciones a aplicar a cada valor antes de enviarlo — codificación/decodificación Base64 o URL, hash MD5/SHA-1/256/512, añadir prefijo o sufijo, o incluso un script personalizado.
5. **Options**: número de hilos concurrentes (`Concurrent Scanning Threads per Scan`), ajustable para acelerar el escaneo sin las limitaciones de velocidad de Burp Community.

### Ejemplo práctico: fuerza bruta de una cookie basada en hash

Imaginemos que una aplicación establece una cookie de sesión calculando el hash MD5 del nombre de usuario actual (`Cookie: cookie=084e0343a0486ff05530df6c705c8bb4`, correspondiente al MD5 de `guest`). Si se sospecha que la aplicación confía en ese valor para identificar al usuario sin más verificación, se puede usar ZAP Fuzzer para:

1. Marcar el valor de la cookie como posición de fuzzing.
2. Cargar una wordlist de nombres de usuario comunes como payload.
3. Añadir un **processor de hash MD5**, de forma que cada nombre de usuario de la lista se transforme automáticamente en su hash antes de insertarse en la cookie.
4. Lanzar el ataque y comparar las respuestas — por ejemplo, por tiempo de respuesta (RTT) o tamaño, ya que una cookie correspondiente a un usuario "real" probablemente genere una respuesta distinta (más contenido, una sección adicional) frente a usuarios que no existen.

Este patrón —**fuzzing con transformación automática del payload**— es extremadamente útil cuando la aplicación no acepta el valor "en crudo" sino una versión derivada (hasheada, codificada, firmada parcialmente), ya que evita tener que generar manualmente cada variante antes de probarla.

## Cuándo usar el fuzzer del proxy vs. una herramienta dedicada

| Escenario | Mejor opción |
|---|---|
| Fuzzing rápido sobre una petición ya capturada, con pocas iteraciones | Intruder/ZAP Fuzzer (todo integrado, sin cambiar de herramienta) |
| Wordlists muy grandes, necesidad de máxima velocidad | `ffuf`/`gobuster` (línea de comandos), o ZAP Fuzzer si no se dispone de Burp Pro |
| Necesidad de transformar el payload sobre la marcha (hash, codificación) antes de insertarlo | ZAP Fuzzer (Processors) o Burp Intruder Pro (Payload Processing avanzado) |
| Fuzzing combinado con múltiples posiciones simultáneas | Burp Intruder con tipo de ataque `Cluster Bomb` o `Pitchfork` |
