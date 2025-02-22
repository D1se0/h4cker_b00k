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

# Impacket y Rpcclient

Imaginemos que hemos obtenido unas credenciales de algun usuario de dominio de `Windows` por ejemplo el de `empleado1` y sabemos que su contraseña es `Passw0rd2`, pero no podemos acceder a la maquina en modo escritorio viendo el `Windows`, pues podremos enumerar o hacer cualquier otra cosa de forma remota desde `kali` de la siguiente forma:

Pero antes vamos a configurar nuestra red en `kali` para que los servidores `DNS` apuntes al `DC` de la siguiente forma:

Buscamos `Settings` -> `Advanced Network Configuration` -> `IPv4 Settings` -> seleccionamos `Automatic (DHCP) addresses only` -> en `DNS Servers` ponemos la IP del `DC` que en mi caso sera `192.168.5.5` -> `Save`.

Y ya lo tendremos listo, ahora si lo probamos de la siguiente forma:

```shell
ping WS01
```

Esto os deberia de dar `ping`.

Para poder identificar que IP tiene nuestro `Controlador de dominio` si estuvieramos sin ningun tipo de informacion, seria de la siguiente forma:

```shell
sudo nmap -sS -n 192.168.5.0-7 
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-09 04:00 EST
Nmap scan report for 192.168.5.1
Host is up (0.00092s latency).
Not shown: 997 filtered tcp ports (no-response)
PORT    STATE SERVICE
135/tcp open  msrpc
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds
MAC Address: 00:50:56:C0:00:08 (VMware)

Nmap scan report for 192.168.5.2
Host is up (0.00027s latency).
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE
53/tcp open  domain
MAC Address: 00:50:56:F5:72:77 (VMware)

Nmap scan report for 192.168.5.5
Host is up (0.00048s latency).
Not shown: 988 filtered tcp ports (no-response)
PORT     STATE SERVICE
53/tcp   open  domain
88/tcp   open  kerberos-sec
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
389/tcp  open  ldap
445/tcp  open  microsoft-ds
464/tcp  open  kpasswd5
593/tcp  open  http-rpc-epmap
636/tcp  open  ldapssl
3268/tcp open  globalcatLDAP
3269/tcp open  globalcatLDAPssl
5357/tcp open  wsdapi
MAC Address: 00:0C:29:B0:CB:01 (VMware)

Nmap done: 8 IP addresses (3 hosts up) scanned in 7.62 seconds
```

Y por lo que vemos podemos identificar que la `192.168.5.5` es claramente el `DC` por los puertos que tiene abiertos ya que son super comunes en servidores `DC`.

### Herramienta Rpcclient

Para poder enumerar la `SAM` de forma remota desde `kali` podremos hacerlo de la siguiente forma:

```shell
rpcclient -U "corp\empleado1%Passw0rd2" WS01
```

Info:

```
rpcclient $>
```

Esta herramienta necesita unas credenciales y como las obtuvimos anteriormente, pues las utilizaremos con esta herramienta, como veremos funciona y estaremos dentro de un interpreter conectados a dicho equipo por terminal.

Por ejemplo si queremos enumerar los privilegios que hay en el sistema:

```shell
enumprivs
```

Info:

```
found 35 privileges

SeCreateTokenPrivilege          0:2 (0x0:0x2)
SeAssignPrimaryTokenPrivilege           0:3 (0x0:0x3)
SeLockMemoryPrivilege           0:4 (0x0:0x4)
SeIncreaseQuotaPrivilege                0:5 (0x0:0x5)
SeMachineAccountPrivilege               0:6 (0x0:0x6)
SeTcbPrivilege          0:7 (0x0:0x7)
SeSecurityPrivilege             0:8 (0x0:0x8)
SeTakeOwnershipPrivilege                0:9 (0x0:0x9)
SeLoadDriverPrivilege           0:10 (0x0:0xa)
SeSystemProfilePrivilege                0:11 (0x0:0xb)
SeSystemtimePrivilege           0:12 (0x0:0xc)
SeProfileSingleProcessPrivilege                 0:13 (0x0:0xd)
SeIncreaseBasePriorityPrivilege                 0:14 (0x0:0xe)
SeCreatePagefilePrivilege               0:15 (0x0:0xf)
SeCreatePermanentPrivilege              0:16 (0x0:0x10)
SeBackupPrivilege               0:17 (0x0:0x11)
SeRestorePrivilege              0:18 (0x0:0x12)
SeShutdownPrivilege             0:19 (0x0:0x13)
SeDebugPrivilege                0:20 (0x0:0x14)
SeAuditPrivilege                0:21 (0x0:0x15)
SeSystemEnvironmentPrivilege            0:22 (0x0:0x16)
SeChangeNotifyPrivilege                 0:23 (0x0:0x17)
SeRemoteShutdownPrivilege               0:24 (0x0:0x18)
SeUndockPrivilege               0:25 (0x0:0x19)
SeSyncAgentPrivilege            0:26 (0x0:0x1a)
SeEnableDelegationPrivilege             0:27 (0x0:0x1b)
SeManageVolumePrivilege                 0:28 (0x0:0x1c)
SeImpersonatePrivilege          0:29 (0x0:0x1d)
SeCreateGlobalPrivilege                 0:30 (0x0:0x1e)
SeTrustedCredManAccessPrivilege                 0:31 (0x0:0x1f)
SeRelabelPrivilege              0:32 (0x0:0x20)
SeIncreaseWorkingSetPrivilege           0:33 (0x0:0x21)
SeTimeZonePrivilege             0:34 (0x0:0x22)
SeCreateSymbolicLinkPrivilege           0:35 (0x0:0x23)
SeDelegateSessionUserImpersonatePrivilege               0:36 (0x0:0x24)
```

