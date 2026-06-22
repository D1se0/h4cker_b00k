# File Upload Attacks

La carga de archivos es una funcionalidad casi universal en aplicaciones web modernas — fotos de perfil, documentos, adjuntos — y, precisamente por su ubicuidad, una de las superficies de ataque más recurrentes. Este bloque cubre cómo se origina esta clase de vulnerabilidad, los distintos tipos de filtro que las aplicaciones implementan (lista negra, lista blanca, validación de tipo MIME) y por qué cada uno puede fallar si no se combina con los demás, otros ataques posibles más allá de la ejecución remota de código, y un apartado de prevención extenso con las medidas estructurales que sí cierran el problema.

## Contenido

1. [Introducción a los ataques de carga de archivos](01-introduccion-file-upload.md)
2. [Explotación cuando no hay validación](02-explotacion-sin-validacion.md)
3. [El impacto de una carga sin restricciones](03-impacto-carga-libre.md)
4. [Validación del lado del cliente](04-validacion-cliente.md)
5. [Filtros de lista negra](05-filtros-lista-negra.md)
6. [Filtros de lista blanca](06-filtros-lista-blanca.md)
7. [Filtros de tipo de contenido](07-filtros-tipo-contenido.md)
8. [Cuando solo se permiten archivos limitados (imágenes, etc.)](08-carga-limitada.md)
9. [Otros ataques de carga de archivos](09-otros-ataques-carga.md)
10. [Prevención de vulnerabilidades en la carga de archivos](10-prevencion-file-upload.md)

## Por qué este bloque importa

Una carga de archivos mal protegida es, con frecuencia, el camino más directo desde una aplicación web hasta ejecución remota de código en el servidor — sin necesitar siquiera una inyección SQL o de comandos. Y, a diferencia de otras vulnerabilidades, casi cualquier aplicación con un sistema de gestión de contenidos, un foro, una tienda online o un panel de administración tiene en algún punto una funcionalidad de carga de archivos que merece revisión.
