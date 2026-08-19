---
icon: diagram-sankey
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

# Flujo de trabajo completo, paso a paso

Este es mi ciclo real de trabajo con Claude Code para un programa de Bug Bounty, de principio a fin. Cada paso incluye el prompt exacto (o muy cercano al exacto) que uso.

## 🗺️ Visión general del ciclo

```
1. Preparar el programa (CLAUDE.md, scope, reglas)
         ↓
2. Lanzar el prompt de inicio → agentes en paralelo investigando
         ↓
3. Un agente encuentra algo prometedor → parar y pedir guía de reproducción manual
         ↓
4. Reproducir manualmente el hallazgo yo mismo, capturando pantallas
         ↓
5. Depositar las capturas en images/ y pedir el reporte completo en Markdown
         ↓
6. Pedir que rellene los campos exactos de la plataforma → deposita en temp/
         ↓
7. Enviar el reporte manualmente en la plataforma (decisión humana, siempre)
         ↓
8. Volver al paso 2 con el mismo prompt de inicio para seguir investigando
```

## 1️⃣ Preparar el programa

Antes de nada, monto la carpeta del programa con la estructura de [Estructura de proyecto](estructura-de-proyecto.md) y relleno bien el `CLAUDE.md` con las reglas reales del programa (ver [Qué es un CLAUDE.md](que-es-claude-md.md)). Esto se hace una vez por programa, no en cada sesión.

## 2️⃣ El prompt de inicio

Este es el prompt que guardo en `promptInicio.txt` y que lanzo cada vez que empiezo (o retomo) una sesión de investigación activa:

```
/goal Ahora lanza distintos agentes para ir probando distintas
vulnerabilidades y debes parar hasta encontrar alguna digna de
reportar
```

### Por qué funciona este prompt

* **`/goal`**: en Claude Code, prefijar con `/goal` (o el modificador equivalente de "modo objetivo/autónomo" de tu versión) le indica que trabaje de forma continuada hacia un objetivo, **sin pararse a preguntar en cada paso individual** — clave para dejarlo trabajando de forma semi-autónoma en vez de tener que aprobar cada acción una por una.
* **"lanza distintos agentes"**: activa explícitamente la metodología de [subagentes en paralelo](agentes-en-paralelo.md) descrita en el `CLAUDE.md` del programa.
* **"debes parar hasta encontrar alguna digna de reportar"**: fija la condición de parada — no quiero que siga indefinidamente ni que se pare al primer indicio dudoso, sino que continúe investigando hasta dar con algo que, tras verificación básica, merezca pasar a la fase de reproducción manual.

> 💡 Todo el detalle de "qué está permitido hacer sin preguntar" y "qué debe seguir preguntando" no vive en este prompt — vive en el `CLAUDE.md`, que Claude ya ha leído al arrancar. Este prompt es corto precisamente porque todo el contexto pesado ya está en los archivos del proyecto.

## 3️⃣ Cuando aparece algo prometedor: pedir la guía de reproducción manual

En cuanto un agente reporta un hallazgo que parece real, **no lo doy por bueno automáticamente**. El siguiente paso es siempre pedirle a Claude que me lo explique de forma que yo pueda reproducirlo con mis propias manos:

```
Ahora quiero que me des la guía paso a paso para poder reproducirlo
manualmente yo y poder sacar las capturas correspondientes, para el
reporte posterior
```

Esto es fundamental por dos motivos:

1. **Verificación humana real**: reproducirlo yo mismo confirma que el hallazgo no es un falso positivo o una malinterpretación del agente.
2. **Capturas limpias y con contexto claro**: al hacerlo yo mismo, controlo exactamente qué se ve en cada captura, en qué orden, y puedo asegurarme de que cada paso queda documentado de forma que un tercero (el triager) lo entienda sin dudas.

## 4️⃣ Reproducción manual + capturas

