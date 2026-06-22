# Introducción a los ataques a las API

## Por qué las APIs merecen un bloque propio de seguridad

Las APIs son la columna vertebral de las aplicaciones modernas: aplicaciones móviles, integraciones de terceros, microservicios, y la mayoría de los frontends de una sola página (SPA) consumen APIs directamente. Esto las convierte en una superficie de ataque de altísima relevancia — con frecuencia menos auditada que las interfaces web tradicionales, y con características propias que las distinguen de una aplicación web convencional.

## Estilos de API

| Estilo | Características clave | Cuándo se usa |
|---|---|---|
| **REST** | Sin estado, JSON/XML, múltiples endpoints por recurso | El más extendido — aplicaciones web y móviles modernas |
| **SOAP** | XML estructurado, mensajes WSDL, muy estandarizado | Sistemas empresariales, servicios financieros, legacy |
| **GraphQL** | Un único endpoint, consultas flexibles, esquema tipado | Cubierto en el bloque anterior |
| **gRPC** | Protocol Buffers, alto rendimiento, multilenguaje | Microservicios, sistemas distribuidos de alto rendimiento |

Este bloque se centra en APIs REST, pero los principios de las vulnerabilidades aplican también a los demás estilos.

## El OWASP API Security Top 10 como marco de referencia

[OWASP](https://owasp.org/www-project-api-security/) mantiene una lista específica de los diez riesgos de seguridad más críticos en APIs — distinta del OWASP Top 10 general de aplicaciones web, porque las APIs tienen particularidades propias:

| # | Categoría | Resumen |
|---|---|---|
| API1 | Autorización de objeto rota (BOLA/IDOR) | Acceder a datos de otros objetos sin permiso |
| API2 | Autenticación defectuosa | Eludir o sortear el mecanismo de autenticación |
| API3 | Autorización de propiedad de objeto rota | Acceder o modificar propiedades no autorizadas de un objeto |
| API4 | Consumo de recursos sin restricciones | La API no limita cuántos recursos puede consumir un usuario |
| API5 | Autorización de función rota | Usuarios sin permiso ejecutando operaciones restringidas |
| API6 | Acceso a flujos de negocio sensibles | Abuso de flujos de negocio legítimos (compras, votaciones, etc.) |
| API7 | SSRF | Solicitudes forjadas que alcanzan recursos internos |
| API8 | Configuración de seguridad incorrecta | Errores de configuración que habilitan ataques de inyección u otros |
| API9 | Gestión inadecuada de inventario | Versiones antiguas, APIs de debug, o endpoints no documentados sin protección |
| API10 | Consumo inseguro de APIs de terceros | La propia API consume servicios externos de forma insegura |

Los siguientes apartados de este bloque desarrollan cada categoría con su contexto, ejemplos de cómo se manifiesta en auditorías, y medidas de mitigación — el mismo esquema aplicado en cada bloque de este temario.

## La diferencia clave frente a aplicaciones web tradicionales

Lo que distingue a las APIs de las aplicaciones web convencionales desde la perspectiva de seguridad no es el tipo de vulnerabilidades (son esencialmente las mismas), sino:

1. **El acceso es directo y programático** — no hay interfaz visual que oscurezca los endpoints o los parámetros disponibles.
2. **Las APIs tienen versiones y pueden existir múltiples versiones en producción simultáneamente** — incluyendo versiones antiguas sin los parches de seguridad más recientes.
3. **Las APIs pueden estar parcialmente documentadas** — lo que significa que pueden existir endpoints funcionales que no aparecen en ninguna documentación pública ni en el frontend.
4. **El abuso automatizado es más fácil** — sin CAPTCHA ni fricción de interfaz, enviar miles de peticiones es trivial.
