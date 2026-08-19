# Intigriti

## 🧭 Qué es

Plataforma europea de bug bounty con un catálogo de programas muy amplio (medios de comunicación, retail, fintech...) y un formulario de envío muy estructurado, con selector de activo (asset) por "tier" y un catálogo enorme de tipos de vulnerabilidad predefinidos organizados por categoría.

## 🗂️ Particularidades del formulario de Intigriti

- **Selector de activo por Tier**: cada dominio/subdominio/wildcard del scope tiene asignado un "Tier" (nivel de importancia/prioridad para el programa). Elegir bien el asset correcto es clave para que tu reporte se enrute al equipo adecuado.
- **Catálogo de tipos de vulnerabilidad gigantesco**: Intigriti no te deja escribir el CWE libremente, sino que **eliges de una lista larguísima** organizada por macro-categoría (Access Control Issues, Injection, Broken Authentication, Cross-Site Scripting, Mobile, Generative AI & LLMs, Memory Management...) y luego el CWE específico dentro de esa categoría.
- **Calculadora CVSS con "Scope (S)"**: a diferencia de Secur0 (que usa CVSS 4.0 con "Attack Requirements" y separación Vulnerable/Subsequent System), Intigriti todavía usa el modelo CVSS 3.1 con la métrica clásica **Scope (Unchanged/Changed)**.
- **Campos de texto con contadores de caracteres generosos**: Proof of Concept (30.000 caracteres), Impact (15.000) y Recommended solution (15.000) — mucho margen para documentar a fondo.
- **IP de pruebas con autocompletado**: botón "Fetch my IP" para rellenar automáticamente tu IP pública real.

## 📎 Ver también

* [Plantilla de reporte de Intigriti](plantilla-reporte.md)
* [Ejemplo real anonimizado en Intigriti](../../06-ejemplos-reales/intigriti-idor-favoritos.md)
