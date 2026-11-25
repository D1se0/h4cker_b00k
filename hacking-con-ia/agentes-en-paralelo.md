---
icon: user-hat-tie-magnifying-glass
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

# Agentes en paralelo

## 🧠 Qué es un "agente" en este contexto

Cuando hablo de "lanzar agentes" en Claude Code, me refiero a **subagentes**: instancias de Claude con su propio contexto de trabajo, invocadas desde la sesión principal para investigar algo concreto (una clase de vulnerabilidad, un lote de subdominios, un activo específico) de forma independiente, y que devuelven un resumen a la sesión principal al terminar.

Esto permite paralelizar el trabajo de reconocimiento y exploración inicial, mientras la sesión principal (tú + Claude) se encarga de decidir qué merece pasar a verificación manual.

## ⚖️ Por qué necesita reglas propias

El paralelismo es potentísimo, pero introduce dos riesgos reales que hay que gestionar explícitamente:

1. **Saltarse límites de rate del programa sin darte cuenta.** Si tienes un límite de, por ejemplo, 5 peticiones/segundo y lanzas 4 agentes que atacan el mismo host a la vez, es muy fácil superar ese límite sin que ningún agente individual "sienta" que está yendo rápido.
2. **Corromper estado compartido.** Si varios agentes comparten el mismo navegador, la misma sesión autenticada, o el mismo fichero de notas, pueden pisarse entre sí — un agente puede leer el contexto de otro por error, o dos agentes pueden intentar escribir en el mismo sitio a la vez.

## 🗂️ Mi metodología en tres fases

### Fase 1 — Recon, en paralelo

Las tareas de **solo lectura**, con huella de red baja y sin estado mutable son las candidatas ideales para lanzar varios agentes a la vez: enumerar subdominios, mapear bundles JS en busca de endpoints nuevos, hacer fingerprint de un lote de hosts sin explorar, o repetir una misma clase de vulnerabilidad conocida contra varios activos independientes entre sí.

**Reglas que sigo:**

* **Alcance acotado por agente**: cada agente recibe una tarea concreta y delimitada (una clase de vulnerabilidad, o un puñado de targets específicos) — nunca un "busca vulnerabilidades en todo el scope" genérico, que es imposible de supervisar bien.
* **Nunca dos agentes contra el mismo target o la misma cuenta de prueba a la vez.** El tráfico concurrente sobre un único objetivo puede disparar defensas anti-bot, y hace mucho más fácil superar el límite de rate sin darte cuenta. Reparto los agentes por target/dominio distinto, nunca por técnica repetida sobre el mismo target.
* **Vigilar que la suma de peticiones/segundo de todos los agentes activos no supere el límite del programa** — si tienes 4 agentes y un límite de 5 req/s total, cada agente individualmente tiene que ir muy por debajo de 5, no cada uno a su propio ritmo de 5.
* **Los agentes devuelven su resumen a la sesión principal**; es la sesión principal la que decide qué se apunta en `RECON.md`/`PROGRESS.md` — evita que cada agente escriba directamente y de forma descoordinada en los archivos compartidos.

### Fase 2 — Explotación y verificación, en serie

En cuanto un hallazgo de la Fase 1 parece prometedor, **pasa a ejecutarse en un único hilo de trabajo, nunca en paralelo**, sobre la cuenta de prueba correspondiente, hasta reproducirlo de principio a fin.

**Regla de oro**: nunca dar por confirmada una vulnerabilidad solo porque un agente diga que la ha encontrado — se reproduce paso a paso, idealmente dos veces, antes de tratarla como real. Esto conecta directamente con el paso 3 del [Flujo de trabajo completo](flujo-de-trabajo-completo.md#3️⃣-cuando-aparece-algo-prometedor-pedir-la-guía-de-reproducción-manual): pedir la guía de reproducción manual y hacerla tú mismo es, precisamente, esa verificación.

### Fase 3 — Guardar el hallazgo reportable

En cuanto una vulnerabilidad está reproducida de principio a fin y con impacto demostrado dentro de los límites del programa:

1. Se guarda un `.md` en `reportar/<nombre-del-hallazgo>.md` con el mismo estándar que un reporte final.
2. Se marca la entrada correspondiente en `PROGRESS.md`.
3. Este guardado se hace **en cuanto se confirma el hallazgo, no al final de la sesión** — para no perderlo si la sesión se corta a mitad de camino (corte de red, límite de uso agotado, etc.).

## 🧭 Riesgos concretos de estado compartido (y cómo mitigarlos)

Si tus agentes comparten un navegador real (por ejemplo, vía un MCP de control de navegador), ten en cuenta:

* **El "puntero de pestaña seleccionada" suele ser global al navegador, no por agente.** Si dos agentes (o un agente + tú) operan a la vez, una acción sin especificar explícitamente sobre qué pestaña/página actuar puede devolver o modificar el contenido de la pestaña de OTRO agente.
* **Mitigación**: evita hacer trabajo interactivo propio en el navegador mientras haya agentes de recon activos usándolo, o usa siempre un identificador de página/pestaña explícito en cada acción en vez de depender de "la pestaña actualmente seleccionada".
* **Para pruebas cross-cuenta** (necesitas dos sesiones logueadas simultáneamente, por ejemplo cuenta A y cuenta B a la vez), las cookies de un dominio suelen compartirse por todo el perfil del navegador — dos pestañas normales van a compartir sesión. La solución es crear **contextos de navegador aislados** (equivalente a modo incógnito, pero controlado programáticamente) para que cada cuenta viva en su propio contexto sin pisarse.

## ✅ Checklist rápida antes de lanzar agentes en paralelo

* [ ] ¿Cada agente tiene una tarea acotada y concreta, no genérica?
* [ ] ¿Ningún par de agentes ataca el mismo host/cuenta de prueba a la vez?
* [ ] ¿La suma de tráfico de todos los agentes respeta el límite de rate del programa?
* [ ] ¿Los agentes van a devolver resultados a la sesión principal en vez de escribir directamente y sin coordinación en archivos compartidos?
* [ ] ¿Tienes plan Max (o equivalente) para no agotar tu cuota de uso a mitad de la investigación?

> ⚠️ Recuerda: esto solo tiene sentido dentro de programas con Rules of Engagement que lo permitan explícitamente. Si un programa prohíbe herramientas automatizadas o exige exclusivamente pruebas manuales, la Fase 1 en paralelo debe respetar igualmente esa restricción — "en paralelo" no es sinónimo de "automatizado y masivo", puede significar simplemente "varios hilos de trabajo manual/asistido investigando cosas distintas al mismo tiempo".
