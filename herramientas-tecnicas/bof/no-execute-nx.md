---
icon: plug-circle-xmark
layout:
  title:
    visible: true
  description:
    visible: false
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
---

# No eXecute (NX)

El bit No eXecute (NX), también conocido como Execute Disable (XD) en la terminología de Intel, es una característica de seguridad implementada a nivel de hardware en los procesadores modernos. Su función principal es distinguir entre áreas de memoria destinadas a datos y aquellas destinadas a código ejecutable.

[Wikipedia](https://en.wikipedia.org/wiki/NX_bit?utm_source=chatgpt.com)

### ¿Qué es el Bit NX?

El bit NX permite al sistema operativo marcar ciertas regiones de la memoria como no ejecutables. Esto significa que el procesador no permitirá la ejecución de código que resida en estas áreas, ayudando a prevenir ataques que intentan ejecutar código malicioso desde ubicaciones no autorizadas, como la pila o el montón.

[Wikipedia](https://en.wikipedia.org/wiki/NX_bit?utm_source=chatgpt.com)

### Función del Bit NX en la Protección de la Pila

En el contexto de la pila, el bit NX es crucial para mitigar ataques de desbordamiento de búfer. Al marcar la pila como no ejecutable, se evita que el código inyectado en la pila sea ejecutado, incluso si un atacante logra sobrescribir el puntero de retorno para redirigir la ejecución al código malicioso.

[book.hacktricks.wiki](https://book.hacktricks.wiki/es/binary-exploitation/common-binary-protections-and-bypasses/no-exec-nx.html?utm_source=chatgpt.com)

### Implementación y Compatibilidad

La implementación del bit NX varía según la arquitectura del procesador:

*   **x86**: AMD introdujo el bit NX en su arquitectura AMD64, permitiendo la protección de la memoria a nivel de página. Intel implementó una característica similar llamada XD bit en sus procesadores Pentium 4 y posteriores.

    [Wikipedia](https://en.wikipedia.org/wiki/NX_bit?utm_source=chatgpt.com)
*   **ARM**: En la arquitectura ARM, el bit NX se conoce como "Execute Never" (XN) y fue introducido en ARMv6.

    [Wikipedia](https://en.wikipedia.org/wiki/NX_bit?utm_source=chatgpt.com)

Es importante destacar que tanto el sistema operativo como el hardware deben soportar y habilitar la funcionalidad NX para que esta protección sea efectiva.

### Beneficios del Bit NX

* **Prevención de Ejecución de Código Malicioso**: Al impedir la ejecución de código en áreas de memoria no autorizadas, el bit NX ayuda a prevenir ataques que intentan ejecutar código desde la pila o el montón.
*   **Mitigación de Desbordamientos de Búfer**: El bit NX es una medida de seguridad que se implementa a nivel de hardware en los procesadores modernos. Su función principal es marcar ciertas áreas de memoria como no ejecutables, lo que significa que el procesador no permitirá que se ejecute ningún código en esas áreas.

    [servernet.com.ar](https://servernet.com.ar/funcion-nx-bit-del-procesador/?utm_source=chatgpt.com)

### Limitaciones

Aunque el bit NX proporciona una capa adicional de seguridad, no es una solución completa por sí sola. Los atacantes pueden emplear técnicas como la programación orientada a retornos (ROP) para ejecutar código malicioso sin necesidad de ejecutar directamente desde la pila. Por lo tanto, es esencial utilizar el bit NX en conjunto con otras medidas de seguridad, como la aleatorización del espacio de direcciones (ASLR) y las pilas protegidas por hardware.

### Resumen

El bit No eXecute (NX) es una característica de seguridad fundamental que ayuda a proteger la pila y otras áreas de memoria contra la ejecución no autorizada de código. Al comprender su funcionamiento e implementación, los desarrolladores y profesionales de seguridad pueden diseñar sistemas más robustos y resistentes a ataques de desbordamiento de búfer y otras técnicas de explotación.
