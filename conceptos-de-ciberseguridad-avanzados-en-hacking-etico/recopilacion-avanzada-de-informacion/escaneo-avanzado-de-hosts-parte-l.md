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

# Escaneo Avanzado de Hosts - Parte l

Si nosotros queremos realizar un escaneo de red avanzado con `nmap` sin que herramientas de seguridad como `snort` nos detecte dicho escaneo, podremos hacerlo de la siguiente forma:

De primeras intentaremos descubrir los `hosts` que estan activos en la red sin ser detectados:

```shell
sudo nmap -sn -n 192.168.20.0/24
```

Con el `-sn` especificamos que no nos haga un escaneo de puertos, para asi pasar mas desapercibido. Con el `-n` especificamos que no nos haga una resolucion reversa

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-02 10:55 EST
Nmap scan report for 192.168.20.1
Host is up (0.00036s latency).
MAC Address: 00:50:56:C0:00:03 (VMware)
Nmap scan report for 192.168.20.128
Host is up (0.000068s latency).
MAC Address: 00:0C:29:30:9B:3A (VMware)
Nmap scan report for 192.168.20.254
Host is up (0.00033s latency).
MAC Address: 00:50:56:FC:E5:23 (VMware)
Nmap scan report for 192.168.20.129
Host is up.
Nmap done: 256 IP addresses (4 hosts up) scanned in 1.92 seconds
```

Vemos que nos muestra los `hosts` y si nos vamos a nuestro `Snort` veremos que no ha capturado nada, por lo que hemos pasado desapercibidos.

Ya que esto solo genera trafico `ARP` y no `TCP` por lo que pasamos de largo con el `IDS`.

Pero este metodo no es efectivo en absolutamente todas las herramientas, ya que si tienen configuraciones mas avanzadas los `IDS` podrian realizar un `ARP Spoofing` y engañarnos sobre los `hosts` que estan `UP` y los que no, haciendo asi imposible la tarea de detectar `hosts` activos, podremos probarlo con un script muy sencillito que vamos a lanzar en nuestro `kali`, que seria el siguiente:

> arp\_scan\_spoof.py

```python
#!/usr/bin/python3

from scapy.all import *

# Manejar paquetes ARP
def handle_packet(packet):
    # Verifica si es un paquete ARP y si es una solicitud ARP (op=1)
    if ARP in packet and packet[ARP].op == 1:  
        # Verifica si la dirección IP de destino coincide
        if packet[ARP].pdst == "192.168.20.152":
            print("Interceptada solicitud ARP para 192.168.20.152")
            
            # Construye una respuesta ARP falsa
            reply = ARP(op=2,  # Respuesta ARP
                        hwsrc="00:0C:29:3D:1D:6F",  # Dirección MAC inventada
                        psrc="192.168.20.152",      # IP suplantada
                        hwdst=packet[ARP].hwsrc,    # MAC de quien envió la solicitud
                        pdst=packet[ARP].psrc)      # IP de quien envió la solicitud
            
            # Empaqueta la respuesta con la capa Ethernet
            pkt = Ether(dst=packet[Ether].src, src="00:0C:29:3D:1D:6F") / reply
            
            # Envía el paquete
            sendp(pkt, verbose=False)
            print("Respuesta ARP enviada")

# Escucha paquetes ARP en la red
try:
    sniff(filter="arp", prn=handle_packet)
except KeyboardInterrupt:
    print("\nDetenido por el usuario.")
```

Estas secciones de aqui nos las inventamos con las `IP's/MAC's` que queramos:

```python
if packet[ARP].pdst == "192.168.20.152":
hwsrc="00:0C:29:3D:1D:6F",
psrc="192.168.20.152",
src="00:0C:29:3D:1D:6F"
```

Si ahora nosotros ejecutamos el script:

```shell
sudo python3 arp_scan_spoof.py
```

Se va a quedar a la escucha, por lo que nosotros volveremos a lanzar la peticion de `nmap`:

```shell
sudo nmap -sn -n 192.168.20.0/24
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-02 11:24 EST
Nmap scan report for 192.168.20.1
Host is up (0.00049s latency).
MAC Address: 00:50:56:C0:00:03 (VMware)
Nmap scan report for 192.168.20.128
Host is up (0.00017s latency).
MAC Address: 00:0C:29:30:9B:3A (VMware)
Nmap scan report for 192.168.20.152
Host is up (0.030s latency).
MAC Address: 00:0C:29:3D:1D:6F (VMware)
Nmap scan report for 192.168.20.254
Host is up (0.000078s latency).
MAC Address: 00:50:56:FC:E5:23 (VMware)
Nmap scan report for 192.168.20.129
Host is up.
Nmap done: 256 IP addresses (5 hosts up) scanned in 1.92 seconds
```

Vemos que a parte de mostrarnos que la `128` esta `UP` tambien nos esta diciendo que la `152` que nosotros nos hemos inventado tambien esta `UP`, por lo que nos esta engañando el escaneo de `ARP` y esto se puede hacer de forma masiva con distintas IP's inventadas.

Y si vemos en donde esta la escucha de nuestro script de `python3` veremos lo siguiente:

```
Interceptada solicitud ARP para 192.168.20.152
Respuesta ARP enviada
```

Ahora lo que podemos hacer para que no nos engañen con este tipo de tecnica en los `hosts` que encuentre sin que la herramienta `snort` la detecte, comprobar mediante el protocolo `TCP` si realmente esta levantado esa IP sin sufrir ningun tipo de engaño mediante el `ARP`, podremos hacerlo de la siguiente forma:

```shell
nmap -sn -n -PS 192.168.20.0/24
```

Con el `-PS` lo que estamos haciendo es validar con el puerto `80` si realmente esta levantado ese `host`, para no caer en la trampa de ningun `ARP Spoofing`.

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-02 11:38 EST
Nmap scan report for 192.168.20.128
Host is up (0.000092s latency).
MAC Address: 00:0C:29:30:9B:3A (VMware)
Nmap scan report for 192.168.20.129
Host is up.
Nmap done: 256 IP addresses (2 hosts up) scanned in 1.95 seconds
```

Y vemos que `Snort` no nos detecto.
