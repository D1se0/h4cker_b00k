---
icon: notebook
---

# Chuleta rápida de CWEs

Referencia rápida de los CWE (Common Weakness Enumeration) que más aparecen en bug bounty de aplicaciones web/móviles/API.

| CWE          | Nombre                                                       | Resumen                                                                                    |
| ------------ | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| **CWE-79**   | Cross-Site Scripting (XSS)                                   | Inyección de código/script que se ejecuta en el navegador de otro usuario.                 |
| **CWE-89**   | SQL Injection                                                | Inyección de consultas SQL no intencionadas a través de entradas no saneadas.              |
| **CWE-798**  | Use of Hard-coded Credentials                                | Credenciales (contraseñas, tokens, claves) escritas directamente en código/binario.        |
| **CWE-639**  | Authorization Bypass Through User-Controlled Key (IDOR/BOLA) | El sistema confía en un identificador que envía el cliente sin comprobar que le pertenece. |
| **CWE-285**  | Improper Authorization                                       | Fallo genérico de comprobación de permisos.                                                |
| **CWE-287**  | Improper Authentication                                      | Fallos en cómo el sistema verifica la identidad.                                           |
| **CWE-306**  | Missing Authentication for Critical Function                 | Una función sensible no exige autenticación en absoluto.                                   |
| **CWE-521**  | Weak Password Requirements                                   | Políticas de contraseña débiles (longitud, complejidad, valores por defecto).              |
| **CWE-352**  | Cross-Site Request Forgery (CSRF)                            | Forzar a la víctima a ejecutar una acción no deseada estando autenticada.                  |
| **CWE-918**  | Server-Side Request Forgery (SSRF)                           | El servidor hace peticiones a destinos controlados por el atacante.                        |
| **CWE-22**   | Path Traversal                                               | Acceso a archivos/directorios fuera del directorio previsto (`../../etc/passwd`).          |
| **CWE-434**  | Unrestricted File Upload                                     | Subida de archivos sin validar tipo/contenido, permitiendo subir ficheros peligrosos.      |
| **CWE-611**  | XML External Entity (XXE)                                    | Procesamiento inseguro de XML que permite leer archivos o hacer SSRF.                      |
| **CWE-502**  | Deserialization of Untrusted Data                            | Deserializar datos no confiables puede llevar a ejecución de código.                       |
| **CWE-200**  | Information Exposure                                         | Exposición de información que no debería ser accesible.                                    |
| **CWE-209**  | Information Exposure Through an Error Message                | Mensajes de error que revelan detalles internos (stack traces, rutas, queries).            |
| **CWE-307**  | Improper Restriction of Excessive Authentication Attempts    | Falta de límite de intentos (fuerza bruta posible).                                        |
| **CWE-384**  | Session Fixation                                             | El atacante puede fijar el identificador de sesión de la víctima.                          |
| **CWE-601**  | Open Redirect                                                | Redirecciones no validadas usadas para phishing.                                           |
| **CWE-732**  | Incorrect Permission Assignment for Critical Resource        | Permisos mal configurados sobre un recurso sensible.                                       |
| **CWE-1021** | Improper Restriction of Rendered UI Layers (Clickjacking)    | Falta de protección frente a superposición de capas UI.                                    |

> 💡 Este listado no sustituye la referencia oficial. Consulta siempre [cwe.mitre.org](https://cwe.mitre.org/) para la definición formal y actualizada de cada entrada, especialmente al rellenar el campo "Bug type" en YesWeHack o el selector de tipo en Intigriti.
