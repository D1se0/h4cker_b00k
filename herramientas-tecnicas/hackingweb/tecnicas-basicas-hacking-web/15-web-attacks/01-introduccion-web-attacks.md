# Introducción a los ataques web

## Por qué las aplicaciones web son la superficie de ataque más relevante hoy

Las aplicaciones web no son solo los sitios públicos de cara al usuario final — incluyen también APIs externas, portales internos, paneles de administración, y cualquier interfaz accesible vía HTTP dentro de una organización. Comprometer una aplicación web externa puede ser el punto de entrada a la red interna completa; una aplicación interna mal protegida puede ser el pivote que un atacante con acceso parcial necesita para escalar.

## Las tres vulnerabilidades que cubre este bloque

### Manipulación de verbos HTTP (HTTP Verb Tampering)

Las configuraciones de autenticación y los filtros de seguridad de un servidor web muchas veces se aplican solo sobre determinados métodos HTTP (`GET`, `POST`), dejando otros verbos (`HEAD`, `PUT`, `DELETE`, `OPTIONS`) sin la misma protección. Enviar la misma petición con un verbo distinto al esperado puede eludir completamente un mecanismo de autenticación o un filtro de seguridad que solo comprueba ciertos métodos.

### IDOR (Insecure Direct Object Reference)

Ocurre cuando la aplicación expone referencias directas a objetos internos (IDs de usuario, nombres de archivo, números de registro) y **no verifica** que el usuario autenticado que hace la petición tenga realmente permiso sobre ese objeto concreto. Cambiar el identificador en la URL o en el cuerpo de la petición es suficiente para acceder a datos de otro usuario. Es, con diferencia, la vulnerabilidad más común en programas de *bug bounty*.

### XXE (XML External Entity Injection)

Cuando una aplicación procesa XML de entrada del usuario con un parser que tiene entidades externas habilitadas, un documento XML malicioso puede hacer que el servidor lea y devuelva archivos del sistema de ficheros local, o que realice peticiones de red no autorizadas — incluyendo hacia servicios internos no accesibles desde el exterior (el mismo tipo de impacto que SSRF, visto en el bloque de *Server-side Attacks*, pero a través del procesador XML en lugar de a través de una petición HTTP del servidor).

## El hilo conductor de los tres ataques

Los tres comparten la misma familia de causa raíz: **controles de seguridad que se aplican de forma incompleta o que confían en un supuesto que el atacante puede invalidar**. En manipulación de verbos, el supuesto es que el cliente usará los métodos que el frontend espera. En IDOR, el supuesto es que el cliente no intentará cambiar el identificador de otro usuario. En XXE, el supuesto es que el cliente enviará XML legítimo sin entidades externas. Los tres supuestos son desmontables con el mismo principio trabajado a lo largo de todo este temario: interactuar directamente con el backend, fuera de las restricciones que impone la interfaz visible.
