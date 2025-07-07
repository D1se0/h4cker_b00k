---
icon: file-shield
---

# Descriptores de seguridad y ACLs

Con las `ACLs` podremos ver como escalar privilegios, las rutas que podamos encontrar vulnerables, etc...

Para ver donde estan las `ACLs` y como verlas nos tendremos que ir a nuestro `DC` -> `Administrador del servidor` -> `Usuarios y equipos de Active Directory` -> `Usuarios` -> por ejemplo elijamos un usuario, en este caso `emplado1` click derecho en el -> `Propiedades` -> `Seguridad` -> `Opciones avanzadas`.

En esta parte veremos varias cosas importantes entre ellas los `Permisos` o tambien llamadas `DACLs` que van a ser las que mas nos van a interesar, despues estaria `Auditoria` o tambien llamada `SACLs`.

Esto es muy importante ya que aplica a todo el sistema operativo `Windows`, en el siguiente enlace se detalla lo que es un `Security Descriptor` ya que es muy importante entenderlo.

URL = [Security Descriptor Windows Microsoft](https://learn.microsoft.com/en-us/windows/win32/secauthz/security-descriptors)

Practicamente casi todos los objetos en `Windows` tienen un descriptor de seguridad asociado.

> Explicación detallada de Descriptores de seguridad:

Un `descriptor de seguridad` contiene la información de seguridad asociada con un objeto asegurable. Un `descriptor de seguridad` consta de una estructura `SECURITY_DESCRIPTOR` y su información de seguridad asociada. Un `descriptor de seguridad` puede incluir la siguiente información de seguridad:

* `Identificadores de seguridad (SID)` para el propietario y el grupo principal de un objeto.
* `Una DACL` que especifica los derechos de acceso permitidos o denegados a `usuarios o grupos` particulares.
* `Una SACL` que especifica los tipos de intentos de acceso que generan registros de `auditoría` para el objeto.
* Un conjunto de `bits` de control que califican el significado de un descriptor de seguridad o de sus miembros individuales.

Las aplicaciones no deben manipular directamente el contenido de un descriptor de seguridad. La `API` de `Windows` proporciona funciones para configurar y recuperar la información de seguridad en el descriptor de seguridad de un objeto. Además, existen funciones para crear e inicializar un descriptor de seguridad para un nuevo objeto.

Las aplicaciones que trabajan con descriptores de seguridad en objetos de `Active Directory` pueden utilizar las funciones de seguridad de `Windows` o las interfaces de seguridad proporcionadas por las interfaces de servicio de Active `Directory (ADSI)`. Para obtener más información sobre las interfaces de seguridad ADSI, consulte Cómo funciona el control de acceso en `Active Directory`.

Si nosotros por ejemplo nos vamos a un script que tengamos en la maquina del `DC` en el escritorio y le damos click derecho al archivo -> `Propiedades` -> `Seguridad` -> `Opciones avanzadas`.

Vamos a ver lo mismo que vemos en el panel del `administrador` con el usuario `empleado1` ya que tambien se maneja por `ACLs` todo esto y veremos el `propietario` del archivo por lo que veremos que permisos tiene, etc...

<figure><img src="../../../.gitbook/assets/image (252).png" alt=""><figcaption></figcaption></figure>

Por lo que todos los objetos en `Windows` van a tener un `Security Descriptor` y con esto podremos manejar los permisos de cada objeto, por lo que si hay alguna mala configuracion en estas dos cosas tan importantes podriamos como atacantes escalar privilegios enseguida.

Por que por ejemplo si nosotros llegaramos a poder modifcar las `ACLs` podremos insertar un objeto en el que `empleado1` pueda resetear la contraseña del `administrador` y con eso cambiariamos la contraseña, por lo que podremos ser `administradores`.

Esto seria un ejemplo del proceso de `DACLs` y `ACEs`:

<figure><img src="../../../.gitbook/assets/image (253).png" alt=""><figcaption></figcaption></figure>

Aqui vemos que el intento del usuario `Andrew` es invalido ya que cuando intenta conectar con el `Object` este mismo revisa en el listado de `DACL` y ve que tiene el permiso denegado, pero cuando lo intenta `Jane` pertenece al `Group A` y este en el listado del `DACL` tiene el acceso permitido, por lo que la deja.
