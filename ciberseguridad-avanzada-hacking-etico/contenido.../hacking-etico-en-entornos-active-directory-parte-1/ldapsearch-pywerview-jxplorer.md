---
icon: laptop-binary
---

# Ldapsearch, pywerview, jxplorer

Si nosotros por ejemplo obtenemos las credenciales de un usuario de dominio por ejemplo del equipo `WS01` o `WS02` que no tienen privilegios de administrador y no podemos utilizar su equipo a nivel de escritorio para ejecutar `PowerView` o `PowerShell` con el modulo de `AD`, podremos hacerlo de forma remota con herramienta desde `kali` ya que no se requiere privilegios de administrador para poder obtener dicha informacion.

### Herramienta ldapsearch

Primero veremos la herramienta llamada `ldapsearch` la cual mediante unas credenciales nos permitira buscar en la base de datos mediante `LDAP` como haciamos anteriormente de la siguiente forma:

Primero vamos hacerlo de forma anonima con `LDAP` pero en entornos de produccion casi nunca esta activo, ya que podria ser un riesgo de seguridad enorme.

```shell
ldapsearch -x -H ldap://192.168.5.5 -D "" -w "" -b "DC=corp,DC=local"
```

Con `-x` le indicamos el modo de autenticación (En este caso es basico) Con `-H` le indicamos el host donde se encuentra la base de datos a la cual queremos interactuar que seria el `DC`. Con `-D` le indicamos el nombre de usuario dentro del dominio (Lo dejamos vacio para que entre como anonimo) Con `-w` le indicamos la contraseña del usuario, pero tambien lo dejaremos vacio por el acceso anonimo. Con `-b` le indicamos con que partes o con que objetos del dominio queremos interactuar, que en este caso le estamos indicando que interactue con los objetos que haya en `corp.local`.

Info:

```
# extended LDIF
#
# LDAPv3
# base <DC=corp,DC=local> with scope subtree
# filter: (objectclass=*)
# requesting: ALL
#

# search result
search: 2
result: 1 Operations error
text: 000004DC: LdapErr: DSID-0C090A58, comment: In order to perform this opera
 tion a successful bind must be completed on the connection., data 0, v4f7c

# numResponses: 1
```

Pero vemos que el acceso anonimo no esta habilitado.

Pero como tenemos las credenciales del `empleado1` podremos acceder de la siguiente forma:

```shell
ldapsearch -x -H ldap://192.168.5.5 -D "CORP\empleado1" -w "Passw0rd2" -b "DC=corp,DC=local"
```

Si todo va bien nos habra enumerado absolutamente todo el dominio entero que sera excesiba informacion, pero en las ultimas lineas tendremos que ver algo asi:

```
# search reference
ref: ldap://ForestDnsZones.corp.local/DC=ForestDnsZones,DC=corp,DC=local

# search reference
ref: ldap://DomainDnsZones.corp.local/DC=DomainDnsZones,DC=corp,DC=local

# search reference
ref: ldap://corp.local/CN=Configuration,DC=corp,DC=local

# search result
search: 2
result: 0 Success

# numResponses: 259
# numEntries: 255
# numReferences: 3
```

Ahora si queremos filtrar la informacion o realizar busquedas concretas, podremos hacerlo de la siguiente forma:

```shell
ldapsearch -x -H ldap://192.168.5.5 -D 'CORP\empleado1' -w 'Passw0rd2' -b "CN=Users,DC=corp,DC=local"
```

Con el `CN=` lo que le estamos indicando es que nos busque el apartado `Users` de esta parte:

<figure><img src="../../../.gitbook/assets/image (227).png" alt=""><figcaption></figcaption></figure>

Por lo que nos va a devolver todos los objetos de usuarios que haya dentro de dicha carpeta.

Info:

