---
icon: arrow-pointer
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

# Documentación Hacking Impresoras

## Hacking Ético de Impresoras de Red vía PJL (Printer Job Language)

Guía técnica completa sobre reconocimiento, explotación y auditoría de impresoras de red que exponen el protocolo **PJL** en el puerto RAW/JetDirect (**TCP 9100**), incluyendo una herramienta propia en Python, un laboratorio virtual con Docker y un listado de referencia de los comandos PJL más relevantes.

### Índice

1. Aviso legal y contexto ético
2. ¿Qué es PJL y por qué es relevante en pentesting?
3. Fase 1 — Detección de la IP de la impresora
4. Fase 2 — Comunicación manual con la impresora
5. Tabla de referencia — Comandos PJL originales más importantes
6. Construyendo una herramienta de auditoría: `hackPrinter.py`
7. Uso práctico de la herramienta
8. Laboratorio local: honeypot PJL con Docker
9. Mitigaciones y defensa
10. Conclusión y recursos

***

### Aviso legal y contexto ético

Antes de tocar un solo comando, hay que dejar claro el marco en el que se mueve todo este documento:

* Todo lo aquí descrito debe practicarse **exclusivamente** sobre dispositivos de tu propiedad, o sobre los que tengas **autorización explícita y por escrito** (un contrato de pentesting, una carta de autorización, o un laboratorio propio) para realizar pruebas de seguridad.
* Acceder sin permiso al puerto 9100 de una impresora ajena, leer sus documentos, modificar su configuración o alterar su NVRAM puede constituir un **delito** (en España, encaja potencialmente en los arts. 197 y 264 del Código Penal, relativos al descubrimiento y revelación de secretos y a los daños informáticos; otras jurisdicciones tienen legislación equivalente, como la _Computer Fraud and Abuse Act_ en EE. UU.).
* El objetivo de esta guía es **formativo**: entender cómo funciona el vector de ataque para poder auditarlo, documentarlo y, sobre todo, **mitigarlo** en tu propia infraestructura.
* Todo el laboratorio práctico se realiza contra una impresora simulada (_honeypot_) desplegada en local mediante Docker, precisamente para poder experimentar sin ningún riesgo legal ni operativo.

Dicho esto, entremos en materia.

### ¿Qué es PJL y por qué es relevante en pentesting?

**PJL (Printer Job Language)** es un protocolo de control de trabajos de impresión creado por HP en 1993 y adoptado después, en mayor o menor medida, por prácticamente todo el sector (Brother, Xerox, Lexmark, Kyocera, Canon, Epson...). PJL no es el lenguaje que describe _qué_ se imprime (eso lo hacen PCL o PostScript); es la capa que hay **alrededor** de ese contenido, y que permite:

* Identificar el dispositivo (marca, modelo, firmware).
* Consultar y modificar variables de configuración (bandeja por defecto, densidad, timeouts, idioma...).
* Leer el estado operativo (atascos, nivel de tóner, errores).
* En muchos modelos, **navegar por un sistema de ficheros interno** (NVRAM/flash) donde se almacenan trabajos de escaneo, libretas de direcciones, credenciales guardadas de servicios (SMB, FTP, correo) o incluso el firmware.

#### Por qué es un vector de ataque tan interesante

1. **Cero autenticación por defecto.** La inmensa mayoría de impresoras de red aceptan comandos PJL en el puerto 9100 sin pedir usuario ni contraseña. Si tu equipo puede alcanzar ese puerto por red, puede hablar con la impresora.
2. **Texto plano sobre TCP.** No hay TLS, no hay cifrado: cualquier interceptación de tráfico en el mismo segmento de red puede ver (y potencialmente modificar) los comandos.
3. **Superficie amplia.** Reconocimiento (`INFO ID/STATUS/VARIABLES`), lectura y escritura de ficheros (`FS*`), modificación persistente de configuración (`DEFAULT`), manipulación física visible (`RDYMSG`)... todo con el mismo canal.
4. **Impacto real en entornos corporativos.** Las impresoras multifunción suelen guardar credenciales de red (para escanear a carpetas SMB o enviar por correo), documentos escaneados recientes, y en algunos casos permiten llegar hasta ejecución de comandos a través de extensiones propietarias del fabricante (por ejemplo `@PJL DMCMD` en impresoras Kyocera).

