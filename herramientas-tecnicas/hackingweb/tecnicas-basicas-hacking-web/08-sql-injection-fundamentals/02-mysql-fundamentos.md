# MySQL: línea de comandos, tablas y consultas

## Conectando con el cliente `mysql`

```bash
mysql -u root -p
```

`-u` indica el usuario; `-p` (sin valor pegado) hace que se solicite la contraseña de forma interactiva, evitando que quede guardada en texto plano en el historial de la shell (`~/.bash_history`).

```bash
mysql -u root -h objetivo.com -P 3306 -p
```

`-h` especifica el host remoto (por defecto, `localhost`); `-P` (mayúscula) el puerto, distinto del `-p` minúscula de la contraseña — el puerto por defecto de MySQL/MariaDB es **3306**.

> **Buena práctica de seguridad operativa**: nunca pasar la contraseña pegada al flag (`-ppassword`) en scripts o comandos que puedan quedar registrados en logs o historial.

## Comandos básicos de exploración

```sql
SHOW DATABASES;
USE nombre_basededatos;
SHOW TABLES;
DESCRIBE nombre_tabla;
```

- `SHOW DATABASES`: lista todas las bases de datos del servidor.
- `USE`: cambia el contexto a una base de datos concreta.
- `SHOW TABLES`: lista las tablas de la base de datos activa.
- `DESCRIBE`: muestra la estructura (columnas y tipos) de una tabla.

> Las sentencias SQL **no distinguen mayúsculas/minúsculas** (`USE` = `use`), pero los **nombres** de bases de datos y tablas **sí** son sensibles a mayúsculas en muchos sistemas. Por convención (y para evitar confusión), las palabras clave SQL se escriben en mayúsculas.

## Creando estructuras: CREATE DATABASE / TABLE

```sql
CREATE DATABASE users;

CREATE TABLE logins (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    date_of_joining DATETIME DEFAULT NOW(),
    PRIMARY KEY (id)
);
```

### Propiedades de columna relevantes

| Propiedad | Efecto |
|---|---|
| `AUTO_INCREMENT` | Incrementa automáticamente el valor (típico en columnas `id`) |
| `NOT NULL` | El campo es obligatorio |
| `UNIQUE` | No se permiten valores duplicados en esa columna |
| `DEFAULT` | Valor por defecto si no se especifica al insertar |
| `PRIMARY KEY` | Identifica de forma única cada fila de la tabla |

## Las cuatro operaciones CRUD en SQL puro

| Operación | Sentencia SQL |
|---|---|
| Crear | `INSERT INTO tabla (col1, col2) VALUES ('val1', 'val2');` |
| Leer | `SELECT * FROM tabla WHERE condicion;` |
| Actualizar | `UPDATE tabla SET col1='nuevo' WHERE condicion;` |
| Eliminar | `DELETE FROM tabla WHERE condicion;` |

Exactamente el mismo patrón CRUD visto desde la perspectiva de API REST en el bloque de *Web Requests* — aquí, en su forma más directa, el lenguaje que el backend traduce internamente.

## Cómo una aplicación web usa esto en la práctica

```php
$conn = new mysqli("localhost", "root", "password", "users");
$query = "select * from logins";
$result = $conn->query($query);

while($row = $result->fetch_assoc()) {
    echo $row["name"]."<br>";
}
```

Y, de forma crítica para todo lo que viene después en este bloque, cuando la consulta incorpora entrada directa del usuario:

```php
$searchInput = $_POST['findUser'];
$query = "select * from logins where username like '%$searchInput'";
$result = $conn->query($query);
```

Esta concatenación directa de entrada de usuario dentro de la cadena SQL —sin ningún tratamiento intermedio— es exactamente la causa raíz de la inyección SQL, que se desarrolla en profundidad a partir del apartado de *Introducción a la inyección SQL* de este mismo bloque.
