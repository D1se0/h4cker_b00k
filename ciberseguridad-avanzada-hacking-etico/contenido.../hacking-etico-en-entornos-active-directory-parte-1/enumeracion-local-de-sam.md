---
icon: street-view
---

# Enumeración local de SAM

Este tipo de tecnicas tambien se le llama `SAM Enumeration`.

Pongamos como dijimos antes que nos han prestado este equipo llamado `empleado1` que es un usuario de dominio, pero sin privilegios de administrador, por lo que mediante este equipo vamos a recopilar toda la informacion que podamos.

Abriremos una `PowerShell` y empezaremos el reconocimiento.

### Ver que usuario somos

```powershell
$env:UserName
```

Info:

```
empleado1
```

### Ver que dominio tiene dicho equipo

```powershell
$env:UserDomain
```

Info:

```
CORP
```

### Ver el nombre del equipo

```powershell
$env:ComputerName
```

Info:

```
WS01
```

### Enumerar grupos locales

Con esta informacion podremos saber como escalar privilegios o que grupos nos interesan mas para poder tener un vector de entrada mas facil, etc...

Vamos a cargar el script de nuevo para utilizarlo ahora.

```powershell
. .\new_powerview.ps1
```

```powershell
Get-NetLocalGroup
```

Info:

```
ComputerName GroupName                                     Comment
------------ ---------                                     -------
WS01         Administradores                               Los administradores tienen acceso completo y sin restricc...
WS01         Administradores de Hyper-V                    Los miembros de este grupo tienen acceso completo y sin r...
WS01         Duplicadores                                  Pueden replicar archivos en un dominio
WS01         IIS_IUSRS                                     Grupo integrado usado por Internet Information Services.
WS01         Invitados                                     De forma predeterminada, los invitados tienen el mismo ac...
WS01         Lectores del registro de eventos              Los miembros de este grupo pueden leer registros de event...
WS01         Operadores criptográficos                     Los miembros tienen autorización para realizar operacione...
WS01         Operadores de asistencia de control de acceso Los miembros de este grupo pueden consultar de forma remo...
WS01         Operadores de configuración de red            Los miembros en este equipo pueden tener algunos privileg...
WS01         Operadores de copia de seguridad              Los operadores de copia de seguridad pueden invalidar res...
WS01         Propietarios del dispositivo                  Los miembros de este grupo pueden cambiar la configuració...
WS01         System Managed Accounts Group                 Los miembros de este grupo los administra el sistema.
WS01         Usuarios                                      Los usuarios no pueden hacer cambios accidentales o inten...
WS01         Usuarios avanzados                            Los usuarios avanzados se incluyen para la compatibilidad...
WS01         Usuarios COM distribuidos                     Los miembros pueden iniciar, activar y usar objetos de CO...
WS01         Usuarios de administración remota             Los miembros de este grupo pueden acceder a los recursos ...
WS01         Usuarios de escritorio remoto                 A los miembros de este grupo se les concede el derecho de...
WS01         Usuarios del monitor de sistema               Los miembros de este grupo tienen acceso a los datos del ...
WS01         Usuarios del registro de rendimiento          Los miembros de este grupo pueden programar contadores de...
```

Con esto simplemente vemos los grupos que hay actualmente en el dominio, pero si queremos saber a que grupos tenemos nosotros privilegios, lo podremos hacer de la siguiente forma:

### Ver los grupos en los que esta nuestro usuario

```powershell
Get-NetGroup -UserName "empleado1" | select name
```

Info:

```
name
----
Domain Users
```

Todo esto que estamos utilizando son funciones de `PowerView`, en este caso vemos que este usuario desgraciadamente no esta en ningun grupo mas interesante en el que podamos escalar privilegios, ya que el grupo en el que esta es el que viene por defecto y esta muy limitado, pero lo que si podemos hacer es ver los usuarios que estan dentro del grupo `administrador`.

### Ver los usuarios que estan en los grupos administradores

```powershell
Get-NetLocalGroupMember -GroupName Administradores | Select-Object MemberName, IsGroup, IsDomain
```

Info:

```
MemberName         IsGroup IsDomain
----------         ------- --------
WS01\Administrador   False    False
WS01\santiago        False    False
CORP\Domain Admins    True     True
```

Por lo que vemos el usuario local tiene privilegios de `administrador`, vemos tambien que hay una cuenta `Administrador` a demas del usuario administrador del dominio, pero si nosotros consiguieramos sacar la contraseña al `Administrador` local del equipo, puede ser que este este en mas equipos conectados a nivel local y con suerte que tengan la misma contraseña, por lo que podriamos `pivotar` hasta llegar al `DC` y hacernos con el control total, pero esto sera mas adelante.

### Hacerlo de forma manual sin PowerView enumeración

En tal caso de que el `script` `PowerView` estuviera siendo detectado por el `Windows Defender` o por otro tipo de herramienta de seguridad, podremos enumerar de forma manual de la siguiente forma:

```powershell
Get-LocalGroup | Select Name, Objectclass, Principalsource, sid
```

Info:

```
Name                                          ObjectClass PrincipalSource SID
----                                          ----------- --------------- ---
Administradores                               Grupo                 Local S-1-5-32-544
Administradores de Hyper-V                    Grupo                 Local S-1-5-32-578
Duplicadores                                  Grupo                 Local S-1-5-32-552
IIS_IUSRS                                     Grupo                 Local S-1-5-32-568
Invitados                                     Grupo                 Local S-1-5-32-546
Lectores del registro de eventos              Grupo                 Local S-1-5-32-573
Operadores criptográficos                     Grupo                 Local S-1-5-32-569
Operadores de asistencia de control de acceso Grupo                 Local S-1-5-32-579
Operadores de configuración de red            Grupo                 Local S-1-5-32-556
Operadores de copia de seguridad              Grupo                 Local S-1-5-32-551
Propietarios del dispositivo                  Grupo                 Local S-1-5-32-583
System Managed Accounts Group                 Grupo                 Local S-1-5-32-581
Usuarios                                      Grupo                 Local S-1-5-32-545
Usuarios avanzados                            Grupo                 Local S-1-5-32-547
Usuarios COM distribuidos                     Grupo                 Local S-1-5-32-562
Usuarios de administración remota             Grupo                 Local S-1-5-32-580
Usuarios de escritorio remoto                 Grupo                 Local S-1-5-32-555
Usuarios del monitor de sistema               Grupo                 Local S-1-5-32-558
Usuarios del registro de rendimiento          Grupo                 Local S-1-5-32-559
```

Este comando hace la misma funcion que este `Get-NetGroup -UserName "empleado1" | select name`.

Si queremos ver los usuarios que pertenecen al grupo `administrador` como lo haciamos con este comando `Get-NetLocalGroupMember -GroupName Administradores | Select-Object MemberName, IsGroup, IsDomain`, de forma manual se podra hacer de la siguiente forma:

```powershell
Get-LocalGroupMember -Group Administradores
```

Info:

```
ObjectClass Name               PrincipalSource
----------- ----               ---------------
Grupo       CORP\Domain Admins ActiveDirectory
Usuario     WS02\Administrador Local
Usuario     WS02\santiago2     Local
```
