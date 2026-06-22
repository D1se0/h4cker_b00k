# Inyección basada en UNION

## El flujo completo, paso a paso

Confirmada la inyectabilidad de un parámetro (mediante el método visto en apartados anteriores: una comilla simple provoca un error de sintaxis), el siguiente objetivo es construir una inyección `UNION SELECT` funcional. Esto requiere dos pasos secuenciales: determinar el número de columnas, y determinar cuáles de ellas se muestran realmente en la página.

## Paso 1: determinar el número de columnas

Existen dos métodos equivalentes.

### Método A: `ORDER BY`

Se prueba ordenar incrementalmente por cada posición de columna, hasta que se produzca un error indicando que esa columna no existe:

```sql
' order by 1-- -   → resultado normal
' order by 2-- -   → resultado normal (orden distinto)
' order by 3-- -   → resultado normal
' order by 4-- -   → resultado normal
' order by 5-- -   → ERROR: Unknown column '5' in 'order clause'
```

El último número que **no** produjo error es el número total de columnas — en este ejemplo, **4**.

### Método B: `UNION SELECT` iterativo

Se prueba directamente con un número creciente de columnas en la inyección, hasta obtener un resultado exitoso (en lugar de un error):

```sql
' UNION select 1,2,3-- -    → ERROR: different number of columns
' UNION select 1,2,3,4-- -  → resultado exitoso
```

### Comparando ambos métodos

| Método | Comportamiento | Cuándo preferirlo |
|---|---|---|
| `ORDER BY` | Funciona hasta que falla | Cuando se sospecha que `UNION` podría estar filtrado o bloqueado por un WAF |
| `UNION SELECT` | Falla hasta que funciona | Más directo cuando ya se sabe que `UNION` no está bloqueado |

Cualquiera de los dos llega al mismo resultado — la elección suele ser cuestión de preferencia o de qué responde mejor en el contexto concreto.

## Paso 2: identificar qué columnas se imprimen en la página

Una consulta puede devolver, por ejemplo, 4 columnas, pero la aplicación solo **mostrar** algunas de ellas en pantalla (un `id` interno, típicamente, no se muestra al usuario final). Es crítico identificar **en qué posiciones concretas** aparece el resultado, porque solo ahí tiene sentido colocar la extracción de datos real.

```sql
' UNION select 1,2,3,4-- -
```

Si en la respuesta renderizada solo se observan los valores `2`, `3` y `4` (pero no `1`), eso confirma que esa primera columna **no se imprime** — no sirve como posición de extracción, aunque técnicamente forme parte del resultado de la consulta.

> Usar números secuenciales como relleno (en lugar de, por ejemplo, todo `NULL`) es precisamente lo que permite este rastreo visual inmediato: ver exactamente qué número aparece dónde en la respuesta renderizada.

## Paso 3: confirmar con datos reales de la base de datos

Antes de pasar a la enumeración completa, conviene confirmar que se puede extraer **información real** (no solo números de relleno) sustituyendo una de las posiciones visibles por una consulta SQL real:

```sql
' UNION select 1,@@version,3,4-- -
```

`@@version` es una variable de MySQL/MariaDB que devuelve la versión exacta del motor — si aparece correctamente en la respuesta, queda confirmado que la inyección UNION funciona de extremo a extremo y está lista para usarse con consultas de enumeración reales.

## Resumen del proceso completo

```
1. Confirmar inyectabilidad (comilla simple → error)
2. Determinar número de columnas (ORDER BY o UNION SELECT iterativo)
3. Identificar qué columnas se imprimen visiblemente
4. Confirmar extracción de datos reales (@@version como prueba)
5. Sustituir las posiciones de relleno por las consultas de enumeración reales
```

Este flujo metodológico —repetible y sistemático— es exactamente lo que se aplica en el siguiente apartado para enumerar la base de datos completa: bases de datos, tablas, columnas, y finalmente los datos sensibles que contienen.
