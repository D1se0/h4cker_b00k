# Web Requests — Fundamentos

Antes de poder atacar una aplicación web hace falta entender cómo conversan un navegador (o cualquier cliente) y un servidor. Todo lo que hacemos en pentesting web —desde mandar un payload de XSS hasta automatizar un fuzzing con miles de peticiones— se construye sobre el mismo bloque básico: una petición HTTP que sale y una respuesta HTTP que vuelve.

Este bloque cubre el protocolo HTTP y HTTPS, la anatomía de peticiones y respuestas, las cabeceras más relevantes para un pentester, los métodos y códigos de estado, y cómo se traduce todo esto al mundo real cuando una aplicación expone una API que sigue el patrón CRUD.

## Contenido

1. [El protocolo HTTP](01-protocolo-http.md)
2. [HTTPS y cifrado en tránsito](02-protocolo-https.md)
3. [Anatomía de peticiones y respuestas HTTP](03-peticiones-respuestas-http.md)
4. [Cabeceras HTTP](04-cabeceras-http.md)
5. [Métodos y códigos de estado HTTP](05-metodos-codigos-http.md)
6. [El método GET y autenticación básica](06-metodo-get.md)
7. [El método POST](07-metodo-post.md)
8. [APIs y el patrón CRUD](08-api-crud.md)

## Por qué importa

Un pentester web pasa la mayor parte del tiempo leyendo e interpretando tráfico HTTP: qué cabecera revela información, qué código de estado indica que algo se ha procesado de forma distinta a la esperada, qué método permite una acción que no debería estar permitida. Dominar este nivel "de bajo nivel" del protocolo es lo que después permite reconocer rápidamente vulnerabilidades en capas superiores (autenticación, control de acceso, inyección, etc.).
