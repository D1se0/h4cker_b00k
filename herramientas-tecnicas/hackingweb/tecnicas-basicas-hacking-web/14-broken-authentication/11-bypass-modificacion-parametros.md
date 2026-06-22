# Bypass de autenticación por modificación de parámetros

## Cuando la autenticación depende de un parámetro que el cliente controla

Una implementación de autenticación puede fallar de forma distinta al caso visto en el apartado anterior: en lugar de "olvidar" detener la ejecución tras una redirección, el fallo aquí está en que la aplicación basa una decisión de identidad o de nivel de acceso en un **parámetro HTTP** que viaja en la propia petición, sin verificar de forma independiente —contra el estado real de la sesión en el servidor— si ese valor corresponde realmente al usuario autenticado.

Este patrón está estrechamente relacionado con las vulnerabilidades de tipo **IDOR (Insecure Direct Object Reference)**, que se tratan en detalle en el bloque de *Web Attacks*: la diferencia de matiz es que aquí el parámetro afecta directamente al **nivel de autenticación o privilegio** concedido, no solo al acceso a un recurso de datos concreto.

## El patrón de fallo, conceptualmente

Imaginemos que, tras un login exitoso, la aplicación redirige a una URL que incluye un identificador del usuario:

```
/panel.php?user_id=183
```

Si el servidor usa ese valor directamente para decidir **qué datos o qué nivel de privilegio mostrar**, en lugar de derivarlo exclusivamente del estado de sesión ya autenticado en el servidor (la cookie de sesión, validada server-side), el parámetro se convierte en una superficie de manipulación: cualquier usuario autenticado, sea cual sea su rol real, podría intentar alterar ese valor para que el servidor le trate como si fuera otro usuario distinto — potencialmente uno con privilegios más altos.

La señal que delata este patrón durante una auditoría: si **eliminar** el parámetro provoca que la aplicación pierda el contexto de quién es el usuario (por ejemplo, redirigiendo de vuelta al login) pero **sin invalidar la sesión actual**, eso confirma que el parámetro está cumpliendo un papel activo en la lógica de autenticación/autorización — y, por tanto, es candidato a manipulación.

## Por qué esto es un fallo de autorización, no solo de autenticación

Técnicamente, el usuario ya superó el login (tiene una sesión válida) — el problema es que el servidor confía en un valor adicional, controlable por el cliente, para decidir **con qué identidad o privilegio** procesar el resto de la petición. Es exactamente el mismo principio de fondo trabajado en el apartado anterior de protección contra fuerza bruta (no confiar en valores que el cliente puede establecer libremente para decisiones de seguridad), aplicado aquí no a la identificación del origen de una petición, sino a la identidad del propio usuario autenticado.

## Mitigación

- **Derivar siempre la identidad del usuario del estado de sesión server-side**, nunca de un parámetro de la URL o del cuerpo de la petición que el cliente pueda modificar libremente.
- **Verificar explícitamente la autorización en cada petición**, comprobando en el servidor que el usuario autenticado tiene realmente permiso sobre el recurso o nivel de privilegio que está solicitando — no asumir que un parámetro recibido es automáticamente legítimo solo porque la sesión en sí es válida.
- **Usar identificadores no predecibles** cuando, por diseño, sea necesario referenciar un recurso mediante un parámetro (por ejemplo, un identificador aleatorio largo en lugar de un número secuencial), reduciendo —aunque sin sustituir nunca a la verificación de autorización real— la facilidad de adivinar o enumerar valores válidos de otros usuarios.

## Por qué este apartado cierra la sección de bypass de autenticación de este bloque

Acceso directo (apartado anterior) y manipulación de parámetros comparten la misma lección de fondo, aplicada a dos mecanismos de fallo distintos: una comprobación de autenticación que existe en el código, pero que **no se aplica de forma estructuralmente completa** en todos los puntos donde debería. Existen variantes más avanzadas de bypass de autenticación —explotando fallos de tipado, vulnerabilidades de inyección que alteran la lógica de validación, o errores lógicos más sutiles en el manejo de parámetros— que se tratan con mayor profundidad en materiales especializados de pentesting de caja blanca y de inyección, ya cubiertos parcialmente en los bloques de *SQL Injection Fundamentals* y *Command Injection* de este mismo temario.

## Hacia dónde sigue este bloque

Con la autenticación inicial cubierta —desde fuerza bruta hasta bypass directo—, el bloque se desplaza hacia el siguiente eslabón de la cadena: una vez que un usuario **está** autenticado, ¿qué mantiene esa autenticación activa, y qué puede salir mal en ese mecanismo? El resto de este bloque trata los **tokens de sesión** que sostienen el estado autenticado tras el login inicial.
