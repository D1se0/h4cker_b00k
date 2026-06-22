# Anatomía de peticiones y respuestas HTTP

Toda comunicación HTTP se reduce a dos piezas: una **petición** que el cliente envía, y una **respuesta** que el servidor devuelve. Saber leer ambas con soltura —línea por línea— es la habilidad base de cualquier pentester web, porque cada línea puede aportar información o ser un punto de manipulación.

## La petición HTTP

Una petición HTTP típica tiene esta forma:

```
GET /users/login.html HTTP/1.1
Host: ejemplo.com
User-Agent: curl/7.81.0
Accept: */*

```

### La línea de petición

La primera línea siempre contiene tres campos separados por espacios:

| Campo | Ejemplo | Descripción |
|---|---|---|
| Método | `GET` | El verbo HTTP que indica la acción a realizar. |
| Ruta | `/users/login.html` | El recurso solicitado, puede incluir *query string*. |
| Versión | `HTTP/1.1` | La versión del protocolo usada. |

### Cabeceras

Después de la línea de petición vienen las cabeceras, una por línea, en formato `Nombre: valor`. Estas describen metadatos sobre el cliente y la petición: qué navegador se usa, qué cookies se envían, qué tipo de contenido se acepta, etc. La sección de cabeceras termina con una línea en blanco.

### Cuerpo (body)

Tras la línea en blanco, opcionalmente, puede venir el cuerpo de la petición: datos de un formulario, un JSON, un archivo subido, etc. Las peticiones `GET` normalmente no llevan cuerpo (los datos viajan en la *query string*), mientras que `POST`, `PUT` y `PATCH` sí suelen incluirlo.

> **Nota técnica**: HTTP/1.x transmite todo en texto plano, separando los campos mediante saltos de línea. HTTP/2 (y HTTP/3) cambian de paradigma y envían los datos en formato binario, multiplexado en un único flujo de conexión — más eficiente, pero ya no se puede "leer" directamente como texto plano sin que el cliente lo decodifique.

## La respuesta HTTP

Una respuesta típica:

```
HTTP/1.1 200 OK
Date: Mon, 21 Jun 2026 10:00:00 GMT
Server: Apache/2.4.41 (Ubuntu)
Content-Type: text/html; charset=UTF-8
Content-Length: 1256

<!DOCTYPE html>
<html>...
```

### La línea de estado

| Campo | Ejemplo | Descripción |
|---|---|---|
| Versión | `HTTP/1.1` | Versión del protocolo. |
| Código de estado | `200 OK` | Resultado del procesamiento de la petición (lo veremos en detalle más adelante). |

Después vienen las cabeceras de respuesta (información sobre el servidor, tipo de contenido, cookies que se establecen, etc.), seguidas de una línea en blanco y, finalmente, el cuerpo de la respuesta: normalmente HTML, pero también puede ser JSON, una imagen, un PDF o cualquier otro tipo de recurso.

## Inspeccionando peticiones completas con `curl`

Hasta ahora solo hemos visto el cuerpo de la respuesta al usar `curl`. Para ver la conversación completa —petición *y* respuesta, incluyendo cabeceras— usamos el flag `-v` (*verbose*):

```bash
curl -v http://ejemplo.com

* Trying 10.10.10.5:80...
* Connected to ejemplo.com (10.10.10.5) port 80
> GET / HTTP/1.1
> Host: ejemplo.com
> User-Agent: curl/7.81.0
> Accept: */*
>
< HTTP/1.1 401 Unauthorized
< Date: Mon, 21 Jun 2026 10:00:00 GMT
< Server: Apache/2.4.41 (Ubuntu)
< WWW-Authenticate: Basic realm="Restricted Content"
< Content-Length: 13
<
Access denied
```

El convenio de `curl` es muy claro de leer: las líneas que empiezan por `>` son lo que **enviamos** (la petición), y las que empiezan por `<` son lo que **recibimos** (la respuesta). Las líneas con `*` son información de depuración sobre la conexión (resolución, TCP, TLS, etc.), no forman parte del tráfico HTTP real.

En el ejemplo anterior, el servidor responde `401 Unauthorized` junto con una cabecera `WWW-Authenticate: Basic`, lo que indica que ese recurso está protegido mediante autenticación HTTP básica (lo veremos en detalle más adelante).

Para un nivel de detalle aún mayor, existe `-vvv`, que añade información adicional sobre el establecimiento de la conexión TCP/TLS.

## Inspeccionando peticiones con las DevTools del navegador

Los navegadores modernos incluyen herramientas de desarrollo (*DevTools*) que resultan imprescindibles en pentesting web, ya que permiten observar en tiempo real todo el tráfico que genera una página, sin necesidad de interceptar nada con un proxy externo.

Para abrirlas: `F12` o `Ctrl+Shift+I` (Windows/Linux) / `Cmd+Option+I` (macOS).

La pestaña más relevante para nosotros es **Network**: al recargar la página, se listan todas las peticiones realizadas (HTML, CSS, JS, imágenes, llamadas AJAX a APIs, etc.), junto con su método, código de estado, tamaño y tiempo de respuesta. Haciendo clic en cualquiera de ellas se puede ver el detalle completo: cabeceras de petición, cabeceras de respuesta, cuerpo enviado/recibido y, en muchos navegadores, una vista "Raw" que muestra el tráfico tal cual viajó por la red.

### Caso de uso típico

Imagina una aplicación que carga contenido de forma asíncrona tras el renderizado inicial de la página (por ejemplo, mediante JavaScript con `fetch()`). Si solo miramos el código fuente HTML (`Ctrl+U`), no veremos ese contenido porque se carga *después*, vía JavaScript. La pestaña Network sí captura esas peticiones adicionales, revelando endpoints, parámetros o incluso datos sensibles que no aparecen en el HTML estático. Esta técnica es habitual para descubrir endpoints de APIs internas que no están documentados ni enlazados desde ninguna parte visible de la interfaz.
