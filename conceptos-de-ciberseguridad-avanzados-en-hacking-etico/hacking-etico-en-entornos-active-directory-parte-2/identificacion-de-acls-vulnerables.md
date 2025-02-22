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

# Identificación de ACLs vulnerables

Primero para poder explotar las `ACLs` tendremos que identificar cuales pueden ser vulnerables para poder ser explotadas:

> Listado de `ACLs` vulnerables

A continuación os indico un listado de `ACEs` que debemos tener en cuenta desde el punto de vista de seguridad de cara a su explotación:

* **ForceChangePassword**: Proporciona la capacidad de cambiar la contraseña del usuario objetivo sin conocer el valor actual. Abusado con `Set-DomainUserPassword`
* **AddMembers**: Proporciona la capacidad de añadir usuarios, grupos o equipos arbitrarios al grupo de destino. Abusado con `Add-DomainGroupMember`
* **GenericAll**: Proporciona control total del objeto, incluyendo la capacidad de añadir otros usuarios a un grupo, cambiar una contraseña de usuario sin conocer su valor actual, registrar un SPN con un objeto de usuario, etc. Abusado con `Set-DomainUserPassword` o `Add-DomainGroupMember`
* **GenericWrite**: Proporciona la capacidad de actualizar cualquier valor de parámetro de objeto de destino no protegido. Por ejemplo, actualizar el valor del parámetro "scriptPath" en un objeto de usuario de destino para hacer que ese usuario ejecute los comandos/ejecutables especificados la próxima vez que se conecte. Abusado con `Set-DomainObject`
* **WriteOwner**: Proporciona la capacidad de actualizar el propietario del objeto de destino. Una vez que el propietario del objeto ha sido cambiado a un usuario que el atacante controla, el atacante puede manipular el objeto de la manera que crea conveniente. Abusado con `Set-DomainObjectOwner`
* **WriteDACL**: Proporciona la capacidad de escribir una nueva ACE en la DACL del objeto objetivo. Por ejemplo, un atacante puede escribir una nueva ACE en la DACL del objeto de destino, dándole el "control total" del objeto de destino. Abusado con `Add-NewADObjectAccessControlEntry`
* **AllExtendedRights**: Proporciona la capacidad de realizar cualquier acción asociada con los derechos extendidos de Active Directory contra el objeto. Por ejemplo, añadir usuarios a un grupo y forzar el cambio de la contraseña de un usuario de destino. Se abusa con `Set-DomainUserPassword` o `Add-DomainGroupMember`

Por supuesto, esta no es la lista completa de `ACEs` que pueden vulnerarse, existen decenas de permisos que bajo ciertas circunstancias también pueden llegar a ser explotados.

Ahora que nosotros tenemos un entorno mas realista en nuestro `DC` con muchisimas `DACLs`, `ACLs`, usuarios, grupos, etc... Si nosotros con `PowerView` intentamos enumerar como haciamos anteriormente vamos a ver que es un locura la de informacion que nos porpociona, por lo que no es muy factible utilizarlo sin filtros, por lo que vamos hacer lo siguiente:

```powershell
cd .\Desktop\
. .\new_powerview.ps1
```

Una vez que tengamos cargado el `PowerView` vamos a añadir filtros para listas todos los grupos y elegir el que nos interese, de ahi podremos elegir un `target` para poder atacarlo.

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
                         GLOBAL_SCOPE, SECURITY Office Admin
                         GLOBAL_SCOPE, SECURITY IT Admins
                         GLOBAL_SCOPE, SECURITY Executives
                         GLOBAL_SCOPE, SECURITY Senior management
                         GLOBAL_SCOPE, SECURITY Project management
                         GLOBAL_SCOPE, SECURITY marketing
                         GLOBAL_SCOPE, SECURITY sales
                         GLOBAL_SCOPE, SECURITY accounting
```

Vemos varios interesantes y los que mas nos interesan son los grupos en los que lleve la palabra `admins`, pero el mas importante de todos es el de `admins. del dominio` por lo que vamos a ver que `DACLs` tiene incorporado dicho grupo para asi poder saber si es vulnerable por alguna mala configuracion o no.

```powershell
Get-DomainObjectAcl -Identity "Domain Admins"
```

Info:

```
ObjectDN               : CN=Domain Admins,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-512
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