```
# extended LDIF
#
# LDAPv3
# base <CN=Users,DC=corp,DC=local> with scope subtree
# filter: (objectclass=*)
# requesting: ALL
#

# Users, corp.local
dn: CN=Users,DC=corp,DC=local
objectClass: top
objectClass: container
cn: Users
description: Default container for upgraded user accounts
distinguishedName: CN=Users,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105110759.0Z
whenChanged: 20250105110759.0Z
uSNCreated: 5660
uSNChanged: 5660
showInAdvancedViewOnly: FALSE
name: Users
objectGUID:: 1RsMVih400yoaKKYnJTzOg==
systemFlags: -1946157056
objectCategory: CN=Container,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: TRUE
dSCorePropagationData: 20250106101207.0Z
dSCorePropagationData: 20250105110850.0Z
dSCorePropagationData: 16010101000416.0Z

# krbtgt, Users, corp.local
dn: CN=krbtgt,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: user
cn: krbtgt
description: Key Distribution Center Service Account
distinguishedName: CN=krbtgt,CN=Users,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105110850.0Z
whenChanged: 20250105113916.0Z
uSNCreated: 12324
memberOf: CN=Denied RODC Password Replication Group,CN=Users,DC=corp,DC=local
uSNChanged: 16421
showInAdvancedViewOnly: TRUE
name: krbtgt
objectGUID:: +ypfPjOEK0qtK+HwgqE1LA==
userAccountControl: 514
badPwdCount: 0
codePage: 0
countryCode: 0
badPasswordTime: 0
lastLogoff: 0
lastLogon: 0
pwdLastSet: 133805489300051366
primaryGroupID: 513
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeS9gEAAA==
adminCount: 1
accountExpires: 9223372036854775807
logonCount: 0
sAMAccountName: krbtgt
sAMAccountType: 805306368
servicePrincipalName: kadmin/changepw
objectCategory: CN=Person,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: TRUE
dSCorePropagationData: 20250105113916.0Z
dSCorePropagationData: 20250105110850.0Z
dSCorePropagationData: 16010101000416.0Z
msDS-SupportedEncryptionTypes: 0

# Domain Computers, Users, corp.local
dn: CN=Domain Computers,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: group
cn: Domain Computers
description: All workstations and servers joined to the domain
distinguishedName: CN=Domain Computers,CN=Users,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105110850.0Z
whenChanged: 20250105110850.0Z
uSNCreated: 12330
uSNChanged: 12332
name: Domain Computers
objectGUID:: A+KOF3zeXEi+nwQHwZkVbw==
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSAwIAAA==
sAMAccountName: Domain Computers
sAMAccountType: 268435456
groupType: -2147483646
objectCategory: CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: TRUE
dSCorePropagationData: 20250105110850.0Z
dSCorePropagationData: 16010101000001.0Z

# Domain Controllers, Users, corp.local
dn: CN=Domain Controllers,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: group
cn: Domain Controllers
description: All domain controllers in the domain
distinguishedName: CN=Domain Controllers,CN=Users,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105110850.0Z
whenChanged: 20250105113916.0Z
uSNCreated: 12333
memberOf: CN=Denied RODC Password Replication Group,CN=Users,DC=corp,DC=local
uSNChanged: 16423
name: Domain Controllers
objectGUID:: x91IdwfvB02LoOglEB+uHg==
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSBAIAAA==
adminCount: 1
sAMAccountName: Domain Controllers
sAMAccountType: 268435456
groupType: -2147483646
objectCategory: CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: TRUE
dSCorePropagationData: 20250105113916.0Z
dSCorePropagationData: 20250105110850.0Z
dSCorePropagationData: 16010101000416.0Z

# Schema Admins, Users, corp.local
dn: CN=Schema Admins,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: group
cn: Schema Admins
description: Designated administrators of the schema
member: CN=Administrator,CN=Users,DC=corp,DC=local
distinguishedName: CN=Schema Admins,CN=Users,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105110850.0Z
whenChanged: 20250105113916.0Z
uSNCreated: 12336
memberOf: CN=Denied RODC Password Replication Group,CN=Users,DC=corp,DC=local
uSNChanged: 16403
name: Schema Admins
objectGUID:: Dr5KZE0xCkySvfCPXiBgBg==
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSBgIAAA==
adminCount: 1
sAMAccountName: Schema Admins
sAMAccountType: 268435456
groupType: -2147483640
objectCategory: CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: TRUE
dSCorePropagationData: 20250105113916.0Z
dSCorePropagationData: 20250105110850.0Z
dSCorePropagationData: 16010101000416.0Z

# Enterprise Admins, Users, corp.local
dn: CN=Enterprise Admins,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: group
cn: Enterprise Admins
description: Designated administrators of the enterprise
member: CN=Administrator,CN=Users,DC=corp,DC=local
distinguishedName: CN=Enterprise Admins,CN=Users,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105110850.0Z
whenChanged: 20250105113916.0Z
uSNCreated: 12339
memberOf: CN=Denied RODC Password Replication Group,CN=Users,DC=corp,DC=local
memberOf: CN=Administrators,CN=Builtin,DC=corp,DC=local
uSNChanged: 16405
name: Enterprise Admins
objectGUID:: GljKQfBTq0eY76pR2ogOEQ==
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSBwIAAA==
adminCount: 1
sAMAccountName: Enterprise Admins
sAMAccountType: 268435456
groupType: -2147483640
objectCategory: CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: TRUE
dSCorePropagationData: 20250105113916.0Z
dSCorePropagationData: 20250105110850.0Z
dSCorePropagationData: 16010101000416.0Z

# Cert Publishers, Users, corp.local
dn: CN=Cert Publishers,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: group
cn: Cert Publishers
description: Members of this group are permitted to publish certificates to th
 e directory
distinguishedName: CN=Cert Publishers,CN=Users,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105110850.0Z
whenChanged: 20250105110850.0Z
uSNCreated: 12342
memberOf: CN=Denied RODC Password Replication Group,CN=Users,DC=corp,DC=local
uSNChanged: 12344
name: Cert Publishers
objectGUID:: 5nAnSq0UAUmz7IlrscrAow==
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSBQIAAA==
sAMAccountName: Cert Publishers
sAMAccountType: 536870912
groupType: -2147483644
objectCategory: CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: TRUE
dSCorePropagationData: 20250105110850.0Z
dSCorePropagationData: 16010101000001.0Z

# Domain Admins, Users, corp.local
dn: CN=Domain Admins,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: group
cn: Domain Admins
description: Designated administrators of the domain
member: CN=Administrator,CN=Users,DC=corp,DC=local
distinguishedName: CN=Domain Admins,CN=Users,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105110850.0Z
whenChanged: 20250109082915.0Z
uSNCreated: 12345
memberOf: CN=Denied RODC Password Replication Group,CN=Users,DC=corp,DC=local
memberOf: CN=Administrators,CN=Builtin,DC=corp,DC=local
uSNChanged: 36892
name: Domain Admins
objectGUID:: iE0OaJSPKkGY4eHoVqVy2w==
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSAAIAAA==
adminCount: 1
sAMAccountName: Domain Admins
sAMAccountType: 268435456
groupType: -2147483646
objectCategory: CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: TRUE
dSCorePropagationData: 20250105113916.0Z
dSCorePropagationData: 20250105110850.0Z
dSCorePropagationData: 16010101000416.0Z

# Domain Users, Users, corp.local
dn: CN=Domain Users,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: group
cn: Domain Users
description: All domain users
distinguishedName: CN=Domain Users,CN=Users,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105110850.0Z
whenChanged: 20250105110850.0Z
uSNCreated: 12348
memberOf: CN=Users,CN=Builtin,DC=corp,DC=local
uSNChanged: 12350
name: Domain Users
objectGUID:: eb0LuwM4d0i1djaNE6uiuQ==
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSAQIAAA==
sAMAccountName: Domain Users
sAMAccountType: 268435456
groupType: -2147483646
objectCategory: CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: TRUE
dSCorePropagationData: 20250105110850.0Z
dSCorePropagationData: 16010101000001.0Z

# Domain Guests, Users, corp.local
dn: CN=Domain Guests,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: group
cn: Domain Guests
description: All domain guests
distinguishedName: CN=Domain Guests,CN=Users,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105110850.0Z
whenChanged: 20250105110850.0Z
uSNCreated: 12351
memberOf: CN=Guests,CN=Builtin,DC=corp,DC=local
uSNChanged: 12353
name: Domain Guests
objectGUID:: uinw8l0BMUGXquMDk9W96A==
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSAgIAAA==
sAMAccountName: Domain Guests
sAMAccountType: 268435456
groupType: -2147483646
objectCategory: CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: TRUE
dSCorePropagationData: 20250105110850.0Z
dSCorePropagationData: 16010101000001.0Z

# Group Policy Creator Owners, Users, corp.local
dn: CN=Group Policy Creator Owners,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: group
cn: Group Policy Creator Owners
description: Members in this group can modify group policy for the domain
member: CN=Administrator,CN=Users,DC=corp,DC=local
distinguishedName: CN=Group Policy Creator Owners,CN=Users,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105110850.0Z
whenChanged: 20250105110850.0Z
uSNCreated: 12354
memberOf: CN=Denied RODC Password Replication Group,CN=Users,DC=corp,DC=local
uSNChanged: 12391
name: Group Policy Creator Owners
objectGUID:: wZM0LULtP0GgySQj+cNfTQ==
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSCAIAAA==
sAMAccountName: Group Policy Creator Owners
sAMAccountType: 268435456
groupType: -2147483646
objectCategory: CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: TRUE
dSCorePropagationData: 20250105110850.0Z
dSCorePropagationData: 16010101000001.0Z

# RAS and IAS Servers, Users, corp.local
dn: CN=RAS and IAS Servers,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: group
cn: RAS and IAS Servers
description: Servers in this group can access remote access properties of user
 s
distinguishedName: CN=RAS and IAS Servers,CN=Users,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105110850.0Z
whenChanged: 20250105110850.0Z
uSNCreated: 12357
uSNChanged: 12359
name: RAS and IAS Servers
objectGUID:: j1hvXiFX+kOTmNl5MRk5Qg==
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSKQIAAA==
sAMAccountName: RAS and IAS Servers
sAMAccountType: 536870912
groupType: -2147483644
objectCategory: CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: TRUE
dSCorePropagationData: 20250105110850.0Z
dSCorePropagationData: 16010101000001.0Z

# Allowed RODC Password Replication Group, Users, corp.local
dn: CN=Allowed RODC Password Replication Group,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: group
cn: Allowed RODC Password Replication Group
description: Members in this group can have their passwords replicated to all 
 read-only domain controllers in the domain
distinguishedName: CN=Allowed RODC Password Replication Group,CN=Users,DC=corp
 ,DC=local
instanceType: 4
whenCreated: 20250105110850.0Z
whenChanged: 20250105110850.0Z
uSNCreated: 12402
uSNChanged: 12404
name: Allowed RODC Password Replication Group
objectGUID:: fPovEzoxNEuQEd9gpJKzhA==
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSOwIAAA==
sAMAccountName: Allowed RODC Password Replication Group
sAMAccountType: 536870912
groupType: -2147483644
objectCategory: CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: TRUE
dSCorePropagationData: 20250105110850.0Z
dSCorePropagationData: 16010101000001.0Z

# Denied RODC Password Replication Group, Users, corp.local
dn: CN=Denied RODC Password Replication Group,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: group
cn: Denied RODC Password Replication Group
description: Members in this group cannot have their passwords replicated to a
 ny read-only domain controllers in the domain
member: CN=Read-only Domain Controllers,CN=Users,DC=corp,DC=local
member: CN=Group Policy Creator Owners,CN=Users,DC=corp,DC=local
member: CN=Domain Admins,CN=Users,DC=corp,DC=local
member: CN=Cert Publishers,CN=Users,DC=corp,DC=local
member: CN=Enterprise Admins,CN=Users,DC=corp,DC=local
member: CN=Schema Admins,CN=Users,DC=corp,DC=local
member: CN=Domain Controllers,CN=Users,DC=corp,DC=local
member: CN=krbtgt,CN=Users,DC=corp,DC=local
distinguishedName: CN=Denied RODC Password Replication Group,CN=Users,DC=corp,
 DC=local
instanceType: 4
whenCreated: 20250105110850.0Z
whenChanged: 20250105110850.0Z
uSNCreated: 12405
uSNChanged: 12433
name: Denied RODC Password Replication Group
objectGUID:: /6RiZ/1IHUqbulL+tHfNzw==
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSPAIAAA==
sAMAccountName: Denied RODC Password Replication Group
sAMAccountType: 536870912
groupType: -2147483644
objectCategory: CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: TRUE
dSCorePropagationData: 20250105110850.0Z
dSCorePropagationData: 16010101000001.0Z

# Read-only Domain Controllers, Users, corp.local
dn: CN=Read-only Domain Controllers,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: group
cn: Read-only Domain Controllers
description: Members of this group are Read-Only Domain Controllers in the dom
 ain
distinguishedName: CN=Read-only Domain Controllers,CN=Users,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105110850.0Z
whenChanged: 20250105113916.0Z
uSNCreated: 12419
memberOf: CN=Denied RODC Password Replication Group,CN=Users,DC=corp,DC=local
uSNChanged: 16422
name: Read-only Domain Controllers
objectGUID:: r0oqvUiCtkiBcbGeA6uV+A==
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSCQIAAA==
adminCount: 1
sAMAccountName: Read-only Domain Controllers
sAMAccountType: 268435456
groupType: -2147483646
objectCategory: CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: TRUE
dSCorePropagationData: 20250105113916.0Z
dSCorePropagationData: 20250105110850.0Z
dSCorePropagationData: 16010101000416.0Z

# Enterprise Read-only Domain Controllers, Users, corp.local
dn: CN=Enterprise Read-only Domain Controllers,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: group
cn: Enterprise Read-only Domain Controllers
description: Members of this group are Read-Only Domain Controllers in the ent
 erprise
distinguishedName: CN=Enterprise Read-only Domain Controllers,CN=Users,DC=corp
 ,DC=local
instanceType: 4
whenCreated: 20250105110850.0Z
whenChanged: 20250105110850.0Z
uSNCreated: 12429
uSNChanged: 12431
name: Enterprise Read-only Domain Controllers
objectGUID:: Sw21vZk4nke+IPIHiQqlrg==
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeS8gEAAA==
sAMAccountName: Enterprise Read-only Domain Controllers
sAMAccountType: 268435456
groupType: -2147483640
objectCategory: CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: TRUE
dSCorePropagationData: 20250105110850.0Z
dSCorePropagationData: 16010101000001.0Z

# Cloneable Domain Controllers, Users, corp.local
dn: CN=Cloneable Domain Controllers,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: group
cn: Cloneable Domain Controllers
description: Members of this group that are domain controllers may be cloned.
distinguishedName: CN=Cloneable Domain Controllers,CN=Users,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105110850.0Z
whenChanged: 20250105110850.0Z
uSNCreated: 12440
uSNChanged: 12442
name: Cloneable Domain Controllers
objectGUID:: EI+eYl/YFUyjA1DdISOePg==
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSCgIAAA==
sAMAccountName: Cloneable Domain Controllers
sAMAccountType: 268435456
groupType: -2147483646
objectCategory: CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: TRUE
dSCorePropagationData: 20250105110850.0Z
dSCorePropagationData: 16010101000001.0Z

# Protected Users, Users, corp.local
dn: CN=Protected Users,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: group
cn: Protected Users
description: Members of this group are afforded additional protections against
  authentication security threats. See http://go.microsoft.com/fwlink/?LinkId=
 298939 for more information.
distinguishedName: CN=Protected Users,CN=Users,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105110850.0Z
whenChanged: 20250105110850.0Z
uSNCreated: 12445
uSNChanged: 12447
name: Protected Users
objectGUID:: SjwDvAhGiUm6S8K/Rs9oAQ==
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSDQIAAA==
sAMAccountName: Protected Users
sAMAccountType: 268435456
groupType: -2147483646
objectCategory: CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: TRUE
dSCorePropagationData: 20250105110850.0Z
dSCorePropagationData: 16010101000001.0Z

# Key Admins, Users, corp.local
dn: CN=Key Admins,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: group
cn: Key Admins
description: Members of this group can perform administrative actions on key o
 bjects within the domain.
distinguishedName: CN=Key Admins,CN=Users,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105110850.0Z
whenChanged: 20250105113916.0Z
uSNCreated: 12450
uSNChanged: 16404
name: Key Admins
objectGUID:: EAaIlGY13U6UtPUoEuE/1Q==
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSDgIAAA==
adminCount: 1
sAMAccountName: Key Admins
sAMAccountType: 268435456
groupType: -2147483646
objectCategory: CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: TRUE
dSCorePropagationData: 20250105113916.0Z
dSCorePropagationData: 20250105110850.0Z
dSCorePropagationData: 16010101000416.0Z

# Enterprise Key Admins, Users, corp.local
dn: CN=Enterprise Key Admins,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: group
cn: Enterprise Key Admins
description: Members of this group can perform administrative actions on key o
 bjects within the forest.
distinguishedName: CN=Enterprise Key Admins,CN=Users,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105110850.0Z
whenChanged: 20250105113916.0Z
uSNCreated: 12453
uSNChanged: 16409
name: Enterprise Key Admins
objectGUID:: qPFFZ4XBKEqlwwHyBw84Yw==
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSDwIAAA==
adminCount: 1
sAMAccountName: Enterprise Key Admins
sAMAccountType: 268435456
groupType: -2147483640
objectCategory: CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: TRUE
dSCorePropagationData: 20250105113916.0Z
dSCorePropagationData: 20250105110850.0Z
dSCorePropagationData: 16010101000416.0Z

# DnsAdmins, Users, corp.local
dn: CN=DnsAdmins,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: group
cn: DnsAdmins
description: DNS Administrators Group
distinguishedName: CN=DnsAdmins,CN=Users,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105110929.0Z
whenChanged: 20250105110929.0Z
uSNCreated: 12486
uSNChanged: 12488
name: DnsAdmins
objectGUID:: EthGo8ppEke6gAy4YGSfvg==
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSTgQAAA==
sAMAccountName: DnsAdmins
sAMAccountType: 536870912
groupType: -2147483644
objectCategory: CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local
dSCorePropagationData: 16010101000000.0Z

# DnsUpdateProxy, Users, corp.local
dn: CN=DnsUpdateProxy,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: group
cn: DnsUpdateProxy
description: DNS clients who are permitted to perform dynamic updates on behal
 f of some other clients (such as DHCP servers).
distinguishedName: CN=DnsUpdateProxy,CN=Users,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105110929.0Z
whenChanged: 20250105110929.0Z
uSNCreated: 12491
uSNChanged: 12491
name: DnsUpdateProxy
objectGUID:: mNlsOLUxIkyFKRQghBsA7g==
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSTwQAAA==
sAMAccountName: DnsUpdateProxy
sAMAccountType: 268435456
groupType: -2147483646
objectCategory: CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local
dSCorePropagationData: 16010101000000.0Z

# empleado1, Users, corp.local
dn: CN=empleado1,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: user
cn: empleado1
givenName: empleado1
distinguishedName: CN=empleado1,CN=Users,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105175705.0Z
whenChanged: 20250108123649.0Z
displayName: empleado1
uSNCreated: 16458
uSNChanged: 32826
name: empleado1
objectGUID:: 6HGPQwU+IU+7p3AN2aBE4Q==
userAccountControl: 66048
badPwdCount: 0
codePage: 0
countryCode: 0
badPasswordTime: 0
lastLogoff: 0
lastLogon: 133809710839425199
pwdLastSet: 133805734257410855
primaryGroupID: 513
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSUAQAAA==
adminCount: 1
accountExpires: 9223372036854775807
logonCount: 16
sAMAccountName: empleado1
sAMAccountType: 805306368
objectCategory: CN=Person,CN=Schema,CN=Configuration,DC=corp,DC=local
dSCorePropagationData: 20250108123649.0Z
dSCorePropagationData: 20250106122705.0Z
dSCorePropagationData: 20250106101329.0Z
dSCorePropagationData: 20250105175705.0Z
dSCorePropagationData: 16010101000000.0Z
lastLogonTimestamp: 133805739382099173

# empleado2, Users, corp.local
dn: CN=empleado2,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: user
cn: empleado2
givenName: empleado2
distinguishedName: CN=empleado2,CN=Users,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105175825.0Z
whenChanged: 20250106122705.0Z
displayName: empleado2
uSNCreated: 16466
uSNChanged: 20603
name: empleado2
objectGUID:: vJdbXKPHJ02CkWuaSnflEQ==
userAccountControl: 66048
badPwdCount: 0
codePage: 0
countryCode: 0
badPasswordTime: 0
lastLogoff: 0
lastLogon: 133809710896952318
pwdLastSet: 133805735057395361
primaryGroupID: 513
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSUQQAAA==
accountExpires: 9223372036854775807
logonCount: 10
sAMAccountName: empleado2
sAMAccountType: 805306368
objectCategory: CN=Person,CN=Schema,CN=Configuration,DC=corp,DC=local
dSCorePropagationData: 20250106122705.0Z
dSCorePropagationData: 20250106101329.0Z
dSCorePropagationData: 20250105175825.0Z
dSCorePropagationData: 16010101000000.0Z
lastLogonTimestamp: 133805739408927413

# Administrator, Users, corp.local
dn: CN=Administrator,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: user
cn: Administrator
description: Built-in account for administering the computer/domain
distinguishedName: CN=Administrator,CN=Users,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105110800.0Z
whenChanged: 20250105113916.0Z
uSNCreated: 8196
memberOf: CN=Group Policy Creator Owners,CN=Users,DC=corp,DC=local
memberOf: CN=Domain Admins,CN=Users,DC=corp,DC=local
memberOf: CN=Enterprise Admins,CN=Users,DC=corp,DC=local
memberOf: CN=Schema Admins,CN=Users,DC=corp,DC=local
memberOf: CN=Administrators,CN=Builtin,DC=corp,DC=local
uSNChanged: 16407
name: Administrator
objectGUID:: VOXAk47bx0GBKcfhg8BaSA==
userAccountControl: 66048
badPwdCount: 0
codePage: 0
countryCode: 0
badPasswordTime: 0
lastLogoff: 0
lastLogon: 133809710783801526
logonHours:: ////////////////////////////
pwdLastSet: 133805464473994852
primaryGroupID: 513
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeS9AEAAA==
adminCount: 1
accountExpires: 0
logonCount: 16
sAMAccountName: Administrator
sAMAccountType: 805306368
objectCategory: CN=Person,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: TRUE
dSCorePropagationData: 20250105113916.0Z
dSCorePropagationData: 20250105113916.0Z
dSCorePropagationData: 20250105110850.0Z
dSCorePropagationData: 16010101181216.0Z
lastLogonTimestamp: 133805491176373670

# Guest, Users, corp.local
dn: CN=Guest,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: user
cn: Guest
description: Built-in account for guest access to the computer/domain
distinguishedName: CN=Guest,CN=Users,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105110800.0Z
whenChanged: 20250105110800.0Z
uSNCreated: 8197
memberOf: CN=Guests,CN=Builtin,DC=corp,DC=local
uSNChanged: 8197
name: Guest
objectGUID:: V15Idh+Dmkq1v1VKUOTltg==
userAccountControl: 66082
badPwdCount: 0
codePage: 0
countryCode: 0
badPasswordTime: 0
lastLogoff: 0
lastLogon: 0
pwdLastSet: 0
primaryGroupID: 514
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeS9QEAAA==
accountExpires: 9223372036854775807
logonCount: 0
sAMAccountName: Guest
sAMAccountType: 805306368
objectCategory: CN=Person,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: TRUE
dSCorePropagationData: 20250105110850.0Z
dSCorePropagationData: 16010101000001.0Z

# search result
search: 2
result: 0 Success

# numResponses: 27
# numEntries: 26
```

