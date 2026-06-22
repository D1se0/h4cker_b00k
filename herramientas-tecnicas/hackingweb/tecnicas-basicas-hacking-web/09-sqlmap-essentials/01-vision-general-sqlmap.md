# SQLMap: visión general y técnicas soportadas

## Qué es

[SQLMap](https://github.com/sqlmapproject/sqlmap) es una herramienta gratuita y de código abierto, escrita en Python, que automatiza la detección y explotación de vulnerabilidades de inyección SQL en el contexto de pruebas de penetración **autorizadas**. En desarrollo activo desde 2006, es la herramienta de referencia del sector para este tipo de auditoría.

```bash
sqlmap -u 'http://objetivo.htb/page.php?id=5'
```

```
[INFO] testing connection to the target URL
[INFO] checking if the target is protected by some kind of WAF/IPS/IDS
[INFO] testing if GET parameter 'id' is dynamic
[INFO] heuristic (basic) test shows that GET parameter 'id' might be injectable (possible DBMS: 'MySQL')
[INFO] testing for SQL injection on GET parameter 'id'
```

## Instalación

```bash
sudo apt install sqlmap
# o, para la versión de desarrollo más reciente:
git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git sqlmap-dev
python sqlmap.py
```

Viene preinstalado en la mayoría de distribuciones orientadas a pentesting (Kali, Parrot, PwnBox).

## Amplitud de soporte de motores de bases de datos

SQLMap ofrece la cobertura más amplia de cualquier herramienta de explotación SQL del mercado: MySQL, PostgreSQL, Microsoft SQL Server, Oracle, SQLite, IBM DB2, MariaDB, y decenas más — incluyendo motores menos comunes como CockroachDB, TiDB o Amazon Redshift. Esto la convierte en la herramienta natural por defecto sin importar qué motor se sospeche que está usando el objetivo.

## Las técnicas de detección: BEUSTQ

SQLMap es la única herramienta capaz de detectar y explotar correctamente **todos** los tipos conocidos de inyección SQL — visibles en `sqlmap -hh` bajo `--technique=TECH` (por defecto, `BEUSTQ`, es decir, todas activas):

| Letra | Técnica | Mecanismo |
|---|---|---|
| **B** | Boolean-based blind | Diferencia respuestas `TRUE`/`FALSE` comparando contenido, código HTTP o título de página |
| **E** | Error-based | Provoca errores del DBMS cuyo mensaje filtra el dato buscado |
| **U** | UNION query-based | Extiende la consulta original con `UNION` — la técnica vista en detalle en el bloque anterior |
| **S** | Stacked queries | Apila sentencias adicionales tras la vulnerable (`; DROP TABLE...`) — funciona en MSSQL/PostgreSQL, no en MySQL por defecto |
| **T** | Time-based blind | Usa `SLEEP()` para inferir verdadero/falso por el tiempo de respuesta |
| **Q** | Inline queries | Inserta una subconsulta dentro de la consulta original — poco común, requiere una estructura SQL específica |

### Velocidad relativa de cada técnica

```
UNION-based  >  Error-based  >  Boolean-based blind  >  Time-based blind
   (más rápida)                                          (más lenta)
```

- **UNION-based**: en el escenario ideal, extrae el contenido completo de una tabla con una sola petición.
- **Error-based**: recupera "fragmentos" (hasta ~200 bytes) por cada petición — más lenta que UNION pero más rápida que las variantes ciegas.
- **Boolean-based blind**: extrae aproximadamente 1 bit de información por petición — se necesitan ~7-8 peticiones para recuperar un solo carácter.
- **Time-based blind**: igual de lenta que boolean-based, pero además cada petición "verdadera" implica esperar deliberadamente (vía `SLEEP()`), multiplicando el tiempo total.

### Un séptimo tipo, fuera de BEUSTQ: Out-of-band

Para escenarios donde ninguna de las técnicas anteriores es viable (por ejemplo, una sentencia SQL vulnerable que no es una consulta de lectura, sino parte de una funcionalidad auxiliar sin efecto visible), SQLMap soporta **exfiltración de DNS**: forzando al servidor de base de datos a realizar consultas DNS hacia subdominios controlados por el auditor (`foo.dominio-controlado.com`, donde `foo` codifica el dato extraído), recuperando así la información a través de un canal completamente distinto al de la petición HTTP original.

## Por qué empezar entendiendo esto antes de usar la herramienta

Saber qué técnica está usando SQLMap en cada momento —y por qué elige una sobre otra según lo que observa en las respuestas— es lo que permite **interpretar correctamente** su salida y **ajustarla** cuando la detección automática no encuentra nada a la primera, tema que se desarrolla en los siguientes apartados de este bloque.
