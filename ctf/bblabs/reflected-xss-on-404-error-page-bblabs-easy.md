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
  tags:
    visible: true
  actions:
    visible: true
---

# Reflected XSS on 404 Error Page BBLabs (Easy)

# Despliegue del Lab

En la propia página buscaremos una de las dos opciones que nos permiten desplegar el lab. En mi caso elegiré la que me crea un subdominio de la página para poder iniciar el lab y empezar a hackearlo.

El objetivo de estos Labs es encontrar la flag final.
# Objetivo

```
Red social donde la página de error 404 refleja el parámetro message en el HTML sin sanitizar, permitiendo XSS reflejado.
```
## Exploración inicial

Entrando dentro de la página veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20260819112417.png" alt=""><figcaption></figcaption></figure>

Hay un login con opción de registro. La pista del lab nos indica que el vector de ataque está en la página de error `404`. Accedemos directamente a la URL que el enunciado nos proporciona al desplegar el lab:

```
URL = https://pf2kvqxppv.lab.bblabs.es/404?message=La ruta no existe
```

Info:

<figure><img src="../../.gitbook/assets/Pasted image 20260819112627.png" alt=""><figcaption></figcaption></figure>
## Identificación del parámetro vulnerable

La página de error muestra el texto `La ruta no existe` directamente en el HTML. El parámetro `message` viaja en la URL como parámetro `GET`, lo que significa que cualquier usuario puede modificarlo simplemente cambiando la URL en el navegador. Esto es la condición necesaria para un **XSS reflejado**: el servidor toma el valor del parámetro y lo inserta directamente en la respuesta HTML sin transformarlo ni validarlo.

Confirmamos que el parámetro se refleja modificando su valor:

<figure><img src="../../.gitbook/assets/Pasted image 20260819112722.png" alt=""><figcaption></figcaption></figure>

El texto que introducimos aparece renderizado en la página. El siguiente paso es comprobar si el servidor aplica alguna sanitización que bloquee etiquetas HTML o JavaScript.
## Explotación del XSS reflejado

A diferencia del **XSS almacenado** (donde el payload se guarda en el servidor y afecta a todos los visitantes), el **XSS reflejado** viaja en la propia URL y solo se ejecuta en el navegador del usuario que abre esa URL concreta. En un ataque real, el atacante envía al objetivo un enlace malicioso ya preparado.

Probamos un payload con una etiqueta `<script>` y una alerta JavaScript:

```
URL = https://pf2kvqxppv.lab.bblabs.es/404?message=<script>alert('XSS')</script>
```

Info:

<figure><img src="../../.gitbook/assets/Pasted image 20260819112835.png" alt=""><figcaption></figcaption></figure>

El navegador ejecuta el `alert()` en lugar de mostrar el texto literal de la etiqueta. Esto confirma que el servidor inserta el valor del parámetro directamente en el DOM sin ninguna sanitización: ni codificación HTML (`&lt;`, `&gt;`) ni filtrado de etiquetas.

En un entorno real, este tipo de vulnerabilidad permite a un atacante robar cookies de sesión, redirigir a páginas maliciosas o ejecutar acciones en nombre del usuario que abra el enlace manipulado.

