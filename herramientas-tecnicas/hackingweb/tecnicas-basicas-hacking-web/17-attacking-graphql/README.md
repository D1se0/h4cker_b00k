# Attacking GraphQL

GraphQL es un lenguaje de consulta para APIs web, alternativa a REST, que permite al cliente especificar exactamente qué datos necesita. Al exponer un único endpoint con capacidades de consulta muy ricas, introduce su propia superficie de ataque: introspección que revela el esquema completo, IDOR por falta de control de acceso, inyecciones (SQL, NoSQL, XSS) a través de argumentos de consulta, y vulnerabilidades específicas de lotes (*batching*). Este bloque cubre todos estos vectores, las herramientas de trabajo específicas para GraphQL, y la prevención.

## Contenido

1. [Introducción a GraphQL](01-introduccion-graphql.md)
2. [Introspección y divulgación de información](02-introspection-disclosure.md)
3. [IDOR en GraphQL](03-idor-graphql.md)
4. [Ataques de inyección](04-inyeccion-graphql.md)
5. [DoS y ataques por lotes (batching)](05-dos-batching.md)
6. [Mutaciones: escribir datos](06-mutaciones.md)
7. [Herramientas para GraphQL](07-herramientas-graphql.md)
8. [Prevención de vulnerabilidades GraphQL](08-prevencion-graphql.md)

## Por qué este bloque importa

GraphQL está cada vez más extendido en aplicaciones modernas (React, Next.js, aplicaciones móviles). Su naturaleza de "único endpoint, esquema completo" concentra la superficie de ataque en un punto específico — si no está bien protegido, un atacante puede mapear toda la estructura de datos disponible en segundos mediante introspección, antes incluso de intentar ninguna explotación.
