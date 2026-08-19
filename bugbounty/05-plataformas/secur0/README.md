# Secur0

## 🧭 Qué es

Plataforma de bug bounty enfocada en comunidad hispanohablante, con formularios de reporte en español y una calculadora CVSS v4.0 integrada muy visual, campo a campo.

## 🗂️ Cómo está organizado el reporte en Secur0

A diferencia de YesWeHack (que separa "cuerpo Markdown libre" + "metadatos"), Secur0 tiene un **formulario con campos de texto libre ya segmentados por secciones fijas**: Título, Alcance, Endpoint, Detalle técnico, Payload, Impacto, Prueba de concepto, y luego la calculadora CVSS con sliders/botones por métrica.

Esto significa que en Secur0 **tú mismo repartes el contenido de tu reporte entre esas cajas de texto ya predefinidas**, en vez de escribir todo en un único bloque Markdown como en YWH.

## 🧮 La calculadora CVSS de Secur0

Secur0 permite:
- **Omitir criticidad** (dejar que el equipo del programa la evalúe).
- **Calcular automáticamente** rellenando el vector CVSS v4.0 completo (Explotabilidad, Impacto en sistema vulnerable, Impacto en sistema subsiguiente) — es la opción recomendada si ya sabes justificar cada métrica (ver [Cálculo de severidad](../../04-como-escribir-reportes/calculo-cvss.md)).
- **Añadir manualmente** un valor si ya tienes el vector calculado por otro medio.

## 👥 Colaboradores y reparto de bounty

Secur0 incluye un campo explícito de **reparto porcentual del bounty entre colaboradores** dentro del propio formulario de envío — muy útil cuando reportas en equipo, ya que queda definido desde el primer momento sin necesidad de negociarlo después.

## 📎 Ver también

* [Plantilla de reporte de Secur0](plantilla-reporte.md)
* [Ejemplo real anonimizado en Secur0](../../06-ejemplos-reales/secur0-password-hardcodeada.md)