Sigo la guía paso a paso, verificando que el comportamiento descrito ocurre realmente, y voy haciendo capturas de pantalla (o grabando vídeo si el flujo lo requiere, ver [Evidencias: capturas y vídeos](../bugbounty/04-como-escribir-reportes/evidencias-capturas-videos.md)) en cada paso relevante. Las guardo todas en `images/`.

## 5️⃣ Pedir el reporte completo con las capturas ya integradas

Una vez tengo todas las capturas en `images/`:

```
Ya tienes las capturas en <PATH_IMAGES> quiero que me realices el
reporte implementando dichas capturas todo en inglés y que sigas la
estructura de example/ todo en markdown super detallado y que sea
fácil de reproducir por alguien que no entienda mucho
```

### Por qué funciona este prompt

* **`<PATH_IMAGES>`**: le doy la ruta exacta (`images/`) para que inspeccione directamente el contenido visual de cada captura — no tengo que describirle qué hay en cada imagen, Claude las analiza directamente.
* **"todo en inglés"**: la mayoría de programas y triagers internacionales trabajan en inglés — redactar directamente en el idioma final ahorra una fase de traducción posterior.
* **"que sigas la estructura de example/"**: aquí es donde `example/report_example.md` entra en juego — le da a Claude un patrón de estilo y estructura ya validado por mí anteriormente, para que el nuevo reporte mantenga el mismo nivel de detalle y el mismo formato que reportes anteriores.
* **"fácil de reproducir por alguien que no entienda mucho"**: refuerza explícitamente el principio de [Anatomía de un buen reporte](../bugbounty/04-como-escribir-reportes/anatomia-de-un-buen-reporte.md) — nada de dar cosas por sabidas.

## 6️⃣ Pedir que rellene los campos exactos de la plataforma

Con el reporte ya en Markdown, el último paso antes de enviar es adaptarlo a los campos exactos del formulario de la plataforma correspondiente:

```
Quiero que me rellenes los campos para poder reportar la
vulnerabilidad <PASAS_LOS_CAMPOS_DE_LA_PAGINA_ENTEROS> quiero que
me deposites los archivos correspondientes a los campos en temp/
con el nombre de la vulnerabilidad correspondiente para no confundirme
```

### Cómo uso esto en la práctica

Le pego literalmente la estructura de campos vacía del formulario de la plataforma (título, tipo, endpoint, payload, impacto, etc. — ver las [plantillas de plataforma](../bugbounty/05-plataformas/) de este manual) para que Claude sepa exactamente qué campos existen y cómo trocear el contenido del reporte ya redactado entre ellos. El resultado se deposita en `temp/vulnN/`, con un archivo por bloque de campos (ver [Estructura de proyecto](estructura-de-proyecto.md#-carpetas-temp--campos-ya-troceados-por-plataforma)), listo para copiar/pegar directamente en cada caja de texto del formulario web.

## 7️⃣ Envío manual — siempre decisión humana

Pulsar "Enviar" en la plataforma **lo hago siempre yo, manualmente**. Ni Claude ni ningún agente tiene permiso para enviar un reporte por su cuenta — es, literalmente, una de las acciones que en el `CLAUDE.md` marco como "debe seguir pidiendo confirmación explícita siempre" (ver [Qué es un CLAUDE.md](que-es-claude-md.md#1-autorización-y-alcance-ético)).

## 8️⃣ Vuelta al ciclo

Una vez enviado el reporte, actualizo el estado en `PROGRESS.md` (o le pido a Claude que lo haga) y vuelvo a lanzar el mismo `promptInicio.txt` para seguir investigando el resto del scope.

***

> 📌 **Resumen de la filosofía**: la IA automatiza recon, exploración e investigación en paralelo, y acelera muchísimo la redacción y el formateo del reporte final — pero **la verificación del hallazgo y el envío del reporte siguen siendo siempre pasos manuales y humanos**, precisamente los dos puntos donde un error tiene consecuencias reales.
