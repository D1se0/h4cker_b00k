# Bases de datos y SQL: fundamentos

## Por qué empezar por aquí

Para explotar una inyección SQL con criterio —no solo copiando payloads de una lista— hace falta entender qué está pasando realmente: cómo se estructura una base de datos relacional, qué hace exactamente cada palabra clave SQL, y cómo una aplicación web típica construye sus consultas a partir de entrada del usuario. Este apartado sienta esa base.

## El flujo: de la petición HTTP a la consulta SQL

```
Petición HTTP del usuario → Servidor de aplicación → Consulta SQL al DBMS → Respuesta → HTML de vuelta al usuario
```

Cuando la aplicación usa información de la petición del usuario (un parámetro de búsqueda, un campo de login) para **construir** la consulta SQL, y esa entrada no se trata con cuidado, un usuario malicioso puede alterar la consulta para que haga algo distinto de lo que el programador original pretendía. Eso es, en esencia, una **inyección SQL (SQLi)**.

> **Terminología**: "inyección SQL" se refiere específicamente a ataques contra bases de datos **relacionales** (MySQL, PostgreSQL, MSSQL, Oracle...). Los ataques equivalentes contra bases de datos no relacionales (MongoDB, por ejemplo) se llaman **inyección NoSQL**, y siguen una lógica distinta — se tratan en un bloque aparte de este temario.

## Sistemas de Gestión de Bases de Datos (DBMS)

Un DBMS crea, define, aloja y administra bases de datos. Propiedades esenciales:

| Propiedad | Qué garantiza |
|---|---|
| **Concurrencia** | Múltiples usuarios interactuando simultáneamente sin corrupción de datos |
| **Consistencia** | Los datos permanecen válidos en toda la base de datos |
| **Seguridad** | Autenticación y permisos granulares por usuario |
| **Fiabilidad** | Copias de seguridad y recuperación ante fallos |
| **SQL** | Sintaxis estandarizada e intuitiva para interactuar con los datos |

## Arquitectura en capas

```
Cliente (navegador) → Middleware (interpreta y formatea peticiones) → DBMS (ejecuta consultas)
```

El cliente envía interacciones de alto nivel (login, comentarios) vía API; el middleware las traduce al formato que el DBMS espera; el DBMS ejecuta la operación (insertar, leer, actualizar, eliminar) y devuelve resultado o error.

## Bases de datos relacionales vs. no relacionales

### Relacionales (SQL)

Usan un **esquema** fijo: tablas con columnas tipadas, relacionadas entre sí mediante claves. Por ejemplo, una tabla `users` (con `id`, `username`...) y una tabla `posts` (con `id`, `user_id`...) donde `user_id` referencia el `id` de `users` — el mismo patrón visto en el bloque de *Introducción a Aplicaciones Web*. Esta estructura predecible es precisamente lo que hace posible **enumerar sistemáticamente** una base de datos comprometida vía inyección, como se verá en detalle más adelante en este bloque.

Ejemplos: **MySQL** (la más usada en internet, gratuita), MariaDB (fork compatible de MySQL, usado en los ejemplos de este bloque), MSSQL, Oracle, PostgreSQL.

### No relacionales (NoSQL)

Sin tablas, filas, columnas ni esquema fijo — almacenan datos según modelos como clave-valor, documentos, columna ancha o grafo. Más flexibles y escalables para datos poco estructurados, pero con su propia clase de inyección (NoSQL Injection), con sintaxis y técnicas distintas.

Ejemplo: **MongoDB**, basado en documentos JSON.

## Por qué este bloque se centra en MySQL

MySQL (y su fork compatible MariaDB) es, con diferencia, el motor relacional más extendido en aplicaciones web — la base natural para aprender los conceptos fundamentales de SQLi antes de generalizar a otros motores (PostgreSQL, MSSQL), que comparten la misma lógica de fondo pero difieren en sintaxis específica para ciertas operaciones avanzadas.
