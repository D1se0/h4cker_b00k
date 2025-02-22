---
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

# Escaneo en IPv6 con Nmap

Si nosotros queremos que `nmap` realice un escaneo de `IPv6` en vez de de `IPv4` tendremos que especificarselo con el parametro `-6` para que haga dicho escaneo.

Pero antes tendremos que identificar esa `IPv6` de ese `host` en concreto, para ello podremos hacer un escaneo de `IPv6` de `host` de la siguiente forma:

> Lo que vamos hacer es hacer `direcciones Multicast`.

<figure><img src="../../.gitbook/assets/image (125).png" alt=""><figcaption></figcaption></figure>

En nuestro caso elegiremos la primera `ff02::1` ya que es para escanear todos los `nodos` de nuestra red local y el segundo seria para todos los `routers` y asi sucesivamente dependiendo de que objetivo de escaneo queramos realizar.

```shell
ping6 ff02::1
```

Con esto vamos a realizar trafico en el protocolo `ICMP` pero al hacer esto `Snort` no nos lo va a detectar y veremos lo siguiente en la terminal.

```
PING ff02::1 (ff02::1) 56 data bytes
64 bytes from fe80::126b:3f32:5e50:9e6%eth0: icmp_seq=1 ttl=64 time=0.097 ms
64 bytes from fe80::20c:29ff:fe30:9b3a%eth0: icmp_seq=1 ttl=64 time=1.21 ms
64 bytes from fe80::126b:3f32:5e50:9e6%eth0: icmp_seq=2 ttl=64 time=0.040 ms
64 bytes from fe80::20c:29ff:fe30:9b3a%eth0: icmp_seq=2 ttl=64 time=0.467 ms
64 bytes from fe80::126b:3f32:5e50:9e6%eth0: icmp_seq=3 ttl=64 time=0.039 ms
64 bytes from fe80::20c:29ff:fe30:9b3a%eth0: icmp_seq=3 ttl=64 time=0.380 ms
^C
--- ff02::1 ping statistics ---
3 packets transmitted, 3 received, +3 duplicates, 0% packet loss, time 2023ms
rtt min/avg/max/mdev = 0.039/0.371/1.208/0.409 ms
```

Vemos que nos esta respondiendo un `nodo` con su `IPv6` por lo que ya la habriamos identificado que sria la siguiente `fe80::20c:29ff:fe30:9b3a`:

Igualmente podremos identificar la direccion con el siguiente comando:

```shell
ip neigh
```

Info:

```
192.168.20.254 dev eth0 lladdr 00:50:56:f0:2c:a7 STALE 
fe80::20c:29ff:fe30:9b3a dev eth0 lladdr 00:0c:29:30:9b:3a STALE
```

Esto lo que te muestra es los `ping's` guardados de las maquinas que te han respondido con la `IP` correspondiente a la cual lo hayas echo.

Para realizar el escaneo con la direccion `IPv6` seria de la siguiente forma:

```shell
sudo nmap -sS -n -6 fe80::20c:29ff:fe30:9b3a -e eth0
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-04 04:15 EST
Nmap scan report for fe80::20c:29ff:fe30:9b3a
Host is up (0.0026s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
MAC Address: 00:0C:29:30:9B:3A (VMware)

Nmap done: 1 IP address (1 host up) scanned in 0.26 seconds
```

Si algunos puertos no nos lo encuentra es por que no soportan `IPv6`.
