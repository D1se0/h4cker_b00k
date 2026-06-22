# Técnicas de ofuscación: minificación y packing

## Punto de partida: código legible

```js
console.log('HTB JavaScript Deobfuscation Module');
```

Una línea simple que imprime un mensaje. Vamos a verla transformarse a través de distintas técnicas, de menor a mayor complejidad.

## Minificación: el primer nivel (apenas ofuscación real)

La **minificación** comprime todo el código en el menor espacio posible: elimina espacios, saltos de línea y comentarios innecesarios, a menudo dejando todo en una sola línea (frecuentemente muy larga). Su propósito principal **no es ocultar nada** — es reducir el tamaño del archivo para que cargue más rápido. El efecto de dificultar la lectura es, en cierto modo, un efecto colateral.

```js
console.log('HTB JavaScript Deobfuscation Module');
```

En una línea ya tan corta como esta, minificar apenas cambia nada visualmente — el verdadero impacto de la minificación se nota en archivos grandes con cientos o miles de líneas, donde comprimir todo en una única línea (o pocas) hace la lectura manual mucho más tediosa, aunque técnicamente cada token siga siendo legible.

> Los archivos minificados suelen guardarse con la extensión `.min.js`, una convención útil para reconocerlos a simple vista durante el reconocimiento.

## Packing: el siguiente nivel

El **empaquetado** (*packing*) va bastante más lejos: transforma el código en una función `eval()` que reconstruye el programa original en tiempo de ejecución, a partir de un diccionario de palabras codificadas.

```js
eval(function(p,a,c,k,e,d){
  e=function(c){return c};
  if(!''.replace(/^/,String)){
    while(c--){d[c]=k[c]||c}
    k=[function(e){return d[e]}];
    e=function(){return'\\w+'};
    c=1
  };
  while(c--){
    if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}
  }
  return p
}('5.4(\'3 2 1 0\');',6,6,'Module|Deobfuscation|JavaScript|HTB|log|console'.split('|'),0,{}))
```

### Cómo reconocer el packing a simple vista

Una firma muy característica: la función inicial declarada con exactamente seis parámetros, `function(p,a,c,k,e,d)`. Esta convención de nombres (heredada del empaquetador "Packer" original, muy popular) es casi siempre reconocible incluso cuando el resto del código varía entre distintas herramientas.

### Cómo funciona conceptualmente

1. El código original se descompone en un diccionario de "tokens" (palabras y símbolos), representado por el array `k` (por ejemplo, `'Module|Deobfuscation|JavaScript|HTB|log|console'.split('|')`).
2. El código real se sustituye por una versión compacta usando referencias numéricas/codificadas a ese diccionario (`'5.4(\'3 2 1 0\');'`).
3. En tiempo de ejecución, la función reconstruye la cadena original sustituyendo cada referencia por su palabra correspondiente del diccionario, y finalmente la ejecuta con `eval()`.

### La debilidad del packing básico

Aunque el resultado es bastante más difícil de leer que el original, **las cadenas de texto del diccionario siguen estando en texto plano** dentro del propio código (`'Module|Deobfuscation|JavaScript|HTB|log|console'`). Esto puede revelar pistas directas sobre la funcionalidad del script con solo mirar esas palabras sueltas — sin necesidad de desofuscar nada todavía.

## Probando el código (legítimo y seguro)

Servicios como [JSConsole](https://jsconsole.com/) permiten pegar y ejecutar fragmentos de JavaScript de forma aislada en el navegador, ideal para confirmar que una versión ofuscada (o desofuscada) produce el mismo comportamiento que el original — sin tener que cargarla dentro de una página real.

> **Precaución**: nunca se debe ejecutar JavaScript de origen desconocido o sospechoso (por ejemplo, extraído de una muestra de malware real) en un navegador normal con sesiones activas. Para análisis de código potencialmente malicioso, conviene usar un entorno aislado y desconectado (sandbox), no la propia máquina de trabajo.
