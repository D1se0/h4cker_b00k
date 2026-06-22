# Vulnerabilidades web comunes

Este apartado funciona como un primer mapa de las vulnerabilidades más habituales en aplicaciones web, todas presentes —en distintas formas— en el [Top 10 de OWASP](https://owasp.org/www-project-top-ten/). Cada una se trata con mucho más detalle en su bloque dedicado más adelante; aquí el objetivo es entender la idea general y por qué importan.

## Autenticación y control de acceso defectuosos

Son, en conjunto, de las categorías más comunes y peligrosas:

- **Broken Authentication**: fallos que permiten a un atacante saltarse por completo el proceso de autenticación — iniciar sesión sin credenciales válidas, o escalar de usuario normal a administrador sin tener los privilegios necesarios.
- **Broken Access Control**: fallos que permiten acceder a páginas o funcionalidades que no deberían estar disponibles para ese usuario — por ejemplo, que un usuario normal acceda directamente a un panel de administración simplemente conociendo (o adivinando) su URL.

Un ejemplo histórico ilustrativo: una aplicación de gestión universitaria con una vulnerabilidad de *authentication bypass* mediante una inyección SQL tan simple como introducir `' or 0=0 #` en el campo de correo electrónico, con cualquier contraseña — la condición `0=0` siempre es verdadera, por lo que la consulta de validación de login devuelve un resultado positivo independientemente de las credenciales reales.

Estas categorías se desarrollan en profundidad en los bloques de *Broken Authentication*, *Login Brute Forcing* y *Web Attacks* (en concreto, IDOR como ejemplo paradigmático de control de acceso roto).

## Carga de archivos maliciosos

Si una aplicación permite subir archivos (fotos de perfil, documentos, adjuntos) sin validar adecuadamente su tipo y contenido, un atacante puede subir un script malicioso (por ejemplo, un webshell en PHP) que, al ejecutarse en el servidor, otorga capacidad de ejecución de comandos sobre el sistema.

Es sorprendentemente habitual encontrar validaciones insuficientes incluso en software ampliamente distribuido — por ejemplo, plugins de gestores de contenido populares que han presentado vulnerabilidades de carga de archivos sin restricciones, explotables simplemente subiendo un archivo con doble extensión (`shell.php.jpg`) que el servidor termina interpretando como PHP ejecutable pese a la extensión final aparentemente inofensiva.

Se desarrolla en profundidad en el bloque de *File Upload Attacks*.

## Inyección de comandos

Cuando una aplicación ejecuta comandos del sistema operativo incorporando entrada de usuario sin la sanitización adecuada, un atacante puede inyectar comandos adicionales que se ejecutarán junto al comando original. Un caso de ejemplo: un campo que toma una dirección IP para ejecutar un `ping`, donde añadir `| comando_arbitrario` tras la IP permite ejecutar ese comando adicional si la aplicación no filtra el carácter `|` ni otros operadores de encadenamiento.

Se desarrolla en profundidad en el bloque de *Command Injections*.

## Inyección SQL (SQLi)

Cuando una consulta SQL incorpora entrada de usuario sin parametrizar, un atacante puede alterar la lógica de esa consulta para que devuelva resultados distintos a los previstos — desde saltarse un login hasta extraer toda la base de datos, pasando por leer o escribir archivos en el servidor de base de datos, e incluso, en ciertas configuraciones, ejecutar comandos en el sistema operativo subyacente.

Se desarrolla en profundidad —con mucho detalle práctico— en los bloques de *SQL Injection Fundamentals* y *SQLMap Essentials*.

## El patrón común detrás de todas estas vulnerabilidades

Si se observa con detenimiento, todas estas categorías comparten una raíz idéntica: **entrada de usuario que llega a un intérprete (SQL, shell del sistema operativo, motor de plantillas, intérprete HTML/JS del navegador) sin la validación, sanitización o parametrización adecuada**. Es la misma idea aplicada a contextos distintos:

| Contexto donde se interpreta la entrada | Vulnerabilidad resultante |
|---|---|
| Consulta SQL | Inyección SQL |
| Shell del sistema operativo | Inyección de comandos |
| Motor de plantillas del servidor | SSTI |
| DOM/JavaScript del navegador | XSS |
| Documento XML | XXE |
| Sistema de archivos | Path Traversal / LFI |

Interiorizar este patrón común es probablemente la lección conceptual más valiosa de todo el temario: una vez se entiende el principio (entrada no confiable → intérprete que la procesa como código/instrucción en lugar de como dato puro), reconocer una variante nueva en un contexto distinto se vuelve mucho más intuitivo.
