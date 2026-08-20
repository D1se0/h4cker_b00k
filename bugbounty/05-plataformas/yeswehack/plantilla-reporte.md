---
icon: cards-blank
---

# Plantilla de reporte

Un reporte en YesWeHack se rellena en un formulario dividido en **cuatro bloques**: `Bug details` (metadatos técnicos), `Bug characteristics` (vector CVSS), `Bug description` (título + cuerpo en Markdown) y, opcionalmente, `Bug chain`. Los campos marcados con `*` en el formulario real son obligatorios.

## 1️⃣ Bug details

```
Bug type
  → Desplegable con el catálogo de CWE de YWH, agrupado por categoría.
    No se escribe libremente: se busca y se selecciona de la lista.
    Categorías disponibles: Access Control issues · Cryptographic issues ·
    Memory corruption issues · Secure design issues · Input issues
    (y alguna más según el programa).

    Ejemplos reales del desplegable:
    - IDOR - Insecure Direct Object Reference (IDOR) (CWE-639)
    - Improper Access Control - Improper Access Control - Generic (CWE-284)
    - Improper Authentication - Improper Authentication - Generic (CWE-287)
    - Hard-coded Credentials - Use of Hard-coded Credentials (CWE-798)
    - XSS - Cross-site Scripting (XSS) - Generic (CWE-79)
    - Reflected XSS - Cross-site Scripting (XSS) - Reflected (CWE-79)
    - Stored XSS - Cross-site Scripting (XSS) - Stored (CWE-79)
    - DOM XSS - Cross-site Scripting (XSS) - DOM (CWE-79)
    - SQL Injection (CWE-89) · SSRF (CWE-918) · XXE (CWE-611)
    - CSRF - Cross-Site Request Forgery (CSRF) (CWE-352)
    - Business Logic Error - Business Logic Errors (CWE-840)
    - Open Redirect (CWE-601) · Race Condition (CWE-364)
    - Subdomain Takeover - Server Misconfiguration (CWE-16)
    - CORS Misconfiguration (CWE-942)
    - Information Disclosure (CWE-200)
    (la lista completa supera el centenar de entradas — escribe
    palabras clave en el buscador del desplegable, ej. "IDOR", "XSS",
    "hard-coded", para encontrar el CWE exacto más rápido)

Scope
  → También es un desplegable, NO texto libre: lista únicamente los
    activos que el programa ha dado de alta como scope. Se busca por
    nombre y se selecciona.
    Ejemplos reales de entradas de este desplegable: una URL de app
    ("https://pidetugasoleo.repsol.es/"), un enlace de Google Play o
    App Store, un wildcard ("*.repsol.com", "*.repsol.es"), o un
    subdominio concreto ("areacliente.repsol.es").

Endpoint
  → Campo de texto libre. Ruta(s) exacta(s) afectadas dentro del
    Scope seleccionado.
    Ej: /resources/assets/index.android.bundle, /recomendarpot/{cups}

Vulnerable part
  → Desplegable con el tipo exacto de parámetro vulnerable. Opciones
    reales disponibles:
    GET parameter · POST parameter · PUT parameter · PATCH parameter ·
    Cookie · Header · Path · HTTP Method · HTTP Response · DNS record ·
    GraphQL Query · GraphQL Mutation · Others

Part name
  → Texto libre. El nombre exacto del parámetro/campo vulnerable.
    Ej: cups

Payload
  → Texto libre. El payload/valor exacto usado en la prueba.

Technical environment
  → Texto libre. Placeholder del propio formulario:
    "OS, Browser, Tools, Version..."
    Ej: Kali Linux, Burp Suite 2026.x, curl 8.18.0, python3

Application fingerprint
  → Texto libre. Tecnología identificada en el backend/frontend, con
    la evidencia que lo confirma.
    Ej: Python/Flask backend (PyJWT) — confirmado por el string
    "Not enough segments"

CVE
  → Texto libre, opcional. Placeholder: "CVE-YYYY-NNNN"
    (solo aplica si la vulnerabilidad corresponde a un CVE ya
    publicado de un componente de terceros — normalmente vacío en
    apps a medida)

Impact
  → Texto libre, campo breve — complementario al Impact detallado
    que se redacta en el cuerpo Markdown de Bug description.

IPs used
  → Texto libre, varias IPs separadas por comas. El propio formulario
    incluye un botón "Get my ip" para autocompletar con tu IP actual.
```

## 2️⃣ Bug characteristics — vector CVSS

⚠️ **Importante**: a diferencia de lo que indicaba la versión anterior de esta plantilla, YesWeHack usa **CVSS 3.1**, no 4.0. El formulario construye el vector en vivo según vas marcando cada métrica, y lo muestra arriba en formato texto:

```
CVSS Vector
CVSS:3.1/AV:[?]/AC:[?]/PR:[?]/UI:[?]/S:[?]/C:[?]/I:[?]/A:[?]
```

Métricas exactas del formulario, con sus opciones reales:

