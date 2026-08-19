# Glosario de términos

Vocabulario que va a aparecer constantemente en este manual y en cualquier programa de bug bounty.

| Término | Significado |
|---|---|
| **Scope / Alcance** | Los activos (dominios, apps, repos) que el programa autoriza a testear. |
| **Out of scope** | Lo que está explícitamente prohibido tocar. |
| **Safe Harbor** | Cláusula legal que protege al investigador si sigue las reglas del programa. |
| **Triage / Triager** | Persona (o equipo) que revisa tu reporte y decide si es válido antes de pasarlo a la empresa. |
| **Duplicate (Dupe)** | Tu reporte describe algo que ya había sido reportado por otra persona antes. |
| **N/A (Not Applicable)** | El equipo considera que no hay vulnerabilidad real o no cumple los criterios del programa. |
| **PoC (Proof of Concept)** | Prueba de concepto: evidencia reproducible de que el fallo existe. |
| **CVSS** | Common Vulnerability Scoring System, sistema estándar para puntuar la severidad de una vulnerabilidad (0.0–10.0). |
| **CWE** | Common Weakness Enumeration, catálogo estándar de tipos de debilidades de seguridad (ej. CWE-798 = credenciales hardcodeadas). |
| **CVE** | Common Vulnerabilities and Exposures, identificador público de una vulnerabilidad concreta y conocida (normalmente en software de terceros, no en apps a medida). |
| **IDOR** | Insecure Direct Object Reference: acceder/modificar datos de otro usuario cambiando un identificador (ID, UUID...) sin control de permisos. |
| **BOLA** | Broken Object Level Authorization, el nombre "moderno" (OWASP API Top 10) para IDOR en APIs. |
| **XSS** | Cross-Site Scripting: inyección de código en el navegador de otro usuario. |
| **SSRF** | Server-Side Request Forgery: forzar al servidor a hacer peticiones a donde tú quieras. |
| **RCE** | Remote Code Execution: ejecución de código arbitrario en el servidor. |
| **Hardcoded credentials** | Credenciales (contraseñas, tokens, claves API) escritas directamente en el código fuente o binario de la app. |
| **Bounty** | Recompensa económica por una vulnerabilidad válida. |
| **VDP** | Vulnerability Disclosure Program: programa sin recompensa económica (reconocimiento). |
| **VRT** | Vulnerability Rating Taxonomy: tabla de referencia que usan algunas plataformas (Bugcrowd sobre todo) para estandarizar severidades. |
| **Retest** | Volver a probar una vulnerabilidad ya reportada tras el parche, para confirmar que se ha corregido bien. |
| **Collaborator / Colaborador** | Otro investigador con el que compartes autoría de un reporte. |
| **Bounty split** | Reparto del dinero de la recompensa entre colaboradores. |
| **Rate limiting** | Límite de peticiones por tiempo que debería impedir ataques de fuerza bruta o scraping masivo. |
| **Recon** | Fase de reconocimiento: descubrir activos, tecnologías, endpoints, subdominios, etc. |
| **Fingerprinting** | Identificar qué tecnología/framework/versión hay detrás de un sistema. |
| **False Positive** | Algo que parecía una vulnerabilidad pero no lo es. |
| **Blind vulnerability** | Vulnerabilidad que no da respuesta visible directa (ej. Blind XSS, Blind SSRF), se confirma por efectos indirectos (logs, callbacks). |