Por lo que vemos si lo hace bien y nos devuelve todo.

Si por ejemplo queremos filtrarlo por un usuario en concreto dentro de la seccion de `Users`, por ejemplo `empleado1`, lo haremos asi:

```shell
ldapsearch -x -H ldap://192.168.5.5 -D 'CORP\empleado1' -w 'Passw0rd2' -b "CN=empleado1,CN=Users,DC=corp,DC=local"
```

Info:

```
# extended LDIF
#
# LDAPv3
# base <CN=empleado1,CN=Users,DC=corp,DC=local> with scope subtree
# filter: (objectclass=*)
# requesting: ALL
#

# empleado1, Users, corp.local
dn: CN=empleado1,CN=Users,DC=corp,DC=local
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: user
cn: empleado1
givenName: empleado1
distinguishedName: CN=empleado1,CN=Users,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105175705.0Z
whenChanged: 20250108123649.0Z
displayName: empleado1
uSNCreated: 16458
uSNChanged: 32826
name: empleado1
objectGUID:: 6HGPQwU+IU+7p3AN2aBE4Q==
userAccountControl: 66048
badPwdCount: 0
codePage: 0
countryCode: 0
badPasswordTime: 0
lastLogoff: 0
lastLogon: 133809710839425199
pwdLastSet: 133805734257410855
primaryGroupID: 513
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSUAQAAA==
adminCount: 1
accountExpires: 9223372036854775807
logonCount: 16
sAMAccountName: empleado1
sAMAccountType: 805306368
objectCategory: CN=Person,CN=Schema,CN=Configuration,DC=corp,DC=local
dSCorePropagationData: 20250108123649.0Z
dSCorePropagationData: 20250106122705.0Z
dSCorePropagationData: 20250106101329.0Z
dSCorePropagationData: 20250105175705.0Z
dSCorePropagationData: 16010101000000.0Z
lastLogonTimestamp: 133805739382099173

# search result
search: 2
result: 0 Success

# numResponses: 2
# numEntries: 1
```

