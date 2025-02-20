---
icon: file-word
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

# Activación de Office Permanente

> NOTA:

Antes de empezar con el tutorial, debemos de tener el office instalado para que funcione (Sin activar).

## <mark style="color:purple;">PowerShell como Admin</mark>

Primero abrimos el `PowerShell` como administrador dandole click izquierdo en el mismo y `Ejecutar como administrador`, esto se nos abrira con los privilegios maximos para realizar lo siguiente.

### Ejecución de comando (Activación)

URL = [Microsoft Activation Scripts (MAS) | MAS](https://massgrave.dev/)

Ejecutamos el siguiente comando...

```powershell
irm https://get.activated.win | iex
```

Esto nos abrira otra termina en el que nos dara varias opciones a elegir, por lo que le daremos al numero `2`, esto nos abrira otra ventana de terminal con otro menu y en el segundo menu le damos al numero `1`

Una vez echo eso, se nos hara el proceso automaticamente y acabara con un mensaje poniendo que ya se activo el office de forma permanente en `verde` y con esto ya tendriamos el office activado.