ObjectDN               : CN=Domain Admins,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-512
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

ObjectDN               : CN=Domain Admins,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-512
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

ObjectDN               : CN=Domain Admins,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-512
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

ObjectDN               : CN=Domain Admins,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-512
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

ObjectDN               : CN=Domain Admins,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-512
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

ObjectDN               : CN=Domain Admins,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-512
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

ObjectDN               : CN=Domain Admins,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-512
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

ObjectDN               : CN=Domain Admins,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-512
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

ObjectDN               : CN=Domain Admins,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-512
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

ObjectDN               : CN=Domain Admins,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-512
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

ObjectDN               : CN=Domain Admins,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-512
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

ObjectDN               : CN=Domain Admins,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-512
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

ObjectDN               : CN=Domain Admins,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-512
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

ObjectDN               : CN=Domain Admins,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-512
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

ObjectDN               : CN=Domain Admins,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-512
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

ObjectDN               : CN=Domain Admins,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-512
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

ObjectDN               : CN=Domain Admins,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-512
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

ObjectDN               : CN=Domain Admins,CN=Users,DC=corp,DC=local
ObjectSID              : S-1-5-21-3352250647-938130414-2449934813-512
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

ObjectDN              : CN=Domain Admins,CN=Users,DC=corp,DC=local
ObjectSID             : S-1-5-21-3352250647-938130414-2449934813-512
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

ObjectDN              : CN=Domain Admins,CN=Users,DC=corp,DC=local
ObjectSID             : S-1-5-21-3352250647-938130414-2449934813-512
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

ObjectDN              : CN=Domain Admins,CN=Users,DC=corp,DC=local
ObjectSID             : S-1-5-21-3352250647-938130414-2449934813-512
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

ObjectDN              : CN=Domain Admins,CN=Users,DC=corp,DC=local
ObjectSID             : S-1-5-21-3352250647-938130414-2449934813-512
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

ObjectDN              : CN=Domain Admins,CN=Users,DC=corp,DC=local
ObjectSID             : S-1-5-21-3352250647-938130414-2449934813-512
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

Vemos que nos vuelca todos las `ACLs` de dicho grupo, podremos ir mirando cual es cada una con el `SID` de cada uno de ellos traduciendolo de la siguiente forma, por ejemplo si quiero ver que significa este `SID` del ultimo `ACL` podremos hacerlo asi:

```powershell
Convert-SidToName S-1-5-21-3352250647-938130414-2449934813-512
```

Info:

```
CORP\Domain Admins
```

Por lo que vemos es de `CORP\Domain Admins` y vemos que pertenece a `GenericAll` que es uno de los que nos interesaba, tiene el acceso en `AccessAllowed` y su `SecurityIdentifier` traducido seria:

```powershell
Convert-SidToName S-1-5-18
```

Info:

```
Local System
```

Por lo que vemos ya hemos sacado bastante informaicon de una `ACL`, esto seria ir viendo una por una, cual es la mas optima para poder escalar privilegios o cual tuviera alguna mala configuracion.

Pero si queremos filtrar para que todo se vea de mejor forma, podremos hacerlo de la siguiente forma:

```powershell
Get-DomainObjectAcl -Identity "Domain Admins" | select SecurityIdentifier,AceType,ActiveDirectoryRights | fl
```

Info:

```
SecurityIdentifier    : S-1-5-32-554
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty

SecurityIdentifier    : S-1-5-32-554
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty

SecurityIdentifier    : S-1-5-32-554
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty

SecurityIdentifier    : S-1-5-32-554
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty

SecurityIdentifier    : S-1-5-32-554
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty

SecurityIdentifier    : S-1-5-32-554
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty

SecurityIdentifier    : S-1-5-32-554
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty

SecurityIdentifier    : S-1-5-32-554
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty

SecurityIdentifier    : S-1-5-32-554
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty

SecurityIdentifier    : S-1-5-32-554
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty

SecurityIdentifier    : S-1-5-21-3352250647-938130414-2449934813-517
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty, WriteProperty

SecurityIdentifier    : S-1-5-32-560
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty

SecurityIdentifier    : S-1-5-32-561
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty, WriteProperty

SecurityIdentifier    : S-1-5-32-561
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty, WriteProperty

SecurityIdentifier    : S-1-5-32-554
AceType               : AccessAllowedObject
ActiveDirectoryRights : GenericRead

SecurityIdentifier    : S-1-5-32-554
AceType               : AccessAllowedObject
ActiveDirectoryRights : GenericRead

SecurityIdentifier    : S-1-1-0
AceType               : AccessAllowedObject
ActiveDirectoryRights : ExtendedRight

SecurityIdentifier    : S-1-5-10
AceType               : AccessAllowedObject
ActiveDirectoryRights : ExtendedRight

SecurityIdentifier    : S-1-5-10
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty, WriteProperty, ExtendedRight

SecurityIdentifier    : S-1-5-21-3352250647-938130414-2449934813-512
AceType               : AccessAllowed
ActiveDirectoryRights : CreateChild, DeleteChild, Self, WriteProperty, ExtendedRight, GenericRead, WriteDacl,
                        WriteOwner

SecurityIdentifier    : S-1-5-21-3352250647-938130414-2449934813-519
AceType               : AccessAllowed
ActiveDirectoryRights : CreateChild, DeleteChild, Self, WriteProperty, ExtendedRight, GenericRead, WriteDacl,
                        WriteOwner

SecurityIdentifier    : S-1-5-32-544
AceType               : AccessAllowed
ActiveDirectoryRights : CreateChild, DeleteChild, Self, WriteProperty, ExtendedRight, Delete, GenericRead, WriteDacl,
                        WriteOwner

SecurityIdentifier    : S-1-5-11
AceType               : AccessAllowed
ActiveDirectoryRights : GenericRead

SecurityIdentifier    : S-1-5-18
AceType               : AccessAllowed
ActiveDirectoryRights : GenericAll
```

Pero si no queremos verlo como `SID` y queremos verlo como nombre podremos traducirlo directamente con el siguiente comando:

```powershell
Get-DomainObjectAcl -Identity "Domain Admins" | select @{name="Name";expression={Convert-SidToName $_.SecurityIdentifier}},AceType,ActiveDirectoryRights | fl
```

Info:

```
Name                  : BUILTIN\Pre-Windows 2000 Compatible Access
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty

Name                  : BUILTIN\Pre-Windows 2000 Compatible Access
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty

Name                  : BUILTIN\Pre-Windows 2000 Compatible Access
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty

Name                  : BUILTIN\Pre-Windows 2000 Compatible Access
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty

Name                  : BUILTIN\Pre-Windows 2000 Compatible Access
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty

Name                  : BUILTIN\Pre-Windows 2000 Compatible Access
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty

Name                  : BUILTIN\Pre-Windows 2000 Compatible Access
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty

Name                  : BUILTIN\Pre-Windows 2000 Compatible Access
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty

Name                  : BUILTIN\Pre-Windows 2000 Compatible Access
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty

Name                  : BUILTIN\Pre-Windows 2000 Compatible Access
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty

Name                  : CORP\Cert Publishers
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty, WriteProperty

Name                  : BUILTIN\Windows Authorization Access Group
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty

Name                  : BUILTIN\Terminal Server License Servers
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty, WriteProperty

Name                  : BUILTIN\Terminal Server License Servers
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty, WriteProperty

Name                  : BUILTIN\Pre-Windows 2000 Compatible Access
AceType               : AccessAllowedObject
ActiveDirectoryRights : GenericRead

Name                  : BUILTIN\Pre-Windows 2000 Compatible Access
AceType               : AccessAllowedObject
ActiveDirectoryRights : GenericRead

Name                  : Everyone
AceType               : AccessAllowedObject
ActiveDirectoryRights : ExtendedRight

Name                  : Principal Self
AceType               : AccessAllowedObject
ActiveDirectoryRights : ExtendedRight

Name                  : Principal Self
AceType               : AccessAllowedObject
ActiveDirectoryRights : ReadProperty, WriteProperty, ExtendedRight

Name                  : CORP\Domain Admins
AceType               : AccessAllowed
ActiveDirectoryRights : CreateChild, DeleteChild, Self, WriteProperty, ExtendedRight, GenericRead, WriteDacl,
                        WriteOwner

Name                  : CORP\Enterprise Admins
AceType               : AccessAllowed
ActiveDirectoryRights : CreateChild, DeleteChild, Self, WriteProperty, ExtendedRight, GenericRead, WriteDacl,
                        WriteOwner

Name                  : BUILTIN\Administrators
AceType               : AccessAllowed
ActiveDirectoryRights : CreateChild, DeleteChild, Self, WriteProperty, ExtendedRight, Delete, GenericRead, WriteDacl,
                        WriteOwner

Name                  : Authenticated Users
AceType               : AccessAllowed
ActiveDirectoryRights : GenericRead

Name                  : Local System
AceType               : AccessAllowed
ActiveDirectoryRights : GenericAll
```

