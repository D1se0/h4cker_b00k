# Introducción a GraphQL

## Qué es GraphQL y por qué difiere de REST

**GraphQL** es un lenguaje de consulta para APIs web, desarrollado por Facebook y publicado en 2015. A diferencia de REST, donde cada recurso tiene su propio endpoint (`/users/1`, `/posts/5`, etc.), GraphQL expone un **único endpoint** que acepta consultas en el lenguaje GraphQL y devuelve exactamente los campos que el cliente solicitó.

Ventajas desde el punto de vista del desarrollo:
- El cliente controla exactamente qué datos recibe (sin over-fetching ni under-fetching).
- Un endpoint único simplifica el enrutamiento del servidor.
- Soporte nativo para relaciones entre objetos en una sola consulta.

Desde el punto de vista de seguridad, esta flexibilidad introduce vectores propios que REST no tiene.

## Anatomía de una consulta GraphQL

```graphql
# Leer datos de usuarios
{
  users {
    id
    username
    role
  }
}
```

La respuesta sigue la misma estructura:

```json
{
  "data": {
    "users": [
      {"id": 1, "username": "htb-stdnt", "role": "user"},
      {"id": 2, "username": "admin", "role": "admin"}
    ]
  }
}
```

Con argumentos para filtrar:

```graphql
{
  users(username: "admin") {
    id
    username
    password
  }
}
```

Con subconsultas (relaciones entre objetos):

```graphql
{
  posts {
    title
    author {
      username
      role
    }
  }
}
```

## Los tres tipos de operación

| Operación | Función | Equivalente REST |
|---|---|---|
| **Query** | Leer datos | `GET` |
| **Mutation** | Crear, actualizar, eliminar | `POST`, `PUT`, `DELETE` |
| **Subscription** | Suscripción en tiempo real | WebSocket |

## Localizando el endpoint GraphQL

Los endpoints GraphQL más habituales:

```
/graphql
/api/graphql
/v1/graphql
/graphql/v1
/gql
```

Señales de que una aplicación usa GraphQL: peticiones POST cuyo cuerpo contiene `{"query": "..."}` en lugar de parámetros de formulario estándar, o respuestas JSON con la estructura `{"data": {...}}`.

## Por qué GraphQL merece un bloque propio en este temario

GraphQL no introduce categorías de vulnerabilidad completamente nuevas — los ataques de fondo son los mismos (IDOR, inyección SQL/NoSQL/comandos, control de acceso deficiente). Lo que cambia es:

1. **La superficie de descubrimiento**: la introspección puede revelar todo el esquema de datos en una sola consulta, sin necesidad de fuzzing manual.
2. **La flexibilidad como amplificador**: una sola consulta puede solicitar datos de múltiples objetos relacionados, amplificando el alcance de un IDOR.
3. **Vectores propios**: batching de consultas (útil para eludir rate limiting), consultas de profundidad excesiva (DoS), y mutaciones no autorizadas.

Los siguientes apartados de este bloque desarrollan cada uno de estos vectores con ejemplos concretos de consultas y mitigaciones específicas.
