---
icon: box-taped
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

# Crear CTF en Docker

## <mark style="color:purple;">Crear maquina vulnerable en un docke</mark>r

### Instalar docker

Primero instalaremos la herramienta `docker`.

```shell
sudo apt install docker-ce
```

Con esto `docker` ya estaria instalado.

### Preparar S.O. para docker

Lo que primero tendremos que hacer es descargarnos la imagen del sistema operativo que vamos a querer utilizar para esa maquina victima mediante la herramienta `docker`.

```shell
docker pull ubuntu:latest
```

Con `latest` lo que decimos es que nos lo descargue en la version mas nueva.

Info:

```
latest: Pulling from library/ubuntu
9c704ecd0c69: Pull complete 
Digest: sha256:2e863c44b718727c860746568e1d54afd13b2fa71b160f5cd9058fc436217b30
Status: Downloaded newer image for ubuntu:latest
docker.io/library/ubuntu:latest
```

Con esto ya tendriamos nuestra base preparada para empezar a configurarla desde ese sistema operativo.

Para comprobar que la imagen del sistema operativo `ubuntu` se instalo bien en `docker` haremos el siguiente comando.

```shell
docker images
```

Info:

```
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
ubuntu       latest    35a88802559d   2 months ago   78.1MB
```

Y veremos que se instalo bien.

### Trabajar con la imagen docker en una shell

Ahora si queremos crearnos una instancia de esa imagen, tendremos que crearnos un contenedor con esa imagen para desplagar una shell sobre ella y poder trabajar.

```shell
docker run -it 35a
```

Info:

```
root@e2764d29611d:/#
```

Pondremos las 3 primeras iniciales del `ID Imagen` del `docker`, por ejemplo mi imagen es `35a88802559d` pues le coloco los 3 primeros numeros `35a`.

Y con esto ya estariamos dentro de la imagen `docker` con una shell, en este punto podemos saber que IP tenemos haciendo...

```shell
hostname -I
```

Info:

```
172.17.0.2
```

Tambien podemos instalar cosas, actualizar los repositorios, etc...

### Crear snapshot de un docker

Cada vez que vayamos avanzando en nuestro trabajo de la maquina vulnerable en un `docker` es recomendable ir haciendo `backups` de la misma por si la liaramos en algun punto, podremos hacerlo de la siguiente forma.

```shell
docker ps
```

Info:

```
CONTAINER ID   IMAGE     COMMAND       CREATED         STATUS         PORTS     NAMES
e2764d29611d   35a       "/bin/bash"   5 minutes ago   Up 5 minutes             youthful_babbage
```

En mi caso el proceso ID seria `e2764d29611d` por lo que hariamso lo siguiente sabiendo esto.

```shell
docker commit e27 snapshot1:latest
```

Y esto creara una imagen del contenedor actual llamada `snapshot1` en `docker` por lo que si listamos las imagenes de los `dockers` tendremos 2, nuestro `docker` principal y despues el `backup` generado del principal.

Si por ejemplo quieres cargar la nueva informacion en la misma `snapshot1` que creamos, lo haremos con el mismo comando indicando siempre la ultima version de nuestr `docker`.

```shell
docker commit e27 snapshot1:latest
```

### Maquina docker terminada importacion a un .tar

Si por ejemplo hemos creado `snapshots` las anteriores se quedaran "huerfanas" pero si nosotros lo importamos en un `.tar` los servicios no se van a quedar adheridos a la `snapshot` por lo que esto es un problema, pero para solucionarlo haremos lo siguiente.

```shell
nano Dockerfile

#Dentro del nano
FROM snapshot1:latest

CMD service ssh start && service apache2 start && service vsftpd start && tail -f /dev/null
```

Donde pone `CMD` tendremos que poner todos los servicios que queramos mantener activos, para que asi aparezcan a la hora de hacer un `nmap` o de intentar vulnerarla.

Tambien hacemos el comando `tail -f /dev/null` para manetener activos los servicios hasta que nosotros lo pausemos.

Ahora si crearemos la imagen `docker` por lo que tendremos que ejecutar el siguiente comando donde este el archivo `Dockerfile`.

```shell
docker build --tag mimaquina .
```

Ahora si ejecutamos `docker images` veremos nuestra maquina `docker` con todos los servicios virtualizados, por lo que tendremos que ver `mimaquina` en las imagenes del `docker`, ahora lo que haremos sera comprimir esa imagen de `mimaquina` en un `.tar`.

```shell
docker save -o mimaquina.tar mimaquina:latest
```

Seleccionamos la imagen `docker` que vamos a pasar al archivo `.tar` en mi caso llamada `mimaquina`.

Y con esto ya estaria hecho, ahora vamos a utilizar un script en `.sh` que te automatiza todo este proceso de montar la imagen `docker` `.tar` a nuestro `docker`.

