# Desofuscación: beautify y unpacking

## Primer paso: embellecer (Beautify)

Antes de intentar desofuscar nada, si el código está **minificado** (todo en una línea, sin formato), el primer paso es simplemente reformatearlo con indentación y saltos de línea legibles — esto no revierte la ofuscación real, pero hace mucho más cómodo trabajar con el código en los pasos siguientes.

### Opciones para embellecer

- **DevTools del navegador**: en Firefox, el depurador (`Ctrl+Shift+Z`) incluye un botón **`{ }` (Pretty Print)** que reformatea automáticamente el script abierto.
- **Herramientas en línea**: [Prettier](https://prettier.io/playground/), [Beautifier](https://beautifier.io/).

Tras embellecer un script con *packing*, el resultado sigue conteniendo la llamada `eval()` y su diccionario codificado — solo ahora con formato legible:

```js
eval(function (p, a, c, k, e, d) {
  e = function (c) { return c.toString(36) };
  if (!''.replace(/^/, String)) {
    while (c--) { d[c.toString(a)] = k[c] || c.toString(a) }
    ...
  }
  return p
}('g 4(){0 5="6{7!}"...', 17, 17, 'var|xhr|url|null|generateSerial|...'.split('|'), 0, {}))
```

Formatear ayuda a la legibilidad, pero **no revierte** el packing en sí — para eso hace falta una herramienta de desofuscación dedicada.

## Desofuscando packing con herramientas dedicadas

[UnPacker](https://matthewfl.com/unPacker.html) está diseñado específicamente para revertir el formato de *packing* visto en el apartado anterior: en lugar de ejecutar el código, simula la reconstrucción que haría `eval()` y muestra el resultado en texto legible, sin llegar a ejecutarlo realmente.

```js
function generateSerial() {
  var flag = "HTB{...}";
  var xhr = new XMLHttpRequest;
  var url = "/serial.php";
  xhr.open("POST", url, true);
  xhr.send(null);
};
```

> **Consejo práctico**: al pegar código en herramientas de desofuscación online, evitar dejar líneas en blanco antes del script — puede interferir con el proceso de análisis y dar resultados incorrectos o incompletos.

## Técnica manual alternativa: interceptar el `return`

Una forma alternativa de "desempaquetar" sin depender de una herramienta externa: identificar la línea `return p` (u operación equivalente) al final de la función empaquetadora, y sustituirla por `console.log(p)` en lugar de dejar que se ejecute con `eval()`. Esto imprime el código reconstruido en la consola sin llegar a ejecutarlo — útil tanto como medida de seguridad (evita ejecutar código potencialmente malicioso) como de control sobre el proceso.

## Cuándo las herramientas automáticas dejan de ser suficientes

Las herramientas de desofuscación funcionan bien contra técnicas **conocidas y estandarizadas** (el packer clásico de seis parámetros, por ejemplo). Pero a medida que la ofuscación se vuelve más sofisticada —especialmente si se trata de un **ofuscador personalizado**, desarrollado a medida específicamente para resistir herramientas conocidas— estas herramientas genéricas pierden eficacia rápidamente.

En esos casos, no queda más remedio que recurrir a **ingeniería inversa manual**: leer con paciencia la lógica del propio mecanismo de ofuscación, entender cómo reconstruye el código original paso a paso, y replicar ese proceso manualmente (o escribiendo un script propio que automatice esa reconstrucción concreta). Es un terreno que se solapa directamente con el análisis de malware y la ingeniería inversa de software en general — disciplinas que merecen su propio estudio en profundidad más allá del alcance introductorio de este bloque.

## El flujo de trabajo completo, resumido

1. **Embellecer** (Pretty Print) si el código está minificado.
2. **Identificar el tipo de ofuscación** (packing clásico de seis parámetros, codificación de cadenas, técnicas extremas tipo JSFuck).
3. **Aplicar la herramienta de desofuscación correspondiente** al tipo identificado.
4. **Repetir** si hay múltiples capas de ofuscación anidadas (es común encontrar un packing dentro de otro, o seguido de una capa adicional de codificación de texto, que se trata en el apartado de *Decodificación* de este mismo bloque).
5. Cuando las herramientas automáticas no avanzan más, pasar a **análisis manual** del código resultante — el tema del siguiente apartado.
