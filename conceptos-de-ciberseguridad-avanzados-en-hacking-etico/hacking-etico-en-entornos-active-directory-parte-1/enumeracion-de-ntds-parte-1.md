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

# Enumeración de NTDS - Parte 1

Si queremos enumerar las politicas que esten establecidas en el equipo `WS01` el cual no tiene privilegios de administrador, podremos hacerlo, ya que cargamos el `PowerView` y seria de la sigueinte forma:

```powershell
Get-DomainPolicy
```

Info:

```
Unicode        : @{Unicode=yes}
SystemAccess   : @{MinimumPasswordAge=1; MaximumPasswordAge=42; MinimumPasswordLength=7; PasswordComplexity=1;
                 PasswordHistorySize=24; LockoutBadCount=0; RequireLogonToChangePassword=0;
                 ForceLogoffWhenHourExpire=0; ClearTextPassword=0; LSAAnonymousNameLookup=0}
KerberosPolicy : @{MaxTicketAge=10; MaxRenewAge=7; MaxServiceAge=600; MaxClockSkew=5; TicketValidateClient=1}
RegistryValues : @{MACHINE\System\CurrentControlSet\Control\Lsa\NoLMHash=System.Object[]}
Version        : @{signature="$CHICAGO$"; Revision=1}
Path           : \\corp.local\sysvol\corp.local\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\MACHINE\Microsoft\Windo
                 ws NT\SecEdit\GptTmpl.inf
GPOName        : {31B2F340-016D-11D2-945F-00C04FB984F9}
GPODisplayName : Default Domain Policy
```

Podremos filtrar para obtener el `SystemAccess` de la siguiente forma:

```powershell
(Get-DomainPolicy)."SystemAccess"
```

Info:

```
MinimumPasswordAge           : 1
MaximumPasswordAge           : 42
MinimumPasswordLength        : 7
PasswordComplexity           : 1
PasswordHistorySize          : 24
LockoutBadCount              : 0
RequireLogonToChangePassword : 0
ForceLogoffWhenHourExpire    : 0
ClearTextPassword            : 0
LSAAnonymousNameLookup       : 0
```

### Información del DC

Si queremos saber la informacion del `DC` tanto su `IP` como demas cosas y no lo queremos hacer con `PowerView`, lo podremos hacer de forma manual en el equipo `WS02` en el que cargamos el `.dll` anteriormente, si se ha reiniciado la maquina o algo por el estilo habra que volver a cargarlo:

```powershell
Import-Module .\Microsoft.ActiveDirectory.Management.dll
Get-ADDomainController
```

Info:

```
Domain             : corp.local
Forest             : corp.local
Name               : DC01
Site               : Default-First-Site-Name
IPv4Address        : 192.168.5.5
IPv6Address        :
PropertyNames      : {ComputerObjectDN, DefaultPartition, Domain, Enabled...}
AddedProperties    : {}
RemovedProperties  : {}
ModifiedProperties : {}
PropertyCount      : 24
```

Y con `PowerView` se podria hacer de la siguiente forma:

```powershell
Get-NetDomainController
```

Info:

```
Forest                     : corp.local
CurrentTime                : 10/01/2025 8:36:46
HighestCommittedUsn        : 45102
OSVersion                  : Windows Server 2022 Standard
Roles                      : {SchemaRole, NamingRole, PdcRole, RidRole...}
Domain                     : corp.local
IPAddress                  : 192.168.5.5
SiteName                   : Default-First-Site-Name
SyncFromAllServersCallback :
InboundConnections         : {}
OutboundConnections        : {}
Name                       : DC01.corp.local
Partitions                 : {DC=corp,DC=local, CN=Configuration,DC=corp,DC=local,
                             CN=Schema,CN=Configuration,DC=corp,DC=local, DC=DomainDnsZones,DC=corp,DC=local...}
```

Al utilizar `PowerView` genera trafico de red en el cual puede ser detectado por herramientas de seguridad, pero son alertas que nadie va a investigar ya que la alerta suele ser de `Bad Trafic` y es por que `PowerView` a veces los paquetes de red van de forma erronea y se genera trafico malo, pero nadie lo va a investigar asi que se puede utilizar las veces que se quiera, pero es para tenerlo en cuenta.

### Enumerar usuarios del dominio

Con un usuario normal sin privilegios podremos ser capaces de sacar todos los usuarios del dominio que existen en dicho dominio, primero empezaremos por el modulo de `AD`:

