---
icon: folder-grid
---

# Enumeración de NTDS - Parte 2

En este caso ya no vamos a ver como se haria con el modulo de `AD` de lo que se haga en `PowerView` pero igualmente todo lo que hagamos en `PowerView` se puede hacer en el modulo de `AD` solo que con otros comandos que se puede buscar informacion en internet o en `ChatGPT`.

Para obtener los grupos de dominio con `PowerView` se hara de la siguiente forma:

```powershell
Get-DomainGroup
```

Info:

```
grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
admincount             : 1
iscriticalsystemobject : True
samaccounttype         : ALIAS_OBJECT
samaccountname         : Administrators
whenchanged            : 06/01/2025 10:33:02
objectsid              : S-1-5-32-544
objectclass            : {top, group}
cn                     : Administrators
usnchanged             : 20556
systemflags            : -1946157056
name                   : Administrators
dscorepropagationdata  : {05/01/2025 11:39:16, 05/01/2025 11:08:50, 01/01/1601 0:04:16}
description            : Administrators have complete and unrestricted access to the computer/domain
distinguishedname      : CN=Administrators,CN=Builtin,DC=corp,DC=local
member                 : {CN=Domain Admins,CN=Users,DC=corp,DC=local, CN=Enterprise Admins,CN=Users,DC=corp,DC=local,
                         CN=Administrator,CN=Users,DC=corp,DC=local}
usncreated             : 8199
whencreated            : 05/01/2025 11:08:00
instancetype           : 4
objectguid             : d7f7ea74-163e-4306-ab6e-1d909f3ed111
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
systemflags            : -1946157056
iscriticalsystemobject : True
samaccounttype         : ALIAS_OBJECT
samaccountname         : Users
whenchanged            : 05/01/2025 11:08:50
objectsid              : S-1-5-32-545
objectclass            : {top, group}
cn                     : Users
usnchanged             : 12381
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : Users
description            : Users are prevented from making accidental or intentional system-wide changes and can run
                         most applications
distinguishedname      : CN=Users,CN=Builtin,DC=corp,DC=local
member                 : {CN=Domain Users,CN=Users,DC=corp,DC=local,
                         CN=S-1-5-11,CN=ForeignSecurityPrincipals,DC=corp,DC=local,
                         CN=S-1-5-4,CN=ForeignSecurityPrincipals,DC=corp,DC=local}
usncreated             : 8202
whencreated            : 05/01/2025 11:08:00
instancetype           : 4
objectguid             : 2c1eb79f-307f-451f-b73a-2c355d0fc94e
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
systemflags            : -1946157056
iscriticalsystemobject : True
samaccounttype         : ALIAS_OBJECT
samaccountname         : Guests
whenchanged            : 05/01/2025 11:08:50
objectsid              : S-1-5-32-546
objectclass            : {top, group}
cn                     : Guests
usnchanged             : 12383
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : Guests
description            : Guests have the same access as members of the Users group by default, except for the Guest
                         account which is further restricted
distinguishedname      : CN=Guests,CN=Builtin,DC=corp,DC=local
member                 : {CN=Domain Guests,CN=Users,DC=corp,DC=local, CN=Guest,CN=Users,DC=corp,DC=local}
usncreated             : 8208
whencreated            : 05/01/2025 11:08:00
instancetype           : 4
objectguid             : 3ad69d35-69d5-4ee7-a3df-497f32825921
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 8211
admincount             : 1
iscriticalsystemobject : True
grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccountname         : Print Operators
whenchanged            : 05/01/2025 11:39:16
objectsid              : S-1-5-32-550
objectclass            : {top, group}
cn                     : Print Operators
usnchanged             : 16418
dscorepropagationdata  : {05/01/2025 11:39:16, 05/01/2025 11:08:50, 01/01/1601 0:04:16}
name                   : Print Operators
description            : Members can administer printers installed on domain controllers
distinguishedname      : CN=Print Operators,CN=Builtin,DC=corp,DC=local
samaccounttype         : ALIAS_OBJECT
systemflags            : -1946157056
whencreated            : 05/01/2025 11:08:00
instancetype           : 4
objectguid             : 098213e7-7f2d-44dd-9e49-303e7444dc16
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 8212
admincount             : 1
iscriticalsystemobject : True
grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccountname         : Backup Operators
whenchanged            : 05/01/2025 11:39:16
objectsid              : S-1-5-32-551
objectclass            : {top, group}
cn                     : Backup Operators
usnchanged             : 16411
dscorepropagationdata  : {05/01/2025 11:39:16, 05/01/2025 11:08:50, 01/01/1601 0:04:16}
name                   : Backup Operators
description            : Backup Operators can override security restrictions for the sole purpose of backing up or
                         restoring files
distinguishedname      : CN=Backup Operators,CN=Builtin,DC=corp,DC=local
samaccounttype         : ALIAS_OBJECT
systemflags            : -1946157056
whencreated            : 05/01/2025 11:08:00
instancetype           : 4
objectguid             : 35950022-1181-4f50-bc6c-674cd0c22b69
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 8213
admincount             : 1
iscriticalsystemobject : True
grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccountname         : Replicator
whenchanged            : 05/01/2025 11:39:16
objectsid              : S-1-5-32-552
objectclass            : {top, group}
cn                     : Replicator
usnchanged             : 16413
dscorepropagationdata  : {05/01/2025 11:39:16, 05/01/2025 11:08:50, 01/01/1601 0:04:16}
name                   : Replicator
description            : Supports file replication in a domain
distinguishedname      : CN=Replicator,CN=Builtin,DC=corp,DC=local
samaccounttype         : ALIAS_OBJECT
systemflags            : -1946157056
whencreated            : 05/01/2025 11:08:00
instancetype           : 4
objectguid             : 6b365345-2dba-4501-b760-64e0dbae8cc4
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 8214
systemflags            : -1946157056
iscriticalsystemobject : True
grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccountname         : Remote Desktop Users
whenchanged            : 05/01/2025 11:08:00
objectsid              : S-1-5-32-555
objectclass            : {top, group}
cn                     : Remote Desktop Users
usnchanged             : 8214
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : Remote Desktop Users
description            : Members in this group are granted the right to logon remotely
distinguishedname      : CN=Remote Desktop Users,CN=Builtin,DC=corp,DC=local
samaccounttype         : ALIAS_OBJECT
whencreated            : 05/01/2025 11:08:00
instancetype           : 4
objectguid             : acbb8f16-2506-4c6a-9ab5-2b1af8e37681
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 8215
systemflags            : -1946157056
iscriticalsystemobject : True
grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccountname         : Network Configuration Operators
whenchanged            : 05/01/2025 11:08:00
objectsid              : S-1-5-32-556
objectclass            : {top, group}
cn                     : Network Configuration Operators
usnchanged             : 8215
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : Network Configuration Operators
description            : Members in this group can have some administrative privileges to manage configuration of
                         networking features
distinguishedname      : CN=Network Configuration Operators,CN=Builtin,DC=corp,DC=local
samaccounttype         : ALIAS_OBJECT
whencreated            : 05/01/2025 11:08:00
instancetype           : 4
objectguid             : cd70aa9c-16e5-46af-ae51-a23b307f580c
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 8216
systemflags            : -1946157056
iscriticalsystemobject : True
grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccountname         : Performance Monitor Users
whenchanged            : 05/01/2025 11:08:00
objectsid              : S-1-5-32-558
objectclass            : {top, group}
cn                     : Performance Monitor Users
usnchanged             : 8216
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : Performance Monitor Users
description            : Members of this group can access performance counter data locally and remotely
distinguishedname      : CN=Performance Monitor Users,CN=Builtin,DC=corp,DC=local
samaccounttype         : ALIAS_OBJECT
whencreated            : 05/01/2025 11:08:00
instancetype           : 4
objectguid             : 823bd367-21d4-4965-85a7-a34c4914475b
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 8217
systemflags            : -1946157056
iscriticalsystemobject : True
grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccountname         : Performance Log Users
whenchanged            : 05/01/2025 11:08:00
objectsid              : S-1-5-32-559
objectclass            : {top, group}
cn                     : Performance Log Users
usnchanged             : 8217
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : Performance Log Users
description            : Members of this group may schedule logging of performance counters, enable trace providers,
                         and collect event traces both locally and via remote access to this computer
distinguishedname      : CN=Performance Log Users,CN=Builtin,DC=corp,DC=local
samaccounttype         : ALIAS_OBJECT
whencreated            : 05/01/2025 11:08:00
instancetype           : 4
objectguid             : 3b61e959-e953-4717-8082-05835c117c15
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 8218
systemflags            : -1946157056
iscriticalsystemobject : True
grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccountname         : Distributed COM Users
whenchanged            : 05/01/2025 11:08:00
objectsid              : S-1-5-32-562
objectclass            : {top, group}
cn                     : Distributed COM Users
usnchanged             : 8218
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : Distributed COM Users
description            : Members are allowed to launch, activate and use Distributed COM objects on this machine.
distinguishedname      : CN=Distributed COM Users,CN=Builtin,DC=corp,DC=local
samaccounttype         : ALIAS_OBJECT
whencreated            : 05/01/2025 11:08:00
instancetype           : 4
objectguid             : d43ecf1d-aa29-4d03-93bb-8d3804c77088
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
systemflags            : -1946157056
iscriticalsystemobject : True
samaccounttype         : ALIAS_OBJECT
samaccountname         : IIS_IUSRS
whenchanged            : 05/01/2025 11:08:00
objectsid              : S-1-5-32-568
objectclass            : {top, group}
cn                     : IIS_IUSRS
usnchanged             : 8222
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : IIS_IUSRS
description            : Built-in group used by Internet Information Services.
distinguishedname      : CN=IIS_IUSRS,CN=Builtin,DC=corp,DC=local
member                 : CN=S-1-5-17,CN=ForeignSecurityPrincipals,DC=corp,DC=local
usncreated             : 8219
whencreated            : 05/01/2025 11:08:00
instancetype           : 4
objectguid             : 5ad7533a-b04c-4e7c-a299-9cae5965d38c
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 8223
systemflags            : -1946157056
iscriticalsystemobject : True
grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccountname         : Cryptographic Operators
whenchanged            : 05/01/2025 11:08:00
objectsid              : S-1-5-32-569
objectclass            : {top, group}
cn                     : Cryptographic Operators
usnchanged             : 8223
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : Cryptographic Operators
description            : Members are authorized to perform cryptographic operations.
distinguishedname      : CN=Cryptographic Operators,CN=Builtin,DC=corp,DC=local
samaccounttype         : ALIAS_OBJECT
whencreated            : 05/01/2025 11:08:00
instancetype           : 4
objectguid             : 656672c8-5378-40ba-9ba1-e2b8c85603a4
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 8224
systemflags            : -1946157056
iscriticalsystemobject : True
grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccountname         : Event Log Readers
whenchanged            : 05/01/2025 11:08:00
objectsid              : S-1-5-32-573
objectclass            : {top, group}
cn                     : Event Log Readers
usnchanged             : 8224
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : Event Log Readers
description            : Members of this group can read event logs from local machine
distinguishedname      : CN=Event Log Readers,CN=Builtin,DC=corp,DC=local
samaccounttype         : ALIAS_OBJECT
whencreated            : 05/01/2025 11:08:00
instancetype           : 4
objectguid             : 0cfd8347-c0e4-4951-85fa-30ea4bddd467
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 8225
systemflags            : -1946157056
iscriticalsystemobject : True
grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccountname         : Certificate Service DCOM Access
whenchanged            : 05/01/2025 11:08:00
objectsid              : S-1-5-32-574
objectclass            : {top, group}
cn                     : Certificate Service DCOM Access
usnchanged             : 8225
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : Certificate Service DCOM Access
description            : Members of this group are allowed to connect to Certification Authorities in the enterprise
distinguishedname      : CN=Certificate Service DCOM Access,CN=Builtin,DC=corp,DC=local
samaccounttype         : ALIAS_OBJECT
whencreated            : 05/01/2025 11:08:00
instancetype           : 4
objectguid             : 12293310-c045-4fb3-8cf5-682bf32ca47a
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 8226
systemflags            : -1946157056
iscriticalsystemobject : True
grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccountname         : RDS Remote Access Servers
whenchanged            : 05/01/2025 11:08:00
objectsid              : S-1-5-32-575
objectclass            : {top, group}
cn                     : RDS Remote Access Servers
usnchanged             : 8226
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : RDS Remote Access Servers
description            : Servers in this group enable users of RemoteApp programs and personal virtual desktops access
                         to these resources. In Internet-facing deployments, these servers are typically deployed in
                         an edge network. This group needs to be populated on servers running RD Connection Broker. RD
                         Gateway servers and RD Web Access servers used in the deployment need to be in this group.
distinguishedname      : CN=RDS Remote Access Servers,CN=Builtin,DC=corp,DC=local
samaccounttype         : ALIAS_OBJECT
whencreated            : 05/01/2025 11:08:00
instancetype           : 4
objectguid             : ae2b4397-8a98-4254-85f0-f94f9e0e8f99
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 8227
systemflags            : -1946157056
iscriticalsystemobject : True
grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccountname         : RDS Endpoint Servers
whenchanged            : 05/01/2025 11:08:00
objectsid              : S-1-5-32-576
objectclass            : {top, group}
cn                     : RDS Endpoint Servers
usnchanged             : 8227
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : RDS Endpoint Servers
description            : Servers in this group run virtual machines and host sessions where users RemoteApp programs
                         and personal virtual desktops run. This group needs to be populated on servers running RD
                         Connection Broker. RD Session Host servers and RD Virtualization Host servers used in the
                         deployment need to be in this group.
distinguishedname      : CN=RDS Endpoint Servers,CN=Builtin,DC=corp,DC=local
samaccounttype         : ALIAS_OBJECT
whencreated            : 05/01/2025 11:08:00
instancetype           : 4
objectguid             : d555758b-1a67-4f7f-8fe5-fb12cc4be9dc
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 8228
systemflags            : -1946157056
iscriticalsystemobject : True
grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccountname         : RDS Management Servers
whenchanged            : 05/01/2025 11:08:00
objectsid              : S-1-5-32-577
objectclass            : {top, group}
cn                     : RDS Management Servers
usnchanged             : 8228
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : RDS Management Servers
description            : Servers in this group can perform routine administrative actions on servers running Remote
                         Desktop Services. This group needs to be populated on all servers in a Remote Desktop
                         Services deployment. The servers running the RDS Central Management service must be included
                         in this group.
distinguishedname      : CN=RDS Management Servers,CN=Builtin,DC=corp,DC=local
samaccounttype         : ALIAS_OBJECT
whencreated            : 05/01/2025 11:08:00
instancetype           : 4
objectguid             : 497a788c-054d-45ad-b2a9-5e381c41fcc9
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 8229
systemflags            : -1946157056
iscriticalsystemobject : True
grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccountname         : Hyper-V Administrators
whenchanged            : 05/01/2025 11:08:00
objectsid              : S-1-5-32-578
objectclass            : {top, group}
cn                     : Hyper-V Administrators
usnchanged             : 8229
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : Hyper-V Administrators
description            : Members of this group have complete and unrestricted access to all features of Hyper-V.
distinguishedname      : CN=Hyper-V Administrators,CN=Builtin,DC=corp,DC=local
samaccounttype         : ALIAS_OBJECT
whencreated            : 05/01/2025 11:08:00
instancetype           : 4
objectguid             : 36275703-94b8-442b-b438-e4d4788cdd97
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 8230
systemflags            : -1946157056
iscriticalsystemobject : True
grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccountname         : Access Control Assistance Operators
whenchanged            : 05/01/2025 11:08:00
objectsid              : S-1-5-32-579
objectclass            : {top, group}
cn                     : Access Control Assistance Operators
usnchanged             : 8230
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : Access Control Assistance Operators
description            : Members of this group can remotely query authorization attributes and permissions for
                         resources on this computer.
distinguishedname      : CN=Access Control Assistance Operators,CN=Builtin,DC=corp,DC=local
samaccounttype         : ALIAS_OBJECT
whencreated            : 05/01/2025 11:08:00
instancetype           : 4
objectguid             : 522cdf07-d99b-485c-bd4b-fd45e9447283
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 8231
systemflags            : -1946157056
iscriticalsystemobject : True
grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccountname         : Remote Management Users
whenchanged            : 05/01/2025 11:08:00
objectsid              : S-1-5-32-580
objectclass            : {top, group}
cn                     : Remote Management Users
usnchanged             : 8231
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : Remote Management Users
description            : Members of this group can access WMI resources over management protocols (such as
                         WS-Management via the Windows Remote Management service). This applies only to WMI namespaces
                         that grant access to the user.
distinguishedname      : CN=Remote Management Users,CN=Builtin,DC=corp,DC=local
samaccounttype         : ALIAS_OBJECT
whencreated            : 05/01/2025 11:08:00
instancetype           : 4
objectguid             : 8c58bcf0-82f6-4e62-a3ed-0f57c8a2d4b5
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 8232
systemflags            : -1946157056
iscriticalsystemobject : True
grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccountname         : Storage Replica Administrators
whenchanged            : 05/01/2025 11:08:00
objectsid              : S-1-5-32-582
objectclass            : {top, group}
cn                     : Storage Replica Administrators
usnchanged             : 8232
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : Storage Replica Administrators
description            : Members of this group have complete and unrestricted access to all features of Storage
                         Replica.
distinguishedname      : CN=Storage Replica Administrators,CN=Builtin,DC=corp,DC=local
samaccounttype         : ALIAS_OBJECT
whencreated            : 05/01/2025 11:08:00
instancetype           : 4
objectguid             : 4e3e4322-3340-408c-8067-92a667aec891
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 12330
iscriticalsystemobject : True
grouptype              : GLOBAL_SCOPE, SECURITY
samaccountname         : Domain Computers
whenchanged            : 05/01/2025 11:08:50
objectsid              : S-1-5-21-3352250647-938130414-2449934813-515
objectclass            : {top, group}
cn                     : Domain Computers
usnchanged             : 12332
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : Domain Computers
description            : All workstations and servers joined to the domain
distinguishedname      : CN=Domain Computers,CN=Users,DC=corp,DC=local
samaccounttype         : GROUP_OBJECT
whencreated            : 05/01/2025 11:08:50
instancetype           : 4
objectguid             : 178ee203-de7c-485c-be9f-0407c199156f
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 12333
admincount             : 1
grouptype              : GLOBAL_SCOPE, SECURITY
samaccounttype         : GROUP_OBJECT
samaccountname         : Domain Controllers
whenchanged            : 05/01/2025 11:39:16
objectsid              : S-1-5-21-3352250647-938130414-2449934813-516
objectclass            : {top, group}
cn                     : Domain Controllers
usnchanged             : 16423
dscorepropagationdata  : {05/01/2025 11:39:16, 05/01/2025 11:08:50, 01/01/1601 0:04:16}
memberof               : CN=Denied RODC Password Replication Group,CN=Users,DC=corp,DC=local
iscriticalsystemobject : True
description            : All domain controllers in the domain
distinguishedname      : CN=Domain Controllers,CN=Users,DC=corp,DC=local
name                   : Domain Controllers
whencreated            : 05/01/2025 11:08:50
instancetype           : 4
objectguid             : 7748ddc7-ef07-4d07-8ba0-e825101fae1e
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

grouptype              : UNIVERSAL_SCOPE, SECURITY
admincount             : 1
iscriticalsystemobject : True
samaccounttype         : GROUP_OBJECT
samaccountname         : Schema Admins
whenchanged            : 05/01/2025 11:39:16
objectsid              : S-1-5-21-3352250647-938130414-2449934813-518
objectclass            : {top, group}
cn                     : Schema Admins
usnchanged             : 16403
dscorepropagationdata  : {05/01/2025 11:39:16, 05/01/2025 11:08:50, 01/01/1601 0:04:16}
memberof               : CN=Denied RODC Password Replication Group,CN=Users,DC=corp,DC=local
description            : Designated administrators of the schema
distinguishedname      : CN=Schema Admins,CN=Users,DC=corp,DC=local
name                   : Schema Admins
member                 : CN=Administrator,CN=Users,DC=corp,DC=local
usncreated             : 12336
whencreated            : 05/01/2025 11:08:50
instancetype           : 4
objectguid             : 644abe0e-314d-4c0a-92bd-f08f5e206006
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

grouptype              : UNIVERSAL_SCOPE, SECURITY
admincount             : 1
iscriticalsystemobject : True
samaccounttype         : GROUP_OBJECT
samaccountname         : Enterprise Admins
whenchanged            : 05/01/2025 11:39:16
objectsid              : S-1-5-21-3352250647-938130414-2449934813-519
objectclass            : {top, group}
cn                     : Enterprise Admins
usnchanged             : 16405
dscorepropagationdata  : {05/01/2025 11:39:16, 05/01/2025 11:08:50, 01/01/1601 0:04:16}
memberof               : {CN=Denied RODC Password Replication Group,CN=Users,DC=corp,DC=local,
                         CN=Administrators,CN=Builtin,DC=corp,DC=local}
description            : Designated administrators of the enterprise
distinguishedname      : CN=Enterprise Admins,CN=Users,DC=corp,DC=local
name                   : Enterprise Admins
member                 : CN=Administrator,CN=Users,DC=corp,DC=local
usncreated             : 12339
whencreated            : 05/01/2025 11:08:50
instancetype           : 4
objectguid             : 41ca581a-53f0-47ab-98ef-aa51da880e11
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 12342
grouptype              : DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype         : ALIAS_OBJECT
samaccountname         : Cert Publishers
whenchanged            : 05/01/2025 11:08:50
objectsid              : S-1-5-21-3352250647-938130414-2449934813-517
objectclass            : {top, group}
cn                     : Cert Publishers
usnchanged             : 12344
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
memberof               : CN=Denied RODC Password Replication Group,CN=Users,DC=corp,DC=local
iscriticalsystemobject : True
description            : Members of this group are permitted to publish certificates to the directory
distinguishedname      : CN=Cert Publishers,CN=Users,DC=corp,DC=local
name                   : Cert Publishers
whencreated            : 05/01/2025 11:08:50
instancetype           : 4
objectguid             : 4a2770e6-14ad-4901-b3ec-896bb1cac0a3
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

grouptype              : GLOBAL_SCOPE, SECURITY
admincount             : 1
iscriticalsystemobject : True
samaccounttype         : GROUP_OBJECT
samaccountname         : Domain Admins
whenchanged            : 09/01/2025 8:29:15
objectsid              : S-1-5-21-3352250647-938130414-2449934813-512
objectclass            : {top, group}
cn                     : Domain Admins
usnchanged             : 36892
dscorepropagationdata  : {05/01/2025 11:39:16, 05/01/2025 11:08:50, 01/01/1601 0:04:16}
memberof               : {CN=Denied RODC Password Replication Group,CN=Users,DC=corp,DC=local,
                         CN=Administrators,CN=Builtin,DC=corp,DC=local}
description            : Designated administrators of the domain
distinguishedname      : CN=Domain Admins,CN=Users,DC=corp,DC=local
name                   : Domain Admins
member                 : CN=Administrator,CN=Users,DC=corp,DC=local
usncreated             : 12345
whencreated            : 05/01/2025 11:08:50
instancetype           : 4
objectguid             : 680e4d88-8f94-412a-98e1-e1e856a572db
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 12348
grouptype              : GLOBAL_SCOPE, SECURITY
samaccounttype         : GROUP_OBJECT
samaccountname         : Domain Users
whenchanged            : 05/01/2025 11:08:50
objectsid              : S-1-5-21-3352250647-938130414-2449934813-513
objectclass            : {top, group}
cn                     : Domain Users
usnchanged             : 12350
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
memberof               : CN=Users,CN=Builtin,DC=corp,DC=local
iscriticalsystemobject : True
description            : All domain users
distinguishedname      : CN=Domain Users,CN=Users,DC=corp,DC=local
name                   : Domain Users
whencreated            : 05/01/2025 11:08:50
instancetype           : 4
objectguid             : bb0bbd79-3803-4877-b576-368d13aba2b9
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 12351
grouptype              : GLOBAL_SCOPE, SECURITY
samaccounttype         : GROUP_OBJECT
samaccountname         : Domain Guests
whenchanged            : 05/01/2025 11:08:50
objectsid              : S-1-5-21-3352250647-938130414-2449934813-514
objectclass            : {top, group}
cn                     : Domain Guests
usnchanged             : 12353
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
memberof               : CN=Guests,CN=Builtin,DC=corp,DC=local
iscriticalsystemobject : True
description            : All domain guests
distinguishedname      : CN=Domain Guests,CN=Users,DC=corp,DC=local
name                   : Domain Guests
whencreated            : 05/01/2025 11:08:50
instancetype           : 4
objectguid             : f2f029ba-015d-4131-97aa-e30393d5bde8
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

grouptype              : GLOBAL_SCOPE, SECURITY
iscriticalsystemobject : True
samaccounttype         : GROUP_OBJECT
samaccountname         : Group Policy Creator Owners
whenchanged            : 05/01/2025 11:08:50
objectsid              : S-1-5-21-3352250647-938130414-2449934813-520
objectclass            : {top, group}
cn                     : Group Policy Creator Owners
usnchanged             : 12391
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
memberof               : CN=Denied RODC Password Replication Group,CN=Users,DC=corp,DC=local
description            : Members in this group can modify group policy for the domain
distinguishedname      : CN=Group Policy Creator Owners,CN=Users,DC=corp,DC=local
name                   : Group Policy Creator Owners
member                 : CN=Administrator,CN=Users,DC=corp,DC=local
usncreated             : 12354
whencreated            : 05/01/2025 11:08:50
instancetype           : 4
objectguid             : 2d3493c1-ed42-413f-a0c9-2423f9c35f4d
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 12357
iscriticalsystemobject : True
grouptype              : DOMAIN_LOCAL_SCOPE, SECURITY
samaccountname         : RAS and IAS Servers
whenchanged            : 05/01/2025 11:08:50
objectsid              : S-1-5-21-3352250647-938130414-2449934813-553
objectclass            : {top, group}
cn                     : RAS and IAS Servers
usnchanged             : 12359
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : RAS and IAS Servers
description            : Servers in this group can access remote access properties of users
distinguishedname      : CN=RAS and IAS Servers,CN=Users,DC=corp,DC=local
samaccounttype         : ALIAS_OBJECT
whencreated            : 05/01/2025 11:08:50
instancetype           : 4
objectguid             : 5e6f588f-5721-43fa-9398-d97931193942
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 12360
admincount             : 1
iscriticalsystemobject : True
grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccountname         : Server Operators
whenchanged            : 05/01/2025 11:39:16
objectsid              : S-1-5-32-549
objectclass            : {top, group}
cn                     : Server Operators
usnchanged             : 16419
dscorepropagationdata  : {05/01/2025 11:39:16, 05/01/2025 11:08:50, 01/01/1601 0:04:16}
name                   : Server Operators
description            : Members can administer domain servers
distinguishedname      : CN=Server Operators,CN=Builtin,DC=corp,DC=local
samaccounttype         : ALIAS_OBJECT
systemflags            : -1946157056
whencreated            : 05/01/2025 11:08:50
instancetype           : 4
objectguid             : 8c08a5eb-c61f-4e00-bb30-e1ffb5990d23
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 12363
admincount             : 1
iscriticalsystemobject : True
grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccountname         : Account Operators
whenchanged            : 05/01/2025 11:39:16
objectsid              : S-1-5-32-548
objectclass            : {top, group}
cn                     : Account Operators
usnchanged             : 16414
dscorepropagationdata  : {05/01/2025 11:39:16, 05/01/2025 11:08:50, 01/01/1601 0:04:16}
name                   : Account Operators
description            : Members can administer domain user and group accounts
distinguishedname      : CN=Account Operators,CN=Builtin,DC=corp,DC=local
samaccounttype         : ALIAS_OBJECT
systemflags            : -1946157056
whencreated            : 05/01/2025 11:08:50
instancetype           : 4
objectguid             : 357e5352-a5d2-4e1c-99b8-c4541b98e4eb
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
systemflags            : -1946157056
iscriticalsystemobject : True
samaccounttype         : ALIAS_OBJECT
samaccountname         : Pre-Windows 2000 Compatible Access
whenchanged            : 05/01/2025 11:08:50
objectsid              : S-1-5-32-554
objectclass            : {top, group}
cn                     : Pre-Windows 2000 Compatible Access
usnchanged             : 12393
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : Pre-Windows 2000 Compatible Access
description            : A backward compatibility group which allows read access on all users and groups in the domain
distinguishedname      : CN=Pre-Windows 2000 Compatible Access,CN=Builtin,DC=corp,DC=local
member                 : CN=S-1-5-11,CN=ForeignSecurityPrincipals,DC=corp,DC=local
usncreated             : 12366
whencreated            : 05/01/2025 11:08:50
instancetype           : 4
objectguid             : 32f5006f-814b-446f-8230-c24fe8e0965d
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 12369
systemflags            : -1946157056
iscriticalsystemobject : True
grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccountname         : Incoming Forest Trust Builders
whenchanged            : 05/01/2025 11:08:50
objectsid              : S-1-5-32-557
objectclass            : {top, group}
cn                     : Incoming Forest Trust Builders
usnchanged             : 12371
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : Incoming Forest Trust Builders
description            : Members of this group can create incoming, one-way trusts to this forest
distinguishedname      : CN=Incoming Forest Trust Builders,CN=Builtin,DC=corp,DC=local
samaccounttype         : ALIAS_OBJECT
whencreated            : 05/01/2025 11:08:50
instancetype           : 4
objectguid             : 7a35a3a8-8170-4b9e-b2b4-526e6a4d4199
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
systemflags            : -1946157056
iscriticalsystemobject : True
samaccounttype         : ALIAS_OBJECT
samaccountname         : Windows Authorization Access Group
whenchanged            : 05/01/2025 11:08:50
objectsid              : S-1-5-32-560
objectclass            : {top, group}
cn                     : Windows Authorization Access Group
usnchanged             : 12396
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : Windows Authorization Access Group
description            : Members of this group have access to the computed tokenGroupsGlobalAndUniversal attribute on
                         User objects
distinguishedname      : CN=Windows Authorization Access Group,CN=Builtin,DC=corp,DC=local
member                 : CN=S-1-5-9,CN=ForeignSecurityPrincipals,DC=corp,DC=local
usncreated             : 12372
whencreated            : 05/01/2025 11:08:50
instancetype           : 4
objectguid             : d893b7c6-5816-4006-b54d-49911eda5abc
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 12375
systemflags            : -1946157056
iscriticalsystemobject : True
grouptype              : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccountname         : Terminal Server License Servers
whenchanged            : 05/01/2025 11:08:50
objectsid              : S-1-5-32-561
objectclass            : {top, group}
cn                     : Terminal Server License Servers
usnchanged             : 12377
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : Terminal Server License Servers
description            : Members of this group can update user accounts in Active Directory with information about
                         license issuance, for the purpose of tracking and reporting TS Per User CAL usage
distinguishedname      : CN=Terminal Server License Servers,CN=Builtin,DC=corp,DC=local
samaccounttype         : ALIAS_OBJECT
whencreated            : 05/01/2025 11:08:50
instancetype           : 4
objectguid             : 4dddf587-71ee-46d6-b3af-ab3c05d7fe60
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 12402
iscriticalsystemobject : True
grouptype              : DOMAIN_LOCAL_SCOPE, SECURITY
samaccountname         : Allowed RODC Password Replication Group
whenchanged            : 05/01/2025 11:08:50
objectsid              : S-1-5-21-3352250647-938130414-2449934813-571
objectclass            : {top, group}
cn                     : Allowed RODC Password Replication Group
usnchanged             : 12404
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : Allowed RODC Password Replication Group
description            : Members in this group can have their passwords replicated to all read-only domain controllers
                         in the domain
distinguishedname      : CN=Allowed RODC Password Replication Group,CN=Users,DC=corp,DC=local
samaccounttype         : ALIAS_OBJECT
whencreated            : 05/01/2025 11:08:50
instancetype           : 4
objectguid             : 132ffa7c-313a-4b34-9011-df60a492b384
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

grouptype              : DOMAIN_LOCAL_SCOPE, SECURITY
iscriticalsystemobject : True
samaccounttype         : ALIAS_OBJECT
samaccountname         : Denied RODC Password Replication Group
whenchanged            : 05/01/2025 11:08:50
objectsid              : S-1-5-21-3352250647-938130414-2449934813-572
objectclass            : {top, group}
cn                     : Denied RODC Password Replication Group
usnchanged             : 12433
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : Denied RODC Password Replication Group
description            : Members in this group cannot have their passwords replicated to any read-only domain
                         controllers in the domain
distinguishedname      : CN=Denied RODC Password Replication Group,CN=Users,DC=corp,DC=local
member                 : {CN=Read-only Domain Controllers,CN=Users,DC=corp,DC=local, CN=Group Policy Creator
                         Owners,CN=Users,DC=corp,DC=local, CN=Domain Admins,CN=Users,DC=corp,DC=local, CN=Cert
                         Publishers,CN=Users,DC=corp,DC=local...}
usncreated             : 12405
whencreated            : 05/01/2025 11:08:50
instancetype           : 4
objectguid             : 6762a4ff-48fd-4a1d-9bba-52feb477cdcf
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 12419
admincount             : 1
grouptype              : GLOBAL_SCOPE, SECURITY
samaccounttype         : GROUP_OBJECT
samaccountname         : Read-only Domain Controllers
whenchanged            : 05/01/2025 11:39:16
objectsid              : S-1-5-21-3352250647-938130414-2449934813-521
objectclass            : {top, group}
cn                     : Read-only Domain Controllers
usnchanged             : 16422
dscorepropagationdata  : {05/01/2025 11:39:16, 05/01/2025 11:08:50, 01/01/1601 0:04:16}
memberof               : CN=Denied RODC Password Replication Group,CN=Users,DC=corp,DC=local
iscriticalsystemobject : True
description            : Members of this group are Read-Only Domain Controllers in the domain
distinguishedname      : CN=Read-only Domain Controllers,CN=Users,DC=corp,DC=local
name                   : Read-only Domain Controllers
whencreated            : 05/01/2025 11:08:50
instancetype           : 4
objectguid             : bd2a4aaf-8248-48b6-8171-b19e03ab95f8
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 12429
iscriticalsystemobject : True
grouptype              : UNIVERSAL_SCOPE, SECURITY
samaccountname         : Enterprise Read-only Domain Controllers
whenchanged            : 05/01/2025 11:08:50
objectsid              : S-1-5-21-3352250647-938130414-2449934813-498
objectclass            : {top, group}
cn                     : Enterprise Read-only Domain Controllers
usnchanged             : 12431
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : Enterprise Read-only Domain Controllers
description            : Members of this group are Read-Only Domain Controllers in the enterprise
distinguishedname      : CN=Enterprise Read-only Domain Controllers,CN=Users,DC=corp,DC=local
samaccounttype         : GROUP_OBJECT
whencreated            : 05/01/2025 11:08:50
instancetype           : 4
objectguid             : bdb50d4b-3899-479e-be20-f207890aa5ae
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 12440
iscriticalsystemobject : True
grouptype              : GLOBAL_SCOPE, SECURITY
samaccountname         : Cloneable Domain Controllers
whenchanged            : 05/01/2025 11:08:50
objectsid              : S-1-5-21-3352250647-938130414-2449934813-522
objectclass            : {top, group}
cn                     : Cloneable Domain Controllers
usnchanged             : 12442
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : Cloneable Domain Controllers
description            : Members of this group that are domain controllers may be cloned.
distinguishedname      : CN=Cloneable Domain Controllers,CN=Users,DC=corp,DC=local
samaccounttype         : GROUP_OBJECT
whencreated            : 05/01/2025 11:08:50
instancetype           : 4
objectguid             : 629e8f10-d85f-4c15-a303-50dd21239e3e
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 12445
iscriticalsystemobject : True
grouptype              : GLOBAL_SCOPE, SECURITY
samaccountname         : Protected Users
whenchanged            : 05/01/2025 11:08:50
objectsid              : S-1-5-21-3352250647-938130414-2449934813-525
objectclass            : {top, group}
cn                     : Protected Users
usnchanged             : 12447
dscorepropagationdata  : {05/01/2025 11:08:50, 01/01/1601 0:00:01}
name                   : Protected Users
description            : Members of this group are afforded additional protections against authentication security
                         threats. See http://go.microsoft.com/fwlink/?LinkId=298939 for more information.
distinguishedname      : CN=Protected Users,CN=Users,DC=corp,DC=local
samaccounttype         : GROUP_OBJECT
whencreated            : 05/01/2025 11:08:50
instancetype           : 4
objectguid             : bc033c4a-4608-4989-ba4b-c2bf46cf6801
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 12450
admincount             : 1
iscriticalsystemobject : True
grouptype              : GLOBAL_SCOPE, SECURITY
samaccountname         : Key Admins
whenchanged            : 05/01/2025 11:39:16
objectsid              : S-1-5-21-3352250647-938130414-2449934813-526
objectclass            : {top, group}
cn                     : Key Admins
usnchanged             : 16404
dscorepropagationdata  : {05/01/2025 11:39:16, 05/01/2025 11:08:50, 01/01/1601 0:04:16}
name                   : Key Admins
description            : Members of this group can perform administrative actions on key objects within the domain.
distinguishedname      : CN=Key Admins,CN=Users,DC=corp,DC=local
samaccounttype         : GROUP_OBJECT
whencreated            : 05/01/2025 11:08:50
instancetype           : 4
objectguid             : 94880610-3566-4edd-94b4-f52812e13fd5
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated             : 12453
admincount             : 1
iscriticalsystemobject : True
grouptype              : UNIVERSAL_SCOPE, SECURITY
samaccountname         : Enterprise Key Admins
whenchanged            : 05/01/2025 11:39:16
objectsid              : S-1-5-21-3352250647-938130414-2449934813-527
objectclass            : {top, group}
cn                     : Enterprise Key Admins
usnchanged             : 16409
dscorepropagationdata  : {05/01/2025 11:39:16, 05/01/2025 11:08:50, 01/01/1601 0:04:16}
name                   : Enterprise Key Admins
description            : Members of this group can perform administrative actions on key objects within the forest.
distinguishedname      : CN=Enterprise Key Admins,CN=Users,DC=corp,DC=local
samaccounttype         : GROUP_OBJECT
whencreated            : 05/01/2025 11:08:50
instancetype           : 4
objectguid             : 6745f1a8-c185-4a28-a5c3-01f2070f3863
objectcategory         : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated            : 12486
grouptype             : DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype        : ALIAS_OBJECT
samaccountname        : DnsAdmins
whenchanged           : 05/01/2025 11:09:29
objectsid             : S-1-5-21-3352250647-938130414-2449934813-1102
objectclass           : {top, group}
cn                    : DnsAdmins
usnchanged            : 12488
dscorepropagationdata : 01/01/1601 0:00:00
name                  : DnsAdmins
description           : DNS Administrators Group
distinguishedname     : CN=DnsAdmins,CN=Users,DC=corp,DC=local
whencreated           : 05/01/2025 11:09:29
instancetype          : 4
objectguid            : a346d812-69ca-4712-ba80-0cb860649fbe
objectcategory        : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated            : 12491
grouptype             : GLOBAL_SCOPE, SECURITY
samaccounttype        : GROUP_OBJECT
samaccountname        : DnsUpdateProxy
whenchanged           : 05/01/2025 11:09:29
objectsid             : S-1-5-21-3352250647-938130414-2449934813-1103
objectclass           : {top, group}
cn                    : DnsUpdateProxy
usnchanged            : 12491
dscorepropagationdata : 01/01/1601 0:00:00
name                  : DnsUpdateProxy
description           : DNS clients who are permitted to perform dynamic updates on behalf of some other clients (such
                        as DHCP servers).
distinguishedname     : CN=DnsUpdateProxy,CN=Users,DC=corp,DC=local
whencreated           : 05/01/2025 11:09:29
instancetype          : 4
objectguid            : 386cd998-31b5-4c22-8529-1420841b00ee
objectcategory        : CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local
```

