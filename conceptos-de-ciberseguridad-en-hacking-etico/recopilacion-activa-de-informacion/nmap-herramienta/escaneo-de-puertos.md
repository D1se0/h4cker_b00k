---
icon: weight-scale
---

# Escaneo de puertos

Es muy importante este paso ya que con ello podemos determinar que puertos estan corriendo en dicha maquina, para investigar las posibles vulnerabilidades de dicha maquina.

Cada puerto esta identificado con un numero, en el que estara corriendo una aplicacion en concreto, dependiendo de la maquina puede estar corriendo o no, tambien se les puede cambiar las aplicaciones de dicho puerto a otro para camuflarlo y que asi sea mas dificil de detectar que tipo de aplicacion es.

Los puertos pueden estar `open` significaria que hay una aplicacion corriendo en dicho puerto, `Closed` significa que no hay nada corriendo ahi, `Filtered` significa que hay una aplicacion corriendo ahi, pero que esta protegido por un `firewall` por lo que no es accesible directamente, etc...

Con el parametro `-sS` en `nmap` lo que haria sera hacer una peticion de forma individual a cada puerto que este escaneando, tanto si le especificamos que sea a todos los puertos `-p-` como si es a un puerto en especifico `-p 21`, con esto lo que hacemos es no realizar tanta interaccion de trafico de red dejando a median el `three-way handshake` cuando ya sabemos que dicho/s puerto/s esta/n abierto/s.

```shell
sudo nmap -sS 192.168.16.129 -p 80
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-11 03:22 EST
Nmap scan report for 192.168.16.129
Host is up (0.00051s latency).

PORT   STATE SERVICE
80/tcp open  http
MAC Address: 00:0C:29:29:E7:FF (VMware)

Nmap done: 1 IP address (1 host up) scanned in 13.21 seconds
```

Lo que estamos viendo aqui es que encontramos que el puerto esta `open` por lo que si esta corriendo una aplicacion en el puerto `80`, tambien nos dice que probablemente este corriendo un `HTTP` pero no nos lo garantiza.

Si queremos escanear todos los puertos de todos los `nodos` de un segmento de red, lo que podremos hacer es lo siguiente:

```shell
sudo nmap -sS 192.168.16.0/24 
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-11 03:30 EST
Nmap scan report for 192.168.16.1
Host is up (0.00065s latency).
Not shown: 997 filtered tcp ports (no-response)
PORT    STATE SERVICE
135/tcp open  msrpc
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds
MAC Address: 00:50:56:C0:00:01 (VMware)

Nmap scan report for 192.168.16.129
Host is up (0.00038s latency).
Not shown: 991 filtered tcp ports (no-response)
PORT     STATE  SERVICE
21/tcp   open   ftp
22/tcp   open   ssh
80/tcp   open   http
445/tcp  open   microsoft-ds
631/tcp  open   ipp
3000/tcp closed ppp
3306/tcp open   mysql
8080/tcp open   http-proxy
8181/tcp closed intermapper
MAC Address: 00:0C:29:29:E7:FF (VMware)

Nmap scan report for 192.168.16.132
Host is up (0.00045s latency).
Not shown: 981 closed tcp ports (reset)
PORT      STATE SERVICE
21/tcp    open  ftp
22/tcp    open  ssh
80/tcp    open  http
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
3389/tcp  open  ms-wbt-server
4848/tcp  open  appserv-http
7676/tcp  open  imqbrokerd
8009/tcp  open  ajp13
8080/tcp  open  http-proxy
8181/tcp  open  intermapper
8383/tcp  open  m2mservices
9200/tcp  open  wap-wsp
49152/tcp open  unknown
49153/tcp open  unknown
49154/tcp open  unknown
49155/tcp open  unknown
49176/tcp open  unknown
MAC Address: 00:0C:29:EC:1E:B9 (VMware)

Nmap scan report for 192.168.16.254
Host is up (0.00053s latency).
All 1000 scanned ports on 192.168.16.254 are in ignored states.
Not shown: 1000 filtered tcp ports (no-response)
MAC Address: 00:50:56:EB:95:6A (VMware)

Nmap scan report for 192.168.16.128
Host is up (0.0000060s latency).
All 1000 scanned ports on 192.168.16.128 are in ignored states.
Not shown: 1000 closed tcp ports (reset)

Nmap done: 256 IP addresses (5 hosts up) scanned in 60.33 seconds
```

