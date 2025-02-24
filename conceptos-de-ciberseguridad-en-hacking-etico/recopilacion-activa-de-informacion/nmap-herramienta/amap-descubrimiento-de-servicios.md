---
icon: map
---

# Amap (descubrimiento de servicios)

`amap` es una herramienta como `nmap` pero en tal caso de que queramos corroborar la informacion de `nmap`, podremos utilizar como herramienta secundaria `amap`, por defecto no viene instalada en `kali`, por lo que la instalaremos:

```shell
sudo apt-get install amap
```

Primero crearemos el fichero con `nmap`.

```shell
sudo nmap -v --reason -sS -oA servicios.amap 192.168.16.129
```

Una vez echo esto, nos generara 3 archivos:

```
servicios.amap.gnmap
servicios.amap.nmap
servicios.amap.xml
```

Ahora utilizaremos `amap` con un fichero, para que testee los servicios, consultando dichos puertos de los banners para asi saber que versiones y servicios estan corriendo en didchos puertos.

```shell
amap -i servicios.amap.gnmap -B
```

Info:

```
amap v5.4 (www.thc.org/thc-amap) started at 2024-11-11 04:37:01 - BANNER mode

Banner on 192.168.16.129:22/tcp : SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13\r\n

amap v5.4 finished at 2024-11-11 04:37:12
```

Con esto nos muestra informacion del los puertos que pueda `amap`, esta claro que es mucho mejor `nmap` pero esta puede ser como herramienta secundaria.
