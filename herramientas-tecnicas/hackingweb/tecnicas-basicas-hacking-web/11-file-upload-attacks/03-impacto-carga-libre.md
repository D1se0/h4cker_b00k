# El impacto de una carga sin restricciones

## De "subir un archivo" a "ejecutar código en el servidor"

El apartado anterior estableció cómo confirmar, con una prueba mínima, que un servidor ejecuta el código de un archivo subido en lugar de tratarlo como dato pasivo. Una vez confirmado eso, la conclusión de impacto es directa: la aplicación permite **ejecución remota de código arbitrario**, la categoría de vulnerabilidad de mayor severidad en cualquier escala de riesgo (la misma conclusión a la que se llegó en el bloque de *SQL Injection Fundamentals* al lograr escritura de archivos con privilegios suficientes, y en el de *Command Injection* al confirmar inyección sin restricciones).

## Por qué no hace falta "demostrarlo más" para documentar el hallazgo

En una auditoría responsable, la prueba de concepto mínima —un script que simplemente imprime un texto fijo y se ejecuta correctamente— ya es evidencia suficiente y reproducible de la vulnerabilidad. No es necesario, ni recomendable, desplegar herramientas de post-explotación (intérpretes de comandos interactivos, conexiones salientes hacia infraestructura del auditor) para documentar el hallazgo: el riesgo de causar un efecto no deseado en el sistema objetivo, o de generar tráfico que complique el análisis forense posterior del equipo defensor, supera el valor añadido de "ir más allá" de la prueba mínima.

## Qué significa este nivel de acceso, en términos de riesgo para la organización

Confirmada la ejecución de código arbitrario en el servidor backend, el riesgo que debe comunicarse al equipo responsable incluye, como mínimo:

- **Acceso a cualquier dato accesible por el proceso del servidor web** — código fuente de la aplicación, archivos de configuración con credenciales, datos de otros usuarios almacenados en disco.
- **Capacidad de pivotar hacia otros sistemas de la red interna**, si el servidor comprometido tiene conectividad hacia ellos — el mismo razonamiento de "esto puede ser el punto de apoyo para comprometer el resto de la infraestructura" visto repetidamente a lo largo de este temario.
- **Capacidad de persistencia**: un atacante real podría dejar mecanismos para mantener acceso incluso después de que la vulnerabilidad original se corrija, si no se hace una limpieza completa del sistema comprometido.

## Por qué la causa raíz siempre es la misma

Más allá de los detalles concretos de cómo se monta la prueba de concepto, la causa de fondo de este escenario es idéntica a la vista en cada bloque anterior de este temario: **el servidor confía en que el contenido recibido es lo que dice ser, sin verificarlo de forma robusta**. Los siguientes apartados de este bloque examinan los intentos más habituales de las aplicaciones por mitigar esto — validación de cliente, listas negras, listas blancas, verificación de tipo de contenido — y por qué cada uno, aplicado de forma aislada, suele ser insuficiente.
