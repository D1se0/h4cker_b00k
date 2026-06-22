# Cabeceras HTTP

Las cabeceras (*headers*) son pares `nombre: valor` que viajan tanto en peticiones como en respuestas, transmitiendo metadatos sobre la comunicación: quién es el cliente, qué tipo de contenido se envía, cómo debe comportarse el navegador, qué políticas de seguridad aplican, etc.

Desde el punto de vista de un pentester, las cabeceras son una mina de información: revelan tecnologías usadas en el servidor, mecanismos de autenticación, políticas de seguridad (o su ausencia) y, en muchos casos, son directamente el vector de ataque (manipulación de `Host`, `X-Forwarded-For`, `Referer`, etc.).

Las cabeceras se agrupan habitualmente en cinco categorías.

## 1. Cabeceras generales

Aplican tanto a peticiones como a respuestas. Describen la comunicación en sí, no su contenido.

| Cabecera | Ejemplo | Descripción |
|---|---|---|
| `Date` | `Date: Mon, 21 Jun 2026 10:00:00 GMT` | Fecha y hora del mensaje, normalmente en UTC. |
| `Connection` | `Connection: keep-alive` | Indica si la conexión TCP debe mantenerse abierta (`keep-alive`) o cerrarse tras la respuesta (`close`). |

## 2. Cabeceras de entidad

Describen el **contenido** que se transfiere, ya sea en una petición (`POST`, `PUT`) o en una respuesta.

| Cabecera | Ejemplo | Descripción |
|---|---|---|
| `Content-Type` | `Content-Type: application/json; charset=UTF-8` | Indica el tipo MIME del cuerpo enviado o recibido. Es crítico para que el servidor sepa cómo interpretar los datos de una petición POST. |
| `Content-Length` | `Content-Length: 1245` | Tamaño en bytes del cuerpo del mensaje. |
| `Content-Encoding` | `Content-Encoding: gzip` | Indica si el cuerpo está comprimido y con qué algoritmo. |
| `Boundary` | dentro de `multipart/form-data` | Delimitador usado para separar las distintas partes de un formulario multipart (por ejemplo, al subir archivos). |

> **Por qué importa `Content-Type` para un pentester**: muchas validaciones del lado del servidor confían (erróneamente) en esta cabecera para decidir cómo procesar una entrada. En ataques de carga de archivos, por ejemplo, cambiar manualmente el `Content-Type` declarado puede ser suficiente para engañar a un filtro mal implementado que solo comprueba esta cabecera en lugar de inspeccionar el contenido real del archivo.

## 3. Cabeceras de petición

Las envía el cliente, aportan contexto sobre quién hace la petición.

| Cabecera | Ejemplo | Descripción |
|---|---|---|
| `Host` | `Host: app.ejemplo.com` | Indica a qué dominio/host va dirigida la petición. Esencial cuando un mismo servidor aloja varios sitios (*virtual hosting*) — manipularla puede revelar hosts internos no documentados. |
| `User-Agent` | `User-Agent: Mozilla/5.0 ...` | Identifica el cliente: navegador, sistema operativo, o herramienta (`curl/7.81.0`). Muchas aplicaciones bloquean herramientas de pentesting detectando este valor — cambiarlo es una técnica básica de evasión. |
| `Referer` | `Referer: https://google.com/` | Indica desde qué página se originó la petición. Es manipulable libremente por el cliente, así que **nunca debería usarse como mecanismo de control de acceso**. |
| `Accept` | `Accept: application/json` | Indica qué tipos de contenido puede interpretar el cliente. |
| `Cookie` | `Cookie: PHPSESSID=abc123` | Pares clave-valor que el navegador reenvía en cada petición para mantener estado (sesión, preferencias, tracking). |
| `Authorization` | `Authorization: Bearer eyJhbGc...` | Transporta credenciales o tokens (Basic, Bearer/JWT, etc.) para autenticar la petición. |

