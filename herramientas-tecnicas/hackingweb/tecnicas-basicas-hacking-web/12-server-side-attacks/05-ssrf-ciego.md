# SSRF ciego

## La diferencia frente a la SSRF "visible"

Como se mencionó en el apartado de identificación, no toda SSRF permite ver directamente el contenido de la respuesta obtenida por el servidor. Cuando la aplicación simplemente realiza la petición intermedia sin reflejar nada de su contenido —ni en pantalla, ni en mensajes de error detallados— se habla de **SSRF ciega**: la vulnerabilidad existe y es explotable, pero la información que se puede extraer de ella es mucho más limitada e indirecta.

## Qué señales quedan disponibles, aun sin ver el contenido

Aunque no haya visibilidad directa del contenido de la respuesta, suele seguir habiendo **señales indirectas** que distinguen distintos resultados posibles:

- **Diferencias de tiempo de respuesta**: una petición hacia un destino que existe y responde rápido se comporta de forma distinta, en términos de tiempo, que una hacia un destino inexistente o que tarda en fallar — el mismo principio de inferencia temporal visto en el bloque de *SQL Injection Fundamentals* al hablar de inyección ciega basada en tiempo.
- **Códigos de estado o mensajes de error genéricos**: aunque no se muestre el contenido real, la aplicación puede comportarse de forma distinta (un error genérico de "no se pudo conectar" frente a una respuesta de éxito sin contenido visible) según si el destino de la petición existe y responde o no.

## Por qué esto sigue siendo explotable, aunque de forma más limitada

Esta combinación de señales —exactamente como en cualquier otra vulnerabilidad ciega trabajada en este temario— sigue permitiendo inferir información real, aunque de forma indirecta y más lenta que en un escenario donde la respuesta es completamente visible. El tipo de información que normalmente se puede inferir en un escenario de SSRF ciega es de naturaleza binaria: "¿existe o no existe algo en esta posición concreta?" — suficiente, por ejemplo, para mapear qué servicios responden en una red interna, aunque no para leer directamente el contenido de esos servicios.

## Por qué la distinción entre ciega y no ciega importa para priorizar el riesgo

Al documentar un hallazgo de SSRF durante una auditoría, distinguir si es ciega o no condiciona directamente cómo se describe el impacto real: una SSRF no ciega que permite leer directamente el contenido de servicios internos representa, en términos generales, un riesgo de exposición de información mucho más inmediato y demostrable que una SSRF ciega, donde el impacto se limita —salvo que se encadene con otra vulnerabilidad adicional— a mapear la existencia de servicios sin acceder a su contenido.

## Conectando con la prevención

Independientemente de si una SSRF es ciega o no, la causa raíz que la hace posible —y, por tanto, la forma de prevenirla— es exactamente la misma. El siguiente apartado desarrolla en detalle esas medidas, válidas para ambos escenarios.
