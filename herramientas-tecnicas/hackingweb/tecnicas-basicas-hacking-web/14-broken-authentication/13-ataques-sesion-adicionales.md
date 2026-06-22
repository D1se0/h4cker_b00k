# Ataques de sesión adicionales

## Más allá de cómo se genera el token: cómo se gestiona durante su ciclo de vida

El apartado anterior cubrió fallos en la **generación** del token de sesión (entropía insuficiente, estructura predecible). Este apartado cierra el bloque con dos fallos distintos, relacionados con cómo la aplicación **gestiona** ese token a lo largo del tiempo, independientemente de cuán bien generado esté en origen.

## Fijación de sesión (Session Fixation)

### El fallo de fondo

Una aplicación es vulnerable a fijación de sesión cuando **no asigna un nuevo token tras un login exitoso** — es decir, si un token de sesión ya existía (incluso uno todavía no autenticado, o conocido de antemano), la aplicación simplemente lo "promueve" a estado autenticado en lugar de generar uno completamente nuevo en ese momento.

### Por qué esto es explotable

Si un atacante puede conseguir que la víctima **use un token de sesión que el atacante ya conoce de antemano** (por ejemplo, porque algunas aplicaciones mal diseñadas aceptan establecer la cookie de sesión a partir de un valor recibido en la propia URL), y después la víctima se autentica normalmente con ese mismo token, el atacante —que ya conocía ese valor desde el principio— puede usarlo él mismo para acceder a la sesión ahora autenticada de la víctima, sin haber tenido que interceptar ni robar nada en ningún momento posterior.

La clave del fallo no está en cómo el atacante consigue que la víctima use un token conocido (eso depende de detalles específicos de cada aplicación vulnerable) — está en que la aplicación **confía en seguir usando un token preexistente** después de la autenticación, en lugar de invalidar cualquier token previo y emitir uno completamente nuevo en el momento exacto en que el usuario pasa de "no autenticado" a "autenticado".

### Mitigación

La defensa es directa y estructural: **regenerar siempre el token de sesión inmediatamente después de una autenticación exitosa**, invalidando cualquier valor de sesión que existiera antes del login. De esta forma, aunque un atacante consiguiera que la víctima usara un token conocido de antemano, ese valor dejaría de tener validez en el momento mismo en que la víctima se autentica — el servidor emite uno nuevo, desconocido para el atacante, rompiendo por completo la cadena de ataque.

## Tiempo de espera de sesión inadecuado (Session Timeout)

### El fallo de fondo

Una sesión que **nunca caduca** permanece válida indefinidamente, incluso mucho después de que el usuario haya dejado de interactuar con la aplicación. Esto amplía sin límite la ventana de oportunidad para cualquier ataque que dependa de obtener un token de sesión ya válido — desde robo de sesión vía XSS (bloque correspondiente), hasta cualquier otro escenario donde un atacante consiga, por cualquier vía, hacerse con un token capturado tiempo atrás.

### No existe un valor universal correcto

El tiempo de espera adecuado depende enteramente del contexto de negocio y de la sensibilidad de los datos que la aplicación maneja:

| Tipo de aplicación | Sensibilidad de los datos | Timeout orientativo |
|---|---|---|
| Datos médicos o financieros sensibles | Muy alta | Minutos |
| Banca, paneles administrativos | Alta | Decenas de minutos |
| Redes sociales, aplicaciones de uso casual | Moderada | Horas, o sesión persistente con reautenticación periódica |

El criterio no es "cuanto más corto, mejor" de forma absoluta — un timeout excesivamente agresivo en una aplicación de bajo riesgo perjudica la experiencia de usuario sin aportar beneficio de seguridad proporcional. El equilibrio correcto depende de evaluar qué impacto tendría una sesión comprometida en ese contexto específico.

### Mitigación

- **Definir explícitamente un tiempo de expiración** acorde a la sensibilidad de los datos manejados — nunca dejar el valor por defecto sin evaluarlo conscientemente.
- **Invalidar la sesión también del lado del servidor** al hacer logout o al expirar, no solo eliminar la cookie del lado del cliente — un token que sigue siendo técnicamente válido en el servidor, aunque el navegador ya no lo envíe, sigue siendo explotable si un atacante lo capturó por cualquier otra vía.
- **Considerar timeouts diferenciados** según el nivel de privilegio: una sesión administrativa, por su mayor impacto potencial si se compromete, justifica un tiempo de expiración más estricto que una sesión de usuario estándar.

## Cierre del bloque de Broken Authentication

Con esto se completa el recorrido de este bloque, desde los fundamentos de los tres factores de autenticación hasta los detalles de gestión del ciclo de vida de una sesión. El hilo conductor, repetido en cada apartado: la autenticación no es un único control aislado, sino una cadena de decisiones —generación de credenciales, verificación, gestión de sesión posterior— donde un fallo en cualquier eslabón compromete la seguridad del conjunto, independientemente de cuán robustos sean los demás. El siguiente bloque, *Web Attacks*, retoma esta misma lógica de cadena aplicada al control de acceso y a otras vulnerabilidades estructurales de aplicaciones web —IDOR, CSRF, XXE— que completan el panorama de fallos lógicos más allá de la autenticación en sí.
