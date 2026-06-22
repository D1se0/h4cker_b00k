# Bases de datos: relacionales y no relacionales

## Por qué las aplicaciones necesitan una base de datos

Las aplicaciones web almacenan prácticamente todo en una base de datos: usuarios y contraseñas (idealmente hasheadas), contenido generado por usuarios, configuración, registros de actividad, etc. Esto permite servir contenido dinámico y personalizado a cada usuario sin tener que regenerar manualmente cada página.

Las prioridades habituales al elegir una base de datos son velocidad, capacidad de almacenamiento, escalabilidad y coste — y, según cuáles de estos factores pesen más, el tipo de base de datos elegido puede ser muy distinto.

## Bases de datos relacionales (SQL)

Almacenan los datos en **tablas**, organizadas en filas y columnas, con relaciones explícitas entre tablas mediante claves.

Ejemplo conceptual: una tabla `users` (con columnas `id`, `username`, `first_name`...) y una tabla `posts` (con columnas `id`, `user_id`, `date`, `content`...), donde `user_id` en `posts` referencia el `id` de `users`. Esto permite recuperar, con una sola consulta, todos los datos relacionados de un usuario y sus publicaciones, sin duplicar información.

| Motor | Características |
|---|---|
| **MySQL** | El más extendido en internet. Gratuito y de código abierto. |
| **MSSQL (SQL Server)** | Implementación de Microsoft, habitual junto a IIS y entornos Windows. |
| **Oracle** | Orientada a gran empresa, muy fiable, licencia comercial costosa. |
| **PostgreSQL** | Gratuita, de código abierto, diseñada para ser fácilmente extensible. |

Otras: SQLite, MariaDB, Amazon Aurora, Azure SQL.

### Relevancia ofensiva

Las bases de datos relacionales son el blanco clásico de la **inyección SQL (SQLi)**, que veremos en profundidad en su propio bloque. La estructura predecible de tablas/columnas y la presencia de un lenguaje de consulta estandarizado (con variaciones de sintaxis entre motores) es lo que hace posible enumerar sistemáticamente toda la base de datos una vez se confirma una inyección.

## Bases de datos no relacionales (NoSQL)

No utilizan tablas, filas, columnas ni esquema fijo. En su lugar, almacenan datos según distintos modelos según el caso de uso:

- **Clave-valor**: cada entrada se identifica por una clave única, asociada a un valor (que puede ser una cadena, un objeto JSON, etc.).
- **Basado en documentos**: cada "documento" es un objeto JSON con su propia estructura, sin necesidad de que todos los documentos de una misma colección compartan exactamente los mismos campos.
- **Columna ancha** (*wide-column*).
- **Grafo**: optimizado para representar y consultar relaciones complejas entre entidades.

```json
{
  "100001": {
    "date": "01-01-2026",
    "content": "Welcome to this web application."
  },
  "100002": {
    "date": "02-01-2026",
    "content": "This is the first post on this web app."
  }
}
```

| Motor | Características |
|---|---|
| **MongoDB** | El más popular en NoSQL. Basado en documentos JSON. Gratuito y de código abierto. |
| **ElasticSearch** | Optimizado para búsqueda y análisis de grandes volúmenes de datos. |
| **Apache Cassandra** | Muy escalable, diseñada para tolerar fallos con elegancia. |

Otras: Redis, Neo4j, CouchDB, Amazon DynamoDB.

Por su falta de esquema rígido, las bases de datos NoSQL son especialmente flexibles y escalables, lo que las hace atractivas para datos poco estructurados o que cambian con frecuencia. A cambio, introducen su propia clase de vulnerabilidades de inyección (**NoSQL Injection**), con sintaxis y técnicas distintas a las de SQL — relevante, por ejemplo, al auditar APIs construidas sobre MongoDB, donde la inyección suele explotarse manipulando la estructura del propio JSON enviado en lugar de cadenas de texto.

## Cómo interactúa una aplicación con su base de datos

Un ejemplo típico en PHP con MySQL:

```php
$conn = new mysqli("localhost", "user", "pass", "database1");
$searchInput = $_POST['findUser'];
$query = "select * from users where name like '%$searchInput%'";
$result = $conn->query($query);

while($row = $result->fetch_assoc()) {
    echo $row["name"]."<br>";
}
```

Este patrón —tomar una entrada de usuario y concatenarla directamente dentro de una cadena de consulta SQL— es exactamente la causa raíz de la inyección SQL. Si `$searchInput` no se valida ni se trata mediante consultas parametrizadas (*prepared statements*), un atacante puede manipular la sintaxis de la consulta resultante e introducir lógica SQL arbitraria. Este ejemplo concreto será el punto de partida del bloque dedicado a *SQL Injection Fundamentals*.
