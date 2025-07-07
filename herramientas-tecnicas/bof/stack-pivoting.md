---
icon: table-pivot
---

# Stack Pivoting

El **Stack Pivoting** es una técnica avanzada utilizada en la explotación de vulnerabilidades, especialmente cuando el espacio disponible en la pila es limitado para ejecutar una cadena completa de ROP (Return-Oriented Programming). Esta técnica permite a un atacante manipular el puntero de pila (RSP) para redirigir el flujo de ejecución a una ubicación controlada, facilitando la ejecución de código malicioso.

### ¿Por qué es útil el Stack Pivoting?

En escenarios donde no se dispone de suficiente espacio en la pila para insertar una cadena ROP completa, el Stack Pivoting ofrece una solución al permitir el control del puntero de pila. Esto posibilita que el atacante establezca la pila en una ubicación conocida y controlada, como una región de memoria en el heap o en la sección BSS, donde puede colocar gadgets y ejecutar su código malicioso.

### ¿Cómo funciona el Stack Pivoting?

El proceso de Stack Pivoting implica tomar control del puntero de pila (RSP) y redirigirlo a una ubicación de memoria que el atacante puede controlar. Esto se logra mediante técnicas como:

* **Uso de Gadgets**: Identificar y utilizar instrucciones existentes en el binario que permitan modificar el valor de RSP. Por ejemplo, buscar gadgets que realicen operaciones como `pop rsp; ret`.
* **Buffer Overflows**: Aprovechar desbordamientos de búfer para sobrescribir el valor de RSP y redirigir la pila a una ubicación controlada.
* **Manipulación de EBP**: En sistemas de 32 bits, manipular el registro EBP para alterar la dirección de retorno y, en consecuencia, el flujo de ejecución.

### Consideraciones de seguridad

La técnica de Stack Pivoting puede eludir diversas medidas de seguridad, como DEP (Data Execution Prevention) y ASLR (Address Space Layout Randomization). Sin embargo, su eficacia puede verse reducida si se implementan defensas adicionales, como:

* **Protección de la pila**: Utilizar canarios de pila para detectar y prevenir modificaciones no autorizadas del puntero de pila.
* **Aleatorización de la disposición del espacio de direcciones (ASLR)**: Aleatorizar las direcciones de memoria para dificultar que los atacantes predigan o controlen las ubicaciones de la pila y otras regiones de memoria.
* **Control de flujo de ejecución**: Implementar técnicas que aseguren que el flujo de ejecución siga rutas predefinidas y no sea redirigido a ubicaciones maliciosas.