#### El "sobre" de cada comando: UEL

Cada sesión PJL se abre y se cierra con la secuencia **UEL (Universal Exit Language)**: el byte `ESC` (`0x1B`) seguido del texto `%-12345X`. Esta secuencia le indica al lenguaje de impresión que esté activo en ese momento (PCL, PostScript...) que debe salir de su modo actual y entrar en modo PJL. Por eso vas a ver siempre este patrón:

```
UEL + "@PJL COMANDO ...\r\n" + UEL
```

Sin el UEL inicial, la mayoría de firmwares ni siquiera reconocen que les estás hablando en PJL; sin el UEL final, la sesión puede quedar "colgada" esperando más datos.

Si esto suena a "netcat con esteroides", es exactamente eso: todo lo que sigue en esta guía consiste en automatizar el envío de estas cadenas de texto por un socket TCP.

### Fase 1 — Detección de la IP de la impresora

Antes de nada: muchas impresoras vienen con el puerto **9100** abierto por defecto en cuanto están conectadas a una red (cableada o wifi). En redes domésticas o de laboratorio esto es habitual; en entornos corporativos bien segmentados, en cambio, suele estar mitigado mediante **VLANs** que separan el tráfico de impresión del resto de la red, precisamente para evitar este tipo de acceso. En esta guía asumimos que estamos en el mismo segmento de red que la impresora (como ocurriría, por ejemplo, tras comprometer un puesto de la LAN de oficina, o en un laboratorio propio).

Como no sabemos qué IP tiene, hacemos un escaneo con `nmap` filtrando por el puerto 9100:

```bash
nmap -p 9100 --open 192.168.1.0/24
```

Salida esperada:

```
Starting Nmap 7.99 ( https://nmap.org ) at 2026-08-22 11:34 +0200
Nmap scan report for 192.168.1.21
Host is up (0.041s latency).

PORT     STATE SERVICE
9100/tcp open  jetdirect
MAC Address: A3:FC:77:1B:78:BD (Mega Well Limited)

Nmap done: 256 IP addresses (19 hosts up) scanned in 3.30 seconds
```

Nmap ya reconoce el puerto 9100 con el nombre de servicio `jetdirect` (el nombre comercial que le dio HP a su implementación de esta interfaz RAW). En este caso ha coincidido con la IP `192.168.1.21`.

#### Alternativas y refinamiento del escaneo

Si quieres ir un paso más allá del simple descubrimiento de puertos:

```bash
# Detección de versión/servicio y scripts NSE por defecto sobre el puerto 9100
nmap -p 9100 -sV -sC 192.168.1.21

# Escaneo también de otros puertos típicos de impresoras (IPP, LPD, HTTP de gestión, SNMP)
nmap -p 9100,631,515,80,443,161 --open 192.168.1.0/24
```

Con esto, además del 9100, puedes detectar el panel web de administración (HTTP/HTTPS), IPP (Internet Printing Protocol, puerto 631), LPD (puerto 515) o SNMP (puerto 161/UDP), todos ellos vectores adicionales de reconocimiento sobre el mismo dispositivo.

### Fase 2 — Comunicación manual con la impresora

Una vez identificada la IP, el método más directo para "hablar" en PJL es abrir una conexión TCP cruda contra el puerto 9100. Con `telnet`:

```bash
telnet 192.168.1.21 9100
```

Una vez dentro, cualquier cadena de texto que empiece por `@PJL` (envuelta en los UEL correspondientes) es interpretada por la impresora. Por ejemplo, para pedir la identificación del dispositivo escribirías (de forma literal, con el carácter ESC incluido, algo que `telnet` no facilita escribir a mano, pero que sí puedes simular con herramientas como `printf` + `nc`):

```bash
printf '\x1b%%-12345X@PJL INFO ID\r\n\x1b%%-12345X' | nc 192.168.1.21 9100
```

Pero si no tenemos `telnet` disponible (por ejemplo, en un `Windows` sin herramientas adicionales instaladas, o simplemente porque queremos algo más cómodo y repetible), lo razonable es escribir un pequeño cliente en `python3` que traduzca comandos con nombres amigables (`ls`, `cat`, `get`, `put`, `rm`...) al PJL real equivalente. Esa es la herramienta que construimos en la sección 6 de esta guía: **`hackPrinter.py`**.

