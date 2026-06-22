# API1: Autorización a nivel de objeto rota (BOLA/IDOR)

## Qué es

**BOLA** (Broken Object Level Authorization) es el nuevo nombre oficial de OWASP para lo que en el bloque de *Web Attacks* se trabajó como **IDOR**: la API devuelve o permite modificar datos de un objeto específico sin verificar que el usuario autenticado tiene permiso sobre ese objeto concreto.

Es el riesgo número 1 del OWASP API Top 10 — el más frecuente y el de mayor prevalencia en auditorías reales.

## Manifestación en APIs REST

```
GET /api/v1/invoices/1042   → devuelve la factura del usuario actual ✓
GET /api/v1/invoices/1043   → ¿devuelve la factura de OTRO usuario? ✗ si hay BOLA
```

La misma lógica aplica a endpoints de actualización:

```
PUT /api/v1/users/183/email  → sin verificar que el token autenticado pertenece al usuario 183
DELETE /api/v1/posts/99      → sin verificar que el usuario autenticado es el autor del post 99
```

## Por qué es especialmente frecuente en APIs

En una aplicación web tradicional, los identificadores de objetos suelen estar "ocultos" detrás de la interfaz — el usuario ve el resultado pero no necesariamente el ID numérico. En una API REST, los IDs de objeto son explícitos en la propia URL y en el cuerpo de las peticiones, lo que hace que intentar modificarlos sea inmediato e intuitivo.

## Mitigación

- Verificar en el backend, para cada petición, que el usuario autenticado (desde el token de sesión, no desde la URL) tiene permiso sobre el objeto con el ID solicitado.
- Usar identificadores no predecibles (UUID v4) como segunda capa — no como sustituto de la verificación de permisos.
