# Ofuscación avanzada

## Más allá del packing básico

El packing simple, como vimos, deja expuestas las cadenas de texto originales dentro del propio código. Los ofuscadores avanzados resuelven esta debilidad codificando también esas cadenas, eliminando cualquier rastro legible del programa original.

## Codificación de cadenas (string array encoding)

Herramientas como [obfuscator.io](https://obfuscator.io/) permiten, además de aplicar packing, **codificar el array de cadenas** (por ejemplo, en Base64), de forma que ni siquiera las palabras del "diccionario" interno sean legibles directamente:

```js
var _0x1ec6=['Bg9N','sfrciePHDMfty3jPChqGrgvVyMz1C2nHDgLVBIbnB2r1Bgu='];
(function(_0x13249d,_0x1ec6e5){ ... }(_0x1ec6,0xb4));
var _0x14f8=function(_0x13249d,_0x1ec6e5){ ...decodifica Base64 internamente... };
console[_0x14f8('0x0')](_0x14f8('0x1'));
```

Aquí no queda ningún rastro textual del programa original: ni `console.log` ni el mensaje aparecen en claro en ningún punto del código — todo se reconstruye dinámicamente, capa sobre capa, en tiempo de ejecución.

## El extremo: ofuscación que reescribe la sintaxis entera

Algunos ofuscadores van todavía más lejos, reescribiendo el código usando exclusivamente un puñado muy reducido de caracteres. El ejemplo más extremo es **JSFuck**, que reescribe cualquier programa JavaScript utilizando únicamente seis caracteres: `[`, `]`, `(`, `)`, `!`, `+`.

```js
[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+...
```

El resultado es completamente ilegible y, además, **notablemente más lento** de ejecutar — un coste de rendimiento real, no solo cosmético, derivado de tener que reconstruir cada operación básica a partir de estas combinaciones mínimas de caracteres.

Otras técnicas similares en el mismo espíritu incluyen **JJEncode** y **AAEncode**, que transforman el código en representaciones visualmente curiosas (emoticonos, símbolos repetidos) manteniendo la funcionalidad intacta.

## El trade-off rendimiento vs. ofuscación

Cuanto más agresiva es la ofuscación, mayor es el impacto en el rendimiento de ejecución — reconstruir un programa completo a partir de combinaciones mínimas de caracteres, o decodificar múltiples capas de codificación en cada llamada, tiene un coste de CPU real. Por esta razón, técnicas como JSFuck rara vez se usan en producción legítima de forma generalizada; se reservan para casos muy concretos donde ocultar la lógica es más prioritario que el rendimiento — típicamente, para evadir filtros o restricciones específicas de un entorno (por ejemplo, restricciones de contenido que solo permiten ciertos caracteres).

## Implicación práctica para quien analiza el código

Cuanto más avanzada es la ofuscación, **menos útiles son las herramientas automáticas de desofuscación genéricas**, y más necesario se vuelve recurrir a:

- **Ejecución controlada y observación**: en lugar de intentar leer el código estáticamente, ejecutarlo en un entorno aislado y observar su comportamiento real (qué peticiones hace, qué valores produce).
- **Ingeniería inversa manual**: entender paso a paso la lógica de reconstrucción del propio ofuscador, en lugar de esperar que una herramienta genérica lo resuelva automáticamente — especialmente cierto cuando se trata de un ofuscador personalizado, diseñado a medida precisamente para resistir las herramientas conocidas.

El siguiente apartado retoma esta idea con el proceso práctico de desofuscación, empezando por los casos más tratables (packing básico) antes de plantear qué hacer cuando las herramientas automáticas no son suficientes.
