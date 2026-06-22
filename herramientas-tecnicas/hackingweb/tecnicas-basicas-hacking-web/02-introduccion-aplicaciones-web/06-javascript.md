# JavaScript

## El lenguaje que da vida a la interfaz

Mientras que HTML define la estructura y CSS la presentación, **JavaScript** es lo que aporta comportamiento e interactividad: procesar eventos (clics, envíos de formulario), modificar el DOM en tiempo real, validar entradas antes de enviarlas, realizar peticiones asíncronas al backend (vía `fetch` o, históricamente, AJAX) sin necesidad de recargar la página completa.

Sin JavaScript, una aplicación web sería esencialmente estática. Es, junto con HTML y CSS, lo que se conoce como "la trinidad" del frontend.

```html
<script type="text/javascript">
  // código JavaScript embebido
</script>

<script src="./script.js"></script>  <!-- código JavaScript remoto -->
```

```js
document.getElementById("button1").innerHTML = "Changed Text!";
```

## Por qué JavaScript es el terreno de juego de XSS

JavaScript se ejecuta directamente en el navegador del usuario, con acceso al DOM completo de la página actual, a las cookies (salvo que estén protegidas con `HttpOnly`), al `localStorage`, y a la capacidad de realizar peticiones HTTP en nombre del usuario autenticado.

Esto es exactamente lo que convierte a **Cross-Site Scripting (XSS)** en una de las vulnerabilidades más impactantes del lado del cliente: si un atacante consigue que su propio JavaScript se ejecute en el navegador de la víctima —dentro del contexto de origen de la aplicación legítima—, hereda efectivamente todo lo que JavaScript puede hacer en esa página: leer cookies, realizar acciones en nombre del usuario, redirigir, modificar el contenido visible, etc. Lo veremos en detalle en el bloque dedicado específicamente a XSS.

## Frameworks de JavaScript

A medida que las aplicaciones crecen en complejidad, escribir toda la lógica de interfaz "a mano" se vuelve poco práctico. De ahí la popularidad de frameworks/librerías como:

- **React** (Meta)
- **Angular** (Google)
- **Vue**
- **jQuery** (más antiguo, pero todavía extendido en aplicaciones legacy)

Estos frameworks introducen el concepto de DOM dinámico (la interfaz se "re-renderiza" en respuesta a cambios de estado, sin recargar la página) y suelen compilar o transpilar su propio código a JavaScript estándar para que el navegador pueda ejecutarlo.

### Relevancia para reconocimiento

Identificar qué framework usa una aplicación (visible en el código fuente, en los nombres de archivos JS cargados, o en atributos `data-react-*` u otros marcadores) ayuda a anticipar patrones de vulnerabilidad conocidos de ese framework concreto (por ejemplo, problemas históricos de XSS en plantillas mal escapadas de ciertas versiones, o vulnerabilidades de deserialización en frameworks de backend asociados como Node/Express).

## Backend en JavaScript: Node.js

Aunque JavaScript nació como lenguaje exclusivamente de frontend, **Node.js** permite ejecutarlo también en el servidor, dando lugar a aplicaciones full-stack escritas enteramente en JavaScript. Esto introduce su propio conjunto de vulnerabilidades específicas (inyección de comandos vía `child_process`, deserialización insegura, prototype pollution), que veremos en bloques posteriores cuando corresponda.

## JavaScript ofuscado

Es habitual que aplicaciones en producción sirvan su JavaScript **minificado** (eliminando espacios y comentarios para reducir tamaño) o **ofuscado** (transformando deliberadamente el código para dificultar su lectura humana, sin afectar su comportamiento). Como pentester, es frecuente encontrarse con código JS ofuscado que conviene desentrañar para entender la lógica de validación del lado del cliente, encontrar endpoints internos no documentados, o localizar claves/tokens embebidos por error. Esta habilidad se trabaja en profundidad en el bloque de *JavaScript Deobfuscation*.