Hay demasiada informacion por lo que lo filtaremos un poco para ver mejor todo:

```powershell
Get-DomainGroup | select grouptype,name,description
```

Info:

```
                                     grouptype name                                    description
                                      --------- ----                                    -----------
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY Administrators                          Administrators have complete...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY Users                                   Users are prevented from mak...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY Guests                                  Guests have the same access ...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY Print Operators                         Members can administer print...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY Backup Operators                        Backup Operators can overrid...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY Replicator                              Supports file replication in...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY Remote Desktop Users                    Members in this group are gr...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY Network Configuration Operators         Members in this group can ha...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY Performance Monitor Users               Members of this group can ac...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY Performance Log Users                   Members of this group may sc...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY Distributed COM Users                   Members are allowed to launc...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY IIS_IUSRS                               Built-in group used by Inter...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY Cryptographic Operators                 Members are authorized to pe...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY Event Log Readers                       Members of this group can re...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY Certificate Service DCOM Access         Members of this group are al...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY RDS Remote Access Servers               Servers in this group enable...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY RDS Endpoint Servers                    Servers in this group run vi...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY RDS Management Servers                  Servers in this group can pe...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY Hyper-V Administrators                  Members of this group have c...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY Access Control Assistance Operators     Members of this group can re...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY Remote Management Users                 Members of this group can ac...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY Storage Replica Administrators          Members of this group have c...
                         GLOBAL_SCOPE, SECURITY Domain Computers                        All workstations and servers...
                         GLOBAL_SCOPE, SECURITY Domain Controllers                      All domain controllers in th...
                      UNIVERSAL_SCOPE, SECURITY Schema Admins                           Designated administrators of...
                      UNIVERSAL_SCOPE, SECURITY Enterprise Admins                       Designated administrators of...
                   DOMAIN_LOCAL_SCOPE, SECURITY Cert Publishers                         Members of this group are pe...
                         GLOBAL_SCOPE, SECURITY Domain Admins                           Designated administrators of...
                         GLOBAL_SCOPE, SECURITY Domain Users                            All domain users
                         GLOBAL_SCOPE, SECURITY Domain Guests                           All domain guests
                         GLOBAL_SCOPE, SECURITY Group Policy Creator Owners             Members in this group can mo...
                   DOMAIN_LOCAL_SCOPE, SECURITY RAS and IAS Servers                     Servers in this group can ac...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY Server Operators                        Members can administer domai...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY Account Operators                       Members can administer domai...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY Pre-Windows 2000 Compatible Access      A backward compatibility gro...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY Incoming Forest Trust Builders          Members of this group can cr...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY Windows Authorization Access Group      Members of this group have a...
CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY Terminal Server License Servers         Members of this group can up...
                   DOMAIN_LOCAL_SCOPE, SECURITY Allowed RODC Password Replication Group Members in this group can ha...
                   DOMAIN_LOCAL_SCOPE, SECURITY Denied RODC Password Replication Group  Members in this group cannot...
                         GLOBAL_SCOPE, SECURITY Read-only Domain Controllers            Members of this group are Re...
                      UNIVERSAL_SCOPE, SECURITY Enterprise Read-only Domain Controllers Members of this group are Re...
                         GLOBAL_SCOPE, SECURITY Cloneable Domain Controllers            Members of this group that a...
                         GLOBAL_SCOPE, SECURITY Protected Users                         Members of this group are af...
                         GLOBAL_SCOPE, SECURITY Key Admins                              Members of this group can pe...
                      UNIVERSAL_SCOPE, SECURITY Enterprise Key Admins                   Members of this group can pe...
                   DOMAIN_LOCAL_SCOPE, SECURITY DnsAdmins                               DNS Administrators Group
                         GLOBAL_SCOPE, SECURITY DnsUpdateProxy                          DNS clients who are permitte...
```

