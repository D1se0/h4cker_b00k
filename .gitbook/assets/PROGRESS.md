# Progreso — [EMPRESA] ([PLATAFORMA])

> Ver `CLAUDE.md` para reglas del programa, scope completo, recompensas y
> datos del hunter. Ver `RECON.md` para el mapa de superficie/subdominios.
> Documento de **estado de trabajo** — optimizado para retomar rápido al
> empezar sesión.
>
> Leyenda: `[ ]` pendiente · `[~]` en curso · `[x]` cerrado/explorado sin
> hallazgo · `[!]` hallazgo confirmado, reproducido de principio a fin y
> guardado en `reportar/`, pendiente de que el hunter lo revise y envíe ·
> `[R]` reportado (enviado a [PLATAFORMA]) · `[BLOQUEADO]` confirmado y
> guardado en `reportar/`, pero **NO ENVIAR** (problema de scope u otro
> impedimento — ver nota en la entrada)

Última actualización: [FECHA] — [RESUMEN BREVE DE LA ÚLTIMA SESIÓN: qué se
cerró, qué se envió, qué quedó bloqueado y por qué, qué se retomó de
sesiones anteriores. Este párrafo es lo primero que se lee al arrancar una
sesión nueva — mantenlo denso y actualizado].

---

## Empezar aquí — pendientes urgentes

