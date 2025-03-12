---
icon: crosshairs-simple
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

# NOPs

En el contexto de la explotación de desbordamientos de búfer, los NOPs (No Operation) son instrucciones que no realizan ninguna acción y se utilizan para facilitar la ejecución de código malicioso.

### ¿Qué son los NOPs?

Los NOPs son instrucciones que, al ejecutarse, no alteran el estado del procesador ni de la memoria. En arquitecturas como x86, la instrucción NOP se representa comúnmente con el byte `0x90`.

### Uso de NOPs en Explotación

Durante un ataque de desbordamiento de búfer, un atacante puede inyectar código malicioso en la pila. Para garantizar que el puntero de retorno sobrescrito apunte a la ubicación correcta del shellcode, se utilizan cadenas de NOPs. Estas cadenas crean una "zona de aterrizaje" amplia, aumentando las posibilidades de que la ejecución del programa alcance y ejecute el shellcode inyectado.

### Ejemplo de Implementación

Consideremos un programa vulnerable que no verifica adecuadamente los límites de un búfer. Al enviar una entrada que sobrescribe el puntero de retorno con la dirección de inicio de una cadena de NOPs seguida del shellcode, el atacante puede redirigir el flujo de ejecución al shellcode. La presencia de NOPs asegura que, incluso si la dirección de retorno no apunta exactamente al inicio del shellcode, la ejecución caerá dentro de la zona de NOPs y continuará hasta alcanzar el código malicioso.

### Resumen

Los NOPs son herramientas esenciales en la explotación de desbordamientos de búfer, ya que permiten al atacante crear una zona de aterrizaje flexible para el shellcode, aumentando la fiabilidad del ataque.
