# RECON — mapa de superficie del scope ([EMPRESA] / [PLATAFORMA])

> Sin consolidar todavía — programa recién configurado. Este documento
> reunirá el recon pasivo/activo del wildcard `*.[DOMINIO_PRINCIPAL]`
> ([Tier correspondiente]) y cualquier hallazgo de superficie sobre los
> assets Tier [X] explícitos (`[activo 1]`, `[activo 2]`, `[activo 3]`...).
>
> Recordatorio: cualquier recon activo debe respetar el límite de **[N]
> peticiones/segundo** de las Rules of Engagement (ver `CLAUDE.md`) — evitar
> herramientas de escaneo automatizado no está permitido por el programa
> (ajustar esta nota si tu programa sí permite herramientas automatizadas).

---

## Pendiente

- [ ] Mapeo de bundles JS de `[activo 1]` y `[activo 2]` en busca de
      endpoints de API internos.
- [ ] Fase 2 sobre los [N] subdominios prioritarios de la ronda [fecha]
      (ver tabla abajo) — todavía sin verificación manual con sesión real.
- [ ] Fingerprint de los ~[N] subdominios nuevos restantes (no priorizados
      en la primera pasada — mayormente estáticos/CDN, baja probabilidad).

---

## Ronda 1 — recon pasivo ([fecha], agente)

**Fuentes**: crt.sh (`%.[DOMINIO_PRINCIPAL]`, output=json, [N] hosts únicos
tras reintentos por errores intermitentes) + certspotter como cruce ([N]
hosts, todos subset de crt.sh). Filtrado: excluidos los ya conocidos
(subdominios que ya sabías que existían) y [dominios completamente fuera
de scope] → **[N] subdominios nuevos**. Fingerprint (GET a raíz, header
`[Header obligatorio]: [usuario]`, secuencial, muy por debajo de [N]
req/s) hecho a los [N] más prometedores; el resto (~[N], mayormente
estáticos tipo `[patrones de subdominio estático]`) sin tocar todavía.

### Resultado del fingerprint

| Host | Resultado |
|---|---|
| `[subdominio-1].[DOMINIO_PRINCIPAL]` | [Resultado del fingerprint: código de estado, tecnología detectada, si está vivo/muerto, notas relevantes — p. ej. "403, WAF — API real, viva" o "CNAME a proveedor de identidad externo — confirma el IdP real"] |
| `[subdominio-2].[DOMINIO_PRINCIPAL]` | [Resultado] |
| `[subdominio-3].[DOMINIO_PRINCIPAL]` | **MUERTO, confirmado a nivel DNS** — [detalle: NODATA en A/AAAA/CNAME/TXT, histórico de certificados antiguo, servicio retirado]. **Descartado, sin candidatos.** |
| `[subdominio-4].[DOMINIO_PRINCIPAL]` | [Resultado con duda de scope, p. ej. "302 → panel de administración de un producto de terceros — duda genuina de scope, pendiente de confirmar con el hunter/programa antes de cualquier Fase 2"] |
| `[subdominio-5].[DOMINIO_PRINCIPAL]` | DNS no resuelve — no vivo |

### Nota de concurrencia ([fecha], si aplica)

