---
icon: section
---

# Secuencias de De Bruijn

Una secuencia de De Bruijn de orden n sobre un alfabeto de tamaño k es una cadena cíclica en la que cada subsecuencia posible de longitud n aparece exactamente una vez. Por ejemplo, una secuencia de De Bruijn de orden 3 en un alfabeto binario (0 y 1) podría ser:

```
00010111
```

En esta secuencia, todas las combinaciones posibles de 3 bits (000, 001, 010, 011, 100, 101, 110, 111) aparecen exactamente una vez cuando la secuencia se considera cíclica.

Estas secuencias son útiles en la explotación de desbordamientos de búfer en la pila, ya que permiten identificar de manera precisa la posición en la que ocurre una sobrescritura. Al enviar una secuencia de De Bruijn como entrada a un programa vulnerable, es posible determinar el desplazamiento exacto en el que se produce el desbordamiento al observar el valor específico que causa la falla.

### Generación de Secuencias de De Bruijn

Existen herramientas y scripts que facilitan la generación de estas secuencias. Por ejemplo, en Python, se puede utilizar la biblioteca `pwn` para generar una secuencia de De Bruijn de longitud específica:

```python
from pwn import cyclic

# Genera una secuencia de De Bruijn de 100 caracteres
secuencia = cyclic(100)
print(secuencia)
```

Esta secuencia se puede utilizar como entrada para probar un programa y determinar el punto exacto de sobrescritura analizando el comportamiento del programa tras el desbordamiento.

### Aplicación en la Explotación

Al provocar un desbordamiento de búfer con una secuencia de De Bruijn, el programa vulnerable puede sobrescribir registros importantes, como el puntero de instrucción (EIP). Al analizar el valor específico en el EIP tras el fallo, se puede utilizar la misma herramienta para determinar el offset exacto de la sobrescritura:

```python
from pwn import cyclic_find

# Valor que apareció en el EIP tras el desbordamiento
valor_eip = 0x61616164

# Determina el offset de sobrescritura
offset = cyclic_find(valor_eip)
print(offset)
```

Con el offset identificado, es posible diseñar una carga útil (payload) que sobrescriba el EIP con una dirección de nuestra elección, facilitando la redirección del flujo de ejecución del programa para lograr la explotación deseada.
