# Bypass de filtros básicos en LFI

## Por qué los filtros de lista negra suelen ser insuficientes

Como hemos visto repetidamente en este temario (Command Injection, SQL Injection, File Upload), los filtros basados en eliminar o rechazar subcadenas concretas son intrínsecamente frágiles. LFI no es la excepción.

## Filtro de eliminación no recursiva de `../`

Un filtro habitual consiste en eliminar la secuencia `../` de la entrada:

```php
$language = str_replace('../', '', $_GET['language']);
```

El fallo: este reemplazo solo se aplica **una vez**, no de forma recursiva. Si el payload usa una construcción que "contiene" `../` de forma anidada, tras eliminar una capa queda otra válida:

| Payload original | Después del filtro |
|---|---|
| `....//` | `../` ← ¡queda válido! |
| `..././` | `../` |
| `....\/` | `..\` (útil en Windows) |

Esto confirma la misma lógica que en Command Injection o XSS: un filtro de un solo paso nunca es exhaustivo frente a la variedad de construcciones equivalentes disponibles.

## Codificación URL de caracteres filtrados

Si el filtro rechaza peticiones que contengan `.` o `/` como caracteres literales, URL-encoding los evade:

```
../    →    %2e%2e%2f
./     →    %2e%2f
```

El servidor decodifica la URL antes de pasarla a la función de inclusión, pero el filtro opero sobre la versión sin decodificar, no viendo los caracteres prohibidos.

**Nota**: en algunos contextos, es necesaria doble codificación (`%2e%2e%2f` → `%252e%252e%252f`) para evadir dos capas de validación que descodifican en momentos distintos.

## Rutas aprobadas (allowlist parcial)

Cuando la aplicación exige que la ruta comience por un directorio concreto:

```php
if(preg_match('/^\.\/languages\/.+$/', $_GET['language'])) {
    include($_GET['language']);
}
```

Se puede evadir comenzando el payload por la ruta aprobada y usando `../` desde ahí:

```
?language=./languages/../../../etc/passwd
```

La expresión regular ve que comienza por `./languages/` y lo aprueba; la función de inclusión resuelve el path traversal posterior y lee el archivo objetivo.

## Extensión añadida (`.php` al final)

```php
include($_GET['language'] . ".php");
```

Con PHP moderno (≥ 5.3/5.4), técnicas clásicas como path truncation o null bytes (`%00`) ya no funcionan. Esto limita el LFI a leer solo archivos `.php` — que sigue siendo valioso para leer código fuente de la propia aplicación. Las técnicas que permiten escalar más allá de esta limitación (wrappers PHP como `php://filter`) se tratan en el siguiente apartado.

## Resumen de payloads por tipo de filtro

| Tipo de filtro | Bypass |
|---|---|
| Eliminación simple de `../` | `....//`, `..././`, `....\/` |
| Filtro de caracteres `.` o `/` | URL encoding: `%2e%2e%2f` |
| Ruta aprobada obligatoria | Iniciar con la ruta aprobada + `../` desde ahí |
| Extensión `.php` añadida | Wrappers PHP (`php://filter/`) — ver siguiente apartado |
