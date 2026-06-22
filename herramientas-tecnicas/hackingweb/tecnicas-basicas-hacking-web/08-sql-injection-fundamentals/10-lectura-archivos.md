# Lectura de archivos del servidor

## Más allá de los datos de la aplicación: el sistema de archivos

Una inyección SQL con privilegios suficientes no se limita a extraer filas de tablas — puede leer (y, como se verá en el siguiente apartado, escribir) **archivos del sistema operativo** sobre el que corre el servidor de base de datos. Esto convierte una SQLi en un vector potencial de filtración de código fuente completo, archivos de configuración con credenciales, o incluso, en combinación con escritura, en ejecución remota de código.

## El requisito: el privilegio FILE

En MySQL/MariaDB modernos, leer o escribir archivos del sistema requiere que el usuario de base de datos tenga el privilegio **`FILE`** concedido explícitamente — una restricción de seguridad deliberada, ya que esta capacidad es extremadamente potente.

```sql
' UNION SELECT 1, user(), 3, 4-- -
```

```sql
' UNION SELECT 1, super_priv, 3, 4 FROM mysql.user WHERE user="root"-- -
```

Si el usuario activo resulta ser `root` (frecuentemente el caso en aplicaciones mal configuradas que no siguen el principio de mínimo privilegio, tratado en el apartado de mitigación de este bloque), es muy probable que tenga también el privilegio `FILE` — confirmable directamente consultando los privilegios otorgados.

## LOAD_FILE(): leyendo archivos arbitrarios

```sql
SELECT LOAD_FILE('/etc/passwd');
```

`LOAD_FILE()` toma una ruta absoluta y devuelve su contenido completo como resultado de la consulta — siempre que el **usuario del sistema operativo** bajo el que corre el proceso MySQL tenga permisos de lectura sobre ese archivo concreto (independientemente de los privilegios SQL del usuario de base de datos).

Vía inyección UNION:

```sql
' UNION SELECT 1, LOAD_FILE("/etc/passwd"), 3, 4-- -
```

## Caso de uso de alto valor: filtrar el código fuente de la propia aplicación

Conociendo la raíz web habitual de Apache (`/var/www/html` en Linux) y el nombre del script actual (visible en la URL), se puede intentar leer su código fuente directamente:

```sql
' UNION SELECT 1, LOAD_FILE("/var/www/html/search.php"), 3, 4-- -
```

> **Detalle práctico**: si el archivo leído es PHP/HTML, el navegador puede **renderizarlo** en lugar de mostrarlo como texto plano (al fin y al cabo, sigue siendo HTML válido desde la perspectiva del navegador). Para ver el código fuente real tal cual se extrajo, hay que consultar el código fuente de la **respuesta** (`Ctrl+U`), no la vista renderizada.

## Por qué esto es tan valioso para un atacante

Filtrar el código fuente de la propia aplicación convierte de facto una auditoría de **caja negra** en una de **caja blanca**: con el código en mano, se pueden identificar otras vulnerabilidades con mucha más precisión (credenciales hardcodeadas, lógica de autenticación defectuosa, otros puntos de inyección no descubiertos por fuzzing), exactamente la distinción entre tipos de pentesting vista en el bloque de *Introducción a Aplicaciones Web*.

## Rutas de interés habituales más allá del código fuente

| Archivo | Por qué interesa |
|---|---|
| `/etc/passwd` | Lista de usuarios del sistema (sin contraseñas, pero útil para reconocimiento) |
| Archivos de configuración de la aplicación (`config.php`, `.env`, `wp-config.php`) | Credenciales de base de datos, claves de API, secretos de aplicación |
| `/etc/apache2/apache2.conf` o `/etc/nginx/nginx.conf` | Revela la raíz web exacta del servidor — esencial para el siguiente apartado sobre escritura de archivos |
| Logs del servidor web o de la aplicación | Pueden filtrar rutas internas, parámetros, o incluso credenciales registradas por error |

## Limitaciones a tener en cuenta

- El privilegio `FILE` debe estar concedido — en instalaciones modernas y bien configuradas, suele estar restringido, lo que bloquea por completo esta técnica.
- Una variable de configuración adicional, `secure_file_priv`, puede restringir aún más desde/hacia dónde se permite leer o escribir — se trata en detalle en el apartado siguiente, ya que afecta tanto a lectura como a escritura.
- Los permisos del **usuario del sistema operativo** que ejecuta el proceso MySQL (normalmente `mysql` en Linux) también limitan qué archivos son legibles, independientemente de los privilegios SQL.
