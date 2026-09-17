---
icon: compass
---

# 9 · Recursos, Playground y Chuleta Final

> El mapa para seguir practicando: tu playground, herramientas, retos y una chuleta con TODO el curso en una página.

***

## 🎮 Tu playground: SQL Learning

**URL:** [https://d1se0.github.io/sql-learning/](https://d1se0.github.io/sql-learning/)

* **SQLite real en el navegador** (nada que instalar).
* Base de datos de hospital lista para usar: `patients`, `admissions`, `doctors`.
* Buscador de querys y comandos.
* Secciones organizadas igual que esta guía: Query Basics, Filtering, Functions, Tables.
* Retos para practicar.

**Cómo sacarle partido:**

1. Lee un capítulo de esta guía → 2. Repite TODOS los ejemplos en el playground → 3. Haz los mini-retos → 4. Intenta los retos del playground.

***

## 🛠️ Herramientas imprescindibles

| Herramienta                                         | Para qué                                       |
| --------------------------------------------------- | ---------------------------------------------- |
| [DB Browser for SQLite](https://sqlitebrowser.org/) | Explorar archivos `.db`/`.sqlite` con GUI      |
| `sqlite3` (CLI)                                     | Consola rápida para SQLite                     |
| `mysql` (CLI)                                       | Cliente MySQL/MariaDB                          |
| [DBeaver](https://dbeaver.io/)                      | Cliente universal (MySQL, Postgres, SQLite...) |
| [sqlmap](https://sqlmap.org/)                       | Automatización de inyección SQL (solo legal ✋) |
| Burp Suite                                          | Interceptar parámetros donde probar SQLi       |
| [CyberChef](https://gchq.github.io/CyberChef/)      | Decodificar payloads y hashes                  |

***

## 🏆 Retos y práctica

| Plataforma                                                                  | Nivel | Nota                    |
| --------------------------------------------------------------------------- | ----- | ----------------------- |
| [sql-learning](https://d1se0.github.io/sql-learning/) retos                 | 🟢    | Empieza aquí            |
| [SQLZoo](https://sqlzoo.net)                                                | 🟢    | Ejercicios de SQL puro  |
| [pgexercises.com](https://pgexercises.com)                                  | 🟡    | PostgreSQL interactivo  |
| [PortSwigger SQLi Labs](https://portswigger.net/web-security/sql-injection) | 🟠    | El estándar para SQLi   |
| OWASP Juice Shop                                                            | 🟠    | App vulnerable completa |
| HackTheBox / TryHackMe                                                      | 🔴    | SQLi en máquinas reales |
| [CTFs de tu repo](https://github.com/D1se0)                                 | 🔴    | Writeups propios        |

***

## 📋 Chuleta final — Todo el curso en una página

### DML — Manejo de datos

```sql
SELECT col1, col2 FROM tabla;              -- leer columnas
SELECT * FROM tabla;                        -- leer todo
SELECT * FROM tabla WHERE cond;             -- filtrar
SELECT * FROM tabla ORDER BY col DESC;      -- ordenar
SELECT DISTINCT col FROM tabla;             -- sin duplicados
SELECT * FROM tabla LIMIT 10;               -- solo 10 filas

INSERT INTO tabla (col1, col2) VALUES (v1, v2);   -- insertar
UPDATE tabla SET col = v WHERE cond;              -- actualizar ⚠️WHERE
DELETE FROM tabla WHERE cond;                     -- borrar ⚠️WHERE
```

### Filtrado

```sql
WHERE a = 1 AND b = 2 OR NOT c = 3
WHERE col LIKE 'a%'       -- empieza por a  (% = varios, _ = uno)
WHERE col IN (1, 2, 3)    -- lista (o subconsulta)
WHERE col BETWEEN 1 AND 10-- rango inclusivo
WHERE col IS NULL         -- vacío (nunca col = NULL)
```

### Multi-tabla

```sql
SELECT * FROM t1 JOIN t2 ON t1.id = t2.id;   -- intersección
SELECT * FROM t1 LEFT JOIN t2 ON t1.id = t2.id; -- todo t1
SELECT col FROM t1 UNION SELECT col FROM t2;    -- apilar resultados
SELECT COUNT(*), col FROM t GROUP BY col HAVING COUNT(*) > 1;
```

### Agregadas y funciones

```sql
COUNT() AVG() SUM() MAX() MIN()              -- agregadas
CONCAT(a, b)  LEN(s)  UPPER(s)  LOWER(s)     -- cadena
ROUND(n, d)  FLOOR(n)  CEIL(n)  ABS(n)  POWER(b, e)  SQRT(n)
CURRENT_TIMESTAMP  YEAR(d)  MONTH(d)  DAY(d)
CASE WHEN c1 THEN r1 ELSE r2 END             -- if/else
LAG(x) OVER()  LEAD(x) OVER()                -- window
```

### DDL — Estructura

```sql
CREATE TABLE t (id int PRIMARY KEY, nombre varchar(50) NOT NULL);
ALTER TABLE t ADD col tipo;         -- añadir columna
ALTER TABLE t DROP COLUMN col;      -- quitar columna
DROP TABLE t;                       -- borrar tabla ⚠️
CREATE INDEX idx ON t (col);        -- índice
-- Constraints: NOT NULL, UNIQUE, PRIMARY KEY, FOREIGN KEY, CHECK, DEFAULT
```

### Orden de ejecución de una consulta (¡mentalidad clave!)

```sql
SELECT    → 5. se proyectan las columnas
FROM      → 1. de dónde sacan los datos
WHERE     → 2. se filtran filas
GROUP BY  → 3. se agrupan
HAVING    → 4. se filtran grupos
ORDER BY  → 6. se ordena
LIMIT     → 7. se recorta
```

***

## 🎓 ¿Y ahora qué?

1. ✅ Termina los retos del playground y de esta guía.
2. ✅ Practica los labs de PortSwigger hasta dominar SQLi manual.
3. ✅ Aprende un lenguaje de backend (PHP/Python/Node) y usa prepared statements.
4. ✅ Mete los writeups de tus CTFs en tu GitBook, junto a esta guía.
5. ✅ Enseña lo aprendido: la mejor forma de afianzar SQL es explicarlo (como esta guía 😉).

***

[⬅️ Volver al índice](./) | [⬅️ Capítulo anterior: SQL para Hacking](07-sql-para-hacking.md)
