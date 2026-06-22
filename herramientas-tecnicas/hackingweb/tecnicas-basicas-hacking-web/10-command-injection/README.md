# Command Injection

La inyección de comandos del sistema operativo es una de las vulnerabilidades de mayor impacto en aplicaciones web: cuando la entrada del usuario llega sin sanitizar a una función que ejecuta comandos del sistema, un atacante puede ejecutar código arbitrario directamente en el servidor backend. Este bloque cubre cómo se origina esta clase de vulnerabilidad, cómo se detecta y explota de forma básica, los distintos operadores de inyección disponibles, las técnicas de evasión de filtros más habituales, y finalmente las medidas de prevención que cierran el círculo desde la perspectiva defensiva.

## Contenido

1. [Introducción a las inyecciones de comandos](01-introduccion-command-injection.md)
2. [Detección de la vulnerabilidad](02-deteccion.md)
3. [Explotación básica: inyectando el primer comando](03-explotacion-basica.md)
4. [Otros operadores de inyección](04-operadores-inyeccion.md)
5. [Identificación de filtros](05-identificacion-filtros.md)
6. [Evasión de caracteres especiales filtrados](06-evasion-caracteres.md)
7. [Evasión de otros caracteres en lista negra](07-evasion-lista-negra.md)
8. [Evasión de comandos bloqueados](08-evasion-comandos.md)
9. [Ofuscación avanzada de comandos](09-ofuscacion-avanzada.md)
10. [Herramientas de evasión automatizada](10-herramientas-evasion.md)
11. [Prevención de la inyección de comandos](11-prevencion.md)

## Por qué este bloque importa

A diferencia de SQLi, que compromete una base de datos, una inyección de comandos exitosa compromete directamente el **sistema operativo** del servidor — el salto de gravedad es inmediato. Entender tanto la mecánica básica como las técnicas de evasión de filtros es esencial porque, en la práctica, raramente se encuentra una inyección de comandos completamente sin protección: casi siempre hay algún filtro, lista negra, o validación parcial que hay que entender y sortear con criterio.
