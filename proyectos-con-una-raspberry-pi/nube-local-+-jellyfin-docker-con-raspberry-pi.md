---
icon: raspberry-pi
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

# Nube local + Jellyfin (Docker) con Raspberry Pi

## Introduccion

Podremos montarnos de forma casera una nube local en nuestra casa o donde queramos, pudiendo acceder desde cualquier parte dentro de la red local a nuestra nube para guardar o descargar archivos del mismo, tambien como complemento añadiremos un software llamado `Jellyfin` donde podremos cargar peliculas, series, etc... Y poderlas consumir desde cualquier parte con la aplicacion de `Jellyfin`.

Instalaremos tambien el `Portainer` para `dockerizar` `Jellyfin` y asi no instalarlo en el propio sistema de la Raspberry Pi.

## Complementos

1. Raspberry Pi 4 de 8 GB (RAM):

* [Link Amazon](https://amzn.eu/d/arFzWD7)

2. Alimentación Raspberry Pi original:

* [Link Amazon](https://amzn.eu/d/etx5dbR)

3. Decoración y protector Raspberry Pi:

* [Link Amazon](https://amzn.eu/d/geV6x2J)

4. MicroSD 64 GB:

* [Link Amazon](https://amzn.eu/d/huB6KMg)

5. Adaptador SATA a USB:

* [Link Amazon](https://amzn.eu/d/9La29Xm)

1. Disco SSD 250 GB:

* [Link Amazon](https://amzn.eu/d/4iE0Vt1)

## Instalación OpenMediaVault (Nube local)

### Instalación sistema operativo Raspberry Pi

Primero tendremos que irnos a la pagina oficial de `Raspberry Pi` para descargarnos la imagen oficial, en este caso utilizaremos el `Lite` ya que es compatible con lo que vamos hacer, tambien seleccionaremos el de `64 Bits` por que es compatible con `Raspberry Pi 4 8 GB (RAM)` para arriba, todo lo que sea de ahi para abajo tendria que ser de `32 Bits`.

URL = [Link Download Raspberry Pi SO Lite 2025](https://downloads.raspberrypi.com/raspios_lite_arm64/images/raspios_lite_arm64-2025-05-13/2025-05-13-raspios-bookworm-arm64-lite.img.xz)

Una vez descargada la imagen, tendremos que insertar la `MicroSD` en nuestro PC con un adaptador para poder cargar ahi la imagen e instalar el `S.O.` en dicha memoria.

Ahora tendremos que descargarnos el `Raspberry Pi Imager` para poder instalar todo esto en la `SD`.

URL = [Link Download Raspberry Pi Imager (Windows)](https://downloads.raspberrypi.com/imager/imager_latest.exe)

Vamos a ejecutar el `imager`, es lo que hara sera abrir una pantalla en la que tendremos que darle a `Elegir Dispositivo`, en esta seccion elegiremos `Raspberry Pi 4`, en `Elegir SO` seleccionaremos la opcion `Usar Personalizado` y de ahi seleccionaremos lo que nos descargamos el archivo `.img.xz`. Por ultimo le daremos a `Elegir Almacenamiento`, dentro de esta opcion seleccionaremos la `MicroSD` de `64 GB` que deberia de aparecernos o la memoria que se haya insertado.

<figure><img src="../.gitbook/assets/Pasted image 20251113102551.png" alt=""><figcaption></figcaption></figure>

Despues de hacer todos estos pasos le tendremos que dar al boton llamado `Siguiente` para empezar el proceso de instalacion, despues no aparecera una ventana en la que nos pondra que si queremos aplicar los ajustes de personalizacion del `SO`, seleccionaremos la opcion llamada `Editar Ajustes` -> Dentro de esta seccion veremos esto:

<figure><img src="../.gitbook/assets/Captura de pantalla 2025-11-13 103154.png" alt=""><figcaption></figcaption></figure>

Vamos a personalizar algunas cosas empezando por la contraseña del usuario `pi`, ya que nos vendra la de por defecto.

Activaremos la opcion de `Establecer ajuster regionales` y lo estableceremos en la region correspondiente nuestra.

Llendonos en la pestaña `Servicios` tendremos que activar la opcion `Activar SSH` y establecer la opcion `Utilizar autenticacion por contraseña`.

Pulsaremos en `Guardar` y seguidamente le daremos al boton `Si` para que se instale con nuestros ajustes personalizados, despues volveremos a dar a `Si`.

Una vez instalador el sistema ya podremos sacar la tarjeta de memoria `MicroSD`, para poder insertarla en la `Raspberry Pi 4`.

Hecho esto tendremos que conectar la `Raspberry Pi` al `Router` mediante un cable `RJ45` y con su cable de alimentacion correspondiente para que pueda funcionar.

### Identificar IP de Raspberry Pi 4

Instalado todos estos pasos, vamos a volver a nuestro PC, abriremos la terminal y ejecutaremos un `ping` al dominio que viene por defecto de la `Raspberry Pi` para saber la IP con la que esta asociada.

```shell
ping raspberrypi.local
```

Con el `output` de este comando como ya mencione obtendremos la IP que tiene dicho `Raspberry Pi`, en mi caso sera la `192.168.1.167`.

### Acceso por SSH a la Raspberry Pi 4

Sabiendo esto vamos a conectarnos por `SSH` al dispositivo.

```shell
ssh pi@192.168.1.167
```

Metemos como contraseña la que establecimos anteriormente...

```
pi@raspberrypi:~ $ 
```

Y si todo sale bien, veremos que estaremos dentro del dispositivo de forma remota desde nuestro PC.

### Actualizar el sistema de la Raspberry Pi 4

Ahora vamos actualizar el sistema para que no nos de ningun error a la hora de utilizar el dispositivo.

```shell
sudo apt update
sudo apt upgrade
```

Hecho esto vamos a utilizar la herramienta que viene por defecto en el sistema de la `Raspberry Pi` para configurar nuestro dispositivo de forma correcta.

```shell
sudo raspi-config
```

Info:

<figure><img src="../.gitbook/assets/Captura de pantalla 2025-11-13 182816.png" alt=""><figcaption></figcaption></figure>

Se nos abrira una interfaz de configuracion con varias opciones, a nosotros nos interesara la llamada `Localisation Options`, dentro de esta seccion seleccionaremos la llamada `es_ES.UTF-8 UTF-8`, pulsaremos el `Ok`, nos llevara a otra seccion en la que seleccionaremos la que nos aparece como `es_ES.UTF-8 UTF-8`, hecho esto volveremos a pulsar en la opcion llamada `Localisation Options` de ahi seleccionamos `Timezone` y seleccionamos en la que estemos en mi caso en `Europa`, despues volvemos a dar a la misma opcion, seleccionamos `Keyboard` para que asi pille el lenguaje de forma automatica, por ultimo volvemos a darle a la misma opcion del principio y seleccionamos `WLAN Country` para seleccionar el correspondiente al nuestro.

Hecho todo esto le daremos en el menu principal a la opcion llamada `Advanced Options`, de ahi seleccionaremos la opcion llamada `A1 Expand Filesystem` para expandir el sistema y aprovechar el espacio completo de la `MicroSD`. Despues nos pedira que reiniciemos el sistema, por lo que le daremos a `Finish` y para aplicar todo reiniciaremos el sistema.

Cuando nos saque del acceso por `SSH`, volveremos a tirar un `ping` para saber cuando esta levantado.

```shell
ping 192.168.1.167
```

Si nos responde bien, significa que ya esta levantado, por lo que nos volveremos a meter por `SSH` para ya poder instalar `OpenMediaVault`.

```shell
ssh pi@192.168.1.167
```

Metemos la contraseña que pusimos...

```
pi@raspberrypi:~ $ 
```

### Instalación OpenMediaVault

Dentro de la `Raspberry Pi` por `SSH` vamos a ejecutar el siguiente comando para instalar dicho `Software`.

URL = [GitHub Instalacion OMV](https://github.com/OpenMediaVault-Plugin-Developers/installScript)

```shell
sudo wget -O - https://github.com/OpenMediaVault-Plugin-Developers/installScript/raw/master/install | sudo bash
```

Cuando ejecutemos esto nos podremos tirar unos `30 minutos` de instalacion, por lo que tardara un poco, pero si se os queda pillado en algun momento por esta parte...

<figure><img src="../.gitbook/assets/Captura de pantalla 2025-11-17 161255.png" alt=""><figcaption></figcaption></figure>

Puede ser por que la `IP` haya cambiado, ya que se toca de forma automatica configuraciones de `red`, por lo que nos iremos a otra terminal y le haremos un `ping` al dominio del dispositivo.

```shell
ping raspberrypi.local
```

En mi caso me paso, y ahora tengo la `IP` asignada `192.168.1.168`, por lo que podremos cerrar la terminal anterior y entrar por la `web` con la `IP` directamente, ya que de forma secundaria se habra instalado.

```
URL = http://192.168.1.168/
```

Lo dejamos por el puerto `80` normal y tendremos que ver esto:

<figure><img src="../.gitbook/assets/Captura de pantalla 2025-11-17 161609.png" alt=""><figcaption></figcaption></figure>

Si vemos esto es que ha funcionado, por lo que tendremos que meter las credenciales por defecto.

```
User: admin
Password: openmediavault
```

Hecho esto veremos lo siguiente:

<figure><img src="../.gitbook/assets/Captura de pantalla 2025-11-17 161705.png" alt=""><figcaption></figcaption></figure>

Estando dentro empezaremos la configuracion de nuestra `nube local`.

### Configuración de OMV

Antes de tocar nada, podemos modificar la contraseña de nuestro usuario llendonos al icono del usuario en la parte derecha superior y desplegada las opciones nos vamos a la llamada `Cambiar contraseña`, cuando la modifiquemos le daremos a `Salvar`.

Ahora vamos a configurar el tiempo de sesion para que no sea cada `5` minutos, nos iremos a la opcion `Sistema` -> `Área de trabajo`, dentro de esta seccion seleccionaremos el numero `5 Minutos` que vemos por la opcion `15 Minutos` por ejemplo.

Vamos a pinear todas las opciones en nuestro `Dashboard` para verlo absolutamente todo, nos iremos a `Dashboard` -> `Configuracion` y dentro de esta seccion seleccionaremos todo, y le daremos a `Salvar`.

Tambien vamos a comprobar que no haya ninguna actualizacion extra llendonos a `Sistema` -> `Gestion de actualizaciones` -> `Actualizaciones`, dentro recargaremos la pagina con el boton de una flechita circular, si no vemos nada perfecto, si vemos algo le daremos a actualizar.

Ahora vamos a configurar la interfaz de red para que no nos cambie la `IP` por el `DHCP`. Nos iremos a `Red` -> `Interfaces`, dentro de esta seccion seleccionaremos la interfaz que queramos modificar, en mi caso `eth0` y le daremos al simbolo `Lapiz` para editarlo. En la seccion de `IPv4` cambiaremos el estado de `Automatico` por `Estatico` y pondremos una `IP` fuera del rango de la asignacion del `DHCP` (Esto se puede saber entrando a nuestro `Router` y llendonos a la seccion `DHCP` o una seccion parecida para poder ver el inicio y fin del rango) en mi caso pondre `192.168.1.100`, como mascara de red pondre `255.255.255.0` y por ultimo en el `Gateway` pondre la `IP` del `Router` generalmente en la `192.168.1.1`. Hecho esto en la seccion de `DNS` pondremos los `2` de `Google` que seria `8.8.8.8,8.8.4.4` separado con una coma. Le daremos a `Salvar` y despues le daremos a `Aplicar Cambios` en un recuadro naranja dandole al `Tick` que tiene que aparecer.

#### Error al aplicar los cambios

> Si en esta parte cuando se aplica los cambios da un error, podremos hacer lo siguiente:

Tendremos que entrar a la `Raspberry Pi` mediante un conversor `MicroUSB` a `HDMI` para conectarnos en un monitor, despues mediante un `USB` conectar un teclado, metiendonos con las credenciales establecidas anteriormente del sistema, tendremos que editar el archivo de configuracion llamado `a` y poner lo siguiente:

```yaml
network:
  renderer: networkd
  ethernets:
    eth0: # Dependiendo de tu interfaz de red
      dhcp4: false
      dhcp6: false
      addresses:
        - 192.168.1.100/24 # Cambiar a la IP que este fuera del rango DHCP
      routes:
        - to: 0.0.0.0/0
          via: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8,8.8.4.4] # Servidores DNS
```

En el nombre de la interfaz de red tendremos que poner la que estemos utilizando, en mi caso me di cuenta de que no era `eth0` si no que era `end0`, esto se puede ver haciendo un `ip a`.

Guardado el archivo y aplicado los cambios con...

```shell
sudo netplan generate
sudo netplan apply
```

Si listamos pasados unos segundos la `IP` veremos que ahora si nos lo ha pillado bien.

#### Continuación con la configuración de OMV

Siguiendo con la configuracion, vamos a configurar el disco `SSD`, nos vamos a `Almacenamiento` -> `Discos`, en esta parte tendremos que instalar el disco `SSD` mediante un conversor `SATA` a `USB 3.0` en tal caso de que fuera un disco interno como el mio, una vez instalado, si cargamos la pagina veremos nuestro nuevo disco, pero vamos a borrarle de ahi para aplicarle un formato compatible como `Ext4`, por lo que seleccionaremos el disco `SSD` y le daremos a `Borrar`, seleccionaremos la casilla de seguridad y le daremos a que `Si`, seguidamente nos aparecera otra opcion y le daremos a `Rapida`, esto borrara todo el contenido del Disco. Hecho esto nos iremos a `Almacenamiento` -> `Sistema de Archivo`, dentro de esta seccion seleccionaremos el `+` (Crea y monta un sistema de archivos), seleccionaremos el formato `EXT4`, por ultimo pondremos el dispositivo que sera nuestra `SSD` que borramos anteriormente, le daremos a `Salvar`, despues seguidamente seleccionaremos el dispisitivo de nuevo y pondremos un `umbral` del `90%` para que nos avise cuando sobre pase ese `umbral` de almacenamiento, le daremos a `Salvar` y despues aplicaremos los cambios dandole al `Check`.

Ahora vamos a configurar nuestra carpeta compartida para que se comparta en la `Red`, nos iremos a `Almacenamiento` -> `Carpetas Compartidas`, dentro de esta seccion le daremos al `+` (Crear) pondremos como nombre el que queramos, en la parte de `Sistema de archivo` seleccionaremos nuestra `SSD`, la ruta relativa la dejamos por defecto y en `Permisos` para que todos puedan entrar y editar seleccionaremos `Todo el mundo: Lectura/Escritura`, le damos a `Salvar` y despues aplicar los cambios en el `Check`.

Ahora para compartirlo en la `red` nos vamos a `Servicios` -> `SMB/CIFS` -> `Configuración`, dentro de esta seccion donde pone la casilla `Habilitado` tendremos que activarla para `habilitarla`, le daremos a `Salvar` y seguidamente `aplicar`.

Nos vamos a ir a `Almacenamiento` -> `SMB/CIFS` -> `Compartidos`, dentro de esta seccion le daremos al `+` (Crear) en la parte de `Shared Folder` seleccionaremos nuestro disco `SSD`, en `Público` pondremos `Invitados solamente`, hecho esto le daremos a `Salvar` y `Aplicar`.

Habiendo hecho todo esto ya tendremos nuestra `nube local` totalmente funcional, para comprobar esto haremos lo siguiente.

### Comprobación de acceso a nube local (OMV)

Desde un `Windows` por ejemplo vamos a una carpeta normal, en la parte de `Red` de la parte izquierda:

<figure><img src="../.gitbook/assets/Captura de pantalla 2025-11-17 165929.png" alt=""><figcaption></figcaption></figure>

Iremos dentro, activaremos el acceso por `red` de `Windows`, hecho esto, nos iremos a la barra de busqueda.

<figure><img src="../.gitbook/assets/Captura de pantalla 2025-11-17 170014.png" alt=""><figcaption></figcaption></figure>

Y pondremos lo siguiente:

```
\\192.168.1.100
```

Cuando le demos a `ENTER` nos saltara que metamos unas credenciales, tendremos que meter las credenciales del usuario `pi` que configuramos al inicio del sistema. Si todo es correcto ya podremos ver la carpeta compartida con el nombre que le hayamos puesto, podremos entrar dentro y crear lo que queramos, vamos a crear las siguientes carpetas para que las detecte posteriormente `Jellyfin`.

```
movies
series
```

Hecho esto ya podremos pasar con la fase de instalacion de `Jellyfin + Portainer + Docker`.

## Instalación de Jellyfin + Portainer (Docker)

### Prepara las carpetas

Primero, crea las carpetas donde `Jellyfin` guardará su configuración y cache:

```shell
# Crea las carpetas necesarias
sudo mkdir -p /home/pi/docker/jellyfin/config
sudo mkdir -p /home/pi/docker/jellyfin/cache

# Cambia los permisos para que Docker pueda escribir
sudo chown -R 1000:1000 /home/pi/docker/jellyfin
```

### Instalar Docker y Docker Compose

Primero tendremos que instalar algunas herramientas que nos haran falta para el funcionamiento del `portainer`.

```shell
# Instalar docker
sudo apt install docker-ce=5:28.5.2-1~debian.12~bookworm \
                 docker-ce-cli=5:28.5.2-1~debian.12~bookworm \
                 containerd.io

# Evitar que se actualice
sudo apt-mark hold docker-ce docker-ce-cli containerd.io

# Enablar los servicios de docker
sudo systemctl start docker
sudo systemctl enable docker

# Añadir nuestro usuario al grupo docker
sudo usermod -aG docker $(USER)

# Reiniciar el sistema
sudo reboot
```

### Instalar Portainer

Ejecuta estos comandos en tu Raspberry Pi:

```bash
# Crear volumen para persistencia de Portainer
docker volume create portainer_data

# Ejecutar Portainer
docker run -d \
  -p 8000:8000 \
  -p 9443:9443 \
  --name portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest

# Verificar que está corriendo
docker ps
```

**Acceso a Portainer**: Ve a `https://[IP-DE-TU-RASPBERRY]:9443`

***

### Identificar las rutas de tu OpenMediaVault

Primero necesitas saber dónde están montados tus discos de OpenMediaVault:

```bash
# Ver todos los discos montados
df -h

# O buscar específicamente
lsblk
mount | grep -i vault
```

**Ejemplo de rutas típicas de OpenVault:**

* `/srv/dev-disk-by-uuid-XXXXX/`
* `/mnt/hdd1/`
* `/media/pi/OpenVault/`

**Anota estas rutas**, las necesitarás para el siguiente paso.

***

### Crear Jellyfin en Portainer

1. **Accede a Portainer** (`https://tu-ip:9443`)
2. **Ve a "Stacks"** en el menú lateral
3. **Clic en "Add stack"**
4. **Nombre del stack**: `jellyfin`
5. **Método**: Web editor

#### 📝 Configuración YAML para Jellyfin

**IMPORTANTE**: Reemplaza `/ruta/a/tu/openvault` con las rutas reales que identificaste en el Paso 2.

```yaml
services:
  jellyfin:
    image: jellyfin/jellyfin
    container_name: jellyfin
    user: 1000:1000  # Cambia por tu UID:GID (ejecuta 'id' en terminal)
    network_mode: host  # Mejor para Raspberry Pi
    volumes:
      # Configuración local
      - /home/pi/docker/jellyfin/config:/config
      - /home/pi/docker/jellyfin/cache:/cache
      
      # TUS RUTAS DE OPENVAULT - ¡ESTO ES LO MÁS IMPORTANTE!
      - /srv/dev-disk-by-uuid-XXXXX/movies:/media/movies:ro
      - /srv/dev-disk-by-uuid-XXXXX/series:/media/tv:ro
      
      # Aceleración por hardware (CRUCIAL para Raspberry Pi)
      - /dev/dri:/dev/dri
      
    restart: 'unless-stopped'
    environment:
      - TZ=Europe/Madrid  # ¡AGREGA esto! Cambia por tu zona horaria
```

***

### Configurar Jellyfin

1. **Accede a Jellyfin**: `http://[IP-DE-TU-RASPBERRY]:8096`
2. **Sigue el asistente inicial**:
   * Idioma: Español
   * Crea usuario y contraseña admin
   * Agrega bibliotecas multimedia
3. **Configurar bibliotecas**:
   * **Películas**: Apunta a `/media/movies`
   * **Series**: Apunta a `/media/tv`
   * **Tipo de contenido**: Selecciona el adecuado para cada uno
