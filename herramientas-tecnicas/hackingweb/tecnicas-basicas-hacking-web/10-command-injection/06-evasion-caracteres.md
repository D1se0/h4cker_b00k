# Evasión de caracteres especiales filtrados

## El principio general

Cuando un filtro bloquea los separadores de comandos más obvios (`;`, `&&`, `||`...), conviene recordar que esos no son las **únicas** formas de inyectar un segundo comando — son simplemente las más conocidas. La tabla de operadores vista en apartados anteriores incluye variantes (pipe, backticds, subshells `$()`) que pueden quedar fuera de una lista negra construida apresuradamente.

## Por qué las listas negras de caracteres son frágiles por diseño

Una lista negra solo bloquea lo que sus autores **anticiparon explícitamente**. La sintaxis de cualquier shell de sistema operativo es rica y tiene múltiples formas de lograr el mismo efecto — encadenar comandos, sustituir variables, expandir rutas — lo que hace extremadamente difícil enumerar exhaustivamente todos los caracteres y combinaciones peligrosas sin, en algún momento, bloquear también funcionalidad legítima de la aplicación.

Esta es precisamente la razón por la que, en el apartado de prevención que cierra este bloque, las listas blancas de entrada esperada (en lugar de listas negras de lo prohibido) se consideran una defensa estructuralmente más sólida — el mismo principio que distingue validación de sanitización visto también en el bloque de XSS.

## Cómo abordar la evasión con criterio

1. **Mapear exactamente qué está bloqueado**, usando la metodología de aislamiento del apartado anterior — probar cada carácter de la tabla de operadores de forma individual.
2. **Identificar qué operadores, si los hay, no están cubiertos** por el filtro — a menudo una lista negra cubre los separadores más citados en documentación pública pero olvida variantes menos comunes.
3. **Considerar codificaciones alternativas** del mismo carácter, si el filtro opera sobre el valor en crudo antes de decodificar la entrada — un escenario análogo al de evasión de filtros de XSS visto en el bloque correspondiente, donde la codificación URL o de entidades HTML podía sortear un filtro que solo comprobaba el texto literal.

## Por qué este conocimiento importa también desde la perspectiva defensiva

Entender por qué las listas negras de caracteres son insuficientes no es solo útil para quien hace pruebas de penetración autorizadas — es la justificación técnica de por qué cualquier desarrollador debería evitar depender de ellas como única defensa. El apartado de prevención de este bloque desarrolla en detalle qué alternativas son estructuralmente más robustas: funciones de ejecución que separan explícitamente comando y argumentos (evitando que la shell interprete el argumento como sintaxis), y listas blancas que solo permiten el conjunto mínimo de caracteres realmente necesario para la funcionalidad concreta.
