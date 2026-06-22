# Escaneo automatizado y prevención de inclusión de archivos

## Escaneo automatizado

Para descubrir puntos de LFI de forma sistemática durante una auditoría, se puede combinar fuzzing de parámetros (visto en el bloque de *Web Fuzzing*) con listas de payloads específicos para path traversal:

```bash
# ffuf fuzzeando el parámetro language con payloads de LFI
ffuf -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt \
     -u "http://objetivo/?language=FUZZ" \
     -fs [tamaño_respuesta_normal]
```

SecLists incluye listas curadas de payloads LFI que cubren las variantes más comunes: path traversal directo, con encoding URL, con técnicas anti-filtro. Un resultado con tamaño distinto al "normal" indica que la inclusión tuvo efecto.

### LFI Suite y herramientas dedicadas

Existen herramientas dedicadas a enumerar y explotar LFI automáticamente (búsqueda rápida en GitHub por "LFI scanner"), que automatizan la combinación de payloads con técnicas de bypass y detectan si la respuesta contiene indicadores de archivos del sistema (patrones típicos de `/etc/passwd`, por ejemplo).

Como siempre con herramientas automatizadas: los resultados requieren validación manual antes de reportar — los falsos positivos son frecuentes.

## Prevención: la jerarquía de medidas

### Capa 1 — Eliminar el parámetro controlado por el usuario (la mejor opción)

La solución más robusta es que la aplicación **no use entrada de usuario para determinar qué archivo cargar**. Si la funcionalidad de carga dinámica de contenido puede redeseñarse para que las referencias a archivos vengan exclusivamente del servidor (no de parámetros GET/POST), LFI desaparece por completo.

### Capa 2 — Lista blanca estricta de archivos permitidos

Si eliminar el parámetro no es viable, restringir la entrada a un conjunto cerrado y explícito de valores permitidos:

```php
// Solo se permiten estos dos idiomas — todo lo demás se rechaza
$allowed = ['en', 'es'];

if (in_array($_GET['language'], $allowed)) {
    include('./languages/' . $_GET['language'] . '.php');
} else {
    include('./languages/en.php'); // valor por defecto
}
```

La entrada del usuario nunca se usa directamente como ruta — solo para seleccionar entre un conjunto de opciones predefinidas y controladas. Nada fuera de esa lista llega nunca a la función de inclusión.

### Capa 3 — Sanitización de path traversal (recursiva)

Si la lista blanca completa no es posible, al menos eliminar de forma **recursiva** los patrones de path traversal:

```php
// Elimina '../' de forma recursiva hasta que no quede ninguno
while (strpos($input, '../') !== false) {
    $input = str_replace('../', '', $input);
}
```

A diferencia del reemplazo simple no recursivo (que es bypasseable, como vimos en el apartado de bypass básicos), la eliminación en bucle sí garantiza que no queden instancias residuales tras el primer pase. Complementar además con `basename()` para asegurarse de que solo se procesa el nombre de archivo, sin componentes de directorio.

### Capa 4 — Configuración de PHP para limitar el alcance

```ini
; php.ini — configuraciones de seguridad relevantes para LFI/RFI
allow_url_include = Off   ; deshabilita RFI y wrappers data://,input://
allow_url_fopen   = Off   ; deshabilita lectura de URLs externas
open_basedir      = /var/www/html  ; restringe PHP a este directorio
disable_functions = system,exec,shell_exec,passthru  ; deshabilita funciones de ejecución
```

`open_basedir` es especialmente potente: aunque exista una vulnerabilidad LFI en el código, PHP simplemente no puede leer archivos fuera del directorio especificado — el mismo principio de contención mediante aislamiento visto en los bloques de *File Upload Attacks* y *Server-side Attacks*.

### Capa 5 — WAF como red de seguridad adicional

ModSecurity (mencionado en el bloque de *Web Proxies* y en el cierre de otros bloques) puede detectar patrones típicos de LFI en las peticiones (`../`, `/etc/passwd`, `php://filter`, etc.) y bloquearlos antes de que lleguen a la aplicación. Como siempre, no debe ser la única línea de defensa — pero añade valor como capa adicional que genera alertas tempranas.

## Checklist de prevención de LFI

- [ ] ¿Ningún parámetro controlado por el usuario se pasa directamente a `include()`, `require()`, `file_get_contents()` o equivalentes?
- [ ] Si se usa un parámetro para seleccionar contenido, ¿se valida contra una lista blanca explícita en el servidor?
- [ ] ¿`allow_url_include` está en `Off` en `php.ini`?
- [ ] ¿`open_basedir` está configurado para restringir el acceso de PHP a solo los directorios necesarios?
- [ ] ¿Los mensajes de error detallados están desactivados en producción (no revelan rutas del sistema)?
- [ ] ¿El directorio de archivos subidos por usuarios tiene desactivada la ejecución PHP?

## Cierre del bloque de File Inclusion

Este bloque ha recorrido el espectro completo de LFI: desde la lectura básica de archivos hasta la ejecución de código vía wrappers PHP, log poisoning, RFI, y la cadena LFI + upload. El hilo conductor es el mismo que en cada bloque de inyección de este temario: la entrada del usuario controlando algo que no debería controlar — aquí, qué archivo incluye el servidor. La prevención, como siempre, requiere actuar en la causa raíz (eliminar o restringir estrictamente esa capacidad de control) más capas adicionales de contención que limiten el impacto si la causa raíz no puede corregirse completamente.
