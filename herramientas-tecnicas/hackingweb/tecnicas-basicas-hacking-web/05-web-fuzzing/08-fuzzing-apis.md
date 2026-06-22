# Fuzzing de APIs web

## En qué se diferencia una API de un servidor web tradicional

| Aspecto | Servidor web tradicional | API |
|---|---|---|
| Propósito | Servir HTML/CSS/JS para humanos | Permitir que aplicaciones se comuniquen entre sí |
| Formato de datos | HTML principalmente | JSON, XML, según la API |
| Interacción | Usuario vía navegador | Otra aplicación, en nombre del usuario |
| Acceso | Generalmente público | Público, privado o de socios |

Esta diferencia condiciona la estrategia: en lugar de buscar directorios y páginas, el fuzzing de APIs se centra en **endpoints**, sus **parámetros**, y los **formatos de datos** que intercambian.

## Los tres estilos principales de API

### REST

Recursos identificados por URLs (`/users/123`), usando métodos HTTP semánticamente (`GET`/`POST`/`PUT`/`DELETE` — el mismo patrón CRUD visto en el bloque de *Web Requests*). Parámetros en *query string*, en la ruta, o en el cuerpo de la petición.

### SOAP

Un único endpoint que recibe mensajes XML estructurados según un archivo **WSDL** (*Web Services Description Language*), que describe operaciones, parámetros de entrada/salida y tipos de datos disponibles.

### GraphQL

Un único endpoint (típicamente `/graphql`) que acepta **consultas** (lectura) y **mutaciones** (escritura), permitiendo al cliente especificar exactamente qué campos necesita en una sola petición — evitando la sobre/infra-carga de datos típica de REST.

```graphql
query {
  user(id: 123) {
    name
    email
    posts(limit: 5) { title body }
  }
}
```

## Cómo descubrir endpoints y parámetros

| Método | Aplicable a |
|---|---|
| **Documentación oficial** (Swagger/OpenAPI, WSDL) | REST, SOAP |
| **Introspección** (consulta especial que revela el esquema completo) | GraphQL |
| **Análisis de tráfico de red** (proxy de intercepción) | Todos |
| **Fuzzing de nombres de parámetro/endpoint** | Todos, especialmente útil sin documentación |

> El bloque de *Attacking GraphQL* profundiza en la introspección y sus implicaciones de seguridad; el de *API Attacks* cubre en detalle la explotación de vulnerabilidades específicas de REST.

## Documentación como punto de partida

Cuando existe documentación autogenerada (Swagger UI en `/docs`, por ejemplo), es el primer lugar a revisar: lista explícitamente los endpoints disponibles, sus métodos y parámetros esperados — información gratuita que ahorra una cantidad enorme de fuzzing exploratorio.

```
GET    /              → Leer raíz
GET    /items/{id}    → Leer un elemento
DELETE /items/{id}    → Eliminar un elemento
PUT    /items/{id}    → Actualizar un elemento
POST   /items/        → Crear/actualizar un elemento
```

**Pero la documentación pública casi nunca cuenta toda la historia.** Es habitual que existan endpoints **no documentados deliberadamente** — funciones internas, código en desarrollo no listo para uso externo, o simplemente "seguridad por oscuridad" mal entendida.

## Fuzzing de endpoints no documentados

```bash
git clone https://github.com/PandaSt0rm/webfuzz_api.git
cd webfuzz_api
pip3 install -r requirements.txt
python3 api_fuzzer.py http://10.10.10.5:8000
```

```
Found valid endpoints:
- http://10.10.10.5:8000/internal_endpoint
- http://10.10.10.5:8000/docs
Unusual status codes:
405: http://10.10.10.5:8000/items
```

Tres señales relevantes en esta salida:

- Un endpoint **no documentado** aparece junto al documentado (`/docs`) — directamente accesible aunque nunca apareciera en la especificación Swagger.
- Un código **`405 Method Not Allowed`** en `/items` sugiere que el endpoint existe, pero se está usando el verbo HTTP incorrecto — invitando a probar otros métodos (`POST`, `PUT`) sobre esa misma ruta.

## Tipos de fuzzing específicos de API

| Tipo | En qué consiste | Vulnerabilidades que puede revelar |
|---|---|---|
| **Parameter Fuzzing** | Variar valores de query params, cabeceras y cuerpo | Inyección SQL/comandos, XSS, manipulación de parámetros |
| **Data Format Fuzzing** | Manipular estructura/codificación de JSON/XML | Errores de parseo, desbordamientos, manejo incorrecto de caracteres especiales |
| **Sequence Fuzzing** | Variar orden y timing de llamadas encadenadas | Condiciones de carrera, IDOR, *bypass* de autorización |

## Por qué fuzzear parámetros de API es especialmente valioso

Manipular sistemáticamente los valores que acepta un endpoint puede exponer directamente algunas de las vulnerabilidades más críticas en aplicaciones modernas:

- **Broken Object-Level Authorization (BOLA/IDOR)**: cambiar un identificador de objeto en la petición revela que se puede acceder a recursos de otro usuario sin autorización.
- **Broken Function-Level Authorization**: invocar una función que debería estar restringida a un rol superior, simplemente porque el backend no comprueba realmente el rol antes de procesar la petición.
- **Server-Side Request Forgery (SSRF)**: inyectar una URL o referencia maliciosa en un parámetro que el servidor usa internamente para realizar una petición saliente.

Estas tres categorías se desarrollan en profundidad en el bloque de *API Attacks*, que retoma exactamente este punto: una vez localizados los endpoints y parámetros mediante fuzzing, el siguiente paso es la explotación dirigida de cada uno de ellos.