### Enumerar grupo administrador

Pero si queremos saber que usuarios pertenecen al grupo administradores mediante `PowerView`, podremos hacerlo de la siguiente forma:

```powershell
Get-NetGroupMember -Identity "Administrators"
```

Info:

```
GroupDomain             : corp.local
GroupName               : Administrators
GroupDistinguishedName  : CN=Administrators,CN=Builtin,DC=corp,DC=local
MemberDomain            : corp.local
MemberName              : Domain Admins
MemberDistinguishedName : CN=Domain Admins,CN=Users,DC=corp,DC=local
MemberObjectClass       : group
MemberSID               : S-1-5-21-3352250647-938130414-2449934813-512

GroupDomain             : corp.local
GroupName               : Administrators
GroupDistinguishedName  : CN=Administrators,CN=Builtin,DC=corp,DC=local
MemberDomain            : corp.local
MemberName              : Enterprise Admins
MemberDistinguishedName : CN=Enterprise Admins,CN=Users,DC=corp,DC=local
MemberObjectClass       : group
MemberSID               : S-1-5-21-3352250647-938130414-2449934813-519

GroupDomain             : corp.local
GroupName               : Administrators
GroupDistinguishedName  : CN=Administrators,CN=Builtin,DC=corp,DC=local
MemberDomain            : corp.local
MemberName              : Administrator
MemberDistinguishedName : CN=Administrator,CN=Users,DC=corp,DC=local
MemberObjectClass       : user
MemberSID               : S-1-5-21-3352250647-938130414-2449934813-500
```

