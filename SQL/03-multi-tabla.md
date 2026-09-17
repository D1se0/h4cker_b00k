---
icon: link
---

# 4 · Consultas Multi-Tabla

> Las bases de datos reales no guardan todo en una tabla: relacionan varias. Aquí aprendes a combinarlas (`JOIN`, `UNION`), a agrupar (`GROUP BY`, `HAVING`) y a usar subconsultas (`EXISTS`, `ANY/ALL`), además de manejar `NULL` y alias. Ejemplos listos para el [playground](https://d1se0.github.io/sql-learning/).

***

## JOIN — Combinar tablas

Una cláusula `JOIN` se usa para **combinar filas de dos o más tablas**, basándose en una columna relacionada entre ellas (normalmente una primary key y una foreign key).

### Tipos de JOIN

| Tipo                 | Qué devuelve                                                         |
| -------------------- | -------------------------------------------------------------------- |
| `(INNER) JOIN`       | Los registros con valores coincidentes en **ambas** tablas           |
| `LEFT (OUTER) JOIN`  | **Todos** los de la tabla izquierda + los coincidentes de la derecha |
| `RIGHT (OUTER) JOIN` | **Todos** los de la tabla derecha + los coincidentes de la izquierda |
| `FULL (OUTER) JOIN`  | Todo de ambas tablas, haya o no coincidencia                         |

> 💡 En la práctica, casi siempre se usa `(INNER) JOIN`. El playground de sql-learning soporta INNER y LEFT JOIN.

### Sintaxis

```sql
SELECT column_name(s)
FROM table1
JOIN table2
ON table1.column_name = table2.column_name;
```

### Entendiendo la relación (ejemplo visual)

Supongamos una selección de la tabla `unit_dose_orders` (dosis de medicamentos):

```sql
unit_dose_order_id | patient_id | dosage
1                  | 9          | 0.25 MG
2                  | 15         | 50 MG
3                  | 18         | 15
```

Y una selección de la tabla `patients`:

```sql
patient_id | first_name | last_name
1          | Miyuki     | Riviera
2          | Deunan     | Knute
3          | Lois       | McAllister
```

Fíjate en que la columna `patient_id` de `unit_dose_orders` **hace referencia** a la columna `patient_id` de `patients`. La relación entre ambas tablas es la columna `patient_id` (FK → PK).

### Ejemplo de JOIN

Selecciona los registros que tienen valores coincidentes en ambas tablas:

```sql
SELECT *
FROM patients p
JOIN admissions a ON a.patient_id = p.patient_id;
```

### JOIN de tres tablas

```sql
SELECT *
FROM patients p
JOIN admissions a ON a.patient_id = p.patient_id
JOIN doctors ph ON ph.doctor_id = a.attending_doctor_id;
```

> 🔗 Los alias `p`, `a`, `ph` se explican más abajo en este capítulo.

***

## UNION — Combinar resultados

El operador `UNION` combina el result-set de **dos o más sentencias SELECT**.

Reglas obligatorias:

* Cada `SELECT` debe tener el **mismo número de columnas**.
* Las columnas deben tener **tipos de datos similares**.
* Las columnas de cada `SELECT` deben ir en el **mismo orden**.

### Sintaxis

```sql
SELECT column_name(s) FROM table1
UNION
SELECT column_name(s) FROM table2;
```

Por defecto `UNION` selecciona solo valores **distintos**. Para permitir duplicados, usa `UNION ALL`:

```sql
SELECT column_name(s) FROM table1
UNION ALL
SELECT column_name(s) FROM table2;
```

> 💡 Los nombres de las columnas del resultado son normalmente los del **primer** `SELECT`.

### Ejemplos

```sql
-- Nombres (sin duplicados) de patients y doctors
SELECT first_name FROM patients
UNION
SELECT first_name FROM doctors
ORDER BY first_name;

-- Nombres (con duplicados) de patients y doctors
SELECT first_name FROM patients
UNION ALL
SELECT first_name FROM doctors
ORDER BY first_name;
```

> 🔥 **Nota para hacking:** `UNION SELECT` es la base del ataque **UNION-based SQLi** (capítulo 7): permite "apilar" los resultados de una consulta propia sobre la respuesta legítima de la web para **extraer datos de otras tablas**. Memoriza sus 3 reglas.

***

## GROUP BY — Agrupar filas

La sentencia `GROUP BY` agrupa las filas que tienen los **mismos valores** en filas-resumen, como "encuentra el número de pacientes de cada provincia".

Se suele usar con **funciones agregadas** (`COUNT()`, `MAX()`, `MIN()`, `SUM()`, `AVG()`) para agrupar el resultado por una o más columnas.

### Sintaxis

```sql
SELECT column_name(s)
FROM table_name
WHERE condition
GROUP BY column_name(s);
```

### Ejemplos

```sql
-- Número de pacientes por provincia
SELECT COUNT(*), province_id
FROM patients
GROUP BY province_id;

-- Lo mismo, ordenado de más a menos
SELECT COUNT(*), province_id
FROM patients
GROUP BY province_id
ORDER BY COUNT(*) DESC;
```

> 📚 Las funciones agregadas se detallan en el [capítulo 4](04-funciones-agregadas.md).

***

## HAVING — Filtrar grupos

La cláusula `HAVING` se añadió a SQL porque `WHERE` **no puede usarse con funciones agregadas**.

### Sintaxis

```sql
SELECT column_name(s)
FROM table_name
WHERE condition
GROUP BY column_name(s)
HAVING condition
ORDER BY column_name(s);
```

### Ejemplos

```sql
-- Nombres que se repiten más de 30 veces
SELECT COUNT(*), first_name
FROM patients
GROUP BY first_name
HAVING COUNT(*) > 30;

-- Lo mismo, ordenado de más a menos
SELECT COUNT(*), first_name
FROM patients
GROUP BY first_name
HAVING COUNT(*) > 30
ORDER BY COUNT(*) DESC;
```

> 🧠 **Regla de oro:** `WHERE` filtra **filas** (antes de agrupar), `HAVING` filtra **grupos** (después de agrupar).

***

## EXISTS — Probar si una subconsulta devuelve filas

El operador `EXISTS` se usa para probar la **existencia de cualquier registro** en una subconsulta. Devuelve `TRUE` si la subconsulta devuelve uno o más registros.

### Sintaxis

```sql
SELECT column_name(s)
FROM table_name
WHERE EXISTS
  (SELECT column_name FROM table_name WHERE condition);
```

### Ejemplo

Devuelve todos los pacientes con diagnóstico de embarazo:

```sql
SELECT * FROM patients
WHERE EXISTS (SELECT diagnosis FROM admissions
              WHERE patients.patient_id = admissions.patient_id
              AND diagnosis = 'Pregnancy');
```

> ⚠️ Esta forma es **ineficiente** (la subconsulta se re-ejecuta por cada fila). Lo mismo, más eficiente con JOIN:

```sql
SELECT * FROM patients
JOIN admissions ON patients.patient_id = admissions.patient_id
WHERE diagnosis = 'Pregnancy';
```

***

## ANY y ALL — Comparar contra un conjunto

Los operadores `ANY` y `ALL` permiten comparar el valor de una columna contra un **rango de otros valores**.

* **ANY**: devuelve `TRUE` si **cualquiera** de los valores de la subconsulta cumple la condición.
* **ALL**: devuelve `TRUE` si **todos** los valores de la subconsulta cumplen la condición.

### Sintaxis ANY

```sql
SELECT column_name(s)
FROM table_name
WHERE column_name operator ANY
  (SELECT column_name FROM table_name WHERE condition);
```

### Sintaxis ALL

```sql
-- Con SELECT
SELECT ALL column_name(s)
FROM table_name
WHERE condition;

-- Con WHERE o HAVING
SELECT column_name(s)
FROM table_name
WHERE column_name operator ALL
  (SELECT column_name FROM table_name WHERE condition);
```

> ℹ️ El playground de sql-learning no soporta ANY/ALL, pero sí la mayoría de motores reales (MySQL, PostgreSQL, SQL Server).

***

## NULL — Valores vacíos

### ¿Qué es un valor NULL?

Un campo con valor `NULL` es un campo **sin valor**. Si un campo es opcional, se puede insertar o actualizar un registro sin darle valor, y quedará guardado como `NULL`.

### ¿Cómo se comprueba un NULL?

❌ **NO** se puede probar con operadores de comparación (`=`, `<`, `<>`). Esto NO funciona: `WHERE allergies = NULL`.

✅ Hay que usar los operadores **`IS NULL`** e **`IS NOT NULL`**:

```sql
-- Sintaxis IS NULL
SELECT column_names
FROM table_name
WHERE column_name IS NULL;

-- Sintaxis IS NOT NULL
SELECT column_names
FROM table_name
WHERE column_name IS NOT NULL;
```

### Ejemplos

```sql
-- Pacientes SIN alergias registradas (allergies es NULL)
SELECT *
FROM patients
WHERE allergies IS NULL;

-- Pacientes CON alergias registradas
SELECT *
FROM patients
WHERE allergies IS NOT NULL;
```

***

## IFNULL / ISNULL / COALESCE / NVL — Sustituir NULL

La función para sustituir `NULL` por otro valor **cambia de nombre según el dialecto** (todas funcionan parecido):

| Dialecto   | Función                  |
| ---------- | ------------------------ |
| MySQL      | `IFNULL()`, `COALESCE()` |
| SQL Server | `ISNULL()`               |
| MS Access  | `IsNull()` (+ `IIF`)     |
| Oracle     | `NVL()`                  |

### Ejemplo

En `patients`, la columna `allergies` muestra `NULL` en algunas filas. Queremos mostrar un valor por defecto:

```sql
-- MySQL
SELECT first_name, IFNULL(allergies, 'none') AS allergies
FROM patients;

-- MySQL (alternativa)
SELECT first_name, COALESCE(allergies, 'none') AS allergies
FROM patients;

-- SQL Server
SELECT first_name, ISNULL(allergies, 'none') AS allergies
FROM patients;

-- MS Access
SELECT first_name, IIF(ISNULL(allergies, 0), allergies) AS allergies
FROM patients;

-- Oracle
SELECT first_name, NVL(allergies, 'none') AS allergies
FROM patients;
```

***

## Alias — Nombres temporales

Los alias de SQL se usan para dar a una tabla, o a una columna, un **nombre temporal**. Se usan mucho para hacer los nombres de columnas más legibles.

* El alias **solo existe durante la duración de esa consulta**.
* Se crea con la palabra clave `AS` (en algunos dialectos es opcional).

### Sintaxis

```sql
-- Alias para columnas
SELECT column_name AS alias_name
FROM table_name;

-- Alias para tablas
SELECT column_name(s)
FROM table_name AS alias_name;
```

### Ejemplos

```sql
-- Alias para dos columnas
SELECT avg(weight) AS average_weight,
       avg(height) AS average_height
FROM patients;

-- Alias para tablas: admissions = 'a', patients = 'p'
SELECT *
FROM patients AS p
JOIN admissions AS a ON a.patient_id = p.patient_id;
```

> 💡 En los JOIN con alias, puedes prefijar las columnas con el alias (`p.patient_id`) para evitar ambigüedades cuando dos tablas tienen columnas con el mismo nombre.

***

## CASE — Lógica if/then/else en SQL

La sentencia `CASE` recorre condiciones y devuelve un valor cuando se cumple la **primera** condición (como un if-then-else). Cuando una condición es verdadera, deja de leer y devuelve el resultado. Si ninguna se cumple, devuelve el valor del `ELSE`. Si no hay `ELSE` ni condiciones verdaderas, devuelve `NULL`.

### Sintaxis

```sql
CASE
  WHEN condition1 THEN result1
  WHEN condition2 THEN result2
  WHEN conditionN THEN resultN
  ELSE result
END;
```

### Ejemplos

```sql
-- Clasificar por altura
SELECT patient_id, height,
  CASE
    WHEN height > 175 THEN 'height is greater than 175'
    WHEN height = 175 THEN 'height is 175'
    ELSE 'height is under 175'
  END AS height_group
FROM patients;

-- CASE dentro de ORDER BY: ordenar por allergies,
-- pero si es NULL, ordenar por first_name
SELECT patient_id, first_name, allergies
FROM patients
ORDER BY
  (CASE
    WHEN allergies IS NULL THEN first_name
    ELSE allergies
  END);
```

***

## 🧪 Mini-retos del capítulo

1. Muestra nombre y diagnóstico de cada ingreso, uniendo `patients` y `admissions`.
2. Cuenta cuántos ingresos hay por cada doctor (`attending_doctor_id`), ordenados desc.
3. Lista los nombres (sin duplicados) que aparecen tanto en `patients` como en `doctors`.
4. Muestra los pacientes que NO tienen alergias (NULL), mostrando 'none' en su lugar.
5. Nombres de pacientes con más de 30 repeticiones.

<details>

<summary>👀 Soluciones</summary>

```sql
-- 1
SELECT p.first_name, a.diagnosis
FROM patients p
JOIN admissions a ON a.patient_id = p.patient_id;
-- 2
SELECT COUNT(*), attending_doctor_id
FROM admissions GROUP BY attending_doctor_id ORDER BY COUNT(*) DESC;
-- 3
SELECT DISTINCT p.first_name
FROM patients p
JOIN doctors d ON d.first_name = p.first_name;
-- 4
SELECT first_name, IFNULL(allergies, 'none') AS allergies
FROM patients WHERE allergies IS NULL;
-- 5
SELECT COUNT(*), first_name FROM patients
GROUP BY first_name HAVING COUNT(*) > 30;
```

</details>

## 📌 Resumen del capítulo

| Herramienta              | Para qué                                                |
| ------------------------ | ------------------------------------------------------- |
| `JOIN ... ON`            | Combinar tablas relacionadas (INNER, LEFT, RIGHT, FULL) |
| `UNION [ALL]`            | Apilar resultados de varios SELECT                      |
| `GROUP BY`               | Agrupar filas por valores comunes                       |
| `HAVING`                 | Filtrar grupos (WHERE no vale con agregados)            |
| `EXISTS` / `ANY` / `ALL` | Subconsultas condicionales                              |
| `IS NULL` / `IFNULL()`   | Manejar valores vacíos                                  |
| `AS`                     | Alias de columnas y tablas                              |
| `CASE WHEN`              | Lógica condicional dentro de la consulta                |

➡️ **Siguiente capítulo:** [Funciones Agregadas](04-funciones-agregadas.md)
