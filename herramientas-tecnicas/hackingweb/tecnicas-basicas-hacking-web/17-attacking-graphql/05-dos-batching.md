# DoS y ataques por lotes (batching) en GraphQL

## Consultas excesivamente complejas — DoS por profundidad

GraphQL permite subconsultas anidadas que referencian objetos relacionados. Si el esquema tiene ciclos (por ejemplo, un `Post` tiene un `author` de tipo `User`, y un `User` tiene `posts` de tipo `Post`), es posible construir una consulta que expanda ese ciclo de forma arbitraria:

```graphql
{
  posts {
    author {
      posts {
        edges {
          node {
            author {
              posts {
                edges {
                  node {
                    author {
                      username
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

Cada nivel de anidamiento multiplica el volumen de datos que el servidor debe resolver. Con suficientes niveles, la respuesta crece exponencialmente y el servidor puede quedarse sin recursos — un ataque de denegación de servicio basado puramente en la capacidad expresiva del lenguaje de consulta, sin ninguna vulnerabilidad de inyección.

**Por qué esto importa para auditorías**: no solo es un vector de DoS directo. También indica una falta de límites de complejidad en la API, que es la misma configuración que permite a un atacante generar carga de trabajo desproporcionada de otras formas.

## Batching — amplificación de fuerza bruta

GraphQL permite enviar múltiples consultas en una sola petición HTTP (batching). Si la API acepta arrays de consultas:

```json
[
  {"query": "{ user(username: \"admin\", password: \"pass1\") { id } }"},
  {"query": "{ user(username: \"admin\", password: \"pass2\") { id } }"},
  {"query": "{ user(username: \"admin\", password: \"pass3\") { id } }"}
]
```

Un atacante puede enviar cientos o miles de intentos de autenticación en una sola petición HTTP — lo que hace que los límites de tasa basados en número de peticiones HTTP sean completamente ineficaces, ya que cada petición HTTP contiene muchos intentos.

Esto es especialmente relevante en el contexto del bloque de *Login Brute Forcing* visto anteriormente: si la aplicación usa GraphQL para autenticación y permite batching, los límites de tasa por petición HTTP no tienen ningún efecto como protección contra fuerza bruta.

## Mitigación

| Vector | Medida |
|---|---|
| Consultas de profundidad excesiva | Limitar la profundidad máxima de consultas en la configuración del motor GraphQL |
| Consultas de complejidad excesiva | Implementar un límite de complejidad de consulta (muchos motores lo soportan) |
| Batching para eludir rate limiting | Deshabilitar el batching si no es necesario; o aplicar límites de intentos a nivel de operación dentro del batch, no solo a nivel de petición HTTP |
| Consultas lentas en general | Timeouts de consulta, monitorización de queries lentas |