Si lo queremos filtrar para que solo aparezca los `MemberName` se hara asi:

```powershell
Get-NetGroupMember -Identity "Administrators" | select MemberName
```

Info:

```
MemberName
----------
Domain Admins
Enterprise Admins
Administrator
```

### Enumerar recursos compartidos del dominio

Lo que tambien podemos hacer es enumerar los recursos compartidos del dominio de la siguiente forma:

```powershell
Find-DomainShare
```

Info:

```
Name                Type Remark                 ComputerName
----                ---- ------                 ------------
ADMIN$        2147483648 Remote Admin           DC01.corp.local
C$            2147483648 Default share          DC01.corp.local
departamental          0                        DC01.corp.local
IPC$          2147483651 Remote IPC             DC01.corp.local
NETLOGON               0 Logon server share     DC01.corp.local
SYSVOL                 0 Logon server share     DC01.corp.local
ADMIN$        2147483648 Admin remota           WS01.corp.local
C$            2147483648 Recurso predeterminado WS01.corp.local
IPC$          2147483651 IPC remota             WS01.corp.local
ADMIN$        2147483648 Admin remota           WS02.corp.local
C$            2147483648 Recurso predeterminado WS02.corp.local
IPC$          2147483651 IPC remota             WS02.corp.local
```

Aviso, esto tarda incluso algunos minutos hasta que te saca todo, pero con esto podremos ver a que recursos podremos intentar entrar como atacante.