Antes de llegar al código, conviene tener a mano una referencia clara de qué comandos PJL existen realmente y qué hace cada uno — eso es lo que cubre la siguiente tabla.

### Tabla de referencia — Comandos PJL originales más importantes

Esta es una recopilación de los comandos PJL **estándar** (definidos originalmente en el _HP PJL Technical Reference Manual_) más relevantes desde el punto de vista de auditoría de seguridad, agrupados por categoría. Todos siguen el mismo patrón de envoltura `UEL + comando + UEL` explicado antes; aquí se muestra únicamente el cuerpo del comando tal cual se escribe.

#### 1. Control de sesión y trabajos

| Comando            | Sintaxis                                     | Descripción                                                                                                                                                                                     |
| ------------------ | -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **UEL**            | `<ESC>%-12345X`                              | No es un comando PJL en sí, sino el delimitador que abre/cierra cada sesión PJL. Obligatorio al principio y al final de cada interacción.                                                       |
| **COMMENT**        | `@PJL COMMENT <texto>`                       | Comentario sin efecto funcional; útil para anotar trabajos o como "no-op" al probar si la impresora acepta PJL.                                                                                 |
| **JOB**            | `@PJL JOB [NAME="<nombre>"]`                 | Marca el inicio de un trabajo de impresión con nombre identificable, útil para agrupar variables `SET` a ese trabajo concreto.                                                                  |
| **EOJ**            | `@PJL EOJ [NAME="<nombre>"]`                 | _End Of Job_: marca el final de un trabajo iniciado con `JOB`.                                                                                                                                  |
| **ENTER LANGUAGE** | `@PJL ENTER LANGUAGE=<PCL\|POSTSCRIPT\|...>` | Le dice a la impresora que lo que sigue a continuación del comando ya no es PJL, sino datos en el lenguaje de impresión indicado (aquí es donde realmente "empieza a imprimirse" el documento). |
| **RESET**          | `@PJL RESET`                                 | Restaura todas las variables de entorno de la _sesión actual_ a los valores por defecto (no toca NVRAM).                                                                                        |
| **INITIALIZE**     | `@PJL INITIALIZE`                            | Reinicializa el entorno PJL del dispositivo a los valores de fábrica guardados en NVRAM.                                                                                                        |

#### 2. Identificación y estado (solo lectura — reconocimiento seguro)

| Comando            | Sintaxis                       | Descripción                                                                                                                                                                                               |
| ------------------ | ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **INFO ID**        | `@PJL INFO ID`                 | Devuelve la cadena de identificación del dispositivo (fabricante, modelo, versión de firmware). Primer comando recomendado en cualquier reconocimiento.                                                   |
| **INFO STATUS**    | `@PJL INFO STATUS`             | Estado operativo actual (listo, imprimiendo, atasco de papel, tóner bajo, error concreto con código numérico).                                                                                            |
| **INFO CONFIG**    | `@PJL INFO CONFIG`             | Configuración hardware instalada: memoria, bandejas, opciones de acabado, idiomas de impresión soportados.                                                                                                |
| **INFO VARIABLES** | `@PJL INFO VARIABLES`          | Vuelca **todas** las variables de entorno configurables del dispositivo (el equivalente a un `env` de Linux). Muy útil para descubrir variables propietarias del fabricante no documentadas públicamente. |
| **INFO FILESYS**   | `@PJL INFO FILESYS`            | Lista los volúmenes de sistema de ficheros que expone el firmware (típicamente `0:` = RAM, `1:` = flash/NVRAM). Si no devuelve nada, el modelo probablemente no implementa filesystem PJL.                |
| **INFO MEMORY**    | `@PJL INFO MEMORY`             | Memoria disponible en el dispositivo.                                                                                                                                                                     |
| **INFO PAGECOUNT** | `@PJL INFO PAGECOUNT`          | Contador total de páginas impresas por el dispositivo desde fábrica.                                                                                                                                      |
| **INFO LOG**       | `@PJL INFO LOG <ERROR\|EVENT>` | Vuelca el histórico interno de errores o eventos registrados por el firmware.                                                                                                                             |
| **INFO FONTS**     | `@PJL INFO FONTS`              | Lista las fuentes tipográficas instaladas.                                                                                                                                                                |
| **INFO USTATUS**   | `@PJL INFO USTATUS`            | Muestra la configuración actual de notificaciones de estado no solicitadas (ver sección USTATUS más abajo).                                                                                               |
| **ECHO**           | `@PJL ECHO "<texto>"`          | Pide a la impresora que repita el texto enviado. Es el "ping" de aplicación: si el eco vuelve, el intérprete PJL está vivo y respondiendo, no solo el puerto TCP.                                         |
| **DINQUIRE**       | `@PJL DINQUIRE <VARIABLE>`     | _Default INQUIRE_: consulta el valor persistido en NVRAM de una variable **concreta**, sin necesidad de volcarlas todas con `INFO VARIABLES`.                                                             |

