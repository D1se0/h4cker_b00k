---
icon: trophy-star
---

# YesWeHack — JWT hardcodeado en app Android

> 🔒 **CONFIDENCIAL — INFORMACIÓN REDACTADA** Este es un reporte real que envié, con el nombre de la empresa, el dominio real, el token completo y la IP ocultados con efecto "rotulador negro". Se comparte solo como referencia de **formato y metodología**, no como PoC explotable.

**Plataforma:** YesWeHack **Programa:** Programa de energía — nombre de la empresa **Estado final:** En revisión (`Under Review`) tras responder a una petición de más información **CVSS asignado por el triager:** 7.5 (Alto)

***

## Título

Hard-coded Credentials en la app Android de \[Empresa X] a través de `/resources/assets/index.android.bundle`, con impacto en `<mark style="background-color:#000;color:#000;user-select:none">backend-interno.ejemplo.com</mark>/recomendarpot/{cups}`

## Resumen

La app oficial de Android de \[Empresa X] incluye un JWT escrito directamente en su bundle de JavaScript. No es un token de sesión emitido en el login: es una cadena de texto literal en el código fuente, **idéntica en todas las instalaciones de la app**, y que **nunca caduca** (el payload no tiene el claim `exp`, y el `sub` es el valor genérico `"[nombre-servicio]"` en vez de un identificador de usuario individual). En otras palabras: es una credencial de servicio compartida que vive dentro de un APK público descargable por cualquiera.

Ese token es aceptado por el backend en `GET /recomendarpot/{cups}`, un endpoint que busca el contrato eléctrico de un cliente por su código CUPS y devuelve datos de recomendación de potencia/tarifa. **El backend nunca comprueba si el CUPS solicitado pertenece realmente a quien tiene el token** — así que cualquiera que extraiga esta única credencial estática de la app pública puede consultar ese endpoint para cualquier CUPS que quiera.

> Todo lo probado usó valores de CUPS inventados, que no corresponden a ningún cliente real, y el token se obtuvo directamente del paquete de la app públicamente descargable — sin login, sin cuenta, sin tocar ningún dato real de cliente en ningún momento.

## Detalles técnicos

| Campo                   | Valor                                                                                               |
| ----------------------- | --------------------------------------------------------------------------------------------------- |
| CWE                     | CWE-798 (Use of Hard-coded Credentials), CWE-639 (Authorization Bypass Through User-Controlled Key) |
| Origen del secreto      | `assets/index.android.bundle` dentro del APK público de la app (v3.0.40)                            |
| Endpoint                | `GET /recomendarpot/{cups}` en backend-interno.ejemplo.com                                          |
| Autenticación requerida | Un token estático, no expirable, idéntico en todas las instalaciones — efectivamente ninguna        |

## Pasos de reproducción (resumen)

**0 — Obtener la app pública** (sin cuenta de Play Store, descarga directa desde una tienda alternativa) y desempaquetarla:

```bash
unzip app.xapk -d xapk_extracted
unzip xapk_extracted/com.empresa.app.apk -d apk_base
```

**1 — Extraer el token en texto plano** (los bundles Hermes/React Native guardan strings en UTF-8 plano, no hace falta descompilar bytecode):

```bash
grep -a -o "Bearer eyJ[A-Za-z0-9_=.-]*" apk_base/assets/index.android.bundle
grep -a -o "recomendarpot[a-zA-Z0-9_/{}]*" apk_base/assets/index.android.bundle
```

**2 — Decodificar el payload** (solo base64, sin necesidad de romper la firma):

```python
import base64, json
payload = "<mark style='background-color:#000;color:#000;user-select:none'>[payload JWT completo redactado]</mark>"
payload += "=" * (-len(payload) % 4)
print(json.dumps(json.loads(base64.urlsafe_b64decode(payload)), indent=2))
```

Resultado: `iat` de febrero de 2024, **sin claim `exp`**, y `sub` con el valor genérico del servicio en vez de un ID de usuario real.

**3 — Control negativo** (confirmar que el servidor sí valida algo, no es un fallo genérico de "todo pasa"):

```bash
# Sin token → 401
curl -s -o /dev/null -w "%{http_code}\n" \
  "https://<mark style='background-color:#000;color:#000;user-select:none'>backend-interno.ejemplo.com</mark>/recomendarpot/ES0000000000000000AA"

# Token roto → 422 "Not enough segments" (prueba de que SÍ parsea el JWT, no solo mira si hay header)
curl -s -H "Authorization: Bearer basura123" \
  "https://<mark style='background-color:#000;color:#000;user-select:none'>backend-interno.ejemplo.com</mark>/recomendarpot/ES0000000000000000AA" -w "\nHTTP:%{http_code}\n"
```

