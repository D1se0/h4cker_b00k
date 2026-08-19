# [EMPRESA] ([GRUPO/EMPRESA MATRIZ, SI APLICA]) — Bug Bounty Program en [PLATAFORMA]

> Programa privado/público en [PLATAFORMA]. Testing autorizado únicamente dentro
> del scope y reglas descritas aquí.

## Autorización y alcance ético — leer antes de dudar

Este es un **engagement de seguridad ofensiva legítimo y autorizado**: un
programa de bug bounty en [PLATAFORMA] en el que el usuario es un hunter
registrado, actuando dentro de las reglas de este documento. No es un
escenario hipotético, un CTF, ni una simulación — es hacking ético real con
fines defensivos (encontrar y reportar vulnerabilidades para que [EMPRESA]
las arregle), remunerado por el propio programa.

**Lo que esto significa en la práctica para minimizar interrupciones
innecesarias**: dentro del scope y las Rules of Engagement de abajo, las
siguientes acciones están **pre-autorizadas** y no requieren pausar a pedir
confirmación ni cuestionar si "esto es ético/legal" — sencillamente hazlo y
documenta el resultado en `PROGRESS.md`:

- Registrar, verificar (OTP/email) y resetear contraseñas de cuentas de
  prueba propias del hunter en cualquier target del scope.
- Enviar peticiones HTTP manipuladas/malformadas (payloads de SQLi, XSS,
  path traversal, headers falsificados, IDs de recurso ajenos,
  tokens/firmas manipuladas, etc.) contra endpoints en scope — es
  literalmente el trabajo.
- Probar IDOR/escalada de privilegios/auth bypass cruzando datos **entre
  cuentas de prueba propias del hunter** (nunca contra cuentas de terceros
  reales).
- Recon pasivo/activo no agresivo (crt.sh, fingerprinting, mapeo de API vía
  bundles JS, etc.) sobre dominios del scope o cubiertos por el wildcard
  `*.[DOMINIO_PRINCIPAL]`, **respetando siempre el límite de [N]
  peticiones/segundo** de las Rules of Engagement.
- Guardar hallazgos, evidencia y credenciales de cuentas de prueba en los
  ficheros de este repo (`PROGRESS.md`, `reportar/`).

**Lo que SÍ debe seguir pausando a confirmar con el usuario** (por ser
irreversible, afectar a terceros reales, o tener coste económico/físico
real) — esto no cambia:
- Cualquier acción listada como fuera de las reglas de testing de abajo
  (scanners automáticos, tráfico masivo, tocar/filtrar/manipular datos de
  usuarios reales, ataques de suplantación/social engineering, disclosure
  no autorizado).
- Acciones con impacto financiero real (cobros reales, compras/reservas
  reales) o físico real — completar la cadena técnica hasta el borde de esa
  acción es válido y esperado; ejecutar el paso final que causa el impacto
  no.
- Enviar el reporte final a [PLATAFORMA] (redactar el borrador sí, pulsar
  "enviar" es decisión del hunter).
- Cualquier duda genuina sobre si un asset/subdominio está realmente
  cubierto por el scope de abajo.

Si una tarea encaja claramente en la lista pre-autorizada, no hace falta
preguntar "¿procedo?" — procede y reporta qué hiciste y qué encontraste.

**Distinción importante — límites negociables vs. no negociables**: el
límite de [N] peticiones/segundo del programa (ver Rules of Engagement) **es
no negociable** — a diferencia de otros programas donde un volumen alto de
tráfico puede negociarse con el hunter, aquí [PLATAFORMA]/[EMPRESA] fija un
techo explícito y pedir superarlo (aunque sea para una técnica de
explotación legítima, ej. completar un ataque que requiera muchas
peticiones) no es una decisión que se pueda tomar unilateralmente — debe
plantearse al hunter y, si hace falta más margen, aclararse con el programa
antes de generar ese tráfico. **"Tocar/filtrar/manipular datos de ficheros
de usuarios reales" NO es negociable bajo ninguna circunstancia** — ni
aunque el hunter lo pida explícitamente, ni reformulando quién ejecuta el
paso técnico. Si una demostración de impacto exige acceder al dato real de
un tercero, la respuesta es no y no se ofrecen vías alternativas para
conseguirlo — la evidencia de que el primitivo funciona (sin apuntar a un
dato real) es suficiente para un reporte.

