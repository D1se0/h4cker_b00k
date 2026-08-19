---
icon: file-powerpoint
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

# PROGRESS.md — memoria de trabajo

## 🧠 Para qué sirve

Si `CLAUDE.md` es "lo que no cambia" de un programa, `PROGRESS.md` es exactamente lo contrario: **el estado vivo de la investigación**. Es el primer archivo que le pido a Claude que lea al empezar una sesión nueva, porque contesta a la pregunta más importante: _"¿dónde lo dejamos la última vez?"_

Sin este archivo, cada sesión nueva empezaría de cero — tendrías que volver a explicar qué cuentas de prueba existen, qué ya se probó y descartó, y qué hallazgos están a medio confirmar. Con él, retomar un programa después de una semana sin tocarlo es tan simple como decir "lee `PROGRESS.md` y `RECON.md` y continúa".

## 🧩 Qué debería contener

### 1. Un resumen de "última actualización"

Dos o tres frases arriba del todo con el estado más reciente: qué se cerró, qué se está investigando ahora mismo, qué está bloqueado y por qué. Esto es lo primero que se lee, así que tiene que ser denso y útil.

### 2. Sección "Empezar aquí — pendientes urgentes"

Una lista corta y accionable de lo próximo que hay que hacer, con lo ya resuelto tachado. Es literalmente el "TODO list" activo del programa.

### 3. Tabla de cuentas de prueba activas

Qué cuentas existen, en qué ecosistema/dominio, y notas relevantes sobre para qué sirve cada una (por ejemplo, "cuenta B — para pruebas cruzadas de IDOR con cuenta A").

> 🔒 **Muy importante**: este archivo va a contener credenciales reales de tus propias cuentas de prueba. **Nunca lo compartas ni lo subas a un repositorio público.** Si vas a compartir un fragmento como ejemplo (como hago yo aquí), redacta siempre usuarios, contraseñas y emails.

### 4. Tabla de hallazgos (confirmados y descartados)

El corazón del archivo: cada fila es una vulnerabilidad investigada, con fecha, target, tipo, severidad estimada, y **estado** usando una leyenda simple y consistente. La que uso yo:

| Símbolo       | Significado                                                                                                |
| ------------- | ---------------------------------------------------------------------------------------------------------- |
| `[ ]`         | Pendiente                                                                                                  |
| `[~]`         | En curso                                                                                                   |
| `[x]`         | Cerrado/explorado sin hallazgo                                                                             |
| `[!]`         | Hallazgo confirmado, reproducido de principio a fin y guardado en `reportar/`, pendiente de revisión/envío |
| `[R]`         | Reportado (ya enviado a la plataforma)                                                                     |
| `[BLOQUEADO]` | Confirmado pero con algún impedimento que bloquea el envío (problema de scope, decisión pendiente, etc.)   |

### 5. Estado por target/activo

Una tabla por cada activo del scope, con su estado de recon/investigación — útil para ver de un vistazo qué parte del scope ya está cubierta y cuál no.

### 6. Candidatos descartados (con motivo)

Muy importante para **no repetir trabajo**: cuando investigas una hipótesis y resulta que no hay impacto real, anótalo igualmente, con el motivo exacto. Esto evita que tú (o un agente, semanas después) vuelvas a perder tiempo probando lo mismo.

### 7. Notas técnicas reutilizables

Cualquier "truco" de infraestructura específico de ese programa que te vaya a hacer falta repetidamente: cómo saltarse una protección anti-bot concreta, cómo mantener dos sesiones simultáneas sin que se pisen las cookies, limitaciones del entorno de red que hayas descubierto, etc.

## 📄 Ejemplo real anonimizado (fragmento de estructura)

Así es como luce, con los datos identificativos sustituidos:

```markdown
# Progreso — [Programa] ([Plataforma])

> Leyenda: [ ] pendiente · [~] en curso · [x] cerrado sin hallazgo ·
> [!] hallazgo confirmado, pendiente de revisión y envío ·
> [R] reportado · [BLOQUEADO] confirmado pero no enviar

Última actualización: [fecha] — reportar/vuln5.md enviado [R].
Barrida amplia de agentes en paralelo sobre el wildcard completada
(ver RECON.md Rondas 4-6) — dos candidatos serios a subdomain
takeover encontrados pero pausados por decisión del hunter (exigen
recursos propios excluidos por CLAUDE.md).

## Empezar aquí — pendientes urgentes

1. ~~Rellenar usuario de la plataforma en CLAUDE.md~~ — ✅ hecho
2. ~~Crear cuentas de prueba A y B~~ — ✅ ambas creadas, listas
   para pruebas cruzadas de IDOR/auth
3. Recon inicial del wildcard (ver RECON.md)
4. Primera pasada sobre el activo de mayor prioridad

## Cuentas de prueba activas

| Cuenta | Email | Password | Notas |
|---|---|---|---|
| A | [redactado] | [redactado] | Creada [fecha] |
| B | [redactado] | [redactado] | Para pruebas cruzadas con A |

## Hallazgos (confirmados y descartados)

| Fecha | Target | Tipo | Severidad | Estado |
|---|---|---|---|---|
| [fecha] | endpoint X | IDOR/BOLA | Low | [!] confirmado, reporte en reportar/vuln1.md |
| [fecha] | endpoint X | Broken Auth | — | [!] confirmado, reporte en reportar/vuln2.md |
| [fecha] | endpoint Y | Broken authz en challenge | Medium | [!] confirmado con test decisivo (ATO descartado) |

## Candidatos descartados en Fase 2

- endpoint Z — el parámetro se ignora completamente server-side,
  probado con varios valores → respuesta idéntica en todos los
  casos. No es IDOR, no hay dato expuesto.

## Notas técnicas reutilizables

- Rellenar formularios de login con JS puro dispara la protección
  anti-bot en este programa — usar eventos CDP reales
  (Input.dispatchMouseEvent / dispatchKeyEvent) en vez de
  manipulación directa del DOM.
```

> 📌 **Detalle real que merece la pena copiar**: en uno de mis programas descubrí que el login disparaba un bloqueo anti-bot cuando rellenaba el formulario con JavaScript puro (`element.value = ...`), pero funcionaba perfectamente simulando eventos reales de teclado/ratón vía Chrome DevTools Protocol. Ese tipo de detalle **tiene que vivir en `PROGRESS.md` (o `RECON.md`)**, porque si no lo vas a redescubrir cada vez que vuelvas a ese programa.

## 🔄 Cómo mantenerlo actualizado sin esfuerzo

No lo actualizo yo a mano: se lo pido directamente a Claude como parte del propio flujo de trabajo (ver [Flujo de trabajo completo](flujo-de-trabajo-completo.md) y [Prompts clave](prompts-clave.md)) — en el `CLAUDE.md` dejo indicado que cualquier hallazgo confirmado se anota en `PROGRESS.md` **en el momento en que se confirma**, no al final de la sesión, precisamente para no perderlo si la sesión se corta a mitad de camino.

### Plantilla descargable PROGRESS.md

{% file src="../.gitbook/assets/PROGRESS.md" %}
