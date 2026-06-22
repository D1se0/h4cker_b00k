# Prevención de XXE

## Por qué XXE se previene de forma diferente a otras inyecciones

A diferencia de SQL Injection o Command Injection — donde la vulnerabilidad nace de código mal escrito por el desarrollador —, XXE ocurre casi siempre porque la aplicación usa una **librería XML con entidades externas habilitadas por defecto** y no ha desactivado explícitamente esa funcionalidad. Esto significa que la prevención principal no está en revisar la lógica de la aplicación, sino en actualizar y configurar correctamente las dependencias XML.

## Capa 1: Actualizar las librerías XML (la más efectiva)

La causa más común de XXE es el uso de librerías XML obsoletas que tienen entidades externas habilitadas por defecto — un comportamiento que las versiones modernas de esas mismas librerías han corregido o que exponen mediante APIs de configuración explícitas.

Ejemplo en PHP: la función `libxml_disable_entity_loader()` fue diseñada precisamente para deshabilitar la carga de entidades externas, pero está **marcada como obsoleta a partir de PHP 8.0** — señal de que el ecosistema ha evolucionado hacia un comportamiento seguro por defecto, y el código que depende de funciones obsoletas para gestionar la seguridad del parser es en sí mismo un riesgo.

La [Hoja de referencia de prevención de XXE de OWASP](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html) mantiene una guía actualizada por lenguaje y librería con las funciones vulnerables y sus alternativas seguras.

**La misma lógica aplica a cualquier componente que procese XML internamente**:
- Procesadores de imágenes SVG
- Parsers de documentos Office (DOCX, XLSX) — que internamente son XML comprimido
- Librerías SOAP
- Módulos Node.js de parsing XML

Mantener todas estas dependencias actualizadas es la medida con mayor cobertura, ya que protege frente a XXE sin requerir cambios en el código de la aplicación.

## Capa 2: Configuración segura del parser XML

Cuando el contexto lo permite (por ejemplo, parsers configurables que no han eliminado la opción manualmente), deshabilitar explícitamente las funcionalidades peligrosas en la configuración del parser:

| Funcionalidad a deshabilitar | Por qué |
|---|---|
| **Definiciones de tipo de documento (DTD) personalizadas** | Elimina la posibilidad de declarar entidades externas en el propio XML de entrada |
| **Referencias a entidades externas XML** | Impide que el parser resuelva `SYSTEM "file://..."` o `SYSTEM "http://..."` |
| **Procesamiento de entidades de parámetro** | Cierra la variante usada en exfiltración ciega |
| **Soporte de XInclude** | Otra forma de incluir contenido externo en documentos XML |

## Capa 3: Manejo de errores que no revele información

Como se señaló en el apartado de exfiltración ciega, algunos ataques XXE aprovechan mensajes de error del servidor para filtrar fragmentos del contenido procesado. **Deshabilitar los mensajes de error detallados del servidor en producción** elimina este canal de exfiltración — la misma recomendación genérica de "no exponer errores internos al cliente" que ha aparecido en múltiples bloques de este temario.

## Capa 4: Considerar alternativas a XML

Cuando el formato de datos no está impuesto por un estándar externo (como SOAP), evaluar si la funcionalidad puede implementarse usando **JSON** en lugar de XML — un formato que no tiene concepto de entidades externas y elimina por completo esta clase de vulnerabilidad. La tendencia general del ecosistema web hacia APIs REST con JSON en lugar de APIs SOAP con XML responde, entre otras razones, a la complejidad de seguridad que XML introduce.

## Capa 5: WAF como defensa adicional

Un WAF bien configurado puede detectar patrones típicos de XXE en las peticiones entrantes (como `<!ENTITY`, `SYSTEM`, `file://` dentro del cuerpo XML). Como siempre, **no debe ser la única línea de defensa** — los WAFs tienen patrones de evasión conocidos y nunca sustituyen a una configuración correcta del parser.

## Checklist de prevención de XXE

- [ ] ¿Las librerías XML usadas están actualizadas a versiones que deshabilitan entidades externas por defecto?
- [ ] ¿Se han actualizado también librerías de terceros que procesan XML (parsers de documentos Office, SVG, SOAP)?
- [ ] ¿El parser está configurado explícitamente para deshabilitar DTD personalizadas y entidades externas?
- [ ] ¿Los mensajes de error del parser no se exponen al cliente en producción?
- [ ] ¿Se ha evaluado si JSON puede sustituir a XML en los endpoints que lo permitan?
- [ ] ¿Existe un WAF como capa adicional de detección de patrones XXE conocidos?

## Cierre del bloque de Web Attacks

Con esto se completa el recorrido de los tres ataques de este bloque: manipulación de verbos HTTP, IDOR, y XXE. Los tres comparten el mismo hilo conductor que ha recorrido todo este temario: controles de seguridad que se aplican de forma incompleta — sobre algunos verbos pero no todos, sobre algunos endpoints pero no los equivalentes, sobre el frontend pero no el backend, sobre la lógica de acceso pero no el parser subyacente. La defensa robusta, en los tres casos, requiere aplicar los controles de forma **consistente y exhaustiva**, no puntualmente o por convención de uso esperado.
