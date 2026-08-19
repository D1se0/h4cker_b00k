# 🤖 Hacking Ético con IA (Claude)

Esta sección explica cómo uso **Claude Code** (la CLI de Claude para terminal) como copiloto para hacer Bug Bounty y CTFs: cómo lo instalo, cómo estructuro mis proyectos para que Claude tenga contexto persistente entre sesiones, cómo lanzo agentes en paralelo para explorar superficie de ataque, y los prompts exactos que uso en cada fase del proceso.

> ⚠️ **Aviso importante**: todo lo descrito aquí se usa exclusivamente dentro de programas de Bug Bounty con autorización explícita (scope, Rules of Engagement, Safe Harbor) o en CTFs/laboratorios legales. Usar Claude (o cualquier IA) para atacar sistemas sin autorización es ilegal exactamente igual que hacerlo sin IA — la IA no cambia la ley, solo la velocidad a la que trabajas dentro de lo permitido.

## 📖 Contenido de esta sección

* [¿Por qué usar IA para Bug Bounty?](por-que-usar-ia-bugbounty.md) — ventajas, límites y honestidad sobre lo que la IA aporta y lo que no.
* [Instalación de Claude Code en Linux](instalacion-claude-code-linux.md) — varias formas de instalarlo, y cómo gestionar sesiones (`/status`, `claude --resume`).
* [Estructura de proyecto y archivos de contexto](estructura-de-proyecto.md) — cómo organizo mi carpeta de trabajo: `CLAUDE.md`, `PROGRESS.md`, `RECON.md`, `example/`, `images/`, `temp/`, `reportar/`.
* [Qué es un CLAUDE.md y cómo escribir el tuyo](que-es-claude-md.md) — la pieza central de todo el sistema, con ejemplo real anonimizado.
* [PROGRESS.md — memoria de trabajo entre sesiones](progress-md.md) — cómo mantener el estado sin perder contexto al reiniciar Claude.
* [RECON.md — mapa de superficie del objetivo](recon-md.md) — dónde vive todo el reconocimiento acumulado.
* [Flujo de trabajo completo, paso a paso](flujo-de-trabajo-completo.md) — desde el prompt de inicio hasta el envío del reporte, con los prompts exactos.
* [Agentes en paralelo: metodología y buenas prácticas](agentes-en-paralelo.md) — cómo repartir el trabajo entre subagentes sin romper las reglas del programa.
* [Prompts clave, plantilla por plantilla](prompts-clave.md) — la biblioteca de prompts que uso en cada fase.
* [Ideas y automatizaciones adicionales](ideas-y-automatizaciones.md) — cosas que se pueden llevar más lejos.
