---
icon: flask
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

# BBLabs

## WriteUps — BBLabs

En este directorio subiré los WriteUps de los retos (labs) de la plataforma **BBLabs**. BBLabs ofrece un entorno web controlado, en español, diseñado para practicar hacking ético y bug bounty hunting. Estos labs son ideales para aprender sobre vulnerabilidades web del mundo real en un entorno seguro y legal.

### ¿Qué es BBLabs?

**BBLabs** (`bblabs.es`) es una plataforma interactiva de laboratorios de bug bounty **en español**, basada en **vulnerabilidades reales extraídas de reportes ya pagados** en programas como HackerOne, Bugcrowd e Intigriti — no CTFs artificiales, sino reproducciones de bugs que realmente cobraron bounty en producción. Cada lab reproduce un entorno web descargable con una vulnerabilidad concreta (XSS, SQLi, IDOR, SSRF, CSRF, y más), permitiendo capturar la flag, leer el writeup oficial y aplicar después la misma técnica en programas de bug bounty activos.

Cada lab incluye información estructurada útil para documentar el WriteUp: dificultad (Fácil/Media/Difícil), tipo de recompensa del reporte original (VDP/Bounty), duración estimada, objetivos paso a paso, herramientas necesarias, prerrequisitos, y tags de la clase de vulnerabilidad — todo esto es el mismo esquema que sigo al redactar cada WriteUp de esta carpeta (ver plantilla más abajo).

### Recursos de BBLabs

* [**Web oficial de BBLabs**](https://bblabs.es/) — el sitio oficial donde encontrar más información y acceder a los labs.
* [**Labs**](https://bblabs.es/labs) — el catálogo completo de laboratorios disponibles.
* [**Academy**](https://bblabs.es/academy) — guías, cheatsheets y diccionario de términos de bug bounty.
* [**Vulnerabilidades**](https://bblabs.es/vulnerabilidades) — labs organizados por clase de vulnerabilidad (XSS, IDOR, SSRF, CSRF...).
* [**Hunter Roadmap**](https://bblabs.es/roadmap) — ruta de aprendizaje de bug bounty paso a paso.
* [**Ranking**](https://bblabs.es/ranking) — clasificación de hunters por labs completados.

### `Machines/` (o `Labs/`)

Cada archivo de este directorio estará nombrado con el nombre del lab correspondiente y contendrá la resolución paso a paso (WriteUp) de la vulnerabilidad, siguiendo la estructura de [Anatomía de un buen reporte](https://claude.ai/04-como-escribir-reportes/anatomia-de-un-buen-reporte.md) de este manual: resumen, objetivos del lab, pasos de reproducción con capturas, causa raíz de la vulnerabilidad, y — cuando aplique — cómo se traduciría en un reporte real (CWE, impacto, severidad).

> 💡 Ejemplo de lab: [**Reflected XSS on 404 Error Page**](https://bblabs.es/labs/reflected-xss-on-404-error-page) — Fácil, VDP, \~10 min. Una red social donde la página de error 404 refleja el parámetro `message` en el HTML sin sanitizar, permitiendo XSS reflejado. El WriteUp correspondiente en esta carpeta seguiría el nombre `reflected-xss-on-404-error-page.md`.
