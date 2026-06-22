# El método POST

## Por qué existe POST si ya tenemos GET

`GET` coloca los datos en la URL, lo cual funciona bien para recuperar recursos, pero tiene tres limitaciones serias cuando lo que queremos es **enviar** datos al servidor (formularios, archivos, credenciales):

1. **Registro en logs**: los servidores web suelen registrar la URL completa de cada petición, incluida la *query string*. Enviar una contraseña por GET significa que quedará escrita en texto plano en los logs del servidor, en el historial del navegador, y posiblemente en cachés intermedias.
2. **Restricciones de codificación**: una URL solo admite un conjunto limitado de caracteres; cualquier dato binario o con caracteres especiales necesita ser codificado (*URL-encoding*), lo que añade complejidad y aumenta el tamaño efectivo de los datos transmitidos.
3. **Límite de tamaño**: las URLs tienen un límite práctico de longitud (~2000 caracteres, dependiendo del navegador y del servidor), insuficiente para enviar archivos o formularios extensos.

`POST` resuelve los tres problemas colocando los datos en el **cuerpo de la petición**, fuera de la URL, sin restricciones prácticas de tamaño y admitiendo datos binarios directamente.

## Formularios de login con POST

A diferencia de la autenticación HTTP básica (gestionada por el servidor web), la mayoría de aplicaciones modernas implementan su propia lógica de login mediante un formulario HTML que envía una petición `POST` a un script del backend (PHP, Node, Python, etc.), que valida las credenciales contra una base de datos.

### Anatomía de la petición

```
POST / HTTP/1.1
Host: 10.10.10.5
Content-Type: application/x-www-form-urlencoded
Content-Length: 30

username=admin&password=admin
```

Aquí el cuerpo sigue el formato `application/x-www-form-urlencoded`: pares `clave=valor` separados por `&`, igual que en una *query string*, pero ubicados en el cuerpo de la petición en lugar de en la URL.

### Reproduciendo el login con `curl`

```bash
curl -X POST -d 'username=admin&password=admin' http://10.10.10.5/
```

- `-X POST` fuerza el método (aunque al usar `-d`, `curl` ya asume POST por defecto si no se especifica otro método).
- `-d` envía los datos indicados en el cuerpo de la petición, con el `Content-Type` adecuado añadido automáticamente.

> **Siguiendo redirecciones**: muchos formularios de login redirigen al usuario a otra página tras autenticarse correctamente (`302 Found` → `/dashboard.php`). Por defecto, `curl` no sigue redirecciones automáticamente; para hacerlo hay que añadir `-L`.

## Cookies de sesión

Tras un login exitoso, el servidor habitualmente devuelve una cookie de sesión mediante la cabecera `Set-Cookie`, que el navegador almacenará y reenviará automáticamente en cada petición posterior, manteniendo así el estado "autenticado" sin tener que volver a enviar usuario y contraseña.

```bash
curl -X POST -d 'username=admin&password=admin' http://10.10.10.5/ -i

HTTP/1.1 200 OK
Set-Cookie: PHPSESSID=c1nsa6op7vtk7kdis7bcnbadf1; path=/
```

Para reutilizar esa cookie en peticiones posteriores con `curl`, existen dos formas equivalentes:

```bash
# Usando el flag dedicado -b
curl -b 'PHPSESSID=c1nsa6op7vtk7kdis7bcnbadf1' http://10.10.10.5/

# Construyendo manualmente la cabecera Cookie
curl -H 'Cookie: PHPSESSID=c1nsa6op7vtk7kdis7bcnbadf1' http://10.10.10.5/
```

### Por qué esto es relevante en seguridad

Que una simple cookie sea suficiente para mantener una sesión autenticada es exactamente lo que hace posible (y peligroso) el robo de sesión: si un atacante consigue copiar el valor de esa cookie —por ejemplo, mediante un ataque XSS que ejecute `document.cookie` y exfiltre el valor— puede suplantar completamente a la víctima sin necesitar nunca su usuario y contraseña. Esto se conoce como **session hijacking**, y lo veremos en detalle en el bloque dedicado a XSS.

Inspeccionar y manipular cookies manualmente desde las DevTools del navegador (pestaña **Application** o **Storage**, según el navegador) es una técnica básica para reproducir este tipo de escenarios durante una auditoría: se puede borrar, copiar o sustituir el valor de una cookie para comprobar si sigue siendo válida, si caduca correctamente, o si es predecible.

## POST con cuerpo JSON

No todas las peticiones POST usan `application/x-www-form-urlencoded`. Las aplicaciones modernas que se comunican mediante JavaScript (AJAX/`fetch`) suelen enviar el cuerpo como JSON:

```
POST /search.php HTTP/1.1
Content-Type: application/json
Cookie: PHPSESSID=c1nsa6op7vtk7kdis7bcnbadf1

{"search":"london"}
```

Para replicar esto con `curl` es imprescindible declarar explícitamente el `Content-Type`, ya que de lo contrario `curl` enviará el cuerpo como `application/x-www-form-urlencoded` por defecto, y el backend podría no interpretarlo correctamente (o, peor aún, comportarse de forma distinta de lo esperado):

```bash
curl -X POST \
  -d '{"search":"london"}' \
  -H 'Content-Type: application/json' \
  -b 'PHPSESSID=c1nsa6op7vtk7kdis7bcnbadf1' \
  http://10.10.10.5/search.php
```

### Por qué interactuar directamente con el endpoint es tan valioso

Una vez identificado el endpoint real al que apunta una funcionalidad (en este caso `search.php`), podemos interactuar con él directamente, sin pasar por la interfaz gráfica de la aplicación. Esto acelera enormemente las pruebas: en lugar de hacer clic, escribir y esperar a que la página renderice cada vez, se puede iterar sobre decenas o cientos de payloads distintos en segundos mediante un simple bucle en `curl` o un script.

Esta capacidad de "saltarse" el frontend y hablar directamente con el backend es una de las habilidades fundamentales en pentesting web y en programas de *bug bounty*, donde la velocidad de iteración marca la diferencia entre encontrar o no una vulnerabilidad explotable.
