# Prevención de SSRF

## Las dos capas donde se puede mitigar SSRF

Las medidas de prevención de SSRF se aplican en dos niveles distintos: la **capa de aplicación** (cómo se valida y procesa la URL proporcionada por el usuario) y la **capa de red** (qué puede alcanzar el servidor, independientemente de lo que la aplicación intente hacer). Una defensa robusta combina ambas, exactamente con la misma filosofía de defensa en profundidad aplicada en cada bloque de este temario.

## Capa de aplicación: validar con lista blanca, nunca con lista negra

Cuando la funcionalidad de la aplicación requiere obtener datos de un host remoto a partir de información del usuario, el principio rector es el mismo trabajado en el bloque de *File Upload Attacks*: definir explícitamente **qué destinos están permitidos**, en lugar de intentar enumerar cuáles están prohibidos.

- **Lista blanca de destinos**: si la aplicación solo necesita comunicarse con un conjunto reducido y conocido de servicios externos, restringir las peticiones salientes exclusivamente a esos destinos —por dominio, o idealmente por dirección IP resuelta— elimina la posibilidad de que un atacante redirija la petición hacia un destino arbitrario.
- **Restricción del esquema de URL**: como se vio en el apartado introductorio de este bloque, permitir esquemas como `file://` u otros no estrictamente necesarios amplía innecesariamente la superficie de ataque. Si la funcionalidad solo necesita realizar peticiones HTTP/HTTPS, cualquier otro esquema debería rechazarse explícitamente.
- **Validación y saneamiento de la entrada**: cualquier dato proporcionado por el usuario que vaya a usarse para construir una petición saliente debe tratarse con el mismo rigor que cualquier otra entrada de usuario trabajada en este temario — nunca confiar en que el formato recibido es el esperado sin verificarlo explícitamente en el servidor.

## Capa de red: limitar qué puede alcanzar el servidor, independientemente de la aplicación

Incluso con una validación de aplicación cuidadosa, una segunda capa de defensa a nivel de red reduce el impacto si, pese a todo, la validación de la aplicación falla:

- **Reglas de firewall restrictivas en las conexiones salientes**: en lugar de permitir que el servidor de aplicación inicie conexiones hacia cualquier destino, restringir explícitamente hacia qué direcciones y puertos puede conectarse — de forma que, aunque una SSRF lograra construirse, el firewall bloquee la conexión saliente hacia destinos no autorizados antes de que llegue a completarse.
- **Segmentación de red**: ubicar el servidor de aplicación en un segmento de red que no tenga visibilidad directa hacia sistemas internos sensibles (paneles de administración, bases de datos, servicios de infraestructura) limita drásticamente lo que una SSRF exitosa podría llegar a alcanzar, incluso si la propia aplicación no implementara ninguna validación adicional.

## Por qué la combinación de ambas capas es la defensa robusta

Confiar únicamente en la validación de la aplicación deja al servidor expuesto si, en algún momento, esa validación tiene un fallo no anticipado. Confiar únicamente en restricciones de red, sin validar nada en la aplicación, sigue permitiendo SSRF hacia cualquier destino que la política de red no haya contemplado explícitamente. La combinación de ambas —validación estricta en el código más contención a nivel de infraestructura— es lo que reduce el riesgo de forma estructural, en lugar de depender de una única línea de defensa.

## Recurso de referencia

La [Guía de Prevención de SSRF de OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) desarrolla estas medidas con mayor detalle técnico específico por plataforma, y es la referencia recomendada para profundizar más allá del nivel conceptual cubierto en este bloque.

## Cierre del apartado de SSRF

Con esto se completa el recorrido de SSRF dentro de este bloque: qué es, cómo se identifica, qué impacto puede llegar a tener (visible y ciega), y cómo se previene desde ambas capas, aplicación y red. El resto de este bloque continúa con SSTI, la siguiente clase de vulnerabilidad del lado del servidor, que comparte el mismo patrón conceptual de fondo aplicado ahora a un contexto distinto: los motores de plantillas.
