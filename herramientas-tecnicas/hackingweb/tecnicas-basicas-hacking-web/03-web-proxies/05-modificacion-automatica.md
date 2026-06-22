# Modificación automática (Match & Replace)

## El problema de interceptar manualmente cada vez

Interceptar y editar manualmente cada petición o respuesta funciona bien para pruebas puntuales, pero se vuelve tedioso —y propenso a errores— cuando se necesita aplicar **el mismo cambio de forma consistente** a lo largo de toda una sesión de pruebas: por ejemplo, sustituir siempre el mismo `User-Agent`, o mantener siempre habilitado un campo de formulario que el servidor reenvía deshabilitado en cada respuesta.

Para esto existen las reglas de **modificación automática**, que aplican una transformación predefinida a cada petición o respuesta que coincida con un patrón, sin intervención manual.

## Burp: Match and Replace

`Proxy > Proxy settings > HTTP match and replace rules > Add`.

### Ejemplo: sustituir el User-Agent en todas las peticiones

| Campo | Valor |
|---|---|
| Type | `Request header` |
| Match | `^User-Agent.*$` |
| Replace | `User-Agent: HackTheBox Agent 1.0` |
| Regex match | `true` |

Con esta regla activa, cada petición que pase por el proxy tendrá su cabecera `User-Agent` reemplazada automáticamente — útil, por ejemplo, cuando una aplicación bloquea explícitamente herramientas de pentesting o navegadores no reconocidos basándose en esta cabecera.

### Ejemplo: modificar automáticamente el cuerpo de la respuesta

Retomando el ejemplo del apartado anterior (campo `type="number"` restringido):

| Campo | Valor |
|---|---|
| Type | `Response body` |
| Match | `type="number"` |
| Replace | `type="text"` |
| Regex match | `false` |

Con esta regla y otra equivalente para `maxlength="3"` → `maxlength="100"`, cada vez que se recargue la página, el campo aparecerá ya editable sin restricciones, de forma persistente, sin tener que interceptar nada manualmente.

## ZAP: Replacer

Accesible con `Ctrl+R` o desde el menú de opciones → **Replacer**. La configuración es conceptualmente idéntica:

- **Description**: nombre identificativo de la regla.
- **Match Type**: tipo de coincidencia (cabecera de petición, cuerpo, etc.) — incluye la opción de **añadir la cabecera si no está presente**, útil cuando se quiere forzar una cabecera que la petición original no incluye.
- **Match String**: qué buscar.
- **Replacement String**: con qué sustituirlo.
- **Initiators**: permite restringir dónde se aplica la regla (por defecto, a todos los mensajes HTTP/S).

## Casos de uso ofensivos de la modificación automática

- **Evasión de filtros basados en User-Agent o cabeceras de cliente**: rotar o falsificar automáticamente estas cabeceras en toda la sesión.
- **Inyección persistente para fuzzing manual**: añadir automáticamente un payload fijo (por ejemplo, una comilla simple `'`) al final de cada valor de un parámetro concreto en todas las peticiones, para detectar de un vistazo en qué respuestas aparece un comportamiento anómalo mientras se navega con normalidad por la aplicación.
- **Bypass de restricciones de frontend de forma permanente**: como se ha visto, mantener siempre habilitados/editables ciertos campos sin tener que repetir la interceptación manual en cada petición.
- **Inserción automática de tokens de autenticación**: si se está probando una API y se dispone de un token de sesión válido, se puede configurar una regla que añada automáticamente la cabecera `Authorization` a cada petición saliente, sin tener que copiarla manualmente cada vez que se usa Repeater o Intruder.

La modificación automática es, en esencia, la diferencia entre hacer una prueba puntual y mantener un comportamiento consistente durante toda una sesión de auditoría — especialmente valioso quando se combina con las herramientas de fuzzing y escaneo que veremos más adelante en este mismo bloque.