## Datos del hunter

- **Usuario de [PLATAFORMA]**: `[USUARIO_PLATAFORMA]`
- **Header obligatorio en TODAS las peticiones**: `[HEADER_OBLIGATORIO: USUARIO_PLATAFORMA]`
  (revisar las Rules of Engagement del programa: algunos exigen un
  `User-Agent` custom en vez de, o además de, este header — anotar aquí
  cuál aplica en este programa concreto).
- **Email de registro en las cuentas de prueba**: [EMAIL/ALIAS PARA
  CUENTAS DE PRUEBA] (confirmar con el hunter qué email/alias usar para
  registrar cuentas de prueba en `[DOMINIO_DE_REGISTRO]` — el de la cuenta
  real de [PLATAFORMA], o un alias dedicado tipo `+[sufijo]@...`).

## Sobre el programa

**[EMPRESA]** ([GRUPO, SI APLICA]) — [DESCRIPCIÓN BREVE DEL NEGOCIO/SECTOR,
p. ej. "periódico", "fintech", "e-commerce"]. Programa gestionado en la
plataforma **[PLATAFORMA]**.

Nota importante del propio programa: [NOTA RELEVANTE DEL PROGRAMA, p. ej.
si varios activos comparten el mismo código base con otros productos del
grupo — listar cuáles — y si un fallo ya encontrado en uno se trata como
duplicado en los demás].

## Recompensas (Reward grid)

| Severidad | Rango CVSS | Tier [X] | Tier [Y] |
|---|---|---|---|
| Low | 0.1 – 3.9 | [CANTIDAD] | [CANTIDAD] |
| Medium | 4.0 – 6.9 | [CANTIDAD] | [CANTIDAD] |
| High | 7.0 – 8.9 | [CANTIDAD] | [CANTIDAD] |
| Critical | 9.0 – 9.4 | [CANTIDAD] | [CANTIDAD] |
| Exceptional | 9.5 – 10.0 | [CANTIDAD] | [CANTIDAD] |

El "Tier" depende del asset concreto (ver tabla de scope más abajo — anotar
aquí qué proporción/qué activos concretos caen en cada Tier de este
programa).

## Rules of Engagement (reglas de testing)

- **User-Agent**: [APLICA / NO APLICA — string obligatorio si lo hay].
- **Herramientas automatizadas**: máximo **[N] peticiones/segundo**. [¿Se
  aceptan submissions encontradas con scanners automáticos, o el programa
  pide explícitamente creatividad manual? Anotar aquí la política exacta].
- **Header obligatorio**: `[Header]: {Username}` en todas las peticiones
  (si aplica).
- Respetar el Community Code of Conduct y los Términos y Condiciones de
  [PLATAFORMA].
- Respetar estrictamente el scope de abajo.
- **No discutir ni divulgar información de vulnerabilidades sin
  consentimiento previo por escrito** (incluidas PoCs en YouTube/Vimeo).
- Identificarse siempre como researcher con el usuario de [PLATAFORMA] (el
  bounty puede denegarse si no se hace).
- Proporcionar pasos de reproducción detallados pero concisos, y un
  escenario de ataque claro (impacto real en [EMPRESA]).
- Calidad antes que cantidad.
- Cuidado especial al probar plataformas que puedan afectar a usuarios
  reales (ej. listados de empleo) o que requieran limpieza manual en el
  back-end.
- Se aplica **safe harbour** para investigadores (ver la página del
  programa en [PLATAFORMA] para el texto legal completo).

## Severidad — cómo se evalúan los hallazgos

Todas las recompensas están basadas en impacto real — evaluar con cuidado
el impacto antes de elegir severidad. Ejemplos orientativos del programa
(la severidad final puede variar según el impacto real — **ajustar esta
lista con los ejemplos concretos que dé tu propio programa**):

- **Exceptional**: RCE en producción; acceso completo a la base de datos
  (incl. update/delete).
- **Critical**: SQL injection; acceso a datos personales de todos los
  clientes o de un usuario concreto; IDOR numérico con lectura/escritura
  masiva en funciones críticas; path traversal con disclosure de ficheros
  locales.