Pero si nosotros queremos enumerar los usuarios de forma remota, tendremos que tener privilegios de administrador y si no los tenemos veremos lo siguiente:

```shell
enumdomusers
```

Info:

```
result was NT_STATUS_CONNECTION_DISCONNECTED
```

Esto significa que nos tenemos los permisos suficientes como para realizar esa accion.

Si por ejemplo nos conectaramos como el `administrador` con un usuario que si tiene privilegios, si podremos hacerlo, por lo que vamos a realizarlo de la siguiente forma para que se vea bien.

```shell
rpcclient -U "corp\Administrator%Passw0rd" WS01
```

```shell
enumdomusers
```

Info:

```
user:[Administrador] rid:[0x1f4]
user:[DefaultAccount] rid:[0x1f7]
user:[Invitado] rid:[0x1f5]
user:[santiago] rid:[0x3e9]
user:[WDAGUtilityAccount] rid:[0x1f8]
```

O si queremos enumerar los grupos:

```shell
enumalsgroups builtin
```

Info:

```
group:[Administradores] rid:[0x220]
group:[Administradores de Hyper-V] rid:[0x242]
group:[Duplicadores] rid:[0x228]
group:[IIS_IUSRS] rid:[0x238]
group:[Invitados] rid:[0x222]
group:[Lectores del registro de eventos] rid:[0x23d]
group:[Operadores criptográficos] rid:[0x239]
group:[Operadores de asistencia de control de acceso] rid:[0x243]
group:[Operadores de configuración de red] rid:[0x22c]
group:[Operadores de copia de seguridad] rid:[0x227]
group:[Propietarios del dispositivo] rid:[0x247]
group:[System Managed Accounts Group] rid:[0x245]
group:[Usuarios] rid:[0x221]
group:[Usuarios avanzados] rid:[0x223]
group:[Usuarios COM distribuidos] rid:[0x232]
group:[Usuarios de administración remota] rid:[0x244]
group:[Usuarios de escritorio remoto] rid:[0x22b]
group:[Usuarios del monitor de sistema] rid:[0x22e]
group:[Usuarios del registro de rendimiento] rid:[0x22f]
```

Si queremos ver que usuario pertenece a que grupo, podremos hacerlo asi:

```shell
queryaliasmem builtin <RID>
```

En mi caso utilizare el identificado `RID` = `0x220` que es el de `Administrador`

```shell
queryaliasmem builtin 0x220
```

Info:

```
		sid:[S-1-5-21-1345059704-770646112-4146140408-500]
        sid:[S-1-5-21-1345059704-770646112-4146140408-1001]
        sid:[S-1-5-21-3352250647-938130414-2449934813-512]
```

Pero nos lo muestra con el `SID` (Security ID) que es un sistema de seguridad que esta dentro de los dispositivos `Windows`.

Por lo que tendremos que utilizar otra funcion para poderlo ver en texto plano:

```shell
lookupsids <SID>
```

En mi caso escogere el primero `S-1-5-21-1345059704-770646112-4146140408-500`:

```shell
lookupsids S-1-5-21-1345059704-770646112-4146140408-500
```

Info:

```
S-1-5-21-1345059704-770646112-4146140408-500 WS01\Administrador (1)
```

Por lo que vemos pertenece a usuario `WS01\Administardor` local del equipo `WS01`.

Pero la desventaja de todo esto es que se requiere privilegios de `administrador` para realizar este tipo de cosas.

### Herramienta Impacket

Esta herramienta es mucho mas estable y mejor, mucho mas uitilizada que la de `rpcclient` ya que tiene muchas mas funcionalidades.

Encontraremos la informacion de la herramienta en el siguiente link:

URL = [Impacket GitHub](https://github.com/fortra/impacket)

En lo ejemplos del repositorio encontraremos varios scripts los cuales hacer diversas cosas, esta herramienta ya viene implementada en `kali` por lo que no tendremos que descargar nada.

Si por ejemplo queremos `dumpear` la informacion del `SAM` mediante el protocolo `SAMR`, podremos hacerlo con el siguiente comando de `impacket`:

```shell
impacket-samrdump corp/Administrator:Passw0rd@WS01
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Retrieving endpoint list from WS01
Found domain(s):
 . WS01
 . Builtin
[*] Looking up users in domain WS01
Found user: Administrador, uid = 500
Found user: DefaultAccount, uid = 503
Found user: Invitado, uid = 501
Found user: santiago, uid = 1001
Found user: WDAGUtilityAccount, uid = 504
Administrador (500)/FullName: 
Administrador (500)/AdminComment: Cuenta integrada para la administración del equipo o dominio
Administrador (500)/UserComment: 
Administrador (500)/PrimaryGroupId: 513
Administrador (500)/BadPasswordCount: 0
Administrador (500)/LogonCount: 0
Administrador (500)/PasswordLastSet: <never>
Administrador (500)/PasswordDoesNotExpire: True
Administrador (500)/AccountIsDisabled: True
Administrador (500)/ScriptPath: 
DefaultAccount (503)/FullName: 
DefaultAccount (503)/AdminComment: Cuenta de usuario administrada por el sistema.
DefaultAccount (503)/UserComment: 
DefaultAccount (503)/PrimaryGroupId: 513
DefaultAccount (503)/BadPasswordCount: 0
DefaultAccount (503)/LogonCount: 0
DefaultAccount (503)/PasswordLastSet: <never>
DefaultAccount (503)/PasswordDoesNotExpire: True
DefaultAccount (503)/AccountIsDisabled: True
DefaultAccount (503)/ScriptPath: 
Invitado (501)/FullName: 
Invitado (501)/AdminComment: Cuenta integrada para el acceso como invitado al equipo o dominio
Invitado (501)/UserComment: 
Invitado (501)/PrimaryGroupId: 513
Invitado (501)/BadPasswordCount: 0
Invitado (501)/LogonCount: 0
Invitado (501)/PasswordLastSet: <never>
Invitado (501)/PasswordDoesNotExpire: True
Invitado (501)/AccountIsDisabled: True
Invitado (501)/ScriptPath: 
santiago (1001)/FullName: 
santiago (1001)/AdminComment: 
santiago (1001)/UserComment: 
santiago (1001)/PrimaryGroupId: 513
santiago (1001)/BadPasswordCount: 0
santiago (1001)/LogonCount: 5
santiago (1001)/PasswordLastSet: 2025-01-05 12:28:22.004346
santiago (1001)/PasswordDoesNotExpire: True
santiago (1001)/AccountIsDisabled: False
santiago (1001)/ScriptPath: 
WDAGUtilityAccount (504)/FullName: 
WDAGUtilityAccount (504)/AdminComment: Una cuenta de usuario que el sistema administra y usa para escenarios de Protección de aplicaciones de Windows Defender.
WDAGUtilityAccount (504)/UserComment: 
WDAGUtilityAccount (504)/PrimaryGroupId: 513
WDAGUtilityAccount (504)/BadPasswordCount: 0
WDAGUtilityAccount (504)/LogonCount: 0
WDAGUtilityAccount (504)/PasswordLastSet: 2025-01-05 12:21:33.705144
WDAGUtilityAccount (504)/PasswordDoesNotExpire: False
WDAGUtilityAccount (504)/AccountIsDisabled: True
WDAGUtilityAccount (504)/ScriptPath: 
[*] Received 5 entries.
```

Utilizamos el del `administrador` ya que se requieren privilegios para volcar la informacion del `SAM`.

Lo que podemos hacer tambien es con este comando capturar sesiones en las que se conecte un usuario a un recurso compartido, pero si lo hacemos con un usuario normal...

```shell
impacket-netview corp/empleado1:'Passw0rd2' -target WS01
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Importing targets
[*] Got 1 machines
```

Esto lo que va hacer es estar escuchando sesiones de red en las cuales cuando detecte que se conecto un usuario o se intento conectar un usuario a dicho equipo, nos aparecera por aqui la informacion de dicho usuario.

Por ejemplo si ahora nosotros vamos a neustro `DC` y abrimos una carpeta, en la barra de busqueda ponemos `\\WS01\C$`

O si mejor lo hacemos desde `PowerShell`:

```powershell
dir \\WS01\c$
```

Y ahora nos vamos a donde tenemos la escucha, veremos lo siguiente:

No veremos absolutamente nada, ya que tambien requiere privilegios de `administrador`, si nosotros cerramos la escucha y la ejecutamos con unas credenciales de `administrador` y hacemos todo el proceso anterior de la misma forma:

```shell
impacket-netview corp/Administrator:'Passw0rd' -target WS01
```

En la maquina `DC` pondremos en un `PwerShell`:

```powershell
dir \\WS01\c$
```

Y si nos volvemos a donde tenemos la escucha veremos lo siguiente:

```
WS01: user Administrator logged from host 192.168.5.5 - active: 160, idle: 5

WS01: user CORP\empleado1 logged in LOCALLY
WS01: user CORP\WS01$ logged in LOCALLY
```

Vemos que la capturo perfectamente.
