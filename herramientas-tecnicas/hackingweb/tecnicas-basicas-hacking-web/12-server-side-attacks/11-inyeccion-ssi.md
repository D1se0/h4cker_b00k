# Inyección SSI (Server-Side Includes)

## Qué es SSI

**Server-Side Includes (SSI)** es una tecnología más antigua, soportada por servidores web extendidos como Apache e IIS, que permite incorporar contenido generado dinámicamente dentro de páginas HTML mediante directivas embebidas directamente en el propio archivo. Aunque su uso se asocia tradicionalmente a extensiones de archivo como `.shtml`, el servidor puede configurarse para procesar directivas SSI en cualquier extensión — la extensión del archivo, por tanto, **no es una garantía fiable** de si SSI está activo o no.

## Cómo se estructura una directiva SSI

```
<!--#nombre parametro="valor" -->
```

Algunas directivas habituales, a modo ilustrativo del tipo de funcionalidad que SSI expone:

- **Mostrar información del entorno o del documento actual** (nombre de archivo, fecha de última modificación, hora del servidor).
- **Incluir el contenido de otro archivo** dentro de la página actual, normalmente restringido al directorio raíz del sitio.
- **Modificar configuración** del propio procesamiento SSI, como el mensaje mostrado ante un error.
- **Ejecutar un comando del sistema operativo** y mostrar su salida directamente en la página — la directiva de mayor riesgo, ya que conecta directamente SSI con el mismo tipo de impacto trabajado en el bloque de *Command Injection*.

## Cómo se produce la inyección

La inyección SSI ocurre cuando un atacante consigue que una directiva SSI maliciosa termine formando parte de un archivo que el servidor web procesa interpretando SSI. Dos escenarios habituales:

- **A través de una carga de archivos vulnerable** (vista en su propio bloque de este temario): si la aplicación permite subir un archivo con directivas SSI hacia un directorio donde el servidor las procesa, esas directivas se ejecutarán cada vez que se sirva ese archivo.
- **A través de escritura de entrada de usuario en archivos servidos por el servidor**: si una funcionalidad de la aplicación escribe contenido proporcionado por el usuario directamente en un archivo dentro del árbol servido por el servidor web, y ese contenido incluye una directiva SSI bien formada, el servidor la interpretará y ejecutará al servir ese archivo a cualquier visitante posterior.

Una vez más, el mismo patrón estructural: entrada de usuario que termina interpretándose como instrucción —en este caso, una directiva del propio servidor web— en lugar de tratarse como contenido textual inerte.

## El impacto: hasta ejecución remota de código

Dada la existencia de directivas capaces de ejecutar comandos del sistema operativo directamente, una inyección SSI exitosa puede escalar hasta el mismo nivel de gravedad alcanzado por cualquier otra vulnerabilidad de ejecución de código vista en este temario — control completo sobre el servidor afectado.

## Prevención

Las medidas de mitigación combinan, una vez más, validación de entrada con restricción de capacidades a nivel de servidor:

- **Validar y sanear rigurosamente cualquier entrada de usuario** que pudiera, directa o indirectamente, terminar formando parte de un archivo servido con procesamiento SSI activo — el mismo principio aplicado de forma consistente en cada bloque de inyección de este temario.
- **Restringir el procesamiento de SSI a extensiones y directorios específicos**, evitando que el servidor interprete directivas en ubicaciones donde no es estrictamente necesario — reduciendo así la superficie donde una inyección accidental podría llegar a tener efecto.
- **Deshabilitar directivas peligrosas que no sean necesarias**, en particular la directiva de ejecución de comandos, si la funcionalidad de la aplicación no la requiere — el mismo principio de minimizar capacidades innecesarias visto en la prevención de SSTI, aplicado aquí a nivel de configuración del servidor web en lugar del motor de plantillas.

## La lección que se repite, una vez más

SSI es, en esencia, una variación del mismo patrón de inyección trabajado en cada bloque de este temario, aplicado a un mecanismo del propio servidor web en lugar de a una base de datos, un motor de plantillas, o un intérprete de comandos. La causa, el impacto potencial, y la filosofía de prevención son estructuralmente idénticos — lo único que cambia es el componente concreto que interpreta la entrada como instrucción.