#### 3. Modificación de variables de entorno

| Comando      | Sintaxis                                  | Descripción                                                                                                                                                                                                                                                                            | Riesgo                      |
| ------------ | ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| **SET**      | `@PJL SET <VARIABLE>=<VALOR>`             | Modifica una variable **solo para el trabajo/sesión actual**. No persiste tras reiniciar el dispositivo.                                                                                                                                                                               | Bajo                        |
| **DEFAULT**  | `@PJL DEFAULT <VARIABLE>=<VALOR>`         | Igual que `SET`, pero **persiste el cambio en NVRAM** como nuevo valor de fábrica. Es el comando que emplean los ataques de "printer bricking" o de bloqueo permanente del dispositivo (p. ej. estableciendo una `PASSWORD` desconocida para el propietario legítimo).                 | **Alto — destructivo**      |
| **FSCONFIG** | `@PJL FSCONFIG VOLUME="<vol>" INIT=<...>` | Configura parámetros de bajo nivel de un volumen de filesystem (en modelos que lo soportan).                                                                                                                                                                                           | Alto                        |
| **SECURITY** | `@PJL SECURITY PASSWORD=<n>`              | Comando histórico (documentado en HP PJL Technical Reference) para proteger con una contraseña numérica el uso de `DEFAULT` y otros comandos administrativos. Su ausencia o mala configuración es lo que permite, en la práctica, que cualquiera pueda usar `DEFAULT` sin restricción. | Crítico (control de acceso) |

#### 4. Mensajería y display físico (bajo riesgo, alta confirmación visual)

| Comando    | Sintaxis                        | Descripción                                                                                                                                                                                   |
| ---------- | ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **RDYMSG** | `@PJL RDYMSG DISPLAY="<texto>"` | Cambia el mensaje mostrado en la pantalla LCD cuando la impresora está en estado "ready". Clásica demo inofensiva para confirmar en persona que los comandos llegan realmente al dispositivo. |
| **OPMSG**  | `@PJL OPMSG DISPLAY="<texto>"`  | Muestra un mensaje de operador que **detiene la cola de impresión** hasta que alguien lo confirma físicamente en el panel. Tiene impacto real en disponibilidad (DoS leve).                   |
| **STMSG**  | `@PJL STMSG DISPLAY="<texto>"`  | Mensaje de estado asociado a un código de error concreto.                                                                                                                                     |

#### 5. Notificación de estado asíncrono (USTATUS)

| Comando            | Sintaxis                                 | Descripción                                                                                                                             |
| ------------------ | ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **USTATUS DEVICE** | `@PJL USTATUS DEVICE=<OFF\|ON\|VERBOSE>` | Activa notificaciones automáticas de cambios de estado del dispositivo (útil para monitorización pasiva de una impresora comprometida). |
| **USTATUS JOB**    | `@PJL USTATUS JOB=<OFF\|ON>`             | Notificaciones de inicio/fin de cada trabajo de impresión.                                                                              |
| **USTATUS PAGE**   | `@PJL USTATUS PAGE=<OFF\|ON>`            | Notificación por cada página impresa.                                                                                                   |
| **USTATUS TIMED**  | `@PJL USTATUS TIMED=<segundos>`          | Notificaciones periódicas de estado cada _n_ segundos.                                                                                  |
| **USTATUSOFF**     | `@PJL USTATUSOFF`                        | Desactiva todas las notificaciones asíncronas. Útil para "limpiar" el canal antes de leer una respuesta puntual.                        |

#### 6. Sistema de ficheros (`FS*`) — el vector más crítico

