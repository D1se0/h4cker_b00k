# Identificación de filtros

## Por qué una aplicación puede rechazar la inyección sin ser invulnerable

Cuando un equipo de desarrollo es consciente del riesgo de inyección de comandos, suele añadir alguna capa de protección reactiva: listas negras de caracteres especiales, listas negras de comandos concretos, o un firewall de aplicaciones web (WAF) delante de la aplicación. Ninguna de estas medidas corrige la causa raíz (entrada sin sanitizar llegando a una función de ejecución), por lo que entender **qué exactamente** está bloqueando el filtro es el primer paso para evaluar si el problema de fondo sigue ahí.

## Reconociendo que existe un filtro

Si al introducir un payload básico (`127.0.0.1; whoami`) la aplicación responde con un mensaje genérico tipo "entrada no válida" en lugar de simplemente fallar silenciosamente o procesar el comando, eso indica que algún mecanismo de detección activo está interviniendo.

Distinguir el origen del rechazo aporta contexto útil:

- Si el mensaje de error aparece **en el mismo formato** que el resto de la interfaz de la aplicación (en el mismo campo de salida, con el mismo estilo visual), es probable que el rechazo provenga de la propia lógica de la aplicación (validación en el backend de la propia app).
- Si en cambio la respuesta cambia completamente de aspecto (una página distinta, con información adicional como la IP del solicitante), es más probable que se trate de un **WAF** interpuesto, rechazando la petición antes de que llegue siquiera al código de la aplicación.

## Las dos categorías de filtro más habituales

| Tipo de filtro | Qué bloquea |
|---|---|
| Lista negra de **caracteres** | Rechaza la petición si contiene determinados símbolos (`;`, `&`, `\|`...) |
| Lista negra de **comandos/palabras** | Rechaza la petición si contiene ciertos nombres de comando (`whoami`, `cat`, `nc`...) |

Una aplicación puede implementar una, otra, o ambas simultáneamente — el proceso de identificación debe contemplar las dos posibilidades.

## Metodología de aislamiento: reducir la entrada paso a paso

La técnica más fiable para identificar qué elemento concreto del payload provoca el rechazo es **reducir la entrada progresivamente**, probando un único elemento adicional cada vez sobre una base que ya se sabe que funciona.

Partiendo de una entrada válida confirmada (`127.0.0.1`), se añade un único carácter sospechoso:

```
127.0.0.1;
```

Si esto ya provoca el rechazo, queda confirmado que el punto y coma forma parte de la lista negra de caracteres — sin necesidad todavía de saber nada sobre el resto del payload.

Repitiendo este mismo proceso con cada operador de la tabla vista en apartados anteriores (`&&`, `||`, `&`, `|`, backticks, `$()`), se puede construir un mapa completo de qué caracteres concretos están bloqueados y cuáles, si los hay, siguen siendo utilizables.

## Por qué este enfoque metódico es preferible a probar payloads completos a ciegas

Probar payloads completos de listas externas (como se desaconsejó también en el bloque de XSS) tiene el mismo problema aquí: si un payload falla, no queda claro **por qué** falló — pudo ser el carácter separador, el comando elegido, o ambos a la vez. Aislar variables una a una, en cambio, construye un entendimiento preciso del filtro que después permite elegir con criterio qué técnica de evasión aplicar — el tema de los siguientes apartados de este bloque.
