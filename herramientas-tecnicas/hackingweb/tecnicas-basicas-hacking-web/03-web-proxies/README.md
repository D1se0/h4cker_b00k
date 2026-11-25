# Uso de Proxies Web

Un proxy web de intercepción (Burp Suite, OWASP ZAP) es probablemente la herramienta individual más usada en cualquier auditoría de aplicaciones web. Se sitúa entre el navegador y el servidor, permitiendo ver, pausar, modificar y reenviar cada petición y respuesta HTTP. Este bloque cubre cómo configurar y sacar partido a estas herramientas: interceptación, modificación automática, repetición de peticiones, codificación/decodificación, fuzzing integrado y escaneo de vulnerabilidades.

## Contenido

1. [Qué son los proxies web y herramientas disponibles](01-introduccion-proxies.md)
2. [Configuración del proxy y certificados](02-configuracion-proxy.md)
3. [Interceptación de peticiones](03-interceptacion-peticiones.md)
4. [Interceptación de respuestas](04-interceptacion-respuestas.md)
5. [Modificación automática (Match & Replace)](05-modificacion-automatica.md)
6. [Repetición de peticiones (Repeater)](06-repeticion-peticiones.md)
7. [Codificación y decodificación](07-codificacion-decodificacion.md)
8. [Proxificando otras herramientas](08-proxy-otras-herramientas.md)
9. [Fuzzing integrado: Burp Intruder y ZAP Fuzzer](09-fuzzing-integrado.md)
10. [Escaneo de vulnerabilidades: Burp Scanner y ZAP Scanner](10-escaneres-web.md)

## Por qué este bloque importa

Cualquier técnica ofensiva que se estudie más adelante —inyecciones, manipulación de autenticación, IDOR, XSS— se ejecuta y depura en la práctica a través de un proxy de intercepción. Dominar Burp/ZAP desde el principio acelera enormemente el aprendizaje de todo lo que viene después.
