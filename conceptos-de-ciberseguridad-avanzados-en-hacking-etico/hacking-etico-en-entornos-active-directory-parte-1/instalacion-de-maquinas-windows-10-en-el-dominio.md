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

# Instalación de máquinas Windows 10 en el dominio

Ahora vamos a instalar 2 `Windows 10` para meterlos dentro del dominio de nuestro `DC`.

URL = [Download Windows10](https://www.microsoft.com/es-es/software-download/windows10)

Una vez que nos hayamos descargado la `ISO` instalaremos el primer `Windows` en `VMWare` siguiendo las instrucciones y lo nombraremos como `WS01.corp.local`, seleccionaremos `Windows 10 Pro` y como credenciales seria `santiago:1234`, una vez que haya terminado la instalacion del primer `Windows` estando dentro del escritorio, crearemos el segundo `Windows` nombrandolo `WS01.corp.local`, eligiendo `Windows 10 Pro` y con las siguientes credenciales `santiago2:1234`, una vez realizado todo lo anterior, ya estariamos listos para pasar a la siguiente fase de configuracion.

Ahora nosotros en vez de autenticarnos contra los servicios de `Windows` como hemos echo con estos 2 `Windows 10` de estos 2 usuarios, lo que queremos hacer es delegar todo esto a nuestro `controlador de dominio` sin necesidad de que tengamos que hacerlo de manera local, para que asi podamos nosotros como `administradores` controlar a que tiene acceso dicho usuario o las configuraciones necesarias desde nuestro `DC`.

### Cambio de nombre de los equipos Windows 10

Vamos a cambiar el nombre de los 2 equipos para que tengan una identificacion mas sencilla de la siguiente forma:

buscaremos `Este equipo` -> click derecho `Propiedades` -> `Cambiar nombre de este equipo` -> pondremos `WS01` para el primero y `WS02` para el segundo -> `Siguiente` -> `Reiniciar Ahora`.

Una vez que se hayan reiniciado los equipos, veremos que se cambio el nombre correctamente.

### Meter los 2 Windows dentro del dominio .corp.local

Ahora si nosotros queremos meter a dichas maquinas dentro del dominio de `Active Directory` del `DC` ya que el `controlador de dominio` actua como `DNS` y puede controlar las IP's que estan dentro del dominio con su nombre de dominio, que es el nombre del `host/maquina` (Ejemplo: `WS01 o WS02`) seguido del nombre del dominio `.corp.local` todo esto lo podremos hacer de la siguiente forma:

#### Configuración de red para los Windows

Pero antes de hacerlo ajustaremos los ajustes de red para los 2 equipos:

Le daremos click derecho al adaptador de red -> `Abrir configuracion de red e internet` -> `Ethernet` -> `Cambiar las opciones del adaptador` -> dentro de `Ethernet0` le damos a `Propiedades` con click derecho -> `Protocolo de internet version 4 (TCP/IPv4)` le damos a `Propiedades` -> dentro de `Usar la siguiente direccion DNS` pondremos `192.168.5.5` y en las opciones de `IP` las dejaremos como estan de forma automatica -> `Aceptar` -> `Cerrar`.

Esto lo hacemos ya que nuestro `DC` actua de por si como un servidor `DNS`.

Ahora le daremos dentro de la seccion `Ethernet` -> `Configuracion de uso compartido avanzadas` -> vamos activar la seccion de `Deteccion de redes` y `Compartir archivos e impresoras` -> `Guardar cambios`

Con esto ya estaria todo configurado en tema de redes.

Ahora siguiendo el punto `Meter los 2 Windows dentro del dominio .corp.local` haremos lo siguiente:

Nos iremos a nuestro `DC` y en el panel del `Administrador del servidor` tendremos que crear los 2 usuarios a nivel de dominio para que lo podamos asociar a las 2 maquinas de `Windows 10` y asi que esten contectadas con el `DC`.

Nos iremos a `Herramientas` -> `Centro de administracion de Active Directory` -> `Corp(local)` -> `Users` -> en la parte del panel derecho donde pone `Users` le daremos a `Nuevo` -> `User` -> le pondremos al primer usuario como nombre `empleado1` el nombre de inicio de sesion tambien se lo pondremos igual como `empleado1` y como contraseña le pondremos `Passw0rd2` -> `Otras opciones de contraseña` -> seleccionar `La contraseña nunca expira` -> `Aceptar`.

Echo esto haremos lo mismo pero con el segundo usuario llamandose `empleado2` el nombre de inicio de sesion igual `empleado2`, su contraseña `Passw0rd3` -> `Otras opciones de contraseña` -> seleccionar `La contraseña nunca expira` -> `Aceptar`.

Con esto ya tendriamos los 2 usuarios creados correctamente a nivel de dominio, ahora solo tendremos que vincular cada uno con el equipo de `Windows 10` correspondiente para que esten dentro del dominio del `DC`.

#### Vincular los equipos de `Windows 10` a los 2 usuarios creados en el `DC`

Llendonos a los equipos de `Windows 10` buscaremos `Obtener acceso a trabajo o escuela` -> `Conectar` -> `Unir este dispositivo a un dominio local de Active Directory` -> pondremos `corp.local` -> `Siguiente` -> metemos como credenciales para el equipo `WS01` (`empleado1:Passw0rd2`) como creamos anteriormente en el `DC` para vincularlo a dicho equipo y en el `WS02` (`empleado2:Passw0rd3`) -> `Aceptar` -> `Siguiente` -> `Reiniciar Ahora`.

Y ahora cuando nos vayamos a iniciar sesion veremos `CORP\empleado1` para el primer equipo y para el segundo `CORP\empleado2` por lo que habremos vinculado todo de forma correcta cada equipo a la cuenta de usuario del dominio del `DC`, ahora si iniciamos sesion, estaremos haciendolo bajo el dominio de nuestro `DC`.

Basicamente se esta autenticando con el dominio de `corp.local` con el usuario que pertenezca al dominio del `DC`.