### Enumerar OUs

Tambien podemos enumerar las `Unidades Organizativas` (OUs):

```powershell
Get-NetOU
```

Info:

```
usncreated             : 5804
systemflags            : -1946157056
iscriticalsystemobject : True
gplink                 : [LDAP://CN={6AC1786C-016F-11D2-945F-00C04fB984F9},CN=Policies,CN=System,DC=corp,DC=local;0]
whenchanged            : 05/01/2025 11:08:00
objectclass            : {top, organizationalUnit}
showinadvancedviewonly : False
usnchanged             : 5804
dscorepropagationdata  : {06/01/2025 10:12:07, 05/01/2025 11:08:50, 01/01/1601 0:04:16}
name                   : Domain Controllers
description            : Default container for domain controllers
distinguishedname      : OU=Domain Controllers,DC=corp,DC=local
ou                     : Domain Controllers
whencreated            : 05/01/2025 11:08:00
instancetype           : 4
objectguid             : bdc182ba-1353-4b04-92b3-37bf5c453dbe
objectcategory         : CN=Organizational-Unit,CN=Schema,CN=Configuration,DC=corp,DC=local
```

### Enumerar GPOs

Tambien podremos enumerar las `GPOs` que son muy importantes para ver que se nos ejecuta o que politicas tenemos de ejecuccion, etc...

```powershell
Get-NetGPO
```

Info:

