# API2: Autenticación defectuosa

## Qué es

La autenticación defectuosa en APIs ocurre cuando los mecanismos de autenticación son débiles, inseguros o directamente bypasseables — permitiendo que actores no autorizados accedan a la API haciéndose pasar por usuarios legítimos o sin presentar credenciales válidas en absoluto.

## Manifestaciones más frecuentes en APIs

### Tokens sin caducidad o con caducidad excesiva

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0...
```

Un token JWT con algoritmo `none` (sin firma) es aceptado por implementaciones vulnerables de JWT — cualquiera puede construir un token con cualquier contenido.

Tokens que nunca expiran significan que una filtración compromete indefinidamente la cuenta.

### Credenciales en URLs (parámetros de query)

```
GET /api/v1/data?api_key=secreto123
```

Las credenciales en la URL terminan en logs de servidor, historial del navegador, cabeceras `Referer` de otras peticiones, y herramientas de monitorización — todas fuentes de fuga fácilmente ignoradas.

### Endpoints que omiten autenticación

Endpoints "olvidados" durante el desarrollo, versiones antiguas de la API, o rutas de debug que no pasan por el middleware de autenticación:

```
/api/v2/users           → autenticado
/api/v1/users           → ¿también autenticado? (versión antigua)
/api/internal/users     → ¿requiere autenticación externa?
```

### Políticas de contraseña y rate limiting inadecuados

Los mismos problemas trabajados en el bloque de *Login Brute Forcing* y *Broken Authentication* — sin límite de intentos en el endpoint de autenticación, fuerza bruta es trivialmente viable.

## Mitigación

- Tokens con caducidad corta y mecanismo de renovación.
- JWT firmados con algoritmo criptográfico robusto (RS256, ES256), nunca `none`.
- Credenciales exclusivamente en cabeceras HTTP (`Authorization: Bearer ...`), nunca en URLs.
- Rate limiting y límite de intentos fallidos en todos los endpoints de autenticación.
- Auditoría periódica de endpoints para confirmar que todos requieren autenticación cuando corresponde.