## <mark style="color:purple;">auto\_mount.sh para montar el docker.tar</mark>

> auto\_mount.sh

```shell
#!/bin/bash

# Colores ANSI
CRE='\033[31m'  # Rojo
CYE='\033[33m'  # Amarillo
CGR='\033[32m'  # Verde
CBL='\033[34m'  # Azul
CBLE='\033[36m' # Cyan
CBK='\033[37m'  # Blanco
CGY='\033[38m'  # Gris
BLD='\033[1m'   # Negrita
CNC='\033[0m'   # Resetear colores

printf "\n" printf "${CRE}___________________¶¶\n" printf "${CRE}____________________¶¶__¶_5¶¶\n" printf "${CRE}____________5¶5__¶5__¶¶_5¶__¶¶¶5\n" printf "${CRE}__________5¶¶¶__¶¶5¶¶¶¶¶5¶¶__5¶¶¶5\n" printf "${CRE}_________¶¶¶¶__¶5¶¶¶¶¶¶¶¶¶¶¶__5¶¶¶¶5\n" printf "${CRE}_______5¶¶¶¶__¶¶¶¶¶¶¶¶¶¶¶_5¶¶__5¶¶¶¶¶5\n" printf "${CRE}______¶¶¶¶¶5_¶¶¶¶¶¶¶¶¶¶¶¶¶5¶¶¶__¶¶¶¶5¶5\n" printf "${CRE}_____¶¶¶¶¶¶_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_¶¶¶¶¶¶¶5\n" printf "${CRE}____¶¶¶¶¶¶¶_¶¶¶5¶¶¶¶5_¶¶¶¶¶5_5¶_¶¶¶¶¶¶¶¶5\n" printf "${CRE}___¶¶¶¶¶¶¶¶__5¶¶¶¶¶¶5___5¶¶¶¶__5¶¶¶¶¶¶¶¶¶5\n" printf "${CRE}__¶¶¶¶¶¶¶¶¶¶5__5¶¶¶¶¶¶5__5¶¶5_5¶¶¶¶¶¶¶¶¶¶¶\n" printf "${CRE}_5¶¶¶¶¶¶¶¶¶¶¶¶_5¶¶¶¶¶¶¶¶¶5__5¶¶¶¶¶¶¶¶¶¶¶¶¶5\n" printf "${CRE}_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_5¶¶¶¶\n" printf "${CRE}5¶¶¶¶¶¶¶¶¶¶¶¶5___5¶¶¶¶¶¶¶5__¶¶¶¶5_¶¶¶5_¶¶¶¶\n" printf "${CRE}¶¶¶¶¶¶¶¶_¶¶5_5¶5__¶¶¶¶¶¶¶¶¶5_5¶¶¶_5¶¶¶_5¶¶¶5\n" printf "${CRE}¶5¶¶¶¶¶5_¶¶_5¶¶¶¶¶_¶¶¶¶¶¶¶¶¶¶5_5¶¶_5¶¶¶_¶¶¶5\n" printf "${CRE}¶¶¶¶_¶¶__¶__¶¶¶¶¶¶5_5¶¶¶¶¶¶¶¶¶¶5_¶¶_5¶¶_5¶¶¶\n" printf "${CRE}¶¶¶5_5¶______5¶¶5¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶5_¶¶_5¶5_¶5¶\n" printf "${CRE}5¶¶____5¶¶¶¶5_____5¶¶¶¶¶¶¶5_¶¶¶¶¶5_¶__¶¶_5¶¶\n" printf "${CRE}_¶¶__5¶¶¶¶¶¶¶¶¶¶5____5¶¶¶¶¶¶_¶¶¶¶¶_____¶5_¶¶\n" printf "${CRE}_¶¶___5¶¶¶¶¶¶¶¶¶__________5¶5_¶¶¶¶¶____¶¶_¶¶\n" printf "${CRE}_¶¶_______5¶¶¶¶¶¶5____________¶¶¶¶¶_____¶_¶¶\n" printf "${CRE}_5¶5________5¶¶_¶¶¶¶5________5¶¶¶¶¶_______¶¶\n" printf "${CRE}__¶¶__________¶___¶¶¶¶¶5___5¶¶¶¶¶¶5_______¶5\n" printf "${CRE}__¶¶____________5¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶________¶\n" printf "${CRE}___¶________________5¶¶¶¶¶¶¶¶5_¶¶\n" printf "${CRE}___¶__________5¶¶¶¶¶¶¶¶5¶¶¶5__5¶5\n" printf "${CRE}_____________________5¶¶¶5____¶5\n" printf "${CNC}\n"
printf "${CBLE}                                           \n"
printf " ##   ##    ##       ####   ###  ##  #######  ######   ####       ##     ######    #####  \n"
printf " ##   ##   ####     ##  ##   ##  ##   ##   #   ##  ##   ##       ####     ##  ##  ##   ## \n"
printf " ##   ##  ##  ##   ##        ## ##    ## #     ##  ##   ##      ##  ##    ##  ##  #       \n"
printf " #######  ##  ##   ##        ####     ####     #####    ##      ##  ##    #####    #####  \n"
printf " ##   ##  ######   ##        ## ##    ## #     ## ##    ##   #  ######    ##  ##       ## \n"
printf " ##   ##  ##  ##    ##  ##   ##  ##   ##   #   ##  ##   ##  ##  ##  ##    ##  ##  ##   ## \n"
printf " ##   ##  ##  ##     ####   ###  ##  #######  #### ##  #######  ##  ##   ######    #####  \n"
printf "${CNC}                                         \n"

# Verificar el número de argumentos
if [ $# -ne 1 ]; then
    echo "Uso: $0 <archivo_tar>"
    exit 1
fi

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo -e "\033[1;36m\nDocker no está instalado. Instalando Docker...\033[0m"
    sudo apt update
    sudo apt install docker.io -y
    echo -e "\033[1;36m\nEstamos habilitando el servicio de docker. Espere un momento...\033[0m"
    sleep 10
    systemctl restart docker && systemctl enable docker
    if [ $? -eq 0 ]; then
        echo "Docker ha sido instalado correctamente."
    else
        echo "Error al instalar Docker. Por favor, verifique y vuelva a intentarlo."
        exit 1
    fi
fi

TAR_FILE="$1"

# Función para detener y eliminar contenedores
detener_y_eliminar_contenedor() {
    IMAGE_NAME="${TAR_FILE%.tar}"
    CONTAINER_NAME="${IMAGE_NAME}_container"

    if [ "$(docker ps -a -q -f name=$CONTAINER_NAME -f status=exited)" ]; then
        docker rm $CONTAINER_NAME > /dev/null
    fi

    if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
        docker stop $CONTAINER_NAME > /dev/null
        docker rm $CONTAINER_NAME > /dev/null
    fi

    if [ "$(docker images -q $IMAGE_NAME)" ]; then
        docker rmi $IMAGE_NAME > /dev/null
    fi

    NETWORK_NAME="dockernetwork"
    if docker network inspect $NETWORK_NAME > /dev/null 2>&1; then
        docker network rm $NETWORK_NAME > /dev/null
    fi
}

# Manejo de la señal INT (Ctrl+C)
trap ctrl_c INT

function ctrl_c() {
    echo -e "\e[1mEliminando el laboratorio, espere un momento...\e[0m"
    detener_y_eliminar_contenedor
    echo -e "\nEl laboratorio ha sido eliminado por completo del sistema."
    exit 0
}

echo -e "\e[1;93m\nEstamos desplegando la máquina vulnerable, espere un momento.\e[0m"
detener_y_eliminar_contenedor
docker load -i "$TAR_FILE" > /dev/null

if [ $? -eq 0 ]; then
    IMAGE_NAME=$(basename "$TAR_FILE" .tar)
    CONTAINER_NAME="${IMAGE_NAME}_container"
    NETWORK_NAME="dockernetwork"

    if docker network inspect $NETWORK_NAME > /dev/null 2>&1; then
        echo -e "\e[38;5;230;1mLa red $NETWORK_NAME ya existe. Eliminándola y recreándola...\e[0m"
        docker network rm $NETWORK_NAME > /dev/null
    fi

    docker network create --internal $NETWORK_NAME > /dev/null

    if uname -a | grep -q arm; then
        apt install --assume-yes binfmt-support qemu-user-static -y > /dev/null
        docker run --privileged --platform linux/amd64 -d --network=$NETWORK_NAME --name $CONTAINER_NAME $IMAGE_NAME > /dev/null
    else
        docker run --privileged -d --network=$NETWORK_NAME --name $CONTAINER_NAME $IMAGE_NAME > /dev/null
    fi

    IP_ADDRESS=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $CONTAINER_NAME)
    echo -e "\e[1;96m\nMáquina desplegada, su dirección IP es --> \e[0m\e[1;97m$IP_ADDRESS\e[0m"
    echo -e "\e[1;91m\nPresiona Ctrl+C cuando termines con la máquina para eliminarla\e[0m"
else
    echo -e "\e[91m\nHa ocurrido un error al cargar el laboratorio en Docker.\e[0m"
    exit 1
fi

# Espera indefinida para que el script no termine
while true; do
    sleep 1
done
```

Se ejecutara de la siguiente forma.

```shell
bash auto_mount.sh <FILE>.tar
```

Y esto montara la imagen en un docker de forma automatica y si queremos eliminarla o pararla y que no nos deje archivos basura, le daremos a `Ctrl+C`.

Y para comprimir las 2 cosas en un archivo `.zip`.

```shell
zip <FILE_ZIP_NAME>.zip <FILE>.tar auto_mount.sh
```

Y esto nos dara el archivo `.zip`.
