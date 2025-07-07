---
icon: apartment
---

# Instalación y configuración del DC

Primero tendremos que descargarnos la `ISO` de un `Windows Server` para poder montarnos nuestro `DC` que estara en el siguiente link:

URL = [Download Windows Server 2022](https://www.microsoft.com/es-es/evalcenter/download-windows-server-2022)

Una vez que nos lo hayamos descargado, tendremos que montarnos una maquina en `VMWare` con dicha `ISO` siguiendo los pasos de instalacion y llamaremos a la maquina `DC01.corp.local`, ya que en un entorno real habra muchos `Controladores de dominio` y especificando el `dominio` que tendra dicho servidor.

Estableceremos las credenciales del `administrator` con la siguiente contraseña `Passw0rd`, al iniciar sesion nos configurara todo de forma automatica las cosas basicas y ahora pasaremos a la configuracion del `DC`.

### Cambio de nombre del server

Antes de empezar con la configuracion inicial, vamos a cambiarle el nombre de equipo del `Windows Server` para que sea mas facil a la hora de identificarlo.

Vamos a buscar `Este equipo` -> Click derecho -> `Propiedades` -> `Cambiar el nombre de este equipo` -> pondremos como nombre `DC01` -> `Siguiente` -> `Reinciar Ahora` -> `Continuar`.

Y con esto ya tendriamos el nombre del equipo cambiado correctamente.

### Configuración de red

Ahora lo que vamos hacer es cambiar la direccion IP de este `Windows Server` de la siguiente forma.

Le daremos click derecho al adaptador de red -> `Abrir configuracion de red e internet` -> `Ethernet` -> `Cambiar las opciones del adaptador` -> dentro de `Ethernet0` le damos a `Propiedades` con click derecho -> `Protocolo de internet version 4 (TCP/IPv4)` le damos a `Propiedades` -> dentro de `Usar la siguiente direccion IP` pondremos `192.168.5.5` y en las opciones de `DNS` pondremos en la primera `127.0.0.1` (Ya que en algun momento nuestro servidor actuara como servidor `DNS`) -> `Aceptar` -> `Cerrar`.

Y con esto ya estaria configurada la red.

### Configurar Administrador del servidor

Vamos a darle dentro del `Administrador del servidor` a `Administrar` -> `Agregar roles y caracteristicas` -> `Siguiente` -> `Siguiente` -> `Siguiente` -> seleccionamos `Servicios de dominio de Active Directory` -> `Agregar Caracteristica` -> `Siguiente` -> `Siguiente` -> `Siguiente` -> marcamos `Reiniciar automaticamente el servidor de destino en caso necesario` y le daremos a `Instalar` -> una vez completada la instalacion le daremos a `Cerrar`.

Ahora le tendremos que configurar el `Bosque` y el `Dominio` que queremos que tenga ese `Active Directory`, le tendremos que dar al icono de la banderita -> `Promover este servidor a controlador de dominio` -> `Agregar un nuevo bosque`, le pondremos como nombre `corp.local` que es el dominio que queremos que tenga -> `Siguiente` -> tendremos que establecer una contraseña, la cual sera la misma que la del `Administrator` (`Passw0rd`) -> `Siguiente` -> `Siguiente` -> `Siguiente` -> `Siguiente` -> `Siguiente` -> `Instalar`.

Una vez echo todo esto y que se haya instalado, se nos reiniciara el servidor para que se apliquen bien todos los cambios.

Ahora cuando queramos iniciar sesion vamos autenticarnos contra el `Controlador de dominio` y no desde nuestra maquina de forma local (`CORP\Administrator`).

Con esto lo que estamos haciendo es autenticarnos en el `dominio` del servidor bajo nuestro usuario correspondiente que pertenece a dicha base de datos del servidor de dominio, teniendo asi todo conectado en un servidor de forma centralizada.
