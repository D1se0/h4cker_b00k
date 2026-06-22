# Mitigación de la inyección SQL

## El código vulnerable de referencia

```php
$username = $_POST['username'];
$password = $_POST['password'];

$query = "SELECT * FROM logins WHERE username='" . $username . "' AND password = '" . $password . "';";

if (!mysqli_query($conn, $query)) {
    die('Error: ' . mysqli_error($conn));
}
```

Toda la vulnerabilidad nace de un único patrón: **concatenar entrada del usuario directamente dentro de la cadena SQL**, sin ningún tratamiento intermedio. Cada técnica de mitigación que sigue ataca este mismo patrón desde un ángulo distinto.

## Capa 1: Sanitización de entrada

Escapar caracteres con significado especial en SQL (comillas, principalmente), de forma que dejen de tener efecto sintáctico:

```php
$username = mysqli_real_escape_string($conn, $_POST['username']);
$password = mysqli_real_escape_string($conn, $_POST['password']);

$query = "SELECT * FROM logins WHERE username='" . $username . "' AND password = '" . $password . "';";
```

`mysqli_real_escape_string()` antepone una barra invertida a cualquier comilla recibida, neutralizando el intento de "escapar" del campo de texto esperado. Equivalentes en otros entornos: `pg_escape_string()` para PostgreSQL.

> **Limitación importante**: estas funciones de escape dependen de aplicarse **consistentemente en cada punto** donde entra datos del usuario — un único punto olvidado reabre la vulnerabilidad. Por eso, aunque útil, esta técnica no es la defensa preferida frente a las consultas parametrizadas (vistas más abajo).

## Capa 2: Validación de entrada

Restringir la entrada a un formato esperado, **rechazando** cualquier cosa que no encaje, en lugar de intentar "limpiarla":

```php
$pattern = "/^[A-Za-z\s]+$/";
$code = $_GET["port_code"];

if (!preg_match($pattern, $code)) {
    die("Invalid input! Please try again.");
}

$q = "Select * from ports where port_code ilike '%" . $code . "%'";
```

Si se sabe que un campo concreto (un código de puerto, en este ejemplo) solo debería contener letras y espacios, cualquier entrada que incluya comillas, punto y coma, u otros caracteres SQL especiales se **rechaza directamente**, sin llegar nunca a construirse la consulta.

```sql
'; SELECT 1,2,3,4-- -
```

Con la validación en su sitio, este payload nunca llega a ejecutarse — la petición se rechaza antes de tocar la base de datos.

## Capa 3: Privilegios de usuario mínimos

El principio de **mínimo privilegio** aplicado al usuario de base de datos que usa la aplicación: nunca debería usarse una cuenta con privilegios de superusuario (`root`) para las operaciones rutinarias de la aplicación.

```sql
CREATE USER 'reader'@'localhost';
GRANT SELECT ON ilfreight.ports TO 'reader'@'localhost' IDENTIFIED BY 'p@ssw0Rd!!';
```

Con este usuario limitado, incluso si una inyección SQL logra ejecutarse con éxito, su **alcance** queda drásticamente reducido:

```sql
SELECT * FROM ilfreight.credentials;
ERROR 1142 (42000): SELECT command denied to user 'reader'@'localhost' for table 'credentials'
```

El atacante puede, como mucho, leer la tabla `ports` (la única autorizada) — sin acceso a `credentials`, sin privilegio `FILE` para leer/escribir archivos, sin capacidad de modificar ni eliminar nada. Esta única medida, aplicada de forma sistemática, **limita drásticamente el impacto** incluso cuando todas las demás defensas fallan.

## Capa 4: Web Application Firewall (WAF)

Un WAF inspecciona el tráfico HTTP entrante y rechaza automáticamente peticiones que coincidan con patrones de ataque conocidos (la presencia de `INFORMATION_SCHEMA`, `UNION SELECT`, secuencias de comillas sospechosas, etc.).

Opciones: open source (**ModSecurity**) o comerciales (**Cloudflare**, entre otros). Aporta una capa de defensa adicional, pero —como se ha mencionado en bloques anteriores de este temario— **nunca debe ser la única línea de defensa**: los WAF pueden evadirse con técnicas de ofuscación de payloads, y nunca sustituyen un código fundamentalmente seguro.

## Capa 5: Consultas parametrizadas (la defensa más robusta)

La técnica más efectiva, con diferencia: en lugar de **concatenar** entrada de usuario dentro de la cadena SQL, se usan **marcadores de posición** que el driver de base de datos rellena de forma segura, tratando siempre el valor como dato puro — nunca como código SQL, sin importar qué contenga.

```php
$username = $_POST['username'];
$password = $_POST['password'];

$query = "SELECT * FROM logins WHERE username=? AND password = ?";
$stmt = mysqli_prepare($conn, $query);
mysqli_stmt_bind_param($stmt, 'ss', $username, $password);
mysqli_stmt_execute($stmt);
$result = mysqli_stmt_get_result($stmt);
```

Los signos de interrogación (`?`) marcan las posiciones donde se insertarán los valores; `mysqli_stmt_bind_param()` los vincula de forma segura, garantizando que **ninguna comilla, punto y coma, ni cualquier otro carácter SQL especial** tenga efecto sintáctico — independientemente de lo que el usuario envíe. Esto elimina la inyección SQL **de raíz**, no solo la mitiga: el motor nunca llega a interpretar la entrada del usuario como parte de la estructura de la consulta, sea cual sea su contenido.

## Por qué las consultas parametrizadas son superiores a la sanitización

| Aspecto | Sanitización (escape) | Consultas parametrizadas |
|---|---|---|
| Garantía | Depende de aplicarse en cada punto correctamente | Estructural — imposible de saltarse por descuido puntual |
| Robustez frente a nuevos vectores de bypass | Vulnerable a técnicas de evasión de escape no contempladas | El dato nunca se interpreta como código, sin importar el vector |
| Mantenimiento | Requiere disciplina constante en todo el código | Una vez adoptado el patrón, se aplica de forma consistente |

## La estrategia de defensa en profundidad

Ninguna capa aislada es perfecta. La estrategia robusta combina **todas** simultáneamente:

```
Consultas parametrizadas (defensa estructural primaria)
  + Validación de entrada (rechazo temprano de formato inesperado)
  + Privilegios mínimos (limita el impacto si algo falla)
  + WAF (capa adicional de detección de patrones conocidos)
```

Esta combinación es exactamente el mismo principio de **defensa en profundidad** visto al cerrar el bloque de XSS: ninguna medida individual es infalible, pero su combinación reduce drásticamente tanto la probabilidad de que una inyección tenga éxito como el daño potencial si, pese a todo, alguna lo consigue.

## Cierre del bloque

Con esto se completa el recorrido de SQL Injection Fundamentals: desde la sintaxis SQL más básica hasta ejecución remota de código completa, pasando por el bypass de autenticación, la inyección basada en UNION, la enumeración sistemática de bases de datos, y la lectura/escritura de archivos del servidor. El siguiente bloque, *SQLMap Essentials*, retoma exactamente este conocimiento para automatizar todo este proceso —incluyendo las variantes ciegas (boolean-based, time-based) que aquí solo se mencionaron conceptualmente— con una de las herramientas más potentes y usadas en pentesting de bases de datos.
