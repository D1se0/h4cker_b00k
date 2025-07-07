---
icon: laptop-arrow-down
---

# Enumeración remota de SAM

Con esta tecnica lo que podemos hacer es enumerar los usuarios que esten dentro del grupo `administradores` dentro del dominio, para enforcarnos concretamente en ese equipo e intentar ganar acceso a el, en vez de tener que ir uno por uno probando cual tiene el grupo `administrador` o no, por lo que con este tipo de tecnicas sabes a que equipo ir mas concretamente.

Si nos encontramos con un `Windows 7` o un `Windows Server 2016` para abajo, podriamos enumerar el `SAM` de forma remota con un usuario cualquiera, pero de esas versiones para arriba, ya no es posible, si estuvieramos de esas versiones para abajo seria con el siguiente comando:

```powershell
Get-NetLocalGroup -ComputerName WS02
```

Pero si nosotros obtenemos un usuario de dominio con privilegios de `administrador` si podremos enumerarlo de forma remota, por lo que vamos a hacer que este usuario tenga privilegios de administrador de forma temporal para que se vea:

Nos iremos a nuestro `DC` en el `Servidor del administrador` -> `Herramientas` -> `Usuarios y equipos de Active Directory` -> `Users` -> click derecho `empleado1` -> `Propiedades` -> `Miembro de` -> `Añadir` -> escribimos `Admins de do` y lo va a detectar solo, seleccionamos el grupo de `Admins de dominio` -> `Aceptar` -> `Aplicar` -> `Acpetar`.

Y con esto ya lo tendremos en el grupo para realizar lo anterior.

Tendremos que reiniciar el equipo para que se apliquen los cambios, volvemos a ejecutar el script de `PowerView` y hacer lo siguiente:

```powershell
. .\new_powerview.ps1
```

```powershell
Get-NetLocalGroup -ComputerName WS02
```

Info:

```
ComputerName GroupName                                     Comment
------------ ---------                                     -------
WS02         Administradores                               Los administradores tienen acceso completo y sin restricc...
WS02         Administradores de Hyper-V                    Los miembros de este grupo tienen acceso completo y sin r...
WS02         Duplicadores                                  Pueden replicar archivos en un dominio
WS02         IIS_IUSRS                                     Grupo integrado usado por Internet Information Services.
WS02         Invitados                                     De forma predeterminada, los invitados tienen el mismo ac...
WS02         Lectores del registro de eventos              Los miembros de este grupo pueden leer registros de event...
WS02         Operadores criptográficos                     Los miembros tienen autorización para realizar operacione...
WS02         Operadores de asistencia de control de acceso Los miembros de este grupo pueden consultar de forma remo...
WS02         Operadores de configuración de red            Los miembros en este equipo pueden tener algunos privileg...
WS02         Operadores de copia de seguridad              Los operadores de copia de seguridad pueden invalidar res...
WS02         Propietarios del dispositivo                  Los miembros de este grupo pueden cambiar la configuració...
WS02         System Managed Accounts Group                 Los miembros de este grupo los administra el sistema.
WS02         Usuarios                                      Los usuarios no pueden hacer cambios accidentales o inten...
WS02         Usuarios avanzados                            Los usuarios avanzados se incluyen para la compatibilidad...
WS02         Usuarios COM distribuidos                     Los miembros pueden iniciar, activar y usar objetos de CO...
WS02         Usuarios de administración remota             Los miembros de este grupo pueden acceder a los recursos ...
WS02         Usuarios de escritorio remoto                 A los miembros de este grupo se les concede el derecho de...
WS02         Usuarios del monitor de sistema               Los miembros de este grupo tienen acceso a los datos del ...
WS02         Usuarios del registro de rendimiento          Los miembros de este grupo pueden programar contadores de...
```

Ahora veremos que si nos funciona siendo administradores del dominio, por lo que hemos obtenido estos datos de manera remota sobre el equipo `WS02`.

En este caso al obtener esta informacion estamos utilizando el protocolo `SAMR` que estaria distribuido por `DCE/RPC` (`Remote Procedure Call`), pero cuando nosotros consultemos la base de datos `NTDS` del `DC` vamos a utilizar el protcolo `LDAP` con el que podemos interactuar con esa base de datos.

Una vez explicado y visto todo esto, vamos a quitarle los privilegios al `empleado1` eliminando el grupo `administrador de dominio`.

### Realizar listado de SAM remota de forma manual sin PowerView

Ahora si nosotros queremos realizar esto anterior pero sin `PowerView` podremos hacerlo de la siguiente forma:

```powershell
Invoke-Command -ScriptBlock { Get-LocalGroupMember -Group Administradores } -ComputerName WS01
```

Pero nos dara un error ya que no tendremos privilegios para listarlo.

### Identificar que equipos son los administradores en el dominio

Para saber que usuarios tenemos registrados por obtener mas informacion, sera de la siguiente forma:

```powershell
Get-NetLoggedon
```

Info:

```
UserName     : empleado1
LogonDomain  : CORP
AuthDomains  :
LogonServer  : DC01
ComputerName : localhost

UserName     : empleado1
LogonDomain  : CORP
AuthDomains  :
LogonServer  : DC01
ComputerName : localhost

UserName     : WS01$
LogonDomain  : CORP
AuthDomains  :
LogonServer  :
ComputerName : localhost

UserName     : WS01$
LogonDomain  : CORP
AuthDomains  :
LogonServer  :
ComputerName : localhost

UserName     : WS01$
LogonDomain  : CORP
AuthDomains  :
LogonServer  :
ComputerName : localhost

UserName     : WS01$
LogonDomain  : CORP
AuthDomains  :
LogonServer  :
ComputerName : localhost

UserName     : WS01$
LogonDomain  : CORP
AuthDomains  :
LogonServer  :
ComputerName : localhost
```

Esto de forma remota no lo podremos hacer ya que requiere privilegios de administrador, pero lo que si podremos obtener son las sesiones de las conexiones que hay a mi maquina a la `WS01`:

```powershell
Get-NetSession
```

Info:

```
CName        : \\[::1]
UserName     : empleado1
Time         : 0
IdleTime     : 0
ComputerName : localhost
```

Pero imaginemos que un `Administrador` se conecta a esta maquina para gestionar algunas cosas, lo haremos de la siguiente forma.

Nos iremos a nuestro `DC` -> abriremos una carpeta normal y en la barra de busqueda pondremos `\\WS01\C$`.

El `C$` es el recurso compartido de un equipo tipico en el que se encuentra todo el sistema operativo entero.

<figure><img src="../../../.gitbook/assets/image (226).png" alt=""><figcaption></figcaption></figure>

Ahora si nos vamos al equipo `WS01` y ejecutamos el mismo comando de antes:

```powershell
Get-NetSession
```

Info:

```
CName        : \\192.168.5.5
UserName     : Administrator
Time         : 57
IdleTime     : 5
ComputerName : localhost

CName        : \\[::1]
UserName     : empleado1
Time         : 0
IdleTime     : 0
ComputerName : localhost
```

Por lo que vemos estamos observando que un usuario `Administrador` se ha conectado a nuestra maquina y sabemos su `IP` por lo que si comprometemos dicha maquina obtendremos privilegios de administrador de forma inmediata, por lo que nos interesa centarnos en dicha `IP`, es una forma de saber por donde atacar o donde ir en estos casos.

Y aunque al internat conectarse falle u otro equipo de la red se intente conectar el cual no tendra privilegios a no ser que sea administrador falle, eso tambien se quedara registrado en las `sesiones`.
