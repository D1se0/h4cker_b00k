# Diagnóstico de problemas en SQLMap

## Por qué dedicarle un apartado entero al diagnóstico

En la práctica, una proporción significativa del tiempo trabajando con SQLMap se invierte en entender **por qué** algo no funciona como se esperaba, más que en lanzar el ataque inicial. Estas son las herramientas de diagnóstico fundamentales para ese trabajo de depuración.

## Mostrar errores del DBMS automáticamente

```bash
sqlmap -u "http://objetivo.htb/vuln.php?id=1" --parse-errors
```

```
[WARNING] parsed DBMS error message: 'SQLSTATE[42000]: Syntax error...'
```

Si la aplicación filtra mensajes de error de la base de datos en su respuesta (algo común cuando la gestión de errores no está bien implementada en producción), `--parse-errors` los extrae y muestra automáticamente — información directamente útil para entender la sintaxis exacta de la consulta original y, en consecuencia, ajustar prefijos/sufijos personalizados si hiciera falta.

## Guardando todo el tráfico generado

```bash
sqlmap -u "http://objetivo.htb/vuln.php?id=1" --batch -t /tmp/traffic.txt
```

`-t` vuelca a un archivo cada petición enviada y cada respuesta recibida durante la ejecución completa. Esto permite una inspección manual exhaustiva después del hecho: comparar exactamente qué se envió en cada intento frente a lo que se recibió, sin tener que confiar únicamente en el resumen que SQLMap imprime por consola.

## Aumentando el nivel de detalle (verbosidad)

```bash
sqlmap -u "http://objetivo.htb/vuln.php?id=1" -v 6 --batch
```

| Nivel | Qué añade |
|---|---|
| 1 (defecto) | Información básica de progreso |
| 3 | Incluye los payloads (`[PAYLOAD]`) probados en cada test |
| 5-6 | Tráfico HTTP completo en bruto (`[TRAFFIC OUT]`/`[TRAFFIC IN]`), mensajes de depuración internos |

Niveles altos de verbosidad son extremadamente útiles para entender exactamente qué payload concreto se está enviando en un momento dado, sin necesidad de recurrir a un proxy externo para interceptarlo.

## Combinando ambas técnicas para un diagnóstico completo

El flujo de diagnóstico más efectivo combina ambas herramientas: `-v 5` o superior para ver en tiempo real qué se está probando, junto con `-t archivo.txt` para tener un registro persistente que revisar con calma después, especialmente útil cuando el volumen de peticiones es alto y resulta poco práctico seguir todo en pantalla durante la ejecución.

## Errores comunes que este nivel de diagnóstico suele revelar

- **Cookie de sesión caducada o ausente**: la aplicación redirige silenciosamente a una página de login, y SQLMap está probando inyecciones contra el formulario de login en lugar del endpoint real — visible inmediatamente al revisar el tráfico capturado.
- **Formato de cuerpo incorrecto**: enviar datos como `application/x-www-form-urlencoded` cuando la aplicación espera JSON (o viceversa) — la aplicación rechaza la petición antes incluso de procesar el parámetro, algo que un mensaje de error parseado revela de inmediato.
- **Protección anti-automatización**: tokens CSRF no actualizados correctamente entre peticiones sucesivas (tratado en detalle en el apartado de *bypass de protecciones* de este mismo bloque), visible como un patrón de respuestas de error consistentes pese a que el payload en sí parece correcto.

## La filosofía de diagnóstico

Antes de concluir "el objetivo no es vulnerable", la disciplina correcta es siempre: **verificar primero que la herramienta está configurada exactamente como se espera**, comparando tráfico capturado frente a una petición legítima conocida. Este principio —común a cualquier herramienta de automatización en pentesting, no solo SQLMap— evita la frustración (y los falsos negativos) de descartar prematuramente un objetivo genuinamente vulnerable por un simple error de configuración.
