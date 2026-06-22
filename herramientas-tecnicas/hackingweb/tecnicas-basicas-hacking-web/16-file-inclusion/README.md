# File Inclusion

La inclusión de archivos es una vulnerabilidad que nace de la misma causa raíz que el resto de inyecciones de este temario: entrada de usuario que controla qué archivo se carga o incluye en la respuesta, sin la validación y restricción adecuadas. Este bloque cubre LFI (Local File Inclusion), sus técnicas de bypass, filtros PHP, wrappers de PHP para RCE, RFI (Remote File Inclusion), combinación de LFI con carga de archivos, y log poisoning. Cierra con escaneo automatizado y prevención.

## Contenido

1. [Introducción a las inclusiones de archivos](01-introduccion-file-inclusion.md)
2. [LFI: Local File Inclusion](02-lfi-basico.md)
3. [Bypass de filtros básicos en LFI](03-lfi-bypass-basico.md)
4. [Filtros PHP y wrappers de lectura](04-php-filtros-wrappers.md)
5. [Wrappers PHP para ejecución de código](05-php-wrappers-rce.md)
6. [RFI: Remote File Inclusion](06-rfi.md)
7. [LFI combinado con carga de archivos](07-lfi-file-upload.md)
8. [Log Poisoning](08-log-poisoning.md)
9. [Escaneo automatizado y prevención](09-automatizacion-prevencion.md)

## Por qué este bloque importa

LFI es uno de los vectores más frecuentes en entornos de pentesting y CTFs porque aparece en una categoría enorme de aplicaciones que construyen rutas de archivo a partir de parámetros controlables por el usuario. En el peor caso, LFI escala hasta RCE completa mediante varias cadenas de explotación (log poisoning, wrappers PHP, upload + include) — exactamente el mismo nivel de impacto que SQL Injection o Command Injection, pero a través de un vector completamente distinto.
