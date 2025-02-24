---
icon: box-check
---

# TCPdump

Esta herramienta va por terminal solamente, viene con `kali` por defecto y es como `wireshark` solo que por terminal, es una herramienta muy completita.

Si ponemos:

```shell
sudo tcpdump -D
```

Nos mostrara las interfaces que tenemos activas.

```
1.eth0 [Up, Running, Connected]
2.any (Pseudo-device that captures on all interfaces) [Up, Running]
3.lo [Up, Running, Loopback]
4.docker0 [Up, Disconnected]
5.bluetooth-monitor (Bluetooth Linux Monitor) [Wireless]
6.nflog (Linux netfilter log (NFLOG) interface) [none]
7.nfqueue (Linux netfilter queue (NFQUEUE) interface) [none]
8.dbus-system (D-Bus system bus) [none]
9.dbus-session (D-Bus session bus) [none]
```

Para estar a la escucha y empezar a capturar paquetes de `red` podremos hacer de la siguiente forma:

```shell
sudo tcpdump -i eth0
```

Con el `-i` especificamos en la interfaz de `red` en la que queremos escuchar.

Si ahora mismo buscamos algo o generamos trafico de `red` esta herramienta lo capturara todo y lo mostrara por terminal todo el flujo de `red`.

Si queremos ver mas informacion que simplemente conexiones de un sitio a otro, podremos hacerlo con el parametro `-v` (`verbose`):

```shell
sudo tcpdump -v -i eth0
```

Si por ejemplo queremos filtrar por el trafico `ICPM` podremos hacerlo de la siguiente forma:

> Explicacion de lo que es `ICMP`

```
> ICMP (Internet Control Message Protocol) es un protocolo de red usado para enviar mensajes de control y diagnóstico entre dispositivos en una red IP.

> Su propósito es notificar problemas de comunicación, informar errores y diagnosticar la conectividad.

> Mensajes ICMP comunes:
    - Echo Request y Echo Reply: usados por "ping" para verificar conectividad.
    - Destination Unreachable: informa cuando un paquete no puede llegar a su destino.
    - Time Exceeded: indica que un paquete superó su tiempo de vida (TTL).

> Es esencial para el monitoreo y mantenimiento de la red, pero también puede representar riesgos de seguridad, por lo que a veces se limita o bloquea.

Es un protocolo auxiliar para la gestión de la red, no para transferir datos de usuario.
```

```shell
sudo tcpdump icmp
```

Y si por ejemplo buscamos en internet no aparecera nada, pero si abrimos una terminal y ponemos:

```shell
ping www.google.com
```

Nos mostrara en la herramienta `tcpdump` la informacon `ICMP` de lo que esta capturando con el otro comando, ya que se estaria generando trafico `ICMP`.

Si por ejemplo queremos filtrar el que solo muestre el trafico de `red` de un `host` en concreto (De un dominio o IP) podremos hacerlo de la siguiente forma:

```shell
sudo tcpdump host 10.10.11.11
```

Si buscamos esa IP en internet que se supone que nos devuelve una pagina web, solo nos mostrara ese trafico, pero si buscamos otra cosa que no sea con esa IP no nos mostrara nada.

Si todo el trafico de `red` queremos volcarlo a un fichero `.pcap` para luego poder verlo en `wireshark` podremos hacerlo de la siguiente forma:

```shell
sudo tcpdump -i eth0 -w Desktop/capture.pcap
```

Y esto estara a la escucha monitoreando todo el trafico de `red` que este pasando por `eth0`, cuando queramos dejar de capturar y que nos genere el archivo, haremos `Ctrl+C` y ya nos habria generado el archivo con todo el trafico capturado.

Si le damos doble click al fichero se nos abrira con `wireshark`, pero si queremos leer el fichero con `tcpdump` lo haremos de la siguiente forma:

```shell
sudo tcpdump -r Desktop/capture.pcap
```

Y con esto nos mostrara todo lo que ha capturado por terminal.

Si queremos filtrar todos los paquetes que van dirigidos al puerto `53` que seria el `DNS` sobre la captura que realizamos anteriormente del `.pcap` podremos hacerlo de la siguiente forma:

```shell
sudo tcpdump -n port 53 -v -r Desktop/capture.pcap
```

Si por ejemplo queremos filtrar por otro puerto que tiene mucha mas informacion, pero solo queremos una informacion especifica de todo ese `trafico de red` lo haremos de la siguiente forma:

```shell
sudo tcpdump -n port 80 -v -r Desktop/capture.pcap | grep phrack.org
```

Donde esta `phrack.org` se le grepea por lo que queramos filtrar.

Y con esto nos mostrara solamente la informacion de lo que ha encontrado con ese dominio.
