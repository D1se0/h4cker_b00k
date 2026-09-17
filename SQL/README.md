---
icon: server
---

# SQL — Fundamentals

> Guía completa de SQL basada en [sql-learning](https://d1se0.github.io/sql-learning/) (SQL Learning — Cheatsheet + Playground). Todo explicado en español, pensado para alguien que **nunca ha tocado SQL** y quiere dominarlo desde cero, incluyendo su uso en **ciberseguridad y hacking ético**.

***

## 📖 ¿Qué es SQL y por qué deberías aprenderlo?

**SQL (Structured Query Language)** es el lenguaje estándar para interactuar con **bases de datos relacionales**. Permite crear, modificar y consultar datos de manera eficiente. Casi todas las aplicaciones web del mundo guardan su información (usuarios, contraseñas, pedidos, mensajes...) en una base de datos SQL, y se comunican con ella mediante consultas SQL.

Por eso SQL es **la herramienta número uno** tanto para desarrolladores como para pentesters: si sabes cómo se construyen las consultas, sabes cómo se atacan (SQL Injection) y cómo se defienden.

***

## 🗺️ Esquema del curso (orden recomendado)

Sigue las secciones en este orden exacto. Cada capítulo está pensado para leerse **en secuencia**: primero entiendes qué es una base de datos, luego aprendes a leer datos, después a filtrarlos, combinarlos, calcular con ellos y finalmente a crear y modificar la estructura. El capítulo 8 es el bonus de hacking.

| # | Capítulo                                                      | Qué aprenderás                                                                               | Nivel         |
| - | ------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ------------- |
| 0 | [Fundamentos — Bases de Datos y SQL](00-fundamentos.md)       | Qué es una BD relacional, tablas, filas, columnas, PK/FK, dialectos, instalar SQLite y MySQL | 🟢 Cero       |
| 1 | [Query Basics — Tus Primeras Consultas](01-query-basics.md)   | SELECT, WHERE, INSERT, UPDATE, DELETE                                                        | 🟢 Cero       |
| 2 | [Filtrado Avanzado](02-filtrado-avanzado.md)                  | Operadores AND/OR/NOT, ORDER BY, LIKE, IN, BETWEEN, DISTINCT                                 | 🟡 Básico     |
| 3 | [Consultas Multi-Tabla](03-multi-tabla.md)                    | JOIN, UNION, GROUP BY, HAVING, EXISTS, ANY/ALL, CASE, NULL, IFNULL, Alias                    | 🟡 Básico     |
| 4 | [Funciones Agregadas](04-funciones-agregadas.md)              | COUNT, SUM, AVG, MAX, MIN + GROUP BY/HAVING combinados                                       | 🟡 Básico     |
| 5 | [Funciones de Utilidad](05-funciones-utilidad.md)             | Cadena, matemáticas, fecha, window functions (LAG, LEAD, FIRST\_VALUE...)                    | 🟠 Intermedio |
| 6 | [Tablas y DDL — Diseño de la Base de Datos](06-tablas-ddl.md) | Tipos de datos, CREATE/ALTER/DROP TABLE, constraints, PK, FK, índices, auto-increment        | 🟠 Intermedio |
| 7 | [SQL para Hacking — Inyección SQL](07-sql-para-hacking.md)    | SQLi: tipos, detección, sqlmap, payloads, prevención + CTFs recomendados                     | 🔴 Hacker     |
| 8 | [Recursos, Playground y Retos](08-recursos.md)                | Herramientas, playgrounds online, retos prácticos, chuleta final                             | 🔗 Extra      |

### 💡 Cómo estudiar este material

1. **Lee el capítulo en orden** — cada uno asume que ya sabes lo anterior.
2. **Ejecuta TODOS los ejemplos** — no sirve de nada leer SQL sin escribirlo.
3. **Practica en el playground** de [sql-learning](https://d1se0.github.io/sql-learning/) (SQLite real en el navegador, no requiere instalar nada).
4. **Haz los retos** del capítulo 8 cuando termines la teoría.
5. En GitBook, activa el modo **página a página** con este mismo orden en el índice (tabla de contenidos).

***

## 📚 Bases de datos de ejemplo usadas en los ejemplos

Todos los ejemplos usan un hospital ficticio con estas tablas (igual que el playground de sql-learning):

| Tabla        | Descripción            | Columnas principales                                                                                                    |
| ------------ | ---------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `patients`   | Pacientes del hospital | `patient_id`, `first_name`, `last_name`, `gender`, `birth_date`, `city`, `province_id`, `allergies`, `height`, `weight` |
| `admissions` | Ingresos de pacientes  | `admission_id`, `patient_id`, `admission_date`, `discharge_date`, `diagnosis`, `attending_doctor_id`                    |
| `doctors`    | Médicos                | `doctor_id`, `first_name`, `last_name`, `specialty`                                                                     |

> 🔎 Si en un ejemplo ves una columna que no reconoces, vuelve a esta tabla para ubicarla.

***

## 🚀 ¿Cómo subir esta guía a tu GitBook?

### Estructura de carpetas y archivos

```
SQL/
├── README.md                  ← Página de inicio del space "SQL" en GitBook
├── 00-fundamentos.md
├── 01-query-basics.md
├── 02-filtrado-avanzado.md
├── 03-multi-tabla.md
├── 04-funciones-agregadas.md
├── 05-funciones-utilidad.md
├── 06-tablas-ddl.md
├── 07-sql-para-hacking.md
└── 08-recursos.md
```

### Pasos para subirlo

1. **Crea un Space nuevo** en tu GitBook ([h4cker\_b00k](https://dise0.gitbook.io/h4cker_b00k)) llamado `SQL` (o una subcolección dentro del libro).
2. **Sube los archivos en orden numérico**: GitBook usa el nombre del archivo para ordenar si usas el prefijo numérico (`00-`, `01-`, `02-`...).
3. En GitBook, edita la **Tabla de Contenidos (SUMMARY)** y arrastra las páginas para que queden: `README` (portada) → `00-fundamentos` → `01-query-basics` → ... → `08-recursos`.
4. **Activa los bloques de código con sintaxis SQL**: en GitBook los bloques \`\`\`sql se resaltan automáticamente. Verifica que el bloque de código use `sql` como lenguaje.
5. Si quieres, **añade el capítulo 7 como página "protegida"** (con un aviso legal, ya lo incluye) o sepáralo en un space aparte llamado `Hacking` si prefieres mantener el libro más "limpio".
6. Publica los cambios. GitBook sincroniza con GitHub si conectas el repo — si lo haces, simplemente sube esta carpeta `SQL/` al repo conectado y GitBook la detectará.

### 🧭 Cómo "dispersar" (distribuir) el contenido en GitBook

* **README.md** = la **portada** del space: índice, explicación general y tabla con el orden de lectura. No repitas contenido de los capítulos aquí.
* **Un capítulo = una página** de GitBook. No unes varios capítulos en una sola página: sería enorme y difícil de navegar.
* Cada capítulo ya tiene **subsecciones con headers (`##`, `###`)** que GitBook convertirá en **mini-tabla de contenidos lateral** automáticamente.
* Los **bloques de código** y **tablas** de Markdown se renderizan perfectamente en GitBook sin configuración extra.
* Si un capítulo te parece muy largo para una sola página, divídelo en dos y renombra con decimales (`05a-funciones-cadena.md`, `05b-window-functions.md`) manteniendo el orden numérico.

***

## ⚠️ Aviso legal

El capítulo 7 (SQL para Hacking) se proporciona **únicamente con fines educativos**. Practicar inyección SQL en sistemas sin autorización explícita es **ilegal** en la mayoría de países. Practica solo en:

* Laboratorios propios (máquinas virtuales, Docker).
* Plataformas legales: HackTheBox, TryHackMe, PortSwigger Web Security Academy, OWASP Juice Shop.
* Programas de bug bounty con scope autorizado.

***