Si queremos realizar un escaneo de todas las `ACLs` que tenemos dentro de nuestro dominio filtrandolo por la informacion importante, pero nos muestra aquellas que tienen un valor mayor a `1000` que lo que significa es que esta `DACL` se ha creado despues, por lo que no es una por defecto, es una que haya creado un `administrador` lo que puede significar que pueda tener una mala configuracion o algo parecido.

```powershell
Invoke-ACLScanner -ResolveGUIDs | select IdentityReferenceName,ObjectDN,ActiveDirectoryRights | fl
```

Info:

```
IdentityReferenceName : lonnie.betti
ObjectDN              : DC=corp,DC=local
ActiveDirectoryRights : ExtendedRight

IdentityReferenceName : angelika.shelly
ObjectDN              : DC=corp,DC=local
ActiveDirectoryRights : ExtendedRight

IdentityReferenceName : cynthie.rori
ObjectDN              : DC=corp,DC=local
ActiveDirectoryRights : ExtendedRight

IdentityReferenceName : lonnie.betti
ObjectDN              : DC=corp,DC=local
ActiveDirectoryRights : ExtendedRight

IdentityReferenceName : angelika.shelly
ObjectDN              : DC=corp,DC=local
ActiveDirectoryRights : ExtendedRight

IdentityReferenceName : cynthie.rori
ObjectDN              : DC=corp,DC=local
ActiveDirectoryRights : ExtendedRight

IdentityReferenceName : lonnie.betti
ObjectDN              : DC=corp,DC=local
ActiveDirectoryRights : ExtendedRight

IdentityReferenceName : angelika.shelly
ObjectDN              : DC=corp,DC=local
ActiveDirectoryRights : ExtendedRight

IdentityReferenceName : cynthie.rori
ObjectDN              : DC=corp,DC=local
ActiveDirectoryRights : ExtendedRight

IdentityReferenceName : DnsAdmins
ObjectDN              : DC=RootDNSServers,CN=MicrosoftDNS,CN=System,DC=corp,DC=local
ActiveDirectoryRights : CreateChild, DeleteChild, ListChildren, ReadProperty, DeleteTree, ExtendedRight, Delete,
                        GenericWrite, WriteDacl, WriteOwner

IdentityReferenceName : DnsAdmins
ObjectDN              : DC=@,DC=RootDNSServers,CN=MicrosoftDNS,CN=System,DC=corp,DC=local
ActiveDirectoryRights : CreateChild, DeleteChild, ListChildren, ReadProperty, DeleteTree, ExtendedRight, Delete,
                        GenericWrite, WriteDacl, WriteOwner

IdentityReferenceName : DnsAdmins
ObjectDN              : DC=A.ROOT-SERVERS.NET,DC=RootDNSServers,CN=MicrosoftDNS,CN=System,DC=corp,DC=local
ActiveDirectoryRights : CreateChild, DeleteChild, ListChildren, ReadProperty, DeleteTree, ExtendedRight, Delete,
                        GenericWrite, WriteDacl, WriteOwner

IdentityReferenceName : DnsAdmins
ObjectDN              : DC=B.ROOT-SERVERS.NET,DC=RootDNSServers,CN=MicrosoftDNS,CN=System,DC=corp,DC=local
ActiveDirectoryRights : CreateChild, DeleteChild, ListChildren, ReadProperty, DeleteTree, ExtendedRight, Delete,
                        GenericWrite, WriteDacl, WriteOwner

IdentityReferenceName : DnsAdmins
ObjectDN              : DC=C.ROOT-SERVERS.NET,DC=RootDNSServers,CN=MicrosoftDNS,CN=System,DC=corp,DC=local
ActiveDirectoryRights : CreateChild, DeleteChild, ListChildren, ReadProperty, DeleteTree, ExtendedRight, Delete,
                        GenericWrite, WriteDacl, WriteOwner

IdentityReferenceName : DnsAdmins
ObjectDN              : DC=D.ROOT-SERVERS.NET,DC=RootDNSServers,CN=MicrosoftDNS,CN=System,DC=corp,DC=local
ActiveDirectoryRights : CreateChild, DeleteChild, ListChildren, ReadProperty, DeleteTree, ExtendedRight, Delete,
                        GenericWrite, WriteDacl, WriteOwner

IdentityReferenceName : DnsAdmins
ObjectDN              : DC=E.ROOT-SERVERS.NET,DC=RootDNSServers,CN=MicrosoftDNS,CN=System,DC=corp,DC=local
ActiveDirectoryRights : CreateChild, DeleteChild, ListChildren, ReadProperty, DeleteTree, ExtendedRight, Delete,
                        GenericWrite, WriteDacl, WriteOwner

IdentityReferenceName : DnsAdmins
ObjectDN              : DC=F.ROOT-SERVERS.NET,DC=RootDNSServers,CN=MicrosoftDNS,CN=System,DC=corp,DC=local
ActiveDirectoryRights : CreateChild, DeleteChild, ListChildren, ReadProperty, DeleteTree, ExtendedRight, Delete,
                        GenericWrite, WriteDacl, WriteOwner

IdentityReferenceName : DnsAdmins
ObjectDN              : DC=G.ROOT-SERVERS.NET,DC=RootDNSServers,CN=MicrosoftDNS,CN=System,DC=corp,DC=local
ActiveDirectoryRights : CreateChild, DeleteChild, ListChildren, ReadProperty, DeleteTree, ExtendedRight, Delete,
                        GenericWrite, WriteDacl, WriteOwner

IdentityReferenceName : DnsAdmins
ObjectDN              : DC=H.ROOT-SERVERS.NET,DC=RootDNSServers,CN=MicrosoftDNS,CN=System,DC=corp,DC=local
ActiveDirectoryRights : CreateChild, DeleteChild, ListChildren, ReadProperty, DeleteTree, ExtendedRight, Delete,
                        GenericWrite, WriteDacl, WriteOwner

IdentityReferenceName : DnsAdmins
ObjectDN              : DC=I.ROOT-SERVERS.NET,DC=RootDNSServers,CN=MicrosoftDNS,CN=System,DC=corp,DC=local
ActiveDirectoryRights : CreateChild, DeleteChild, ListChildren, ReadProperty, DeleteTree, ExtendedRight, Delete,
                        GenericWrite, WriteDacl, WriteOwner

IdentityReferenceName : DnsAdmins
ObjectDN              : DC=J.ROOT-SERVERS.NET,DC=RootDNSServers,CN=MicrosoftDNS,CN=System,DC=corp,DC=local
ActiveDirectoryRights : CreateChild, DeleteChild, ListChildren, ReadProperty, DeleteTree, ExtendedRight, Delete,
                        GenericWrite, WriteDacl, WriteOwner

IdentityReferenceName : DnsAdmins
ObjectDN              : DC=K.ROOT-SERVERS.NET,DC=RootDNSServers,CN=MicrosoftDNS,CN=System,DC=corp,DC=local
ActiveDirectoryRights : CreateChild, DeleteChild, ListChildren, ReadProperty, DeleteTree, ExtendedRight, Delete,
                        GenericWrite, WriteDacl, WriteOwner

IdentityReferenceName : DnsAdmins
ObjectDN              : DC=L.ROOT-SERVERS.NET,DC=RootDNSServers,CN=MicrosoftDNS,CN=System,DC=corp,DC=local
ActiveDirectoryRights : CreateChild, DeleteChild, ListChildren, ReadProperty, DeleteTree, ExtendedRight, Delete,
                        GenericWrite, WriteDacl, WriteOwner

IdentityReferenceName : DnsAdmins
ObjectDN              : DC=M.ROOT-SERVERS.NET,DC=RootDNSServers,CN=MicrosoftDNS,CN=System,DC=corp,DC=local
ActiveDirectoryRights : CreateChild, DeleteChild, ListChildren, ReadProperty, DeleteTree, ExtendedRight, Delete,
                        GenericWrite, WriteDacl, WriteOwner

IdentityReferenceName : DC01$
ObjectDN              : CN=DFSR-LocalSettings,CN=DC01,OU=Domain Controllers,DC=corp,DC=local
ActiveDirectoryRights : GenericAll

IdentityReferenceName : DC01$
ObjectDN              : CN=Domain System Volume,CN=DFSR-LocalSettings,CN=DC01,OU=Domain Controllers,DC=corp,DC=local
ActiveDirectoryRights : GenericAll

IdentityReferenceName : DC01$
ObjectDN              : CN=SYSVOL Subscription,CN=Domain System Volume,CN=DFSR-LocalSettings,CN=DC01,OU=Domain
                        Controllers,DC=corp,DC=local
ActiveDirectoryRights : GenericAll

IdentityReferenceName : empleado1
ObjectDN              : CN=WS01,CN=Computers,DC=corp,DC=local
ActiveDirectoryRights : WriteProperty

IdentityReferenceName : empleado1
ObjectDN              : CN=WS01,CN=Computers,DC=corp,DC=local
ActiveDirectoryRights : WriteProperty

IdentityReferenceName : empleado1
ObjectDN              : CN=WS01,CN=Computers,DC=corp,DC=local
ActiveDirectoryRights : WriteProperty

IdentityReferenceName : empleado1
ObjectDN              : CN=WS01,CN=Computers,DC=corp,DC=local
ActiveDirectoryRights : WriteProperty

IdentityReferenceName : empleado1
ObjectDN              : CN=WS01,CN=Computers,DC=corp,DC=local
ActiveDirectoryRights : WriteProperty

IdentityReferenceName : empleado1
ObjectDN              : CN=WS01,CN=Computers,DC=corp,DC=local
ActiveDirectoryRights : ExtendedRight, GenericRead

IdentityReferenceName : empleado2
ObjectDN              : CN=WS02,CN=Computers,DC=corp,DC=local
ActiveDirectoryRights : WriteProperty

IdentityReferenceName : empleado2
ObjectDN              : CN=WS02,CN=Computers,DC=corp,DC=local
ActiveDirectoryRights : WriteProperty

IdentityReferenceName : empleado2
ObjectDN              : CN=WS02,CN=Computers,DC=corp,DC=local
ActiveDirectoryRights : WriteProperty

IdentityReferenceName : empleado2
ObjectDN              : CN=WS02,CN=Computers,DC=corp,DC=local
ActiveDirectoryRights : WriteProperty

IdentityReferenceName : empleado2
ObjectDN              : CN=WS02,CN=Computers,DC=corp,DC=local
ActiveDirectoryRights : WriteProperty

IdentityReferenceName : empleado2
ObjectDN              : CN=WS02,CN=Computers,DC=corp,DC=local
ActiveDirectoryRights : ExtendedRight, GenericRead

IdentityReferenceName : marketing
ObjectDN              : CN=Fayina Hyacinth,CN=Users,DC=corp,DC=local
ActiveDirectoryRights : GenericAll

IdentityReferenceName : sales
ObjectDN              : CN=Georgia Marie-Ann,CN=Users,DC=corp,DC=local
ActiveDirectoryRights : WriteDacl

IdentityReferenceName : Senior management
ObjectDN              : CN=Levin Bab,CN=Users,DC=corp,DC=local
ActiveDirectoryRights : WriteOwner

IdentityReferenceName : Project management
ObjectDN              : CN=Geneva Lorrin,CN=Users,DC=corp,DC=local
ActiveDirectoryRights : WriteOwner

IdentityReferenceName : Project management
ObjectDN              : CN=IT Admins,CN=Users,DC=corp,DC=local
ActiveDirectoryRights : WriteOwner

IdentityReferenceName : Senior management
ObjectDN              : CN=IT Admins,CN=Users,DC=corp,DC=local
ActiveDirectoryRights : GenericAll

IdentityReferenceName : Senior management
ObjectDN              : CN=Executives,CN=Users,DC=corp,DC=local
ActiveDirectoryRights : GenericWrite, WriteDacl

IdentityReferenceName : marketing
ObjectDN              : CN=Senior management,CN=Users,DC=corp,DC=local
ActiveDirectoryRights : GenericWrite, WriteDacl

IdentityReferenceName : sales
ObjectDN              : CN=Senior management,CN=Users,DC=corp,DC=local
ActiveDirectoryRights : GenericAll

IdentityReferenceName : sales
ObjectDN              : CN=Project management,CN=Users,DC=corp,DC=local
ActiveDirectoryRights : WriteOwner
```

