# LFI combinado con carga de archivos

## La cadena: subir un archivo, luego incluirlo

Si una aplicación tiene dos vulnerabilidades simultáneas — LFI y una carga de archivos sin validación suficiente — la combinación puede escalar hasta ejecución de código incluso cuando RFI está desactivado y los wrappers de ejecución no están disponibles.

La lógica es simple: si se puede **subir** un archivo PHP al servidor (o un archivo con contenido PHP aunque tenga extensión de imagen), y luego **incluirlo** vía LFI, el servidor ejecutará ese código.

## Confirmando la ruta del archivo subido

El paso crítico es conocer exactamente dónde almacena la aplicación los archivos subidos. Técnicas para descubrirlo:

- **Código fuente**: si LFI ya funciona, leer el código de la funcionalidad de carga (`php://filter/read=convert.base64-encode/resource=upload.php`) puede revelar la ruta directamente.
- **Mensajes de la aplicación**: algunos formularios de subida muestran la URL o la ruta del archivo subido en la confirmación de éxito.
- **Fuzzing de directorios**: buscar directorios comunes como `/uploads/`, `/files/`, `/tmp/`, `/assets/` (técnica vista en el bloque de *Web Fuzzing*).

## El archivo a subir

Si la aplicación acepta imágenes pero no verifica el contenido real (solo la extensión o la cabecera MIME), un archivo con contenido PHP y extensión `.jpg` puede pasar el filtro:

```
Nombre: imagen.jpg
Content-Type: image/jpeg
Contenido: <?php echo file_get_contents('/etc/passwd'); ?>
```

Los bytes mágicos de JPEG al inicio (`FF D8 FF`) más el código PHP al final pueden satisfacer un filtro MIME superficial mientras el contenido PHP sigue siendo interpretable por el engine PHP cuando se incluye vía LFI.

Una PoC mínima y razonable para una auditoría: incluir código que lea `/etc/passwd` o ejecute `phpinfo()` — suficiente para demostrar la ejecución sin ir más lejos.

## Por qué esta cadena es especialmente relevante

- Elude la restricción de `allow_url_include=Off` (no necesita RFI).
- Elude la falta de wrappers de ejecución.
- Combina dos vulnerabilidades que, por separado, podrían parecer de impacto limitado: "solo puedo subir imágenes" + "solo puedo leer archivos locales" → juntas, RCE completa.

Esto ilustra el principio de encadenamiento visto también en IDOR (un IDOR de lectura más uno de escritura = impacto combinado mayor que la suma de las partes).

## Condiciones necesarias para que funcione

1. La aplicación acepta cargar archivos sin validar el contenido real (solo extensión o MIME declarado).
2. El archivo subido queda almacenado en una ruta accesible desde el LFI.
3. La función de inclusión (PHP `include()` o equivalente) interpreta el código PHP dentro del archivo subido, independientemente de su extensión.

Si alguna de las tres condiciones no se cumple, la cadena se rompe en ese punto — lo que subraya que ninguna de las dos vulnerabilidades aisladas es el problema único: ambas juntas crean el riesgo.

## Mitigación de esta cadena

- **Validación real del contenido** de archivos subidos (firma MIME real, no la cabecera declarada) — visto en detalle en el bloque de *File Upload Attacks*.
- **Almacenamiento fuera del alcance web** de archivos subidos por usuarios, o en directorios donde PHP no tenga permisos de ejecución.
- **Desactivar ejecución PHP** en el directorio de uploads (directiva `php_flag engine off` en Apache para ese directorio).
- **Restricción de LFI** con listas blancas de archivos incluibles — visto en el apartado de prevención de este bloque.
