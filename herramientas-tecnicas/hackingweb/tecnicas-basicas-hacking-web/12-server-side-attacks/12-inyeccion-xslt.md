# Inyección XSLT

## Qué es XSLT

**XSLT (Extensible Stylesheet Language Transformations)** es un lenguaje pensado para transformar documentos XML — seleccionar nodos concretos, reordenarlos, filtrarlos, y combinarlos con texto estático para producir una salida final, habitualmente HTML. Es relevante recordar, conectando con el bloque de *Web Requests*, que XML es la base sobre la que se construyen tecnologías como SOAP, lo que hace que XSLT siga apareciendo en sistemas empresariales y servicios web que procesan ese tipo de formato.

Conceptualmente, una hoja de estilo XSLT funciona de forma similar a una plantilla (en el sentido visto en el apartado de SSTI de este mismo bloque): combina una estructura predefinida con datos extraídos dinámicamente de un documento XML de origen, para producir el resultado final.

## Cómo se produce la inyección

La inyección XSLT ocurre exactamente con el mismo patrón estructural trabajado en SSTI, pero aplicado a hojas de estilo XSLT en lugar de plantillas de un motor de renderizado: cuando entrada proporcionada por el usuario se incorpora **dentro de los propios datos XSLT** antes de que el procesador genere la salida final, en lugar de insertarse únicamente como un valor sustituido de forma segura. Si el atacante logra insertar elementos XSL adicionales dentro de esa estructura, el procesador los interpretará y ejecutará como parte legítima de la transformación.

## Por qué el impacto puede ser significativo

El lenguaje XSLT, más allá de operaciones simples de selección y formateo, incluye en algunas de sus versiones e implementaciones capacidades que se extienden hacia funcionalidad más cercana a la de un lenguaje de programación de propósito general — dependiendo del procesador XSLT concreto utilizado por la aplicación. Esto hace que, igual que ocurría con SSTI, el rango de impacto real de una inyección XSLT dependa fuertemente de las capacidades específicas que el procesador en uso expone, pudiendo llegar en los escenarios más graves hasta divulgación de información sensible del servidor o ejecución de código.

## La conexión con el resto de este bloque

Inyección XSLT comparte la misma estructura conceptual que cada una de las vulnerabilidades trabajadas en este bloque: entrada de usuario que termina mezclada con la lógica de transformación/renderizado, en lugar de quedar confinada a un valor de datos puro. La diferencia, una vez más, está únicamente en el componente concreto que interpreta esa entrada — aquí, un procesador de transformaciones XML en lugar de un motor de plantillas HTML, un servidor web procesando directivas SSI, o un cliente HTTP interno en el caso de SSRF.

## Prevención

Las medidas de prevención siguen el mismo principio rector que el resto de este bloque:

- **Nunca insertar entrada de usuario directamente dentro de los datos de la hoja de estilo XSLT** antes de que el procesador genere la salida — la misma separación estructural entre dato e instrucción trabajada de forma consistente en SSTI y en cada bloque de inyección de este temario. Si la aplicación necesita personalizar la salida según entrada del usuario, esa entrada debe proporcionarse como un valor que el procesador sustituye, nunca como parte de la propia estructura de transformación.
- **Restringir las capacidades del procesador XSLT** utilizado, deshabilitando funcionalidad avanzada que la aplicación no necesite realmente — reduciendo así la superficie de lo que una inyección, si llegara a producirse, podría llegar a alcanzar.
- **Mantener actualizado el procesador XSLT** utilizado por la aplicación, ya que —como se mencionó en el bloque de *Introducción a Aplicaciones Web* respecto a componentes de terceros en general— vulnerabilidades conocidas en versiones desactualizadas de estas librerías pueden ampliar significativamente el impacto disponible incluso en escenarios donde la validación de entrada propia de la aplicación es razonablemente cuidadosa.

## Cierre del bloque de Server-side Attacks

Con esto se completa el recorrido de las cuatro vulnerabilidades del lado del servidor cubiertas en este bloque: SSRF, SSTI, SSI y XSLT. Las cuatro, pese a operar sobre componentes técnicamente muy distintos —un cliente HTTP interno, un motor de plantillas, el propio servidor web, un procesador de transformaciones XML—, comparten exactamente el mismo patrón conceptual de fondo que ha recorrido todo este temario desde el bloque de *SQL Injection Fundamentals*: la ausencia de una separación estructural robusta entre la entrada que controla el usuario y la lógica que el servidor interpreta y ejecuta. Interiorizar este patrón común es, como se señaló al cierre del bloque de *Introducción a Aplicaciones Web*, la lección conceptual más transferible de todo el temario — permite reconocer variantes nuevas de esta misma familia de vulnerabilidades en contextos y tecnologías que todavía no se han estudiado de forma explícita.