Tambien podremos filtrarlo con `grep` los nombres solamente de los usuarios del dominio:

```shell
ldapsearch -x -H ldap://192.168.5.5 -D 'CORP\empleado1' -w 'Passw0rd2' -b "CN=Users,DC=corp,DC=local" | grep "name*"
```

Info:

```
name: Users
name: krbtgt
name: Domain Computers
name: Domain Controllers
name: Schema Admins
name: Enterprise Admins
name: Cert Publishers
name: Domain Admins
name: Domain Users
name: Domain Guests
name: Group Policy Creator Owners
name: RAS and IAS Servers
name: Allowed RODC Password Replication Group
name: Denied RODC Password Replication Group
name: Read-only Domain Controllers
name: Enterprise Read-only Domain Controllers
name: Cloneable Domain Controllers
name: Protected Users
name: Key Admins
name: Enterprise Key Admins
name: DnsAdmins
description: DNS clients who are permitted to perform dynamic updates on behal
name: DnsUpdateProxy
name: empleado1
name: empleado2
name: Administrator
name: Guest
```

Si queremos obtener informacion de los equipos sera:

```shell
ldapsearch -x -H ldap://192.168.5.5 -D 'CORP\empleado1' -w 'Passw0rd2' -b "CN=Computers,DC=corp,DC=local"
```