Pero para no tener que ir en la consola viendo uno por uno todo esto, vamos a utilizar `BloodHound` mejor ya que es mucho mejor para identificar este tipo de cosas, por lo que vamos a volver a cargar el archivo `sh.ps1` y volcar los ficheros nuevamente en el escritorio para pasarlo a nuestro `kali`.

```powershell
. .\sh.ps1
Invoke-BloodHound -CollectionMethod All -OutputDirectory "C:\Users\<USER>\Desktop"
```

Y con esto ya lo habremos generado, ahora el `ZIP` nos lo pasamos a nuestro `kali`.

Por lo que solo tendremos que arrastrar el archivo en el `BloodHound` y estaria listo.

```shell
sudo neo4j console
```

En otra terminal.

```shell
bloodhound
```

Y arrastramos el archivo al `bloodhound`, esto cargara los nuevos archivos de lo que habia anteriormente, por lo que lo actualizaremos.

Ahora vamos a darle a la siguiente opcion en la seccion de `Analysis`:

<figure><img src="../../.gitbook/assets/image (232).png" alt=""><figcaption></figcaption></figure>

Para buscar las rutas mas rapidas para poder ser de dicho grupo y asi poder ser `admins`.

<figure><img src="../../.gitbook/assets/image (233).png" alt=""><figcaption></figcaption></figure>

