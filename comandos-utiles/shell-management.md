---
icon: square-terminal
---

# Shell Management

### Sanitización de Shell (TTY)

#### Recuperar TTY interactiva

```bash
script /dev/null -c bash
```

Crea una sesión de pseudo-terminal

```bash
# <Ctrl> + <z> para suspender
stty raw -echo; fg
reset xterm
export TERM=xterm
export SHELL=/bin/bash
```

* `stty raw -echo`: Configura terminal en modo raw
* `reset xterm`: Reinicia configuración terminal
* Variables de entorno para shell interactiva

#### Manejo de dimensiones de consola

```bash
stty size
# Muestra filas y columnas actuales

stty rows <ROWS> columns <COLUMNS>
# Ajusta dimensiones de la terminal
```
