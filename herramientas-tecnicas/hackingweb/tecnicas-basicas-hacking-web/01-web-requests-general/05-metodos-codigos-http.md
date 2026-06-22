# Métodos y códigos de estado HTTP

## Métodos HTTP

El método (o "verbo") HTTP indica al servidor qué tipo de acción se quiere realizar sobre un recurso. Es el primer campo de la línea de petición (`GET / HTTP/1.1`), y en las DevTools del navegador aparece en la columna **Method** de la pestaña Network.

| Método | Descripción | Relevancia en pentesting |
|---|---|---|
| `GET` | Solicita un recurso. Los datos adicionales se pasan por *query string*. | Vector clásico para inyecciones reflejadas en parámetros visibles en la URL. |
| `POST` | Envía datos al servidor (formularios, JSON, archivos) en el cuerpo de la petición. | Usado para login, formularios, subida de archivos — superficie habitual de inyección, IDOR, CSRF. |
| `HEAD` | Igual que `GET` pero sin cuerpo de respuesta; solo cabeceras. | Útil para comprobar el tamaño/tipo de un recurso sin descargarlo, o para sondear la existencia de rutas sin generar tráfico pesado. |
| `PUT` | Crea o reemplaza un recurso en el servidor. | Si está mal restringido, permite subir/sobrescribir archivos arbitrarios. |
| `DELETE` | Elimina un recurso. | Si no está protegido, puede usarse para denegación de servicio borrando datos críticos. |
| `OPTIONS` | Devuelve qué métodos acepta el servidor para un recurso dado. | Técnica de reconocimiento: revela qué verbos están habilitados, a veces incluyendo métodos peligrosos olvidados (`PUT`, `DELETE`, `TRACE`). |
| `PATCH` | Aplica una modificación *parcial* a un recurso existente. | Frecuente en APIs REST, junto a `PUT`. |

> **Nota**: la mayoría de aplicaciones web "tradicionales" basadas en formularios solo usan `GET` y `POST`. Las APIs REST, en cambio, suelen aprovechar todo el abanico (`GET`/`POST`/`PUT`/`DELETE`/`PATCH`) para representar operaciones CRUD de forma semántica, como veremos en el último apartado de este bloque.

La existencia de un método concreto en una ruta dada no depende del protocolo en sí, sino de cómo esté configurado el servidor o la aplicación. Por eso comprobar qué métodos responde realmente cada endpoint —más allá del que usa la interfaz web normalmente— es una técnica de reconocimiento valiosa (lo veremos en profundidad en el bloque de *Web Attacks*, en el apartado de manipulación de verbos HTTP).

## Códigos de estado HTTP

El código de estado es el segundo campo de la línea de estado en la respuesta (`HTTP/1.1 200 OK`) e informa sobre el resultado del procesamiento de la petición. Se agrupan en cinco clases según su primer dígito:

| Clase | Significado |
|---|---|
| `1xx` | Informativo. La petición se está procesando, no afecta al resultado final. |
| `2xx` | Éxito. La petición se procesó correctamente. |
| `3xx` | Redirección. El cliente debe realizar otra acción (normalmente, ir a otra URL) para completar la petición. |
| `4xx` | Error del cliente. La petición está mal formada, no autorizada, o el recurso no existe. |
| `5xx` | Error del servidor. Algo falló al procesar una petición que, en principio, era válida. |

### Códigos más relevantes en el día a día de un pentester

| Código | Significado | Por qué importa |
|---|---|---|
| `200 OK` | Petición exitosa. | Confirma que el recurso existe y es accesible. |
| `301 / 302` | Redirección permanente / temporal. | Útil para rastrear cadenas de redirección, detectar migraciones HTTP→HTTPS, o *open redirects* mal validados. |
| `400 Bad Request` | La petición está mal formada. | Puede indicar que un payload ha roto la sintaxis esperada por el servidor (señal útil al fuzzear). |
| `401 Unauthorized` | Falta autenticación o es inválida. | Indica un recurso protegido — candidato a pruebas de fuerza bruta o bypass de autenticación. |
| `403 Forbidden` | El cliente no tiene permisos, aunque esté autenticado. | Puede señalar un control de acceso roto (IDOR) si cambiando un parámetro pasamos de `403` a `200`. |
| `404 Not Found` | El recurso no existe. | La respuesta base para comparar durante fuzzing de directorios — cualquier código distinto de `404` en una ruta probada suele ser interesante. |
| `500 Internal Server Error` | Fallo no controlado del servidor. | Señal clásica de que un payload (SQLi, por ejemplo) ha provocado un comportamiento inesperado en el backend. |

### Por qué los códigos de estado son una herramienta de detección

Más allá de su función "normal", los códigos de estado son una de las señales más fiables a la hora de automatizar pruebas: cuando se hace *fuzzing* de directorios, parámetros o payloads, comparar el código de estado devuelto frente a una petición "limpia" de control permite distinguir respuestas legítimas de errores, sin tener que analizar el contenido completo de cada respuesta. Por ejemplo, si todas las rutas inexistentes devuelven `404` salvo una que devuelve `200` o `403`, esa ruta merece investigación inmediata.

## Comprobando métodos y códigos con `curl`

```bash
# Ver el método y código en una petición verbose
curl -v -X OPTIONS http://ejemplo.com/api/usuarios

# Probar un método distinto al habitual
curl -X PUT http://ejemplo.com/recurso -d "datos"

# Comprobar solo el código de estado, sin descargar el cuerpo
curl -o /dev/null -s -w "%{http_code}\n" http://ejemplo.com/admin
```

Este último comando es especialmente útil al automatizar comprobaciones masivas: descarta el cuerpo de la respuesta (`-o /dev/null`), silencia la salida de progreso (`-s`) e imprime únicamente el código HTTP (`-w "%{http_code}"`), lo que permite construir scripts rápidos de reconocimiento.
