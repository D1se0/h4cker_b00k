# Ataques a tokens de sesión

## Por qué el token de sesión es tan crítico como la propia contraseña

Como se vio en el bloque de *Web Requests*, una vez que un usuario se autentica, la aplicación le asigna un **token de sesión** (normalmente transportado en una cookie) que el navegador reenvía en cada petición posterior, evitando reintroducir credenciales constantemente. Esto tiene una implicación de seguridad directa: **si un atacante obtiene un token de sesión válido de otro usuario, puede suplantarlo completamente** sin necesitar jamás su contraseña — el mismo principio de *session hijacking* trabajado en detalle en el bloque de *Cross-Site Scripting*, pero aquí abordado desde el ángulo de **cómo se genera** el token, no de cómo se roba.

## Primer fallo: tokens con entropía insuficiente

Un token de sesión solo es una defensa real si resulta computacionalmente inviable de adivinar. Esto falla en dos variantes habituales:

- **Token demasiado corto**: un identificador de pocos caracteres tiene, exactamente como cualquier PIN o código corto trabajado en apartados anteriores de este bloque, un espacio de búsqueda reducido susceptible de fuerza bruta directa.
- **Token mayormente estático**: un token que parece largo y aleatorio a primera vista, pero donde la mayor parte de sus caracteres son siempre **idénticos** entre sesiones distintas, reduce su entropía efectiva al tamaño de la porción realmente variable — capturando varios tokens emitidos por la misma aplicación y comparándolos carácter a carácter, se puede detectar qué parte es constante y cuál cambia, revelando el verdadero (y mucho menor) espacio de búsqueda real.
- **Identificadores secuenciales**: si los tokens emitidos son números consecutivos o casi consecutivos, enumerar sesiones ajenas (pasadas o futuras) se reduce a incrementar o decrementar un contador — el caso más extremo y trivial de entropía insuficiente.

La técnica de detección común a las tres variantes es la misma: **capturar múltiples tokens emitidos por la aplicación y compararlos entre sí**, buscando patrones, partes constantes, o progresión predecible — exactamente el mismo principio de "observar el comportamiento real para inferir la lógica interna" aplicado de forma recurrente a lo largo de este temario.

## Segundo fallo: tokens predecibles por contener datos manipulables

Una categoría de fallo más sutil —y más grave— ocurre cuando el token de sesión no es un identificador opaco y aleatorio, sino una estructura que **codifica directamente información del usuario** (su nombre, su rol) sin ninguna protección criptográfica que impida su manipulación.

### Por qué la codificación no es protección

Como se ha repetido en varios bloques de este temario (especialmente en *Web Proxies*, al hablar de Base64), **codificar no es lo mismo que cifrar o firmar**. Base64, hexadecimal, o codificación URL son transformaciones completamente reversibles sin necesidad de ninguna clave — cualquiera que reconozca el patrón puede decodificar el contenido, **y volver a codificarlo tras modificarlo**, sin que la aplicación tenga ninguna forma de detectar que el valor ha sido alterado.

Si un token de sesión contiene, una vez decodificado, datos estructurados como `usuario=nombre;rol=user` sin ninguna firma criptográfica que valide su integridad, la aplicación no tiene manera de distinguir un token legítimo emitido por el servidor de uno construido por un atacante con el mismo formato pero contenido alterado — el servidor confía ciegamente en cualquier dato que llegue con la estructura esperada, sea cual sea su origen real.

Esta vulnerabilidad puede aparecer codificada de formas distintas (Base64, hexadecimal, codificación URL) — el principio de fondo es siempre el mismo: si los datos del token son legibles y reconstruibles sin necesidad de ninguna clave secreta, no hay ninguna garantía real de que ese token provenga genuinamente del servidor.

## Mitigación

- **Generar tokens con un generador de números aleatorios criptográficamente seguro (CSPRNG)**, nunca con contadores secuenciales, marcas de tiempo predecibles, ni concatenaciones parcialmente estáticas.
- **Longitud suficiente**: un token de sesión debe tener una longitud y un alfabeto de caracteres que hagan su espacio de búsqueda computacionalmente inviable de agotar por fuerza bruta — equivalente, en términos de entropía, a una contraseña fuerte.
- **Nunca codificar datos de identidad/privilegio de forma reversible sin protección**: si el token necesita transportar información estructurada, debe ir **firmado criptográficamente** (de forma que cualquier alteración del contenido invalide la firma) o, mejor aún, ser un identificador opaco que el servidor usa únicamente para consultar el estado real de la sesión en su propio almacenamiento — nunca un valor que el cliente pueda reconstruir y volver a presentar con contenido modificado.
- **Mecanismos estándar bien auditados**, como JWT firmado correctamente (verificando siempre la firma, no solo decodificando el contenido) o identificadores de sesión opacos gestionados server-side, en lugar de esquemas de codificación caseros — el mismo principio de "no reinventar mecanismos de seguridad cuando existen soluciones estándar ya auditadas" aplicable a cualquier control criptográfico.

## Por qué esta vulnerabilidad es tan grave en la práctica

A diferencia de otras vulnerabilidades de este bloque que requieren, como mínimo, fuerza bruta contra un espacio de valores limitado, un token de sesión predecible **por estructura** (no solo por longitud) puede permitir construir directamente una sesión con cualquier privilegio deseado, sin necesidad de probar ningún valor — el salto de "usuario normal autenticado" a "administrador" se reduce, en el peor caso, a modificar un único campo de texto reconocible y volver a codificarlo.

## Conectando con el siguiente apartado

Más allá de cómo se genera el token, existen otros fallos relacionados con **cómo se gestiona** durante todo el ciclo de vida de una sesión — qué ocurre tras un logout, si el token cambia tras un cambio de privilegio, o si puede reutilizarse después de haber sido invalidado. El siguiente apartado, que cierra este bloque, desarrolla estas variantes adicionales de ataques de sesión.
