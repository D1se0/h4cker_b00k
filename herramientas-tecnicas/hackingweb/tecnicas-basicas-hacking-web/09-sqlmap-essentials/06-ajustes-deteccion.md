# Ajustando la detección: nivel, riesgo y comparación de respuestas

## La anatomía de un payload de SQLMap

Cada carga útil que SQLMap envía se compone de dos partes:

- **Vector**: el código SQL útil que se ejecutará (`UNION ALL SELECT 1,2,VERSION()`).
- **Límites** (prefijo/sufijo): lo necesario para insertar correctamente el vector dentro de la sintaxis de la consulta vulnerable (`'<vector>-- -`).

## Prefijo y sufijo personalizados

En casos especiales no cubiertos por el conjunto de límites estándar:

```bash
sqlmap -u "http://objetivo.htb/?q=test" --prefix="%'))" --suffix="-- -"
```

Tomando el ejemplo de una consulta vulnerable con doble paréntesis:

```php
$query = "SELECT id,name FROM users WHERE id LIKE (('" . $_GET["q"] . "')) LIMIT 0,1";
```

El vector `UNION ALL SELECT 1,2,VERSION()`, envuelto entre el prefijo `%'))` y el sufijo `-- -`, produce una sentencia sintácticamente válida — el mismo principio de "equilibrar delimitadores" trabajado manualmente en el bloque anterior, ahora aplicado de forma explícita a través de la configuración de SQLMap.

## `--level` y `--risk`: ampliando la búsqueda

Por defecto (`--level=1 --risk=1`), SQLMap usa un conjunto reducido y de alta probabilidad de éxito — aproximadamente **72 payloads** por parámetro probado.

| Opción | Rango | Qué amplía |
|---|---|---|
| `--level` | 1-5 | Número de vectores y límites probados, según su probabilidad esperada de éxito |
| `--risk` | 1-3 | Vectores adicionales según su riesgo de causar efectos secundarios en el objetivo |

Con `--level=5 --risk=3`, el número de payloads probados por parámetro asciende a **más de 7.800** — una diferencia de dos órdenes de magnitud en tiempo de ejecución.

### Por qué `--risk` es especialmente delicado

Los payloads de mayor riesgo incluyen, por ejemplo, variantes con `OR` que en sentencias `DELETE` o `UPDATE` vulnerables podrían modificar o destruir datos del objetivo de forma no intencionada — el mismo principio de "PoC mínima, sin causar daño" trabajado en el bloque de *Web Fuzzing* al hablar de validación responsable de hallazgos. Aumentar `--risk` solo está justificado cuando hay una razón concreta (por ejemplo, sospecha fundada de una vulnerabilidad en un formulario de login que usa lógica `OR`) y siempre dentro de un alcance de auditoría debidamente autorizado.

### Cuándo SÍ vale la pena aumentar estos valores

- El escaneo por defecto no encuentra nada, pero hay fuertes indicios manuales (del trabajo hecho en el bloque anterior) de que el parámetro **sí** es vulnerable.
- Se sospecha de un tipo de inyección poco común no cubierto por el conjunto reducido de payloads por defecto.

En la mayoría de casos rutinarios, sin embargo, se recomienda **no** tocar estos valores — ralentiza considerablemente la detección sin aportar beneficio si el objetivo es razonablemente "normal".

## Ajuste fino de la comparación TRUE/FALSE

Cuando la respuesta del objetivo es muy grande o tiene mucho contenido dinámico variable, distinguir entre una respuesta `TRUE` y una `FALSE` por simple comparación de contenido puede no ser fiable. SQLMap ofrece anclas alternativas:

| Opción | Ancla usada para distinguir TRUE/FALSE |
|---|---|
| `--code` | Código de estado HTTP específico (p. ej. `--code=200`) |
| `--titles` | Contenido de la etiqueta `<title>` |
| `--string` / `--not-string` | Presencia/ausencia de una cadena de texto específica |
| `--regex` | Coincidencia de una expresión regular |

Estas opciones son particularmente valiosas en inyección **boolean-based blind**, donde toda la técnica depende enteramente de detectar correctamente esa diferencia — un ancla mal elegida (o ausente) puede producir tanto falsos positivos como falsos negativos sistemáticos.

## Viendo qué payloads se están probando realmente

```bash
sqlmap -u www.objetivo.htb/?id=1 -v 3 --level=5
```

Con verbosidad 3 o superior, cada payload probado se imprime explícitamente con la etiqueta `[PAYLOAD]` — la forma más directa de comparar en la práctica qué cambia exactamente entre `--level=1` y `--level=5`, en lugar de confiar únicamente en la documentación.

## El principio general de ajuste

SQLMap ya está calibrado por defecto para cubrir el caso más común con la mayor eficiencia posible. Tocar `--level`, `--risk`, o las opciones de ancla de comparación tiene sentido únicamente cuando hay una razón concreta y informada para hacerlo — nunca como ajuste "por defecto" para cualquier auditoría, ya que el coste en tiempo y en peticiones generadas contra el objetivo crece muy rápidamente.