```
Attack Vector (AV)         → Network · Adjacent · Local · Physical
Attack Complexity (AC)     → Low · High
Privileges Required (PR)   → None · Low · High
User Interaction (UI)      → None · Required
Scope (S)                  → Unchanged · Changed
Confidentiality (C)        → None · Low · High
Integrity (I)               → None · Low · High
Availability (A)           → None · Low · High
```

El formulario recalcula la puntuación en tiempo real conforme seleccionas cada métrica (por defecto arranca en `None - 0.0` con todo en `null`). Aviso textual del propio formulario, que conviene tener siempre presente:

> *"Before selecting a CVSS vector, please consider its impact on the company and users to avoid overestimating the score."*

## 3️⃣ Bug description

```
Report title
  → Texto libre. Título del reporte.

Description (Accepted language)
  → Editor Markdown con pestañas "Write" / "Preview".
```

YWH **precarga su propia plantilla oficial** en este campo (el "YWH Report Template"), con estas secciones exactas — adapta aquí el contenido que hayas redactado siguiendo la [plantilla genérica de reporte](../../04-como-escribir-reportes/anatomia-de-un-buen-reporte.md#-plantilla-genérica-reutilizable) de este manual, pero usando los nombres de sección propios de YWH:

```markdown
## Description
General description of this kind of vulnerability and in which
*workflow* of the application it is part.

## Exploitation
Description of each of the exploitation steps

## PoC
Here you can paste your Proof of Concept.

## Risk
Here you can describe risks for the application, its users and the
company

## Remediation
Here you can provide vulnerability remediation elements to help the
program manager to the report treatment
```

**Tips de Markdown soportado en este editor** (según la propia ayuda del formulario):

- Encabezados `#`, `##`, `###`, `####`; listas con `-`; **negrita** con `**texto**`; *cursiva* con `*texto*`; enlaces `[texto](url)`.
- Bloques de código con lenguaje especificado — lenguajes soportados: `burp`, `bash`, `css`, `html`, `http`, `java`, `javascript`, `json`, `php`, `python`, `shell`, `xml`, `graphql`, `ruby`, y `brainfuck` (guiño del propio formulario).
- **Adjuntos**: primero se suben en el bloque `Attachments` (más abajo), lo que genera un ID `YWH-RXXX`. Ese ID se referencia dentro del cuerpo Markdown de dos formas:
  - `YWH-RXXX` → inserta un **enlace** al adjunto.
  - `{YWH-RXXX}` → **inserta la imagen/vídeo directamente** en el cuerpo del reporte.

```
Attachments
  → Imágenes: JPEG o PNG, máx. 10MB. Vídeos: MP4 o WEBM, máx. 100MB.
  → Botón "Upload" para subir archivo, o "Live recording" para grabar
    directamente desde el navegador.
```

## 4️⃣ Bug chain (opcional)

```
☐ Check this to chain this bug to another
```

Casilla para **encadenar** este reporte con otro ya existente — útil cuando la vulnerabilidad que reportas solo tiene impacto real combinada con otra ya reportada (por ejemplo: un IDOR que por sí solo es de severidad baja, pero encadenado con un bypass de autenticación de otro reporte tuyo se convierte en account takeover completo).

---

`* Mandatory fields` — el formulario marca así los campos obligatorios; el resto son opcionales pero muy recomendables para acelerar el triage.

> 📌 Antes de pulsar "Submit report", YWH muestra un aviso de confirmación: *"You're about to submit a report on [Programa] Bug Bounty Program. Have you checked all the report information?"* — con opciones **Cancel** / **Submit report**. Una vez enviado, si el programa lo permite, podrás invitar colaboradores al reporte.

## ✅ Checklist antes de enviar en YWH

* [ ] El `Bug type` está seleccionado del desplegable con el CWE más específico posible (usa el buscador interno, no te quedes con el genérico "Generic" si existe uno más preciso).
* [ ] El `Scope` seleccionado es exactamente el activo correcto de la lista del programa (revisa que no exista una entrada más específica, ej. un subdominio concreto en vez del wildcard).
* [ ] `Endpoint`, `Vulnerable part` y `Part name` describen con precisión dónde vive el fallo.
* [ ] El `Payload` es el mínimo necesario para reproducir (sin datos reales de terceros).
* [ ] `Technical environment` está relleno — ayuda al triager a reproducir en condiciones similares.
* [ ] El vector CVSS 3.1 está completo (`AV`/`AC`/`PR`/`UI`/`S`/`C`/`I`/`A`) y razonado, sin sobrestimar la puntuación.
* [ ] El cuerpo de `Description` sigue las 5 secciones del YWH Report Template (Description, Exploitation, PoC, Risk, Remediation), con capturas insertadas vía `{YWH-RXXX}`.
* [ ] `IPs used` está relleno (botón "Get my ip" o manual si usas VPN/VPS).
* [ ] Revisado si el hallazgo debería marcarse como `Bug chain` de otro reporte tuyo ya existente.