Info:

```
# extended LDIF
#
# LDAPv3
# base <CN=Computers,DC=corp,DC=local> with scope subtree
# filter: (objectclass=*)
# requesting: ALL
#

# Computers, corp.local
dn: CN=Computers,DC=corp,DC=local
objectClass: top
objectClass: container
cn: Computers
description: Default container for upgraded computer accounts
distinguishedName: CN=Computers,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105110759.0Z
whenChanged: 20250105110759.0Z
uSNCreated: 5661
uSNChanged: 5661
showInAdvancedViewOnly: FALSE
name: Computers
objectGUID:: MYMRsAKJ/06tgP4lTxc8Zg==
systemFlags: -1946157056
objectCategory: CN=Container,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: TRUE
dSCorePropagationData: 20250106101207.0Z
dSCorePropagationData: 20250105110850.0Z
dSCorePropagationData: 16010101000416.0Z

# WS01, Computers, corp.local
dn: CN=WS01,CN=Computers,DC=corp,DC=local
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: user
objectClass: computer
cn: WS01
distinguishedName: CN=WS01,CN=Computers,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105180538.0Z
whenChanged: 20250105180538.0Z
displayName: WS01$
uSNCreated: 16477
uSNChanged: 16485
name: WS01
objectGUID:: 1w3OLUFbCUit64r7ZgOfJg==
userAccountControl: 4096
badPwdCount: 0
codePage: 0
countryCode: 0
badPasswordTime: 0
lastLogoff: 0
lastLogon: 133809771904013577
localPolicyFlags: 0
pwdLastSet: 133805739382937299
primaryGroupID: 515
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSUgQAAA==
accountExpires: 9223372036854775807
logonCount: 33
sAMAccountName: WS01$
sAMAccountType: 805306369
operatingSystem: Windows 10 Pro
operatingSystemVersion: 10.0 (19045)
dNSHostName: WS01.corp.local
servicePrincipalName: RestrictedKrbHost/WS01
servicePrincipalName: RestrictedKrbHost/WS01.corp.local
servicePrincipalName: HOST/WS01
servicePrincipalName: HOST/WS01.corp.local
objectCategory: CN=Computer,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: FALSE
dSCorePropagationData: 16010101000000.0Z
mS-DS-CreatorSID:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSUAQAAA==
lastLogonTimestamp: 133805739384985924
msDS-SupportedEncryptionTypes: 28

# WS02, Computers, corp.local
dn: CN=WS02,CN=Computers,DC=corp,DC=local
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: user
objectClass: computer
cn: WS02
distinguishedName: CN=WS02,CN=Computers,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105180540.0Z
whenChanged: 20250105180541.0Z
displayName: WS02$
uSNCreated: 16490
uSNChanged: 16499
name: WS02
objectGUID:: KJGbiYwHsU6vTqAH+bRKGw==
userAccountControl: 4096
badPwdCount: 0
codePage: 0
countryCode: 0
badPasswordTime: 0
lastLogoff: 0
lastLogon: 133809771914481606
localPolicyFlags: 0
pwdLastSet: 133805739409703850
primaryGroupID: 515
objectSid:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSUwQAAA==
accountExpires: 9223372036854775807
logonCount: 29
sAMAccountName: WS02$
sAMAccountType: 805306369
operatingSystem: Windows 10 Pro
operatingSystemVersion: 10.0 (19045)
dNSHostName: WS02.corp.local
servicePrincipalName: RestrictedKrbHost/WS02
servicePrincipalName: RestrictedKrbHost/WS02.corp.local
servicePrincipalName: HOST/WS02
servicePrincipalName: HOST/WS02.corp.local
objectCategory: CN=Computer,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: FALSE
dSCorePropagationData: 16010101000000.0Z
mS-DS-CreatorSID:: AQUAAAAAAAUVAAAAF0nPx+676jfdCQeSUQQAAA==
lastLogonTimestamp: 133805739411590180
msDS-SupportedEncryptionTypes: 28

# search result
search: 2
result: 0 Success

# numResponses: 4
# numEntries: 3
```

Para enumerar el grupo administradores, sera de la siguiente forma:

```shell
ldapsearch -x -H ldap://192.168.5.5 -D 'CORP\empleado1' -w 'Passw0rd2' -b "CN=Administrators,CN=Builtin,DC=corp,DC=local"
```

Info:

```
# extended LDIF
#
# LDAPv3
# base <CN=Administrators,CN=Builtin,DC=corp,DC=local> with scope subtree
# filter: (objectclass=*)
# requesting: ALL
#

# Administrators, Builtin, corp.local
dn: CN=Administrators,CN=Builtin,DC=corp,DC=local
objectClass: top
objectClass: group
cn: Administrators
description: Administrators have complete and unrestricted access to the compu
 ter/domain
member: CN=Domain Admins,CN=Users,DC=corp,DC=local
member: CN=Enterprise Admins,CN=Users,DC=corp,DC=local
member: CN=Administrator,CN=Users,DC=corp,DC=local
distinguishedName: CN=Administrators,CN=Builtin,DC=corp,DC=local
instanceType: 4
whenCreated: 20250105110800.0Z
whenChanged: 20250106103302.0Z
uSNCreated: 8199
uSNChanged: 20556
name: Administrators
objectGUID:: dOr31z4WBkOrbh2Qnz7REQ==
objectSid:: AQIAAAAAAAUgAAAAIAIAAA==
adminCount: 1
sAMAccountName: Administrators
sAMAccountType: 536870912
systemFlags: -1946157056
groupType: -2147483643
objectCategory: CN=Group,CN=Schema,CN=Configuration,DC=corp,DC=local
isCriticalSystemObject: TRUE
dSCorePropagationData: 20250105113916.0Z
dSCorePropagationData: 20250105110850.0Z
dSCorePropagationData: 16010101000416.0Z

# search result
search: 2
result: 0 Success

# numResponses: 2
# numEntries: 1
```

