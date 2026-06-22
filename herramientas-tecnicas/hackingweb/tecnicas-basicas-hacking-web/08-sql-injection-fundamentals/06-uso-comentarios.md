# Uso de comentarios en inyecciones SQL

## Por qué los comentarios son una herramienta tan potente

En lugar de equilibrar cuidadosamente comillas y paréntesis (como en el apartado anterior), una alternativa mucho más simple y generalizable consiste en **comentar** —es decir, hacer que el motor SQL ignore por completo— todo lo que sigue a la inyección. Esto evita preocuparse por la sintaxis del resto de la consulta original: ya no importa qué venga después, porque nunca se evaluará.

## Sintaxis de comentarios en MySQL

| Sintaxis | Notas |
|---|---|
| `-- ` | Requiere un espacio en blanco después de los dos guiones para ser válido en MySQL |
| `#` | Alternativa de un solo carácter |
| `/* ... */` | Comentario de bloque/en línea, menos habitual en inyecciones básicas |

```sql
SELECT username FROM logins; -- Comentario explicativo
```

```sql
SELECT * FROM logins WHERE username = 'admin'; # Todo esto se ignora AND password = 'algo'
```

> **Detalle crítico de `--`**: en MySQL, dos guiones por sí solos **no inician** un comentario — necesitan ir seguidos de al menos un espacio. En URLs, ese espacio suele codificarse como `+` o `%20`, por lo que es habitual escribir el payload como `-- -` (con un guion extra al final) para dejar visualmente claro que hay un espacio tras los dos guiones iniciales.

> **Detalle sobre `#` en navegadores**: al escribir directamente en la barra de direcciones, el símbolo `#` suele interpretarse como un fragmento de URL (visto en el bloque de *Web Requests*) y puede no enviarse al servidor. Para usarlo de forma fiable como comentario SQL en una URL, conviene codificarlo como `%23`.

## Bypass de autenticación usando comentarios

Con el nombre de usuario `admin'--`:

```sql
SELECT * FROM logins WHERE username='admin'-- ' AND password = 'algo';
```

Todo lo que sigue a `--` (incluida la comilla de cierre del nombre de usuario inyectado, y la condición de contraseña completa) se ignora. La consulta efectiva que el motor evalúa es:

```sql
SELECT * FROM logins WHERE username='admin'
```

Sin ningún chequeo de contraseña en absoluto — login exitoso solo con conocer (o adivinar) un nombre de usuario válido.

## Comentarios y paréntesis combinados

Retomando el caso de consultas con paréntesis del apartado anterior:

```sql
SELECT * FROM logins WHERE (username='admin')
```

Con el nombre de usuario `admin')-- `:

```sql
SELECT * FROM logins WHERE (username='admin')-- ' AND password=SHA1('...')
```

El paréntesis se cierra explícitamente dentro de la inyección, y el comentario elimina cualquier resto — combinando ambas técnicas (cierre de delimitadores + comentarios) para máxima robustez frente a estructuras de consulta más complejas.

## Por qué los comentarios son, en la práctica, la técnica preferida

Frente a la alternativa de "contar y equilibrar" delimitadores manualmente (que requiere conocer o inferir con precisión la estructura exacta de la consulta original), los comentarios ofrecen una ventaja decisiva: **no es necesario saber qué viene después de la inyección** — simplemente se anula, sea lo que sea. Esto hace que la técnica de comentarios sea mucho más robusta y generalizable frente a consultas de estructura desconocida, que es exactamente la situación habitual en una auditoría real donde no se tiene acceso al código fuente del backend.

## Conectando con la inyección basada en UNION

Los comentarios cumplen un segundo propósito, además del bypass de autenticación: cuando se inyecta una consulta `UNION SELECT` completa (tema del siguiente apartado), el comentario al final sigue siendo necesario para anular cualquier resto de la consulta original que pudiera causar un error de sintaxis tras la cláusula `UNION` inyectada — una técnica que se usará de forma constante en el resto de este bloque.
