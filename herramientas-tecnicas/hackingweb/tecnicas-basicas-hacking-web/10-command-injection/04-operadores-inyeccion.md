# Otros operadores de inyección

## Por qué importa entender el comportamiento exacto de cada operador

No todos los operadores de la tabla del apartado anterior se comportan igual ante un fallo del primer comando. Entender esta diferencia es lo que permite elegir el operador correcto según el contexto — por ejemplo, cuando el comando original podría fallar (o cuando interesa que falle deliberadamente) para forzar la ejecución del segundo.

## El operador AND (`&&`)

Ejecuta el segundo comando **solo si** el primero finaliza con éxito (código de salida `0`):

```bash
ping -c 1 127.0.0.1 && whoami
```

Si la IP es válida y el `ping` se completa correctamente, `whoami` se ejecuta a continuación, y ambas salidas aparecen en la respuesta.

## El operador OR (`||`)

El comportamiento opuesto: el segundo comando solo se ejecuta si el **primero falla** (código de salida distinto de `0`).

```bash
ping -c 1 127.0.0.1 || whoami
```

Con una IP válida, el `ping` tiene éxito y `whoami` **nunca llega a ejecutarse** — el operador `||` corta la cadena en cuanto el primer comando ya devolvió éxito.

### Forzando el fallo del comando original

Una técnica útil cuando se trabaja con `||`: en lugar de proporcionar una entrada válida, se puede dejar el campo vacío o usar un valor que garantice el fallo del comando original, de forma que el operador `||` sí dispare la ejecución del comando inyectado:

```bash
ping -c 1 || whoami
```

```
ping: usage error: Destination address required
21y4d
```

El `ping` falla por falta de argumento, y el shell pasa automáticamente a evaluar el segundo comando — confirmando que la ejecución condicional funciona exactamente como se espera.

## Por qué esto es relevante en la práctica

Elegir el operador adecuado depende del contexto de la inyección:

- **`;`** es el más universal y directo cuando no importa si el comando original tiene éxito o no — ambos se ejecutan siempre, de forma secuencial.
- **`&&`** es útil cuando se quiere preservar la apariencia de "funcionamiento normal" del comando original (por ejemplo, para no levantar sospechas si la aplicación muestra algún tipo de alerta visible ante errores).
- **`||`** es la opción cuando el comando original **no puede** completarse con éxito de forma natural, o cuando se prefiere forzar deliberadamente su fallo para concentrar la atención exclusivamente en la salida del comando inyectado.

## Recordando el resto de operadores de la tabla

Además de `;`, `&&` y `||`, conviene tener presentes también `&` (ejecuta ambos en segundo plano), `|` (encadena la salida del primero como entrada del segundo, mostrando solo la salida final) y las construcciones de subshell (`` `comando` `` y `$(comando)`), exclusivas de sistemas tipo Unix, que permiten anidar la ejecución de un comando dentro de otro.

## Verificando siempre el comportamiento localmente antes de aplicar la técnica

Una buena práctica recurrente en este tipo de pruebas: reproducir primero el comando combinado en un entorno propio y controlado (una terminal local, un laboratorio) para confirmar exactamente qué salida produce **antes** de enviarlo contra el objetivo — esto evita confusiones sobre si una respuesta inesperada se debe al comportamiento real de la aplicación o a un malentendido sobre cómo opera el operador elegido en esa shell concreta.
