---
icon: fingerprint
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

# Spoofing de la identidad del atacante con Nmap

Nosotros con un escaneo y con el parametro `-S` podremos `Spoofear` una IP que nosotros escojamos a poder ser una que este activa, ya que si elegimos una que no este activa cuando llegue un analista a investigar lo que ha pasado puede darse cuenta de que ha sido un `Spoofing` por lo que utilizaremos la que generalmente siempre esta activa que seria la `.1` la del `router` u otra que hayamos descubierto en el reconocimiento de `Hosts Discovery`:

```shell
sudo nmap -Pn -S 192.168.20.1 -n -e eth0 192.168.20.128
```

Tambien tendremos que especificar el parametro `-Pn` ya que depende de `-S`. Con el `-e` especificamos la interfaz de red nuestra la cual cogera nuestra direccion `MAC` para enviarnos la informacion, ya que si tambien modificamos la `MAC` cuando nos responda con la informacion la `128` le llegara a la `1` y no a nuestra IP ya que se hace mediante `ARP`, por lo que la direccion `MAC` tiene que ser la nuestra para que nos llegue la informacion a nosotros, pero la IP la estaremos cambiando con el `-S`.

En tal caso de que se tuviera la version de `nmap` (7.92 o 7.94) no va a funcionar este tipo de escaneos ya que hay un fallo en la herramienta, por lo que instalaremos una version mas antigua de `nmap` de la siguiente forma:

URL = [Download Nmap 7.91](https://packages.debian.org/bookworm/amd64/nmap/download)

Ahora tendremos que desinstalar `nmap`:

```shell
sudo apt-get remove nmap
```

Y ejecutamos lo siguiente:

```shell
sudo dpkg -i <FILE>.deb
```

Y con esto ya podriamos volverlo a lanzar.

Si hubiera alguna restriccion en algun puerto en el cual te corta el escaneo podemos redirigir un puerto a otro, para `Bypassear` esa restriccion:

```shell
sudo nmap -Pn -S 192.168.20.1 -n -e eth0 --source-port 80 -p21 192.168.20.128
```

Aqui lo que estamos haciendo es escanear el puerto `21` pero haciendo creer al `IDS` que estamos escaneando el puerto `80` pasando de largo esa restriccion del puerto `21`.

Para volver a la version en la que estabamos con `nmap` solo tendremos que hacer lo siguiente:

```shell
sudo apt-get install nmap
```
