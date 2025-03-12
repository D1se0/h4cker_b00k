---
icon: pen-swirl
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

# Sobrescritura de la Tabla de Desplazamiento Global (GOT)

La **Tabla de Desplazamiento Global (GOT)** es una estructura utilizada en programas con enlace dinámico para gestionar las direcciones de las funciones y variables importadas. Manipular o sobrescribir las entradas de la GOT es una técnica común en la explotación de binarios, permitiendo a los atacantes redirigir la ejecución del programa hacia código malicioso.

### ¿Qué es la GOT?

La GOT es una tabla que almacena las direcciones reales de las funciones y variables importadas en un programa. Durante la ejecución, el enlazador dinámico resuelve estas direcciones, permitiendo que el programa acceda a funciones de bibliotecas compartidas, como `libc`. Cada entrada de la GOT corresponde a una función o variable externa utilizada por el programa.

### ¿Cómo funciona la sobrescritura de la GOT?

Los atacantes pueden explotar vulnerabilidades, como desbordamientos de búfer o cadenas de formato, para sobrescribir las entradas de la GOT. Al hacerlo, pueden redirigir las llamadas a funciones legítimas hacia direcciones de funciones maliciosas, como `system()`, que pueden ejecutar comandos arbitrarios.

### Ejemplo de explotación

Consideremos el siguiente código vulnerable:

```c
cCopiarEditar#include <stdio.h>

void vuln() {
    char buffer[300];
    while (1) {
        fgets(buffer, sizeof(buffer), stdin);
        printf(buffer);
        puts("");
    }
}

int main() {
    vuln();
    return 0;
}
```

En este ejemplo, la función `vuln()` contiene una vulnerabilidad de cadena de formato. Un atacante podría usar esta vulnerabilidad para sobrescribir la entrada de la GOT correspondiente a `printf()`, redirigiéndola a `system()`. De esta manera, al llamar a `printf()`, el programa ejecutaría `system()`, permitiendo al atacante ejecutar comandos arbitrarios.

[ir0nstone.gitbook.io](https://ir0nstone.gitbook.io/notes/binexp/stack/got-overwrite/exploiting-a-got-overwrite?utm_source=chatgpt.com)

### Pasos para la explotación

1. **Identificación de la vulnerabilidad**: Detectar que el programa permite la entrada de datos sin una validación adecuada, como en el caso de la función `vuln()`.
2. **Análisis del binario**: Utilizar herramientas como `gdb` o `objdump` para identificar las direcciones de las funciones y las entradas de la GOT.
3. **Construcción del payload**: Crear una cadena de formato que sobrescriba la entrada de la GOT de `printf()` con la dirección de `system()`.
4. **Ejecución del ataque**: Proporcionar el payload como entrada al programa, redirigiendo la ejecución a la función deseada.

### Consideraciones de seguridad

La sobrescritura de la GOT es una técnica poderosa, pero su eficacia puede verse reducida por medidas de seguridad modernas, como:

* **Protección de pila**: Mecanismos como canarios de pila que detectan y previenen desbordamientos.
* **Aleatorización del espacio de direcciones (ASLR)**: Hace que las direcciones de memoria sean impredecibles, dificultando la localización de la GOT y otras estructuras.
* **No ejecución (NX)**: Previene la ejecución de código en áreas de memoria no destinadas a código, como la pila.

A pesar de estas medidas, técnicas como la sobrescritura de la GOT siguen siendo efectivas en sistemas con configuraciones de seguridad débiles o deshabilitadas.

### Conclusión

La sobrescritura de la GOT es una técnica de explotación que permite a los atacantes redirigir la ejecución de un programa manipulando las direcciones de las funciones importadas. Comprender este método es esencial para desarrollar defensas efectivas contra ataques de ejecución de código arbitrario.
