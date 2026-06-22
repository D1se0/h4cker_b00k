# Bypass de autenticación por acceso directo

## La forma más simple de eludir la autenticación: pedir el recurso directamente

Hasta ahora, este bloque ha cubierto vulnerabilidades que requieren obtener o adivinar algo (una contraseña, un token, una respuesta de seguridad). El bypass por acceso directo es conceptualmente más simple: ocurre cuando un recurso que **debería** estar protegido es accesible solicitándolo directamente, sin pasar realmente por ninguna comprobación de autenticación efectiva.

## El fallo de fondo: comprobar sin detener la ejecución

El patrón de vulnerabilidad más habitual no es la ausencia total de comprobación, sino una comprobación **incompleta**: el código verifica si el usuario está autenticado y, si no lo está, intenta redirigirlo — pero no detiene la ejecución del resto del script después de esa redirección.

```php
if (!$_SESSION['active']) {
    header("Location: index.php");
}
// El resto del script de la página protegida sigue ejecutándose aquí
```

El problema es que en PHP (y en muchos otros lenguajes), enviar una cabecera de redirección **no interrumpe automáticamente** la ejecución del script — solo añade esa cabecera a la respuesta. Si el desarrollador no añade explícitamente una instrucción de parada justo después, el resto del código de la página protegida se sigue ejecutando y su contenido se sigue generando, terminando en el cuerpo de la respuesta HTTP **aunque el código de estado indique una redirección**.

Esto significa que, técnicamente, los datos protegidos sí viajan en la respuesta — solo que un navegador normal nunca los muestra, porque sigue automáticamente la redirección indicada en la cabecera `Location` antes de que el usuario llegue a ver ese contenido.

## Por qué esto sigue siendo una vulnerabilidad explotable

Un navegador estándar oculta este comportamiento porque sigue la redirección de forma transparente. Pero cualquier herramienta que permita inspeccionar o modificar la respuesta antes de que el navegador la procese automáticamente —como un proxy de intercepción, visto en detalle en el bloque de *Web Proxies*— revela que el contenido protegido ya estaba presente en esa misma respuesta, sin que la redirección llegara a impedir nada realmente.

## La mitigación es igual de simple que el fallo

```php
if (!$_SESSION['active']) {
    header("Location: index.php");
    exit;
}
```

Una única instrucción de parada inmediatamente después de la cabecera de redirección resuelve el problema de raíz: si la ejecución se detiene ahí, ningún contenido posterior de la página protegida llega a generarse ni a incluirse en la respuesta, independientemente de cómo se inspeccione esa respuesta después.

## La lección de fondo

Este es un ejemplo muy claro de por qué **la intención del desarrollador no es suficiente** — el código "parece" proteger el recurso (hay una comprobación, hay una redirección), pero el comportamiento real del lenguaje no garantiza que esa intención se cumpla sin el paso explícito adicional. Es el mismo tipo de fallo sutil de implementación que ha aparecido en otros bloques de este temario: una protección que existe conceptualmente en el código, pero que no se aplica de forma estructuralmente completa.

## Por qué conviene comprobar siempre el cuerpo completo de una respuesta de redirección

Como técnica general de auditoría: ante cualquier redirección hacia una página de login (código `3xx`), vale la pena inspeccionar también el **cuerpo** de esa misma respuesta antes de asumir que no contiene nada relevante — en aplicaciones con este patrón de fallo, el contenido que se supone protegido puede estar presente ahí mismo, aunque el navegador nunca lo muestre por seguir automáticamente la redirección.

## Conectando con el siguiente apartado

El acceso directo es la variante más simple de bypass de autenticación. El siguiente apartado cubre un escenario relacionado pero distinto: cuando la autenticación **sí** se comprueba correctamente, pero un parámetro adicional de la petición —pensado originalmente con otro propósito— puede manipularse para alterar el resultado de esa comprobación.
