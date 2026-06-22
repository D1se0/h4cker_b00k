# Cuando solo se permiten archivos limitados (imágenes, etc.)

## El escenario: filtros bien implementados, pero el problema no termina ahí

Hasta ahora este bloque se ha centrado en aplicaciones donde, por una u otra debilidad de filtro, era posible cargar y ejecutar código arbitrario. Pero incluso cuando una aplicación implementa correctamente las capas de validación vistas en los apartados anteriores —lista blanca de extensión, verificación de tipo de contenido real— y solo acepta de forma genuina tipos de archivo no ejecutables (imágenes, documentos), eso no significa que la carga de archivos quede completamente libre de riesgo.

## Por qué algunos formatos "seguros" no lo son tanto

Ciertos formatos de archivo, aunque no son código ejecutable en el sentido tradicional, pueden incorporar contenido interpretable por el navegador o por otros componentes de la aplicación:

- **SVG**: es, estructuralmente, un documento **XML**. Los navegadores que renderizan SVG interpretan también el marcado que contiene, lo que abre la puerta a que ese marcado incluya contenido interactivo en el contexto de la página que lo muestra — el mismo principio de XSS visto en su propio bloque, aplicado aquí a través de un formato de imagen.
- **Metadatos de imágenes** (campos como autor, comentario, descripción en formatos JPEG/PNG/TIFF): si una aplicación muestra estos metadatos sin sanitizarlos al renderizarlos en una página, cualquier texto colocado en esos campos —incluido marcado HTML/JS— se trata exactamente igual que cualquier otra entrada de usuario reflejada sin escapar.
- **Documentos HTML subidos directamente**: si la aplicación permite adjuntar archivos HTML y luego los sirve accesibles vía URL, cualquier persona que abra ese enlace ejecuta en su navegador el contenido completo del documento, en el contexto de origen de la aplicación que lo aloja.

## Por qué esto importa incluso sin lograr ejecución de código en el servidor

Estos vectores no comprometen el servidor backend directamente —no son ejecución remota de código—, pero sí pueden comprometer a **otros usuarios** de la aplicación que terminen visualizando el archivo subido, exactamente con el mismo impacto descrito en el bloque dedicado a XSS: robo de sesión, desfiguración, phishing dirigido contra quien visualice el archivo.

## Por qué los formatos basados en XML merecen atención adicional

Más allá de XSS, los formatos basados en XML (como SVG) pueden, en aplicaciones que parsean su contenido de forma insegura, abrir la puerta a una clase de vulnerabilidad distinta conocida como **XXE (XML External Entity)** — donde el procesador XML del servidor puede inducirse a resolver referencias externas dentro del propio documento, potencialmente filtrando archivos del servidor o realizando peticiones de red no autorizadas. Esta vulnerabilidad se trata en profundidad, con su propio análisis técnico y mitigaciones específicas, en el bloque de *Web Attacks* de este mismo temario.

## La lección de fondo

Limitar correctamente **qué extensión y qué contenido binario** se acepta es una capa de defensa necesaria, pero no agota el análisis de riesgo de una funcionalidad de carga de archivos: incluso dentro de los formatos legítimamente permitidos, hay que considerar **qué hace la aplicación con ese archivo después de aceptarlo** — si lo renderiza directamente, si extrae y muestra sus metadatos, o si lo procesa con librerías que interpretan su estructura interna. Cada uno de esos pasos posteriores introduce su propia superficie de riesgo, independiente de si el archivo en sí "es" o "no es" ejecutable.
