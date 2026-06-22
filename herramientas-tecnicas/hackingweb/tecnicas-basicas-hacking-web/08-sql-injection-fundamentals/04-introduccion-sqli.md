# Introducción a la inyección SQL

## Qué significa "inyectar"

La inyección ocurre cuando una aplicación **malinterpreta entrada del usuario como código ejecutable** en lugar de tratarla como una simple cadena de datos. El mecanismo habitual: "escapar" de los límites esperados de la entrada introduciendo un carácter especial (como una comilla simple `'`), de forma que lo que sigue ya no se interprete como dato, sino como sintaxis SQL real.

## El ejemplo canónico

```php
$searchInput = $_POST['findUser'];
$query = "select * from logins where username like '%$searchInput'";
```

En uso normal, `$searchInput` se inserta dentro de las comillas, completando la consulta de forma segura: si se busca `admin`, la consulta resultante es `...like '%admin'` — perfectamente válida.

Pero si el atacante introduce una comilla simple seguida de SQL arbitrario:

```
1'; DROP TABLE users;
```

La consulta resultante es:

```sql
select * from logins where username like '%1'; DROP TABLE users;'
```

La comilla simple inyectada **cierra** el campo de texto esperado por el programador antes de tiempo, dejando el resto de la entrada como SQL real que el motor interpreta y ejecuta — en este caso, eliminando completamente una tabla.

> **Nota técnica importante**: en MySQL, las consultas apiladas separadas por `;` (como en el ejemplo anterior) **no funcionan** a través de la interfaz estándar de la mayoría de drivers/APIs web — sí son posibles en MSSQL y PostgreSQL bajo ciertas configuraciones. Este ejemplo se usa con fines puramente ilustrativos del concepto; las técnicas reales para MySQL que se desarrollan en el resto de este bloque (UNION, comentarios) no dependen de apilar consultas con `;`.

## El problema de los errores de sintaxis

El payload anterior, tal cual, generaría un error:

```
Error: near line 1: near "'": syntax error
```

La comilla simple inyectada deja un número **impar** de comillas en la consulta final, rompiendo su sintaxis. Para que una inyección funcione de verdad, la consulta resultante debe seguir siendo **sintácticamente válida** — sin esto, el ataque simplemente falla con un error, sin ejecutar nada útil.

Existen dos estrategias principales para resolver esto, que se desarrollan en los siguientes apartados:

1. **Usar comentarios SQL** para anular el resto de la consulta original tras la inyección.
2. **Equilibrar el número de comillas** dentro de la propia inyección, de forma que la sintaxis general siga siendo válida.

## Los cinco tipos de inyección SQL, según cómo se obtiene el resultado

| Categoría | Tipo | Cómo funciona |
|---|---|---|
| **In-band** | Union-based | El resultado de la consulta inyectada se imprime directamente en una posición de la página, gracias a `UNION` |
| **In-band** | Error-based | Se provoca deliberadamente un error SQL cuyo mensaje filtra el dato buscado |
| **Blind** | Boolean-based | No hay salida visible directamente; se infiere el dato observando si la página cambia de comportamiento según una condición verdadera/falsa |
| **Blind** | Time-based | Similar al anterior, pero se usa `SLEEP()` para inferir la condición según el tiempo de respuesta |
| **Out-of-band** | — | Ni la salida directa ni el comportamiento son observables; se exfiltra el dato a través de un canal alternativo (por ejemplo, una consulta DNS hacia un servidor controlado por el atacante) |

Este bloque se centra específicamente en **inyección basada en UNION** — la variante más directa de aprender porque el resultado se ve inmediatamente en la respuesta, y la base conceptual sobre la que se construyen las demás técnicas (que se tratan con más profundidad en el bloque siguiente, *SQLMap Essentials*, que automatiza también las variantes ciegas).

## El flujo completo de una explotación exitosa

1. **Inyectar** código fuera de los límites esperados de la entrada (la comilla simple inicial).
2. **Subvertir la lógica** de la consulta original — modificándola (bypass de autenticación) o ejecutando una consulta adicional completa (UNION).
3. **Capturar el resultado** — interpretarlo directamente en la interfaz, provocar un error que lo revele, o inferirlo mediante lógica booleana/temporal.

Los siguientes apartados de este bloque recorren cada uno de estos pasos en profundidad, empezando por la subversión de lógica más sencilla: el bypass de autenticación.
