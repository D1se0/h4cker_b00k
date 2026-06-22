# Motores de plantillas y SSTI: conceptos

## Qué es un motor de plantillas

Un motor de plantillas combina una **plantilla** predefinida con datos generados dinámicamente para producir contenido final — habitualmente HTML. El caso de uso más intuitivo: una página que reutiliza el mismo encabezado y pie de página en todo el sitio, mientras el contenido central cambia según la página visitada. Esto evita duplicar la misma estructura HTML una y otra vez, centralizando el mantenimiento del diseño común.

Ejemplos extendidos de motores de plantillas en el ecosistema web: **Jinja2** (Python, usado por Flask y Django), **Twig** (PHP, usado por Symfony), y muchos otros equivalentes en distintos lenguajes y frameworks.

## Cómo funciona, conceptualmente

Un motor de plantillas recibe dos entradas: la **plantilla** en sí (con marcadores de posición predefinidos) y un conjunto de **valores** que deben insertarse en esos marcadores. El proceso de combinar ambos para producir el resultado final se llama *renderizado*.

```
Plantilla:  "Hola {{ nombre }}!"
Valor:      nombre = "Ana"
Resultado:  "Hola Ana!"
```

Más allá de simples sustituciones de variables, los motores de plantillas modernos suelen soportar lógica más compleja —condicionales, bucles, llamadas a funciones— directamente dentro de la sintaxis de la propia plantilla, lo que les da una expresividad cercana a la de un lenguaje de programación de propósito general, aunque limitada a su contexto de renderizado.

## El límite que separa el uso seguro del inseguro

La clave de seguridad en cualquier motor de plantillas está en **dónde** entra la entrada del usuario:

- **Uso seguro**: la entrada del usuario se proporciona como un **valor** que se inserta en un marcador de posición ya existente en la plantilla. El motor sustituye ese valor literalmente, sin interpretarlo como código de plantilla.
- **Uso inseguro (SSTI)**: la entrada del usuario se incorpora **dentro de la propia cadena de la plantilla**, antes de que esta se procese. En ese caso, el motor no distingue entre "la plantilla legítima que el desarrollador escribió" y "el fragmento que el usuario logró insertar" — todo se interpreta y ejecuta como parte de la misma plantilla.

Esta distinción es, una vez más, el mismo principio de fondo repetido en cada bloque de inyección de este temario: separar estructuralmente **dato** de **instrucción**. Cuando esa separación se rompe —porque la entrada del usuario termina formando parte de la instrucción en lugar de quedar confinada a un valor sustituible— aparece la vulnerabilidad.

## Patrones habituales que introducen SSTI sin que el desarrollador lo perciba

- **Concatenar entrada de usuario directamente en la cadena de la plantilla**, antes de pasarla a la función de renderizado — en lugar de pasarla como un valor independiente.
- **Renderizar dos veces la misma plantilla**, donde la salida del primer renderizado (que ya incluye entrada de usuario insertada como texto) se vuelve a tratar como plantilla en un segundo paso — el contenido del usuario, ya "dentro" del texto, se interpreta esta vez como código de plantilla.
- **Permitir que el usuario edite o envíe directamente una plantilla completa** — el caso más evidente de SSTI, donde no hay ninguna separación entre lo que el desarrollador diseñó y lo que el usuario puede modificar.

## Por qué el impacto potencial es tan alto

Dado que los motores de plantillas modernos suelen ofrecer capacidades cercanas a las de un lenguaje de programación completo (acceso a objetos, llamadas a funciones, en algunos casos acceso a librerías del sistema subyacente), una SSTI explotada con éxito puede escalar mucho más allá de simplemente alterar el HTML mostrado — llegando, en el peor caso, a ejecución remota de código completa sobre el servidor, el mismo nivel de gravedad alcanzado en los bloques de *SQL Injection Fundamentals* y *Command Injection*.

## Qué viene a continuación

Los siguientes apartados desarrollan cómo se identifica esta vulnerabilidad durante una auditoría, qué impacto puede llegar a tener en la práctica, y finalmente cómo se previene desde el diseño de la aplicación.
