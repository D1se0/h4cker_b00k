# Bypass de filtros de seguridad con manipulación de verbos

## El segundo tipo: inconsistencia en el código de la aplicación

A diferencia del caso anterior (configuración del servidor), este tipo de vulnerabilidad nace de una inconsistencia en el propio código de la aplicación: el filtro de seguridad inspecciona los parámetros de un verbo, pero la lógica de negocio los lee de otro.

## El patrón de código vulnerable

```php
if (isset($_REQUEST['filename'])) {
    // Filtro: solo comprueba parámetros POST
    if (!preg_match('/[^A-Za-z0-9. _-]/', $_POST['filename'])) {
        // Lógica: usa REQUEST, que incluye GET Y POST
        system("touch " . $_REQUEST['filename']);
    } else {
        echo "Malicious Request Denied!";
    }
}
```

El filtro `preg_match` verifica `$_POST['filename']` (solo parámetros POST), pero el comando `system()` usa `$_REQUEST['filename']` (que abarca GET, POST y cookies). Si se envía la entrada maliciosa vía GET, `$_POST` estará vacío — el filtro no la ve — pero `$_REQUEST` la recoge perfectamente y la pasa al comando.

## Cómo se detecta durante una auditoría

Si una aplicación bloquea un carácter especial (por ejemplo, `;`) con un mensaje genérico como "Malicious Request Denied!", pero la misma entrada enviada con un verbo distinto (cambiando de POST a GET, o al revés) no produce ese bloqueo, hay un fuerte indicio de inconsistencia — el filtro cubre un verbo, la lógica usa otro.

```bash
# POST bloqueado:
curl -X POST http://objetivo/ -d "filename=test;"
# -> "Malicious Request Denied!"

# GET no bloqueado:
curl -X GET "http://objetivo/?filename=test;"
# -> El archivo se crea (el filtro POST estaba vacío)
```

## Por qué es más difícil de detectar que la configuración insegura

En una aplicación real, el filtro de seguridad y la lógica de creación/uso del parámetro probablemente están en funciones distintas, potencialmente en archivos distintos, con docenas de líneas de código entre ellos. La inconsistencia no es "dos líneas seguidas con variables diferentes" sino una discrepancia que solo se hace visible al trazar el flujo completo de un dato desde la entrada hasta la ejecución.

Esta es exactamente la razón por la que la revisión de código manual (caja blanca) complementa y no sustituye las pruebas de penetración: un auditor externo puede descubrir el comportamiento inesperado probando verbos distintos, incluso sin ver el código; un revisor de código puede encontrar la inconsistencia en las variables sin necesitar probarla en vivo.

## La regla de mitigación de código

La inconsistencia en el uso de variables HTTP es el problema de fondo. La corrección es usar **la misma variable** en el filtro y en la lógica:

| Lenguaje | Variable consistente para todos los métodos |
|---|---|
| PHP | `$_REQUEST['param']` — tanto en el filtro como en el uso |
| Java | `request.getParameter('param')` — igual en ambos sitios |
| C# / ASP.NET | `Request['param']` — igual en ambos sitios |

Si el filtro debe cubrir todos los métodos, la variable de entrada del filtro debe también cubrir todos — no solo `$_POST` o solo `$_GET`, sino el equivalente que lee de cualquier origen.
