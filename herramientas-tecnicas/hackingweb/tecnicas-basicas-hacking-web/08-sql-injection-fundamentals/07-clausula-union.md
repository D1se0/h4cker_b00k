# La cláusula UNION

## Qué hace

`UNION` combina los resultados de dos (o más) sentencias `SELECT` independientes en un único conjunto de resultados:

```sql
SELECT * FROM ports
UNION
SELECT * FROM ships;
```

```
+----------+-----------+
| code     | city      |
+----------+-----------+
| CN SHA   | Shanghai  |
| SG SIN   | Singapore |
| Morrison | New York  |
| ZZ-21    | Shenzhen  |
+----------+-----------+
```

Las filas de ambas consultas se fusionan en una única salida, aunque procedan de tablas completamente distintas.

## La regla fundamental: mismo número de columnas

`UNION` exige que ambas sentencias `SELECT` devuelvan **exactamente el mismo número de columnas**. Si no coincide:

```sql
SELECT city FROM ports UNION SELECT * FROM ships;

ERROR 1222 (21000): The used SELECT statements have a different number of columns
```

Esta restricción es la base técnica de toda la metodología de **inyección basada en UNION**: antes de poder extraer datos de otra tabla, hay que determinar exactamente cuántas columnas tiene la consulta original — paso que se desarrolla en el siguiente apartado.

## Por qué UNION es tan potente para inyección SQL

Una vez que se confirma el número correcto de columnas, se puede usar `UNION SELECT` para anexar **cualquier dato de cualquier tabla y base de datos accesible** al resultado de la consulta original, simplemente sustituyendo la segunda mitad de la unión:

```sql
SELECT * FROM products WHERE product_id = 'entrada_usuario'
```

Si se inyecta:

```sql
1' UNION SELECT username, password FROM passwords-- -
```

```sql
SELECT * FROM products WHERE product_id = '1' UNION SELECT username, password FROM passwords-- -'
```

Asumiendo que `products` tiene dos columnas, el resultado combinado incluirá tanto los productos legítimos como, anexados, los nombres de usuario y contraseñas de una tabla completamente distinta — exactamente el tipo de exfiltración de datos que constituye el objetivo de la explotación basada en UNION.

## Rellenando columnas con datos de relleno (padding)

En la práctica, la consulta original casi nunca tiene el mismo número de columnas que la tabla de interés del atacante. La solución: rellenar las columnas sobrantes con valores "de relleno" que no rompan la sintaxis.

```sql
SELECT * FROM products WHERE product_id = '1' UNION SELECT username, 2 FROM passwords-- -
```

Si `products` tiene dos columnas, y solo interesa extraer `username` de la tabla `passwords`, se rellena la segunda posición con cualquier valor — un número (`2`) es la opción más práctica.

### Por qué usar números (y no, por ejemplo, texto) como relleno

Usar números como `1`, `2`, `3`... en cada posición de relleno tiene una ventaja operativa clave: permite **rastrear visualmente qué columna corresponde a qué posición** en la respuesta final — esencial en el siguiente paso de la metodología, donde hay que identificar **cuál** de las columnas devueltas se imprime realmente en la página (no todas las columnas de una consulta llegan necesariamente a mostrarse en la interfaz).

> **Para inyecciones avanzadas**: `NULL` es una alternativa universal de relleno, ya que es compatible con cualquier tipo de dato (numérico, texto, fecha) sin generar errores de tipo — preferible a números cuando el tipo de columna es incierto.

## Coincidencia de tipos de datos

Más allá del número de columnas, MySQL también exige (en la mayoría de los casos) que los **tipos de datos** sean compatibles posición a posición. Si una columna espera un número y se inyecta texto en esa posición concreta, puede producirse un error — otra razón por la que `NULL`, al ser compatible con cualquier tipo, suele ser la opción de relleno más segura cuando no se conoce de antemano el tipo exacto esperado en cada columna.

El siguiente apartado pone en práctica todo esto: el flujo completo, paso a paso, para descubrir el número de columnas y construir una inyección UNION funcional desde cero.
