# Manipulación de verbos HTTP: configuraciones inseguras

## Por qué existen estos ataques

Como vimos en el bloque de *Web Requests*, HTTP soporta varios métodos (verbos) más allá de `GET` y `POST`. Los más relevantes en este contexto:

| Verbo | Función |
|---|---|
| `HEAD` | Igual que GET pero sin cuerpo en la respuesta |
| `OPTIONS` | Lista los métodos HTTP que acepta el servidor para una ruta |
| `PUT` | Escribe o reemplaza un recurso en la ruta indicada |
| `DELETE` | Elimina el recurso en la ruta indicada |
| `PATCH` | Modificación parcial de un recurso |

El problema aparece cuando los controles de seguridad (autenticación, filtros de input) se configuran solo para ciertos verbos, dejando otros libres de esa protección — aunque ejecuten exactamente la misma funcionalidad en el backend.

## Los dos orígenes del problema

### 1. Configuración insegura del servidor

Cuando la autenticación se configura a nivel de servidor web solo para verbos específicos:

```xml
<!-- Apache: solo requiere auth para GET y POST -->
<Limit GET POST>
    Require valid-user
</Limit>
```

Un atacante puede enviar la misma petición con `HEAD` u `OPTIONS` y el servidor la procesa sin exigir credenciales, porque esos verbos no están dentro del bloque `<Limit>`.

### 2. Codificación insegura

Cuando un filtro de seguridad en el código de la aplicación solo inspecciona los parámetros de un verbo concreto, pero la lógica de negocio lee de todos:

```php
// Filtro solo sobre GET
if (preg_match($pattern, $_GET["code"])) {
    // Pero la consulta usa $_REQUEST, que incluye GET y POST
    $query = "SELECT * FROM ports WHERE port_code LIKE '%" . $_REQUEST["code"] . "%'";
}
```

Un atacante puede enviar la entrada maliciosa vía `POST` — el filtro no la inspeccionará (comprueba `$_GET`), pero la consulta sí la usará (`$_REQUEST` incluye ambos).

## Identificando verbos aceptados

```bash
curl -i -X OPTIONS http://objetivo/ruta
```

La respuesta incluirá una cabecera `Allow:` listando los métodos aceptados:

```
Allow: POST,OPTIONS,HEAD,GET
```

Esto confirma qué verbos vale la pena probar como vector de bypass. Es el primer paso antes de intentar ninguna manipulación.

## Por qué esto es especialmente relevante en servidores mal configurados

La manipulación de verbos es uno de los pocos vectores donde la vulnerabilidad puede estar completamente en la **configuración del servidor**, no en el código de la aplicación — lo que significa que puede aparecer en aplicaciones por lo demás bien escritas, simplemente porque el administrador de sistema no bloqueó explícitamente los verbos no necesarios. Los siguientes dos apartados desarrollan ambos escenarios con su metodología completa.
