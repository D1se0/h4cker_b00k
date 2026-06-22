# Evasión de comandos bloqueados

## La segunda capa de lista negra: nombres de comando

Además de filtrar caracteres separadores, algunas aplicaciones intentan bloquear directamente **nombres de comandos** considerados peligrosos (`whoami`, `cat`, `nc`, `bash`...), buscando esas cadenas literales dentro de la entrada recibida.

## Por qué este enfoque es todavía más frágil que filtrar caracteres

Una lista negra de caracteres al menos opera sobre un conjunto relativamente pequeño y bien definido de símbolos. Una lista negra de **comandos**, en cambio, intenta anticipar un universo prácticamente ilimitado: cualquier sistema operativo incluye decenas de utilidades capaces de leer archivos, listar directorios o ejecutar acciones equivalentes, y los shells modernos ofrecen múltiples formas de invocar el mismo binario sin que su nombre aparezca de forma literal y reconocible en la cadena enviada (rutas alternativas, alias, variables, o construcción dinámica del nombre a partir de fragmentos).

Esto convierte el bloqueo de comandos por nombre en una medida que, en el mejor de los casos, detiene los intentos más obvios y documentados, pero que no representa una barrera real para alguien que entienda la sintaxis del intérprete subyacente.

## La conclusión que se repite en cada capa de este problema

Tanto si el filtro opera sobre caracteres como sobre nombres de comando, el patrón de fondo es el mismo ya identificado en los apartados anteriores: **una lista negra solo bloquea lo que sus autores anticiparon**, y la superficie real de variantes sintácticas disponibles en cualquier shell de uso general es demasiado amplia para enumerar exhaustivamente. Cuantas más capas de listas negras se acumulan intentando tapar huecos sucesivos, más evidente resulta que el problema no se está resolviendo en su causa raíz, sino parcheando sus síntomas uno a uno.

## Por dónde sigue este bloque

El resto de apartados de evasión de filtros profundiza brevemente en esta misma idea (ofuscación de comandos, herramientas automatizadas de prueba), pero el valor real para cualquier persona que construya o audite aplicaciones está en el apartado final de **Prevención**, que es donde se explica con detalle qué alternativas sí resuelven el problema de forma estructural — y es, deliberadamente, el apartado más extenso y detallado de todo este bloque.
