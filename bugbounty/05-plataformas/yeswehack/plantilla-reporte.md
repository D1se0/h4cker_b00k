# Plantilla de reporte — YesWeHack

Estos son los campos exactos que maneja YesWeHack en el panel de **Report metadata** de un reporte, más el cuerpo en Markdown de **Bug description**.

## 📋 Bug description (cuerpo Markdown)

Usa aquí la [plantilla genérica de reporte](../../04-como-escribir-reportes/anatomia-de-un-buen-reporte.md#-plantilla-genérica-reutilizable) completa: Summary, Vulnerability Details, Steps to Reproduce & PoC, Impact, Recommended Fix, Reproduction Checklist.

## 🗂️ Report metadata (panel lateral)

```
CVSS
(Puntuación calculada con la calculadora CVSS integrada de YWH)

Report metadata
─────────────────────────────
Bug type
  → El CWE correspondiente, con su enlace a cwe.mitre.org
    Ej: Use of Hard-coded Credentials (CWE-798)

Scope
  → El activo exacto del programa donde aplica
    (una URL de Google Play, un dominio, un repositorio...)

Host
  → El host/dominio concreto donde vive la vulnerabilidad
    Ej: maceba.ejemplo-empresa.com

Endpoint
  → Ruta(s) exacta(s) afectadas, separadas por coma si son varias
    Ej: /resources/assets/index.android.bundle, /recomendarpot/{cups}

Vulnerable part
  → Dónde vive el parámetro vulnerable: Path / Query / Body / Header / Cookie

Part name
  → El nombre exacto del parámetro vulnerable
    Ej: cups

Payload
  → El payload/valor exacto usado en la prueba
    (en credenciales hardcodeadas, el propio token; en un IDOR, el ID usado)

Technical env.
  → Tu entorno de pruebas: SO, versión de herramientas
    Ej: Kali Linux, curl 8.18.0, python3, grep

App. fingerprint
  → Tecnología identificada en el backend/frontend, con la evidencia que lo confirma
    Ej: Python/Flask backend (PyJWT) — confirmado por el string "Not enough segments"

CVE
  → Si aplica (normalmente "-" en apps a medida, sí aplica en software de terceros conocido)

Impact
  → Campo breve, complementario al Impact detallado del cuerpo Markdown

IP used
  → La IP desde la que hiciste las pruebas (para que el equipo pueda cruzarlo con sus logs)
```

## ✅ Checklist antes de enviar en YWH

- [ ] El `Bug type` tiene el CWE correcto y enlazado.
- [ ] `Scope`, `Host` y `Endpoint` son exactos y coinciden con lo descrito en el cuerpo.
- [ ] El `Payload` es el mínimo necesario para reproducir (sin datos reales de terceros).
- [ ] `Technical env.` está relleno — ayuda al triager a reproducir en condiciones similares.
- [ ] La `IP used` es la real de tus pruebas.
- [ ] El CVSS calculado en el cuerpo del reporte coincide con el de la calculadora integrada.