1. ~~[Tarea de configuración inicial ya hecha, p. ej. "Rellenar usuario de
   la plataforma en CLAUDE.md"]~~ — ✅ hecho.
2. ~~[Otra tarea inicial ya hecha, p. ej. "Decidir qué email/alias usar
   para cuentas de prueba"]~~ — ✅ hecho, [detalle: alias usado].
3. ~~[Otra tarea inicial ya hecha, p. ej. "Crear cuentas de prueba A y
   B"]~~ — ✅ hecho, ambas creadas en `[DOMINIO_DE_REGISTRO]` (ver tabla
   de abajo), listas para pruebas cruzadas de IDOR/auth.
4. [Tarea pendiente, p. ej. "Recon inicial del wildcard
   *.DOMINIO_PRINCIPAL"] (ver `RECON.md`, sin arrancar todavía).
5. [Tarea pendiente, p. ej. "Primera pasada sobre ACTIVO_PRIORITARIO —
   mayor superficie de cuenta propia del scope, prioridad 1 según
   CLAUDE.md"].

---

## Cuentas de prueba activas

| Cuenta | Email | Password | Ecosistema | Notas |
|---|---|---|---|---|
| A | [CREDENCIALES CUENTA A — email] | [CREDENCIALES CUENTA A — password] | [dominio/ecosistema] | Creada [fecha]. |
| B | [CREDENCIALES CUENTA B — email] | [CREDENCIALES CUENTA B — password] | [dominio/ecosistema] | Creada [fecha]. Para pruebas cruzadas de IDOR/auth con cuenta A. |

> 🔒 Añade tantas filas como cuentas de prueba tengas (C, D...) según lo
> necesite el programa (por ejemplo, distintos niveles de suscripción o
> roles). Recuerda: este archivo contiene credenciales reales — nunca lo
> subas a un repositorio compartido o público sin redactar antes.

---

## Hallazgos (confirmados y descartados)

| Fecha | Target | Tipo | Severidad | Estado |
|---|---|---|---|---|
| [fecha] | `[activo]` — `[endpoint/método]` | [tipo de vulnerabilidad, p. ej. IDOR/BOLA] | [severidad estimada] | `[!]` confirmado, reproducido de principio a fin múltiples veces, reporte final listo en `reportar/vulnN.md`, pendiente de revisión del hunter y envío |
| [fecha] | `[activo]` — `[endpoint/método]` | [tipo] | [severidad] | `[R]` reportado — enviado a [PLATAFORMA] (confirmado por el hunter, [fecha]) |
| [fecha] | `[activo]` — `[endpoint/método]` | [tipo] | — | `[ ]` pendiente de investigar |

> Añade una fila por cada hipótesis/hallazgo investigado, aunque termine
> descartado — mejor tenerlo aquí con una línea explicando por qué no vale,
> que volver a perder tiempo investigándolo dentro de unas semanas.

---

## Estado por target

| Target | Tier | Estado | Hallazgo |
|---|---|---|---|
| `[activo 1]` | [Tier] | `[x]` recon + Fase 2 completadas — [resumen breve de qué se hizo y qué se concluyó] | — |
| `[activo 2]` | [Tier] | `[~]` recon completada, [detalle de lo hecho hasta ahora y lo que falta] | — |
| `[activo 3]` | [Tier] | `[ ]` sin empezar todavía | — |
| `*.[DOMINIO_PRINCIPAL]` (wildcard) | [Tier] | `[~]` recon activa amplia completada ([N] subdominios fingerprinteados en total), varios candidatos investigados y descartados, [N] hallazgo(s) confirmado(s) | `reportar/vulnN.md` |

---

## Investigación en curso: [NOMBRE DE LA LÍNEA DE INVESTIGACIÓN] — [ESTADO: EN CURSO / BLOQUEADA] ([fecha])

**Hallazgo de superficie nueva / hipótesis en curso.** [Descripción de qué
se está investigando y por qué parece prometedor — de dónde salió la pista
(p. ej. un feature flag visto en un bundle JS, un endpoint nuevo
descubierto en recon), qué páginas/endpoints están involucrados.]

### [Subsección: detalle técnico relevante, p. ej. "Bug de formato resuelto" o "Cómo se llegó al endpoint real"]

[Aquí documenta cualquier detalle técnico no obvio necesario para
reproducir esta línea de investigación — formatos exactos de petición,
prefijos/headers necesarios, hashes o identificadores de operación
extraídos de bundles, etc. Este es exactamente el tipo de detalle que,
si no se documenta aquí, se acaba re-descubriendo desde cero la próxima
sesión.]

### Resultado de las pruebas ([fecha], con [contexto: p. ej. "hashes/valores correctos"])

- **[Prueba 1]** con [parámetro] inventado → [resultado exacto obtenido,
  código de error, mensaje].
  - **Control decisivo**: [variación de la prueba con un control — por
    ejemplo, mismo test pero con un identificador que sí coincide con la
    sesión llamante] → [resultado].
  - **Control 2**: [otra variación, p. ej. repetido desde la sesión de la
    Cuenta B en vez de A] → [resultado].
  - Conclusión: [qué demuestra la combinación de estos resultados —
    normalmente: si el control positivo y negativo dan el mismo resultado,
    el check que se buscaba no depende de lo que se pensaba].
- **[Prueba 2]** → [resultado, con nota de si hay algún error no manejado
  interesante pero sin impacto real — recordar que "mensaje verbose sin
  fuga de info" normalmente cae en las exclusiones de scope, no
  reportable por sí solo].

### Bloqueo real — requiere decisión del hunter

[Si la línea de investigación está bloqueada, explica exactamente por qué
(falta de un recurso/entitlement concreto, requiere gasto de dinero real,
requiere una acción irreversible) y qué decisión concreta necesita tomar
el hunter para desbloquearla. Recordar: cualquier gasto de dinero real o
acción irreversible requiere confirmación explícita del hunter, nunca se
decide unilateralmente.]

Pendiente de que el hunter decida si:
- (a) [opción A, p. ej. "activar un recurso de pago real para completar el test"], o
- (b) [opción B, p. ej. "cerrar esta línea de investigación aquí, documentada pero sin explotar, y priorizar otra superficie"].

---

## Candidatos descartados en Fase 2 ([fecha])

- **`[endpoint/parámetro investigado]`** ([activo], [cómo se descubrió])
  — [parámetro sospechoso identificado, por qué parecía candidato a
  IDOR/otro fallo]. Probado con [metodología de control usada, p. ej.
  "control riguroso antes/después: se cambió un dato verificable en la
  cuenta B, y se repitió la consulta con el ID de B pero desde la sesión
  de A"] → [resultado: siguió devolviendo el dato de la propia sesión, sin
  cambios]. Confirma que el parámetro se ignora por completo server-side,
  la identidad se deriva solo de la sesión — **no es IDOR.**
- **`[otro endpoint investigado]`** — [descripción de la prueba y
  resultado, mismo nivel de detalle que el anterior]. **Sin impacto real,
  no hay [tipo de vulnerabilidad] aquí.** Nota técnica reutilizable: [
  cualquier detalle de implementación necesario para repetir este test en
  el futuro, p. ej. "el identificador se re-cifra en cada petición —
  cualquier test futuro debe usar uno recién obtenido, no uno de una
  lectura anterior"].

## Candidatos descartados en Fase 2 ([fecha], verificado en vivo por el hunter)

Todos estos parecían seguir el mismo patrón que [un hallazgo ya
confirmado], pero al verificarlos con sesión real **no tienen impacto
real** — quedan descartados, no reportar salvo que aparezca nueva
evidencia:

- **`[endpoint]`** ([activo]) — [parámetro sospechoso] se ignora
  completamente server-side: probado con [valores probados: ID de A, ID de
  B, uno inventado, vacío] → **respuesta idéntica en todos los casos**. No
  es IDOR, no hay dato de cuenta expuesto.
- **`[otro endpoint/operación]`**: [descripción] — [conclusión: backend
  bien diseñado en este punto / sin superficie explotable].
- **[Otra hipótesis probada y descartada, con su motivo]**.

## Candidatos de Fase 1 aún sin verificar

- `[endpoint/URL]` — [nota de por qué no se ha verificado todavía, o por
  qué no hace falta verificarlo por separado — p. ej. "no es un endpoint
  de API real, es el prefetch interno del framework; el backend real de
  esa página ya está cubierto en otro punto"]. Cerrado / pendiente según
  aplique.

## Notas técnicas reutilizables

- **[Título de la técnica/limitación, p. ej. "Si el MCP de navegador no
  está disponible en una sesión"]**: [descripción del problema y la
  solución alternativa encontrada — mantener el nivel de detalle
  suficiente para que un agente/sesión futura pueda aplicarlo
  directamente sin re-investigar].
- **[Otra técnica, p. ej. "Rellenar formularios de login con JS puro
  dispara la protección anti-bot"]**: [descripción del bloqueo observado
  (código de error, mensaje) y la solución que funcionó, p. ej. usar
  eventos reales de CDP en vez de manipulación directa del DOM]. **Usar
  siempre [la solución encontrada] en este programa.**
- **[Otra nota, p. ej. "Para pruebas cross-cuenta que necesiten dos
  sesiones simultáneas"]**: [descripción del problema de estado
  compartido (cookies compartidas por todo el perfil del navegador) y la
  solución (contextos de navegador aislados, etc.)].
- **[Otra nota, p. ej. fricción esperada del programa, como verificación
  extra por email en cada login]**: [descripción de la fricción y cómo
  gestionarla — no es un fallo, es comportamiento normal a asumir en la
  metodología de pruebas de este programa].
- **[Nota de riesgo de concurrencia entre agentes, si aplica]**: [qué pasó
  exactamente, y la mitigación aplicada].
- **[Cualquier limitación del entorno de red/sandbox descubierta]**: [p.
  ej. si `curl` está bloqueado por el WAF del target y hay que usar
  siempre un navegador real].
- **[Cualquier matiz de comportamiento del propio endpoint que sea fácil
  de malinterpretar]**: [p. ej. diferencia entre "cero cookies" y "cero
  cookies de sesión/login" — importante para no sobre-reportar o
  sub-reportar un hallazgo].
