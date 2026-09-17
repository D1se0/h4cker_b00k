---
icon: database
---

# 1 · Fundamentos: Bases de Datos y SQL

> Si nunca has tocado una base de datos, empieza aquí. Este capítulo te da las bases conceptuales para entender todo lo que viene después.

***

## ¿Qué es una Base de Datos?

Una **base de datos (BD)** es un sistema organizado para **almacenar datos** de forma que se puedan guardar, buscar, actualizar y borrar de manera eficiente.

Piensa en un hospital: necesita guardar miles de pacientes, sus ingresos, sus médicos... Todo eso vive en una base de datos. Instagram guarda tus fotos y seguidores, tu banco guarda tus movimientos, un videojuego guarda tu inventario. **Todo usa bases de datos.**

### Tipos de bases de datos

* **Relacionales (SQL)**: los datos se guardan en **tablas** relacionadas entre sí. Ejemplos: MySQL, PostgreSQL, SQLite, SQL Server, Oracle, MariaDB.
* **No relacionales (NoSQL)**: los datos se guardan en otros formatos (documentos, clave-valor, grafos). Ejemplos: MongoDB, Redis, Cassandra.

> 🎯 Esta guía se centra en las **relacionales**, que son las más usadas y el objetivo principal de las inyecciones SQL.

## ¿Qué es SQL?

**SQL = Structured Query Language** (Lenguaje de Consulta Estructurado).

Es el lenguaje estándar (definido por ANSI/ISO) para hablar con bases de datos relacionales. Con SQL puedes:

| Operación            | Verbo SQL |
| -------------------- | --------- |
| Leer datos           | `SELECT`  |
| Insertar datos       | `INSERT`  |
| Modificar datos      | `UPDATE`  |
| Borrar datos         | `DELETE`  |
| Crear tablas/bases   | `CREATE`  |
| Modificar estructura | `ALTER`   |
| Borrar tablas        | `DROP`    |

> 💡 **Dato clave para hacking:** SQL es un lenguaje **declarativo**: tú dices _qué_ quieres, no _cómo_ hacerlo. Esto significa que las consultas se construyen como frases: `SELECT ... FROM ... WHERE ...`. Entender esta estructura es lo que te permitirá entender las inyecciones SQL del capítulo 7.

## Bases de Datos Relacionales: conceptos clave

### Tabla

Una **tabla** es una estructura con **filas** (registros) y **columnas** (campos). Cada tabla representa un tipo de entidad: pacientes, pedidos, usuarios...

```sql
-- Una tabla "patients" se ve así por dentro:
-- | patient_id | first_name | last_name | gender | city     |
-- |------------|------------|-----------|--------|----------|
-- | 1          | Miyuki     | Riviera   | F      | Toronto  |
-- | 2          | Deunan     | Knute     | F      | Hamilton |
-- | 3          | Lois       | McAllister| F      | London   |
```

* **Fila (row/record)**: un registro completo. Ej: el paciente nº 1.
* **Columna (column/field)**: un dato de cada registro. Ej: `first_name`.
* **Celda**: la intersección de una fila y una columna. Ej: "Miyuki".

### Clave Primaria — Primary Key (PK)

La **PRIMARY KEY** es la columna (o combinación de columnas) que identifica **de forma única** cada fila. No puede repetirse ni ser `NULL`. Ej: `patient_id`.

### Clave Foránea — Foreign Key (FK)

La **FOREIGN KEY** es una columna que apunta a la PK de **otra tabla**, creando la relación entre ambas. Ej: `admissions.patient_id` apunta a `patients.patient_id`.

```sql
-- Relación entre tablas:
-- patients (padre)          admissions (hija)
-- | patient_id (PK) |       | admission_id (PK) | patient_id (FK) | diagnosis |
-- | 1               |  ←--- | 1                 | 1               | Pregnancy |
-- | 2               |       | 2                 | 2               | Anxiety   |
```

Gracias a las FK evitamos duplicar datos: no repetimos los datos del paciente en cada ingreso, solo su `id`.

### Relaciones entre tablas