### Herramienta pywerview

Si quiero obtener informacion sobre el `Controlador de Dominio` podremos hacerlo de la siguiente forma:

```shell
pywerview get-netdomaincontroller -u empleado1 --dc-ip 192.168.5.5 -p Passw0rd2
```

Info:

```
objectclass:                   top, person, organizationalPerson, user, computer
cn:                            DC01
distinguishedname:             CN=DC01,OU=Domain Controllers,DC=corp,DC=local
instancetype:                  4
whencreated:                   2025-01-05 11:08:49+00:00
whenchanged:                   2025-01-05 11:14:30+00:00
usncreated:                    12293
usnchanged:                    12763
name:                          DC01
objectguid:                    {cccef2ba-863c-497e-a461-f69fd9e4fa7e}
useraccountcontrol:            SERVER_TRUST_ACCOUNT, TRUSTED_FOR_DELEGATION
badpwdcount:                   0
codepage:                      0
countrycode:                   0
badpasswordtime:               1601-01-01 00:00:00+00:00
lastlogoff:                    1601-01-01 00:00:00+00:00
lastlogon:                     2025-01-10 08:20:11.769865+00:00
localpolicyflags:              0
pwdlastset:                    2025-01-05 11:09:18.285751+00:00
primarygroupid:                516
objectsid:                     S-1-5-21-3352250647-938130414-2449934813-1001
accountexpires:                9999-12-31 23:59:59.999999+00:00
logoncount:                    46
samaccountname:                DC01$
samaccounttype:                805306369
operatingsystem:               Windows Server 2022 Standard
operatingsystemversion:        10.0 (20348)
serverreferencebl:             CN=DC01,CN=Servers,CN=Default-First-Site-Name,CN=Sites,CN=Configuration,DC=corp,DC=local
dnshostname:                   DC01.corp.local
ridsetreferences:              CN=RID Set,CN=DC01,OU=Domain Controllers,DC=corp,DC=local
serviceprincipalname:          Dfsr-12F9A27C-BF97-4787-9364-D31B6C55EB04/DC01.corp.local, 
                               ldap/DC01.corp.local/ForestDnsZones.corp.local, ldap/DC01.corp.local/DomainDnsZones.corp.local, 
                               DNS/DC01.corp.local, GC/DC01.corp.local/corp.local, RestrictedKrbHost/DC01.corp.local, 
                               RestrictedKrbHost/DC01, RPC/53f09dda-3e57-4c8c-a34b-f31144b8f612._msdcs.corp.local, HOST/DC01/CORP, 
                               HOST/DC01.corp.local/CORP, HOST/DC01, HOST/DC01.corp.local, HOST/DC01.corp.local/corp.local, 
                               E3514235-4B06-11D1-AB04-00C04FC2DCD2/53f09dda-3e57-4c8c-a34b-f31144b8f612/corp.local, ldap/DC01/CORP, 
                               ldap/53f09dda-3e57-4c8c-a34b-f31144b8f612._msdcs.corp.local, ldap/DC01.corp.local/CORP, ldap/DC01, 
                               ldap/DC01.corp.local, ldap/DC01.corp.local/corp.local
objectcategory:                CN=Computer,CN=Schema,CN=Configuration,DC=corp,DC=local
iscriticalsystemobject:        True
dscorepropagationdata:         2025-01-05 11:08:50+00:00, 1601-01-01 00:00:01+00:00
lastlogontimestamp:            2025-01-05 11:09:29.916424+00:00
msds-supportedencryptiontypes: 28
msds-generationid:             f64915010f98397f...
msdfsr-computerreferencebl:    CN=DC01,CN=Topology,CN=Domain System Volume,CN=DFSR-GlobalSettings,CN=System,DC=corp,DC=local 
```

Si queremos obtener los usuarios, sera de esta forma:

```shell
pywerview get-netuser -u empleado1 --dc-ip 192.168.5.5 -p Passw0rd2
```

Info:

