# Ideas y automatizaciones adicionales

Cosas que ya uso, cosas que estoy explorando, y cosas que tiene sentido probar más adelante para llevar este flujo aún más lejos.

## 🔌 MCPs útiles para este flujo

Los **MCP (Model Context Protocol)** son conectores que le dan a Claude acceso a herramientas externas de forma estructurada. Algunos especialmente útiles para Bug Bounty:

- **MCP de navegador (control de Chrome/Chromium vía DevTools Protocol)**: permite que Claude navegue, rellene formularios con eventos reales (útil para saltarse detección anti-bot basada en manipulación directa del DOM), y capture snapshots del DOM/red — clave para automatizar la fase de recon y exploración dentro de un navegador real con tu proxy (Burp/ZAP) ya configurado.
- **MCP de sistema de ficheros**: ya viene integrado en Claude Code de forma nativa, es lo que permite todo el flujo de `CLAUDE.md`/`PROGRESS.md`/`RECON.md`/`images/`/`temp/`/`reportar/`.
- **MCPs de gestión de proyecto/notas** (si usas alguna herramienta externa para llevar el seguimiento de programas): pueden sincronizar tu `PROGRESS.md` con un tablero visual si trabajas en equipo.

## 🗃️ Un `CLAUDE.md` "base" reutilizable entre programas

Además del `CLAUDE.md` específico de cada programa, tiene sentido mantener un **`CLAUDE.md` de nivel superior** (en la carpeta padre que contiene todos tus proyectos de Bug Bounty) con las reglas que son iguales SIEMPRE, independientemente del programa:

- Tu metodología general de verificación (nunca dar por confirmado sin reproducir dos veces).
- Tu criterio ético no negociable (nunca tocar datos reales de terceros, bajo ninguna circunstancia).
- Tu estructura de carpetas estándar.
- Tu estilo preferido de reportes.

Así, el `CLAUDE.md` específico de cada programa solo necesita añadir lo que cambia: scope, recompensas, reglas técnicas concretas del programa.

## 🧪 Entorno de pruebas separado por programa

Mantener un **perfil de navegador dedicado por programa** (con sus propias cookies/cuentas guardadas) evita mezclar sesiones entre distintos objetivos por error — algo fácil de hacer quien trabaja en varios programas a la vez, y potencialmente arriesgado si terminas mandando una petición al programa equivocado con la sesión equivocada.

## 📊 Llevar un "dashboard" simple de todos tus programas activos

Un archivo (o tablero) de nivel superior que resuma, por programa: estado general, última actividad, número de hallazgos confirmados/reportados/pendientes, y el ID de conversación de Claude Code de cada uno (para poder hacer `claude --resume <ID>` directamente sin tener que recordarlo de memoria).

## 🔁 Plantillas de agente reutilizables

Si sueles lanzar el mismo tipo de agente una y otra vez (por ejemplo, "agente que prueba IDOR sistemáticamente sobre una lista de endpoints"), guardar ese prompt como una plantilla propia (en un fichero de notas, o como un snippet) ahorra tener que redactarlo desde cero cada vez — solo cambias el activo/endpoint objetivo.

## 🧾 Generación automática de changelogs de sesión

Pedirle a Claude, al final de cada sesión, un resumen tipo "changelog" de lo hecho (qué se investigó, qué se confirmó, qué se descartó) para pegarlo directamente al principio de `PROGRESS.md` — mantiene el historial ordenado sin esfuerzo manual.

## 🎯 Aplicabilidad a CTFs

Todo este flujo se traslada casi 1:1 a CTFs (Capture The Flag), con algunos ajustes:

- El equivalente a `CLAUDE.md` sería las reglas del CTF concreto (qué herramientas están permitidas, qué máquinas/retos están en scope, formato de la flag).
- `PROGRESS.md` funciona igual de bien para llevar el estado de qué retos ya están resueltos, cuáles están en curso, y qué pistas/hipótesis se han probado ya.
- La metodología de agentes en paralelo es especialmente potente en CTFs con múltiples retos independientes abiertos a la vez (web, pwn, forense, cripto...) — puedes tener un agente explorando cada categoría simultáneamente.
- La diferencia principal es que en un CTF no hay "reporte" que enviar a una plataforma — el equivalente sería simplemente el flujo hasta obtener y validar la flag.

## ⚠️ Límites que conviene tener siempre presentes

- **La cuota de uso es un recurso real y limitado**, incluso con plan Max. Lanzar demasiados agentes simultáneos sin criterio agota la cuota rápido y sin necesariamente aportar valor proporcional — prioriza calidad de las tareas por agente sobre cantidad de agentes.
- **La IA puede sonar muy segura de sí misma incluso cuando se equivoca.** Mantén siempre el hábito de verificación manual descrito en este manual, por muy convincente que suene el resumen de un agente.
- **Automatizar la redacción no debe convertirse en automatizar la comprensión.** Si no puedes explicar tú mismo, con tus propias palabras, por qué existe la vulnerabilidad y cuál es su impacto real, no estás listo para reportarla — independientemente de lo bien redactado que esté el Markdown que generó Claude.
