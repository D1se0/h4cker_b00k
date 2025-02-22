---
icon: container-storage
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

# AD Module

Con estas tecnicas de recopilacion remota nos vamos a enforcar en esa base de datos que tiene el `Domain Controller` que se denomina `NTDS.dir` y para interactuar con ella necesitaremos hacer una llamada remota al `DC` utilizando el protocolo `LDAP`.

Vamos a utilizar un modulo que suele venir en casi todos los soportes de dominio de un servidor, el cual es de forma legitima y no lo va a detectar como malicioso como por ejemplo lo puede hacer `PowerView`, vamos a utilizar el equipo `WS02` para utilizar este modulo y el equipo `WS01` para utilizar `PowerView` y ver las diferencias.

Por ejemplo si nosotros queremos obtener informacion del dominio de forma muy detallada lo podremos hacer con el siguiente comando:

```powershell
Get-ADDomain
```

Pero este comando solo ira en nuestro `DC` ya que cuando se crea el dominio se instala una libreria `.dll` la cual tiene registrado este comando, pero en los equipos normales no lo va a reconocer, por lo que tendremos que obtener esa libreria para poder obetenr la informacion del dominio en un equipo normal.

Si nosotros en el `DC` vamos a la siguiente ruta de carpetas:

```
C:\Windows\Microsoft.NET\assembly\GAC_64\Microsoft.ActiveDirectory.Management\v4.0_10.0.0.0__31bf3856ad364e35\
```

Dentro de esta encontraremos un archivo llamado `Microsoft.ActiveDirectory.Management.dll` que es el que importa dicha libreria para que ese comando anterior funcione.

Por lo que podemos hacer es crear como atacante nosotros un `Windows Server` promocionarlo a un servidor de dominio y obtener esta `.dll` para asi pasarnoslo a nuestro equipo `WS02`.

Una vez que hayamos obtenido el archivo lo pasaremos al escritorio del equipo `WS02`.

Abriremos una `PowerShell`:

```powershell
cd .\Desktop\
Import-Module .\Microsoft.ActiveDirectory.Management.dll
Get-ADDomain
```

Info:

```
DomainSID                          : S-1-5-21-3352250647-938130414-2449934813
AllowedDNSSuffixes                 : {}
LastLogonReplicationInterval       :
DomainMode                         : Windows2016Domain
ManagedBy                          :
LinkedGroupPolicyObjects           : {cn={410CF9DA-E128-4646-B131-688DF0C8538D},cn=policies,cn=system,DC=corp,DC=local,
                                      CN={31B2F340-016D-11D2-945F-00C04FB984F9},CN=Policies,CN=System,DC=corp,DC=local}
ChildDomains                       : {}
ComputersContainer                 : CN=Computers,DC=corp,DC=local
DomainControllersContainer         : OU=Domain Controllers,DC=corp,DC=local
ForeignSecurityPrincipalsContainer : CN=ForeignSecurityPrincipals,DC=corp,DC=local
Forest                             : corp.local
InfrastructureMaster               : DC01.corp.local
NetBIOSName                        : CORP
PDCEmulator                        : DC01.corp.local
ParentDomain                       :
RIDMaster                          : DC01.corp.local
SystemsContainer                   : CN=System,DC=corp,DC=local
UsersContainer                     : CN=Users,DC=corp,DC=local
SubordinateReferences              : {DC=ForestDnsZones,DC=corp,DC=local, DC=DomainDnsZones,DC=corp,DC=local,
                                     CN=Configuration,DC=corp,DC=local}
DNSRoot                            : corp.local
LostAndFoundContainer              : CN=LostAndFound,DC=corp,DC=local
DeletedObjectsContainer            : CN=Deleted Objects,DC=corp,DC=local
QuotasContainer                    : CN=NTDS Quotas,DC=corp,DC=local
ReadOnlyReplicaDirectoryServers    : {}
ReplicaDirectoryServers            : {DC01.corp.local}
DistinguishedName                  : DC=corp,DC=local
Name                               : corp
ObjectClass                        : domainDNS
ObjectGuid                         : a72d122a-d459-40c5-a96b-8ef515bee704
PropertyNames                      : {AllowedDNSSuffixes, ChildDomains, ComputersContainer, DeletedObjectsContainer...}
AddedProperties                    : {}
RemovedProperties                  : {}
ModifiedProperties                 : {PublicKeyRequiredPasswordRolling}
PropertyCount                      : 30
```

Vemos que ahora si nos funciona y nos saca toda la informacion del dominio.

Y esto se estaria haciendo mediante el protocolo `TCP` por lo que pasa desapercibido de una herramienta de seguridad, pero si lo hacemos con `PowerView` en el equipo `WS01` de la siguiente forma:

```powershell
. .\new_powerview.ps1
Get-NetDomain
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

Vamos a ver que se esta haciendo mediante el protocolo `LDAP` y es mas sospechoso por lo que una herramienta de seguridad nos podria detectar.
