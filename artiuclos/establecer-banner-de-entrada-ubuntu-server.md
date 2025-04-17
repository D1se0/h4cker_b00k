---
icon: ubuntu
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

# Establecer Banner de entrada Ubuntu Server

Cuando nosotros nos descargamos un `Ubuntu Server` para crear un `CTF` y queremos que cuando nos aparezca el `login` veamos la informacion de la maquina como por ejemplo su `nombre`, el `autor`, la `IP`, etc... Podremos hacerlo de la siguiente forma:

## Creacion Banner de entrada CTF

Una vez que ya tengamos un `Ubuntu Server` instalado y configurado, tendremos que iniciar sesion con el usuario que tengamos y escalar a `root`, para poder cofigurar el `banner`.

> NOTA

Os dejo el link del `Ubuntu Server v22.04.05` que para mi es el que mejor funciona.

URL = [Download Ubuntu Server](https://releases.ubuntu.com/22.04/ubuntu-22.04.5-live-server-amd64.iso)

### Banner pre-login

Una vez que ya seamos `root` vamos a realizar lo siguiente:

Iniciamos el servicio de `crontab` para que esto pueda funcionar y lo `enablamos`.

```shell
sudo systemctl start cron
sudo systemctl enable cron
```

Creamos el archivo que necesitaremos para que se ejecuten los comandos y se plasme en el `banner`.

```shell
nano /usr/local/bin/issue-banner.sh

#Dentro del nano
#!/bin/bash

echo "==========================================" > /etc/issue
echo "        🚩  Bienvenido a la Máquina CTF" >> /etc/issue
echo "==========================================" >> /etc/issue
echo "    📛 Nombre:     <NAME> MACHINE" >> /etc/issue
echo "    🧑 Autor:      <AUTHOR>" >> /etc/issue
echo "    🌐 IP actual:  $(hostname -I | awk '{print $1}')" >> /etc/issue
echo "    📈 Uptime:     $(uptime -p)" >> /etc/issue
echo "    💾 Disco:      $(df -h / | awk 'NR==2 {print $3 "/" $2}')" >> /etc/issue
echo "    🧠 Memoria:    $(free -h | awk '/Mem:/ {print $3 "/" $2}')" >> /etc/issue
echo "==========================================" >> /etc/issue
```

Lo guardamos y establecemos los permisos necesarios:

```shell
chmod +x /usr/local/bin/issue-banner.sh
```

Vamos a crear el `crontab` para que se ejecute como `root`:

```shell
sudo -u root crontab -e
# <ELEGIMOS LA OPCION 1 (nano)>
```

Info:

```
.............................<RESTO DE LINEAS>....................................

@reboot /usr/local/bin/issue-banner.sh
```

Guardamos el archivo de `crontab` y ahora si, vamos a reiniciar la maquina para que cuando se inicie podamos ver el `banner` con todos los comandos ejecutados de forma correcta:

```shell
reboot
```

Info:

<figure><img src="../.gitbook/assets/image (351).png" alt=""><figcaption></figcaption></figure>

### Banner post-login

Una vez que ya seamos `root` vamos a crear el siguiente fichero de condiguracion:

```shell
sudo nano /etc/update-motd.d/00-ctf-banner
```

Info:

```bash
#!/bin/bash

# ========================
# 🧠 CTF: <NAME> MACHINE
# 👨‍💻 Autor: <AUTHOR>
# ========================

IP=$(hostname -I | awk '{print $1}')
UPTIME=$(uptime -p)
DISK=$(df -h / | awk 'NR==2 {print $3 "/" $2}')
MEM=$(free -h | awk '/Mem:/ {print $3 "/" $2}')

echo "=========================================="
echo "    🚩  Bienvenido a la Máquina CTF"
echo "=========================================="
echo "  📛 Nombre:     <NAME> MACHINE"
echo "  🧑 Autor:      <AUTHOR>"
echo "  🌐 IP actual:  $IP"
echo "  📈 Uptime:     $UPTIME"
echo "  💾 Disco:      $DISK usados"
echo "  🧠 Memoria:    $MEM"
echo "=========================================="
```

Ahora esto lo guardaremos y le daremos permisos de ejecuccion:

```shell
sudo chmod -x /etc/update-motd.d/*
sudo chmod +x /etc/update-motd.d/00-ctf-banner
```

Con esto lo que hacemos es quitar los permisos de ejecuccion de los demas `banners` por si acaso entraran en conflicto, para que asi nos aseguremos de que solamente se muestra el nuestro.

Ahora solo tendremos que reiniciar la maquina y cuando entremos por `SSH` veremos lo siguiente:

<figure><img src="../.gitbook/assets/image (350).png" alt=""><figcaption></figcaption></figure>

Con esto ya tendremos nuestro `banner` de forma personalizada para nuestro `CTF` y que se vea de forma mas profesional.
