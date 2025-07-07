---
icon: arrow-right-to-arc
---

# Introducción

La explotación binaria consiste en identificar vulnerabilidades en programas y utilizarlas para que realicen acciones a nuestra conveniencia. Esto puede resultar en la omisión de autenticaciones, la filtración de información confidencial o, en ocasiones (si tenemos suerte), en la ejecución remota de código (RCE, por sus siglas en inglés). Las formas más básicas de explotación binaria ocurren en la pila (stack), una región de la memoria que almacena variables temporales creadas por funciones en el código.

Cuando se llama a una nueva función, se empuja una dirección de memoria de la función que la invocó a la pila. De esta manera, el programa sabe a dónde regresar una vez que la función llamada finaliza su ejecución. Analicemos un binario básico para ilustrar este comportamiento.

### Análisis

El binario consta de dos archivos: `source.c` y `vuln`; este último es un archivo `ELF`, que es el formato ejecutable para Linux (se recomienda seguir este análisis en una máquina virtual propia, preferiblemente con Linux).

Utilizaremos una herramienta llamada `radare2` para analizar el comportamiento del binario cuando se llaman funciones.

El comando `-d` lo ejecuta mientras que `-A` realiza el análisis. Podemos desensamblar la función `main` con:

El comando `s main` busca (mueve) a la función `main`, mientras que `pdf` significa P rint D isassembly F unction (literalmente, desensambla la función).

La llamada a `unsafe` está en `0x080491bb`, así que establezcamos un punto de interrupción allí.

El comando `db` significa d ebug b reakpoint y establece un punto de interrupción. Un punto de interrupción es simplemente un lugar que, al alcanzarse, pausa el programa para que podamos ejecutar otros comandos. Ahora ejecutamos `dc` para d ebug c ontinue; esto simplemente continúa la ejecución del archivo.

Debería detenerse antes de que se llame a `unsafe`; analicemos la parte superior de la pila ahora:

El comando `pxw` le indica a r2 que analice el hexadecimal como palabras, es decir, valores de 32 bits. Aquí solo se muestra el primer valor, que es `0xf7efe000`. Este valor se almacena en la parte superior de la pila, ya que ESP apunta a la parte superior de la pila, en este caso, `0xff984af0`.

Es importante notar que el valor `0xf7efe000` es aleatorio; es un artefacto de procesos anteriores que han utilizado esa parte de la pila. La pila nunca se limpia; simplemente se marca como utilizable, por lo que antes de que se almacenen datos allí, el valor depende completamente de tu sistema.

Avancemos una instrucción más con `ds` (d ebug s tep) y verifiquemos la pila nuevamente. Esto ejecutará la instrucción `call sym.unsafe`.

Observamos que algo ha sido empujado a la parte superior de la pila: el valor `0x080491c0`. Esto parece estar en el binario, pero ¿dónde exactamente? Veamos nuevamente el desensamblado anterior:

Podemos ver que `0x080491c0` es la dirección de memoria de la instrucción posterior a la llamada a `unsafe`. ¿Por qué ocurre esto? Así es como el programa sabe a dónde regresar después de que `unsafe()` ha finalizado.

### Debilidades

Dado que nos interesa la explotación binaria, veamos cómo podemos posiblemente vulnerar esto. Primero, desensamblemos `unsafe` y establezcamos un punto de interrupción en la instrucción `ret`; `ret` es equivalente a `pop eip`, lo que obtendrá el puntero de retorno guardado que analizamos anteriormente en la pila en el registro `eip`. Luego, continuemos y enviemos una gran cantidad de caracteres en la entrada y veamos cómo podría afectar esto.

Ahora leamos el valor en la ubicación donde estaba el puntero de retorno previamente, que como vimos era `0xff984aec`.

¿Qué ha sucedido?

Es bastante simple: ingresamos más datos de los que el programa esperaba, lo que resultó en que sobrescribiéramos más de la pila de lo que el desarrollador anticipó. El puntero de retorno guardado también está en la pila, lo que significa que logramos sobrescribirlo. Como resultado, en la instrucción `ret`, el valor extraído en `eip` no estará en la función anterior, sino en `0x41414141`. Verifiquemos con `ds`.

### Resumen

Cuando una función llama a otra función, realiza las siguientes acciones:

* Empuja un puntero de retorno a la pila para que la función llamada sepa a dónde regresar.
* Cuando la función llamada finaliza su ejecución, extrae este puntero de la pila.