Vemos algo asi parecido, vemos varias vias por las que tirar para poder ser dicho grupo y ser `admins`.

Si nosotros pulsamos sobre el objeto de `DOMAIN ADMINS` y nos vamos abajo del todo, podremos ver estos 2 apartados:

<figure><img src="../../.gitbook/assets/image (234).png" alt=""><figcaption></figcaption></figure>

El primero es que privilegios tiene este objeto sobre otros objetos de forma muy resumida, que este apartado no viene en el propio `Windows`.

El segundo (`DACL`) es sobre los objetos que tienen control explicito sobre el objeto `DOMAIN ADMINS` y si le damos a `Explicit Object Controllers` de forma grafica nos mostrara cuales son esos objetos.

<figure><img src="../../.gitbook/assets/image (235).png" alt=""><figcaption></figcaption></figure>

Ya con esto podemos ver de todas esas lineas que estamos viendo la informacion de como pueden ser explotadas, por lo que nos facilita mucho mas el trabajo de explotacion, el cual veremos un poco mas adelante.

Si le damos al objeto llamado `ADMINISTRATORS` y le damos a la siguiente opcion.

<figure><img src="../../.gitbook/assets/image (236).png" alt=""><figcaption></figcaption></figure>

Para ver que usuarios tiene dentro de dicho grupo, veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (237).png" alt=""><figcaption></figcaption></figure>

Por lo que vemos aparece el `IT Admins` el cual metimos anteriormente al grupo de `Administradores`, si vemos que usuarios tiene de forma directa:

<figure><img src="../../.gitbook/assets/image (238).png" alt=""><figcaption></figcaption></figure>

Vemos los siguientes, por lo que estos podrian delegar los privilegios de administrador, los cuales nos interesa.
