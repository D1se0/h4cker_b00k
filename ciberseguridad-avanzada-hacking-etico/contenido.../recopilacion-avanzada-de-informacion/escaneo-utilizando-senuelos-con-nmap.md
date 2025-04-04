---
icon: blueberries
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

# Escaneo utilizando señuelos con Nmap

Lo que podemos hacer es realizar un señuelo de escaneo de puertos, el cual consiste en especificar una IP que exista y que este levantado, como por ejemplo puede ser el del `router` para engañar al `IDS`(Snort) y creer que lo esta realizando el `router` en vez de nuestra IP, se haria de la siguiente forma:

```shell
sudo nmap -sS -n -D 192.168.20.1,ME 192.168.20.128
```

Con el `ME` especificamos que haga nuestra IP el escaneo despues con la `128`.

Aqui lo que estamos haciendo es con el `-D` especificar que haga un `Decoy Scan` y en este punto se le pueden especificar mas direcciones IP, pero en mi caso solo tengo esas, por lo que se hara como en el ejemplo, si vemos la salida de `nmap`:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-03 04:10 EST
Nmap scan report for 192.168.20.128
Host is up (0.0016s latency).
Not shown: 997 closed tcp ports (reset)
PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh
80/tcp open  http
MAC Address: 00:0C:29:30:9B:3A (VMware)

Nmap done: 1 IP address (1 host up) scanned in 0.30 seconds
```

Veremos que nos escaneo los puertos del `host`, pero si nos vamos a nuestro `Snort` veremos lo siguiente:

```
01/03-10:10:53.910154  [**] [122:1:1] (portscan) TCP Portscan [**] [Classification: Attempted Information Leak] [Priority: 2] {PROTO:255} 192.168.20.1 -> 192.168.20.128
```

Claramente nos ha detectado que ha sido un escaneo de puertos, pero como se ve no esta apuntando a nuestra direccion IP, si no a la del `router` como si fuera el, el que lo esta realizando.
