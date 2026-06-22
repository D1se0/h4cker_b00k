# Vulnerabilidades públicas y CVSS

## Por qué buscar vulnerabilidades conocidas es siempre el primer paso

No siempre es necesario (ni eficiente) descubrir una vulnerabilidad desde cero. Muchísimas aplicaciones web —tanto de código abierto como propietarias— son usadas por miles de organizaciones a la vez, lo que significa que también han sido auditadas extensamente por investigadores de todo el mundo. Cuando se descubre y confirma una vulnerabilidad en una de estas aplicaciones, normalmente se le asigna un identificador **CVE** (*Common Vulnerabilities and Exposures*) y se publica, junto a una puntuación de gravedad.

Muchos investigadores también desarrollan y publican **exploits de prueba de concepto** (PoC) para esas vulnerabilidades, con fines educativos y de validación. Esto convierte la búsqueda de exploits públicos en uno de los primeros pasos lógicos al auditar cualquier aplicación de la que se pueda identificar nombre y versión.

## Flujo de trabajo típico

1. **Identificar la aplicación y su versión exacta.** Suele encontrarse en el código fuente, en archivos típicos como `version.php`, `CHANGELOG.md`, en metadatos del HTML, o en cabeceras HTTP.
2. **Buscar exploits públicos** para esa versión concreta en fuentes como [Exploit-DB](https://www.exploit-db.com/), [Rapid7 Vulnerability & Exploit Database](https://www.rapid7.com/db/), o motores de búsqueda generales combinando el nombre, la versión y términos como "exploit" o "CVE".
3. **Priorizar** vulnerabilidades con puntuación CVSS alta (8-10) o que deriven directamente en **ejecución remota de código (RCE)**, sin descartar por completo otras categorías si no hay nada de mayor impacto disponible.
4. **Validar y adaptar** el exploit al entorno concreto — los PoC públicos no siempre funcionan "tal cual" y a menudo requieren ajustes menores.

> **No solo la aplicación principal**: si la aplicación usa componentes externos (plugins, librerías, temas en un CMS), también hay que buscar vulnerabilidades específicas de esos componentes — a menudo son el eslabón más débil, ya que reciben menos escrutinio que el núcleo de la aplicación principal.

## CVSS: el sistema de puntuación de gravedad

El **Common Vulnerability Scoring System (CVSS)** es el estándar de facto para puntuar objetivamente la gravedad de una vulnerabilidad, usado ampliamente por organizaciones y gobiernos para priorizar la respuesta y asignación de recursos.

La puntuación se construye combinando tres grupos de métricas:

- **Base**: características inherentes de la vulnerabilidad, independientes del tiempo o del entorno concreto (es la única que la NVD publica de forma estándar para todas las CVE).
- **Temporal**: factores que cambian con el tiempo (por ejemplo, disponibilidad de un exploit funcional, o de un parche oficial).
- **Environmental**: factores específicos del entorno de cada organización (criticidad del activo afectado, controles compensatorios ya existentes).

### Rangos de gravedad

**CVSS v2.0**

| Gravedad | Rango |
|---|---|
| Bajo | 0.0 – 3.9 |
| Medio | 4.0 – 6.9 |
| Alto | 7.0 – 10.0 |

**CVSS v3.x**

| Gravedad | Rango |
|---|---|
| Ninguno | 0.0 |
| Bajo | 0.1 – 3.9 |
| Medio | 4.0 – 6.9 |
| Alto | 7.0 – 8.9 |
| Crítico | 9.0 – 10.0 |

La [National Vulnerability Database (NVD)](https://nvd.nist.gov/) ofrece calculadoras interactivas oficiales para ambas versiones, donde se puede ajustar cada métrica y observar cómo afecta a la puntuación final — un buen ejercicio para entender qué hace que una vulnerabilidad concreta se considere más o menos grave (por ejemplo, si requiere interacción del usuario, si necesita privilegios previos, si el impacto es solo en confidencialidad o también en integridad y disponibilidad).

## Vulnerabilidades del servidor backend

Más allá de las vulnerabilidades propias de la aplicación, conviene considerar también vulnerabilidades en el servidor web o el sistema operativo subyacente. Las más críticas son las explotables **externamente**, sin necesidad de acceso previo — el caso histórico más conocido es **Shellshock** (CVE-2014-6271), que afectó a servidores Apache que invocaban Bash a través de CGI, permitiendo ejecución remota de comandos simplemente manipulando cabeceras HTTP. Se trata en detalle en el bloque de *Attacking Common Applications*.

Las vulnerabilidades que requieren acceso local previo al servidor o a la red interna (por ejemplo, fallos de escalada de privilegios en el propio sistema operativo) suelen explotarse en una fase posterior del compromiso, tras haber obtenido ya algún punto de apoyo mediante una vulnerabilidad externa — pero siguen siendo igual de críticas de corregir, ya que limitan el alcance de cualquier compromiso inicial.