## 4. Cabeceras de respuesta

Las envía el servidor, aportan contexto adicional sobre la respuesta.

| Cabecera | Ejemplo | Descripción |
|---|---|---|
| `Server` | `Server: Apache/2.4.41 (Ubuntu)` | Revela el software (y a veces versión) del servidor web. Información valiosa para buscar CVEs conocidos. |
| `Set-Cookie` | `Set-Cookie: session=abc123; HttpOnly; Secure` | Establece una cookie en el navegador. Los atributos `HttpOnly` y `Secure` son relevantes en seguridad: el primero impide que JavaScript lea la cookie (mitigando robo vía XSS), el segundo obliga a que solo se envíe por HTTPS. |
| `WWW-Authenticate` | `WWW-Authenticate: Basic realm="Restricted"` | Indica qué esquema de autenticación espera el servidor cuando devuelve `401 Unauthorized`. |
| `Location` | `Location: /dashboard` | Usada junto a códigos `3xx` para indicar a dónde debe redirigirse el cliente. |

## 5. Cabeceras de seguridad

Un subconjunto especial de cabeceras de respuesta, pensadas para que el navegador aplique políticas de seguridad adicionales. Su **ausencia** suele ser en sí misma un hallazgo a reportar en una auditoría.

| Cabecera | Ejemplo | Descripción |
|---|---|---|
| `Content-Security-Policy` (CSP) | `Content-Security-Policy: script-src 'self'` | Define desde qué orígenes puede cargarse contenido activo (scripts, estilos, iframes). Una CSP bien configurada es una de las mitigaciones más efectivas contra XSS. |
| `Strict-Transport-Security` (HSTS) | `Strict-Transport-Security: max-age=31536000; includeSubDomains` | Obliga al navegador a comunicarse siempre por HTTPS con ese dominio, incluso si el usuario escribe `http://`. Mitiga ataques de degradación de protocolo. |
| `X-Content-Type-Options` | `X-Content-Type-Options: nosniff` | Impide que el navegador intente "adivinar" el tipo de contenido distinto al declarado en `Content-Type`, evitando ciertos vectores de XSS. |
| `X-Frame-Options` | `X-Frame-Options: DENY` | Evita que la página se cargue dentro de un `<iframe>`, mitigando ataques de *clickjacking*. |
| `Referrer-Policy` | `Referrer-Policy: no-referrer` | Controla cuánta información se filtra en la cabecera `Referer` al navegar fuera del sitio. |

## Trabajando con cabeceras desde `curl`

### Ver solo las cabeceras de respuesta

```bash
curl -I https://ejemplo.com
```

`-I` envía una petición `HEAD` (que por definición no devuelve cuerpo, solo cabeceras). Si en cambio queremos ver las cabeceras de respuesta de una petición que sí necesita cuerpo (como un `GET` normal), usamos `-i` (minúscula), que añade las cabeceras a la salida habitual sin cambiar el método.

### Enviar cabeceras personalizadas

```bash
curl -H "X-Custom-Header: valor" https://ejemplo.com
```

Se puede repetir `-H` tantas veces como cabeceras se necesiten enviar.

### Cambiar el User-Agent

Algunas cabeceras tienen su propio flag dedicado por lo habitual que es modificarlas:

```bash
curl -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" https://ejemplo.com
```

Esto es útil, por ejemplo, cuando una aplicación bloquea explícitamente clientes que se identifican como `curl` o como herramientas de escaneo automatizado.

## Inspección desde las DevTools del navegador

En la pestaña **Network**, al seleccionar cualquier petición, la sub-pestaña **Headers** muestra tanto las cabeceras de petición como las de respuesta, organizadas en secciones legibles. La mayoría de navegadores ofrece también una vista "Raw" que muestra el bloque de texto tal y como viajó por la red, útil cuando se necesita copiar la petición completa para reproducirla en otra herramienta (como un proxy de intercepción).