**4 — Usar el token hardcodeado contra un CUPS inventado:**

```bash
TOKEN="<mark style='background-color:#000;color:#000;user-select:none'>[JWT completo redactado]</mark>"

curl -s -H "Authorization: Bearer $TOKEN" \
  "https://<mark style='background-color:#000;color:#000;user-select:none'>backend-interno.ejemplo.com</mark>/recomendarpot/ES0000000000000000AA" -w "\nHTTP:%{http_code}\n"
```

Un CUPS que nunca estuvo registrado a ningún contrato real devuelve igualmente un **200 completo y bien formado** — el token de la app basta por sí solo, sin ninguna sesión detrás.

**5 — Repetir con un segundo CUPS distinto** para probar que es una consulta real por CUPS y no una respuesta cacheada/genérica: mismo resultado, con el CUPS reflejado exactamente en la respuesta.

## Impacto

Para cualquier CUPS que alguien decida consultar, el endpoint devuelve `potencia_actual`, `potencia_recomendada`, `potencia_registrada`, `ahorro`, un rango de precios, y si el contrato está activo — usando solo un token que cualquiera puede extraer de la app pública.

## Recomendación de solución

1. Eliminar el token estático del cliente y sustituirlo por autenticación de sesión por usuario.
2. En el backend, `GET /recomendarpot/{cups}` debe verificar que el CUPS solicitado pertenece realmente a la sesión autenticada — nunca confiar en un parámetro de ruta sin comprobar propiedad.
3. Rotar la clave de firma HS256 en el servidor para invalidar este token específico — corregir solo el endpoint no basta, cada copia del APK ya distribuida seguiría teniendo un token válido hasta que cambie la clave.

***

## 💬 Cómo defendí el impacto tras un "Need More Info"

El programa respondió inicialmente con dudas legítimas: _"No estamos seguros de entender el impacto de seguridad. El PoC solo muestra una diferencia de respuesta (200 en vez de 401). ¿Podéis aportar una PoC que muestre cómo el conocimiento de este token permite acceder a información a la que no se tenía acceso, o modificarla?"_

Esta es exactamente la situación descrita en [Comunicación con los programas](../04-como-escribir-reportes/comunicacion-con-programas.md#-cómo-responder-a-un-need-more-info-necesita-más-información). Así respondí, punto por punto:

1. **El propio cuerpo de la respuesta demuestra que es una consulta real a base de datos**, no una respuesta genérica: el JSON devuelto incluye un código de negocio específico (`SIN_CONTRATOS_ACTIVOS`) que refleja exactamente el CUPS solicitado — no es un mock ni una plantilla estática.
2. **Confirmado con 3 valores de CUPS distintos**, incluido uno que ni siquiera tenía el formato válido de un CUPS — demostrando que el endpoint no hace ninguna validación de formato antes de consultar la base de datos: no hay ninguna barrera entre "tener el token estático" y "obtener un resultado directo de base de datos".
3. **Sin rate limiting**: varias peticiones consecutivas con distintos CUPS, todas con 200, sin bloqueo ni CAPTCHA — lo que en combinación con el punto 2 permitiría barrer rangos de CUPS reales a escala.
4. **Por qué no fuimos más allá**: explicité que deliberadamente no consultamos ningún CUPS de un cliente real, porque hacerlo habría significado acceder a datos reales sin consentimiento — precisamente la línea que este tipo de reporte existe para proteger. Ofrecí al equipo dos formas de cerrar el círculo ellos mismos, sin que yo tuviera que cruzar esa línea: (a) probar el endpoint con un CUPS interno de prueba con contrato activo y comparar la respuesta, o (b) revisar en sus logs las peticiones que llevan el mismo `jti` del token — que por sí solo demuestra que no hay ningún límite por usuario en este endpoint.

> 📌 **Lección clave**: cuando te pidan "más pruebas de impacto", no repitas lo mismo con otras palabras. Aporta **evidencia estructural nueva** (aquí: la forma del JSON, la ausencia de validación de formato, la ausencia de rate limiting) y ofrece explícitamente una vía para que el propio equipo cierre el círculo sin que tengas que cruzar ninguna línea ética.
