# Explotación cuando no hay validación

## El escenario más simple: ausencia total de filtros

El caso más básico de vulnerabilidad de carga de archivos ocurre cuando la aplicación **no implementa ningún tipo de validación** sobre lo que se sube — ni de extensión, ni de tipo de contenido, ni de tamaño. En este escenario, cualquier archivo, incluido un script ejecutable en el lenguaje del propio backend, se acepta y almacena sin restricción.

## Señales que sugieren ausencia de validación

Antes de probar nada activamente, conviene observar la propia interfaz de carga:

- El formulario no menciona qué tipos de archivo están permitidos.
- El diálogo de selección de archivos del sistema operativo no filtra por extensión (aparece como "Todos los archivos" en lugar de restringir a, por ejemplo, solo imágenes).

Ninguna de estas observaciones confirma por sí sola la vulnerabilidad — son simplemente indicios de que el frontend, al menos, no está aplicando ninguna restricción visible. Como se ha repetido a lo largo de este temario, **la validación de frontend nunca es una garantía de seguridad real**; lo que importa es qué ocurre realmente en el servidor.

## Identificando el lenguaje del backend antes de probar

Para construir una prueba de concepto efectiva, primero hay que saber en qué lenguaje está escrita la aplicación — un script de prueba en PHP no demuestra nada si el backend en realidad corre en Python o Node.js.

Técnicas habituales de identificación (conectando directamente con el bloque de *Information Gathering*):

- **Observar extensiones visibles en la URL** (`.php`, `.aspx`, `.jsp`), cuando la aplicación no oculta el enrutamiento detrás de URLs "limpias".
- **Probar variantes de página índice**: visitar `/index.php`, `/index.aspx`, etc., y comprobar cuál responde igual que la raíz del sitio — un indicio razonable, aunque no infalible, del lenguaje de backend.
- **Extensiones de fingerprinting del navegador** (como Wappalyzer), que identifican de un vistazo el stack tecnológico completo: lenguaje, servidor web, framework, e incluso el sistema operativo subyacente — la misma técnica vista en detalle en el bloque de *Information Gathering*.
- **Escáneres de proxy** (Burp, ZAP), que pueden incorporar detección de tecnologías como parte de su análisis pasivo.

## Construyendo una prueba de concepto mínima y segura

Antes de intentar cualquier impacto significativo, la prueba de concepto correcta —siguiendo el mismo principio de "demostrar lo justo y necesario" trabajado en el bloque de *Web Fuzzing*— es confirmar simplemente que el código del lenguaje identificado **se ejecuta** tras subir el archivo, sin ir más allá:

```php
<?php echo "Hello HTB"; ?>
```

Si, tras subir este archivo y acceder a él por su URL, la página devuelve el texto `Hello HTB` (en lugar de mostrar el propio código fuente sin procesar), queda confirmado que:

1. El archivo se subió sin ninguna restricción de tipo.
2. El servidor lo está **interpretando y ejecutando** como código, no sirviéndolo como texto plano o forzando su descarga.

Esta segunda condición es tan importante como la primera: subir un archivo `.php` no implica automáticamente que el servidor lo vaya a ejecutar como tal — depende de la configuración del directorio donde se almacena. Confirmar ambas condiciones con esta prueba mínima es el paso indispensable antes de razonar sobre cualquier impacto mayor.

## Por qué confirmar esto primero, antes de pasar a explotación completa

Esta separación entre "confirmar la vulnerabilidad" y "demostrar impacto completo" es deliberada: en una auditoría autorizada, basta con esta prueba de ejecución de código mínima para documentar de forma incuestionable que existe una vulnerabilidad crítica de ejecución remota de código — sin necesidad de desplegar herramientas adicionales de post-explotación, que quedarían fuera del alcance de una demostración de concepto responsable.
