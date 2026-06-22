# Detección de la vulnerabilidad

## El principio: detección y explotación van de la mano

Para vulnerabilidades básicas de inyección de comandos, el proceso de detección **es** el de explotación: se intenta inyectar un comando, y si la salida cambia respecto al resultado esperado, queda confirmado. En casos más avanzados (cuando hay filtros o validación parcial) hace falta un proceso más gradual de fuzzing y revisión, que se trata en los apartados posteriores de este bloque.

## Reconociendo el patrón en una funcionalidad

Imaginemos una utilidad de "comprobador de host" que pide una IP y, aparentemente, ejecuta un `ping` contra ella. Probando con `127.0.0.1`, la salida muestra un único paquete enviado — un patrón reconocible que sugiere un comando interno del tipo:

```bash
ping -c 1 ENTRADA_USUARIO
```

Sin acceso al código fuente, esta inferencia se hace observando cómo varía la salida según la entrada — exactamente el mismo principio de "observar el comportamiento para inferir la lógica interna" aplicado repetidamente a lo largo de este temario (en XSS al identificar el sink, en SQLi al inferir la estructura de la consulta).

## Los operadores de inyección: la tabla de referencia

| Operador | Carácter | Codificado en URL | Qué se ejecuta |
|---|---|---|---|
| Punto y coma | `;` | `%3b` | Ambos comandos, secuencialmente |
| Salto de línea | `\n` | `%0a` | Ambos comandos |
| Background | `&` | `%26` | Ambos (normalmente se muestra antes la salida del segundo) |
| Pipe | `\|` | `%7c` | Ambos, pero solo se muestra la salida del segundo |
| AND | `&&` | `%26%26` | Ambos, solo si el primero tiene éxito |
| OR | `\|\|` | `%7c%7c` | Solo el segundo, y solo si el primero falla |
| Subshell (backticks) | `` `` `` | `%60%60` | Ambos (solo Linux) |
| Subshell `$()` | `$()` | `%24%28%29` | Ambos (solo Linux) |

Estos operadores funcionan de forma prácticamente universal, **independientemente del lenguaje o framework** de la aplicación web — lo que importa es el sistema operativo y la shell que interpreta el comando final, no la tecnología que lo construyó.

> **Excepción relevante**: el punto y coma (`;`) no funciona como separador de comandos en `cmd.exe` de Windows, aunque sí en PowerShell — un matiz a tener en cuenta al adaptar la técnica según el sistema operativo del objetivo.

## El flujo de detección

1. Identificar una funcionalidad cuya salida sugiere la ejecución de un comando del sistema (resultado de `ping`, de `nslookup`, de procesamiento de archivos, etc.).
2. Probar añadir uno de los operadores de la tabla anterior tras la entrada esperada.
3. Observar si la respuesta cambia de forma reconocible — la aparición de salida adicional, no relacionada con el comando original, confirma la inyección.

Este proceso se desarrolla en detalle, paso a paso, en el siguiente apartado.
