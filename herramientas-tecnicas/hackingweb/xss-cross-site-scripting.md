---
icon: code
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

# XSS (Cross Site Scripting)

### Lab: Reflected XSS into HTML context with nothing encoded

Basicamente lo que te pide aqui es que haga un `alert` aprovechando la vulnerabilidad de `XSS` que tiene esa pagina...

Habra un panel de busqueda, ahi sera donde inyectemos el codigo `XSS`...

```html
<script>alert('XSS')</script>
```

Esto hara que nos salte una `alerta` cuando le demos a buscar, por lo que este `lab` ya estaria resuelto...

### Lab: Stored XSS into HTML context with nothing encoded

En este caso hay que hacer lo mismo que antes pero con la pequeña diferencia de que no estara al principio, nos tendremos que meter en algun `Post` donde abajo del todo se encontrara un formulario para enviar un comentario, tanto en el campo de `Comment` como en el de `Name` seran vulnerables a `XSS`, por lo que tendremos que poner lo siguiente...

```html
<script>alert('XSS')</script>
```

La enviar esto ya habriamos resuelto este `lab`...

### Lab: DOM XSS in `document.write` sink using source `location.search`

Aqui lo que hay que hacer es lo mismo que lo anterior pero intentar `bypassear` el script para que pueda ser inyectado, tendremos que irnos a la parte vulnerable de la pagina de `XSS` que sera el `search`, cuando buscas algo en la `URL` te aparece `?search=` por lo que por ahi intentaremos inyectarlo...

Si ponemos lo de siempre...

```html
<script>alert('XSS')</script>
```

No funcionara, pero si ponemos esto si...

Ya que lo que estamos haciendo es cerrar lo que viene en el codigo que no se ve y ejecutar nosotros lo que queremos hacer en este caso un `alert`...

(Si `document.write` está escribiendo dentro de una etiqueta HTML específica, puede que necesites encapsular tu carga útil de manera diferente.)

```html
"><script>alert('XSS')</script>
```

Nos aparecera una alerta y ya lo habriamos resuelto el `lab`...

### Lab: DOM XSS in `innerHTML` sink using source `location.search`

Aqui lo que nos dice es que el codigo se encuentra dentro de un `div` por lo que las inyecciones de codigo normales como hemos estado haciendo no van a valer, lo que tendremos que hacer sera inyectar codigo pero que un `div` pueda soportar, como por ejemplo una imagen...

En el campo de `seatch` en la `URL` inyectaremos lo siguiente...

```html
<img src=x onerror=alert(1)>
```

Lo que quiere decir esto es que esta intentando buscar la direccion de la imagen con `src=` pero tiene una `x` por lo que dara un error, por lo que en `onerror=` lo que dice es que si diera error esa busqueda ejecutaria lo que este ahi que en este caso es `alert(1)` por lo que nos saltaria una alerta y el `lab` estaria hecho...

### Lab: DOM XSS in jQuery anchor `href` attribute sink using `location.search` source

En esta parte lo que haremos sera cambiar el codigo `html` y con el codigo inyectado de lo que cambiamos darle a un boton para que se ejecute ese codgio y asi nos salte una `alerta`...

Cuando estamos dentro vemos un boton llamado `Submit Feedback` por lo que ese sera neustro objetivo, si le damos a `inspeccionar pagina` a tiempo real, nos iremos a la linea donde se encuentra el boton...

```html
<a href="/feedback?returnPath=/feedback">Submit feedback</a>
```

De aqui lo que cambiaremos sera lo siguiente...

```html
<a href="/feedback?returnPath=javascript:alert(document.cookie)">Submit feedback</a>
```

Le damos al boton `Submit Feedback` y se ejecutaria lo que inyectamos...

Esto lo que hara sera que en una alerta nos aparezca la `cookie` del usuario que este recibiendo eso, por lo que ya estaria completado el `lab`...
