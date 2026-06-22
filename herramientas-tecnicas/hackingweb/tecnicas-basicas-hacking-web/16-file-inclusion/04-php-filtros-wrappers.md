# Filtros PHP y wrappers de lectura

## Por qué los wrappers de PHP amplían el alcance de LFI

PHP incluye un sistema de "wrappers" (envoltorios de stream) que permiten acceder a distintos tipos de recursos usando una sintaxis de pseudo-protocolo. En el contexto de LFI, el más relevante para lectura de código fuente es `php://filter`, que permite aplicar transformaciones al contenido de un archivo antes de devolverlo.

## El problema: incluir un archivo PHP lo ejecuta

Cuando LFI incluye un archivo `.php`, PHP lo interpreta y ejecuta — no lo devuelve como texto. Si `config.php` solo establece variables de configuración sin generar salida HTML, la respuesta estará vacía aunque el archivo exista:

```
?language=config.php  →  (respuesta vacía)
```

El archivo se incluyó y ejecutó, pero no hay nada que ver.

## La solución: `php://filter` con codificación Base64

El wrapper `php://filter` permite leer el archivo y transformarlo antes de que PHP lo interprete, devolviendo el contenido codificado en lugar de ejecutarlo:

```
php://filter/read=convert.base64-encode/resource=config
```

Incluido vía el parámetro LFI:

```
?language=php://filter/read=convert.base64-encode/resource=config
```

Si la aplicación añade `.php` automáticamente, el recurso será `config.php`. El resultado en la respuesta es una cadena Base64 del código fuente completo del archivo:

```
PD9waHAKICAgIC8vIGRhdGFiYXNlIGNyZWRlbnRpYWxzCiAgICAkdXNlcm5hbWUgPSAiYWRtaW4i...
```

Decodificando:

```bash
echo "PD9waHAK..." | base64 -d
# -> <?php
#    // database credentials
#    $username = "admin";
#    $password = "secret_db_pass";
#    ...
```

## Descubriendo archivos PHP adicionales

Antes de explotar este wrapper, conviene descubrir qué archivos PHP existen en la aplicación:

```bash
ffuf -w wordlist.txt -u "http://objetivo/?language=FUZZ.php" -fs [tamaño_respuesta_vacía]
```

Cualquier archivo que genere una respuesta distinta al comportamiento por defecto es candidato a revelar código fuente valioso — incluso archivos con código de respuesta `302` (redirección) o `403` pueden contener código fuente interesante si se leen directamente vía LFI en lugar de accederse como páginas normales.

## Por qué leer el código fuente es tan valioso

Como se mencionó en los bloques de SQL Injection Fundamentals y XXE: obtener código fuente PHP completo convierte una auditoría de caja negra en una de caja blanca. Esto permite:

- Identificar otras vulnerabilidades que no serían visibles desde fuera (lógica de autenticación, consultas SQL sin parametrizar, otros puntos LFI).
- Extraer credenciales de base de datos, claves de API, y otros secretos hardcodeados.
- Entender exactamente cómo funciona la aplicación para planificar ataques más dirigidos.

## Tabla de filtros disponibles

| Filtro | Uso |
|---|---|
| `convert.base64-encode` | Codifica el archivo en Base64 — el más usado para evitar que PHP ejecute el código |
| `convert.iconv.utf-8.utf-16` | Cambia la codificación del texto |
| `string.rot13` | Aplica ROT13 al contenido |
| `zlib.deflate` | Comprime el contenido |

En la práctica, `convert.base64-encode` es el de uso casi universal para lectura de código fuente PHP vía LFI, porque garantiza que el output sea una cadena ASCII válida sin caracteres que puedan romper la respuesta HTTP.
