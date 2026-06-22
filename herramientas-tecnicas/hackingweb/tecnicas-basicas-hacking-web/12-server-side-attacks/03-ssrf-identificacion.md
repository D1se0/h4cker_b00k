# Identificación de SSRF

## Buscando funcionalidades que "obtienen algo remoto"

El primer paso para reconocer una posible SSRF es identificar funcionalidades donde la aplicación, a partir de un dato proporcionado por el usuario, va a **buscar o consultar un recurso externo** en nombre de ese usuario. Patrones habituales:

- Funciones de "previsualización de enlace" (mostrar una miniatura o un resumen de una URL pegada por el usuario).
- Integraciones con servicios externos donde la URL del servicio es configurable.
- Funcionalidades de importación de datos desde una URL proporcionada.
- Webhooks o notificaciones donde el usuario define el destino.

En todos estos casos, el patrón de fondo es el mismo: el servidor va a realizar una petición HTTP saliente basada en un valor que el usuario controla, de forma similar a como una aplicación toma entrada del usuario para construir una consulta SQL (visto en el bloque correspondiente) — solo que aquí el "intérprete" final es el propio cliente HTTP del servidor.

## Confirmando la vulnerabilidad

La forma más directa de confirmar SSRF es proporcionar, en el campo correspondiente, una URL que apunte a un servidor controlado por quien realiza la auditoría, y verificar si efectivamente se recibe una conexión entrante procedente de la infraestructura del objetivo. Si esa conexión llega, queda confirmado que el servidor está realizando la petición saliente exactamente como se sospechaba.

## SSRF visible vs. SSRF ciego

Una distinción importante, que se retoma en detalle en un apartado posterior de este bloque: si la respuesta de la petición intermedia se refleja de alguna forma en lo que la aplicación devuelve al usuario (por ejemplo, mostrando el contenido HTML obtenido), se trata de una **SSRF no ciega** — el atacante puede ver directamente el resultado de las peticiones que fuerza al servidor a realizar. Si, en cambio, la aplicación no muestra ningún contenido de esa petición intermedia (solo confirma de forma indirecta, por ejemplo a través de tiempos de respuesta o códigos de error genéricos, que la petición se realizó), se trata de una **SSRF ciega**, considerablemente más limitada en cuanto a la información que se puede extraer directamente.

## Por qué esta distinción condiciona el resto del análisis

Determinar si la respuesta de la petición SSRF es visible o no marca completamente la diferencia respecto a qué información puede llegar a obtenerse: con una SSRF no ciega, el contenido de cualquier recurso interno alcanzado queda potencialmente expuesto de forma directa; con una SSRF ciega, solo es posible inferir información indirecta (como qué puertos responden y cuáles no), un escenario que se desarrolla con su propia metodología en el apartado dedicado a SSRF ciego.

## La conexión con el impacto real

Confirmar que existe SSRF —ya sea visible o ciega— es solo el primer paso. El verdadero alcance de la vulnerabilidad depende de **qué hay realmente accesible** desde la posición de red del servidor: qué servicios internos responden, qué información exponen, y si alguno de ellos tiene a su vez vulnerabilidades explotables. Este análisis de impacto se desarrolla en el siguiente apartado.