```
usncreated               : 5672
systemflags              : -1946157056
displayname              : Default Domain Policy
gpcmachineextensionnames : [{35378EAC-683F-11D2-A89A-00C04FBBCFA2}{53D6AB1B-2488-11D1-A28C-00C04FB94F17}][{827D319E-6EA
                           C-11D2-A4EA-00C04F79F83A}{803E14A0-B4FB-11D0-A0D0-00A0C90F574B}][{B1BE8D72-6EAC-11D2-A4EA-00
                           C04F79F83A}{53D6AB1B-2488-11D1-A28C-00C04FB94F17}]
whenchanged              : 05/01/2025 11:11:58
objectclass              : {top, container, groupPolicyContainer}
gpcfunctionalityversion  : 2
showinadvancedviewonly   : True
usnchanged               : 12751
dscorepropagationdata    : {05/01/2025 11:08:50, 01/01/1601 0:00:00}
name                     : {31B2F340-016D-11D2-945F-00C04FB984F9}
flags                    : 0
cn                       : {31B2F340-016D-11D2-945F-00C04FB984F9}
iscriticalsystemobject   : True
gpcfilesyspath           : \\corp.local\sysvol\corp.local\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}
distinguishedname        : CN={31B2F340-016D-11D2-945F-00C04FB984F9},CN=Policies,CN=System,DC=corp,DC=local
whencreated              : 05/01/2025 11:07:59
versionnumber            : 3
instancetype             : 4
objectguid               : 69776306-72bc-4096-81ac-9065448cb4a0
objectcategory           : CN=Group-Policy-Container,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated               : 5675
systemflags              : -1946157056
displayname              : Default Domain Controllers Policy
gpcmachineextensionnames : [{827D319E-6EAC-11D2-A4EA-00C04F79F83A}{803E14A0-B4FB-11D0-A0D0-00A0C90F574B}]
whenchanged              : 05/01/2025 11:07:59
objectclass              : {top, container, groupPolicyContainer}
gpcfunctionalityversion  : 2
showinadvancedviewonly   : True
usnchanged               : 5675
dscorepropagationdata    : {05/01/2025 11:08:50, 01/01/1601 0:00:00}
name                     : {6AC1786C-016F-11D2-945F-00C04fB984F9}
flags                    : 0
cn                       : {6AC1786C-016F-11D2-945F-00C04fB984F9}
iscriticalsystemobject   : True
gpcfilesyspath           : \\corp.local\sysvol\corp.local\Policies\{6AC1786C-016F-11D2-945F-00C04fB984F9}
distinguishedname        : CN={6AC1786C-016F-11D2-945F-00C04fB984F9},CN=Policies,CN=System,DC=corp,DC=local
whencreated              : 05/01/2025 11:07:59
versionnumber            : 1
instancetype             : 4
objectguid               : 7ee475ca-6694-4ab0-8b83-d00a93a7bcfa
objectcategory           : CN=Group-Policy-Container,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated              : 20589
displayname             : Unidad Compartida Policy
whenchanged             : 06/01/2025 12:18:22
objectclass             : {top, container, groupPolicyContainer}
gpcfunctionalityversion : 2
showinadvancedviewonly  : True
usnchanged              : 20600
dscorepropagationdata   : 01/01/1601 0:00:00
name                    : {507F35A7-D0D3-4917-9561-240C31EE0DD4}
flags                   : 0
cn                      : {507F35A7-D0D3-4917-9561-240C31EE0DD4}
gpcuserextensionnames   : [{42B5FAAE-6536-11D2-AE5A-0000F87571E3}{40B66650-4972-11D1-A7CA-0000F87571E3}]
gpcfilesyspath          : \\corp.local\SysVol\corp.local\Policies\{507F35A7-D0D3-4917-9561-240C31EE0DD4}
distinguishedname       : CN={507F35A7-D0D3-4917-9561-240C31EE0DD4},CN=Policies,CN=System,DC=corp,DC=local
whencreated             : 06/01/2025 12:14:51
versionnumber           : 131072
instancetype            : 4
objectguid              : 1b078af7-1c9d-4c53-8318-2f0013d62e64
objectcategory          : CN=Group-Policy-Container,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated               : 24603
displayname              : Script Execution Policy
gpcmachineextensionnames : [{35378EAC-683F-11D2-A89A-00C04FBBCFA2}{D02B1F72-3407-48AE-BA88-E8213C6761F1}]
whenchanged              : 07/01/2025 19:33:42
objectclass              : {top, container, groupPolicyContainer}
gpcfunctionalityversion  : 2
showinadvancedviewonly   : True
usnchanged               : 24613
dscorepropagationdata    : 01/01/1601 0:00:00
name                     : {410CF9DA-E128-4646-B131-688DF0C8538D}
flags                    : 0
cn                       : {410CF9DA-E128-4646-B131-688DF0C8538D}
gpcfilesyspath           : \\corp.local\SysVol\corp.local\Policies\{410CF9DA-E128-4646-B131-688DF0C8538D}
distinguishedname        : CN={410CF9DA-E128-4646-B131-688DF0C8538D},CN=Policies,CN=System,DC=corp,DC=local
whencreated              : 07/01/2025 19:27:07
versionnumber            : 1
instancetype             : 4
objectguid               : 6c17e59c-b1ec-411a-ad2c-ef273ba52208
objectcategory           : CN=Group-Policy-Container,CN=Schema,CN=Configuration,DC=corp,DC=local
```

Vamos a filtrarlo un poco por los nombres de las politicas que estan en ejeccucion:

```powershell
Get-NetGPO | select displayname
```

Info:

```
displayname
-----------
Default Domain Policy
Default Domain Controllers Policy
Unidad Compartida Policy
Script Execution Policy
```

Tambien podemos ver que `GPOs` estan aplicando a dicho equipo de la siguiente forma:

```powershell
Get-NetGPO -ComputerIdentity WS02
```

Info:

```
usncreated               : 24603
displayname              : Script Execution Policy
gpcmachineextensionnames : [{35378EAC-683F-11D2-A89A-00C04FBBCFA2}{D02B1F72-3407-48AE-BA88-E8213C6761F1}]
whenchanged              : 07/01/2025 19:33:42
objectclass              : {top, container, groupPolicyContainer}
gpcfunctionalityversion  : 2
showinadvancedviewonly   : True
usnchanged               : 24613
dscorepropagationdata    : 01/01/1601 0:00:00
name                     : {410CF9DA-E128-4646-B131-688DF0C8538D}
flags                    : 0
cn                       : {410CF9DA-E128-4646-B131-688DF0C8538D}
gpcfilesyspath           : \\corp.local\SysVol\corp.local\Policies\{410CF9DA-E128-4646-B131-688DF0C8538D}
distinguishedname        : CN={410CF9DA-E128-4646-B131-688DF0C8538D},CN=Policies,CN=System,DC=corp,DC=local
whencreated              : 07/01/2025 19:27:07
versionnumber            : 1
instancetype             : 4
objectguid               : 6c17e59c-b1ec-411a-ad2c-ef273ba52208
objectcategory           : CN=Group-Policy-Container,CN=Schema,CN=Configuration,DC=corp,DC=local

usncreated               : 5672
systemflags              : -1946157056
displayname              : Default Domain Policy
gpcmachineextensionnames : [{35378EAC-683F-11D2-A89A-00C04FBBCFA2}{53D6AB1B-2488-11D1-A28C-00C04FB94F17}][{827D319E-6EA
                           C-11D2-A4EA-00C04F79F83A}{803E14A0-B4FB-11D0-A0D0-00A0C90F574B}][{B1BE8D72-6EAC-11D2-A4EA-00
                           C04F79F83A}{53D6AB1B-2488-11D1-A28C-00C04FB94F17}]
whenchanged              : 05/01/2025 11:11:58
objectclass              : {top, container, groupPolicyContainer}
gpcfunctionalityversion  : 2
showinadvancedviewonly   : True
usnchanged               : 12751
dscorepropagationdata    : {05/01/2025 11:08:50, 01/01/1601 0:00:00}
name                     : {31B2F340-016D-11D2-945F-00C04FB984F9}
flags                    : 0
cn                       : {31B2F340-016D-11D2-945F-00C04FB984F9}
iscriticalsystemobject   : True
gpcfilesyspath           : \\corp.local\sysvol\corp.local\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}
distinguishedname        : CN={31B2F340-016D-11D2-945F-00C04FB984F9},CN=Policies,CN=System,DC=corp,DC=local
whencreated              : 05/01/2025 11:07:59
versionnumber            : 3
instancetype             : 4
objectguid               : 69776306-72bc-4096-81ac-9065448cb4a0
objectcategory           : CN=Group-Policy-Container,CN=Schema,CN=Configuration,DC=corp,DC=local
```

Igual, si lo queremos filtrar por los nombre sera de la siguiente forma:

```powershell
Get-NetGPO -ComputerIdentity WS02 | select displayname
```

Info:

```
displayname
-----------
Script Execution Policy
Default Domain Policy
```

### Enumerar ACL's

Tambien podremos enumerar las `ACLs` de la siguiente forma:

```powershell
Get-ObjectAcl
```

Pero esto va a sacar excesiba informacion, por lo que vamos a filtrarlo por un usuario, por ejemplo `empleado1` el de nuestro equipo:

```powershell
Get-ObjectAcl -SamAccountName empleado1
```

Info:

