---
icon: angles-left
---

# ret2csu

**ret2csu** es una técnica avanzada de explotación en el ámbito de la programación orientada a retornos (ROP) que permite a un atacante manipular el flujo de ejecución de un programa, incluso cuando los gadgets disponibles son limitados. Esta técnica se basa en la explotación de funciones específicas presentes en la biblioteca estándar de C (libc), como `__libc_csu_init()`, para controlar registros críticos utilizados en las convenciones de llamadas, como `rdi`, `rsi` y `rdx`.

### ¿Por qué es útil ret2csu?

En escenarios donde los gadgets son escasos o inexistentes, ret2csu ofrece una solución al aprovechar funciones predefinidas en la libc que contienen secuencias de instrucciones útiles. Esto permite a los atacantes establecer los valores necesarios en los registros de llamada sin depender de gadgets adicionales.

### Funcionamiento de ret2csu

La técnica ret2csu se basa en dos gadgets específicos presentes en la función `__libc_csu_init()`. Estos gadgets permiten cargar valores en los registros `rdi`, `rsi` y `rdx`, que son utilizados para pasar argumentos a las funciones en arquitecturas x86\_64. Al manipular el flujo de ejecución para invocar estos gadgets con los valores deseados, un atacante puede controlar el comportamiento del programa y, potencialmente, ejecutar código malicioso.

### Implementación de ret2csu

La implementación de ret2csu implica identificar y encadenar estos gadgets para establecer los registros necesarios antes de llamar a la función objetivo, como `system()`, con los argumentos deseados, como `/bin/sh`. Herramientas como **pwntools** en Python facilitan la construcción de cargas útiles ROP y la manipulación de estas secuencias.

**Ejemplo de uso con pwntools**:

```python
pythonCopiarEditarfrom pwn import *

# Cargar el binario
elf = context.binary = ELF('./binario_vulnerable', checksec=False)

# Iniciar el proceso
p = elf.process()

# Crear el objeto ROP
rop = ROP(elf)

# Definir la dirección de la función system y el argumento '/bin/sh'
system_addr = elf.symbols['system']
bin_sh_addr = next(elf.search(b'/bin/sh'))

# Construir la carga útil
rop.raw('A' * offset)  # Rellenar hasta la dirección de retorno
rop.system(bin_sh_addr)  # Llamar a system('/bin/sh')

# Enviar la carga útil
p.sendline(rop.chain())

# Interactuar con la shell
p.interactive()
```

En este ejemplo, se utiliza pwntools para construir una cadena ROP que sobrescribe la dirección de retorno y llama a `system()` con el argumento `/bin/sh`, logrando así la ejecución de una shell.

### Consideraciones de seguridad

La técnica ret2csu puede ser mitigada mediante la implementación de medidas de seguridad como:

* **Full RELRO**: Evita la escritura en la GOT, dificultando la manipulación de direcciones de funciones.
* **ASLR (Address Space Layout Randomization)**: Aleatoriza las direcciones de funciones y estructuras de datos, dificultando la predicción de direcciones objetivo.
* **Stack Canaries**: Detectan y previenen desbordamientos de búfer que intentan sobrescribir direcciones de retorno.
* **NX (No eXecute)**: Previene la ejecución de código en regiones de memoria no ejecutables, dificultando la ejecución de shellcodes.

Es importante destacar que, aunque estas medidas aumentan la seguridad, una combinación adecuada de ellas es esencial para proteger los sistemas contra técnicas como ret2csu.