```
objectclass:           top, person, organizationalPerson, user
cn:                    empleado2
givenname:             empleado2
distinguishedname:     CN=empleado2,CN=Users,DC=corp,DC=local
instancetype:          4
whencreated:           2025-01-05 17:58:25+00:00
whenchanged:           2025-01-06 12:27:05+00:00
displayname:           empleado2
usncreated:            16466
usnchanged:            20603
name:                  empleado2
objectguid:            {5c5b97bc-c7a3-4d27-8291-6b9a4a77e511}
useraccountcontrol:    NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
badpwdcount:           0
codepage:              0
countrycode:           0
badpasswordtime:       1601-01-01 00:00:00+00:00
lastlogoff:            1601-01-01 00:00:00+00:00
lastlogon:             2025-01-10 08:24:49.695232+00:00
pwdlastset:            2025-01-05 17:58:25.739536+00:00
primarygroupid:        513
objectsid:             S-1-5-21-3352250647-938130414-2449934813-1105
accountexpires:        9999-12-31 23:59:59.999999+00:00
logoncount:            10
samaccountname:        empleado2
samaccounttype:        805306368
objectcategory:        CN=Person,CN=Schema,CN=Configuration,DC=corp,DC=local
dscorepropagationdata: 2025-01-06 12:27:05+00:00, 2025-01-06 10:13:29+00:00, 2025-01-05 17:58:25+00:00, 
                       1601-01-01 00:00:00+00:00
lastlogontimestamp:    2025-01-05 18:05:40.892740+00:00 

objectclass:           top, person, organizationalPerson, user
cn:                    empleado1
givenname:             empleado1
distinguishedname:     CN=empleado1,CN=Users,DC=corp,DC=local
instancetype:          4
whencreated:           2025-01-05 17:57:05+00:00
whenchanged:           2025-01-08 12:36:49+00:00
displayname:           empleado1
usncreated:            16458
usnchanged:            32826
name:                  empleado1
objectguid:            {438f71e8-3e05-4f21-bba7-700dd9a044e1}
useraccountcontrol:    NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
badpwdcount:           0
codepage:              0
countrycode:           0
badpasswordtime:       1601-01-01 00:00:00+00:00
lastlogoff:            1601-01-01 00:00:00+00:00
lastlogon:             2025-01-10 08:24:43.942520+00:00
pwdlastset:            2025-01-05 17:57:05.741085+00:00
primarygroupid:        513
objectsid:             S-1-5-21-3352250647-938130414-2449934813-1104
admincount:            1
accountexpires:        9999-12-31 23:59:59.999999+00:00
logoncount:            16
samaccountname:        empleado1
samaccounttype:        805306368
objectcategory:        CN=Person,CN=Schema,CN=Configuration,DC=corp,DC=local
dscorepropagationdata: 2025-01-08 12:36:49+00:00, 2025-01-06 12:27:05+00:00, 2025-01-06 10:13:29+00:00, 
                       2025-01-05 17:57:05+00:00, 1601-01-01 00:00:00+00:00
lastlogontimestamp:    2025-01-05 18:05:38.209917+00:00 

objectclass:                   top, person, organizationalPerson, user
cn:                            krbtgt
description:                   Key Distribution Center Service Account
distinguishedname:             CN=krbtgt,CN=Users,DC=corp,DC=local
instancetype:                  4
whencreated:                   2025-01-05 11:08:50+00:00
whenchanged:                   2025-01-05 11:39:16+00:00
usncreated:                    12324
memberof:                      CN=Denied RODC Password Replication Group,CN=Users,DC=corp,DC=local
usnchanged:                    16421
showinadvancedviewonly:        True
name:                          krbtgt
objectguid:                    {3e5f2afb-8433-4a2b-ad2b-e1f082a1352c}
useraccountcontrol:            ACCOUNTDISABLE, NORMAL_ACCOUNT
badpwdcount:                   0
codepage:                      0
countrycode:                   0
badpasswordtime:               1601-01-01 00:00:00+00:00
lastlogoff:                    1601-01-01 00:00:00+00:00
lastlogon:                     1601-01-01 00:00:00+00:00
pwdlastset:                    2025-01-05 11:08:50.005136+00:00
primarygroupid:                513
objectsid:                     S-1-5-21-3352250647-938130414-2449934813-502
admincount:                    1
accountexpires:                9999-12-31 23:59:59.999999+00:00
logoncount:                    0
samaccountname:                krbtgt
samaccounttype:                805306368
serviceprincipalname:          kadmin/changepw
objectcategory:                CN=Person,CN=Schema,CN=Configuration,DC=corp,DC=local
iscriticalsystemobject:        True
dscorepropagationdata:         2025-01-05 11:39:16+00:00, 2025-01-05 11:08:50+00:00, 1601-01-01 00:04:16+00:00
msds-supportedencryptiontypes: 0 

objectclass:            top, person, organizationalPerson, user
cn:                     Guest
description:            Built-in account for guest access to the computer/domain
distinguishedname:      CN=Guest,CN=Users,DC=corp,DC=local
instancetype:           4
whencreated:            2025-01-05 11:08:00+00:00
whenchanged:            2025-01-05 11:08:00+00:00
usncreated:             8197
memberof:               CN=Guests,CN=Builtin,DC=corp,DC=local
usnchanged:             8197
name:                   Guest
objectguid:             {76485e57-831f-4a9a-b5bf-554a50e4e5b6}
useraccountcontrol:     ACCOUNTDISABLE, PASSWD_NOTREQD, NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
badpwdcount:            0
codepage:               0
countrycode:            0
badpasswordtime:        1601-01-01 00:00:00+00:00
lastlogoff:             1601-01-01 00:00:00+00:00
lastlogon:              1601-01-01 00:00:00+00:00
pwdlastset:             1601-01-01 00:00:00+00:00
primarygroupid:         514
objectsid:              S-1-5-21-3352250647-938130414-2449934813-501
accountexpires:         9999-12-31 23:59:59.999999+00:00
logoncount:             0
samaccountname:         Guest
samaccounttype:         805306368
objectcategory:         CN=Person,CN=Schema,CN=Configuration,DC=corp,DC=local
iscriticalsystemobject: True
dscorepropagationdata:  2025-01-05 11:08:50+00:00, 1601-01-01 00:00:01+00:00 

objectclass:            top, person, organizationalPerson, user
cn:                     Administrator
description:            Built-in account for administering the computer/domain
distinguishedname:      CN=Administrator,CN=Users,DC=corp,DC=local
instancetype:           4
whencreated:            2025-01-05 11:08:00+00:00
whenchanged:            2025-01-05 11:39:16+00:00
usncreated:             8196
memberof:               CN=Group Policy Creator Owners,CN=Users,DC=corp,DC=local, CN=Domain Admins,CN=Users,DC=corp,DC=local, 
                        CN=Enterprise Admins,CN=Users,DC=corp,DC=local, CN=Schema Admins,CN=Users,DC=corp,DC=local, 
                        CN=Administrators,CN=Builtin,DC=corp,DC=local
usnchanged:             16407
name:                   Administrator
objectguid:             {93c0e554-db8e-41c7-8129-c7e183c05a48}
useraccountcontrol:     NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
badpwdcount:            0
codepage:               0
countrycode:            0
badpasswordtime:        1601-01-01 00:00:00+00:00
lastlogoff:             1601-01-01 00:00:00+00:00
lastlogon:              2025-01-10 08:24:38.380152+00:00
logonhours:             ffffffffffffffffffffffffffffffffffffffffff...
pwdlastset:             2025-01-05 10:27:27.399485+00:00
primarygroupid:         513
objectsid:              S-1-5-21-3352250647-938130414-2449934813-500
admincount:             1
accountexpires:         1601-01-01 00:00:00+00:00
logoncount:             16
samaccountname:         Administrator
samaccounttype:         805306368
objectcategory:         CN=Person,CN=Schema,CN=Configuration,DC=corp,DC=local
iscriticalsystemobject: True
dscorepropagationdata:  2025-01-05 11:39:16+00:00, 2025-01-05 11:39:16+00:00, 2025-01-05 11:08:50+00:00, 
                        1601-01-01 18:12:16+00:00
lastlogontimestamp:     2025-01-05 11:11:57.637367+00:00
```

Los grupos tambien podremos enumerarlos de la siguiente forma:

```shell
pywerview get-netgroup -u empleado1 --dc-ip 192.168.5.5 -p Passw0rd2
```

Info:

```
samaccountname: DnsUpdateProxy 

samaccountname: DnsAdmins 

samaccountname: Enterprise Key Admins 

samaccountname: Key Admins 

samaccountname: Protected Users 

samaccountname: Cloneable Domain Controllers 

samaccountname: Enterprise Read-only Domain Controllers 

samaccountname: Read-only Domain Controllers 

samaccountname: Denied RODC Password Replication Group 

samaccountname: Allowed RODC Password Replication Group 

samaccountname: Terminal Server License Servers 

samaccountname: Windows Authorization Access Group 

samaccountname: Incoming Forest Trust Builders 

samaccountname: Pre-Windows 2000 Compatible Access 

samaccountname: Account Operators 

samaccountname: Server Operators 

samaccountname: RAS and IAS Servers 

samaccountname: Group Policy Creator Owners 

samaccountname: Domain Guests 

samaccountname: Domain Users 

samaccountname: Domain Admins 

samaccountname: Cert Publishers 

samaccountname: Enterprise Admins 

samaccountname: Schema Admins 

samaccountname: Domain Controllers 

samaccountname: Domain Computers 

samaccountname: Storage Replica Administrators 

samaccountname: Remote Management Users 

samaccountname: Access Control Assistance Operators 

samaccountname: Hyper-V Administrators 

samaccountname: RDS Management Servers 

samaccountname: RDS Endpoint Servers 

samaccountname: RDS Remote Access Servers 

samaccountname: Certificate Service DCOM Access 

samaccountname: Event Log Readers 

samaccountname: Cryptographic Operators 

samaccountname: IIS_IUSRS 

samaccountname: Distributed COM Users 

samaccountname: Performance Log Users 

samaccountname: Performance Monitor Users 

samaccountname: Network Configuration Operators 

samaccountname: Remote Desktop Users 

samaccountname: Replicator 

samaccountname: Backup Operators 

samaccountname: Print Operators 

samaccountname: Guests 

samaccountname: Users 

samaccountname: Administrators
```

Tambien podremos enumerar las `GPOs`:

```shell
pywerview get-netgpo -u empleado1 --dc-ip 192.168.5.5 -p Passw0rd2
```

