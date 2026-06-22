# API8: Configuración de seguridad incorrecta

## Qué es

Errores de configuración que debilitan la seguridad de la API — desde cabeceras de seguridad ausentes hasta endpoints de debug expuestos, CORS mal configurado, o funcionalidades peligrosas habilitadas por defecto.

## Manifestaciones habituales

**CORS demasiado permisivo:**
```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
```

Combinar `*` en el origen con `Allow-Credentials: true` permite que cualquier sitio web haga peticiones autenticadas a la API en nombre del usuario — el mismo principio del CSRF que aplica aquí a nivel de configuración de cabeceras.

**Métodos HTTP no necesarios habilitados:**
```
Allow: GET, POST, PUT, DELETE, TRACE, OPTIONS
```

El método `TRACE` puede usarse para leer cabeceras de sesión incluso cuando las cookies están marcadas como `HttpOnly` — el mismo vector de verb tampering trabajado en el bloque de *Web Attacks*.

**Mensajes de error detallados:**
Stack traces, nombres de librerías, rutas del sistema de archivos, o fragmentos de código en respuestas de error — el mismo principio de "no exponer errores internos en producción" repetido en cada bloque de este temario.

## Mitigación

- Cabeceras de seguridad HTTP correctamente configuradas (`Content-Security-Policy`, `X-Content-Type-Options`, `Strict-Transport-Security`).
- CORS restrictivo: lista blanca de orígenes permitidos, nunca `*` con credenciales.
- Solo los métodos HTTP estrictamente necesarios habilitados.
- Mensajes de error genéricos en producción.
- Revisión de configuración como parte del proceso de release.

---

# API9: Gestión inadecuada del inventario

## Qué es

La API tiene versiones antiguas, endpoints de desarrollo, o funcionalidades no documentadas accesibles en producción sin la misma protección que la versión actual.

## Por qué es frecuente

Las APIs evolucionan — se añaden versiones nuevas (`/api/v2/`), pero las versiones antiguas (`/api/v1/`) permanecen activas para no romper clientes existentes. Con el tiempo, la versión antigua puede quedarse sin las mejoras de seguridad aplicadas a la nueva, incluyendo validaciones adicionales, controles de acceso más robustos, o correcciones de vulnerabilidades.

## Señales de alerta durante una auditoría

- URLs que sugieren versionado: `/v1/`, `/v2/`, `/beta/`, `/legacy/`.
- Endpoints que responden con comportamiento distinto en versiones distintas.
- Documentación que menciona endpoints ya "deprecados" pero que siguen siendo funcionales.
- Endpoints con nombre de herramienta de desarrollo (`/swagger`, `/api-docs`, `/debug`).

## Mitigación

- Inventario actualizado de todos los endpoints de API activos, incluyendo versiones.
- Proceso formal de retirada de versiones antiguas: anuncio con tiempo de aviso, luego desactivación real.
- Aplicar los mismos controles de seguridad a todas las versiones activas, no solo a la más reciente.
- Deshabilitar (no solo "no documentar") los endpoints de debug y administración en producción.

---

# API10: Consumo inseguro de APIs de terceros

## Qué es

La propia API consume servicios externos (otras APIs, webhooks, enriquecimiento de datos) de forma insegura — confiando en datos de terceros sin la validación adecuada, lo que puede permitir ataques de inyección o manipulación de datos a través de la cadena de confianza.

## La lógica del ataque

Si una API recibe datos de un servicio externo y los procesa directamente sin validación:

1. Un atacante compromete (o simplemente encuentra una debilidad en) ese servicio externo.
2. El servicio externo devuelve datos manipulados que contienen un payload de inyección.
3. La API los procesa como si fueran datos confiables, ejecutando el payload.

O bien, si la API acepta datos de un webhook sin verificar su autenticidad:

```http
POST /api/v1/webhook/payment-confirmed
{"transaction_id": "123", "status": "paid", "amount": 0.01}
```

Si la API confía en este payload sin verificar una firma criptográfica del servicio de pago, un atacante puede simular confirmaciones de pago fraudulentas.

## Mitigación

- Tratar los datos de APIs externas como datos de usuario no confiables — validarlos y sanitizarlos igual que cualquier otra entrada.
- Verificar firmas/tokens de autenticación en webhooks entrantes.
- Definir una política de seguridad para las dependencias de APIs externas (¿qué ocurre si el servicio externo se ve comprometido?).
- HTTPS y certificados verificados en todas las conexiones a APIs externas.

---

## Cierre del bloque de API Attacks

El OWASP API Security Top 10 cubre exactamente el tipo de fallos que aparecen con mayor frecuencia en auditorías de APIs reales — muchos de ellos son variantes de vulnerabilidades ya trabajadas en bloques anteriores de este temario (IDOR, autenticación, inyección, SSRF), pero con particularidades propias del contexto de APIs. La clave para auditar una API es aplicar de forma sistemática cada categoría del Top 10 sobre todos los endpoints descubiertos — incluyendo los no documentados, las versiones antiguas, y los endpoints que la interfaz visual nunca invoca directamente. El siguiente bloque, *Attacking Common Applications*, retoma estos principios aplicados a plataformas específicas y ampliamente desplegadas: WordPress, Tomcat, Jenkins y similares.
