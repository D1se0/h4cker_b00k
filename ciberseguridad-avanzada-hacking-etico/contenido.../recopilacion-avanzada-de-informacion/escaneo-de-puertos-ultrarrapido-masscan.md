---
icon: filters
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

# Escaneo de puertos ultrarrápido - Masscan

En este caso esta herramienta no es que sirva para pasar desapercibido de las herramientas de `IDS` si no que, es para realizar un escaneo a gran escala en el menor tiempo posible y seria con la siguiente herramienta que encontraremos en el siguiente link:

URL = [Masscan GitHub](https://github.com/robertdavidgraham/masscan)

Esta herramienta ya viene por defecto en `kali`.

Lo que podemos hacer con esta herramienta es realizar un escaneode todo `internet` entero en menos de 5 minutos, lanzando mas de `10 millones` de paquetes de red a la vez, por lo que para escanear nuestra red local, podremos hacerlo de la siguiente forma:

```shell
sudo masscan 192.168.5.0/24 -p80 --interface eth0
```

En este caso solo que nos escanee los puertos `80` de toda la red.

```
Starting masscan 1.3.2 (http://bit.ly/14GZzcT) at 2025-01-04 10:10:32 GMT
Initiating SYN Stealth Scan
Scanning 256 hosts [1 port/host]
Discovered open port 80/tcp on 192.168.5.206 
```

Tambien le podemos deslimitar y que en vez de que envie `100` paquetes por segundo, establecerle que haga `1000` paquetes por segundo.

```shell
sudo masscan 192.168.5.0/24 -p80 --interface eth0 --rate 10000
```

Si queremos especificarle un rango de puertos, lo podremos hacer de la siguiente forma:

```shell
sudo masscan 192.168.5.0/24 -p1-1000 --interface eth0
```

Si por ejemplo tenemos que pausar el escaneo, podremos hacerlo con `Ctrl+C` y se nos guardara el escaneo en un `paused.conf`:

```
Starting masscan 1.3.2 (http://bit.ly/14GZzcT) at 2025-01-04 10:15:16 GMT
Initiating SYN Stealth Scan
Scanning 256 hosts [1000 ports/host]
^Cwaiting several seconds to exit...                                            
saving resume file to: paused.conf
```

Para retomarlo mas tarde, pero ahora para retomar el escaneo, podremos hacer lo siguiente:

```shell
sudo masscan --resume paused.conf
```

Si os diera este error de aqui:

```
CONF: unknown config option: nocapture=servername
```

Tendremos que instalar la herramienta a la maxima version que hay, de la siguiente forma, ya que en la que viene por defecto tiene ese fallo.

```shell
sudo apt remove masscan
sudo apt-get --assume-yes install git make gcc
git clone https://github.com/robertdavidgraham/masscan
cd masscan
make
sudo make install
cd ..
sudo rm -r masscan
```

Y si ahora hacemos:

```shell
masscan -h
```

Vemos que se instalo correctamente y que tiene una version mas moderna del que teniamos ya, y si intentamos restaurar la sesion de escaneo, veremos lo siguiente:

```
Starting masscan 1.3.9-integration (http://bit.ly/14GZzcT) at 2025-01-04 10:24:50 GMT
Initiating SYN Stealth Scan
Scanning 256 hosts [1000 ports/host]
```

Vemos que se restaura correctamente.

Tambien le podemos decir a esta herramienta que nos escane el numero de puertos mas comunes, como haciamos con `nmap`:

```shell
sudo masscan 192.168.5.0/24 --top-ports 100 --interface eth0 --rate 10000
```

Con esto lo que estamos haciendo es que nos haga un escaneo de los `100` puertos mas comunes.
