# Introducción a XSS

## Qué es

**Cross-Site Scripting (XSS)** aprovecha un fallo en el saneamiento de la entrada del usuario para conseguir que un navegador ejecute código JavaScript que el atacante ha "inyectado" en una página, en el contexto de origen de la propia aplicación legítima.

El mecanismo de fondo: una aplicación web normal recibe HTML del servidor y lo muestra en el navegador del cliente. Si esa aplicación no valida correctamente la entrada del usuario, un atacante puede inyectar JavaScript adicional en un campo (comentario, búsqueda, perfil...) que se ejecutará sin que la víctima lo perciba, simplemente al visualizar esa página.

## Por qué XSS se considera "riesgo medio" pese a su bajo impacto directo en el servidor

XSS se ejecuta **exclusivamente en el lado del cliente** — no compromete directamente el servidor backend. Por eso su impacto técnico directo suele considerarse relativamente bajo. Sin embargo, es una de las vulnerabilidades **más comunes** en aplicaciones web reales, lo que se traduce en la fórmula clásica de evaluación de riesgo:

```
Impacto bajo + Probabilidad alta = Riesgo medio
```

Y "riesgo medio" no significa "ignorable": sigue siendo una prioridad de detección, corrección y prevención en cualquier programa de seguridad serio.

## Qué se puede lograr con XSS

Como el código se ejecuta en el motor JavaScript del navegador de la víctima (V8 en Chrome, SpiderMonkey en Firefox), las posibilidades incluyen:

- Exfiltrar la cookie de sesión de la víctima hacia un servidor controlado por el atacante.
- Forzar al navegador a realizar llamadas a la API de la aplicación en nombre de la víctima (por ejemplo, cambiar su contraseña).
- Minería de criptomonedas no autorizada, fraude publicitario, y prácticamente cualquier acción que JavaScript pueda realizar dentro del navegador.

### Límites de XSS

El código se ejecuta confinado al **motor JS del navegador**: no puede, por sí solo, ejecutar código a nivel de sistema operativo. En navegadores modernos, además, está limitado al **mismo origen** de la aplicación vulnerable (la política de mismo origen, *Same-Origin Policy*). Dicho esto, si se combina con una vulnerabilidad adicional del propio navegador (por ejemplo, un desbordamiento de búfer en el motor de renderizado), un XSS puede servir como **vector de entrega** de un exploit que sí escape del sandbox del navegador y comprometa el sistema operativo subyacente — un escenario poco común, pero documentado.

## Casos reales que ilustran el impacto

- **El gusano Samy (MySpace, 2005)**: una vulnerabilidad XSS almacenada permitió que un script se autopropagara: cada vez que alguien visitaba un perfil infectado, su propio perfil quedaba también infectado con el mensaje "Samy is my hero" y el mismo payload. En menos de 24 horas, más de un millón de usuarios habían visto el mensaje. El payload en sí era inofensivo, pero el mismo vector podría haber robado información de tarjetas de crédito o instalado keyloggers en el navegador de cada víctima.
- **TweetDeck (Twitter, 2014)**: un investigador descubrió accidentalmente una vulnerabilidad XSS que permitió crear un tuit capaz de retuitearse a sí mismo, generando más de 38.000 retuits en menos de dos minutos. Twitter tuvo que cerrar temporalmente TweetDeck para corregirlo.
- **Google Search (2019)**: se descubrió una vulnerabilidad de XSS por mutación (*mutation XSS*) en la barra de búsqueda de Google, derivada de un problema en el manejo de XML.
- **Apache.org**: el propio servidor web más usado del mundo sufrió en su día una vulnerabilidad XSS explotada activamente para robar contraseñas de usuarios de organizaciones concretas.

Estos ejemplos —de aplicaciones extremadamente maduras y con recursos de seguridad considerables— ilustran que XSS no es un problema "de principiantes" exclusivamente: sigue apareciendo, en formas más sutiles, incluso en el software mejor auditado del planeta.

## Los tres tipos de XSS

| Tipo | Dónde se procesa | Persistencia |
|---|---|---|
| **Almacenado (Stored)** | Backend — la entrada se guarda en base de datos y se muestra a cualquier visitante posterior | Persistente: afecta a todo usuario que visite la página, indefinidamente hasta que se elimine |
| **Reflejado (Reflected)** | Backend — la entrada se devuelve inmediatamente en la respuesta sin almacenarse | No persistente: solo afecta a quien visite la URL/petición concreta que contiene el payload |
| **Basado en DOM (DOM-based)** | Exclusivamente en el cliente — nunca llega al servidor | No persistente: depende enteramente del JavaScript del propio navegador, en el momento de la visita |

Los siguientes apartados de este bloque desarrollan cada tipo en profundidad, con ejercicios prácticos paso a paso, antes de pasar a los ataques que se construyen sobre ellos.