| Comando        | Sintaxis                                                                             | Descripción                                                                                                                                                                                                                                             | Riesgo                              |
| -------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| **FSQUERY**    | `@PJL FSQUERY NAME="<ruta>"`                                                         | Consulta metadatos de un fichero o directorio (existencia, tipo, tamaño) sin descargar contenido. Equivalente a un `stat` remoto.                                                                                                                       | Bajo                                |
| **FSDIRLIST**  | `@PJL FSDIRLIST NAME="<ruta>" ENTRY=<n> COUNT=<n>`                                   | Lista el contenido de un directorio del volumen indicado, paginando con `ENTRY`/`COUNT`.                                                                                                                                                                | Bajo–Medio                          |
| **FSUPLOAD**   | `@PJL FSUPLOAD NAME="<ruta>" OFFSET=<n> SIZE=<n>`                                    | El nombre está desde el punto de vista de la impresora (ella "sube" el fichero hacia el cliente): en la práctica es una **descarga** para el auditor/atacante. Permite leer escaneos, libretas de direcciones, configuración, credenciales guardadas... | **Alto — fuga de datos**            |
| **FSDOWNLOAD** | `@PJL FSDOWNLOAD FORMAT:BINARY SIZE=<n> NAME="<ruta>"` seguido de _n_ bytes binarios | Igual de invertido: la impresora "descarga" lo que el cliente le envía, es decir, es una **escritura/subida** para el auditor. Permite sobrescribir ficheros existentes o depositar contenido arbitrario.                                               | **Alto — destructivo/persistencia** |
| **FSAPPEND**   | `@PJL FSAPPEND FORMAT:BINARY SIZE=<n> NAME="<ruta>"`                                 | Igual que `FSDOWNLOAD` pero añadiendo al final de un fichero existente en lugar de sobrescribirlo.                                                                                                                                                      | Alto                                |
| **FSDELETE**   | `@PJL FSDELETE NAME="<ruta>"`                                                        | Borra un fichero o directorio vacío del volumen indicado.                                                                                                                                                                                               | **Alto — destructivo**              |
| **FSMKDIR**    | `@PJL FSMKDIR NAME="<ruta>"`                                                         | Crea un directorio nuevo en el volumen indicado.                                                                                                                                                                                                        | Medio                               |
| **FSINIT**     | `@PJL FSINIT VOLUME="<vol>"`                                                         | Formatea/inicializa por completo un volumen de filesystem.                                                                                                                                                                                              | **Crítico — irreversible**          |

#### 7. Extensiones propietarias relevantes en pentesting

No son parte del estándar PJL original de HP, pero aparecen con frecuencia en auditorías reales y merece la pena conocerlas:

| Comando            | Fabricante           | Descripción                                                                                                                                                                                                                                                                                                     |
| ------------------ | -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **DMCMD**          | Kyocera              | _Direct Mode Command_: extensión propietaria (`@PJL DMCMD ASCII "..."`) que en ciertos modelos permite ejecutar operaciones internas del firmware más allá de lo que cubre el PJL estándar; ha sido la base de varias PoC de compromiso total de impresoras Kyocera publicadas por investigadores de seguridad. |
| **XRXEXTENSION**   | Xerox                | Variantes propietarias para operaciones específicas de la familia Xerox, con espíritu similar a `INFO`/`SET` pero para parámetros no estándar.                                                                                                                                                                  |
| **SIINFO / SISET** | HP (algunos modelos) | Variables extendidas específicas de ciertas gamas HP, no cubiertas por el `INFO VARIABLES` genérico.                                                                                                                                                                                                            |

> **Nota metodológica:** la forma correcta de descubrir variables y comandos propietarios de un modelo concreto es lanzar `@PJL INFO VARIABLES` y `@PJL INFO CONFIG`, y después ir probando `DINQUIRE` sobre cualquier nombre de variable sospechoso que aparezca ahí, en lugar de asumir a ciegas comandos de otros fabricantes.

Con esta referencia ya tenemos vocabulario suficiente para entender exactamente qué hace cada línea del código que viene a continuación.

### Construyendo una herramienta de auditoría: `hackPrinter.py`

