# 📖 Capítulo 1 — Query Basics: Tus Primeras Consultas

> Aquí aprendes las 5 sentencias que usarás el 90% del tiempo: `SELECT`, `WHERE`, `INSERT`, `UPDATE` y `DELETE`. Todas las tablas de ejemplo son las del hospital (`patients`, `admissions`, `doctors`) del [playground](https://d1se0.github.io/sql-learning/).

---

## SELECT — Leer datos

La sentencia `SELECT` se usa para **seleccionar datos de una base de datos**. Los datos devueltos se guardan en una tabla de resultados llamada **result-set**.

### Sintaxis

```sql
SELECT column1, column2, ...
FROM tablename;
```

Aquí `column1`, `column2`, ... son los nombres de los campos de la tabla de los que quieres sacar datos. Si quieres **todas** las columnas, usa `*`:

```sql
SELECT * FROM tablename;
```

> 💡 `SELECT *` es cómodo para explorar, pero en código real conviene seleccionar solo las columnas necesarias: es más rápido y más seguro.

### Ejemplo: seleccionar columnas concretas

La siguiente consulta selecciona las columnas `first_name` y `last_name` de la tabla `patients`:

```sql
SELECT first_name, last_name FROM patients;
```

### Ejemplo: seleccionar todas las columnas

```sql
SELECT * FROM patients;
```

---

## WHERE — Filtrar registros

La cláusula `WHERE` se usa para **filtrar registros**: extrae solo las filas que cumplen una condición.

### Sintaxis

```sql
SELECT column1, column2, ...
FROM tablename
WHERE condition;
```

### Ejemplo

Selecciona todos los pacientes con sexo "F":

```sql
SELECT * FROM patients
WHERE gender = 'F';
```

### ⚠️ Texto vs números (¡muy importante!)

- Los **valores de texto** van entre **comillas simples**: `'Toronto'`.
- Los **valores numéricos** van **sin comillas**: `1`.

```sql
-- Texto: con comillas
SELECT * FROM patients WHERE city = 'Hamilton';

-- Número: sin comillas
SELECT * FROM patients WHERE patient_id = 1;
```

### Operadores disponibles en WHERE

| Operador | Significado | Ejemplo |
|----------|-------------|---------|
| `=` | Igual | `WHERE patient_id = 1` |
| `>` | Mayor que | `WHERE patient_id > 5` |
| `<` | Menor que | `WHERE patient_id < 5` |
| `>=` | Mayor o igual | `WHERE patient_id >= 5` |
| `<=` | Menor o igual | `WHERE patient_id <= 5` |
| `<>` | Distinto | `WHERE patient_id <> 5` |
| `BETWEEN` | En un rango inclusivo | `WHERE patient_id BETWEEN 4 AND 6` |
| `LIKE` | Búsqueda por patrón | `WHERE first_name LIKE 'a%'` |
| `IN` | En una lista de valores | `WHERE patient_id IN (1, 3, 6, 9)` |

Ejemplos de todos:

```sql
SELECT * FROM patients WHERE patient_id = 1;   -- igual
SELECT * FROM patients WHERE patient_id > 5;   -- mayor que
SELECT * FROM patients WHERE patient_id < 5;   -- menor que
SELECT * FROM patients WHERE patient_id >= 5;  -- mayor o igual
SELECT * FROM patients WHERE patient_id <= 5;  -- menor o igual
SELECT * FROM patients WHERE patient_id <> 5;  -- distinto (no sale el paciente 5)
SELECT * FROM patients WHERE patient_id BETWEEN 4 AND 6;  -- rango inclusivo
SELECT * FROM patients WHERE first_name LIKE 'a%';  -- nombres que empiezan por 'a'
SELECT * FROM patients WHERE patient_id IN (1, 3, 6, 9);  -- los valores pueden ser una subconsulta
```

> 🔗 `LIKE`, `IN`, `BETWEEN` y los operadores lógicos se explican a fondo en el [capítulo 2](./02-filtrado-avanzado.md).

---

## INSERT — Insertar registros

La sentencia `INSERT INTO` se usa para **insertar nuevos registros** en una tabla.

### Sintaxis (2 formas)

**1. Especificando columnas y valores** (la recomendada):

```sql
INSERT INTO tablename (column1, column2, column3, ...)
VALUES (value1, value2, value3, ...);
```

**2. Sin especificar columnas** (solo si vas a dar valor a TODAS las columnas, en el orden exacto de la tabla):

```sql
INSERT INTO tablename
VALUES (value1, value2, value3, ...);
```

### Ejemplo: insertar un registro completo

```sql
INSERT INTO patients (first_name, last_name, gender, birth_date, city, province_id, allergies, weight, height)
VALUES ('John', 'Smith', 'M', '1994-02-21', 'Hamilton', 'ON', NULL, 132, 182);

-- Comprobar el registro insertado (el último id)
SELECT * FROM patients
WHERE patient_id = (SELECT MAX(patient_id) FROM patients);
```

### Ejemplo: insertar solo en algunas columnas

Si una columna admite `NULL`, puedes omitirla en el `INSERT`:

```sql
INSERT INTO patients (first_name, last_name, gender)
VALUES ('Jane', 'Doe', 'F');

SELECT * FROM patients
WHERE patient_id = (SELECT MAX(patient_id) FROM patients);
```

> 💡 Si la columna no admite NULL y no tiene valor por defecto (`DEFAULT`), el INSERT fallará. Esto se ve en el [capítulo 6](./06-tablas-ddl.md).

---

## UPDATE — Modificar registros

La sentencia `UPDATE` se usa para **modificar registros existentes**.

### Sintaxis

```sql
UPDATE tablename
SET column1 = value1, column2 = value2, ...
WHERE condition;
```

> ⚠️ **Cuidado:** si olvidas el `WHERE`, ¡se actualizan **TODAS** las filas de la tabla! Esta es también la base de un ataque real: modificar datos de una web vulnerable vía inyección SQL.

### Ejemplo: actualizar un registro

Actualiza el paciente con `patient_id = 1` con un nuevo nombre y peso:

```sql
UPDATE patients
SET
  first_name = 'John',
  weight = 120
WHERE patient_id = 1;

-- Ver el resultado
SELECT * FROM patients WHERE patient_id = 1;
```

### Ejemplo: actualizar varios registros

Es el `WHERE` el que determina cuántas filas se actualizan. Aquí se pone `'NKA'` (no known allergies) a todos los pacientes que tienen `allergies` en `NULL`:

```sql
UPDATE patients
SET allergies = 'NKA'
WHERE allergies IS NULL;

SELECT * FROM patients;
```

---

## DELETE — Borrar registros

La sentencia `DELETE` se usa para **borrar registros existentes**.

### Sintaxis

```sql
DELETE FROM tablename WHERE condition;
```

> ⚠️ **Cuidado:** si omites el `WHERE`, se borran **TODAS** las filas. Revisa siempre el `WHERE` antes de ejecutar.

### Ejemplo

Borra todos los pacientes llamados "Paul":

```sql
DELETE FROM patients WHERE first_name = 'Paul';

-- Comprobar que ya no quedan 'Paul'
SELECT * FROM patients WHERE first_name = 'Paul';
```

> 💡 `DELETE` borra filas, no la tabla. Para borrar la tabla entera se usa `DROP TABLE` (capítulo 6), y para vaciarla manteniendo la estructura, `TRUNCATE TABLE`.

---

## 🧪 Mini-retos del capítulo

Hazlos en el [playground](https://d1se0.github.io/sql-learning/) sin mirar la solución:

1. Muestra solo el nombre y apellido de todos los pacientes.
2. Muestra todos los datos de las pacientes de sexo 'F' de la ciudad 'Hamilton'.
3. Inserta un paciente nuevo con tu nombre.
4. Actualiza el peso de tu paciente a 75.
5. Borra tu paciente.

<details>
<summary>👀 Soluciones</summary>

```sql
-- 1
SELECT first_name, last_name FROM patients;
-- 2
SELECT * FROM patients WHERE gender = 'F' AND city = 'Hamilton';
-- 3
INSERT INTO patients (first_name, last_name, gender) VALUES ('Tú', 'Mismo', 'M');
-- 4
UPDATE patients SET weight = 75 WHERE first_name = 'Tú';
-- 5
DELETE FROM patients WHERE first_name = 'Tú';
```
</details>

## 📌 Resumen del capítulo

| Sentencia | Para qué | Punto clave |
|-----------|----------|-------------|
| `SELECT` | Leer datos | `*` = todas las columnas |
| `WHERE` | Filtrar | Texto con `'comillas'`, números sin |
| `INSERT INTO` | Crear filas | Especifica siempre las columnas |
| `UPDATE` | Modificar filas | Sin `WHERE` actualizas todo ⚠️ |
| `DELETE` | Borrar filas | Sin `WHERE` borras todo ⚠️ |

➡️ **Siguiente capítulo:** [Filtrado Avanzado](./02-filtrado-avanzado.md)
