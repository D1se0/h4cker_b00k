# APIs y el patrón CRUD

## De parámetros sueltos a una API estructurada

En los apartados anteriores vimos cómo una aplicación puede exponer una funcionalidad de búsqueda mediante un script (`search.php`) que recibe un parámetro y devuelve resultados. Una **API** (*Application Programming Interface*) lleva esta idea un paso más allá: en lugar de un único endpoint con lógica ad-hoc, expone una interfaz estructurada y predecible para interactuar con los datos de la aplicación, normalmente organizada en torno a "recursos" (tablas, entidades) y operaciones bien definidas sobre ellos.

Un ejemplo de URL típica de una API orientada a recursos:

```
PUT /api.php/city/london
```

Aquí `city` identifica el recurso (una tabla, conceptualmente) y `london` identifica la entrada concreta sobre la que se quiere operar. El método HTTP utilizado determina qué operación se realiza.

## El patrón CRUD

La inmensa mayoría de APIs que interactúan con una base de datos giran en torno a cuatro operaciones fundamentales, conocidas por el acrónimo **CRUD**:

| Operación | Método HTTP | Qué hace |
|---|---|---|
| **C**reate | `POST` | Añade una nueva entrada al recurso. |
| **R**ead | `GET` | Consulta una o varias entradas existentes. |
| **U**pdate | `PUT` / `PATCH` | Modifica una entrada existente. |
| **D**elete | `DELETE` | Elimina una entrada existente. |

Este mapeo entre operación lógica y método HTTP es la base de las **APIs REST**, el estilo arquitectónico más extendido en la web actual, aunque el mismo principio aparece —con variaciones— en otros estilos de API.

> **`PUT` vs `PATCH`**: ambos se usan para actualizar, pero con matices. `PUT` se entiende habitualmente como reemplazo completo del recurso (hay que enviar todos los campos, incluso los que no cambian), mientras que `PATCH` se usa para una actualización parcial (solo se envían los campos que se quieren modificar). En la práctica, muchas APIs son flexibles con esta distinción, y conviene comprobar con `OPTIONS` qué métodos acepta realmente un endpoint concreto antes de asumir su comportamiento.

## Read: consultando datos

```bash
curl http://10.10.10.5/api.php/city/london
[{"city_name":"London","country_name":"UK"}]
```

Para formatear la salida JSON de forma legible, es habitual canalizarla a `jq`:

```bash
curl -s http://10.10.10.5/api.php/city/london | jq
```

Muchas APIs permiten búsquedas parciales (devolviendo todas las coincidencias de un término) o incluso devolver el listado completo si se envía un parámetro vacío:

```bash
curl -s http://10.10.10.5/api.php/city/ | jq    # todas las entradas
curl -s http://10.10.10.5/api.php/city/le | jq  # coincidencias parciales con "le"
```

## Create: añadiendo datos

```bash
curl -X POST \
  -d '{"city_name":"NuevaCiudad", "country_name":"ES"}' \
  -H 'Content-Type: application/json' \
  http://10.10.10.5/api.php/city/
```

## Update: modificando datos existentes

```bash
curl -X PUT \
  -d '{"city_name":"CiudadRenombrada", "country_name":"ES"}' \
  -H 'Content-Type: application/json' \
  http://10.10.10.5/api.php/city/london
```

> **Nota**: en algunas implementaciones de API, una operación de `Update` sobre un recurso que **no existe** puede acabar creándolo igualmente (comportamiento conocido como *upsert*). Esto no es universal: depende completamente de cómo esté programado el backend, y conviene comprobarlo explícitamente durante una auditoría, ya que puede revelar comportamientos no documentados.

## Delete: eliminando datos

```bash
curl -X DELETE http://10.10.10.5/api.php/city/CiudadRenombrada
```

## Por qué esto importa para un pentester: control de acceso roto en APIs

En una aplicación bien diseñada, estas cuatro operaciones no están disponibles para cualquier usuario sin restricción: normalmente se exige autenticación (cookie de sesión, token Bearer/JWT) y, además, autorización (que el usuario autenticado tenga permiso para *esa* operación concreta sobre *ese* recurso concreto).

Cuando una API no implementa correctamente estos controles, aparecen vulnerabilidades muy serias:

- **Falta de autenticación**: cualquiera puede leer, crear, modificar o borrar datos sin necesidad de iniciar sesión.
- **Autorización rota a nivel de operación**: un usuario autenticado con permisos de solo lectura consigue ejecutar operaciones de escritura (`POST`/`PUT`/`DELETE`) porque el backend no comprueba el rol del usuario antes de procesar la petición — solo comprueba que esté autenticado.
- **IDOR (Insecure Direct Object Reference)**: un usuario autenticado puede acceder o modificar recursos que pertenecen a otro usuario simplemente cambiando un identificador en la URL (por ejemplo, pasar de `/api/orders/105` —su propio pedido— a `/api/orders/106` —el pedido de otra persona—), porque el backend no verifica la propiedad del recurso. Este caso se trata en detalle en el bloque de *Web Attacks*.

Probar sistemáticamente las cuatro operaciones CRUD sobre cada endpoint detectado —incluso aquellos para los que la interfaz visual solo expone lectura— es una técnica de reconocimiento fundamental: muchas veces el frontend oculta botones de "editar" o "borrar" para ciertos roles, pero el endpoint backend sigue aceptando esas operaciones sin comprobar realmente quién las solicita.

### Checklist práctico al auditar una API CRUD

- [ ] ¿Qué ocurre si llamo al endpoint con `GET` sin estar autenticado?
- [ ] ¿El método `OPTIONS` revela verbos habilitados que no usa la interfaz visual?
- [ ] ¿Puedo crear (`POST`) o modificar (`PUT`/`PATCH`) recursos con un usuario de bajo privilegio?
- [ ] ¿Puedo leer o modificar el recurso de **otro** usuario cambiando solo el identificador?
- [ ] ¿El `DELETE` está protegido frente a abuso (por ejemplo, frente a un usuario que intenta borrar recursos en masa)?
