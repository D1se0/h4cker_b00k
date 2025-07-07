---
icon: merge
---

# Shellcode

El término _shellcode_ se refiere a una secuencia de instrucciones en lenguaje ensamblador que, al ser ejecutadas, generalmente inician una shell o intérprete de comandos en el sistema objetivo. Estas secuencias se utilizan comúnmente en la explotación de vulnerabilidades de desbordamiento de búfer para lograr la ejecución arbitraria de código.

### Propósito y Funcionamiento

El propósito principal de un shellcode es proporcionar al atacante una interfaz de comandos en la máquina comprometida, permitiéndole ejecutar órdenes con los privilegios del proceso afectado. Para lograr esto, el shellcode se inyecta en la memoria del programa vulnerable, generalmente a través de un desbordamiento de búfer, y se redirige el flujo de ejecución para que el procesador ejecute el shellcode en lugar del código legítimo.

### Construcción de un Shellcode

La creación de un shellcode efectivo implica escribir código en ensamblador que realice las acciones deseadas, como abrir una shell. Este código se convierte luego en una secuencia de bytes que puede ser inyectada en la memoria del programa objetivo. Es crucial que el shellcode sea compacto y no contenga caracteres nulos (0x00), ya que estos podrían interrumpir la inyección o ejecución del código.

A continuación, se muestra un ejemplo de shellcode en lenguaje C que ejecuta una shell en sistemas Linux:

```c
char shellcode[] =
 "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f"
 "\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0"
 "\x0b\xcd\x80";
```

Este shellcode realiza las siguientes acciones:

* Limpia los registros EAX, EBX, ECX y EDX.
* Empuja la cadena "/bin/sh" en la pila.
* Configura los registros para apuntar a la cadena y establece los parámetros necesarios.
* Invoca la interrupción 0x80 para ejecutar la llamada al sistema `execve`, que inicia una shell.

### Consideraciones de Seguridad

Debido a que los shellcodes se utilizan para explotar vulnerabilidades y ejecutar código arbitrario, representan una amenaza significativa para la seguridad informática. Para mitigar estos riesgos, se han implementado diversas técnicas de protección, como la prevención de ejecución en áreas de datos (DEP) y la aleatorización del diseño del espacio de direcciones (ASLR), que dificultan la inyección y ejecución de shellcodes.
