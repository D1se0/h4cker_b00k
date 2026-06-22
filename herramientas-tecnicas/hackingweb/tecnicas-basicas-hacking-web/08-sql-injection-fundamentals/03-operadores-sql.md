# Operadores lógicos en SQL

## Por qué dominar AND/OR es la clave del bypass de autenticación

Los operadores lógicos son, sin exagerar, el corazón técnico de las inyecciones de bypass de autenticación que se verán más adelante en este bloque. Entender exactamente cómo se evalúan permite construir el payload correcto con criterio, en lugar de memorizar fórmulas.

## AND

Devuelve verdadero (`1`) únicamente si **ambas** condiciones son verdaderas:

```sql
SELECT 1 = 1 AND 'test' = 'test';  -- 1 (true)
SELECT 1 = 1 AND 'test' = 'abc';   -- 0 (false)
```

En MySQL, cualquier valor distinto de cero se considera verdadero, y el resultado de una comparación booleana se representa como `1` (verdadero) o `0` (falso).

## OR

Devuelve verdadero si **al menos una** de las dos condiciones es verdadera:

```sql
SELECT 1 = 1 OR 'test' = 'abc';  -- 1 (true, porque 1=1 ya es verdadero)
SELECT 1 = 2 OR 'test' = 'abc';  -- 0 (false, ambas son falsas)
```

## NOT

Invierte un valor booleano:

```sql
SELECT NOT 1 = 1;  -- 0
SELECT NOT 1 = 2;  -- 1
```

## Operadores simbólicos equivalentes

| Palabra clave | Símbolo |
|---|---|
| `AND` | `&&` |
| `OR` | `\|\|` |
| `NOT` | `!` |
| `!=` | Distinto de |

## Precedencia: por qué AND se evalúa antes que OR

Este es el detalle técnico que hace posible el bypass de autenticación clásico. Según la [documentación de precedencia de operadores de MySQL](https://dev.mysql.com/doc/refman/8.0/en/operator-precedence.html), `AND` tiene **mayor precedencia** que `OR` — se evalúa primero.

Esto significa: en una expresión `condicion1 OR condicion2 AND condicion3`, MySQL evalúa primero `condicion2 AND condicion3`, y **después** aplica el `OR` con `condicion1`. Si `condicion1` por sí sola ya es verdadera, el resultado completo será verdadero **sin importar** qué devuelva el `AND` posterior — exactamente el mecanismo que permite que una condición como `'1'='1'` inyectada con un `OR` haga que toda la cláusula `WHERE` se evalúe como verdadera, sin importar lo que venga después con `AND`.

```sql
SELECT * FROM logins WHERE username='admin' OR '1'='1' AND password = 'cualquier_cosa';
```

Desglosando la evaluación:

1. `AND` se evalúa primero: `'1'='1'` (verdadero) `AND` `password='cualquier_cosa'` (probablemente falso) → resultado: **falso**.
2. `OR` se evalúa después: `username='admin'` (depende) `OR` (falso del paso 1).
3. Si `username='admin'` existe, el resultado final es **verdadero**, independientemente de la contraseña.

Este análisis exacto —descomponer la precedencia paso a paso— es la base de la técnica de bypass de autenticación que se desarrolla en el apartado *Subvirtiendo la lógica de las consultas* de este mismo bloque.

## Operadores en cláusulas WHERE

```sql
SELECT * FROM logins WHERE username != 'john';
```

`!=` (o `<>`) excluye coincidencias exactas — útil tanto en consultas legítimas como, potencialmente, en técnicas de enumeración cuando se está explotando una inyección a ciegas (visto en bloques posteriores sobre inyección ciega).

## Por qué esto importa más allá del bypass de login

Comprender la precedencia de operadores no es solo relevante para el ejemplo clásico de login: es la base conceptual para construir **cualquier** condición de inyección SQL de forma predecible, incluyendo las condiciones booleanas usadas en inyección ciega (*Boolean-based blind SQLi*), donde controlar con precisión qué evalúa verdadero o falso es literalmente el mecanismo completo de extracción de datos, carácter a carácter.
