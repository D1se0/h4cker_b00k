# Hydra contra autenticación HTTP básica

## Repaso: cómo funciona la autenticación básica

Como se vio en detalle en el bloque de *Web Requests*, la autenticación HTTP básica es un protocolo de desafío-respuesta gestionado directamente por el servidor web: ante un recurso protegido, el servidor responde `401 Unauthorized` junto con una cabecera `WWW-Authenticate: Basic`, y el cliente debe reenviar la petición incluyendo una cabecera `Authorization: Basic <credenciales_en_base64>`.

```
GET /recurso_protegido HTTP/1.1
Host: www.ejemplo.com
Authorization: Basic YWxpY2U6c2VjcmV0MTIz
```

Como ya se explicó entonces, Base64 **no es cifrado** — es una codificación trivialmente reversible. Esto significa que, si se conoce o se intercepta el par usuario/contraseña, decodificarlo es inmediato. Pero también significa algo relevante para este bloque: dado que el formato de la cabecera es fijo y predecible, automatizar la prueba sistemática de credenciales contra este mecanismo es directo.

## Por qué Basic Auth es un objetivo habitual de fuerza bruta

A diferencia de un formulario de login personalizado (con su propia lógica de validación, posibles tokens CSRF, mensajes de error variables), la autenticación básica sigue siempre el mismo protocolo estandarizado — lo que la hace especialmente sencilla de atacar con una herramienta genérica como Hydra, sin necesidad de adaptar la lógica de ataque a particularidades de cada aplicación.

## El módulo `http-get` de Hydra

```bash
hydra -l basic-auth-user -P 2023-200_most_used_passwords.txt 10.10.10.5 http-get / -s 81
```

Desglosando el comando:

| Parte | Función |
|---|---|
| `-l basic-auth-user` | Nombre de usuario conocido (si se desconoce, se usaría `-L` con una lista de usuarios candidatos) |
| `-P 2023-200_most_used_passwords.txt` | Wordlist de contraseñas a probar |
| `10.10.10.5` | IP del objetivo |
| `http-get /` | Protocolo y ruta sobre la que se realiza cada intento |
| `-s 81` | Puerto no estándar del servicio |

Hydra construye automáticamente, para cada contraseña candidata, la cabecera `Authorization: Basic` codificada correctamente y envía la petición, interpretando el código de respuesta (`401` vs. `200`) para determinar si la combinación es válida.

```
[81][http-get] host: 10.10.10.5   login: basic-auth-user   password: ...
1 of 1 target successfully completed, 1 valid password found
```

## Por qué conocer el usuario de antemano simplifica el ataque

Cuando el nombre de usuario ya es conocido (visible en mensajes de la aplicación, documentación, o simplemente un valor común como `admin`), el ataque se reduce a probar **solo la dimensión de la contraseña** — exactamente la mitad del espacio de combinaciones que tendría que probarse si también hubiera que adivinar el usuario. Esto conecta directamente con lo discutido en el apartado de fundamentos de este bloque sobre por qué conocer (o mantener) un nombre de usuario por defecto reduce tan significativamente la dificultad de un ataque de fuerza bruta.

## Eligiendo bien la wordlist

Para Basic Auth, una wordlist de contraseñas comunes de propósito general (como la usada en el ejemplo, con las 200 contraseñas más usadas según datos de 2023) suele ser un buen punto de partida: este mecanismo de autenticación se usa habitualmente para proteger recursos administrativos sencillos o paneles internos, donde es razonablemente común encontrar credenciales débiles o poco cuidadas, en contraste con sistemas de autenticación principales de la aplicación que suelen recibir más atención de seguridad.

## El siguiente paso: formularios de login personalizados

Basic Auth es el caso más sencillo porque sigue un protocolo estandarizado. La mayoría de aplicaciones web modernas, sin embargo, implementan su **propio** formulario de login con lógica personalizada — el escenario que se desarrolla en el siguiente apartado, donde Hydra necesita información adicional sobre la estructura exacta de la petición y cómo distinguir un intento fallido de uno exitoso.
