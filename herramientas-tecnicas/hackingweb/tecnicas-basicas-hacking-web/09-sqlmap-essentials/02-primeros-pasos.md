# Primeros pasos: ejecución básica e interpretación de resultados

## Los dos niveles de ayuda

```bash
sqlmap -h    # opciones básicas, suficiente en la mayoría de casos
sqlmap -hh   # listado completo y avanzado de todas las opciones
```

La [wiki oficial del proyecto](https://github.com/sqlmapproject/sqlmap/wiki/Usage) es la referencia completa y siempre actualizada — el punto de consulta recomendado ante cualquier duda sobre una opción concreta.

## El escenario más básico: un parámetro GET

Tomando como referencia el patrón vulnerable visto en el bloque anterior:

```php
$sql = "SELECT * FROM users WHERE id = " . $_GET["id"] . " LIMIT 0, 1";
```

```bash
sqlmap -u "http://objetivo.htb/vuln.php?id=1" --batch
```

`--batch` indica a SQLMap que use siempre la respuesta por defecto ante cualquier pregunta interactiva durante la ejecución — esencial para scripting y automatización, evitando que el proceso se quede esperando confirmación manual.

## Qué ocurre internamente durante esta ejecución

1. **Comprobación de conexión** al objetivo.
2. **Detección de WAF/IPS/IDS** mediante una sonda heurística.
3. **Verificación de estabilidad** del contenido (¿la respuesta cambia entre peticiones idénticas, más allá de lo esperado?).
4. **Verificación de que el parámetro es dinámico** — si cambiar su valor no altera la respuesta, no tiene sentido seguir probando ahí.
5. **Test heurístico básico**: una sonda rápida (no concluyente) que sugiere si el parámetro podría ser inyectable y, en su caso, qué DBMS es probable.
6. **Pruebas sistemáticas** de cada técnica (BEUSTQ) y, dentro de cada una, de múltiples variantes de payload específicas por motor de base de datos.

## Interpretando el resultado final

```
sqlmap identified the following injection point(s) with a total of 46 HTTP(s) requests:
---
Parameter: id (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: id=1 AND 8814=8814

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: ...

    Type: UNION query
    Title: Generic UNION query (NULL) - 3 columns
    Payload: id=1 UNION ALL SELECT NULL,NULL,CONCAT(...)-- -
```

Tres datos críticos en esta salida:

- **El parámetro vulnerable** (`id`, vía `GET`).
- **Las técnicas confirmadas** que funcionan contra él — a menudo más de una simultáneamente, lo que da margen para elegir la más rápida disponible (recordando el orden de velocidad visto en el apartado anterior).
- **El payload exacto** de cada técnica — información valiosa incluso para quien prefiera continuar la explotación manualmente a partir de aquí, exactamente con el conocimiento construido en el bloque de *SQL Injection Fundamentals*.

## Por qué esto vale la pena entenderlo, no solo "lanzar y esperar"

SQLMap puede sentirse como una caja negra que "simplemente funciona" — pero cada mensaje de su salida tiene un significado preciso que ayuda a diagnosticar problemas, ajustar la estrategia, o decidir cuándo merece la pena pasar a una explotación más manual y dirigida. El siguiente apartado desglosa en detalle los mensajes de log más habituales que aparecen durante una ejecución típica.
