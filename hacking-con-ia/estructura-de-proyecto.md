---
icon: list-tree
layout:
  width: default
  title:
    visible: true
  description:
    visible: false
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
  metadata:
    visible: true
  tags:
    visible: true
  actions:
    visible: true
---

# Estructura de proyecto y archivos de contexto

## 🗂️ Cómo organizo la carpeta de un programa

Cada programa de Bug Bounty que audito vive en su propia carpeta, con siempre la misma estructura. Esto es clave: **la consistencia entre programas es lo que permite reutilizar la misma metodología y los mismos prompts sin tener que reaprenderlo cada vez.**

```
mi-programa/
├── CLAUDE.md            ← Reglas estáticas del programa (contexto permanente)
├── PROGRESS.md          ← Estado de trabajo — lo primero que se lee al empezar sesión
├── RECON.md             ← Mapa de superficie/subdominios (recon acumulado)
├── promptInicio.txt     ← El prompt que lanzo al empezar cada sesión nueva
├── example/
│   └── report_example.md   ← Plantilla/ejemplo de cómo quiero que se vea un reporte
├── images/
│   └── (capturas de pantalla de las PoCs manuales)
├── reportar/
│   ├── vuln1.md          ← Reporte completo de una vulnerabilidad ya confirmada
│   ├── vuln2.md
│   └── ...
└── temp/
    ├── vuln2/
    │   ├── 00_general_fields.md
    │   ├── 01_proof_of_concept.md
    │   ├── 02_impact.md
    │   └── 03_recommended_solution.md
    ├── vuln3/
    └── ...
```

## 📄 Qué contiene cada pieza

### `CLAUDE.md` — el "manual de instrucciones" del programa

Es el archivo que Claude Code lee automáticamente al arrancar en esa carpeta. Contiene todo el contexto **estático** que no cambia sesión a sesión: reglas de autorización, scope, out-of-scope, tabla de recompensas, Rules of Engagement, cómo organizar los ficheros, y la metodología de trabajo con agentes. Ver el detalle completo en [Qué es un CLAUDE.md](que-es-claude-md.md).

### `PROGRESS.md` — la memoria de trabajo

Es el archivo **dinámico**: qué se ha probado, qué se ha encontrado, qué cuentas de prueba existen, qué queda pendiente. Es lo primero que Claude debe leer al empezar una sesión nueva para saber "dónde lo dejamos". Ver [PROGRESS.md — memoria de trabajo](progress-md.md).

### `RECON.md` — el mapa de superficie

Separado de `PROGRESS.md` a propósito: el recon (subdominios, fingerprinting, hallazgos de análisis de APKs, notas técnicas de infraestructura) puede crecer muchísimo y no conviene que ensucie el archivo de estado, que debe ser rápido de leer. Ver [RECON.md — mapa de superficie](recon-md.md).

### `promptInicio.txt` — el prompt de arranque

Un fichero de texto plano con el prompt exacto que uso para lanzar una nueva sesión de trabajo (lanzar agentes, investigar, parar solo si aparece algo digno de reportar). Ver el detalle en [Flujo de trabajo completo](flujo-de-trabajo-completo.md).

### `example/report_example.md` — plantilla de reporte

Un reporte ya redactado (de un hallazgo real anterior, o uno de referencia) que uso como **ejemplo de estilo y estructura** para que Claude replique el mismo nivel de detalle y el mismo formato en reportes futuros. Ver [Prompts clave](prompts-clave.md) para cómo se referencia en el prompt.

### `images/` — capturas de pantalla

Aquí deposito las capturas que hago **manualmente** al reproducir un hallazgo yo mismo (ver el flujo completo). Le pido a Claude que inspeccione directamente estas imágenes y las integre en el reporte final, tanto en Markdown como en PDF según lo que pida cada plataforma.

### `reportar/` — reportes ya redactados, pendientes de enviar

Cada archivo `vulnN.md` es un reporte completo, en el formato de `example/`, listo para copiar/pegar (o casi) en la plataforma correspondiente.

### `temp/` — campos ya troceados por plataforma

Cuando le pido a Claude que rellene los campos exactos del formulario de una plataforma concreta (YesWeHack, Secur0, Intigriti...), deposita en `temp/vulnN/` un archivo por cada bloque de campos del formulario (título/metadatos, PoC, impacto, solución recomendada...), listos para copiar directamente en cada caja de texto del formulario web.

## 🧹 Limpieza entre sesiones

Es buena práctica pedirle a Claude, al terminar una sesión o un programa, que limpie cualquier script/fichero temporal generado durante la investigación que no sea uno de estos ficheros "oficiales" — así el repo se mantiene limpio y no se acumulan JSONs sueltos, capturas de recon intermedias, o scripts de prueba que ya no hacen falta.
