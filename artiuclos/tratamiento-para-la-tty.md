---
icon: rectangle-terminal
---

# Tratamiento para la TTY

Cuando obtenemos acceso a un sistema víctima mediante una **reverse shell**, muchas veces nos encontramos con un entorno limitado donde ciertas funciones no están disponibles, como el uso de `su`, edición de texto o incluso comandos que requieren interacción. Para solucionar esto, podemos mejorar la TTY y convertirla en una terminal completamente interactiva.

***

### <mark style="color:green;">**¿Qué es una TTY y por qué mejorarla?**</mark>

En sistemas UNIX/Linux, una **TTY (Teletype Terminal)** es la interfaz de línea de comandos que permite la interacción con el sistema. Cuando obtenemos una **reverse shell**, normalmente estamos en un **PTY (Pseudo-terminal)** básico que no tiene las capacidades de una TTY real.

#### ⚠️ **Problemas comunes en una Reverse Shell sin tratamiento de TTY:**

* No podemos usar comandos interactivos como `sudo`, `su`, `nano`, `vim`.
* La terminal no reconoce combinaciones como `Ctrl + C` o `Ctrl + Z`.
* La salida de comandos puede mostrarse de manera incorrecta o sin formateo adecuado.
* Problemas al ejecutar programas que dependen de una terminal real.

Para evitar estos problemas, aplicamos una serie de ajustes que convierten nuestra shell en una más funcional.

***

### <mark style="color:purple;">**Creación de una TTY interactiva con**</mark><mark style="color:purple;">**&#x20;**</mark><mark style="color:purple;">**`script`**</mark>

```shell
script /dev/null -c bash
```

📌 Este comando **inicia un entorno TTY funcional** ejecutando `bash` dentro de un pseudo-terminal gestionado por `script`.

#### 🔍 **Explicación:**

* `script` crea una sesión de terminal grabable.
* `/dev/null` evita la creación de un archivo de log innecesario.
* `-c bash` ejecuta `bash` dentro de esta sesión.

✅ **Esto nos permite una mejor interacción con la shell y mayor compatibilidad con herramientas interactivas.**

***

### <mark style="color:purple;">**Mejorando la Terminal y Ajustando TTY Manualmente**</mark>

Una vez obtenida la shell, podemos mejorarla con los siguientes pasos:

#### 🛠️ **Poner la Shell en Segundo Plano y Modificar `stty`**

```shell
# <Ctrl> + <Z>   (Para suspender la shell)
stty raw -echo; fg
reset xterm
export TERM=xterm
export SHELL=/bin/bash
```

#### 🔍 **Explicación:**

1. **Suspender la shell con `<Ctrl> + <Z>`**
   * Esto envía la shell en segundo plano y nos permite modificar la terminal.
2. **Configurar `stty raw -echo`**
   * `stty raw` -> Pone la terminal en modo raw, permitiendo un control más completo.
   * `stty -echo` -> Desactiva el eco de caracteres, evitando doble impresión en pantalla.
3. **`fg` (Foreground)**
   * Vuelve a traer la shell a primer plano para seguir interactuando.
4. **`reset xterm`**
   * Restablece la terminal con una configuración más adecuada.
5. **Exportar variables esenciales:**
   * `export TERM=xterm` → Define el tipo de terminal como `xterm`, asegurando compatibilidad.
   * `export SHELL=/bin/bash` → Nos aseguramos de que estamos en `bash` en lugar de `sh` u otra shell limitada.

✅ **Esto mejora la estabilidad de la sesión y evita problemas con la ejecución de ciertos comandos.**

***

### <mark style="color:purple;">**Ajustando el Tamaño de la Terminal**</mark>

Algunas aplicaciones dependen de conocer el tamaño de la terminal. Podemos verificar y ajustar sus dimensiones con los siguientes comandos:

#### 📏 **Ver el tamaño de la terminal en el host víctima**

```sh
stty size
```

Este comando devuelve las dimensiones actuales en **filas (rows) y columnas (columns)**, por ejemplo:

```shell
24 80
```

#### 🔄 **Ajustar manualmente el tamaño de la terminal**

```shell
stty rows <ROWS> columns <COLUMNS>
```

Ejemplo:

```shell
stty rows 40 columns 100
```

✅ **Esto garantiza que programas como `vi`, `nano` o incluso `less` se rendericen correctamente.**

***

### <mark style="color:purple;">**Conclusión**</mark>

El tratamiento de una TTY en una reverse shell es **esencial** para mejorar la estabilidad y funcionalidad de la sesión. Aplicando estos ajustes, podemos convertir una shell limitada en una terminal completamente interactiva, lo que nos permite ejecutar herramientas avanzadas sin restricciones.

🚀 **¡Ahora tu reverse shell será mucho más poderosa!** 🏴‍☠️

### <mark style="color:orange;">Código utilizado completo</mark>

```shell
script /dev/null -c bash
```

```shell
# <Ctrl> + <z>
stty raw -echo; fg
reset xterm
export TERM=xterm
export SHELL=/bin/bash

# Para ver las dimensiones de nuestra consola en el Host
stty size

# Para redimensionar la consola ajustando los parametros adecuados
stty rows <ROWS> columns <COLUMNS>
```
