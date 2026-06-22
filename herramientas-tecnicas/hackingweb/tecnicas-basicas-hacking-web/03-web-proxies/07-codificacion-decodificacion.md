# Codificación y decodificación

## Por qué es imprescindible dominar esto

Al modificar y reenviar peticiones manualmente, es habitual introducir caracteres especiales en los payloads (comillas, espacios, símbolos de control de shell, `&`, `#`) que tienen un significado reservado dentro de la sintaxis HTTP/URL. Si no se codifican correctamente, pueden romper la estructura de la petición —generando un error del servidor que no tiene nada que ver con la vulnerabilidad que se está probando— o ser interpretados de forma distinta a la pretendida.

## Codificación URL: lo mínimo imprescindible

| Carácter | Por qué hay que codificarlo |
|---|---|
| espacio | Puede interpretarse como el final de los datos de la petición |
| `&` | Se interpreta como separador de parámetros |
| `#` | Se interpreta como identificador de fragmento |

### En Burp

Seleccionar el texto en Repeater → clic derecho → `Convert Selection > URL > URL-encode key characters`, o usar el atajo `Ctrl+U`. También se puede activar la codificación automática mientras se escribe (clic derecho → habilitar esa opción), de forma que cualquier texto introducido se codifique sobre la marcha.

### En ZAP

ZAP codifica automáticamente los datos de la petición en segundo plano antes de enviarla, sin que normalmente sea necesario hacerlo de forma manual y explícita.

Existen variantes adicionales como **Full URL-Encoding** (codifica absolutamente todos los caracteres, no solo los reservados) o codificación **Unicode**, útiles en escenarios de evasión de filtros donde una codificación parcial no es suficiente para saltarse una validación.

## Decodificación de datos recibidos

Es muy habitual que una aplicación codifique datos antes de mostrarlos o almacenarlos (cookies en Base64, parámetros con múltiples capas de codificación, hashes). Saber decodificar rápidamente esos valores es esencial para entender qué información viaja realmente.

### Herramientas dedicadas

- **Burp**: pestaña **Decoder**, o el más reciente **Burp Inspector** (integrado en Proxy/Repeater), que detecta y ofrece decodificar automáticamente valores reconocidos.
- **ZAP**: herramienta **Encoder/Decoder/Hash** (`Ctrl+E`), con pestaña de decodificación automática que prueba varios decodificadores a la vez.

Tipos de codificación habituales soportados por ambas herramientas: HTML entities, Unicode, Base64, ASCII hex, además de URL-encoding.

### Ejemplo práctico

Una cookie con el valor `eyJ1c2VybmFtZSI6Imd1ZXN0IiwgImlzX2FkbWluIjpmYWxzZX0=` tiene toda la apariencia de estar codificada en Base64 (el patrón de caracteres y el `=` final de relleno son pistas características). Decodificándola se obtiene:

```json
{"username":"guest", "is_admin":false}
```

Esto revela inmediatamente un vector de prueba evidente: si la aplicación confía en este valor sin validarlo también en el servidor, modificar `"is_admin":false` a `"is_admin":true`, volver a codificar en Base64, y sustituir la cookie en la petición podría escalar privilegios — un ejemplo claro de por qué nunca se debe confiar en datos que el cliente puede leer y modificar libremente (lo que conecta directamente con los principios vistos en el bloque de *Broken Authentication*).

```
Original:  {"username":"guest", "is_admin":false}
Modificado: {"username":"guest", "is_admin":true}
Recodificado en Base64: eyJ1c2VybmFtZSI6Imd1ZXN0IiwgImlzX2FkbWluIjp0cnVlfQ==
```

## Codificación encadenada (múltiples capas)

No es raro encontrar datos codificados varias veces de forma sucesiva (por ejemplo, Base64 sobre Base64 sobre URL-encoding). La estrategia es siempre la misma: identificar el patrón de la capa más externa, decodificar, y repetir el proceso sobre el resultado hasta llegar a texto plano legible. Tanto el Decoder de Burp como el Encoder/Decoder/Hash de ZAP permiten encadenar estas operaciones cómodamente, reutilizando la salida de un paso como entrada del siguiente, sin tener que copiar y pegar manualmente entre herramientas externas.

Reconocer patrones visuales ayuda a identificar rápidamente el tipo de codificación en cada capa:

| Patrón observado | Probable codificación |
|---|---|
| Solo caracteres `A-Za-z0-9+/=`, longitud múltiplo de 4 | Base64 |
| Secuencias `%XX` (dos dígitos hexadecimales) | URL-encoding |
| Solo caracteres `0-9a-fA-F` | Hexadecimal |
| Secuencias `&#xXX;` o `&entity;` | HTML entities |
