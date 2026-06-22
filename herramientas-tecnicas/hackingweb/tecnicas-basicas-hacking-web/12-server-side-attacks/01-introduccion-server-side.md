# Introducción a los ataques del lado del servidor

## La distinción clave: cliente vs. servidor

A lo largo de este temario se han trabajado vulnerabilidades de ambos lados de la arquitectura cliente-servidor vista en el bloque de *Introducción a Aplicaciones Web*. XSS, por ejemplo, ataca al **cliente**: el código malicioso se ejecuta en el navegador de otro usuario, no en la infraestructura del servidor. Los ataques del lado del servidor invierten ese objetivo: el código o la lógica maliciosa se ejecuta o se procesa directamente en la infraestructura que aloja la aplicación.

Esta distinción importa porque condiciona tanto el impacto potencial como la metodología de detección: una vulnerabilidad del lado del servidor compromete directamente los activos que la organización aloja —datos, sistemas internos, capacidad de cómputo— mientras que una del lado del cliente compromete, en primera instancia, a usuarios individuales de la aplicación.

## Las cuatro clases cubiertas en este bloque

| Vulnerabilidad | Qué explota |
|---|---|
| **SSRF** (Server-Side Request Forgery) | El servidor realiza peticiones HTTP en nombre del atacante hacia destinos que este controla o elige |
| **SSTI** (Server-Side Template Injection) | El motor de plantillas del servidor interpreta entrada de usuario como código de plantilla en lugar de como texto plano |
| **Inyección SSI** (Server-Side Includes) | El servidor web interpreta directivas SSI inyectadas dentro de contenido controlado por el usuario |
| **Inyección XSLT** | El procesador de transformaciones XML del servidor ejecuta instrucciones inyectadas en una hoja de estilo XSLT |

## El patrón común, una vez más

Cada una de estas cuatro vulnerabilidades repite la misma estructura de fondo que ha aparecido en cada bloque de inyección de este temario: **entrada de usuario que llega a un intérprete sin la separación adecuada entre "dato" e "instrucción"**. Lo que cambia en cada caso es el intérprete concreto involucrado — un cliente HTTP interno en SSRF, un motor de renderizado de plantillas en SSTI, el propio servidor web en SSI, un procesador XSLT en el último caso.

## Por qué merecen un bloque propio, aparte de SQLi y Command Injection

Aunque comparten la misma causa raíz conceptual, estas cuatro vulnerabilidades tienen mecanismos de explotación y superficies de impacto suficientemente distintas como para merecer un tratamiento específico:

- **SSRF** no inyecta código ejecutable — manipula **a quién** se dirige una petición que el servidor ya iba a realizar, lo que la convierte en un vector de acceso a redes internas normalmente inaccesibles desde fuera.
- **SSTI** explota motores de plantillas (Jinja2, Twig, y muchos otros), cada vez más comunes en aplicaciones web modernas que generan HTML dinámicamente — y su impacto potencial llega hasta ejecución remota de código completa.
- **SSI** es una tecnología más antigua, pero sigue presente en servidores web heredados o mal configurados, con el mismo potencial de impacto.
- **XSLT** afecta específicamente a aplicaciones que procesan y transforman documentos XML — un escenario cada vez menos común, pero todavía presente en sistemas empresariales y servicios web tipo SOAP (visto en el bloque de *Web Requests*).

## Cómo se organiza el resto de este bloque

Cada una de las cuatro vulnerabilidades se trabaja siguiendo la misma estructura: qué es y por qué ocurre, cómo se identifica durante una auditoría, qué impacto puede llegar a tener, y finalmente cómo se previene desde el diseño — el mismo recorrido aplicado consistentemente a cada clase de vulnerabilidad vista hasta ahora en este temario.