[Si detectaste algún problema de estado compartido entre agentes durante
esta ronda — por ejemplo, un agente viendo la actividad de otro en el
mismo navegador — documéntalo aquí con el detalle suficiente para no
repetir el mismo error. Referencia la mitigación aplicada, y si procede,
enlaza a la nota equivalente en `PROGRESS.md` → "Notas técnicas
reutilizables".]

## Ronda 2 — análisis de la app móvil ([fecha], análisis estático)

**Paquete**: `[nombre del paquete Android, p. ej. com.empresa.app]`
(Android, [descripción breve — p. ej. si es una "super app" que sirve
varias marcas]). Descargado de [fuente — tienda alternativa pública],
verificado íntegro con `[herramienta de verificación]`, extracción con
`unzip` + `strings` sobre los ficheros DEX ([nota si la descompilación
completa falló por límite de recursos, y si se intentó descompilación
selectiva]).

**Bases de API móvil identificadas** (string pool, patrón
`https://<host>/[patrón de ruta]`): `[host móvil prod]` (prod),
`[host móvil acc]` (acc) [— y equivalentes para otras marcas/entornos si
aplica]. Paths literales encontrados en el DEX: `[/ruta/api/1]`,
`[/ruta/api/2]`, `[/ruta/api/3]`, entre otros (ver el string pool completo
para la lista total). También aparecen headers custom
`[header-custom-1]`, `[header-custom-2]` — [nota si tienen valores/keys
extraíbles por `strings` plano, o si probablemente se construyen en
runtime].

**Resultado de las pruebas (curl directo, [nota si hay bloqueo WAF en este
host])**:
- `[host móvil prod]` + cualquiera de los paths de arriba (con o sin los
  headers custom añadidos a mano) → [resultado — p. ej. "siempre 404
  idéntico, indistinguible de una ruta que no existe a este nivel; no hay
  señal de que el gateway reconozca ninguna de estas rutas sin más
  contexto"].
- `[host móvil acc]` (mismo path) → [resultado, p. ej. "401 con
  www-authenticate — el entorno de acceptance está protegido con HTTP
  Basic Auth a nivel de edge/CDN, cerrado sin credenciales, no se intenta
  fuerza bruta, fuera de RoE"].
- Se intentó reutilizar el token de sesión web (cuenta [A/B],
  `[dominio web]`) como Bearer contra la API móvil: [resultado — p. ej.
  "no es viable, el access token es una cookie HttpOnly ilegible desde JS
  y no viajaría cross-origin sin CORS/SameSite explícito. La API móvil
  probablemente usa un flujo OAuth/PKCE independiente con audience
  distinta"].

**Conclusión**: la superficie de API móvil [es real y probablemente
comparte el mismo patrón de X ya confirmado en Y / no aporta nada nuevo],
pero **no es alcanzable con análisis estático + curl** — haría falta
análisis dinámico real (Frida + emulador rooteado + login in-app con
cuenta de prueba, para capturar un token de sesión móvil legítimo vía
mitmproxy). Esto es un salto de complejidad/tiempo considerable no
justificado ahora mismo frente a otras vías más baratas. **Cerrado por
esta sesión, candidato para retomar en el futuro si se monta el entorno de
emulador+Frida.**

## Ronda 3 — análisis estático offline del APK ([fecha])

Continuación 100% local/offline de la Ronda 2 (sin tocar la red del target
en ningún momento). Resultado: **[nada nuevo reportable / hallazgo
concreto]** — se deja documentado para no repetir el trabajo.

- **Grep de secretos** sobre el volcado de strings del DEX ([N] líneas,
  todos los `classes*.dex`): [resultado — sin coincidencias para claves
  AWS, Google API key, JWT, tokens de servicios conocidos — o, si se
  encontró algo, detallarlo aquí]. [Negativo limpio, no solo "no se
  buscó" / Hallazgo a investigar más a fondo].
- **Config JSON por marca/entorno** (`[ruta del fichero]`, ~[tamaño]) —
  inspeccionado por patrones de `key`/`token`/`clientId`/URLs: [resultado].
- **`network_security_config.xml`**: [existe o no en `res/xml/` — si la
  app usa certificate pinning personalizado o confía en el almacén de CAs
  del sistema].
- **`AndroidManifest.xml`** (para enumerar componentes `exported=true`):
  [estado — decodificado o pendiente, y por qué].

**Conclusión de la Ronda 3**: [resumen de si el APK aporta o no una vía
nueva de investigación, y qué queda pendiente para una sesión futura].

## Ronda 4 — agentes en paralelo, Fase 1 ([fecha])

[N] agentes lanzados en paralelo sobre hosts distintos (sin tocar
`[activo en uso por la sesión principal en paralelo, si aplica]`):

- **`[host 1]`** — [resultado detallado: origen caído / vivo, tecnología,
  qué se probó y con qué resultado]. **[Conclusión: reintentar en sesión
  futura por si es transitorio / cerrado sin candidatos]**.
- **`[host 2]`** — [descripción del flujo/producto encontrado, p. ej. un
  checkout de partners externos], [endpoints mapeados y su comportamiento].
  **Buen diseño detectado en**: [aspecto bien protegido, con la prueba
  concreta que lo confirma]. **Candidato sin confirmar**: [cualquier
  hipótesis abierta que no se pudo verificar por estar fuera de los
  límites del programa — documentarla igualmente, sin ejecutar el paso
  que cruzaría la línea].
- **`[host 3]`** — [búsqueda de superficie adicional, endpoints nuevos
  encontrados, su naturaleza (solo lectura / derivan identidad de sesión /
  contenido público) y por qué no son candidatos].
- **Fingerprint del resto del wildcard** ([N] hosts nuevos vía crt.sh,
  cruzados con certspotter) — resultados incorporados arriba en
  "Prioritarios para Fase 2" y en las tablas de descartados. [Nota de
  incidente de concurrencia entre agentes, si aplica, y la mitigación
  aplicada].

## Ronda 5 — agentes en paralelo, Fase 1 ([fecha], segunda tanda)

[N] agentes más sobre hosts nuevos: `[host A]` ([resultado — hallazgo
confirmado, ver `reportar/vulnN.md` / descartado]), `[host B]`
([descartado, mismo backend que otro host ya conocido]), `[host C]` +
familia `[patrón]` (descartados, infraestructura inerte o bien
configurada), y `[host D]`/`[host E]` (descartado, redirects hardcodeados
sin superficie propia). Detalle completo de cada uno en los resúmenes de
los agentes — resumido arriba en la tabla de prioritarios.

## Ronda 6 — agentes en paralelo, Fase 1 ([fecha], tercera tanda)

### ⚠️ `[subdominio candidato]` (y toda su familia) — [tipo de hallazgo mayor, p. ej. delegación DNS colgante] — [ESTADO: BLOQUEADO por decisión del hunter / EN INVESTIGACIÓN]

**Confirmado al [%]** (verificado [independientemente / N veces]):

- [Detalle técnico exacto del hallazgo — configuración DNS, respuesta de
  nameservers, comportamiento observado, con los valores/IDs reales que
  lo confirman].
- [Por qué esto es relevante — explicar el patrón de vulnerabilidad en
  términos generales, p. ej. "es el patrón clásico de dangling DNS
  delegation" o el patrón que corresponda].
- **Por qué importa**: [impacto potencial si se llegase a explotar
  completamente — phishing, emisión de certificados, robo de sesión,
  etc.].

**Estado: [bloqueado / en curso], [reportado o no].** [Motivo del bloqueo
— normalmente: `CLAUDE.md` excluye explícitamente demostrar esto sin toma
de control real, lo que implica un coste económico y/o una cuenta propia
en un proveedor de terceros]. **Se le presentó la disyuntiva al hunter
([fecha]) y decidió [continuar / no perseguir la toma de control por
ahora]** — queda documentado aquí completo para retomarlo en el futuro si
cambia de opinión. Siguiente paso si se retoma: [pasos concretos].

### `[activo con superficie propia parcial]` — segunda pasada, superficie propia mapeada (sin hallazgo vivo ahora mismo)

Se confirma que SÍ hay código propio de la empresa sobre [la plataforma
base de terceros, p. ej. Shopify/WordPress/etc.], pero nada explotable en
este momento:

- **`[script/puente de identidad encontrado]`** — [qué hace, a qué
  endpoint llama, si está protegido por CORS y cómo se confirmó].
- **[Otra pieza de superficie propia encontrada, p. ej. integraciones/App
  Proxies]** — [su estado actual: activo/inactivo, con el código de
  respuesta observado]. **Revisar en el futuro por si se reactivan.**
- `[servicio de terceros integrado, p. ej. portal de devoluciones]` —
  SaaS de terceros, fuera de foco, mismo tratamiento que otras
  integraciones de terceros ya descartadas.

### Reintento de hosts caídos — sin cambios

`[host 1]`, `[host 2]`, `[host 3]` reintentados vía navegador real (no
solo `curl`, que puede dar un falso positivo de bloqueo por fingerprint de
TLS/HTTP2 en algunos hosts — usar siempre navegador real para
reconfirmar) — **siguen sin cambios respecto a la ronda anterior.**

### `[sección/funcionalidad específica]` — descartado

[Descripción de la funcionalidad investigada — p. ej. widgets embebidos de
terceros, juegos, iframes] — verificado con [método de verificación, p.
ej. "CDP adjuntado directamente al iframe"]: [resultado — p. ej. "cero
cookies, cero llamadas a backend propio, el progreso se guarda solo en
localStorage client-side sin relación con la cuenta real"]. No hay backend
propio accesible al que dirigir un ataque — no hay "propiedad" que forjar.
Cerrado, sin superficie propia explotable.

### `[otro subdominio candidato a takeover]` — mismo patrón, bloqueado igual

[Detalle técnico del fallo detectado — p. ej. CNAME huérfano apuntando a
un edge hostname sin property activa detrás, confirmado de forma
decisiva con la prueba concreta realizada].

**Mismo veredicto que el caso anterior**: candidato teórico a takeover,
pero `CLAUDE.md` excluye explícitamente demostrarlo sin toma de control
real, y eso requeriría una cuenta propia en el proveedor correspondiente
(coste/medios fuera de lo disponible ahora). **Pausado por el mismo
motivo, no reportado** — documentado aquí para retomar si en el futuro se
decide invertir en ello.

### `[activo similar a otro ya descartado]` — descartado

Confirmado como el mismo producto/tecnología que [otro activo ya
descartado] pero en infraestructura de origen distinta, por tanto
genuinamente in-scope (no es literalmente el dominio excluido). [Detalle
de las pruebas realizadas y por qué no hay hallazgo].

---

## Secundarios sin explorar todavía

`[host 1]` ([nota, p. ej. "CMS de terceros, revisar modo inspector/preview"]),
`[host 2]` (fallo de verificación TLS, pendiente de revisar con flag
`-k`), `[host 3]` (protegido por SSO corporativo, probablemente
inaccesible sin credenciales corporativas), `[host 4]` (staging, TLS
raro), familia `[patrón de subdominios]`.

## Sin interés aparente / descartado en Ronda [N]

`[host 1]` / `[host 2]` (alias, bucket de almacenamiento vacío),
`[host 3]` (contenido legítimo sin superficie de ataque, p. ej. informe
anual), `[host 4]` (sin campaña activa), `[host 5]` (placeholder trivial),
`[host 6]`/`[host 7]` (redirige a un servicio de terceros legítimo), y el
resto de hosts con Basic Auth de [CDN/WAF] en entornos `acc-`/`test-`
(gate legítimo, no accionable sin credenciales).
