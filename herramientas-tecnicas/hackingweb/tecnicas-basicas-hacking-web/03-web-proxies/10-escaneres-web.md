# Escaneo de vulnerabilidades: Burp Scanner y ZAP Scanner

## Qué aporta un escáner automatizado integrado

Más allá del fuzzing dirigido por el pentester, ambos proxies incluyen un **escáner de vulnerabilidades** capaz de mapear una aplicación completa (siguiendo enlaces, formularios y peticiones) y, después, probar automáticamente patrones conocidos de vulnerabilidades web sobre cada punto de entrada descubierto. No sustituye al análisis manual, pero acelera enormemente la cobertura inicial de una aplicación grande.

## Burp Scanner (función Pro)

Burp Scanner combina un **crawler** (construye el mapa del sitio) con un motor de **escaneo pasivo y activo**. Es una función exclusiva de la versión Professional.

### Definiendo el alcance (Scope)

Antes de lanzar un escaneo amplio, conviene delimitar exactamente qué dominios/rutas se incluyen, usando `Target > Scope`. Esto evita que Burp gaste recursos —o, peor, envíe tráfico potencialmente disruptivo— contra sistemas fuera del alcance autorizado de la auditoría. Es buena práctica excluir explícitamente funcionalidades sensibles como **logout**, ya que un escaneo automatizado podría cerrar la sesión activa accidentalmente e interrumpir el resto del escaneo.

### Crawl (rastreo)

El crawler navega la aplicación siguiendo enlaces y enviando formularios para construir un mapa completo de rutas accesibles. A diferencia de un fuzzer de directorios (`ffuf`, `gobuster`), el crawler **solo descubre lo que está enlazado** desde algún punto accesible — no encuentra rutas "ocultas" que no estén referenciadas en ningún sitio. Para eso se necesita fuzzing de contenido (visto en el bloque de *Web Fuzzing*), o la función de **Content Discovery** integrada en Burp.

Es posible configurar credenciales de login para que el crawler navegue también la parte autenticada de la aplicación, ampliando significativamente la cobertura del escaneo.

### Escaneo pasivo

Analiza el contenido de las páginas ya visitadas **sin enviar peticiones adicionales**, buscando indicios de vulnerabilidades potenciales: cabeceras de seguridad ausentes, posibles XSS basados en DOM, comentarios sospechosos. Es rápido y de bajo impacto, pero solo *sugiere* posibles problemas — no los confirma activamente. Cada hallazgo incluye un nivel de **confianza** (`Certain`, `Firm`, `Tentative`) que ayuda a priorizar qué revisar primero.

### Escaneo activo

El más completo y "agresivo": además de repetir el rastreo y el escaneo pasivo, **envía activamente payloads de prueba** sobre cada parámetro y punto de inserción identificado, intentando confirmar vulnerabilidades como XSS, inyección SQL, inyección de comandos, entre otras. Está considerado uno de los escáneres más fiables del mercado, mantenido y actualizado constantemente.

## ZAP Scanner (gratuito)

ZAP ofrece una funcionalidad equivalente sin coste, estructurada en **Spider** + escaneo pasivo + escaneo activo.

### Spider

Equivalente al crawler de Burp. Se lanza con clic derecho sobre una petición → `Attack > Spider`, o desde el HUD. Recorre la aplicación siguiendo enlaces, construyendo el árbol de sitios visible en la pestaña **Sites**.

Existe además el **Ajax Spider**, una variante que también sigue enlaces generados dinámicamente vía peticiones AJAX/JavaScript — relevante en aplicaciones modernas de página única (SPA), donde un crawler tradicional basado solo en HTML estático se quedaría corto. Ejecutar ambos (Spider normal seguido de Ajax Spider) suele dar la cobertura más completa.

### Escaneo pasivo

Se ejecuta automáticamente en segundo plano sobre cada respuesta que ZAP observa mientras el Spider trabaja (o mientras se navega manualmente con el proxy activo). Los hallazgos se acumulan en la pestaña **Alerts**, accesible también desde el HUD.

### Escaneo activo

Se lanza con el botón **Active Scan**, y si aún no se ha ejecutado un Spider, ZAP lo hace automáticamente primero. Envía peticiones de prueba contra cada parámetro identificado, igual que el escáner activo de Burp.

### Priorizando hallazgos

Las alertas se clasifican por severidad. Conviene revisar primero las de severidad **alta** (`High`), que normalmente apuntan a vulnerabilidades con potencial de comprometer directamente la aplicación o el servidor backend — aunque, en auditorías exhaustivas, ninguna severidad debería descartarse sin revisión.

### Generación de informes

`Report > Generate HTML Report` (también disponible en XML o Markdown) produce un documento estructurado con todos los hallazgos del escaneo, útil como base de partida para un informe de auditoría — aunque, como veremos en el bloque de *Bug Bounty Hunting Process*, un informe profesional siempre requiere validación manual y contexto adicional, no solo la salida cruda del escáner.

## Extensiones: ampliando las capacidades base

Ambas herramientas soportan extensiones de terceros que añaden funcionalidad adicional:

- **Burp BApp Store**: catálogo oficial de extensiones (algunas gratuitas, otras exclusivas de Pro), accesible desde la pestaña **Extensions**. Incluye herramientas para detección de tecnologías, generación de payloads especializados, análisis de JWT, entre muchas otras.
- **ZAP Marketplace**: equivalente en ZAP, accesible desde el icono correspondiente en la interfaz, con extensiones para añadir wordlists adicionales, nuevos scanners, o integraciones con otras herramientas.

Explorar el catálogo de extensiones disponible es recomendable al especializarse en un tipo concreto de auditoría (por ejemplo, hay extensiones específicas para probar JWT, GraphQL, o aplicaciones móviles), ya que pueden ahorrar tiempo considerable frente a replicar esa funcionalidad manualmente.

## Advertencia importante sobre escaneo activo

Un escaneo activo **envía tráfico real** capaz de disparar acciones en la aplicación objetivo: crear registros, enviar formularios, o incluso (en aplicaciones mal protegidas) ejecutar acciones destructivas si encuentra, por ejemplo, un endpoint de borrado sin protección adecuada. Nunca debe lanzarse un escaneo activo contra un sistema sin autorización explícita, y conviene revisar cuidadosamente el alcance configurado antes de iniciarlo, especialmente en entornos de producción.
