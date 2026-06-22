# Mutaciones: escribir datos en GraphQL

## Qué son las mutaciones

Las **mutaciones** son el mecanismo GraphQL para operaciones que modifican datos — equivalente a `POST`, `PUT`, `DELETE` en REST. Crean, actualizan o eliminan objetos en el servidor.

Al igual que las queries, las mutaciones se descubren mediante introspección:

```graphql
query {
  __schema {
    mutationType {
      fields {
        name
        args {
          name
          type { name kind }
        }
      }
    }
  }
}
```

Esto devuelve todas las mutaciones disponibles y sus argumentos — equivalente a descubrir todos los endpoints POST/PUT/DELETE de una API REST.

## Vectores de auditoría en mutaciones

### Mutaciones sin autorización adecuada

Si una mutación permite modificar datos de otro usuario sin verificar permisos:

```graphql
mutation {
  updateUser(id: 2, email: "atacante@mail.com") {
    id
    email
  }
}
```

Si actualiza el email del usuario con `id=2` sin verificar que el usuario autenticado es ese mismo usuario o un administrador → IDOR de escritura, exactamente el patrón visto en el bloque de *Web Attacks*.

### Mutaciones que permiten escalada de privilegios

Si una mutación de actualización acepta cambiar el campo `role`:

```graphql
mutation {
  updateUser(id: 1, role: "admin") {
    id
    role
  }
}
```

Si el servidor no verifica que solo un admin puede asignar el rol admin → escalada de privilegios vía mutación.

### Mutaciones de registro sin límites

Si una mutación de creación de usuario no tiene rate limiting ni validación adecuada, puede usarse para crear cuentas masivamente o para batching de intentos de credenciales, como se vio en el apartado anterior.

## El patrón de auditoría

1. **Descubrir mutaciones** vía introspección.
2. **Probar cada mutación** con los parámetros mínimos necesarios para ejecutarla.
3. **Comprobar autorización**: ¿puede un usuario estándar ejecutar mutaciones que deberían estar restringidas? ¿Puede modificar datos de otros usuarios?
4. **Comprobar si los campos sensibles** (role, is_admin, verified) son modificables sin restricciones.

## Mitigación

Las mutaciones requieren exactamente el mismo control de acceso que los endpoints REST equivalentes — verificar en el servidor que el usuario autenticado tiene permiso para realizar cada operación concreta sobre cada objeto concreto. La flexibilidad de GraphQL no cambia este principio; solo hace que sea más fácil olvidarlo o implementarlo de forma inconsistente.