Escribir cada comando PJL a mano con `telnet` es viable para probar dos o tres cosas sueltas, pero se queda corto en cuanto queremos hacer un reconocimiento serio: navegar directorios, descargar ficheros completos, alternar entre variables, o simplemente repetir el proceso sobre varias impresoras de forma sistemática. Para eso construimos un cliente propio en `python3` que actúa como **traductor**: expone comandos con nombres humanos (`ls`, `id`, `get`, `put`, `rm`, `set`, `default`...) y por debajo genera el PJL real equivalente — mostrándolo siempre en pantalla, para que se vea exactamente qué se está enviando "por detrás" y sirva también como material de aprendizaje del protocolo.

#### Arquitectura del script

El script se organiza en cinco capas con responsabilidades claramente separadas:

1. **`PJLTransport`** — Maneja la conexión TCP cruda (socket), el envío/recepción de datos, los timeouts y los reintentos. Es la única clase que toca la red directamente.
2. **`PJLProtocol`** — Construye las cadenas PJL correctas (el "diccionario" del protocolo, uno por uno documentados en la tabla de referencia anterior) y parsea las respuestas.
3. **`PJLClient`** — API de alto nivel ("traductor"): métodos con nombres humanos (`ls`, `get_file`, `put_file`, `whoami`...) que internamente llaman a `PJLProtocol` + `PJLTransport`.
4. **`PJLShell`** — Interfaz interactiva tipo shell (REPL) que mapea comandos escritos por el usuario a métodos de `PJLClient`.
5. **CLI (`main`)** — Parseo de argumentos para uso no interactivo / scriptable (automatización, integración en otras herramientas, pipelines de pentesting).

El script es **cross-platform** y únicamente usa la librería estándar de Python 3 (`socket`, `argparse`, `logging`, `shlex`, `cmd`, `dataclasses`...), por lo que funciona igual en Windows, Linux y macOS sin dependencias externas — nada que instalar con `pip`.

Un par de decisiones de diseño que merece la pena resaltar antes de leer el código:

* **Se abre una conexión TCP nueva por cada comando**, en lugar de mantener un socket persistente. Muchas impresoras cierran la sesión tras cada intercambio PJL, así que reabrir conexión es más robusto que gestionar reconexiones silenciosas a mitad de un comando.
* **La lectura de la respuesta se basa en un timeout de silencio**, no en un delimitador de "fin de mensaje": PJL es texto plano y no todas las implementaciones marcan de forma fiable dónde termina una respuesta, así que el script simplemente sigue leyendo mientras lleguen datos y se detiene cuando la impresora se queda en silencio un tiempo prudencial.
* **Los comandos destructivos piden confirmación explícita** en el modo shell (`rm`, `put`, `default`, `fsinit`), precisamente porque comandos como `@PJL DEFAULT` o `@PJL FSINIT` pueden dejar el dispositivo inutilizable o borrar datos de forma irreversible.

A continuación, el código completo y comentado:

> `hackPrinter.py`

{% file src="../../.gitbook/assets/hackPrinter.py" %}

### Uso práctico de la herramienta

#### Modo shell interactivo

Con la impresora ya localizada (`192.168.1.21`, según nuestro escaneo inicial), lanzamos el shell interactivo:

```bash
python3 hackPrinter.py --host 192.168.1.21 shell
```

Salida:

```
=== PJL-Toolkit :: shell interactivo ===
Escribe 'help' para ver comandos disponibles, 'exit' para salir.

pjl@192.168.1.21:9100>
```

**Reconocimiento básico — identificar el dispositivo:**

```bash
pjl@192.168.1.21:9100> id
[11:59:36] INFO       ↳ PJL enviado: <UEL>@PJL INFO ID\r\n<UEL>\r\n
@PJL INFO ID
"Brother CFP-L1820ER series:9E4-L7G:Ver.N"
```

Como se puede ver, la herramienta muestra siempre el comando PJL real que se está enviando (`@PJL INFO ID`) justo antes de imprimir la respuesta — así se aprende la traducción shell → PJL en cada interacción, en lugar de tratar el script como una caja negra.

**Listar el sistema de ficheros interno** (si el modelo no lo tiene restringido; en algunos dispositivos esta funcionalidad viene deshabilitada de fábrica o requiere contraseña):

```bash
pjl@192.168.1.21:9100> ls
[13:23:33] INFO       ↳ PJL enviado: <UEL>@PJL FSDIRLIST NAME="0:" ENTRY=1 COUNT=999\r\n<UEL>\r\n
TIPO      TAMANO  NOMBRE
DIR            -  .
DIR            -  ..
DIR            -  pcl
FILE          51  scan001.pdf
FILE          45  scan002.pdf
DIR            -  config
DIR            -  scans
```