* **1 a 1 (1:1)**: una fila de A se relaciona con una de B.
* **1 a muchos (1:N)**: un paciente tiene muchos ingresos. La más común.
* **Muchos a muchos (N:M)**: se resuelve con una tabla intermedia.

### ¿Qué es un NULL?

`NULL` significa "**sin valor**". No es `0` ni una cadena vacía: es _ausencia de dato_. Se estudia a fondo en el capítulo 3.

## Dialectos de SQL

SQL es estándar, pero cada motor tiene pequeñas diferencias de sintaxis (funciones, tipos de datos, etc.):

| Motor                  | Uso típico                                    | Nota                                    |
| ---------------------- | --------------------------------------------- | --------------------------------------- |
| **MySQL / MariaDB**    | Webs con PHP, WordPress                       | El más visto en pentesting web          |
| **PostgreSQL**         | Apps modernas, backend Python/Node            | Muy completo                            |
| **SQLite**             | Apps móviles, browsers, dispositivos pequeños | Archivo único, el que usa el playground |
| **SQL Server (MSSQL)** | Entornos Microsoft/empresariales              | Funciones como `ISNULL()`               |
| **Oracle**             | Banca, corporaciones                          | Usa secuencias para auto-increment      |

> 💡 En esta guía los ejemplos son compatibles con la mayoría, y donde un motor difiere se indica con comentarios `-- MySQL`, `-- SQL Server`, etc.

## 🖥️ Instala tu entorno de práctica

### Opción 1: Playground online (sin instalar nada) ✅ Recomendada para empezar

Usa tu propia web: [SQL Learning Playground](https://d1se0.github.io/sql-learning/)

* SQLite real corriendo en el navegador.
* Base de datos de hospital (`patients`, `admissions`, `doctors`) ya cargada.
* Buscador de comandos y retos.

### Opción 2: SQLite local (un solo archivo)

```bash
# Instalar
sudo apt install sqlite3        # Debian/Ubuntu/Kali
brew install sqlite3            # macOS

# Crear y abrir una base de datos
sqlite3 prueba.db

# Comandos útiles dentro de sqlite3
.help        -- ayuda
.tables      -- listar tablas
.headers on  -- mostrar cabeceras de columnas
.mode column -- salida alineada
.quit        -- salir
```

### Opción 3: MySQL local (lo típico en servidores web y CTFs)

```bash
# Instalar (Kali/Debian/Ubuntu)
sudo apt install mysql-server
sudo systemctl start mysql

# Entrar como root
sudo mysql -u root -p
```

```sql
-- Dentro de MySQL: crear una base y usarla
CREATE DATABASE hospital;
USE hospital;
SHOW TABLES;      -- listar tablas
DESCRIBE patients; -- ver columnas de una tabla
```

### Opción 4: Docker (laboratorio limpio al instante)

```bash
# MySQL en docker
docker run --name mysql-prac -e MYSQL_ROOT_PASSWORD=mi_clave -p 3306:3306 -d mysql:8
docker exec -it mysql-prac mysql -u root -p
```

## 🧪 Tu primera consulta

Ya sea en el playground, sqlite3 o MySQL, escribe esto y ejecútalo:

```sql
SELECT * FROM patients;
```

🎉 Eso es SQL: "_dame todas las columnas (`*`) de la tabla `patients`_". Si has visto resultados, ya estás haciendo SQL.

```sql
-- Prueba también estas dos:
SELECT first_name, last_name FROM patients;

SELECT * FROM patients WHERE city = 'Toronto';
```

## 📌 Resumen del capítulo

* Una **BD relacional** guarda datos en **tablas** (filas + columnas).
* **PK** identifica cada fila; **FK** conecta tablas entre sí.
* **SQL** es el lenguaje para leer (`SELECT`), escribir (`INSERT`, `UPDATE`, `DELETE`) y estructurar (`CREATE`, `ALTER`, `DROP`).
* Hay varios **dialectos** (MySQL, SQLite, SQL Server...), pero el 90% es igual.
* Practica desde ya en el [playground](https://d1se0.github.io/sql-learning/).

➡️ **Siguiente capítulo:** [Query Basics — Tus Primeras Consultas](01-query-basics.md)