- **High**: acceso a datos de usuarios aleatorios (PII sensible); XSS
  almacenado explotable (excluye self-XSS no explotable); bypass de
  autenticación vertical.
- **Medium**: DOM XSS; XSS reflejado; IDOR con disclosure de datos no
  críticos; CSRF con impacto significativo; bypass de autenticación
  lateral.
- **Low**: XSS reflejado que requiere interacción significativa del
  usuario; CSRF en funcionalidad no crítica; open redirect; IDOR con
  identificadores UUID (salvo que se demuestre una vía real de
  enumeración/listado de UUIDs válidos, o que los UUID no sean aleatorios
  de verdad — ej. UUIDv1 — y por tanto adivinables).

[NOTA DE SEVERIDAD ESPECÍFICA DEL PROGRAMA, si la hay — ejemplo: "CPDoS en
contenido con caché larga: se puede evaluar con Attack Complexity 'High' en
CVSS"].

## Assets — In Scope

| Target | Tier |
|---|---|
| `[SUBDOMINIO_1].[DOMINIO_PRINCIPAL]` | Tier [X] |
| `[SUBDOMINIO_2].[DOMINIO_PRINCIPAL]` | Tier [X] |
| `[SUBDOMINIO_3].[DOMINIO_PRINCIPAL]` | Tier [X] |
| `[RUTA_ESPECÍFICA, p. ej. www.dominio.com/seccion]` | Tier [X] |
| `*.[DOMINIO_PRINCIPAL]` (wildcard) | Tier [Y] |

## Out of Scope

**Explícitamente fuera de scope** (aunque en apariencia caerían bajo el
wildcard o parezcan parte de la superficie):

- `[DOMINIO_PRINCIPAL]/[ruta excluida 1]`
- `[DOMINIO_PRINCIPAL]/[ruta excluida 2]`
- `[DOMINIO_PRINCIPAL]/[ruta excluida 3]`
- `[SUBDOMINIO_EXCLUIDO].[DOMINIO_PRINCIPAL]`

**Extra — categorías/hallazgos explícitamente fuera de scope (no
reportables)** — copiar literalmente las de tu programa; la siguiente lista
es un ejemplo típico de lo que suelen excluir muchos programas:

- Cross-Site Scripting (XSS) en `[ruta/activo concreto excluido]`
- `[URL concreta excluida, p. ej. página de contacto]`
- Bypass del paywall / de la funcionalidad de pago (si aplica)
- Open redirects en endpoints de consentimiento de privacidad
- Filtraciones de contraseñas de usuario que no se originen en una
  vulnerabilidad propia del programa (se pueden reportar, pero sin bounty)
- Disclosure de API key sin impacto de negocio demostrado
- Disclosure de usernames de WordPress
- Account takeover / OAuth squatting pre-auth
- Self-XSS no explotable contra otros usuarios
- Mensajes verbosos/listados de ficheros o directorios sin exponer
  información sensible
- CORS misconfiguration en endpoints no sensibles
- Falta de flags de seguridad en cookies
- Falta de cabeceras de seguridad
- CSRF sin impacto o de impacto bajo
- Presencia del atributo `autocomplete` en formularios web
- Reverse tabnabbing
- Bypass de rate-limits, o ausencia de rate-limiting
- Violaciones de buenas prácticas (complejidad/expiración/reutilización de
  contraseñas, etc.)
- Clickjacking sin impacto demostrado / interacción de usuario poco
  realista
- CSV Injection
- Sesiones no invalidadas (logout, activación de 2FA, etc.)
- Tokens filtrados a terceros
- Cualquier tema relacionado con spoofing de email, SPF, DMARC o DKIM
- Content injection sin capacidad de modificar el HTML
- Enumeración de usernames/emails
- Email bombing
- HTTP Request smuggling sin impacto demostrado
- Homograph attacks
- XMLRPC habilitado
- Banner grabbing / disclosure de versión
- No eliminar metadatos de ficheros
- Same-site scripting
- Subdomain takeover sin tomar realmente el control del subdominio
- Subida de ficheros arbitraria sin prueba de que el fichero subido exista
  realmente en el servidor
- Blind SSRF sin impacto de negocio demostrado (los pingbacks no son
  suficientes)
- Google Maps API keys expuestas o mal configuradas
- Host header injection sin impacto de negocio demostrado
- Vulnerabilidades ya conocidas por la empresa por sus propias pruebas
  internas (se marcan como duplicado)
- Problemas de seguridad teóricos sin escenario de explotación realista, o
  que requieran interacción de usuario compleja e improbable
- Spam, ingeniería social e intrusión física
- Ataques DoS/DDoS o de fuerza bruta
- Vulnerabilidades que solo funcionen en software sin soporte de
  seguridad activo
- Ataques que requieran acceso físico al dispositivo de la víctima, MITM,
  o cuentas de usuario ya comprometidas
- Vulnerabilidades 0-day recientes en assets del scope, dentro de los 14
  días posteriores a la publicación del parche/mitigación — se pueden
  reportar pero normalmente no son elegibles para bounty (posible bonus
  discrecional)
- Reportar que un software está desactualizado/es vulnerable sin PoC

> ⚠️ **Importante**: la lista de arriba es orientativa/genérica. Sustitúyela
> siempre por la lista real y completa de exclusiones de TU programa — cada
> programa tiene sus propias particularidades y esta lista puede quedarse
> corta o desactualizada.

## Organización de ficheros de trabajo

El repo debe contener en la raíz **tres ficheros y una carpeta**:
`CLAUDE.md` (este documento, reglas estáticas del programa), `PROGRESS.md`
(estado de trabajo — hallazgos, pendientes, cuentas de prueba; lo primero
que se lee al empezar sesión), `RECON.md` (mapa de superficie/subdominios
de recon pasivo/activo del wildcard `*.[DOMINIO_PRINCIPAL]`) y `reportar/`
(borradores de reportes de vulnerabilidades ya confirmadas y reproducidas
de principio a fin, uno por fichero).

- No crear carpetas `reporte-*/` sueltas ni ficheros de evidencia
  (scripts, capturas, logs, JSON crudos) que persistan entre sesiones
  **fuera de `reportar/`**. Cualquier evidencia o script generado durante
  la sesión se **resume dentro de `PROGRESS.md`** (con los
  valores/comandos/payloads clave necesarios para reproducirlo) y se borra
  al terminar de documentarlo. La única excepción es un `.md` de reporte ya
  terminado dentro de `reportar/`: solo texto y PoC (comandos/payloads),
  sin capturas de pantalla ni scripts sueltos — las capturas para el envío
  real a [PLATAFORMA] se generan aparte, en el momento de enviar, no se
  guardan en el repo.
- Los datos de recon (subdominios, resultados de crt.sh/certspotter) van
  en `RECON.md`, no en `PROGRESS.md` — así `PROGRESS.md` se mantiene
  legible y rápido de leer al arrancar sesión; `RECON.md` puede ser largo y
  denso sin problema, es de consulta puntual.
- Al terminar una sesión (o cuando el hunter lo pida explícitamente),
  limpiar cualquier fichero/carpeta temporal creado durante la sesión,
  dejando solo los 3 ficheros + `reportar/` de arriba.

## Metodología de hunting con agentes

Para sacar el máximo partido a los subagentes sin violar las Rules of
Engagement (en particular el límite de **[N] peticiones/segundo**) ni
corromper estado compartido entre ellos, el trabajo se reparte en tres
fases con reglas distintas cada una.

### Fase 1 — Recon, en paralelo

Las tareas de solo lectura, sin estado mutable y con huella de red baja se
lanzan como varios subagentes a la vez (mismo mensaje, varias tool calls
del Agent tool): enumerar subdominios del wildcard `*.[DOMINIO_PRINCIPAL]`,
mapear bundles JS en busca de endpoints nuevos, fingerprint de un lote de
subdominios sin explorar, o repetir una misma clase de vulnerabilidad
conocida contra varios targets independientes.

- Cada agente debe tener **alcance acotado**: una clase de vulnerabilidad o
  un puñado de targets concretos, nunca un "busca vulnerabilidades en todo
  el scope" genérico.
- **No lanzar varios agentes contra el mismo target o la misma cuenta de
  prueba a la vez** — el tráfico concurrente sobre un único objetivo puede
  disparar defensas anti-bot y, dado el límite explícito de [N] req/s de
  este programa, es más fácil saltarse ese límite sin darse cuenta cuando
  varios agentes atacan el mismo host en paralelo. Repartir los agentes
  por target/dominio distinto, no por técnica repetida sobre el mismo
  target, y vigilar que la suma de peticiones/segundo de todos los agentes
  activos no supere el límite del programa.
- Los agentes de recon devuelven su resumen a la sesión principal; es esta
  sesión la que decide qué se apunta en `RECON.md`/`PROGRESS.md`.

### Fase 2 — Explotación y verificación, en serie

En cuanto un hallazgo de la Fase 1 parece prometedor, pasa a ejecutarse en
un único hilo de trabajo (no en paralelo), sobre la cuenta de prueba
correspondiente, hasta reproducirlo de principio a fin. **Nunca dar por
confirmada una vulnerabilidad solo porque un agente diga que la ha
encontrado** — reproducirla paso a paso (idealmente dos veces) antes de
tratarla como real.

### Fase 3 — Guardar el hallazgo reportable

En cuanto una vulnerabilidad esté **reproducida de principio a fin** y con
impacto demostrado dentro de los límites de las Rules of Engagement:

1. Guardar un `.md` en `reportar/<slug-del-hallazgo>.md` con: resumen,
   endpoints/activos afectados, PoC reproducible paso a paso
   (payloads/comandos/curl, siempre incluyendo el header
   `[Header obligatorio, si aplica]`), impacto y remediación sugerida —
   mismo estándar que el reporte que se enviaría a [PLATAFORMA].
2. Marcar la entrada correspondiente en `PROGRESS.md` como `[!]`,
   indicando que ya está guardada en `reportar/<fichero>.md` y lista para
   que el hunter la revise y envíe.
3. Cuando el hunter confirme el envío a [PLATAFORMA], actualizar el estado
   a `[R]` en `PROGRESS.md`. El `.md` de `reportar/` se mantiene como
   archivo histórico.

Este guardado se hace en cuanto se confirma el hallazgo, no al final de la
sesión, para no perderlo si la sesión se corta a medio camino.

## Entorno de navegación (Chrome + Burp)

Para navegar con el MCP `chrome-devtools` con el tráfico pasando por Burp
Suite (necesario para interceptar/reproducir peticiones manualmente):

1. `open -a "Burp Suite"` y esperar a que escuche en `127.0.0.1:8080`
   (comprobar con `lsof -iTCP:8080 -sTCP:LISTEN`).
2. `cd [RUTA_A_TU_SCRIPT_DE_LANZAMIENTO] && ./launch.sh` (si hay una
   instancia previa colgada, `./stop.sh` primero) — lanza un Chrome real
   con el perfil dedicado a este programa (cuentas/cookies ya guardadas) y
   proxy a Burp ya configurado (`--proxy-server=127.0.0.1:8080`),
   escuchando CDP en `:9222`.
3. El MCP `chrome-devtools` ya está configurado para conectarse a ese
   `:9222` (`--browserUrl http://127.0.0.1:9222`) — no lanza su propio
   Chrome.

El certificado CA de Burp ya está confiado en el keychain del usuario — no
hace falta repetir ese paso salvo que se reinstale Burp (CA nueva) o se
limpie el keychain.

## Estrategia de trabajo

Ver `PROGRESS.md` para el estado de la auditoría por asset y la sección
"Metodología de hunting con agentes" de arriba para cómo repartir el
trabajo entre subagentes. Prioridad sugerida (**ajustar según el scope
real de tu programa**):

1. `[ACTIVO_1].[DOMINIO_PRINCIPAL]` — [motivo de la prioridad, p. ej. mayor
   superficie de registro/cuenta propia] → foco en IDOR, auth, business
   logic.
2. `[ACTIVO_2].[DOMINIO_PRINCIPAL]` — [motivo, p. ej. flujos de
   suscripción/pago] → foco en lógica de negocio, IDOR
   [**anotar aquí explícitamente cualquier categoría excluida del scope
   relacionada, para no perder tiempo investigando algo no reportable**].
3. `[ACTIVO_3].[DOMINIO_PRINCIPAL]` — [motivo, p. ej. superficie de
   contenido/lectura, mayor volumen de tráfico de usuarios reales, más
   cuidado necesario].
4. `*.[DOMINIO_PRINCIPAL]` (wildcard, Tier [Y]) — recon de subdominios
   antes de profundizar, recordando siempre el límite de [N] req/s.