Desde `empleado2` en la consola haremos lo siguiente:

```powershell
Get-ADUser -Filter *
```

Info:

```
GivenName          :
Surname            :
UserPrincipalName  :
Enabled            : True
SamAccountName     : Administrator
SID                : S-1-5-21-3352250647-938130414-2449934813-500
DistinguishedName  : CN=Administrator,CN=Users,DC=corp,DC=local
Name               : Administrator
ObjectClass        : user
ObjectGuid         : 93c0e554-db8e-41c7-8129-c7e183c05a48
PropertyNames      : {DistinguishedName, Enabled, GivenName, Name...}
AddedProperties    : {}
RemovedProperties  : {}
ModifiedProperties : {}
PropertyCount      : 10

GivenName          :
Surname            :
UserPrincipalName  :
Enabled            : False
SamAccountName     : Guest
SID                : S-1-5-21-3352250647-938130414-2449934813-501
DistinguishedName  : CN=Guest,CN=Users,DC=corp,DC=local
Name               : Guest
ObjectClass        : user
ObjectGuid         : 76485e57-831f-4a9a-b5bf-554a50e4e5b6
PropertyNames      : {DistinguishedName, Enabled, GivenName, Name...}
AddedProperties    : {}
RemovedProperties  : {}
ModifiedProperties : {}
PropertyCount      : 10

GivenName          :
Surname            :
UserPrincipalName  :
Enabled            : False
SamAccountName     : krbtgt
SID                : S-1-5-21-3352250647-938130414-2449934813-502
DistinguishedName  : CN=krbtgt,CN=Users,DC=corp,DC=local
Name               : krbtgt
ObjectClass        : user
ObjectGuid         : 3e5f2afb-8433-4a2b-ad2b-e1f082a1352c
PropertyNames      : {DistinguishedName, Enabled, GivenName, Name...}
AddedProperties    : {}
RemovedProperties  : {}
ModifiedProperties : {}
PropertyCount      : 10

GivenName          : empleado1
Surname            :
UserPrincipalName  :
Enabled            : True
SamAccountName     : empleado1
SID                : S-1-5-21-3352250647-938130414-2449934813-1104
DistinguishedName  : CN=empleado1,CN=Users,DC=corp,DC=local
Name               : empleado1
ObjectClass        : user
ObjectGuid         : 438f71e8-3e05-4f21-bba7-700dd9a044e1
PropertyNames      : {DistinguishedName, Enabled, GivenName, Name...}
AddedProperties    : {}
RemovedProperties  : {}
ModifiedProperties : {}
PropertyCount      : 10

GivenName          : empleado2
Surname            :
UserPrincipalName  :
Enabled            : True
SamAccountName     : empleado2
SID                : S-1-5-21-3352250647-938130414-2449934813-1105
DistinguishedName  : CN=empleado2,CN=Users,DC=corp,DC=local
Name               : empleado2
ObjectClass        : user
ObjectGuid         : 5c5b97bc-c7a3-4d27-8291-6b9a4a77e511
PropertyNames      : {DistinguishedName, Enabled, GivenName, Name...}
AddedProperties    : {}
RemovedProperties  : {}
ModifiedProperties : {}
PropertyCount      : 10
```

Estamos viendo que nos aparece practicamente casi toda la informacion de cada usuario hasta el `SamAccountName` que es importante el id del nombre de como se tiene que logear en el dominio, etc...

Pero si lo queremos filtrar mas, para que no aparezca tanta info, podremos hacerlo de la siguiente forma:

```powershell
Get-ADUser -Filter * | select Name,ObjectClass,ObjectGuid
```

Info:

```
Name          ObjectClass ObjectGuid
----          ----------- ----------
Administrator user        93c0e554-db8e-41c7-8129-c7e183c05a48
Guest         user        76485e57-831f-4a9a-b5bf-554a50e4e5b6
krbtgt        user        3e5f2afb-8433-4a2b-ad2b-e1f082a1352c
empleado1     user        438f71e8-3e05-4f21-bba7-700dd9a044e1
empleado2     user        5c5b97bc-c7a3-4d27-8291-6b9a4a77e511
```

Ahora si queremos hacerlo con `PowerView` podremos hacerlo asi:

```powershell
Get-NetUser
```

Info:

```
logoncount             : 16
badpasswordtime        : 01/01/1601 1:00:00
description            : Built-in account for administering the computer/domain
distinguishedname      : CN=Administrator,CN=Users,DC=corp,DC=local
objectclass            : {top, person, organizationalPerson, user}
lastlogontimestamp     : 05/01/2025 12:11:57
name                   : Administrator
objectsid              : S-1-5-21-3352250647-938130414-2449934813-500
samaccountname         : Administrator
logonhours             : {255, 255, 255, 255...}
admincount             : 1
codepage               : 0
samaccounttype         : USER_OBJECT
accountexpires         : 01/01/1601 1:00:00
countrycode            : 0
whenchanged            : 05/01/2025 11:39:16
instancetype           : 4
objectguid             : 93c0e554-db8e-41c7-8129-c7e183c05a48
lastlogon              : 10/01/2025 9:24:38
lastlogoff             : 01/01/1601 1:00:00
objectcategory         : CN=Person,CN=Schema,CN=Configuration,DC=corp,DC=local
dscorepropagationdata  : {05/01/2025 11:39:16, 05/01/2025 11:39:16, 05/01/2025 11:08:50, 01/01/1601 18:12:16}
memberof               : {CN=Group Policy Creator Owners,CN=Users,DC=corp,DC=local, CN=Domain
                         Admins,CN=Users,DC=corp,DC=local, CN=Enterprise Admins,CN=Users,DC=corp,DC=local, CN=Schema
                         Admins,CN=Users,DC=corp,DC=local...}
whencreated            : 05/01/2025 11:08:00
iscriticalsystemobject : True
badpwdcount            : 0
cn                     : Administrator
useraccountcontrol     : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
usncreated             : 8196
primarygroupid         : 513
pwdlastset             : 05/01/2025 11:27:27
usnchanged             : 16407

pwdlastset             : 01/01/1601 1:00:00
logoncount             : 0
badpasswordtime        : 01/01/1601 1:00:00
description            : Built-in account for guest access to the computer/domain
distinguishedname      : CN=Guest,CN=Users,DC=corp,DC=local
objectclass            : {top, person, organizationalPerson, user}
name                   : Guest
objectsid              : S-1-5-21-3352250647-938130414-2449934813-501
samaccountname         : Guest
codepage               : 0
samaccounttype         : USER_OBJECT
accountexpires         : NEVER
countrycode            : 0
whenchanged            : 05/01/2025 11:08:00
instancetype           : 4
objectguid             : 76485e57-831f-4a9a-b5bf-554a50e4e5b6
lastlogon              : 01/01/1601 1:00:00
lastlogoff             : 01/01/1601 1:00:00
objectcategory         : CN=Person,CN=Schema,CN=Configuration,DC=corp,DC=local
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
memberof               : CN=Guests,CN=Builtin,DC=corp,DC=local
whencreated            : 05/01/2025 11:08:00
badpwdcount            : 0
cn                     : Guest
useraccountcontrol     : ACCOUNTDISABLE, PASSWD_NOTREQD, NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
usncreated             : 8197
primarygroupid         : 514
iscriticalsystemobject : True
usnchanged             : 8197

logoncount                    : 0
badpasswordtime               : 01/01/1601 1:00:00
description                   : Key Distribution Center Service Account
distinguishedname             : CN=krbtgt,CN=Users,DC=corp,DC=local
objectclass                   : {top, person, organizationalPerson, user}
name                          : krbtgt
primarygroupid                : 513
objectsid                     : S-1-5-21-3352250647-938130414-2449934813-502
samaccountname                : krbtgt
admincount                    : 1
codepage                      : 0
samaccounttype                : USER_OBJECT
showinadvancedviewonly        : True
accountexpires                : NEVER
cn                            : krbtgt
whenchanged                   : 05/01/2025 11:39:16
instancetype                  : 4
objectguid                    : 3e5f2afb-8433-4a2b-ad2b-e1f082a1352c
lastlogon                     : 01/01/1601 1:00:00
lastlogoff                    : 01/01/1601 1:00:00
objectcategory                : CN=Person,CN=Schema,CN=Configuration,DC=corp,DC=local
dscorepropagationdata         : {05/01/2025 11:39:16, 05/01/2025 11:08:50, 01/01/1601 0:04:16}
serviceprincipalname          : kadmin/changepw
memberof                      : CN=Denied RODC Password Replication Group,CN=Users,DC=corp,DC=local
whencreated                   : 05/01/2025 11:08:50
iscriticalsystemobject        : True
badpwdcount                   : 0
useraccountcontrol            : ACCOUNTDISABLE, NORMAL_ACCOUNT
usncreated                    : 12324
countrycode                   : 0
pwdlastset                    : 05/01/2025 12:08:50
msds-supportedencryptiontypes : 0
usnchanged                    : 16421

logoncount            : 16
badpasswordtime       : 01/01/1601 1:00:00
distinguishedname     : CN=empleado1,CN=Users,DC=corp,DC=local
objectclass           : {top, person, organizationalPerson, user}
displayname           : empleado1
lastlogontimestamp    : 05/01/2025 19:05:38
name                  : empleado1
objectsid             : S-1-5-21-3352250647-938130414-2449934813-1104
samaccountname        : empleado1
admincount            : 1
codepage              : 0
samaccounttype        : USER_OBJECT
accountexpires        : NEVER
countrycode           : 0
whenchanged           : 08/01/2025 12:36:49
instancetype          : 4
usncreated            : 16458
objectguid            : 438f71e8-3e05-4f21-bba7-700dd9a044e1
lastlogoff            : 01/01/1601 1:00:00
objectcategory        : CN=Person,CN=Schema,CN=Configuration,DC=corp,DC=local
dscorepropagationdata : {08/01/2025 12:36:49, 06/01/2025 12:27:05, 06/01/2025 10:13:29, 05/01/2025 17:57:05...}
givenname             : empleado1
lastlogon             : 10/01/2025 9:24:43
badpwdcount           : 0
cn                    : empleado1
useraccountcontrol    : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
whencreated           : 05/01/2025 17:57:05
primarygroupid        : 513
pwdlastset            : 05/01/2025 18:57:05
usnchanged            : 32826

logoncount            : 10
badpasswordtime       : 01/01/1601 1:00:00
distinguishedname     : CN=empleado2,CN=Users,DC=corp,DC=local
objectclass           : {top, person, organizationalPerson, user}
displayname           : empleado2
lastlogontimestamp    : 05/01/2025 19:05:40
name                  : empleado2
objectsid             : S-1-5-21-3352250647-938130414-2449934813-1105
samaccountname        : empleado2
codepage              : 0
samaccounttype        : USER_OBJECT
accountexpires        : NEVER
countrycode           : 0
whenchanged           : 06/01/2025 12:27:05
instancetype          : 4
usncreated            : 16466
objectguid            : 5c5b97bc-c7a3-4d27-8291-6b9a4a77e511
lastlogoff            : 01/01/1601 1:00:00
objectcategory        : CN=Person,CN=Schema,CN=Configuration,DC=corp,DC=local
dscorepropagationdata : {06/01/2025 12:27:05, 06/01/2025 10:13:29, 05/01/2025 17:58:25, 01/01/1601 0:00:00}
givenname             : empleado2
lastlogon             : 10/01/2025 9:24:49
badpwdcount           : 0
cn                    : empleado2
useraccountcontrol    : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
whencreated           : 05/01/2025 17:58:25
primarygroupid        : 513
pwdlastset            : 05/01/2025 18:58:25
usnchanged            : 20603
```

