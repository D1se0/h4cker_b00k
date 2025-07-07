---
icon: door-open
---

# FTP vsftpd-2.3.4 backdoor

Primero tendremos que descargarnos el repositorio donde se encuentra este `FTP` vulnerable:

URL = [FTP Vuln GitHub](https://github.com/nikdubois/vsftpd-2.3.4-infected)

Nos clonamos el repositorio y entramos en el:

```shell
sudo apt update
apt install git
cd /tmp
git clone https://github.com/nikdubois/vsftpd-2.3.4-infected.git
cd vsftpd-2.3.4-infected/
```

Es importante decir que si tenemos un `FTP` ya activo lo paremos y eliminemos sus archivo para que no haya conflicto.

Ahora antes de hacer un `make` y compilarlo todo, tendremos que hacer una pequeña configuracion para que no de error y tambien tendremos que instalar las herramientas necesarias:

```shell
sudo apt install gcc
sudo apt install build-essential libssl-dev libcrypt-dev
```

Tendremos que realizar la siguiente configuracion:

```shell
nano Makefile

#Dentro del nano
#Cambiar esta linea de aqui:
LIBS = `./vsf_findlibs.sh`
#Por esta de aqui:
LIBS = -lcrypt
```

Lo guardamos y ahora si podremos compilarlo de la siguiente forma:

```shell
make
```

Una vez que se haya compilado tendremos que modificar el siguiente fichero de configuracion del `FTP` para que funcione el `exploit`.

```shell
nano vsftpd.conf

#Dentro del nano
anonymous_enable=YES
local_enable=YES
write_enable=YES
```

Y ahora si ejecutamos el siguiente comando para levantar el servidor de `FTP`:

```shell
sudo ./vsftpd vsftpd.conf
```

Veremos que funciona ya que se queda ahi funcionando, ahora solo tendremos que irnos a `msfconsole` para utilizar el `exploit` llamado `exploit/unix/ftp/vsftpd_234_backdoor` y configurar la `IP` donde esta corriendo el `FTP` de la maquina victima y ya solo tendremos que darle a `exploit`, con esto obtendremos una shell como el usuario `root` directamente.
