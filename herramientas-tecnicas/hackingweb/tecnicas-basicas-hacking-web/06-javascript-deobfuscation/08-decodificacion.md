# Decodificación: Base64, Hex y ROT13

## Por qué la codificación de texto acompaña tan a menudo a la ofuscación

Igual que el código se ofusca para dificultar la lectura, el **contenido** que ese código maneja (cadenas, payloads, respuestas del servidor) también suele codificarse, por las mismas razones: dificultar el análisis humano y evadir sistemas de detección automatizados basados en patrones de texto plano. Es habitual encontrar ambas capas combinadas: código ofuscado que, al desofuscarse, revela cadenas codificadas que requieren un paso de decodificación adicional.

## Base64

### Reconociéndolo

- Solo usa caracteres alfanuméricos más `+` y `/`.
- Su longitud es siempre **múltiplo de 4** — si el resultado natural no lo es, se rellena con uno o más caracteres `=` al final.
- Es, con diferencia, la codificación más común en este contexto.

### Codificar y decodificar en Linux

```bash
echo "texto" | base64
# dGV4dG8K

echo "dGV4dG8K" | base64 -d
# texto
```

## Hexadecimal

### Reconociéndolo

Solo contiene los 16 caracteres `0-9` y `a-f` — cada par de dígitos hexadecimales representa un byte (carácter) según su valor en la tabla ASCII.

### Codificar y decodificar en Linux

```bash
echo "texto" | xxd -p
# 7465787 40a

echo "74657874" | xxd -p -r
# text
```

## ROT13 / Cifrado César

### Reconociéndolo

Cada letra se desplaza un número fijo de posiciones en el alfabeto — ROT13 desplaza siempre 13 posiciones, lo que tiene la propiedad curiosa de que aplicarlo dos veces devuelve el texto original. Aunque el resultado parece aleatorio a primera vista, **conserva patrones reconocibles**: por ejemplo, `http://www` se convierte en `uggc://jjj` — la estructura sigue siendo perceptible para un ojo entrenado.

### Codificar y decodificar en Linux

```bash
echo "texto" | tr 'A-Za-z' 'N-ZA-Mn-za-m'
# grkgb
```

Como ROT13 es simétrico (aplicarlo dos veces revierte el cambio), el mismo comando sirve tanto para codificar como para decodificar.

## Identificación automática

Cuando no está claro a simple vista qué codificación se está usando, herramientas como [Cipher Identifier](https://www.boxentriq.com/code-breaking/cipher-identifier) analizan la cadena y sugieren el tipo más probable — un buen punto de partida antes de probar manualmente cada técnica conocida.

## Codificación vs. cifrado: una distinción importante

Todo lo visto en este apartado es **codificación**, no **cifrado**: son transformaciones completamente reversibles sin necesidad de ninguna clave secreta — cualquiera que reconozca el esquema puede revertirlas. El **cifrado**, en cambio, requiere una clave para revertir la transformación; si esa clave no está presente en el propio script (algo que ocurre, mejor diseñado, en malware más sofisticado), la ingeniería inversa se vuelve sustancialmente más compleja, y puede requerir analizar el comportamiento en tiempo de ejecución en lugar de solo el código estático.

## Resolviendo el ejemplo completo del bloque

Retomando la respuesta obtenida en el apartado anterior:

```
N2gxNV8xNV9hX3MzY3IzN19tMzU1NGcz
```

El patrón (alfanumérico, longitud múltiplo de 4) sugiere Base64:

```bash
echo "N2gxNV8xNV9hX3MzY3IzN19tMzU1NGcz" | base64 -d
# 7h15_15_a_s3cr37_m3554g3
```

El resultado (`7h15_15_a_s3cr37_m3554g3`, leetspeak para "this is a secret message") confirma que efectivamente se trataba de Base64 de una sola capa. Con este valor decodificado, el siguiente paso natural —cerrando el círculo completo de este bloque— es reenviarlo de vuelta al mismo endpoint descubierto anteriormente (`/serial.php`), esta vez como parámetro, para comprobar si el servidor procesa ese valor de alguna forma adicional:

```bash
curl -X POST http://10.10.10.5/serial.php -d "serial=7h15_15_a_s3cr37_m3554g3"
```

## El ciclo completo de este bloque, de principio a fin

1. Localizar JavaScript en el código fuente de una página.
2. Reconocer que está ofuscado (packing, codificación de cadenas, o técnicas más avanzadas).
3. Desofuscarlo con herramientas dedicadas (UnPacker u equivalentes).
4. Analizar manualmente el código resultante para entender su función.
5. Replicar directamente con `curl` cualquier petición HTTP descubierta en el script.
6. Identificar y revertir cualquier codificación de texto en la respuesta obtenida (Base64, Hex, ROT13).
7. Usar el resultado decodificado para continuar interactuando con la aplicación, cerrando el ciclo de descubrimiento.

Este flujo de trabajo —observar, desofuscar, entender, replicar, decodificar— es exactamente el tipo de proceso iterativo que define gran parte del trabajo real de auditoría web y análisis de malware, y se apoya directamente en las bases sentadas en los bloques de *Web Requests* y *Web Proxies* vistos anteriormente en este temario.
