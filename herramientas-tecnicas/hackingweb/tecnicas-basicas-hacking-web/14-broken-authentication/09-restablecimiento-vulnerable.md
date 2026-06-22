# Restablecimiento de contraseña vulnerable

## Más allá de la fuerza bruta de tokens: fallos de lógica de negocio

El apartado anterior de este bloque cubrió cómo un token de restablecimiento con espacio de búsqueda insuficiente puede vulnerarse mediante fuerza bruta directa. Pero incluso una aplicación que protege correctamente sus tokens (longitud adecuada, límite de intentos, expiración corta) puede seguir siendo vulnerable si el **diseño lógico** del flujo de restablecimiento contiene un fallo — independientemente de cuán robusto sea el token en sí.

## El problema de fondo de las preguntas de seguridad

Muchas aplicaciones ofrecen, como alternativa o complemento al token enviado por email, un mecanismo basado en "preguntas de seguridad" (ciudad de nacimiento, nombre de una mascota, etc.). El problema estructural de este enfoque es que **la respuesta no es realmente secreta** en el mismo sentido que una contraseña: a menudo es información que puede investigarse (perfiles públicos, redes sociales, registros) o que pertenece a un conjunto relativamente reducido de respuestas plausibles (un número finito y conocido de ciudades grandes, por ejemplo), lo que la hace fundamentalmente distinta —y más débil— que un secreto elegido aleatoriamente por el usuario.

A esto se suma, con frecuencia, un problema de implementación: si la aplicación ofrece la misma lista cerrada de preguntas genéricas a todos los usuarios (en lugar de permitir preguntas personalizadas), el **conjunto de respuestas posibles** para una pregunta como "ciudad de nacimiento" puede acotarse y probarse sistemáticamente — el mismo principio de espacio de búsqueda reducido trabajado en los apartados anteriores de este bloque, aplicado aquí a una respuesta en lenguaje natural en lugar de a un código numérico.

### Por qué esto es, en esencia, el mismo problema que un token débil

Una pregunta de seguridad con un universo de respuestas plausibles relativamente acotado (miles, no millones de combinaciones, y filtrable aún más con cualquier contexto adicional conocido del objetivo) es, conceptualmente, un token débil disfrazado de pregunta personal — comparte la misma vulnerabilidad estructural que un PIN de 4 dígitos: el espacio de búsqueda es manejable y, si no existe protección contra intentos repetidos, fuerza bruta sigue siendo viable.

## Manipulación de parámetros en flujos de restablecimiento multi-paso

Un segundo patrón de fallo, distinto pero igualmente relevante: cuando un flujo de restablecimiento se divide en varios pasos (especificar usuario → responder verificación → establecer nueva contraseña), la aplicación necesita "recordar" a qué usuario corresponde el proceso entre un paso y el siguiente. Si esa asociación se transporta mediante un **parámetro visible y modificable** en lugar de quedar anclada de forma segura al estado de sesión del servidor, existe el riesgo de que ese valor pueda alterarse entre pasos — permitiendo, en el peor caso, que el flujo de verificación completado para un usuario termine aplicándose sobre una cuenta distinta a la que originalmente lo inició.

Este es exactamente el mismo principio de **nunca confiar en un valor que el cliente puede modificar para decisiones de identidad o autorización**, trabajado de forma constante a lo largo de este temario — desde la validación de tipo de archivo del lado del cliente en *File Upload Attacks*, hasta la cabecera `X-Forwarded-For` no validada vista en el apartado anterior de este mismo bloque sobre protección contra fuerza bruta.

## Mitigación

- **Eliminar las preguntas de seguridad como único mecanismo de verificación**, o tratarlas, como mucho, como un factor adicional dentro de un esquema más amplio — nunca como la barrera principal de un restablecimiento de cuenta.
- **Si se usan, exigir respuestas verdaderamente personalizadas** (definidas libremente por el usuario, no elegidas de una lista cerrada de preguntas genéricas) y aplicarles el mismo límite de intentos y protección que a cualquier otro secreto de autenticación.
- **Vincular cada paso de un flujo multi-paso al estado de sesión del servidor**, nunca a un parámetro visible y modificable por el cliente — el servidor, no la petición del usuario, debe ser la única fuente de verdad sobre a qué cuenta corresponde cada paso del proceso.
- **Pruebas de lógica de negocio explícitas**, no solo de fuerza bruta: revisar manualmente cada transición entre pasos del flujo de restablecimiento, comprobando qué ocurre si se altera, omite o repite cualquier parámetro — el mismo enfoque de revisión de lógica de aplicación recomendado de forma recurrente en este temario allí donde la automatización por sí sola no es suficiente.

## Cierre de la sección de ataques de contraseña de este bloque

Con credenciales por defecto y restablecimiento de contraseña vulnerable cubiertos, se completa esta parte del bloque centrada en fallos de proceso y de lógica de negocio en torno a la gestión de contraseñas. Los siguientes apartados abordan un terreno distinto: el **bypass directo de la autenticación**, sin necesidad de obtener ni adivinar ninguna credencial en absoluto.
