# Subvirtiendo la lógica de las consultas: bypass de autenticación

## El escenario base

Un formulario de login típico ejecuta, internamente, algo como:

```sql
SELECT * FROM logins WHERE username='admin' AND password = 'p@ssw0rd';
```

Si la base de datos devuelve una fila coincidente, el backend interpreta eso como credenciales válidas. El objetivo del bypass: conseguir que esta consulta devuelva un resultado **sin conocer la contraseña real**.

## Paso 1: confirmar la inyectabilidad

Antes de construir un bypass, hay que confirmar que el campo es vulnerable, probando caracteres que tienen significado especial en SQL:

| Payload | Codificado en URL |
|---|---|
| `'` | `%27` |
| `"` | `%22` |
| `#` | `%23` |
| `;` | `%3B` |
| `)` | `%29` |

```sql
SELECT * FROM logins WHERE username=''' AND password = 'algo';
```

Una sola comilla deja un número impar de comillas, provocando un error de sintaxis SQL visible — la primera confirmación de que la entrada llega sin sanitizar hasta la consulta.

## Paso 2: construir la condición que siempre es verdadera

Aprovechando la precedencia AND-antes-que-OR vista en el apartado anterior, se inyecta una condición que garantiza verdadero independientemente del resto:

```sql
admin' or '1'='1
```

> Nótese que se omite deliberadamente la comilla final de cierre: la comilla simple que ya existe al final de la consulta original (`... AND password = '...'`) se reutiliza para cerrar correctamente la sintaxis, manteniendo el número de comillas equilibrado.

Consulta resultante:

```sql
SELECT * FROM logins WHERE username='admin' or '1'='1' AND password = 'algo';
```

### Desglosando la evaluación

1. **`AND` primero**: `'1'='1'` (verdadero) `AND` `password='algo'` (probablemente falso) → resultado: falso.
2. **`OR` después**: `username='admin'` (verdadero, si ese usuario existe) `OR` falso → resultado final: **verdadero**.

La consulta devuelve la fila de `admin`, sin haber proporcionado nunca su contraseña real.

## El caso sin conocer ningún nombre de usuario válido

Si no se conoce ningún usuario existente, se puede aplicar la misma lógica en el campo de **contraseña** en su lugar:

```sql
algo' or '1'='1
```

```sql
SELECT * FROM logins WHERE username='cualquiera' AND password = 'algo' or '1'='1';
```

Aquí, por precedencia, se evalúa primero `username='cualquiera' AND password='algo'` (probablemente falso), y después `OR '1'='1'` (siempre verdadero) — el resultado final es verdadero sin importar el contenido de ninguno de los dos campos originales.

### El payload mínimo universal

Combinando ambas ideas, ni siquiera hace falta conocer un usuario válido si la inyección se hace correctamente en el campo de usuario:

```sql
' or '1' = '1
```

Funciona porque, sea cual sea la consulta exacta tras él, la condición `OR '1'='1'` garantiza verdadero — el payload de bypass de autenticación más citado en toda la literatura de seguridad web, y ahora completamente entendido en su mecánica interna.

## Cuando hay paréntesis de por medio

Algunas consultas anidan condiciones con paréntesis para forzar un orden de evaluación específico:

```sql
SELECT * FROM logins WHERE (id > 1) AND username='admin' AND password=SHA1('...');
```

Aquí, simplemente inyectar `admin'--` produce un error de sintaxis: el paréntesis de apertura `(` queda sin su correspondiente cierre `)`. La solución es **cerrar explícitamente el paréntesis** dentro de la propia inyección:

```sql
admin')-- -
```

```sql
SELECT * FROM logins WHERE (username='admin')-- ' AND password=...
```

El paréntesis se cierra correctamente, y el comentario (`-- `, tratado en el siguiente apartado) elimina el resto de la consulta original. Esta técnica de **equilibrar manualmente la sintaxis** —contando comillas, paréntesis, y cualquier otro delimitador abierto— es generalizable a prácticamente cualquier variante de consulta que se encuentre en la práctica, no solo a este ejemplo concreto.

## La lección de fondo

Este apartado ilustra el principio central de toda inyección SQL exitosa: **no basta con "romper" la consulta original — hay que reconstruirla de forma que el resultado completo siga siendo sintácticamente válido y, además, lógicamente favorable al atacante**. Dominar la precedencia de operadores y el equilibrio de delimitadores (comillas, paréntesis) es lo que permite adaptar esta técnica a cualquier variante de consulta, en lugar de depender de payloads memorizados que solo funcionan en el caso exacto para el que fueron escritos.