```
ObjectDN               : CN=empleado1,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-1104
ActiveDirectoryRights  : ReadProperty
ObjectAceFlags         : ObjectAceTypePresent, InheritedObjectAceTypePresent
ObjectAceType          : 4c164200-20c0-11d0-a768-00aa006e0529
InheritedObjectAceType : 4828cc14-1437-45bc-9b07-ad6f015e5f28
BinaryLength           : 60
AceQualifier           : AccessAllowed
IsCallback             : False
OpaqueLength           : 0
AccessMask             : 16
SecurityIdentifier     : S-1-5-32-554
AceType                : AccessAllowedObject
AceFlags               : None
IsInherited            : False
InheritanceFlags       : None
PropagationFlags       : None
AuditFlags             : None

ObjectDN               : CN=empleado1,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-1104
ActiveDirectoryRights  : ReadProperty
ObjectAceFlags         : ObjectAceTypePresent, InheritedObjectAceTypePresent
ObjectAceType          : 4c164200-20c0-11d0-a768-00aa006e0529
InheritedObjectAceType : bf967aba-0de6-11d0-a285-00aa003049e2
BinaryLength           : 60
AceQualifier           : AccessAllowed
IsCallback             : False
OpaqueLength           : 0
AccessMask             : 16
SecurityIdentifier     : S-1-5-32-554
AceType                : AccessAllowedObject
AceFlags               : None
IsInherited            : False
InheritanceFlags       : None
PropagationFlags       : None
AuditFlags             : None

ObjectDN               : CN=empleado1,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-1104
ActiveDirectoryRights  : ReadProperty
ObjectAceFlags         : ObjectAceTypePresent, InheritedObjectAceTypePresent
ObjectAceType          : 5f202010-79a5-11d0-9020-00c04fc2d4cf
InheritedObjectAceType : 4828cc14-1437-45bc-9b07-ad6f015e5f28
BinaryLength           : 60
AceQualifier           : AccessAllowed
IsCallback             : False
OpaqueLength           : 0
AccessMask             : 16
SecurityIdentifier     : S-1-5-32-554
AceType                : AccessAllowedObject
AceFlags               : None
IsInherited            : False
InheritanceFlags       : None
PropagationFlags       : None
AuditFlags             : None

ObjectDN               : CN=empleado1,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-1104
ActiveDirectoryRights  : ReadProperty
ObjectAceFlags         : ObjectAceTypePresent, InheritedObjectAceTypePresent
ObjectAceType          : 5f202010-79a5-11d0-9020-00c04fc2d4cf
InheritedObjectAceType : bf967aba-0de6-11d0-a285-00aa003049e2
BinaryLength           : 60
AceQualifier           : AccessAllowed
IsCallback             : False
OpaqueLength           : 0
AccessMask             : 16
SecurityIdentifier     : S-1-5-32-554
AceType                : AccessAllowedObject
AceFlags               : None
IsInherited            : False
InheritanceFlags       : None
PropagationFlags       : None
AuditFlags             : None

ObjectDN               : CN=empleado1,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-1104
ActiveDirectoryRights  : ReadProperty
ObjectAceFlags         : ObjectAceTypePresent, InheritedObjectAceTypePresent
ObjectAceType          : bc0ac240-79a9-11d0-9020-00c04fc2d4cf
InheritedObjectAceType : 4828cc14-1437-45bc-9b07-ad6f015e5f28
BinaryLength           : 60
AceQualifier           : AccessAllowed
IsCallback             : False
OpaqueLength           : 0
AccessMask             : 16
SecurityIdentifier     : S-1-5-32-554
AceType                : AccessAllowedObject
AceFlags               : None
IsInherited            : False
InheritanceFlags       : None
PropagationFlags       : None
AuditFlags             : None

ObjectDN               : CN=empleado1,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-1104
ActiveDirectoryRights  : ReadProperty
ObjectAceFlags         : ObjectAceTypePresent, InheritedObjectAceTypePresent
ObjectAceType          : bc0ac240-79a9-11d0-9020-00c04fc2d4cf
InheritedObjectAceType : bf967aba-0de6-11d0-a285-00aa003049e2
BinaryLength           : 60
AceQualifier           : AccessAllowed
IsCallback             : False
OpaqueLength           : 0
AccessMask             : 16
SecurityIdentifier     : S-1-5-32-554
AceType                : AccessAllowedObject
AceFlags               : None
IsInherited            : False
InheritanceFlags       : None
PropagationFlags       : None
AuditFlags             : None

ObjectDN               : CN=empleado1,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-1104
ActiveDirectoryRights  : ReadProperty
ObjectAceFlags         : ObjectAceTypePresent, InheritedObjectAceTypePresent
ObjectAceType          : 59ba2f42-79a2-11d0-9020-00c04fc2d3cf
InheritedObjectAceType : 4828cc14-1437-45bc-9b07-ad6f015e5f28
BinaryLength           : 60
AceQualifier           : AccessAllowed
IsCallback             : False
OpaqueLength           : 0
AccessMask             : 16
SecurityIdentifier     : S-1-5-32-554
AceType                : AccessAllowedObject
AceFlags               : None
IsInherited            : False
InheritanceFlags       : None
PropagationFlags       : None
AuditFlags             : None

ObjectDN               : CN=empleado1,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-1104
ActiveDirectoryRights  : ReadProperty
ObjectAceFlags         : ObjectAceTypePresent, InheritedObjectAceTypePresent
ObjectAceType          : 59ba2f42-79a2-11d0-9020-00c04fc2d3cf
InheritedObjectAceType : bf967aba-0de6-11d0-a285-00aa003049e2
BinaryLength           : 60
AceQualifier           : AccessAllowed
IsCallback             : False
OpaqueLength           : 0
AccessMask             : 16
SecurityIdentifier     : S-1-5-32-554
AceType                : AccessAllowedObject
AceFlags               : None
IsInherited            : False
InheritanceFlags       : None
PropagationFlags       : None
AuditFlags             : None

ObjectDN               : CN=empleado1,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-1104
ActiveDirectoryRights  : ReadProperty
ObjectAceFlags         : ObjectAceTypePresent, InheritedObjectAceTypePresent
ObjectAceType          : 037088f8-0ae1-11d2-b422-00a0c968f939
InheritedObjectAceType : 4828cc14-1437-45bc-9b07-ad6f015e5f28
BinaryLength           : 60
AceQualifier           : AccessAllowed
IsCallback             : False
OpaqueLength           : 0
AccessMask             : 16
SecurityIdentifier     : S-1-5-32-554
AceType                : AccessAllowedObject
AceFlags               : None
IsInherited            : False
InheritanceFlags       : None
PropagationFlags       : None
AuditFlags             : None

ObjectDN               : CN=empleado1,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-1104
ActiveDirectoryRights  : ReadProperty
ObjectAceFlags         : ObjectAceTypePresent, InheritedObjectAceTypePresent
ObjectAceType          : 037088f8-0ae1-11d2-b422-00a0c968f939
InheritedObjectAceType : bf967aba-0de6-11d0-a285-00aa003049e2
BinaryLength           : 60
AceQualifier           : AccessAllowed
IsCallback             : False
OpaqueLength           : 0
AccessMask             : 16
SecurityIdentifier     : S-1-5-32-554
AceType                : AccessAllowedObject
AceFlags               : None
IsInherited            : False
InheritanceFlags       : None
PropagationFlags       : None
AuditFlags             : None

ObjectDN               : CN=empleado1,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-1104
ActiveDirectoryRights  : ReadProperty, WriteProperty
ObjectAceFlags         : ObjectAceTypePresent
ObjectAceType          : bf967a7f-0de6-11d0-a285-00aa003049e2
InheritedObjectAceType : 00000000-0000-0000-0000-000000000000
BinaryLength           : 56
AceQualifier           : AccessAllowed
IsCallback             : False
OpaqueLength           : 0
AccessMask             : 48
SecurityIdentifier     : S-1-5-21-3352250647-938130414-2449934813-517
AceType                : AccessAllowedObject
AceFlags               : None
IsInherited            : False
InheritanceFlags       : None
PropagationFlags       : None
AuditFlags             : None

ObjectDN               : CN=empleado1,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-1104
ActiveDirectoryRights  : ReadProperty
ObjectAceFlags         : ObjectAceTypePresent
ObjectAceType          : 46a9b11d-60ae-405a-b7e8-ff8a58d456d2
InheritedObjectAceType : 00000000-0000-0000-0000-000000000000
BinaryLength           : 44
AceQualifier           : AccessAllowed
IsCallback             : False
OpaqueLength           : 0
AccessMask             : 16
SecurityIdentifier     : S-1-5-32-560
AceType                : AccessAllowedObject
AceFlags               : None
IsInherited            : False
InheritanceFlags       : None
PropagationFlags       : None
AuditFlags             : None

ObjectDN               : CN=empleado1,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-1104
ActiveDirectoryRights  : ReadProperty, WriteProperty
ObjectAceFlags         : ObjectAceTypePresent
ObjectAceType          : 6db69a1c-9422-11d1-aebd-0000f80367c1
InheritedObjectAceType : 00000000-0000-0000-0000-000000000000
BinaryLength           : 44
AceQualifier           : AccessAllowed
IsCallback             : False
OpaqueLength           : 0
AccessMask             : 48
SecurityIdentifier     : S-1-5-32-561
AceType                : AccessAllowedObject
AceFlags               : None
IsInherited            : False
InheritanceFlags       : None
PropagationFlags       : None
AuditFlags             : None

ObjectDN               : CN=empleado1,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-1104
ActiveDirectoryRights  : ReadProperty, WriteProperty
ObjectAceFlags         : ObjectAceTypePresent
ObjectAceType          : 5805bc62-bdc9-4428-a5e2-856a0f4c185e
InheritedObjectAceType : 00000000-0000-0000-0000-000000000000
BinaryLength           : 44
AceQualifier           : AccessAllowed
IsCallback             : False
OpaqueLength           : 0
AccessMask             : 48
SecurityIdentifier     : S-1-5-32-561
AceType                : AccessAllowedObject
AceFlags               : None
IsInherited            : False
InheritanceFlags       : None
PropagationFlags       : None
AuditFlags             : None

ObjectDN               : CN=empleado1,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-1104
ActiveDirectoryRights  : GenericRead
ObjectAceFlags         : InheritedObjectAceTypePresent
ObjectAceType          : 00000000-0000-0000-0000-000000000000
InheritedObjectAceType : 4828cc14-1437-45bc-9b07-ad6f015e5f28
BinaryLength           : 44
AceQualifier           : AccessAllowed
IsCallback             : False
OpaqueLength           : 0
AccessMask             : 131220
SecurityIdentifier     : S-1-5-32-554
AceType                : AccessAllowedObject
AceFlags               : None
IsInherited            : False
InheritanceFlags       : None
PropagationFlags       : None
AuditFlags             : None

ObjectDN               : CN=empleado1,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-1104
ActiveDirectoryRights  : GenericRead
ObjectAceFlags         : InheritedObjectAceTypePresent
ObjectAceType          : 00000000-0000-0000-0000-000000000000
InheritedObjectAceType : bf967aba-0de6-11d0-a285-00aa003049e2
BinaryLength           : 44
AceQualifier           : AccessAllowed
IsCallback             : False
OpaqueLength           : 0
AccessMask             : 131220
SecurityIdentifier     : S-1-5-32-554
AceType                : AccessAllowedObject
AceFlags               : None
IsInherited            : False
InheritanceFlags       : None
PropagationFlags       : None
AuditFlags             : None

ObjectDN               : CN=empleado1,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-1104
ActiveDirectoryRights  : ExtendedRight
ObjectAceFlags         : ObjectAceTypePresent
ObjectAceType          : ab721a53-1e2f-11d0-9819-00aa0040529b
InheritedObjectAceType : 00000000-0000-0000-0000-000000000000
BinaryLength           : 40
AceQualifier           : AccessAllowed
IsCallback             : False
OpaqueLength           : 0
AccessMask             : 256
SecurityIdentifier     : S-1-1-0
AceType                : AccessAllowedObject
AceFlags               : None
IsInherited            : False
InheritanceFlags       : None
PropagationFlags       : None
AuditFlags             : None

ObjectDN               : CN=empleado1,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-1104
ActiveDirectoryRights  : ExtendedRight
ObjectAceFlags         : ObjectAceTypePresent
ObjectAceType          : ab721a53-1e2f-11d0-9819-00aa0040529b
InheritedObjectAceType : 00000000-0000-0000-0000-000000000000
BinaryLength           : 40
AceQualifier           : AccessAllowed
IsCallback             : False
OpaqueLength           : 0
AccessMask             : 256
SecurityIdentifier     : S-1-5-10
AceType                : AccessAllowedObject
AceFlags               : None
IsInherited            : False
InheritanceFlags       : None
PropagationFlags       : None
AuditFlags             : None

ObjectDN               : CN=empleado1,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-1104
ActiveDirectoryRights  : ReadProperty, WriteProperty, ExtendedRight
ObjectAceFlags         : ObjectAceTypePresent
ObjectAceType          : 91e647de-d96f-4b70-9557-d63ff4f3ccd8
InheritedObjectAceType : 00000000-0000-0000-0000-000000000000
BinaryLength           : 40
AceQualifier           : AccessAllowed
IsCallback             : False
OpaqueLength           : 0
AccessMask             : 304
SecurityIdentifier     : S-1-5-10
AceType                : AccessAllowedObject
AceFlags               : ContainerInherit
IsInherited            : False
InheritanceFlags       : ContainerInherit
PropagationFlags       : None
AuditFlags             : None

ObjectDN              : CN=empleado1,CN=Users,DC=corp,DC=local
ObjectSID             : S-1-5-21-3352250647-938130414-2449934813-1104
ActiveDirectoryRights : CreateChild, DeleteChild, Self, WriteProperty, ExtendedRight, GenericRead, WriteDacl,
                        WriteOwner
BinaryLength          : 36
AceQualifier          : AccessAllowed
IsCallback            : False
OpaqueLength          : 0
AccessMask            : 917951
SecurityIdentifier    : S-1-5-21-3352250647-938130414-2449934813-512
AceType               : AccessAllowed
AceFlags              : None
IsInherited           : False
InheritanceFlags      : None
PropagationFlags      : None
AuditFlags            : None

ObjectDN              : CN=empleado1,CN=Users,DC=corp,DC=local
ObjectSID             : S-1-5-21-3352250647-938130414-2449934813-1104
ActiveDirectoryRights : CreateChild, DeleteChild, Self, WriteProperty, ExtendedRight, GenericRead, WriteDacl,
                        WriteOwner
BinaryLength          : 36
AceQualifier          : AccessAllowed
IsCallback            : False
OpaqueLength          : 0
AccessMask            : 917951
SecurityIdentifier    : S-1-5-21-3352250647-938130414-2449934813-519
AceType               : AccessAllowed
AceFlags              : None
IsInherited           : False
InheritanceFlags      : None
PropagationFlags      : None
AuditFlags            : None

ObjectDN              : CN=empleado1,CN=Users,DC=corp,DC=local
ObjectSID             : S-1-5-21-3352250647-938130414-2449934813-1104
ActiveDirectoryRights : CreateChild, DeleteChild, Self, WriteProperty, ExtendedRight, Delete, GenericRead, WriteDacl,
                        WriteOwner
BinaryLength          : 24
AceQualifier          : AccessAllowed
IsCallback            : False
OpaqueLength          : 0
AccessMask            : 983487
SecurityIdentifier    : S-1-5-32-544
AceType               : AccessAllowed
AceFlags              : None
IsInherited           : False
InheritanceFlags      : None
PropagationFlags      : None
AuditFlags            : None

ObjectDN              : CN=empleado1,CN=Users,DC=corp,DC=local
ObjectSID             : S-1-5-21-3352250647-938130414-2449934813-1104
ActiveDirectoryRights : GenericRead
BinaryLength          : 20
AceQualifier          : AccessAllowed
IsCallback            : False
OpaqueLength          : 0
AccessMask            : 131220
SecurityIdentifier    : S-1-5-11
AceType               : AccessAllowed
AceFlags              : None
IsInherited           : False
InheritanceFlags      : None
PropagationFlags      : None
AuditFlags            : None

ObjectDN              : CN=empleado1,CN=Users,DC=corp,DC=local
ObjectSID             : S-1-5-21-3352250647-938130414-2449934813-1104
ActiveDirectoryRights : GenericAll
BinaryLength          : 20
AceQualifier          : AccessAllowed
IsCallback            : False
OpaqueLength          : 0
AccessMask            : 983551
SecurityIdentifier    : S-1-5-18
AceType               : AccessAllowed
AceFlags              : None
IsInherited           : False
InheritanceFlags      : None
PropagationFlags      : None
AuditFlags            : None
```

