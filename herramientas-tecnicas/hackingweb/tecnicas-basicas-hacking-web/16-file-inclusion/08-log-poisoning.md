# Log Poisoning

## La idea central

Log poisoning combina LFI con la capacidad de "escribir" en un log del servidor — no mediante un exploit de escritura directa, sino simplemente haciendo peticiones HTTP cuyo contenido queda registrado en el log. Si esa entrada de log contiene código PHP, y luego se incluye el archivo de log vía LFI, el servidor ejecutará ese código.

Es, conceptualmente, el mismo patrón que LFI + upload pero usando los logs del servidor como "almacenamiento" alternativo cuando no hay acceso a funcionalidades de carga de archivos.

## Requisitos

1. **LFI confirmado**: la aplicación puede incluir el archivo de log.
2. **El log es legible** por el proceso PHP (permisos de fichero adecuados).
3. **Algún campo del log** está bajo control del usuario — la cabecera `User-Agent` es el caso más habitual.

## Cómo funciona el envenenamiento del log de acceso de Apache

El log de acceso de Apache (`/var/log/apache2/access.log`) registra cada petición HTTP, incluyendo la cabecera `User-Agent` tal cual la envía el cliente, sin sanitización.

Si se realiza una petición con un `User-Agent` que contiene código PHP:

```
User-Agent: <?php system($_GET['cmd']); ?>
```

Apache guarda literalmente esa cadena en el log. La línea en el log quedará como:

```
10.10.10.x - - [fecha] "GET / HTTP/1.1" 200 1234 "-" "<?php system($_GET['cmd']); ?>"
```

A continuación, si se incluye el log vía LFI:

```
?language=/var/log/apache2/access.log&cmd=id
```

PHP interpreta el archivo de log como código PHP, ejecuta `system($_GET['cmd'])` con el valor de `cmd`, y devuelve la salida del comando en la respuesta.

## PoC mínima responsable

Como en todos los apartados de este temario donde se llega a ejecución de código: la PoC adecuada para una auditoría es ejecutar un comando inofensivo (`id`, `hostname`, `whoami`) y documentar la salida — suficiente para demostrar RCE sin escalar la explotación más allá de lo necesario.

## Otros logs explotables con la misma técnica

| Log | Qué campo inyectar |
|---|---|
| `/var/log/apache2/access.log` | `User-Agent` |
| `/var/log/apache2/error.log` | User-Agent en peticiones que generan errores |
| `/var/log/ssh/auth.log` (Ubuntu) | Nombre de usuario en intentos SSH fallidos |
| `/var/log/vsftpd.log` | Nombre de usuario en intentos de login FTP |
| `/proc/self/environ` | Variable de entorno `HTTP_USER_AGENT` |

## Por qué este vector puede ser difícil de detectar

A diferencia de LFI + upload (donde hay un artefacto visible — el archivo subido), log poisoning no deja ningún archivo nuevo en el sistema. El "payload" está embebido en los logs normales del servidor, mezclado con miles de peticiones legítimas. Esto lo hace más sigiloso en términos de rastro, pero también más limitado: si el log rota o se limpia, el payload desaparece.

## Mitigación

- **Restringir qué archivos puede incluir LFI** con listas blancas estrictas (apartado siguiente) — si `/var/log/` no está en la lista de rutas permitidas, no importa lo que esté en el log.
- **Permisos de fichero restrictivos** en logs del servidor: el proceso PHP no debería necesitar leer los logs de Apache (`www-data` leer `/var/log/apache2/` es un privilegio innecesario en la mayoría de aplicaciones).
- **Deshabilitar la visualización de mensajes de error** que puedan acabar en logs accesibles vía LFI.
- La mitigación estructural de LFI en sí (apartado siguiente) es la defensa principal — si no hay LFI, el log poisoning no tiene vector de entrega.
