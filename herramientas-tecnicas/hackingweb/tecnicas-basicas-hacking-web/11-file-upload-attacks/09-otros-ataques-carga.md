# Otros ataques de carga de archivos

## Más allá del contenido del archivo: el nombre también es entrada de usuario

Hasta ahora este bloque se ha centrado en el **contenido** del archivo subido. Pero el **nombre** del archivo es, en sí mismo, una cadena de texto proporcionada por el usuario — y si la aplicación lo usa después en algún contexto sin la sanitización adecuada, hereda exactamente los mismos riesgos que cualquier otro campo de entrada visto en bloques anteriores de este temario.

### Inyección a través del nombre del archivo

Si el backend incorpora el nombre del archivo subido dentro de un comando del sistema operativo (por ejemplo, al moverlo o renombrarlo con una utilidad externa), un nombre construido con los operadores vistos en el bloque de *Command Injection* podría inyectar un comando adicional — el vector de entrada es distinto (un nombre de archivo en lugar de un campo de formulario directo), pero la causa raíz y la mitigación son idénticas: nunca construir comandos de shell concatenando datos de usuario sin la separación estructural adecuada.

De la misma forma, si el nombre del archivo se muestra después en una página sin escapar (por ejemplo, en una lista de "documentos subidos recientemente"), hereda el mismo riesgo de XSS trabajado en su propio bloque. Y si se usa dentro de una consulta SQL sin parametrizar, el riesgo es el de inyección SQL.

### La lección común

Esto refuerza una idea que ha aparecido constantemente a lo largo de este temario: **cualquier dato que provenga del usuario —incluidos metadatos aparentemente secundarios como un nombre de archivo— debe tratarse con el mismo rigor que un campo de formulario explícito.** No basta con validar el contenido binario del archivo si su nombre se reutiliza después sin las mismas garantías.

## Divulgación de la ubicación de archivos subidos

En formularios donde la aplicación no devuelve directamente un enlace al archivo recién subido (por ejemplo, un formulario de adjuntos en un sistema de tickets), encontrar dónde quedan accesibles esos archivos puede requerir técnicas de reconocimiento adicionales: fuzzing de directorios (visto en el bloque de *Web Fuzzing*), o aprovechar otras vulnerabilidades que permitan leer la estructura de directorios del servidor.

Desde la perspectiva defensiva, esto subraya por qué confiar en que una ruta "no sea fácil de adivinar" nunca debería considerarse una medida de seguridad por sí sola — el mismo principio de "seguridad por oscuridad no es seguridad" que apareció al hablar de `robots.txt` en el bloque de *Information Gathering*.

## Comportamientos específicos de plataforma

Algunos sistemas operativos introducen matices propios en cómo gestionan nombres de archivo que conviene tener presentes al diseñar (o auditar) una funcionalidad de carga:

- **Caracteres reservados del sistema de archivos**: ciertos caracteres tienen un significado especial reservado en algunos sistemas operativos. Si la aplicación no valida ni escapa correctamente el nombre de archivo recibido antes de usarlo en operaciones del sistema, pueden producirse comportamientos no previstos por el desarrollador, incluyendo mensajes de error que revelan información interna.
- **Nombres reservados del sistema operativo**: algunos sistemas reservan ciertos nombres de archivo para fines especiales del propio sistema, lo que puede provocar errores si una aplicación intenta crear un archivo con ese nombre sin contemplarlo.
- **Convenciones de nomenclatura heredadas**: algunos sistemas operativos mantienen, por compatibilidad histórica, formas alternativas y más cortas de referirse a un mismo archivo. Una aplicación que no tenga esto en cuenta podría, en determinadas circunstancias, sobrescribir sin querer un archivo existente al recibir un nombre que coincide con esa forma alternativa.

El denominador común de todos estos casos es el mismo: **el nombre de archivo es una entrada que el sistema operativo interpreta con sus propias reglas**, y una aplicación que no las conozca o no las contemple puede comportarse de forma distinta a la esperada, con consecuencias que van desde la simple divulgación de información hasta la sobrescritura accidental de archivos sensibles.

## Riesgos en el procesamiento posterior del archivo

Cualquier transformación automática que la aplicación aplique al archivo después de recibirlo —generar una miniatura, convertir un formato, extraer metadatos, comprimir o descomprimir— introduce su propia superficie de riesgo si la librería responsable de ese procesamiento no está actualizada o no maneja correctamente entradas malformadas. Esto conecta directamente con lo señalado en la introducción de este bloque: una vulnerabilidad de carga de archivos no siempre nace de un error en el código propio de la aplicación, sino que puede heredarse de un componente de terceros desactualizado.

La defensa frente a esta categoría de riesgo no es distinta de la recomendada para cualquier dependencia externa, vista también en el bloque de *Introducción a Aplicaciones Web*: mantener actualizadas las librerías de procesamiento de archivos, y tratar cualquier archivo recibido de un usuario —incluso ya validado en tipo y contenido— como una entrada potencialmente hostil durante todo su ciclo de procesamiento posterior, no solo en el momento de la carga inicial.

## Cierre conceptual

Este recorrido por vectores "secundarios" —nombre de archivo, ubicación de almacenamiento, comportamiento específico de plataforma, procesamiento posterior— completa la idea central de este bloque: una funcionalidad de carga de archivos segura no se resuelve únicamente filtrando bien la extensión y el contenido en el momento de la subida. Requiere considerar el ciclo de vida completo del archivo dentro de la aplicación — exactamente el enfoque que se sistematiza en el apartado de prevención que cierra este bloque.
