---
icon: fork
---

# Creación de Procesos: fork

En sistemas operativos tipo Unix, la creación de procesos se realiza comúnmente mediante la llamada al sistema **`fork()`**. Esta operación permite que un proceso (denominado _padre_) genere una copia de sí mismo, creando un nuevo proceso hijo.

### ¿Qué es `fork()`?

La función `fork()` crea un nuevo proceso al duplicar el proceso que la invoca. Tras ejecutar `fork()`, existen dos procesos en ejecución:

* **Proceso Padre**: Es el proceso original que invocó `fork()`.
* **Proceso Hijo**: Es la copia del proceso padre, con su propio espacio de direcciones y recursos.

Ambos procesos continúan su ejecución desde el punto donde se realizó la llamada a `fork()`.

### Funcionamiento de `fork()`

Al invocar `fork()`, el sistema operativo realiza las siguientes acciones:

1. **Duplicación del Espacio de Direcciones**: Se crea una copia del espacio de direcciones del proceso padre para el hijo. En sistemas modernos, se utiliza la técnica de _copy-on-write_, donde la memoria física no se copia inmediatamente; en su lugar, ambas copias apuntan a las mismas páginas de memoria hasta que una de ellas realiza una modificación.
2. **Identificación de Procesos**: La función `fork()` devuelve:
   * **0** al proceso hijo.
   * Un número positivo que representa el ID del proceso hijo al proceso padre.

Esto permite que cada proceso determine su rol y actúe en consecuencia.

### Uso Común: `fork()` seguido de `exec()`

Una práctica común es que el proceso hijo, después de ser creado, reemplace su imagen de proceso con otro programa utilizando la llamada al sistema `exec()`. Este patrón, conocido como _fork-exec_, permite que un proceso ejecute un programa diferente al suyo.

El flujo típico es:

1. **Proceso Padre**: Invoca `fork()` para crear un proceso hijo.
2. **Proceso Hijo**: Llama a `exec()` para cargar y ejecutar un nuevo programa.

Este enfoque es fundamental en sistemas Unix y permite la creación y gestión eficiente de procesos.

### Consideraciones Adicionales

* **Manejo de Recursos**: El proceso hijo hereda recursos del padre, como descriptores de archivos. Es esencial que el padre cierre los descriptores que no necesita antes de llamar a `fork()`, y que el hijo cierre los que no utilizará.
* **Terminación de Procesos**: Tras finalizar su ejecución, el proceso hijo envía una señal `SIGCHLD` al padre. Si el padre no recoge el estado de salida del hijo utilizando `wait()`, el hijo puede convertirse en un proceso zombi, ocupando recursos del sistema innecesariamente.
* **Compatibilidad**: Sistemas operativos como Windows no implementan `fork()` de la misma manera que Unix. En Windows, se utilizan funciones como `CreateProcess()` para crear nuevos procesos.
