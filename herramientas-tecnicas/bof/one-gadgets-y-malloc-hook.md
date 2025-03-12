---
icon: hockey-mask
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

# One Gadgets y Malloc Hook

## One Gadgets

**One Gadgets** son herramientas desarrolladas por el investigador de seguridad **@oneferris** que permiten identificar y utilizar gadgets en binarios de 64 bits. Estos gadgets son fragmentos de código existentes en el binario que pueden ser encadenados para ejecutar acciones específicas, como invocar funciones del sistema o ejecutar código malicioso. La herramienta facilita la explotación de vulnerabilidades al identificar secuencias de instrucciones que pueden ser aprovechadas sin necesidad de inyectar código adicional.

### Características de One Gadgets

* **Identificación Automática**: Analiza el binario para detectar gadgets potenciales que pueden ser utilizados en ataques.
* **Compatibilidad**: Funciona con binarios de 64 bits, facilitando la explotación en sistemas modernos.
* **Eficiencia**: Permite encontrar gadgets útiles sin la necesidad de realizar un análisis manual exhaustivo del código.

### Uso de One Gadgets

Para utilizar One Gadgets, se ejecuta la herramienta especificando el binario objetivo. La herramienta escaneará el binario en busca de gadgets y proporcionará una lista de direcciones y descripciones que pueden ser utilizadas en un ataque de encadenamiento de gadgets.

***

## Malloc Hook

**Malloc Hook** es una característica de la biblioteca estándar de C que permite a los desarrolladores interceptar y personalizar las funciones de asignación y liberación de memoria, como `malloc()`, `free()`, `realloc()`, entre otras. Esta funcionalidad es útil para depurar, monitorear el uso de memoria o implementar comportamientos personalizados en la gestión de memoria dinámica.

### Uso de Malloc Hook

Para utilizar Malloc Hook, se deben incluir las cabeceras adecuadas y definir las funciones de reemplazo antes de realizar cualquier operación de asignación o liberación de memoria. Por ejemplo, se pueden definir funciones como `__malloc_hook`, `__free_hook`, `__realloc_hook`, entre otras, que serán llamadas en lugar de las funciones estándar correspondientes.

```c
cCopiarEditar#include <stdio.h>
#include <stdlib.h>

void* my_malloc(size_t size) {
    printf("Allocating %zu bytes\n", size);
    return malloc(size);
}

void my_free(void* ptr) {
    printf("Freeing memory at %p\n", ptr);
    free(ptr);
}

int main() {
    // Reemplazar las funciones de malloc y free
    __malloc_hook = my_malloc;
    __free_hook = my_free;

    // Realizar operaciones de asignación y liberación de memoria
    int* ptr = malloc(sizeof(int));
    free(ptr);

    return 0;
}
```

Es importante tener en cuenta que el uso de Malloc Hook puede afectar el comportamiento del programa y debe ser utilizado con precaución. Además, en entornos multihilo, el uso de Malloc Hook puede ser complejo debido a problemas de sincronización.
