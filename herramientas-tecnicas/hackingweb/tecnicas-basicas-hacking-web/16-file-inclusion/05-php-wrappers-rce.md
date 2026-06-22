# Wrappers PHP para ejecución de código

## El salto de lectura a ejecución

Hasta ahora, LFI ha permitido leer archivos del sistema. Algunos wrappers PHP permiten ir más allá: **ejecutar código** directamente a través del mecanismo de inclusión, sin necesitar que un archivo malicioso preexista en el sistema. Esto representa el escalón más alto de impacto en LFI — el mismo nivel que SQL Injection con escritura de archivos o Command Injection.

> **Contexto**: estas técnicas requieren configuraciones PHP específicas. En PHP moderno con configuración por defecto, muchas están desactivadas. Pero siguen apareciendo en instalaciones antiguas, aplicaciones heredadas, y entornos de laboratorio/CTF.

## Wrapper `data://`: código inline

Si `allow_url_include` está activado, `data://` permite incluir contenido directamente en la petición:

```
data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ID8+
```

La cadena Base64 decodifica a `<?php system($_GET['cmd']); ?>` — el mismo intérprete mínimo visto en el bloque de *File Upload Attacks* (donde rechazamos incluirlo como payload operativo completo). Aquí lo mencionamos conceptualmente para que entiendas cómo funciona el vector, no como receta lista para desplegar.

La petición resultante sería:
```
?language=data://text/plain;base64,<b64_del_codigo>&cmd=id
```

## Wrapper `input://`: payload en el cuerpo POST

Similar a `data://`, pero el código a ejecutar viaja en el cuerpo de una petición POST en lugar de en la URL:

```
POST ?language=php://input
Body: <?php system($_GET['cmd']); ?>
```

Útil cuando la URL tiene limitaciones de longitud o cuando ciertos caracteres se filtran en la query string.

## Wrapper `expect://`: ejecución directa (rarísimo)

El módulo `expect` de PHP (que **no** viene instalado por defecto) expone un wrapper que ejecuta directamente comandos del sistema operativo:

```
?language=expect://id
```

Si `expect` está disponible, el resultado del comando aparece directamente en la respuesta. En entornos reales modernos esto es excepcional — se menciona por completitud.

## Por qué `php://filter` (visto en el apartado anterior) es más universal

A diferencia de los wrappers de ejecución (que requieren `allow_url_include=On` o módulos adicionales), `php://filter` solo necesita que PHP pueda leer el archivo — sin configuración especial adicional. Por eso, en una auditoría real, la lectura de código fuente vía `php://filter` tiene mucha más probabilidad de funcionar que los wrappers de ejecución de código.

## El criterio para reportar

En una auditoría autorizada, si se confirma que un wrapper de ejecución funciona:

1. **PoC mínima**: ejecutar un comando inofensivo (`id`, `hostname`, `whoami`) y documentar la salida — suficiente para demostrar RCE sin ir más lejos.
2. **Documentar los requisitos**: qué configuración PHP está habilitada que lo permite, y qué cambio de configuración lo mitigaría.
3. **No escalar** más allá de la PoC mínima dentro del alcance de la auditoría.

## Mitigación de los wrappers de ejecución

La configuración más directa: en `php.ini`:
```ini
allow_url_include = Off   ; deshabilita data://, php://input con código remoto
allow_url_fopen = Off     ; deshabilita también RFI (próximo apartado)
```

Estas dos directivas desactivadas juntos eliminan los vectores de ejecución de código vía wrappers. El resto de la mitigación de LFI se desarrolla en el apartado final de este bloque.
