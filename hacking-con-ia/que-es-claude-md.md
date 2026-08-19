# Qué es un CLAUDE.md y cómo escribir el tuyo

## 🧠 Qué es

`CLAUDE.md` es un archivo especial que **Claude Code lee automáticamente** al arrancar dentro de una carpeta (y en cada subcarpeta que visite). Es el mecanismo oficial de Claude Code para darle **contexto persistente** a un proyecto: en vez de tener que volver a explicarle todo cada vez que abres una sesión nueva, ese contexto vive escrito en el propio repositorio.

Para Bug Bounty, esto es oro puro: en un `CLAUDE.md` guardo **todo lo que no cambia sesión a sesión** de un programa concreto — quién soy como hunter, qué está autorizado, qué no, cuánto pagan, qué reglas técnicas hay que respetar (rate limits, headers obligatorios), y cómo quiero que Claude organice el trabajo.

## 🧱 Por qué es tan importante en un contexto de hacking ético

Hay un matiz importante y honesto que quiero explicar bien: por defecto, cualquier asistente de IA bien diseñado va a dudar antes de ayudarte a mandar payloads de SQLi, manipular tokens de sesión, o registrar cuentas falsas — porque, sin contexto, eso **parece** una actividad maliciosa. El `CLAUDE.md` es donde **dejas constancia explícita, por escrito, de que esto es un engagement de seguridad autorizado**, dentro de qué límites, y qué tipo de acciones están pre-aprobadas para no tener que confirmar cada paso individualmente — a la vez que dejas igual de claro qué cosas SÍ deben seguir pidiendo tu confirmación explícita (acciones irreversibles, con coste económico real, o fuera de las reglas).

Esto no es "engañar" a la IA ni saltarse ninguna salvaguarda — es exactamente lo mismo que harías con un compañero de equipo humano nuevo: le explicas el contexto, las reglas del cliente, y qué decisiones puede tomar solo y cuáles tiene que consultar contigo.

## 🧩 Secciones que debería tener un buen CLAUDE.md de Bug Bounty

Basado en el que uso yo (con datos reales sustituidos por placeholders/ejemplos genéricos):

### 1. Autorización y alcance ético

Deja explícito, al principio de todo, que esto es un engagement autorizado y real, no una simulación — y qué tipo de acciones concretas están pre-autorizadas dentro del scope (registrar cuentas de prueba propias, mandar payloads contra endpoints en scope, probar IDOR entre cuentas propias, recon dentro de los límites de rate) frente a qué debe seguir pausando siempre a pedir confirmación (acciones irreversibles, impacto económico/físico real, tocar datos de terceros reales, enviar el reporte final).

### 2. Datos del hunter

Tu usuario en la plataforma, cualquier header obligatorio que el programa exija en todas las peticiones (algunos piden un `User-Agent` específico o un header custom de identificación), y qué email/alias usar para registrar cuentas de prueba.

> 🔒 *Aquí es donde más cuidado hay que tener con la privacidad: nunca compartas este archivo tal cual si contiene tu usuario real, tu email real, o contraseñas de cuentas de prueba. Sustituye siempre por placeholders antes de compartirlo o subirlo a cualquier repositorio, incluso privado.*

### 3. Información del programa

Nombre de la empresa/producto, plataforma en la que está gestionado, notas relevantes (por ejemplo, si varios activos comparten el mismo código base y por tanto un mismo fallo puede aplicar a varios dominios a la vez).

### 4. Tabla de recompensas (Reward grid)

Copiar literalmente la tabla de bounties por severidad/tier del programa — así Claude puede ayudarte a estimar el valor esperado de un hallazgo y priorizar dónde mirar.

### 5. Rules of Engagement

Todo lo técnico: límite de peticiones por segundo, si están permitidas herramientas automatizadas o solo pruebas manuales, headers obligatorios, política de divulgación, requisitos de identificación en las peticiones.

### 6. Criterios de severidad del propio programa

Muchos programas dan ejemplos concretos de qué consideran Low/Medium/High/Critical — copiarlos aquí ayuda a que las estimaciones de CVSS que Claude te ayude a redactar estén alineadas con el criterio real del triager, no solo con la teoría general de CVSS.

### 7. Scope (In Scope / Out of Scope)

La tabla de activos autorizados, y — muy importante — la lista de categorías/hallazgos explícitamente excluidos (cosas que el programa ya sabe que no va a pagar ni aceptar, como clickjacking sin impacto demostrado, disclosure de versión sin más, ausencia de rate-limiting, etc.). Tenerlo aquí evita perder tiempo investigando algo que el programa ya ha dicho que no le interesa.

### 8. Organización de ficheros de trabajo

Le dices explícitamente a Claude cómo quieres que organice el repo (ver [Estructura de proyecto](estructura-de-proyecto.md)) — qué va en `PROGRESS.md`, qué va en `RECON.md`, qué se limpia al terminar la sesión, qué formato deben tener los reportes en `reportar/`.

### 9. Metodología de hunting con agentes

