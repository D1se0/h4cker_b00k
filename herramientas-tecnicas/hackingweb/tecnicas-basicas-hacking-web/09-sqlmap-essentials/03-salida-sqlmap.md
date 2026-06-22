# Entendiendo la salida de SQLMap

## Por qué merece la pena leer los logs, no solo el resultado final

Cada línea que SQLMap imprime durante su ejecución documenta una decisión concreta del motor de detección. Entender estos mensajes permite diagnosticar por qué algo no funciona, confirmar que el objetivo se está probando de la forma esperada, y en muchos casos aprender lo suficiente como para continuar manualmente si la automatización se queda corta.

## Mensajes más habituales, explicados

### "El contenido de la URL de destino es estable"

Confirma que peticiones idénticas consecutivas devuelven respuestas equivalentes — condición necesaria para poder atribuir cualquier diferencia observada después a los payloads de prueba, y no a "ruido" aleatorio de la propia aplicación.

### "El parámetro GET 'id' parece ser dinámico"

Cambiar el valor del parámetro **sí** altera la respuesta — señal de que está conectado a alguna lógica de backend (probablemente una consulta a base de datos), y por tanto vale la pena seguir probándolo.

### "Prueba heurística (básica) muestra que el parámetro podría ser inyectable (posible DBMS: MySQL)"

Una sonda rápida con un valor intencionalmente malformado (`?id=1",)..).))'`) provocó un error reconocible de MySQL. **Esto no es una confirmación de SQLi** — solo indica que merece la pena profundizar con el motor de detección completo en la siguiente fase.

### "El sistema de gestión de bases de datos backend es 'MySQL'. ¿Desea omitir las pruebas para otros DBMS?"

Si ya hay indicios claros del motor concreto, SQLMap puede limitar las pruebas exclusivamente a la sintaxis de ese motor, ahorrando tiempo considerable frente a probar payloads de los más de 30 motores soportados.

### "Valores reflectivos encontrados y filtrados"

Advertencia de que fragmentos del propio payload aparecen reflejados en la respuesta — esto podría confundir a una comparación ingenua entre respuestas, pero SQLMap aplica filtrado interno para descartar ese "ruido" antes de comparar.

### "El parámetro parece ser inyectable... (con --string='luther')"

SQLMap ha identificado una cadena constante (`luther`) que aparece consistentemente en respuestas `TRUE` y desaparece en `FALSE` — un ancla muy fiable para distinguir ambos casos sin depender de comparaciones difusas más propensas a falsos positivos.

### "La comparación basada en tiempo requiere un modelo estadístico más amplio, espere..."

Para inyección **time-based**, SQLMap necesita primero recopilar una muestra de tiempos de respuesta "normales" (sin retraso) antes de poder distinguir estadísticamente un retraso intencional de la latencia natural de la red — especialmente importante en redes con latencia variable, donde una sola medición no sería fiable.

### "Técnica 'ORDER BY' parece utilizable. Ampliando rango de pruebas UNION..."

Antes de probar fuerza bruta con `UNION SELECT`, SQLMap comprueba si `ORDER BY` funciona para determinar el número de columnas mucho más rápido (mediante búsqueda binaria) — exactamente la técnica vista manualmente en el bloque anterior, ahora automatizada.

### "El parámetro es vulnerable. ¿Desea seguir probando los demás?"

Confirmación positiva. Por defecto, SQLMap se detiene en el primer parámetro vulnerable encontrado — útil responder afirmativamente si se está auditando exhaustivamente una aplicación con múltiples parámetros potencialmente afectados, en lugar de conformarse con el primer hallazgo.

### "sqlmap identificó los siguientes puntos de inyección con un total de N peticiones HTTP"

El resumen final, con tipo, título y payload exacto de cada técnica confirmada — la prueba definitiva y reproducible del hallazgo.

## Registro persistente de los datos extraídos

SQLMap guarda automáticamente toda la información recopilada (sesión, datos enumerados, archivos descargados) en un directorio de salida estructurado, organizado por dominio objetivo — permitiendo retomar una sesión interrumpida sin tener que repetir la fase de detección desde cero, y manteniendo un registro auditable de todo lo extraído durante la prueba.

## La lección de fondo

Aprender a "leer" SQLMap en lugar de tratarlo como una caja negra es lo que permite, ante una ejecución que no encuentra nada, distinguir entre "el objetivo realmente no es vulnerable" y "la configuración de detección no está bien ajustada para este caso concreto" — la diferencia exacta que se trabaja en los siguientes apartados sobre configuración y ajuste fino del ataque.
