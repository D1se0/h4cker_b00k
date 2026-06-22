# SSRF: qué es y por qué importa

## Definición

**SSRF (Server-Side Request Forgery)** es una vulnerabilidad —incluida en el [Top 10 de OWASP](https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery_%28SSRF%29/)— que ocurre cuando una aplicación web obtiene un recurso remoto (normalmente vía una petición HTTP) basándose en una URL o dirección que el usuario controla, sin verificar adecuadamente hacia dónde se dirige esa petición. El resultado: el atacante puede hacer que **el propio servidor** realice peticiones hacia destinos arbitrarios elegidos por él.

## Por qué esto es diferente de "simplemente" hacer una petición HTTP por su cuenta

La clave de SSRF está en que la petición la origina el **servidor**, no el atacante directamente. Esto importa porque el servidor suele tener una posición de red privilegiada: puede tener acceso a sistemas internos, servicios de infraestructura, o metadatos de la nube que **no son alcanzables directamente desde internet**. Forzar al servidor a hacer esa petición en su nombre es, en la práctica, usar al servidor como un "trampolín" hacia una red a la que el atacante no tendría acceso de ninguna otra forma.

## El papel del esquema de la URL

Cuando la aplicación confía en el esquema (`http://`, `file://`, etc.) proporcionado por el usuario, sin restringirlo, el riesgo se amplía más allá de simples peticiones HTTP:

| Esquema | Qué permite, conceptualmente |
|---|---|
| `http://` / `https://` | Petición HTTP estándar — el caso más común, usado para alcanzar servicios internos no expuestos públicamente |
| `file://` | Lectura de archivos del sistema de ficheros local del servidor — un punto de convergencia con la inclusión de archivos locales (LFI), tratada en su propio bloque de este temario |
| Otros esquemas no estándar | Algunos entornos permiten que la aplicación interprete protocolos adicionales con su propia sintaxis, ampliando potencialmente el alcance de lo que se puede alcanzar a través de la vulnerabilidad |

Esta es exactamente la razón por la que **restringir explícitamente qué esquemas se aceptan** es una de las primeras medidas de mitigación que se desarrolla en el apartado de prevención de este bloque.

## El impacto en términos generales

Una SSRF explotada con éxito puede permitir:

- **Acceso a sistemas internos** normalmente protegidos por estar fuera del alcance de internet — bases de datos, paneles de administración internos, servicios de infraestructura.
- **Elusión de controles perimetrales** (firewalls, listas de bloqueo por IP) que protegen esos sistemas internos, precisamente porque la petición se origina **desde dentro** de la red, no desde el exterior.
- **Exposición de información de configuración interna**, en entornos cloud donde existen servicios de metadatos accesibles solo desde dentro de la propia infraestructura.

## El siguiente paso: cómo se reconoce esta vulnerabilidad

El apartado siguiente desarrolla cómo identificar, durante una auditoría, que una funcionalidad concreta de una aplicación es susceptible de SSRF — observando qué parámetros aceptan URLs y cómo la aplicación procesa la respuesta de esa petición intermedia.
