# LFI: Local File Inclusion

## El caso más básico

Si el parámetro de la URL va directamente a la función de inclusión sin modificación alguna, la lectura de archivos arbitrarios es inmediata:

```php
include($_GET['language']);
```

```
/index.php?language=/etc/passwd
```

Esto devuelve el contenido completo de `/etc/passwd` como parte de la página renderizada.

## Path Traversal (recorrido de directorios)

El escenario más frecuente no es el anterior —rara vez el parámetro va directo y sin adornos— sino que la aplicación prepend o append alguna cadena al valor recibido:

```php
include("./languages/" . $_GET['language']);
```

Con esta construcción, pedir `/etc/passwd` resulta en la ruta `./languages//etc/passwd`, que no existe. Pero usando `../` para "subir" un directorio cada vez, se puede alcanzar cualquier ruta del sistema:

```
/index.php?language=../../../../etc/passwd
```

Esto construye `./languages/../../../../etc/passwd`, que el sistema operativo resuelve como `/etc/passwd`.

**Regla práctica**: agregar `../` más veces de las necesarias nunca rompe nada (en la raíz, `../` mantiene la raíz), así que si no se sabe con exactitud cuántos niveles hay que subir, usar varios de más es seguro.

## Casos con prefijo en el código

```php
include("lang_" . $_GET['language']);
```

Si la aplicación antepone un prefijo al parámetro, la técnica anterior genera una ruta como `lang_../../../etc/passwd` que no es válida. Solución: añadir `/` al inicio del payload, haciendo que el prefijo quede "absorbido" como parte de un nombre de directorio inexistente:

```
?language=/../../../etc/passwd
```

Esto intenta `lang_/`, que PHP no puede resolver como directorio, y a partir de ahí el path traversal procede normalmente.

## Casos con extensión añadida en el código

```php
include($_GET['language'] . ".php");
```

Aquí cualquier archivo que se intente leer recibirá automáticamente `.php` al final (`/etc/passwd.php` no existe). Las técnicas para sortear esta limitación se desarrollan en el apartado de bypass de filtros y wrappers PHP.

## Archivos de alto valor para LFI en Linux

| Archivo | Contenido relevante |
|---|---|
| `/etc/passwd` | Lista de usuarios del sistema |
| `/etc/hosts` | Mapa de hosts internos |
| `/etc/shadow` | Hashes de contraseñas (si el proceso tiene permisos) |
| `/proc/self/environ` | Variables de entorno del proceso web — a veces contiene rutas o claves |
| `/var/log/apache2/access.log` | Log de acceso de Apache — relevante para log poisoning |
| Archivos de configuración de la app | Credenciales de BD, claves de API |
| `~/.ssh/id_rsa` | Clave SSH privada si existe y es legible |

## Archivos de alto valor en Windows

```
C:\Windows\System32\drivers\etc\hosts
C:\Windows\boot.ini
C:\inetpub\logs\LogFiles\
C:\Windows\System32\winevt\Logs\System.evtx
```

La sintaxis de path traversal en Windows usa también `../` (funciona en la mayoría de stacks web aunque el sistema operativo subyacente use `\`) — pero si el servidor usa directamente rutas del SO, puede ser necesario usar `..\\`.

## Por qué LFI siempre debe probarse sistemáticamente

Cualquier parámetro que parezca controlar qué "página", "template", "idioma" o "sección" se carga es un candidato directo. La señal más clara: que el valor del parámetro se parezca a un nombre de archivo (`.php`, sin extensión pero con nombre de plantilla reconocible) o que cambiarlo produce una página de error que menciona rutas del sistema de archivos del servidor.
