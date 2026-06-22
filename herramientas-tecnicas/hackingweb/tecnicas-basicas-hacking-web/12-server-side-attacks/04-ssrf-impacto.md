# Impacto de la explotación de SSRF

## Qué puede llegar a alcanzar un atacante a través del servidor

Una vez confirmada una SSRF, el alcance real del impacto depende enteramente de **qué hay accesible desde la red interna del servidor** — algo que varía completamente de un entorno a otro. Conceptualmente, los escenarios de mayor riesgo incluyen:

- **Servicios internos sin autenticación propia**, que confían en estar protegidos únicamente por no ser alcanzables desde fuera de la red — paneles de administración, interfaces de gestión de bases de datos, colas de mensajería, dashboards de monitorización. Si SSRF permite alcanzarlos, esa "protección por inaccesibilidad" deja de existir.
- **Servicios de metadatos en entornos cloud**, accesibles únicamente desde dentro de la propia infraestructura del proveedor, que en configuraciones inseguras pueden exponer información sensible sobre el entorno de ejecución.
- **Otros servidores de la misma red interna**, ampliando el reconocimiento más allá del propio servidor vulnerable — el mismo principio de "una vulnerabilidad como punto de apoyo para alcanzar el resto de la infraestructura" repetido a lo largo de este temario.

## El reconocimiento de red como primer paso de la explotación

Antes de poder aprovechar cualquiera de estos escenarios, suele ser necesario primero **descubrir qué existe** en la red interna alcanzable desde el servidor — qué direcciones y puertos responden, y qué tipo de servicio hay detrás de cada uno. Esto se apoya en el mismo tipo de razonamiento por diferencias de respuesta visto en el bloque de *Web Fuzzing*: comparar cómo responde la aplicación cuando la SSRF apunta a un destino que existe frente a uno que no, infiriendo así un mapa de la red interna sin tener acceso directo a ella.

## Por qué este reconocimiento puede automatizarse, y por qué eso no cambia el riesgo de fondo

Igual que ocurre con el descubrimiento de directorios o de subdominios (vistos en bloques anteriores), explorar sistemáticamente un rango de direcciones o puertos a través de una SSRF es, en esencia, un problema de fuzzing: se prueba una secuencia de valores y se observan las diferencias de respuesta para distinguir "existe" de "no existe". El hecho de que este proceso pueda automatizarse no cambia el riesgo subyacente — simplemente acelera la fase de reconocimiento, igual que ocurre con cualquier otra vulnerabilidad de este temario.

## Cuándo el impacto se vuelve crítico

El salto de gravedad más significativo ocurre cuando, a través de SSRF, se llega a alcanzar un servicio interno que **a su vez** es vulnerable a algo más: una interfaz de administración sin autenticación, una base de datos con credenciales débiles, o un endpoint que permite ejecutar comandos. En ese punto, SSRF deja de ser "solo" una vulnerabilidad de acceso a red y se convierte en el primer eslabón de una cadena de compromiso más amplia — exactamente el mismo patrón de encadenamiento de vulnerabilidades mencionado en el bloque de *Introducción a Aplicaciones Web*.

## Qué viene después

El siguiente apartado trata el caso de **SSRF ciega**, donde no se dispone de visibilidad directa sobre el contenido de las respuestas obtenidas, y cómo ese escenario condiciona —y limita— qué información puede inferirse razonablemente.