Con esto lo que nos esta mostrando es que encontro en la maquina `192.168.16.129` todos esos puertos abiertos y en la maquina `192.168.16.132` todos esos puertos abiertos, escaneando asi todos los hosts que estan activos en el segmento de red y seguidamente sus puertos activos, esto claramente genera un volumen enorme de trafico en la red.

Si queremos delimitarle dentro del rango de red, un rango especifico de `IP's` podremos hacerlo de la siguiente forma:

```shell
sudo nmap -sS 192.168.16.125-135
```

Con esto lo que hacemos es limitar la busqueda entre el `192.168.16.125` hasta el `192.168.16.135`.

Si nosotros queremos generar un reporte de forma profesional sobre la informacion de los `hosts`, los puertos, etc... Lo podremos hacer de la siguiente forma:

```shell
sudo nmap -v --reason -sS -oX puertos.xml --stylesheet="https://svn.nmap.org/nmap/docs/nmap.xsl" 192.168.16.125-135
```

Con `-v` especificamos que nos de mas informacion del escaneo que esta realizando. Con `--reason` especificamos que nos de informacion de por que motivo los puertos estan abiertos, cerrados, filtrados, etc... Con `-oX` lo que hacemos es exportar toda esta informacion que nos proporcione `nmap` a un fichero como le llamemos de extension `XML`. Con `--stylesheet=` lo que hacemos es especificarle que un estilo para el reporte que nos genere y no se vea tan crudo, en mi caso es u nestilo que ya nos proporciona `nmap` en dicha URL.

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-11 03:43 EST
Initiating ARP Ping Scan at 03:43
Scanning 10 hosts [1 port/host]
Completed ARP Ping Scan at 03:43, 1.25s elapsed (10 total hosts)
Initiating Parallel DNS resolution of 2 hosts. at 03:43
Completed Parallel DNS resolution of 2 hosts. at 03:43, 13.00s elapsed
Nmap scan report for 192.168.16.125 [host down, received no-response]
Nmap scan report for 192.168.16.126 [host down, received no-response]
Nmap scan report for 192.168.16.127 [host down, received no-response]
Nmap scan report for 192.168.16.130 [host down, received no-response]
Nmap scan report for 192.168.16.131 [host down, received no-response]
Nmap scan report for 192.168.16.133 [host down, received no-response]
Nmap scan report for 192.168.16.134 [host down, received no-response]
Nmap scan report for 192.168.16.135 [host down, received no-response]
Initiating Parallel DNS resolution of 1 host. at 03:43
Completed Parallel DNS resolution of 1 host. at 03:44, 13.00s elapsed
Initiating SYN Stealth Scan at 03:44
Scanning 2 hosts [1000 ports/host]
Discovered open port 3306/tcp on 192.168.16.129
Discovered open port 445/tcp on 192.168.16.129
Discovered open port 3389/tcp on 192.168.16.132
Discovered open port 80/tcp on 192.168.16.132
Discovered open port 80/tcp on 192.168.16.129
Discovered open port 22/tcp on 192.168.16.132
Discovered open port 135/tcp on 192.168.16.132
Discovered open port 21/tcp on 192.168.16.132
Discovered open port 22/tcp on 192.168.16.129
Discovered open port 8080/tcp on 192.168.16.132
Discovered open port 139/tcp on 192.168.16.132
Discovered open port 4848/tcp on 192.168.16.132
Discovered open port 8181/tcp on 192.168.16.132
Discovered open port 49154/tcp on 192.168.16.132
Discovered open port 7676/tcp on 192.168.16.132
Discovered open port 445/tcp on 192.168.16.132
Discovered open port 8383/tcp on 192.168.16.132
Discovered open port 49155/tcp on 192.168.16.132
Discovered open port 8009/tcp on 192.168.16.132
Discovered open port 49176/tcp on 192.168.16.132
Discovered open port 9200/tcp on 192.168.16.132
Discovered open port 49153/tcp on 192.168.16.132
Discovered open port 21/tcp on 192.168.16.129
Discovered open port 8080/tcp on 192.168.16.129
Discovered open port 49152/tcp on 192.168.16.132
Completed SYN Stealth Scan against 192.168.16.132 in 1.34s (1 host left)
Discovered open port 631/tcp on 192.168.16.129
Completed SYN Stealth Scan at 03:44, 4.78s elapsed (2000 total ports)
Nmap scan report for 192.168.16.129
Host is up, received arp-response (0.00056s latency).
Not shown: 991 filtered tcp ports (no-response)
PORT     STATE  SERVICE      REASON
21/tcp   open   ftp          syn-ack ttl 64
22/tcp   open   ssh          syn-ack ttl 64
80/tcp   open   http         syn-ack ttl 64
445/tcp  open   microsoft-ds syn-ack ttl 64
631/tcp  open   ipp          syn-ack ttl 64
3000/tcp closed ppp          reset ttl 64
3306/tcp open   mysql        syn-ack ttl 64
8080/tcp open   http-proxy   syn-ack ttl 64
8181/tcp closed intermapper  reset ttl 64
MAC Address: 00:0C:29:29:E7:FF (VMware)

