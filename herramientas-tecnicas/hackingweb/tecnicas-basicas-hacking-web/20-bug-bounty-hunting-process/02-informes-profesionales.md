# Cómo redactar un informe de vulnerabilidad profesional

## Por qué el informe importa tanto como el hallazgo

Un hallazgo técnico brillante comunicado de forma confusa o incompleta tiene pocas probabilidades de ser corregido rápidamente, recompensado justamente, o tomado en serio. La calidad del informe determina la percepción de la severidad del hallazgo, el tiempo de triaje del equipo de seguridad, y la velocidad de corrección. En un programa de bug bounty, también determina directamente la recompensa recibida.

## Estructura estándar de un informe de vulnerabilidad

| Campo | Contenido |
|---|---|
| **Título** | Tipo de vulnerabilidad + dominio/endpoint afectado + impacto en una línea. Ejemplo: "Stored XSS en el campo de nombre de perfil permite robo de sesión de administrador" |
| **CWE** | Clasificación de la debilidad según el catálogo MITRE CWE — lenguaje estándar para describir el tipo de fallo |
| **CVSS Score** | Puntuación de severidad calculada con la calculadora CVSS 3.1 (ver más abajo) |
| **Descripción** | Qué es la vulnerabilidad, por qué existe, qué componente está afectado |
| **Proof of Concept (PoC)** | Pasos numerados y reproducibles para demostrar la vulnerabilidad |
| **Impacto** | Qué puede lograr un atacante explotando esta vulnerabilidad — impacto técnico Y de negocio |
| **Remediación** | Cómo corregirlo (recomendado pero opcional en BBP) |

## El campo más crítico: Proof of Concept

Un buen PoC tiene tres características:

1. **Reproducible**: cualquier persona del equipo de seguridad puede seguir los pasos y obtener el mismo resultado, sin necesidad de contexto adicional.
2. **Conciso**: solo los pasos estrictamente necesarios para demostrar la vulnerabilidad, sin detalles irrelevantes.
3. **Claro sobre el impacto**: el resultado final muestra inequívocamente que la vulnerabilidad existe y cuál es su consecuencia.

**Ejemplo de PoC bien estructurado (XSS almacenado):**
```
1. Autenticarse en la aplicación como usuario estándar.
2. Navegar a Perfil > Editar nombre.
3. En el campo "Nombre completo", introducir: <script>alert(document.cookie)</script>
4. Guardar el perfil.
5. Navegar a cualquier página que muestre el nombre del usuario (p.ej., /dashboard).
6. Observar que se ejecuta la alerta con las cookies de sesión actuales.

Resultado: código JavaScript arbitrario se ejecuta en el navegador de cualquier usuario que visualice el perfil comprometido.
```

## Calculando la severidad con CVSS 3.1

El [Sistema de Puntuación de Vulnerabilidades Común (CVSS)](https://www.first.org/cvss/calculator/3.1) proporciona un método estandarizado para comunicar la gravedad. Los factores del **Base Score** (puntuación base):

### Vector de ataque
| Valor | Qué significa |
|---|---|
| **Network (N)** | Explotable de forma remota a través de internet |
| **Adjacent (A)** | Solo desde la misma red local o VPN |
| **Local (L)** | Requiere acceso local al sistema |
| **Physical (P)** | Requiere acceso físico al dispositivo |

### Complejidad del ataque
| Valor | Qué significa |
|---|---|
| **Low (L)** | Explotable repetidamente sin preparación especial |
| **High (H)** | Requiere preparación específica o condiciones especiales |

### Privilegios requeridos
| Valor | Qué significa |
|---|---|
| **None (N)** | Explotable sin ninguna autenticación |
| **Low (L)** | Requiere cuenta de usuario estándar |
| **High (H)** | Requiere cuenta de administrador |

### Interacción de usuario
| Valor | Qué significa |
|---|---|
| **None (N)** | No requiere acción de otro usuario |
| **Required (R)** | Requiere que otro usuario realice alguna acción (p.ej., visitar una URL) |

### Impacto (Confidencialidad / Integridad / Disponibilidad)
| Valor | Qué significa |
|---|---|
| **None (N)** | No hay impacto en esta dimensión |
| **Low (L)** | Impacto parcial o limitado |
| **High (H)** | Impacto total o crítico |

### Ejemplo completo: CVE-2016-1287 (Cisco ASA buffer overflow)

| Métrica | Valor | Justificación |
|---|---|---|
| Attack Vector | Network | Dispositivo expuesto a internet como VPN gateway |
| Attack Complexity | Low | El exploit disponible se ejecuta directamente |
| Privileges Required | None | Explotable sin autenticación previa |
| User Interaction | None | No requiere interacción del usuario |
| Scope | Unchanged | Solo afecta al componente vulnerable |
| Confidentiality | High | Shell reversa con acceso total a la información |
| Integrity | High | Control total sobre los datos del componente |
| Availability | High | Puede deshabilitar el servicio completamente |
| **CVSS Score** | **9.8 (Crítico)** | |

## Escalas de severidad

| Rango CVSS | Severidad |
|---|---|
| 9.0 – 10.0 | Crítico |
| 7.0 – 8.9 | Alto |
| 4.0 – 6.9 | Medio |
| 0.1 – 3.9 | Bajo |
| 0.0 | Ninguno |

## El CWE: clasificar el tipo de debilidad

El [catálogo CWE de MITRE](https://cwe.mitre.org/) proporciona identificadores estandarizados para tipos de debilidades. Algunos CWEs frecuentes en este temario:

| CWE | Tipo de debilidad |
|---|---|
| CWE-79 | Cross-Site Scripting (XSS) |
| CWE-89 | SQL Injection |
| CWE-78 | OS Command Injection |
| CWE-22 | Path Traversal |
| CWE-639 | IDOR (Authorization Bypass Through User-Controlled Key) |
| CWE-918 | SSRF |
| CWE-611 | XXE |
| CWE-287 | Autenticación defectuosa |
| CWE-352 | CSRF |

En una cadena de vulnerabilidades, usar el CWE correspondiente a la **vulnerabilidad inicial** que hace posible el resto de la cadena.

## Recomendaciones para reportar a organizaciones menos maduras técnicamente

Cuando el receptor del informe no tiene un equipo de seguridad técnico, traducir el impacto a términos de negocio es fundamental:

- En lugar de "SQLi UNION-based permite extraer todos los registros de la tabla `users`" → "Un atacante puede acceder a todos los nombres de usuario y contraseñas de los clientes registrados, comprometiendo sus cuentas y exponiendo a la empresa a responsabilidades legales bajo la normativa de protección de datos".
- Cuantificar el impacto cuando sea posible: "X usuarios afectados", "datos de Y años de historial accesibles", "coste estimado por incidente similar en el sector".

## Un buen ejemplo público de referencia

HackerOne publica informes cerrados y reconocidos. Un buen ejemplo para entender el estándar: [hackerone.com/reports/341876](https://hackerone.com/reports/341876) — estructura clara, PoC reproducible, impacto bien articulado.

## Cierre del temario

Con este bloque se completa el recorrido completo del temario CWES de HackTheBox Academy: desde los fundamentos del protocolo HTTP hasta el proceso profesional de reporte de vulnerabilidades, pasando por 18 categorías de vulnerabilidades web cubiertas con su contexto técnico, payloads de ejemplo, y mitigaciones concretas. La seguridad ofensiva y la defensiva no son mundos separados — entender cómo funciona un ataque es el mejor fundamento para diseñar sistemas que lo resistan.
