---
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

# ret2win

Un desafío "ret2win" es simplemente un binario que contiene una función `win()` (o equivalente); una vez que logras redirigir la ejecución hacia ella, completas el desafío.

Para llevar esto a cabo, debemos aplicar lo aprendido en la introducción, pero de manera más precisa: debemos sobrescribir el registro EIP con un valor específico de nuestra elección.

Para lograr esto, necesitamos conocer dos cosas:

* El relleno necesario hasta que comencemos a sobrescribir el puntero de retorno (EIP).
* El valor con el que queremos sobrescribir EIP.

Cuando mencionamos "sobrescribir EIP", nos referimos a sobrescribir el puntero de retorno guardado que se extrae en EIP. El registro EIP no se encuentra en la pila, por lo que no se sobrescribe directamente.

Para determinar el relleno necesario, podemos utilizar una cadena cíclica. Una cadena cíclica es una secuencia de caracteres única que nos ayuda a identificar la posición exacta donde ocurre el desbordamiento. Herramientas como `pwn cyclic` de Pwntools pueden generar estas cadenas.

Una vez que conocemos la cantidad de relleno necesaria, el siguiente paso es encontrar la dirección de la función `win()`. Podemos utilizar herramientas como `objdump` o `nm` para listar las funciones del binario y sus direcciones.

Con esta información, podemos construir nuestra cadena de explotación:

1. Relleno hasta alcanzar el puntero de retorno.
2. Dirección de la función `win()`.

Al proporcionar esta cadena como entrada al programa vulnerable, sobrescribiremos el puntero de retorno con la dirección de `win()`, redirigiendo así la ejecución del programa a dicha función y completando el desafío.
