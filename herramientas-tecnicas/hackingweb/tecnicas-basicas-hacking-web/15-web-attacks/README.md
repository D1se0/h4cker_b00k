# Web Attacks

Este bloque cubre tres vulnerabilidades web adicionales que aparecen con frecuencia en aplicaciones reales y que complementan el panorama trabajado en bloques anteriores: **manipulación de verbos HTTP**, que explota configuraciones incorrectas del servidor para eludir autenticación o filtros de seguridad; **IDOR (Insecure Direct Object Reference)**, el fallo de control de acceso más extendido, que permite acceder a datos de otros usuarios cambiando un identificador; y **XXE (XML External Entity Injection)**, que explota procesadores XML inseguros para filtrar archivos del servidor o establecer canales de comunicación no autorizados.

## Contenido

1. [Introducción a los ataques web](01-introduccion-web-attacks.md)
2. [Manipulación de verbos HTTP: configuraciones inseguras](02-http-verb-tampering-intro.md)
3. [Bypass de autenticación con manipulación de verbos](03-bypass-auth-verbos.md)
4. [Bypass de filtros de seguridad con manipulación de verbos](04-bypass-filtros-verbos.md)
5. [Prevención de manipulación de verbos HTTP](05-prevencion-verbos.md)
6. [Introducción a IDOR](06-introduccion-idor.md)
7. [Identificación de IDOR](07-identificacion-idor.md)
8. [Enumeración masiva y referencias codificadas](08-idor-enumeracion-codificadas.md)
9. [IDOR en APIs](09-idor-apis.md)
10. [Encadenamiento de vulnerabilidades IDOR](10-idor-encadenamiento.md)
11. [Prevención de IDOR](11-prevencion-idor.md)
12. [Introducción a XXE](12-introduccion-xxe.md)
13. [Divulgación de archivos locales con XXE](13-xxe-archivos-locales.md)
14. [Exfiltración ciega con XXE](14-xxe-ciega.md)
15. [Prevención de XXE](15-prevencion-xxe.md)

## Por qué este bloque importa

IDOR ocupa consistentemente el primer puesto en programas de *bug bounty* por número de reportes válidos — es la vulnerabilidad más común y, paradójicamente, una de las más fáciles de encontrar y de reportar con impacto demostrable. Manipulación de verbos y XXE completan el mapa de vectores de ataque estructurales que toda auditoría web debe contemplar sistemáticamente.
