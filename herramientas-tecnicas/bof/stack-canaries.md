---
icon: stack-overflow
---

# Stack Canaries

Los **Stack Canaries** son una técnica de seguridad utilizada para detectar desbordamientos de búfer en la pila y prevenir la ejecución de código malicioso. Su nombre proviene de la analogía con los canarios en las minas de carbón, que servían como una advertencia temprana de gases tóxicos.

### ¿Qué son los Stack Canaries?

Los Stack Canaries son valores secretos que se colocan en la pila, justo antes del puntero de retorno de una función. Estos valores se generan aleatoriamente al inicio del programa y se verifican antes de que una función retorne. Si el valor del canario ha cambiado, indica que ha ocurrido un desbordamiento de búfer que ha sobrescrito la memoria adyacente, comprometiendo la integridad del flujo de control del programa.

[sans.org](https://www.sans.org/blog/stack-canaries-gingerly-sidestepping-the-cage/?utm_source=chatgpt.com)

### Tipos de Stack Canaries

Existen varios tipos de Stack Canaries, cada uno con sus características particulares:

*   **Canarios Terminadores**: Estos canarios utilizan caracteres de terminación comunes, como nulos (`\0`), retornos de carro (), saltos de línea () o caracteres de formulario de página (`\f`). La idea es que las funciones de manejo de cadenas que dependen de estos caracteres no sobrescriban el canario. Sin embargo, si un atacante escribe un carácter de terminación antes del canario, podría evitar su detección.

    [Wikipedia](https://en.wikipedia.org/wiki/Buffer_overflow_protection?utm_source=chatgpt.com)
*   **Canarios Aleatorios**: Estos canarios se generan de manera aleatoria al inicio del programa y se almacenan en una ubicación protegida de la memoria para dificultar su descubrimiento por parte de un atacante. La aleatoriedad aumenta la seguridad, ya que el atacante no puede predecir el valor del canario.

    [Wikipedia](https://en.wikipedia.org/wiki/Buffer_overflow_protection?utm_source=chatgpt.com)
*   **Canarios Aleatorios con XOR**: En este enfoque, el valor del canario se combina con otras partes de la memoria, como el puntero de retorno, mediante una operación XOR. Esto añade una capa adicional de complejidad, ya que el atacante necesitaría conocer tanto el valor del canario como la disposición de la memoria para explotarlo.

    [Wikipedia](https://en.wikipedia.org/wiki/Buffer_overflow_protection?utm_source=chatgpt.com)

### Funcionamiento de los Stack Canaries

1. **Inserción del Canario**: Al entrar en una función, el compilador inserta un valor de canario en la pila, justo antes del puntero de retorno.
2.  **Verificación del Canario**: Antes de que la función retorne, el valor del canario se verifica. Si el valor ha cambiado, el programa detecta un desbordamiento de búfer y puede tomar acciones preventivas, como abortar la ejecución.

    [sans.org](https://www.sans.org/blog/stack-canaries-gingerly-sidestepping-the-cage/?utm_source=chatgpt.com)

### Limitaciones y Controversias

Aunque los Stack Canaries son efectivos para detectar desbordamientos de búfer que afectan al puntero de retorno, no protegen contra otros tipos de ataques, como los que manipulan punteros de función o utilizan técnicas como Return-Oriented Programming (ROP). Además, si un atacante puede predecir o descubrir el valor del canario, podría eludir esta protección.

[sans.org](https://www.sans.org/blog/stack-canaries-gingerly-sidestepping-the-cage/?utm_source=chatgpt.com)

### Conclusión

Los Stack Canaries son una medida de seguridad valiosa para detectar y prevenir ciertos tipos de ataques de desbordamiento de búfer. Sin embargo, deben implementarse junto con otras técnicas de seguridad, como la aleatorización del espacio de direcciones (ASLR) y la protección de ejecución de datos, para ofrecer una defensa más completa contra las diversas técnicas de explotación.
