---
icon: radar
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

# Radare2

### Introducción a Radare2

**Radare2 (r2)** es una potente herramienta de **ingeniería inversa**, **análisis binario** y **modificación de ejecutables**. Su versatilidad permite analizar binarios, depurarlos y modificarlos directamente a nivel de **bytes**.

Algunas de sus principales características son:

* **Desensamblado y Análisis**: Permite visualizar código en ensamblador.
* **Depuración**: Compatible con GDB y otros depuradores.
* **Edición de Binarios**: Modificación en caliente de ejecutables.
* **Automatización**: Soporte para scripting con Python y r2pipe.

### Cargar un Binario en Radare2

Para modificar un ejecutable, es necesario cargarlo en Radare2 con permisos de escritura:

```sh
radare2 -A -w binario
```

* **`-A`**: Análisis automático.
* **`-w`**: Permiso de escritura para modificar el binario.

### Navegación y Búsqueda en el Binario

#### Ver el Punto de Entrada

```sh
pdf @ main
```

Este comando nos muestra el **desensamblado** de la función `main`.

Si queremos buscar llamadas a funciones específicas, podemos usar:

```sh
aaa  # Análisis profundo del binario
axt sym.factor2  # Buscar referencias a la función factor2
```

Esto nos indicará en qué parte del código se está llamando `factor2`.

#### Identificar Direcciones de Funciones

Para ver la dirección de una función específica:

```sh
pdf @ sym.factor1
```

Nos devolverá algo como:

```assembly
CODE XREF from sym.factor1 @ 0x22d2(x)
```

### Modificación de Llamadas a Funciones

Vamos a cambiar una llamada a `factor2` para que en su lugar se ejecute `factor1`.

#### Identificar la Dirección de la Llamada

En el desensamblado de `main`, encontramos:

```assembly
0x000023dc      e8fafeffff     call sym.factor2
```

Esto significa que en la dirección `0x000023dc` se está llamando `factor2`.

#### Obtener la Dirección de `factor1`

Ejecutamos:

```sh
pdf @ sym.factor1
```

Nos indica que `factor1` está en:

```assembly
CODE XREF from sym.factor1 @ 0x22d2(x)
```

Ahora, debemos calcular el **desplazamiento relativo** para modificar la instrucción `call`.

### Cálculo del Desplazamiento Relativo

Las instrucciones `call` en x86-64 utilizan direcciones relativas. La fórmula para calcular el desplazamiento es:

```
Desplazamiento = Destino - (Origen + Tamaño de la instrucción)
```

Sabemos que:

* `factor1` = **0x000022d2**
* `call` en **0x000023dc**
* Tamaño de la instrucción `call` = **5 bytes**

Cálculo:

```
0x22d2 - (0x23dc + 5) = -0x33A
```

Convertimos `-0x33A` a **little-endian** en 4 bytes:

```
c6 fc ff ff
```

#### Modificar los Bytes en el Binario

Ahora sobrescribimos la instrucción `call` en `0x000023dc`:

```sh
s 0x000023dc  # Moverse a la dirección
wx e8 c6 fc ff ff @ 0x000023dc  # Escribir los nuevos bytes
wq  # Guardar y salir
```

Para verificar los cambios:

```sh
pd 5 @ 0x000023dc
```

Salida esperada:

```assembly
│           0x000023dc      e8c6fcffff     call sym.factor1
```

### Comprobación y Ejecución del Binario Modificado

Ahora ejecutamos el binario modificado:

```sh
./binario_modificado
```

Si la modificación fue exitosa, `factor1` será llamada en lugar de `factor2`.

### Conclusión

Hemos visto cómo usar **Radare2** para: ✅ Navegar en un binario y encontrar referencias a funciones. ✅ Calcular el desplazamiento relativo de una instrucción `call`. ✅ Modificar bytes a nivel de ensamblador para cambiar la lógica de ejecución.

Este proceso es clave en el **análisis y modificación de binarios**, permitiendo realizar **parches** o incluso crear **exploits** para auditorías de seguridad.

