---
icon: file-code
---

# 5 · Funciones Agregadas

> Las funciones agregadas **resumen** muchas filas en un solo valor: cuántos son, cuánto suman, cuál es el mayor... Son el "Excel" de SQL. Ejemplos ejecutables en el [playground](https://d1se0.github.io/sql-learning/).

***

## COUNT() — Contar filas

La función `COUNT()` devuelve el **número de filas** que coinciden con un criterio especificado.

`COUNT()` normalmente lleva `*` como parámetro, porque el nombre de la columna no suele importar: todas tienen el mismo conteo.

### Sintaxis

```sql
SELECT COUNT(column_name)
FROM table_name
WHERE condition;
```

### Ejemplo

Encuentra el número de pacientes que pesan más de 120 kg:

```sql
SELECT COUNT(*)
FROM patients
WHERE weight > 120;
```

> 💡 Variantes útiles: `COUNT(*)` cuenta todas las filas; `COUNT(columna)` solo las que tienen esa columna con valor no-NULL; `COUNT(DISTINCT columna)` las distintas.

***

## AVG() — Promedio

La función `AVG()` devuelve el **valor promedio** de una columna numérica.

### Sintaxis

```sql
SELECT AVG(column_name)
FROM table_name
WHERE condition;
```

### Ejemplo

Encuentra el peso promedio de los pacientes:

```sql
SELECT AVG(weight) FROM patients;
```

Con alias para que la columna tenga nombre bonito:

```sql
SELECT AVG(weight) AS average_weight FROM patients;
```

***

## SUM() — Suma total

La función `SUM()` devuelve la **suma total** de una columna numérica.

### Sintaxis

```sql
SELECT SUM(column_name)
FROM table_name
WHERE condition;
```

### Ejemplo

Encuentra la suma de los pesos de todos los pacientes:

```sql
SELECT SUM(weight) FROM patients;
```

***

## MAX() — Valor máximo

La función `MAX()` devuelve el **mayor valor** de la columna seleccionada.

### Sintaxis

```sql
SELECT MAX(column_name)
FROM table_name
WHERE condition;
```

### Ejemplo

Encuentra el mayor peso entre los pacientes:

```sql
SELECT MAX(weight) FROM patients;
```

> 💡 `MAX()` también funciona con texto y fechas: `MAX(birth_date)` da la fecha más reciente.

***

## MIN() — Valor mínimo

La función `MIN()` devuelve el **menor valor** de la columna seleccionada.

### Sintaxis

```sql
SELECT MIN(column_name)
FROM table_name
WHERE condition;
```

### Ejemplo

Encuentra el menor peso entre los pacientes:

```sql
SELECT MIN(weight) FROM patients;
```

***

## Combinando agregadas con GROUP BY y HAVING

El verdadero poder de las agregadas aparece al combinarlas con lo aprendido en el [capítulo 3](03-multi-tabla.md):

```sql
-- Peso promedio por provincia
SELECT province_id, AVG(weight) AS avg_weight
FROM patients
GROUP BY province_id;

-- Número de ingresos por diagnóstico, solo con más de 5 casos
SELECT diagnosis, COUNT(*) AS total
FROM admissions
GROUP BY diagnosis
HAVING COUNT(*) > 5
ORDER BY total DESC;

-- Altura máxima y mínima por sexo
SELECT gender, MAX(height), MIN(height)
FROM patients
GROUP BY gender;
```

> 🧠 **Recuerda:** toda columna del `SELECT` que NO esté dentro de una función agregada debe ir en el `GROUP BY`. Ej: si seleccionas `province_id, AVG(weight)` → `GROUP BY province_id`.

***

## 🧪 Mini-retos del capítulo

1. ¿Cuántas pacientes hay en total?
2. ¿Cuál es la altura media de los pacientes de sexo 'F'?
3. ¿Cuántos diagnósticos distintos hay en `admissions`?
4. La fecha de nacimiento del paciente más joven.
5. El diagnóstico más repetido (con su cantidad).

<details>

<summary>👀 Soluciones</summary>

```sql
-- 1
SELECT COUNT(*) FROM patients;
-- 2
SELECT AVG(height) AS avg_height FROM patients WHERE gender = 'F';
-- 3
SELECT COUNT(DISTINCT diagnosis) FROM admissions;
-- 4
SELECT MAX(birth_date) FROM patients;
-- 5
SELECT diagnosis, COUNT(*) AS total FROM admissions
GROUP BY diagnosis ORDER BY total DESC LIMIT 1;
```

</details>

## 📌 Resumen del capítulo

| Función   | Devuelve                              |
| --------- | ------------------------------------- |
| `COUNT()` | Número de filas                       |
| `AVG()`   | Media de una columna numérica         |
| `SUM()`   | Suma total de una columna numérica    |
| `MAX()`   | Valor máximo (números, texto, fechas) |
| `MIN()`   | Valor mínimo (números, texto, fechas) |

> 🔥 **Nota para hacking:** en extracción de datos con SQLi a ciegas, `COUNT(*)` se usa para saber cuántas tablas/columnas existen, y `MAX()`/`MIN()` para acotar valores carácter a carácter.

➡️ **Siguiente capítulo:** [Funciones de Utilidad](05-funciones-utilidad.md)