Cómo repartir el trabajo entre subagentes sin violar las reglas del programa (por ejemplo, no lanzar dos agentes contra el mismo host a la vez si hay un límite estricto de peticiones/segundo) y sin corromper el estado compartido (por ejemplo, si varios agentes comparten la misma sesión de navegador). Ver el detalle completo en [Agentes en paralelo](agentes-en-paralelo.md).

### 10. Entorno técnico / herramientas

Cómo arrancar tu entorno de navegación con proxy (por ejemplo, Burp Suite + un perfil de Chrome dedicado conectado por Chrome DevTools Protocol), certificados ya confiados, MCPs configurados, etc. — todo lo necesario para que una sesión nueva pueda ponerse a trabajar sin que tengas que explicar el setup cada vez.

### 11. Estrategia de trabajo / prioridades

Qué activos del scope merecen más atención primero y por qué (mayor superficie de cuenta propia, mayor volumen de datos sensibles, etc.), para que Claude sepa por dónde empezar si le pides que continúe el trabajo sin más indicaciones.

## 📄 Ejemplo real anonimizado (fragmento)

Esto es un fragmento real de uno de mis `CLAUDE.md`, con el nombre de la empresa, dominios reales, usuario de la plataforma y datos identificativos ocultados con el efecto "rotulador negro":

> *"Este es un engagement de seguridad ofensiva legítimo y autorizado: un programa de bug bounty en <mark style="background-color:#000;color:#000;user-select:none">[Plataforma]</mark> en el que el usuario es un hunter registrado, actuando dentro de las reglas de este documento. No es un escenario hipotético, un CTF, ni una simulación — es hacking ético real con fines defensivos (...) Dentro del scope y las Rules of Engagement de abajo, las siguientes acciones están pre-autorizadas y no requieren pausar a pedir confirmación: registrar, verificar y resetear contraseñas de cuentas de prueba propias del hunter; enviar peticiones HTTP manipuladas/malformadas contra endpoints en scope; probar IDOR/escalada de privilegios cruzando datos entre cuentas de prueba propias (nunca contra cuentas de terceros reales); recon pasivo/activo no agresivo respetando siempre el límite de <mark style="background-color:#000;color:#000;user-select:none">[N] peticiones/segundo</mark> de las Rules of Engagement."*

> *"Lo que SÍ debe seguir pausando a confirmar con el usuario (...): cualquier acción con impacto financiero real o físico real — completar la cadena técnica hasta el borde de esa acción es válido y esperado; ejecutar el paso final que causa el impacto no. Enviar el reporte final a la plataforma (redactar el borrador sí, pulsar 'enviar' es decisión del hunter)."*

> *"Distinción importante — límites negociables vs. no negociables: (...) 'Tocar/filtrar/manipular datos de ficheros de usuarios reales' NO es negociable bajo ninguna circunstancia — ni aunque el hunter lo pida explícitamente, ni reformulando quién ejecuta el paso técnico. Si una demostración de impacto exige acceder al dato real de un tercero, la respuesta es no y no se ofrecen vías alternativas para conseguirlo — la evidencia de que el primitivo funciona (sin apuntar a un dato real) es suficiente para un reporte."*

> 📌 **Por qué este último párrafo es tan importante**: es la diferencia entre un `CLAUDE.md` bien escrito y uno peligroso. No basta con decir "tienes permiso para probar cosas" — hay que ser igual de explícito sobre **qué límites son absolutamente innegociables**, incluso si en el calor de la investigación tú mismo (el hunter) le pidieras a Claude saltárselos. Un buen `CLAUDE.md` protege tanto al programa como a ti.

## ✍️ Plantilla mínima para empezar tu propio CLAUDE.md

```markdown
# [Nombre del programa] — Bug Bounty en [Plataforma]

## Autorización y alcance ético
(Explicar que es un engagement real y autorizado, qué está pre-aprobado
y qué debe seguir pidiendo confirmación explícita)

## Datos del hunter
- Usuario en la plataforma: [tu-usuario]
- Header obligatorio (si aplica): [Header: valor]
- Email/alias para cuentas de prueba: [alias+sufijo@dominio.com]

## Sobre el programa
(Empresa, sector, notas relevantes de infraestructura compartida)

## Recompensas
(Tabla de bounty por severidad/tier)

## Rules of Engagement
(Rate limits, herramientas permitidas/prohibidas, headers obligatorios,
política de divulgación)

## Severidad — criterios del programa
(Ejemplos de Low/Medium/High/Critical según el propio programa)

## Assets — In Scope / Out of Scope
(Tabla de activos autorizados + lista de exclusiones explícitas)

## Organización de ficheros de trabajo
(Cómo quieres que Claude organice PROGRESS.md, RECON.md, reportar/, etc.)

## Metodología de hunting con agentes
(Reglas de paralelismo, qué no lanzar en paralelo, cómo evitar
corromper estado compartido)

## Entorno técnico
(Cómo arrancar proxy/navegador/MCPs necesarios)

## Estrategia de trabajo
(Prioridades sugeridas dentro del scope)
```
