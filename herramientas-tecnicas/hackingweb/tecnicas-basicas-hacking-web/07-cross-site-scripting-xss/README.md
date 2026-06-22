# Cross-Site Scripting (XSS)

XSS es probablemente la vulnerabilidad web más extendida en la historia de internet, y sigue apareciendo hoy incluso en aplicaciones de gigantes tecnológicos. Este bloque cubre en profundidad los tres tipos de XSS (almacenado, reflejado y basado en DOM), cómo descubrirlos sistemáticamente, y los tres ataques canónicos que se construyen sobre ellos: desfiguración, phishing y secuestro de sesión (incluyendo el caso especial de Blind XSS). Cierra con una guía completa de prevención, tanto en frontend como en backend.

## Contenido

1. [Introducción a XSS](01-introduccion-xss.md)
2. [XSS Almacenado (Stored)](02-xss-almacenado.md)
3. [XSS Reflejado (Reflected)](03-xss-reflejado.md)
4. [XSS basado en DOM](04-xss-dom.md)
5. [Descubrimiento de XSS](05-descubrimiento-xss.md)
6. [Ataque: Desfiguración (Defacing)](06-ataque-desfiguracion.md)
7. [Ataque: Phishing](07-ataque-phishing.md)
8. [Ataque: Secuestro de sesión (Session Hijacking) y Blind XSS](08-session-hijacking.md)
9. [Prevención de XSS](09-prevencion-xss.md)

## Por qué este bloque importa

XSS combina dos factores que lo hacen crítico: es extremadamente común (cualquier campo de entrada sin sanitizar es un candidato) y, cuando es de tipo almacenado, su impacto se multiplica por cada usuario que visite la página afectada — incluyendo administradores con privilegios elevados. Entender XSS en profundidad es también la puerta de entrada conceptual a CSRF, session hijacking, y buena parte de los ataques del lado del cliente que aparecen en bloques posteriores.
