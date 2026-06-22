# Identificación de SSTI

## Buscando puntos donde la entrada podría llegar a la plantilla

El primer paso para sospechar de SSTI es identificar funcionalidades donde la aplicación toma entrada de usuario y la incorpora de alguna forma al contenido que se renderiza dinámicamente — campos de perfil, mensajes personalizados, plantillas de correo configurables, o cualquier funcionalidad donde el resultado final parece "componerse" a partir de texto introducido por el usuario.

## La prueba de concepto conceptual: sondas de evaluación matemática

La técnica de detección más extendida consiste en introducir una expresión que, si el motor de plantillas la interpreta como código en lugar de como texto literal, produce un resultado evaluado en lugar de mostrar la cadena tal cual se escribió. Si una entrada como una expresión matemática simple se devuelve **resuelta** (mostrando el resultado numérico) en lugar de mostrarse literalmente como el texto que se introdujo, eso confirma que el motor de plantillas está interpretando la entrada como código de plantilla — la señal inequívoca de SSTI.

Esta técnica es conceptualmente idéntica a las pruebas de detección vistas en otros bloques de este temario: en SQL Injection se prueba una condición lógica simple para ver si altera el comportamiento esperado; en XSS se prueba una etiqueta sencilla para ver si se ejecuta como código en lugar de mostrarse como texto. En SSTI, la prueba equivalente consiste en una expresión cuyo resultado evaluado es trivialmente distinguible de su representación literal.

## Por qué la sintaxis exacta de la prueba varía según el motor

Cada motor de plantillas tiene su propia sintaxis para delimitar expresiones evaluables dentro de una plantilla (Jinja2 y Twig, por ejemplo, usan delimitadores similares entre sí por herencia de diseño, pero distintos motores en otros lenguajes usan convenciones propias). Por eso, antes de poder construir una prueba dirigida, conviene primero **identificar qué motor de plantillas** está usando la aplicación — observando, por ejemplo, el lenguaje de backend (técnica vista en el bloque de *Information Gathering*), o probando sucesivamente las sintaxis más comunes hasta observar una reacción reconocible.

## Diferenciando SSTI de otras inyecciones con síntomas similares

Una entrada que provoca un comportamiento inesperado en la respuesta del servidor podría deberse a varias causas distintas — SSTI, pero también XSS, inyección SQL, o simplemente un error de la aplicación no relacionado con seguridad. Confirmar específicamente que se trata de SSTI requiere observar que el comportamiento anómalo es consistente con la **evaluación de una expresión**, no simplemente con la reflexión sin procesar de la entrada (que apuntaría más bien a XSS) ni con un error de base de datos (que apuntaría a SQLi).

## Por qué la identificación correcta del motor condiciona todo lo que viene después

Una vez confirmada la existencia de SSTI y, en la medida de lo posible, identificado el motor de plantillas concreto involucrado, el análisis de impacto y la explotación dependen completamente de las capacidades específicas que ese motor expone — algunos son deliberadamente más restrictivos en lo que permiten evaluar (priorizando la seguridad por diseño), mientras que otros ofrecen acceso mucho más amplio a funcionalidad del lenguaje subyacente. Esta variabilidad entre motores es exactamente lo que se examina en el siguiente apartado, centrado en el impacto real que SSTI puede llegar a tener.
