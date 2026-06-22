# Prevención de inyección de comandos

## El principio rector: nunca confiar en filtrar lo prohibido

Todos los apartados anteriores de este bloque llegan a la misma conclusión por caminos distintos: las listas negras (de caracteres, de comandos, combinadas con WAFs) son medidas reactivas que reducen el riesgo pero no lo eliminan, porque dependen de anticipar correctamente todo lo que un atacante podría intentar — algo estructuralmente imposible de garantizar frente a la riqueza sintáctica de cualquier shell de sistema. La prevención real exige un cambio de enfoque: en lugar de intentar bloquear lo malicioso, eliminar por completo la posibilidad de que la entrada del usuario se interprete como sintaxis ejecutable.

## Capa 1: evitar ejecutar comandos del sistema cuando no es estrictamente necesario

La medida más efectiva, con diferencia, es **no necesitar** invocar una shell del sistema operativo en primer lugar. Muchas tareas que tradicionalmente se resolvían llamando a un binario externo (comprobar si un host responde, manipular archivos, realizar operaciones de red) tienen hoy equivalentes nativos en la mayoría de lenguajes de programación, sin pasar por una shell:

| Necesidad habitual | Alternativa sin shell |
|---|---|
| Comprobar conectividad de red | Librerías de sockets nativas del lenguaje, en lugar de invocar `ping` |
| Manipular archivos | Funciones nativas de sistema de archivos del lenguaje (`fopen`, `fs.readFile`, etc.) |
| Procesar imágenes, PDFs, etc. | Librerías nativas o bindings específicos, en lugar de invocar utilidades de línea de comandos externas |

Cuando la funcionalidad puede resolverse sin tocar una shell, el vector de inyección de comandos desaparece por completo — no hay nada que sanitizar porque no hay intérprete de comandos involucrado.

## Capa 2: cuando ejecutar un comando externo es inevitable, separar el comando de sus argumentos

Si la funcionalidad realmente necesita invocar un programa externo, la diferencia crítica está en **cómo** se invoca. La causa raíz de la inyección de comandos es que la entrada del usuario se concatena dentro de una **cadena de texto** que después se entrega completa a un intérprete de shell, el cual decide qué partes son comandos, separadores y argumentos.

La alternativa estructuralmente segura: usar las funciones que la mayoría de lenguajes modernos ofrecen para ejecutar un programa pasando sus argumentos como una **lista de valores independientes**, sin pasar nunca por una shell intermedia que tenga que "interpretar" la cadena completa.

- En **PHP**, evitar pasar entrada de usuario a `system()`, `exec()` o `shell_exec()` construida por concatenación; cuando es imprescindible interactuar con procesos externos, recurrir a funciones que invoquen el binario con argumentos como array (similar al patrón de `proc_open()` con argumentos separados) en lugar de una única cadena de comando.
- En **Node.js**, preferir `child_process.execFile()` (que recibe el binario y un array de argumentos por separado) frente a `child_process.exec()` (que construye y ejecuta una cadena completa a través de una shell).
- El mismo principio se aplica en prácticamente cualquier lenguaje: Python distingue entre pasar una cadena con `shell=True` (vulnerable) y pasar una lista de argumentos con `shell=False` (estructuralmente segura) a sus funciones de ejecución de procesos.

Con esta separación, aunque la entrada del usuario contenga caracteres como `;`, `&&` o `|`, **nunca se interpretan como sintaxis de shell** — se tratan como un valor literal de argumento, exactamente el mismo principio que las consultas parametrizadas aplican a la inyección SQL en el bloque anterior: separar estructuralmente "instrucción" de "dato", en lugar de confiar en sanear el dato después de haberlo mezclado con la instrucción.

## Capa 3: validación estricta mediante listas blancas

Cuando la entrada del usuario tiene un formato predecible y acotado (una IP, un nombre de archivo de un conjunto cerrado, un identificador numérico), la validación más robusta no es intentar bloquear caracteres peligrosos, sino **definir explícitamente qué formato se acepta** y rechazar cualquier cosa que no encaje exactamente:

```php
$pattern = '/^((\d{1,3})\.){3}\d{1,3}$/';
if (!preg_match($pattern, $_GET['ip'])) {
    die("Entrada no válida");
}
```

Esta validación de formato, aplicada siempre del lado del **servidor** (nunca confiando únicamente en la validación de frontend, como se vio en el apartado de explotación básica de este mismo bloque), reduce drásticamente la superficie de ataque: si solo se acepta una secuencia de dígitos y puntos con la estructura exacta de una IPv4, ningún operador de shell ni nombre de comando puede colarse dentro de una entrada válida.

## Capa 4: principio de mínimo privilegio en el proceso que ejecuta comandos

Igual que se recomienda en el bloque de SQL Injection limitar los privilegios del usuario de base de datos, el proceso del servidor de aplicaciones que eventualmente invoca comandos del sistema debería ejecutarse con el **mínimo privilegio posible** — un usuario del sistema operativo sin permisos administrativos, con acceso de escritura restringido únicamente a los directorios estrictamente necesarios, y sin acceso a binarios o rutas sensibles del sistema. Esto no impide la inyección en sí, pero limita drásticamente su impacto si, pese a todas las capas anteriores, alguna llegara a fallar.

## Capa 5: entornos aislados (sandboxing y contenedores)

Ejecutar procesos potencialmente sensibles dentro de contenedores o entornos aislados (con acceso restringido al sistema de archivos del host, sin conectividad de red innecesaria, con límites de recursos) añade una capa adicional de contención: incluso si una inyección de comandos tiene éxito, el daño queda confinado al entorno aislado, sin comprometer directamente el servidor de producción ni el resto de la infraestructura.

## La estrategia de defensa en profundidad, resumida

```
1. Evitar invocar una shell siempre que exista una alternativa nativa (la defensa más fuerte)
2. Si es inevitable, separar comando y argumentos sin pasar por un intérprete de shell
3. Validar con listas blancas de formato esperado, siempre en el servidor
4. Ejecutar con el mínimo privilegio posible
5. Aislar en contenedores/sandboxes para limitar el impacto residual
```

Exactamente el mismo patrón de **defensa en profundidad** que ha cerrado cada bloque de explotación de este temario: ninguna medida aislada es perfecta, pero su combinación reduce tanto la probabilidad de que una inyección tenga éxito como el daño potencial si, pese a todo, alguna lo consigue. La diferencia decisiva frente a las listas negras trabajadas en los apartados anteriores de este bloque es que estas capas atacan el problema desde su causa estructural, no desde el intento —siempre incompleto— de anticipar cada variante posible de ataque.
