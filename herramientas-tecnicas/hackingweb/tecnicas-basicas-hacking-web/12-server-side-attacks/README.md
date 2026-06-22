# Server-side Attacks

A diferencia de las vulnerabilidades del lado del cliente como XSS, este bloque cubre cuatro clases de vulnerabilidad que atacan directamente al **servidor**: SSRF (falsificación de solicitudes del lado del servidor), SSTI (inyección de plantillas), inyección SSI (Server-Side Includes) e inyección XSLT. Las cuatro comparten un patrón de fondo similar al resto de inyecciones vistas en este temario — entrada de usuario que termina interpretándose como instrucción en un contexto donde debería tratarse solo como dato — pero cada una con su propio mecanismo, impacto y mitigación específicos.

## Contenido

1. [Introducción a los ataques del lado del servidor](01-introduccion-server-side.md)
2. [SSRF: qué es y por qué importa](02-ssrf-introduccion.md)
3. [Identificación de SSRF](03-ssrf-identificacion.md)
4. [Impacto de la explotación de SSRF](04-ssrf-impacto.md)
5. [SSRF ciego](05-ssrf-ciego.md)
6. [Prevención de SSRF](06-ssrf-prevencion.md)
7. [Motores de plantillas y SSTI: conceptos](07-ssti-conceptos.md)
8. [Identificación de SSTI](08-ssti-identificacion.md)
9. [Impacto de la explotación de SSTI](09-ssti-impacto.md)
10. [Prevención de SSTI](10-ssti-prevencion.md)
11. [Inyección SSI (Server-Side Includes)](11-inyeccion-ssi.md)
12. [Inyección XSLT](12-inyeccion-xslt.md)

## Por qué este bloque importa

Estas cuatro vulnerabilidades comparten una característica que las hace especialmente peligrosas: explotadas con éxito, pueden derivar en acceso a sistemas internos normalmente inaccesibles desde fuera (SSRF) o en ejecución remota de código directamente en el servidor (SSTI, SSI, XSLT) — el mismo nivel de impacto que SQL Injection o Command Injection, pero a través de vectores menos conocidos y, por tanto, frecuentemente menos vigilados durante el desarrollo.
