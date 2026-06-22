# Evasión de otros caracteres en lista negra

## Más allá de los separadores de comandos

Algunos filtros no se limitan a bloquear los operadores de encadenamiento (`;`, `&&`, etc.) — también restringen otros caracteres habituales dentro de un payload de explotación, como espacios, barras de ruta, o comillas. Esto obliga a replantear cómo se construye el comando inyectado, no solo cómo se separa del original.

## El espacio como carácter frecuentemente filtrado

El espacio es uno de los caracteres más probables de aparecer en una lista negra, ya que casi cualquier comando con argumentos lo necesita (`cat archivo`, `ls -la`). Los sistemas operativo tipo Unix ofrecen alternativas sintácticas para separar un comando de sus argumentos sin usar literalmente el carácter espacio — por ejemplo, recurriendo a variables de entorno internas que contienen ese carácter, o a secuencias de tabulación equivalentes en determinados contextos de shell.

## Caracteres de ruta y especiales

De forma similar, si la barra (`/`) está filtrada (impidiendo referenciar rutas absolutas como `/etc/passwd`), algunos shells permiten construir esa misma ruta de forma indirecta a partir de variables de entorno o de expansión de comodines, sin que el carácter `/` aparezca de forma literal en el payload enviado.

## El patrón común detrás de todas estas técnicas

Cada lista negra de caracteres bloquea un conjunto concreto de símbolos que sus autores consideraron peligrosos — pero la sintaxis de cualquier shell moderna suele ofrecer **más de una forma** de lograr el mismo resultado. Esto es, en esencia, la misma lección vista en el apartado anterior: una lista negra de caracteres rara vez es exhaustiva frente a la riqueza sintáctica real del intérprete subyacente.

## Por qué esto refuerza, una vez más, la conclusión defensiva

Cuantas más variantes sintácticas existen para lograr el mismo efecto (separar comandos, construir rutas, pasar argumentos), más evidente resulta que **filtrar caracteres específicos nunca puede ser una defensa completa**. La única forma estructuralmente sólida de prevenir la inyección de comandos es evitar por completo que la entrada del usuario llegue a ser interpretada como sintaxis de shell — usando, como se detalla en el apartado de prevención que cierra este bloque, funciones que invocan comandos pasando los argumentos como una lista de valores explícitos, en lugar de construir una cadena de texto que después se entrega a un intérprete de shell completo.
