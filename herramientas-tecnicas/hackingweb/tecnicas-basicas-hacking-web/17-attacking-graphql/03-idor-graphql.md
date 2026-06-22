# IDOR en GraphQL

## El mismo problema, nuevo contexto

IDOR en GraphQL sigue exactamente el mismo patrón trabajado en el bloque de *Web Attacks*: el servidor devuelve datos de objetos que el usuario no debería poder ver, porque no verifica en el backend que el usuario autenticado tiene permiso sobre el objeto solicitado.

La diferencia con REST es que GraphQL puede hacer que el impacto sea mayor por su flexibilidad: una única consulta puede pedir campos de un objeto al que se tiene IDOR, incluyendo campos sensibles descubiertos vía introspección.

## Detectando IDOR en una consulta GraphQL

Observando la consulta que la aplicación envía al cargar el perfil propio:

```graphql
{
  user(username: "htb-stdnt") {
    username
    email
  }
}
```

Si cambiar el argumento `username` a otro usuario devuelve sus datos sin error de autorización, hay IDOR confirmado.

## Amplificando el impacto con introspección

Una vez detectado IDOR, se consulta el esquema para descubrir qué campos sensibles tiene el tipo:

```graphql
{
  __type(name: "UserObject") {
    fields { name type { name } }
  }
}
```

Si el tipo `UserObject` incluye campos como `password`, `apiToken`, o `sessionId`, la consulta IDOR puede ampliarse para extraerlos:

```graphql
{
  user(username: "admin") {
    username
    password
    email
  }
}
```

## La mitigación: idéntica a IDOR en REST

Verificar server-side que el usuario autenticado (desde el token de sesión, no desde el argumento de la consulta) tiene permiso sobre cada objeto solicitado. La introspección puede revelar qué campos existen, pero un control de acceso robusto evita que sean accesibles sin autorización.
