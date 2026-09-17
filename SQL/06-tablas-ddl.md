# 🏗️ Capítulo 6 — Tablas y DDL: Diseño de la Base de Datos

> Hasta ahora has manipulado datos dentro de tablas existentes (DML). Ahora pasas al **DDL (Data Definition Language)**: crear, modificar y borrar la **estructura** de la base de datos. Ejemplos en el [playground](https://d1se0.github.io/sql-learning/).

---

## Tipos de datos (Data Types)

El **tipo de dato** de una columna define qué valores puede almacenar: enteros, texto, dinero, fecha/hora, binario y más.

> ⚠️ Los tipos varían entre bases de datos. Estas son las tablas de referencia para MySQL, SQL Server y MS Access.

### MySQL

**Cadenas (String):**

| Tipo | Descripción |
|------|-------------|
| `CHAR(size)` | Cadena de longitud fija, 0-255 caracteres |
| `VARCHAR(size)` | Cadena de longitud variable, hasta 65535 caracteres |
| `BINARY(size)` / `VARBINARY(size)` | Binarios de longitud fija / variable |
| `TINYTEXT` / `TINYBLOB` | Máx. 255 bytes / caracteres |
| `TEXT` / `BLOB` | Máx. 65535 bytes / caracteres |
| `MEDIUMTEXT` / `MEDIUMBLOB` | Máx. 16.777.215 bytes / caracteres |
| `LONGTEXT` / `LONGBLOB` | Máx. 4.294.967.295 bytes / caracteres |
| `ENUM` / `SET` | Listas predefinidas de valores |

**Numéricos:**

| Tipo | Descripción |
|------|-------------|
| `TINYINT` / `SMALLINT` / `MEDIUMINT` / `INT` / `INTEGER` / `BIGINT` | Enteros con varios rangos |
| `FLOAT` / `DOUBLE` / `DECIMAL` | Punto flotante y numéricos exactos |
| `BIT` | Valores de bit, 1-64 bits |
| `BOOL` / `BOOLEAN` | Verdadero/Falso |

**Fecha y hora:**

| Tipo | Formato |
|------|---------|
| `DATE` | `YYYY-MM-DD` |
| `DATETIME` / `TIMESTAMP` | Fecha y hora |
| `TIME` | Solo hora |
| `YEAR` | Año de 4 dígitos |

### SQL Server

| Categoría | Tipos |
|-----------|-------|
| Cadenas | `char(n)`, `varchar(n)`, `varchar(max)`, `text`, `nchar`, `nvarchar(n)`, `nvarchar(max)`, `ntext` |
| Numéricos | `bit`, `tinyint`, `smallint`, `int`, `bigint`, `decimal(p,s)`, `numeric(p,s)`, `smallmoney`, `money`, `float(n)`, `real` |
| Fecha/Hora | `datetime`, `datetime2`, `smalldatetime`, `date`, `time`, `datetimeoffset`, `timestamp` |
| Otros | `sql_variant`, `uniqueidentifier`, `xml`, `cursor`, `table` |

### MS Access

`Text`, `Memo`, `Byte`, `Integer`, `Long`, `Single`, `Double`, `Currency`, `AutoNumber`, `Date/Time`, `Yes/No`, `Ole Object`, `Hyperlink`, `Lookup Wizard`.

> 🔥 **Nota para hacking:** reconocer tipos de datos te ayuda a entender errores de SQLi. Un clásico: si la web concatena `id` en una consulta sin comillas, es probable que el campo sea numérico → la inyección va sin comillas (`AND 1=1`); si va entre comillas, hay que cerrarlas (`' AND 1=1-- -`).

---

## Constraints — Restricciones

Las **constraints** (restricciones) de SQL se usan para **especificar reglas para los datos** de una tabla.

Se pueden especificar:
- Al crear la tabla → `CREATE TABLE`.
- Después de crearla → `ALTER TABLE`.

### Sintaxis

```sql
CREATE TABLE table_name (
  column1 datatype constraint,
  column2 datatype constraint,
  column3 datatype constraint,
  ....
);
```

### Las constraints principales

| Constraint | Qué garantiza |
|------------|---------------|
| `NOT NULL` | La columna no puede tener valor `NULL` |
| `UNIQUE` | Todos los valores de la columna son distintos |
| `PRIMARY KEY` | Combinación de NOT NULL + UNIQUE. Identifica cada fila |
| `FOREIGN KEY` | Evita acciones que destruyan los enlaces entre tablas |
| `CHECK` | Los valores cumplen una condición específica |
| `DEFAULT` | Valor por defecto si no se especifica otro |

Las constraints pueden ser **de columna** (afectan a una columna) o **de tabla** (afectan a toda la tabla).

> 🧠 Si se viola una constraint, la acción se **aborta**: la base de datos rechaza la operación. Esto es la "integridad de los datos" y es lo que un atacante intenta *sortear* cuando explota una inyección SQL (por ejemplo, actualizando la tabla de usuarios directamente).

---

## CREATE TABLE — Crear tablas

La sentencia `CREATE TABLE` se usa para **crear una nueva tabla** en la base de datos.

### Sintaxis

```sql
CREATE TABLE table_name (
  column1 datatype,
  column2 datatype,
  column3 datatype,
  ...
);
```

Cada columna necesita: **nombre** + **tipo de dato** (y opcionalmente constraints).

### Ejemplo

Crear una tabla `Persons` con 5 columnas:

```sql
CREATE TABLE Persons (
  PersonID int,
  LastName varchar(255),
  FirstName varchar(255),
  Address varchar(255),
  City varchar(255)
);
```

### Crear una tabla a partir de otra

Puedes crear una tabla nueva **como copia** de una existente (todas o solo algunas columnas):

```sql
CREATE TABLE new_table_name AS
SELECT column1, column2, ...
FROM existing_table_name
WHERE ...;
```

Ejemplo: copiar columnas seleccionadas de `patients`:

```sql
CREATE TABLE TestPatients AS
SELECT patient_id, first_name, last_name
FROM patients;

-- Verificar la nueva tabla
SELECT * FROM TestPatients;
```

---

## PRIMARY KEY — Clave primaria

La constraint `PRIMARY KEY` **identifica de forma única** cada registro de una tabla.

- Los valores deben ser **UNIQUE** y no pueden ser **NULL**.
- Una tabla solo puede tener **UNA** primary key, que puede ser de una o varias columnas.

### En CREATE TABLE

```sql
-- MySQL
CREATE TABLE Persons (
  ID int NOT NULL,
  LastName varchar(255) NOT NULL,
  FirstName varchar(255),
  Age int,
  PRIMARY KEY (ID)
);
```

```sql
-- SQL Server / Oracle / MS Access
CREATE TABLE Persons (
  ID int NOT NULL PRIMARY KEY,
  LastName varchar(255) NOT NULL,
  FirstName varchar(255),
  Age int
);
```

Con nombre propio y múltiples columnas:

```sql
CREATE TABLE Persons (
  ID int NOT NULL,
  LastName varchar(255) NOT NULL,
  FirstName varchar(255),
  Age int,
  CONSTRAINT PK_Person PRIMARY KEY (ID, LastName)
);
```

### En ALTER TABLE

```sql
ALTER TABLE Persons
ADD PRIMARY KEY (ID);

-- Con nombre / múltiples columnas
ALTER TABLE Persons
ADD CONSTRAINT PK_Person PRIMARY KEY (ID, LastName);
```

> ⚠️ Si añades la PK con `ALTER TABLE`, la columna debió declararse `NOT NULL` al crear la tabla.

### Eliminar la PK

```sql
-- MySQL
ALTER TABLE Persons
DROP PRIMARY KEY;

-- SQL Server / Oracle / MS Access
ALTER TABLE Persons
DROP CONSTRAINT PK_Person;
```

---

## FOREIGN KEY — Clave foránea

La constraint `FOREIGN KEY` **evita acciones que destruyan los enlaces entre tablas**.

- Una FK es un campo (o conjunto de campos) de una tabla que apunta a la **PRIMARY KEY** de otra.
- La tabla con la FK se llama tabla **hija**; la tabla con la PK referenciada es la tabla **padre**.
- Evita insertar datos inválidos en la columna FK: el valor **debe existir** en la tabla padre.

### En CREATE TABLE

```sql
-- MySQL
CREATE TABLE Orders (
  OrderID int NOT NULL,
  OrderNumber int NOT NULL,
  PersonID int,
  PRIMARY KEY (OrderID),
  FOREIGN KEY (PersonID) REFERENCES Persons(PersonID)
);
```

```sql
-- SQL Server / Oracle / MS Access
CREATE TABLE Orders (
  OrderID int NOT NULL PRIMARY KEY,
  OrderNumber int NOT NULL,
  PersonID int FOREIGN KEY REFERENCES Persons(PersonID)
);
```

Con nombre propio:

```sql
CREATE TABLE Orders (
  OrderID int NOT NULL,
  OrderNumber int NOT NULL,
  PersonID int,
  PRIMARY KEY (OrderID),
  CONSTRAINT FK_PersonOrder FOREIGN KEY (PersonID)
    REFERENCES Persons(PersonID)
);
```

### En ALTER TABLE

```sql
ALTER TABLE Orders
ADD FOREIGN KEY (PersonID) REFERENCES Persons(PersonID);

-- Con nombre
ALTER TABLE Orders
ADD CONSTRAINT FK_PersonOrder
FOREIGN KEY (PersonID) REFERENCES Persons(PersonID);
```

### Eliminar la FK

```sql
-- MySQL
ALTER TABLE Orders
DROP FOREIGN KEY FK_PersonOrder;

-- SQL Server / Oracle / MS Access
ALTER TABLE Orders
DROP CONSTRAINT FK_PersonOrder;
```

---

## UNIQUE — Valores únicos

La constraint `UNIQUE` garantiza que **todos los valores de una columna sean diferentes**.

- `UNIQUE` y `PRIMARY KEY` dan garantía de unicidad, pero: una tabla tiene **solo una PK** y puede tener **muchas UNIQUE**.
- Una `PRIMARY KEY` lleva automáticamente una constraint `UNIQUE`.

### En CREATE TABLE

```sql
-- SQL Server / Oracle / MS Access
CREATE TABLE Persons (
  ID int NOT NULL UNIQUE,
  LastName varchar(255) NOT NULL,
  FirstName varchar(255),
  Age int
);

-- MySQL (sintaxis alternativa)
CREATE TABLE Persons (
  ID int NOT NULL,
  LastName varchar(255) NOT NULL,
  FirstName varchar(255),
  Age int,
  UNIQUE (ID)
);
```

Con nombre o en varias columnas:

```sql
CREATE TABLE Persons (
  ID int NOT NULL,
  LastName varchar(255) NOT NULL,
  FirstName varchar(255),
  Age int,
  CONSTRAINT UC_Person UNIQUE (ID, LastName)
);
```

### En ALTER TABLE

```sql
ALTER TABLE Persons
ADD UNIQUE (ID);

-- Con nombre / múltiples columnas
ALTER TABLE Persons
ADD CONSTRAINT UC_Person UNIQUE (ID, LastName);
```

### Eliminar la UNIQUE

```sql
-- MySQL
ALTER TABLE Persons
DROP INDEX UC_Person;

-- SQL Server / Oracle / MS Access
ALTER TABLE Persons
DROP CONSTRAINT UC_Person;
```

---

## NOT NULL — Valores obligatorios

Por defecto, una columna puede contener `NULL`. La constraint `NOT NULL` **obliga a que la columna NO acepte valores NULL**: no podrás insertar ni actualizar un registro sin dar valor a ese campo.

### En CREATE TABLE

```sql
CREATE TABLE Persons (
  ID int NOT NULL,
  LastName varchar(255) NOT NULL,
  FirstName varchar(255) NOT NULL,
  Age int
);
```

### En ALTER TABLE

```sql
ALTER TABLE Persons
MODIFY Age int NOT NULL;
```

---

## CHECK — Validar condiciones

La constraint `CHECK` **limita el rango de valores** que puede almacenar una columna.

- Si defines un `CHECK` en una columna, solo se permiten ciertos valores en ella.
- Si lo defines en la tabla, puede limitar valores de unas columnas según otras de la misma fila.

### En CREATE TABLE

```sql
-- MySQL
CREATE TABLE Persons (
  ID int NOT NULL,
  LastName varchar(255) NOT NULL,
  FirstName varchar(255),
  Age int,
  CHECK (Age >= 18)
);
```

```sql
-- SQL Server / Oracle / MS Access
CREATE TABLE Persons (
  ID int NOT NULL,
  LastName varchar(255) NOT NULL,
  FirstName varchar(255),
  Age int CHECK (Age >= 18)
);
```

Con nombre o en varias columnas:

```sql
CREATE TABLE Persons (
  ID int NOT NULL,
  LastName varchar(255) NOT NULL,
  FirstName varchar(255),
  Age int,
  City varchar(255),
  CONSTRAINT CHK_Person CHECK (Age >= 18 AND City = 'Sandnes')
);
```

### En ALTER TABLE

```sql
ALTER TABLE Persons
ADD CHECK (Age >= 18);

-- Con nombre / varias columnas
ALTER TABLE Persons
ADD CONSTRAINT CHK_PersonAge CHECK (Age >= 18 AND City = 'Sandnes');
```

### Eliminar el CHECK

```sql
-- MySQL
ALTER TABLE Persons
DROP CHECK CHK_PersonAge;

-- SQL Server / Oracle / MS Access
ALTER TABLE Persons
DROP CONSTRAINT CHK_PersonAge;
```

---

## DEFAULT — Valores por defecto

La constraint `DEFAULT` se usa para fijar un **valor por defecto** para una columna: se añadirá a todos los registros nuevos si no se especifica otro valor.

### En CREATE TABLE

```sql
CREATE TABLE Persons (
  ID int NOT NULL,
  LastName varchar(255) NOT NULL,
  FirstName varchar(255),
  Age int,
  City varchar(255) DEFAULT 'Sandnes'
);
```

También puede usar valores del sistema, como la fecha actual:

```sql
CREATE TABLE Orders (
  ID int NOT NULL,
  OrderNumber int NOT NULL,
  OrderDate date DEFAULT CURRENT_TIMESTAMP
);

-- El INSERT sin OrderDate toma el valor por defecto
INSERT INTO Orders (ID, OrderNumber) VALUES (1, 1);
SELECT * FROM Orders;
```

### En ALTER TABLE

```sql
-- MySQL
ALTER TABLE Persons
ALTER City SET DEFAULT 'Sandnes';

-- SQL Server
ALTER TABLE Persons
ADD CONSTRAINT df_City DEFAULT 'Sandnes' FOR City;

-- MS Access
ALTER TABLE Persons
ALTER COLUMN City SET DEFAULT 'Sandnes';

-- Oracle
ALTER TABLE Persons
MODIFY City DEFAULT 'Sandnes';
```

### Eliminar el DEFAULT

```sql
-- MySQL
ALTER TABLE Persons
ALTER City DROP DEFAULT;

-- SQL Server / Oracle / MS Access
ALTER TABLE Persons
ALTER COLUMN City DROP DEFAULT;
```

---

## AUTO INCREMENT — Contador automático

El auto-incremento genera un **número único automáticamente** cada vez que se inserta un nuevo registro. Normalmente se usa en el campo **primary key**.

La sintaxis cambia **muchísimo** según el motor (¡repásalo!):

### MySQL

```sql
CREATE TABLE Persons (
  Personid int NOT NULL AUTO_INCREMENT,
  LastName varchar(255) NOT NULL,
  FirstName varchar(255),
  Age int,
  PRIMARY KEY (Personid)
);

-- Empezar el contador en otro valor
ALTER TABLE Persons AUTO_INCREMENT = 100;

-- Insertar sin indicar Personid (se genera solo)
INSERT INTO Persons (FirstName, LastName)
VALUES ('Lars', 'Monsen');
```

### SQL Server

```sql
CREATE TABLE Persons (
  Personid int IDENTITY(1,1) PRIMARY KEY,
  LastName varchar(255) NOT NULL,
  FirstName varchar(255),
  Age int
);
-- IDENTITY(seed, incremento): IDENTITY(10,5) empieza en 10 y suma 5

INSERT INTO Persons (FirstName, LastName)
VALUES ('Lars', 'Monsen');
```

### MS Access

```sql
CREATE TABLE Persons (
  Personid AUTOINCREMENT PRIMARY KEY,
  LastName varchar(255) NOT NULL,
  FirstName varchar(255),
  Age int
);
-- AUTOINCREMENT(10,5) para empezar en 10 e incrementar de 5 en 5

INSERT INTO Persons (FirstName, LastName)
VALUES ('Lars', 'Monsen');
```

### Oracle

Oracle usa un objeto **secuencia**:

```sql
-- Crear la secuencia
CREATE SEQUENCE seq_person
  MINVALUE 1
  START WITH 1
  INCREMENT BY 1
  CACHE 10;

-- Insertar usando nextval
INSERT INTO Persons (Personid, FirstName, LastName)
VALUES (seq_person.nextval, 'Lars', 'Monsen');
```

> 🔥 **Nota para hacking:** reconocer el patrón de auto-increment te ayuda en SQLi: si los `id` de una web son 1, 2, 3..., es una columna auto-increment, y `UPDATE`/`DELETE` sin `WHERE` (o con el `WHERE` troyanizado por una inyección) afectan a todo.

---

## Índices (CREATE INDEX)

La sentencia `CREATE INDEX` se usa para **crear índices** en las tablas. Los índices ayudan a **recuperar datos más rápido** (como el índice de un libro).

- Los usuarios no ven los índices: solo se usan para acelerar búsquedas y consultas.
- ⚠️ Actualizar una tabla con índices cuesta más tiempo (hay que actualizar también el índice). Solo crea índices en columnas que se busquen **frecuentemente**.

### Crear un índice

```sql
-- Índice normal (se permiten duplicados)
CREATE INDEX index_name
ON table_name (column1, column2, ...);

-- Índice único (no se permiten duplicados)
CREATE UNIQUE INDEX index_name
ON table_name (column1, column2, ...);
```

**Ejemplos:**

```sql
-- Índice sobre last_name
CREATE INDEX idx_last_name
ON patients (last_name);

-- Índice sobre dos columnas
CREATE INDEX idx_pname
ON patients (last_name, first_name);
```

### Borrar un índice (DROP INDEX)

La sintaxis depende del motor:

```sql
-- MS Access
DROP INDEX index_name ON table_name;

-- SQL Server
DROP INDEX table_name.index_name;

-- DB2 / Oracle
DROP INDEX index_name;

-- MySQL
ALTER TABLE table_name
DROP INDEX index_name;
```

---

## ALTER TABLE — Modificar tablas

La sentencia `ALTER TABLE` se usa para **añadir, borrar o modificar columnas** de una tabla existente, y para añadir o quitar constraints.

### Añadir una columna

```sql
ALTER TABLE table_name
ADD column_name datatype;
```

Ejemplo: añadir "email" a `patients`:

```sql
ALTER TABLE patients
ADD email varchar(255);

SELECT patient_id, email FROM patients;
```

### Borrar una columna

```sql
ALTER TABLE table_name
DROP COLUMN column_name;
```

Ejemplo: borrar la columna "last_name" de `patients`:

```sql
ALTER TABLE patients
DROP COLUMN last_name;

SELECT * FROM patients;
```

### Cambiar el tipo de dato de una columna

```sql
-- SQL Server / MS Access
ALTER TABLE table_name
ALTER COLUMN column_name datatype;

-- MySQL / Oracle (antes de 10G)
ALTER TABLE table_name
MODIFY COLUMN column_name datatype;

-- Oracle 10G y posteriores
ALTER TABLE table_name
MODIFY column_name datatype;
```

---

## DROP TABLE — Borrar tablas

La sentencia `DROP TABLE` se usa para **eliminar una tabla existente** de la base de datos.

### Sintaxis

```sql
DROP TABLE table_name;
```

> ⚠️ **Mucho cuidado:** al borrar una tabla se pierden **todos sus datos**. No hay "deshacer" (salvo backups).

### Ejemplo

```sql
DROP TABLE patients;

-- Intentar consultarla después del DROP dará error
SELECT * FROM patients;
```

> 💡 **Diferencias clave:**
> - `DELETE FROM tabla` → borra **filas** (puede llevar WHERE), la tabla sigue existiendo.
> - `TRUNCATE TABLE tabla` → vacía la tabla **completa** rápidamente, mantiene la estructura.
> - `DROP TABLE tabla` → elimina la **tabla entera** (estructura + datos).

> 🔥 **Nota para hacking:** `'; DROP TABLE usuarios; --` es el payload de broma de las películas, pero `DROP` y `DELETE` troyanizados son un riesgo real en SQLi destructiva. Nunca los lances sin autorización: la destrucción de datos NO es reversible y te convierte en delincuente.

---

## 🧪 Mini-retos del capítulo

1. Crea una tabla `hackers` con: id (entero, PK, auto-increment), alias (texto, obligatorio y único), nivel (entero con CHECK ≥ 1), pais (texto con DEFAULT 'Unknown').
2. Inserta dos hackers sin indicar el id ni el país.
3. Añade la columna `email` a `hackers`.
4. Crea un índice sobre `alias`.
5. Vacía la tabla sin borrar su estructura... y luego bórrala del todo.

<details>
<summary>👀 Soluciones</summary>

```sql
-- 1 (MySQL)
CREATE TABLE hackers (
  id int NOT NULL AUTO_INCREMENT,
  alias varchar(50) NOT NULL UNIQUE,
  nivel int CHECK (nivel >= 1),
  pais varchar(50) DEFAULT 'Unknown',
  PRIMARY KEY (id)
);
-- 2
INSERT INTO hackers (alias, nivel) VALUES ('Dise0', 5), ('Neo', 3);
-- 3
ALTER TABLE hackers ADD email varchar(100);
-- 4
CREATE INDEX idx_alias ON hackers (alias);
-- 5
TRUNCATE TABLE hackers;
DROP TABLE hackers;
```
</details>

## 📌 Resumen del capítulo

| Sentencia / Constraint | Para qué |
|------------------------|----------|
| `CREATE TABLE` | Crear tablas (nombre + tipo + constraints) |
| `ALTER TABLE` | Añadir/borrar/modificar columnas y constraints |
| `DROP TABLE` | Eliminar tabla y datos ⚠️ |
| `PRIMARY KEY` | Identificador único de fila |
| `FOREIGN KEY` | Enlace íntegro entre tablas |
| `UNIQUE` / `NOT NULL` | Unicidad y obligatoriedad |
| `CHECK` / `DEFAULT` | Validación y valores por defecto |
| `AUTO_INCREMENT` / `IDENTITY` / `SEQUENCE` | Contadores automáticos (según motor) |
| `CREATE INDEX` | Acelerar búsquedas frecuentes |

➡️ **Siguiente capítulo:** [SQL para Hacking — Inyección SQL](./07-sql-para-hacking.md)
