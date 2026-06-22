# API3: Autorización de nivel de propiedad de objeto rota

## Qué es

A diferencia de BOLA/IDOR (que trata sobre acceso a *objetos* completos no autorizados), esta categoría trata sobre acceso o modificación de *propiedades específicas* dentro de un objeto al que el usuario *sí* tiene acceso legítimo. Se divide en dos subcategorías:

- **Exposición excesiva de datos**: la API devuelve más campos de los que el cliente debería ver.
- **Asignación masiva**: la API acepta la modificación de propiedades que el usuario no debería poder cambiar.

## Exposición excesiva de datos

```http
GET /api/v1/users/183
```

```json
{
  "id": 183,
  "username": "alice",
  "email": "alice@ejemplo.com",
  "password_hash": "$2b$10$...",   ← no debería exponerse
  "role": "admin",                 ← dato sensible en respuesta
  "api_token": "secreto123"        ← credencial en respuesta
}
```

La API devuelve el objeto completo desde la base de datos — incluyendo campos sensibles que el frontend simplemente ignora pero que son completamente visibles en la respuesta HTTP.

Muchos frameworks ORM hacen trivial serializar y devolver un objeto completo, y los equipos de desarrollo confían en que "el frontend no muestra esos campos" — sin darse cuenta de que cualquier cliente HTTP puede leer la respuesta completa.

## Asignación masiva (Mass Assignment)

```http
PUT /api/v1/users/183
```

```json
{
  "email": "nuevo@ejemplo.com",
  "role": "admin"    ← el usuario no debería poder cambiar su propio rol
}
```

Si el backend acepta y aplica todos los campos del cuerpo de la petición sin filtrar cuáles el usuario tiene permiso para modificar, un usuario estándar puede modificar propiedades privilegiadas (rol, estado de verificación, saldo, nivel de suscripción).

## Detección durante una auditoría

1. Inspeccionar las respuestas de los endpoints de lectura — ¿devuelven más campos de los que la interfaz muestra?
2. Probar peticiones de actualización incluyendo campos que no están en el formulario visible (inspeccionando el código JavaScript del frontend, como se vio en el bloque de *Web Attacks*).
3. Comparar qué campos acepta el endpoint con qué campos debería poder modificar un usuario estándar según la lógica de negocio.

## Mitigación

- **Serialización explícita**: definir exactamente qué campos se incluyen en cada respuesta, en lugar de serializar el objeto completo de la base de datos.
- **Lista blanca de campos modificables**: en endpoints de actualización, validar que solo los campos permitidos para ese rol específico se aplican — ignorar o rechazar cualquier otro campo en el cuerpo de la petición.
- **DTOs (Data Transfer Objects)**: usar objetos de transferencia de datos separados del modelo de base de datos, con únicamente los campos relevantes para cada caso de uso.
