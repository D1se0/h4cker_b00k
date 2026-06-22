# Impacto de la explotación de SSTI

## Por qué el rango de impacto varía tanto según el motor

A diferencia de otras inyecciones vistas en este temario, donde el impacto potencial es relativamente uniforme entre implementaciones (una inyección SQL exitosa siempre permite, en mayor o menor medida, interactuar con la base de datos), el impacto real de una SSTI depende fuertemente de **qué capacidades expone concretamente el motor de plantillas** afectado. Esto se debe a que cada motor fue diseñado con un equilibrio distinto entre expresividad y seguridad.

## El espectro de impacto, de menor a mayor gravedad

| Nivel de impacto | Qué implica |
|---|---|
| **Divulgación de información limitada** | El atacante puede leer valores de variables o de configuración interna que la plantilla tiene accesibles, sin poder ir más allá |
| **Lectura extendida de objetos y atributos internos** | Algunos motores permiten navegar la jerarquía de objetos del lenguaje subyacente desde dentro de la plantilla, exponiendo potencialmente más información de la que el desarrollador previó |
| **Ejecución de funciones del lenguaje subyacente** | El motor permite invocar funciones del lenguaje de programación en el que está implementado, no solo construcciones propias de la sintaxis de plantillas |
| **Ejecución remota de código completa** | El nivel máximo de gravedad: el atacante logra ejecutar comandos arbitrarios en el servidor, exactamente el mismo desenlace alcanzado en los bloques de *SQL Injection Fundamentals* y *Command Injection* |

No todos los motores de plantillas llegan al nivel más alto de esta escala — algunos están diseñados deliberadamente con un entorno de ejecución restringido (un "sandbox") que limita qué se puede hacer incluso si se logra inyectar y evaluar una expresión arbitraria. Otros, en cambio, conceden por defecto un acceso mucho más amplio al lenguaje de programación subyacente, lo que en la práctica suele traducirse en una vía directa hacia ejecución remota de código si la vulnerabilidad se confirma.

## Por qué esta variabilidad es relevante al documentar un hallazgo

Durante una auditoría, confirmar la existencia de SSTI no es, por sí sola, suficiente para establecer la severidad del hallazgo — hay que determinar, dentro de las capacidades concretas del motor identificado, **hasta dónde llega realmente** el acceso obtenido. Una SSTI confirmada que solo permite leer un par de variables internas tiene un perfil de riesgo sustancialmente distinto a una que permite ejecución de comandos del sistema, aunque ambas compartan la misma causa raíz.

## El paralelismo con otras vulnerabilidades de este temario

Esta misma idea —que la causa raíz es compartida pero el impacto final depende de las capacidades concretas del componente afectado— ya apareció en el bloque de *SQL Injection Fundamentals*: una inyección SQL exitosa puede quedarse en "leer datos de una tabla" o escalar hasta "ejecutar comandos en el servidor", dependiendo de los privilegios del usuario de base de datos y de la configuración del motor concreto. SSTI sigue exactamente el mismo patrón, pero con el motor de plantillas y su configuración de sandboxing como variable determinante en lugar de los privilegios de un usuario de base de datos.

## Qué viene a continuación

El siguiente apartado cierra el bloque de SSTI con las medidas de prevención — que, a diferencia del impacto (variable según el motor), comparten un mismo conjunto de principios estructurales aplicables independientemente de la tecnología concreta utilizada.
