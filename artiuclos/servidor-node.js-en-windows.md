---
icon: square-js
layout:
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
---

# Servidor Node.js en Windows

Para nosotros poder alojar una pagina web a nivel local pero sin limitaciones sobre `JavaScript` u otro tipo de cosas, en vez de abrir un servidor de `Python3` el cual tambien trae sus limitaciones, podremos utilizar `Node.js` todo esto para `Windows`, para ello primero tendremos que descargarnos dicho `Software`.

URL = [Download Node.js](https://nodejs.org/es)

Antes de abrir nuestro `PowerShell` tendremos definir las variables de entorno en `Windows` para que nos las pille bien.

Abriremos `Ediatr las variables de entorno del sistema` viendo algo asi:

<figure><img src="../.gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>

Tendremos que darle a `Variables de entorno...`, dentro de esta parte:

<figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

Le daremos a `Editar` seleccionando `Path`, dentro de esa parte tendremos que darle a `Nueva` y seleccionar los ejecutables para que cuando los llamemos de forma relativa los ejecute directamente sin necesidad de llamar a la ruta absoluta:

Tiene que quedar algo asi.

<figure><img src="../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>

Suele estar en la ruta expuesta en la imagen, echo eso le daremos a `Aceptar` y ahora si abriremos un `PowerShell`, nos iremos al directorio donde esta la pagina web y ejecutaremos los siguiente comandos.

```powershell
cd \<PATH>\page_example\
```

Ahora iniciaremos el `Node.js` dentro de la carpeta donde queremos que coja todo (`Pagina web`).

```powershell
npm init -y
```

Instalamos antes un requisito para que funcione el servidor de `Node.js` que vamos a crear:

```powershell
npm install express
```

Ahora crearemos un archivo llamado `server.js` dentro de la raiz de la carpeta de la pagina web.

> server.js

```js
const express = require('express');
const path = require('path');

const app = express();
const port = 3000;  // Puedes cambiar el puerto si lo prefieres

// Servir archivos estáticos desde la carpeta actual
app.use(express.static(path.join(__dirname, '')));

// Ruta de prueba
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html')); // Cambia esto según tu archivo inicial
});

// Iniciar el servidor
app.listen(port, () => {
  console.log(`Servidor escuchando en http://localhost:${port}`);
});
```

Lo guardamos y con esto estaria preparado para ejecutar el archivo `server.js` y que corra nuestra pagina web en este caso por el puerto `3000` por el `localhost`.

```powershell
node server.js
```

Info:

```
Servidor escuchando en http://localhost:3000
```

Ahora si entramos a dicha direccion veremos nuestra pagina web de forma correcta y sin ningun tipo de restricciones.
