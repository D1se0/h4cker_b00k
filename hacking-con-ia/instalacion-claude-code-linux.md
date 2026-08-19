# Instalación de Claude Code en Linux

> 💡 Antes de nada: comprueba la documentación oficial más reciente en [docs.claude.com](https://docs.claude.com), ya que los pasos de instalación pueden cambiar. Lo de abajo son las formas habituales de instalarlo en Linux (probado en Kali).

## Requisitos previos

- **Node.js** (versión reciente, LTS recomendada) y `npm`.
- Una cuenta de Claude con **plan Pro o Max** para poder usar Claude Code con límites de uso razonables (ver aviso más abajo).

## Opción 1 — Instalación vía npm (la más habitual)

```bash
npm install -g @anthropic-ai/claude-code
```

Comprueba que se instaló correctamente:

```bash
claude --version
```

## Opción 2 — Instalación vía script oficial (nativo, sin depender de npm global)

Anthropic ofrece también un instalador nativo (binario nativo, sin depender de tu instalación global de Node):

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Este método es útil si no quieres depender de permisos globales de `npm` o si trabajas con varias versiones de Node y prefieres aislar la instalación de Claude Code del resto de tu entorno.

## Opción 3 — Vía gestor de paquetes de tu distro (si está disponible)

Algunas distros/comunidades mantienen paquetes empaquetados de terceros. Si tu distro lo ofrece, revisa siempre que provenga de un repositorio de confianza antes de instalarlo así — la vía oficial (npm o script de instalación) es la más fiable y la que se mantiene siempre actualizada.

## Primer arranque

Dentro de la carpeta de tu proyecto (ver [Estructura de proyecto](estructura-de-proyecto.md)):

```bash
cd ~/bugbounty/de-morgen
claude
```

La primera vez te pedirá autenticarte (login con tu cuenta de Anthropic). A partir de ahí, cada vez que ejecutes `claude` dentro de esa carpeta, tendrá acceso automáticamente a los ficheros de contexto que tengas ahí (`CLAUDE.md`, etc.).

## 🔑 Ver el ID de la conversación con `/status`

Dentro de una sesión activa de Claude Code, puedes ejecutar el comando:

```
/status
```

Esto te muestra información de la sesión actual, incluido el **ID de la conversación**. Apunta ese ID — te va a hacer falta para retomar exactamente esa misma conversación más adelante.

## 🔁 Retomar una conversación anterior

Para continuar una sesión pasada (con todo su historial y contexto ya cargado), en vez de arrancar una conversación nueva desde cero:

```bash
claude --resume <ID>
```

Sustituyendo `<ID>` por el que copiaste con `/status` en la sesión original.

Esto es especialmente útil en Bug Bounty porque:

- Puedes cerrar el terminal, apagar el ordenador, y retomar exactamente el mismo hilo de investigación días después sin perder el razonamiento intermedio que Claude ya había hecho.
- Te permite tener **conversaciones distintas por programa** (una por cada empresa/scope que estés auditando) y saltar entre ellas por ID sin mezclarlas.

> 💡 **Tip**: lleva un pequeño registro propio (puede ser tan simple como una nota) de qué ID de conversación corresponde a qué programa, especialmente si trabajas varios a la vez.

## ⚠️ Aviso importante sobre planes

> Esto funciona con cuentas de **Claude Pro o Max**. Recomiendo **Max**, ya que con el plan Pro el límite de uso se agota rápido en cuanto empiezas a lanzar varios agentes en paralelo (cada agente consume su propia cuota de uso). Si vas a trabajar con la metodología de [agentes en paralelo](agentes-en-paralelo.md) descrita en este manual, Max es prácticamente imprescindible para no quedarte bloqueado a mitad de una sesión de recon.