Nmap scan report for 192.168.16.132
Host is up, received arp-response (0.00011s latency).
Not shown: 981 closed tcp ports (reset)
PORT      STATE SERVICE       REASON
21/tcp    open  ftp           syn-ack ttl 128
22/tcp    open  ssh           syn-ack ttl 128
80/tcp    open  http          syn-ack ttl 128
135/tcp   open  msrpc         syn-ack ttl 128
139/tcp   open  netbios-ssn   syn-ack ttl 128
445/tcp   open  microsoft-ds  syn-ack ttl 128
3389/tcp  open  ms-wbt-server syn-ack ttl 128
4848/tcp  open  appserv-http  syn-ack ttl 128
7676/tcp  open  imqbrokerd    syn-ack ttl 128
8009/tcp  open  ajp13         syn-ack ttl 128
8080/tcp  open  http-proxy    syn-ack ttl 128
8181/tcp  open  intermapper   syn-ack ttl 128
8383/tcp  open  m2mservices   syn-ack ttl 128
9200/tcp  open  wap-wsp       syn-ack ttl 128
49152/tcp open  unknown       syn-ack ttl 128
49153/tcp open  unknown       syn-ack ttl 128
49154/tcp open  unknown       syn-ack ttl 128
49155/tcp open  unknown       syn-ack ttl 128
49176/tcp open  unknown       syn-ack ttl 128
MAC Address: 00:0C:29:EC:1E:B9 (VMware)

Initiating SYN Stealth Scan at 03:44
Scanning 192.168.16.128 [1000 ports]
Completed SYN Stealth Scan at 03:44, 0.03s elapsed (1000 total ports)
Nmap scan report for 192.168.16.128
Host is up, received localhost-response (0.0000020s latency).
All 1000 scanned ports on 192.168.16.128 are in ignored states.
Not shown: 1000 closed tcp ports (reset)

Read data files from: /usr/bin/../share/nmap
Nmap done: 11 IP addresses (3 hosts up) scanned in 32.17 seconds
           Raw packets sent: 4071 (178.836KB) | Rcvd: 3013 (124.608KB)