Y podemos filtrar esta informacion de la misma forma:

```powershell
Get-NetUser | select name,lastlogoff,lastlogon
```

Info:

```
name          lastlogoff         lastlogon
----          ----------         ---------
Administrator 01/01/1601 1:00:00 10/01/2025 9:24:38
Guest         01/01/1601 1:00:00 01/01/1601 1:00:00
krbtgt        01/01/1601 1:00:00 01/01/1601 1:00:00
empleado1     01/01/1601 1:00:00 10/01/2025 9:24:43
empleado2     01/01/1601 1:00:00 10/01/2025 9:24:49
```

### Enumerar información de los equipos del dominio

Con el modulo de `AD` podremos sacar los grupos que tenemos en el dominio de la siguiente forma:

```powershell
Get-ADComputer -Filter *
```

Info:

```
DNSHostName        : DC01.corp.local
UserPrincipalName  :
Enabled            : True
SamAccountName     : DC01$
SID                : S-1-5-21-3352250647-938130414-2449934813-1001
DistinguishedName  : CN=DC01,OU=Domain Controllers,DC=corp,DC=local
Name               : DC01
ObjectClass        : computer
ObjectGuid         : cccef2ba-863c-497e-a461-f69fd9e4fa7e
PropertyNames      : {DistinguishedName, DNSHostName, Enabled, Name...}
AddedProperties    : {}
RemovedProperties  : {}
ModifiedProperties : {}
PropertyCount      : 9

DNSHostName        : WS01.corp.local
UserPrincipalName  :
Enabled            : True
SamAccountName     : WS01$
SID                : S-1-5-21-3352250647-938130414-2449934813-1106
DistinguishedName  : CN=WS01,CN=Computers,DC=corp,DC=local
Name               : WS01
ObjectClass        : computer
ObjectGuid         : 2dce0dd7-5b41-4809-adeb-8afb66039f26
PropertyNames      : {DistinguishedName, DNSHostName, Enabled, Name...}
AddedProperties    : {}
RemovedProperties  : {}
ModifiedProperties : {}
PropertyCount      : 9

DNSHostName        : WS02.corp.local
UserPrincipalName  :
Enabled            : True
SamAccountName     : WS02$
SID                : S-1-5-21-3352250647-938130414-2449934813-1107
DistinguishedName  : CN=WS02,CN=Computers,DC=corp,DC=local
Name               : WS02
ObjectClass        : computer
ObjectGuid         : 899b9128-078c-4eb1-af4e-a007f9b44a1b
PropertyNames      : {DistinguishedName, DNSHostName, Enabled, Name...}
AddedProperties    : {}
RemovedProperties  : {}
ModifiedProperties : {}
PropertyCount      : 9
```

