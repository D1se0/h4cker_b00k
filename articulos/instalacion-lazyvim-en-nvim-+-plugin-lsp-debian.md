---
icon: vimeo-v
---

# Instalación Lazyvim en nvim + Plugin LSP (Debian)

## Introducción

Neovim es un editor de texto altamente configurable y potente. En esta guía, aprenderemos a personalizarlo para que tenga una **interfaz más estética e intuitiva**, además de contar con **resaltado de sintaxis** y soporte para múltiples lenguajes de programación.

Para mejorar la experiencia de programación, utilizaremos el **plugin LSP (Language Server Protocol)**, que ofrece funcionalidades avanzadas como autocompletado, sugerencias de código y detección de errores según el lenguaje del archivo.

* Más información: [LazyVim](https://www.lazyvim.org/)

### Requisitos

| Requisito                                      | Versión mínima / Notas     | Comentario                                                                                                                                                        |
| ---------------------------------------------- | -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Neovim                                         | ≥ 0.11.2                   | Debe estar compilado con LuaJIT                                                                                                                                   |
| Git                                            | ≥ 2.19.0                   | Para soportar "partial clones"                                                                                                                                    |
| Nerd Font                                      | v3.0 o superior (opcional) | Necesario para mostrar algunos íconos                                                                                                                             |
| lazygit                                        | Opcional                   | Herramienta para gestión de repositorios                                                                                                                          |
| tree-sitter-cli y compilador C                 | —                          | Requerido por nvim-treesitter                                                                                                                                     |
| curl                                           | —                          | Necesario para blink.cmp (motor de autocompletado)                                                                                                                |
| fzf-lua                                        | Opcional                   | Requiere: - fzf ≥ 0.25.1 - ripgrep para búsqueda en vivo - fd para búsqueda de archivos                                                                           |
| Terminal compatible con True Color y undercurl | —                          | Recomendados: - kitty (Linux & macOS) - wezterm (Linux, macOS & Windows) - alacritty (Linux, macOS & Windows) - iterm2 (macOS) - ghostty (Linux, macOS & Windows) |

## Instalación nvim

Para comenzar, instalaremos la herramienta base:

```shell
sudo apt update
sudo apt install neovim
```

## Instalación Lazyvim

Seguiremos las instrucciones oficiales de LazyVim: [Instalación LazyVim](https://www.lazyvim.org/installation)

1. **Eliminar configuraciones antiguas** (previene conflictos):

```shell
# required
mv ~/.config/nvim{,.bak}

# optional but recommended
mv ~/.local/share/nvim{,.bak}
mv ~/.local/state/nvim{,.bak}
mv ~/.cache/nvim{,.bak}
```

2. **Clonar el repositorio oficial de LazyVim**:

```shell
git clone https://github.com/LazyVim/starter ~/.config/nvim
```

3. **Eliminar el repositorio Git dentro del clon** (innecesario):

```shell
rm -rf ~/.config/nvim/.git
```

4. **Iniciar Neovim**:

```shell
nvim
```

Al abrirlo, LazyVim comenzará a instalar los plugins y dependencias necesarios. Durante este proceso, puedes navegar por el menú utilizando `Shift + <LETRA>`:

* `Shift + I` → Install (instalar plugins)
* `Shift + U` → Update (actualizar plugins)
* `Shift + S` → Sync (sincronizar cambios)

Una vez finalizado el proceso, sal del editor con:

```
:q!
```

## Instalación plugin LSP

La guía oficial de LazyVim para LSP está disponible aquí: [Plugin LSP LazyVim](https://www.lazyvim.org/plugins/lsp)

Antes de instalar el plugin, necesitamos algunas dependencias:

```shell
sudo apt install npm
sudo npm install -g pyright
```

### Configuración personalizada de LSP para Python

Creamos un archivo de configuración para el plugin LSP:

```shell
nano ~/.config/nvim/lua/plugins/lsp.lua
```

Dentro del archivo, pegamos lo siguiente:

```
return {
  {
    "neovim/nvim-lspconfig",
    opts = {
      servers = {
        pyright = {
          settings = {
            python = {
              analysis = {
                autoSearchPaths = true,       -- busca paquetes instalados
                useLibraryCodeForTypes = true,
                diagnosticMode = "workspace",
                autoImportCompletions = true, -- SUGERIR IMPORTS automáticamente
              },
            },
          },
        },
      },
    },
  },
}
```

### Probar la configuración

1. Abrimos un archivo Python para probar:

```shell
nvim test.py
```

2. Ejecutamos el comando `LazyVim`:

```
:Lazy
```

Dentro del menú:

* `Shift + U` → Actualizar plugins
* `Shift + S` → Sincronizar
* `Shift + I` → Instalar (por si falta algo)

3. Una vez finalizado, salimos con:

```
:q
```

### Comprobación del autocompletado

Ahora, dentro de un archivo Python:

* Escribe `imp` → debería sugerirte `import`
* Escribe `import req` → debería sugerirte paquetes instalados como `requests`, etc.

Con esto, tendrás **NeoVim, LazyVim y LSP configurados correctamente**, listos para programar de forma cómoda y potente.
