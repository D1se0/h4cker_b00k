# API Attacks

Las APIs son la columna vertebral de las aplicaciones modernas — y una de las superficies de ataque más frecuentemente subestimadas. Este bloque sigue el [OWASP API Security Top 10](https://owasp.org/www-project-api-security/) como marco de referencia, cubriendo las diez categorías de riesgo más comunes en APIs REST: desde problemas de control de acceso (BOLA/IDOR, autorización de propiedad rota, autorización de función rota) hasta gestión de recursos, configuración incorrecta, consumo inseguro de APIs de terceros, y SSRF específico de APIs.

## Contenido

1. [Introducción a los ataques a las API](01-introduccion-api-attacks.md)
2. [API1: Autorización a nivel de objeto rota (BOLA/IDOR)](02-bola-idor.md)
3. [API2: Autenticación defectuosa](03-autenticacion-defectuosa.md)
4. [API3: Autorización de nivel de propiedad rota](04-autorizacion-propiedad.md)
5. [API4: Consumo ilimitado de recursos](05-consumo-recursos.md)
6. [API5: Autorización de nivel de función rota](06-autorizacion-funcion.md)
7. [API6: Acceso sin restricciones a flujos de negocio sensibles](07-flujos-negocio.md)
8. [API7: SSRF en APIs](08-ssrf-api.md)
9. [API8: Configuración de seguridad incorrecta](09-configuracion-incorrecta.md)
10. [API9: Gestión inadecuada del inventario](10-inventario-inadecuado.md)
11. [API10: Consumo inseguro de APIs de terceros](11-consumo-inseguro-terceros.md)

## Por qué el OWASP API Top 10 como marco

APIs y aplicaciones web comparten muchas vulnerabilidades, pero las APIs tienen particularidades propias — especialmente en cómo se documentan (o no), cómo gestionan versiones, y cómo su acceso programático las hace más susceptibles a automatización de ataques. El OWASP API Top 10 captura exactamente las categorías donde las APIs difieren más de las aplicaciones web tradicionales en términos de riesgo.
