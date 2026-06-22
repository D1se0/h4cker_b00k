# Qué es una aplicación web

## Definición

Una aplicación web es un programa interactivo que se ejecuta dentro de un navegador, siguiendo —en la inmensa mayoría de los casos— una arquitectura **cliente-servidor**: una parte de la lógica (la interfaz, lo que el usuario ve y con lo que interactúa) corre en el navegador del cliente, mientras que otra parte (la lógica de negocio, el acceso a datos) corre en uno o varios servidores remotos.

Gmail, Amazon, Google Docs, cualquier panel de administración corporativo o cualquier API que consume una app móvil son aplicaciones web. No hace falta ser una gran corporación para tener una: cualquier desarrollador puede crear y desplegar una aplicación web en un servicio de *hosting*, lo que explica por qué existen literalmente millones de ellas en internet, con miles de millones de interacciones diarias — y, en consecuencia, una superficie de ataque descomunal.

## Aplicaciones web vs. sitios web estáticos

Antes de que la web se volviera interactiva, lo habitual eran páginas estáticas (la llamada *Web 1.0*): contenido fijo que solo cambiaba si un desarrollador editaba manualmente el archivo HTML. No había lógica de negocio, ni base de datos, ni personalización por usuario.

Las aplicaciones web modernas (*Web 2.0*) presentan contenido **dinámico**, generado en función de la interacción del usuario, su sesión, sus datos almacenados, etc. Características distintivas:

- Son **modulares**: distintas funcionalidades pueden desarrollarse, desplegarse y escalarse de forma independiente.
- Se adaptan a **cualquier tamaño de pantalla** (diseño responsive).
- Funcionan en **cualquier plataforma** sin necesidad de compilación específica — basta un navegador.

## Aplicaciones web vs. aplicaciones nativas

Frente a una aplicación nativa (instalada en el sistema operativo), una aplicación web:

- **No requiere instalación**: se ejecuta remotamente, sin ocupar espacio en disco del cliente más allá de la caché del navegador.
- Garantiza **uniformidad de versión**: todos los usuarios usan siempre la misma versión, actualizada centralizadamente desde el servidor, sin necesidad de distribuir parches a cada cliente.

A cambio, pierde algo de **rendimiento** y **acceso a hardware/librerías nativas** frente a una aplicación instalada localmente — aunque las aplicaciones web progresivas (PWA) e híbridas reducen cada vez más esta brecha.

## Por qué esto importa para un pentester

Cuanto más dinámica y compleja es una aplicación, mayor es su superficie de ataque: más entradas de usuario que procesar, más lógica de negocio que puede tener fallos, más componentes (frontend, backend, base de datos, APIs de terceros) que pueden estar mal configurados o desactualizados.

Un ataque exitoso contra una aplicación web puede tener un impacto desproporcionado respecto al esfuerzo invertido: estas aplicaciones suelen estar conectadas a bases de datos con información sensible de usuarios o de la empresa, y muchas veces sirven de puerta de entrada hacia el resto de la infraestructura interna.

### Ejemplo real de impacto en cadena

Una inyección SQL en una aplicación que usa Active Directory para autenticar usuarios no suele permitir extraer contraseñas directamente (Active Directory las gestiona de forma separada y con hashing fuerte), pero sí puede filtrar la lista completa de **correos electrónicos/nombres de usuario**. Esa lista, a su vez, puede alimentar un ataque de *password spraying* contra un portal corporativo (VPN, Outlook Web Access, Office 365), abriendo una vía de entrada a la red interna de la organización a partir de un fallo "menor" en una aplicación web aparentemente aislada.

Este tipo de encadenamiento de vulnerabilidades —una vulnerabilidad "pequeña" que habilita la siguiente— es el patrón más habitual en compromisos reales, y es la razón por la que entender en profundidad las aplicaciones web es una habilidad transversal en cualquier perfil de pentesting, no solo en quienes se dedican exclusivamente a "web".

## Cómo se aborda normalmente una auditoría web

Un flujo de trabajo habitual sigue, a grandes rasgos, la [Guía de Pruebas de Seguridad Web de OWASP (WSTG)](https://github.com/OWASP/wstg):

1. **Revisión de los componentes de interfaz** (HTML, CSS, JavaScript): buscar exposición de datos sensibles, comentarios olvidados, lógica de validación únicamente en el lado del cliente.
2. **Enumeración de tecnologías de backend**: servidor web, lenguaje, framework, base de datos.
3. **Pruebas funcionales sin autenticación**: qué se puede hacer/ver siendo un usuario anónimo.
4. **Pruebas funcionales con autenticación**: una vez se dispone de credenciales (propias o de prueba), repetir el proceso evaluando control de acceso, lógica de negocio, IDOR, etc.

Esta doble perspectiva (sin y con autenticación) es clave: muchas vulnerabilidades solo aparecen cuando se compara el comportamiento esperado para un rol concreto frente a lo que realmente permite hacer la aplicación.
