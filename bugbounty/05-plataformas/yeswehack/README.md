---
icon: eyes
---

# Visión general

## 🧭 Qué es

Plataforma europea de bug bounty y coordinación de divulgación de vulnerabilidades (CVD), con programas tanto públicos como privados, muchos de empresas europeas (incluyendo grandes cuentas de telecomunicaciones, energía y sector público).

## 🗂️ Cómo está organizado el reporte en YWH

YesWeHack organiza el reporte en dos grandes bloques:

1. **Bug description**: el cuerpo libre en Markdown donde escribes resumen, detalles técnicos, PoC, impacto y recomendación — aquí es donde aplicas tal cual la [plantilla genérica de reporte](../../04-como-escribir-reportes/anatomia-de-un-buen-reporte.md#-plantilla-genérica-reutilizable).
2. **Report metadata**: un panel lateral de campos estructurados que YWH (o el propio programa, tras revisión) rellena/ajusta — ver la [plantilla de campos](plantilla-reporte.md).

## 🔁 Particularidad clave: los metadatos los puede editar el programa

En YesWeHack, es habitual que el equipo del programa **reescriba el título y ajuste los metadatos** (Scope, Endpoint, Payload...) después de tu envío inicial, para estandarizarlos según su propio criterio interno. No te sorprendas si ves un historial de cambios en el título o el endpoint — es parte normal del proceso de triage en esta plataforma, no significa que algo esté mal en tu reporte original.

## 💬 Sistema de comentarios/actividad

YWH mantiene un hilo de actividad cronológico con cada cambio de estado y cada comentario, tanto tuyo como del programa/triager. Es importante:

* Revisar todo el historial antes de responder, para no repetir lo que ya se dijo.
* Etiquetar bien a los colaboradores si trabajas en equipo (se añaden como "Collaborators" desde el propio reporte).

## 📎 Ver también

* [Plantilla de reporte de YesWeHack](plantilla-reporte.md)
* [Ejemplo real anonimizado en YesWeHack](../../06-ejemplos-reales/yeswehack-jwt-hardcodeado.md)