Aquí ya vemos ficheros y directorios reales dentro del firmware — en un caso real, `scan001.pdf`/`scan002.pdf` podrían ser documentos escaneados por usuarios legítimos de la organización, y `config` podría contener credenciales de red guardadas para el envío automático de escaneos.

**Consultar los volúmenes disponibles y sus permisos:**

```bash
pjl@127.0.0.1:9100> volumes
[13:23:40] INFO       ↳ PJL enviado: <UEL>@PJL INFO FILESYS\r\n<UEL>\r\n
VOLUME TOTAL SIZE FREE SPACE LOCATION LABEL STATUS
0:     1755136    1718272    <HT>     <HT>  READ-WRITE
```

El estado `READ-WRITE` confirma que el volumen no solo se puede leer (`FSUPLOAD`/`FSDIRLIST`), sino también escribir (`FSDOWNLOAD`) y borrar (`FSDELETE`) — es decir, permisos peligrosos desde el punto de vista de seguridad: con esto ya podemos descargar, subir, leer y listar ficheros libremente.

#### Modo scriptable / no interactivo (CLI)

Para automatizar auditorías sobre varias impresoras o integrar la herramienta en un pipeline, todos los comandos anteriores están también disponibles como subcomandos de `argparse`, por ejemplo:

```bash
python3 hackPrinter.py --host 192.168.1.21 id
python3 hackPrinter.py --host 192.168.1.21 ls --path "0:\scans"
python3 hackPrinter.py --host 192.168.1.21 get --remote "0:\scans\scan001.pdf" --local ./evidencia.pdf
```

#### Modo `--original` / raw

Si en algún momento se necesita enviar un comando PJL exacto que la capa de traducción no contempla (por ejemplo, una variable propietaria descubierta con `INFO VARIABLES`), el script ofrece también un modo "crudo" que envía el texto tal cual, sin más añadido que el envoltorio UEL obligatorio:

```bash
python3 hackPrinter.py --host 192.168.1.21 --original '@PJL DINQUIRE PASSWORD'
```

### Laboratorio local: honeypot PJL con Docker

Practicar contra una impresora real de terceros, como se ha explicado en el aviso legal, **no es una opción** salvo que sea de tu propiedad o tengas autorización expresa. Para poder entrenar todas estas técnicas de forma segura, legal y repetible, lo mejor es montar un entorno virtual ultra-realista con Docker que simule el comportamiento de una impresora JetDirect real.

Existe un repositorio público pensado exactamente para esto:

