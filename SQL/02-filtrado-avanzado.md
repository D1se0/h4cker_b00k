---
icon: magnifying-glass
---

# 3 · Filtrado Avanzado

> Ya sabes leer y filtrar con `WHERE`. Ahora aprendemos a filtrar con precisión quirúrgica: operadores lógicos, ordenación, patrones, listas, rangos y valores únicos. Ejemplos ejecutables en el [playground](https://d1se0.github.io/sql-learning/).

***

## AND, OR y NOT — Operadores lógicos

La cláusula `WHERE` se puede combinar con los operadores `AND`, `OR` y `NOT` para filtrar con más de una condición:

* **AND** muestra un registro si **TODAS** las condiciones son verdaderas.
* **OR** muestra un registro si **ALGUNA** de las condiciones es verdadera.
* **NOT** muestra un registro si la condición **NO** es verdadera.

### Sintaxis

```sql
-- AND
SELECT column1, column2, ...
FROM table_name
WHERE condition1 AND condition2 AND condition3 ...;

-- OR
SELECT column1, column2, ...
FROM table_name
WHERE condition1 OR condition2 OR condition3 ...;

-- NOT
SELECT column1, column2, ...
FROM table_name
WHERE NOT condition;
```

### Ejemplos

```sql
-- AND: nombre 'John' Y ciudad 'Toronto'
SELECT * FROM patients
WHERE first_name = 'John' AND city = 'Toronto';

-- OR: ciudad 'Hamilton' O 'Toronto'
SELECT * FROM patients
WHERE city = 'Hamilton' OR city = 'Toronto';

-- NOT: todo excepto la provincia 'ON' (Ontario)
SELECT * FROM patients
WHERE NOT province_id = 'ON';
```

> 💡 Puedes combinarlos con paréntesis para controlar el orden de evaluación:
>
> ```sql
> SELECT * FROM patients
> WHERE (city = 'Hamilton' OR city = 'Toronto')
>   AND gender = 'F';
> ```

***

## ORDER BY — Ordenar resultados

La palabra clave `ORDER BY` **ordena** el result-set de forma ascendente o descendente.

* Por defecto ordena **ascendente** (ASC, de la A a la Z / del 1 al 9).
* Con `DESC` ordena **descendente**.

### Sintaxis

```sql
SELECT column1, column2, ...
FROM table_name
ORDER BY column1, column2, ... ASC|DESC;
```

### Ejemplos

```sql
-- Orden ascendente por first_name (por defecto)
SELECT * FROM patients
ORDER BY first_name;

-- Orden descendente
SELECT * FROM patients
ORDER BY first_name DESC;

-- Ordenar por varias columnas: primero first_name,
-- y si hay empates, por last_name
SELECT * FROM patients
ORDER BY first_name, last_name;

-- Mezclado: first_name ascendente, last_name descendente
SELECT * FROM patients
ORDER BY first_name ASC, last_name DESC;
```

***

## LIKE — Búsqueda por patrón

El operador `LIKE` se usa en `WHERE` para buscar un **patrón** en una columna.

Hay dos comodines (wildcards) que se usan con `LIKE`:

| Comodín | Significado                                  |
| ------- | -------------------------------------------- |
| `%`     | Representa **cero, uno o varios** caracteres |
| `_`     | Representa **un solo** carácter              |

Se pueden combinar entre sí.

### Sintaxis

```sql
SELECT column1, column2, ...
FROM table_name
WHERE column LIKE pattern;
```

### Los patrones más usados

```sql
-- Empieza por "a"
WHERE first_name LIKE 'a%';
-- Termina en "a"
WHERE first_name LIKE '%a';
-- Contiene "or" en cualquier posición
WHERE first_name LIKE '%or%';
-- Tiene "r" en la segunda posición
WHERE first_name LIKE '_r%';
-- Empieza por "a" y tiene al menos 2 caracteres
WHERE first_name LIKE 'a_%';
-- Empieza por "a" y tiene al menos 3 caracteres
WHERE first_name LIKE 'a__%';
-- Empieza por "a" y termina en "o"
WHERE first_name LIKE 'a%o';
```

### Ejemplos completos

```sql
SELECT * FROM patients WHERE first_name LIKE 'a%';    -- empieza por 'a'
SELECT * FROM patients WHERE first_name LIKE '%a';    -- termina en 'a'
SELECT * FROM patients WHERE first_name LIKE '%or%';  -- contiene 'or'
SELECT * FROM patients WHERE first_name LIKE '_r%';   -- 'r' en 2ª posición
SELECT * FROM patients WHERE first_name LIKE 'a__%';  -- empieza por 'a', ≥3 caracteres
SELECT * FROM patients WHERE first_name LIKE 'a%o';   -- empieza por 'a', acaba en 'o'
SELECT * FROM patients WHERE first_name NOT LIKE 'a%';-- NO empieza por 'a'
```

> 🔥 **Nota para hacking:** `LIKE` esconde técnica. En inyecciones **blind SQLi** (capítulo 7) se usa `LIKE 'a%'` para adivinar contenido carácter a carácter cuando la web no muestra errores. Recuérdalo.

***

## IN — Filtrar por lista de valores

El operador `IN` permite especificar **múltiples valores** en un `WHERE`. Es un atajo de varias condiciones `OR`.

### Sintaxis

```sql
SELECT column_name(s)
FROM table_name
WHERE column_name IN (value1, value2, ...);
```

o con una **subconsulta** (un SELECT dentro de otro):

```sql
SELECT column_name(s)
FROM table_name
WHERE column_name IN (SELECT statement);
```

### Ejemplos

```sql
-- Pacientes de 'SK', 'AB' o 'MB'
SELECT * FROM patients
WHERE province_id IN ('SK', 'AB', 'MB');

-- Lo contrario: todos MENOS esas provincias
SELECT * FROM patients
WHERE province_id NOT IN ('SK', 'AB', 'MB');

-- Pacientes con el mismo first_name que algún doctor (subconsulta)
SELECT * FROM patients
WHERE first_name IN (SELECT first_name FROM doctors);
```

***

## BETWEEN — Filtrar por rango

El operador `BETWEEN` selecciona valores **dentro de un rango** (números, texto o fechas). Es **inclusivo**: los valores inicial y final se incluyen.

### Sintaxis

```sql
SELECT column_name(s)
FROM table_name
WHERE column_name BETWEEN value1 AND value2;
```

### Ejemplos

```sql
-- Pacientes con peso entre 100 y 120 (ambos incluidos)
SELECT * FROM patients
WHERE weight BETWEEN 100 AND 120;

-- NOT BETWEEN: fuera del rango
SELECT * FROM patients
WHERE weight NOT BETWEEN 100 AND 120;

-- Combinando con IN
SELECT * FROM patients
WHERE weight BETWEEN 100 AND 120
  AND province_id NOT IN ('ON', 'SK', 'AB');

-- BETWEEN con texto (compara por valor ASCII)
SELECT * FROM patients
WHERE first_name BETWEEN 'Alex' AND 'Ben';
```

> 💡 Con texto, la comparación usa el código ASCII: `'c'` (99) está entre `'a'` (97) y `'e'` (101), pero `'C'` (67) no, porque las mayúsculas van antes en la tabla ASCII.

***

## DISTINCT — Valores únicos

`SELECT DISTINCT` devuelve **solo valores distintos** (sin duplicados). En una tabla, una columna suele tener valores repetidos; a veces solo quieres listar los diferentes.

### Sintaxis

```sql
SELECT DISTINCT column1, column2, ...
FROM table_name;
```

### Ejemplos

```sql
-- Con duplicados
SELECT first_name FROM patients;

-- Sin duplicados
SELECT DISTINCT first_name FROM patients;

-- Contar cuántos nombres distintos hay
SELECT COUNT(DISTINCT first_name) FROM patients;
```

***

## 🧪 Mini-retos del capítulo

1. Lista los pacientes de sexo 'M' de 'Toronto' u 'Hamilton', ordenados por apellido descendente.
2. Busca pacientes cuyo nombre contenga "an" en cualquier posición.
3. Muestra las provincias distintas que hay en `patients` (sin repetir).
4. Pacientes con `patient_id` entre 10 y 20, excepto los de 'ON'.
5. Nombres de 4 letras exactas que empiecen por 'J' (pista: `___` con tres guiones bajos).

<details>

<summary>👀 Soluciones</summary>

```sql
-- 1
SELECT * FROM patients
WHERE gender = 'M' AND city IN ('Toronto', 'Hamilton')
ORDER BY last_name DESC;
-- 2
SELECT * FROM patients WHERE first_name LIKE '%an%';
-- 3
SELECT DISTINCT province_id FROM patients;
-- 4
SELECT * FROM patients
WHERE patient_id BETWEEN 10 AND 20 AND province_id <> 'ON';
-- 5
SELECT * FROM patients WHERE first_name LIKE 'J___';
```

</details>

## 📌 Resumen del capítulo

| Herramienta          | Para qué                                      |
| -------------------- | --------------------------------------------- |
| `AND` / `OR` / `NOT` | Combinar o invertir condiciones               |
| `ORDER BY`           | Ordenar (ASC por defecto, DESC para invertir) |
| `LIKE` + `%` `_`     | Buscar por patrones                           |
| `IN` / `NOT IN`      | Coincidir contra una lista o subconsulta      |
| `BETWEEN`            | Rango inclusivo (números, texto, fechas)      |
| `DISTINCT`           | Eliminar duplicados del resultado             |

➡️ **Siguiente capítulo:** [Consultas Multi-Tabla](03-multi-tabla.md)
