---
icon: reel
---

# RELRO (Relocation Read-Only)

**RELRO (Relocation Read-Only)** es una característica de seguridad utilizada en binarios ELF (Executable and Linkable Format) para proteger las tablas de desplazamiento (relocation tables), como la **Tabla de Desplazamiento Global (GOT)**, de modificaciones maliciosas durante la ejecución del programa. Esta protección dificulta que los atacantes redirijan funciones o alteren el flujo de ejecución del programa.

### Tipos de RELRO

Existen dos niveles de protección RELRO:

#### Partial RELRO

En **Partial RELRO**, solo una parte de la GOT se marca como de solo lectura después de que el enlazador dinámico resuelve las direcciones de las funciones. Esto significa que algunas entradas de la GOT pueden seguir siendo modificadas en tiempo de ejecución, lo que permite ciertos ataques, como la sobrescritura de entradas de la GOT. Esta configuración ofrece una protección básica con un impacto mínimo en el rendimiento.

**Habilitación de Partial RELRO:**

```bash
bashCopiarEditargcc -Wl,-z,relro -o mi_programa mi_programa.c
```

#### Full RELRO

En **Full RELRO**, toda la GOT se marca como de solo lectura después de la resolución de direcciones, impidiendo cualquier modificación en tiempo de ejecución. Además, el enlazador resuelve todas las direcciones de funciones al inicio de la ejecución del programa, eliminando la posibilidad de ataques que dependan de la modificación de la GOT. Sin embargo, esta configuración puede aumentar el tiempo de carga del programa debido al procesamiento adicional requerido durante el enlace.

**Habilitación de Full RELRO:**

```bash
bashCopiarEditargcc -Wl,-z,relro,-z,now -o mi_programa mi_programa.c
```

### Beneficios de RELRO

* **Protección contra sobrescritura de la GOT**: RELRO dificulta que los atacantes modifiquen las entradas de la GOT, reduciendo el riesgo de redirigir funciones críticas del sistema.
* **Mejora de la seguridad en binarios dinámicamente enlazados**: Al proteger las tablas de desplazamiento, RELRO aumenta la resistencia de los programas que dependen de bibliotecas compartidas.

### Consideraciones

* **Impacto en el rendimiento**: Mientras que Partial RELRO tiene un impacto mínimo, Full RELRO puede aumentar el tiempo de carga del programa debido a la resolución completa de direcciones en tiempo de inicio.
* **Compatibilidad**: No todos los sistemas o herramientas de depuración son compatibles con Full RELRO. Es importante verificar la compatibilidad antes de implementar esta protección.

### Conclusión

Implementar RELRO en la compilación de programas es una práctica recomendada para mejorar la seguridad, especialmente en aplicaciones que utilizan enlaces dinámicos. La elección entre Partial y Full RELRO debe basarse en un equilibrio entre los requisitos de seguridad y el rendimiento deseado.
