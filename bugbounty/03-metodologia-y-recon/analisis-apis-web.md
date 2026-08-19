---
icon: rectangle-api
---

# Análisis de APIs y aplicaciones web

## 🔑 La pregunta central: ¿quién comprueba qué?

La inmensa mayoría de vulnerabilidades de API interesantes (IDOR/BOLA, escalada de privilegios, bypass de autorización) se reducen a una sola pregunta:

> **Cuando el cliente le dice al servidor "dame/modifica el recurso X", ¿el servidor comprueba de verdad que X le pertenece a quien está pidiendo, o se fía del identificador que le mandan?**

## 🧪 Metodología práctica paso a paso

1. **Crea dos cuentas de prueba propias** (cuenta A y cuenta B). Nunca uses cuentas reales de terceros.
2. **Realiza una acción normal con la cuenta A** (crear un recurso, guardar un favorito, ver un dato) y captura la petición con el proxy.
3. **Identifica todos los identificadores presentes**: en la URL (`/user/123`), en query params (`?userId=...`), en el body JSON, en headers, e incluso en cookies o en el propio JWT.
4. **Repite la petición pero sustituyendo el identificador por el de la cuenta B**, mientras sigues autenticado como A.
5. **Observa el resultado**:
   * Si el servidor te devuelve/modifica datos de B estando autenticado como A → vulnerabilidad de autorización (IDOR/BOLA).
   * Si el servidor responde 403/401 → correctamente protegido.
6. **Confirma el impacto real**: no te quedes en "responde 200 distinto", demuestra lectura, escritura o borrado real de un dato de la otra cuenta (siempre con tus propias cuentas de prueba).
7. **Prueba variantes**: ¿funciona igual en GET que en POST/PUT/DELETE? ¿Funciona igual desde la app móvil que desde la web? ¿Hay una versión antigua de la API (`/api/v1/`) menos protegida que la nueva?

## 🔐 Cosas específicas a revisar en APIs

* **Autenticación**: tipo de token (JWT, sesión, API key), dónde vive el identificador de usuario (¿en el token firmado, o en un campo que manda el cliente sin más?).
* **JWT**: decodifica siempre el payload (no hace falta romper la firma para leerlo, es solo base64). Revisa: `sub` (¿identifica a un usuario real o es un valor genérico compartido?), `exp` (¿caduca?), `iat` (¿cuándo se emitió?).
* **CORS**: cabeceras `Access-Control-Allow-Origin` demasiado permisivas combinadas con `Access-Control-Allow-Credentials: true`.
* **Rate limiting**: manda varias peticiones seguidas a un endpoint sensible (login, recuperación de contraseña, el propio IDOR) y observa si hay algún tipo de bloqueo o CAPTCHA.
* **Versionado de API**: prueba las rutas antiguas (`/v1/`, `/legacy/`) que a veces siguen activas con menos controles.
* **Mensajes de error verbosos**: a veces revelan estructura interna, stack traces, nombres de tablas/columnas.

## 🧾 Documentar mientras pruebas

Para cada endpoint interesante, anota:

* Método + ruta completa.
* Parámetros/identificadores relevantes y de dónde vienen (URL, body, header).
* Qué pasa con cuenta propia (A) sobre su propio recurso (control positivo).
* Qué pasa con cuenta A sobre recurso de cuenta B (la prueba real).
* Qué pasa sin token / con token inválido (control negativo, para demostrar que el servidor sí valida algo).

> 💡 Ver ejemplo completo aplicado de este método en [Intigriti — IDOR en API de favoritos](../06-ejemplos-reales/intigriti-idor-favoritos.md).