**Repositorio:** [github.com/michaelneu/pjl-honeypot](https://github.com/michaelneu/pjl-honeypot)

#### Despliegue

```bash
git clone https://github.com/michaelneu/pjl-honeypot
cd pjl-honeypot/
```

```bash
sudo make build
sudo make run
```

Salida esperada:

```
docker run \
	--rm \
	-it \
	-p 9100:9100 \
    -v `pwd`/prints:/app/prints \
	honeynet-jetdirect
2026-08-22 11:23:19,457 [INFO]	listening on port 9100
```

Con esto el honeypot ya tiene el puerto 9100 abierto y accesible en `127.0.0.1:9100` (o en la IP del host Docker si se despliega en otra máquina de la red), listo para recibir comandos PJL exactamente igual que una impresora física.

#### Corrigiendo el comportamiento del honeypot

El honeypot original tiene, tal como viene de fábrica, algunos comandos implementados como _stubs_ vacíos que no llegan a devolver contenido real (por ejemplo, `FSUPLOAD` no leía realmente del sistema de ficheros simulado). Para que el laboratorio se comporte de forma fiel a una impresora real — y así poder practicar de verdad la descarga de ficheros con `get`/`FSUPLOAD` — sustituimos el fichero `jetdirect.py` del repositorio por esta versión mejorada, que:

* Implementa `FSUPLOAD` leyendo de verdad de un sistema de ficheros simulado en memoria (`Filesystem`), en lugar de devolver siempre una cadena vacía.
* Conecta el volumen virtual `0:\scans` con una carpeta real del contenedor (compartida por volumen Docker), de modo que un fichero subido desde la web de administración del honeypot aparezca inmediatamente al hacer `ls 0:\scans` sin necesidad de reiniciar el servicio.
* Mantiene fieles el resto de comandos estándar (`INFO ID/STATUS/VARIABLES/FILESYS`, `FSDIRLIST`, `FSQUERY`, `RDYMSG`, `USTATUS`...) para que la herramienta `hackPrinter.py` se comporte exactamente igual que contra hardware real.

> `jetdirect.py`

{% file src="../../.gitbook/assets/jetdirect.py" %}

Tras aplicar el cambio, hay que reconstruir y relanzar el contenedor:

```bash
sudo make build && sudo make run
```

Una vez desplegado de nuevo, ya podemos apuntar `hackPrinter.py` contra el laboratorio local y repetir toda la investigación anterior con total libertad:

```bash
python3 hackPrinter.py --host 127.0.0.1 --port 9100 shell
```

Este entorno es ideal para practicar de forma segura los comandos destructivos de la tabla de referencia (`FSDELETE`, `FSINIT`, `DEFAULT`) sin arriesgar hardware real ni incurrir en ningún problema legal.

### Mitigaciones y defensa

Todo lo anterior tiene su contrapartida defensiva. Si administras impresoras de red, estas son las medidas que realmente reducen la superficie de ataque descrita en esta guía:

1. **Segmentación de red (VLANs).** Aislar las impresoras en una VLAN dedicada, accesible únicamente desde los segmentos de red que realmente necesitan imprimir, y bloquear el acceso directo al puerto 9100 desde el resto de la red — tal como se menciona al principio de esta guía, es la mitigación más efectiva y la que ya aplican muchas empresas.
2. **Filtrado a nivel de firewall/ACL.** Restringir el puerto 9100 (y 631, 515, 161, el panel web de administración) mediante reglas de firewall, en lugar de confiar únicamente en la topología de red.
3. **Contraseña PJL (`@PJL SECURITY PASSWORD=`).** Muchos modelos permiten proteger los comandos `DEFAULT` (y a veces también `FS*`) con una contraseña numérica. No es infalible, pero eleva la barrera de entrada frente a un atacante oportunista.
4. **Deshabilitar el sistema de ficheros PJL si no se usa.** Si el modelo lo permite, desactivar el acceso `FS*` reduce drásticamente el impacto de un acceso no autorizado, ya que impide la lectura/escritura de ficheros aunque el puerto siga abierto.
5. **Actualizar el firmware.** Los fabricantes publican periódicamente parches para extensiones propietarias vulnerables (como los casos conocidos de `DMCMD` en Kyocera); mantener el firmware al día cierra estas vías adicionales.
6. **Monitorización.** Registrar y alertar sobre conexiones inusuales al puerto 9100, especialmente desde equipos que normalmente no imprimen, puede detectar un reconocimiento o ataque en curso antes de que se complete.
7. **Borrado de datos sensibles.** Configurar la impresora para no retener copias de los trabajos escaneados/impresos más tiempo del necesario, y revisar periódicamente qué credenciales de red (SMB, FTP, correo) tiene guardadas en su configuración.

### Conclusión y recursos

PJL es un ejemplo perfecto de cómo un protocolo de los años 90, diseñado en una época sin apenas consideraciones de seguridad, sigue vivo y sin autenticación en miles de dispositivos corporativos actuales. Con muy poca fricción técnica — un socket TCP y un puñado de comandos de texto plano — es posible pasar de "descubrir un puerto abierto" a "leer documentos escaneados" o "dejar una impresora inutilizable". Esa misma sencillez es la razón por la que merece la pena auditarlo de forma proactiva en cualquier red corporativa.

**Recursos relacionados para profundizar:**

* Repositorio del laboratorio: [github.com/michaelneu/pjl-honeypot](https://github.com/michaelneu/pjl-honeypot)
* Herramienta de referencia de la comunidad para este tipo de auditorías: **PRET (Printer Exploitation Toolkit)**, que además de PJL soporta PostScript y PCL.
* _HP PJL Technical Reference Manual_, la especificación original en la que se basa la tabla de comandos de esta guía.

Recuerda siempre: reconocimiento, explotación y documentación van de la mano con **autorización explícita**. El objetivo final de todo pentester ético no es solo "romper cosas", sino dejar el sistema auditado con una lista clara de mitigaciones aplicables — como la sección anterior.
