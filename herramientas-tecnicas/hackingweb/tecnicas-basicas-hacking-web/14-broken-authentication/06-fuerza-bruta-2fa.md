# Fuerza bruta de códigos 2FA

## Por qué 2FA puede seguir siendo vulnerable

Como se vio en el apartado de fundamentos de este bloque, 2FA combina dos factores distintos para reducir drásticamente el riesgo de que un atacante acceda con solo la contraseña comprometida. Pero esa protección depende enteramente de que el **segundo factor** esté bien implementado. Una de las formas más comunes de 2FA en aplicaciones web es un código numérico de un solo uso (TOTP) enviado por SMS o generado por una aplicación de autenticación — y, exactamente como ocurría con los tokens de restablecimiento de contraseña del apartado anterior, si ese código tiene muy pocos dígitos y no existe ningún límite de intentos, hereda la misma debilidad estructural: un espacio de búsqueda demasiado pequeño para resistir fuerza bruta.

## La señal de alarma

Un código 2FA de 4 dígitos tiene exactamente las mismas 10.000 combinaciones posibles que un token de restablecimiento corto — trivialmente agotable mediante fuerza bruta si no hay ninguna protección adicional en el endpoint que lo verifica.

## El patrón de ataque, a alto nivel

El flujo general es: tras superar el primer factor (contraseña), la aplicación pasa a un segundo paso donde solicita el código 2FA, normalmente asociado a la sesión ya parcialmente autenticada mediante una cookie. Si ese endpoint de verificación no limita el número de intentos fallidos, se puede automatizar la prueba sistemática de **todo el espacio de valores posibles** del código, exactamente con la misma técnica de fuzzing dirigido por mensaje de error vista en el apartado anterior sobre tokens de restablecimiento — generando la lista completa de candidatos numéricos y filtrando las respuestas según el mensaje de "código inválido" que el servidor devuelve.

## Por qué el espacio de búsqueda es, de nuevo, el factor decisivo

Esta es la misma matemática que ha aparecido repetidamente en este bloque y en el de *Login Brute Forcing*: la seguridad real de un código de un solo uso depende casi por completo de su longitud y de la protección activa contra intentos repetidos — no del mecanismo de entrega (SMS vs. app de autenticación), que no aporta ninguna resistencia adicional frente a fuerza bruta si el código en sí es corto y el endpoint no limita los intentos.

## Mitigación

- **Códigos suficientemente largos**: 6 dígitos (un millón de combinaciones) es el estándar habitual en implementaciones TOTP serias, frente a 4 dígitos (solo diez mil) — una diferencia de cien veces en el espacio de búsqueda.
- **Límite estricto de intentos** sobre el endpoint de verificación del segundo factor — bloqueando la sesión, invalidando el código, o exigiendo reautenticación completa tras un número reducido de intentos fallidos (por ejemplo, 3-5).
- **Expiración corta del código**, normalmente entre 30 segundos y unos pocos minutos — reduciendo drásticamente la ventana de tiempo disponible para completar cualquier ataque automatizado.
- **Vincular el segundo factor de forma robusta a la sesión** y a la identidad ya autenticada en el primer paso, evitando que un código válido para una sesión pueda reutilizarse o probarse de forma desacoplada.

## Por qué esto no invalida el valor de 2FA en general

Que una implementación concreta de 2FA pueda fallar por un código demasiado corto no significa que 2FA, como concepto, sea débil — significa que, como cualquier control de seguridad trabajado en este temario, su efectividad real depende enteramente de los detalles de implementación. Un 2FA bien implementado (código largo, límite de intentos estricto, expiración corta) sigue siendo una de las medidas individuales más efectivas para proteger una cuenta, incluso frente a una contraseña ya comprometida — la clave es auditar la implementación concreta, no asumir que "tener 2FA" es automáticamente sinónimo de "estar protegido".

## Conectando con el siguiente apartado

Tanto los tokens de restablecimiento como los códigos 2FA comparten la misma defensa estructural pendiente de desarrollar: **limitar el número de intentos permitidos**. El siguiente apartado trata específicamente este tema desde una perspectiva más amplia — qué hace que una protección contra fuerza bruta sea robusta o, por el contrario, fácilmente evadible.
