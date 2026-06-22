# Introducción a las inclusiones de archivos

## El patrón de causa raíz

Las vulnerabilidades de inclusión de archivos aparecen cuando una aplicación web carga dinámicamente un archivo cuya ruta —total o parcialmente— está controlada por el usuario, sin la validación y restricción adecuadas. El caso de uso legítimo que lo habilita es frecuente: muchas aplicaciones usan un parámetro para determinar qué "página" o "plantilla" cargar.

```
/index.php?page=about
/index.php?lang=es
/index.php?template=header
```

Si ese parámetro se pasa directamente a una función que incluye o lee el archivo indicado, el usuario puede redirigirlo hacia archivos no previstos por el desarrollador.

## Ejemplos de código vulnerable por lenguaje

### PHP

```php
// Vulnerable — el parámetro va directo a include()
include($_GET['language']);
```

Funciones PHP que generan la misma vulnerabilidad cuando reciben una ruta sin validar: `include()`, `include_once()`, `require()`, `require_once()`, `file_get_contents()`.

### Node.js

```javascript
// Vulnerable — parámetro GET -> readFile sin sanitizar
fs.readFile(path.join(__dirname, req.query.language), function(err, data) {
    res.write(data);
});
```

### Java

```jsp
<!-- Vulnerable — parámetro controlado por el usuario en jsp:include -->
<jsp:include file="<%= request.getParameter('language') %>" />
```

### .NET

```csharp
// Vulnerable — parámetro en la ruta de WriteFile
Response.WriteFile(HttpContext.Request.Query["language"]);
```

El patrón es idéntico en todos los lenguajes: una función que carga un archivo recibe como argumento un valor controlado por el usuario sin que la aplicación restrinja qué valores son válidos.

## LFI vs. RFI: la distinción fundamental

| Tipo | Qué incluye | Requisito adicional |
|---|---|---|
| **LFI** (Local File Inclusion) | Archivos que ya existen en el servidor | Ninguno — siempre presente si el código es vulnerable |
| **RFI** (Remote File Inclusion) | Archivos alojados en un servidor remoto | Configuración PHP con `allow_url_include=On` (desactivado por defecto en PHP moderno) |

LFI es universalmente aplicable cuando el código es vulnerable; RFI requiere una configuración adicional que cada vez es menos común pero que aún aparece en instalaciones antiguas.

## Espectro de impacto

LFI puede parecer "solo" una vulnerabilidad de lectura de archivos, pero bajo ciertas condiciones escala hasta **ejecución remota de código**:

1. **Lectura de archivos locales sensibles**: el caso más básico — leer `/etc/passwd`, archivos de configuración con credenciales, código fuente de la aplicación.
2. **LFI + carga de archivos**: si la aplicación también permite subir archivos, LFI puede incluir el archivo subido y ejecutarlo como código.
3. **Log Poisoning**: inyectar código PHP en un log del servidor y luego incluirlo vía LFI para ejecutarlo.
4. **Wrappers PHP**: usar pseudo-protocolos PHP (`php://`, `data://`) para ejecutar código directamente sin necesitar archivos preexistentes.
5. **RFI**: incluir directamente un script alojado en un servidor externo controlado por el atacante.

Este mismo espectro de escalada de impacto — de lectura de datos a ejecución de código — es el mismo patrón que se vio en SQL Injection (lectura de tablas → lectura de archivos → escritura de archivos → RCE) y en XXE (lectura de archivos → SSRF). Los bloques restantes de esta categoría desarrollan cada uno de esos escalones en detalle.
