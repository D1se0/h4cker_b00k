# Medusa contra servicios web

## El módulo `http` y la variante `web-form`

Igual que Hydra ofrece módulos dedicados para autenticación HTTP básica y formularios personalizados (vistos en los apartados anteriores de este bloque), Medusa ofrece su propio módulo `http`, con soporte tanto para `GET` (típicamente Basic Auth) como para `POST` (formularios de login personalizados).

### Contra autenticación HTTP básica

```bash
medusa -h 10.10.10.5 -u admin -P contraseñas.txt -M http -m GET
```

Conceptualmente idéntico al flujo visto con Hydra en el apartado de autenticación básica: Medusa construye automáticamente la cabecera `Authorization: Basic` codificada para cada contraseña candidata, interpretando el código de respuesta para determinar éxito o fracaso.

### Contra un formulario de login personalizado

```bash
medusa -h www.ejemplo.com -U usuarios.txt -P contraseñas.txt -M http \
  -m DIR:/login.php \
  -m FORM:"username=^USER^&password=^PASS^:F=Invalid"
```

La estructura es equivalente a la vista con `http-post-form` en Hydra: se especifica la ruta del endpoint (`DIR:`), el cuerpo de la petición con los marcadores `^USER^`/`^PASS^`, y la condición que distingue un intento fallido (`F=`) de uno exitoso.

## El mismo proceso de reconocimiento previo, independientemente de la herramienta

Antes de construir el comando, sigue siendo imprescindible el mismo trabajo de inspección manual trabajado en el apartado de Hydra contra formularios: identificar la ruta exacta del endpoint, los nombres reales de los parámetros del formulario, y observar manualmente qué distingue una respuesta de fallo de una de éxito — capturando la petición real con las DevTools del navegador o un proxy de intercepción (bloque de *Web Proxies*), en lugar de asumir nombres de parámetros genéricos.

## Eligiendo entre Hydra y Medusa para un ataque concreto contra una aplicación web

Para el caso de uso de este temario —pentesting de aplicaciones web—, ambas herramientas cubren exactamente el mismo terreno: autenticación HTTP básica y formularios de login personalizados. La elección entre una u otra suele reducirse a preferencia personal o a qué sintaxis resulte más cómoda de ajustar para el caso concreto que se está auditando. Lo importante, una vez más, no es la herramienta en sí, sino el trabajo previo de reconocimiento: identificar correctamente el endpoint, los parámetros, la condición de éxito/fracaso, y elegir una wordlist orientada al contexto (genérica, filtrada por política conocida, o construida a partir de información específica del objetivo, como se desarrolla en el siguiente y último apartado de este bloque).

## Limitaciones a tener en cuenta al atacar formularios web reales

Más allá de la sintaxis correcta, conviene recordar limitaciones prácticas que pueden afectar al éxito de un ataque de fuerza bruta contra un formulario de login real:

- **Tokens CSRF dinámicos**: si el formulario incluye un token único por petición (visto en el bloque de *Introducción a Aplicaciones Web*), cada intento de Hydra/Medusa con un valor de token reutilizado o ausente puede rechazarse antes siquiera de validar la contraseña — el mismo problema, y la misma solución, vistos al hablar de tokens anti-CSRF en el bloque de *SQLMap Essentials*.
- **Límites de tasa o bloqueo de cuentas**: una aplicación bien protegida puede bloquear temporalmente una cuenta tras varios intentos fallidos consecutivos, lo que limita drásticamente la viabilidad de un ataque de fuerza bruta tradicional contra una única cuenta — la razón de fondo detrás del *password spraying* visto en el apartado de tipos de ataque de este bloque.
- **CAPTCHA**: presente en muchos formularios modernos precisamente para frustrar la automatización — un obstáculo que ni Hydra ni Medusa resuelven por sí solas.

Documentar la ausencia (o presencia insuficiente) de estas protecciones es, en sí mismo, uno de los hallazgos más valiosos al auditar un mecanismo de autenticación — el tema que se retoma con mucha más profundidad en el bloque de *Broken Authentication*.