Info:

```
objectclass:              top, container, groupPolicyContainer
cn:                       {410CF9DA-E128-4646-B131-688DF0C8538D}
distinguishedname:        CN={410CF9DA-E128-4646-B131-688DF0C8538D},CN=Policies,CN=System,DC=corp,DC=local
instancetype:             4
whencreated:              2025-01-07 19:27:07+00:00
whenchanged:              2025-01-07 19:33:42+00:00
displayname:              Script Execution Policy
usncreated:               24603
usnchanged:               24613
showinadvancedviewonly:   True
name:                     {410CF9DA-E128-4646-B131-688DF0C8538D}
objectguid:               {6c17e59c-b1ec-411a-ad2c-ef273ba52208}
flags:                    0
versionnumber:            1
objectcategory:           CN=Group-Policy-Container,CN=Schema,CN=Configuration,DC=corp,DC=local
gpcfunctionalityversion:  2
gpcfilesyspath:           \\corp.local\SysVol\corp.local\Policies\{410CF9DA-E128-4646-B131-688DF0C8538D}
gpcmachineextensionnames: [{35378EAC-683F-11D2-A89A-00C04FBBCFA2}{D02B1F72-3407-48AE-BA88-E8213C6761F1}]
dscorepropagationdata:    1601-01-01 00:00:00+00:00 

objectclass:             top, container, groupPolicyContainer
cn:                      {507F35A7-D0D3-4917-9561-240C31EE0DD4}
distinguishedname:       CN={507F35A7-D0D3-4917-9561-240C31EE0DD4},CN=Policies,CN=System,DC=corp,DC=local
instancetype:            4
whencreated:             2025-01-06 12:14:51+00:00
whenchanged:             2025-01-06 12:18:22+00:00
displayname:             Unidad Compartida Policy
usncreated:              20589
usnchanged:              20600
showinadvancedviewonly:  True
name:                    {507F35A7-D0D3-4917-9561-240C31EE0DD4}
objectguid:              {1b078af7-1c9d-4c53-8318-2f0013d62e64}
flags:                   0
versionnumber:           131072
objectcategory:          CN=Group-Policy-Container,CN=Schema,CN=Configuration,DC=corp,DC=local
gpcfunctionalityversion: 2
gpcfilesyspath:          \\corp.local\SysVol\corp.local\Policies\{507F35A7-D0D3-4917-9561-240C31EE0DD4}
gpcuserextensionnames:   [{42B5FAAE-6536-11D2-AE5A-0000F87571E3}{40B66650-4972-11D1-A7CA-0000F87571E3}]
dscorepropagationdata:   1601-01-01 00:00:00+00:00 

objectclass:              top, container, groupPolicyContainer
cn:                       {6AC1786C-016F-11D2-945F-00C04fB984F9}
distinguishedname:        CN={6AC1786C-016F-11D2-945F-00C04fB984F9},CN=Policies,CN=System,DC=corp,DC=local
instancetype:             4
whencreated:              2025-01-05 11:07:59+00:00
whenchanged:              2025-01-05 11:07:59+00:00
displayname:              Default Domain Controllers Policy
usncreated:               5675
usnchanged:               5675
showinadvancedviewonly:   True
name:                     {6AC1786C-016F-11D2-945F-00C04fB984F9}
objectguid:               {7ee475ca-6694-4ab0-8b83-d00a93a7bcfa}
flags:                    0
versionnumber:            1
systemflags:              -1946157056
objectcategory:           CN=Group-Policy-Container,CN=Schema,CN=Configuration,DC=corp,DC=local
iscriticalsystemobject:   True
gpcfunctionalityversion:  2
gpcfilesyspath:           \\corp.local\sysvol\corp.local\Policies\{6AC1786C-016F-11D2-945F-00C04fB984F9}
gpcmachineextensionnames: [{827D319E-6EAC-11D2-A4EA-00C04F79F83A}{803E14A0-B4FB-11D0-A0D0-00A0C90F574B}]
dscorepropagationdata:    2025-01-05 11:08:50+00:00, 1601-01-01 00:00:00+00:00 

objectclass:              top, container, groupPolicyContainer
cn:                       {31B2F340-016D-11D2-945F-00C04FB984F9}
distinguishedname:        CN={31B2F340-016D-11D2-945F-00C04FB984F9},CN=Policies,CN=System,DC=corp,DC=local
instancetype:             4
whencreated:              2025-01-05 11:07:59+00:00
whenchanged:              2025-01-05 11:11:58+00:00
displayname:              Default Domain Policy
usncreated:               5672
usnchanged:               12751
showinadvancedviewonly:   True
name:                     {31B2F340-016D-11D2-945F-00C04FB984F9}
objectguid:               {69776306-72bc-4096-81ac-9065448cb4a0}
flags:                    0
versionnumber:            3
systemflags:              -1946157056
objectcategory:           CN=Group-Policy-Container,CN=Schema,CN=Configuration,DC=corp,DC=local
iscriticalsystemobject:   True
gpcfunctionalityversion:  2
gpcfilesyspath:           \\corp.local\sysvol\corp.local\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}
gpcmachineextensionnames: [{35378EAC-683F-11D2-A89A-00C04FBBCFA2}{53D6AB1B-2488-11D1-A28C-00C04FB94F17}][{827D319E-6EAC-11D2-A4EA-00C04F79F83A}{803E14A0-B4FB-11D0-A0D0-00A0C90F574B}][{B1BE8D72-6EAC-11D2-A4EA-00C04F79F83A}{53D6AB1B-2488-11D1-A28C-00C04FB94F17}]
dscorepropagationdata:    2025-01-05 11:08:50+00:00, 1601-01-01 00:00:00+00:00
```

### Herramienta jxplorer

Si por ejemplo queremos hacerlo de otra forma pero mas grafico todo, podremos hacerlo con la herramienta `jxplorer`, pero tendremos que instalarlo ya que no viene por defecto en `kali`:

```shell
sudo apt install jxplorer
```

Una vez instalada, la abriremos de la siguiente forma:

```shell
jxplorer
```

Dentro de la herramienta tendremos que pulsar el siguiente boton para establecer la conexion:

<figure><img src="../../../.gitbook/assets/image (228).png" alt=""><figcaption></figcaption></figure>

Se nos abrira una ventana en la que tendremos que introducir la informacion necesaria -> `Host` = `192.168.5.5` -> `Level` = `User + Password` -> `User DN` = `CN=empleado1,CN=Users,DC=corp,DC=local` -> `Password` = `Passw0rd2` -> `Ok`

<figure><img src="../../../.gitbook/assets/image (229).png" alt=""><figcaption></figcaption></figure>

Y veremos que se nos conecto correctamente:

<figure><img src="../../../.gitbook/assets/image (230).png" alt=""><figcaption></figcaption></figure>

Si pulsamos 2 veces en `corp` veremos todos los objetos que tenemos en el `LDAP`:

<figure><img src="../../../.gitbook/assets/image (231).png" alt=""><figcaption></figcaption></figure>

Si nos vamos a `Users` y nos vamos en la seccion de `Table Editor`, podremos visualizar todo de mejor forma:

<figure><img src="../../../.gitbook/assets/image (232).png" alt=""><figcaption></figcaption></figure>

Incluso si tuviramos privilegios de administrador podremos editar toda esta informacion desde este entorno grafico.
