# SQL Injection Fundamentals

La inyección SQL es, históricamente, una de las vulnerabilidades web más devastadoras: permite leer, modificar o eliminar datos de toda una base de datos, eludir mecanismos de autenticación, leer y escribir archivos en el servidor, y en muchos casos escalar hasta ejecución remota de código completa. Este bloque construye el conocimiento desde cero — fundamentos de bases de datos relacionales y sintaxis SQL/MySQL — hasta la explotación práctica completa: descubrimiento, bypass de autenticación, inyección basada en UNION, enumeración sistemática vía `INFORMATION_SCHEMA`, lectura y escritura de archivos, y finalmente las técnicas de mitigación que cierran el círculo desde la perspectiva defensiva.

## Contenido

1. [Bases de datos y SQL: fundamentos](01-fundamentos-bases-datos.md)
2. [MySQL: línea de comandos, tablas y consultas](02-mysql-fundamentos.md)
3. [Operadores lógicos en SQL](03-operadores-sql.md)
4. [Introducción a la inyección SQL](04-introduccion-sqli.md)
5. [Subvirtiendo la lógica de las consultas: bypass de autenticación](05-subvirtiendo-logica.md)
6. [Uso de comentarios en inyecciones SQL](06-uso-comentarios.md)
7. [La cláusula UNION](07-clausula-union.md)
8. [Inyección basada en UNION](08-inyeccion-union.md)
9. [Enumeración de bases de datos vía INFORMATION_SCHEMA](09-enumeracion-bases-datos.md)
10. [Lectura de archivos del servidor](10-lectura-archivos.md)
11. [Escritura de archivos y camino a RCE](11-escritura-archivos.md)
12. [Mitigación de la inyección SQL](12-mitigacion-sqli.md)

## Por qué este bloque importa

SQL Injection sigue apareciendo en el Top 10 de OWASP y en compromisos reales de alto perfil, décadas después de ser ampliamente conocida. Entender no solo "qué payload probar" sino **por qué funciona cada paso** —desde la lógica booleana del bypass de autenticación hasta la estructura exacta de `INFORMATION_SCHEMA`— es lo que diferencia a quien copia payloads de listas de quien realmente puede adaptar la técnica a cualquier escenario nuevo, incluyendo los que se cubren en el bloque siguiente de *SQLMap Essentials*.
