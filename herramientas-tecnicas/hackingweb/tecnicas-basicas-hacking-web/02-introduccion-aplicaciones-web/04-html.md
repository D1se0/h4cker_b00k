# HTML y el DOM

## HTML como base de toda página web

HTML (*HyperText Markup Language*) es el componente fundamental de cualquier página web: define la estructura y el contenido —títulos, párrafos, formularios, imágenes, enlaces— que el navegador interpreta y renderiza.

```html
<!DOCTYPE html>
<html>
    <head>
        <title>Page Title</title>
    </head>
    <body>
        <h1>A Heading</h1>
        <p>A Paragraph</p>
    </body>
</html>
```

Los elementos HTML se organizan en forma de **árbol**, de manera similar a otros lenguajes de marcado como XML:

```
document
 - html
   -- head
      --- title
   -- body
      --- h1
      --- p
```

Cada elemento se abre y se cierra con una etiqueta (`<p>...</p>`), y puede llevar atributos como `id` o `class` que sirven para identificarlo de forma única o agruparlo con otros, algo imprescindible para que CSS y JavaScript puedan referenciarlo.

## El DOM (Document Object Model)

El **DOM** es la representación en memoria, en forma de árbol de objetos, de la página HTML que el navegador ha cargado. El W3C lo define como una interfaz neutral de plataforma y lenguaje que permite a programas y scripts acceder y modificar dinámicamente el contenido, la estructura y el estilo de un documento.

El estándar DOM se divide en tres partes:

- **Core DOM**: modelo base para cualquier tipo de documento.
- **XML DOM**: modelo específico para documentos XML.
- **HTML DOM**: modelo específico para documentos HTML.

Gracias al DOM, se puede acceder a cualquier elemento de la página vía JavaScript: `document.body`, `document.getElementById('miElemento')`, etc.

### Por qué el DOM es crítico para un pentester

Entender el árbol DOM es la base para comprender —y explotar— vulnerabilidades de tipo **XSS basado en DOM**: cuando una entrada de usuario se inyecta directamente en el árbol DOM (por ejemplo, vía `innerHTML`, `document.write()`, o atributos manipulados dinámicamente) sin sanitización, un atacante puede inyectar HTML o JavaScript arbitrario que se ejecutará en el contexto de la página de la víctima. Profundizaremos en esto en el bloque dedicado a XSS.

Saber localizar elementos por su `id`, etiqueta o clase también es esencial al inspeccionar el código fuente de una página en busca de comportamientos inesperados, formularios ocultos, o puntos de inyección.

## Codificación de URL (Percent-Encoding)

Las URLs solo admiten de forma nativa el conjunto de caracteres ASCII. Cualquier carácter fuera de ese conjunto —o que tenga un significado especial dentro de la sintaxis de la URL (`&`, `?`, `=`, espacios, etc.)— debe **codificarse** reemplazándolo por un símbolo `%` seguido de su valor hexadecimal.

| Carácter | Codificación |
|---|---|
| espacio | `%20` (o `+` en *query strings*) |
| `!` | `%21` |
| `"` | `%22` |
| `#` | `%23` |
| `$` | `%24` |
| `%` | `%25` |
| `&` | `%26` |
| `'` | `%27` |
| `(` | `%28` |
| `)` | `%29` |

> **Relevancia ofensiva**: la codificación URL es una de las técnicas de **evasión de filtros** más usadas en pentesting. Si una aplicación filtra la cadena `<script>` en busca de XSS pero no decodifica adecuadamente antes de aplicar el filtro (o lo hace en el orden incorrecto), enviar el payload codificado (`%3Cscript%3E`) puede saltarse esa comprobación. La misma idea se aplica a inyecciones SQL, path traversal, y prácticamente cualquier filtro basado en coincidencia de cadenas. Volveremos sobre esta técnica repetidamente a lo largo del temario.

Herramientas como Burp Suite incluyen un codificador/decodificador integrado (*Decoder*) que permite convertir cadenas entre distintos esquemas de codificación (URL, Base64, HTML entities, etc.) de forma rápida durante una auditoría.
