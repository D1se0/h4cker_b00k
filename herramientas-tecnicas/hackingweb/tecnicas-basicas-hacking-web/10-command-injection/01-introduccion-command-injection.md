# Introducción a las inyecciones de comandos

## Por qué es una de las vulnerabilidades más críticas

Una inyección de comandos del sistema operativo permite ejecutar instrucciones arbitrarias **directamente en el servidor backend** — no en una base de datos, no en el navegador de otro usuario, sino en el propio sistema operativo que aloja la aplicación. El salto de gravedad respecto a otras inyecciones es inmediato: un compromiso exitoso puede significar control total del servidor y, desde ahí, una vía de entrada hacia el resto de la red interna.

## El patrón común: inyecciones en general

Las vulnerabilidades de inyección ocupan un lugar destacado en el [Top 10 de OWASP](https://owasp.org/www-project-top-ten/) por su combinación de alto impacto y alta frecuencia. El patrón de fondo es siempre el mismo, visto ya repetidamente en este temario: entrada controlada por el usuario que se interpreta erróneamente como parte de una instrucción ejecutable, en lugar de como dato puro.

| Tipo de inyección | Dónde se interpreta la entrada como código |
|---|---|
| Inyección de comandos del SO | Una función que ejecuta comandos del sistema operativo |
| Inyección SQL | Una consulta a la base de datos |
| XSS / Inyección HTML | El motor de renderizado del navegador |
| Inyección de código | Una función que evalúa código (`eval()` y similares) |

Existen muchas otras variantes (LDAP, NoSQL, cabeceras HTTP, XPath, IMAP, ORM...) — cualquier contexto donde entrada no confiable llegue a un intérprete sin la separación adecuada entre "dato" e "instrucción" es, potencialmente, un nuevo tipo de inyección.

## Cómo aparece en código real

Cualquier lenguaje de programación web ofrece funciones para ejecutar comandos del sistema operativo cuando la aplicación lo necesita (instalar un plugin, procesar un archivo, ejecutar una utilidad externa).

### PHP

```php
<?php
if (isset($_GET['filename'])) {
    system("touch /tmp/" . $_GET['filename'] . ".pdf");
}
?>
```

Funciones equivalentes en PHP: `exec()`, `system()`, `shell_exec()`, `passthru()`, `popen()` — cada una con matices sobre qué devuelven y cómo gestionan la salida, pero todas igualmente vulnerables si reciben entrada sin sanitizar.

### Node.js

```js
app.get("/createfile", function(req, res) {
    child_process.exec(`touch /tmp/${req.query.filename}.txt`);
});
```

`child_process.exec()` y `child_process.spawn()` cumplen el mismo papel en el ecosistema Node.js.

En ambos ejemplos, el parámetro `filename` se concatena directamente dentro del comando que se ejecutará, sin ninguna validación ni escape previo — exactamente el mismo patrón de causa raíz visto en SQL Injection, aplicado ahora a un intérprete distinto: la shell del sistema operativo en lugar del motor de base de datos.

## No es exclusivo de aplicaciones web

Cualquier programa —un binario de escritorio, un script de automatización, un cliente de red— que reciba entrada de usuario y la use para construir un comando del sistema sin la sanitización adecuada es vulnerable exactamente al mismo tipo de ataque, con las mismas técnicas de explotación que se desarrollan en el resto de este bloque.

## Qué viene a continuación

Los siguientes apartados recorren el proceso completo: cómo detectar que una funcionalidad concreta está ejecutando comandos del sistema, qué operadores permiten "inyectar" un comando adicional al previsto, cómo sortear filtros y listas negras cuando la aplicación intenta (parcialmente) protegerse, y finalmente cómo prevenir esta clase de vulnerabilidad desde el diseño.
