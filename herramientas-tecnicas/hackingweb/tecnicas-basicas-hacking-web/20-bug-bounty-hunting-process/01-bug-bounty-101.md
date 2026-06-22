# Bug Bounty 101: cómo funcionan los programas

## Qué es un programa de bug bounty

Un programa de bug bounty (también llamado **VRP — Vulnerability Rewards Program**) es una iniciativa por la que una organización invita a investigadores de seguridad externos a probar sus sistemas y reportar vulnerabilidades a cambio de una recompensa económica. Es una forma de prueba de seguridad continua que complementa las auditorías internas y los pentests formales — añadiendo la perspectiva de la comunidad investigadora.

> **Distinción importante**: un programa de bug bounty (BBP) no es lo mismo que un **VDP (Vulnerability Disclosure Program)**. Un VDP solo define el proceso de comunicación de vulnerabilidades, sin recompensa económica. Un BBP incentiva activamente la búsqueda con recompensas monetarias.

## Tipos de programa

| Tipo | Características |
|---|---|
| **Privado** | Solo accesible por invitación directa — la mayoría de programas empiezan así para controlar el volumen de reportes. Las invitaciones se basan en historial, reputación, y tipo de hallazgos previos del investigador. |
| **Público** | Abierto a cualquier investigador — la mayoría de programas evolucionan hacia este modelo. |
| **Padre/hijo** | Un programa que cubre simultáneamente la empresa matriz y sus subsidiarias, con un único equipo de gestión de seguridad. |

## Anatomía de un programa

Cada programa de bug bounty tiene una política que define exactamente cómo participar. Los elementos estándar:

| Elemento | Qué define |
|---|---|
| **Scope** | Qué dominios, IPs, aplicaciones o componentes están incluidos en el alcance y pueden ser probados |
| **Out of Scope** | Qué está explícitamente excluido — probar algo fuera del scope puede resultar en descalificación o consecuencias legales |
| **Rewards** | Rangos de recompensa según severidad del hallazgo (normalmente por CVSS score o clasificación propia) |
| **Responsible Disclosure Policy** | Plazos para coordinar la divulgación pública — habitualmente 90 días para que la organización corrija antes de revelar públicamente |
| **Rules of Engagement** | Qué está permitido y qué no durante las pruebas (por ejemplo, no provocar DoS, no acceder a datos reales de usuarios) |
| **Eligibility** | Condiciones para recibir recompensa (primero en reportar, vulnerabilidad no previamente conocida, etc.) |
| **Safe Harbor** | Protección legal para investigadores que actúen dentro del alcance definido |
| **SLA de respuesta** | En cuánto tiempo el equipo de seguridad responde al reporte inicial |

## Plataformas principales

- **HackerOne** (hackerone.com): la más extendida. Directorio público de programas en hackerone.com/directory/programs.
- **Bugcrowd** (bugcrowd.com): segunda plataforma más grande.
- **Intigriti** (intigriti.com): fuerte presencia en Europa.
- **Programas directos**: muchas organizaciones grandes (Google, Microsoft, Apple) gestionan sus propios programas independientemente de plataformas intermediarias.

## Reglas de comportamiento profesional

El historial de infracciones de un investigador afecta directamente a sus posibilidades de ser invitado a programas privados y de mantener reputación en la comunidad. Las normas fundamentales:

- **Nunca probar fuera del scope definido** — aunque creas haber encontrado algo importante.
- **No almacenar datos personales** de usuarios reales encontrados durante las pruebas.
- **No provocar daño** — sin DoS, sin borrado de datos, sin modificaciones que afecten a usuarios reales.
- **Reportar de forma completa** — un reporte incompleto o reproducible solo para el investigador no es útil para el equipo de seguridad.
- **Respetar los plazos de divulgación** — no publicar el hallazgo antes de que el proveedor haya tenido tiempo de corregirlo.

## Por qué el bug bounty como complemento al pentesting convencional

Los pentests formales son snapshots — una auditoría de dos semanas no puede cubrir la misma superficie que cientos de investigadores durante todo el año. Los programas de bug bounty añaden profundidad de cobertura y perspectivas diversas, a menudo encontrando vulnerabilidades que escapan a los procesos de seguridad internos. Son, en este sentido, una capa adicional de defensa en profundidad aplicada a la propia estrategia de seguridad de una organización.