Esto tiene muchisima relevancia mas adelante el poder identificar esto, pero mas adelante lo veremos con mas profundidad.

### Enumerar Forest's

Tambien podemos enumerar los `Forest's`:

```powershell
Get-NetForestDomain
```

Info:

```
Forest                  : corp.local
DomainControllers       : {DC01.corp.local}
Children                : {}
DomainMode              : Unknown
DomainModeLevel         : 7
Parent                  :
PdcRoleOwner            : DC01.corp.local
RidRoleOwner            : DC01.corp.local
InfrastructureRoleOwner : DC01.corp.local
Name                    : corp.local
```

### Enumerar administradores locales de equipos

Con el siguiente comando podremos hacer multiples peticiones en el dominio para poder identificar en todas las maquinas que encuentre un administrador local:

```powershell
Find-LocalAdminAccess -Verbose
```

Info:

```
DETALLADO: [Find-LocalAdminAccess] Querying computers in the domain
DETALLADO: [Get-DomainSearcher] search base: LDAP://DC01.CORP.LOCAL/DC=CORP,DC=LOCAL
DETALLADO: [Get-DomainComputer] Get-DomainComputer filter string: (&(samAccountType=805306369))
DETALLADO: [Find-LocalAdminAccess] TargetComputers length: 3
DETALLADO: [Find-LocalAdminAccess] Using threading with threads: 20
DETALLADO: [New-ThreadedFunction] Total number of hosts: 3
DETALLADO: [New-ThreadedFunction] Total number of threads/partitions: 3
DETALLADO: [New-ThreadedFunction] Threads executing
DETALLADO: [New-ThreadedFunction] Waiting 100 seconds for final cleanup...
```

Por lo que vemos no encontro nada, ya que este usuario no tiene privilegios de administrador a nivel local en ningun otro equipo.

Si queremos enumerar usuarios administradores locales en diferentes equipos, podremos hacerlos asi:

```powershell
Invoke-EnumerateLocalAdmin -Verbose
```

Info:

```
DETALLADO: [Find-DomainLocalGroupMember] Querying computers in the domain
DETALLADO: [Get-DomainSearcher] search base: LDAP://DC01.CORP.LOCAL/DC=CORP,DC=LOCAL
DETALLADO: [Get-DomainComputer] Get-DomainComputer filter string: (&(samAccountType=805306369))
DETALLADO: [Find-DomainLocalGroupMember] TargetComputers length: 3
DETALLADO: [Find-DomainLocalGroupMember] Using threading with threads: 20
DETALLADO: [New-ThreadedFunction] Total number of hosts: 3
DETALLADO: [New-ThreadedFunction] Total number of threads/partitions: 3
DETALLADO: [New-ThreadedFunction] Threads executing
DETALLADO: [New-ThreadedFunction] Waiting 100 seconds for final cleanup...


ComputerName : WS01.corp.local
GroupName    : Administradores
MemberName   : WS01\Administrador
SID          : S-1-5-21-1345059704-770646112-4146140408-500
IsGroup      : False
IsDomain     : False

ComputerName : WS01.corp.local
GroupName    : Administradores
MemberName   : WS01\santiago
SID          : S-1-5-21-1345059704-770646112-4146140408-1001
IsGroup      : False
IsDomain     : False

ComputerName : WS01.corp.local
GroupName    : Administradores
MemberName   : CORP\Domain Admins
SID          : S-1-5-21-3352250647-938130414-2449934813-512
IsGroup      : True
IsDomain     : True
```

Para buscar sesion de algun usuario que pertenezca al `RDPUsers` se podra hacer asi:

```powershell
Invoke-UserHunter -GroupName "RDPUsers"
```

Pero en este caso no nos encontrara nada ya que no hay ningun usuario en ese grupo.
