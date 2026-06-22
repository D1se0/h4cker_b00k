# El método GET y autenticación HTTP básica

## GET en la práctica

`GET` es el método por defecto que usa cualquier navegador al visitar una URL, y el más usado para recuperar recursos: páginas, imágenes, resultados de búsqueda, etc. Su característica definitoria es que **los parámetros viajan en la propia URL**, dentro de la *query string* (`?param=valor&otro=valor2`).

Esto tiene implicaciones directas en seguridad:

- Los parámetros GET quedan **registrados en los logs del servidor**, en el historial del navegador y, potencialmente, en la cabecera `Referer` de la siguiente petición que se haga desde esa página. Por eso nunca deberían usarse para transmitir datos sensibles (contraseñas, tokens).
- Son fácilmente **manipulables y compartibles**: basta con cambiar un valor en la URL para alterar el comportamiento de la petición, lo que los convierte en el primer sitio donde se prueban inyecciones (SQLi, XSS reflejado, etc.).
- Son **idempotentes** por definición: una petición GET no debería tener efectos secundarios en el servidor (no debería, por ejemplo, borrar datos). Cuando una aplicación rompe esta convención —usando GET para acciones destructivas como `?action=delete&id=5`— se abre la puerta a ataques como CSRF mediante simples enlaces o imágenes.

## Autenticación HTTP básica

Antes de que los formularios de login con backend (PHP, Node, etc.) se popularizaran, era común proteger recursos mediante **HTTP Basic Authentication**, un mecanismo gestionado directamente por el servidor web (Apache, Nginx, IIS) a nivel de directorio o ruta, sin que la lógica de la aplicación intervenga.

### Cómo se reconoce

Cuando se intenta acceder a un recurso protegido sin credenciales, el servidor responde con:

```
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Basic realm="Restricted Content"
```

La presencia de `WWW-Authenticate: Basic` es la confirmación inequívoca de que ese recurso usa este esquema.

### Cómo funciona "por debajo"

El cliente debe enviar la cabecera `Authorization` con el esquema `Basic` seguido de las credenciales `usuario:contraseña` **codificadas en Base64** (no cifradas — Base64 es trivialmente reversible):

```
Authorization: Basic YWRtaW46YWRtaW4=
```

Donde `YWRtaW46YWRtaW4=` es el resultado de codificar `admin:admin` en Base64. Esto es importante: **Base64 no es cifrado**, es solo una codificación. Cualquiera que intercepte esa cabecera (por ejemplo, en una conexión HTTP sin TLS) puede decodificarla instantáneamente y obtener las credenciales en claro.

### Probarlo con `curl`

Hay tres formas equivalentes de autenticarse:

```bash
# 1. Usando el flag dedicado -u
curl -u admin:admin http://10.10.10.5/

# 2. Embebiendo las credenciales en la URL
curl http://admin:admin@10.10.10.5/

# 3. Construyendo manualmente la cabecera Authorization
curl -H 'Authorization: Basic YWRtaW46YWRtaW4=' http://10.10.10.5/
```

La tercera opción es especialmente útil cuando ya se dispone de una cabecera capturada (por ejemplo, de una sesión de proxy de intercepción) y se quiere reproducir exactamente esa autenticación sin volver a teclear usuario y contraseña.

> **Diferencia con JWT/Bearer**: en esquemas de autenticación más modernos, la cabecera `Authorization` usa el prefijo `Bearer` seguido de un token (típicamente un JWT), en lugar de `Basic` seguido de credenciales en Base64. La estructura de la cabecera es la misma, pero el significado y el formato del valor son distintos.

## Encontrando peticiones GET ocultas con las DevTools

Muchas aplicaciones cargan contenido dinámicamente vía JavaScript después de la carga inicial de la página (por ejemplo, una función de búsqueda que consulta `search.php?search=termino` en segundo plano). Estas peticiones no aparecen en el HTML fuente, pero sí en la pestaña **Network** de las DevTools mientras se interactúa con la página.

Flujo de trabajo típico:

1. Abrir DevTools (`F12`) y la pestaña **Network**.
2. Limpiar el historial de peticiones (icono de papelera) para evitar ruido.
3. Interactuar con la funcionalidad de interés (por ejemplo, escribir en un buscador).
4. Localizar la petición generada, inspeccionar su URL, parámetros y cabeceras.
5. Reproducirla directamente con `curl` o desde la consola JavaScript usando `fetch()` — la mayoría de navegadores permiten clic derecho sobre la petición → **Copy → Copy as cURL** o **Copy as fetch**, lo que genera automáticamente el comando equivalente.

### Por qué esto importa

Interactuar directamente con el endpoint subyacente (en lugar de pasar por la interfaz visual) suele ser mucho más rápido durante una auditoría, y además revela el comportamiento "real" del backend sin el filtrado o formateo que aplica el frontend. Es habitual, por ejemplo, descubrir que un endpoint backend devuelve más información en bruto (JSON completo) de la que finalmente se muestra renderizada en pantalla.
