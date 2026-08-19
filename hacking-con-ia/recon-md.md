---
icon: file-magnifying-glass
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

# RECON.md — mapa de superficie

## 🧠 Para qué sirve

`RECON.md` guarda todo el reconocimiento acumulado de un programa: subdominios descubiertos, resultados de fingerprinting, análisis de APKs, notas de infraestructura. Se mantiene **separado de `PROGRESS.md` a propósito**: el recon puede crecer muchísimo (cientos de líneas, tablas enormes) y no queremos que eso ensucie el archivo de estado, que tiene que seguir siendo rápido de leer al arrancar cada sesión.

Piensa en `RECON.md` como una base de datos de consulta puntual, y en `PROGRESS.md` como el resumen ejecutivo.

## 🧩 Qué debería contener

### 1. Pendientes de recon

Una lista de tareas de reconocimiento aún no hechas o no verificadas — por ejemplo, mapeo de bundles JS pendiente, subdominios sin fingerprint todavía, activos priorizados para la próxima ronda.

### 2. Rondas de recon, numeradas y fechadas

Cada "ronda" documenta una sesión de reconocimiento concreta: qué fuentes se usaron (certificados SSL vía `crt.sh`, `certspotter`, herramientas de enumeración de subdominios...), cuántos resultados dio, qué filtros se aplicaron, y sobre todo, **una tabla de resultados por host** con su estado (vivo/muerto, tecnología detectada, notas).

```markdown
## Ronda 1 — recon pasivo ([fecha], agente)

**Fuentes**: crt.sh (`%.dominio.com`, 81 hosts únicos) + certspotter
como cruce (24 hosts, subset de crt.sh). Filtrado: excluidos los ya
conocidos → 72 subdominios nuevos. Fingerprint hecho a los 20 más
prometedores.

### Resultado del fingerprint

| Host | Resultado |
|---|---|
| api-interna.ejemplo.com | 403, WAF — API real, viva |
| legacy.ejemplo.com | DNS no resuelve — no vivo |
| id.ejemplo.com | 302 a proveedor externo de identidad — duda de scope, pendiente de confirmar con el programa |
```

### 3. Análisis de apps móviles (si aplica)

Qué paquete se analizó, de dónde se descargó, qué herramientas se usaron, y — lo más valioso — los **endpoints/paths literales encontrados** en el binario/bundle, que luego alimentan directamente la fase de explotación.

### 4. Notas de concurrencia / limitaciones técnicas del entorno

Cuando trabajas con varios agentes compartiendo un mismo navegador o el mismo entorno de red, es habitual toparte con problemas de estado compartido (dos agentes navegando en la misma pestaña sin querer, por ejemplo). Documentarlo aquí en cuanto ocurre te ahorra volver a diagnosticarlo la próxima vez.

## 📄 Ejemplo real anonimizado (fragmento de estilo)

```markdown
# RECON — mapa de superficie del scope ([Programa])

> Recordatorio: cualquier recon activo debe respetar el límite de
> [N] peticiones/segundo de las Rules of Engagement.

## Ronda 1 — recon pasivo ([fecha], agente)

**Fuentes**: crt.sh + certspotter como cruce → [N] subdominios
nuevos tras filtrar los ya conocidos. Fingerprint (GET a raíz,
header de identificación obligatorio, secuencial, muy por debajo
del límite de rate) hecho a los más prometedores.

### Resultado del fingerprint

| Host | Resultado |
|---|---|
| mobilebackend.ejemplo.com | 403, WAF — API real, viva. App móvil
identificada para referencia: [paquete Android], [ID iOS] —
analizar el APK sería tarea aparte, no priorizado todavía. |
| accounts.ejemplo.com | CNAME a proveedor de identidad externo —
confirma el IdP real de la empresa |
| magiclink.ejemplo.com | MUERTO, confirmado a nivel DNS — servicio
antiguo retirado hace años, sin candidatos |
| id.ejemplo.com | 302 a panel de administración de un producto de
terceros (gestión de paywall) — duda genuina de scope, pendiente de
confirmar con el hunter/programa antes de cualquier fase de
explotación |

### Nota de concurrencia ([fecha])

Un agente reportó actividad de OTRO agente en el mismo navegador
compartido mientras trabajaba — vio una pestaña ajena navegando a
otro subdominio y la cerró para recuperar el foco. Los resultados de
ambos agentes llegaron coherentes esta vez, pero refuerza la
mitigación: no lanzar agentes de recon con navegador compartido en
paralelo sin pestañas/contextos aislados confirmados.

## Ronda 2 — análisis de la app móvil ([fecha], análisis estático)

**Paquete**: [nombre del paquete] (Android). Descargado de una
tienda alternativa pública, extracción con unzip + strings sobre
los ficheros DEX (descompilación completa falló por falta de
memoria en el sandbox, no se intentó descompilación selectiva).

**Bases de API móvil identificadas** (patrón de string pool):
`mobile2.ejemplo.com` (prod), `mobile-acc.ejemplo.com` (acc).
Paths literales encontrados: `/rest/mobile/userdata/v1/bookmarks`,
`/rest/mobile/list/v3/bookmarks` — estos alimentan directamente la
siguiente fase de pruebas de IDOR sobre la API móvil.
```

> 📌 **Por qué separar RECON de PROGRESS marca la diferencia**: cuando `RECON.md` alcanza varios miles de palabras (es normal en programas con wildcards grandes), seguiría siendo perfectamente consultable porque solo se abre cuando hace falta un dato concreto de superficie — mientras que `PROGRESS.md` se mantiene corto y se lee entero, cada vez, al arrancar sesión.

## 🎯 Cómo se usa en la práctica

Le pido a los agentes de recon (ver [Agentes en paralelo](agentes-en-paralelo.md)) que devuelvan su resumen a la sesión principal, y es la propia sesión principal la que decide qué se apunta en `RECON.md` frente a qué merece subir directamente a `PROGRESS.md` como hallazgo o pendiente urgente — así se evita que `RECON.md` se convierta en un volcado desordenado de todo lo que hizo cada agente.

### Plantilla descargable RECON.md

{% file src="../.gitbook/assets/RECON.md" %}
