# 🛠️ Capítulo 5 — Funciones de Utilidad

> Funciones para transformar texto, calcular números, manipular fechas y analizar filas "ventana a ventana". Son el cuchillo suizo de SQL. Ejemplos en el [playground](https://d1se0.github.io/sql-learning/).

---

## 📝 Funciones de cadena

### CONCAT() — Unir textos

La función `CONCAT()` **une dos o más expresiones** en una sola cadena.

> 💡 Según el dialecto puede haber sintaxis nativa de concatenación: `+` (SQL Server) o `||` (Oracle, PostgreSQL, SQLite).

**Sintaxis:**

```sql
CONCAT(expression1, expression2, expression3, ...)
```

Si cualquier expresión es `NULL`, el resultado es `NULL`.

**Ejemplo:** concatena el nombre y apellido de cada paciente:

```sql
SELECT CONCAT(first_name, ' ', last_name) AS full_name
FROM patients;
```

### LEN() — Longitud de una cadena

La función `LEN()` devuelve la **longitud de una cadena** en bytes.

> 💡 Según el dialecto puede llamarse `LENGTH()` (SQLite, MySQL, PostgreSQL).

**Sintaxis:**

```sql
LEN(string)
```

**Ejemplo:** muestra cada nombre y su longitud:

```sql
SELECT first_name, LEN(first_name) AS length_of_name
FROM patients;
```

### UPPER() — Convertir a mayúsculas

La función `UPPER()` devuelve una cadena **en mayúsculas**. Ejemplo: `'ExAmple'` → `'EXAMPLE'`.

> 💡 También llamada `UCASE()` en algunos dialectos.

**Sintaxis:**

```sql
UPPER(string)
```

**Ejemplo:**

```sql
SELECT first_name, UPPER(first_name) AS uppercase_name
FROM patients;
```

### LOWER() — Convertir a minúsculas

La función `LOWER()` devuelve una cadena **en minúsculas**. Ejemplo: `'ExAmple'` → `'example'`.

> 💡 También llamada `LCASE()` en algunos dialectos.

**Sintaxis:**

```sql
LOWER(string)
```

**Ejemplo:**

```sql
SELECT first_name, LOWER(first_name) AS lowercase_name
FROM patients;
```

> 🔥 **Nota para hacking:** `CONCAT()` es clave en SQLi de MySQL (permite juntar datos de varias columnas en una sola salida) y `UPPER()`/`LOWER()` ayudan a evadir filtros que distinguen mayúsculas (`SeLeCt`).

---

## 🔢 Funciones numéricas

### RAND() — Número aleatorio

La función `RAND()` devuelve un **número aleatorio entre 0 y 1**.

> 💡 También llamada `RANDOM()` en algunos dialectos. Esta implementación no soporta el parámetro `seed`.

**Sintaxis:**

```sql
RAND(seed)
```

- `seed` (opcional): si se indica, devuelve una secuencia **repetible** de números aleatorios.

**Ejemplo:**

```sql
SELECT RAND();
```

### ROUND() — Redondear

La función `ROUND()` devuelve un número **redondeado a la posición decimal** especificada.

**Sintaxis:**

```sql
ROUND(number, decimals)
```

- `number`: obligatorio, el número a redondear.
- `decimals`: opcional, decimales a redondear. Si se omite, el resultado es un entero.

**Ejemplo:** redondea 135.375 a 2 decimales:

```sql
SELECT ROUND(135.375, 2);
```

### FLOOR() — Redondear hacia abajo

La función `FLOOR()` devuelve un número **redondeado hacia abajo** al entero más cercano.

**Sintaxis:**

```sql
FLOOR(number)
```

**Ejemplo:** redondea 25.9 hacia abajo a 25:

```sql
SELECT FLOOR(25.9);
```

### CEIL() — Redondear hacia arriba

La función `CEIL()` devuelve un número **redondeado hacia arriba** al entero más cercano.

**Sintaxis:**

```sql
CEIL(number)
```

**Ejemplo:** redondea 25.1 hacia arriba a 26:

```sql
SELECT CEIL(25.1);
```

---

## ➗ Funciones matemáticas

### ABS() — Valor absoluto

La función `ABS()` devuelve el **valor absoluto (positivo)** de un número.

**Sintaxis:**

```sql
ABS(number)
```

**Ejemplo:** devuelve el valor absoluto de -362.3:

```sql
SELECT ABS(-362.3);
```

### POWER() — Potencia

La función `POWER()` devuelve el valor de un número **elevado a la potencia** de otro.

> 💡 También llamada `POW()` en algunos dialectos.

**Sintaxis:**

```sql
POWER(base, exponent)
```

**Ejemplo:** 8 elevado a 3:

```sql
SELECT POWER(8, 3);
```

### SQRT() — Raíz cuadrada

La función `SQRT()` devuelve la **raíz cuadrada** de un número.

**Sintaxis:**

```sql
SQRT(number)
```

- `number`: obligatorio, debe ser **mayor que 0**.

**Ejemplo:**

```sql
SELECT SQRT(13);
```

---

## 📅 Funciones de fecha

### CURRENT_TIMESTAMP — Fecha y hora actuales

La función `CURRENT_TIMESTAMP` devuelve la **fecha y hora actuales**.

> 💡 Se devuelve en formato `"YYYY-MM-DD HH-MM-SS"` (cadena).

**Ejemplo:**

```sql
SELECT CURRENT_TIMESTAMP;
```

### YEAR() — Extraer el año

La función `YEAR()` devuelve la **parte del año** de una fecha dada (un número de 1000 a 9999).

**Sintaxis:**

```sql
YEAR(date)
```

**Ejemplo:**

```sql
SELECT YEAR(CURRENT_TIMESTAMP);
```

### MONTH() — Extraer el mes

La función `MONTH()` devuelve la **parte del mes** de una fecha dada.

**Sintaxis:**

```sql
MONTH(date)
```

**Ejemplo:**

```sql
SELECT MONTH(CURRENT_TIMESTAMP);
```

### DAY() — Extraer el día

La función `DAY()` devuelve la **parte del día** de una fecha dada.

**Sintaxis:**

```sql
DAY(date)
```

**Ejemplo:**

```sql
SELECT DAY(CURRENT_TIMESTAMP);
```

> 💡 Estas funciones funcionan sobre cualquier fecha, no solo la actual: `SELECT YEAR(birth_date) FROM patients;`

---

## 🪟 Window Functions — Funciones de ventana

Las **window functions** (funciones de ventana) son el nivel avanzado: hacen cálculos sobre un conjunto de filas **sin colapsarlas en una sola**, a diferencia de las agregadas normales.

### Agregada normal vs window function

Una función agregada (`SUM`, `AVG`, `COUNT`, `MIN`, `MAX`...) calcula sobre un conjunto de filas y devuelve **una sola fila**:

```sql
-- Una única fila con la media de todos los pesos
SELECT AVG(weight) AS avg_weight
FROM patients;
```

Una **window function** hace el mismo cálculo pero **conserva cada fila**, añadiendo el resultado como columna extra:

```sql
-- Cada fila, junto a la media global
SELECT
  first_name,
  last_name,
  weight,
  AVG(weight) OVER() AS avg_weight
FROM patients;
```

La cláusula **`OVER()`** indica que la función se usa como window function.

### Sintaxis general

```sql
window_function_name ( expression ) OVER (
  partition_clause
  order_clause
  frame_clause
)
```

**Explicación de las cláusulas:**

- `window_function_name`: la función (`ROW_NUMBER()`, `RANK()`, `SUM()`, `AVG()`, etc.).
- `expression`: la columna o expresión objetivo.
- **`OVER`**: define particiones y el orden de las filas.
- **`partition_clause`**: divide las filas en particiones → `PARTITION BY expr1, expr2, ...`
- **`order_clause`**: ordena las filas dentro de la partición → `ORDER BY expression [ASC|DESC] [NULL {FIRST|LAST}], ...`
- **`frame_clause`**: subconjunto de la partición → `{ROWS|RANGE} frame_start [{BETWEEN frame_start AND frame_end}]`

**Opciones del frame:**

| Opción | Significado |
|--------|-------------|
| `UNBOUNDED PRECEDING` | Empieza en la primera fila de la partición |
| `N PRECEDING` | Empieza N filas antes de la actual |
| `CURRENT ROW` | Fila actual |
| `N FOLLOWING` | Termina N filas después de la actual |
| `UNBOUNDED FOLLOWING` | Termina en la última fila de la partición |

**Tipos de window functions:**

| Tipo | Funciones |
|------|-----------|
| De valor | `FIRST_VALUE()`, `LAST_VALUE()`, `LAG()`, `LEAD()` |
| De ranking | `CUME_DIST()`, `DENSE_RANK()`, `NTILE()`, `PERCENT_RANK()`, `RANK()`, `ROW_NUMBER()` |
| Agregadas | `AVG()`, `COUNT()`, `MAX()`, `MIN()`, `SUM()` |

### LAG() — El valor de la fila anterior

La función `LAG()` devuelve el registro **desplazado hacia atrás** la cantidad especificada.

**Sintaxis:**

```sql
LAG(expression [, offset])
```

- `expression`: obligatorio. Debe ser un valor escalar (no puede ser otra función analítica).
- `offset`: opcional. Filas hacia atrás desde la actual. Por defecto `1`. Debe ser positivo.

**Ejemplo:** muestra cada nombre junto al del paciente anterior:

```sql
SELECT
  patient_id,
  first_name,
  LAG(first_name, 1) OVER() AS previous_name
FROM patients;
```

### LEAD() — El valor de la fila siguiente

La función `LEAD()` devuelve el registro **desplazado hacia adelante** la cantidad especificada.

**Sintaxis:**

```sql
LEAD(expression [, offset])
```

- `expression`: obligatorio. Valor escalar.
- `offset`: opcional. Filas hacia adelante desde la actual. Por defecto `1`. Debe ser positivo.

**Ejemplo:** muestra cada nombre junto al del paciente siguiente:

```sql
SELECT
  patient_id,
  first_name,
  LEAD(first_name, 1) OVER() AS next_name
FROM patients;
```

### FIRST_VALUE() — Primer valor de la partición

La función `FIRST_VALUE()` devuelve el **primer valor** de una partición ordenada del result-set.

**Sintaxis:**

```sql
FIRST_VALUE ( scalar_expression ) OVER (
  [PARTITION BY partition_expression, ... ]
  ORDER BY sort_expression [ASC | DESC], ...
)
```

- `scalar_expression`: obligatorio. Expresión evaluada contra el valor de la **primera fila** de la partición ordenada. Puede ser una columna, subconsulta o expresión que evalúe a un único valor. No puede ser otra window function.

**Ejemplo:** la fecha de nacimiento del paciente **más mayor** de cada provincia:

```sql
SELECT
  patient_id,
  province_id,
  FIRST_VALUE(birth_date) OVER(
    PARTITION BY province_id   -- agrupar por provincia
    ORDER BY birth_date        -- ordenar por fecha de nacimiento
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) AS oldest_birth_date
FROM patients
ORDER BY patient_id;
```

### LAST_VALUE() — Último valor de la partición

La función `LAST_VALUE()` devuelve el **último valor** de una partición ordenada del result-set.

**Sintaxis:**

```sql
LAST_VALUE ( scalar_expression ) OVER (
  [PARTITION BY partition_expression, ... ]
  ORDER BY sort_expression [ASC | DESC], ...
)
```

**Ejemplo:** la fecha de nacimiento del paciente **más joven** de cada provincia:

```sql
SELECT
  patient_id,
  province_id,
  LAST_VALUE(birth_date) OVER(
    PARTITION BY province_id   -- agrupar por provincia
    ORDER BY birth_date        -- ordenar por fecha de nacimiento
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) AS youngest_birth_date
FROM patients
ORDER BY patient_id;
```

### Suma acumulativa (rolling sum)

```sql
SELECT
  patient_id,
  first_name,
  weight,
  SUM(weight) OVER(ORDER BY patient_id) AS rolling_sum
FROM patients;
```

### ⚠️ Filtrar por el resultado de una window function

El resultado de una window function **NO se puede filtrar** con `WHERE` ni `HAVING` directamente. Hay que usar la cláusula `WITH` para crear una tabla temporal:

```sql
-- ❌ INCORRECTO (no funciona):
SELECT
  patient_id,
  first_name,
  weight,
  SUM(weight) OVER(ORDER BY patient_id) AS rolling_sum
FROM patients
WHERE rolling_sum < 1000;
```

```sql
-- ✅ CORRECTO (con WITH):
WITH rolling_sum_table AS (
  SELECT
    patient_id,
    first_name,
    weight,
    SUM(weight) OVER(ORDER BY patient_id) AS rolling_sum
  FROM patients
)
SELECT *
FROM rolling_sum_table
WHERE rolling_sum < 1000;
```

---

## 🧪 Mini-retos del capítulo

1. Muestra el nombre completo de cada paciente en una sola columna.
2. Nombres con más de 5 letras.
3. Nombres y apellidos todo en mayúsculas.
4. Edad aproximada de cada paciente (pista: `YEAR(CURRENT_TIMESTAMP) - YEAR(birth_date)`).
5. Cada paciente junto al nombre del paciente 2 posiciones detrás (LAG con offset 2).

<details>
<summary>👀 Soluciones</summary>

```sql
-- 1
SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM patients;
-- 2
SELECT first_name FROM patients WHERE LEN(first_name) > 5;
-- 3
SELECT UPPER(CONCAT(first_name, ' ', last_name)) AS full_name FROM patients;
-- 4
SELECT first_name, YEAR(CURRENT_TIMESTAMP) - YEAR(birth_date) AS approx_age FROM patients;
-- 5
SELECT patient_id, first_name, LAG(first_name, 2) OVER() AS prev2_name FROM patients;
```
</details>

## 📌 Resumen del capítulo

| Categoría | Funciones |
|-----------|-----------|
| Cadena | `CONCAT()`, `LEN()`, `UPPER()`, `LOWER()` |
| Numéricas | `RAND()`, `ROUND()`, `FLOOR()`, `CEIL()` |
| Matemáticas | `ABS()`, `POWER()`, `SQRT()` |
| Fecha | `CURRENT_TIMESTAMP`, `YEAR()`, `MONTH()`, `DAY()` |
| Ventana | `LAG()`, `LEAD()`, `FIRST_VALUE()`, `LAST_VALUE()` + agregadas con `OVER()` |

➡️ **Siguiente capítulo:** [Tablas y DDL](./06-tablas-ddl.md)
