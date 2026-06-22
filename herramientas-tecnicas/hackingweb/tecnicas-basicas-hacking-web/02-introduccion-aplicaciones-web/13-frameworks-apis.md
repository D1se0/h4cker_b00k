# Frameworks de desarrollo y APIs (REST vs SOAP)

## Frameworks de desarrollo

Construir una aplicación web compleja completamente desde cero es ineficiente: la mayoría de aplicaciones comparten funcionalidad común (registro de usuarios, autenticación, gestión de sesiones, conexión a base de datos). Los frameworks de desarrollo encapsulan estas funcionalidades habituales, acelerando el desarrollo y estandarizando patrones.

| Framework | Lenguaje | Usado por |
|---|---|---|
| **Laravel** | PHP | Startups y empresas pequeñas/medianas, por su curva de aprendizaje accesible |
| **Express** | Node.js | PayPal, Yahoo, Uber, IBM |
| **Django** | Python | Google, YouTube, Instagram, Mozilla, Pinterest |
| **Rails** | Ruby | GitHub, Hulu, Twitch, Airbnb |

### Relevancia ofensiva

Cada framework tiene sus propios patrones de vulnerabilidad conocidos: deserialización insegura en ciertos frameworks Ruby, SSTI (*Server-Side Template Injection*, que veremos en el bloque de *Server-side Attacks*) en motores de plantillas asociados a Django o Express, exposición de modos de depuración (`DEBUG=True` en Django, por ejemplo) que filtran trazas de error con información extremadamente sensible. Identificar el framework mediante cabeceras, cookies con nombres característicos (`laravel_session`, `connect.sid`), o mensajes de error específicos es un paso de reconocimiento habitual.

## APIs web

Una API es la interfaz que permite a un componente (el frontend, u otra aplicación externa) interactuar con la funcionalidad de otro (el backend) sin necesidad de conocer su implementación interna. En el contexto web, normalmente se accede vía HTTP, y el servidor web se encarga de enrutar y procesar esas peticiones.

### Parámetros de consulta como forma básica de API

El método más sencillo para enviar argumentos a una página es mediante parámetros `GET` o `POST`, como vimos en el bloque de *Web Requests*. Por ejemplo, `/search.php?item=manzanas` indica al script `search.php` qué término buscar.

## SOAP

**SOAP** (*Simple Object Access Protocol*) intercambia datos mediante mensajes XML estructurados, tanto en la petición como en la respuesta:

```xml
<?xml version="1.0"?>
<soap:Envelope
  xmlns:soap="http://www.example.com/soap/soap/"
  soap:encodingStyle="http://www.w3.org/soap/soap-encoding">
  <soap:Header></soap:Header>
  <soap:Body>
    <soap:Fault></soap:Fault>
  </soap:Body>
</soap:Envelope>
```

Es especialmente adecuado para transferir datos estructurados complejos u objetos con estado, pero suele resultar verboso incluso para operaciones sencillas, lo que ha favorecido la popularidad de alternativas más ligeras como REST.

> **Relevancia ofensiva**: las APIs SOAP, al estar construidas sobre XML, son susceptibles a ataques específicos de ese formato — en particular **XXE (XML External Entity)**, que veremos en detalle en el bloque de *Web Attacks*. Cualquier endpoint que acepte y procese XML merece comprobarse específicamente frente a este vector.

## REST

**REST** (*Representational State Transfer*) estructura los datos a través de la propia ruta de la URL (`/search/users/1`) y, normalmente, devuelve la respuesta en formato JSON. A diferencia de SOAP, REST aprovecha directamente la semántica de los métodos HTTP:

| Método | Operación |
|---|---|
| `GET` | Recuperar datos |
| `POST` | Crear datos (no idempotente) |
| `PUT` | Crear o reemplazar datos existentes (idempotente) |
| `DELETE` | Eliminar datos |

Este es exactamente el patrón CRUD que se vio en detalle en el bloque de *Web Requests*. La popularidad de REST se debe en buena parte a su simplicidad: una URL clara, un método HTTP semánticamente correcto, y una respuesta JSON ligera y fácil de consumir desde cualquier cliente (navegador, app móvil, otro servicio backend).

### Relevancia ofensiva

Las APIs REST son el terreno de juego de vulnerabilidades específicas que se tratan en el bloque dedicado *API Attacks*: autorización rota a nivel de objeto (BOLA/IDOR), autenticación defectuosa, exposición excesiva de datos (devolver más campos de los necesarios en la respuesta JSON), y falta de límites de tasa que habilitan fuerza bruta o abuso de recursos. La naturaleza "modular" de REST —donde cada recurso suele tener su propio conjunto de endpoints CRUD— también amplía la superficie de ataque: cada endpoint individual necesita sus propios controles de autenticación y autorización, y es habitual que alguno se quede mal protegido por simple descuido al escalar la aplicación.

## Documentación de APIs y reconocimiento

Muchas APIs REST modernas se documentan mediante estándares como **OpenAPI/Swagger**, a menudo accesibles en rutas predecibles (`/swagger.json`, `/api-docs`, `/openapi.yaml`). Encontrar esta documentación —intencionalmente expuesta o dejada accesible por error— acelera enormemente el reconocimiento de una API, revelando de un vistazo todos los endpoints, parámetros esperados y modelos de datos, sin necesidad de inferirlos mediante fuzzing manual.