Si lo queremos filtrar por informacion mas relevante:

```powershell
Get-ADComputer -Filter * | select DNSHostName,SamAccountName,Name
```

Info:

```
DNSHostName     SamAccountName Name
-----------     -------------- ----
DC01.corp.local DC01$          DC01
WS01.corp.local WS01$          WS01
WS02.corp.local WS02$          WS02
```

Podremos hacer esto mismo pero con `PowerView` de la siguiente forma:

```powershell
Get-NetComputer
```

Info:

```
pwdlastset                    : 05/01/2025 12:09:18
logoncount                    : 46
msds-generationid             : {246, 73, 21, 1...}
serverreferencebl             : CN=DC01,CN=Servers,CN=Default-First-Site-Name,CN=Sites,CN=Configuration,DC=corp,DC=loca
                                l
badpasswordtime               : 01/01/1601 1:00:00
distinguishedname             : CN=DC01,OU=Domain Controllers,DC=corp,DC=local
objectclass                   : {top, person, organizationalPerson, user...}
lastlogontimestamp            : 05/01/2025 12:09:29
name                          : DC01
objectsid                     : S-1-5-21-3352250647-938130414-2449934813-1001
samaccountname                : DC01$
localpolicyflags              : 0
codepage                      : 0
samaccounttype                : MACHINE_ACCOUNT
whenchanged                   : 05/01/2025 11:14:30
accountexpires                : NEVER
countrycode                   : 0
operatingsystem               : Windows Server 2022 Standard
instancetype                  : 4
msdfsr-computerreferencebl    : CN=DC01,CN=Topology,CN=Domain System
                                Volume,CN=DFSR-GlobalSettings,CN=System,DC=corp,DC=local
objectguid                    : cccef2ba-863c-497e-a461-f69fd9e4fa7e
operatingsystemversion        : 10.0 (20348)
lastlogoff                    : 01/01/1601 1:00:00
objectcategory                : CN=Computer,CN=Schema,CN=Configuration,DC=corp,DC=local
dscorepropagationdata         : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
serviceprincipalname          : {Dfsr-12F9A27C-BF97-4787-9364-D31B6C55EB04/DC01.corp.local,
                                ldap/DC01.corp.local/ForestDnsZones.corp.local,
                                ldap/DC01.corp.local/DomainDnsZones.corp.local, DNS/DC01.corp.local...}
usncreated                    : 12293
lastlogon                     : 10/01/2025 9:20:11
badpwdcount                   : 0
cn                            : DC01
useraccountcontrol            : SERVER_TRUST_ACCOUNT, TRUSTED_FOR_DELEGATION
whencreated                   : 05/01/2025 11:08:49
primarygroupid                : 516
iscriticalsystemobject        : True
msds-supportedencryptiontypes : 28
usnchanged                    : 12763
ridsetreferences              : CN=RID Set,CN=DC01,OU=Domain Controllers,DC=corp,DC=local
dnshostname                   : DC01.corp.local

logoncount                    : 33
badpasswordtime               : 01/01/1601 1:00:00
distinguishedname             : CN=WS01,CN=Computers,DC=corp,DC=local
objectclass                   : {top, person, organizationalPerson, user...}
badpwdcount                   : 0
displayname                   : WS01$
lastlogontimestamp            : 05/01/2025 19:05:38
objectsid                     : S-1-5-21-3352250647-938130414-2449934813-1106
samaccountname                : WS01$
localpolicyflags              : 0
lastlogon                     : 10/01/2025 9:41:10
codepage                      : 0
samaccounttype                : MACHINE_ACCOUNT
countrycode                   : 0
cn                            : WS01
accountexpires                : NEVER
whenchanged                   : 05/01/2025 18:05:38
instancetype                  : 4
usncreated                    : 16477
objectguid                    : 2dce0dd7-5b41-4809-adeb-8afb66039f26
operatingsystem               : Windows 10 Pro
operatingsystemversion        : 10.0 (19045)
lastlogoff                    : 01/01/1601 1:00:00
objectcategory                : CN=Computer,CN=Schema,CN=Configuration,DC=corp,DC=local
dscorepropagationdata         : 01/01/1601 0:00:00
serviceprincipalname          : {RestrictedKrbHost/WS01, RestrictedKrbHost/WS01.corp.local, HOST/WS01,
                                HOST/WS01.corp.local}
ms-ds-creatorsid              : {1, 5, 0, 0...}
iscriticalsystemobject        : False
usnchanged                    : 16485
useraccountcontrol            : WORKSTATION_TRUST_ACCOUNT
whencreated                   : 05/01/2025 18:05:38
primarygroupid                : 515
pwdlastset                    : 05/01/2025 19:05:38
msds-supportedencryptiontypes : 28
name                          : WS01
dnshostname                   : WS01.corp.local

logoncount                    : 29
badpasswordtime               : 01/01/1601 1:00:00
distinguishedname             : CN=WS02,CN=Computers,DC=corp,DC=local
objectclass                   : {top, person, organizationalPerson, user...}
badpwdcount                   : 0
displayname                   : WS02$
lastlogontimestamp            : 05/01/2025 19:05:41
objectsid                     : S-1-5-21-3352250647-938130414-2449934813-1107
samaccountname                : WS02$
localpolicyflags              : 0
lastlogon                     : 10/01/2025 9:41:11
codepage                      : 0
samaccounttype                : MACHINE_ACCOUNT
countrycode                   : 0
cn                            : WS02
accountexpires                : NEVER
whenchanged                   : 05/01/2025 18:05:41
instancetype                  : 4
usncreated                    : 16490
objectguid                    : 899b9128-078c-4eb1-af4e-a007f9b44a1b
operatingsystem               : Windows 10 Pro
operatingsystemversion        : 10.0 (19045)
lastlogoff                    : 01/01/1601 1:00:00
objectcategory                : CN=Computer,CN=Schema,CN=Configuration,DC=corp,DC=local
dscorepropagationdata         : 01/01/1601 0:00:00
serviceprincipalname          : {RestrictedKrbHost/WS02, RestrictedKrbHost/WS02.corp.local, HOST/WS02,
                                HOST/WS02.corp.local}
ms-ds-creatorsid              : {1, 5, 0, 0...}
iscriticalsystemobject        : False
usnchanged                    : 16499
useraccountcontrol            : WORKSTATION_TRUST_ACCOUNT
whencreated                   : 05/01/2025 18:05:40
primarygroupid                : 515
pwdlastset                    : 05/01/2025 19:05:40
msds-supportedencryptiontypes : 28
name                          : WS02
dnshostname                   : WS02.corp.local
```

Aqui por lo que vemos, estamos viendo mucha mas informacion, como por ejemplo la version del sistema operativo que tiene cada uno, el sistema operativo de que tipo es, etc.. Informacion que puede venir muy bien de cara al atacante.

Para filtrar un poco haremos esto:

```powershell
Get-NetComputer | select name,operatingsystemversion
```

Info:

```
name operatingsystemversion
---- ----------------------
DC01 10.0 (20348)
WS01 10.0 (19045)
WS02 10.0 (19045)
```

Para poder identificar si un equipo esta activo o no, `PowerView` te proporciona una opcion la cual puede ver si esta activo o no con el `-Ping` de la siguiente forma:

```powershell
Get-NetComputer -Ping | select name,operatingsystem
```

Info:

```
name operatingsystem
---- ---------------
DC01 Windows Server 2022 Standard
WS01 Windows 10 Pro
WS02 Windows 10 Pro
```
