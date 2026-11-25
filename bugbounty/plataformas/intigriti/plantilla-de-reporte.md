---
icon: cards-blank
---

# Plantilla de reporte

Estos son los campos exactos del formulario de envío de Intigriti.

## 📋 General

```
Title
  → Título del reporte (obligatorio)
    Ej: IDOR en API de favoritos permite leer/añadir/borrar
        la lista de guardados de otro usuario

Select asset
  → Elige el activo exacto afectado del scope del programa,
    filtrable por Tier y por tipo (URL, Wildcard, Other...)
    Ej: www.ejemplo-medio.com   (URL, Tier 2)

Endpoint / vulnerable component
  → Endpoint concreto donde vive el fallo
    Ej: https://ejemplo.com/api/_next-api/recurso/
```

## 📋 Tipo de vulnerabilidad

```
Type
  → Macro-categoría (filtro): Access Control Issues / Injection /
    Broken Authentication / Broken Access Control / Mobile /
    Cross site scripting / Vulnerable components / Cryptographic
    issues / Generative AI & LLMs / Memory Management / Other...

  → Dentro de la categoría, el CWE/CAPEC específico, ej.:
    CAPEC-233 Horizontal Privilege Escalation (Broken Access Control)
    CWE-639 Insecure Direct Object Reference (Broken Access Control)
    CWE-798 Use of Hard-coded Credentials (Broken Authentication)
```

## 📋 Severidad (CVSS 3.1)

```
cvss calculator (severity selector)
─────────────────────────────
Attack Vector (AV)        → Network / Adjacent / Local / Physical
Attack Complexity (AC)    → Low / High
Privileges Required (PR)  → None / Low / High
User Interaction (UI)     → None / Required
Scope (S)                 → Unchanged / Changed
Confidentiality (C)       → None / Low / High
Integrity (I)             → None / Low / High
Availability (A)          → None / Low / High

→ Genera automáticamente la puntuación final (0.0–10.0)
```

## 📋 Detalles y evidencias

```
Details
  Attachments
    → Adjuntar capturas/vídeos que soporten el reporte

  Proof of Concept / description
    → (hasta 30.000 caracteres) Pasos de reproducción completos,
      con comandos, capturas embebidas y explicación paso a paso

  Impact
    → (hasta 15.000 caracteres) Impacto real de la vulnerabilidad

  Recommended solution
    → (hasta 15.000 caracteres) Causa raíz + solución sugerida

  IP address used for testing
    → IP pública usada durante las pruebas
      (botón "Fetch my IP" para autocompletar, o manual si usas VPS)
```

## ✅ Checklist antes de enviar en Intigriti

* [ ] El asset elegido es el correcto dentro del scope (revisa el Tier).
* [ ] El tipo de vulnerabilidad elegido es el más específico disponible en el catálogo (evita "Other" si existe una entrada más precisa).
* [ ] El vector CVSS 3.1 está completo, incluyendo el `Scope (S)` (a menudo olvidado, y cambia bastante el resultado si tu vulnerabilidad afecta a un componente distinto del vulnerado inicialmente).
* [ ] El PoC usa el margen de caracteres disponible para ser exhaustivo, no minimalista.
* [ ] La IP de pruebas está rellena (con "Fetch my IP" o manualmente si usas VPS/proxy).
