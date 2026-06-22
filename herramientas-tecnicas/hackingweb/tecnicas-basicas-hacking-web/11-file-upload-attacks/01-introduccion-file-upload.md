# Introducción a los ataques de carga de archivos

## Por qué la carga de archivos es tan habitual como sensible

Permitir que los usuarios suban contenido propio (una foto de perfil, un documento, un archivo adjunto) es una funcionalidad casi universal en aplicaciones web modernas: redes sociales, sitios corporativos, plataformas de gestión documental. Pero cada vez que una aplicación acepta un archivo enviado por un usuario, se enfrenta a un riesgo estructural: ese archivo se almacena en el servidor backend, y si su contenido o su tipo no se verifican adecuadamente, puede convertirse en el vehículo perfecto para introducir contenido malicioso directamente dentro de la infraestructura de la aplicación.

Las vulnerabilidades de carga de archivos figuran de forma recurrente entre las más reportadas en bases de datos de CVE, y una proporción significativa de ellas se clasifica con severidad **alta** o **crítica** — un reflejo directo del impacto potencial cuando esta funcionalidad no está correctamente protegida.

## El escenario más grave: carga arbitraria sin autenticación

El caso límite es una aplicación que permite a **cualquier usuario, sin necesidad de iniciar sesión**, subir **cualquier tipo de archivo** sin ninguna restricción. Esto equivale, en la práctica, a ofrecer a cualquier visitante la capacidad de depositar y ejecutar código en el servidor — el escalón de gravedad más alto posible para este tipo de vulnerabilidad.

## El ataque central: ejecución remota de código vía webshell

El ataque más asociado a una carga de archivos insegura es subir un **webshell**: un script (en el lenguaje del backend, normalmente PHP, ASP, o similar) que, una vez accesible vía HTTP, permite ejecutar comandos arbitrarios en el servidor a través de simples peticiones web — exactamente la misma capacidad de impacto que se vio en el bloque de *SQL Injection Fundamentals* al escribir un intérprete PHP mínimo mediante `INTO OUTFILE`. La diferencia aquí es que la carga de archivos ofrece, potencialmente, una vía mucho más directa para lograr lo mismo: no hace falta una inyección SQL previa si el propio formulario de subida ya acepta el archivo malicioso sin restricción.

## Más allá de la ejecución remota de código

Incluso cuando una aplicación **sí** restringe correctamente qué tipos de archivo acepta, pueden existir otros vectores de ataque relevantes aprovechando huecos en la implementación:

- **Introducir otras vulnerabilidades indirectamente**: un archivo SVG o HTML cargado y servido sin las cabeceras adecuadas puede abrir la puerta a XSS; un archivo XML especialmente construido puede explotar XXE (*XML External Entity*, tratado en el bloque de *Web Attacks*).
- **Denegación de servicio (DoS)**: archivos diseñados para consumir recursos desproporcionados al procesarse (descompresión, redimensionado de imágenes, parseo de formatos complejos).
- **Sobrescritura de archivos críticos**: si el nombre o la ruta de destino del archivo subido no se controla adecuadamente, podría sobrescribirse configuración existente del sistema o de la propia aplicación.

## Una causa adicional, más allá del código propio: dependencias desactualizadas

No toda vulnerabilidad de carga de archivos nace de código mal escrito en la propia aplicación. El uso de **librerías o componentes de terceros desactualizados** para procesar archivos subidos (parseo de imágenes, generación de miniaturas, extracción de metadatos) puede introducir vulnerabilidades conocidas y ya documentadas, exactamente la misma idea trabajada en el bloque de *Introducción a Aplicaciones Web* sobre la importancia de buscar CVEs públicos asociados a la pila tecnológica identificada — aplicable aquí específicamente a las librerías de procesamiento de archivos.

## Qué cubre el resto de este bloque

Los siguientes apartados recorren, de menor a mayor sofisticación, los distintos enfoques con que las aplicaciones intentan restringir qué se puede subir (validación de cliente, listas negras, listas blancas, verificación de tipo de contenido), por qué cada uno tiene limitaciones si se aplica de forma aislada, otros vectores de ataque más allá de la ejecución de código, y finalmente un conjunto de medidas de prevención estructurales que, combinadas, reducen el riesgo de forma robusta.
