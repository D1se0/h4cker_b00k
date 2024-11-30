# Descubrimiento de hosts (Host Discovery)

La primera tecnica que utilizaremos sera la llamada `Host Discovery`, lo haremos frente a las maquinas de nuestro entorno las llamadas `metasploitable3` tanto la de `windows` como la de `linux`.

Vamos a empezar con esta herramienta descubriendo que hosts hay conectados a esta red actual con el siguiente comando:

```shell
nmap -sn 192.168.16.0/24
```

Hay que poner el rango de red en la que estamos, que esto se identifca viendo el penultimo numero de nuestra IP y poniendo en el ultimo numero un `0` y despues poniendo el tipo de IP que sea, lo normal es que sea el generico `/24`.

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-10 11:23 EST
Nmap scan report for 192.168.16.1
Host is up (0.00060s latency).
MAC Address: 00:50:56:C0:00:01 (VMware)
Nmap scan report for 192.168.16.129
Host is up (0.00014s latency).
MAC Address: 00:0C:29:29:E7:FF (VMware)
Nmap scan report for 192.168.16.132
Host is up (0.00032s latency).
MAC Address: 00:0C:29:EC:1E:B9 (VMware)
Nmap scan report for 192.168.16.254
Host is up (0.00059s latency).
MAC Address: 00:50:56:E0:99:54 (VMware)
Nmap scan report for 192.168.16.128
Host is up.
Nmap done: 256 IP addresses (5 hosts up) scanned in 27.94 seconds
```

Y nos sacara las 2 maquinas que estan conectadas a la red las `metasploitables` que serian las siguientes IP's:

```
192.168.16.129
192.168.16.132
```

Si se ejecuta sin privilegios elevados `nmap` el funcionamiento que va a tener es que para identificar los `nodos` que estan conectados a la red y lo que estan activos es haciendolo mediante los puertos `80` y `443`, mediante el protocolo `TCP/IP`, pero si lo hacemos con privilegios elevados, para identificar las maquinas que estan conectadas y activas en la red, lo va hacer mediante el protocolo `ARP` que este consiste en que nosotros preguntamos al rango de red (`mediante el Broadcast`) entero quien es tal IP enviando una serie de paquetes de red con dicha IP y el que coincida con dicha IP nos devuelve como respuesta la `MAC` (IP fisica) del nodo en cuestion, por lo que podremos identificarlo de esa forma, ya que el protocolo `ARP` funciona de esa forma se identifica mediante la IP fisica del equipo `MAC`.

Una vez sabiendo los `hosts` que estan corriendo en nuestra red, si hacemos el siguiente comando con alguna de las 2 IP's:

```shell
nmap -PS 192.168.16.129
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-10 11:46 EST
Nmap scan report for 192.168.16.129
Host is up (0.00021s latency).
Not shown: 990 closed tcp ports (reset)
PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
80/tcp   open  http
111/tcp  open  rpcbind
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
631/tcp  open  ipp
3306/tcp open  mysql
6667/tcp open  irc
8080/tcp open  http-proxy
MAC Address: 00:0C:29:29:E7:FF (VMware)

Nmap done: 1 IP address (1 host up) scanned in 13.25 seconds
```

Por lo que vemos con el parametro `-PS` lo que hacemos es probar todos los puertos y ver cuales nos responden mostrando solo los resultados de los cuales estan activos, el unico inconveniente es que este tipo de escaneos hacen mucho ruido, mucho trafico de red, pero si queremos no hacer tanto trafico de red y solamente escanear un puerto en concreto para verificar si esta activo o no, podremos hacerlo de la siguiente forma:

```shell
nmap -PS 192.168.16.129 -p 80
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-10 11:51 EST
Nmap scan report for 192.168.16.129
Host is up (0.00028s latency).

PORT   STATE SERVICE
80/tcp open  http
MAC Address: 00:0C:29:29:E7:FF (VMware)

Nmap done: 1 IP address (1 host up) scanned in 13.14 seconds
```

Aqui nos esta diciendo que el puerto `80` esta activo (`open`), sin hacer tanto trafico de red.

Para verificar que el `host` al que queremos escanear dicho puerto esta activo, se puede hacer añadiendole al parametro `-PS` un par de puertos para verificar si estan activos y de ser asi le respondera por lo que verificara que esta activo el `host` y despues escaneara el puerto de `-p` una vez verificado esto anterior:

```shell
nmap -PS21,22,23 192.168.16.129 -p 21
```