```

Y con esto a parte de mostrarnos la informacion por terminal, tambien nos habra generado el archivo que especificamos que nos creara antes con estilos.

!\[\[Pasted image 20241111095241.png]]

Si queremos hacer el `three-way handshake` entero sin que se quede a median como haciamos con el `-sS` podremos hacerlo de la siguiente forma:

```shell
sudo nmap -sT 192.168.16.129 -p 80
```

Con el `-sT` lo que hacemos es que haga todos los pasos del `three-way handshake` de comprobaciones.

Claramente es mucho mejor el `-sS` ya que genera menos trafico de red.

De normal los escaneo de puertos, se suelen hacer enviando paquetes `TCP` que es lo mas normal, solo que hay veces en los que los puertos estan en `UDP`, y `TCP` no llega a descubrirlo bien ya que esta por otro protocolo de red, por lo que si queremos enviar paquetes `UDP` podremos hacerlo de la siguiente forma:

```shell
sudo nmap -sU 192.168.16.129 -p 53
```

Con el `-sU` lo que hacemos es hacer un escaneo en el protocolo `UDP` en el puerto `53`.

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-11 04:02 EST
Nmap scan report for 192.168.16.129
Host is up (0.00070s latency).

PORT   STATE         SERVICE
53/udp open|filtered domain
MAC Address: 00:0C:29:29:E7:FF (VMware)

Nmap done: 1 IP address (1 host up) scanned in 13.49 seconds
```

Como se puede ver lo esta haciendo mediante `UDP` (`53/udp`).

En este caso para notificar a `nmap` que no esta abierto el puerto, en tal caso de que no lo estuviera, le envia un `ICMP` como diciendo que no esta activo y seguidamente corta conexion.

> NOTA Puertos Info:

```
Nmap: Estados de los puertos

Estados en los que pueden encontrarse los puertos:

**open**

An application is actively accepting TCP connections, UDP datagrams or SCTP associations on this port. Finding these is often the primary goal of port scanning. Security-minded people know that each open port is an avenue for attack. Attackers and pen-testers want to exploit the open ports, while administrators try to close or protect them with firewalls without thwarting legitimate users. Open ports are also interesting for non-security scans because they show services available for use on the network.

**closed**

A closed port is accessible (it receives and responds to Nmap probe packets), but there is no application listening on it. They can be helpful in showing that a host is up on an IP address (host discovery, or ping scanning), and as part of OS detection. Because closed ports are reachable, it may be worth scanning later in case some open up. Administrators may want to consider blocking such ports with a firewall. Then they would appear in the filtered state, discussed next.

**filtered**

Nmap cannot determine whether the port is open because packet filtering prevents its probes from reaching the port. The filtering could be from a dedicated firewall device, router rules, or host-based firewall software. These ports frustrate attackers because they provide so little information. Sometimes they respond with ICMP error messages such as type 3 code 13 (destination unreachable: communication administratively prohibited), but filters that simply drop probes without responding are far more common. This forces Nmap to retry several times just in case the probe was dropped due to network congestion rather than filtering. This slows down the scan dramatically.

**unfiltered**

The unfiltered state means that a port is accessible, but Nmap is unable to determine whether it is open or closed. Only the ACK scan, which is used to map firewall rulesets, classifies ports into this state. Scanning unfiltered ports with other scan types such as Window scan, SYN scan, or FIN scan, may help resolve whether the port is open.

**open|filtered**

Nmap places ports in this state when it is unable to determine whether a port is open or filtered. This occurs for scan types in which open ports give no response. The lack of response could also mean that a packet filter dropped the probe or any response it elicited. So Nmap does not know for sure whether the port is open or being filtered. The UDP, IP protocol, FIN, NULL, and Xmas scans classify ports this way.

**closed|filtered**

This state is used when Nmap is unable to determine whether a port is closed or filtered. It is only used for the IP ID idle scan.
```
