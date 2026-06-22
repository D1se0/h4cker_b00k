# De SQLi a interacción con el sistema operativo

## El último escalón de impacto

Como se vio en el bloque anterior, una inyección SQL con privilegios suficientes puede leer y, en condiciones más restrictivas, escribir archivos en el servidor backend — y desde ahí, en el peor caso, escalar hasta ejecución de comandos sobre el propio sistema operativo. SQLMap automatiza este mismo recorrido completo, ofreciendo además funciones dedicadas para confirmar en qué punto exacto se detiene la viabilidad de la cadena, sin tener que construir manualmente cada payload.

## Confirmando privilegios antes de intentar nada

```bash
sqlmap -u "http://objetivo.htb/?id=1" --is-dba
```

```
current user is DBA: False
```

Sin privilegios de administrador de base de datos, cualquier intento posterior de leer o escribir archivos fallará silenciosamente — por eso este es siempre el primer paso, exactamente como se trabajó manualmente en el bloque anterior al consultar `super_priv` y los privilegios otorgados al usuario activo.

## Lectura de archivos

```bash
sqlmap -u "http://objetivo.htb/?id=1" --file-read "/etc/passwd"
```

SQLMap automatiza por completo el proceso que se vio manualmente con `LOAD_FILE()`: selecciona la técnica más adecuada disponible (UNION, ciega, etc.), reconstruye el contenido del archivo, y lo guarda localmente en el directorio de salida de la sesión para su revisión posterior — sin que el operador tenga que construir manualmente la consulta de extracción.

## Por qué la escritura está mucho más restringida (repaso)

Igual que se explicó en el bloque anterior, escribir archivos arbitrarios en el servidor es la capacidad más peligrosa que una inyección SQL puede otorgar, ya que en último término permite depositar código ejecutable directamente en la raíz web. Por eso los motores modernos exigen, además del privilegio `FILE`, que la variable `secure_file_priv` no esté restringida — sin ambas condiciones, ningún intento de escritura prosperará, sea cual sea la herramienta usada.

```bash
sqlmap -u "http://objetivo.htb/?id=1" --file-write "local.php" --file-dest "/var/www/html/remoto.php"
```

Cuando ambos requisitos se cumplen, SQLMap puede localizar automáticamente la raíz web del servidor (probando rutas comunes o analizando configuración filtrada por lectura de archivos) y depositar el archivo local indicado en la ruta remota especificada.

## El flag `--os-shell`: orquestando el ciclo completo

Cuando los privilegios lo permiten, SQLMap incluye una funcionalidad de alto nivel que automatiza el ciclo completo "escribir un intermediario en el servidor → usarlo para ejecutar comandos → presentar una shell interactiva" en un único flujo guiado, sin que el operador tenga que construir manualmente cada pieza del proceso vista en el bloque anterior (localización de raíz web, escritura del intermediario, confirmación de ejecución).

```bash
sqlmap -u "http://objetivo.htb/?id=1" --os-shell
```

Tras confirmar privilegios y ubicación de escritura, SQLMap presenta un prompt interactivo (`os-shell>`) desde el que cada comando introducido se ejecuta en el servidor remoto a través del mecanismo desplegado, devolviendo la salida estándar directamente en la terminal local — el punto final de la cadena completa de impacto que arrancó con un simple parámetro `id` sin sanitizar.

## Por qué esta capacidad exige el máximo rigor ético y de autorización

Llegar hasta este punto implica tener, de facto, capacidad de ejecución de comandos sobre un servidor de terceros. Esto **solo** es aceptable dentro del alcance explícitamente autorizado de una auditoría de seguridad contratada, un programa de *bug bounty* con reglas de contratación claras, o un entorno de laboratorio propio. Usar esta funcionalidad contra cualquier sistema sin autorización expresa constituye un delito en la gran mayoría de jurisdicciones, independientemente de la intención del operador.

## La perspectiva defensiva: por qué este recorrido nunca debería ser posible

Que una inyección SQL pueda llegar hasta ejecución de comandos revela, casi siempre, un fallo acumulado de varias capas de seguridad simultáneamente:

1. **Falta de consultas parametrizadas** — la causa raíz, vista en el bloque anterior.
2. **Privilegios excesivos del usuario de base de datos** — el principio de mínimo privilegio violado, permitiendo el privilegio `FILE` a una cuenta de aplicación rutinaria.
3. **`secure_file_priv` sin restringir** — una configuración de motor que debería limitarse explícitamente en cualquier despliegue de producción.
4. **Permisos de escritura excesivos en la raíz web** — el proceso de base de datos no debería, en ningún caso, tener permisos de escritura sobre el directorio que sirve contenido público.

Cada una de estas capas, corregida de forma independiente, ya habría bastado para detener la cadena de ataque mucho antes de llegar a ejecución de comandos — la misma filosofía de **defensa en profundidad** que ha aparecido de forma constante a lo largo de todo este temario.

## Cierre del bloque

Con esto se completa el recorrido de SQLMap Essentials: desde entender qué técnica de detección usa internamente, pasando por configurar correctamente el ataque y diagnosticar problemas, hasta la enumeración sistemática y, en el límite, la interacción con el sistema operativo subyacente. El conocimiento manual construido en *SQL Injection Fundamentals* es, en última instancia, lo que permite usar SQLMap con criterio — entendiendo qué hace en cada paso, en lugar de depender ciegamente de una herramienta que, sin ese contexto, sería simplemente una caja negra impredecible.
