# Prevención de SSTI

## El principio rector: la entrada del usuario nunca debe llegar a la cadena de la plantilla

Como se estableció en el apartado conceptual de este bloque, la causa raíz de SSTI es que entrada de usuario termina formando parte de la **plantilla en sí**, en lugar de quedar confinada a un **valor** que el motor sustituye sin interpretar. La medida de prevención más directa y efectiva es, por tanto, garantizar estructuralmente esa separación: revisar cuidadosamente cada ruta de código donde se construye una plantilla, confirmando que la entrada del usuario se pasa siempre como un valor a la función de renderizado, nunca concatenada dentro de la cadena de la plantilla antes de esa llamada.

Este es, una vez más, el mismo principio estructural ya trabajado en otros bloques de este temario — las consultas parametrizadas en SQL Injection, las funciones que separan comando de argumentos en Command Injection: separar de forma estructural el código de la aplicación (lo que el desarrollador escribió y controla) de los datos del usuario (lo que nunca debería interpretarse como instrucción).

## Cuando la aplicación necesita aceptar plantillas del usuario por diseño

Algunas aplicaciones tienen, como parte legítima de su funcionalidad, la necesidad de permitir que los usuarios carguen o modifiquen plantillas completas — por ejemplo, sistemas de generación de documentos o de correo personalizable. En estos casos, donde la separación estricta entre "plantilla del desarrollador" y "entrada del usuario" no es viable por diseño, se requieren medidas de contención adicionales.

### Restringir las capacidades del motor de plantillas

Algunos motores ofrecen mecanismos para ejecutar plantillas en un entorno restringido (un *sandbox*), limitando deliberadamente qué funciones y objetos del lenguaje subyacente son accesibles desde dentro de una plantilla. Eliminar o deshabilitar el acceso a funcionalidad potencialmente peligrosa reduce la superficie de lo que una SSTI exitosa podría llegar a alcanzar.

> **Limitación importante de este enfoque**: igual que ocurre con las listas negras vistas en bloques anteriores de este temario, restringir funciones específicas dentro de un motor de plantillas es un enfoque que depende de anticipar correctamente todo lo peligroso — y la superficie de funcionalidad de un lenguaje de programación completo suele ser lo bastante amplia como para que sea difícil garantizar una cobertura exhaustiva. Por sí solo, este enfoque reduce el riesgo pero no lo elimina estructuralmente.

### Aislar el entorno de ejecución del motor de plantillas

La medida estructuralmente más robusta, cuando la aplicación necesita aceptar plantillas controladas por el usuario, es **separar completamente** el entorno donde se renderizan esas plantillas del resto de la infraestructura del servidor — por ejemplo, ejecutando el proceso de renderizado dentro de un contenedor aislado, sin acceso a la red interna ni a los archivos del servidor principal. Con esta separación, incluso si una SSTI llega a su máximo nivel de impacto (ejecución de código), ese código queda confinado a un entorno desechable y sin valor para un atacante más allá de la propia operación de renderizado — el mismo principio de contención mediante aislamiento visto también en el bloque de *File Upload Attacks*.

## La síntesis defensiva

```
1. Garantizar estructuralmente que la entrada de usuario nunca se concatena en la plantilla (la defensa más fuerte)
2. Si la aplicación necesita aceptar plantillas de usuario por diseño:
   a. Restringir las funciones peligrosas accesibles desde el motor (capa adicional, no suficiente por sí sola)
   b. Aislar el entorno de renderizado del resto de la infraestructura (la contención estructural real)
```

Exactamente el mismo patrón de defensa en profundidad que cierra cada bloque de explotación de este temario: ninguna medida aislada es perfecta, pero la combinación de separación estructural de datos e instrucciones, reducción de superficie de ataque, y contención mediante aislamiento reduce el riesgo de forma robusta frente a cualquier intento de explotación de SSTI.

## Cierre del bloque de SSTI

Con esto se completa el recorrido de SSTI: qué son los motores de plantillas y por qué existe esta vulnerabilidad, cómo se identifica, qué rango de impacto puede llegar a tener según el motor afectado, y cómo se previene desde el diseño. El resto de este bloque continúa con las dos últimas clases de vulnerabilidad del lado del servidor: inyección SSI e inyección XSLT, ambas variaciones del mismo patrón de fondo aplicado a tecnologías distintas.
